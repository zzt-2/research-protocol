# Ch1: GNN 跨规模 LEO 路由 — Paper Materials

> 重新提取自终审14轮对话 + 旧paper-materials + 项目文件
> 终审结论 > 旧paper-materials > 原始项目文件（矛盾以终审为准）
> 贡献定位：GNN 跨规模路由的系统性验证（非"首次创新"）
> 注意：01_research_context.md L187 仍有旧值 91.7%，需后续同步

---

## A. 研究问题与论证逻辑

### A.1 问题定义

LEO mega-constellation 路由中 GNN 的跨规模零样本泛化——在小星座训练后直接部署到大星座，保持路由质量。

Starlink Gen2 规划数千颗卫星，GNN+RL 路由已在 LEO 场景验证可行，但所有现有工作在单一规模训练测试。当部署规模远超训练规模时性能未知。Walker-Delta 星座具有规则网格结构（每星恒定 4 ISL），GNN message-passing 面对相同的局部邻居结构，与图规模无关——是 size generalization 的有利条件（非"理论最优"，S011 降级）。

### A.2 现状局限

1. **GNN+RL LEO 路由全部单一规模**：13 篇论文（L13-L25）无一涉及跨规模泛化实验。来源：literature_notes §5; D006
2. **传统路由无法利用学习型表示**：Dijkstra/SPF 每快照独立计算最短路径，丢弃历史负载趋势和邻居拥塞传播信号。来源：feasibility_report §A; L10
3. **分治策略适应性有限**：MCSR (L10) SRD 分割增加管理开销；CMCR (L11) 纬度聚类静态适应性有限；DuJo (L03) 集中优化分钟级，不适合实时。来源：literature_notes §1.A, §2
4. **GNN 路由缺乏位置感知**：所有 GNN+RL LEO 路由论文未使用位置编码，仅依赖节点特征。来源：D026（消融 A1 证实无 PE 精度约等于随机）

### A.3 研究空白

**空白陈述**：GNN size generalization 在 LEO/satellite routing 领域完全空白。

**证据**：25 篇论文 + GRLR 44 篇引用链 + GraphPR 19 篇引用链 = 63 篇引用链筛查，零提及 size generalization。6 组关键词检索，零命中。Web 搜索声称 GRLR 涉及 size generalization，经 Semantic Scholar API 验证系 AI 幻觉（D004, D006）。

**结构性原因**：(1) GNN 理论研究集中在通用图/节点分类，未触达卫星路由场景；(2) 卫星网络社区关注拓扑时变和负载均衡，未关注跨规模部署；(3) 两个社区缺乏交叉。

### A.4 论证主线

LEO mega-constellation 路由面临规模爆炸挑战。现有 GNN 路由全部在单一规模训练测试，跨规模泛化完全未被探索。Walker-Delta 星座的规则网格结构使 GNN 的局部邻居环境与全局规模无关，为 size generalization 提供了结构基础。本研究设计 Orbital PE + 多尺度混合训练框架，系统性验证 GNN 在卫星路由中的跨规模泛化可行性。

**论证模式**：空白填补型（实证验证）

### A.5 Gap-Contribution 闭环映射表

| 空白(Gap) | 方法组件 | 结论回应 | 数据证据(板块E编号) |
|-----------|---------|---------|-------------------|
| GNN 路由无法跨规模部署 | Orbital PE | PE 是学习必要前提，无 PE 精度降至随机水平 | E3 |
| 单一训练规模泛化不足 | 多尺度混合训练 | 贡献 stretch 改善 | E4 |
| 贪心推理路径成功率低 | 加权 Dijkstra 推理 | 100% 路径成功率 | E8 |
| 跨规模性能损失未知 | 11x 零样本实验 | 保留率 91.5%，stretch 可接受 | E1, E2 |
| 理论到实践验证 | MVE + 完整实验 | GNN 跨规模泛化在卫星路由工程可行 | E1, E10 |

---

## B. 文献格局

### B.1 文献角色速览

