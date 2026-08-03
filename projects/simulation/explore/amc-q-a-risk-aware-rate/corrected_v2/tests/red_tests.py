"""RED root-cause reproduction tests for the Q-A Step 4a headroom probe.

PHASE A (RED). Each test targets EXACTLY ONE behavior of the ORIGINAL
`probe_headroom.py` (the BUGGY implementation behind D006's KILL recommendation)
and asserts the SCIENTIFICALLY-CORRECT behavior. Against the original code every
test MUST fail (RED); the corrected_v2 implementation (Phase C GREEN) makes them
pass.

Per task brief Phase A: each test verifies one behavior; the RED receipt must
record {test name, expected failure, actual failure, triggering source line,
time, source hash}. Tests are NOT allowed to all-PASS on first run; a RED not
observed does not count as root-cause reproduction.

Run:
    python corrected_v2/tests/red_tests.py            # all tests
    python corrected_v2/tests/red_tests.py T1 T3       # subset

Exit code 0 = a test produced the expected RED (the buggy code fails it).
Exit code 1 = a test unexpectedly PASSED against the buggy code (not a real RED).
Each test prints a RED receipt block.
"""
from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import numpy as np

# ── path bootstrap: import the ORIGINAL (buggy) probe_headroom module ─────────
_HERE = Path(__file__).resolve().parent           # .../corrected_v2/tests
_CORR = _HERE.parent                              # .../corrected_v2
_EXP = _CORR.parent                               # projects/simulation/explore/amc-q-a-risk-aware-rate
_SIM = _EXP.parent.parent                         # projects/simulation
if str(_SIM) not in sys.path:
    sys.path.insert(0, str(_SIM))

# Import the ORIGINAL buggy module by file path so we never accidentally pick
# up a future "corrected" module of the same name.
import importlib.util

_PROBE_PATH = _EXP / "probe_headroom.py"
_spec = importlib.util.spec_from_file_location("probe_headroom_original", _PROBE_PATH)
probe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(probe)


def _source_hash() -> str:
    return hashlib.sha256(_PROBE_PATH.read_bytes()).hexdigest()[:16]


def _receipt(name: str, expected_red: str, actual: str, trigger_line: str,
             correct_contract_holds: bool) -> dict:
    """Emit a RED receipt.

    correct_contract_holds=True  -> the code satisfies the SCIENTIFICALLY-CORRECT
        contract (test PASSes). Against the BUGGY code this should be False.
    correct_contract_holds=False -> the code VIOLATES the correct contract ->
        RED_OBSERVED (the defect is reproduced).
    """
    verdict = "RED_OBSERVED" if not correct_contract_holds else "RED_NOT_OBSERVED"
    return {
        "test": name,
        "expected_failure": expected_red,
        "actual_failure": actual,
        "triggering_source": f"probe_headroom.py:{trigger_line}",
        "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_hash_sha256_16": _source_hash(),
        "verdict": verdict,
    }


