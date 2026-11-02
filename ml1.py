
# ============================================================
# UBER FARE PREDICTION USING LINEAR REGRESSION AND RANDOM FOREST
# ============================================================

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error


# ============================================================
# 1. LOAD AND PREPROCESS THE DATASET
# ============================================================

df = pd.read_csv("archive (1)\\uber.csv")

# Remove unnecessary columns if present
df.drop(columns=["Unnamed: 0", "key"], errors="ignore", inplace=True)

# Convert pickup_datetime to datetime format
df["pickup_datetime"] = pd.to_datetime(
    df["pickup_datetime"], errors="coerce", utc=True
)

# Remove missing values and duplicate rows
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Remove invalid fare amounts and passenger counts
df = df[(df["fare_amount"] > 0) & (df["passenger_count"] > 0)]

# Select numerical features and target variable
features = [
    "pickup_longitude",
    "pickup_latitude",
    "dropoff_longitude",
    "dropoff_latitude",
    "passenger_count"
]

X = df[features]
y = df["fare_amount"]

print("Dataset shape after preprocessing:", df.shape)


# ============================================================
# 2. IDENTIFY AND REMOVE OUTLIERS USING IQR
# ============================================================

Q1 = y.quantile(0.25)
Q3 = y.quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = df[
    (df["fare_amount"] < lower_limit) |
    (df["fare_amount"] > upper_limit)
]

print("Number of outliers:", len(outliers))

# Visualize fare outliers
sns.boxplot(x=df["fare_amount"])
plt.title("Outliers in Uber Fare Amount")
plt.show()

# Remove outliers
df = df[
    df["fare_amount"].between(lower_limit, upper_limit)
].copy()

X = df[features]
y = df["fare_amount"]


# ============================================================
# 3. CHECK CORRELATION
# ============================================================

corr = df[features + ["fare_amount"]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

print("Correlation with fare amount:")
print(corr["fare_amount"].sort_values(ascending=False))


# ============================================================
# 4. SPLIT DATA AND TRAIN BOTH MODELS
# ============================================================

# Split dataset into training (80%) and testing (20%) data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# Random Forest Regression
rf = RandomForestRegressor(
    n_estimators=100, random_state=42, n_jobs=-1
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)


# ============================================================
# 5. EVALUATE AND COMPARE THE MODELS
# ============================================================

# Calculate R2 and RMSE for both models
lr_r2 = r2_score(y_test, y_pred_lr)
lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))

rf_r2 = r2_score(y_test, y_pred_rf)
rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))

# Display results
results = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "R2 Score": [lr_r2, rf_r2],
    "RMSE": [lr_rmse, rf_rmse]
})

print("\nModel Evaluation Results:")
print(results.to_string(index=False))

# Comparative diagram
results.set_index("Model").plot(
    kind="bar", figsize=(8, 5), rot=0
)

plt.title("Comparison of Regression Models")
plt.ylabel("Score")
plt.xlabel("Model")
plt.legend(["R2 Score", "RMSE"])
plt.tight_layout()
plt.show()
