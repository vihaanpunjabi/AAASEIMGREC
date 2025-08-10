#!/usr/bin/env python3

import cv2
import numpy as np
import time
from datetime import datetime
from pathlib import Path
from analyzer import SimpleEWasteAnalyzer


class AutoDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Detection parameters
        self.motion_threshold = 30  # Pixel difference threshold
        self.area_threshold = 5000  # Minimum area of changed pixels
        self.stability_frames = 10  # Frames to wait for stability
        self.cooldown_frames = 30  # Frames to wait after detection
        
        # State tracking
        self.prev_frame = None
        self.stable_count = 0
        self.cooldown_count = 0
        self.object_detected = False
        
    def run(self):
        print("="*60)
        print("AUTO OBJECT DETECTION - E-WASTE ANALYZER")
        print("="*60)
        print("\nPlace object in front of camera for auto-analysis")
        print("Press 'q' to quit\n")
        
        analyzer = SimpleEWasteAnalyzer()
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Initialize prev_frame on first iteration
            if self.prev_frame is None:
                self.prev_frame = gray
                continue
            
            # Calculate frame difference
            frame_diff = cv2.absdiff(self.prev_frame, gray)
            thresh = cv2.threshold(frame_diff, self.motion_threshold, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            # Find contours (areas of change)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calculate total area of changed pixels
            total_area = sum(cv2.contourArea(c) for c in contours)
            
            # Create display frame
            display = frame.copy()
            
            # Draw contours and status
            motion_detected = False
            if total_area > self.area_threshold:
                motion_detected = True
                # Draw bounding boxes around detected areas
                for contour in contours:
                    if cv2.contourArea(contour) > 1000:
                        (x, y, w, h) = cv2.boundingRect(contour)
                        cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Status text
            status = "WAITING"
            color = (255, 255, 255)
            
            # Cooldown after detection
            if self.cooldown_count > 0:
                self.cooldown_count -= 1
                status = f"COOLDOWN: {self.cooldown_count}"
                color = (0, 255, 255)
            
            # Check for stable object
            elif motion_detected:
                self.stable_count = 0
                status = "MOTION DETECTED"
                color = (0, 255, 0)
            else:
                if total_area < 500:  # Very little change
                    self.stable_count += 1
                    if self.stable_count > self.stability_frames and not self.object_detected:
                        status = "STABLE - NO OBJECT"
                        color = (128, 128, 128)
                else:
                    # Object present but stable
                    self.stable_count += 1
                    if self.stable_count > self.stability_frames:
                        if not self.object_detected:
                            # CAPTURE AND ANALYZE!
                            status = "ANALYZING..."
                            color = (0, 0, 255)
                            
                            # Save photo
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            photo_path = f"captured_photos/auto_{timestamp}.jpg"
                            cv2.imwrite(photo_path, frame)
                            
                            # Analyze
                            print(f"\n{'='*40}")
                            print(f"Object detected! Analyzing...")
                            result = analyzer.analyze_one_image(Path(photo_path), 1, 1)
                            
                            # Display results
                            print(f"\nRESULT:")
                            print(f"  Item: {result['item_name']}")
                            print(f"  Safety: {result['safety_level']}")
                            if result['hazards']:
                                print(f"  Hazards: {', '.join(result['hazards'])}")
                            print(f"{'='*40}\n")
                            
                            self.object_detected = True
                            self.cooldown_count = self.cooldown_frames
                        else:
                            status = "OBJECT PRESENT"
                            color = (255, 0, 0)
                    else:
                        status = f"STABILIZING... {self.stable_count}/{self.stability_frames}"
                        color = (255, 255, 0)
            
            # Reset object detection when area is very small
            if total_area < 500 and self.cooldown_count == 0:
                self.object_detected = False
            
            # Add status text to display
            cv2.putText(display, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(display, f"Changed Area: {int(total_area)}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show motion threshold view in corner
            thresh_small = cv2.resize(thresh, (160, 120))
            thresh_color = cv2.cvtColor(thresh_small, cv2.COLOR_GRAY2BGR)
            display[10:130, display.shape[1]-170:display.shape[1]-10] = thresh_color
            
            # Display the frame
            cv2.imshow('Auto Object Detection', display)
            
            # Update prev_frame
            self.prev_frame = gray
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import os
    if not os.path.exists("captured_photos"):
        os.makedirs("captured_photos")
    
    detector = AutoDetector()
    detector.run()