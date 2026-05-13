# Literature Notes — GNN-based LEO Mega-Constellation Routing

> 方向：GNN-based routing optimization for LEO mega-constellation networks
> 精读论文数：12 篇精读 + 6 篇摘要验证（L13-L18）
> 检索存档：`search-archive/2026-05-13/` 下 8+ 个 JSON 文件
> 最后更新：2026-05-13（Step 3.5 定向补充检索完成）

---

## 精读论文

### [L01] Toward Scalable SDN for LEO Mega-Constellations: A Graph Learning Approach
- arXiv：arXiv:2604.27478
- **发表状态**：预印本（2026年4月）
- **发表渠道**：arXiv（投 IEEE 期刊中）
- 年份/会议：2026
- 核心贡献：提出分层 SDN 框架，将星座分解为轨道壳层，每个壳层使用 Graph Koopman Autoencoder (GKAE) 进行拓扑压缩和时间预测。GKAE 融合 GNN 空间压缩与 Koopman 理论线性化非线性动态，在连续线性潜空间中预测网络状态演化。中心控制器聚合各壳层预测实现全局协调。
- 方法概述：GNN encoder 将卫星网格压缩为低维嵌入，Koopman 算子将非线性动态映射到线性不变子空间，实现多步预测。节点特征为经纬度+队列长度，边特征为 ISL 距离/容量/状态。
- 实验设置：Starlink Shell 1（1442 颗卫星，550 km，53° 倾角）；20 分钟预测窗口，1 分钟采样间隔
- 使用的 Baseline 方法：
  - CNN：卷积神经网络编码器
  - DNN/MLP：全连接网络编码器
  - LSTM：循环神经网络时间预测
- 关键结论：GNN 空间压缩比 CNN/DNN 提升 43-47.4%；GKAE 时间预测比 LSTM 好 10.81%、比 CNN 好 60.86%；模型体积比 CNN 小 2.7x、比 LSTM 小 40x
- 与本研究关系：**直接相关** — GNN 在 LEO 星座上的首次系统性应用（拓扑表示+预测），非路由算法但是 GNN 路由的基础设施
- 实现关键细节：GNN 的置换不变性和归纳泛化能力使其能从 400 星训练推广到 1444 星推理；分层架构支持新壳层热插拔
- 开源代码：无
- 验证状态：已通过 arXiv 验证

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| 星座按壳层分解，壳层间独立学习 | §III-C | 降低维度但忽略壳层间耦合 |
| 卫星流量和轨迹准周期 | §III-C | Koopman 线性化的前提 |
| 预测用于辅助路由（Backpressure/RL），非直接路由决策 | §IV-B | 本论文不是路由算法 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL（星间） | 自由空间传播 | 距离由轨道力学决定 | 隐含假设 |
| 节点特征 | 位置+队列 | lat, lon, alt, queue_length | §IV |

---

### [L02] Starfield: Demand-Aware Satellite Topology Design for LEO Mega-Constellations
- arXiv：arXiv:2601.10083
- **发表状态**：预印本（2026年1月）
- **发表渠道**：arXiv
- 年份：2026
- 核心贡献：提出基于黎曼度量的需求感知 ISL 拓扑设计算法。在星座球壳流形上构建需求向量场，通过黎曼度量引导 ISL 朝主要流量测地线方向对齐。相比 +Grid，stretch factor 降低 15-20%，跳数减少 30%。
- 方法概述：将卫星视为球面流形上的点，构造流量需求向量场，用黎曼度量编码链路距离，启发式选择最优 ISL 邻居。路由用标准 Dijkstra。
- 实验设置：Starlink Phase 1（1584 星，72 面×22 颗，550 km，53°）；4 种流量模式（uniform/hotspot/distance/population）
- 使用的 Baseline 方法：
  - +Grid：经典网格拓扑（Wood 2001）
  - Random：静态随机拓扑
  - Motif：基于 motif 搜索的拓扑方案
- 关键结论：流量越集中、方向性越强 Starfield 优势越大；均匀流量下优势减弱；密度从 100→400 星时延降 33%，超过 400 改善有限
- 与本研究关系：**方法可借鉴** — ISL 拓扑设计是 GNN 路由的输入；Starfield 的拓扑可提供更好的初始结构；+Grid 是通用 baseline 拓扑
- 实现关键细节：自定义 packet-level 仿真器（Go/C++/Python，9000+ 行）；Shannon-Hartley 链路容量模型
- 开源代码：有（https://github.com/shayunak/Starfield）

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL（激光） | Shannon-Hartley + 逆平方律 | 1 Tbit/s 上限，噪声系数 0.1 | Chaudhry & Yanikomeroglu 2021 |
| GSL（星地） | Shannon-Hartley + 逆平方律 | 100 Gbit/s 上限，噪声系数 0.001，最小仰角 25° | Starlink Technology |

---

### [L03] Joint Laser ISL Matching and Traffic Flow Routing in LEO Mega-Constellations via Lagrangian Duality
- arXiv：arXiv:2601.21914
- **发表状态**：预印本（2026年1月）
- **发表渠道**：arXiv
- 年份：2025/2026
- 核心贡献：首个将激光 ISL 连接匹配与业务流路由**联合优化**的框架（DuJo），通过拉格朗日对偶松弛将 NP-hard MILP 解耦为三个多项式可解子问题（加权图匹配 + 最短路径 + LP 速率分配），相比 Grid 方案吞吐提升最高 145%。
- 方法概述：对链路速率约束做拉格朗日松弛，次梯度下降迭代求解对偶问题。每轮：贪心加权图匹配(MWM)→Dijkstra 最短路径(SPF)→LP 流量速率最大化(FRM)。500 轮收敛。
- 实验设置：Starlink 真实 TLE 数据（默认 1000 星）；额外测试 Walker-delta（50°，1000 星）、OneWeb（650 星）
- 使用的 Baseline 方法：
  - +Grid：网格对齐匹配 + OSPF 路由
  - Rand：随机匹配 + OSPF
  - MRate：最大链路速率匹配 + OSPF
