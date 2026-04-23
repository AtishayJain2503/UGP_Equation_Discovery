import csv
from experiments.run_benchmark import generate_html_report

summary_rows = []
try:
    with open("results/benchmark_summary.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for r in reader:
            if len(r) != 9: continue
            method, system, noise, nmse, rollout, complexity, status, true_eq, pred_eq = r
            nmse = float(nmse) if nmse not in ('inf', 'DIVERGED') else float('inf')
            rollout = float(rollout) if rollout not in ('inf', 'nan') else float('inf')
            complexity = float(complexity) if complexity != 'nan' else float('nan')
            summary_rows.append([method, system, noise, nmse, rollout, complexity, status, true_eq, pred_eq])

    html = generate_html_report(summary_rows, 20508.6)
    with open("results/benchmark_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("UI successfully updated!")
except Exception as e:
    print(f"Error: {e}")
