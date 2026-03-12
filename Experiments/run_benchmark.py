import os
import numpy as np

from registry.methods import METHOD_REGISTRY
from evaluation.metrics import normalized_mse
from evaluation.rollout import rollout_error
from evaluation.complexity import count_terms


DATA_DIR = "data"
RESULTS_DIR = "results"


def load_dataset(path):
    d = np.load(path, allow_pickle=True)

    return (
        d["t"],
        d["x"],
        d["xdot_true"],
        d["system"],
        d["dt"],
        d["noise_level"]
    )


def run_benchmark():

    os.makedirs(RESULTS_DIR, exist_ok=True)

    summary_rows = []

    # ---- iterate over methods
    for method_name, Method in METHOD_REGISTRY.items():

        print(f"\n=== Running method: {method_name} ===")

        # ---- iterate over systems
        for system in os.listdir(DATA_DIR):

            system_path = os.path.join(DATA_DIR, system)

            if not os.path.isdir(system_path):
                continue

            # ---- iterate over datasets
            for file in os.listdir(system_path):

                if not file.endswith(".npz"):
                    continue
                dataset_path = os.path.join(system_path, file)

                t, X, Xdot, system_id, dt, noise = load_dataset(dataset_path)
                if system_id == "D1":

                    t_feature = t.reshape(-1, 1)

                    X = np.hstack([X, t_feature])

                label = f"{system_id}_{file.replace('.npz','')}"

                print(f"Running {method_name} on {label}")

                model = Method()

                # ---- train
                model.fit(X, Xdot, t)

                # ---- simulate learned dynamics
                X_pred = model.simulate(X[0], t)

                if X_pred is None:
                    nmse = np.inf
                    rollout = np.inf
                    complexity = np.nan
                    status = "UNSTABLE"

                else:
                    nmse = normalized_mse(X, X_pred)
                    rollout = rollout_error(X, X_pred)
                    complexity = count_terms(model)
                    status = "STABLE"

                summary_rows.append([
                    method_name,
                    system_id,
                    noise,
                    nmse,
                    rollout,
                    complexity,
                    status
                ])

    # ---- save results table
    results_path = os.path.join(RESULTS_DIR, "benchmark_summary.csv")

    with open(results_path, "w") as f:

        f.write("method,system,noise,nmse,rollout_error,complexity,status\n")

        for r in summary_rows:
            f.write(",".join(map(str, r)) + "\n")

    print("\nBenchmark completed")
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    run_benchmark()