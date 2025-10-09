"""Tests for SVD Embedding Regression"""

import numpy as np
import pytest
from ser import SVDEmbeddingRegression


def test_ser_basic_fit():
    """Test basic fitting of SER model"""
    X = np.random.randn(50, 10)
    y = np.random.randn(50)
    
    model = SVDEmbeddingRegression(n_components=5)
    model.fit(X, y)
    
    assert model.U_ is not None
    assert model.s_ is not None
    assert model.Vt_ is not None
    assert model.weights_ is not None


def test_ser_predict():
    """Test prediction with SER model"""
    X = np.random.randn(50, 10)
    y = np.random.randn(50)
    
    model = SVDEmbeddingRegression(n_components=5)
    model.fit(X, y)
    
    y_pred = model.predict(X)
    
    assert y_pred.shape == y.shape


def test_ser_transform():
    """Test transformation with SER model"""
    X = np.random.randn(50, 10)
    y = np.random.randn(50)
    
    model = SVDEmbeddingRegression(n_components=5)
    model.fit(X, y)
    
    X_transformed = model.transform(X)
    
    assert X_transformed.shape == (50, 5)


def test_ser_score():
    """Test scoring with SER model"""
    # Create data with linear relationship
    X = np.random.randn(100, 5)
    true_weights = np.array([1.0, 2.0, -1.0, 0.5, -0.5])
    y = X @ true_weights + 0.1 * np.random.randn(100)
    
    model = SVDEmbeddingRegression(n_components=5)
    model.fit(X, y)
    
    score = model.score(X, y)
    
    # Score should be high for data with clear linear relationship
    assert score > 0.9


def test_ser_fit_transform():
    """Test fit_transform method"""
    X = np.random.randn(50, 10)
    y = np.random.randn(50)
    
    model = SVDEmbeddingRegression(n_components=5)
    X_transformed = model.fit_transform(X, y)
    
    assert X_transformed.shape == (50, 5)
    assert model.U_ is not None


def test_ser_n_components_none():
    """Test SER with n_components=None"""
    X = np.random.randn(50, 10)
    y = np.random.randn(50)
    
    model = SVDEmbeddingRegression(n_components=None)
    model.fit(X, y)
    
    # Should keep all components (min of dimensions)
    assert len(model.s_) == min(X.shape)
