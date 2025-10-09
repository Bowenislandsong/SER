"""
Example: Distributed SVD

This example demonstrates how to use the DistributedSVD algorithm
to perform SVD on data distributed across multiple nodes.
"""

import numpy as np
from ser import DistributedSVD

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic distributed data
print("Generating distributed data across 4 nodes...")
n_features = 15
n_components_true = 5

# Create a low-rank structure
V_true = np.random.randn(n_components_true, n_features)

# Simulate data on different nodes
node_sizes = [100, 80, 120, 90]
X_nodes = []

for i, size in enumerate(node_sizes):
    U_node = np.random.randn(size, n_components_true)
    X_node = U_node @ V_true + 0.3 * np.random.randn(size, n_features)
    X_nodes.append(X_node)
    print(f"Node {i+1}: {X_node.shape}")

# Create and fit the distributed SVD model
print("\nFitting Distributed SVD model...")
model = DistributedSVD(n_components=10)
model.fit(X_nodes)

print(f"Computed {len(model.s_)} singular values")
print(f"Top 5 singular values: {model.s_[:5]}")

# Get explained variance ratio
variance_ratio = model.explained_variance_ratio()
print(f"\nExplained variance ratio for top 5 components:")
for i, ratio in enumerate(variance_ratio[:5]):
    print(f"  Component {i+1}: {ratio:.4f} ({ratio*100:.2f}%)")

cumulative_variance = np.cumsum(variance_ratio)
print(f"\nCumulative variance explained:")
print(f"  First 5 components: {cumulative_variance[4]:.4f} ({cumulative_variance[4]*100:.2f}%)")
print(f"  All components: {cumulative_variance[-1]:.4f} ({cumulative_variance[-1]*100:.2f}%)")

# Transform some test data
print("\nTransforming new data...")
X_test = np.random.randn(50, n_features)
X_transformed = model.transform(X_test)
print(f"Original shape: {X_test.shape}")
print(f"Transformed shape: {X_transformed.shape}")

# Inverse transform
X_reconstructed = model.inverse_transform(X_transformed)
print(f"Reconstructed shape: {X_reconstructed.shape}")

# Calculate reconstruction error
reconstruction_error = np.mean((X_test - X_reconstructed) ** 2)
print(f"\nReconstruction MSE: {reconstruction_error:.6f}")

# Demonstrate fit_transform
print("\nDemonstrating fit_transform...")
model2 = DistributedSVD(n_components=5)
X_all_transformed = model2.fit_transform(X_nodes)
print(f"All data transformed shape: {X_all_transformed.shape}")

print("\n✓ Example completed successfully!")
