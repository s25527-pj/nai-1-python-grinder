import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Wczytaj dane z CSV
data = pd.read_csv('data/breast-cancer.csv')

# Usuwanie nieistotnych kolumn
X = data.drop(columns=['id', 'diagnosis'])

# Przekształcenie etykiet na liczby
y = data['diagnosis'].map({'M': 1, 'B': 0})

# Podział na zbiory treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standaryzacja danych wejściowych
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Budowa modelu
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Użycie sigmoid dla binarnej klasyfikacji
])

# Kompilacja modelu
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Trenowanie modelu
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Ewaluacja modelu
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss}, Accuracy: {accuracy}")
