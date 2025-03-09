import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Define motor control pins
IN1, IN2 = 17, 18  # Left Motor
IN3, IN4 = 22, 23  # Right Motor
ENA, ENB = 12, 13  # PWM for Speed Control

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)
speed_left = GPIO.PWM(ENA, 1000)
speed_right = GPIO.PWM(ENB, 1000)
speed_left.start(70)
speed_right.start(70)

# Car movement functions
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def get_lane_info(image):
    """Detect road (blue) and lane boundaries (yellow)."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Detect Blue Road
    lower_blue = np.array([34, 36, 139])
    upper_blue = np.array([51, 53, 155])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Detect Yellow Lane Boundaries
    lower_yellow = np.array([203, 183, 1])
    upper_yellow = np.array([208, 188, 73])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cx_road = None
    if contours_blue:
        largest_contour = max(contours_blue, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] > 0:
            cx_road = int(M["m10"] / M["m00"])  

    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    left_boundary, right_boundary = None, None
    if contours_yellow:
        yellow_x_positions = [cv2.boundingRect(cnt)[0] for cnt in contours_yellow]
        left_boundary = min(yellow_x_positions)  # Leftmost yellow lane
        right_boundary = max(yellow_x_positions)  # Rightmost yellow lane

    return cx_road, left_boundary, right_boundary

# Opens camera
cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_width = frame.shape[1]
        cx_road, left_boundary, right_boundary = get_lane_info(frame)

        if cx_road and left_boundary and right_boundary:
            if cx_road < left_boundary or cx_road > right_boundary:
                print("🚨 Car is crossing the lane! Stopping!")
                stop()
            else:
                if cx_road < frame_width // 2 - 50:
                    print("Turning Left")
                    left()
                elif cx_road > frame_width // 2 + 50:
                    print("Turning Right")
                    right()
                else:
                    print("Moving Forward")
                    forward()
        else:
            print("No clear lane detected, stopping")
            stop()

        cv2.imshow("Lane Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    print("Car Stopped and Cleaned Up")