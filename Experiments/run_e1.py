import numpy as np

from equations.van_der_pol import VanDerPol
from utils.plotting import plot_time_series, plot_phase


def main():
    # -----------------------
    # Simulation parameters
    # -----------------------
    t = np.linspace(0, 20, 3000)

    # -----------------------
    # System
    # -----------------------
    system = VanDerPol(mu=1.5)
    x0 = system.initial_conditions()

    # -----------------------
    # Simulate
    # -----------------------
    X = system.simulate(x0, t)

    print("E1 Van der Pol")
    print("X shape:", X.shape)
    print("pos min/max:", X[:, 0].min(), X[:, 0].max())
    print("vel min/max:", X[:, 1].min(), X[:, 1].max())

    # -----------------------
    # Plots
    # -----------------------
    plot_time_series(
        t,
        X,
        labels=["x", "v"],
        title="Van der Pol Oscillator (Time Series)",
    )

    plot_phase(
        X[:, 0],
        X[:, 1],
        xlabel="x",
        ylabel="v",
        title="Van der Pol Phase Portrait",
    )


if __name__ == "__main__":
    main()
