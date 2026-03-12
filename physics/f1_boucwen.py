import numpy as np
from physics.base import DynamicalSystem


class F1BoucWen(DynamicalSystem):
    has_memory = True

    def __init__(self, A=1.0, beta=0.5, gamma=0.5):
        self.A = A
        self.beta = beta
        self.gamma = gamma

    def rhs(self, t, x):
        u, z = x
        dz = self.A * u - self.beta * abs(u) * z - self.gamma * u * abs(z)
        return [z, dz]

    def initial_conditions(self):
        return [0.1, 0.0]
