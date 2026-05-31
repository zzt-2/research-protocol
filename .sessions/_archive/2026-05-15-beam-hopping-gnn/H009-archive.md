# Handoff 2026-05-15 (Round 9 — BH+GNN 归档)

## 最终状态：归档

项目 leo-beam-hopping-gnn 经充分验证后确认不可行，归档处理。

## 归档原因

6 种学习方法在 N=19 和 N=37 上全部失败，干扰指标均 ≈ Random：

| Method            | N   | Total | Interference | vs Random    |
| ----------------- | --- | ----- | ------------ | ------------ |
| Random            | 19  | 5.85  | 4.70         | —            |
| PPO+GNN           | 19  | 5.94  | 4.37         | +1.5%        |
| PPO+GNN           | 37  | 4.94  | 12.74        | +6.2%        |
| DiffGNN v1        | 37  | 4.64  | 11.57        | -0.3%        |
| DiffGNN v2        | 37  | 4.60  | 11.59        | -1.1%        |
| REINFORCE+softmax | 37  | 4.73  | 11.67        | +1.7%        |
| REINFORCE(γ=0.7)  | 37  | -6.33 | 11.74        | 比 Random 差 |
| ApproxGreedy      | 37  | 5.19  | 8.72         | +11.6%       |

**根因**：干扰是 beam pair 之间的物理关系，需要直接计算（如 ApproxGreedy 的逐波束 SINR 评估），无法从标量奖励通过梯度反向传播学到。不是方法问题、不是规模问题、不是奖励权重问题。

## 本轮完成

1. Config 规模预设（small/medium/large）
2. ApproxGreedy（可扩展贪心，C(N,K)过大时替代OptGreedy）
3. PPO+GNN@N=37 验证
4. DiffGNN 可微分优化尝试（3 个版本）
5. REINFORCE+softmax 尝试
6. γ=0.7 干扰主导奖励尝试
7. 完整 N=37 baseline 对比

## 文件路径

- 决策日志: `projects/leo-beam-hopping-gnn/decision_log.md` (D001-D013)
- Baselines: `projects/leo-beam-hopping-gnn/baselines/` (greedy/ppo_mlp/ppo_gnn/graph_coloring/diff_gnn)
- 仿真器: `projects/leo-beam-hopping-gnn/simulator/` (config/env/antenna/channel/traffic)
- 前轮 handoff: `.sessions/2026-05-15-beam-hopping-gnn/HANDOFF-008-ppo-gnn-trial.md`

## 归档结论

BH+GNN 方向不成立。ISL Scheduling DRL 在另一个对话推进中。
