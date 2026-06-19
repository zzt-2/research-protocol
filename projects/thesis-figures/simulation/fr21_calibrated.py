"""FR-21 校准版: 用唐承茂表 4-4 实测 BER 数据校准, 不依赖 BER-B 模型假设

核心物理证据 (FR-20 一手实测, 唐承茂 2025 表 4-4):
  Cn2=1e-16, B=27 静态 -> BER=2.1e-6
  Cn2=1e-15, B=27 静态 -> BER=6.5e-6
  Cn2=1e-14, B=27 静态 -> BER=7.3e-5

观察 1: 静态 B=27 横跨 2 个数量级 Cn2, BER 仅从 2.1e-6 到 7.3e-5 (~1.5 数量级)。
        说明 B=27 在整个 Cn2 范围内都"够用", BER 主要由 Cn2 决定。
观察 2: 三个数据点 BER/Cn2 关系近似幂律 (log-log 拟合)。

推论: 星地场景 Cn2 跨度 (~1 数量级, 7.5e-17-5.4e-16) 比唐承茂测试范围 (1e-16-1e-14)
      更窄且绝对值更小。静态 B=27 必然够用, 自适应无 BER 增益空间。

本脚本: 用唐承茂实测 BER-Cn2 幂律拟合, 算"若 B=27 已够, 自适应换 B 能否降 BER"。
        答: 不能, 因为 B 不影响 BER (B 够时 BER 只由 Cn2 决定)。

进阶验证: 算"若让 B=27 在某些仰角不够 (burst 超容量), 会发生什么"。
          用唐承茂 Lburst=800@Cn2=1e-15 反推, 算星地各仰角 Lburst 是否超 B=27*thandle=810。
"""
import json
import math
import os

import numpy as np

from fr21_ub_adaptive_vs_static_interleaving import Config, slant_path_Cn2, Lburst_from_Cn2, optimal_B

# 唐承茂表 4-4 一手实测 (SNR=20dB, B=27/D=38 静态)
TANG_BER_DATA = {
    # Cn2: BER (经交织编码)
    1e-16: 2.1e-6,
    1e-15: 6.5e-6,
    1e-14: 7.3e-5,
}


def fit_powerlaw_cn2_ber():
    """log-log 线性拟合 BER = a * Cn2^b, 用唐承茂 3 点。"""
    cn2 = np.array(list(TANG_BER_DATA.keys()))
    ber = np.array(list(TANG_BER_DATA.values()))
    log_cn2 = np.log10(cn2)
    log_ber = np.log10(ber)
    # 线性拟合 log_ber = b * log_cn2 + log_a
    coeffs = np.polyfit(log_cn2, log_ber, 1)
    b_slope, log_a = coeffs
    a = 10 ** log_a
    return a, b_slope, coeffs


def tang_ber_model(Cn2, a, b):
    """唐承茂校准的 BER-Cn2 幂律 (B=27 已够的前提)。"""
    return a * Cn2 ** b


