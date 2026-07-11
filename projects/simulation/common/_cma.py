"""CMA 均衡器：双偏振 2×2 蝶形恒模算法。

> 方向: Q-CMA-FADE (Step B, 分析层) | 状态: WIP | 创建: 2026-07-11
> 组织规范: ../SIM-ORG.md (P4 只扩不改；新算法=1新文件+0改动现有)

公式溯源 (C6 核心公式标来源 + 公式号，禁靠文字重建):
  - 蝶形结构: sat.1553 §6 Eq.(28) (content.md L570)
      zX = wxx ∗ rX + wxy ∗ rY
      zY = wyx ∗ rX + wyy ∗ rY
    其中 wxx,wxy,wyx,wyy 是 4 个复 FIR 滤波器, rX/rY 是双偏接收信号。
  - CMA 误差: sat.1553 §6 Eq.(50) (content.md L721) + Godard 1980 原文
      e[n] = R² − |z[n]|²   (恒模, QPSK)
    Godard 1980: D. Godard, "Self-Recovering Equalization and Carrier Tracking
    in Two-Dimensional Data Communication Systems," IEEE Trans. Commun. 28(11):
    1867-1875, 1980. Eq.(10) 定义恒模代价函数 J = E[(R²−|z|²)²]。
    (sat.1553 引 [84] Johnson et al. 1998 综述, 原始 CMA 公式来自 Godard 1980 [12])
  - 权重更新: sat.1553 §6 Eq.(48) (content.md L705, LMS/CMA 共用更新结构)
      W[n+1] = W[n] + μ · e[n] · r*[n]
    CMA 与 LMS 唯一区别在误差函数 (sat.1553 L715: "only the error function
    in Eq.(48) changes in the CMA algorithm")。
  - 恒模半径: R = E[|s|⁴] / E[|s|²] (Godard 1980)
    QPSK: |s|=1 → R = E[1]/E[1] = 1; R² = 1。
  - CMA 发散空白: sat.1553 §6.3 L778 自认
      "the probability of the equalizer diverging to a local optimum during
       deep fades has not been analyzed here"

参数溯源 (FR-20):
  - CMA 步长 μ: sat.1553 §6.3 L760 "step size parameter μ"; Qin 2025 L263
    用 22 tap 蝴蝶 + 收敛~10⁵ 符号 (隐含 μ 量级); 本模块 μ 作为扫描参数暴露
  - tap 数: sat.1553 §6 L572 "number of taps ... determined by channel impulse
    response length"; Qin 2025 L263 用 22 tap; sat.1553 Fig.13 仿真用 N=11 tap

发散判据 (预定义, 守 TL-20):
  - 系数范数 |w| 超阈值 (如 10× 初始范数)
  - 或均衡后符号幅度 |z| 超动态范围 (如 > 1e3)
  - 或 BER 突然恶化 (发散后不可恢复)
"""
import numpy as np


# ─── 恒模半径 ───────────────────────────────────────────────

def cma_radius(symbols):
    """计算 Godard 1980 恒模半径 R = E[|s|⁴] / E[|s|²]。

    QPSK (|s|=1): R=1, R²=1。
    16QAM: R² = E[|s|⁴]/E[|s|²] (多模 CMA 需多 R 值, 本模块先支持 QPSK)。
    """
    abs_s2 = np.abs(symbols) ** 2
    abs_s4 = np.abs(symbols) ** 4
    R2 = abs_s4.mean() / abs_s2.mean()
    return np.sqrt(R2)


# ─── 2×2 蝶形 CMA ──────────────────────────────────────────

