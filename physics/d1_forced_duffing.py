import numpy as np
from physics.base import DynamicalSystem


class D1ForcedDuffing(DynamicalSystem):
    is_autonomous = False

    def __init__(self, delta=0.2, alpha=-1.0, beta=1.0, gamma=0.3, omega=1.2):
        self.delta = delta
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.omega = omega

    def rhs(self, t, x):
        return [
            x[1],
            -self.delta * x[1]
            - self.alpha * x[0]
            - self.beta * x[0] ** 3
            + self.gamma * np.cos(self.omega * t),
        ]

    def initial_conditions(self):
        return [1.0, 0.0]
