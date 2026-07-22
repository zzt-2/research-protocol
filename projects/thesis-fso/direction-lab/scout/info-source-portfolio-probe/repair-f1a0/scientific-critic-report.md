# Scientific Critic Report — F1-A0 (repair-f1a0)

**Role:** Independent scientific critic (adversarial, P6 separation). I attacked, not confirmed.
**Date:** 2026-07-22 (D021). **Verdict below.**

I independently recomputed from `F1-A0-result.v1.json:raw_rows` (110 rows): all seven method macros, the E1-vs-E3 row-by-row split, the g0 help/hurt counts + binomial p, the SOP-rotation magnitude, the causal_plugin≈E1≈nopred collapse, the g4 cross-cell count, and the CMA-divergence count. I additionally re-derived E2's failure, the blind_affine RAW-vs-CMA-fed ranking, the CMA μ-sweep, and the future-perturbation invariant by re-running the implementation — none of those three come from the artifact's pre-computed macros.

---

## Verdict on F1-A0 conclusion

**HOLDS — but on a DIFFERENT and WEAKER evidentiary basis than the Probe claims, with two of its supporting sub-claims OVERTURNED.**

The headline ("F1-A0 FAIL; the 0.133 F1-A headroom was bad CMA-anchor attribution, not CSI/TX-truth/model-prior headroom; do not build a tracker") survives, because it is dominated by a confound the Probe only half-credits: the SOP rotation over the eval window is ~0.06° (near-zero), so "predict next-block SOP state" is a near-vacuous task by construction — no information source can win here. But two of the Probe's *specific* supporting arguments are wrong/broken (E2 is implementation-broken; blind_affine is unfairly CMA-fed), and one gate (g6) is vacuous. The FAIL is correct; several of the *reasons given* for it are not.

---

## Attacks that landed

### L1. blind_affine is fed a FAILED CMA stream → comparator fairness is broken (STRONGEST)

`run_f1a0_causal.py:261-264` (`blind_affine_method`) feeds `cma["zX"]`/`cma["zY"]` — the CMA-equalized output — into `blind_affine_compare_16qam`. On these short (512–8192 sym) realizations fixed-μ CMA μ=0.03 is badly mistuned (see L4), so the z-stream is already mangled. I re-ran blind_affine on the **raw** `rX/rY` stream vs the CMA-fed path (same cell/seed, same eval window):

| cell (seed 161) | BA on RAW | BA on CMA-fed (probe path) |
|---|---|---|
| snr15-nominal-short | **0.0000** | 0.8359 |
| snr20-nominal-short | **0.0000** | 0.8242 |
| snr10-nominal-short | **0.0117** | 0.8164 |
| snr05-nominal-short | 0.0898 | 0.8906 |

blind_affine is a 2×2 complex affine LS; on the raw stream it inverts the channel's linear mix directly and is near-optimal. The probe's choice to chain it after a broken CMA **cripples** the comparator. Consequence: gates g1 (`run_f1a0_causal.py:570-575`, "causal_plugin beats blind_affine") and g2 (`:577-584`) are confounded — causal_plugin "wins" 11/11 cells (`:602-606`, confirmed by recompute) only because its opponent was sabotaged. The contract's `fair_comparison.methods_on_same_realization` (`probe-contract.v1.yaml:92-98`) is technically honored (same realization) but the *information path* is not equal: causal_plugin reads raw `rX/rY[ce:ee]` (`:397-398`), blind_affine reads CMA-corrupted `rX/rY`. This is an apples-to-oranges comparison the contract intended to forbid.

### L2. E2 (budgeted pilot) is implementation-broken — the pilots are never transmitted (STRONG)

`run_f1a0_causal.py:309-314` (`_e2_pilot_sequence`) synthesizes a frozen-random 16QAM pilot sequence `px/py` **in the receiver**. `e2_jones_pilot` (`:332-339`) then LS-fits `gx = Σ(rX_derot·conj(px)) / Σ|px|²` over `[es:es+32]`. But the channel (`_dual_pol_channel.py:119-132`, `make_realization`) transmits `sX/sY` (random 16QAM data), **never** `px/py`. So `p_rx = rX_derot[es:es+32]` is de-rotated *data*, correlated against an *unrelated fictitious pilot*. I confirmed empirically (snr20-nominal, seed 161): `|gx| = 0.195` (noise correlation) while the true channel gain `sqrt(h) ≈ 2.27`. The LS then divides by this noise gain, catastrophically amplifying — hence E2 macro PI-SER = **0.763** (artifact `:44`), near-random, on **every** cell including 25 dB-SNR where E1 = 0.005. A pilot that is never sent cannot "fail to help"; it is not a pilot. The "budgeted pilot is harmful / E2 worse than raw CMA" sub-claim in the Probe's conclusion is **invalid** — E2 measures noise amplification, not pilot performance.

