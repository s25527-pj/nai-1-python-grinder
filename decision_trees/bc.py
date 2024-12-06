import pandas as pd
import matplotlib.pyplot as plt

from sklearn.discriminant_analysis import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import plot_tree
from sklearn.svm import SVC

df = pd.read_csv("breast-cancer.csv")
# Remove first column (ID)
df = df.drop(df.columns[0], axis=1).reset_index(drop=True)

# CART
decision_tree = DecisionTreeClassifier(
    max_depth=4, min_samples_split=10, random_state=42
)
x = df.iloc[:, 1:].reset_index(drop=True)
y = df.iloc[:, 0].map({"M": 1, "B": 0})
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

decision_tree.fit(X_train, y_train)

y_pred = decision_tree.predict(X_test)

plt.figure(figsize=(20, 10))
plot_tree(
    decision_tree,
    feature_names=x.columns,
    class_names=["Benign", "Malignant"],
    filled=True,
)
plt.show()

print(
    "Dokładność CART:",
    round(accuracy_score(y_test, y_pred), 2),
)

# SVM
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)

svm.fit(X_train_scaled, y_train)

y_pred_svm = svm.predict(X_test_scaled)
print("Dokładność SVM:", accuracy_score(y_test, y_pred_svm))

custom_record = [[15.34, 18.10, 92.45, 876.5, 0.1023, 0.1256, 0.1384, 0.0749, 0.1793, 0.0625,
                  0.5432, 0.7350, 2.567, 62.45, 0.00456, 0.03245, 0.04056, 0.01034, 0.02045, 0.00412,
                  22.87, 24.53, 145.3, 1345, 0.1456, 0.3567, 0.4523, 0.1987, 0.3564, 0.0948]]
custom_record_scaled = scaler.transform(custom_record)
y_pred_custom = svm.predict(custom_record_scaled)
print("Przewidywana klasa:", "Malignant" if y_pred_custom[0] == 1 else "Benign")
