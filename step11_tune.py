import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from signals import make_true, add_noise
from filters import kalman_1d
from metrics import rmse, lag

true = make_true()
noisy = add_noise(true, sigma=2.0)

# Part 1: sweep q with r fixed at 4
qs = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]
rows = []
plt.figure(figsize=(11, 5))
plt.plot(noisy, color="lightgray", label="noisy sensor")
plt.plot(true, color="black", linewidth=2, label="true value")
for q in qs:
    est = kalman_1d(noisy, q=q, r=4.0)
    plt.plot(est, label=f"q={q}")
    rows.append({"q": q, "r": 4.0, "RMSE": round(rmse(est, true), 3), "lag": lag(est, true)})
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 11: Kalman tuning, q sweep (r=4)")
plt.savefig("results/10_kalman_q_sweep.png", dpi=150)
plt.close()

table = pd.DataFrame(rows)
print(table.to_string(index=False))
table.to_csv("results/kalman_tuning.csv", index=False)

# Part 2: RMSE vs lag tradeoff
plt.figure(figsize=(7, 5))
for _, row in table.iterrows():
    if pd.notna(row["lag"]):
        plt.scatter(row["lag"], row["RMSE"])
        plt.annotate(f"q={row['q']}", (row["lag"], row["RMSE"]))
plt.xlabel("lag (samples to settle after the step)")
plt.ylabel("RMSE")
plt.title("Kalman tradeoff: error vs lag")
plt.savefig("results/11_tradeoff.png", dpi=150)
plt.close()

# Part 3: does only the ratio q/r matter?
a = kalman_1d(noisy, q=0.01, r=4.0)
b = kalman_1d(noisy, q=0.1, r=40.0)
print()
print("q=0.01, r=4   -> RMSE", round(rmse(a, true), 3), "lag", lag(a, true))
print("q=0.1,  r=40  -> RMSE", round(rmse(b, true), 3), "lag", lag(b, true))
print("largest gap between the two outputs:", round(float(abs(a - b).max()), 3))