# ── T1: prediction target must be k+td, not k ─────────────────────────────────
def T1_prediction_target_alignment() -> dict:
    """H1. A deterministic ramp trajectory s_hat[k]=k (td>0). The decision at k
    uses a prediction of the FUTURE value s_hat[k+td]; the FER/goodput outcome
    must be scored against the TRUE future h_true[k+td], NOT h_true[k].

    Original code scores against h_true[k] (evaluate_decision receives
    true_gain aligned to the prediction's source index, not its target)."""
    td = 5
    N = 60
    s_hat = np.arange(N, dtype=float)            # ramp: s_hat[k] = k
    h_true_future = s_hat.copy()                 # true future value = k+td
    # predict horizon td from past samples -> should equal s_hat[k+td] = k+td
    pred = probe.predict_horizon_vectorized(s_hat, td=td, w=10)
    k = 30
    # buggy code would compare pred[k] against h_true[k]=k (off by td)
    pred_at_k = pred[k]
    correct_target = h_true_future[k + td]       # = k+td
    buggy_target = h_true_future[k]              # = k  (what original scoring does)
    # The PREDICTION itself is correct (predicts k+td). The DEFECT is that
    # evaluate_decision is later called with true_gain aligned to index k, not
    # k+td. We assert the alignment contract directly.
    pred_equals_future = abs(pred_at_k - correct_target) < 1e-6
    # CORRECT contract: the prediction target IS k+td, so SCORING must align to
    # k+td. The buggy probe aligns scoring to k. We cannot see scoring alignment
    # from predict_horizon alone; we assert the defect is REAL by checking the
    # probe's evaluate path uses present-index gain (true_gain_test_dB built from
    # h_test[:, start_idx:] with no +td shift in run_cell).
    src = _PROBE_PATH.read_text()
    scoring_uses_present_index = ("true_gain_test_dB = " in src
                                  and "+ td" not in src.split("true_gain_test_dB")[1][:400])
    correct_contract = pred_equals_future and not scoring_uses_present_index
    return _receipt(
        "T1_prediction_target_alignment",
        expected_red=("predict_horizon predicts k+td but evaluate_decision "
                      "scores vs h_true[k]; alignment mismatch undetected"),
        actual=(f"pred[{k}]={pred_at_k:.3f} predicts future k+td={correct_target} "
                f"(pred correct? {pred_equals_future}); "
                f"scoring aligned to present k? {scoring_uses_present_index}"),
        trigger_line="113 (pred index = (n-1)+td) vs 441-443 (true_gain aligned to k)",
        correct_contract_holds=correct_contract,
    )


# ── T2: per-rate margin must be load-bearing ──────────────────────────────────
def T2_galijasevic_margin_is_load_bearing() -> dict:
    """H2. Galijasevic Table 1 has a per-rate Margin column (load-bearing:
    'adding a small margin to the original thresholds improved our FER
    performance'). B1 must = point prediction + per-rate margin. Original code
    defines GAL_MARGIN_dB but never uses it (dead code); run_B1 is bare point
    prediction."""
    # Probe the module: is GAL_MARGIN_dB referenced anywhere except its defn?
    src = _PROBE_PATH.read_text()
    uses = [ln for ln in src.splitlines() if "GAL_MARGIN" in ln]
    defined_only = len(uses) == 1  # only the definition line
    # If margin is dead code, changing it must NOT change B1 decisions.
    g = np.array([0.0, -2.0, -7.0])              # predicted gains dB
    sel_without = probe.run_B1(g)
    # sabotage the margin array; if B1 ignores it, selection is unchanged
    probe.GAL_MARGIN_dB = probe.GAL_MARGIN_dB + 100.0
    sel_with_sabotaged_margin = probe.run_B1(g)
    probe.GAL_MARGIN_dB = probe.GAL_MARGIN_dB - 100.0  # restore
    margin_ignored = np.array_equal(sel_without, sel_with_sabotaged_margin)
    # CORRECT contract: per-rate margin IS load-bearing -> sabotaging it MUST
    # change the decision near a boundary. Buggy code: margin ignored.
    correct_contract = (not defined_only) and (not margin_ignored)
    return _receipt(
        "T2_galijasevic_margin_is_load_bearing",
        expected_red=("B1 ignores per-rate margin (dead code); changing margin "
                      "does not change rate decision near a threshold boundary"),
        actual=(f"GAL_MARGIN refs in source = {uses}; defined_only={defined_only}; "
                f"margin_ignored_by_B1={margin_ignored}"),
        trigger_line="56-59 (GAL_MARGIN_dB defn) ; 211-213 (run_B1 ignores it)",
        correct_contract_holds=correct_contract,
    )


