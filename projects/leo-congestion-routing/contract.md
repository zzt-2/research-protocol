---
created: 2026-05-17
status: frozen
version: 1
amendment:
  date: 2026-05-17
  reason: "MVE 用 K-path 逐流路由 beat ECMP 12%，正式模型偏离为 per-edge 同时路由导致 GNN/ECMP=1.07 FAIL。修正正式模型与 MVE 对齐。"
  changes:
    - "动作空间: per-edge continuous weights (E=264维) → per-flow discrete K-path selection (K=4)"
    - "路由方式: 同时路由所有流 → 逐流顺序路由"
    - "奖励: -MLU (绝对) → -(MLU_after - MLU_before) (增量)"
    - "模型输出: EdgeWeightDecoder → PathScoringHead (Categorical)"
    - "Episode: t_slots=20步 → n_flows=40步 (每步路由一条流)"
  unchanged: ["hypothesis 目标值", "success_signal", "failure_signal", "fairness_rules", "ablation_plan"]
  user_confirmed: true
---

# Research Contract: leo-congestion-routing

## Hypothesis

在 Walker delta LEO 卫星星座中，当链路故障率 ≥5% 且流量非均匀分布时，基于 GNN 消息传递的 per-link 负载均衡策略（GAT encoder → per-edge weight → 加权最短路路由）相比 ECMP 可降低最大链路利用率（MLU）≥10%，相比同架构 MLP（无 message passing）可降低 MLU ≥15%，且在不重新训练的情况下可泛化至训练规模 4×~10× 的星座，MLU 退化 <10%。

**理论依据**: GNN message passing 通过多跳聚合全局链路负载状态，在链路故障打破 ECMP 等价路径后仍能做出负载感知的分流决策（feasibility_report §A）。MVE-2 已验证 GNN/ECMP=0.88（改善 12%）、GNN/MLP=0.80（改善 20%）（decision_log D4）。

## Success Signal

**评估条件**: 66 节点 Walker delta 星座，8% 链路故障率，非均匀流量（25% 重型流 + 热点目的地），3 seeds × 500 episodes × 50 eval episodes。

1. **核心优势**: GNN MLU ≤ 0.90 × ECMP MLU（改善 ≥10%，与 MVE-2 一致）
2. **结构优势**: GNN MLU ≤ 0.85 × MLP MLU（改善 ≥15%，验证 message passing 价值）
3. **跨规模泛化**: 在 48/288/720 节点（训练规模 0.7×~10.9×）上，GNN（66 节点训练模型直接部署）MLU ≤ 1.10 × 同规模 ECMP MLU

三者均满足 → **Success**。

## Failure Signal

独立于 success signal，关注不同维度：

1. **无实用价值**: GNN MLU > 0.95 × ECMP MLU（改善 <5%，不值得额外部署复杂度）
2. **无结构优势**: GNN MLU > 0.95 × MLP MLU（GNN message passing 无贡献，核心假设不成立）
3. **泛化失败**: 在 ≥1 个泛化规模上，GNN MLU > 1.20 × 同规模 ECMP MLU（泛化后性能退化到比 ECMP 更差）

任一满足 → **Failure**。

## Baselines

- B1: **SP (Dijkstra)** (来源: 标准算法) — 复现状态: ✅ 已复现 (baselines/sp.py) — 交叉验证: 被 11/22 篇论文使用，领域绝对共识
- B2: **ECMP** (来源: 标准算法, Chiesa 2017) — 复现状态: ✅ 已复现 (baselines/ecmp.py) — 交叉验证: 被 L02 GMR/L04 PathGNN/L16 FlexSATE 使用，负载均衡标准方法
- B3: **MLP** (来源: 自实现消融对照) — 复现状态: ✅ 已复现 (baselines/mlp.py) — 交叉验证: L01 GRLR RLR 消融 / L07 Fan DQN 消融均使用 FC 对照验证 GNN 优势
- B4: **DTAR** (来源: Zhou 2026, arXiv:2604.12382, GitHub: ChenZ-code/DTAR_Routing) — 复现状态: ⏳ 待适配 — 交叉验证: 288 星域间路由标杆，有开源代码
- B5: **GMR-simplified** (来源: Huang 2024, TVT, DOI:10.1109/TVT.2023.3333848) — 复现状态: ⏳ 待自实现 (MPNN+DDPG, 去 PER, K=2) — 交叉验证: 41 引用，跨星座泛化标杆；**P4 风险**: 无代码+超参缺失，退守策略为放弃此 baseline

