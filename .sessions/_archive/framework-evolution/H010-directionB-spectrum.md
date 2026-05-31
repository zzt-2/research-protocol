# [H010] 方向 B 验证 — 频谱共享 LEO+GEO 共存

## 背景

学位论文要求：1 个大方向 → 3 个互相关联的问题 → 3 章主体。

候选方向：**LEO+GEO 频谱共享/干扰协调**
- 真蓝海：DRL 仅 5 篇，GNN 零篇
- 实际问题：Ku/Ka 频段 LEO 与 GEO 共存是监管热点
- GNN 有天然优势：卫星间干扰关系可建模为图
- 与现有 5 个项目零重叠

初步检索的竞品：
- "DRL-Based Spectrum-Sharing for GEO-LEO Co-Existing" (2024, cite=2)
- "Joint Beam Management and Resource Allocation in GEO-LEO Spectrum-Sharing" (2025, cite=11)
- "DRL-Based Intellectual Spectrum Planning" (2026)
- "LLM-Aided Spectrum-Sharing LEO" (2026)

## 核心问题

**这个方向能否自然拆出 3 个互相关联的子问题？** 3 个子问题需要有：
1. 逻辑递进或互补关系（不是平行独立的 3 个实验）
2. 每个都能独立成章，有足够的新颖性和工作量
3. 合在一起能支撑一个连贯的论点

## 前置阅读

1. `directions-registry.md` — 已排除/已探索方向
2. `projects-overview.md` — 跨项目教训
3. `domain-comms.md` — 通信领域定制

## 任务

### Step 1: 深入检索

用 `tools/search` 对频谱共享方向做更深入的检索（之前只做了浅搜）：

英文关键词（每组 ≤30 条）：
- LEO GEO coexistence spectrum sharing + DRL/GNN/ML
- satellite interference coordination + graph neural network
- cognitive radio satellite + deep reinforcement learning
- LEO GEO spectrum sharing + power control / beam management

中文关键词：
- 低轨高轨卫星 频谱共享 干扰协调 + 深度学习
- 卫星同频干扰 + 资源分配 + 强化学习

### Step 2: 分析问题空间

基于检索结果，分析这个方向的问题空间能否拆成 3 个：

可能的拆分维度：
- **按优化目标拆**：干扰最小化 → 频谱效率最大化 → 公平性保障
- **按技术手段拆**：GNN 干扰拓扑建模 → DRL 功率分配 → 联合优化
- **按场景复杂度拆**：静态场景（固定 GEO）→ 动态场景（LEO 运动）→ 多运营商场景
- **按问题层次拆**：频谱感知/检测 → 干扰建模 → 动态资源分配

对每种拆分方案评估：
- 3 个子问题之间是否有关联（递进/互补/依赖）
- 每个子问题的独立新颖性够不够
- 是否有足够的蓝海空间（每个子问题 <10 篇 ML 论文）

### Step 3: 给出结论

明确回答：

**结论 A: 能拆** — 给出最优拆分方案 + 论点表述 + 每个子问题的蓝海判断
**结论 B: 勉强** — 能拆但某个子问题较弱，指出哪个弱+为什么
**结论 C: 不能拆** — 问题空间太窄，3 个子问题会撞车

如果结论是 A 或 B，同时评估：
- 这个方向的工作量 vs 方向 A（路由+ISL+抗毁）
- 哪个更容易在学位论文时限内完成

## 约束

- **严禁在主对话中使用 WebSearch 或 webReader**，会导致上下文爆炸。检索只能用 `tools/search`，web 查询只能在子 agent 中执行
- 检索结果存 `search-archive/{today}/`
- 不精读论文，只看标题/摘要
- 不创建项目目录，不写正式报告
- 检索前先查 `directions-registry.md` 和 `search-archive/2026-05-15/` 已有记录
- 单对话内完成；只有确认需要开新对话继续时才写 handoff
