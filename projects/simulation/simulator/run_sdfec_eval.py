# -*- coding: utf-8 -*-
"""SD-FEC 阈值评估 (纯后处理, 不重跑仿真).

导师要求: 当前 HD-FEC BER=3.8e-3 (7% 开销) 阈值过低, 须补 SD-FEC (软判决 FEC) 阈值评估.
本脚本把已有主实验 raw BER 曲线 (sc_nda_ml_main/_main_experiment_5seed.json) 拿过来,
在多个 BER 阈值下重新算 fair gain (γ_tot 坐标). 不改任何仿真代码, 不重跑 BER.
注: D-007 (2026-07-07) 后真相源从 sc_nda_ml_main_improved 迁到 sc_nda_ml_main.

阈值网格 (见 brief):
  - pre-FEC BER: [1e-2, 1.5e-2, 2e-2, 2.5e-2]  (覆盖 20-30% SD-FEC 开销; 25% SD-FEC ≈ 2e-2)
  - HD-FEC 3.8e-3 (7% 开销): 对照档, 必须和主实验 _fair_gain_summary.json 完全一致 (sanity check)
  - post-FEC BER 1e-7: 参考, 大概率不可达 (BER floor 远高于此), 如实记录

公平 gain 定义 (同主实验, γ_tot 坐标):
  gain@target_BER = (DA γ_tot @ target) − (NDA γ_tot @ target)
                  = (γ_d_da@target + pilot_overhead) − γ_d_nda@target
  正 = NDA 赢. pilot_overhead = 1.249 dB (spacing=4, 25% pilot), 与 FEC 开销无关 (载波同步层开销).

统计 (同主实验): 每 seed 独立算 gain (analyze_fair_gain), 再 5 seed 统计 mean±CI (t 分布 df=n-1).
"""
import os
import sys
import json

import numpy as np

# --- 路径 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import _b11_params as P  # noqa: E402
from fair_comparison import analyze_fair_gain  # noqa: E402
from scipy import stats  # noqa: E402

# --- 输入 / 输出 ---
# D-007 (2026-07-07) 后主实验真相源从 sc_nda_ml_main_improved（旧 25GBaud/500kHz AWGN）
# 迁到 sc_nda_ml_main（统一 2.5GBaud/10kHz 全场景）。sdfec 是后处理，重跑会读新数据。
RAW_JSON = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main',
                        '_main_experiment_5seed.json')
MAIN_FAIR_JSON = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main',
                              '_fair_gain_summary.json')
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_sdfec_eval')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
SCENES = ['awgn', 'weak', 'moderate', 'strong']

# --- BER 阈值网格 ---
# pre-FEC: 覆盖 20-30% SD-FEC 开销; 25% SD-FEC (Staircase/LDPC) ≈ 2e-2.
# HD-FEC 3.8e-3: 7% 开销, 对照档 (必须复现主实验).
# post-FEC 1e-7: 参考, 大概率不可达.
BER_THRESHOLDS = [
    {'ber': 3.8e-3, 'label': 'HD-FEC_7pct_3.8e-3', 'kind': 'hdfec_ref',
     'note': 'HD-FEC 7% 开销; 对照档, 必须复现主实验 _fair_gain_summary.json'},
    {'ber': 1e-2,   'label': 'SD-FEC_preFEC_1e-2',  'kind': 'pre_fec',
     'note': 'pre-FEC BER; ~低开销 SD-FEC 区间'},
    {'ber': 1.5e-2, 'label': 'SD-FEC_preFEC_1.5e-2', 'kind': 'pre_fec',
     'note': 'pre-FEC BER; ~20% SD-FEC 开销'},
    {'ber': 2e-2,   'label': 'SD-FEC_preFEC_2e-2',  'kind': 'pre_fec',
     'note': 'pre-FEC BER; 25% SD-FEC (Staircase/LDPC) 典型容限 (DVB-S2X 25%)'},
    {'ber': 2.5e-2, 'label': 'SD-FEC_preFEC_2.5e-2', 'kind': 'pre_fec',
     'note': 'pre-FEC BER; ~30% SD-FEC 开销'},
    {'ber': 1e-7,   'label': 'post-FEC_1e-7',       'kind': 'post_fec',
     'note': 'post-FEC BER; 参考, 大概率不可达 (BER floor 远高于此)'},
]


