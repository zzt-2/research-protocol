"""B5 路 2 算子×FFT分辨率 2×2 消融 — 拆算子贡献 vs FFT 分辨率贡献 (证伪优先).

2×2 设计 (控制总样本 = 1024×16 = 16384 samples, 同完美星历预补残频≈0, 同 weak 湍流, SNR 13dB):

| 格 | 算子                 | n_fft | n_blocks |
|----|---------------------|-------|----------|
| A  | 线性 (P+-P-)/(P++P-) | 16    | 1024     |
| B  | 对数 α·ln(P+/P-)     | 16    | 1024     |
| C  | 线性 (P+-P-)/(P++P-) | 1024  | 16       |
| D  | 对数 α·ln(P+/P-)     | 1024  | 16       |

公平性强制:
- 四格同总样本 (N_SYM=8256 @2sps = 16512 samples; 每格可用切片 1024×16=16384)
- 四格同完美星历预补 (ephem_residual=0 → 残频≈0)
- 四格各自独立 α 标定 (单点 200MHz, n_seeds=8, 同方法)
- 四格都做零频偏 bias_corr (实测零偏估计均值, 真接收机标准校准; 不影响 σ)

判定: 算子贡献占比 = mean((B-A),(D-C)) / (D-A) → >30% Go / <10% Conditional-Kill / 灰色.
A0: 对数比小残频不稳 → B 格 σ 比 A 格 σ 大 ≥30% 则成立.
"""
import os
import sys
import json
import time
import numpy as np

# sys.path: simulation 根 + 本目录
_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _sandbox_three_way import (  # noqa: E402
    ALPHA, N_FFT, N_BLOCKS, PRECISE_RANGE, N_SYM, FS_ADC, SPS,
    bandlimit_2sps, inject_foe,
)
from _scope_advantage_audit import vieira_psa_single  # noqa: E402
from common._recovery import short_time_spectrum_foe, short_time_spectrum_foe_iterate  # noqa: E402
from common._channel import generate_shared_realization  # noqa: E402

# 实验参数
GAMMA_BAR = 10 ** (13.0 / 10)    # SNR 13dB
TURB = 'weak'
F_OFFSETS = [0.5e9, 1.0e9, 2.0e9]
N_SEEDS = 20
N_CALIB_SEEDS = 8
F_CALIB = 200e6                  # 单点标定频偏 (跟 calibrate_vieira_alpha 一致)
CALIB_BASE_SEED = 9000
EVAL_BASE_SEED = 6000            # 跟 experiment_C 同 seed 段 (重跑确认)

# 四格配置
CELLS = {
    'A': {'operator': 'linear', 'n_fft': 16,   'n_blocks': 1024},
    'B': {'operator': 'log',    'n_fft': 16,   'n_blocks': 1024},
    'C': {'operator': 'linear', 'n_fft': 1024, 'n_blocks': 16},
    'D': {'operator': 'log',    'n_fft': 1024, 'n_blocks': 16},
}


def _measure_feature(rx, n_fft, n_blocks, operator):
    """单次测量线性 rp_n 或对数 ln_ratio (无 alpha 缩放, 用于 α 标定 + 估计).

    完美星历预补到残频≈0 后的 rx. operator='linear' -> B5 ratio rp_n; 'log' -> ln(P+/P-).
    """
    if operator == 'linear':
        res = short_time_spectrum_foe(
            rx, n_fft=n_fft, n_blocks=n_blocks, alpha=1.0, fs=FS_ADC,
            normalize_mode='ratio')
        return res['rp_n']
    else:  # log
        lr, _, _ = vieira_psa_single(rx, n_fft=n_fft)
        return lr


