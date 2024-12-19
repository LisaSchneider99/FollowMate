from robot_hat import Servo
from robot_hat.utils import reset_mcu
from time import sleep

from parameters import *

def servo_zeroing():
 if STATUS:
  print(f"[Status] Set servo to zero")
 for i in range(12):
   # print(f"Servo {i} set to zero")
   Servo(i).angle(10)
   sleep(0.1)
   Servo(i).angle(0)
   sleep(0.1)