### L3. g6 (PI vs fixed-label non-reversal) is VACUOUS — the two metrics are bit-identical

Recompute over all 110 rows: `*_pi_ser == *_fixed_label_ser` to within 1e-12 for **every method, every row** (verified for cma, blind_affine, e1, e2, e3, causal_plugin, causal_plugin_nopred). Per `cb1_evaluator.py:227-233`, `fixed_label_ser` uses assignment `(0,1)`; `pi_ser` uses the min over both stream permutations. They differ only when swapping X↔Y helps — which never happens here because E1/E3/causal_plugin de-rotate with a proper Jones (no axis swap) and CMA's residual swap never beats identity. So g6 (`run_f1a0_causal.py:614-619`) "passes" trivially: it is checking `x == x`, not two independent metrics. The contract's `dual_metric` requirement (`probe-contract.v1.yaml:99`) and `g6` falsifier (`:114`) are **not actually exercised**. g6 provides zero independent evidence.

### L4. The "CMA diverges" framing is factually wrong; it's μ-mistuning (confirms mechanism, contradicts wording)

The Probe's conclusion says "fixed-μ CMA μ=0.03 fails to converge / **diverges** on short realizations." The artifact says otherwise: `cma_diverged = False` for all 110 rows (`run_f1a0_causal.py:480`; recompute: 0/110 diverged; max cma_pi_ser = 0.930 < RANDOM_CEILING 0.9375). CMA does not diverge — it converges to a **poor** fixed point because μ=0.03 is mistuned for short blocks. My μ-sweep (snr15-short, seeds 161-163): μ=0.003→0.159, μ=0.01→**0.083**, μ=0.03→0.369, μ=0.05→0.397. Across all 11 cells (seeds 161-163): μ=0.03 macro = 0.415 vs μ=0.01 macro = **0.220** — a blind, zero-CSI CMA closes ~60% of the gap to the E1 CSI-genie (0.168) just by retuning μ. So the headroom is substantially "wrong CMA step size," and a fair conventional anchor would shrink the apparent CSI value a lot.

### L5. g1 is not a real persistence baseline — it's a confounded proxy

`_persistence_baseline_theta_error` returns `None` (`run_f1a0_causal.py:544`). g1 is then operationalized as "causal_plugin < blind_affine" (`:570-575`). That is not the contract's g1 ("held-out next-block state prediction significantly beats persistence/AR/no-information baseline", `probe-contract.v1.yaml:109`). Combined with L1 (blind_affine is CMA-crippled), g1 is doubly invalid as evidence.

---

## Attacks that did NOT land (Probe survived these)

### N1. Causality / future leakage — CLEAN
I re-ran the future-perturbation invariant myself (perturbed `rX/rY/h/theta` at index ≥ cut by large random values): `prefix_features` output and `predict_next_block_rotation` were **bit-identical**. Source confirms: `prefix_features` reads only `rX[:cut]`/`rY[:cut]` (`run_f1a0_causal.py:95-135`); `causal_plugin_method`'s slope uses prefix-only `_cma_prefix_trace(rX[:ce], rY[:ce])` (`:379`). The ridge probe is fit on `VAL_SEEDS` only (`:174-217`) and cached before any test seed. No leakage. g3 legitimately passes.

### N2. E1 TX-truth leakage — CLEAN (mostly)
`e1_jones_inverse` (`:271-302`) references only `rX/rY/h/theta` — grep confirms no `sX_calib/sY_calib`. It does use `R2_16QAM = 1.32` (the public constellation average power) for the unit-gain normalization (`:295-297`). That is **modulation-format knowledge** (TX *structure*), not TX *truth* (symbols). The contract's E1 says "no TX-truth symbols" — that holds. Calling it "pure CSI" slightly overstates (it assumes known 16QAM), but this does not rise to leakage and does not change the E1≈E3 finding.

### N3. g0 (prediction adds nothing) — the FAIL is real and robust
Recompute: prediction helps in 8 rows, hurts in 13, ties in 89; mean gain −0.00025 rad. Two-sided binomial p ≈ 0.38 (n=21) — i.e. the 8/13 split is **indistinguishable from a coin flip**. The Probe's "g0 FAIL, 8 help / 13 hurt" is correct; if anything it *understates* how null this is (the split is not even significantly negative, just noise around zero).

---

## Confounds / alternative explanations

