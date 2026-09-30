"""Shared helpers for decode-budget-rule (contract.yaml v1, FROZEN).

Rule semantics (deployment-faithful, evaluated offline on logged trajectories;
flooding statelessness makes the logged prefix identical whether or not the
decoder would later abort, per rescue_decoder header probe):
  - accept when s_t == 0 (cost t, N6-proven FER-equivalent early stop);
  - at checkpoints CP = {20, 30, 50, 100} reached without acceptance, abort if
    the pre-registered hopeless criterion fires (cost t, marked failure);
  - otherwise run to CAP = 200.
"""

from __future__ import annotations

import numpy as np

CAP = 200
CP = [20, 30, 50, 100]
WINDOW = 8
_SLOPE_W = np.array([-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5])

# outcome codes
ACCEPT = 0      # syndrome hit 0 at t, accepted (correct iff acc_info_ok)
CUT_CORRECT = 1  # aborted, label says never converges (true death cut)
CUT_WRONG = 2   # aborted, label says converges later (FER loss)
EXHAUST = 3     # no acceptance, no abort, ran to CAP (failure)


def first_zero(sw: np.ndarray) -> np.ndarray:
    """[N,200] syndrome weights -> converged_at (1-based; -1 = never within 200)."""
    z = sw == 0
    any_z = z.any(axis=1)
    return np.where(any_z, z.argmax(axis=1) + 1, -1)


def window_stats(sw: np.ndarray) -> dict[int, dict[str, np.ndarray]]:
    """Per-checkpoint receiver-visible features from the trajectory so far."""
    out: dict[int, dict[str, np.ndarray]] = {}
    for c in CP:
        w = sw[:, c - WINDOW:c]  # iterations c-7 .. c (0-based slice)
        d = np.diff(w, axis=1)
        sgn = np.sign(d)
        out[c] = {
            "mean8": w.mean(axis=1),
            "level": sw[:, c - 1],
            "red": sw[:, c - 1] / np.maximum(sw[:, 0], 1),
            # OLS slope sign over the window: sum((x - xbar) * y) >= 0
            "slope8_nonneg": (w @ _SLOPE_W) >= 0,
            "osc8": (sgn[:, 1:] * sgn[:, :-1] < 0).sum(axis=1),
        }
    return out


def criterion_mask(stats: dict[int, dict], c: int, spec: dict) -> np.ndarray:
    fam = spec["family"]
    st = stats[c]
    if fam == "RA":
        return st["mean8"] >= spec["tau"]
    if fam == "RC":
        return st["level"] >= spec["tau"]
    if fam == "RD":
        return st["red"] >= spec["tau"]
    if fam == "RB":
        return (st["mean8"] >= spec["tau"]) & st["slope8_nonneg"]
    if fam == "RE":
        return (st["osc8"] >= spec["tau_o"]) & (st["mean8"] >= spec["tau_m"])
    raise ValueError(f"unknown rule family {fam}")


def simulate_rule(
    sw: np.ndarray, conv: np.ndarray, spec: dict
) -> tuple[np.ndarray, np.ndarray]:
    """Offline rule simulation.

    Returns (stop_iter [N], outcome [N]) -- correctness of accepted frames is
    resolved by the caller via acc_info_ok (accepted-but-wrong measured in the
    trajectory run, expected 0 per N6).
    """
    n = sw.shape[0]
    stats = window_stats(sw)
    aborted_at = np.full(n, -1, dtype=np.int64)
    for c in CP:
        m = criterion_mask(stats, c, spec)
        elig = m & ((conv == -1) | (conv > c))  # accept wins at s_c == 0
        fresh = elig & (aborted_at == -1)
        aborted_at[fresh] = c
    stop = np.where(aborted_at > 0, aborted_at, np.where(conv > 0, conv, CAP))
    outcome = np.full(n, EXHAUST, dtype=np.int64)
    outcome[(aborted_at > 0) & (conv == -1)] = CUT_CORRECT
    outcome[(aborted_at > 0) & (conv > 0)] = CUT_WRONG
    outcome[(aborted_at < 0) & (conv > 0)] = ACCEPT
    return stop, outcome


def es_point(sw: np.ndarray, conv: np.ndarray, acc_ok: np.ndarray, cap: int):
    """NOMS+ES fixed-cap point from the same trajectory log.

    Returns (fer, mean_it, n_accepted_wrong).
    """
    accepted = (conv > 0) & (conv <= cap)
    stop = np.where(conv > 0, np.minimum(conv, cap), cap)
    wrong = accepted & (~acc_ok)
    fer = 1.0 - (accepted & acc_ok).sum() / sw.shape[0]
    return float(fer), float(stop.mean()), int(wrong.sum())


def candidate_specs() -> list[dict]:
    """The 28 pre-registered candidates from contract rule_family_preregistered."""
    specs: list[dict] = []
    for tau in [40, 60, 80, 100, 120, 140]:
        specs.append({"family": "RA", "tau": tau})
    for tau in [60, 80, 100, 120, 140, 160]:
        specs.append({"family": "RC", "tau": tau})
    for tau in [0.35, 0.45, 0.55, 0.65, 0.75]:
        specs.append({"family": "RD", "tau": tau})
    for tau in [40, 60, 80, 100, 120]:
        specs.append({"family": "RB", "tau": tau})
    for tau_o in [4, 5]:
        for tau_m in [60, 80, 100]:
            specs.append({"family": "RE", "tau_o": tau_o, "tau_m": tau_m})
    assert len(specs) == 28, len(specs)
    return specs


SIMPLICITY_ORDER = {"RA": 0, "RC": 1, "RD": 2, "RB": 3, "RE": 4}


def candidate_key(spec: dict) -> str:
    if spec["family"] == "RE":
        return f"RE_o{spec['tau_o']}_m{spec['tau_m']}"
    return f"{spec['family']}_{spec['tau']:g}"
