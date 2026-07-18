# -*- coding: utf-8 -*-
"""30-seed 主实验: NDA-ML vs DA-ML vs oracle BER 曲线 + fair_gain @ HD-FEC + 95% CI.

把主实验 fair_gain 链从 5 seed 补到 30 seed (CI 可信, 简报主引数据).

薄包装 (守 §2.3 纪律 2 / TL-13): 复用 run_main_experiment.py 的 run_awgn/run_turb/aggregate
逻辑, 只改 N_SEEDS=30, 并合并 6 场景 (4 下行 + 2 上行) 于一个脚本. 不改 common/.

种子策略 (§2.3 纪律 1/3, 沿用主实验湍流惯例, 已验证 30 seed 块范围互斥):
  - AWGN: seed_base_i = SEED_AWGN + i  (i=0..29)
      per-SNR seed = seed_base + int(snr*1000), 30 seed 互斥. seed 0 = MVE.
  - 湍流(下行): seed0_i = SEED_TURB0 + i*N_BLOCKS  (i=0..29, N_BLOCKS=400)
      per-block seed = seed0 + b. 30 seed 块范围互斥 (2000..13999). seed 0 = MVE.
  - 上行: seed0_i = SEED_TURB0 + UPLINK_SEED_OFFSET + i*N_BLOCKS
      = 502000..513600, 与下行不重叠且 30 seed 互斥.

统计方法 (§2.3 纪律 4): t 分布 95% CI, df=29, t_{0.975,29}=2.0452.
  CI = mean ± t · std/sqrt(30).
  fair_gain @ HD-FEC: 每 seed 独立算 gain 再统计 30 个 [主]; avg 曲线 gain [参考].
  strong/uplink HD-FEC 物理不可达 → 用工作区 (γ_tot≥15dB) per-point grand mean.

运行: cd projects/simulation && python simulator/run_main_experiment_30seed.py
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
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_main_30seed')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 30
T05_29 = float(stats.t.ppf(0.975, 29))   # 2.0452 (95% CI, df=29)

# 6 场景: 4 下行 + 2 上行. 下行跑 AWGN 扫描, 上行/湍流跑 γ_bar 扫描.
DOWN_SCENES = ['awgn', 'weak', 'moderate', 'strong']      # 含 MVE 一致性核查 (seed0 vs MVE)
UPLINK_SCENES = ['uplink_moderate', 'uplink_strong']       # 无 MVE
ALL_SCENES = DOWN_SCENES + UPLINK_SCENES
UPLINK_SEED_OFFSET = 500000  # 与 run_uplink_experiment.py 一致, 错开下行 seed 范围

# HD-FEC 不可达的场景 → 工作区 per-point grand mean 判据
WR_SCENES = {'strong', 'uplink_moderate', 'uplink_strong'}
WR_GTOT_MIN = 15.0


def seed_base_awgn(i):
    """AWGN seed i: seed_base = SEED_AWGN + i. seed 0 = MVE."""
    return P.SEED_AWGN + i


def seed0_turb(i, uplink=False):
    """湍流 seed i: seed0 = SEED_TURB0 [+ UPLINK_OFFSET] + i*N_BLOCKS.
    seed 0 = MVE (下行). 30 seed 块范围互斥."""
    base = P.SEED_TURB0 + (UPLINK_SEED_OFFSET if uplink else 0)
    return base + i * P.N_BLOCKS


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


def run_scene(scene, raw):
    """跑单场景 30 seed, 填入 raw[scene][seed_i]. 复用 S.run_awgn / S.run_turb."""
    cfg = SimulationConfig()
    if scene == 'awgn':
        for i in range(N_SEEDS):
            sb = seed_base_awgn(i)
            print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
            raw['awgn'][i] = S.run_awgn(P.N_BLOCKS, P.SNR_AWGN_DB, sb)
    else:
        uplink = scene in UPLINK_SCENES
        for i in range(N_SEEDS):
            s0 = seed0_turb(i, uplink=uplink)
            print(f"\n########## {scene} seed {i} (seed0={s0}) ##########")
            raw[scene][i] = S.run_turb(scene, P.SNR_TURB_DB, P.N_BLOCKS, cfg, s0)


def run_all():
    t0 = time.time()
    raw = {sc: {} for sc in ALL_SCENES}

    print("=" * 100)
    print(f"30-seed 主实验: {N_SEEDS} seed × {len(ALL_SCENES)} 场景")
    print(f"AWGN seed_base: {seed_base_awgn(0)} .. {seed_base_awgn(N_SEEDS-1)}")
    print(f"湍流下行 seed0: {seed0_turb(0)} .. {seed0_turb(N_SEEDS-1)} "
          f"(30 seed 块范围互斥, 2000..{seed0_turb(N_SEEDS-1)+P.N_BLOCKS-1})")
    print(f"上行      seed0: {seed0_turb(0,uplink=True)} .. {seed0_turb(N_SEEDS-1,uplink=True)} "
          f"(与下行不重叠)")
    print(f"t-distribution 95% CI (df=29): ±{T05_29:.4f}·std/sqrt({N_SEEDS})")
    print("=" * 100)

    for scene in ALL_SCENES:
        run_scene(scene, raw)

    elapsed = time.time() - t0
    print(f"\n[总耗时] {elapsed:.1f} s")
    return raw, elapsed


def aggregate(raw, scenes):
    """每场景每 SNR: 30 seed BER 均值 ± std + 95% CI. 返回 summary[scene]."""
    summary = {}
    for sc in scenes:
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
                'nda_ml_ber_mean': m_nda, 'nda_ml_ber_std': s_nda,
                'nda_ml_ber_ci95': [lo_nda, hi_nda], 'nda_ml_ber_ci_halfwidth': hw_nda,
                'da_ml_ber_mean': m_da, 'da_ml_ber_std': s_da,
                'da_ml_ber_ci95': [lo_da, hi_da], 'da_ml_ber_ci_halfwidth': hw_da,
                'oracle_ber_mean': m_or, 'oracle_ber_std': s_or,
                'oracle_ber_ci95': [lo_or, hi_or], 'oracle_ber_ci_halfwidth': hw_or,
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def fair_gain_per_seed(raw, scenes):
    """每 seed 独立算 fair gain @ HD-FEC, 再统计 30 个. HD-FEC 不可达 → 工作区 grand mean."""
    out = {}
    for sc in scenes:
        gains = []
        wr_by_snr = {}   # {gamma_tot_db: [per-seed fair_gain_db]}
        for i in range(N_SEEDS):
            per_snr = raw[sc][i]
            fg = analyze_fair_gain(per_snr, P.HDFEC, P.PILOT_OVERHEAD_DB)
            gains.append(fg['gain_nda_vs_da_fair_db'])
            if sc in WR_SCENES:
                for p in fg['per_point_fair_gain']:
                    if p['gamma_tot_db'] >= WR_GTOT_MIN:
                        wr_by_snr.setdefault(p['gamma_tot_db'], []).append(
                            (i, float(p['fair_gain_db'])))
        entry = {'per_seed_gain_db': [None if g is None else float(g) for g in gains]}
        valid = [g for g in gains if g is not None]
        if len(valid) >= 2:
            m, s, hw, lo, hi = ci_t(valid)
            entry.update({'gain_mean_db': m, 'gain_std_db': s,
                          'gain_ci95_db': [lo, hi], 'gain_ci_halfwidth_db': hw,
                          'n_valid_seeds': len(valid)})
        else:
            entry.update({'gain_mean_db': None, 'gain_std_db': None,
                          'gain_ci95_db': [None, None], 'n_valid_seeds': len(valid)})
        # 工作区 per-point grand mean (HD-FEC 不可达时主判据)
        if wr_by_snr:
            wr_snrs_sorted = sorted(wr_by_snr.keys())
            wr_points = []
            all_wr = []
            for gtot in wr_snrs_sorted:
                col = [g for (_, g) in wr_by_snr[gtot]]
                m, s, hw, lo, hi = ci_t(col)
                wr_points.append({
                    'gamma_tot_db': float(gtot), 'n_seeds': len(col),
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


def fair_gain_avg_curve(summary, scenes):
    """参考: 用 30 seed 平均 BER 曲线算 fair gain @ HD-FEC."""
    out = {}
    for sc in scenes:
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
        }
    return out


def check_seed0_vs_mve(raw, mve_results_path):
    """§2.3 纪律 1: 下行 4 场景 seed 0 BER 必须与 MVE 一致 (5% rel / 1e-4 abs 容差)."""
    with open(mve_results_path, 'r', encoding='utf-8') as f:
        mve = json.load(f)
    report = {'pass': True, 'scenes': {}}
    for sc in DOWN_SCENES:
        formal = raw[sc][0]
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
            pts.append({'snr_db': fp['snr_db'], 'ok': ok})
            sc_pass = sc_pass and ok
        report['scenes'][sc] = {'pass': sc_pass, 'max_rel_err': max_rel}
        report['pass'] = report['pass'] and sc_pass
    return report


def mve_self_check(raw, scenes):
    """守 TL-23: NDA BER ≥ oracle BER, 全场景全 SNR 全 seed (0 违例)."""
    violations = []
    for sc in scenes:
        for i in range(N_SEEDS):
            for p in raw[sc][i]:
                if p['nda_ml_ber'] < p['oracle_ber'] - 1e-12:
                    violations.append({'scene': sc, 'seed': i, 'snr_db': p['snr_db']})
    return {'pass': len(violations) == 0, 'n_violations': len(violations),
            'violations': violations[:20]}


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
    t0 = time.time()

    raw, elapsed_run = run_all()

    # --- 纪律 1: 下行 seed0 vs MVE ---
    print("\n" + "#" * 40 + " 下行 seed 0 可复现性核查 (vs MVE) " + "#" * 40)
    repro = check_seed0_vs_mve(raw, mve_path)
    for sc in DOWN_SCENES:
        sr = repro['scenes'][sc]
        print(f"  {sc:>10}: pass={sr['pass']}  max_rel_err={sr['max_rel_err']*100:.4f}%")
    print(f"  下行总体: {'PASS ✅' if repro['pass'] else 'FAIL ❌'}")

    # --- TL-23: NDA ≥ oracle (全 6 场景) ---
    mve_chk = mve_self_check(raw, ALL_SCENES)
    print(f"  NDA ≥ oracle 违例数: {mve_chk['n_violations']} ({'PASS ✅' if mve_chk['pass'] else 'FAIL ❌'})")

    # --- 聚合统计 ---
    summary = aggregate(raw, ALL_SCENES)
    fair_per_seed = fair_gain_per_seed(raw, ALL_SCENES)
    fair_avg_curve = fair_gain_avg_curve(summary, ALL_SCENES)

    elapsed = time.time() - t0

    # --- 落盘 _main_experiment_30seed.json ---
    out = {
        'meta': {
            'task': '30-seed 主实验: NDA-ML vs DA-ML vs oracle (6 场景, fair_gain@HD-FEC)',
            'n_seeds': N_SEEDS,
            'scenes': ALL_SCENES,
            'down_scenes': DOWN_SCENES,
            'uplink_scenes': UPLINK_SCENES,
            'snr_awgn_db': P.SNR_AWGN_DB,
            'snr_turb_db': P.SNR_TURB_DB,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'M0': P.M0,
            'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'hdfec': P.HDFEC,
            'wr_scenes': list(WR_SCENES),
            'wr_gtot_min_db': WR_GTOT_MIN,
            'ci_method': f't-distribution 95% CI, df={N_SEEDS-1} (t={T05_29:.4f}); CI=mean±t·std/sqrt({N_SEEDS})',
            'seed_strategy': {
                'awgn': f'seed_base_i = SEED_AWGN + i, i=0..{N_SEEDS-1} (seed0=MVE)',
                'turb_down': f'seed0_i = SEED_TURB0 + i*N_BLOCKS, i=0..{N_SEEDS-1} (互斥 2000..{seed0_turb(N_SEEDS-1)+P.N_BLOCKS-1})',
                'turb_uplink': f'seed0_i = SEED_TURB0 + {UPLINK_SEED_OFFSET} + i*N_BLOCKS, i=0..{N_SEEDS-1} (与下行不重叠)',
            },
            'algorithm_source': 'common/ via sc_nda_ml_sim.py (Formal, MVE-verified, 未改核心逻辑)',
            'simulator_unchanged': True,
            'scipy_t_value_df29': T05_29,
            'elapsed_sec': float(elapsed),
        },
        'seed0_reproducibility_vs_mve': to_jsonable(repro),
        'mve_self_check': mve_chk,
        'summary': to_jsonable(summary),
        'fair_gain_per_seed': to_jsonable(fair_per_seed),
        'fair_gain_avg_curve_ref': to_jsonable(fair_avg_curve),
    }
    out_json = os.path.join(OUT_DIR, '_main_experiment_30seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 落盘 _fair_gain_summary_30seed.json (简报主引数据) ---
    fair_short = {}
    for sc in ALL_SCENES:
        e = fair_per_seed[sc]
        entry = {
            'scene': sc,
            'gain_mean_db': e.get('gain_mean_db'),
            'gain_std_db': e.get('gain_std_db'),
            'gain_ci95_db': e.get('gain_ci95_db'),
            'n_valid_seeds': e.get('n_valid_seeds'),
            'hdfec_reachable': e.get('gain_mean_db') is not None,
        }
        if e.get('workregion_grand_mean_db') is not None:
            entry['note'] = 'HD-FEC 物理不可达; 用工作区 (γ_tot≥15dB) per-point grand mean'
            entry['workregion_grand_mean_db'] = e['workregion_grand_mean_db']
            entry['workregion_grand_std_db'] = e['workregion_grand_std_db']
            entry['workregion_grand_ci95_db'] = e['workregion_grand_ci95_db']
            entry['workregion_n_total'] = e['workregion_n_total']
        fair_short[sc] = entry
    fair_summary = {
        'meta': {
            'task': 'fair_gain @ HD-FEC 汇总 (30 seed, 简报主引数据)',
            'ci_method': out['meta']['ci_method'],
            'gain_definition': 'fair_gain@HD-FEC = (DA γ_tot @ HD-FEC) − (NDA γ_tot @ HD-FEC); 正=NDA赢',
            'per_seed_method': '每 seed 独立算 gain, 再统计 30 个 gain 的 mean±std (主)',
            'wr_method': 'HD-FEC 不可达场景: 工作区 (γ_tot≥15dB) per-point fair_gain grand mean',
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
        },
        'fair_gain': fair_short,
    }
    fair_json = os.path.join(OUT_DIR, '_fair_gain_summary_30seed.json')
    with open(fair_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(fair_summary), f, indent=2, ensure_ascii=False)
    print(f"[保存] {fair_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print(f"Fair gain (30 seed, df=29):")
    print(f"{'场景':>18} {'mean(dB)':>10} {'std(dB)':>9} {'95% CI':>24} {'判据':>9}")
    chain = []
    for sc in ALL_SCENES:
        e = fair_per_seed[sc]
        if e.get('gain_mean_db') is not None:
            ci = e['gain_ci95_db']
            print(f"{sc:>18} {e['gain_mean_db']:>+10.3f} {e['gain_std_db']:>9.3f} "
                  f"[{ci[0]:>+8.3f},{ci[1]:>+8.3f}] {'HD-FEC':>9}")
            chain.append(e['gain_mean_db'])
        else:
            gm = e['workregion_grand_mean_db']; gs = e['workregion_grand_std_db']
            gci = e['workregion_grand_ci95_db']
            print(f"{sc:>18} {gm:>+10.3f} {gs:>9.3f} "
                  f"[{gci[0]:>+8.3f},{gci[1]:>+8.3f}] {'工作区':>9}")
            chain.append(gm)
    print(f"\nfair_gain 链 (awgn→weak→mod→strong→up_mod→up_str): "
          f"{[f'{c:+.2f}' for c in chain]}")
    print(f"单调: {all(chain[i] <= chain[i+1] for i in range(len(chain)-1))}")
    print(f"\n下行 seed0 vs MVE: {'PASS ✅' if repro['pass'] else 'FAIL ❌'}")
    print(f"NDA ≥ oracle: {'PASS ✅' if mve_chk['pass'] else 'FAIL ❌'} "
          f"(违例={mve_chk['n_violations']})")
    print(f"[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