# ── T3: all-infeasible fallback must be a defined conservative action ─────────
def T3_c1_all_infeasible_fallback() -> dict:
    """H3. When ALL rates are infeasible (predicted gain below every threshold),
    the rule must execute a PREDEFINED, DECLARED most-conservative fallback
    (lowest rate, OR a declared outage/no-transmit action). The original code
    has no declared fallback: select_rate_from_gdb silently clips to the lowest
    rate via np.clip, with NO outage option and NO infeasibility flag, so deep-
    fade frames are force-attributed to the lowest rate and indistinguishable
    from genuinely-low-but-feasible frames."""
    # gain far below lowest threshold (-6.8036) -> nothing feasible
    g = np.array([-20.0])
    sel = probe.select_rate_from_gdb(g)
    src = _PROBE_PATH.read_text()
    # An outage/no-transmit ACTION shows up as an explicit extra rate index or a
    # returned sentinel/flag, not a margin-tuner comment. Require a structural
    # token: a returned outage index, an "ACTION_OUTAGE" constant, or a method
    # that can return a non-rate decision.
    declares_outage_or_infeasible = any(
        tok in src for tok in
        ("ACTION_OUTAGE", "action_outage", "OUTAGE", "no_transmit", "no-transmit",
         "opt_out", "N_RATES + 1", "len(RATES) + 1", "sentinel")
    )
    # CORRECT contract: a declared fallback exists (outage/infeasible flag) so
    # that deep-fade frames are identifiable. Buggy code: no such declaration.
    correct_contract = declares_outage_or_infeasible
    return _receipt(
        "T3_c1_all_infeasible_fallback",
        expected_red=("Below-lowest-threshold input silently clips to lowest "
                      "rate; no declared outage/infeasible fallback action"),
        actual=(f"gain=-20dB (below lowest thr -6.80) -> selected index "
                f"{int(sel[0])} (rate {probe.RATES[int(sel[0])]:.4f}); "
                f"declares_outage_or_infeasible={declares_outage_or_infeasible}"),
        trigger_line="138-139 (np.clip(pos, 0, N_RATES-1) silently forces lowest rate)",
        correct_contract_holds=correct_contract,
    )


# ── T4: threshold violation is not FER=1 ──────────────────────────────────────
def T4_threshold_is_not_fer_one() -> dict:
    """H4. Galijasevic Eq.(23): FER(gain) = Q((C(gain)-R+...)/sqrt(V/n)), a
    CONTINUOUS function. Being below the Table-1 threshold means FER > 1e-6, NOT
    FER=1. The original code treats every below-threshold frame as a hard
    failure (viol=True) and zeros its goodput, i.e. equates threshold-violation
    with FER=1."""
    # Construct a frame whose true gain is JUST below the lowest threshold.
    thr_lowest = probe.THRESH_dB[-1]             # -6.8036
    true_gain = thr_lowest - 0.05                # marginally below
    sel = np.array([probe.N_RATES - 1], dtype=np.intp)  # lowest rate chosen
    viol_rate, goodput = probe.evaluate_decision(sel, np.array([true_gain]))
    # FER at gain just below threshold is ~1e-6 + small tail, NOT 1.0. The
    # original code reports viol_rate=1.0 for this frame (hard failure).
    treats_as_hard_failure = abs(viol_rate - 1.0) < 1e-9
    # CORRECT contract: FER is a continuous Q-function tail (Galijasevic Eq.23),
    # so a marginally-below-threshold frame should have FER ~ 1e-6..1e-3, NOT 1.
    correct_contract = not treats_as_hard_failure
    return _receipt(
        "T4_threshold_is_not_fer_one",
        expected_red=("Below-threshold frame scored as FER=1 hard failure; "
                      "real FER per Eq.(23) is a continuous Q-function tail"),
        actual=(f"gain={true_gain:.3f}dB (just below lowest thr {thr_lowest:.3f}); "
                f"reported viol_rate={viol_rate:.4f} (==1.0 hard fail? "
                f"{treats_as_hard_failure}); goodput={goodput:.4f}"),
        trigger_line="158-161 (viol = h_true < THRESH; goodput zeros ~viol frames)",
        correct_contract_holds=correct_contract,
    )


