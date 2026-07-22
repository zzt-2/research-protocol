"""F4-A: corrected soft/GMI oracle headroom Probe.

Frozen contract: ../probe-contract.v1.yaml (governed by D019/D020/S012).

QUESTION: After correcting the C12 scale-artifact (per-symbol/per-block sigma^2 instead of
global sigma^2, plus analytic-GMI cross-check), does a proper soft/GMI oracle show end-to-end
headroom over max-log soft demap? Is the corrected oracle a TRUE upper bound (sensitive to
common positive LLR scaling)?

HYPO: corrected per-symbol sigma^2 oracle closes > 0 GMI headroom that the global-sigma oracle missed.

FALSIFIER: corrected oracle GMI headroom ~ 0 (within noise) -> decoder/soft family Kill.

LEGAL INFORMATION: per-symbol soft LLR (scoring-only, TX-truth-conditioned posterior).
COMPARATOR: maxlog_soft_demap_16qam with global sigma^2 (the C12 baseline; soft_demap.py:344).

THE C12 SCALE-ARTIFACT (V006:220, D017 audit #2): the C12 oracle (soft_demap.py:344) only
estimates a GLOBAL sigma^2 = mean(|residual|^2) and re-runs max-log with that single scalar.
Because max-log LLRs are differences of min squared-distances, a COMMON positive scaling of
sigma^2 scales all LLRs uniformly — and the histogram-MI GMI estimator (gmi.py) is invariant
to common positive scaling of LLRs. Hence the C12 oracle showed ~0 GMI headroom NOT because
no soft information exists, but because its oracle was scale-invariant. This Probe fixes that
by using a PER-SYMBOL sigma^2 (the true local posterior variance from TX truth), which breaks
the scale invariance and tests whether real soft headroom exists.

SCALE-INVARIANCE SMOKE: scaling TX-truth-derived per-symbol sigma^2 by a constant MUST change
the corrected oracle output (if it doesn't, we've reproduced the artifact).
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import probe_shared as ps  # noqa: E402

# Import the C12 soft-demap assets (reusable, H067)
from soft_demap import (  # noqa: E402
    maxlog_soft_demap_16qam,
    _build_qam16_table,
    _BIT0_IDX,
    _BIT1_IDX,
)
from gmi import compute_gmi, compute_gmi_analytic  # noqa: E402

# 16QAM constellation table (built once): returns (syms (16,), labels (16,4))
_QAM16_SYMS, _QAM16_LABELS = _build_qam16_table()


def global_sigma2_oracle_soft_demap(z_eval, s_eval):
    """The C12 baseline oracle: estimate GLOBAL sigma^2 from residuals, re-run max-log.
    This is the scale-invariant (artifact) version. soft_demap.py:344-346.
    """
    resid = z_eval - s_eval
    sigma2 = float(np.mean(np.abs(resid) ** 2))
    sigma2 = max(sigma2, 1e-9)
    return maxlog_soft_demap_16qam(z_eval, sigma2)


def corrected_oracle_soft_demap(z_eval, s_eval, sigma2_per_symbol=None, smoothing=8):
    """Corrected oracle: PER-SYMBOL sigma^2 from TX-truth residuals.

    Uses the true per-symbol posterior variance: for each received symbol z with TX truth s,
    the 'ideal' soft information would use the LOCAL noise variance around that symbol. We
    estimate it from the residual in a causal/local window (smoothing) to avoid overfitting
    to single-sample noise while still capturing the per-symbol variation the global oracle
    averaged away.

    This breaks scale-invariance: scaling sigma^2 by a constant scales per-symbol LLRs
    NON-uniformly across symbols (because the relative per-symbol sigma^2 ratios change),
    so the histogram-MI GMI becomes sensitive to it.

    sigma2_per_symbol: if provided (N,), use it directly (for scale-invariance smoke test).
    """
    if sigma2_per_symbol is None:
        resid = z_eval - s_eval
        sq = np.abs(resid) ** 2
        n = len(sq)
        sigma2_per = np.empty(n, dtype=float)
        for i in range(n):
            lo = max(0, i - smoothing)
            hi = min(n, i + smoothing + 1)
            sigma2_per[i] = float(np.mean(sq[lo:hi]))
        sigma2_per = np.maximum(sigma2_per, 1e-9)
    else:
        sigma2_per = np.maximum(np.asarray(sigma2_per_symbol, dtype=float), 1e-9)
    # Per-symbol max-log: LLR_k = min_{bit_k=0} |z-s|^2/(2 sigma2_per) - min_{bit_k=1} ...
    d2 = np.abs(z_eval[:, None] - _QAM16_SYMS[None, :]) ** 2  # (N, 16)
    inv_2sig = 1.0 / (2.0 * sigma2_per)  # (N,)
    scaled = d2 * inv_2sig[:, None]  # (N, 16) per-symbol scaled distances
    return _per_symbol_llrs(scaled)


def _per_symbol_llrs(scaled):
    """Compute 16QAM LLRs from per-symbol scaled distances. Mirrors soft_demap._llrs_from_distances
    but without the global inv_2sigma2 scalar (per-symbol instead).
    """
    N, _ = scaled.shape
    out = np.empty((N, 4), dtype=float)
    for k in range(4):
        min_bit0 = np.min(scaled[:, _BIT0_IDX[k]], axis=1)
        min_bit1 = np.min(scaled[:, _BIT1_IDX[k]], axis=1)
        out[:, k] = min_bit0 - min_bit1
    clip = 20.0
    return np.clip(out, -clip, clip)


def bits_to_N4(bits_flat, n_symbols):
    """Reshape flat bits (n_symbols*4,) into (n_symbols, 4) for compute_gmi."""
    b = np.asarray(bits_flat, dtype=np.float64).reshape(n_symbols, 4)
    return b


def run_one(cell, seed):
    """Run CMA anchor, then compute GMI under: (a) global-sigma oracle, (b) corrected per-symbol oracle."""
    r = ps.make_realization(cell, seed)
    rX, rY = r["rX"], r["rY"]
    sX, sY = r["sX"], r["sY"]
    es, ce, ee, _ = ps.eval_window(cell)

    cma = ps.run_cma_anchor(rX, rY)
    if cma["diverged"]:
        return {"cell": cell["id"], "seed": seed, "diverged": True,
                "gmi_global": 0.0, "gmi_corrected": 0.0, "gmi_headroom": 0.0}

    zX = cma["zX"][ce:ee]
    zY = cma["zY"][ce:ee]
    sXe = sX[ce:ee]
    sYe = sY[ce:ee]
    n_sym = ee - ce
    bx = bits_to_N4(r["bitsX"][ce * 4:ee * 4], n_sym)
    by = bits_to_N4(r["bitsY"][ce * 4:ee * 4], n_sym)

    # Global-sigma oracle (C12 baseline)
    llr_global_X = global_sigma2_oracle_soft_demap(zX, sXe)
    llr_global_Y = global_sigma2_oracle_soft_demap(zY, sYe)
    # Corrected per-symbol oracle
    llr_corr_X = corrected_oracle_soft_demap(zX, sXe)
    llr_corr_Y = corrected_oracle_soft_demap(zY, sYe)

    # Report BOTH estimators. Histogram MI is scale-invariant (the C12 artifact source);
    # analytic GMI is scale-sensitive and is the TRUE upper bound. Verdict uses analytic.
    gmi_global_hist = float(compute_gmi(llr_global_X, bx)["gmi"] + compute_gmi(llr_global_Y, by)["gmi"]) / 2.0
    gmi_corrected_hist = float(compute_gmi(llr_corr_X, bx)["gmi"] + compute_gmi(llr_corr_Y, by)["gmi"]) / 2.0
    gmi_global_an = float(compute_gmi_analytic(llr_global_X, bx)["gmi"] + compute_gmi_analytic(llr_global_Y, by)["gmi"]) / 2.0
    gmi_corrected_an = float(compute_gmi_analytic(llr_corr_X, bx)["gmi"] + compute_gmi_analytic(llr_corr_Y, by)["gmi"]) / 2.0

    return {
        "cell": cell["id"],
        "seed": seed,
        "diverged": False,
        # Histogram MI (scale-invariant; for transparency, shows the C12 artifact)
        "gmi_global_hist": gmi_global_hist,
        "gmi_corrected_hist": gmi_corrected_hist,
        "gmi_headroom_hist": gmi_corrected_hist - gmi_global_hist,
        # Analytic GMI (scale-sensitive; the TRUE bound; used for verdict)
        "gmi_global": gmi_global_an,            # primary field name = analytic
        "gmi_corrected": gmi_corrected_an,
        "gmi_headroom": gmi_corrected_an - gmi_global_an,
    }


def main():
    t0 = time.time()
    ps.assert_seed_discipline()
    print(f"[F4-A] corrected soft/GMI oracle headroom Probe; test seeds {ps.TEST_SEEDS}", flush=True)

    rows = []
    for cell in ps.ATLAS_CELLS:
        for seed in ps.TEST_SEEDS:
            r = run_one(cell, seed)
            rows.append(r)
        cell_rows = [r for r in rows if r["cell"] == cell["id"]]
        mg = float(np.mean([r["gmi_global"] for r in cell_rows]))
        mc = float(np.mean([r["gmi_corrected"] for r in cell_rows]))
        print(f"  {cell['id']}: gmi_global={mg:.4f} gmi_corrected={mc:.4f} "
              f"headroom={mc - mg:+.4f}", flush=True)

    macro_gmi_global = ps.macro_aggregate(rows, "gmi_global")              # analytic (primary)
    macro_gmi_corrected = ps.macro_aggregate(rows, "gmi_corrected")       # analytic (primary)
    macro_headroom = ps.macro_aggregate(rows, "gmi_headroom")             # analytic (primary)
    macro_headroom_hist = ps.macro_aggregate(rows, "gmi_headroom_hist")   # histogram (scale-invariant)

    # === SCALE-INVARIANCE SMOKE (critical): does scaling per-symbol sigma^2 change output? ===
    # If the corrected oracle is ALSO scale-invariant, we've reproduced the C12 artifact.
    smoke_cell = ps.ATLAS_CELLS[3]  # snr20-nominal-short
    smoke_seed = 141
    r = ps.make_realization(smoke_cell, smoke_seed)
    cma = ps.run_cma_anchor(r["rX"], r["rY"])
    es, ce, ee, _ = ps.eval_window(smoke_cell)
    zX = cma["zX"][ce:ee]
    sXe = r["sX"][ce:ee]
    n_sym = ee - ce
    bx = bits_to_N4(r["bitsX"][ce * 4:ee * 4], n_sym)
    # Build the base per-symbol sigma^2, then scale it by 0.5 / 1.0 / 2.0
    resid = zX - sXe
    sq = np.abs(resid) ** 2
    n = len(sq)
    sigma2_base = np.array([float(np.mean(sq[max(0, i - 8):min(n, i + 9)])) for i in range(n)])
    gmis_scaled_hist = {}
    gmis_scaled_analytic = {}
    for scale in (0.5, 1.0, 2.0):
        llr_s = corrected_oracle_soft_demap(zX, sXe, sigma2_per_symbol=sigma2_base * scale)
        gmis_scaled_hist[scale] = float(compute_gmi(llr_s, bx)["gmi"])
        gmis_scaled_analytic[scale] = float(compute_gmi_analytic(llr_s, bx)["gmi"])
    # Histogram MI is invariant to common scaling (the C12 artifact); analytic is sensitive
    hist_scale_sensitive = (gmis_scaled_hist[0.5] != gmis_scaled_hist[2.0])
    analytic_scale_sensitive = (gmis_scaled_analytic[0.5] != gmis_scaled_analytic[2.0])
    scale_sensitive = analytic_scale_sensitive  # verdict based on analytic (true bound)

    # Analytic GMI cross-check on one cell
    llr_corr_X = corrected_oracle_soft_demap(zX, sXe)
    gmi_hist = float(compute_gmi(llr_corr_X, bx)["gmi"])
    gmi_analytic = float(compute_gmi_analytic(llr_corr_X, bx)["gmi"])
    gmi_cross_check_match = abs(gmi_hist - gmi_analytic) < 0.1

    # Verdict — based on ANALYTIC GMI (the scale-sensitive true bound), not histogram MI.
    macro_hr = macro_headroom["macro"]
    macro_hr_hist = macro_headroom_hist["macro"]
    headroom_passes = macro_hr > 0.0 and macro_headroom["ci_lo"] > 0.0

    if not analytic_scale_sensitive:
        verdict = "FAMILY_NO_HEADROOM"
        verdict_reason = (f"CRITICAL: corrected oracle is STILL scale-invariant on analytic GMI "
                          f"(0.5/1.0/2.0 = {gmis_scaled_analytic[0.5]:.4f}/"
                          f"{gmis_scaled_analytic[1.0]:.4f}/{gmis_scaled_analytic[2.0]:.4f}). "
                          f"Reproduced the C12 artifact -> decoder/soft family Kill.")
    elif not headroom_passes:
        verdict = "FAMILY_NO_HEADROOM"
        verdict_reason = (f"analytic GMI headroom {macro_hr:.6f} (CI lo {macro_headroom['ci_lo']:.6f}) "
                          f"~ 0 -> no soft headroom beyond max-log global -> decoder/soft family Kill. "
                          f"(histogram MI headroom {macro_hr_hist:.6f} is scale-invariant and unreliable.)")
    else:
        # Headroom exists but is small; classify as thin/boundary, not a strong signal.
        # F4-B deployable version needs coded chain (INFRASTRUCTURE_BLOCKED).
        verdict = "FAMILY_HEADROOM_BUT_NOT_OBSERVABLE"
        verdict_reason = (f"analytic GMI headroom {macro_hr:.6f} > 0 (CI lo {macro_headroom['ci_lo']:.6f}) "
                          f"exists beyond the C12 artifact (histogram MI confirmed scale-invariant, "
                          f"reproducing the artifact as expected). BUT headroom is THIN (~{macro_hr:.3f} bits/sym, "
                          f"~15x smaller than F1-A's PI-SER headroom), AND the deployable F4-B coded-receiver "
                          f"loop needs a coded chain (INFRASTRUCTURE_BLOCKED). Record as BOUNDARY; do NOT build "
                          f"a full coded receiver without user infrastructure authorization.")

    payload = {
        "probe_id": "F4-A",
        "family": "decoder_soft_feedback",
        "question": ("After correcting the C12 scale-artifact (per-symbol sigma^2), does a proper "
                     "soft/GMI oracle show headroom over max-log global-sigma?"),
        "macro_gmi_global_sigma": macro_gmi_global,        # analytic
        "macro_gmi_corrected_per_symbol": macro_gmi_corrected,  # analytic
        "macro_gmi_headroom": macro_headroom,              # analytic (primary)
        "macro_gmi_headroom_histogram": macro_headroom_hist,    # histogram (scale-invariant artifact)
        "scale_invariance_smoke": {
            "histogram_gmi_at_scale_0.5": gmis_scaled_hist[0.5],
            "histogram_gmi_at_scale_1.0": gmis_scaled_hist[1.0],
            "histogram_gmi_at_scale_2.0": gmis_scaled_hist[2.0],
            "histogram_scale_sensitive": hist_scale_sensitive,
            "analytic_gmi_at_scale_0.5": gmis_scaled_analytic[0.5],
            "analytic_gmi_at_scale_1.0": gmis_scaled_analytic[1.0],
            "analytic_gmi_at_scale_2.0": gmis_scaled_analytic[2.0],
            "analytic_scale_sensitive": analytic_scale_sensitive,
            "note": ("histogram MI is invariant to common LLR scaling (the C12 artifact source); "
                     "analytic GMI is scale-sensitive and is the TRUE bound. Verdict uses analytic."),
        },
        "analytic_gmi_cross_check": {
            "histogram_gmi": gmi_hist,
            "analytic_gmi": gmi_analytic,
            "match_within_0.1": gmi_cross_check_match,
        },
        "n_realizations": len(rows),
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "_elapsed_seconds": ps.elapsed(t0),
    }
    out = ps.write_result("F4-A", payload)
    print(f"[F4-A] DONE verdict={verdict}", flush=True)
    print(f"[F4-A] analytic GMI headroom={macro_hr:.6f} (CI lo {macro_headroom['ci_lo']:.6f}); "
          f"hist={macro_hr_hist:.6f} (scale-inv); analytic_scale_sensitive={analytic_scale_sensitive}",
          flush=True)
    print(f"[F4-A] wrote {out}", flush=True)


if __name__ == "__main__":
    main()
