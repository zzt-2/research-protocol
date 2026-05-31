# Execute V2 · Size Generalization 方向

## 你的任务

继续 LEO NTN 切换 DRL 项目的 Execute 阶段。方向已从"GNN 提升绝对性能"转向 **"可扩展的负载感知切换架构"**。

核心变更：
- 方案 A（LA-DDQN）已死亡：DLA cross-attention 被消融否定，不再投入
- 方案 C（GNN+DDQN）保留，但叙事调整：从"性能提升"到"size generalization"
- 需要验证 GNN 在大规模（50-100 UE）场景下的 scaling advantage

## 必读文件（按顺序）

1. `execute_progress.md` — 当前实验结果（超参搜索 E4 最佳、消融结果、B2 对比）
2. `decision_log.md` — D021-D025 是本次转向的关键决策
3. `novelty_search.md` — 末尾"Size Generalization 方向检索"部分
4. `design_C.md` — 方案 C 完整技术设计（GNN 架构、训练策略）
5. `execution_report.md` — 方案 A 验证报告（参考 top-K 压缩实现）

## 实验计划

### Phase 1：仿真器验证（~30 min）

确认仿真器在不同 UE 规模下行为正确：

1. **sat_capacity 调参**：当前默认 capacity=5。在不同 UE 数下确认负载竞争足够：
   - 20 UE, capacity=5 → 平均 ~4.4 可见卫星，负载竞争适中
   - 50 UE, capacity=5 → 某些热点卫星可能过载，需要确认
   - 100 UE, capacity=5 → 强竞争，容量约束成为关键瓶颈
   - 如果 50 UE 下阻塞率太低（<5%），考虑降低 capacity 或增加热点 UE 分布

2. **基线统计**：每个 UE 规模跑 10 episode 统计：
   - HHS baseline（B1）的阻塞率和切换次数
   - 可见卫星数分布（mean/max/min）
   - 负载竞争指标（标准差、最大负载卫星的 UE 数）

### Phase 2：20 UE 基线实验（~1 hr）

复用 execute_progress.md 中 E4 和 C6 的配置（target_update=3000, eps_decay=20），在 20 UE 下重新训练：

| 实验 | 方法 | 目的 |
|------|------|------|
| E4-20 | GNN+DDQN (E4 最佳配置) | 确认 20 UE 下 GNN ≈ MLP |
| C6-20 | flat MLP+topK | 对比基线 |

预期：GNN ≈ MLP（reward 差距 <2%），这是预期的——15 UE 已验证，20 UE 仍在 MLP 够用区间。

### Phase 3：50 UE 扩展实验（~2 hr）

| 实验 | 方法 | 目的 |
|------|------|------|
| E4-50 | GNN+DDQN, 50 UE | 验证 GNN 在规模增加时保持稳定 |
| C6-50 | flat MLP+topK, 50 UE | 预期：性能退化 |
| B2-50 | flat DDQN (无 top-K), 50 UE | 对照组 |

预期：GNN 开始显著优于 MLP（文献阈值 N>20-30）。

### Phase 4：100 UE 扩展实验（~3 hr）

| 实验 | 方法 | 目的 |
|------|------|------|
| E4-100 | GNN+DDQN, 100 UE | 进一步验证 scaling advantage |
| C6-100 | flat MLP+topK, 100 UE | 预期：显著退化 |

### Phase 5：Size Generalization（~1 hr）

**核心实验——这是论文最强论点：**

1. 取 E4-20 训练好的模型（Phase 2 的产出）
2. **不重训练**，直接在 50 UE 和 100 UE 环境中推理评估
3. 对比 C6-20 模型在 50/100 UE 下的推理表现

预期：
- GNN 模型由于 permutation equivariance，在大规模下保持大部分性能
- MLP 模型由于固定维度输入，在大规模下性能急剧退化

### Phase 6：Contract 冻结

实验结果出来后，按 `v2/templates.md` 中的 contract 模板创建 `contract.md`。

核心假设：**在 UE 数量 ≥ 50 的 LEO 切换场景下，基于二部图 GNN 的负载感知架构比 flat MLP 方法在 reward 上提升 ≥15%，且 GNN 模型可直接从 20 UE 训练迁移到 100 UE 部署，性能保持 ≥90%。**

Success signal：50 UE 下 GNN vs MLP reward 差距 ≥15%，100 UE 下 ≥25%
Failure signal：50 UE 下 GNN vs MLP reward 差距 <5%（GNN 的结构化编码无额外价值）

Contract 冻结前必须经用户确认。

## 关键代码文件

- `simulator/env.py` — 仿真器（已支持 `num_ues`, `sat_capacity` 参数）
- `simulator/orbit.py` — 轨道模型和 UE 位置生成
- `simulator/reward.py` — 奖励函数
- `c_gnn_ddqn.py` — 方案 C GNN+DDQN 实现（execute_progress.md §1）
- `baselines/b2_dueling_ddqn.py` — B2 DDQN baseline

## 注意事项

1. Python 环境：`~/.venvs/torch/bin/python`
2. GPU：RTX 4070，CUDA 已验证
3. 每个实验用 3 seeds，报告均值 ± 标准差
4. 训练时长估算：50 episode ~6 min (20 UE)，线性增长
5. 结果保存到 `results/` 目录，JSON 格式
6. **不要修改仿真器的物理模型**（轨道、信道），只调 `num_ues` 和 `sat_capacity`
7. 如发现仿真器不支持某些需求（如热点 UE 分布），记录到 decision_log 并与用户确认

## 输出

1. 各 phase 实验结果写入 `execute_progress.md`
2. 决策写入 `decision_log.md`
3. Contract 冻结后写入 `contract.md`
