import numpy as np
from equations.base import DynamicalSystem

class LargeAnglePendulum(DynamicalSystem):
    """
    B2: Large-angle pendulum (nonlinear)
    theta'' + (g/l) sin(theta) = 0
    """

    name = "B2_Large_Angle_Pendulum"
    state_dim = 2

    def __init__(self, g=9.81, length=1.0):
        self.g = g
        self.length = length

    def rhs(self, t, x):
        theta, omega = x
        dtheta = omega
        domega = -(self.g / self.length) * np.sin(theta)
        return np.array([dtheta, domega])

    def initial_conditions(self):
        # Large angle → strongly nonlinear
        return np.array([np.pi / 2, 0.0])