class CMAEqualizer2x2:
    """双偏振 2×2 蝶形 CMA 均衡器 (sat.1553 §6 Eq.28/50, Godard 1980)。

    4 个复 FIR 滤波器: wxx, wxy, wyx, wyy (各 L_tap 抽头)。
    初始化: 中心抽头脉冲 (wxx/wyy 中心=1, wxy/wyx=0), 标准 CMA 初始化
    (sat.1553 §6 隐含, Qin 2025 L283 明确 "中心 1, 其余全零")。

    参数
    ----
    n_tap : int
        每个 FIR 的抽头数 (sat.1553 L572: 由信道脉冲响应长度定)。
    mu : float
        CMA 步长 (sat.1553 L760: "step size parameter μ")。
    R2 : float
        恒模半径平方 R² (QPSK=1, Godard 1980)。
    """

    def __init__(self, n_tap, mu, R2=1.0):
        self.n_tap = n_tap
        self.mu = mu
        self.R2 = R2
        # 4 个复 FIR: wxx, wxy, wyx, wyy
        # 中心抽头初始化 (Qin 2025 L283: hIXX/hIYY 中心=1, 其余=0)
        center = n_tap // 2
        self.wxx = np.zeros(n_tap, dtype=complex)
        self.wxy = np.zeros(n_tap, dtype=complex)
        self.wyx = np.zeros(n_tap, dtype=complex)
        self.wyy = np.zeros(n_tap, dtype=complex)
        self.wxx[center] = 1.0
        self.wyy[center] = 1.0
        # 记录初始范数 (发散判据用)
        self._init_norm = np.sqrt(
            np.sum(np.abs(self.wxx)**2) + np.sum(np.abs(self.wxy)**2) +
            np.sum(np.abs(self.wyx)**2) + np.sum(np.abs(self.wyy)**2)
        )

    def weights_norm(self):
        """当前 4 个 FIR 的总范数 |w|。"""
        return np.sqrt(
            np.sum(np.abs(self.wxx)**2) + np.sum(np.abs(self.wxy)**2) +
            np.sum(np.abs(self.wyx)**2) + np.sum(np.abs(self.wyy)**2)
        )

    def equalize(self, rX, rY, block_size=64):
        """块级 2×2 蝶形 CMA 均衡 (sat.1553 Eq.28/48/50, Godard 1980)。

        sat.1553 §6.3 L756 明确使用 "parallelization factor of 64" 的块级
        实现——块内用固定权重滤波 (向量化), 块末用块内平均梯度更新权重。
        这对应真实 FPGA 实现的串行-并行折衷, 物理上比纯逐符号更贴近工程。

        参数
        ----
        rX, rY : ndarray, shape (N,)
            双偏振接收信号 (复数)。
        block_size : int
            并行化因子 (sat.1553 L756: 64 或 256)。

        返回
        ----
        result : dict (zX/zY/w_norm_traj/z_amp_traj/diverged/diverge_idx/...)
        """
        from numpy.lib.stride_tricks import sliding_window_view
        N = len(rX)
        L = self.n_tap
        half = L // 2

        zX = np.zeros(N, dtype=complex)
        zY = np.zeros(N, dtype=complex)
        w_norm_traj = np.zeros(N)
        z_amp_traj = np.zeros(N)

        # 滑动窗口矩阵 (N-L+1, L) — 向量化所有 FIR 滤波
        rX_win = sliding_window_view(rX, L)  # (N-L+1, L)
        rY_win = sliding_window_view(rY, L)

        # 发散判据 (预定义, TL-20)
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

            # 块内向量化滤波: sat.1553 Eq.(28)
            # zX = wxx·rX + wxy·rY;  zY = wyx·rX + wyy·rY
            rX_blk = rX_win[s:e]  # (block_size, L)
            rY_blk = rY_win[s:e]
            zx_blk = rX_blk @ self.wxx + rY_blk @ self.wxy  # (block_size,)
            zy_blk = rX_blk @ self.wyx + rY_blk @ self.wyy

            # 写入输出 (对齐到 half 偏移)
            idx = s + half
            zX[idx:idx + block_size] = zx_blk
            zY[idx:idx + block_size] = zy_blk

            # 块末梯度更新: sat.1553 Eq.(48/50), Godard 1980
            # e = R² − |z|²;  W += μ · mean(e · r*)
            eX = self.R2 - np.abs(zx_blk)**2  # (block_size,)
            eY = self.R2 - np.abs(zy_blk)**2
            self.wxx += self.mu * np.mean(eX[:, None] * np.conj(rX_blk), axis=0)
            self.wxy += self.mu * np.mean(eX[:, None] * np.conj(rY_blk), axis=0)
            self.wyx += self.mu * np.mean(eY[:, None] * np.conj(rX_blk), axis=0)
            self.wyy += self.mu * np.mean(eY[:, None] * np.conj(rY_blk), axis=0)

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

        return {
            'zX': zX, 'zY': zY,
            'w_norm_traj': w_norm_traj,
            'z_amp_traj': z_amp_traj,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self.weights_norm(),
            'init_w_norm': self._init_norm,
        }


# ─── 单偏振 CMA (退化版, 供无 SOP 旋转的纯衰落发散分析) ─────

