import numpy as np
import os

from discovery.sindy import SINDyModel
from evaluation.metrics import nmse
from evaluation.plots import time_series, phase_portrait


DATA_DIR = "data"


def load_dataset(path):
    d = np.load(path, allow_pickle=True)
    return d["t"], d["x"], d["xdot_true"], d["system"], d["dt"], d["noise_level"]


def main():

    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("results/equations", exist_ok=True)
    os.makedirs("results/tables", exist_ok=True)

    summary = []

    for system in os.listdir(DATA_DIR):

        system_path = os.path.join(DATA_DIR, system)

        if not os.path.isdir(system_path):
            continue

        for file in os.listdir(system_path):
            if not file.endswith(".npz"):
                continue
            dataset_path = os.path.join(system_path, file)

            t, X, Xdot, system_id, dt, noise = load_dataset(dataset_path)

            label = f"{system_id}_{file.replace('.npz','')}"
            print(f"\nRunning {label}")

            model = SINDyModel(poly_order=3, threshold=0.1)

            model.fit(X, Xdot, t)

            Xp = model.simulate_safe(X[0], t)

            if Xp is None:
                error = np.inf
                status = "UNSTABLE"
            else:
                error = nmse(X, Xp)
                status = "STABLE"

                time_series(label, t, X, Xp, "results/figures")
                phase_portrait(label, X, Xp, "results/figures")

            with open(f"results/equations/{label}.txt", "w") as f:
                f.write(model.equations_as_str())

            summary.append((label, error, status))

            print(f"{label} NMSE: {error}")

    with open("results/tables/summary.csv", "w") as f:
        f.write("system_dataset,nmse,status\n")
        for s in summary:
            f.write(f"{s[0]},{s[1]},{s[2]}\n")


if __name__ == "__main__":
    main()