"""FR-21 预筛: GG-LLR vs 高斯 LLR 失配量级 (候选 (c) 译码改进方向)

目的: 在投入 MVE 前，量化"GG 湍流感知 LLR vs AWGN/高斯 LLR"的译码增益上界。
      上界 <0.5dB → 候选 (c) 在该湍流强度下不成立。同 4b#1 的 FR-21 范式。

背景 (S002/S003 待写):
  唐承茂 L1270 原文: 用 AWGN "对数似然值计算较为简单" (纯计算便利, 非高斯够好论证)
  唐承茂 L1278: 给 GG 接收信号表达式但 LLR 仍走 AWGN
  Jiang 2024 Photonics 11(1):34: dB 提升 100% 来自交织, 0% 来自 LLR 接入 GG
  → (c) 失去"同族先例背书", 本脚本用一手数值估算 (c) 真实空间

物理模型 (IM/DD + OOK + Gamma-Gamma, 同唐承茂设定):
  发送: s ∈ {0, 1} (OOK), 等概
  接收: y = η·I·s + n, I ~ GG(α,β), n ~ N(0, σ²)
  η = 光电转换效率 (取 1, 归一化, 不失一般性)
  I = 光强衰落系数, GG 分布: p(I) = 2(αβ)^((α+β)/2) / (Γ(α)Γ(β)) · I^((α+β)/2-1) · K_{α-β}(2√(αβI))

湍流强度 -> (α,β) 映射 (Andrews & Phillips 标准, 平面波 Rytov σ²_R):
  弱:  σ²_R = 0.2  -> α=11.62, β=10.02  (典型值, LogNormal 边界)
  中:  σ²_R = 1.0  -> α=4.39,  β=2.56
  强:  σ²_R = 3.5  -> α=4.39,  β=1.40  (Jiang 2024 设定)
  极强: σ²_R = 8.0 -> α=4.0,   β=1.2   (深衰落)

三种 baseline (v2 修正: 原 v1 用无 CSI 盲判决立了稻草人, 25dB 是伪信号):

  B1 无 CSI 盲高斯判决 (稻草人, 仅对照):
      L_B1(y) = (η² - 2ηy)/(2σ²), 判 s=1 若 y>η/2 (把 I 完全当地板)
      BER 地板 = P(I<0.5), 与 LLR 失配无关 -> v1 的 25dB 来自这里, 无效

  B2 理想 CSI 高斯 LLR (仿真标准, 最可能是唐承茂实际用):
      L_B2(y; Î) = (2ηÎ·y - η²Î²)/(2σ²), Î = 当前符号真实 I (仿真已知)
      物理含义: 已知当前衰落, 用已知 Î 算 LLR, 深衰落时 LLR 幅值小 (软信息弱)
      在此 baseline 下, GG-LLR 相对 B2 的增益才是 "(c) 真实空间"
      理论预期: 理想 CSI 下高斯 LLR 已接近最优, GG-LLR 增益 ≈ 0

  B3 GG-aware LLR (proposed, (c) 的真实定义):
      L_B3(y) = log( p(y|s=0) / p(y|s=1) )
              = log( N(y;0,σ²) / ∫N(y;ηI,σ²)·p_GG(I)dI )  ← 对 I 积分
      物理含义: 不知道当前 I, 但知道 GG 统计, 用边际似然
      相对 B2 (理想 CSI): B3 信息更少 (只有统计先验), 理论上 BER_B3 >= BER_B2
      相对 B1 (无 CSI): B3 信息更多 (知道 GG 分布), BER_B3 < BER_B1

关键判据 (v2 修正):
  (c) 增益 = BER_B2 (理想 CSI 高斯) - BER_B3 (GG-LLR)
  - 若 ≈ 0 dB: B2 已最优, (c) 无空间 (理想 CSI 下高斯 LLR 够好) -> KILL
  - 若 >0.5dB: B3 反而比 B2 好 (反常, 需查是否数值积分误差/方差)
  注: 正常物理是 B2 >= B3 (B2 信息更多), 若出现 B3>B2 是数值伪信号

量化方法 (oracle 上界):
  对每个 (σ²_R, SNR) 组合, MC 采样 N_mc 条 (I_k, n_k), 发 s_k:
  1. L_GG(y_k)   硬判决 BER_GG
  2. L_gauss(y_k) 硬判决 BER_gauss
  3. 互信息代理 (BPSK-AWGN 等效): 等效 SNR 损失 = ΔSNR 使得 BER_gauss(用 SNR-Δ) = BER_GG(用 SNR)
  dB 增益上界 = ΔSNR_dB

注 (上界性质):
  - 这是"无编码硬判决 BER 差"的上界。Polar+SCL 实际增益 ≤ 此值 (软信息失配在译码后会被部分吸收)
  - 但作为方向 Go/No-Go 门控, 硬判决 BER 差 <0.5dB → 软判决差更小 → 方向不成立, 这是安全上界
  - 反之硬判决 >0.5dB 不一定保证软判决 >0.5dB, 但说明物理空间存在, 值得进 MVE

TL-25 起飞检查单:
  [1] 信道/参数溯源: GG(α,β) <- Andrews & Phillips Ch 9 (σ²_R 映射表)
  [2] baseline 已定义: 高斯 LLR = 唐承茂 L1270 实际用的 (I 当确定值 1)
  [3] 理论预期: ΔSNR 随 σ²_R 单调增, 弱湍流<0.3dB / 中<0.5dB / 强>0.5dB
      —— 反向 (强湍流反而小) = 物理错误, 查
  [4] N_mc >= 1e6 (BER 低至 1e-4 需要大样本)
  [5] 输出含元数据: git hash + 时间戳 + 参数源
  [6] 上界性质显式标注
"""
import json
import math
import os
import subprocess
import time
from dataclasses import dataclass

