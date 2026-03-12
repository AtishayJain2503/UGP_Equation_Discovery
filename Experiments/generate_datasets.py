import numpy as np
import os
from registry.systems import SYSTEM_REGISTRY


def add_noise(x, level):
    std = np.std(x, axis=0)
    noise = level * std * np.random.randn(*x.shape)
    return x + noise


def generate_dataset(system_id, cfg, t, noise_level):

    system = cfg["class"]()

    X = system.simulate(t)
    dt = t[1] - t[0]
    Xdot = np.gradient(X, dt, axis=0)

    if noise_level > 0:
        X = add_noise(X, noise_level)

    return {
        "t": t,
        "x": X,
        "xdot_true": Xdot,
        "system": system_id,
        "dt": dt,
        "noise_level": noise_level,
    }


def main():

    t = np.linspace(0, 30, 3000)

    noise_levels = {
        "clean": 0.0,
        "noise_2": 0.02,
        "noise_5": 0.05,
    }

    os.makedirs("data", exist_ok=True)

    for sid, cfg in SYSTEM_REGISTRY.items():

        system_dir = f"data/{sid}"
        os.makedirs(system_dir, exist_ok=True)

        for label, noise in noise_levels.items():

            dataset = generate_dataset(sid, cfg, t, noise)

            path = f"{system_dir}/{label}.npz"
            np.savez(path, **dataset)

            print(f"Saved {path}")


if __name__ == "__main__":
    main()