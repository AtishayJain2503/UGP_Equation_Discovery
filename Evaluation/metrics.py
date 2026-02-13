import numpy as np

def mse(true, pred):
    """
    Mean Squared Error over trajectories
    """
    return np.mean((true - pred) ** 2)


def rmse(true, pred):
    """
    Root Mean Squared Error
    """
    return np.sqrt(mse(true, pred))


def nmse(true, pred):
    """
    Normalized Mean Squared Error
    Normalized by variance of true signal
    """
    return mse(true, pred) / np.var(true)