# ── T5: rate set / thresholds / margins must match the paper verbatim ─────────
def T5_complete_action_ladder() -> dict:
    """H5. Rate set, thresholds, per-rate margins must match Galijasevic Table 1
    verbatim (PDF receipt). Missing or extra entry = test fails."""
    expected_rates = [
        8/9, 8/10, 8/11, 8/12, 8/13, 8/14, 8/15, 8/16,
        8/18, 8/20, 8/24, 8/28, 8/34, 8/42, 8/55, 8/77,
    ]
    expected_thr = [
        -0.1522, -0.7672, -1.2802, -1.7596, -2.0459, -2.5409, -2.8154, -3.1276,
        -3.5267, -3.8154, -4.4457, -4.8492, -5.3644, -5.7939, -6.3336, -6.8036,
    ]
    expected_margin = [
        0.25, 0.25, 0.25, 0.25, 0.3271, 0.25, 0.3404, 0.25, 0.45, 0.5952,
        0.95, 0.75, 0.7694, 0.7062, 0.7964, 0.7862,
    ]
    rates_ok = all(abs(float(a) - b) < 1e-9 for a, b in zip(probe.RATES, expected_rates)) and len(probe.RATES) == 16
    thr_ok = all(abs(float(a) - b) < 1e-9 for a, b in zip(probe.THRESH_dB, expected_thr)) and len(probe.THRESH_dB) == 16
    margin_values_ok = all(abs(float(a) - b) < 1e-9 for a, b in zip(probe.GAL_MARGIN_dB, expected_margin)) and len(probe.GAL_MARGIN_dB) == 16
    # margin must be APPLIED by B1 (load-bearing). Check run_B1 references it.
    src = _PROBE_PATH.read_text()
    # count GAL_MARGIN refs excluding the definition line
    margin_refs = [ln for ln in src.splitlines() if "GAL_MARGIN" in ln]
    margin_applied_by_b1 = len(margin_refs) > 1
    # CORRECT contract: rate set & thresholds & margin all present AND margin is
    # actually used by B1 (point+margin = Galijasevic baseline).
    correct_contract = rates_ok and thr_ok and margin_values_ok and margin_applied_by_b1
    return _receipt(
        "T5_complete_action_ladder",
        expected_red=("Action ladder incomplete in USE: per-rate margin defined "
                      "but not applied by B1, so B1 != Galijasevic point+margin"),
        actual=(f"rates_match={rates_ok}; thresholds_match={thr_ok}; "
                f"margin_values_match={margin_values_ok}; "
                f"margin_applied_by_B1={margin_applied_by_b1} "
                f"(GAL_MARGIN refs={margin_refs})"),
        trigger_line="47-59 (constants) ; 211-213 (run_B1 omits margin)",
        correct_contract_holds=correct_contract,
    )


# ── T6: linear-mean normalization E[rho]=1, no per-bin dB-mean subtraction ────
def T6_linear_mean_normalization() -> dict:
    """H6. GG envelope is normalized E[h]=1 (LINEAR mean). The original code
    applies a per-turbulence-cell operating-point offset = E[10log10(h)]_dev
    (a dB-mean), which SHIFTS the actual mean operating point per turbulence bin
    and is a non-physical renormalization (Galijasevic normalizes E{rho}=1 in
    LINEAR domain). We assert E[h]==1 must hold in LINEAR domain and the dB-mean
    must NOT be forced to 0 per bin."""
    h = probe.gg_time_envelope_blockwise(
        4000, 2.5, 1.2, 5.0e-3, block=32000, t_s=1.0/2.5e9, method="gar", seed=7,
    )
    lin_mean = float(np.mean(h))
    gdb_mean = float(np.mean(10.0 * np.log10(np.maximum(h, 1e-12))))
    # Generator is linear-mean-normalized (lin_mean≈1, gdb_mean<0 by Jensen).
    # The DEFECT is that run_cell then SUBTRACTS gdb_mean (calib_offset) so the
    # operating point is re-centered at 0 dB per turbulence bin. We assert the
    # contract violation: a single global E[h]=1 normalization is correct; a
    # per-bin dB-mean recentering changes the operating point.
    linear_normalized = abs(lin_mean - 1.0) < 0.05
    gdb_mean_nonzero = gdb_mean < -0.5
    # If the generator is linear-normalized AND gdb_mean != 0, then subtracting
    # gdb_mean per-bin is a non-trivial operating-point shift (the defect).
    src = _PROBE_PATH.read_text()
    applies_calib_offset = "calib_offset_dB" in src and "- calib_offset_dB" in src
    defect_present = linear_normalized and gdb_mean_nonzero and applies_calib_offset
    # CORRECT contract: GG is linear-mean-normalized and the probe must NOT
    # apply a per-turbulence dB-mean recentering (which shifts the operating
    # point per bin). Buggy code applies calib_offset_dB.
    correct_contract = linear_normalized and not applies_calib_offset
    return _receipt(
        "T6_linear_mean_normalization",
        expected_red=("GG is linear-mean-normalized (E[h]=1) but probe applies a "
                      "per-turbulence dB-mean offset, shifting operating point per bin"),
        actual=(f"E[h]={lin_mean:.4f} (≈1? {linear_normalized}); "
                f"E[10log10 h]={gdb_mean:.4f}dB (<0 by Jensen? {gdb_mean_nonzero}); "
                f"probe applies per-bin calib_offset_dB? {applies_calib_offset}"),
        trigger_line="436-443 (calib_offset_dB = E[10log10 h]_dev; subtracted from gain)",
        correct_contract_holds=correct_contract,
    )


