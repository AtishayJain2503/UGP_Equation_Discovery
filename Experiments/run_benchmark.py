import os
import json
import time
import threading
import numpy as np

from registry.methods import METHOD_REGISTRY
from registry.systems import SYSTEM_REGISTRY
from evaluation.metrics import normalized_mse
from evaluation.rollout import rollout_error
from evaluation.complexity import count_terms


DATA_DIR = "data"
RESULTS_DIR = "results"

# Per-method simulation timeouts (seconds)
METHOD_TIMEOUTS = {
    "M1_SINDy_poly":     30,
    "M2_SINDy_custom":   30,
    "M3_BayesianSINDy":  30,
    "M4_PySR":           600,
    "M5_NeuralODE":      120,
    "M6_PINN":           120,
    "M7_GrammarSymbolic":600,
    "M8_PISF":           30,
    "M9_EnsembleSINDy":  30,
}
DEFAULT_TIMEOUT = 60


def simulate_with_timeout(model, x0, t, timeout_sec):
    """Run model.simulate in a thread; return None if it exceeds timeout_sec."""
    import threading
    result = [None]
    exc = [None]

    def worker():
        try:
            result[0] = model.simulate(x0, t)
        except Exception as e:
            exc[0] = e

    th = threading.Thread(target=worker, daemon=True)
    th.start()
    th.join(timeout=timeout_sec)

    if th.is_alive():
        # Thread exceeded timeout.
        return None

    return result[0]


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


def generate_html_report(summary_rows, elapsed_seconds):
    """Generate a self-contained HTML dashboard from benchmark results."""
    from experiments.html_template import build_html

    rows_json = []
    for r in summary_rows:
        method, system, noise, nmse_val, rollout_val, complexity_val, status, true_eq, pred_eq = r
        rows_json.append({
            "method": method,
            "system": system,
            "noise": noise,
            "nmse": float(nmse_val) if np.isfinite(nmse_val) else None,
            "rollout": float(rollout_val) if np.isfinite(rollout_val) else None,
            "complexity": int(complexity_val) if not np.isnan(complexity_val) else None,
            "status": status,
            "true_eq": true_eq,
            "pred_eq": pred_eq,
        })

    data_json = json.dumps(rows_json, indent=2)
    n_results = len(rows_json)
    elapsed_fmt = f"{elapsed_seconds:.1f}s"

    return build_html(data_json, n_results, elapsed_fmt)


def run_benchmark():

    os.makedirs(RESULTS_DIR, exist_ok=True)

    summary_rows = []
    start_time = time.time()

    total_methods = len(METHOD_REGISTRY)

    # Write CSV header once up front
    csv_path = os.path.join(RESULTS_DIR, "benchmark_summary.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("method,system,noise,nmse,rollout_error,complexity,status,true_eq,pred_eq\n")

    for m_idx, (method_name, Method) in enumerate(METHOD_REGISTRY.items(), 1):

        print(f"\n=== [{m_idx}/{total_methods}] Running method: {method_name} ===")

        sim_timeout = METHOD_TIMEOUTS.get(method_name, DEFAULT_TIMEOUT)

        for system in sorted(os.listdir(DATA_DIR)):

            system_path = os.path.join(DATA_DIR, system)
            if not os.path.isdir(system_path):
                continue

            for file in sorted(os.listdir(system_path)):

                if not file.endswith(".npz"):
                    continue

                dataset_path = os.path.join(system_path, file)
                t, X, Xdot, system_id, dt, noise = load_dataset(dataset_path)

                system_id   = str(system_id)
                noise_label = file.replace('.npz', '')

                if system_id in SYSTEM_REGISTRY:
                    true_cfg = SYSTEM_REGISTRY[system_id]["class"]()
                    true_eq  = true_cfg.true_equation
                else:
                    true_eq = "Unknown"
                    
                import pysindy as ps
                if noise > 0:
                    # Provide an empirical derivative for methods that expect one. 
                    # DO NOT pass the perfectly clean analytic target if input is noisy!
                    diff = ps.SmoothedFiniteDifference()
                    Xdot = diff(X, t=t)

                if system_id == "D1":
                    t_feature = t.reshape(-1, 1)
                    X    = np.hstack([X,    t_feature])
                    Xdot = np.hstack([Xdot, np.ones((len(Xdot), 1))])

                print(f"  {method_name} on {system_id}/{noise_label} ... ", end="", flush=True)

                t0 = time.time()

                try:
                    model = Method()
                    model.fit(X, Xdot, t)
                except Exception as e:
                    elapsed = time.time() - t0
                    print(f"[ERROR] FIT_ERROR ({elapsed:.1f}s): {e}")
                    X_pred = None
                    model  = None
                else:
                    # Simulate with per-method timeout
                    X_pred = simulate_with_timeout(model, X[0], t, timeout_sec=sim_timeout)

                elapsed = time.time() - t0

                if X_pred is None or X_pred.shape[0] != len(t):
                    nmse       = np.inf
                    rollout    = np.inf
                    complexity = np.nan
                    status     = "UNSTABLE"
                else:
                    if system_id == "D1" and X_pred.shape[1] >= 3:
                        X_pred = X_pred[:, :2]
                        X_true = X[:, :2]
                    else:
                        X_true = X

                    nmse       = normalized_mse(X_true, X_pred)
                    rollout    = rollout_error(X_true, X_pred)
                    complexity = count_terms(model) if model else np.nan
                    status     = "STABLE"

                try:
                    predicted_eq = model.equations() if model else "Fit failed"
                except Exception as e:
                    predicted_eq = f"Error: {str(e)}"

                status_icon = "[PASS]" if status == "STABLE" else "[FAIL]"
                nmse_str    = f"{nmse:.4e}" if np.isfinite(nmse) else "DIVERGED"
                print(f"{status_icon} {nmse_str} ({elapsed:.1f}s)")

                row_data = [
                    method_name,
                    system_id,
                    noise_label,
                    nmse,
                    rollout,
                    complexity,
                    status,
                    true_eq.replace('\n', '; '),
                    predicted_eq.replace('\n', '; ')
                ]
                summary_rows.append(row_data)

                # Append to CSV immediately so data is never lost on crash
                with open(csv_path, "a", encoding="utf-8") as f:
                    safe_row = []
                    for x in row_data:
                        s = str(x)
                        if "," in s or '"' in s:
                            s = '"' + s.replace('"', '""') + '"'
                        safe_row.append(s)
                    f.write(",".join(safe_row) + "\n")

    total_elapsed = time.time() - start_time

    # Write final HTML dashboard
    html_path = os.path.join(RESULTS_DIR, "benchmark_report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(generate_html_report(summary_rows, total_elapsed))

    print(f"\n{'='*60}")
    print(f"Benchmark completed in {total_elapsed:.1f}s")
    print(f"  CSV:  {csv_path}")
    print(f"  HTML: {html_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    run_benchmark()