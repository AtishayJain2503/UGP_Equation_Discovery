import os
import json
import time
import numpy as np
import multiprocessing

from registry.methods import METHOD_REGISTRY
from registry.systems import SYSTEM_REGISTRY
from evaluation.metrics import normalized_mse
from evaluation.rollout import rollout_error
from evaluation.complexity import count_terms


DATA_DIR = "data"
RESULTS_DIR = "results"


def _sim_worker(model, x0, t, return_dict):
    try:
        res = model.simulate(x0, t)
        return_dict['res'] = res
    except Exception:
        return_dict['res'] = None

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

    # Prepare JSON data for the dashboard
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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Equation Discovery Benchmark Report</title>
<style>
    :root {{
        --bg: #0f1117;
        --card: #1a1d27;
        --border: #2a2d3a;
        --text: #e4e6eb;
        --text-dim: #8b8fa3;
        --accent: #6366f1;
        --green: #22c55e;
        --yellow: #eab308;
        --red: #ef4444;
        --orange: #f97316;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', -apple-system, sans-serif;
        background: var(--bg);
        color: var(--text);
        padding: 24px;
        line-height: 1.5;
    }}
    h1 {{
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .subtitle {{ color: var(--text-dim); margin-bottom: 24px; font-size: 14px; }}
    .stats-row {{
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
        flex-wrap: wrap;
    }}
    .stat-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px 20px;
        min-width: 180px;
        flex: 1;
    }}
    .stat-card .label {{ color: var(--text-dim); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .stat-card .value {{ font-size: 24px; font-weight: 700; margin-top: 4px; }}
    .filters {{
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        flex-wrap: wrap;
        align-items: center;
    }}
    .filters label {{ color: var(--text-dim); font-size: 13px; }}
    select, input[type="text"] {{
        background: var(--card);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        outline: none;
    }}
    select:focus, input:focus {{ border-color: var(--accent); }}
    .results-grid {{
        display: grid;
        gap: 12px;
    }}
    .result-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px 20px;
        transition: border-color 0.2s;
    }}
    .result-card:hover {{ border-color: var(--accent); }}
    .result-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 8px;
    }}
    .result-header .method {{
        font-weight: 600;
        font-size: 15px;
        color: var(--accent);
    }}
    .result-header .dataset {{
        font-size: 13px;
        color: var(--text-dim);
        background: var(--bg);
        padding: 4px 10px;
        border-radius: 6px;
    }}
    .badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .badge-stable {{ background: rgba(34,197,94,0.15); color: var(--green); }}
    .badge-unstable {{ background: rgba(239,68,68,0.15); color: var(--red); }}
    .metrics-row {{
        display: flex;
        gap: 24px;
        margin-bottom: 14px;
        flex-wrap: wrap;
    }}
    .metric {{
        display: flex;
        flex-direction: column;
    }}
    .metric .mlabel {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.4px; }}
    .metric .mval {{ font-size: 16px; font-weight: 600; font-family: 'Consolas', monospace; }}
    .nmse-excellent {{ color: var(--green); }}
    .nmse-good {{ color: #4ade80; }}
    .nmse-moderate {{ color: var(--yellow); }}
    .nmse-bad {{ color: var(--orange); }}
    .nmse-terrible {{ color: var(--red); }}
    .eq-section {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }}
    .eq-box {{
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px 14px;
    }}
    .eq-box .eq-title {{
        font-size: 11px;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 6px;
    }}
    .eq-box .eq-content {{
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
        color: var(--text);
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
    }}
    .eq-true .eq-content {{ color: var(--green); }}
    .eq-pred .eq-content {{ color: #c4b5fd; }}
    @media (max-width: 768px) {{
        .eq-section {{ grid-template-columns: 1fr; }}
        .stats-row {{ flex-direction: column; }}
    }}
    .sort-btn {{
        background: var(--card);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
    }}
    .sort-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
    .sort-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}
</style>
</head>
<body>

<h1>Equation Discovery Benchmark Report</h1>
<p class="subtitle">Generated in {elapsed_seconds:.1f}s &mdash; {len(rows_json)} experiments across {len(set(r['system'] for r in rows_json))} systems and {len(set(r['method'] for r in rows_json))} methods</p>

<div class="stats-row" id="stats-row"></div>

<div class="filters">
    <label>Method:</label>
    <select id="filter-method"><option value="all">All Methods</option></select>
    <label>System:</label>
    <select id="filter-system"><option value="all">All Systems</option></select>
    <label>Noise:</label>
    <select id="filter-noise"><option value="all">All Noise</option></select>
    <label>Status:</label>
    <select id="filter-status">
        <option value="all">All</option>
        <option value="STABLE">Stable only</option>
        <option value="UNSTABLE">Unstable only</option>
    </select>
    <label>Sort:</label>
    <select id="sort-by">
        <option value="default">Default order</option>
        <option value="nmse-asc">NMSE ↑ (best first)</option>
        <option value="nmse-desc">NMSE ↓ (worst first)</option>
        <option value="method">Method name</option>
        <option value="system">System name</option>
    </select>
</div>

<div class="results-grid" id="results-grid"></div>

<script>
const DATA = {data_json};

function nmseClass(v) {{
    if (v === null) return 'nmse-terrible';
    if (v < 0.01) return 'nmse-excellent';
    if (v < 0.1) return 'nmse-good';
    if (v < 1.0) return 'nmse-moderate';
    if (v < 10.0) return 'nmse-bad';
    return 'nmse-terrible';
}}

function fmtNum(v, digits) {{
    if (v === null) return '∞';
    if (v === 0) return '0';
    if (Math.abs(v) < 0.001 || Math.abs(v) > 99999) return v.toExponential(digits || 3);
    return v.toFixed(digits || 4);
}}

function formatEq(eq) {{
    return eq.replace(/; /g, '\\n');
}}

function extractSystem(sysNoise) {{
    return sysNoise.split('_')[0];
}}

function extractNoise(sysNoise) {{
    let parts = sysNoise.split('_');
    return parts.slice(1).join('_');
}}

// Populate filters
let methods = [...new Set(DATA.map(r => r.method))].sort();
let systems = [...new Set(DATA.map(r => r.system))].sort();
let noises = [...new Set(DATA.map(r => r.noise))].sort();

methods.forEach(m => {{
    document.getElementById('filter-method').innerHTML += `<option value="${{m}}">${{m}}</option>`;
}});
systems.forEach(s => {{
    document.getElementById('filter-system').innerHTML += `<option value="${{s}}">${{s}}</option>`;
}});
noises.forEach(n => {{
    document.getElementById('filter-noise').innerHTML += `<option value="${{n}}">${{n}}</option>`;
}});

function render() {{
    let fm = document.getElementById('filter-method').value;
    let fs = document.getElementById('filter-system').value;
    let fn = document.getElementById('filter-noise').value;
    let fst = document.getElementById('filter-status').value;
    let sort = document.getElementById('sort-by').value;

    let filtered = DATA.filter(r => {{
        if (fm !== 'all' && r.method !== fm) return false;
        if (fs !== 'all' && r.system !== fs) return false;
        if (fn !== 'all' && r.noise !== fn) return false;
        if (fst !== 'all' && r.status !== fst) return false;
        return true;
    }});

    if (sort === 'nmse-asc') filtered.sort((a, b) => (a.nmse ?? Infinity) - (b.nmse ?? Infinity));
    else if (sort === 'nmse-desc') filtered.sort((a, b) => (b.nmse ?? -Infinity) - (a.nmse ?? -Infinity));
    else if (sort === 'method') filtered.sort((a, b) => a.method.localeCompare(b.method));
    else if (sort === 'system') filtered.sort((a, b) => a.system.localeCompare(b.system));

    // Stats
    let stable = filtered.filter(r => r.status === 'STABLE');
    let avgNmse = stable.length ? stable.reduce((s, r) => s + (r.nmse || 0), 0) / stable.length : 0;
    let bestNmse = stable.length ? Math.min(...stable.map(r => r.nmse || Infinity)) : null;

    document.getElementById('stats-row').innerHTML = `
        <div class="stat-card"><div class="label">Showing</div><div class="value">${{filtered.length}}</div></div>
        <div class="stat-card"><div class="label">Stable</div><div class="value" style="color:var(--green)">${{stable.length}}</div></div>
        <div class="stat-card"><div class="label">Unstable</div><div class="value" style="color:var(--red)">${{filtered.length - stable.length}}</div></div>
        <div class="stat-card"><div class="label">Avg NMSE (stable)</div><div class="value">${{fmtNum(avgNmse, 4)}}</div></div>
        <div class="stat-card"><div class="label">Best NMSE</div><div class="value" style="color:var(--green)">${{bestNmse !== null ? fmtNum(bestNmse, 6) : 'N/A'}}</div></div>
    `;

    // Cards
    let html = '';
    filtered.forEach(r => {{
        let badgeClass = r.status === 'STABLE' ? 'badge-stable' : 'badge-unstable';
        html += `
        <div class="result-card">
            <div class="result-header">
                <span class="method">${{r.method}}</span>
                <span class="dataset">${{r.system}} &mdash; ${{r.noise}}</span>
                <span class="badge ${{badgeClass}}">${{r.status}}</span>
            </div>
            <div class="metrics-row">
                <div class="metric">
                    <span class="mlabel">NMSE</span>
                    <span class="mval ${{nmseClass(r.nmse)}}">${{fmtNum(r.nmse)}}</span>
                </div>
                <div class="metric">
                    <span class="mlabel">Rollout Error</span>
                    <span class="mval">${{fmtNum(r.rollout)}}</span>
                </div>
                <div class="metric">
                    <span class="mlabel">Complexity</span>
                    <span class="mval">${{r.complexity !== null ? r.complexity : 'N/A'}}</span>
                </div>
            </div>
            <div class="eq-section">
                <div class="eq-box eq-true">
                    <div class="eq-title">✓ True Equation</div>
                    <div class="eq-content">${{formatEq(r.true_eq)}}</div>
                </div>
                <div class="eq-box eq-pred">
                    <div class="eq-title">⟶ Predicted Equation</div>
                    <div class="eq-content">${{formatEq(r.pred_eq)}}</div>
                </div>
            </div>
        </div>
        `;
    }});

    document.getElementById('results-grid').innerHTML = html;
}}

// Event listeners
['filter-method', 'filter-system', 'filter-noise', 'filter-status', 'sort-by'].forEach(id => {{
    document.getElementById(id).addEventListener('change', render);
}});

render();
</script>
</body>
</html>"""

    return html


def run_benchmark():

    os.makedirs(RESULTS_DIR, exist_ok=True)

    summary_rows = []
    start_time = time.time()

    total_methods = len(METHOD_REGISTRY)

    # ---- Setup CSV incrementally so we don't lose data on crashes
    csv_path = os.path.join(RESULTS_DIR, "benchmark_summary.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("method,system,noise,nmse,rollout_error,complexity,status,true_eq,pred_eq\n")

    # ---- iterate over methods
    for m_idx, (method_name, Method) in enumerate(METHOD_REGISTRY.items(), 1):

        print(f"\n=== [{m_idx}/{total_methods}] Running method: {method_name} ===")

        # ---- iterate over systems
        for system in sorted(os.listdir(DATA_DIR)):

            system_path = os.path.join(DATA_DIR, system)

            if not os.path.isdir(system_path):
                continue

            # ---- iterate over datasets
            for file in sorted(os.listdir(system_path)):

                if not file.endswith(".npz"):
                    continue
                dataset_path = os.path.join(system_path, file)

                t, X, Xdot, system_id, dt, noise = load_dataset(dataset_path)

                system_id = str(system_id)
                noise_label = file.replace('.npz', '')

                if system_id in SYSTEM_REGISTRY:
                    true_cfg = SYSTEM_REGISTRY[system_id]["class"]()
                    true_eq = true_cfg.true_equation
                else:
                    true_eq = "Unknown"

                if system_id == "D1":
                    t_feature = t.reshape(-1, 1)
                    X = np.hstack([X, t_feature])
                    Xdot = np.hstack([Xdot, np.ones((len(Xdot), 1))])

                print(f"  {method_name} on {system_id}/{noise_label} ... ", end="", flush=True)

                model = Method()

                t0 = time.time()

                # ---- train
                model.fit(X, Xdot, t)

                # ---- simulate learned dynamics (wrapped in timeout to prevent infinite freezes)
                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                p = multiprocessing.Process(target=_sim_worker, args=(model, X[0], t, return_dict))
                p.start()
                p.join(timeout=10) # 10 second strict time limit

                if p.is_alive():
                    # Terminate stuck process
                    p.terminate()
                    p.join()
                    X_pred = None
                else:
                    X_pred = return_dict.get('res', None)

                elapsed = time.time() - t0

                if X_pred is None or X_pred.shape[0] != len(t):
                    nmse = np.inf
                    rollout = np.inf
                    complexity = np.nan
                    status = "UNSTABLE"
                else:
                    if system_id == "D1" and X_pred.shape[1] >= 3:
                        X_pred = X_pred[:, :2]
                        X_true = X[:, :2]
                    else:
                        X_true = X

                    nmse = normalized_mse(X_true, X_pred)
                    rollout = rollout_error(X_true, X_pred)
                    complexity = count_terms(model)
                    status = "STABLE"

                try:
                    predicted_eq = model.equations()
                except Exception as e:
                    predicted_eq = f"Error: {str(e)}"

                status_icon = "✓" if status == "STABLE" else "✗"
                nmse_str = f"{nmse:.4e}" if np.isfinite(nmse) else "DIVERGED"
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

                # Write incrementally to CSV
                with open(csv_path, "a", encoding="utf-8") as f:
                    safe_row = []
                    for x in row_data:
                        s = str(x)
                        if "," in s or '"' in s:
                            s = '"' + s.replace('"', '""') + '"'
                        safe_row.append(s)
                    f.write(",".join(safe_row) + "\n")

    total_elapsed = time.time() - start_time

    # ---- save HTML dashboard (requires full memory)
    html_path = os.path.join(RESULTS_DIR, "benchmark_report.html")
    html_content = generate_html_report(summary_rows, total_elapsed)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n{'='*60}")
    print(f"Benchmark completed in {total_elapsed:.1f}s")
    print(f"  CSV:  {csv_path}")
    print(f"  HTML: {html_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    run_benchmark()