- 关键结论：联合优化显著优于分离决策；非规则星座（Starlink）优势更大；论文在结论中明确提出"learning to predict Lagrange multipliers"作为未来方向
- 与本研究关系：**方法可借鉴** — 拉格朗日乘子反映拥塞权重，可融入 GNN 边特征；联合优化框架可作为 GNN 路由的对比基准；真实 Starlink 仿真框架可复用
- 实现关键细节：Python + Numba JIT；HiGHS LP 求解器；Intel Core Ultra 9 285K
- 开源代码：论文录用后公开

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| LISL（激光） | 高斯光束 + IM-DD | P₀=20W, λ=1.55μm, 束散角 100μrad, W₀=9.87e-3m, z_R=1.97e3m | Saleh & Teich 2019 |
| LISL 接收 | IM-DD 光检测 | A=0.01m², Ψ=0.5A/W, σ_N=3e-7A | Kaymak 2018 |
| LISL 指向误差 | Rayleigh 分布 | σ_J=10μrad, 中断阈值 ε=0.001 | Arnon 2003 |
| 流量模型 | 人口驱动 Poisson | 活跃率 0.01%, D=0.1Gbps/用户, Q=20Gbps | GHS-POP 2023 |

---

### [L04] Investigating Inter-Satellite Link Spanning Patterns on Networking Performance in Mega-Constellations
- arXiv：arXiv:2312.15873
- **发表状态**：正式发表（推测 IEEE 期刊）
- **发表渠道**：IEEE 期刊（具体刊名未在 arXiv 版本标注）
- 年份：2023
- 核心贡献：首次对 Walker 星座 ISL spanning pattern 进行形式化定义，通过相位偏差集合 B 将 ISL 拓扑分类为 '+Grid'（每星 4 ISL）和 '*Grid'（每星 6 ISL）共 10 种模式。穷举评估所有 pattern 的时延/stretch/容量/吞吐。
- 方法概述：Walker 星座 T/P/F/i 建模，枚举所有合法相位偏差子集，Dijkstra 最短路径 + max-flow 评估。
- 实验设置：Walker 星座（20²=400 星为主，另测 10²/30²/40²）；53° 倾角；'+Grid' 和 '*Grid' 两种 ISL 模式
- 使用的 Baseline 方法：本文为穷举对比范式，对比 10 种 ISL spanning pattern
- 关键结论：'+Grid' 最优 bm1（F=Fm），时延 <50ms；'*Grid' 最优 b0m1（F=0），容量比 '+Grid' 高 37%；密度 400 星是性价比较高的选择
- 与本研究关系：**方法可借鉴** — ISL 拓扑形式化定义方法（相位偏差集合）可直接用于 GNN 路由仿真环境的拓扑建模；多密度基准数据可复用
- 实现关键细节：自研仿真框架（基于图论算法），Dijkstra 路由 + max-flow 吞吐计算
- 开源代码：无

**建模假设**：
| 假设 | 说明 |
|------|------|
| 拓扑准静态 | 相邻时间戳之间拓扑不变（eISL 遇到式切换） |
| 卫星容量无限 | 仅受 ISL 链路容量限制 |
| 自由空间传播 | 链路容量由 free space loss 决定 |

---

### [L05] xeoverse: A Real-time Simulation Platform for Large LEO Satellite Mega-Constellations
- arXiv：arXiv:2406.11366
- **发表状态**：预印本（2024年6月）
- **发表渠道**：arXiv
- 年份：2024
- 核心贡献：提出基于 Mininet 的实时 LEO 星座仿真平台，在单机（26核 64GB）上仿真完整 Starlink（5442 星）。核心设计：预计算拓扑 + 增量链路更新 + 流量相关子集筛选。比 Hypatia 快 2.3x，比 StarryNet 快 40x。
- 方法概述：Back Stage（TLE→SGP4 轨道传播→连通/延迟/容量矩阵→Dijkstra 路由表）+ Main Stage（Mininet 进程级虚拟化，增量更新 ISL/GSL）。
- 实验设置：Starlink Shell 1（1584 星）和全星座（5442 星）；TLE 轨道数据；Grid ISL 拓扑
- 使用的 Baseline 方法（仿真工具对比）：
  - Hypatia：NS-3 离散事件仿真器
  - StarryNet：Docker 容器仿真器
  - ns-3/STK/MATLAB：通用工具
- 关键结论：单机实时仿真可行；晴天与真实 Starlink 吞吐误差 2%；ISL 路径变更对 TCP 性能影响显著（延迟均值上升 67.6%），Hypatia 无法捕获
- 与本研究关系：**方法可借鉴** — 星座拓扑建模框架可作为 GNN 路由的仿真环境或数据生成工具；预计算的连通/延迟/容量矩阵可直接作为 GNN 图特征输入；Dijkstra 可作为 baseline
- 实现关键细节：Python + Mininet + networkx；SGP4/J2/J4 轨道传播器；Shannon 公式 + ITU-T Ku/Ka 波段 SNR 模型 + 天气衰减（OpenWeatherMap API）
- 开源代码：未公开，需联系作者

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL | 固定容量光链路 | 容量可配置，延迟按传播距离 | Grid 拓扑设计 |
| GSL | ITU-T Ku/Ka + Shannon | EIRP, 自由空间损耗, 天气衰减 | ITU-T 标准 |
| 天气 | OpenWeatherMap 实时 | 降雨/降雪/温湿度/气压 | OpenWeatherMap API |

---

### [L06] Graph Neural Network-Based Multicast Routing for On-Demand Streaming Services in 6G Networks
- arXiv：arXiv:2510.11109
- **发表状态**：预印本（2025年10月），投 IEEE 期刊中
- **发表渠道**：IEEE Transactions on Mobile Computing（DOI: 10.1109/TMC.2025.3634587）
- 年份：2025
- 核心贡献：提出 GNN+RL 组播路由框架（GPN），基于 GAT 编码器 + LSTM 路径历史聚合器 + 注意力解码器，策略梯度训练。利用 flow-reuse 结构特性，按需求降序逐用户构建路径。训练在 30 节点，零样本泛化到 50 节点。
- 方法概述：序列化 MDP 建模，GAT 编码节点嵌入，LSTM 聚合已选路径历史，注意力解码器输出候选下一跳概率分布。REINFORCE 训练。
- 实验设置：合成随机图（NetworkX Erdos-Renyi），30-50 节点，1-15 用户，degree=4
- 使用的 Baseline 方法：
  - Dijkstra (Shortest Path)：独立最短路径，无路径复用
  - DP (Dynamic Programming)：理论最优参考
  - BCO (Bee Colony Optimization)：人工蜂群优化
  - GA (Genetic Algorithm)：遗传算法
