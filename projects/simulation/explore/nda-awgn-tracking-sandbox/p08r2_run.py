"""P08-R2 Phase A orchestrator — H7/H9 repaired, fresh-seed crossing experiment.

Execution order (D049):
  0. metamorphic information gate (EXECUTION_INVALID gate) — must PASS first
  1. AWGN B0 sanity (EXECUTION_INVALID gate)
  2. dev workspace scan (B0/O1/O2) to find achievable SNR/FER region
  3. freeze metric (Primary B fixed-SNR paired FER) BEFORE reading test
  4. tune B1/B2 on dev_tune
  5. test on FRESH test seeds 8000-8039 (disjoint from P08-R's observed 7000-7039)
  6. trajectory-cluster bootstrap CI; report CI half-width honestly
  7. terminal verdict with EVIDENCE_INSUFFICIENT state (H9 fix)

H9 fixes vs p08r_run:
  - MDE = 0.05 a-priori (NOT post-hoc power threshold)
  - NO per-trajectory min(B1,B2); B2 is the single pre-registered comparator,
    AND B0-B1 / B0-B2 deltas reported separately
  - CI_lo=0 + CI_hw > MDE/2  ⇒  EVIDENCE_INSUFFICIENT (not ABSENT)
  - fresh test seeds 8000-8039
"""
from __future__ import annotations

import json
import sys
import time
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
    CodedRealizationR2,
)
from p08r2_phaseA import (  # noqa: E402
    MetricContractR2, bootstrap_ci, ci_half_width,
    method_B0, method_B1, method_B2, method_oracle,
    score_trajectory, trajectory_evidence,
)
import p08r2_metamorphic_gate as mmg  # noqa: E402 (Step 0 gate)

OUT = _SIM / "results" / "p08r2_receiver_info_repair"
OUT.mkdir(parents=True, exist_ok=True)


def build_realization(mc, scene_ab, contract, codec, prefix, seed, scene, f_g, snr_db):
    g = float(10 ** (snr_db / 10.0))
    real = CodedRealizationR2(
        seed=seed, scene=scene, alpha=scene_ab[0], beta=scene_ab[1],
        f_g=f_g, sop_rate=mc.sop_rate, gamma_bar=g,
        n_cw_per_pol=mc.n_cw_per_pol, cw_n=contract.n,
        codec=codec, prefix=prefix, eval_block=mc.eval_block,
    ).realize()
    eq = real.equalize()
    return real, eq, g


def run_method(method_id, real, eq, contract, codec, prefix, mc, b1_T=None, b2=None):
    if method_id == "B0":
        return method_B0(real, eq, contract, codec, prefix)
    if method_id == "B1":
        return method_B1(real, eq, contract, codec, prefix, b1_T)
    if method_id == "B2":
        return method_B2(real, eq, contract, prefix, b2["alpha"], b2["offset"], b2["llr_clip"])
    if method_id in ("O0", "O1", "O2"):
        return method_oracle(real, eq, contract, codec, prefix, method_id, mc.o2_block)
    raise ValueError(method_id)


def scan_workspace(mc, scenes_dict, contract, codec, prefix, seeds, snr_grid,
                   scenes, f_Gs, methods=("B0", "O1", "O2")):
    rows = []
    for seed in seeds:
        for scene in scenes:
            ab = scenes_dict[scene]
            for f_g in f_Gs:
                for db in snr_grid:
                    real, eq, g = build_realization(mc, ab, contract, codec, prefix,
                                                    seed, scene, f_g, db)
                    ev = trajectory_evidence(real, eq)
                    for m in methods:
                        kwargs = {}
                        if m == "B1": kwargs["b1_T"] = 1.0
                        if m == "B2": kwargs["b2"] = {"alpha": 0.75, "offset": 0.1, "llr_clip": 20.0}
                        us, sig = run_method(m, real, eq, contract, codec, prefix, mc, **kwargs)
                        sc = score_trajectory(real, us, contract)
                        rows.append({"method": m, "seed": seed, "scene": scene, "f_G": f_g,
                                     "esn0_dB": db, **sc, **ev, **sig})
    return rows


