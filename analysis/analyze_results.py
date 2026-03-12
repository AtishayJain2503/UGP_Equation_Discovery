import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("results/benchmark_summary.csv")

df = df[df["status"] == "STABLE"]

# =========================
# Mean NMSE per method
# =========================

method_perf = df.groupby("method")["nmse"].mean()

print("\nAverage NMSE by Method\n")
print(method_perf.sort_values())

# =========================
# System difficulty
# =========================

system_perf = df.groupby("system")["nmse"].mean()

print("\nAverage NMSE by System\n")
print(system_perf.sort_values())

# =========================
# Heatmap
# =========================

heat = df.pivot_table(
    values="nmse",
    index="system",
    columns="method",
    aggfunc="mean"
)

plt.figure(figsize=(10,6))

sns.heatmap(
    heat,
    annot=True,
    fmt=".2g",
    cmap="viridis"
)

plt.title("Method vs System Performance (NMSE)")

plt.tight_layout()

plt.savefig("results/figures/method_system_heatmap.png")

# =========================
# Accuracy vs Complexity
# =========================

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x="complexity",
    y="nmse",
    hue="method"
)

plt.yscale("log")

plt.title("Accuracy vs Complexity")

plt.tight_layout()

plt.savefig("results/figures/accuracy_complexity.png")

# =========================
# Noise robustness
# =========================

plt.figure(figsize=(8,6))

sns.lineplot(
    data=df,
    x="noise",
    y="nmse",
    hue="method"
)

plt.yscale("log")

plt.title("Noise Robustness")

plt.tight_layout()

plt.savefig("results/figures/noise_robustness.png")


print("\nAnalysis complete.")