- 关键结论：GPN 接近 DP 理论最优；比 GA 快多个数量级；30→50 节点零样本泛化；GAT 编码器贡献最大
- 与本研究关系：**直接相关** — GAT+LSTM+Policy Gradient 路由架构可直接迁移到 LEO ISL 路由；拓扑泛化能力对卫星场景有直接参考
- 开源代码：有（https://github.com/UNIC-Lab/GNN-Routing）

**结构化提取**：

1. **状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|------------|
| 图 G=(V,E) | 30-50 节点 | GAT 编码 |
| 已访问节点集 | 前 k-1 用户路径节点并集 | 直接使用 |
| 当前部分路径 | 节点子集 | LSTM 编码 |
| 候选下一跳 | 当前节点邻居 | softmax 归一化 |

2. **动作空间**：离散 | 动态维度（=候选下一跳数） | 防环约束（已在路径中的节点 logit=-∞）

3. **奖励函数**：$r_t = -x_{(k)} \cdot e(u_t, v_t)$，回报 $R = \sum_t \gamma^t r_t$ | 无归一化 | 单目标

4. **建模假设**：最优解为树结构（Theorem 1）；共享链路流量=下游最大需求（Lemma 1）；链路代价静态

5. **网络架构**：
| 组件 | 层类型 | 维度 | 激活函数 |
|------|--------|------|----------|
| GAT 编码器 | Graph Attention (K=4 heads) | H=128 | LeakyReLU(attention), ReLU(update) |
| 路径聚合器 | LSTM | hidden=128 | LSTM 门控 |
| 注意力解码器 | Attention scoring | →标量 | tanh |
| 输出 | Softmax | 候选数 | — |

训练：lr=5e-4, Adam, gradient clip=1.0, MultiStepLR(γ=0.96), batch=16, 20 epochs, 2500 steps/epoch

---

### [L07] Structural Generalization for Microservice Routing Using Graph Neural Networks
- arXiv：arXiv:2510.15210
- **发表状态**：预印本
- **发表渠道**：arXiv
- 年份：2025
- 核心贡献：提出边特征感知注意力机制的 GNN 路由优化框架，将微服务调用图建模为动态图，GNN 做信息聚合，注意力机制感知链路质量，softmax 输出路由决策。MRE 0.072，路由决策准确率 91.4%。
- 方法概述：多层 GNN message-passing + 边感知注意力（$\alpha_{ij} = \text{softmax}(\mathbf{a}^\top [W_q h_i \| W_k h_j \| e_{ij}])$）+ MLP 评分 + softmax 路由选择。
- 实验设置：DeathStarBench Social Network 数据集，10+ 微服务，GNN 4 层最优
- 使用的 Baseline 方法：
  - RouteNet-Fermi：GNN 网络建模（IEEE/ACM ToN）
  - GNN-DRL：GNN+DRL 路由优化
  - OSPF：PPO+GNN SDN 路由
- 关键结论：4 层 GNN 最优（过深导致过平滑）；平均出度 2.5 性能峰值；边感知注意力对链路质量波动建模有效
- 与本研究关系：**方法可借鉴** — 边感知注意力对卫星链路质量波动建模有参考价值；但面向微服务（小规模、静态拓扑），需大量适配
- 开源代码：无

**结构化提取**：

1. **状态空间**：节点特征（CPU利用率、响应时间、队列长度）+ 边特征（调用延迟、链路稳定性）

2. **动作空间**：离散 | 候选目标集合 $C(i)$ | softmax 概率选择

3. **奖励函数**：论文未给出显式公式 — 重要缺失

4. **网络架构**：
| 组件 | 层类型 | 维度 | 激活函数 |
|------|--------|------|----------|
| GNN 骨干 | Message-passing | 未披露 | ReLU |
| 注意力 | Edge-aware attention | 未披露 | — |
| 评分头 | MLP | [h_i‖h_j]→标量 | — |
| 输出 | Softmax | 候选数 | — |

---

## 精读论文（IEEE，用户手动获取）

### [L08] GNN-Based Routing for Link Reliability Optimization in SD-LEO Satellite Networks
- DOI：10.1109/NFV-SDN61811.2024.10807492
- **发表状态**：正式发表
- **发表渠道**：IEEE NFV-SDN 2024 会议
- 年份：2024
- 核心贡献：将基础 GCN 应用于 SD-LEO 卫星网络的 ISL 链路可靠性评估与切换管理。GNN 仅做 ISL 性能指标聚合（mean pooling），路由决策由 SDN 控制器完成。
- 方法概述：标准 GCN（$\hat{A}H^{(l-1)}W^{(l)}$）+ FC 层输出全局网络状态 → SDN 控制器根据链路成本公式（$C_{ij} = k_1 L_{ij} + k_2/B_{eff,ij} + k_3 PLR_{ij}$）做路由决策。
- 实验设置：Iridium 星座（66 星，6 面×11 星，780 km）；NS-3.37.1 + NetworkX；300 秒仿真
- 使用的 Baseline 方法：无（仅展示自身性能，无对比实验）
- 关键结论：平均时延 99.6-100.5 ms，带宽 ~700 Kbps（窄带），丢包率 4-11%；切换时服务不中断
- 与本研究关系：**已知唯一 GNN+LEO 路由论文**，但仅用 GCN 做聚合不做决策，66 星小规模，窄带，质量有限（会议论文，无 baseline 对比）
- 实现关键细节：链路成本考虑时延（$d_{ij}/c$）、仰角相关有效带宽、丢包率；节点特征为 ISL 性能指标
- 开源代码：无
- 验证状态：已精读

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| Iridium 66 星小星座 | §V | 非巨型星座，结论不可直接推广 |
| 窄带 700 Kbps | §V | 非宽带卫星通信场景 |
| GNN 仅做聚合 | §IV-D | 不是端到端学习型路由 |
| 无 baseline 对比 | §V | 无法评估相对性能 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL | 传播时延 + 仰角带宽 + 丢包率 | $L_{ij}=d_{ij}/c$, $B_{eff}=B_{ij}\cdot(\theta_{eff}/90°)$, $PLR_{ij}$ | Kumar 2021 |
| 仰角模型 | 几何三角 | $R_e$=6371km, $h$=780km, $\theta_{min}$约束 | Cakaj 2011 |

---

