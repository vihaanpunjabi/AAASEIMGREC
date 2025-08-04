# Image Recognition Project

This project implements a simple CNN-based image classifier using TensorFlow/Keras.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare your dataset:
   - Create a `dataset` directory in the project root
   - Add subdirectories for each class you want to classify
   - Place images for each class in their respective subdirectories

Example structure:
```
dataset/
├── cats/
│   ├── cat1.jpg
│   ├── cat2.jpg
│   └── ...
├── dogs/
│   ├── dog1.jpg
│   ├── dog2.jpg
│   └── ...
└── birds/
    ├── bird1.jpg
    ├── bird2.jpg
    └── ...
```

## Usage

Run the training script:
```bash
python3 imagerec.py
```

The script will:
- Check if the dataset directory exists and has the correct structure
- Load and preprocess the images
- Train a CNN model for 10 epochs
- Save the trained model as `image_classifier_model`

## Features

- Automatic train/validation split (80%/20%)
- Image resizing to 128x128 pixels
- Data augmentation and caching for performance
- Dropout regularization to prevent overfitting
- Comprehensive error handling and user feedback

## Requirements

- Python 3.7+
- TensorFlow 2.10+
- NumPy
- Pillow

## Troubleshooting

If you encounter errors:
1. Make sure the `dataset` directory exists
2. Ensure each class has its own subdirectory with images
3. Check that images are in common formats (jpg, png, etc.)
4. Verify all dependencies are installed correctly