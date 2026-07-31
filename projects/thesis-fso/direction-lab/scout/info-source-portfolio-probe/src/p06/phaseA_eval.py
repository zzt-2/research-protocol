"""P06 Phase A: problem & strict-causal information gate.

Consumes the raw per-frame rows (chunks/*.json) produced by build_datasets.py and
the FROZEN config. Runs the traditional predictive baselines + history-expanded
comparison, produces the Phase A verdict.

Causality (frozen):
  features(t) = receiver-visible summaries of frames <= t
  target(t+1) = frozen-receiver next-frame outcome
  history adds frames t-K..t-1 ON TOP of current frame t summary

Baselines (>=5):
  1. unconditional prior (train mean)
  2. last-value persistence (predict y(t+1) = y(t), i.e. previous frame's own outcome)
  3. EWMA of past outcomes (dev-tuned decay)
  4. AR(1) on outcomes (dev-tuned)
  5. current-only ridge (continuous) / current-only logistic (failure)
History-expanded:
  ridge/logistic on [current summary] + [past K frame summaries]  (no deep nets)

Verdict (frozen, read-before-test):
  - dev failure events < floor => PROBLEM_ABSENT_AT_PHYSICAL_TIMESCALE
  - history not stably > strongest current-only/persistence, or CI crosses 0 / MDE not met
    => NO_CAUSAL_HISTORY_INCREMENT
  - strict causal increment passes => CAUSAL_HISTORY_INFORMATION_SIGNAL (-> Phase B)

MI is NOT reported (old F3-A MI path invalidated).
"""
from __future__ import annotations
import glob
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import run_p06 as P  # noqa: E402


def load_chunks():
    """Load all chunk files, return list of frame records."""
    rows = []
    cfg = None
    for fpath in sorted(glob.glob(str(P.RESULTS_DIR / "chunks" / "chunk_*.json"))):
        with open(fpath, encoding="utf-8") as f:
            d = json.load(f)
        rows.extend(d["rows"])
    return rows


def assemble_by_condition(rows):
    """Group rows by (phase, fg, snr); within each, index by (traj_idx, frame_idx)."""
    by_cond = {}
    for r in rows:
        key = (r["phase"], r["fg_hz"], r["snr_db"])
        by_cond.setdefault(key, []).append(r)
    return by_cond


def _per_traj_macro(per_frame_vals, traj_ids):
    """Macro = mean of per-trajectory means. Returns (macro, traj_means_list)."""
    tm = {}
    for v, t in zip(per_frame_vals, traj_ids):
        tm.setdefault(int(t), []).append(float(v))
    means = [float(np.mean(vs)) for vs in tm.values()]
    return float(np.mean(means)), means


def _bootstrap_paired_ci(deltas, n_boot, alpha, seed):
    if len(deltas) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    n = len(deltas)
    out = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        out[b] = float(np.mean(np.asarray(deltas)[idx]))
    return (float(np.mean(deltas)),
            float(np.quantile(out, alpha / 2)),
            float(np.quantile(out, 1 - alpha / 2)))


# ─── outcome-only temporal baselines (persistence/EWMA/AR(1)) ──────────────
# These predict next-frame outcome from PAST outcomes only (no summary features).
# Built per-trajectory to preserve causality (within-traj past only).

