"""
Comparison of Neural Network Architectures for Fashion MNIST Classification
Author: Maksymilian Mrówka, Maciej Uzarski

Environment Setup:
1. Navigate to the directory containing the script:
    - cd path/to/neural_networks
2. Ensure necessary dependencies are installed:
    - pip install -r requirements.txt
3. Run the script:
    - Execute the script with `python fashion_mnist_classifier.py`

Description:
- This script compares the performance of two neural network architectures (small and large) on the Fashion MNIST dataset.
- The Fashion MNIST dataset contains 70,000 grayscale images of size 28x28 across 10 fashion categories. The dataset is divided into 60,000 training images and 10,000 test images.
- Key features of the script:
  1. **Small Neural Network**:
     - Input layer: Flattens the 28x28 image into a 1D array.
     - Dense layer: 64 neurons with ReLU activation.
     - Output layer: 10 neurons with softmax activation for classification.
  2. **Large Neural Network**:
     - Input layer: Flattens the 28x28 image into a 1D array.
     - Dense layers: 256 and 128 neurons with ReLU activation.
     - Output layer: 10 neurons with softmax activation.
- Both networks are trained using the Adam optimizer, sparse categorical cross-entropy loss, and accuracy as a metric over 5 epochs with validation on the test dataset.
- Results:
  - Loss and accuracy are computed and compared for both networks on the test dataset.
- A confusion matrix is generated for the larger network, visualizing the model's performance across all categories.
- The confusion matrix is displayed using a `viridis` colormap for better interpretability.
"""


import matplotlib
matplotlib.use('TkAgg')
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Pobranie danych
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

# Normalizacja danych
x_train, x_test = x_train / 255.0, x_test / 255.0

# Budowa mniejszej sieci
small_model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

# Kompilacja i trenowanie mniejszej sieci
small_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
small_model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Ewaluacja mniejszej sieci
small_loss, small_accuracy = small_model.evaluate(x_test, y_test)
print(f"Mniejsza sieć - Loss: {small_loss}, Accuracy: {small_accuracy}")

# Budowa większej sieci
large_model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(256, activation='relu'),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# Kompilacja i trenowanie większej sieci
large_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
large_model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Ewaluacja większej sieci
large_loss, large_accuracy = large_model.evaluate(x_test, y_test)
print(f"Większa sieć - Loss: {large_loss}, Accuracy: {large_accuracy}")

# Porównanie wyników
print("Porównanie wyników:")
print(f"Mniejsza sieć - Loss: {small_loss}, Accuracy: {small_accuracy}")
print(f"Większa sieć - Loss: {large_loss}, Accuracy: {large_accuracy}")

# Confusion Matrix dla większej sieci
y_pred_large = large_model.predict(x_test).argmax(axis=1)
cm = confusion_matrix(y_test, y_pred_large)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[str(i) for i in range(10)])
disp.plot(cmap='viridis')

plt.gcf().canvas.draw()  # Aktualizacja canvy
plt.show()
