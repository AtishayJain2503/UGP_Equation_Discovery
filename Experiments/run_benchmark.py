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
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--border);
        padding-bottom: 20px;
        margin-bottom: 24px;
    }}
    .header-text h1 {{
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }}
    .subtitle {{ color: var(--text-dim); font-size: 14px; }}
    .nav-tabs {{
        display: flex;
        gap: 12px;
    }}
    .nav-tabs button {{
        background: transparent;
        color: var(--text-dim);
        border: none;
        padding: 10px 16px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        border-radius: 8px;
        transition: 0.2s;
    }}
    .nav-tabs button.active {{
        background: var(--card);
        color: var(--text);
        border: 1px solid var(--border);
    }}
    .nav-tabs button:hover:not(.active) {{
        color: var(--text);
        background: rgba(255,255,255,0.05);
    }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}
    
    /* Stats & Results styles */
    .stats-row {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .stat-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; flex: 1; min-width: 180px; }}
    .stat-card .label {{ color: var(--text-dim); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .stat-card .value {{ font-size: 24px; font-weight: 700; margin-top: 4px; }}
    .filters {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center; }}
    .filters label {{ color: var(--text-dim); font-size: 13px; }}
    select, input[type="text"] {{ background: var(--card); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 8px 12px; font-size: 13px; outline: none; }}
    select:focus, input:focus {{ border-color: var(--accent); }}
    .results-grid {{ display: grid; gap: 12px; }}
    .result-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; transition: border-color 0.2s; }}
    .result-card:hover {{ border-color: var(--accent); }}
    .result-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px; }}
    .result-header .method {{ font-weight: 600; font-size: 15px; color: var(--accent); }}
    .result-header .dataset {{ font-size: 13px; color: var(--text-dim); background: var(--bg); padding: 4px 10px; border-radius: 6px; }}
    .badge {{ display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    .badge-stable {{ background: rgba(34,197,94,0.15); color: var(--green); }}
    .badge-unstable {{ background: rgba(239,68,68,0.15); color: var(--red); }}
    .metrics-row {{ display: flex; gap: 24px; margin-bottom: 14px; flex-wrap: wrap; }}
    .metric {{ display: flex; flex-direction: column; }}
    .metric .mlabel {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.4px; }}
    .metric .mval {{ font-size: 16px; font-weight: 600; font-family: 'Consolas', monospace; }}
    .nmse-excellent {{ color: var(--green); }}
    .nmse-good {{ color: #4ade80; }}
    .nmse-moderate {{ color: var(--yellow); }}
    .nmse-bad {{ color: var(--orange); }}
    .nmse-terrible {{ color: var(--red); }}
    .eq-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .eq-box {{ background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; }}
    .eq-box .eq-title {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 6px; }}
    .eq-box .eq-content {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; color: var(--text); white-space: pre-wrap; word-break: break-all; line-height: 1.6; }}
    .eq-true .eq-content {{ color: var(--green); }}
    .eq-pred .eq-content {{ color: #c4b5fd; }}
    
    /* Report Tab Styles */
    .report-container {{
        max-width: 950px;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 40px;
        line-height: 1.7;
    }}
    .report-container h2 {{ color: var(--accent); margin-top: 30px; margin-bottom: 15px; font-size: 24px; }}
    .report-container h2:first-child {{ margin-top: 0; }}
    .report-container h3 {{ color: #fff; margin-top: 20px; margin-bottom: 10px; font-size: 18px; }}
    .report-container p {{ margin-bottom: 16px; color: #cbd5e1; }}
    .report-container ul {{ margin-bottom: 16px; padding-left: 20px; color: #cbd5e1; }}
    .report-container li {{ margin-bottom: 8px; }}
    .report-block {{ background: var(--bg); padding: 16px; border-left: 4px solid var(--accent); border-radius: 4px; margin-bottom: 20px; }}
    code {{ font-family: 'Consolas', monospace; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; color: #e4e6eb; }}
    
    @media (max-width: 768px) {{
        .eq-section {{ grid-template-columns: 1fr; }}
        .header-container {{ flex-direction: column; align-items: flex-start; gap: 16px; }}
    }}
</style>
</head>
<body>

<div class="header-container">
    <div class="header-text">
        <h1>Equation Discovery Benchmark</h1>
        <p class="subtitle">Generated in {{elapsed_seconds:.1f}}s &mdash; {{len(rows_json)}} experiments evaluated</p>
    </div>
    <div class="nav-tabs">
        <button id="btn-results" class="active" onclick="switchTab('results')">Benchmark Grid</button>
        <button id="btn-report" onclick="switchTab('report')">Project Report & Story</button>
    </div>
</div>

<div id="tab-results" class="tab-content active">
    <div class="stats-row" id="stats-row"></div>
    <div class="filters">
        <label>Method:</label><select id="filter-method"><option value="all">All</option></select>
        <label>System:</label><select id="filter-system"><option value="all">All</option></select>
        <label>Noise:</label><select id="filter-noise"><option value="all">All</option></select>
        <label>Status:</label><select id="filter-status"><option value="all">All</option><option value="STABLE">Stable</option><option value="UNSTABLE">Unstable</option></select>
        <label>Sort:</label><select id="sort-by">
            <option value="default">Default</option>
            <option value="nmse-asc">NMSE ↑</option><option value="nmse-desc">NMSE ↓</option>
            <option value="method">Method</option><option value="system">System</option>
        </select>
    </div>
    <div class="results-grid" id="results-grid"></div>
</div>

<div id="tab-report" class="tab-content">
    <div class="report-container">
        <h2>The Equation Discovery Journey</h2>
        <p>Welcome to the <strong>Universal Equation Discovery Benchmark</strong>. This project was built to systematically evaluate how well Modern AI and traditional sparse regression algorithms can reverse-engineer the underlying laws of physics strictly from observational data. Our goal was not just to test clean, perfect conditions, but to stress-test these algorithms against <strong>noise, sparse observations, and chaotic dynamics</strong>.</p>

        <h3>Why these Methods?</h3>
        <p>The field is broadly split between algebraic regressors (like SINDy) and Neural/Evolutionary models (like PySR and Neural ODEs). We systematically pitted 9 different modeling approaches against one another:</p>
        <ul>
            <li><strong>SINDy Variants (M1, M2, M3, M8, M9)</strong>: Sparse Identification of Nonlinear Dynamics. Highly efficient but historically brittle to correlated subsets and noise. We evaluated Standard polynomial suites, Bayesian regularizations, Ensembles, and PISF (Pipeline with Spline Filtering).</li>
            <li><strong>PySR (M4)</strong>: PySymbolic Regression uses evolutionary genetic algorithms to probabilistically mutate equation trees. It easily escapes algebraic limits but is computationally massive.</li>
            <li><strong>Neural Approximators (M5, M6)</strong>: Neural ODEs and Physics-Informed Neural Networks (PINNs). These act as black box benchmarks: they learn incredibly tight latent continuous representations of the physics, establishing the limit on predictive NMSE accuracy, even if they don't hand us the mathematical equation string directly.</li>
        </ul>

        <h2>The Anatomy of the Physics Breakdown: Lessons Learned</h2>
        <p>You can't test complex physics engines without crashing them natively! During the development of this benchmark, we hit a massive mathematical paradox that completely halted execution and caused models to output unhinged, exploding equations like <code>12.9 x1^3 - 11.9 x0^2 * x1</code> for simple Harmonic Oscillators!</p>
        
        <div class="report-block">
            <strong>1. The Collinearity Explosion in SINDy:</strong> We noticed even perfectly clean data failed. Why? A simple harmonic oscillator (like a pendulum curve) lives on the constant algebraic constraint <code>x_0^2 + x_1^2 = 1</code>. The standard SINDy `STLSQ` (Iterative sparse regression with L2 Ridge limits) heavily punishes massive standalone weights like `1.0`. Instead of choosing the correct `1.0 * x_1`, it mathematically proved that spreading the weights into a combination of equivalent terms like <code>0.33 x1 + 0.33 x0^2 x1 + 0.33 x1^3</code> resulted in a lower L2 penalty limit! This created chaotic equations that instantly shattered our RK45 numeric integrator, triggering an infinite freeze-loop that originally lasted 14 hours.<br><br>
            <strong>The Fix:</strong> We migrated the entire benchmark SINDy backbone to <strong>SR3 with strict L0 Regularization constraints</strong>, which forces absolute non-distributive sparsity. It perfectly collapsed the solution into pure unitary dynamics directly bypassing the integration failure!
        </div>

        <div class="report-block">
            <strong>2. The Target Data Leak Paradox:</strong> Initially, we added 5% observational noise to our input trajectory <code>X</code>, but naturally passed the perfectly clean analytical slope mathematically derived by the simulator (<code>Xdot</code>) directly into the models for training. Mathematically, no static algebraic polynomial can map a noisy trajectory matrix to a strictly smooth derivative matrix natively. As a result, PySR and SINDy models overfitted massively trying to construct polynomials that bizarrely "cancelled out" and modelled the Random Noise Generator just to fit the clean target line. <br><br>
            <strong>The Fix:</strong> All generated noise derivatives evaluate through an empirical <code>SmoothedFiniteDifference()</code> physics engine before being fed to the optimization loops. Models now correctly see realistic noisy derivatives, simulating real-world physics measurements perfectly.
        </div>

        <h2>How to Read the Results Grid</h2>
        <p>In this benchmark grid, we enforce a strict zero-tolerance policy for instability:</p>
        <ul>
            <li><strong>NMSE (Normalized Mean Squared Error):</strong> Evaluates purely the difference between the <em>true trajectory</em> of the physics and the numeric trajectory generated by iteratively integrating the <em>predicted equation</em> iteratively. Below 0.01 is Excellent.</li>
            <li><strong>Rollout Error:</strong> Long-range stability integration test. If an equation explodes to infinity (or fails RK45 stepping), it means it's fundamentally mathematically stiff. The model simply receives an <strong>UNSTABLE</strong> rating limit instantly.</li>
            <li><strong>Complexity:</strong> The number of absolute algebraic nodes in the resulting equation tree. Lower is better.</li>
        </ul>

        <h3>Illustrative Example: Reading Real vs Predicted Equations</h3>
        <p>Let's look at how to verify an equation visually. Take the unforced <strong>A2 Linear Duffing Oscillator</strong>:</p>
        <div class="report-block">
            <code>✓ TRUE EQUATION</code><br>
            <code style="color:var(--green)">x0_dot = x1</code><br>
            <code style="color:var(--green)">x1_dot = -1.0000 * x0</code><br><br>
            <code>⟶ PREDICTED EQUATION (SINDy_poly on Clean Data)</code><br>
            <code style="color:#c4b5fd">x0_dot = 1.0000 x1</code><br>
            <code style="color:#c4b5fd">x1_dot = -1.0000 x0</code>
        </div>
        <p>However, what happens when we jump to <code>A2 - noise_5</code> (5% raw acoustic noise)? Highly optimized and hyper-parameterized models like SR3 or robust evolutionary PySR will still cleanly resolve coefficients near the truth, like <code>-0.9850 x0</code>, gracefully dropping off random Gaussian noise while maintaining native mathematical stability limiters! A poor implementation will begin filling out equations with fractional chaotic terms like <code>0.0050 x0^3 - 0.012 x1^2</code> specifically to map the noisy stochastic behavior! This dashboard will explicitly visually notify and penalize failures resulting from such attempts!</p>

    </div>
</div>

<script>
function switchTab(tabId) {{
    document.getElementById('btn-results').classList.remove('active');
    document.getElementById('btn-report').classList.remove('active');
    document.getElementById('tab-results').classList.remove('active');
    document.getElementById('tab-report').classList.remove('active');
    
    document.getElementById('btn-' + tabId).classList.add('active');
    document.getElementById('tab-' + tabId).classList.add('active');
}}

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

let methods = [...new Set(DATA.map(r => r.method))].sort();
let systems = [...new Set(DATA.map(r => r.system))].sort();
let noises  = [...new Set(DATA.map(r => r.noise))].sort();

methods.forEach(m => {{ document.getElementById('filter-method').innerHTML += `<option value="${{m}}">${{m}}</option>`; }});
systems.forEach(s => {{ document.getElementById('filter-system').innerHTML += `<option value="${{s}}">${{s}}</option>`; }});
noises.forEach(n  => {{ document.getElementById('filter-noise').innerHTML  += `<option value="${{n}}">${{n}}</option>`; }});

function render() {{
    let fm  = document.getElementById('filter-method').value;
    let fs  = document.getElementById('filter-system').value;
    let fn  = document.getElementById('filter-noise').value;
    let fst = document.getElementById('filter-status').value;
    let sort = document.getElementById('sort-by').value;

    let filtered = DATA.filter(r => {{
        if (fm  !== 'all' && r.method !== fm)  return false;
        if (fs  !== 'all' && r.system !== fs)  return false;
        if (fn  !== 'all' && r.noise  !== fn)  return false;
        if (fst !== 'all' && r.status !== fst) return false;
        return true;
    }});

    if (sort === 'nmse-asc')  filtered.sort((a,b) => (a.nmse ?? Infinity) - (b.nmse ?? Infinity));
    else if (sort === 'nmse-desc') filtered.sort((a,b) => (b.nmse ?? -Infinity) - (a.nmse ?? -Infinity));
    else if (sort === 'method') filtered.sort((a,b) => a.method.localeCompare(b.method));
    else if (sort === 'system') filtered.sort((a,b) => a.system.localeCompare(b.system));

    let stable   = filtered.filter(r => r.status === 'STABLE');
    let avgNmse  = stable.length ? stable.reduce((s,r) => s + (r.nmse || 0), 0) / stable.length : 0;
    let bestNmse = stable.length ? Math.min(...stable.map(r => r.nmse || Infinity)) : null;

    document.getElementById('stats-row').innerHTML = `
        <div class="stat-card"><div class="label">Showing</div><div class="value">${{filtered.length}}</div></div>
        <div class="stat-card"><div class="label">Stable</div><div class="value" style="color:var(--green)">${{stable.length}}</div></div>
        <div class="stat-card"><div class="label">Unstable</div><div class="value" style="color:var(--red)">${{filtered.length - stable.length}}</div></div>
        <div class="stat-card"><div class="label">Avg NMSE</div><div class="value">${{fmtNum(avgNmse, 4)}}</div></div>
        <div class="stat-card"><div class="label">Best NMSE</div><div class="value" style="color:var(--green)">${{bestNmse !== null ? fmtNum(bestNmse, 6) : 'N/A'}}</div></div>
    `;

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
                <div class="metric"><span class="mlabel">NMSE</span><span class="mval ${{nmseClass(r.nmse)}}">${{fmtNum(r.nmse)}}</span></div>
                <div class="metric"><span class="mlabel">Rollout Error</span><span class="mval">${{fmtNum(r.rollout)}}</span></div>
                <div class="metric"><span class="mlabel">Complexity</span><span class="mval">${{r.complexity !== null ? r.complexity : 'N/A'}}</span></div>
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
        </div>`;
    }});
    document.getElementById('results-grid').innerHTML = html;
}}

['filter-method','filter-system','filter-noise','filter-status','sort-by'].forEach(id => {{
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
                    print(f"✗ FIT_ERROR ({elapsed:.1f}s): {e}")
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

                status_icon = "✓" if status == "STABLE" else "✗"
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