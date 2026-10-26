import matplotlib.pyplot as plt
from signals import make_true, add_noise, add_spikes
from filters import moving_average, median_filter

true = make_true()
noisy = add_noise(true, sigma=2.0)
spiky = add_spikes(noisy, prob=0.02, size=20.0)

plt.figure(figsize=(11, 5))
plt.plot(spiky, color="lightgray", label="noisy + spikes")
plt.plot(true, color="black", linewidth=2, label="true value")
plt.plot(moving_average(spiky, 11), label="moving average, w=11")
plt.plot(median_filter(spiky, 11), label="median, w=11")
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 5: spikes, average vs median")
plt.savefig("results/04_median_spikes.png", dpi=150)
