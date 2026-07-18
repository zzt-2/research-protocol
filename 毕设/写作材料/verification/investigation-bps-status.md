# BPS (Blind Phase Search) 实现状态调查报告

> 2026-06-01 | 调查 | 状态: 完成
> 目标: 查明 BPS 实现现状、算法规范、实现工作量、以及论文是否需要 BPS 数据

---

## 1. 当前实现状态

### 1.1 common.py — 无 BPS 实现

`common.py` 是当前唯一的仿真基础设施（SPEC.md 指定为唯一来源）。该文件包含以下方法：

| 方法 | 函数 | 状态 |
|------|------|------|
| FOE (FFT-FOE) | `fft_foe()` | 已实现 |
| VV (Viterbi-Viterbi) | `vv_cpr()` | 已实现 |
| DPLL | `dpll_track()` | 已实现 |
| Fixed (FOE+DPLL+VV) | `carrier_recovery_fixed()` | 已实现 |
| KF oracle | `kf_oracle_recovery()` | 已实现 |
| KF frame-h | `kf_frame_h_recovery()` | 已实现 |
| KF pilot | `kf_pilot_recovery()` | 已实现 |
| **BPS** | — | **未实现** |

`run_trial_shared()` 的 schemes 列表为 `['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot']`，不包含 BPS。

### 1.2 multi_seed_sweep.py — 占位符（伪造数据）

`experiments/multi_seed_sweep.py` 中 `method_bps()` 函数（L75-92）是一个占位符：

- 输出 `WARNING: BPS is not implemented, using DPLL as placeholder`
- 实际调用的是 `dpll_track(omega_n=20e6, zeta=sqrt(2)/2)`，**不是 BPS 算法**
- 默认 `--methods` 已排除 BPS：`['VV', 'DPLL', 'KF_pilot', 'Fixed']`
- BPS 是被有意排除的，因为它是占位符

### 1.3 旧代码 — 有可工作的 BPS 实现

`projects/thesis-figures/simulation/sim_ch4_systematic_analysis.py`（旧文件，SPEC.md 标记为"参考"）包含完整的 BPS 实现（L150-175）：

```python
def bps_cpr(rx, B=32, Nw=61):
    """Blind Phase Search (Pfau 2009, JLT)"""
    N = len(rx)
    phases = 2 * pi * arange(B) / B

    # 向量化: B个候选相位 x N个符号
    rotated = rx[newaxis, :] * exp(-1j * phases[:, newaxis])
    dec = (sign(real(rotated)) + 1j * sign(imag(rotated))) / sqrt(2)
    metrics = abs(rotated - dec)**2

    # 滑动窗口平均
    ker = ones(Nw) / Nw
    for b in range(B):
        metrics[b] = convolve(metrics[b], ker, mode='same')

    # 选择最小距离对应的相位
    best_b = argmin(metrics, axis=0)
    pe_raw = phases[best_b]

    # M=4 相位模糊展开
    pe = unwrap(4 * pe_raw) / 4

    return rx * exp(-1j * pe), pe
```

该实现已通过 100 种子验证（`verify_systematic.py`），强湍流失败率 ~45% 与文献预期一致。

---

## 2. BPS 算法规范摘要

### 2.1 核心算法（Pfau 2009, JLT）

| 步骤 | 操作 | 公式 |
|------|------|------|
| 1 | 构造 B 个候选相位 | phi_b = 2*pi*b/B, b=0,...,B-1 |
| 2 | 旋转接收信号 | r_rot = r[k] * exp(-j*phi_b) |
| 3 | 硬判决 | s_hat = (sign(Re(r_rot)) + j*sign(Im(r_rot))) / sqrt(2) |
| 4 | 计算距离度量 | d[k,b] = abs(r_rot - s_hat)^2 |
| 5 | 滑动窗口平均 | S[k,b] = sum(d[i,b], i=k-Nw..k+Nw) / Nw |
| 6 | 选择最优相位 | pe_raw[k] = phi_{argmin_b S[k,b]} |
| 7 | 相位模糊展开 | pe = unwrap(4 * pe_raw) / 4 |

### 2.2 默认参数

| 参数 | 值 | 说明 |
|------|-----|------|
| B (候选相位数) | 32 | 分辨率 pi/32 = 5.6 deg |
| Nw (窗口长度) | 61 | 对称窗口 2*30+1 |
| M (调制阶数) | 4 (QPSK) | unwrap 乘 4 |

### 2.3 与 VV 的关键差异

| 维度 | VV | BPS |
|------|----|-----|
| 鉴相方式 | 4次方去调制 | 硬判决+距离度量 |
| pi/4 偏移 | 有（需修正） | 无 |
| 复杂度/符号 | O(Nw) | O(B*Nw) ~32x |
| 相位分辨率 | 连续 | 离散 (pi/B) |
| 调制格式 | 仅 M-PSK | 任意 QAM |

---

## 3. 预期性能特征

来自 V-15 调研文档和旧代码 100 种子验证：

| 湍流等级 | BPS BER 预期 | VV BER | DPLL BER | 失败率 (BER>10%) |
|----------|-------------|--------|----------|-----------------|
| 弱 | 0.01%-0.05% | 0.015% | 0.20% | ~0% |
| 中 | 0.1%-0.3% | 0.15% | 0.37% | ~0% |
| 强 | 5%-15% | 7.9% | 1.93% | ~45% (VV ~40%, DPLL 0%) |

关键结论：BPS 与 VV 在 QPSK 场景下性能同量级，无显著优势。BPS 的价值在于高阶调制（16-QAM），在 QPSK 场景下复杂度高 32 倍却无性能增益。

