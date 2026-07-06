# -*- coding: utf-8 -*-
"""Step 7 主实验: 5 seed 多种子统计 BER 曲线 + 公平对照 + 置信区间.

薄包装 (守 §2.3 纪律 2: 不改 sc_nda_ml_sim.py 核心逻辑). 仅调用其 API:
  run_awgn(n_blocks, snr_points, seed_base)
  run_turb(turb_name, gamma_bar_points_db, n_blocks, cfg, seed0)
  analyze_fair_gain(per_snr, hdfec)

种子策略 (§2.3 纪律 1: 第 0 seed = MVE seed 保可复现):
  - AWGN: seed_base_i = SEED_AWGN + i  (i=0..4)
      per-SNR seed = seed_base + int(snr*1000), 5 seed 间互斥 (每点偏移 i).
      seed 0 = SEED_AWGN → 与 MVE 完全一致.
  - 湍流: seed0_i = SEED_TURB0 + i*N_BLOCKS  (i=0..4, N_BLOCKS=400)
      per-block seed = seed0 + b (b=0..399). 用 i*N_BLOCKS 偏移保证 5 seed
      的 per-block seed 范围互不相交 → 5 个真正独立的实现 (置信区间有意义).
      seed 0 = SEED_TURB0 → 与 MVE 完全一致.
      注: 简单 seed0+i 会使 5 seed 重叠 399 块 → 方差被人为缩小, 违背 §2.3 纪律 4
      (置信区间须反映真实统计涨落). 故用互斥块范围.

统计方法 (§2.3 纪律 4):
  - BER: 每点 5 seed 均值 ± 标准差 (样本), 95% CI 用 t 分布 df=4 (scipy.stats.t).
      CI = mean ± t_{0.975,4} * std/sqrt(5), t_{0.975,4}=2.7764.
      备选 (记录): mean ± 1.96·std/sqrt(5) (正态近似).
  - fair gain @ HD-FEC: 每 seed 独立算 gain (analyze_fair_gain), 再统计 5 个 gain 的
      均值 ± 标准差. 注: 简述要求 "用 5 seed 平均 BER 曲线算" — 但平均 BER 曲线会
      破坏 BER 的随机性 (CLT 平均), 且 HD-FEC 交叉点对平均曲线更敏感.
      本脚本同时给两种: (a) per-seed gain 统计 [主], (b) 平均曲线 gain [参考].
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
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5
T05_4 = float(stats.t.ppf(0.975, 4))   # 2.7764 (95% CI, df=4)
Z95 = 1.96                              # 正态近似 95%

SCENES = ['awgn', 'weak', 'moderate', 'strong']
TURB_LEVELS = ['weak', 'moderate', 'strong']


def seed_base_awgn(i):
    """AWGN seed i: seed_base = SEED_AWGN + i. seed 0 = MVE."""
    return P.SEED_AWGN + i


def seed0_turb(i):
    """湍流 seed i: seed0 = SEED_TURB0 + i*N_BLOCKS. seed 0 = MVE. 5 seed 块范围互斥."""
    return P.SEED_TURB0 + i * P.N_BLOCKS


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
    # raw[scene][seed_i] = per_snr list (dict: snr_db/nda_ml_ber/da_ml_ber/oracle_ber)
    raw = {sc: {} for sc in SCENES}

    print("=" * 100)
    print(f"Step 7 主实验: {N_SEEDS} seed × {len(SCENES)} 场景")
    print(f"AWGN seed_base: {[seed_base_awgn(i) for i in range(N_SEEDS)]}")
    print(f"湍流 seed0   : {[seed0_turb(i) for i in range(N_SEEDS)]} "
          f"(5 seed 块范围互斥: {[f'{seed0_turb(i)}-{seed0_turb(i)+P.N_BLOCKS-1}' for i in range(N_SEEDS)]})")
    print(f"t-distribution 95% CI (df=4): ±{T05_4:.4f}·std/sqrt(5)")
    print("=" * 100)

    # --- AWGN ---
    for i in range(N_SEEDS):
        sb = seed_base_awgn(i)
        print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
        raw['awgn'][i] = S.run_awgn(P.N_BLOCKS, P.SNR_AWGN_DB, sb)

    # --- 湍流 ---
    for turb in TURB_LEVELS:
        for i in range(N_SEEDS):
            s0 = seed0_turb(i)
            print(f"\n########## {turb} seed {i} (seed0={s0}) ##########")
            raw[turb][i] = S.run_turb(turb, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)

    elapsed = time.time() - t0
    print(f"\n[总耗时] {elapsed:.1f} s")
    return raw, elapsed


def aggregate(raw):
    """每场景每 SNR: 5 seed BER 均值 ± std + 95% CI. 返回 summary[scene]."""
    summary = {}
    for sc in SCENES:
        per_seed = raw[sc]   # {seed_i: [per_snr dict]}
        # 对齐 SNR 点
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


def fair_gain_per_seed(raw):
    """每 seed 独立算 fair gain @ HD-FEC (analyze_fair_gain), 再统计 5 个 gain.
    返回 {scene: {per_seed_gains: [...], gain_mean, gain_std, gain_ci95, mve_single, ...}}.
    """
    out = {}
    # MVE 单 seed 对照值 (从 brief / _mve_results.json gain_analysis)
    mve_gain = {
        'awgn': 0.7041511552225828,
        'weak': 1.1985019094558034,
        'moderate': 1.921910939698943,
        'strong': None,   # HD-FEC 不可达
    }
    for sc in SCENES:
        gains = []
        # strong 工作区: 按 γ_tot_db 分组 (per-point fair gain), 处理各 seed 可能不同点数
        wr_by_snr = {}   # {gamma_tot_db: [per-seed fair_gain_db]}
        for i in range(N_SEEDS):
            per_snr = raw[sc][i]
            fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            g = fg['gain_nda_vs_da_fair_db']
            gains.append(g)
            # strong: 记录工作区 (γ_tot>=15) per-point fair gain (按 γ_tot 分组)
            if sc == 'strong':
                for p in fg['per_point_fair_gain']:
                    if p['gamma_tot_db'] >= 15.0:
                        wr_by_snr.setdefault(p['gamma_tot_db'], []).append(
                            (i, float(p['fair_gain_db'])))
        entry = {
            'per_seed_gain_db': [None if g is None else float(g) for g in gains],
            'mve_single_seed_db': mve_gain[sc],
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
        # strong 工作区 per-point 统计 (按 γ_tot 分组, 处理各 seed 不同点数)
        if sc == 'strong' and wr_by_snr:
            wr_snrs_sorted = sorted(wr_by_snr.keys())
            wr_points = []
            all_wr = []
            for gtot in wr_snrs_sorted:
                pairs = wr_by_snr[gtot]   # [(seed_i, gain), ...]
                col = [g for (_, g) in pairs]
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
            # 工作区 grand mean (所有工作点 × 所有 seed)
            gm, gs, ghw, glo, ghi = ci_t(all_wr)
            entry['workregion_grand_mean_db'] = gm
            entry['workregion_grand_std_db'] = gs
            entry['workregion_grand_ci95_db'] = [glo, ghi]
            entry['workregion_n_total'] = len(all_wr)
        out[sc] = entry
    return out


def fair_gain_avg_curve(summary):
    """参考: 用 5 seed 平均 BER 曲线算 fair gain @ HD-FEC. (平均曲线, 非 per-seed)."""
    out = {}
    for sc in SCENES:
        pts = summary[sc]['points']
        per_snr = [{
            'snr_db': p['snr_db'],
            'nda_ml_ber': p['nda_ml_ber_mean'],
            'da_ml_ber': p['da_ml_ber_mean'],
            'oracle_ber': p['oracle_ber_mean'],
        } for p in pts]
        fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
        out[sc] = {
            'gain_nda_vs_da_fair_db': fg['gain_nda_vs_da_fair_db'],
            'hdfec_reachable': fg['hdfec_reachable'],
            'snr_nda_tot_at_hdfec': fg['snr_nda_tot_at_hdfec'],
            'snr_da_tot_at_hdfec': fg['snr_da_tot_at_hdfec'],
            'snr_oracle_at_hdfec': fg['snr_oracle_at_hdfec'],
            'min_nda_ber': fg['min_nda_ber'],
        }
    return out


def check_seed0_vs_mve(raw, mve_results_path):
    """§2.3 纪律 1: 第 0 seed BER 必须与 MVE 一致 (否则停).
    用 5% 相对 / 1e-4 绝对容差 (同 consistency_check)."""
    with open(mve_results_path, 'r', encoding='utf-8') as f:
        mve = json.load(f)
    report = {'pass': True, 'scenes': {}}
    for sc in SCENES:
        formal = raw[sc][0]   # seed 0
        mve_pts = mve['results'][sc]
        pts = []
        sc_pass = True
        max_rel = 0.0
        for fp, mp in zip(formal, mve_pts):
            f_nda, f_da, f_or = fp['nda_ml_ber'], fp['da_ml_ber'], fp['oracle_ber']
            m_nda, m_da, m_or = mp['nda_ber'], mp['da_ber'], mp['oracle_ber']
            ok = True
            for f, m in [(f_nda, m_nda), (f_da, m_da), (f_or, m_or)]:
                rel = abs(f - m) / max(abs(m), 1e-12) if m > 1e-12 else abs(f - m)
                ok = ok and ((rel < 0.05) or (abs(f - m) < 1e-4))
                max_rel = max(max_rel, rel)
            pts.append({'snr_db': fp['snr_db'], 'ok': ok,
                        'nda': [f_nda, m_nda], 'da': [f_da, m_da], 'oracle': [f_or, m_or]})
            sc_pass = sc_pass and ok
        report['scenes'][sc] = {'pass': sc_pass, 'max_rel_err': max_rel, 'points': pts}
        report['pass'] = report['pass'] and sc_pass
    return report


def plot_curves(summary, fair_summary):
    """BER 曲线: 每场景子图, 5 seed 均值线 + 95% CI 阴影 (NDA/DA/oracle 三线)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 4, figsize=(22, 5.2))
    titles = {'awgn': 'AWGN', 'weak': 'weak (α4/β3)',
              'moderate': 'moderate (α2.5/β1.8)', 'strong': 'strong (α1.5/β0.8)'}
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
            ttl = f"{titles[sc]}\ngain@HD-FEC = {fg['gain_mean_db']:+.2f}±{fg['gain_std_db']:.2f} dB"
        elif sc == 'strong':
            ttl = f"{titles[sc]}\nHD-FEC 不可达; 工作区 gain {fg.get('workregion_grand_mean_db', 0):+.2f}±{fg.get('workregion_grand_std_db', 0):.2f} dB"
        else:
            ttl = titles[sc]
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel(r'$\gamma_{tot}$ (dB)')
        ax.set_ylabel('BER')
        ax.grid(True, which='both', alpha=0.3)
        ax.legend(fontsize=7.5, loc='best')
        ax.set_ylim(bottom=1e-4)
    fig.suptitle('Step 7 主实验: NDA-ML vs DA ML vs oracle (5 seed 均值 ± 95% CI)',
                 fontsize=12, y=1.01)
    fig.tight_layout()
    png = os.path.join(OUT_DIR, '_main_ber_curves_5seed.png')
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
    mve_path = os.path.join(_SIM_ROOT, 'explore', 'single-carrier-nda-ml', '_mve_results.json')

    raw, elapsed = run_all()

    # --- §2.3 纪律 1: seed 0 vs MVE 一致性核查 (失败则停) ---
    print("\n" + "#" * 40 + " seed 0 可复现性核查 (vs MVE) " + "#" * 40)
    repro = check_seed0_vs_mve(raw, mve_path)
    for sc in SCENES:
        sr = repro['scenes'][sc]
        print(f"  {sc:>10}: pass={sr['pass']}  max_rel_err={sr['max_rel_err']*100:.4f}%")
    print(f"  总体: {'PASS ✅' if repro['pass'] else 'FAIL ❌'}")
    if not repro['pass']:
        print("!!! seed 0 与 MVE 不一致, 停止 (仿真器 bug 或 seed 用错) !!!")
        # 仍落盘诊断信息
        diag = {'status': 'FAIL_seed0_vs_mve', 'repro_check': to_jsonable(repro)}
        with open(os.path.join(OUT_DIR, '_DIAG_FAIL.json'), 'w', encoding='utf-8') as f:
            json.dump(to_jsonable(diag), f, indent=2, ensure_ascii=False)
        return

    # --- 聚合统计 ---
    summary = aggregate(raw)
    fair_per_seed = fair_gain_per_seed(raw)
    fair_avg_curve = fair_gain_avg_curve(summary)

    # --- 画图 ---
    png_path = plot_curves(summary, fair_per_seed)

    # --- 落盘 _main_experiment_5seed.json ---
    out = {
        'meta': {
            'task': 'Step 7 主实验 (5 seed 多种子统计)',
            'metric': 'BER 曲线 + fair gain @ HD-FEC (γ_tot 坐标) + 95% CI',
            'n_seeds': N_SEEDS,
            'seed_strategy': {
                'awgn': f'seed_base_i = SEED_AWGN + i, i=0..4 (per-SNR seed=seed_base+int(snr*1000), 5 seed 互斥)',
                'turbulence': f'seed0_i = SEED_TURB0 + i*N_BLOCKS, i=0..4 (per-block seed=seed0+b, 5 seed 块范围互斥)',
                'note': 'seed 0 = MVE seed (可复现); 湍流用 i*N_BLOCKS 偏移 (非简单 +i) 保证 5 seed 真正独立 (避免 399 块重叠致方差人为缩小)',
            },
            'scenes': SCENES,
            'snr_awgn_db': P.SNR_AWGN_DB,
            'snr_turb_db': P.SNR_TURB_DB,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'M0': P.M0,
            'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'hdfec': P.HDFEC,
            'ci_method': f't-distribution 95% CI, df=n-1 (5 seed→df=4, t={T05_4:.4f}); CI=mean±t·std/sqrt(n)',
            'ci_method_alt': f'normal approx: mean ± {Z95}·std/sqrt(n)',
            'seed_awgn_mve': P.SEED_AWGN,
            'seed_turb0_mve': P.SEED_TURB0,
            'algorithm_source': 'common/ via sc_nda_ml_sim.py (Formal, MVE-verified, 未改核心逻辑)',
            'simulator_unchanged': True,
            'python': sys.executable,
            'numpy_version': np.__version__,
            'scipy_t_value_df4': T05_4,
            'elapsed_sec': float(elapsed),
        },
        'seed0_reproducibility_vs_mve': to_jsonable(repro),
        'summary': to_jsonable(summary),
        'fair_gain_per_seed': to_jsonable(fair_per_seed),
        'fair_gain_avg_curve_ref': to_jsonable(fair_avg_curve),
        'ber_curves_png': png_path,
    }
    out_json = os.path.join(OUT_DIR, '_main_experiment_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[保存] {png_path}")

    # --- 落盘 _fair_gain_summary.json (精简汇总) ---
    fair_short = {}
    for sc in SCENES:
        e = fair_per_seed[sc]
        entry = {
            'scene': sc,
            'gain_mean_db': e.get('gain_mean_db'),
            'gain_std_db': e.get('gain_std_db'),
            'gain_ci95_db': e.get('gain_ci95_db'),
            'per_seed_gain_db': e.get('per_seed_gain_db'),
            'mve_single_seed_db': e.get('mve_single_seed_db'),
            'n_valid_seeds': e.get('n_valid_seeds'),
        }
        if e.get('gain_mean_db') is not None and e.get('mve_single_seed_db') is not None:
            entry['mean_minus_mve_db'] = float(e['gain_mean_db'] - e['mve_single_seed_db'])
        if sc == 'strong':
            entry['note'] = 'HD-FEC 物理不可达 (oracle 也不可达); 用工作区 (γ_tot≥15dB) per-point fair gain'
            entry['workregion_grand_mean_db'] = e.get('workregion_grand_mean_db')
            entry['workregion_grand_std_db'] = e.get('workregion_grand_std_db')
            entry['workregion_grand_ci95_db'] = e.get('workregion_grand_ci95_db')
            entry['workregion_per_point'] = e.get('workregion_per_point')
            # MVE 工作区范围对照
            entry['mve_workregion_range_db'] = '+1.19~+2.62'
        fair_short[sc] = entry
    fair_summary = {
        'meta': {
            'task': 'fair gain @ HD-FEC 汇总 (5 seed)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC); 正=NDA赢',
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'per_seed_method': '每 seed 独立算 gain (analyze_fair_gain), 再统计 5 个 gain 的 mean±std (主)',
            'avg_curve_method': '5 seed 平均 BER 曲线算 gain (参考, 见 _main_experiment_5seed.json:fair_gain_avg_curve_ref)',
        },
        'fair_gain': fair_short,
    }
    fair_json = os.path.join(OUT_DIR, '_fair_gain_summary.json')
    with open(fair_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(fair_summary), f, indent=2, ensure_ascii=False)
    print(f"[保存] {fair_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print("Fair gain @ HD-FEC (5 seed):")
    print(f"{'场景':>10} {'mean(dB)':>10} {'std(dB)':>10} {'95% CI':>20} {'MVE':>8} {'Δmean-MVE':>10}")
    for sc in SCENES:
        e = fair_per_seed[sc]
        if e.get('gain_mean_db') is not None:
            ci = e['gain_ci95_db']
            dmve = e['gain_mean_db'] - e['mve_single_seed_db']
            print(f"{sc:>10} {e['gain_mean_db']:>+10.3f} {e['gain_std_db']:>10.3f} "
                  f"[{ci[0]:>+7.3f},{ci[1]:>+7.3f}] {e['mve_single_seed_db']:>+8.3f} {dmve:>+10.3f}")
        elif sc == 'strong':
            print(f"{sc:>10} HD-FEC 不可达, 工作区 grand mean={e.get('workregion_grand_mean_db',0):+.3f}"
                  f"±{e.get('workregion_grand_std_db',0):.3f} (MVE: +1.19~+2.62)")
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
