import numpy as np

def moving_average(x, w=11):
    out = np.empty(len(x))
    for i in range(len(x)):
        start = max(0, i - w + 1)
        out[i] = np.nanmean(x[start:i + 1])
    return out
