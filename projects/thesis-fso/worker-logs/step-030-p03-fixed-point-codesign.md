# step-030 — P03 Fixed-Point / Resource-Performance Co-Design (Independent Executor)

> Task: T031-p03-fixed-point-resource-codesign (Package P03, family B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN)
> Source: S003 / D040 campaign authorization; brief at
> `.sessions/2026-07-23-research-direction-lab-longitudinal-test/T031-p03-fixed-point-resource-codesign.md`
> Worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Python (anchor-provenance 3.11.9): `/c/Users/zzt/scoop/apps/python311/current/python`
> Date: 2026-07-30
> TERMINAL VERDICT: **PROBLEM_RESOLVED_BY_UNIFORM_PRECISION** (a genuine bit-true Q(W,F)
> model reproduces the frozen float selector byte-exact under bypass; uniform precision
> at (8,6)–(14,12) already sits at the regret floor; the residual regret is a
> branch-statistical boundary phenomenon, NOT a quantization artifact. Phase B/C: one
> mixed candidate (`two_exp`) lands on the Pareto front and Pareto-dominates the uniform
> comparator, but its regret advantage is +0.017 dB — 9× below the frozen MDE 0.15 dB —
> so it is NOT a real method signal. Fixed-point is not the bottleneck of this selector.)

## 0. Mission recap

P03 asks whether the already-closed DA/NDA CPR selector (`_a4_switch_common768_30seed.decide`,
family A) suffers a **real resource-performance tension** when deployed in fixed-point:
does uniform bitwidth either waste resource or harm branch selection, and if so can a
sensitivity-aware mixed-precision datapath beat it? This is a PREFORMAL_METHOD_FACTORY
engineering-diagnosis package on the selector CONTROL PATH only — branch outputs (DA/NDA
common-768 errors) are the FROZEN per-window errors from `run_case_multidelta`; BER is
never recomputed.

## 1. CRITERION FREEZE — written BEFORE any test data (brief trap #9)

**Float-bypass identity (gate 1, BLOCKER if fail):** `decide_fp(W=64,F=40)` must equal
`A.decide` byte-exact (per-window decision) on dev seeds 0–9 across the full anchor grid
{weak,moderate,strong} × range(5,26,2) dB = 33 cells × 10 seeds × 400 windows. Pass bar =
0 mismatches. A single mismatch → `BLOCKED_NO_BITTRUE_MODEL`, stop.

**Bit-true contract (gates 2–4):** explicit saturating two's-complement Q(W,F),
round-half-up (ties→+inf), block-floating-point per-window shared exponent, accumulator
widened by ceil(log2(N))+2 guard. No `np.round(decimals=)` fake fixed-point. Saturation
must not wrap.

**Info boundary (gate 5, BLOCKER if fail):** AST-audit `decide_fp` source — no
true_snr/true_h/true_phi/tx_sym/tx_bits/oracle/labels; signature consumes only
(raw, gamma_db, gamma_lin, W, F).

**Uniform-tension definition (decides whether Phase B runs):** a "clear resource-performance
tension" exists iff widening the datapath across the frozen ladder reduces mean wrong-branch
regret by ≥ MDE AND the reduction is monotone/attributable to quantization (not a
branch-statistical floor that persists at the widest width where float-bypass proves
quantization is negligible). Concretely: if regret at (16,14) — where bypass proves Q-error
is ≤ 2^-40 — is still ≥ MDE above the float reference at gain-bearing cells, the floor is
branch-statistical and NOT a bitwidth tension.

**Mixed-precision success bar (frozen MDE = 0.15 dB, same as P01/P02):** a mixed candidate
"really" beats uniform iff it Pareto-dominates the dev-chosen uniform point by ≥ MDE on
regret at lower op×bit_proxy OR storage_bit_proxy, on fresh held-out seeds 30–49.

**Seed isolation (frozen):**
- Phase A dev = seeds 0–9 (anchor subset; range-finding + uniform ladder).
- Phase B dev-tuning = seeds 10–19 (disjoint from 0–9 AND from held-out — chosen because
  P03's estimand is a bitwidth CONFIG, but to be conservative and fully disjoint from the
  Phase-A range-finding set and the held-out set, per brief §3.4 fallback).
