# Phase B — Physics & Algorithm-Identity Closure Receipt

> Q-A Step 4a scientific-integrity repair. Owner: AMC topic
> `2026-08-02-fso-amc-groundwork`. Created 2026-08-03.
> Companion to RED receipt `tests/red_receipt.json` (Phase A, 10/10 RED observed).
> This receipt closes the **physics, formula, parameter-provenance and action-
> contract identity** BEFORE any GREEN fix or re-measurement (brief Phase B).
> Decision problem redefinition is in Phase D; headroom gate in Phase E.

## 1. FER / rate-selection model identity (Galijasevic, source.pdf visual)

Verified by fresh-context subagent rendering the PDF (text layer + PNG of pp.4-7).
`papers/doi/10.1109_ojcoms.2024.011100/source.pdf` (9 pp.).

| Field | Verdict | Value (verbatim from PDF) |
|-------|---------|---------------------------|
| Modulation / detection | CONFIRMED | **OOK + APD** (NOT QAM, NOT coherent). p.4 |
| Coding family | CONFIRMED | PBRL-LDPC, RCA + ACE-PEG, k=8192 info bits. 72 codes designed (8/9…8/80); **16-rate subset** simulated |
| Full simulated rate set | CONFIRMED | 8/9, 8/10, 8/11, 8/12, 8/13, 8/14, 8/15, 8/16, 8/18, 8/20, 8/24, 8/28, 8/34, 8/42, 8/55, 8/77 |
| FER formula | CONFIRMED | **Eq.(23)** `FER(POD) = Q[ (C(POD) − R + log₂(n)/2n) / √(V(POD)/n) ]` — Polyanskiy normal approximation in DIRECT (Q-function) form, with Eq.(19) capacity `C=½(m₁(i₁)+m₁(i₀))`, Eq.(20) dispersion `V=½(m₂(i₁)+m₂(i₀))−C²`, n=k/R. **CONTINUOUS in gain**, NOT a hard threshold |
| FER target | CONFIRMED | **1e-6** (NOT 1e-2/1e-3/1e-4). p.3,6,7 |
| Table 1 threshold semantics | CONFIRMED | "channel gain threshold" = (POD achieving FER 1e-6) − (reference POD −53.9 dBm), in dB. 16 rows verbatim match `probe_headroom.py` THRESH_dB |
| Per-rate margin | CONFIRMED load-bearing | Table 1 Margin column; p.7 "adding a small margin to the original thresholds improved our FER performance". Application sign convention AMBIGUOUS in paper (states "added to thresholds") |
| Predictor | CONFIRMED | predicts **fading channel gain in dB**; polynomial fit (zero/linear/quadratic, Eq.27-28); **target index = k+td** (future), input = past estimates c₁..cₙ |
| Feedback delay | CONFIRMED | error-free, **round-trip**, values **1/2/3/4 ms**, distance c·t_d/2 |
| Frame / codeword | CONFIRMED | 2.5 Gsym/s; codeword 3.69 µs (8/9) – 31.5 µs (8/77); block-fading (ρ constant over codeword); one fade per 1024 bits |
| Channel model | CONFIRMED | **log-normal** (correlated, low-pass-filtered Gaussian → memoryless nonlinear), **PSI=10**, **τ₀=10 ms** (Eq.1 autocorr). **NOT Gamma-Gamma**, no α/β |
| Outage / no-transmit fallback | **NOT_FOUND** | No rule stated. Rate rule = "highest rate achieving FER<1e-6 for current known channel state". Behavior below 8/77 threshold is UNDEFINED in the paper |

**Identity decision (brief Phase B.1)**: FER model identity is **RECOVERABLE**
(Eq.23 is in the PDF; not BLOCKED_BY_FER_MODEL_IDENTITY). corrected_v2 will
compute **continuous FER via Eq.23** for the OOK/APD POD axis, NOT a hard
threshold. Because the threshold table is itself derived from Eq.23 at FER=1e-6,
the threshold-violation surrogate is a valid BINARY post-hoc summary but MUST
NOT be equated with FER (T4 RED).

## 2. Action-space adjudication (USER DECISION — recorded verbatim)

**Question put to user (2026-08-03)**: Galijasevic has NO outage/no-transmit
action. Adding one changes M (the baseline) = a reframe to a new problem Q-A'
requiring a new GW cycle (brief: "不得偷偷改成 Q-A'"). Three options offered.

**User decision**: *"同时跑两个动作契约（原契 + no-transmit 对称）"* — run BOTH
action contracts in corrected_v2:

- **Contract A (Galijasevic original)**: 16 rates only; below-lowest-threshold
  silently forces the lowest rate (= Galijasevic's own implicit behavior, since
  the paper does not declare a fallback). This is the contract under which Q-A
  is judged against the TRUE Galijasevic M.
- **Contract B (symmetric no-transmit)**: ALL methods in the ladder
  {B0,B1,B2,B3,B4,B5,C0,C1,O1,O2} share an additional no-transmit action chosen
  when the predicted/reliable gain is below the lowest threshold minus margin.
  Explicitly tagged **Q-A' reframe candidate**, requires user decision to
  promote to a new research direction (new GW Step 1-3 M-C-A + four-criteria).

No method gets an action the others lack (T10 / brief symmetry rule).

## 3. GG / operating-point / parameter provenance

