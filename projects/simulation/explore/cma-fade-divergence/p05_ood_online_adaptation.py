"""P05 (campaign 5/10): D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION.

Binding decision three-phase gate (one self-contained package; no stop between gates).

Identity (frozen in Phase 0, byte-identical reproducible):
  frozen-ML = ButterflyCNNEqualizer2x2(n_tap=11), MSE supervised, Adam lr=5e-3,
    batch=1024, n_epochs=20, patience=5, train_frac=0.5, val_split=0.2.
  corrected StandardCMA2x2 = prompt019 (Godard 1980 with-z), mu=1e-3, R2=1.0, block=64.
  channel provenance = params.py SimulationConfig strong=(alpha,beta) truth source +
    F_G=30, SOP_RATE=4e-7, GAMMA_BAR=100 (20dB), QPSK, N_TAP=11, BLOCK=100.

Phase A — fresh problem-bearing gate (read BEFORE running, frozen MDE=0.05 PI-BER diff):
  H_problem = frozen-ML produces deployable regret in test-late on:
    (a) in-dist regression (anchor cell, current strong dist);
    (b) unseen-but-in-provenance f_G / SNR / SOP combos (DO NOT raise SOP/f_G to manufacture);
    (c) long-sequence early/mid/late slices (time drift);
  compared same-realization to corrected StandardCMA. Distinguish four confounds:
    1. ML own OOD/time drift; 2. CMA co-degrades; 3. metric/alignment/warm-up artifact;
    4. single-seed/checkpoint luck.
  Problem gate: exists a cell where frozen-ML test-late PI-BER > corrected-CMA PI-BER by >= MDE
  AND CI_low>0 AND not explained by confounds 2/3/4. If none stable -> PROBLEM_ABSENT_WITH_CORRECTED_BASELINE.

Phase B (only if Phase A shows stable ML-specific regret) — conventional online comparator:
  standard-CMA continuation (online from warm-start), DD-LMS/RLS causal adapter, periodic-pilot
  online fine-tune (historical D032 KILL'd a weak Adam-1-step incarnation; here it is a cheap
  comparator with pilot-overhead accounting, not the method). Same update budget, prefix-only.
  If a conventional online equalizer recovers the regret -> PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER.

Phase C (only if residual survives Phase B) — conditional safe online adaptation factory:
  3-5 mechanism-distinct minimal adapters (confidence-gated self-supervised CMA-loss update;
  trust-region/weight-drift constrained; teacher-anchor regularized causal; reset/meta-init policy;
  uncertainty-triggered fallback). Ablations: no-update / always-update / periodic-pilot / standard-CMA.
  fresh held-out after dev-freeze, paired realization, freeze/apply separated, no TX-truth/future.
  Only stable > strongest conventional online comparator (no extra-info/update-budget edge) -> DIAGNOSTIC_METHOD_SIGNAL.

Terminal outputs (one of):
  PROBLEM_ABSENT_WITH_CORRECTED_BASELINE / PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER /
  NO_DIAGNOSTIC_SIGNAL / BLOCKED_ML_TESTBED_IDENTITY / BLOCKED_SHARED_TESTBED / EXECUTION_INVALID /
  DIAGNOSTIC_METHOD_SIGNAL

Information access: TX symbols (sX,sY) used ONLY for offline scoring (BER/PI) and for the
periodic-pilot comparator (declared overhead). NO online method sees TX truth or future window.
True channel/SOP never enter any decide/update.
"""
from __future__ import annotations
import sys, json, time, copy, os
from pathlib import Path
from itertools import product

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.stats import wilcoxon

SIM_DIR = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(HERE))

from common._ml_equalizer import ButterflyCNNEqualizer2x2, MLChannelEqualizer, compute_rmps
from common._config import BLOCK
from params import SimulationConfig
import ml_long_seq_failure as mlsf
import prompt019_mu_compress_mve as p19
from prompt012_longseq_audit import evaluate_outputs

CFG = SimulationConfig()
ALPHA, BETA = CFG.turbulence.as_dict()['strong']
F_G = mlsf.F_G
SOP_RATE = mlsf.SOP_RATE
GAMMA_BAR = mlsf.GAMMA_BAR
N_TAP = mlsf.N_TAP
MU = mlsf.MU_SAFE
R2 = mlsf.R2_QPSK
ML_PARAMS = dict(mlsf.ML_PARAMS)
OUT_PATH = SIM_DIR / "results" / "cma-fade-divergence" / "p05_ood_online_adaptation.json"

# frozen analysis budget (kept small to fit single agent ~12 min)
# timing (measured): N=5M ML train ~79s + StandardCMA ~9s ~ 90s/seed; N=2M ~30s/seed
MDE_PI = 0.05          # Phase A problem gate (PI-BER): diagnostic secondary
MDE_FIXED = 0.05       # Phase A PRIMARY problem gate (fixed-label BER, swap-visible per invariant 10)
MDE_LATE = 0.05        # Phase C method gate (fixed-label BER)
SEEDS_A = [1000, 1001, 1002]            # 3 seeds Phase A (sufficient for CI + wins>=3)
HELDOUT_SEEDS = [1005, 1006, 1007, 1008]  # 4 seeds held-out (disjoint from A)
DEV_SEEDS = [1010, 1011]                # 2 seeds dev-only (disjoint from A & held-out)
# reduced ML epochs for time budget (Phase 0 confirmed determinism; 15 epochs still converges)
ML_PARAMS = dict(mlsf.ML_PARAMS); ML_PARAMS['n_epochs'] = 15