## Metrics

- M1: **MLU (Maximum Link Utilization)** — max_e(load_e / capacity_e)，主指标，越低越好。TE 核心指标 [来源: L04 PathGNN, L11 TELGEN]
- M2: **CV (Coefficient of Variation)** — std(link_util) / mean(link_util)，负载均衡质量，越低越好 [来源: L06 DTAR]
- M3: **Overflow Ratio** — count(load_e > capacity_e) / |E|，拥塞严重度，越低越好
- M4: **Generalization Gap** — MLU_test_scale / MLU_train_scale，跨规模性能保持度，越接近 1.0 越好 [来源: L02 GMR, L11 TELGEN]
- M5: **Convergence Speed** — 达到稳定 MLU（最近 50 episode 方差 < 0.01）所需 episodes，越少越好

## Fairness Rules

1. **数据一致**: 所有方法在相同 topology seeds × traffic seeds × fault seeds 组合上评估，共用同一组测试 episode
2. **目标一致**: 所有方法评估统一用 MLU；DTAR/GMR 各自原始奖励仅用于训练
3. **信息等价**:
   - GNN vs MLP: 相同输入特征（节点/边/流量），MLP 用全局拼接替代 message passing，参数量相当
   - DTAR/GMR: 保留各自原始观测/动作空间（已在各自论文中验证），但在相同拓扑和流量场景下评估
4. **超参预算等价**: 每个方法允许 3 次超参调优（lr × entropy coeff grid），GNN 不获得额外调优预算
5. **训练-测试分离**: 所有方法训练在 66 节点，泛化测试在 48/288/720 节点（零样本，不微调）
6. **已知不公平声明**:
   - DTAR 原始设计为域间路由（18 域，非全网 per-link），粒度差异在论文中需说明
   - GMR-simplified 去除 PER（原论文使用），性能可能低于原论文报告值

## Ablation Plan

| 编号 | 消融目标 | 预期影响方向 | 预期影响大小 | 理由 |
|------|---------|-------------|-------------|------|
| A1 | GNN → MLP (移除 message passing) | MLU 上升 | 大 (≥15%) | MVE-2 GNN/MLP=0.80，message passing 是核心优势来源 |
| A2 | 移除链路故障 (8%→0%) | GNN vs ECMP 差距缩小 | 大 | MVE-1 无故障 GNN≈ECMP，故障是优势激活条件 |
| A3 | 均匀流量 (去掉热点/重型流) | GNN vs ECMP 差距缩小 | 中 | 均匀流量下 ECMP 足够好 |
| A4 | GNN 层数 1/2/3 | 2 层最优 | 小 (±5%) | L06 DTAR 2 层最佳实践，过深可能过平滑 |
| A5 | 注意力头数 2/4/8 | 4 头最优，8 头边际 | 小 (±3%) | 标准配置 |

## Experiment List

| 编号 | 实验名 | 类型 | 优先级 | 说明 |
|------|--------|------|--------|------|
| E01 | 核心对比 | 核心 | P0 | GNN vs B1-B5, 66 节点, 8% 故障, 3 seeds × 500 eps |
| E02 | 无故障对照 | 对比 | P1 | 同 E01 但 fault_rate=0%, 验证故障激活条件 |
| E03 | 突发流量 | 对比 | P1 | 同 E01 但 surge_factor=5×, 验证拥塞适应 |
| E04 | 泛化 48 节点 | 核心 | P0 | 66 节点训练模型 → 48 节点测试 (0.7×) |
| E05 | 泛化 288 节点 | 核心 | P0 | 66 节点训练模型 → 288 节点测试 (4.4×) |
| E06 | 泛化 720 节点 | 核心 | P0 | 66 节点训练模型 → 720 节点测试 (10.9×) |
| E07 | 消融 GNN vs MLP | 消融 | P1 | 即 A1, E01 场景下对比 |
| E08 | 消融故障率 | 消融 | P1 | 即 A2, fault_rate ∈ {0%, 5%, 8%, 10%, 15%} |
| E09 | 消融流量均匀性 | 消融 | P2 | 即 A3, 热点比例 ∈ {0%, 3%, 5%, 10%} |
| E10 | 消融 GNN 层数 | 消融 | P2 | 即 A4, layers ∈ {1, 2, 3} |
| E11 | 消融注意力头数 | 消融 | P2 | 即 A5, heads ∈ {2, 4, 8} |
| E12 | 故障模式对比 | 鲁棒 | P2 | 随机 vs 区域 vs 级联故障 |

