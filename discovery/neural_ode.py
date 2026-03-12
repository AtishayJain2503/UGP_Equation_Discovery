import numpy as np
import torch
import torch.nn as nn
from scipy.integrate import solve_ivp


class NeuralODEModel(nn.Module):

    def __init__(self, input_dim, state_dim):

        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, state_dim)
        )

    def forward(self, x):

        return self.net(x)


class NeuralODE:

    name = "M5_NeuralODE"

    def __init__(self):

        self.model = None
        self.input_dim = None
        self.state_dim = None

    def fit(self, X, Xdot, t):

        self.input_dim = X.shape[1]
        self.state_dim = Xdot.shape[1]

        X_t = torch.tensor(X, dtype=torch.float32)
        Xdot_t = torch.tensor(Xdot, dtype=torch.float32)

        # create network here (after knowing dimensions)
        self.model = NeuralODEModel(self.input_dim, self.state_dim)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)

        for _ in range(1000):

            pred = self.model(X_t)

            loss = ((pred - Xdot_t) ** 2).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def rhs(self, t, x):

        x = np.array(x)

        # add time feature if necessary
        if len(x) < self.input_dim:
            x = np.concatenate([x, [t]])

        x_t = torch.tensor(x.reshape(1, -1), dtype=torch.float32)

        dx = self.model(x_t).detach().numpy()[0]

        return dx

    def simulate(self, x0, t):

        try:

            sol = solve_ivp(
                self.rhs,
                (t[0], t[-1]),
                x0,
                t_eval=t
            )

            if not sol.success:
                return None

            return sol.y.T

        except:
            return None

    def equations(self):

        return "Neural ODE dynamics"