
# K-Means Clustering on Sales Data

# 1. Import libraries
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 2. Load dataset
df = pd.read_csv("archive (4)\\sales_data_sample.csv", encoding="latin1")

# 3. Select numerical features and preprocess
X = df[["SALES", "QUANTITYORDERED", "PRICEEACH"]].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Elbow Method to find the number of clusters
inertia = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 11), inertia, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.show()

# 5. Apply K-Means with the selected number of clusters
# Choose K by observing the elbow in the graph
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# 6. Display cluster results
X = X.copy()
X["Cluster"] = clusters

print("Cluster assignments:")
print(X.head())

print("\nNumber of records in each cluster:")
print(X["Cluster"].value_counts())

# 7. Visualize clusters
plt.scatter(X["SALES"], X["QUANTITYORDERED"], c=X["Cluster"])
plt.title("Sales Data Clusters")
plt.xlabel("Sales")
plt.ylabel("Quantity Ordered")
plt.show()
