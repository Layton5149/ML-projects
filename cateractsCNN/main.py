import tensorflow as tf
from keras import layers, models

# -----------------------
# 1. Basic config
# -----------------------
IMG_SIZE = (224, 224)   # you can change, but keep it consistent
BATCH_SIZE = 32
EPOCHS = 15

train_dir = "dataset/train"
test_dir = "dataset/test"

# -----------------------
# 2. Load datasets
# -----------------------
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    labels='inferred',
    label_mode='binary',          # cataract vs normal -> binary
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=True,
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    labels='inferred',
    label_mode='binary',
    color_mode='rgb',
    batch_size=BATCH_SIZE,
    image_size=IMG_SIZE,
    shuffle=False,
)

# (optional but recommended) – make datasets fast
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

# -----------------------
# 3. Build the CNN
# -----------------------
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=IMG_SIZE + (3,)),  # normalize pixels

    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')   # 1 unit + sigmoid for binary
])

model.summary()

# -----------------------
# 4. Compile the model
# -----------------------
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# -----------------------
# 5. Train
# -----------------------
history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=EPOCHS
)

# -----------------------
# 6. Evaluate on test data
# -----------------------
test_loss, test_acc = model.evaluate(test_ds)
print(f"\nTest accuracy: {test_acc:.4f}")

# -----------------------
# 7. (Optional) Save the model
# -----------------------
model.save("cataract_cnn.h5")
print("Model saved to cataract_cnn.h5")
