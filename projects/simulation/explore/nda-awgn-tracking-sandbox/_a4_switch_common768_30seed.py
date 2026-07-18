# -*- coding: utf-8 -*-
"""A4 切换策略 — common-768 公平口径 30-seed 扫描.

**目的（R004 §3/§5 + R005 5seed 探索确认）**：在 common-768 公平口径下用 30seed
收窄 CI，定稿 selector 真实避险增益。Fig.5 现有 mixed 口径有问题（R004 G4）：
selector 选 DA 时错误计数在 768 解码数据位上累加，选 NDA 时在 1024 全部位上累加，
两边都除 1024 但比值约掉，实际是 branch-dependent error-count ratio，不是公平 BER。
R004 §3 病态退化证明：即使 selector 毫无本事，只要选了 DA 窗也会机械白送最多 1.249 dB。

本脚本把口径改成 common-768（NDA 和 selector 都只在 DA 评的那 192 个非 pilot
symbol = 768 bit 上算错误），看真实增益是多少。

**common-768 mask 定义（R004 §3 已验证，不重新定义）**：
  - pilot symbol 位置：np.arange(0,256,4)，共 64 个
  - 非 pilot symbol：其余 192 个，每个 4 bit = 768 bit
  - DA 本身只评这 768 位（ne_da 就是 common-768），DA 不重算
  - NDA 评全部 1024 位 → 新增 ne_nda_common768 = NDA demod 结果在 192 非 pilot
    symbol 上的错误数
  - selector common-768：选 DA 窗用 ne_da（=common-768），选 NDA 窗用 ne_nda_common768

**5seed 结论（R005）**：selector 真实增益集中在 weak/moderate 低 SNR 区
（0.4–1.25dB），strong 区几乎为零（mixed 的 1.3dB 几乎全是口径白送）。
扫描场景和 SNR 网格由命令行参数冻结；输出元数据必须反映实际请求的网格。

**纪律（brief）**：
  - 不改 estimate/decide/demod 逻辑（只加位计数，不重新估计）
  - 不改图/不改判据/不改参数/改正文
  - 30seed 定稿；请求网格若包含历史 mixed 锚点，则将其作为并行 sanity check
  - TL-23 守门：30seed 结果通过后可写进论文，但本轮先交主控判断不直接改正文

**两口径增益定义**（gain 正=selector 错误更少=selector 赢）：
  - mixed 口径（现有 = _a4_switch_30seed_fixed.py 的 switch_vs_nda_db_mean）：
      gain_mixed = 10·log10(Σ ne_nda_all1024 / Σ ne_sw_mixed)
    与 NDA/selector 全除 1024 等价（分母约掉）。
  - common768 口径（新）：
      gain_c768 = 10·log10(Σ ne_nda_common768 / Σ ne_sw_common768)
    NDA 和 selector 都除 (N_win × 768)，公平同口径。

**基于** `_a4_switch_common768_probe.py`（5seed 探索版）。common-768 位计数逻辑、
mixed 口径并行输出、estimate/decide/demod/判据/参数全部不变。
"""
import os
import sys
import json
import time
import hashlib
import inspect
import platform
import subprocess
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
    nda_ml_recovery, da_ml_recovery,
    mmse_equalize, amp_limit,
    generate_shared_realization_apsk,
    save_results,
)
from params import SimulationConfig
from scipy import stats
import scipy

OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')
N_SEEDS_DEFAULT = 30               # brief: 5 → 30（定稿版，收窄 CI）
GAMMA_EFF_TH = 13.0
CV_MARGIN = 1.10

# 全块 bit 分母（Bug 1 修复：mixed 口径所有方法统一用此口径）
FULL_BITS_PER_BLOCK = P.N_DFT * P.BITS_PER_SYM          # 256 × 4 = 1024
# common-768 mask：192 非 pilot symbol × 4 bit = 768 bit
N_PILOT = P.N_DFT // P.DA_PILOT_SPACING                  # 256/4 = 64 pilot symbol
COMMON768_SYMS = P.N_DFT - N_PILOT                        # 192 非 pilot symbol
COMMON768_BITS_PER_BLOCK = COMMON768_SYMS * P.BITS_PER_SYM   # 192 × 4 = 768

