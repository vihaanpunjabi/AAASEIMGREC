import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import serial
import base64

MOTOR_PIN = 18  
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)


camera = PiCamera()
camera.resolution = (640, 480)

SERIAL_PORT = "/dev/ttyUSB0"  # Adjust as needed for your setup
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Warning: could not open serial port {SERIAL_PORT}: {e}")
    ser = None

def send_image_serial(filename):
    """Send an image file over the serial connection encoded in base64.

    The image is wrapped between IMG_START and IMG_END markers so that
    the receiver can detect boundaries. The content itself is base64
    text to stay ASCII-safe across typical serial monitors.
    """
    if ser is None or not ser.is_open:
        print("Serial port not available – skipping image transfer.")
        return

    try:
        with open(filename, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("ascii")
    except FileNotFoundError:
        print(f"Image {filename} not found – cannot send over serial.")
        return

    # Notify start of image
    ser.write(b"IMG_START\n")

    # Send data in manageable chunks to avoid overflowing buffers
    CHUNK_SIZE = 512  # characters (not bytes) per line
    for i in range(0, len(b64_data), CHUNK_SIZE):
        chunk = b64_data[i:i + CHUNK_SIZE]
        ser.write(chunk.encode("ascii") + b"\n")

    # Notify end of image
    ser.write(b"IMG_END\n")
    print(f"Sent {filename} over serial ({len(b64_data)} base64 chars)")


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
    send_image_serial("object_on_belt.jpg")

    time.sleep(2)
    motor_off()

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    GPIO.cleanup()
    print("GPIO cleanup complete.")

print("Working
")




      
