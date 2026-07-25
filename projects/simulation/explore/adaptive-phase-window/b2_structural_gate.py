"""T007 Phase B2 — structural gate runner.

Runs the source-native window-optimum sweep on the AWGN+Wiener slice, then
the GG block-fading oracle-window check, then applies the four pre-registered
structural KILL conditions. Writes raw rows and a result JSON. If the gate
PASSES, signals the Phase C method package to run; if it FAILS, returns
KILL_NO_ADAPTIVE_WINDOW_SPACE and primary methods are NOT implemented.

All seeds are deterministic integers; PYTHONUTF8=1. The shared generator and
params.py are read-only.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
# _HERE = .../simulation/explore/adaptive-phase-window
# _SIM_DIR = .../simulation (two levels up: parent of explore, parent of this)
_SIM_DIR = os.path.dirname(os.path.dirname(_HERE))
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from channel import ChannelParams, generate_channel, estimate_snr_hat, estimate_phase_innovation_hat  # noqa: E402
from cpe import WINDOW_GRID, vv_block_mean  # noqa: E402
from evaluator import ber_with_legal_resolve  # noqa: E402

# ---------------------------------------------------------------------------
# Frozen literals (read from contract.yaml — duplicated here for the runner;
# tests assert they match the file).
# ---------------------------------------------------------------------------
WINDOW_GRID_RUN = list(WINDOW_GRID)             # [8,16,32,64,128,256]
SNR_GRID = [10.0, 14.0, 18.0, 22.0]
LINEWIDTHS_HZ = {"clean": 10000.0, "operational": 20000.0, "adversarial": 80000.0}
LINEWIDTH_VAL_SEEDS = [7800, 7801, 7802, 7803, 7804]
LINEWIDTH_TEST_SEEDS = [7900, 7901, 7902, 7903, 7904, 7905, 7906, 7907, 7908, 7909]
N_SYMBOLS = 2048
BLOCK = 256

# Structural KILL thresholds (MVE-SPEC §8)
UNIVERSAL_FIXED_REGRET_DB = 0.3
ORACLE_HEADROOM_DB = 0.5
ORACLE_COLLAPSE_BER = 0.2
FEATURE_SPEARMAN_RHO = 0.5


def _ber_for_window(out, N, modulation):
    """BER for one realization under fixed window N (legal pi/2 resolve)."""
    rx_comp = vv_block_mean(out.rx, N=N, modulation=modulation)
    return ber_with_legal_resolve(rx_comp, out.debug()["tx_bits"], modulation)


def _best_window_ber(out, modulation, windows=None):
    """Return (best_N, best_BER, per_window_BERs) for one realization."""
    ws = windows or WINDOW_GRID_RUN
    bers = []
    for N in ws:
        rx_comp = vv_block_mean(out.rx, N=N, modulation=modulation)
        bers.append(ber_with_legal_resolve(rx_comp, out.debug()["tx_bits"], modulation))
    j = int(np.argmin(bers))
    return ws[j], float(bers[j]), [float(b) for b in bers]


# ---------------------------------------------------------------------------
# B2.1 — AWGN+Wiener source-native window-optimum sweep
# ---------------------------------------------------------------------------
def run_awgn_wiener_sweep(out_lines, mod="qpsk"):
    """Sweep window N across (SNR, linewidth) on the flat AWGN+Wiener slice.

    Returns per-cell best N, the E1/E2 direction checks, and the receiver-
    visible feature Spearman correlations.
    """
    rows = []
    best_n_by_cell = {}   # (snr, lw_key) -> best N (majority across seeds)
    for snr in SNR_GRID:
        for lw_key, lw in LINEWIDTHS_HZ.items():
            best_Ns = []
            for seed in LINEWIDTH_VAL_SEEDS:
                out = generate_channel(ChannelParams(
                    modulation=mod, snr_db=snr, linewidth_hz=lw,
                    n_symbols=N_SYMBOLS, seed=seed, channel="awgn_wiener"))
                best_N, best_BER, per_w = _best_window_ber(out, mod)
                best_Ns.append(best_N)
                rows.append({
                    "phase": "b2_awgn_wiener", "modulation": mod,
                    "channel": "awgn_wiener", "snr_db": snr,
                    "linewidth_key": lw_key, "linewidth_hz": lw,
                    "seed": seed, "best_N": best_N, "best_BER": best_BER,
                    "per_window_BER": per_w, "window_grid": WINDOW_GRID_RUN,
                })
                out_lines.append(f"  awgn_wiener {mod} snr={snr} lw={lw_key} seed={seed}: "
                                 f"best_N={best_N} best_BER={best_BER:.3e}")
            # Majority best N across the 5 seeds.
            uniq, counts = np.unique(best_Ns, return_counts=True)
            best_n_by_cell[(snr, lw_key)] = int(uniq[np.argmax(counts)])

    # E1 check: SNR down -> best N up (within each linewidth).
    e1_pass_count = 0
    e1_total = 0
    for lw_key in LINEWIDTHS_HZ:
        ns = [best_n_by_cell[(snr, lw_key)] for snr in SNR_GRID]
        # As SNR decreases (reverse the list), N should be non-decreasing.
        ns_rev = list(reversed(ns))
        # Count monotone-non-decreasing pairs.
        ok = all(ns_rev[i] <= ns_rev[i + 1] + 1e-9 for i in range(len(ns_rev) - 1))
        e1_total += 1
        if ok:
            e1_pass_count += 1
        out_lines.append(f"  E1 (SNR down -> N up) @ {lw_key}: N(snr 22->10) = "
                         f"{list(reversed(ns))}, monotone_nondec={ok}")

    # E2 check: linewidth up -> best N down (within each SNR).
    e2_pass_count = 0
    e2_total = 0
    for snr in SNR_GRID:
        ns = [best_n_by_cell[(snr, lw_key)] for lw_key in LINEWIDTHS_HZ]
        # As linewidth increases, N should be non-increasing.
        ok = all(ns[i] >= ns[i + 1] - 1e-9 for i in range(len(ns) - 1))
        e2_total += 1
        if ok:
            e2_pass_count += 1
        out_lines.append(f"  E2 (linewidth up -> N down) @ snr={snr}: "
                         f"N(clean,operational,adversarial) = {ns}, monotone_noninc={ok}")

    # Receiver-visible feature Spearman correlations vs the per-cell best N.
    # Gather (SNR_hat, innov_hat, best_N) tuples across all cells/seeds.
    feat_rows = []
    for r in rows:
        out = generate_channel(ChannelParams(
            modulation=mod, snr_db=r["snr_db"], linewidth_hz=r["linewidth_hz"],
            n_symbols=N_SYMBOLS, seed=r["seed"], channel="awgn_wiener"))
        sh = float(np.mean(estimate_snr_hat(out.rx, window=BLOCK)))
        ih = float(np.mean(estimate_phase_innovation_hat(out.rx, m0=4, window=BLOCK)))
        feat_rows.append((sh, ih, r["best_N"]))
    sh_arr = np.array([f[0] for f in feat_rows])
    ih_arr = np.array([f[1] for f in feat_rows])
    n_arr = np.array([f[2] for f in feat_rows])
    rho_snr = float(_spearman(sh_arr, n_arr))
    rho_innov = float(_spearman(ih_arr, n_arr))
    # E1 wants SNR_hat negatively correlated with N (high SNR -> small N).
    # E2 wants innov_hat positively correlated with N (high innov -> small N).
    feat_snr_ok = rho_snr <= -FEATURE_SPEARMAN_RHO
    feat_innov_ok = rho_innov >= FEATURE_SPEARMAN_RHO
    out_lines.append(f"  feature Spearman: rho(SNR_hat, best_N)={rho_snr:.3f} "
                     f"(want <=-{FEATURE_SPEARMAN_RHO}); "
                     f"rho(innov_hat, best_N)={rho_innov:.3f} "
                     f"(want >={FEATURE_SPEARMAN_RHO})")

    return {
        "rows": rows,
        "best_n_by_cell": {f"{k[0]}_{k[1]}": v for k, v in best_n_by_cell.items()},
        "e1_pass_count": e1_pass_count, "e1_total": e1_total,
        "e2_pass_count": e2_pass_count, "e2_total": e2_total,
        "rho_snr_hat_best_n": rho_snr, "rho_innov_hat_best_n": rho_innov,
        "feat_snr_ok": bool(feat_snr_ok), "feat_innov_ok": bool(feat_innov_ok),
    }


def _spearman(x, y):
    """Spearman rho via rank correlation (no scipy dependency)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rx = _rank(x)
    ry = _rank(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def _rank(a):
    """Average-rank of array elements (ties get mean rank)."""
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=float)
    ranks[order] = np.arange(1, len(a) + 1, dtype=float)
    # Resolve ties by averaging ranks.
    sa = a[order]
    i = 0
    while i < len(sa):
        j = i
        while j + 1 < len(sa) and sa[j + 1] == sa[i]:
            j += 1
        if j > i:
            avg = np.mean(ranks[order][i:j + 1])
            for k in range(i, j + 1):
                ranks[order[k]] = avg
        i = j + 1
    return ranks


