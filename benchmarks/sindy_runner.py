import numpy as np
import pysindy as ps
import matplotlib.pyplot as plt

from evaluation.metrics import normalized_mse
from evaluation.rollout import rollout_error
from evaluation.complexity import count_terms


def run_sindy(system, t, x0, noise_std=0.0, poly_order=3):
    # ---- Simulate ground truth
    X = system.simulate(x0, t)

    if noise_std > 0:
        X = X + noise_std * np.std(X, axis=0) * np.random.randn(*X.shape)

    dt = t[1] - t[0]

    # ---- Fit SINDy
    model = ps.SINDy(
        feature_library=ps.PolynomialLibrary(degree=poly_order),
        optimizer=ps.STLSQ(threshold=0.05)
    )

    model.fit(X, t=dt)

    # ---- Rollout prediction
    X_pred = model.simulate(X[0], t)

    # ---- Metrics
    nmse = normalized_mse(X, X_pred)
    rollout_err = rollout_error(X, X_pred)
    complexity = count_terms(model)

    return {
        "model": model,
        "nmse": nmse,
        "rollout_error": rollout_err,
        "complexity": complexity,
        "X_true": X,
        "X_pred": X_pred
    }
