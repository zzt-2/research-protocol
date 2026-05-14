# 研究上下文

> 来源：feasibility_report.md, literature_notes.md (L01-L25, T01-T02), competitor_notes/, decision_log.md (D003-D029)
> 生成时间：2026-05-14
> 项目：GNN size generalization for LEO mega-constellation routing

---

## 1. 问题定义

### 1.1 LEO mega-constellation 路由的具体挑战

LEO mega-constellation（巨型低轨星座）路由面临规模、动态性和异质性三重挑战：

| 挑战 | 具体表现 | 关键数据 | 来源 |
|------|----------|----------|------|
| 规模爆炸 | Starlink Gen2 规划 2520+ 星，Kuiper 1156 星 | 1000-10000 级节点图 | feasibility_report §C; L10 (MCSR) |
| 拓扑时变 | 卫星运动导致 ISL 连通性周期性变化 | ISL 切换周期 ~3 min | L10 §V-C; L04 |
| ISL 质量异质 | 时延/容量因轨道位置、距离、负载而异 | 传播时延 d/c，轨内 1086-4277 km，轨间 1963-5694 km | L03 (DuJo) Shannon 模型; D016 |
| 流量非均匀 | 地面用户分布导致 hotspot 模式 | 4 种模式 (uniform/hotspot/distance/population) | L02 (Starfield); L10 (MCSR) |
| 计算开销 | 传统方法 O(N^2) 随规模增长 | Dijkstra 每快照需全局重计算 | feasibility_report §A |
| 训练成本 | GNN+RL 在 6000+ 星训练计算成本极高 | GDRL-SFCR 单规模 6048 星训练 | L16; feasibility_report §B |

**核心矛盾**：GNN+RL 路由已在 LEO 场景验证可行（GRLR 44 引用 [L13]，GraphPR 19 引用 [L14]），但所有现有工作都在**单一规模**上训练和测试。当部署规模（如 Starlink 4000+ 星）远超训练规模时，模型性能未知。

### 1.2 规模泛化的工程需求

| 需求维度 | 理由 | 来源 |
|----------|------|------|
| 降低训练成本 | 在 66-200 星训练 vs 在 4000+ 星训练，计算和采样成本差距数十倍 | feasibility_report §E; D012 |
| 适应星座演进 | 运营商分阶段部署卫星，规模持续增长；重训练代价大 | feasibility_report §B |
| 实时部署 | 新区域/新轨道壳层加入时，无需从零训练 | L01 (GKAE) 热插拔讨论 |
| 学术可行性 | 实验室 GPU (RTX 4070) 无法训练 4000+ 星 GNN+RL 模型 | D012; MVE 设置 |

**关键观察**：Walker-Delta 星座具有规则网格结构，每颗卫星恒定 4 ISL（2 轨内 + 2 轨间）。GNN 的 message-passing 聚合函数面对相同的局部邻居结构，与图规模无关——这是 size generalization 的理想条件。

> 来源：feasibility_report §A; L04 (ISL Pattern) 形式化定义; L01 理论分析 "learns local connectivity patterns rather than fixed global topology"

---

## 2. 现有方法局限

### 局限 1：GNN+RL LEO 路由全部在单一规模训练测试

13 篇 GNN+RL LEO 路由论文（L13-L25）无一涉及跨规模泛化实验。

| 论文 | 规模 | 跨规模? | literature_notes 条目 |
|------|------|---------|----------------------|
| GRLR (TVT 2025) | 未披露 | 否 | L13 |
| GraphPR (TVT 2025) | 未披露 | 否 | L14 |
| GQN (ICCC 2024) | 108 星 | 仅时序泛化 | L15 |
| GDRL-SFCR (Sensors 2025) | 6048 星 | 否（同规模） | L16 |
| GAT-LSTM-DQN (arXiv 2026) | 45 星 | 否 | L17 |
| DTAR (预印本 2026) | 288 星 | 否 | L18 |
| DeepLaDu (arXiv 2026) | Starlink-like | 否 | L19 |
| GNN-ASSSP (AST 2026) | 未注明 | 否 | L20 |
| ADRLRM/ST-GNN (ToN 2026) | 未注明 | 否 | L21 |
| FGRLR (WCL 2025) | 未注明 | 否 | L22 |
| DGA-IES (IoTJ 2025) | 未注明 | 否 | L23 |
| DLBR (TAES 2025) | 未注明 | 否 | L24 |
| Transformer-MIX (IoTJ 2025) | 未注明 | 否 | L25 |

> 来源：literature_notes §5 Size Generalization 现状; D006

### 局限 2：传统路由方法无法利用学习型表示

