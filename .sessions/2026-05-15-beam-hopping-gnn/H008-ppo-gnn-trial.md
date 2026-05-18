# Handoff 2026-05-15 (Round 8 — PPO+GNN 初试 + 方向待决)

## 当前进度
- 阶段：GW Step 7 §impl（Part B 完成，PPO+GNN 初试完成）
- 状态：**方向待决** — PPO+GNN 效果不理想，需用户决策
- 本轮完成：PPO+GNN 实现 + 训练 + 与所有 baseline 统一对比

## 全部结果汇总（30 eps, 同种子）

| Method | Total | Interference | vs Random |
|--------|-------|-------------|-----------|
| Random | 5.85 | 4.70 | — |
| PPO+MLP | 5.86 | 4.89 | +0.2% |
| **PPO+GNN** | **5.94** | **4.37** | **+1.5%** |
| GraphColoring | 5.96 | 3.02 | +1.8% |
| OptGreedy | 6.47 | 0.50 | +10.5% |

GNN 消融成立（PPO+GNN > PPO+MLP, +1.4%），但提升有限，未超传统 GC。

## 根因分析（为什么 PPO+GNN 效果差）

### 1. 方法选择有根本问题
- **成功 GNN 论文全不用 RL**：L01/L02/L06 用无监督/监督学习，梯度从 loss 直通 GNN 参数
- **RL 论文不用 Gaussian policy**：L03 用 QPLEX（值分解），L05 用 A3C+MADDPG
- 我们选了最差的组合：Gaussian policy（稀疏梯度）+ top-K 机制（14/19 维无梯度）

### 2. 奖励信号结构问题
- Fairness 占 82% 奖励，几乎恒定（~0.88/步），不可学
- 可学信号 interference 仅占 ~7%，被噪声淹没
- OptGreedy 的优势 68% 来自干扰降低，但 PPO 学不到这个信号

### 3. D002 的判断需要修正
- 原判断："REINFORCE 不稳定，PPO 可解决"
- 实际：问题不在算法稳定性，在 action space 设计 + 奖励结构
- MVE 的 +16~48% 可能是其他因素（不同奖励/简化设置），不应作为 PPO 的预期

## 三条路径

| 路径 | 描述 | 投入 | 风险 |
|------|------|------|------|
| A. 调参 | 加大 γ(interference)权重，更长训练 | 0.5天 | 改了问题定义，治标不治本 |
| B. 换方法 | 模仿 L01 无监督学习，GNN 直接优化 throughput | 2-3天 | 最接近成功论文，但需重写 |
| C. 换方向 | 放弃 BH+GNN，聚焦 ISL Scheduling / Handover DRL | — | 已有进展，沉没成本低 |

## 文件路径
- PPO+GNN: `baselines/ppo_gnn.py`
- PPO+GNN 模型: `results/ppo_gnn_model.pt`
- 统一评估: `verify/evaluate_baselines.py`
- Baselines: `baselines/` (greedy/ppo_mlp/graph_coloring/ppo_gnn)
- 决策日志: `decision_log.md` (D001-D012)
- Baseline 报告: `baseline_report.md`

## 下一步
**等待用户决策**。如果继续本方向，优先考虑路径 B（换无监督方法）。
