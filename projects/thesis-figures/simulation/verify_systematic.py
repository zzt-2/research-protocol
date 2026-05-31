#!/usr/bin/env python3
"""Track A 验证：sim_ch4_systematic_analysis.py 多种子鲁棒性测试"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import time

from sim_ch4_systematic_analysis import (
    generate_signal,
    chain_foe_vv, chain_foe_bps, chain_foe_dpll, chain_foe_dpll_vv,
    resolve_qpsk, ber_count,
    TURB, BLOCK,
)

def exp4_multi_seed(n_seeds=100, Ns=10000, gamma_bar_db=20):
    """Exp4 湍流总结 — 100 个独立种子"""
    turb_list = ['weak', 'moderate', 'strong']
    methods = ['FOE+VV', 'FOE+BPS', 'FOE+DPLL', 'FOE+DPLL+VV']
    results = {t: {m: [] for m in methods} for t in turb_list}

    t0 = time.time()
    for seed in range(n_seeds):
        for turb in turb_list:
            rx_eq, bits = generate_signal(Ns, turb, gamma_bar_db, seed=seed)

            for name, rx_corr in [('FOE+VV', chain_foe_vv(rx_eq)),
                                   ('FOE+BPS', chain_foe_bps(rx_eq)),
                                   ('FOE+DPLL', chain_foe_dpll(rx_eq)),
                                   ('FOE+DPLL+VV', chain_foe_dpll_vv(rx_eq))]:
                b = resolve_qpsk(rx_corr, bits)
                results[turb][name].append(b)

        if (seed + 1) % 20 == 0:
            print(f"  [{seed+1}/{n_seeds}] elapsed={time.time()-t0:.1f}s")

    print("\n" + "="*80)
    print(f"Exp4 多种子鲁棒性 ({n_seeds} seeds, Ns={Ns}, SNR={gamma_bar_db}dB)")
    print("="*80)

    for turb in turb_list:
        print(f"\n--- {turb.upper()} ---")
        for m in methods:
            bers = np.array(results[turb][m])
            fail_rate = np.mean(bers > 0.1)
            print(f"  {m:12s}: mean={np.mean(bers):.4e}  med={np.median(bers):.4e}  "
                  f"std={np.std(bers):.4e}  p5={np.percentile(bers,5):.4e}  "
                  f"p95={np.percentile(bers,95):.4e}  fail={fail_rate:.0%}  "
                  f"max={np.max(bers):.4e}")

    print("\n--- DPLL 增益分布 (dB) ---")
    for turb in turb_list:
        vv = np.array(results[turb]['FOE+VV'])
        bps = np.array(results[turb]['FOE+BPS'])
        dll = np.array(results[turb]['FOE+DPLL'])

        mask_v = (vv > 0) & (dll > 0)
        mask_b = (bps > 0) & (dll > 0)
        if np.sum(mask_v) > 0:
            g = 10*np.log10(vv[mask_v]/dll[mask_v])
            print(f"  {turb:8s} DPLL vs VV:  mean={np.mean(g):+.1f} med={np.median(g):+.1f} "
                  f"p5={np.percentile(g,5):+.1f} DPLL更好={np.mean(g>0):.0%}")
        if np.sum(mask_b) > 0:
            g = 10*np.log10(bps[mask_b]/dll[mask_b])
            print(f"  {turb:8s} DPLL vs BPS: mean={np.mean(g):+.1f} med={np.median(g):+.1f} "
                  f"p5={np.percentile(g,5):+.1f} DPLL更好={np.mean(g>0):.0%}")

    return results


if __name__ == '__main__':
    print("Track A 验证开始")
    t_start = time.time()
    results = exp4_multi_seed(n_seeds=100, Ns=10000, gamma_bar_db=20)
    print(f"\n总耗时: {time.time()-t_start:.1f}s")
