# Equation Discovery Benchmark Framework for Nonlinear Dynamical Systems

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SciML](https://img.shields.io/badge/Field-SciML-red.svg)](https://sciml.ai/)

A modular benchmarking framework designed to systematically evaluate **Equation Discovery** and **System Identification** methodologies across a spectrum of nonlinear dynamical regimes.

---

##  Abstract

The primary objective of this project is to evaluate the efficacy, limitations, and failure boundaries of modern **Scientific Machine Learning (SciML)** algorithms. While existing methods excel in idealized, low-dimensional settings, their performance often degrades when encountering:
* Strong nonlinearities and non-polynomial forces.
* External periodic forcing and non-autonomous dynamics.
* Limit cycles, hysteresis (memory effects), and chaotic attractors.

This repository provides a controlled, scalable environment to test state-of-the-art algorithms—such as **SINDy, PySR, and Neural ODEs**—under progressively complex dynamical challenges. Developed as part of an undergraduate research initiative, it aims to bridge the gap between automated law extraction and real-world physical complexity.

---

##  Table of Contents
* [Problem Motivation](#-problem-motivation)
* [Benchmark Systems](#-benchmark-systems)
* [Equation Discovery Methodologies](#-equation-discovery-methodologies)
* [System Architecture](#-system-architecture)
* [Evaluation Metrics](#-evaluation-metrics)
* [Installation & Usage](#-installation--usage)
* [Research Applications](#-research-applications)

---

##  Problem Motivation

Modern SciML paradigms often operate under the assumption of polynomial basis expansions and Markovian state transitions. However, real-world systems present significant hurdles:

1.  **Nonlinear Stiffness/Damping:** Deviations from standard harmonic assumptions.
2.  **Transcendentals:** Trigonometric or exponential restoring forces.
3.  **Non-Autonomous Dynamics:** Time-dependent external forcing functions.
4.  **Chaos:** High sensitivity to initial conditions and phase space folding.
5.  **Internal State Variables:** Hysteresis and history-dependent forces.

This framework isolates these phenomena to determine exactly where specific algorithms succeed or fail.

---

##  Benchmark Systems

The corpus consists of canonical systems curated to strictly isolate mathematical complexities. *(Note: Equations are represented using prime notation `x'` for first derivatives and `x''` for second derivatives to ensure cross-platform markdown compatibility).*

| ID | System | Governing Equation | Primary Challenge |
|:---|:---|:---|:---|
| **A2** | Damped Harmonic Oscillator | `x'' + cx' + kx = 0` | Baseline linear dynamics |
| **B2** | Large-Angle Pendulum | `θ'' + ω² sin(θ) = 0` | Non-polynomial transcendentals |
| **C2** | Duffing Oscillator | `x'' + δx' + αx + βx³ = 0` | Nonlinear polynomial stiffness |
| **D1** | Forced Duffing | `x'' + δx' + αx + βx³ = γ cos(ωt)` | External forcing |
| **E1** | Van der Pol | `x'' - μ(1 - x²)x' + x = 0` | Limit cycles |
| **F1** | Bouc–Wen Model | `x'' + cx' + kx + αz = 0` | Hysteresis / Hidden states |
| **G1** | Lorenz System | `x' = σ(y - x)` <br> `y' = x(ρ - z) - y` <br> `z' = xy - βz` | 3D Chaos & Sensitivity |
| **G2** | Rössler System | `x' = -y - z` <br> `y' = x + ay` <br> `z' = b + z(x - c)` | Phase space folding |

---

##  Equation Discovery Methodologies

The framework supports **192 discrete experiments** (8 Methods × 8 Systems × 3 Noise Levels).

| ID | Methodology | Algorithmic Category |
|:---|:---|:---|
| **M1** | SINDy (Polynomial Library) | Sparse Regression |
| **M2** | SINDy (Custom Library) | Physics-Informed Sparse Regression |
| **M3** | Bayesian SINDy | Probabilistic Sparse Learning |
| **M4** | Symbolic Regression (PySR) | Genetic Evolutionary Search |
| **M5** | Neural ODE | Neural Dynamical Systems |
| **M6** | Physics-Informed Neural Network (PINN) | Neural Physics Modeling |
| **M7** | Grammar-Constrained Symbolic Reg. | Restricted Domain Symbolic Search |
| **M8** | Physics-Informed Spline + Sparse | Noise-Robust Sparse Regression |

---

##  System Architecture

The project employs a modular execution flow to ensure reproducibility and ease of extension.

### Execution Pipeline
1.  **Physics Layer:** RK45 Integration of ground truth dynamics.
2.  **Dataset Generation:** Noise injection (0%, 2%, 5%).
3.  **Discovery Module:** Execution of algorithmic wrappers (SINDy, PySR, etc.).
4.  **Rollout Layer:** Forward numerical simulation of discovered equations.
5.  **Evaluation Layer:** Calculation of metrics and statistical aggregation.

### Directory Structure
```text
UGP_Equation_Discovery/
├── physics/          # Ground truth systems (A2 to G2)
├── discovery/        # Algorithmic wrappers for SINDy, PySR, PINNs
├── evaluation/       # Scoring, Rollout, and Complexity metrics
├── registry/         # Centralized mapping for automation
├── experiments/      # Main execution scripts
├── analysis/         # Visualization and reporting tools
├── data/             # Generated noisy/clean trajectories (.npz)
└── results/          # Output metrics, plots, and CSV summaries