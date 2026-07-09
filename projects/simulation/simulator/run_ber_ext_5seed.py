# -*- coding: utf-8 -*-
"""BER 补点实验 (5 seed × 6 场景): 给主实验补高 SNR 点, 探各场景 BER 能降到多低.

任务来源: 导师要求 BER 展示到 1e-5, 现有 30seed 主实验只扫到 1e-2~1e-4.
本轮 = 探索性补点 (5 seed, 看趋势/到哪算哪), 不是正式统计. 报告里标清"5 seed 探索性".

薄包装 (守 §2.3 纪律 2 / TL-13): 复用 run_main_experiment_30seed.py 的 run_awgn/run_turb
调用逻辑 + seed 派生策略, 只改 N_SEEDS=5 + 扩展 SNR 范围 (往上补). 不改 common/.
除 SNR 范围 + seed 数外, 一切 (N_BLOCKS/M0/pilot_spacing/LW=10kHz/amp_limit) 沿用.

SNR 补点设计 (在现有范围之上补, 高 SNR 区 2 dB 步长衔接):
  现有: AWGN 5..20 dB (8 点); turb 5..26 dB (7 点).
  本轮只跑 NEW 区间 (不重复跑现有区, 省算力; 报告时与 30seed 数据拼接):
    awgn:           22, 24, 26, 28, 30 dB                     (+10 dB, 预判到 1e-5)
    weak:           28, 30, 32, 34, 36, 38, 40 dB              (+14 dB)
    moderate:       28, 30, 32, 34, 36, 38, 40, 42, 44, 46 dB  (+20 dB, 看 1e-5)
    strong:         28, 30, 32, 34, 36, 38, 40, 42, 44 dB      (+18 dB, 探地板)
    uplink_moderate:28, 30, 32, 34, 36, 38, 40, 42, 44 dB      (+18 dB, 探地板)
    uplink_strong:  28, 30, 32, 34, 36, 38, 40, 42, 44, 46 dB  (+20 dB, 探地板)

seed 策略 (与 30seed 一致, i=0..4 对齐 30seed 前 5 个 seed, 方便未来升级):
  - AWGN: seed_base_i = SEED_AWGN + i  (i=0..4)
  - 湍流下行: seed0_i = SEED_TURB0 + i*N_BLOCKS  (i=0..4)
  - 上行: seed0_i = SEED_TURB0 + UPLINK_SEED_OFFSET + i*N_BLOCKS  (i=0..4)

运行: cd projects/simulation && python simulator/run_ber_ext_5seed.py
"""
import os
import sys
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
from params import SimulationConfig  # noqa: E402

# --- 输出目录 ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5

DOWN_SCENES = ['awgn', 'weak', 'moderate', 'strong']
UPLINK_SCENES = ['uplink_moderate', 'uplink_strong']
ALL_SCENES = DOWN_SCENES + UPLINK_SCENES
UPLINK_SEED_OFFSET = 500000  # 与 run_main_experiment_30seed.py 一致

# --- SNR 补点 (仅在现有范围之上补; 现有 AWGN 顶 20dB, turb 顶 26dB) ---
SNR_AWGN_EXT = [22.0, 24.0, 26.0, 28.0, 30.0]
SNR_WEAK_EXT = [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0]
SNR_MOD_EXT = [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0]
SNR_STRONG_EXT = [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0]
SNR_UPLINK_MOD_EXT = [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0]
SNR_UPLINK_STRONG_EXT = [28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0]

SNR_EXT = {
    'awgn': SNR_AWGN_EXT,
    'weak': SNR_WEAK_EXT,
    'moderate': SNR_MOD_EXT,
    'strong': SNR_STRONG_EXT,
    'uplink_moderate': SNR_UPLINK_MOD_EXT,
    'uplink_strong': SNR_UPLINK_STRONG_EXT,
}


