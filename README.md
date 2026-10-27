# Sensor Noise Filtering Lab

A small prototype comparing four filters (moving average, exponential moving average, median, and a 1D Kalman filter) on noisy sensor data. Every filter trades smoothness against delay, so the question is how much, and where each one breaks.

## Problem

Real sensors are noisy, and robots, drones and phones need a clean estimate of what is actually happening. Which filter gives the best balance between error and lag, and how does each one cope with extra noise, spikes and missing samples?

## Method

- Simulated signal: a flat value of 10 that jumps to 25 at sample 250 (a step), with Gaussian noise (sigma = 2, fixed random seeds so results can be reproduced).
- Filters, all written from scratch with numpy: moving average (w=11), EMA (alpha=0.2), median (w=11), Kalman (q=0.01, r=4, where r is the noise variance sigma squared).
- Metrics: RMSE against the true signal (typical error), and lag (samples after the step until the output stays within 10% of the step size for 10 samples in a row).
- Stress tests: noise sigma from 0.5 to 8, 2% spikes of size 20, and 10% missing samples.
- Tuning: a sweep of the Kalman q value, plus a check that only the ratio q/r matters.
- Real-data check: a phone accelerometer recording (z-axis) resampled to 10 Hz. There is no ground truth, so no RMSE is reported for it.

## Results

| condition | filter | RMSE | lag (samples) |
|---|---|---|---|
| noise only (sigma=2) | Moving average (w=11) | 1.288 | 10 |
| noise only (sigma=2) | EMA (alpha=0.2) | 1.07 | 11 |
| noise only (sigma=2) | Median (w=11) | 1.459 | 6 |
| noise only (sigma=2) | Kalman (q=0.01, r=4) | 2.094 | 49 |
| spikes (2%, size 20) | Moving average (w=11) | 1.523 | 17 |
| spikes (2%, size 20) | EMA (alpha=0.2) | 1.406 | 14 |
| spikes (2%, size 20) | Median (w=11) | 1.47 | 7 |
| spikes (2%, size 20) | Kalman (q=0.01, r=4) | 2.227 | 50 |
| 10% dropouts | Moving average (w=11) | 1.305 | 10 |
| 10% dropouts | EMA (alpha=0.2) | 1.063 | 12 |
| 10% dropouts | Median (w=11) | 1.467 | 6 |
| 10% dropouts | Kalman (q=0.01, r=4) | 2.15 | 50 |

Lag is the number of samples the filter needs to settle after the step. "did not settle" means it never stayed inside the band.

![All filters, noise only](results/06_all_filters.png)
![Spikes](results/07_spikes.png)
![Missing samples](results/08_dropouts.png)
![RMSE as noise increases](results/09_rmse_vs_noise.png)
![Kalman q sweep](results/10_kalman_q_sweep.png)
![Error vs lag tradeoff](results/11_tradeoff.png)
![Real phone data](results/12_phone_data.png)

## Findings

FINDING 1: which filter had the lowest RMSE, and which had the shortest lag? Were they the same one?
FINDING 2: which filter handled spikes best, and why?
FINDING 3: what did missing samples do to the results, and why?
FINDING 4: what happened to the Kalman filter as q grew, and which q did you choose and why?
FINDING 5: did the phone data show the same noise-versus-lag pattern?

## Limitations

- The main data is simulated, and the signal has a single step, so it does not cover ramps, oscillations or drift.
- The 1D Kalman filter assumes the true value stays constant between samples, so it is a simplified version of what real systems use.
- One random seed was used for most runs, so small differences between filters may not be significant.
- The phone recording has no ground truth, is a single run, and was not recorded under controlled conditions.

## How to run

    pip install -r requirements.txt
    python3 main.py
    python3 step11_tune.py
    python3 step12_phone.py data/phone_accel.csv 3

Plots and tables are saved in the results folder.
