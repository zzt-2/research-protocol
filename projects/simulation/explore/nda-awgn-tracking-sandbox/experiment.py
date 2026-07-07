# -*- coding: utf-8 -*-
"""[DEPRECATED] NDA-ML 加块内相位跟踪 vs BPS — sandbox 实验.

**D-007 (2026-07-07) 后废弃**: 本脚本引用 P.CLW_B11/P.SIGMA2_P_B11 (B11 OFDM 场景参数),
这些字段已从 _b11_params.py 删除 (AWGN 改单载波统一 LASER_LW). 脚本不再可运行.
保留作历史记录 (S002 阶段 segK8 跟踪验证). 结论已沉淀到 sc_nda_ml_sim.ber_nda_awgn
(intra_block_tracking='segmented'). 详见 decisions.md D-007.

任务 (HANDOFF.md §2): 试 "给 NDA-ML 加逐符号/块内相位跟踪" 能否在 AWGN HD-FEC 段 (18dB)
追平 BPS. 只改本 sandbox 目录, 不动 common/ / simulator/ (守纪律 1, 2).

机制 (HANDOFF.md §1.2):
  NDA-ML 当前 AWGN 实现 = nda_ml_recovery(assume_df_zero=True): 整块 (256 sym) 升 M0=8
  次幂后做一次 mean-angle → 一个常相位 φ 补偿全块. 块内 Wiener PN 累积相位方差
  σ²_φ = 2π·CLW·T_S·N_block ≈ 0.032 rad → high SNR 段成主导 → BER floor 比 BPS 高.
  BPS: 滑窗 Nw=101 逐符号搜最佳相位 → 跟得上块内漂移.

两个候选改进 (HANDOFF.md §2.2):
  方案 1 (segmented mean-angle): 256 块切 K 段, 每段独立 mean-angle, 段间线性插值.
  方案 2 (sliding-window mean-angle): 升 M0 后做 Nw 滑窗 mean-angle → 逐符号相位
          (类 BPS 但用升幂去调制, 保留 NDA-ML 内核).

公平对照 (HANDOFF.md §2.3 + 纪律 2): 复用 common/ 的信道 (awgn_wiener_channel 复制自
sc_nda_ml_sim, 等价 MVE)、调制、BPS (bps_cpr_m16apsk 复制自 run_bps_ablation)、
resolve (resolve_m16apsk_blockwise 直接 import). 参数全从 _b11_params 读 (纪律 3).

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/experiment.py
  可选 --seeds N (默认 1 = MVE seed 快速看趋势; 5 = 复现主实验多种子统计)
"""
import os
import sys
import json
import time
import argparse

import numpy as np

# --- 路径: simulation 根 (与 sc_nda_ml_sim.py / run_bps_ablation.py 同构) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 核心算法从 common/ 导入 (守 TL-13 + 纪律 2: 复用, 不重写信道/调制/BPS)
from common import (  # noqa: E402
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
)
import _b11_params as P  # noqa: E402  (参数全溯源, 纪律 3)
import sc_nda_ml_sim as S  # noqa: E402  (复用 awgn_wiener_channel + ber_nda_awgn + ber_oracle_awgn)
import run_bps_ablation as BPS  # noqa: E402  (复用 bps_cpr_m16apsk + ber_bps_awgn)
from fair_comparison import snr_at_ber  # noqa: E402


# =============================================================================
# AWGN 信道 — 复用 sc_nda_ml_sim.awgn_wiener_channel (逻辑等价 MVE, 同 seed 派生)
# 守 TL-13 + 纪律 2: 不重写信道, 保证 NDA/BPS/oracle 用同一物理信道 (公平对照前提).
# =============================================================================
awgn_wiener_channel = S.awgn_wiener_channel