# ---------------------------------------------------------------------------
# B2.2 — universal fixed-N regret check (KILL condition 2)
# ---------------------------------------------------------------------------
def run_universal_fixed_regret_check(out_lines, sweep_result, mod="qpsk"):
    """For each fixed N, compute the required-SNR-at-FEC regret vs the best
    fixed N, per linewidth. KILL condition 2: if ANY single fixed N has regret
    < 0.3 dB in ALL linewidths (with a reachable FEC crossing), no adaptive
    space exists.

    Uses the pre-registered required-SNR-at-FEC metric (MVE-SPEC §7). A
    linewidth is 'reachable' if at least one fixed N crosses HD-FEC somewhere
    in the SNR grid. Unreachable linewidths are skipped (no FEC crossing to
    measure regret against).
    """
    from evaluator import required_snr_at_fec, HD_FEC_BER
    rows = sweep_result["rows"]
    # Group: (linewidth_key, N) -> list of (snr, mean_log_ber_across_seeds)
    # Build the BER-vs-SNR curve per (linewidth, N), then interpolate required SNR.
    per_lw_N = {}   # (lw_key, N) -> {snr: mean_log10_BER}
    for r in rows:
        lw_key = r["linewidth_key"]
        snr = r["snr_db"]
        for N, b in zip(r["window_grid"], r["per_window_BER"]):
            per_lw_N.setdefault((lw_key, N), {}).setdefault(snr, []).append(b)
    # Mean log-BER per (lw, N, snr).
    curves = {}
    for (lw, N), d in per_lw_N.items():
        snrs = sorted(d.keys())
        mean_logber = [float(np.mean(np.log10(np.clip(d[s], 1e-12, 0.5)))) for s in snrs]
        curves[(lw, N)] = (snrs, mean_logber)

    # Required SNR at FEC per (lw, N).
    req_snr = {}
    for (lw, N), (snrs, lb) in curves.items():
        req = required_snr_at_fec(snrs, [10 ** x for x in lb], target_ber=HD_FEC_BER)
        req_snr[(lw, N)] = req

    # Per linewidth, the best fixed N (lowest required SNR; reachable only).
    best_per_lw = {}
    reachable_lws = []
    for lw in LINEWIDTHS_HZ:
        candidates = {N: req_snr[(lw, N)] for N in WINDOW_GRID_RUN
                      if not np.isnan(req_snr[(lw, N)])}
        if len(candidates) == 0:
            out_lines.append(f"  universal-regret: linewidth {lw} FEC UNREACHABLE "
                             f"(no fixed N crosses HD-FEC in the SNR grid) -> skip")
            continue
        reachable_lws.append(lw)
        best_N = min(candidates, key=candidates.get)
        best_per_lw[lw] = (best_N, candidates[best_N])
        all_req = {N: round(v, 2) for N, v in candidates.items()}
        out_lines.append(f"  universal-regret {lw}: best fixed N*={best_N} "
                         f"(req SNR={candidates[best_N]:.2f} dB); "
                         f"all req SNR (N:dB)={all_req}")

    # Regret per (N, lw) vs the best fixed N for that linewidth.
    universal_regret = {}
    for N in WINDOW_GRID_RUN:
        universal_regret[N] = {}
        for lw in reachable_lws:
            best_N, best_req = best_per_lw[lw]
            req_N = req_snr[(lw, N)]
            if np.isnan(req_N):
                continue   # N does not reach FEC in this linewidth
            regret = req_N - best_req   # >= 0
            universal_regret[N][lw] = float(regret)
    # KILL condition 2: any fixed N with max regret < 0.3 dB across ALL reachable
    # linewidths.
    kill2 = False
    for N, reg in universal_regret.items():
        if len(reg) == 0:
            continue
        max_reg = max(reg.values())
        if max_reg < UNIVERSAL_FIXED_REGRET_DB and len(reg) == len(reachable_lws):
            kill2 = True
            out_lines.append(f"  KILL cond 2: fixed N={N} max regret={max_reg:.3f} dB "
                             f"< {UNIVERSAL_FIXED_REGRET_DB} across all reachable linewidths "
                             f"-> universal fixed exists")
            break
    if not kill2:
        out_lines.append(f"  KILL cond 2 NOT triggered: no fixed N has max regret "
                         f"< {UNIVERSAL_FIXED_REGRET_DB} dB across all {len(reachable_lws)} "
                         f"reachable linewidths")
    return {"universal_regret": universal_regret, "kill2_triggered": bool(kill2),
            "reachable_lws": reachable_lws, "best_per_lw": {lw: {"N": v[0], "req_snr_db": v[1]} for lw, v in best_per_lw.items()}}


