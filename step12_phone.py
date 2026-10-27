import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filters import moving_average, ema, median_filter, kalman_1d

path = sys.argv[1]
col = int(sys.argv[2]) if len(sys.argv) > 2 else 1
df = pd.read_csv(path)
t = df.iloc[:, 0].to_numpy(dtype=float)
v = df.iloc[:, col].to_numpy(dtype=float)
print("rows:", len(t), "| duration (s):", round(t[-1] - t[0], 1))
print("using column:", df.columns[col])

# resample onto an even grid (10 samples per second)
fs = 10
grid = np.arange(t[0], t[-1], 1 / fs)
raw = np.interp(grid, t, v)
time_s = grid - grid[0]

# find the step: the biggest change over half a second
k = 5
step_i = int(np.argmax(np.abs(raw[k:] - raw[:-k])))
before = float(np.median(raw[:int(5 * fs)]))
final = float(np.median(raw[-int(5 * fs):]))
step_size = abs(final - before)
print("step at t =", round(time_s[step_i], 1), "s | before:", round(before, 2),
      "| after:", round(final, 2), "| size:", round(step_size, 2))

# flat section before the step, used to estimate noise
flat = slice(int(3 * fs), max(int(3 * fs) + 5, step_i - int(1 * fs)))
r_est = max(float(np.var(raw[flat])), 1e-6)
print("estimated sensor noise variance r =", round(r_est, 6))

outputs = {
    "Raw sensor": raw,
    "Moving average (w=11)": moving_average(raw, 11),
    "EMA (alpha=0.2)": ema(raw, 0.2),
    "Median (w=11)": median_filter(raw, 11),
    "Kalman (q=0.05*r)": kalman_1d(raw, 0.05 * r_est, r_est),
    "Kalman (q=0.5*r)": kalman_1d(raw, 0.5 * r_est, r_est),
}

def settle_time(est):
    limit = 0.1 * step_size
    hold = int(1 * fs)
    for i in range(step_i, len(est) - hold):
        if np.all(np.abs(est[i:i + hold] - final) < limit):
            return round((i - step_i) / fs, 2)
    return None

rows = []
for name, est in outputs.items():
    rows.append({
        "filter": name,
        "noise on flat part (std)": round(float(np.std(est[flat])), 4),
        "settle time (s)": settle_time(est),
    })
table = pd.DataFrame(rows)
print()
print(table.to_string(index=False))
table.to_csv("results/phone_table.csv", index=False)

plt.figure(figsize=(11, 5))
plt.plot(time_s, raw, color="lightgray", label="raw phone sensor")
for name, est in outputs.items():
    if name != "Raw sensor":
        plt.plot(time_s, est, label=name)
plt.axvline(time_s[step_i], color="black", linestyle=":", label="step")
plt.legend()
plt.xlabel("time (s)")
plt.ylabel("acceleration (m/s^2)")
plt.title("Step 12: real phone accelerometer (z-axis)")
plt.savefig("results/12_phone_data.png", dpi=150)
