# -*- coding: utf-8 -*-
"""上行(地面→卫星)湍流场景主实验: 5 seed × 2 上行场景, 复用改进版 Formal 仿真器.

背景 (sat.1553 Valjus 2025 综述 Table 1):
  星地链路上行受湍流影响远大于下行 (大气湍流主要在低空, 上行信号发射即受扰).
  sat.1553 Rytov 方差: 下行 σ²_R=0.029, 上行弱 σ²_R=0.15, 上行强 σ²_R=0.25.
  当前主实验仅测下行 weak/moderate/strong; 本实验补上行两档验证 NDA-ML 增益方向是否成立.

新增上行场景 (设计选择, 参考 sat.1553 上行 σ²_R 区间):
  - uplink_moderate: α=1.2, β=0.9 (≈σ²_R 0.15, 比现有 strong 略强)
  - uplink_strong  : α=1.0, β=0.7 (≈σ²_R 0.25, 明显比 strong 强, 接近 deep fade)

薄包装 (守 §2.3 纪律 2: 不改 sc_nda_ml_sim.py 核心逻辑). 仅调用 S.run_turb:
  湍流场景用 ber_nda_turb (intra_block_tracking='none' 默认, 即改进版的湍流分支不变).
  → 与主实验改进版 (sc_nda_ml_main_improved) 的湍流分支完全一致 (信道实现复用, TL-13).

种子策略 (§2.3 纪律 1/3, 同主实验湍流):
  湍流: seed0_i = SEED_TURB0 + i*N_BLOCKS (i=0..4, N_BLOCKS=400)
        per-block seed = seed0 + b (b=0..399). 5 seed 块范围互斥 → 真正独立.
        注: 上行场景不在 MVE 中, 故无 seed0=MVE 对照; 用 MVE 派生的 seed 偏移惯例.
        为与主实验湍流 seed 范围错开 (避免上行种子碰巧与下行同实现), 上行加 UPLINK_SEED_OFFSET
        = 500000, 保证上行 5 seed 块范围与主实验下行不重叠且互斥.

MVE 一致性自检 (守 TL-23, 此处因 MVE 无上行档, 改为守序约束):
  全场景全 SNR 全 seed: NDA BER ≥ oracle BER (0 违例, MVE 上界约束).
  现有 weak/moderate/strong 不参与 (本脚本只跑上行, 现有档由主实验改进版守).

输出 (results/sc_nda_ml_uplink/):
  _uplink_5seed.json     每场景每 SNR 每 seed 的 BER + 聚合统计
  _uplink_summary.json   fair gain 表 (每场景)
  _uplink_curves.png     BER 曲线

运行: cd projects/simulation && python simulator/run_uplink_experiment.py
"""
import os
import sys
import json
import time

import numpy as np

# --- 路径 ---
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
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_uplink')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764 (95% CI, df=4)
Z95 = 1.96

# 上行场景 (设计选择, 参考 sat.1553 上行 σ²_R=0.15/0.25)
SCENES = list(P.UPLINK_LEVELS)   # ['uplink_moderate', 'uplink_strong']
SCENE_TITLES = {
    'uplink_moderate': 'uplink_moderate (α1.2/β0.9, ≈σ²_R 0.15)',
    'uplink_strong': 'uplink_strong (α1.0/β0.7, ≈σ²_R 0.25)',
}

# 上行 seed 偏移: 错开主实验下行 seed 范围 (下行 SEED_TURB0 + i*400 ∈ [2000, 3999]),
# 上行 SEED_TURB0 + 500000 + i*400 ∈ [502000, 503999], 完全不重叠且 5 seed 互斥.
UPLINK_SEED_OFFSET = 500000


def seed0_uplink(i):
    """上行 seed i: seed0 = SEED_TURB0 + UPLINK_SEED_OFFSET + i*N_BLOCKS.
    5 seed 块范围互斥, 且与主实验下行 seed 范围不重叠."""
    return P.SEED_TURB0 + UPLINK_SEED_OFFSET + i * P.N_BLOCKS


def ci_t(data):
    """95% CI 半宽 (t 分布, df=n-1). 返回 (mean, std, ci_half_width, ci_low, ci_high)."""
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


