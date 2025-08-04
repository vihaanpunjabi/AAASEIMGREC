#!/usr/bin/env python3
"""
Demo Setup Script for Image Recognition
========================================

This script creates a sample dataset structure with placeholder images
to test the image recognition functionality.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_image(width=128, height=128, color=(255, 255, 255), text="Sample"):
    """Create a simple sample image with text."""
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a basic font, fallback to default if not available
    try:
        # Try to find a system font
        import platform
        if platform.system() == "Linux":
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, 20)
                    break
            if font is None:
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text with contrasting color
    text_color = (0, 0, 0) if sum(color) > 384 else (255, 255, 255)
    draw.text((x, y), text, font=font, fill=text_color)
    
    return img

def setup_demo_dataset():
    """Set up a demo dataset with sample images."""
    dataset_dir = "dataset"
    
    # Remove existing dataset if it exists
    if os.path.exists(dataset_dir):
        print(f"Removing existing '{dataset_dir}' directory...")
        import shutil
        shutil.rmtree(dataset_dir)
    
    # Create dataset structure
    classes = {
        "cats": [(255, 200, 200), (255, 150, 150), (255, 100, 100)],  # Red tones
        "dogs": [(200, 255, 200), (150, 255, 150), (100, 255, 100)],  # Green tones
        "birds": [(200, 200, 255), (150, 150, 255), (100, 100, 255)]  # Blue tones
    }
    
    print(f"Creating demo dataset in '{dataset_dir}/'...")
    
    for class_name, colors in classes.items():
        class_dir = os.path.join(dataset_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        
        print(f"  Creating {class_name} images...")
        
        # Create 20 sample images per class
        for i in range(20):
            # Random color from the class palette
            color = random.choice(colors)
            
            # Add some randomness to the color
            color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in color)
            
            # Create image with class name and index
            img = create_sample_image(
                width=128, 
                height=128, 
                color=color, 
                text=f"{class_name}\n#{i+1}"
            )
            
            # Save image
            img_path = os.path.join(class_dir, f"{class_name}_{i+1:02d}.png")
            img.save(img_path)
    
    print(f"\nDemo dataset created successfully!")
    print(f"Dataset structure:")
    for class_name in classes.keys():
        class_dir = os.path.join(dataset_dir, class_name)
        num_images = len([f for f in os.listdir(class_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
        print(f"  {class_name}/: {num_images} images")
    
    print(f"\nYou can now run: python imagerec.py")

def main():
    """Main function."""
    print("Image Recognition Demo Setup")
    print("=" * 40)
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Error: PIL (Pillow) is required but not installed.")
        print("Please install it with: pip install pillow")
        return False
    
    setup_demo_dataset()
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)