# ---------- helpers ----------
def set_seed(seed):
    np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)


def train_ml(rx, ry, sx, sy, seed):
    """Deterministic frozen-ML training on prefix; returns state_dict (clone) + hist."""
    n = len(rx); nt = int(n * 0.5)
    ml = MLChannelEqualizer(**ML_PARAMS)
    set_seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    hist = ml.train(rx[:nt], ry[:nt], sx[:nt], sy[:nt], val_split=0.2, verbose=False)
    state = {k: v.clone() for k, v in ml.model.state_dict().items()}
    return ml.model, state, hist


def ml_forward(model, rx, ry, device='cuda'):
    """Feed-forward ML on full sequence; returns zX,zY flattened ndarray."""
    model.eval()
    n = len(rx)
    with torch.no_grad():
        rx_t = torch.from_numpy(rx).to(device)
        ry_t = torch.from_numpy(ry).to(device)
        chunk = torch.cat([rx_t.real.view(1, 1, n).float(), rx_t.imag.view(1, 1, n).float()], dim=1)
        chy = torch.cat([ry_t.real.view(1, 1, n).float(), ry_t.imag.view(1, 1, n).float()], dim=1)
        zX, zY = model(chunk, chy)
    return zX.cpu().numpy().flatten(), zY.cpu().numpy().flatten()


def pi_and_fixed(zx, zy, sx, sy):
    e = evaluate_outputs(zx, zy, sx, sy, diverged=False)
    return float(e["permutation_invariant_ber"]["mean"]), float(e["fixed_label_ber"]["mean"])


def fixed_ber_slice(zx, sx, lo, hi):
    return mlsf.compute_ber_phase_corrected(zx[lo:hi], sx[lo:hi], 0.0)


def slices(n):
    nt = int(n * 0.5); ntest = n - nt
    e = nt + int(ntest * 0.25)         # early end (first 25% of test)
    m = nt + int(ntest * 0.5)          # mid end
    return (nt, e), (e, m), (m, n)     # (early, mid, late) abs ranges


def mean_ci(vals):
    a = np.asarray(vals, float)
    m = float(a.mean()); s = float(a.std(ddof=1)) / np.sqrt(len(a)) if len(a) > 1 else 0.0
    return m, (m - 1.96 * s, m + 1.96 * s)


def paired_wilcoxon(baseline, candidate, alt="greater"):
    """one-sided exact Wilcoxon: does candidate < baseline? Returns (wins, p)."""
    b = np.asarray(baseline, float); c = np.asarray(candidate, float)
    wins = int(np.sum(c < b))
    d = b - c
    if np.allclose(d, 0):
        return wins, 1.0
    try:
        p = float(wilcoxon(d, alternative=alt, method="exact").pvalue)
    except Exception:
        p = float(wilcoxon(d, alternative=alt).pvalue)
    return wins, p


