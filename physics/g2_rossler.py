import numpy as np
from physics.base import DynamicalSystem


class G2Rossler(DynamicalSystem):

    def __init__(self, a=0.2, b=0.2, c=5.7):

        self.a = a
        self.b = b
        self.c = c

    def rhs(self, t, x):

        dx = -x[1] - x[2]
        dy = x[0] + self.a * x[1]
        dz = self.b + x[2] * (x[0] - self.c)

        return [dx, dy, dz]

    def initial_conditions(self):

        return [1.0, 1.0, 1.0]