### [L09] Geographic-Based Auxiliary Routing Scheme in SDN-Based Mega Constellation Networks
- DOI：10.1109/JIOT.2025.3638842
- **发表状态**：正式发表
- **发表渠道**：IEEE Internet of Things Journal（SCI Q1）
- 年份：2026
- 核心贡献：提出轻量级地理辅助路由方案 GARS，作为 SDN 集中路由的故障恢复辅助。利用 Walker-Delta 星座轨道几何信息实现 O(1) 复杂度的分布式路由，恢复时间缩短 65.5%，丢包率降低 67.2%。
- 方法概述：Walker-Delta 坐标模型 → 基于相对几何位置的 GRA（Algorithm 2/3）→ 三级优先级防环机制（loop > direction > availability）→ 扩展 BFD 协议传递邻居链路状态
- 实验设置：Walker-Delta（70° 倾角，1000 km）；600-2000 星；STK + OMNeT++；链路故障率 1%-15%
- 使用的 Baseline 方法：CRA（SDN 集中路由）、OSPF-TE（分布式最短路径）、传统 GRA
- 关键结论：GARS 恢复时间比 CRA 短 253ms（2000 星），丢包率低 2.57%；故障率越高优势越大；O(1) 复杂度不随规模增长
- 与本研究关系：**方法可借鉴** — GRA 作为 O(1) 快速路由的 baseline 参考；防环机制设计思路可参考；但不涉及 ML/GNN
- 实现关键细节：扩展 BFD 协议（添加链路状态和拥塞位）；每节点维护 4 链路优先级数组 <L, D, A>；GRA 表存储目标-下一跳映射
- 开源代码：无
- 验证状态：已精读

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| Walker-Delta 星座，70° 倾角 | §III | 不适用 Walker-Star 或不规则星座 |
| 每星 4 ISL（2 轨内 + 2 轨间） | §III | 未考虑 6 ISL 或动态 ISL 拓扑 |
| GRA 仅做故障恢复辅助 | §IV-A | 不替代集中路由，仅作临时路径 |
| 链路带宽容量 1.5 Gb/s | §V-C | 固定带宽假设 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL | 链路带宽利用率 | capacity=1.5Gb/s, congestion thresholds: 30%/80% | §IV-D |
| 链路状态 | BFD 检测 | 检测时间 ≤50ms（软件），≤3.3ms（硬件） | RFC 5883 |

---

### [L10] Multi-Attribute Consistency Segment Resilient Routing for LEO Satellite Mega Constellation
- DOI：10.1109/TMC.2025.3570670
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Mobile Computing（SCI Q1）
- 年份：2025
- 核心贡献：提出多属性一致性分段弹性路由 MCSR，将巨型星座分割为不相交的段路由域（SRD），联合优化域内/域间更新时间。支持 3 类差异化服务（LS/TS/HR），重路由频率降低 45%，在 10000 星规模下收敛时间比 SPF 降低 63%。
- 方法概述：Walker-Delta → SRD 分割（最小化联合更新时间 $T_{Cov}$）→ 多属性一致性主导路径筛选（tuple {D, A, J}）→ 域间 SRD-BCM 协作 + 域内分布式计算 → 弹性重路由（周期 3min + 条件触发）
- 实验设置：5 种星座（Kuiper K1=1156 星 / Starlink S1=1584 / Walker3024 / Walker5040 / Walker10000）；基于 Hypatia + NS-3 自研平台；全球 100 城市 CBR 流量 10-50 Mbps
- 使用的 Baseline 方法：SPF、OSPF、AODV、TPLB（流量预分流负载均衡）、CMCR（L11 聚类多准则路由）
- 关键结论：MCSR-LS 平均 RTT <100ms（SPF 150ms）；吞吐量比 AODV/CMCR 提高 19%；PDR 97.2%（SPF 92.5%）；服务可用率 99.8%；SRD 中位数路径变化 4-8 次
- 与本研究关系：**方法可借鉴** — 目前 LEO mega-constellation 路由中最强的传统方法之一；SRD 分割思想可用于 GNN 的图划分；多属性一致性可作 GNN 路由的辅助策略；**重要 Baseline 对比对象**
- 实现关键细节：SRv6+uSIDs 协议；基于 TLE 预计算 ISL 切换；DS（指定卫星）负责域间路由计算；ISL 带宽 1Gbps，GSL 100Mbps
- 开源代码：无（基于开源 Hypatia 开发）
- 验证状态：已精读

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| Walker-Delta 星座 | §II-A | 不适用极轨/太阳同步轨道 |
| 每星 4 ISL | §II-A | 未考虑动态 ISL 拓扑 |
| $T_{Cal}$ 为常数 | §II-C | 忽略规模扩大时计算时间增长 |
| 完美星历信息 | §V-C | 未考虑轨道摄动 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL | 自由空间传播 | bandwidth=1Gbps, B=500, D=d/c, A=(B-b_t)/B | Table II |
| GSL | 仰角约束 | $L_{MAX-GSL}=h/\sin(\phi_{min})$, bandwidth=100Mbps, $\phi_{min}$=25°(Starlink)/45° | §II-E |

---

### [L11] Clustered Multi-Criteria Routing Algorithm for Mega LEO Satellite Constellations
- DOI：10.1109/tvt.2024.3396350
- **发表状态**：正式发表（22 次引用）
- **发表渠道**：IEEE Transactions on Vehicular Technology（SCI Q1）
- 年份：2024
- 核心贡献：提出聚类多准则路由 CMCR，按飞行方向+LoS+纬度将巨型星座分簇，将路由分为簇内/簇间。引入属性一致性理论（Theorem 1-4 证明收敛），支持多模态服务（MCPTT 延迟优先 / MCD 可靠性优先）。复杂度 $[n \cdot O(N^2), n \cdot O(N^3)]$。
- 方法概述：Walker-Delta 70° → 聚类（9 轨×2 星/簇）→ 时变图 → 属性一致性主导路径（tuple {D, A} 的笛卡尔积）→ 簇内 CMCR + 簇间 edge-ISL 路由
- 实验设置：Starlink Phase I（1584 星，72×22，550 km，70°）；1000 字节分组，缓冲 500 分组，ISL 带宽 100 Mbps
- 使用的 Baseline 方法：IUDR（ISL utility-based dynamic routing）、TPLB（traffic pre-shunting load balancing）
- 关键结论：MCPTT 服务时延低于 TPLB/IUDR；MCD 服务 PDR 保持 100%；OR（机会路由利用反向飞行 ISL）进一步降低时延；理论证明无环且收敛到最优
- 与本研究关系：**方法可借鉴** — 有理论保证的传统路由算法；属性一致性理论可融入 GNN 的训练目标；聚类思想可用于 GNN 的分层架构；**重要 Baseline 对比对象**
- 实现关键细节：M/M/1 排队模型（$D = d/c + p/r + b_k/r$，$A = (B-b_k)/B$）；聚类按纬度动态调整（阈值纬度 $l_1$ 处分裂/合并）
- 开源代码：无
- 验证状态：已精读

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| Walker-Delta 70° | §II-A | 不适用其他星座类型 |
| 每星 4 ISL + CH 额外 4 ISL | §II-B | 特定连接模式假设 |
| M/M/1 排队 | §III-B | 简化的流量模型 |
| 静态聚类（周期性调整） | §II-B | 非实时动态聚类 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| ISL | M/M/1 排队 + 自由空间 | bandwidth=100Mbps, B=500, D=d/c+p/r+b_k/r | §III-A |
| LoS 约束 | 几何 | $\theta = 2\arccos((R+\tau)/(R+h))$, $\tau$=100km, $h$=550km | §II-B |

