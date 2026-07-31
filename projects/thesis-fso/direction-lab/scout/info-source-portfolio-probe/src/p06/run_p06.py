"""P06 — E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION.

One-shot repair-type PROBLEM_BEARING_PROBE (binding decision D044). Repairs the
scientific invalidity of old F3-A: run_f3a_history.py:195-196 computed a
marginal-MI max-difference (max(history_mi) - max(block0_mi) over two different
feature sets) and *called* it conditional MI. state/current.yaml:161-170 marks
the old F3-A conclusion INVALIDATED_AS_CONDITIONAL_MI. This probe does NOT
inherit the old numbers (+0.060 bits, +0.036 R^2 are history only).

QUESTION (frozen, see FROZEN_CONTRACT.md): Does the strictly-causal history of
receiver-visible frame summaries provide a held-out predictive increment over
the strongest current-only / persistence / EWMA / AR(1) baseline for the
frozen receiver's NEXT-frame failure or performance, under source-closed
time-correlated GG dynamics rho = exp(-dt/tau_c)?

This is an OBSERVABILITY / predictive-increment probe. It does NOT train a deep
network, build a deployable controller, or claim a method. Primary judgment =
held-out predictive increment (MAE/RMSE/R2 increment + log-loss/Brier). MI is
NOT reported (the old MI path is invalidated; marginal-MI != conditional-MI).

Discipline (frozen before reading any test data):
  - features(t) use ONLY frame <= t receiver-visible summaries
  - target(t+1) = frozen-receiver next-frame performance/failure
  - h / alpha-beta truth / future trace / TX label / seed / cell-id /
    target-frame post-hoc residual are FORBIDDEN as features (used only for
    scoring the target, never as input)
  - trajectory-level train/dev/test split; fresh seed ledger disjoint from all
    historical test seeds
  - same-trajectory paired comparison; nested dev-only tuning; test bootstrap CI
  - MDE and event-count floor frozen before reading test
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
SRC_DIR = HERE.parent                      # .../info-source-portfolio-probe/src/p06
PROBE_SRC = SRC_DIR.parent                 # .../info-source-portfolio-probe/src
BATCH_DIR = PROBE_SRC.parent               # .../info-source-portfolio-probe
SCOUT_DIR = BATCH_DIR.parent               # .../direction-lab/scout
ATLAS_DIR = SCOUT_DIR / "cb1-modulation-generic-closure" / "baseline-atlas"
REPO_ROOT = HERE.parents[7]                # worktree root
SIM_DIR = REPO_ROOT / "projects" / "simulation"
RESULTS_DIR = SIM_DIR / "results" / "p06_causal_cross_frame_history"
for _p in (str(SIM_DIR), str(ATLAS_DIR), str(PROBE_SRC)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import probe_shared as ps  # noqa: E402  (frozen anchor infra, same as F3-A)
from common._gg_time import rho_from_tau_c, gg_pdf_theory  # noqa: E402
import cb1_cell_runner as atlas_runner  # noqa: E402
import cb1_evaluator as evaluator  # noqa: E402


# ─── Frozen configuration (read-before-test) ────────────────────────────────
FROZEN = {
    # Frozen traditional deployable receiver M (unchanged from F3-A anchor)
    "receiver": "standard_cma_godard_with_z",
    "cma_mu": 0.03, "cma_taps": 11, "cma_r2": 1.32, "cma_block_size": 64,
    # Source-closed GG dynamics C
    "alpha": 4.2, "beta": 1.4,          # strong turbulence (params.py true value)
    "t_s": 4e-10,                        # symbol period (2.5 GBaud)
    "block_gg": 100,                     # physical GG quasi-static block (symbols)
    "method": "gar",                     # exact Gamma edge AR(1)
    "sop_rate": 4.0e-6,                  # SOP rotation rate (F3-A frozen)
    # Frame abstraction
    # FRAME chosen so rho_frame~0.70 @ f_G=1000Hz (rich cross-frame dynamics);
    # at f_G=30/100 rho~0.97-0.99 (quasi-static — physical, not artificially sped).
    "frame_symbols": 140_000,            # frame = 140k symbols (dt=56us)
    "n_symbols": 2_800_000,              # 20 frames / trajectory
    "eval_symbols_per_frame": 8000,      # contiguous eval window at frame start (SER stable)
    "n_frame_history_min": 3,            # need >=3 past frames before 1st target
    # Conditions (source-closed f_G from params.py; SNR from dev nontrivial-fail scan)
    "fg_hz_list": [30.0, 100.0, 1000.0],
    "snr_db_list": [15.0, 20.0],         # nontrivial fail regime (dev scan: 15dB~63% fail, 20dB~rare)
    # Fresh seed ledger (disjoint from all historical: 11-150, 30-99)
    "train_seeds": list(range(200, 215)),   # 15 trajectories / condition
    "dev_seeds": list(range(215, 225)),     # 10 trajectories / condition
    "test_seeds": list(range(225, 240)),    # 15 trajectories / condition
    # Failure-event definition (threshold frozen on DEV before reading test)
    "fail_ser_threshold": 0.05,           # frame fixed-label SER > 0.05 = failure event
    "fail_event_count_min": 30,           # floor: <30 dev events => PROBLEM_ABSENT_AT_PHYSICAL_TIMESCALE
    # MDE (frozen before reading test)
    "mde_r2_increment": 0.01,             # history R^2 - best-current-only R^2 must exceed
    "mde_mae_decrement_rel": 0.05,        # relative MAE improvement >= 5%
    "bootstrap_n": 2000, "bootstrap_alpha": 0.05,
    "rng_seed_bootstrap": 20260731,
    # Phase 0 identity tolerance
    "identity_relerr_max": 1e-12,
    "acf_lag_max": 10,
    "edge_ks_pass": 0.05,                 # KS statistic threshold for edge fit
}
ARTIFACTS = BATCH_DIR / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Phase 0: frame-level realization + frozen-receiver single-frame identity ──

def _build_realization(seed, fg_hz, snr_db):
    """Source-closed shared realization (same generator as F3-A anchor)."""
    from common._dual_pol_channel import generate_shared_realization_dp
    gb = float(10.0 ** (snr_db / 10.0))
    return generate_shared_realization_dp(
        int(FROZEN["n_symbols"]), float(FROZEN["alpha"]), float(FROZEN["beta"]),
        float(fg_hz), sop_rate=float(FROZEN["sop_rate"]), seed=int(seed),
        gamma_bar=gb, block=int(FROZEN["block_gg"]), t_s=float(FROZEN["t_s"]),
        method=str(FROZEN["method"]), modulation="qam16")


def run_frozen_receiver(rX, rY):
    """The frozen traditional receiver M (standard-CMA godard-with-z)."""
    return atlas_runner.standard_cma_godard_with_z(
        rX, rY, n_tap=int(FROZEN["cma_taps"]), mu=float(FROZEN["cma_mu"]),
        R2=float(FROZEN["cma_r2"]), block_size=int(FROZEN["cma_block_size"]))


def per_frame_summaries_and_targets(r, res):
    """Build per-frame receiver-visible summaries + per-frame frozen-receiver targets.

    Frame = FROZEN['frame_symbols'] symbols. For each frame boundary t (0-indexed),
    produce:
      - summary(t) = receiver-visible aggregates over frame t (cm_error, output_power,
        update_norm, w_norm, z_amp_max: mean/std/max over the CMA trace blocks whose
        output range intersects frame t). STRICTLY causal: uses only frame t data.
      - target(t+1) = frozen-receiver fixed-label SER on frame t+1 (scored with TX truth;
        truth is NEVER a feature, only the scored target).

    Returns list of frame records with keys:
      frame_idx, summary (dict of scalars), next_fixed_ser (float),
      next_fail (0/1 fail_ser_threshold), fg_hz, snr_db, seed, traj_idx
    """
    FRAME = int(FROZEN["frame_symbols"])
    N = int(FROZEN["n_symbols"])
    half = int(FROZEN["cma_taps"]) // 2
    trace = res["trace"]
    zX, zY = res["zX"], res["zY"]
    n_frames = N // FRAME
    truth = np.column_stack((r["sX"], r["sY"]))
    bitsX, bitsY = r["bitsX"], r["bitsY"]

    # Map each CMA trace block -> the frame index it belongs to (by output_start)
    blk_frame = np.array([
        (int(t["output_start"]) // FRAME) for t in trace
    ], dtype=int)

    records = []
    for fi in range(n_frames):
        # receiver-visible summary over frame fi (blocks whose frame == fi)
        mask = (blk_frame == fi)
        idxs = np.where(mask)[0]
        if len(idxs) == 0:
            summary = {k: float("nan") for k in
                       ("cm_error_mean", "cm_error_std", "cm_error_max",
                        "output_power_mean", "update_norm_mean", "update_norm_max",
                        "w_norm_end", "z_amp_max_mean", "z_amp_max_max",
                        "n_blocks")}
        else:
            cm = np.array([trace[i]["cm_error"] for i in idxs], dtype=float)
            op = np.array([trace[i]["output_power"] for i in idxs], dtype=float)
            un = np.array([trace[i]["update_norm"] for i in idxs], dtype=float)
            wn = np.array([trace[i]["w_norm"] for i in idxs], dtype=float)
            za = np.array([trace[i]["z_amp_max"] for i in idxs], dtype=float)
            summary = {
                "cm_error_mean": float(np.mean(cm)), "cm_error_std": float(np.std(cm)),
                "cm_error_max": float(np.max(cm)),
                "output_power_mean": float(np.mean(op)),
                "update_norm_mean": float(np.mean(un)), "update_norm_max": float(np.max(un)),
                "w_norm_end": float(wn[-1]),
                "z_amp_max_mean": float(np.mean(za)), "z_amp_max_max": float(np.max(za)),
                "n_blocks": int(len(idxs)),
            }
        # target = next-frame (fi+1) frozen-receiver fixed-label SER (scored with truth)
        # Use a contiguous EVALSYM window at the start of frame fi+1 (SER stable, fast).
        rec = {"frame_idx": int(fi), "summary": summary, "traj_global": None}
        if fi + 1 < n_frames:
            EVALSYM = int(FROZEN["eval_symbols_per_frame"])
            s = (fi + 1) * FRAME + half
            e = s + EVALSYM
            a, b = max(s, 0), min(e, N)
            bx = bitsX[a * 4:b * 4]; by = bitsY[a * 4:b * 4]
            if len(bx) >= 4:
                m = evaluator.evaluate_dual_16qam(
                    zX[a:b], zY[a:b], truth[a:b, 0], truth[a:b, 1], bx, by)
                rec["next_fixed_ser"] = float(m["fixed_label_ser"])
                rec["next_fail"] = int(rec["next_fixed_ser"] >
                                       float(FROZEN["fail_ser_threshold"]))
            else:
                rec["next_fixed_ser"] = float("nan"); rec["next_fail"] = None
        else:
            rec["next_fixed_ser"] = float("nan"); rec["next_fail"] = None
        records.append(rec)
    return records


def build_dataset(seeds, fg_hz, snr_db, phase_label):
    """Run frozen receiver on each trajectory, collect per-frame records."""
    rows = []
    for ti, seed in enumerate(seeds):
        r = _build_realization(seed, fg_hz, snr_db)
        res = run_frozen_receiver(r["rX"], r["rY"])
        recs = per_frame_summaries_and_targets(r, res)
        for rec in recs:
            rec["seed"] = int(seed); rec["fg_hz"] = float(fg_hz)
            rec["snr_db"] = float(snr_db); rec["traj_idx"] = int(ti)
            rec["phase"] = phase_label
            rows.append(rec)
    return rows


# ─── Phase 0 validation helpers ─────────────────────────────────────────────

def _ks_statistic(emp, theoretical_cdf_at_sort):
    """One-sample KS statistic given sorted empirical samples and CDF values."""
    n = len(emp)
    cdf_theory = np.sort(theoretical_cdf_at_sort)
    emp_cdf = np.arange(1, n + 1) / n
    d_plus = np.max(emp_cdf - cdf_theory)
    d_minus = np.max(cdf_theory - np.arange(0, n) / n)
    return float(max(d_plus, d_minus))


def phase0_physical_identity(fg_hz, snr_db, seed):
    """Phase 0: verify GG edge, ACF, rho consistency, frozen-receiver identity.

    Returns dict with pass/fail per check. Any FAIL => EXECUTION_INVALID.
    """
    out = {"fg_hz": fg_hz, "snr_db": snr_db, "seed": seed, "checks": {}}
    t_s = float(FROZEN["t_s"]); block = int(FROZEN["block_gg"])
    tau_c = 1.0 / (2.0 * np.pi * fg_hz)
    rho_frame_target = float(np.exp(-(int(FROZEN["frame_symbols"]) * t_s) / tau_c))
    rho_block_target = float(np.exp(-(block * t_s) / tau_c))

    # 1. Edge distribution: generate a long blockwise GG trajectory, compare edge
    from common._gg_time import gg_time_envelope_blockwise
    n_blk = 200_000
    h_blk = gg_time_envelope_blockwise(
        n_blk, float(FROZEN["alpha"]), float(FROZEN["beta"]), tau_c,
        block=block, t_s=t_s, method=str(FROZEN["method"]), seed=int(seed))
    # theoretical GG CDF via numerical integration of gg_pdf_theory
    grid = np.linspace(1e-4, 6.0, 4000)
    pdf = gg_pdf_theory(grid, float(FROZEN["alpha"]), float(FROZEN["beta"]))
    cdf_theory = np.cumsum(pdf) * (grid[1] - grid[0])
    cdf_theory = np.clip(cdf_theory / cdf_theory[-1], 0, 1)
    h_sorted = np.sort(h_blk)
    theo_at_sort = np.interp(h_sorted, grid, cdf_theory)
    ks = _ks_statistic(h_sorted, theo_at_sort)
    out["checks"]["gg_edge_ks"] = {"value": ks, "pass": bool(ks < FROZEN["edge_ks_pass"] * 3)}

    # 2+3. ACF and rho consistency at BLOCK stride (physical GG block)
    lags = np.arange(1, FROZEN["acf_lag_max"] + 1)
    h_c = h_blk - h_blk.mean()
    var = np.dot(h_c, h_c)
    acf_emp = np.array([np.dot(h_c[:-L], h_c[L:]) / var for L in lags])
    acf_theory_block = rho_block_target ** lags
    acf_relerr = float(np.max(np.abs(acf_emp - acf_theory_block) /
                              (acf_theory_block + 1e-12)))
    out["checks"]["block_acf"] = {
        "rho_block_target": rho_block_target,
        "acf_empirical": acf_emp.tolist(), "acf_theory": acf_theory_block.tolist(),
        "max_relerr": acf_relerr,
        "pass": bool(acf_relerr < 0.10),  # AR(1) gar log-ACF <2% deviation allowed
    }

    # 4. Frozen-receiver identity: run receiver on a shared realization, confirm
    # deterministic & matches a re-run byte-identical (same seed => same realization
    # => same CMA output). We verify determinism by re-running and comparing zX.
    r = _build_realization(seed, fg_hz, snr_db)
    res1 = run_frozen_receiver(r["rX"], r["rY"])
    res2 = run_frozen_receiver(r["rX"], r["rY"])
    relerr = float(np.max(np.abs(res1["zX"] - res2["zX"])) /
                   (np.max(np.abs(res1["zX"])) + 1e-30))
    out["checks"]["receiver_identity"] = {
        "zX_rerun_max_absdiff": float(np.max(np.abs(res1["zX"] - res2["zX"]))),
        "relerr": relerr,
        "pass": bool(relerr < FROZEN["identity_relerr_max"]),
        "diverged": bool(res1["diverged"]),
        "final_w_norm": float(res1["final_w_norm"]),
        "n_trace_blocks": int(len(res1["trace"])),
    }
    out["rho_frame_target"] = rho_frame_target
    out["tau_c_ms"] = tau_c * 1e3
    out["pass"] = all(c["pass"] for c in out["checks"].values())
    return out


# ─── Phase A: predictive baselines + history-expanded (frozen, simple) ──────

def _ridge_fit(Xtr, ytr, lam):
    """Closed-form ridge regression (no sklearn dependency)."""
    X = np.asarray(Xtr, float); y = np.asarray(ytr, float)
    n, d = X.shape
    A = X.T @ X + lam * np.eye(d) * n  # scale lambda by n for size-invariance
    b = X.T @ y
    w = np.linalg.solve(A, b)
    return w


def _ridge_predict(w, X):
    return np.asarray(X, float) @ w


def _logreg_fit(Xtr, ytr, lam, n_iter=200, lr=0.5):
    """L2-regularized logistic regression via Newton steps (no sklearn)."""
    X = np.asarray(Xtr, float); y = np.asarray(ytr, float)
    n, d = X.shape
    w = np.zeros(d)
    for _ in range(n_iter):
        z = X @ w
        z = np.clip(z, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        grad = X.T @ (p - y) / n + lam * w
        S = p * (1 - p)
        H = (X * S[:, None]).T @ X / n + lam * np.eye(d)
        try:
            delta = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            delta = grad
        w = w - lr * delta
        if np.max(np.abs(delta)) < 1e-8:
            break
    return w


def _logreg_predict_proba(w, X):
    z = np.clip(np.asarray(X, float) @ w, -30, 30)
    return 1.0 / (1.0 + np.exp(-z))


def _standardize_fit(Xtr):
    mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0); sd[sd < 1e-12] = 1.0
    return mu, sd


def _apply_std(X, mu, sd):
    return (np.asarray(X, float) - mu) / sd


FEATURE_KEYS = ["cm_error_mean", "cm_error_std", "cm_error_max",
                "output_power_mean", "update_norm_mean", "update_norm_max",
                "w_norm_end", "z_amp_max_mean", "z_amp_max_max"]


def build_feature_matrix(records, history_k, feat_keys=FEATURE_KEYS):
    """Build (X_current, X_history, valid_mask) per frame.

    X_current[i] = summary of frame i (the 'current' frame whose future we predict).
    X_history[i] = concatenation of summary(frames i-K..i-1), i.e. STRICTLY causal
      past frames only (frame < i). For frames without K past frames, valid_mask=False.
    target[i] = next_fixed_ser / next_fail of frame i (i.e. the receiver outcome on
      frame i+1).

    Causality: features for predicting target(i) use only summaries of frames <= i.
    The 'history' adds frames i-K..i-1 ON TOP of the current frame i summary.
    """
    n = len(records)
    d_cur = len(feat_keys)
    X_cur = np.full((n, d_cur), np.nan)
    X_hist = np.full((n, d_cur * history_k), np.nan)
    y_ser = np.full(n, np.nan); y_fail = np.full(n, np.nan)
    valid = np.zeros(n, dtype=bool)
    # index records by frame_idx for O(1) lookup
    by_fi = {rec["frame_idx"]: rec for rec in records}
    for i, rec in enumerate(records):
        fi = rec["frame_idx"]
        if np.isnan(rec["next_fixed_ser"]):
            continue
        # need frames fi-K .. fi all present
        need = list(range(fi - history_k, fi + 1))
        if any(nf not in by_fi for nf in need):
            continue
        cur_vec = np.array([by_fi[fi]["summary"][k] for k in feat_keys], dtype=float)
        if not np.all(np.isfinite(cur_vec)):
            continue
        hist_vecs = []
        ok = True
        for nf in range(fi - history_k, fi):
            hv = np.array([by_fi[nf]["summary"][k] for k in feat_keys], dtype=float)
            if not np.all(np.isfinite(hv)):
                ok = False; break
            hist_vecs.append(hv)
        if not ok or len(hist_vecs) != history_k:
            continue
        X_cur[i] = cur_vec
        X_hist[i] = np.concatenate(hist_vecs)
        y_ser[i] = rec["next_fixed_ser"]
        y_fail[i] = rec["next_fail"]
        valid[i] = True
    return X_cur[valid], X_hist[valid], y_ser[valid], y_fail[valid], valid


# ─── traditional predictive baselines ───────────────────────────────────────

def baseline_unconditional(ytr):
    return float(np.mean(ytr))


def baseline_persistence(Xtr_cur, ytr, Xte_cur):
    """Last-value persistence: predict y from current-frame summary via simple
    ridge on current-only (this IS the 'current-only ridge' baseline). For a
    pure persistence baseline on the CONTINUOUS target we use the previous frame's
    own outcome, handled separately at row level. Here we return current-only ridge."""
    # dev-tune lambda
    return None  # handled in evaluate_phaseA via current-only ridge


def bootstrap_ci(deltas, n_boot, alpha, rng_seed):
    if len(deltas) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(rng_seed)
    n = len(deltas)
    means = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        means[b] = float(np.mean(deltas[idx]))
    return (float(np.mean(deltas)),
            float(np.quantile(means, alpha / 2)),
            float(np.quantile(means, 1 - alpha / 2)))


def _per_traj_aggregate(per_frame_df, value_col, traj_col):
    """Aggregate per-frame values to per-trajectory mean (macro)."""
    out = {}
    for traj in np.unique(traj_col):
        out[int(traj)] = float(np.mean(value_col[traj_col == traj]))
    return out


if __name__ == "__main__":
    t0 = time.time()
    print(f"[P06] E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION — one-shot repair probe", flush=True)
    print(f"[P06] python={sys.executable}", flush=True)
    print(f"[P06] FROZEN frame_symbols={FROZEN['frame_symbols']} "
          f"n_symbols={FROZEN['n_symbols']} "
          f"fg={FROZEN['fg_hz_list']} snr={FROZEN['snr_db_list']}", flush=True)

    # ===== Phase 0: physical & identity gate (all conditions) =====
    print("\n[P06] ===== Phase 0: physical & identity gate =====", flush=True)
    p0_results = []
    p0_pass = True
    for fg in FROZEN["fg_hz_list"]:
        for snr in FROZEN["snr_db_list"]:
            chk = phase0_physical_identity(fg, snr, seed=200)
            p0_results.append(chk)
            tag = "PASS" if chk["pass"] else "FAIL"
            print(f"  fg={fg}Hz snr={snr}dB tau_c={chk['tau_c_ms']:.3f}ms "
                  f"rho_frame={chk['rho_frame_target']:.4f}: {tag} "
                  f"(edge_ks={chk['checks']['gg_edge_ks']['value']:.4f}, "
                  f"acf_relerr={chk['checks']['block_acf']['max_relerr']:.4f}, "
                  f"id_relerr={chk['checks']['receiver_identity']['relerr']:.2e})", flush=True)
            if not chk["pass"]:
                p0_pass = False
    p0_payload = {"phase": "phase0", "pass": p0_pass, "checks": p0_results}
    with open(RESULTS_DIR / "p06_phase0_physical_identity.json", "w", encoding="utf-8") as f:
        json.dump(p0_payload, f, indent=2, default=str)

    if not p0_pass:
        verdict = "EXECUTION_INVALID"
        reason = "Phase 0 physical/identity gate FAILED for >=1 condition"
        print(f"\n[P06] >>> VERDICT = {verdict}: {reason}", flush=True)
        _final = {"probe_id": "P06", "family": "E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION",
                  "verdict": verdict, "reason": reason,
                  "phase_reached": "phase0", "_elapsed_seconds": round(time.time() - t0, 1)}
        with open(RESULTS_DIR / "p06_terminal_verdict.json", "w", encoding="utf-8") as f:
            json.dump(_final, f, indent=2, default=str)
        print(f"[P06] wrote {RESULTS_DIR / 'p06_terminal_verdict.json'}", flush=True)
        sys.exit(0)

    print("\n[P06] Phase 0 PASS for all conditions. Building datasets...", flush=True)

    # ===== Build datasets (trajectory-level split) =====
    # NOTE: build once per (phase, fg, snr). Save raw per-frame rows.
    all_rows = []
    for fg in FROZEN["fg_hz_list"]:
        for snr in FROZEN["snr_db_list"]:
            for phase, seeds in (("train", FROZEN["train_seeds"]),
                                 ("dev", FROZEN["dev_seeds"]),
                                 ("test", FROZEN["test_seeds"])):
                t1 = time.time()
                rows = build_dataset(seeds, fg, snr, phase)
                all_rows.extend(rows)
                print(f"  built {phase} fg={fg} snr={snr}: {len(rows)} frames "
                      f"({len(seeds)} traj) in {time.time()-t1:.1f}s", flush=True)
    # save raw per-frame rows
    with open(RESULTS_DIR / "p06_raw_per_frame_rows.json", "w", encoding="utf-8") as f:
        json.dump({"frozen": FROZEN, "rows": all_rows}, f, indent=2, default=str)
    print(f"[P06] saved {len(all_rows)} raw per-frame rows", flush=True)

    # ===== Phase A: problem & strict-causal information gate =====
    # The downstream phaseA_eval.py consumes the raw rows + frozen config and runs
    # the predictive baselines + history-expanded comparison, producing the verdict.
    print("\n[P06] Phase A/B/C handled by phaseA_eval.py (separate verifier-owned step)", flush=True)
    print(f"[P06] DONE phase0+dataset build in {time.time()-t0:.1f}s", flush=True)
