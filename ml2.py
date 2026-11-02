
# ============================================================
# EMAIL SPAM DETECTION USING KNN AND SVM
# ============================================================

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. LOAD AND PREPROCESS DATASET
# ============================================================

df = pd.read_csv("archive (2)\\emails.csv")

# Remove unnecessary columns and duplicate rows
df.drop(columns=["Email No."], errors="ignore", inplace=True)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Separate features and target
# Change "Prediction" if your dataset uses another target column name
X = df.drop("Prediction", axis=1)
y = df["Prediction"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features for KNN and SVM
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ============================================================
# 2. K-NEAREST NEIGHBORS (KNN) CLASSIFICATION
# ============================================================

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)

knn_accuracy = accuracy_score(y_test, y_pred_knn)

print("KNN Accuracy:", round(knn_accuracy * 100, 2), "%")
print("\nKNN Classification Report:")
print(classification_report(y_test, y_pred_knn))


# ============================================================
# 3. SUPPORT VECTOR MACHINE (SVM) CLASSIFICATION
# ============================================================

svm = SVC(kernel="linear")
svm.fit(X_train, y_train)

y_pred_svm = svm.predict(X_test)

svm_accuracy = accuracy_score(y_test, y_pred_svm)

print("SVM Accuracy:", round(svm_accuracy * 100, 2), "%")
print("\nSVM Classification Report:")
print(classification_report(y_test, y_pred_svm))


# ============================================================
# 4. COMPARE MODEL ACCURACY
# ============================================================

models = ["KNN", "SVM"]
accuracies = [knn_accuracy * 100, svm_accuracy * 100]

print("\nModel Comparison:")
print("KNN Accuracy:", round(accuracies[0], 2), "%")
print("SVM Accuracy:", round(accuracies[1], 2), "%")

plt.bar(models, accuracies)
plt.title("KNN vs SVM Accuracy")
plt.xlabel("Classification Model")
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.show()