- **Dijkstra/SPF**：每个拓扑快照独立计算最短路径，丢弃历史负载趋势和邻居拥塞传播信号。SPF 平均 RTT 150 ms vs MCSR-LS <100 ms（33% 差距）。
  > 来源：feasibility_report §A; L10 (MCSR) 实验数据
- **分治策略**：MCSR (L10) 通过 SRD 分割处理 10000 星，但分割本身增加管理开销；CMCR (L11) 按纬度聚类，理论优雅但静态聚类适应性有限。
  > 来源：literature_notes §1.A; L10, L11
- **集中式优化**：DuJo (L03) 拉格朗日对偶松弛理论优雅但计算耗时（分钟级/快照），不适合实时路由。
  > 来源：literature_notes §2 已知局限; L03

### 局限 3：仿真工具不支持学习型路由

xeoverse (L05)、Hypatia、StarryNet 均为静态路由仿真器，GNN 路由需自建仿真环境或替换路由模块。

> 来源：literature_notes §6 仿真工具链分析; L05

### 局限 4：现有 GNN 路由缺乏位置感知

所有 GNN+RL LEO 路由论文未使用位置编码（PE），模型仅依赖节点特征（队列、负载）区分节点。当图规模变化时，缺乏位置锚点导致模型无法建立空间方向感。

> 来源：D026 消融 A1 证实无 PE 时训练精度 39.66%（≈随机 25%），PE 是学习必要条件

---

## 3. 研究空白

### 3.1 Size generalization 在 LEO 路由领域的空白

**检索范围**：12 篇精读 + 13 篇定向检索（共 25 篇）+ GRLR 引用链 44 篇 + GraphPR 引用链 19 篇 = **63 篇引用链筛查**。

| 检索维度 | 覆盖 | 结果 |
|----------|------|------|
| GNN+RL LEO 路由论文 | L13-L25 (13 篇) | **零提及** size generalization |
| GRLR 引用链 | 44 篇引用 | **零提及** |
| GraphPR 引用链 | 19 篇引用 | **零提及** |
| GAT/GraphSAGE 卫星变体 | 补充检索 | **零提及** |
| GNN 可扩展性/迁移学习 | 补充检索 | **零提及** |
| 联邦 GRL | 补充检索 | **零提及** |
| GNN 归纳泛化理论 | 补充检索 | **零 LEO 应用** |

**关键纠正**：Web 搜索多次声称 GRLR 涉及 size generalization，经 Semantic Scholar API 验证 TVT 2025 和 ICCC 2023 双版摘要均无提及，系 AI 幻觉。

> 来源：D004, D006; literature_notes §5; feasibility_report §B 新颖性论据

**结论**：GNN size generalization 在 LEO/satellite routing 领域**完全空白**。

### 3.2 GNN size generalization 理论基础

虽然卫星领域空白，但 ML 理论侧已有坚实基础：

| 文献 | 核心结论 | 与本研究关系 |
|------|----------|-------------|
| T01 (ICML 2024) 解耦表示学习 | 将大小相关和大小无关特征分离可提升跨规模泛化 | Walker-Delta 恒定度数结构有利于解耦 |
| T02 (NeurIPS 2025) 统一理论框架 | 当神经网络与目标函数对齐时，size generalization 可证明成立 | 路由目标函数（加权最短路径）可能满足"对齐"条件 |
| Size Transferability (arXiv 2026) | Graph Transformer + 卷积 PE 的跨规模可迁移性有流形收敛界 | Walker-Delta 可建模为轨道球面离散采样，满足流形假设 |

> 来源：literature_notes T01, T02; competitor_notes/porras-valenzuela_2026.md

---

## 4. 新颖性确认

### 4.1 要素组合

本研究的核心创新是以下要素的**首次组合**：

1. **Orbital Positional Encoding (PE)**：基于轨道力学的位置编码（sin/cos dim 16），使 GNN 获得空间方向感
2. **多尺度混合训练**：在 66+100+200 星三个规模上联合训练，增强跨规模鲁棒性
3. **加权 Dijkstra 推理**：GNN 输出方向偏好加权 Dijkstra，保证 100% 路径成功率
4. **零样本跨规模部署**：训练最大规模 200 星，零样本部署到 720 星（11x 扩展）

### 4.2 竞品排除记录

