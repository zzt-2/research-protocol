---
created: 2026-05-13
status: frozen
version: 1
---

# Research Contract

## Hypothesis

在 Walker-Delta LEO 卫星网络中，使用**轨道位置编码 (Orbital PE)** 和**多尺度混合训练**的 GNN 路由策略，在小星座 (≤100 卫星) 上训练后，可以零样本泛化到 11x 更大的星座 (720 卫星)，端到端时延性能保留率 ≥80%（相对于同规模训练的 GNN），且端到端时延与 Dijkstra 最优路由差距 ≤20%。

位置编码通过编码卫星在星座结构中的相对位置 (轨道面编号/总面数、面内序号/面内总数)，使 GNN 学到规模无关的路由策略。

## Success Signal

1. **规模泛化成功**：核心方法 (GNN + Orbital PE + 多尺度训练) 在 66→720 (11x) 零样本迁移下，平均端到端时延保留率 ≥80%，即 cross-scale delay / same-scale delay ≤ 1.25
2. **实用价值成立**：在 720 卫星目标规模上，核心方法平均时延与 Dijkstra 差距 ≤20%
3. **PE 关键性确认**：消融实验中，移除 PE 导致保留率下降 ≥8 个百分点

以上 3 条需同时满足。

## Failure Signal

1. **方法基础失败**：同规模 GNN 路由 (无 PE、同规模训练) 平均时延 > 1.5x Dijkstra → GNN 路由方法本身不适用
2. **泛化灾难性失败**：跨规模 GNN 时延 > 1.8x 同规模 GNN (保留率 < 56%) → 规模泛化不可行
3. **PE 无贡献**：移除 PE 后保留率变化 < 3pp → PE 不是泛化的关键因素，核心假设被否定

以上任一条成立即为失败。

## Baselines

- B1: **Dijkstra 最短路径** (来源: 领域共识) — 复现状态: 待实现 — 交叉验证: 19+ 篇论文使用，Groundwork 田野调查 15/40 篇以此为 baseline
- B2: **GRLR** (来源: TVT 2025, DOI:10.1109/TVT.2024.3471658, 44 引用) — 复现状态: 待复现 — 交叉验证: GNN+Actor-Critic LEO 路由标杆，被 L14-L18 引用对比。同架构对比确保结论干净 (都使用 GNN+RL，差异仅在 PE + 跨规模)
- B3: **GraphPR** (来源: 2025, DOI:10.1109/TVT.2024.3499933) — 复现状态: 待复现 — 交叉验证: GAT+MADRL 分布式路由，推荐级 baseline

## Metrics

- M1: **平均端到端时延** (ms) — 所有流量的端到端传输时延均值 — 越低越好
- M2: **最大链路利用率** (%) — 所有 ISL 中最高利用率 — 越低越好 (负载均衡)
- M3: **P95 端到端时延** (ms) — 95th 百分位时延 — 越低越好 (尾延迟)
- M4: **规模泛化保留率** = same-scale delay / cross-scale delay — 越高越好，1.0 = 无退化
- M5: **路径最优性比** (%) — 时延在 Dijkstra 最优路径 1.2x 以内的流量比例 — 越高越好

## Fairness Rules

