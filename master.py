# -*- coding: utf-8 -*- 

#-------------Import Libraries-------------

import sys
import cv2
import numpy as np
import picamera2 as picamera
import time
from picarx import Picarx
from robot_hat import Servo, Motors
import threading
import queue
from time import sleep
from robot_hat import Music,TTS
import readchar
import subprocess
import speech_recognition as sr

#-------------Import additional python files-------------

from parameters import *
from timer import *
import camera as cam
import head_control as hc
import wheel_control as wc
import micro as mc

class LatestQueue(queue.Queue):
    def put(self, item, block=True, timeout=None):
        # Ersetzt den alten Inhalt durch den neuesten Wert
        with self.mutex:  # Gewährleistet Thread-Sicherheit
            self.queue.clear()  # Löscht alte Werte
        super().put(item, block, timeout)

#-------------Camera Thread-------------

def camera_thread_function():
  global initial_target
  global color
  target = False
  counter = 0

  while True:
  
    distance_to_target_cam = [] #Distance calculated by camera frame analysis
    distance_to_target_us = [] #Distance calculated by ultra sound module
    
    current_x = 0 #current 
    current_y = 0 
  
    for i in range(0,1):
      frame = camera.capture_array()  
      frame = cv2.resize(frame, (640,480)) #resize camera frame to 640x480
      if STATUS:
        print(f"[Status] Frame captured")
      
      x,y,height,frame_2,area = cam.detect_target(frame,color)
      
      if x != 0:
        current_x = x
        
      if y != 0:
        current_y = y       
      
      resized_image = cv2.resize(frame_2, (640,480))
      cv2.imshow("Frame", resized_image)
      cv2.waitKey(1)
      
      current_distance_to_target_cam = cam.calculate_distance_to_target(height)
      current_distance_to_target_us = round(px.ultrasonic.read(), 2)
      
      distance_to_target_us.append(current_distance_to_target_us)
      
      if current_distance_to_target_cam != -1:
        distance_to_target_cam.append(current_distance_to_target_cam)
        if target == False:
          initial_target = True
          target = True
          tts.say("Following Target")
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
    
    data = (median_distance_to_target_cam,median_distance_to_target_us, current_x, current_y,target)
    
    latest_queue.put(data)
    
#-------------Servo Thread-------------
    
def servo_thread_function():
    global px
    global initial_target
    global start_time, current_time
    global pan_angle,tilt_angle

    data = 0,0,0,0,0
    
    while True:
      data = latest_queue.get()
      #print(data)
      
      if STATUS:
        print(f"[Status] Data: {data}")

      median_distance_to_target_cam,median_distance_to_target_us, x, y, target = data
      
      if abs(median_distance_to_target_cam - median_distance_to_target_us) < 20 and median_distance_to_target_cam != -1 and median_distance_to_target_us != -1:
        distance = median_distance_to_target_us
      else:
        distance = median_distance_to_target_cam
      if median_distance_to_target_us > 10 and median_distance_to_target_us != -1: 
    
        if target == True and x != 0 and y != 0 and median_distance_to_target_us > 10:
          #print("Target True")
          start_time = 0
          offset_x , offset_y = hc.calculate_offset(x,y)
        
          hc.angle_calculation(offset_x, offset_y, median_distance_to_target_cam)
          
          pan = hc.get_pan_angle()
          tilt = hc.get_tilt_angle()

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
              hc.set_pan_angle(15)
          if current_time - start_time > 2 and current_time - start_time < 3 and start_time != 0:
              px.set_cam_pan_angle(30) 
              px.set_dir_servo_angle(30)
              hc.set_pan_angle(30) 
          if current_time - start_time > 3 and current_time - start_time < 4 and start_time != 0:
              px.set_cam_pan_angle(-15) 
              px.set_dir_servo_angle(-15)
              hc.set_pan_angle(-15) 
          if current_time - start_time > 4 and current_time - start_time < 5 and start_time != 0:
              px.set_cam_pan_angle(-30) 
              px.set_dir_servo_angle(-30)
              hc.set_pan_angle(-30)         
          if current_time - start_time > 5 and current_time - start_time < 6 and start_time != 0:
              px.set_dir_servo_angle(0)
              px.set_cam_pan_angle(0) 
              hc.set_pan_angle(0)
              px.backward(10)
          elif current_time - start_time > 6 and current_time - start_time < 7 and start_time != 0: #If robot drove backwards for two seconds, Target ist completely lost. Stop Robot and play status message
            px.stop()
            tts.say("Lost Target")
          else: 
            px.stop()
      elif median_distance_to_target_us != -1: 
        print(median_distance_to_target_us)
        px.stop()
        tts.say("I can not drive forward. My way is blocked")
        px.backward(10)
        time.sleep(1)
        px.stop()
#-------------Microphone routine-------

def micro_thread_function():
  global color
  recognizer = sr.Recognizer()

  with sr.Microphone(sample_rate = RATE, chunk_size = CHUNK) as source:
    print("Kalibriere Mikrofon für Umgebungsgeräusche...")
    recognizer.adjust_for_ambient_noise(source)
    print("Bereit. Sprechen Sie, um erkannt zu werden.")

    try:
        while True:
            print("\nHöre zu...")
            # Audio aufnehmen
            audio_data = recognizer.listen(source)

            # Verstärke das Audio
            #amplified_audio = mc.process_audio(audio_data)

            # Sprache in Text umwandeln
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                print("Erkannter Text:", text)
                text_lower = text.lower()
                #print(f"text_lower {text_lower}")
                for colors in ["green", "blue", "pink", "yellow", "red", "orange"]:
                  if colors in text_lower: #and color != colors:
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
                print("Entschuldigung, ich konnte Sie nicht verstehen.")            
            except sr.RequestError as e:
                print(f"Fehler beim Abrufen der Ergebnisse: {e}")

    except KeyboardInterrupt:
        print("\nBeende die Erkennung.")


#-------------Main routine-------------
        
try: 
  # Initial setup
  initial_target = False
  start_time = 0
  current_time = 0
  color = "red"

  px = Picarx()
  
  wc.servo_zeroing()
    
  latest_queue = LatestQueue()
  
  tts = TTS()
  tts.lang("en-US")
  tts.say("Hello my name is Picar X. I am now following you around")
  
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
      
finally: 
  px.stop()
  if STATUS:
    print("[Status] Picar has stopped")
  

  
    
  