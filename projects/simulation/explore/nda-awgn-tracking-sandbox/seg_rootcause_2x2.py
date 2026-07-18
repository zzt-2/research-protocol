# -*- coding: utf-8 -*-
"""2×2 消融: {等权, 加权} × {none, segmented} — AWGN 高 SNR 哪格异常 (segmented 根因确认).

任务 (HANDOFF brief): 上一轮 sandbox 发现 "加权 segmented" 在 AWGN 高 SNR BER 暴涨
(18dB 3.42e-3→1.28e-2, +272%), 但 "加权 none" 正常. 怀疑根因 = segmented+加权的组合.
本脚本跑 2×2 消融确认哪格异常.

四格:
  等权-none   | 等权 `rx**M0`, none (整块 mean-angle)
  等权-seg    | 等权 `rx**M0`, segmented (K=8)
  加权-none   | 加权 `(rx/|rx|)^M0 * |rx|^2`, none
  加权-seg    | 加权 `(rx/|rx|)^M0 * |rx|^2`, segmented

最高纪律:
  1. 只改本 explore/ 目录, 绝不改 common/ 或 simulator/ (本脚本只 import)
  2. 复用 ml_weighting_check.py 的 nda_weighted_recovery (加权) 和 sc_nda_ml_sim 的
     awgn_wiener_channel, 不重写信道
  3. 4 格 BER 外壳完全一致 (同 seed / 同 tx_bits / 同 awgn_wiener_channel / 同
     resolve_m16apsk_blockwise / 同 demod), 只改恢复内核

运行:
  cd projects/simulation && python explore/nda-awgn-tracking-sandbox/seg_rootcause_2x2.py
"""
import os
import sys
import json
import time
import importlib.util

import numpy as np

# --- 路径: simulation 根 (与 ml_weighting_check.py 同构) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

# 复用 common/ + simulator/ (守纪律 1,2: 只 import 不改)
from common import (  # noqa: E402
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
)
import _b11_params as P  # noqa: E402
import sc_nda_ml_sim as S  # noqa: E402  (awgn_wiener_channel, ber_nda_awgn, nda_ml_recovery)

# 从 ml_weighting_check.py 复用加权恢复内核 (目录名含连字符, 按 spec 加载)
_spec = importlib.util.spec_from_file_location(
    '_mlwc', os.path.join(_HERE, 'ml_weighting_check.py'))
_mlwc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mlwc)
nda_weighted_recovery = _mlwc.nda_weighted_recovery  # 加权 none/seg 内核


# =============================================================================
# 4 个 recovery 内核 (都返回 rx_comp, 签名 (seg, M0) -> rx_comp). 公式逐字 brief §2.
# =============================================================================
def rec_eq_none(seg, M0):
    """等权-none: raised=rx**M0; phi=angle(raised.mean())/M0; rx*exp(-1j*phi).

    与 common/_recovery.py nda_ml_recovery(assume_df_zero=True, intra='none') 等价
    (raised=rx**M0 整块 mean-angle). 此处手写一份以保证 4 格内核结构对齐.
    """
    seg = np.asarray(seg, dtype=complex)
    raised = seg ** M0
    phi_est = np.angle(raised.mean()) / M0
    return seg * np.exp(-1j * phi_est)


def rec_eq_seg(seg, M0):
    """等权-seg: raised=rx**M0; K=8 段 angle(raised[lo:hi].mean())/M0; unwrap; interp.

    与 common/_recovery.py nda_ml_recovery(assume_df_zero=True, intra='segmented')
    bit-exact 等价 (raised=rx**M0 段内 mean-angle). 此处手写以与加权-seg 对齐结构
    (差异仅在 raised.mean() vs (w*yn).sum()).
    """
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    raised = seg ** M0
    K = 8
    seg_len = N // K
    seg_phi = np.empty(K)
    seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k * seg_len, (k + 1) * seg_len
        seg_phi[k] = np.angle(raised[lo:hi].mean()) / M0   # 先 /M0 (对齐加权 seg)
        seg_center[k] = (lo + hi) / 2.0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_est = np.interp(t, seg_center, seg_phi_unw)
    return seg * np.exp(-1j * phi_est)


