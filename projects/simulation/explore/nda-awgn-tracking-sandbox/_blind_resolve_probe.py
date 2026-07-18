# -*- coding: utf-8 -*-
"""盲 NDA 八重相位模糊消歧探针 — oracle(tx_bits) vs blind 损失量化.

[探针 / 非正式算法] 守 sim-preflight 纪律：只在 sandbox 跑，不改 _modulation.py /
_recovery.py / _a4 脚本 / 信道参数 / 论文 / 图 / 正式 JSON。

=============================================================================
TL;DR（先读 TL-22/TL-27 前置结论）
=============================================================================
(8,8)-16APSK 星座：内环 r1·exp(j(π/8+kπ/4))，外环 r2·exp(j·kπ/4)，两环都是
**均匀 8 点环**。整个星座作为**集合**在旋转 exp(j·π/4) 下**完全不变**（核验：
set rot(pi/4)->orig max err ≈ 5e-16，机器精度）。

直接推论（TL-22 物理前提）：
  对任一接收序列 rx，"到最近星座点的欧氏距离平方和"（remod-error）在 8 个旋转下
  **逐位 bit-exact 相等**（remod std/mean = 0.000000，100% 确定性退化）。
  → 方法 (a) 重调制误差最小化 **结构性不可能**区分 8 重模糊（hit rate = chance 12.5%）。

但任务要求**实测**（不只纸笔），所以本探针仍然跑全管线，把 oracle 损失 vs 几种盲选
度量的 hit-rate / BER 损失量化，给主线程拍板。

=============================================================================
盲选方法（候选 3 种，全部不读 tx_bits）
=============================================================================
  M1: remod-error 最小化（_modulation.py:168 注释预留的"硬判决重调制误差"）。
      物理预测：完全失效（星座集合 pi/4 不变）。
  M2: 标签直方图离散度（label-histogram dispersion）。把硬判决的 16 个 label
      频次排序后，对不同旋转比"偏离均匀分布"的程度。物理预测：失效（sorted
      histogram 在 pi/4 下也是循环置换，sorted 不变；但浮点噪声会引入数值差异，
      实测看是否真的退化）。
  M3: 内环相位离散度（inner-ring phase spread）。对硬判到内环的符号，看其相位是否
      集中在内环 8 点附近。物理预测：失效（内环本身是均匀 8 点环，相位天然覆盖全
      圈，与旋转无关）。

三个候选物理上都预期失效（因星座对称性），实测确认 + 量化损失。

=============================================================================
管线（复用 _a4_switch_common768_30seed.py，只换 resolve）
=============================================================================
  generate_shared_realization_apsk (共享信道)
    → estimate_h_blind_perblock + mmse_equalize + amp_limit  → rx_blind
    → fft_foe_m0_omega + nda_ml_recovery(assume_df_zero)     → rc_nda (raw, 消歧前)
    → oracle: resolve_m16apsk_blockwise(rc_nda, tx_bits)      → res_nda_oracle
    → blind:  resolve_m16apsk_blockwise_blind(rc_nda, method) → res_nda_blind
    → m16apsk_demod → 错误数 (oracle vs blind)
损失定义：BER_blind / BER_oracle（同 block 同 seed 同信道，纯消歧差异）。

=============================================================================
纪律（brief）
=============================================================================
  - 不改 estimate/recovery/demod/信道/参数，只加盲选 resolve
  - 不改图/判据/论文/正式 JSON
  - 探针：判断死活不是定稿 CI。5 seed 先跑，看趋势再决定加 seed
  - TL-27：损失先用物理直觉估量级（八重模糊选错的概率 × 选错的 BER 惩罚）
  - TL-22：若盲选 BER ≈ oracle，先查 bug（盲选碰巧退化成 oracle / 信息泄漏）
"""
import os
import sys
import json
import time
import platform
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