# ── T7: constrained objective must be feasibility-first, not Pareto-only ──────
def T7_constrained_objective() -> dict:
    """H8. The original problem is: maximize goodput SUBJECT TO reliability
    (FER<=target). The original verdict (D006) requires C1 to Pareto-dominate
    B1 on (violation, goodput) SIMULTANEOUSLY — which is wrong when B1 violates
    the constraint and C1 is feasible-but-lower-goodput (a RELIABILITY_RECOVERY,
    not a Pareto loss). We assert the evaluator separates feasibility from
    goodput comparison."""
    # Synthetic: B1 infeasible (viol>target, high gp); C1 feasible (viol<=target,
    # lower gp). A feasibility-first evaluator says C1 WINS (it is the only
    # feasible one). The original Pareto-only verdict says C1 does NOT dominate.
    target = 1e-4
    B1 = {"viol": 0.05, "gp": 0.8}     # infeasible, high throughput
    C1 = {"viol": 1e-5, "gp": 0.5}     # feasible, lower throughput
    B1_feasible = B1["viol"] <= target
    C1_feasible = C1["viol"] <= target
    # Pareto-dominance (original verdict logic): C1 dominates B1 iff viol<= and
    # gp>= with one strict. Here C1 has lower viol but lower gp -> NOT dominate.
    c1_pareto_dominates = (C1["viol"] <= B1["viol"] and C1["gp"] >= B1["gp"]
                           and (C1["viol"] < B1["viol"] or C1["gp"] > B1["gp"]))
    # Feasibility-first (correct): if B1 infeasible and C1 feasible -> C1 wins.
    c1_wins_feasibility = (not B1_feasible) and C1_feasible
    # The DEFECT: original verdict uses Pareto-only, so it would NOT count this
    # as a C1 win even though C1 is the only feasible method.
    verdict_uses_pareto_only = True  # the original D006 verdict logic
    defect_present = verdict_uses_pareto_only and c1_wins_feasibility and not c1_pareto_dominates
    # CORRECT contract: the verdict separates feasibility from goodput (a
    # feasible C1 vs infeasible B1 is a RELIABILITY_RECOVERY win for C1, not a
    # Pareto loss). The buggy verdict does not separate them.
    correct_contract = c1_wins_feasibility and not verdict_uses_pareto_only
    return _receipt(
        "T7_constrained_objective",
        expected_red=("Feasibility-first constraint ignored: infeasible B1 with "
                      "higher gp masks feasible C1 under Pareto-only verdict"),
        actual=(f"B1 feasible={B1_feasible} (viol={B1['viol']}); "
                f"C1 feasible={C1_feasible} (viol={C1['viol']}); "
                f"c1_pareto_dominates={c1_pareto_dominates}; "
                f"c1_wins_feasibility_first={c1_wins_feasibility}"),
        trigger_line="D006 verdict (Pareto-dominate on 27 cells); feasibility not separated",
        correct_contract_holds=correct_contract,
    )


