# -*- coding: utf-8 -*-
"""湍流场景验证: segK8 / swNw51 在 weak/moderate/strong 下是否退化或有害.

为什么跑: sandbox experiment.py 只测了 AWGN. 主实验交付是 4 场景 (AWGN + 3 湍流).
segK8 在 AWGN 反超 BPS, 但湍流场景块内 PN 被 GG 块衰落 h 掩盖, 块内跟踪可能:
  (a) 无增益 (h 衰落主导, PN 跟踪无关紧要) — 安全, 可回写;
  (b) 有害 (跟踪放大的升幂噪声在低 SNR 湍流段 dominate) — 不能盲目回写.
本脚本验证 segK8/swNw51 vs NDA-orig/BPS/oracle 在 3 湍流场景的 BER.

公平 (守 TL-13 + 纪律): 复用 generate_shared_realization_apsk (信道)、
estimate_h_blind_perblock + mmse_equalize + amp_limit (h 均衡)、
fft_foe_m0_omega (湍流两阶段 FOE)、resolve_m16apsk_blockwise.
NDA 两阶段第二阶段 nda_ml_recovery(assume_df_zero=True) 换成改进 estimator (本实验变量).

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/turb_sandbox.py
  可选 --seeds N (默认 1 = MVE seed)
"""
import os
import sys
import json
import time
import argparse

import numpy as np

# --- 路径 ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

