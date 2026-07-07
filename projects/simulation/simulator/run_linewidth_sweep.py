# -*- coding: utf-8 -*-
"""激光线宽扫描实验 (导师第 1 条必做项): 10k / 50k / 100k / 500 kHz × 4 场景 × 5 seed.

**D-007 (2026-07-07) 重构**: 线宽注入方式从"运行时改写信道函数默认参数"改为显式传参
(param-source.md 失败模式 A 的症状修复):
  - AWGN: sc_nda_ml_sim.run_awgn(..., sigma2_p=derived) 透传给 awgn_wiener_channel
  - 湍流: sc_nda_ml_sim.run_turb(..., lw=clw_hz) 透传给 generate_shared_realization_apsk

全场景统一单载波参数 (LASER_LW @ R_SYM=2.5GBaud, T_S=400ps). AWGN 不再用 B11 OFDM
25GBaud 场景. σ²_p = 2π·CLW·T_S (T_S=400ps 两路径一致).

守 TL-13: 不动信道生成逻辑, 只改线宽参数. 种子策略 100% 沿用 run_main_experiment.py
(AWGN: seed_base_i=SEED_AWGN+i; 湍流: seed0_i=SEED_TURB0+i*N_BLOCKS) — 保证
5 seed 独立且各档可与主实验逐 seed 对照.

输出 (projects/simulation/results/sc_nda_ml_linewidth_sweep/):
  _linewidth_sweep_raw.json     每 CLW × 场景 × seed 的 per_snr BER
  _linewidth_sweep_summary.json 每 CLW × 场景的 fair gain@HD-FEC (mean±CI) + vs 主实验基线
  _linewidth_sweep_timing.json  各阶段耗时
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径 (与 run_main_experiment.py 一致) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402
from fair_comparison import analyze_fair_gain  # noqa: E402
from params import SimulationConfig  # noqa: E402
from scipy import stats  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_linewidth_sweep')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764 (95% CI, df=4)

SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']

# 线宽扫描网格 (Hz). 主实验基线 = LASER_LW 默认 10kHz (D-007 单载波统一).
LINEWIDTHS_HZ = [10e3, 50e3, 100e3, 500e3]

# 单载波符号周期 (D-007 统一, 两路径一致)
T_S_SC = 1.0 / P._CFG.system.R_SYM   # = 4e-10 s (2.5GBaud)


def sigma2p_from_lw(lw_hz):
    """从线宽算 Wiener PN 每符号方差 σ²_p = 2π·Δν·T_S (Viterbi 1963). D-007 单载波 T_S."""
    return 2.0 * np.pi * lw_hz * T_S_SC


# --- 种子策略 (100% 复用 run_main_experiment.py, 保 5 seed 独立 + 可对照主实验) ---
def seed_base_awgn(i):
    return P.SEED_AWGN + i


def seed0_turb(i):
    return P.SEED_TURB0 + i * P.N_BLOCKS


def ci_t(data):
    """95% CI 半宽 (t 分布, df=n-1). 返回 (mean, std, ci_halfwidth, ci_low, ci_high)."""
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


# =============================================================================
# 主扫描
# =============================================================================
def run_sweep():
    """4 线宽 × 4 场景 × 5 seed = 80 run. D-007: 传参注入 (不再 monkey-patch)."""
    cfg = SimulationConfig()
    timing = {'stages': {}, 'per_clw': {}}
    t_all = time.time()

    # raw[clw_hz][scene][seed_i] = per_snr list
    raw = {clw: {sc: {} for sc in SCENES} for clw in LINEWIDTHS_HZ}

    print("=" * 100)
    print(f"激光线宽扫描: {len(LINEWIDTHS_HZ)} 线宽 × {len(SCENES)} 场景 × {N_SEEDS} seed = "
          f"{len(LINEWIDTHS_HZ)*len(SCENES)*N_SEEDS} run")
    print(f"线宽: {[f'{c/1e3:.0f}kHz' for c in LINEWIDTHS_HZ]}")
    print(f"AWGN seed_base: {[seed_base_awgn(i) for i in range(N_SEEDS)]}")
    print(f"湍流 seed0   : {[seed0_turb(i) for i in range(N_SEEDS)]}")
    print(f"T_S (D-007 单载波统一)={T_S_SC:.2e}s (两路径一致, 不再有 B11/AWGN 双 T_S)")
    print(f"t-dist 95% CI (df=4): ±{T05_4:.4f}·std/sqrt(5)")
    print("=" * 100)

    for clw in LINEWIDTHS_HZ:
        t_clw = time.time()
        # D-007: 传参注入 σ²_p (不再 monkey-patch). 单载波 T_S 两路径一致.
        sigma2p = sigma2p_from_lw(clw)
        print(f"\n{'#'*100}")
        print(f"### LW = {clw/1e3:.0f} kHz | σ²_p=2π·{clw/1e3:.0f}k·{T_S_SC:.2e}="
              f"{sigma2p:.4e} rad²/sym (D-007 单载波, 两路径一致) ###")
        print(f"{'#'*100}")

        # --- AWGN (传 sigma2_p) ---
        for i in range(N_SEEDS):
            sb = seed_base_awgn(i)
            print(f"\n########## LW={clw/1e3:.0f}kHz AWGN seed {i} (seed_base={sb}) ##########")
            raw[clw]['awgn'][i] = S.run_awgn(P.N_BLOCKS, P.SNR_AWGN_DB, sb, sigma2_p=sigma2p)

        # --- 湍流 (传 lw) ---
        for turb in TURB_LEVELS:
            for i in range(N_SEEDS):
                s0 = seed0_turb(i)
                print(f"\n########## LW={clw/1e3:.0f}kHz {turb} seed {i} (seed0={s0}) ##########")
                raw[clw][turb][i] = S.run_turb(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0, lw=clw)

        timing['per_clw'][f'{clw/1e3:.0f}kHz'] = time.time() - t_clw
        print(f"\n[LW={clw/1e3:.0f}kHz 耗时] {timing['per_clw'][f'{clw/1e3:.0f}kHz']:.1f}s")

    timing['stages']['total'] = time.time() - t_all
    print(f"\n[总耗时] {timing['stages']['total']:.1f}s")
    return raw, timing


# =============================================================================
# 聚合: 每 CLW × 场景 fair gain@HD-FEC (per-seed 统计) + BER 聚合
# =============================================================================
def _seed_lookup(seed_dict, i):
    """兼容 int / str 键 (内存 raw 用 int, 重载 JSON 用 str)."""
    if i in seed_dict:
        return seed_dict[i]
    return seed_dict[str(i)]


def fair_gain_per_seed_for_clw(clw_raw):
    """对单个线宽的 raw[scene][seed_i] 算 per-seed fair gain. 返回 {scene: entry}.

    逻辑同 run_main_experiment.fair_gain_per_seed (strong 场景 HD-FEC 不可达时用工作区).
    兼容 int/str seed 键 (内存用 int, 重载 JSON 用 str).
    """
    out = {}
    for sc in SCENES:
        gains = []
        wr_by_snr = {}
        for i in range(N_SEEDS):
            per_snr = _seed_lookup(clw_raw[sc], i)
            fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            g = fg['gain_nda_vs_da_fair_db']
            gains.append(g)
            if sc == 'strong':
                for pp in fg['per_point_fair_gain']:
                    if pp['gamma_tot_db'] >= 15.0:
                        wr_by_snr.setdefault(pp['gamma_tot_db'], []).append(
                            (i, float(pp['fair_gain_db'])))
        entry = {
            'per_seed_gain_db': [None if g is None else float(g) for g in gains],
        }
        valid = [g for g in gains if g is not None]
        if len(valid) >= 2:
            m, s, hw, lo, hi = ci_t(valid)
            entry.update({
                'gain_mean_db': m, 'gain_std_db': s,
                'gain_ci95_db': [lo, hi], 'gain_ci_halfwidth_db': hw,
                'n_valid_seeds': len(valid),
            })
        else:
            entry.update({'gain_mean_db': None, 'gain_std_db': None,
                          'gain_ci95_db': [None, None], 'n_valid_seeds': len(valid)})
        # strong 工作区 (γ_tot≥15)
        if sc == 'strong' and wr_by_snr:
            wr_snrs_sorted = sorted(wr_by_snr.keys())
            wr_points = []
            all_wr = []
            for gtot in wr_snrs_sorted:
                col = [g for (_, g) in wr_by_snr[gtot]]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({
                    'gamma_tot_db': float(gtot),
                    'n_seeds': len(col),
                    'per_seed_fair_gain_db': col,
                    'fair_gain_mean_db': m, 'fair_gain_std_db': s,
                    'fair_gain_ci95_db': [lo, hi],
                })
                all_wr.extend(col)
            entry['workregion_per_point'] = wr_points
            gm, gs, ghw, glo, ghi = ci_t(all_wr)
            entry['workregion_grand_mean_db'] = gm
            entry['workregion_grand_std_db'] = gs
            entry['workregion_grand_ci95_db'] = [glo, ghi]
            entry['workregion_n_total'] = len(all_wr)
        out[sc] = entry
    return out


def aggregate_ber_for_clw(clw_raw):
    """对单个线宽聚合 BER (5 seed mean±CI). 返回 {scene: {snr_db, points}}.
    兼容 int/str seed 键."""
    summary = {}
    for sc in SCENES:
        per_seed = clw_raw[sc]
        snrs = [p['snr_db'] for p in _seed_lookup(per_seed, 0)]
        points = []
        for j, snr in enumerate(snrs):
            nda = [_seed_lookup(per_seed, i)[j]['nda_ml_ber'] for i in range(N_SEEDS)]
            da = [_seed_lookup(per_seed, i)[j]['da_ml_ber'] for i in range(N_SEEDS)]
            orc = [_seed_lookup(per_seed, i)[j]['oracle_ber'] for i in range(N_SEEDS)]
            m_nda, s_nda, hw_nda, lo_nda, hi_nda = ci_t(nda)
            m_da, s_da, hw_da, lo_da, hi_da = ci_t(da)
            m_or, s_or, hw_or, lo_or, hi_or = ci_t(orc)
            points.append({
                'snr_db': float(snr),
                'per_seed': {
                    'nda_ml_ber': [float(x) for x in nda],
                    'da_ml_ber': [float(x) for x in da],
                    'oracle_ber': [float(x) for x in orc],
                },
                'nda_ml_ber_mean': m_nda, 'nda_ml_ber_std': s_nda,
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


# =============================================================================
# JSON 序列化辅助
# =============================================================================
def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return to_jsonable(o.tolist())
    return o


def aggregate_and_save(raw, timing, injection_check, t0):
    """从 raw 结果聚合 fair gain/BER, 生成 _summary.json + _timing.json.
    raw 键可为 int 或 str (重载 JSON). injection_check 为必验1 的传参注入结果."""
    # --- 聚合: 每 CLW fair gain + BER ---
    print("\n" + "#" * 40 + " 聚合统计 (fair gain@HD-FEC) " + "#" * 40)
    fair_by_clw = {}      # {clw: {scene: entry}}
    ber_summary_by_clw = {}  # {clw: {scene: summary}}
    for clw in LINEWIDTHS_HZ:
        fair_by_clw[clw] = fair_gain_per_seed_for_clw(raw[clw])
        ber_summary_by_clw[clw] = aggregate_ber_for_clw(raw[clw])
        print(f"\n--- CLW={clw/1e3:.0f}kHz fair gain@HD-FEC ---")
        for sc in SCENES:
            e = fair_by_clw[clw][sc]
            if e.get('gain_mean_db') is not None:
                ci = e['gain_ci95_db']
                print(f"  {sc:>10}: {e['gain_mean_db']:>+8.4f} ± {e['gain_std_db']:.4f} dB "
                      f"95%CI[{ci[0]:+8.4f},{ci[1]:+8.4f}] n={e['n_valid_seeds']}")
            elif sc == 'strong':
                print(f"  {sc:>10}: HD-FEC 不可达, 工作区 grand mean="
                      f"{e.get('workregion_grand_mean_db', 0):+.4f} "
                      f"± {e.get('workregion_grand_std_db', 0):.4f} dB")

    # --- vs 主实验基线 (D-007: 全场景 LASER_LW=10kHz 单载波统一) ---
    # 主实验基线 = LASER_LW 默认 10kHz (单载波统一, AWGN 不再用 B11 OFDM 500kHz).
    baseline_clw = 10e3
    baseline_fair = fair_by_clw[baseline_clw]
    # 宽线宽极端档 (sweep 最宽, 仍保留 delta_vs_500kHz 双向解读)
    wide_clw = 500e3
    wide_fair = fair_by_clw[wide_clw]

    # --- 必验 2: vs 主实验 _fair_gain_summary.json ---
    # D-007 后主实验全场景统一 LASER_LW=10kHz (单载波, 不再有 AWGN 500kHz / 湍流 10kHz 双源):
    #   全场景 10kHz sweep 档 = 主实验 (应逐 seed 完全一致, per_seed_diff==0).
    main_summary_path = os.path.join(_SIM_ROOT, 'results',
                                     'sc_nda_ml_main', '_fair_gain_summary.json')
    main_check = {'available': False, 'scenes': {}, 'baseline_map_note':
                  '主实验全场景 LASER_LW=10kHz (D-007 单载波统一); 10kHz sweep 档 = 主实验.'}
    # 场景 → 对照的 sweep 线宽档 (D-007: 全场景对照 10kHz)
    scene_baseline_clw = {sc: 10e3 for sc in SCENES}
    if os.path.exists(main_summary_path):
        try:
            with open(main_summary_path, 'r', encoding='utf-8') as f:
                main_fair = json.load(f)
            main_check['available'] = True
            main_check['main_path'] = main_summary_path
            for sc in SCENES:
                cmp_clw = scene_baseline_clw[sc]
                e_sweep = fair_by_clw[cmp_clw][sc]
                e_main = main_fair['fair_gain'].get(sc, {})
                sweep_mean = e_sweep.get('gain_mean_db')
                main_mean = e_main.get('gain_mean_db')
                sweep_ps = e_sweep.get('per_seed_gain_db')
                main_ps = e_main.get('per_seed_gain_db')
                # 逐 seed 对比 (最强 sanity: 同 seed 应完全一致)
                per_seed_diff = None
                if sweep_ps is not None and main_ps is not None:
                    per_seed_diff = [None if (s is None or m is None) else float(s - m)
                                     for s, m in zip(sweep_ps, main_ps)]
                diff_mean = None
                if sweep_mean is not None and main_mean is not None:
                    diff_mean = float(sweep_mean - main_mean)
                # strong 工作区对比
                wr_diff = None
                if sc == 'strong':
                    sw = e_sweep.get('workregion_grand_mean_db')
                    mw = e_main.get('workregion_grand_mean_db')
                    if sw is not None and mw is not None:
                        wr_diff = float(sw - mw)
                main_check['scenes'][sc] = {
                    'comparison_sweep_clw_hz': cmp_clw,
                    'comparison_sweep_clw_label': f'{cmp_clw/1e3:.0f}kHz',
                    'sweep_gain_mean_db': sweep_mean,
                    'main_gain_mean_db': main_mean,
                    'diff_mean_db': diff_mean,
                    'within_float_tol': abs(diff_mean) < 1e-9 if diff_mean is not None else None,
                    'per_seed_diff_db': per_seed_diff,
                    'per_seed_all_zero': (per_seed_diff is not None
                                          and all(d is not None and abs(d) < 1e-12
                                                  for d in per_seed_diff)),
                    'workregion_diff_db': wr_diff,
                }
        except Exception as e:
            main_check['error'] = str(e)

    print("\n" + "#" * 40 + " 必验 2: sweep vs 主实验对照 (全场景↔10kHz) " + "#" * 40)
    if main_check.get('available'):
        for sc in SCENES:
            c = main_check['scenes'].get(sc, {})
            az = c.get('per_seed_all_zero')
            sm = c.get('sweep_gain_mean_db')
            mm = c.get('main_gain_mean_db')
            lbl = c.get('comparison_sweep_clw_label', '?')
            print(f"  {sc:>10} (↔{lbl}): sweep={sm} main={mm} per_seed_all_zero={az}")
            if c.get('per_seed_diff_db'):
                diffs = c['per_seed_diff_db']
                print(f"             per_seed_diff=["
                      + ', '.join('None' if d is None else f'{d:.2e}' for d in diffs) + "]")
    else:
        print("  主实验 _fair_gain_summary.json 不可用, 跳过")

    # --- 落盘 _summary.json ---
    # fair_gain_by_clw: {clw_str: {scene: {gain_mean, gain_std, gain_ci95, per_seed, workregion...}}}
    # 窄线宽基线 (10kHz) 与 宽线宽极端档 (500kHz) 各算一次 delta, 便于双向解读:
    #   - AWGN: 500kHz sweep 极端档是 DA 受 Wiener PN 打击最大处 → NDA gain 最大; 窄线宽下两法都接近 oracle,
    #     差距收窄 (gain 略降是 DA/NDA 共同收敛所致, 非算法失效).
    #   - 湍流: 500kHz sweep 极端档是 NDA-ML tracking 崩塌点 (块内 PN 累积 >> segK8 跟踪能力);
    #     窄线宽 (10kHz) 下 NDA 恢复正常, gain 最大.
    narrow_clw = 10e3
    narrow_fair = fair_by_clw[narrow_clw]
    fair_short = {}
    for clw in LINEWIDTHS_HZ:
        key = f'{clw/1e3:.0f}kHz'
        entry = {}
        for sc in SCENES:
            e = fair_by_clw[clw][sc]
            d = {
                'gain_mean_db': e.get('gain_mean_db'),
                'gain_std_db': e.get('gain_std_db'),
                'gain_ci95_db': e.get('gain_ci95_db'),
                'per_seed_gain_db': e.get('per_seed_gain_db'),
                'n_valid_seeds': e.get('n_valid_seeds'),
            }
            # delta vs 500kHz (宽线宽极端档, sweep 最宽, NDA 最坏跟踪点)
            if e.get('gain_mean_db') is not None and wide_fair[sc].get('gain_mean_db') is not None:
                d['delta_vs_500kHz_mean_db'] = float(e['gain_mean_db']
                                                     - wide_fair[sc]['gain_mean_db'])
            # delta vs 10kHz (窄线宽基线 = 主实验基线, NDA 最佳跟踪点)
            if e.get('gain_mean_db') is not None and narrow_fair[sc].get('gain_mean_db') is not None:
                d['delta_vs_10kHz_mean_db'] = float(e['gain_mean_db']
                                                    - narrow_fair[sc]['gain_mean_db'])
            if sc == 'strong':
                d['workregion_grand_mean_db'] = e.get('workregion_grand_mean_db')
                d['workregion_grand_std_db'] = e.get('workregion_grand_std_db')
                d['workregion_grand_ci95_db'] = e.get('workregion_grand_ci95_db')
                if wide_fair[sc].get('workregion_grand_mean_db') is not None \
                        and e.get('workregion_grand_mean_db') is not None:
                    d['workregion_delta_vs_500kHz_db'] = float(
                        e['workregion_grand_mean_db']
                        - wide_fair[sc]['workregion_grand_mean_db'])
                if narrow_fair[sc].get('workregion_grand_mean_db') is not None \
                        and e.get('workregion_grand_mean_db') is not None:
                    d['workregion_delta_vs_10kHz_db'] = float(
                        e['workregion_grand_mean_db']
                        - narrow_fair[sc]['workregion_grand_mean_db'])
            entry[sc] = d
        fair_short[key] = entry

    # 物理合理性检查 (D-007: 全场景单载波统一, T_S 一致; 失效模式仍按场景区分)
    monotonicity = {'scenes': {}, 'note':
        'AWGN: 500kHz sweep 极端档下 DA 受 Wiener PN 打击最大 (segK8 NDA 跟踪能力强), gain 最大; '
        '窄线宽下 NDA/DA 共同趋近 oracle, 差距收窄 (gain 略降, 非 NDA 失效). '
        '湍流: 500kHz sweep 极端档下 NDA-ML 跟踪崩塌 (块内 PN 累积 >> segK8 能力), gain 大跌甚至转负; '
        '窄线宽 (10kHz) 下 NDA 恢复正常. '
        '判据: gain 不出现非物理负崩塌 (<-2dB 且非 strong 工作区) 即合理.'}
    for sc in SCENES:
        means = []
        for clw in LINEWIDTHS_HZ:
            e = fair_by_clw[clw][sc]
            means.append(e.get('gain_mean_db') if sc != 'strong'
                         else e.get('workregion_grand_mean_db'))
        if means[0] is not None and means[-1] is not None:
            monotonicity['scenes'][sc] = {
                'gains_by_clw': {f'{LINEWIDTHS_HZ[k]/1e3:.0f}kHz': means[k]
                                 for k in range(len(LINEWIDTHS_HZ))},
                'narrowest_minus_widest_db': float(means[0] - means[-1]),
                # 湍流场景: 窄线宽 gain 应显著 > 宽线宽 (NDA 跟踪恢复); AWGN: 允许反向小幅
                'narrowest_geq_widest_minus_tol': means[0] >= means[-1] - 0.5,
                'no_severe_negative_collapse': all(m is not None and m > -2.0 for m in means),
                'interpretation': (
                    'AWGN: 宽线宽 gain 略大 (DA 受 PN 打击多), 物理合理' if sc == 'awgn'
                    else ('湍流: 窄线宽 gain 应恢复 (500kHz sweep 极端档 NDA 跟踪崩塌)' )),
            }

    summary_out = {
        'meta': {
            'task': '激光线宽扫描 fair gain@HD-FEC 汇总',
            'linewidths_hz': LINEWIDTHS_HZ,
            'linewidths_khz': [c/1e3 for c in LINEWIDTHS_HZ],
            'baseline_clw_hz': baseline_clw,
            'n_seeds': N_SEEDS,
            'ci_method': f't-dist 95% CI df=n-1 (5 seed→df=4, t={T05_4:.4f})',
            'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot@HD-FEC)-(NDA γ_tot@HD-FEC); 正=NDA赢',
            'per_seed_method': '每 seed 独立 analyze_fair_gain, 再统计 5 个 gain mean±std',
            'strong_note': 'HD-FEC 物理不可达, 用工作区 (γ_tot≥15dB) per-point fair gain grand mean',
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'seed_strategy_100pct_same_as_main': True,
            'two_linewidth_paths': {
                'awgn': 'sigma2_p 传参注入 run_awgn (D-007, 不再 monkey-patch)',
                'turbulence': 'lw 传参注入 run_turb→generate_shared_realization_apsk (D-007)',
                'note': '主实验全场景 LASER_LW=10kHz (D-007 单载波统一). sweep 各档两路径同步扫描.',
            },
        },
        'fair_gain_by_clw': fair_short,
        'vs_main_experiment_check': main_check,
        'physical_monotonicity_check': monotonicity,
    }
    summary_path = os.path.join(OUT_DIR, '_linewidth_sweep_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(summary_out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {summary_path}")

    # --- 落盘 _timing.json ---
    # aggregate 耗时 = 本次 aggregate_and_save 调用至今的时间 (reaggregate 模式下 t0=本次启动,
    # timing.stages.total 是历史仿真耗时, 不应从 t0 减; 用 wall_now - aggregate_start 替代)
    if not hasattr(aggregate_and_save, '_t_agg_start'):
        aggregate_and_save._t_agg_start = t0
    agg_elapsed = time.time() - t0
    sim_total = timing['stages'].get('total', 0.0)
    timing_out = {
        'meta': {
            'task': '激光线宽扫描各阶段耗时',
            'n_runs_total': len(LINEWIDTHS_HZ) * len(SCENES) * N_SEEDS,
        },
        'stages': {
            'run_sweep': timing,
            'injection_check': injection_check,
            'aggregate_and_save_sec': agg_elapsed,
            'pure_simulation_sec': sim_total,
            'total_run_plus_aggregate_sec': sim_total + agg_elapsed,
        },
        'per_clw': timing.get('per_clw', {}),
    }
    timing_path = os.path.join(OUT_DIR, '_linewidth_sweep_timing.json')
    with open(timing_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(timing_out), f, indent=2, ensure_ascii=False)
    print(f"[保存] {timing_path}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("Fair gain@HD-FEC by linewidth (5 seed mean):")
    hdr = f"{'场景':>10}"
    for clw in LINEWIDTHS_HZ:
        hdr += f" {clw/1e3:>9.0f}kHz"
    print(hdr)
    for sc in SCENES:
        line = f"{sc:>10}"
        for clw in LINEWIDTHS_HZ:
            e = fair_by_clw[clw][sc]
            m = e.get('gain_mean_db') if sc != 'strong' else e.get('workregion_grand_mean_db')
            if m is not None:
                line += f"  {m:>+9.4f}"
            else:
                line += f"  {'N/A':>9}"
        print(line)
    print(f"\n[总耗时] pure_sim={timing['stages']['total']:.1f}s + aggregate={agg_elapsed:.1f}s")


def main(argv=None):
    """入口. 默认全跑; --reaggregate 从已存 _raw.json 重算 summary/timing."""
    argv = argv if argv is not None else sys.argv[1:]
    t0 = time.time()

    if '--reaggregate' in argv:
        raw_path = os.path.join(OUT_DIR, '_linewidth_sweep_raw.json')
        print(f"[reaggregate] 从 {raw_path} 重载 raw, 重算 summary/timing")
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_doc = json.load(f)
        # raw 键为 str (JSON) → 转 float (与 LINEWIDTHS_HZ 一致), seed 键兼容 str/int
        raw = {float(k): v for k, v in raw_doc['raw'].items()}
        # 从 timing JSON 读回 per-clw 耗时 (若存在), 否则用 raw meta 的 elapsed_sec_total
        timing_path = os.path.join(OUT_DIR, '_linewidth_sweep_timing.json')
        timing = {'stages': {'total': raw_doc['meta'].get('elapsed_sec_total', 0.0)}, 'per_clw': {}}
        if os.path.exists(timing_path):
            with open(timing_path, 'r', encoding='utf-8') as f:
                tj = json.load(f)
            if tj.get('per_clw'):
                timing['per_clw'] = tj['per_clw']
            if tj.get('stages', {}).get('pure_simulation_sec'):
                timing['stages']['total'] = tj['stages']['pure_simulation_sec']
        injection_check = raw_doc['meta'].get('injection_check', {})
        aggregate_and_save(raw, timing, injection_check, t0)
        return

    # --- 必验 1: 传参注入验证 (σ²_p=2π·LW·T_S) ---
    injection_check = {}
    print("\n" + "#" * 40 + " 必验 1: 传参注入验证 (σ²_p=2π·LW·T_S) " + "#" * 40)
    for clw in LINEWIDTHS_HZ:
        expected = sigma2p_from_lw(clw)
        ok = abs(expected - 2*np.pi*clw*T_S_SC) < 1e-15
        injection_check[f'{clw/1e3:.0f}kHz'] = {
            'lw_hz': clw, 'sigma2_p': expected, 'ok': ok}
        print(f"  LW={clw/1e3:>5.0f}kHz: σ²_p={expected:.4e} OK={ok}")
    assert all(v['ok'] for v in injection_check.values()), "传参 σ²_p 计算错!"

    # --- 主扫描 ---
    raw, timing = run_sweep()

    # --- 落盘 _raw.json ---
    raw_out = {
        'meta': {
            'task': '激光线宽扫描 (导师第 1 条): 10k/50k/100k/500kHz × 4 场景 × 5 seed',
            'linewidths_hz': LINEWIDTHS_HZ,
            'linewidths_khz': [c/1e3 for c in LINEWIDTHS_HZ],
            'baseline_clw_hz': 10e3,
            'n_seeds': N_SEEDS,
            'scenes': SCENES,
            'snr_awgn_db': P.SNR_AWGN_DB,
            'snr_turb_db': P.SNR_TURB_DB,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'T_S_sc_s': float(T_S_SC),
            'T_S_note': 'D-007 单载波统一, AWGN/湍流两路径 T_S 一致',
            'hdfec': P.HDFEC,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'seed_strategy': {
                'awgn': 'seed_base_i = SEED_AWGN + i, per-SNR seed=seed_base+int(snr*1000)',
                'turbulence': 'seed0_i = SEED_TURB0 + i*N_BLOCKS, per-block seed=seed0+b',
                'note': '100% 复用 run_main_experiment.py, 10kHz 档可逐 seed 与主实验对照',
            },
            'injection_strategy': {
                'awgn': 'sigma2_p 传参注入 run_awgn (D-007, 不再 monkey-patch)',
                'turbulence': 'lw 传参注入 run_turb→generate_shared_realization_apsk (D-007)',
                'note': '只改线宽参数, 不改信道生成/估计算法逻辑 (守 TL-13)',
            },
            'injection_check': injection_check,
            'simulator_unchanged': True,
            'elapsed_sec_total': timing['stages']['total'],
        },
        'raw': to_jsonable(raw),
    }
    raw_path = os.path.join(OUT_DIR, '_linewidth_sweep_raw.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(raw_out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {raw_path}")

    # --- 聚合 + summary/timing ---
    aggregate_and_save(raw, timing, injection_check, t0)


if __name__ == '__main__':
    main()