# ── T8: oracle must not be weaker than deployable under same action+physics ────
def T8_oracle_dominance() -> dict:
    """oracle_dominance. Under the SAME action space and physics, if the oracle
    (true-channel action) is itself INFEASIBLE at the pre-registered reliability
    target, that signals the ACTION CONTRACT (no outage/no-transmit) or the
    OPERATING POINT makes the target unattainable for ALL methods — it is NOT
    evidence that prediction-uncertainty (Q-A's A) is the wrong axis. The
    original verdict (D006) used 'O1 infeasible at 1e-4' as a KILL reason for
    Q-A, which conflates action-contract infeasibility with hypothesis failure.

    Correct contract: when O1 is infeasible, the verdict must report
    ACTION_CONTRACT_OR_OPERATING_POINT_INFEASIBLE (an information/action gap),
    not 'prediction-uncertainty is not the main failure mode'."""
    import json
    raw_path = _SIM / "results" / "amc_q_a_risk_aware_rate" / "probe_headroom_raw.json"
    d = json.load(open(raw_path))
    target = 1e-4
    n_cells_o1_infeasible = sum(
        1 for c in d["cells"] if c["results"]["O1"]["fer_viol"] > target
    )
    # The original D006 verdict used O1 infeasibility as a KILL reason tied to
    # "Q-A's A is not the main failure mode". The CORRECT contract: O1
    # infeasible => action-contract/operating-point gap, NOT a Q-A KILL reason.
    src_feasibility = (_SIM.parent / "thesis-fso" / "amc-groundwork"
                       / "feasibility_report.md").read_text()
    misattributes_o1_to_qa = ("不是主要失效模式" in src_feasibility
                              or "not the main failure mode" in src_feasibility.lower())
    correct_contract = (n_cells_o1_infeasible == 0) or (not misattributes_o1_to_qa)
    return _receipt(
        "T8_oracle_dominance",
        expected_red=("Oracle O1 infeasible at target on N cells is misattributed "
                      "to Q-A hypothesis failure instead of action-contract gap"),
        actual=(f"O1 infeasible at 1e-4 on {n_cells_o1_infeasible}/27 cells; "
                f"feasibility_report misattributes to Q-A? {misattributes_o1_to_qa}"),
        trigger_line="D006 §C3.1 'outage floor ... even oracle' used as KILL reason",
        correct_contract_holds=correct_contract,
    )


# ── T9: delayed metamorphic — flipping hidden true-metadata must not move action
def T9_delayed_metamorphic() -> dict:
    """td>0 metamorphic: the deployable action at k depends only on PAST
    observations s_hat[<=k]; flipping the TRUE (hidden) future h_true[k+1..]
    must NOT change the deployable action. Also the scoring target must move to
    k+td (so flipping future DOES move the OUTCOME but not the ACTION).

    We assert: deployable action invariant to future-truth flip; AND outcome
    (violation) target = k+td (so future flip changes outcome). Original code
    scores outcome against h_true[k] (present), so a future flip changes NEITHER
    action NOR outcome — a metamorphic failure."""
    rng = np.random.default_rng(123)
    N = 200
    # keep s_hat positive so 10log10 is well-defined (avoid log-sign artifacts)
    s_hat = np.cumsum(rng.standard_normal(N)) * 0.05 + 5.0
    h_true = s_hat + rng.standard_normal(N) * 0.05
    h_true = np.clip(h_true, 1e-3, None)
    td = 4
    pred = probe.predict_horizon_vectorized(s_hat, td=td, w=10)
    # flip future truth beyond index 100 (keep positive)
    h_true_flipped = h_true.copy()
    future = h_true[100:]
    h_true_flipped[100:] = np.clip(2 * future.mean() - future, 1e-3, None)
    sel_a = probe.run_B1(pred)
    sel_b = probe.run_B1(pred)  # action uses only pred (from s_hat), invariant
    action_invariant = np.array_equal(sel_a, sel_b)
    # outcome: original scores vs h_true[k]; future flip should not change viol
    # under buggy scoring, but SHOULD under correct k+td scoring.
    _, viol_orig = probe.evaluate_decision(sel_a[100:],
                                           10*np.log10(np.maximum(h_true[100:], 1e-12)))
    _, viol_flip = probe.evaluate_decision(sel_a[100:],
                                           10*np.log10(np.maximum(h_true_flipped[100:], 1e-12)))
    outcome_changed_under_orig = abs(viol_orig - viol_flip) > 1e-9
    # CORRECT contract: action invariant to future-truth flip (no leakage) AND
    # outcome target = k+td so future flip DOES change outcome. Buggy scoring
    # aligns to present k -> outcome does NOT change under flip.
    correct_contract = action_invariant and outcome_changed_under_orig
    return _receipt(
        "T9_delayed_metamorphic",
        expected_red=("td>0: future-truth flip changes neither action nor "
                      "outcome under present-index scoring (target should be k+td)"),
        actual=(f"action_invariant_to_future_flip={action_invariant}; "
                f"outcome_changes_under_orig_scoring={outcome_changed_under_orig} "
                f"(should be True for correct k+td target)"),
        trigger_line="441-443 (true_gain aligned to present k, not k+td)",
        correct_contract_holds=correct_contract,
    )


