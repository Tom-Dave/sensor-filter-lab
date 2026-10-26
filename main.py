import numpy as np
import matplotlib.pyplot as plt
from signals import make_true, add_noise, add_spikes, add_dropouts

true = make_true()
noisy = add_noise(true, sigma=2.0)

plt.figure(figsize=(10, 4))
plt.plot(noisy, color="lightgray", label="noisy sensor")
plt.plot(true, color="black", label="true value")
plt.legend()
plt.xlabel("sample")
plt.ylabel("value")
plt.title("Step 2: signal and noise")
plt.savefig("results/01_signal.png", dpi=150)
plt.show()

