"""PROMPT-032 D3 MMA (多模算法) vs CMA — 攻 SOP swap 盆地对称 MVE.

> 方向: Q-CMA-FADE 方法层解冻 (D030, 机制 D 换范式) / 状态: WIP / 创建: 2026-07-16
> 组织规范: ../../SIM-ORG.md (P4 只扩不改 common/; P5 标方向+状态)
> 来源: PROMPT-032 (S033 Tier 1, 主控派出, 方向 2)

## 研究问题

S033 坐实 swap 是 SOP 累积旋转的物理现象（临界角 29°~114°），CMA 和 ML 在新域
4.2/1.4 都 100% swap（fixed-label BER≈0.5）。机制 = 恒模代价"正确盆地/交换盆地"
在 SOP 旋转下势能反转。

D3 MMA（multi-modulus algorithm，CMA 直系变种，Yang 2002 JSAC / Oh & Chin 1999）
分离实/虚部模值：J = E[(R²_R - z_R²)² + (R²_I - z_I²)²]，对 QAM 天然。
**核心假设**：MMA 的轴分离代价打破 CMA 的旋转不变性（CMA 只依赖 |z|² → 任何旋转
零代价 → 相位模糊 → swap 盆地等势），钉住相位可能抵抗 SOP 旋转驱动的 swap。

## TL-20 假设（跑前写，含信息论边界先验）

H_MMA (机制, 主): MMA 轴分离代价打破旋转不变性 → swap 盆地不再等势 → MMA
  fixed-label BER 显著低于 CMA（swap 率下降）。
  预测: MMA fixed_ber < 0.1（多数 seed 不 swap），CMA fixed_ber ≈ 0.5（全 swap）。
H_info_bound (S032 §B 信息论, 强先验): MMA 是盲方法（D 类），swap 本质是 X/Y 排列
  模糊（无参考帧）；MMA 的模值分离是实/虚轴不是 X/Y 轴 → 期望下对 X/Y swap 不变。
  预测: MMA fixed_ber ≈ 0.5（与 CMA 一样 swap），PI-BER 接近 oracle（排列不变口径）。

预注册 Go/Kill（防事后移门槛，守铁律 #2 fixed-label BER 作 Go 判据）：
  - GO  : MMA mean fixed-label BER 显著低于 standard-CMA（≥4/5 seeds 胜 + 配对
          Wilcoxon p<0.05），且 MMA mean fixed_ber < 0.2（实质不 swap）
  - KILL: MMA 与 standard-CMA 无显著差异（swap 率相同，fixed_ber 都 ≈0.5）
          → 信息论边界坐实，盲方法（D 类）注定碰不到 fixed-label BER

## 关键约束（守纪律）

1. 守 FR-22: GW Step 1 检索完成（子 agent 报告：FSO+SOP swap 场景无硬撞车，GO）。
   邻近 = 光纤色散场景 MMA-singularity 线（Yang 2002 / Vgenis 2010 / Kikuchi 2011），
   非 FSO；OFC 2026 EKF (Liu, DOI 10.1364/ofc.2026.w2a.67) 是 FSO comparator 但用 EKF
   非 MMA、打 RSOP 不打 swap。2015 Kalman 邻近点未定位到（疑似误标注）。
2. 守 D030: 归类批量 + 消融可验（拿掉 SOP 这个 swap 驱动 → MMA≈CMA≈oracle）。
3. 守 D018: 双口径 fixed/PI 并报（复用 prompt012 evaluate_outputs）。
4. 守铁律 #3: swap 分类用 correlation 口径（prompt012 evaluate_outputs），不用
   divergence trigger 口径（prompt029 那个在新域失灵）。
5. 不改 common/: 隔离脚本，MMA / standard-CMA 在本文件内实现，复用 gen_channel /
   oracle / evaluate_outputs。
6. 参数域与 S033 一致: N=5M/f_G=30/SOP=4e-7/strong(4.2/1.4)/20dB/QPSK,
   seeds 1000-1004（prompt030 证实新域 CMA/ML 全 swap 的子集）, late [4.375M, 5M)。
7. D020 公平性: 主基线 = standard-CMA（有 z 因子，Godard 1980 标准）；同时报
   current-scalar-CMA（common/_cma.py 现版，无 z 因子）作 sanity 对照（应复现
   prompt030 的 10/10 swap）。

## MMA 公式溯源 (FR-20)

- MMA 代价: Yang 2002 JSAC "MMA" + Oh & Chin 1999. J = E[(R²_R-z_R²)² + (R²_I-z_I²)²]
- 恒模半径（按轴）: R²_k = E[s_k⁴]/E[s_k²], k∈{R,I}. QPSK: s_R=s_I=±1/√2,
  s_R²=0.5, s_R⁴=0.25 → R²_R = R²_I = 0.25/0.5 = 0.5
- MMA 更新（含 z 因子，与 standard-CMA 公平）:
    err = (R²_R - z_R²)·z_R + j·(R²_I - z_I²)·z_I
    w += μ · mean(err · conj(r))
  对比 standard-CMA: err = (R² - |z|²)·z;  w += μ·mean(err·conj(r))
  差异仅在误差分解（轴分离 vs 耦合），z 因子结构相同 → 公平对比。

用法:
  cd projects/simulation && python explore/cma-fade-divergence/prompt032_d3_mma_mve.py
"""
from __future__ import annotations

