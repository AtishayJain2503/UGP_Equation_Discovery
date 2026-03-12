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

        optimizer = ps.STLSQ(threshold=0.1)

        self.model = ps.SINDy(
            feature_library=library,
            optimizer=optimizer
        )

    def fit(self, X, Xdot, t):

        self.model.fit(X, t=t, x_dot=Xdot)

    def simulate(self, x0, t):

        try:
            Xp = self.model.simulate(x0, t)

            if np.any(np.isnan(Xp)) or np.any(np.abs(Xp) > 1e6):
                return None

            return Xp

        except:
            return None

    def equations(self):

        return "\n".join(self.model.equations())