# Equation Discovery Benchmark for Nonlinear Dynamical Systems

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SciML](https://img.shields.io/badge/Field-SciML-red.svg)](https://sciml.ai/)

A modular benchmarking framework that systematically evaluates **9 Equation Discovery methods** across **10 nonlinear dynamical systems** at **3 noise levels** (270 total experiments). Built as an Undergraduate Project (UGP) to expose the failure boundaries of modern Scientific Machine Learning algorithms.

---

## Abstract

Modern SciML algorithms excel in idealized settings but degrade when encountering strong nonlinearities, hysteresis, chaos, and observational noise. This framework provides a controlled environment to test methods like **SINDy, PySR, Neural ODEs, and PINNs** under progressively complex dynamical challenges.

**Key Results:**
- **PySR (M4)** achieves the best accuracy across diverse nonlinear systems via evolutionary symbolic search.
- **Bayesian SINDy (M3)** is the most noise-robust sparse method due to probabilistic sparsity priors.
- **Hysteretic systems (F1–F3)** expose fundamental basis limitations in all polynomial methods.
- **Neural methods (M5, M6)** provide stability bounds but yield no interpretable equations.

---

## Benchmark Systems (10 Dynamical Regimes)

| ID | System | Dim | Type | Primary Challenge |
|:---|:---|:---:|:---|:---|
| **A2** | Damped Harmonic Oscillator | 2D | Linear | Baseline |
| **B2** | Large-Angle Pendulum | 2D | Nonlinear | Transcendental (`sin`) |
| **C2** | Duffing Oscillator | 2D | Nonlinear | Cubic stiffness |
| **D1** | Forced Duffing | 3D+t | Forced | External `cos(ωt)` forcing |
| **E1** | Van der Pol Oscillator | 2D | Nonlinear | Limit cycles |
| **F1** | Bouc–Wen I | 3D | Hysteretic | Memory / hidden states |
| **F2** | Bouc–Wen II | 3D | Hysteretic | Nonlinear hysteresis |
| **F3** | Bouc–Wen 4D | 4D | Hysteretic | 4-state coupling |
| **G1** | Lorenz Attractor | 3D | Chaotic | Sensitivity to ICs |
| **G2** | Rössler Attractor | 3D | Chaotic | Phase space folding |

---

## Equation Discovery Methods (9 Algorithms)

| ID | Method | Type | Outputs Equations? | Noise Robustness |
|:---|:---|:---|:---:|:---:|
| **M1** | SINDy (Polynomial Basis) | Sparse Regression | ✅ Yes | Medium |
| **M2** | SINDy (Custom: Poly + Fourier) | Sparse Regression | ✅ Yes | Low |
| **M3** | Bayesian SINDy | Bayesian Sparse | ✅ Yes | ⭐ High |
| **M4** | PySR (Genetic Programming) | Symbolic Evolution | ✅ Yes | ⭐ High |
| **M5** | Neural ODE | Neural | ❌ Black-box | High |
| **M6** | PINN | Neural | ❌ Black-box | High |
| **M7** | Grammar-Constrained Symbolic | Symbolic Evolution | ✅ Yes | Medium |
| **M8** | PISF (Physics-Informed Sparse) | Sparse Regression | ✅ Yes | Medium |
| **M9** | Ensemble SINDy (Bootstrap) | Ensemble Sparse | ✅ Yes | High |

> **Note:** Neural ODE (M5) and PINN (M6) are included as **black-box baselines** — they establish the maximum achievable predictive fidelity but do not produce human-readable symbolic equations.

---

## Project Architecture

```text
UGP_Equation_Discovery/
├── physics/              # Ground truth ODE systems (A2–G2)
├── discovery/            # Algorithmic wrappers for all 9 methods
├── evaluation/           # NMSE, Rollout Error, Complexity metrics
├── registry/             # Centralized method & system registries
├── experiments/
│   ├── generate_datasets.py   # Physics simulation + noise injection
│   ├── run_benchmark.py       # Main benchmark orchestrator
│   └── html_template.py       # Interactive dashboard generator
├── data/                 # Generated .npz trajectories (gitignored)
├── results/
│   ├── benchmark_summary.csv  # Raw results (270 rows)
│   └── benchmark_report.html  # Interactive 3-tab dashboard
├── regenerate_html.py    # Rebuild dashboard from existing CSV
├── requirements.txt      # Python dependencies
└── Readme.md
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/AtishayJain2503/UGP_Equation_Discovery.git
cd UGP_Equation_Discovery

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Core dependencies:** `pysindy`, `pysr`, `torch`, `scipy`, `numpy`, `scikit-learn`

### 2. Generate Datasets

Simulate ground-truth physics with RK45 integration and inject noise (0%, 2%, 5%):

```bash
python -m experiments.generate_datasets
```

This creates `data/` with `.npz` files for all 10 systems × 3 noise levels.

### 3. Run the Full Benchmark

```bash
python -m experiments.run_benchmark
```

> ⏱ **Estimated runtime:** ~5 hours on a modern GPU machine (PySR evolutionary search is the bottleneck).
>
> Results are saved incrementally to `results/benchmark_summary.csv` — if the run crashes, no data is lost.

### 4. View the Interactive Dashboard

```bash
# Windows:
start results/benchmark_report.html

# Mac/Linux:
open results/benchmark_report.html
```

The dashboard is a **standalone HTML file** — no server needed. It has 3 tabs:

| Tab | Contents |
|:---|:---|
| **📊 Results** | Filterable/sortable cards for all 270 runs with true vs discovered equations |
| **📄 Whitepaper** | Full methodology writeup: 9 methods table, 10 systems table, worked examples, engineering challenges |
| **📈 Analytics** | Method leaderboard, NMSE heatmap, live trajectory comparison (RK4 in browser), stability bars |

### 5. Regenerate Dashboard (without re-running benchmark)

If you already have `results/benchmark_summary.csv`, you can rebuild just the HTML:

```bash
python regenerate_html.py
```

---

## 📊 Evaluation Metrics

| Metric | Description | Good Value |
|:---|:---|:---|
| **NMSE** | Normalized Mean Squared Error between true and predicted trajectories | < 0.01 |
| **Rollout Error** | Accumulated absolute deviation over the full simulation horizon | < 0.3 |
| **Stability** | Whether the discovered ODE remains bounded during forward simulation | STABLE |
| **Complexity** | Number of terms in the discovered equation (Occam's razor) | 2–8 |

---

## 🔧 Engineering Challenges Solved

### The Collinearity Explosion
The default `STLSQ` optimizer in SINDy spread mass across correlated polynomial terms on clean periodic data, causing catastrophic divergence. **Fix:** Migrated all SINDy variants to `SR3` with `L0` regularization. Runtime dropped from 14h → 5.6h.

### The Target Data Leak
Passing clean analytical derivatives (`Ẋ_clean`) alongside noisy states (`X_noisy`) creates an information mismatch that causes systematic overfitting. **Fix:** All noisy experiments now use `SmoothedFiniteDifference()` to compute empirical derivatives from the noisy data itself.

---

## 📄 Pre-computed Results

The repository includes pre-computed results from a full benchmark run:
- **`results/benchmark_summary.csv`** — 270 rows of raw metrics
- **`results/benchmark_report.html`** — Interactive dashboard (open directly in browser)

You can explore these without running any code.

---

## 🔬 Research Applications

This framework provides a systematic way to:
1. **Identify algorithm failure modes** on specific dynamical regimes
2. **Compare sparse vs evolutionary vs neural** approaches under controlled conditions
3. **Quantify noise robustness** across methods
4. **Benchmark new equation discovery algorithms** by adding them to `discovery/` and `registry/methods.py`

---

## License

MIT License. See [LICENSE](LICENSE) for details.