# 探测点缩减：weak/moderate/strong × {5,10,15} dB = 9 点（brief）
PROBE_SCENES = ['weak', 'moderate', 'strong']
PROBE_SNR_DB = [5.0, 10.0, 15.0]


def cv_awgn_theory(snr_db):
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def decide(rx_seg, gamma_db, gamma_lin):
    """两层切换判据（保留 raw 信号，见 _a4_switch_30seed_fixed.py decide docstring）.

    不改判据逻辑（brief 纪律）。判据用 raw 信号统计 CV + 盲 h。
    """
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'


def per_block(rx_blind, rx_pilot, bits, tx_sym):
    """湍流 per-block：返回 ne_nda, ne_da, ne_nda_common768（错误数）.

    不改 estimate/decide/demod 逻辑（brief 纪律），仅新增 ne_nda_common768。
      - ne_nda：NDA demod 在全部 1024 bit 上错误数（mixed 口径 NDA 分子）
      - ne_da：DA demod 在 192 非 pilot symbol = 768 bit 上错误数（= common-768，
        DA 只评这些位，pilot 不算信息错误）
      - ne_nda_common768：NDA demod 在同一 192 非 pilot symbol = 768 bit 上错误数
        （common-768 口径 NDA 分子）= 新增计数
    """
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                 pilot_sym=tx_sym[pidx], mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    dm_nda = m16apsk_demod(res_nda)                       # NDA demod（全部 256 symbol）
    ne_nda = int(np.sum(tb != dm_nda))                    # 全部 1024 bit 错误数（mixed）
    dm = m16apsk_demod(rc_da)
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dma_nda = dm_nda.reshape(P.N_DFT, P.BITS_PER_SYM)     # 新增：NDA demod reshape
    dma = dm.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tba[is_d] != dma[is_d]))           # data 位错误数 = common-768
    # 新增：NDA 在同一 192 非 pilot symbol 上的错误数 = common-768 口径 NDA 分子
    ne_nda_common768 = int(np.sum(tba[is_d] != dma_nda[is_d]))
    return ne_nda, ne_da, ne_nda_common768


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)); std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def loaded_dependency_paths():
    """Collect every loaded source module that can affect this simulation output."""
    common_root = os.path.realpath(os.path.join(_SIM_ROOT, 'common'))
    exact_files = {
        os.path.realpath(inspect.getsourcefile(SimulationConfig)),
        os.path.realpath(P.__file__),
        os.path.realpath(S.__file__),
    }
    paths = set()
    for module in tuple(sys.modules.values()):
        if module is None:
            continue
        source = getattr(module, '__file__', None)
        if not source or not source.endswith('.py'):
            continue
        source = os.path.realpath(source)
        try:
            in_common = os.path.commonpath((common_root, source)) == common_root
        except ValueError:
            # Windows raises when the loaded module and workspace use different drives.
            in_common = False
        if in_common or source in exact_files:
            paths.add(source)
    return sorted(paths)


REQUIRED_PROVENANCE_FIELDS = {
    'generated_at', 'git_head', 'git_dirty', 'script_sha256',
    'imported_file_sha256', 'seed_formula', 'python_version',
    'numpy_version', 'scipy_version', 'run_command', 'elapsed_sec',
}


def build_paper_summary(per_seed):
    """Build the sole paper estimand from paired-seed log BER ratios."""
    gains = [float(x['gain_db']) for x in per_seed]
    mean, _, _, lo, hi = ci_t(gains)
    nda_total = int(sum(x['nda_common_errors'] for x in per_seed))
    switch_total = int(sum(x['switch_common_errors'] for x in per_seed))
    assert nda_total > 0 and switch_total > 0, 'paired gain requires positive error counts'
    return {
        'estimand': 'mean paired-seed log10 BER ratio',
        'n_seeds': int(len(per_seed)),
        'mean_gain_db': mean,
        'ci95_low_db': lo,
        'ci95_high_db': hi,
        'ci_method': f'two-sided Student t, df={len(per_seed) - 1}',
        'pooled_count_gain_db': float(10 * np.log10(nda_total / switch_total)),
        'pooled_count_diagnostic_only': True,
        'diagnostic_only': True,
        'aggregate_raw_counts': {
            'n_windows': int(sum(x['n_windows'] for x in per_seed)),
            'n_bits': int(sum(x['n_bits'] for x in per_seed)),
            'nda_common_errors': nda_total,
            'switch_common_errors': switch_total,
            'common_oracle_errors': int(sum(x['common_oracle_errors'] for x in per_seed)),
            'n_select_da': int(sum(x['n_select_da'] for x in per_seed)),
            'n_select_nda': int(sum(x['n_select_nda'] for x in per_seed)),
        },
    }


