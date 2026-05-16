# Handoff 2026-05-16 (Round 16) — ILP 标签失败，转向路由感知标签

## 当前进度
- **阶段：Execute Step 1 → 标签生成修正**
- Contract 状态：**frozen**（待修订）
- 本轮完成：Phase A 代码全部实现 + ILP 数据集 + 监督训练 + 评估
- **ILP 标签验证失败，需转向路由感知标签**

## 核心发现：ILP 标签是代理目标，不能直接用

### Phase A 完整实验结果

| 指标 | Phase A (ILP监督) | B1 Grid/Fixed | 差距 |
|------|-------------------|---------------|------|
| M1_throughput | 0.0787 | 0.1739 | -55% |
| M3_switch_rate | 0.0441 | 0.0000 | 严重 |
| M5_fairness | 0.3661 | 0.5207 | -30% |
| F1 (ILP拟合) | 0.9998 | — | 完美 |

**结论**：GNN 完美学到了 ILP 解（F1=0.9998），但 ILP 解本身不是好的策略。根因：
1. ILP 最大化加权容量（代理目标）≠ 最大化路由吞吐量（真实目标）
2. ILP 每步独立求解→无时序一致性→频繁切换→setup delay 损失
3. B1 的固定 grid 拓扑天然零切换、零 setup、路由连通性保证

### 与之前先验策略的对比

| 方法 | M1 | M3 | 说明 |
|------|-----|-----|------|
| Prior (active_bias=3) | 0.078 | 0.03 | D020 |
| Phase A (ILP监督) | 0.079 | 0.044 | D029 |
| B1 Grid/Fixed | 0.174 | 0.000 | 下限 |

Phase A 和先验策略性能几乎相同——因为 ILP 的单步最优解本质上和"选短边+保持活跃"是同构的。

## 已完成的代码资产

### 新建文件（全部可用）
```
simulator/ilp_solver.py          — PuLP CBC ILP 求解器 (~150行)
simulator/generate_dataset.py    — ILP 数据集生成 (~200行)
simulator/discrete_wrapper.py    — 离散动作包装器 (~100行)
simulator/train_supervised.py    — Phase A 监督训练 (~180行)
simulator/train_ppo_discrete.py  — Phase B 离散 PPO (~330行)
run_pipeline.py                  — 端到端流水线 (~150行)
evaluate_phase_a.py              — Phase A vs B1 评估
```

### 修改文件
```
simulator/config.py              — +ILP/Phase A/B 参数
simulator/environment.py         — +set_isl_configuration() + get_candidate_info()
simulator/model_gat.py           — +GATv2Backbone + SupervisedGNN + DiscreteRLGNN
```

### 已生成的数据
```
data/ilp_dataset_24x20/          — 500 快照，avg 5642 候选边，ILP 选 93 条
results/phase_a_24x20/           — Phase A 训练结果 (acc=1.0, F1=0.9998)
```

## 下一步：路由感知标签 + N_LCT=4

### 核心改动

**1. N_LCT 从 3 改为 4**（`config.py`）
- 目的：与 B1 公平对比（B1 有 4 条固定 ISL：2 同轨 + 2 跨轨）
- 之前 N_LCT=3 是为了给 DRL 留优化空间（D012），但现在监督学习证明空间不在 N_LCT 上

**2. 路由感知标签生成器**（重写 `generate_dataset.py` 的核心逻辑）
- 不再调用 `ilp_solver.py`
- 改用**贪心局部搜索**：
  1. 初始拓扑 = B1 的 grid 拓扑（4 条 ISL/星）
  2. 每步：对每颗卫星，尝试替换一条 ISL（保持其他 3 条不变）
  3. 计算替换前后的**路由吞吐量**（调用 `router.py`）
  4. 只保留有改善的替换
  5. 生成的标签 = 改善后的拓扑
- 这样标签天然路由感知 + 时序一致

**3. 具体实现方案**

```python
def generate_route_aware_dataset(...):
    for ep_idx in range(n_episodes):
        env.reset(seed=seed + ep_idx)
        # 初始拓扑 = B1 grid
        grid_edges = build_grid_topology(env)  # 复用 baselines/grid_fixed.py 逻辑
        env.set_isl_configuration(grid_edges)
        
        for step in range(episode_steps):
            obs = env._build_obs()
            current_edges = get_active_edges(env)
            
            # 贪心搜索：对每颗卫星尝试替换一条 ISL
            best_edges = current_edges
            best_throughput = compute_throughput(env, current_edges)
            
            for sat in range(n_sats):
                sat_edges = [e for e in best_edges if sat in e]
                for old_edge in sat_edges:
                    for new_edge in get_candidates_for_sat(env, sat):
                        if new_edge == old_edge:
                            continue
                        trial_edges = (best_edges - {old_edge}) | {new_edge}
                        trial_tp = compute_throughput(env, trial_edges)
                        if trial_tp > best_throughput:
                            best_edges = trial_edges
                            best_throughput = trial_tp
            
            # 保存标签
            save_sample(obs, best_edges)
            
            # 用最优边推进 env
            scores = edges_to_scores(best_edges, obs)
            env.step(scores)
```

**关键依赖**：
- `baselines/grid_fixed.py` 的 `_build_grid_topology()` 逻辑可复用作初始拓扑
- `router.py` 的 `route()` 已有完整的路由计算
- `environment.py` 的 `set_isl_configuration()` 可直接设置拓扑

**4. 计算成本估算**
- 每步贪心搜索：~480 sat × ~3 ISL/星 × ~20 候选/星 = ~28K 次路由计算
- 每次路由 ~10ms (Dijkstra) → 每步 ~280s → 太慢
- **优化**：只对随机采样的 k 颗卫星做替换（如 k=50），减少到 ~3K 次路由 → ~30s/步
- 50 步/episode × 5 episode × 30s = ~2h 数据生成（可接受）

**5. 训练和评估**
- 用新标签重训 `SupervisedGNN`（代码不变，只换数据集）
- 评估：Phase A vs B1(N_LCT=4)，目标 Phase A M1 > B1 M1
- 如 Phase A 成功，继续 Phase B 离散 RL 微调

## B1 基线数据 (24×20)

| 指标 | 值 |
|------|-----|
| M1_throughput | 0.1739 |
| M3_switch_rate | 0.0000 |
| M5_fairness | 0.5207 |
| total_reward | 8.6958 |

## 决策索引

- D029: Phase A ILP 标签验证失败（M1=0.079 vs B1=0.174）
- D030: 转向路由感知标签 + N_LCT=4

## 新对话应读的文件

1. 本 handoff
2. `projects/leo-isl-scheduling-drl/decision_log.md` D029-D030
3. `code-quality.md` 失败模式 A1-A3
4. `baselines/grid_fixed.py` — B1 拓扑构建逻辑（路由感知标签的初始拓扑来源）
5. `simulator/router.py` — 路由计算（标签生成的核心）
6. `simulator/environment.py` — set_isl_configuration() 接口
7. `simulator/model_gat.py` — 已重构的模型（Backbone + SupervisedGNN + DiscreteRLGNN）
