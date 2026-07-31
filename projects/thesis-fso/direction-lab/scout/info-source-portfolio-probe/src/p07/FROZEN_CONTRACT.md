# P07 Frozen Contract — `F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`

> Frozen BEFORE any test data is read. Binding decision D045 (2026-07-31).
> Campaign P07, new mechanism family F (1st package).
> Distinct from P03 (selector-internal fixed-point Q(W,F) digital post-processing); P07 = analog
> front-end variable gain + ADC full-scale/clipping/quantization on `rx_raw` BEFORE the frozen
> receiver chain.

## 1. Entry correction (binding decision)

The old P07-entry-selection scan (F timing offset / G scenario extension / H FEC-APSK) is
**REJECTED** (kept as rejected brief, not counted as valid P07). Three independent FAILs:

- **F symbol-timing offset**: channel (`common/_channel.py:97-169`, `common/_dual_pol_channel.py`)
  has only per-symbol `signal = tx*sqrt(h)*carrier` + AWGN, **no oversampling / pulse shaping /
  fractional delay** (grep-confirmed zero hits for oversamp|pulse_shape|rrc|upsample|
  fractional_delay). At 1-sps there is no physical DOF for a symbol-timing offset to act on.
- **G scenario extension**: no frozen M-C-A; risks re-entering closed P04 (continuous GG OOD) /
  closed FOE-residual axis (T030 withdrawn).
- **H FEC/APSK**: coded chain blocked (P05-D withdrawn: no real codec / threshold eval not FEC);
  APSK ring-ratio entry withdrawn in P04 (γ is modulation config, not channel random quantity;
  selector does not read ring-ratio).

**Formal P07 = `F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`** (candidate-universe.yaml U07, ap=AP06).

## 2. Frozen problem M-C-A

- **M (method/frozen receiver)**: `run_case_multidelta` per-window chain
  (`_p01_cpr_snr_mismatch_probe.py:172`): per window of N_DFT=256 symbols —
  `estimate_h_blind_perblock` + `estimate_h_pilot_perblock` → `amp_limit(mmse_equalize(...),3.0)` →
  `A.per_block` (DA/NDA common-768 errors) + `A.decide` branch choice + `S.ber_oracle_turb` offline.
  A fixed-gain, fixed-full-scale, finite-bitwidth I/Q ADC sits at the analog front end, BEFORE this
  chain consumes the (quantized) `rx_raw`.
- **C (conditions)**: source-closed GG dynamic amplitude via `generate_shared_realization_apsk`
  (`common/_channel.py:97`). Scenes {weak(α,β)=(11.6,10.1), moderate=(4.0,1.9), strong=(4.2,1.4)}
  (params.py:101-171), SNR 5..25 dB step 2 (P01-P04 anchor grid), N_DFT=256, 400 windows/cell,
  f_dot=DOPPLER_HIGH=150e6, mod='m16apsk', SEED_TURB0=2000. Deep fades (low h) and strong peaks
  (high h) alternate in time (GG block AR(1)).
- **A (action / failure to show)**: the fixed gain must trade off two impairments — gain too high
  → peak clipping at the rails; gain too low → effective quantization resolution insufficient in
  deep fades. Question: does this trade-off produce a real, stable, cross-bitwidth receive
  performance loss under source-closed GG, can a standard causal AGC resolve it, and does a
  robust/clipping-aware AGC still offer a distinguishable increment?

## 3. Phase 0 — trustworthy causal AGC/ADC adapter (BLOCKER gates)

Fixed signal chain:
```
channel float rx_raw
  → gain (decided from PAST quantized samples / rail-hit flags / receiver-visible stats)
  → I/Q rail clip to ±FS
  → finite-bitwidth uniform signed I/Q ADC
  → quantized raw
  → frozen receiver chain (unchanged)
```

