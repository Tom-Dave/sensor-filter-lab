import numpy as np

def rmse(estimate, true):
    return np.sqrt(np.mean((estimate - true) ** 2))

def lag(estimate, true, step_at=250, tolerance=0.1, hold=10):
    step_size = abs(true[step_at] - true[step_at - 1])
    limit = tolerance * step_size
    for i in range(step_at, len(true) - hold):
        window = estimate[i:i + hold]
        if np.all(np.abs(window - true[i:i + hold]) < limit):
            return i - step_at
    return None
