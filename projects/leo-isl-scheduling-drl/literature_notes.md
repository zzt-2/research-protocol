# Literature Notes — LEO ISL Scheduling + DRL

> 方向：巨型 LEO 星座中 ISL（星间链路）的建立、维护和切换如何用 DRL 在线优化
> 创建：2026-05-15 | 论文数：12 篇精读 + 3 篇浅读（Step 3.5 补充）

## 步骤进度

| 步骤 | 状态 | 日期 | Commit |
|------|------|------|--------|
| Step 1 检索 | ✅ | 2026-05-15 | — |
| Step 2 获取 | ✅ | 2026-05-15 | — |
| Step 3 精读 | ✅ | 2026-05-15 | — |
| Step 3.5 补充检索 | ✅ | 2026-05-15 | — |
| Step 4a 方向 Go/No-Go | ✅ Go | 2026-05-15 | — |
| Step 5 Baseline 确认 | ✅ | 2026-05-15 | — |
| Step 4b 执行 Go/No-Go | ✅ Go | 2026-05-15 | — |
| Step 6 §sim 设计 | ✅ | 2026-05-15 | — |
| Step 7 §impl Part A | ✅ | 2026-05-15 | a27dea4 |
| Step 7 §impl Part B | ✅ B1+B2 | 2026-05-15 | — |

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

### [L09] Optimization for Dynamic Laser Inter-Satellite Link Scheduling With Routing: A Multi-Agent Deep Reinforcement Learning Approach

- DOI/来源：10.1109/TCOMM.2023.3347775
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Communications (SCI Q1)
- **年份/会议**：2024年5月（Vol. 72, No. 5；早期版本 IEEE GLOBECOM 2023）
- 核心贡献：(1) 设计"3固定+1动态"激光ISL模式，通过可行性分析验证动态LISL建立条件（通信距离<4000km，仰角-12°~0°，方位角间隔17.9°大于盲区10°），每颗卫星可从7个候选目标或关闭中选择；(2) 提出MADRL协作式动态LISL调度算法，将全局优化目标分解为每颗卫星独立奖励函数，利用压缩感知降低状态维度，结合Double Dueling DQN、参数/经验共享和优先经验回放在720颗LEO卫星规模上实现收敛。
- 方法概述：将动态LISL调度建模为MDP，每个时隙根据链路负载状态决定下一时隙的动态链路建立/关闭。全局奖励分解为各卫星局部奖励，Double Dueling DQN + CS压缩 + 参数/经验共享 + 优先经验回放。
- 实验设置：OneWeb星座（720星/18面/1200km），K=20源/目的节点，380条数据流，每episode T=10时隙，训练50 episodes。路由由LP独立求解。
- 使用的 Baseline：
  - Fixed LISLs: 4条固定相邻链路（自实现）
  - T-shaped LISLs: 3条固定T形链路（自实现）
  - Random LISLs: T形+随机动态链路（自实现）
- 关键结论：MADRL平均跳数减少约2跳，LISL数量减少约15%；奖励分解有效性相关系数>0.98；算法在episode第2时隙内快速适应新流量。
- 与本研究关系：**直接相关** — MADRL奖励分解、CS状态压缩、参数共享策略均可借鉴，是最直接的DRL竞品之一
- 实现关键细节：gamma=0.9；epsilon: max(1-i/30, 0.05)；经验池10^6，起始训练Ns=5000；DNN推理<1ms；通信开销3245 B/卫星/时隙；Adam优化器（lr未给）
- 开源代码：无
- 验证状态：已通过学术搜索工具验证

#### 结构化提取

**状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|-----------|
| 链路负载矩阵 s_i^t | (2a+1)×(2b+1) 区域内卫星链路负载 | s_uv = 流量/容量 → [0,1] |
| 压缩后状态 \tilde{s}_i^t | D×L 矩阵 (Lin=810) | CS: \tilde{s} = Phi_0 * s，固定高斯随机矩阵 |

**动作空间**：离散，a_i^t ∈ {0,1,...,7}（7个候选目标+关闭），双向同意约束

