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

def median_filter(x, w=11):
    out = np.empty(len(x))
    for i in range(len(x)):
        start = max(0, i - w + 1)
        out[i] = np.nanmedian(x[start:i + 1])
    return out

def kalman_1d(z, q=0.01, r=4.0):
    x = z[~np.isnan(z)][0]
    p = 1.0
    out = np.empty(len(z))
    for i, m in enumerate(z):
        p = p + q
        if not np.isnan(m):
            k = p / (p + r)
            x = x + k * (m - x)
            p = (1 - k) * p
        out[i] = x
    return out
