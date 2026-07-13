"""PROMPT-011 minimal root-cause diagnostic for the 2x2 CMA update.

Hypothesis: the current scalar-error update is not the standard complex CMA
gradient because it omits the equalizer-output factor.  The standard update
implemented here uses the repository convention ``z = x @ w``:

    w <- w + mu * mean((R2 - |z|^2) * z * conj(x))

This is the conjugated-coordinate form of the conventional descent update.
ACP 2025 Eq. (2) confirms the required output factor and conjugate-input
structure, but its printed error sign points uphill despite the surrounding
text calling the update gradient descent; this implementation follows the
mathematical descent sign rather than claiming literal sign agreement.
The signal/channel model is reused unchanged from ``ml_long_seq_failure``.
"""
from __future__ import annotations

import argparse
import sys
import time
from itertools import permutations
from pathlib import Path

import numpy as np


SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))

from common._cma import CMAEqualizer2x2
from common._experiment import save_results
from ml_long_seq_failure import (
    F_G,
    GAMMA_BAR,
    MU_SAFE,
    N_TAP,
    R2_QPSK,
    SOP_RATE,
    compute_ber_phase_corrected,
    gen_channel,
    oracle_equalize,
    test_late_slice,
)
from params import SimulationConfig


N_SYMBOLS = 5_000_000
TURBULENCE = "strong"
DOMINANCE_RATIO = 1.5
DEFAULT_SEEDS = tuple(range(1000, 1010))
RESULT_PATH = (
    SIM_DIR / "results" / "cma-fade-divergence"
    / "prompt011_cma_root_diagnostic.json"
)


def save_diagnostic_results(payload, path=RESULT_PATH):
    """Save through the repository metadata-injecting result writer."""
    save_results(payload, str(path), "prompt011_cma_root_diagnostic")