import _b11_params as P
import sc_nda_ml_sim as S
from common import (
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    nda_ml_recovery,
    mmse_equalize, amp_limit,
    generate_shared_realization_apsk,
)
from params import SimulationConfig

OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')
PROBE_SCENES = ['weak', 'moderate', 'strong']
PROBE_SNR_DB = [5.0, 10.0, 15.0, 20.0]
N_SEEDS_PROBE = 5  # 探针：先 5 seed 看趋势


# ============================================================================
# 盲消歧实现（三个候选，全部不读 tx_bits）
# ============================================================================

def blind_resolve_remod(rx, block_size=256):
    """M1：重调制误差最小化（_modulation.py:168 注释预留的"硬判决众数投票"之一）。

    对每 block 试 8 个 2π/8 旋转，每个旋转 demod 后重调制，选 |rx - dec_sym|² 最小的旋转。
    **不读 tx_bits**。物理预测：完全失效（星座集合 pi/4 不变 → remod-error 在 8 旋转下 bit-exact 相等）。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    L = n_blk * block_size
    out = np.zeros(L, dtype=complex)
    rot_choice = np.zeros(n_blk, dtype=int)  # 记录每块选了哪个旋转（诊断）
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        best_err = np.inf
        best_seg = seg
        best_m = 0
        for m in range(8):
            r = m * np.pi / 4
            rotated = seg * np.exp(-1j * r)
            dec_bits = m16apsk_demod(rotated)
            dec_sym = m16apsk_mod(dec_bits)
            err = np.sum(np.abs(rotated - dec_sym) ** 2)
            if err < best_err:
                best_err = err
                best_seg = rotated
                best_m = m
        out[s] = best_seg
        rot_choice[b] = best_m
    return out, rot_choice


def blind_resolve_histdisp(rx, block_size=256):
    """M2：标签直方图离散度最小化（盲选，不读 tx_bits）。

    对每 block 试 8 旋转，硬判得 16-label，统计 label 频次直方图，
    选"最偏离均匀分布"（histogram variance 最大）的旋转。
    逻辑假设：均匀随机 bits 的 label 应该近似均匀分布；错误的旋转使判决偏向某些 label
    （因星座结构）→ 偏离均匀。物理预测：失效（sorted histogram 在 pi/4 循环置换下不变）。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    L = n_blk * block_size
    out = np.zeros(L, dtype=complex)
    rot_choice = np.zeros(n_blk, dtype=int)
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        best_score = -np.inf
        best_seg = seg
        best_m = 0
        for m in range(8):
            r = m * np.pi / 4
            rotated = seg * np.exp(-1j * r)
            dec_bits = m16apsk_demod(rotated)
            hist = np.bincount(dec_bits, minlength=16).astype(float)
            score = np.sum((hist - len(seg) / 16.0) ** 2)  # 离散度（越大越非均匀）
            if score > best_score:
                best_score = score
                best_seg = rotated
                best_m = m
        out[s] = best_seg
        rot_choice[b] = best_m
    return out, rot_choice