## Simulation Config

### 星座配置

- 星座类型: Walker delta (F=0, 4-ISL MSN 拓扑)
- 训练规模: P=6, S=11 → 66 节点 [来源: L02 GMR §V Iridium]
- 泛化测试: 48 (4×12) / 288 (12×24) / 720 (36×20) [来源: L02/L06/L01]
- 轨道高度: 780 km [来源: Iridium specification, L02 GMR]
- 倾角: 86.4° [来源: Iridium specification]
- ISL 配置: 4 ISL/sat (2 intra-plane ring + 2 inter-plane)
- ISL 容量: 10 Gbps [设计选择: 光学 ISL 量级, 与 Starlink v2 激光链路对齐。MVE 验证 MLU ∈ [0.8,1.5]]
- ISL 带宽: 500 MHz [来源: L06 DTAR §V]

### 流量模型

- 类型: 非均匀，重型/轻型两档
- 流数量: 40 (66 节点, 约 0.6 flows/node) [设计选择: MVE 验证配置]
- 重型流: 10 条 (25%), demand ~ U(3, 5) Gbps [设计选择: 接近 ISL 容量 50%, 制造拥塞]
- 轻型流: 30 条 (75%), demand ~ U(0.1, 1.0) Gbps [设计选择: 背景流量]
- 热点目的地: 3 个节点 (~5%) [设计选择: 非均匀性来源]
- 突发因子: μ = 5× [来源: L06 DTAR §V surge indicator]
- 时变模式: NHPP λ(t) = λ₀(1 + sin(2πt/T)) [来源: L10 ST-QoS §III]

### 故障模型

- 基础故障率: 8% [来源: MVE-2 验证配置, decision_log D4]
- 故障分布: 随机独立移除 ISL
- 区域故障 (消融): 10% 节点周围链路全断 [设计选择: 极端场景消融, 模拟太阳风暴/碎片事件]

### GNN 架构

- Encoder: GAT, 2 层, 4 注意力头, hidden_dim = 64 [来源: L06 DTAR §IV GAT+LN+Residual]
- Normalization: LayerNorm + Residual connection [来源: L06 DTAR]
- Readout: PathScoringHead (mean path emb → MLP → K scores → Categorical)
- 输出: K 个候选路径的离散选择概率 (K=4, Categorical 分布)
- 激活: ELU [来源: L06 DTAR]

### RL 训练配置

- 算法: PPO + GAE [来源: L06 DTAR, L01 GRLR]
- clip ε: 0.2 [来源: L03 POMAP §IV, 标准值]
- Learning rate: 3e-4 [来源: MVE 配置, Adam 默认]
- Entropy coefficient: 0.01 [来源: MVE 配置]
- Discount factor γ: 0.99 [来源: 标准]
- GAE λ: 0.95 [来源: 标准]
- Optimizer: Adam
- Episode 结构: 逐流顺序路由, 每步路由一条流, 共 n_flows 步 [来源: MVE K-path 范式]
- Episodes: 500 [设计选择: MVE 150 → 增大]
- Seeds: ≥3 [设计选择: 统计显著性]
- 评估 episodes: 50 [设计选择: MVE 20 → 增大]
- Early stopping: 连续 50 episode 无改善
- Logging: wandb

### 评估条件

- 主评估场景: 66 节点, 8% 故障, 非均匀流量, 无突发
- 统计报告: mean ± std over 3 seeds, 每场景 50 eval episodes
- 泛化评估: 48/288/720 节点, 同流量模型(按节点数缩放), 同故障率

