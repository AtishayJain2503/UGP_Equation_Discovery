import numpy as np
import torch
import torch.nn as nn
from scipy.integrate import solve_ivp


class PINNNet(nn.Module):

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


class PINNMethod:

    name = "M6_PINN"

    def __init__(self):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.input_dim = None
        self.state_dim = None
        self.final_loss = None

    def fit(self, X, Xdot, t):

        self.input_dim = X.shape[1]
        self.state_dim = Xdot.shape[1]

        X_t = torch.tensor(X, dtype=torch.float32).to(self.device)
        Xdot_t = torch.tensor(Xdot, dtype=torch.float32).to(self.device)

        self.model = PINNNet(self.input_dim, self.state_dim).to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=500)

        for epoch in range(500):

            pred = self.model(X_t)

            loss = ((pred - Xdot_t) ** 2).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

        self.final_loss = loss.item()

    def rhs(self, t, x):

        x = np.array(x)

        with torch.no_grad():
            x_t = torch.tensor(x.reshape(1, -1), dtype=torch.float32).to(self.device)
            dx = self.model(x_t).cpu().numpy()[0]

        return dx

    def simulate(self, x0, t):

        self.model.eval()

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

        loss_str = f"{self.final_loss:.6e}" if self.final_loss is not None else "N/A"
        return f"PINN: MLP [{self.input_dim}->64->64->{self.state_dim}], 500 epochs, final_loss={loss_str}"