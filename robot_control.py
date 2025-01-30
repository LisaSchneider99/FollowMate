from parameters import *
from robot_hat import Servo
from time import sleep

# Initialize pan and tilt angles
pan_angle, tilt_angle = 0, 0

def clamp_number(num, a, b):
    """
    Clamps a number between two given bounds.
    
    Args:
        num (float): The number to be clamped.
        a (float): The lower bound.
        b (float): The upper bound.
    
    Returns:
        float: The clamped number.
    """
    return max(min(num, max(a, b)), min(a, b))

def calculate_offset(x, y):
    """
    Calculates the offset of the detected object from the image center.
    
    Args:
        x (int): X-coordinate of the object center.
        y (int): Y-coordinate of the object center.
    
    Returns:
        tuple: Offset values (offset_x, offset_y).
    """
    image_center_x = image_size[0] / 2
    image_center_y = image_size[1] / 2
    
    offset_x = x - image_center_x
    offset_y = y - image_center_y
    
    return offset_x, offset_y

def angle_calculation(offset_x, offset_y, distance_to_target):
    """
    Calculates the pan and tilt angles based on the object's position and distance.
    
    Args:
        offset_x (float): Horizontal offset from the center.
        offset_y (float): Vertical offset from the center.
        distance_to_target (float): Distance to the target.
    """
    global pan_angle, tilt_angle
    
    pan_angle_temp = (offset_x / image_size[0]) * FOV_HORIZONTAL
    pan_angle = clamp_number(pan_angle_temp, -25, 25) # Clamping to stop wheels from getting stuck when angle is too high.
    
    tilt_angle_temp = -(offset_y / image_size[1]) * FOV_VERTICAL
    tilt_angle = clamp_number(tilt_angle_temp, -35, 35)
    
    def reduce_angle(value):
        """ Gradually reduces the angle towards zero if its absolute value is greater than 5. """
        if abs(value) > 5:
            return value - 5 if value > 0 else value + 5
        return 0
    
    pan_angle = reduce_angle(pan_angle)
    tilt_angle = reduce_angle(tilt_angle)

def servo_zeroing():
    """
    Resets all servos to the zero position.
    """
    if STATUS:
        print(f"[Status] Set servo to zero")
    
    for i in range(12):
        Servo(i).angle(10)
        sleep(0.1)
        Servo(i).angle(0)
        sleep(0.1)

def set_pan_angle(angle):
    """ Sets the pan angle. """
    global pan_angle
    pan_angle = angle

def set_tilt_angle(angle):
    """ Sets the tilt angle. """
    global tilt_angle
    tilt_angle = angle

def get_pan_angle():
    """ Returns the current pan angle. """
    global pan_angle
    return pan_angle

def get_tilt_angle():
    """ Returns the current tilt angle. """
    global tilt_angle
    return tilt_angle