def validate_authoritative_result(out, expected_scenes, expected_snrs, expected_n_seeds):
    """Deterministic T011 contract checks; raises before persistence."""
    provenance = out.get('meta', {}).get('provenance', {})
    missing = REQUIRED_PROVENANCE_FIELDS - set(provenance)
    assert not missing, f'provenance missing fields: {sorted(missing)}'
    expected_imports = {os.path.relpath(p, _SIM_ROOT) for p in loaded_dependency_paths()}
    assert set(provenance['imported_file_sha256']) == expected_imports, 'loaded dependency provenance mismatch'
    assert set(out.get('summary', {})) == set(expected_scenes), 'scene schema mismatch'
    for sc in expected_scenes:
        scene = out['summary'][sc]
        assert scene['snr_db'] == [float(x) for x in expected_snrs], 'SNR schema mismatch'
        assert len(scene['points']) == len(expected_snrs), 'point schema mismatch'
        for point, expected_snr in zip(scene['points'], expected_snrs):
            assert point['snr_db'] == float(expected_snr), 'point SNR mismatch'
            seeds = point['per_seed']
            assert len(seeds) == expected_n_seeds, 'per-seed record count mismatch'
            paper = point['paper_summary']
            expected_paper = build_paper_summary(seeds)
            for key in ('mean_gain_db', 'ci95_low_db', 'ci95_high_db', 'pooled_count_gain_db'):
                assert abs(paper[key] - expected_paper[key]) <= 1e-12, f'paper_summary {key} mismatch'
            assert paper['estimand'] == expected_paper['estimand'], 'estimand mismatch'
            assert paper['n_seeds'] == expected_n_seeds, 'paper_summary seed count mismatch'
            assert paper['pooled_count_diagnostic_only'] is True, 'pooled count must be diagnostic only'
            for seed_index, x in enumerate(seeds):
                assert x['seed_index'] == seed_index, 'seed index mismatch'
                assert x['n_windows'] == P.N_BLOCKS == 400, 'n_windows must remain 400'
                assert x['n_bits'] == 400 * COMMON768_BITS_PER_BLOCK, 'n_bits mismatch'
                expected_start = P.SEED_TURB0 + seed_index * P.N_BLOCKS
                assert x['window_seed_start'] == expected_start, 'window seed start mismatch'
                assert x['window_seed_end_inclusive'] == expected_start + P.N_BLOCKS - 1, 'window seed end mismatch'
                assert x['n_select_da'] + x['n_select_nda'] == x['n_windows'], 'branch count sum mismatch'
                assert x['switch_common_errors'] >= x['common_oracle_errors'], 'common oracle inequality violated'
                assert x['nda_common_errors'] > 0 and x['switch_common_errors'] > 0
                gain = 10 * np.log10(x['nda_common_errors'] / x['switch_common_errors'])
                assert abs(x['gain_db'] - gain) <= 1e-12, 'per-seed gain mismatch'