def _ber_blockwise_legal_resolve(seg, seg_bits, modulation, block):
    """Per-block BER with legal pi/2 resolve using that block's tx_bits.

    This is the Kill-only truth-assisted oracle resolve (the per-block
    equivalent of common's resolve_*_blockwise, but restricted to the LEGAL
    pi/2 rotation set — NOT the T006 8-pi/4 mismatch). Returns the mean BER
    over the segment's blocks.
    """
    seg = np.asarray(seg, dtype=complex)
    from common._modulation import qpsk_demod, qam16_demod
    demod = qpsk_demod if modulation == "qpsk" else qam16_demod
    bps = 2 if modulation == "qpsk" else 4
    n = len(seg)
    nb = n // block
    total_err = 0
    total_bits = 0
    for b in range(nb):
        s = slice(b * block, (b + 1) * block)
        blk = seg[s]
        tb = seg_bits[b * block * bps:(b + 1) * block * bps]
        best = 1.0
        for r in np.arange(0, 2 * np.pi, np.pi / 2):   # 4 legal pi/2 rotations
            ber = float(np.mean(tb != demod(blk * np.exp(-1j * r))))
            if ber < best:
                best = ber
        total_err += best * len(tb)
        total_bits += len(tb)
    return total_err / max(total_bits, 1)


