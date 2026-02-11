import numpy as np
from equations.base import DynamicalSystem

class DampedOscillator(DynamicalSystem):
    """
    A2: Damped Harmonic Oscillator
    x'' + c x' + ω^2 x = 0
    """

    name = "A2_Damped_Oscillator"
    state_dim = 2

    def __init__(self, omega=1.0, damping=0.1):
        self.omega = omega
        self.damping = damping

    def rhs(self, t, x):
        """
        x = [position, velocity]
        """
        pos, vel = x
        dpos = vel
        dvel = -self.damping * vel - self.omega**2 * pos
        return np.array([dpos, dvel])

    def initial_conditions(self):
        """
        Standard non-zero initial condition
        """
        return np.array([1.0, 0.0])