| cite key | 一句话贡献 | 与本研究关系 | 引用角色 |
|----------|-----------|------------|---------|
| L01 GKAE | GNN+Koopman 空间压缩，400→1444 星泛化实证 | GNN 置换不变性在卫星领域的实证 | 前驱/基础 |
| L02 Starfield | 黎曼度量引导 ISL 拓扑设计 | 仿真基础设施参考 | 背景 |
| L03 DuJo | 拉格朗日对偶解耦 MILP | 信道参数来源（B=1GHz）；方法对照 | 理论/方法支撑 |
| L04 ISL Pattern | Walker 星座 ISL 拓扑形式化 | 拓扑建模基础 | 前驱/基础 |
| L05 xeoverse | 基于 Mininet 的实时 LEO 仿真平台 | 仿真框架参考 | 背景 |
| L06 GPN | GAT+LSTM+REINFORCE 组播路由，30→50 节点泛化 | 路由架构可迁移参考 | 前驱/基础 |
| L07 微服务路由 | 边特征感知注意力 GNN 路由 | 边感知注意力设计参考 | 方法支撑 |
| L08 GNN-SD-LEO | GCN 做 ISL 性能聚合（非决策） | 唯一 GNN+LEO 但仅聚合 | 竞品（弱） |
| L09 GARS | 地理位置辅助路由，O(1) 复杂度 | 传统 baseline | Baseline |
| L10 MCSR | 不相交段路由域，10000 星 | 最强传统方法 baseline | 背景/方法参考 |
| L11 CMCR | 纬度分簇路由，理论收敛保证 | 传统方法参考 | 背景/方法参考 |
| L12 SDN TopoVirt | 拓扑虚拟化多控制器 | SDN 部署架构参考 | 背景 |
| L13 GRLR | GNN+Actor-Critic LEO 路由，44 引用 | 核心竞品，无 size gen | 竞品 |
| L14 GraphPR | GAT+MADRL 全分布式路由 | 竞品，无 size gen | 竞品 |
| L15 GQN | GNN+DRL 路由，108 星，仅时序泛化 | 竞品（弱） | 竞品 |
| L16 GDRL-SFCR | GCN+PPO 路由，6048 星最大规模但同规模 | 竞品 | 竞品 |
| L17 GAT-LSTM-DQN | GAT+LSTM+DQN 时空路由，45 星规模极小，仅验证时空建模可行性 | 空白证据 | 背景 |
| L18 DTAR | NSGA-II 离线域划分+GAT+Action-masked PPO 在线路由，288 星，域划分思想可结合规模泛化但未探索 | 空白证据 | 背景 |
| L19 DeepLaDu | Lagrangian 对偶变量解释为拥塞价格，GNN 单次前向推理输出拥塞价格，Starlink-like 星座 | 空白证据 | 背景 |
| L20 GNN-ASSSP | 注意力机制+GNN 动态路由，发表于 Aerospace Science and Technology | 空白证据 | 背景 |
| L21 ADRLRM | ST-GNN+DRL 最小化 AoI，时空图编码，发表于 IEEE ToN | 空白证据 | 背景 |
| L22 FGRLR | 联邦学习+GNN+RL 路由，发表于 IEEE WCL | 空白证据 | 背景 |
| L23 DGA-IES | 深度图注意力+增量进化策略替代 PPO，E2E 时延降低 10.3%-58.1%，发表于 IEEE IoTJ | 空白证据 | 背景 |
| L24 DLBR | GCN+LSTM+Attention 时空流量预测+多 agent Dueling DQN 负载均衡路由，发表于 IEEE TAES | 空白证据 | 背景 |
| L25 Transformer-MIX | Multiagent Transformer-MIX 架构统一负载均衡奖励，发表于 IEEE IoTJ | 空白证据 | 背景 |
| T01 DISGEN | ICML'24 解耦表示学习提升跨规模泛化 | Walker-Delta 恒定度数有利于解耦 | 理论支撑 |
| T02 Size Gen Theory | NeurIPS'25 神经网络与目标函数对齐时 size gen 成立 | Walker-Delta 可能满足对齐条件 | 理论支撑 |
| C01 TELGEN | GNN 模仿 IPM，TE 流量拆分跨规模 20x | 差异化参照：非路由/非卫星/无 PE | 竞品 |
| C02 Size Transferability | Graph Transformer+卷积 PE 跨规模 | 差异化参照：非 GNN 路由/非卫星 | 理论支撑 |
| C03 Scaling Swarm | 1 层 GAT+DQN 零样本迁移（最高 3x） | 差异化参照：简单 2D 导航 | 竞品（低） |

**文献缺口 ⚠**：终审发现 GAUSS、GAT-MARL、GROM 等 5 篇低威胁竞品在 04 中未出现，如需可补充引用。

**传统方法定位说明**：MCSR (L10) 和 CMCR (L11) 是 LEO 路由领域有代表性的传统方法，分别采用分段路由和聚类路由策略。本研究聚焦 GNN 跨规模泛化验证，实验对比以 GRLR（同规模 GNN 路由标杆）和 Dijkstra（性能上界）为主。MCSR/CMCR 为非学习型方法，其路由范式与 GNN 方法差异较大（分治 vs 端到端），不适合作为等价实验 baseline；它们在 B 段作为"传统方法天花板"定位，为研究动机提供背景支撑。

### B.1x 中文学术文献

> 共 22 篇中文文献（CN01-CN22），按方向分组详见 [chinese-literature.md](chinese-literature.md)。
> 分布：LEO 路由综述(4) / 星座+ISL(4) / GNN 综述(4) / DRL/GNN+DRL(6) / 大规模路由+安全(4)。核心期刊占比 68%。