from common import (  # noqa: E402
    generate_shared_realization_apsk,
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    mmse_equalize, amp_limit,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402
import run_bps_ablation as BPS  # noqa: E402
from params import SimulationConfig  # noqa: E402
from experiment import nda_ml_segmented, nda_ml_sliding, _to_jsonable  # noqa: E402


# =============================================================================
# 湍流改进 NDA: 两阶段 fft_foe + 改进 CPE (替换 nda_ml_recovery 那步)
# =============================================================================
def ber_nda_improved_turb(rx_eq, bits, estimator, est_kwargs):
    """湍流改进 NDA 完整评估. rx_eq 已 per-block h 均衡 + amp_limit.

    两阶段 (同 S.ber_nda_turb): (1) fft_foe_m0_omega 估 CFO 去斜; (2) 改进 estimator 估 CPE.
    estimator(seg_foe, M0, **kwargs) -> (rx_comp, phi). 逐块 + resolve.
    """
    N = len(rx_eq)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx_eq[b * P.N_DFT:(b + 1) * P.N_DFT]
        omega_est = S.fft_foe_m0_omega(seg, P.M0)
        k = np.arange(P.N_DFT)
        seg_foe = seg * np.exp(-1j * omega_est * k)
        rc, _ = estimator(seg_foe, P.M0, **est_kwargs)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 配置 (只测关键变体, 省时间)
# =============================================================================
# name -> ('orig'|'bps'|'oracle'|'improved', estimator, est_kwargs)
VARIANTS = {
    'NDA-orig':   ('orig', None, None),
    'NDA-segK8':  ('improved', nda_ml_segmented, {'K': 8}),
    'NDA-swNw51': ('improved', nda_ml_sliding, {'Nw': 51}),
    'BPS':        ('bps', None, None),
    'oracle':     ('oracle', None, None),
}


def run_turb_scene(turb_name, gamma_points, n_blocks, seed0):
    """单湍流场景 × SNR 扫描 × 5 配置. 返回 per-SNR BER 行."""
    cfg = SimulationConfig()
    Ns = P.N_DFT
    print(f"\n[{turb_name}] N_sym={n_blocks*Ns}/点, {len(VARIANTS)} 配置")
    print(f"{'γd_dB':>6}" + "".join(f"{n:>13}" for n in VARIANTS))
    per_snr = []
    for gamma_db in gamma_points:
        gamma_lin = 10 ** (gamma_db / 10)
        acc = {n: [0, 0] for n in VARIANTS}  # [n_err, n_bits]
        for b in range(n_blocks):
            r = generate_shared_realization_apsk(
                Ns, gamma_lin, turb_name, cfg.doppler.DOPPLER_HIGH,
                mod='m16apsk', seed=seed0 + b)
            rx_raw = r['rx_raw']; bits = r['bits']; phi = r['phi']
            tx_sym = r['tx']; h_true = r['h']
            # h 均衡 (盲 NDA/BPS 用 blind, oracle 用 trueh — 同主实验公平)
            h_blind = S.estimate_h_blind_perblock(rx_raw, gamma_lin)
            rx_blind = amp_limit(mmse_equalize(rx_raw, h_blind, gamma_lin), 3.0)
            rx_trueh = amp_limit(mmse_equalize(rx_raw, h_true, gamma_lin), 3.0)
            for name, (kind, est, kw) in VARIANTS.items():
                if kind == 'orig':
                    ne, nb = S.ber_nda_turb_eval(rx_blind, bits)
                elif kind == 'bps':
                    ne, nb = BPS.ber_bps_turb_eval(rx_blind, bits)
                elif kind == 'oracle':
                    ne, nb = S.ber_oracle_turb(rx_trueh, bits, phi)
                else:  # improved
                    ne, nb = ber_nda_improved_turb(rx_blind, bits, est, kw)
                acc[name][0] += ne; acc[name][1] += nb
        row = {'snr_db': float(gamma_db)}
        ber_str = f"{gamma_db:>6.0f}"
        for n in VARIANTS:
            ber = acc[n][0] / acc[n][1]
            row[n] = float(ber)
            ber_str += f"{ber:>13.4e}"
        print(ber_str)
        per_snr.append(row)
    return per_snr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=1)
    args = ap.parse_args()
    t0 = time.time()

    print("=" * 100)
    print(f"湍流场景验证: segK8/swNw51 vs NDA-orig/BPS/oracle ({args.seeds} seed × "
          f"{len(P.TURB_LEVELS)} 湍流 × {len(P.SNR_TURB_DB)} SNR)")
    print(f"变体: {list(VARIANTS.keys())}")
    print("=" * 100)

    raw = {sc: [] for sc in P.TURB_LEVELS}
    for i in range(args.seeds):
        seed0 = P.SEED_TURB0 + i * P.N_BLOCKS  # 5 seed 块范围互斥 (同主实验)
        print(f"\n########## seed {i} (seed0={seed0}) ##########")
        for turb in P.TURB_LEVELS:
            raw[turb].append(run_turb_scene(turb, P.SNR_TURB_DB, P.N_BLOCKS, seed0))

    # 聚合 mean over seeds
    names = list(VARIANTS.keys())
    summary = {}
    for turb in P.TURB_LEVELS:
        snrs = [r['snr_db'] for r in raw[turb][0]]
        pts = []
        for j, s in enumerate(snrs):
            row = {'snr_db': s}
            for n in names:
                vals = [raw[turb][seed][j][n] for seed in range(len(raw[turb]))]
                row[n + '_mean'] = float(np.mean(vals))
                if len(vals) > 1:
                    row[n + '_std'] = float(np.std(vals, ddof=1))
            pts.append(row)
        summary[turb] = {'snr_db': snrs, 'points': pts}

    # 判断: 改进 vs orig vs BPS 每点
    print("\n" + "=" * 100)
    print("判断 (改进 vs NDA-orig: 正=改进赢orig; vs BPS: 正=改进赢BPS)")
    for turb in P.TURB_LEVELS:
        print(f"\n--- {turb} ---")
        print(f"{'γd_dB':>6} {'orig':>11} {'segK8':>11} {'swNw51':>11} {'BPS':>11} "
              f"{'segK8-orig':>11} {'segK8-BPS':>11}")
        for p in summary[turb]['points']:
            o = p['NDA-orig_mean']; seg = p['NDA-segK8_mean']
            sw = p['NDA-swNw51_mean']; bps = p['BPS_mean']
            print(f"{p['snr_db']:>6.0f} {o:>11.4e} {seg:>11.4e} {sw:>11.4e} {bps:>11.4e} "
                  f"{seg-o:>+11.4e} {seg-bps:>+11.4e}")

    # 落盘
    out = {
        'meta': {
            'task': '湍流场景 segK8/swNw51 退化验证 (AWGN 已证反超, 本实验测湍流副作用)',
            'n_seeds': args.seeds,
            'turb_levels': P.TURB_LEVELS,
            'snr_turb_db': P.SNR_TURB_DB,
            'variants': list(VARIANTS.keys()),
            'fairness': '复用 generate_shared_realization_apsk + estimate_h_blind_perblock + '
                        'fft_foe_m0_omega (两阶段 FOE) + resolve. 改进只替换第二阶段 CPE.',
            'common_modified': False,
            'elapsed_sec': float(time.time() - t0),
            'python': sys.executable,
            'numpy_version': np.__version__,
        },
        'summary': _to_jsonable(summary),
        'raw_per_seed': _to_jsonable(raw),
    }
    out_json = os.path.join(_HERE, '_turb_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(_to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {time.time() - t0:.1f} s")


if __name__ == '__main__':
    main()
