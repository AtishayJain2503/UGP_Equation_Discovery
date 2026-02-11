import numpy as np
from equations.base import DynamicalSystem


class ForcedDuffing(DynamicalSystem):
    """
    D1: Forced Duffing Oscillator

    x'' + δ x' + α x + β x^3 = γ cos(ω t)
    """

    name = "D1_Forced_Duffing"
    state_dim = 2

    def __init__(
        self,
        alpha=1.0,
        beta=1.0,
        damping=0.02,
        gamma=0.3,
        omega=1.2,
    ):
        self.alpha = alpha
        self.beta = beta
        self.damping = damping
        self.gamma = gamma
        self.omega = omega

    def rhs(self, t, x):
        pos, vel = x

        dpos = vel
        dvel = (
            -self.damping * vel
            - self.alpha * pos
            - self.beta * pos**3
            + self.gamma * np.cos(self.omega * t)
        )

        return np.array([dpos, dvel])

    def initial_conditions(self):
        return np.array([1.0, 0.0])