import json
import sys
import tempfile
import os
import time
from pathlib import Path
from itertools import combinations
from collections import defaultdict

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

# 路径设置
SIM_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 同级 import

from params import SimulationConfig
from common._config import BLOCK
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2  # current scalar-error CMA (sanity 对照)
from ml_long_seq_failure import (  # type: ignore
    F_G, GAMMA_BAR, N_TAP, SOP_RATE, T_S, MU_SAFE, R2_QPSK,
    gen_qpsk, qpsk_demap, compute_ber_phase_corrected, test_late_slice,
    gen_channel, oracle_equalize,
)
from prompt012_longseq_audit import evaluate_outputs  # type: ignore  D018 双口径

cfg = SimulationConfig()

# ─── 实验参数（与 S033/prompt030 一致：新域 4.2/1.4）─────────
N_SYMBOLS = 5_000_000
TURBULENCE = "strong"          # α=4.2, β=1.4 (Gu 2022, S032 审计确认的新正确域)
SEEDS = (1000, 1001, 1002, 1003, 1004)  # prompt030 证实新域 CMA/ML 全 swap 的子集
LATE_S, LATE_E = test_late_slice(N_SYMBOLS)  # [4.375M, 5M)

# MMA 模值（QPSK 按轴）
R2_R = 0.5   # R²_R = E[s_R⁴]/E[s_R²] = 0.25/0.5
R2_I = 0.5   # R²_I 同
# CMA 模值
R2_CMA = R2_QPSK  # 1.0

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
OUT_PATH = RESULTS_DIR / 'prompt032_d3_mma_mve.json'


# ─── MMA / standard-CMA 隔离实现（2×2 蝶形，块级更新，与 common/_cma.py 同结构）──

