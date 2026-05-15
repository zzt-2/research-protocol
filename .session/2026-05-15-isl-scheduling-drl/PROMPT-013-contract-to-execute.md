# 新对话提示词 — ISL Scheduling DRL: Contract → Execute

## 项目恢复

读以下文件恢复上下文（按顺序）：

1. `.session/2026-05-15-isl-scheduling-drl/HANDOFF-012-lct-constraint.md` — 最新交接
2. `projects/leo-isl-scheduling-drl/decision_log.md` — 全部决策记录（注意 [D012] 问题重设定）
3. `projects/leo-isl-scheduling-drl/baseline_report.md` — B1+B2 结果
4. `projects/leo-isl-scheduling-drl/literature_notes.md` — 文献精读

## 当前状态

- **GW 全部完成**，问题经过重设定（D012）
- 核心变更：强制 N_LCT=3 终端约束，固定贪心 M1=17.09%，与无限 ISL（28.19%）的 gap=11.1%
- 参数鲁棒性扫描 9/9 配置 gap>5%，方向确认
- 仿真器 + B1 + B2 已实现并验证
- 模板体系已更新：`reference/sim-template/` 有完整的 BaseActorCritic、PPO、DQN、BaselineSuite、Evaluator、ExperimentRecorder 等

## 任务：从 Contract 开始，一直做到 Execute 完成

### 阶段流程

1. **Contract 阶段** — 读 `stages/contract.md`，按步骤执行：
   - Step 0: 方案新颖性检索
   - Step 1-5: 假设冻结、数据流推演、反模式审查、Contract 冻结
   - 产出：`contract.md` + `data-flow.md`

2. **Execute 阶段** — 读 `stages/execute.md`，实现核心方法：
   - 用 `reference/sim-template/` 模板：BaseActorCritic、PPO/DQN 训练循环、BaselineSuite、Evaluator
   - 实现 GNN-DRL 核心：继承 BaseActorCritic，GAT 编码器 + PPO actor-critic
   - 在 N_LCT=3 约束下训练并评估
   - 目标：M1 从 17.09%（固定贪心）提升到 25%+

### 关键参数（已验证）

- N_LCT=3, demand=10Gbps, N_GS=100, Z_MAX=3000km
- 单路径 Dijkstra 路由（多路径仅+5%不值得）
- Episode: 50 步 × τ=10s

### 框架文件必须读

- 进入 Contract → 读 `stages/contract.md`
- 进入 Execute → 读 `stages/execute.md`
- 写代码前 → 读 `code-quality.md` + `reference/sim-template/` 对应模板
- 每完成一步 → 更新 handoff 文件

### 执行要求

- 一直做下去，不要停下来问我，除非需要用户确认（Contract 冻结前必须确认）
- 遵循 `stages/contract.md` 和 `stages/execute.md` 的每一步
- 子 agent 委托规则：论文精读、web 检索结果、MVE 实验在子 agent 执行
- 代码用新模板，不要从零手搓
- 完成一个阶段/步骤后立即 commit
- 跨对话 handoff：每完成一个步骤写 HANDOFF 文件到 `.session/2026-05-15-isl-scheduling-drl/`
