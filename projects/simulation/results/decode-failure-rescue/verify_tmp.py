"""Independent re-verification of confirm_W12 / confirm_S16 (verify_tmp).

Read-only: recomputes every headline number from raw_confirm_*.json and the
llr_cache npz files; never writes raw/summary/npz.

Checks:
  A  counts + paired stats from raw, zero-deviation vs summary
  B  re-decode 3 frames per condition via run_confirm.run_one_frame
  C  data-level unified-output-rule consistency across ALL frames
     (trigger == own stage-1 syndrome!=0, accepted == stage-2 syndrome==0,
      final source selection) -- code review reported separately
  D  seed isolation (sets + historical blocks)
  E  shared inputs (raw vs npz llr_sha256, snr/turbulence params, manifest)
  F  composition band table from npz llr + truth_coded
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent          # results/decode-failure-rescue
EXPLORE = (HERE / ".." / ".." / "explore" / "decode-failure-rescue").resolve()
sys.path.insert(0, str(EXPLORE))

CONDITIONS = {
    "confirm_W12": dict(
        cache="confirm_W12_snr12_turb11.6x10.1", snr_db=12.0,
        turb_alpha=11.6, turb_beta=10.1, seeds=set(range(50000, 52048))),
    "confirm_S16": dict(
        cache="confirm_S16_snr16_turb4.2x1.4", snr_db=16.0,
        turb_alpha=4.2, turb_beta=1.4, seeds=set(range(53000, 55048))),
}
HIST_BLOCKS = [(0, 64), (2000, 2064), (2900, 2908), (3000, 3064), (4000, 4512),
               (5000, 5064), (6000, 6020), (7000, 7040), (8000, 8040),
               (9000, 9020), (10000, 10100), (130000, 140000), (30000, 32048),
               (40000, 40512), (41000, 41512), (42000, 42512), (43000, 43512)]
BANDS = [(0, 100), (100, 140), (140, 160), (160, 220), (220, 320), (320, 10**9)]
ARMS = ("B0", "R1", "R3", "F")

CHECKS: list[tuple[str, bool, str]] = []


def record_check(name: str, ok: bool, evidence: str) -> None:
    CHECKS.append((name, bool(ok), evidence))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {evidence}", flush=True)


def final_of(rec: dict, arm: str) -> dict:
    if arm == "B0":
        return {"info_errors": rec["B0"]["info_errors"],
                "final_syndrome": rec["B0"]["final_syndrome"]}
    return rec["arms"][arm]["final"]


def exact_binom_2sided(wins: int, losses: int) -> tuple[float, float]:
    d = wins + losses
    if d == 0:
        return 1.0, 1.0
    lo = min(wins, losses)
    tail = sum(math.comb(d, i) for i in range(0, lo + 1)) / 2 ** d
    return min(1.0, 2 * tail), tail


def bootstrap_ci(a: np.ndarray, b: np.ndarray, *, resamples=10000,
                 seed=20260921) -> list[float]:
    n = len(a)
    rng = np.random.default_rng(seed)
    diffs = np.empty(resamples)
    for k in range(resamples):
        idx = rng.integers(0, n, size=n)
        diffs[k] = a[idx].mean() - b[idx].mean()
    return [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]


def paired_from_raw(records: list[dict], arm_a: str, arm_b: str,
                    with_ci: bool = True) -> dict:
    a = np.array([1 if final_of(r, arm_a)["info_errors"] > 0 else 0
                  for r in records])
    b = np.array([1 if final_of(r, arm_b)["info_errors"] > 0 else 0
                  for r in records])
    wins = int(np.sum((a == 0) & (b == 1)))
    losses = int(np.sum((a == 1) & (b == 0)))
    p2, p1 = exact_binom_2sided(wins, losses)
    out = {"wins_a": wins, "losses_a": losses, "discordant": wins + losses,
           "point_estimate": float(a.mean() - b.mean()),
           "exact_two_sided_p": p2, "exact_one_sided_p": p1}
    if with_ci:
        out["ci95"] = bootstrap_ci(a, b)
    return out


def load_npz_condition(cache: str) -> dict[int, dict]:
    frames = {}
    for path in sorted((HERE / "llr_cache" / cache).glob("frame_*.npz")):
        with np.load(path) as d:
            frames[int(d["seed"])] = {
                "path": path.name,
                "llr": d["llr"].astype(np.float32),
                "truth_info": d["truth_info"].astype(np.uint8),
                "truth_coded": d["truth_coded"].astype(np.uint8),
                "llr_sha256": str(d["llr_sha256"]),
                "snr_db": float(d["snr_db"]),
                "turbulence_alpha": float(d["turbulence_alpha"]),
                "turbulence_beta": float(d["turbulence_beta"]),
                "turbulence_alpha_manifest": float(d["turbulence_alpha_manifest"]),
                "turbulence_beta_manifest": float(d["turbulence_beta_manifest"]),
            }
    return frames


def array_sha256(array: np.ndarray) -> str:
    arr = np.ascontiguousarray(array)
    dig = hashlib.sha256()
    dig.update(str(arr.shape).encode("ascii"))
    dig.update(arr.dtype.str.encode("ascii"))
    dig.update(arr.tobytes())
    return dig.hexdigest()


def fmt(x) -> str:
    return f"{x:.10g}" if isinstance(x, float) else str(x)


# ====================================================================== #
def main() -> None:
    raw, summary, npz = {}, {}, {}
    for tag in CONDITIONS:
        raw[tag] = json.loads((HERE / f"raw_{tag}.json").read_text(encoding="utf-8"))
        raw[tag]["frames"].sort(key=lambda r: r["seed"])
        summary[tag] = json.loads((HERE / f"summary_{tag}.json").read_text(encoding="utf-8"))
        npz[tag] = load_npz_condition(CONDITIONS[tag]["cache"])

    # ---------------- A: counts + paired ------------------------------- #
    for tag in CONDITIONS:
        frames = raw[tag]["frames"]
        n = len(frames)
        assert n == 2048, f"{tag}: {n} frames"
        mine = {}
        for arm in ARMS:
            ie = [final_of(r, arm)["info_errors"] for r in frames]
            mine[arm] = (sum(1 for e in ie if e > 0), sum(ie))
        pa = {f"{a}_vs_{b}": paired_from_raw(frames, a, b)
              for a, b in (("R3", "R1"), ("F", "R1"), ("R3", "F"))}
        # extra: paired BER diff R3 vs R1
        ea = np.array([final_of(r, "R3")["info_errors"] for r in frames])
        eb = np.array([final_of(r, "R1")["info_errors"] for r in frames])
        ber_ci = bootstrap_ci(ea, eb)
        ber = {"point_bit_diff": int(ea.sum() - eb.sum()),
               "point_ber_diff": float(ea.mean() - eb.mean()) / 1024,
               "ci95_ber_diff": [ber_ci[0] / 1024, ber_ci[1] / 1024]}

        # compare vs summary
        diffs = []
        for arm in ARMS:
            s = summary[tag]["arms"][arm]
            if s["info_error_frames"] != mine[arm][0]:
                diffs.append(f"arms.{arm}.info_error_frames {s['info_error_frames']}!={mine[arm][0]}")
            if s["bit_errors"] != mine[arm][1]:
                diffs.append(f"arms.{arm}.bit_errors {s['bit_errors']}!={mine[arm][1]}")
        counts_str = " ".join(f"{a}={mine[a][0]}fr/{mine[a][1]}bit" for a in ARMS)
        record_check(f"A4 counts {tag}", not diffs,
                     f"{counts_str}" + ("; " + "; ".join(diffs) if diffs else "; zero deviation vs summary"))

        pdiffs = []
        for key, val in pa.items():
            s = summary[tag]["paired"][key]
            for f in ("wins_a", "losses_a", "discordant", "point_estimate",
                      "exact_two_sided_p", "exact_one_sided_p", "ci95"):
                if s[f] != val[f]:
                    pdiffs.append(f"paired.{key}.{f} {s[f]}!={val[f]}")
        # F1_vs_B0 stage-1-only pairing
        a1 = np.array([1 if r["F1"]["info_errors"] > 0 else 0 for r in frames])
        b1 = np.array([1 if r["B0"]["info_errors"] > 0 else 0 for r in frames])
        w, l = int(np.sum((a1 == 0) & (b1 == 1))), int(np.sum((a1 == 1) & (b1 == 0)))
        p2, p1 = exact_binom_2sided(w, l)
        s = summary[tag]["paired"]["F1_vs_B0_stage1only"]
        for fname, mval in (("wins_a", w), ("losses_a", l), ("discordant", w + l),
                            ("point_estimate", float(a1.mean() - b1.mean())),
                            ("exact_two_sided_p", p2), ("exact_one_sided_p", p1)):
            if s[fname] != mval:
                pdiffs.append(f"paired.F1_vs_B0_stage1only.{fname} {s[fname]}!={mval}")
        sb = summary[tag]["paired_ber_R3_vs_R1"]
        for fname, mval in ber.items():
            if sb[fname] != mval:
                pdiffs.append(f"paired_ber.{fname} {sb[fname]}!={mval}")
        r31 = pa["R3_vs_R1"]
        record_check(
            f"A2/A3/A4 paired {tag}", not pdiffs,
            f"R3_vs_R1 w/l={r31['wins_a']}/{r31['losses_a']} p={fmt(r31['exact_two_sided_p'])}; "
            f"R3_vs_F w/l={pa['R3_vs_F']['wins_a']}/{pa['R3_vs_F']['losses_a']} "
            f"p={fmt(pa['R3_vs_F']['exact_two_sided_p'])}; "
            f"F_vs_R1 w/l={pa['F_vs_R1']['wins_a']}/{pa['F_vs_R1']['losses_a']} "
            f"p={fmt(pa['F_vs_R1']['exact_two_sided_p'])}"
            + ("; " + "; ".join(pdiffs) if pdiffs else "; zero deviation vs summary (incl. ci95, ber pairing)"))

        # A5 accepted_but_wrong
        abw = {}
        for arm in ARMS:
            abw[arm] = sum(1 for r in frames
                           if final_of(r, arm)["final_syndrome"] == 0
                           and final_of(r, arm)["info_errors"] > 0)
        record_check(f"A5 accepted_but_wrong {tag}", all(v == 0 for v in abw.values()),
                     f"per-arm final(synd==0 & err>0): {abw} (summary: "
                     f"{ {a: summary[tag]['arms'][a]['accepted_but_wrong_frames'] for a in ARMS} })")

        # ---------------- C: unified rule, data level ------------------- #
        viol = []
        for r in frames:
            b0, f1 = r["B0"], r["F1"]
            for arm, stage1 in (("R1", b0), ("R3", b0), ("F", f1)):
                a = r["arms"][arm]
                if a["trigger"] != (stage1["final_syndrome"] != 0):
                    viol.append(f"seed {r['seed']} {arm}: trigger != stage1 synd")
                if (a["stage2"] is None) != (not a["trigger"]):
                    viol.append(f"seed {r['seed']} {arm}: stage2 presence")
                if a["trigger"]:
                    if a["stage2"]["accepted"] != (a["stage2"]["final_syndrome"] == 0):
                        viol.append(f"seed {r['seed']} {arm}: accepted != s2 synd==0")
                    if a["stage2"]["accepted"]:
                        if (a["final"]["source"] != "stage2"
                                or a["final"]["final_syndrome"] != 0
                                or a["final"]["info_errors"] != a["stage2"]["stage2_info_errors"]):
                            viol.append(f"seed {r['seed']} {arm}: accepted final != stage2")
                    else:
                        if (a["final"]["source"] != "stage1_fallback"
                                or a["final"]["final_syndrome"] != stage1["final_syndrome"]
                                or a["final"]["info_errors"] != stage1["info_errors"]):
                            viol.append(f"seed {r['seed']} {arm}: fallback final != stage1")
                else:
                    if (a["final"]["source"] != "stage1_not_triggered"
                            or a["final"]["final_syndrome"] != stage1["final_syndrome"]
                            or a["final"]["info_errors"] != stage1["info_errors"]):
                        viol.append(f"seed {r['seed']} {arm}: not-triggered final != stage1")
        record_check(f"C unified-rule consistency {tag}", not viol,
                     f"2048 frames x 3 arms: trigger==own-stage1-syndrome!=0, "
                     f"accepted==stage2-syndrome==0, final selection coherent"
                     + (f"; {len(viol)} violations, first: {viol[0]}" if viol else "; 0 violations"))

    # ---------------- B: re-decode 3 frames per condition -------------- #
    from rescue_decoder import RescueDecoder, make_encoder  # noqa: E402
    from run_confirm import run_one_frame                    # noqa: E402
    decoder = RescueDecoder(make_encoder())
    for tag in CONDITIONS:
        frames = raw[tag]["frames"]
        picks = {}
        for r in frames:  # sorted by seed
            a = r["arms"]["R1"]
            if "trig_acc" not in picks and a["trigger"] and a["stage2"] and a["stage2"]["accepted"]:
                picks["trig_acc"] = r["seed"]
            if "trig_rej" not in picks and a["trigger"] and a["stage2"] and not a["stage2"]["accepted"]:
                picks["trig_rej"] = r["seed"]
            if "no_trig" not in picks and not a["trigger"]:
                picks["no_trig"] = r["seed"]
            if len(picks) == 3:
                break
        assert len(picks) == 3, f"{tag}: could not pick 3 frames: {picks}"
        mism = []
        for role, seed in picks.items():
            rec_raw = next(r for r in frames if r["seed"] == seed)
            d = npz[tag][seed]
            frame = {"seed": seed, "frame_index": rec_raw["frame_index"],
                     "llr": d["llr"], "truth_info": d["truth_info"],
                     "truth_coded": d["truth_coded"], "llr_sha256": d["llr_sha256"]}
            redo = run_one_frame(decoder, frame)
            for arm in ARMS[1:]:
                g, m = redo["arms"][arm], rec_raw["arms"][arm]
                for f in ("trigger",):
                    if g[f] != m[f]:
                        mism.append(f"seed{seed}/{arm}.{f} {g[f]}!={m[f]}")
                for f in ("accepted", "final_syndrome", "iterations_run", "stage2_info_errors"):
                    if (g["stage2"] or {}).get(f) != (m["stage2"] or {}).get(f):
                        mism.append(f"seed{seed}/{arm}.stage2.{f} "
                                    f"{(g['stage2'] or {}).get(f)}!={(m['stage2'] or {}).get(f)}")
                for f in ("info_errors", "final_syndrome", "source"):
                    if g["final"][f] != m["final"][f]:
                        mism.append(f"seed{seed}/{arm}.final.{f} {g['final'][f]}!={m['final'][f]}")
            for st in ("B0", "F1"):
                for f in ("info_errors", "final_syndrome", "converged_at"):
                    if redo[st][f] != rec_raw[st][f]:
                        mism.append(f"seed{seed}/{st}.{f} {redo[st][f]}!={rec_raw[st][f]}")
            if json.dumps(redo["B0"]["syndrome_weights"]) != json.dumps(rec_raw["B0"]["syndrome_weights"]):
                mism.append(f"seed{seed}/B0.syndrome_weights differ")
        record_check(f"B re-decode {tag}", not mism,
                     f"3 frames re-decoded from cached llr (trig+acc seed {picks['trig_acc']}, "
                     f"trig+rej seed {picks['trig_rej']}, no-trig seed {picks['no_trig']}): "
                     "trigger/accepted/final.info_errors/source all identical"
                     + (f"; {len(mism)} field mismatches, first: {mism[0]}" if mism else ""))

    # ---------------- D: seed isolation -------------------------------- #
    for tag in CONDITIONS:
        seeds = set(npz[tag])
        exp = CONDITIONS[tag]["seeds"]
        ok_set = seeds == exp
        n_files = len(npz[tag])
        record_check(f"D seed set {tag}", ok_set and n_files == 2048,
                     f"{n_files} npz, seeds {min(seeds)}..{max(seeds)}, "
                     f"set==expected[{min(exp)}..{max(exp)}, n={len(exp)}]: {ok_set}")
    s1, s2 = set(npz["confirm_W12"]), set(npz["confirm_S16"])
    record_check("D disjoint W12 vs S16", not (s1 & s2),
                 f"intersection size {len(s1 & s2)}")
    for tag in CONDITIONS:
        seeds = set(npz[tag])
        hits = [(lo, hi) for lo, hi in HIST_BLOCKS
                if any(lo <= s < hi for s in seeds)]
        record_check(f"D historical blocks {tag}", not hits,
                     f"{len(HIST_BLOCKS)} blocks checked, overlaps: {hits if hits else 'none'}")

    # ---------------- E: shared inputs + params ------------------------ #
    import generate_llrs as gl                              # noqa: E402
    sc_mod = gl._load_single_cell()
    codec = sc_mod._correctness().TargetApskCodec()
    for tag in CONDITIONS:
        frames = raw[tag]["frames"]
        cond = CONDITIONS[tag]
        idx = np.unique(np.linspace(0, 2047, 50).astype(int))
        mismatch = []
        for i in idx:
            r = frames[int(i)]
            d = npz[tag].get(r["seed"])
            if d is None or r["llr_sha256"] != d["llr_sha256"]:
                mismatch.append(r["seed"])
        record_check(f"E1 llr_sha256 raw vs npz {tag}", not mismatch,
                     f"50 sampled frames: string match {50 - len(mismatch)}/50"
                     + (f"; mismatch seeds {mismatch[:5]}" if mismatch else ""))
        # stronger content integrity: regenerate 2 frames (first + middle)
        # through the real signal chain; npz stores the float32 cast of the
        # float64 (1,1536) chain output whose sha the npz records.
        regen_bad = []
        for seed in (min(npz[tag]), sorted(npz[tag])[len(npz[tag]) // 2]):
            d = npz[tag][seed]
            fr = gl.build_frame(sc_mod, codec, seed=seed,
                                snr_db_override=cond["snr_db"],
                                turb_alpha_override=cond["turb_alpha"],
                                turb_beta_override=cond["turb_beta"])
            if (fr["llr_sha256"] != d["llr_sha256"]
                    or not np.array_equal(fr["llr"], d["llr"])
                    or not np.array_equal(fr["truth_info"], d["truth_info"])
                    or not np.array_equal(fr["truth_coded"], d["truth_coded"])):
                regen_bad.append(seed)
        record_check(f"E1b regen integrity {tag}", not regen_bad,
                     f"seeds {min(npz[tag])} and {sorted(npz[tag])[len(npz[tag]) // 2]} "
                     "regenerated via generate_llrs.build_frame: llr bytes, truth_info, "
                     "truth_coded, llr_sha256 all bit-exact vs npz"
                     + (f"; mismatch {regen_bad}" if regen_bad else ""))
        bad_param, bad_manifest = [], []
        for seed, d in npz[tag].items():
            if (d["snr_db"] != cond["snr_db"]
                    or d["turbulence_alpha"] != cond["turb_alpha"]
                    or d["turbulence_beta"] != cond["turb_beta"]):
                bad_param.append(seed)
            if (d["turbulence_alpha_manifest"] != 4.0
                    or d["turbulence_beta_manifest"] != 1.9):
                bad_manifest.append(seed)
        record_check(f"E2 params {tag}", not bad_param,
                     f"all {len(npz[tag])} npz: snr_db=={cond['snr_db']:g}, "
                     f"alpha=={cond['turb_alpha']:g}, beta=={cond['turb_beta']:g}; "
                     f"violations {len(bad_param)}")
        record_check(f"E3 manifest {tag}", not bad_manifest,
                     f"all {len(npz[tag])} npz: alpha_manifest==4.0 & beta_manifest==1.9; "
                     f"violations {len(bad_manifest)}")

    # ---------------- F: composition bands ------------------------------ #
    for tag in CONDITIONS:
        frames = raw[tag]["frames"]
        ch_err = {}
        for seed, d in npz[tag].items():
            hd = (d["llr"] > 0).astype(np.uint8)   # llr>0 -> bit1
            ch_err[seed] = int(np.count_nonzero(hd != d["truth_coded"]))
        b0_wrong = [r for r in frames if r["B0"]["info_errors"] > 0]
        rows = [(ch_err[r["seed"]],
                 r["arms"]["R1"]["final"]["info_errors"] == 0,
                 r["arms"]["R3"]["final"]["info_errors"] == 0)
                for r in b0_wrong]
        bands = {}
        for lo, hi in BANDS:
            band = [x for x in rows if lo <= x[0] < hi]
            key = f"[{lo},{hi if hi < 10**9 else 'inf'})"
            bands[key] = {"n": len(band),
                          "r1_rescued": sum(1 for x in band if x[1]),
                          "r3_rescued": sum(1 for x in band if x[2])}
        errs = np.array([x[0] for x in rows], dtype=float)
        quant = {str(q): float(np.percentile(errs, q)) for q in (10, 25, 50, 75)}
        marg = bands["[100,140)"]["n"] / len(b0_wrong) if b0_wrong else None
        mine = {"b0_failed": len(b0_wrong), "ch_hd_err_quantiles": quant,
                "bands": bands, "marginal_band_fraction_of_failures": marg}
        scomp = summary[tag]["composition"]
        diffs = []
        if scomp["b0_failed"] != mine["b0_failed"]:
            diffs.append(f"b0_failed {scomp['b0_failed']}!={mine['b0_failed']}")
        if scomp["ch_hd_err_quantiles"] != mine["ch_hd_err_quantiles"]:
            diffs.append(f"quantiles {scomp['ch_hd_err_quantiles']}!={mine['ch_hd_err_quantiles']}")
        if scomp["marginal_band_fraction_of_failures"] != marg:
            diffs.append(f"marginal {scomp['marginal_band_fraction_of_failures']}!={marg}")
        for key, val in bands.items():
            for f in ("n", "r1_rescued", "r3_rescued"):
                if scomp["bands"][key][f] != val[f]:
                    diffs.append(f"bands.{key}.{f} {scomp['bands'][key][f]}!={val[f]}")
        agg160 = {"n": sum(bands[k]["n"] for k in ("[160,220)", "[220,320)", "[320,inf)")),
                  "r1": sum(bands[k]["r1_rescued"] for k in ("[160,220)", "[220,320)", "[320,inf)")),
                  "r3": sum(bands[k]["r3_rescued"] for k in ("[160,220)", "[220,320)", "[320,inf)"))}
        b100, b140 = bands["[100,140)"], bands["[140,160)"]
        record_check(
            f"F composition {tag}", not diffs,
            f"b0_failed={mine['b0_failed']}; [100,140): n={b100['n']} r1={b100['r1_rescued']} "
            f"r3={b100['r3_rescued']} (marg={fmt(marg)}); [140,160): n={b140['n']} "
            f"r1={b140['r1_rescued']} r3={b140['r3_rescued']}; [160,inf): n={agg160['n']} "
            f"r1={agg160['r1']} r3={agg160['r3']}"
            + ("; " + "; ".join(diffs) if diffs else "; zero deviation vs summary"))

    # ---------------- summary ------------------------------------------- #
    print("\n==== SUMMARY ====")
    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    for name, ok, ev in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{len(CHECKS)} checks, {n_fail} FAIL" if n_fail
          else f"\nALL {len(CHECKS)} CHECKS PASS")


if __name__ == "__main__":
    main()
