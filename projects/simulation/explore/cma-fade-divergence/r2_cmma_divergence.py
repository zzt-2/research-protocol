"""R2 — CMMA (Cascaded Multi-Modulus CMA) + 发散扫描.

> 方向: Q-CMA-FADE (Step B 分析层, R2 子实验) | 状态: WIP
> 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 代码结果分离; P4 只扩不改; P5 标方向+状态)

TL-20 假设验证:
  多模 (CMMA) 修复星座失配 (16QAM 三环), 但梯度噪声驱动机制不变 →
  危险区仍应发散, 只是 P_div 可能略低于单模 CMA.
  如果 CMMA 完全不发散 → "多模修复了发散" → 方向变弱.

R4 重大发现 (影响 R2):
  发散主要由高 μ 数值不稳定驱动, 深衰落不是必要触发条件 (57% 发散前零深衰落).
  → CMMA 可能也会发散 (梯度噪声机制不变).
  关键对比: CMMA vs CMA 在相同 μ 下的 P_div.

CMMA 架构 (不改 common/_cma.py, P4 原则):
  - 继承 CMAEqualizer2x2 的蝶形结构 (4 个复 FIR: wxx/wxy/wyx/wyy)
  - 误差函数改为多模: 对 16QAM 三环 |s|² ∈ {0.2,1.0,1.8}, 取最近环算误差
      e[n] = nearest_R2 − |z[n]|²
  - 块级更新 (block_size=64, 跟 CMA 一致, sat.1553 §6.3 L756)
  - 发散判据同 CMA: |w|>10×init_norm OR |z|>1e3 OR NaN

公式溯源:
  - 多模 CMA: Oh & Chin 1999 "New blind equalization techniques based on
    cascaded multistage CMA", Quadriga & Barbarossa 2001 "Cascaded blind
    equalization for radio communications." 多 R² 匹配多环星座.
  - 16QAM 三环: |s|² ∈ {2,10,18}/10 = {0.2,1.0,1.8}, probs {4/16,8/16,4/16}.
  - QPSK 退化: R2_rings=[1.0] = 单模 CMA (Godard 1980).
"""
import sys
import os
import json
import time
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from params import SimulationConfig


# ─── 参数 (FR-20 溯源, 从 params.py 读) ─────────────────────

cfg = SimulationConfig()

TURB_LEVELS = {
    'weak':          cfg.turbulence.as_dict()['weak'],
    'moderate':      cfg.turbulence.as_dict()['moderate'],
    'strong':        cfg.turbulence.as_dict()['strong'],
    'uplink_strong': cfg.turbulence.as_dict()['uplink_strong'],
}

F_G_SWEEP = [30.0, 100.0, 300.0, 1000.0]
MU_SWEEP = [5e-4, 1e-3, 5e-3, 1e-2]
TAP_SWEEP = [11, 22]

N_SYMBOLS = 5_000_000
N_TRIALS = 3
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100 → noise_var = 1/(2*100) = 0.005
BLOCK = cfg.experiment.BLOCK  # 100
T_S = cfg.system.T_S  # 1/2.5e9
R_SYM = cfg.system.R_SYM
SOP_RATE = 1e-4  # 跟 Step B 一致 (cma_divergence_scan.py 用 1e-4)

# 16QAM 恒模半径 (Godard 1980): R² = E[|s|⁴]/E[|s|²] = 1.32
R2_16QAM = 1.32
R2_QPSK = 1.0
# 16QAM 三环 CMMA: |s|² ∈ {0.2, 1.0, 1.8}
R2_RINGS_16QAM = np.array([0.2, 1.0, 1.8])
# QPSK 单环 CMMA (退化到 CMA)
R2_RINGS_QPSK = np.array([1.0])


# ─── CMMA 均衡器 (继承 CMAEqualizer2x2, 重写误差函数) ──────

