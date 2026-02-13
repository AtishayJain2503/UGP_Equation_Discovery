import pysindy as ps
import numpy as np
from methods.base import DiscoveryMethod

class SINDyMethod(DiscoveryMethod):

    def __init__(self, poly_order=3, threshold=0.05):
        self.model = ps.SINDy(
            feature_library=ps.PolynomialLibrary(degree=poly_order),
            optimizer=ps.STLSQ(threshold=threshold)
        )

    def fit(self, X, t):
        dt = t[1] - t[0]
        self.model.fit(X, t=dt)

    def simulate(self, x0, t):
        return self.model.simulate(x0, t)

    def complexity(self):
        return sum(len(eq) > 0 for eq in self.model.coefficients())
