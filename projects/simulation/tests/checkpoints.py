"""运行时检查点 — 在实验脚本中显式调用

启用: 设置环境变量 SIM_CHECKPOINTS=1
关闭: 不设置（默认关闭，零开销）

用法:
  SIM_CHECKPOINTS=1 python experiments/multi_seed_sweep.py
"""
import os
import sys

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

_ENABLED = os.environ.get('SIM_CHECKPOINTS', '0') == '1'


def cp1_channel(shared):
    """CP-1: 信道生成后验证
    位置: generate_shared_realization() 返回后立即调用
    """
    if not _ENABLED:
        return
    h = shared['h']
    assert np.all(h > 0), f"CP-1 FAIL: h 含非正值, min={np.min(h):.2e}"
    mean_h = np.mean(h)
    assert abs(mean_h - 1.0) < 0.15, f"CP-1 FAIL: E[h]={mean_h:.4f}, 偏离 1"
    # SNR 验证: sig_power / noise_power ≈ gamma_bar * E[h]
    carrier = np.exp(1j * shared['phi'])
    signal = shared['tx'] * np.sqrt(h) * carrier
    noise = shared['rx_raw'] - signal
    snr_meas = np.mean(np.abs(signal)**2) / np.mean(np.abs(noise)**2)
    snr_exp = shared['gamma_bar'] * mean_h
    rel = abs(snr_meas - snr_exp) / snr_exp
    assert rel < 0.1, f"CP-1 FAIL: SNR measured={snr_meas:.1f}, expected={snr_exp:.1f}"


def cp2_carrier_recovery(rx_out, label=""):
    """CP-2: 载波恢复后验证
    位置: 每个载波恢复方法返回后调用
    """
    if not _ENABLED:
        return
    assert not np.any(np.isnan(rx_out)), f"CP-2 FAIL [{label}]: 输出含 NaN"
    assert not np.any(np.isinf(rx_out)), f"CP-2 FAIL [{label}]: 输出含 Inf"


def cp3_ber(ber, method='', turbulence='', snr_db=20):
    """CP-3: BER 计算后红旗检测
    位置: 每个 BER 值计算后调用
    """
    if not _ENABLED:
        return
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    from red_flags import check_ber, format_flags
    flags = check_ber(ber, method=method, turbulence=turbulence, snr_db=snr_db)
    critical = [f for f in flags if f.severity == 'CRITICAL']
    if critical:
        raise RuntimeError(f"CP-3 CRITICAL:\n{format_flags(flags)}")


def cp4_results(data, filepath):
    """CP-4: 结果保存前验证
    位置: save_results() 内部，在 json.dump 之前
    """
    if not _ENABLED:
        return
    meta = data.get('_meta', {})
    assert 'script' in meta, "CP-4 FAIL: _meta 缺少 script"
    assert 'common_md5' in meta, "CP-4 FAIL: _meta 缺少 common_md5"
    assert 'git_commit' in meta, "CP-4 FAIL: _meta 缺少 git_commit"
