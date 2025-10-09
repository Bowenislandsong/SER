"""Tests for Federated SVD"""

import numpy as np
import pytest
from ser import FederatedSVD


def test_federated_svd_basic_fit():
    """Test basic fitting of Federated SVD"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    X3 = np.random.randn(25, 10)
    
    model = FederatedSVD(n_components=5)
    model.fit([X1, X2, X3])
    
    assert model.U_ is not None
    assert model.s_ is not None
    assert model.Vt_ is not None
    assert len(model.s_) == 5


def test_federated_svd_transform():
    """Test transformation with Federated SVD"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = FederatedSVD(n_components=5)
    model.fit([X1, X2])
    
    X_test = np.random.randn(10, 10)
    X_transformed = model.transform(X_test)
    
    assert X_transformed.shape == (10, 5)


def test_federated_svd_inverse_transform():
    """Test inverse transformation"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = FederatedSVD(n_components=5)
    model.fit([X1, X2])
    
    X_test = np.random.randn(10, 10)
    X_transformed = model.transform(X_test)
    X_reconstructed = model.inverse_transform(X_transformed)
    
    assert X_reconstructed.shape == X_test.shape


def test_federated_svd_explained_variance():
    """Test explained variance ratio"""
    X1 = np.random.randn(50, 10)
    X2 = np.random.randn(50, 10)
    
    model = FederatedSVD(n_components=5)
    model.fit([X1, X2])
    
    variance_ratio = model.explained_variance_ratio()
    
    assert len(variance_ratio) == 5
    assert np.all(variance_ratio >= 0)
    assert np.all(variance_ratio <= 1)


def test_federated_svd_privacy_info():
    """Test privacy budget information"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = FederatedSVD(n_components=5)
    model.fit([X1, X2])
    
    privacy_info = model.get_privacy_budget()
    
    assert isinstance(privacy_info, dict)
    assert 'raw_data_shared' in privacy_info
    assert privacy_info['raw_data_shared'] == False


def test_federated_svd_fit_transform():
    """Test fit_transform method"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = FederatedSVD(n_components=5)
    X_transformed = model.fit_transform([X1, X2])
    
    assert X_transformed.shape == (50, 5)


def test_federated_svd_iterations():
    """Test with different number of iterations"""
    X1 = np.random.randn(30, 10)
    X2 = np.random.randn(20, 10)
    
    model = FederatedSVD(n_components=5, n_iterations=20)
    model.fit([X1, X2])
    
    assert model.n_iterations == 20
    assert model.s_ is not None