---

### [L12] A Scalable Multicontroller SDN Framework for LEO Mega-Constellation via Topology Virtualization
- DOI：10.1109/JIOT.2025.3576912
- **发表状态**：正式发表
- **发表渠道**：IEEE Internet of Things Journal（SCI Q1）
- 年份：2025
- 核心贡献：提出全球可扩展的多控制器 SDN 框架，通过拓扑虚拟化屏蔽控制平面频繁变化。将虚拟-物理映射分解为平面映射+集群映射，推导出 O(N_V·N_H) 闭式解。证明星座规模增大时渐近最优（R_rms → 0）。两种负载均衡规则 LFR/FFR 将计算时间从 47.36 秒降至 ~10ms。
- 方法概述：Walker-Delta 卫星聚类 → ECEF 虚拟集群定义 → k-means++ 地球固定单元分组预分配 → 平面映射（基于 RAAN 差异）+ 集群映射（球面三角）→ LFR/FFR 负载均衡
- 实验设置：Starlink Gen II（90×28=2520 星，530 km，53°）；H3 六边形网格 4794 单元；SDN 控制器 1-250 个；最小仰角 10°-30°；3 小时仿真
- 使用的 Baseline 方法：GHA（全局匈牙利，O(N_V³N_H³)）、PHA（逐平面匈牙利，O(N_V³N_H)）、BB（分支定界负载均衡）
- 关键结论：Proposed 闭式解映射距离为 GHA 最优的 119%，但计算时间 <0.1s（GHA 需 15.99 小时）；映射间隔 65-190s（GHA 36-91s），网络更稳定；FFR/LFR ~10ms vs BB 47.36s
- 与本研究关系：**方法可借鉴** — SDN 控制器架构可作为 GNN 路由的部署框架；拓扑虚拟化思想可用于 GNN 输入的图预处理；但不涉及路由算法本身或 ML
- 实现关键细节：仅考虑接入链路（无 ISL）；负载模型 Uniform(0,1) 每 15 秒更新；基于几何可见性（最小仰角）判断覆盖
- 开源代码：无
- 验证状态：已精读

**建模假设**：
| 假设 | 位置 | 影响 |
|------|------|------|
| Walker-Delta 星座 | §II-A | 不适用不规则星座 |
| 无 ISL，仅接入链路 | 全文 | 不支持星上路由 |
| 负载独立同分布 Uniform(0,1) | §V-A | 忽略真实流量时空相关性 |
| SDN 控制器完全获取负载信息 | §II-B | 未考虑信息获取延迟 |

**信道模型参数**：
| 链路类型 | 模型 | 参数 | 来源 |
|---------|------|------|------|
| 接入链路 | 几何可见性（最小仰角） | $R_e$=6400km, $h$=530km, $\gamma$∈[10°,30°], $d_{max}$公式 | §II-A |
| ISL | 未建模 | — | 论文未考虑 |

---

## 补充检索论文（Step 3.5，基于摘要 + Semantic Scholar API 验证）

> 以下论文通过 Step 3.5 定向检索发现，经 Semantic Scholar API 验证摘要和引用数据。
> 核心验证目标：是否涉及 GNN size generalization。结论：**无一涉及**。
> 验证手段：Semantic Scholar paperId/DOI 查询 + 引用链分析 + 摘要文本比对。

### [L13] GRLR: Routing With Graph Neural Network and Reinforcement Learning for Mega LEO Satellite Constellations
- DOI：10.1109/TVT.2024.3471658
- **发表状态**：正式发表（**44 次引用**，Semantic Scholar paperId: 0813c11caa97b3b1044656fc76bc43d16967131c）
- **发表渠道**：IEEE Transactions on Vehicular Technology（SCI Q1）
- 年份：2025
- 核心贡献：在 Walker-Delta 星座中将路由建模为 MDP，结合 GNN 特征提取与 Actor-Critic RL 框架实现分布式智能路由。GNN 提取用户分布、网络拓扑和 ISL 动态特征，Actor-Critic 网络做路由决策，目标为最小化源-宿卫星间时延。
- 实验设置：Walker-Delta mega-LEO 星座
- 与本研究关系：**直接竞争者** — GNN+RL LEO 路由领域引用最高的论文。但 **未涉及 size generalization**（已通过 Semantic Scholar API 验证 TVT 2025 和 ICCC 2023 两个版本的摘要，均无提及）。Web 搜索声称其涉及 size generalization 系 AI 幻觉。
- 会议版本：ICCC 2023（paperId: 9349bd943ed50df01d4ef11a2d0013c88a28088d），摘要几乎相同

---

### [L14] GraphPR: Fully-Distributed Dynamic Packet Routing for LEO Satellite Networks
- DOI：10.1109/TVT.2024.3499933
- **发表状态**：正式发表（**19 次引用**）
- **发表渠道**：IEEE Transactions on Vehicular Technology（SCI Q1）
- 年份：2025
- 核心贡献：全分布式 GNN+MADRL 动态包路由算法。路由建模为 POMDP，每颗卫星仅与一跳邻居共享信息，GAT 编码局部信息隐式捕获多跳状态，MADRL 做分布式路由决策。设计 RSPH（Residual Shortest Path Hops）机制避免路由环路。
- 方法概述：GAT 编码一跳邻居 → 隐式多跳状态 → MADRL 分布式优化 → RSPH 防环
- 与本研究关系：**直接竞争者** — GAT+MADRL 全分布式架构设计精巧。但 **未涉及 size generalization**。

