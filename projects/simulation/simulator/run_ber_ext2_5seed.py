# -*- coding: utf-8 -*-
"""BER 补点实验第二轮 (5 seed): strong/uplink 三场景补到 ~50dB 探边界.

任务来源: 第一轮 ber_ext_5seed 补到 44/46dB 后, strong/uplink 衰减率 ~1.4x/2dB
(无地板但降得慢). 外推到 1e-5 需 64-81dB (远超实际工作区, 无物理意义).
用户决策: 折中方案——补到 ~50dB 探边界, 展示"仍在降只是慢"的趋势, 不硬补到 1e-5.

薄包装 (守 TL-13): 复用 S.run_turb, seed 策略与 run_ber_ext_5seed.py 一致.
只补 strong/uplink 三场景的 46/48/50dB 区间 (在第一轮 44/46dB 之上).
moderate 已破 1e-5 (8.3e-6@46dB), awgn/weak 已零错饱和, 不再补.

SNR 补点 (在第一轮之上):
  strong:          46, 48, 50 dB   (第一轮顶 44dB)
  uplink_moderate: 46, 48, 50 dB   (第一轮顶 44dB)
  uplink_strong:   48, 50 dB       (第一轮顶 46dB)

运行: cd projects/simulation && python simulator/run_ber_ext2_5seed.py
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

# --- 输出目录 (同第一轮, 汇总用) ---
OUT_DIR = os.path.join(_SIM_ROOT, 'results', 'sc_nda_ml_ber_ext_5seed')
os.makedirs(OUT_DIR, exist_ok=True)

N_SEEDS = 5

# 第二轮只补 strong/uplink 三场景的高 SNR 探边界区
SCENES = ['strong', 'uplink_moderate', 'uplink_strong']
UPLINK_SCENES = ['uplink_moderate', 'uplink_strong']
UPLINK_SEED_OFFSET = 500000  # 与 run_main_experiment_30seed.py 一致

# --- SNR 补点 (在第一轮 44/46dB 之上补到 50dB) ---
SNR_EXT = {
    'strong': [46.0, 48.0, 50.0],          # 第一轮顶 44dB
    'uplink_moderate': [46.0, 48.0, 50.0],  # 第一轮顶 44dB
    'uplink_strong': [48.0, 50.0],          # 第一轮顶 46dB
}


def seed0_turb(i, uplink=False):
    """湍流 seed i: seed0 = SEED_TURB0 [+ UPLINK_OFFSET] + i*N_BLOCKS. (同 30seed)."""
    base = P.SEED_TURB0 + (UPLINK_SEED_OFFSET if uplink else 0)
    return base + i * P.N_BLOCKS


def run_scene(scene, raw):
    """跑单场景 5 seed, 填入 raw[scene][seed_i]. 复用 S.run_turb."""
    cfg = SimulationConfig()
    snr_pts = SNR_EXT[scene]
    uplink = scene in UPLINK_SCENES
    for i in range(N_SEEDS):
        s0 = seed0_turb(i, uplink=uplink)
        print(f"\n########## {scene} seed {i} (seed0={s0}) ##########")
        raw[scene][i] = S.run_turb(scene, snr_pts, P.N_BLOCKS, cfg, s0)


def run_all():
    t0 = time.time()
    raw = {sc: {} for sc in SCENES}

    print("=" * 100)
    print(f"BER 补点第二轮 (探边界): {N_SEEDS} seed × {len(SCENES)} 场景, 补到 ~50dB")
    for sc in SCENES:
        print(f"  {sc:>16}: SNR 补点 = {SNR_EXT[sc]}")
    print("=" * 100)

    for scene in SCENES:
        run_scene(scene, raw)

    elapsed = time.time() - t0
    print(f"\n[总耗时] {elapsed:.1f} s")
    return raw, elapsed


def aggregate(raw, scenes):
    """每场景每 SNR: 5 seed BER 均值 ± std + min/max."""
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
    summary = aggregate(raw, SCENES)
    elapsed = time.time() - t0

    out = {
        'meta': {
            'task': 'BER 补点第二轮 (5 seed 探边界): strong/uplink 补到 ~50dB',
            'note': '第一轮补到 44/46dB 后衰减率 ~1.4x/2dB 无地板, 外推到 1e-5 需 64-81dB(不现实). '
                    '本轮折中补到 50dB 展示仍在降只是慢的趋势, 不硬补到 1e-5 (守 TL-22)',
            'n_seeds': N_SEEDS,
            'scenes': SCENES,
            'snr_ext': SNR_EXT,
            'N_per_point': P.N_SYM_PER_POINT,
            'N_blocks': P.N_BLOCKS,
            'laser_lw_hz': float(P.LASER_LW),
            'seed_strategy': {
                'turb_down': f'seed0_i = SEED_TURB0({P.SEED_TURB0}) + i*N_BLOCKS({P.N_BLOCKS}), i=0..{N_SEEDS-1}',
                'turb_uplink': f'seed0_i = SEED_TURB0 + {UPLINK_SEED_OFFSET} + i*N_BLOCKS, i=0..{N_SEEDS-1}',
            },
            'algorithm_source': 'common/ via sc_nda_ml_sim.py (Formal, MVE-verified, 未改核心逻辑)',
            'simulator_unchanged': True,
            'elapsed_sec': float(elapsed),
        },
        'summary': to_jsonable(summary),
    }
    out_json = os.path.join(OUT_DIR, '_ber_ext2_5seed.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")

    # --- 控制台汇总 ---
    print("\n" + "=" * 100)
    print(f"BER 补点第二轮 (探边界, 5 seed):")
    print(f"{'场景':>16} {'SNR 区间':>16} {'DA_mean':>11} {'NDA_mean':>11} {'ORACLE':>11}")
    for sc in SCENES:
        pts = summary[sc]['points']
        snr_lo, snr_hi = pts[0]['snr_db'], pts[-1]['snr_db']
        print(f"{sc:>16} {snr_lo:>5.0f}..{snr_hi:.0f} dB  ", end='')
        for p in pts:
            print(f"\n{'':>36}{p['da_ml_ber_mean']:>11.3e} {p['nda_ml_ber_mean']:>11.3e} {p['oracle_ber_mean']:>11.3e}  (SNR={p['snr_db']:.0f})", end='')
        print()
    print(f"\n[总耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
