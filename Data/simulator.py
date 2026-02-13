import numpy as np
from scipy.integrate import solve_ivp

def simulate(system, t):
    """
    Generic ODE simulator for any DynamicalSystem.
    """
    x0 = system.initial_conditions()

    sol = solve_ivp(
        fun=system.rhs,
        t_span=(t[0], t[-1]),
        y0=x0,
        t_eval=t,
        method="RK45"
    )

    return sol.y.T