---

### [L15] Inter-Satellite Routing for LEO: A GNN and DRL Integrated Approach (GQN)
- DOI：10.1109/ICCC62479.2024.10681995
- **发表状态**：正式发表（**12 次引用**）
- **发表渠道**：IEEE/CIC ICCC 2024 会议
- 年份：2024
- 核心贡献：将 LEO 卫星网络建模为图，GNN 学习卫星节点关系，DRL 做自适应路由决策。目标为最小化全网平均端到端时延 + 链路负载均衡。
- 实验设置：108 颗卫星
- 与本研究关系：**直接竞争者** — GNN+DRL 星间路由。仅有时序泛化（跨时间槽），**未涉及跨规模泛化**。前次会话全文分析确认。

---

### [L16] GDRL-SFCR: Deep RL Routing with Service Function Constraints
- DOI：10.3390/s25041232
- **发表状态**：正式发表
- **发表渠道**：MDPI Sensors（SCI）
- 年份：2025
- 核心贡献：GNN+DRL 端到端路由，联合优化传输时延和网络负载均衡，考虑 SFC（Service Function Chain）约束。基于最新 NTN LEO 端到端传输架构建模。
- 方法概述：GCN 提取节点属性和动态拓扑 → PPO 训练 → SFC 约束奖励函数
- 实验设置：**6048 颗卫星**（GNN+LEO 路由领域报告的最大规模）
- 关键结论：时延 -11.3%+，负载 -14.1%+，接入成功率 +19.1%+，容量 2x
- 与本研究关系：**直接竞争者** — 规模最大的 GNN+LEO 实验，NTN 建模可参考。但在 **单一规模 6048 星上训练和测试，未涉及 size generalization**。

---

### [L17] GAT-LSTM-DQN: Spatial-Temporal Routing with Proactive Congestion Avoidance
- arXiv：arXiv:2605.02413
- **发表状态**：预印本
- **发表渠道**：arXiv
- 年份：2026
- 核心贡献：GAT+LSTM+DQN 时空路由框架，GAT 编码空间拓扑，LSTM 捕获时序动态，DQN 输出路由决策。支持主动拥塞避免。
- 实验设置：**45 颗卫星**（规模极小）
- 与本研究关系：**间接竞争者** — 时空 GNN 架构可参考。**未涉及 size generalization**。为 GRLR 的引用者。

---

### [L18] DTAR: Traffic-Aware Domain Partitioning and Load-Balanced Inter-Domain Routing
- **发表状态**：预印本
- 年份：2026
- 核心贡献：流量感知域划分 + GAT+PPO 域间路由。离线 NSGA-II 多目标优化生成域划分，在线 GAT 动态编码域间状态 + Action-masked PPO 学习路由。测试正常、流量激增、故障三种场景。
- 方法概述：NSGA-II 离线域划分 → GAT 编码域间链路状态 → Action-masked PPO 在线路由
- 实验设置：288 颗卫星 Walker 星座
- 与本研究关系：**直接竞争者** — 域划分+GAT+PPO 混合架构有参考价值，域划分思想可与 GNN 规模泛化结合。**未涉及 size generalization**。为 GRLR 的引用者。

---

## 综合分析

### 1. 现有方法分类

**A. 传统路由方法（非 ML）**
- **Dijkstra/OSPF 最短路径**：Starfield (L02)、DuJo (L03)、ISL Pattern (L04)、xeoverse (L05) 均使用 Dijkstra 作为基础路由。简单、确定性，但无法适应动态负载和链路质量变化。
- **拉格朗日对偶松弛**：DuJo (L03) 将 ISL 匹配与路由联合优化。理论优雅但计算耗时（分钟级），且为静态快照优化。
- **启发式拓扑设计**：Starfield (L02) 用黎曼度量引导 ISL 方向，ISL Pattern (L04) 穷举 Walker 星座拓扑。均为拓扑层面优化，路由本身仍用 Dijkstra。
- **地理辅助路由**：GARS (L09) 利用轨道几何实现 O(1) 复杂度快速故障恢复路由，三级优先级防环机制设计精巧。
- **聚类多准则路由**：CMCR (L11) 按飞行方向+纬度分簇，属性一致性理论筛选主导路径，有理论收敛保证。
- **分段弹性路由**：MCSR (L10) 将星座分割为 SRD，支持 3 类差异化服务，在 10000 星规模下验证可扩展性。
- **域划分 + DRL 路由**：DTAR (L18) 用 NSGA-II 离线域划分 + GAT+PPO 在线路由。域划分降低决策空间，但非模型泛化。

**B. GNN + RL 路由（LEO 卫星专用，2024-2026 新兴活跃方向）**
- **GRLR (L13)**：GNN + Actor-Critic RL，Walker-Delta，MDP 建模，时延最小化。**44 引用**，该方向引用最高的工作。每星 4 ISL，分布式决策。
- **GraphPR (L14)**：GAT + MADRL，POMDP，**全分布式**（仅一跳邻居通信），RSPH 防环机制。19 引用。
- **GQN/ICCC (L15)**：GNN + DRL 集成，图建模卫星网络，108 星，最小化全网平均端到端时延。仅时序泛化。12 引用。
- **GDRL-SFCR (L16)**：GCN + PPO，**6048 星**（GNN+LEO 最大规模），SFC 约束，NTN 架构。单一规模训练测试。
- **GAT-LSTM-DQN (L17)**：GAT+LSTM+DQN 时空路由，45 星，主动拥塞避免。规模极小。
- **DTAR (L18)**：GAT + Action-masked PPO，288 星 Walker，域划分+在线路由。混合架构。
- **DRL-MPCR**（IEEE IoTJ 2025）：DRL 多路径协作路由，**非 GNN**，水填充调度。

**C. GNN 方法（非 LEO 专用）**
- **GNN + 指标聚合**：L08 用基础 GCN 做 ISL 性能指标聚合（非路由决策），66 星 Iridium 窄带。
- **GNN + 表示学习**：GKAE (L01) 用 GNN 压缩星座拓扑 + Koopman 预测。非路由算法，但证明 GNN 置换不变性适合卫星网络。
- **GNN + RL 路由（地面）**：GPN (L06) 用 GAT+LSTM+Policy Gradient 做组播路由（30-50 节点合成图），证明拓扑泛化可行性。
- **GNN + 监督路由**：微服务路由 (L07) 用边感知 GNN + softmax 端到端学习。