class CMMAEqualizer2x2(CMAEqualizer2x2):
    """Cascaded Multi-Modulus CMA (Oh & Chin 1999, Quadriga 2001).

    与 CMAEqualizer2x2 唯一区别: 误差函数从单模 e = R² − |z|² 改为
    多模 e = nearest_R2 − |z|², 其中 nearest_R2 是离 |z|² 最近的星座环.

    其余 (蝶形结构 4 FIR, 中心抽头初始化, 块级更新 block_size=64,
    发散判据 |w|>10×init OR |z|>1e3 OR NaN) 完全复用基类.

    参数
    ----
    n_tap : int
        每个 FIR 的抽头数.
    mu : float
        CMA 步长 μ.
    R2_rings : array-like
        星座模环的 R² 集合. 单元素时退化为标准 CMA.
    """

    def __init__(self, n_tap, mu, R2_rings):
        # 基类需要一个 R2 标量; 用第一个环初始化 (后面会用多模覆盖)
        super().__init__(n_tap=n_tap, mu=mu, R2=float(R2_rings[0]))
        self.R2_rings = np.asarray(R2_rings, dtype=float)
        self._is_single_modulus = (len(self.R2_rings) == 1)

    def _multi_modulus_error(self, z_blk):
        """多模误差: 对每个 z 找最近环 R², 返回 e = nearest_R2 − |z|².

        向量化实现: |z|² 与所有环的距离矩阵 → argmin 选最近环.
        单环时退化为 e = R2 − |z|² (标准 CMA).
        """
        abs_z2 = np.abs(z_blk) ** 2  # (block_size,)
        if self._is_single_modulus:
            return self.R2_rings[0] - abs_z2
        # 多模: 找每个样本最近的环
        # dist shape (block_size, n_rings)
        dist = np.abs(abs_z2[:, None] - self.R2_rings[None, :])
        nearest_idx = np.argmin(dist, axis=1)
        nearest_R2 = self.R2_rings[nearest_idx]
        return nearest_R2 - abs_z2

    def equalize(self, rX, rY, block_size=64):
        """块级 2×2 蝶形 CMMA 均衡. 结构同基类, 仅误差函数改为多模."""
        from numpy.lib.stride_tricks import sliding_window_view
        N = len(rX)
        L = self.n_tap
        half = L // 2

        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)
        w_norm_traj = np.zeros(N)
        z_amp_traj = np.zeros(N)

        rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
        rY_win = sliding_window_view(rY, L)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None
        n_valid = N - L + 1
        n_blocks = n_valid // block_size

        for blk in range(n_blocks):
            s = blk * block_size
            e = s + block_size
            if e > n_valid:
                break

            rX_blk = rX_win[s:e]
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # 多模误差 (唯一与 CMA 不同的地方)
            eX = self._multi_modulus_error(zx_blk)
            eY = self._multi_modulus_error(zy_blk)
            self.wxx += self.mu * np.mean(eX[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * np.mean(eX[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += self.mu * np.mean(eY[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += self.mu * np.mean(eY[:, None] * np.conj(rY_blk), axis=0)

            cur_norm = self.weights_norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            w_norm_traj[idx + block_size - 1] = cur_norm
            z_amp_traj[idx + block_size - 1] = cur_zamp

            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break

        return {
            'zX': zX, 'zY': zY,
            'w_norm_traj': w_norm_traj,
            'z_amp_traj': z_amp_traj,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self.weights_norm(),
            'init_w_norm': self._init_norm,
        }


# ─── 16QAM 调制/解调 (复用自 sup_stress_test.py) ────────────

QAM16_LEVELS = np.array([-3, -1, 1, 3])
QAM16_NORM = np.sqrt(10.0)


def gen_16qam(N, rng):
    """16QAM Gray-coded, E[|s|²]=1."""
    levels = QAM16_LEVELS / QAM16_NORM
    I_idx = rng.integers(0, 4, N)
    Q_idx = rng.integers(0, 4, N)
    s = levels[I_idx] + 1j * levels[Q_idx]
    return s


def gen_qpsk(N, rng):
    """QPSK 符号, |s|=1."""
    bits = rng.integers(0, 2, N * 2)
    return ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)


# ─── 信道生成 (跟 cma_divergence_scan.py / sup_stress_test.py 一致) ──

def gen_channel(N, alpha, beta, f_g, sop_rate, seed, mod='qpsk'):
    """双偏振 GG 衰落 + SOP 旋转信道.

    信道模型:
      - 强度衰落: gg_time_envelope (Step A, 块内恒定块间 AR(1))
      - 双偏振: X/Y 共享 h (同大气路径), SOP 用 Jones 旋转
      - SOP 速率 sop_rate (rad/sample), 跟 cma_divergence_scan.py 一致用 1e-4
    """
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)

    if mod == 'qpsk':
        sX = gen_qpsk(N, rng)
        sY = gen_qpsk(N, rng)
    else:  # 16qam
        sX = gen_16qam(N, rng)
        sY = gen_16qam(N, rng)

    # SOP 旋转: sat.1553 Eq.(51) Jones J=rot(theta(t))
    theta = sop_rate * np.arange(N)
    rX = np.sqrt(h) * (np.cos(theta) * sX + np.sin(theta) * sY)
    rY = np.sqrt(h) * (-np.sin(theta) * sX + np.cos(theta) * sY)

    noise_var = 1.0 / (2 * GAMMA_BAR)
    rX += np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY += np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY


# ─── 单次发散测试 ───────────────────────────────────────────

def run_single_trial(turb_name, alpha, beta, f_g, mu, n_tap, seed,
                     mod='16qam', method='cmma'):
    """跑一次 (CMMA 或 CMA) 发散测试, 返回是否发散 + 统计."""
    rX, rY = gen_channel(N_SYMBOLS, alpha, beta, f_g, SOP_RATE, seed, mod=mod)

    if method == 'cmma':
        if mod == '16qam':
            R2_rings = R2_RINGS_16QAM
        else:
            R2_rings = R2_RINGS_QPSK
        eq = CMMAEqualizer2x2(n_tap=n_tap, mu=mu, R2_rings=R2_rings)
    else:  # cma (单模)
        R2 = R2_16QAM if mod == '16qam' else R2_QPSK
        eq = CMAEqualizer2x2(n_tap=n_tap, mu=mu, R2=R2)

    res = eq.equalize(rX, rY)

    return {
        'diverged': res['diverged'],
        'diverge_idx': res['diverge_idx'],
        'final_w_norm': res['final_w_norm'],
        'init_w_norm': res['init_w_norm'],
        'max_w_norm': float(np.max(res['w_norm_traj'])) if np.any(res['w_norm_traj'] > 0) else 0.0,
        'max_z_amp': float(np.max(res['z_amp_traj'])) if np.any(res['z_amp_traj'] > 0) else 0.0,
    }


# ─── 扫描主循环 ─────────────────────────────────────────────

def run_scan(turb_levels=None, f_g_list=None, mu_list=None, tap_list=None,
             n_trials=None, mod='16qam', methods=None, label='scan'):
    """跑 CMMA vs CMA 发散概率扫描.

    对每个 (turb, f_g, mu, tap) 组合, 每个 method 跑 n_trials 个种子.
    CMMA 和 CMA 用相同 seed → 配对对比 (控制变量).
    """
    turb_levels = turb_levels or TURB_LEVELS
    f_g_list = f_g_list or F_G_SWEEP
    mu_list = mu_list or MU_SWEEP
    tap_list = tap_list or TAP_SWEEP
    n_trials = n_trials or N_TRIALS
    methods = methods or ['cmma', 'cma']

    total_combos = (len(turb_levels) * len(f_g_list) *
                    len(mu_list) * len(tap_list) * len(methods))
    total_runs = total_combos * n_trials
    print(f"[{label}] mod={mod}")
    print(f"  {len(turb_levels)} turb × {len(f_g_list)} f_G × "
          f"{len(mu_list)} mu × {len(tap_list)} tap × "
          f"{len(methods)} method × {n_trials} trials = {total_runs} runs")
    print(f"  N_symbols={N_SYMBOLS}, methods={methods}")

    results = []
    run_count = 0
    t_start = time.time()

    for turb_name, (alpha, beta) in turb_levels.items():
        for f_g in f_g_list:
            for mu in mu_list:
                for n_tap in tap_list:
                    for method in methods:
                        diverge_count = 0
                        trial_details = []
                        for trial in range(n_trials):
                            seed = hash((turb_name, f_g, mu, n_tap, mod, trial)) % (2**32)
                            res = run_single_trial(
                                turb_name, alpha, beta, f_g, mu, n_tap, seed,
                                mod=mod, method=method)
                            if res['diverged']:
                                diverge_count += 1
                            trial_details.append({
                                'seed': seed,
                                'diverged': res['diverged'],
                                'diverge_idx': res['diverge_idx'],
                                'max_w_norm': res['max_w_norm'],
                                'max_z_amp': res['max_z_amp'],
                            })
                            run_count += 1

                        p_div = diverge_count / n_trials
                        combo = {
                            'turb_name': turb_name,
                            'alpha': alpha, 'beta': beta,
                            'f_g_hz': f_g,
                            'tau_c_ms': cfg.gg_time.tau_c_from_fg(f_g) * 1e3,
                            'mu': mu,
                            'n_tap': n_tap,
                            'mod': mod,
                            'method': method,
                            'n_trials': n_trials,
                            'diverge_count': diverge_count,
                            'p_div': p_div,
                            'trials': trial_details,
                        }
                        results.append(combo)

                        elapsed = time.time() - t_start
                        eta = elapsed / run_count * (total_runs - run_count)
                        print(f"  [{run_count}/{total_runs}] {turb_name} f_G={f_g:.0f} "
                              f"μ={mu:.0e} tap={n_tap} {mod}/{method}"
                              f" → P_div={p_div:.2f} ({diverge_count}/{n_trials})"
                              f"  [{elapsed:.0f}s, ETA {eta:.0f}s]")

    return {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'B (R2: CMMA vs CMA 发散扫描)',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'n_symbols': N_SYMBOLS,
            'n_trials': n_trials,
            'gamma_bar': GAMMA_BAR,
            'block': BLOCK,
            't_s': T_S,
            'r_sym': R_SYM,
            'sop_rate': SOP_RATE,
            'dual_pol': True,
            'method': 'gar',
            'cmma_R2_rings_16qam': [0.2, 1.0, 1.8],
            'cma_R2_16qam': R2_16QAM,
            'cma_R2_qpsk': R2_QPSK,
        },
        'scan_dims': {
            'turb_levels': list(turb_levels.keys()),
            'f_g_hz': f_g_list,
            'mu': mu_list,
            'n_tap': tap_list,
            'methods': methods,
        },
        'results': results,
    }


# ─── 结果保存 ───────────────────────────────────────────────

def save_results(summary, filename):
    out_dir = SIM_DIR / 'results' / 'cma-fade-divergence'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to: {out_path}")
    return out_path


# ─── 汇总表打印 ─────────────────────────────────────────────

def print_comparison_table(summary):
    """打印 CMMA P_div vs CMA P_div 对比表 (按 μ 和 f_G 分组)."""
    results = summary['results']
    turb_levels = summary['scan_dims']['turb_levels']
    f_g_list = summary['scan_dims']['f_g_hz']
    mu_list = summary['scan_dims']['mu']
    tap_list = summary['scan_dims']['n_tap']
    mod = results[0]['mod'] if results else '?'

    # 索引: (turb, f_g, mu, tap, method) → p_div
    lookup = {(r['turb_name'], r['f_g_hz'], r['mu'], r['n_tap'], r['method']): r['p_div']
              for r in results}

    print("\n" + "=" * 78)
    print(f"P_div 对比表 (mod={mod}) — CMMA vs CMA")
    print("=" * 78)

    for turb_name in turb_levels:
        for n_tap in tap_list:
            print(f"\n[{turb_name}, tap={n_tap}]")
            # 表头: μ 行, f_G 列, CMMA/CMA 交替
            header = f"{'μ':>10}"
            for f_g in f_g_list:
                header += f" | f_G={f_g:>5.0f}: CMMA  CMA"
            print(header)
            print("-" * len(header))
            for mu in mu_list:
                row = f"{mu:>10.0e}"
                for f_g in f_g_list:
                    p_cmma = lookup.get((turb_name, f_g, mu, n_tap, 'cmma'))
                    p_cma = lookup.get((turb_name, f_g, mu, n_tap, 'cma'))
                    if p_cmma is not None:
                        row += f" |          {p_cmma:5.2f}  {p_cma:4.2f}"
                    else:
                        row += f" |            N/A"
                print(row)


# ─── 入口 ───────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='R2: CMMA vs CMA 发散扫描')
    parser.add_argument('--smoke', action='store_true',
                        help='快速 smoke test (小规模验证正确性 + 计时)')
    parser.add_argument('--n-symbols', type=int, default=N_SYMBOLS)
    parser.add_argument('--n-trials', type=int, default=N_TRIALS)
    args = parser.parse_args()

    N_SYMBOLS = args.n_symbols
    N_TRIALS = args.n_trials

    t0 = time.time()

    if args.smoke:
        # Smoke: strong+uplink × 2 f_G × 2 mu × 1 tap × 2 method × 3 trials
        # 用较小 N_symbols 快速验证正确性 + 计时
        N_SYMBOLS_LOCAL = min(N_SYMBOLS, 500_000)
        print("=" * 78)
        print(f"SMOKE TEST (N={N_SYMBOLS_LOCAL})")
        print("=" * 78)
        # 临时覆盖全局
        globals()['N_SYMBOLS'] = N_SYMBOLS_LOCAL
        summary_16 = run_scan(
            turb_levels={'strong': TURB_LEVELS['strong'],
                         'uplink_strong': TURB_LEVELS['uplink_strong']},
            f_g_list=[100.0, 1000.0],
            mu_list=[5e-3, 1e-2],
            tap_list=[11],
            n_trials=3,
            mod='16qam',
            methods=['cmma', 'cma'],
            label='smoke-16qam',
        )
        print_comparison_table(summary_16)
        save_results(summary_16, 'r2_cmma_smoke_16qam.json')
        print(f"\nSmoke time: {time.time()-t0:.0f}s")
    else:
        # 全量扫描: 16QAM + QPSK 对照
        # 时间预算 ≤15 分钟. 16QAM 全量 = 4×4×4×2×2×3 = 1536 runs × 5M.
        # 用 strong+uplink × 4 f_G × 4 mu × 1 tap(11) × 2 method × 3 = 192 runs per mod.
        print("=" * 78)
        print("FULL SCAN (16QAM + QPSK 对照)")
        print("=" * 78)

        all_summaries = {}

        print("\n[Phase 1] 16QAM: strong+uplink_strong, tap=11")
        summary_16 = run_scan(
            turb_levels={'strong': TURB_LEVELS['strong'],
                         'uplink_strong': TURB_LEVELS['uplink_strong']},
            f_g_list=F_G_SWEEP,
            mu_list=MU_SWEEP,
            tap_list=[11],
            n_trials=N_TRIALS,
            mod='16qam',
            methods=['cmma', 'cma'],
            label='16qam',
        )
        print_comparison_table(summary_16)
        all_summaries['16qam'] = summary_16

        print("\n[Phase 2] QPSK 对照: strong+uplink_strong, tap=11")
        summary_qpsk = run_scan(
            turb_levels={'strong': TURB_LEVELS['strong'],
                         'uplink_strong': TURB_LEVELS['uplink_strong']},
            f_g_list=F_G_SWEEP,
            mu_list=MU_SWEEP,
            tap_list=[11],
            n_trials=N_TRIALS,
            mod='qpsk',
            methods=['cmma', 'cma'],
            label='qpsk',
        )
        print_comparison_table(summary_qpsk)
        all_summaries['qpsk'] = summary_qpsk

        # 合并保存
        merged = {
            'meta': {
                'direction': 'Q-CMA-FADE',
                'step': 'B (R2: CMMA vs CMA 发散扫描)',
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'elapsed_s': time.time() - t0,
                'n_symbols': N_SYMBOLS,
                'n_trials': N_TRIALS,
                'description': 'CMMA (multi-modulus, 16QAM 三环) vs CMA (单模) '
                               '发散概率对比, 验证多模修复星座失配但修不好高μ发散.',
            },
            '16qam': summary_16,
            'qpsk': summary_qpsk,
            # 扁平化 results 列表 (方便分析)
            'results': summary_16['results'] + summary_qpsk['results'],
        }
        save_results(merged, 'r2_cmma_divergence_results.json')
        print(f"\nTotal time: {time.time()-t0:.0f}s")
