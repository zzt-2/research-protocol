# Groundwork（铺垫）

> 建立可靠的研究起点。
> 通信领域研究：额外阅读 `domain-comms.md`。

## 目标

理解领域、找到并精读核心论文、交叉验证选定 baseline、设计仿真器、复现 baseline。

## 输入 / 输出

- **输入**：用户的研究方向描述
- **输出**：`literature_notes.md` + `baseline_report.md` + `decision_log.md`

## 步骤编排

| 步骤 | 职责文件 | 产出 | 人介入 |
|------|---------|------|--------|
| Step 1 | [gw-search.md](gw-search.md) | search-archive/{date}/{slug}.json + 候选列表 | 否 |
| Step 2 | [gw-acquire.md](gw-acquire.md) | papers/{arxiv|doi}/{id}/content.md + 覆盖面缺口报告 | 是（缺口确认）|
| Step 3 | [gw-read.md](gw-read.md) | literature_notes.md（含 2-3 篇标杆论文写作架构提取） | 否 |
| Step 3.5 | [gw-supplement.md](gw-supplement.md) | 补充论文 + 更新 literature_notes | 否 |
| Step 4a | [gw-feasibility.md](gw-feasibility.md) §4a | feasibility_report.md（A/B/D 维度） | 是（方向+可行性 Go/No-Go）|
| Step 5 | [gw-validate.md](gw-validate.md) | Baseline 候选评估表 | 是（Baseline 确认）|
| Step 4b | [gw-feasibility.md](gw-feasibility.md) §4b | feasibility_report.md（C/E 维度） | 是（执行可行性 Go/No-Go）|
| Step 6 | [gw-experiment.md](gw-experiment.md) §sim | 仿真器设计规格 | 是（设计确认）|
| Step 7 | [gw-experiment.md](gw-experiment.md) §impl | baseline_report.md | 否 |

> **步骤依赖**：Step 4a（方向根基）在 Step 5 前执行，因为 Go/No-Go 决策应先于 Baseline 投入。
> Step 4b（仿真条件）在 Step 5 后执行，因为需要 Baseline 的具体参数来评估仿真可行性。
> 如果 Step 4a 结论为 No-Go，则项目终止，不执行 Step 5 及后续。

## Step 3.5：定向补充检索（必做）

完整定义见 [gw-supplement.md](gw-supplement.md)。

Step 3 精读完成后**必须执行**。用精读产生的新认知做一轮定向检索，弥补初始搜索的盲区。该步骤必须在子 agent 中执行上下文密集型操作（见 CLAUDE.md "上下文管理规则"）。

## 共享规则

### 方法类型标注 [FR-07]

框架中的研究类型相关规则使用以下标签标注适用范围：

| 标签 | 含义 | 典型规则 |
|------|------|---------|
| `[DRL]` | 仅适用于深度强化学习方向 | 奖励函数审查、MDP 试运行、状态/动作/奖励结构化提取 |
| `[监督]` | 仅适用于监督/自监督学习方向 | 训练数据构造、损失函数选择 |
| `[优化]` | 仅适用于纯优化方向 | 约束建模、求解器选择 |
| `[通用]` | 所有方向都适用 | 文献检索、Go/No-Go 决策、仿真器验证 |

Agent 进入新方向时，先确认方法类型。遇到不适用的标签规则时跳过，并在 `decision_log.md` 记录跳过原因。当前框架中 DRL 相关规则最多（奖励函数审查 `domain-comms.md` §1.5、MDP 试运行 `groundwork.md` S6、状态/动作/奖励提取 `gw-read.md`），非 DRL 方向不应被迫执行这些步骤。

### 步骤完成标记（FR-22 执行载体）

每个步骤完成时，**必须同步更新两处进度表**：

1. `literature_notes.md` 的步骤进度表（⬜→✅ + 日期 + commit hash）
2. `master-state.md` 的 `## GW Progress` 表（见 `templates/master-state-template.md`，跨阶段权威）

两处必须一致，冲突时以 master-state.md 为准。

### 跨 Step 硬门控（FR-22）