- Fresh held-out test = seeds 30–49 (P01's set; P03 estimand is a bitwidth config not a
  gain fit → no leakage, brief §3.4).
- Pollution seeds 71–80 FORBIDDEN. dev ≠ held-out throughout.

## 2. Bit-true model — `_p03_fixed_point.py` (Q-format contract + smoke result)

Implements the brief §2.2 contract item-by-item:
- `quantize(value, W, F, signed, mode='half_up')`: `raw = floor(value*2^F + 0.5)`, saturate
  to signed `[−2^(W-1), 2^(W-1)−1]` / unsigned `[0, 2^W−1]`. Returns the held int code.
- float-bypass: `quantize(x,64,40)` error ≤ 2^-40 (measured 3.4e-14).
- `block_float_normalise`: ONE shared window exponent `e=floor(log2(max|rx|^2))`,
  mantissa `pwr/2^e ∈ [0,2)` quantised unsigned Q(W,F); mean via exact integer accumulator
  (W_acc = W+ceil(log2(N))+2) then divide-by-n; cv scale-invariant under shared exponent.
- Non-linear ops (sqrt/std, log10, div): float-evaluated BUT input operands quantised
  before, output quantised after — LUT I/O-width model (no free-precision op).
- LUT coefficients (cv_thr=cv_awgn_theory(γ)*1.10, noise_sub=1/(2γ_lin)) precomputed &
  quantised per call.
- `decide_fp(raw, gamma_db, gamma_lin, W, F)` mirrors `A.decide` stage-1 (CV) + stage-2
  (γ_eff) with every data-dependent op quantised.

**Smoke result (`_p03_smoke_check.py`, all 5 gates PASS, 220 s):**
- Gate 1 float-bypass: **0 / 132,000 per-window mismatches** (33 cells = 3 scenes ×
  gamma_db∈{5..25 step 2} = 11 SNR × 10 dev seeds × 400 windows/cell). Byte-exact to `A.decide`.
  [In-package deterministic fix: original prose mis-stated the denominator as 726,000 implying
  2200 windows/cell; the correct frozen N_WINDOWS=400 gives 132,000. Substance (0 mismatches)
  unchanged — independent verifier re-ran the gate and confirmed 0 mismatches.]
- Gate 2 edge/zero/saturation: all-zero, constant-mag, spike, huge-mag, threshold-adjacent
  (γ_eff=13.05), unsigned & signed saturation (no wrap) — all match `A.decide` / saturate.
- Gate 3 rounding: +/−0.5 LSB ties→+inf, below/above-half, in-range reconstruction ≤ 0.5 LSB,
  float-bypass quantize err 3.4e-14 — all OK.
- Gate 4 determinism: same input twice byte-identical at (6,4),(10,8),(16,14),(64,40); array
  quantise deterministic.
- Gate 5 info-boundary AST: signature `decide_fp(raw, gamma_db, gamma_lin, W, F)` clean;
  zero forbidden-substring leaks in body.

## 3. Phase A — uniform-precision baseline (`_p03_phaseA.py`, dev 0–9)

Grid: 3 scenes × 11 SNR (5..25 dB step 2) × 10 dev seeds = 330 cells; all 6 frozen widths
{(6,4),(8,6),(10,8),(12,10),(14,12),(16,14)} + float bypass (64,40) evaluated in ONE channel
pass per cell (paired). δ=0 only. 2310 raw rows; aggregates independently recomputed from
raw_rows (regret identity `10log10(fp_sel/bypass_sel)` holds on every row).

Pooled Pareto (dev 0–9, 330 cells):
| bitwidth | regret_dB | [CI95] | overflow% | op×bit_proxy | storage_proxy | W_acc |
|---|---|---|---|---|---|---|
| (6,4)  | +0.23900 | [+0.2004,+0.2776] | 0.0939 | 264  | 1658 | 16 |
| (8,6)  | +0.20050 | [+0.1621,+0.2389] | 0.1394 | 332  | 2198 | 18 |
| (10,8) | +0.19676 | [+0.1588,+0.2347] | 0.1545 | 400  | 2738 | 20 |
| (12,10)| +0.19648 | [+0.1586,+0.2343] | 0.1606 | 468  | 3278 | 22 |
| (14,12)| +0.19613 | [+0.1583,+0.2340] | 0.1629 | 536  | 3818 | 24 |
| (16,14)| +0.19583 | [+0.1580,+0.2337] | 0.1629 | 604  | 4358 | 26 |

