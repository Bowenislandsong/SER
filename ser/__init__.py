"""
SER - A machine learning library with distributed and federated algorithms.

This library provides implementations of various machine learning algorithms
including:
- SVD Embedding Regression (SER)
- Distributed SVD
- Federated SVD
"""

__version__ = "0.1.0"

from .svd_embedding_regression import SVDEmbeddingRegression
from .distributed_svd import DistributedSVD
from .federated_svd import FederatedSVD

__all__ = [
    "SVDEmbeddingRegression",
    "DistributedSVD",
    "FederatedSVD",
]
