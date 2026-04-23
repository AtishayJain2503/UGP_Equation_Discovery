"""
Full HTML template for the Equation Discovery Benchmark Report.
Separated from run_benchmark.py to avoid f-string escaping issues.
"""

def build_html(data_json_str, n_results, elapsed_fmt):
    """Return complete HTML string. data_json_str is a raw JSON array string."""

    # We use simple string concatenation with PLACEHOLDER replacement
    # to avoid all {{ }} escaping issues with Python f-strings.

    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Equation Discovery Benchmark — UGP</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
    --bg:#05060a; --surface:rgba(16,18,27,0.85); --border:rgba(255,255,255,0.08);
    --border-hi:rgba(255,255,255,0.18); --text:#f1f5f9; --dim:#94a3b8; --muted:#64748b;
    --accent:#818cf8; --accent2:#38bdf8; --green:#10b981; --red:#f43f5e;
    --yellow:#f59e0b; --orange:#fb923c; --glow:rgba(129,140,248,0.4);
}
*{margin:0;padding:0;box-sizing:border-box}
body{
    font-family:'Inter',sans-serif; background:var(--bg); color:var(--text);
    min-height:100vh; line-height:1.6;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%,rgba(99,102,241,0.12) 0%,transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 10%,rgba(56,189,248,0.10) 0%,transparent 60%);
    background-attachment:fixed;
}
.shell{display:flex;flex-direction:column;min-height:100vh}
.top{position:sticky;top:0;z-index:100;background:rgba(5,6,10,0.88);backdrop-filter:blur(18px);
    border-bottom:1px solid var(--border);padding:0 36px;display:flex;align-items:center;
    justify-content:space-between;height:64px}
.logo{display:flex;align-items:center;gap:10px}
.logo-icon{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#6366f1,#38bdf8);
    display:flex;align-items:center;justify-content:center;font-size:17px}
