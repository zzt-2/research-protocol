"""R7: 被动冻结（深衰落时停止 CMA 更新）效果量化。

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)

补 sat.1553 §6 引 [79] Matsuda 2020 提"低功率时停止 CMA 更新"（被动冻结），
但从未量化效果。R7 首次量化冻结能避免多少发散 + 冻结期间的 SOP 漂移代价。

TL-20 理论预期:
  - 冻结应大幅降 P_div（若发散由深衰落触发）
  - 但 R4 发现发散可能不靠深衰落触发（57% 发散前零深衰落事件）→ 冻结可能效果有限
  - 冻结期间不跟踪 SOP → 恢复后有 SOP 偏差 → 冻结不是万能的

TL-22 物理前提检查: 冻结 P_div→0 → 查物理前提（冻结期间 SOP 漂移? 恢复后 BER?）

冻结逻辑: 块级 CMA 更新循环中, 若当前块信道增益 h_block < threshold, 跳过权重
更新（只滤波不做梯度更新）。

实现: 子类化 CMAEqualizer2x2（不改 common/_cma.py, 守 P4 只扩不改）。
"""
import sys
import json
import time
import numpy as np
from pathlib import Path

# 路径设置
SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._modulation import ber_count
from params import SimulationConfig


# ─── 参数 (FR-20 溯源, 从 params.py 读) ─────────────────────

cfg = SimulationConfig()

TURB_LEVELS = {
    'weak':          cfg.turbulence.as_dict()['weak'],
    'moderate':      cfg.turbulence.as_dict()['moderate'],
    'strong':        cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}

N_SYMBOLS = 2_000_000   # 2M 符号（降自 5M 以控时; CMA 发散快, 2M 足覆盖发散事件）
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 (20 dB)
BLOCK = cfg.experiment.BLOCK  # 100
T_S = cfg.system.T_S  # 1/2.5e9
R_SYM = cfg.system.R_SYM
R2_QPSK = 1.0
CMA_BLOCK_SIZE = 64   # sat.1553 §6.3 L756 并行化因子
SOP_RATE = 1e-4       # Step B 参数 (rad/sym; ~250 krad/s @ 2.5GBaud)

FREEZE_THRESHOLD_DEFAULT = 0.1   # 默认冻结门限 (h_block < 0.1 → 冻结)
FREEZE_THRESHOLDS = [0.05, 0.1, 0.3, 0.5]   # 实验 C 门限敏感性


# ─── 冻结版 CMA 均衡器 (子类化, 不改 _cma.py) ───────────────

