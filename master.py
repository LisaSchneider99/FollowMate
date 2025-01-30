# -*- coding: utf-8 -*- 

#-------------Import Libraries-------------

import cv2
import numpy as np
import picamera2 as picamera
import time
from picarx import Picarx
import threading
import queue
from robot_hat import TTS
import speech_recognition as sr

#-------------Import additional python files and classes -------------

from parameters import *
import camera as cam
import robot_control as rc

class LatestQueue(queue.Queue):
    """
    Custom queue that always keeps only the latest item.
    """
    def put(self, item, block=True, timeout=None):
        # Replaces old value with newest one
        with self.mutex:  # Ensures thread saftey
            self.queue.clear()  # Deletes old values
        super().put(item, block, timeout)

#-------------Camera Thread-------------

def camera_thread_function():
  """
  Captures frames from the camera, detects a target of a specific color, and calculates its distance.
  """
  global initial_target
  global color
  target = False

  while True:
  
    distance_to_target_cam = [] #Distance calculated by camera frame analysis
    distance_to_target_us = [] #Distance calculated by ultra sound module
    
    current_x = 0 
    current_y = 0 
  
    for i in range(0,1):
      frame = camera.capture_array()  
      frame = cv2.resize(frame, (640,480)) #resize camera frame to 640x480
      if STATUS:
        print(f"[Status] Frame captured")
      
      x,y,height,processed_frame = cam.detect_target(frame,color)
      
      if x != 0:
        current_x = x
        
      if y != 0:
        current_y = y       
      
      # Show current processed image
      resized_image = cv2.resize(processed_frame, (640,480))
      cv2.imshow("Frame", resized_image)
      cv2.waitKey(1)
      
      # Get distance values (Camera and Ultrasonic)
      current_distance_to_target_cam = cam.calculate_distance_to_target(height)
      current_distance_to_target_us = round(px.ultrasonic.read(), 2)
      
      distance_to_target_us.append(current_distance_to_target_us)
      
      if current_distance_to_target_cam != -1:
        distance_to_target_cam.append(current_distance_to_target_cam)
        if target == False:
          initial_target = True
          target = True
          if STATUS:
            print("[Status] Following Target")
        
      if len(distance_to_target_cam) == 0 and target == True:
        target = False
        if STATUS:
          print("[Status] Target lost")
    
    if len(distance_to_target_cam) != 0:
      median_distance_to_target_cam = np.median(distance_to_target_cam)
    else:
      median_distance_to_target_cam = -1

    if len(distance_to_target_us) != 0:
      median_distance_to_target_us = np.median(distance_to_target_us)  
    else:
      median_distance_to_target_us = -1
    
    if median_distance_to_target_us == -2: 
      median_distance_to_target_us = -1
    
    # Put data in queue
    data = (median_distance_to_target_cam,median_distance_to_target_us, current_x, current_y,target)
    latest_queue.put(data) 
    
#-------------Servo Thread-------------

