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

### 步骤完成标记

每个步骤完成时，**必须更新 `literature_notes.md` 的步骤进度表**（将 ⬜ 改为 ✅，填写日期和 commit hash）。跨对话恢复时优先读取此表判断已完成步骤，避免重复执行。

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
