"""
Banknote Classification Using Neural Networks
Author: Maksymilian Mrówka, Maciej Uzarski

Environment Setup:
1. Navigate to the directory containing the script:
    - cd path/to/neural_networks
2. Install required dependencies:
    - pip install -r requirements.txt
3. Run the script:
    - Execute the script with `python banknote_classifier.py`

Description:
- This script implements a neural network model to classify banknotes as authentic or forged.
- It uses a dataset in CSV format, where the last column represents the binary labels (0 → authentic, 1 → forged), and the preceding columns represent the features.
- The input data is split into training and test sets, and features are standardized using `StandardScaler` for improved model convergence.
- The neural network architecture consists of:
  1. Input layer: Fully connected layer with 32 neurons and ReLU activation.
  2. Hidden layer: Fully connected layer with 16 neurons and ReLU activation.
  3. Output layer: Single neuron with sigmoid activation for binary classification.
- The model is compiled using the Adam optimizer and binary cross-entropy loss function, with accuracy as the evaluation metric.
- Training is conducted over 10 epochs, with validation on the test dataset.
- The script outputs the model's loss and accuracy on the test dataset, as well as example predictions.

"""

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#
data = np.loadtxt("data/banknote.csv", delimiter=",")
X = data[:, :-1]
y = data[:, -1]  

# Podział na dane testowe i treningowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standaryzacja danych
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Tworzenie modelu
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Użycie sigmoid dla binarnej klasyfikacji
])

# Kompilacja modelu
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Trenowanie modelu
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Ewaluacja modelu
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Dokładność testu: {test_accuracy}")

# Predykcje
y_pred = (model.predict(X_test) > 0.5).astype(int)
print(f"Przykładowe predykcje: {y_pred[:5]}")