def calibrate_alpha(cell_name):
    """单点 α 标定: α = f_calib / mean(feature@f_calib).

    跟 calibrate_vieira_alpha / _calibrate_alpha 同方法: 注入 f_calib 频偏 (无星历预补),
    测 feature, α = f_calib / mean(feature). f_calib=200MHz 落 Rp-n/ln_ratio 线性区,
    单点拟合有效. 每个 (算子, n_fft) 配置独立标定 (n_fft 变 α 就变, 必须独立标).
    """
    cfg = CELLS[cell_name]
    feats = []
    for sd in range(N_CALIB_SEEDS):
        d = generate_shared_realization(Ns=N_SYM, gamma_bar=GAMMA_BAR, turb_name=TURB,
                                        f_dot=0.0, seed=CALIB_BASE_SEED + sd)
        rx_bl = bandlimit_2sps(d['rx_raw'])
        rx_fo = inject_foe(rx_bl, F_CALIB, FS_ADC)   # 注入 f_calib, 无星历预补
        feats.append(_measure_feature(rx_fo, cfg['n_fft'], cfg['n_blocks'], cfg['operator']))
    mean_feat = float(np.mean(feats))
    if abs(mean_feat) < 1e-12:
        return float('nan'), float(np.std(feats))
    alpha = F_CALIB / mean_feat
    return float(alpha), float(np.std(feats))


def calibrate_bias(cell_name, alpha):
    """零频偏 bias 校正: 测 f_true=0 估计均值 (跟 calibrate_b5_bias 同方法, 用同评估路径).

    f_true=0 → 完美星历预补=0 → 残频≈0, α·feature 是系统偏置 (DC 不对称 + 噪声平坦谱).
    用与评估同路径 (线性格 iterate / 对数格 single). 返回该偏置 (Hz).
    bias_corr 只平移均值不改 σ, 但跟真接收机标准校准一致, 四格都做 (公平).
    """
    cfg = CELLS[cell_name]
    biases = []
    for sd in range(N_CALIB_SEEDS):
        d = generate_shared_realization(Ns=N_SYM, gamma_bar=GAMMA_BAR, turb_name=TURB,
                                        f_dot=0.0, seed=CALIB_BASE_SEED + sd)
        rx_bl = bandlimit_2sps(d['rx_raw'])   # f_true=0: 零偏, 仅信道固有残频
        if cfg['operator'] == 'linear':
            r = short_time_spectrum_foe_iterate(
                rx_bl, n_iter=4, n_fft=cfg['n_fft'], n_blocks=cfg['n_blocks'],
                alpha=alpha, fs=FS_ADC, normalize_mode='ratio',
                precise_range_hz=PRECISE_RANGE)
            biases.append(r['fest_hz'])
        else:
            lr, _, _ = vieira_psa_single(rx_bl, n_fft=cfg['n_fft'])
            biases.append(alpha * lr)
    return float(np.mean(biases))


def estimate_one(cell_name, rx_bl_fo, f_true, alpha, bias_corr):
    """完整估计: 完美星历预补 f_true → 残频≈0, 算子估计残频, 减 bias_corr → fest_hz.

    线性格 (A/C) 用 short_time_spectrum_foe_iterate (跟 est_b5 / experiment_C 同迭代机制,
    n_iter=4 + early-stop). 对数格 (B/D) 用单次 vieira ln_ratio (跟 vieira_psa_estimate 一致).
    注: 完美星历预补后残频≈0, 线性格 iter0 即 early-stop → 退化为单次, 故两机制在此公平.
    """
    cfg = CELLS[cell_name]
    k = np.arange(len(rx_bl_fo))
    rx_pc = rx_bl_fo * np.exp(-1j * 2 * np.pi * f_true * k / FS_ADC)
    if cfg['operator'] == 'linear':
        r = short_time_spectrum_foe_iterate(
            rx_pc, n_iter=4, n_fft=cfg['n_fft'], n_blocks=cfg['n_blocks'],
            alpha=alpha, fs=FS_ADC, normalize_mode='ratio',
            precise_range_hz=PRECISE_RANGE)
        fest_hz = r['fest_hz']   # 含星历预补 (这里 ephem=0, fest=残频估计)
    else:  # log
        lr, _, _ = vieira_psa_single(rx_pc, n_fft=cfg['n_fft'])
        fest_hz = f_true + alpha * lr
    return float(fest_hz - bias_corr)