import numpy as np
from scipy import special
from scipy.integrate import quad

# ---------- 参数溯源 ----------
PARAM_SOURCES = {
    "modulation": ("OOK (IM/DD)", "唐承茂 L1278 / Jiang 2024 式1"),
    "channel": ("Gamma-Gamma(α,β)", "Andrews & Phillips Ch 9"),
    "rytov_map": ("σ²_R → (α,β)", "Uysal 2014 综述 / Ghassemlooy 2019 表"),
    "noise": ("AWGN N(0,σ²)", "唐承茂 L1270"),
    "B1_blind": ("无 CSI 盲判决 y>η/2", "对照 (稻草人), v1 误用为 baseline"),
    "B2_ideal_csi": ("L=(2ηÎy-η²Î²)/(2σ²), Î=I", "仿真标准 (理想 CSI), 最可能是唐承茂实际用"),
    "B3_gg_aware": ("对 I 积分边际似然", "本文 proposed (c) 的真实定义"),
    "N_mc": (2_000_000, "BER 低至 1e-5 需要 >1e6 样本"),
}

# 湍流强度 -> (α, β) 映射 (Andrews & Phillips Ch 9, 平面波)
# 关键: 这些是标准表值, 不是拟合
RYTOV_TO_AB = {
    0.2:  (11.62, 10.02),   # 弱湍流 (LogNormal 边界)
    1.0:  (4.39, 2.56),     # 中湍流
    3.5:  (4.39, 1.40),     # 强湍流 (Jiang 2024 设定)
    8.0:  (4.0, 1.2),       # 极强湍流 (深衰落)
}


@dataclass
class Config:
    eta: float = 1.0           # 光电转换效率 (归一化)
    N_mc: int = 2_000_000      # MC 样本数/条件
    seed: int = 42
    # SNR 扫描范围 (dB), 覆盖星地典型工作点 + Jiang 2024 测试点
    snr_db_axis: tuple = (-5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0)
    # 湍流强度扫描
    rytov_axis: tuple = (0.2, 1.0, 3.5, 8.0)


def gg_pdf(I, alpha, beta):
    """Gamma-Gamma PDF (Andrews 式 9.27). 向量化."""
    I = np.asarray(I, dtype=float)
    # 避免除零: I=0 时 PDF=0
    out = np.zeros_like(I, dtype=float)
    mask = I > 0
    Im = I[mask]
    coef = 2.0 * (alpha * beta) ** ((alpha + beta) / 2.0) / (special.gamma(alpha) * special.gamma(beta))
    out[mask] = coef * Im ** ((alpha + beta) / 2.0 - 1.0) * special.kv(alpha - beta, 2.0 * np.sqrt(alpha * beta * Im))
    return out


