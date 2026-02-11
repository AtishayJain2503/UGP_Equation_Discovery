import numpy as np
from equations.base import DynamicalSystem


class BoucWenMinimal(DynamicalSystem):
    """
    F1: Minimal Bouc–Wen hysteresis model
    """

    def __init__(
        self,
        k=1.0,
        c=0.05,
        alpha=1.0,
        A=1.0,
        beta=0.5,
    ):
        super().__init__(name="BoucWenMinimal", dim=3)

        self.k = k
        self.c = c
        self.alpha = alpha
        self.A = A
        self.beta = beta

    def rhs(self, t, x):
        pos, vel, z = x

        dpos = vel
        dvel = -self.k * pos - self.c * vel - self.alpha * z
        dz = self.A * vel - self.beta * np.abs(vel) * z

        return np.array([dpos, dvel, dz])

    def initial_conditions(self):
        return np.array([1.0, 0.0, 0.0])