**奖励函数**：
单卫星：$r_i^t = \frac{1}{2}\left[\sum_{j \in N(i)} \sum_{(u,v) \in P_{ij}} (s_{uv}^t - s_{uv}^{t+1}) \cdot \eta - \beta \cdot \mathbb{1}[|N(i)| > 0]\right]$

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| 3固定+1动态模式，N_LISL=4 | II-B | 每卫星最多4条ISL |
| 7个候选目标（轨道几何确定） | II-C | 动作空间限定为8选项 |
| 激光ISL干扰可忽略（角间隔1.13°时增益<0dBi） | Appendix B | 无需建模ISL间干扰 |
| 路由由LP独立求解 | III-A | 需内嵌LP求解器 |
| MEO/GEO集中训练中心 | V-C | 集中训练+分布执行 |

**网络架构**：
| 层 | 维度 | 激活 |
|-----|------|------|
| FC1 | 810→512 | ReLU |
| FC2 | 512→256 | ReLU |
| Advantage | 256→8 | 无 |
| Value | 256→1 | 无 |

优化器：Adam；Double Dueling DQN

**适配性分析**：
- 适配点(1)：奖励分解思想可直接借鉴用于ISL建立/拆除/切换的局部决策
- 适配点(2)：参数/经验共享适用于同构LEO星座大规模智能体训练
- 不适配点(1)：动作空间粗糙（8选项），不支持细粒度建立/拆除/切换三类型决策
- 不适配点(2)：路由与调度完全解耦，非端到端联合优化
- 改进方向：扩展为结构化动作空间（操作类型×目标链路），引入GNN编码拓扑

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| 激光ISL | FSO天线增益模型 | 距离≤4000km，10Gbps，对准误差1μrad，最大增益104dBi | [4] Carrizo SPIE 2020 |

---

### [L10] Dynamic Planning of Inter-Plane Inter-Satellite Links in LEO Satellite Networks

- DOI/来源：10.1109/ICC45855.2022.9838251
- **发表状态**：正式发表
- **发表渠道**：IEEE ICC 2022 (会议)
- **年份/会议**：2022, IEEE ICC
- 核心贡献：提出 MA-IILP（Multi-Agent Inter-plane ISL Planning）算法，基于MADDPG实现集中训练-分布执行的inter-plane ISL动态规划。首次将inter-plane ISL建立问题建模为POMDP，联合优化总吞吐量和ISL切换率。设计冲突惩罚机制（decision conflict discount），central trainer根据全局信息对冲突agent贡献打折扣。逐轨道训练策略缓解维度灾难。
- 方法概述：每颗卫星视为独立agent，主动决策其"正侧"inter-plane ISL的目标卫星。状态为距离集合+当前连接+速率。动作为从LoS范围内候选卫星中选一个建立ISL或保持沉默(K)。奖励为通信速率利润减去天线切换成本，经冲突惩罚折扣后全局共享。MADDPG + Gumbel-Softmax求解。
- 实验设置：极轨星座，N_m=11星/面，M={6,8,10}面，h=780km，Ka 23.28GHz，B=15MHz，EIRP=8912.5W，G/τ=8dB/K，Q=2 inter-plane收发器，T_d=300s，训练75000 episodes。
- 使用的 Baseline：
  - GIEM (Greedy Independent Experiments Matching): 贪心动态规划，引用[3]，自实现
  - GMM (Greedy Markovian Matching): GIEM扩展保持链路，引用[3]，自实现
  - GEO (Geographical matching): 纬度分区匹配，引用[3]，自实现
- 关键结论：MA-IILP相比GIEM总吞吐量提升2.8%~7.2%，ISL切换率降低30.7%~68.4%。M=10时切换率始终低于30.4%。
- 与本研究关系：**直接相关** — 最直接的DRL竞品之一，MADDPG集中训练分布执行范式可直接借鉴
- 实现关键细节：buffer 10000，batch 1024，lr=0.01，gamma=0.95，T_d=300s；冲突折扣：无冲突=1.0，冲突且速率最大=0.8，冲突且速率非最大=0.1；Gumbel-Softmax可微采样
- 开源代码：无
- 验证状态：已通过学术搜索工具验证

#### 结构化提取

**状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|-----------|
| D_i: 到下一面LoS范围内卫星距离集合 | 0~LoS距离(~5000-6000km) | 未明确 |
| L_i: 当前连接目标 | 候选集合元素或None | 离散索引 |
| R_i: 当前ISL通信速率 | 0~max data rate | 未明确 |

**动作空间**：离散，|V_i|+1（候选目标+保持沉默K），约束：仅下一面+LoS范围+无跨seam

