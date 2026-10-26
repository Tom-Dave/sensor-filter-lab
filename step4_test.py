import matplotlib.pyplot as plt
from signals import make_true, add_noise
from filters import moving_average, ema

true = make_true()
noisy = add_noise(true, sigma=2.0)

plt.figure(figsize=(11, 5))
plt.plot(noisy, color="lightgray", label="noisy sensor")
plt.plot(true, color="black", linewidth=2, label="true value")
for a in [0.05, 0.2, 0.5]:
    plt.plot(ema(noisy, a), label=f"EMA, alpha={a}")
plt.plot(moving_average(noisy, 11), "--", color="tab:blue", label="moving average, w=11")
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 4: EMA alpha values vs moving average")
plt.savefig("results/03_ema.png", dpi=150)
