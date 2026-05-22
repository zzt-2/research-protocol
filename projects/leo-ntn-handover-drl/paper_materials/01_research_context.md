# 研究上下文

## 1. 问题定义

### 1.1 LEO 卫星切换的具体挑战

LEO 卫星（500-2000 km 轨道）相对地面高速运动（~7.5 km/s），导致覆盖时间极短、切换极为频繁。

| 指标 | 数值 | 来源 |
|------|------|------|
| 星座规模 | 18面×22星=396星，550km，53°倾角（Walker-delta） | 来源：baseline_report §1.3 |
| 平均可见卫星数 | 4.4 颗/UE，范围 2-6 颗 | 来源：baseline_report §1.2 |
| 最小仰角 | 20°（低于此卫星不可见） | 来源：baseline_report §1.3 |
| 决策间隔 | 10s | 来源：baseline_report §1.3 |
| 仿真时长 | 2h（720 步） | 来源：baseline_report §1.3 |
| 频段 | Ku 12 GHz，250 MHz | 来源：baseline_report §1.3 |
| 卫星容量 | 10 信道/星 | 来源：baseline_report §1.3 |

核心矛盾：卫星快速移动导致 UE 频繁面临卫星切换，且多 UE 同时可见同一卫星子集引发负载竞争。传统方法（如 A3/MVT）以单 UE 视角选星，无法感知全局负载分布。

### 1.2 多 UE 场景的负载聚集问题

传统启发式 HHS 在 15 UE 场景下的实验数据：

| 指标 | HHS (B1) | Random (B4) | 差距 |
|------|----------|-------------|------|
| 吞吐量 | 20,911 Mbps | 36,105 Mbps | -42% |
| **阻塞率** | **37.4%** | 0.02% | +37.4pp |
| 切换次数 | 877 | 8,435 | -90% |

来源：baseline_report §2.2

**根因**：HHS 原为单 UE 算法（L08），多 UE 独立决策时稳定性奖励使 UE 粘滞在同一卫星，超过容量限制导致阻塞。这是传统方法在多 UE 场景的结构性局限，也是 DRL 的核心改进空间。（来源：baseline_report §5）

B2 Dueling DDQN 在 15 UE 下初始阻塞率 ~25%（396 维动作空间，reward 仅 4866），经 top-K 压缩后降至 0%。50 UE 时 B2 因 396 维动作空间导致 CUDA 崩溃。（来源：decision_log D031）

---

## 2. 现有方法局限

| # | 局限 | 证据论文 | 具体事实 |
|---|------|---------|---------|
| L1 | **仿真规模有限** | literature_notes 综合分析 | 所有论文仿真 3-298 星、10-200 UE，与 mega-constellation（数千星、百万 UE）差距大。L029 仅 10-30 UE，L018 仅 10 终端。 |
| L2 | **奖励设计缺乏理论** | L004 (arXiv:2604.03562) | L004 揭示自适应奖励的"切换-稳定性困境"：PPO 需准稳态奖励收敛，动态权重导致性能下降。近恒定权重（342.1 Mbps）大幅优于动态权重（103.3±96.8 Mbps）。多数论文奖励依赖经验调参。来源：literature_notes [L004] |
| L3 | **可扩展性未验证** | literature_notes 综合分析 | DRL 训练随 UE/卫星数量增长的计算和样本复杂度问题未充分解决。B2 在 50 UE 时 CUDA 崩溃（396 维动作空间）。来源：decision_log D031 |
| L4 | **信道/环境简化** | literature_notes 综合分析 | 多数假设 CSI 可获取、轨道模式已知固定，未考虑多小区干扰和 ISL。来源：literature_notes §已知局限 |
| L5 | **flat observation 信息浪费** | novelty_search §C2 | B2 flat obs 维度 1585（396×4+1），有效数据仅 ~18 维（avg 4.4 可见卫星），利用率 1.1%。zero-padding 浪费 ~45% FC 计算。来源：novelty_search §A4 |
| L6 | **无规模泛化能力** | decision_log D029 | MLP（C6）从 20 UE 迁移到 100 UE 完全崩溃（reward -9,710，71.5% 阻塞），固定维度输入无法适应 UE 数量变化。来源：decision_log D029 |