**All 6 widths are Pareto-optimal** (each step lowers regret slightly at more resource),
but the frontier is nearly flat: regret (6,4)→(16,14) drops only **0.0432 dB over a 2.3×
op×bit / 2.6× storage increase**, and (8,6)→(16,14) drops only **0.0047 dB** (32× below MDE).

**The regret floor is branch-statistical, NOT quantization.** At (16,14) — where float-bypass
proves Q-error ≤ 2^-40 — the per-cell regret at high-SNR cells is large and persistent
(moderate@25=+0.685 dB, strong@25=+0.806 dB) while agreement there is only ~10–13%. Those
flips are intrinsic to the CV/γ_eff boundary (DA and NDA have comparable error), not
fixable by more bits. Overflow is tiny (<0.3%) and HIGHER at low SNR (where it causes no
regret) than high SNR — overflow is not the driver.

**Gain-bearing subset** (weak/mod/strong × {5,7,9,11,13} dB, where the anchor's +0.8..+1.5 dB
gain lives): regret (8,6)=+0.027 dB, (16,14)=+0.022 dB, (6,4)=+0.107 dB — all **well below
MDE 0.15** at (8,6)+. The pooled ~0.196 dB is dominated by high-SNR cells where the anchor
gain itself collapses to ~0.

**Best uniform point:** (8,6) — the knee. Pooled regret +0.2005 dB (driven by high-SNR
boundary noise); on the gain-bearing region it is +0.027 dB. Past (8,6), 2× more resource
buys <0.005 dB.

## 4. Phase B/C — mixed-precision candidates + fair comparison (`_p03_phaseBC.py`)

_RUN DESPITE the weak pooled tension_, to make the verdict ironclad: the only honest way
to confirm "no mixed candidate can beat the floor by a real margin" is to run them. Four
mechanism-distinct candidates (each a different deployable bit-allocation / scaling action),
dev-tuned on seeds 10–19 (disjoint), final comparison on fresh held-out 30–49. All 21 dev
configs + the 6-rung uniform ladder + bypass are BATCHED into ONE channel pass per cell
(strongly paired, channel-identical). 6930 dev rows + 7260 held-out rows; regret identity
`10log10(fp_sel/bypass_sel)` verified on all rows.

Dev-tune (seeds 10–19) chosen configs (min mean regret, tie→min op×bit):
- uniform → **(14,12)** regret +0.17853 dB, op×bit=536
- stage_widths → **cv(8,6)/s2(12,10)** regret +0.16114 dB, op×bit=776
- two_exp → **(8,6)** regret +0.16114 dB, op×bit=348 (same regret as stage_widths at <half the op×bit)
- boundary_adaptive → **n(8,6)/w(14,12)** regret +0.18297 dB, op×bit=868
- narrow_acc → **(12,10)** regret +0.17856 dB, op×bit=468

Held-out (seeds 30–49, 660 cells paired):
| method | mechanism | regret_dB | [CI95] | agree% | op×bit | storage | Pareto |
|---|---|---|---|---|---|---|---|
| uniform_14_12 (comparator) | uniform       | +0.18953 | [+0.1618,+0.2173] | 56.09 | 536 | 3818 | no |
| stage_widths_8_6_12_10     | stage_widths | +0.17292 | [+0.1439,+0.2019] | 50.49 | 776 | 3222 | no |
| **two_exp_8_6**            | two_exp      | +0.17292 | [+0.1439,+0.2019] | 50.49 | **348** | 2206 | **YES** |
| boundary_8_6_14_12         | boundary_adv | +0.19177 | [+0.1640,+0.2195] | 54.99 | 868 | 6016 | no |
| narrow_acc_12_10           | narrow_acc   | +0.18956 | [+0.1618,+0.2173] | 55.83 | 468 | 3272 | no |

