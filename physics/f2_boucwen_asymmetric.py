import numpy as np
from physics.base import DynamicalSystem


class F2BoucWenAsymmetric(DynamicalSystem):
    has_memory = True

    def __init__(self, omega=1.0, zeta=0.1, alpha=0.5, A=1.0, beta=0.5, gamma=0.5, n=2):
        self.omega = omega
        self.zeta = zeta
        self.alpha = alpha
        self.A = A
        self.beta = beta
        self.gamma = gamma
        self.n = n

    @property
    def true_equation(self):
        return f"x0_dot = x1\nx1_dot = -{self.omega**2:.4f} * x0 - {self.zeta:.4f} * x1 - {self.alpha:.4f} * x2\nx2_dot = {self.A:.4f} * x1 - {self.beta:.4f} * abs(x1) * abs(x2)**({self.n-1}) * x2 - {self.gamma:.4f} * x1 * abs(x2)**{self.n}"

    def rhs(self, t, x):
        u, v, z = x

        du = v
        dv = -self.omega**2 * u - self.zeta * v - self.alpha * z
        
        # Asymmetric variant (exponent n)
        dz = self.A * v - self.beta * abs(v) * abs(z)**(self.n - 1) * z - self.gamma * v * abs(z)**self.n

        return [du, dv, dz]

    def initial_conditions(self):
        return [1.0, 0.0, 0.0]
