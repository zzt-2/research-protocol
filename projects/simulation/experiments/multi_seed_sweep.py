#!/usr/bin/env python3
"""多种子 SNR 扫描 — 论文级稳定数字

用法:
  ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py
  ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py --n-seeds 10 --n-symbols 5000
  ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py --methods VV DPLL --turbulence weak moderate

设计决策:
  - 从 common.py 导入所有方法实现，不自写信号处理
  - 使用 generate_shared_realization 保证同一 seed 下所有方法共享信道
  - Fixed 基线用 FIXED_CFG_OPTIMAL（按湍流等级选参数）
  - KF 使用导频辅助版本（kf_pilot），n_pilots=5
  - 所有方法统一用 resolve_qpsk 评估（SPEC §4.3）
  - 参数与 SPEC.md 完全一致（BLOCK=100, R_SYM=2.5e9 等）
  - 断点续跑：已完成 (snr, turb, method) 跳过
  - 中间结果每完成一个 (snr, turb) 对就落盘
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import numpy as np
from tqdm import tqdm

# 确保 common.py 可导入
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

from common import (
    BLOCK,
    DOPPLER_HIGH,
    FIXED_CFG_OPTIMAL,
    TURB,
    ber_eval,
    bps_cpr,
    carrier_recovery_fixed,
    fft_foe,
    generate_shared_realization,
    insert_pilots,
    kf_pilot_recovery,
    amp_limit,
    mmse_equalize,
    run_fixed,
    run_kf_pilot,
    vv_cpr,
    dpll_track,
    resolve_qpsk,
    qpsk_demod,
)

RESULTS_DIR = os.path.join(SIM_DIR, "results")


# ═══════════════════════════════════════════════════════════════
# 方法实现
# ═══════════════════════════════════════════════════════════════

def method_vv(shared):
    """FOE + VV 载波恢复"""
    from common import equalize_oracle
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_cpr, _ = vv_cpr(rx_foc, Nw=64)
    return rx_cpr


def method_bps(shared):
    """FOE + BPS 载波恢复"""
    from common import equalize_oracle
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_cpr, _ = bps_cpr(rx_foc)
    return rx_cpr


def method_dpll(shared):
    """FOE + DPLL 载波恢复"""
    from common import equalize_oracle
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_cpr, _ = dpll_track(rx_foc, omega_n=8e6, zeta=np.sqrt(2)/2)
    return rx_cpr


def method_kf_pilot(shared):
    """导频辅助 KF 载波恢复

    注意: KF pilot 需要插入导频，数据位置与原始比特不同。
    返回 (data_indices, data_bits) 以便正确评估。
    """
    corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots=5)
    return corrected, data_idx, data_bits


def method_fixed(shared, turb_name):
    """Fixed 基线（FOE+DPLL+VV），使用最优参数"""
    from common import equalize_oracle
    rx_eq = equalize_oracle(shared)
    cfg = FIXED_CFG_OPTIMAL[turb_name]
    return carrier_recovery_fixed(rx_eq, cfg=cfg)


# ═══════════════════════════════════════════════════════════════
# 单种子试验
# ═══════════════════════════════════════════════════════════════

METHOD_MAP = {
    'VV':      method_vv,
    'BPS':     method_bps,
    'DPLL':    method_dpll,
    'KF_pilot': method_kf_pilot,
}


def run_single_seed(Ns, gamma_bar, turb_name, method_name, seed):
    """运行单次种子试验，返回 BER。

    所有方法统一用 resolve_qpsk 评估（SPEC §4.3）。
    """
    shared = generate_shared_realization(
        Ns=Ns, gamma_bar=gamma_bar, turb_name=turb_name,
        f_dot=DOPPLER_HIGH, seed=seed,
    )

    if method_name == 'Fixed':
        rx = method_fixed(shared, turb_name)
        ber = ber_eval(shared['bits'], rx, mode='oracle')
    elif method_name == 'KF_pilot':
        corrected, data_idx, data_bits = method_kf_pilot(shared)
        ber = ber_eval(data_bits, corrected[data_idx], mode='oracle')
    else:
        fn = METHOD_MAP[method_name]
        rx = fn(shared)
        ber = ber_eval(shared['bits'], rx, mode='oracle')

    return ber


# ═══════════════════════════════════════════════════════════════
# 统计量计算
# ═══════════════════════════════════════════════════════════════

def compute_stats(ber_list, n_symbols):
    """计算 BER 统计量。

    置信区间: 正态近似（适用于 N>=30 且 BER 不极端接近 0 或 1 的场景）。
    对于 BER 极低的情况，Wilson score 区间更准确，此处用正态近似。
    """
    bers = np.array(ber_list)
    n = len(bers)
    mean = float(np.mean(bers))
    std = float(np.std(bers, ddof=1)) if n > 1 else 0.0

    # 95% 置信区间（正态近似）
    se = std / np.sqrt(n)
    ci_lo = max(0.0, mean - 1.96 * se)
    ci_hi = min(1.0, mean + 1.96 * se)

    # 失败率: BER > 10% 视为失败
    fail_rate = float(np.mean(bers > 0.10))

    return {
        'ber_mean': mean,
        'ber_std': std,
        'ci_95': [ci_lo, ci_hi],
        'fail_rate': fail_rate,
        'per_seed_ber': [float(b) for b in bers],
    }


# ═══════════════════════════════════════════════════════════════
# 断点续跑
# ═══════════════════════════════════════════════════════════════

def load_existing_results(output_path):
    """加载已有结果，用于断点续跑。"""
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            return json.load(f)
    return None


def is_completed(existing, method_name, turb_name, snr_db):
    """检查某个配置是否已完成。"""
    if existing is None:
        return False
    key = f"{method_name}_{turb_name}"
    if key not in existing.get('results', {}):
        return False
    snr_points = existing['results'][key].get('snr_points', [])
    for pt in snr_points:
        if pt['snr_db'] == snr_db:
            return True
    return False


def merge_result(existing, method_name, turb_name, snr_db, stats):
    """将单个配置结果合并到已有结果中。"""
    key = f"{method_name}_{turb_name}"
    if key not in existing['results']:
        existing['results'][key] = {'snr_points': []}

    snr_points = existing['results'][key]['snr_points']
    # 替换或追加
    replaced = False
    for i, pt in enumerate(snr_points):
        if pt['snr_db'] == snr_db:
            snr_points[i] = {'snr_db': snr_db, **stats}
            replaced = True
            break
    if not replaced:
        snr_points.append({'snr_db': snr_db, **stats})

    # 按 snr_db 排序
    existing['results'][key]['snr_points'].sort(key=lambda x: x['snr_db'])


def save_results(data, output_path):
    """原子写入 JSON 结果。"""
    tmp_path = output_path + '.tmp'
    with open(tmp_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, output_path)


# ═══════════════════════════════════════════════════════════════
# 主循环
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='多种子 SNR 扫描')
    parser.add_argument('--n-seeds', type=int, default=100,
                        help='每配置种子数 (default: 100)')
    parser.add_argument('--n-symbols', type=int, default=100000,
                        help='每种子符号数 (default: 100000)')
    parser.add_argument('--methods', nargs='+',
                        default=['VV', 'DPLL', 'KF_pilot', 'Fixed', 'BPS'],
                        choices=['VV', 'BPS', 'DPLL', 'KF_pilot', 'Fixed'],
                        help='要测试的方法')
    parser.add_argument('--turbulence', nargs='+',
                        default=['weak', 'moderate', 'strong'],
                        choices=['weak', 'moderate', 'strong'],
                        help='湍流等级')
    parser.add_argument('--snr-min', type=float, default=0,
                        help='最小 SNR (dB)')
    parser.add_argument('--snr-max', type=float, default=30,
                        help='最大 SNR (dB)')
    parser.add_argument('--snr-step', type=float, default=2,
                        help='SNR 步进 (dB)')
    parser.add_argument('--seed-base', type=int, default=1000,
                        help='种子基数 (default: 1000)')
    parser.add_argument('--resume', action='store_true',
                        help='从已有结果文件断点续跑')
    parser.add_argument('--output', type=str, default=None,
                        help='输出文件路径 (default: auto)')
    args = parser.parse_args()

    # SNR 范围
    snr_range = np.arange(args.snr_min, args.snr_max + 0.01, args.snr_step)
    n_snr = len(snr_range)

    # 输出文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if args.output:
        output_path = args.output
    else:
        output_path = os.path.join(RESULTS_DIR, f'sweep_{timestamp}.json')

    os.makedirs(RESULTS_DIR, exist_ok=True)

    # 加载已有结果（断点续跑）
    existing = None
    if args.resume:
        existing = load_existing_results(output_path)
        if existing:
            print(f"[续跑] 已加载 {output_path}")

    # 初始化结果结构
    if existing:
        results_data = existing
    else:
        results_data = {
            'metadata': {
                'timestamp': timestamp,
                'n_seeds': args.n_seeds,
                'n_symbols': args.n_symbols,
                'snr_range': [args.snr_min, args.snr_max, args.snr_step],
                'turbulence_levels': args.turbulence,
                'methods': args.methods,
                'seed_base': args.seed_base,
            },
            'results': {},
        }

    # 总配置数
    total_configs = len(args.methods) * len(args.turbulence) * n_snr
    completed = 0
    skipped = 0

    print(f"=== 多种子 SNR 扫描 ===")
    print(f"  方法: {args.methods}")
    print(f"  湍流: {args.turbulence}")
    print(f"  SNR: {args.snr_min:.0f} ~ {args.snr_max:.0f} dB, step {args.snr_step:.0f} dB ({n_snr} 点)")
    print(f"  种子: {args.n_seeds}/配置, {args.n_symbols} 符号/种子")
    print(f"  总配置: {total_configs}")
    print(f"  输出: {output_path}")
    print()

    # 外层循环: (turbulence, snr) — 每完成一对就落盘
    pbar_outer = tqdm(
        [(t, s) for t in args.turbulence for s in snr_range],
        desc="SNR sweep", unit="cfg", ncols=100,
    )

    for turb_name, snr_db in pbar_outer:
        gamma_bar = 10 ** (snr_db / 10)

        for method_name in args.methods:
            # 断点续跑检查
            if is_completed(results_data, method_name, turb_name, snr_db):
                skipped += 1
                completed += 1
                continue

            pbar_outer.set_postfix(
                method=method_name, turb=turb_name[:3], snr=f"{snr_db:.0f}dB"
            )

            # 多种子并行
            ber_list = []
            for seed_idx in range(args.n_seeds):
                seed = args.seed_base + seed_idx
                ber = run_single_seed(
                    Ns=args.n_symbols,
                    gamma_bar=gamma_bar,
                    turb_name=turb_name,
                    method_name=method_name,
                    seed=seed,
                )
                ber_list.append(ber)

            # 计算统计量
            stats = compute_stats(ber_list, args.n_symbols)

            # 合并到结果
            merge_result(results_data, method_name, turb_name, snr_db, stats)
            completed += 1

            # 每个配置落盘（防止中断丢失）
            save_results(results_data, output_path)

    # 最终保存
    save_results(results_data, output_path)

    print(f"\n=== 完成 ===")
    print(f"  完成: {completed}/{total_configs} 配置")
    print(f"  跳过(已完成): {skipped}")
    print(f"  输出: {output_path}")


if __name__ == '__main__':
    main()
