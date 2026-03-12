class DiscoveryMethod:

    name = "base"

    def fit(self, X, Xdot, t):
        raise NotImplementedError

    def simulate(self, x0, t):
        raise NotImplementedError

    def equations(self):
        return "Not available"