def servo_thread_function():
    """
    Controls the servo motors and directs the robot towards the detected target.
    """
    global px
    global initial_target
    global start_time, current_time
    global pan_angle,tilt_angle

    data = 0,0,0,0,0
    
    while True:
      data = latest_queue.get() # Get data from queue
      
      if STATUS:
        print(f"[Status] Data: {data}")

      median_distance_to_target_cam,median_distance_to_target_us, x, y, target = data
      
      # Decide which distance value is more reliable (Camera or Ultrasonic)
      if abs(median_distance_to_target_cam - median_distance_to_target_us) < 20 and median_distance_to_target_cam != -1 and median_distance_to_target_us != -1:
        distance = median_distance_to_target_us
      else:
        distance = median_distance_to_target_cam

      if median_distance_to_target_us > 10 and median_distance_to_target_us != -1:   
    
        if target == True and x != 0 and y != 0:
          start_time = 0
          offset_x , offset_y = rc.calculate_offset(x,y)
        
          rc.angle_calculation(offset_x, offset_y, median_distance_to_target_cam)
          
          pan = rc.get_pan_angle()
          tilt = rc.get_tilt_angle()

          px.set_cam_tilt_angle(tilt)
          px.set_cam_pan_angle(pan)
          px.set_dir_servo_angle(pan)
          
          if STATUS:
            print(f"[Status] Distance to target: {distance }")
            
          # Driving algorithms
          if distance > 50: #Only drive forward if distance is greater than 50cm
            px.forward(10)
          else: #If distance is smaller than 50cm stop the robot
            px.stop()
        elif target == False and initial_target == True and median_distance_to_target_us > 10: #If the previously detected target was lost
          #Timer to be able to drive backwards for 2 seconds maximum while trying to find the lost target again
          if start_time == 0: 
            start_time = time.time() #Start time for the timer (The moment the target was lost)
          else:
            current_time = time.time() #Current time

          if current_time - start_time > 1 and current_time - start_time < 2 and start_time != 0: #When time difference between start and current moment is smaller than 2 seconds, drive backwards to find target again
              px.set_cam_pan_angle(15)
              px.set_dir_servo_angle(15)
              rc.set_pan_angle(15)
          if current_time - start_time > 2 and current_time - start_time < 3 and start_time != 0:
              px.set_cam_pan_angle(30) 
              px.set_dir_servo_angle(30)
              rc.set_pan_angle(30) 
          if current_time - start_time > 3 and current_time - start_time < 4 and start_time != 0:
              px.set_cam_pan_angle(-15) 
              px.set_dir_servo_angle(-15)
              rc.set_pan_angle(-15) 
          if current_time - start_time > 4 and current_time - start_time < 5 and start_time != 0:
              px.set_cam_pan_angle(-30) 
              px.set_dir_servo_angle(-30)
              rc.set_pan_angle(-30)         
          if current_time - start_time > 5 and current_time - start_time < 6 and start_time != 0:
              px.set_dir_servo_angle(0)
              px.set_cam_pan_angle(0) 
              rc.set_pan_angle(0)
              px.backward(10)
          elif current_time - start_time > 6 and current_time - start_time < 7 and start_time != 0: #If robot drove backwards for two seconds, Target ist completely lost. Stop Robot and play status message
            px.stop()
            tts.say("Lost Target")
          else: 
            px.stop()
      elif median_distance_to_target_us != -1 and median_distance_to_target_us < 10: 
        print(median_distance_to_target_us)
        px.stop()
        tts.say("I can not drive forward. My way is blocked")
        px.backward(10)
        time.sleep(1)
        px.stop()
#-------------Microphone routine-------

def micro_thread_function():
  """
  Listens for voice commands and updates the target color accordingly.
  """
  global color
  recognizer = sr.Recognizer()

  with sr.Microphone(sample_rate = RATE, chunk_size = CHUNK) as source:
    print("Calibrate microphone for ambient sound...")
    recognizer.adjust_for_ambient_noise(source)
    print("Ready. You can speak now.")

    try:
        while True:
            print("\nListening...")
            audio_data = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                print("Recognized Text:", text)
                text_lower = text.lower()
                for colors in ["green", "blue", "pink", "yellow", "red", "orange"]:
                  if colors in text_lower: 
                    color = colors
                    match color: #Check hsv frame for specific color
                      case "blue":
                        tts.say("Blue target chosen")
                      case "pink":
                        tts.say("Pink target chosen")
                      case 'green':
                       tts.say("Green target chosen")
                      case 'yellow':
                       tts.say("Yellow target chosen")
                      case 'orange':
                        tts.say("Orange target chosen")
                      case 'red':
                        tts.say("Red target chosen")
                      case _ :
                        tts.say("No color selected.")
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand you.")            
            except sr.RequestError as e:
                print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nEnd of speech recognition.")


#-------------Main routine-------------
        
try: 
  # Initial setup
  initial_target = False
  start_time = 0
  current_time = 0
  color = "green"

  px = Picarx()
  
  rc.servo_zeroing()
    
  latest_queue = LatestQueue()
  
  camera = picamera.Picamera2()  # Initialize Camera
  camera.configure(camera.create_still_configuration())  # Configure camera for still pictures
  camera.resolution = image_size  #Set resolution to preconfigured image size
  camera.start()  #Start camera
  if STATUS:
    print("[Status] Camera initialized")
    
  time.sleep(2) #Wait short time for camera to initialize
  
  camera_thread = threading.Thread(target=camera_thread_function)
  servo_thread = threading.Thread(target=servo_thread_function)
  micro_thread = threading.Thread(target=micro_thread_function)
  camera_thread.start()
  servo_thread.start()
  micro_thread.start()

  tts = TTS()
  tts.lang("en-US")
  tts.say("Hello my name is Follow Mate. I am now following you around")
      
finally: 
  px.stop()
  if STATUS:
    print("[Status] Picar has stopped")
  

  
    
  