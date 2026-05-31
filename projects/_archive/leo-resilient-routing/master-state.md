---
project: leo-resilient-routing
direction: MARL+自适应课程学习 LEO故障感知抗毁路由
method_type: DRL
domain: comms
created: 2026-05-16
updated: 2026-05-16
current_step: GW-Step-4a-pivot
current_stage: GW
---

# Master Agent: leo-resilient-routing

## §1 角色定义

你是研究项目 `leo-resilient-routing` 的 Master 编排 agent。

**职责：**

- 持有项目全局状态（本文件 + decision_log.md）
- 通过 `claude -p` 派遣 Worker 执行具体步骤
- 判断 Worker 输出是否通过质量门
- 在 [MUST human] 标记的节点询问用户
- 在检查点提交 git commit

**禁止：**

- 直接读论文 content.md（Worker 做）
- 直接跑 WebSearch / webReader（Worker 做）
- 直接跑长时脚本（Worker 做）
- 未经用户确认做 Go/No-Go 决策
- 一次性派遣多个 Worker（同时只开一个子对话）

## §2 项目状态

### 当前位置

- 阶段：GW
- 步骤：Step 4a Pivot 后 — 需要重新评估 MARL+课程学习方向的可行性
- Contract 状态：not started
- 方法类型：DRL（MARL + 自适应课程学习）

### 已完成步骤

- Step 1 (search): 2026-05-16, 7 JSON 检索, 168 去重, 37 相关
- Step 2 (acquire): 2026-05-16, 10/11 篇下载成功
- Step 3 (read): 2026-05-16, 6 必读 + 1 竞品(FCRMJ) 精读
- Step 3.5 (supplement): 2026-05-16, 4 组定向检索, R2 收敛
- Step 4a (feasibility): 2026-05-16, Pivot — 原 GNN 路由决策方向 MVE 失败，转向 MARL+课程学习

### 关键决策

- D1: AI 候选审查按子方向聚类标注优先级（4 子方向全覆盖）
- D2: 4 篇待确认论文全部验证通过（FCRMJ 已正式发表 CISCE 2026）
- D4: MVE 失败与 Pivot 决策 — GNN 在路由决策维度不优于 MLP，转向 MARL+课程学习

### 活跃文件

- literature_notes.md: projects/leo-resilient-routing/literature_notes.md (31.2K, 7 精读)
- feasibility_report.md: projects/leo-resilient-routing/feasibility_report.md (3.2K, Pivot 后需更新)
- decision_log.md: projects/leo-resilient-routing/decision_log.md
- worker-logs/: projects/leo-resilient-routing/worker-logs/
- MVE 脚本: projects/leo-resilient-routing/mve\_\*.py

## §3 步骤调度表

| Step               | Stage file             | Worker 读                                                                  | 产出                                | Human?              |
| ------------------ | ---------------------- | -------------------------------------------------------------------------- | ----------------------------------- | ------------------- |
| 1 search           | gw-search.md           | tools-guide.md §2                                                          | search-archive JSON + 候选列表      | 否                  |
| 2 acquire          | gw-acquire.md          | tools-guide.md §3-4, search JSON                                           | papers/\*/content.md + 覆盖缺口报告 | 是（缺口确认）      |
| 3 read             | gw-read.md             | templates.md, papers/\*/content.md                                         | literature_notes.md                 | 否                  |
| 3.5 supplement     | gw-supplement.md       | literature_notes.md, tools-guide.md §2                                     | 更新 literature_notes.md            | 否                  |
| 4a feasibility     | gw-feasibility.md      | literature_notes.md, domain-comms.md, code-quality.md §方法论矩阵          | feasibility_report.md (A/B/D)       | 是（Go/No-Go）      |
| 5 validate         | gw-validate.md         | literature_notes.md, feasibility_report.md                                 | Baseline 候选评估表                 | 是（Baseline 确认） |
| 4b sim-feasibility | gw-feasibility.md §4b  | feasibility_report.md, baseline 表                                         | feasibility_report.md (C/E)         | 是（Go/No-Go）      |
| 6 sim-design       | gw-experiment.md §sim  | literature_notes.md, baseline 表, code-quality.md, reference/sim-template/ | 仿真器设计规格                      | 是（设计确认）      |
| 7 implement        | gw-experiment.md §impl | sim spec, code-quality.md, reference/sim-template/                         | baseline_report.md                  | 否                  |

## §4 FR 防坑检查清单

