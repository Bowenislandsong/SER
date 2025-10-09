"""
Example: SVD Embedding Regression

This example demonstrates how to use the SVDEmbeddingRegression algorithm
for dimensionality reduction and regression on synthetic data.
"""

import numpy as np
from ser import SVDEmbeddingRegression

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
print("Generating synthetic data...")
n_samples = 200
n_features = 20
n_informative = 5

# Create a low-rank matrix with noise
U = np.random.randn(n_samples, n_informative)
V = np.random.randn(n_informative, n_features)
X = U @ V + 0.5 * np.random.randn(n_samples, n_features)

# Create target variable that depends on the first few components
true_weights = np.random.randn(n_informative)
y = U @ true_weights + 0.1 * np.random.randn(n_samples)

# Split into train and test sets
train_size = 150
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# Create and train the model
print("\nTraining SVD Embedding Regression model...")
model = SVDEmbeddingRegression(n_components=10)
model.fit(X_train, y_train)

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Evaluate the model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"\nResults:")
print(f"Training R² Score: {train_score:.4f}")
print(f"Test R² Score: {test_score:.4f}")

# Show the singular values
print(f"\nSingular values: {model.s_[:5]}")
print(f"Number of components used: {len(model.s_)}")

# Transform the data
X_train_transformed = model.transform(X_train)
print(f"\nOriginal feature space: {X_train.shape}")
print(f"Transformed feature space: {X_train_transformed.shape}")

# Demonstrate fit_transform
print("\nDemonstrating fit_transform...")
model2 = SVDEmbeddingRegression(n_components=5)
X_transformed = model2.fit_transform(X_train, y_train)
print(f"Transformed shape with 5 components: {X_transformed.shape}")

print("\n✓ Example completed successfully!")