def run_all():
    cfg = SimulationConfig()
    t0 = time.time()
    # raw[scene][seed_i] = per_snr list
    raw = {sc: {} for sc in SCENES}

    print("=" * 100)
    print(f"上行湍流实验: {N_SEEDS} seed × {len(SCENES)} 场景")
    print(f"上行场景: {SCENES}")
    print(f"  α/β: {P.UPLINK_ALPHA_BETA}")
    print(f"SNR 点 (γ_tot dB): {P.SNR_TURB_DB} (同主实验湍流)")
    for sc in SCENES:
        print(f"  {sc} seed0: {[seed0_uplink(i) for i in range(N_SEEDS)]} "
              f"(5 seed 块范围互斥, 与下行不重叠)")
    print(f"t-distribution 95% CI (df=4): ±{T05_4:.4f}·std/sqrt(5)")
    print("=" * 100)

    for turb in SCENES:
        for i in range(N_SEEDS):
            s0 = seed0_uplink(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = S.run_turb(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)

    elapsed = time.time() - t0
    print(f"\n[总耗时] {elapsed:.1f} s")
    return raw, elapsed


def aggregate(raw):
    """每场景每 SNR: 5 seed BER 均值 ± std + 95% CI. 返回 summary[scene]."""
    summary = {}
    for sc in SCENES:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        points = []
        for j, snr in enumerate(snrs):
            nda = [per_seed[i][j]['nda_ml_ber'] for i in range(N_SEEDS)]
            da = [per_seed[i][j]['da_ml_ber'] for i in range(N_SEEDS)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(N_SEEDS)]
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
                'nda_ml_ber_ci95': [lo_nda, hi_nda], 'nda_ml_ber_ci_halfwidth': hw_nda,
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'da_ml_ber_ci95': [lo_da, hi_da], 'da_ml_ber_ci_halfwidth': hw_da,
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
                'oracle_ber_ci95': [lo_or, hi_or], 'oracle_ber_ci_halfwidth': hw_or,
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def mve_self_check(raw):
    """MVE 一致性自检 (守 TL-23): NDA BER ≥ oracle BER, 全场景全 SNR 全 seed (0 违例).
    oracle 是 genie 相位+幅度, BER 必为下界. 违例 = 仿真 bug. 返回 {pass, violations}."""
    violations = []
    for sc in SCENES:
        for i in range(N_SEEDS):
            for j, p in enumerate(raw[sc][i]):
                if p['nda_ml_ber'] < p['oracle_ber'] - 1e-12:
                    violations.append({
                        'scene': sc, 'seed': i, 'snr_db': p['snr_db'],
                        'nda_ber': float(p['nda_ml_ber']),
                        'oracle_ber': float(p['oracle_ber']),
                        'deficit': float(p['oracle_ber'] - p['nda_ml_ber']),
                    })
    return {'pass': len(violations) == 0, 'n_violations': len(violations),
            'violations': violations[:20]}


def fair_gain_per_seed(raw):
    """每 seed 独立算 fair gain @ HD-FEC, 再统计. 上行档 HD-FEC 多半不可达 → 用工作区 per-point."""
    out = {}
    for sc in SCENES:
        gains = []
        wr_by_snr = {}
        for i in range(N_SEEDS):
            per_snr = raw[sc][i]
            fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            g = fg['gain_nda_vs_da_fair_db']
            gains.append(g)
            for p in fg['per_point_fair_gain']:
                if p['gamma_tot_db'] >= 15.0:
                    wr_by_snr.setdefault(p['gamma_tot_db'], []).append(
                        (i, float(p['fair_gain_db'])))
        entry = {
            'per_seed_gain_db': [None if g is None else float(g) for g in gains],
        }
        valid = [g for g in gains if g is not None]
        if len(valid) >= 2:
            m, s, hw, lo, hi = ci_t(valid)
            entry.update({'gain_mean_db': m, 'gain_std_db': s,
                          'gain_ci95_db': [lo, hi], 'gain_ci_halfwidth_db': hw,
                          'n_valid_seeds': len(valid)})
        else:
            entry.update({'gain_mean_db': None, 'gain_std_db': None,
                          'gain_ci95_db': [None, None], 'n_valid_seeds': len(valid)})
        # 工作区 (γ_tot≥15) per-point 统计 (HD-FEC 不可达时主判据)
        if wr_by_snr:
            wr_snrs_sorted = sorted(wr_by_snr.keys())
            wr_points = []
            all_wr = []
            for gtot in wr_snrs_sorted:
                col = [g for (_, g) in wr_by_snr[gtot]]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({
                    'gamma_tot_db': float(gtot), 'n_seeds': len(col),
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


def fair_gain_avg_curve(summary):
    """参考: 用 5 seed 平均 BER 曲线算 fair gain @ HD-FEC."""
    out = {}
    for sc in SCENES:
        pts = summary[sc]['points']
        per_snr = [{'snr_db': p['snr_db'],
                    'nda_ml_ber': p['nda_ml_ber_mean'],
                    'da_ml_ber': p['da_ml_ber_mean'],
                    'oracle_ber': p['oracle_ber_mean']} for p in pts]
        fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
        out[sc] = {
            'gain_nda_vs_da_fair_db': fg['gain_nda_vs_da_fair_db'],
            'hdfec_reachable': fg['hdfec_reachable'],
            'snr_nda_tot_at_hdfec': fg['snr_nda_tot_at_hdfec'],
            'snr_da_tot_at_hdfec': fg['snr_da_tot_at_hdfec'],
            'min_nda_ber': fg['min_nda_ber'],
            'equiv_gain_at_achievable_db': fg['equiv_gain_at_achievable_db'],
        }
    return out


def plot_curves(summary, fair_summary):
    """BER 曲线: 每场景子图, 5 seed 均值线 + 95% CI 阴影 (NDA/DA/oracle)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(SCENES), figsize=(11 * len(SCENES) / 2, 5.2))
    if len(SCENES) == 1:
        axes = [axes]
    for ax, sc in zip(axes, SCENES):
        pts = summary[sc]['points']
        gts = [p['snr_db'] for p in pts]
        nda_m = np.array([p['nda_ml_ber_mean'] for p in pts])
        nda_lo = np.array([p['nda_ml_ber_ci95'][0] for p in pts])
        nda_hi = np.array([p['nda_ml_ber_ci95'][1] for p in pts])
        da_m = np.array([p['da_ml_ber_mean'] for p in pts])
        da_lo = np.array([p['da_ml_ber_ci95'][0] for p in pts])
        da_hi = np.array([p['da_ml_ber_ci95'][1] for p in pts])
        or_m = np.array([p['oracle_ber_mean'] for p in pts])
        or_lo = np.array([p['oracle_ber_ci95'][0] for p in pts])
        or_hi = np.array([p['oracle_ber_ci95'][1] for p in pts])

        ax.semilogy(gts, nda_m, 'o-', color='C0', label='NDA-ML (M0=8)', lw=1.8)
        ax.fill_between(gts, np.maximum(nda_lo, 1e-6), nda_hi, color='C0', alpha=0.18)
        ax.semilogy(gts, da_m, 's-', color='C1', label='DA ML (sp=4)', lw=1.8)
        ax.fill_between(gts, np.maximum(da_lo, 1e-6), da_hi, color='C1', alpha=0.18)
        ax.semilogy(gts, or_m, '^--', color='C2', label='oracle', lw=1.6)
        ax.fill_between(gts, np.maximum(or_lo, 1e-6), or_hi, color='C2', alpha=0.15)
        ax.axhline(P.HDFEC, color='k', ls=':', label='HD-FEC 3.8e-3')

        fg = fair_summary[sc]
        if fg.get('gain_mean_db') is not None:
            ttl = (f"{SCENE_TITLES[sc]}\n"
                   f"gain@HD-FEC = {fg['gain_mean_db']:+.2f}±{fg['gain_std_db']:.2f} dB")
        elif fg.get('workregion_grand_mean_db') is not None:
            ttl = (f"{SCENE_TITLES[sc]}\n"
                   f"HD-FEC 不可达; 工作区 gain {fg['workregion_grand_mean_db']:+.2f}"
                   f"±{fg['workregion_grand_std_db']:.2f} dB")
        else:
            ttl = SCENE_TITLES[sc]
        ax.set_title(ttl, fontsize=9.5)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7.5, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('上行(地面→卫星)湍流场景: NDA-ML vs DA ML vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_uplink_curves.png')
    fig.savefig(png, dpi=120, bbox_inches='tight')
    return png


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


def main():
    t0 = time.time()
    raw, elapsed_run = run_all()

    # --- MVE 一致性自检 (守 TL-23): NDA ≥ oracle, 0 违例 ---
    print("\n" + "#" * 40 + " MVE 自检 (NDA ≥ oracle, 守 TL-23) " + "#" * 40)
    mve_chk = mve_self_check(raw)
    print(f"  NDA ≥ oracle 违例数: {mve_chk['n_violations']}")
    if not mve_chk['pass']:
        for v in mve_chk['violations'][:5]:
            print(f"    {v}")
        print("  !!! 危险: NDA BER < oracle (违反 MVE 上界), 停止 !!!")

    # --- 聚合统计 ---
    summary = aggregate(raw)
    fair_per_seed = fair_gain_per_seed(raw)
    fair_avg_curve = fair_gain_avg_curve(summary)

    # --- 画图 ---
    png_path = plot_curves(summary, fair_per_seed)

    elapsed = time.time() - t0

    # --- 落盘 _uplink_5seed.json ---
    out = {
        'meta': {
            'task': '上行(地面→卫星)湍流场景主实验 (5 seed × 2 上行场景)',
            'background': 'sat.1553 Valjus 2025 综述 Table 1: 上行 σ²_R(0.15/0.25) >> 下行 0.029',
            'metric': 'BER 曲线 + fair gain @ HD-FEC (γ_tot 坐标) + 95% CI',
            'n_seeds': N_SEEDS,
            'scenes': SCENES,
            'uplink_alpha_beta': {k: list(v) for k, v in P.UPLINK_ALPHA_BETA.items()},
            'uplink_param_source': ('设计选择: 参考 sat.1553 上行 σ²_R=0.15/0.25, '
                                    '选对应强度区间 Gamma-Gamma α/β (比现有 strong 更极端)'),
            'snr_turb_db': P.SNR_TURB_DB,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'M0': P.M0,
            'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'hdfec': P.HDFEC,
            'seed_strategy': {
                'uplink': (f'seed0_i = SEED_TURB0 + {UPLINK_SEED_OFFSET} + i*N_BLOCKS, '
                           f'i=0..4 (per-block seed=seed0+b, 5 seed 块范围互斥, 与下行不重叠)'),
                'note': ('上行不在 MVE 中, 故无 seed0=MVE 对照; 用主实验湍流 seed 派生惯例 '
                         '+ UPLINK_SEED_OFFSET 错开下行范围.'),
            },
            'ci_method': f't-distribution 95% CI, df=n-1 (5 seed→df=4, t={T05_4:.4f})',
            'recovery': ('湍流场景用改进版 Formal ber_nda_turb (intra_block_tracking=none 默认), '
                         '与主实验改进版湍流分支完全一致'),
            'algorithm_source': 'common/ via sc_nda_ml_sim.py (Formal, MVE-verified)',
            'simulator_unchanged': True,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'scipy_t_value_df4': T05_4,
            'elapsed_sec': float(elapsed),
        },
        'mve_self_check': mve_chk,
        'summary': to_jsonable(summary),
        'fair_gain_per_seed': to_jsonable(fair_per_seed),
        'fair_gain_avg_curve_ref': to_jsonable(fair_avg_curve),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_uplink_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[保存] {png_path}")

    # --- 落盘 _uplink_summary.json (精简 fair gain 表) ---
    fair_short = {}
    for sc in SCENES:
        e = fair_per_seed[sc]
        entry = {
            'scene': sc,
            'alpha_beta': list(P.UPLINK_ALPHA_BETA[sc]),
            'gain_mean_db': e.get('gain_mean_db'),
            'gain_std_db': e.get('gain_std_db'),
            'gain_ci95_db': e.get('gain_ci95_db'),
            'per_seed_gain_db': e.get('per_seed_gain_db'),
            'n_valid_seeds': e.get('n_valid_seeds'),
            'hdfec_reachable': e.get('gain_mean_db') is not None,
        }
        if e.get('workregion_grand_mean_db') is not None:
            entry['note'] = 'HD-FEC 物理不可达 (上行 deep fade); 用工作区 (γ_tot≥15dB) per-point fair gain'
            entry['workregion_grand_mean_db'] = e.get('workregion_grand_mean_db')
            entry['workregion_grand_std_db'] = e.get('workregion_grand_std_db')
            entry['workregion_grand_ci95_db'] = e.get('workregion_grand_ci95_db')
        fair_short[sc] = entry
    fair_summary = {
        'meta': {
            'task': '上行湍流 fair gain 汇总 (5 seed)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC); 正=NDA赢',
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'comparison': '主实验改进版下行 strong 工作区 gain ≈ +2.51 dB (参考)',
        },
        'fair_gain': fair_short,
    }
    fair_json = os.path.join(OUT_DIR, '_uplink_summary.json')
    with open(fair_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(fair_summary), f, indent=2, ensure_ascii=False)
    print(f"[保存] {fair_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("上行湍流 Fair gain (5 seed):")
    print(f"{'场景':>18} {'α/β':>10} {'mean(dB)':>10} {'std(dB)':>10} {'95% CI':>22} {'HD-FEC':>8}")
    for sc in SCENES:
        e = fair_per_seed[sc]
        ab = f"{P.UPLINK_ALPHA_BETA[sc][0]}/{P.UPLINK_ALPHA_BETA[sc][1]}"
        if e.get('gain_mean_db') is not None:
            ci = e['gain_ci95_db']
            print(f"{sc:>18} {ab:>10} {e['gain_mean_db']:>+10.3f} {e['gain_std_db']:>10.3f} "
                  f"[{ci[0]:>+8.3f},{ci[1]:>+8.3f}] {'可达':>8}")
        else:
            gm = e.get('workregion_grand_mean_db', 0)
            gs = e.get('workregion_grand_std_db', 0)
            print(f"{sc:>18} {ab:>10} {'--':>10} {'--':>10} {'工作区':>22} {'不可达':>8}")
            print(f"{'':>18} {'':>10} 工作区 gain={gm:+.3f}±{gs:.3f} dB (γ_tot≥15dB)")
    print(f"\nMVE 自检 (NDA ≥ oracle): {'PASS ✅' if mve_chk['pass'] else 'FAIL ❌'} "
          f"(违例={mve_chk['n_violations']})")
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
