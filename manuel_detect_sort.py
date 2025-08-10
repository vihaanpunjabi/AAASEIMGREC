#!/usr/bin/env python3

import sys
import time
from pathlib import Path
from utils.phone_coms import take_photo_from_front_camera
from utils.analyzer import SimpleEWasteAnalyzer
from utils.sorter import ArduinoController


def main():
    print("\n" + "="*50)
    print("E-WASTE ANALYZER WITH SORTING")
    print("="*50)
    
    # Initialize Arduino with auto port detection
    print("\nConnecting to Arduino (auto-detecting port)...")
    arduino = ArduinoController()  # Auto-detects port
    
    if not arduino.connect():
        print("WARNING: Arduino not connected. Continuing without sorting...")
        arduino = None
    else:
        print("Arduino connected successfully!")
    
    # Main loop
    while True:
        # Take photo
        print("\nCapturing photo...")
        photo_path = take_photo_from_front_camera()
        
        if not photo_path:
            print("Failed to capture photo")
            continue
        
        # Analyze
        print("Analyzing...")
        analyzer = SimpleEWasteAnalyzer()
        result = analyzer.analyze_one_image(Path(photo_path), 1, 1)
        
        # Display results
        print("\n" + "="*50)
        print(f"Item: {result['item_name']}")
        print(f"Safety: {result['safety_level']}")
        
        if result['hazards']:
            print(f"Hazards: {', '.join(result['hazards'])}")
        
        if result['notes']:
            print(f"Notes: {result['notes']}")
        
        # Perform sorting based on safety level
        if arduino and arduino.connected:
            print("\n--- SORTING DECISION ---")
            safety_level = result['safety_level']
            
            if safety_level == "Safe to Shred":
                # SAFE: Sort to left bin
                print("✅ SAFE TO SHRED - Sorting to LEFT bin")
                arduino.sort_safe()
                print("Item sorted to SAFE bin")
                
            else:
                # NOT SAFE: Sort to right bin
                # This includes: "Requires Preprocessing", "Do Not Shred", "Discard", or unknown
                print(f"⚠️ NOT SAFE TO SHRED ({safety_level}) - Sorting to RIGHT bin")
                arduino.sort_unsafe()
                print("Item sorted to SPECIAL HANDLING bin")
        
        print("="*50)
        
        # Continue?
        if input("\nAnalyze another? (y/n): ").lower() != 'y':
            break
    
    # Cleanup
    if arduino:
        print("\nDisconnecting Arduino...")
        arduino.disconnect()


if __name__ == "__main__":
    main()