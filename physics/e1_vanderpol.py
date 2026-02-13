import numpy as np
from physics.base import DynamicalSystem

class E1VanDerPol(DynamicalSystem):
    """
    Van der Pol oscillator:
    x'' - mu (1 - x^2) x' + x = 0
    """

    def __init__(self):
        self._mu = 1.5

    @property
    def name(self):
        return "E1"

    @property
    def dimension(self):
        return 2

    @property
    def state_names(self):
        return ["x", "x_dot"]

    def parameters(self):
        return {
            "mu": self._mu
        }

    def initial_conditions(self):
        return np.array([2.0, 0.0])

    def rhs(self, t, x):
        x1, x2 = x
        dx1 = x2
        dx2 = self._mu * (1 - x1**2) * x2 - x1
        return np.array([dx1, dx2])
