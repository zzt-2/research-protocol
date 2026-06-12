#!/usr/bin/env python3
"""红旗检测器 — 仿真结果物理合理性验证

在实验脚本中调用，捕获"震撼发现"级的 bug，防止错误结论传播。

用法:
  from tests.red_flags import check_results, check_ber, RedFlag

  # 方式1: 批量检查结果 dict
  flags = check_results({
      'method': 'DPLL', 'turbulence': 'strong', 'snr_db': 20,
      'ber': 0.0193, 'n_symbols': 10000,
  })

  # 方式2: 单个 BER 检查
  flags = check_ber(ber, method='KF_pilot', turbulence='strong', snr_db=20)

  # 方式3: 在实验循环中内联检查
  for seed in range(100):
      ber = run_experiment(seed)
      flags = check_ber(ber, method='DPLL', turbulence='strong', snr_db=20)
      if any(f.severity == 'CRITICAL' for f in flags):
          print(f"CRITICAL: {flags[0].message}")
          break

规则来源:
  - SPEC.md §6.1 已验证事实
  - thesis-lessons.md TL-20~25
  - 6 项目代码评审经验
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RedFlag:
    """红旗条目"""
    rule_id: str
    severity: str      # 'CRITICAL' (bug/物理不可能), 'WARNING' (可疑), 'INFO' (注意)
    category: str      # 'physical', 'regression', 'statistical', 'fairness'
    message: str
    detail: str

    def __str__(self):
        icon = {'CRITICAL': '!!!', 'WARNING': ' ! ', 'INFO': '   '}[self.severity]
        return f"[{icon}] {self.rule_id}: {self.message}"


# ═══════════════════════════════════════════════════════════════════
# 检查规则
# ═══════════════════════════════════════════════════════════════════

def _check_ber_range(ber: float, **ctx) -> List[RedFlag]:
    """RF-01: BER 在 [0, 1]"""
    if ber < 0 or ber > 1:
        return [RedFlag('RF-01', 'CRITICAL', 'physical',
                        f"BER={ber:.6f} 不在 [0,1]",
                        "计算错误或数值溢出")]
    return []


def _check_ber_not_near_half(ber: float, **ctx) -> List[RedFlag]:
    """RF-02: QPSK BER 不应长期接近 0.5

    BER ≈ 0.5 意味着载波恢复完全失败（输出随机星座）。
    可能原因: 4 次方鉴相器 pi/4 偏移未处理、频偏估计完全错误。
    """
    method = ctx.get('method', '')
    snr_db = ctx.get('snr_db', 20)

    # 高 SNR 下 BER 接近 0.5 是严重问题
    if snr_db >= 10 and 0.45 < ber < 0.55:
        return [RedFlag('RF-02', 'CRITICAL', 'physical',
                        f"BER={ber:.4f} ≈ 0.5 at SNR={snr_db}dB — 载波恢复完全失败",
                        f"检查 {method} 的频偏估计和相位模糊处理")]
    return []


def _check_ber_snr_monotonic(ber: float, **ctx) -> List[RedFlag]:
    """RF-03: 高 SNR 下 BER 应低

    20dB 以上 BER 应 < 10%。否则说明信号模型或载波恢复有根本问题。
    """
    snr_db = ctx.get('snr_db', 0)
    if snr_db >= 20 and ber > 0.10:
        method = ctx.get('method', 'unknown')
        turb = ctx.get('turbulence', 'unknown')
        return [RedFlag('RF-03', 'WARNING', 'physical',
                        f"BER={ber:.4f} > 10% at SNR={snr_db}dB ({method}, {turb})",
                        "高 SNR 高 BER: 检查信号模型(E[h]=1?)和载波恢复")]
    return []


def _check_known_ranges(ber: float, **ctx) -> List[RedFlag]:
    """RF-04: 与 SPEC.md §6.1 已验证事实对比

    基于 30 种子统计，允许 5x 容差（单种子 vs 30 种子平均）。
    """
    method = ctx.get('method', '')
    turb = ctx.get('turbulence', '')
    snr_db = ctx.get('snr_db', 20)

    if snr_db != 20:
        return []  # 只检查 20dB 单点

    # SPEC §6.1 已知范围 (30种子平均 ± 宽容差)
    known = {
        ('FOE+DPLL', 'strong'):   (0.005, 0.05),   # 1.93%
        ('FOE+VV', 'strong'):     (0.02, 0.15),     # 7.9%
        ('KF_pilot', 'strong'):   (0.01, 0.10),     # 3.08%
        ('Fixed', 'strong'):      (0.005, 0.05),    # 1.74%
        ('BPS', 'strong'):        (0.02, 0.15),     # BPS 强湍流类似 VV
        ('DPLL', 'strong'):       (0.005, 0.05),    # 同 FOE+DPLL
        ('VV', 'strong'):         (0.02, 0.15),     # 同 FOE+VV

        ('Fixed', 'weak'):        (0.0001, 0.01),   # 0.016%
        ('KF_pilot', 'weak'):     (0.0001, 0.01),   # 0.016%
        ('VV', 'weak'):           (0.0001, 0.01),   # 0.015%
        ('DPLL', 'weak'):         (0.001, 0.05),    # 0.20%

        ('Fixed', 'moderate'):    (0.001, 0.01),    # 0.15%
        ('KF_pilot', 'moderate'): (0.001, 0.01),    # 0.17%
        ('VV', 'moderate'):       (0.001, 0.01),    # 0.15%
        ('DPLL', 'moderate'):     (0.001, 0.01),    # 0.37%
    }

    key = (method, turb)
    if key in known:
        lo, hi = known[key]
        if ber < lo * 0.2:
            return [RedFlag('RF-04', 'WARNING', 'regression',
                            f"BER={ber:.6f} 远低于已知范围 [{lo:.4f}, {hi:.4f}] "
                            f"({method}, {turb})",
                            "可能使用了 oracle 信息或参数错误")]
        if ber > hi * 3:
            return [RedFlag('RF-04', 'WARNING', 'regression',
                            f"BER={ber:.6f} 远高于已知范围 [{lo:.4f}, {hi:.4f}] "
                            f"({method}, {turb})",
                            "可能是 bug 导致性能退化")]

    return []


def _check_gain_reasonable(ber: float, **ctx) -> List[RedFlag]:
    """RF-05: dB 增益在合理范围 [-10, +20] dB

    超出此范围意味着比较基线有问题（如旧 VV bug 导致 Fixed 基线 27%）。
    """
    gain_db = ctx.get('gain_db', None)
    if gain_db is None:
        return []

    if gain_db > 20:
        return [RedFlag('RF-05', 'CRITICAL', 'physical',
                        f"增益 {gain_db:.1f} dB > 20 dB — 基线可能有 bug",
                        "检查基线是否使用了正确的 VV 公式 (unwrap(angle)/M)")]
    if gain_db < -10:
        return [RedFlag('RF-05', 'WARNING', 'physical',
                        f"增益 {gain_db:.1f} dB < -10 dB — 新方法远不如基线",
                        "检查新方法实现是否正确")]

    return []


def _check_h_positive(ber: float, **ctx) -> List[RedFlag]:
    """RF-06: h 应始终 > 0"""
    h = ctx.get('h', None)
    if h is not None:
        if np.any(np.array(h) <= 0):
            return [RedFlag('RF-06', 'CRITICAL', 'physical',
                            "h 含非正值",
                            f"min(h)={np.min(h):.6e}, Gamma-Gamma 应始终 > 0")]
    return []


def _check_nans(ber: float, **ctx) -> List[RedFlag]:
    """RF-07: 输出不含 NaN/Inf"""
    rx = ctx.get('rx', None)
    if rx is not None:
        flags = []
        if np.any(np.isnan(rx)):
            flags.append(RedFlag('RF-07', 'CRITICAL', 'physical',
                                 "接收信号含 NaN", "检查除零或数值溢出"))
        if np.any(np.isinf(rx)):
            flags.append(RedFlag('RF-07', 'CRITICAL', 'physical',
                                 "接收信号含 Inf", "检查指数爆炸或除零"))
        return flags
    return []


def _check_seed_variance(ber: float, **ctx) -> List[RedFlag]:
    """RF-08: 多种子 BER 方差不应过小

    如果 30 个种子的 BER 完全相同（variance ≈ 0），说明随机数种子未生效。
    """
    ber_list = ctx.get('ber_list', None)
    if ber_list is not None and len(ber_list) >= 10:
        ber_arr = np.array(ber_list)
        std = np.std(ber_arr)
        mean = np.mean(ber_arr)
        if mean > 0 and std / mean < 1e-6:
            return [RedFlag('RF-08', 'WARNING', 'statistical',
                            f"BER 种子间变异系数 {std/mean:.2e} 极小",
                            "可能种子未正确传递或信道被缓存")]
    return []


def _check_fairness(ber: float, **ctx) -> List[RedFlag]:
    """RF-09: 同 seed 不同方法应使用相同信道"""
    # 这个检查需要在实验框架层做，这里只做标记
    channel_seed = ctx.get('channel_seed', None)
    if channel_seed is None:
        return [RedFlag('RF-09', 'INFO', 'fairness',
                        "未提供 channel_seed — 无法验证信道共享",
                        "建议使用 generate_shared_realization 保证公平性")]
    return []


# ═══════════════════════════════════════════════════════════════════
# 公开 API
# ═══════════════════════════════════════════════════════════════════

_ALL_CHECKS = [
    _check_ber_range,
    _check_ber_not_near_half,
    _check_ber_snr_monotonic,
    _check_known_ranges,
    _check_gain_reasonable,
    _check_h_positive,
    _check_nans,
    _check_seed_variance,
    _check_fairness,
]


def check_ber(ber: float, **context) -> List[RedFlag]:
    """检查单个 BER 值的物理合理性。

    Args:
        ber: 误码率
        **context: 上下文信息
            method: 方法名 ('DPLL', 'VV', 'KF_pilot', 'Fixed', 'BPS')
            turbulence: 湍流等级 ('weak', 'moderate', 'strong')
            snr_db: 信噪比 (dB)
            gain_db: 相对基线的 dB 增益
            h: 信道增益数组（可选，检查正值）
            rx: 接收信号数组（可选，检查 NaN/Inf）
            ber_list: 多种子 BER 列表（可选，检查统计特性）
            channel_seed: 信道种子（可选，检查公平性）
    """
    flags = []
    for check_fn in _ALL_CHECKS:
        flags.extend(check_fn(ber, **context))
    return flags


def check_results(results: dict) -> List[RedFlag]:
    """检查结果 dict 的物理合理性。

    Args:
        results: 包含 'ber', 'method', 'turbulence', 'snr_db' 等键的字典
    """
    ber = results.get('ber', results.get('ber_mean', None))
    if ber is None:
        return [RedFlag('RF-00', 'WARNING', 'statistical',
                        "结果 dict 缺少 'ber' 或 'ber_mean'",
                        "无法检查")]

    context = {
        'method': results.get('method', ''),
        'turbulence': results.get('turbulence', results.get('turb', '')),
        'snr_db': results.get('snr_db', results.get('snr', 20)),
        'gain_db': results.get('gain_db', None),
        'h': results.get('h', None),
        'rx': results.get('rx', None),
        'ber_list': results.get('ber_list', results.get('per_seed_ber', None)),
        'channel_seed': results.get('channel_seed', results.get('seed', None)),
    }
    return check_ber(ber, **context)


def format_flags(flags: List[RedFlag], verbose: bool = False) -> str:
    """格式化红旗列表为可读字符串"""
    if not flags:
        return "All checks passed — no red flags."

    lines = [f"Red flag detection: {len(flags)} issue(s) found"]
    lines.append("=" * 60)
    for f in flags:
        lines.append(str(f))
        if verbose:
            lines.append(f"    Category: {f.category}")
            lines.append(f"    Detail: {f.detail}")
            lines.append("")

    crit = sum(1 for f in flags if f.severity == 'CRITICAL')
    warn = sum(1 for f in flags if f.severity == 'WARNING')
    if crit > 0:
        lines.append(f"\n!!! {crit} CRITICAL issue(s) — STOP and investigate before proceeding")
    if warn > 0:
        lines.append(f"    {warn} WARNING(s) — review before writing conclusions")

    return "\n".join(lines)
