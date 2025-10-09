# SER - Machine Learning Algorithms Library

A Python library providing advanced machine learning algorithms including distributed and federated implementations, similar to scikit-learn.

## Features

- **SVD Embedding Regression (SER)**: Combines Singular Value Decomposition with regression for dimensionality reduction and prediction
- **Distributed SVD**: Scalable SVD implementation for data distributed across multiple nodes
- **Federated SVD**: Privacy-preserving SVD that keeps data on local nodes while computing global decomposition

## Installation

### From source

```bash
git clone https://github.com/Bowenislandsong/SER.git
cd SER
pip install -e .
```

### Dependencies

- Python >= 3.8
- NumPy >= 1.20.0
- SciPy >= 1.7.0

## Quick Start

### SVD Embedding Regression

```python
import numpy as np
from ser import SVDEmbeddingRegression

# Generate sample data
X = np.random.randn(100, 10)
y = np.random.randn(100)

# Create and fit model
model = SVDEmbeddingRegression(n_components=5)
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Get R^2 score
score = model.score(X, y)
print(f"R^2 Score: {score:.3f}")
```

### Distributed SVD

```python
import numpy as np
from ser import DistributedSVD

# Simulate distributed data across 3 nodes
X_node1 = np.random.randn(50, 10)
X_node2 = np.random.randn(50, 10)
X_node3 = np.random.randn(50, 10)

# Create and fit model
model = DistributedSVD(n_components=5)
model.fit([X_node1, X_node2, X_node3])

# Transform new data
X_test = np.random.randn(20, 10)
X_transformed = model.transform(X_test)

# Get explained variance ratio
variance_ratio = model.explained_variance_ratio()
print(f"Explained variance: {variance_ratio}")
```

### Federated SVD

```python
import numpy as np
from ser import FederatedSVD

# Simulate data on different nodes (data stays local)
X_node1 = np.random.randn(50, 10)
X_node2 = np.random.randn(50, 10)
X_node3 = np.random.randn(50, 10)

# Create and fit model (only statistics are shared)
model = FederatedSVD(n_components=5, n_iterations=10)
model.fit([X_node1, X_node2, X_node3])

# Transform data
X_test = np.random.randn(20, 10)
X_transformed = model.transform(X_test)

# Check privacy information
privacy_info = model.get_privacy_budget()
print(f"Privacy level: {privacy_info['privacy_level']}")
```

## Algorithms

### SVD Embedding Regression

The SVD Embedding Regression (SER) algorithm combines the power of Singular Value Decomposition (SVD) for dimensionality reduction with linear regression. It's particularly useful when dealing with high-dimensional data where features might be correlated.

**Key Features:**
- Automatic dimensionality reduction
- Handles multicollinearity
- Efficient computation through SVD
- Works with both single and multi-target regression

**Use Cases:**
- High-dimensional regression problems
- Feature extraction and prediction
- Data with correlated features

### Distributed SVD

The Distributed SVD algorithm enables computation of SVD on large datasets that are split across multiple nodes or partitions. It uses a block-based approach where each partition computes local SVD, and results are combined to produce the global decomposition.

**Key Features:**
- Scalable to large datasets
- Works with data distributed across nodes
- Maintains numerical accuracy
- Efficient parallel computation

**Use Cases:**
- Big data analytics
- Distributed computing environments
- Data too large for single machine memory

### Federated SVD

The Federated SVD algorithm computes SVD while preserving data privacy. Raw data never leaves local nodes; instead, only aggregated statistics (means and covariances) are shared to compute the global decomposition.

**Key Features:**
- Privacy-preserving computation
- No raw data sharing
- Suitable for sensitive data
- Compliant with data governance policies

**Use Cases:**
- Healthcare data analysis
- Financial data processing
- Multi-organization collaborations
- Privacy-sensitive applications

## API Reference

All classes follow the scikit-learn API conventions with `fit()`, `transform()`, `fit_transform()`, and `predict()` methods where applicable.

### SVDEmbeddingRegression

```python
SVDEmbeddingRegression(n_components=None)
```

**Methods:**
- `fit(X, y)`: Fit the model to training data
- `transform(X)`: Transform data to reduced space
- `predict(X)`: Make predictions
- `fit_transform(X, y)`: Fit and transform in one step
- `score(X, y)`: Compute R^2 score

### DistributedSVD

```python
DistributedSVD(n_components=None)
```

**Methods:**
- `fit(X_partitions)`: Fit on distributed data (list of arrays)
- `transform(X)`: Transform data to reduced space
- `fit_transform(X_partitions)`: Fit and transform
- `inverse_transform(X_transformed)`: Transform back to original space
- `explained_variance_ratio()`: Get variance explained by components

### FederatedSVD

```python
FederatedSVD(n_components=None, n_iterations=10)
```

**Methods:**
- `fit(X_nodes)`: Fit on federated data (list of arrays)
- `transform(X)`: Transform data to reduced space
- `fit_transform(X_nodes)`: Fit and transform
- `inverse_transform(X_transformed)`: Transform back to original space
- `explained_variance_ratio()`: Get variance explained by components
- `get_privacy_budget()`: Get privacy information

## Examples

See the `examples/` directory for more detailed usage examples and tutorials.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Citation

If you use this library in your research, please cite:

```bibtex
@software{ser_algorithms,
  title = {SER: Machine Learning Algorithms Library},
  author = {Bowenislandsong},
  year = {2024},
  url = {https://github.com/Bowenislandsong/SER}
}
```

## Roadmap

Future algorithms planned:
- Distributed PCA
- Federated Gradient Boosting
- Distributed K-Means
- Privacy-preserving Neural Networks
- Federated Random Forest

## Support

For questions, issues, or suggestions, please open an issue on GitHub.