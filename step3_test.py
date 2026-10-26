import matplotlib.pyplot as plt
from signals import make_true, add_noise
from filters import moving_average

true = make_true()
noisy = add_noise(true, sigma=2.0)

plt.figure(figsize=(11, 5))
plt.plot(noisy, color="lightgray", label="noisy sensor")
plt.plot(true, color="black", linewidth=2, label="true value")
for w in [3, 11, 51]:
    plt.plot(moving_average(noisy, w), label=f"moving average, w={w}")
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 3: moving average window size")
plt.savefig("results/02_moving_average.png", dpi=150)