def build_grid_metadata(scenes, snr_db, mixed_oracle_violations, common_oracle_violations):
    """Describe the requested grid and self-checks without frozen-grid assumptions."""
    snr_text = ', '.join(f'{float(x):g}' for x in snr_db)
    scene_text = ', '.join(scenes)
    historical_anchors = {
        ('weak', 10.0): 2.3,
        ('moderate', 10.0): 2.0,
        ('strong', 5.0): 1.3,
    }
    available = [
        f'{scene}@{snr:g}≈{gain:g} dB'
        for (scene, snr), gain in historical_anchors.items()
        if scene in scenes and snr in {float(x) for x in snr_db}
    ]
    if available:
        sanity_check = (
            'mixed 口径仅作历史复现诊断；当前网格包含的锚点为 '
            + ', '.join(available)
            + '。'
        )
    else:
        sanity_check = '当前网格不含历史 mixed 锚点；以 common-768 合同自检为准。'
    awgn_note = (
        'AWGN 场景包含在请求网格中。'
        if 'awgn' in scenes
        else 'AWGN 场景未包含在请求网格中；common-768 计数逻辑与湍流场景对称。'
    )
    return {
        'sanity_check': sanity_check,
        'selfcheck_mixed_oracle_violations': int(mixed_oracle_violations),
        'selfcheck_common_oracle_violations': int(common_oracle_violations),
        'selfcheck_note': (
            'SW 是盲判据；mixed 与 common-768 两种总体分别检查 '
            'per-seed SW errors 不得低于同总体 per-block oracle errors。'
        ),
        'awgn_note': awgn_note,
        'scope_note': (
            f'{len(scenes) * len(snr_db)} points = {scene_text} × '
            f'{{{snr_text}}} dB'
        ),
    }