- **Signed I/Q quantizer**: `code = clip(round_half_up(gain*value / step), ±(2^(W-1)-1))`,
  `step = 2*FS / 2^W`, reconstruct `q = code * step`. Round-half-up (ties→+∞). Saturation clips,
  **never wraps** (no two's-complement overflow). Identical contract for real and imag parts.
- **Full-scale / step**: FS frozen per the pre-registered ladder (see §4); not cherry-picked to
  manufacture method benefit. step = 2*FS/2^W.
- **Causality**: gain at window b decided ONLY from windows `< b` (quantized samples, rail-hit
  flags, receiver-visible running statistics). Window 0 uses nominal fixed gain (no past).
- **Info-boundary (AST audit, BLOCKER)**: `decide_gain` body must contain NONE of
  {`h`, `alpha`, `beta`, `tx`, `phi`, `bits`, `true`, future-window index, true-amplitude}.
  Signature consumes only past-quantized-rx / rail-hit / receiver-visible-stats. **One forbidden
  substring → BLOCKED_AGC_INFO_LEAK, EXECUTION_INVALID.**
- **Float-bypass identity (BLOCKER)**: at gain=1.0, FS=large, W=64, the quantized raw must
  reconstruct the float raw to ≤ 2^-40, AND the frozen receiver chain run on quantized raw must
  reproduce the original float `run_case_multidelta` per-cell outputs (selected_errors, branch
  counts, oracle errors) **byte-identical** (0 mismatch across all dev cells). **Any mismatch →
  BLOCKED_NO_FLOATBYPASS, EXECUTION_INVALID.**
- **Bitwidths**: must cover at least {6, 8, 10} bit (low-to-mid optical-receiver ADC; conclusion
  must not depend on a single bitwidth).
- **Fairness**: fixed-gain / conventional AGC / new candidates share identical realization,
  bitwidth, FS, update interval, and delay.

**If the adapter cannot be made trustworthy → `EXECUTION_INVALID` (does not count P07).**

## 4. Phase A — problem existence (dev 0-9, criteria frozen BEFORE reading results)

**Frozen before reading** (this section):
- **MDE = 0.15 dB** (consistent with P01-P04; paired-regret dB scale relative to ideal float ADC).
- **At least 3 physical conditions** (scene×SNR cells) must pass the problem gate for the problem
  to be "established" (no single-cell claim).
- **Problem-gate definition**: dev-tuned best fixed-gain ADC, at bitwidth W, has paired regret
  (vs ideal float ADC, same realization) with **pooled mean ≥ MDE AND pooled CI_low > 0**, AND
  this holds **consistently across {6,8,10} bit** (not one bitwidth alone). Per-bitwidth best
  fixed gain is chosen on dev only (within the pre-registered gain ladder, not cherry-picked).
- **Pre-registered fixed-gain ladder**: nominal gain set derived from signal RMS range, NOT
  hand-picked to create a benefit. Specifically `gain ∈ {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0}`
  with FS=1.0 (unit-power-normalized full scale) — chosen a priori to bracket the typical
  `|rx|` swing across the anchor grid.
- **Seed isolation**: dev = seeds 0-9 (P01-P04 anchor dev set); fresh held-out = seeds 30-49
  (P01's set; AGC estimand is a gain/config, not a fit on these seeds → no leakage, per P03
  §3.4 precedent). dev ≠ held-out throughout. Seeds 71-80 forbidden.

- **Phase-A dev grid (pre-registered, representative subset of the anchor grid)**:
  scenes {weak, moderate, strong} × SNR {5, 9, 13, 17, 21} dB (5 points spanning
  the gain-bearing low/mid/high SNR, NOT a single point) × dev seeds {0,1,2,3,4}
  (5 seeds) = **75 cells**. Rationale: (a) the frozen receiver's per-window
  `per_block` (11 m16apsk_demod calls × 400 windows) makes the full 330-cell
  anchor grid ~3.5 h on one core; (b) 75 cells give 75 paired-regret samples per
  bitwidth at the dev-best gain — sufficient for a t-CI; (c) the problem gate
  needs ≥3 cells passing, well covered by 15 cells/scene×SNR. The 5-SNR subset
  spans the same low–high range as the 11-SNR anchor; conclusions are NOT
  based on a single SNR. If Phase A is ambiguous on this subset, the full grid
  can be added as a bounded in-package repair.
- **Comparators in Phase A**: ideal float ADC (regret=0 reference); dev-tuned best fixed-gain ADC
  (per bitwidth); **oracle per-block gain as headroom/Kill bound ONLY, NOT a Go comparator**
  (TL-32 / FR-25).
- **Metrics**: frozen-receiver BER / PI-SER on the branch the selector picks; clipping rate
  (fraction of samples hitting the rail); effective occupied codes / quantization utilization;
  paired regret (dB) vs ideal ADC.

**Gate outcome (frozen BEFORE reading results):**
- best fixed-gain regret pooled < MDE OR pooled CI crosses 0 OR not consistent across bitwidths →
  **`PROBLEM_ABSENT_ON_SOURCED_ADC_RANGE`** (valid P07, counts 7/10; Phase B/C NOT run).
- otherwise problem established → proceed to Phase B.

## 5. Phase B — strong conventional comparators (only if Phase A establishes the problem)

Conventional AGCs, dev-only tuned, test frozen, identical past-info / update budget / gain bounds
/ slew-rate / delay, do NOT read true GG/channel:
- **causal RMS AGC** (running RMS over past quantized samples → gain to target RMS);
- **peak-hold / attack-release AGC** (peak envelope with attack/release time constants);
- **log-domain AGC** (3rd conventional comparator, if straight RMS/peak-hold ambiguous).

Each AGC: gain ∈ [g_min, g_max] pre-frozen, update interval pre-frozen, slew-rate pre-frozen,
one-block causal delay. Dev-only tuning of a **pre-registered small-but-diverse 3-config set per
family** (target spans {0.2,0.3,0.4} × forget/release span {0.8,0.9,0.95}) on a representative
dev grid; final test on fresh held-out seeds. Each family gets the SAME 3-config dev budget (fair).
dev grid = weak/strong × SNR {5,13,21} dB × dev seeds {0,1,2} = 18 cells; held-out grid =
3 scenes × SNR {5,9,13,17,21} dB × held-out seeds {30,31,32,33,34} = 75 cells.

**Gate (frozen BEFORE reading B results):** strongest conventional AGC recovers regret to within
MDE of ideal across the established cells (pooled |Δregret| ≤ MDE AND CI consistent) →
**`PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC`** (no method packaging).

## 6. Phase C — method factory (only if Phase B leaves a residual)

At least 4 mechanism-distinct candidates, each a DIFFERENT deployable action (not hyperparameter
swaps of one formula):
1. **dual-time-constant attack/release** (fast attack on peak, slow release on fade);
2. **clipping-aware anti-windup** (gain backs off immediately on rail-hit burst);
3. **robust Huber / percentile amplitude estimator** (resists the clipped/fade tails);
4. **hysteretic two-range gain** (separate high/low gain bands with hysteresis);
5. (optional) uncertainty-gated combination — **NO ML filler**.

Cheap-alternative checked first. Dev-tune on 0-9, fresh held-out 30-49. Save raw rows (per-cell
regret / clipping rate / code utilization / help-hurt-tie), ablation (gain mechanism vs plain AGC
at equal update budget).

**METHOD_SIGNAL requires ALL (frozen BEFORE C):**
- best candidate strictly beats the strongest conventional AGC on fresh held-out;
- gap ≥ frozen MDE;
- paired CI does not cross 0;
- direction consistent across multiple bitwidths / turbulence conditions;
- no benefit gained from more update calls or larger info budget;
- ablation supports the clipping–resolution mechanism (not some other artifact).

Only then: **`DIAGNOSTIC_METHOD_SIGNAL`** (register pre-formal carrier only; still needs GW
Step 3/3.5/4a + novelty closure before any formal claim). Otherwise NO_DIAGNOSTIC_METHOD_SIGNAL
/ PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC / EXECUTION_INVALID.

## 7. P06 wording boundary (no edit, no rerun of P06)

P06 NO_CAUSAL_HISTORY_INCREMENT must be described accurately: history-expanded > current-only,
persistence > history-expanded → "no method increment over a strong conventional temporal
baseline", **NOT "history carries no information"**. P07 records must preserve this.

## 8. Terminal verdict set (method-production, six-way)

`DIAGNOSTIC_METHOD_SIGNAL` / `NO_DIAGNOSTIC_METHOD_SIGNAL` /
`PROBLEM_RESOLVED_BY_CONVENTIONAL_AGC` / `PROBLEM_ABSENT_ON_SOURCED_ADC_RANGE` /
`BLOCKED_SHARED_TESTBED` / `EXECUTION_INVALID`.

## 9. Discipline

- executor (implement+run) and verifier (independent recompute) separated.
- one in-package deterministic fix allowed; no second repair conversation.
- save_results() artifacts with raw rows + aggregates + contract + source hashes + seed ledger.
- frozen files (common/, params.py, _a4_switch_common768_30seed.py, _p01_*.py,
  _a4_branchrouted_30seed.py, sc_nda_ml_sim.py, anchor JSON) MUST be byte-identical
  (`git diff --stat HEAD` empty on them).
- do NOT modify Skill / controller / formal owner / protected history. No push.