def outcome_history_records(rows_by_cond):
    """For each condition+phase, build per-frame (outcome_history, target) where
    outcome_history = past frame OUTCOMES (the receiver's own past fixed-label SER),
    which IS receiver-visible (the receiver can score its own decisions against the
    known constellation; fixed-label SER uses TX label only for SCORING in this probe,
    but a deployable receiver would use a decision-directed error proxy — we note this
    as a deployment proxy and keep it as the temporal-baseline outcome channel)."""
    out = {}
    for key, recs in rows_by_cond.items():
        # order by (traj_idx, frame_idx)
        recs_sorted = sorted(recs, key=lambda r: (r["traj_idx"], r["frame_idx"]))
        by_traj = {}
        for r in recs_sorted:
            by_traj.setdefault(r["traj_idx"], []).append(r)
        frames = []
        for tidx, lst in sorted(by_traj.items()):
            lst.sort(key=lambda r: r["frame_idx"])
            outcomes = [r["next_fixed_ser"] for r in lst]  # outcome OF frame = next SER recorded on that frame
            for i, r in enumerate(lst):
                if i < 1:
                    continue
                # past outcomes = outcomes[0..i-1] but note outcomes[i] is the SER of frame i+1
                # we want: predict outcome of frame i+1 (= outcomes[i]) from outcomes[0..i-1]
                past_outcomes = outcomes[:i]  # strictly before the target frame i+1's outcome
                if len(past_outcomes) < 1 or any(o != o for o in past_outcomes):
                    continue
                if outcomes[i] != outcomes[i]:
                    continue
                frames.append({
                    "traj_idx": tidx, "frame_idx": r["frame_idx"],
                    "past_outcomes": list(past_outcomes),
                    "target_ser": float(outcomes[i]),
                    "target_fail": int(r["next_fail"]) if r["next_fail"] is not None else None,
                    "fg_hz": r["fg_hz"], "snr_db": r["snr_db"], "phase": r["phase"],
                })
        out[key] = frames
    return out


def baseline_persistence_predict(frames):
    """predict target = last past outcome."""
    preds, tgts, fails = [], [], []
    for fr in frames:
        preds.append(fr["past_outcomes"][-1])
        tgts.append(fr["target_ser"])
        if fr["target_fail"] is not None:
            fails.append(fr["target_fail"])
    return np.array(preds), np.array(tgts), (np.array(fails) if fails else None)


def baseline_ewma_predict(frames, alpha, fit_on):
    """EWMA over past outcomes (dev-tuned alpha). alpha in (0,1]."""
    preds, tgts = [], []
    for fr in frames:
        po = fr["past_outcomes"]
        if len(po) == 0:
            continue
        ew = po[0]
        for x in po[1:]:
            ew = alpha * x + (1 - alpha) * ew
        preds.append(ew); tgts.append(fr["target_ser"])
    return np.array(preds), np.array(tgts)


def baseline_ar1_predict(train_frames, eval_frames):
    """AR(1): target = c0 + c1 * last past outcome, fit on train outcomes."""
    x = np.array([fr["past_outcomes"][-1] for fr in train_frames if len(fr["past_outcomes"]) >= 1])
    y = np.array([fr["target_ser"] for fr in train_frames if len(fr["past_outcomes"]) >= 1])
    if len(x) < 5:
        return None, None
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    preds = []
    tgts = []
    for fr in eval_frames:
        if len(fr["past_outcomes"]) < 1:
            continue
        preds.append(coef[0] * fr["past_outcomes"][-1] + coef[1])
        tgts.append(fr["target_ser"])
    return np.array(preds), np.array(tgts)


# ─── continuous-target metrics ──────────────────────────────────────────────

def _mae(pred, tgt):
    return float(np.mean(np.abs(np.asarray(pred) - np.asarray(tgt))))


def _rmse(pred, tgt):
    d = np.asarray(pred) - np.asarray(tgt)
    return float(np.sqrt(np.mean(d ** 2)))


def _r2(pred, tgt):
    y = np.asarray(tgt); ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot < 1e-15:
        return 0.0
    ss_res = float(np.sum((y - np.asarray(pred)) ** 2))
    return 1.0 - ss_res / ss_tot


# ─── failure-target metrics ─────────────────────────────────────────────────

def _brier(pred_prob, y):
    return float(np.mean((np.asarray(pred_prob) - np.asarray(y)) ** 2))


