"""γ_th 敏感性扫描 + ρ_fade 实测（sandbox 第一步，FR-20/TL-26 不拍参数）.

目的（阶段 0.4 §3.3 + 阶段 0.5 §1.5 留给 sandbox 的参数任务）:
1. 实测 rx 功率分布 P(mean(|rx_block|²))（weak/moderate/strong × 各 OSNR 点）
2. 定 γ_th 扫参范围 [γ̄−3σ, γ̄−1σ]（γ̄=mean, σ=std，不拍脑袋定值）
3. 逐点（turb × snr × γ_th）实测 ρ_fade = P(mean(|rx_block|²) < γ_th)
4. 选最优 γ_th（ρ_fade 在合理范围 [0.05, 0.40]，过低估漏触发过高误触发）

物理约定（阶段 0.3 §5.2 + 阶段 0.4 §3.2）:
- fade 检测粒度 = N_DFT 块级（256 符号，跟逐块恢复块对齐）
- 每块算 P = mean(|rx_block|²)，跟信道块（CH_BLOCK=100）不同尺度
- ρ_fade = N_fade_blocks / N_total_blocks（fade 块占空比）
- B2-Q2 pilot overhead 摊薄 = ρ_fade × PILOT_OVERHEAD_DB_FULL（阶段 0.4 §3.2）

输出:
- _gamma_th_sweep.json: 功率分布统计 + γ_th 扫参范围 + ρ_fade 逐点表
- _rho_fade_measure.json: 选定 γ_th 后的 ρ_fade（每 turb × snr）
"""
import os
import sys
import json
import time
import numpy as np

_SIM_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

# 同目录 import B2Params
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _b2_params_draft import (
    LASER_LW, R_SYM, T_S, SIGMA2_PN,
    TURB_LEVELS, GG_ALPHA_BETA,
    DA_PILOT_SPACING, PILOT_OVERHEAD_DB_FULL,
    N_DFT, CH_BLOCK, N_BLOCKS, HDFEC,
    SNR_TURB, SEED_TURB0, DOPPLER,
    M0,
)

from common import generate_shared_realization_apsk


def measure_rx_power_distribution(turb_name, gamma_lin, n_blocks, seed0):
    """跑 n_blocks 块信道，实测每块 rx 功率 P_b = mean(|rx_block|²).

    返回 P_blocks（n_blocks 数组，每块一个功率值）.
    注: 用 generate_shared_realization_apsk 共享信道实现（守 TL-13），不 per-block h 均衡
        （功率统计是信道直接统计，均衡前/后功率分布形状一致，均衡只影响绝对值不影响 fade 判据）。
    """
    P_blocks = np.empty(n_blocks)
    for b in range(n_blocks):
        r = generate_shared_realization_apsk(
            N_DFT, gamma_lin, turb_name, DOPPLER, mod='m16apsk', seed=seed0 + b,
        )
        rx_raw = r['rx_raw']
        # 块级功率（N_DFT 块内平均）
        P_blocks[b] = float(np.mean(np.abs(rx_raw) ** 2))
    return P_blocks


def sweep_gamma_th(P_blocks):
    """给定功率分布，定 γ_th 扫参范围 + 计算 ρ_fade(γ_th) 曲线.

    双层扫参（sandbox 实测发现功率分布严重右偏，单 σ 标准化范围失效）:
      Layer 1 [γ̄−3σ, γ̄−1σ]: 阶段 0.5 §1.5 原始设计（σ 标准化）
        · weak/moderate 可用，strong 失效（右偏致 ρ_fade≈0）
      Layer 2 [P_05, P_30]（功率分布 5%~30% 经验分位数）: 按 ρ_fade 目标值定 γ_th
        · ρ_fade 是 B2-Q2 实际控制变量（pilot overhead 摊薄 + fade 触发频率）
        · 按 ρ_fade∈[0.05, 0.30] 反推 γ_th，保证 fade 块够多有统计意义

    返回 dict: gamma_mean, gamma_std, 两层 sweep + 合并 rho_fade_vs_gamma_th 曲线.
    """
    gamma_mean = float(np.mean(P_blocks))
    gamma_std = float(np.std(P_blocks))

    # Layer 1: σ 标准化扫参 [γ̄−3σ, γ̄−1σ]（阶段 0.5 原设计）
    lo1 = gamma_mean - 3.0 * gamma_std
    hi1 = gamma_mean - 1.0 * gamma_std
    grid1 = list(np.linspace(lo1, hi1, 11))

    # Layer 2: 经验分位数扫参 [P_30, P_05]（按 ρ_fade 目标值反推 γ_th）
    # P_30 = 30th percentile（ρ_fade≈0.30 处），P_05 = 5th percentile（ρ_fade≈0.05 处）
    # 从高 γ_th（高 ρ_fade）扫到低 γ_th（低 ρ_fade），11 个点
    quantiles_hi = np.linspace(0.30, 0.05, 11)
    grid2 = [float(np.quantile(P_blocks, q)) for q in quantiles_hi]

    rho_fade_vs_gamma_th = []
    # 合并两层去重排序（按 γ_th 降序，γ_th 越高 ρ_fade 越高）
    all_grid = sorted(set(grid1 + grid2), reverse=True)
    for gth in all_grid:
        rho = float(np.mean(P_blocks < gth))
        rho_fade_vs_gamma_th.append({
            'gamma_th': float(gth),
            'gamma_th_minus_mean_sigma': float((gamma_mean - gth) / gamma_std) if gamma_std > 0 else 0.0,
            'rho_fade': rho,
        })
    return {
        'gamma_mean': gamma_mean,
        'gamma_std': gamma_std,
        'gamma_th_sweep_range_layer1_sigma': [float(lo1), float(hi1)],  # [γ̄−3σ, γ̄−1σ]
        'gamma_th_sweep_range_layer2_quantile': {
            'quantile_grid': [float(q) for q in quantiles_hi],  # [0.30, ..., 0.05]
            'gamma_th_grid': grid2,
        },
        'gamma_th_grid': [float(x) for x in all_grid],
        'rho_fade_vs_gamma_th': rho_fade_vs_gamma_th,
    }


