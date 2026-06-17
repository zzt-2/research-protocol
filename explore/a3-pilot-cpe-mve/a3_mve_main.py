"""A3 §4a 维度 D MVE — 主扫描入口。

全扫描：3 湍流 × 6 SNR × 5 seed × 6 方法（M1a/M1b/M2/M3/M4/raw）
产出：a3_mve_results.json + 控制台摘要

运行：wsl -e bash -c "cd .../explore/a3-pilot-cpe-mve && ~/.venvs/torch/bin/python a3_mve_main.py"
"""
import json
import subprocess
import time
import numpy as np
from a3_channel import generate_shared_realization, ber_count
from a3_baselines import (fft_foe, m2_grid_search, m3_vv_grid,
                          m4_pasc_digital, m2_agc_dpll)
from a3_pilot_cpe import m1a_frame_header_pilot, m1b_frequency_tone

TURBS = ['weak', 'moderate', 'strong']
GAMMAS_DB = [-5, 0, 5, 10, 15, 20]
SEEDS = [42, 43, 44, 45, 46]
NS = 8192

# M1a 参数（frame-header pilot，P=4 fl=32）
M1A_P, M1A_FL = 4, 32
# M1b 参数（频域 tone，sp=4）
M1B_SP = 4


def run_single(turb, gdb, seed):
    """跑单个 (turb, γ, seed) 下所有方法。返回 dict。"""
    # raw + M2/M3 用无 pilot 信道
    ch_nopilot = generate_shared_realization(NS, gdb, turb, seed=seed, with_pilot_header=False)
    # M1a/M1b 用带 pilot 信道（frame_len 匹配）
    ch_m1a = generate_shared_realization(NS, gdb, turb, seed=seed,
                                          with_pilot_header=True, frame_len=M1A_FL)
    ch_m1b = generate_shared_realization(NS, gdb, turb, seed=seed,
                                          with_pilot_header=True, frame_len=M1B_SP)
    # 注意：不同 frame_len 的信道 pilot 位置不同，但 h/phi/noise 由 seed 决定，
    # 同 seed 下信道物理一致（只有 pilot 注入位置不同）——公平比较

    results = {}
    N = NS

    # raw：fft_foe 去多普勒，无 CPE
    f0 = fft_foe(ch_nopilot['rx_raw'], M=4)
    rx_raw = ch_nopilot['rx_raw'] * np.exp(-1j * f0 * np.arange(N))
    results['raw'] = {'ber': ber_count(ch_nopilot['tx'], rx_raw, resolve_ambiguity=True)}

    # M1a frame-header pilot
    rx_comp, phi_ref, cs_rate, params, dm = m1a_frame_header_pilot(ch_m1a, P=M1A_P, frame_len=M1A_FL)
    results['M1a'] = {'ber': ber_count(ch_m1a['tx'], rx_comp, data_mask=dm, resolve_ambiguity=True),
                       'cs_rate': cs_rate}

    # M1b 频域 tone
    rx_comp, phi_ref, cs_rate, params, dm = m1b_frequency_tone(ch_m1b, tone_spacing=M1B_SP)
    results['M1b'] = {'ber': ber_count(ch_m1b['tx'], rx_comp, data_mask=dm, resolve_ambiguity=True),
                       'cs_rate': cs_rate}

    # M2 AGC+DPLL（BER-based grid）
    res_m2 = m2_grid_search(ch_nopilot['rx_raw'], ch_nopilot['tx'])
    results['M2'] = {'ber': res_m2['ber'], 'bn_norm': res_m2['bn_norm'], 'zeta': res_m2['zeta']}

    # M3 VV（BER-based grid）
    res_m3 = m3_vv_grid(ch_nopilot['rx_raw'], ch_nopilot['tx'])
    results['M3'] = {'ber': res_m3['ber'], 'block_len': res_m3['block_len']}

    # M4 PASC 数字近似（用 M1b 的带 tone 信道，近似光域共轭补偿）
    # M4 简化：用 pilot tone 估相位后直接减（不 unwrap，不 PAPU）—— 近似 PASC
    f0_m4 = fft_foe(ch_m1b['rx_raw'], M=4)
    rx_defo_m4 = ch_m1b['rx_raw'] * np.exp(-1j * f0_m4 * np.arange(N))
    pilot_sym = (1+1j)/np.sqrt(2)
    pilot_idx_m4 = ch_m1b['pilot_idx']
    pilot_phase_m4 = np.angle(rx_defo_m4[pilot_idx_m4] / pilot_sym)
    # M4 不 unwrap，直接用原始相位（近似光域即时补偿，无 unwrap 锁定）
    phi_ref_m4 = np.interp(np.arange(N), pilot_idx_m4, pilot_phase_m4)
    rx_comp_m4 = rx_defo_m4 * np.exp(-1j * phi_ref_m4)
    dm_m4 = ch_m1b['data_bits_mask'].copy()
    results['M4'] = {'ber': ber_count(ch_m1b['tx'], rx_comp_m4, data_mask=dm_m4, resolve_ambiguity=True)}

    # oracle（理论下界）
    rx_oracle = ch_nopilot['rx_raw'] * np.exp(-1j * ch_nopilot['phi_total'])
    results['oracle'] = {'ber': ber_count(ch_nopilot['tx'], rx_oracle, resolve_ambiguity=True)}

    return results


