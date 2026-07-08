"""B3-Q2 sandbox 三方对照主脚本（§0.4 三方对照矩阵 + §0.4.5 分层 Go/Kill）。

对话 3a: 骨架搭建 + smoke test PASS。正式跑数在对话 3b。

三方对照（_fair_comparison_framework.md §0.4.2）:
    M1 传统分立 TS（祖师爷/弱 baseline）
    M2 jphot FSTS（公平对照基准——同 FS+FOE 算法结构）
    M3 B3-Q2 联合（M2 + CPE 联合 + Doppler 维度）
    M3a = M2 + CPE 联合（无 Doppler）→ CPE 贡献归因
    M3b = M2 + Doppler（独立 CPE）→ Doppler 贡献归因

场景（§0.4.3）:
    S1 单链路强湍 + Doppler（主场景）
    S2 单链路强湍无 Doppler（对照，验证 Doppler 增量）

指标:
    BER vs 接收光功率 @ HD-FEC 3.8e-3（主指标）
    FOE MSE（诊断）/ CPE RMSE（诊断）/ outage 概率（A5 补充）

fair gain（§0.4.2）:
    gain_vs_M1 = M1.BER - M3.BER（含 jphot 继承，仅参考）
    gain_vs_M2 = M2.BER - M3.BER（B3-Q2 真实增量，Go 判据）

分层 Go/Kill（§0.4.5）:
    L1 全条件: gain_vs_M2 > 0 全条件 + CPE/Doppler 贡献各≥10%
    L2 Doppler crossover: 扫 f_dot 找 M2/M3 交叉点
    L3 失效边界: jphot 高 Doppler 失效而 B3-Q2 仍工作

运行（对话 3b）: cd explore/b3-joint-estimation && python b3_joint_mve.py

守:
- 禁 baseline 只比传统 TS（必须含 jphot FSTS M2，否则增益是继承的）
- 禁 L1 全条件 FAIL 就直接 Kill（守 §0.4.5 分层，走 L2/L3）
- 禁用旧"4 支路 +2~3dB"数字（D002 修正：2 支路才 +2~3dB）
- 多 seed（adaptation-scan 防坑：物理因果 + 多 seed）
"""
import json
import os
import sys
import time

import numpy as np

# 路径
_SIM_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _b3_params import B3Params, B3SandboxConfig  # noqa: E402
from multi_aperture_channel import generate_multi_aperture_realization  # noqa: E402
from joint_estimation_pipeline import b3_joint_pipeline, estimate_block_df_sequence  # noqa: E402
from common._modulation import resolve_qpsk  # noqa: E402

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')


def ber_count(tx_bits, rx):
    """BER 统计（含 QPSK π/2 相位模糊 resolve）。"""
    return resolve_qpsk(rx, tx_bits)


def run_single_config(params, gamma_bar, f_dot, turb_name, n_branches,
                      modes, n_seeds=10, Ns=8192):
    """单配置（SNR + Doppler + 支路数 + 湍流）多 seed 三方对照。

    Returns:
        dict: 每个 mode 的 {ber_mean, ber_std, ber_per_seed, df_est_mean, f_dot_est_mean}
    """
    results = {m: {'ber_per_seed': [], 'df_est': [], 'f_dot_est': []} for m in modes}

    for seed in range(n_seeds):
        ch = generate_multi_aperture_realization(
            n_branches=n_branches, Ns=Ns, gamma_bar=gamma_bar,
            turb_name=turb_name, f_dot=f_dot,
            aperture_spacing_m=params.aperture_spacing_m,
            seed=seed, lw=params.lw_hz, f_res=params.f_res,
            cn2=params.cn2, z_km=params.z_km,
        )
        tx_bits = ch['bits']

        for mode in modes:
            # 传 h_branches 给 MRC（多支路用）
            params._h_branches = ch['h_branches'] if n_branches > 1 else None
            # 传 block-df 序列给 Doppler 估计（多块 f_dot 回归）
            if mode in ('full', 'm3b_doppler_only') and n_branches >= 1:
                params._block_df_sequence = estimate_block_df_sequence(
                    ch['branches'][0], params.ts_total, params.bl, params.bn
                )
            else:
                params._block_df_sequence = None

            out = b3_joint_pipeline(
                ch['branches'], ts_template=None, mode=mode,
                params=params, mod='qpsk',
            )
            ber = ber_count(tx_bits, out['rx_combined'])
            results[mode]['ber_per_seed'].append(ber)
            results[mode]['df_est'].append(
                np.mean(out['df_est']) if isinstance(out['df_est'], list) else out['df_est']
            )
            results[mode]['f_dot_est'].append(out['f_dot_est'])

    # 统计
    for mode in modes:
        bers = np.array(results[mode]['ber_per_seed'])
        results[mode]['ber_mean'] = float(np.mean(bers))
        results[mode]['ber_std'] = float(np.std(bers))
        results[mode]['df_est_mean'] = float(np.mean(results[mode]['df_est']))
        results[mode]['f_dot_est_mean'] = float(np.mean(results[mode]['f_dot_est']))

    return results


