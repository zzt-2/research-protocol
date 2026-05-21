#!/usr/bin/env python3
"""Quick 24x66 go/no-go: grid baseline + failure gap + swap diagnostic."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from baselines.grid_fixed import GridFixedBaseline
from simulator.orbit import OrbitPropagator
from simulator import config

NP, SPP = 24, 66
STEPS = 15       # quick: 15 steps instead of 50
SEEDS = [42, 100]
N_LCT = 4

print(f"=== 24×{SPP} Go/No-Go (quick {STEPS} steps) ===\n")

# ── 1. Topology info + candidate diversity ──
b0 = GridFixedBaseline(n_planes=NP, sats_per_plane=SPP, n_lct=N_LCT, seed=42)
print(f"Topology: {b0.topology_summary()}")

orbit = OrbitPropagator(NP, SPP)
pos0 = orbit.propagate(0)
n_cand = []
for p in range(NP):
    pn = (p + 1) % NP
    for s in range(SPP):
        i = p * SPP + s
        d = np.linalg.norm(pos0[pn*SPP:(pn+1)*SPP] - pos0[i], axis=1)
        n_cand.append(int(np.sum(d < config.Z_MAX)))
nc = np.array(n_cand)
print(f"Cross-orbit cand/sat: mean={nc.mean():.1f} min={nc.min()} max={nc.max()}\n")

# ── 2. Grid baseline (no failure) ──
t0 = time.time()
m1_grid = []
for seed in SEEDS:
    b = GridFixedBaseline(n_planes=NP, sats_per_plane=SPP, n_lct=N_LCT,
                          seed=seed, episode_steps=STEPS)
    m, _ = b.run_episode()
    m1_grid.append(m['M1_throughput'])
    print(f"  Grid seed={seed}: M1={m['M1_throughput']:.6f} M3={m['M3_switch_rate']:.4f}")
m1_g = np.mean(m1_grid)
print(f"  → Grid M1 = {m1_g:.6f} ± {np.std(m1_grid):.6f}  ({time.time()-t0:.0f}s)\n")

# ── 3. Grid + failure (p=0.05) ──
t0 = time.time()
m1_fail = []
for seed in SEEDS:
    b = GridFixedBaseline(n_planes=NP, sats_per_plane=SPP, n_lct=N_LCT,
                          seed=seed, episode_steps=STEPS, failure_prob=0.05)
    m, _ = b.run_episode()
    m1_fail.append(m['M1_throughput'])
    print(f"  Fail seed={seed}: M1={m['M1_throughput']:.6f} M3={m['M3_switch_rate']:.4f}")
m1_f = np.mean(m1_fail)
gap = (m1_g - m1_f) / m1_g * 100
print(f"  → Fail M1 = {m1_f:.6f}, gap = {gap:.1f}%  ({time.time()-t0:.0f}s)\n")

# ── 4. Swap diagnostic ──
print("--- Swap Diagnostic ---")
orig = dict(b0._fixed_edges)
b0.episode_steps = STEPS
ref_m, _ = b0.run_episode()
ref_m1 = ref_m['M1_throughput']
print(f"  Ref M1 = {ref_m1:.6f}")

inter_edges = [k for k, v in orig.items() if v == 'inter']
print(f"  Inter-plane edges: {len(inter_edges)}")

N_TRIALS = 12
N_SWAP = 15
deltas = []

for trial in range(N_TRIALS):
    rng = np.random.default_rng(trial * 7)
    mod = dict(orig)
    idxs = rng.choice(len(inter_edges), size=min(N_SWAP, len(inter_edges)), replace=False)

    for idx in idxs:
        (i, j) = inter_edges[idx]
        del mod[(i, j)]
        # Determine planes
        pi_i, si_i = i // SPP, i % SPP
        pi_j, sj_j = j // SPP, j % SPP
        # The edge connects plane pi_i to pi_j (adjacent). Pick one side to reconnect.
        # Reconnect satellite i to a different neighbor in plane pi_j
        candidates = []
        for s2 in range(SPP):
            j2 = pi_j * SPP + s2
            key = (min(i, j2), max(i, j2))
            if key not in mod:
                d = np.linalg.norm(pos0[i] - pos0[j2])
                if 1.0 < d < config.Z_MAX:
                    candidates.append((d, j2))
        if candidates:
            candidates.sort()
            # Pick from top 2-4 (not nearest, to test if farther links help)
            pick = rng.integers(1, min(4, len(candidates)))
            new_j = candidates[pick][1]
            mod[(min(i, new_j), max(i, new_j))] = 'inter'

    b0._fixed_edges = mod
    b0.n_lct = None
    mod_m, _ = b0.run_episode()
    delta = mod_m['M1_throughput'] - ref_m1
    deltas.append(delta)
    print(f"  Trial {trial:2d}: M1={mod_m['M1_throughput']:.6f}  Δ={delta:+.6f}")

# Restore
b0._fixed_edges = orig

deltas = np.array(deltas)
n_pos = int(np.sum(deltas > 0))
print(f"\n  Positive: {n_pos}/{N_TRIALS}  max={deltas.max():+.6f}  mean={deltas.mean():+.6f}")

# ── Verdict ──
print("\n" + "=" * 55)
print("VERDICT")
print("=" * 55)
print(f"  Grid M1:     {m1_g:.6f}")
print(f"  Failure gap: {gap:.1f}%")
print(f"  Best swap:   {deltas.max():+.6f}")
print(f"  Candidates:  mean={nc.mean():.1f} (24×20 was ~3)")

if deltas.max() > 0.003:
    print("\n  → GO: swap shows improvement room at 24×66")
    print("     Next: generate dataset + Phase A + dynamic scenario")
elif gap > 15:
    print("\n  → MAYBE: failure gap is large, dynamic scenario worth exploring")
    print("     But grid topology itself is hard to beat")
else:
    print("\n  → NO-GO: grid still near-optimal at 24×66")
    print("     Recommend archive and move on")
