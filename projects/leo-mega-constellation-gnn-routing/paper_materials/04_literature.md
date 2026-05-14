# 文献定位

> 方向：GNN size generalization for LEO mega-constellation routing
> 文献基座：12 篇精读 + 13 篇摘要验证 + 2 篇理论背景 + 3 篇竞品深度分析 + 30 篇背景引用 = 共 60 篇
> 核心结论：GNN size generalization 在 LEO/satellite routing 领域完全空白

---

## 1. 核心论文完整条目

### 1.1 精读论文（L01-L12）

#### [L01] GKAE — Toward Scalable SDN for LEO Mega-Constellations: A Graph Learning Approach
- **作者**: 未提取
- **年份/来源**: 2026 / arXiv:2604.27478（预印本，投 IEEE 期刊中）
- **DOI**: —
- **方法**: Graph Koopman Autoencoder (GKAE)，GNN 空间压缩 + Koopman 理论线性化非线性动态，分层 SDN 框架按轨道壳层分解
- **实验**: Starlink Shell 1（1442 星，550 km，53° 倾角），20 分钟预测窗口
- **关键结论**: GNN 压缩比 CNN/DNN 提升 43-47.4%；GKAE 时间预测比 LSTM 好 10.81%；模型体积比 CNN 小 2.7x
- **与本研究关系**: 直接相关 — GNN 置换不变性从 400 星训练推广到 1444 星推理，非路由算法但是 GNN 路由基础设施
- **精读状态**: 精读

#### [L02] Starfield — Demand-Aware Satellite Topology Design for LEO Mega-Constellations
- **作者**: 未提取
- **年份/来源**: 2026 / arXiv:2601.10083（预印本）
- **DOI**: —
- **方法**: 黎曼度量引导 ISL 拓扑设计，流量需求向量场，测地线对齐
- **实验**: Starlink Phase 1（1584 星，72 面 x 22 颗，550 km），4 种流量模式
- **关键结论**: stretch factor 降低 15-20%，跳数减少 30%；密度 400 星后边际收益递减
- **与本研究关系**: 方法可借鉴 — ISL 拓扑设计是 GNN 路由输入；+Grid 是通用 baseline 拓扑
- **开源**: https://github.com/shayunak/Starfield
- **精读状态**: 精读

#### [L03] DuJo — Joint Laser ISL Matching and Traffic Flow Routing via Lagrangian Duality
- **作者**: 未提取
- **年份/来源**: 2025/2026 / arXiv:2601.21914（预印本）
- **DOI**: —
- **方法**: 拉格朗日对偶松弛将 NP-hard MILP 解耦为加权图匹配 + 最短路径 + LP 速率分配
- **实验**: Starlink TLE 数据（1000 星默认），额外 Walker-delta/OneWeb
- **关键结论**: 联合优化吞吐提升最高 145%；提出 "learning to predict Lagrange multipliers" 未来方向
- **与本研究关系**: 方法可借鉴 — 拉格朗日乘子可融入 GNN 边特征；真实 Starlink 仿真框架可复用
- **精读状态**: 精读

