"""B1 Baseline: Hybrid Handover Strategy (HHS) — Algorithm 1 from L08.

Traditional multi-criteria handover heuristic combining SINR quality, elevation
angle, satellite load, and connection stability into a per-satellite utility score.
Uses a three-tier decision logic: forced handover, opportunity upgrade, or maintain.

This is NOT a DRL method — it is a pure heuristic requiring no training.
"""

import json
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulator.environment import LEOSatHandoverEnv
from simulator.orbit import compute_elevation_batch
import config as cfg

SEEDS = [42, 43, 44, 45, 46]

# HHS parameters (from config.py)
W_SINR = cfg.HHS_W_SINR          # 0.5
W_ELEV = cfg.HHS_W_ELEV          # 0.15
W_LOAD = cfg.HHS_W_LOAD          # 0.25
W_STAB = cfg.HHS_W_STAB          # 0.1
P_HO = cfg.HHS_P_HO              # 0.03
STAB_K = cfg.HHS_STAB_K          # 0.2
STAB_MID = cfg.HHS_STAB_MID      # 15.0
DEGRADE_TH = cfg.HHS_DEGRADE_TH_DB  # 8.0 dB
UPGRADE_TH = cfg.HHS_UPGRADE_TH     # 0.02


def compute_utility(
    sinr_db: np.ndarray,
    elevations: np.ndarray,
    sat_loads: np.ndarray,
    current_sat: int,
    t_conn: int,
) -> np.ndarray:
    """Compute per-satellite utility for a single UE.

    Parameters
    ----------
    sinr_db : shape (num_sats,) — SINR in dB for each satellite
    elevations : shape (num_sats,) — elevation angle in degrees
    sat_loads : shape (num_sats,) — current number of UEs served by each satellite
    current_sat : int — index of currently serving satellite (-1 if none)
    t_conn : int — connection duration in steps for current satellite

    Returns
    -------
    utilities : shape (num_sats,) — utility score per satellite
    """
    num_sats = sinr_db.shape[0]

    # Normalized SINR: q(s) = clip((SINR - SINR_min) / (SINR_max - SINR_min), 0, 1)
    q = np.clip(
        (sinr_db - cfg.SINR_MIN_DB) / (cfg.SINR_MAX_DB - cfg.SINR_MIN_DB),
        0.0, 1.0,
    )

    # Normalized elevation: e(s) = clip((elev - min_elev) / (elev_max - min_elev), 0, 1)
    e = np.clip(
        (elevations - cfg.MIN_ELEVATION_DEG) / (cfg.ELEV_MAX_DEG - cfg.MIN_ELEVATION_DEG),
        0.0, 1.0,
    )

    # Normalized load: l(s) = 1 - N_occ(s) / SAT_CAPACITY
    l = 1.0 - sat_loads / cfg.SAT_CAPACITY

    # Base utility: U_base(s) = w_sinr * q(s) + w_elev * e(s) + w_load * l(s)
    u_base = W_SINR * q + W_ELEV * e + W_LOAD * l

    # Stability bonus (logistic) for current serving satellite
    psi = 1.0 / (1.0 + np.exp(-STAB_K * (t_conn - STAB_MID)))

    utilities = u_base.copy()
    if current_sat >= 0:
        # Add stability bonus to serving satellite
        utilities[current_sat] += W_STAB * psi
        # Subtract handover penalty from all other satellites
        mask = np.ones(num_sats, dtype=bool)
        mask[current_sat] = False
        utilities[mask] -= P_HO
    else:
        # No serving satellite: small penalty on all (pushes toward picking one)
        utilities -= P_HO

    return utilities


def select_hhs(
    sinr_db: np.ndarray,
    elevations: np.ndarray,
    sat_loads: np.ndarray,
    valid_mask: np.ndarray,
    prev_sats: np.ndarray,
    t_conn: np.ndarray,
) -> np.ndarray:
    """HHS per-UE satellite selection (Algorithm 1 from L08).

    Parameters
    ----------
    sinr_db : shape (num_ues, num_sats) — SINR in dB
    elevations : shape (num_ues, num_sats) — elevation in degrees
    sat_loads : shape (num_sats,) — current satellite loads
    valid_mask : shape (num_ues, num_sats) — visibility boolean mask
    prev_sats : shape (num_ues,) — previously connected satellite index per UE
    t_conn : shape (num_ues,) — connection duration in steps per UE

    Returns
    -------
    actions : shape (num_ues,) — selected satellite per UE
    """
    num_ues = valid_mask.shape[0]
    actions = np.zeros(num_ues, dtype=int)

    for ue in range(num_ues):
        visible = np.where(valid_mask[ue])[0]
        if len(visible) == 0:
            actions[ue] = 0
            continue

        current_sat = prev_sats[ue]

        # Compute utilities for all satellites
        utilities = compute_utility(
            sinr_db[ue], elevations[ue], sat_loads, current_sat, t_conn[ue],
        )

        if current_sat < 0:
            # No serving satellite yet: pick highest-utility visible satellite
            vis_utils = utilities[visible]
            actions[ue] = visible[np.argmax(vis_utils)]
            continue

        # Three-tier decision logic
        current_sinr = sinr_db[ue, current_sat]

        # Tier 1: Forced handover — current SINR below degradation threshold
        if current_sinr < DEGRADE_TH:
            vis_utils = utilities.copy()
            vis_utils[~valid_mask[ue]] = -np.inf
            actions[ue] = int(np.argmax(vis_utils))
            continue

        # Tier 2: Opportunity upgrade — better satellite available
        vis_utils = utilities.copy()
        vis_utils[~valid_mask[ue]] = -np.inf
        best_idx = int(np.argmax(vis_utils))
        best_util = vis_utils[best_idx]
        current_util = utilities[current_sat]

        if best_util - current_util > UPGRADE_TH:
            actions[ue] = best_idx
            continue

        # Tier 3: Maintain current satellite
        actions[ue] = current_sat

    return actions