- 所有方法使用相同的拓扑快照、流量矩阵、ISL 容量模型
- GRLR 和核心方法使用相同的 GNN+RL 框架 (Actor-Critic, PPO)，相同训练步数/epoch 预算
- 超参搜索预算相同：每个方法 3 组超参配置，取最优
- Dijkstra 为非学习方法，每个快照独立计算最优路径，作为性能上界参考
- **不公平之处**：核心方法在多规模混合训练 (66+100+200) 上训练，GRLR 仅在目标规模 (720) 训练。GRLR 训练数据更多但规模单一，核心方法训练数据少但覆盖多规模。这是实验设计本身的要求 (对比跨规模 vs 同规模训练)，非可消除的不公平

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 |
|------|---------|-------------|-------------|
| A1 | 移除 Orbital PE | 保留率下降 | 大 (≥8pp) |
| A2 | 移除多尺度训练 (仅单规模 100 星训练) | 保留率下降 | 中 (5-8pp) |
| A3 | 同时移除 PE 和多尺度训练 | 保留率显著下降 | 大 (≥15pp) |
| A4 | GNN 深度 4 层 vs 2 层 | 同规模改善但跨规模可能退化 (过平滑) | 中 |
| A5 | PE 类型: 轨道位置 vs 随机 PE vs 无 PE | 轨道 PE > 随机 PE > 无 PE | 中-大 |

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 |
|------|--------|------|--------|
| E01 | 核心实验: 66→720 跨规模泛化 | 核心 | P0 |
| E02 | 对比实验: 核心 vs Dijkstra vs GRLR vs GraphPR (720 星) | 对比 | P0 |
| E03 | 消融 A1: 移除 PE | 消融 | P0 |
| E04 | 消融 A2: 移除多尺度训练 | 消融 | P1 |
| E05 | 消融 A3: 同时移除 PE + 多尺度 | 消融 | P1 |
| E06 | 鲁棒性: 不同流量模式 (uniform/hotspot/distance) | 鲁棒 | P1 |
| E07 | 鲁棒性: 不同规模因子 (5x/11x/24x, 即 720/1584) | 鲁棒 | P1 |
| E08 | 消融 A4: GNN 深度影响 | 消融 | P2 |
| E09 | 消融 A5: PE 类型对比 | 消融 | P2 |

## Simulation Config

### 星座参数
- **星座类型**: Walker-Delta (单壳层)
- **训练规模**: 66 星 (6面×11星), 100 星 (10面×10星), 200 星 (10面×20星) — 多尺度混合
- **目标规模**: 720 星 (18面×40星)
- **扩展目标**: 1584 星 (72面×22星, Starlink Phase 1)
- **轨道高度**: 550 km
- **轨道倾角**: 53°
- **ISL 拓扑**: +Grid (每星 4 ISL: 2 轨内 + 2 轨间)

### 信道/链路模型
- **ISL 容量**: Shannon-Hartley, C = B log₂(1 + SNR), B=500 MHz, 参考距离 5000 km
- **ISL 时延**: 传播时延 = d/c, d = ISL 几何距离 (由轨道力学计算)
- **ISL 距离**: 轨内 ~2700 km, 轨间 ~5500 km (550 km 高度 Walker-Delta)
- **最小仰角**: 25° (GSL, 用于地面站接入判断)
- **流量模型**: (a) uniform: 每对节点等概率 (b) hotspot: 10% 节点产生 50% 流量 (c) distance-weighted: 近距离流量概率高

### GNN + RL 配置
- **GNN**: GAT (Graph Attention Network), 2-3 层, hidden dim 64, multi-head attention (4 heads)
- **Orbital PE**: sin/cos 编码 (plane_idx/P, sat_idx/S)，维度 16，附加到节点特征
- **RL**: PPO (Proximal Policy Optimization), Actor-Critic 架构
- **观测空间**: 节点特征 = [队列长度, 当前时延, Orbital PE] + 边特征 = [ISL 距离, 当前利用率]
- **动作空间**: 每个流量包选择下一跳 ISL (4 选 1)
- **奖励**: 负端到端时延 + 拥塞惩罚 (链路利用率 > 阈值)
- **训练**: 多尺度混合 (从 66/100/200 星随机采样), 1000 episodes, 学习率 3e-4

### 评估条件
- 每个实验 5 个随机种子取均值 ± 标准差
- 快照间隔: 60 秒 (轨道周期 ~96 分钟, 约 96 个快照/周期)
- 评估: 10 个拓扑快照 × 5 种流量矩阵 = 50 个测试场景
- 统计显著性: Welch's t-test, p < 0.05

### 参数来源

| 参数 | 值 | 来源 |
|------|-----|------|
| 轨道高度 550 km | Starlink Shell 1 | L02 Starfield |
| ISL 容量 Shannon 模型 | B=500MHz | L03 DuJo, L02 Starfield |
| +Grid ISL 拓扑 | 4 ISL/sat | L04 ISL Pattern |
| PPO 学习率 3e-4 | 标准 DRL 配置 | [ASSUMPTION] 待调参 |
| 快照间隔 60s | 卫星拓扑变化率 | L10 MCSR |
| 最小仰角 25° | Starlink 标准 | L02 Starfield |