---

## 3. 研究空白

### 3.1 Size generalization 在 LEO 切换领域的空白

四组系统检索（S2 + OpenAlex）结果：

| 搜索组 | 关键词 | 结果数 | 存档 |
|--------|--------|--------|------|
| scale-gnn | "LEO satellite handover GNN graph neural network scalability user" | 30 | contract-scale-gnn.json |
| scale-bipartite | "satellite handover load balancing DRL multi-user bipartite graph" | 30 | contract-scale-bipartite.json |
| size-generalization | "GNN size generalization wireless resource allocation scalable" | 30 | contract-size-generalization.json |
| scale-dense | "LEO NTN handover dense multi-user load-aware neural network" | 30 | contract-scale-dense.json |

来源：novelty_search §Size Generalization 检索

**结论**：size generalization 在 LEO 切换中完全空白。Jayarajan 2025 做了初步的 100→200 规模测试，但在网络侧分配场景而非切换场景。（来源：novelty_search §新颖性结论）

### 3.2 GNN vs MLP 优势阈值的文献证据

| UE/Agent 规模 | GNN vs MLP 表现 | 来源 |
|---------------|----------------|------|
| N ≤ 10 | MLP 够用，GNN 优势有限 | Lee et al. 2023 (Frontiers) |
| 10 < N < 30 | GNN 开始显著优于 MLP | Lee et al. 2023, Shen et al. 2019 |
| N ≥ 30-40 | MLP 可能崩溃，GNN 不可替代 | Lee et al. 2023, Eisen & Ribeiro 2020 |

来源：novelty_search §GNN vs MLP 优势阈值

关键理论支撑：
- **Wu et al. 2022**：GNN size generalization 理论，mean aggregator 的跨规模泛化条件
- **Garcia Camargo et al. 2025**：稀疏随机几何图上的 GNN 可迁移性形式化证明
- **Shen et al. 2019 (IGCNet)**：无线功率控制，MLP 在大规模网络性能急剧退化
- **Lee et al. 2023**：多智能体防御，N>40 时 MLP 甚至劣于随机

来源：novelty_search §关键文献

### 3.3 "UE 数量对切换算法性能影响"的空白确认

文献中所有 LEO 切换 DRL 论文均在固定 UE 数量下评估（L029: 10-30 UE, L018: 10 终端, L024: 10-200 UE 但无跨规模分析）。**没有任何论文系统研究 UE 数量对切换算法性能的影响。** 来源：novelty_search §新颖性结论 + literature_notes 综合分析

---

## 4. 新颖性确认

### 4.1 四要素组合

**"二部图 GNN + DDQN + size generalization + LEO 切换"**四要素组合在现有文献中无完全先例。

来源：decision_log D032

### 4.2 竞品排除记录

| 论文 | 覆盖要素 | 缺失要素 | 威胁等级 |
|------|---------|---------|---------|
| Lee 2025 (ICT Express) | GNN + 分布式 LEO 切换 + 负载均衡 | 无 DRL、非二部图、可扩展性仅为固有性质声明 | 低-中 |
| Eydian 2025 (IEEE OJCOMS) | 加权二部图匹配 + LEO 切换 | 无 GNN、无 RL、经典优化 | 低 |
| Chou 2026 (arXiv:2605.02416) | Dueling DDQN + 多目标 LEO 切换 | 无 GNN、无二部图、无 size generalization | 低-中 |
| Kim 2022 (IEEE TWC, BGNN) | 二部图 GNN + 波束赋形 + 跨规模可扩展 | 非切换场景、无 DRL | 低-中 |
| Fan 2026 (Springer) | GNN + DQN | ISL 路由非切换 | 低 |
| Jayarajan 2025 (GT) | 异构图分配 | 无 RL | 低 |
| Wang 2025 (IEEE ICCC) | GNN + UE-UAV 接入 | UAV 非卫星切换 | 低 |
| ARTHF (Fan 2025, MDPI) | Self-attention + Dueling Rainbow + 负载 | 无 GNN、无二部图、无规模泛化 | 中 |