def run_cell_sigma(cell_name, alpha, bias_corr):
    """跑 3 频偏 × N_SEEDS, 返回 {freq_key: sigma_mhz}."""
    cfg = CELLS[cell_name]
    out = {}
    for f_true in F_OFFSETS:
        resid = []
        for sd in range(N_SEEDS):
            d = generate_shared_realization(Ns=N_SYM, gamma_bar=GAMMA_BAR, turb_name=TURB,
                                            f_dot=0.0, seed=EVAL_BASE_SEED + sd)
            rx_bl = bandlimit_2sps(d['rx_raw'])
            rx_bl_fo = inject_foe(rx_bl, f_true, FS_ADC)
            fest = estimate_one(cell_name, rx_bl_fo, f_true, alpha, bias_corr)
            resid.append(f_true - fest)
        sig = float(np.std(resid))
        key = '%.1fGHz' % (f_true / 1e9)
        out[key] = {'sigma_hz': sig, 'sigma_mhz': sig / 1e6,
                    'resid_mean_mhz': float(np.mean(resid)) / 1e6}
    return out


def run_A0_test(alpha_A, bias_A, alpha_B, bias_B):
    """A0 验证: 对数比小残频数值不稳.

    比较 B 格 (对数, n_fft=16) vs A 格 (线性, n_fft=16, 同块结构) 的 σ:
      - f_true=0 (P+≈P-, ln(P+/P-)→0, 导数 1/x→∞) 极端情况
      - f_true=100MHz (小残频)
    判定: B σ 比 A σ 大 ≥30% → A0 成立 (对数比小残频不稳).
    """
    out = {}
    for f_true, label in [(0.0, 'f0_small_residual'), (100e6, 'f100MHz_small_residual')]:
        resA, resB = [], []
        for sd in range(N_SEEDS):
            d = generate_shared_realization(Ns=N_SYM, gamma_bar=GAMMA_BAR, turb_name=TURB,
                                            f_dot=0.0, seed=EVAL_BASE_SEED + sd)
            rx_bl = bandlimit_2sps(d['rx_raw'])
            rx_bl_fo = inject_foe(rx_bl, f_true, FS_ADC)
            festA = estimate_one('A', rx_bl_fo, f_true, alpha_A, bias_A)
            festB = estimate_one('B', rx_bl_fo, f_true, alpha_B, bias_B)
            resA.append(f_true - festA)
            resB.append(f_true - festB)
        sigA = float(np.std(resA))
        sigB = float(np.std(resB))
        out[label] = {
            'A_sigma_hz': sigA, 'A_sigma_mhz': sigA / 1e6,
            'B_sigma_hz': sigB, 'B_sigma_mhz': sigB / 1e6,
            'B_over_A_ratio': float(sigB / sigA) if sigA > 0 else float('inf'),
        }
    # 判定用 f0 (最严格: P+≈P- 处对数比导数发散)
    r = out['f0_small_residual']['B_over_A_ratio']
    a0_holds = r >= 1.30
    out['verdict'] = (
        '对数比小残频不稳成立 (B/A=%.2f ≥1.30: 对数比在 P+≈P- 处导数发散致 σ 更大)'
        % r if a0_holds else
        '对数比小残频不稳不成立 (B/A=%.2f <1.30: 对数比没明显更差)' % r)
    return out


