# -*- coding: utf-8 -*-
"""独立 verifier：路线 B (branch-routed) vs 路线 A (error-count mux) bit-exact 等价性核查.

**授权范围**：只读核查，不改算法/参数/论文/图。核查 B 的 branch-routed 实现
（_a4_branchrouted_30seed.py）是否与 A 的权威实现（_a4_switch_common768_30seed.py）
在 selector 端量上 bit-exact 等价，并实测 branch compute wall-clock 比。

**核查项（R013 §5-B 预注册验证 PASS 标准）**：
  1. 逐 seed switch_common_errors (e_s_c768) 与 A 权威 JSON bit-exact 一致（容差 1e-12，
     实为整数严格相等）
  2. 逐 seed n_select_da / n_select_nda 与 A 一致 + n_select_da + n_select_nda = 400
  3. selector common-768 BER 统计（paper_summary selector_c768_ber_*）自洽重算
  4. selected_rx 提取验证：重跑样本窗，确认 DA 窗 selected_rx == rc_da，NDA 窗 == res_nda
     （shape=(256,) complex）
  5. branch compute wall-clock 比：B（单路）vs A（两路全跑）per-window 实测（不报理论值）

**结构性边界（用户确认「忠实 branch-routed」，非实现错误）**：
  - NDA-only fixed-branch BER / per-block oracle / gain_db = NDA/selector 在 branch-routed 下
    不可得（需两路全跑），不在等价性核查范围，仅在报告里标注 N/A
  - 等价性 = selector 端量 bit-exact，不是「所有 A 字段都在 B 中复现」

**输出**：_verify_b_vs_a_equiv_report.json（PASS/FAIL + 逐项核查结果 + 不一致根因）
"""
import os
import sys
import json
import time
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
    m16apsk_demod, resolve_m16apsk_blockwise,
    nda_ml_recovery, da_ml_recovery,
    mmse_equalize, amp_limit, generate_shared_realization_apsk,
)
from params import SimulationConfig

# B 版 per_block 分支函数（import 被验证脚本本身）
sys.path.insert(0, _HERE)
import _a4_branchrouted_30seed as B

A_JSON = os.path.join(_HERE, '_a4_switch_common768_30seed_snr5_25_step2.json')
B_JSON = os.path.join(_HERE, '_a4_branchrouted_30seed_snr5_25_step2.json')
REPORT_JSON = os.path.join(_HERE, '_verify_b_vs_a_equiv_report.json')
TOL = 1e-12


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_grid_schema(a, b):
    """核查 A/B 网格 schema 一致（scenes / snr_db / n_seeds / n_points）。"""
    am, bm = a['meta'], b['meta']
    checks = {
        'scenes': am['scenes'] == bm['scenes'],
        'n_seeds': am['n_seeds'] == bm['n_seeds'],
        'n_points': am['n_points'] == bm['n_points'],
        'snr_db_equal': [float(x) for x in am['snr_db']] == [float(x) for x in bm['snr_db']],
    }
    return checks


def check_bitexact_selector(a, b):
    """逐 scene × snr × seed 核查 selector 端量 bit-exact.

    核查字段（branch-routed 可得且应与 A bit-exact）：
      - switch_common_errors（e_s_c768）：整数严格相等
      - n_select_da / n_select_nda：整数严格相等
      - window_seed_start / window_seed_end_inclusive / n_windows：整数严格相等
    """
    scenes = a['meta']['scenes']
    results = {'per_point': [], 'n_checked': 0, 'n_match': 0, 'mismatches': []}
    for sc in scenes:
        a_pts = a['summary'][sc]['points']
        b_pts = b['summary'][sc]['points']
        assert len(a_pts) == len(b_pts), f'{sc} point count mismatch'
        for ap, bp in zip(a_pts, b_pts):
            assert abs(ap['snr_db'] - bp['snr_db']) <= TOL, 'snr mismatch'
            a_seeds = ap['per_seed']
            b_seeds = bp['per_seed']
            assert len(a_seeds) == len(b_seeds), 'seed count mismatch'
            for a_s, b_s in zip(a_seeds, b_seeds):
                results['n_checked'] += 1
                field_cmp = {}
                for fld in ('switch_common_errors', 'n_select_da', 'n_select_nda',
                            'window_seed_start', 'window_seed_end_inclusive', 'n_windows'):
                    av, bv = a_s[fld], b_s[fld]
                    ok = (av == bv)
                    field_cmp[fld] = {'A': av, 'B': bv, 'match': ok}
                # n_select_da + n_select_nda == n_windows
                sel_sum_ok = (b_s['n_select_da'] + b_s['n_select_nda'] == b_s['n_windows'])
                all_match = all(fc['match'] for fc in field_cmp.values()) and sel_sum_ok
                if all_match:
                    results['n_match'] += 1
                else:
                    results['mismatches'].append({
                        'scene': sc, 'snr_db': bp['snr_db'], 'seed_index': b_s['seed_index'],
                        'field_cmp': field_cmp, 'sel_sum_ok': sel_sum_ok,
                    })
                results['per_point'].append({
                    'scene': sc, 'snr_db': bp['snr_db'], 'seed_index': b_s['seed_index'],
                    'all_match': all_match, 'sel_sum_ok': sel_sum_ok, 'field_cmp': field_cmp,
                })
    return results


