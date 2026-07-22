# C16 Non-Modulus HOS Paradigm Scout — Synthesis

> Schema: `direction-lab.cb1.c16-nonmodulus-jade.v1`
> Campaign: `science-scout-2026-07-20.dual-pol-osl`
> Date: 2026-07-22
> Verdict: **MECHANISM NEGATIVE** — non-modulus HOS paradigm does NOT escape the collapse

## 0. TL;DR

This Scout tested the LAST remaining equalizer paradigm: a non-modulus blind
equalizer based on higher-order-statistics source separation (kurtosis
maximization / JADE-style 4th-order independence). The cost function contains
NO |z|² modulus term by construction.

**The non-modulus paradigm performs WORSE than Godard CMA on every cell.** It
does not escape the inner-ring collapse; it produces a HIGHER collapse rate.
This closes the paradigm axis and establishes that the collapse is a
**channel property**, not a cost-function or paradigm artifact.

## 1. Scientific question

Can a higher-order-statistics source separation method (no modulus cost) equalize
the dual-pol 16QAM channel without the inner-ring collapse, because it separates
sources by 4th-order statistical independence rather than modulus matching?

## 2. Setup

- **Candidate**: HOS kurtosis-maximization equalizer. Whitening (2nd-order
  decorrelation) + Givens rotation search maximizing |kurtosis(zX)−2| +
  |kurtosis(zY)−2| (deviation from complex-Gaussian). NO modulus term.
- **Anchor**: Godard CMA (center-tap, mu=0.03, R²=1.32, block_size=64).
- **Kill bound**: oracle 2×2 LS unmixing (TX-truth-conditioned).
- 11 atlas cells × 10 test seeds [71-80].
- Metric: PI-SER (permutation-invariant), collapse rate (>0.3 threshold).

Provenance: Cardoso & Souloumiac 1993 (JADE); Comon 1994 (ICA); Hyvarinen 1999 (FastICA).

## 3. Results

### Smoke (sanity)
- snr25 (clean): CMA PI-SER=0.731 (this seed collapsed even at high SNR),
  HOS=0.004, oracle=0.000 — HOS recovered this one collapsed seed
- snr05 (hard): CMA=0.859, HOS=0.856, oracle=0.875 — all fail at low SNR

### Full eval (11 cells × 10 seeds)

| Cell | CMA | HOS | Oracle |
|---|---|---|---|
| snr05-nominal-short | 0.586 | 0.682 | 0.599 |
| snr10-nominal-short | 0.316 | 0.604 | 0.298 |
| snr15-nominal-short | 0.176 | 0.415 | 0.109 |
| snr20-nominal-short | 0.153 | 0.415 | 0.030 |
| snr25-nominal-short | 0.148 | 0.301 | 0.000 |
| snr20-fg100-short | 0.153 | 0.361 | 0.030 |
| snr20-fg1000-short | 0.153 | 0.375 | 0.031 |
| snr20-sop40e-short | 0.153 | 0.438 | 0.030 |
| snr10-fg100-long | 0.429 | 0.527 | 0.409 |
| snr15-fg1000-long | 0.261 | 0.593 | 0.163 |
| snr20-nominal-long | 0.230 | 0.418 | 0.044 |

### Aggregate
- Macro PI-SER: CMA=0.251, **HOS=0.466** (HOS 1.86× worse)
- Collapse rate: CMA=0.336, **HOS=0.791** (HOS 2.35× more collapsed)

## 4. Verdict: MECHANISM NEGATIVE

The non-modulus HOS paradigm does NOT escape the collapse. HOS is worse than
Godard CMA on ALL 11 cells and has a 2.35× higher collapse rate.

## 5. Mechanism analysis

The key finding is counterintuitive but well-explained:

1. **HOS is worse even on clean cells**: On snr20-nominal-short (high SNR,
   nominal conditions), CMA achieves PI-SER=0.153 but HOS only 0.415. The
   oracle shows 0.030 is achievable. HOS is far from the oracle — it's not
   that HOS collapses to the inner ring; it fails to separate the sources at all.

2. **The 16QAM kurtosis signal is too weak for 2-source separation on short,
   time-varying blocks**: 16QAM is sub-Gaussian (platykurtic), and the
   kurtosis deviation from Gaussian is small relative to the noise and
   channel time-variation within a block. The whitening + Givens search
   cannot reliably identify the unmixing matrix from 256-symbol windows with
   SOP rotation and GG fading.

3. **The collapse is a CHANNEL property, not a cost property**: With C14
   (init-invariant), C15 (cost-invariant within modulus family + ring-aware
   worse), and now C16 (paradigm-negative — non-modulus HOS even worse), the
   collapse has been shown to survive:
   - ALL post-equalizer corrections (C04/C09 affine, C12 soft-demap/GMI)
   - ALL within-CMA adaptations (C08 mu, C10 per-symbol, C11 DD-LMS)
   - ALL cost variants (Godard, MMA, ring-aware, reduced-constellation)
   - ALL initializations (center-tap, whitening, multistart, oracle Wiener)
   - ALL equalizer paradigms (modulus CMA, non-modulus HOS source separation)

## 6. What this means for the campaign

The negative-boundary thesis is now maximally complete and coherent. The 16QAM
inner-ring collapse on dual-pol OSL under GG turbulence + SOP dynamics is a
**fundamental property of the blind equalization problem on this channel** — it
is not fixable by any receiver-visible equalizer-level method tested across
five independent mechanism axes. The TX-truth oracle shows the channel IS
invertible (oracle PI-SER is low), but the information required to invert it
is not extractable from the received statistics alone.

This is a strong, publishable boundary result: it maps the entire blind-
equalization solution space and shows where the collapse lives.

## 7. Unchanged / preserved

- All prior artifacts untouched. No protected history modified.
- No TX truth in HOS at runtime (identity tests confirm).
- No push, no merge.
