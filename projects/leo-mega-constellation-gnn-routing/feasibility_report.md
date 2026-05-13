# 方向可行性报告

## 研究方向
GNN size generalization for LEO mega-constellation routing — 在小星座上训练 GNN 路由模型，零样本泛化到大星座（如 Starlink 级）。

## A. 结构优势论证

### 核心方法 vs 最简 baseline

**最简 baseline**：Dijkstra/OSPF 最短路径路由。每个拓扑快照独立计算最短路径，O(N²) 复杂度，无学习、无泛化。

**结构性优势**：GNN 的 message-passing 机制天然编码局部连通模式而非全局拓扑。训练时学习的权重是邻居聚合函数，与图规模无关。具体条件：

1. **ISL 质量异质性**：卫星网络中 ISL 时延/容量因轨道位置、距离、负载而异（L03 DuJo 的 Shannon 模型、L05 xeoverse 的天气衰减模型）。Dijkstra 仅用静态权重，无法捕获动态负载变化。GNN 通过注意力机制（GAT）可学习区分 ISL 质量差异（L14 GraphPR 的 GAT 编码已验证有效）。

2. **拓扑规则性 + 规模变化**：Walker-Delta 星座具有规则网格结构（L04 ISL Pattern 形式化定义），每个卫星度数恒定（通常 4 ISL）。这意味着 GNN 的聚合函数在训练和推理时面对相同局部结构——这是 size generalization 的理想条件。Dijkstra 没有这个问题因为它重新计算，但计算成本随规模 O(N²) 增长；GNN 推理 O(1) per node，与规模无关。

3. **信息损失量化**：Dijkstra 在每个快照独立计算，丢弃了：(a) 历史负载趋势信息（L10 MCSR 需要周期性更新路由表），(b) 邻居拥塞传播信号。GNN+RL 的 Actor-Critic 框架（L13 GRLR 已验证）可利用时序信息做预防性路由。

**关键证据**：
- L01 (GKAE) 理论分析：GNN "learns local connectivity patterns rather than fixed global topology"，置换不变性天然适配卫星网络
- L06 (GPN) 实证：30→50 节点零样本泛化（67% 扩展），证明 GNN 跨规模泛化在路由任务上可行
- L14 (GraphPR) 实证：GAT 编码一跳邻居信息可隐式捕获多跳状态，全分布式架构有效
- L10 (MCSR) 规模分析：传统方法通过 SRD 分割处理 10000 星，但分割本身增加管理开销；GNN 模型泛化可避免分治策略的局限

### 在什么条件下简单方法会导致信息损失？

当 ISL 负载在时空上非均匀分布时（L10 MCSR 证明了 LEO 流量的 hotspot 模式、L02 Starfield 的 4 种流量模式），Dijkstra 无法利用全局负载分布信息做负载均衡路由。信息损失 = 最短路径 vs 全局最优路径的时延差距。L10 实验数据显示：SPF 平均 RTT 150ms vs MCSR-LS <100ms（33% 差距）。

## B. 新颖性-可行性解耦

### 新颖性论据（事实判断，已确认）

经 12 篇精读 + 6 篇定向检索（共 18 篇），Semantic Scholar API 验证：

- **GNN size generalization in LEO/satellite routing**：**完全空白**
  - 6 篇 GNN+RL LEO 路由论文（L13-L18）无一涉及跨规模泛化
  - L16 (GDRL-SFCR) 在 6048 星训练测试（最大规模但同规模）
  - L13 (GRLR, 44 引用) 经双版摘要验证无提及
  - Web 搜索声称 GRLR 涉及 size generalization 系 AI 幻觉（已通过 Semantic Scholar API 纠正）
- GNN size generalization 在其他领域有理论基础：ICML 2024 解耦表示学习、KDD 2023 谱方法

### 可行性论据（预测）

1. **Walker-Delta 拓扑的规则性有利于泛化**：每颗卫星恒定 4 ISL（2 轨内 + 2 轨间），GNN 聚合函数面对相同局部结构。训练 100 星和推理 4000 星的邻居结构一致——这是 size generalization 的理想条件。
2. **已有跨领域实证**：L06 (GPN) 在 Erdos-Renyi 图上 30→50 节点泛化成功。卫星网格比随机图更规则，泛化应该更容易而非更难。
3. **L01 (GKAE) 已在 1442 星上验证 GNN 有效**，虽然未做跨规模测试，但证明 GNN 可以处理 1000+ 规模的卫星拓扑。
4. **RL 训练框架已有成熟参考**：L13 GRLR 的 Actor-Critic + L14 GraphPR 的 MADRL 均已验证可行，可直接复用训练范式。

### 空白原因分析

**技术限制刚解除**（论据最强）：
- GNN+RL for LEO routing 本身在 2024-2025 才刚被验证（GRLR 2025 ICCC → TVT, GraphPR 2025），研究者还在解决"能不能做"的问题
- Size generalization 是更高级的研究问题，需要先验证基础可行性
- 计算：训练 6000+ 星的 GNN+RL 模型计算成本极高，size generalization 提供了降低训练成本的工程动机
- **时间窗口**：2025-2026 是最佳切入期，基础方法已验证但高级问题尚未探索

## Step 4a 决策建议

**决策：Go**

理由：
- 维度 A：结构性优势明确（GNN 局部聚合 vs Dijkstra 全局重计算 + 负载信息利用）
- 维度 B：新颖性确凿（18 篇论文零覆盖），可行性有强论据（拓扑规则性 + 跨领域实证 + 技术限制刚解除）
- 无致命信号

## Go/No-Go 决策
- 决策：Go（待用户确认）
- 理由：Size generalization 在 LEO GNN 路由中完全空白，拓扑规则性提供有利条件，技术窗口期 2025-2026
- 用户确认：[留空]