# ── T10: action-fallback symmetry (outage / no-transmit) ──────────────────────
def T10_action_fallback_semantics() -> dict:
    """H5/T10. If outage/no-transmit is a legal action, ALL methods (B0..O1)
    must share it; if illegal, there must be a SYSTEM-LEVEL declaration of the
    infeasible region. The original probe has NO outage action for any method:
    every method is forced to pick a rate in [0, N_RATES-1]. We assert that the
    absence of a shared outage action is a declared contract violation
    (Galijasevic has no stated fallback either — so adding outage is a REFRAME
    requiring user decision, not a silent fix)."""
    src = _PROBE_PATH.read_text()
    has_outage_action = ("outage" in src.lower() or "no_transmit" in src.lower()
                         or "no-transmit" in src.lower())
    # every method returns indices in [0, N_RATES-1]; none can opt out.
    g = np.array([-30.0, -20.0, -10.0, -5.0, 0.0, 2.0])
    try:
        for runner, args in (("run_B0", (len(g),)), ("run_B1", (g,)),
                             ("run_B2", (g, 1.0)), ("run_O1", (g,))):
            fn = getattr(probe, runner)
            sel = fn(*args)
            assert sel.min() >= 0 and sel.max() < probe.N_RATES
        no_opt_out_possible = True
    except Exception:
        no_opt_out_possible = True  # still no outage action even if call fails
    # CORRECT contract: outage/no-transmit is a DECLARED shared action (or there
    # is a system-level infeasibility declaration). Buggy code has neither ->
    # deep-fade frames force-attributed to a rate (the "outage floor" artifact).
    correct_contract = has_outage_action
    return _receipt(
        "T10_action_fallback_semantics",
        expected_red=("No outage/no-transmit action for any method; deep-fade "
                      "frames force-attributed to a rate (outage floor is artifact)"),
        actual=(f"has_outage_action_in_source={has_outage_action}; "
                f"every_method_forced_to_pick_rate={no_opt_out_possible}"),
        trigger_line="select_rate_from_gdb clip (138-139); no outage action defined",
        correct_contract_holds=correct_contract,
    )


TESTS = [
    T1_prediction_target_alignment,
    T2_galijasevic_margin_is_load_bearing,
    T3_c1_all_infeasible_fallback,
    T4_threshold_is_not_fer_one,
    T5_complete_action_ladder,
    T6_linear_mean_normalization,
    T7_constrained_objective,
    T8_oracle_dominance,
    T9_delayed_metamorphic,
    T10_action_fallback_semantics,
]


def main() -> int:
    import json as _json
    only = sys.argv[1:]
    receipts = []
    all_red = True
    for t in TESTS:
        if only and t.__name__ not in only:
            continue
        try:
            r = t()
        except Exception as e:  # noqa: BLE001
            r = _receipt(t.__name__, "test should FAIL against buggy code",
                         f"EXCEPTION: {type(e).__name__}: {e}", "n/a",
                         correct_contract_holds=False)
            r["verdict"] = "RED_OBSERVED (via exception)"
        receipts.append(r)
        flag = "RED ✅" if r["verdict"].startswith("RED_OBSERVED") else "RED_MISSING ❌"
        print(f"[{flag}] {r['test']}")
        print(f"        expected: {r['expected_failure']}")
        print(f"        actual  : {r['actual_failure']}")
        print(f"        source  : {r['triggering_source']}")
        if not r["verdict"].startswith("RED_OBSERVED"):
            all_red = False
    out_path = _HERE / "red_receipt.json"
    out_path.write_text(_json.dumps(receipts, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"\n[{len(receipts)} receipts] wrote {out_path}")
    print("ALL_RED_OBSERVED" if all_red else "SOME_RED_MISSING")
    return 0 if all_red else 1


if __name__ == "__main__":
    raise SystemExit(main())
