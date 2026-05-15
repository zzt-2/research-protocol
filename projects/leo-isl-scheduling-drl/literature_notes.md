# Literature Notes — LEO ISL Scheduling + DRL

> 方向：巨型 LEO 星座中 ISL（星间链路）的建立、维护和切换如何用 DRL 在线优化
> 创建：2026-05-15 | 论文数：8 篇精读 + 4 篇待补充（用户手动获取）

---

## 精读论文

### [L01] Joint Laser Inter-Satellite Link Matching and Traffic Flow Routing in LEO Mega-Constellations via Lagrangian Duality

- DOI/来源：arXiv 2601.21914
- **发表状态**：预印本
- **发表渠道**：arXiv preprint
- 年份：2025
- 核心贡献：提出基于拉格朗日对偶的联合 LISL 匹配与流量路由优化方法（DuJo），将 NP-hard MIP 通过松弛链路速率约束分解为三个子问题——最大权匹配（MWM）用于 LCT 连接、加权最短路径用于路由、线性规划用于速率分配。次梯度下降迭代优化拉格朗日乘子，乘子反映卫星对间拥塞权重。证明乘子和次梯度有界性，保证收敛。
- 方法概述：将 LCT 连接决策、流量路由和速率分配通过对偶松弛解耦，次梯度迭代调整乘子直至收敛，转换为可行方案。每次迭代复杂度多项式级。
- 实验设置：Starlink 真实 TLE（UTC 2025-07-16），1000 颗卫星，每颗 2 个 LCT，100 个地面网关，用户分布基于 GHS-POP。Python+Numba JIT，HiGHS 求解 LP。
- 使用的 Baseline：
  - +Grid：网格对齐优先匹配
  - Rand：随机匹配
  - MRate：最大链路速率匹配
  - OSPF：最短路径路由
- 关键结论：DuJo 相比 Grid/Rand 提升吞吐量 ~145%，相比 MRate 提升 ~35%。β=0.5 性能最优，K=500 次迭代近似收敛。Starlink 等复杂星座中 DuJo 优势显著。
- 与本研究关系：**直接相关** — ISL 建立和路由联合优化，传统优化方法，可借鉴问题建模和 baseline 设计
- 实现关键细节：步长 α^{[k]} = α₀/k^β，β=0.5，K=500；乘子初始化 λ^{[1]}=0；MWM 贪心匹配；路由 Dijkstra
- 开源代码：无（"upon acceptance"）

#### 结构化提取

