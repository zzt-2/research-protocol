"""B7 Gardner TED FOE — 经典频偏 ML CRB 下界 (FR-21 参考对照, D005 降级非 Kill 门).

任务 (见 sandbox task brief):
  推导 B7 FOE (基于 Gardner TED 增益扫频峰反演的间接估计) 的 CRB 下界, 作 FR-21
  参考对照. D005 已将 FR-21 降级为参考——CRB 只回答"B7 FOE 估计精度离理论极限多远",
  不当 Kill 门. 即使 CRB 很小也不 Kill B7.

============================================================================
CRB 公式确定 (Phase 1) — 经典频偏 ML CRB (参照下界)
============================================================================
B7 FOE 的信号模型 (跟 _ted_gain_analytic.py / content.md L47 一致):
    rx(t) = s(t)·exp(j·2π·f_D·t) + n(t)
    s(t) = RRC 成型 QPSK 符号序列 (25 GBaud, roll-off 0.1)
    f_D  = 待估 Doppler 频偏 (扫频范围 0-23 GHz)
    n(t) = AWGN (OSNR 17 dB 主测 / 10 dB 低 SNR)

B7 是**间接估计** (Gardner TED 增益 G(f̂)=K_max·|cos(π f̂/B)| 扫频找峰反演 f̂_D),
非直接 ML 频偏估计. 严格 CRB 推导复杂. 实务用**经典频偏 ML CRB 作参照下界**:
B7 作为次优 NDA 间接估计, 实际方差一定 ≥ (高于) 此 CRB.

选用 **Rife & Boorstijn 1974 单音频率估计 CRB** (data-aided / 已知 s(t) 的绝对下界,
ML 频偏估计器一致下界). 辅助来源: Mengali & Andò 1997, Kay 1993 (max-likelihood
频率估计). 这些是频偏估计的经典标准文献, 非臆造.

  信号 (符号率采样, N 个符号): r(n) = s(n)·exp(j·2π·f_D·n·T_s) + w(n),  n=0..N-1
    未知参数 (f_D, 相位 φ, 幅度). f_D 的 CRB (相位作 nuisance 积分掉):

      var(f̂_D) ≥ CRB(f_D) = 12 / [ (2π)² · (E_s/N_0) · T_s² · N·(N²−1) ]   [Hz²]   ★

    标准 (见 Rife-Boorstijn IEEE TASSP 1974, Eq. for simultaneous tone freq/phase;
          Kay "Fundamentals of Statistical Signal Processing: Estimation Theory"
          1993, ch. 15.7 ML frequency estimation CRB; Mengali & D'Andrea
          "Synchronization Techniques for Digital Receivers" 1997 §3.7.
    常数 12 (不是 6) 对应 f_D 与初相 φ 同时未知的情形——这是 FOE 现实场景 (B7
    相位未知), 用 12 更贴切. 6 对应相位已知特例 (不现实, 留作对照).

    SNR = E_s/N_0 (每符号能量 / 单边噪声功率谱密度).
    T_s = 1/R_SYM (符号周期, B7 在 FOE 前降采样到 2 sps 但符号率采样是 CRB 自然的
          观测网格; 这里观测 N 个符号, 间隔 T_s).
    N   = 观测符号数.

  关键: CRB(f_D) ∝ 1/(SNR · N³) (大 N 极限, 因 N·(N²−1)≈N³). 理论趋势 std ∝ N^(-3/2).

OSNR → E_s/N_0 转换 (光通信标准, B_ref=12.5 GHz 参考, 0.1nm):
    OSNR = P_signal / P_ASE(0.1nm);  E_s/N_0 = OSNR · (2·B_ref) / R_SYM
    对于 B7: R_SYM = 25 GBaud, 2·B_ref = 25 GHz ⇒ (2·B_ref)/R_SYM = 1.0 恰好
    ⇒ E_s/N_0 (linear) = OSNR (linear)  for 25 GBaud (巧合约为 1, 但仍写出式)
    线性 ↔ dB: E_s/N_0_dB = OSNR_dB + 10·log10((2·B_ref)/R_SYM) = OSNR_dB + 0 dB

  注: 此转换对 DP-QPSK 单偏振成立; 双偏振 (DP) 总能量翻倍但每偏振 SNR 不变, B7 FOE
  在单偏振工作 (或两偏振独立估), CRB 用单偏振 E_s/N_0 即可.

============================================================================
要点 / 陷阱防护
============================================================================
  1. CRB 给的是**方差** [Hz²]; 报告同时给 std = sqrt(CRB) [Hz] 更直观 (任务陷阱 3).
  2. CRB 是 DA 绝对下界; B7 实际方差 ≥ CRB (B7 次优 NDA 间接估计). 不臆造"B7 的 CRB"
     (陷阱 4).
  3. FR-21 降级 (D005): CRB 不当 Kill 门, 只作"B7 离理论极限多远"的参考尺 (陷阱 5).
  4. 公式常数 12 (相位未知) vs 6 (相位已知) 必须明确——本任务用 12 (陷阱 1).
  5. B7 是间接估计, 严格 CRB 复杂; 用经典 ML CRB 参照下界, 标注假设 (DA, 已知 s(t)).
  6. 自包含 (跟 _ted_gain_analytic.py / _psa_foe_asymmetry.py 一致): 不 import common/
     params, 参数内联 (值 = B7Params 真相源, content.md L21/L47/L49 溯源).

运行: cd projects/simulation && python explore/b7-gardner-ted-foe/_crb_lower_bound.py
"""
import os
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
# CJK 字体 (Windows): 优先 Microsoft YaHei / SimHei, 兼容中文字符 (避免方框)
for _f in ("Microsoft YaHei", "SimHei", "Microsoft JhengHei", "DejaVu Sans"):
    try:
        matplotlib.font_manager.findfont(_f, fallback_to_default=False)
        matplotlib.rcParams["font.sans-serif"] = [_f]
        break
    except Exception:
        continue
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt


