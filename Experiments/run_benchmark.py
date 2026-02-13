import numpy as np
from registry.systems import SYSTEM_REGISTRY
from methods.sindy import SINDyMethod
from data.simulator import simulate
from evaluation.metrics import nmse

t = np.linspace(0, 30, 3000)

system = SYSTEM_REGISTRY["A2"]()
X_true = simulate(system, t)

method = SINDyMethod()
method.fit(X_true, t)

X_pred = method.simulate(X_true[0], t)

print("NMSE:", nmse(X_true, X_pred))
method.model.print()
