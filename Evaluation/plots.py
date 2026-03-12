import matplotlib.pyplot as plt
import os


def time_series(system_id, t, x_true, x_pred, outdir):
    plt.figure()
    plt.plot(t, x_true[:, 0], label="true")
    plt.plot(t, x_pred[:, 0], "--", label="sindy")
    plt.legend()
    plt.title(f"{system_id} Time Series")
    plt.savefig(os.path.join(outdir, f"{system_id}_timeseries.png"))
    plt.close()


def phase_portrait(system_id, x_true, x_pred, outdir):
    plt.figure()
    plt.plot(x_true[:, 0], x_true[:, 1], label="true")
    plt.plot(x_pred[:, 0], x_pred[:, 1], "--", label="sindy")
    plt.legend()
    plt.title(f"{system_id} Phase Portrait")
    plt.savefig(os.path.join(outdir, f"{system_id}_phase.png"))
    plt.close()
