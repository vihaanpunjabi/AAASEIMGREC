#!/usr/bin/env python3
"""
Camera utilities - auto camera detection and capture
"""

import cv2
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def find_available_camera():
    """
    Find first available camera
    
    Returns:
        int: Camera index if found, None otherwise
    """
    # Try common camera indices
    for i in range(5):  # Check first 5 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                logger.info(f"Found camera at index {i}")
                return i
    
    logger.error("No camera found")
    return None

def capture_photo(camera_index=None, save_dir="captured_photos"):
    """
    Capture a photo from camera with auto-detection
    
    Args:
        camera_index: Camera index (auto-detects if None)
        save_dir: Directory to save photos
        
    Returns:
        str: Path to saved photo or None if failed
    """
    # Auto-detect camera if not specified
    if camera_index is None:
        camera_index = find_available_camera()
        if camera_index is None:
            print("❌ No camera found!")
            return None
    
    # Create save directory if needed
    Path(save_dir).mkdir(exist_ok=True)
    
    # Open camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"❌ Failed to open camera {camera_index}")
        return None
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ Failed to capture frame")
        return None
    
    # Save photo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_path = f"{save_dir}/captured_{timestamp}.jpg"
    cv2.imwrite(photo_path, frame)
    
    print(f"✅ Photo saved: {photo_path}")
    return photo_path

def preview_camera(camera_index=None):
    """
    Preview camera feed
    
    Args:
        camera_index: Camera index (auto-detects if None)
    """
    # Auto-detect camera if not specified
    if camera_index is None:
        camera_index = find_available_camera()
        if camera_index is None:
            print("❌ No camera found!")
            return
    
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"Camera preview (index {camera_index})")
    print("Press 'q' to quit, SPACE to capture")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Camera Preview', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            photo_path = f"captured_photos/manual_{timestamp}.jpg"
            cv2.imwrite(photo_path, frame)
            print(f"✅ Captured: {photo_path}")
    
    cap.release()
    cv2.destroyAllWindows()