def seed_base_awgn(i):
    """AWGN seed i: seed_base = SEED_AWGN + i. seed 0 = MVE (同 30seed)."""
    return P.SEED_AWGN + i


def seed0_turb(i, uplink=False):
    """湍流 seed i: seed0 = SEED_TURB0 [+ UPLINK_OFFSET] + i*N_BLOCKS. (同 30seed)."""
    base = P.SEED_TURB0 + (UPLINK_SEED_OFFSET if uplink else 0)
    return base + i * P.N_BLOCKS


def run_scene(scene, raw):
    """跑单场景 5 seed, 填入 raw[scene][seed_i]. 复用 S.run_awgn / S.run_turb."""
    cfg = SimulationConfig()
    snr_pts = SNR_EXT[scene]
    if scene == 'awgn':
        for i in range(N_SEEDS):
            sb = seed_base_awgn(i)
            print(f"\n########## AWGN seed {i} (seed_base={sb}) ##########")
            raw['awgn'][i] = S.run_awgn(P.N_BLOCKS, snr_pts, sb)
    else:
        uplink = scene in UPLINK_SCENES
        for i in range(N_SEEDS):
            s0 = seed0_turb(i, uplink=uplink)
            print(f"\n########## {scene} seed {i} (seed0={s0}) ##########")
            raw[scene][i] = S.run_turb(scene, snr_pts, P.N_BLOCKS, cfg, s0)


def run_all():
    t0 = time.time()
    raw = {sc: {} for sc in ALL_SCENES}

    print("=" * 100)
    print(f"BER 补点实验 (探索性): {N_SEEDS} seed × {len(ALL_SCENES)} 场景, 仅高 SNR 新区")
    print(f"AWGN seed_base: {seed_base_awgn(0)} .. {seed_base_awgn(N_SEEDS-1)}")
    print(f"湍流下行 seed0: {seed0_turb(0)} .. {seed0_turb(N_SEEDS-1)}")
    print(f"上行      seed0: {seed0_turb(0,uplink=True)} .. {seed0_turb(N_SEEDS-1,uplink=True)}")
    for sc in ALL_SCENES:
        print(f"  {sc:>16}: SNR 补点 = {SNR_EXT[sc]}")
    print("=" * 100)

    for scene in ALL_SCENES:
        run_scene(scene, raw)

    elapsed = time.time() - t0
    print(f"\n[总耗时] {elapsed:.1f} s")
    return raw, elapsed


def aggregate(raw, scenes):
    """每场景每 SNR: 5 seed BER 均值 ± std + min/max. 返回 summary[scene]."""
    summary = {}
    for sc in scenes:
        per_seed = raw[sc]
        snrs = [p['snr_db'] for p in per_seed[0]]
        points = []
        for j, snr in enumerate(snrs):
            nda = [per_seed[i][j]['nda_ml_ber'] for i in range(N_SEEDS)]
            da = [per_seed[i][j]['da_ml_ber'] for i in range(N_SEEDS)]
            orc = [per_seed[i][j]['oracle_ber'] for i in range(N_SEEDS)]
            nda_a = np.asarray(nda, dtype=float)
            da_a = np.asarray(da, dtype=float)
            orc_a = np.asarray(orc, dtype=float)
            points.append({
                'snr_db': float(snr),
                'nda_ml_ber_mean': float(nda_a.mean()),
                'nda_ml_ber_std': float(nda_a.std(ddof=1)),
                'nda_ml_ber_min': float(nda_a.min()),
                'nda_ml_ber_max': float(nda_a.max()),
                'da_ml_ber_mean': float(da_a.mean()),
                'da_ml_ber_std': float(da_a.std(ddof=1)),
                'da_ml_ber_min': float(da_a.min()),
                'da_ml_ber_max': float(da_a.max()),
                'oracle_ber_mean': float(orc_a.mean()),
                'oracle_ber_std': float(orc_a.std(ddof=1)),
                'oracle_ber_min': float(orc_a.min()),
                'oracle_ber_max': float(orc_a.max()),
            })
        summary[sc] = {'snr_db': snrs, 'points': points}
    return summary


