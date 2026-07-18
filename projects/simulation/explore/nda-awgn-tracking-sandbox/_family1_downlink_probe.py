# -*- coding: utf-8 -*-
"""T017 Family-1 downlink-only matched diagnostic (3 seeds; not for paper)."""
import hashlib
import inspect
import os
import platform
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIM_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
for path in (SIM_ROOT, os.path.join(SIM_ROOT, "simulator"), HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import _a4_switch_common768_30seed as A
import _a4_branchrouted_30seed as B
import _b11_params as P
import sc_nda_ml_sim as S
from common import amp_limit, generate_shared_realization_apsk, mmse_equalize, save_results
from params import SimulationConfig

OUT_JSON = os.path.join(HERE, "_family1_downlink_probe.json")
SCENES = ("weak", "moderate", "strong")
SNR_DB = (5.0, 13.0, 17.0, 19.0, 25.0)
SEEDS = (0, 1, 2)
PARAMS = {
    "old": {
        "weak": (4.0, 3.0), "moderate": (2.5, 1.8), "strong": (1.5, 0.8),
    },
    "new_family1": {
        "weak": (11.65104537862684, 10.122365306725285),
        "moderate": (4.026521312058279, 1.9105223344570113),
        "strong": (4.2256713509586925, 1.3621952523122576),
    },
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def realization_digest_update(h, realization, window_seed):
    h.update(np.asarray([window_seed], dtype=np.int64).tobytes())
    for key in ("bits", "tx", "h", "phi", "rx_raw"):
        h.update(np.ascontiguousarray(realization[key]).view(np.uint8).tobytes())


def run_a_case(scene, snr_db, seed_index, turb_params, also_b=False):
    cfg = SimulationConfig()
    ns, nw = P.N_DFT, P.N_BLOCKS
    gamma_lin = 10.0 ** (snr_db / 10.0)
    start = P.SEED_TURB0 + seed_index * nw
    counts = {"fixed_nda_errors": 0, "fixed_da_errors": 0,
              "selected_errors": 0, "oracle_errors": 0,
              "n_select_da": 0, "n_select_nda": 0}
    bcounts = {"selected_errors": 0, "n_select_da": 0, "n_select_nda": 0}
    identity = hashlib.sha256()
    for offset in range(nw):
        window_seed = start + offset
        r = generate_shared_realization_apsk(
            ns, gamma_lin, scene, cfg.doppler.DOPPLER_HIGH,
            mod="m16apsk", seed=window_seed, turb_params=turb_params,
        )
        realization_digest_update(identity, r, window_seed)
        raw, bits, tx = r["rx_raw"], r["bits"], r["tx"]
        hb = S.estimate_h_blind_perblock(raw, gamma_lin)
        blind = amp_limit(mmse_equalize(raw, hb, gamma_lin), 3.0)
        hp = S.estimate_h_pilot_perblock(raw, tx, gamma_lin)
        pilot = amp_limit(mmse_equalize(raw, hp, gamma_lin), 3.0)
        ne_nda_all, ne_da, ne_nda = A.per_block(blind, pilot, bits, tx)
        choice = A.decide(raw, snr_db, gamma_lin)
        counts["fixed_nda_errors"] += ne_nda
        counts["fixed_da_errors"] += ne_da
        counts["oracle_errors"] += min(ne_nda, ne_da)
        counts["n_select_da" if choice == "da" else "n_select_nda"] += 1
        counts["selected_errors"] += ne_da if choice == "da" else ne_nda
        if also_b:
            bchoice = B.decide(raw, snr_db, gamma_lin)
            assert bchoice == choice
            if bchoice == "da":
                bcounts["n_select_da"] += 1
                bh = S.estimate_h_pilot_perblock(raw, tx, gamma_lin)
                binput = amp_limit(mmse_equalize(raw, bh, gamma_lin), 3.0)
                bne, selected_rx = B.per_block_da(binput, bits, tx)
            else:
                bcounts["n_select_nda"] += 1
                bh = S.estimate_h_blind_perblock(raw, gamma_lin)
                binput = amp_limit(mmse_equalize(raw, bh, gamma_lin), 3.0)
                bne_all, bne, selected_rx = B.per_block_nda(binput, bits)
            assert selected_rx.shape == (ns,)
            bcounts["selected_errors"] += bne
    n_bits = nw * A.COMMON768_BITS_PER_BLOCK
    out = {
        "scene": scene, "snr_db": float(snr_db), "seed_index": int(seed_index),
        "window_seed_start": int(start),
        "window_seed_end_inclusive": int(start + nw - 1),
        "window_seeds": list(range(start, start + nw)),
        "n_windows": int(nw), "n_bits": int(n_bits),
        "realization_identity_sha256": identity.hexdigest(),
        **{k: int(v) for k, v in counts.items()},
    }
    out.update({
        "fixed_nda_ber": counts["fixed_nda_errors"] / n_bits,
        "fixed_da_ber": counts["fixed_da_errors"] / n_bits,
        "selected_ber": counts["selected_errors"] / n_bits,
        "oracle_ber": counts["oracle_errors"] / n_bits,
    })
    if also_b:
        out["route_b"] = {
            **{k: int(v) for k, v in bcounts.items()},
            "n_windows": int(nw), "n_bits": int(n_bits),
            "window_seed_start": int(start),
            "window_seed_end_inclusive": int(start + nw - 1),
            "realization_identity_sha256": identity.hexdigest(),
            "selected_ber": bcounts["selected_errors"] / n_bits,
        }
    return out


def aggregate_cells(cases):
    cells = []
    for scene in SCENES:
        for snr in SNR_DB:
            cell = {"scene": scene, "snr_db": snr}
            for family in ("old", "new_family1"):
                rows = [x for x in cases[family]
                        if x["scene"] == scene and x["snr_db"] == snr]
                nb = sum(x["n_bits"] for x in rows)
                vals = {k: sum(x[k] for x in rows) for k in (
                    "fixed_nda_errors", "fixed_da_errors", "selected_errors",
                    "oracle_errors", "n_select_da", "n_select_nda")}
                cell[family] = {**vals, "n_bits": nb,
                    "fixed_nda_ber": vals["fixed_nda_errors"] / nb,
                    "fixed_da_ber": vals["fixed_da_errors"] / nb,
                    "selected_ber": vals["selected_errors"] / nb,
                    "oracle_ber": vals["oracle_errors"] / nb,
                    "selected_vs_fixed_nda_gain_db": float(
                        10 * np.log10(vals["fixed_nda_errors"] / vals["selected_errors"])),
                    "fixed_winner": "da" if vals["fixed_da_errors"] < vals["fixed_nda_errors"] else "nda",
                }
            cells.append(cell)
    return cells


def main():
    t0 = time.time()
    cases = {"old": [], "new_family1": []}
    total = len(SCENES) * len(SNR_DB) * len(SEEDS)
    done = 0
    for scene in SCENES:
        for snr in SNR_DB:
            for seed_index in SEEDS:
                cases["old"].append(run_a_case(
                    scene, snr, seed_index, PARAMS["old"][scene], False))
                cases["new_family1"].append(run_a_case(
                    scene, snr, seed_index, PARAMS["new_family1"][scene], True))
                done += 1
                print(f"[{done:02d}/{total}] {scene}@{snr:g} seed={seed_index}", flush=True)
    script = os.path.abspath(__file__)
    dependencies = {
        os.path.relpath(os.path.abspath(inspect.getsourcefile(module)), SIM_ROOT):
            sha256_file(os.path.abspath(inspect.getsourcefile(module)))
        for module in (A, B, S)
    }
    dependencies[os.path.relpath(script, SIM_ROOT)] = sha256_file(script)
    channel_path = os.path.join(SIM_ROOT, "common", "_channel.py")
    dependencies[os.path.relpath(channel_path, SIM_ROOT)] = sha256_file(channel_path)
    out = {
        "authority_status": "diagnostic_probe_not_for_paper",
        "contract": "T017_downlink_only_family1",
        "parameters": {f: {s: list(v) for s, v in p.items()} for f, p in PARAMS.items()},
        "grid": {"scenes": list(SCENES), "snr_db": list(SNR_DB),
                 "seed_indices": list(SEEDS), "windows_per_case_seed": P.N_BLOCKS,
                 "common_bits_per_window": A.COMMON768_BITS_PER_BLOCK},
        "frozen": {"gamma_eff_threshold_db": A.GAMMA_EFF_TH,
                   "cv_margin": A.CV_MARGIN, "selector": "A.decide == B.decide",
                   "nda_resolution": "post-hoc tx_bits BER evaluation; not deployable"},
        "seed_formula": "window_seed = SEED_TURB0 + seed_index * N_BLOCKS + window_offset",
        "shared_realization": "A and B new consume the exact same in-memory realization; old/new use identical window seeds",
        "cases": cases, "cells": aggregate_cells(cases),
        "provenance": {"elapsed_sec": time.time() - t0,
            "python_version": platform.python_version(), "numpy_version": np.__version__,
            "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=SIM_ROOT,
                capture_output=True, text=True).stdout.strip(),
            "git_dirty": bool(subprocess.run(["git", "status", "--porcelain"], cwd=SIM_ROOT,
                capture_output=True, text=True).stdout.strip()),
            "run_command": "python _family1_downlink_probe.py",
            "file_sha256": dependencies},
    }
    save_results(out, OUT_JSON, os.path.basename(__file__))
    print(f"elapsed_sec={time.time() - t0:.3f}")


if __name__ == "__main__":
    main()
