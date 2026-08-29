# Ch4 gated-RDE correctness seam

Status: `CORRECTNESS_ONLY / NO_METHOD_SIGNAL`.

This isolated seam implements four arms after one shared finite-pilot 2x2 LS
initialization: plain RDE, native-ring-residual cheap gate, the two-evidence
hard-gated candidate v1, and a truth-bearing oracle used only as a correctness
ceiling. The three deployable arm signatures do not accept transmitted
symbols, true Jones matrices, true SNR, or BER.

All four arms select their update target with the canonical receiver-visible
nearest-radius criterion `argmin_m ||z|^2-r_m^2|`. The cheap gate uses the
corresponding native RDE ring residual. The candidate gate remains distinct:
its ring feature is the residual to the ring of the nearest constellation
point, paired with nearest-point decision distance.

## Formula authority

T056 independently verified Di Rosa and Richter, JLT 2021, Section II-A,
Eq. (1)--(3), together with the Ready--Gooch nearest-radius criterion and a
row-convention derivation. Under this seam's convention `z = W @ y`, the
frozen transcription is:

`W_i <- W_i + mu * g_i * z_i * (R_i^2 - |z_i|^2) * y.conj()`.

The update sign, conjugation, dimensions, and nearest-radius selection are
pinned by literal complex-number and nearest-point/radius divergence tests.

## Commands

From the repository root:

```text
python -m pytest projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py -q
python projects/simulation/explore/ch4-apsk-ring-gated-rde/run_smoke.py
git diff --check
```

`run_smoke.py` executes exactly three preregistered correctness cells:
identity/noiseless, random-J/noiseless, and one 30 dB cell. It does not scan
SNR, pilot count, thresholds, or update step and does not compute a BER-based
method verdict.
