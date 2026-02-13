from physics.a2_linear import A2LinearOscillator
from physics.d1_duffing import D1ForcedDuffing
from physics.e1_vanderpol import E1VanDerPol
from physics.f1_boucwen import F1BoucWen

SYSTEM_REGISTRY = {
    "A2": A2LinearOscillator,
    "D1": D1ForcedDuffing,
    "E1": E1VanDerPol,
    "F1": F1BoucWen,
}
