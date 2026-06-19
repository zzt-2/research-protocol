"""FR-21 敏感性分析: 验证 Kill 信号是否稳健

针对主脚本 fr21_ub_adaptive_vs_static_interleaving.py 的三个潜在翻转因素:
  S1. BER-B 关系陡峭度: 主脚本用 P(burst>B*thandle) 上界, 这里试"瀑布陡峭"模型
      (B 不够时 BER 暴涨, B 够时 BER 平台), 看自适应优势是否显现
  S2. Cn2 跨度放大: 把 eta_h 从 0.3 扫到 1.0, 看 Cn2 跨度增大后自适应是否拉开
  S3. 静态 baseline 策略: 试"固定拍 B=27 全程" vs "固定拍 B=15 全程" 等多种静态策略,
      看自适应是否能 beat 合理的工程静态

判定: 若任一敏感性下自适应 vs 合理静态 > 0.5dB, Kill 信号不稳健, 需 MVE 验证。
      若全部敏感性下都 < 0.5dB, Kill 稳健。
"""
import json
import math
import os
import time

import numpy as np

from fr21_ub_adaptive_vs_static_interleaving import (
    Config, slant_path_Cn2, Lburst_from_Cn2, Lburst_from_Cn2_log,
    optimal_B, PARAM_SOURCES,
)


def codeword_err_waterfall(Lburst_mean, B, thandle, N_mc=200000, steepness=8.0):
    """瀑布陡峭模型: BER 在 B*thandle 附近急剧下降 (更接近真实 Polar+CA-SCL)。

    P_err = 1 / (1 + (B*thandle / Lburst_mean)^steepness)
    steepness 大 -> 瀑布陡 (B 不够时全错, B 够时全对); 主脚本等价 steepness->inf 的上界。
    """
    capacity = B * thandle
    ratio = capacity / Lburst_mean
    return 1.0 / (1.0 + ratio ** steepness)


def gain_db(better, worse):
    if better <= 0 or worse <= 0:
        return 0.0
    return 10.0 * math.log10(worse / better)