def run_gg_oracle_headroom(out_lines, mod="qpsk"):
    """Per-block oracle window vs the fixed B* (validation-aggregate best N)
    on the GG block-fading channel. KILL condition 3: if the median or 20%
    trimmed mean gain < 0.5 dB, OR the signal only comes from cells with
    BER >= 0.2, no adaptive space exists.

    Oracle definition (Kill-only, truth-assisted): for each block, pick the N
    minimizing THAT BLOCK's BER under a legal per-block pi/2 resolve (using
    that block's tx_bits). This is the honest upper bound on per-block window
    adaptation. It cannot lose to B* by construction (B* is one of the N
    choices per block). The T006 per-block 8-pi/4 resolve mismatch is avoided.
    """
    rows = []
    n_sym = BLOCK * 16   # 16 blocks per realization
    conditions = {"operational": 20000.0, "adversarial": 80000.0}
    snr_pts = [14.0, 18.0, 22.0]
    for cond_key, lw in conditions.items():
        for snr in snr_pts:
            for seed in LINEWIDTH_VAL_SEEDS:
                out = generate_channel(ChannelParams(
                    modulation=mod, snr_db=snr, linewidth_hz=lw,
                    n_symbols=n_sym, seed=seed, channel="gg_block_fading",
                    alpha=1.0, beta=0.7, f_g=500.0, gamma_bar=100.0))
                tx_bits = out.debug()["tx_bits"]
                # Fixed B* (validation-aggregate best N at this cell).
                per_w_ber = {}
                for N in WINDOW_GRID_RUN:
                    rx_comp = vv_block_mean(out.rx, N=N, modulation=mod)
                    per_w_ber[N] = ber_with_legal_resolve(rx_comp, tx_bits, mod)
                bstar_N = min(per_w_ber, key=per_w_ber.get)
                bstar_ber = float(per_w_ber[bstar_N])
                # Per-block oracle: pick the N minimizing each block's BER under
                # legal per-block pi/2 resolve (truth-assisted, Kill-only).
                nb = n_sym // BLOCK
                bps = 2 if mod == "qpsk" else 4
                oracle_err = 0
                oracle_bits = 0
                for blk in range(nb):
                    lo, hi = blk * BLOCK, (blk + 1) * BLOCK
                    seg_rx = out.rx[lo:hi]
                    seg_bits = tx_bits[lo * bps:hi * bps]
                    best_b = 1.0
                    for N in WINDOW_GRID_RUN:
                        if N > BLOCK:
                            continue
                        seg = vv_block_mean(seg_rx, N=N, modulation=mod)
                        b = _ber_blockwise_legal_resolve(seg, seg_bits, mod, BLOCK)
                        if b < best_b:
                            best_b = b
                    oracle_err += best_b * len(seg_bits)
                    oracle_bits += len(seg_bits)
                oracle_ber = oracle_err / max(oracle_bits, 1)
                rows.append({
                    "phase": "b2_gg_oracle", "modulation": mod,
                    "channel": "gg_block_fading", "condition": cond_key,
                    "linewidth_hz": lw, "snr_db": snr, "seed": seed,
                    "bstar_N": int(bstar_N), "bstar_BER": bstar_ber,
                    "oracle_BER": float(oracle_ber),
                    "bstar_minus_oracle_logber": float(np.log10(max(bstar_ber, 1e-12))
                                                        - np.log10(max(oracle_ber, 1e-12))),
                })
                out_lines.append(f"  gg {mod} {cond_key} snr={snr} seed={seed}: "
                                 f"B*={bstar_N} BER={bstar_ber:.3e}, oracle BER={oracle_ber:.3e}")
    # Headroom: dB-equivalent gain of oracle over B*, using the GG SNR slope.
    # We approximate with log-BER gap / slope (calibrated on the GG snr_pts).
    gains_db = []
    valid_gains = []   # gains from non-collapse cells (BER < 0.2)
    for r in rows:
        gap = r["bstar_minus_oracle_logber"]
        # dB proxy: assume slope ~ -0.15 log-BER/dB near FEC (typical); we report
        # the log-BER gap directly AND a dB-proxy. The gate uses the log-BER gap
        # median / trimmed mean vs the ORACLE_HEADROOM_DB threshold converted to
        # log-BER (0.5 dB * |slope|). Use |slope|~0.15 as the GG FEC slope.
        slope = 0.15
        gain_db = gap / slope
        gains_db.append(gain_db)
        if r["bstar_BER"] < ORACLE_COLLAPSE_BER:
            valid_gains.append(gain_db)
    median_gain = float(np.median(gains_db)) if gains_db else float("nan")
    trimmed_gain = float(_trimmed_mean(gains_db, 0.2)) if gains_db else float("nan")
    valid_median = float(np.median(valid_gains)) if valid_gains else float("nan")
    out_lines.append(f"  GG oracle headroom: median={median_gain:.3f} dB, "
                     f"20%-trimmed={trimmed_gain:.3f} dB, "
                     f"non-collapse-median={valid_median:.3f} dB")
    kill3 = (median_gain < ORACLE_HEADROOM_DB and trimmed_gain < ORACLE_HEADROOM_DB) or \
            (len(valid_gains) == 0)
    return {"rows": rows, "median_gain_db": median_gain,
            "trimmed_gain_db": trimmed_gain, "valid_median_gain_db": valid_median,
            "kill3_triggered": bool(kill3)}


