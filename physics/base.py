from abc import ABC, abstractmethod
import numpy as np
from scipy.integrate import solve_ivp


class DynamicalSystem(ABC):
    is_autonomous = True
    has_memory = False

    @abstractmethod
    def rhs(self, t, x):
        pass

    @abstractmethod
    def initial_conditions(self):
        pass

    def simulate(self, t):
        x0 = self.initial_conditions()
        sol = solve_ivp(
            self.rhs,
            (t[0], t[-1]),
            x0,
            t_eval=t,
            rtol=1e-8,
            atol=1e-8,
        )
        return sol.y.T