**奖励函数**：
$$r_i = \alpha_i \cdot (\rho \cdot R_{uv} - \lambda \cdot \theta_{uv}), \quad R = \sum_{i=1}^{N_a} r_i$$
$\alpha_i$冲突折扣{1.0, 0.8, 0.1}；$\gamma=0.95$

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| FSPL+AWGN，无多径/干扰 | III.B | 仅需FSPL |
| 极轨(~90°)，seam区域无跨seam ISL | III.A | 需seam检测 |
| T_d=300s准静态 | III.B | 粗粒度，不适用秒级调度 |
| Q=2 inter-plane收发器 | III.A | 每卫星最多2条inter-plane ISL |
| 逐轨道训练，同面agent共享参数 | IV.A | 按轨道面分组训练 |

**网络架构**：
| 组件 | 层 | 维度 | 激活 |
|------|-----|------|------|
| Policy π_i | 单隐藏层FC | 未明确 | 未明确 |
| Value Q_i | 单隐藏层FC | 全局状态+动作 | 未明确 |

优化器：未明确类型，lr=0.01；MADDPG标准架构

**适配性分析**：
- 适配点(1)：MADDPG集中训练-分布执行范式可直接借鉴解决POMDP
- 适配点(2)：冲突惩罚机制可用于多卫星竞争同一ISL目标场景
- 不适配点(1)：决策粒度过粗（T_d=300s），不适用秒级ISL调度
- 不适配点(2)：动作空间为"选目标卫星"的一次性匹配，不支持建立/保持/拆除三态决策
- 改进方向：动作空间扩展为"对每条候选ISL发建立/保持/拆除指令"，GNN替代手工状态特征

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| Inter-plane ISL | FSPL+AWGN | f=23.28GHz(Ka), B=15MHz, EIRP=8912.5W, G/τ=8dB/K | 3GPP TR 38.821 |

---

### [L11] Task-Aware Distributed Inter-Layer Topology Optimization Method in Resource-Limited LEO-LEO Satellite Networks

- DOI/来源：10.1109/TWC.2023.3309379
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Wireless Communications (SCI Q1)
- **年份/会议**：2024年4月（Vol. 23, No. 4）
- 核心贡献：提出面向LEO双层卫星网络（遥感层RLS + 通信层CLS）的分布式层间拓扑优化方法DITO，基于时空关系实现分布式交互，最大化任务感知的观测收益。引入链路切换间隔约束和基于切换间隔的时隙划分方法，将非线性时序耦合问题线性化建模为ILP。500颗卫星30分钟周期下仅需1.49秒求解，接近集中式全局最优。
- 方法概述：每颗RLS建立ILP模型优化层间链路拓扑，基于六类激光可连接性约束（仰角/可见性/功率范围/仰角-方位角-功率变化率）构建潜在链路矩阵。CLS收到请求后按任务重要性排序选择（最多L_c个RLS），RLS再基于确定拓扑用LP管理流量和能量。RSW/RNC预处理降低变量规模。
- 实验设置：Walker星座（33/50/136/500星），RLS太阳同步500km，CLS倾斜/极轨1150-1200km。时隙Δτ=120s，最小有效窗口w_min=240s，周期T=30min。Gurobi+MATLAB。
- 使用的 Baseline：
  - COP: 集中式MILP全局优化（自实现，最优性上界）
  - DITO-nodif: 分布式但不区分任务重要性（自实现）
  - DITO-nopre: 分布式但不使用RSW/RNC预处理（自实现）
- 关键结论：DITO在500星/30min场景下1.49s求解（COP 12h无法解）；任务重要性带来12.4%收益提升；预处理降求解时间约16倍。
- 与本研究关系：方法可借鉴 — 六类激光可连接性约束框架和链路切换间隔约束可直接复用
- 实现关键细节：Δτ=120s，w_min=240s；RLS 500km太阳同步，CLS 1150-1200km；L_c=2；观测任务6-10min；ω归一化和为1；求解器：Gurobi(ILP)+MATLAB linprog(LP)
- 开源代码：无（MATLAB+STK+Gurobi）
- 验证状态：已通过学术搜索工具验证

#### 结构化提取

**状态空间**（非RL，ILP输入）：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|-----------|
| 可连接矩阵 S_i | {0,1}^{N_c×T} | 六类约束二值判定 |
| 任务重要性 ω_{i,t} | [0,1]，Σω=1 | 已归一化 |
| 初始缓冲区 b_{i,0} | [0, b_i^max] Gbit | 未归一化 |