### C1. The dominant confound is physics, not attribution: SOP rotation over the eval window is ~0.06°
`theta = sop_rate · arange(N)` (`_dual_pol_channel.py:123`) with `sop_rate = 4e-6` rad/sample. Over the 256-symbol eval window the accumulated rotation is `4e-6·256 = 1.02e-3 rad = 0.059°` (10° cell: 0.59°). De-rotation is therefore near-identity. This is why **E1 (true θ) ≈ causal_plugin (predicted θ) ≈ nopred (θ≡0)** to within 0.0005 macro PI-SER (all ≈ 0.168). The candidate "matches the CSI ceiling" vacuously — there is essentially nothing to predict. The Probe's conclusion ("rotation prediction adds nothing") is correct but its *reason* ("the ridge probe is weak") is secondary; the primary reason is "the target variable is near-constant over the horizon." Any tracker, however good, would look identical here. This means F1-A0 is a weak test of the F1 family's core question *by construction of the cell atlas*, not just by estimator choice.

### C2. "CMA-anchor-bad" is correct but under-attributed to "divergence"
See L4. The headroom is largely μ-mistuning, not divergence. This **supports** the Probe's headline ("headroom is fake") but the Probe's specific mechanism label is wrong, and — more importantly — it means a fair comparator (μ-tuned CMA, or blind_affine on the raw stream, L1) would erase most of the apparent CSI advantage. The "E1≈E3, so TX-truth adds nothing" claim (E1=0.168, E3=0.179; TX-truth is actually *worse* by +0.011 macro, and E1<E3 in 38 rows vs E1>E3 in 19) is confounded the same way: with rotation ≈ 0, the LS calibration has almost no residual to remove, so TX-truth can only add LS overfit noise. "TX-truth adds nothing" is not a general finding; it is an artifact of the near-zero-rotation regime.

### C3. E2 brokenness does NOT rescue the CSI case, but it removes one piece of evidence
A correctly-implemented E2 (actually transmit `px/py` in the calibration window) would very likely beat raw CMA and approach E1 — pilots + true de-rotation is a strong, realistic hybrid. That would *weaken* the "budgeted pilot is harmful" sub-claim (already invalid) but would not change the FAIL: even a perfect E2 would still be ≈ E1 ≈ causal_plugin ≈ nopred in this near-zero-rotation regime, so it still would not justify a one-day tracker. E2's brokenness is a validity bug, not a conclusion-flipper.

---

## What would change the conclusion

1. **Re-run blind_affine on the RAW stream (not CMA output)** — L1. If raw-fed blind_affine ≈ causal_plugin ≈ E1 (likely), then g1/g2 collapse to "candidate ties the best receiver-visible comparator," and the *comparator* story (not the FAIL) changes: the FAIL still holds but the framing shifts from "candidate fails to beat comparators" to "candidate offers nothing over an existing blind affine."
2. **Add a μ-tuned CMA anchor (μ swept on VAL, frozen)** — L4. If μ-tuned CMA ≈ E1, the entire "CSI headroom" framing dissolves into "CMA tuning debt," which D005/D007 already flagged. This would re-cast F1-A0 as re-discovering a known debt rather than as a clean info-source attribution.
3. **Run on a high-SOP-rate cell atlas** (sop_rate ≫ 4e-6, e.g. 4e-4–4e-3 rad/sample) so the eval-window rotation is ≥ several degrees — C1. Only then does "predict next-block θ" become a non-vacuous task, and only then can E1/E3/causal_plugin/nopred separate. In the current atlas they are forced to coincide by physics.
4. **Fix E2 to actually transmit the pilot** and re-evaluate — L2. Needed before any "budgeted pilot" claim (pro or con) can be made.
5. **Implement a real persistence/AR(1) baseline for g1** instead of the blind_affine proxy — L5.

---

## Independence note

I did not rubber-stamp. From `raw_rows` alone I independently recomputed: (a) all 7 method macros (match artifact to 5 dp); (b) E1-vs-E3 row split (38/53/19) and the +0.011 macro "TX-truth hurts" sign; (c) g0 counts (8/13/89) + binomial p≈0.38; (d) the E1≈causal_plugin≈nopred collapse (within 0.0005); (e) g4 = 11/11; (f) 0/110 CMA diverged. Beyond `raw_rows`, I re-derived by re-running code: E2's fictitious-pilot failure (|gx|=0.195 vs √h=2.27), blind_affine RAW(0.00) vs CMA-fed(0.84), the CMA μ-sweep (μ=0.01→0.22 vs μ=0.03→0.41), and the future-perturbation invariant (passes).

**Claims I could NOT independently recompute from `raw_rows`:** the ridge probe's fitted weights and the actual prefix-feature vectors are not stored, so I cannot re-derive the probe's `predict_next_block_rotation` target values or verify g1 against a true persistence/AR(1) baseline — I rely on the code (which I read) and the invariant test (which I re-ran) for those. Also not stored: per-sample `h`/`theta` arrays (needed to confirm the 0.06° rotation claim from data rather than from the channel model — I derived it from `_dual_pol_channel.py:123` + cell `sop_rate`).
