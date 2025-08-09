import time
import serial
import RPi.GPIO as GPIO
from picamera import PiCamera

# -----------------------------
# Configuration
# -----------------------------
SERIAL_PORT = '/dev/ttyUSB0'  # Change as per your USB port
BAUD_RATE = 115200
SERVO_PIN = 17  # GPIO pin for the servo

# Servo PWM settings
SERVO_LEFT_DUTY = 2.5    # Duty cycle for left position
SERVO_RIGHT_DUTY = 12.5  # Duty cycle for right position
SERVO_MID_DUTY = 7.5     # Duty cycle for mid position

# -----------------------------
# Setup
# -----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
servo_pwm.start(SERVO_MID_DUTY)

camera = PiCamera()
camera.resolution = (640, 480)

# Serial setup
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)

def cleanup():
    servo_pwm.stop()
    GPIO.cleanup()
    camera.close()
    ser.close()

def move_servo(direction):
    if direction == "left":
        servo_pwm.ChangeDutyCycle(SERVO_LEFT_DUTY)
    elif direction == "right":
        servo_pwm.ChangeDutyCycle(SERVO_RIGHT_DUTY)
    elif direction == "mid":
        servo_pwm.ChangeDutyCycle(SERVO_MID_DUTY)
    else:
        print("Unknown direction:", direction)
    time.sleep(1)
    servo_pwm.ChangeDutyCycle(SERVO_MID_DUTY)  # Return to mid position

def take_picture(filename="capture.jpg"):
    camera.capture(filename)
    return filename

def send_image(filename):
    with open(filename, "rb") as f:
        data = f.read()
        # Send file size first
        ser.write(f"SIZE:{len(data)}\n".encode())
        ack = ser.readline()
        if b"OK" in ack:
            ser.write(data)
        else:
            print("No ACK received for size.")

def receive_command():
    # Wait for ML result: expects 'LEFT\n' or 'RIGHT\n'
    line = ser.readline().decode().strip().lower()
    if "left" in line:
        return "left"
    elif "right" in line:
        return "right"
    else:
        return None

def main():
    try:
        while True:
            print("Taking picture...")
            fname = take_picture()
            print("Sending image over serial...")
            send_image(fname)
            print("Waiting for ML direction...")
            direction = None
            while direction is None:
                direction = receive_command()
            print(f"ML says: {direction}, moving servo.")
            move_servo(direction)
            time.sleep(2)  # Wait before next cycle
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