**动作空间**：离散（二值），δ_i ∈ {0,1}^{N_c×T}，约束：(14)仅选可连接CLS；(15)每时隙最多连1个；(18)链路切换间隔约束

**优化目标**（非RL奖励）：
ILP: $\max_{\delta_i} \sum_{t} \sum_{j} \omega_{i,t} \cdot \delta_{i,j,t}$；LP: $\max \sum_{t} \sum_{j} \omega_{i,t} \cdot q_{i,j,t}$

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| 每RLS每时隙最多连1个CLS | III-B | 链路数上限约束 |
| CLS最多连L_c个RLS | II-C | 需全局调度机制 |
| 虚拟拓扑快照法 | II-B | 时隙内拓扑静止 |
| RLS间无层内链路 | II-A | 仅建模层间+CLS层内 |

**网络架构**：不适用（ILP+LP优化方法，Gurobi+MATLAB linprog）

**适配性分析**：
- 适配点(1)：六类激光可连接性约束模型可直接复用于ISL调度仿真器链路可行性判断
- 适配点(2)：基于链路切换间隔的时隙划分方法，将时序约束线性化的思路可借鉴
- 不适配点(1)：优化对象是层间链路（异层），非同层ISL
- 不适配点(2)：分布式交互假设RLS独立优化后CLS集中仲裁，不适用纯P2P场景
- 改进方向：将六类可连接性约束作为DRL环境的硬约束，DRL在可行链路子集中做建立/拆除/保持决策

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| RLS→CLS层间激光 | 自由空间光通信+六类约束 | ε_min, P_S^max, dΦ_max, dΨ_max, dP_S^max | 参照[20,26,28] |

---

### [L12] Dynamic Laser Inter-Satellite Link Scheduling Based on Federated Reinforcement Learning: An Asynchronous Hierarchical Architecture

- DOI/来源：10.1109/TWC.2024.3411169
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Wireless Communications (SCI Q1)
- **年份/会议**：2024年10月（Vol. 23, No. 10）
- 核心贡献：(1) 提出基于联邦MADRL的LISL调度算法，将全局调度分解为每颗卫星独立决策，平均跳数降低约2跳，LISL数量减少>25%。(2) 设计异步层次化联邦学习架构：LEO本地训练DQN→GEO部分聚合→GEO间低频全局聚合，利用LEO快速运动带来的样本分布一致性减少聚合频率。(3) 自适应模型上传方案，基于参数变化量评估层效用，凸优化选择上传贡献最大的网络层。
- 方法概述：Double DQN作为每颗LEO卫星本地RL算法，每颗卫星独立决策其inter-OP LISL建立（16种模式选1）。联邦学习三层架构：LEO本地→GEO部分聚合（每t_l次）→GEO全局聚合（每τ_p次部分聚合）。上传时以概率p_{i,l}选择性传输各层参数。
- 实验设置：Walker Delta 72星（18面×4颗），1200km/87.9°，3颗GEO，N_t=4激光终端。N_e=50时隙/episode，流量0.5-2Gbps均匀分布。DNN 6层FC（324-256-256-256-128-128-16），float16。Dijkstra路由。
- 使用的 Baseline：
  - T-shaped/Fixed/One dynamic/Random LISLs: 不同拓扑模式（自实现）
  - Centralized training: 集中训练DQN（自实现）
  - FedAvg: 单GEO全局服务器（自实现）
  - Average/Greedy/Random upload: 不同上传策略（自实现）
- 关键结论：β≥0.4时跳数降低>2跳，LISL数量减少>25%；异步层次化FL性能与集中训练一致，LEO通信开销仅46.6%；自适应上传在受限功率下优于贪心上传。
- 与本研究关系：**直接相关** — LEO ISL调度+DRL方向，联邦学习异步层次化架构可借鉴；动作空间（16选1）仍为粗粒度
- 实现关键细节：状态324维（4×81矩阵展平）；动作16种模式；奖励r_i=Σy(i,j)-β，β∈[0.1,1.0]；float16存储，总参数30,304B；DQN
- 开源代码：无
- 验证状态：已通过学术搜索工具验证

#### 结构化提取

**状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|-----------|
| 卫星局部邻域链路状态与负载 | 压缩为4×81矩阵→324维 | 未明确归一化 |

**动作空间**：离散，a_i ∈ {1,...,16}（4种inter-OP LISL选项×2个相邻OP），双向同意约束