## 数据集设计

### 参数空间

| 参数 | 取值范围 | 文献溯源 | 备注 |
|------|---------|---------|------|
| 星座规模 | 48/66/288/720 节点 | [来源: L02/L06/L01] | 固定 4 档 |
| 轨道高度 | 780 km | [来源: Iridium spec] | 固定 |
| 倾角 | 86.4° | [来源: Iridium spec] | 固定 |
| 流量流数 | 0.6 × N_nodes | [设计选择: MVE 验证] | 按节点数线性缩放 |
| 重型流比例 | 25% | [设计选择: 80/20 近似] | |
| 重型需求 | U(3, 5) Gbps | [设计选择: ~50% ISL capacity] | |
| 轻型需求 | U(0.1, 1.0) Gbps | [设计选择: 背景流量] | |
| 热点比例 | 5% | [设计选择: 非均匀性] | |
| 故障率 | 0%~15% | [来源: MVE-2, 8% 默认] | 消融: 0/5/8/10/15 |
| 突发因子 | 1× / 5× | [来源: L06 DTAR] | |
| 时变模式 | NHPP sin | [来源: L10 ST-QoS] | |

### 数据规模与划分

- 训练: 3 seeds × 500 episodes（在线生成）
- 测试: 3 seeds × 50 episodes（独立随机种子）
- 泛化测试: 每规模 3 seeds × 50 episodes
- 无预存数据集（在线生成，固定种子保证可复现）

## Parameter Provenance

| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| 训练星座 66 节点 | P=6, S=11 | [来源: L02 GMR §V] | Iridium 66 星 |
| 泛化 48 | P=4, S=12 | [来源: L02 GMR §V] | GlobalStar 48 星 |
| 泛化 288 | P=12, S=24 | [来源: L06 DTAR §V] | |
| 泛化 720 | P=36, S=20 | [来源: L01 GRLR §V] | |
| 轨道高度 | 780 km | [来源: Iridium spec, L02 GMR] | |
| 倾角 | 86.4° | [来源: Iridium specification] | |
| ISL 容量 | 10 Gbps | [设计选择: 光学 ISL 量级, 与 Starlink v2 激光链路对齐。绝对值不影响方法间相对对比, 决定性参数为 demand/capacity ratio。MVE 验证当前参数下 MLU ∈ [0.8,1.5], 拥塞场景合理] | |
| ISL 带宽 | 500 MHz | [来源: L06 DTAR §V] | Ka 频段 |
| 流数量 40 | 40 (66 节点) | [设计选择: MVE 验证, 0.6/node] | |
| 重型流比例 | 25% | [设计选择: 80/20 近似] | |
| 重型需求 | U(3, 5) Gbps | [设计选择: ~50% ISL cap] | |
| 轻型需求 | U(0.1, 1.0) Gbps | [设计选择: 背景流量] | |
| 热点目的地 | 3 (5%) | [设计选择: 非均匀性] | |
| 突发因子 | 5× | [来源: L06 DTAR §V] | |
| NHPP 模式 | sin(2πt/T) | [来源: L10 ST-QoS §III] | |
| 故障率 | 8% | [来源: MVE-2, D4] | GNN 优势激活条件 |
| 区域故障 | 10% 节点周围 | [设计选择: 极端场景消融, 模拟太阳风暴/碎片事件集中故障。10% (~7 节点) 足以施压但不致网络分区] | |
| GAT 2 层 4 头 64 | 2/4/64 | [来源: L06 DTAR §IV] | LN + Residual |
| PPO+GAE | PPO | [来源: L06 DTAR, L01 GRLR] | |
| clip ε | 0.2 | [来源: L03 POMAP §IV] | 标准值 |
| lr | 3e-4 | [来源: MVE 配置] | Adam 默认 |
| entropy coeff | 0.01 | [来源: MVE 配置] | |
| γ | 0.99 | [来源: 标准 RL] | |
| GAE λ | 0.95 | [来源: 标准 PPO] | |
| episodes | 500 | [设计选择: MVE 150→增] | |
| seeds | ≥3 | [设计选择: 统计显著性] | |
| eval episodes | 50 | [设计选择: MVE 20→增] | |