**Pareto front = {`two_exp_8_6`}** (sole point). `two_exp(8,6)` Pareto-dominates the uniform
comparator (lower regret +0.1729 vs +0.1895 AND lower op×bit 348 vs 536) AND dominates
`stage_widths` (same regret, half the op×bit). The mechanism: stage-2 normalises by the
MEAN power (its own exponent) instead of the MAX, giving full fraction resolution where the
noise-subtraction `1/(2γ)` is sensitive — this is the one candidate that touches the actual
stage-2 dynamic-range tension the brief hypothesised.

## 5. Fair comparison + ablation

**Pareto dominance vs uniform:** `mixed_pareto_dominates_uniform = [stage_widths, two_exp]`.
**BUT `mixed_strictly_better_by_mde = []`** — the regret advantage of the best mixed
(`two_exp`) over the uniform comparator is **+0.0166 dB, 9× below the frozen MDE 0.15 dB**.
So while `two_exp` is nominally on the Pareto front, its edge is sub-MDE — not a real
method signal, just the branch-statistical floor wobbling.

**Ablation (mixed vs uniform at the closest op×bit budget — controls total bit budget):**
| mixed method | mixed regret | uniform@same budget | Δ (mixed − uniform) |
|---|---|---|---|
| two_exp(8,6)        | +0.17292 | uniform(8,6) +0.19664 @ op×bit=332 | **−0.0237 dB** |
| stage_widths(8,6,12,10) | +0.17292 | uniform(16,14) +0.19001 @ op×bit=604 | −0.0171 dB |
| boundary(8,6,14,12) | +0.19177 | uniform(16,14) +0.19001 @ op×bit=604 | +0.0018 dB |
| narrow_acc(12,10)   | +0.18956 | uniform(12,10) +0.18956 @ op×bit=468 | +0.0000 dB |

The cleanest control is `two_exp(8,6)` vs `uniform(8,6)` at the SAME width (op×bit 348 vs
332): the per-stage exponent buys **−0.024 dB** — real in sign, consistent across dev and
held-out, but an order of magnitude below MDE. `boundary_adaptive` and `narrow_acc` give
zero edge (their mechanism does not touch the stage-2 dynamic range).

**Held-out uniform ladder** (confirms the floor): regret plateaus at +0.1895 dB from (12,10)
onward; (16,14) is +0.1900 (slightly WORSE than (14,12) — pure boundary noise). The floor is
flat past (10,8), confirming width cannot break it.

