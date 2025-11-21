"""Tests for Distributed SVD"""

import numpy as np
import pytest
from ser import DistributedSVD


def test_distributed_svd_basic_fit():
    """Test basic fitting of Distributed SVD"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    X3 = np.random.randn(25, 10)
    
    model = DistributedSVD(n_components=5)
    model.fit([X1, X2, X3])
    
    assert model.U_ is not None
    assert model.s_ is not None
    assert model.Vt_ is not None
    assert len(model.s_) == 5


def test_distributed_svd_transform():
    """Test transformation with Distributed SVD"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = DistributedSVD(n_components=5)
    model.fit([X1, X2])
    
    X_test = np.random.randn(10, 10)
    X_transformed = model.transform(X_test)
    
    assert X_transformed.shape == (10, 5)


def test_distributed_svd_inverse_transform():
    """Test inverse transformation"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = DistributedSVD(n_components=5)
    model.fit([X1, X2])
    
    X_test = np.random.randn(10, 10)
    X_transformed = model.transform(X_test)
    X_reconstructed = model.inverse_transform(X_transformed)
    
    assert X_reconstructed.shape == X_test.shape


def test_distributed_svd_explained_variance():
    """Test explained variance ratio"""
    X1 = np.random.randn(50, 10)
    X2 = np.random.randn(50, 10)
    
    model = DistributedSVD(n_components=5)
    model.fit([X1, X2])
    
    variance_ratio = model.explained_variance_ratio()
    
    assert len(variance_ratio) == 5
    assert np.all(variance_ratio >= 0)
    assert np.all(variance_ratio <= 1)
    # Variance ratios should be in descending order
    assert np.all(np.diff(variance_ratio) <= 0)


def test_distributed_svd_single_partition():
    """Test with single partition (edge case)"""
    X = np.random.randn(50, 10)
    
    model = DistributedSVD(n_components=5)
    model.fit([X])
    
    assert model.s_ is not None
    assert len(model.s_) == 5


def test_distributed_svd_fit_transform():
    """Test fit_transform method"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = DistributedSVD(n_components=5)
    X_transformed = model.fit_transform([X1, X2])
    
    assert X_transformed.shape == (50, 5)
