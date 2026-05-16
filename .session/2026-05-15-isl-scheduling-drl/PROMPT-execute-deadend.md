# PROMPT: ISL Scheduling Execute 死胡同 — 方向决策

## 背景

leo-isl-scheduling-drl 项目 Execute 阶段陷入死胡同：PPO 无法超越手写先验。

当前状态：
- 纯先验策略（active_bias + distance_bias）M1=0.0774，已达 B1(0.1035) 的 75%
- PPO 微调 30ep 后 M1=0.0780，仅 +0.0006，几乎无改善
- 根因：连续分数 + Normal 分布 + top-K 选择 → PPO 不适配这个动作空间
- 全规模(24×66=1584) env.step=0.6s，候选边 65664 条，有内存/显存风险

这是一个已识别的跨项目失败模式。`code-quality.md` 末尾"失败模式记录"中 A1(连续分数+top-K) 和 A2(先验>学习) 均命中。

## 前置阅读

1. `projects/leo-isl-scheduling-drl/decision_log.md` — D017-D022（Execute 死胡同全过程）
2. `code-quality.md` 末尾"失败模式记录"段 — A1、A2 模式及先例
3. `projects-overview.md` 跨项目教训 — 方法选择段
4. `projects/leo-beam-hopping-gnn/decision_log.md` — D011-D013（类似失败案例，参考其处理方式）
5. `.session/2026-05-15-isl-scheduling-drl/HANDOFF-014-*.md` — 最新 handoff（如果有）

## 核心问题

**ISL 调度这个方向还能救吗？如果能，怎么救？**

## 任务

### Step 1: 确认根因

读 decision_log D017-D022，确认死胡同的根因分类：
- 是方法问题（PPO 不适配，换算法可解）？
- 是问题建模问题（连续分数+top-K 本身有缺陷，需要重新设计动作空间）？
- 是方向问题（ISL 调度本身不适合 DRL，需要换方向）？

参考 beam-hopping 的判断标准：D013 归档时认为"干扰是物理关系不可学习"，ISL 的情况是否类似？

### Step 2: 评估替代方案

针对每个可能的根因，评估替代方案：

**如果是方法问题：**
- 换离散动作空间（keep/drop/swap 三选一）→ 与 D012 的 N_LCT 约束是否兼容？
- 换算法（ES/SAC/行为克隆）→ beam-hopping 用监督学习有效（D011），ISL 能否类似？
- 分层决策（先选候选集，再逐链路决策）→ 能否解决 65664 候选边问题？

**如果是问题建模问题：**
- 重设计 MDP（状态/动作/奖励）→ 成本多大？需要回到 Contract 吗？
- 把"先验策略"本身作为贡献 → 类似 handover 项目的叙事转向经验

**如果是方向问题：**
- 归档，转入方向 A（路由+ISL+抗毁）的其他子问题
- 参考学位论文结构要求（1方向→3问题），路由已有结果，ISL 如果做不了，找替代子问题

### Step 3: 给出建议

给出明确建议（不是多个选项让用户选）：

1. **推荐方案**：一个具体方案，说明做什么、怎么做、预期效果、时间成本
2. **理由**：为什么选这个而不是其他
3. **风险**：这个方案可能失败的情况
4. **Plan B**：如果推荐方案失败，下一步是什么

## 约束

- 只读项目内文件 + code-quality.md + projects-overview.md，不额外检索文献
- 不在当前对话执行任何实验或代码修改
- 纯分析+建议，产出是口头讨论，不写文档
- 单对话内完成；只有确认需要开新对话继续时才写 handoff
