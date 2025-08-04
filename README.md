# Image Recognition Project

A TensorFlow-based image classification system with comprehensive error handling and easy setup.

## Features

- **Robust CNN Architecture**: Multi-layer convolutional neural network with dropout for regularization
- **Comprehensive Error Handling**: Detailed error messages and graceful failure handling
- **Automatic Dataset Validation**: Checks for proper dataset structure and valid image files
- **Easy Demo Setup**: Includes script to create sample dataset for testing
- **Modern TensorFlow Integration**: Uses latest Keras 3 format and best practices

## Quick Start

### 1. Set up the environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create demo dataset (optional)

```bash
python setup_demo.py
```

This creates a sample dataset with 3 classes (cats, dogs, birds) for testing.

### 3. Run the image classifier

```bash
python imagerec.py
```

## Dataset Structure

Your dataset should be organized as follows:

```
dataset/
├── class1/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── class2/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
└── class3/
    ├── image1.jpg
    ├── image2.png
    └── ...
```

## Requirements

- Python 3.8+
- TensorFlow 2.20.0rc0
- NumPy
- Pillow (PIL)

## Bugs Fixed

### 1. **Missing Dependencies**
- **Problem**: `ModuleNotFoundError: No module named 'tensorflow'`
- **Solution**: Created `requirements.txt` with proper dependency versions and virtual environment setup

### 2. **Missing Dataset Validation**
- **Problem**: Script would crash if dataset directory didn't exist
- **Solution**: Added comprehensive checks for:
  - Dataset directory existence
  - Minimum number of class subdirectories (≥2)
  - Valid image files in dataset

### 3. **Poor Error Handling**
- **Problem**: Cryptic error messages and immediate crashes
- **Solution**: Added try-catch blocks around:
  - Dataset loading
  - Model training
  - Model saving
  - All with informative error messages

### 4. **Deprecated Model Saving Format**
- **Problem**: `save_format` argument deprecated in Keras 3
- **Solution**: Updated to use `.keras` extension without deprecated parameters

### 5. **Missing Input Validation**
- **Problem**: No validation of dataset contents or structure
- **Solution**: Added validation for:
  - Minimum number of classes
  - Class names extraction and verification
  - Dataset splits validation

### 6. **No Overfitting Prevention**
- **Problem**: Simple model without regularization
- **Solution**: Added dropout layers (0.5 rate) after Conv2D and Dense layers

### 7. **Poor User Experience**
- **Problem**: No progress feedback or final results summary
- **Solution**: Added:
  - Progress messages throughout execution
  - Model architecture summary
  - Training progress display
  - Final accuracy reporting
  - Clear success/failure messages

### 8. **No Persistence of Class Information**
- **Problem**: Class names not saved with model
- **Solution**: Save class names to `class_names.txt` for future inference

## Model Architecture

```
Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ rescaling (Rescaling)           │ (None, 128, 128, 3)    │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d (Conv2D)                 │ (None, 126, 126, 32)   │           896 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d (MaxPooling2D)    │ (None, 63, 63, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_1 (Conv2D)               │ (None, 61, 61, 64)     │        18,496 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_1 (MaxPooling2D)  │ (None, 30, 30, 64)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_2 (Conv2D)               │ (None, 28, 28, 128)    │        73,856 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_2 (MaxPooling2D)  │ (None, 14, 14, 128)    │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout (Dropout)               │ (None, 14, 14, 128)    │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 25088)          │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 128)            │     3,211,392 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_1 (Dropout)             │ (None, 128)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 3)              │           387 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
```

## Output Files

After successful training, the script creates:
- `image_classifier_model.keras`: Trained model in Keras format
- `class_names.txt`: List of class names for inference

## Troubleshooting

### Virtual Environment Issues
If you encounter virtual environment issues:
```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

### Memory Issues
For large datasets or limited memory:
- Reduce `batch_size` in `imagerec.py`
- Reduce `img_size` from (128, 128) to (64, 64)

### Training Too Slow
- Reduce number of `epochs` from 10 to 5
- Use smaller `img_size`
- Reduce dataset size

## Contributing

When adding new features or fixing bugs:
1. Test with the demo dataset first
2. Ensure proper error handling
3. Add appropriate progress messages
4. Update this README if needed

## License

This project is open source and available under the MIT License.