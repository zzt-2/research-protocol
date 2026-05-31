#!/usr/bin/env python3
"""KF Stress Test C4+C5: Block size impact & deep fade analysis

C4: Block size sweep — BER vs block_size, net BER vs block_size
C5: Deep fade block analysis — per-block BER for KF pilot vs Fixed
"""

from sim_kf_stress_common import *

# ═══════════════════════════════════════════════════════════════
# C4 helpers: custom block-size channel generation & pilot insertion
# ═══════════════════════════════════════════════════════════════
def generate_custom_block(Ns, gamma_bar, turb_name, f_dot, seed, block_size):
    np.random.seed(seed)
    a, b = TURB[turb_name]
    bits = np.random.randint(0, 2, Ns * 2)
    tx = qpsk_mod(bits)
    h = gg_block(Ns, a, b, bs=block_size)
    n_blocks = Ns // block_size
    h_blocks = np.array([h[i * block_size] for i in range(n_blocks)])
    h_med = np.median(h_blocks)
    phi = doppler_phase(Ns, f_res=F_RESIDUAL, f_dot=f_dot)
    carrier = np.exp(1j * phi)
    signal = tx * np.sqrt(h) * carrier
    noise_var = 1.0 / (2 * gamma_bar)
    noise = np.sqrt(noise_var) * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
    rx_raw = signal + noise
    return {'rx_raw': rx_raw, 'bits': bits, 'tx': tx, 'h': h,
            'h_blocks': h_blocks, 'h_med': h_med, 'phi': phi,
            'Ns': Ns, 'gamma_bar': gamma_bar,
            'turb_name': turb_name, 'f_dot': f_dot}


def insert_pilots_bs(shared, n_pilots, block_size):
    """insert_pilots with custom block_size."""
    Ns = shared['Ns']
    n_blocks = Ns // block_size
    tx = shared['tx'].copy()
    bits = shared['bits']
    known_pilots = get_pilots(n_pilots)
    pilot_indices = []
    data_indices = []
    for b in range(n_blocks):
        base = b * block_size
        for p in range(n_pilots):
            tx[base + p] = known_pilots[p % len(known_pilots)]
            pilot_indices.append(base + p)
        for d in range(n_pilots, block_size):
            data_indices.append(base + d)
    pilot_indices = np.array(pilot_indices)
    data_indices = np.array(data_indices)
    # Rebuild rx with pilot symbols
    carrier = np.exp(1j * shared['phi'])
    noise = shared['rx_raw'] - shared['tx'] * np.sqrt(shared['h']) * carrier
    rx_pilot = tx * np.sqrt(shared['h']) * carrier + noise
    # Extract data bits
    data_bits = np.zeros(len(data_indices) * 2, dtype=int)
    for i, idx in enumerate(data_indices):
        data_bits[2*i] = bits[2*idx]
        data_bits[2*i+1] = bits[2*idx+1]
    return rx_pilot, pilot_indices, data_indices, data_bits