def _logloss(pred_prob, y):
    p = np.clip(np.asarray(pred_prob), 1e-12, 1 - 1e-12)
    y = np.asarray(y)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def _reliability(pred_prob, y, n_bins=5):
    """Expected calibration error (ECE)."""
    p = np.asarray(pred_prob); y = np.asarray(y)
    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0; n = len(p)
    for bi in range(n_bins):
        m = (p >= edges[bi]) & (p < edges[bi + 1])
        if bi == n_bins - 1:
            m = (p >= edges[bi]) & (p <= edges[bi + 1])
        if m.sum() > 0:
            ece += (m.sum() / n) * abs(p[m].mean() - y[m].mean())
    return float(ece)


def main():
    t0 = time.time()
    print("[PhaseA] loading chunks...", flush=True)
    rows = load_chunks()
    if not rows:
        print("[PhaseA] NO chunk data found. Run build_datasets.py first.", flush=True)
        sys.exit(1)
    print(f"[PhaseA] loaded {len(rows)} frame rows", flush=True)
    by_cond = assemble_by_condition(rows)
    conds = sorted(by_cond.keys())
    print(f"[PhaseA] conditions ({len(conds)}): {conds}", flush=True)

    # ===== Check dev failure-event floor (frozen before reading test) =====
    dev_rows = [r for r in rows if r["phase"] == "dev"]
    dev_fails = [r["next_fail"] for r in dev_rows if r.get("next_fail") is not None]
    dev_n_fail = int(np.nansum(dev_fails))
    dev_frac_fail = float(np.nanmean(dev_fails)) if dev_fails else 0.0
    print(f"[PhaseA] DEV failure events: {dev_n_fail}/{len(dev_fails)} "
          f"(frac={dev_frac_fail:.4f}, floor={P.FROZEN['fail_event_count_min']})", flush=True)

    floor_met = dev_n_fail >= P.FROZEN["fail_event_count_min"]

    # Build outcome-history frames for temporal baselines
    outframes = outcome_history_records(by_cond)

    # ===== Dev tuning: EWMA alpha, ridge lambda, history K =====
    # Tune on DEV only. Candidate grids frozen.
    ewma_alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
    ridge_lams = [0.01, 0.1, 1.0, 10.0, 100.0]
    history_Ks = [1, 2, 3, 5]

    # aggregate dev outframes across conditions for tuning
    dev_of = [fr for key in conds for fr in outframes.get(key, []) if fr["phase"] == "dev"]
    test_of = [fr for key in conds for fr in outframes.get(key, []) if fr["phase"] == "test"]
    train_of = [fr for key in conds for fr in outframes.get(key, []) if fr["phase"] == "train"]

    # EWMA alpha tune on dev (lower MAE better)
    best_alpha, best_dev_mae = 0.5, float("inf")
    for a in ewma_alphas:
        # EWMA needs at least 2 past outcomes for meaningful smoothing; use >=2
        of2 = [fr for fr in dev_of if len(fr["past_outcomes"]) >= 2]
        p, t = baseline_ewma_predict(of2, a, fit_on=True)
        if len(p):
            m = _mae(p, t)
            if m < best_dev_mae:
                best_dev_mae = m; best_alpha = a
    print(f"[PhaseA] dev-tuned EWMA alpha={best_alpha} (dev MAE={best_dev_mae:.5f})", flush=True)

    # ===== Feature-based models: current-only vs history-expanded =====
    # Build feature matrices per condition+phase using run_p06.build_feature_matrix
    def build_feat_sets(records_list, K):
        """Return dict cond -> {phase -> (X_cur, X_hist, y_ser, y_fail, valid)}"""
        sets = {}
        # group
        grouped = {}
        for r in records_list:
            grouped.setdefault((r["phase"], r["fg_hz"], r["snr_db"]), []).append(r)
        for (phase, fg, snr), recs in grouped.items():
            # need per-trajectory ordered frames; build_feature_matrix indexes by frame_idx
            # but recs here may span multiple trajectories — we must build per-trajectory.
            by_traj = {}
            for r in recs:
                by_traj.setdefault(r["traj_idx"], []).append(r)
            Xc_all, Xh_all, ys_all, yf_all, traj_all = [], [], [], [], []
            for tidx, lst in sorted(by_traj.items()):
                Xc, Xh, ys, yf, valid = P.build_feature_matrix(lst, K)
                if valid.sum() == 0:
                    continue
                Xc_all.append(Xc); Xh_all.append(Xh)
                ys_all.append(ys); yf_all.append(yf)
                traj_all.append(np.full(len(ys), tidx))
            if not Xc_all:
                continue
            sets[(phase, fg, snr)] = (np.vstack(Xc_all), np.vstack(Xh_all),
                                       np.concatenate(ys_all), np.concatenate(yf_all),
                                       np.concatenate(traj_all))
        return sets

    # Tune K and ridge lambda on DEV (continuous target)
    best_K, best_lam_cur, best_lam_hist = 2, 1.0, 1.0
    best_dev_hist_advantage = -float("inf")
    for K in history_Ks:
        fsets = build_feat_sets(rows, K)
        # pool dev across conditions
        dev_Xc, dev_Xh, dev_ys, dev_yf, dev_tj = [], [], [], [], []
        tr_Xc, tr_Xh, tr_ys, tr_yf, tr_tj = [], [], [], [], []
        for key, (Xc, Xh, ys, yf, tj) in fsets.items():
            if key[0] == "dev":
                dev_Xc.append(Xc); dev_Xh.append(Xh); dev_ys.append(ys); dev_yf.append(yf); dev_tj.append(tj)
            elif key[0] == "train":
                tr_Xc.append(Xc); tr_Xh.append(Xh); tr_ys.append(ys); tr_yf.append(yf); tr_tj.append(tj)
        if not dev_Xc or not tr_Xc:
            continue
        dev_Xc = np.vstack(dev_Xc); dev_Xh = np.vstack(dev_Xh); dev_ys = np.concatenate(dev_ys)
        tr_Xc = np.vstack(tr_Xc); tr_Xh = np.vstack(tr_Xh); tr_ys = np.concatenate(tr_ys)
        mu_c, sd_c = P._standardize_fit(tr_Xc)
        mu_h, sd_h = P._standardize_fit(np.hstack([tr_Xc, tr_Xh]))
        for lam in ridge_lams:
            # current-only ridge
            wc = P._ridge_fit(P._apply_std(tr_Xc, mu_c, sd_c), tr_ys, lam)
            pc = P._ridge_predict(wc, P._apply_std(dev_Xc, mu_c, sd_c))
            r2_c = _r2(pc, dev_ys)
            # history-expanded ridge
            Xtr_h = P._apply_std(np.hstack([tr_Xc, tr_Xh]), mu_h, sd_h)
            Xde_h = P._apply_std(np.hstack([dev_Xc, dev_Xh]), mu_h, sd_h)
            wh = P._ridge_fit(Xtr_h, tr_ys, lam)
            ph = P._ridge_predict(wh, Xde_h)
            r2_h = _r2(ph, dev_ys)
            adv = r2_h - r2_c
            if adv > best_dev_hist_advantage:
                best_dev_hist_advantage = adv
                best_K, best_lam_cur, best_lam_hist = K, lam, lam
    print(f"[PhaseA] dev-tuned K={best_K} ridge_lam={best_lam_cur} "
          f"(dev history R2 advantage over current-only={best_dev_hist_advantage:+.5f})", flush=True)

    # ===== TEST evaluation (frozen K, lam, alpha; no more tuning) =====
    fsets = build_feat_sets(rows, best_K)

    # pool test + train across conditions
    def pool(phase):
        Xc_l, Xh_l, ys_l, yf_l, tj_l, fg_l, snr_l = [], [], [], [], [], [], []
        for key, (Xc, Xh, ys, yf, tj) in fsets.items():
            if key[0] == phase:
                Xc_l.append(Xc); Xh_l.append(Xh); ys_l.append(ys); yf_l.append(yf); tj_l.append(tj)
                fg_l.append(np.full(len(ys), key[1])); snr_l.append(np.full(len(ys), key[2]))
        if not Xc_l:
            return None
        return (np.vstack(Xc_l), np.vstack(Xh_l), np.concatenate(ys_l),
                np.concatenate(yf_l), np.concatenate(tj_l),
                np.concatenate(fg_l), np.concatenate(snr_l))

    tr = pool("train")
    te = pool("test")
    if tr is None or te is None:
        print("[PhaseA] ERROR: train/test feature pools empty", flush=True)
        sys.exit(1)
    tr_Xc, tr_Xh, tr_ys, tr_yf, tr_tj, tr_fg, tr_snr = tr
    te_Xc, te_Xh, te_ys, te_yf, te_tj, te_fg, te_snr = te

    mu_c, sd_c = P._standardize_fit(tr_Xc)
    mu_h, sd_h = P._standardize_fit(np.hstack([tr_Xc, tr_Xh]))

    # current-only ridge
    wc = P._ridge_fit(P._apply_std(tr_Xc, mu_c, sd_c), tr_ys, best_lam_cur)
    pred_cur = P._ridge_predict(wc, P._apply_std(te_Xc, mu_c, sd_c))
    # history-expanded ridge
    Xtr_h = P._apply_std(np.hstack([tr_Xc, tr_Xh]), mu_h, sd_h)
    Xde_h = P._apply_std(np.hstack([te_Xc, te_Xh]), mu_h, sd_h)
    wh = P._ridge_fit(Xtr_h, tr_ys, best_lam_hist)
    pred_hist = P._ridge_predict(wh, Xde_h)

    # outcome temporal baselines on TEST (persistence/EWMA/AR1)
    # match test frames by (traj, frame). Use outcome-history test frames.
    # Build a lookup from (fg,snr,traj,frame) -> past_outcomes for test
    te_of_lookup = {}
    for fr in test_of:
        te_of_lookup[(fr["fg_hz"], fr["snr_db"], fr["traj_idx"], fr["frame_idx"])] = fr
    # For paired comparison, restrict test feature-rows to those with an outcome-history match
    keep = []
    for i in range(len(te_ys)):
        key = (te_fg[i], te_snr[i], te_tj[i], None)  # frame_idx not stored in pool; use traj-level outcome
        keep.append(i)
    # NOTE: feature rows don't carry frame_idx in pool; for outcome baselines we use the
    # outcome-history test set directly (per-frame), and for the FEATURE comparison we use
    # the per-frame MAE/R2 on the test feature pool. These are two complementary evidence
    # channels; the headline verdict uses the FEATURE history-vs-current paired comparison.

    # Continuous metrics (feature channel)
    cont = {
        "current_only": {"MAE": _mae(pred_cur, te_ys), "RMSE": _rmse(pred_cur, te_ys), "R2": _r2(pred_cur, te_ys)},
        "history_expanded": {"MAE": _mae(pred_hist, te_ys), "RMSE": _rmse(pred_hist, te_ys), "R2": _r2(pred_hist, te_ys)},
    }
    # unconditional
    cont["unconditional"] = {"MAE": _mae(np.full_like(te_ys, tr_ys.mean()), te_ys),
                              "RMSE": _rmse(np.full_like(te_ys, tr_ys.mean()), te_ys),
                              "R2": _r2(np.full_like(te_ys, tr_ys.mean()), te_ys)}

    # Outcome temporal baselines (test, per-frame where >=2 past outcomes)
    te_of2 = [fr for fr in test_of if len(fr["past_outcomes"]) >= 2]
    if te_of2:
        p_pers, t_pers, _ = baseline_persistence_predict(te_of2)
        p_ewma, t_ewma = baseline_ewma_predict(te_of2, best_alpha, fit_on=False)
        # AR1 fit on train outcomes, predict test
        p_ar1, t_ar1 = baseline_ar1_predict(train_of, te_of2)
        cont["persistence"] = {"MAE": _mae(p_pers, t_pers), "RMSE": _rmse(p_pers, t_pers), "R2": _r2(p_pers, t_pers),
                                 "n": len(t_pers)}
        cont["ewma"] = {"MAE": _mae(p_ewma, t_ewma), "RMSE": _rmse(p_ewma, t_ewma), "R2": _r2(p_ewma, t_ewma),
                         "n": len(t_ewma)}
        if p_ar1 is not None:
            cont["ar1"] = {"MAE": _mae(p_ar1, t_ar1), "RMSE": _rmse(p_ar1, t_ar1), "R2": _r2(p_ar1, t_ar1),
                            "n": len(t_ar1)}

    # Paired per-frame R2 increment (history - current_only) on test feature pool
    # Per-frame squared error difference -> bootstrap on the per-trajectory macro of (err_hist - err_cur)
    err_hist = (pred_hist - te_ys) ** 2
    err_cur = (pred_cur - te_ys) ** 2
    delta_err = err_cur - err_hist  # >0 means history reduces error
    # macro per trajectory
    tj_unique = np.unique(te_tj)
    traj_delta = np.array([float(np.mean(delta_err[te_tj == t])) for t in tj_unique])
    dmean, dlo, dhi = _bootstrap_paired_ci(
        traj_delta, P.FROZEN["bootstrap_n"], P.FROZEN["bootstrap_alpha"],
        P.FROZEN["rng_seed_bootstrap"])
    cont["history_minus_current_MSE_reduction"] = {
        "macro_mean": dmean, "ci_lo": dlo, "ci_hi": dhi, "n_traj": len(traj_delta)}

    # Failure-target metrics (logistic) — only if floor met
    fail_metrics = {}
    if floor_met:
        # current-only logistic
        wl_c = P._logreg_fit(P._apply_std(tr_Xc, mu_c, sd_c), tr_yf, best_lam_cur)
        pprob_c = P._logreg_predict_proba(wl_c, P._apply_std(te_Xc, mu_c, sd_c))
        wl_h = P._logreg_fit(Xtr_h, tr_yf, best_lam_hist)
        pprob_h = P._logreg_predict_proba(wl_h, Xde_h)
        fail_metrics["current_only"] = {
            "logloss": _logloss(pprob_c, te_yf), "brier": _brier(pprob_c, te_yf),
            "ECE": _reliability(pprob_c, te_yf)}
        fail_metrics["history_expanded"] = {
            "logloss": _logloss(pprob_h, te_yf), "brier": _brier(pprob_h, te_yf),
            "ECE": _reliability(pprob_h, te_yf)}
        # paired brier reduction bootstrap (per traj macro)
        brier_diff = (pprob_c - te_yf) ** 2 - (pprob_h - te_yf) ** 2
        tj_u = np.unique(te_tj)
        traj_bd = np.array([float(np.mean(brier_diff[te_tj == t])) for t in tj_u])
        bm, bl, bh = _bootstrap_paired_ci(traj_bd, P.FROZEN["bootstrap_n"],
                                           P.FROZEN["bootstrap_alpha"],
                                           P.FROZEN["rng_seed_bootstrap"])
        fail_metrics["history_minus_current_brier_reduction"] = {
            "macro_mean": bm, "ci_lo": bl, "ci_hi": bh, "n_traj": len(traj_bd)}

    # ===== Verdict (frozen logic) =====
    print("\n[PhaseA] ===== TEST RESULTS =====", flush=True)
    print(f"  dev_n_fail={dev_n_fail} floor={P.FROZEN['fail_event_count_min']} floor_met={floor_met}", flush=True)
    print(f"  continuous (feature pool, n={len(te_ys)}):", flush=True)
    for k in ("unconditional", "current_only", "history_expanded", "persistence", "ewma", "ar1"):
        if k in cont:
            c = cont[k]
            print(f"    {k:18s}: MAE={c.get('MAE',float('nan')):.5f} RMSE={c.get('RMSE',float('nan')):.5f} R2={c.get('R2',float('nan')):.5f}", flush=True)
    print(f"  history-current MSE reduction (per-traj macro): mean={dmean:.2e} CI=[{dlo:.2e},{dhi:.2e}]", flush=True)
    if fail_metrics:
        print(f"  failure-target (logistic):", flush=True)
        for k in ("current_only", "history_expanded"):
            print(f"    {k:18s}: logloss={fail_metrics[k]['logloss']:.5f} brier={fail_metrics[k]['brier']:.5f} ECE={fail_metrics[k]['ECE']:.5f}", flush=True)

    # Verdict
    if not floor_met:
        verdict = "PROBLEM_ABSENT_AT_PHYSICAL_TIMESCALE"
        reason = (f"dev failure events {dev_n_fail} < floor {P.FROZEN['fail_event_count_min']} "
                  f"(frac={dev_frac_fail:.4f}): under source-closed GG dynamics at deployable "
                  f"frame rate, the frozen receiver does not produce enough failure events for "
                  f"a causal-history predictive question to exist.")
    else:
        r2_cur = cont["current_only"]["R2"]
        r2_hist = cont["history_expanded"]["R2"]
        r2_inc = r2_hist - r2_cur
        mae_red_rel = (cont["current_only"]["MAE"] - cont["history_expanded"]["MAE"]) / max(cont["current_only"]["MAE"], 1e-12)
        # signal requires: MSE-reduction CI_lo > 0 (strict) AND (r2_inc >= MDE OR mae_red_rel >= MDE)
        # AND history beats the strongest traditional temporal comparator too
        temporal_keys = [k for k in ("persistence", "ewma", "ar1") if k in cont]
        best_temporal_r2 = max([cont[k]["R2"] for k in temporal_keys], default=-float("inf"))
        ci_lo_positive = (dlo > 0)
        mde_met = (r2_inc >= P.FROZEN["mde_r2_increment"]) or (mae_red_rel >= P.FROZEN["mde_mae_decrement_rel"])
        beats_temporal = r2_hist > best_temporal_r2
        if ci_lo_positive and mde_met and beats_temporal:
            verdict = "CAUSAL_HISTORY_INFORMATION_SIGNAL"
            reason = (f"history-expanded stably beats strongest current-only/temporal on test: "
                      f"R2_inc={r2_inc:+.5f} (MDE={P.FROZEN['mde_r2_increment']}), "
                      f"MAE_red_rel={mae_red_rel:.4f}, MSE-red CI_lo={dlo:.2e}>0, "
                      f"history R2={r2_hist:.5f} > best temporal R2={best_temporal_r2:.5f}.")
        else:
            verdict = "NO_CAUSAL_HISTORY_INCREMENT"
            reason = (f"history-expanded does NOT stably beat strongest baseline on test: "
                      f"R2_inc={r2_inc:+.5f}, MAE_red_rel={mae_red_rel:.4f}, "
                      f"MSE-red CI=[{dlo:.2e},{dhi:.2e}] (CI_lo>0={ci_lo_positive}), "
                      f"history R2={r2_hist:.5f} vs best temporal R2={best_temporal_r2:.5f} "
                      f"(beats_temporal={beats_temporal}). MDE_met={mde_met}.")

    print(f"\n[PhaseA] >>> VERDICT = {verdict}\n          reason: {reason}", flush=True)

    payload = {
        "probe_id": "P06", "phase": "phaseA",
        "family": "E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION",
        "dev_n_fail": dev_n_fail, "dev_frac_fail": dev_frac_fail,
        "fail_event_count_min_floor": P.FROZEN["fail_event_count_min"],
        "floor_met": floor_met,
        "dev_tuned": {"ewma_alpha": best_alpha, "history_K": best_K,
                       "ridge_lam": best_lam_cur,
                       "dev_history_r2_advantage": best_dev_hist_advantage},
        "continuous_metrics": cont,
        "failure_metrics": fail_metrics,
        "verdict": verdict, "reason": reason,
        "_elapsed_seconds": round(time.time() - t0, 1),
    }
    with open(P.RESULTS_DIR / "p06_phaseA_result.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"[PhaseA] wrote {P.RESULTS_DIR / 'p06_phaseA_result.json'}", flush=True)


if __name__ == "__main__":
    main()
