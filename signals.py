import numpy as np

def make_true(n=500, step_at=250, low=10.0, high=25.0):
    # a flat value that suddenly jumps (a step)
    true = np.full(n, low)
    true[step_at:] = high
    return true

def add_noise(true, sigma=2.0, seed=42):
    rng = np.random.default_rng(seed)
    return true + rng.normal(0, sigma, len(true))

def add_spikes(x, prob=0.02, size=20.0, seed=1):
    # random glitches: a few readings jump far up or down
    rng = np.random.default_rng(seed)
    out = x.copy()
    mask = rng.random(len(x)) < prob
    out[mask] += rng.choice([-1, 1], mask.sum()) * size
    return out

def add_dropouts(x, prob=0.10, seed=2):
    # random missing samples, stored as NaN
    rng = np.random.default_rng(seed)
    out = x.copy()
    mask = rng.random(len(x)) < prob
    mask[0] = False
    out[mask] = np.nan
    return out
