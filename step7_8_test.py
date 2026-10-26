import pandas as pd
from signals import make_true, add_noise
from filters import moving_average, ema, median_filter, kalman_1d
from metrics import rmse, lag

true = make_true()
noisy = add_noise(true, sigma=2.0)

outputs = {
    "Raw sensor (no filter)": noisy,
    "Moving average (w=11)": moving_average(noisy, 11),
    "EMA (alpha=0.2)": ema(noisy, 0.2),
    "Median (w=11)": median_filter(noisy, 11),
    "Kalman (q=0.01, r=4)": kalman_1d(noisy, 0.01, 4.0),
    "Kalman (q=0.1, r=4)": kalman_1d(noisy, 0.1, 4.0),
}

rows = []
for name, est in outputs.items():
    rows.append({"filter": name, "RMSE": round(rmse(est, true), 3), "lag": lag(est, true)})

table = pd.DataFrame(rows)
print(table.to_string(index=False))
table.to_csv("results/table_noise_only.csv", index=False)