class _ButterflyBlockEqualizer:
    """2×2 蝶形块级均衡器骨架（复用 common/_cma.py 结构，仅改误差函数）.

    子类实现 _error(zx, zy) → (errX, errY) 复值误差（已含 z 因子结构）.
    更新: w += μ·mean(err·conj(r_blk))，与 common/_cma.py 块级更新一致.
    """

    def __init__(self, n_tap, mu):
        self.n_tap = n_tap
        self.mu = mu
        center = n_tap // 2
        self.wxx = np.zeros(n_tap, dtype=complex)
        self.wxy = np.zeros(n_tap, dtype=complex)
        self.wyx = np.zeros(n_tap, dtype=complex)
        self.wyy = np.zeros(n_tap, dtype=complex)
        self.wxx[center] = 1.0
        self.wyy[center] = 1.0
        self._init_norm = self._norm()

    def _norm(self):
        return float(np.sqrt(
            np.sum(np.abs(self.wxx)**2) + np.sum(np.abs(self.wxy)**2) +
            np.sum(np.abs(self.wyx)**2) + np.sum(np.abs(self.wyy)**2)))

    def _error(self, zx, zy):
        """子类实现: 返回 (errX, errY) 复值误差 (block_size,)."""
        raise NotImplementedError

    def equalize(self, rX, rY, block_size=64):
        N = len(rX)
        L = self.n_tap
        half = L // 2
        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)
        rX_win = sliding_window_view(rX, L)
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
            errX, errY = self._error(zx_blk, zy_blk)
            self.wxx += self.mu * np.mean(errX[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * np.mean(errX[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += self.mu * np.mean(errY[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += self.mu * np.mean(errY[:, None] * np.conj(rY_blk), axis=0)
            cur_norm = self._norm()
            cur_zamp = float(np.max(np.maximum(np.abs(zx_blk), np.abs(zy_blk))))
            if not diverged:
                if (cur_norm > norm_thresh or cur_zamp > z_amp_thresh
                        or not np.isfinite(cur_norm)):
                    diverged = True
                    diverge_idx = idx + block_size - 1
                    break
        return {'zX': zX, 'zY': zY, 'diverged': diverged, 'diverge_idx': diverge_idx,
                'final_w_norm': self._norm(), 'init_w_norm': self._init_norm}


class MMAEqualizer2x2(_ButterflyBlockEqualizer):
    """多模算法 (Yang 2002 JSAC / Oh & Chin 1999). 实/虚部模值分离.

    err = (R²_R - z_R²)·z_R + j·(R²_I - z_I²)·z_I   (含 z 因子, 与 standard-CMA 公平)
    机制: 轴分离代价打破 CMA 的旋转不变性 (CMA 只依赖 |z|²).
    """

    def __init__(self, n_tap, mu, R2_R=0.5, R2_I=0.5):
        super().__init__(n_tap, mu)
        self.R2_R = R2_R
        self.R2_I = R2_I

    def _error(self, zx, zy):
        eX_R = self.R2_R - zx.real**2
        eX_I = self.R2_I - zx.imag**2
        errX = eX_R * zx.real + 1j * eX_I * zx.imag
        eY_R = self.R2_R - zy.real**2
        eY_I = self.R2_I - zy.imag**2
        errY = eY_R * zy.real + 1j * eY_I * zy.imag
        return errX, errY


class StandardCMA2x2(_ButterflyBlockEqualizer):
    """标准 Godard 1980 CMA (有 z 因子, D021/D022 合法基线).

    err = (R² - |z|²)·z   (e·z, D021 称的"z 因子")
    """

    def __init__(self, n_tap, mu, R2=1.0):
        super().__init__(n_tap, mu)
        self.R2 = R2

    def _error(self, zx, zy):
        eX = self.R2 - np.abs(zx)**2
        eY = self.R2 - np.abs(zy)**2
        return eX * zx, eY * zy


# ─── 配对 Wilcoxon（复用 prompt024 实现，无 scipy 依赖）─────────

def paired_wilcoxon_p(a, b):
    """配对 Wilcoxon 双侧 p 值（精确，小样本 n≤30）."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    d = a - b
    d = d[d != 0]
    n = len(d)
    if n == 0:
        return 1.0
    signs = (d > 0).astype(int)
    abs_d = np.abs(d)
    order = np.argsort(abs_d)
    ranks = np.empty(n)
    ranks[order] = np.arange(1, n + 1)
    sorted_abs = abs_d[order]
    i = 0
    while i < n:
        j = i
        while j + 1 < n and sorted_abs[j + 1] == sorted_abs[i]:
            j += 1
        if j > i:
            avg = (ranks[order[i]] + ranks[order[j]]) / 2.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg
        i = j + 1
    w_plus = float(np.sum(ranks[signs == 1]))
    rank_list = ranks.tolist()
    coef = defaultdict(int)
    coef[0.0] = 1
    for rk in rank_list:
        new = defaultdict(int)
        for s, c in coef.items():
            new[s] += c
            new[s + rk] += c
        coef = new
    total_count = sum(coef.values())
    ge = sum(c for s, c in coef.items() if s >= w_plus - 1e-9)
    le = sum(c for s, c in coef.items() if s <= w_plus + 1e-9)
    p_one_side = min(ge, le) / total_count
    return float(min(1.0, 2.0 * p_one_side))


# ─── 单 seed 三方法评估 ──────────────────────────────────────

def run_seed(seed, alpha, beta):
    """生成信道 → MMA / standard-CMA / current-CMA / oracle 四方法 → late-slice 评估."""
    t0 = time.time()
    rX, rY, sX, sY, h, theta = gen_channel(
        N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)
    sX_l, sY_l = sX[LATE_S:LATE_E], sY[LATE_S:LATE_E]
    methods = {}

    # MMA
    mma = MMAEqualizer2x2(N_TAP, MU_SAFE, R2_R=R2_R, R2_I=R2_I)
    res = mma.equalize(rX, rY)
    zX, zY = res['zX'][LATE_S:LATE_E], res['zY'][LATE_S:LATE_E]
    methods['mma'] = evaluate_outputs(zX, zY, sX_l, sY_l, bool(res['diverged']))
    methods['mma']['diverge_idx'] = res['diverge_idx']
    methods['mma']['final_w_norm'] = res['final_w_norm']

    # standard-CMA (有 z 因子, D021/D022 合法基线, 主对照)
    scma = StandardCMA2x2(N_TAP, MU_SAFE, R2=R2_CMA)
    res = scma.equalize(rX, rY)
    zX, zY = res['zX'][LATE_S:LATE_E], res['zY'][LATE_S:LATE_E]
    methods['standard_cma'] = evaluate_outputs(zX, zY, sX_l, sY_l, bool(res['diverged']))
    methods['standard_cma']['diverge_idx'] = res['diverge_idx']
    methods['standard_cma']['final_w_norm'] = res['final_w_norm']

    # current scalar-error CMA (common/_cma.py, sanity 对照, 应复现 prompt030 全 swap)
    ccma = CMAEqualizer2x2(n_tap=N_TAP, mu=MU_SAFE, R2=R2_CMA)
    res = ccma.equalize(rX, rY)
    zX, zY = res['zX'][LATE_S:LATE_E], res['zY'][LATE_S:LATE_E]
    methods['current_cma'] = evaluate_outputs(zX, zY, sX_l, sY_l, bool(res['diverged']))
    methods['current_cma']['diverge_idx'] = res['diverge_idx']

    # oracle (完美 CSI 上界)
    zX_or, zY_or = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    methods['oracle'] = evaluate_outputs(
        zX_or[LATE_S:LATE_E], zY_or[LATE_S:LATE_E], sX_l, sY_l, False)

    # 摘要
    elapsed = time.time() - t0
    summary_line = " | ".join(
        f"{m}:fixed={methods[m]['fixed_label_ber']['mean']:.4f},"
        f"pi={methods[m]['permutation_invariant_ber']['mean']:.4f},"
        f"class={methods[m]['classification']}"
        for m in ('mma', 'standard_cma', 'current_cma', 'oracle'))
    print(f"  seed{seed}: {summary_line} ({elapsed:.0f}s)", flush=True)

    return {'seed': int(seed), 'methods': methods, 'elapsed_s': elapsed}


def _save(payload):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".prompt032_", suffix=".json", dir=RESULTS_DIR)
    os.close(fd)
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, OUT_PATH)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    t0 = time.time()
    alpha, beta = cfg.turbulence.as_dict()[TURBULENCE]
    print("=" * 78)
    print("PROMPT-032: D3 MMA (多模算法) vs CMA — 攻 SOP swap 盆地对称 MVE")
    print(f"参数: N={N_SYMBOLS}, f_G={F_G}, SOP={SOP_RATE}(1krad/s), turb={TURBULENCE} "
          f"(α={alpha},β={beta}), 20dB, QPSK, tap={N_TAP}, μ={MU_SAFE}")
    print(f"  MMA: R²_R=R²_I={R2_R} (轴分离), standard-CMA: R²={R2_CMA} (有z因子)")
    print(f"  seeds={SEEDS}, late=[{LATE_S},{LATE_E})")
    print("=" * 78)

    payload = {
        'meta': {
            'direction': 'Q-CMA-FADE 方法层解冻 (D030) — D3 MMA (机制 D 换范式)',
            'step': 'PROMPT-032',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'params': {
                'N': N_SYMBOLS, 'f_G': F_G, 'sop_rate': SOP_RATE,
                'turbulence': TURBULENCE, 'alpha': alpha, 'beta': beta,
                'gamma_bar': GAMMA_BAR, 'n_tap': N_TAP, 'mod': 'qpsk',
                'mu': MU_SAFE, 'seeds': list(SEEDS),
                'mma_R2_R': R2_R, 'mma_R2_I': R2_I, 'cma_R2': R2_CMA,
                'late_slice': [LATE_S, LATE_E],
            },
            'gw_step1_search_verdict': (
                'GO (子 agent 报告: FSO+SOP swap 场景无硬撞车). 邻近=光纤色散场景 '
                'MMA-singularity 线 (Yang 2002/Vgenis 2010/Kikuchi 2011) 非 FSO; '
                'OFC 2026 EKF (Liu 10.1364/ofc.2026.w2a.67) FSO comparator 但用 EKF 打 '
                'RSOP 不打 swap. 2015 Kalman 邻近点未定位到 (疑似误标注).'),
            'tl20_hypotheses': {
                'H_MMA': 'MMA 轴分离代价打破旋转不变性 → swap 盆地不等势 → fixed_ber<0.1',
                'H_info_bound': 'MMA 盲方法(D类), swap=X/Y排列模糊; 模值分离是实/虚轴非X/Y轴 → fixed_ber≈0.5 (强先验 KILL)',
                'go_kill_preregistered': 'GO: MMA mean fixed_ber < standard-CMA, ≥4/5 胜 p<0.05, 且 mean<0.2; 否则 KILL',
            },
        },
        'trials': [],
    }
    _save(payload)

    # ── Phase 1: 主对比 (MMA vs standard-CMA vs current-CMA vs oracle) ──
    print("\n[Phase 1] 主对比 (5 seeds)")
    for seed in SEEDS:
        trial = run_seed(seed, alpha, beta)
        payload['trials'].append(trial)
        _save(payload)

    # ── Phase 2: Go/Kill 判定 (MMA vs standard-CMA, fixed-label BER) ──
    print("\n[Phase 2] Go/Kill 判定 (MMA vs standard-CMA, fixed-label BER)")
    mma_fixed = [t['methods']['mma']['fixed_label_ber']['mean'] for t in payload['trials']]
    scma_fixed = [t['methods']['standard_cma']['mean'] for t in payload['trials']] \
        if False else [t['methods']['standard_cma']['fixed_label_ber']['mean'] for t in payload['trials']]
    ccma_fixed = [t['methods']['current_cma']['fixed_label_ber']['mean'] for t in payload['trials']]
    mma_pi = [t['methods']['mma']['permutation_invariant_ber']['mean'] for t in payload['trials']]
    scma_pi = [t['methods']['standard_cma']['permutation_invariant_ber']['mean'] for t in payload['trials']]
    orc_pi = [t['methods']['oracle']['permutation_invariant_ber']['mean'] for t in payload['trials']]
    orc_fixed = [t['methods']['oracle']['fixed_label_ber']['mean'] for t in payload['trials']]

    wins_mma_vs_scma = int(np.sum(np.array(mma_fixed) < np.array(scma_fixed)))
    p_mma_vs_scma = paired_wilcoxon_p(scma_fixed, mma_fixed)
    mma_mean = float(np.mean(mma_fixed))
    scma_mean = float(np.mean(scma_fixed))

    go_stat = (p_mma_vs_scma < 0.05 and wins_mma_vs_scma >= 4 and mma_mean < 0.2)
    verdict = 'GO' if go_stat else 'KILL'

    # swap 分类计数
    def swap_count(method_key):
        return sum(1 for t in payload['trials']
                   if 'swap' in t['methods'][method_key]['classification'])

    go_kill = {
        'mma_mean_fixed_ber': mma_mean,
        'mma_per_seed_fixed': mma_fixed,
        'standard_cma_mean_fixed_ber': scma_mean,
        'standard_cma_per_seed_fixed': scma_fixed,
        'current_cma_mean_fixed_ber': float(np.mean(ccma_fixed)),
        'oracle_mean_fixed_ber': float(np.mean(orc_fixed)),
        'mma_mean_pi_ber': float(np.mean(mma_pi)),
        'standard_cma_mean_pi_ber': float(np.mean(scma_pi)),
        'oracle_mean_pi_ber': float(np.mean(orc_pi)),
        'wins_mma_vs_standard_cma': wins_mma_vs_scma,
        'n_seeds': len(mma_fixed),
        'p_value_wilcoxon': p_mma_vs_scma,
        'mma_swap_count': swap_count('mma'),
        'standard_cma_swap_count': swap_count('standard_cma'),
        'current_cma_swap_count': swap_count('current_cma'),
        'verdict': verdict,
    }
    payload['go_kill'] = go_kill
    _save(payload)

    print(f"  MMA         fixed={mma_mean:.4f} (swap {swap_count('mma')}/{len(SEEDS)}) "
          f"PI={np.mean(mma_pi):.5f}")
    print(f"  standard-CMA fixed={scma_mean:.4f} (swap {swap_count('standard_cma')}/{len(SEEDS)}) "
          f"PI={np.mean(scma_pi):.5f}")
    print(f"  current-CMA  fixed={np.mean(ccma_fixed):.4f} (swap {swap_count('current_cma')}/{len(SEEDS)})")
    print(f"  oracle       fixed={np.mean(orc_fixed):.4f} PI={np.mean(orc_pi):.5f}")
    print(f"  MMA vs standard-CMA: 胜 {wins_mma_vs_scma}/{len(SEEDS)}, p={p_mma_vs_scma:.4f}")
    print(f"\n>>> D3 MMA 整体 Go/Kill: {verdict}")
    if verdict == 'KILL':
        print(f"    (信息论边界先验应验: MMA 盲方法 fixed_ber≈{mma_mean:.3f} 与 CMA≈{scma_mean:.3f} 同 swap)")

    # ── Phase 3: 消融/SOP=0 对照 (拿掉 swap 驱动 → MMA≈CMA≈oracle) ──
    # D030 消融可验: 去掉 SOP (swap 驱动), MMA 和 CMA 都应正常 (fixed_ber≈0, 不 swap)
    print("\n[Phase 3] 消融: SOP=0 (拿掉 swap 驱动), MMA/standard-CMA 应都正常")
    abl_trials = []
    for seed in SEEDS:
        t0s = time.time()
        rX, rY, sX, sY, h, theta = gen_channel(
            N_SYMBOLS, alpha, beta, F_G, 0.0, seed)  # SOP=0
        sX_l, sY_l = sX[LATE_S:LATE_E], sY[LATE_S:LATE_E]
        mma = MMAEqualizer2x2(N_TAP, MU_SAFE, R2_R=R2_R, R2_I=R2_I)
        res = mma.equalize(rX, rY)
        zX, zY = res['zX'][LATE_S:LATE_E], res['zY'][LATE_S:LATE_E]
        mma_eval = evaluate_outputs(zX, zY, sX_l, sY_l, bool(res['diverged']))
        scma = StandardCMA2x2(N_TAP, MU_SAFE, R2=R2_CMA)
        res = scma.equalize(rX, rY)
        zX, zY = res['zX'][LATE_S:LATE_E], res['zY'][LATE_S:LATE_E]
        scma_eval = evaluate_outputs(zX, zY, sX_l, sY_l, bool(res['diverged']))
        abl_trials.append({
            'seed': int(seed),
            'mma_fixed': mma_eval['fixed_label_ber']['mean'],
            'mma_class': mma_eval['classification'],
            'standard_cma_fixed': scma_eval['fixed_label_ber']['mean'],
            'standard_cma_class': scma_eval['classification'],
        })
        print(f"  SOP=0 seed{seed}: MMA fixed={mma_eval['fixed_label_ber']['mean']:.4f} "
              f"[{mma_eval['classification']}] | stdCMA fixed={scma_eval['fixed_label_ber']['mean']:.4f} "
              f"[{scma_eval['classification']}] ({time.time()-t0s:.0f}s)", flush=True)
    abl_mma = [t['mma_fixed'] for t in abl_trials]
    abl_scma = [t['standard_cma_fixed'] for t in abl_trials]
    ablation = {
        'trials': abl_trials,
        'mma_mean_fixed': float(np.mean(abl_mma)),
        'standard_cma_mean_fixed': float(np.mean(abl_scma)),
        'both_work_without_sop': bool(np.mean(abl_mma) < 0.1 and np.mean(abl_scma) < 0.1),
    }
    payload['ablation_sop0'] = ablation
    payload['meta']['elapsed_s'] = time.time() - t0
    _save(payload)
    print(f"  SOP=0 mean: MMA={np.mean(abl_mma):.4f} stdCMA={np.mean(abl_scma):.4f} "
          f"→ 消融{'PASS (都正常)' if ablation['both_work_without_sop'] else 'CHECK'}")

    print(f"\n结果已保存: {OUT_PATH}")
    print(f"总耗时: {time.time()-t0:.0f}s")
    print(f"\n=== D3 MMA 整体: {verdict} ===")
    return payload


if __name__ == '__main__':
    main()
