"""
SVD Embedding Regression (SER)

This module implements the SVD Embedding Regression algorithm, which combines
Singular Value Decomposition with regression for dimensionality reduction and
prediction.
"""

import numpy as np
from scipy.linalg import svd


class SVDEmbeddingRegression:
    """
    SVD Embedding Regression (SER) algorithm.
    
    This algorithm performs dimensionality reduction using SVD and then
    applies linear regression in the reduced space.
    
    Parameters
    ----------
    n_components : int, optional (default=None)
        Number of singular values to keep. If None, all components are kept.
    
    Attributes
    ----------
    U_ : ndarray
        Left singular vectors
    s_ : ndarray
        Singular values
    Vt_ : ndarray
        Right singular vectors (transposed)
    weights_ : ndarray
        Regression coefficients in the reduced space
    """
    
    def __init__(self, n_components=None):
        self.n_components = n_components
        self.U_ = None
        self.s_ = None
        self.Vt_ = None
        self.weights_ = None
        self.mean_X_ = None
        self.mean_y_ = None
    
    def fit(self, X, y):
        """
        Fit the SVD Embedding Regression model.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,) or (n_samples, n_targets)
            Target values
            
        Returns
        -------
        self : object
            Returns self
        """
        X = np.asarray(X)
        y = np.asarray(y)
        
        # Center the data
        self.mean_X_ = np.mean(X, axis=0)
        self.mean_y_ = np.mean(y, axis=0) if y.ndim > 1 else np.mean(y)
        
        X_centered = X - self.mean_X_
        y_centered = y - self.mean_y_
        
        # Perform SVD
        self.U_, self.s_, self.Vt_ = svd(X_centered, full_matrices=False)
        
        # Keep only n_components if specified
        if self.n_components is not None:
            self.U_ = self.U_[:, :self.n_components]
            self.s_ = self.s_[:self.n_components]
            self.Vt_ = self.Vt_[:self.n_components, :]
        
        # Project X onto the reduced space (principal components)
        # We use the projection onto the right singular vectors (Vt)
        X_reduced = self.U_ @ np.diag(self.s_) @ self.Vt_
        # Actually, for regression we want to work in the PC space directly
        # X_centered @ Vt.T gives us the principal component scores
        X_reduced = X_centered @ self.Vt_.T
        
        # Fit linear regression in the reduced space
        # weights = (X^T X)^-1 X^T y
        self.weights_ = np.linalg.lstsq(X_reduced, y_centered, rcond=None)[0]
        
        return self
    
    def transform(self, X):
        """
        Transform data to the reduced SVD space.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Data to transform
            
        Returns
        -------
        X_transformed : ndarray, shape (n_samples, n_components)
            Transformed data
        """
        X = np.asarray(X)
        X_centered = X - self.mean_X_
        
        # Project onto the right singular vectors and scale by singular values
        X_transformed = X_centered @ self.Vt_.T
        
        return X_transformed
    
    def predict(self, X):
        """
        Predict using the SVD Embedding Regression model.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Samples
            
        Returns
        -------
        y_pred : ndarray, shape (n_samples,) or (n_samples, n_targets)
            Predicted values
        """
        X = np.asarray(X)
        X_centered = X - self.mean_X_
        
        # Project onto the principal components (right singular vectors)
        X_reduced = X_centered @ self.Vt_.T
        
        # Apply regression weights
        y_pred = X_reduced @ self.weights_ + self.mean_y_
        
        return y_pred
    
    def fit_transform(self, X, y):
        """
        Fit the model and transform the data.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,) or (n_samples, n_targets)
            Target values
            
        Returns
        -------
        X_transformed : ndarray, shape (n_samples, n_components)
            Transformed training data
        """
        self.fit(X, y)
        return self.transform(X)
    
    def score(self, X, y):
        """
        Return the coefficient of determination R^2 of the prediction.
        
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Test samples
        y : array-like, shape (n_samples,) or (n_samples, n_targets)
            True values
            
        Returns
        -------
        score : float
            R^2 score
        """
        y = np.asarray(y)
        y_pred = self.predict(X)
        
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        return 1 - (ss_res / ss_tot)
