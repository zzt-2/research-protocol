"""P08-R Phase A orchestrator — dev workspace → freeze metric → test → verdict.

Execution order (H4): (1) AWGN B0 sanity (EXECUTION_INVALID gate), (2) dev workspace
scan with B0 to find achievable SNR/FER region, (3) freeze metric (Primary A or B)
BEFORE reading test, (4) tune B1/B2 on dev_tune, (5) test on fresh test_seeds,
(6) bootstrap CI on trajectory-cluster deltas, (7) terminal verdict per §9 A-D.

Statistical unit = trajectory/seed (H6). No early stopping. CI half-width too wide
⇒ evidence_insufficient (not absent).
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

from p08r_chain import (  # noqa: E402
    get_gg_scenes, CodedContractR, CodecAdapterR, CalibrationPrefix,
    CodedRealizationR, split_prefix_data, estimate_sigma2_from_prefix,
)
from p08r_phaseA import (  # noqa: E402
    MetricContractR, bootstrap_ci, method_B0, method_B1, method_B2,
    method_oracle, score_trajectory, trajectory_evidence, llr_per_cw_from_eq,
)
from p08_coded_chain import maxlog_soft_demap_16qam  # noqa: E402


def build_realization(mc: MetricContractR, scene_ab, contract, codec, prefix,
                      seed, scene, f_g, snr_db):
    g = float(10 ** (snr_db / 10.0))
    real = CodedRealizationR(
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
                   scenes, f_Gs, methods=("B0", "O1", "O2"), verbose=True):
    """Scan a (seed × scene × fG × SNR × method) grid. Returns raw rows."""
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
                        row = {"method": m, "seed": seed, "scene": scene, "f_G": f_g,
                               "esn0_dB": db, **sc, **ev, **sig}
                        rows.append(row)
                    if verbose:
                        last = rows[-1]
                        print(f"  seed={seed} {scene} fG={f_g} {db}dB: "
                              f"B0 fer_traj={rows[-3]['fer_traj']:.3f} "
                              f"O1={rows[-2]['fer_traj']:.3f} O2={rows[-1]['fer_traj']:.3f}")
    return rows


def main():
    out_dir = Path(__file__).resolve().parents[2] / "results" / "p08r_coded_chain_repair"
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    mc = MetricContractR()
    scenes_dict = get_gg_scenes()
    contract = CodedContractR()
    codec = CodecAdapterR(contract)
    prefix = CalibrationPrefix(n_prefix_symbols=mc.n_prefix_symbols)

    print("=" * 70)
    print("P08-R Phase A — H1-H6 repaired chain")
    print("=" * 70)
    print(f"H1 GG scenes (from params): weak={scenes_dict['weak']} "
          f"moderate={scenes_dict['moderate']} strong={scenes_dict['strong']}")
    print(f"H5 interleaver out_int active: {codec.out_int is not None}, "
          f"n_moved={int((codec.out_int != np.arange(contract.n)).sum())}/{contract.n}")
    print(f"H2 prefix: {mc.n_prefix_symbols} known symbols, shared by all methods")
    print(f"H6 cluster unit: trajectory/seed; n_cw/pol={mc.n_cw_per_pol}")

    # --- Step 1: AWGN B0 sanity (EXECUTION_INVALID gate) ---
    print("\n--- Step 1: AWGN B0 sanity (EXECUTION_INVALID gate) ---")
    awgn_rows = []
    for db in (8.0, 10.0, 12.0):
        # AWGN = weak scene is closest to AWGN at high SNR; use weak + fG=100
        real, eq, g = build_realization(mc, scenes_dict["weak"], contract, codec, prefix,
                                        seed=599999, scene="weak", f_g=100.0, snr_db=db)
        us, _ = method_B0(real, eq, contract, codec, prefix)
        sc = score_trajectory(real, us, contract)
        awgn_rows.append({"esn0_dB": db, **sc})
        print(f"  AWGN-ish (weak,fG100) {db}dB: fer_traj={sc['fer_traj']:.3f}")
    exec_invalid = awgn_rows[-1]["fer_traj"] > 0.5  # at 12dB weak must decode
    print(f"  EXECUTION_INVALID? {exec_invalid}")

    # --- Step 2: dev workspace scan (B0, O1, O2) to find achievable region ---
    print("\n--- Step 2: dev workspace scan (B0/O1/O2) ---")
    dev_rows = scan_workspace(mc, scenes_dict, contract, codec, prefix,
                              seeds=mc.dev_seeds, snr_grid=mc.dev_snr_dB,
                              scenes=mc.scenes, f_Gs=mc.f_G_Hz, methods=("B0", "O1", "O2"),
                              verbose=False)
    # summarize: per (scene, fG, SNR, method) mean trajectory FER
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

    print("\nDev mean trajectory FER (B0 / O1 / O2):")
    print(f"{'scene':<10}{'fG':>6}{'SNR':>6}  {'B0':>7}{'O1':>7}{'O2':>7}  {'O2-B0':>7}")
    for scene in mc.scenes:
        for f_g in mc.f_G_Hz:
            for db in mc.dev_snr_dB:
                b0 = summary.get((scene, f_g, db, "B0"), (float('nan'),0))[0]
                o1 = summary.get((scene, f_g, db, "O1"), (float('nan'),0))[0]
                o2 = summary.get((scene, f_g, db, "O2"), (float('nan'),0))[0]
                print(f"{scene:<10}{f_g:>6.0f}{db:>6.0f}  {b0:>7.3f}{o1:>7.3f}{o2:>7.3f}  {o2-b0:>+7.3f}")

    # --- Step 3: freeze metric BEFORE reading test ---
    print("\n--- Step 3: freeze metric (H4) BEFORE reading test ---")
    # Decision rule (pre-registered): prefer a cell where B0 FER is in the
    # OPERATING REGION [0.1, 0.3] (realistic coded operating point, gives
    # well-powered test). Among those, pick the cell with the LARGEST oracle
    # headroom (O2-B0) on dev — the most favorable to detecting a calibration
    # effect. If no [0.1,0.3] cell exists, fall back to [0.15,0.5].
    def pick_cell(lo, hi):
        cands = []
        for scene in mc.scenes:
            for f_g in mc.f_G_Hz:
                for db in mc.dev_snr_dB:
                    b0 = summary.get((scene, f_g, db, "B0"), (None,0))[0]
                    o2 = summary.get((scene, f_g, db, "O2"), (None,0))[0]
                    if b0 is not None and lo <= b0 <= hi and o2 is not None:
                        cands.append((b0 - o2, scene, f_g, db, b0, o2))
        if not cands:
            return None
        cands.sort(reverse=True)  # largest headroom first
        return cands[0]

    pick = pick_cell(0.1, 0.3) or pick_cell(0.15, 0.5)
    if pick is None:
        # last resort: any cell with B0 in [0.05, 0.7]
        pick = pick_cell(0.05, 0.7)
    if pick is None:
        chosen = None
    else:
        _, cs, cfg, cdb, _, _ = pick
        chosen = (cs, cfg, cdb)
    # freeze MDE_fer from dev event rate at chosen cell
    if chosen:
        cs, cfg, cdb = chosen
        dev_b0_fers = [r["fer_traj"] for r in dev_rows if r["scene"] == cs and r["f_G"] == cfg
                       and abs(r["esn0_dB"]-cdb) < 1e-9 and r["method"] == "B0"]
        p_hat = float(np.mean(dev_b0_fers)) if dev_b0_fers else 0.2
        n_dev = len(dev_b0_fers)
        # MDE for paired FER delta at power 0.8, two-sided alpha 0.05:
        # need |delta| > z_{0.975}+z_{0.8} * sqrt(2*p*(1-p)/n) ≈ 2.802 * sd
        n_test = len(mc.test_seeds)
        mde_fer_est = 2.802 * np.sqrt(2 * p_hat * (1 - p_hat) / max(n_test, 1))
        mc.primary_metric_choice = "B_fixed_snr_paired_fer"
        mc.fixed_snr_dB_primaryB = (cdb,)
        mc.mde_fer = float(mde_fer_est)
        print(f"  Frozen: Primary B at fixed SNR={cdb}dB, scene={cs}, fG={cfg}")
        print(f"  dev B0 FER={p_hat:.3f} (n={n_dev}); MDE_fer frozen={mc.mde_fer:.4f} (n_test={n_test}, power 0.8)")
        print(f"  rationale: operating region [0.1,0.3] preferred for well-powered test")
    else:
        mc.primary_metric_choice = "B_fixed_snr_paired_fer"
        mc.fixed_snr_dB_primaryB = (mc.dev_snr_dB[len(mc.dev_snr_dB)//2],)
        mc.mde_fer = 0.05
        print(f"  No shoulder cell found; freeze Primary B at SNR={mc.fixed_snr_dB_primaryB}")

    # save dev workspace + frozen metric
    with open(out_dir / "p08r_dev_workspace.json", "w") as f:
        json.dump({"metric_contract_frozen": mc.to_dict(),
                   "chosen_cell": list(chosen) if chosen else None,
                   "dev_summary": {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}": v[0]
                                   for k, v in summary.items()},
                   "awgn_sanity": awgn_rows}, f, indent=2, default=str)

    # --- Step 4: tune B1/B2 on dev_tune ---
    print("\n--- Step 4: tune B1/B2 on dev_tune ---")
    if chosen:
        cs, cfg, cdb = chosen
    else:
        cs, cfg, cdb = mc.scenes[1], mc.f_G_Hz[0], mc.fixed_snr_dB_primaryB[0]
    tune_rows = []
    ab = scenes_dict[cs]
    for T in mc.b1_temperature_grid:
        fers = []
        for seed in mc.dev_tune_seeds:
            real, eq, g = build_realization(mc, ab, contract, codec, prefix, seed, cs, cfg, cdb)
            us, _ = method_B1(real, eq, contract, codec, prefix, T)
            sc = score_trajectory(real, us, contract)
            fers.append(sc["fer_traj"])
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
                    sc = score_trajectory(real, us, contract)
                    fers.append(sc["fer_traj"])
                b2_rows.append(("B2", (a, off, clip), float(np.mean(fers))))
    best_b2 = min(b2_rows, key=lambda x: x[2])
    print(f"  B2 best (alpha,offset,clip)={best_b2[1]} (dev_tune mean FER={best_b2[2]:.3f})")

    # --- Step 5: test on fresh test_seeds (paired, all methods same realization) ---
    print("\n--- Step 5: test on fresh test_seeds (paired) ---")
    test_rows = []
    for seed in mc.test_seeds:
        real, eq, g = build_realization(mc, ab, contract, codec, prefix, seed, cs, cfg, cdb)
        ev = trajectory_evidence(real, eq)
        # B0, B1 (frozen T), B2 (frozen tuple), O0, O1, O2 — all on SAME realization
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
    with open(out_dir / "p08r_phaseA_raw_rows.json", "w") as f:
        json.dump(test_rows, f, indent=2, default=str)

    # --- Step 6: trajectory-cluster bootstrap CI ---
    print("\n--- Step 6: trajectory-cluster bootstrap CI ---")
    def fers(method):
        return np.array([r["fer_traj"] for r in test_rows if r["method"] == method])
    B0 = fers("B0"); B1 = fers("B1"); B2 = fers("B2")
    O0 = fers("O0"); O1 = fers("O1"); O2 = fers("O2")
    strongest_conv = np.minimum(B1, B2)  # best of B1/B2 per trajectory
    # paired deltas (per trajectory)
    d_b0_conv = B0 - strongest_conv
    d_conv_o0 = strongest_conv - O0
    d_conv_o1 = strongest_conv - O1
    d_conv_o2 = strongest_conv - O2
    d_b0_o2 = B0 - O2

    def ci(d): return bootstrap_ci(d)
    results = {
        "n_test_traj": int(len(B0)),
        "mean_fer": {m: float(np.mean(fers(m))) for m in ("B0","B1","B2","O0","O1","O2")},
        "delta_B0_minus_strongest_conv": ci(d_b0_conv),
        "delta_strongest_conv_minus_O0": ci(d_conv_o0),
        "delta_strongest_conv_minus_O1": ci(d_conv_o1),
        "delta_strongest_conv_minus_O2": ci(d_conv_o2),
        "delta_B0_minus_O2": ci(d_b0_o2),
    }
    print(f"  n_test_traj={results['n_test_traj']}")
    print(f"  mean FER: " + " ".join(f"{m}={results['mean_fer'][m]:.3f}" for m in ("B0","B1","B2","O0","O1","O2")))
    for k in ("delta_B0_minus_strongest_conv","delta_strongest_conv_minus_O0",
              "delta_strongest_conv_minus_O1","delta_strongest_conv_minus_O2","delta_B0_minus_O2"):
        m, lo, hi = results[k]
        print(f"  {k}: mean={m:+.4f} CI=[{lo:+.4f},{hi:+.4f}]")

    # --- Step 6b: mechanism decomposition (§9 step 1: failure-class analysis) ---
    print("\n--- Step 6b: mechanism decomposition (failure classes) ---")
    # Per trajectory, classify B0 failure: all-cw (16/16) = deep-fade burst,
    # partial = some cw survive, none = success. Same for O2 (does local truth save any?).
    b0_by_seed = {s: [r for r in test_rows if r["method"]=="B0" and r["seed"]==s][0] for s in mc.test_seeds}
    o2_by_seed = {s: [r for r in test_rows if r["method"]=="O2" and r["seed"]==s][0] for s in mc.test_seeds}
    n_deep_b0 = sum(1 for s in mc.test_seeds if b0_by_seed[s]["n_cw_err_X"]+b0_by_seed[s]["n_cw_err_Y"] >= 2*mc.n_cw_per_pol)
    n_deep_o2 = sum(1 for s in mc.test_seeds if o2_by_seed[s]["n_cw_err_X"]+o2_by_seed[s]["n_cw_err_Y"] >= 2*mc.n_cw_per_pol)
    n_b0_success = sum(1 for s in mc.test_seeds if b0_by_seed[s]["fer_traj"] == 0.0)
    n_o2_rescues_b0fail = sum(1 for s in mc.test_seeds if b0_by_seed[s]["fer_traj"]>0 and o2_by_seed[s]["fer_traj"]<b0_by_seed[s]["fer_traj"])
    n_o2_full_rescue = sum(1 for s in mc.test_seeds if b0_by_seed[s]["fer_traj"]>0 and o2_by_seed[s]["fer_traj"]==0.0)
    mech = {
        "n_test_traj": len(mc.test_seeds),
        "n_deep_fade_b0_allcw_fail": n_deep_b0,           # both pols all cw fail
        "n_deep_fade_o2_allcw_fail": n_deep_o2,           # O2 also fails all (unrecoverable)
        "n_b0_full_success": n_b0_success,
        "n_o2_partial_rescue_vs_b0": n_o2_rescues_b0fail,  # O2 < B0 on trajectories where B0 failed
        "n_o2_full_rescue": n_o2_full_rescue,              # O2 fully recovers a B0-failed trajectory
    }
    print(f"  trajectories where B0 all-cw-fail (deep burst): {n_deep_b0}/{mech['n_test_traj']}")
    print(f"  trajectories where O2 ALSO all-cw-fail (unrecoverable): {n_deep_o2}/{mech['n_test_traj']}")
    print(f"  B0 full success: {n_b0_success}/{mech['n_test_traj']}")
    print(f"  O2 partially rescues a B0-failed traj: {n_o2_rescues_b0fail}/{mech['n_test_traj']}")
    print(f"  O2 fully rescues a B0-failed traj: {n_o2_full_rescue}/{mech['n_test_traj']}")
    results["mechanism_decomposition"] = mech

    # --- Step 7: terminal verdict (§9 A-D) ---
    print("\n--- Step 7: terminal verdict (§9 A-D) ---")
    if exec_invalid:
        verdict = "EXECUTION_INVALID"
    else:
        conv_helps = results["delta_B0_minus_strongest_conv"][0] > mc.mde_fer and \
                     results["delta_B0_minus_strongest_conv"][1] > 0
        o1_headroom = results["delta_strongest_conv_minus_O1"][0] > mc.mde_fer and \
                      results["delta_strongest_conv_minus_O1"][1] > 0
        o2_headroom = results["delta_strongest_conv_minus_O2"][0] > mc.mde_fer and \
                      results["delta_strongest_conv_minus_O2"][1] > 0
        oracle_headroom = o1_headroom or o2_headroom
        print(f"  conv_helps(B0-conv>{mc.mde_fer:.4f} & CI_lo>0): {conv_helps}")
        print(f"  O1 headroom(>{mc.mde_fer:.4f} & CI_lo>0): {o1_headroom}")
        print(f"  O2 headroom(>{mc.mde_fer:.4f} & CI_lo>0): {o2_headroom}")
        if conv_helps and not oracle_headroom:
            verdict = "PROBLEM_RESOLVED_BY_TEMPERATURE_AND_DECODER_TUNING"
        elif not oracle_headroom:
            verdict = "PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE"
        else:
            verdict = "PROBLEM_SURVIVES_CONVENTIONAL_BASELINE_PROCEED_TO_BC"
    print(f"\n  >>> VERDICT: {verdict}")

    final = {"metric_contract_frozen": mc.to_dict(),
             "best_b1": {"temperature": best_b1[1], "dev_tune_fer": best_b1[2]},
             "best_b2": {"alpha_offset_clip": best_b2[1], "dev_tune_fer": best_b2[2]},
             "chosen_cell": list(chosen) if chosen else None,
             "test_results": results,
             "awgn_sanity": awgn_rows,
             "exec_invalid": exec_invalid,
             "terminal_verdict": verdict,
             "elapsed_sec": round(time.time() - t0, 1)}
    with open(out_dir / "p08r_phaseA_gate.json", "w") as f:
        json.dump(final, f, indent=2, default=str)
    print(f"\nDone in {final['elapsed_sec']}s. Artifacts in {out_dir}")


if __name__ == "__main__":
    main()
