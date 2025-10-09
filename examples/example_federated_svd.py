"""
Example: Federated SVD

This example demonstrates how to use the FederatedSVD algorithm
for privacy-preserving SVD where data stays on local nodes.
"""

import numpy as np
from ser import FederatedSVD

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic federated data
print("Generating federated data across 3 organizations...")
print("(Data will stay on local nodes, only statistics are shared)\n")

n_features = 12
n_components_true = 4

# Create a shared low-rank structure
V_true = np.random.randn(n_components_true, n_features)

# Simulate data on different organizations
org_names = ["Hospital A", "Hospital B", "Hospital C"]
org_sizes = [150, 100, 120]
X_orgs = []

for name, size in zip(org_names, org_sizes):
    U_org = np.random.randn(size, n_components_true)
    X_org = U_org @ V_true + 0.4 * np.random.randn(size, n_features)
    X_orgs.append(X_org)
    print(f"{name}: {size} samples, {n_features} features")

# Create and fit the federated SVD model
print("\n" + "="*50)
print("Training Federated SVD model...")
print("="*50)
model = FederatedSVD(n_components=8, n_iterations=10)
model.fit(X_orgs)

# Display privacy information
print("\nPrivacy Information:")
privacy_info = model.get_privacy_budget()
for key, value in privacy_info.items():
    print(f"  {key}: {value}")

# Display results
print(f"\nModel Results:")
print(f"Computed {len(model.s_)} singular values")
print(f"Top 5 singular values: {model.s_[:5]}")

# Get explained variance ratio
variance_ratio = model.explained_variance_ratio()
print(f"\nExplained variance ratio:")
for i, ratio in enumerate(variance_ratio[:5]):
    print(f"  Component {i+1}: {ratio:.4f} ({ratio*100:.2f}%)")

cumulative_variance = np.cumsum(variance_ratio)
print(f"\nCumulative variance:")
for i in [2, 4, 7]:
    print(f"  First {i+1} components: {cumulative_variance[i]:.4f} ({cumulative_variance[i]*100:.2f}%)")

# Transform new data (e.g., from a new patient)
print("\n" + "="*50)
print("Transforming new data...")
print("="*50)
X_new = np.random.randn(10, n_features)
X_new_transformed = model.transform(X_new)
print(f"New data shape: {X_new.shape}")
print(f"Transformed shape: {X_new_transformed.shape}")

# Inverse transform to reconstruct
X_reconstructed = model.inverse_transform(X_new_transformed)
print(f"Reconstructed shape: {X_reconstructed.shape}")

# Calculate reconstruction error
reconstruction_error = np.mean((X_new - X_reconstructed) ** 2)
print(f"Reconstruction MSE: {reconstruction_error:.6f}")

# Compare with centralized approach (for demonstration)
print("\n" + "="*50)
print("Comparison with centralized data:")
print("="*50)
print("In centralized approach:")
print("  - All raw data would be shared to central server")
print("  - Privacy concerns for sensitive data")
print("\nIn federated approach:")
print("  - Only aggregated statistics (mean, covariance) shared")
print("  - Raw data never leaves local organizations")
print("  - Suitable for healthcare, finance, etc.")

# Demonstrate fit_transform
print("\n" + "="*50)
print("Demonstrating fit_transform...")
print("="*50)
model2 = FederatedSVD(n_components=5)
X_all_transformed = model2.fit_transform(X_orgs)
print(f"All federated data transformed shape: {X_all_transformed.shape}")

print("\n✓ Example completed successfully!")
print("\nNote: In a real federated setting, raw data would never")
print("be concatenated or shared between organizations.")