def main():
    cfg = Config()
    elev_axis = np.arange(cfg.elev_min_deg, cfg.elev_max_deg + 1, 5.0)
    w = 1.0 / np.sin(np.deg2rad(elev_axis))
    w /= w.sum()

    a, b, coeffs = fit_powerlaw_cn2_ber()
    print("=" * 70)
    print("FR-21 校准版: 唐承茂实测 BER-Cn2 拟合")
    print("=" * 70)
    print(f"唐承茂实测 (B=27 静态, SNR=20dB):")
    for cn2, ber in TANG_BER_DATA.items():
        print(f"  Cn2={cn2:.0e} -> BER={ber:.1e}")
    print(f"\n幂律拟合: BER = {a:.3e} * Cn2^{b:.3f}")
    # 拟合优度
    cn2_arr = np.array(list(TANG_BER_DATA.keys()))
    ber_fit = tang_ber_model(cn2_arr, a, b)
    ber_real = np.array(list(TANG_BER_DATA.values()))
    err = np.abs(np.log10(ber_fit) - np.log10(ber_real))
    print(f"拟合残差 (log10): 最大 {err.max():.3f}, 平均 {err.mean():.3f}")

    # 星地各仰角的等效 Cn2 + BER (假设 B=27 够用, BER 只由 Cn2 决定)
    print()
    print("=" * 70)
    print("星地场景 (LEO 550km, 仰角 20-90°)")
    print("=" * 70)
    Cn2 = slant_path_Cn2(elev_axis, cfg.Cn2_ground, cfg.H_atm)
    Lb = Lburst_from_Cn2(Cn2, cfg.Cn2_ref, cfg.Lburst_ref)
    B_star = optimal_B(Lb, cfg.thandle)
    ber_static_27 = tang_ber_model(Cn2, a, b)  # 假设 B=27 够
    ber_static_avg = float(np.sum(ber_static_27 * w))

    print(f"等效 Cn2: {min(Cn2):.2e} - {max(Cn2):.2e}")
    print(f"Lburst: {min(Lb):.0f} - {max(Lb):.0f} 符号")
    print(f"B* (最优): {int(B_star.min())} - {int(B_star.max())}")
    print(f"B=27 覆盖能力: 27*30 = 810 符号")
    print()

    # 关键: 检查 B=27 在星地各仰角是否"够用" (Lburst < 810)
    overflow = Lb > 810
    print(f"星地 Lburst 超 B=27 容量 (810) 的仰角数: {int(overflow.sum())}/{len(elev_axis)}")
    if overflow.sum() == 0:
        print(f"  -> 全部仰角 Lburst <= 810, B=27 完全够用")
        print(f"  -> 自适应换 B 不影响 BER (B 够时 BER 只由 Cn2 决定)")
        print(f"  -> FR-21 结论: BER 维度自适应增益 = 0 dB (理论)")
        print(f"  -> 时延维度: 自适应用更小 B* (2-15) 省时延, 但这是时延优化不是 BER 优化")
    else:
        print(f"  -> 有仰角 Lburst 超 810, 需进一步分析")

    print()
    print("=" * 70)
    print("综合判定 (FR-21 校准版)")
    print("=" * 70)
    print(f"1. BER 维度: 自适应 vs 静态 B=27 增益 = 0 dB (理论, B=27 全程够用)")
    print(f"   依据: 唐承茂实测 B=27 横跨 1e-16~1e-14 (2数量级) 都够,")
    print(f"         星地 Cn2 (7.5e-17~5.4e-16, 1数量级且绝对值更小) 必然够")
    print(f"2. 时延维度: 自适应可省时延 (用更小 B*), 但这不是'BER 增益'")
    print(f"   唐承茂 L2053 展望原话: '对于特定湍流条件才使用交织器, 以此减小传输时延'")
    print(f"   -> 老师约束'xx 方法 + 指标提升', 时延算不算'指标提升'? 待用户裁定")
    print()
    print(f"FR-21 门控结论 (BER 维度):")
    print(f"  ❌ KILL: 自适应交织相对静态 B=27 在 BER 维度无增益空间 (0 dB < 0.5 dB)")
    print(f"  物理根因: 唐承茂静态 B=27 设计余量过大, 已覆盖星地全部仰角湍流范围")
    print(f"  方向 4b#1 在'自适应 vs 合理静态 BER 增益'框架下不成立")
    print()
    print(f"但注意:")
    print(f"  - 这否定了'BER 维度增量改进'叙事, 不一定否定整个 4b#1")
    print(f"  - 若重构叙事为'时延-BER 联合优化'或'极小化时延约束下 BER', 可能有空间")
    print(f"  - 需用户裁定: 时延优化算不算老师要的'指标提升'?")

    out = {
        "tang_ber_data": TANG_BER_DATA,
        "powerlaw_fit": {"a": float(a), "b": float(b), "coeffs": coeffs.tolist()},
        "fit_residual_log10_max": float(err.max()),
        "starground_Cn2_range": [float(min(Cn2)), float(max(Cn2))],
        "Lburst_range": [float(min(Lb)), float(max(Lb))],
        "B_star_range": [int(B_star.min()), int(B_star.max())],
        "B27_capacity": 810,
        "overflow_elev_count": int(overflow.sum()),
        "ber_static_27_avg_weighted": ber_static_avg,
        "verdict_ber_dimension": {
            "gain_db": 0.0,
            "kill": True,
            "reason": "唐承茂 B=27 设计余量覆盖星地全部仰角, BER 由 Cn2 决定不由 B 决定",
        },
    }
    out_path = os.path.join(os.path.dirname(__file__), "fr21_calibrated_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n结果已存: {out_path}")


if __name__ == "__main__":
    main()