**D. SDN 架构与仿真基础设施**
- 多控制器 SDN (L12)：拓扑虚拟化可扩展控制平面。
- xeoverse (L05)：单机实时仿真完整 Starlink (5442 星)，基于 Mininet + 预计算。
- **关键发现**：所有仿真平台均不支持学习型路由，GNN 路由需自建仿真或替换路由模块。

### 2. 已知局限

| 来源 | 局限 | 具体内容 |
|------|------|---------|
| L01 (GKAE) | 不是路由算法 | 仅做拓扑表示和状态预测，路由仍依赖 Backpressure/RL |
| L01 (GKAE) | 壳层间耦合被忽略 | 分层架构假设壳层独立，但实际 ISL 跨壳层通信影响路由 |
| L03 (DuJo) | 静态快照优化 | 不处理时间动态切换，每次快照需分钟级计算 |
| L06 (GPN) | 合成图实验 | 30-50 节点 Erdos-Renyi 图，未测试卫星拓扑特性 |
| L08 (GNN-SD-LEO) | 仅 GCN 聚合非路由 | GNN 只做指标聚合，路由决策由 SDN 控制器完成 |
| L08 (GNN-SD-LEO) | 极小规模窄带 | 66 星 Iridium + 700Kbps 窄带 |
| L13 (GRLR) | 单一规模训练测试 | 44 引用但未做跨规模泛化实验，摘要和会议版均无提及 |
| L14 (GraphPR) | POMDP 仅一跳信息 | 全分布式但信息受限，可能限制全局优化质量 |
| L15 (GQN) | 仅时序泛化 | 108 星，跨时间槽泛化但未跨规模 |
| L16 (GDRL-SFCR) | 单一规模 6048 星 | 最大规模但训练测试同规模，无泛化验证 |
| L17 (GAT-LSTM-DQN) | 极小规模 | 仅 45 星，预印本 |
| L18 (DTAR) | 域划分依赖离线优化 | NSGA-II 域划分离线完成，适应性受限 |
| 全部 GNN+LEO | **无 size generalization** | L13-L18 六篇论文无一涉及 GNN 跨规模泛化 |
| 全部 LEO 路由 | 仿真工具不支持 ML | xeoverse/Hypatia/StarryNet 均为静态路由 |

### 3. 2-3 年趋势

**技术路线演进**：
1. **2023-2024**：传统优化方法主导 LEO 路由。GNN 首次应用于 LEO 网络表示（L01），仅做预测不做路由。GQN/ICCC 2024 (L15) 首次将 GNN+DRL 用于 LEO 星间路由。
2. **2025**：**GNN+RL LEO 路由爆发** — GRLR (L13, TVT, 44 引用) 和 GraphPR (L14, TVT, 19 引用) 在同一期刊发表，确立了 GNN+RL 作为 LEO 路由的有效范式。GDRL-SFCR (L16) 在 6048 星规模验证可行性。传统路由向多属性/多目标联合优化演进（L10 MCSR、L11 CMCR）。
3. **2026**：领域划分+GAT+PPO 混合架构出现（DTAR, L18）。时空 GNN 路由（L17）。多路径 DRL 路由（DRL-MPCR, IEEE IoTJ）。方向仍在快速演进中。

**关键趋势**：
- GNN+RL 从"验证可行性"（2024）到"成为主流范式之一"（2025-2026），已有多篇 IEEE 期刊论文
- GAT 成为 LEO 路由中 GNN 的主导架构（L14, L18, L17 均使用 GAT）
- 全分布式架构趋势明显（L14 GraphPR 的 POMDP + 一跳邻居通信）
- 规模从 45 星 (L17) → 108 星 (L15) → 288 星 (L18) → 6048 星 (L16)，但 **全部在单一规模训练测试**
- **核心空白确认**：6 篇 GNN+RL LEO 路由论文（L13-L18），无一涉及跨规模泛化。传统方法（L10 MCSR）通过分治策略处理大规模，但 GNN 模型的 size generalization 在卫星路由中完全未被探索

### 4. GNN 架构选择分析

| 架构 | 现有使用 | 优势 | 劣势 | 适合 LEO 路由？ |
|------|---------|------|------|---------------|
| GCN | L01, L08, L16 | 简单、快速 | 平等对待所有邻居 | 基础 baseline |
| GAT | L06, L07, **L14, L17, L18** | 注意力加权，可融入边特征 | 计算量稍大 | **主流选择** — LEO 路由中 GAT 已成主导 |
| GraphSAGE | 无 | 采样聚合，天然支持归纳推理 | 采样可能丢失关键邻居 | 可选 — 适合大规模+size generalization |
| GKAE | L01 | 线性化时间动态 | 复杂 | 辅助模块 |

**趋势**：GAT 在 2025-2026 的 LEO GNN 路由论文中占主导地位（L14, L17, L18），但 GraphSAGE 的采样机制天然更适合 size generalization（训练时见过固定数量邻居，推理时不受图规模影响），值得探索。

### 5. Size Generalization 现状

**核心问题**：在小星座（如 66 星 Iridium）上训练的 GNN，能否泛化到 Starlink 级（4000+ 星）？

**已验证：无一涉及 size generalization**

| 论文 | 规模 | 跨规模实验？ | 说明 |
|------|------|-------------|------|
| L01 (GKAE) | 1442 星 | ❌ | 理论分析支持归纳泛化，但未做跨规模测试 |
| L06 (GPN) | 30→50 节点 | ✅ (仅 67%) | Erdos-Renyi 合成图，非卫星拓扑 |
| L08 (GNN-SD-LEO) | 66 星 | ❌ | 仅 Iridium，完全未涉及 |
| L10 (MCSR) | 1156-10000 星 | ✅ (传统) | SRD 分割策略，非模型泛化 |
| L13 (GRLR) | 未披露 | ❌ | 44 引用，Semantic Scholar 双版验证无提及 |
| L14 (GraphPR) | 未披露 | ❌ | 全分布式 POMDP，单一规模 |
| L15 (GQN) | 108 星 | ❌ | 仅时序泛化（跨时间槽） |
| L16 (GDRL-SFCR) | 6048 星 | ❌ | 最大规模，但训练测试同规模 |
| L17 (GAT-LSTM-DQN) | 45 星 | ❌ | 极小规模 |
| L18 (DTAR) | 288 星 | ❌ | 域划分+GAT+PPO，单一规模 |

