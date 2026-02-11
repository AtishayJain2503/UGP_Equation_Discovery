import numpy as np
import matplotlib.pyplot as plt
from equations.forced_duffing import ForcedDuffing


def main():
    # Time grid
    dt = 0.01
    t = np.arange(0.0, 50.0, dt)

    # System
    system = ForcedDuffing(
        alpha=1.0,
        beta=1.0,
        damping=0.02,
        gamma=0.3,
        omega=1.2,
    )

    # Initial condition
    x0 = system.initial_conditions()

    # Simulate
    X = system.simulate(x0, t)

    x = X[:, 0]
    v = X[:, 1]

    # Plot
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))

    axs[0].plot(t, x)
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Displacement")
    axs[0].set_title("Displacement vs Time")

    axs[1].plot(t, v)
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Velocity")
    axs[1].set_title("Velocity vs Time")

    axs[2].plot(x, v)
    axs[2].set_xlabel("Displacement")
    axs[2].set_ylabel("Velocity")
    axs[2].set_title("Phase Portrait")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
