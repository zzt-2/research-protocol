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


# --------------------------------------------------------------------- #
# round-2 extensions (contract_r2.yaml, frozen 2026-09-30)
# --------------------------------------------------------------------- #
# checkpoint pairs for persistence families: (cut_cp, reference_cp)
PAIR_CP = {30: 20, 50: 30, 100: 50}


def criterion_mask_r2(stats: dict, c: int, spec: dict) -> np.ndarray:
    """Round-2 deployable families (checkpoint-pair persistence)."""
    fam = spec["family"]
    if c not in PAIR_CP:
        return np.zeros(stats[c]["level"].shape, dtype=bool)  # cp20: no pair yet
    st, stp = stats[c], stats[PAIR_CP[c]]
    if fam == "PL":  # F2 persist-level
        return (stp["level"] >= spec["ta"]) & (st["level"] >= spec["tb"])
    if fam == "PR":  # F3 persist-red
        return (stp["red"] >= spec["tau"]) & (st["red"] >= spec["tau"])
    raise ValueError(fam)


def simulate_rule_r2(sw: np.ndarray, conv: np.ndarray, spec: dict):
    """Dispatch: round-1 families + r2 checkpoint families + r2 per-iteration
    ablations (C1/OSC). Returns (stop_iter, outcome) like simulate_rule."""
    fam = spec["family"]
    if fam == "C1":
        return _simulate_c1(sw, conv, spec)
    if fam == "OSC":
        return _simulate_osc(sw, conv, spec)
    if fam in ("PL", "PR"):
        n = sw.shape[0]
        stats = window_stats(sw)
        aborted_at = np.full(n, -1, dtype=np.int64)
        for c in CP:
            if c not in PAIR_CP:
                continue
            m = criterion_mask_r2(stats, c, spec)
            elig = m & ((conv == -1) | (conv > c))
            fresh = elig & (aborted_at == -1)
            aborted_at[fresh] = c
        stop = np.where(aborted_at > 0, aborted_at,
                        np.where(conv > 0, conv, CAP))
        outcome = np.full(n, EXHAUST, dtype=np.int64)
        outcome[(aborted_at > 0) & (conv == -1)] = CUT_CORRECT
        outcome[(aborted_at > 0) & (conv > 0)] = CUT_WRONG
        outcome[(aborted_at < 0) & (conv > 0)] = ACCEPT
        return stop, outcome
    return simulate_rule(sw, conv, spec)  # round-1 families (RA/RC/RD/RB/RE)


def _simulate_c1(sw: np.ndarray, conv: np.ndarray, spec: dict):
    """GC-LDPC C1-type: from l1_min, per-iteration abort if s_t > s_thr OR
    s failed to strictly decrease T consecutive steps (v1 non-increase)."""
    n, cap = sw.shape[0], sw.shape[1]
    l1_min = spec.get("l1_min", 20)
    thr, T = spec["s_thr"], spec["T"]
    aborted_at = np.full(n, -1, dtype=np.int64)
    stag = np.zeros(n, dtype=np.int64)
    for t in range(1, cap + 1):
        idx = t - 1
        if t >= 2:
            nondec = sw[:, idx] >= sw[:, idx - 1]
            # stagnation observations counted only for t > l1_min (paper
            # reading: "v1 non-increase T consecutive times while l > l1_min")
            stag = np.where(nondec, stag + 1, 0) if t > l1_min else 0
        if t <= l1_min:
            continue
        trig = (sw[:, idx] > thr) | (stag >= T)
        # accept priority: frames with conv == t accepted before any check
        elig = trig & (aborted_at < 0) & ((conv == -1) | (conv > t))
        aborted_at[elig] = t
    stop = np.where(aborted_at > 0, aborted_at, np.where(conv > 0, conv, CAP))
    outcome = np.full(n, EXHAUST, dtype=np.int64)
    outcome[(aborted_at > 0) & (conv == -1)] = CUT_CORRECT
    outcome[(aborted_at > 0) & (conv > 0)] = CUT_WRONG
    outcome[(aborted_at < 0) & (conv > 0)] = ACCEPT
    return stop, outcome


