"""FR-21 oracle 上界门控：自适应交织 vs 静态交织（星地 GG 湍流）

目的: 在投入 MVE 前，用纯解析/数值方法估算"理想自适应（每个仰角用最优 B/D）
      相对 静态（固定 B/D）"的 BER 增益上界。上界 <0.5dB → 方向 Kill。
      来源: TL-27 / FR-21（groundwork.md §4a 维度 D step 5）。

TL-25 起飞检查单:
  [1] 信道/参数溯源: 唐承茂表 4-1/4-3 + HV 标准廓线 (见 PARAM_SOURCES)
  [2] baseline 已优化: 静态 B=27/D=38 = 唐承茂 Lburst≈800 反推
  [3] 先写理论预期: 自适应增益应随仰角跨度增大（低仰角湍流强→自适应省更多 BER）
      —— 若反过来（高仰角优势大），物理错误，查
  [4] N>=100000 MC 样本 (TL-27 教训: N=20000 会虚高)
  [5] 输出含元数据: git hash + 时间戳 + 参数源
  [6] 估算过粗的部分显式标注"上界"/"下界"

参数溯源 (FR-20)
- Cn2(0) = 1.7e-14 m^-2/3 (地面) — HV 白天标准值
    来源: Hufnagel 1978 / Andrews & Phillips "Laser Beam Propagation through Random Media" Ch 12 (HV 5/7 模型)
- 仰角->Cn2 映射: sec^(11/3) 简化 + 高度积分 (slant path)
    来源: Andrews Ch 12 标准 slant-path Rytov 积分
- 波长 lambda = 1.55e-6 m — 唐承茂表 4-1
- Polar N=1024 R=0.5, thandle ~= 30 bit — 唐承茂 3.2.4 (3GPP TS 38.212 估算)
- Lburst(Cn2=1e-15) ~= 800 — 唐承茂 L1081-1088
- 静态 B=27/D=38 — 唐承茂表 4-3 (由 Lburst=800 / thandle=30 反推)
- LEO 高度 H_sat = 550 km — 标准 Starlink-like (未验证 Le 2021 是否同值, 标 TBD)
- 仰角范围 20-90 deg — LEO 过境典型 (未验证 Le 2021, 标 TBD)

注意 (未验证项, 影响 FR-21 可信度)
- Le 2021 abstract 未出现 "Gamma-Gamma" (子 agent 2026-06-19 核查),
  仅称 "atmospheric turbulence"。本文按 GG 模型估算; 若 Le 2021 全文非 GG,
  上界结论不变 (FR-21 只需任意弱->强湍流跨度下的交织增益), 但 §F17
  "GG-LCR/AFD 解析链" 创新核描述需修正。后续 Groundwork Step 3 精读确认。
"""
import json
import math
import os
import subprocess
import time
from dataclasses import dataclass, asdict

import numpy as np

# ---------- 参数溯源 ----------
PARAM_SOURCES = {
    "Cn2_ground": ("1.7e-14 m^-2/3", "HV 白天标准 (Hufnagel 1978 / Andrews Ch12)"),
    "lambda": ("1.55e-6 m", "唐承茂 2025 表 4-1"),
    "Polar_N": (1024, "唐承茂 2025 表 4-3"),
    "Polar_R": (0.5, "唐承茂 2025 表 4-3"),
    "thandle_bits": (30, "唐承茂 3.2.4 (3GPP TS 38.212 估算)"),
    "Lburst_at_Cn2_1e-15": (800, "唐承茂 L1081-1088 (L=200km 空空反推)"),
    "static_B": (27, "唐承茂 2025 表 4-3"),
    "static_D": (38, "唐承茂 2025 表 4-3 (D=N/B=1024/27)"),
    "H_sat_km": (550, "LEO 标准 (Starlink-like), 未验证 Le 2021"),
    "elev_range_deg": ([20, 90], "LEO 过境典型, 未验证 Le 2021"),
    "rate_Mbps": (200, "唐承茂 2025 表 4-1"),
    "N_mc": (200000, "TL-27 要求 >=100000, 取 2x 安全"),
}


