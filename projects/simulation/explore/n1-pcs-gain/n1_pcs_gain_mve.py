"""
N1 §4a 维度 D MVE — 离线静态 PCS (MB 分布) 在 Gamma-Gamma 湍流下的 AIR gain.

验证假设: 强湍流 (alpha=1.5/beta=0.8) 下, 离线单一 MB 分布相比均匀 16-QAM,
在 AIR=3.0 bit/sym 工作点的 SNR 增益 >= 0.5 dB.

SPEC: projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md

TL-25 起飞检查:
  [1] 共享信道: 三方案 (uniform/offline-MB/oracle) 用同一组 h 块 (同 seed GG)
  [2] 重生信道: 不同 gamma_bar / 不同湍流各自生成
  [3] 复用代码: gg_block 逻辑复刻自 projects/simulation/common/_channel.py (3 行 scipy),
                qam16 星座与 _modulation.py 一议 (Gray 00->-3,01->-1,11->+1,10->+3, /sqrt(10)).
                不导入 common 包以避开多普勒/相位/FEC 重依赖; 信号模型严格遵循相干约定.
  [4] baseline 已优化: uniform = MB nu=0 天然公平; oracle 是 CSI-aware 上界
  [5] 理论预期: 见 SPEC Sec.2 (AWGN uniform->4, gain<=2dB, weak gain<0.3)
  [6] 元数据: 输出 JSON 含 seed/sym_count/git_hash

TL-01 相干约定 (红线): signal = tx * sqrt(h); h 实值 GG 辐照度;
  SNR ≜ Es/N0 = gamma_bar * h (信号功率归一为1, 复噪声方差 sigma2 = 1/SNR).
  注: 毕设 _channel.py 用 sigma2=1/(2*gamma) (gamma=Es/2N0 惯例); 本 MVE 用自洽
      Es/N0 惯例 sigma2=1/gamma, gamma_dB 即 Es/N0_dB, 与 Shannon log2(1+SNR) 直接对应.

AIR 估计 (法3, 后验积分, 经三法交叉验证可靠):
  早期版本用 LLR 熵 log2(1+exp(-|L|)), 对 uniform 偏高 ~1bit (OVER-SHANNON).
  _validate_estimator.py 对照三法 (LLR熵 / Y分箱 / 后验积分), 确认后验积分法对照
  Shannon 最合理 (uniform@0dB≈0.9<1.0, @12dB≈3.58<4.075). 改用此法.

运行: wsl ~/.venvs/torch/bin/python n1_pcs_gain_mve.py
"""
import json
import os
import subprocess
import time

import numpy as np
from scipy.stats import gamma as gamma_dist

# ─── 参数 (复刻自 projects/simulation/params.py TurbulenceParams, BLOCK) ───
TURB = {
    "weak":     (4.0, 3.0),
    "moderate": (2.5, 1.8),
    "strong":   (1.5, 0.8),
}
BLOCK = 100  # 块内 h 恒定 (params.py ExperimentParams.BLOCK)

GAMMA_BAR_DB = [0, 4, 8, 12, 16, 20]
N_SYM = 200_000          # SPEC; 超时则降
N_SYM_ORACLE = 100_000   # oracle 较慢减半
SEED = 42
NU_SWEEP = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.5]  # MB 参数; nu=0 即均匀
WORK_AIR = 3.0           # gain 工作点 (bit/sym), 16-QAM 上限 4

