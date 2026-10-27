import re
import pandas as pd

def lag_txt(v):
    return "did not settle" if pd.isna(v) else f"{int(v)} samples"

t = pd.read_csv("results/results_table.csv")
t["lag"] = pd.to_numeric(t["lag"], errors="coerce")
clean = t[t["condition"] == "noise only (sigma=2)"].drop_duplicates("filter")

# Finding 1: lowest RMSE vs shortest lag
best = clean.loc[clean["RMSE"].idxmin()]
settled = clean.dropna(subset=["lag"])
if len(settled):
    short = settled.loc[settled["lag"].idxmin()]
    lag_part = f"the {short['filter']} had the shortest lag ({lag_txt(short['lag'])})"
    same = best["filter"] == short["filter"]
else:
    lag_part = "none of the filters settled within the lag band"
    same = False
f1 = (f"On the noise-only test (sigma=2), the {best['filter']} had the lowest RMSE ({best['RMSE']}) and {lag_part}. "
      + ("They were the same filter. " if same else "No single filter won on both measures. ")
      + "A smoother filter averages over more past readings, so it removes more noise but takes longer to follow the step.")

# Finding 2: spikes
sp = t[t["condition"] == "spikes (2%, size 20)"].drop_duplicates("filter")
sb = sp.loc[sp["RMSE"].idxmin()]
sw = sp.loc[sp["RMSE"].idxmax()]
w_clean = clean[clean["filter"] == sw["filter"]]["RMSE"].iloc[0]
f2 = (f"With 2% spikes, the {sb['filter']} had the lowest RMSE ({sb['RMSE']}) and the {sw['filter']} the highest ({sw['RMSE']}, up from {w_clean} without spikes). "
      "Averaging filters (moving average, EMA, Kalman) are pulled toward each spike, while a median takes the middle value of its window and cannot be moved by one extreme reading.")

# Finding 3: dropouts
dr = t[t["condition"] == "10% dropouts"].drop_duplicates("filter").set_index("filter")["RMSE"]
cl = clean.set_index("filter")["RMSE"]
chg = (dr - cl).dropna()
big = chg.abs().idxmax()
f3 = (f"With 10% of samples missing, RMSE changed by at most {abs(chg[big]):.3f} across the filters (largest change: {big}, from {cl[big]} to {dr[big]}). "
      "Each filter skips a missing reading and carries on from its previous estimate, or averages only the readings it has, so a gap costs very little.")

# Finding 4: Kalman q
k = pd.read_csv("results/kalman_tuning.csv")
k["lag"] = pd.to_numeric(k["lag"], errors="coerce")
a, b = k.iloc[0], k.iloc[-1]
f4 = (f"As q grew from {a['q']} to {b['q']}, the Kalman filter's RMSE went from {a['RMSE']} to {b['RMSE']} and its lag went from {lag_txt(a['lag'])} to {lag_txt(b['lag'])}. "
      "A larger q tells the filter the true value changes a lot, so it trusts each new reading more: faster, but noisier. ")
ok = k.dropna(subset=["lag"])
if len(ok):
    c = ok.loc[ok["RMSE"].idxmin()]
    f4 += f"I chose q={c['q']}, the lowest RMSE ({c['RMSE']}) among the settings that settled (lag {lag_txt(c['lag'])})."
else:
    f4 += "None of the q values settled within the lag band."

# Finding 5: phone data
try:
    p = pd.read_csv("results/phone_table.csv")
    p["settle time (s)"] = pd.to_numeric(p["settle time (s)"], errors="coerce")
    nz = "noise on flat part (std)"
    raw = p[p["filter"] == "Raw sensor"].iloc[0]
    oth = p[p["filter"] != "Raw sensor"]
    q = oth.loc[oth[nz].idxmin()]
    def st(v):
        return "did not settle" if pd.isna(v) else f"{v} s"
    slower = pd.isna(q["settle time (s)"]) or (not pd.isna(raw["settle time (s)"]) and q["settle time (s)"] > raw["settle time (s)"])
    f5 = (f"The phone accelerometer recording has no ground truth, so noise was measured as the standard deviation on a flat stretch. The raw sensor had a noise std of {raw[nz]}; the quietest filter was {q['filter']} at {q[nz]}, and it settled in {st(q['settle time (s)'])} compared with {st(raw['settle time (s)'])} for the raw signal. "
          + ("Less noise came with slower settling, the same tradeoff as in the simulation." if slower else "In this recording the tradeoff was not clear: the quietest filter did not settle later than the raw signal."))
except FileNotFoundError:
    f5 = "The real-sensor test was not completed."

findings = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5}
out = []
for line in open("README.md").read().split("\n"):
    m = re.match(r"FINDING (\d):", line)
    out.append(f"- **Finding {m.group(1)}:** " + findings[int(m.group(1))] if m else line)
open("README.md", "w").write("\n".join(out))
print("README updated")
