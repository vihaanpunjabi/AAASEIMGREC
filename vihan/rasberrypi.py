import RPi.GPIO as GPIO
import time
from picamera import PiCamera

MOTOR_PIN = 18  
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)


camera = PiCamera()
camera.resolution = (640, 480)

def motor_on():
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    print("Motor ON")

def motor_off():
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    print("Motor OFF")

def capture_image(filename="image.jpg"):
    camera.start_preview()
    time.sleep(2)  
    camera.capture(filename)
    camera.stop_preview()
    print(f"Captured {filename}")


try:
    print("Starting system...")
    motor_on()
    time.sleep(5)  

    capture_image("object_on_belt.jpg")

    time.sleep(2)
    motor_off()

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    GPIO.cleanup()
    print("GPIO cleanup complete.")

print("Working
")




      
