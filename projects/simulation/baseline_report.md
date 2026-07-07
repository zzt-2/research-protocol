# Baseline Report — SC-NDA-ML 正式仿真（Step 7 出参）

> 项目: projects/simulation | 阶段: GW Step 7（§impl 仿真环境搭建 + Baseline 复现）| 日期: 2026-07-06
> 上游: simulator-design.md（Step 6 设计确认）+ feasibility_report.md（4a+4b Go）+ decision_log.md（D-S5-01 baseline 选定）
> 框架: gw-experiment.md §impl Part A（搭建验证）+ Part B（Baseline 复现）

## 0. 状态摘要

**Step 7 Part A（仿真环境搭建 + 验证）PASS**：
- Formal 仿真器独立实现（`simulator/{sc_nda_ml_sim.py, fair_comparison.py, _b11_params.py}`，648+157+106 行），核心算法全从 common/ 导入（守 TL-13），不 import explore/
- **[§4.5] MVE 一致性验证**：4 场景 × 29 SNR 点 × 3 方法 = 87 BER 值 bit-exact 一致（相对误差 0.0000%），Formal 独立实现正确性证明
- 退化测试（关湍流/Wiener/Doppler）全 ✅
- 自相关：h 块间 lag-100 = 0.0164（非"过于平滑"），lag-1=0.99 是块内恒定物理特性（详见 simulator-design.md §4.4 修订）

**Step 7 主实验（5 seed 多种子统计）PASS**：
- 150 运行（5 seed × 4 场景 × 29 SNR 点），耗时 75s
- 第 0 seed bit-exact 复现 MVE（4 场景全 0.0000%）
- fair gain @ HD-FEC 5 seed 统计稳健，MVE 单 seed 全落 95% CI 内

---

## 1. Baseline 复现状态（gw-experiment §impl Part B）

### 1.1 复现定义（本项目适用）

本项目是**信号处理估计算法**（NDA-ML/DA ML 载波相位估计），不是 RL/MDP。gw-experiment §impl Part B"复现"定义为：
1. 在自己的仿真环境中实现论文算法架构和核心设计 ✅
2. 验证相对趋势（DRL > 传统 > 随机）→ 本项目映射为 **NDA-ML（提出方法）vs DA ML（FR-15 目标 baseline）vs oracle（上界）**
3. [MUST NOT] 直接对比绝对数值（环境不同）→ 本项目自建仿真器，与 B11 环境（OFDM 频域）架构性不等价（D002），只比相对趋势

### 1.2 Baseline 清单（templates.md B1 格式）

| 角色 | 方法 | 来源 | 复现状态 | 交叉验证 |
|------|------|------|----------|---------|
| **B1 目标 baseline**（FR-15）| DA ML（pilot-aided，pilot sp=4）| B11 行 181/191（自实现，common/_recovery.py:da_ml_recovery）| ✅ 已复现（Formal 仿真器 + 5 seed）| NDA-ML 天然对照（D-S5-01）；pilot-aided 是载波同步主流范式（田野调查部分确认）|
| **B2 上界对照**（非 baseline）| oracle（genie-aided 真相位 + 真 h）| 信息论上界（自实现）| ✅ 已实现 | NDA-vs-oracle gap 0.38-2.58dB 全 <3dB（升幂实现正确）|
| **提出方法**（非 baseline）| NDA-ML（升 M₀=8 + per-block 盲 h + resolve blockwise + 两阶段 FOE）| B11 思想源头（D002 重定位）+ 单载波时域改进（本方向贡献）| ✅ 已实现（common/_recovery.py:nda_ml_recovery D003 修复）| 5 seed 全赢 DA，无一反转 |

### 1.3 复现结果（趋势验证）

gw-experiment §impl Part B"复现成功 = DRL baseline 在关键指标上结构性优于传统 baseline" → 本项目映射：

**主指标：公平对照 fair gain @ HD-FEC BER=3.8e-3（5 seed 统计）**

| 场景 | NDA-ML vs DA ML gain mean (dB) | std | 95% CI (t,df=4) | MVE 单 seed | 趋势 |
|------|-------------------------------|-----|-----------------|-------------|------|
| AWGN（形态 A）| **+1.351** | 0.072 | [+1.305, +1.397] | +1.310 | ✅ NDA > DA（CI 下界 >>0.5dB SPEC §5 Go 门）|
| weak（α4/β3）| **+1.529** | 0.321 | [+1.131, +1.928] | +1.199 | ✅ NDA > DA |
| moderate（α2.5/β1.8）| **+1.712** | 0.250 | [+1.314, +2.110] | +1.922 | ✅ NDA > DA |
| strong（α1.5/β0.8）| HD-FEC 不可达（物理上限，oracle 也不可达），工作区 grand mean +2.515±0.555 | 0.555 | — | +1.19~+2.62 | ✅ NDA 全工作区赢 DA（5 seed × 18 工作点无一反转）|

> **D-007 (2026-07-07) 更新**：AWGN 场景从 B11 OFDM（25GBaud/500kHz）重定义为单载波（2.5GBaud/10kHz），与湍流路径统一。AWGN fair gain 从旧 +0.776 升至 +1.351（σ²p 弱 5× + segK8 块内跟踪让 NDA 优势增大）。weak/moderate/strong 不变（湍流路径参数未改，只改读法）。详见 decisions.md D-007。

**辅助：NDA-ML vs oracle gap**（升幂实现正确性）：0.38-2.58 dB 全 <3dB（TL-22 锚点），5 seed 下保持。

