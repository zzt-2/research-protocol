# S003 跨领域理论文献 + GNN scaling 叙事

> 2026-05-25 | Phase 1 | 进行中
> 文件名: S003-conversation3-theory-literature.md

## 目标

确认 size generalization 理论基础 + "GNN 在大规模才有效"叙事有文献支撑 + DRL 统计报告标准合规

## 记录

### 已有理论基础 (进入本轮前)

| 文献 | 核心结论 | 章节 |
|------|----------|------|
| Wu et al. 2022 | mean aggregator 跨规模泛化条件 | Ch2 §3.2 |
| Garcia Camargo et al. 2025 | 稀疏随机几何图可迁移性证明 | Ch2 §3.2 |
| T01 (ICML 2024) | 解耦表示学习提升跨规模泛化 | Ch1 §3.2 |
| T02 (NeurIPS 2025) | 统一理论框架（网络-目标函数对齐） | Ch1 §3.2 |
| Size Transferability (arXiv 2026) | Graph Transformer + 卷积 PE 迁移界 | Ch1 §4.2 |

### 已有经验证据

| 来源 | 结论 | 阈值 |
|------|------|------|
| Shen et al. 2019 (IGCNet) | 无线功率控制，MLP 大规模退化 | N>? |
| Lee et al. 2023 | 多智能体防御，N>40 MLP 劣于随机 | N>40 |
| 本实验 Ch1 | 路由 66-200→720 星 91.7% 保留 | 11x |
| 本实验 Ch2 | 切换 20UE GNN≈MLP, 100UE GNN+34% | N>20-30 |

### 子 agent 结果

#### 3a: Size Generalization 理论文献 (完成)

**新增 11 篇理论论文**（2024-2026），按重要性排序：

| # | 论文 | 会议 | 核心结论 | Walker-Delta 适用性 |
|---|------|------|----------|-------------------|
| N2 | Manifold Perspective (Wang, Cervino et al.) | ICML 2025 | GNN 泛化界由流形上的谱连续常数决定 | **高** — 卫星在球面 S² 采样 |
| N4 | Robust to Model Mismatch | AAAI 2025 | 泛化差距随节点数增加而减小，随流形维度增加而增大 | **高** — d=2 最优 |
| N7 | Topology-Aware PAC-Bayesian (GCN) | arXiv 2026 | 明确纳入图拓扑的 PAC-Bayes 界，规则图界更紧 | **高** — 规则图谱结构可预测 |
| N1 | Survey on GNN Generalization Theory | arXiv 2025 | 统一 PAC-Bayes/graphon/谱界框架 | 参考文档 |
| N3 | Generalization of Geometric GNNs | arXiv 2024 | 几何图上 GNN 到流形极限的非渐近收敛 | **高** |
| N5 | MPNNs on Mixture of Graphons | SIAM 2024 | 混合 graphon 下 MPNN 泛化界 | **中** — 规则网格收敛到 graphon |
| N6 | Scale Invariance of GNNs | arXiv 2024 | 尺度不变消息传递的形式化保证 | **中** |
| N8 | Compositional PAC-Bayes | NeurIPS 2024 | 持久同调与 GNN 泛化界 | **中** |
| N9 | Why Does Your GNN Fail? | arXiv 2025 | 精确泛化误差：仅特征-结构对齐有效 | **重要限制** |
| N11 | OOD Size Generalization (spectral) | OpenReview | 谱相似性提供 OOD 尺寸泛化保证 | **高** |

**四大充分条件族**：

| 条件族 | 核心机制 | Walker-Delta 满足情况 |
|--------|---------|---------------------|
| A: 局部结构不变性 | k-hop ego-network 分布跨规模相似 | ✅ 恒定度数4，局部结构完全相同 |
| B: Graphon 收敛 | 图序列收敛到同一 graphon 极限 | ✅ 规则球面网格收敛到连续极限 |
| C: 谱/流形相似性 | 流形采样图的谱分解收敛 | ✅ 2D 球面 S²，低维最优 |
| D: 架构-任务对齐 | GNN 结构与目标函数分解方式匹配 | ⚠️ 任务相关，需具体验证 |

**Walker-Delta 评估**：Agent 原文 "arguably the most favorable graph family in the entire size generalization theory landscape"。恒定度数4 + 2D球面流形 + 规则网格 = 四族条件近乎全覆盖。唯一不确定项是 D（特征-结构对齐），取决于具体任务。

**已知理论限制**：
1. 局部结构不匹配会破坏泛化（Yehudai ICML 2021）— Walker-Delta 不受影响
2. Over-squashing：信息从指数增长邻域压缩到固定向量 — 规则图 k² 增长，浅层可控
3. 特征-结构不对齐会引入惩罚项（N9）— 需要任务级验证
4. Over-smoothing 深度限制：规则图上收敛更快 — 深度约束，非规模约束
5. **无已知不可能性定理适用于规则图**