# =============================================================================
# 改进 NDA-ML 估计器 — 复制 common.nda_ml_recovery 的 assume_df_zero 分支后改.
# 不动 common/ (纪律 1). 升幂 mean-angle 内核保留 (纪律 Dead End: 不重写骨架).
# =============================================================================
def nda_ml_segmented(rx, M0, K):
    """方案 1: 块内分段 mean-angle + 段间线性插值.

    把 N 符号块切 K 段 (每段 N/K 符号), 每段独立升幂 mean-angle 估常相位, 段中心之间
    线性插值得逐符号相位轨迹 (端点外推/常数外推由 np.interp 的外推规则 = hold).

    数学:
      raised = rx^M0 (去调制, B11 行 75-77)
      每段 s_k: phi_raised_seg[k] = angle(raised[s_k].mean())  # 段内常相位近似
      段中心 t_k = (k+0.5)*N/K,  插值 phi_raised(t) 在 [0, N) 上,  /M0 还原.
      unwrap 处理: 段间 phi_raised 可能跨 2π, 用 np.unwrap 平滑后再插值.
    K=1 退化到现状 (整块 mean-angle). 参数: M0=8 (溯源 _b11_params.M0).
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    seg_len = N // K
    raised = rx ** M0
    # 每段 mean-angle (段内常相位)
    seg_phi = np.empty(K)
    seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k * seg_len, (k + 1) * seg_len
        seg_phi[k] = np.angle(raised[lo:hi].mean())
        seg_center[k] = (lo + hi) / 2.0
    # unwrap 段相位 (段间可能跨 2π) → 线性插值 → /M0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_raised = np.interp(t, seg_center, seg_phi_unw)
    phi_est = phi_raised / M0
    return rx * np.exp(-1j * phi_est), phi_est


def nda_ml_sliding(rx, M0, Nw):
    """方案 2: 块内滑窗 mean-angle (类 BPS 但用升幂去调制).

    升 M0 后对 raised=rx^M0 做 Nw 滑窗 mean (→ 滑窗内的角度平均, 等价于
    sum-raised 的 angle 滑窗), unwrap 后 /M0 得逐符号相位.

    数学:
      raised = rx^M0
      raised_sm = convolve(raised, ones(Nw)/Nw, 'same')  # 滑窗均值 (复数, 含幅度+相位)
      phi_raised(k) = angle(raised_sm(k))  # 逐符号相位
      unwrap → /M0.
    Nw=N 退化到整块 mean-angle (现状); Nw 小 → 噪声大但跟踪快.
    参数: M0=8, Nw 滑窗长 (奇数对称).
    """
    rx = np.asarray(rx, dtype=complex)
    raised = rx ** M0
    ker = np.ones(Nw) / Nw
    raised_sm = np.convolve(raised, ker, mode='same')
    phi_raised = np.unwrap(np.angle(raised_sm))
    phi_est = phi_raised / M0
    return rx * np.exp(-1j * phi_est), phi_est


# =============================================================================
# BER 评估: 逐块跑改进估计器 + resolve M0-fold 模糊 (守 D003, 同 NDA-ML 主流程).
# =============================================================================
def ber_nda_improved_awgn(rx, tx_bits, estimator, est_kwargs):
    """通用改进 NDA BER 评估. estimator(seg, M0, **est_kwargs) -> (rx_comp, phi). 逐块跑."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _ = estimator(seg, P.M0, **est_kwargs)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# SNR 扫描 (AWGN 单 seed, 同主实验 seed 派生)
# =============================================================================
def run_awgn_scan(n_blocks, snr_points, seed_base, configs):
    """跑多配置 (NDA-原 + 改进变体 + BPS + oracle) × SNR 扫描, 返回 BER 表.

    configs: list of (name, callable(rx, tx_bits) -> (n_err, n_bits))
    seed 派生同 sc_nda_ml_sim.run_awgn (保 §4.5 一致性): seed = seed_base + int(snr*1000).
    """
    N_sym = n_blocks * P.N_DFT
    print(f"[AWGN sandbox] N_sym={N_sym}/点, CLW={P.CLW_B11/1e3:.0f}kHz, "
          f"σ²_p={P.SIGMA2_P_B11:.2e}, M0={P.M0}, N_DFT={P.N_DFT}")
    hdr = f"{'SNR':>5}" + "".join(f"{name:>14}" for name, _ in configs)
    print(hdr)
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = awgn_wiener_channel(tx, snr, seed)
        row = {'snr_db': float(snr)}
        ber_str = f"{snr:>5.0f}"
        for name, fn in configs:
            ne, nb = fn(rx, bits) if name != 'oracle' else fn(rx, bits, phi_true)
            ber = ne / nb
            row[name] = float(ber)
            ber_str += f"{ber:>14.4e}"
        print(ber_str)
        per_snr.append(row)
    return per_snr