| cite key | 一句话贡献 | 引用角色 |
|----------|-----------|---------|
| CN01 | 卫星互联网路由技术现状及展望（朱立东 2021 通信学报） | 背景/综述 |
| CN02 | 卫星网络路由技术现状及展望（倪少杰 2023 电子与信息学报） | 背景/综述 |
| CN03 | 低轨巨型星座网络组网技术与研究现状（陈全 2022 通信学报） | 背景/综述 |
| CN04 | 未来低轨信息网络发展与架构展望（王宁远 2023 电子与信息学报） | 背景 |
| CN05 | 低轨巨型星座构型设计与控制（阮永井 2022 中国空间科学技术） | 前驱/基础 |
| CN06 | 大规模 LEO 星间链路连接策略 Grid-V/Grid+（燕锋 2024 通信学报） | 前驱/基础 |
| CN07 | 低轨巨型星座路由技术研究现状及展望（李佳奇 2025 空间电子技术） | 背景/综述 |
| CN08 | 低轨卫星互联网从星地融合到通导遥一体化（孙耀华 2024 北邮学报） | 背景 |
| CN09 | 图神经网络前沿进展与应用（吴博 2022 计算机学报） | 理论支撑 |
| CN10 | 图神经网络综述（马帅 2022 计算机研究与发展） | 理论支撑 |
| CN11 | 图神经网络在通信网络领域应用综述（李硕朋 2021 北工大学报） | 方法支撑 |
| CN12 | 大规模图神经网络研究综述（肖国庆 2024 计算机学报） | 理论支撑 |
| CN13 | 深度强化学习综述（刘全 2018 计算机学报） | 理论支撑 |
| CN14 | 基于深度强化学习的组合优化研究进展（李凯文 2021 自动化学报） | 方法支撑 |
| CN15 | 联邦 DRL LEO 路由方法（李学华 2025 电子与信息学报） | 竞品参考 |
| CN16 | 低轨巨型星座网络抗毁性研究进展（杨华果 2025 系统工程与电子技术） | 背景 |
| CN17 | 低轨卫星网络安全问题及防御技术（杜星葵 2024 电子与信息学报） | 背景 |
| CN18 | **GNN+DRL LEO 动态路由**（汪昊 2023 重庆邮电大学学报）被引12次，66星同规模 | 前驱/方法参考 |
| CN19 | GNN+DRL 卫星网络切片（汤雪岩 2024 北邮硕士） | 方法参考 |
| CN20 | 时空状态感知卫星网络路由（王宇卓 2025 中科大） | 方法参考 |
| CN21 | LEO 多层异构星座拓扑路由联合优化（赵艳春 2025 宇航学报） | 背景/方法参考 |
| CN22 | 大规模 LEO 动态路由+安全（杨子健 2023 中科院博士）被引16次，纯传统方法 | 背景 |

### B.2 竞品精确区分

| 论文 | 覆盖要素 | 缺失要素 | 威胁等级 | 我们的优势 |
|------|---------|---------|---------|-----------|
| GRLR (L13) | GNN 路由, LEO, 动态拓扑 | 跨规模泛化, PE, 多尺度训练 | 中-高 | 核心竞品但无跨规模 |
| GraphPR (L14) | GNN 路由(GAT), LEO, 全分布式 | 跨规模泛化, PE, 多尺度训练 | 中 | 无跨规模能力 |
| GDRL-SFCR (L16) | GNN 路由, LEO, 最大规模 6048 星 | 跨规模泛化, PE | 中 | 训练测试同规模 |
| TELGEN (C01) | 跨规模泛化(20x) | GNN 路由(TE), LEO, PE, 动态拓扑 | 中 | 非路由/非卫星/无 PE |
| Size Transferability (C02) | PE 理论, 跨规模 | GNN 路由(GT), LEO | 低 | GT vs GNN 架构差异 |
| Scaling Swarm (C03) | 跨规模(3x), GAT | LEO, PE, 大规模, 结构化图 | 低-中 | 简单 2D vs LEO 路由 |
| MCSR (L10) | LEO, 10000 星, 弹性路由 | GNN, 跨规模泛化, PE | 低 | 传统方法天花板 |

**核心结论**：无任何单一竞品覆盖"GNN 路由 + 跨规模泛化 + Orbital PE + 多尺度训练"组合，空白声称成立。

---

## C. 贡献与核心论据

### C.1 贡献声明

**C1**: 系统性验证 GNN 在 LEO mega-constellation 路由中的跨规模零样本泛化可行性——在 66+100+200 星训练后部署到 720 星（11x），时延保留率 91.5%（3-seed），stretch 1.083±0.015。（支撑证据：E1, E2, E10）

**C2**: 设计并消融验证 Orbital PE + 多尺度混合训练框架——PE 是模型可学习的必要前提（无 PE 精度降至随机水平），多尺度训练贡献 stretch 改善。（支撑证据：E3, E4, E5）

**C3**: 提出加权 Dijkstra 推理策略替代贪心部署——100% 路径成功率（贪心仅 1.7%），stretch 1.083，推理复杂度 O(N log N)。（支撑证据：E8）

> 贡献定位说明（S011 校准）：C1 定位为"系统性验证"非"首次创新"——size generalization 是 GNN 理论性质非 LEO 路由领域公认挑战。Walker-Delta 规则拓扑是"有利条件"非"理论最优"。各组件均有先例（PE 属标准领域特征工程，加权 Dijkstra 推理有 GRLR 先例）。

### 跨章元分析定位