#### 3b: GNN Scaling Behavior 经验证据 (完成)

**新增关键经验论文**：

| 论文 | 会议 | 领域 | 关键发现 |
|------|------|------|---------|
| Huang 2025 | COLT (PMLR) | 节点分类 | GNN 相对 MLP 优势量化为 D^(q-2) 倍（D=度数），随度数增长 |
| Shen 2021 | IEEE JSAC | 无线资源分配 | GNN K=10→K=100+ 泛化成功，MLP 在 K>20-30 退化 |
| Eisen & Ribeiro 2020 | IEEE TSP | 无线资源分配 | REGNN 排列等变性支持跨规模，MLP 每次需重训 |
| Yehudai 2021 | ICML | 图级任务 | 局部结构保持时 GNN 跨规模泛化，MLP 不能 |

**交叉点综合**：

| 领域 | 交叉点 | 说明 |
|------|--------|------|
| 无线功率控制 (Shen) | K~20-30 | MLP 和速率退化 15-30% |
| 多智能体防御 (Lee) | N>40 | MLP 劣于随机 |
| 本论文 Ch1 路由 | ~200 星 | 规则拓扑延迟退让 MLP 空间 |
| 本论文 Ch2 切换 | ~50-100 UE | 排列等变性成为关键 |
| 节点分类 (NeurIPS 2023) | 取决于 SNR+同质性 | 非纯规模阈值 |

**反例**（重要）：
1. "Revisiting Necessity of Graph Learning" (2024→2026 Neural Processing Letters)：精调 MLP 在 5/7 标准基准上优于 GNN — 但这是小规模节点分类（Cora/Citeseer），特征丰富，与卫星网络场景根本不同
2. "Locality Radius Framework" (2025)：局部邻域信息噪声大时图结构反而有害 — 卫星拓扑结构直接决定任务（路由/切换/卸载），结构信息可靠

**叙事支撑评级：MODERATE-TO-STRONG**
- 无线网络资源分配领域（Shen, Eisen）与卫星领域最直接类比，支撑强
- 理论量化（Huang 2025 COLT：优势随度数 D 增长）提供形式化基础
- 反例全部来自小规模特征丰富节点分类，不构成对本论文的威胁

#### 3c: DRL 统计报告标准 (完成)

**关键标准**：

| 来源 | 年份 | 推荐 | 权威级别 |
|------|------|------|---------|
| Henderson et al. "Deep RL That Matters" | 2018 AAAI | 5-10+ seeds; CI; Welch's t-test | 高引用奠基论文 |
| Colas et al. "How Many Random Seeds?" | 2018 | 功效分析定种子数；20-100+ seeds | 社区参考标准 |
| Agarwal et al. RLiable | 2021 NeurIPS Outstanding | IQM + 分层 bootstrap CI；≥10 runs | NeurIPS 杰出论文 |
| JMLR Empirical Design in RL | 2024 | 5-10 basic, 15-20+ for publications | JMLR 同行评审 |
| NeurIPS Paper Checklist | 2024 | 误差棒/CI/显著性检验必选 | 会议要求 |

**我们的做法 vs 标准**：

| 维度 | 我们 | 社区标准 | 差距 |
|------|------|---------|------|
| Seed 数 | 3 | ≥5 最低, 10+ 推荐 | **显著** |
| 描述统计 | mean±std | 可接受；IQM 更好 | 轻微 |
| 置信区间 | 无 | Bootstrap 95% CI | **中等** |
| 统计检验 | 无 | Welch's t 或 Mann-Whitney U | **中等** |

**领域现状**：IEEE 通信 DRL 论文通常用 3-5 seeds + mean±std，这是通行做法但被承认为弱点。

**可执行建议**（按性价比排序）：

| 优先级 | 建议 | 工作量 | 影响 |
|--------|------|--------|------|
| R1 **高** | 加 bootstrap 95% CI | 低（后处理） | 显著提升统计严谨性 |
| R2 **高** | 加 Welch's t-test 主对比 | 低（后处理） | 主声称有 p-value 支撑 |
| R3 **中** | 关键实验增到 5 seeds | 高（重训） | 最大改进但需 GPU 时间 |
| R4 **低** | 方法论段落明确声明 | 低 | 透明度提升 |

### 3d: 跨章 GNN 叙事可防御性评估

#### 核心评估框架

本论文三章均使用 GNN 作为核心表示学习方法，但 GNN 的角色和优势来源不同：