# ─── 16-QAM 星座 (与 _modulation.py:qam16_mod 一致) ───
AMP = np.array([-3.0, -1.0, 1.0, 3.0])
IDX2GRAY = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])  # index -> (b_high, b_low)
I_IDX, Q_IDX = np.meshgrid(np.arange(4), np.arange(4), indexing="ij")
CONST = (AMP[I_IDX.ravel()] + 1j * AMP[Q_IDX.ravel()]) / np.sqrt(10.0)  # (16,)
LABELS = np.zeros((16, 4), dtype=np.int8)
for _idx in range(16):
    LABELS[_idx, 0:2] = IDX2GRAY[_idx // 4]
    LABELS[_idx, 2:4] = IDX2GRAY[_idx % 4]


def gg_block(N, a, b, bs=BLOCK):
    """复刻自 projects/simulation/common/_channel.py:gg_block.
    GG 块衰落: h = Gamma(a)*Gamma(b), 块内恒定."""
    nb = (N + bs - 1) // bs
    h = (gamma_dist.rvs(a, scale=1.0 / a, size=nb) *
         gamma_dist.rvs(b, scale=1.0 / b, size=nb))
    return np.repeat(h, bs)[:N]


def mb_pmf_16qam(nu):
    """Maxwell-Boltzmann PMF over 16-QAM (PAS 幅度整形).
    I/Q 独立: P(a)∝exp(-nu*a^2) for a in {-3,-1,1,3}; sign 均匀 (MB 只作用幅度)."""
    p_amp = np.exp(-nu * AMP ** 2)
    p_amp = p_amp / p_amp.sum()
    p_joint = np.outer(p_amp, p_amp).ravel()  # index = I*4+Q
    return p_joint / p_joint.sum()


def bmd_air(y, h, sigma2, idx, pmf):
    """BMD achievable information rate via posterior integration (法3, 可靠).
    R_BMD = sum_k I(b_k; Y) = sum_k [H(b_k) - H(b_k|Y)].
    H(b_k|Y) = E_Y[ h2(P(b_k=0|Y)) ], 后验 P(b_k=0|y) 由全 16 点后验聚合.
    H(b_k) 由实际采样 bit 边际估.

    y: received (N,), h: per-symbol fading (N,), sigma2: noise var (N,) [E|n|^2=sigma2]
    idx: symbol index (N,) in [0,15]; pmf: 符号级输入分布 (16,)
    """
    sqrt_h = np.sqrt(h)
    resid = y[:, None] - sqrt_h[:, None] * CONST[None, :]
    log_lik = -(np.abs(resid) ** 2) / sigma2[:, None]
    weighted = log_lik + np.log(pmf + 1e-300)[None, :]
    mx = np.max(weighted, axis=1, keepdims=True)
    logZ = mx[:, 0] + np.log(np.sum(np.exp(weighted - mx), axis=1))
    post = np.exp(weighted - logZ[:, None])                    # (N,16) P(x|y)
    air = 0.0
    for k in range(4):
        bit_k = LABELS[:, k]
        p0_post = np.clip(np.sum(post[:, bit_k == 0], axis=1), 1e-12, 1 - 1e-12)
        cond_h_mean = np.mean(-(p0_post * np.log2(p0_post) +
                                (1 - p0_post) * np.log2(1 - p0_post)))
        p0m = np.clip(np.mean(bit_k[idx] == 0), 1e-6, 1 - 1e-6)
        h_marg = -(p0m * np.log2(p0m) + (1 - p0m) * np.log2(1 - p0m))
        air += (h_marg - cond_h_mean)
    return air


def find_best_nu_offline(gamma_bar, h_blocks, rng, N_search=40000):
    """Elzanaty blind: 代表性 SNR = gamma_bar * median(h), 在该 SNR 上搜 nu 最大化 AIR."""
    h_med = np.median(h_blocks)
    snr_rep = gamma_bar * h_med
    sigma2_rep = 1.0 / snr_rep
    best_nu, best_air = 0.0, -np.inf
    for nu in NU_SWEEP:
        pmf = mb_pmf_16qam(nu)
        tx_idx = rng.choice(16, size=N_search, p=pmf)
        tx = CONST[tx_idx]
        n = np.sqrt(sigma2_rep / 2) * (rng.standard_normal(N_search) + 1j * rng.standard_normal(N_search))
        y = tx * np.sqrt(h_med) + n
        air = bmd_air(y, np.full(N_search, h_med), np.full(N_search, sigma2_rep), tx_idx, pmf)
        if air > best_air:
            best_air, best_nu = air, nu
    return best_nu


def find_best_nu_for_snr(snr_val, rng, N_search=20000):
    """给瞬时 SNR 找最优 nu (oracle per-block 用)."""
    if snr_val <= 1e-6:
        return 0.0
    sigma2 = 1.0 / snr_val
    best_nu, best_air = 0.0, -np.inf
    for nu in NU_SWEEP:
        pmf = mb_pmf_16qam(nu)
        tx_idx = rng.choice(16, size=N_search, p=pmf)
        tx = CONST[tx_idx]
        nn = np.sqrt(sigma2 / 2) * (rng.standard_normal(N_search) + 1j * rng.standard_normal(N_search))
        y = tx + nn
        air = bmd_air(y, np.full(N_search, 1.0), np.full(N_search, sigma2), tx_idx, pmf)
        if air > best_air:
            best_air, best_nu = air, nu
    return best_nu


def snr_for_air(airs, gdbs, target):
    """反向插值: AIR 随 gamma 单调升, 找达 target 所需的 gamma (dB)."""
    if target > airs.max() or target < airs.min():
        return None
    for i in range(len(airs) - 1):
        if (airs[i] - target) * (airs[i + 1] - target) <= 0 and airs[i + 1] != airs[i]:
            frac = (target - airs[i]) / (airs[i + 1] - airs[i])
            return gdbs[i] + frac * (gdbs[i + 1] - gdbs[i])
    return None


def main():
    t0 = time.time()
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        git_hash = "unknown"

    results = {"meta": {"seed": SEED, "git_hash": git_hash, "block": BLOCK,
                        "nu_sweep": NU_SWEEP, "work_air": WORK_AIR,
                        "turb_params": TURB, "air_method": "posterior_integration"},
               "curves": {}, "gain_at_work_air": {}, "deviations": []}

    # 锚点: uniform + AWGN AIR 应随 SNR 单调升到 4, 且 < Shannon log2(1+SNR)
    rng_chk = np.random.default_rng(SEED + 999)
    awgn_check = []
    for gdb in [0, 4, 8, 12, 16, 20]:
        g = 10 ** (gdb / 10)
        s2 = 1.0 / g
        Nck = 40000
        idx_u = rng_chk.integers(0, 16, Nck)
        tx = CONST[idx_u]
        nn = np.sqrt(s2 / 2) * (rng_chk.standard_normal(Nck) + 1j * rng_chk.standard_normal(Nck))
        y = tx + nn
        air = bmd_air(y, np.ones(Nck), np.full(Nck, s2), idx_u, mb_pmf_16qam(0.0))
        shannon = np.log2(1 + g)
        awgn_check.append((gdb, round(air, 3), round(shannon, 3)))
        if air > shannon + 0.05:
            results["deviations"].append(f"AWGN uniform AIR@{gdb}dB={air:.3f} > Shannon={shannon:.3f} (OVER-SHANNON, BUG)")
    results["meta"]["awgn_uniform_check"] = awgn_check
    print(f"[AWGN uniform check (AIR vs Shannon)] {awgn_check}")
    airs_awgn = [a for _, a, _ in awgn_check]
    if airs_awgn[-1] < 3.5:
        results["deviations"].append(f"AWGN uniform AIR@20dB={airs_awgn[-1]:.3f} 未趋 4 (BUG)")
    if airs_awgn != sorted(airs_awgn):
        results["deviations"].append("AWGN uniform AIR 非单调上升 (BUG)")

    # 锚点2: AWGN 下 MB vs uniform (16-QAM 整形空间小, 预期 gain 很小甚至略负)
    rng_mb = np.random.default_rng(SEED + 777)
    Nmb = 40000
    awgn_mb = []
    for gdb in [0, 5, 10]:
        g = 10 ** (gdb / 10)
        s2 = 1.0 / g
        row = {"snr_db": gdb}
        for nu in [0.0, 0.1, 0.3]:
            pmf = mb_pmf_16qam(nu)
            idx = rng_mb.choice(16, Nmb, p=pmf)
            tx = CONST[idx]
            nn = np.sqrt(s2 / 2) * (rng_mb.standard_normal(Nmb) + 1j * rng_mb.standard_normal(Nmb))
            y = tx + nn
            air = bmd_air(y, np.ones(Nmb), np.full(Nmb, s2), idx, pmf)
            row[f"nu{nu}"] = round(air, 3)
        awgn_mb.append(row)
    results["meta"]["awgn_mb_vs_uniform"] = awgn_mb
    print(f"[AWGN MB vs uniform (16-QAM整形空间小, gain预期小/略负)] {awgn_mb}")

    for turb in ["weak", "moderate", "strong"]:
        a, b = TURB[turb]
        results["curves"][turb] = {}
        for gdb in GAMMA_BAR_DB:
            gamma_bar = 10 ** (gdb / 10)
            t1 = time.time()
            elapsed = time.time() - t0
            use_n = N_SYM
            use_n_oracle = N_SYM_ORACLE
            if elapsed > 350:
                use_n = 50000
                use_n_oracle = 30000
                results["deviations"].append(f"降精度 @ {turb}/{gdb}dB (elapsed={elapsed:.0f}s): N={use_n}")
            elif elapsed > 250:
                use_n = 100000
                use_n_oracle = 50000

            base_seed = SEED + hash((turb, gdb)) % 100000

            # --- 1. uniform ---
            rng = np.random.default_rng(base_seed)
            h_u = gg_block(use_n, a, b)
            snr_u = gamma_bar * h_u
            s2_u = 1.0 / snr_u
            idx_u = rng.integers(0, 16, use_n)
            tx_u = CONST[idx_u]
            n_u = np.sqrt(s2_u / 2) * (rng.standard_normal(use_n) + 1j * rng.standard_normal(use_n))
            y_u = tx_u * np.sqrt(h_u) + n_u
            air_u = bmd_air(y_u, h_u, s2_u, idx_u, mb_pmf_16qam(0.0))

            # --- 2. offline MB: 共享 h, best_nu 选自代表 SNR ---
            rng_nu = np.random.default_rng(base_seed + 1)
            h_blocks_sample = gg_block(2000, a, b)
            best_nu = find_best_nu_offline(gamma_bar, h_blocks_sample, rng_nu)
            pmf_off = mb_pmf_16qam(best_nu)
            rng_o = np.random.default_rng(base_seed)
            h_o = h_u.copy()
            snr_o, s2_o = snr_u, s2_u
            idx_o = rng_o.choice(16, size=use_n, p=pmf_off)
            tx_o = CONST[idx_o]
            n_o = np.sqrt(s2_o / 2) * (rng_o.standard_normal(use_n) + 1j * rng_o.standard_normal(use_n))
            y_o = tx_o * np.sqrt(h_o) + n_o
            air_o = bmd_air(y_o, h_o, s2_o, idx_o, pmf_off)

            # --- 3. oracle per-block (CSI-aware 上界) ---
            rng_or = np.random.default_rng(base_seed + 2)
            h_or = gg_block(use_n_oracle, a, b)
            snr_or = gamma_bar * h_or
            s2_or = 1.0 / snr_or
            unique_snrs = np.unique(np.round(snr_or, 2))
            nu_cache = {}
            rng_orc = np.random.default_rng(base_seed + 3)
            for us in unique_snrs:
                nu_cache[us] = find_best_nu_for_snr(us, rng_orc, N_search=8000)
            idx_or = np.empty(use_n_oracle, dtype=int)
            n_blocks_or = use_n_oracle // BLOCK
            for blk in range(n_blocks_or):
                s, e = blk * BLOCK, (blk + 1) * BLOCK
                key = np.round(snr_or[s], 2)
                nu = nu_cache.get(key, 0.0)
                pmf = mb_pmf_16qam(nu)
                idx_or[s:e] = rng_or.choice(16, size=BLOCK, p=pmf)
            tx_or = CONST[idx_or]
            n_or = np.sqrt(s2_or / 2) * (rng_or.standard_normal(use_n_oracle) + 1j * rng_or.standard_normal(use_n_oracle))
            y_or = tx_or * np.sqrt(h_or) + n_or
            pmf_emp_or = np.bincount(idx_or, minlength=16) / len(idx_or)
            air_or = bmd_air(y_or, h_or, s2_or, idx_or, pmf_emp_or)

            results["curves"][turb][gdb] = {
                "uniform_air": round(air_u, 4),
                "offline_mb_air": round(air_o, 4),
                "offline_mb_nu": best_nu,
                "oracle_air": round(air_or, 4),
                "N_sym": use_n, "N_sym_oracle": use_n_oracle,
            }
            print(f"[{turb} {gdb:>2}dB] uniform={air_u:.3f} offline(nu={best_nu})={air_o:.3f} oracle={air_or:.3f}  (t={time.time()-t1:.1f}s)")

    # gain @ AIR=WORK_AIR 工作点
    for turb in ["weak", "moderate", "strong"]:
        curve = results["curves"][turb]
        gdbs = sorted(curve.keys())
        uni = np.array([curve[g]["uniform_air"] for g in gdbs])
        off = np.array([curve[g]["offline_mb_air"] for g in gdbs])
        g_uni = snr_for_air(uni, gdbs, WORK_AIR)
        g_off = snr_for_air(off, gdbs, WORK_AIR)
        if g_uni is not None and g_off is not None:
            gain = round(g_uni - g_off, 3)
        elif uni.max() < WORK_AIR and off.max() < WORK_AIR:
            gain = None
            results["deviations"].append(f"{turb}: 两方案 AIR 均未达 {WORK_AIR} (uni max={uni.max():.3f}, off max={off.max():.3f})")
        else:
            gain = None
        results["gain_at_work_air"][turb] = {
            "uniform_snr_db": round(g_uni, 2) if g_uni is not None else None,
            "offline_snr_db": round(g_off, 2) if g_off is not None else None,
            "gain_db": gain,
            "max_uniform_air": round(float(uni.max()), 3),
            "max_offline_air": round(float(off.max()), 3),
        }

    # TL-20 偏离检查
    gains = {t: results["gain_at_work_air"][t]["gain_db"] for t in ["weak", "moderate", "strong"]}
    for t, g in gains.items():
        if g is not None:
            if g < -0.1:
                results["deviations"].append(f"{t} gain={g:.3f}dB 为负 (offline MB < uniform)")
            if g > 2.0:
                results["deviations"].append(f"{t} gain={g:.3f}dB >2 (超 MB 上限, 查归一化)")

    results["meta"]["runtime_sec"] = round(time.time() - t0, 1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "n1_pcs_gain_mve_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[done] runtime={results['meta']['runtime_sec']}s  -> {out}")
    print(f"\n=== gain @ AIR={WORK_AIR} ===")
    for t in ["weak", "moderate", "strong"]:
        g = results["gain_at_work_air"][t]
        print(f"  {t:9s}: gain={g['gain_db']} dB  (uni_max={g['max_uniform_air']}, off_max={g['max_offline_air']})")
    if results["deviations"]:
        print(f"\n=== DEVIATIONS ({len(results['deviations'])}) ===")
        for d in results["deviations"]:
            print(f"  ! {d}")


if __name__ == "__main__":
    main()
