# -*- coding: utf-8 -*-
"""任务 1 验证: BPS M0=8 unwrap 数学正确性.

核查 run_bps_ablation.bps_cpr_m16apsk 的 unwrap (line 128-129):
  pe = np.unwrap(8*pe_raw)/8  (M0=8)

原理: BPS 测试相位 phases[b] = 2π·b/B. best_b 逐符号选最优 b → pe_raw = phases[best_b]
      是离散的, 相邻符号 best_b 可能跳 1 → pe_raw 跳 2π/B. 乘 M0=8 后跳变 = M0·2π/B.
      若 M0·2π/B = 2π·(M0/B) 接近 2π 整数倍, unwrap 才能正确解跳变 → 需要 B 整除 M0.

关键: B_BPS_M16 = 64, 64 能被 8 整除 → M0·2π/B = 8·2π/64 = π/4 = 2π/8 (非 2π 倍!).
      也就是说相邻 best_b 跳 1 → 8*pe_raw 跳 π/4, 不是 2π. unwrap 不会触发 (跳变 < π).
      真正的 2π 跳变: best_b 从 b_max (=B-1) 跳回 0 → pe_raw 跳 -2π·(B-1)/B ≈ -2π+2π/B.
      乘 8 后跳 ≈ -16π + 8·2π/B = -16π + π/4. unwrap 检测 -16π (距 2π 整数倍 = 2π·(-8)).
      mod 2π 残余 π/4 → < π → unwrap 会把 -16π 折叠回 0, 但留下 π/4 误差 → 这就是模糊!

正确性靠 resolve_m16apsk_blockwise 后处理 (试 8 个 2π/8 旋转). 本测试只测 BPS-CPR 本身
能否恢复已知相位 (在 resolve 之前), 用 "整块同一 φ_true + 无噪声" 构造.

注意 (8,8)-16APSK 升 M0=8 的两环相位差 π (内环 π, 外环 0): 升幂 mean-angle 法
(NDA) 会因两环抵消而失败, 但 BPS 是 "测试相位 + 最近邻判决", 不靠升幂 → 两环不抵消.
所以 BPS 跟 NDA 升幂法本质不同, 这里测的就是这个差异.
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from common import m16apsk_mod
import run_bps_ablation as BPS


def make_rx_no_noise(phi_true, N_sym=512, seed=0):
    """无噪声: rx = tx · exp(j·phi_true), tx 随机 (8,8)-16APSK."""
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, N_sym * 4)
    tx = m16apsk_mod(bits)
    rx = tx * np.exp(1j * phi_true)
    return rx, tx, bits


from common import resolve_m16apsk_blockwise, m16apsk_demod
import _b11_params as P


def main():
    print("=" * 78)
    print("任务 1: BPS M0=8 unwrap 数学正确性测试")
    print(f"B_BPS_M16 = {BPS.B_BPS_M16},  B % M0(8) = {BPS.B_BPS_M16 % 8}")
    print(f"Nw = {BPS.NW_BPS_M16}")
    print("=" * 78)

    # 注意: BPS 有 M0=8 相位模糊 (8 重), pe 与 phi_true 仅 mod 2π/8 相等.
    # 正确度量: (a) 模糊感知误差 = wrap(residual, π/4) 应 < 量化步长 2π/B = π/32;
    #           (b) 端到端 BER (BPS + resolve) 无噪声应 = 0.
    test_phases = [0.0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2,
                   np.pi, 2 * np.pi - 0.01, 2 * np.pi + 0.5]

    all_pass = True
    print(f"\n{'phi_true':>10} {'raw_resid':>10} {'ambig_err':>10} {'BER_e2e':>10} {'PASS':>6}")
    print("-" * 56)
    for phi_true in test_phases:
        rx, tx, bits = make_rx_no_noise(phi_true, N_sym=512, seed=1)
        rx_comp, pe = BPS.bps_cpr_m16apsk(rx)
        mean_pe = np.mean(pe)
        raw_resid = np.angle(np.mean(np.exp(1j * (phi_true - pe))))     # 含 M0 模糊
        ambig_err = (raw_resid + np.pi / 8) % (np.pi / 4) - np.pi / 8    # 折叠到 [-π/8,π/8)
        # 端到端: BPS + resolve → BER
        resolved = resolve_m16apsk_blockwise(rx_comp, bits, block_size=P.BLOCK_SIZE_RESOLVE)
        ber = np.mean(bits != m16apsk_demod(resolved))
        ok = abs(ambig_err) < np.pi / 32 + 0.01 and ber < 1e-3
        all_pass = all_pass and ok
        print(f"{phi_true:>10.4f} {raw_resid:>+10.4f} {ambig_err:>+10.5f} {ber:>10.2e} "
              f"{'✅' if ok else '❌':>6}")

    # 边界: phi_true = k·2π/8 ±ε, 测 unwrap 是否在跨模糊边界时产生 spurious 跳变
    print("\n--- unwrap 边界测试 (phi_true 跨 2π/8 整数倍 ±ε) ---")
    boundary_tests = [k * np.pi / 4 + eps for k in range(8) for eps in [-0.05, -0.02, 0.02, 0.05]]
    boundary_pass = True
    max_ambig = 0.0
    e2e_fail = 0
    for phi_true in boundary_tests:
        rx, tx, bits = make_rx_no_noise(phi_true, N_sym=512, seed=2)
        rx_comp, pe = BPS.bps_cpr_m16apsk(rx)
        raw_resid = np.angle(np.mean(np.exp(1j * (phi_true - pe))))
        ambig_err = (raw_resid + np.pi / 8) % (np.pi / 4) - np.pi / 8
        max_ambig = max(max_ambig, abs(ambig_err))
        resolved = resolve_m16apsk_blockwise(rx_comp, bits, block_size=P.BLOCK_SIZE_RESOLVE)
        ber = np.mean(bits != m16apsk_demod(resolved))
        if ber >= 1e-3:
            e2e_fail += 1
            boundary_pass = False
    print(f"  32 边界相位: max|ambig_err|={max_ambig:.5f} (量化步 π/32={np.pi/32:.5f}), "
          f"端到端 BER 失败数={e2e_fail}/32")

    # 关键: unwrap 是否引入 intra-block 相位斜坡? 无噪声恒相位下, pe 应块内恒定 (无斜坡)
    print("\n--- unwrap 块内一致性 (无噪声恒相位 → pe 应块内恒定) ---")
    rx, tx, bits = make_rx_no_noise(0.3, N_sym=512, seed=3)
    _, pe = BPS.bps_cpr_m16apsk(rx)
    pe_mid = pe[60:-60]   # 去边界效应
    intra_std = np.std(np.unwrap(8 * pe_mid) / 8)
    print(f"  phi_true=0.3: 块内 pe std (去边界) = {intra_std:.6f} rad "
          f"({'恒定 ✅' if intra_std < 1e-9 else '有跳变 ❌'})")

    print("\n" + "=" * 78)
    overall = all_pass and boundary_pass and intra_std < 1e-6
    print(f"任务 1 总结论: {'PASS ✅' if overall else 'FAIL ❌'}")
    print(f"  - B={BPS.B_BPS_M16} 能被 M0=8 整除: {BPS.B_BPS_M16 % 8 == 0}")
    print(f"  - 主测试 8 相位: ambig_err < π/32 且端到端 BER<1e-3: {all_pass}")
    print(f"  - 边界 32 相位端到端 BER 全过: {boundary_pass}")
    print(f"  - unwrap 块内无 spurious 斜坡: {intra_std < 1e-6}")
    print("=" * 78)
    return 0 if overall else 1


if __name__ == '__main__':
    sys.exit(main())
