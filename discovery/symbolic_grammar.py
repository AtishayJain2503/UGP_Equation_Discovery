import numpy as np
from pysr import PySRRegressor
from scipy.integrate import solve_ivp


class GrammarSymbolic:

    name = "M7_GrammarSymbolic"

    def __init__(self):

        self.models = []

    def fit(self, X, Xdot, t):

        self.models = []

        for i in range(Xdot.shape[1]):

            model = PySRRegressor(
                niterations=60,
                binary_operators=["+", "-", "*"],
                unary_operators=["sin", "cos"],
                maxsize=20,
                progress=False
            )

            model.fit(X, Xdot[:, i])

            self.models.append(model)

    def rhs(self, t, x):

        dx = []

        for m in self.models:

            dx.append(m.predict(x.reshape(1, -1))[0])

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