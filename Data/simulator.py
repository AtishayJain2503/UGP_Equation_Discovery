import numpy as np
from scipy.integrate import solve_ivp

class Simulator:
    """
    Generic ODE simulator for DynamicalSystem objects
    """

    def __init__(self, system, dt=0.01, T=50.0):
        self.system = system
        self.dt = dt
        self.T = T

    def run(self, x0=None):
        if x0 is None:
            x0 = self.system.initial_conditions()

        t_eval = np.arange(0.0, self.T, self.dt)

        sol = solve_ivp(
            fun=self.system,
            t_span=(0.0, self.T),
            y0=x0,
            t_eval=t_eval,
            method="RK45"
        )

        if not sol.success:
            raise RuntimeError("ODE solver failed.")

        return sol.t, sol.y.T
