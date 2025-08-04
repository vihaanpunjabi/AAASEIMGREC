#!/usr/bin/env python3
"""
Helper script to create a sample dataset structure for testing the image recognition project.
This script creates the directory structure and provides instructions for adding images.
"""

import os
import sys

def create_sample_dataset():
    """Create a sample dataset directory structure."""
    
    # Define sample classes
    classes = ['cats', 'dogs', 'birds']
    
    # Create dataset directory
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print(f"Created directory: {dataset_dir}")
    else:
        print(f"Directory already exists: {dataset_dir}")
    
    # Create class subdirectories
    for class_name in classes:
        class_dir = os.path.join(dataset_dir, class_name)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
            print(f"Created directory: {class_dir}")
        else:
            print(f"Directory already exists: {class_dir}")
    
    print("\n" + "="*50)
    print("Sample dataset structure created successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Add images to each class directory:")
    for class_name in classes:
        print(f"   - {dataset_dir}/{class_name}/ (add {class_name} images here)")
    print("\n2. Supported image formats: jpg, jpeg, png, bmp, gif")
    print("3. Run the training script: python3 imagerec.py")
    print("\nExample:")
    print("dataset/")
    print("├── cats/")
    print("│   ├── cat1.jpg")
    print("│   ├── cat2.jpg")
    print("│   └── ...")
    print("├── dogs/")
    print("│   ├── dog1.jpg")
    print("│   └── ...")
    print("└── birds/")
    print("    ├── bird1.jpg")
    print("    └── ...")

if __name__ == "__main__":
    create_sample_dataset()