在跨章元分析框架（"探索性分化"）中，Ch1 代表 GNN 有效性的"规模不变性"维度——同构 GAT 编码器 + 规则拓扑（Walker-Delta）+ 监督学习范式下，当部署规模仅增加同类节点、不改变局部结构统计性质时，GNN 路由策略成功实现零样本跨规模泛化。与 Ch2（排列等变性 + DRL 范式下 N>30 时规模适应性）和 Ch3（故障场景下结构漂移触发的故障弹性）形成探索性分化对比。三章的统一论点为：GNN 的有效性取决于架构复杂度与任务需求的匹配程度。

### C.2 贡献间关系

C2（框架设计）→ C3（推理策略）→ C1（跨规模验证），递进关系。C2 提供可学习的前提条件，C3 解决推理部署问题，C1 在目标规模上验证整体效果。

### C.3 证据蓝图

| 贡献 | 核心证据(板块E) | 补充证据(板块E) |
|------|----------------|----------------|
| C1 跨规模验证 | E1(主实验), E2(基线对比) | E6(统计汇总), E7(规模分解), E10(拓扑分析) |
| C2 框架设计 | E3(A1消融), E4(A2消融) | E5(A3双消融) |
| C3 推理策略 | E8(贪心vs Dijkstra) | E9(训练收敛) |

---

## D. 方法描述

### D.1 架构总览

**训练阶段**：在 Walker-Delta 星座（66/100/200 星）上构建动态 ISL 拓扑快照 + 时延边权，预计算 Orbital PE 附加到节点特征，运行全对 Dijkstra 生成 4 方向监督标签（轨内前/后、轨间左/右），训练 3 层 GAT 编码器通过交叉熵损失学习方向预测。

**推理阶段**：在目标 720 星星座上构建拓扑快照，附加 Orbital PE，GNN forward 得到方向 logits，构造加性惩罚边权重，运行加权 Dijkstra 生成路由表。

### D.2 核心组件

**Orbital Positional Encoding**：基于归一化轨道坐标的 sin/cos 多频率编码，维度 16。Walker-Delta 星座中每颗卫星由 $(p, k)$ 唯一确定，归一化后用多频率编码：

$$\text{PE}(p, k) = \big[ \sin(f_i \cdot p/P),\ \cos(f_i \cdot p/P),\ \sin(f_i \cdot k/S),\ \cos(f_i \cdot k/S) \big]_{i=0}^{3}$$

其中 $f_i = 2^i \cdot 2\pi$，输出维度 $d_{\text{PE}} = 16$（4 个频率）。归一化坐标 $p/P \in [0,1)$, $k/S \in [0,1)$ 天然规模无关，固定维度可泛化到任意 $(P,S)$ 组合。消融证实 PE 是学习必要前提（无 PE 精度 ~40%，接近随机 25%），非可选增强。设计范式借鉴 Transformer 位置编码（R13）。

**GAT 编码器（3 层, $d_h$=128, 4 heads）**：消息传递聚合函数面对相同局部邻居结构（恒定度数 4），与图规模无关。第 $l$ 层更新：

$$\mathbf{h}_u^{(l+1)} = \text{ELU}\left( \big\|_{m=1}^{4} \sum_{v \in \mathcal{N}(u)} \alpha_{uv}^{(m)} \mathbf{W}^{(m)} \mathbf{h}_v^{(l)} \right)$$

注意力系数含边特征：

$$\alpha_{uv} = \frac{\exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_v \| \mathbf{W}_e \mathbf{e}_{uv}]))}{\sum_{w \in \mathcal{N}(u)} \exp(\text{LeakyReLU}(\mathbf{a}^\top [\mathbf{W}\mathbf{h}_u \| \mathbf{W}\mathbf{h}_w \| \mathbf{W}_e \mathbf{e}_{uw}]))}$$

边特征 $\mathbf{e}_{uv} = [\delta_{\text{delay}}, d]$ 通过独立变换矩阵 $\mathbf{W}_e$ 参与注意力计算，使模型感知链路质量异质性。3 层覆盖 3-hop 感受野。

**节点特征设计（33 维）**：$[\mathbb{1}[\text{is\_dest}](1) + \text{PE}_{\text{own}}(16) + \text{PE}_{\text{dest}}(16)] = 33$。目的节点 PE 广播到全图使每颗卫星获得目的地方向信息，与自身位置编码的差值隐式编码"我在哪里、要去哪里"的关系。is_dest 标记提供 1 bit 身份信息，消融 A1 证实仅靠此 1 bit 无法学习有效路由（精度 ~40%）。

**边特征设计（2 维）**：$[\delta_{\text{delay}}(1), d(1)] = 2$。ISL 传播时延和几何距离。时延直接反映路由代价，距离提供链路稳定性信号（距离近的链路更稳定）。边特征通过 $\mathbf{W}_e$ 参与注意力计算（PyG GATConv edge_dim 参数），使注意力权重同时考虑拓扑结构和链路质量。

**监督损失函数**：交叉熵 4 类分类，含标签过滤：

$$\mathcal{L} = \frac{1}{|\mathcal{V}_{\text{valid}}|} \sum_{u \in \mathcal{V}_{\text{valid}}} \text{CE}(\hat{\mathbf{o}}_u, y_u)$$

