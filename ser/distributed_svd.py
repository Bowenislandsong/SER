"""
Distributed SVD

This module implements a distributed version of Singular Value Decomposition
that can work with data split across multiple nodes or partitions.
"""

import numpy as np
from scipy.linalg import svd


class DistributedSVD:
    """
    Distributed Singular Value Decomposition.
    
    This algorithm computes SVD on data that is distributed across multiple
    partitions. It uses a block-based approach where each partition computes
    local SVD and then combines results.
    
    Parameters
    ----------
    n_components : int, optional (default=None)
        Number of singular values/vectors to compute. If None, computes all.
    
    Attributes
    ----------
    U_ : ndarray
        Left singular vectors of shape (n_samples, n_components)
    s_ : ndarray
        Singular values in descending order
    Vt_ : ndarray
        Right singular vectors (transposed) of shape (n_components, n_features)
    """
    
    def __init__(self, n_components=None):
        self.n_components = n_components
        self.U_ = None
        self.s_ = None
        self.Vt_ = None
        self.mean_ = None
    
    def fit(self, X_partitions):
        """
        Fit the Distributed SVD model.
        
        Parameters
        ----------
        X_partitions : list of array-like
            List of data partitions, each of shape (n_samples_i, n_features).
            Each partition represents data on a different node.
            
        Returns
        -------
        self : object
            Returns self
        """
        # Convert all partitions to arrays
        X_partitions = [np.asarray(X) for X in X_partitions]
        
        # Compute global mean
        total_samples = sum(X.shape[0] for X in X_partitions)
        self.mean_ = sum(np.sum(X, axis=0) for X in X_partitions) / total_samples
        
        # Center each partition
        X_centered = [X - self.mean_ for X in X_partitions]
        
        # Step 1: Compute local SVDs on each partition
        local_svds = []
        for X in X_centered:
            if X.shape[0] > 0:  # Check partition is not empty
                U_local, s_local, Vt_local = svd(X, full_matrices=False)
                local_svds.append((U_local, s_local, Vt_local))
        
        # Step 2: Combine the right singular vectors (Vt)
        # Weight by singular values and concatenate
        weighted_Vt = []
        for U_local, s_local, Vt_local in local_svds:
            # Weight Vt by singular values
            weighted_Vt.append(np.diag(s_local) @ Vt_local)
        
        # Stack all weighted Vt matrices
        combined_Vt = np.vstack(weighted_Vt)
        
        # Step 3: Compute SVD of the combined matrix to get global Vt
        U_global, s_global, Vt_global = svd(combined_Vt, full_matrices=False)
        
        # Step 4: Keep only n_components if specified
        if self.n_components is not None:
            s_global = s_global[:self.n_components]
            Vt_global = Vt_global[:self.n_components, :]
            U_global = U_global[:, :self.n_components]
        
        self.s_ = s_global
        self.Vt_ = Vt_global
        
        # Step 5: Compute global U by projecting original data
        # Concatenate all partitions
        X_full = np.vstack(X_centered)
        self.U_ = X_full @ Vt_global.T / s_global
        
        return self
    
    def transform(self, X):
        """
        Transform data using the fitted distributed SVD.
        
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
        X_centered = X - self.mean_
        
        # Project onto right singular vectors
        X_transformed = X_centered @ self.Vt_.T
        
        return X_transformed
    
    def fit_transform(self, X_partitions):
        """
        Fit the model and transform the data.
        
        Parameters
        ----------
        X_partitions : list of array-like
            List of data partitions
            
        Returns
        -------
        X_transformed : ndarray
            Transformed data (concatenated from all partitions)
        """
        self.fit(X_partitions)
        
        # Transform all partitions and concatenate
        X_full = np.vstack([np.asarray(X) for X in X_partitions])
        return self.transform(X_full)
    
    def inverse_transform(self, X_transformed):
        """
        Transform data back to original space.
        
        Parameters
        ----------
        X_transformed : array-like, shape (n_samples, n_components)
            Transformed data
            
        Returns
        -------
        X : ndarray, shape (n_samples, n_features)
            Data in original space
        """
        X_transformed = np.asarray(X_transformed)
        
        # Project back using Vt
        X = X_transformed @ self.Vt_ + self.mean_
        
        return X
    
    def explained_variance_ratio(self):
        """
        Compute the proportion of variance explained by each component.
        
        Returns
        -------
        explained_variance_ratio : ndarray
            Percentage of variance explained by each component
        """
        if self.s_ is None:
            raise ValueError("Model has not been fitted yet.")
        
        # Variance is proportional to squared singular values
        variance = self.s_ ** 2
        total_variance = np.sum(variance)
        
        return variance / total_variance
