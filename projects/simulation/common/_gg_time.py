"""GG 时间域衰落模型：块间 AR(1) 相关的 Gamma-Gamma 包络生成器。

> 方向: Q-CMA-FADE (Step A, FR-20 前置门控) | 状态: WIP | 创建: 2026-07-11
> 组织规范: ../SIM-ORG.md (P4 只扩不改；新算法=1新文件+0改动现有)

补 ``_channel.gg_block`` 的缺口: ``gg_block`` 块间独立(无时间动力学)，本模块
生成**块间有相干时间 τ_c 控制的连续演化**的 GG 包络——块内恒定物理成立
(τ_c ≫ 符号周期)，块间用 AR(1) 相关。

物理依据(FR-20, 全标来源):
  - f_G 公式: Greenwood 1977 JOSA 67(3):390-393 + Andrews&Phillips 2005
  - τ_c = 1/(2π·f_G): Conan 1995 JOSA A 12(7):1559 (强度闪烁相干时间)
  - τ_c 典型 1-100 ms: sat.1553:167 (>1ms) + s24248036:872 (1-100ms)
  - 强度谱高频 f⁻¹¹ᐟ³: Tatarskii 1971 / Clifford 1971 / Ishimaru 1972

建模方法:
  GG 包络 h = X · Y, X~Gamma(α,1/α) 大尺度, Y~Gamma(β,1/β) 小尺度。
  两种 AR(1) 实现:
    - 'gar' (默认, 边缘精确): 标准正态 AR(1) + quantile matching 映射到精确
      Gamma 边缘(KS<0.006 全湍流档); log-ACF 略低于 ρ(高 ρ 区 <2% 偏差)。
    - 'lognormal' (log-ACF 精确): 对 log(X), log(Y) 各做平稳 AR(1),
      对数域 ACF[lag=1] = ρ 精确(匹配 Kolmogorov f⁻¹¹ᐟ³ 滚降 + Conan τ_c);
      边缘近似 Gamma(对数正态矩匹配, 强湍 β<1 偏差大 KS~0.15)。

  ρ = exp(-Δt/τ_c), Δt = block·t_s (块时长)。
  注: τ_c ≫ block·t_s 时 ρ→1, 单帧内近似准静态(sat.1553 L167 物理一致);
  时间动力学在跨多帧(≫τ_c)序列才显现。
"""
import numpy as np
from scipy.stats import gamma as gamma_dist, norm

from ._config import BLOCK


# ─── AR(1) 块间相关系数 ─────────────────────────────────────

def rho_from_tau_c(tau_c, block=BLOCK, t_s=1.0 / 2.5e9):
    """块间 AR(1) 相关系数 ρ = exp(-Δt/τ_c)。

    Δt = block·t_s 是块时长(块内符号数 × 符号周期)。
    ρ→1: τ_c 大(慢变) → 连续块高度相关;
    ρ→0: τ_c 小(快变) → 连续块近似独立(退化为 gg_block)。
    """
    dt = block * t_s
    return float(np.exp(-dt / tau_c))


# ─── Gamma 边缘参数 ─────────────────────────────────────────

def _gamma_lognormal_params(a):
    """Gamma(a, scale=1/a) [均值1] 的对数正态近似参数 (μ_ln, σ_ln)。

    矩匹配: E[X]=1, Var[X]=1/a → LogNormal(μ,σ²):
      σ²_ln = ln(1 + 1/a),  μ_ln = -σ²_ln/2  (使 E[X]=exp(μ+σ²/2)=1)
    """
    var = 1.0 / a
    sigma2 = np.log(1.0 + var)
    mu = -sigma2 / 2.0
    return mu, np.sqrt(sigma2)


# ─── AR(1) 实现 (向量化) ────────────────────────────────────

def _ar1_lognormal(n_blocks, a, rho, rng):
    """对数域平稳 AR(1), 边缘近似 Gamma(a, 1/a) [均值1].

    标准平稳 AR(1): x[k] = ρ·x[k-1] + ε[k]
      稳态: E[x]=E[ε]/(1-ρ),  Var[x]=Var[ε]/(1-ρ²)
    要稳态 N(μ_ln, σ²_ln) → E[ε]=μ_ln·(1-ρ), Var[ε]=σ²_ln·(1-ρ²)。
    对数域 ACF[lag]=ρ^lag 精确(验证: ρ=0.5→log ACF[1]=0.5016)。
    """
    mu_ln, sigma_ln = _gamma_lognormal_params(a)
    # 平稳初始化
    x0 = mu_ln + sigma_ln * rng.standard_normal()
    eps_mean = mu_ln * (1.0 - rho)
    eps = eps_mean + np.sqrt(sigma_ln ** 2 * (1.0 - rho ** 2)) * rng.standard_normal(n_blocks)
    # 向量化递推 (rho<1 收敛; rho→1 时 eps→eps_mean, 序列近常数=物理准静态)
    log_x = np.empty(n_blocks)
    x = x0
    for k in range(n_blocks):
        x = rho * x + eps[k]
        log_x[k] = x
    return np.exp(log_x)


