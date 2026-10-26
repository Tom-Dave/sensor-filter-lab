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

# ---------- Step 10: stress tests ----------
all_rows = evaluate(noisy, "noise only (sigma=2)")

# Test A: increasing noise
for sigma in [0.5, 1, 2, 4, 8]:
    sig = add_noise(true, sigma=sigma)
    label = f"noise sigma={sigma}"
    all_rows += evaluate(sig, label)
    est = kalman_1d(sig, 0.01, sigma ** 2)
    all_rows.append({
        "condition": label,
        "filter": "Kalman (q=0.01, r=sigma^2)",
        "RMSE": round(rmse(est, true), 3),
        "lag": lag(est, true),
    })

# Test B: spikes
spiky = add_spikes(noisy, prob=0.02, size=20.0)
all_rows += evaluate(spiky, "spikes (2%, size 20)")
plot_all(spiky, "Test B: spikes", "results/07_spikes.png")

# Test C: dropouts
dropped = add_dropouts(noisy, prob=0.10)
all_rows += evaluate(dropped, "10% dropouts")
plot_all(dropped, "Test C: 10% missing samples", "results/08_dropouts.png")

table = pd.DataFrame(all_rows)
table.to_csv("results/results_table.csv", index=False)
print(table.to_string(index=False))

# RMSE vs noise level
noise_rows = table[table["condition"].str.startswith("noise sigma")].copy()
noise_rows["sigma"] = noise_rows["condition"].str.replace("noise sigma=", "").astype(float)
plt.figure(figsize=(8, 5))
for name, grp in noise_rows.groupby("filter"):
    grp = grp.sort_values("sigma")
    plt.plot(grp["sigma"], grp["RMSE"], marker="o", label=name)
plt.xlabel("noise sigma")
plt.ylabel("RMSE")
plt.title("Test A: RMSE as noise increases")
plt.legend()
plt.savefig("results/09_rmse_vs_noise.png", dpi=150)
plt.close()
