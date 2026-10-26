import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from signals import make_true, add_noise, add_spikes, add_dropouts
from filters import moving_average, ema, median_filter, kalman_1d
from metrics import rmse, lag

true = make_true()

def run_all(signal):
    return {
        "Moving average (w=11)": moving_average(signal, 11),
        "EMA (alpha=0.2)": ema(signal, 0.2),
        "Median (w=11)": median_filter(signal, 11),
        "Kalman (q=0.01, r=4)": kalman_1d(signal, 0.01, 4.0),
    }

def evaluate(signal, label):
    rows = []
    for name, est in run_all(signal).items():
        rows.append({
            "condition": label,
            "filter": name,
            "RMSE": round(rmse(est, true), 3),
            "lag": lag(est, true),
        })
    return rows

def plot_all(signal, title, path):
    plt.figure(figsize=(11, 5))
    plt.plot(signal, color="lightgray", label="sensor input")
    plt.plot(true, color="black", linewidth=2, label="true value")
    for name, est in run_all(signal).items():
        plt.plot(est, label=name)
    plt.legend()
    plt.xlabel("sample")
    plt.ylabel("value")
    plt.title(title)
    plt.savefig(path, dpi=150)
    plt.close()

noisy = add_noise(true, sigma=2.0)

plot_all(noisy, "Step 9: all filters, noise only (sigma=2)", "results/06_all_filters.png")

table = pd.DataFrame(evaluate(noisy, "noise only (sigma=2)"))
print(table.to_string(index=False))
table.to_csv("results/results_table.csv", index=False)
