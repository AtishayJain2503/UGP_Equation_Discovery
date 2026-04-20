import numpy as np


def count_terms(model):
    """
    Count the number of terms in discovered equations.
    Returns NaN for black-box models (Neural ODE, PINN).
    """
    eqs = model.equations()

    # Black-box models that don't produce symbolic equations
    if isinstance(eqs, str) and ("Neural ODE" in eqs or "PINN" in eqs):
        return np.nan

    # For Bayesian SINDy, count non-zero terms from equations string
    if isinstance(eqs, str):
        lines = eqs.split("\n")
    else:
        lines = eqs

    total_terms = 0
    for eq in lines:
        # Split on + or - as term delimiters (skip the "x0_dot = " prefix)
        eq_body = eq.split("=", 1)[-1] if "=" in eq else eq
        # Count terms by splitting on sign boundaries
        terms = [t.strip() for t in eq_body.replace("-", "+-").split("+") if t.strip()]
        total_terms += len(terms)

    return total_terms
