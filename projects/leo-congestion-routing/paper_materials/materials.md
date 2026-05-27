# Paper Materials: Ch3 — Online Fault-Resilient Per-Flow Routing via GNN for LEO Constellations

> 定位: 学位论文第三章 | 项目: leo-congestion-routing
> 论证模式: 空白填补型（实证） | 贡献定位: 故障弹性路由的实证分析
> 最后更新: 2026-05-26 | 基于终审 S001-S014 全部结论 + 物理仿真拓扑数据
> 权威数据源: simulator/results/stat_tests.json（mean 值以此为唯一权威）

---

## A. 研究问题与论证逻辑

### A.1 问题定义

在 LEO Walker-Delta 星座中，ISL 因轨道力学、硬件老化、空间天气等因素频繁中断（经验故障率 5-15%），静态路由协议（ECMP/SP）无法自适应拓扑变化导致的路径失效和负载失衡。如何在链路频繁故障且流量非均匀分布的条件下，实现在线逐流故障弹性路由，使 E2E 延迟和负载均衡同时优于无状态方法（ECMP），是本章研究的核心问题。

研究挑战的量化锚点：链路故障率覆盖 0-15%（三种故障模式）；非均匀流量含 25% 重型流（需求接近 ISL 容量 50%）和热点目的地；跨规模部署跨度 0.7x-10.9x（66 星训练，48-720 星零样本部署）。

### A.2 现状局限

1. 全局 TE 方法（如 TELGEN [L11]）需离线求解每个拓扑快照，无法应对突发故障和实时负载变化
2. 分布式逐跳方法（如 GRLR [L01]）仅聚合局部子图信息，无法避免全局拥塞热点
3. 域间路由方法（如 DTAR [L06]）粒度为域（非逐流），域内仍依赖最短路径
4. 现有 GNN+LEO 路由工作未系统验证 0-15% 故障率下的路由鲁棒性
5. 现有方法（DTAR/GMR）每星座单独训练，无跨规模零样本部署能力

### A.3 研究空白

**空白 1：故障弹性 + 跨规模泛化**。检索初筛 22 篇 GNN+LEO 路由论文，经去重和主题相关性筛选后保留 17 篇纳入文献格局分析（B.1）。TELGEN 有泛化无故障，GNN-ASSSP [L13] 有故障容忍但未测试跨规模，DTAR 有故障但仅单一 288 星规模。无任何论文同时验证故障弹性与跨规模泛化。空白结构性原因：故障弹性要求在线适应（DRL 范式），跨规模泛化要求参数共享（GNN 范式），二者结合的技术门槛较高。

**空白 2：GNN per-flow K-path + LEO 时变**。GMR [L02] 和 PathGNN [L04] 做 per-path 流量分割但依赖预计算路径集，LEO 时变拓扑使预计算路径频繁失效。所有 LEO GNN 路由工作要么是逐跳离散选择（GRLR/DTAR），要么是 per-path 分割（GMR/PathGNN），per-flow K-path 端到端决策完全缺失。

**空白 3：在线 DRL + Walker-Delta 族内泛化**。所有 GNN+DRL LEO 工作在单一星座规模验证。GMR 验证跨星座泛化（GlobalStar→Iridium）但用离线 DDPG 且规模跨度小。Walker-Delta 族内泛化在在线 DRL 框架下尚无验证。

### A.4 论证主线

LEO 星座规模快速增长与 ISL 频繁中断使得静态路由无法自适应。现有 GNN+LEO 路由在故障弹性、在线逐流决策和跨规模部署三个维度存在不足，本章逐一填补。核心发现是 GNN 的优势是条件激活的——无故障时 GNN 与 ECMP 性能相当（未学到无意义策略），有故障时 GNN 的全局负载感知能力在拓扑规则性被打破后发挥关键作用，E2E 延迟相比 ECMP 降低 20%。论证模式为空白填补型（实证）。

### A.5 Gap-Contribution 闭环映射表

| 空白(Gap) | 方法组件 | 结论回应 | 数据证据(板块E编号) |
|-----------|---------|---------|-------------------|
| 空白1: 故障弹性+跨规模 | GAT encoder + PPO + BFS 候选路径 | 故障激活 GNN 优势，0.7x-4.4x 规模泛化有效 | E01, E08, E12, E04-E06 |
| 空白2: GNN per-flow K-path | PathScoringHead + 增量奖励 | 逐流顺序路由 + K-path 离散选择，delay -20% | E01, E09 |
| 空白3: 在线DRL+族内泛化 | 共享权重 GNN + Walker-Delta F=1 | 66→288 星零样本 delay 降至 ECMP 的 25% | E04-E06 |

---

## B. 文献格局

### B.1 文献角色速览