| 章 | GNN 角色 | 优势来源 | 理论支撑 | 经验支撑 |
|----|---------|---------|---------|---------|
| **Ch1 路由** | 状态编码器 + 跨规模部署 | Size generalization（规则图结构） | **极强**（4族条件全覆盖） | **强**（91.7% 保留，11x） |
| **Ch2 切换** | 状态编码器 + 可变规模输入 | 排列等变性 + size generalization | **中-强**（排列等变性 + 无线领域经验） | **强**（GNN +34% over MLP at 100UE） |
| **Ch3 卸载** | 异构图注意力编码器 | 类型感知消息传递 | **中**（MVE 验证，理论空白较大） | **弱-中**（同规模有效，零样本失败） |

#### 跨章统一叙事建议

**不建议**使用简单的"GNN 在大规模才有效"作为统一叙事。应采用分层叙事：

**统一叙事框架：GNN 在卫星网络中的三种优势机制**

1. **规模不变性 (Scale Invariance)**：GNN 的 message-passing 在局部邻域操作，与图全局规模无关。Walker-Delta 星座的恒定度数结构使得训练和推理的局部邻域完全一致 → Ch1 路由的 size generalization 有最强理论支撑
2. **排列等变性 (Permutation Equivariance)**：GNN 参数在节点间共享，自然支持可变数量的输入。当 UE 数量从 20 增至 100 时，GNN 无需改变架构 → Ch2 切换的跨 UE 规模泛化
3. **结构类型感知 (Structural Type-Awareness)**：异构图注意力通过类型特定投影捕获不同节点类型的能力差异 → Ch3 卸载的同规模优势

**关键边界条件**（必须在论文中讨论）：
- Ch3 零样本泛化失败（D020）表明：类型感知注意力在跨规模时方差过高（std≈100 vs GCN<1），简单聚合器（GCN mean）的泛化性反而更好
- 这与理论一致：N9 (arXiv 2025) 证明特征-结构不对齐会引入惩罚项，HGAT attention 在大图上的高方差可视为对齐失配
- 结论：GNN 跨规模泛化不是架构无关的，简单聚合器（mean/sum）比复杂注意力机制泛化性更强

#### 叙事可防御性评估总结

| 叙事声称 | 可防御性 | 关键支撑 | 需注意 |
|---------|---------|---------|--------|
| Walker-Delta 有利 size gen | **极强** | 4族条件全覆盖，11篇理论论文 | 讨论特征-结构对齐的不确定性 |
| GNN > MLP at scale | **中-强** | 无线领域多篇经验 + Huang COLT 量化 | 反例存在但领域不同 |
| GNN 排列等变性支持跨规模 | **强** | Eisen & Ribeiro 理论 + 本实验验证 | 二部图度数变化需讨论 |
| HGAT 类型感知优于同构 | **弱-中** | MVE 验证 + 同规模训练稳定性 | 零样本失败必须正视 |
| 3 seeds + mean±std 统计合规 | **弱** | 低于所有 ML 标准，IEEE 通行 | 必须加 CI + t-test |

#### 新增文献引用建议

**必须引用**（理论支撑核心）：
1. Wang et al. ICML 2025 (Manifold Perspective) — Walker-Delta 流形论证
2. Huang et al. COLT 2025 (GNN vs MLP 量化) — 优势随度数增长
3. Yehudai et al. ICML 2021 (Local Structures) — 局部结构保持条件

**建议引用**（加强论证）：
4. Shen et al. JSAC 2021 (Scalable Radio Resource) — 无线领域 GNN scaling 先例
5. AAAI 2025 (Robust to Model Mismatch) — 低维流形优势
6. arXiv 2026 (Topology-Aware PAC-Bayesian) — 规则图更紧的界

**统计方法论引用**：
7. Henderson et al. AAAI 2018 (Deep RL That Matters)
8. Agarwal et al. NeurIPS 2021 (RLiable)

## 决策引用

- 无

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

### 对话4 (Ch1 内部修复) 可直接使用

1. Ch1 paper-materials 可加入流形理论论证（ICML 2025 + AAAI 2025）
2. 贡献定位修正时引用 Huang COLT 2025 量化 GNN 优势
3. 统计部分加 bootstrap CI + t-test

### 对话6 (跨章整合) 可直接使用

1. 三种 GNN 优势机制框架（规模不变/排列等变/类型感知）
2. Ch3 零样本失败的统一解释（attention 方差 + N9 理论）
3. 符号统一中的 GNN 架构对比表

### 统计改进优先级

1. **立即执行**（零 GPU）：三章结果加 bootstrap 95% CI + Welch's t-test
2. **建议执行**（需 GPU）：关键实验增到 5 seeds
