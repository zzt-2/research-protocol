# 通信领域 AI 辅助研究协议 v2

> 适用对象：AI agent（Claude / Gemini / GPT 等）
> 研究领域：通信（卫星通信、信道预测、随机接入、自适应编码调制等）
> 纯 Python 技术栈：仿真、DL 训练、数据处理、可视化全部 Python

---

## 协议结构

```
research-protocol/
├── overview.md          # 本文件：协议总览 + 核心规则
├── domain-comms.md      # 通信领域定制（指标、仿真、反模式、多模型）
├── stages/
│   ├── groundwork.md    # Groundwork 执行手册
│   ├── gw-search.md     # Step 1: 文献检索
│   ├── gw-acquire.md    # Step 2: 论文获取
│   ├── gw-read.md       # Step 3: 文献精读
│   ├── gw-feasibility.md # Step 4a+4b: 方向可行性预判（分两段）
│   ├── gw-validate.md    # Step 5: Baseline 候选选定
│   ├── gw-experiment.md # Step 6-7: 仿真器设计 + Baseline 复现
│   ├── contract.md      # Contract 执行手册
│   ├── execute.md       # Execute 执行手册
│   ├── thesis-materials.md # 学位论文：§0 章节方向决策 + §1-§5 材料准备
│   └── paper-materials-workflow.md # 论文素材提取工作流（通用版）
├── templates.md         # 文档模板集
├── tools-guide.md       # 工具链指南
└── tools-scenarios.md   # 工具使用场景速查
```

| 文件 | 职责 | 何时读 |
|------|------|--------|
| `overview.md` | 协议身份、核心原则、文档系统、变更分级、上下文管理 | 每个新对话必读 |
| `stages/groundwork.md` | Groundwork 7 步执行流程 | Groundwork 阶段 |
| `stages/contract.md` | Contract 7 步执行流程（Step 0-6） | Contract 阶段 |
| `stages/execute.md` | Execute 7 步执行流程（Step 0-6） | Execute 阶段 |
| `stages/thesis-materials.md` | 学位论文材料准备：章节方向决策 + 多子问题组织 + 材料包清单 + 记录钩子 | ≥2 方向完成 GW Step 4 时读 §0；准备论文时读 §1-§5 |
| `stages/paper-materials-workflow.md` | 论文素材提取工作流（通用版） | 提取 paper_materials 时 |
| `domain-comms.md` | 通信领域定制内容 | 通信领域研究必读 |
| `templates.md` | contract / decision_log / experiment_result / literature_notes 模板 | 创建/填写文档时读 |
| `tools-guide.md` | 搜索、下载、内容处理工具链 | 使用工具时读 |

---

## 三阶段模型

```
Groundwork ──→ Contract ──→ Execute
(铺垫)         (冻结)       (执行)

↩ 可回退        ↩ 高成本回退   ↩ 禁止回退（仅追加）
```

阶段设计理由：通信研究的自然节奏是"先跑通 baseline → 冻结假设 → 执行验证"。Baseline 复现是 Groundwork 的硬性完成条件。