@dataclass
class Config:
    # 物理
    Cn2_ground: float = 1.7e-14        # HV 白天地面
    lam: float = 1.55e-6               # 波长 m
    H_sat: float = 550e3               # 卫星高度 m
    H_atm: float = 20e3                # 大气等效厚度 m (HV 主要湍流层在 0-20km)
    # 编码/交织 (唐承茂)
    thandle: float = 30.0              # Polar N=1024 R=0.5 单码字纠错 bit
    Lburst_ref: float = 800.0          # Cn2=1e-15 反推的 Lburst (符号)
    Cn2_ref: float = 1e-15             # Lburst_ref 对应的 Cn2
    static_B: int = 27
    static_D: int = 38
    rate_Mbps: float = 200.0
    # 仰角 (LEO 过境)
    elev_min_deg: float = 20.0
    elev_max_deg: float = 90.0
    # MC
    N_mc: int = 200000
    seed: int = 42


def slant_path_Cn2(elev_deg: np.ndarray, Cn2_ground: float, H_atm: float) -> np.ndarray:
    """简化 slant-path 等效 Cn2: 沿斜径积分 Rytov, 折算回水平等效 Cn2。

    物理: Rytov sigma_R^2 = 1.23 * Cn2 * k^(7/6) * L^(11/6) (平面波, 水平路径)
    斜径: L_eff = H_atm / sin(elev), 等效 Cn2 沿积分。
    简化: 取 Cn2 沿斜径平均近似 = Cn2_ground * (高度衰减因子), 折算成
          "若水平链路要用多大 Cn2 才产生相同 Rytov"。
    用 sec^(11/6) 的 L^(11/6) 部分 + Cn2 高度衰减 h^-4/3 (HV 上层) 近似。

    返回: 每个仰角下的"等效 Cn2_eff" (用于 Lburst 反推)。
    来源: Andrews Ch12 标准 slant-path 积分; HV h^-4/3 上层衰减 (Hufnagel 1978)。
    """
    elev = np.deg2rad(elev_deg)
    # 斜径因子: L_eff ∝ 1/sin(elev)
    sec_factor = 1.0 / np.sin(elev)
    # Cn2 高度衰减: 地面 Cn2_ground, 沿斜径积分 HV 平均 ~ Cn2_ground * (H_atm 积分衰减)
    # 取等效平均 Cn2 = Cn2_ground * eta_h (eta_h ~ 0.3, HV 廓线 0-20km 积分均值/地面值)
    eta_h = 0.3  # HV 标准, Andrews Ch12 图 12.2 估算
    # Rytov ∝ Cn2_eff * L^(11/6). 把 (Cn2_eff, L_eff) 等效为 (Cn2_eq, L_ref) 同 Rytov
    # 这里直接给"若唐承茂 200km 水平链路要产生相同 Rytov, 需多大 Cn2_eq"
    # 唐承茂 L=200km 是水平, 这里 L_eff = H_atm/sin(elev)
    L_ref = 200e3  # 唐承茂参考距离
    L_eff = H_atm / np.sin(elev)
    # Rytov_eq = Cn2_eff * L_eff^(11/6) = Cn2_eq * L_ref^(11/6)
    # => Cn2_eq = Cn2_ground * eta_h * (L_eff / L_ref)^(11/6)
    Cn2_eq = Cn2_ground * eta_h * (L_eff / L_ref) ** (11.0 / 6.0)
    return Cn2_eq