def run_sandbox_sweep():
    """§0.4.3 + §0.4.5: SNR 扫值 × Doppler 扫值 × 三方对照。"""
    params = B3Params()
    config = B3SandboxConfig()

    modes = list(config.modes)
    gamma_bar_sweep = [10 ** (db / 10) for db in params.gamma_bar_sweep_db]
    f_dot_sweep = params.f_dot_sweep

    all_results = {
        'meta': {
            'modes': modes,
            'gamma_bar_db': list(params.gamma_bar_sweep_db),
            'f_dot_sweep_hz': list(f_dot_sweep),
            'n_seeds': params.n_seeds,
            'scenes': list(config.scenes),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        'S1': {},  # 单链路强湍 + Doppler
        'S2': {},  # 单链路强湍无 Doppler
    }

    print("=" * 70)
    print("B3-Q2 sandbox 三方对照（对话 3b 正式跑数）")
    print("=" * 70)
    print(f"modes: {modes}")
    print(f"SNR sweep: {params.gamma_bar_sweep_db} dB")
    print(f"f_dot sweep: {[f'{x/1e6}MHz/s' if x>0 else '0' for x in f_dot_sweep]}")
    print(f"n_seeds: {params.n_seeds}")
    print()

    # S1: 单链路强湍 + Doppler 扫值（找 crossover）
    print("--- S1: 单链路强湍 + Doppler 扫值（L2 crossover 主轴）---")
    for f_dot in f_dot_sweep:
        print(f"\nf_dot = {f_dot/1e6 if f_dot>0 else 0} MHz/s:")
        all_results['S1'][f'fdot_{f_dot}'] = {}
        for gamma_db, gamma_bar in zip(params.gamma_bar_sweep_db, gamma_bar_sweep):
            t0 = time.time()
            res = run_single_config(
                params, gamma_bar, f_dot, 'strong', 1, modes,
                n_seeds=params.n_seeds,
            )
            all_results['S1'][f'fdot_{f_dot}'][f'snr_{gamma_db}dB'] = res
            # 简报
            m2_ber = res['m2_fsts']['ber_mean']
            full_ber = res['full']['ber_mean']
            gain_vs_m2 = m2_ber - full_ber
            elapsed = time.time() - t0
            print(f"  SNR={gamma_db:>3}dB: M2={m2_ber:.4f} M3={full_ber:.4f} "
                  f"gain_vs_M2={gain_vs_m2:+.4f} ({elapsed:.1f}s)")

    # S2: 单链路强湍无 Doppler（验证 Doppler 维度增量）
    print("\n--- S2: 单链路强湍无 Doppler（S1 fdot=0 即 S2，复用）---")
    all_results['S2'] = all_results['S1'].get('fdot_0.0', {})

    # 保存结果
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_file = os.path.join(RESULTS_DIR, 'b3_sandbox_results.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果保存到: {out_file}")

    return all_results


def compute_go_kill(results, params):
    """§0.4.5 分层 Go/Kill 判定。"""
    print("\n" + "=" * 70)
    print("分层 Go/Kill 判定（§0.4.5）")
    print("=" * 70)

    # L1 全条件: gain_vs_M2 > 0（S1 全 SNR 全 f_dot）
    l1_pass = True
    l1_details = []
    for fdot_key, snr_dict in results['S1'].items():
        for snr_key, res in snr_dict.items():
            m2 = res['m2_fsts']['ber_mean']
            full = res['full']['ber_mean']
            gain = m2 - full
            l1_pass = l1_pass and (gain > 0)
            l1_details.append((fdot_key, snr_key, gain))
    print(f"\nL1 全条件 (gain_vs_M2 > 0 全条件): {'PASS' if l1_pass else 'FAIL'}")
    n_positive = sum(1 for _, _, g in l1_details if g > 0)
    print(f"  gain_vs_M2 > 0 的配置: {n_positive}/{len(l1_details)}")

    if not l1_pass:
        print("\n  → L1 FAIL，进 L2（Doppler crossover）")
        # L2: 高 Doppler 区 gain_vs_M2 > 0？
        l2_signal = False
        for fdot_key in ['fdot_56000000.0', 'fdot_100000000.0']:  # 中、高 Doppler
            if fdot_key in results['S1']:
                for snr_key, res in results['S1'][fdot_key].items():
                    gain = res['m2_fsts']['ber_mean'] - res['full']['ber_mean']
                    if gain > 0:
                        l2_signal = True
                        print(f"  L2 信号: {fdot_key} @ {snr_key} gain_vs_M2={gain:+.4f}")
        print(f"\nL2 Doppler crossover: {'有信号' if l2_signal else '无信号'}")
        if not l2_signal:
            print("  → L2 无 crossover，进 L3（失效边界）—— 对话 3b 查 jphot 高 Doppler 是否失效")

    # 消融归因（CPE vs Doppler 贡献）
    print("\n--- 消融归因（§0.4.4，需 S1 全配置）---")
    # CPE 贡献 = M3a - M2, Doppler 贡献 = M3b - M2
    # 留对话 3b 正式算（需全配置数据）


def main():
    """对话 3a: 只跑骨架验证（小规模），对话 3b 跑全量。"""
    # 骨架验证：单配置快速跑通
    params = B3Params()
    params.n_seeds = 2  # 骨架验证用少量 seed
    params.gamma_bar_sweep_db = (0, 10)  # 骨架用 2 个 SNR 点
    params.f_dot_sweep = (0.0, 56e6)  # 骨架用 2 个 f_dot

    print("=== 对话 3a 骨架验证（小规模，正式跑数在 3b）===")
    results = run_sandbox_sweep()
    compute_go_kill(results, params)
    print("\n对话 3a 骨架验证完成。下一步（3b）: 全量 SNR×f_dot 扫值 + 多 seed + 消融归因")


if __name__ == '__main__':
    main()
