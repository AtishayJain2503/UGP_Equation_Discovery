from abc import ABC, abstractmethod

class DiscoveryMethod(ABC):

    @abstractmethod
    def fit(self, X, t):
        pass

    @abstractmethod
    def simulate(self, x0, t):
        pass

    @abstractmethod
    def complexity(self):
        pass
