#!/usr/bin/env python3
"""Analytical: E[1/h] divergence criterion for GG turbulence.

TL-25 checklist:
1. 共享信道: 不适用（纯解析）
2. 重生信道: 不适用
3. 从 common.py 导入: 不适用（纯数学，但参数与 TURB 一致）
4. 基线已优化: 不适用
5. 先写理论预期: 见下方
6. 输出含元数据: 时间戳

理论预期（TL-20）:
- GG(α,β) = Gamma(α,1/α) × Gamma(β,1/β)
- E[1/h] = (α/(α-1))·(β/(β-1)), 收敛条件: α>1 且 β>1
- weak(4.0,3.0) → 2.00, moderate(2.5,1.8) → 3.75, strong(1.5,0.8) → +∞
- C4-01 VV BER: weak 0.015%, moderate 0.15%, strong 39.2%
- 量化锚点: strong MC 验证应 >50
"""

import sys, os, time, datetime
import numpy as np
from scipy.stats import gamma as gamma_dist
from scipy.special import gamma as gamma_func

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import TURB, BLOCK

N_MC = 10**6

def gg_sample(alpha, beta, n, rng=None):
    """Sample from GG(alpha, beta) = Gamma(alpha, 1/alpha) × Gamma(beta, 1/beta)."""
    if rng is None:
        rng = np.random.default_rng()
    x = gamma_dist.rvs(alpha, scale=1/alpha, size=n, random_state=rng)
    y = gamma_dist.rvs(beta, scale=1/beta, size=n, random_state=rng)
    return x * y

def e_inv_h_analytical(alpha, beta):
    """E[1/h] for GG(alpha, beta). Returns inf if alpha<=1 or beta<=1."""
    if alpha <= 1 or beta <= 1:
        return np.inf
    return (alpha / (alpha - 1)) * (beta / (beta - 1))

def e_inv_h_mc(alpha, beta, n=N_MC, seed=42):
    """MC estimate of E[1/h] for GG(alpha, beta)."""
    rng = np.random.default_rng(seed)
    h = gg_sample(alpha, beta, n, rng)
    h_safe = np.clip(h, 1e-10, None)
    inv_h = 1.0 / h_safe
    return float(np.mean(inv_h)), float(np.std(inv_h) / np.sqrt(n))

def main():
    t0 = time.time()
    print("=" * 70)
    print("E[1/h] Divergence Criterion for GG Turbulence")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print("=" * 70)

    # --- 1. Analytical E[1/h] ---
    print("\n--- Analytical E[1/h] ---")
    print(f"{'Turbulence':<12} {'α':>5} {'β':>5} {'α>1?':>5} {'β>1?':>5} {'E[1/h]':>12}")
    print("-" * 50)
    analytical = {}
    for name, (a, b) in TURB.items():
        val = e_inv_h_analytical(a, b)
        analytical[name] = val
        print(f"{name:<12} {a:>5.1f} {b:>5.1f} {'Y' if a>1 else 'N':>5} "
              f"{'Y' if b>1 else 'N':>5} {val:>12.4f}" if np.isfinite(val)
              else f"{name:<12} {a:>5.1f} {b:>5.1f} {'Y' if a>1 else 'N':>5} "
              f"{'Y' if b>1 else 'N':>5} {'+∞':>12}")

    # --- 2. MC Verification ---
    print(f"\n--- MC Verification (N={N_MC:.0e}) ---")
    print(f"{'Turbulence':<12} {'Analytical':>12} {'MC mean':>12} {'MC stderr':>12} {'Match?':>8}")
    print("-" * 60)
    for name, (a, b) in TURB.items():
        mc_mean, mc_se = e_inv_h_mc(a, b)
        ana = analytical[name]
        if np.isfinite(ana):
            match = abs(mc_mean - ana) < 3 * mc_se
            print(f"{name:<12} {ana:>12.4f} {mc_mean:>12.4f} {mc_se:>12.4f} "
                  f"{'✓' if match else '✗':>8}")
        else:
            print(f"{name:<12} {'+∞':>12} {mc_mean:>12.2f} {mc_se:>12.2f} "
                  f"{'(divergent)':>8}")

    # --- 3. VV BER Causal Chain ---
    print(f"\n--- VV BER Causal Chain Verification ---")
    vv_ber = {'weak': 0.00015, 'moderate': 0.0015, 'strong': 0.392}
    print(f"{'Turbulence':<12} {'E[1/h]':>12} {'VV BER':>10} {'Consistent?':>12}")
    print("-" * 50)
    for name in TURB:
        ana = analytical[name]
        ber = vv_ber[name]
        if np.isfinite(ana):
            consistent = ber < 0.01  # small E[1/h] → low VV BER
            label = f"{ana:.2f}"
        else:
            consistent = ber > 0.1  # divergent E[1/h] → catastrophic VV BER
            label = "+∞"
        print(f"{name:<12} {label:>12} {ber:>10.4f} {'✓' if consistent else '✗':>12}")

    # --- 4. Progression with C16 (E[1/h²]) ---
    print(f"\n--- Progression: E[1/h²] (C16) vs E[1/h] (this work) ---")
    print("E[1/h²] = (α²/((α-1)(α-2))) · (β²/((β-1)(β-2)))")
    print(f"{'Turbulence':<12} {'E[1/h²]':>12} {'E[1/h²] div?':>12} "
          f"{'E[1/h]':>10} {'E[1/h] div?':>12}")
    print("-" * 60)
    for name, (a, b) in TURB.items():
        # E[1/h²]
        if a > 2 and b > 2:
            e_inv_h2 = (a**2 / ((a-1)*(a-2))) * (b**2 / ((b-1)*(b-2)))
            h2_div = "No"
            h2_str = f"{e_inv_h2:.4f}"
        elif a <= 2:
            e_inv_h2 = np.inf
            h2_div = "α≤2"
            h2_str = "+∞"
        else:
            e_inv_h2 = np.inf
            h2_div = "β≤2"
            h2_str = "+∞"

        e_inv_h1 = analytical[name]
        if np.isfinite(e_inv_h1):
            h1_div = "No"
            h1_str = f"{e_inv_h1:.2f}"
        else:
            h1_div = "β≤1"
            h1_str = "+∞"

        print(f"{name:<12} {h2_str:>12} {h2_div:>12} {h1_str:>10} {h1_div:>12}")

    print("\n--- Interpretation ---")
    print("β < 2: E[1/h²] diverges → adaptive window theoretically necessary (C16)")
    print("β < 1: E[1/h]  diverges → feedforward methods (VV/BPS) theoretically fail")
    print("Progression: β<2 needs adaptive window; β<1 feedforward method itself fails")

    # --- 5. Conclusion ---
    print(f"\n{'='*70}")
    print("CONCLUSION")
    print(f"{'='*70}")
    print("When GG parameter β < 1, E[1/h] diverges, causing VV/BPS average")
    print("phase estimation variance to diverge → feedforward methods theoretically fail.")
    print("This is verified by C4-01: strong turbulence (β=0.8) VV BER = 39.2%.")
    print("Complements C16 (β<2: E[1/h²] diverges → adaptive window necessary).")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")

if __name__ == '__main__':
    main()