| 阶段 | 目标 | 核心产出 | 人介入 |
|------|------|---------|--------|
| Groundwork | 建立可靠研究起点 | literature_notes + baseline_report + decision_log | 覆盖面缺口确认、baseline 确认、仿真器设计确认、完成审查 |
| Contract | 冻结经验证的假设和实验方案 | contract.md + data-flow.md + parameter_provenance | **最关键**：冻结前必须用户确认 |
| Execute | 按 Contract 执行实验 | results/*.md | FAIL/MARGINAL 判定时 |

---

## 核心原则

### Context Is all You Need

上下文被污染后模型能力系统性塌陷。[MUST] 遵守上下文隔离规则（见"上下文管理策略"）。主线程不做杂活——文献调研、baseline 复现、实验执行全部隔离到子 agent 或独立对话。

### Baseline-first

Baseline 是后续一切判断的锚点。[MUST] Groundwork 完成至少一个 baseline 复现，不可跳过。没有 baseline 的比较没有意义。"从零开始写代码效果一定很差"（社区经验）。

### Human-in-the-loop

AI 的优势是效率，不是创新。人定义问题，AI 验证问题。[MUST] 在人介入点停止执行并等待用户确认。实验执行、结果记录、技术实现细节——agent 自主。

### 单一事实源

每种信息只在一个文档中"拥有"，其他文档只引用。

| 信息类型 | 唯一拥有者 |
|---------|-----------|
| 假设 + 实验方案 | contract.md |
| 参数溯源 | contract.md §parameter_provenance |
| 端到端数据流 | data-flow.md |
| 决策及理由 | decision_log.md |
| 实验数据 + 结果 | results/*.md |
| 文献记录 | literature_notes.md |
| Baseline 信息 | baseline_report.md |
| 方向可行性评估 | feasibility_report.md |

### 方向验证先行

新颖性 ≠ 可行性。"没人做过"不等于"值得做"。[MUST] 在投入仿真器搭建和 baseline 复现前，通过结构优势论证、仿真条件推理和最小可行实验验证方向可行性（`stages/gw-feasibility.md`）。Go/No-Go 决策经用户确认后方可继续。

---

## 文档系统

### 核心文档（协议强制）

| 文档 | 生命周期 | 约束 |
|------|---------|------|
| `contract.md` | Contract 阶段创建，之后不可变 | ≤100 行 |
| `decision_log.md` | 全程追加，支持 SUPERSEDED | 单条 ≤3 行 |
| `results/*.md` | Execute 阶段产出，完成后冻结 | 每个 ≤80 行 |

### 辅助文档（按需创建）

| 文档 | 何时创建 |
|------|---------|
| `literature_notes.md` | Groundwork 阶段 |
| `baseline_report.md` | Groundwork 阶段 |
| `interaction_log.md` | 全程追加 |

---

## 变更分级

```
IF 变更涉及 contract 中任何字段 → 高风险
IF 仿真环境修改导致核心方法 vs baseline 差距增大 → 高风险
OTHERWISE → 低风险
```

**低风险**：agent 自决 + decision_log 追加 `[AUTO]` 标记。

**高风险**：[MUST] 停止执行 → 生成变更提案 → 等待用户确认。变更提案格式（内嵌 decision_log）：

```
[D{序号}][CHANGE-PROPOSAL] {变什么} | 理由: {为什么} | 影响: {哪些结果会作废} | 用户决定: {留空}
```

Contract 的特殊效力见 `stages/contract.md` 末节（不可修改、变更提案格式、例外处理）。

---

## 上下文管理策略

### 隔离规则

| 活动 | 执行方式 | 理由 |
|------|---------|------|
| 文献调研（搜索+精读） | 子 agent 或独立对话 | 文献全文量大，稀释主线程 |
| Baseline 复现 | 子 agent 或独立对话 | 环境配置和调试日志是上下文杀手 |
| 实验执行 | 子 agent 或后台任务 | 长时间运行的输出不适合占主线程 |
| 结果分析 | **主线程** | 需要全量上下文做综合判断 |
| 决策 + Contract | **主线程** | 研究者的核心价值环节 |

### 状态交付

子 agent / 独立对话通过文件系统交付：

- 文献调研 → `literature_notes.md`（摘要级，不喂全文）
- Baseline 复现 → `baseline_report.md`（结果 + 关键代码路径）
- 实验执行 → `results/*.md`（结果 + 数据）

主线程只读摘要，不读原始输出。

### 压缩/续接后的强制重读

上下文压缩（`/compact`）或跨对话续接后，以下文件必须重新读取，不能用"之前读过"或"大概记得"替代：

1. 当前阶段的 stage 文件（如正在 Groundwork Step 5 → 读 `gw-validate.md`）
2. `decision_log.md`（最新决策状态）
3. `projects/{name}/sessions/` 下最新的 handoff 文件（如有）

判定标准：本轮上下文里没有新鲜的阅读证据（如本轮明确读过对应文件），视为未读，必须补读后才能继续规划或实施。
