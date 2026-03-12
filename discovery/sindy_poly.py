import numpy as np
import pysindy as ps
from discovery.base import DiscoveryMethod


class SINDyPoly(DiscoveryMethod):

    name = "SINDy_poly"

    def __init__(self, poly_order=3, threshold=0.1):

        self.model = ps.SINDy(
            feature_library=ps.PolynomialLibrary(poly_order),
            optimizer=ps.STLSQ(threshold=threshold)
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