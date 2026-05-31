# [H013] 创建跨项目状态汇总

## 背景

目前有多个并行推进的研究项目（leo-gnn-routing、leo-isl-scheduling-drl、leo-beam-hopping-gnn、hgat-dag-offloading、ris-phase-drl 等），分散在不同对话中推进。缺乏一个统一的项目状态视图，导致：

- 选新方向时无法快速参考已有项目的教训
- 设计 baseline/仿真器时重复犯同类错误
- 跨对话恢复时需要读多个 handoff 才能了解全局
- 跨项目共性问题（如"6 个项目全缺 early stopping"）没有汇总机制

## 任务

创建根目录 `projects-overview.md`，汇总所有研究项目的状态、关键结论和跨项目教训。

## 执行步骤

### Step 1: 项目发现（派子 agent 并行检查）

派 explore 子 agent 逐一检查 `projects/` 下每个子目录，每个 agent 负责 2-3 个项目，收集：

1. **decision_log.md** — 读阶段摘要行和最新决策
2. **feasibility_report.md** — 如存在，读结论段
3. **baseline_report.md** — 如存在，读评估结果
4. **.sessions/_-{project}/HANDOFF-_.md** — 读最新 handoff
5. **simulator/ 目录** — 如存在，说明已进入实现阶段
6. **results/ 目录** — 如存在，看有哪些结果文件
7. **git log** — 最近 3-5 个 commit 了解进度

每个子 agent 返回结构化摘要：

```
项目名: xxx
方向: 一句话描述
状态: active / archived / completed
阶段: GW-StepX / Contract / Execute
关键结论: 1-2 句（成功/失败的根因）
教训: 跨项目可复用的经验
文件完整性: 缺什么重要文件
```

### Step 2: 跨项目教训提取

从所有项目的失败/成功中提取通用经验，按维度组织：

- **方法选择**：什么方法在什么问题上有效/无效（如 BH 的"干扰是物理关系不可学习"）
- **仿真器**：共性问题（如 reward 归一化、参数溯源）
- **训练**：缺失模式（如 early stopping、save/load）
- **baseline**：选型模式（什么类型的 baseline 是领域共识）
- **方向选择**：蓝海判断的实际验证情况（哪些蓝海是真蓝海，哪些是"没人做因为不值得做"）

### Step 3: 使用场景说明

在文档中明确什么场景下应参考本文档：

1. **选新方向前** → 看"方向选择"教训和已有项目覆盖范围
2. **设计 baseline 前** → 看"baseline 选型"模式和同领域项目的 baseline 报告
3. **搭仿真器前** → 读 `code-quality.md` + 看"仿真器"教训
4. **选学习方法前** → 看"方法选择"教训，特别是失败案例
5. **跨对话恢复** → 先读本文件了解全局，再读具体项目 handoff
6. **归档/转阶段时** → 更新本文档对应项目条目

### Step 4: 框架集成

思考并记录以下框架改进建议（不执行，只记录到文档末尾的"待办"段）：

1. **归档时更新**：当 decision_log 标记归档时，应同步更新 projects-overview.md
2. **转阶段时更新**：每次 handoff 写入时，检查是否需要更新 projects-overview 的阶段标记
3. **是否需要 CLAUDE.md 引用**：是否在"状态恢复"段落中加入 projects-overview.md 作为优先读取项

## 输出格式

```markdown
# 项目总览

> 最后更新: YYYY-MM-DD | 活跃项目: X | 已归档: Y | 总计: Z

## 活跃项目

### [项目名]

- **方向**: 一句话
- **状态**: active | 阶段: GW-StepX
- **关键技术**: GNN/DRL/...
- **关键结论**: 1-2 句
- **教训**: 跨项目可复用经验
- **最新 handoff**: `.sessions/.../HANDOFF-XXX.md`

## 已归档项目

（同格式，加归档原因）

## 跨项目教训

### 方向选择

- ...

### 方法选择

- ...

### 仿真器

- ...

### 训练

- ...

## 使用场景

（Step 3 的内容）

## 框架改进待办

（Step 4 的内容）
```

## 约束

- 控制在 150 行以内，方便每次对话开头快速扫读
- 只记录框架无法自动获取的信息（代码和 git 可查的不重复记录）
- 重点关注：方向选择理由、方法失败/成功的根因、跨项目模式
- 每个项目不超过 8 行（名称+5个字段+handoff路径）
- 写完后读一遍确认没有遗漏项目（对照 `projects/` 目录和 `MEMORY.md`）