**奖励函数**：
全局：$\min_\pi \mathbb{E}[H_0(E_e^{[n+1]}, f^{[n+1]}) + \beta |E_e^{[n+1]}|/2]$
单卫星：$r_i^{[n]} = \sum_{j \in N(i)} y^{[n+1]}(i,j) - \beta$，无显式归一化

**建模假设**：
| 假设 | 位置 | 仿真器影响 |
|------|------|-----------|
| Intra-OP LISL始终可用 | II-A | 面内链路固定 |
| Inter-OP仅4种位置选项(same/front/rear/none) | II-A | 动作空间16种模式 |
| Episode内拓扑准静态 | II-B | 按episode离散化 |
| 激光束极窄，干扰可忽略 | II-A | 无需建模干扰 |
| LISL能耗由APT机制决定，非通信功率 | II-A | 能耗用LISL数量衡量 |

**网络架构**：
| 层 | 维度 | 激活 | 存储 |
|-----|------|------|------|
| FC1-FC3 | 324→256→256→256 | 未明确(推测ReLU) | float16 |
| FC4-FC5 | 256→128→128 | 未明确 | float16 |
| Output | 128→16 | 线性 | float16 |

优化器：未明确；Double DQN，总参数30,304B

**适配性分析**：
- 适配点(1)：MADRL将全局ISL调度分解为每卫星独立MDP的范式可直接借鉴
- 适配点(2)：异步层次化FL架构（LEO→GEO聚合）为大规模训练通信开销问题提供工程可落地方案
- 不适配点(1)：动作空间粗粒度16选1，不支持逐链路建立/拆除/切换决策
- 不适配点(2)：奖励函数基于下一时隙流量负载，需路由计算反馈，实时性要求高
- 改进方向：DQN替换为GNN+DRL架构，利用图结构编码星座拓扑，扩展动作空间支持逐条ISL细粒度调度

**信道模型参数表**：
| 链路类型 | 模型 | 关键参数 | 来源 |
|----------|------|----------|------|
| LEO-GEO上传 | AWGN+Shannon | B, h_i, n_i | V-B Eq.(33) |
| Inter-OP LISL | 理想化（忽略干扰） | 容量c(u,v) | II-A |

---

## 综合分析

### 1. 现有方法分类

**A. 确定性优化（5 篇）**
- ILP/MIP + 对偶分解：DuJo (L01) — 拉格朗日对偶分解 LISL 匹配+路由+速率，K=500 迭代
- 动态规划评分：DoTD (L03) — DTEG 框架，归一化多目标评分选链
- 图论匹配：L07 — "3+1"方案 + 精英保留最大权匹配
- 贪心+可见性：LPTSO (L06) — 星载集中式，FSA 时段贪心选链
- ILP+LP：DITO (L11) — 双层LEO分布式层间拓扑优化，六类激光约束+链路切换间隔约束

**B. GNN 监督学习（1 篇）**
- DeepLaDu (L02) — GATv2 学习拉格朗日对偶乘子，单次前向推断替代迭代，subgradient-based edge-level loss 训练

**C. DRL/RL 方法（4 篇）**
- MARL + DQN：SatFlow (L05) — 分层框架，上层 MARL 做 ISL 重建（index offset），下层凸优化分配
- MADRL + Double Dueling DQN：Wang TCOM (L09) — "3固定+1动态"模式，CS压缩状态，奖励分解+参数共享，720星收敛
- MADDPG + Gumbel-Softmax：Pi ICC (L10) — inter-plane ISL规划POMDP，冲突惩罚机制，逐轨道训练
- 联邦MADRL + Double DQN：Wang TWC (L12) — 异步层次化FL架构（LEO→GEO聚合），自适应模型上传，16选1动作空间

**D. 启发式路由（1 篇）**
- ISASR (L04) — 稳定性/活跃度加权修改边代价，首次纳入 setup delay，Dijkstra 路由

**E. 管理架构（1 篇）**
- Mao 2025 (L08) — 管理域划分+低频切换，非 ISL 物理调度

### 2. 已知局限

