import numpy as np
from physics.base import DynamicalSystem


class E1VanDerPol(DynamicalSystem):
    def __init__(self, mu=2.0):
        self.mu = mu

    def rhs(self, t, x):
        return [
            x[1],
            self.mu * (1 - x[0] ** 2) * x[1] - x[0],
        ]

    def initial_conditions(self):
        return [2.0, 0.0]
