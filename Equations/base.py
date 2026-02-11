import numpy as np
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp


class DynamicalSystem(ABC):
    """
    Abstract base class for all dynamical systems
    """

    name = "abstract_system"
    state_dim = None

    @abstractmethod
    def rhs(self, t, x):
        """
        Right-hand side of the ODE: dx/dt = f(t, x)
        """
        pass

    @abstractmethod
    def initial_conditions(self):
        """
        Return default initial condition
        """
        pass

    def simulate(self, x0, t):
        """
        Simulate the system using solve_ivp
        """

        sol = solve_ivp(
            fun=self.rhs,
            t_span=(t[0], t[-1]),
            y0=x0,
            t_eval=t,
            method="RK45",
            rtol=1e-8,
            atol=1e-10,
        )

        if not sol.success:
            raise RuntimeError("ODE solver failed")

        return sol.y.T
