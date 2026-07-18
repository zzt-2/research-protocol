"""验证 BMD rate 估计器: 三法交叉对照 (后验积分 / LLR熵 / Y分箱).

背景: 调试期发现 LLR 熵法 log2(1+exp(-|L|)) 对 uniform 系统偏高 ~1bit (OVER-SHANNON).
本脚本用三种独立方法估同一 BMD rate, 对照 Shannon 上界 log2(1+SNR) (复 AWGN).
结论: 后验积分法对照 Shannon 最合理 (uniform@0dB≈0.9<1.0), 已采纳为 bmd_air 实现.

注: 目录名 n1-pcs-gain 含连字符, 非合法 Python 包名, 故用 importlib 加载主模块.
运行: cd 本目录 && wsl ~/.venvs/torch/bin/python _validate_estimator.py
"""
import os
import importlib.util

import numpy as np

_d = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("mve", os.path.join(_d, "n1_pcs_gain_mve.py"))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)
CONST, LABELS, mb_pmf_16qam, bmd_air = (
    m.CONST, m.LABELS, m.mb_pmf_16qam, m.bmd_air)

UNI = mb_pmf_16qam(0.0)
rng = np.random.default_rng(1)
N = 100000


def method2_binning(y, idx, n_bins=32):
    """法2: Y 幅度分箱估 I(b_k;Y). 粗糙 (只用 |Y|), 仅作独立参照."""
    R = np.abs(y)
    air = 0.0
    for k in range(4):
        bk = LABELS[idx, k]
        edges = np.quantile(R, np.linspace(0, 1, n_bins + 1))
        binned = np.digitize(R, edges[1:-1])
        cond_h = 0.0
        for b in range(n_bins):
            mask = binned == b
            if mask.sum() < 5:
                continue
            p0 = np.clip(np.mean(bk[mask] == 0), 1e-6, 1 - 1e-6)
            cond_h += (-(p0 * np.log2(p0) + (1 - p0) * np.log2(1 - p0))) * (mask.sum() / len(bk))
        air += (1.0 - cond_h)  # uniform H(b_k)=1
    return air


def method3_analytic_mc(sigma2, pmf=UNI):
    """法3 (= 主脚本 bmd_air 用的后验积分法): 从 p(y) 采样, 后验聚合估 H(b_k|Y).
    此处独立实现一遍, 与主脚本 bmd_air 交叉验证实现一致性."""
    rng3 = np.random.default_rng(42)
    xs = rng3.choice(16, N, p=pmf)
    tx = CONST[xs]
    nn = np.sqrt(sigma2 / 2) * (rng3.standard_normal(N) + 1j * rng3.standard_normal(N))
    y = tx + nn
    resid = y[:, None] - CONST[None, :]
    log_lik = -(np.abs(resid) ** 2) / sigma2 + np.log(pmf + 1e-300)[None, :]
    mx = np.max(log_lik, axis=1, keepdims=True)
    logZ = mx[:, 0] + np.log(np.sum(np.exp(log_lik - mx), axis=1))
    post = np.exp(log_lik - logZ[:, None])
    air = 0.0
    for k in range(4):
        bit_k = LABELS[:, k]
        p0p = np.clip(np.sum(post[:, bit_k == 0], axis=1), 1e-12, 1 - 1e-12)
        cond_h = np.mean(-(p0p * np.log2(p0p) + (1 - p0p) * np.log2(1 - p0p)))
        p0m = np.clip(np.mean(bit_k[xs] == 0), 1e-6, 1 - 1e-6)
        h_marg = -(p0m * np.log2(p0m) + (1 - p0m) * np.log2(1 - p0m))
        air += (h_marg - cond_h)
    return air


print("=== 三法对照: AWGN uniform 16-QAM BMD rate (Shannon 复 AWGN = log2(1+SNR)) ===")
print(f"{'SNR':>4} {'bmd_air(主)':>11} {'Y分箱':>8} {'解析MC':>8} {'Shannon':>8}")
for gdb in [0, 4, 8, 12]:
    gamma = 10 ** (gdb / 10)
    sigma2 = 1.0 / gamma
    idx = rng.integers(0, 16, N)
    tx = CONST[idx]
    nn = np.sqrt(sigma2 / 2) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    y = tx + nn
    a1 = bmd_air(y, np.ones(N), np.full(N, sigma2), idx, UNI)
    a2 = method2_binning(y, idx)
    a3 = method3_analytic_mc(sigma2)
    sh = np.log2(1 + gamma)
    print(f"{gdb:>3}dB {a1:>11.3f} {a2:>8.3f} {a3:>8.3f} {sh:>8.3f}")

print("\n=== MB vs uniform (后验积分法, 采纳的估计器) ===")
print(f"{'SNR':>4} {'nu':>5} {'AIR':>8}")
for gdb in [0, 10]:
    gamma = 10 ** (gdb / 10)
    sigma2 = 1.0 / gamma
    for nu in [0.0, 0.2, 0.5]:
        pmf = mb_pmf_16qam(nu)
        idx = rng.choice(16, N, p=pmf)
        tx = CONST[idx]
        nn = np.sqrt(sigma2 / 2) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
        y = tx + nn
        a = bmd_air(y, np.ones(N), np.full(N, sigma2), idx, pmf)
        print(f"{gdb:>3}dB {nu:>5.2f} {a:>8.3f}")
print("结论: MB 全 SNR < uniform (nu=0). 16-QAM 整形空间不足, 验证 MVE FAIL 根因.")