def main():
    t0 = time.time()
    mc = MetricContractR2()
    scenes_dict = get_gg_scenes()
    contract = CodedContractR()
    codec = CodecAdapterR(contract)
    prefix = CalibrationPrefix(n_prefix_symbols=mc.n_prefix_symbols)

    print("=" * 70)
    print("P08-R2 Phase A — H7/H8/H9 repaired chain")
    print("=" * 70)
    print(f"H1 GG scenes (params): weak={scenes_dict['weak']} "
          f"moderate={scenes_dict['moderate']} strong={scenes_dict['strong']}")
    print(f"H5 interleaver: num_bits_per_symbol=4, out_int n_moved="
          f"{int((codec.out_int != np.arange(contract.n)).sum())}/{contract.n}")
    print(f"H7 receiver-visible σ²_pre: prefix LS (32 sym, 2×2 H_eff, 60 dof)")
    print(f"H9 MDE (a-priori): mde_fer={mc.mde_fer} (NOT post-hoc power threshold)")
    print(f"H9 comparator: single pre-registered B2 (NO min(B1,B2) cherry-pick)")
    print(f"H9 test seeds: {mc.test_seeds[0]}-{mc.test_seeds[-1]} (FRESH, disjoint "
          f"from P08-R observed 7000-7039)")

    # --- Step 0: metamorphic information gate (EXECUTION_INVALID gate) ---
    print("\n--- Step 0: metamorphic information gate (H7 runtime proof) ---")
    mmg_pass = (mmg.main() == 0)
    print(f"  metamorphic gate: {'PASS' if mmg_pass else 'FAIL'}")
    if not mmg_pass:
        verdict = "EXECUTION_INVALID"
        print(f"\n  >>> VERDICT: {verdict} (metamorphic gate FAIL — H7 fix incomplete)")
        _save_final(mc, verdict, None, None, None, [], [], t0, exec_invalid=True)
        return

    # --- Step 1: AWGN B0 sanity ---
    print("\n--- Step 1: AWGN B0 sanity (EXECUTION_INVALID gate) ---")
    awgn_rows = []
    for db in (8.0, 10.0, 12.0):
        real, eq, g = build_realization(mc, scenes_dict["weak"], contract, codec, prefix,
                                        seed=599999, scene="weak", f_g=100.0, snr_db=db)
        us, _ = method_B0(real, eq, contract, codec, prefix)
        sc = score_trajectory(real, us, contract)
        awgn_rows.append({"esn0_dB": db, **sc})
        print(f"  AWGN-ish (weak,fG100) {db}dB: fer_traj={sc['fer_traj']:.3f}")
    exec_invalid = awgn_rows[-1]["fer_traj"] > 0.5
    print(f"  EXECUTION_INVALID? {exec_invalid}")

    # --- Step 2: dev workspace scan ---
    print("\n--- Step 2: dev workspace scan (B0/O1/O2) ---")
    dev_rows = scan_workspace(mc, scenes_dict, contract, codec, prefix,
                              seeds=mc.dev_seeds, snr_grid=mc.dev_snr_dB,
                              scenes=mc.scenes, f_Gs=mc.f_G_Hz, methods=("B0", "O1", "O2"))
    summary = {}
    for scene in mc.scenes:
        for f_g in mc.f_G_Hz:
            for db in mc.dev_snr_dB:
                for m in ("B0", "O1", "O2"):
                    rs = [r for r in dev_rows if r["scene"] == scene and r["f_G"] == f_g
                          and abs(r["esn0_dB"] - db) < 1e-9 and r["method"] == m]
                    if rs:
                        fers = [r["fer_traj"] for r in rs]
                        summary[(scene, f_g, db, m)] = (float(np.mean(fers)), len(fers))
    print(f"\nDev mean trajectory FER (B0 / O1 / O2):")
    print(f"{'scene':<10}{'fG':>6}{'SNR':>6}  {'B0':>7}{'O1':>7}{'O2':>7}  {'O2-B0':>7}")
    for scene in mc.scenes:
        for f_g in mc.f_G_Hz:
            for db in mc.dev_snr_dB:
                b0 = summary.get((scene, f_g, db, "B0"), (float('nan'), 0))[0]
                o1 = summary.get((scene, f_g, db, "O1"), (float('nan'), 0))[0]
                o2 = summary.get((scene, f_g, db, "O2"), (float('nan'), 0))[0]
                print(f"{scene:<10}{f_g:>6.0f}{db:>6.0f}  {b0:>7.3f}{o1:>7.3f}{o2:>7.3f}  {o2-b0:>+7.3f}")

    # --- Step 3: freeze metric BEFORE reading test ---
    print("\n--- Step 3: freeze metric (H4 + H9 a-priori MDE) BEFORE reading test ---")
    # Pre-registered cell selection: among dev cells with B0 FER in [0.1, 0.3]
    # (operating region), pick the one with largest oracle headroom (O2-B0) —
    # most favourable to detecting a calibration effect. Fall back to [0.15,0.5].
    def pick_cell(lo, hi):
        cands = []
        for scene in mc.scenes:
            for f_g in mc.f_G_Hz:
                for db in mc.dev_snr_dB:
                    b0 = summary.get((scene, f_g, db, "B0"), (None, 0))[0]
                    o2 = summary.get((scene, f_g, db, "O2"), (None, 0))[0]
                    if b0 is not None and lo <= b0 <= hi and o2 is not None:
                        cands.append((b0 - o2, scene, f_g, db, b0, o2))
        if not cands:
            return None
        cands.sort(reverse=True)
        return cands[0]

    pick = pick_cell(0.1, 0.3) or pick_cell(0.15, 0.5) or pick_cell(0.05, 0.7)
    if pick is None:
        chosen = (mc.scenes[1], mc.f_G_Hz[0], mc.dev_snr_dB[len(mc.dev_snr_dB) // 2])
    else:
        _, cs, cfg, cdb, _, _ = pick
        chosen = (cs, cfg, cdb)
    mc.chosen_cell = chosen
    mc.fixed_snr_dB_primaryB = (chosen[2],)
    # H9 fix: MDE stays at the a-priori 0.05; do NOT overwrite with power threshold.
    # Report the power-required-n for transparency.
    cs, cfg, cdb = chosen
    dev_b0_fers = [r["fer_traj"] for r in dev_rows if r["scene"] == cs and r["f_G"] == cfg
                   and abs(r["esn0_dB"] - cdb) < 1e-9 and r["method"] == "B0"]
    p_hat = float(np.mean(dev_b0_fers)) if dev_b0_fers else 0.2
    # required n at a-priori MDE for power 0.8 two-sided 0.05
    # z_{0.975}=1.95996, z_{0.8}=0.84162  (no scipy dep — hard-coded constants)
    z = 1.959963984540054 + 0.8416212335729143  # ≈ 2.802
    n_required = z * z * 2 * p_hat * (1 - p_hat) / (mc.mde_fer ** 2)
    print(f"  Frozen: Primary B at fixed SNR={cdb}dB, scene={cs}, fG={cfg}")
    print(f"  dev B0 FER={p_hat:.3f} (n_dev={len(dev_b0_fers)})")
    print(f"  H9 a-priori MDE_fer={mc.mde_fer} (NOT overwritten by power threshold)")
    print(f"  Power transparency: required n≈{n_required:.0f} for MDE={mc.mde_fer} at "
          f"power 0.8; actual n_test={len(mc.test_seeds)} "
          f"({'adequate' if len(mc.test_seeds) >= n_required else 'INSUFFICIENT — may yield EVIDENCE_INSUFFICIENT'})")

    with open(OUT / "p08r2_dev_workspace.json", "w") as f:
        json.dump({"metric_contract_frozen": mc.to_dict(),
                   "chosen_cell": list(chosen),
                   "dev_summary": {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v[0]
                                   for k, v in summary.items()},
                   "awgn_sanity": awgn_rows,
                   "metamorphic_gate_pass": mmg_pass,
                   "n_required_for_mde": float(n_required)}, f, indent=2, default=str)

    # --- Step 4: tune B1/B2 on dev_tune ---
    print("\n--- Step 4: tune B1/B2 on dev_tune ---")
    ab = scenes_dict[cs]
    tune_rows = []
    for T in mc.b1_temperature_grid:
        fers = []
        for seed in mc.dev_tune_seeds:
            real, eq, g = build_realization(mc, ab, contract, codec, prefix, seed, cs, cfg, cdb)
            us, _ = method_B1(real, eq, contract, codec, prefix, T)
            fers.append(score_trajectory(real, us, contract)["fer_traj"])
        tune_rows.append(("B1", T, float(np.mean(fers))))
    best_b1 = min(tune_rows, key=lambda x: x[2])
    print(f"  B1 best temperature={best_b1[1]} (dev_tune mean FER={best_b1[2]:.3f})")

    b2_rows = []
    for a in mc.b2_alpha_grid:
        for off in mc.b2_offset_grid:
            for clip in mc.b2_llr_clip_grid:
                fers = []
                for seed in mc.dev_tune_seeds:
                    real, eq, g = build_realization(mc, ab, contract, codec, prefix, seed, cs, cfg, cdb)
                    us, _ = method_B2(real, eq, contract, prefix, a, off, clip)
                    fers.append(score_trajectory(real, us, contract)["fer_traj"])
                b2_rows.append(("B2", (a, off, clip), float(np.mean(fers))))
    best_b2 = min(b2_rows, key=lambda x: x[2])
    print(f"  B2 best (alpha,offset,clip)={best_b2[1]} (dev_tune mean FER={best_b2[2]:.3f})")

    # --- Step 5: test on FRESH test seeds (paired, all methods same realization) ---
    print(f"\n--- Step 5: test on FRESH test seeds {mc.test_seeds[0]}-{mc.test_seeds[-1]} (paired) ---")
    test_rows = []
    for seed in mc.test_seeds:
        real, eq, g = build_realization(mc, ab, contract, codec, prefix, seed, cs, cfg, cdb)
        ev = trajectory_evidence(real, eq)
        for m, fn, kw in [
            ("B0", method_B0, {}),
            ("B1", method_B1, {"temperature": best_b1[1]}),
            ("B2", method_B2, {"alpha_d": best_b2[1][0], "offset_d": best_b2[1][1], "llr_clip_d": best_b2[1][2]}),
            ("O0", method_oracle, {"level": "O0", "o2_block": mc.o2_block}),
            ("O1", method_oracle, {"level": "O1", "o2_block": mc.o2_block}),
            ("O2", method_oracle, {"level": "O2", "o2_block": mc.o2_block}),
        ]:
            if m == "B0":
                us, sig = fn(real, eq, contract, codec, prefix)
            elif m == "B1":
                us, sig = fn(real, eq, contract, codec, prefix, **kw)
            elif m == "B2":
                us, sig = fn(real, eq, contract, prefix, **kw)
            else:
                us, sig = fn(real, eq, contract, codec, prefix, **kw)
            sc = score_trajectory(real, us, contract)
            test_rows.append({"method": m, "seed": seed, "scene": cs, "f_G": cfg,
                              "esn0_dB": cdb, **sc, **ev, **sig})
    with open(OUT / "p08r2_phaseA_raw_rows.json", "w") as f:
        json.dump(test_rows, f, indent=2, default=str)

    # --- Step 6: trajectory-cluster bootstrap CI (H9 fix: no min(B1,B2)) ---
    print("\n--- Step 6: trajectory-cluster bootstrap CI (H9: no min(B1,B2)) ---")
    def fers(method):
        return np.array([r["fer_traj"] for r in test_rows if r["method"] == method])
    B0 = fers("B0"); B1 = fers("B1"); B2 = fers("B2")
    O0 = fers("O0"); O1 = fers("O1"); O2 = fers("O2")
    # H9③ fix: report B0-B1 and B0-B2 SEPARATELY (no min(B1,B2) cherry-pick).
    # B2 is the single pre-registered conventional comparator.
    d_b0_b1 = B0 - B1
    d_b0_b2 = B0 - B2
    d_b2_o1 = B2 - O1
    d_b2_o2 = B2 - O2
    d_b0_o2 = B0 - O2

    def ci(d): return bootstrap_ci(d)
    results = {
        "n_test_traj": int(len(B0)),
        "mean_fer": {m: float(np.mean(fers(m))) for m in ("B0", "B1", "B2", "O0", "O1", "O2")},
        # separate deltas — NO post-hoc min(B1,B2)
        "delta_B0_minus_B1": ci(d_b0_b1),
        "delta_B0_minus_B2": ci(d_b0_b2),
        "delta_B2_minus_O1": ci(d_b2_o1),
        "delta_B2_minus_O2": ci(d_b2_o2),
        "delta_B0_minus_O2": ci(d_b0_o2),
    }
    print(f"  n_test_traj={results['n_test_traj']}")
    print(f"  mean FER: " + " ".join(f"{m}={results['mean_fer'][m]:.3f}" for m in ("B0", "B1", "B2", "O0", "O1", "O2")))
    for k in ("delta_B0_minus_B1", "delta_B0_minus_B2", "delta_B2_minus_O1",
              "delta_B2_minus_O2", "delta_B0_minus_O2"):
        m, lo, hi = results[k]
        hw = ci_half_width((m, lo, hi))
        print(f"  {k}: mean={m:+.4f} CI=[{lo:+.4f},{hi:+.4f}] hw={hw:.4f}")

    # --- Step 6b: mechanism decomposition ---
    print("\n--- Step 6b: mechanism decomposition (failure classes) ---")
    b0_by_seed = {s: [r for r in test_rows if r["method"] == "B0" and r["seed"] == s][0] for s in mc.test_seeds}
    o2_by_seed = {s: [r for r in test_rows if r["method"] == "O2" and r["seed"] == s][0] for s in mc.test_seeds}
    n_deep_b0 = sum(1 for s in mc.test_seeds if b0_by_seed[s]["n_cw_err_X"] + b0_by_seed[s]["n_cw_err_Y"] >= 2 * mc.n_cw_per_pol)
    n_deep_o2 = sum(1 for s in mc.test_seeds if o2_by_seed[s]["n_cw_err_X"] + o2_by_seed[s]["n_cw_err_Y"] >= 2 * mc.n_cw_per_pol)
    n_b0_success = sum(1 for s in mc.test_seeds if b0_by_seed[s]["fer_traj"] == 0.0)
    n_o2_rescues = sum(1 for s in mc.test_seeds if b0_by_seed[s]["fer_traj"] > 0 and o2_by_seed[s]["fer_traj"] < b0_by_seed[s]["fer_traj"])
    mech = {
        "n_test_traj": len(mc.test_seeds),
        "n_deep_fade_b0_allcw_fail": n_deep_b0,
        "n_deep_fade_o2_allcw_fail": n_deep_o2,
        "n_b0_full_success": n_b0_success,
        "n_o2_partial_rescue_vs_b0": n_o2_rescues,
    }
    print(f"  B0 all-cw-fail (deep burst): {n_deep_b0}/{mech['n_test_traj']}")
    print(f"  O2 ALSO all-cw-fail (unrecoverable): {n_deep_o2}/{mech['n_test_traj']}")
    print(f"  B0 full success: {n_b0_success}/{mech['n_test_traj']}")
    print(f"  O2 partially rescues a B0-failed traj: {n_o2_rescues}/{mech['n_test_traj']}")
    results["mechanism_decomposition"] = mech

    # --- Step 7: terminal verdict (H9 fix: EVIDENCE_INSUFFICIENT state) ---
    print("\n--- Step 7: terminal verdict (H9: a-priori MDE, EVIDENCE_INSUFFICIENT) ---")
    if exec_invalid:
        verdict = "EXECUTION_INVALID"
    else:
        # Use B2 (pre-registered comparator) and O2 (finest oracle) for headroom.
        conv = B2  # NOT min(B1,B2)
        mde = mc.mde_fer
        # CI half-widths (B0-conv headroom and conv-O2 oracle headroom)
        ci_b0_conv = results["delta_B0_minus_B2"]
        ci_conv_o2 = results["delta_B2_minus_O2"]
        hw_b0_conv = ci_half_width(ci_b0_conv)
        hw_conv_o2 = ci_half_width(ci_conv_o2)
        # evidence_sufficient: CI narrow enough to decide (hw ≤ MDE/2)
        ev_sufficient = (hw_b0_conv <= mde / 2) and (hw_conv_o2 <= mde / 2)
        # conv_helps: B2 strictly beats B0 by ≥ MDE with CI_lo > 0
        conv_helps = (ci_b0_conv[0] > mde) and (ci_b0_conv[1] > 0)
        # oracle headroom: O2 strictly beats conv by ≥ MDE with CI_lo > 0
        oracle_headroom = (ci_conv_o2[0] > mde) and (ci_conv_o2[1] > 0)
        print(f"  mde(a-priori)={mde:.4f}")
        print(f"  CI_hw B0-B2={hw_b0_conv:.4f} (≤mde/2={mde/2:.4f}? {hw_b0_conv <= mde/2})")
        print(f"  CI_hw B2-O2={hw_conv_o2:.4f} (≤mde/2={mde/2:.4f}? {hw_conv_o2 <= mde/2})")
        print(f"  evidence_sufficient={ev_sufficient}")
        print(f"  conv_helps(B0-B2>mde & CI_lo>0): {conv_helps}")
        print(f"  oracle_headroom(B2-O2>mde & CI_lo>0): {oracle_headroom}")
        if not ev_sufficient:
            verdict = "EVIDENCE_INSUFFICIENT"
        elif conv_helps and not oracle_headroom:
            verdict = "PROBLEM_RESOLVED_BY_LLR_CLIP_AND_DECODER_TUNING"
        elif not oracle_headroom:
            verdict = "PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE"
        else:
            verdict = "PROBLEM_SURVIVES_CONVENTIONAL_BASELINE_PROCEED_TO_BC"
    print(f"\n  >>> VERDICT: {verdict}")

    _save_final(mc, verdict, best_b1, best_b2, results, awgn_rows, [], t0,
                exec_invalid=exec_invalid, mmg_pass=mmg_pass)


def _save_final(mc, verdict, best_b1, best_b2, results, awgn_rows, dev_rows,
                t0, exec_invalid=False, mmg_pass=True):
    final = {
        "metric_contract_frozen": mc.to_dict(),
        "best_b1": ({"temperature": best_b1[1], "dev_tune_fer": best_b1[2]}
                    if best_b1 is not None else None),
        "best_b2": ({"alpha_offset_clip": best_b2[1], "dev_tune_fer": best_b2[2]}
                    if best_b2 is not None else None),
        "chosen_cell": list(mc.chosen_cell) if mc.chosen_cell else None,
        "test_results": results,
        "awgn_sanity": awgn_rows,
        "metamorphic_gate_pass": mmg_pass,
        "exec_invalid": exec_invalid,
        "terminal_verdict": verdict,
        "elapsed_sec": round(time.time() - t0, 1),
    }
    with open(OUT / "p08r2_phaseA_gate.json", "w") as f:
        json.dump(final, f, indent=2, default=str)
    print(f"\nDone in {final['elapsed_sec']}s. Artifacts in {OUT}")


if __name__ == "__main__":
    main()