def Lburst_from_Cn2(Cn2: np.ndarray, Cn2_ref: float, Lburst_ref: float) -> np.ndarray:
    """由 Cn2 反推平均突发长度 Lburst (符号)。

    模型: Lburst ∝ AFD * rate ∝ 1/LCR * rate. LCR/AFD 与湍流强度关系:
      强湍流 (大 Cn2) -> 深衰落频发 -> AFD (单次衰落持续) 也会变, 但 burst 长度主要 ∝ AFD。
      简化: AFD ∝ sigma_I^2 (闪烁指数, 弱到中湍流近似线性)。
      sigma_I^2 ∝ Cn2 (线性, 平面波 Rytov)。
    => Lburst ∝ Cn2 (弱-中湍流线性近似)。

    注: 这是上界估算, 非精确 LCR/AFD 闭式。中-强湍流 GG 饱和会让 Lburst 增长变缓,
    这里线性外推是**乐观上界** (高估强湍流下 Lburst, 高估自适应潜力)。
    若想保守, 用 log 关系 Lburst ∝ log(Cn2); 两种都跑做对比 (见 main)。
    """
    return Lburst_ref * (Cn2 / Cn2_ref)


def Lburst_from_Cn2_log(Cn2: np.ndarray, Cn2_ref: float, Lburst_ref: float) -> np.ndarray:
    """对数版 (保守下界): 强湍流 GG 饱和后 Lburst 增长慢。

    模型: Lburst = Lburst_ref * (1 + log10(Cn2/Cn2_ref)), 下限 clamp 到 Lburst_ref*0.1
    (弱湍流下 Lburst 不会无限小, 物理下限 ~ AWGN 误码随机化的最小突发长度)。
    """
    val = Lburst_ref * (1.0 + np.log(Cn2 / Cn2_ref) / np.log(10.0))
    return np.maximum(Lburst_ref * 0.1, val)  # 每数量级 Cn2 +1x Lburst, 物理下限保护


def optimal_B(Lburst: np.ndarray, thandle: float) -> np.ndarray:
    """最优交织深度 B* = ceil(Lburst / thandle). 唐承茂反推逻辑 (L1081-1088)."""
    return np.maximum(1, np.ceil(Lburst / thandle)).astype(int)


def codeword_error_prob(Lburst_samples: np.ndarray, B: int, thandle: float) -> float:
    """简化码字错误率上界估计 (MC)。

    模型: 单个 Polar 码字 (N=1024 bit) 内若实际 burst 总长 > B*thandle,
    则交织后仍有连续突发 > 单码字纠错能力 -> 码字错。
    P_err = P(burst_in_codeword > B*thandle)
    burst_in_codeword: Poisson 采样 (单位时间到达的 burst 数), 每个 burst 长度 Exp(Lburst_mean)。

    更简化 (上界): 给定瞬时 Lburst, 码字错概率 ≈ P(Poisson(rate_burst * T_codeword) * Lburst > B*thandle)
    这里直接用 Lburst_samples 当瞬时, 算"若用 B, 该样本是否 burst > B*thandle"。
    """
    capacity = B * thandle
    # MC: 每个样本 (瞬时 Lburst) 下, 实际 burst 长 Exp(Lburst) 采样, 判断是否 > capacity
    rng = np.random.default_rng(42)
    # 每样本采 1 个实际 burst 长度
    actual = rng.exponential(scale=Lburst_samples)
    return float(np.mean(actual > capacity))


def ber_from_codeword_err(p_cw_err: float, R: float, N: int) -> float:
    """由码字错误率近似 BER (上界): 码字错则贡献 ~R/2 比特错 (最坏全错)。"""
    # 简化上界: BER <= p_cw_err * 0.5 (最坏全码字 bit 错)
    return p_cw_err * 0.5


