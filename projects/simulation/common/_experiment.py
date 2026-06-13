"""实验便捷函数：单次试验、结果保存"""
import os
import hashlib
import subprocess
import json
import datetime
import numpy as np

from ._config import BLOCK
from ._channel import generate_shared_realization
from ._modulation import ber_eval
from ._equalizer import amp_limit, mmse_equalize, equalize_oracle, equalize_hmed
from ._recovery import fft_foe, bps_cpr, carrier_recovery_fixed
from ._kf import (design_Q, kf_oracle_recovery, kf_frame_h_recovery,
                  kf_pilot_recovery, get_pilots)


def insert_pilots(shared, n_pilots_per_block=5):
    """
    在共享实现上插入导频。不重新生成信道/噪声/相位。

    返回 pilot 版本的 rx_raw、导频/数据索引、数据比特。
    """
    rx_raw = shared['rx_raw']
    tx = shared['tx'].copy()
    bits = shared['bits']
    h = shared['h']
    phi = shared['phi']
    gamma_bar = shared['gamma_bar']
    Ns = shared['Ns']
    n_blocks = Ns // BLOCK

    known_pilots = get_pilots(n_pilots_per_block)
    pilot_indices = []
    data_indices = []

    for b in range(n_blocks):
        base = b * BLOCK
        for p in range(n_pilots_per_block):
            idx = base + p
            tx[idx] = known_pilots[p % len(known_pilots)]
            pilot_indices.append(idx)
        for d in range(n_pilots_per_block, BLOCK):
            data_indices.append(base + d)

    pilot_indices = np.array(pilot_indices)
    data_indices = np.array(data_indices)

    # 重建 rx（替换导频位置的发符号，噪声/信道/相位不变）
    carrier = np.exp(1j * phi)
    noise = rx_raw - shared['tx'] * np.sqrt(h) * carrier
    signal_pilot = tx * np.sqrt(h) * carrier
    rx_pilot = signal_pilot + noise

    # 数据比特
    data_bits = np.zeros(len(data_indices) * 2, dtype=int)
    for i, idx in enumerate(data_indices):
        data_bits[2*i] = bits[2*idx]
        data_bits[2*i+1] = bits[2*idx+1]

    return rx_pilot, pilot_indices, data_indices, data_bits


def run_fixed(shared, eq_mode='oracle'):
    """Fixed 基线（FOE+DPLL+VV）"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return carrier_recovery_fixed(rx_eq)


def run_kf_oracle(shared, eq_mode='oracle', **kf_kwargs):
    """KF oracle-h"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return kf_oracle_recovery(rx_eq, shared['h'], shared['gamma_bar'],
                              shared['turb_name'], shared['f_dot'], **kf_kwargs)


def run_kf_frame_h(shared, eq_mode='oracle', **kf_kwargs):
    """KF frame-level h"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    return kf_frame_h_recovery(rx_eq, shared['h_med'], shared['gamma_bar'],
                               shared['turb_name'], shared['f_dot'], **kf_kwargs)


def run_kf_pilot(shared, n_pilots=5, eq_mode='oracle', **kf_kwargs):
    """KF pilot-h（导频辅助）"""
    rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots)
    if eq_mode == 'oracle':
        rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h'], shared['gamma_bar']), 3.0)
    else:
        rx_eq = amp_limit(mmse_equalize(rx_pilot, shared['h_med'], shared['gamma_bar']), 3.0)
    corrected, h_est = kf_pilot_recovery(
        rx_eq, shared['gamma_bar'], shared['turb_name'], n_pilots,
        shared['h_med'], shared['f_dot'], **kf_kwargs)
    return corrected, data_idx, data_bits, h_est


def run_bps(shared, eq_mode='oracle'):
    """BPS 载波恢复（FOE + BPS）"""
    if eq_mode == 'oracle':
        rx_eq = equalize_oracle(shared)
    else:
        rx_eq = equalize_hmed(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_cpr, _ = bps_cpr(rx_foc)
    return rx_cpr


def db_ratio(a, b):
    if a > 0 and b > 0:
        return 10 * np.log10(a / b)
    return 0.0


def run_trial_shared(Ns, gamma_bar, turb_name, f_dot, seed,
                     schemes=None, n_pilots=5, eq_mode='oracle',
                     eval_mode='oracle'):
    """
    单次试验：共享信道，多方案对比。

    schemes: list of 'fixed', 'kf_oracle', 'kf_frame', 'kf_pilot'
    eval_mode: 'direct' (ber_count, 公平) 或 'oracle' (resolve_qpsk)
    Returns: dict {scheme: BER}
    """
    if schemes is None:
        schemes = ['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']

    shared = generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)
    results = {}

    if 'fixed' in schemes:
        rx_fixed = run_fixed(shared, eq_mode)
        results['fixed'] = ber_eval(shared['bits'], rx_fixed, mode=eval_mode)

    if 'kf_oracle' in schemes:
        rx_kf_or = run_kf_oracle(shared, eq_mode)
        results['kf_oracle'] = ber_eval(shared['bits'], rx_kf_or, mode=eval_mode)

    if 'kf_frame' in schemes:
        rx_kf_fr = run_kf_frame_h(shared, eq_mode)
        results['kf_frame'] = ber_eval(shared['bits'], rx_kf_fr, mode=eval_mode)

    if 'kf_pilot' in schemes:
        corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots, eq_mode)
        results['kf_pilot'] = ber_eval(data_bits, corrected[data_idx], mode=eval_mode)

    if 'bps' in schemes:
        rx_bps = run_bps(shared, eq_mode)
        results['bps'] = ber_eval(shared['bits'], rx_bps, mode=eval_mode)

    return results


def save_results(data, filepath, script_name):
    """保存结果 JSON 并自动注入元数据（TL-25 rule 6）。

    Args:
        data: 要保存的 dict（会被原地修改，加入 _meta 键）
        filepath: 输出路径（如 'results/sweep.json'）
        script_name: 脚本名（如 'multi_seed_sweep'）
    """
    with open(__file__, 'rb') as f:
        chash = hashlib.md5(f.read()).hexdigest()[:8]
    try:
        commit = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True, cwd=os.path.dirname(__file__)
        ).stdout.strip()
    except Exception:
        commit = 'unknown'
    data['_meta'] = {
        'script': script_name,
        'common_md5': chash,
        'git_commit': commit,
        'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
    }
    # CP-4: 元数据完整性验证（始终执行，零开销）
    meta = data.get('_meta', {})
    if 'script' not in meta:
        import warnings
        warnings.warn("save_results: _meta 缺少 script 字段", stacklevel=3)

    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {filepath} [common@{chash}, git@{commit}]")
