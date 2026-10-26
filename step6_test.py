import matplotlib.pyplot as plt
from signals import make_true, add_noise
from filters import ema, kalman_1d

true = make_true()
noisy = add_noise(true, sigma=2.0)

plt.figure(figsize=(11, 5))
plt.plot(noisy, color="lightgray", label="noisy sensor")
plt.plot(true, color="black", linewidth=2, label="true value")
for q in [0.001, 0.01, 0.1, 1.0]:
    plt.plot(kalman_1d(noisy, q=q, r=4.0), label=f"Kalman q={q}")
plt.plot(ema(noisy, 0.05), "--", color="gray", label="EMA alpha=0.05")
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 6: Kalman filter, effect of q (r=4)")
plt.savefig("results/05_kalman.png", dpi=150)