class CMAEqualizer2x2WithFreeze(CMAEqualizer2x2):
    """带被动冻结的 2×2 蝶形 CMA。

    [79] Matsuda 2020: 低功率（深衰落）时停止 CMA 更新。
    冻结逻辑: 块级更新循环中, 若 h_block[blk] < freeze_threshold,
    跳过梯度更新（只滤波, sat.1553 Eq.28 不变, 跳过 Eq.48/50 权重更新）。

    额外记录:
      - n_frozen_blocks: 冻结块数
      - n_frozen_symbols: 冻结期间累计符号数
      - sop_theta: SOP 旋转角序列 (theta, 符号级) — 用于算冻结期间 SOP 漂移
      - freeze_segments: [(start_idx, end_idx, theta_start, theta_end), ...]
    """

    def equalize(self, rX, rY, h_block_series=None, theta_series=None,
                 block_size=CMA_BLOCK_SIZE, freeze_threshold=FREEZE_THRESHOLD_DEFAULT):
        """带冻结的块级 2×2 CMA 均衡。

        参数
        ----
        rX, rY : ndarray (N,)
            双偏振接收信号。
        h_block_series : ndarray (n_blocks,) or None
            块级信道增益序列。None = 不冻结（退化为父类行为, 用于公平对照）。
        theta_series : ndarray (N,) or None
            符号级 SOP 旋转角 (rad)。用于记录冻结期间 SOP 漂移。
        block_size : int
            CMA 并行化因子。
        freeze_threshold : float
            h_block < 此值 → 冻结该块。

        返回
        ----
        result : dict (含父类字段 + freeze 统计)
        """
        from numpy.lib.stride_tricks import sliding_window_view
        N = len(rX)
        L = self.n_tap
        half = L // 2

        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)
        w_norm_traj = np.zeros(N)
        z_amp_traj = np.zeros(N)

        rX_win = sliding_window_view(rX, L)
        rY_win = sliding_window_view(rY, L)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None
        n_valid = N - L + 1
        n_blocks = n_valid // block_size

        # 冻结统计
        n_frozen_blocks = 0
        n_frozen_symbols = 0
        freeze_segments = []   # [(blk_start_idx, blk_end_idx), ...] (符号级 idx)
        cur_freeze_start = None

        freeze_enabled = h_block_series is not None
        if freeze_enabled:
            # h_block_series 长度可能 < n_blocks, 截断到 n_blocks
            h_blk_arr = h_block_series[:n_blocks]

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break

            # 判断是否冻结
            is_frozen = False
            if freeze_enabled:
                h_blk_val = h_blk_arr[blk]
                if h_blk_val < freeze_threshold:
                    is_frozen = True
                    n_frozen_blocks += 1
                    n_frozen_symbols += block_size
                    if cur_freeze_start is None:
                        cur_freeze_start = s + half   # 符号级起始

            # 块内向量化滤波: sat.1553 Eq.(28) (始终执行, 冻结也滤波)
            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # 块末梯度更新: sat.1553 Eq.(48/50) — 冻结时跳过
            if not is_frozen:
                eX = self.R2 - np.abs(zx_blk) ** 2
                eY = self.R2 - np.abs(zy_blk) ** 2
                self.wxx += self.mu * np.mean(eX[:, None] * np.conj(rX_blk), axis=0)
                self.wxy += self.mu * np.mean(eX[:, None] * np.conj(rY_blk), axis=0)
                self.wyx += self.mu * np.mean(eY[:, None] * np.conj(rX_blk), axis=0)
                self.wyy += self.mu * np.mean(eY[:, None] * np.conj(rY_blk), axis=0)
            # else: 冻结 — 跳过权重更新 ([79] Matsuda 2020)

            # 记录冻结段结束
            if is_frozen:
                pass   # 继续累积, 等解冻时关闭
            else:
                if cur_freeze_start is not None:
                    freeze_segments.append((cur_freeze_start, idx + block_size - 1))
                    cur_freeze_start = None

            # 记录轨迹 (块末)
            cur_norm = self.weights_norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            w_norm_traj[idx + block_size - 1] = cur_norm
            z_amp_traj[idx + block_size - 1] = cur_zamp

            # 发散检测
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        # 关闭末尾未结束的冻结段
        if cur_freeze_start is not None:
            freeze_segments.append((cur_freeze_start, idx + block_size - 1))

        # 算冻结期间 SOP 漂移 (theta 变化量)
        freeze_sop_drift = 0.0   # rad, 总绝对漂移
        if theta_series is not None and freeze_segments:
            for (fs_idx, fe_idx) in freeze_segments:
                if fe_idx < len(theta_series) and fs_idx < len(theta_series):
                    drift = abs(float(theta_series[min(fe_idx, len(theta_series)-1)]
                                     - theta_series[fs_idx]))
                    freeze_sop_drift += drift

        return {
            'zX': zX, 'zY': zY,
            'w_norm_traj': w_norm_traj,
            'z_amp_traj': z_amp_traj,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self.weights_norm(),
            'init_w_norm': self._init_norm,
            # 冻结统计
            'n_frozen_blocks': n_frozen_blocks,
            'n_frozen_symbols': n_frozen_symbols,
            'n_freeze_segments': len(freeze_segments),
            'freeze_segments': freeze_segments,
            'freeze_sop_drift_rad': freeze_sop_drift,
            'freeze_fraction': n_frozen_blocks / max(n_blocks, 1),
        }


# ─── 信道/信号生成 (跟 cma_divergence_scan.py 一致) ─────────

