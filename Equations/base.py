from abc import ABC, abstractmethod
import numpy as np
from scipy.integrate import solve_ivp


class DynamicalSystem(ABC):
    """
    Abstract base class for all dynamical systems
    """

    def __init__(self, name: str, dim: int):
        self.name = name
        self.dim = dim

    @abstractmethod
    def rhs(self, t, x):
        """Right-hand side dx/dt"""
        pass

    @abstractmethod
    def initial_conditions(self):
        """Return initial condition vector"""
        pass

    def simulate(self, x0, t):
        sol = solve_ivp(
            fun=self.rhs,
            t_span=(t[0], t[-1]),
            y0=x0,
            t_eval=t,
            rtol=1e-8,
            atol=1e-10,
        )
        return sol.y.T
