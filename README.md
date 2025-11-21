# SER - Machine Learning Algorithms Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/ser-algorithms.svg)](https://pypi.org/project/ser-algorithms/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library providing advanced machine learning algorithms including distributed and federated implementations, designed with a scikit-learn compatible API. This library focuses on privacy-preserving and scalable machine learning algorithms suitable for big data and federated learning scenarios.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Algorithms](#algorithms)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)
- [References](#references)
- [Roadmap](#roadmap)
- [Support](#support)

📖 **[Full Documentation](https://bowenislandsong.github.io/SER/)**

## Features

- **SVD Embedding Regression (SER)**: Combines Singular Value Decomposition with regression for dimensionality reduction and prediction
- **Distributed SVD**: Scalable SVD implementation for data distributed across multiple nodes
- **Federated SVD**: Privacy-preserving SVD that keeps data on local nodes while computing global decomposition

## Installation

### From PyPI (recommended)

```bash
pip install ser-algorithms
```

### From Conda

```bash
conda install -c conda-forge ser-algorithms
```

### Using Docker

```bash
# Pull the Docker image
docker pull ghcr.io/bowenislandsong/ser:latest

# Run Jupyter notebook
docker run -p 8888:8888 ghcr.io/bowenislandsong/ser:latest

# Or use it interactively
docker run -it ghcr.io/bowenislandsong/ser:latest python
```

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

The SVD Embedding Regression (SER) algorithm combines the power of Singular Value Decomposition (SVD) for dimensionality reduction with linear regression. This approach is particularly effective for high-dimensional data where features might be correlated, providing both interpretability and computational efficiency.

**Mathematical Foundation:**

The algorithm performs the following steps:
1. Compute SVD: X = UΣV^T
2. Project data to reduced space: X' = XVₖ (using k components)
3. Fit regression: y = X'w + b
4. Predict: ŷ = X'w + b

**Key Features:**
- Automatic dimensionality reduction through truncated SVD
- Handles multicollinearity in feature space
- Efficient computation through matrix factorization
- Works with both single and multi-target regression
- Regularization through component selection

**Use Cases:**
- High-dimensional regression problems (e.g., genomics, text analysis)
- Feature extraction and prediction pipelines
- Data with correlated or redundant features
- Dimensionality reduction with supervised learning

**References:** Based on SVD-based dimensionality reduction and regression techniques [1, 2].

### Distributed SVD

The Distributed SVD algorithm enables computation of SVD on large datasets that are partitioned across multiple nodes or machines. It uses a block-based approach where each partition computes local statistics, which are then combined to produce the global decomposition, enabling scalability to massive datasets.

**Mathematical Foundation:**

Given data distributed across N nodes: X = [X₁; X₂; ...; Xₙ]
1. Each node computes local SVD: Xᵢ = UᵢΣᵢVᵢᵀ
2. Combine local matrices: M = [Σ₁V₁ᵀ; Σ₂V₂ᵀ; ...; ΣₙVₙᵀ]
3. Compute global SVD: M = ŨΣ̃Ṽᵀ
4. Global components: Vglobal = Ṽᵀ

**Key Features:**
- Scalable to datasets larger than single machine memory
- Works with data distributed across multiple nodes
- Maintains numerical accuracy comparable to centralized SVD
- Efficient parallel computation with minimal communication
- Supports incremental updates

**Use Cases:**
- Big data analytics and processing
- Distributed computing environments (Spark, Dask)
- Data too large for single machine memory
- Parallel processing pipelines

**References:** Based on distributed matrix decomposition methods [2, 3].

### Federated SVD

The Federated SVD algorithm computes SVD while preserving data privacy. Raw data never leaves local nodes; instead, only aggregated statistics (covariance matrices and means) are shared to compute the global decomposition. This makes it suitable for privacy-sensitive applications where data governance is critical.

**Mathematical Foundation:**

For data on N nodes where Xᵢ remains local:
1. Each node computes local statistics: μᵢ = mean(Xᵢ), Cᵢ = XᵢᵀXᵢ
2. Aggregate statistics: μglobal = (1/N)Σμᵢ, Cglobal = ΣCᵢ
3. Compute SVD from covariance: Cglobal = VΣ²Vᵀ
4. Iterate to refine components through federated averaging

**Key Features:**
- Privacy-preserving computation (raw data stays local)
- Only shares aggregated statistics (means, covariances)
- Suitable for sensitive data (healthcare, finance)
- Compliant with data governance policies (GDPR, HIPAA)
- Supports differential privacy extensions

**Use Cases:**
- Healthcare data analysis across hospitals
- Financial data processing across institutions
- Multi-organization collaborations
- Privacy-sensitive applications
- Cross-silo federated learning scenarios

**References:** Based on federated averaging [4], federated machine learning [6], and privacy-preserving computation methods [5].

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

## Documentation

- **[Full Documentation](https://bowenislandsong.github.io/SER/)** - Complete API reference and guides
- **[Installation Guide](INSTALL.md)** - Detailed installation instructions for all methods
- **[Release Guide](RELEASE.md)** - Guide for maintainers on releasing new versions
- **[Changelog](CHANGELOG.md)** - History of changes and releases

## Contributing

Contributions are welcome! We appreciate bug reports, feature requests, documentation improvements, and code contributions.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/SER.git
cd SER

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=ser --cov-report=html
```

### Code Style

This project follows PEP 8 style guidelines. Please ensure your code is properly formatted before submitting.

### Reporting Issues

Please use the GitHub issue tracker to report bugs or request features. Include:
- A clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and dependency versions

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Citation

If you use this library in your research, please cite it as follows:

### BibTeX

```bibtex
@software{ser_algorithms_2024,
  title = {{SER}: Machine Learning Algorithms Library with Distributed and Federated Learning},
  author = {Bowenislandsong},
  year = {2024},
  version = {0.1.0},
  url = {https://github.com/Bowenislandsong/SER},
  note = {A Python library for distributed and federated machine learning algorithms}
}
```

### APA Style

Bowenislandsong. (2024). *SER: Machine Learning Algorithms Library* (Version 0.1.0) [Computer software]. https://github.com/Bowenislandsong/SER

### MLA Style

Bowenislandsong. *SER: Machine Learning Algorithms Library*. Version 0.1.0, 2024. GitHub, https://github.com/Bowenislandsong/SER.

## References

The algorithms implemented in this library are based on the following research:

### Singular Value Decomposition (SVD)

1. Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
   - The foundational text for SVD algorithms and matrix factorizations.

2. Halko, N., Martinsson, P. G., & Tropp, J. A. (2011). Finding structure with randomness: Probabilistic algorithms for constructing approximate matrix decompositions. *SIAM Review*, 53(2), 217-288.
   - Modern approaches to scalable SVD computation.

### Distributed Computing

3. Constantine, P. G., & Gleich, D. F. (2011). Tall and skinny QR factorizations in MapReduce architectures. *Proceedings of the Second International Workshop on MapReduce and its Applications*, 43-50.
   - Block-based distributed decomposition methods for large-scale matrices.

### Federated Learning

4. McMahan, B., Moore, E., Ramage, D., Hampson, S., & y Arcas, B. A. (2017). Communication-efficient learning of deep networks from decentralized data. *Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS)*, 1273-1282.
   - Foundational work on federated averaging and privacy-preserving computation.

5. Kairouz, P., McMahan, H. B., et al. (2021). Advances and open problems in federated learning. *Foundations and Trends in Machine Learning*, 14(1-2), 1-210.
   - Comprehensive survey of federated learning methods and privacy considerations.

6. Yang, Q., Liu, Y., Chen, T., & Tong, Y. (2019). Federated machine learning: Concept and applications. *ACM Transactions on Intelligent Systems and Technology*, 10(2), 1-19.
   - Overview of federated machine learning architectures.

## Roadmap

Future algorithms and features planned:

**Algorithms:**
- Distributed PCA (Principal Component Analysis)
- Federated Gradient Boosting with privacy guarantees
- Distributed K-Means clustering
- Privacy-preserving Neural Networks with secure aggregation
- Federated Random Forest
- Distributed LASSO and Ridge regression

**Features:**
- Differential privacy support
- Secure multi-party computation protocols
- Model compression for federated settings
- Advanced communication optimization
- GPU acceleration support
- Integration with popular distributed computing frameworks (Dask, Ray)

**Documentation:**
- Comprehensive tutorials and examples
- Theoretical background documentation
- Performance benchmarks
- Best practices guide

## Support

For questions, issues, or suggestions:
- 📧 Open an issue on [GitHub Issues](https://github.com/Bowenislandsong/SER/issues)
- 💬 Start a discussion in [GitHub Discussions](https://github.com/Bowenislandsong/SER/discussions)
- 📖 Check the [documentation](https://github.com/Bowenislandsong/SER/tree/main/examples) and examples

## Acknowledgments

This project builds upon fundamental research in distributed computing, federated learning, and matrix factorization. We acknowledge the contributions of the research community in developing these foundational algorithms.

---

**Note:** This is an active research and development project. APIs may change between versions. For production use, please pin to specific versions and thoroughly test the algorithms with your data.