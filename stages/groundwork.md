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
| Step 3 | [gw-read.md](gw-read.md) | literature_notes.md | 否（可触发迭代） |
| Step 4 | [gw-feasibility.md](gw-feasibility.md) | feasibility_report.md | 是（Go/No-Go）|
| Step 5 | [gw-validate.md](gw-validate.md) | Baseline 候选评估表 | 是（Baseline 确认）|
| Step 6 | [gw-experiment.md](gw-experiment.md) §sim | 仿真器设计规格 | 是（设计确认）|
| Step 7 | [gw-experiment.md](gw-experiment.md) §impl | baseline_report.md | 否 |

## 迭代检索

Step 1→2→3 是基础线性流程。当 Step 3 精读后发现以下情况时，触发迭代：

- 精读论文 related work/reference 中出现高度相关但未收录的论文
- 综合分析发现新的技术子方向，当前候选池未覆盖
- 竞品分析发现新的直接竞争者

迭代操作：
1. `tools/search --find-similar` 或 `--citations` 定向补充（参见 tools-scenarios.md S3/S4）
2. 新结果 `--merge` 到已有搜索结果
3. 新论文走 gw-acquire → gw-read（精读或浅读）

终止条件：连续一轮未发现新的高相关论文（低于"建议读"门槛）。上限 3 轮。每轮更新 literature_notes.md 综合分析。

## 共享规则

### 环境检查

运行任何脚本前，确认 Python 环境（详见 gw-acquire.md）。

### 止损

下载和实现均有止损规则，分别见 gw-acquire.md 和 gw-experiment.md。

### 文件传递协议

各步骤通过文件路径传递数据，不依赖上下文记忆：
- Step 1 → Step 2：`search-archive/{date}/{slug}.json`
- Step 2 → Step 3：`papers/{arxiv|doi}/{id}/content.md`
- Step 3 → Step 4：`literature_notes.md`
- Step 4 → Step 5：`feasibility_report.md` + `decision_log.md`
- Step 5 → Step 6：Baseline 候选评估表 + `decision_log.md`
- Step 6 → Step 7：仿真器设计规格（见 gw-experiment.md）

## 完成条件

- [ ] literature_notes.md 包含 ≥8 篇核心文献，且有交叉验证数据（≥5 为单步质量门槛，≥8 为 Groundwork 整体完成门槛）
- [ ] feasibility_report.md 已创建，Go/No-Go 决策已记录并经用户确认（Step 4 产出）
- [ ] 仿真器设计规格经用户确认（Step 6 产出）
- [ ] baseline_report.md 包含仿真器验证通过 + 至少 1 个成功复现的 baseline

**人介入**：[MUST] 用户审查全部 Groundwork 产出后方可进入 Contract 阶段。