def main(n_seeds=N_SEEDS_DEFAULT, scenes=None, snr_db=None, out_json=None):
    scenes = list(PROBE_SCENES if scenes is None else scenes)
    snr_db = [float(x) for x in (PROBE_SNR_DB if snr_db is None else snr_db)]
    cfg = SimulationConfig()
    NB = P.N_BLOCKS; Ns = P.N_DFT
    t0 = time.time()
    print(f"A4 切换 [common-768 PROBE] {n_seeds} seed × {len(scenes)}场景 × "
          f"{len(snr_db)}点 = {n_seeds * len(scenes) * len(snr_db)} seed-point")

    raw = {sc: [] for sc in scenes}

    # Requested turbulence scenes and SNR grid.
    for turb in scenes:
        for i in range(n_seeds):
            s0 = P.SEED_TURB0 + i * NB
            per_snr = []
            for gdb in snr_db:
                gl = 10 ** (gdb / 10)
                e_n = e_d = e_s = e_o = 0
                e_n_c768 = e_s_c768 = e_o_c768 = 0
                n_select_da = n_select_nda = 0
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                                         mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
                    hb = S.estimate_h_blind_perblock(rx_raw, gl)
                    rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                    hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
                    rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
                    ne_n, ne_d, ne_n_c768 = per_block(rxb, rxp, bits, txs)   # 新增第三返回值
                    e_n += ne_n; e_d += ne_d
                    e_n_c768 += ne_n_c768                     # 新增
                    e_o += min(ne_n, ne_d)                     # per-block oracle 上界
                    e_o_c768 += min(ne_n_c768, ne_d)
                    c = decide(rx_raw, gdb, gl)
                    if c == 'da':
                        n_select_da += 1
                        e_s += ne_d
                        e_s_c768 += ne_d                        # 新增：DA 窗 = common-768（ne_d 本就是）
                    else:
                        n_select_nda += 1
                        e_s += ne_n
                        e_s_c768 += ne_n_c768                   # 新增：NDA 窗 = common-768
                n_blk_bits_full = NB * FULL_BITS_PER_BLOCK
                n_data_bits = NB * int((Ns - len(np.arange(0, Ns, P.DA_PILOT_SPACING))) * P.BITS_PER_SYM)
                n_c768_bits = NB * COMMON768_BITS_PER_BLOCK     # 新增：400 × 768
                per_snr.append({'snr_db': float(gdb),
                                # mixed 口径（同 _a4_switch_30seed_fixed.py）
                                'nda': e_n / n_blk_bits_full,
                                'da_full': e_d / n_blk_bits_full,
                                'da_data': e_d / n_data_bits,
                                'sw': e_s / n_blk_bits_full,
                                'oracle': e_o / n_blk_bits_full,
                                # 新增：common-768 口径 BER
                                'nda_c768': e_n_c768 / n_c768_bits,
                                'sw_c768': e_s_c768 / n_c768_bits,
                                # 新增：raw 错误计数（供建议主控验证）
                                'raw_ne_nda_all1024': int(e_n),
                                'raw_ne_sw_mixed': int(e_s),
                                'raw_ne_nda_common768': int(e_n_c768),
                                'raw_ne_da': int(e_d),       # DA = common-768
                                'raw_ne_sw_common768': int(e_s_c768),
                                'seed_index': int(i),
                                'window_seed_start': int(s0),
                                'window_seed_end_inclusive': int(s0 + NB - 1),
                                'n_windows': int(NB),
                                'n_bits': int(n_c768_bits),
                                'nda_common_errors': int(e_n_c768),
                                'switch_common_errors': int(e_s_c768),
                                'common_oracle_errors': int(e_o_c768),
                                'n_select_da': int(n_select_da),
                                'n_select_nda': int(n_select_nda),
                                'gain_db': float(10 * np.log10(e_n_c768 / e_s_c768)),
                                })
            raw[turb].append(per_snr)
        print(f"  {turb} done ({time.time() - t0:.0f}s)")

    elapsed = time.time() - t0

    # ============ 聚合：mixed 口径 + common-768 口径增益对照 ============
    n_violations = 0   # TL-23 自检：SW 必须 ≥ per-seed per-block-oracle
    summary = {}
    for sc in scenes:
        snrs = [p['snr_db'] for p in raw[sc][0]]
        pts = []
        for j, snr in enumerate(snrs):
            nda = [raw[sc][i][j]['nda'] for i in range(n_seeds)]
            da_full = [raw[sc][i][j]['da_full'] for i in range(n_seeds)]
            da_data = [raw[sc][i][j]['da_data'] for i in range(n_seeds)]
            sw = [raw[sc][i][j]['sw'] for i in range(n_seeds)]
            oracle = [raw[sc][i][j]['oracle'] for i in range(n_seeds)]
            nda_c768 = [raw[sc][i][j]['nda_c768'] for i in range(n_seeds)]
            sw_c768 = [raw[sc][i][j]['sw_c768'] for i in range(n_seeds)]

            m_n, *_ = ci_t(nda)
            m_d_full, *_ = ci_t(da_full)
            m_d_data, *_ = ci_t(da_data)
            m_sw, s_sw, hw_sw, lo_sw, hi_sw = ci_t(sw)
            m_o, *_ = ci_t(oracle)
            m_n_c768, *_ = ci_t(nda_c768)
            m_sw_c768, s_sw_c768, hw_sw_c768, lo_sw_c768, hi_sw_c768 = ci_t(sw_c768)

            # mixed 口径增益（= switch_vs_nda_db_mean，应复现 2.3/2.0/1.3 附近）
            # 两者同除 1024，等价于 10log10(Σe_NDA / Σe_SW)
            gain_mixed = 10 * np.log10(m_n / m_sw) if m_sw > 0 and m_n > 0 else 0.0
            # common-768 口径增益（新）：NDA 和 selector 都除 (N_win×768)，公平同口径
            gain_c768 = 10 * np.log10(m_n_c768 / m_sw_c768) if m_sw_c768 > 0 and m_n_c768 > 0 else 0.0
            # SW vs per-block oracle（TL-23 守门：可实现上界）
            gain_oracle_vs_sw = 10 * np.log10(m_sw / m_o) if m_sw > 0 and m_o > 0 else 0.0
            # per-seed 增益（粗 CI，5seed 很宽）
            g_nda_seed = [10 * np.log10(n / s) if s > 0 and n > 0 else 0.0
                          for n, s in zip(nda, sw)]
            g_c768_seed = [10 * np.log10(n / s) if s > 0 and n > 0 else 0.0
                           for n, s in zip(nda_c768, sw_c768)]
            _, _, _, lo_m, hi_m = ci_t(g_nda_seed)
            _, _, _, lo_c, hi_c = ci_t(g_c768_seed)
            mean_c, _, _, lo_c, hi_c = ci_t(g_c768_seed)

            # raw 计数总和（跨 seed，供建议主控验证）
            sum_ne_nda_all1024 = int(sum(raw[sc][i][j]['raw_ne_nda_all1024'] for i in range(n_seeds)))
            sum_ne_sw_mixed = int(sum(raw[sc][i][j]['raw_ne_sw_mixed'] for i in range(n_seeds)))
            sum_ne_nda_c768 = int(sum(raw[sc][i][j]['raw_ne_nda_common768'] for i in range(n_seeds)))
            sum_ne_da = int(sum(raw[sc][i][j]['raw_ne_da'] for i in range(n_seeds)))
            sum_ne_sw_c768 = int(sum(raw[sc][i][j]['raw_ne_sw_common768'] for i in range(n_seeds)))
            per_seed_records = [{k: raw[sc][i][j][k] for k in (
                'seed_index', 'window_seed_start', 'window_seed_end_inclusive',
                'n_windows', 'n_bits', 'nda_common_errors', 'switch_common_errors',
                'common_oracle_errors', 'n_select_da', 'n_select_nda', 'gain_db')}
                for i in range(n_seeds)]
            paper_summary = build_paper_summary(per_seed_records)

            pts.append({
                'snr_db': float(snr),
                # mixed 口径（现有）
                'mixed': {
                    'nda_ber_mean': m_n, 'sw_ber_mean': m_sw,
                    'gain_db': gain_mixed, 'gain_ci95': [lo_m, hi_m],
                },
                # common-768 口径（新）
                'common768': {
                    'nda_ber_mean': m_n_c768, 'sw_ber_mean': m_sw_c768,
                    'gain_db': mean_c, 'gain_ci95': [lo_c, hi_c],
                },
                'paper_summary': paper_summary,
                'per_seed': per_seed_records,
                'da_ber_mean_full': m_d_full, 'da_ber_mean_data': m_d_data,
                'oracle_ber_mean': m_o,
                'switch_ber_ci95': [lo_sw, hi_sw],
                'oracle_vs_switch_db_mean': gain_oracle_vs_sw,
                # raw 计数（跨 seed 总和，供建议主控验证）
                'raw_counts': {
                    'ne_nda_all1024': sum_ne_nda_all1024,
                    'ne_sw_mixed': sum_ne_sw_mixed,
                    'ne_nda_common768': sum_ne_nda_c768,
                    'ne_da': sum_ne_da,
                    'ne_sw_common768': sum_ne_sw_c768,
                },
                'per_seed_mixed_gain_db': g_nda_seed,
                'per_seed_c768_gain_db': g_c768_seed,
            })
            # TL-23 自检：SW 是盲判据，不可能赢 per-block oracle
            for o_v, s_v in zip(oracle, sw):
                if o_v > 0 and s_v < o_v * (1 - 1e-9):
                    n_violations += 1
        summary[sc] = {'snr_db': snrs, 'points': pts}

    script_path = os.path.abspath(__file__)
    imported_paths = loaded_dependency_paths()
    git_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=_SIM_ROOT, text=True).strip()
    git_dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=_SIM_ROOT, text=True).strip())
    provenance = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'git_head': git_head,
        'git_dirty': git_dirty,
        'script_sha256': sha256_file(script_path),
        'imported_file_sha256': {os.path.relpath(p, _SIM_ROOT): sha256_file(p) for p in imported_paths},
        'seed_formula': f'window_seed = {P.SEED_TURB0} + seed_index*{NB} + window_index',
        'seed_index_range': [0, int(n_seeds - 1)],
        'python_version': platform.python_version(),
        'numpy_version': np.__version__,
        'scipy_version': scipy.__version__,
        'run_command': ' '.join([sys.executable, script_path] + sys.argv[1:]),
        'elapsed_sec': float(elapsed),
    }
    common_oracle_violations = sum(
        int(seed['switch_common_errors'] < seed['common_oracle_errors'])
        for scene in summary.values()
        for point in scene['points']
        for seed in point['per_seed']
    )
    grid_metadata = build_grid_metadata(
        scenes,
        snr_db,
        mixed_oracle_violations=n_violations,
        common_oracle_violations=common_oracle_violations,
    )
    out = {
        'meta': {
            'task': 'A4 切换 common-768 公平口径探测', 'n_seeds': n_seeds,
            'scenes': scenes, 'snr_db': snr_db,
            'n_points': len(scenes) * len(snr_db),
            'gamma_eff_th': GAMMA_EFF_TH, 'cv_margin': CV_MARGIN,
            'cv_model': 'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
            'ci_method': f't-dist 95% df={n_seeds - 1}',
            'elapsed_sec': float(elapsed),
            'provenance': provenance,
            'caliber_definition': {
                'mixed': 'selector 选 DA 窗累加 ne_da(768-pop)，选 NDA 窗累加 ne_nda(1024-pop)，'
                         'NDA/selector 都除 (N_win×1024)。等价于 branch-dependent error-count ratio，'
                         '不是公平 BER（R004 §3 病态退化：选 DA 窗机械白送最多 1.249 dB）。',
                'common768': 'selector 选 DA 窗累加 ne_da(768)，选 NDA 窗累加 ne_nda_common768(768)，'
                             'NDA/selector 都除 (N_win×768)。两边在同一 768-bit 冻结 population 上，公平同口径。',
                'common768_mask': f'192 非 pilot symbol (pilot at np.arange(0,256,4)) × {P.BITS_PER_SYM} bit = 768 bit/block',
                'note': 'DA 的 ne_da 本身就是 common-768（DA 只评 192 非 pilot 位）；'
                        '新增 ne_nda_common768 = NDA demod 在同一 192 非 pilot 位的错误数。'
                        'estimate/decide/demod 逻辑未改，只加位计数。',
            },
            **grid_metadata,
        },
        'summary': summary,
    }
    validate_authoritative_result(out, scenes, snr_db, n_seeds)
    out_json = out_json or os.path.join(OUT_DIR, '_a4_switch_common768_30seed.json')
    save_results(out, out_json, os.path.basename(script_path))
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"[TL-23 自检] SW < per-seed per-block-oracle 违例数 = {n_violations}（应为 0）")

    # ============ 打印对照表（核心交付）============
    print(f"\n{'='*92}")
    print(f"{'场景':<9}{'γd':>5}{'mixed gain':>12}{'[CI95]':>14}{'c768 gain':>12}{'[CI95]':>14}{'差值':>9}{'oracle-SW':>11}")
    print(f"{'-'*92}")
    for sc in scenes:
        for p in summary[sc]['points']:
            gm = p['mixed']['gain_db']; lo_m, hi_m = p['mixed']['gain_ci95']
            gc = p['common768']['gain_db']; lo_c, hi_c = p['common768']['gain_ci95']
            orc = p['oracle_vs_switch_db_mean']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{gm:>+10.3f}dB[{lo_m:+.1f},{hi_m:+.1f}]"
                  f"{gc:>+10.3f}dB[{lo_c:+.1f},{hi_c:+.1f}]{(gm - gc):>+8.3f}{orc:>+10.2f}")
    print(f"{'='*92}")

    # raw 计数（供建议主控验证）
    print(f"\n{'='*92}")
    print("raw 错误计数（跨 {0} seed 总和，每 seed 400 block）:".format(n_seeds))
    print(f"{'场景':<9}{'γd':>5}{'nda_1024':>10}{'sw_mixed':>10}{'nda_c768':>10}{'ne_da':>8}{'sw_c768':>9}")
    print(f"{'-'*92}")
    for sc in scenes:
        for p in summary[sc]['points']:
            r = p['raw_counts']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{r['ne_nda_all1024']:>10}{r['ne_sw_mixed']:>10}"
                  f"{r['ne_nda_common768']:>10}{r['ne_da']:>8}{r['ne_sw_common768']:>9}")
    print(f"{'='*92}")
    print(f"mixed 口径 BER 验算：gain_mixed = 10log10(nda_1024/sw_mixed)")
    print(f"common768 口径 BER 验算：gain_c768 = 10log10(nda_c768/sw_c768)")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=N_SEEDS_DEFAULT)
    ap.add_argument('--scenes', nargs='+', choices=PROBE_SCENES)
    ap.add_argument('--snr-db', nargs='+', type=float)
    ap.add_argument('--output')
    a = ap.parse_args()
    main(n_seeds=a.seeds, scenes=a.scenes, snr_db=a.snr_db, out_json=a.output)