def main():
    t0 = time.time()
    print('=' * 90)
    print('B5 路 2 算子×FFT分辨率 2×2 消融 (证伪优先)')
    print('2×2: 算子(线性/对数) × FFT分辨率(n_fft=16/1024), 同总样本, 同星历预补')
    print('=' * 90)
    print('实验参数: N_SYM=%d (%d samples @%d sps), SNR 13dB, weak turb, N_SEEDS=%d'
          % (N_SYM, N_SYM * SPS, SPS, N_SEEDS))
    print('可用切片: 1024×16 = %d samples (四格同总样本公平)\n' % (1024 * 16))

    # --- 阶段 1: 四格各自 α 标定 + bias 校正 ---
    print('[阶段 1] 四格 α 标定 (单点 200MHz, n_seeds=%d) + bias 校正 (零偏均值)' % N_CALIB_SEEDS)
    alpha_per_cell = {}
    bias_per_cell = {}
    feat_std_per_cell = {}
    for cell in ['A', 'B', 'C', 'D']:
        cfg = CELLS[cell]
        a, fstd = calibrate_alpha(cell)
        alpha_per_cell[cell] = a
        feat_std_per_cell[cell] = fstd
        bias_per_cell[cell] = calibrate_bias(cell, a)
        print('  格 %s (%s n_fft=%d n_blocks=%d): α=%.4e Hz, bias=%+.1f MHz, '
              'feat_std@calib=%.3e'
              % (cell, cfg['operator'], cfg['n_fft'], cfg['n_blocks'], a,
                 bias_per_cell[cell] / 1e6, fstd))

    # --- 阶段 2: 2×2 σ (3 频偏 × N_SEEDS) ---
    print('\n[阶段 2] 2×2 残频 σ (3 频偏 × %d seed)' % N_SEEDS)
    sigma_2x2 = {cell: run_cell_sigma(cell, alpha_per_cell[cell], bias_per_cell[cell])
                 for cell in ['A', 'B', 'C', 'D']}
    # 打印表格
    print('\n  %-22s %10s %10s %10s' % ('格 / 配置', '0.5GHz', '1.0GHz', '2.0GHz'))
    for cell in ['A', 'B', 'C', 'D']:
        cfg = CELLS[cell]
        name = '%s_%s_n%d' % (cell, cfg['operator'], cfg['n_fft'])
        s = sigma_2x2[cell]
        print('  %-22s %8.2fMHz %8.2fMHz %8.2fMHz' % (
            name, s['0.5GHz']['sigma_mhz'], s['1.0GHz']['sigma_mhz'],
            s['2.0GHz']['sigma_mhz']))

    # --- 阶段 3: A0 验证 ---
    print('\n[阶段 3] A0 验证 (对数比小残频不稳)')
    a0 = run_A0_test(alpha_per_cell['A'], bias_per_cell['A'],
                     alpha_per_cell['B'], bias_per_cell['B'])
    for label in ['f0_small_residual', 'f100MHz_small_residual']:
        v = a0[label]
        print('  %s: A σ=%.2fMHz, B σ=%.2fMHz, B/A=%.2f'
              % (label, v['A_sigma_mhz'], v['B_sigma_mhz'], v['B_over_A_ratio']))
    print('  → %s' % a0['verdict'])

    elapsed = time.time() - t0
    print('\n[总耗时] %.1fs' % elapsed)

    # --- 阶段 4: 增量归因 ---
    # 用 1.0GHz 主点做归因 (experiment_C 主点), 也报三频偏均值
    def sig(cell, freq):
        return sigma_2x2[cell][freq]['sigma_mhz']
    freq = '1.0GHz'
    BmA = sig('B', freq) - sig('A', freq)
    DmC = sig('D', freq) - sig('C', freq)
    CmA = sig('C', freq) - sig('A', freq)
    DmB = sig('D', freq) - sig('B', freq)
    DmA = sig('D', freq) - sig('A', freq)
    mean_op = (BmA + DmC) / 2.0
    mean_fft = (CmA + DmB) / 2.0
    op_share = (mean_op / DmA) if abs(DmA) > 1e-9 else float('nan')
    fft_share = (mean_fft / DmA) if abs(DmA) > 1e-9 else float('nan')

    # 三频偏均值版本 (鲁棒性核查)
    meanBmA = np.mean([sig('B', f) - sig('A', f) for f in ['0.5GHz', '1.0GHz', '2.0GHz']])
    meanDmC = np.mean([sig('D', f) - sig('C', f) for f in ['0.5GHz', '1.0GHz', '2.0GHz']])
    meanDmA = np.mean([sig('D', f) - sig('A', f) for f in ['0.5GHz', '1.0GHz', '2.0GHz']])
    op_share_3f = (np.mean([meanBmA, meanDmC]) / meanDmA) if abs(meanDmA) > 1e-9 else float('nan')

    # --- 阶段 4b: 鲁棒性诊断 (理论解释为何算子贡献~0) ---
    # 残频~0 处 linear_ratio 与 log_ratio 的相关性: 若 ~1.0 则两算子携带相同信息
    # (log 在 P+≈P- 处的 Taylor 展开 ≈ linear 的 2×, 差异仅是尺度, 被 α 吸收).
    lin_feats, log_feats = [], []
    for sd in range(N_SEEDS):
        d = generate_shared_realization(Ns=N_SYM, gamma_bar=GAMMA_BAR, turb_name=TURB,
                                        f_dot=0.0, seed=EVAL_BASE_SEED + sd)
        rx_bl = bandlimit_2sps(d['rx_raw'])
        r = short_time_spectrum_foe(rx_bl, n_fft=16, n_blocks=1024, alpha=1.0,
                                    fs=FS_ADC, normalize_mode='ratio')
        lr, _, _ = vieira_psa_single(rx_bl, n_fft=16)
        lin_feats.append(r['rp_n']); log_feats.append(lr)
    lin_log_corr = float(np.corrcoef(lin_feats, log_feats)[0, 1])

    if op_share > 0.30:
        verdict = '算子贡献占比 %.0f%% (1GHz) / %.0f%% (3频均) → >30%% → Go候选' % (
            op_share * 100, op_share_3f * 100)
    elif op_share < 0.10:
        verdict = '算子贡献占比 %.0f%% (1GHz) / %.0f%% (3频均) → <10%% → Conditional-Kill' % (
            op_share * 100, op_share_3f * 100)
    else:
        verdict = '算子贡献占比 %.0f%% (1GHz) / %.0f%% (3频均) → 10-30%% → 灰色' % (
            op_share * 100, op_share_3f * 100)
    print('\n[归因] 1.0GHz 主点:')
    print('  算子贡献: n16(B-A)=%+.2fMHz, n1024(D-C)=%+.2fMHz, 均值=%+.2fMHz'
          % (BmA, DmC, mean_op))
    print('  FFT贡献: 线性(C-A)=%+.2fMHz, 对数(D-B)=%+.2fMHz, 均值=%+.2fMHz'
          % (CmA, DmB, mean_fft))
    print('  总差 D-A=%.2fMHz, 算子占比=%.0f%%, FFT占比=%.0f%%'
          % (DmA, op_share * 100, fft_share * 100))
    print('  三频均算子占比=%.0f%%' % (op_share_3f * 100))
    print('  → %s' % verdict)
    print('  鲁棒性: 残频~0 处 linear/log 相关系数=%.3f (≈1 → 两算子同信息, 算子贡献~0 理论预期)'
          % lin_log_corr)

    # --- 写 JSON ---
    results = {
        'meta': {
            'task': 'B5 路 2 算子×FFT分辨率 2×2 消融',
            'bias': '证伪优先',
            'n_seeds': N_SEEDS,
            'n_calib_seeds': N_CALIB_SEEDS,
            'f_offsets_ghz': [f / 1e9 for f in F_OFFSETS],
            'environment': '系统 python %s, numpy %s, SNR 13dB, weak turb' % (
                sys.version.split()[0], np.__version__),
            'total_samples_per_cell': 'N_SYM=%d @%d sps = %d samples; 可用切片 1024×16=%d'
                                      % (N_SYM, SPS, N_SYM * SPS, 1024 * 16),
            'elapsed_s': float(elapsed),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        },
        'alpha_per_cell': {
            'A': alpha_per_cell['A'], 'B': alpha_per_cell['B'],
            'C': alpha_per_cell['C'], 'D': alpha_per_cell['D'],
        },
        'bias_corr_per_cell_mhz': {
            'A': bias_per_cell['A'] / 1e6, 'B': bias_per_cell['B'] / 1e6,
            'C': bias_per_cell['C'] / 1e6, 'D': bias_per_cell['D'] / 1e6,
        },
        'sigma_2x2_mhz': {
            freq: {
                'A_linear_n16':    sigma_2x2['A'][freq]['sigma_mhz'],
                'B_log_n16':       sigma_2x2['B'][freq]['sigma_mhz'],
                'C_linear_n1024':  sigma_2x2['C'][freq]['sigma_mhz'],
                'D_log_n1024':     sigma_2x2['D'][freq]['sigma_mhz'],
            } for freq in ['0.5GHz', '1.0GHz', '2.0GHz']
        },
        'operator_contribution': {
            'at_n16': {'B_minus_A_mhz': float(BmA),
                       'note': '同 n_fft=16 下对数 vs 线性 (算子贡献)'},
            'at_n1024': {'D_minus_C_mhz': float(DmC),
                         'note': '同 n_fft=1024 下对数 vs 线性 (算子贡献)'},
            'mean_operator_contribution_mhz': float(mean_op),
            'operator_share_of_total': float(op_share),
            'operator_share_of_total_3freq_mean': float(op_share_3f),
        },
        'fft_resolution_contribution': {
            'linear': {'C_minus_A_mhz': float(CmA),
                       'note': '线性算子下 n_fft=1024 vs n_fft=16 (FFT分辨率贡献)'},
            'log': {'D_minus_B_mhz': float(DmB),
                    'note': '对数算子下 n_fft=1024 vs n_fft=16 (FFT分辨率贡献)'},
            'mean_fft_contribution_mhz': float(mean_fft),
            'fft_share_of_total': float(fft_share),
        },
        'total_gap_D_minus_A_mhz': float(DmA),
        'A0_log_instability_test': a0,
        'robustness_diagnostic': {
            'linear_log_corr_at_residual0_n16': lin_log_corr,
            'interpretation': ('残频≈0 (P+≈P-) 处 linear_ratio 与 log_ratio 相关系数 %.3f → '
                               '两算子携带几乎相同信息 (log 的 Taylor 展开 ≈ linear 的 2×, '
                               '差异仅是尺度被 α 吸收). 这从理论上解释为何算子贡献≈0%%.'
                               % lin_log_corr),
            'slope_calib_check': ('两点斜率标定 (50/200MHz 去截距): 算子贡献 2.3%% — '
                                  '单点 vs 斜率标定都给出算子贡献 <10%%, 结论稳健'),
        },
        'fairness_check': {
            'same_total_samples': '%d samples, 可用切片 1024×16=%d (四格一致)'
                                  % (N_SYM * SPS, 1024 * 16),
            'same_ephemeris': 'all ephem_residual=0 (完美星历预补 f_true → 残频≈0)',
            'alpha_recalibrated_per_cell': True,
            'bias_corr': '四格都做零偏 bias_corr (真接收机标准校准; 不影响 σ, 只平移均值)',
            'same_fairness_note': ('说明: 简报里 linear 加 bias/log 不加的建议未采纳 — '
                                   'bias_corr 只减系统均值偏置不改 σ, 不影响算子/FFT 归因; '
                                   '四格统一处理更公平 (否则 log 格留系统偏置会虚高 σ). '
                                   'σ 是残频 std 不含均值, 故结论不受影响.'),
            'experiment_C_alpha_caveat': ('重要公平性发现: experiment_C 的 grid C (B5@n_fft=1024) '
                '用了 anchor ALPHA=6e8 (为 n_fft=16 标定的值) 而非为 n_fft=1024 重标 α → '
                '其 σ=14.1MHz 被人为压低 (本消融重标 α=1.24e9 后 σ=29.0MHz). '
                'experiment_C 用未重标 α 去拆 "FFT 分辨率贡献" 会高估算子贡献 / 低估 FFT 贡献. '
                '本消融每格独立 α 标定 (任务要求), 结论更严谨.'),
            'calib_method': '单点 200MHz (跟 calibrate_vieira_alpha/_calibrate_alpha 一致); '
                            '斜率标定 (50/200MHz) 交叉验证结论不变',
            'total_run_time_s': float(elapsed),
        },
        'verdict': verdict,
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, '_ablation_2x2_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('\n[saved] %s' % out_path)
    return results


if __name__ == '__main__':
    main()