def gg_mean(alpha, beta):
    """GG 均值 = 1 (归一化), 验证用."""
    return special.gamma(alpha + 1) * special.gamma(beta + 1) / (alpha * beta * special.gamma(alpha) * special.gamma(beta))


def gg_scintillation_index(alpha, beta):
    """闪烁指数 σ²_I = Var(I)/E(I)² = 1/α + 1/β + 1/(αβ)."""
    return 1.0 / alpha + 1.0 / beta + 1.0 / (alpha * beta)


def gauss_llr_blind_b1(y, sigma2, eta=1.0):
    """B1 无 CSI 盲高斯判决 (v1 误用的稻草人 baseline, 保留作对照).
    把 I 当确定值 E[I]=1. 判 s=1 若 y>η/2.
    BER 地板 = P(I<0.5), 与 LLR 失配无关.
    """
    return (eta ** 2 - 2 * eta * y) / (2 * sigma2)


def gauss_llr_ideal_csi_b2(y, I_hat, sigma2, eta=1.0):
    """B2 理想 CSI 高斯 LLR (仿真标准, 最可能是唐承茂实际用).
    已知当前衰落 Î, 用已知 Î 算 LLR. Î = 当前符号真实 I (仿真理想 CSI).
    OOK 条件 LLR (给定 Î):
      p(y|s=0,Î) = N(y;0,σ²)
      p(y|s=1,Î) = N(y;ηÎ,σ²)
      L = log(p0/p1) = [(y-ηÎ)² - y²]/(2σ²) = (η²Î² - 2ηÎy)/(2σ²)
    判 s=1 若 L<0, 即 y > ηÎ/2 (阈值随 Î 变化).
    """
    return (eta ** 2 * I_hat ** 2 - 2 * eta * I_hat * y) / (2 * sigma2)


def gg_llr_via_mc_lookup(y_grid, sigma2, alpha, beta, eta=1.0, n_I_samples=20000):
    """GG-aware LLR: L_GG(y) = log( p(y|s=0) / p(y|s=1) ).
    p(y|s=0) = N(y; 0, σ²)  (s=0 无光, I 不影响)
    p(y|s=1) = ∫ N(y; ηI, σ²) p_GG(I) dI  ← 对 I 积分

    数值方法: 用 MC 采样 I ~ GG, 算混合高斯密度作为 p(y|s=1) 的无偏估计。
    为加速, 预算 (y_grid, I_samples) 上的核密度, 再对任意 y 插值。

    返回: L_GG(y_grid) 查找表 (插值函数)。
    """
    rng = np.random.default_rng(123)
    # 采样 I ~ GG. GG 可由两个独立 Gamma 构造: I = X/Y, X~Γ(α), Y~Γ(β)
    # 但标准采样: I = G1*G2 不对. 正确: GG 采样 = gammarnd(α,1/β)... 实际用
    #   scipy 统计分布或拒绝采样。这里用 Gamma 比值法 (Andrews 附录):
    #   I = (X/α)*(Y/β) where X~Γ(α,1), Y~Γ(β,1)? 验证均值=1.
    # 更简单: 直接用 numpy gamma. GG(α,β): I 的均值=1 当参数化正确。
    X = rng.gamma(alpha, 1.0 / alpha, n_I_samples)  # E[X]=1
    Y = rng.gamma(beta, 1.0 / beta, n_I_samples)    # E[Y]=1
    I_samples = X * Y  # 均值=1, 方差=1/α+1/β+1/(αβ) ✓ (与闪烁指数一致)

    # p(y|s=1) = E_I[N(y; ηI, σ²)] ≈ (1/n) Σ N(y; ηI_k, σ²)
    # 对 y_grid 算
    sigma = math.sqrt(sigma2)
    # 广播: y_grid (Ny,1) x I_samples (1,n)
    yg = y_grid[:, None]
    Is = I_samples[None, :]
    # 高斯核
    kernels = np.exp(-0.5 * ((yg - eta * Is) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))
    p_y_s1 = kernels.mean(axis=1)  # (Ny,)
    p_y_s0 = np.exp(-0.5 * (yg[:, 0] / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))

    # L = log(p0/p1), 避免 log0
    eps = 1e-30
    L_grid = np.log(np.maximum(p_y_s0, eps) / np.maximum(p_y_s1, eps))
    return L_grid, p_y_s1, p_y_s0


