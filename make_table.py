import pandas as pd

t = pd.read_csv("results/results_table.csv")
keep = ["noise only (sigma=2)", "spikes (2%, size 20)", "10% dropouts"]
t = t[t["condition"].isin(keep)].drop_duplicates()
t["lag"] = t["lag"].apply(lambda v: "did not settle" if pd.isna(v) else int(v))

print("| condition | filter | RMSE | lag (samples) |")
print("|---|---|---|---|")
for _, r in t.iterrows():
    print(f"| {r['condition']} | {r['filter']} | {r['RMSE']} | {r['lag']} |")
