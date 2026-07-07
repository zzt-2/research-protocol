# PSA Spectral-Asymmetry FOE Baseline — B7-Q1 Sub-agent Summary

Probe: `_psa_foe_asymmetry.py` · artifacts: `_psa_foe_asymmetry_results.json`,
`_psa_foe_asymmetry_curve.png`. Scenario: 25 GBaud, RRC β=0.1, single-pol QPSK,
2 Sa/sym, OSNR 17 dB (and noiseless). Probe is **self-contained** (no
common/ imports, no params.py) to avoid parallel-write races.

## 1. Vieira 2023 formula extraction (C6 audit)

Source: `papers/doi/10.1109_access.2023.3287501/content.md`, cross-checked
against `papers/_read_notes/10.1109_ACCESS.2023.3287501.md`.

- **content.md L343**: "The coarse CFE algorithm is based on the asymmetry of
  the received spectrum upon high DSs. The DS is estimated as"
- **content.md L345**: `===> picture [162 x 25] intentionally omitted <==`
  — the *display* equation image is **lost** in the PDF→md conversion.
- **content.md L347** (prose fully recovers the structure):
  - "P+ is the power content on positive frequencies and P− ... negative"
  - "The ratio between P+ and P− provides an indication [of] the imprinted
    frequency shift."
  - "The logarithmic operation maps the result to the [−∞, ∞] range."
  - "The scaling factor α, which converts the resulting value to frequency,
    was obtained through a sequential search algorithm."
- Read-note L44 records the recovered closed form: **Δf̂ = α·ln(P+/P−)/2**.
- **α source**: Vieira reports α = 17 GHz at Rs = 32 GBaud, β = 0.1, found by
  sequential search over [15, 25] GHz minimizing mean error at Δf = 10 GHz
  subject to `|est−Δf| ≤ Rs/(2M)` covering [0, 10] GHz. **No closed form is
  given** — α is purely a fitted constant.

**Verdict: formula is NOT a downgrade.** Structure recovered from prose + the
read-note's recorded `/2` factor; the lost image is a display equation, not a
missing derivation. The only genuine gap is the *value* of α, which Vieira
itself obtains empirically — we reproduce that procedure by calibration
(§3 below), which is the faithful reading of the paper.

## 2. Core algorithm steps (per Vieira §VI + Fig. 6c)

| # | Step | Formula | Source |
|---|------|---------|--------|
| 1 | N-pt FFT of received samples | `FFT(rx)`, N=4096 (=2048 sym @2sp) | Vieira: N=1024 (=512 sym); scaled up for averaging |
| 2 | Power spectrum | `|FFT|²` (Hann window) | Vieira Fig.6c "power content" |
| 3 | Asymmetry indicator | `L = ln(P+/P−)/2`, P± = Σ over ±freq bins | content.md L347 prose |
| 4 | Frequency inversion | `Δf̂ = α · L` | content.md L347 + read-note L44 |
| 5 | Feed-forward compensation | `rx·exp(−j2πΔf̂t)` | Vieira "frequency compensation" stage |

## 3. Calibration of α (replaces Vieira's sequential search)

A naive closed-form guess α_guess = (1+β)·Rs/2 = 13.75 GHz is **wrong by
~14×** for this RRC spectrum (gives df_est=17.6 GHz at true f_D=1 GHz). The
ln(P+/P−) function is highly nonlinear in f_D because the RRC spectrum has
near-vertical edges, so the indicator saturates within ~1 GHz. We therefore
**calibrate** α by a 1-point slope fit at f_D = 1 GHz (noiseless),
faithfully reproducing Vieira's empirical-search procedure:
**α_calib = 0.953 GHz** (single-α, RRC β=0.1, 25 GBaud). This value is
reported in the JSON for audit.

## 4. Estimation-range results (f_D sweep 0–25 GHz)

Criteria: **A** = |Δf̂−f_D|>0.5 GHz (BER would blow up); **B** = |Δf̂|<0.3·f_D
(drift to zero, poster content.md L49).