> 设计意图：Groundwork 各 Step 原本只靠 markdown 进度表标记完成，跨 Step 无硬门控——agent 可以在早期 Step 全未完成时，跳过精读和可行性判断直接跑去试方法，结果反复撞物理天花板把方向做死。本节把"进下游前先查进度"做成硬门控。

**[MUST] 进入任何下游步骤前，先查 master-state.md 的 GW Progress 表**：

- 上游任一项 ⬜ = **禁止进入下游**。
- **Step 3（精读）和 Step 4a（可行性 Go/No-Go）是硬门，不可跳过**。
- literature_notes 进度表 / master-state GW Progress 任一 Step 2/3/3.5/4a 为 ⬜ 时，**禁止进 MVE / Contract / 任意"试新方法/新方向"动作**。
- 进 Step 4a 额外要求：literature_notes 研究问题清单至少含 1 条四判据全过的 Q#（gw-feasibility §A0 §0 会再查一次）。

**唯一窄例外：Research Direction Lab 的 `PREFORMAL_METHOD_FACTORY`。**
只有在 method-producing mission 无 active scientific carrier，且当前 remap
同时为 `READY=0 / NEEDS_SMALL_ADAPTER=0` 时，才可按
`.agents/skills/research-direction-lab/references/method-production.md` 运行。
它必须复用已验证的共享测试床与传统 baseline，只能使用 diagnostic seeds，
并且只产生诊断信号；**不算 MVE、不完成任何 GW Step、不产生 Go/Kill 或论文
结论**。任何 winner 都必须从 Step 1 返回并补齐 Step 1–3/3.5/4a，之后才能做
正式实验。不得借此重开已明确 rejected 的轴，也不得把单候选 formalization
改名为方法工厂。

> **跳步识别信号**：候选的论证起点是"标题联想"（如"PCS 能不能提升""交织能不能省东西"）而非 GW Step 4a 维度 A0 的产物（某个过四判据的 Q#）→ 一定跳了 Step 3-4a，**禁止开跑**。判断"现在在 GW 哪一步"时，以 master-state.md GW Progress 表为准，不靠记忆。

### 环境检查

运行任何脚本前，确认 Python 环境（详见 gw-acquire.md）。

### 止损

下载和实现均有止损规则，分别见 gw-acquire.md 和 gw-experiment.md。

### 文件传递协议

各步骤通过文件路径传递数据，不依赖上下文记忆：
- Step 1 → Step 2：`search-archive/{date}/{slug}.json`
- Step 2 → Step 3：`papers/{arxiv|doi}/{id}/content.md`
- Step 3 → Step 3.5：`literature_notes.md`（综合分析中的新发现 → 定向检索词）
- Step 3.5 → Step 4a：更新后的 `literature_notes.md`
- Step 4a → Step 5：`feasibility_report.md`（A/B/D 维度）+ `decision_log.md`
- Step 5 → Step 4b：Baseline 候选评估表 + `decision_log.md`
- Step 4b → Step 6：`feasibility_report.md`（C/E 维度补完）+ `decision_log.md`
- Step 6 → Step 7：仿真器设计规格（见 gw-experiment.md）

## 完成条件

- [ ] literature_notes.md 包含 ≥8 篇核心文献，且有交叉验证数据（≥5 为单步质量门槛，≥8 为 Groundwork 整体完成门槛）
  > 5 篇为 Step 3 单步通过门槛（见 gw-read.md），8 篇为 GW 整体完成门槛。Step 3.5 补充检索后通常可达 8+。不足时返回 Step 3.5。
- [ ] literature_notes.md 综合分析包含"研究背景概述"（领域脉络+核心挑战+研究定位）
- [ ] 每篇精读条目包含"适配性分析"字段（适配点/不适配点/改进方向）
- [ ] feasibility_report.md 已创建，Go/No-Go 决策已记录并经用户确认（Step 4 产出）
- [ ] 仿真器设计规格经用户确认（Step 6 产出）
- [ ] baseline_report.md 包含仿真器验证通过 + 至少 1 个成功复现的 baseline

**人介入**：[MUST] 用户审查全部 Groundwork 产出后方可进入 Contract 阶段。
