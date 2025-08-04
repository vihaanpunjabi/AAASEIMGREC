import tensorflow as tf
from tensorflow.keras import layers, models
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

try:
    # Load dataset (automatically splits 80% train, 20% val)
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=img_size,
        batch_size=batch_size
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=img_size,
        batch_size=batch_size
    )

    # Optional: Cache and prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Get class names
    class_names = train_ds.class_names
    num_classes = len(class_names)
    
    print(f"Training with {num_classes} classes: {class_names}")

    # Build a simple CNN model
    model = models.Sequential([
        layers.Rescaling(1./255, input_shape=(img_size[0], img_size[1], 3)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),  # Add dropout to prevent overfitting
        layers.Dense(num_classes, activation='softmax')
    ])

    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Print model summary
    model.summary()

    # Train model
    print("Starting training...")
    history = model.fit(
        train_ds, 
        validation_data=val_ds, 
        epochs=10,
        verbose=1
    )

    # Save model
    model.save("image_classifier_model")
    print("Model saved successfully as 'image_classifier_model'")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please check your dataset structure and try again.")
    sys.exit(1)
