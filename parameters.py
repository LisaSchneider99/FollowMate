import numpy as np

# Enable or disable status messages
STATUS = False

# Focal length of the camera in pixels
FOCAL_LENGTH = 624  

# Known parameters for the reference object
KNOWN_HEIGHT = 2.0  # Actual height of the reference object in cm
KNOWN_AREA = 10.0   # Actual area of the reference object in cm²

# HSV color thresholds for different colors
LOWER_COLOR_GREEN = np.array([25, 180, 45])
UPPER_COLOR_GREEN = np.array([45, 255, 255])

LOWER_COLOR_PINK = np.array([120, 90, 100])
UPPER_COLOR_PINK = np.array([140, 255, 255]) 

LOWER_COLOR_ORANGE = np.array([105, 200, 70])
UPPER_COLOR_ORANGE = np.array([115, 255, 255])

LOWER_COLOR_YELLOW = np.array([90, 192, 115]) 
UPPER_COLOR_YELLOW = np.array([105, 255, 255])

LOWER_COLOR_BLUE = np.array([0, 150, 50])
UPPER_COLOR_BLUE = np.array([20, 255, 185])

LOWER_COLOR_RED = np.array([115, 150, 50]) 
UPPER_COLOR_RED = np.array([140, 255, 225]) 

image_size = (640, 480) # Image resolution settings
FOV_HORIZONTAL = 52.1  # Horizontal field of view in degrees
FOV_VERTICAL = 41.8    # Vertical field of view in degrees

# Audio settings
RATE = 44100  # Sampling rate
CHUNK = 4096  # Number of frames per buffer
