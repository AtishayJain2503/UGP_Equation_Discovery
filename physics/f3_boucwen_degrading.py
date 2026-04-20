import numpy as np
from physics.base import DynamicalSystem


class F3BoucWenDegrading(DynamicalSystem):
    has_memory = True

    def __init__(self, omega=1.0, zeta=0.1, alpha=0.5, A=1.0, beta=0.5, gamma=0.5, delta=0.05):
        self.omega = omega
        self.zeta = zeta
        self.alpha = alpha
        self.A = A
        self.beta = beta
        self.gamma = gamma
        self.delta = delta

    @property
    def true_equation(self):
        return f"x0_dot = x1\nx1_dot = -{self.omega**2:.4f} * x0 - {self.zeta:.4f} * x1 - {self.alpha:.4f} * x2\nx2_dot = ({self.A:.4f} - {self.delta:.4f} * x3) * x1 - {self.beta:.4f} * abs(x1) * x2 - {self.gamma:.4f} * x1 * abs(x2)\nx3_dot = x2 * x1"

    def rhs(self, t, x):
        u, v, z, e = x

        du = v
        dv = -self.omega**2 * u - self.zeta * v - self.alpha * z
        
        # Degrading stiffness A_degraded = A - delta * e
        A_degraded = self.A - self.delta * e
        dz = A_degraded * v - self.beta * abs(v) * z - self.gamma * v * abs(z)
        
        # Energy dissipation state
        de = z * v

        return [du, dv, dz, de]

    def initial_conditions(self):
        return [1.0, 0.0, 0.0, 0.0]
