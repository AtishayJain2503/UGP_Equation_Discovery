import numpy as np
from physics.base import DynamicalSystem

class F1BoucWen(DynamicalSystem):
    """
    Minimal Bouc–Wen hysteresis model (no pinching, no degradation)

    x'' + c x' + k x + alpha z = 0
    z' = A x' - beta |x'| |z|^{n-1} z - gamma x' |z|^n
    """

    def __init__(self):
        # Mechanical parameters
        self._c = 0.05
        self._k = 1.0
        self._alpha = 1.0

        # Bouc–Wen parameters
        self._A = 1.0
        self._beta = 0.5
        self._gamma = 0.5
        self._n = 1

    @property
    def name(self):
        return "F1"

    @property
    def dimension(self):
        return 3

    @property
    def state_names(self):
        return ["x", "x_dot", "z"]

    def parameters(self):
        return {
            "c": self._c,
            "k": self._k,
            "alpha": self._alpha,
            "A": self._A,
            "beta": self._beta,
            "gamma": self._gamma,
            "n": self._n,
        }

    def initial_conditions(self):
        return np.array([1.0, 0.0, 0.0])

    def rhs(self, t, x):
        x1, x2, z = x

        dx1 = x2
        dx2 = -self._c * x2 - self._k * x1 - self._alpha * z

        dz = (
            self._A * x2
            - self._beta * np.abs(x2) * np.abs(z) ** (self._n - 1) * z
            - self._gamma * x2 * np.abs(z) ** self._n
        )

        return np.array([dx1, dx2, dz])
