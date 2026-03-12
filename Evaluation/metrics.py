import numpy as np


def mse(true, pred):
    return np.mean((true - pred) ** 2)


def rmse(true, pred):
    return np.sqrt(mse(true, pred))


def normalized_mse(true, pred):
    """
    NMSE normalized by variance of true signal
    """
    return mse(true, pred) / np.var(true)


# alias for backward compatibility
nmse = normalized_mse