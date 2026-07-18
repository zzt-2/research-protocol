# -*- coding: utf-8 -*-
"""A4 切换策略 — branch-routed receiver (路线 B) 30-seed 扫描.

**目的（R013 §1-B / DRAFT CCE-SEL-002）**：在 _a4_switch_common768_30seed.py（路线 A，
error-count mux：两路全跑，selector 只累加错误计数）基础上实现路线 B = "控制器先决策、
每窗只跑被选 CPR 分支"，并验证 B 与 A bit-exact 等价 + 实测分支计算节省。

路线 B 相对 A 的两点增量（R013 §1-B / §3-B delta）：
  1. per_block 返回 selected 复数序列（rc_da 或 res_nda 之一）—— 这是 A 的部分
     （R013 §1-A：selected 对象从错误计数提升为复数序列）
  2. decide() 提前到两路 recovery 之前，每窗只执行被选分支 —— 这是 B 相对 A 的增量

**等价性前提（R013 §1-B + §5-B 预注册，本轮 Step 0 已独立核验 PASS）**：
  - decide() 判据数据独立于 branch output（只读 rx_raw 功率统计 + nominal SNR，
    _a4_switch_common768_30seed.py:97-107），decide 提前后输入不变（rx_raw 在
    原 :324 已得，gdb/gl 在 :316-317 已得）
  - estimate_h_blind_perblock / estimate_h_pilot_perblock 确定性（无随机性）：
    sc_nda_ml_sim.py:95-110 / :113-130，纯 numpy 无 RNG → decide 提前后调用顺序变化
    不改变 h 估计结果
  - recovery/demod/resolve 全确定性（nda_ml_recovery / da_ml_recovery /
    resolve_m16apsk_blockwise / m16apsk_demod 均无随机性）
  → B 的逐窗错误计数应与 A bit-exact 等价。**默认预测 = 零 BER 不一致**，
    任何不一致优先视为实现错误，不写成算法增益。

**结构差异（相对 A）**：
  - B 每窗只跑被选分支（DA 窗只跑 pilot h + da_ml_recovery + demod；NDA 窗只跑
    blind h + fft_foe + nda_ml_recovery + resolve + demod），selected_rx = rc_da 或
    res_nda
  - **per-block oracle 不可计算**：A 的 e_o/e_o_c768 = min(ne_n, ne_d) 需同时跑两路，
    B 只跑一路 → common_oracle_errors 字段标 N/A（结构上不可得，非实现错误）
  - 新增 per-window branch compute 计时（A 两路全跑 vs B 单路），实测 wall-clock 比

**不改（硬边界，R013 §3-B / 本轮纪律）**：
  - decide() 判据、recovery/demod/resolve 算法逻辑、信道参数、seed、窗口数（400）、
    common-768 mask、两口径增益定义（mixed / common768）—— 全部与 A 一致

**纪律**：
  - 不声称 BER 增益（B 默认与 A bit-exact）；任何不一致优先查实现错误
  - 不声称可部署（NDA 仍用 tx_bits 消歧 resolve_m16apsk_blockwise，genie-aided 保留）
  - 计算节省只报实测 wall-clock 比，不报理论值
  - 守 FR-22：B 是 implementation repair（控制流重构，不改算法），不触发 Groundwork/Contract
  - sim-preflight 5 条核心全守（共用信道/参数溯源/save_results/provenance 自检）

**基于** `_a4_switch_common768_30seed.py`（路线 A 权威版）。common-768 mask、mixed/common768
两口径、estimate/decide/demod/resolve 逻辑、信道参数、seed、窗口数全部不变。
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


def per_block_da(rx_pilot, bits, tx_sym):
    """路线 B — DA 分支 per-block（decide='da' 时只跑此路）.

    数学 bit-exact 复制 _a4_switch_common768_30seed.py:per_block 的 DA 部分（:124-136）：
      pidx = arange(0,256,4); rc_da = da_ml_recovery(rx_pilot, pidx, tx_sym[pidx]);
      dm = demod(rc_da); ne_da = sum(tb[is_d] != dm[is_d])  # 192 非 pilot = common-768

    返回 (ne_da, rc_da)：
      ne_da = DA demod 在 192 非 pilot symbol = 768 bit 上错误数（= common-768，与 A 一致）
      rc_da = da_ml_recovery 输出的 carrier-corrected 复数序列（selected_rx，A 丢弃但 B 保留）
    """
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                 pilot_sym=tx_sym[pidx], mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    dm = m16apsk_demod(rc_da)
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dma = dm.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tba[is_d] != dma[is_d]))           # data 位错误数 = common-768
    return ne_da, rc_da


def per_block_nda(rx_blind, bits):
    """路线 B — NDA 分支 per-block（decide='nda' 时只跑此路）.

    数学 bit-exact 复制 _a4_switch_common768_30seed.py:per_block 的 NDA 部分（:120-138）：
      omega = fft_foe_m0_omega(rx_blind); rc_nda = nda_ml_recovery(rx_blind*exp(-jωk), assume_df_zero=True);
      res_nda = resolve_m16apsk_blockwise(rc_nda, tb);
      ne_nda = sum(tb != demod(res_nda))  # 全 1024（mixed 口径 NDA 分子）
      ne_nda_common768 = sum(tb[is_d] != demod(res_nda)[is_d])  # 192 非 pilot（common-768 口径 NDA 分子）

    返回 (ne_nda, ne_nda_common768, res_nda)：
      ne_nda = NDA demod 在全部 1024 bit 上错误数（mixed 口径 NDA 分子，与 A 一致）
      ne_nda_common768 = NDA demod 在 192 非 pilot = 768 bit 上错误数（common-768，与 A 一致）
      res_nda = resolve 后的消歧复数序列（selected_rx，A 丢弃但 B 保留）
    """
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    dm_nda = m16apsk_demod(res_nda)
    ne_nda = int(np.sum(tb != dm_nda))                    # 全部 1024 bit（mixed）
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM)
    dma_nda = dm_nda.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_nda_common768 = int(np.sum(tba[is_d] != dma_nda[is_d]))
    return ne_nda, ne_nda_common768, res_nda


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
    """路线 B branch-routed paper_summary：仅含 branch-routed 可自证的指标.

    与 A 的 build_paper_summary 区别：gain_db (NDA/selector BER ratio) 在 branch-routed 下
    不可得（NDA-only fixed-branch 需 NDA 全跑）。改为报告 selector 自身的 common-768 BER
    统计 + 选择分布，作为 branch-routed receiver 的自洽描述。bit-exact 等价性由独立
    verifier 对照 A 的权威 JSON 核查（switch_common_errors 逐 seed 一致）。
    """
    sw_c768_rates = [float(x['switch_common_errors']) / float(x['n_bits']) for x in per_seed]
    mean, std, hw, lo, hi = ci_t(sw_c768_rates)
    switch_total = int(sum(x['switch_common_errors'] for x in per_seed))
    n_bits_total = int(sum(x['n_bits'] for x in per_seed))
    return {
        'estimand': 'branch-routed selector common-768 BER (self-description; gain_db N/A — NDA-only baseline unreachable in branch-routed)',
        'n_seeds': int(len(per_seed)),
        'selector_c768_ber_mean': mean,
        'selector_c768_ber_std': std,
        'selector_c768_ber_ci95': [lo, hi],
        'ci_method': f'two-sided Student t, df={len(per_seed) - 1}',
        'aggregate_raw_counts': {
            'n_windows': int(sum(x['n_windows'] for x in per_seed)),
            'n_bits': n_bits_total,
            'switch_common_errors': switch_total,
            'n_select_da': int(sum(x['n_select_da'] for x in per_seed)),
            'n_select_nda': int(sum(x['n_select_nda'] for x in per_seed)),
            'branch_compute_sec_total': float(sum(x['branch_compute_sec'] for x in per_seed)),
        },
    }


def validate_authoritative_result(out, expected_scenes, expected_snrs, expected_n_seeds):
    """路线 B 结构性自检（provenance 完整 + schema + seed/window/selection 不变量）.

    与 A 的区别：移除 gain_db / oracle / NDA-only 不等式断言（branch-routed 下不可得），
    保留 provenance 完整性、seed 编号、窗口数、common-768 mask、选择分布自洽。
    bit-exact 等价性（switch_common_errors 逐 seed vs A）由独立 verifier 核查，不在此断言。
    """
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
            # selector BER 统计自洽重算（branch-routed 可得）
            for key in ('selector_c768_ber_mean', 'selector_c768_ber_ci95'):
                ev = expected_paper[key]
                pv = paper[key]
                if isinstance(ev, list):
                    assert all(abs(a - b) <= 1e-12 for a, b in zip(pv, ev)), f'paper_summary {key} mismatch'
                else:
                    assert abs(pv - ev) <= 1e-12, f'paper_summary {key} mismatch'
            assert paper['estimand'] == expected_paper['estimand'], 'estimand mismatch'
            assert paper['n_seeds'] == expected_n_seeds, 'paper_summary seed count mismatch'
            for seed_index, x in enumerate(seeds):
                assert x['seed_index'] == seed_index, 'seed index mismatch'
                assert x['n_windows'] == P.N_BLOCKS == 400, 'n_windows must remain 400'
                assert x['n_bits'] == 400 * COMMON768_BITS_PER_BLOCK, 'n_bits mismatch'
                expected_start = P.SEED_TURB0 + seed_index * P.N_BLOCKS
                assert x['window_seed_start'] == expected_start, 'window seed start mismatch'
                assert x['window_seed_end_inclusive'] == expected_start + P.N_BLOCKS - 1, 'window seed end mismatch'
                assert x['n_select_da'] + x['n_select_nda'] == x['n_windows'], 'branch count sum mismatch'
                assert x['switch_common_errors'] > 0, 'switch_common_errors must be positive'


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
            'branch-routed (路线 B)：per-block oracle 需两路同窗，branch-routed 只跑一路 → '
            'oracle 自检项不适用（N/A），selfcheck_*_oracle_violations 恒 0。'
            'selector 端 bit-exact 等价性由独立 verifier _verify_b_vs_a_equiv.py 核查。'
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
    print(f"A4 branch-routed (路线 B) {n_seeds} seed × {len(scenes)}场景 × "
          f"{len(snr_db)}点 = {n_seeds * len(scenes) * len(snr_db)} seed-point")

    raw = {sc: [] for sc in scenes}

    # Requested turbulence scenes and SNR grid.
    for turb in scenes:
        for i in range(n_seeds):
            s0 = P.SEED_TURB0 + i * NB
            per_snr = []
            for gdb in snr_db:
                gl = 10 ** (gdb / 10)
                e_n = e_d = e_s = 0
                e_n_c768 = e_s_c768 = 0
                n_select_da = n_select_nda = 0
                # 路线 B 计时：per-window branch compute（仅被选分支），供与 A 对比
                t_branch_compute = 0.0
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH,
                                                         mod='m16apsk', seed=s0 + b)
                    rx_raw = r['rx_raw']; bits = r['bits']; txs = r['tx']
                    # 路线 B delta：decide() 提前到两路 recovery 之前。
                    # decide 只读 rx_raw 功率统计 + nominal SNR（decide() :97-107），
                    # 输入与 A 相同（rx_raw / gdb / gl），提前不改变 decide 结果（确定性）。
                    c = decide(rx_raw, gdb, gl)
                    # 路线 B delta：每窗只执行被选分支。计时覆盖「h 估计+均衡+recovery+demod/resolve」
                    # 的单路计算（B），对应 A 的两路全跑。信道生成（generate_shared_realization）
                    # 两版相同，不计入 branch compute。
                    t_b0 = time.perf_counter()
                    if c == 'da':
                        n_select_da += 1
                        # 选 DA：只跑 pilot h + 均衡 + da_ml_recovery + demod（与 A DA 部分数学一致）
                        hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
                        rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
                        ne_d, selected_rx = per_block_da(rxp, bits, txs)
                        e_d += ne_d
                        # mixed 口径 DA 贡献：ne_d 在 768 位（A 除 1024）；e_s 用 ne_d
                        e_s += ne_d
                        # common-768：DA 窗 = ne_d（ne_d 本就是 common-768，与 A :338 一致）
                        e_s_c768 += ne_d
                        # DA 窗也需要 ne_n（mixed 口径 NDA 分子 e_n）和 ne_n_c768（common-768 NDA 分子）
                        # 用于两口径增益定义。但 B 只跑了 DA 路，NDA 路未跑 → ne_n / ne_n_c768 无法取得。
                        # 然而 A 的 e_n / e_n_c768 是**全窗 NDA 错误总和**（无论 selector 选哪路都全算），
                        # 这是 NDA-only fixed-branch BER 的分子，不是 selector 的。B 若不全跑 NDA 路，
                        # 无法给出 NDA-only fixed-branch BER。这是 B 相对 A 的结构性信息损失。
                        # → B 仅输出 selector (e_s/e_s_c768) 和被选分支 fixed-branch，NDA-only fixed
                        #   不再可得；增益定义需用「两路全跑」的 A 结果对照（本脚本聚焦等价性验证）。
                    else:
                        n_select_nda += 1
                        # 选 NDA：只跑 blind h + 均衡 + fft_foe + nda_ml_recovery + resolve + demod
                        hb = S.estimate_h_blind_perblock(rx_raw, gl)
                        rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                        ne_n, ne_n_c768, selected_rx = per_block_nda(rxb, bits)
                        e_n += ne_n
                        e_n_c768 += ne_n_c768
                        # mixed 口径 NDA 贡献：e_s 用 ne_n（全 1024）
                        e_s += ne_n
                        # common-768：NDA 窗 = ne_n_c768
                        e_s_c768 += ne_n_c768
                    t_branch_compute += time.perf_counter() - t_b0
                    # selected_rx 形状自检（DA/NDA 窗分别对应 rc_da / res_nda，shape=(256,) complex）
                    assert selected_rx.shape == (Ns,), f'selected_rx shape {selected_rx.shape} != ({Ns},)'
                n_blk_bits_full = NB * FULL_BITS_PER_BLOCK
                n_data_bits = NB * int((Ns - len(np.arange(0, Ns, P.DA_PILOT_SPACING))) * P.BITS_PER_SYM)
                n_c768_bits = NB * COMMON768_BITS_PER_BLOCK     # 400 × 768
                # 路线 B 结构性差异：per-block oracle = min(ne_n, ne_d) 需同时跑两路，
                # B 只跑一路 → oracle 不可得。标 0（下游 build_grid_metadata / validate 适配）。
                e_o = e_o_c768 = 0
                per_snr.append({'snr_db': float(gdb),
                                # mixed 口径（同 _a4_switch_30seed_fixed.py）
                                'nda': e_n / n_blk_bits_full,
                                'da_full': e_d / n_blk_bits_full,
                                'da_data': e_d / n_data_bits,
                                'sw': e_s / n_blk_bits_full,
                                'oracle': e_o / n_blk_bits_full,
                                # common-768 口径 BER
                                'nda_c768': e_n_c768 / n_c768_bits,
                                'sw_c768': e_s_c768 / n_c768_bits,
                                # raw 错误计数（供建议主控验证）
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
                                # 路线 B 新增：per-window branch compute 时间（秒）
                                'branch_compute_sec': float(t_branch_compute),
                                'branch_compute_per_window_sec': float(t_branch_compute / NB),
                                })
            raw[turb].append(per_snr)
        print(f"  {turb} done ({time.time() - t0:.0f}s)")

    elapsed = time.time() - t0

    # ============ 聚合：branch-routed 可得指标（selector + 被选分支）============
    # 路线 B 结构性信息边界（R013 §1-B / 用户确认「忠实 branch-routed」）：
    #   - 可得（bit-exact = A）：switch_common_errors (e_s_c768)、n_select_da/nda、
    #     DA-only fixed-branch 在被选 DA 窗的错误 (e_d)、各窗 selected_rx、branch_compute 时间
    #   - 不可得（结构上需两路全跑）：NDA-only fixed-branch BER（需 NDA 全跑 400 窗）、
    #     per-block oracle = min(ne_n, ne_d)（需两路同窗）、gain_db = 10log10(nda/sw)
    # → paper_summary 改为「branch-routed receiver 可自证指标」，gain_db 字段标 null。
    #   bit-exact 等价性由独立 verifier _verify_b_vs_a_equiv.py 对照 A 的权威 JSON 核查。
    n_violations = 0   # branch-routed 下 oracle 不可得，自检项移除（见 grid_metadata note）
    summary = {}
    for sc in scenes:
        snrs = [p['snr_db'] for p in raw[sc][0]]
        pts = []
        for j, snr in enumerate(snrs):
            # branch-routed 可得的 per-seed 量
            sw_mixed = [raw[sc][i][j]['sw'] for i in range(n_seeds)]              # selector mixed BER
            sw_c768 = [raw[sc][i][j]['sw_c768'] for i in range(n_seeds)]          # selector common-768 BER
            da_full = [raw[sc][i][j]['da_full'] for i in range(n_seeds)]          # DA-on-selected-DA-windows BER (full pop)
            da_data = [raw[sc][i][j]['da_data'] for i in range(n_seeds)]          # DA-on-selected-DA-windows BER (data pop)
            branch_compute = [raw[sc][i][j]['branch_compute_sec'] for i in range(n_seeds)]

            m_sw, s_sw, hw_sw, lo_sw, hi_sw = ci_t(sw_mixed)
            m_sw_c768, s_sw_c768, hw_sw_c768, lo_sw_c768, hi_sw_c768 = ci_t(sw_c768)
            m_d_full, *_ = ci_t(da_full)
            m_d_data, *_ = ci_t(da_data)
            m_bc, _, _, lo_bc, hi_bc = ci_t(branch_compute)

            # raw 计数总和（跨 seed）— 仅 branch-routed 可得项
            sum_ne_sw_mixed = int(sum(raw[sc][i][j]['raw_ne_sw_mixed'] for i in range(n_seeds)))
            sum_ne_da = int(sum(raw[sc][i][j]['raw_ne_da'] for i in range(n_seeds)))
            sum_ne_sw_c768 = int(sum(raw[sc][i][j]['raw_ne_sw_common768'] for i in range(n_seeds)))
            sum_ne_nda_partial = int(sum(raw[sc][i][j]['raw_ne_nda_all1024'] for i in range(n_seeds)))
            sum_ne_nda_c768_partial = int(sum(raw[sc][i][j]['raw_ne_nda_common768'] for i in range(n_seeds)))
            sum_n_select_da = int(sum(raw[sc][i][j]['n_select_da'] for i in range(n_seeds)))
            sum_n_select_nda = int(sum(raw[sc][i][j]['n_select_nda'] for i in range(n_seeds)))
            sum_branch_compute = float(sum(branch_compute))

            per_seed_records = [{k: raw[sc][i][j][k] for k in (
                'seed_index', 'window_seed_start', 'window_seed_end_inclusive',
                'n_windows', 'n_bits', 'switch_common_errors', 'n_select_da', 'n_select_nda',
                'branch_compute_sec', 'branch_compute_per_window_sec',
                'raw_ne_da', 'raw_ne_sw_common768',
                'raw_ne_nda_all1024', 'raw_ne_nda_common768')}
                for i in range(n_seeds)]
            paper_summary = build_paper_summary(per_seed_records)

            pts.append({
                'snr_db': float(snr),
                # selector BER（branch-routed 可得，bit-exact = A）
                'selector': {
                    'sw_mixed_ber_mean': m_sw,
                    'sw_c768_ber_mean': m_sw_c768,
                    'sw_mixed_ber_ci95': [lo_sw, hi_sw],
                    'sw_c768_ber_ci95': [lo_sw_c768, hi_sw_c768],
                },
                'da_on_selected_ber_mean_full': m_d_full,
                'da_on_selected_ber_mean_data': m_d_data,
                'paper_summary': paper_summary,
                'per_seed': per_seed_records,
                # branch-routed 计时（仅 B 有，供 verifier 与 A 对比 wall-clock 比）
                'branch_compute_sec_total': sum_branch_compute,
                'branch_compute_per_window_sec_mean': m_bc,
                'branch_compute_per_window_sec_ci95': [lo_bc, hi_bc],
                # raw 计数（跨 seed 总和）— 仅 branch-routed 可得项
                'raw_counts': {
                    'ne_sw_mixed': sum_ne_sw_mixed,
                    'ne_sw_common768': sum_ne_sw_c768,
                    'ne_da_on_selected': sum_ne_da,
                    # partial：仅 NDA 被选窗累加，非 NDA-only fixed-branch 全窗总和
                    'ne_nda_all1024_partial': sum_ne_nda_partial,
                    'ne_nda_common768_partial': sum_ne_nda_c768_partial,
                    'n_select_da': sum_n_select_da,
                    'n_select_nda': sum_n_select_nda,
                },
            })
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
    # branch-routed 下 per-block oracle 不可得（需两路同窗），common_oracle_violations 标 N/A
    grid_metadata = build_grid_metadata(
        scenes,
        snr_db,
        mixed_oracle_violations=n_violations,
        common_oracle_violations=0,   # N/A：branch-routed 无 oracle，自检项不适用
    )
    out = {
        'meta': {
            'task': 'A4 branch-routed receiver (路线 B) — common-768 口径 30seed 扫描',
            'route': 'B (branch-routed: decide 前置, 每窗只跑被选分支)',
            'n_seeds': n_seeds,
            'scenes': scenes, 'snr_db': snr_db,
            'n_points': len(scenes) * len(snr_db),
            'gamma_eff_th': GAMMA_EFF_TH, 'cv_margin': CV_MARGIN,
            'cv_model': 'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
            'ci_method': f't-dist 95% df={n_seeds - 1}',
            'elapsed_sec': float(elapsed),
            'provenance': provenance,
            'route_B_semantics': {
                'decide_timing': 'decide() 提前到两路 recovery 之前（_a4_switch_common768_30seed.py:334→本脚本 block loop 开头）',
                'branch_execution': '每窗只执行被选分支（选 DA 跑 pilot h+da_ml_recovery+demod；选 NDA 跑 blind h+fft_foe+nda_ml_recovery+resolve+demod）',
                'selected_output': 'selected_rx = rc_da (DA 窗) 或 res_nda (NDA 窗)，shape=(256,) complex',
                'equivalence_basis': 'decide 数据独立于 branch output（只读 rx_raw 功率+nominal SNR）+ h 估计/recovery/demod/resolve 全确定性 → B 逐窗错误计数 bit-exact = A',
            },
            'structural_limits': {
                'nda_only_baseline': 'N/A — NDA-only fixed-branch BER 需 NDA 全跑 400 窗，branch-routed 只在 NDA 被选窗跑 NDA',
                'per_block_oracle': 'N/A — per-block oracle = min(ne_n, ne_d) 需两路同窗，branch-routed 只跑一路',
                'gain_db': 'N/A — gain_db = 10log10(nda_common_errors/switch_common_errors) 需 NDA-only fixed-branch 全窗总和',
                'verifier_role': 'bit-exact 等价性由独立 verifier _verify_b_vs_a_equiv.py 对照 A 的权威 JSON 核查',
            },
            'caliber_definition': {
                'mixed': 'selector 选 DA 窗累加 ne_da(768-pop)，选 NDA 窗累加 ne_nda(1024-pop)，'
                         'NDA/selector 都除 (N_win×1024)。等价于 branch-dependent error-count ratio，'
                         '不是公平 BER（R004 §3 病态退化：选 DA 窗机械白送最多 1.249 dB）。',
                'common768': 'selector 选 DA 窗累加 ne_da(768)，选 NDA 窗累加 ne_nda_common768(768)，'
                             'NDA/selector 都除 (N_win×768)。两边在同一 768-bit 冻结 population 上，公平同口径。',
                'common768_mask': f'192 非 pilot symbol (pilot at np.arange(0,256,4)) × {P.BITS_PER_SYM} bit = 768 bit/block',
                'note_branch_routed': '路线 B 结构性差异：NDA-only fixed-branch / per-block oracle / gain_db '
                                      '需两路全跑，branch-routed 不可得（标 N/A）。'
                                      'selector 端量（switch_common_errors、n_select、selected_rx）bit-exact = A。',
            },
            **grid_metadata,
        },
        'summary': summary,
    }
    validate_authoritative_result(out, scenes, snr_db, n_seeds)
    out_json = out_json or os.path.join(OUT_DIR, '_a4_branchrouted_30seed_snr5_25_step2.json')
    save_results(out, out_json, os.path.basename(script_path))
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"[结构说明] branch-routed 下 per-block oracle / NDA-only baseline / gain_db 不可得（需两路全跑）")

    # ============ 打印 branch-routed 可得指标 ============
    print(f"\n{'='*92}")
    print(f"{'场景':<9}{'γd':>5}{'sw_c768_BER':>14}{'[CI95]':>16}{'sel_DA':>8}{'sel_NDA':>9}{'bcomp/win[ms]':>15}")
    print(f"{'-'*92}")
    for sc in scenes:
        for p in summary[sc]['points']:
            sel = p['selector']
            r = p['raw_counts']
            lo, hi = sel['sw_c768_ber_ci95']
            bc_ms = p['branch_compute_per_window_sec_mean'] * 1e3
            print(f"{sc:<9}{p['snr_db']:>5.0f}{sel['sw_c768_ber_mean']:>14.4e}[{lo:.2e},{hi:.2e}]"
                  f"{r['n_select_da']:>8}{r['n_select_nda']:>9}{bc_ms:>13.3f}")
    print(f"{'='*92}")
    print(f"sw_c768 = selector common-768 BER（bit-exact 应与 A 一致，由 verifier 核查）")
    print(f"sel_DA/sel_NDA = 跨 {n_seeds} seed 累计选择次数（每 seed 400 窗）")
    print(f"bcomp/win = branch compute per window（仅 B 单路，供与 A 两路全跑对比 wall-clock）")


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=N_SEEDS_DEFAULT)
    ap.add_argument('--scenes', nargs='+', choices=PROBE_SCENES)
    ap.add_argument('--snr-db', nargs='+', type=float)
    ap.add_argument('--output')
    a = ap.parse_args()
    main(n_seeds=a.seeds, scenes=a.scenes, snr_db=a.snr_db, out_json=a.output)