def estimate_upper_bound(cfg: Config, elev_axis: np.ndarray, Lburst_fn):
    """对给定仰角轴, 算自适应 vs 静态的 BER 加权平均 + dB 增益。"""
    # 1. 每仰角的等效 Cn2
    Cn2 = slant_path_Cn2(elev_axis, cfg.Cn2_ground, cfg.H_atm)
    # 2. 每仰角的瞬时 Lburst (这里直接用均值, MC 在 codeword_error_prob 内)
    Lburst_mean = Lburst_fn(Cn2, cfg.Cn2_ref, cfg.Lburst_ref)
    # 3. 自适应: 每仰角最优 B*(elev)
    B_star = optimal_B(Lburst_mean, cfg.thandle)
    # 4. 静态: 全程加权平均 B* 的四舍五入 (按唐承茂逻辑, 取代表性)
    #    仰角权重: LEO 过境, 低仰角停留时间长, 用 sec(elev) 加权 (过境轨迹均匀)
    w = 1.0 / np.sin(np.deg2rad(elev_axis))
    w /= w.sum()
    B_static_optimal = int(np.round(np.sum(B_star * w)))  # 全程最优静态
    B_static_tang = cfg.static_B  # 唐承茂静态值

    # 5. 每仰角 BER (MC)
    #    用大样本: 对每仰角独立 MC
    p_cw_static_tang = np.array([
        codeword_error_prob(np.full(cfg.N_mc, lb), cfg.static_B, cfg.thandle)
        for lb in Lburst_mean
    ])
    p_cw_static_opt = np.array([
        codeword_error_prob(np.full(cfg.N_mc, lb), max(1, B_static_optimal), cfg.thandle)
        for lb in Lburst_mean
    ])
    p_cw_adaptive = np.array([
        codeword_error_prob(np.full(cfg.N_mc, lb), max(1, int(b)), cfg.thandle)
        for lb, b in zip(Lburst_mean, B_star)
    ])

    ber_static_tang = ber_from_codeword_err(p_cw_static_tang, cfg.Polar_R if hasattr(cfg, 'Polar_R') else 0.5, 1024)
    ber_static_opt = ber_from_codeword_err(p_cw_static_opt, 0.5, 1024)
    ber_adaptive = ber_from_codeword_err(p_cw_adaptive, 0.5, 1024)

    # 6. 加权平均 BER (LEO 过境全程)
    ber_static_tang_avg = float(np.sum(ber_static_tang * w))
    ber_static_opt_avg = float(np.sum(ber_static_opt * w))
    ber_adaptive_avg = float(np.sum(ber_adaptive * w))

    # 7. dB 增益 (BER 比值取 log10*10)
    def gain_db(better, worse):
        if better <= 0 or worse <= 0:
            return float('inf') if better < worse else float('-inf')
        return 10.0 * math.log10(worse / better)

    # 时延上界: 自适应在弱湍流区 (B*<B_static) 省交织深度 -> 省时延
    # 时延 ∝ B*D ∝ B*(N/B)=N ... 卷积交织时延 = B*(B-1)*D = ~B^2*D/something
    # 唐承茂卷积交织总延时 = B_max * (B-1) * D. 简化: 时延 ∝ B*(B-1)*D
    def delay(B, D):
        return B * (B - 1) * D
    delay_static = delay(cfg.static_B, cfg.static_D)
    delay_adaptive_per_elev = np.array([delay(max(1, int(b)), max(1, int(b))) for b in B_star])  # D=B 近似
    delay_adaptive_avg = float(np.sum(delay_adaptive_per_elev * w))
    delay_save_pct = (delay_static - delay_adaptive_avg) / delay_static * 100.0

    return {
        "elev_axis": elev_axis.tolist(),
        "Cn2_eq": Cn2.tolist(),
        "Lburst_mean": Lburst_mean.tolist(),
        "B_star": B_star.tolist(),
        "B_static_optimal_global": B_static_optimal,
        "B_static_tangchengmao": cfg.static_B,
        "ber_static_tang_per_elev": ber_static_tang.tolist(),
        "ber_adaptive_per_elev": ber_adaptive.tolist(),
        "ber_static_tang_avg": ber_static_tang_avg,
        "ber_static_opt_avg": ber_static_opt_avg,
        "ber_adaptive_avg": ber_adaptive_avg,
        "gain_adaptive_vs_tang_db": gain_db(ber_adaptive_avg, ber_static_tang_avg),
        "gain_adaptive_vs_optstatic_db": gain_db(ber_adaptive_avg, ber_static_opt_avg),
        "delay_static": delay_static,
        "delay_adaptive_avg": delay_adaptive_avg,
        "delay_save_pct": delay_save_pct,
        "B_star_min": int(B_star.min()),
        "B_star_max": int(B_star.max()),
    }


