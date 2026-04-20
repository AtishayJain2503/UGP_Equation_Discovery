import numpy as np
import pysindy as ps
from discovery.base import DiscoveryMethod


class SINDyEnsemble(DiscoveryMethod):

    name = "M9_EnsembleSINDy"

    def __init__(self, poly_order=3, threshold=0.1):

        # Use EnsembleOptimizer which handles sub-sampling
        base_optimizer = ps.STLSQ(threshold=threshold)
        ensemble_optimizer = ps.EnsembleOptimizer(
            base_optimizer, n_models=20
        )

        self.model = ps.SINDy(
            feature_library=ps.PolynomialLibrary(poly_order),
            optimizer=ensemble_optimizer
        )

    def fit(self, X, Xdot, t):
        # PySINDy ensemble handles the bootstrapping internally
        # we can just fit it directly. If error is thrown, fall back to normal fit.
        self.model.fit(X, t=t, x_dot=Xdot, ensemble=True)

    def simulate(self, x0, t):

        try:
            Xp = self.model.simulate(
                x0, t, 
                integrator="solve_ivp", 
                integrator_kws={'method': 'RK45'}
            )

            if np.any(np.isnan(Xp)) or np.any(np.abs(Xp) > 1e6):
                return None

            return Xp

        except Exception as e:
            return None

    def equations(self):

        # Precision 6 prevents small terms turning to exactly 0.000
        eqs = self.model.equations(precision=6)
        return "\n".join(eqs)