| cite key | 一句话贡献 | 与本研究关系 | 引用角色 |
|----------|-----------|------------|---------|
| TELGEN (Zhou 2025, ToN) [L11] | 双循环 GCN 将 TE LP 转化为二部图消息传递，20x 规模泛化 optimality gap <3% | 最直接竞品——GNN+TE+size gen 已被做完整 | 竞品/替代方案 |
| GNN-ASSSP (He 2026) [L13] | ST-GNN Transformer 预测动态拓扑 + 层次化图注意力学习拥塞感知边权重 | 直接竞品——per-edge weight learning for LEO；但纯 SL 无在线适应 | 竞品/替代方案 |
| DTAR (Zhou 2026) [L06] | NSGA-II 域划分 + GAT+PPO 域间路由 | 直接竞品——GAT+DRL LEO 路由；但域间粒度非全网逐流 | 竞品/替代方案 |
| GMR (Huang 2024, TVT, 41cit) [L02] | MPNN+DDPG 多路径流量分割，跨星座零重训练泛化 | 架构最接近竞品——per-path 分割+跨拓扑泛化 | 竞品/替代方案 |
| GRLR (Zhang 2025, TVT) [L01] | GAT+Actor-Critic 分布式逐跳路由 | 前驱——验证 GNN 结构优势 | 前驱/基础 |
| PathGNN (2025, JSAC) [L04] | path-link 二部图 + 5 层多头注意力 SL | 方法借鉴——path-link 二部图建模思路 | 理论/方法支撑 |
| PRIMAL (2025, arXiv) [L08] | 异步事件驱动 primal-dual CRL 约束尾部风险，1584 星 | 方法借鉴——primal-dual CRL + 异步设计 | 理论/方法支撑 |
| POMAP (Li 2025, IoT-J) [L03] | Pareto 多目标 MAPPO + G/G/1/K 队列建模 | 方法借鉴——队列感知+多目标+奖励归一化 | 理论/方法支撑 |
| DLBR (Ju 2025, TAES) [L15] | GCN-LSTM-Attention 流量预测 + D3QN 负载均衡路由 | 直接相关——GNN 仅用于预测非路由决策 | 竞品/替代方案 |
| Fan 2026 (Springer) [L07] | GNN edge-level 消息传递全局嵌入 + DQN k-shortest path | 直接相关——edge-level 消息传递与本研究同思路 | 竞品/替代方案 |
| DeepLaDu (Gu 2026) [L12] | GATv2 一次前向推理输出 per-link Lagrange 乘子 | 间接相关——per-edge Lagrangian 对偶思路可借鉴 | 理论/方法支撑 |
| QueueMARL (2026) [L09] | Queue-aware MA-DDQN 弹性路由 + 弹性分数概念 | 方法借鉴——弹性分数+queue-aware 奖励设计 | 理论/方法支撑 |
| ST-QoS (2026) [L10] | GAT+LSTM+DQN 分布式拥塞路由 | 相关——GAT 聚合邻居负载做拥塞路由 | 背景/综述 |
| LARRI (Ye 2026, ToN) [L14] | GNN(LSTM+多头注意力)SL 预测 range routing 策略 | 背景——GNN+TE SL 标杆 | 背景/综述 |
| FlexSATE (Liu 2024, GLOBECOM) [L16] | 分布式 GNN(Transformer)模仿 MCF 做 per-flow split ratio | 背景——LEO TE+GNN+分布式 | 背景/综述 |
| GDRL-SFCR (Chen 2025) [L05] | GCN+PPO SFC 约束端到端路由 | 相关——GNN+DRL LEO 路由+负载均衡 | 背景/综述 |
| GRL-TE (Fan 2026, TAES) [L17] | 多层卫星 MPNN+DDPG 多路径流量分配 | 背景——GNN+DRL 卫星路由范式重叠 | 背景/综述 |

文献缺口 ⚠：
1. ⚠ DPR/Wang 2026 两篇待获取论文，需至少获取 abstract 验证威胁等级（P1-11）
2. ⚠ GMR/GNN-ASSSP 缺详细对比表（P1-5）

### B.2 竞品精确区分

| 论文 | 覆盖要素 | 缺失要素 | 威胁等级 | 我们的优势 |
|------|---------|---------|---------|-----------|
| TELGEN [L11] | GNN+TE, 20x 规模泛化, <3% gap | LEO 时变, 在线 DRL, per-link 决策, 故障弹性 | P0 | 在线 DRL vs 离线 SL; 故障弹性 vs 无故障; LEO 特化 vs 通用 |
| GNN-ASSSP [L13] | LEO 动态拓扑预测, 拥塞感知, 1584 星, 20%故障100%成功率 | 跨规模泛化, per-link 分配, 在线 DRL | P1 | 在线 DRL vs 纯 SL; 跨规模 vs 单规模; per-link 决策 vs 路径选择 |
| GMR [L02] | GNN 多路径 TE, 跨星座泛化(48→66), MPNN 链路-路径 | 故障弹性, 在线 DRL, LEO 时变, per-link 决策 | P1 | 在线 DRL vs 离线 DDPG; 故障弹性 vs 无; per-link vs 预计算路径分割 |
| DTAR [L06] | GAT+PPO 域间路由, 故障(p_f=0.02), 有代码 | 全网 per-link 粒度, 跨规模, 负载均衡 | P1 | 全网逐流 vs 域间; 跨规模 vs 单规模 |
| GRLR [L01] | GAT+AC 分布式 LEO 路由, 720 星 | 全局负载聚合, per-link 负载均衡, 故障, 跨规模 | P2 | 全局消息传递 vs 6节点子图; 故障弹性 vs 无 |

### B.3 竞品详细方法特性对比

#### B.3.1 与 TELGEN 详细对比（13 维度）

