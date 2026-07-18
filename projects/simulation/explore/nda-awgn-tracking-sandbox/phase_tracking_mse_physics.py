# -*- coding: utf-8 -*-
"""物理验证: segmented vs VV 相位跟踪 MSE (直接测相位误差, 不经 BER).

目的: 验证物理推导预期——
  κ = N_seg·σ²_p 是决定 segmented vs VV 差异可见性的无维度量
  κ << 0.01: 持平 (段/窗内相位近常数)
  κ ~ 0.01-1: segmented 略优 (线性插值比矩形窗平均更贴 Wiener 轨迹)
  κ >> 1: 两者都失效, cycle slip / resolve 模糊主导

直接测相位跟踪 MSE = E[(φ̂(n) - θ(n))²], 跳过 demod/resolve/BER 链路,
暴露 BER 掩盖的微小相位精度差异.

纪律: 只改本 explore 目录, 复用 awgn_wiener_channel 生成真实 Wiener 相位,
seg/VV 恢复函数本地实现 (跟 parity_tuning_sweep 一致).
"""
import os
import sys
import json
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from common import m16apsk_mod  # noqa: E402
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402

KS = [1, 2, 4, 8, 16, 32, 64, 128]
NWS = [4, 8, 16, 32, 64, 128, 256]


def nda_seg_phase(seg, M0, K):
    """NDA-segmented 返回相位估计 (不乘回, 只返回 φ̂). 段间线性插值."""
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    seg_len = N // K
    raised = seg ** M0
    seg_phi = np.empty(K)
    seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k * seg_len, (k + 1) * seg_len
        seg_phi[k] = np.angle(raised[lo:hi].mean())
        seg_center[k] = (lo + hi) / 2.0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_raised = np.interp(t, seg_center, seg_phi_unw)
    return phi_raised / M0


def vv_phase(rx, M0, Nw):
    """VV 返回相位估计 φ̂ (滑窗 mean-angle /M0)."""
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    raised = rx ** M0
    amp = np.abs(raised)
    mask = amp > 1e8
    if np.any(mask):
        raised[mask] = raised[mask] / amp[mask] * 1e8
    ker = np.ones(Nw) / Nw
    avg = np.convolve(raised, ker, mode='same')
    return np.unwrap(np.angle(avg)) / M0


def phase_mse_over_block(rx_block, theta_true_block, M0, estimator, param):
    """单块相位跟踪 MSE: 估计 φ̂, 解 M0-fold 模糊 (找最近 2π/M0 旋转), 算 MSE.

    theta_true_block: 真实 Wiener 相位 (每符号). estimator: 'seg'/'vv'. param: K 或 Nw.
    返回 per-symbol (φ̂-θ)² 的均值.
    """
    if estimator == 'seg':
        phi_est = nda_seg_phase(rx_block, M0, param)
    else:
        phi_est = vv_phase(rx_block, M0, param)
    # 解 M0-fold 模糊: φ̂ 可能跟 θ 差 k·2π/M0, 找最优 k 使残差最小
    # 残差 r = φ̂ - θ - k·2π/M0, 选 k = round((φ̂-θ)·M0/(2π)) 逐符号
    diff = phi_est - theta_true_block
    k_rot = np.round(diff * M0 / (2 * np.pi))
    diff_resolved = diff - k_rot * 2 * np.pi / M0
    # 限制到主值区间检查 (大的 cycle slip 不计入, 跟踪阶段假设已锁)
    # 但这里全计入, 看 raw MSE
    return np.mean(diff_resolved ** 2)


