import numpy as np
from equations.base import DynamicalSystem


class VanDerPol(DynamicalSystem):
    """
    E1: Van der Pol Oscillator
    """

    def __init__(self, mu=1.0):
        super().__init__(name="VanDerPol", dim=2)
        self.mu = mu

    def rhs(self, t, x):
        pos, vel = x

        dpos = vel
        dvel = self.mu * (1 - pos**2) * vel - pos

        return np.array([dpos, dvel])

    def initial_conditions(self):
        return np.array([1.0, 0.0])