# =============================================================================
# B7 场景参数 (内联, 值 = B7Params 真相源; 不 import params 守自包含)
# 来源行号溯源: content.md L21/L25/L47「25-Gbaud DP-QPSK」, L49「OSNR 17 dB」, L49「interval 1 GHz」
# =============================================================================
R_SYM = 25e9              # 符号率 25 GBaud (content.md L21/L25/L47)
T_S = 1.0 / R_SYM         # 符号周期 40 ps
ROLL_OFF = 0.1            # RRC roll-off (content.md L47)
DOPPLER_INTERVAL = 1e9    # 扫频间隔 1 GHz (content.md L49) — B7 量化精度基准
DOPPLER_RANGE = 23e9      # 扫频范围 0-23 GHz (content.md L49)
B_REF = 12.5e9            # OSNR 参考带宽 0.1nm (光通信标准, = 12.5 GHz)
K_MAX = 0.13214186192586033   # G(f_D)=K_max|cos(pi f_D/B)| 峰 (步骤3 解析, _ted_gain_analytic_results.json)
# B = R_SYM = 25 GHz (G(f_D) 周期, 步骤3)

# Sweep 配置 (任务 §2.2)
N_SWEEP = [256, 512, 1024, 2048, 4096]      # 观测符号数 sweep
OSNR_SWEEP_DB = [10.0, 17.0, 20.0]          # OSNR dB sweep (10 低 SNR / 17 主测 / 20 高)
OSNR_MAIN_DB = 17.0                         # B7 主测点 (content.md L49)
N_MAIN = 1024                               # B7 典型观测长度 (_ted_gain_analytic_results.json meta.n_sym)


# =============================================================================
# CRB 公式
# =============================================================================
def osnr_to_esn0(osnr_db, r_sym=R_SYM, b_ref=B_REF):
    """OSNR (dB, 0.1nm 参考) → E_s/N_0 (linear, 每符号 SNR).

    光通信标准: E_s/N_0 (linear) = OSNR (linear) · (2·B_ref) / R_SYM
    对 25 GBaud: (2·12.5GHz)/25GHz = 1.0 ⇒ E_s/N_0_dB = OSNR_dB (巧合).
    """
    osnr_lin = 10.0 ** (osnr_db / 10.0)
    return osnr_lin * (2.0 * b_ref) / r_sym


