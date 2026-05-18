# Handoff: Step 4b Go → Step 6 仿真器设计

> 来源: Step 4a/4b/5 完成 | 交接目标: Step 6 仿真器设计
> 文件名: H003-step6-sim-design.md

## 已完成边界

1. **Step 4a**: A0/A'/A/B/D 全通过，MVE PASS（GNN AC=0.966, R2C=0.748 > MLP 0.942/0.682），用户已确认 Go
2. **Step 5**: Baseline 选定，用户已确认
   - B1: GRC (`grc_rank`) — 启发式代表
   - B2: PPO-DualGAT+ (`ppo_dual_gat+`) — GNN+DRL SOTA
   - B3: pg_mlp (`pg_mlp`) — MLP 消融
   - B4: CONAL (`conal`) — 约束感知竞品
   - B5: PPO-DualGCN (`ppo_dual_gcn`) — GNN 架构变体
3. **Step 4b**: C/E 无致命信号，建议 Go，待用户确认
4. **精读提取补做**: 5 篇核心竞品已补提取实验完备性（L01/L04/L10/L11/L12），流程已修复（gw-read.md 新增派遣强制清单）

## 不要做什么

- 不要重新评估 A0/A'/A/B/D（已通过并确认）
- 不要更换 Baseline（已确认 B1-B5）
- 不要跳过 Step 6 直接实现（需要设计规格经用户确认）
- 主对话不要直接 webSearch/webReader

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态
2. `projects/nfv-sfc-vne/feasibility_report.md` — 含 A0/A'/A/B/D/C/E 全部维度 + MVE 架构摘要
3. `stages/gw-experiment.md §sim` — Step 6 框架
4. `projects/nfv-sfc-vne/literature_notes.md` — 含实验完备性汇总和 Baseline 候选表
5. `stages/gw-feasibility.md §FR-12` — MVE→Formal 架构差异门控（Step 6 必须做）
6. `code-quality.md` + `reference/sim-template/` — 代码模板（实现前必读）

## 下一轮

### Step 4b 用户确认（最快）

直接问用户确认 Step 4b Go，一句话的事。

### Step 6 仿真器设计（核心任务）

按 `gw-experiment.md §sim` 执行：

1. **读框架文件**：`stages/gw-experiment.md`、`code-quality.md`、`reference/sim-template/`
2. **基于 Virne 设计扩展方案**：
   - SFC 依赖链约束建模（VNR → SFC DAG）
   - Matching-style GNN policy（Node-Edge 联合嵌入）
   - 评估指标（AC, R2C, SFC 链完整性, 端到端延迟）
   - 拓扑配置（Waxman100/500, Geant, Brain）
   - 训练配置（超参、early stopping、wandb/tensorboard）
3. **FR-12 MVE vs Formal 架构差异门控**：必须做对照表
4. **用户确认设计规格**

### MVE 架构摘要（FR-11，供 FR-12 对照）

- 动作空间: 离散节点选择（双向：先选虚拟节点再选物理节点）
- 决策粒度: per-VNR（逐请求处理，每请求内逐节点放置）
- 对比范式: PPO-DualGAT+（GNN 跨图编码）vs pg_mlp（MLP）vs GRC（启发式）
- 奖励语义: fixed intermediate reward (0.1) + episode-level R2C

### Virne 关键路径

- 仿真器位置: `projects/nfv-sfc-vne/Virne/`
- Solver 注册: `virne/solver/` 下各子目录，用 `@SolverRegistry.register` 装饰器
- 配置: `settings/main.yaml`（solver_name）、`settings/learning.yaml`（训练参数）
- 已验证可用: GRC(21s), pg_mlp(30ep~170s/ep), PPO-DualGAT+(epoch1, AC=0.966)

### 关键约束

- 核心贡献 = "SFC 依赖链约束 + matching-style GNN"，非"跨规模泛化"
- GNN 架构走 Node-Edge 联合嵌入（matching-style），不用 HGAT
- 跨规模降级为论文级共享特性（Ch3 已占据）