**Noiseless (OSNR=∞):**
| f_D | Δf̂ | |err| | A | B |
|----:|-----:|-----:|---|---|
| 1 GHz | 1.000 | 0.000 | OK | — |
| 5 GHz | 1.220 | 3.780 | **FAIL** | **FAIL** |
| 12 GHz | 2.435 | 9.565 | **FAIL** | **FAIL** |
| 13 GHz | 2.429 | 10.571 | **FAIL** | **FAIL** (peak, then folds) |
| 15 GHz | 1.772 | 13.228 | **FAIL** | **FAIL** |
| 24 GHz | 1.000 | 23.000 | **FAIL** | **FAIL** (mirrors f_D=1) |
| 25 GHz | −0.534 | 25.534 | **FAIL** | sign flip (cross Nyquist) |

**OSNR 17 dB:** essentially identical (f_D=1 → 0.962 err 0.038 OK; f_D=5 →
1.167 failA+failB; f_D=12 → 1.970 failA+failB). Noise is not the limiter —
the **nonlinearity/aliasing of the indicator is**.

**Key numbers (mainline V5 independent re-check):**
- f_D=5 GHz → Δf̂ = **1.22 GHz** (noiseless) / **1.17 GHz** (OSNR17)
- f_D=12 GHz → Δf̂ = **2.44 GHz** / **1.97 GHz**
- f_D=15 GHz → Δf̂ = **1.77 GHz** / **1.61 GHz** → **drifts to zero (failB)**

## 5. Interpretation

- **Linear region is ~1 GHz, far below the claimed half-baud 12.5 GHz.** A
  single-α spectral-asymmetry estimator on a sharp-edge (low-β) RRC spectrum
  saturates almost immediately; the theoretical "≤ half baud rate" bound is an
  *aliasing* bound, not a *linearity* bound. Above ~13 GHz the estimate
  **folds back** (f_D and 25−f_D give the same Δf̂), and at 25 GHz it flips
  sign — classic Nyquist aliasing of the power spectrum.
- **This is consistent with the B7 poster's stated limitation** (content.md
  L19: "typically confined to a narrow estimation range—usually within half
  the baud rate"; L49: FOE output drifts toward zero). Our measurement shows
  the *practical* usable range is even narrower (~1 GHz at this β) than the
  half-baud aliasing ceiling.
- Vieira's much wider [0, 10 GHz] coverage at 32 GBaud is **not reproducible
  with a single α** at 25 GBaud/β=0.1. The likely difference: Vieira's α=17 GHz
  plus their fine M-th-power stage jointly cover the range; the **coarse stage
  alone has a narrow linear region**, and Vieira relies on the fine stage to
  clean up residuals. Our probe implements **only the coarse PSA stage** (the
  true B7 baseline per the task spec) — the residual-coverage gain from a fine
  stage is a candidate-improvement axis, not part of this baseline.

## 6. Red-flag / B7-vs-Gardner-1986 alert

**No BER comparison was run** (out of scope for this probe). No direct
evidence of a B7-vs-Gardner-1986 BER gap <0.1 dB surfaced. The only
abnormality is that the **single-α PSA baseline fails criterion A for all
f_D ≥ 2 GHz** — meaning the coarse-stage-alone baseline is *very* weak at
25 GBaud, which would make any Gardner-TED-reused candidate look strong by
comparison. The mainline should ensure the **fair-comparison framework**
(_fair_comparison_framework.md §3.1) applies the same α-calibration and
includes the fine CFE stage (or its equivalent) on *both* sides before drawing
BER-gap conclusions.

## 7. Honest caveats

1. The display equation image (content.md L345) is lost; the `/2` factor is
   taken from the structured read-note (L44), not re-derived from the PDF.
2. α is fitted, not analytical — exactly as in Vieira. Our 1-point fit
   differs from Vieira's multi-point search; a multi-α or piecewise-linear
   inversion would widen the linear region but is *not* what a single-α
   baseline does.
3. The probe does **not** reuse `common/_recovery.py:435 psa_foe_recovery`
   (confirmed pilot-aided differential-phase, wrong concept — D004).
   No common/ files were modified.