def run_sensitivity():
    cfg = Config()
    elev_axis = np.arange(cfg.elev_min_deg, cfg.elev_max_deg + 1, 5.0)
    # 仰角权重
    w = 1.0 / np.sin(np.deg2rad(elev_axis))
    w /= w.sum()

    results = {}

    # === S1: BER-B 瀑布陡峭度扫描 ===
    print("=" * 70)
    print("S1: BER-B 瀑布陡峭度敏感性")
    print("=" * 70)
    s1 = {}
    for steep in [2.0, 4.0, 8.0, 16.0]:
        # 用线性 Lburst (乐观上界)
        Cn2 = slant_path_Cn2(elev_axis, cfg.Cn2_ground, cfg.H_atm)
        Lb = Lburst_from_Cn2(Cn2, cfg.Cn2_ref, cfg.Lburst_ref)
        B_star = optimal_B(Lb, cfg.thandle)

        # 几种静态策略
        B_static_candidates = {
            "tang_27": 27,
            "opt_global_6": 6,
            "median_5": 5,
            "high_15": 15,
            "very_high_30": 30,
        }
        # 自适应 BER
        p_adaptive = np.array([codeword_err_waterfall(lb, max(1, int(b)), cfg.thandle, steepness=steep) for lb, b in zip(Lb, B_star)])
        ber_adaptive = float(np.sum(p_adaptive * w))

        row = {"ber_adaptive": ber_adaptive, "vs_static_db": {}}
        for name, Bs in B_static_candidates.items():
            p_s = np.array([codeword_err_waterfall(lb, Bs, cfg.thandle, steepness=steep) for lb in Lb])
            ber_s = float(np.sum(p_s * w))
            row["vs_static_db"][name] = gain_db(ber_adaptive, ber_s)
        s1[f"steep_{steep}"] = row
        best_vs_fair = max(v for k, v in row["vs_static_db"].items() if k != "tang_27")
        print(f"  steepness={steep}: 自适应 BER={ber_adaptive:.2e}, vs 最优静态(max gain)={best_vs_fair:.3f} dB")
    results["S1_waterfall"] = s1

    # === S2: Cn2 跨度放大 (eta_h 扫描) ===
    print()
    print("=" * 70)
    print("S2: Cn2 跨度敏感性 (eta_h: 大气湍流层衰减因子)")
    print("=" * 70)
    s2 = {}
    for eta_h in [0.1, 0.3, 0.5, 1.0]:
        # 临时改 eta_h: 直接用修改后的 slant_path
        elev = np.deg2rad(elev_axis)
        L_eff = cfg.H_atm / np.sin(elev)
        L_ref = 200e3
        Cn2 = cfg.Cn2_ground * eta_h * (L_eff / L_ref) ** (11.0 / 6.0)
        span = max(Cn2) / min(Cn2)
        Lb = Lburst_from_Cn2(Cn2, cfg.Cn2_ref, cfg.Lburst_ref)
        B_star = optimal_B(Lb, cfg.thandle)

        p_adaptive = np.array([codeword_err_waterfall(lb, max(1, int(b)), cfg.thandle, steepness=8.0) for lb, b in zip(Lb, B_star)])
        ber_adaptive = float(np.sum(p_adaptive * w))
        # vs 全程最优静态
        B_opt = int(np.round(np.sum(B_star * w)))
        p_opt = np.array([codeword_err_waterfall(lb, max(1, B_opt), cfg.thandle, steepness=8.0) for lb in Lb])
        ber_opt = float(np.sum(p_opt * w))
        g = gain_db(ber_adaptive, ber_opt)
        s2[f"eta_h_{eta_h}"] = {
            "Cn2_span_orders": math.log10(span),
            "B_star_range": [int(B_star.min()), int(B_star.max())],
            "B_static_optimal": B_opt,
            "gain_vs_opt_static_db": g,
        }
        print(f"  eta_h={eta_h}: Cn2 跨度={math.log10(span):.2f} 数量级, B*=[{int(B_star.min())},{int(B_star.max())}], 最优静态={B_opt}, 自适应增益={g:.3f} dB")
    results["S2_Cn2_span"] = s2

    # === S3: 极端放大场景 (假设更大仰角跨度或更强湍流变化) ===
    print()
    print("=" * 70)
    print("S3: 极端场景 (低仰角 5° + 强地面湍流 Cn2_ground=5e-14)")
    print("=" * 70)
    s3 = {}
    for elev_min in [20.0, 10.0, 5.0]:
        for cn2_g in [1.7e-14, 5e-14]:
            elev = np.deg2rad(np.arange(elev_min, 90 + 1, 5.0))
            L_eff = cfg.H_atm / np.sin(elev)
            L_ref = 200e3
            Cn2 = cn2_g * 0.3 * (L_eff / L_ref) ** (11.0 / 6.0)
            Lb = Lburst_from_Cn2(Cn2, cfg.Cn2_ref, cfg.Lburst_ref)
            B_star = optimal_B(Lb, cfg.thandle)
            w_local = 1.0 / np.sin(elev)
            w_local /= w_local.sum()

            p_adaptive = np.array([codeword_err_waterfall(lb, max(1, int(b)), cfg.thandle, steepness=8.0) for lb, b in zip(Lb, B_star)])
            ber_adaptive = float(np.sum(p_adaptive * w_local))
            B_opt = int(np.round(np.sum(B_star * w_local)))
            p_opt = np.array([codeword_err_waterfall(lb, max(1, B_opt), cfg.thandle, steepness=8.0) for lb in Lb])
            ber_opt = float(np.sum(p_opt * w_local))
            g = gain_db(ber_adaptive, ber_opt)
            key = f"elev_min_{elev_min}_cn2g_{cn2_g:.1e}"
            s3[key] = {
                "Cn2_span_orders": math.log10(max(Cn2) / min(Cn2)),
                "B_star_range": [int(B_star.min()), int(B_star.max())],
                "B_static_optimal": B_opt,
                "gain_vs_opt_static_db": g,
            }
            print(f"  elev_min={elev_min}°, Cn2_ground={cn2_g:.1e}: Cn2跨度={math.log10(max(Cn2)/min(Cn2)):.2f}量级, B*=[{int(B_star.min())},{int(B_star.max())}], 最优静态={B_opt}, 增益={g:.3f} dB")
    results["S3_extreme"] = s3

    # === 综合判定 ===
    print()
    print("=" * 70)
    print("综合判定 (FR-21 敏感性)")
    print("=" * 70)
    # 收集所有"自适应 vs 合理静态"的增益 (排除 tang_27 不公平对比)
    all_gains = []
    for k, v in s1.items():
        for name, g in v["vs_static_db"].items():
            if name != "tang_27":
                all_gains.append(("S1_" + k + "_" + name, g))
    for k, v in s2.items():
        all_gains.append(("S2_" + k, v["gain_vs_opt_static_db"]))
    for k, v in s3.items():
        all_gains.append(("S3_" + k, v["gain_vs_opt_static_db"]))

    max_gain = max(all_gains, key=lambda x: x[1])
    over_threshold = [(k, g) for k, g in all_gains if g >= 0.5]

    print(f"所有合理对比中最大增益: {max_gain[0]} = {max_gain[1]:.3f} dB")
    if over_threshold:
        print(f"⚠️ 有 {len(over_threshold)} 个场景增益 >= 0.5dB, Kill 信号不稳健:")
        for k, g in over_threshold:
            print(f"    {k}: {g:.3f} dB")
        print("  -> 建议: 进 MVE 用真实 Polar+CA-SCL 验证 (而非瀑布近似)")
    else:
        print(f"✅ 所有 {len(all_gains)} 个合理对比场景增益均 < 0.5dB, Kill 信号稳健")
        print("  -> 自适应交织在'自适应 vs 合理静态'框架下无 BER 增益空间")
        print("  -> 方向 4b#1 在当前 BER 维度判定为不成立")

    out = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "param_sources": PARAM_SOURCES,
        "results": results,
        "verdict": {
            "max_gain_fair_comparison": max_gain[1],
            "scenarios_over_0p5dB": over_threshold,
            "kill_robust": len(over_threshold) == 0,
        },
    }
    out_path = os.path.join(os.path.dirname(__file__), "fr21_sensitivity_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n结果已存: {out_path}")


if __name__ == "__main__":
    run_sensitivity()
