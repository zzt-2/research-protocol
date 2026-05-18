# Handoff 2026-05-16 — 框架文档精简与补充

## 当前进度
- 阶段：框架演进（非具体项目，是跨项目框架维护）
- 状态：用户确认需要精简文档 + 补充规则，上下文已满需要交接

## 本轮完成

### 1. 创建 projects-overview.md
- 跨项目状态汇总（5 活跃 + 1 归档），100 行
- 跨项目教训（方向/方法/仿真器/训练/Baseline 5 维度）
- 使用场景说明
- CLAUDE.md 状态恢复段已加入此文件为第 1 优先读取项

### 2. 创建 directions-registry.md
- 所有已探索方向全记录（20+ 方向），95 行
- 活跃项目 / 已归档 / 已排除 / 未深入 / 潜在空白
- CLAUDE.md 和 projects-overview.md 已引用

### 3. 学位论文结构要求
- 导师要求：1 个大方向 → 3 个互相关联的问题 → 3 章主体
- 现有项目可组成的方向：
  - 方向 A：LEO 星座网络优化（路由+ISL调度+切换）— 3 个都有进展
  - 方向 B：频谱共享/干扰协调（LEO+GEO 共存）— 新方向
  - 方向 C：卫星边缘智能计算（仅 DAG 卸载 1 个，缺 2 个）
  - 方向 D：RIS 辅助卫星通信（仅相移 1 个，缺 2 个）
- 已写入 memory: `project_thesis-structure.md`

### 4. 防死胡同机制
- `stages/execute.md` 新增 Step 4.5：触发条件（连续 3 次迭代核心指标改善 <5%）+ 处理流程（暂停→写 analysis→写 PROMPT→交接新对话）
- `templates.md` 新增 `[DEAD_END]` 决策标记格式
- `CLAUDE.md` 跨阶段护栏新增索引条目

### 5. 实验执行纪律
- `stages/execute.md` Step 2 新增"实验执行纪律"段：跑前报时间预估、先跑 1-2 episode 烟雾测试、长任务用 run_in_background

### 6. 失败模式提取
- 另一对话完成：从 6 个项目 decision_log 提取 14 个失败模式，20 条案例
- 写入 `code-quality.md` 末尾"失败模式记录"段
- `projects-overview.md` 跨项目教训段新增引用

### 7. webSearch 禁令
- `CLAUDE.md` 新增"主对话严禁 WebSearch/webReader"段
- 三个 PROMPT 文件同步加入禁令

### 8. blit --source cnki 学位论文支持
- 另一对话完成：`tools/blit.py` 新增 `--doc-type phd/master` 支持
- CLAUDE.md 检索工具段已更新

## 待办：文档精简与补充

用户要求新对话做两件事：**精简冗余文档** + **补充缺失规则**。

### 精简项

#### P1: CLAUDE.md 跨阶段护栏段压缩（优先级最高）
当前状态：~15 行索引，但很多条目写得太详细（如防死胡同规则、检索工具规则），等于在 CLAUDE.md 和对应文件中重复维护。

要求：
- 每条索引**只保留 ≤10 字的一句话**+文件引用
- 删掉详细描述（详细内容只存在于 execute.md / contract.md 等）
- CLAUDE.md 定位是"去哪看"，不是"看什么"
- 但要注意：CLAUDE.md 中的"上下文管理规则"段（子agent委托、webSearch禁令等）是**跨阶段强制规则**，这些规则没有对应阶段文件，必须留在 CLAUDE.md，不能删

#### P2: execute.md 起源段落外移
当前状态：3 处 `> 起源：xxx 项目中...` 背景故事散在正文，占比大。

要求：
- 起源故事全部移到 execute.md 末尾新增"设计决策记录"段
- 正文只留规则本身

#### P3: 跨项目教训合并
当前分散在三处：
- `projects-overview.md` "跨项目教训"段
- `code-quality.md` "失败模式记录"段
- `directions-registry.md` 排除原因

要求：
- 合并为一处。方案 A：`code-quality.md` 改名为 `experience.md`（代码质量+失败模式+跨项目教训统一管理）。方案 B：保持 code-quality.md 但把跨项目教训从 projects-overview.md 删除改为引用。
- 另外 two files（projects-overview.md 和 directions-registry.md）的教训段只保留引用，不重复内容
- 新对话自行判断选哪个方案

### 补充项

#### P4: 先验策略基线测试（加在 execute.md Step 1 前）
多项目教训：手写先验接近最优时 RL 基本学不到东西。

要求：
- 在写 RL 代码之前，增加一个"先验策略基线测试"步骤
- 测 trivial policy（最近邻/随机+简单规则）的表现
- 如果 trivial policy 已达目标 70%+，标记为风险，需要重新评估 RL 价值主张
- 先例：ISL active_bias 达 B1 的 75%，Routing 贪心推理 97.6%，Handover top-K 压缩做主功

#### P5: 动作空间-算法兼容性检查（加在 execute.md Step 0 或 code-quality.md）
选算法之前先检查动作空间与算法的兼容性。

已知的失败组合：
- 连续分数 + top-K 选择 vs PPO(Normal 分布) — ISL, BH 项目验证
- 离散选择 + 图结构信号 vs Gaussian policy — BH 项目验证
- 高维连续(100+) vs A2C — RIS 竞品撤稿验证

要求：
- 写成决策参考表，放在合适的位置（code-quality.md 或 execute.md）
- 新对话判断放在哪里最合适

## 关键上下文

### 文件改动清单（本轮已改）
- `CLAUDE.md` — 状态恢复段、跨阶段护栏（防死胡同+检索工具+webSearch禁令）
- `stages/execute.md` — Step 2 实验执行纪律、Step 4.5 防死胡同检测、Step 4.5 典型死胡同模式表
- `templates.md` — `[DEAD_END]` 标记格式
- `projects-overview.md` — 新建
- `directions-registry.md` — 新建
- `code-quality.md` — 失败模式记录（另一对话写入）

### 待跑的新对话提示词（已写好）
- `.sessions/framework-evolution/H014-thesis-structure-research.md` — 研究硕博论文结构（优先跑）
- `.sessions/framework-evolution/H009-directionA-resilience.md` — 方向 A 验证（路由+ISL+抗毁）
- `.sessions/framework-evolution/H010-directionB-spectrum.md` — 方向 B 验证（频谱共享拆3子问题）
- `.session/2026-05-15-isl-scheduling-drl/PROMPT-execute-deadend.md` — ISL 死胡同方向决策

### ISL 项目当前状态
- Execute Step 0-1 完成，PPO 未超越先验
- 另一对话尝试 REINFORCE + Gumbel-top-K 方案（D024），测试超时/OOM，未得出结论
- decision_log 到 D024，待方向决策

## 下一步
1. **先精简文档**（P1-P3），减少后续对话的阅读负担
2. **再补充规则**（P4-P5）
3. 精简完成后，用户可以继续跑待跑的提示词