---

## 4. 实现工作量评估

### 4.1 方案 A：移植旧实现到 common.py（推荐）

从 `sim_ch4_systematic_analysis.py` 移植 `bps_cpr()` 到 `common.py`，约 25 行核心代码。

具体步骤：
1. 将 `bps_cpr()` 复制到 common.py 的载波恢复区域（L171 之后）
2. 添加 `run_bps(shared, eq_mode='oracle')` 便捷函数
3. 在 `run_trial_shared()` 中添加 `'bps'` scheme
4. 在 `multi_seed_sweep.py` 中替换占位符为真实实现
5. 运行验证：10 种子快检 + 100 种子全验证

工作量：**约 30 分钟**（代码简单，已有经过验证的实现可直接移植）

风险：低。旧实现已通过 100 种子验证，算法正确。需确认 unwrap 方式与 resolve_qpsk 的兼容性。

### 4.2 方案 B：直接用旧代码跑 BPS 数据

不移植到 common.py，而是在旧 `sim_ch4_systematic_analysis.py` 中运行 Exp4 + verify_systematic.py。

工作量：**约 10 分钟**（代码已就绪，直接运行）

风险：中。旧代码使用独立的信号生成（非 `generate_shared_realization`），与其他方法不共享信道实例，对比公平性需额外论证。

### 4.3 方案 C：不实现 BPS，调整论文叙述

如果 BPS 数据不关键，可以：
- 论文中描述 BPS 算法原理（公式层面），引用文献数据
- 仿真对比聚焦 VV vs DPLL vs KF（已有完整数据）
- 将 BPS 作为"理论分析对象"而非"仿真验证对象"

工作量：**约 1 小时**（调整论文结构和叙述）

风险：低。BPS 在 QPSK 下与 VV 性能同量级，缺少 BPS 仿真数据不影响核心结论。

---

## 5. 论文是否需要 BPS 数据

### 5.1 论文中 BPS 的定位

根据 `thesis-status.md` 和 `design-decisions.md`：

- **thesis-status.md L74**: "4.4.2 盲相位搜索算法" -- BPS 作为 Ch4 的一个独立子节
- **thesis-status.md L100**: "4.4 增加 BPS 作为独立子节，与 VV/DPLL 并列"
- **design-decisions.md C03**: "系统性分析路线（VV/BPS/DPLL 对比）"
- **D013**: "Ch4 战略转向系统性分析路线" -- 已锁定决策

论文结构明确将 BPS 与 VV、DPLL 并列为三大 CPR 基线方法。**如果缺少 BPS 仿真数据，Ch4 的系统性分析叙述不完整。**

### 5.2 核心判断

| 维度 | 评估 |
|------|------|
| 论文结构要求 | BPS 是 Ch4 三大基线之一，**需要仿真数据** |
| 实现难度 | 低（25 行代码，已有验证过的实现） |
| 工作量 | 方案 A 约 30 分钟，方案 B 约 10 分钟 |
| 对结论的影响 | BPS 与 VV 同量级，不影响"DPLL 最优"核心结论 |
| 风险 | 极低 -- 不涉及新算法，只是补齐已有算法的数据 |

### 5.3 建议

**推荐方案 A**：移植旧 BPS 实现到 common.py，在多种子扫描中跑 BPS 数据。

理由：
1. 论文结构明确要求 BPS 数据（与 VV/DPLL 并列分析）
2. 已有经过 100 种子验证的实现，移植工作量极小（30 分钟）
3. 使用 `generate_shared_realization` 保证与其他方法对比的公平性
4. BPS 数据补齐后，Ch4 的"三方法系统性对比"叙事完整

**不推荐省略 BPS**：虽然 BPS 与 VV 性能同量级、对核心结论无影响，但论文结构已锁定为 VV/BPS/DPLL 三方法并列，缺少 BPS 数据会在答辩时被质疑。

---

## 6. 实现检查清单（如决定实现）

- [ ] 将 `bps_cpr()` 从旧代码移植到 `common.py`（L171 后）
- [ ] 添加默认参数常量：`DEF_B_BPS = 32`, `DEF_NW_BPS = 61`
- [ ] 添加 `run_bps(shared, eq_mode='oracle')` 便捷函数
- [ ] 在 `run_trial_shared()` 的 schemes 中添加 `'bps'`
- [ ] 在 `multi_seed_sweep.py` 中替换占位符为真实实现
- [ ] 运行 10 种子快检：确认 BPS BER 在预期范围内
- [ ] 运行 100 种子验证：确认强湍流失败率 ~45%
- [ ] 更新 SPEC.md 已验证事实清单

---

## 7. 关键文件索引

| 文件 | 路径 | 角色 |
|------|------|------|
| 仿真基础设施 | `projects/simulation/common.py` | 当前唯一来源，缺 BPS |
| 仿真规范 | `projects/simulation/SPEC.md` | 参数和评估标准 |
| 多种子扫描 | `projects/simulation/experiments/multi_seed_sweep.py` | 含 BPS 占位符 |
| 旧 BPS 实现 | `projects/thesis-figures/simulation/sim_ch4_systematic_analysis.py` L150-175 | 可移植的工作实现 |
| 旧 BPS 验证 | `projects/thesis-figures/simulation/verify_systematic.py` | 100 种子验证 |
| BPS 性能预期 | `毕设/写作材料/verification/phase1-research/ch4-systematic/V-15-bps-performance-expectations.md` | 量化锚点 |
| 论文状态 | `毕设/thesis-status.md` | BPS 在论文中的定位 |
| 设计决策 | `毕设/design-decisions.md` D013, C03 | 系统性分析路线 |