def main():
    t0 = time.time()
    M0 = P.M0
    N_sym = P.N_BLOCKS * P.N_DFT  # 102400
    N_blk = P.N_BLOCKS
    N_DFT = P.N_DFT
    T_S = P.T_S

    print("=" * 100)
    print("物理验证: segmented vs VV 相位跟踪 MSE (直接测相位误差)")
    print(f"M0={M0}, N_DFT={N_DFT}, N_BLOCKS={N_blk}, N_sym={N_sym}")
    print(f"直接测 E[(φ̂-θ)²], 跳过 demod/resolve/BER, 暴露 BER 掩盖的微小差异")
    print("=" * 100)

    # 场景: AWGN, SNR=18dB (高 SNR 让估计噪声方差项小, 凸显偏差结构差异)
    # 扫线宽 [10,50,100,200,500,1000]kHz
    snr_db = 18.0
    linewidths = [10e3, 50e3, 100e3, 200e3, 500e3, 1000e3]
    n_seeds = 5

    results = []
    print(f"\nSNR={snr_db}dB, {n_seeds} seed 平均. MSE 单位 rad²")
    print(f"\n{'线宽kHz':>8} {'κ(K=8)':>10} |", end='')
    for K in KS:
        print(f"{'seg K'+str(K):>10}", end='')
    print(" |", end='')
    for Nw in NWS:
        print(f"{'VV Nw'+str(Nw):>10}", end='')
    print(" | " + f"{'seg最优':>8} {'VV最优':>8} {'比值':>6}")

    for lw in linewidths:
        sigma2_p = 2 * np.pi * lw * T_S
        # 多 seed 平均相位 MSE
        seg_mse = {K: [] for K in KS}
        vv_mse = {Nw: [] for Nw in NWS}
        for si in range(n_seeds):
            seed = P.SEED_AWGN + int(snr_db * 1000) + si * 999983
            rng = np.random.default_rng(seed + 7)
            bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
            tx = m16apsk_mod(bits)
            rx, phi_true = S.awgn_wiener_channel(tx, snr_db, seed, sigma2_p=sigma2_p)
            # 逐 N_DFT 块算相位 MSE (resolve 模糊用每块真实相位)
            for b in range(N_blk):
                lo, hi = b * N_DFT, (b + 1) * N_DFT
                rx_blk = rx[lo:hi]
                theta_blk = phi_true[lo:hi]
                for K in KS:
                    seg_mse[K].append(phase_mse_over_block(rx_blk, theta_blk, M0, 'seg', K))
                for Nw in NWS:
                    vv_mse[Nw].append(phase_mse_over_block(rx_blk, theta_blk, M0, 'vv', Nw))
        seg_mean = {K: float(np.mean(seg_mse[K])) for K in KS}
        vv_mean = {Nw: float(np.mean(vv_mse[Nw])) for Nw in NWS}
        seg_best_K = min(seg_mean, key=lambda k: seg_mean[k])
        vv_best_Nw = min(vv_mean, key=lambda n: vv_mean[n])
        ratio = seg_mean[seg_best_K] / vv_mean[vv_best_Nw] if vv_mean[vv_best_Nw] > 0 else 0
        kappa = 32 * sigma2_p  # K=8 N_seg=32 的 κ
        cat = 'seg赢' if ratio < 0.95 else ('持平' if ratio <= 1.05 else 'VV赢')
        print(f"{lw/1e3:>8.0f} {kappa:>10.4f} |", end='')
        for K in KS:
            print(f"{seg_mean[K]:>10.2e}", end='')
        print(" |", end='')
        for Nw in NWS:
            print(f"{vv_mean[Nw]:>10.2e}", end='')
        print(f" | {seg_mean[seg_best_K]:>8.2e} {vv_mean[vv_best_Nw]:>8.2e} {ratio:>6.3f} {cat}")
        results.append({
            'linewidth_hz': float(lw), 'linewidth_khz': float(lw/1e3),
            'sigma2_p': float(sigma2_p), 'snr_db': float(snr_db),
            'kappa_K8': float(kappa),
            'seg_mse_by_k': {int(k): v for k, v in seg_mean.items()},
            'vv_mse_by_nw': {int(n): v for n, v in vv_mean.items()},
            'seg_best_k': int(seg_best_K), 'seg_best_mse': seg_mean[seg_best_K],
            'vv_best_nw': int(vv_best_Nw), 'vv_best_mse': vv_mean[vv_best_Nw],
            'ratio_seg_over_vv': float(ratio), 'cat': cat,
        })

    elapsed = time.time() - t0
    out = {
        'meta': {
            'task': '物理验证: segmented vs VV 相位跟踪 MSE',
            'purpose': '验证 κ=N_seg·σ²_p 决定差异可见性; 直接测相位 MSE 暴露 BER 掩盖的差异',
            'snr_db': snr_db, 'n_seeds': n_seeds, 'n_blocks_per_seed': N_blk,
            'M0': M0, 'N_DFT': N_DFT, 'T_S': float(T_S),
            'mse_unit': 'rad²',
            'note': '高 SNR=18dB 让估计噪声方差项小, 凸显偏差结构差异; 多 seed 平均',
            'common_or_simulator_or_params_modified': False,
            'elapsed_sec': float(elapsed),
        },
        'results': results,
    }
    out_json = os.path.join(_HERE, '_phase_tracking_mse.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {elapsed:.1f}s")


if __name__ == '__main__':
    main()
