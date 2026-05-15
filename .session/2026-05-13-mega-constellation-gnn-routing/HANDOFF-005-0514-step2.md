# Handoff 2026-05-14 (Round 2)

## 当前进度
- 阶段：Execute Step 2（核心实验 — baseline 对比完成，消融实验待做）
- 状态：Baseline 对比结果积极，Contract 核心指标达标
- Contract 状态：frozen
- 本轮完成：
  - 发现并修复 `_build_neighbor_map` bug（单向映射→双向映射，D022）
  - 修复后重新评估：mean stretch 1.097, median 1.056, 85.1% ≤1.2x optimal（D023）
  - GRLR 论文下载+精读+复现（6节点局部图 GAT + Actor-Critic, D024）
  - GRLR 加权 Dijkstra 评估：mean stretch 1.008, 100% ≤1.2x（D024）
  - 三方对比表生成：Dijkstra / GRLR / 我们的方法（D025）
  - 时延保留率 90.3%，vs Dijkstra 差距 9.9% — Contract 两项核心指标达标

## 关键数据

### 修复 neighbor_map 前后对比
| 指标 | 修复前(2/4方向) | 修复后(4/4方向) |
|------|----------------|----------------|
| Mean stretch | 2.1-2.6 | 1.097 |
| Median stretch | 1.5-1.8 | 1.056 |
| P95 stretch | 5-7 | 1.315 |
| ≤1.2x optimal | — | 85.1% |

### Baseline 对比（720星，加权 Dijkstra 推理）
| 指标 | Dijkstra | GRLR(同规模) | 我们(跨规模) |
|------|----------|-------------|-------------|
| Mean stretch | 1.000 | 1.008 | 1.097 |
| Median stretch | 1.000 | 1.000 | 1.056 |
| ≤1.2x optimal | 100% | 100% | 85.1% |
| Mean delay(ms) | 60.77 | 60.32 | 66.77 |

### Contract 指标达标情况
- [✓] 时延保留率 90.3% ≥ 80%
- [✓] vs Dijkstra 差距 9.9% ≤ 20%
- [ ] PE 关键性 ≥8pp — 消融实验 A1 待做

### 仿真器文件索引（simulator/）
| 文件 | 用途 | 状态 |
|------|------|------|
| config.py | 全局参数 | ✓ |
| constellation.py | Walker-Delta 星座 | ✓ |
| topology.py | +Grid ISL 拓扑 | ✓ |
| channel.py | Shannon 容量 | ✓ |
| traffic.py | 流量模型 | ✓ |
| routing.py | Dijkstra | ✓ |
| snapshot.py | PyG 图 + PE | ✓ |
| models.py | RoutingGNN + RoutingActorCritic | ✓ |
| smoke_test.py | 物理验证 | ✓ (通过) |
| quick_test.py | 监督泛化测试 | ✓ (retention 70%) |
| env.py | RL 环境 | ✓ (neighbor_map bug已修复) |
| pretrain.py | 监督预训练 | ✓ |
| train.py | PPO 微调 | ✓ (无效) |
| grlr_model.py | GRLR 6节点GAT+AC | ✓ (新建) |
| grlr_train.py | GRLR 训练 | ✓ (2000 eps) |
| grlr_eval.py | GRLR 评估(贪心+加权) | ✓ (新建) |
| pretrained.pt | 监督预训练权重 | ✓ (72,965 params) |
| grlr_trained.pt | GRLR 训练权重 | ✓ (6,565 params) |

## 下一步
1. **消融实验 A1**：移除 Orbital PE，重新预训练+评估，验证 PE 贡献 ≥8pp
2. **消融实验 A2**：移除多尺度训练（仅单规模 100 星训练），评估跨规模性能
3. **同规模消融**：我们的架构在 720 星训练+测试，分离架构 vs 规模泛化的影响
4. **完整实验 E01-E09**：跑 Contract 中所有实验

## 文件路径
- Decision log：`decision_log.md`（D001-D025）
- Contract：`contract.md`（frozen）
- GRLR 论文：`papers/doi/10.1109_tvt.2024.3471658/content.md`
- 仿真器：`simulator/`（16 个 .py 文件 + 2 个 .pt 权重）