def main():
    cfg = Config()
    elev_axis = np.arange(cfg.elev_min_deg, cfg.elev_max_deg + 1, 5.0)

    # 两种 Lburst-Cn2 关系: 线性 (乐观上界) + 对数 (保守下界)
    res_linear = estimate_upper_bound(cfg, elev_axis, Lburst_from_Cn2)
    res_log = estimate_upper_bound(cfg, elev_axis, Lburst_from_Cn2_log)

    # 元数据
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.getcwd()).decode().strip()
    except Exception:
        git_hash = "unknown"

    out = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "git_hash": git_hash,
        "param_sources": PARAM_SOURCES,
        "config": asdict(cfg),
        "model_assumption": {
            "burst_dist": "Exponential(mean=Lburst) per codeword",
            "codeword_err_rule": "P(actual_burst > B*thandle)",
            "weight_elev": "1/sin(elev) (LEO 过境轨迹, 低仰角停留久)",
            "static_B_strategy": [
                "tang: 唐承茂固定 B=27/D=38 (空空 Cn2=1e-15 反推)",
                "opt: 全程加权最优 B_static_optimal (公平 baseline)",
            ],
            "ber_model": "BER <= 0.5 * p_cw_err (最坏全码字错上界)",
        },
        "linear_Lburst_optimistic_ub": res_linear,
        "log_Lburst_conservative_lb": res_log,
    }

    out_path = os.path.join(os.path.dirname(__file__), "fr21_ub_adaptive_vs_static_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # 打印关键结论
    print("=" * 70)
    print("FR-21 上界门控结果 (自适应 vs 静态交织)")
    print("=" * 70)
    print(f"仰角范围: {cfg.elev_min_deg}-{cfg.elev_max_deg} deg, MC N={cfg.N_mc}/仰角")
    print(f"等效 Cn2 跨度: {min(res_linear['Cn2_eq']):.2e} - {max(res_linear['Cn2_eq']):.2e}")
    print(f"最优 B* 跨度: {res_linear['B_star_min']} - {res_linear['B_star_max']}")
    print(f"全程最优静态 B_static_optimal = {res_linear['B_static_optimal_global']}")
    print(f"唐承茂静态 B = {res_linear['B_static_tangchengmao']}")
    print()
    print("--- 线性 Lburst-Cn2 (乐观上界: 高估自适应潜力) ---")
    print(f"  自适应 vs 唐承茂静态 BER 增益: {res_linear['gain_adaptive_vs_tang_db']:.3f} dB")
    print(f"  自适应 vs 全程最优静态 BER 增益: {res_linear['gain_adaptive_vs_optstatic_db']:.3f} dB")
    print(f"  时延节省: {res_linear['delay_save_pct']:.1f}%")
    print()
    print("--- 对数 Lburst-Cn2 (保守下界: GG 饱和) ---")
    print(f"  自适应 vs 唐承茂静态 BER 增益: {res_log['gain_adaptive_vs_tang_db']:.3f} dB")
    print(f"  自适应 vs 全程最优静态 BER 增益: {res_log['gain_adaptive_vs_optstatic_db']:.3f} dB")
    print(f"  时延节省: {res_log['delay_save_pct']:.1f}%")
    print()
    print("判定 (FR-21):")
    best_db = max(res_linear['gain_adaptive_vs_optstatic_db'], res_log['gain_adaptive_vs_optstatic_db'])
    if best_db < 0.5:
        print(f"  ❌ KILL: 最乐观上界 {best_db:.3f} dB < 0.5 dB, 方向不成立")
    else:
        print(f"  ✅ PASS: 最乐观上界 {best_db:.3f} dB >= 0.5 dB, 可进 MVE")
        print(f"     (但注意: 上界乐观, MVE 实际增益可能更低; 还需 §D MVE 验证)")
    print()
    print(f"结果已存: {out_path}")


if __name__ == "__main__":
    main()
