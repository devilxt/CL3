import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report
from scipy.spatial.distance import cdist

print("Generating synthetic structural damage data...")
X, y = make_classification(n_samples=1000, n_features=15, n_informative=8, 
                           n_classes=3, random_state=42)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step B: Compress data using PCA (Dimensionality Reduction)
pca = PCA(n_components=8) # Compress from 15 down to 8 crucial features
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print("Initializing Memory Cells using K-Means...")

memory_cells = []
memory_labels = []

# Number of antibodies (memory cells) to generate per damage class
n_antibodies_per_class = 5

# Step C: Initialize memory cell set using k-means
for class_label in np.unique(y_train):
    # Isolate antigens belonging to the current damage class
    antigens_class = X_train_pca[y_train == class_label]
    
    # Use K-Means to find representative clusters (these become our antibodies)
    kmeans = KMeans(n_clusters=n_antibodies_per_class, random_state=42, n_init=10)
    kmeans.fit(antigens_class)
    
    memory_cells.extend(kmeans.cluster_centers_)
    memory_labels.extend([class_label] * n_antibodies_per_class)

memory_cells = np.array(memory_cells)
memory_labels = np.array(memory_labels)

print("Testing the Artificial Immune System...")
distances = cdist(X_test_pca, memory_cells, metric='euclidean')

closest_memory_cell_indices = np.argmin(distances, axis=1)

y_pred = memory_labels[closest_memory_cell_indices]

print("\n--- AIPR Classification Results ---")
print(f"Overall Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print(classification_report(y_test, y_pred, 
                            target_names=["No Damage", "Minor Damage", "Severe Damage"]))