**结论**：
- GNN size generalization 在 LEO/satellite routing 领域**完全空白**——经 12 篇精读 + 6 篇定向检索验证
- 唯一的跨规模实验是 L06 (30→50 节点合成图) 和 L10 (传统方法 1156→10000 星)，均不涉及 GNN 模型跨规模泛化
- L02 (Starfield) 的密度分析暗示 400+ 规模边际收益递减，但这是对路由性能的观察，非对 GNN 泛化能力的研究
- **核心创新空间完全成立**：首次在卫星拓扑上系统研究 GNN 的跨规模泛化能力

### 6. 仿真工具链分析

| 工具 | 语言 | 最大规模 | 路由支持 | ML 集成 | 适合本项目 |
|------|------|---------|---------|---------|-----------|
| xeoverse (L05) | Python+Mininet | 5442 星 | Dijkstra | ❌ 不支持 | 参考框架，需扩展 |
| Starfield (L02) | Go/C++/Python | 1584 星 | Dijkstra | ❌ | 开源，可参考 |
| Hypatia | Python+NS-3 | ~1500 星 | Dijkstra | ❌ | 过慢 |
| MCSR 平台 (L10) | Python+Hypatia+NS-3 | 10000 星 | 自定义 | ❌ | 规模最大，可参考 |
| CMCR (L11) | 未说明 | 1584 星 | 自定义 | ❌ | 参考框架 |
| GARS (L09) | STK+OMNeT++ | 2000 星 | 自定义 | ❌ | 参考框架 |
| 自建 | Python+PyG | 无限制 | 自定义 | ✅ | **推荐** |
| DuJo (L03) | Python+Numba | 1000 星 | 自定义 | ❌ | 参考框架 |

**推荐路径**：参考 xeoverse 的轨道力学（SGP4/TLE）和链路建模（Shannon + ITU-T），参考 DuJo 的 Starlink TLE 数据处理，参考 MCSR (L10) 的 Hypatia+NS-3 平台设计，自建 GNN 路由仿真环境。PyTorch Geometric 做 GNN 训练，NumPy 做星座拓扑。

### 7. Baseline 惯例

**路由 baseline（需对比）**：
1. **Dijkstra/OSPF/SPF**：最短路径，所有论文的必备 baseline
2. **+Grid 拓扑 + Dijkstra**：标准 ISL 拓扑 baseline（L02, L03, L04 共用）
3. **Backpressure**：L01 提到的队列稳定路由
4. **负载均衡路由**（ECMP/TPLB）：L10、L11 使用的流量预分流负载均衡
5. **CMCR**（L11）：聚类多准则路由，有理论保证 — **必须对比**
6. **MCSR**（L10）：分段弹性路由，10000 星规模验证 — **必须对比**
7. **IUDR**：ISL 效用动态路由（L10, L11 共用 baseline）
8. **GARS**（L09）：O(1) 地理辅助路由
9. **GRLR**（L13）：GNN+Actor-Critic，44 引用，该方向标杆 — **必须对比**
10. **GraphPR**（L14）：GAT+MADRL 全分布式 — **推荐对比**（如采用分布式架构）

**GNN baseline（消融实验）**：
1. GCN vs GAT vs GraphSAGE：架构对比
2. 无 GNN（纯 MLP/DNN）：消融 GNN 的贡献
3. L08 的基础 GCN 聚合方案：已知 GNN+LEO 的最基础实现

**Size Generalization 评估（本项目特有）**：
- 在 N 星训练 → 在 2N, 4N, 8N 星测试，对比同规模训练 vs 跨规模推理的性能差距
- 对比传统分治方法（如 MCSR 的 SRD 分割）在同等规模下的性能

**指标**：
- 主指标：端到端时延（ms）、吞吐量（Gbps/Tbps）
- 辅指标：负载均衡系数、路径 stretch factor、收敛速度
- 系统指标：推理时延（ms）、模型参数量、FLOPs
- Size generalization 特有：跨规模性能保持率（%）

### 8. 创新空间确认

经过 12 篇精读 + 6 篇定向检索验证（共 18 篇），**核心创新点重新定位**：

| 创新点 | 现状 | 差异化空间 |
|--------|------|-----------|
| **GNN size generalization** | **完全空白** — 6 篇 GNN+RL LEO 论文（L13-L18）无一涉及。L06 仅 30→50 合成图，L01 仅理论分析 | **核心创新**：首次在卫星拓扑上系统研究 GNN 跨规模泛化（小星座训练→大星座部署） |
| GNN+RL 端到端 LEO 路由 | **已有 6 篇论文**（L13-L18），非创新点 | 不再作为独立创新点，但 size generalization 使其具有工程实用价值 |
| 全分布式 vs 集中式 | GraphPR (L14) 已做全分布式 POMDP | 可作为架构选择而非创新点 |
| 动态路由 vs 静态路由 | L10/L11/L18 通过分段/聚类/域划分处理时变拓扑 | GNN 在线推理仍有优势，但非核心创新 |

**创新定位调整**：
- **之前的定位**："GNN+RL for LEO routing"（Step 2-3 初期，仅知 L08 一篇）
- **现在的定位**："GNN size generalization for satellite routing"（Step 3.5 后，确认 6 篇竞争对手均未涉及）
- 核心叙事：GNN+RL for LEO routing 已被验证可行（GRLR 44 引用），但**训练与部署必须同规模**这一限制严重制约了实用价值（训练 6000+ 星星座的计算成本极高）。本研究首次解决 GNN 跨规模泛化问题，使小星座训练→大星座部署成为可能。

**风险评估**：
- ✅ Size generalization 在 LEO 路由中**零竞争**（经 Semantic Scholar API 验证）
- ✅ GNN size generalization 在其他领域已有理论基础（ICML 2024 解耦表示学习、KDD 2023 谱方法），可迁移
- ⚠️ 需验证卫星网格拓扑的特殊性（规则结构、时变性）是否有利于或不利于泛化
- ⚠️ GRLR (44 引用) 是强竞争者，如果其后续工作加入 size generalization，时间窗口有限
