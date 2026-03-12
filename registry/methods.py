from discovery.sindy_poly import SINDyPoly
from discovery.sindy_custom import SINDyCustom
from discovery.bayesian_sindy import BayesianSINDy
from discovery.pysr_method import PySRMethod
from discovery.neural_ode import NeuralODE
from discovery.pinn import PINNMethod
from discovery.symbolic_grammar import GrammarSymbolic
from discovery.pisf import PISFMethod
from physics.g1_lorenz import G1Lorenz
from physics.g2_rossler import G2Rossler

METHOD_REGISTRY = {   
    "M1_SINDy_poly": SINDyPoly,
    "M2_SINDy_custom": SINDyCustom,
    "M3_BayesianSINDy": BayesianSINDy,
    "M4_PySR": PySRMethod,
    "M5_NeuralODE": NeuralODE,
    "M6_PINN": PINNMethod,
    "M7_GrammarSymbolic": GrammarSymbolic,
    "M8_PISF": PISFMethod,
}