import numpy as np
from scipy.interpolate import UnivariateSpline

from discovery.sindy_poly import SINDyPoly
from discovery.base import DiscoveryMethod


class PISFMethod(DiscoveryMethod):

    name = "M8_PISF"

    def __init__(self):

        self.sindy = SINDyPoly()

    def smooth_derivatives(self, X, t, Xdot_finite):

        Xdot = []

        for i in range(X.shape[1]):

            # Adaptive smoothing: scale with signal variance
            signal_var = np.var(X[:, i])
            s = max(0.001, 0.01 * signal_var) * len(t)

            try:
                spline = UnivariateSpline(t, X[:, i], s=s)
                deriv = spline.derivative()(t)

                # Sanity check: if the spline derivative is wildly off,
                # fall back to finite-difference derivative
                if np.std(deriv) > 100 * np.std(Xdot_finite[:, i]):
                    deriv = Xdot_finite[:, i]

            except Exception:
                deriv = Xdot_finite[:, i]

            Xdot.append(deriv)

        return np.vstack(Xdot).T

    def fit(self, X, Xdot, t):

        smooth_dot = self.smooth_derivatives(X, t, Xdot)

        self.sindy.fit(X, smooth_dot, t)

    def simulate(self, x0, t):

        return self.sindy.simulate(x0, t)

    def equations(self):

        return self.sindy.equations()