from picarx import Picarx
import numpy as np
from parameters import *

pan_angle,tilt_angle = 0,0

def clamp_number(num,a,b):
  return max(min(num, max(a, b)), min(a, b))

def calculate_offset(x,y):
  image_center_x = image_size[0]/2
  image_center_y = image_size[1]/2
  
  object_center_x = x
  object_center_y = y
  
  offset_x = object_center_x - image_center_x
  offset_y = object_center_y - image_center_y

  return offset_x, offset_y
  
  
def angle_calculation(offset_x, offset_y, distance_to_target):
  global pan_angle,tilt_angle
  
  pan_angle_temp = (offset_x/image_size[0]) * FOV_HORIZONTAL
  pan_angle = pan_angle_temp
  pan_angle = clamp_number(pan_angle,-25,25)
  
  tilt_angle_temp =  -(offset_y/image_size[1]) * FOV_VERTICAL
  tilt_angle = tilt_angle_temp
  tilt_angle = clamp_number(tilt_angle,-35,35)

  def reduce_angle(value):
    if abs(value) > 5:
      if value > 0:
        value -= 5
      else:
        value += 5
    else: 
      value = 0
    return value

  pan_angle = reduce_angle(pan_angle)
  tilt_angle = reduce_angle(tilt_angle)

def set_pan_angle(angle):
  global pan_angle
  pan_angle = angle

def set_tilt_angle(angle):
  global tilt_angle
  tilt_angle = angle

def get_pan_angle():
  global pan_angle
  return pan_angle 

def get_tilt_angle():
  global tilt_angle
  return tilt_angle
  

  
