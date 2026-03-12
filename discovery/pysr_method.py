from pysr import PySRRegressor
import numpy as np
from scipy.integrate import solve_ivp


class PySRMethod:

    name = "M4_PySR"

    def __init__(self):

        self.models = []

    def fit(self, X, Xdot, t):

        self.models = []

        state_dim = Xdot.shape[1]

        for i in range(state_dim):

            model = PySRRegressor(
                niterations=80,
                binary_operators=["+", "-", "*", "/"],
                unary_operators=["sin", "cos", "exp"],
                maxsize=20,
                progress=False
            )

            model.fit(X, Xdot[:, i])

            self.models.append(model)

    def rhs(self, t, x):

        dx = []

        x = np.array(x).reshape(1, -1)

        for m in self.models:

            dx.append(m.predict(x)[0])

        return np.array(dx)

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

        eqs = []

        for m in self.models:

            eqs.append(str(m.sympy()))

        return "\n".join(eqs)