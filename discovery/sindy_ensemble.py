import numpy as np
import pysindy as ps
from discovery.base import DiscoveryMethod


class SINDyEnsemble(DiscoveryMethod):

    name = "M9_EnsembleSINDy"

    def __init__(self, poly_order=3, threshold=0.1):

        # EnsembleOptimizer requires ensemble_data=True or ensemble_library=True
        # We use ensemble_data=True which sub-samples rows of the data matrix
        base_optimizer = ps.SR3(reg_weight_lam=threshold, regularizer='L0')
        self.ensemble_optimizer = ps.EnsembleOptimizer(
            base_optimizer,
            bagging=True,
            n_models=20,
        )

        self.library = ps.PolynomialLibrary(poly_order)
        self.model = ps.SINDy(
            feature_library=self.library,
            optimizer=self.ensemble_optimizer,
            differentiation_method=ps.SmoothedFiniteDifference()
        )

    def fit(self, X, Xdot, t):
        self.model.fit(X, t=t, x_dot=Xdot)

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

        except Exception:
            return None

    def equations(self):

        eqs = self.model.equations(precision=6)
        return "\n".join(eqs)
