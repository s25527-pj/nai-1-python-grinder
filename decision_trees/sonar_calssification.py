"""
Sonar Dataset Classification System
Authors: Maksymilian Mrówka, Maciej Uzarski

Environment Setup:
1. Navigate to the directory containing the script:
    - cd path/to/decision_trees

2. Install necessary dependencies:
    - pip install -r requirements.txt

3. Run the code:
    - Execute the script with `python sonar_classification.py`

Description:
- The script performs binary classification of sonar signals to determine whether an object is a mine (M) or a rock (R).
- Two machine learning algorithms are implemented for classification:
  1. CART (Classification and Regression Trees) using the DecisionTreeClassifier.
  2. SVM (Support Vector Machine) using the SVC classifier with an RBF kernel.
- Data preprocessing includes mapping the target variable (M/R) to binary values (1/0) and splitting the dataset into training and test sets.
- For SVM, data is standardized using StandardScaler to ensure proper scaling of features.
- Evaluation is based on accuracy scores for both classifiers on the test dataset.

"""

import pandas as pd

from sklearn.discriminant_analysis import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

df = pd.read_csv("sonar.csv")

# CART
decision_tree = DecisionTreeClassifier(
    max_depth=4, min_samples_split=5, random_state=42
)

x = df.iloc[:, :-1]
y = df.iloc[:, -1].map({"M": 1, "R": 0})

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=36
)

decision_tree.fit(X_train, y_train)

y_pred = decision_tree.predict(X_test)

print(
    "Dokładność CART:",
    round(accuracy_score(y_test, y_pred), 2),
)

# SVM
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm = SVC(kernel='rbf', C=10, gamma='auto', random_state=88)

svm.fit(X_train_scaled, y_train)

y_pred_svm = svm.predict(X_test_scaled)
print("Dokładność SVM:", round(accuracy_score(y_test, y_pred_svm), 2))