import RPi.GPIO as GPIO
import time
import threading
import subprocess

# Motor GPIO Pins
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
ENA = 12  # Left Motor Enable (PWM)
ENB = 13  # Right Motor Enable (PWM)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# PWM for speed control
speed_left = GPIO.PWM(ENA, 1000)  # 1 kHz PWM frequency
speed_right = GPIO.PWM(ENB, 1000)

speed_left.start(70)  # Start motors at 70% speed
speed_right.start(70)

# Function to move forward
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

# Function to stop
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Function to start live video feed using libcamera
def start_camera():
    print("Starting live camera feed...")
    subprocess.run(["libcamera-vid", "-t", "0", "--inline", "--width", "640", "--height", "480", "--framerate", "30", "-o", "-", "|", "ffplay", "-"], shell=True)

# Run motor and camera together using threading
try:
    print("Car is moving forward...")

    # Start live camera feed in a separate thread
    camera_thread = threading.Thread(target=start_camera)
    camera_thread.start()

    # Move forward
    forward()

    # Keep running until interrupted
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping car...")
    stop()
    speed_left.stop()
    speed_right.stop()
    GPIO.cleanup()
    print("Program exited and GPIO cleaned up.")