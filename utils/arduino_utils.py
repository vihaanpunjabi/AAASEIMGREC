#!/usr/bin/env python3
"""
Arduino utilities - auto port detection
"""

import serial.tools.list_ports
import serial
import time
import logging

logger = logging.getLogger(__name__)

def find_arduino_port():
    """
    Automatically find Arduino port
    
    Returns:
        str: Port path if found, None otherwise
    """
    ports = list(serial.tools.list_ports.comports())
    
    # Common Arduino identifiers
    arduino_keywords = ['usbmodem', 'usbserial', 'Arduino', 'CH340', 'CP210', 'FTDI', 'USB']
    
    for port in ports:
        port_str = f"{port.device} {port.description}".lower()
        
        for keyword in arduino_keywords:
            if keyword.lower() in port_str:
                # Test if it's actually an Arduino by trying to connect
                try:
                    test_conn = serial.Serial(port.device, 9600, timeout=1)
                    test_conn.close()
                    logger.info(f"Found Arduino at {port.device}")
                    return port.device
                except:
                    continue
    
    logger.error("No Arduino found")
    return None

def get_arduino_connection(baud_rate=9600):
    """
    Get Arduino serial connection with auto port detection
    
    Args:
        baud_rate: Serial communication speed
        
    Returns:
        serial.Serial object or None
    """
    port = find_arduino_port()
    
    if not port:
        print("❌ Arduino not found! Please:")
        print("1. Connect Arduino via USB")
        print("2. Close Arduino IDE Serial Monitor")
        print("3. Check USB cable supports data")
        return None
    
    try:
        conn = serial.Serial(port, baud_rate, timeout=1)
        print(f"✅ Connected to Arduino on {port}")
        time.sleep(2)  # Arduino initialization
        return conn
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None