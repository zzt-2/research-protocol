# Master State: leo-mega-constellation-gnn-routing

## 项目概况

- **方向**: GNN size generalization — 小星座训练零样本泛化到大星座路由
- **方法**: GAT (Graph Attention Network) + Orbital PE + 多尺度监督训练 + 加权 Dijkstra 推理
- **当前阶段**: Execute P0 完成 → paper-materials 待重写
- **学位论文章节**: Ch1 — 路由 Size Generalization

## 已完成步骤

### Groundwork
- Step 1-3: 完成
- Step 4: 可行性 PASS（A-E 维度全部通过）
- Step 5-6: 完成

### Contract
- v1 冻结，假设验证通过

### Execute
- Step 1-2: 完成
- **P0 实验**: 3-seed 完成（full/A1/A2/A3 各 3 seed, same 2 seed）
  - 核心: stretch=1.099±0.012, delay=66.84ms, ≤1.2x%=86.2%
  - 消融: PE必要(A1≈随机), 多尺度有贡献(+2pp), 同规模完美(1.000)
  - Delay retention=109.9%

### 领域验证 (2026-05-24)
- Size generalization 是 GNN 理论问题，非 LEO 路由公认挑战
- 叙事定位调整为"跨领域技术迁移"
- Li 2026 排除（子agent幻觉，实际做意图编译）
- Stretch 合法但非主指标，E2E delay 为主
- Delay retention rate 为自造指标，需标注

## 关键决策

- D013: Contract 冻结
- D022: _build_neighbor_map bug 修复（单向→双向映射，stretch 从 2.1-2.6 降至 1.097）
- D023: 修复后加权 Dijkstra 评估结果确认（stretch 1.097, ≤1.2x 85.1%）
- D024: GRLR baseline 复现完成（stretch 1.008, delay 60.32ms）
- D025: Contract 两项核心指标达标（时延保留率 90.3%, vs Dijkstra 9.9%）
- D026: 消融 A1 — PE 是学习必要条件（移除 PE 训练精度降至 39.7%）
- D027: 消融 A2 — 单尺度训练 stretch 1.120（多尺度贡献 2-4pp）
- D028: 消融 A3 — 无PE+单尺度 stretch 1.049
- D029: 同规模消融 stretch 1.000（完美），9.7pp 差距完全来自跨规模迁移

## FR 检查清单

- [x] 奖励归一化审查（监督学习，无奖励函数）
- [x] Baseline 合法性（Dijkstra 为先验 baseline）
- [x] 方向可行性预判（GW 通过）
- [x] 参数溯源审计（Contract 冻结）
- [x] 仿真器验证（GW Step 7）
- [x] 反模式审查（无重大问题）
- [x] 预印本验证（Li 2026 排除）
- [x] MVE 先验对照（A1≈Dijkstra 先验）

## 待办

- [ ] Ch1 paper-materials 重写（3-seed 数据 + 领域验证叙事调整）
- [ ] random_pe 补跑（~20 min，3 seed）
- [ ] E06 hotspot（P1，~30 min）
- [ ] E08 GNN 深度（P1，~1-2h）
- [ ] 跨章符号统一 + 贡献差异化

## 结果文件

- `simulator/results/ch1_multi_seed_results.json` — P0 核心实验数据
- `simulator/results/ch1_batch_log.txt` — 批量实验日志
- `run_experiments.py` — 多 seed 批量实验脚本