class StandardCMAEqualizer2x2(CMAEqualizer2x2):
    """2x2 block CMA with the standard complex output-weighted gradient."""

    def equalize(self, rX, rY, block_size=64):
        from numpy.lib.stride_tricks import sliding_window_view

        n = len(rX)
        length = self.n_tap
        half = length // 2
        zX = np.zeros(n, dtype=complex)
        zY = np.zeros(n, dtype=complex)
        w_norm_traj = np.zeros(n)
        z_amp_traj = np.zeros(n)
        rX_win = sliding_window_view(rX, length)
        rY_win = sliding_window_view(rY, length)
        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3
        diverged = False
        diverge_idx = None
        n_valid = n - length + 1

        for start in range(0, (n_valid // block_size) * block_size, block_size):
            end = start + block_size
            x_block = rX_win[start:end]
            y_block = rY_win[start:end]
            zx_block = x_block @ self.wxx + y_block @ self.wxy
            zy_block = x_block @ self.wyx + y_block @ self.wyy
            out_start = start + half
            zX[out_start:out_start + block_size] = zx_block
            zY[out_start:out_start + block_size] = zy_block

            error_x = self.R2 - np.abs(zx_block) ** 2
            error_y = self.R2 - np.abs(zy_block) ** 2
            # Standard complex CMA descent for z = x @ w.  The current
            # common implementation omits zx_block / zy_block here.
            self.wxx += self.mu * np.mean(
                error_x[:, None] * zx_block[:, None] * np.conj(x_block), axis=0
            )
            self.wxy += self.mu * np.mean(
                error_x[:, None] * zx_block[:, None] * np.conj(y_block), axis=0
            )
            self.wyx += self.mu * np.mean(
                error_y[:, None] * zy_block[:, None] * np.conj(x_block), axis=0
            )
            self.wyy += self.mu * np.mean(
                error_y[:, None] * zy_block[:, None] * np.conj(y_block), axis=0
            )

            cur_norm = self.weights_norm()
            cur_amp = float(np.max(np.maximum(np.abs(zx_block), np.abs(zy_block))))
            record_idx = out_start + block_size - 1
            w_norm_traj[record_idx] = cur_norm
            z_amp_traj[record_idx] = cur_amp
            if (cur_norm > norm_thresh or cur_amp > z_amp_thresh
                    or not np.isfinite(cur_norm)):
                diverged = True
                diverge_idx = record_idx
                break

        return {
            "zX": zX,
            "zY": zY,
            "w_norm_traj": w_norm_traj,
            "z_amp_traj": z_amp_traj,
            "diverged": diverged,
            "diverge_idx": diverge_idx,
            "final_w_norm": self.weights_norm(),
            "init_w_norm": self._init_norm,
        }


def _abs_corr(a, b):
    a = np.asarray(a) - np.mean(a)
    b = np.asarray(b) - np.mean(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(abs(np.vdot(a, b)) / denom) if denom else 0.0


def _classify(corr):
    corr = np.asarray(corr)
    choices = []
    for row in corr:
        order = np.argsort(row)
        if row[order[-1]] < DOMINANCE_RATIO * max(row[order[-2]], 1e-15):
            return "mixed"
        choices.append(int(order[-1]))
    if choices == [0, 1]:
        return "normal"
    if choices == [1, 0]:
        return "swap"
    return "same-source"


def _metrics(z_x, z_y, s_x, s_y, diverged):
    corr = [
        [_abs_corr(z_x, s_x), _abs_corr(z_x, s_y)],
        [_abs_corr(z_y, s_x), _abs_corr(z_y, s_y)],
    ]
    fixed_x = compute_ber_phase_corrected(z_x, s_x)
    fixed_y = compute_ber_phase_corrected(z_y, s_y)
    assignment_results = []
    outputs = (z_x, z_y)
    sources = (s_x, s_y)
    for assignment in permutations((0, 1)):
        per_output = [
            compute_ber_phase_corrected(outputs[i], sources[assignment[i]])
            for i in range(2)
        ]
        assignment_results.append((float(np.mean(per_output)), assignment, per_output))
    best_mean, best_assignment, best_per_output = min(assignment_results, key=lambda x: x[0])
    return {
        "label_fixed_ber": {"X": fixed_x, "Y": fixed_y, "mean": (fixed_x + fixed_y) / 2},
        "permutation_invariant_ber": {
            "mean": best_mean,
            "per_output": best_per_output,
            "assignment": ["X" if i == 0 else "Y" for i in best_assignment],
        },
        "abs_corr_output_source": {"zX": {"sX": corr[0][0], "sY": corr[0][1]},
                                    "zY": {"sX": corr[1][0], "sY": corr[1][1]}},
        "abs_corr_zX_zY": _abs_corr(z_x, z_y),
        "classification": _classify(corr),
        "diverged": bool(diverged),
    }


def run(seeds=DEFAULT_SEEDS):
    cfg = SimulationConfig()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    trials = []
    for seed in seeds:
        started = time.time()
        r_x, r_y, s_x, s_y, h, theta = gen_channel(
            N_SYMBOLS, alpha, beta, F_G, SOP_RATE, int(seed)
        )
        late_start, late_end = test_late_slice(N_SYMBOLS)
        methods = {}
        for label, cls in (
            ("current_scalar_error_cma", CMAEqualizer2x2),
            ("standard_complex_cma", StandardCMAEqualizer2x2),
        ):
            equalizer = cls(n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK)
            result = equalizer.equalize(r_x, r_y)
            methods[label] = _metrics(
                result["zX"][late_start:late_end],
                result["zY"][late_start:late_end],
                s_x[late_start:late_end],
                s_y[late_start:late_end],
                result["diverged"],
            )
            methods[label]["diverge_idx"] = result["diverge_idx"]
            del result, equalizer

        oracle_x, oracle_y = oracle_equalize(r_x, r_y, h, theta, GAMMA_BAR)
        methods["oracle"] = _metrics(
            oracle_x[late_start:late_end], oracle_y[late_start:late_end],
            s_x[late_start:late_end], s_y[late_start:late_end], False,
        )
        trials.append({"seed": int(seed), "methods": methods, "elapsed_s": time.time() - started})
        print(
            f"seed={seed} "
            + " ".join(
                f"{name}:fixed={value['label_fixed_ber']['mean']:.4f},"
                f"pi={value['permutation_invariant_ber']['mean']:.4f},"
                f"class={value['classification']}"
                for name, value in methods.items()
            ), flush=True,
        )

    summaries = {}
    for method in ("current_scalar_error_cma", "standard_complex_cma", "oracle"):
        summaries[method] = {}
        for key, getter in {
            "label_fixed_mean_ber": lambda x: x["label_fixed_ber"]["mean"],
            "permutation_invariant_mean_ber": lambda x: x["permutation_invariant_ber"]["mean"],
            "abs_corr_zX_zY": lambda x: x["abs_corr_zX_zY"],
        }.items():
            values = [getter(t["methods"][method]) for t in trials]
            summaries[method][key] = {"mean": float(np.mean(values)), "std": float(np.std(values)),
                                      "values": values}
        summaries[method]["classification_counts"] = {
            label: sum(t["methods"][method]["classification"] == label for t in trials)
            for label in ("normal", "swap", "same-source", "mixed")
        }
        summaries[method]["diverged_count"] = sum(
            t["methods"][method]["diverged"] for t in trials
        )

    payload = {
        "experiment": "PROMPT-011 minimal CMA root diagnostic",
        "hypothesis": "current CMA omits the output factor in the standard complex gradient",
        "parameters": {"N": N_SYMBOLS, "SOP": SOP_RATE, "f_G": F_G,
                       "turbulence": TURBULENCE, "snr_db": 20, "modulation": "QPSK",
                       "n_tap": N_TAP, "mu": MU_SAFE, "R2": R2_QPSK,
                       "seeds": list(map(int, seeds)), "late_slice": [late_start, late_end]},
        "classification_rule": f"dominant correlation ratio >= {DOMINANCE_RATIO}; otherwise mixed",
        "summaries": summaries,
        "trials": trials,
    }
    save_diagnostic_results(payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=10, help="use first N shared seeds (1000+)")
    args = parser.parse_args()
    run(DEFAULT_SEEDS[:args.seeds])