def _simulate_osc(sw: np.ndarray, conv: np.ndarray, spec: dict):
    """N04 bootstrapped 3-shift-register oscillation stop: from l_min,
    s_t == s_{t-2} and s_t > 0 -> abort."""
    n, cap = sw.shape[0], sw.shape[1]
    l_min = spec["l_min"]
    aborted_at = np.full(n, -1, dtype=np.int64)
    for t in range(max(l_min, 3), cap + 1):
        trig = (sw[:, t - 1] == sw[:, t - 3]) & (sw[:, t - 1] > 0)
        elig = trig & (aborted_at < 0) & ((conv == -1) | (conv > t))
        aborted_at[elig] = t
    stop = np.where(aborted_at > 0, aborted_at, np.where(conv > 0, conv, CAP))
    outcome = np.full(n, EXHAUST, dtype=np.int64)
    outcome[(aborted_at > 0) & (conv == -1)] = CUT_CORRECT
    outcome[(aborted_at > 0) & (conv > 0)] = CUT_WRONG
    outcome[(aborted_at < 0) & (conv > 0)] = ACCEPT
    return stop, outcome


def pool_simulate(sw: np.ndarray, conv: np.ndarray, spec: dict, *,
                  block: int = 32, budget_per_frame: float = 20.0):
    """Exploratory cross-frame budget pool (contract_r2).

    Blocks of `block` frames (seed order) share budget B = block * c.
    Decisions happen only at checkpoints (deployable semantics): frames that
    hit syndrome-0 stop at conv; the frozen rule's cut criterion fires at
    checkpoints; after cuts, if the remaining budget cannot carry all active
    frames to the next checkpoint, frames are stopped at c in decreasing s_c
    order. Segment commitment already made may overshoot the pool (flagged);
    actual mean_it is what gets reported.
    Returns (stop_iter, outcome, per-block overshoot flags).
    """
    n = sw.shape[0]
    stop = np.full(n, CAP, dtype=np.int64)
    outcome = np.full(n, EXHAUST, dtype=np.int64)
    stats = window_stats(sw)
    use_r1 = spec["family"] in ("RA", "RC", "RD", "RB", "RE")
    overshoot = []
    cps = [0] + CP + [CAP]
    for b0 in range(0, n, block):
        idx = list(range(b0, min(b0 + block, n)))
        budget = len(idx) * budget_per_frame
        active = list(idx)
        for k in range(1, len(cps)):
            c_prev, c = cps[k - 1], cps[k]
            seg = c - c_prev
            # acceptance inside the segment: exact per-frame cost up to conv
            still = []
            for i in active:
                if 0 < conv[i] <= c:
                    stop[i] = conv[i]
                    outcome[i] = ACCEPT
                    budget -= max(conv[i] - c_prev, 0)
                else:
                    still.append(i)
            # all remaining frames ran the full segment to reach checkpoint c
            budget -= len(still) * seg
            if c in CP and still:
                m = (criterion_mask(stats, c, spec) if use_r1
                     else criterion_mask_r2(stats, c, spec))
                cut = [i for i in still
                       if m[i] and (conv[i] == -1 or conv[i] > c)]
                for i in cut:
                    stop[i] = c
                    outcome[i] = CUT_CORRECT if conv[i] == -1 else CUT_WRONG
                still = [i for i in still if i not in set(cut)]
            # budget guard: afford carrying actives to the next checkpoint
            if k + 1 < len(cps) and still:
                nxt = cps[k + 1]
                need = len(still) * (nxt - c)
                while still and budget < need:
                    worst = max(still, key=lambda i: sw[i, c - 1])
                    still.remove(worst)
                    stop[worst] = c
                    outcome[worst] = EXHAUST  # budget-stopped at checkpoint
                    need = len(still) * (nxt - c)
            active = still
        overshoot.append(budget < 0)
    return stop, outcome, overshoot