def main():
    t_start = time.time()
    all_results = []
    total = len(TURBS) * len(GAMMAS_DB) * len(SEEDS)

    print(f"A3 §4a MVE 全扫描：{len(TURBS)}湍流 × {len(GAMMAS_DB)}SNR × {len(SEEDS)}seed = {total} 点")
    print(f"{'turb':<10}{'γ(dB)':<8}{'raw':<10}{'M1a':<10}{'M1b':<10}{'M2':<10}{'M3':<10}{'M4':<10}{'oracle':<10}")

    count = 0
    for turb in TURBS:
        for gdb in GAMMAS_DB:
            seed_results = {m: [] for m in ['raw', 'M1a', 'M1b', 'M2', 'M3', 'M4', 'oracle']}
            cs_results = {m: [] for m in ['M1a', 'M1b']}
            for seed in SEEDS:
                res = run_single(turb, gdb, seed)
                for m in seed_results:
                    seed_results[m].append(res[m]['ber'])
                for m in cs_results:
                    cs_results[m].append(res[m].get('cs_rate', 0))
                count += 1

            # 均值
            mean_ber = {m: float(np.mean(seed_results[m])) for m in seed_results}
            mean_cs = {m: float(np.mean(cs_results[m])) for m in cs_results}
            all_results.append({
                'turb': turb, 'gamma_db': gdb,
                'ber_mean': mean_ber,
                'ber_std': {m: float(np.std(seed_results[m])) for m in seed_results},
                'cs_rate_mean': mean_cs,
            })
            print(f"{turb:<10}{gdb:<8}{mean_ber['raw']:<10.5f}{mean_ber['M1a']:<10.5f}"
                  f"{mean_ber['M1b']:<10.5f}{mean_ber['M2']:<10.5f}{mean_ber['M3']:<10.5f}"
                  f"{mean_ber['M4']:<10.5f}{mean_ber['oracle']:<10.5f}")

    elapsed = time.time() - t_start

    # 元数据
    try:
        git_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd='.').decode().strip()[:12]
    except Exception:
        git_hash = 'unknown'

    output = {
        'metadata': {
            'git_hash': git_hash,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'elapsed_sec': round(elapsed, 1),
            'nsymbols': NS,
            'n_points': total,
            'turbs': TURBS,
            'gammas_db': GAMMAS_DB,
            'seeds': SEEDS,
            'm1a_params': {'P': M1A_P, 'frame_len': M1A_FL, 'overhead': M1A_P/M1A_FL},
            'm1b_params': {'tone_spacing': M1B_SP, 'overhead': 1.0/M1B_SP},
            'tl25_checklist': {
                'shared_channel': True,
                'regen_channel': True,
                'self_written': True,
                'baseline_optimized': True,
                'theory_first': True,
                'output_metadata': True,
            },
            'fidelity_note': (
                'Gamma-Gamma 块衰落近似 Paillier TURANDOT 波动光学（35 层相位屏）。'
                '保留：deep fade 瞬态/块间相位跳变/多普勒残余/AO 残余活塞相位（主导损伤）。'
                '省略：AO 闭环动态（静态 GG 近似）。'
                'AO 残余等效线宽：weak=30kHz/moderate=100kHz/strong=300kHz（对标 Paillier §IV-A/B 主导损伤）。'
                '调试教训：pilot 位置必须注入已知 pilot_sym（with_pilot_header=True），否则失效。'
            ),
        },
        'results': all_results,
    }

    with open('a3_mve_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n结果写入 a3_mve_results.json ({elapsed:.1f}s, git {git_hash})")

    # 理论预期检查（TL-20）
    print("\n=== 理论预期检查（TL-20）===")
    strong_10 = next(r for r in all_results if r['turb']=='strong' and r['gamma_db']==10)
    print(f"strong γ=10dB: M1b BER={strong_10['ber_mean']['M1b']:.5f}, "
          f"raw={strong_10['ber_mean']['raw']:.5f}, "
          f"oracle={strong_10['ber_mean']['oracle']:.5f}")
    m1b_gain = strong_10['ber_mean']['raw'] / max(strong_10['ber_mean']['M1b'], 1e-9)
    print(f"  M1b vs raw BER 改善比: {m1b_gain:.1f}x")
    print(f"  M1b CS rate: {strong_10['cs_rate_mean']['M1b']:.4f}")
    print(f"  M3 VV BER: {strong_10['ber_mean']['M3']:.5f} (应复现失效，>>M1b)")


if __name__ == '__main__':
    main()
