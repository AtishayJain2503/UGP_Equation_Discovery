import numpy as np
import pysindy as ps
from sklearn.linear_model import BayesianRidge

from discovery.base import DiscoveryMethod


class BayesianSINDy(DiscoveryMethod):

    name = "M3_BayesianSINDy"

    def __init__(self, poly_order=3):

        self.library = ps.PolynomialLibrary(degree=poly_order)

        # use Bayesian ridge regression
        self.regressor = BayesianRidge()

        self.model = None

    def fit(self, X, Xdot, t):

        # build feature matrix
        Theta = self.library.fit_transform(X)

        coefs = []

        for i in range(Xdot.shape[1]):

            y = Xdot[:, i]

            self.regressor.fit(Theta, y)

            coefs.append(self.regressor.coef_)

        self.coefs = np.array(coefs)

        self.X = X

    def rhs(self, t, x):

        Theta = self.library.transform(x.reshape(1, -1))

        dx = Theta @ self.coefs.T

        return dx.flatten()

    def simulate(self, x0, t):

        from scipy.integrate import solve_ivp

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

        return "Bayesian sparse regression"