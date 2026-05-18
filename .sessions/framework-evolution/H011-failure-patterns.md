# [H011] 跨项目失败模式提取

## 背景

跨 6 个研究项目积累了大量失败/死胡同/调参循环的经验，但目前散落在各项目的 decision_log.md 和 handoff 中，没有集中整理。需要一个结构化的失败模式记录，供后续项目遇到类似情况时快速检索对照。

## 前置阅读

1. `projects-overview.md` — 跨项目教训段（已有初步整理）
2. `stages/execute.md` Step 4.5 — 防死胡同规则和典型模式表
3. `code-quality.md` — 代码质量经验（部分与失败模式重叠）

## 任务

### Step 1: 逐一读 6 个项目的 decision_log

按以下顺序读，每个重点标注失败/死胡同/重大转向的决策：

1. `projects/leo-beam-hopping-gnn/decision_log.md` — D011(方法失败), D013(归档)
2. `projects/leo-isl-scheduling-drl/decision_log.md` — D017-D022(Execute死胡同)
3. `projects/leo-ntn-handover-drl/decision_log.md` — 找叙事转向的决策
4. `projects/leo-mega-constellation-gnn-routing/decision_log.md` — D021(PPO无效), D022(bug修复)
5. `projects/hgat-satellite-dag-offloading/decision_log.md` — 找多IoTD改造相关决策
6. `projects/ris-phase-drl/decision_log.md` — 找方向调整相关决策

### Step 2: 提取失败模式

对每个失败的决策/死胡同，提取结构化记录：

```
模式: {简短名称}
项目: {项目名}
决策ID: D{N}
阶段: {GW/CT/EX}
表现: {具体发生了什么，含数值}
根因: {根本原因}
先例: {之前有没有类似情况}
教训: {下次遇到怎么做}
严重程度: 致命(项目归档) / 严重(换方案) / 中等(调参可解)
```

### Step 3: 归类整理

按模式类别组织（不是按项目），参考 `stages/execute.md` Step 4.5 的典型死胡同模式表，但不限于 Execute 阶段。预期类别：

- **RL 训练失败模式**（梯度信号弱 / 先验>学习 / 探索破坏稳定）
- **方向判断失败模式**（假蓝海 / 方法与问题不匹配 / 叙事转向）
- **仿真器/实现失败模式**（物理模型错误 / 规模扩展崩溃 / 性能瓶颈）
- **设计决策失败模式**（奖励函数设计 / 动作空间设计 / 基线选择）

### Step 4: 写入

将提取结果追加到 `code-quality.md` 末尾的"失败模式"段（如已有则合并去重），格式为可增量添加的结构化列表。

同时更新 `projects-overview.md` 的"跨项目教训"段，确保与失败模式记录一致（不重复内容，只引用）。

## 约束

- 只读 decision_log.md + projects-overview.md + stages/execute.md，不需要读其他文件
- 不精读全文，只看 `[DEAD_END]`、归档、转向、FAIL 相关的决策
- 结果写入 `code-quality.md` 和 `projects-overview.md`（已有文件，用 Edit 追加）
- 不创建新文件
- 单对话内完成；只有确认需要开新对话继续时才写 handoff
