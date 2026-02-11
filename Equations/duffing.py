import numpy as np
from equations.base import DynamicalSystem

class DuffingOscillator(DynamicalSystem):
    """
    C2: Duffing Oscillator
    x'' + δ x' + α x + β x^3 = 0
    """

    name = "C2_Duffing_Oscillator"
    state_dim = 2

    def __init__(self, alpha=1.0, beta=1.0, damping=0.1):
        self.alpha = alpha
        self.beta = beta
        self.damping = damping

    def rhs(self, t, x):
        pos, vel = x
        dpos = vel
        dvel = (
            -self.damping * vel
            - self.alpha * pos
            - self.beta * pos**3
        )

        # print("RHS CALLED:", pos, vel, "->", dpos, dvel)

        return np.array([dpos, dvel])


    def initial_conditions(self):
        return np.array([1.0, 0.0])