**Ablation conclusion:** the only mechanism with a consistent (sign-correct, dev+held-out
stable) edge is stage-2 mean-normalisation (`two_exp`), and it is sub-MDE. No mixed
candidate crosses the frozen 0.15 dB bar. The brief's hypothesised stage-2 high-SNR
noise-subtraction tension IS weakly real (two_exp's sign confirms it), but it is far too
small to motivate a deployable mixed-precision method over a uniform (8,6) datapath.

## 6. Terminal verdict + rationale

**PROBLEM_RESOLVED_BY_UNIFORM_PRECISION.**

Rationale (consistent with the numbers):
1. Bit-true model is trustworthy: float-bypass byte-exact (0/132k), Q-format contract
   fully implemented and smoke-tested (incl. the 4 mixed-candidate paths at wide widths).
2. No real resource-performance tension in uniform: regret is width-flat past (8,6)
   ((8,6)→(16,14) = 0.0047 dB over 1.82× resource; 32× below MDE). On the gain-bearing
   region (where the selector delivers its anchor gain), regret at (8,6)+ is ≤ 0.027 dB,
   far under MDE 0.15.
3. The residual pooled regret (~0.19 dB) is a branch-statistical boundary floor — it
   persists undiminished at (16,14) where quantization is provably negligible, and is
   concentrated at high-SNR cells where the anchor gain itself is ~0.
4. Phase B/C confirms mixed precision cannot break the floor by a real margin: the best
   mixed candidate (`two_exp(8,6)`) IS on the Pareto front and Pareto-dominates the
   uniform comparator, but its regret advantage is **+0.0166 dB — 9× below MDE 0.15**.
   `mixed_strictly_better_by_mde = []`. The brief's hypothesised stage-2 noise-subtraction
   tension is weakly real (two_exp's sign is correct and dev/held-out-stable: −0.024 dB
   vs uniform(8,6) at equal width) but an order of magnitude too small to motivate a
   deployable mixed-precision method.
5. No METHOD_SIGNAL / method card: no deployable mixed-precision lever stably beats a
   uniform datapath by the frozen MDE. Engineering finding: **deploy uniform (8,6) [or
   (12,10)–(14,12) for headroom] — fixed-point quantization is NOT the bottleneck of this
   selector; the residual wrong-branch regret is intrinsic to the CV/γ_eff boundary.**

## 7. Key numbers (for controller relay)

- Verdict: `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`.
- Float-bypass identity: **0 / 132,000** per-window mismatch (byte-exact to `A.decide`).
- Best uniform point: **(8,6)** (the knee) — dev pooled regret +0.2005 dB [CI +0.162,+0.239];
  on the gain-bearing region (weak/mod/strong ×{5,7,9,11,13} dB) +0.027 dB [CI +0.011,+0.044];
  overflow 0.14%; op×bit_proxy=332, storage_proxy=2198, W_acc=18. Uniform regret plateaus
  at +0.1895 dB from (12,10) on held-out (floor).
- Tension: absent at MDE — (8,6)→(16,14) regret delta = **0.0047 dB** (32× below MDE) for
  1.82× op×bit. Floor is branch-statistical (persists at (16,14) where Q-error ≤ 2^-40;
  concentrated at high-SNR cells where anchor gain ≈ 0).
- Phase B/C best mixed: **`two_exp(8,6)`** — held-out regret +0.1729 dB [CI +0.144,+0.202],
  op×bit_proxy=348, storage_proxy=2206; **sole Pareto-front point**; Pareto-dominates
  uniform comparator (14,12). Advantage over uniform = **+0.0166 dB (9× below MDE 0.15)**.
  Ablation vs uniform(8,6) at equal width: −0.024 dB (sign-correct, sub-MDE).
- METHOD_SIGNAL / method card: **NO** (no mixed lever beats uniform by the frozen MDE;
  two_exp's sub-MDE edge is noted as a weak hint, not a method).

## 8. Discipline items

- **Info boundary:** AST-audited — `decide_fp` consumes only (raw, gamma_db, gamma_lin);
  zero true/tx/oracle/h/phi leakage. true γ only in channel gen + offline BER (frozen probe).
- **Seed isolation:** dev=0–9; Phase-B dev-tune=10–19; held-out=30–49; pollution 71–80 unused.
- **Frozen files:** `git diff --stat HEAD` empty on common/, params.py,
  `_a4_switch_common768_30seed.py`, `_p01_*.py`, `_a4_branchrouted_30seed.py`,
  `sc_nda_ml_sim.py`, anchor JSON. Only new files `_p03_*.py` added (untracked).
- **Resource proxy:** labelled "proxy" throughout — op×operand-bit and storage-bit sums;
  NO LUT/DSP/power/area/throughput claim, no synthesis.
- **Repro:** `save_results()` artifacts with raw rows + aggregates; aggregates independently
  recomputed from raw_rows (regret identity verified on every row).

## Artifacts
- `projects/simulation/results/p03_fixed_point_codesign/phaseA_uniform.json` (2310 raw rows + aggregates; 308 s)
- `projects/simulation/results/p03_fixed_point_codesign/phaseBC_dev_tuning.json` (6930 dev rows + chosen configs)
- `projects/simulation/results/p03_fixed_point_codesign/phaseBC_mixed.json` (3300 held-out + 3960 uniform-ladder rows + aggregates + ablation; 876 s)

## Source
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_fixed_point.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_smoke_check.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_phaseA.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/_p03_phaseBC.py`

Elapsed (wall): smoke 220 s + Phase A 308 s + Phase BC 876 s ≈ 24 min compute (plus analysis).
Total session wall incl. verification/diagnosis/debug-fix: ~50 min.
