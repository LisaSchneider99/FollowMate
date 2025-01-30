from picamera2 import Picamera2
import cv2
import numpy as np

def nothing(x):
    pass

# Initialize Camera
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

# Create a single OpenCV window
cv2.namedWindow('Camera')
cv2.resizeWindow('Camera', 640, 480)

# Create trackbars inside the same window
cv2.createTrackbar('Low H', 'Camera', 0, 179, nothing)
cv2.createTrackbar('Low S', 'Camera', 0, 255, nothing)
cv2.createTrackbar('Low V', 'Camera', 0, 255, nothing)
cv2.createTrackbar('High H', 'Camera', 179, 179, nothing)
cv2.createTrackbar('High S', 'Camera', 255, 255, nothing)
cv2.createTrackbar('High V', 'Camera', 255, 255, nothing)

while True:
    # Capture image from camera
    frame = picam2.capture_array()

    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Get color limits from trackbars
    low_h = cv2.getTrackbarPos('Low H', 'Camera')
    low_s = cv2.getTrackbarPos('Low S', 'Camera')
    low_v = cv2.getTrackbarPos('Low V', 'Camera')
    high_h = cv2.getTrackbarPos('High H', 'Camera')
    high_s = cv2.getTrackbarPos('High S', 'Camera')
    high_v = cv2.getTrackbarPos('High V', 'Camera')

    # Create mask for color boundaries
    lower_bound = np.array([low_h, low_s, low_v])
    upper_bound = np.array([high_h, high_s, high_v])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours
    for contour in contours:
        if cv2.contourArea(contour) > 2:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    # Show image with trackbars
    cv2.imshow('Camera', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
picam2.stop()
cv2.destroyAllWindows()
