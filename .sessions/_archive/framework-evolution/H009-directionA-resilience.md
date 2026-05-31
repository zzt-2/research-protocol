# [H009] 方向 A 验证 — 路由+ISL+抗毁

## 背景

学位论文要求：1 个大方向 → 3 个互相关联的问题 → 3 章主体。

方向 A 的候选组合：
- **Ch1: GNN 路由 Size Gen**（leo-mega-constellation-gnn-routing）— Execute 完成
- **Ch2: ISL 链路调度 DRL**（leo-isl-scheduling-drl）— GW 完成，待 Contract
- **Ch3: LEO 星座抗毁/故障恢复 DRL** — 尚未启动

初步检索显示抗毁方向：~15-20 篇论文，DRL 渗透率 ~30%（3-5 篇），是真蓝海。但与路由/ISL 有重叠风险。

## 核心问题

**抗毁/故障恢复 与 现有的路由和 ISL 调度，差异够大吗？** 具体来说：
- "故障恢复路由" vs "正常路由" — 是否只是换了场景的同一个问题？
- "抗毁链路重构" vs "ISL 调度" — 是否只是换了优化目标？
- 如果差异不够，3 章会不会被答辩委员会认为是"同一件事做了 3 遍"？

## 前置阅读

1. `directions-registry.md` — 已排除/已探索方向
2. `projects/leo-mega-constellation-gnn-routing/decision_log.md` — 路由项目的核心决策
3. `projects/leo-isl-scheduling-drl/decision_log.md` — ISL 项目的核心决策
4. `projects-overview.md` — 跨项目教训

## 任务

### Step 1: 读现有项目，提取问题边界

读路由和 ISL 项目的 decision_log 和 feasibility_report，明确：
- 路由项目解决的问题边界（什么做了，什么没做）
- ISL 项目解决的问题边界
- 两者的建模方式差异（状态/动作/奖励空间）
- 是否已经涉及了"故障/抗毁"场景

### Step 2: 检索抗毁方向的论文

用 `tools/search` 检索 2-3 组关键词：
- LEO satellite resilience / fault recovery / cascading failure + DRL
- 低轨星座 抗毁 / 故障恢复 / 链路重构 + 深度学习
- LEO constellation topology reconfiguration after failure

评估：
- 抗毁方向的核心问题定义是什么？（路由修复？拓扑重构？资源重分配？）
- 它与正常路由/ISL调度的**本质差异**在哪里？（不仅是换了参数）
- 已有的 3-5 篇 DRL 论文具体做了什么？方法是什么？

### Step 3: 判断

给出明确结论：

**方案 A: 可行** — 三个问题有本质差异，给出差异论证（每对差异 1-2 句）
**方案 B: 不可行** — 重叠太大，说明具体哪里重叠
**方案 C: 需要调整** — 差异存在但不够，需要调整某个子问题来拉开距离

如果结论是 A 或 C，给出建议的论点表述（一句话概括整个方向）。

## 约束

- **严禁在主对话中使用 WebSearch 或 webReader**，会导致上下文爆炸。检索只能用 `tools/search`，web 查询只能在子 agent 中执行
- 检索结果存 `search-archive/{today}/`
- 不精读论文，只看标题/摘要
- 不创建项目目录，不写正式报告
- 单对话内完成；只有确认需要开新对话继续时才写 handoff
