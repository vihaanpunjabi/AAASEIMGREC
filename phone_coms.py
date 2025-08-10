#!/usr/bin/env python3

import cv2
import os
from datetime import datetime


def take_photo_from_front_camera(save_path=None):
    """
    Takes a single photo from the front camera and saves it.
    
    Args:
        save_path: Optional custom path to save the photo. 
                   If None, saves to captured_photos/ with timestamp.
    
    Returns:
        str: Path to the saved photo if successful, None if failed.
    """
    # Create photos directory if it doesn't exist
    photos_dir = "captured_photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    
    # Open front camera (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access front camera. Check camera permissions.")
        return None
    
    # Set camera properties for better quality
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    # Take photo
    ret, frame = cap.read()
    
    # Release camera immediately
    cap.release()
    
    if not ret or frame is None:
        print("Error: Failed to capture photo")
        return None
    
    # Generate filename if not provided
    if save_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        save_path = os.path.join(photos_dir, filename)
    
    # Save the photo
    cv2.imwrite(save_path, frame)
    print(f"Photo saved: {save_path}")
    
    return save_path


if __name__ == "__main__":
    # Example usage
    photo_path = take_photo_from_front_camera()
    if photo_path:
        print(f"Successfully captured photo at: {photo_path}")
    else:
        print("Failed to capture photo")