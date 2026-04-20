import numpy as np
import pysindy as ps
from sklearn.linear_model import BayesianRidge
from scipy.integrate import solve_ivp

from discovery.base import DiscoveryMethod


class BayesianSINDy(DiscoveryMethod):

    name = "M3_BayesianSINDy"

    def __init__(self, poly_order=3, threshold=0.01):

        self.poly_order = poly_order
        self.library = ps.PolynomialLibrary(degree=poly_order)
        self.threshold = threshold
        self.coefs = None
        self.feature_names = None

    def fit(self, X, Xdot, t):

        # build feature matrix
        Theta = self.library.fit_transform(X)

        # store feature names for equation reconstruction
        self.feature_names = self.library.get_feature_names()

        self.state_dim = Xdot.shape[1]
        coefs = []

        for i in range(self.state_dim):

            y = Xdot[:, i]

            reg = BayesianRidge()
            reg.fit(Theta, y)

            c = reg.coef_.copy()
            # threshold small coefficients for sparsity
            c[np.abs(c) < self.threshold] = 0.0
            coefs.append(c)

        self.coefs = np.array(coefs)

    def rhs(self, t, x):

        Theta = self.library.transform(x.reshape(1, -1))

        dx = Theta @ self.coefs.T

        return dx.flatten()

    def simulate(self, x0, t):

        try:

            sol = solve_ivp(
                self.rhs,
                (t[0], t[-1]),
                x0,
                t_eval=t
            )

            if not sol.success:
                return None

            return sol.y.T

        except:
            return None

    def equations(self):

        if self.coefs is None or self.feature_names is None:
            return "Not fitted yet"

        eq_lines = []
        for i in range(self.coefs.shape[0]):
            terms = []
            for j, name in enumerate(self.feature_names):
                c = self.coefs[i, j]
                if abs(c) > 1e-10:
                    terms.append(f"{c:+.6f} {name}")

            if terms:
                eq_lines.append(f"x{i}_dot = " + " ".join(terms))
            else:
                eq_lines.append(f"x{i}_dot = 0")

        return "\n".join(eq_lines)