def check_selected_rx_extraction(cfg):
    """重跑样本窗，确认 DA 窗 selected_rx == rc_da，NDA 窗 == res_nda（shape=(256,) complex）.

    在 weak@5dB 跑前 20 窗（seed0），逐窗验证：
      - decide 提前后 decide 结果与 A 调用方式一致（decide 只读 rx_raw/gdb/gl）
      - 选 DA 窗：B 的 per_block_da 输出 == 独立重算的 da_ml_recovery rc_da
      - 选 NDA 窗：B 的 per_block_nda 输出 res_nda == 独立重算的 resolve(nda_ml_recovery)
    """
    Ns = P.N_DFT
    turb = 'weak'
    gdb = 5.0
    gl = 10 ** (gdb / 10)
    s0 = P.SEED_TURB0
    n_test = 20
    results = {'windows_checked': 0, 'da_windows': 0, 'nda_windows': 0,
               'da_match': 0, 'nda_match': 0, 'shape_ok': 0, 'errors': []}
    for b_idx in range(n_test):
        r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                             mod='m16apsk', seed=s0 + b_idx)
        rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
        c = B.decide(rx_raw, gdb, gl)
        if c == 'da':
            results['da_windows'] += 1
            # 独立重算 DA 路
            hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
            rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
            ne_d_b, rc_da_b = B.per_block_da(rxp, bits, txs)
            # 独立参考（手写，不复用 B 函数）
            pidx = np.arange(0, Ns, P.DA_PILOT_SPACING)
            rc_da_ref, _, _ = da_ml_recovery(rxp, pilot_idx=pidx,
                                             pilot_sym=txs[pidx], mod='m16apsk')
            match = np.array_equal(rc_da_b, rc_da_ref)
            shape_ok = rc_da_b.shape == (Ns,) and np.iscomplexobj(rc_da_b)
            if match and shape_ok:
                results['da_match'] += 1
            else:
                results['errors'].append({'window': b_idx, 'branch': 'da',
                                          'match': match, 'shape_ok': shape_ok})
            results['shape_ok'] += int(shape_ok)
        else:
            results['nda_windows'] += 1
            # 独立重算 NDA 路
            hb = S.estimate_h_blind_perblock(rx_raw, gl)
            rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
            ne_n_b, ne_n_c768_b, res_nda_b = B.per_block_nda(rxb, bits)
            # 独立参考
            omega = S.fft_foe_m0_omega(rxb, P.M0)
            k = np.arange(Ns)
            rc_nda_ref, _, _, _ = nda_ml_recovery(rxb * np.exp(-1j * omega * k),
                                                  P.M0, mod='m16apsk', assume_df_zero=True)
            tb = bits[:Ns * P.BITS_PER_SYM]
            res_nda_ref = resolve_m16apsk_blockwise(rc_nda_ref, tb, block_size=P.BLOCK_SIZE_RESOLVE)
            match = np.array_equal(res_nda_b, res_nda_ref)
            shape_ok = res_nda_b.shape == (Ns,) and np.iscomplexobj(res_nda_b)
            if match and shape_ok:
                results['nda_match'] += 1
            else:
                results['errors'].append({'window': b_idx, 'branch': 'nda',
                                          'match': match, 'shape_ok': shape_ok})
            results['shape_ok'] += int(shape_ok)
        results['windows_checked'] += 1
    return results


