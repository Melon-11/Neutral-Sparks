import RPi.GPIO as GPIO
import time

# Define Motor Control Pins
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
ENA = 12
ENB = 13

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)
GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

# PWM Setup (Speed Control)
pwmA = GPIO.PWM(ENA, 1000)  
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(50)  
pwmB.start(50)

speed = 50  

def set_speed(value):
    global speed
    speed = max(0, min(100, value))  
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    print(f"Speed set to {speed}%")

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Moving Forward")

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Moving Backward")

def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print("Turning Left")

def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print("Turning Right")

def stop():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("Stopping")

def main():
    print("Control Car with W/A/S/D. Use '+' to increase speed, '-' to decrease speed. Press 'Q' to quit.")
    try:
        while True:
            command = input("Enter command: ").strip().lower()
            if command == 'w':
                forward()
            elif command == 's':
                backward()
            elif command == 'a':
                left()
            elif command == 'd':
                right()
            elif command == '+':
                set_speed(speed + 10)
            elif command == '-':
                set_speed(speed - 10)
            elif command == 'q':
                print("Exiting...")
                break
            else:
                stop()
    except KeyboardInterrupt:
        pass
    finally:
        stop()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
        print("GPIO Cleaned Up. Program Stopped.")

if _name_ == "_main_":
    main()