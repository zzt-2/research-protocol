"""P08-R2 Phase 1 — H7 reproduction: prove the receiver info-boundary leak.

DETERMINISTIC, run BEFORE any code change. Uses the CURRENT (still-broken) p08r_chain
to demonstrate that toggling the hidden truth `gamma_bar` — while holding
rX/rY/prefix/receiver-state/codeword/noise-realization fixed — changes the
deployable outputs (equalized samples, prefix residual, B0 LLR). This is illegal:
a receiver must not depend on the hidden SNR loop variable.

Chain (per p08r_run.build_realization):
    build_realization(real)  -> real.equalize()  -> blind h est (uses 1/(2*gamma_bar))
                                              -> mmse_equalize(rx, h, gamma_bar)
                                              -> amp_limit(.., 3.0)
    method_B0(eq, prefix)    -> estimate_sigma2_from_prefix(eq_prefix, tx_prefix)
                            -> demap -> LLR

We hold the REALIZATION (rX, rY, sX, sY, h, theta, prefix, codewords) fixed by
building it ONCE at a reference gamma_bar, then we MANUALLY flip the realization's
`gamma_bar` attribute to two different values and re-call equalize() + B0. Because
equalize() reads self.gamma_bar (lines 344, 358, 359), the equalized output must
change if H7 is real.

Outputs JSON: p08r2_h7_reproduce.json with max|ΔeqX|, max|Δ prefix resid|, max|ΔLLR|.
This file is the pre-code-change evidence referenced by p08r2_prefail_evidence.md.
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

from p08r_chain import (  # noqa: E402  (CURRENT chain, broken — evidence)
    get_gg_scenes, CodedContractR, CodecAdapterR, CalibrationPrefix,
    CodedRealizationR, split_prefix_data, estimate_sigma2_from_prefix,
)
from p08r_phaseA import method_B0, llr_per_cw_from_eq  # noqa: E402
from p08_coded_chain import maxlog_soft_demap_16qam  # noqa: E402

OUT = _SIM / "results" / "p08r2_receiver_info_repair"
OUT.mkdir(parents=True, exist_ok=True)


def build_and_equalize(seed, scene_ab, scene, f_g, gamma_bar, contract, codec, prefix):
    """Build ONE realization at gamma_bar, return (real, eq)."""
    real = CodedRealizationR(
        seed=seed, scene=scene, alpha=scene_ab[0], beta=scene_ab[1],
        f_g=f_g, sop_rate=1e-5, gamma_bar=gamma_bar,
        n_cw_per_pol=16, cw_n=contract.n, codec=codec, prefix=prefix,
        eval_block=100,
    ).realize()
    eq = real.equalize()
    return real, eq


def b0_llr_per_pol(real, eq, contract, codec, prefix, pol):
    """Reproduce method_B0's LLR for one polarization (no decode, just LLR)."""
    eqp, eqd = split_prefix_data(eq[f"eq{pol}"], real.n_prefix)
    sp, _ = split_prefix_data(getattr(real, f"s{pol}"), real.n_prefix)
    sig2 = estimate_sigma2_from_prefix(eqp, sp)
    llr = llr_per_cw_from_eq(eqd, sig2, contract)  # (n_cw, n)
    return sig2, llr, eqp, sp


