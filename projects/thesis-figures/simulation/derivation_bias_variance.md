# Bias-Variance Optimal FOE Window: Derivation

## Problem

The noise-only FOE window formula N_opt = 80 / (gamma_bar * h^2) gives N < 1 for h > 0.3
at 20 dB SNR, which is absurdly small. The root cause is that it only considers noise,
ignoring Doppler dynamics which penalize long windows.

We need a formula that balances two impairments:
1. **Noise** — longer window helps (variance decreases as N^{-3})
2. **Doppler dynamics** — shorter window helps (frequency drifts, bias increases as N^2)

## Signal Model

Carrier phase at symbol k:

```
phi(k) = 2*pi*f_res*k*T_s + pi*f_dot*(k*T_s)^2 + theta_laser(k)
```

The instantaneous frequency in rad/symbol:

```
omega(k) = 2*pi*f_res*T_s + 2*pi*f_dot*T_s^2 * k
```

Over N symbols, the frequency changes by:

```
delta_omega = 2*pi*f_dot*T_s^2 * N
```

## MSE Model

Total estimation error MSE = Bias^2 + Variance.

### Bias Term

For a linear frequency ramp (Doppler rate), the FFT-based 4th-power estimator
measures the average frequency over the N-symbol window. The instantaneous
frequency at symbol k within the window is:

```
omega(k) = omega_0 + beta*k,  where beta = 2*pi*f_dot*T_s^2
```

The FFT peak corresponds to the average frequency, but the frequency spread
across the window causes spectral broadening. The effective bias squared is
proportional to the variance of the frequency over the window:

```
Bias^2 = Var[omega(k)] for k in [0, N-1]
       = beta^2 * N^2 / 12
       = (2*pi*f_dot*T_s^2)^2 * N^2 / 12
       = (pi*f_dot*T_s^2)^2 * N^2 / 3
```

### Variance Term

For the FFT 4th-power frequency estimator (Mengali et al.), the variance is:

```
Var(f_hat) = 6 / (pi^2 * N^3 * gamma)
```

where gamma = gamma_bar * h is the effective SNR.

This is a well-established result for the modified Cramer-Rao bound (MCRB)
of frequency estimation with raised-power estimators.

### Full MSE

```
MSE(N) = (pi*f_dot*T_s^2)^2 * N^2 / 3 + 6 / (pi^2 * N^3 * gamma)
```

## Optimization

Setting dMSE/dN = 0:

```
dMSE/dN = 2*(pi*f_dot*T_s^2)^2 * N / 3 - 18 / (pi^2 * N^4 * gamma) = 0
```

Solving for N:

```
N^5 = 27 / (pi^4 * (f_dot * T_s^2)^2 * gamma)

N_opt = (27 / (pi^4 * (f_dot * T_s^2)^2 * gamma_bar * h))^{1/5}
```

### Key Properties

1. **Scaling**: N_opt ~ h^{-1/5}, a very weak dependence on channel gain.
   Unlike the noise-only formula (h^{-2}), this does NOT diverge for small h.

2. **At the balance point**, bias^2 and variance contribute equally (3:2 ratio):
   - Bias^2 = (2/5) * MSE_opt
   - Variance = (3/5) * MSE_opt

3. **Dominant factor**: At LEO FSO parameters, noise dominates over dynamics.
   The optimal window is large (~5000-8000 symbols), consistent with the
   observation that Doppler frequency change over 1024 symbols is only ~61 Hz.

## Numerical Evaluation

Parameters:
- f_dot = 150 MHz/s (low elevation)
- T_s = 0.4 ns (2.5 Gsps)
- gamma_bar = 100 (20 dB SNR)
- alpha = 27 / (pi^4 * (f_dot*T_s^2)^2 * gamma_bar) = 4.812e18

```
N_opt(h) = (4.812e18 / h)^{1/5}
```

