from abc import ABC, abstractmethod
import numpy as np

class DynamicalSystem(ABC):
    """
    Abstract base class for all dynamical systems.
    Each system must define:
    - state dimension
    - RHS of ODE
    - initial conditions
    """

    name: str
    state_dim: int

    @abstractmethod
    def rhs(self, t, x):
        """
        Right-hand side of ODE: dx/dt = f(x, t)
        """
        pass

    @abstractmethod
    def initial_conditions(self):
        """
        Return a valid initial condition for simulation
        """
        pass

    def __call__(self, t, x):
        """
        Allows the system to be passed directly to ODE solvers
        """
        return self.rhs(t, x)