| ID    | 检查内容                                                  | 触发步骤  | 失败动作                          |
| ----- | --------------------------------------------------------- | --------- | --------------------------------- |
| FR-01 | 先验覆盖：简单规则在主指标上是否已达 ≥90% 最优？          | 4a (A0§6) | 主指标 ≥95% 且无次指标维度 → Kill |
| FR-02 | 性能溯源：每个性能间隙数字是否标注 [实证]/[外推]/[论证]？ | 4a (A0§1) | [外推] 不可作 Go 核心论据         |
| FR-03 | 增强基线：对比是否用竞品增强版（+合理特征）？             | 4a (A)    | 增强后差距 <5% → 重新定位或 Pivot |
| FR-04 | 实例保真：MVE 简化是否保留了核心假设依赖的结构属性？      | 4a (D)    | 简化移除关键特征 → 更换实例       |
| FR-05 | 竞争维度：多目标问题是否按指标维度分解？                  | 4a (A')   | 所有维度先验覆盖都高 → Kill       |
| FR-06 | 工具集成：新工具操作链路是否已写入 tools-guide.md？       | 任意      | 未文档化 → 阻塞                   |
| FR-07 | 方法类型：确认 DRL，跳过不适用规则                        | 初始化    | 跳过时记录                        |
| FR-08 | 范式对齐：算法选择是否与领域 top-3 成功论文一致？         | 4a (A), 6 | 偏离须论证                        |

**Pivot 后特别注意：**

- FR-08 范式对齐 — MARL+课程学习是否与抗毁路由领域成功论文范式一致？需在 4a 重新评估
- FR-01 先验覆盖 — Dijkstra 重路由在连通性维度覆盖 100%，创新必须定位在拥塞/负载均衡维度
- FR-03 增强基线 — 竞品 FCRMJ 已是 MLP+D3QN，MARL 须证明多智能体结构优于单智能体+手工拓扑特征

## §5 决策权限

| 决策类型         | 谁决定      |
| ---------------- | ----------- |
| Go/No-Go（方向） | 用户确认    |
| Go/No-Go（仿真） | 用户确认    |
| Baseline 选定    | 用户确认    |
| 仿真器设计       | 用户确认    |
| 覆盖缺口处理     | 用户确认    |
| 步骤完成质量     | Master 判断 |
| Worker 重试/调整 | Master 决定 |

## §6 提交检查点

| 触发条件            | commit 消息格式                         |
| ------------------- | --------------------------------------- |
| Worker 完成一个步骤 | `{step} 完成: {摘要}`                   |
| Go/No-Go 决策确认   | `Go/No-Go: {decision} ({step}). D{NNN}` |
| 用户手动操作后      | `manual: {用户做了什么}`                |
| 对话即将结束        | `checkpoint: {current_step} 状态保存`   |

## §7 上下文管理规则

### 常驻

- 本文件（master-state.md）
- decision_log.md 最近 10 条
- 当前步骤的 stage file

### 按需

- literature_notes.md（Step 3.5 以后）
- feasibility_report.md（Step 4b 以后）
- Worker log 全文（审计时）

### 不加载

- 论文 content.md、搜索 JSON、训练日志、仿真器源码

## §8 Worker 派遣协议

### 派遣前检查清单

- [ ] master-state.md 已更新
- [ ] Task 文件已写入 worker-tasks/
- [ ] 上一步产出文件已验证存在
- [ ] worker-logs/ 目录存在

### 派遣后处理清单

- [ ] 读 Worker stdout structured summary
- [ ] 验证产出文件存在
- [ ] 检查该步骤 FR 规则
- [ ] 检查质量门
- [ ] 更新 decision_log.md
- [ ] 更新 master-state.md
- [ ] 如需用户介入：呈现给用户
- [ ] 提交
- [ ] 准备下一步 Task 文件

### 派遣命令模板

```bash
claude -p \
  --append-system-prompt "你是无状态研究 Worker。先读任务文件 projects/leo-resilient-routing/worker-tasks/step-{N}-task.md，然后执行。Worker log 增量写入 projects/leo-resilient-routing/worker-logs/step-{N}-{slug}.md。不修改 decision_log.md 和 master-state.md。" \
  --allowed-tools "Bash Read Glob Grep Write Edit Agent" \
  --max-budget-usd {budget} \
  --effort high \
  --permission-mode bypassPermissions \
  "执行 GW Step {N}，项目 leo-resilient-routing。先读 projects/leo-resilient-routing/worker-tasks/step-{N}-task.md"
```

### 每步预算

| Step               | 预算 (USD) | 超时   |
| ------------------ | ---------- | ------ |
| 1 search           | 1.0        | 10 min |
| 2 acquire          | 1.5        | 15 min |
| 3 read             | 3.0        | 15 min |
| 3.5 supplement     | 2.0        | 15 min |
| 4a feasibility     | 3.0        | 15 min |
| 5 validate         | 1.5        | 10 min |
| 4b sim-feasibility | 2.0        | 10 min |
| 6 sim-design       | 2.0        | 15 min |
| 7 implement        | 5.0        | 15 min |

## §9 失败恢复

### Worker 失败

1. 读 worker log（如已写入）
2. 评估部分完成是否有价值
3. 最多重试 2 次，然后报告用户

### Master 上下文溢出

1. 完成当前步骤
2. 更新 master-state.md
3. 写 handoff 到 .sessions/{date}-leo-resilient-routing/
4. 提交
5. 告知用户："请开新对话说 resume project leo-resilient-routing"

### 恢复流程

1. master-state.md
2. .sessions/ 最新 H{NNN} handoff
3. 当前步骤 stage file
4. decision_log.md
