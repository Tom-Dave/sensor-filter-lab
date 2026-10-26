import numpy as np

def moving_average(x, w=11):
    out = np.empty(len(x))
    for i in range(len(x)):
        start = max(0, i - w + 1)
        out[i] = np.nanmean(x[start:i + 1])
    return out

def ema(x, alpha=0.2):
    out = np.empty(len(x))
    out[0] = x[0]
    for i in range(1, len(x)):
        if np.isnan(x[i]):
            out[i] = out[i - 1]
        else:
            out[i] = alpha * x[i] + (1 - alpha) * out[i - 1]
    return out