def ci_t(data):
    """95% CI 半宽 (t 分布, df=n-1). 返回 (mean, std, ci_half_width, ci_low, ci_high). 复用主实验逻辑."""
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a))
    std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    if n > 1:
        tval = float(stats.t.ppf(0.975, n - 1))
        hw = tval * std / np.sqrt(n)
    else:
        hw = 0.0
    return mean, std, hw, mean - hw, mean + hw


def reconstruct_per_seed(summary):
    """从 summary[sc]['points'] (含 per_seed BER) 重建 per-seed per_snr 曲线.

    返回 raw[sc][seed_i] = list of dict(snr_db/nda_ml_ber/da_ml_ber/oracle_ber),
    与主实验 analyze_fair_gain 输入格式完全一致.
    """
    raw = {}
    for sc in SCENES:
        pts = summary[sc]['points']
        raw[sc] = {}
        for seed_i in range(N_SEEDS):
            per_snr = [{
                'snr_db': p['snr_db'],
                'nda_ml_ber': p['per_seed']['nda_ml_ber'][seed_i],
                'da_ml_ber': p['per_seed']['da_ml_ber'][seed_i],
                'oracle_ber': p['per_seed']['oracle_ber'][seed_i],
            } for p in pts]
            raw[sc][seed_i] = per_snr
    return raw


def eval_threshold(raw, ber_target, pilot_overhead_db):
    """对单一 BER 阈值: 每 scene 每 seed 独立算 fair gain, 再统计.

    返回 {scene: {per_seed_gain_db, gain_mean, gain_std, gain_ci95, n_valid, reachable_flags, ...}}.
    reachable: per-seed 是否可达该阈值 (NDA 和 DA 都达得到).
    """
    out = {}
    for sc in SCENES:
        gains = []
        reachable_flags = []      # per-seed reachability (both NDA & DA reach threshold)
        min_nda_per_seed = []     # per-seed min NDA BER (BER floor proxy)
        min_da_per_seed = []
        for seed_i in range(N_SEEDS):
            per_snr = raw[sc][seed_i]
            fg = analyze_fair_gain(per_snr, ber_target, pilot_overhead_db)
            g = fg['gain_nda_vs_da_fair_db']
            gains.append(g)
            reachable_flags.append(bool(fg['hdfec_reachable']))
            min_nda_per_seed.append(float(fg['min_nda_ber']))
            min_da_per_seed.append(float(np.min(
                [p['da_ml_ber'] for p in per_snr])))
        entry = {
            'per_seed_gain_db': [None if g is None else float(g) for g in gains],
            'per_seed_reachable': reachable_flags,
            'n_valid_seeds': int(sum(reachable_flags)),
        }
        valid = [g for g in gains if g is not None]
        if len(valid) >= 2:
            m, s, hw, lo, hi = ci_t(valid)
            entry.update({
                'gain_mean_db': m, 'gain_std_db': s,
                'gain_ci95_db': [lo, hi], 'gain_ci_halfwidth_db': hw,
            })
        else:
            entry.update({'gain_mean_db': None, 'gain_std_db': None,
                          'gain_ci95_db': [None, None], 'gain_ci_halfwidth_db': None})
        # BER floor 信息 (per-seed min BER; 取跨 seed 的最小/最大做区间)
        entry['ber_floor'] = {
            'min_nda_ber_per_seed': min_nda_per_seed,
            'min_da_ber_per_seed': min_da_per_seed,
            'min_nda_ber_overall': float(min(min_nda_per_seed)),
            'min_da_ber_overall': float(min(min_da_per_seed)),
            'threshold': float(ber_target),
            'reachable_overall': all(reachable_flags),
            'reachable_any': any(reachable_flags),
        }
        out[sc] = entry
    return out


