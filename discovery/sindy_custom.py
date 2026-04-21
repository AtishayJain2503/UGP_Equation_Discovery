import numpy as np
import pysindy as ps
from discovery.base import DiscoveryMethod


class SINDyCustom(DiscoveryMethod):

    name = "SINDy_custom"

    def __init__(self):

        library = ps.GeneralizedLibrary([
            ps.PolynomialLibrary(3),
            ps.FourierLibrary(n_frequencies=2)
        ])

        self.model = ps.SINDy(
            feature_library=library,
            optimizer=ps.SR3(reg_weight_lam=0.1, regularizer='L0'),
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

        except Exception as e:
            return None

    def equations(self):

        eqs = self.model.equations(precision=6)
        return "\n".join(eqs)