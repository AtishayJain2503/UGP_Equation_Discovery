import numpy as np
from physics.base import DynamicalSystem

class A2LinearOscillator(DynamicalSystem):

    def __init__(self):
        self._omega = 1.0
        self._zeta = 0.02

    @property
    def name(self):
        return "A2"

    @property
    def dimension(self):
        return 2

    @property
    def state_names(self):
        return ["x", "x_dot"]

    def parameters(self):
        return {
            "omega": self._omega,
            "zeta": self._zeta
        }

    def initial_conditions(self):
        return np.array([1.0, 0.0])

    def rhs(self, t, x):
        x1, x2 = x
        dx1 = x2
        dx2 = -2*self._zeta*self._omega*x2 - self._omega**2 * x1
        return np.array([dx1, dx2])
