import cv2
import numpy as np

from parameters import *

def detect_target(original_frame, color):
    """
    Detects a specific color target in the given frame and calculates its position and size.

    Args:
        original_frame (numpy.ndarray): The input image frame.
        color (str): The target color to detect (e.g., 'blue', 'red', etc.).

    Returns:
        tuple: (x, y, height, frame) where:
            - x (int): X-coordinate of the detected target's center.
            - y (int): Y-coordinate of the detected target's center.
            - height (float): Estimated height of the detected target.
            - frame (numpy.ndarray): The processed image frame with drawn contours.
    """
    frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)  # Convert color from BGR to RGB
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # Convert frame to HSV for further analysis

    # Select the appropriate HSV range for the given color
    match color:
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
        case _:
            mask = cv2.inRange(hsv, LOWER_COLOR_RED, UPPER_COLOR_RED)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:  # Check if any contours are found
        contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort contours by area (largest first)
        largest_contour = contours[0]

        area = cv2.contourArea(largest_contour)  # Calculate contour area

        # Calculate the center of the contour
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            x = int(moments["m10"] / moments["m00"])
            y = int(moments["m01"] / moments["m00"])
        else:
            x, y = 0, 0

        # Compute the minimum area rectangle around the contour
        rot_rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rot_rect)
        box = np.int0(box)

        # Calculate height as the smaller side of the bounding rectangle
        edge_lengths = [
            np.linalg.norm(box[1] - box[0]),
            np.linalg.norm(box[2] - box[1])
        ]
        height = min(edge_lengths)

        if area < 50: # if area is too small
            return 0, 0, 0, frame
        else:
            # Draw the contours on the frame
            cv2.drawContours(frame, [largest_contour], -1, (0, 0, 255), 2)
            cv2.drawContours(frame, [box], -1, (255, 0, 0), 2)
            return x, y, height, frame
    else:
        return 0, 0, 0, frame

def calculate_distance_to_target(perceived_height):
    """
    Calculates the distance to the target based on its perceived height.

    Args:
        perceived_height (float): The detected height of the target in pixels.

    Returns:
        float: Estimated distance to the target, or -1 if height is invalid.
    """
    if perceived_height > 0:
        return (KNOWN_HEIGHT * FOCAL_LENGTH) / perceived_height
    else:
        return -1

def calculate_distance_to_target_area(area):
    """
    Calculates the distance to the target based on its detected area.

    Args:
        area (float): The detected area of the target in pixels.

    Returns:
        float: Estimated distance to the target, or -1 if area is invalid.
    """
    if area > 0:
        return np.sqrt((KNOWN_AREA * FOCAL_LENGTH**2) / area)
    else:
        return -1
