# Handoff 2026-05-14 (Round 3 — 消融实验)

## 当前进度
- 阶段：Execute Step 2（核心实验 baseline 对比已完成，消融实验待做）
- Contract 状态：frozen
- 本轮完成：neighbor_map bug修复、GRLR复现、三方对比、Contract两项核心指标达标
- 待做：消融实验 A1/A2/A3

## Contract 核心指标状态
- [✓] 时延保留率 90.3% ≥ 80%
- [✓] vs Dijkstra 差距 9.9% ≤ 20%
- [ ] PE 关键性 ≥8pp — **消融 A1 待做**
- [ ] 多尺度训练贡献 — **消融 A2 待做**

## 待做实验

### A1：移除 Orbital PE（P0）
- 修改 `snapshot_to_pyg`，将 PE 替换为零向量（保持输入维度不变）
- 重新预训练（`pretrain.py`），评估 720 星加权 Dijkstra stretch
- 预期：保留率下降 ≥8pp

### A2：移除多尺度训练（P1）
- 仅用 train_100（100 星）单一规模训练
- 评估 720 星加权 Dijkstra stretch
- 预期：保留率下降 5-8pp

### A3：同时移除 PE + 多尺度训练（P1）
- A1 + A2 组合
- 预期：保留率下降 ≥15pp

### 同规模消融（额外）
- 我们的架构（RoutingActorCritic, 3层GAT, PE）在 720 星训练+测试
- 分离架构 vs 规模泛化的影响
- 这个实验回答：性能差距来自跨规模还是架构本身？

## 关键数据参考

### 我们的方法（修复后，跨规模 66+100+200→720）
- Mean stretch: 1.097, Median: 1.056, P95: 1.315
- ≤1.2x optimal: 85.1%, ≤1.5x: 98.9%
- Mean delay: 66.77 ms (Dijkstra: 60.77 ms)

### GRLR（同规模 720→720）
- Mean stretch: 1.008, Median: 1.000, P95: 1.050
- 100% ≤1.2x optimal
- Mean delay: 60.32 ms

### 66 星同规模（快速测试）
- Mean stretch: 1.016, Median: 1.000

## 仿真器文件索引（simulator/）
核心文件：
- `config.py` — 参数配置
- `models.py` — RoutingGNN, RoutingActorCritic（3层GAT, h=128）
- `snapshot.py` — snapshot_to_pyg（含 PE 计算和 dir_mask）
- `env.py` — RoutingEnv + _build_neighbor_map（已修复双向映射）
- `pretrain.py` — 监督预训练
- `grlr_model.py` — GRLR 6节点GAT+AC
- `grlr_train.py` / `grlr_eval.py` — GRLR 训练/评估
- `pretrained.pt` — 监督预训练权重（72,965 params）

## 文件路径
- Decision log：`decision_log.md`（D001-D025）
- Contract：`contract.md`（frozen）
- Feasibility：`feasibility_report.md`
- Literature：`literature_notes.md`（25篇+2理论）
- GRLR 论文：`papers/doi/10.1109_tvt.2024.3471658/content.md`
