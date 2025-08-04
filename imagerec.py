import tensorflow as tf
from tensorflow.keras import layers, models
import os
import sys

def main():
    # Set path to your dataset directory
    data_dir = "dataset"
    img_size = (128, 128)  # Resize all images to this size
    batch_size = 32

    # Check if dataset directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Dataset directory '{data_dir}' not found!")
        print(f"Please create the directory and organize your images in subdirectories.")
        print(f"Example structure:")
        print(f"  {data_dir}/")
        print(f"    ├── class1/")
        print(f"    │   ├── image1.jpg")
        print(f"    │   └── image2.jpg")
        print(f"    └── class2/")
        print(f"        ├── image3.jpg")
        print(f"        └── image4.jpg")
        return False

    # Check if dataset directory has subdirectories (classes)
    subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    if len(subdirs) < 2:
        print(f"Error: Dataset directory must contain at least 2 class subdirectories.")
        print(f"Found {len(subdirs)} subdirectories: {subdirs}")
        return False

    try:
        # Load dataset (automatically splits 80% train, 20% val)
        print("Loading training dataset...")
        train_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=img_size,
            batch_size=batch_size
        )

        print("Loading validation dataset...")
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=img_size,
            batch_size=batch_size
        )

    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Please check that your dataset directory contains valid image files.")
        return False

    # Get class names and validate
    class_names = train_ds.class_names
    num_classes = len(class_names)
    
    if num_classes < 2:
        print(f"Error: Need at least 2 classes for classification. Found {num_classes}: {class_names}")
        return False
    
    print(f"Found {num_classes} classes: {class_names}")

    # Optional: Cache and prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Build a simple CNN model
    print("Building CNN model...")
    model = models.Sequential([
        layers.Rescaling(1./255, input_shape=(img_size[0], img_size[1], 3)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.5),  # Add dropout to prevent overfitting
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
    print("\nModel Architecture:")
    model.summary()

    try:
        # Train model
        print(f"\nStarting training for 10 epochs...")
        history = model.fit(
            train_ds, 
            validation_data=val_ds, 
            epochs=10,
            verbose=1
        )

        # Print final training results
        final_train_acc = history.history['accuracy'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        print(f"\nTraining completed!")
        print(f"Final Training Accuracy: {final_train_acc:.4f}")
        print(f"Final Validation Accuracy: {final_val_acc:.4f}")

    except Exception as e:
        print(f"Error during training: {e}")
        return False

    try:
        # Save model
        model_path = "image_classifier_model.keras"
        print(f"\nSaving model to '{model_path}'...")
        model.save(model_path)  # Keras 3 format
        print("Model saved successfully!")

        # Save class names for future use
        class_names_path = "class_names.txt"
        with open(class_names_path, 'w') as f:
            for class_name in class_names:
                f.write(f"{class_name}\n")
        print(f"Class names saved to '{class_names_path}'")

    except Exception as e:
        print(f"Error saving model: {e}")
        return False

    print("\nScript completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
