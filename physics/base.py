# physics/base.py
from abc import ABC, abstractmethod
import numpy as np

class DynamicalSystem(ABC):
    """
    Abstract base class for all continuous-time dynamical systems.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass

    @property
    @abstractmethod
    def state_names(self) -> list:
        pass

    @abstractmethod
    def parameters(self) -> dict:
        pass

    @abstractmethod
    def initial_conditions(self) -> np.ndarray:
        pass

    @abstractmethod
    def rhs(self, t: float, x: np.ndarray) -> np.ndarray:
        pass
