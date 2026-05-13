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
| Step 3 | [gw-read.md](gw-read.md) | literature_notes.md | 否 |
| Step 3.5 | 定向补充检索（见下方） | 补充论文 + 更新 literature_notes | 否 |
| Step 4a | [gw-feasibility.md](gw-feasibility.md) §4a | feasibility_report.md（初步） | 是（方向根基 Go/No-Go）|
| Step 5 | [gw-validate.md](gw-validate.md) | Baseline 候选评估表 | 是（Baseline 确认）|
| Step 4b | [gw-feasibility.md](gw-feasibility.md) §4b | feasibility_report.md（完整） | 是（执行可行性 Go/No-Go）|
| Step 6 | [gw-experiment.md](gw-experiment.md) §sim | 仿真器设计规格 | 是（设计确认）|
| Step 7 | [gw-experiment.md](gw-experiment.md) §impl | baseline_report.md | 否 |

## Step 3.5：定向补充检索（必做）

Step 3 精读后，对方向的理解远深于 Step 1 构造关键词时。用新认知做一轮定向检索，弥补初始搜索的盲区。

### 触发条件（始终满足）

精读完成后**必须执行**，不需额外判断。典型场景：
- 精读论文 related work/reference 中出现高度相关但未收录的论文
- 综合分析发现新的技术子方向，当前候选池未覆盖
- 竞品分析发现新的直接竞争者
- 方向收窄后，需要更精确的检索词覆盖特定方法/场景

### 操作

1. 从精读发现中提炼**定向检索词**（比 Step 1 更精确，如从 "DRL RIS" 收窄到 "DDPG phase shift RIS MISO"）
2. 用 `tools/search --find-similar` 或 `--citations` 定向补充（参见 tools-scenarios.md S3/S4），或用精确关键词重搜
3. 新结果 `--merge` 到已有搜索结果
4. 新论文走 gw-acquire → gw-read（精读或浅读）

### 终止条件

连续一轮未发现新的高相关论文（低于"建议读"门槛）。上限 3 轮。每轮更新 literature_notes.md 综合分析。

## 共享规则

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
- Step 4a → Step 5：`feasibility_report.md`（初步）+ `decision_log.md`
- Step 5 → Step 4b：Baseline 候选评估表 + `decision_log.md`
- Step 4b → Step 6：`feasibility_report.md`（完整）+ `decision_log.md`
- Step 6 → Step 7：仿真器设计规格（见 gw-experiment.md）

## 完成条件

- [ ] literature_notes.md 包含 ≥8 篇核心文献，且有交叉验证数据（≥5 为单步质量门槛，≥8 为 Groundwork 整体完成门槛）
- [ ] feasibility_report.md 已创建，Go/No-Go 决策已记录并经用户确认（Step 4 产出）
- [ ] 仿真器设计规格经用户确认（Step 6 产出）
- [ ] baseline_report.md 包含仿真器验证通过 + 至少 1 个成功复现的 baseline

**人介入**：[MUST] 用户审查全部 Groundwork 产出后方可进入 Contract 阶段。
