import matplotlib.pyplot as plt


def plot_time_series(t, X, labels, title):
    plt.figure(figsize=(10, 4))
    for i, label in enumerate(labels):
        plt.plot(t, X[:, i], label=label)
    plt.xlabel("Time")
    plt.ylabel("State")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_phase(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(4, 4))
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
