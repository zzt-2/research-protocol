# Handoff: HGAT DAG Offloading — GW Stage 7 训练状态 + Baseline 修复

> 来源: S007 (GW Stage 7 仿真器重写+训练) | 交接目标: 修好 GraphSAGE/GCN/MLP 的 KL 问题，完成完整模型对比
> 文件名: H001-simulator-training-status.md

## 已完成边界

### 仿真器重写（全部完成，7 类验证 PASS）
- config.py: SimConfig dataclass，所有参数有据可查
- channel.py / orbital.py / dag.py: 物理模型构造函数注入
- env.py: Gymnasium 环境，HeteroData 图观测，action mask
- reward.py: RewardCalculator，log1p 变换后的有界奖励
- model_gnn.py: BaseActorCritic 抽象基类
- models_hgat.py: HGATActorCritic — bilinear policy head
- models_homo.py: GraphSAGE/GCN/MLP — bilinear policy head
- ppo.py: PPO + EarlyStopping + RewardNormalizer（已关闭）
- run.py: CLI 训练入口，4 模型注册表
- baselines/__init__.py: Random + GreedySPT + BaselineSuite
- verify.py: 7 类验证全部 PASS

### 训练结果（results_final/）
| Model | Best (avg) | Median (avg) | 状态 |
|-------|-----------|-------------|------|
| HGAT | -11.8 | -14.7 | 3/3 seed 收敛，超越 greedy(-16.7) |
| GCN | -29.1 | -280.4 | 2/3 seed KL early stop (3-16 ep) |
| GraphSAGE | -294.5 | -554.6 | 3/3 seed KL early stop (3-15 ep) |
| MLP | -164.9 | -559.9 | 3/3 seed KL early stop (3-6 ep) |
| Greedy(SPT) | -16.7 | - | baseline |
| Random | -1064 | - | baseline |

### 关键修复历程
1. **Mask 时序错误**: buf.add 存了 step 后的 mask → 存 step 前的 mask
2. **Reward normalizer**: 跨 episode Welford 处理不了双峰分布 → 关闭
3. **Bilinear policy**: Linear(64,4600) → task_emb @ node_emb.T，保留 per-node 信息
4. **Log1p reward**: t_norm 无上界(最高 -281K/step) → log1p 压缩到 [-215, -0.02]
5. **超参调整**: lr 3e-4, entropy 0.01, patience 100

## 不要做什么

- 不要恢复 reward normalizer（跨 episode 归一化在双峰分布下会崩溃）
- 不要恢复 Linear(64, 4600) policy head（mean pool 丢失 per-node 信息，KL=99M）
- 不要去掉 log1p 变换（原始 reward 尺度 PPO 无法学习）
- 不要把 mask 时序改回去

## 必读

1. `projects/hgat-satellite-dag-offloading/simulator/models_homo.py` — 问题代码所在
2. `projects/hgat-satellite-dag-offloading/simulator/models_hgat.py` — 可正常工作的参考实现
3. `projects/hgat-satellite-dag-offloading/simulator/reward.py` — log1p 奖励
4. `projects/hgat-satellite-dag-offloading/simulator/config.py` — 当前超参
5. `projects/hgat-satellite-dag-offloading/decision_log.md` — D013-D017 全部决策记录

## 下一轮

### 问题：GraphSAGE/GCN/MLP 的 KL 爆炸

**根因分析**：homo 模型将 HeteroData 转为同构图时，把 5 种节点类型（task/iotd/uav/leo/cs）合并。bilinear scoring 需要按 node type 拆分 embedding（task 部分 vs compute node 部分），但 `_split_homo_embs_single` 按固定 offset 切割。同构图 message-passing 后，类型边界信息被 GNN 混合，导致 bilinear scoring 不稳定 → KL 爆炸。

HGAT 没有这个问题，因为 HeteroConv 保持类型隔离，每种 node type 有独立的 embedding 空间。

**解决思路（按优先级）**：

1. **放宽 KL 阈值**（最简单）：将 early_stop_kl_threshold 从 0.15 提到 0.5 或 1.0。GraphSAGE seed=123 在 KL=0.21 时停止，实际上并不算大。GCN seed=123 跑了 112 ep（KL=0.15 刚过阈值）。这说明 KL 阈值太严是主因之一。

2. **降低 homo 模型学习率**：homo 模型信息混合后梯度可能更大，需要更小的 lr（3e-4 → 1e-4）。

3. **用 per-type projection 代替简单 offset 切割**：在 `_split_homo_embs_single` 中不用固定 offset，而是给每个 node type 加一个 learnable projection，让模型自己学会区分类型。

4. **降低 PPO epochs**：4 → 2，减少每次 update 的策略变化幅度。

**建议先试方案 1+2**（改 config 即可），如果不够再加方案 3。

### 具体任务
1. 修改 config 或 run.py，给 homo 模型单独设 KL 阈值（如 1.0）和更低的 lr（1e-4）
2. 重跑 GraphSAGE/GCN/MLP 各 3 seed × 300 ep
3. 汇总 4 模型对比表，确认 HGAT > GraphSAGE > GCN > MLP > Random
4. 更新 master-state.md