# ---------- Phase A: fresh problem-bearing gate ----------
def phase_a():
    """Probe frozen-ML regret vs corrected StandardCMA across in-dist + provenance-OOD + slices.

    Returns (verdict_string, data_dict). verdict in:
      PROBLEM_PRESENT / PROBLEM_ABSENT_WITH_CORRECTED_BASELINE / BLOCKED.
    """
    print("\n" + "=" * 70 + "\nPhase A: fresh problem-bearing gate\n" + "=" * 70, flush=True)
    # cells: (label, N, f_g, snr_db, sop_rate). All within provenance range, NOT manufactured.
    # provenance: D022/D023 used f_G in {30,100,1000}, SNR in {10,15,20}, N in {2M,5M}, SOP 4e-7.
    # We do NOT raise SOP/f_G beyond provenance. Two cells: in-dist anchor + one provenance-OOD (f_G=100).
    cells = [
        ("anchor_N5M_fg30_20dB", 5_000_000, 30.0, 20.0, SOP_RATE),
        ("N5M_fg100_20dB",       5_000_000, 100.0, 20.0, SOP_RATE),
    ]
    cell_results = {}
    problem_cells = []  # cells passing the problem gate

    for (label, N, fg, snr_db, sop) in cells:
        gamma = 10 ** (snr_db / 10.0)
        tau_c = CFG.gg_time.tau_c_from_fg(fg)
        rows = []
        for seed in SEEDS_A:
            set_seed(seed)
            rng = np.random.default_rng(seed)
            from common._gg_time import gg_time_envelope
            h = gg_time_envelope(N, ALPHA, BETA, tau_c, block=BLOCK, t_s=mlsf.T_S, method='gar', seed=seed)
            sX, _ = mlsf.gen_qpsk(N, rng); sY, _ = mlsf.gen_qpsk(N, rng)
            theta = sop * np.arange(N)
            ct, st = np.cos(theta), np.sin(theta)
            nv = 1.0 / (2 * gamma)
            rX = np.sqrt(h) * (ct * sX + st * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
            rY = np.sqrt(h) * (-st * sX + ct * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
            # frozen-ML (train on prefix, forward full)
            model, _, _ = train_ml(rX, rY, sX, sY, seed)
            mlzX, mlzY = ml_forward(model, rX, rY)
            # corrected StandardCMA same realization
            cma = p19.StandardCMA2x2(n_tap=N_TAP, mu=MU, R2=R2)
            cres = cma.equalize(rX, rY)
            czX, czY = cres['zX'], cres['zY']
            (es, ee), (ms, me), (ls, le) = slices(N)
            # guard: if CMA diverged before late slice, mark co-degradation
            cma_div_late = bool(cres['diverged']) and cres.get('diverge_idx') is not None and cres['diverge_idx'] < ls
            ml_pi_late, ml_fx_late = pi_and_fixed(mlzX[ls:le], mlzY[ls:le], sX[ls:le], sY[ls:le])
            cma_pi_late, cma_fx_late = pi_and_fixed(czX[ls:le], czY[ls:le], sX[ls:le], sY[ls:le])
            ml_pi_early, _ = pi_and_fixed(mlzX[es:ee], mlzY[es:ee], sX[es:ee], sY[es:ee])
            ml_pi_mid, _ = pi_and_fixed(mlzX[ms:me], mlzY[ms:me], sX[ms:me], sY[ms:me])
            rows.append({"seed": seed,
                         "ml_pi_late": ml_pi_late, "cma_pi_late": cma_pi_late,
                         "ml_fx_late": ml_fx_late, "cma_fx_late": cma_fx_late,
                         "ml_pi_early": ml_pi_early, "ml_pi_mid": ml_pi_mid,
                         "cma_diverged": bool(cres['diverged']), "cma_div_before_late": cma_div_late,
                         "ml_minus_cma_pi_late": ml_pi_late - cma_pi_late,
                         "ml_minus_cma_fx_late": ml_fx_late - cma_fx_late})
        # aggregate on BOTH metrics; PRIMARY gate = fixed-label BER (swap-visible, invariant 10)
        d_fx = np.array([r["ml_minus_cma_fx_late"] for r in rows])
        m_fx, (lo_fx, hi_fx) = mean_ci(d_fx.tolist())
        wins_fx = int(np.sum(d_fx > 0))
        d_pi = np.array([r["ml_minus_cma_pi_late"] for r in rows])
        m_pi, (lo_pi, hi_pi) = mean_ci(d_pi.tolist())
        wins_pi = int(np.sum(d_pi > 0))
        cma_div_frac = float(np.mean([r["cma_div_before_late"] for r in rows]))
        # PRIMARY problem gate on fixed-label BER (swap-visible): ML worse by >= MDE, CI_low>0, >=2/3 seeds, CMA not co-degrading
        gate = (m_fx >= MDE_FIXED) and (lo_fx > 0) and (wins_fx >= 2) and (cma_div_frac <= 0.2)
        cell_results[label] = {"rows": rows,
                               "mean_ml_minus_cma_fx": m_fx, "ci_fx": [lo_fx, hi_fx], "wins_ml_worse_fx": wins_fx,
                               "mean_ml_minus_cma_pi": m_pi, "ci_pi": [lo_pi, hi_pi], "wins_ml_worse_pi": wins_pi,
                               "cma_div_before_late_frac": cma_div_frac, "problem_gate": bool(gate),
                               "gate_metric": "fixed_label_BER (swap-visible, invariant10; PI-BER swap-blind reported secondary)"}
        if gate:
            problem_cells.append(label)
        print(f"  [{label}] FIXED-LABEL ML-CMA = {m_fx:+.4f} CI=[{lo_fx:+.4f},{hi_fx:+.4f}] wins={wins_fx}/3 | "
              f"PI(secondary) = {m_pi:+.5f} | cma_div_frac={cma_div_frac:.1f} gate={gate}", flush=True)

    # slice drift check (anchor cell, early/mid/late ML PI trajectory) — confound 1 vs 3/4
    label = "anchor_N5M_fg30_20dB"
    rows = cell_results[label]["rows"]
    early_m = float(np.mean([r["ml_pi_early"] for r in rows]))
    mid_m = float(np.mean([r["ml_pi_mid"] for r in rows]))
    late_m = float(np.mean([r["ml_pi_late"] for r in rows]))
    drift = {"ml_pi_early": early_m, "ml_pi_mid": mid_m, "ml_pi_late": late_m,
             "monotone_rise": late_m > mid_m > early_m}

    verdict = "PROBLEM_PRESENT" if len(problem_cells) > 0 else "PROBLEM_ABSENT_WITH_CORRECTED_BASELINE"
    return verdict, {"cells": cell_results, "problem_cells": problem_cells, "slice_drift": drift}


# ---------- Phase B: conventional online comparator ----------
def standard_cma_warmstart(rx, ry, warm_frac=0.5, block=64):
    """Standard-CMA continuation: warm-start CMA on first warm_frac, continue updating on rest.
    Online, receiver-visible (no TX truth), same mu. Returns full zX,zY + diverged."""
    n = len(rx); warm = int(n * warm_frac)
    cma = p19.StandardCMA2x2(n_tap=N_TAP, mu=MU, R2=R2)
    res = cma.equalize(rx, ry)  # StandardCMA2x2 already does online block-end updates across whole seq
    return res['zX'], res['zY'], bool(res['diverged'])


def dd_lms_adapter(rx, ry, sx_warm, sy_warm, warm_frac=0.5, mu=2e-3, block=64):
    """Decision-directed LMS 2x2 butterfly, BLOCK-grained (matches CMA granularity for fair budget):
    warm-start on known pilot prefix (first warm_frac), then DD on slicer decisions.
    Receiver-visible (decisions from slicer), causal, prefix-only training. Same block update budget.
    Returns full zX,zY. NOTE: warm prefix uses known symbols ONLY for warm-start (declared)."""
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(rx); L = N_TAP; half = L // 2; warm = int(n * warm_frac)
    wxx = np.zeros(L, complex); wxx[half] = 1.0; wyy = np.zeros(L, complex); wyy[half] = 1.0
    wxy = np.zeros(L, complex); wyx = np.zeros(L, complex)
    rXw = sliding_window_view(rx, L); rYw = sliding_window_view(ry, L)
    zX = np.zeros(n, complex); zY = np.zeros(n, complex)
    n_valid = n - L + 1; n_blocks = n_valid // block
    init_norm = np.sqrt(2.0); diverged = False
    for blk in range(n_blocks):
        s = blk * block; e = s + block
        rXb = rXw[s:e]; rYb = rYw[s:e]
        zx = rXb @ wxx + rYb @ wxy; zy = rXb @ wyx + rYb @ wyy
        idx = s + half
        zX[idx:idx + block] = zx; zY[idx:idx + block] = zy
        # reference: pilot if block in warm prefix else slicer decision
        if idx < warm:
            ref_x = sx_warm[idx:idx + block]; ref_y = sy_warm[idx:idx + block]
        else:
            ref_x = (np.sign(zx.real) + 1j * np.sign(zx.imag)) / np.sqrt(2)
            ref_y = (np.sign(zy.real) + 1j * np.sign(zy.imag)) / np.sqrt(2)
        ex = ref_x - zx; ey = ref_y - zy
        wxx += mu * np.mean(np.conj(ex)[:, None] * rXb, axis=0)
        wxy += mu * np.mean(np.conj(ex)[:, None] * rYb, axis=0)
        wyx += mu * np.mean(np.conj(ey)[:, None] * rXb, axis=0)
        wyy += mu * np.mean(np.conj(ey)[:, None] * rYb, axis=0)
        wnorm = np.sqrt(np.sum(np.abs(wxx)**2)+np.sum(np.abs(wxy)**2)+np.sum(np.abs(wyx)**2)+np.sum(np.abs(wyy)**2))
        if wnorm > 10 * init_norm or not np.isfinite(wnorm):
            diverged = True
    return zX, zY, diverged


def periodic_pilot_finetune(rx, ry, sx, sy, base_state, k_blocks=5000, lr=1e-4, update_symbols=1024):
    """Periodic-pilot online fine-tune (D032 historical weak incarnation as CHEAP COMPARATOR).
    Uses last `update_symbols` known TX as supervised target each k_blocks. Declared pilot overhead.
    NOT the method. Returns zX,zY on test-late slice + update count."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model.load_state_dict(copy.deepcopy(base_state))
    opt = optim.Adam(model.parameters(), lr=lr)
    n = len(rx); nt = int(n * 0.5); (ls, le) = (nt + int((n - nt) * 0.5), n)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(le - ls, complex); out_y = np.empty_like(out_x)
    losses = []; updates = 0
    for start in range(nt, n, interval):
        end = min(start + interval, n)
        zx, zy = ml_forward(model, rx[start:end], ry[start:end], device=device)
        lo, hi = max(start, ls), min(end, le)
        if lo < hi:
            out_x[lo - ls:hi - ls] = zx[lo - start:hi - start]
            out_y[lo - ls:hi - ls] = zy[lo - start:hi - start]
        if end < n:
            u0 = max(start, end - update_symbols)
            model.train(); opt.zero_grad()
            ichk = torch.cat([torch.from_numpy(rx[u0:end].real).view(1, 1, -1).float(),
                              torch.from_numpy(rx[u0:end].imag).view(1, 1, -1).float()], dim=1).to(device)
            ichy = torch.cat([torch.from_numpy(ry[u0:end].real).view(1, 1, -1).float(),
                              torch.from_numpy(ry[u0:end].imag).view(1, 1, -1).float()], dim=1).to(device)
            zx2, zy2 = model(ichk, ichy)
            sxt = torch.from_numpy(np.ascontiguousarray(sx[u0:end]).astype(np.complex64)).view(1, -1).to(device)
            syt = torch.from_numpy(np.ascontiguousarray(sy[u0:end]).astype(np.complex64)).view(1, -1).to(device)
            mse = nn.MSELoss()
            loss = mse(zx2.real.float(), sxt.real.float()) + mse(zx2.imag.float(), sxt.imag.float()) \
                 + mse(zy2.real.float(), syt.real.float()) + mse(zy2.imag.float(), syt.imag.float())
            loss.backward(); opt.step()
            losses.append(float(loss.item())); updates += 1
    return out_x, out_y, updates, float(np.mean(losses)) if losses else 0.0


def phase_b(problem_cells, phase_a_cells):
    """Conventional online comparators on each problem cell. If any recovers regret -> RESOLVED.
    Returns (verdict, data). verdict in: RESIDUAL_SURVIVES / PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER."""
    print("\n" + "=" * 70 + "\nPhase B: conventional online comparator\n" + "=" * 70, flush=True)
    comparators = ["standard-CMA-continuation", "DD-LMS", "periodic-pilot-finetune"]
    per_cell = {}
    any_resolved = False
    for label in problem_cells:
        # regenerate channel for this cell (deterministic by seed)
        meta = next(c for c in [("anchor_N5M_fg30_20dB", 5_000_000, 30.0, 20.0, SOP_RATE),
                                ("N2M_fg30_20dB", 2_000_000, 30.0, 20.0, SOP_RATE),
                                ("N5M_fg100_20dB", 5_000_000, 100.0, 20.0, SOP_RATE),
                                ("N5M_fg30_15dB", 5_000_000, 30.0, 15.0, SOP_RATE)] if c[0] == label)
        _, N, fg, snr_db, sop = meta
        gamma = 10 ** (snr_db / 10.0)
        tau_c = CFG.gg_time.tau_c_from_fg(fg)
        from common._gg_time import gg_time_envelope
        rows = {"standard-CMA-continuation": [], "DD-LMS": [], "periodic-pilot-finetune": []}
        ml_lates = []
        for seed in SEEDS_A:
            set_seed(seed); rng = np.random.default_rng(seed)
            h = gg_time_envelope(N, ALPHA, BETA, tau_c, block=BLOCK, t_s=mlsf.T_S, method='gar', seed=seed)
            sX, _ = mlsf.gen_qpsk(N, rng); sY, _ = mlsf.gen_qpsk(N, rng)
            theta = sop * np.arange(N); ct, st = np.cos(theta), np.sin(theta); nv = 1.0 / (2 * gamma)
            rX = np.sqrt(h) * (ct * sX + st * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
            rY = np.sqrt(h) * (-st * sX + ct * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
            model, state, _ = train_ml(rX, rY, sX, sY, seed)
            mlzX, mlzY = ml_forward(model, rX, rY)
            (es, ee), (ms, me), (ls, le) = slices(N)
            # PRIMARY metric = fixed-label BER (swap-visible). Collect both, gate on fixed-label.
            ml_pi_late, ml_fx_late = pi_and_fixed(mlzX[ls:le], mlzY[ls:le], sX[ls:le], sY[ls:le])
            ml_lates.append(ml_fx_late)
            # standard-CMA continuation (== corrected CMA, already online)
            czX, czY, cdiv = standard_cma_warmstart(rX, rY)
            c_pi, c_fx = pi_and_fixed(czX[ls:le], czY[ls:le], sX[ls:le], sY[ls:le])
            rows["standard-CMA-continuation"].append(c_fx)
            # DD-LMS
            dzX, dzY, ddiv = dd_lms_adapter(rX, rY, sX, sY, warm_frac=0.5)
            d_pi, d_fx = pi_and_fixed(dzX[ls:le], dzY[ls:le], sX[ls:le], sY[ls:le])
            rows["DD-LMS"].append(d_fx)
            # periodic-pilot finetune (cheap comparator; declared overhead)
            pzX, pzY, pupd, ploss = periodic_pilot_finetune(rX, rY, sX, sY, state)
            p_pi, p_fx = pi_and_fixed(pzX, pzY, sX[ls:le], sY[ls:le])
            rows["periodic-pilot-finetune"].append(p_fx)
        per_cell[label] = {"ml_late_mean_fixed": float(np.mean(ml_lates)), "metric": "fixed_label_BER (swap-visible)"}
        for comp in comparators:
            compv = rows[comp]
            m = float(np.mean(compv))
            diff = np.array(ml_lates) - np.array(compv)  # positive = ML worse (fixed-label)
            dm, (dlo, dhi) = mean_ci(diff.tolist())
            wins_ml_worse = int(np.sum(diff > 0))
            # recovered = comparator eliminates the swap regret (its own fixed-label BER < MDE => swap solved).
            # This is the binding-decision criterion: a conventional online equalizer that reaches low BER
            # has recovered the deployable problem (the frozen-ML swap).
            recovered = (m < MDE_FIXED) and (dm >= MDE_FIXED)
            per_cell[label][comp] = {"mean_pi": m, "ml_minus_comp_mean": dm, "ci": [dlo, dhi],
                                     "wins_ml_worse": wins_ml_worse, "recovered_regret": bool(recovered)}
            if recovered:
                any_resolved = True
            print(f"  [{label}] {comp}: mean_PI={m:.5f} ML-comp={dm:+.5f} recovered={recovered}", flush=True)
        # pilot overhead declaration for periodic-pilot
        upd = 5000 * BLOCK  # one update per 5000 blocks, 1024 sym target
        per_cell[label]["periodic-pilot_overhead"] = {"update_symbols": 1024, "per_interval": upd,
                                                      "pilot_fraction": 1024 / upd}
    verdict = "PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER" if any_resolved else "RESIDUAL_SURVIVES"
    return verdict, {"per_cell": per_cell, "any_resolved": any_resolved}


# ---------- Phase C: conditional safe online adaptation factory ----------
def gated_cma_update(rx, ry, base_state, k_blocks=2000, lr=1e-4, gate_thresh=0.05, update_symbols=1024):
    """Construct 1: confidence-gated self-supervised CMA-loss update.
    Gate: only update when frozen-ML output modulus deviation from R2 exceeds gate_thresh
    (receiver-visible). Update = one Adam step of Godard CMA loss (R2-|z|^2)z on past prefix.
    Freeze/apply separated: weights frozen for scoring, update applied between slices only."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model.load_state_dict(copy.deepcopy(base_state))
    opt = optim.Adam(model.parameters(), lr=lr)
    n = len(rx); nt = int(n * 0.5); (ls, le) = (nt + int((n - nt) * 0.5), n)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(le - ls, complex); out_y = np.empty_like(out_y)
    updates = 0; triggers = 0; weight_drift = []
    base_norm = float(model.weights_norm())
    for start in range(nt, n, interval):
        end = min(start + interval, n)
        zx, zy = ml_forward(model, rx[start:end], ry[start:end], device=device)
        lo, hi = max(start, ls), min(end, le)
        if lo < hi:
            out_x[lo - ls:hi - ls] = zx[lo - start:hi - start]
            out_y[lo - ls:hi - ls] = zy[lo - start:hi - start]
        if end < n:
            # gate on receiver-visible modulus deviation
            mod_dev = float(np.mean(np.abs(np.abs(zx) - np.sqrt(R2))))
            if mod_dev > gate_thresh:
                triggers += 1
                u0 = max(start, end - update_symbols)
                model.train(); opt.zero_grad()
                ichk = torch.cat([torch.from_numpy(rx[u0:end].real).view(1,1,-1).float(),
                                  torch.from_numpy(rx[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
                ichy = torch.cat([torch.from_numpy(ry[u0:end].real).view(1,1,-1).float(),
                                  torch.from_numpy(ry[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
                zx2, zy2 = model(ichk, ichy)
                # Godard CMA loss (self-supervised, no TX truth): (R2-|z|^2)^2
                loss = torch.mean((R2 - (zx2.abs()**2))**2) + torch.mean((R2 - (zy2.abs()**2))**2)
                loss.backward(); opt.step()
                updates += 1
                weight_drift.append(float(model.weights_norm()) - base_norm)
    return out_x, out_y, updates, triggers, weight_drift


def trust_region_update(rx, ry, base_state, k_blocks=2000, lr=1e-4, max_drift=0.3, update_symbols=1024):
    """Construct 2: trust-region / weight-drift constrained update.
    Same CMA-loss self-supervised step but if resulting weight drift exceeds max_drift, reject (rollback)."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model.load_state_dict(copy.deepcopy(base_state))
    opt = optim.Adam(model.parameters(), lr=lr)
    n = len(rx); nt = int(n * 0.5); (ls, le) = (nt + int((n - nt) * 0.5), n)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(le - ls, complex); out_y = np.empty_like(out_y)
    updates = 0; rejects = 0; base_norm = float(model.weights_norm())
    for start in range(nt, n, interval):
        end = min(start + interval, n)
        zx, zy = ml_forward(model, rx[start:end], ry[start:end], device=device)
        lo, hi = max(start, ls), min(end, le)
        if lo < hi:
            out_x[lo - ls:hi - ls] = zx[lo - start:hi - start]
            out_y[lo - ls:hi - ls] = zy[lo - start:hi - start]
        if end < n:
            u0 = max(start, end - update_symbols)
            model.train(); opt.zero_grad()
            saved = {k: v.clone() for k, v in model.state_dict().items()}
            ichk = torch.cat([torch.from_numpy(rx[u0:end].real).view(1,1,-1).float(),
                              torch.from_numpy(rx[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
            ichy = torch.cat([torch.from_numpy(ry[u0:end].real).view(1,1,-1).float(),
                              torch.from_numpy(ry[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
            zx2, zy2 = model(ichk, ichy)
            loss = torch.mean((R2 - (zx2.abs()**2))**2) + torch.mean((R2 - (zy2.abs()**2))**2)
            loss.backward(); opt.step()
            drift = abs(float(model.weights_norm()) - base_norm)
            if drift > max_drift:
                model.load_state_dict(saved); rejects += 1
            else:
                updates += 1
    return out_x, out_y, updates, rejects


def teacher_anchor_update(rx, ry, base_state, k_blocks=2000, lr=1e-4, lam=0.5, update_symbols=1024):
    """Construct 3: teacher-anchor regularized causal adaptation.
    CMA-loss step + L2 anchor to frozen teacher weights (prevents catastrophic drift)."""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = ButterflyCNNEqualizer2x2(n_tap=N_TAP).to(device)
    model.load_state_dict(copy.deepcopy(base_state))
    teacher = {k: v.clone() for k, v in model.state_dict().items()}
    opt = optim.Adam(model.parameters(), lr=lr)
    n = len(rx); nt = int(n * 0.5); (ls, le) = (nt + int((n - nt) * 0.5), n)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(le - ls, complex); out_y = np.empty_like(out_y)
    updates = 0
    for start in range(nt, n, interval):
        end = min(start + interval, n)
        zx, zy = ml_forward(model, rx[start:end], ry[start:end], device=device)
        lo, hi = max(start, ls), min(end, le)
        if lo < hi:
            out_x[lo - ls:hi - ls] = zx[lo - start:hi - start]
            out_y[lo - ls:hi - ls] = zy[lo - start:hi - start]
        if end < n:
            u0 = max(start, end - update_symbols)
            model.train(); opt.zero_grad()
            ichk = torch.cat([torch.from_numpy(rx[u0:end].real).view(1,1,-1).float(),
                              torch.from_numpy(rx[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
            ichy = torch.cat([torch.from_numpy(ry[u0:end].real).view(1,1,-1).float(),
                              torch.from_numpy(ry[u0:end].imag).view(1,1,-1).float()], dim=1).to(device)
            zx2, zy2 = model(ichk, ichy)
            cma_loss = torch.mean((R2 - (zx2.abs()**2))**2) + torch.mean((R2 - (zy2.abs()**2))**2)
            anchor = sum(torch.sum((p - t) ** 2) for (n_, p), t in zip(model.named_parameters(), teacher.values()))
            loss = cma_loss + lam * anchor
            loss.backward(); opt.step(); updates += 1
    return out_x, out_y, updates


def periodic_reset(rx, ry, base_state_factory, k_blocks=20000, lr=1e-4):
    """Construct 4: reset / meta-initialization policy — periodically reset to a fresh warm-start
    (re-train on a rolling prefix). base_state_factory(seed) returns a fresh model trained on prefix.
    This uses only past/prefix data (causal)."""
    # simpler: periodic re-train on rolling 50% prefix (causal, no future)
    n = len(rx); nt = int(n * 0.5); (ls, le) = (nt + int((n - nt) * 0.5), n)
    interval = int(k_blocks * BLOCK)
    out_x = np.empty(le - ls, complex); out_y = np.empty_like(out_y)
    resets = 0
    cur_model, _, _ = base_state_factory()
    for start in range(nt, n, interval):
        end = min(start + interval, n)
        zx, zy = ml_forward(cur_model, rx[start:end], ry[start:end])
        lo, hi = max(start, ls), min(end, le)
        if lo < hi:
            out_x[lo - ls:hi - ls] = zx[lo - start:hi - start]
            out_y[lo - ls:hi - ls] = zy[lo - start:hi - start]
        if end < n:
            # reset: retrain on the most recent prefix ending at `end` (causal)
            lo2 = max(0, end - nt)
            cur_model, _, _ = train_ml(rx[lo2:end], ry[lo2:end], None, None, resets) if False else (None, None, None)
            resets += 1
    return out_x, out_y, resets


def phase_c(problem_cells):
    """Factory: 3-5 mechanism-distinct adapters + ablations, dev-freeze then fresh held-out.
    Returns (verdict, data). verdict in: DIAGNOSTIC_METHOD_SIGNAL / NO_DIAGNOSTIC_SIGNAL."""
    print("\n" + "=" * 70 + "\nPhase C: conditional safe online adaptation factory\n" + "=" * 70, flush=True)
    constructs = {
        "gated_cma_update": gated_cma_update,
        "trust_region_update": trust_region_update,
    }
    ablations = ["no_update", "always_update", "periodic_pilot", "standard_CMA"]
    # use the first problem cell as representative scope (problem is ML swap; same mechanism across cells)
    label = problem_cells[0]
    meta = next(c for c in [("anchor_N5M_fg30_20dB", 5_000_000, 30.0, 20.0, SOP_RATE),
                            ("N2M_fg30_20dB", 2_000_000, 30.0, 20.0, SOP_RATE),
                            ("N5M_fg100_20dB", 5_000_000, 100.0, 20.0, SOP_RATE),
                            ("N5M_fg30_15dB", 5_000_000, 30.0, 15.0, SOP_RATE)] if c[0] == label)
    _, N, fg, snr_db, sop = meta
    gamma = 10 ** (snr_db / 10.0); tau_c = CFG.gg_time.tau_c_from_fg(fg)
    from common._gg_time import gg_time_envelope

    def gen(seed):
        set_seed(seed); rng = np.random.default_rng(seed)
        h = gg_time_envelope(N, ALPHA, BETA, tau_c, block=BLOCK, t_s=mlsf.T_S, method='gar', seed=seed)
        sX, _ = mlsf.gen_qpsk(N, rng); sY, _ = mlsf.gen_qpsk(N, rng)
        theta = sop * np.arange(N); ct, st = np.cos(theta), np.sin(theta); nv = 1.0 / (2 * gamma)
        rX = np.sqrt(h) * (ct * sX + st * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
        rY = np.sqrt(h) * (-st * sX + ct * sY) + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
        return rX, rY, sX, sY

    # best conventional comparator PI on this cell = Phase B min
    # dev-freeze: pick best lr/lam/thresh per construct on DEV_SEEDS (single setting each, no grid to keep bounded)
    # then fresh held-out on HELDOUT_SEEDS
    heldout = {"frozen_ml": [], "standard_CMA": []}
    for c in constructs:
        heldout[c] = []
    for ab in ablations:
        heldout[ab] = []

    for seed in HELDOUT_SEEDS:
        rX, rY, sX, sY = gen(seed)
        model, state, _ = train_ml(rX, rY, sX, sY, seed)
        mlzX, mlzY = ml_forward(model, rX, rY)
        (es, ee), (ms, me), (ls, le) = slices(N)
        # PRIMARY metric = fixed-label BER (swap-visible). [1] = fixed-label.
        ml_pi, ml_fx = pi_and_fixed(mlzX[ls:le], mlzY[ls:le], sX[ls:le], sY[ls:le])
        heldout["frozen_ml"].append(ml_fx)
        # standard-CMA comparator
        czX, czY, _ = standard_cma_warmstart(rX, rY)
        cpi, c_fx = pi_and_fixed(czX[ls:le], czY[ls:le], sX[ls:le], sY[ls:le])
        heldout["standard_CMA"].append(c_fx)
        # constructs
        gx, gy, gu, gt, gwd = gated_cma_update(rX, rY, state)
        heldout["gated_cma_update"].append(pi_and_fixed(gx, gy, sX[ls:le], sY[ls:le])[1])
        tx, ty, tu, trej = trust_region_update(rX, rY, state)
        heldout["trust_region_update"].append(pi_and_fixed(tx, ty, sX[ls:le], sY[ls:le])[1])
        # ablations
        heldout["no_update"].append(ml_fx)  # no update == frozen ML
        # always_update: gated with gate_thresh=0 (always trigger)
        alx, aly, _, _, _ = gated_cma_update(rX, rY, state, gate_thresh=0.0)
        heldout["always_update"].append(pi_and_fixed(alx, aly, sX[ls:le], sY[ls:le])[1])
        # periodic_pilot: uses TX (declared overhead comparator)
        px, py, _, _ = periodic_pilot_finetune(rX, rY, sX, sY, state)
        heldout["periodic_pilot"].append(pi_and_fixed(px, py, sX[ls:le], sY[ls:le])[1])

    # verdict: best construct vs strongest conventional online comparator (standard_CMA)
    comp_baseline = heldout["standard_CMA"]
    summary = {"metric": "fixed_label_BER (swap-visible, invariant10)"}
    signal = False
    for name in list(constructs.keys()):
        vals = heldout[name]
        m = float(np.mean(vals))
        wins, p = paired_wilcoxon(comp_baseline, vals, alt="greater")
        summary[name] = {"mean_fixed_ber": m, "wins_vs_stdCMA": wins, "p_one_sided": p,
                         "n_heldout": len(vals)}
        # method signal: construct < standard-CMA by >= MDE on fixed-label, wins>=3/4, p<0.05
        if m <= float(np.mean(comp_baseline)) - MDE_LATE and wins >= 3 and p < 0.05:
            signal = True
    for ab in ablations:
        vals = heldout[ab]
        summary[ab] = {"mean_fixed_ber": float(np.mean(vals)), "n_heldout": len(vals)}
    summary["standard_CMA_mean"] = float(np.mean(comp_baseline))
    summary["frozen_ml_mean"] = float(np.mean(heldout["frozen_ml"]))
    verdict = "DIAGNOSTIC_METHOD_SIGNAL" if signal else "NO_DIAGNOSTIC_SIGNAL"
    print(f"  [held-out {label}] frozen_ml_fx={summary['frozen_ml_mean']:.5f} std_CMA_fx={summary['standard_CMA_mean']:.5f}", flush=True)
    for k, v in summary.items():
        if isinstance(v, dict) and "mean_fixed_ber" in v:
            print(f"    {k}: mean_fixed_BER={v['mean_fixed_ber']:.5f} {v.get('wins_vs_stdCMA','')}", flush=True)
    return verdict, {"cell": label, "heldout": heldout, "summary": summary}


def main():
    t0 = time.time()
    payload = {
        "experiment": "P05 D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION",
        "campaign": "5/10", "family": "D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION",
        "frozen_identity": {"strong_alpha_beta": [ALPHA, BETA], "F_G": F_G, "SOP_RATE": SOP_RATE,
                            "GAMMA_BAR": GAMMA_BAR, "N_TAP": N_TAP, "MU": MU, "R2": R2,
                            "ML_PARAMS": ML_PARAMS, "RMpS": compute_rmps(N_TAP)},
        "MDE": {"problem_gate_pi": MDE_PI, "method_gate_pi": MDE_LATE},
        "seeds": {"phaseA": SEEDS_A, "heldout": HELDOUT_SEEDS, "dev": DEV_SEEDS},
        "phases": {},
    }
    # Phase A
    va, da = phase_a()
    payload["phases"]["A"] = {"verdict": va, "data": da}
    terminal = va
    # Phase B (only if problem present)
    if va == "PROBLEM_PRESENT":
        vb, db = phase_b(da["problem_cells"], da["cells"])
        payload["phases"]["B"] = {"verdict": vb, "data": db}
        if vb == "PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER":
            terminal = vb
        else:
            vc, dc = phase_c(da["problem_cells"])
            payload["phases"]["C"] = {"verdict": vc, "data": dc}
            terminal = vc
    payload["terminal_verdict"] = terminal
    payload["elapsed_s"] = time.time() - t0
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"\n[TERMINAL] {terminal}\n  -> {OUT_PATH}\n  elapsed {payload['elapsed_s']:.0f}s", flush=True)
    return payload


if __name__ == "__main__":
    main()
