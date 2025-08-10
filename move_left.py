#!/usr/bin/env python3
"""
Move LEFT motor only (0 → 180 → 0)
For SAFE items - with auto port detection
"""

from utils.arduino_utils import get_arduino_connection
import time

# Get Arduino connection with auto port detection
ser = get_arduino_connection(baud_rate=9600)

if ser:
    # Move LEFT motor (0 → 180 → 0)
    print("Moving LEFT motor: 0° → 180° → 0°")
    ser.write(b'L180\n')
    ser.flush()
    
    # Arduino handles the return automatically
    time.sleep(2)  # Wait for movement to complete
    
    # Close connection
    ser.close()
    print("Done!")
else:
    print("Failed to connect to Arduino")