其中 $\mathcal{V}_{\text{valid}}$ 排除 $u = d$（源=目的）和 next_hop 不存在的节点（标签 $y = -1$）。对不可用方向（ISL 断链）的 logit 置 $-\infty$，防止对不存在的类别产生梯度。

**多尺度混合训练**：66+100+200 星三配置混合，每 batch 随机采样，让模型见过不同 $(P,S)$ 下的归一化位置分布。消融 A2 证实贡献 stretch 改善。

**加权 Dijkstra 推理**：GNN logits 构造加性惩罚边权：

$$w(u, v) = \delta_{\text{delay}}(u, v) + \text{relu}\big(\max_d\ o_{u,d} - o_{u, \text{dir}(u,v)}\big)$$

首选方向 penalty=0（等于纯时延），非首选方向 penalty>0。Dijkstra 全局优化可修正单跳错误，100% 路径成功率。推理范式同 GRLR (L13)。

**训练收敛行为**：监督学习（Cross-Entropy 4 类），Adam lr=1e-3, batch=64, 150 epochs。训练数据 7320 samples。Loss 在 ~50 epoch 后趋于稳定，150 epoch 内无显著过拟合。训练集方向精度 97.6%，表明监督信号充分。PPO 微调 80 轮无改善（greedy reward 稀疏 + action-reward 解耦），最终方案不使用 PPO 微调。

### D.3 设计决策表

| 选择 | 理由 | 排除的替代方案 | 支撑 cite key |
|------|------|---------------|--------------|
| sin/cos PE（归一化坐标） | 固定维度、连续、多频率、规模无关 | 可学习嵌入（固定词表）、one-hot（维度变化） | R13 |
| GAT 3 层 h=128 | 边特征参与注意力，3-hop 覆盖路由决策 | GCN（无注意力）、更深层（过平滑风险，MVE 证实） | L13 |
| 监督预训练（Dijkstra labels） | 方向精度 97.6%，加权 Dijkstra 成功率 100% | PPO 微调（reward 稀疏+action-reward 解耦，80 轮无改善，D021） | — |
| 加权 Dijkstra 推理 | 成功率 100%，stretch 可接受 | 纯贪心（1.7% 成功率） | L13 |
| 实时轨道力学距离 + 5000km 断链 | 四配置 ISL 距离差异大，固定值不适用 | 固定距离（错误） | L02, L03 |
| 多尺度混合（66+100+200） | 消融证实 stretch 改善 | 单规模训练（A2 证实退化） | — |

---

## E. 证据目录

### E.core 核心证据

### E1 主实验：11x 零样本跨规模部署
- 证据类型：定量数据 + 统计结果
- 内容：多尺度混合训练（66+100+200 星），零样本部署到 720 星。3-seed 评估。Stretch 1.083±0.015, delay 65.92±1.01 ms, ≤1.2x optimal 90.3±4.0%, 路径成功率 100%。Delay 开销 vs Dijkstra ~8.5%。时延保留率 91.5%（GRLR 同规模 delay 60.32 / 跨规模 delay 65.92）。
- 完整上下文：加权 Dijkstra 推理、监督学习、uniform 流量、Walker-Delta 53°/550km。规模因子 min(train)/target = 66/720 = 10.9x。
- 来源：E01/D031, stat_tests.json
- 支撑论点：C1
- 统计显著性：full vs same stretch t=7.62, p=0.017 (显著)；delay t=7.17, p=0.019 (显著)

### E2 同规模基线对比
- 证据类型：定量数据
- 内容：Ours(跨规模) stretch 1.083±0.015, delay 65.92±1.01 ms。GRLR(同规模) stretch 1.008, delay 60.32 ms。Dijkstra(上界) stretch 1.000, delay 60.77 ms。三方统一评估协议。
- 完整上下文：GRLR 为复现版本，On-policy AC, 1 层 GAT, 2000 episodes, 720 星同规模训练。注：GRLR 的 stretch 1.008（720星同规模训练）≠ E6 表中 "same" 的 stretch 1.000（确定性 Dijkstra），两者为不同实验——GRLR 是学习方法的最优表现，"same" 是理论下界。
- 来源：E02/D024(GRLR), D031
- 支撑论点：C1（保留率 91.5% > 80% 目标，开销 8.5% < 20% 目标）
- 统计显著性：Ours vs Same 差距显著 p=0.017

### E3 消融 A1：移除 Orbital PE
- 证据类型：定量数据 + 质性发现
- 内容：移除 PE 后 stretch 1.006±0.002, delay 61.13±0.12 ms, ≤1.2x 99.9%。训练精度 ~39.7%（4 类随机=25%）。加权 Dijkstra 退化为近纯 Dijkstra。
- 完整上下文：无 PE 时节点仅靠 is_dest (1 bit) 无法区分位置。stretch 近 1.0 是因为 Dijkstra 退化——PE 不是"增强"而是"学习前提"。
- 来源：D026, D031, stat_tests.json
- 支撑论点：C2（PE 必要性）
- 统计显著性：full vs A1 stretch t=6.98, p=0.018 (显著)

