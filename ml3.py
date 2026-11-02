
# ============================================================
# BANK CUSTOMER CHURN PREDICTION USING ANN
# ============================================================

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


# ============================================================
# 1. READ AND PREPROCESS THE DATASET
# ============================================================

df = pd.read_csv("archive (3)\\Churn_Modelling.csv")

# Remove unnecessary columns
df.drop(columns=["RowNumber", "CustomerId", "Surname"], inplace=True)

# Handle missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Convert categorical columns into numerical columns
df = pd.get_dummies(df, columns=["Geography", "Gender"], drop_first=True, dtype=int)

# Separate features and target
X = df.drop("Exited", axis=1)
y = df["Exited"]


# ============================================================
# 2. SPLIT DATA INTO TRAINING AND TESTING SETS
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# ============================================================
# 3. NORMALIZE THE DATA
# ============================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ============================================================
# 4. BUILD AND IMPROVE THE NEURAL NETWORK
# ============================================================

# Initial ANN model
model = Sequential([
    Dense(16, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(8, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Train the model
model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Improvement: dropout to reduce overfitting and early stopping
model = Sequential([
    Dense(32, activation="relu", input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(16, activation="relu"),
    Dropout(0.2),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(
    monitor="val_loss", patience=5, restore_best_weights=True
)

model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=0
)


# ============================================================
# 5. ACCURACY AND CONFUSION MATRIX
# ============================================================

y_prob = model.predict(X_test, verbose=0)
y_pred = (y_prob >= 0.5).astype(int).ravel()

accuracy = accuracy_score(y_test, y_pred)

print("ANN Accuracy:", round(accuracy * 100, 2), "%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Display confusion matrix
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred,
    display_labels=["Not Exited", "Exited"],
    cmap="Blues"
)

plt.title("Customer Churn Confusion Matrix")
plt.show()