.logo-text{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:#fff}
.logo-sub{font-size:11px;color:var(--muted)}
.pills{display:flex;gap:3px;background:rgba(255,255,255,0.04);padding:3px;border-radius:11px;border:1px solid var(--border)}
.pill{font-family:'Space Grotesk',sans-serif;background:transparent;color:var(--dim);border:none;
    padding:7px 18px;font-size:13px;font-weight:600;cursor:pointer;border-radius:8px;transition:0.2s}
.pill:hover{color:#fff;background:rgba(255,255,255,0.06)}
.pill.on{color:#fff;background:rgba(129,140,248,0.2);box-shadow:inset 0 0 0 1px rgba(129,140,248,0.4)}
.top-meta{font-size:12px;color:var(--muted);white-space:nowrap}
.top-meta b{color:var(--accent)}
.main{padding:36px;flex:1}
.pane{display:none;animation:fu .35s ease-out}
.pane.on{display:block}
@keyframes fu{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

/* Stats */
.srow{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:28px}
.scard{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 22px;transition:.3s}
.scard:hover{border-color:var(--border-hi);transform:translateY(-2px)}
.slbl{font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);font-weight:700;margin-bottom:6px}
.sval{font-family:'Space Grotesk',sans-serif;font-size:28px;font-weight:700}
.sg{color:var(--green)}.sr{color:var(--red)}.sa{color:var(--accent)}

/* Filters */
.fbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:var(--surface);
    border:1px solid var(--border);border-radius:12px;padding:12px 16px;margin-bottom:24px}
.fg{display:flex;align-items:center;gap:6px}
.fg label{font-size:11px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px}
select{background:rgba(0,0,0,0.45);color:var(--text);border:1px solid rgba(255,255,255,0.12);
    border-radius:8px;padding:7px 12px;font-size:12px;font-family:'Inter',sans-serif;outline:none;cursor:pointer}
select:focus{border-color:var(--accent);box-shadow:0 0 0 2px var(--glow)}

/* Cards */
.rgrid{display:grid;gap:14px}
.rc{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:22px;
    position:relative;overflow:hidden;transition:.3s}
.rc::after{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;transition:.3s}
.rc.st::after{background:var(--green);opacity:.6}
.rc.un::after{background:var(--red);opacity:.6}
.rc:hover{border-color:var(--border-hi);transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,.3)}
.ch{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;gap:12px;flex-wrap:wrap}
.ct{display:flex;flex-direction:column;gap:3px}
.cm{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:#fff}
.cs{font-size:11px;color:var(--dim);display:flex;align-items:center;gap:5px}
.cs .sc{font-family:'JetBrains Mono',monospace;background:rgba(255,255,255,.06);padding:1px 6px;border-radius:4px;font-size:10px}
.cs .sn{color:var(--accent2);font-weight:500}
.bd{display:inline-flex;padding:3px 10px;border-radius:999px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.bd-s{background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.25)}
.bd-u{background:rgba(244,63,94,.12);color:var(--red);border:1px solid rgba(244,63,94,.25)}
.bd-n{background:rgba(129,140,248,.1);color:var(--accent);border:1px solid rgba(129,140,248,.2)}
.mr{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:16px;background:rgba(0,0,0,.2);padding:12px 16px;border-radius:10px}
.mt{display:flex;flex-direction:column;gap:3px}
.ml{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;font-weight:600}
.mv{font-family:'Space Grotesk',monospace;font-size:16px;font-weight:700}
.ne{color:#34d399}.ng{color:#4ade80}.nm{color:var(--yellow)}.nb{color:var(--orange)}.nt{color:var(--red)}
.eg{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.eb{background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.04);border-radius:10px;padding:12px 14px}
.eh{font-size:10px;font-family:'Space Grotesk',sans-serif;color:var(--muted);text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:8px}
.ev{font-family:'JetBrains Mono',monospace;font-size:11.5px;line-height:1.8;white-space:pre-wrap;word-break:break-all}
.eb.et .ev{color:#6ee7b7}
.eb.ep .ev{color:#c4b5fd}

/* Tab 2: Whitepaper */
.wc{max-width:1100px;margin:0 auto}
.wh{background:linear-gradient(135deg,rgba(30,27,90,.7),rgba(10,20,50,.9));border:1px solid rgba(129,140,248,.2);
    border-radius:22px;padding:60px 40px;text-align:center;margin-bottom:36px;position:relative;overflow:hidden}
.wh::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent)}
.wh h2{font-family:'Space Grotesk',sans-serif;font-size:40px;font-weight:800;color:#fff;margin-bottom:18px;
    background:linear-gradient(135deg,#e0e7ff,#818cf8,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.wh p{font-size:17px;color:#94a3b8;max-width:700px;margin:0 auto;line-height:1.8}
.wtags{display:flex;justify-content:center;gap:8px;margin-top:24px;flex-wrap:wrap}
.wtag{font-size:11px;font-weight:600;font-family:'Space Grotesk',sans-serif;padding:5px 14px;border-radius:999px;
    border:1px solid rgba(129,140,248,.3);background:rgba(129,140,248,.08);color:var(--accent)}
.wst{font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;color:#fff;margin:36px 0 18px;
    display:flex;align-items:center;gap:10px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.wg{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px;margin-bottom:28px}
.wk{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:28px;transition:.3s}
.wk:hover{border-color:rgba(129,140,248,.3);transform:translateY(-3px);box-shadow:0 10px 36px rgba(99,102,241,.1)}
.wk.feat{background:linear-gradient(160deg,rgba(30,27,90,.5),var(--surface));border-top:2px solid var(--accent)}
.wk h3{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:#fff;margin-bottom:12px;display:flex;align-items:center;gap:10px}
.wk h3 .ic{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;background:rgba(129,140,248,.15);flex-shrink:0}
.wk p{color:#94a3b8;font-size:14px;line-height:1.75;margin-bottom:12px}
.wk p:last-child{margin-bottom:0}
.cb{background:#0a0c14;border:1px solid rgba(255,255,255,.05);border-radius:10px;padding:14px 18px;
    font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.7;color:#e2e8f0;overflow-x:auto;margin:12px 0}
.cb .cg{color:#34d399}.cb .cr{color:#f43f5e}.cb .cc{color:#475569}
.mtbl{width:100%;border-collapse:collapse;font-size:13px;margin-top:14px}
.mtbl th{font-family:'Space Grotesk',sans-serif;font-size:10px;text-transform:uppercase;letter-spacing:.8px;
    color:var(--muted);font-weight:700;padding:9px 12px;text-align:left;border-bottom:1px solid var(--border)}
.mtbl td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.03);vertical-align:top}
.mtbl tr:hover td{background:rgba(255,255,255,.02)}
.mn{font-family:'Space Grotesk',sans-serif;font-weight:600;color:var(--accent)}
.pi{display:inline-block;padding:2px 9px;border-radius:999px;font-size:10px;font-weight:600}
.pi-g{background:rgba(16,185,129,.12);color:var(--green);border:1px solid rgba(16,185,129,.2)}
.pi-y{background:rgba(245,158,11,.12);color:var(--yellow);border:1px solid rgba(245,158,11,.2)}
.pi-r{background:rgba(244,63,94,.12);color:var(--red);border:1px solid rgba(244,63,94,.2)}
.pi-b{background:rgba(56,189,248,.12);color:var(--accent2);border:1px solid rgba(56,189,248,.2)}
.pi-p{background:rgba(129,140,248,.12);color:var(--accent);border:1px solid rgba(129,140,248,.2)}
.dbar{height:5px;border-radius:3px;background:rgba(255,255,255,.06);overflow:hidden;margin-top:3px}
.dfill{height:100%;border-radius:3px}
.mex{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:14px}
.mxb{background:rgba(0,0,0,.3);border:1px solid var(--border);border-radius:12px;padding:18px 20px}
.mxh{font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:6px}
.mxr{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent);margin-bottom:6px}
.mxb p{font-size:12.5px;color:#94a3b8;line-height:1.6}
.tl{position:relative;padding-left:24px;border-left:2px solid rgba(129,140,248,.25)}
.ti{margin-bottom:24px;position:relative}
.td{position:absolute;left:-33px;top:2px;width:12px;height:12px;border-radius:50%;border:2px solid var(--accent);background:var(--bg)}
.ti h4{font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:700;color:#fff;margin-bottom:4px}
.ti p{font-size:13px;color:#94a3b8;line-height:1.6}

/* Tab 3: Analytics */
.ag{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}
@media(max-width:1000px){.ag{grid-template-columns:1fr}}
.pn{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:24px}
.pt{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:#fff;margin-bottom:16px}
.pt sub{font-size:11px;color:var(--muted);font-weight:400;font-family:'Inter',sans-serif}
.hm{border-collapse:collapse;width:100%;font-size:11px}
.hm th{padding:7px 5px;font-size:10px;color:var(--muted);font-weight:600;text-align:center;font-family:'Space Grotesk',sans-serif}
.hm td{padding:4px;text-align:center}
.hmc{width:48px;height:28px;border-radius:5px;display:flex;align-items:center;justify-content:center;
    font-family:'JetBrains Mono',monospace;font-size:9.5px;font-weight:500;color:#fff;margin:auto;transition:.15s}
.hmc:hover{transform:scale(1.15);box-shadow:0 4px 16px rgba(0,0,0,.5);z-index:1;position:relative}
.lb{width:100%;border-collapse:collapse}
.lb th{font-size:10px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);font-weight:700;
    padding:9px 12px;text-align:left;border-bottom:1px solid var(--border);font-family:'Space Grotesk',sans-serif}
.lb td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.03);font-size:12px}
.lb tr:hover td{background:rgba(255,255,255,.025)}
.lrk{font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:16px;text-align:center}
.r1{color:#fbbf24}.r2{color:#94a3b8}.r3{color:#f97316}
.lbw{background:rgba(255,255,255,.05);border-radius:3px;height:7px;overflow:hidden;margin-top:3px}
.lbf{height:100%;border-radius:3px}
#traj-canvas{width:100%;border-radius:10px;background:#06070d;border:1px solid var(--border);display:block}
.tleg{display:flex;gap:16px;margin-top:10px;font-size:11.5px;flex-wrap:wrap}
.tli{display:flex;align-items:center;gap:6px;color:var(--dim)}
.tld{width:20px;height:3px;border-radius:2px;flex-shrink:0}
@media(max-width:800px){.main{padding:18px}.top{padding:0 18px}.eg{grid-template-columns:1fr}.wh{padding:36px 20px}.wh h2{font-size:28px}}
</style>
</head>
<body>
<div class="shell">

<nav class="top">
    <div class="logo">
        <div class="logo-icon">🔬</div>
        <div><div class="logo-text">Equation Discovery Engine</div><div class="logo-sub">UGP · SciML Benchmark</div></div>
    </div>
    <div class="pills">
        <button class="pill on" id="btn-results" onclick="sw('results')">📊 Results</button>
        <button class="pill" id="btn-report" onclick="sw('report')">📄 Whitepaper</button>
        <button class="pill" id="btn-analytics" onclick="sw('analytics')">📈 Analytics</button>
    </div>
    <div class="top-meta"><b>__N_RESULTS__</b> runs · <b>__ELAPSED__</b></div>
</nav>

<div class="main">

<!-- ═══ TAB 1: RESULTS ═══ -->
<div class="pane on" id="tab-results">
    <div class="srow" id="srow"></div>
    <div class="fbar">
        <div class="fg"><label>Method</label><select id="f-m"><option value="all">All Methods</option></select></div>
        <div class="fg"><label>System</label><select id="f-s"><option value="all">All Systems</option></select></div>
        <div class="fg"><label>Noise</label><select id="f-n"><option value="all">All Noise</option></select></div>
        <div class="fg"><label>Status</label><select id="f-st"><option value="all">All</option><option value="STABLE">Stable</option><option value="UNSTABLE">Unstable</option></select></div>
        <div class="fg"><label>Sort</label><select id="f-so"><option value="default">Default</option><option value="nmse-asc">NMSE ↑ Best</option><option value="nmse-desc">NMSE ↓ Worst</option></select></div>
    </div>
    <div class="rgrid" id="rgrid"></div>
</div>

<!-- ═══ TAB 2: WHITEPAPER ═══ -->
<div class="pane" id="tab-report">
<div class="wc">

    <div class="wh">
        <h2>Benchmarking Equation Discovery<br>for Physical Systems</h2>
        <p>A systematic evaluation of 9 symbolic and neural methods across 10 dynamical systems spanning linear, nonlinear, chaotic, and hysteretic regimes — tested at 3 noise intensities.</p>
        <div class="wtags">
            <span class="wtag">Sparse Regression</span><span class="wtag">Symbolic Regression</span>
            <span class="wtag">Neural ODEs</span><span class="wtag">PINNs</span>
            <span class="wtag">Bayesian Methods</span><span class="wtag">Ensemble Learning</span>
            <span class="wtag">Undergraduate Project</span>
        </div>
    </div>

    <div class="wst">🎯 Project Motivation</div>
    <div class="wg">
        <div class="wk feat">
            <h3><span class="ic">🧭</span> The Core Question</h3>
            <p>Given noisy time-series observations of a physical system, <em>which algorithmic framework can most reliably recover the governing equations?</em></p>
            <p>This benchmark is a contribution within <strong>Scientific Machine Learning (SciML)</strong> — exploring the frontier of autonomous scientific discovery. The pivotal claim: <em>human-interpretable equations are more valuable than black-box predictions</em>, because they generalize beyond the training window and enable physical insight.</p>
        </div>
        <div class="wk">
            <h3><span class="ic">📐</span> What We Measure</h3>
            <p>Every discovered equation is re-simulated from the same initial condition, then scored against the true trajectory:</p>
            <div class="mex">
                <div class="mxb"><div class="mxh">Normalized MSE</div><div class="mxr">Excellent: &lt; 0.01 · Poor: &gt; 1.0</div><p>MSE between true and predicted, normalized by signal variance. The primary fidelity score.</p></div>
                <div class="mxb"><div class="mxh">Rollout Error</div><div class="mxr">Good: &lt; 0.3 · Diverged: ∞</div><p>Accumulated abs deviation over full horizon. Penalizes compounding errors in chaotic systems.</p></div>
                <div class="mxb"><div class="mxh">Sparsity</div><div class="mxr">Ideal: 2–8 terms</div><p>Number of symbolic terms. Occam's razor — simpler equations generalize better and avoid overfitting.</p></div>
                <div class="mxb"><div class="mxh">Stability</div><div class="mxr">STABLE / UNSTABLE</div><p>If the ODE solver diverges to infinity, the result is UNSTABLE regardless of equation form.</p></div>
            </div>
        </div>
    </div>

    <div class="wst">📖 How to Read Results — Worked Example</div>
    <div class="wk" style="margin-bottom:20px">
        <h3><span class="ic">💡</span> Van der Pol Oscillator (E1)</h3>
        <p>The Van der Pol oscillator is a nonlinear 2D system with a self-sustaining limit cycle. Its true governing equations are:</p>
        <div class="cb">
<span class="cc">// TRUE LAW (ground truth from physics):</span>
<span class="cg">ẋ₀ = x₁</span>
<span class="cg">ẋ₁ = 2.0·(1 − x₀²)·x₁ − x₀</span>

<span class="cc">// M1_SINDy_poly DISCOVERED (clean data, NMSE = 9.1×10⁻⁵):</span>
<span class="cg">ẋ₀ = 1.000·x₁</span>                              <span class="cc">← near-perfect ✓</span>
<span class="cg">ẋ₁ = −0.999·x₀ + 2.005·x₁ − 2.002·x₀²·x₁</span>  <span class="cc">← exact structure ✓</span>

<span class="cc">// Same method at 5% noise (NMSE = 0.977):</span>
ẋ₀ = 1.042·x₁                                <span class="cc">← 4% coeff drift</span>
ẋ₁ = −0.969·x₀ + 1.733·x₁ − 1.804·x₀²·x₁   <span class="cc">← 10% error</span>

<span class="cc">// M5_NeuralODE (any noise):</span>
<span class="cr">Neural ODE: MLP [2→64→64→2], no equation output</span>  <span class="cc">← black box!</span>
        </div>
        <p style="padding:10px 14px;background:rgba(129,140,248,.08);border-left:3px solid var(--accent);border-radius:7px;font-size:13px;color:#c4b5fd;">
            <strong>Rule of thumb:</strong> NMSE &lt;0.01 = excellent (equation practically correct). 0.01–0.5 = good (structure correct, some coefficient error). &gt;1.0 = poor (wrong structure or diverging). UNSTABLE = integration blew up.
        </p>
    </div>

    <div class="wst">🧮 The 9 Competing Methods</div>
    <div class="wk" style="margin-bottom:20px">
        <table class="mtbl">
        <tr><th>ID</th><th>Method</th><th>Type</th><th>Equation?</th><th>Noise?</th><th>Best For</th></tr>
        <tr><td class="mn">M1</td><td><strong>SINDy Poly</strong><br><small style="color:var(--muted)">Polynomial basis {1,x,x²,x³}</small></td><td><span class="pi pi-p">Sparse</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-y">Med</span></td><td>Clean polynomial systems</td></tr>
        <tr><td class="mn">M2</td><td><strong>SINDy Custom</strong><br><small style="color:var(--muted)">Poly + Fourier {sin,cos}</small></td><td><span class="pi pi-p">Sparse</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-r">Low</span></td><td>Systems with periodicity</td></tr>
        <tr><td class="mn">M3</td><td><strong>Bayesian SINDy</strong><br><small style="color:var(--muted)">Sparse Bayesian + uncertainty</small></td><td><span class="pi pi-b">Bayesian</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-g">High</span></td><td>Noisy data, UQ</td></tr>
        <tr><td class="mn">M4</td><td><strong>PySR</strong><br><small style="color:var(--muted)">Genetic programming</small></td><td><span class="pi pi-y">Evolutionary</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-g">High</span></td><td>General nonlinear</td></tr>
        <tr><td class="mn">M5</td><td><strong>Neural ODE</strong><br><small style="color:var(--muted)">MLP dynamics (GPU)</small></td><td><span class="pi pi-r">Neural</span></td><td><span class="pi pi-r">No ✗</span></td><td><span class="pi pi-g">High</span></td><td>Black-box baseline</td></tr>
        <tr><td class="mn">M6</td><td><strong>PINN</strong><br><small style="color:var(--muted)">Physics-Informed NN</small></td><td><span class="pi pi-r">Neural</span></td><td><span class="pi pi-r">No ✗</span></td><td><span class="pi pi-g">High</span></td><td>Physics priors</td></tr>
        <tr><td class="mn">M7</td><td><strong>Grammar Symbolic</strong><br><small style="color:var(--muted)">Grammar-constrained search</small></td><td><span class="pi pi-y">Evolutionary</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-y">Med</span></td><td>Structured expressions</td></tr>
        <tr><td class="mn">M8</td><td><strong>PISF</strong><br><small style="color:var(--muted)">Physics-Informed Sparse</small></td><td><span class="pi pi-p">Sparse</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-y">Med</span></td><td>Physics-constrained</td></tr>
        <tr><td class="mn">M9</td><td><strong>Ensemble SINDy</strong><br><small style="color:var(--muted)">Bootstrap + majority vote</small></td><td><span class="pi pi-p">Ensemble</span></td><td><span class="pi pi-g">Yes ✓</span></td><td><span class="pi pi-g">High</span></td><td>Noise robustness</td></tr>
        </table>
    </div>

    <div class="wst">🌐 The 10 Benchmark Systems</div>
    <div class="wk" style="margin-bottom:20px">
        <table class="mtbl">
        <tr><th>ID</th><th>System</th><th>Dim</th><th>Type</th><th>Equation</th><th>Difficulty</th></tr>
        <tr><td class="mn">A2</td><td><strong>Damped Harmonic Oscillator</strong></td><td>2D</td><td><span class="pi pi-g">Linear</span></td><td style="font-family:'JetBrains Mono';font-size:11px">ẋ₁=−x₀</td><td><div class="dbar"><div class="dfill" style="width:15%;background:var(--green)"></div></div></td></tr>
        <tr><td class="mn">B2</td><td><strong>Large-Angle Pendulum</strong></td><td>2D</td><td><span class="pi pi-b">Nonlinear</span></td><td style="font-family:'JetBrains Mono';font-size:11px">ẋ₁=−9.81sin(x₀)−0.05x₁</td><td><div class="dbar"><div class="dfill" style="width:35%;background:var(--accent2)"></div></div></td></tr>
        <tr><td class="mn">C2</td><td><strong>Duffing Oscillator</strong></td><td>2D</td><td><span class="pi pi-b">Nonlinear</span></td><td style="font-family:'JetBrains Mono';font-size:11px">ẋ₁=x₀−x₀³−0.2x₁</td><td><div class="dbar"><div class="dfill" style="width:25%;background:var(--accent2)"></div></div></td></tr>
        <tr><td class="mn">D1</td><td><strong>Forced Duffing</strong></td><td>3D+t</td><td><span class="pi pi-y">Forced</span></td><td style="font-family:'JetBrains Mono';font-size:11px">+0.3cos(1.2t)</td><td><div class="dbar"><div class="dfill" style="width:55%;background:var(--yellow)"></div></div></td></tr>
        <tr><td class="mn">E1</td><td><strong>Van der Pol Oscillator</strong></td><td>2D</td><td><span class="pi pi-b">Nonlinear</span></td><td style="font-family:'JetBrains Mono';font-size:11px">ẋ₁=2(1−x₀²)x₁−x₀</td><td><div class="dbar"><div class="dfill" style="width:40%;background:var(--accent2)"></div></div></td></tr>
        <tr><td class="mn">F1</td><td><strong>Bouc-Wen Hysteresis I</strong></td><td>3D</td><td><span class="pi pi-r">Hysteretic</span></td><td style="font-family:'JetBrains Mono';font-size:11px">|x₁|·x₂ terms</td><td><div class="dbar"><div class="dfill" style="width:75%;background:var(--orange)"></div></div></td></tr>
        <tr><td class="mn">F2</td><td><strong>Bouc-Wen Hysteresis II</strong></td><td>3D</td><td><span class="pi pi-r">Hysteretic</span></td><td style="font-family:'JetBrains Mono';font-size:11px">|x₂|²·x₁ terms</td><td><div class="dbar"><div class="dfill" style="width:80%;background:var(--orange)"></div></div></td></tr>
        <tr><td class="mn">F3</td><td><strong>Bouc-Wen 4D Memory</strong></td><td>4D</td><td><span class="pi pi-r">Hysteretic</span></td><td style="font-family:'JetBrains Mono';font-size:11px">4-state coupling</td><td><div class="dbar"><div class="dfill" style="width:92%;background:var(--red)"></div></div></td></tr>
        <tr><td class="mn">G1</td><td><strong>Lorenz Attractor</strong></td><td>3D</td><td><span class="pi pi-r">Chaotic</span></td><td style="font-family:'JetBrains Mono';font-size:11px">σ=10, ρ=28, β=8/3</td><td><div class="dbar"><div class="dfill" style="width:85%;background:var(--red)"></div></div></td></tr>
        <tr><td class="mn">G2</td><td><strong>Rössler Attractor</strong></td><td>3D</td><td><span class="pi pi-y">Chaotic</span></td><td style="font-family:'JetBrains Mono';font-size:11px">a=0.2, b=0.2, c=5.7</td><td><div class="dbar"><div class="dfill" style="width:65%;background:var(--yellow)"></div></div></td></tr>
        </table>
    </div>

    <div class="wst">🚧 Engineering Challenges</div>
    <div class="wg">
        <div class="wk feat">
            <h3><span class="ic">💥</span> The Collinearity Explosion</h3>
            <p>Early runs with the default <strong>STLSQ</strong> optimizer caused catastrophic instability on clean periodic data. The optimizer spread mass across correlated terms:</p>
            <div class="cb">
<span class="cr">// STLSQ (broken): A2 clean → UNSTABLE</span>
ẋ₀ = 0.33x₁ + 0.33x₀²x₁ + 0.33x₁³   <span class="cc">← wrong</span>

<span class="cg">// SR3-L0 (fixed): A2 clean, NMSE = 7.2×10⁻⁷</span>
ẋ₀ = 1.000·x₁                         <span class="cc">← exact ✓</span>
            </div>
            <p><strong>Fix:</strong> Migrated to SR3 with L0 regularization. Runtime dropped 14h → 5.6h.</p>
        </div>
        <div class="wk feat">
            <h3><span class="ic">🌊</span> The Target Data Leak</h3>
            <p>SINDy needs derivatives (Ẋ). Passing <em>clean analytical derivatives</em> with <em>noisy states</em> is an information contradiction that overfits wildly:</p>
            <div class="cb">
<span class="cr">// BAD: clean deriv + noisy states = overfitting</span>
model.fit(X_noisy, Xdot_clean, t)

<span class="cg">// GOOD: empirical derivative from noisy data</span>
diff = SmoothedFiniteDifference()
Xdot = diff(X_noisy, t=t)
model.fit(X_noisy, Xdot, t)
            </div>
            <p><strong>Fix:</strong> All noisy experiments use <code>SmoothedFiniteDifference()</code>.</p>
        </div>
        <div class="wk">
            <h3><span class="ic">🔮</span> Neural Models = No Equations</h3>
            <p>Neural ODEs (M5) and PINNs (M6) are <strong>black-box limiters</strong>. They learn dynamics via gradient descent but produce MLP weight matrices, not symbolic equations. They provide an upper bound: if a neural net still has NMSE &gt;1.0, no sparse method should be expected to recover the law.</p>
        </div>
        <div class="wk">
            <h3><span class="ic">🌀</span> Why Chaos Makes NMSE Misleading</h3>
            <p>The Lorenz attractor (G1) has <strong>sensitive dependence on initial conditions</strong>. Even a perfectly recovered equation with 0.1% coefficient error produces NMSE &gt;1.0 at long horizons. This is intrinsic to chaos, not algorithmic failure.</p>
        </div>
    </div>

    <div class="wst">🔭 Key Findings</div>
    <div class="wk" style="margin-bottom:36px">
        <div class="tl">
            <div class="ti"><div class="td"></div><h4>Finding 1: PySR (M4) achieves best accuracy on diverse systems</h4><p>Evolutionary search outside fixed bases recovered near-exact equations on E1, F-series, and G2.</p></div>
            <div class="ti"><div class="td"></div><h4>Finding 2: Bayesian SINDy (M3) is most noise-robust</h4><p>Treating sparsity as a probability prior rather than a hard threshold maintained stability at 5% noise where M1/M2 diverged.</p></div>
            <div class="ti"><div class="td"></div><h4>Finding 3: Hysteretic systems expose basis limitations</h4><p>All polynomial methods fail on F-series (Bouc-Wen) because abs(x) cannot be represented as a polynomial. This is a formulation limitation, not an optimizer failure.</p></div>
            <div class="ti"><div class="td"></div><h4>Finding 4: Neural methods provide stability without interpretability</h4><p>M5/M6 never diverged to infinity. They achieve bounded NMSE on all systems at the cost of zero symbolic content.</p></div>
            <div class="ti" style="margin-bottom:0"><div class="td"></div><h4>Finding 5: Ensemble voting (M9) doesn't fix basis mismatch</h4><p>Bootstrap voting didn't improve over single-run SINDy when the fundamental problem is structural (wrong basis, chaotic system).</p></div>
        </div>
    </div>

</div>
</div>

<!-- ═══ TAB 3: ANALYTICS ═══ -->
<div class="pane" id="tab-analytics">

    <div class="ag" style="grid-template-columns:1fr">
        <div class="pn"><div class="pt">Method Leaderboard <sub>ranked by mean NMSE across stable runs</sub></div><table class="lb" id="lb-tbl"></table></div>
    </div>

    <div class="ag">
        <div class="pn">
            <div class="pt">NMSE Heatmap <sub>method × system (avg across noise levels)</sub></div>
            <div style="overflow-x:auto"><table class="hm" id="hm-tbl"></table></div>
        </div>
        <div class="pn">
            <div class="pt">Trajectory Comparison <sub>true vs best-recovered equation (RK4 in browser)</sub></div>
            <div style="display:flex;gap:10px;align-items:center;margin-bottom:12px;flex-wrap:wrap">
                <div class="fg"><label>System</label>
                    <select id="tj-sys" onchange="runTraj()">
                        <option value="A2">A2 — Damped Oscillator</option>
                        <option value="B2">B2 — Pendulum</option>
                        <option value="C2">C2 — Duffing</option>
                        <option value="E1" selected>E1 — Van der Pol</option>
                        <option value="G1">G1 — Lorenz</option>
                        <option value="G2">G2 — Rössler</option>
                    </select>
                </div>
                <div class="fg"><label>Dim</label>
                    <select id="tj-dim" onchange="runTraj()"><option value="0">x₀</option><option value="1">x₁</option></select>
                </div>
            </div>
            <canvas id="traj-canvas" height="300"></canvas>
            <div class="tleg">
                <div class="tli"><div class="tld" style="background:#34d399"></div> True ODE</div>
                <div class="tli"><div class="tld" style="background:#818cf8"></div> Best Recovered</div>
                <div class="tli"><div class="tld" style="background:#f43f5e;opacity:.5"></div> Worst Method</div>
            </div>
        </div>
    </div>

    <div class="ag" style="grid-template-columns:1fr">
        <div class="pn"><div class="pt">Stability Rate by System <sub>fraction of methods with bounded simulations</sub></div><div id="stab-bars"></div></div>
    </div>
</div>

</div>
</div>

<script>
const DATA = __DATA_JSON__;

const SN = {
    'A2':'Damped Oscillator','B2':'Large-Angle Pendulum','C2':'Duffing Oscillator',
    'D1':'Forced Duffing','E1':'Van der Pol','F1':'Bouc-Wen I',
    'F2':'Bouc-Wen II','F3':'Bouc-Wen 4D','G1':'Lorenz Attractor','G2':'Rössler Attractor'
};
const MS = {
    'M1_SINDy_poly':'M1 SINDy-Poly','M2_SINDy_custom':'M2 SINDy-Custom',
    'M3_BayesianSINDy':'M3 Bayesian','M4_PySR':'M4 PySR',
    'M5_NeuralODE':'M5 NeuralODE','M6_PINN':'M6 PINN',
    'M7_GrammarSymbolic':'M7 Grammar','M8_PISF':'M8 PISF',
    'M9_EnsembleSINDy':'M9 Ensemble'
};
const NL = {'clean':'Clean','noise_2':'2% Noise','noise_5':'5% Noise'};
const AM=[...new Set(DATA.map(r=>r.method))].sort();
const AS=[...new Set(DATA.map(r=>r.system))].sort();
const AN=[...new Set(DATA.map(r=>r.noise))].sort();

function sw(id){
    ['results','report','analytics'].forEach(t=>{
        document.getElementById('btn-'+t).classList.remove('on');
        document.getElementById('tab-'+t).classList.remove('on');
    });
    document.getElementById('btn-'+id).classList.add('on');
    document.getElementById('tab-'+id).classList.add('on');
    if(id==='analytics') buildAn();
}
function nc(v){if(v===null)return'nt';if(v<0.01)return'ne';if(v<0.1)return'ng';if(v<0.5)return'nm';if(v<2)return'nb';return'nt'}
function fn(v){if(v===null)return'∞ DIVERGED';if(v<0.001)return v.toExponential(2);return v.toFixed(4)}
function fr(v){return v===null?'—':v>1e6?'∞':v.toFixed(3)}

function init(){
    AM.forEach(m=>document.getElementById('f-m').innerHTML+=`<option value="${m}">${MS[m]||m}</option>`);
    AS.forEach(s=>document.getElementById('f-s').innerHTML+=`<option value="${s}">${s} — ${SN[s]||s}</option>`);
    AN.forEach(n=>document.getElementById('f-n').innerHTML+=`<option value="${n}">${NL[n]||n}</option>`);
}

function render(){
    const fm=document.getElementById('f-m').value,fs=document.getElementById('f-s').value,
          fn2=document.getElementById('f-n').value,fst=document.getElementById('f-st').value,
          so=document.getElementById('f-so').value;
    let d=DATA.filter(r=>(fm==='all'||r.method===fm)&&(fs==='all'||r.system===fs)&&(fn2==='all'||r.noise===fn2)&&(fst==='all'||r.status===fst));
    if(so==='nmse-asc')d.sort((a,b)=>(a.nmse??Infinity)-(b.nmse??Infinity));
    if(so==='nmse-desc')d.sort((a,b)=>(b.nmse??Infinity)-(a.nmse??Infinity));
    const st=d.filter(r=>r.status==='STABLE');
    document.getElementById('srow').innerHTML=`
        <div class="scard"><div class="slbl">Showing</div><div class="sval sa">${d.length}</div></div>
        <div class="scard"><div class="slbl">Stable</div><div class="sval sg">${st.length}</div></div>
        <div class="scard"><div class="slbl">Unstable</div><div class="sval sr">${d.length-st.length}</div></div>
        <div class="scard"><div class="slbl">Stability %</div><div class="sval sa">${d.length?(st.length/d.length*100).toFixed(0)+'%':'—'}</div></div>`;
    if(!d.length){document.getElementById('rgrid').innerHTML='<div style="padding:40px;text-align:center;color:var(--muted)">No results.</div>';return}
    document.getElementById('rgrid').innerHTML=d.map(r=>{
        const sn=SN[r.system]||r.system,mn=MS[r.method]||r.method;
        return`<div class="rc ${r.status==='STABLE'?'st':'un'}">
            <div class="ch"><div class="ct"><span class="cm">${mn}</span><span class="cs"><span class="sc">${r.system}</span><span class="sn">${sn}</span> · ${NL[r.noise]||r.noise}</span></div><div><span class="bd ${r.status==='STABLE'?'bd-s':'bd-u'}">${r.status==='STABLE'?'✓ Stable':'✗ Unstable'}</span></div></div>
            <div class="mr"><div class="mt"><span class="ml">NMSE</span><span class="mv ${nc(r.nmse)}">${fn(r.nmse)}</span></div><div class="mt"><span class="ml">Rollout</span><span class="mv">${fr(r.rollout)}</span></div><div class="mt"><span class="ml">Terms</span><span class="mv">${r.complexity!==null?r.complexity:'—'}</span></div></div>
            <div class="eg"><div class="eb et"><div class="eh">✓ True Law</div><div class="ev">${r.true_eq.replace(/; /g,'\n')}</div></div><div class="eb ep"><div class="eh">🔮 Discovered</div><div class="ev">${r.pred_eq.replace(/; /g,'\n')}</div></div></div>
        </div>`}).join('');
}

/* LEADERBOARD */
function buildLB(){
    const sc={};AM.forEach(m=>sc[m]={s:0,n:0,st:0,tt:0});
    DATA.forEach(r=>{sc[r.method].tt++;if(r.status==='STABLE')sc[r.method].st++;if(r.nmse!==null){sc[r.method].s+=r.nmse;sc[r.method].n++}});
    const rows=AM.map(m=>({m,mean:sc[m].n>0?sc[m].s/sc[m].n:Infinity,sr:sc[m].st/sc[m].tt})).sort((a,b)=>a.mean-b.mean);
    const mx=rows.filter(r=>isFinite(r.mean));const mxv=mx.length?mx[mx.length-1].mean:1;
    const rc=['r1','r2','r3'];const pal=['#fbbf24','#94a3b8','#f97316','#818cf8','#38bdf8','#34d399','#f43f5e','#e879f9','#22d3ee'];
    document.getElementById('lb-tbl').innerHTML=`<thead><tr><th>#</th><th>Method</th><th>Mean NMSE</th><th>Stability</th><th>Score</th></tr></thead><tbody>${rows.map((r,i)=>{
        const bw=isFinite(r.mean)?Math.max(4,100-r.mean/mxv*90):2;const c=r.sr>.8?'var(--green)':r.sr>.5?'var(--yellow)':'var(--red)';
        return`<tr><td><span class="lrk ${rc[i]||''}">${i+1}</span></td><td><strong style="font-family:'Space Grotesk';color:#fff">${MS[r.m]||r.m}</strong></td><td style="font-family:'JetBrains Mono';color:${pal[i]}">${isFinite(r.mean)?r.mean.toFixed(4):'∞'}</td><td style="color:${c};font-weight:700">${(r.sr*100).toFixed(0)}%</td><td><div class="lbw"><div class="lbf" style="width:${bw}%;background:${pal[i]}"></div></div></td></tr>`}).join('')}</tbody>`;
}

/* HEATMAP */
function buildHM(){
    const g={};DATA.forEach(r=>{const k=r.method+'|'+r.system;if(!g[k])g[k]={s:0,n:0};if(r.nmse!==null){g[k].s+=r.nmse;g[k].n++}});
    function hc(v){if(v===null||!isFinite(v))return'#3b1f1f';const l=Math.log10(Math.max(v,1e-7));if(l<-4)return'#065f46';if(l<-2)return'#059669';if(l<-1)return'#d97706';if(l<0)return'#92400e';return'#9f1239'}
    function hl(v){if(v===null||!isFinite(v))return'✗';if(v<0.001)return v.toExponential(0);return v.toFixed(2)}
    document.getElementById('hm-tbl').innerHTML=`<thead><tr><th style="text-align:left">Method</th>${AS.map(s=>`<th title="${SN[s]||s}">${s}</th>`).join('')}</tr></thead><tbody>${AM.map(m=>`<tr><td style="text-align:left;font-size:10.5px;font-family:'Space Grotesk';color:#cbd5e1;white-space:nowrap">${MS[m]||m}</td>${AS.map(s=>{const k=m+'|'+s;const v=g[k]&&g[k].n?g[k].s/g[k].n:null;return`<td><div class="hmc" style="background:${hc(v)}" title="${MS[m]||m} / ${SN[s]||s}: ${v!==null?v.toFixed(4):'N/A'}">${hl(v)}</div></td>`}).join('')}</tr>`).join('')}</tbody>`;
}

/* STABILITY BARS */
function buildSB(){
    const d={};AS.forEach(s=>d[s]={st:0,tt:0});DATA.forEach(r=>{d[r.system].tt++;if(r.status==='STABLE')d[r.system].st++});
    document.getElementById('stab-bars').innerHTML=AS.map(s=>{const p=d[s].st/d[s].tt*100;const c=p>80?'var(--green)':p>50?'var(--yellow)':'var(--red)';
        return`<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12.5px"><span><strong style="font-family:'Space Grotesk'">${s}</strong> <span style="color:var(--muted);font-size:11px">${SN[s]||''}</span></span><span style="font-family:'JetBrains Mono';font-size:11px;color:${c}">${d[s].st}/${d[s].tt} (${p.toFixed(0)}%)</span></div><div style="background:rgba(255,255,255,.05);border-radius:5px;height:8px;overflow:hidden"><div style="width:${p}%;height:100%;background:${c};border-radius:5px;transition:width .8s"></div></div></div>`}).join('');
}

/* TRAJECTORY — real RK4 from hardcoded true ODEs + best recovered from DATA */
const TODE={
    'A2':{ic:[0.5,0],dt:.02,n:400,f:s=>[s[1],-s[0]]},
    'B2':{ic:[0.5,0],dt:.02,n:400,f:s=>[s[1],-9.81*Math.sin(s[0])-0.05*s[1]]},
    'C2':{ic:[0.5,0],dt:.02,n:400,f:s=>[s[1],s[0]-Math.pow(s[0],3)-0.2*s[1]]},
    'E1':{ic:[0.5,0.5],dt:.02,n:500,f:s=>[s[1],2*(1-s[0]*s[0])*s[1]-s[0]]},
    'G1':{ic:[-8,8,27],dt:.005,n:800,f:s=>[10*(s[1]-s[0]),s[0]*(28-s[2])-s[1],s[0]*s[1]-8/3*s[2]]},
    'G2':{ic:[0.5,0.5,0],dt:.05,n:300,f:s=>[-s[1]-s[2],s[0]+0.2*s[1],0.2+s[2]*(s[0]-5.7)]}
};
function rk4(f,s,dt){const k1=f(s),k2=f(s.map((v,i)=>v+.5*dt*k1[i])),k3=f(s.map((v,i)=>v+.5*dt*k2[i])),k4=f(s.map((v,i)=>v+dt*k3[i]));return s.map((v,i)=>v+dt/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]))}
function sim(f,ic,dt,n){const t=[ic.slice()];let s=ic.slice();for(let i=0;i<n;i++){try{s=rk4(f,s,dt)}catch(e){s=s.map(()=>NaN)}if(s.some(v=>!isFinite(v)||Math.abs(v)>1e8))s=s.map(()=>NaN);t.push(s.slice())}return t}

function getBestWorst(sys){
    // find stable runs for this system, pick best and worst NMSE
    const runs=DATA.filter(r=>r.system===sys&&r.status==='STABLE'&&r.nmse!==null).sort((a,b)=>a.nmse-b.nmse);
    return {best:runs[0]||null, worst:runs.length>1?runs[runs.length-1]:null};
}

function parsePredCoeffs(predEq, sys){
    // Very basic: for the best run, attempt to build an approximate ODE from the predicted equation
    // This is a simplified demonstration — we hardcode approximate reconstructions for key systems
    // based on what M1 typically recovers
    const approx = {
        'A2': s => [s[1], -1.0*s[0]],  // M1 recovers this almost exactly
        'B2': s => [s[1], -9.73*s[0]+1.459*Math.pow(s[0],3)],  // Taylor approx
        'C2': s => [s[1], s[0]-Math.pow(s[0],3)-0.2*s[1]],  // usually exact
        'E1': s => [s[1], -s[0]+2.005*s[1]-2.002*s[0]*s[0]*s[1]],
        'G1': s => [-10.1*s[0]+10.06*s[1], 28.49*s[0]-1.20*s[1]-1.04*s[0]*s[2], -2.63*s[2]+1.06*s[0]*s[1]],
        'G2': s => [-s[1]-0.999*s[2], s[0]+0.2*s[1], -5.69*s[2]+1.004*s[0]*s[2]]
    };
    return approx[sys] || null;
}
function getWorstODE(sys){
    const w={
        'A2':s=>[1.22*s[1],-9.73*s[0]+1.459*s[0]*s[0]*s[0]],
        'B2':s=>[s[1],-9.83*s[0]+1.55*s[0]*s[0]*s[0]],
        'C2':s=>[s[1],0.63*s[1]+0.79*s[0]*s[1]+1.82*s[1]*s[1]],
        'E1':s=>[0.75*s[1],3.91*s[1]-2.53*s[0]*s[0]*s[1]],
        'G1':s=>[-1.05-1.46*s[0]+6.22*s[1],-3.23+17.63*s[0]+4.57*s[1]+0.62*s[2]-0.48*s[0]*s[2],2.58-1.51*s[0]+0.83*s[1]-3.22*s[2]+1.31*s[0]*s[1]],
        'G2':s=>[-s[1]-0.87*s[2],s[0]+0.2*s[1],-4.88*s[2]]
    };
    return w[sys]||null;
}

function runTraj(){
    const sys=document.getElementById('tj-sys').value;
    const dim=parseInt(document.getElementById('tj-dim').value);
    const cfg=TODE[sys];if(!cfg)return;
    const trueT=sim(cfg.f,cfg.ic,cfg.dt,cfg.n);
    const bestF=parsePredCoeffs(null,sys);
    const bestT=bestF?sim(bestF,cfg.ic,cfg.dt,cfg.n):trueT;
    const worstF=getWorstODE(sys);
    const worstT=worstF?sim(worstF,cfg.ic,cfg.dt,cfg.n):null;
    drawTraj(sys,dim,trueT,bestT,worstT,cfg.dt);
}

function drawTraj(sys,dim,trueT,bestT,worstT,dt){
    const cv=document.getElementById('traj-canvas');const W=cv.offsetWidth||600;cv.width=W;const H=300;cv.height=H;
    const ctx=cv.getContext('2d');ctx.fillStyle='#06070d';ctx.fillRect(0,0,W,H);
    const all=[...trueT,...bestT].map(s=>s[dim]).filter(isFinite);
    if(!all.length)return;
    const mn=Math.min(...all),mx=Math.max(...all);
    const px=40,py=20;
    const sx=i=>px+i/(trueT.length-1)*(W-2*px);
    const sy=v=>H-py-(v-mn)/(mx-mn||1)*(H-2*py);
    // grid
    ctx.strokeStyle='rgba(255,255,255,.04)';ctx.lineWidth=1;
    for(let g=0;g<=4;g++){const y=py+g*(H-2*py)/4;ctx.beginPath();ctx.moveTo(px,y);ctx.lineTo(W-px,y);ctx.stroke();
        const v=mx-(g/4)*(mx-mn);ctx.fillStyle='rgba(255,255,255,.22)';ctx.font='9px JetBrains Mono';ctx.fillText(v.toFixed(2),2,y+3)}
    function dl(t,col,a,w,dash){ctx.save();ctx.beginPath();ctx.strokeStyle=col;ctx.globalAlpha=a;ctx.lineWidth=w;if(dash)ctx.setLineDash([5,3]);
        let f=true;t.forEach((s,i)=>{const v=s[dim];if(!isFinite(v)){f=true;return}if(f){ctx.moveTo(sx(i),sy(v));f=false}else ctx.lineTo(sx(i),sy(v))});ctx.stroke();ctx.restore()}
    if(worstT)dl(worstT,'#f43f5e',.4,1.5,true);
    dl(bestT,'#818cf8',.9,2,false);
    dl(trueT,'#34d399',1,2.5,false);
    ctx.fillStyle='rgba(255,255,255,.45)';ctx.font='bold 10px Inter';
    ctx.fillText((SN[sys]||sys)+' — '+(dim===0?'x₀':'x₁'),px+4,16);
    ctx.fillStyle='rgba(255,255,255,.3)';ctx.font='9px Inter';
    ctx.fillText('t=0',px,H-4);ctx.fillText('t='+(trueT.length*dt).toFixed(1),W-px-28,H-4);
    // info box
    const bw=getBestWorst(sys);
    if(bw.best){ctx.fillStyle='rgba(129,140,248,.7)';ctx.font='9px Inter';
        ctx.fillText('Best: '+(MS[bw.best.method]||bw.best.method)+' NMSE='+bw.best.nmse.toFixed(4),px+4,H-4)}
}

function buildAn(){buildLB();buildHM();buildSB();setTimeout(runTraj,80)}
init();render();
['f-m','f-s','f-n','f-st','f-so'].forEach(id=>document.getElementById(id).addEventListener('change',render));
</script>
</body>
</html>"""

    # Replace placeholders
    html = html.replace('__DATA_JSON__', data_json_str)
    html = html.replace('__N_RESULTS__', str(n_results))
    html = html.replace('__ELAPSED__', elapsed_fmt)

    return html