| Parameter | Value | Provenance | Notes |
|-----------|-------|-----------|-------|
| Symbol rate | 2.5 Gsym/s | Galijasevic p.4,8 | matches probe T_S |
| Codeword symbols | 32000 | Galijasevic n=k/R with k=8192, R=8/77→ but probe uses 32000 as block. **DEBT**: 32000 corresponds to R≈0.256 (between 8/31 and 8/32), NOT a Galijasevic rate. Block=32000 is an APPROXIMATION; the paper's fade is per 1024 bits. Recorded as approximation debt |
| FER target | 1e-6 | Galijasevic p.3,6,7 | OLD probe scored at 1e-4 — **mismatched** |
| τ₀ (coherence) | 10 ms | Galijasevic p.4 Fig.4 | matches probe TAU_C_S |
| Feedback delay | 1-4 ms round-trip | Galijasevic p.2,7,8 | probe td_ratio maps to ms via block×t_s |
| Turbulence cells (α,β) | **(5,2)/(2.5,1.2)/(4,0.5)** | **NO PROVENANCE** — these are Gamma-Gamma medium/strong-turbulence values from the FSO literature, NOT from Galijasevic (which uses lognormal PSI=10). H7 violation. corrected_v2 must either (a) use Galijasevic's lognormal PSI=10 channel, or (b) explicitly declare GG (α,β) as a scenario-transfer choice with citation |
| GG normalization | E[h]=1 (LINEAR) | `_gg_time.py` independently verified: E[h]=1.004-1.013 at N=1e6 | per-turbulence `calib_offset_dB=E[10log10 h]` subtraction in old probe is a NON-PHYSICAL recentering (H6) |

**Provenance debt (recorded, not silently kept)**:
- The scenario itself is a **TRANSFER**: Galijasevic's exact channel is lognormal
  PSI=10 on OOK/APD; the AMC topic's target scenario is coherent sat-ground FSO
  under Gamma-Gamma. corrected_v2 runs under GG (α,β) as a declared
  scenario-transfer (Q-A's C condition), NOT a reproduction of Galijasevic's
  exact channel. This is consistent with Q-A's M-C-A (M=Galijasevic's
  rate-rule, C=GG+delay+estimation-noise, A=prediction-uncertainty risk-mismatch).

## 4. information_access / metric_signature / state_lifecycle (sim-preflight C4)

```yaml
information_access:
  online_known: [past_observation_s_hat_leq_k,  predicted_gain_dB_at_k_for_k_plus_td]
  receiver_visible: [s_hat_k = h_true_k + N(0,sigma_est^2)]
  oracle: [h_true_at_k_plus_td]   # only O1/O2 use future true channel
  post_hoc: [per_frame_FER_via_Eq23,  per_frame_goodput]
  deployable_forbidden: [h_true_at_k_plus_td, future_s_hat]   # no leakage

metric_signature:
  event_population: all_scoring_frames_in_eval_region (k >= start_idx = td+1)
  numerator_goodput: sum( RATES[selected] * (1 - per_frame_FER_Eq23) )
  numerator_threshold_violation: count( predicted_gain_threshold_condition_false )
  denominator: number of scoring frames
  excluded_positions: first td+1 warmup blocks per trajectory (no prediction)
  aggregation: mean over trajectories, paired by seed-pair across methods
  primary: feasibility_first_constrained_goodput   # Phase D
  secondary: [threshold_violation_rate, raw_goodput, mean_rate]

state_lifecycle:
  initialization_scope: per-seed RNG + gg_time_envelope_blockwise steady-state init
  reset_scope: new seed regenerates full h_true + s_hat trajectory (no carryover)
  generator_call_scope: one gg_time_envelope_blockwise call per (seed, alpha, beta)
  continuity_span: n_blocks=1500 per trajectory; AR(1) inter-block, constant intra-block
  delay_indexing: decision at k uses prediction of k+td; outcome scored at h_true[k+td]
```

## 5. What corrected_v2 MUST fix (mapping RED → GREEN)

| RED test | Defect | GREEN fix |
|----------|--------|-----------|
| T1 | scoring aligned to k, not k+td | score outcome vs h_true[k+td] |
| T2 | B1 ignores per-rate margin | B1 = point prediction + Galijasevic per-rate margin (load-bearing) |
| T3 | no declared infeasibility fallback | Contract A: declare "force-lowest" as the named fallback; Contract B: add symmetric no-transmit action |
| T4 | threshold-violation equated to FER=1 | compute continuous FER via Eq.23; report threshold-violation as a SEPARATE binary metric |
| T5 | action ladder missing margin in use | B1 uses margin; full ladder B0-B5+C0-C1+O1-O2 |
| T6 | per-turbulence dB-mean recentering | use LINEAR E[h]=1 normalization; do NOT subtract per-bin dB-mean; calibrate the threshold table to the link operating point ONCE (global, dev-frozen) if at all |
| T7 | Pareto-only verdict | feasibility-first constrained-goodput evaluator (Phase D) |
| T8 | O1 infeasibility misattributed to Q-A | when O1 infeasible at target → report ACTION_CONTRACT_OR_OPERATING_POINT_INFEASIBLE, NOT a Q-A KILL reason |
| T9 | present-index scoring defeats td>0 metamorphic | outcome target = k+td (same fix as T1) |
| T10 | no symmetric outage action | Contract B adds symmetric no-transmit to ALL methods; Contract A declares the force-lowest fallback explicitly |

## 6. NOT done in Phase B (deferred to later phases)

- Phase C: GREEN implementation + per-test RED→GREEN + verifier hand-recompute.
- Phase D: feasibility-first constrained-goodput evaluator (5 cell classes).
- Phase E: dev-only headroom gate (6 entry conditions).
- Phase F: fresh held-out MVE (only if Phase E passes).
- Governance: D007 supersedes D006; V008 supersedes V007 (Phase G sync).