def crb_variance_hz2(n_sym, osnr_db, r_sym=R_SYM):
    """经典 ML 频偏 CRB (Rife-Boorstijn / Kay / Mengali), 单位 Hz².

    var(f̂_D) ≥ 12 / [(2π)²·(E_s/N_0)·T_s²·N·(N²−1)]   [Hz²]  (相位未知 DA 下界)

    n_sym: 观测符号数 N; osnr_db: OSNR dB; r_sym: 符号率.
    返回 (CRB_variance_Hz2, CRB_std_Hz). std = sqrt(var).
    """
    esn0 = osnr_to_esn0(osnr_db, r_sym)   # E_s/N_0 (linear)
    t_s = 1.0 / r_sym
    N = n_sym
    # 大 N 近似: 用精确 N(N²-1) (不近似成 N³, 守小 N 精度)
    var = 12.0 / ((2.0 * np.pi) ** 2 * esn0 * t_s ** 2 * N * (N ** 2 - 1))
    return var, np.sqrt(var)


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # ---- 表头 ----
    print("=" * 92)
    print("B7 Gardner TED FOE — 经典频偏 ML CRB 下界 (FR-21 参考对照, D005 降级非 Kill 门)")
    print(f"信号模型: rx(t)=s(t)·exp(j2π f_D t)+n(t), 25 GBaud DP-QPSK, RRC roll-off 0.1")
    print(f"CRB 公式: var(f̂_D) ≥ 12/[(2π)²·(E_s/N_0)·T_s²·N(N²−1)]  [Rife-Boorstijn 1974/Kay/Mengali, DA 下界]")
    print(f"OSNR→E_s/N_0: (2·B_ref)/R_SYM = (2·12.5GHz)/25GHz = 1.0 ⇒ E_s/N_0_dB = OSNR_dB (25GBaud 巧合)")
    print(f"扫频量化基准 (B7 DOPPLER_INTERVAL): {DOPPLER_INTERVAL/1e9:.0f} GHz")
    print("=" * 92)

    # ---- N × OSNR sweep ----
    results = {
        "meta": {
            "task": "B7 Gardner TED FOE CRB lower bound (FR-21 reference, D005 downgraded not Kill gate)",
            "source": "B7 OFC 2026 doi:10.1364_ofc.2026.w2a.62 + Rife-Boorstijn/Kay/Mengali classic FOE CRB",
            "crb_formula": {
                "expression": "var(f_D) >= 12 / [(2*pi)^2 * (E_s/N_0) * T_s^2 * N*(N^2-1)]  [Hz^2]",
                "std_expression": "std(f_D) >= sqrt(var)  [Hz]",
                "sources": [
                    "Rife & Boorstijn 1974, IEEE TASSP 22(2): single-tone freq+phase ML estimation CRB",
                    "Kay 1993, Fundamentals of Statistical Signal Processing Vol I, ch.15.7: ML frequency CRB",
                    "Mengali & D'Andrea 1997, Synchronization Techniques for Digital Receivers, Sec.3.7",
                ],
                "assumptions": [
                    "Data-aided / known s(t) (absolute lower bound)",
                    "Phase phi unknown (nuisance integrated out) -> constant 12 (not 6)",
                    "AWGN, symbol-rate samples, N symbols observed at interval T_s",
                    "CRB is variance lower bound; std=sqrt(CRB) reported for intuition",
                ],
                "scaling": "CRB(std) ~ 1/sqrt(SNR) * 1/N^(3/2)  (large N: N(N^2-1)~N^3)",
                "caveat": "B7 is NDA INDIRECT estimator (Gardner TED gain-scan peak inversion). "
                          "Strict CRB is complex. Classic ML CRB used as REFERENCE lower bound. "
                          "B7 actual variance >= this CRB (B7 suboptimal). NOT a Kill gate (D005).",
            },
            "osnr_to_esn0": {
                "formula": "E_s/N_0 (linear) = OSNR (linear) * (2*B_ref)/R_SYM,  B_ref=12.5 GHz",
                "factor_25gbaud": (2.0 * B_REF) / R_SYM,
                "factor_25gbaud_dB": 10 * np.log10((2.0 * B_REF) / R_SYM),
                "note": "For 25 GBaud: factor=1.0 exactly, so E_s/N_0_dB = OSNR_dB (coincidence).",
            },
            "params": {
                "R_SYM_Hz": R_SYM,
                "T_S_s": T_S,
                "roll_off": ROLL_OFF,
                "DOPPLER_INTERVAL_Hz": DOPPLER_INTERVAL,
                "DOPPLER_RANGE_Hz": DOPPLER_RANGE,
                "B_REF_Hz": B_REF,
                "K_max": K_MAX,
                "B_period_Hz": R_SYM,   # G(f_D) period (step3 analytic)
            },
            "sweep": {
                "N_symbols": N_SWEEP,
                "OSNR_dB": OSNR_SWEEP_DB,
            },
            "fr21_status": (
                "D005 downgraded FR-21 to REFERENCE (not Kill gate). "
                "CRB computed as a 'reference ruler': how far is B7 FOE accuracy from theoretical limit. "
                "Even if CRB << 1 GHz (huge headroom), B7 NOT killed. Go criteria = win baseline by few dB."
            ),
        },
        "results": {},   # per OSNR -> per N
    }

    print(f"\n{'OSNR_dB':>8} {'E_s/N_0':>8} {'N':>6} "
          f"{'CRB_var_Hz2':>14} {'CRB_std_Hz':>13} {'CRB_std_MHz':>12} "
          f"{'CRB/1GHz':>11} {'CRB/std@17dB_1024':>20}")
    print("-" * 92)

    # 基准 (OSNR=17dB, N=1024) — 主线核查锚点
    _, ref_std = crb_variance_hz2(N_MAIN, OSNR_MAIN_DB)

    for osnr_db in OSNR_SWEEP_DB:
        osnr_key = f"osnr_{osnr_db:.0f}dB"
        results["results"][osnr_key] = {
            "OSNR_dB": osnr_db,
            "EsN0_linear": osnr_to_esn0(osnr_db),
            "EsN0_dB": 10 * np.log10(osnr_to_esn0(osnr_db)),
            "by_N": {},
        }
        for N in N_SWEEP:
            var, std = crb_variance_hz2(N, osnr_db)
            ratio_vs_interval = std / DOPPLER_INTERVAL   # CRB std / 1 GHz
            entry = {
                "N": N,
                "CRB_variance_Hz2": float(var),
                "CRB_std_Hz": float(std),
                "CRB_std_MHz": float(std / 1e6),
                "CRB_std_GHz": float(std / 1e9),
                "CRB_ratio_vs_DOPPLER_INTERVAL": float(ratio_vs_interval),
                "obs_window_us": float(N * T_S * 1e6),
            }
            results["results"][osnr_key]["by_N"][str(N)] = entry
            print(f"{osnr_db:>8.0f} {osnr_to_esn0(osnr_db):>8.2f} {N:>6d} "
                  f"{var:>14.4e} {std:>13.4e} {std/1e6:>12.4e} "
                  f"{ratio_vs_interval:>11.3e} {std/ref_std:>20.4f}")

    # ---- 关键结论提取 (主线核查锚点) ----
    main17 = results["results"]["osnr_17dB"]["by_N"][str(N_MAIN)]
    main10 = results["results"]["osnr_10dB"]["by_N"][str(N_MAIN)]

    # N 趋势 (OSNR=17dB): 拟合 std ∝ N^alpha 验证 N^-3/2
    ns_arr = np.array(N_SWEEP, dtype=float)
    stds17 = np.array([results["results"]["osnr_17dB"]["by_N"][str(int(n))]["CRB_std_Hz"]
                       for n in ns_arr])
    # 大 N 段拟合 (N>=512) 避免 N(N²-1) vs N³ 偏差
    mask = ns_arr >= 512
    alpha_fit = float(np.polyfit(np.log(ns_arr[mask]), np.log(stds17[mask]), 1)[0])

    verdict_n = main17["CRB_ratio_vs_DOPPLER_INTERVAL"]
    if verdict_n < 0.01:
        bottleneck = ("CRB std << 1 GHz (by %g x). B7 scan quantization (1 GHz) is the "
                      "FAR dominant accuracy bottleneck, NOT the theoretical CRB limit. "
                      "B7 could in principle do much finer by shrinking scan interval.") % (1.0 / verdict_n)
    elif verdict_n < 0.1:
        bottleneck = ("CRB std << 1 GHz (by %g x). B7 scan quantization (1 GHz) dominates; "
                      "CRB far below scan step.") % (1.0 / verdict_n)
    elif verdict_n < 1.0:
        bottleneck = ("CRB std < 1 GHz but same order of magnitude. Scan interval 1 GHz is "
                      "reasonable vs theoretical limit (no huge headroom but not CRB-limited).")
    else:
        bottleneck = ("CRB std >= 1 GHz: theoretical limit near/above scan step. "
                      "Scan interval 1 GHz already finer than CRB allows — CRB-bound regime.")

    results["key_findings"] = {
        "anchor_N1024_OSNR17dB": {
            "CRB_variance_Hz2": main17["CRB_variance_Hz2"],
            "CRB_std_Hz": main17["CRB_std_Hz"],
            "CRB_std_MHz": main17["CRB_std_MHz"],
            "CRB_std_GHz": main17["CRB_std_GHz"],
            "CRB_over_DOPPLER_INTERVAL": main17["CRB_ratio_vs_DOPPLER_INTERVAL"],
            "interpretation": (
                "At B7 main test point (N=1024, OSNR=17 dB), the DA ML frequency CRB std is "
                f"{main17['CRB_std_MHz']:.4g} MHz = {main17['CRB_std_GHz']:.4g} GHz. "
                f"This is {main17['CRB_ratio_vs_DOPPLER_INTERVAL']:.4g} of the 1 GHz scan step."),
        },
        "N_scaling_exponent": {
            "fitted_alpha": alpha_fit,
            "expected_large_N": -1.5,
            "note": "std ∝ N^alpha; large-N theory = -3/2 (since CRB ∝ 1/N^3). "
                    "Fitted on N>=512 (avoids N(N^2-1) vs N^3 small-N deviation).",
        },
        "bottleneck_verdict": bottleneck,
        "fr21_reference_conclusion": (
            "CRB provides B7 FOE theoretical accuracy floor (DA ML, optimistic). B7 (NDA indirect "
            "estimator) actual variance >= CRB. Since CRB std << 1 GHz scan step, B7's dominant "
            "error source is the discrete 1 GHz scan grid, not the fundamental estimation limit. "
            "FR-21 REFERENCE only (D005): CRB does NOT kill B7 regardless of magnitude. "
            "Practical path: if sub-GHz precision needed, B7 can refine by narrowing scan interval "
            "(poster Fig.3b confirms narrow re-scan after initial estimate works)."
        ),
    }

    print("\n" + "=" * 92)
    print("关键结论 (主线核查锚点):")
    print(f"  N=1024, OSNR=17dB: CRB std = {main17['CRB_std_MHz']:.4g} MHz "
          f"= {main17['CRB_std_GHz']:.4g} GHz  = {main17['CRB_ratio_vs_DOPPLER_INTERVAL']:.4g}× 1GHz scan step")
    print(f"  N scaling: std ∝ N^{alpha_fit:.3f} (theory large-N = -1.5)")
    print(f"  瓶颈: {bottleneck}")
    print(f"\n  FR-21: 参考对照 (D005 降级非 Kill 门). CRB << 1GHz ⇒ B7 精度瓶颈 = 扫频量化, 非理论极限.")

    # ---- 写 JSON ----
    out_json = os.path.join(out_dir, "_crb_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nJSON: {out_json}")

    # ---- 画图: CRB vs N (双 OSNR) + 1GHz 水平线 ----
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    # 左: CRB std vs N (log-log), 三 OSNR 曲线
    ax = axes[0]
    colors = {10.0: "#d62728", 17.0: "#1f77b4", 20.0: "#2ca02c"}
    for osnr_db in OSNR_SWEEP_DB:
        stds = [results["results"][f"osnr_{osnr_db:.0f}dB"]["by_N"][str(N)]["CRB_std_Hz"]
                for N in N_SWEEP]
        ax.plot(N_SWEEP, np.array(stds) / 1e6, "o-", color=colors[osnr_db], linewidth=2,
                markersize=7, label=f"OSNR={osnr_db:.0f} dB (E_s/N_0_dB={10*np.log10(osnr_to_esn0(osnr_db)):.1f})")
    ax.axhline(DOPPLER_INTERVAL / 1e6, color="black", linestyle="--", linewidth=2,
               label=f"B7 scan step = {DOPPLER_INTERVAL/1e9:.0f} GHz (DOPPLER_INTERVAL)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("观测符号数 N")
    ax.set_ylabel("CRB std(f_D)  [MHz]")
    ax.set_title("B7 FOE CRB 下界 vs 观测长度\n"
                 "var(f_D) ≥ 12/[(2π)²(E_s/N_0)T_s²N(N²−1)]  (Rife-Boorstijn/Kay/Mengali, DA 下界)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8.5, loc="upper right")
    # 标注 N=1024 主点
    ax.axvline(N_MAIN, color="gray", linestyle=":", alpha=0.6)
    ax.annotate("B7 主测点\nN=1024", xy=(N_MAIN, main17["CRB_std_Hz"] / 1e6),
                xytext=(N_MAIN * 1.4, main17["CRB_std_Hz"] / 1e6 * 6),
                fontsize=8, color="gray",
                arrowprops=dict(arrowstyle="->", color="gray", alpha=0.6))

    # 右: 柱状对比 CRB std vs 扫频间隔 vs 扫频范围 (log y), OSNR=17dB
    ax2 = axes[1]
    bar_labels = [f"N={N}" for N in N_SWEEP] + ["1 GHz\n(scan step)", "23 GHz\n(scan range)"]
    bar_vals_mhz = ([results["results"]["osnr_17dB"]["by_N"][str(N)]["CRB_std_Hz"] / 1e6
                     for N in N_SWEEP]
                    + [DOPPLER_INTERVAL / 1e6, DOPPLER_RANGE / 1e6])
    bar_colors = (["#1f77b4"] * len(N_SWEEP) + ["#ff7f0e", "#7f7f7f"])
    bars = ax2.bar(range(len(bar_vals_mhz)), bar_vals_mhz, color=bar_colors, alpha=0.85)
    ax2.set_yscale("log")
    ax2.set_xticks(range(len(bar_labels)))
    ax2.set_xticklabels(bar_labels, fontsize=8)
    ax2.set_ylabel("频率 [MHz]  (log scale)")
    ax2.set_title("CRB std(f_D) vs B7 扫频量化 (OSNR=17 dB)\n"
                  "CRB std << 1 GHz scan step ⇒ 瓶颈=量化非理论极限")
    ax2.grid(True, axis="y", alpha=0.3, which="both")
    for b, v in zip(bars, bar_vals_mhz):
        ax2.text(b.get_x() + b.get_width() / 2, v * 1.15, f"{v:.3g}",
                 ha="center", va="bottom", fontsize=7.5)

    plt.tight_layout()
    out_png = os.path.join(out_dir, "_crb_curve.png")
    plt.savefig(out_png, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"PNG:  {out_png}")
    print("=" * 92)


if __name__ == "__main__":
    main()
