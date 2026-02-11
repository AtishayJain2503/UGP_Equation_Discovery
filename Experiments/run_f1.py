import numpy as np

from equations.bouc_wen_minimal import BoucWenMinimal
from utils.plotting import plot_time_series, plot_phase


def main():
    # -----------------------
    # Simulation parameters
    # -----------------------
    t = np.linspace(0, 40, 6000)

    # -----------------------
    # System
    # -----------------------
    system = BoucWenMinimal(
        k=1.0,
        c=0.05,
        alpha=1.0,
        A=1.0,
        beta=0.8,
    )

    x0 = system.initial_conditions()

    # -----------------------
    # Simulate
    # -----------------------
    X = system.simulate(x0, t)

    print("F1 Minimal Bouc–Wen")
    print("X shape:", X.shape)
    print("pos min/max:", X[:, 0].min(), X[:, 0].max())
    print("vel min/max:", X[:, 1].min(), X[:, 1].max())
    print("z min/max:", X[:, 2].min(), X[:, 2].max())

    # -----------------------
    # Full-state plots
    # -----------------------
    plot_time_series(
        t,
        X,
        labels=["x", "v", "z"],
        title="Minimal Bouc–Wen (Time Series)",
    )

    # -----------------------
    # Phase plots
    # -----------------------
    plot_phase(
        X[:, 0],
        X[:, 1],
        xlabel="x",
        ylabel="v",
        title="Bouc–Wen Phase Portrait (x–v)",
    )

    plot_phase(
        X[:, 1],
        X[:, 2],
        xlabel="v",
        ylabel="z",
        title="Bouc–Wen Internal Hysteresis (v–z)",
    )


if __name__ == "__main__":
    main()
