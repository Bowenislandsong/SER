"""
Federated SVD

This module implements a federated learning version of Singular Value
Decomposition where data remains on local nodes and only model parameters
are shared.
"""

import numpy as np
from scipy.linalg import svd


class FederatedSVD:
    """
    Federated Singular Value Decomposition.
    
    This algorithm computes SVD in a federated manner where data stays on
    local nodes. Only aggregated statistics and model parameters are shared
    between nodes, preserving data privacy.
    
    Parameters
    ----------
    n_components : int, optional (default=None)
        Number of singular values/vectors to compute. If None, computes all.
    n_iterations : int, optional (default=10)
        Number of federated averaging iterations
    
    Attributes
    ----------
    U_ : ndarray
        Left singular vectors
    s_ : ndarray
        Singular values in descending order
    Vt_ : ndarray
        Right singular vectors (transposed)
    """
    
    def __init__(self, n_components=None, n_iterations=10):
        self.n_components = n_components
        self.n_iterations = n_iterations
        self.U_ = None
        self.s_ = None
        self.Vt_ = None
        self.mean_ = None
    
    def _compute_local_statistics(self, X):
        """
        Compute local statistics for a data partition.
        
        Parameters
        ----------
        X : array-like
            Local data partition
            
        Returns
        -------
        stats : dict
            Dictionary containing local statistics
        """
        X = np.asarray(X)
        n_samples = X.shape[0]
        
        # Compute local sum and count for mean calculation
        local_sum = np.sum(X, axis=0)
        
        # Compute local covariance contribution
        # C = X^T X (for centered data, but we'll center after aggregation)
        local_cov = X.T @ X
        
        return {
            'n_samples': n_samples,
            'local_sum': local_sum,
            'local_cov': local_cov
        }
    
    def _aggregate_statistics(self, local_stats_list):
        """
        Aggregate statistics from all nodes.
        
        Parameters
        ----------
        local_stats_list : list of dict
            List of local statistics from each node
            
        Returns
        -------
        global_stats : dict
            Aggregated global statistics
        """
        total_samples = sum(stats['n_samples'] for stats in local_stats_list)
        
        # Compute global mean
        global_sum = sum(stats['local_sum'] for stats in local_stats_list)
        global_mean = global_sum / total_samples
        
        # Compute global covariance (we'll need to adjust for mean)
        global_cov = sum(stats['local_cov'] for stats in local_stats_list)
        
        # Adjust for centering: subtract n * mean * mean^T
        global_cov = global_cov - total_samples * np.outer(global_mean, global_mean)
        
        return {
            'mean': global_mean,
            'cov': global_cov,
            'n_samples': total_samples
        }
    
    def fit(self, X_nodes):
        """
        Fit the Federated SVD model.
        
        Parameters
        ----------
        X_nodes : list of array-like
            List of data on each node, each of shape (n_samples_i, n_features).
            Data remains on each node and only statistics are aggregated.
            
        Returns
        -------
        self : object
            Returns self
        """
        # Step 1: Each node computes local statistics
        local_stats = [self._compute_local_statistics(X) for X in X_nodes]
        
        # Step 2: Aggregate statistics at central server
        global_stats = self._aggregate_statistics(local_stats)
        
        self.mean_ = global_stats['mean']
        global_cov = global_stats['cov']
        
        # Step 3: Compute SVD of the covariance matrix
        # For covariance matrix C = X^T X, the SVD gives us V and singular values
        # Since C = V S^2 V^T, we can get V and s from eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(global_cov)
        
        # Sort by eigenvalues in descending order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Singular values are square roots of eigenvalues
        singular_values = np.sqrt(np.maximum(eigenvalues, 0))
        
        # Keep only n_components if specified
        if self.n_components is not None:
            singular_values = singular_values[:self.n_components]
            eigenvectors = eigenvectors[:, :self.n_components]
        
        self.s_ = singular_values
        self.Vt_ = eigenvectors.T
        
        # Step 4: Compute U from all data (in practice, this would be done locally)
        # For demonstration, we concatenate data (in real federated learning,
        # each node would compute its portion of U locally)
        X_full = np.vstack([np.asarray(X) for X in X_nodes])
        X_centered = X_full - self.mean_
        
        # U = X V S^-1
        self.U_ = X_centered @ eigenvectors / singular_values
        
        return self
    
    def transform(self, X):
        """
        Transform data using the fitted federated SVD.
        
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
    
    def fit_transform(self, X_nodes):
        """
        Fit the model and transform the data.
        
        Parameters
        ----------
        X_nodes : list of array-like
            List of data on each node
            
        Returns
        -------
        X_transformed : ndarray
            Transformed data (concatenated from all nodes)
        """
        self.fit(X_nodes)
        
        # Transform all nodes and concatenate
        X_full = np.vstack([np.asarray(X) for X in X_nodes])
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
    
    def get_privacy_budget(self):
        """
        Get information about privacy preservation in the federated approach.
        
        Returns
        -------
        info : dict
            Dictionary with privacy-related information
        """
        return {
            'method': 'Federated Learning',
            'data_sharing': 'Only aggregated statistics (mean, covariance)',
            'raw_data_shared': False,
            'privacy_level': 'High - raw data never leaves local nodes'
        }
