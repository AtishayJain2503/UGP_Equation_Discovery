import numpy as np
from physics.base import DynamicalSystem

class D1ForcedDuffing(DynamicalSystem):
    """
    Forced Duffing oscillator:
    x'' + delta x' + alpha x + beta x^3 = gamma cos(omega t)
    """

    def __init__(self):
        self._delta = 0.2
        self._alpha = -1.0
        self._beta = 1.0
        self._gamma = 0.3
        self._omega = 1.2

    @property
    def name(self):
        return "D1"

    @property
    def dimension(self):
        return 2

    @property
    def state_names(self):
        return ["x", "x_dot"]

    def parameters(self):
        return {
            "delta": self._delta,
            "alpha": self._alpha,
            "beta": self._beta,
            "gamma": self._gamma,
            "omega": self._omega,
        }

    def initial_conditions(self):
        return np.array([1.0, 0.0])

    def rhs(self, t, x):
        x1, x2 = x
        dx1 = x2
        dx2 = (
            -self._delta * x2
            - self._alpha * x1
            - self._beta * x1**3
            + self._gamma * np.cos(self._omega * t)
        )
        return np.array([dx1, dx2])
