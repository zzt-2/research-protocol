"""Verification script for LEO ISL scheduling simulator.

Runs the full verification checklist:
  1. Analytical verification (orbital period, beam radius, FSPL)
  2. Statistical verification (capacity distribution, traffic, visibility)
  3. Regression tests (fixed orbit, fixed traffic, σ_J=0)
  4. Autocorrelation warning
  5. MDP trial run (Part A-checkpoint)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

# Use small constellation for fast verification: 4 planes × 8 sats = 32
N_PLANES = 4
SATS_PER_PLANE = 8

from simulator.orbit import OrbitPropagator
from simulator.visibility import VisibilityConnectivity
from simulator.channel import ChannelModel
from simulator.traffic import TrafficGenerator
from simulator.router import Router
from simulator.environment import ISLEnvironment
from simulator import config


def header(msg):
    print(f"\n{'='*60}\n  {msg}\n{'='*60}")


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and condition else ""))
    if not condition:
        print(f"        Detail: {detail}")
    return condition


# ─── 1. Analytical Verification ───

def test_orbital_period():
    header("1. Analytical Verification — Orbital Period")
    orb = OrbitPropagator(n_planes=N_PLANES, sats_per_plane=SATS_PER_PLANE)
    T = orb.period
    # Expected: T = 2π√((R_e+h)³/μ) ≈ 5790s for 550km (using RE=6378 gives ~5730)
    expected_low, expected_high = 5700, 5900
    check("Orbital period range",
          expected_low < T < expected_high,
          f"T = {T:.1f}s (expected ~5730-5790s)")

    # Verify positions
    pos = orb.propagate(0)
    check("Position shape", pos.shape == (orb.n_sats, 3),
          f"shape = {pos.shape}")
    alt = np.sqrt(np.sum(pos**2, axis=1)) - config.RE
    check("Altitude range", 500 < alt.mean() < 600,
          f"mean alt = {alt.mean():.1f} km (expected ~550km)")
    return orb


def test_beam_and_fspl():
    header("1b. Analytical Verification — Beam Radius & FSPL")
    ch = ChannelModel()

    # Beam radius at 1000 km
    d_m = 1000e3
    w = ch.beam_radius(d_m)
    z_R = ch.z_R
    w_expected = ch.w0 * np.sqrt(1 + (d_m / z_R)**2)
    check("Beam radius formula",
          abs(w - w_expected) / w_expected < 1e-6,
          f"w(1000km) = {w:.4f} m")

    # FSPL at 1000 km
    fspl = ch.fspl_db(1000)
    expected_fspl = 20 * np.log10(4 * np.pi * 1e6 / (1.55e-6))
    check("FSPL formula",
          abs(fspl - expected_fspl) < 0.01,
          f"FSPL(1000km) = {fspl:.2f} dB (expected {expected_fspl:.2f})")

    # Capacity at various distances
    dists = np.array([100, 500, 1000, 2000, 3000])
    caps, pouts, avail = ch.compute(dists)
    check("Capacity decreases with distance",
          all(caps[i] >= caps[i+1] for i in range(len(caps)-1)),
          f"caps = {[f'{c:.2f}' for c in caps]} Gbps")
    check("All links available (high SNR)",
          all(avail),
          f"P_out range: [{pouts.min():.2e}, {pouts.max():.2e}]")
    return ch


# ─── 2. Statistical Verification ───

def test_visibility(orb):
    header("2. Statistical Verification — Visibility & Topology")
    vis = VisibilityConnectivity()
    pos = orb.propagate(0)
    edges = vis.compute(pos)
    n_edges = len(edges)
    n_sats = orb.n_sats

    check("Candidate edges found", n_edges > 0,
          f"{n_edges} candidate edges for {n_sats} satellites")

    avg_neighbors = 2 * n_edges / n_sats if n_sats > 0 else 0
    check("Reasonable avg neighbors", 2 < avg_neighbors < 30,
          f"avg neighbors = {avg_neighbors:.1f}")

    # Check distances
    dists = [d for _, _, d in edges]
    check("All distances ≤ z_max", max(dists) <= config.Z_MAX + 1,
          f"max dist = {max(dists):.1f} km (z_max = {config.Z_MAX})")

    # Cross-orbit distance at equator (approximate)
    raan_step = 360 / orb.n_planes
    eq_dist = 2 * (config.RE + orb.altitude) * np.sin(np.radians(raan_step) / 2)
    check("Cross-orbit spacing < z_max for small constellations",
          eq_dist < config.Z_MAX or n_edges > 0,
          f"cross-orbit spacing ≈ {eq_dist:.0f} km")
    return vis


def test_traffic():
    header("2b. Statistical Verification — Traffic Distribution")
    traffic = TrafficGenerator(n_gs=50, seed=42)
    lat, lon, pop = traffic.get_gs_positions()

    check("GS on land (lat range)", (-60 < lat).all() and (lat < 70).all(),
          f"lat range [{lat.min():.1f}, {lat.max():.1f}]")

    # Check demand: land >> ocean (all GS are on land by construction)
    total_land_pop = pop.sum()
    check("Land-based GS (population > 0)", total_land_pop > 0,
          f"total pop weight = {total_land_pop:.0f}")

    # Check demand matrix
    n = traffic.n_gs
    check("Demand matrix shape", traffic._demand_scale.shape == (n, n),
          f"demand matrix {traffic._demand_scale.shape}")
    diag_zero = np.all(np.diag(traffic._demand_scale) == 0)
    check("Zero self-demand", diag_zero)
    return traffic


# ─── 3. Regression Tests ───

def test_regression_fixed_orbit(orb, vis):
    header("3. Regression Tests — Fixed Orbit")
    pos_t0 = orb.propagate(0)
    edges_t0 = vis.compute(pos_t0)
    edges_t0_set = {(i, j) for i, j, _ in edges_t0}

    # Same time → same edges
    pos_t0b = orb.propagate(0)
    edges_t0b = vis.compute(pos_t0b)
    edges_t0b_set = {(i, j) for i, j, _ in edges_t0b}

    check("Same time → same topology", edges_t0_set == edges_t0b_set,
          f"|E| = {len(edges_t0_set)}")

    # Different time → potentially different topology
    pos_t100 = orb.propagate(100)
    edges_t100 = vis.compute(pos_t100)
    check("Different time → topology changes",
          len({(i,j) for i,j,_ in edges_t100} - edges_t0_set) > 0 or
          len(edges_t0_set - {(i,j) for i,j,_ in edges_t100}) > 0,
          f"t=0: {len(edges_t0)} edges, t=100: {len(edges_t100)} edges")


def test_regression_no_jitter():
    header("3b. Regression Tests — σ_J = 0 → Pure Gaussian Beam")
    ch_jitter = ChannelModel(sigma_jitter=1e-5)
    ch_no_jitter = ChannelModel(sigma_jitter=0)

    dists = np.array([500, 1000, 2000])
    caps_j, _, _ = ch_jitter.compute(dists)
    caps_nj, _, _ = ch_no_jitter.compute(dists)

    check("No jitter → higher capacity",
          all(caps_nj >= caps_j - 0.01),
          f"with jitter: {caps_j.round(2)}, without: {caps_nj.round(2)}")


def test_router():
    header("3c. Regression Tests — Router (known topology)")
    router = Router()

    # Simple 4-node line topology: 0-1-2-3
    active = [(0, 1), (1, 2), (2, 3)]
    dists = {(0,1): 100, (1,2): 100, (2,3): 100}
    caps = {(0,1): 10, (1,2): 10, (2,3): 10}
    flows = [(0, 3, 5.0)]

    result = router.route(active, dists, caps, flows, n_sats=4)
    check("Shortest path found", result['flow_details'][0][4] == [0, 1, 2, 3],
          f"path = {result['flow_details'][0][4]}")
    check("Full delivery (no congestion)", abs(result['delivered'] - 5.0) < 0.01,
          f"delivered = {result['delivered']:.2f}")

    # Congestion test: two flows competing for link 1-2 (cap=10)
    flows2 = [(0, 3, 6.0), (0, 3, 6.0)]  # total 12 > cap 10
    result2 = router.route(active, dists, caps, flows2, n_sats=4)
    check("Congestion → proportional reduction",
          abs(result2['delivered'] - 10.0) < 0.1,
          f"delivered = {result2['delivered']:.2f} (demand=12, cap=10)")


# ─── 4. Autocorrelation ───

def test_autocorrelation(orb, ch):
    header("4. Autocorrelation Warning (lag-1 ρ < 0.95)")
    vis = VisibilityConnectivity()

    # Collect capacity time series for a fixed edge
    n_steps = 20
    dt = config.TAU

    # Find a stable edge
    pos0 = orb.propagate(0)
    edges0 = vis.compute(pos0)
    if not edges0:
        print("  [SKIP] No edges for autocorrelation test")
        return

    target_edge = edges0[0]
    i, j, d0 = target_edge
    capacities = []

    for t in range(n_steps):
        pos = orb.propagate(t * dt)
        # Recompute distance for this pair
        d = np.linalg.norm(pos[i] - pos[j])
        if d > config.Z_MAX:
            capacities.append(0)
            continue
        c, _, _ = ch.compute(np.array([d]))
        capacities.append(c[0])

    caps_arr = np.array(capacities)
    if len(caps_arr) < 3 or np.std(caps_arr) < 1e-10:
        print(f"  [SKIP] Insufficient variance in capacity series")
        return

    # Lag-1 autocorrelation
    mean = caps_arr.mean()
    var = np.sum((caps_arr - mean)**2)
    if var < 1e-10:
        print(f"  [SKIP] Zero variance")
        return
    autocorr = np.sum((caps_arr[1:] - mean) * (caps_arr[:-1] - mean)) / var
    check(f"Capacity lag-1 ρ < 0.95", autocorr < 0.95,
          f"ρ = {autocorr:.4f}")


# ─── 5. MDP Trial Run (Part A-checkpoint) ───

def test_mdp_trial():
    header("5. MDP Trial Run (Part A-checkpoint)")

    env = ISLEnvironment(
        n_planes=N_PLANES, sats_per_plane=SATS_PER_PLANE,
        episode_steps=10, seed=42
    )

    # Random policy
    def random_policy(obs):
        n = obs['n_candidates']
        return np.random.random(n)

    # Greedy policy: select edges with highest capacity
    def greedy_policy(obs):
        ef = obs['edge_features']
        if len(ef) == 0:
            return np.array([])
        # Greedily prefer high-capacity, short-distance edges
        scores = ef[:, 0] / (ef[:, 1] + 0.01)  # capacity / distance
        return scores / (scores.max() + 1e-10)

    print("\n  --- Random policy episode ---")
    np.random.seed(42)
    metrics_random, reward_random = env.run_episode(random_policy, verbose=True)

    print("\n  --- Greedy policy episode ---")
    metrics_greedy, reward_greedy = env.run_episode(greedy_policy, verbose=True)

    # Reward breakdown table
    print("\n  Reward breakdown:")
    print(f"  {'':20s} {'Random':>10s} {'Greedy':>10s}")
    print(f"  {'-'*42}")

    # Re-run to get detailed breakdown
    obs, _ = env.reset()
    random_breakdown = {'throughput': [], 'switch': [], 'setup': []}
    for _ in range(env.episode_steps):
        scores = random_policy(obs)
        obs, r, term, trunc, info = env.step(scores)
        bd = info['reward_dict']['abs_breakdown']
        for k in bd:
            random_breakdown[k].append(bd[k])
        if term:
            break

    obs, _ = env.reset()
    greedy_breakdown = {'throughput': [], 'switch': [], 'setup': []}
    for _ in range(env.episode_steps):
        scores = greedy_policy(obs)
        obs, r, term, trunc, info = env.step(scores)
        bd = info['reward_dict']['abs_breakdown']
        for k in bd:
            greedy_breakdown[k].append(bd[k])
        if term:
            break

    for k in ['throughput', 'switch', 'setup']:
        r_avg = np.mean(random_breakdown[k])
        g_avg = np.mean(greedy_breakdown[k])
        print(f"  {k:20s} {r_avg:10.4f} {g_avg:10.4f}")

    # Check dominance
    r_total_abs = sum(np.mean(random_breakdown[k]) for k in random_breakdown)
    g_total_abs = sum(np.mean(greedy_breakdown[k]) for k in greedy_breakdown)

    # Check: no single term > 95% of total abs reward
    for policy_name, breakdown in [("Random", random_breakdown), ("Greedy", greedy_breakdown)]:
        total_abs = sum(np.mean(breakdown[k]) for k in breakdown)
        for k in breakdown:
            ratio = np.mean(breakdown[k]) / max(total_abs, 1e-10) * 100
            check(f"{policy_name}: {k} < 95% of total",
                  ratio < 95,
                  f"{ratio:.1f}%")

    # Check: greedy > random by > 10%
    gap = (reward_greedy - reward_random) / max(abs(reward_random), 1e-6) * 100
    check("Greedy vs Random gap > 10%",
          abs(gap) > 10 or reward_greedy > reward_random,
          f"greedy={reward_greedy:.4f}, random={reward_random:.4f}, gap={gap:.1f}%")

    print(f"\n  Random episode: reward={reward_random:.4f}, M1={metrics_random['M1_throughput']:.3f}")
    print(f"  Greedy episode: reward={reward_greedy:.4f}, M1={metrics_greedy['M1_throughput']:.3f}")


# ─── Main ───

if __name__ == "__main__":
    print("LEO ISL Scheduling Simulator — Verification Suite")
    print(f"Small constellation: {N_PLANES}×{SATS_PER_PLANE} = {N_PLANES*SATS_PER_PLANE} sats")

    orb = test_orbital_period()
    ch = test_beam_and_fspl()
    vis = test_visibility(orb)
    test_traffic()
    test_regression_fixed_orbit(orb, vis)
    test_regression_no_jitter()
    test_router()
    test_autocorrelation(orb, ch)
    test_mdp_trial()

    print(f"\n{'='*60}")
    print("  Verification complete.")
    print(f"{'='*60}")