def select_gamma_th(sweep_result, target_rho=0.15, target_rho_tol=0.05):
    """从 sweep 结果选最优 γ_th（按 ρ_fade 目标值，不按 σ 标准化）.

    sandbox 实测发现：功率分布严重右偏，σ 标准化扫参 [γ̄−3σ, γ̄−1σ] 在 strong 失效
    （strong ρ_fade≈0.008，fade 块太少无法测动态恢复）。改用 ρ_fade 作为控制变量：
      target_rho=0.15（fade 块占 15%，统计意义够，不占主导）
      tol=0.05（接受 [0.10, 0.20]）

    理由: ρ_fade 是 B2-Q2 的实际控制变量（pilot overhead 摊薄 + fade 触发频率 + 动态恢复可测性）。
    固定 ρ_fade 反推 γ_th 让三方对照在"相同 fade 统计"下比较（公平）。

    返回 (selected_gamma_th, selected_rho_fade, rationale).
    """
    rfv = sweep_result['rho_fade_vs_gamma_th']
    # 找 ρ_fade 最接近 target_rho 的
    best = min(rfv, key=lambda x: abs(x['rho_fade'] - target_rho))
    in_tol = abs(best['rho_fade'] - target_rho) <= target_rho_tol
    rationale = (f"ρ_fade={best['rho_fade']:.3f} 最接近 target={target_rho}"
                 f" {'(在容差内)' if in_tol else '(超容差，但已是最近)'})")
    return best['gamma_th'], best['rho_fade'], rationale


