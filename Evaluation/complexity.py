def count_terms(model):
    """
    Works with PySINDy models
    """
    eqs = model.equations()
    total_terms = 0

    for eq in eqs:
        terms = eq.split('+')
        total_terms += len(terms)

    return total_terms