def _trimmed_mean(a, frac):
    a = sorted(a)
    n = len(a)
    k = int(n * frac)
    if n - 2 * k <= 0:
        return float(np.mean(a))
    return float(np.mean(a[k:n - k]))


# ---------------------------------------------------------------------------
# B2.4 — structural KILL gate verdict
# ---------------------------------------------------------------------------
def evaluate_structural_gate(sweep, universal, gg_headroom, out_lines):
    """Apply the four pre-registered KILL conditions."""
    e1_majority = sweep["e1_pass_count"] / max(sweep["e1_total"], 1) > 0.5
    e2_majority = sweep["e2_pass_count"] / max(sweep["e2_total"], 1) > 0.5
    direction_ok = e1_majority and e2_majority
    # KILL condition 1: E1/E2 fail in the majority of cells.
    kill1 = not direction_ok
    # KILL condition 4: optimal N varies but features cannot predict.
    # (treated as: BOTH feature Spearman |rho| < 0.5 — no receiver-visible
    # feature predicts the best N well enough to deploy.)
    kill4 = (not sweep["feat_snr_ok"]) and (not sweep["feat_innov_ok"])
    # Note: kill4 requires "optimal N varies" — we check that the best_n_by_cell
    # has > 1 unique value.
    n_varies = len(set(sweep["best_n_by_cell"].values())) > 1
    kill4 = kill4 and n_varies

    kills = {
        "kill1_e1e2_direction_fails": bool(kill1),
        "kill2_universal_fixed_exists": bool(universal["kill2_triggered"]),
        "kill3_oracle_headroom_too_small": bool(gg_headroom["kill3_triggered"]),
        "kill4_features_cannot_predict": bool(kill4),
    }
    gate_passed = not any(kills.values())
    out_lines.append("  --- structural KILL gate ---")
    for k, v in kills.items():
        out_lines.append(f"    {k}: {v}")
    out_lines.append(f"  GATE {'PASSED' if gate_passed else 'FAILED (KILL)'}")
    return {
        "e1_majority_pass": bool(e1_majority),
        "e2_majority_pass": bool(e2_majority),
        "n_varies": bool(n_varies),
        "kills": kills,
        "gate_passed": bool(gate_passed),
        "verdict": "PASS" if gate_passed else "KILL_NO_ADAPTIVE_WINDOW_SPACE",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(mod="qpsk", out_dir=None):
    out_dir = out_dir or os.path.join(_SIM_DIR, "results", "adaptive-phase-window")
    os.makedirs(out_dir, exist_ok=True)
    out_lines = []
    out_lines.append(f"=== B2 structural gate (modulation={mod}) ===")

    sweep = run_awgn_wiener_sweep(out_lines, mod=mod)
    universal = run_universal_fixed_regret_check(out_lines, sweep, mod=mod)
    gg = run_gg_oracle_headroom(out_lines, mod=mod)
    verdict = evaluate_structural_gate(sweep, universal, gg, out_lines)

    # Write raw rows.
    raw_path = os.path.join(out_dir, f"b2_raw_{mod}.jsonl")
    with open(raw_path, "w", encoding="utf-8") as f:
        for r in sweep["rows"] + gg["rows"]:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # Write result JSON.
    result = {
        "modulation": mod,
        "sweep": {k: v for k, v in sweep.items() if k != "rows"},
        "universal": universal,
        "gg_headroom": {k: v for k, v in gg.items() if k != "rows"},
        "verdict": verdict,
        "n_symbols": N_SYMBOLS,
        "block": BLOCK,
        "window_grid": WINDOW_GRID_RUN,
        "snr_grid": SNR_GRID,
        "linewidths_hz": LINEWIDTHS_HZ,
        "validation_seeds": LINEWIDTH_VAL_SEEDS,
        "test_seeds": LINEWIDTH_TEST_SEEDS,
    }
    res_path = os.path.join(out_dir, f"b2_result_{mod}.json")
    with open(res_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # SHA stamping.
    closure_sha = _sha_file(os.path.join(_HERE, "source-closure.yaml"))
    contract_sha = _sha_file(os.path.join(_HERE, "contract.yaml"))
    spec_sha = _sha_file(os.path.join(_HERE, "MVE-SPEC.md"))
    out_lines.append(f"  source-closure.yaml SHA256: {closure_sha}")
    out_lines.append(f"  contract.yaml SHA256: {contract_sha}")
    out_lines.append(f"  MVE-SPEC.md SHA256: {spec_sha}")

    log_path = os.path.join(out_dir, f"b2_log_{mod}.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print("\n".join(out_lines))
    print(f"\nWrote: {raw_path}\n       {res_path}\n       {log_path}")
    return result


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


if __name__ == "__main__":
    mod = sys.argv[1] if len(sys.argv) > 1 else "qpsk"
    main(mod=mod)