def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1。"""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2*bits[0::2]) + 1j * (1 - 2*bits[1::2])) / np.sqrt(2)


def gen_signals(N, h, seed, sop_rate=SOP_RATE):
    """生成双偏振接收信号 + TX 参考符号 + theta 序列。

    返回 (rX, rY, sX, sY, theta, tx_bits_X)。
    sX/sY 用于 BER 评估 (X 偏振主判)。
    """
    rng = np.random.default_rng(seed)
    bits_X = rng.integers(0, 2, N * 2)
    sX = ((1 - 2*bits_X[0::2]) + 1j * (1 - 2*bits_X[1::2])) / np.sqrt(2)
    sY = gen_qpsk(N, rng)

    noise_var = 1.0 / (2 * GAMMA_BAR)
    nX = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    nY = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))

    # SOP 旋转: sat.1553 Eq.(51) Jones J=rot(theta(t))
    theta = sop_rate * np.arange(N)
    rX = np.sqrt(h) * (np.cos(theta) * sX + np.sin(theta) * sY) + nX
    rY = np.sqrt(h) * (-np.sin(theta) * sX + np.cos(theta) * sY) + nY

    return rX, rY, sX, sY, theta, bits_X


def compute_h_block_series(h, n_blocks, block_size=CMA_BLOCK_SIZE):
    """符号级 h → 块级 h_block_series。

    块级 h = h[blk*block_size : (blk+1)*block_size] 的均值 (代表该块信道增益)。
    gg_time_envelope 块内恒定 (BLOCK=100 信道块), CMA block_size=64,
    所以 CMA 块可能跨信道块边界 → 均值是合理代表。
    """
    h_block = np.zeros(n_blocks)
    n_valid = len(h)
    for blk in range(n_blocks):
        s = blk * block_size
        e = min(s + block_size, n_valid)
        h_block[blk] = np.mean(h[s:e]) if e > s else 0.0
    return h_block


def compute_ber_X(zX, sX, tx_bits_X, theta, n_tap=11):
    """X 偏振 BER 评估。

    均衡输出 zX 含残余 SOP/相位（CMA 不锁相, 有任意旋转）。
    用 resolve_qpsk (试 8 个 π/4 旋转取最低 BER) 消相位模糊。
    跳过首尾各 half 符号 (FIR 群延迟未覆盖区)。
    """
    from common._modulation import resolve_qpsk
    half = n_tap // 2
    valid = slice(half, len(zX) - half)
    z = zX[valid]
    bits_valid = tx_bits_X[2 * valid.start:2 * valid.stop]
    return float(resolve_qpsk(z, bits_valid))


# ─── 单次 trial: CMA vs Freeze ──────────────────────────────

def run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed,
                     freeze_threshold=FREEZE_THRESHOLD_DEFAULT,
                     use_freeze=True, n_symbols=N_SYMBOLS):
    """跑一次 CMA 发散测试, 返回 CMA 基线 + Freeze 版结果。

    信道生成跟 cma_divergence_scan.py 完全一致 (双偏振 + SOP)。
    """
    N = n_symbols
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)

    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK,
                         t_s=T_S, method='gar', seed=seed)
    rX, rY, sX, sY, theta, bits_X = gen_signals(N, h, seed, sop_rate=SOP_RATE)

    n_valid = N - n_tap + 1
    n_blocks = n_valid // CMA_BLOCK_SIZE
    h_block_series = compute_h_block_series(h, n_blocks, CMA_BLOCK_SIZE)

    results = {}

    # --- 基线 CMA (无冻结): 用 Freeze 子类 + h_block_series=None ---
    eq_base = CMAEqualizer2x2WithFreeze(n_tap=n_tap, mu=mu, R2=R2_QPSK)
    res_base = eq_base.equalize(rX, rY, h_block_series=None,
                                block_size=CMA_BLOCK_SIZE)
    # BER (X 偏振)
    if not res_base['diverged']:
        ber_base = compute_ber_X(res_base['zX'], sX, bits_X, theta)
    else:
        ber_base = 0.5   # 发散 → BER ≈ 0.5 (随机)
    results['cma'] = {
        'diverged': res_base['diverged'],
        'diverge_idx': res_base['diverge_idx'],
        'final_w_norm': float(res_base['final_w_norm']),
        'ber': float(ber_base),
    }

    # --- Freeze 版 CMA ---
    if use_freeze:
        eq_fr = CMAEqualizer2x2WithFreeze(n_tap=n_tap, mu=mu, R2=R2_QPSK)
        res_fr = eq_fr.equalize(rX, rY, h_block_series=h_block_series,
                                theta_series=theta,
                                block_size=CMA_BLOCK_SIZE,
                                freeze_threshold=freeze_threshold)
        if not res_fr['diverged']:
            ber_fr = compute_ber_X(res_fr['zX'], sX, bits_X, theta)
        else:
            ber_fr = 0.5
        results['freeze'] = {
            'diverged': res_fr['diverged'],
            'diverge_idx': res_fr['diverge_idx'],
            'final_w_norm': float(res_fr['final_w_norm']),
            'ber': float(ber_fr),
            'n_frozen_blocks': res_fr['n_frozen_blocks'],
            'n_frozen_symbols': res_fr['n_frozen_symbols'],
            'n_freeze_segments': res_fr['n_freeze_segments'],
            'freeze_sop_drift_rad': float(res_fr['freeze_sop_drift_rad']),
            'freeze_fraction': float(res_fr['freeze_fraction']),
        }

    return results


# ─── 实验 A: 冻结效果扫描 ───────────────────────────────────

def run_experiment_A(turb_list, f_g_list, mu_list, n_tap=11, n_trials=3,
                     freeze_threshold=FREEZE_THRESHOLD_DEFAULT,
                     n_symbols=N_SYMBOLS, label='A'):
    """实验 A: 冻结效果 — P_div(CMA) vs P_div(Freeze) 扫描。

    返回 list of combo dicts (含两版 P_div + 冻结次数统计)。
    """
    total_combos = len(turb_list) * len(f_g_list) * len(mu_list)
    total_runs = total_combos * n_trials
    print(f"\n[Exp {label}] 冻结效果扫描: {total_combos} combos × {n_trials} trials = {total_runs} trials")
    print(f"  turb={turb_list}, f_G={f_g_list}, mu={mu_list}, tap={n_tap}")
    print(f"  freeze_threshold={freeze_threshold}, N_symbols={n_symbols}")

    results = []
    run_count = 0
    t_start = time.time()

    for turb_name in turb_list:
        alpha, beta = TURB_LEVELS[turb_name]
        for f_g in f_g_list:
            for mu in mu_list:
                cma_div_count = 0
                fr_div_count = 0
                trial_details = []
                fr_stats_acc = {'n_frozen_blocks': 0, 'n_frozen_symbols': 0,
                                'n_freeze_segments': 0, 'freeze_sop_drift_rad': 0.0,
                                'freeze_fraction': 0.0}
                for trial in range(n_trials):
                    seed = hash((turb_name, f_g, mu, n_tap, trial)) % (2**32)
                    res = run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap,
                                           seed, freeze_threshold=freeze_threshold,
                                           use_freeze=True, n_symbols=n_symbols)
                    if res['cma']['diverged']:
                        cma_div_count += 1
                    if res['freeze']['diverged']:
                        fr_div_count += 1
                    # 累积冻结统计
                    fs = res['freeze']
                    for k in fr_stats_acc:
                        fr_stats_acc[k] += fs.get(k, 0)
                    trial_details.append({
                        'seed': seed,
                        'cma_div': res['cma']['diverged'],
                        'fr_div': res['freeze']['diverged'],
                        'cma_ber': res['cma']['ber'],
                        'fr_ber': res['freeze']['ber'],
                    })
                    run_count += 1

                p_div_cma = cma_div_count / n_trials
                p_div_fr = fr_div_count / n_trials
                combo = {
                    'turb_name': turb_name,
                    'f_g_hz': f_g,
                    'mu': mu,
                    'n_tap': n_tap,
                    'n_trials': n_trials,
                    'p_div_cma': p_div_cma,
                    'p_div_freeze': p_div_fr,
                    'cma_div_count': cma_div_count,
                    'freeze_div_count': fr_div_count,
                    'mean_freeze_fraction': fr_stats_acc['freeze_fraction'] / n_trials,
                    'mean_freeze_blocks': fr_stats_acc['n_frozen_blocks'] / n_trials,
                    'mean_freeze_sop_drift_rad': fr_stats_acc['freeze_sop_drift_rad'] / n_trials,
                    'trials': trial_details,
                }
                results.append(combo)
                elapsed = time.time() - t_start
                eta = elapsed / run_count * (total_runs - run_count)
                print(f"  [{run_count}/{total_runs}] {turb_name} f_G={f_g:>5.0f} μ={mu:.0e}"
                      f" → P_div CMA={p_div_cma:.2f} Freeze={p_div_fr:.2f}"
                      f" (freeze {fr_stats_acc['n_frozen_blocks']/n_trials:.0f}blk)"
                      f"  [{elapsed:.0f}s, ETA {eta:.0f}s]")

    return results


# ─── 实验 B: 冻结 SOP 代价 (单场景深查) ─────────────────────

def run_experiment_B(n_trials=5, freeze_threshold=FREEZE_THRESHOLD_DEFAULT,
                     n_symbols=N_SYMBOLS, label='B'):
    """实验 B: 冻结 SOP 代价 — strong 湍流 + f_G=1000Hz + μ=1e-2 (危险区)。

    记录: 冻结次数 + 总冻结符号数 + 冻结期间 SOP 漂移角度 + 恢复后 BER 对比。
    """
    turb_name = 'strong'
    alpha, beta = TURB_LEVELS[turb_name]
    f_g = 1000.0
    mu = 1e-2
    n_tap = 11

    print(f"\n[Exp {label}] 冻结 SOP 代价: {turb_name} f_G={f_g} μ={mu} tap={n_tap}")
    print(f"  {n_trials} seeds, N_symbols={n_symbols}, threshold={freeze_threshold}")

    trials = []
    t_start = time.time()
    for trial in range(n_trials):
        seed = hash(('B', turb_name, f_g, mu, n_tap, trial)) % (2**32)
        res = run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed,
                               freeze_threshold=freeze_threshold,
                               use_freeze=True, n_symbols=n_symbols)
        fs = res['freeze']
        tr = {
            'seed': seed,
            'cma_diverged': res['cma']['diverged'],
            'freeze_diverged': fs['diverged'],
            'cma_ber': res['cma']['ber'],
            'freeze_ber': fs['ber'],
            'n_frozen_blocks': fs['n_frozen_blocks'],
            'n_frozen_symbols': fs['n_frozen_symbols'],
            'n_freeze_segments': fs['n_freeze_segments'],
            'freeze_sop_drift_rad': fs['freeze_sop_drift_rad'],
            'freeze_fraction': fs['freeze_fraction'],
        }
        trials.append(tr)
        elapsed = time.time() - t_start
        print(f"  [trial {trial+1}/{n_trials}] CMA div={tr['cma_diverged']} "
              f"Freeze div={tr['freeze_diverged']} | "
              f"frozen {tr['n_frozen_blocks']}blk ({tr['n_freeze_segments']}seg, "
              f"{tr['freeze_fraction']*100:.1f}%) | "
              f"SOP drift {np.degrees(tr['freeze_sop_drift_rad']):.1f}° | "
              f"BER CMA={tr['cma_ber']:.4f} Freeze={tr['freeze_ber']:.4f}  [{elapsed:.0f}s]")

    # 汇总 (只对未发散 trial 算 BER 均值)
    summary = {
        'config': {'turb_name': turb_name, 'f_g_hz': f_g, 'mu': mu, 'n_tap': n_tap,
                   'n_trials': n_trials, 'freeze_threshold': freeze_threshold,
                   'sop_rate': SOP_RATE},
        'mean_freeze_blocks': float(np.mean([t['n_frozen_blocks'] for t in trials])),
        'mean_freeze_symbols': float(np.mean([t['n_frozen_symbols'] for t in trials])),
        'mean_freeze_segments': float(np.mean([t['n_freeze_segments'] for t in trials])),
        'mean_freeze_fraction': float(np.mean([t['freeze_fraction'] for t in trials])),
        'mean_sop_drift_rad': float(np.mean([t['freeze_sop_drift_rad'] for t in trials])),
        'mean_sop_drift_deg': float(np.degrees(np.mean([t['freeze_sop_drift_rad'] for t in trials]))),
        'cma_div_rate': float(np.mean([t['cma_diverged'] for t in trials])),
        'freeze_div_rate': float(np.mean([t['freeze_diverged'] for t in trials])),
        # BER: 发散=0.5, 未发散算均值
        'mean_cma_ber': float(np.mean([t['cma_ber'] for t in trials])),
        'mean_freeze_ber': float(np.mean([t['freeze_ber'] for t in trials])),
        'trials': trials,
    }
    return summary


# ─── 实验 C: 冻结 threshold 敏感性 ──────────────────────────

def run_experiment_C(thresholds, n_trials=3, label='C'):
    """实验 C: threshold 敏感性 — strong + f_G=1000Hz + μ=1e-2。

    看 P_div 如何随 threshold 变化。
    """
    turb_name = 'strong'
    alpha, beta = TURB_LEVELS[turb_name]
    f_g = 1000.0
    mu = 1e-2
    n_tap = 11

    print(f"\n[Exp {label}] threshold 敏感性: {turb_name} f_G={f_g} μ={mu}")
    print(f"  thresholds={thresholds}, {n_trials} seeds each")

    results = []
    t_start = time.time()
    for thr in thresholds:
        fr_div_count = 0
        freeze_frac_acc = []
        for trial in range(n_trials):
            seed = hash(('C', thr, turb_name, f_g, mu, trial)) % (2**32)
            res = run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed,
                                   freeze_threshold=thr, use_freeze=True)
            if res['freeze']['diverged']:
                fr_div_count += 1
            freeze_frac_acc.append(res['freeze']['freeze_fraction'])
        p_div = fr_div_count / n_trials
        entry = {
            'threshold': thr,
            'n_trials': n_trials,
            'p_div_freeze': p_div,
            'freeze_div_count': fr_div_count,
            'mean_freeze_fraction': float(np.mean(freeze_frac_acc)),
        }
        results.append(entry)
        elapsed = time.time() - t_start
        print(f"  threshold={thr:.2f} → P_div(Freeze)={p_div:.2f} "
              f"(freeze {entry['mean_freeze_fraction']*100:.1f}%)  [{elapsed:.0f}s]")

    return results


# ─── 结果保存 ───────────────────────────────────────────────

def save_results(summary, filename):
    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")
    return out_path


# ─── 汇总打印 ───────────────────────────────────────────────

def print_summary_table(exp_a, exp_b, exp_c):
    print("\n" + "=" * 78)
    print("R7 汇总: 被动冻结效果量化")
    print("=" * 78)

    # 实验 A: P_div CMA vs Freeze
    print("\n── 实验 A: P_div(CMA) vs P_div(Freeze) ──")
    print(f"{'turb':>13} {'f_G':>6} {'mu':>8} | {'P_div CMA':>9} {'P_div Frz':>9} {'Δ':>5} | {'freeze%':>7}")
    print("-" * 78)
    # 按 turb, mu, f_G 分组
    by_turb = {}
    for c in exp_a:
        by_turb.setdefault(c['turb_name'], []).append(c)
    for turb_name in sorted(by_turb.keys()):
        for mu in sorted(set(c['mu'] for c in by_turb[turb_name])):
            for c in sorted([x for x in by_turb[turb_name] if x['mu'] == mu],
                            key=lambda x: x['f_g_hz']):
                delta = c['p_div_cma'] - c['p_div_freeze']
                print(f"{turb_name:>13} {c['f_g_hz']:>6.0f} {mu:>8.0e} | "
                      f"{c['p_div_cma']:>9.2f} {c['p_div_freeze']:>9.2f} {delta:>+5.2f} | "
                      f"{c['mean_freeze_fraction']*100:>6.1f}%")

    # 实验 B: SOP 代价
    print(f"\n── 实验 B: 冻结 SOP 代价 (strong, f_G=1000, μ=1e-2) ──")
    print(f"  冻结块数:     {exp_b['mean_freeze_blocks']:.0f} 块/trial")
    print(f"  冻结符号数:   {exp_b['mean_freeze_symbols']:.0f} sym/trial")
    print(f"  冻结占比:     {exp_b['mean_freeze_fraction']*100:.1f}%")
    print(f"  冻结段数:     {exp_b['mean_freeze_segments']:.1f} seg/trial")
    print(f"  SOP 漂移:     {exp_b['mean_sop_drift_deg']:.1f}° (累计绝对漂移)")
    print(f"  P_div CMA:    {exp_b['cma_div_rate']:.2f}")
    print(f"  P_div Freeze: {exp_b['freeze_div_rate']:.2f}")
    print(f"  BER CMA:      {exp_b['mean_cma_ber']:.4f}")
    print(f"  BER Freeze:   {exp_b['mean_freeze_ber']:.4f}")

    # 实验 C: threshold 敏感性
    print(f"\n── 实验 C: threshold 敏感性 (strong, f_G=1000, μ=1e-2) ──")
    print(f"{'threshold':>10} {'P_div Frz':>10} {'freeze%':>9}")
    print("-" * 35)
    for c in exp_c:
        print(f"{c['threshold']:>10.2f} {c['p_div_freeze']:>10.2f} {c['mean_freeze_fraction']*100:>8.1f}%")


# ─── 入口 ───────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='R7: 被动冻结效果量化')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (1 湍流 × 1 f_G × 1 μ × 1 trial)')
    parser.add_argument('--n-symbols', type=int, default=N_SYMBOLS)
    args = parser.parse_args()

    N_SYM = args.n_symbols

    t_global = time.time()

    if args.smoke:
        print("=" * 60)
        print("SMOKE TEST (验证冻结子类正确性)")
        print("=" * 60)
        exp_a = run_experiment_A(
            turb_list=['strong'],
            f_g_list=[1000.0],
            mu_list=[1e-2],
            n_tap=11, n_trials=1,
            n_symbols=min(N_SYM, 500_000),
            label='A-smoke',
        )
        exp_b = run_experiment_B(n_trials=2, n_symbols=min(N_SYM, 500_000), label='B-smoke')
        exp_c = run_experiment_C([0.1, 0.3], n_trials=1, label='C-smoke')
    else:
        # 实验 A: 2 湍流 (危险档) × 3 f_G × 4 μ × 1 tap × 3 seeds
        # = 24 combos × 3 = 72 trials × 2 版 = 144 trial-runs
        # 控时: ~3.5s × 144 ≈ 8.4 min
        print("=" * 60)
        print("R7: 被动冻结效果量化 (FULL)")
        print("=" * 60)
        exp_a = run_experiment_A(
            turb_list=['strong', 'uplink_strong'],
            f_g_list=[100.0, 300.0, 1000.0],
            mu_list=[5e-4, 1e-3, 5e-3, 1e-2],
            n_tap=11, n_trials=3,
            n_symbols=N_SYM,
            label='A',
        )
        exp_b = run_experiment_B(n_trials=5, n_symbols=N_SYM, label='B')
        exp_c = run_experiment_C(FREEZE_THRESHOLDS, n_trials=3, label='C')

    summary = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'R7 (被动冻结效果量化)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYM,
            'gamma_bar': GAMMA_BAR,
            'block': BLOCK,
            't_s': T_S,
            'r_sym': R_SYM,
            'cma_block_size': CMA_BLOCK_SIZE,
            'sop_rate': SOP_RATE,
            'freeze_threshold_default': FREEZE_THRESHOLD_DEFAULT,
            'elapsed_s': time.time() - t_global,
        },
        'experiment_A_freeze_effect': exp_a,
        'experiment_B_sop_cost': exp_b,
        'experiment_C_threshold_sensitivity': exp_c,
    }

    fname = 'r7_freeze_smoke.json' if args.smoke else 'r7_freeze_results.json'
    save_results(summary, fname)

    print_summary_table(
        exp_a if isinstance(exp_a, list) else [exp_a],
        exp_b if isinstance(exp_b, dict) else exp_b,
        exp_c if isinstance(exp_c, list) else [exp_c],
    )

    print(f"\n总耗时: {time.time() - t_global:.0f}s")