def main():
    print("=" * 100)
    print("SD-FEC 阈值评估 (纯后处理, 不重跑仿真)")
    print(f"raw BER: {RAW_JSON}")
    print(f"pilot_overhead_db = {float(P.PILOT_OVERHEAD_DB):.4f} (spacing=4, 25% pilot, 与 FEC 开销无关)")
    print(f"BER 阈值: {[t['ber'] for t in BER_THRESHOLDS]}")
    print("=" * 100)

    with open(RAW_JSON, 'r', encoding='utf-8') as f:
        d = json.load(f)
    summary = d['summary']

    # 重建 per-seed raw
    raw = reconstruct_per_seed(summary)

    # --- sanity check: HD-FEC 3.8e-3 必须复现主实验 ---
    print("\n[SANITY] HD-FEC 3.8e-3 复现核查 (vs 主实验 _fair_gain_summary.json) ...")
    with open(MAIN_FAIR_JSON, 'r', encoding='utf-8') as f:
        main_fair = json.load(f)
    hdfec_result = eval_threshold(raw, P.HDFEC, P.PILOT_OVERHEAD_DB)
    sanity_report = {'pass': True, 'max_abs_diff_db': 0.0, 'per_scene': {}}
    for sc in SCENES:
        mine = hdfec_result[sc]
        ref = main_fair['fair_gain'][sc]
        mine_per_seed = mine['per_seed_gain_db']
        ref_per_seed = ref['per_seed_gain_db']
        diffs = []
        for ms, rs in zip(mine_per_seed, ref_per_seed):
            if ms is None and rs is None:
                diffs.append(0.0)
            elif ms is None or rs is None:
                diffs.append(None)
            else:
                diffs.append(abs(ms - rs))
        valid_diffs = [x for x in diffs if x is not None]
        sc_max = max(valid_diffs) if valid_diffs else 0.0
        sanity_report['per_scene'][sc] = {
            'mine_per_seed_gain_db': mine_per_seed,
            'ref_per_seed_gain_db': ref_per_seed,
            'per_seed_abs_diff_db': diffs,
            'max_abs_diff_db': sc_max,
            'mine_gain_mean_db': mine.get('gain_mean_db'),
            'ref_gain_mean_db': ref.get('gain_mean_db'),
            'mean_abs_diff_db': (abs(mine['gain_mean_db'] - ref['gain_mean_db'])
                                 if mine.get('gain_mean_db') is not None
                                 and ref.get('gain_mean_db') is not None else None),
        }
        sanity_report['max_abs_diff_db'] = max(sanity_report['max_abs_diff_db'], sc_max)
        sanity_report['pass'] = sanity_report['pass'] and (sc_max < 1e-9)
        print(f"  {sc:>10}: max per-seed |Δ| = {sc_max:.3e} dB  "
              f"{'OK' if sc_max < 1e-9 else 'MISMATCH'}")
    status = 'PASS' if sanity_report['pass'] else 'FAIL'
    print(f"  SANITY 总体: {status} (全局 max |Δ| = {sanity_report['max_abs_diff_db']:.3e} dB)")

    # --- 全阈值评估 ---
    print("\n[EVAL] 全 BER 阈值评估 ...")
    all_thresholds = []   # 列表, 保留顺序
    for tdef in BER_THRESHOLDS:
        res = eval_threshold(raw, tdef['ber'], P.PILOT_OVERHEAD_DB)
        all_thresholds.append({
            'ber': float(tdef['ber']),
            'label': tdef['label'],
            'kind': tdef['kind'],
            'note': tdef['note'],
            'results': res,
        })
        print(f"  --- BER={tdef['ber']:.0e} ({tdef['label']}) ---")
        for sc in SCENES:
            e = res[sc]
            bf = e['ber_floor']
            if e.get('gain_mean_db') is not None:
                ci = e['gain_ci95_db']
                print(f"    {sc:>10}: gain={e['gain_mean_db']:+.4f}±{e['gain_std_db']:.4f} dB "
                      f"CI[{ci[0]:+.4f},{ci[1]:+.4f}]  n_valid={e['n_valid_seeds']}/5  "
                      f"reachable={bf['reachable_overall']}")
            else:
                print(f"    {sc:>10}: UNREACHABLE  min_NDA_BER={bf['min_nda_ber_overall']:.3e}  "
                      f"min_DA_BER={bf['min_da_ber_overall']:.3e}  n_valid={e['n_valid_seeds']}/5")

    # --- 构建 _sdfec_gain_summary.json ---
    gain_summary = {
        'meta': {
            'task': 'SD-FEC 阈值 fair gain 评估 (纯后处理, 不重跑仿真)',
            'source_raw': os.path.relpath(RAW_JSON, _SIM_ROOT),
            'source_main_fair': os.path.relpath(MAIN_FAIR_JSON, _SIM_ROOT),
            'gain_definition': ('fair_gain@target_BER = (DA γ_tot @ target) − (NDA γ_tot @ target); '
                                '正=NDA赢; γ_tot_da=γ_d_da+pilot_overhead, γ_tot_nda=γ_d_nda'),
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'pilot_overhead_note': ('spacing=4 → 10·log10(4/3)=1.249 dB (25% pilot). '
                                    '这是载波同步层开销, 与 FEC 开销 (7%/20%/25%/30%) 是两回事, '
                                    'pre-FEC BER 阈值下 DA 仍须加此 overhead.'),
            'stat_method': ('每 seed 独立算 fair gain (analyze_fair_gain), 再 5 seed 统计 '
                            'mean±std, 95% CI t 分布 df=n-1 (5 seed→df=4). 复用主实验 ci_t 逻辑.'),
            'scenes': SCENES,
            'n_seeds': N_SEEDS,
            'hdfec_reference': float(P.HDFEC),
            'sdfec_prefec_mapping': {
                '1e-2': '~低开销 SD-FEC',
                '1.5e-2': '~20% SD-FEC 开销',
                '2e-2': '25% SD-FEC (Staircase/LDPC) 典型容限 (DVB-S2X 25%)',
                '2.5e-2': '~30% SD-FEC 开销',
            },
            'postfec_note': ('post-FEC BER 1e-7: pre-FEC BER 曲线在 1e-7 处通常不可达 '
                             '(BER floor 远高于此). 如不可达, 见 reachability 中 BER floor 位置.'),
            'simulator_unchanged': True,
            'numpy_version': np.__version__,
            'scipy_t_value_df4': float(stats.t.ppf(0.975, 4)),
        },
        'hdfec_sanity_check_vs_main': sanity_report,
        'thresholds': all_thresholds,
    }
    gain_path = os.path.join(OUT_DIR, '_sdfec_gain_summary.json')
    with open(gain_path, 'w', encoding='utf-8') as f:
        json.dump(gain_summary, f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {gain_path}")

    # --- 构建 _sdfec_reachability.json (精简可达性表) ---
    reach = {
        'meta': {
            'task': 'SD-FEC 阈值可达性 (每 scene 每 threshold 是否 BER 曲线达到该阈值)',
            'reachability_def': ('reachable = NDA 和 DA 曲线都插值得到该 BER (snr_at_ber 非 None). '
                                 'BER floor = 曲线最低 BER; 若 floor > threshold 则 unreachable.'),
            'source_raw': os.path.relpath(RAW_JSON, _SIM_ROOT),
        },
        'reachability': {},
    }
    for tdef, tres in zip(BER_THRESHOLDS, all_thresholds):
        ber = float(tdef['ber'])
        reach['reachability'][tdef['label']] = {
            'ber': ber,
            'kind': tdef['kind'],
            'per_scene': {
                sc: {
                    'reachable_overall': tres['results'][sc]['ber_floor']['reachable_overall'],
                    'reachable_any_seed': tres['results'][sc]['ber_floor']['reachable_any'],
                    'n_seeds_reachable': tres['results'][sc]['n_valid_seeds'],
                    'min_nda_ber_overall': tres['results'][sc]['ber_floor']['min_nda_ber_overall'],
                    'min_da_ber_overall': tres['results'][sc]['ber_floor']['min_da_ber_overall'],
                    'verdict': _verdict(ber, tres['results'][sc]['ber_floor']),
                } for sc in SCENES
            }
        }
    reach_path = os.path.join(OUT_DIR, '_sdfec_reachability.json')
    with open(reach_path, 'w', encoding='utf-8') as f:
        json.dump(reach, f, indent=2, ensure_ascii=False)
    print(f"[保存] {reach_path}")

    print("\n" + "=" * 100)
    print("完成.")


def _fmt_ber(ber):
    """BER 精确打印 (避免 2.5e-2 被 .0e 截成 1e-02)."""
    s = f'{ber:.1e}'
    return s


def _verdict(ber, bf):
    """生成可达性判定文字."""
    bs = _fmt_ber(ber)
    if bf['reachable_overall']:
        return f'REACHABLE (所有 seed NDA+DA 均达 BER={bs})'
    elif bf['reachable_any']:
        return (f'PARTIALLY REACHABLE ({bf["reachable_any"]}; '
                f'部分 seed: NDA floor {bf["min_nda_ber_overall"]:.3e})')
    else:
        return (f'UNREACHABLE (BER floor 高于阈值: '
                f'min NDA BER={bf["min_nda_ber_overall"]:.3e} > {bs})')


if __name__ == '__main__':
    main()
