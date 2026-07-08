# Handoff: 阶段 1.5 重设计——放松前馈化到 [79] 式闭环 hold + power-boosted pilot（救援 B2-Q2）

> 来源: S004（主控对话 V5 核查 + 方向定夺）| 交接目标: 下一工作对话执行阶段 1.5 重设计（闭环 hold + power-boosted pilot）
> 文件名: H004-conversation4-rescue-redesign.md
> 日期: 2026-07-08

## 到哪了（状态）

**主控对话 S004 完成 sandbox V5 核查 + 方向定夺**。用户推翻主线初始 Kill 建议，选**救援路线**（D003）。

**V5 核查结论**：
- 接收方验证 5 PASS + 1 口径修正（H003 fair gain -0.187dB 算错，实测 +0.02dB，C 微赢但仍远低于 0.5dB 阈值）
- 三 Go 全 FAIL（动态恢复结构性失效 + 范围扩展无 + 稳态 BER +0.02dB 不够格）
- Kill2（前馈 A≈C）结构性成立——**根因是前馈架构砍掉 [79] 闭环环路惯性**

**方向定夺**（D003）：
- 不 Kill B2-Q2
- 放松前馈化（D002）—— 阶段 0.3 INVARIANT 降级为可推翻的设计选择
- 加 power-boosted pilot —— 解 fade 块 pilot SNR 低的物理问题
- 精读 D006 后修正：[79] 式闭环 hold（功率阈值 gate + 环路 TF 不感知湍流）**严格说不撞 D006**

**已登记决策**：
- D002（前馈化降级 + D006 边界精读修正）
- D003（救援路线四步重设计 + 3 诚实风险）

## 下一步干什么（阶段 1.5 重设计）

**四步重设计**（守 3 步上限，本轮工作对话建议拆 2 步）：

### 步骤 1：阶段 0.3 重定性 + 0.4 重审（架构 + 公平对照）

1. **0.3 重定性闭环 hold 机制**：
   - 设计 [79] 式闭环 freeze 的具体实现（tracking loop + 功率阈值 gate）
   - 决策：完全 hold（fade 期不更新环路）vs partial hold + pilot 微调（fade 期用 power-boosted pilot 辅助环路）
   - D006 不撞论证：门控用信号功率 P < γ_th（不用相位 φ_T）+ 环路 TF 固定不感知湍流
   - 产出更新 `_architecture_decision.md`（闭环版）

2. **0.4 重审公平对照**：
   - power-boost 策略决策：全帧固定 power-boost（简单但 overhead 大）vs 仅 fade 期自适应（复杂但 overhead 小）
   - power-boost overhead 理论预期：3dB boost → overhead 0.26-0.64dB（取决于策略），写进 fair_comparison_framework
   - fair gain 阈值重新审视：救援版 fair gain 需 >0.5dB @ HD-FEC（D005 + INVARIANT 13）

### 步骤 2：阶段 0.5 加参数 + 重跑 sandbox

3. **0.5 加参数**：
   - B2Params 扩 `power_boost_factor`（3dB? 6dB? 文献溯源——DVB-S2 pilot 功率增强参考）
   - 加闭环环路参数（环路带宽 / noise variance / hold 机制参数）—— 文献溯源 [79] / 经典 DPLL 文献
   - 守 TL-26：每个新参数标文献来源，禁拍参数

4. **重跑 sandbox**（闭环版三方对照）：
   - A 闭环 freeze [79]（闭环 tracking loop + 功率阈值 gate hold）
   - B 闭环 power-boost pilot 全程（da_ml + power-boosted pilot）
   - C B2-Q2 闭环双模（非fade 闭环 blind / fade 闭环 power-boosted pilot）
   - 守 V2 三方 + V3 祖师爷（[79] 闭环 freeze 实现一致性核查）+ V5 主线独立重算

## 纪律（和下一步直接相关的约束）

1. **D006 边界已精读修正**（D002）：[79] 式闭环 hold（功率阈值 gate + 环路 TF 不感知湍流）**不撞 D006**。但仍禁 Q12/B1 式"把 φ_T 当算法状态"。设计闭环时门控必须用功率不用相位
2. **3 个诚实风险必须跟踪**（D003）：
   - 风险 1 power-boost overhead trade-off：3dB boost 降估计噪声但 overhead 涨，net 能否 >0 需 MVE 实测
   - 风险 2 跟 [79] baseline 差异够格：救援版 vs [79] 完全 hold 的差异需够 D005（赢几 dB）
   - 风险 3 sat.1553 口径：不能引 sat.1553 L440 +1dB（口径错位，阶段 0.2 已确认），增量独立 MVE
3. **守 TL-26 参数溯源**：power_boost_factor + 环路参数必须标文献来源（[79] / DVB-S2 / 经典 DPLL），禁拍
4. **守 TL-13 共用信道**：闭环版仍从 `common/_channel.py` 导入，禁自建信道
5. **守 sim-preflight v1.3.0**：V2 三方 + V3 祖师爷（[79] 闭环 freeze 实现严格）+ V5 主线独立重算
6. **若闭环版 sandbox 仍 FAIL**（三 Go 仍全 FAIL）：回主控对话重新评估 Kill。救援路线不是无限救援，power-boost 后仍不够格则 Kill

## 接口变更（代码改动，预声明）

阶段 1.5 重设计将新增/修改（仍在 explore 私有 `_` 前缀，不污染 common）：