**状态空间**（非 DRL，等价决策变量）：
| 决策变量 | 维度 | 约束 |
|----------|------|------|
| c_{n,m}（LCT 连接） | \|E\| 维，{0,1} | 对称，每 LCT 恰好连一个对端 |
| q^{s,s'}（流量速率） | \|F\| 维，≥0 | 受限于服务/需求速率 |
| x_{i,j}^{s,s'}（路由） | \|L\|×\|F\|，{0,1} | 流守恒 |
| λ_{i,j}（对偶乘子） | \|L\| 维，≥0 | 初始化为 0 |

**动作空间**：不适用（非 DRL）

**奖励函数/优化目标**：
$$\max_{\mathbf{c}, \mathbf{q}, \mathbf{x}} \sum_{(s,s') \in \mathcal{F}} q^{s,s'}$$

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| 卫星对地定向，LCT 方向固定 | II-B | 简化 LCT 指向计算 |
| 指向抖动 Rayleigh 分布，σ_J=10μrad | II-B Eq.(2) | 影响链路容量计算 |
| 理想捕获跟踪 | II-C | 忽略建链时延 |
| 仅下行流量 | II-D | 未建模双向流量 |
| 静态时间快照 | III 全文 | 未考虑时间动态 |

**网络架构**：不适用（非 DRL）。算法：MWM(O(E log E)) + Dijkstra(O(I·E·log N)) + LP(HiGHS)

**适配性分析**：
- 适配点(1)：LISL 匹配+路由的联合优化问题建模可直接转化为 DRL 的 MDP
- 适配点(2)：Gaussian beam 信道模型（含指向抖动、中断概率）可直接复用于仿真
- 不适配点(1)：静态快照优化，无时间动态，DRL 需处理时变拓扑
- 不适配点(2)：不考虑 ISL 建立/切换时延和信令开销
- 改进方向：将对偶分解框架与 GNN/DRL 结合，用 GNN 学习拉格朗日乘子预测，避免 K=500 次迭代

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| LISL | Gaussian beam + OOK | λ=1.55μm, W₀=9.87×10⁻³m, P₀=20W, B=1GHz | II-C Eq.(3)-(5) |
| LISL 接收 | 孔径接收+热噪声 | A=0.01m², Ψ=0.5A/W, σ_N=3×10⁻⁷A | II-C Eq.(5) |
| LISL 指向抖动 | Rayleigh | σ_J=10μrad | II-B Eq.(2) |
| LISL 中断约束 | Outage-based | ε=0.001 | III-D Eq.(20)-(21) |
| LISL 连接约束 | 距离+FOR | z_max=3000km, θ=60° | III-A Eq.(8) |

---

### [L02] Duality-Guided Graph Learning for Real-Time Joint Connectivity and Routing in LEO Mega-Constellations

- DOI/来源：无 DOI（手动下载）
- **发表状态**：未知（疑似已投稿/刚接收）
- **发表渠道**：疑似 IEEE Transactions（双栏格式）
- 年份：2025/2026
- 核心贡献：提出 DeepLaDu 框架，用 GATv2 GNN 直接从星座状态推断边级拥塞价格（拉格朗日乘子），替代迭代对偶更新，单次前向传播获得近最优决策。Starlink 级星座中提升最高 20% 吞吐量，计算时间比迭代对偶快 4 个数量级。
- 方法概述：将联合 LISL 连接+路由+流率分配建模为 MIP，对偶松弛后 GATv2 GNN 接收节点/边特征输出拥塞价格 λ∈[0,1]，subgradient-based edge-level loss 训练（非 graph-level reward）。推理后 MWM→Dijkstra→LP 三步获得方案。
- 实验设置：Starlink TLE（2025-07-16），I∈{500,750,1000,1250,1500} 颗卫星，每颗 2 个 LCT，P₀=20W，Intel Ultra 9 + RTX 5090。
- 使用的 Baseline：
  - PG：Policy Gradient GNN（自实现）
  - DDPG：Actor-Critic GNN（自实现）
  - LaDu-K：迭代次梯度对偶（K=5~500，前作）
  - MRate/+Grid/Rand：启发式匹配+OSPF
  - SaTE：非联合优化
- 关键结论：DeepLaDu 相比启发式提升 20%~100% 吞吐量，与 LaDu-100 性能相当但快 10⁴ 倍。PG/DDPG 因 graph-level reward 信号粒度不足，性能显著差。星座 coherent time ~0.5~3.6s。
- 与本研究关系：**直接相关** — GNN 学习对偶变量指导 ISL 调度，与 ISL 调度+DRL 方向高度契合
- 实现关键细节：SGD lr=10⁻³, β=0.7 衰减；GATv2 4 heads 64 dim；3 层 MLP 隐层 64，输出 sigmoid
- 开源代码：承诺开源（github.com/zhouyou-gu），目前未公开

#### 结构化提取

**状态空间**（GNN 输入）：
| 特征 | 维度 | 归一化 |
|------|------|--------|
| 节点 [s_i, d_i]（供给/需求率） | 2 维 | 未明确 |
| 边 R_{i,j}（聚合链路容量） | 标量 | 未明确 |

**动作空间**：连续，边级 λ_{i,j}∈[0,1]，sigmoid 输出

**奖励函数**：subgradient-based loss（非 RL reward）
$$L(\mathbf{w}) = -\mathbb{E}_{\Gamma}[g(\lambda|G_{SAT}, G_{LCT})]$$

**网络架构**：
| 组件 | 层 | 维度 | 激活 |
|------|-----|------|------|
| NEF | 线性 | 2→64 | ReLU |
| EEF | 线性 | 1→64 | ReLU |
| GATv2 × L | 4-head | 64/head | LeakyReLU |
| ROF | 3 层 MLP | 64→64→64→1 | ReLU+Sigmoid |
| 优化器 | SGD | α₀=10⁻³, β=0.7 | — |

**适配性分析**：
- 适配点(1)：GNN 学习对偶变量指导 ISL 调度的范式可直接迁移
- 适配点(2)：准静态 ~1s 决策窗口与 ISL 调度频率一致
- 不适配点(1)：非 DRL，监督学习无环境交互/探索
- 不适配点(2)：无切换/切换成本建模
- 改进方向：将对偶分解+GNN 框架嵌入 DRL loop，学习对偶变量生成策略

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| LISL | Gaussian beam + Rayleigh jitter | P₀=20W, λ=1.55μm, A=0.01m², σ_J=10μrad, ε=10⁻³, θ=60°, ẑ=3000km | III-A.2, Appendix |

---

### [L03] Time-Dependent Network Topology Optimization for LEO Satellite Constellations

- DOI/来源：arXiv 2501.13280
- **发表状态**：预印本
- **发表渠道**：arXiv（投稿中）
- 年份：2025
- 核心贡献：提出 Dynamic Time-Expanded Graph (DTEG) 框架，将 LEO 拓扑优化转化为时间依赖评分函数优化。每颗卫星基于归一化多目标评分（容量/时延/链路抖动）选择最优 U=4 条 ISL。DoTD 算法利用轨道可预测性预计算未来 T=10 分钟评分，动态规划递推历史评分。证明评分函数有界，O(M²) 复杂度。
- 方法概述：多目标优化转化为归一化评分函数，每颗卫星按评分在可见且通信距离内的卫星中选 top-U。DTEG 分层图表示未来时间步通信可能性，评分融合历史实现时间一致性。路由层用 OSPF。
- 实验设置：Starlink 真实 TLE（2024-06-10），907 颗卫星，5 个 GS 源-目的对，Mininet 仿真 3h20min，xeoverse+MATLAB。
- 使用的 Baseline：
  - Greedy：DoTD 一阶退化，仅看当前时间步
  - +Grid：默认 ISL（2 同轨 + 2 跨轨）
- 关键结论：vs Greedy：容量+28%，跳数-11%，时延-40%；vs +Grid：容量最高+70%，时延最高-97%。OSPF 路由。
- 与本研究关系：**直接相关** — LEO ISL 拓扑优化核心文献，评分框架和归一化方法可借鉴用于 DRL 奖励设计
- 实现关键细节：U=4 端口；w₁=w₂=0.4（容量/时延），链路抖动 0.2；归一化到 [0,1]；τ=1s，T=10min；12GHz Ku 频段
- 开源代码：有 — SpaceNet (github.com/FarzadMehri/SpaceNet)

#### 结构化提取

**状态空间**：
| 维度 | 范围 | 归一化 |
|------|------|--------|
| 星间距离 D_{i,j,t} | [0, 7000km] | 不归一化 |
| 网络容量 S_{i,j,t} | (0, S_Max] | S̄=S/S_Max → [0,1] |
| 传播时延 L_{i,j,t} | (0, L_Max] | L̄=L/L_Max → [0,1] |
| 链路抖动 φ_{i,j,t-1} | {0,1} | φ̄=φ/U → [0,0.25] |
| 可见性 Γ_{i,j,t} | >Γ_Atmos | 约束条件 |

**动作空间**：离散，每颗卫星选至多 U=4 条 ISL，约束：总连接≤U，双工，可见性，距离<D_Max

**评分函数**：
$$A_{i,j,t} = w_1 \bar{S}_{i,j,t} + w_2(1-\bar{L}_{i,j,t}) + (1-w_1-w_2)\bar{\phi}_{i,j,t-1}$$

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| GS-LEO 为 LoS，无多径 | II-B | 无需多径模型 |
| ISL 为自由空间损耗 | II-C | 仅需 FSPL |
| 固定发射功率 | II-B | 无功率控制 |
| 静态节点集 | III-A | 无卫星故障 |

**适配性分析**：
- 适配点(1)：多目标评分归一化框架可直接迁移到 DRL 奖励设计
- 适配点(2)：ISL 拓扑优化约束建模方法为 DRL 动作空间提供完整约束集
- 不适配点(1)：确定性优化，无法处理突发流量等不可预测场景
- 不适配点(2)：O(M²) 随星座规模增长，GNN+DRL 可更好扩展
- 改进方向：将评分函数作为 DRL 奖励基础，结合 GNN 捕获拓扑结构

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| GS↔LEO | LoS FSPL+天气衰减 | f=12.2GHz, B=100MHz, G_GS=33.2dBi, G_LEO=40dBi | II-B, Table I |
| ISL | FSPL+极化/对准损耗 | f=12.2GHz, Los_Pol=4.5dB, Los_Mis=0.5dB, D_Max=7000km | II-C, Table I |
| 可见性 | 高度模型 | Γ_Atmos=R_e+50km | II-C Eq.(6) |

---

### [L04] On-Demand Routing in LEO Mega-Constellations with Dynamic Laser Inter-Satellite Links

- DOI/来源：arXiv 2406.01953
- **发表状态**：正式发表（IEEE 期刊）
- **发表渠道**：IEEE Transactions on Aerospace and Electronic Systems
- 年份：2024
- 核心贡献：首次将 LISL 建立延迟（setup delay）纳入路由优化目标函数，建立 INLP→ILP 模型。提出三种启发式算法（ILPR/ALPR/ISASR）以不同性能-复杂度权衡求解。在 Starlink 1584 星上证明 ISASR 在所有 setup delay 范围内最优。
- 方法概述：虚拟拓扑快照模型，边代价=传播延迟+1ms 节点延迟，路由切换引入 setup delay 惩罚。ISASR 修改边代价加入稳定性/活跃度加权，每时隙重算 Dijkstra。
- 实验设置：Starlink Phase I v2（1584 星/24 轨/66 星），550km/53°，LISL range 1500km，N=600 时隙（每隙 1s），STK+Python。
- 使用的 Baseline：ILSR（每时隙 Dijkstra）
- 关键结论：中高 setup delay 下 ISASR 最优；高时重稳定、低时重最短路由；gamma 与 setup delay 成正比时接近最优。
- 与本研究关系：**直接相关** — setup delay 建模框架可直接嵌入 DRL 环境 reward 惩罚项；Starlink 参数基准可复用
- 实现关键细节：节点延迟=1ms；LISL range 1500km；setup delay 1ms~1000ms 参数扫描；ISASR gamma=eta_s
- 开源代码：未提及

#### 结构化提取

**状态空间**：边传播延迟、节点延迟(1ms)、边存在性、活跃链路集合、setup delay 参数、稳定性/活跃度代价

**动作空间**：路由选择（离散组合），每时隙一条路由

**目标函数**：
$$\eta_{LE} = \underbrace{\sum_{i=1}^{N}\sum_{r} \delta_r^{[i]} \alpha_r^{[i]}}_{\text{delay}} + \underbrace{\eta_s \sum_{i=1}^{N-1}(1 - \sum_{r} \alpha_r^{[i]}\alpha_r^{[i+1]})}_{\text{penalty}}$$

**适配性分析**：
- 适配点(1)：setup delay 建模可直接作为 DRL reward 惩罚项
- 适配点(2)：星座参数基准（1584 星/24 轨/550km/1500km LISL）
- 不适配点：纯确定性算法，单源-单目的假设过于简化
- 改进方向：DRL agent 替代 ISASR 启发式，学习自适应平衡 delay 与切换率

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| LISL | 自由空间光传播 | range 1500km, 容量 tens of Gbps, setup 2~30s | [9][13] |
| GS-卫星 | 光链路 | GS range 1000km | [13] |

---

### [L05] SatFlow: Scalable Network Planning for LEO Mega-Constellations

- DOI/来源：arXiv 2412.20475
- **发表状态**：预印本（IEEE ICNP 投稿）
- **发表渠道**：IEEE International Conference on Network Protocols
- 年份：2024
- 核心贡献：提出分布式分层网络规划框架，上层用时序图学习辅助的多智能体 DRL（DQN）做 ISL 重建决策，下层用分布式 Lagrangian 交替步法做流量和功率分配。首次考虑激光终端功率精细调节。
- 方法概述：上层每 D_i=1200s 用 MARL 选择 ISL 连接方案（index offset），下层每 D_e=30s 用分布式凸优化分配可分流量和功率。状态用 LINE 预训练图嵌入+GCN 聚合，动作为离散 index offset 候选集。
- 实验设置：Starlink Shell A/B + Kuiper，PyEphem 仿真 7200s，功率 4W，23.28GHz K-band。
- 使用的 Baseline：SP-F/SP-D（流量分配）；+Grid/GEO/CapOpt/RS（ISL 重建）
- 关键结论：SatFlow 降低 FVR 最高 21%，总成本降低最高 89.4%，吞吐量平均高 8~10%。推理延迟 Jetson TX2 <5ms。
- 与本研究关系：**直接相关** — MARL 做 ISL 重建，分布式分层框架，多智能体分组策略
- 实现关键细节：DQN 1000 episodes, γ=0.95, batch=256, Adam lr=0.0025; GCN 2 层 (S=40, C₀=32, C₁=16); MLP 2 层 (M₀=20)
- 开源代码：未提及

#### 结构化提取

**状态空间**：
| 维度 | 描述 | 归一化 |
|------|------|--------|
| LINE 节点嵌入 d_j^t | 时序加权最大数据速率 | 时序加权归一化 |
| LINE 节点嵌入 f_j^t | 源-目的流数据速率 | 时序加权归一化 |
| 切换成本向量 s_j^t | 各候选 offset 的 ISL 切换成本 | 否 |

**动作空间**：离散，W 个候选 index offset，同组卫星统一选择

**奖励函数**：
$$r^t = \alpha(1 - \tilde{r}_E^t) + \beta(1 - \tilde{r}_s^t)$$
归一化到 [0,1]，α+β=1

**网络架构**：
| 组件 | 层 | 维度 | 激活 |
|------|-----|------|------|
| 图嵌入 | LINE（预训练） | S=40 | — |
| GCN×2 | 图卷积 | 40→32→16 | ReLU |
| MLP×2 | 全连接 | N_s·16+W → 20 → W | ReLU |

**适配性分析**：
- 适配点(1)：MARL 分组策略有效解决巨型星座动作空间爆炸
- 适配点(2)：LINE 预训练+GCN 聚合的状态表示适合动态星座拓扑
- 不适配点(1)：下层用凸优化非 DRL，无法处理非凸约束
- 不适配点(2)：不涉及用户接入调度
- 改进方向：端到端 DRL 框架，扩展到 ISL+流量+接入统一调度

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| ISL | FSPL+Shannon | f=23.28GHz, B=15MHz, P_max=4W, EIRP_max=53dBW | [40][22][21] |

---

### [L06] Onboard Centralized ISL-Building Planning for LEO Satellite Constellation Networks

- DOI/来源：10.3390/electronics12030635
- **发表状态**：正式发表（OA）
- **发表渠道**：MDPI Electronics
- 年份：2023
- 核心贡献：首次提出星载集中式 ISL 建链规划方案，LPTSO 算法将 ILP 复杂度从 O(2^{N²K}) 降至 O(N²K)，50MHz CPU 上 N=32、K=32 时 <1 秒。以天线为对象的多天线可见性计算，考虑安装角、转台旋转阈值和卫星姿态。
- 方法概述：轨道外推计算天线间可见性矩阵→最长覆盖时间策略选择首选链路伙伴→FSA 时段内选最晚断裂链路。面内 ISL 永久环状连接，面间 ISL 由 LPTSO 动态规划。
- 实验设置：Walker Delta 32/4/1（小）和 500/20/1（大）；每颗 4 个 ISL 终端；FSA 时段 300s；星载 50MHz CPU。
- 使用的 Baseline：MSN（Manhattan Street Network）、LCTS（Longest Coverage Time）
- 关键结论：LPTSO 平均 ISL 持续 3168s，拓扑稳定；32 星平均时延 2.74 跳；500 星 89% 建链率。
- 与本研究关系：直接相关 — 面间 ISL 建链规划的确定性低复杂度方法，可见性建模框架可参考
- 实现关键细节：Walker Delta 32/4/1, 半长轴 8500km; 每卫星 4 ISL 终端; FSA=300s; ILP 权重 l/h/m/s
- 开源代码：无

#### 结构化提取

**状态空间**：轨道根数、ISL 终端健康状态、天线安装参数、卫星姿态 → 可见性布尔矩阵 V∈{0,1}^{N×N×K}

**动作空间**：建链布尔矩阵 T∈{0,1}^{N×N×K}，约束：每天线同时最多 1 条面间链路，仅相邻面建链

**优化目标**：
$$\min_T \sum_{k=1}^{K}(l \cdot p_k + h \cdot q_k + m \cdot h_{k,\max} + s \cdot h_{k,\text{mean}})$$

**适配性分析**：
- 适配点(1)：可见性建模框架（地球遮挡+转台角约束+链路长度阈值）可直接复用于 RL 环境
- 适配点(2)：建链约束体系（天线级粒度、多天线、相邻面限制）为 RL 动作空间设计提供参考
- 不适配点(1)：确定性贪心无法处理流量感知等动态目标
- 不适配点(2)：集中式架构有单点故障风险
- 改进方向：用 DRL agent 替换贪心决策，实现流量感知动态 ISL 调度

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| ISL 可见性 | 几何模型（地球遮挡+视线） | 转台半角 89°，链路长度阈值（由链路预算确定） | Eq.(15)(16) |
| 轨道 | 开普勒力学 | a=8500km(小)/8059km(大), e=0, i=60°/55° | Table 1/4 |
| 时延 | 跳数度量 | 端到端=转发+ISL 传播 | Eq.(27)(28) |

---

### [L07] A Flexible Topology Control Strategy for Mega-Constellations via ISL Based on Dynamic Link Optimization

- DOI/来源：10.3390/aerospace11070510
- **发表状态**：正式发表（OA, CC BY 4.0）
- **发表渠道**：MDPI Aerospace
- 年份：2024
- 核心贡献：提出"3+1"动态拓扑控制方案：3 条静态固定 ISL（2 同轨+1 跨轨）+1 条动态临时 ISL。设计基于精英保留策略的一般图最大权匹配算法优化动态链路分配。
- 方法概述：固定链路基于角速度/角加速度最小化选择，动态链路建模为一般图最大权匹配，权重为可连接持续时间。精英保留策略：将已连接对的权重恢复为初始最大值，避免频繁切换。
- 实验设置：Walker 1584/24/11, 550km, 53°（Starlink Phase 1），仿真步 3s。
- 使用的 Baseline：贪心算法、一般图最大权匹配（无精英保留）
- 关键结论：精英保留策略平均链路持续 429s（vs 贪心 24s），拓扑变换仅 39 次。延迟 49.88ms vs Manhattan 52.27ms。
- 与本研究关系：直接相关 — "3+1"模型和约束条件可作 DRL 状态/约束参考，精英保留思想可启发奖励设计
- 实现关键细节：动态链路距离上限 1620.06km；角速度上限 0.5°/s；最大可见距离 5168.4km
- 开源代码：无

#### 结构化提取

**适配性分析**：
- 适配点(1)：约束条件（距离<1620km、角速度<0.5°/s）可作为 DRL 约束参考
- 适配点(2)：精英保留策略隐含"稳定性激励"，可转化为连续性奖励项
- 不适配点：仅传播延迟，未考虑流量负载，星座规模固定
- 改进方向：将约束和稳定性目标融入 DRL 环境

**信道模型参数表**：
| 参数 | 值 | 来源 |
|------|-----|------|
| 轨道高度 | 550km | Starlink Phase 1 |
| 最大可见距离 | 5168.4km | 几何推导 |
| 动态链路距离上限 | 1620.06km | 固定链路最大距离 |
| 角速度上限 | 0.5°/s | 动态链路约束 |

---

### [L08] Dynamic Management Topology Construction, Evolution, and Maintenance of LEO Mega-Constellation

- DOI/来源：10.34133/space.0248
- **发表状态**：正式发表
- **发表渠道**：Space Science and Technology (BIT Press)
- 年份：2025
- 核心贡献：提出基于分布式管理域的 LEO 巨型星座管理拓扑方法。均匀排列中心节点，基于 RAAN+真近点角划分管理域。几何预测切换策略使 1 个月内平均每小时仅 5.9 颗卫星切换（vs SDA 的 375.9 颗）。
- 方法概述：SDN 架构划分管理域，中心节点通过平行+同轨推导排列。成员归属由复合性能函数（距离+切换频率）确定。切换时间通过球面几何解析预测。
- 实验设置：Starlink 1248 星（72 面, 550km, 53°），J2 摄动，81 个管理域，管理周期 1 个月。
- 使用的 Baseline：SDA（最短路径动态分配）
- 关键结论：初始域内时延 4.8ms，维护后 4.7~7.8ms；93.6% 卫星月内切换≤3 次；419 颗从未离开初始域。
- 与本研究关系：方法可借鉴 — 管理域可作 ISL 调度粗粒度单元，低频拓扑更新策略可减少 DRL 策略不稳定
- 实现关键细节：管理域半径 R_m=2506.96km，81 个域（9×9），每域~15 星，解析切换预测
- 开源代码：无

#### 结构化提取

**适配性分析**：
- 适配点：管理域划分可降低 DRL 状态空间维度（81 域 vs 1248 星），低频拓扑更新策略可借鉴
- 不适配点：不涉及具体 ISL 物理层和流量路由，非 DRL 方法
- 改进方向：将管理域作为 ISL 调度的分层基础，域间 ISL 由 DRL 决策

**信道模型参数表**：
| 参数 | 值 | 来源 |
|------|-----|------|
| 管理域半径 | 2506.96km | 由 d_max 确定 |
| 可见距离 | d_vis=2√((r+H)²-r²) | Eq.(3) |
| 轨道传播 | J2 摄动 | 单一摄动项 |

---

## 待补充论文（用户手动获取后追加精读）

- [L09] Wang TCOM 2024 — MADRL 激光 ISL 调度 (DOI: 10.1109/TCOMM.2023.3347775)
- [L10] Pi ICC 2022 — MADDPG ISL 规划 (DOI: 10.1109/ICC45855.2022.9838251)
- [L11] Guo TWC 2024 — 分布式拓扑优化 (DOI: 10.1109/TWC.2023.3309379)
- [L12] Wang TWC 2024 — 联邦 RL 激光 ISL (DOI: 10.1109/TWC.2024.3411169)

---

## 综合分析

### 1. 现有方法分类

**A. 确定性优化（5 篇）**
- ILP/MIP + 分解：DuJo (L01) — 拉格朗日对偶分解 LISL 匹配+路由+速率，K=500 迭代
- GNN 监督学习：DeepLaDu (L02) — GATv2 学习对偶乘子，单次前向推断替代迭代
- 动态规划评分：DoTD (L03) — DTEG 框架，归一化多目标评分选链
- 图论匹配：L07 — "3+1"方案 + 精英保留最大权匹配
- 贪心+可见性：LPTSO (L06) — 星载集中式，FSA 时段贪心选链

**B. DRL/RL 方法（1 篇）**
- MARL + DQN：SatFlow (L05) — 分层框架，上层 MARL 做 ISL 重建，下层凸优化分配

**C. 启发式路由（1 篇）**
- ISASR (L04) — 稳定性/活跃度加权修改边代价，Dijkstra 路由

**D. 管理架构（1 篇）**
- Mao 2025 (L08) — 管理域划分+低频切换，非 ISL 物理调度

### 2. 已知局限

1. **静态快照优化为主**：L01/L02/L03/L06/L07 均为静态时间快照优化或准静态方法，未真正建模 ISL 建立/切换的时序决策过程
2. **DRL 应用极少**：仅 SatFlow 使用 MARL，且仅做 ISL 重建（index offset），未涉及细粒度的链路建立/拆除/切换决策
3. **缺乏切换成本建模**：仅 L04 考虑 setup delay，其他论文均忽略 ISL 建立/切换时延和信令开销
4. **流量感知不足**：多数论文假设固定或简化流量模型，未考虑动态负载均衡
5. **规模限制**：LPTSO 仅验证 500 星，DuJo/DeepLaDu 验证 1000-1500 星，缺乏万星级验证

### 3. 2-3 年趋势

1. **从确定性优化到学习型方法**：2022-2023 以 ILP/图论/贪心为主，2024-2025 出现 GNN 监督学习（DeepLaDu）和 MARL（SatFlow），趋势明确向 ML 方向发展
2. **联合优化成为主流**：从单独 ISL 匹配发展到 ISL+路由+速率联合优化（DuJo/DeepLaDu），或 ISL+功率联合（SatFlow）
3. **激光 ISL 成为焦点**：2024 年后论文几乎全部针对激光/LISL，射频 ISL 逐渐退出主流
4. **对偶分解范式**：L01 和 L02 共同建立了拉格朗日对偶分解 + 学习的范式，可能是 ISL 调度的发展方向

### 4. 研究背景概述

**领域脉络**：
- 2020-2022：ISL 拓扑管理以确定性方法为主（+Grid, Manhattan, MSN），关注拓扑稳定性和时延最小化
- 2022-2023：Pi (ICC 2022) 引入 MADDPG 做 ISL 规划，首次尝试 DRL 化
- 2023-2024：Wang (TCOM 2024) 提出 MADRL 激光 ISL 调度，Guo (TWC 2024) 做分布式拓扑优化
- 2024-2025：拉格朗日对偶分解范式成熟（DuJo → DeepLaDu），GNN 监督学习实现对偶变量推断；SatFlow 引入 MARL 分层框架

**核心技术挑战**：
1. **决策空间爆炸**：万星星座每颗卫星 4 个 LCT，组合空间极大
2. **时间动态性**：ISL 可见性/质量随轨道运动持续变化，coherent time 仅 0.5~3.6s
3. **切换成本**：激光 ISL 建立/切换耗时 2~30s（当前技术），显著影响路由稳定性
4. **在线决策延迟**：迭代优化方法（K=500 迭代）耗时分钟级，无法满足秒级决策需求

**本研究定位**：
- **创新空白**：现有 DRL 工作仅做粗粒度 ISL 重建（SatFlow 的 index offset），缺乏细粒度的在线 ISL 建立/拆除/切换决策
- **方法切入点**：将 DeepLaDu 的对偶分解+GNN 范式与 DRL 在线学习结合，用 DRL agent 学习对偶变量生成策略（同时引入切换成本和时间相关性建模）
- **竞品对标**：Wang TCOM 2024 (MADRL) 和 Pi ICC 2022 (MADDPG) 是最直接的 DRL 竞品，需手动获取后详细对比