#### [L04] ISL Spanning Patterns — Investigating ISL Spanning Patterns on Networking Performance
- **作者**: 未提取
- **年份/来源**: 2023 / IEEE 期刊（arXiv:2312.15873）
- **DOI**: —
- **方法**: Walker 星座 ISL spanning pattern 形式化定义（相位偏差集合 B），穷举 +Grid/*Grid 共 10 种模式
- **实验**: Walker 星座（10²-40² 星），53° 倾角
- **关键结论**: +Grid 最优 bm1 时延 <50ms；*Grid 最优 b0m1 容量比 +Grid 高 37%
- **与本研究关系**: 方法可借鉴 — ISL 拓扑形式化方法直接用于仿真环境拓扑建模
- **精读状态**: 精读

#### [L05] xeoverse — A Real-time Simulation Platform for Large LEO Mega-Constellations
- **作者**: 未提取
- **年份/来源**: 2024 / arXiv:2406.11366（预印本）
- **DOI**: —
- **方法**: 基于 Mininet 的实时仿真，预计算拓扑 + 增量链路更新，Dijkstra 路由
- **实验**: Starlink Shell 1（1584 星）和全星座（5442 星）
- **关键结论**: 单机实时仿真可行；比 Hypatia 快 2.3x，比 StarryNet 快 40x
- **与本研究关系**: 方法可借鉴 — 星座拓扑建模/链路建模框架可复用；所有仿真平台不支持学习型路由
- **精读状态**: 精读

#### [L06] GPN — GNN-Based Multicast Routing for On-Demand Streaming in 6G Networks
- **作者**: 未提取
- **年份/来源**: 2025 / IEEE TMC（DOI: 10.1109/TMC.2025.3634587，arXiv:2510.11109）
- **DOI**: 10.1109/TMC.2025.3634587
- **方法**: GAT 编码器 + LSTM 路径历史聚合器 + 注意力解码器，REINFORCE 训练，序列化 MDP
- **实验**: 合成 Erdos-Renyi 图，30-50 节点
- **关键结论**: 接近 DP 理论最优；30→50 节点零样本泛化；GAT 编码器贡献最大
- **与本研究关系**: 直接相关 — GAT+LSTM+Policy Gradient 路由架构可迁移到 LEO ISL 路由；拓扑泛化能力有参考
- **开源**: https://github.com/UNIC-Lab/GNN-Routing
- **精读状态**: 精读

#### [L07] Structural Generalization — GNN for Microservice Routing
- **作者**: 未提取
- **年份/来源**: 2025 / arXiv:2510.15210（预印本）
- **DOI**: —
- **方法**: 边特征感知注意力 GNN + softmax 路由选择，多层 message-passing
- **实验**: DeathStarBench Social Network，10+ 微服务，GNN 4 层最优
- **关键结论**: MRE 0.072，路由决策准确率 91.4%；4 层 GNN 最优（过深过平滑）
- **与本研究关系**: 方法可借鉴 — 边感知注意力对卫星链路质量波动建模有参考价值
- **精读状态**: 精读

#### [L08] GNN-Based Routing for Link Reliability in SD-LEO
- **作者**: 未提取
- **年份/来源**: 2024 / IEEE NFV-SDN 2024
- **DOI**: 10.1109/NFV-SDN61811.2024.10807492
- **方法**: 基础 GCN 做 ISL 性能指标聚合（mean pooling），SDN 控制器做路由决策
- **实验**: Iridium 66 星，NS-3.37.1，300 秒仿真
- **关键结论**: 平均时延 99.6-100.5 ms；无 baseline 对比
- **与本研究关系**: 已知唯一 GNN+LEO 路由论文，但仅聚合非决策，小规模窄带，质量有限
- **精读状态**: 精读

#### [L09] GARS — Geographic-Based Auxiliary Routing in SDN Mega Constellations
- **作者**: 未提取
- **年份/来源**: 2026 / IEEE IoT Journal
- **DOI**: 10.1109/JIOT.2025.3638842
- **方法**: Walker-Delta 坐标模型 + 基于相对几何位置的 GRA + 三级优先级防环机制
- **实验**: Walker-Delta（70°，1000 km），600-2000 星，STK + OMNeT++
- **关键结论**: 恢复时间缩短 65.5%，丢包率降低 67.2%，O(1) 复杂度
- **与本研究关系**: 方法可借鉴 — O(1) 快速路由 baseline 参考；防环机制设计思路
- **精读状态**: 精读

#### [L10] MCSR — Multi-Attribute Consistency Segment Resilient Routing
- **作者**: 未提取
- **年份/来源**: 2025 / IEEE TMC
- **DOI**: 10.1109/TMC.2025.3570670
- **方法**: 不相交段路由域（SRD）分割，多属性一致性主导路径筛选（{D, A, J}），域间 SRD-BCM 协作
- **实验**: 5 种星座（1156-10000 星），Hypatia + NS-3，全球 100 城市 CBR 流量
- **关键结论**: MCSR-LS RTT <100ms，吞吐量比 AODV/CMCR 提高 19%，10000 星收敛时间比 SPF 降低 63%
- **与本研究关系**: 重要 Baseline 对比对象 — LEO mega-constellation 路由中最强传统方法之一
- **精读状态**: 精读

#### [L11] CMCR — Clustered Multi-Criteria Routing for Mega LEO Constellations
- **作者**: 未提取
- **年份/来源**: 2024 / IEEE TVT（22 次引用）
- **DOI**: 10.1109/tvt.2024.3396350
- **方法**: 按飞行方向+LoS+纬度分簇，属性一致性理论（Theorem 1-4 证明收敛），多模态服务
- **实验**: Starlink Phase I（1584 星，72x22，550 km），ISL 100 Mbps
- **关键结论**: MCPTT 时延低于 TPLB/IUDR；MCD PDR 100%；理论证明无环且收敛到最优
- **与本研究关系**: 重要 Baseline 对比对象 — 有理论保证的传统路由算法
- **精读状态**: 精读

#### [L12] Scalable Multicontroller SDN via Topology Virtualization
- **作者**: 未提取
- **年份/来源**: 2025 / IEEE IoT Journal
- **DOI**: 10.1109/JIOT.2025.3576912
- **方法**: 拓扑虚拟化屏蔽控制平面变化，虚拟-物理映射分解（平面+集群映射），O(N_V·N_H) 闭式解
- **实验**: Starlink Gen II（2520 星），H3 六边形网格 4794 单元，SDN 控制器 1-250 个
- **关键结论**: 映射距离为最优的 119% 但计算 <0.1s（最优需 15.99 小时）
- **与本研究关系**: 方法可借鉴 — SDN 控制器架构可作 GNN 路由部署框架
- **精读状态**: 精读

### 1.2 补充检索论文（L13-L25，摘要验证）

#### [L13] GRLR — Routing With GNN and RL for Mega LEO Satellite Constellations
- **年份/来源**: 2025 / IEEE TVT（44 次引用，GNN+LEO 路由引用最高）
- **DOI**: 10.1109/TVT.2024.3471658
- **方法**: GNN 特征提取 + Actor-Critic RL，MDP 建模，分布式路由，最小化时延
- **实验**: Walker-Delta mega-LEO 星座
- **与本研究关系**: **直接竞争者** — 但未涉及 size generalization（Semantic Scholar API 双版验证）
- **精读状态**: 浅读（摘要 + Semantic Scholar 验证）

#### [L14] GraphPR — Fully-Distributed Dynamic Packet Routing for LEO Satellite Networks
- **年份/来源**: 2025 / IEEE TVT（19 次引用）
- **DOI**: 10.1109/TVT.2024.3499933
- **方法**: GAT + MADRL，POMDP，一跳邻居通信，RSPH 防环机制
- **与本研究关系**: 直接竞争者 — 未涉及 size generalization
- **精读状态**: 浅读

#### [L15] GQN — Inter-Satellite Routing for LEO: GNN and DRL Integrated Approach
- **年份/来源**: 2024 / IEEE/CIC ICCC（12 次引用）
- **DOI**: 10.1109/ICCC62479.2024.10681995
- **方法**: GNN 学习卫星节点关系 + DRL 自适应路由决策
- **实验**: 108 颗卫星
- **与本研究关系**: 直接竞争者 — 仅时序泛化，未涉及跨规模泛化
- **精读状态**: 浅读

#### [L16] GDRL-SFCR — Deep RL Routing with Service Function Constraints
- **年份/来源**: 2025 / MDPI Sensors
- **DOI**: 10.3390/s25041232
- **方法**: GCN + PPO，SFC 约束奖励函数
- **实验**: 6048 颗卫星（GNN+LEO 路由领域报告最大规模）
- **与本研究关系**: 直接竞争者 — 单一规模训练测试，未涉及 size generalization
- **精读状态**: 浅读

#### [L17] GAT-LSTM-DQN — Spatial-Temporal Routing with Proactive Congestion Avoidance
- **年份/来源**: 2026 / arXiv:2605.02413（预印本）
- **方法**: GAT+LSTM+DQN 时空路由
- **实验**: 45 颗卫星（规模极小）
- **与本研究关系**: 间接竞争者 — 未涉及 size generalization
- **精读状态**: 浅读

#### [L18] DTAR — Traffic-Aware Domain Partitioning and Load-Balanced Routing
- **年份/来源**: 2026 / 预印本
- **方法**: NSGA-II 离线域划分 + GAT + Action-masked PPO 在线路由
- **实验**: 288 颗卫星 Walker 星座
- **与本研究关系**: 直接竞争者 — 域划分思想可结合规模泛化，未涉及 size generalization
- **精读状态**: 浅读

#### [L19] DeepLaDu — Duality-Guided Graph Learning for Joint Connectivity and Routing
- **年份/来源**: 2026 / arXiv:2601.21921（预印本）
- **方法**: Lagrangian 对偶变量解释为拥塞价格，GNN 单次前向推理输出拥塞价格
- **实验**: Starlink-like 星座
- **与本研究关系**: 未涉及 size generalization — 聚焦联合优化
- **精读状态**: 浅读

#### [L20] GNN-ASSSP — Attention Mechanism Driven Dynamic Routing
- **年份/来源**: 2026 / Aerospace Science and Technology, Vol. 178
- **方法**: 注意力机制 + GNN 动态路由
- **与本研究关系**: 未涉及 size generalization
- **精读状态**: 浅读

#### [L21] ADRLRM — Age-Oriented Distributed Routing via ST-GNN
- **年份/来源**: 2026 / IEEE ToN
- **DOI**: 10.1109/TON.2025.3597928
- **方法**: ST-GNN + DRL 最小化 AoI，时空图编码
- **与本研究关系**: 未涉及 size generalization — 聚焦 AoI
- **精读状态**: 浅读

#### [L22] FGRLR — Federated Graph RL Routing
- **年份/来源**: 2025 / IEEE WCL
- **DOI**: 10.1109/LWC.2025.3593508
- **方法**: 联邦学习 + GNN + RL 路由
- **与本研究关系**: 未涉及 size generalization — 聚焦联邦训练范式
- **精读状态**: 浅读

#### [L23] DGA-IES — Deep Graph Attention + Incremental Evolutionary RL
- **年份/来源**: 2025 / IEEE IoTJ（5 次引用）
- **方法**: 深度图注意力 + 增量进化策略替代 PPO
- **关键结论**: E2E 时延降低 10.3%-58.1%
- **与本研究关系**: 未涉及 size generalization — 聚焦进化策略加速收敛
- **精读状态**: 浅读

#### [L24] DLBR — Dynamic Load-Balancing Routing via GCN+LSTM Traffic Prediction
- **年份/来源**: 2025 / IEEE TAES（12 次引用）
- **方法**: GCN+LSTM+Attention 时空流量预测 + 多 agent Dueling DQN 负载均衡路由
- **与本研究关系**: 未涉及 size generalization — 聚焦流量预测驱动负载均衡
- **精读状态**: 浅读

#### [L25] Transformer-MIX — Distributed Routing via Multiagent Transformer
- **年份/来源**: 2025 / IEEE IoTJ（8 次引用）
- **方法**: Multiagent Transformer-MIX 架构，统一负载均衡奖励
- **与本研究关系**: 未涉及 size generalization — 聚焦 Transformer 多 agent 协作
- **精读状态**: 浅读

### 1.3 理论背景（T01-T02）

#### [T01] Enhancing Size Generalization in GNNs through Disentangled Representation Learning
- **年份/来源**: ICML 2024（Poster #35203）
- **核心贡献**: 解耦表示学习将大小相关和大小无关特征分离，提升跨规模泛化
- **与本研究关系**: 核心理论基础 — 证明 GNN size generalization 问题存在且有解法；卫星拓扑规则结构有利于解耦
- **精读状态**: 精读（理论引用）

#### [T02] Towards a Theory for Size Generalization
- **年份/来源**: NeurIPS 2025（Poster #118775）
- **核心贡献**: 统一框架分析 ML 模型处理可变大小输入的泛化能力；当神经网络与目标函数对齐时 size generalization 可证明成立
- **与本研究关系**: 核心理论基础 — Walker-Delta 恒定度数结构可能满足"对齐"条件
- **精读状态**: 精读（理论引用）

### 1.4 竞品深度分析

#### [C01] TELGEN — Traffic Engineering in Large-Scale Networks With Generalizable GNNs
- **年份/来源**: 2025 / IEEE/ACM ToN（arXiv:2503.24203）
- **DOI**: 10.1109/TON.2026.3659135
- **方法**: 定制消息传递 GNN 模仿 Interior Point Method，LP 公式图（4 类顶点，6 类消息方向），监督学习
- **实验**: Erdos-Renyi/Waxman/ASN，训练 20-800 节点，测试 200-5000 节点（最高 20x）
- **关键结论**: OnoCGap < 3%（20x 规模下）；IPM 模仿继承算法的问题实例无关性
- **与本研究关系**: 竞品（威胁等级：中）— WAN TE 非 LEO 路由，LP 流量拆分非路由决策，无 PE，无动态拓扑，监督非 DRL
- **精读状态**: 精读（competitor_notes）

#### [C02] Size Transferability — Graph Transformers with Convolutional PE
- **年份/来源**: 2026 / arXiv（arXiv:2602.15239，预印本）
- **作者**: Porras-Valenzuela, Wang, Ribeiro (UPenn)
- **方法**: RPEARL 卷积 PE（随机高斯特征 + TAGConv + 经验平均恢复置换等变性），Graph Transformer
- **理论**: Theorem 1 GT 点态收敛到 MT，Corollary 2-4 收敛界和 k-hop 稀疏扩展
- **实验**: 节点分类（SNAP-Patents 1.7M 节点），10.5% 训练达 ~90% 准确率
- **与本研究关系**: 技术借鉴价值高（威胁等级：低）— GT 非 GNN 消息传递，节点分类非路由；RPEARL PE 可集成；Walker-Delta 可建模为球面流形采样
- **精读状态**: 精读（competitor_notes）

#### [C03] Scaling Swarm — Zero-shot GNN Policy Transfer across Swarm Sizes
- **年份/来源**: 2025 / AI journal, Vol. 6, Issue 11（DOI: 10.3390/ai6110282，2 次引用）
- **方法**: 1 层 GAT + Deep Q-Learning + epsilon-greedy，CTDE 范式，动态 k-NN 通信图
- **实验**: N=10 训练，零样本部署到 N=15-29（最高 3x），超过 ~2x 退化加速
- **与本研究关系**: 非直接竞争者（威胁等级：低-中）— 简单 swarm 2D 导航 vs LEO 路由，非结构化 k-NN vs 规则网格，3x vs 16x+
- **精读状态**: 精读（competitor_notes）

---

## 2. 技术路线分类体系

### 路线 A: GNN+RL LEO 路由（2024-2026 新兴活跃方向）
- **论文**: L13(GRLR), L14(GraphPR), L15(GQN), L16(GDRL-SFCR), L17(GAT-LSTM-DQN), L18(DTAR)
- **特征**: GAT/GCN 编码卫星拓扑，Actor-Critic/PPO/DQN 训练路由策略，MDP/POMDP 建模，分布式决策
- **局限**: **全部在单一规模训练测试**，无一涉及 size generalization
- **趋势**: 2024 验证可行性 → 2025 成为主流范式（GRLR 44 引用）→ 2026 混合架构

### 路线 B: 传统 LEO 路由优化
- **论文**: L09(GARS), L10(MCSR), L11(CMCR), L03(DuJo)
- **特征**: 分段/聚类/分治策略处理大规模，几何辅助路由，拉格朗日对偶松弛
- **优势**: 有理论收敛保证，可扩展到 10000 星
- **局限**: 非学习型，无法适应动态负载

### 路线 C: GNN 网络表示与预测
- **论文**: L01(GKAE), L08(GNN-SD-LEO)
- **特征**: GNN 做拓扑压缩/状态预测/指标聚合，路由决策仍依赖传统方法
- **意义**: 证明 GNN 置换不变性适合卫星网络（L01: 400→1444 星推理）

### 路线 D: GNN 路由（非 LEO 领域）
- **论文**: L06(GPN), L07(微服务路由)
- **特征**: GAT+RL 端到端路由，边感知注意力机制
- **意义**: L06 证明 GNN 路由拓扑泛化可行性（30→50 节点）；L07 证明边感知注意力对链路质量建模有效

### 路线 E: Size Generalization 理论
- **论文**: T01(ICML'24 解耦表示), T02(NeurIPS'25 统一理论), C02(Size Transferability GT+PE)
- **特征**: 解耦大小相关/无关特征；对齐条件下 size generalization 可证明；卷积 PE 流形收敛
- **核心支撑**: 卫星拓扑规则结构（恒定度数、Walker-Delta 球面采样）有利于 size generalization

### 路线 F: 网络规模泛化（非卫星）
- **论文**: C01(TELGEN), C03(Scaling Swarm)
- **特征**: GNN 在 WAN TE/Swarm 导航中的跨规模泛化
- **局限**: TELGEN 为 TE 非路由、监督非 RL、静态非动态；Swarm 仅 3x 简单场景

### 路线 G: 仿真基础设施
- **论文**: L02(Starfield), L04(ISL Pattern), L05(xeoverse), L12(SDN)
- **特征**: 星座拓扑建模、ISL 拓扑设计、实时仿真平台、SDN 控制框架
- **关键发现**: 所有平台不支持学习型路由，GNN 路由需自建仿真

---

## 3. 竞品精确区分表

| 竞品 | 覆盖要素 | 缺失要素 | 威胁等级 | 差异化要点 |
|------|---------|---------|---------|-----------|
| **TELGEN** (C01) | GNN size generalization (20x), 大规模网络 | LEO 卫星, 路由(TE非路由), PE, 动态拓扑, DRL | 中 | LEO 特有挑战 + 路由 vs TE + 位置感知 GNN + 动态拓扑 |
| **Size Transferability** (C02) | PE 理论(RPEARL), size generalization 理论界 | GNN 消息传递(用 GT), 路由, LEO, DRL | 低 | GT vs GNN 架构差异，节点分类 vs 路由，可借鉴 PE 理论 |
| **Scaling Swarm** (C03) | 零样本 GNN 跨规模迁移 | LEO, 路由(2D 导航), PE, 大规模(仅 3x), 结构化图 | 低-中 | 简单场景 vs LEO 路由复杂度，k-NN vs 规则网格 |
| **GRLR** (L13) | GNN+RL LEO 路由, 44 引用 | Size generalization, PE, 多尺度训练 | 中-高 | 最强直接竞争者但无跨规模能力；如后续工作加 size gen 则窗口关闭 |
| **GraphPR** (L14) | GAT+MADRL LEO 路由, 全分布式, RSPH 防环 | Size generalization, PE | 中 | 全分布式架构精巧但无跨规模 |
| **GDRL-SFCR** (L16) | GNN+LEO 最大规模(6048 星), NTN 建模 | Size generalization, PE, 多尺度训练 | 中 | 规模最大但训练测试同规模 |
| **DTAR** (L18) | GAT+PPO, 域划分思想 | Size generalization, 跨规模实验 | 低-中 | 域划分可结合规模泛化但论文未探索 |
| **MCSR** (L10) | 10000 星规模, 分段弹性路由 | ML/GNN, 学习型方法 | 低 | 传统方法天花板，GNN 路由需超越此基线 |

### 核心创新要素覆盖分析

| 要素 | 本研究 | GRLR | GraphPR | TELGEN | Size Trans. | Scaling Swarm |
|------|--------|------|---------|--------|-------------|---------------|
| GNN 路由 | GAT | GNN | GAT | 定制 GNN | GT (非 GNN) | GAT |
| LEO 卫星 | mega | mega | mega | WAN (非卫星) | 通用图 | Swarm (非卫星) |
| Orbital PE | 有 | 无 | 无 | 无 | RPEARL | 无 |
| 多尺度训练 | 有 | 无 | 无 | 单尺度 | 单尺度 | 单尺度 |
| Size generalization | 有 | 无 | 无 | 有(TE) | 有(理论) | 有(仅 3x) |
| 动态拓扑 | 有 | 有 | 有 | 无(静态) | 无 | 有(k-NN) |

**结论**: "GNN 路由 + Orbital PE + 多尺度训练 + size generalization"四要素组合在 LEO 卫星路由领域无完全先例。

---

## 4. 理论支撑文献

### 4.1 GNN Size Generalization 机制

| 文献 | 核心理论 | 对本研究的支撑 |
|------|---------|--------------|
| T01 (ICML'24) | 解耦大小相关/无关特征，分离学习 | 卫星拓扑恒定度数有利于解耦 |
| T02 (NeurIPS'25) | 神经网络与目标函数对齐时 size generalization 可证明成立 | Walker-Delta 规则结构可能满足对齐条件 |
| C02 (arXiv'26) | RPEARL PE 的流形收敛界 O((log N/N)^{1/d}) | Walker-Delta 可建模为球面流形采样 |

### 4.2 为什么卫星拓扑有利于 size generalization

1. **恒定度数**: Walker-Delta 每星 4 ISL，训练和推理图度分布一致
2. **球面流形**: 卫星分布在球壳上，满足 C02 的流形采样假设
3. **规则结构**: 相位偏差集合定义的 ISL 模式在任意规模保持同构
4. **L01 实证**: GKAE 从 400 星训练推广到 1444 星推理（GNN 置换不变性）

### 4.3 PE 在 size generalization 中的作用

- C02 证明 PE 是 Graph Transformer size transferability 的关键机制
- Orbital PE（基于轨道参数的位置编码）利用卫星的物理位置信息，比 RPEARL 的随机特征更结构化
- 多尺度训练确保 PE 在不同密度下学习一致的表示

---

## 5. 适配性分析汇总

### 5.1 高适配性论文（可直接迁移方法/框架）

| 论文 | 适配点 | 不适配点 | 改进方向 |
|------|--------|---------|---------|
| L06(GPN) | GAT+LSTM+PG 路由架构；30→50 零样本泛化 | 合成 Erdos-Renyi 图非卫星拓扑；规模太小 | 迁移到 LEO 拓扑，加 Orbital PE，扩展到 mega-constellation |
| L01(GKAE) | GNN 置换不变性；400→1444 星推理 | 非路由算法（预测） | 路由策略网络复用拓扑编码器 |
| L04(ISL Pattern) | Walker 星座 ISL 形式化；多密度基准数据 | 仅 Dijkstra 路由 | 用作仿真环境拓扑建模基础 |

### 5.2 中等适配性论文（方法可借鉴）

| 论文 | 适配点 | 不适配点 | 改进方向 |
|------|--------|---------|---------|
| C01(TELGEN) | GNN size generalization 20x; IPM 模仿思路 | WAN TE 非路由；监督非 RL；静态拓扑 | DRL 路由 + 动态卫星拓扑 + Orbital PE |
| C02(Size Trans.) | RPEARL PE 理论；流形收敛界 | GT 非 GNN；节点分类非路由 | 将 RPEARL 思想融入 GNN 消息传递 + Orbital PE |
| L14(GraphPR) | GAT+MADRL 全分布式；RSPH 防环 | 无 size generalization | 加多尺度训练 + PE |
| L03(DuJo) | 真实 Starlink TLE 仿真；拉格朗日乘子 | 静态快照优化 | 拉格朗日乘子融入 GNN 边特征 |
| L07(微服务路由) | 边感知注意力机制 | 微服务小规模静态 | 迁移边感知注意力到卫星链路质量建模 |

### 5.3 Baseline 参考论文

| 论文 | 作为 Baseline 的价值 |
|------|---------------------|
| L10(MCSR) | 传统路由天花板 — 10000 星分段弹性路由 |
| L11(CMCR) | 有理论保证的聚类路由 |
| L09(GARS) | O(1) 地理辅助路由 |
| L13(GRLR) | GNN+RL 路由标杆（44 引用） |
| L14(GraphPR) | GAT+MADRL 全分布式路由 |
| L16(GDRL-SFCR) | 最大规模 GNN+LEO 实验（6048 星） |

### 5.4 基础设施参考论文

| 论文 | 参考价值 |
|------|---------|
| L02(Starfield) | ISL 拓扑设计；+Grid baseline 拓扑；开源代码 |
| L05(xeoverse) | SGP4/TLE 轨道力学；Shannon + ITU-T 链路建模 |
| L03(DuJo) | Starlink TLE 数据处理框架 |
| L12(SDN) | 多控制器 SDN 部署架构 |

---

## 6. 文献索引

### 6.1 按 ID 排序

| ID | 标题简称 | DOI/arXiv | 来源 | 年份 | 引用 | 精读状态 |
|----|---------|-----------|------|------|------|---------|
| C01 | TELGEN | 10.1109/TON.2026.3659135 / arXiv:2503.24203 | IEEE/ACM ToN | 2025 | 0 | 精读 |
| C02 | Size Transferability | arXiv:2602.15239 | arXiv | 2026 | 0 | 精读 |
| C03 | Scaling Swarm | 10.3390/ai6110282 | AI journal | 2025 | 2 | 精读 |
| L01 | GKAE | arXiv:2604.27478 | arXiv | 2026 | — | 精读 |
| L02 | Starfield | arXiv:2601.10083 | arXiv | 2026 | — | 精读 |
| L03 | DuJo | arXiv:2601.21914 | arXiv | 2025 | — | 精读 |
| L04 | ISL Pattern | arXiv:2312.15873 | IEEE 期刊 | 2023 | — | 精读 |
| L05 | xeoverse | arXiv:2406.11366 | arXiv | 2024 | — | 精读 |
| L06 | GPN | 10.1109/TMC.2025.3634587 / arXiv:2510.11109 | IEEE TMC | 2025 | — | 精读 |
| L07 | 微服务路由 | arXiv:2510.15210 | arXiv | 2025 | — | 精读 |
| L08 | GNN-SD-LEO | 10.1109/NFV-SDN61811.2024.10807492 | IEEE NFV-SDN | 2024 | — | 精读 |
| L09 | GARS | 10.1109/JIOT.2025.3638842 | IEEE IoTJ | 2026 | — | 精读 |
| L10 | MCSR | 10.1109/TMC.2025.3570670 | IEEE TMC | 2025 | — | 精读 |
| L11 | CMCR | 10.1109/tvt.2024.3396350 | IEEE TVT | 2024 | 22 | 精读 |
| L12 | SDN TopoVirt | 10.1109/JIOT.2025.3576912 | IEEE IoTJ | 2025 | — | 精读 |
| L13 | GRLR | 10.1109/TVT.2024.3471658 | IEEE TVT | 2025 | 44 | 浅读 |
| L14 | GraphPR | 10.1109/TVT.2024.3499933 | IEEE TVT | 2025 | 19 | 浅读 |
| L15 | GQN | 10.1109/ICCC62479.2024.10681995 | IEEE ICCC | 2024 | 12 | 浅读 |
| L16 | GDRL-SFCR | 10.3390/s25041232 | MDPI Sensors | 2025 | — | 浅读 |
| L17 | GAT-LSTM-DQN | arXiv:2605.02413 | arXiv | 2026 | — | 浅读 |
| L18 | DTAR | — | 预印本 | 2026 | — | 浅读 |
| L19 | DeepLaDu | arXiv:2601.21921 | arXiv | 2026 | — | 浅读 |
| L20 | GNN-ASSSP | — | Aerosp. Sci. Technol. | 2026 | — | 浅读 |
| L21 | ADRLRM | 10.1109/TON.2025.3597928 | IEEE ToN | 2026 | — | 浅读 |
| L22 | FGRLR | 10.1109/LWC.2025.3593508 | IEEE WCL | 2025 | — | 浅读 |
| L23 | DGA-IES | — | IEEE IoTJ | 2025 | 5 | 浅读 |
| L24 | DLBR | — | IEEE TAES | 2025 | 12 | 浅读 |
| L25 | Transformer-MIX | — | IEEE IoTJ | 2025 | 8 | 浅读 |
| T01 | Disentangled Size Gen. | ICML #35203 | ICML | 2024 | — | 精读(理论) |
| T02 | Theory for Size Gen. | NeurIPS #118775 | NeurIPS | 2025 | — | 精读(理论) |

### 6.2 统计

- **总计**: 30 篇（精读 15 篇，浅读 13 篇，理论引用 2 篇）
- **有 DOI**: 18 篇
- **仅 arXiv**: 9 篇
- **无 ID**: 3 篇（L18, L20, T01/T02 会议投稿号）
- **时间分布**: 2023(1) → 2024(5) → 2025(14) → 2026(10)
- **引用链覆盖**: GRLR 44 篇 + GraphPR 19 篇 = 63 篇引用链筛查，无一篇涉及 size generalization

---

## 7. 背景引用（论文写作辅助引用）

> 以下论文非项目核心文献，但论文写作时必须引用作为方法基础、领域背景和理论支撑。

### 7.1 GNN 基础方法（方法章必引）

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R01 | Graph Attention Networks | Velickovic | 2018 | ICLR 2018 | arXiv:1710.10903 | 我们 GAT 编码器的架构基础 |
| R02 | Semi-Supervised Classification with Graph Convolutional Networks | Kipf | 2017 | ICLR 2017 | arXiv:1609.02907 | GCN 基础，多篇 baseline (L08, L24) 的架构来源 |
| R03 | Neural Message Passing for Quantum Chemistry | Gilmer | 2017 | ICML 2017 | arXiv:1704.01212 | 消息传递框架统一所有 GNN 方法 |
| R04 | Fast Graph Representation Learning with PyTorch Geometric | Fey | 2019 | ICLR Workshop | arXiv:1903.02428 | 实现框架 |
| R05 | Inductive Representation Learning on Large Graphs (GraphSAGE) | Hamilton | 2017 | NeurIPS 2017 | arXiv:1706.02216 | 归纳式 GNN 范式，支持不可见图泛化 |

### 7.2 LEO 卫星网络综述（引言章必引）

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R06 | Dynamic Routings in Satellite Networks: An Overview | Liu | 2022 | Wireless Comm. & Mobile Computing | DOI:10.1155/2022/5471480 | 卫星路由全面综述（快照/虚拟节点/DT-DVTR 分类） |
| R07 | Large Satellite Constellations: Challenges and Impact | CNES/ONERA | 2024 | HAL Science Report | hal-04626677 | mega-constellation 挑战最全面的 2024 报告 |
| R08 | Satellite Constellations and Connectivity from Space | ITU | 2024 | ITU Journal Vol.5(2) | ITU:S-JNL-VOL5.ISSUE2-2024 | 星座连接性和 5G/6G 集成的官方 ITU 视角 |
| R09 | Internetworking with Satellite Constellations | Wood | 2001 | PhD Thesis, Univ. Surrey | — | 提出 +Grid ISL 拓扑，被 L02/L04/L05 引用 |

### 7.3 GNN Size Generalization / Transferability 理论（补充 T01/T02）

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R10 | Graphon Neural Networks and the Transferability of GNNs | Ruiz | 2020 | NeurIPS 2020 | arXiv:2006.03548 | 基于 Graphon 极限的 GNN 可迁移性奠基理论 |
| R11 | Transferability of Spectral Graph Convolutional Neural Networks | Levie | 2021 | JMLR 22 | arXiv:1907.12972 | 证明谱图 CNN 在同离散化图间可迁移 |
| R12 | From Local Structures to Size Generalization in GNNs | Yehudai | 2021 | ICML 2021 | proceedings.mlr.press/v139/yehudai21a | 分析 size generalization 失败案例，局部结构匹配改善泛化 |

### 7.4 图位置编码方法（方法章 PE 设计）

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R13 | Attention Is All You Need | Vaswani | 2017 | NeurIPS 2017 | arXiv:1706.03762 | sin/cos 位置编码的原始出处，我们 Orbital PE 的灵感来源 |
| R14 | A Generalization of Transformer Networks to Graphs | Dwivedi | 2020 | AAAI 2021 Workshop | arXiv:2012.09699 | 将 Laplacian PE 引入图 Transformer |
| R15 | Rethinking Graph Transformers with Spectral Attention (SAN) | Kreuzer | 2021 | NeurIPS 2021 | arXiv:2106.03893 | 从完整 Laplacian 谱学习 PE，谱注意力理论 |
| R16 | Benchmarking Graph Neural Networks | Dwivedi | 2022 | JMLR 24 | jmlr.org/papers/v24/22-0567 | Laplacian 特征向量 PE 作为标准 benchmark 组件 |

### 7.5 光学 ISL / 星座设计（系统模型）

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R17 | Satellite Constellations | Walker | 1984 | J. British Interplanetary Society 37:559-571 | — | Walker 星座设计原始论文，定义 Walker-Delta 参数化 |
| R18 | Free Space Optical Communication for ISL | IEEE Comm. Magazine | 2023 | IEEE Comm. Magazine | DOI:10.1109/MCOM.002.2300024 | FSO ISL 架构和趋势权威综述 |
| R19 | Inter-Satellite Link Technologies and Applications in LEO | — | 2025 | — | DOI:10.1016/j.icl.2026.01.001 | RF 和 FSO ISL 类型综述 |

### 7.6 多尺度学习 / GNN 迁移学习

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R20 | Hierarchical Graph Representation Learning with Differentiable Pooling | Ying | 2018 | NeurIPS 2018 | arXiv:1806.08804 | 可微分分层池化，多尺度图表示 |
| R21 | Strategies for Pre-training Graph Neural Networks | Hu | 2020 | ICLR 2020 | OpenReview:HJlWWJSFDH | GNN 预训练策略（节点级/图级），迁移学习范式 |
| R22 | GPT-GNN: Generative Pre-Training of GNNs | Hu | 2020 | KDD 2020 | arXiv:2006.15437 | 自监督图生成预训练 |

### 7.7 DRL 基础方法

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R23 | Proximal Policy Optimization Algorithms | Schulman | 2017 | arXiv | arXiv:1707.06347 | PPO 算法，RL baseline 的训练基础 |
| R24 | High-Dimensional Continuous Control Using GAE | Schulman | 2016 | ICLR 2016 | arXiv:1506.02438 | GAE 平衡策略梯度偏差-方差 |
| R25 | ML for Combinatorial Optimization: a Methodological Tour d'Horizon | Bengio | 2021 | European J. Operational Research | arXiv:1811.06128 | 路由组合优化 ML 权威综述 |
| R26 | Attention, Learn to Solve Routing Problems! | Kool | 2019 | ICLR 2019 | OpenReview:ByxBFsRqYm | Transformer 路由，注意力解决路由 CO 问题 |

### 7.8 经典卫星路由方法

| # | 标题 | 第一作者 | 年份 | 来源 | 标识符 | 引用理由 |
|---|------|---------|------|------|--------|---------|
| R27 | A Note on Two Problems in Connexion with Graphs | Dijkstra | 1959 | Numerische Mathematik 1:269-271 | DOI:10.1007/BF01386390 | 最短路径算法原始论文，我们推理阶段和 baseline |
| R28 | A Distributed Routing Algorithm for Datagram Traffic in LEO Satellite Networks | Ekici | 2001 | IEEE/ACM ToN 9(2) | — | 经典分布式 LEO 数据报路由，基于位置路由 baseline |
| R29 | A Dynamic Routing Concept for ATM-Based Satellite PCN | Werner | 1997 | IEEE JSAC 15(2):163-171 | — | 首个快照动态路由 (DT-DVTR) 概念 |
| R30 | Reinforcement Learning for Combinatorial Optimization: A Survey | Mazyavkina | 2021 | Computers & Operations Research | arXiv:2003.03600 | RL 组合优化全面综述 |

### 7.9 统计

- **背景引用总计**: 30 篇（R01-R30）
- **类别分布**: GNN基础(5) / LEO综述(4) / 泛化理论(3) / 图PE(4) / ISL星座(3) / 多尺度迁移(3) / DRL基础(4) / 经典路由(4)
- **时间分布**: 1959(1) → 1997-2001(3) → 2017-2019(7) → 2020-2022(12) → 2023-2025(7)
- **全部文献总计**: 60 篇（L01-L25 + C01-C03 + T01-T02 + R01-R30）
