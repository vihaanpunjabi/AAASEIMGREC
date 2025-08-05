import argparse
import os
import tensorflow as tf
from tensorflow.keras import layers, models

# Default hyper-parameters
IMG_SIZE = (128, 128)  # Resize all images to this size
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE

def load_datasets(data_dir: str, img_size: tuple = IMG_SIZE, batch_size: int = BATCH_SIZE, seed: int = 123):
    """Load training and validation datasets from *data_dir*.
    The directory is expected to have one sub-folder per class.
    Returns (train_ds, val_ds, class_names).
    """
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Dataset directory '{data_dir}' does not exist.")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.8,
        subset="training",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size,
    )

    # Optional: Cache and prefetch for performance
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, train_ds.class_names


def build_model(num_classes: int, img_size: tuple = IMG_SIZE) -> tf.keras.Model:
    """Build and compile a simple CNN model."""
    model = models.Sequential(
        [
            layers.Rescaling(1.0 / 255, input_shape=(img_size[0], img_size[1], 3)),
            layers.Conv2D(32, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(128, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train an image classification model using Keras.")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="dataset",
        help="Path to the dataset directory (one sub-folder per class).",
    )
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs.")
    parser.add_argument("--output", type=str, default="image_classifier_model", help="Directory to save the trained model.")
    args = parser.parse_args()

    # Load datasets
    train_ds, val_ds, class_names = load_datasets(args.data_dir)
    num_classes = len(class_names)

    # Build and train model
    model = build_model(num_classes)
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)

    # Persist model
    model.save(args.output)
    print(f"Model saved to '{args.output}'")


if __name__ == "__main__":
    main()
