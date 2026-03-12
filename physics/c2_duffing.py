import numpy as np
from physics.base import DynamicalSystem


class C2DampedDuffing(DynamicalSystem):
    is_autonomous = True

    def __init__(self, delta=0.2, alpha=-1.0, beta=1.0):
        self.delta = delta
        self.alpha = alpha
        self.beta = beta

    def rhs(self, t, x):
        position, velocity = x

        dpos = velocity
        dvel = (
            -self.delta * velocity
            - self.alpha * position
            - self.beta * position**3
        )

        return [dpos, dvel]

    def initial_conditions(self):
        return [1.0, 0.0]