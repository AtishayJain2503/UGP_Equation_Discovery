import numpy as np
from physics.base import DynamicalSystem


class A2LinearOscillator(DynamicalSystem):
    def __init__(self, omega=1.0):
        self.omega = omega

    def rhs(self, t, x):
        return [x[1], -self.omega**2 * x[0]]

    def initial_conditions(self):
        return [1.0, 0.0]
