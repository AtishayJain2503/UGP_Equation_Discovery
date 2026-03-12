import numpy as np
from scipy.interpolate import UnivariateSpline

from discovery.sindy_poly import SINDyPoly
from discovery.base import DiscoveryMethod


class PISFMethod(DiscoveryMethod):

    name = "M8_PISF"

    def __init__(self):

        self.sindy = SINDyPoly()

    def smooth_derivatives(self, X, t):

        Xdot = []

        for i in range(X.shape[1]):

            spline = UnivariateSpline(t, X[:, i], s=0.01)

            Xdot.append(spline.derivative()(t))

        return np.vstack(Xdot).T

    def fit(self, X, Xdot, t):

        smooth_dot = self.smooth_derivatives(X, t)

        self.sindy.fit(X, smooth_dot, t)

    def simulate(self, x0, t):

        return self.sindy.simulate(x0, t)

    def equations(self):

        return self.sindy.equations()