def measure_branch_compute_wallclock(cfg, n_windows=400):
    """实测 branch compute wall-clock：B（单路）vs A（两路全跑）per-window.

    在 weak@5dB seed0 跑 400 窗，分别计时：
      - B branch compute = decide 后只跑被选分支（h+均衡+recovery+demod/resolve）
      - A branch compute = 两路 h+均衡+recovery+demod/resolve 全跑（_a4_switch 原结构）
    channel generation 两版相同，不计入。报告实测 wall-clock 比，不报理论值。
    """
    Ns = P.N_DFT
    turb = 'weak'
    gdb = 5.0
    gl = 10 ** (gdb / 10)
    s0 = P.SEED_TURB0

    # 预生成信道实现（两版共用，不计入 branch compute 计时）
    realizations = []
    for b_idx in range(n_windows):
        r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                             mod='m16apsk', seed=s0 + b_idx)
        realizations.append(r)

    # --- B branch compute（单路）---
    t_b0 = time.perf_counter()
    for r in realizations:
        rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
        c = B.decide(rx_raw, gdb, gl)
        if c == 'da':
            hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
            rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
            B.per_block_da(rxp, bits, txs)
        else:
            hb = S.estimate_h_blind_perblock(rx_raw, gl)
            rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
            B.per_block_nda(rxb, bits)
    t_b = time.perf_counter() - t_b0

    # --- A branch compute（两路全跑，复刻 _a4_switch per_block 的两路结构）---
    def a_both_branches(rx_blind, rx_pilot, bits, tx_sym):
        """复刻 _a4_switch_common768_30seed.py:per_block 两路全跑（:120-138）。"""
        omega = S.fft_foe_m0_omega(rx_blind, P.M0)
        k = np.arange(P.N_DFT)
        rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                          P.M0, mod='m16apsk', assume_df_zero=True)
        pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
        rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                     pilot_sym=tx_sym[pidx], mod='m16apsk')
        tb = bits[:P.N_DFT * P.BITS_PER_SYM]
        res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
        m16apsk_demod(res_nda)
        m16apsk_demod(rc_da)

    t_a0 = time.perf_counter()
    for r in realizations:
        rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
        # A 结构：两路 h + 均衡 + per_block 两路全跑（decide 在 per_block 之后）
        hb = S.estimate_h_blind_perblock(rx_raw, gl)
        rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
        hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
        rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
        a_both_branches(rxb, rxp, bits, txs)
    t_a = time.perf_counter() - t_a0

    return {
        'n_windows': n_windows,
        'scene': f'{turb}@{gdb}dB seed0',
        'A_two_branch_sec': float(t_a),
        'A_per_window_sec': float(t_a / n_windows),
        'B_single_branch_sec': float(t_b),
        'B_per_window_sec': float(t_b / n_windows),
        'wallclock_ratio_B_over_A': float(t_b / t_a) if t_a > 0 else None,
        'savings_pct': float((1.0 - t_b / t_a) * 100.0) if t_a > 0 else None,
        'note': '实测 wall-clock（仅 branch compute，不含信道生成）；不报理论值。'
                'A = 两路 h+均衡+recovery+demod/resolve 全跑；B = decide 后只跑被选分支。',
    }


