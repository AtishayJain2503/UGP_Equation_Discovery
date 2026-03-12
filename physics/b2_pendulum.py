import numpy as np
from physics.base import DynamicalSystem


class B2LargeAnglePendulum(DynamicalSystem):
    is_autonomous = True

    def __init__(self, g=9.81, L=1.0, c=0.05):
        self.g = g
        self.L = L
        self.c = c

    def rhs(self, t, x):
        theta, omega = x

        dtheta = omega
        domega = -(self.g / self.L) * np.sin(theta) - self.c * omega

        return [dtheta, domega]

    def initial_conditions(self):
        # large angle to avoid small-angle approximation
        return [1.5, 0.0]