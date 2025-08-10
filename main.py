#!/usr/bin/env python3

import sys
from pathlib import Path
from phone_coms import take_photo_from_front_camera
from analyzer import SimpleEWasteAnalyzer


def main():
    print("\n" + "="*50)
    print("E-WASTE ANALYZER")
    print("="*50)
    
    # Take photo
    print("\nCapturing photo...")
    photo_path = take_photo_from_front_camera()
    
    if not photo_path:
        print("Failed to capture photo")
        return
    
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
    
    print("="*50)
    
    # Continue?
    if input("\nAnalyze another? (y/n): ").lower() == 'y':
        main()


if __name__ == "__main__":
    main()