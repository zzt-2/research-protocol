"""P08-R2 metamorphic information gate — runtime proof that the deployable
receiver path consumes NO hidden truth (gamma_bar / h_truth / theta / TX data).

Metamorphic testing principle (H7 fix runtime guarantee): hold the realization
arrays (rX, rY, sX, sY, h, theta, prefix, codewords, noise) fixed; flip only the
HIDDEN `gamma_bar` attribute to several different values; re-run equalize() +
method_B0. If the receiver path truly ignores gamma_bar (the H7 fix), the
deployable outputs (eqX, prefix residual, B0 LLR) must NOT change (Δ < tol).

This is the runtime counterpart to the static AST recursion check (H8 fix) in
p08r2_verify.py. Both must pass before Phase A is allowed to run.

Tolerances (float32-cumulative-aware):
  ΔeqX, ΔeqY, Δprefix_resid < 1e-12   (equalized samples — real64 throughout)
  ΔLLR < 1e-9                         (LLR has demap + reshape stack)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

torch.set_default_device("cpu")

_THIS = Path(__file__).resolve().parent
_SIM = _THIS.parents[1]
for p in (str(_SIM), str(_THIS)):
    if p not in sys.path:
        sys.path.insert(0, p)

from p08r2_chain import (  # noqa: E402
    get_gg_scenes, CodedContractR, CodecAdapterR, CalibrationPrefix,
    CodedRealizationR2, split_prefix_data, estimate_sigma2_from_prefix,
)
from p08r_phaseA import llr_per_cw_from_eq  # noqa: E402 (reuse demapper)

OUT = _SIM / "results" / "p08r2_receiver_info_repair"
OUT.mkdir(parents=True, exist_ok=True)

TOL_EQ = 1e-12
TOL_LLR = 1e-9


def build_realization(seed, scene_ab, scene, f_g, gamma_bar, contract, codec, prefix):
    real = CodedRealizationR2(
        seed=seed, scene=scene, alpha=scene_ab[0], beta=scene_ab[1],
        f_g=f_g, sop_rate=1e-5, gamma_bar=gamma_bar,
        n_cw_per_pol=16, cw_n=contract.n, codec=codec, prefix=prefix,
        eval_block=100,
    ).realize()
    return real


def main():
    print("=" * 70)
    print("P08-R2 metamorphic information gate (runtime H7 verification)")
    print("=" * 70)
    scenes = get_gg_scenes()
    contract = CodedContractR()
    codec = CodecAdapterR(contract)
    prefix = CalibrationPrefix(n_prefix_symbols=32)

    g_ref = float(10 ** (12.0 / 10.0))
    flip_values_db = (6.0, 9.0, 15.0, 18.0, 22.0)  # hidden truth flipped to these

    # test on a few representative (scene, fG) cells
    cells = [("weak", 1000.0), ("moderate", 100.0), ("strong", 100.0)]
    seed = 8000  # fresh test seed (disjoint from dev 6000-6019)
    all_pass = True
    per_cell = {}

    for scene, f_g in cells:
        ab = scenes[scene]
        real = build_realization(seed, ab, scene, f_g, g_ref, contract, codec, prefix)
        eq_ref = real.equalize()
        cell_entry = {"gamma_ref_dB": 12.0, "flips": []}
        for pol in ("X", "Y"):
            eqp_r0, _ = split_prefix_data(eq_ref[f"eq{pol}"], real.n_prefix)
            sp_r0, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
            cell_entry[f"ref_sigma2_prefix_{pol}"] = estimate_sigma2_from_prefix(eqp_r0, sp_r0)
            cell_entry[f"ref_sigma2_pre_{pol}"] = float(eq_ref["sigma2_pre"])

        for flip_db in flip_values_db:
            g_flip = float(10 ** (flip_db / 10.0))
            real.gamma_bar = g_flip  # flip the HIDDEN truth; arrays stay identical
            eq_flip = real.equalize()
            flip_entry = {"gamma_flip_dB": flip_db}
            for pol in ("X", "Y"):
                # recompute ref and flip LLR cleanly from the respective eq arrays
                eqp_r, eqd_r = split_prefix_data(eq_ref[f"eq{pol}"], real.n_prefix)
                sp_r, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
                sig2_r = estimate_sigma2_from_prefix(eqp_r, sp_r)
                llr_r = llr_per_cw_from_eq(eqd_r, sig2_r, contract)
                eqp_f, eqd_f = split_prefix_data(eq_flip[f"eq{pol}"], real.n_prefix)
                sp_f, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
                sig2_f = estimate_sigma2_from_prefix(eqp_f, sp_f)
                llr_f = llr_per_cw_from_eq(eqd_f, sig2_f, contract)
                d_eq = np.abs(eq_flip[f"eq{pol}"] - eq_ref[f"eq{pol}"])
                d_prefix_resid = np.abs((eqp_f - sp_f) - (eqp_r - sp_r))
                d_llr = np.abs(llr_f - llr_r)
                flip_entry[f"max_abs_deq_{pol}"] = float(np.max(d_eq))
                flip_entry[f"max_abs_dprefix_resid_{pol}"] = float(np.max(d_prefix_resid))
                flip_entry[f"max_abs_dLLR_{pol}"] = float(np.max(d_llr))
                flip_entry[f"sigma2_pre_flip_{pol}"] = float(eq_flip["sigma2_pre"])
                flip_entry[f"sigma2_prefix_flip_{pol}"] = sig2_f
                # gate check
                ok = (flip_entry[f"max_abs_deq_{pol}"] < TOL_EQ and
                      flip_entry[f"max_abs_dprefix_resid_{pol}"] < TOL_EQ and
                      flip_entry[f"max_abs_dLLR_{pol}"] < TOL_LLR)
                flip_entry[f"pass_{pol}"] = bool(ok)
                if not ok:
                    all_pass = False
            cell_entry["flips"].append(flip_entry)
            # restore gamma_bar before next flip
            real.gamma_bar = g_ref
        per_cell[f"{scene}|{f_g}"] = cell_entry
        # report worst per cell
        worst_deq = max(f.get("max_abs_deq_X", 0) for f in cell_entry["flips"])
        worst_dllr = max(f.get("max_abs_dLLR_X", 0) for f in cell_entry["flips"])
        print(f"  {scene}/fG={f_g}: worst max|ΔeqX|={worst_deq:.2e}  "
              f"worst max|ΔLLR_X|={worst_dllr:.2e}")

    result = {
        "tol_eq": TOL_EQ, "tol_llr": TOL_LLR,
        "test_seed": seed, "gamma_ref_dB": 12.0,
        "flip_values_dB": list(flip_values_db),
        "cells": list(f"{s}|{f}" for s, f in cells),
        "per_cell": per_cell,
        "metamorphic_gate_pass": bool(all_pass),
        "verdict": ("PASS — flipping hidden gamma_bar does NOT change any "
                    "deployable output (equalize respects receiver information "
                    "boundary)" if all_pass else
                    "FAIL — deployable output still depends on gamma_bar (H7 "
                    "fix incomplete)"),
    }
    print(f"\n  >>> {result['verdict']}")
    with open(OUT / "p08r2_metamorphic_gate.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"  gate result -> {OUT / 'p08r2_metamorphic_gate.json'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