class CMAEqualizer1x1:
    """单偏振 CMA 均衡器 (Godard 1980, 蝶形退化 wxy=wyx=0)。

    用于纯强度衰落场景的发散分析 (无偏振串扰时 2×2 退化为两个独立 1×1)。
    公式同 2×2 版, 仅 z = w ∗ r, e = R² − |z|², w += μ·e·r*。
    """

    def __init__(self, n_tap, mu, R2=1.0):
        self.n_tap = n_tap
        self.mu = mu
        self.R2 = R2
        center = n_tap // 2
        self.w = np.zeros(n_tap, dtype=complex)
        self.w[center] = 1.0
        self._init_norm = np.linalg.norm(self.w)

    def weights_norm(self):
        return np.linalg.norm(self.w)

    def equalize_blockwise(self, r, block_size=64):
        """块级 CMA 均衡 (sat.1553 §6.3 并行化因子, 工程标准实现)。

        权重在每 block 内固定, block 间更新一次 (块内用块首权重滤波,
        块末用输出计算梯度更新权重)。这模拟 FPGA 并行实现
        (sat.1553 L756: "parallelization factor of 64")。

        比逐符号快 ~block_size 倍, 且物理上对应真实硬件实现。
        """
        N = len(r)
        L = self.n_tap
        half = L // 2
        n_blocks = N // block_size

        z = np.zeros(N, dtype=complex)
        w_norm_traj = np.zeros(N)
        z_amp_traj = np.zeros(N)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None

        # 构建滑动窗口矩阵 (N-L+1, L) 用于向量化滤波
        from numpy.lib.stride_tricks import sliding_window_view
        if N > L:
            r_windows = sliding_window_view(r, L)  # shape (N-L+1, L)

        for blk in range(n_blocks):
            start = blk * block_size
            end = start + block_size
            if end + half >= N - half:
                break

            # 块内滤波 (向量化): z = w · r_windows (块内所有符号)
            win_start = start  # 对齐 sliding_window_view 起始
            win_end = min(end, len(r_windows))
            if win_end <= win_start:
                continue
            r_blk = r_windows[win_start:win_end]  # (block, L)
            z_blk = r_blk @ self.w  # (block,) — 向量化 FIR
            z[start:start + len(z_blk)] = z_blk

            # 块末梯度更新 (用块内平均梯度, 对应并行实现)
            e_blk = self.R2 - np.abs(z_blk)**2  # (block,)
            grad = np.mean(e_blk[:, None] * np.conj(r_blk), axis=0)  # (L,)
            self.w += self.mu * grad

            # 记录轨迹 (块末)
            cur_norm = self.weights_norm()
            cur_zamp = float(np.max(np.abs(z_blk))) if len(z_blk) > 0 else 0
            idx_end = start + len(z_blk) - 1
            w_norm_traj[idx_end] = cur_norm
            z_amp_traj[idx_end] = cur_zamp

            # 发散检测
            if not diverged:
                if cur_norm > norm_thresh or cur_zamp > z_amp_thresh or not np.isfinite(cur_norm):
                    diverged = True
                    diverge_idx = idx_end
                    break

        return {
            'z': z,
            'w_norm_traj': w_norm_traj,
            'z_amp_traj': z_amp_traj,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self.weights_norm(),
            'init_w_norm': self._init_norm,
        }

    def equalize(self, r):
        """逐符号运行单偏振 CMA (Godard 1980)。"""
        N = len(r)
        L = self.n_tap
        half = L // 2

        z = np.zeros(N, dtype=complex)
        w_norm_traj = np.zeros(N)
        z_amp_traj = np.zeros(N)

        norm_thresh = 10.0 * self._init_norm
        z_amp_thresh = 1e3

        diverged = False
        diverge_idx = None

        for n in range(half, N - half):
            r_win = r[n - half : n - half + L]
            zn = np.dot(self.w, r_win)
            z[n] = zn

            # 发散检测 (更新前检查, 防溢出 NaN)
            cur_norm = self.weights_norm()
            cur_zamp = np.abs(zn)
            w_norm_traj[n] = cur_norm
            z_amp_traj[n] = cur_zamp
            if not diverged:
                if cur_norm > norm_thresh or cur_zamp > z_amp_thresh or not np.isfinite(cur_norm):
                    diverged = True
                    diverge_idx = n
                    break  # 停止更新, 防溢出

            e = self.R2 - np.abs(zn)**2
            self.w += self.mu * e * np.conj(r_win)

        return {
            'z': z,
            'w_norm_traj': w_norm_traj,
            'z_amp_traj': z_amp_traj,
            'diverged': diverged,
            'diverge_idx': diverge_idx,
            'final_w_norm': self.weights_norm(),
            'init_w_norm': self._init_norm,
        }
