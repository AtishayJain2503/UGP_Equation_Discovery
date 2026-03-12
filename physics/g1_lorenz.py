import numpy as np
from physics.base import DynamicalSystem


class G1Lorenz(DynamicalSystem):

    def __init__(self, sigma=10.0, rho=28.0, beta=8/3):

        self.sigma = sigma
        self.rho = rho
        self.beta = beta

    def rhs(self, t, x):

        dx = self.sigma * (x[1] - x[0])
        dy = x[0] * (self.rho - x[2]) - x[1]
        dz = x[0] * x[1] - self.beta * x[2]

        return [dx, dy, dz]

    def initial_conditions(self):

        return [1.0, 1.0, 1.0]