| h   | gamma | N_opt (raw) | N_opt (clip 256-8192) | N_opt (pow2) | Bias^2        | Variance      | MSE           |
|-----|-------|-------------|----------------------|--------------|---------------|---------------|---------------|
| 0.1 | 10    | 8639        | 8192                 | 8192         | 1.41e-13      | 9.43e-14      | 2.36e-13      |
| 0.3 | 30    | 6935        | 6934                 | 8192         | 9.11e-14      | 6.08e-14      | 1.52e-13      |
| 0.5 | 50    | 6261        | 6261                 | 8192         | 7.43e-14      | 4.95e-14      | 1.24e-13      |
| 0.7 | 70    | 5854        | 5853                 | 8192         | 6.49e-14      | 4.33e-14      | 1.08e-13      |
| 1.0 | 100   | 5451        | 5450                 | 8192         | 5.63e-14      | 3.75e-14      | 9.38e-14      |
| 1.5 | 150   | 5026        | 5026                 | 8192         | 4.79e-14      | 3.19e-14      | 7.98e-14      |
| 2.0 | 200   | 4745        | 4745                 | 8192         | 4.27e-14      | 2.84e-14      | 7.11e-14      |
| 3.0 | 300   | 4376        | 4375                 | 8192         | 3.63e-14      | 2.42e-14      | 6.05e-14      |

Units: Bias^2, Variance, MSE in (rad/symbol)^2.

## Comparison with Old Formula

| h   | N_old = 80/(gamma_bar*h^2) | N_new (bias-variance) | Ratio |
|-----|----------------------------|-----------------------|-------|
| 0.1 | 80                         | 8639                  | 108x  |
| 0.3 | 8.9                        | 6935                  | 780x  |
| 0.5 | 3.2                        | 6261                  | 1957x |
| 0.7 | 1.6                        | 5854                  | 3590x |
| 1.0 | 0.8                        | 5451                  | 6814x |

The old formula is catastrophically wrong because it has N ~ h^{-2} while the
correct scaling is N ~ h^{-1/5}. At h=1 the old formula gives N<1 (meaningless),
while the new formula gives N~5450 (physically sensible, close to Zhao's 1024).

## Physical Interpretation

The Doppler-induced frequency change over N symbols:

```
delta_f = f_dot * T_s * N
```

For N=8192 (maximum): delta_f = 150e6 * 0.4e-9 * 8192 = 492 Hz
For N=1024 (Zhao fixed): delta_f = 61 Hz

Both are negligible compared to the 1 MHz residual frequency offset that must be
estimated. This confirms that **noise is the dominant impairment** at these
parameters, and the optimal strategy is to use as large a window as possible
within the clipping bound.

The h^{-1/5} scaling means the adaptive window varies only weakly with channel
conditions: from 8192 at h=0.1 to 4375 at h=3.0 (less than 2x variation).
This is qualitatively different from the old h^{-2} formula which predicted
extreme sensitivity to channel gain.

## Simulation Verification

Running 6 scenarios x 30 trials x 10000 symbols (VV/DPLL fixed, only FOE window varies):

```
Strategy              | BV gain vs fixed | Old gain vs fixed
weak_low  (150 MHz/s) | ~0.00 dB         | ~0.00 dB
weak_high (30 MHz/s)  | ~0.00 dB         | ~0.00 dB
mod_low  (150 MHz/s)  | +0.02 dB         | ~0.00 dB
mod_high (30 MHz/s)   | +0.02 dB         | ~0.00 dB
strong_low  (150 MHz/s)| ~0.00 dB        | +0.09 dB
strong_high (30 MHz/s) | ~0.00 dB        | +0.09 dB
```

**Conclusion**: Both adaptive FOE formulas show minimal (<0.1 dB) improvement over
fixed N=1024. The bias-variance formula is physically correct but the improvement
is negligible because noise dominates at these parameters.

This is the expected result: with f_dot*T_s = 6e-2 Hz/symbol, even 8192 symbols
produce only 492 Hz of frequency drift -- negligible vs the 1 MHz residual offset.
The FOE window is NOT the bottleneck; the carrier recovery chain is limited by
other components (VV averaging window, DPLL tracking bandwidth).

**Implication**: FOE window adaptation is NOT a productive axis for innovation
in LEO FSO carrier synchronization. Fixed N=1024 (or any value 512-8192) works
equally well. Future work should focus on VV and DPLL adaptation instead.

## Implementation

```python
def adaptive_params_bv(h_est, gamma_bar_db=20, f_dot=150e6, T_s=0.4e-9):
    gamma_bar = 10**(gamma_bar_db / 10)
    h_safe = max(h_est, 0.001)
    alpha = 27 / (np.pi**4 * (f_dot * T_s**2)**2 * gamma_bar)
    N_opt = (alpha / h_safe)**(1/5)
    # Clip to practical range and round to power of 2
    N_fft = int(np.clip(N_opt, 256, 8192))
    N_fft = int(2**np.ceil(np.log2(N_fft)))
    return N_fft
```