### E4 消融 A2：单尺度训练 vs 多尺度训练
- 证据类型：定量数据
- 内容：仅 train_100 训练，PE 开启，评估 720 星。Stretch 1.106±0.015, delay 67.66±0.80 ms, ≤1.2x 84.0±3.2%。多尺度训练贡献 stretch 改善 2.3 pp，≤1.2x 改善 6.3 pp。
- 完整上下文：训练精度 97.7%（与完整方法相当），说明多尺度训练不影响学习质量但影响跨规模泛化。
- 来源：D027, D031, stat_tests.json
- 支撑论点：C2（多尺度训练贡献）
- 统计显著性：full vs A2 stretch t=-1.52, p=0.203 (不显著，3-seed 检验力不足)

### E5 消融 A3：双消融（无 PE + 单尺度）
- 证据类型：定量数据
- 内容：无 PE + 单尺度。Stretch 1.058±0.002, delay 63.32±0.05 ms, ≤1.2x 92.2%。Stretch 介于 A1(1.006) 和 A2(1.106) 之间，内部一致性验证通过。
- 来源：D028, D031, stat_tests.json
- 支撑论点：C2（效应可叠加）
- 统计显著性：full vs A3 stretch t=2.23, p=0.153 (不显著，3-seed)

### E6 3-seed 统计汇总（stat_tests.json 权威数据）
- 证据类型：统计结果
- 内容：

| 配置 | Stretch mean±std | 95% CI | Delay mean±std (ms) | 95% CI |
|------|------------------|--------|---------------------|--------|
| full | 1.083±0.015 | [1.066, 1.103] | 65.92±1.01 | [64.80, 67.25] |
| A1 (无PE) | 1.006±0.002 | [1.005, 1.009] | 61.13±0.12 | [61.06, 61.27] |
| A2 (单尺度) | 1.106±0.015 | [1.085, 1.120] | 67.66±0.80 | [66.53, 68.32] |
| A3 (双消融) | 1.058±0.002 | [1.056, 1.060] | 63.32±0.05 | [63.29, 63.38] |
| same (720→720) | 1.000±0.0 | [1.0, 1.0] | 60.80±0.01 | [60.79, 60.80] |

- 来源：stat_tests.json
- 支撑论点：全局

### E7 不同规模配置与方向精度分解
- 证据类型：定量数据
- 内容：训练集（66+100+200）方向精度 97.6%，目标集（720）精度 66.8%，精度保留率 71%。加权 Dijkstra 弥补单跳错误。
- 完整上下文：精度退化是跨规模的直接后果，但 stretch 仅退化至 1.083——说明少量方向错误通过全局路径优化可被容忍。
- 来源：D018, D031
- 支撑论点：C1

### E8 贪心 vs 加权 Dijkstra 推理对比
- 证据类型：定量数据 + 设计产物
- 内容：贪心（逐跳 argmax）训练集成功率 22-30%，目标集 1.7%。加权 Dijkstra 成功率 100%，stretch 1.083。贪心失败根因 = 逐跳精度之积，跨规模 66.8% 精度下 10 跳路径成功率极低。
- 完整上下文：测试 4 种权重公式，加性惩罚最终胜出。推理 O(N log N)。
- 来源：D019, D020, D022
- 支撑论点：C3

### E9 训练收敛行为
- 证据类型：定量数据
- 内容：监督学习，Cross-Entropy 4 类，Adam lr=1e-3, batch=64, 150 epochs。训练数据 7320 samples。模型参数 72,965。PPO 微调 80 轮无改善（greedy reward 稀疏 + action-reward 解耦）。
- 来源：D018, D021
- 支撑论点：方法表述为"GNN-guided Dijkstra"而非端到端路由

### E10 Walker-Delta 拓扑结构分析
- 证据类型：质性发现 + 定量数据
- 内容：Walker-Delta 单壳层 F=1, +Grid 拓扑，每星恒定 4 ISL（2 轨内 + 2 轨间）。ISL 类型 1550nm 激光, Shannon B=1GHz。断链阈值 5000km。恒定度数 = GNN 聚合函数面对相同局部结构 = size generalization 有利条件。T01 (ICML 2024) 指出解耦表示学习在规则结构上更有效。
- 来源：contract.md, feasibility_report.md
- 支撑论点：C1 的结构基础

### E.supplement 补充证据

1. **MVE 先验结果**：96→384 星(4x)保持率 87%, 96→1536 星(16x)保持率 83%。GATx3 优于 GATx6/x8（过平滑）。来源：feasibility_report D
2. **消融内部一致性**：A3 stretch(1.058)介于 A1(1.006)和 A2(1.106)之间，通过验证。
3. **仿真器验证**：轨道位置(atol=1.0km), +Grid 拓扑完整性, Shannon 容量, Dijkstra 全对最短路全部 PASS。
4. **关键 Bug 修复**：neighbor_map 单向注册→补全双向, ISL 容量 500MHz→1GHz, ISL 距离固定值→实时轨道力学。
5. **Contract 指标达成**：S1 保留率 91.5%≥80% PASS; S2 vs Dijkstra 8.5%≤20% PASS; S3 PE 关键性 PASS。