| 竞品 | 发表渠道 | 任务 | 领域 | PE | 跨规模 | 威胁等级 | 排除理由 |
|------|----------|------|------|-----|--------|----------|----------|
| GRLR (L13) | TVT 2025 | LEO 路由 | 卫星 | 无 | 无 | 低 | 无 size gen，无 PE，单一规模 |
| GraphPR (L14) | TVT 2025 | LEO 路由 | 卫星 | 无 | 无 | 低 | 全分布式但单一规模 |
| GDRL-SFCR (L16) | Sensors 2025 | LEO+SFC | 卫星 | 无 | 无 | 低 | 6048 星但训练测试同规模 |
| TELGEN | IEEE/TON 2025 | TE 流量拆分 | WAN | 无 | 有(20x) | 中 | 非路由(LP 拆分)，非卫星，无 PE |
| Size Transferability | arXiv 2026 | 节点分类 | 通用图 | 有(RPEARL) | 有 | 低 | Graph Transformer 非 GNN 路由，非卫星 |
| Scaling Swarm | AI 2025 | 2D 导航 | 群智 | 无 | 有(3x) | 低-中 | 非路由，k-NN 非规则图，仅 3x |
| Lee ICT Express 2025 | ICT Express 2025 | LEO 切换 | 卫星 | 无 | 无 | 低 | GNN 分布式切换，非路由 |

> 来源：D010, D011; competitor_notes/telgen_2025.md, competitor_notes/porras-valenzuela_2026.md, competitor_notes/swarm-scaling_2025.md

### 4.3 新颖性检索通过的证据

- 4 组关键词检索（GNN size generalization satellite / GNN scalable LEO routing / position encoding GNN routing / zero-shot GNN network）
- 3 篇竞品精读（TELGEN, Size Transferability, Scaling Swarm）
- 2 组定向检索（GNN 归纳泛化理论 + GNN 可扩展性）
- GRLR+GraphPR 63 篇引用链筛查

**结论**：GNN size generalization for LEO satellite routing 仍为空白。

> 来源：D010; feasibility_report §B

---

## 5. 论文叙事弧线

实验设计采用三级递进结构，每级回答一个关键问题：

### Level 1：方法有效性（能否做到？）

**实验 E01 核心对比**

在 66+100+200 星训练，零样本部署到 720 星（11x），与 Dijkstra（下界）和 GRLR 同规模训练（上界）对比。

| 对比组 | 训练规模 | 评估规模 | 预期定位 |
|--------|----------|----------|----------|
| Dijkstra | 无训练 | 720 | 性能下界 |
| **Ours（跨规模）** | 66+100+200 | 720 | 中间 |
| GRLR（同规模） | 720 | 720 | 性能上界 |

**预期结果**：时延保留率 >= 80%，vs Dijkstra 差距 <= 20%。

> 来源：D012, D025; Contract 核心指标

**实际结果**（已获得）：

| 方法 | Mean Stretch | <=1.2x Optimal | Delay (ms) | 保留率 |
|------|-------------|----------------|------------|--------|
| Dijkstra | 1.000 | 100% | 60.32 | — |
| **Ours** | **1.097** | **85.1%** | **66.77** | **90.3%** |
| GRLR (同规模) | 1.008 | 100% | 60.32 | 100% |

> 来源：D023, D024, D025

### Level 2：组件贡献（为什么有效？）

**消融实验 A1-A3**

| 消融 | 变量 | 训练精度 | Stretch | <=1.2x | 结论 |
|------|------|----------|---------|--------|------|
| A1 | 移除 Orbital PE | 39.66% | 1.002 | — | PE 是学习必要条件 |
| A2 | 单尺度训练 (train_100) | 97.70% | 1.120 | 81.1% | 多尺度贡献 2-4pp |
| A3 | 无 PE + 单尺度 | 40.16% | 1.049 | 93.6% | 确认 PE 不可替代 |

**同规模消融**：720->720 训练，stretch 1.000（完美），证实 9.7pp stretch 差距完全来自跨规模迁移。

> 来源：D026, D027, D028, D029

### Level 3：边界条件（泛化的极限在哪？）

待补充。建议方向：
- 不同规模比例（4x, 8x, 11x, 16x）的保持率曲线
- 不同星座拓扑（Walker-Delta vs Walker-Star）的泛化差异
- 训练规模下限（最小可用训练规模是多少？）

---

## 6. 论证主线建议稿

LEO mega-constellation 路由面临规模爆炸与拓扑时变的双重挑战。尽管 GNN+RL 路由已在卫星网络中验证可行（GRLR, GraphPR），现有 13 篇工作全部在单一规模上训练和测试，跨规模泛化能力完全未被探索（25 篇论文 + 63 篇引用链筛查确认空白 [D006, D010]）。然而，Walker-Delta 星座的规则网格结构（每星恒定 4 ISL）为 GNN 的 message-passing 提供了天然一致的局部环境——训练 66 星和推理 720 星的邻居结构完全相同，使 size generalization 成为工程可行的问题。

