# -*- coding: utf-8 -*-
"""P02 (T029) — Cheap alternative: region-retuned cand_rank threshold.

The body is IDENTICAL to `decide_cand_rank` (P01 frozen, _p01_adapter_and_candidates.py
lines 205-217) EXCEPT the stage-1 `ref_snr_db` constant is read from a module-global
(`_FROZEN_REF_SNRS["weakretune"]`) that is frozen on DEV seeds 50-59 ONLY and never
touched again. Default 9.0 -> identical to cand_rank until tuned.

Discipline (T029 §2 / §3):
  - This adds NO new method logic. The only delta vs cand_rank is the value of a
    single scalar frozen at dev-time.
  - Receiver-visible only: uses raw rx + known pilots + the (biased) nominal gamma_hat
    is NOT consumed (cand_rank is gamma-magnitude-free at stage-1; stage-2 uses the
    pilot estimator). TRUE gamma never enters this decide.
  - `freeze_ref(name, val)` is the single dev-time entry point; held-out runs MUST
    use the value recorded in dev_tuning.json and never call freeze_ref again.

Selector signature (matches the multidelta runner):
    decide_fn(raw, gamma_hat_db, gamma_hat_lin, b) -> 'da' or 'nda'
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path[:0] = [_SIM_ROOT, os.path.join(_SIM_ROOT, 'simulator'), _HERE]

import _a4_switch_common768_30seed as A  # noqa: E402  (frozen selector)
from _p01_adapter_and_candidates import estimate_snr_pilot  # noqa: E402  (frozen pilot estimator)

# Module-global frozen reference SNR for the weakretune cheap alternative.
# Default 9.0 => identical to cand_rank until dev tuning overrides it.
_FROZEN_REF_SNRS = {"weakretune": 9.0}


def freeze_ref(name, val):
    """DEV-ONLY setter: freeze the reference SNR for cheap alternative `name`.

    Called once during dev tuning (seeds 50-59) to record the chosen value; the
    held-out run MUST reuse that frozen value (set once at startup from
    dev_tuning.json) and never re-tune.
    """
    _FROZEN_REF_SNRS[name] = float(val)


def get_ref(name="weakretune"):
    """Read-only accessor for the frozen reference SNR."""
    return float(_FROZEN_REF_SNRS[name])


def decide_adapter_weakretune(raw, gamma_hat_db, gamma_hat_lin, b):
    """Cheap alternative: cand_rank body with ref_snr_db frozen at dev-time.

    Body is line-for-line identical to decide_cand_rank EXCEPT ref_snr_db is read
    from the module-global _FROZEN_REF_SNRS["weakretune"]. gamma-magnitude-free
    at stage-1; stage-2 uses the frozen pilot SNR estimator (never true gamma).
    """
    ref_snr_db = _FROZEN_REF_SNRS["weakretune"]
    pwr = np.abs(raw) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    # stage-1 boundary fixed at the (dev-frozen) reference SNR -> gamma-magnitude-free
    if cv < A.cv_awgn_theory(ref_snr_db) * A.CV_MARGIN:
        return 'nda'
    # stage-2: pilot-estimated gamma for the (still magnitude-dependent) gamma_eff test
    g_est_db = estimate_snr_pilot(raw)
    g_est_lin = 10.0 ** (g_est_db / 10.0)
    h = max(float(np.mean(pwr) - 1.0 / (2 * g_est_lin)), 1e-6)
    return 'da' if g_est_db + 10 * np.log10(h) < A.GAMMA_EFF_TH else 'nda'


def decide_adapter_weakretune_fn():
    """Return (fn, needs_pilot=True, needs_reset=False) for the multidelta runner.

    Compatible with PR.run_case_multidelta(extra_selector={name: {...}}).
    needs_pilot=True because stage-2 calls estimate_snr_pilot which reads the
    per-window pilot tx symbols published via AD.set_window_pilots.
    """
    return decide_adapter_weakretune, True, False