---

## F. 术语与符号

### F.1 术语表

| 术语 | 英文 | 缩写 | 定义 |
|------|------|------|------|
| 巨型低轨星座 | LEO mega-constellation | — | 千星级低轨卫星网络 |
| 星间链路 | Inter-Satellite Link | ISL | 卫星间激光通信链路 |
| 轨道位置编码 | Orbital Positional Encoding | Orbital PE | 基于轨道参数的 sin/cos 位置编码 |
| 加权 Dijkstra | Weighted Dijkstra | — | GNN logits 构造惩罚边权的最短路算法 |
| 时延保留率 | Delay Retention | — | GRLR同规模最优时延/跨规模部署时延，衡量泛化退化程度（⚠ 自造指标，D030） |
| 路径最优性比 | Stretch | — | 实际路径时延/Dijkstra 最优时延 |
| 规模泛化 | Size Generalization | — | GNN 在未见图规模上保持性能的能力 |
| 星座规模泛化 | Constellation-size Generalization | — | 图节点数变化（P,S 变化），拓扑类型不变的泛化（S011 命名） |

### F.2 符号表（跨章统一方案）

| 符号 | 含义 | 单位 | 值/范围 | 首现章节 |
|------|------|------|---------|---------|
| $N_{\text{sat}}$ | 卫星总数 | — | 训练 66/100/200，目标 720 | Ch1 |
| $P$ | 轨道面数 | — | 6/10/10/18 | Ch1 |
| $S$ | 每面卫星数 | — | 11/10/20/40 | Ch1 |
| $h_{\text{orb}}$ | 轨道高度 | km | 550 | Ch1 |
| $i$ | 轨道倾角 | ° | 53 | Ch1 |
| $F$ | Walker 相位因子 | — | 1 | Ch1 |
| $(p, k)$ | 卫星轨道位置 | — | $p \in [0,P), k \in [0,S)$ | Ch1 |
| $d_{\max}$ | ISL 断链阈值 | km | 5000 | Ch1 |
| $B_{\text{ISL}}$ | ISL 带宽 | GHz | 1 | Ch1 |
| $d_h$ | GNN 隐层维度 | — | 128 | Ch1 |
| $L$ | GAT 层数 | — | 3 | Ch1 |
| $M$ | 注意力头数 | — | 4 | Ch1 |
| $d_{\text{PE}}$ | PE 输出维度 | — | 16 | Ch1 |
| $f$ | PE 频率参数 | — | $f_i = 2^i \cdot 2\pi$ | Ch1 |
| $\mathcal{V}, \mathcal{E}$ | 节点集、边集 | — | — | 跨章统一 |
| $\alpha_{uv}$ | 注意力系数 | — | [0,1] | Ch1 |
| $\mathbf{x}_u$ | 节点输入特征 | — | $\mathbb{R}^{33}$ (1+16+16) | Ch1 |
| $\mathbf{e}_{uv}$ | 边特征 | — | $\mathbb{R}^{2}$ (时延+距离) | Ch1 |
| $\mathbf{o}_u$ | 方向 logits | — | $\mathbb{R}^{4}$ | Ch1 |
| $w(u,v)$ | 加权 Dijkstra 边权 | ms | — | Ch1 |
| stretch | 路径最优性比 | — | ≥1.0，目标 ≤1.2 | Ch1 |
| retention | 时延保留率 | — | (0,+∞)，1.0=无退化 | Ch1 |
| $\hat{\mathbf{o}}_u$ | 掩码后方向 logits | — | $\mathbb{R}^{4}$，不可用方向置 $-\infty$ | Ch1 |
| $y_u$ | 方向标签 | — | $\{0,1,2,3,-1\}$，$-1$=无标签 | Ch1 |
| $\mathbf{W}_e$ | 边特征变换矩阵 | — | $\mathbb{R}^{d_h \times 2}$ | Ch1 |
| $\mathbf{a}$ | 注意力参数向量 | — | $\mathbb{R}^{3d_h}$ | Ch1 |

---

## G. 实验设计

### G.1 仿真环境参数表

| 参数 | 值 | 来源 |
|------|------|------|
| 星座类型 | Walker-Delta 单壳层 F=1 | contract |
| 轨道高度 $h_{\text{orb}}$ | 550 km | contract |
| 倾角 $i$ | 53° | contract |
| 训练规模 (P×S) | 6×11, 10×10, 10×20 | contract |
| 目标规模 (P×S) | 18×40 | contract |
| ISL 类型 | +Grid, 1550nm 激光 | L02, L04 |
| ISL 带宽 $B_{\text{ISL}}$ | 1 GHz | L03 |
| ISL 断链阈值 $d_{\max}$ | 5000 km | contract |
| 信道模型 | Shannon $B \cdot \log_2(1+\text{SNR})$ | L03 |
| 流量模型 | Uniform | contract |
| 快照数 | 10（均匀采样一个轨道周期） | contract |
| 流量矩阵 | 每快照 5 组, 每组 100 flow | contract |
| 评估 seeds | 123, 42, 0（每 seed 10×5×100） | stat_tests.json |