def mc_ber_for_condition(alpha, beta, snr_lin, cfg, n_I_for_lookup=20000, y_grid_n=2000):
    """给定 (α,β,SNR), MC 估计三种 LLR 的硬判决 BER。
    SNR 定义: 平均 SNR = η²·E[I²]/σ² = η²·(1+σ²_I)/σ² (I 归一化均值=1)
    => σ² = η²·(1+σ²_I)/SNR

    返回 (ber_B1_blind, ber_B2_ideal_csi, ber_B3_gg_aware, sigma2_I, sigma2)
    """
    sigma2_I = gg_scintillation_index(alpha, beta)
    sigma2 = cfg.eta ** 2 * (1.0 + sigma2_I) / snr_lin  # 噪声方差

    # 采样 y: s, I, n
    rng = np.random.default_rng(cfg.seed)
    s = rng.integers(0, 2, cfg.N_mc)  # 0/1 等概
    # I ~ GG via Gamma 比值
    X = rng.gamma(alpha, 1.0 / alpha, cfg.N_mc)
    Y = rng.gamma(beta, 1.0 / beta, cfg.N_mc)
    I = X * Y
    n = rng.normal(0, math.sqrt(sigma2), cfg.N_mc)
    y = cfg.eta * I * s + n

    # --- B1 无 CSI 盲判决 (对照): y > eta/2 ---
    s_hat_b1 = (y > cfg.eta / 2.0).astype(int)
    ber_b1 = float(np.mean(s_hat_b1 != s))

    # --- B2 理想 CSI 高斯 LLR (仿真标准 baseline): y > eta*I/2 ---
    # 判 s=1 若 L<0 即 y > eta*Î/2, Î=I (仿真理想 CSI)
    s_hat_b2 = (y > cfg.eta * I / 2.0).astype(int)
    ber_b2 = float(np.mean(s_hat_b2 != s))

    # --- B3 GG-aware LLR (proposed (c)): 对 I 积分, 查找表 ---
    y_min, y_max = float(np.percentile(y, 0.1)), float(np.percentile(y, 99.9))
    y_grid = np.linspace(max(y_min, -3 * math.sqrt(sigma2)), y_max + 1, y_grid_n)
    L_grid, _, _ = gg_llr_via_mc_lookup(y_grid, sigma2, alpha, beta, cfg.eta, n_I_for_lookup)
    L_at_y = np.interp(y, y_grid, L_grid)
    s_hat_b3 = (L_at_y < 0).astype(int)
    ber_b3 = float(np.mean(s_hat_b3 != s))

    return ber_b1, ber_b2, ber_b3, sigma2_I, sigma2


def gain_db_from_ber(ber_proposed, ber_baseline):
    """proposed (GG-LLR) 相对 baseline (高斯 LLR) 的 BER 增益 (dB)。
    gain = 10*log10(ber_baseline / ber_proposed). 正数=proposed 更好。
    """
    if ber_proposed <= 0 or ber_baseline <= 0:
        return float('inf') if ber_proposed < ber_baseline else 0.0
    return 10.0 * math.log10(ber_baseline / ber_proposed)