1. **DRL 动作空间均为粗粒度**：L05/L09/L10/L12 四篇DRL论文的动作空间分别是 index offset、8选1、选目标卫星、16选1，全部是从有限候选集中选拓扑模式，无一篇支持逐链路的建立/保持/拆除三态决策
2. **DRL 网络架构简单**：四篇DRL论文全部使用 FC 网络（DQN/MADDPG），无拓扑感知能力。L09/L12 使用 Double Dueling DQN，L10 使用 MADDPG，L05 使用 GCN+MLP，均未使用图神经网络编码星座拓扑结构
3. **静态快照优化为主**：L01/L03/L06/L07/L11 为静态快照或准静态方法，L10 决策周期 300s，未真正建模 ISL 建立/切换的时序过程
4. **缺乏切换成本建模**：仅 L04 考虑 setup delay（2~30s），L10 考虑天线转向角成本，其他论文均忽略 ISL 建立/切换时延
5. **路由与调度解耦**：L09/L12 的路由由 LP/Dijkstra 独立求解，DRL 仅负责链路调度，非端到端联合优化。仅 L01/L02/DeepLaDu 做路由+ISL联合
6. **流量感知不足**：多数论文假设固定或简化流量模型，L09/L12 假设 episode 内流量分布平稳

### 3. 2-3 年趋势

1. **DRL 成为 ISL 调度研究热点**：2022 年仅 Pi ICC 1 篇（MADDPG），2024 年出现 3 篇（Wang TCOM、Wang TWC、SatFlow），DRL 从探索性尝试发展为该方向主流方法
2. **联合优化成为共识**：从单独 ISL 匹配发展到 ISL+路由+速率联合（L01/L02），ISL+功率联合（L05），或 ISL+流量+能量联合（L11）
3. **激光 ISL 全面替代射频 ISL**：2024 年后论文几乎全部针对 LISL，L09/L10/L12 均聚焦激光终端
4. **大规模训练技术出现**：L09 的参数/经验共享、L10 的逐轨道训练、L12 的联邦学习，均针对万星星座的维度灾难提出工程解决方案
5. **对偶分解+学习范式成熟**：L01→L02 建立了拉格朗日对偶分解+GNN 学习的范式，是确定性优化→学习型方法的桥梁

### 4. 研究背景概述

**领域脉络**：
- 2020-2022：ISL 拓扑管理以确定性方法为主（+Grid, Manhattan, MSN, LPTSO），关注拓扑稳定性和时延最小化。Pi (ICC 2022) 首次引入 MADDPG 做 inter-plane ISL 规划
- 2023-2024：DRL 方法爆发——Wang (TCOM 2024) MADRL+DQN 做 LISL 调度，Wang (TWC 2024) 联邦RL+DQN。Guo (TWC 2024) ILP 做双层分布式拓扑优化
- 2024-2025：对偶分解范式成熟（DuJo → DeepLaDu），GNN 监督学习实现对偶变量推断；SatFlow 引入 MARL 分层框架。确定性优化方法精化约束建模（DITO 六类约束+切换间隔）

**核心技术挑战**：
1. **决策空间爆炸**：万星星座每颗卫星 2~4 个 LCT，组合空间极大。L09 用 CS 压缩、L10 逐轨道训练、L12 联邦学习分别应对
2. **时间动态性**：ISL 可见性/质量随轨道运动持续变化，coherent time 仅 0.5~3.6s（L02），但现有 DRL 方法决策周期 300s（L10）或 episode 内静态（L09/L12）
3. **切换成本**：激光 ISL 建立/切换耗时 2~30s（L04），显著影响路由稳定性，但仅 L04/L10 显式建模
4. **在线决策延迟**：迭代优化方法耗时分钟级（L01 K=500），DeepLaDu 单次前向推断快 10⁴ 倍但为监督学习无在线探索

**本研究定位**：
- **创新空白**：现有 4 篇 DRL 工作全部使用粗粒度动作空间（从固定候选集中选拓扑模式），无一篇支持逐链路的细粒度建立/保持/拆除决策；全部使用 FC 网络，无拓扑感知
- **方法切入点**：将 DeepLaDu (L02) 的 GNN 拓扑编码 + 对偶分解框架与 DRL 在线学习结合，设计结构化动作空间支持逐链路决策（建立/保持/拆除），引入切换成本建模（借鉴 L04/L10）和时间相关性
- **竞品对标**：
  - L09 (Wang TCOM MADRL)：最直接竞品，但动作空间仅 8 选项，无 GNN，路由与调度解耦
  - L10 (Pi ICC MADDPG)：最接近的 MARL 方案，但决策粒度 300s，仅做 inter-plane 匹配
  - L12 (Wang TWC 联邦RL)：最新竞品，异步 FL 架构可借鉴，但动作空间 16 选 1，无 GNN
  - L02 (DeepLaDu)：方法可借鉴——GNN 学习对偶变量的范式是本研究的技术基础

