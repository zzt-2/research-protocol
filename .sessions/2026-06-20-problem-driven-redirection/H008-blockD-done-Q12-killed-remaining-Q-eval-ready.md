# Handoff: 块D完成 + Q12 Step4a评估=Kill，剩余Q#评估就绪

> 来源: S015+S016(块D) + 本轮Q12评估 | 交接目标: 下一个对话继续Step 4a评估剩余Q#
> 日期: 2026-06-27
> 文件名: H008-blockD-done-Q12-killed-remaining-Q-eval-ready.md

## 到哪了（状态）

**块 D Step 3.5 完成** + **块 E Step 4a 启动，Q12 评估=Kill**。

- Step 3.5 ✅（master-state 已更新）：检索+召回+Paillier JLT 精读完成，Q# 清单 Q1-Q13
- Step 4a 🔄进行中：**Q12 评估完成=Kill（D006）**，feasibility_report.md 已建（DSP 适配版）

### 🔴 Q12 Kill 的核心教训（对剩余 Q# 评估最重要）

**Q12 高度同构被证伪的旧 B1（湍流感知 Kalman CPR），是 B1 换皮。** Q12 用环路传递函数，旧 B1 用 KF，但**物理假设完全相同**（都假设主动建模湍流相位带来同步增益）。旧 B1 已被 S024 KF 压力测试证伪（增益消失 0/-0.7/-2.5dB + B2 消融证明增益来自跟踪而非湍流感知）。

**对剩余 Q# 的纪律（每个 Q# 都要做 B1 换皮核查）**：
1. 评估每个 Q# 前先查 thesis-direction-pivot/ 有无同构方向被证伪
2. Kill 理由要诚实——D005 务实路线救不了"赢不了传统 baseline"的方向（Q12 连 Paillier 分治 DPLL 都赢不了）

## 下一步干什么

**继续 Step 4a 评估剩余 Q#**，建议优先级：
1. **Q8（PCS+Rs 治 Doppler）**——同门范式最浓，增益 ~100Gbps 硬，但增益来自 Rs 非 PS
2. **Q1（TS-KF 两阶段解耦 Doppler）**——四判据全过
3. **Q7（两阶段 CFE）**——四判据全过

**评估流程（DSP 适配版，用户拍板）**：
- 读 `projects/thesis-fso/feasibility_report.md`（Q12 评估是模板）
- 跳过 ML 专用项（A0§2 问题结构适配/§3 跨域 ML 先例/§4 MDP 非平凡性 + 维度 D DRL 先验对照）
- 保留：A0§0（问题合法性）/§1（性能间隙）/§5（负面证据搜索，**最重要**）/§6（先验覆盖）+ 维度 A（结构优势）/B（空白零假设，**致命项**）/C（仿真条件）/E（资源风险）
- 每个 Q# 必做：① B1 换皮核查（查 thesis-direction-pivot/）② D005 务实标准（赢传统 baseline 几 dB）③ 四判据不可放水

**Step 4a 前必读**：gw-feasibility.md（本轮已读，DSP 适配版）/ TL-30/31（FR-22/24）/ decisions.md D005（务实 INVARIANT）+ D004-c（FR-26）/ D006（Q12 Kill 教训）。

## 纪律（和下一步直接相关的约束）

1. **D005 务实路线 INVARIANT**：Go=赢传统未优化 baseline 几 dB。FR-21 oracle 上界降为参考不当 Kill 门。FR-25 Go/Kill 对手标准分离
2. **B1 换皮核查（本轮 Q12 教训）**：每个 Q# 评估前必查 thesis-direction-pivot/ 有无同构方向。Q12 就是因为没查漏了"旧 B1 已证伪"才走到 Step 4a 才 Kill（如果块 D 召回时就查，能更早 Kill）
3. **维度 B 空白零假设是致命项**：3 个结构性原因都暗示方法冗余 → Kill。这是 Q12 Kill 的关键维度
4. **四判据不可放水**（topic-index 不变量 3）
5. **FR-26 证据链**：声称必附证据指针

---
## 接收方验证（续接对话时必须完成）
- [ ] 已读取 topic-index 不变量段落（8 条，D005 务实路线最高优先级）
- [ ] 已验证至少 3 条关键事实声称：
  - [ ] Q12 Kill 已记录在 decisions.md D006（核查 `grep "## D006" .sessions/2026-06-20-problem-driven-redirection/decisions.md`）
  - [ ] feasibility_report.md 存在且含 Q12 评估（核查 `ls projects/thesis-fso/feasibility_report.md` + grep Q12）
  - [ ] master-state Step 4a = 🔄 进行中 + Q12 Kill（核查 `grep "4a feasibility" projects/thesis-fso/master-state.md`）
- [ ] 已检查 _registry.yaml depends_on/conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 3 篇论文下不到（Rustum2026/Tang2024/Mosnier2025）| Step 3.5 补充 | SPIE/IET 非 OA 确认下不到 | 块 E 按需（Rustum DL 对比/Tang[50]核对读新2原文 references）|
| H004 选样漏召根因 | D003 多候选不应路径过滤 | 已纠正 Q11-Q13 召回，根因（选样无历史资产召回步骤）未修流程 | 下次选样加检查步骤 |
| **B1 换皮核查应前置**（Q12 教训） | 块 D 召回时就该查 thesis-direction-pivot | Q12 走到 Step 4a 才 Kill（本可块 D 就 Kill） | 下次召回/评估前先查旧方向 Kill 记录 |

## 下一轮

1. 读 H008 + feasibility_report.md（Q12 模板）+ D006（Q12 Kill 教训）
2. 评估 Q8（PCS+Rs 治 Doppler）：先查 thesis-direction-pivot 有无 PCS/Rs 同构方向被 Kill + 维度 B 空白零假设 + D005 务实标准
3. 若 Q8 Go → Q1/Q7 继续评；若 Q8 Kill → Q1/Q7 优先。至少 1 个 Q# Go 才进块 F（Step 5-7 baseline 复现）
