from physics.a2_linear import A2LinearOscillator
from physics.b2_pendulum import B2LargeAnglePendulum
from physics.c2_duffing import C2DampedDuffing
from physics.d1_forced_duffing import D1ForcedDuffing
from physics.e1_vanderpol import E1VanDerPol
from physics.f1_boucwen import F1BoucWen
from physics.f2_boucwen_asymmetric import F2BoucWenAsymmetric
from physics.f3_boucwen_degrading import F3BoucWenDegrading
from physics.g1_lorenz import G1Lorenz
from physics.g2_rossler import G2Rossler

SYSTEM_REGISTRY = {
    "A2": {
        "class": A2LinearOscillator,
        "poly_order": 1,        
        "threshold": 0.05,
    },

    "B2": {
        "class": B2LargeAnglePendulum,
        "poly_order": 3,        
        "threshold": 0.1,
    },

    "C2": {
        "class": C2DampedDuffing,
        "poly_order": 3,        
        "threshold": 0.1,
    },

    "D1": {
        "class": D1ForcedDuffing,
        "poly_order": 3,
        "threshold": 0.1,
    },

    "E1": {
        "class": E1VanDerPol,
        "poly_order": 3,
        "threshold": 0.1,
    },

    "F1": {
        "class": F1BoucWen,
        "poly_order": 3,
        "threshold": 0.1,
    },
    
    "F2": {
        "class": F2BoucWenAsymmetric,
        "poly_order": 3,
        "threshold": 0.1,
    },
    
    "F3": {
        "class": F3BoucWenDegrading,
        "poly_order": 3,
        "threshold": 0.1,
    },
    
    "G1": {
        "class": G1Lorenz,
        "poly_order": 3,
        "threshold": 0.05
    },
    
    "G2": {
        "class": G2Rossler,
        "poly_order": 3,
        "threshold": 0.05
    }
}