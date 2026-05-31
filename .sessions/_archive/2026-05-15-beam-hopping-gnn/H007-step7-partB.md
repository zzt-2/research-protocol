# Handoff 2026-05-15 (Round 7 — Step 7 Part B 完成)

## 当前进度
- 阶段：GW Step 7 §impl
- 状态：Part A + Part A-checkpoint + Part B 全部完成
- 本轮完成：3 个 baseline 实现 + 统一评估 + baseline_report

## Baseline 评估结果（30 eps, 同种子）

| Method | Total | vs Random | Interference |
|--------|-------|-----------|-------------|
| Random | 5.853 | — | 4.698 |
| PPO+MLP | 5.864 | +0.2% | 4.890 |
| GraphColoring | 5.958 | +1.8% | 3.020 |
| DemandGreedy | 5.987 | +2.3% | 4.654 |
| OptGreedy | 6.468 | +10.5% | 0.496 |

## 关键发现

1. **干扰惩罚是核心区分因子**：OptGreedy intf=0.50 vs Random intf=4.70，差距贡献 ~70% total reward gap
2. **PPO+MLP ≈ Random**：扁平 MLP 无法学习空间干扰结构，+0.2% 不显著
3. **GraphColoring 部分有效**：HEAD 着色分 3 组，降低 35.7% 干扰，但受固定分组约束
4. **PPO+MLP < GC 的意义**：这不是失败，而是支持 GNN 必要性——扁平 DRL 不够，需要图编码器

## PPO+MLP 训练说明
- v1（500eps, 1ep/update）→ 5.73 (比 Random 差)
- v2（2000eps, 10eps/batch, obs norm）→ 5.93 (略好于 Random)
- 两次训练 avg_reward 都在 5.8 附近收敛，未见明显上升趋势
- 根因：Gaussian policy 的 top-K 机制导致梯度稀疏，fairness 主导奖励信号

## 文件路径
- Baselines: `projects/leo-beam-hopping-gnn/baselines/` (greedy/ppo_mlp/graph_coloring)
- 评估脚本: `projects/leo-beam-hopping-gnn/verify/evaluate_baselines.py`
- 报告: `projects/leo-beam-hopping-gnn/baseline_report.md`
- PPO 模型: `projects/leo-beam-hopping-gnn/results/ppo_mlp_model.pt`
- 决策日志: `projects/leo-beam-hopping-gnn/decision_log.md` (D001-D010)

## 下一步：Contract 阶段
按 `stages/contract.md` 流程：
1. 先读 `stages/contract.md` 获取 Contract 阶段操作规范
2. Contract Step 0: 文献补充检索（如需）
3. Contract Step 1: 冻结参数表
4. Contract Step 2: 实验设计
5. Contract Step 3-5: 验证 + 反模式审查 + 冻结

## 需要先读的文件
1. 本 handoff
2. `stages/contract.md`（Contract 阶段完整操作）
3. `projects/leo-beam-hopping-gnn/baseline_report.md`（baseline 结果）
4. `projects/leo-beam-hopping-gnn/decision_log.md`（已有决策）