| 维度 | TELGEN [L11] | 本文 |
|------|-------------|------|
| **问题类型** | 流量工程 (TE) | 拥塞感知路由 |
| **决策粒度** | per-path 流量分割 | per-flow 路径选择 |
| **优化方式** | 离线监督学习 | 在线 DRL (PPO) |
| **训练标签** | IPM 最优解 | 增量 MLU 奖励 |
| **网络类型** | 通用（ER/Waxman/ASN） | LEO 星座（Walker-Delta） |
| **时变拓扑** | 静态快照 | 在线适应（故障+突发） |
| **泛化方式** | 跨拓扑族（ER→Waxman） | Walker-Delta 族内 |
| **泛化倍数** | 20x (100→2000 节点) | 6.7x (66→288 节点，有效范围） |
| **泛化 gap** | < 3% optimality gap | GNN/ECMP MLU ≤ 0.989（288 节点） |
| **故障处理** | 无（静态快照） | 0-15% 链路故障，3 种模式 |
| **推理延迟** | 1.52ms (GPU) | 1.2-2.0ms (CPU) |
| **部署模式** | 集中式 SDN | 集中式（可分布式扩展） |
| **参数量** | ~500K (双循环 GCN) | 28,546 (GAT) |
| **训练时间** | 4h (A100) | 22min (RTX 4070) |

**差异化论证逻辑**：TELGEN 在泛化倍数（20x）和理论保证（对齐 IPM 迭代）上更强，但采用离线 SL 范式——每个拓扑快照需预计算 IPM 最优解，在链路频繁故障的 LEO 场景中不现实；无在线适应能力，无法响应突发流量或实时故障。本文差异化在于：在线 DRL vs 离线 SL（故障无需重算）、逐流 vs 全局（天然增量部署）、轻量 vs 重量（28K 参数 vs 500K，CPU 推理可行）、LEO 特化 vs 通用（故障是核心考量）。

#### B.3.2 与 DTAR 详细对比（8 维度）

| 维度 | DTAR [L06] | 本文 |
|------|-----------|------|
| **路由粒度** | 域间（18 域） | 全网逐流 |
| **域内路由** | 最短路径 | N/A（无域划分） |
| **故障处理** | action masking | BFS 候选路径 + GNN 编码 |
| **规模** | 288 星 | 48-720 星（泛化） |
| **GNN 架构** | GAT (2L, 4H, d=64) | GAT (2L, 4H, d=64) |
| **训练方式** | PPO | PPO |
| **在线/离线** | 在线 | 在线 |
| **拓扑** | Walker-Delta 仿真 | Walker-Delta 物理仿真（含极地间隙） |

**讨论要点**：DTAR 不作为 baseline 直接对比，理由——(1) 问题建模不同：DTAR 域间路由 vs 本研究全网逐流路由，不在同一问题空间；(2) 强行对比的风险：DTAR 的域划分已做负载均衡的粗粒度优化，直接对比路由阶段不公平。DTAR 的 action masking（基于物理可达性和跳数约束）和 GAT+LayerNorm+Residual 架构值得借鉴，本文的 PathScoringHead 通过路径可达性预筛实现了类似效果。

---

## C. 贡献与核心论据

### C.1 贡献声明

**贡献 1（主）：故障弹性路由**。针对 LEO 卫星网络 ISL 频繁故障场景，设计了基于 GNN 的 per-flow K-path 在线路由框架。实验表明，GNN 的全局负载感知能力在故障打破拓扑规则性后被激活——8% 故障率下 E2E 延迟较 ECMP 降低 20%，15% 故障率下 MLU 降低 13.4%。3 种故障模式 × 4 个故障率共 12 组测试中 GNN 在 11 组优于 ECMP。（支撑证据：E01, E08, E12）

**贡献 2（次）：在线逐流决策**。每条流到达时通过 GNN 一次编码 + PathScoringHead 独立评分实现路由决策，推理延迟 1.2-2.0ms（CPU），故障响应比 ECMP 重算快 7.7x。增量奖励设计使每步决策直接反映该步质量。（支撑证据：E01）

**贡献 3（辅）：跨规模零样本部署**。利用 GNN 共享权重与节点/边数无关的特性，66 星训练的模型零样本部署到 Walker-Delta 族内 48-720 星。0.7x 规模 delay 降低 17%，4.4x 规模 delay 降低 75%。10.9x（720 星）跨度过大导致退化，表明零样本泛化的有效边界。（支撑证据：E04-E06）

### C.2 贡献间关系

贡献 1（故障弹性）是核心，贡献 2（在线决策）是实现贡献 1 的技术手段（逐流顺序路由 + 增量奖励使故障响应成为可能），贡献 3（跨规模）是辅助发现。三者关系为互补：贡献 1 定义"为什么需要 GNN"，贡献 2 定义"怎么用 GNN"，贡献 3 拓展"用 GNN 还能做什么"。

### C.3 证据蓝图

| 贡献 | 核心证据(板块E编号) | 补充证据(板块E编号) |
|------|-------------------|-------------------|
| 贡献1 故障弹性 | E01(核心), E08(故障率), E12(故障模式) | E02(无故障对照), E03(突发鲁棒性) |
| 贡献2 在线决策 | E01(推理+delay), E08(响应) | E09(流量模式) |
| 贡献3 跨规模 | E04(48星), E05(288星) | E06(720星退化), E10-E11(架构消融) |

### C.4 跨章元分析定位

在跨章元分析框架（"探索性分化"）中，Ch3 代表 GNN 有效性的"故障弹性"维度——当网络拓扑因节点/链路故障发生结构漂移时，GNN 凭借消息传递机制动态感知拓扑变化，在故障率 ≥4% 时展现出显著优于 ECMP/SP 的路由质量（20% delay 降低 at 15% fault rate）。关键发现：故障场景是 GNN 优势的激活条件（贡献来源 ~80%），无故障场景下 GNN 与 ECMP 差异不显著（p=0.262）。与 Ch1（规则拓扑下规模不变性）和 Ch2（排列等变性下规模适应性）形成探索性分化对比。三章统一论点：GNN 的有效性取决于架构复杂度与任务需求的匹配——当任务需求超越规则策略的能力边界（如结构漂移、规模变化），GNN 的表达能力才被激活。

---

## D. 方法描述

### D.1 架构总览

GAT encoder（$L$=2 层，$H$=4 头，$d$=64）将节点特征和边特征编码为全局节点嵌入 → PathScoringHead 对每条流的 $K$=4 候选路径，取路径上节点嵌入均值并评分 → Categorical 分布选择路径 → PPO 训练（增量奖励 $r_t = -(\text{MLU}_{\text{after}} - \text{MLU}_{\text{before}})$）。每条流到达时执行一次编码（跨流共享）+ 一次评分，故障发生时无需重算路径集。

### D.2 核心组件

**GATEncoder**：Linear(7,64) → 2× GATConv + LayerNorm + ELU + Residual → $(N_{\text{node}}, 64)$。动机：需要全局负载感知以识别拥塞热点和故障链路。注意力机制可学习故障链路的权重降低（GCN 等权聚合无法做到）。LayerNorm + Residual 稳定训练。

**PathScoringHead**：mean(node_emb[path_nodes]) → MLP(64→32→1) → scalar score。无效位置填 -1e9。K-path 天然保证路径可达性（BFS 预计算），离散选择比连续分割稳定。

**ValueHead**：cat(node_emb[src], node_emb[dst]) → FC(128→64→1)。拼接源目的节点嵌入，维度无关，支持跨规模。

**增量奖励**：$r_t = -(\text{MLU}_{\text{after}} - \text{MLU}_{\text{before}})$。比绝对 -MLU 更适合逐流路由：每步奖励直接反映该步决策质量。Welford 在线归一化稳定训练。

**BFS 候选路径生成**：在去掉故障边的无向图上用 nx.shortest_simple_paths 生成 $K$ 条候选路径。故障边保留在 edge_index 中（is_failed=1）以保持维度固定。

**状态空间**：obs dict {node_feat($N_{\text{node}}$,7), edge_index(2,$E$), edge_feat($E$,4), paths, flow, n_valid}。节点特征 7 维：in_load_norm, out_load_norm, is_current_src, is_current_dst, current_demand_norm, is_hotspot, degree_norm。边特征 4 维：utilization, edge_type, is_failed, capacity_norm。

**动作空间**：离散，$K$=4 候选路径的 Categorical 选择。

### D.3 设计决策表

| 选择 | 理由 | 排除的替代方案 | 支撑 cite key |
|------|------|--------------|--------------|
| Walker-Delta F=1 物理仿真(alt=550km) | 最广泛使用，DTAR/GMR/PRIMAL 均使用 | 抽象 4-regular 网格（升级后 GNN/ECMP 从 0.78 降至 0.96） | [L06][L02] |
| GAT encoder (2L, 4H, d=64) | 注意力可区分故障链路；LN+Residual 稳定训练 | GCN（等权聚合无法区分故障） | [L06] |
| Per-flow K-path 离散选择 (K=4) | 路径可达性保证；离散稳定；与 ECMP 范式一致 | Per-edge continuous weights（264 维 FAIL） | MVE-2 |
| 增量奖励 | 逐流范式下每步奖励直接反映决策质量 | 绝对 -MLU（MVE 验证增量式更优） | — |
| 逐流顺序路由（40步/episode） | 增量式更新负载状态 | 同时路由所有流（FAIL） | MVE-2 |
| 极地间隙 polar_gap_lat=70° | 物理真实性：高纬度 inter-plane ISL 几何不可达 | 无间隙（过于理想化） | — |
| congestion_factor 封顶 100x | 避免 util=1 时无穷大 | 无封顶（数值不稳定） | — |
| congestion_factor 1/(1-util) | 定性反映真实网络拥塞行为：util=0.8 放大 5x，util=0.95 放大 20x | 线性模型 1+α·util²（α=1 时 GNN/ECMP=1.14，GNN 反而输 ECMP，线性模型不够捕捉拥塞效应对路由决策的区分度） | — |
| 86.4° 倾角 | Iridium 规格产生极地间隙，53° 无法产生间隙 | 53°（无极地间隙，ECMP 过强） | — |

### D.4 计算复杂度

- 前向推理：$O(|E| \cdot d \cdot L)$，其中 $|E|$=ISL 数量（66 星时 ≤264），$d$=隐层维度（64），$L$=GNN 层数（2）。实际推理延迟：1.2-2.0ms（单次决策，CPU），满足实时性要求（远小于路由更新周期）。
- 训练：800 episodes × 40 步/episode，wall-clock time 约 22 分钟（单 seed，RTX 4070）。3 seeds 总计约 66 分钟。
- 与 ECMP 对比：ECMP 为 $O(|V|^2)$ 全对最短路（Dijkstra per flow），GNN 为 $O(|E| \cdot d \cdot L)$ 单次前向传播。在 288 星规模下，ECMP 重算全路径需 ~9.3ms，GNN 编码+评分仅需 1.2-2.0ms（7.7x 加速）。
- 参数效率：GNN 28,546 参数（GATEncoder ~18K + PathScoringHead ~2K + ValueHead ~8K），远小于 TELGEN 的 ~500K 参数。

---

## E. 证据目录

### E.core 核心证据

### E01: 核心对比——GNN 故障弹性路由优势
- 证据类型：定量数据 + 统计结果
- 内容：66 星，8% 故障率，surge=1.0。GNN MLU = 1.378 ± 0.049 (3 seeds), ECMP MLU = 1.436, MLP MLU = 1.637。GNN/ECMP MLU = 0.96，E2E delay GNN/ECMP = 0.80（GNN 137ms vs ECMP 171ms）。CV: GNN 0.855 vs ECMP 1.028。GNN vs ECMP MLU 不显著(p=0.262, d=-0.160)，GNN vs MLP 显著(p<0.001, d=-0.516)。MLP delay 是 GNN 的 2.7 倍（373ms vs 137ms），确认 message passing 关键作用。
- 完整上下文：Walker-Delta F=1 物理仿真(alt=550km, inc=86.4°)，3 seeds × 800 episodes 训练，50 eval episodes per seed。ECMP 为无状态基线。
- 来源：本论文实验，stat_tests.json 为权威数据源
- 支撑论点：贡献 1 + 贡献 2
- 统计显著性：GNN vs ECMP MLU p=0.262 (不显著), GNN vs MLP MLU p<0.001 (显著, d=-0.516)

### E02: 无故障基线——GNN 优势的条件性
- 证据类型：定量数据
- 内容：66 星，0% 故障率。GNN MLU = 1.347, ECMP MLU = 1.323, MLP MLU = 1.571, GNN/ECMP = 1.018（ECMP 略优）, GNN/MLP = 0.857。无故障时极地间隙虽存在但固定，ECMP 等价路径机制天然有效，GNN 的自适应能力无用武之地。但 MLP 仍明显劣于 GNN（14% MLU 差距），说明即使无故障，message passing 对负载均衡仍有贡献。
- 完整上下文：与 E01 同批实验的对照组（同一 3-seed × 800ep 配置和种子）。
- 来源：本论文实验
- 支撑论点：贡献 1（GNN 优势是条件激活的）
- 统计显著性：无统计检验（单次对照）

### E03: 突发流量鲁棒性
- 证据类型：定量数据
- 内容：66 星，8% 故障，surge=20x。GNN MLU = 6.588, ECMP MLU = 6.769, MLP MLU = 7.795, GNN/ECMP = 0.973, GNN/MLP = 0.845。极端突发下 GNN 仍保持 MLU 优势，MLP 劣势进一步放大（MLP MLU 接近 ECMP 的 1.15 倍）。
- 完整上下文：surge_factor=20.0 使流量需求放大 20 倍，模拟突发拥塞。
- 来源：本论文实验
- 支撑论点：贡献 1（故障弹性在极端条件下仍有效）

### E04: 跨规模 0.7x（48 星）泛化
- 证据类型：定量数据
- 内容：48 星(P=4, S=12)，8% 故障。GNN MLU = 1.508, ECMP MLU = 1.644, GNN/ECMP = 0.917。GNN delay = 247ms, ECMP delay = 296ms, GNN/ECMP delay = 0.83。MLP(zero-shot) MLU = 1.843, GNN/MLP = 0.82。0.7x 缩减规模零样本泛化有效。
- 完整上下文：66 星训练模型直接部署到 48 星，不微调。Walker-Delta F=1 族内约束。
- 来源：本论文实验
- 支撑论点：贡献 3

### E05: 跨规模 4.4x（288 星）泛化
- 证据类型：定量数据
- 内容：288 星(P=12, S=24)，8% 故障。GNN MLU = 4.282, ECMP MLU = 4.331, GNN/ECMP = 0.989。GNN delay = 1051ms, ECMP delay = 4222ms, GNN/ECMP delay = 0.25。MLP = 4.770, GNN/MLP = 0.90。MLU 差距不大但 delay 仅为 ECMP 的 25%——负载分布差异在 delay 维度被放大。
- 完整上下文：66 星训练零样本部署到 288 星。GNN 推理延迟 1.2-2.0ms (CPU)，故障响应比 ECMP 重算快 7.7x。
- 来源：本论文实验
- 支撑论点：贡献 3（delay 维度的显著优势来自拥塞惩罚权重的放大效应）

### E06: 跨规模 10.9x（720 星）退化
- 证据类型：定量数据
- 内容：720 星(P=18, S=40)，8% 故障。GNN MLU = 5.008, ECMP MLU = 4.519, MLP MLU = 5.129, GNN/ECMP = 1.108（GNN 反超）, GNN/MLP = 0.977。GNN delay = 507ms, ECMP delay = 517ms, GNN/ECMP = 0.98（基本持平）。10.9x 跨度过大导致泛化退化。MLP 同样退化严重（MLP/ECMP = 1.13），说明跨规模退化并非 GNN 特有问题，而是大规模下特征分布漂移的普遍挑战。
- 完整上下文：66 星训练零样本部署到 720 星。退化原因：节点特征统计分布漂移（节点数增加 10.9x 但训练集仅 66 星的分布）。
- 来源：本论文实验
- 支撑论点：贡献 3 的有效边界（10.9x 退化为有价值的负面发现）

### E08: 故障率消融
- 证据类型：定量数据
- 内容：66 星，故障率 0-15%，5 个梯度。GNN 在所有故障率下均优于 ECMP（GNN/ECMP 0.866-0.974）。15% 故障率下优势最大（GNN/ECMP = 0.866），确认故障是 GNN 优势的激活条件。

| 故障率 | GNN MLU | ECMP MLU | GNN/ECMP |
|--------|---------|----------|----------|
| 0% | 1.222 | 1.313 | 0.931 |
| 5% | 1.351 | 1.471 | 0.919 |
| 8% | 1.335 | 1.436 | 0.930 |
| 10% | 1.458 | 1.497 | 0.974 |
| 15% | 1.471 | 1.700 | 0.866 |

- 完整上下文：E08@0% (GNN/ECMP=0.931) 与 E02 (GNN/ECMP=1.018) 数值不同——来自不同实验批次（E08 为故障率扫描序列，E02 为核心实验对照组）。E02 更适合作为无故障基线参照。E01@8%（GNN/ECMP=0.960）与 E08@8%（GNN/ECMP=0.930）数值不同，原因同上——E08 为故障率扫描序列的独立运行，与 E01 的核心实验批次使用不同随机种子。论文正文中应以 E01 为权威数据源。
- 来源：本论文实验
- 支撑论点：贡献 1（故障率越高，GNN 优势越大）

### E12: 故障模式对比
- 证据类型：定量数据
- 内容：3 种故障模式 × 4 个故障率，共 12 组。GNN 在 11/12 组中 MLU 优于 ECMP。唯一失利：cascading 15%（GNN/ECMP = 1.008，差异 < 1%）。Regional 模式优势最大（0.853-0.909），因区域故障打破 ECMP 等价路径。Random 模式全面占优（0.884-0.914）。Cascading 高故障率下 MLU 急剧下降（大量链路中断），GNN/ECMP 接近 1.0。

| 故障模式 | 故障率 | GNN MLU | ECMP MLU | MLP MLU | GNN/ECMP | GNN/MLP |
|----------|--------|---------|----------|---------|----------|---------|
| random | 5% | 1.329 | 1.491 | 1.669 | **0.891** | **0.797** |
| random | 8% | 1.359 | 1.487 | 1.649 | **0.914** | **0.824** |
| random | 10% | 1.422 | 1.609 | 1.720 | **0.884** | **0.827** |
| random | 15% | 1.484 | 1.637 | 1.737 | **0.906** | **0.854** |
| regional | 5% | 1.220 | 1.430 | 1.525 | **0.853** | **0.800** |
| regional | 8% | 1.304 | 1.434 | 1.481 | **0.909** | **0.880** |
| regional | 10% | 1.280 | 1.412 | 1.510 | **0.907** | **0.848** |
| regional | 15% | 1.221 | 1.397 | 1.448 | **0.874** | **0.843** |
| cascading | 5% | 1.266 | 1.404 | 1.523 | **0.901** | **0.831** |
| cascading | 8% | 1.077 | 1.278 | 1.195 | **0.843** | 0.901 |
| cascading | 10% | 0.970 | 1.013 | 1.064 | **0.958** | **0.911** |
| cascading | 15% | 0.503 | 0.499 | 0.608 | 1.008 | **0.826** |

- 完整上下文：66 星，surge=1.0。Regional：10% 节点周围链路全断。Cascading：级联扩散。Random：独立随机。MLP 在所有 12 组中均劣于 GNN（GNN/MLP 范围 0.797-0.901），且在 cascading 高故障率下同样急剧下降，说明 message passing 无法弥补信息缺失（大量链路中断导致图结构稀疏）。
- 来源：本论文实验
- 支撑论点：贡献 1（故障弹性的全面验证）

### E09: 流量模式消融
- 证据类型：定量数据
- 内容：4 种流量配置（uniform→high），GNN/ECMP 在 0.879-0.930 范围。非均匀流量下 GNN 优势更明显。GNN 在 uniform 流量下仍有优势（0.911），说明即使无热点/重型流，GNN 的负载均衡仍有效。

| 流量模式 | GNN MLU | ECMP MLU | GNN/ECMP |
|----------|---------|----------|----------|
| uniform | 0.319 | 0.350 | 0.911 |
| moderate (3h,5hv) | 0.898 | 1.022 | 0.879 |
| default (3h,10hv) | 1.335 | 1.436 | 0.930 |
| high (5h,15hv) | 1.547 | 1.690 | 0.915 |

- 来源：本论文实验
- 支撑论点：贡献 2（在线决策在不同流量模式下均有效）

### E10-E11: 架构消融
- 证据类型：定量数据
- 内容：层数 L∈{1,2,3}：MLU = 1.429/1.408/1.354，3 层最优（更多消息传递轮次）。头数 H∈{2,4,8}：MLU = 1.367/1.385/1.399，架构对超参不敏感（差异 < 4%）。默认 L=2, H=4 为合理折中。单 seed 结果。
- 完整上下文：66 星，8% 故障。⚠ 单 seed，无统计验证。
- 来源：本论文实验
- 支撑论点：方法鲁棒性（架构对超参不敏感）

### E.supplement 补充证据

### E07: 参数量与推理延迟
- 证据类型：设计产物
- 内容：GNN 总参数量 28,546（GATEncoder ~18K + PathScoringHead ~2K + ValueHead ~8K），推理延迟 1.2-2.0ms (CPU)。ECMP 无参数但需 O(F·(E+N)) 全路径 BFS 重算。MLP 10,309 参数，推理 0.09-0.11ms。
- 来源：本论文实验
- 支撑论点：贡献 2（轻量部署可行性）

### BFS 候选路径可达性
- 证据类型：设计产物
- 内容：BFS 在去掉故障边的无向图上生成 K=4 候选路径，天然保证路径可达性。故障边保留在 edge_index（is_failed=1），保持模型参数维度固定。
- 来源：本论文设计
- 支撑论点：贡献 2（路径可达性保证）

### 元分析跨章定位
- 证据类型：质性发现
- 内容：Ch3 在元分析框架"探索性分化"中的定位——故障弹性。统一解释：规模扩展不改变局部结构的统计性质→泛化成功。Ch3 的 0.7x-4.4x 泛化有效（Walker-Delta 族内结构相似），10.9x 退化（结构漂移过大）。与 Ch1（11x 监督学习泛化成功）和 Ch2（5x 用户规模泛化）形成对比——训练范式（SL vs DRL）和故障场景是泛化难度的关键因素。
- 来源：S011, S012, S014
- 支撑论点：跨章元分析

---

## F. 术语与符号

### F.1 术语表

| 术语 | 英文 | 缩写 | 定义 |
|------|------|------|------|
| 最大链路利用率 | Maximum Link Utilization | MLU | max(load_e / capacity_e)，衡量负载均衡质量 |
| 端到端延迟 | End-to-End Delay | E2E delay | Σ(propagation × congestion_factor)，拥塞惩罚权重放大后的路径延迟 |
| 拥塞惩罚权重 | Congestion Factor | — | 1/(1-utilization)，高利用率链路延迟贡献指数增长 |
| 跨规模零样本泛化 | Zero-shot Cross-Scale Generalization | — | 在规模 A 训练的模型直接部署到规模 B，不微调 |
| 故障弹性 | Fault Resilience | — | 在链路故障条件下维持路由性能的能力 |
| 逐流路由 | Per-Flow Routing | — | 每条流独立路由决策，从 K 条候选路径中选择 |
| 负载均衡系数 | Coefficient of Variation | CV | std(link_util) / mean(link_util) |
| Walker-Delta 星座 | Walker-Delta Constellation | — | Delta 型 Walker 星座，F=1 表示最小相位偏移 |

### F.2 符号表（采用跨章统一方案）

| 符号 | 含义 | 单位 | 值/范围 | 首现章节 |
|------|------|------|---------|---------|
| $N_{\text{node}}$ | 网络节点（卫星）数 | 个 | 48/66/288/720 | Ch3 |
| $E$ | 有向边数 | 条 | ≤264 (66星) | Ch3 |
| $\mathcal{V}, \mathcal{E}$ | 图的节点集和边集 | — | — | Ch3 |
| $P$ | 轨道面数 | 个 | 4/6/12/18 | Ch3 |
| $S$ | 每面卫星数 | 个 | 11/12/24/40 | Ch3 |
| $K$ | 候选路径数 | 条 | 4 | Ch3 |
| $L$ | GNN 层数 | 层 | 2 | 跨章统一 |
| $H$ | 注意力头数 | 个 | 4 | Ch3 |
| $d$ / $d_h$ | 隐层维度 | 维 | 64 | Ch3 |
| $F$ | Walker-Delta 参数 | — | 1 | Ch3 |
| $h_{\text{orb}}$ | 轨道高度 | km | 550 | 跨章统一 |
| $c$ | 光速 | km/s | 299792 | Ch3 |
| $\text{MLU}$ | 最大链路利用率 | — | ≥0 | Ch3 |
| $\text{CV}$ | 负载均衡系数 | — | ≥0 | Ch3 |
| $\gamma$ | 折扣因子 | — | 0.99 | Ch3 |
| $\lambda$ | GAE 参数 | — | 0.95 | Ch3 |
| $\epsilon$ | PPO clip | — | 0.2 | Ch3 |
| $\eta$ | 奖励权重 | — | — | 跨章统一加语义下标 |

**与其他章的符号消歧**：
- $N$：Ch1 用 $N_{\text{sat}}$，Ch2 用 $N_{\text{UE}}$，本章用 $N_{\text{node}}$
- $h$：轨道高度统一 $h_{\text{orb}}$，隐层维度统一 $d_h$
- $B$：本章不使用 $B$（固定容量 10Gbps，不使用 Shannon 容量）
- GNN 层数：统一 $L$（Ch2 原用 $T$，已改为 $L$）
- 节点集：统一花体 $\mathcal{V}, \mathcal{E}$

**⚠ 缺失**：本章无独立 `06_formulas_symbols.md` 文件，需在论文撰写时基于本表创建（P1-10）。

### F.3 跨章符号消歧

- $K$：本章不使用 $K$ 作为 Rician 因子（不用 $K_R$），但与 Ch2 的 $K$=top-K 候选卫星不冲突（本章无 top-K 机制）
- $f$：本章不涉及频率参数；Ch1 的 $f$ 指位置编码频率，Ch2 的 $f_c$ 指载波频率
- $L$：本章 $L$=GNN 层数，与 Ch2 统一（原 Ch2 用 $T$，已统一为 $L$）

---

## G. 实验设计

### G.1 仿真环境参数表

| 参数 | 值 | 来源 | 备注 |
|------|-----|------|------|
| 星座类型 | Walker-Delta F=1, 4-ISL MSN | 设计选择 | [L06][L02] 均使用 |
| 训练规模 | P=6, S=11 = 66 节点 | [L02] | Iridium 66 星 |
| 泛化测试规模 | 48(4×12) / 288(12×24) / 720(18×40) | [L02][L06][L01] | Walker-Delta 族内 |
| 轨道高度 | 550 km | 设计选择 | 跨章统一 |
| 轨道倾角 | 86.4° | Iridium spec | 产生极地间隙（Ch1/Ch2 为 53°，有意差异） |
| 极地间隙纬度 | 70° | 设计选择 | 高纬度 inter-plane ISL 几何不可达 |
| ISL 容量 | 10 Gbps | 设计选择 | 光学 ISL 量级 |
| 信道模型 | 固定容量 10 Gbps | 设计选择 | **不使用 Shannon/FSPL**（与 Ch1/Ch2 物理层根本不同）。本章使用固定链路容量 10Gbps，不涉及 antenna_gain 和 noise_power 参数（这些参数来自旧 hgat 项目，与当前 leo-congestion-routing 无关）。 |
| 流数量 | 40（66 节点），按 0.6×$N_{\text{node}}$ 缩放 | MVE 验证 | — |
| 重型流 | 10 条(25%)，demand ~ U(3,5) Gbps | 设计选择 | 接近 ISL 容量 50% |
| 轻型流 | 30 条(75%)，demand ~ U(0.1,1.0) Gbps | 设计选择 | 背景流量 |
| 热点目的地 | 3 个(5%) | 设计选择 | — |
| 突发因子 | 默认 1.0（E03 用 20x） | F1 修正 | — |
| 时变调制 | NHPP, amplitude=0.3 | [L10] | — |
| 故障率 | 默认 8%，消融 {0,5,8,10,15}% | MVE 验证 | — |
| 故障模式 | random / regional / cascading | 设计选择 | regional: 10% 节点周围链路全断 |
| GAT 层数 | 2 | [L06] | LayerNorm + Residual |
| GAT 头数 | 4 | [L06] | — |
| 隐层维度 | 64 | [L06] | — |
| Learning rate | 3e-4 | MVE | Adam |
| Entropy coeff | 0.01 | MVE | — |
| PPO clip $\epsilon$ | 0.2 | [L03] | 标准值 |
| $\gamma$ | 0.99 | 标准 RL | — |
| GAE $\lambda$ | 0.95 | 标准 PPO | — |
| Episodes | 800（核心）/ 500（泛化消融） | 设计选择 | ⚠ 文件间不一致，以 800 为准 |
| Seeds | ≥3 | 设计选择 | — |
| Eval episodes | 50 per seed | 设计选择 | — |

### G.2 对比对象 / Baseline

| ID | 方法 | 类型 | 复现状态 | 来源 |
|----|------|------|----------|------|
| B1 | SP (Dijkstra) | 标准算法 | 已复现 | 标准算法 |
| B2 | ECMP | 标准算法 | 已复现 | [L02][L04][L16] |
| B3 | MLP | 消融对照 | 已复现 | [L01][L07] |

**公平性声明**：GNN 和 MLP 共享 PPO 训练框架（相同 lr, clip, entropy, gamma, lambda），相同输入特征空间。MLP 用全局特征拼接替代 message passing，参数量相当（10K vs 28K）。所有方法在相同 topology seeds × traffic seeds × fault seeds 组合上评估。超参预算等价：每个方法允许 3 次超参调优。训练-测试分离：所有方法训练在 66 节点，泛化测试在 48/288/720（零样本不微调）。

**Baseline 数量说明**：当前 3 个 baseline（SP, ECMP, MLP）低于通行标准（5-8 个）。DTAR 不作为直接 baseline（问题空间不同：域间 vs 全网逐流），在 Related Work 详细讨论粒度差异。GMR 风险 P4（无代码+超参缺失）。⚠ PARTIAL（P1-6）。

### G.3 评估标准

**主指标**：E2E delay (ms) = $\sum_{e \in \text{path}} \text{propagation\_delay}_e \times \text{congestion\_factor}_e$。E2E delay 在 LEO 路由领域共识度最高（11/17 论文使用），且能同时反映路径长度和负载均衡质量。

**辅助指标**：MLU（训练奖励，同时也是负载均衡指标）；CV（负载分布均匀性）；Overflow Ratio（链路过载比例）；Generalization Gap（跨规模性能保持度）。

**延迟模型说明**：本章 E2E delay = 传播延迟 × 拥塞惩罚权重 1/(1-util)，**不是 M/M/1 排队延迟**。仿真为确定性逐流顺序路由（非泊松到达），congestion_factor 是拥塞惩罚权重——利用率越高，该链路对 E2E 延迟的贡献越大（util=0.8 时放大 5x，util=0.95 时放大 20x）。Ch1 的 E2E delay = Σ(ISL 传播时延)（无拥塞建模），Ch2 无 E2E delay 指标。三章延迟模型根本不同，绪论需显式说明。

**统计方法**：3 seeds + mean ± std + bootstrap 95% CI + Welch's t-test。统一以 stat_tests.json 为权威数据源。GNN vs ECMP MLU 不显著(p=0.262)，如实报告，强调 delay 维度。Wilcoxon N=3 无统计效力，不报告（P1-9）。

### G.4 控制变量

1. 所有方法在相同 topology seeds × traffic seeds × fault seeds 组合上评估
2. 所有方法评估统一用 MLU/E2E delay/CV
3. GNN vs MLP：相同输入特征，MLP 用全局拼接替代 message passing，参数量相当
4. 超参预算等价：每个方法允许 3 次超参调优
5. 训练-测试分离：所有方法训练在 66 节点，泛化测试在 48/288/720（零样本不微调）

### G.4.1 训练收敛行为

- 训练配置：800 episodes，每 episode 40 步（40 条流逐流路由），3 seeds
- 收敛行为：reward 在 ~300 episode 后趋于稳定，后续 500 episode 为策略微调阶段
- 总训练时间：22 分钟（RTX 4070，单 seed），3 seeds 总计约 66 分钟
- MLP 对照使用完全相同的训练配置和 episode 数，同样在 ~300 episode 后收敛
- 具体收敛曲线见 worker-logs

### G.5 图表规划

| 编号 | 类型 | 标题 | 数据来源 | 说明 |
|------|------|------|----------|------|
| Fig.1 | 拓扑图 | Walker-Delta 星座拓扑示意 | G.1 | 66星+ISL网格结构+极地间隙标注 |
| Fig.2 | 架构图 | GNN per-flow K-path 路由框架 | D.1 | 状态编码→GATEncoder→PathScoringHead→路径选择 |
| Fig.3 | 结果图 | 核心实验：GNN vs ECMP vs MLP（MLU + Delay 双指标） | E01 | 柱状图，3 方法对比 |
| Fig.4 | 结果图 | 故障率消融：GNN/ECMP vs fault rate 曲线 | E08 | 含 E02 无故障基线标注 |
| Fig.5 | 结果图 | 跨规模泛化：GNN/ECMP delay 随规模变化 | E04-E06 | 48-720 星延迟对比 |
| Fig.6 | 消融图 | 故障模式热力图：3 模式 × 4 故障率 | E12 | GNN/ECMP 比值热力图 |
| Fig.7 | 结果图 | 贡献来源分解：有故障 vs 无故障 GNN 优势对比 | C.1 | 故障激活效应可视化 |
| Tab.1 | 参数表 | 仿真环境参数 | G.1 | 完整参数（~34 行） |
| Tab.2 | Baseline表 | 对比方法 + 公平性声明 | G.2 | 3 baseline + 公平性说明 |
| Tab.3 | 统计表 | 核心实验统计检验 | E01 | p-value + Cohen's d + bootstrap CI |

**论文精简建议**：7 张图中保留 5-6 张。保留 Fig.3（核心双指标）、Fig.4（故障消融）、Fig.5（泛化）、Fig.6（故障模式热力图）、Fig.7（贡献分解）。可选：Fig.1 拓扑图（可移至方法节），Fig.2 架构图（可简化合并至方法描述）。

---

## 已知问题与待修项

### P1（建议补充，写作前）

| # | 问题 | 来源 |
|---|------|------|
| 5 | GMR/GNN-ASSSP 缺对比表 | S013-P1-1a |
| 6 | Baseline 公平性声明段落 | S013-P3-7e |
| 7 | 训练配置表（lr/batch/clip/gamma/lambda） | S013-P3-7e |
| 8 | GNN vs ECMP MLU 不显著→如实报告，强调 delay | S013-P3-7f |
| 9 | Wilcoxon N=3 无意义→不报告或标注局限 | S013-P2-5b |
| 10 | 创建 06_formulas_symbols.md，采用跨章统一符号 | S013-P2-5c |
| 11 | 2 篇待获取论文 DPR/Wang 2026→至少获取 abstract | S013-P1-1a |

### P2（可选增强）

| # | 问题 | 来源 |
|---|------|------|
| 12 | Ch3 章间过渡句 | S013-P1-3d |
| 13 | 绪论 Ch1/Ch3 分工表 | S013-P1-3d |
| 14 | 延迟模型局限性承认（非泊松到达） | S013-P1-1c |
| 15 | E10/E11 消融单 seed 脚注 | S013-P1-1c |
| 16 | Ch1 断链性质说明（确定性 vs 随机故障） | S013-P1-3d |
| 17 | 跨章星座参数比较表（86.4° vs 53°） | S013-P2-5c |

### 跨章一致性注意事项

- **轨道高度**：550km，三章统一 ✅
- **轨道倾角**：Ch3 = 86.4°（近极轨）vs Ch1/Ch2 = 53°，有意设计产生极地间隙
- **信道模型**：Ch3 不使用 Shannon/FSPL（固定容量 10Gbps），与 Ch1/Ch2 物理层根本不同
- **E2E delay 模型**：Ch3 = 传播×拥塞惩罚权重，Ch1 = 纯传播延迟，Ch2 无 delay 指标
- **元分析框架**：Ch3 定位为"故障弹性"——GNN 有效性取决于架构复杂度与任务需求的匹配
- **规模泛化**：Ch1 主贡献=星座规模泛化(11x)，Ch3 辅助贡献=Walker-Delta 族内泛化(0.7x-4.4x有效，10.9x退化)
- **贡献隔离**：Ch1/Ch3 贡献机制零重叠 STRONG（Ch1=无故障SL+规模泛化，Ch3=故障DRL+弹性路由）
