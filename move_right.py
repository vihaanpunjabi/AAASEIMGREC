#!/usr/bin/env python3
"""
Move RIGHT motor only (180 → 0 → 180)
For UNSAFE items - with auto port detection
"""

from utils.arduino_utils import get_arduino_connection
import time

# Get Arduino connection with auto port detection
ser = get_arduino_connection(baud_rate=9600)

if ser:
    # Move RIGHT motor (180 → 0 → 180)
    print("Moving RIGHT motor: 180° → 0° → 180°")
    ser.write(b'R180\n')
    ser.flush()
    
    # Arduino handles the return automatically
    time.sleep(2)  # Wait for movement to complete
    
    # Close connection
    ser.close()
    print("Done!")
else:
    print("Failed to connect to Arduino")