def rec_w_none(seg, M0):
    """加权-none: yn=(rx/|rx|)^M0, w=|rx|^2; phi=angle((w*yn).sum())/M0."""
    return nda_weighted_recovery(seg, M0, mode='none')


def rec_w_seg(seg, M0):
    """加权-seg: K=8 段 (w*yn).sum() → /M0 → unwrap → interp."""
    return nda_weighted_recovery(seg, M0, mode='segmented')


# =============================================================================
# 统一 BER 外壳: 4 格共用. 逐 N_DFT 块 recovery_fn → resolve_m16apsk_blockwise → demod.
# 与 ml_weighting_check.ber_nda_weighted_awgn / S.ber_nda_awgn 结构逐字对齐.
# =============================================================================
def ber_eval(rx, tx_bits, recovery_fn, M0=P.M0):
    """统一 BER 外壳. 逐块 recovery_fn(seg, M0) → resolve → demod. 返回 (n_err, n_bits)."""
    N = len(rx)
    n_blk = N // P.N_DFT
    L = n_blk * P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = recovery_fn(seg, M0)
    tb = tx_bits[:L * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


# =============================================================================
# 2×2 消融 sweep (单 seed, AWGN 高 SNR). 4 格共用同一 rx (公平前提).
# =============================================================================
def run_2x2(n_blocks, snr_points, seed_base):
    """2×2: {等权,加权}×{none,segmented}, 单 seed. 4 格共用同一 rx.

    seed 派生对齐 ml_weighting_check.run_awgn_three_way / S.run_awgn.
    返回 list[dict] (每 SNR 点含 4 格 BER + 比率).
    """
    N_sym = n_blocks * P.N_DFT
    cells = [
        ('eq_none', rec_eq_none),
        ('eq_seg',  rec_eq_seg),
        ('w_none',  rec_w_none),
        ('w_seg',   rec_w_seg),
    ]
    print(f"\n[2×2 消融] N_sym={N_sym}/点, M0={P.M0}, seed_base={seed_base}")
    print(f"{'SNR_dB':>7} {'eq_none':>12} {'eq_seg':>12} {'w_none':>12} {'w_seg':>12}   "
          f"{'w_seg/eq_seg':>12}")
    per_snr = []
    for snr in snr_points:
        seed = seed_base + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        # 同一 rx 给 4 格 (公平前提 — 同 awgn_wiener_channel 调用)
        rx, _phi_true = S.awgn_wiener_channel(tx, snr, seed)
        row = {'snr_db': float(snr)}
        for name, fn in cells:
            ne, nb = ber_eval(rx, bits, fn)
            row[f'ber_{name}'] = ne / nb
        b_eq_seg = row['ber_eq_seg']
        ratio = (row['ber_w_seg'] / b_eq_seg) if b_eq_seg > 0 else float('nan')
        row['ratio_w_seg_over_eq_seg'] = float(ratio)
        print(f"{snr:>7.0f} {row['ber_eq_none']:>12.4e} {row['ber_eq_seg']:>12.4e} "
              f"{row['ber_w_none']:>12.4e} {row['ber_w_seg']:>12.4e}   {ratio:>12.3f}")
        per_snr.append(row)
    return per_snr


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
    print("=" * 100)
    print("2×2 消融: {等权,加权}×{none,segmented} — AWGN 高 SNR segmented 根因确认")
    print(f"M0={P.M0}, LASER_LW={P.LASER_LW/1e3:.0f}kHz, single seed={P.SEED_AWGN}, "
          f"N_BLOCKS={P.N_BLOCKS}")
    print("4 格: eq_none(等权整块mean-angle) / eq_seg(等权K=8) / "
          "w_none(加权整块) / w_seg(加权K=8)")
    print("公平: 4 格同 seed / 同 tx_bits / 同 awgn_wiener_channel / 同 resolve / 同 demod")
    print("=" * 100)

    # SNR = [16,18,20] dB (高 SNR, 异常区). n_blocks 用 P.N_BLOCKS (与上一轮对齐)
    snr_points = [16.0, 18.0, 20.0]
    pts = run_2x2(P.N_BLOCKS, snr_points, P.SEED_AWGN)

    # --- 异常格判定 (供分类, 不替决策) ---
    # 加权-seg > 2× 等权-seg → seg 不适合配加权
    w_seg_anomalous = []
    for p in pts:
        r = p['ratio_w_seg_over_eq_seg']
        if r > 2.0:
            w_seg_anomalous.append((p['snr_db'], r))
    # 加权-none 异常?
    w_none_anomalous = []
    for p in pts:
        if p['ber_eq_none'] > 0 and (p['ber_w_none'] / p['ber_eq_none']) > 2.0:
            w_none_anomalous.append((p['snr_db'], p['ber_w_none'] / p['ber_eq_none']))
    # 等权-seg 异常?
    eq_seg_anomalous = []
    for p in pts:
        if p['ber_eq_none'] > 0 and (p['ber_eq_seg'] / p['ber_eq_none']) > 2.0:
            eq_seg_anomalous.append((p['snr_db'], p['ber_eq_seg'] / p['ber_eq_none']))

    diagnosis = {
        'w_seg_gt_2x_eq_seg': w_seg_anomalous,
        'w_none_gt_2x_eq_none': w_none_anomalous,
        'eq_seg_gt_2x_eq_none': eq_seg_anomalous,
    }
    if w_seg_anomalous and not w_none_anomalous and not eq_seg_anomalous:
        diag_cat = 'seg_incompatible_with_weighting'
    elif w_none_anomalous:
        diag_cat = 'weighting_formula_problem_in_awgn'
    elif eq_seg_anomalous:
        diag_cat = 'segmented_high_snr_hazard'
    else:
        diag_cat = 'no_anomaly'
    diagnosis['category'] = diag_cat

    print("\n" + "=" * 100)
    print("异常格判定 (分类用, 不替决策):")
    print(f"  category = {diag_cat}")
    print(f"  w_seg > 2× eq_seg 的 SNR 点: {w_seg_anomalous}")
    print(f"  w_none > 2× eq_none 的 SNR 点: {w_none_anomalous}")
    print(f"  eq_seg > 2× eq_none 的 SNR 点: {eq_seg_anomalous}")

    # --- 落盘 JSON ---
    elapsed = time.time() - t0
    out = {
        'meta': {
            'task': '2×2 消融 {等权,加权}×{none,segmented} AWGN 高 SNR — segmented 根因确认',
            'cells': {
                'eq_none': '等权 rx**M0, none (整块 mean-angle)',
                'eq_seg': '等权 rx**M0, segmented (K=8 段 mean-angle /M0 unwrap interp)',
                'w_none': '加权 (rx/|rx|)^M0, w=|rx|^2, none (整块 (w*yn).sum())',
                'w_seg': '加权 (rx/|rx|)^M0, w=|rx|^2, segmented (K=8 段 (w*yn).sum())',
            },
            'fairness': '4 格同 seed / 同 tx_bits / 同 awgn_wiener_channel / 同 resolve_m16apsk_blockwise / 同 m16apsk_demod',
            'ber_shell': 'ber_eval: 逐 N_DFT 块 recovery_fn(seg,M0) → resolve → demod (4 格统一)',
            'M0': P.M0,
            'N_DFT': P.N_DFT,
            'N_BLOCKS': P.N_BLOCKS,
            'K_seg': 8,
            'seed_awgn': P.SEED_AWGN,
            'snr_points_db': snr_points,
            'HDFEC': P.HDFEC,
            'LASER_LW_Hz': float(P.LASER_LW),
            'common_or_simulator_modified': False,
            'reuse': 'nda_weighted_recovery (加权) from ml_weighting_check.py; awgn_wiener_channel / ber_nda_awgn from sc_nda_ml_sim',
            'python': sys.executable,
            'numpy_version': np.__version__,
            'elapsed_sec': float(elapsed),
        },
        'results': pts,
        'diagnosis': diagnosis,
    }
    out_json = os.path.join(_HERE, '_seg_rootcause_2x2.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(to_jsonable(out), f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_json}")
    print(f"[耗时] {elapsed:.1f} s")


if __name__ == '__main__':
    main()