def mve_self_check(raw, scenes):
    """守 TL-23: NDA BER >= oracle BER, 全场景全 SNR 全 seed (0 违例)."""
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
    import json
    t0 = time.time()

    raw, elapsed_run = run_all()

    # --- TL-23: NDA >= oracle ---
    mve_chk = mve_self_check(raw, ALL_SCENES)
    print(f"\n  NDA >= oracle 违例数: {mve_chk['n_violations']} "
          f"({'PASS' if mve_chk['pass'] else 'FAIL'})")

    # --- 聚合 ---
    summary = aggregate(raw, ALL_SCENES)

    elapsed = time.time() - t0

    out = {
        'meta': {
            'task': 'BER 补点实验 (5 seed 探索性): 高 SNR 区探各场景 BER 最低值',
            'note': '探索性补点 (5 seed), 非正式统计. 配置除 SNR 范围+seed 数外与 30seed 主实验一致',
            'n_seeds': N_SEEDS,
            'scenes': ALL_SCENES,
            'down_scenes': DOWN_SCENES,
            'uplink_scenes': UPLINK_SCENES,
            'snr_ext': SNR_EXT,
            'snr_existing_awgn_db': P.SNR_AWGN_DB,
            'snr_existing_turb_db': P.SNR_TURB_DB,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'M0': P.M0,
            'pilot_spacing': P.DA_PILOT_SPACING,
            'pilot_overhead_db': float(P.PILOT_OVERHEAD_DB),
            'laser_lw_hz': float(P.LASER_LW),
            'r_sym': float(P.R_SYM),
            'sigma2_p': float(P.SIGMA2_P),
            'hdfec': P.HDFEC,
            'seed_strategy': {
                'awgn': f'seed_base_i = SEED_AWGN({P.SEED_AWGN}) + i, i=0..{N_SEEDS-1}',
                'turb_down': f'seed0_i = SEED_TURB0({P.SEED_TURB0}) + i*N_BLOCKS({P.N_BLOCKS}), i=0..{N_SEEDS-1}',
                'turb_uplink': f'seed0_i = SEED_TURB0 + {UPLINK_SEED_OFFSET} + i*N_BLOCKS, i=0..{N_SEEDS-1}',
            },
            'algorithm_source': 'common/ via sc_nda_ml_sim.py (Formal, MVE-verified, 未改核心逻辑)',
            'simulator_unchanged': True,
            'elapsed_sec': float(elapsed),
        },
        'mve_self_check': mve_chk,
        'summary': to_jsonable(summary),
    }
    out_json = os.path.join(OUT_DIR, '_ber_ext_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 控制台汇总: 各场景 BER 最低值 ---
    print("\n" + "=" * 100)
    print(f"BER 补点 (5 seed) 各场景最低 BER:")
    print(f"{'场景':>16} {'SNR 区间':>20} {'DA_min':>12} {'NDA_min':>12} {'ORACLE_min':>12}")
    for sc in ALL_SCENES:
        pts = summary[sc]['points']
        snr_lo, snr_hi = pts[0]['snr_db'], pts[-1]['snr_db']
        da_min = min(p['da_ml_ber_mean'] for p in pts)
        nda_min = min(p['nda_ml_ber_mean'] for p in pts)
        or_min = min(p['oracle_ber_mean'] for p in pts)
        print(f"{sc:>16} {snr_lo:>7.0f}..{snr_hi:.0f} dB   "
              f"{da_min:>12.3e} {nda_min:>12.3e} {or_min:>12.3e}")
    print(f"\nNDA >= oracle: {'PASS' if mve_chk['pass'] else 'FAIL'} "
          f"(违例={mve_chk['n_violations']})")
    print(f"[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