def main():
    cfg = Config()

    # 元数据
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.getcwd()).decode().strip()
    except Exception:
        git_hash = "unknown"

    results = {}
    print("=" * 78)
    print("FR-21 预筛 v2: (c) GG-LLR vs 理想 CSI 高斯 LLR 失配 (修正 v1 稻草人)")
    print("=" * 78)
    print(f"MC N={cfg.N_mc}/条件, 调制=OOK(IM/DD), 信道=Gamma-Gamma")
    print(f"B1 = 无 CSI 盲判决 (对照, v1 误用为 baseline -> 25dB 伪信号来源)")
    print(f"B2 = 理想 CSI 高斯 LLR (仿真标准 baseline, 最可能是唐承茂实际用)")
    print(f"B3 = GG-aware LLR (proposed (c), 对 I 积分)")
    print(f"(c) 真实增益 = B2 vs B3. 正常物理: BER_B2 <= BER_B3 (B2 信息更多)")
    print()

    for rytov in cfg.rytov_axis:
        alpha, beta = RYTOV_TO_AB[rytov]
        sigma2_I = gg_scintillation_index(alpha, beta)
        print(f"--- σ²_R = {rytov}  (α={alpha}, β={beta}, 闪烁指数 σ²_I={sigma2_I:.3f}) ---")
        per_rytov = {
            "alpha": alpha, "beta": beta, "sigma2_I": sigma2_I,
            "snr_axis_db": list(cfg.snr_db_axis),
            "ber_B1_blind": [], "ber_B2_ideal_csi": [], "ber_B3_gg_aware": [],
            "gain_c_vs_B2_db": [],  # (c) = B3 相对 B2 (负=B3 更差, 正常)
            "gain_B3_vs_B1_db": [],  # 对照: B3 相对 B1 (应正, 体现统计先验价值)
        }
        for snr_db in cfg.snr_db_axis:
            snr_lin = 10.0 ** (snr_db / 10.0)
            ber_b1, ber_b2, ber_b3, _, _ = mc_ber_for_condition(alpha, beta, snr_lin, cfg)
            # (c) 增益 = B3 相对 B2: gain = 10*log10(BER_B2/BER_B3). 正常<=0 (B3 更差)
            g_c = gain_db_from_ber(ber_b3, ber_b2)  # proposed=B3, baseline=B2
            # 对照 B3 vs B1
            g_b3_b1 = gain_db_from_ber(ber_b3, ber_b1)
            per_rytov["ber_B1_blind"].append(ber_b1)
            per_rytov["ber_B2_ideal_csi"].append(ber_b2)
            per_rytov["ber_B3_gg_aware"].append(ber_b3)
            per_rytov["gain_c_vs_B2_db"].append(g_c)
            per_rytov["gain_B3_vs_B1_db"].append(g_b3_b1)
            flag_c = "  ⚠反常" if g_c > 0.5 else ""
            print(f"  SNR={snr_db:+5.1f}dB  B1={ber_b1:.3e}  B2={ber_b2:.3e}  B3={ber_b3:.3e}"
                  f"  | (c)B3vsB2={g_c:+.3f}dB  B3vsB1={g_b3_b1:+.3f}dB{flag_c}")
        # 工作区峰值 (B2 BER 在 1e-5~1e-1)
        ber_b2_arr = np.array(per_rytov["ber_B2_ideal_csi"])
        work_mask = (ber_b2_arr > 1e-5) & (ber_b2_arr < 1e-1)
        g_c_arr = np.array(per_rytov["gain_c_vs_B2_db"])
        if work_mask.any():
            peak_c = float(g_c_arr[work_mask].max())
        else:
            peak_c = float(g_c_arr.max())
        per_rytov["peak_c_gain_in_work_region_db"] = peak_c
        print(f"  → 工作区 (c) 峰值增益 (B3 vs B2): {peak_c:+.3f} dB"
              f"  {'(反常: B3>B2, 查数值)' if peak_c > 0.5 else '(B2 已更优或持平, 符合物理)'}")
        print()
        results[f"rytov_{rytov}"] = per_rytov

    # 星地 LEO 场景对应哪个 σ²_R? (4b#1 V001 确认的星地等效 Cn2)
    # 4b#1: 星地仰角 20-90°, 等效 Cn2 7.5e-17~5.4e-16 (~1 数量级)
    # Rytov σ²_R = 1.23·Cn2·k^(7/6)·L^(11/6), L=H_atm/sin(elev)=20km/sin(20°)=58km ~ 20km/sin(90°)=20km
    # k=2π/λ=4.05e6, λ=1.55e-6
    # σ²_R @ elev=90° (L=20km, Cn2=7.5e-17): 1.23*7.5e-17*(4.05e6)^(7/6)*(20e3)^(11/6)
    #   ≈ 1.23*7.5e-17 * 1.5e7 * 1.4e9 ≈ ... 数量级 ~0.01-0.1 (弱湍流)
    # σ²_R @ elev=20° (L=58km, Cn2=5.4e-16): ~0.1-0.5 (弱-中)
    # => 星地 LEO 常规仰角 = 弱到中湍流, σ²_R < 1
    print("=" * 78)
    print("星地 LEO 场景对照 (4b#1 V001 物理天花板自洽性检查)")
    print("=" * 78)
    lam = 1.55e-6
    k = 2 * math.pi / lam
    H_atm = 20e3
    Cn2_star_range = [7.5e-17, 5.4e-16]
    for elev_deg in [20, 45, 90]:
        L = H_atm / math.sin(math.radians(elev_deg))
        # 用中值 Cn2 估 σ²_R
        for cn2, label in [(Cn2_star_range[0], "弱端"), (Cn2_star_range[1], "强端")]:
            sigma_R2 = 1.23 * cn2 * k ** (7.0 / 6.0) * L ** (11.0 / 6.0)
            print(f"  elev={elev_deg}° Cn2={cn2:.1e} ({label}): σ²_R ≈ {sigma_R2:.3f}")
    print("  => 星地 LEO 常规仰角 σ²_R < 1 (弱-中湍流), 对应本脚本 rytov=0.2/1.0 行")

    # 综合 FR-21 判定 (v2)
    print()
    print("=" * 78)
    print("FR-21 门控结论 v2 (候选 (c) GG-LLR vs 理想 CSI 高斯 LLR)")
    print("=" * 78)
    print("各湍流强度下 (c) 工作区峰值增益 (B3 GG-aware vs B2 理想 CSI):")
    for rytov in cfg.rytov_axis:
        pk = results[f"rytov_{rytov}"]["peak_c_gain_in_work_region_db"]
        verdict = "✓ >0.5dB (反常, 查数值)" if pk > 0.5 else "✗ <=0.5dB (B2 已更优或持平)"
        print(f"  σ²_R={rytov:<4}  (c) 峰值 {pk:+.3f} dB  {verdict}")
    print()
    star_ground_peak = max(results["rytov_0.2"]["peak_c_gain_in_work_region_db"],
                           results["rytov_1.0"]["peak_c_gain_in_work_region_db"])
    print(f"星地常规仰角 (σ²_R<1) 最乐观 (c) 峰值增益: {star_ground_peak:+.3f} dB")
    if star_ground_peak <= 0.5:
        print(f"  ✅ 物理自洽: 理想 CSI 下高斯 LLR 已最优, GG-LLR (B3) 不比 B2 好")
        print(f"     -> (c) 在'理想 CSI' baseline 假设下无 BER 增益空间")
        print(f"     -> 但这依赖 baseline 是 B2 (理想 CSI) 的假设")
        print(f"     -> 若唐承茂实际是 B1 (无 CSI), (c) 有空间但那是统计先验价值非 LLR 失配")
        print(f"     -> 需查唐承茂 PDF 原图确认 CSI 假设 (S003 待办)")
    else:
        print(f"  ⚠ 反常: B3>B2 在理想 CSI 下不应发生, 查 MC 方差 / LLR 查找表精度")

    out = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "git_hash": git_hash,
        "param_sources": PARAM_SOURCES,
        "config": {"eta": cfg.eta, "N_mc": cfg.N_mc, "seed": cfg.seed,
                   "snr_db_axis": list(cfg.snr_db_axis), "rytov_axis": list(cfg.rytov_axis)},
        "rytov_to_ab": {str(k): list(v) for k, v in RYTOV_TO_AB.items()},
        "model_assumption": {
            "version": "v2 (修正 v1 稻草人: v1 用 B1 无 CSI 当 baseline, 25dB 伪信号)",
            "modulation": "OOK IM/DD",
            "channel": "Gamma-Gamma(α,β)",
            "B1_blind": "无 CSI, y>η/2 判决 (对照, 地板=P(I<0.5))",
            "B2_ideal_csi": "理想 CSI, L=(2ηÎy-η²Î²)/(2σ²), Î=I (仿真标准)",
            "B3_gg_aware": "GG-aware, 对 I 积分边际似然 (proposed (c))",
            "c_gain_definition": "10·log10(BER_B2/BER_B3), 正常<=0 (B2 信息更多)",
            "upper_bound_nature": "硬判决 BER 差是软判决译码增益的代理",
        },
        "results_per_rytov": results,
        "fr21_verdict_v2": {
            "starground_routine_c_peak_db": float(star_ground_peak),
            "c_dead_under_ideal_csi_baseline": star_ground_peak <= 0.5,
            "c_dead_under_blind_baseline": False,  # v1 已证 B1 下 (c) 有大空间 (稻草人)
            "pending_check": "需查唐承茂 PDF 原图确认 CSI 假设 (B1 or B2)",
        },
    }
    out_path = os.path.join(os.path.dirname(__file__), "fr21_gg_llr_vs_gauss_llr_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n结果已存: {out_path}")


if __name__ == "__main__":
    main()