def _gamma_ar1_exact(n_blocks, a, rho, rng):
    """精确 Gamma 边缘 AR(1) — 标准正态 AR(1) + quantile matching。

    z[k]=ρ·z[k-1]+√(1-ρ²)·η[k], η~N(0,1), z 稳态 N(0,1);
    X = Gamma.ppf(Φ(z), a, 1/a) → 边缘精确 Gamma(a,1/a)。
    log-ACF 略低于 ρ(非线性分位数畸变, 高 ρ<2% 偏差)。
    """
    z0 = rng.standard_normal()
    eta = np.sqrt(1.0 - rho ** 2) * rng.standard_normal(n_blocks)
    z = np.empty(n_blocks)
    cur = z0
    for k in range(n_blocks):
        cur = rho * cur + eta[k]
        z[k] = cur
    u = norm.cdf(z)
    return gamma_dist.ppf(u, a, scale=1.0 / a)


# ─── 主接口: 时间相关 GG 包络 ───────────────────────────────

def gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=1.0 / 2.5e9,
                     method='gar', seed=None):
    """时间相关 Gamma-Gamma 衰落包络(块内恒定, 块间 AR(1) 相关)。

    参数
    ----
    N : int
        总符号数。
    alpha, beta : float
        GG 大/小尺度形状参数(与 ``gg_block`` 同约定, 均值=1)。
    tau_c : float
        强度闪烁相干时间(秒)。τ_c=1/(2π·f_G)(Conan 1995)。
    block : int
        块内符号数(块内 h 恒定), 默认 ``BLOCK``。
    t_s : float
        符号周期(秒), 默认 1/2.5e9。
    method : {'lognormal', 'gar'}
        'gar'(默认): 精确 Gamma 边缘(KS<0.006 全湍流档), log-ACF 略低于 ρ(<2%);
        'lognormal': 对数域 AR(1) log-ACF=ρ 精确, 边缘近似(强湍偏差大 KS~0.15)。
    seed : int or None
        随机种子。

    返回
    ----
    h : ndarray, shape (N,)
        时间相关 GG 包络, 块内恒定, 块间 AR(1) 相关(ρ=exp(-block·t_s/τ_c))。
        边缘分布近似 Gamma-Gamma(α,β) [均值1]。

    物理约定
    --------
    - 块内恒定: τ_c ≫ block·t_s 时物理成立(sat.1553 L167 准静态假设)。
    - 块间 AR(1): ρ=exp(-Δt/τ_c), Δt=block·t_s。
    - GG = 大尺度 X · 小尺度 Y, X/Y 各自独立 AR(1)。
    - τ_c ≫ 符号周期 → 单帧(≪τ_c)内序列近似常数; 需序列长 ≫ τ_c/t_s
      才能看到完整衰落动力学。
    """
    rng = np.random.default_rng(seed)
    n_blocks = (N + block - 1) // block
    rho = rho_from_tau_c(tau_c, block, t_s)

    if method == 'lognormal':
        big = _ar1_lognormal(n_blocks, alpha, rho, rng)
        small = _ar1_lognormal(n_blocks, beta, rho, rng)
    elif method == 'gar':
        big = _gamma_ar1_exact(n_blocks, alpha, rho, rng)
        small = _gamma_ar1_exact(n_blocks, beta, rho, rng)
    else:
        raise ValueError(f"method must be 'lognormal' or 'gar', got {method!r}")

    h_blocks = big * small  # GG = 大尺度 × 小尺度, 均值≈1
    h = np.repeat(h_blocks, block)[:N]
    return h


def gg_time_envelope_blockwise(n_blocks, alpha, beta, tau_c, block=BLOCK,
                               t_s=1.0 / 2.5e9, method='gar', seed=None):
    """块级时间相关 GG 包络(返回 n_blocks 个块值, 不展开)。

    供需要块级序列(非逐符号)的分析用, 如 CMA 发散扫描按块评估。
    """
    rng = np.random.default_rng(seed)
    rho = rho_from_tau_c(tau_c, block, t_s)

    if method == 'lognormal':
        big = _ar1_lognormal(n_blocks, alpha, rho, rng)
        small = _ar1_lognormal(n_blocks, beta, rho, rng)
    elif method == 'gar':
        big = _gamma_ar1_exact(n_blocks, alpha, rho, rng)
        small = _gamma_ar1_exact(n_blocks, beta, rho, rng)
    else:
        raise ValueError(f"method must be 'lognormal' or 'gar', got {method!r}")

    return big * small


# ─── GG PDF 理论(验证用) ────────────────────────────────────

def gg_pdf_theory(I, alpha, beta, I_bar=1.0):
    """Gamma-Gamma 强度 PDF 理论值(验证边缘分布用)。

    f(I) = 2(αβ)^((α+β)/2) / (Γ(α)Γ(β)·Ī) · (I/Ī)^((α+β)/2-1) · K_{α-β}(2√(αβ·I/Ī))
    (formulas-master F32)
    """
    from scipy.special import gamma as gamma_func, kv
    ab = alpha * beta
    exponent = (alpha + beta) / 2.0 - 1.0
    coeff = 2.0 * ab ** ((alpha + beta) / 2.0) / (gamma_func(alpha) * gamma_func(beta) * I_bar)
    x = I / I_bar
    return coeff * x ** exponent * kv(abs(alpha - beta), 2.0 * np.sqrt(ab * x))
