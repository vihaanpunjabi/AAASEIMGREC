import os
import sys

# Set path to your dataset directory
data_dir = "dataset"
img_size = (128, 128)  # Resize all images to this size
batch_size = 32

# Check if dataset directory exists
if not os.path.exists(data_dir):
    print(f"Error: Dataset directory '{data_dir}' not found!")
    print("Please create a dataset directory with the following structure:")
    print("dataset/")
    print("├── class1/")
    print("│   ├── image1.jpg")
    print("│   ├── image2.jpg")
    print("│   └── ...")
    print("├── class2/")
    print("│   ├── image1.jpg")
    print("│   └── ...")
    print("└── ...")
    sys.exit(1)

# Check if dataset directory has subdirectories (classes)
subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
if not subdirs:
    print(f"Error: No class subdirectories found in '{data_dir}'!")
    print("Please add subdirectories for each class containing the respective images.")
    sys.exit(1)

print(f"Found {len(subdirs)} classes: {subdirs}")

# Check if each class directory has images
for class_name in subdirs:
    class_dir = os.path.join(data_dir, class_name)
    images = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    if not images:
        print(f"Warning: No images found in class directory '{class_name}'")
    else:
        print(f"Found {len(images)} images in class '{class_name}'")

print("\nSimulation complete! The script would now:")
print("1. Load and preprocess the images")
print("2. Train a CNN model")
print("3. Save the trained model")
print("\nTo run the actual training, install TensorFlow and run imagerec.py")