---

## 浅读论文（Step 3.5 补充检索）

> 检索源：S2 + OpenAlex，7 组检索组合 + Wang TCOM 2024 反向引用链（36 篇）
> 关键结论：**GNN+DRL 细粒度 ISL 调度为文献空白**，所有 DRL ISL 论文均为粗粒度动作空间 + FC 网络

### [L13] GRLR: Routing with GNN and RL for Mega LEO Constellations
- DOI/来源：10.1109/TVT.2024.3471658
- 发表状态：正式发表
- 发表渠道：IEEE Transactions on Vehicular Technology
- 核心方法：Actor-Critic + GNN 做 LEO 路由优化，GNN 编码时变拓扑特征
- 与本研究关系：方法可借鉴 — GNN+RL 架构可迁移到 ISL 调度场景
- 引用定位：Related Work 中 GNN+RL LEO 路由代表（44 引用，高影响力）

### [L14] DRL-Based Multipath Routing with GNN for LEO Satellite Networks
- DOI/来源：10.3390/electronics13153054
- 发表状态：正式发表
- 发表渠道：MDPI Electronics (OA)
- 核心方法：GNN 做 ISL 状态感知 + DRL 做多路径流量调度
- 与本研究关系：**最接近 GNN+DRL ISL 调度** — GNN 感知 ISL 状态后做调度决策的范式与本方向一致
- 引用定位：Related Work 中 GNN+DRL 卫星调度代表

### [L15] GNN-MAPPO: Dynamic Resource Management and Routing for LEO Satellite Networks
- DOI/来源：10.1109/ISCEIC67854.2025.11405598
- 发表状态：正式发表
- 发表渠道：IEEE ISCEIC 2025 (会议)
- 核心方法：GCN + MAPPO 联合优化路由和资源分配，将卫星网络建模为动态图
- 与本研究关系：方法可借鉴 — GNN+MARL 架构与本研究方向高度匹配
- 引用定位：GNN+MARL 卫星网络架构参考

### Step 3.5 补充检索总结

**检索充分性**：
1. ✅ 关键词矩阵：GNN/DRL/Graph RL × ISL/topology/handover × mega constellation — 7 组组合
2. ✅ 搜索源覆盖：S2 + OpenAlex
3. ✅ 引用链分析：Wang TCOM 2024 反向引用 36 篇
4. ✅ 收敛：最后一轮无新增"必读"论文直接做 GNN+DRL ISL 调度
5. ✅ 轮次：2 轮（含初始 4 组 + 补充 3 组）

**创新空白确认**：12 篇精读 + 3 篇浅读 = 15 篇文献，无一做 GNN+DRL 细粒度 ISL 建立/拆除/切换决策。L14 最接近但仍聚焦路由而非调度。蓝海特征明确。

## Baseline 交叉验证

### Baseline 出现频率统计
| 方法名 | 被几篇论文使用 | 使用该 baseline 的论文 | 代码状态 | 推荐优先级 |
|--------|--------------|----------------------|---------|-----------|
| +Grid / Fixed LISLs | 5 篇 | L01, L03, L05, L09, L12 | 无 | 1（必选，基础拓扑） |
| Random 拓扑 | 3 篇 | L03, L07, L09 | 无 | 2 |
| OSPF / Dijkstra 路由 | 4 篇 | L01, L03, L04, L12 | Python标准 | 1（必选，基础路由） |
| MRate (最大速率匹配) | 2 篇 | L01, L02 | 无 | 2 |
| DuJo / LaDu 迭代对偶 | 2 篇 | L02 (作为 LaDu-K) | 无 | 3 |

### Baseline 候选
| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: +Grid/Fixed | L01/L09 | 自实现 | 1 | 所有论文共同基准，工业标准拓扑 |
| B2: Wang TCOM MADRL | L09 | 无（需复现） | 2 | 最直接DRL竞品，720星验证，奖励分解思想 |
| B3: Pi ICC MADDPG | L10 | 无（需复现） | 3 | 集中训练分布执行参考，但网络细节不充分 |
| B4: DeepLaDu (监督学习) | L02 | 待公开 | 2 | GNN学习对偶变量范式，本研究的技术基础 |
