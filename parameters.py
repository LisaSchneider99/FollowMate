import numpy as np

STATUS = False

FOCAL_LENGTH = 624  # Beispielwert f�r die Fokusl�nge, an deine Kamera anpassen 

# Bekannte Parameter f�r das Referenzobjekt
KNOWN_HEIGHT = 2.0  # tats�chliche Breite des Referenzobjekts in cm
KNOWN_AREA = 10.0

LOWER_COLOR_GREEN = np.array([25, 180, 45])
UPPER_COLOR_GREEN = np.array([45, 255, 255])

LOWER_COLOR_PINK = np.array([120, 90, 100])
UPPER_COLOR_PINK = np.array([140, 255, 255]) #Currently not used

LOWER_COLOR_ORANGE = np.array([105, 200, 70])
UPPER_COLOR_ORANGE = np.array([115, 255, 255])

LOWER_COLOR_YELLOW = np.array([90, 192, 115]) 
UPPER_COLOR_YELLOW = np.array([105, 255, 255])

LOWER_COLOR_BLUE = np.array([0, 150, 50])
UPPER_COLOR_BLUE = np.array([20, 255, 185])

LOWER_COLOR_RED = np.array([115, 150, 50]) #200
UPPER_COLOR_RED = np.array([140, 255, 225]) #140

image_size = (640,480)
FOV_HORIZONTAL = 52.1
FOV_VERTICAL = 41.8

RATE = 44100 # Abtastrate 
CHUNK = 4096 # Anzahl der Frames pro Puffer 

pan_angle = 0 
tilt_angle = 0 