来源：decision_log D032 + novelty_search §空隙确认

### 4.3 新颖性检索通过的证据

- **第一轮检索**：3 路并行（方案 A/B/C 新颖性评估），结论"三元组合无人占据"。来源：novelty_search §检索结论
- **第二轮检索**：叙事转向后 4 组系统检索（scale-gnn/scale-bipartite/size-generalization/scale-dense），120 篇结果，无高度重叠竞争者。来源：novelty_search §文献检索
- **第三轮检索**：D024 二次检索（Fan 2026/Jayarajan/Wang 2025）+ IEEE Xplore 补充检索（7 组 site:ieeexplore + OpenAlex），新发现 1 篇中等重叠（Wiriya 2025，传统图匹配非 GNN/DRL）。来源：decision_log D032
- **总计**：14+ 组系统检索，所有竞品均为部分覆盖，无四要素完全重叠。

---

## 5. 论文叙事弧线

三级递进实验设计，对应 GNN 优势从无到有的文献阈值（来源：decision_log D025, D030）：

### 第一级：20 UE 基线可行性（GNN ≈ MLP）

- 目的：建立公平比较基线，验证 GNN+top-K 方案在小规模下不劣于 MLP+top-K
- 预期：GNN 在 20 UE 下与 MLP 性能接近（GNN vs MLP gap ≈ 0%，实测 -0.13%）
- 意义：排除"GNN 以牺牲小规模性能换取泛化性"的质疑
- 文献支撑：Lee 2023 确认 N<20 时 MLP 够用
- 来源：decision_log D022, D023

### 第二级：50-100 UE 规模扩展（MLP 退化，GNN 稳定）

- 目的：展示 GNN 在负载竞争足够强时的结构性优势
- 实验数据（100 UE, cap=25）：

| 指标 | GNN (E4) | MLP (C6) | GNN 优势 |
|------|----------|----------|---------|
| Reward | 45,313 | 33,843 | **+34%** |
| 阻塞率 | 8.56% | 20.6% | **-58%** |

- 50 UE 迁移：GNN 比 MLP 高 61.5%（远超 execute_v2 的 15% 成功阈值）
- 意义：文献阈值 N>20-30 在 LEO 切换场景中得到实验验证
- 来源：decision_log D028, D030

### 第三级：Size Generalization（20 UE 训练 → 50/100 UE 直接推理）

- 核心实验：20 UE 训练的模型直接部署到 100 UE 场景

| 迁移方向 | GNN Reward | MLP Reward | GNN 优势 |
|---------|-----------|-----------|---------|
| 20→100 UE | 35,699（正值） | -9,710（崩溃） | **绝对差 45,409** |
| 50→100 UE | GNN +61.5% over MLP | — | 显著 |

- 意义：GNN 的 permutation equivariance 使参数在 UE 数量变化时保持语义；MLP 固定维度输入无法泛化
- 工程价值：小规模训练、大规模部署，大幅降低 DRL 训练成本
- 来源：decision_log D029

---

## 6. 论证主线建议稿

LEO 卫星网络的高速移动性导致频繁切换，传统方法以单 UE 视角选星，在多 UE 场景下因负载聚集产生高阻塞率（HHS 37.4%）。现有 DRL 方法虽然缓解了此问题，但使用 flat observation 将 UE-卫星关系展平为固定维度向量，既浪费了 98.9% 的输入维度，又丧失了跨规模泛化能力——当 UE 数量从 20 增至 100 时 MLP 完全崩溃。本研究提出基于二部图 GNN 编码的 Dueling DDQN 切换架构：通过 top-K 候选压缩将动作空间从 396 降至 6，GNN 消息传递让每个 UE 感知邻居卫星的负载状态，分解式 Q 函数将参数量从 490K 压缩至 25,858（19× 压缩）。实验结果表明，该方法在 100 UE 下阻塞率比 MLP 降低 58%（reward +34%），且支持 zero-shot 规模迁移：20 UE 训练的模型直接部署到 100 UE 场景获得正值 reward，而同等条件下 MLP 迁移崩溃（71.5% 阻塞）。