# ═══════════════════════════════════════════════════════════════
# C4 trial: KF pilot with custom block_size
# ═══════════════════════════════════════════════════════════════
def trial_c4(shared, n_pilots, block_size):
    """Single C4 trial: KF pilot with specified block_size."""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots_bs(shared, n_pilots, block_size)
    rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    corrected, _ = kf_pilot_recovery(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'], block_size=block_size)
    ber = ber_count(data_bits, corrected[data_idx])
    return ber


# ═══════════════════════════════════════════════════════════════
# C5 helpers: per-block BER
# ═══════════════════════════════════════════════════════════════
def per_block_ber_kf(rx_corrected, tx_bits, h_blocks, block_size, n_pilots=5):
    """Per-block BER for KF pilot output (skip pilot symbols)."""
    n_blocks = len(h_blocks)
    bers = []
    for b in range(n_blocks):
        s, e = b * block_size, (b + 1) * block_size
        data_start = s + n_pilots
        rx_data = rx_corrected[data_start:e]
        bit_start = data_start * 2
        bit_end = e * 2
        block_bits = tx_bits[bit_start:bit_end]
        bers.append(ber_count(block_bits, rx_data))
    return np.array(bers), np.array(h_blocks)


def per_block_ber_fixed(rx_corrected, tx_bits, h_blocks, block_size):
    """Per-block BER for Fixed output (no pilots, full block is data)."""
    n_blocks = len(h_blocks)
    bers = []
    for b in range(n_blocks):
        s, e = b * block_size, (b + 1) * block_size
        rx_data = rx_corrected[s:e]
        bit_start = s * 2
        bit_end = e * 2
        block_bits = tx_bits[bit_start:bit_end]
        bers.append(ber_count(block_bits, rx_data))
    return np.array(bers), np.array(h_blocks)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════
def main():
    n_seeds = 30
    seeds = list(range(n_seeds))
    turbs = ['weak', 'moderate', 'strong']
    f_dot = DOPPLER_HIGH
    n_pilots = 5

    # ── C4 parameters ─────────────────────────────────────────
    BLOCK_SIZES = [20, 50, 100, 200, 500, 1000]
    Ns_c4 = 20000  # divisible by all block sizes
    gamma_bar = GAMMA_BAR_DEFAULT

    # ── C5 parameters ─────────────────────────────────────────
    Ns_c5 = 10000
    block_size_c5 = BLOCK
    DEEP_FADE_THRESHOLDS = [0.01, 0.05, 0.1, 0.2]

    results = {
        'params': {
            'C4': {'Ns': Ns_c4, 'block_sizes': BLOCK_SIZES, 'n_pilots': n_pilots,
                    'n_seeds': n_seeds, 'turbs': turbs},
            'C5': {'Ns': Ns_c5, 'block_size': block_size_c5,
                    'deep_fade_thresholds': DEEP_FADE_THRESHOLDS,
                    'n_seeds': n_seeds, 'turbs': turbs},
        },
        'C4_ber': {},        # {turb: {bs: mean_BER}}
        'C4_net_ber': {},    # {turb: {bs: net_BER}}
        'C5_deep_blocks': {},     # {turb: {threshold: fraction}}
        'C5_ber_kf_deep': {},     # {turb: {threshold: mean_BER}}
        'C5_ber_fixed_deep': {},  # {turb: {threshold: mean_BER}}
        'C5_ber_kf_normal': {},   # {turb: BER for h>=0.1}
        'C5_ber_fixed_normal': {},
    }

    t0 = time.time()

    # ═══════════════════════════════════════════════════════════
    # C4: Block size sweep
    # ═══════════════════════════════════════════════════════════
    print("=" * 70)
    print("C4: Block size sweep")
    print("=" * 70)
    for turb in turbs:
        results['C4_ber'][turb] = {}
        results['C4_net_ber'][turb] = {}
        for bs in BLOCK_SIZES:
            bers = []
            for seed in seeds:
                shared = generate_custom_block(Ns_c4, gamma_bar, turb, f_dot, seed, bs)
                ber = trial_c4(shared, n_pilots, bs)
                bers.append(ber)
            mean_ber = np.mean(bers)
            pilot_overhead = n_pilots / bs
            net_ber = mean_ber * (1 - pilot_overhead)
            results['C4_ber'][turb][str(bs)] = mean_ber
            results['C4_net_ber'][turb][str(bs)] = net_ber
            print(f"  {turb:>8s} | BS={bs:>5d} | overhead={pilot_overhead*100:>5.1f}% "
                  f"| BER={mean_ber:.4e} | net_BER={net_ber:.4e}")
    print()

    # ═══════════════════════════════════════════════════════════
    # C5: Deep fade analysis
    # ═══════════════════════════════════════════════════════════
    print("=" * 70)
    print("C5: Deep fade block analysis")
    print("=" * 70)
    for turb in turbs:
        # Accumulate per-block results across seeds
        all_block_ber_kf = []
        all_block_ber_fixed = []
        all_block_h = []

        for seed in seeds:
            shared = generate_shared_realization(Ns_c5, gamma_bar, turb, f_dot, seed)

            # KF pilot path
            rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
            rx_eq_kf = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
            corrected_kf, _ = kf_pilot_recovery(
                rx_eq_kf, gamma_bar, turb, n_pilots,
                shared['h_med'], f_dot, block_size=block_size_c5)
            blk_ber_kf, blk_h = per_block_ber_kf(
                corrected_kf, shared['bits'], shared['h_blocks'], block_size_c5, n_pilots)

            # Fixed path (no pilots, uses oracle h)
            rx_eq_fixed = equalize_oracle(shared)
            rx_fixed = carrier_recovery_fixed(rx_eq_fixed)
            blk_ber_fixed, _ = per_block_ber_fixed(
                rx_fixed, shared['bits'], shared['h_blocks'], block_size_c5)

            all_block_ber_kf.extend(blk_ber_kf)
            all_block_ber_fixed.extend(blk_ber_fixed)
            all_block_h.extend(blk_h)

        all_block_ber_kf = np.array(all_block_ber_kf)
        all_block_ber_fixed = np.array(all_block_ber_fixed)
        all_block_h = np.array(all_block_h)

        # Statistics per threshold
        results['C5_deep_blocks'][turb] = {}
        results['C5_ber_kf_deep'][turb] = {}
        results['C5_ber_fixed_deep'][turb] = {}

        print(f"\n  --- {turb} ---")
        print(f"  {'Thresh':>8s} | {'Deep%':>7s} | {'KF BER':>10s} | "
              f"{'Fixed BER':>10s} | {'Improv(dB)':>10s}")
        print("  " + "-" * 58)

        for thresh in DEEP_FADE_THRESHOLDS:
            deep_mask = all_block_h < thresh
            n_deep = np.sum(deep_mask)
            fraction = n_deep / len(all_block_h)

            if n_deep > 0:
                ber_kf_deep = np.mean(all_block_ber_kf[deep_mask])
                ber_fixed_deep = np.mean(all_block_ber_fixed[deep_mask])
                improvement_db = db_ratio(ber_fixed_deep, ber_kf_deep)
            else:
                ber_kf_deep = 0.0
                ber_fixed_deep = 0.0
                improvement_db = 0.0

            results['C5_deep_blocks'][turb][str(thresh)] = fraction
            results['C5_ber_kf_deep'][turb][str(thresh)] = ber_kf_deep
            results['C5_ber_fixed_deep'][turb][str(thresh)] = ber_fixed_deep

            print(f"  {thresh:>8.2f} | {fraction*100:>6.1f}% | {ber_kf_deep:>10.4e} | "
                  f"{ber_fixed_deep:>10.4e} | {improvement_db:>10.2f}")

        # Normal blocks (h >= 0.1) BER
        normal_mask = all_block_h >= 0.1
        ber_kf_normal = np.mean(all_block_ber_kf[normal_mask]) if np.any(normal_mask) else 0.0
        ber_fixed_normal = np.mean(all_block_ber_fixed[normal_mask]) if np.any(normal_mask) else 0.0
        results['C5_ber_kf_normal'][turb] = ber_kf_normal
        results['C5_ber_fixed_normal'][turb] = ber_fixed_normal
        improv_normal = db_ratio(ber_fixed_normal, ber_kf_normal)
        print(f"  {'h>=0.1':>8s} | {(1 - np.sum(all_block_h < 0.1)/len(all_block_h))*100:>6.1f}% | "
              f"{ber_kf_normal:>10.4e} | {ber_fixed_normal:>10.4e} | {improv_normal:>10.2f}")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")

    # ── Save JSON ──────────────────────────────────────────────
    json_path = os.path.join(OUT, 'results_kf_stress_C4C5.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {json_path}")

    # ═══════════════════════════════════════════════════════════
    # Plotting: 1x2 figure
    # ═══════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    turb_colors = {'weak': 'blue', 'moderate': 'green', 'strong': 'red'}
    turb_markers = {'weak': 'o', 'moderate': 's', 'strong': '^'}

    # Panel 0: C4 — BER vs block_size + net BER
    ax = axes[0]
    for turb in turbs:
        ber_vals = [results['C4_ber'][turb][str(bs)] for bs in BLOCK_SIZES]
        net_vals = [results['C4_net_ber'][turb][str(bs)] for bs in BLOCK_SIZES]
        ax.semilogy(BLOCK_SIZES, ber_vals, marker=turb_markers[turb],
                    color=turb_colors[turb], label=f'{turb} (raw)',
                    linewidth=1.5, linestyle='-')
        ax.semilogy(BLOCK_SIZES, net_vals, marker=turb_markers[turb],
                    color=turb_colors[turb], label=f'{turb} (net)',
                    linewidth=1.5, linestyle='--', alpha=0.7)
    ax.axvline(x=100, color='gray', linestyle=':', alpha=0.7, label='BS=100')
    ax.set_xlabel('Block size')
    ax.set_ylabel('BER')
    ax.set_title('C4: BER vs Block Size (raw & net)')
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')

    # Panel 1: C5 — deep fade BER comparison (grouped bars)
    ax = axes[1]
    x_pos = np.arange(len(DEEP_FADE_THRESHOLDS))
    bar_width = 0.13
    group_labels = [f'h<{t}' for t in DEEP_FADE_THRESHOLDS]

    for ti, turb in enumerate(turbs):
        kf_vals = [results['C5_ber_kf_deep'][turb][str(t)] for t in DEEP_FADE_THRESHOLDS]
        fix_vals = [results['C5_ber_fixed_deep'][turb][str(t)] for t in DEEP_FADE_THRESHOLDS]
        offset_kf = (2 * ti) * bar_width
        offset_fix = (2 * ti + 1) * bar_width
        ax.bar(x_pos + offset_kf, kf_vals, bar_width,
               color=turb_colors[turb], alpha=0.6,
               label=f'{turb} KF' if ti == 0 or True else '', hatch='')
        ax.bar(x_pos + offset_fix, fix_vals, bar_width,
               color=turb_colors[turb], alpha=0.9,
               label=f'{turb} Fixed' if ti == 0 or True else '', hatch='///')

    ax.set_xticks(x_pos + 3 * bar_width)
    ax.set_xticklabels(group_labels)
    ax.set_ylabel('BER')
    ax.set_title('C5: Deep Fade Block BER (KF pilot vs Fixed)')
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')

    fig.suptitle('KF Stress Test C4+C5: Block Size & Deep Fade', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig_path = os.path.join(OUT, 'fig_kf_stress_C4C5.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to {fig_path}")
    plt.close(fig)

    # ═══════════════════════════════════════════════════════════
    # Summary & PASS/FAIL
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("SUMMARY: C4 Block Size — Raw BER")
    print("=" * 70)
    header = f"{'Turb':>10s}"
    for bs in BLOCK_SIZES:
        header += f" | BS={bs:>5d}"
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        for bs in BLOCK_SIZES:
            row += f" | {results['C4_ber'][turb][str(bs)]:>7.1e}"
        print(row)

    print("\n" + "=" * 70)
    print("SUMMARY: C4 Block Size — Net BER (扣除导频开销)")
    print("=" * 70)
    print(header)
    print("-" * len(header))
    for turb in turbs:
        row = f"{turb:>10s}"
        for bs in BLOCK_SIZES:
            row += f" | {results['C4_net_ber'][turb][str(bs)]:>7.1e}"
        print(row)

    # C4 PASS/FAIL: BS=100 should be near optimal in net BER
    print("\n" + "=" * 70)
    print("C4 PASS/FAIL: BS=100 net BER near optimal?")
    print("=" * 70)
    c4_pass = True
    for turb in turbs:
        net_100 = results['C4_net_ber'][turb]['100']
        all_net = [results['C4_net_ber'][turb][str(bs)] for bs in BLOCK_SIZES]
        best_net = min(all_net)
        ratio = net_100 / best_net if best_net > 0 else float('inf')
        passed = ratio < 1.5
        if not passed:
            c4_pass = False
        print(f"  {turb:>8s}: net_BER(BS=100)={net_100:.4e}, "
              f"best={best_net:.4e}, ratio={ratio:.2f}x => {'PASS' if passed else 'FAIL'}")

    # C5 PASS/FAIL: deep fade (h<0.1) BER improvement > 3 dB
    print("\n" + "=" * 70)
    print("C5 PASS/FAIL: Deep fade (h<0.1) BER improvement > 3 dB?")
    print("=" * 70)
    c5_pass = True
    for turb in turbs:
        ber_kf = results['C5_ber_kf_deep'][turb]['0.1']
        ber_fix = results['C5_ber_fixed_deep'][turb]['0.1']
        improv_db = db_ratio(ber_fix, ber_kf)
        passed = improv_db > 3.0
        if not passed:
            c5_pass = False
        print(f"  {turb:>8s}: KF={ber_kf:.4e}, Fixed={ber_fix:.4e}, "
              f"improvement={improv_db:.1f} dB => {'PASS' if passed else 'FAIL'}")

    print("\n" + "=" * 70)
    print("OVERALL VERDICT")
    print("=" * 70)
    print(f"  C4 Block size: {'PASS' if c4_pass else 'FAIL'} "
          f"(BS=100 net BER within 1.5x of optimal)")
    print(f"  C5 Deep fade:  {'PASS' if c5_pass else 'FAIL'} "
          f"(h<0.1 blocks: KF improvement > 3 dB vs Fixed)")


if __name__ == '__main__':
    main()
