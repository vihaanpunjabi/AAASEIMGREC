#!/usr/bin/env python3
"""
Arduino Servo Controller for Sorting System
Simple L/R + degrees command format with auto port detection
"""

import serial
import time
import logging
from typing import Optional
from .arduino_utils import find_arduino_port

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArduinoController:
    """Simple Arduino servo controller with auto port detection"""
    
    def __init__(self, port: str = None, baud_rate: int = 9600):
        """
        Initialize Arduino controller
        
        Args:
            port: Serial port (auto-detects if None)
            baud_rate: Communication speed (9600 for this Arduino)
        """
        # Auto-detect port if not provided
        if port is None:
            port = find_arduino_port()
            if port is None:
                logger.error("No Arduino detected. Please connect Arduino.")
        
        self.port = port
        self.baud_rate = baud_rate
        self.connection = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to Arduino with auto port detection
        
        Returns:
            True if connection successful, False otherwise
        """
        # Re-detect port if connection failed previously
        if self.port is None:
            self.port = find_arduino_port()
            if self.port is None:
                logger.error("Arduino not found. Please connect and try again.")
                return False
        
        try:
            self.connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            
            # Test connection by sending home command
            self.send_command("H90")  # Home position
            
            self.connected = True
            logger.info(f"Arduino connected on {self.port}")
            return True
                    
        except serial.SerialException as e:
            logger.error(f"Failed to connect to Arduino: {e}")
            return False
    
    def send_command(self, command: str) -> bool:
        """
        Send command to Arduino
        
        Args:
            command: Command string (e.g., "L180", "R90")
            
        Returns:
            True if command sent successfully
        """
        if not self.connected or not self.connection:
            logger.error("Arduino not connected")
            return False
        
        try:
            command_bytes = (command + '\n').encode('utf-8')
            self.connection.write(command_bytes)
            self.connection.flush()
            logger.info(f"Sent to Arduino: {command}")
            return True
                
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            self.connected = False
            return False
    
    def move_servo(self, direction: str, degrees: int = None) -> bool:
        """
        Move servo to specified direction and degrees
        
        Args:
            direction: "left", "right", or "center"
            degrees: 0-180 (optional, defaults based on direction)
            
        Returns:
            True if movement successful
        """
        direction = direction.lower()
        
        # Default positions for sorting
        if degrees is None:
            if direction == "left":
                degrees = 180  # Full left for safe items
            elif direction == "right":
                degrees = 180  # Full right for unsafe items
            elif direction == "center":
                degrees = 90   # Center position
            else:
                logger.error(f"Invalid direction: {direction}")
                return False
        
        # Clamp degrees to valid range
        degrees = max(0, min(180, degrees))
        
        # Create command
        if direction == "left":
            command = f"L{degrees}"
        elif direction == "right":
            command = f"R{degrees}"
        elif direction == "center":
            command = "L90"  # Either L90 or R90 centers both motors
        else:
            logger.error(f"Invalid direction: {direction}")
            return False
        
        success = self.send_command(command)
        if success:
            logger.info(f"Moved {direction} to {degrees} degrees")
        return success
    
    def sort_safe(self) -> bool:
        """Sort item to safe bin (left motor: 0→180→0)"""
        logger.info("Sorting to SAFE bin")
        success = self.move_servo("left", 180)
        if success:
            time.sleep(2)  # Wait for movement to complete (Arduino auto-returns)
        return success
    
    def sort_unsafe(self) -> bool:
        """Sort item to unsafe bin (right motor: 180→0→180)"""
        logger.info("Sorting to UNSAFE bin")
        success = self.move_servo("right", 180)
        if success:
            time.sleep(2)  # Wait for movement to complete (Arduino auto-returns)
        return success
    
    def test_servo(self) -> bool:
        """
        Test servo movement sequence
        
        Returns:
            True if test successful
        """
        logger.info("Testing servos...")
        
        test_sequence = [
            ("center", 90, 1),
            ("left", 180, 2),
            ("center", 90, 1),
            ("right", 180, 2),
            ("center", 90, 1),
        ]
        
        for direction, degrees, delay in test_sequence:
            if not self.move_servo(direction, degrees):
                return False
            time.sleep(delay)
        
        logger.info("Test complete")
        return True
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.connection:
            try:
                self.move_servo("center")  # Center before disconnecting
                self.connection.close()
                self.connected = False
                logger.info("Arduino disconnected")
            except:
                pass


def main():
    """Test the servo controller"""
    arduino = ArduinoController()
    
    if not arduino.connect():
        print("Failed to connect!")
        return
    
    print("Connected! Testing servos...")
    
    # Test sorting movements
    print("\nSorting SAFE item...")
    arduino.sort_safe()
    time.sleep(2)
    
    print("\nSorting UNSAFE item...")
    arduino.sort_unsafe()
    time.sleep(2)
    
    print("\nTest complete!")
    arduino.disconnect()


if __name__ == "__main__":
    main()