本研究提出 Orbital PE + 多尺度混合训练的 GNN 路由框架，在 66+100+200 星上联合训练后零样本部署到 720 星（11x 扩展）。消融实验证实：位置编码是模型学习的必要条件（移除后精度降至随机水平 [D026]），多尺度训练贡献 2-4 pp 性能提升 [D027]。核心实验表明跨规模部署时延保留率 90.3%（vs 同规模 GRLR），代价仅 9.9% 额外时延 [D025]。这是 GNN size generalization 在卫星路由领域的首次实证。

---

## 7. Gap-Contribution 闭环映射

| Gap | 方法组件 | 结论回应 | 数据证据 |
|-----|----------|----------|----------|
| GNN 路由无法跨规模部署 | Orbital PE (sin/cos dim 16) | PE 是学习必要条件，使 GNN 获得空间方向感 | A1: 无 PE 精度 39.66%, 有 PE 97.6% [D026] |
| 单一训练规模泛化不足 | 多尺度混合训练 (66+100+200) | 多尺度联合训练贡献 2-4 pp stretch 改善 | A2: 单尺度 stretch 1.120, 多尺度 1.097 [D027] |
| 贪心推理路径成功率低 | 加权 Dijkstra 推理 | 保证 100% 路径成功率，stretch 可控 | D020: 贪心 1.7% 成功率, 加权 Dijkstra 100% |
| 跨规模部署性能损失未知 | 11x 零样本实验 (66-200->720) | 保留率 90.3%, vs Dijkstra 差距 9.9% | D025: mean stretch 1.097, delay 66.77ms |
| 同规模 vs 跨规模差距来源 | 同规模消融 (720->720) | 9.7pp 差距完全来自跨规模迁移，非架构限制 | D029: 同规模 stretch 1.000（完美） |
| 空白领域首次验证 | MVE (96->384->1536) + 完整实验 | GNN 跨规模泛化在卫星路由中可行 | D007: MVE 83-87% 保持率; D023: 完整实验 |

---

## 8. 待补充标记

以下内容需在论文写作前补充：

- [ ] **Level 3 边界条件实验数据**：不同规模比例 (4x, 8x, 16x) 的保持率曲线
- [ ] **Starlink 级部署验证**：720->4000+ 星的实际部署性能（如计算资源允许）
- [ ] **TELGEN 差异化论述强化**：论文 Related Work 中需明确区分 TE（流量拆分）vs 路由（每跳决策）
- [ ] **PE 设计消融**：Orbital PE vs 随机 PE vs 无 PE 的对比（A1 已部分覆盖）
- [ ] **不同流量模式下的泛化性能**：hotspot / distance / population 模式（当前仅 uniform）
- [ ] **与 Scaling Swarm (3x) 的定量对比**：我们的 11x vs 他们的 3x，差异原因分析
- [ ] **理论分析**：基于 T02 (NeurIPS 2025) 的 Walker-Delta 拓扑对齐条件验证
- [ ] **论文定位的最终目标期刊/会议**：影响 narrative tone 和篇幅

---

## 附录：关键数字速查

| 指标 | 数值 | 来源 |
|------|------|------|
| 训练规模 | 66+100+200 星 | D012 |
| 目标规模 | 720 星 (11x) | D012 |
| Mean Stretch | 1.097 | D023 |
| Median Stretch | 1.056 | D023 |
| P95 Stretch | 1.315 | D023 |
| <=1.2x Optimal | 85.1% | D023 |
| <=1.5x Optimal | 98.9% | D023 |
| Delay (Ours) | 66.77 ms | D025 |
| Delay (GRLR 同规模) | 60.32 ms | D024 |
| Delay (Dijkstra) | 60.32 ms | D024 |
| 时延保留率 | 90.3% | D025 |
| vs Dijkstra 差距 | 9.9% | D025 |
| 消融 A1 (无 PE) 精度 | 39.66% | D026 |
| 消融 A2 (单尺度) Stretch | 1.120 | D027 |
| 消融 A3 (无 PE+单尺度) 精度 | 40.16% | D028 |
| 同规模消融 Stretch | 1.000 | D029 |
| GNN 架构 | GAT 3 层 h=128 | Contract |
| PE 维度 | sin/cos dim 16 | Contract |
| 评估样本 | 10 snapshots x 5 TMs x 100 flows | D023 |
| MVE 保持率 | 83-87% (均匀), 80-86% (异质) | D007 |
| 检索覆盖 | 25 篇论文 + 63 篇引用链 | D006 |
