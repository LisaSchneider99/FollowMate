import cv2
import numpy as np

from parameters import *

def detect_target(original_frame,color):
  frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB) #Convert color from BGR to RGB 
  hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) #Convert frame to hsv for further analysis 

  #print(f"Color: {color}")
  match color: #Check hsv frame for specific color
    case 'blue':
      mask = cv2.inRange(hsv, LOWER_COLOR_BLUE, UPPER_COLOR_BLUE)
    case 'pink':
      mask = cv2.inRange(hsv, LOWER_COLOR_PINK, UPPER_COLOR_PINK)
    case 'green':
      mask = cv2.inRange(hsv, LOWER_COLOR_GREEN, UPPER_COLOR_GREEN)
    case 'yellow':
      mask = cv2.inRange(hsv, LOWER_COLOR_YELLOW, UPPER_COLOR_YELLOW)
    case 'orange':
      mask = cv2.inRange(hsv, LOWER_COLOR_ORANGE, UPPER_COLOR_ORANGE)
    case 'red':
      mask = cv2.inRange(hsv, LOWER_COLOR_RED, UPPER_COLOR_RED)
    case _ :
      mask = cv2.inRange(hsv, LOWER_COLOR_RED, UPPER_COLOR_RED)

  contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find contours mask created from hsv frame

  if contours: #Check for the biggest contour
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = contours[0]

    area = cv2.contourArea(largest_contour) #Calculate contour area

    # Calculation Contour center
    moments = cv2.moments(largest_contour) #Contour middle of contour

    if moments["m00"] != 0:
      x = int(moments["m10"] / moments["m00"])
      y = int(moments["m01"] / moments["m00"])
      #print(f"Schwerpunkt ({x},{y})")

    # Calculation Rotationrectangle 
    rot_rect = cv2.minAreaRect(largest_contour) 
    box = cv2.boxPoints(rot_rect) 
    box = np.int0(box)

    # Calculation height
    edge_lengths = [
                    np.linalg.norm(box[1] - box[0]),
                    np.linalg.norm(box[2] - box[1])
                   ]
    height = min(edge_lengths)
    
    if area < 50:
      return 0,0,0,frame,0
    else: 
      cv2.drawContours(frame,[largest_contour],-1,(0,0,255),2)
      cv2.drawContours(frame,[box],-1,(255,0,0),2)
      cv2.imshow("Frame", frame)
      return x, y,height,frame,area
      
  
  else:
    #print("Referenzobjekt nicht gefunden. Bitte sicherstellen, dass die Farbeinstellungen korrekt sind.")
    
    
    return 0,0,0,frame,0

def calculate_distance_to_target(perceived_height):
    # Berechne die Entfernung
    if perceived_height > 0:
        distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / perceived_height
    else: 
      distance = -1
        
    return distance
    
def calculate_distance_to_target_area(area):
    perceived_area = area
    if perceived_area > 0:
      return np.sqrt((KNOWN_AREA * FOCAL_LENGTH**2) / perceived_area) 
    else:
      return -1