def main():
    print("=" * 70)
    print("P08-R2 Phase 1 — H7 reproduction (BEFORE any code change)")
    print("=" * 70)
    scenes = get_gg_scenes()
    contract = CodedContractR()
    codec = CodecAdapterR(contract)
    prefix = CalibrationPrefix(n_prefix_symbols=32)

    # Reference realization built at gamma_ref. We then FLIP real.gamma_bar in-place
    # to gamma_flip and re-run equalize(). Because rX/rY/sX/sY/h/theta are already
    # materialized arrays, they do NOT change; only the read of self.gamma_bar inside
    # equalize() changes. If equalize() truly ignored gamma_bar (legal), Δ=0.
    seed = 7000
    scene, f_g = "weak", 1000.0
    ab = scenes[scene]
    g_ref = float(10 ** (12.0 / 10.0))   # 12 dB reference
    g_flip_hi = float(10 ** (18.0 / 10.0))  # pretend true SNR is 18 dB
    g_flip_lo = float(10 ** (8.0 / 10.0))   # pretend true SNR is 8 dB

    real_ref, eq_ref = build_and_equalize(seed, ab, scene, f_g, g_ref,
                                          contract, codec, prefix)

    results = {"seed": seed, "scene": scene, "f_g": f_g,
               "gamma_ref_dB": 12.0, "gamma_flip_hi_dB": 18.0, "gamma_flip_lo_dB": 8.0,
               "note": "realization arrays (rX,rY,sX,sY,h,theta) held fixed; only "
                       "real.gamma_bar attribute flipped to demonstrate equalize() leak"}

    per_pol = {}
    for pol in ("X", "Y"):
        sig2_ref, llr_ref, eqp_ref, sp_ref = b0_llr_per_pol(
            real_ref, eq_ref, contract, codec, prefix, pol)
        entry = {"sigma2_prefix_ref": sig2_ref}

        for label, g_flip in (("hi", g_flip_hi), ("lo", g_flip_lo)):
            # flip the hidden truth attribute; arrays stay identical
            real_ref.gamma_bar = g_flip
            eq_flip = real_ref.equalize()
            sig2_flip, llr_flip, eqp_flip, sp_flip = b0_llr_per_pol(
                real_ref, eq_flip, contract, codec, prefix, pol)
            d_eq_full = np.abs(eq_flip[f"eq{pol}"] - eq_ref[f"eq{pol}"])
            d_eqp = np.abs(eqp_flip - eqp_ref)  # equalized PREFIX residual change
            # prefix residual itself = eqp - sp; sp fixed so Δ(resid) = Δeqp
            d_llr = np.abs(llr_flip - llr_ref)
            entry[f"gamma_{label}_dB"] = 18.0 if label == "hi" else 8.0
            entry[f"max_abs_deq_{label}"] = float(np.max(d_eq_full))
            entry[f"max_abs_dprefix_eq_{label}"] = float(np.max(d_eqp))
            entry[f"max_abs_dprefix_resid_{label}"] = float(np.max(d_eqp))  # sp fixed
            entry[f"max_abs_dLLR_{label}"] = float(np.max(d_llr))
            entry[f"mean_abs_dLLR_{label}"] = float(np.mean(d_llr))
            entry[f"sigma2_prefix_{label}"] = sig2_flip
            print(f"  pol={pol} flip={label}({entry[f'gamma_{label}_dB']}dB): "
                  f"max|Δeq|={entry[f'max_abs_deq_{label}']:.3e}  "
                  f"max|Δprefix_resid|={entry[f'max_abs_dprefix_resid_{label}']:.3e}  "
                  f"max|ΔLLR|={entry[f'max_abs_dLLR_{label}']:.3e}  "
                  f"σ²_prefix {sig2_ref:.4e}->{sig2_flip:.4e}")
        # restore
        real_ref.gamma_bar = g_ref
        per_pol[pol] = entry

    # verdict: if any |Δ| > tol, H7 leak CONFIRMED
    tol_eq = 1e-12
    tol_llr = 1e-9
    leaks = []
    for pol, e in per_pol.items():
        for lab in ("hi", "lo"):
            if e[f"max_abs_deq_{lab}"] > tol_eq:
                leaks.append(f"{pol}.deq.{lab}={e[f'max_abs_deq_{lab}']:.2e}")
            if e[f"max_abs_dprefix_resid_{lab}"] > tol_eq:
                leaks.append(f"{pol}.dprefix.{lab}={e[f'max_abs_dprefix_resid_{lab}']:.2e}")
            if e[f"max_abs_dLLR_{lab}"] > tol_llr:
                leaks.append(f"{pol}.dLLR.{lab}={e[f'max_abs_dLLR_{lab}']:.2e}")
    h7_confirmed = len(leaks) > 0
    results["per_pol"] = per_pol
    results["h7_leak_confirmed"] = bool(h7_confirmed)
    results["leak_channels"] = leaks
    results["tol_eq"] = tol_eq
    results["tol_llr"] = tol_llr
    results["verdict"] = ("H7 CONFIRMED: equalize()/prefix-residual/LLR change when "
                          "hidden gamma_bar is flipped (receiver consumes true SNR)"
                          if h7_confirmed else
                          "H7 NOT confirmed (unexpected — re-examine)")

    print(f"\n  >>> {results['verdict']}")
    print(f"  leak channels: {leaks}")

    with open(OUT / "p08r2_h7_reproduce.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nEvidence written to {OUT / 'p08r2_h7_reproduce.json'}")


if __name__ == "__main__":
    main()