---

## 7. Gap-Contribution 闭环映射

| Gap | 对应方法组件 | 结论回应 | 数据证据 |
|-----|------------|---------|---------|
| **G1**: 传统方法多 UE 负载聚集（HHS 37.4% 阻塞） | top-K 候选压缩 + 分解式 Q 函数（负载感知动作空间） | top-K 将 B2 的 25% 阻塞率降至 0%，GNN 进一步在大规模下保持低阻塞 | B2 25%→C6 0%（15 UE）; E4 100 UE 8.56% vs C6 20.6% |
| **G2**: flat observation 信息浪费（1.1% 利用率）+ 固定维度不可扩展 | 二部图 GNN 编码（352 维结构化表示 vs 1585 维冗余向量） | GNN 参数在 UE/卫星间共享，自然支持可变图规模 | 参数量 25,858 vs 490,125（19× 压缩）; 20→100 UE 零样本迁移成功 |
| **G3**: DRL 无规模泛化能力（MLP 跨规模崩溃） | GNN permutation equivariance + size generalization 训练策略 | 20 UE 训练的 GNN 直接部署到 100 UE 获得正 reward，MLP 崩溃至 -9,710 | 20→100: GNN 35,699 vs MLP -9,710（绝对差 45,409） |
| **G4**: 奖励尺度失衡导致 DRL 退化为贪心 | 归一化 rate（R_norm）+ 增大阻塞惩罚 β | v2 奖励函数通过 MDP checkpoint 验证：策略区分度 120%，无单项>95% | Random 586.7 vs Greedy -118.0（baseline_report §1.2） |

来源：G1 来自 baseline_report §2.2 + decision_log D022; G2 来自 novelty_search §C2 + D029; G3 来自 D029; G4 来自 baseline_report §1.2 + D005/D006

---

## 8. 待补充标记

以下细节需从论文原文补充：

| 待补充项 | 建议查阅论文 | 优先级 |
|---------|------------|--------|
| ARTHF 的 attention softmax 是否真的在有效卫星间计算（Eq.27 M_k^t 的精确定义） | ARTHF (Fan 2025, MDPI Electronics 14(15), 3040) 全文 Eq.26-28 | 中 |
| L029 Dueling DDQN 奖励函数的三目标自适应加权具体公式 | L029 (Chou 2026, arXiv:2605.02416) 全文 | 中 |
| Lee 2025 (ICT Express) 的 GNN 可扩展性声明是显式实验还是固有性质推断 | Lee 2025 ICT Express 全文 | 高（影响新颖性论证） |
| Kim 2022 BGNN 的跨规模实验设置（训练规模→测试规模的具体数值） | Kim 2022 (IEEE TWC, arXiv:2207.05364) | 中 |
| Wu 2022 size generalization 理论的具体条件（mean aggregator + 什么假设） | Wu 2022 全文 | 高（理论支撑） |
| Shen 2019 IGCNet 的 MLP 退化拐点精确数据（N=? 时 MLP 崩溃） | Shen et al. 2019 (IGCNet) | 中 |
| L018 的 EMODRL 在不同 UE 数量下的性能数据（如有） | L018 (JSAC 2024, DOI:10.1109/JSAC.2024.3459029) | 低 |
| L15/Lee 2025 的二部图 GNN 50 UE→其他规模的泛化数据 | Lee 2025 ICT Express 全文 | 高 |
| Garcia Camargo 2025 GNN 可迁移性证明的适用条件（图类型、聚合函数约束） | Garcia Camargo et al. 2025 全文 | 高（理论支撑） |
| sat_capacity 按比例调整的工程合理性论证（cap=10→15→25 的依据） | 需参考 3GPP TR 38.821 或运营商容量规划文献 | 中 |