**TL-20 理论预期对照**（见 SC-NDA-ML-MVE-SPEC.md §2 预期表）：weak/moderate/strong 三场景实测均落在预期区间（0 DEVIATION）。AWGN 实测 +1.351 超 D-007 前旧预期上界 +0.8——**合理超出非 bug**，因 D-007 重定义场景（σ²p 从 500kHz→10kHz 弱 5×）+ segK8 块内跟踪让 NDA 全帧积分优势放大。旧预期基于过强 PN，新场景 NDA 优势更大（gain 1.351 > pilot overhead 1.249 → 估计精度维度也赢 DA）。详见 MVE-SPEC §2 偏离处理记录 + decisions.md D-007。

**复现判定**：**PASS**。提出方法（NDA-ML）在 4 场景全结构性优于目标 baseline（DA ML），CI 下界全 ≥0.5dB（SPEC §5 Go 门），strong 工作区全赢无反转。oracle 上界合理（gap <3dB）。

---

## 2. 仿真环境验证（gw-experiment §impl Part A 清单）

| 验证项 | 结果 | 证据 |
|--------|------|------|
| 解析验证 | ✅（隐含）| Formal bit-exact 复现 MVE，MVE 已通过 CRLB 解析对照（`_crlb_results.json`）|
| 统计验证 | ✅ | GG 幅度分布 + Wiener 增量正态（common/ 已验证，Formal 复用）|
| 退化测试 | ✅ | 关湍流（h≡1）/ 关 Wiener（σ²_p=0）/ 关 Doppler（f_dot=0）三场景 BER 退化正确（simulator/_consistency_check.json degradation_tests）|
| 自相关预警 | ✅（带修订）| h 块间 lag-100=0.0164（非"过于平滑"）；lag-1=0.99 是块内恒定物理特性（simulator-design.md §4.4 已修订）|
| **§4.5 MVE 一致性** | ✅ **bit-exact** | 4 场景 × 29 点 × 3 方法 BER 值全 0.0000% 相对误差（D-007 后重跑，含 NDA 路径修复 segK8 对齐，simulator/_consistency_check.json）|
| MDP 试运行 | N/A | 估计类方法非 RL/MDP（gw-feasibility §A0 §4 判定）|

---

## 3. 主实验结果细节

### 3.1 5 seed 统计（per-seed 法，主）

per-seed 法：每 seed 独立算 gain，再统计 5 个 gain 的 mean ± std。CI = t 分布 df=4，t=2.776。

per-seed gain（dB，5 seed，D-007 后）：
- AWGN：[1.310, 1.390, 1.391, 1.333, 1.333]（seed 0 = MVE 1.310，D-007 单载波统一 + segK8）
- weak：[1.199, 1.326, 1.824, 1.919, 1.379]（不变，湍流路径未改）
- moderate：[不可达_seed2, ...4 有效...] mean=1.712（seed 2 HD-FEC 不可达，正常涨落）
- strong：工作区 grand mean +2.515，per-point 15dB +1.77 / 20dB +2.73 / 22dB +2.82 / 24dB +2.90

### 3.2 参考法（avg-curve 法，交叉验证）

5 seed 平均 BER 曲线算 gain：AWGN +1.35 / weak +1.509 / moderate +1.841（D-007 后 AWGN 单载波统一）。与 per-seed 主法差异 <0.2dB，两法互证。

### 3.3 种子策略（防 CI 被人为缩小）

- AWGN：`seed_base_i = SEED_AWGN + i`（i=0..4）
- 湍流：`seed0_i = SEED_TURB0 + i·N_BLOCKS`（非 +i）——保证 5 seed 的 per-block seed 范围**互斥**，否则会重叠 399 块人为缩小方差

---

## 4. 已知债务与消融后置

| 债务/消融 | 状态 | 触发 |
|-----------|------|------|
| 跨块 KF/CPE 跟踪消融（FR-18 预判）| 后置（Step 7 主实验已完成，消融作 ablation 报告）| 论文写作需验证 cross-over 移动时 |
| BPS 迁移对比（田野调查候选补充）| 后置（场景不同，二级 baseline）| 论文写作需二级迁移 baseline 时 |
| SPEC.md §8 NDA-ML 段补完 | 待（Step 7 后用实际参数补更准）| 论文写作前 |
| decision-feedback DA ML 对照（B11 论文 DA ML 形式）| 后置（债务提示①）| 若 reviewer 质疑 pilot sp=4 vs decision-feedback 不对等 |

---

## 5. GW Step 7 质量门槛核查

- [x] 仿真器验证清单全部通过（§2）
- [x] MDP 试运行 N/A（估计类方法）
- [x] 至少 1 个 baseline 成功复现（DA ML FR-15 目标 baseline，5 seed 趋势 PASS）
- [x] 路径合规：代码 `projects/simulation/simulator/`，结果 `projects/simulation/results/sc_nda_ml_main/`
- [x] **[§4.5] MVE 一致性 bit-exact**（Formal 独立实现正确性证明）

**Step 7 出参完整**。GW Step 4a/4b/5/6/7 全闭合（feasibility_report + decision_log + simulator-design + baseline_report）。

---

## 6. 下一步（出 GW 进 Contract）

GW 阶段（Step 1-7）已完成核心路径。下一步选择：
1. **进 Contract 阶段**（stages/contract.md）：把 GW 产出的"单载波时域 NDA-ML 改进"落成 Contract（假设 + 信号 + success_signal + 反模式）
2. **补消融**（跨块 KF + BPS 迁移）：论文写作前补，作 ablation
3. **B7 Gardner TED FOE MVE**（并行第二候选，D004 后置）：视用户意图
4. **B3 架构决策**（多孔径阵列 vs 单链路）：最后做

待用户拍板下一步方向。