def blind_resolve_phasespread(rx, block_size=256):
    """M3：内环硬判符号相位离散度（盲选，不读 tx_bits）。

    对每 block 试 8 旋转，对硬判到内环（|dec|<thr）的符号取角度，看其到最近内环 8 点
    相位的残差离散度。选残差最小的旋转。
    物理预测：失效（内环是均匀 8 点环，相位天然覆盖全圈，与旋转无关）。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    L = n_blk * block_size
    out = np.zeros(L, dtype=complex)
    rot_choice = np.zeros(n_blk, dtype=int)
    inner_phases = np.pi / 8 + np.arange(8) * np.pi / 4  # 内环 8 点相位
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        best_err = np.inf
        best_seg = seg
        best_m = 0
        for m in range(8):
            r = m * np.pi / 4
            rotated = seg * np.exp(-1j * r)
            dec_bits = m16apsk_demod(rotated)
            dec_sym = m16apsk_mod(dec_bits)
            # 内环归属：硬判符号幅值 < 内外环阈值（(r1+r2)/2，与 demod 一致）
            from common._modulation import _R1_16, _R2_16
            thr_inner = 0.5 * (_R1_16 + _R2_16)
            is_inner = np.abs(dec_sym) < thr_inner
            if np.any(is_inner):
                # 接收 / 最近内环点 的残差相位，升 8 次幂去内环 8 点模糊后取方差
                phase_resid = np.angle(rotated[is_inner] / dec_sym[is_inner])
                phase_resid_wrapped = np.angle(np.exp(1j * 8 * phase_resid)) / 8
                err = np.sum(phase_resid_wrapped ** 2)
            else:
                err = np.inf
            if err < best_err:
                best_err = err
                best_seg = rotated
                best_m = m
        out[s] = best_seg
        rot_choice[b] = best_m
    return out, rot_choice


BLIND_METHODS = {
    'remod': blind_resolve_remod,
    'histdisp': blind_resolve_histdisp,
    'phasespread': blind_resolve_phasespread,
}


# ============================================================================
# 管线（复用 _a4_switch_common768_30seed.py，只换 resolve）
# ============================================================================

def per_block_oracle_vs_blind(rx_blind, bits, blind_method='remod'):
    """对同一 block，同时算 oracle 和 blind 的 NDA 错误数。

    返回 (ne_nda_oracle, ne_nda_blind, oracle_rot_match_rate, blind_rot_pick_hist)
    其中 oracle_rot_match_rate = blind 选的旋转 == oracle 选的旋转的比例（诊断盲选 vs oracle 一致性）。
    """
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    # oracle
    res_nda_oracle = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    dm_oracle = m16apsk_demod(res_nda_oracle)
    ne_oracle = int(np.sum(tb != dm_oracle))
    # blind
    res_nda_blind, _rot_choice = BLIND_METHODS[blind_method](rc_nda, block_size=P.BLOCK_SIZE_RESOLVE)
    dm_blind = m16apsk_demod(res_nda_blind)
    ne_blind = int(np.sum(tb != dm_blind))
    return ne_oracle, ne_blind


def oracle_rotation_choice(rx, tx_bits, block_size=256):
    """诊断用：返回 oracle（tx_bits）每块选的旋转索引 m∈{0..7}。

    复制 resolve_m16apsk_blockwise 的选择逻辑，但不 apply 旋转，只返回选择。
    """
    rx = np.asarray(rx, dtype=complex)
    N = len(rx)
    n_blk = N // block_size
    bits_per_sym = 4
    choice = np.zeros(n_blk, dtype=int)
    for b in range(n_blk):
        s = slice(b * block_size, (b + 1) * block_size)
        seg = rx[s]
        tb = tx_bits[b * block_size * bits_per_sym:(b + 1) * block_size * bits_per_sym]
        best_ber = 1.0
        best_m = 0
        for m in range(8):
            ber = np.mean(tb != m16apsk_demod(seg * np.exp(-1j * m * np.pi / 4)))
            if ber < best_ber:
                best_ber = ber
                best_m = m
        choice[b] = best_m
    return choice


# ============================================================================
# 主循环
# ============================================================================

def main(n_seeds=N_SEEDS_PROBE, scenes=None, snr_db=None, blind_methods=None, out_json=None):
    scenes = list(PROBE_SCENES if scenes is None else scenes)
    snr_db = [float(x) for x in (PROBE_SNR_DB if snr_db is None else snr_db)]
    blind_methods = list(blind_methods or ['remod'])
    cfg = SimulationConfig()
    NB = P.N_BLOCKS
    Ns = P.N_DFT
    t0 = time.time()
    print(f"盲消歧探针 {n_seeds} seed × {len(scenes)}场景 × {len(snr_db)}点 × "
          f"{len(blind_methods)}方法 = {n_seeds * len(scenes) * len(snr_db) * len(blind_methods)} cell")

    # 每点记录：oracle 总错误数、blind 总错误数（各方法）、n_block、elapsed
    results = {sc: [] for sc in scenes}
    # 额外：每点采一个 block 的 oracle 旋转分布（看 oracle 是否均匀选 8 旋转，即模糊是否真的均匀发生）
    oracle_rot_dist_sample = {}

    for turb in scenes:
        for i in range(n_seeds):
            s0 = P.SEED_TURB0 + i * NB
            per_snr = []
            for gdb in snr_db:
                gl = 10 ** (gdb / 10)
                # oracle 总错误数 + 各 blind 方法总错误数
                e_oracle = 0
                e_blind = {m: 0 for m in blind_methods}
                n_block_total = 0
                oracle_rot_choices_all = []  # 所有 window 的 oracle 旋转选择（诊断模糊分布）
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                                         mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']
                    hb = S.estimate_h_blind_perblock(rx_raw, gl)
                    rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                    # oracle vs blind
                    ne_o, _ = per_block_oracle_vs_blind(rxb, bits, blind_method=blind_methods[0])
                    e_oracle += ne_o
                    for m in blind_methods:
                        _, ne_b = per_block_oracle_vs_blind(rxb, bits, blind_method=m)
                        e_blind[m] += ne_b
                    n_block_total += 1
                    # 诊断：oracle 旋转选择（每 window 1 block）
                    omega = S.fft_foe_m0_omega(rxb, P.M0)
                    kk = np.arange(P.N_DFT)
                    rc_nda_diag, _, _, _ = nda_ml_recovery(rxb * np.exp(-1j * omega * kk),
                                                            P.M0, mod='m16apsk', assume_df_zero=True)
                    oracle_rot_choices_all.extend(oracle_rotation_choice(rc_nda_diag, bits[:P.N_DFT * P.BITS_PER_SYM],
                                                                          block_size=P.BLOCK_SIZE_RESOLVE).tolist())
                n_bits_per_window = Ns * P.BITS_PER_SYM  # 1024
                n_bits_total = n_block_total * n_bits_per_window
                per_snr.append({
                    'snr_db': float(gdb),
                    'n_blocks': int(n_block_total),
                    'n_bits': int(n_bits_total),
                    'oracle_errors': int(e_oracle),
                    'oracle_ber': float(e_oracle / n_bits_total),
                    'blind': {m: {
                        'errors': int(e_blind[m]),
                        'ber': float(e_blind[m] / n_bits_total),
                        'loss_ratio': float(e_blind[m] / max(e_oracle, 1)),  # blind/oracle error ratio
                        'loss_db': float(10 * np.log10((e_blind[m] / n_bits_total) / max(e_oracle / n_bits_total, 1e-12))),
                    } for m in blind_methods},
                    'oracle_rot_dist': {str(m): int(oracle_rot_choices_all.count(m)) for m in range(8)},
                })
            results[turb].append({
                'seed_index': int(i),
                'window_seed_start': int(s0),
                'per_snr': per_snr,
            })
        print(f"  {turb} done ({time.time() - t0:.0f}s)")

    elapsed = time.time() - t0

    # 聚合（跨 seed 求错误数总和，再算 BER / loss）
    summary = {}
    for sc in scenes:
        pts = []
        for j, snr in enumerate(snr_db):
            seeds = results[sc]
            o_tot = sum(s['per_snr'][j]['oracle_errors'] for s in seeds)
            n_bits = seeds[0]['per_snr'][j]['n_bits'] * len(seeds)
            rot_dist_tot = {str(m): sum(s['per_snr'][j]['oracle_rot_dist'][str(m)] for s in seeds)
                            for m in range(8)}
            entry = {
                'snr_db': float(snr),
                'n_seeds': len(seeds),
                'n_blocks_total': sum(s['per_snr'][j]['n_blocks'] for s in seeds),
                'n_bits_total': int(n_bits),
                'oracle_errors': int(o_tot),
                'oracle_ber': float(o_tot / n_bits),
                'oracle_rot_dist': rot_dist_tot,
                'oracle_rot_uniform': (max(rot_dist_tot.values()) - min(rot_dist_tot.values()))
                                       / max(max(rot_dist_tot.values()), 1),
                'blind': {},
            }
            for m in blind_methods:
                b_tot = sum(s['per_snr'][j]['blind'][m]['errors'] for s in seeds)
                b_ber = b_tot / n_bits
                entry['blind'][m] = {
                    'errors': int(b_tot),
                    'ber': float(b_ber),
                    'loss_ratio': float(b_tot / max(o_tot, 1)),
                    'loss_db': float(10 * np.log10(b_ber / max(o_tot / n_bits, 1e-12))),
                }
            pts.append(entry)
        summary[sc] = {'snr_db': [float(x) for x in snr_db], 'points': pts}

    out = {
        'meta': {
            'task': '盲 NDA 八重相位模糊消歧探针（非正式算法，sandbox 探测死活）',
            'purpose': '测盲消歧（不读 tx_bits）vs tx_bits oracle 的 BER 损失，判断死活',
            'n_seeds': n_seeds,
            'scenes': scenes,
            'snr_db': snr_db,
            'blind_methods': blind_methods,
            'n_windows_per_seed': int(NB),
            'block_size_resolve': int(P.BLOCK_SIZE_RESOLVE),
            'note': '探针非正式算法；不改正式仿真代码/论文/图/JSON',
            'physics_prior': {
                'constellation_pi4_set_invariant': True,
                'remod_error_rotation_invariant': True,
                'prediction': '方法 (a) remod-error 结构性失效（hit rate = chance 12.5%）',
            },
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'elapsed_sec': float(elapsed),
            'python_version': platform.python_version(),
            'numpy_version': np.__version__,
        },
        'summary': summary,
        'per_seed': results,
    }

    out_json = out_json or os.path.join(OUT_DIR, '_blind_resolve_probe_results.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[保存] {out_json} ({elapsed:.0f}s)")

    # 打印对照表（核心交付）
    print(f"\n{'='*100}")
    print(f"盲消歧探针：oracle(tx_bits) vs blind BER 损失（{n_seeds} seed × {NB} window/seed）")
    print(f"{'-'*100}")
    hdr = f"{'场景':<9}{'γd':>5}{'oracle BER':>12}"
    for m in blind_methods:
        hdr += f"{f'{m} BER':>12}{f'{m} loss_dB':>13}"
    print(hdr)
    print(f"{'-'*100}")
    for sc in scenes:
        for p in summary[sc]['points']:
            line = f"{sc:<9}{p['snr_db']:>5.0f}{p['oracle_ber']:>12.2e}"
            for m in blind_methods:
                bm = p['blind'][m]
                line += f"{bm['ber']:>12.2e}{bm['loss_db']:>+12.2f}dB"
            print(line)
    print(f"{'='*100}")
    print("oracle 旋转选择分布（看模糊是否真的均匀发生 in 8 rotations）:")
    for sc in scenes:
        for p in summary[sc]['points']:
            d = p['oracle_rot_dist']
            print(f"  {sc}@{p['snr_db']:.0f}dB: " + " ".join(f"m{k}:{d[str(k)]}" for k in range(8))
                  + f"  (uniform spread={p['oracle_rot_uniform']:.2f})")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=N_SEEDS_PROBE)
    ap.add_argument('--scenes', nargs='+', choices=PROBE_SCENES)
    ap.add_argument('--snr-db', nargs='+', type=float)
    ap.add_argument('--methods', nargs='+', default=['remod'],
                    choices=['remod', 'histdisp', 'phasespread'])
    ap.add_argument('--output')
    a = ap.parse_args()
    main(n_seeds=a.seeds, scenes=a.scenes, snr_db=a.snr_db,
         blind_methods=a.methods, out_json=a.output)