- **新增** `explore/b2-fade-freeze-pilot-fallback/_closed_loop_freeze.py`（闭环 freeze 实现，[79] 式 tracking loop + 功率阈值 gate）
- **修改** `_sandbox_three_way.py` → `_sandbox_closed_loop_three_way.py`（闭环版三方对照）
- **修改** `_b2_params_draft.py`（加 `power_boost_factor` + 闭环环路参数）
- **新增** `_power_boost_theory.md`（power-boost overhead trade-off 理论预期）
- **不修改** `common/`（4 估计器 + 信道只 import，守 INVARIANT 14）
- **新增依赖**：闭环 tracking loop 可能需新写（common/_recovery.py 4 估计器全前馈，无闭环）—— 若需新写闭环估计器，放 explore 私有，不进 common

## 失败数据附录（前馈版 sandbox，作为救援版对照基准）

### 前馈版三 Go 全 FAIL（闭环版需翻盘的对照）

| 判据 | 前馈版结果 | 闭环版目标 |
|---|---|---|
| Go1 动态恢复 C<A | FAIL（21 点 A_recover==C_recover 全相同）| 闭环版 A 有环路收敛动力学，C 若也闭环则仍 A≈C；**除非 C 用 power-boost pilot 加速收敛** |
| Go2 范围扩展 | FAIL（A/C HD-FEC 可达性一致）| power-boost 可能扩 C 的可达性（低 SNR fade 块 pilot SNR 提升）|
| Go3 稳态 BER fair gain | PARTIAL（+0.02dB，C 微赢但 <<0.5dB）| power-boost 提升 fade 块 pilot 估计精度，可能涨 fair gain |

### fade 块 C(da_ml) vs A(freeze) 直接对照（前馈版，闭环版对照基准）

反推 A_fade_ber（A 全局 = 非fade×340 + A_fade×60 / 400）：
- weak 高 SNR（22-26dB）：C/A = 0.60-0.85（C 赢 A）—— **power-boost 可能扩大这个优势**
- moderate/strong 中高 SNR：C/A = 1.10-1.50（C 输 A）—— **power-boost 需翻盘这个劣势**

### Kill2 物理根因（前馈架构必然，闭环版可解）

前馈架构每块独立估计无环路惯性 → fade→非fade 转换后第一个非 fade 块立即用当前 blind 估计（无收敛过程）→ A/C 非 fade 期 BER 序列完全相同 → N_recover A≈C。

闭环版：[79] 闭环 freeze 有环路 hold 状态，fade 结束后环路从 hold 重新收敛（有惯性）→ N_recover 有意义。**但 C 也闭环的话 C 也有环路惯性，A≈C 可能仍成立**——除非 C 的 power-boost pilot 能加速收敛（这是救援版的核心物理假设，需 MVE）。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| D002 前馈化降级 | 阶段 0.3 INVARIANT | ✅ S004 已降级（D002 登记）| — |
| 闭环 freeze 实现未写 | D003 救援路线 | 🔴 阶段 1.5 步骤 1 需新写 | 本工作对话步骤 1 |
| power-boost 理论预期未算 | TL-20 + D003 风险 1 | 🔴 阶段 1.5 步骤 1 需算 | 本工作对话步骤 1 |
| 闭环参数无文献溯源 | TL-26 | 🔴 阶段 1.5 步骤 2 需查 [79]/DVB-S2/经典 DPLL | 本工作对话步骤 2 |

## 验证阈值（救援版 sandbox 重新定义）

| 验证项 | PASS 标准 | 阈值来源 | 前馈版结果 | 闭环版目标 |
|--------|----------|---------|-----------|------------|
| sandbox 维度 C2 | 非全输（da 赢 blind）| INVARIANT 11 | ✅ PASS | ✅ 保持（不退化）|
| sandbox 动态恢复 | N_recover,C < N_recover,A | 阶段 0.4 核心增量 | ❌ FAIL（前馈 A≈C）| 🎯 **救援核心：闭环 + power-boost 使 C<A** |
| sandbox 范围扩展 | strong 某 OSNR C 可达 HD-FEC 而 A 不可达 | INVARIANT 13 | ❌ FAIL | 🎯 power-boost 可能扩 C 可达性 |
| sandbox 稳态 BER fair gain | ≥0.5dB @ HD-FEC | D005 | ⚠️ PARTIAL（+0.02dB）| 🎯 power-boost 提升 fade 块估计精度 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或范围/鲁棒性维度够格 | D005 + INVARIANT 13 | 不进 MVE | 救援版 sandbox PASS 后进 MVE |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（重点新增的 15 D002 修正）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] D002 前馈化降级合理（核查 `_architecture_decision.md` §3.2 + D006 原文 `decisions.md:313-355`，确认 [79] 式闭环 hold 不撞 D006）
  - [ ] sandbox 物理根因（前馈砍环路惯性）—— 核查 `_sandbox_results.json` 21 点 A_recover==C_recover + [79] L33 闭环 freeze 机制
  - [ ] power-boost 是核心物理解（核查 sandbox fade 块 C 输 A 物理根因：fade 块 pilot SNR 低 → da_ml 估计噪声大）
- [ ] 已检查 D003 救援路线 3 风险（power-boost overhead / 跟 [79] 差异够格 / sat.1553 口径）
- [ ] 已确认当前范围未违反"明确不含"（仍在 explore 私有，不污染 common）

## 下一轮

**阶段 1.5 重设计（2 步，守 3 步上限）**：
- 步骤 1：0.3 重定性闭环 hold + 0.4 重审公平对照（power-boost 策略 + overhead 理论预期）
- 步骤 2：0.5 加参数（power_boost_factor + 闭环环路参数，文献溯源）+ 重跑 sandbox（闭环版三方对照）

**若步骤 2 sandbox 仍 FAIL**（三 Go 仍全 FAIL）：回主控对话重新评估 Kill。救援路线有 3 风险（power-boost overhead / 跟 [79] 差异 / 口径），若都过不了则 B2-Q2 真 Kill。