def check_paper_summary_self_consistency(b):
    """核查 B 的 paper_summary selector BER 统计自洽重算（branch-routed 可得项）。"""
    scenes = b['meta']['scenes']
    results = {'per_point': [], 'all_consistent': True}
    for sc in scenes:
        for pt in b['summary'][sc]['points']:
            seeds = pt['per_seed']
            rates = [s['switch_common_errors'] / s['n_bits'] for s in seeds]
            mean = float(np.mean(rates))
            n = len(rates)
            std = float(np.std(rates, ddof=1)) if n > 1 else 0.0
            from scipy import stats as st
            hw = float(st.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
            lo, hi = mean - hw, mean + hw
            paper = pt['paper_summary']
            consistent = (
                abs(paper['selector_c768_ber_mean'] - mean) <= TOL
                and abs(paper['selector_c768_ber_ci95'][0] - lo) <= TOL
                and abs(paper['selector_c768_ber_ci95'][1] - hi) <= TOL
            )
            results['per_point'].append({
                'scene': sc, 'snr_db': pt['snr_db'],
                'selector_c768_ber_mean': paper['selector_c768_ber_mean'],
                'recomputed_mean': mean, 'consistent': consistent,
            })
            if not consistent:
                results['all_consistent'] = False
    return results


def main():
    print('=' * 80)
    print('verifier: 路线 B (branch-routed) vs 路线 A (error-count mux) bit-exact 等价核查')
    print('=' * 80)
    cfg = SimulationConfig()

    if not os.path.exists(A_JSON):
        print(f'[FAIL] A 权威 JSON 不存在: {A_JSON}')
        return
    if not os.path.exists(B_JSON):
        print(f'[FAIL] B JSON 不存在（B 网格未跑完）: {B_JSON}')
        return
    a = load_json(A_JSON)
    b = load_json(B_JSON)

    report = {'A_json': os.path.basename(A_JSON), 'B_json': os.path.basename(B_JSON),
              'tol': TOL, 'checks': {}}

    # --- 核查 1: 网格 schema ---
    schema = check_grid_schema(a, b)
    report['checks']['grid_schema'] = schema
    print(f"\n[1] 网格 schema: {'PASS' if all(schema.values()) else 'FAIL'} {schema}")

    # --- 核查 2: 逐 seed selector 端 bit-exact ---
    bitexact = check_bitexact_selector(a, b)
    report['checks']['bitexact_selector'] = {
        'n_checked': bitexact['n_checked'],
        'n_match': bitexact['n_match'],
        'pass': bitexact['n_checked'] == bitexact['n_match'],
        'n_mismatches': len(bitexact['mismatches']),
        'mismatches': bitexact['mismatches'][:10],  # 只记前 10 个
    }
    print(f"[2] 逐 seed selector bit-exact: {bitexact['n_match']}/{bitexact['n_checked']} match "
          f"({'PASS' if bitexact['n_match'] == bitexact['n_checked'] else 'FAIL'})")
    if bitexact['mismatches']:
        print(f"    首个 mismatch: {bitexact['mismatches'][0]}")

    # --- 核查 3: selected_rx 提取 ---
    sel_rx = check_selected_rx_extraction(cfg)
    report['checks']['selected_rx_extraction'] = sel_rx
    da_ok = sel_rx['da_windows'] == sel_rx['da_match']
    nda_ok = sel_rx['nda_windows'] == sel_rx['nda_match']
    print(f"[3] selected_rx 提取: DA 窗 {sel_rx['da_match']}/{sel_rx['da_windows']} match, "
          f"NDA 窗 {sel_rx['nda_match']}/{sel_rx['nda_windows']} match, "
          f"shape_ok {sel_rx['shape_ok']}/{sel_rx['windows_checked']} "
          f"({'PASS' if da_ok and nda_ok else 'FAIL'})")

    # --- 核查 4: paper_summary 自洽 ---
    ps = check_paper_summary_self_consistency(b)
    report['checks']['paper_summary_self_consistency'] = ps
    print(f"[4] paper_summary 自洽: {'PASS' if ps['all_consistent'] else 'FAIL'} "
          f"({len(ps['per_point'])} points)")

    # --- 核查 5: branch compute wall-clock 比 ---
    bc = measure_branch_compute_wallclock(cfg, n_windows=400)
    report['checks']['branch_compute_wallclock'] = bc
    print(f"[5] branch compute wall-clock ({bc['scene']}, {bc['n_windows']} windows):")
    print(f"    A 两路全跑: {bc['A_per_window_sec']*1e3:.3f} ms/win ({bc['A_two_branch_sec']:.3f}s 总)")
    print(f"    B 单路:     {bc['B_per_window_sec']*1e3:.3f} ms/win ({bc['B_single_branch_sec']:.3f}s 总)")
    print(f"    B/A 比 = {bc['wallclock_ratio_B_over_A']:.3f}  → 实测节省 {bc['savings_pct']:.1f}%")

    # --- 总判定 ---
    overall = (
        all(schema.values())
        and bitexact['n_match'] == bitexact['n_checked']
        and da_ok and nda_ok
        and ps['all_consistent']
    )
    report['overall'] = 'PASS' if overall else 'FAIL'
    report['overall_criteria'] = {
        'grid_schema_match': all(schema.values()),
        'selector_bitexact': bitexact['n_match'] == bitexact['n_checked'],
        'selected_rx_extraction': bool(da_ok and nda_ok),
        'paper_summary_consistency': ps['all_consistent'],
    }
    report['structural_limits_NA'] = {
        'nda_only_baseline': 'branch-routed 下 NDA-only fixed-branch BER 不可得（需 NDA 全跑 400 窗）',
        'per_block_oracle': 'branch-routed 下 per-block oracle = min(ne_n,ne_d) 不可得（需两路同窗）',
        'gain_db': 'branch-routed 下 gain_db = 10log10(nda/sw) 不可得（需 NDA-only 全窗总和）',
    }
    print(f"\n{'='*80}")
    print(f"总判定: {report['overall']}")
    print(f"  selector 端 bit-exact 等价: {report['overall_criteria']['selector_bitexact']}")
    print(f"  selected_rx 提取: {report['overall_criteria']['selected_rx_extraction']}")
    print(f"  实测 branch compute 节省: {bc['savings_pct']:.1f}% (B/A={bc['wallclock_ratio_B_over_A']:.3f})")
    print(f"  结构性 N/A: NDA-only baseline / per-block oracle / gain_db（非实现错误）")
    print(f"{'='*80}")

    with open(REPORT_JSON, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=_json_default)
    print(f"[保存] {REPORT_JSON}")


def _json_default(o):
    """numpy 类型 → Python 原生类型（np.bool_/np.integer/np.floating/np.ndarray）。"""
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


if __name__ == '__main__':
    main()
