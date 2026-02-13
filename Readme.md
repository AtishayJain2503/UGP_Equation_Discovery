# Equation Discovery Benchmarks for Nonlinear Dynamical Systems

This repository contains a modular benchmarking framework for evaluating **equation discovery and system identification methods** on nonlinear dynamical systems of increasing complexity.

The primary motivation is to understand **where existing methods succeed, where they fail, and why**, particularly for systems with:
- strong nonlinearities
- external forcing
- limit cycles
- hysteresis and memory effects

This project is developed as part of an undergraduate research project, with the long-term goal of exploring **machine learning–based approaches for discovering governing equations beyond current limits**.

---

## 🔍 Problem Motivation

Equation discovery methods such as:
- Sparse Identification of Nonlinear Dynamics (SINDy)
- Symbolic regression
- Bayesian sparse learning

have shown strong performance on **low-dimensional, memoryless systems**.

However, real-world mechanical and structural systems often involve:
- nonlinear damping and stiffness
- bifurcations and chaos
- hysteresis and internal state variables (memory)

This repository focuses on **systematically benchmarking** these methods on progressively harder systems to identify **failure modes and performance boundaries**.

---

## 📐 Benchmark Systems

The following canonical dynamical systems are currently implemented:

| ID | System | Key Features |
|----|-------|--------------|
| A2 | Damped Harmonic Oscillator | Linear, dissipative |
| B2 | Nonlinear Oscillator | Polynomial nonlinearity |
| C2 | Large-Angle Pendulum | Strong nonlinearity (sin θ) |
| D1 | Forced Duffing Oscillator | Nonlinearity + external forcing |
| E1 | Van der Pol Oscillator | Limit cycle, nonlinear damping |
| F1 | Minimal Bouc–Wen Model | Hysteresis, internal memory |

These systems are chosen to represent a **controlled increase in modeling difficulty**, culminating in hysteretic dynamics.

---

## 🧠 Methods (Current & Planned)

### Currently
- High-fidelity numerical simulation (ground truth data)
- Phase portraits and trajectory visualization
- Baseline evaluation using SINDy (PySINDy)

### Planned
- Physics-informed sparse regression
- Memory-augmented libraries
- Neural ODE / transformer-based equation discovery
- Symbolic latent-space search methods

---

## 🗂️ Project Structure

```text
.
├── equations/          # Dynamical system definitions (physics + ODEs)
│   ├── base.py
│   ├── damped_oscillator.py
│   ├── duffing.py
│   ├── van_der_pol.py
│   └── bouc_wen.py
│
├── experiments/        # Reproducible experiment scripts
│   ├── run_a2.py
│   ├── run_d1.py
│   ├── run_e1.py
│   └── run_f1.py
│
├── utils/              # Plotting and helper utilities
│
├── README.md
└── .gitignore