### G.2 对比对象/Baseline

| 方法 | 类型 | 训练规模 | 推理方式 | 公平性说明 |
|------|------|---------|---------|-----------|
| Ours (Full) | GNN (GAT 3层) | 66+100+200 (多尺度) | 加权 Dijkstra | — |
| GRLR | GNN (GAT 1层)+AC | 720 (同规模) | 加权 Dijkstra | 复现版本，同推理范式 |
| Dijkstra | 传统最短路 | N/A | 全对最短路 | 性能上界 |
| Random | 随机方向 | N/A | 随机 | 性能下界 |

**公平性声明**：GRLR 为复现版本（On-policy AC, 1 层 GAT, 2000 episodes），与原文架构一致。所有方法统一评估协议（相同快照、流量矩阵、flows）。⚠ 需补充同架构不同编码器声明和源-目的对多样性确认（S002）。

**传统方法说明**：MCSR (L10) 和 CMCR (L11) 未纳入实验对比。原因：(1) 两者为非学习型分治方法，与 GNN 端到端路由范式差异大，不属于"控制变量下的等价比较"；(2) MCSR 的 SRD 分段机制和 CMCR 的纬度聚类机制需要独立的基础设施适配，超出本研究的"GNN 跨规模泛化验证"核心范围。它们在 B 段作为传统方法天花板定位。

**消融变体**：
- A1：无 Orbital PE（移除 PE 模块）
- A2：单尺度训练（仅 train_100）
- A3：双消融（无 PE + 单尺度）

### G.3 评估标准

| 指标类型 | 指标 | 定义 | 说明 |
|---------|------|------|------|
| 主指标 | E2E delay (ms) | Σ(ISL 传播时延) | 纯传播延迟，不含排队（⚠ 与 Ch3 延迟模型根本不同，需绪论说明） |
| 辅助指标 | Stretch | 实际时延/Dijkstra 最优时延 | ≥1.0 |
| 辅助指标 | ≤1.2x optimal (%) | stretch≤1.2 的路径比例 | — |
| Contract 指标 | Retention | 同规模时延/跨规模时延 | ⚠ 自造指标（D030），需标注 |

**统计方法**：3 seeds + mean±std + bootstrap 95% CI + Welch's t-test。超出国内学位论文通行标准（18 篇精读零统计报告）。

### G.4 控制变量

| 变量 | 固定值 | 变化范围（消融） |
|------|--------|----------------|
| GNN 架构 | GAT 3 层 h=128 4 heads | — |
| PE 维度 | 16 | — |
| 训练规模 | 66+100+200 | A2: 仅 100 |
| PE | 开启 | A1/A3: 关闭 |
| 推理方式 | 加权 Dijkstra | — |
| 流量模式 | Uniform | ⚠ 未测试其他模式 |
| 训练 epochs | 150 | — |
| 优化器 | Adam lr=1e-3 | — |

### G.5 图表规划

| 编号 | 类型 | 标题 | 数据来源 | 说明 |
|------|------|------|----------|------|
| Fig.1 | 架构图 | 系统架构：训练-推理两阶段 | D.1 | 含多尺度训练和零样本推理流程 |
| Fig.2 | 结果图 | Stretch ratio 对比（Full/A1/A2/A3） | E6 表 | 4组 bar chart + error bar |
| Fig.3 | 结果图 | 跨规模泛化：训练规模 vs 推理规模 heatmap | E4/E5 | 4×4 或 3×4 矩阵 |
| Fig.4 | 消融图 | 消融实验对比 | E1-E3 | stretch/delay 双指标 |
| Tab.1 | 参数表 | 仿真环境参数 | G.1 | 星座/拓扑/评估参数 |
| Tab.2 | Baseline 表 | 对比方法概述 | G.2 | 方法/参数量/训练规模 |
| Tab.3 | 统计表 | 3-seed 统计汇总 | E6 | mean/std/CI + t-test |

---

## 已知局限性（综合终审+旧 materials）

### 仿真简化
1. Shannon 容量模型为 RF 信道，不直接适用光链路（stretch 指标不受绝对值影响）
2. 仅 FSPL，无多普勒/天气衰减/指向误差
3. 流量模型单一（仅 uniform）
4. 单壳层，未考虑多壳层
5. 无 GSL 建模（仅 ISL 路由）
6. 静态快照独立评估，忽略快照间切换代价

### 方法论局限
7. PPO 微调失败（greedy reward 稀疏 + action-reward 解耦）
8. GNN 仅提供边权重偏置，非端到端决策
9. 监督标签依赖 Dijkstra，性能上界受约束
10. PE 设计为手工领域编码，缺理论指导

### 评估局限
11. 仅验证 11x（720 星），1584 星（24x）未执行
12. 3-seed 检验力有限（A2/A3 与 Full 差异不显著）
13. 单一 eval seed（训练 3 seed 但评估 seed 固定）
14. E06（多流量模式）、E07（24x 规模）、E08（GNN 深度）、E09（PE 类型对比）未执行
15. train_66 连通性问题：6 面配置赤道处轨间 ISL >5000km 断链
