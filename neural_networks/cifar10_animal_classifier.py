"""
Image Classification with Convolutional Neural Networks (CNN)
Author: Maksymilian Mrówka, Maciej Uzarski

Environment Setup:
1. Navigate to the directory containing the script:
    - cd path/to/neural_networks
2. Install required dependencies:
    - pip install -r requirements.txt
2. Run the script:
    - Execute the script with `python cifar10_animal_classifier.py`

Description:
- This script implements a Convolutional Neural Network (CNN) to classify images from the CIFAR-10 dataset into 10 categories.
- The CIFAR-10 dataset consists of 60,000 32x32 color images in 10 classes, with 50,000 training images and 10,000 testing images.
- The images are normalized by scaling pixel values to the range [0, 1] to improve training stability.
- The CNN architecture includes:
  1. Convolutional layer: 32 filters of size 3x3 with ReLU activation.
  2. MaxPooling layer: Down-samples feature maps using 2x2 pooling.
  3. Flatten layer: Converts 2D feature maps into 1D vectors for the fully connected layers.
  4. Fully connected layer: 128 neurons with ReLU activation.
  5. Output layer: 10 neurons with softmax activation for multi-class classification.
- The model is compiled with the Adam optimizer and sparse categorical cross-entropy loss function, using accuracy as the evaluation metric.
- Training is conducted over 10 epochs with validation on the test dataset.
- The script evaluates the model's performance on the test dataset, displaying accuracy and loss metrics.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Pobranie danych
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalizacja danych
x_train, x_test = x_train / 255.0, x_test / 255.0

# Budowa modelu
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# Kompilacja i trenowanie
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

# Ewaluacja
model.evaluate(x_test, y_test)