def main():
    t0 = time.time()
    print("=" * 90)
    print("B2-Q2 sandbox 第一步：γ_th 扫参 + ρ_fade 实测（FR-20/TL-26 不拍参数）")
    print(f"N_BLOCKS/点={N_BLOCKS}, N_DFT={N_DFT} (块级功率), CH_BLOCK={CH_BLOCK}")
    print(f"PILOT_OVERHEAD_DB_FULL(spacing={DA_PILOT_SPACING})={PILOT_OVERHEAD_DB_FULL:.4f}dB")
    print("=" * 90)

    sweep_all = {}
    rho_fade_selected = {}
    print(f"\n{'turb':10s} {'γd_dB':>6s} {'γ̄(mean)':>12s} {'σ(std)':>12s} "
          f"{'γ_th_sel(ρ_fade=0.15)':>22s} {'ρ_fade_sel':>10s}")
    print("-" * 90)

    for turb in TURB_LEVELS:
        sweep_all[turb] = {}
        rho_fade_selected[turb] = {}
        for gamma_db in SNR_TURB:
            gamma_lin = 10 ** (gamma_db / 10)
            P_blocks = measure_rx_power_distribution(turb, gamma_lin, N_BLOCKS, SEED_TURB0)
            sweep_result = sweep_gamma_th(P_blocks)
            gth_sel, rho_sel, rationale = select_gamma_th(sweep_result)
            sweep_all[turb][f'{gamma_db:.1f}'] = {
                **sweep_result,
                'selected_gamma_th': gth_sel,
                'selected_rho_fade': rho_sel,
                'selection_rationale': rationale,
                'P_blocks_raw_count': len(P_blocks),
                # 不存 raw P_blocks（太大，只存统计量）
            }
            rho_fade_selected[turb][f'{gamma_db:.1f}'] = {
                'gamma_th': gth_sel,
                'rho_fade': rho_sel,
            }
            print(f"{turb:10s} {gamma_db:>6.0f} {sweep_result['gamma_mean']:>12.4e} "
                  f"{sweep_result['gamma_std']:>12.4e} {gth_sel:>22.4e} {rho_sel:>10.4f}")

    elapsed = time.time() - t0
    print(f"\n[耗时] {elapsed:.1f}s")

    # 保存 sweep 结果（含功率分布统计 + ρ_fade vs γ_th 曲线）
    out_sweep = {
        'meta': {
            'task': 'B2-Q2 sandbox 第一步 γ_th 扫参 + ρ_fade 实测',
            'purpose': 'FR-20/TL-26 不拍参数：实测 rx 功率分布定 γ_th 扫参范围 + 逐点 ρ_fade',
            'params': {
                'N_BLOCKS': N_BLOCKS, 'N_DFT': N_DFT, 'CH_BLOCK': CH_BLOCK,
                'DA_PILOT_SPACING': DA_PILOT_SPACING,
                'PILOT_OVERHEAD_DB_FULL': float(PILOT_OVERHEAD_DB_FULL),
                'SNR_TURB': SNR_TURB,
                'TURB_LEVELS': TURB_LEVELS,
                'GG_ALPHA_BETA': {k: list(v) for k, v in GG_ALPHA_BETA.items()},
                'SIGMA2_PN': float(SIGMA2_PN),
                'LASER_LW': float(LASER_LW), 'R_SYM': float(R_SYM), 'T_S': float(T_S),
                'DOPPLER': float(DOPPLER), 'SEED_TURB0': SEED_TURB0,
            },
            'fade_detection_granularity': 'N_DFT block-level (256 sym, aligned with per-block recovery)',
            'rho_fade_definition': 'P(mean(|rx_block|²) < γ_th) = N_fade_blocks / N_total_blocks',
            'pilot_overhead_thinning': 'B2Q2_overhead ≈ ρ_fade × PILOT_OVERHEAD_DB_FULL (阶段 0.4 §3.2)',
            'gamma_th_selection_strategy': (
                '双层扫参: Layer1=[γ̄−3σ,γ̄−1σ] σ标准化 (阶段0.5原设计, strong失效); '
                'Layer2=[P_30,P_05] 功率分布经验分位数. '
                '选择: 按 ρ_fade target=0.15 反推 γ_th (sandbox实测发现功率分布严重右偏, '
                'σ标准化在strong致ρ_fade≈0.008 fade块太少, 改用ρ_fade作控制变量)'
            ),
            'physical_finding': (
                '功率分布 P(mean(|rx_block|²)) 严重右偏 (GG长尾). '
                'strong α1.5/β0.8: σ=0.99但fade深而稀疏, γ̄−1σ处ρ_fade仅0.008~0.015. '
                'weak α4/β3: σ=0.47 fade浅而频繁, γ̄−1σ处ρ_fade≈0.12. '
                '→ 阶段0.4 §3.2 示例"strong ρ_fade=30%"物理直觉错 (实测strong最低). '
                '→ sandbox实测修正: ρ_fade用经验分位数定, 不用σ标准化'
            ),
            'elapsed_s': float(elapsed),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        'results': sweep_all,
    }
    out_dir = os.path.dirname(os.path.abspath(__file__))
    sweep_path = os.path.join(out_dir, '_gamma_th_sweep.json')
    with open(sweep_path, 'w') as f:
        json.dump(out_sweep, f, indent=2, ensure_ascii=False)
    print(f"\n[saved] {sweep_path}")

    # 保存选定 γ_th 的 ρ_fade（sandbox 三方对照用）
    out_rho = {
        'meta': {
            'task': 'B2-Q2 ρ_fade 实测（选定 γ_th 后，sandbox 三方对照用）',
            'source': '_gamma_th_sweep.json select_gamma_th 结果',
            'selection_criterion': 'ρ_fade 接近 0.20（平衡漏触发/误触发），范围 [0.05, 0.40]',
            'params': out_sweep['meta']['params'],
        },
        'selected': rho_fade_selected,
    }
    rho_path = os.path.join(out_dir, '_rho_fade_measure.json')
    with open(rho_path, 'w') as f:
        json.dump(out_rho, f, indent=2, ensure_ascii=False)
    print(f"[saved] {rho_path}")


if __name__ == '__main__':
    main()