# =============================================================================
# 主
# =============================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=1,
                    help='seed 数 (1=只跑 MVE seed 看趋势; 5=复现主实验多种子统计)')
    ap.add_argument('--no-plot', action='store_true')
    args = ap.parse_args()
    t0 = time.time()

    # 候选配置 (HANDOFF §2.2): 方案 1 K=4/8/16; 方案 2 Nw=11/21/51/101.
    # 先小集合快看趋势 (single seed), 用户回来前完成.
    plan_k = [4, 8, 16]              # 方案 1 段数
    plan_nw = [21, 51, 101]          # 方案 2 滑窗 (101 对齐 BPS Nw)

    all_configs = [
        ('NDA-orig', lambda rx, tb: S.ber_nda_awgn(rx, tb)),
        ('BPS',      lambda rx, tb: BPS.ber_bps_awgn(rx, tb)),
        ('oracle',   None),  # 特殊处理 (需 phi_true)
    ]
    # 方案 1
    for K in plan_k:
        all_configs.append(
            (f'NDA-segK{K}',
             (lambda K: (lambda rx, tb: ber_nda_improved_awgn(rx, tb, nda_ml_segmented, {'K': K})))(K)))
    # 方案 2
    for Nw in plan_nw:
        all_configs.append(
            (f'NDA-swNw{Nw}',
             (lambda Nw: (lambda rx, tb: ber_nda_improved_awgn(rx, tb, nda_ml_sliding, {'Nw': Nw})))(Nw)))
    # oracle 占位补 callable
    for i, (name, _) in enumerate(all_configs):
        if name == 'oracle':
            all_configs[i] = ('oracle', lambda rx, tb, phi: S.ber_oracle_awgn(rx, tb, phi))

    seeds = list(range(args.seeds))
    seed_bases = [P.SEED_AWGN + i for i in seeds]
    print("=" * 110)
    print(f"NDA-ML 块内跟踪 sandbox: {args.seeds} seed × {len(P.SNR_AWGN_DB)} SNR 点 × "
          f"{len(all_configs)} 配置")
    print(f"方案 1 K ∈ {plan_k} (段内 mean-angle + 段间插值)")
    print(f"方案 2 Nw ∈ {plan_nw} (滑窗 mean-angle, 对标 BPS Nw=101)")
    print(f"seed_base: {seed_bases} (seed 0 = MVE seed)")
    print("=" * 110)

    raw = []
    for idx, sb in enumerate(seed_bases):
        print(f"\n########## seed {idx} (seed_base={sb}) ##########")
        raw.append(run_awgn_scan(P.N_BLOCKS, P.SNR_AWGN_DB, sb, all_configs))

    # 聚合 (mean over seeds)
    names = [name for name, _ in all_configs]
    agg = {n: [] for n in names}
    for per_snr in raw:
        for row in per_snr:
            for n in names:
                agg[n].append((row['snr_db'], row[n]))
    # mean per (snr, config)
    snrs_unique = sorted(set(s for s, _ in agg[names[0]]))
    mean_ber = {n: {s: 0.0 for s in snrs_unique} for n in names}
    count = {n: {s: 0 for s in snrs_unique} for n in names}
    for n in names:
        for s, b in agg[n]:
            mean_ber[n][s] += b
            count[n][s] += 1
    for n in names:
        for s in snrs_unique:
            mean_ber[n][s] /= max(count[n][s], 1)

    # 判定 (HANDOFF §0 成功判据): HD-FEC 18dB 处 NDA-改进 ≤ BPS.
    hdfec_snr = 18.0
    bps_at_hdfec = mean_ber['BPS'][hdfec_snr]
    nda_orig_at_hdfec = mean_ber['NDA-orig'][hdfec_snr]
    print("\n" + "=" * 110)
    print(f"判定 @ HD-FEC (SNR={hdfec_snr}dB, BER≈{P.HDFEC}):")
    print(f"  NDA-orig = {nda_orig_at_hdfec:.6f}   BPS = {bps_at_hdfec:.6f}   "
          f"oracle = {mean_ber['oracle'][hdfec_snr]:.6f}")
    print(f"  {'config':>14} {'BER@18dB':>12} {'vs BPS':>10} {'追平 BPS?':>10}")
    verdict = {}
    for n in names:
        b = mean_ber[n][hdfec_snr]
        diff = b - bps_at_hdfec
        catch = '✅' if (n not in ('BPS', 'oracle') and b <= bps_at_hdfec) else ''
        if n not in ('BPS', 'oracle'):
            verdict[n] = {'ber_hdfec': b, 'vs_bps': diff, 'catch_up': bool(catch)}
        print(f"  {n:>14} {b:>12.6f} {diff:>+10.6f} {catch:>10}")

    # 画图
    png_path = None
    if not args.no_plot:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 1, figsize=(8.5, 6))
            colors = {'NDA-orig': 'C0', 'BPS': 'C3', 'oracle': 'C2'}
            styles = {'NDA-orig': 'o-', 'BPS': 'D-', 'oracle': '^--'}
            for n in names:
                ys = [mean_ber[n][s] for s in snrs_unique]
                c = colors.get(n, None)
                ls = styles.get(n, None)
                # 改进变体: 方案 1 蓝色系, 方案 2 紫色系
                if c is None:
                    if n.startswith('NDA-segK'):
                        c, ls = 'C1', 's-'
                    elif n.startswith('NDA-swNw'):
                        c, ls = 'C4', 'v-'
                ax.semilogy(snrs_unique, ys, ls, color=c, label=n, lw=1.7, ms=5)
            ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')
            ax.axvline(hdfec_snr, color='gray', ls=':', alpha=0.5)
            ax.set_xlabel(r'$\gamma_d$ (dB)')
            ax.set_ylabel('BER')
            ax.set_title('NDA-ML 块内跟踪 vs BPS (AWGN + Wiener PN, CLW=500kHz)',
                         fontsize=10.5)
            ax.grid(True, which='both', alpha=0.3)
            ax.legend(fontsize=7.5, loc='best')
            ax.set_ylim(bottom=1e-4)
            fig.tight_layout()
            png_path = os.path.join(_HERE, '_curves.png')
            fig.savefig(png_path, dpi=120, bbox_inches='tight')
            plt.close(fig)
            print(f"\n[PNG] {png_path}")
        except Exception as e:
            print(f"(PNG skipped: {e})")

    # 落盘 JSON
    out = {
        'meta': {
            'task': 'NDA-ML 加块内相位跟踪 vs BPS (AWGN HD-FEC 段追平测试)',
            'mechanism': ('NDA-orig 整块 mean-angle (常相位) 没跟块内 Wiener PN 漂移; '
                          'BPS 滑窗逐符号跟踪. 试方案 1 分段插值 + 方案 2 滑窗 mean-angle.'),
            'success_criterion': f'改进 NDA BER @ 18dB ≤ BPS BER ({bps_at_hdfec:.6f})',
            'n_seeds': args.seeds,
            'seed_bases': seed_bases,
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_blocks': P.N_BLOCKS,
            'N_sym_per_point': P.N_SYM_PER_POINT,
            'CLW_B11': P.CLW_B11,
            'SIGMA2_P_B11': float(P.SIGMA2_P_B11),
            'sigma_phi_intra_block_rad': float(np.sqrt(P.SIGMA2_P_B11 * P.N_DFT)),
            'HDFEC': P.HDFEC,
            'plan_k_seg': plan_k,
            'plan_nw_sliding': plan_nw,
            'algorithm_source': ('channel=S.awgn_wiener_channel; BPS=BPS.ber_bps_awgn; '
                                 'resolve=common.resolve_m16apsk_blockwise; 改进 NDA 本地实现'),
            'common_modified': False,
            'elapsed_sec': float(time.time() - t0),
            'python': sys.executable,
            'numpy_version': np.__version__,
        },
        'mean_ber': {n: {str(s): mean_ber[n][s] for s in snrs_unique} for n in names},
        'raw_per_seed': raw,
        'verdict_at_hdfec': verdict,
        'bps_at_hdfec': bps_at_hdfec,
        'nda_orig_at_hdfec': nda_orig_at_hdfec,
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(_HERE, '_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(_to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"[保存] {out_json}")
    print(f"\n[耗时] {time.time() - t0:.1f} s")


def _to_jsonable(o):
    if isinstance(o, dict):
        return {k: _to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return _to_jsonable(o.tolist())
    return o


if __name__ == '__main__':
    main()
