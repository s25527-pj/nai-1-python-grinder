import pandas as pd

from sklearn.discriminant_analysis import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

df = pd.read_csv("sonar.csv")

# CART
decision_tree = DecisionTreeClassifier(
    max_depth=4, min_samples_split=10, random_state=42
)

x = df.iloc[:, :-1]
y = df.iloc[:, -1].map({"M": 1, "R": 0})

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
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
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)

svm.fit(X_train_scaled, y_train)

y_pred_svm = svm.predict(X_test_scaled)
print("Dokładność SVM:", accuracy_score(y_test, y_pred_svm))