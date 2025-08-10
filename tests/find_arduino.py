#!/usr/bin/env python3
"""
Find Arduino port automatically
"""

import serial.tools.list_ports
import time

def find_arduino():
    """Find Arduino port automatically"""
    print("Searching for Arduino...")
    print("-" * 40)
    
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("❌ No serial ports found!")
        return None
    
    print("All available ports:")
    for p in ports:
        print(f"  {p.device}: {p.description}")
    
    print("\nLooking for Arduino...")
    
    # Common Arduino identifiers
    arduino_ids = ['usbmodem', 'usbserial', 'Arduino', 'CH340', 'CP210', 'FTDI']
    
    for port in ports:
        port_lower = port.device.lower()
        desc_lower = port.description.lower()
        
        for id in arduino_ids:
            if id.lower() in port_lower or id.lower() in desc_lower:
                print(f"✅ Found possible Arduino at: {port.device}")
                return port.device
    
    print("❌ No Arduino found. Please:")
    print("1. Connect your Arduino via USB")
    print("2. Close Arduino IDE Serial Monitor if open")
    print("3. Check that you're using a data USB cable (not charge-only)")
    print("4. Try unplugging and reconnecting the Arduino")
    
    return None

if __name__ == "__main__":
    port = find_arduino()
    
    if port:
        print(f"\n✅ Arduino found at: {port}")
        print(f"\nUpdate your scripts with:")
        print(f"PORT = '{port}'")
    else:
        print("\n⚠️ Please connect your Arduino and run this script again")