def run_episode(seed: int) -> dict:
    """Run one full episode with HHS policy. Returns aggregated metrics."""
    env = LEOSatHandoverEnv(num_ues=cfg.NUM_UES, seed=seed)
    obs = env.reset(seed=seed)

    # HHS tracks its own connection time for decision logic
    prev_sats = np.full(env.num_ues, -1, dtype=int)
    t_conn = np.zeros(env.num_ues, dtype=int)

    total_throughputs = []
    blocking_rates = []
    handover_count = 0
    done = False

    while not done:
        valid_mask = env.get_valid_actions()

        # Get SINR from environment info by peeking at current channel state
        # Reconstruct elevation from satellite positions
        sat_pos = env.constellation.get_positions(env._step)
        elevations = np.zeros((env.num_ues, env.num_sats))
        for ue in range(env.num_ues):
            elevations[ue] = compute_elevation_batch(sat_pos, env.ue_positions[ue])

        # Estimate SINR using channel model (without shadow fading for decision)
        snr_db = np.zeros((env.num_ues, env.num_sats))
        for ue in range(env.num_ues):
            d = sat_pos - env.ue_positions[ue][np.newaxis, :]
            distances = np.linalg.norm(d, axis=1)
            snr_db[ue] = env.channel.compute_snr_db(distances, elevations[ue])

        # HHS satellite selection
        actions = select_hhs(
            snr_db, elevations, env._sat_loads, valid_mask, prev_sats, t_conn,
        )

        obs, _rewards, done, info = env.step(actions)

        # Update connection tracking
        for ue in range(env.num_ues):
            if actions[ue] != prev_sats[ue] or prev_sats[ue] < 0:
                t_conn[ue] = 0
            else:
                t_conn[ue] += 1
        prev_sats = actions.copy()

        total_throughputs.append(float(info["total_throughput_bps"]))
        blocking_rates.append(float(info["blocking_rate"]))
        handover_count += int(info["handover_count"])

    return {
        "seed": seed,
        "mean_throughput_mbps": float(np.mean(total_throughputs)) / 1e6,
        "mean_blocking_rate": float(np.mean(blocking_rates)),
        "total_handover_count": handover_count,
    }


def main():
    print("=" * 60)
    print("B1 HHS (Hybrid Handover Strategy) Baseline")
    print("=" * 60)

    seed_results = []
    for seed in SEEDS:
        metrics = run_episode(seed)
        seed_results.append(metrics)
        print(
            f"  seed={seed:3d} | "
            f"avg_tput={metrics['mean_throughput_mbps']:8.2f} Mbps | "
            f"avg_blk={metrics['mean_blocking_rate']:.4f} | "
            f"HO_count={metrics['total_handover_count']:5d}"
        )

    throughputs = [r["mean_throughput_mbps"] for r in seed_results]
    blockings = [r["mean_blocking_rate"] for r in seed_results]
    handovers = [r["total_handover_count"] for r in seed_results]

    summary = {
        "seeds": seed_results,
        "summary": {
            "mean_throughput_mbps": float(np.mean(throughputs)),
            "std_throughput_mbps": float(np.std(throughputs)),
            "mean_blocking_rate": float(np.mean(blockings)),
            "std_blocking_rate": float(np.std(blockings)),
            "mean_handover_count": float(np.mean(handovers)),
            "std_handover_count": float(np.std(handovers)),
        },
    }

    s = summary["summary"]
    print(f"\n  Summary ({len(SEEDS)} seeds):")
    print(f"    Throughput : {s['mean_throughput_mbps']:.2f} +/- {s['std_throughput_mbps']:.2f} Mbps")
    print(f"    Blocking   : {s['mean_blocking_rate']:.4f} +/- {s['std_blocking_rate']:.4f}")
    print(f"    Handovers  : {s['mean_handover_count']:.1f} +/- {s['std_handover_count']:.1f}")

    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    out_path = results_dir / "b1_hhs_results.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
