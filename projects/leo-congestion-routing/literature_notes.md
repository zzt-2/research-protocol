# Literature Notes: leo-congestion-routing

> GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座

## 步骤进度

| 步骤 | 状态 | 日期 | Commit |
|------|------|------|--------|
| Step 1 检索+初筛 | ✅ 完成 | 2026-05-16 | TBD |
| Step 2 论文获取 | ✅ 完成 | 2026-05-16 | TBD |
| Step 3 精读 | ✅ 完成 | 2026-05-16 | TBD |
| Step 3.5 定向补充 | ✅ 完成 | 2026-05-16 | TBD |
| Step 4a 可行性预判 | ✅ 完成 | 2026-05-16 | TBD |
| Step 5 Baseline选定 | ✅ 完成 | 2026-05-16 | TBD |
| Step 4b 执行可行性 | ⬜ | | |
| Step 6 仿真器设计 | ⬜ | | |
| Step 7 Baseline复现 | ⬜ | | |

## Step 1 检索结果摘要

### 检索策略
- R1: 4 组关键词（GNN+congestion+satellite, GNN+load balancing+satellite, GNN+congestion general, non-GNN congestion+LEO）
- R1 已有方向侦察结果补充（3 个相关文件）
- R2: 2 组定向检索（size generalization+TE, GNN congestion adaptive routing）

### 质量统计
- 去重前: 180 条（R1 7文件）+ 50 条（R2 2文件）
- 去重后: 87 条独立论文
- 必读 15 / 建议读 20 / 待确认 6 / 备选 9 / 排除 37
- 正式发表占比: ~70%
- 覆盖子方向: GNN+LEO路由, GNN+负载均衡(通用), LEO拥塞控制(非GNN), GNN+TE

### 核心空白确认

**"GNN + 拥塞感知路由 + LEO"三角交集区**：有论文但无直接竞品做 per-link 负载均衡决策。

最接近竞品：
| 论文 | 方法 | 与本研究的差异 |
|------|------|---------------|
| GNN-ASSSP (He 2026) | GAT+Transformer, congestion-aware edge weights | per-edge weight learning，非 per-link 负载均衡决策 |
| GMR (Huang 2024, TVT, 41cit) | GNN multipath TE | per-path traffic splitting，非 per-link |
| DTAR (Zhou 2026) | GAT+PPO domain routing | 域间路由，非全网 per-link |
| DLBR (Ju 2025, TAES) | GCN+LSTM+DRL load balancing | GNN 仅用于流量预测，非路由决策 |

**Size generalization × 拥塞路由交叉**：完全真空。无任何论文同时涉及 GNN size generalization 和拥塞感知路由/TE。这是 thesis 框架一致性的关键空白，也是潜在核心贡献。

### 关键风险

**[已继承] leo-resilient-routing MVE 两次证明 GNN ≈ MLP for routing decisions。**
新方向的核心赌注：拥塞/负载信息需要全局聚合（不同于纯拓扑路由），GNN message passing 在这个维度上有优势。
必须在 Step 4a MVE 中优先验证此假设。

---

## Step 3 精读提取

### [L01] GRLR: Routing With Graph Neural Network and Reinforcement Learning for Mega LEO Satellite Constellations

- DOI/来源: 10.1109/TVT.2024.3471658
- **发表状态**: 正式发表
- **发表渠道**: IEEE TVT (SCI Q1)
- 年份/会议: 2025, Vol.74, No.2
- 核心贡献: 提出 GRLR 分布式路由算法，GAT 作为特征提取网络与 Actor-Critic RL 框架结合，在 mLEO 星座中实现分布式智能路由。地面站集中训练、卫星分布式执行，仅依赖局部 6 节点子图状态做逐跳决策。RLR（FC 替换 GAT）消融验证了 GNN 的结构优势。
- 方法概述: 路由建模为 MDP，每颗卫星构建以自身为中心的 6 节点有向子图，GAT 聚合邻居特征，经 GraphNorm + GlobalAddPool 后输入 FC+Softmax 决策网络，输出 4 方向动作概率。奖励为负单跳时延。
- 实验设置: 720 卫星(36×20), 570km walker-delta; STK 轨道模型; 流量 U(0,300) packets, 热点区 U(100,300); ISL 100MHz/2W/3GHz; 5 seeds
- 使用的 Baseline 方法:
  - CR: Dijkstra 全局最短时延（理想上界）
  - DR: DRA (Ekici 2001) 分布式最小跳数
  - DisCoRoute: (Stock 2022) 分布式最小距离路径
  - RLR: 同框架 FC 替换 GAT（消融对照）
- 关键结论: GRLR 收敛远快于 RLR（~50 episode），延迟介于 CR 和 DR 之间，能绕热点自适应重路由（多跳但总延迟更低）
- 与本研究关系: 直接相关 — GNN+RL LEO 路由，验证 GNN>FC，但分布式逐 hop 4 选 1 与本研究 per-link 负载均衡粒度不同
- 实现关键细节: 奖励 r_t = -delay(i,j)，到达 ε1/超时 -ε2（具体值未给）；折扣 γ、熵系数 β 未给；Actor GAT(64)→GraphNorm→Pool→FC(64,4)→Softmax; Critic GAT(32)→...→FC(32,1); Adam
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 节点特征 [lat,lon,λ_i,d,P_out] 5 维，构建 6 节点子图；未归一化（使用 GraphNorm 层）
2. **动作空间**: 离散 4 选 1（同轨±1, 邻轨±1）；边界 ISL 不存在时非法
3. **奖励函数**: $r_t = -d_k = -(t_q + t_t + t_p)$，$R = \sum \gamma^{k-1} r_k + \varepsilon_1 \mathbf{1}_{到达} - \varepsilon_2 \mathbf{1}_{超时}$；无归一化；ε1/ε2/γ 具体值未给
4. **建模假设**: walker-delta F=0 固定 4-ISL MSN 拓扑；Poisson 队列到达；AWGN+FSPL；地面站训练/卫星推理
5. **网络架构**: GAT(64, LeakyReLU)→GraphNorm→GlobalAddPool→FC(64,ReLU)→FC(4,Softmax) [Actor]; GAT(32)→...→FC(1) [Critic]; Adam
6. **适配性分析**: 适配: GAT 框架可复用，验证 GNN>FC | 不适配: 6 节点局部子图太粗糙，需全局聚合；无归一化/超参数缺失 | 改进: 扩展到全图消息传递，动作改为 per-link 分流比

---

### [L02] GMR: A GNN-Enabled Multipath Routing Algorithm for Spatial-Temporal Varying LEO Satellite Networks

- DOI/来源: 10.1109/TVT.2023.3333848
- **发表状态**: 正式发表
- **发表渠道**: IEEE TVT (SCI Q1)
- 年份/会议: 2024, Vol.73, No.4
- 核心贡献: 提出 GMR 两阶段方案：(1) LDMR 离线多路径规划（Dijkstra+随机权重找 K 条链路不相交路径）；(2) GNN-MPTE 在线流量分割（MPNN+DDPG+PER）。核心创新是 GNN 处理变规模拓扑，实现零重训练跨星座泛化（GlobalStar 48 星训练→Iridium 66 星直接部署）。
- 方法概述: 问题分解为离线路径规划和在线流量分割。MPNN 在链路和路径之间做消息传递（双层图），DDPG 输出连续流量分配比例。K=2 条 link-disjoint 路径性能最优。
- 实验设置: GlobalStar(48星,1400km) 训练+测试; Iridium(66星,780km) 仅测试验证泛化; NS3+ns3gym; Pareto on/off 流量(shape=1.5,scale=500ms); 2~8GB 总流量
- 使用的 Baseline 方法:
  - SPF (Song 2014): 最短路径优先
  - ECMP (Chiesa 2017): 等价多路径
  - DRL-TE (Xu 2018): AC+PER 流量工程（自实现）
  - DDPG-TE (Chen 2021): DDPG 无 GNN（自实现）
- 关键结论: 2 条路径最优；吞吐量提升 11.2%~26.2%；跨星座泛化有效（8.9%~20.2%）；Jain 公平性大幅提升；~60 episode 收敛；消息传递 3 次迭代足够
- 与本研究关系: **直接相关，架构最接近** — per-path 流量分割 + 跨拓扑泛化 + MPNN 链路-路径消息传递
- 实现关键细节: 奖励 $r_t = \sigma_1 \bar{f} - \sigma_2 \bar{d}$（权重未给）；softmax 约束分流比和为 1；MPNN hidden=32, ReLU, GRU update; h=3 次迭代; K=2; DDPG+OU 噪声+PER
- 开源代码: 无

**结构化提取**:

1. **状态空间**: TM_t(流量矩阵), F_t(链路占用), C_t(剩余容量), P_t(路径矩阵, zero-padding)；未显式归一化
2. **动作空间**: 连续 1×(K×M)，每组 K 个分流比 Σw=1，w≥0
3. **奖励函数**: $r_t = \sigma_1 \bar{f}^{\tau_i} - \sigma_2 \bar{d}^{\tau_i}$；无归一化；σ1/σ2 具体值未给
4. **建模假设**: SDN 集中控制; Pareto on/off 流量; 虚拟拓扑(快照内固定); K 条路径预计算; 单步 MDP(无历史)
5. **网络架构**: MPNN Edge/Path Embedding(32,ReLU) → Message(32,ReLU) → GRU Update(32) → Readout FC → DDPG Actor/Critic; NS3+ns3gym
6. **适配性分析**: 适配: MPNN 链路-路径消息传递可迁移，连续动作+和约束匹配，跨拓扑泛化范式可复用 | 不适配: 预计算路径集合限制，需端到端联合优化，超参数缺失 | 改进: 改为全局链路图直接传播，动作从 per-flow 改 per-link

---

### [L03] POMAP: Efficient Packet Routing for Large-Scale LEO Satellite Networks: A Pareto-Optimal MARL Approach With Queueing Theory

- DOI/来源: 10.1109/JIOT.2025.3610772
- **发表状态**: 正式发表
- **发表渠道**: IEEE IoT Journal (SCI Q1)
- 年份/会议: 2025, Vol.12, No.22
- 核心贡献: 将 Pareto 多目标优化与 MAPPO 结合用于 LEO 包路由。每卫星建模为 G/G/1/K 队列（M=4 类，K=200），配备 AQM+WPQ 调度。分解策略将多目标转化为标量子问题，邻域参数迁移加速收敛。首个多目标 MARL 用于卫星网络包路由。
- 方法概述: GAT 编码一跳邻居信息做观测编码器，动作含流量分配比例(连续)+WPQ 权重+AQM 参数。CTDE 范式，集中式 critic 用全局状态。奖励 min-max 归一化后的负加权和多目标成本。
- 实验设置: Starlink1 四组(172/348/720/1584 节点); StarPerf 拓扑; XuanCe MARL; M=4 队列类, K=200 packets; B=500MHz, P_tx=35W; 5 次独立运行
- 使用的 Baseline 方法:
  - GraphPR (Ran 2025, TVT): GNN+MARL 路由
  - MAFDR (Xu 2022, GLOBECOM): 全分布式 MARL
  - epsilon-DMOGA (Zhang 2023, TVT): 离散多目标遗传算法
  - NC-MOPSO (Wu 2023, TNSE): 多目标粒子群
- 关键结论: 收敛更稳定（峰值得分 1.55e5 vs GraphPR 振荡>1.5e4）；720 节点延迟降低 6-9%，能耗降低 8-15%，丢包率降低 15-30%
- 与本研究关系: 直接相关 — MARL LEO 路由，队列感知设计可借鉴，但 per-packet 粒度太细
- 实现关键细节: 奖励 min-max 归一化到[0,1]：$r = -\lambda^T c_{norm}$；PPO clip ε=0.2；队列长度隐式归一化(÷K_m)；流量分配 softmax 约束
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 队列状态 Q_i(t)(长度+丢包概率), 链路延迟, 能量状态(剩余比例), 邻居信息；队列 ÷K 隐式归一化
2. **动作空间**: 混合 — 流量分配(连续, softmax 约束) + WPQ 权重(M=4) + AQM 参数(α,β,p_max)
3. **奖励函数**: $r_t = -\lambda^T c_{norm}$，$c^{norm} = (c - c_{min})/(c_{max} - c_{min})$；min-max 归一化到[0,1]；λ=(λ_1,λ_2,λ_3), sum=1
4. **建模假设**: G/G/1/K 队列；理想 FSPL 信道；WPQ 严格优先级；Little's law 延迟近似
5. **网络架构**: GAT 编码器(共享) → MLP 策略头(流量分配/WPQ/AQM) → Critic 全局状态(permutation-invariant readout); XuanCe MARL
6. **适配性分析**: 适配: 队列感知+AQM 拥塞控制建模思路可迁移，GAT 一跳邻居编码可借鉴 | 不适配: per-packet 太细粒度，动作含跨层控制(调度+拥塞控制) | 改进: 简化动作空间为路由分流比，保留队列建模和归一化奖励

---

### [L04] PathGNN: Path-Based Graph Neural Network for Robust and Resilient Routing in Distributed Traffic Engineering

- DOI/来源: 10.1109/JSAC.2025.3528815
- **发表状态**: 正式发表
- **发表渠道**: IEEE JSAC (SCI Q1, 通信顶刊)
- 年份/会议: 2025, Vol.43, No.2
- 核心贡献: 提出 path-link 二部图建模，将路由路径和链路作为不同图实体，GNN 消息传递捕获链路资源竞争。监督学习（SL）从最优路由策略（Gurobi LP）学习。支持分布式部署（512 字节 GNN 消息包跨路由器交换）。负载均衡性能至少超 MARL-GNN 24.4%。
- 方法概述: 路径实体=流量需求，链路实体=容量。5 层多头注意力(H=8, d=128)编码，pair-wise softmax 输出路径分流比。CLF 训练策略用 max-flow min-cut 选 top 10% 链路构造故障样本。
- 实验设置: Abilene(12), CERNET(14), GEANT(23) 有真实 TM; Sprintlink(52) MGM 生成; 每源-目的 4 条预配置路径; Tesla V100 训练; 4-core Intel 推理
- 使用的 Baseline 方法:
  - MARL-GNN (Bernardez 2021/2023): GNN+MARL（自实现）
  - Oblivious Routing (Applegate 2003): LP 鲁棒路由
  - ECMP: 等价多路径
  - Optimal Routing (Mitra 1999): Gurobi 集中上界
- 关键结论: MLU 性能比 91.9%-94.5%（接近最优）；vs MARL-GNN 提升至少 24.4%；训练数小时 vs MARL-GNN>2 个月；推理<1ms
- 与本研究关系: 方法可借鉴 — path-link 二部图建模和 GNN 消息传递可迁移；**对比 baseline 候选**：GNN 路由标杆
- 实现关键细节: SL 方法无奖励；训练损失 L = KL_div + MAE + L2_reg(λ=0.001)；dropout=0.1；pair-wise softmax 保证分流比和=1；d_h=128, ω=8 heads, d_f=256, lr=1e-4, batch=64, H=5 layers
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 路径实体=流量需求 D_{s,d}；链路实体=容量 C_e；path-link connectivity matrix；未显式归一化
2. **动作空间**: 连续，每路径一个分流比 σ_p^{v,d}；pair-wise softmax per (v,d) 保证 Σσ=1
3. **奖励函数**: 无（SL）；训练目标 $L = L_{KL} + L_{MAE} + \lambda L_{L2}$, λ=0.001
4. **建模假设**: 预配置 4 条路径(oblivious routing)；静态拓扑快照(非 LEO)；无队列模型；M/M/1 延迟近似
5. **网络架构**: Encoder FF(1→128) → 5×(MHA: d=128,ω=8) + FF(256,GELU) + SkipConn+LayerNorm → Decoder FF(128→1); SGD lr=1e-4, batch=64
6. **适配性分析**: 适配: path-link 二部图建模可迁移，多头注意力做资源竞争建模 | 不适配: 地面 WAN 静态拓扑，SL 需全局最优 label | 改进: 扩展到动态 LEO 拓扑，SL 改 RL 适应无 label 场景

---

### [L05] GDRL-SFCR: Deep Reinforcement Learning-Based Routing Method for LEO Mega-Constellation Satellite Networks with Service Function Constraints

- DOI/来源: 10.3390/s25041232
- **发表状态**: 正式发表
- **发表渠道**: Sensors (MDPI, SCI Q2, IF ~3.4)
- 年份/会议: 2025年2月
- 核心贡献: 提出 GDRL-SFCR 在 LEO 巨型星座中实现 SFC 约束下的端到端路由，联合优化时延和负载均衡。GCN 提取拓扑特征 + PPO 训练 + SFC 约束动作屏蔽。6048 颗卫星 StarLink 规模仿真验证。
- 方法概述: GCN 2 层消息传递(d=6)提取节点嵌入，MLP 计算内积作为有效状态，PPO actor-critic 输出下一跳概率。SFC 约束通过 action masking 实现。
- 实验设置: 6048 卫星(84×72), 550km/53°; SGP4 轨道模型; 数据流 [5,100]Mb 对数正态; max_step=50, max_episode=10000
- 使用的 Baseline 方法:
  - SFC-APS: 图论 SFC 路由（引用 [26]）
  - DQN-LBR: DQN 负载均衡（引用 [39]）
  - DQR: DQN 贪心 SFC 路由（引用 [34]，自实现）
- 关键结论: 端到端时延降低 11.3%+，负载降低 14.1%+，接入成功率提升 19.1%+，容量提升 2 倍；θ_1=0.6 时延-负载最佳平衡
- 与本研究关系: 直接相关 — GNN+DRL LEO 路由+负载均衡，GCN 消息传递聚合全局负载信息
- 实现关键细节: 分段奖励（环路-1，正常=-R_L+R_F+R_T，到达额外+1）；未归一化；PPO clip=0.2, γ=1, entropy=0.02; GCN 2 层 d=6; Actor FC(64,4,tanh); Adam lr=1e-4; OpenRL
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 源/目的/当前节点 ID, 负载值, 已过功能节点数, 邻居集合；经 GCN 嵌入后送策略网络；未显式归一化
2. **动作空间**: 离散 one-hot, dim=max_degree(G)；SFC 顺序违反的动作屏蔽
3. **奖励函数**: 分段设计 — 环路-1；正常 $-R_L + R_F + R_T$；到达且满足 SFC 额外+1；未归一化；θ_1=0.6, θ_2=0.4
4. **建模假设**: 同轨 ISL 稳定；卫星功能随机分配；端到端三种模式(全地/半星/全星)；单卫星单功能；集中训练
5. **网络架构**: GCN(d=6,×2) → MLP_f(64) / MLP_g(64) → Actor(3-hidden, d_pi=4, ReLU) / Critic(2-hidden, d_phi=4, tanh); Adam lr=1e-4
6. **适配性分析**: 适配: GCN+PPO 框架可复用 | 不适配: SFC 约束是额外复杂度，GCN 太浅(d=6)，奖励未归一化 | 改进: 去掉 SFC，加深 GNN(GAT/GIN)，增加嵌入维度，奖励归一化

---

### [L06] DTAR: Traffic-Aware Domain Partitioning and Load-Balanced Inter-Domain Routing for LEO Satellite Networks

- DOI/来源: arXiv:2604.12382v1
- **发表状态**: 预印本
- **发表渠道**: arXiv (cs.NI)
- 年份/会议: 2026
- 核心贡献: DTAR 两阶段框架：(1) NSGA-II 离线流量感知域划分(max IDTR + min load deviation)；(2) GAT 编码域间链路状态 + action-masked PPO 在线路由。288 卫星 Walker 星座，三种场景均优于 4 个 baseline。
- 方法概述: 离线 NSGA-II 做域划分(双目标优化)；在线 GAT(2层,4头,h=64,out=32)编码域级状态，89 维观测送 PPO，hop-by-hop 选域。Action masking 保证物理可达性和跳数约束。
- 实验设置: 288 卫星(12×24), 1450km/89°; 18 域; episode 144 步×3 流; H_max=9; p_f=0.02, p_r=0.02; μ=5×突增; 2.5×10^6 训练步
- 使用的 Baseline 方法:
  - Dijkstra: 最短路径
  - ELB: 负载加权最短路径
  - QRLSN: Q-learning 路由
  - CDPAR: DQN 域划分路由
- 关键结论: CV（负载变异系数）最低；突增时 surge indicator 帮助绕行；故障时成功率提升 9.25pp；消融: NSGA-II 划分在故障场景主导，GAT 编码在突增场景贡献更大
- 与本研究关系: 直接相关 — GAT 聚合域间链路负载做域间路由，action masking 可借鉴；**有开源代码**
- 实现关键细节: 奖励 $R(c,a,c') = \delta(d(c,D)-d(c',D)) - \beta + \mathbf{1}[c'=D_{dst}](r_s-\beta h) - r_f \mathbf{1}[fail]$；δ/β/r_s/r_f 具体值未给；观测 89 维；GAT ELU+LayerNorm+Residual; PPO lr=3e-4, mini-batch=256, entropy=0.03
- 开源代码: 有 — https://github.com/ChenZ-code/DTAR_Routing

**结构化提取**:

1. **状态空间**: 当前/目的域嵌入(32), flow state(3), 邻居距离(18), 全局状态(4: 时间/CV/突增/故障)；GAT LayerNorm
2. **动作空间**: 离散 K=18(选下一域)；action masking: 故障域屏蔽 + 超跳数预算屏蔽
3. **奖励函数**: $R(c,a,c') = \delta(d(c,D_{dst})-d(c',D_{dst})) - \beta + \mathbf{1}[c'=D_{dst}](r_s - \beta h) - r_f \mathbf{1}[\text{fail}]$；未归一化；具体超参未给
4. **建模假设**: 域划分离线固定；域间链路独立故障 p_f=0.02；域内最短路径(与域间正交)；标准 4-ISL；日模式流量
5. **网络架构**: InputProj(6→64) → GAT1(64→64,H=4,ELU,LN+Res) → GAT2(64→32,H=4,ELU,LN+Res) → PPO(obs89→act18); Adam lr=3e-4; SB3
6. **适配性分析**: 适配: GAT+边特征+action masking 直接复用，方向塑造奖励设计可借鉴 | 不适配: 域级路由抽象掉了卫星级细节 | 改进: 去掉域划分，直接卫星级图上做 GNN 路由

---

### [L07] Research on power control and load balancing based on distributed algorithm in satellite communication system (Fan 2026)

- DOI/来源: 10.1007/s44163-026-01073-x
- **发表状态**: 正式发表
- **发表渠道**: Discover Artificial Intelligence (Springer)
- 年份/会议: 2026 (Published 2026-03-29)
- 核心贡献: 混合 GNN+DQN 框架用于 LEO 分布式功率控制与负载均衡路由。GNN 多轮 edge-level 消息传递（带宽、延迟、介数中心性）生成全局嵌入，DQN 从 k-shortest path 候选选路。两跳负载感知 RMLBR 扩展负载感知范围。
- 方法概述: 虚拟节点模型屏蔽卫星运动；GNN edge-level 消息传递→全局嵌入→DQN 选路；RMLBR 两跳负载感知+闭环功率控制。
- 实验设置: 类 Iridium 极轨星座; OPNET Modeler; ISL 200Mbps, 队列 66Mbit/link; 24 小时循环流量; 10 次重复
- 使用的 Baseline 方法:
  - TLR: 阈值负载感知路由
  - ELB: 两阶段分布式负载均衡
  - Maximum-Elevation / Maximum-ServeTime
  - 传统 DRL: 无 GNN 纯 DQN
- 关键结论: 链路切换频率降低 42.2%，吞吐量 63.08 Mbps，丢包率<4%，延迟~100ms；消融: DQN-only +4.2%, GNN-only +5.0%, GNN+DQN +8.6%
- 与本研究关系: 直接相关 — GNN edge-level 消息传递聚合全局链路状态做路由，与本研究思路高度吻合
- 实现关键细节: 奖励 $r = \alpha \cdot \text{TP/TP}_{max} - \beta \cdot \text{Delay/Delay}_{max} + \gamma \cdot \text{Reliability}$；α∈[0.4,0.6], β∈[0.5,0.7]；链路状态 [剩余带宽, 延迟, 介数中心性, 选择标志]
- 开源代码: 无（有 Supplementary Material）

**结构化提取**:

1. **状态空间**: 链路状态 s_ij=[x1(带宽),x2(延迟),x3(介数中心性),x4(选择标志)] → GNN 全局嵌入 z_G；介数中心性 [0,1] 天然归一
2. **动作空间**: 离散，k-shortest path 候选路径数；带宽约束 x1≥b_min
3. **奖励函数**: $r = \alpha \cdot \frac{\text{TP}}{\text{TP}_{max}} - \beta \cdot \frac{D}{D_{max}} + \gamma \cdot \text{Rel}$；除以最大值归一化；α∈[0.4,0.6], β∈[0.5,0.7], ±10% 稳定
4. **建模假设**: 虚拟节点屏蔽运动；极区排除 inter-plane ISL；忽略误码率；均匀 ISL 200Mbps；负载比 ρ=Q/Q_max 三级离散化
5. **网络架构**: GNN message passing(K 轮, edge embedding) → Readout(sum/mean/max/attn) → z_G → RNN(时序) → DQN；具体维度/层数未公开
6. **适配性分析**: 适配: GNN edge-level 消息传递与本研究核心思路一致，两跳负载感知机制可借鉴 | 不适配: 路径级动作(k-shortest 选一)非 per-link，架构/超参未公开 | 改进: 改为 per-link 出端口选择，更细粒度

---

### [L08] PRIMAL: Asynchronous Risk-Aware Multi-Agent Packet Routing for Ultra-Dense LEO Satellite Networks

- DOI/来源: arXiv:2510.27506v1
- **发表状态**: 预印本（截至 2026-05-16 无正式发表记录）
- **发表渠道**: arXiv (cs.NI), University of Luxembourg / SnT
- 年份/会议: 2025 (arXiv submitted October 2025)
- 核心贡献: 事件驱动异步多智能体路由，primal-dual 方法+分布式 RL(IQN)学习 QoS 代价分布，直接约束 CVaR 控制尾部风险。解决同步 MARL 不实际假设和 reward shaping 缺乏理论保证的问题。
- 方法概述: POCSMDP 建模，SAC actor-critic 扩展为 constrained RL。PRIMAL-Avg 约束期望代价，PRIMAL-CVaR 用 IQN 约束尾部风险。所有卫星参数共享，去中心化执行。
- 实验设置: Walker-Delta 1584 卫星(72×22), 600km/53°; GSL 1000Mbps, ISL 50Mbps; 缓冲 16Mbits; Poisson 10000pkt/s, 80%×64.8Kb+20%×16.2Kb; TTL=64 hops; 30s epoch
- 使用的 Baseline 方法:
  - SPF: Dijkstra 预计算路由表
  - MADQN: 多智能体 DQN+手工 reward shaping
- 关键结论: E2E 延迟~62ms（MADQN~77ms）；排队延迟降低>70%；丢包率 0%（SPF 84.8%）；吞吐量 543Mbps（SPF 27Mbps）；CVaR_{0.25} 排队延迟 1.7ms（MADQN 31.1ms）
- 与本研究关系: 直接相关 — 异步 per-hop 路由+负载均衡约束，大规模星座验证，**有开源代码**
- 实现关键细节: 奖励 $r_h = \tau/D_{norm} - c_h + \Delta d + B_p$，D_norm=100ms，$c_h = D_h^Q/D_{norm}$；γ_r=0.99, γ_c=0.97；熵最小 0.067；排队约束 D_max^Q=10ms；backbone 2-layer MLP 512 hidden
- 开源代码: 有 — https://github.com/skypitcher/risk_aware_marl

**结构化提取**:

1. **状态空间**: 包状态(源/目的), 当前卫星位置, 邻居链路排队状态, GCD 距离差 Δd；精确维度需查代码
2. **动作空间**: 离散 4 (N/S/W/E)；连通性约束
3. **奖励函数**: $r_h = \frac{\tau}{D_{norm}} - \frac{D_h^Q}{D_{norm}} + \Delta d + B_p$，D_norm=100ms；成功 B_p=1+L_p，丢包 $B_p = -5\tau_p^{ttl}/D_{norm} - \sum \Delta d_{GCD}$
4. **建模假设**: 事件驱动异步(非时隙)；parameter sharing；CTDE；Grid 4-ISL；ISL 50Mbps 固定；Walker-Delta 53°(无极区断链)
5. **网络架构**: 共享 backbone MLP(2层, 512 hidden) → Actor(4, softmax) / Reward Critic(|A|×1) / Cost Critic(IQN, 64 samples); batch=1024, buffer=300K
6. **适配性分析**: 适配: 异步事件驱动设计贴近真实 LEO，primal-dual CRL 方法论可直接用于约束负载均衡 | 不适配: 纯 MLP 无 GNN，4 方向动作空间过于简化 | 改进: 加 GNN 替换 backbone，扩展为 per-link 负载比例决策

---

### [L09] Queue-Aware and Resilient Routing in LEO Satellite Networks Using Multi-Agent Reinforcement Learning (QueueMARL)

- DOI/来源: arXiv:2605.04448v1
- **发表状态**: 预印本
- **发表渠道**: arXiv (cs.NI), NSERC 资助
- 年份/会议: 2026
- 核心贡献: Queue-aware MA-DRL 路由框架，将队列积压、距离缩减、环路惩罚、弹性分数纳入奖励函数。DDQN 先集中训练后分布式部署。计算开销约为 Dijkstra 的 50%。
- 方法概述: MDP+DDQN+ε-greedy。状态含卫星坐标、邻居坐标和队列水平、目的坐标、链路弹性分数。动作选 next-hop（上下左右 4 方向）。奖励含排队延迟+距离+环路+弹性。
- 实验设置: Starlink Shell 1 (72×22=1584卫星), 550km; 200 地面站; ISL 20W/500MHz/30GHz; 包 64kb; 100K iterations; 背景：均匀+人口比例两种
- 使用的 Baseline 方法:
  - Dijkstra: 最短路径（自实现）
  - SARSA: 集中训练拷贝（自实现）
- 关键结论: 平均时延 49.31ms（Dijkstra 38.54ms, SARSA 59.28ms）；计算开销 ~50% Dijkstra；弹性分数 Dijkstra>MA-DRL>SARSA
- 与本研究关系: 方法可借鉴 — queue-aware 奖励设计、弹性分数概念；但无 GNN
- 实现关键细节: 奖励四项组合（无显式完整公式）；弹性分数 $R^{all} = \omega_1(1-P_{out}^{all}) + \omega_2 \max(\max(1-q_i,1-q_j) \cdot S_{ij})$；ω_1/ω_2 未给；ε: 0.99→0.1, decay=1000; DDQN lr=1e-4, Huber loss, replay=2000, batch=128
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 当前/邻居坐标, 邻居队列水平 q_i, 目的坐标, 链路弹性分数 [0,1]；未显式归一化
2. **动作空间**: 离散 4（上/下/左/右）；边界可能不足 4 邻居（未明确处理）
3. **奖励函数**: 4 项文字描述（排队延迟+距离缩减+环路惩罚+弹性分数），无显式公式；$R^{all}$ 见上
4. **建模假设**: Walker Delta Starlink Shell 1; 圆轨道 e≈0.00001; 4-ISL + 1 地面链路; Nakagami-m(m=2) 衰落; 均匀+人口比例流量
5. **网络架构**: DNN 3 层全连接（维度未给）+ Target 网络; DDQN, lr=1e-4, Huber loss, replay=2000, batch=128
6. **适配性分析**: 适配: queue-aware 奖励设计值得借鉴，弹性分数结合 outage+队列条件 | 不适配: 纯 DNN 无 GNN，4 方向动作空间简化，replay 仅 2000 极小 | 改进: 弹性分数概念引入 GNN 框架，GNN 替代 DNN 做邻居负载聚合

---

### [L10] ST-QoS: Spatial-Temporal Learning-Based Distributed Routing for Dynamic LEO Satellite Networks

- DOI/来源: arXiv:2605.02413v1
- **发表状态**: 预印本
- **发表渠道**: arXiv (cs.NI), 台湾师范大学
- 年份/会议: 2026
- 核心贡献: GAT+LSTM+DQN 分布式路由。GAT 聚合邻居拓扑特征做空间建模，LSTM 捕捉时序流量模式做拥塞预判，DQN 做 Q 值估计。队列长度降低最多 23.26%。
- 方法概述: POMDP 建模，每卫星独立 agent。GAT(4头,h=64)提取空间特征，LSTM(h=128)建模时序依赖，DQN 输出 Q 值选 next-hop。完全分布式。
- 实验设置: 45 卫星(非真实星座); ISL 300Mbps, 570km/70°/23.28GHz/25MHz; 最大队列 640 包; TTL 30 跳; NHPP 流量 120/180/240Mbps; 1300 episodes
- 使用的 Baseline 方法:
  - Dijkstra: 拓扑自适应最短路径
  - GraphPR (Ran 2025, TVT): GNN+MARL
  - DQN-IR (Zuo 2021): 单 agent DRL
  - FDR-MARL (Xu 2022): 多 agent RL
- 关键结论: 队列降低 23.26%；240Mbps 吞吐~210Mbps，延迟~498ms；计算开销可控（2.70ms/10K 推理）
- 与本研究关系: 直接相关 — GAT 聚合邻居负载/拓扑信息做拥塞路由，与本研究 GNN 消息传递思路一致；但规模太小(45 星)
- 实现关键细节: 奖励 $r_i = -(\alpha D_{i,a_i} + \beta Q_i)$，β>α（拥塞权重>时延），具体值未给；ε: 1.0→0.01, decay=0.995; GAT 4头 h=64; LSTM h=128; DQN lr=1e-4, γ=0.99, batch=128, buffer=100K, target=200
- 开源代码: 无

**结构化提取**:

1. **状态空间**: 本地队列长度 [0,640], 邻居链路时延, 拓扑特征 x_i；未归一化
2. **动作空间**: 离散 |N_i(t)|（动态邻居数）；选当前可达邻居之一
3. **奖励函数**: $r_i(t) = -(\alpha D_{i,a_i(t)}(t) + \beta Q_i(t))$，$\beta > \alpha > 0$；无归一化；具体值未给
4. **建模假设**: NHPP 流量 λ_i(t)=λ_0(1+sin(2πt/T)); 动态时变拓扑; FIFO 队列 Q(t+1)=max(Q-μ,0)+A; POMDP(仅本地); 45 星(非真实规模)
5. **网络架构**: GAT(4 heads, h=64, σ) → LSTM(h=128) → DQN FC; Adam lr=1e-4, γ=0.99, batch=128, buffer=100K
6. **适配性分析**: 适配: GAT 聚合邻居拓扑/负载做拥塞路由与本研究一致，LSTM 时序建模可辅助拥塞预判 | 不适配: 45 星规模太小，无 per-link 负载均衡 | 改进: 用真实规模验证 GNN 可扩展性，加归一化奖励和权重消融

---

## Step 3.5 定向补充检索

### 检索执行

**关键词矩阵** (3 方法变体 × 2 问题+规模 = 6 组合):
1. GIN + routing + load balancing + scalability (S2) ✅
2. GAT edge features + per-link traffic splitting + congestion (S2) ✅
3. MPNN + cross-topology generalization + TE zero-shot (S2) ✅
4. GMR 双向引用链分析 (Semantic Scholar + OpenAlex) ✅
5. 竞品共引 10 篇存在性验证 ✅

**搜索源**: S2 (Semantic Scholar) + OpenAlex, ≥2 源满足

**收敛性**: 第 1 轮发现 TELGEN + 4 篇高优新竞品，需第 2 轮精读 DeepLaDu 确认收敛

### 新发现论文

#### [L11] TELGEN: Traffic Engineering in Large-scale Networks with Generalizable GNNs

- DOI/来源: arXiv:2503.24203v2
- **发表状态**: 已被 IEEE/ACM ToN 接收
- **发表渠道**: IEEE/ACM ToN（计算机网络顶刊）
- 年份/会议: 2025 (Zhou, Liu, Liu, Yu, Xue — NCSU/ASU)
- 核心贡献: 将 TE LP 问题转化为二部图（path/constraint/objective vertices），GNN 直接在 LP 结构上做消息传递。双循环 GNN（K=8~16 外循环对齐 IPM 迭代，J=2 内循环近似 Newton step），逐步强监督训练。训练在 20~100 节点，推理泛化到 200~5000 节点（20x），optimality gap < 3%。
- 方法概述: LP 变量/约束/目标→四类顶点→六种消息传递方向。双循环 GCN 架构，跨外循环参数共享。Loss = variable loss + constraint loss + objective loss（含 discount factor）。推理时 readout 从 path vertices 读出流量分配比。
- 实验设置: ER 20~2000, Waxman 200~5000, ASN 553/1739, B4(12); 最大 5000 节点/3.6M links; A100 GPU
- 使用的 Baseline 方法:
  - TEAL (SIGCOMM 2023): GNN+MARL+ADMM
  - HARP (SIGCOMM 2024): GNN+Transformer+RAU
  - SciPy IPM / Gurobi: 最优基线
- 关键结论: optimality gap 0.3%~2.99%（远优于 TEAL 26%+ / HARP 73%+）；推理 1.52ms；训练 4h；跨需求分布泛化 OGap 波动仅 ±0.03%
- 与本研究关系: **最直接竞品** — GNN+TE+size generalization 已被做完整。差异化必须聚焦：(1) LEO 时变拓扑（TELGEN future work）；(2) per-link 负载均衡 vs per-path 流量分割；(3) DRL 在线适应 vs SL 离线训练
- 实现关键细节: MLP encoder(180/360) + 双循环 GCN(K=8~16, J=2) + MLP readout(360/720) + ReLU + Residual；150 epoch；基于 IPM-GNN codebase；Yen's k-shortest paths 预计算
- 开源代码: 引用 github.com/chendiqian/IPM_MPNN，TELGEN 本身未明确开源

**结构化提取**:
1. **状态空间**: 网络 G=(N,L,C), SD 对, 预定义路径集 P; 无 RL 状态空间概念（SL 方法）
2. **动作空间**: per-path 流量分配比 R(p)∈[0,1]；readout 从 path vertices 读出+ReLU
3. **奖励函数**: 无 RL；训练 loss = ρ1·L_p(variable) + ρ2·L_dl(constraint) + ρ3·L_o(objective)，含 discount
4. **建模假设**: 有向图静态快照；预定义 k-shortest paths；集中式 SDN；链路容量固定；单时间快照无时序；自述局限：(1)不适用无线干扰场景 (2)未利用时序信息 (3)集中式设计
5. **网络架构**: MLP enc(2层,180/360) → 双循环 GCN(K=8~16外循环×J=2内循环 GCN) → MLP readout(2层,360/720) + ReLU + Residual
6. **适配性分析**: 适配: size generalization 20x 泛化范式、双循环 GNN 算法对齐思路、LEO 列为目标场景 | 不适配: 静态快照无时序（LEO 最关键的时变性完全缺失）、per-path 决策需预计算路径、SL 需离线 IPM label | **核心差异化**: LEO 时变拓扑 + per-link 在线负载均衡决策

#### 其他高优先级新发现（待精读）

| # | 论文 | 来源 | 优先级 | 关键点 |
|---|------|------|--------|--------|
| 1 | **DeepLaDu** (Gu 2026, arXiv:2601.21921) | GMR 前向引用 | 高 | GNN 推断 per-link congestion prices，Lagrangian dual 框架，与本研究 per-link 最接近。**已下载** |
| 2 | **ALIDT/ADRLRM** (Gao 2025/2026, TMC/ToN) | GMR 前向引用 | 高 | STGNN 做卫星路由，声称超越 GMR。同一团队两篇 |
| 3 | **GRL-RR** (Bai 2025, Computer Networks) | GMR 前向引用 | 高 | GNN+DRL LEO 弹性路由 |
| 4 | **Fan 2026 TAES** (DOI:10.1109/TAES.2026.3652971) | GMR 前向引用 | 高 | GNN+RL 多路径流量拆分（与 L07 不同论文）。**下载失败** |
| 5 | HARP (SIGCOMM 2024) | 新检索 | 中 | cross-topology TE 神经方法，98% 场景 MLU 仅高 11% |

### 缺失论文状态

| 论文 | 下载尝试 | 状态 |
|------|---------|------|
| GNN-ASSSP (ScienceDirect) | tools/download | 付费墙，需用户手动 |
| DLBR (IEEE TAES) | tools/download | 付费墙，需用户手动 |
| LARRI (IEEE ToN) | tools/download | 付费墙，需用户手动 |
| FlexSATE (IEEE GLOBECOM) | tools/download | 付费墙，需用户手动 |
| CA-GAR (MDPI Symmetry) | tools/download | 失败（OA 但下载失败） |
| Fan 2026 TAES (IEEE TAES) | tools/download | 付费墙，需用户手动 |
| DeepLaDu (arXiv) | tools/download | ✅ 已下载 |

### 检索充分性判据

- [x] 关键词矩阵覆盖：3 方法变体 × 2 组合 = 6 组合已执行
- [x] 搜索源覆盖：S2 + OpenAlex (≥2)
- [x] 引用链分析：GMR 双向引用链已完成
- [ ] 收敛性：第 1 轮发现 4 篇高优新竞品，需 DeepLaDu 精读后确认
- [x] 上限：第 1 轮完成，需进入第 2 轮

---

## Step 3 综合分析（含 Step 3.5 更新）

### 1. 现有方法分类

**A. GNN+RL 分布式逐跳路由** (L01 GRLR, L05 GDRL-SFCR, L06 DTAR, L10 ST-QoS)
每颗卫星/域作为独立 agent，GNN 提取局部/域级拓扑特征，输出 next-hop 或下一域。动作空间为离散选择（4 方向或邻居数）。GRLR 和 ST-QoS 使用 GAT，GDRL-SFCR 使用浅层 GCN(d=6)，DTAR 使用 GAT+边特征。共同局限：只能选"下一跳走哪"，无法做多下一跳负载分担。

**B. GNN 多路径流量分割** (L02 GMR, L04 PathGNN)
预计算 K 条路径，GNN 消息传递在链路-路径双层图上交换信息，输出连续流量分配比例。GMR 使用 MPNN+DDPG，PathGNN 使用 5 层注意力+SL。**与本研究 per-link 负载均衡在问题建模上最接近**，但依赖预计算路径集合。

**C. GNN 辅助选路** (L07 Fan 2026)
GNN 做 edge-level 消息传递生成全局嵌入，DQN 从 k-shortest path 候选选一条。GNN 在这里充当"特征提取器"而非"决策器"，动作粒度仍是路径级。

**D. 纯 RL 路由（无 GNN）** (L08 PRIMAL, L09 QueueMARL)
MLP+DDQN/SAC，强调 queue-aware 奖励设计和约束优化（primal-dual）。PRIMAL 的异步事件驱动和 CRL 方法论有理论价值，但缺乏拓扑结构利用。

**E. 多目标队列感知 MARL** (L03 POMAP)
MAPPO+GAT，每节点 G/G/1/K 队列建模最精细，但 per-packet 粒度太细。

### 2. 已知局限

1. **GNN ≈ MLP 风险**: L01 GRLR 中 GAT vs FC 有差异但在路由决策维度是否显著存疑。L05 GDRL-SFCR 的 GCN 太浅(d=6)。L07 消融显示 GNN-only 仅+5%。需在拥塞/负载信息聚合维度验证 GNN 的结构性优势。
2. **超参数缺失**: L01/L02/L05/L06/L07 均有奖励权重、学习率、网络维度等关键超参缺失，直接复现困难。L06 DTAR 和 L08 PRIMAL 有代码可查。
3. **规模-粒度矛盾**: 多数论文在小规模（45~288 星）验证（L06, L10）；L05 在 6048 星但 GCN 太浅；L08 在 1584 星但无 GNN。GNN 在大规模星座的 per-link 负载均衡决策尚无验证。
4. **预计算路径依赖**: L02 GMR 和 L04 PathGNN 依赖预计算路径集合，限制了灵活性。端到端直接输出 per-link 决策的方案缺失。
5. **奖励设计粗糙**: 多数论文奖励无归一化，权重未消融，收敛性无法保证。L03 POMAP 的 min-max 归一化和 L08 PRIMAL 的 CRL 是少数例外。

### 3. 2-3 年趋势

1. **GNN 架构演进**: GCN→GAT→MPNN→自定义注意力（PathGNN 5 层）。趋势是更深、更多注意力头、边特征参与消息传递。L06 DTAR 的 GAT+边特征+LayerNorm+Residual 是当前最佳实践。
2. **从分布式逐跳到集中式优化**: 早期工作（GRLR, GDRL-SFCR）偏分布式逐跳决策；近期（GMR, PathGNN, DTAR）倾向于集中式/分层的流量工程。本研究 per-link 负载均衡属于后者。
3. **从单目标到多目标/约束优化**: L03 POMAP（多目标 Pareto）、L08 PRIMAL（CVaR 约束）代表了从简单奖励到有理论保证的约束 RL 的趋势。
4. **泛化性成为核心关注**: L02 GMR 验证跨星座泛化，L04 PathGNN 强调分布式部署。Size generalization 在拥塞路由场景的空白是本研究的机会。
5. **仿真器从简化到真实**: 早期用均匀流量+静态拓扑，近期（PRIMAL, QueueMARL）用 NHPP/人口分布+动态拓扑+真实星座参数。

### 4. 研究背景概述

**时间线**:
- 2021-2023: DRL 路由起步（DRL-TE, DQN-LBR），纯 RL 无 GNN，小规模验证
- 2024: GNN 进入 LEO 路由（GMR/MPNN, GRLR/GAT），验证 GNN>FC，但仍以逐 hop 为主
- 2025: GNN+RL 成熟（PathGNN/SL, POMAP/多目标, GDRL-SFCR/大规模），开始关注泛化和多目标
- 2026: 域划分+GAT（DTAR）、异步+CRL（PRIMAL）、edge-level GNN+负载均衡（Fan 2026）——开始接近 per-link 负载均衡，但无人做 size generalization

**核心技术挑战**:
1. 动态拓扑下的稳定 GNN 消息传递（时变 ISL 连接）
2. 全局负载信息的有效聚合（hop-by-hop 的局部信息 vs 全局最优）
3. 大规模星座的可扩展性（从 48 星到 1584+ 星的泛化）
4. 奖励设计的理论保证（避免 reward shaping 的随意性）

**本研究定位**（Step 3.5 更新）:

TELGEN (Zhou 2025, ToN) 已将"GNN + TE + size generalization"做完整（20x 泛化，<3% gap）。纯 size generalization for TE 已不再是空白。

**差异化必须聚焦 LEO 时变场景**（TELGEN 的明确 future work）：
1. **LEO 时变拓扑 TE**：利用轨道力学确定性+周期性，做跨时间步的增量 TE（TELGEN 静态快照无法处理）
2. **per-link 负载均衡决策**：LEO 拓扑频繁变化导致预计算路径失效，per-link 决策比 per-path 更灵活
3. **DRL 在线适应**：时变场景下 DRL 可在线调整，TELGEN 的 SL 需要离线预计算每个快照的 IPM 解
4. **LEO 特有约束**：ISL 可用性受限（纬度/极区）、传播时延、地面站接入选择

核心贡献点修订为：(1) LEO 时变拓扑下的 GNN 拥塞感知 TE（vs TELGEN 静态快照）；(2) per-link 在线负载均衡决策（vs per-path 预计算分割）；(3) 跨星座规模的时序泛化（vs 跨静态拓扑泛化）。

---

## 写作架构参考

### A. GRLR 写作架构

**章节结构**:
- I. Introduction (~1.5p)
- II. Related Work (~1p): A.传统路由 B.智能路由
- III. System Model (~2p): A.星座模型 B.延迟模型(含排队/传输/传播) C.问题建模
- IV. 路由策略 (~3p): A.图建模 B.GNN C.DRL D.MDP定义 E.GRLR方案
- V. 实验结果 (~2p): A.设置 B.性能分析(4子主题)
- VI. Conclusion (~0.5p)
- References: 52 篇

**参数展示**: Table I(符号表), Table II(动作映射), Table III(仿真参数)；符号在 Section III 首次引入，Table I 汇总；**无参数敏感度分析**。

**图表**: 8 图(系统模型,拓扑,架构,收敛曲线,3组 box plot,动态流量,路径可视化) + 3 表。大量 box plot 展示延迟分布。

**实验组织**: 4 baseline(CR理想/DR传统/DisCoRoute专用/RLR消融)；RLR 消融验证 GNN；评价: 端到端延迟+收敛+动态适应性；无复杂度分析。

**叙述模式**: Intro: 大背景→挑战→NP-hard→传统局限→RL优势→GNN+RL；3 条贡献；Related Work: 传统vs智能二分法。

**经典段落**:
1. GNN 必要性论证: "However, it is hard to extract effective features of heterogenic data... Thus, we propose an intelligent distributed method..." — 仿写要点: 指出 FC 局限→自然引出 GNN
2. 动态流量分析: "Since the CR strategy makes routing decisions based on all satellites... However, DR and DisCoRoute only optimize distance..." — 对比分析结构
3. 路径可视化: "These excess forwarding make the packet avoid hotspot area and reduce the delay." — 解释反直觉现象

**公式**: (1)-(25) 连续编号；变量首次出现时斜体定义；推导深度中等（排队+SNR 推导，不深入稳态分析）。

**参考文献**: 52 篇；Intro/RW 密度高(~30)；竞品共引未覆盖: [28] GRouting (Wang 2021) GNN+DRL 路由。

---

### B. GMR 写作架构

**章节结构**:
- I. Introduction (~1.5p)
- II. Related Work (~1.5p): A.路径规划 B.RL TE C.GNN
- III. System Model (~2p): A.场景 B.流量模型 C.路由模型 D.问题建模
- IV. 多路径优化 (~4p): A.LDMR 路径规划 B.GNN-MPTE 流量分割(MDP) C.训练 D.消息传递 E.方案流程
- V. 性能评估 (~3p): A.设置 B.结果分析(6子主题)
- VI. Conclusion (~0.5p)
- References: 52 篇

**参数展示**: Table I(符号表), Table II(仿真参数)；LDMR 参数敏感度有(Fig.4)；消息传递迭代次数消融(Fig.5)；关键超参(σ1/σ2,λ)缺失。

**图表**: 9 图(架构,框架,MPNN,路径性能,收敛,吞吐×4,流完成率×4,延迟×4,公平性×4) + 2 表。4 子图(2 星座×2 数据集)的系统性组织。

**实验组织**: 4 baseline(SPF/ECMP/DRL-TE/DDPG-TE)；消融: 消息传递迭代次数+路径类型；评价: 吞吐+流完成率+延迟+Jain 公平性(4 维)；跨拓扑泛化实验（GlobalStar→Iridium）。

**叙述模式**: Intro: 背景→多路径必要性→SDN 优势→DRL 潜力→泛化差→GNN 解决→GMR；3 条贡献；Related Work: 路径规划/RL TE/GNN 三分法。

**经典段落**:
1. 问题分解: "Since the traffic splitting decision lies on current network state without requiring historical experience, the problem P2 can be transformed as MDP..." — 论证分解合理性
2. GNN 泛化性: "Comparing with general DNN, the GNN has better generalization... since it can aggregate characteristics between different elements in a graph without a specification for dimensions of the input." — 从机制层面解释
3. 跨星座泛化: "With the topology structure changed, GNN-MPTE still outperforms benchmarks, where the former applies the same model, and others should re-train." — "同一模型 vs 重新训练"对比框架

**公式**: (1)-(44) 连续编号；推导较深（优化建模P0→分解P1/P2→MDP→Bellman→TD→PER）。

**参考文献**: 52 篇；竞品共引未覆盖: [14] RouteNet (Rusek 2020, JSAC), [34] DRL-TE (Xu 2018), [37] ENERO (Almasan 2022)。

---

### C. PathGNN 写作架构

**章节结构**:
- I. Introduction (~2p)
- II. Background and Motivation (~3p): A.TE 概述(问题/控制/优化) B.挑战 C.洞察(why GNN/PathGNN/SL)
- III. System Design (~3p): A.二部图建模 B.工作流
- IV. Proposed Model (~2p): A.概述 B.细节
- V. Implementation (~3p): A.数据集 B.方法 C.训练 D.CLF E.超参 F.Baseline G.指标
- VI. Evaluation (~4p): A.负载均衡 B.QoS C.链路故障 D.流量变化 E.消融(3组) F.开销
- VII. Related Work (~1p): A.传统 TE B.ML TE C.GNN
- VIII. Conclusion (~0.3p)

**特点**: Related Work 放在实验后（非 Intro 后），避免打断技术叙事流；Background+Motivation 独立为 II 节(3 页)，充分铺垫"为什么这样做"。

**参数展示**: Table I(拓扑), Table II(MGM), Table III(训练/推理时间)；超参在 V-E 文字中给出；GNN 层数 H 有消融(1→5, 26.4% 提升)；无其他超参敏感度。

**图表**: 11 图(5 CDF + 1 scatter + 2 boxplot + 1 柱状 + 2 示意) + 3 表。大量 CDF 展示性能分布（优于仅平均值）。

**实验组织**: 4 baseline(MARL-GNN/OR/ECMP/Optimal)；3 组消融(encoder/CLF/层数)；主指标: MLU Performance Ratio(越接近 1 越好)；训练时间对比(数小时 vs >2 月)。

**叙述模式**: Intro: 问题→局限(传统复杂度+ML 突发退化)→两层挑战→两个障碍→PathGNN→3 条贡献。

**经典段落**:
1. 问题动机: "First, they cannot guarantee good performance under dynamic traffic scenarios... However, actual traffic demands could be highly dynamic..." — "前提-现实冲突-后果"三段式
2. 竞品失效分析: "MARL-GNN is pioneering... However, when trained with real-world dynamic traffic patterns, its load balancing may severely degrade... This is because it cannot capture sufficient generalizable knowledge..." — "承认-失效-根因"
3. 实验解读: "Compared to OR and ECMP, PathGNN outperforms by 11.5%-17.1% and 28.3%-45.5%... This is because OR would sacrifice optimality in common cases to trade for worst-case guarantee..." — 定量对比+"because"机制解释

**公式**: (1)-(14) 编号；变量在公式后紧跟定义；推导浅层(给最终形式，不展示推导过程)。

**参考文献**: 58 篇；Intro 高密度(~15)；竞品共引未覆盖: [6] DATE (Geng 2021), [12] MA-AC (2019), [17] FlexDATE (Ye 2023), [56] LARRI (Ye 2023)。

---

## Step 3.5 定向补充检索候选

以下文献在精读论文中被多次引用但本 GW 未覆盖，建议 Step 3.5 定向补充：

| 论文 | 引用来源 | 重要性 |
|------|---------|--------|
| RouteNet (Rusek 2020, JSAC) | L02 GMR, L04 PathGNN | GNN 网络建模标杆 |
| DRL-TE (Xu 2018, INFOCOM) | L02 GMR | DRL TE 基线 |
| ENERO/RouteNet+RL (Almasan 2022) | L02 GMR | GNN+DRL 路由优化 |
| GRouting (Wang 2021) | L01 GRLR | GNN+DRL 路由直接相关 |
| DATE (Geng 2021, IWQoS) | L04 PathGNN | DDPG 分布式多路径 TE |
| FlexDATE (Ye 2023, ToN) | L04 PathGNN | RL+SDN TE |
| LARRI (Ye 2023, INFOCOM) | L04 PathGNN | 学习型自适应范围路由 |
| FlexSATE (Liu 2024, GLOBECOM) | Handoff 缺失列表 | 分布式 TE+监督 |
| GNN-ASSSP (He 2026) | Handoff 缺失列表 | 最直接竞品 GAT+Transformer |
| DLBR (Ju 2025, TAES) | Handoff 缺失列表 | GCN+LSTM+DRL 负载均衡 |

---

## 必读论文清单（15 篇）

1. GNN-ASSSP (He 2026, Aerospace Sci Tech) — 最直接竞品
2. Knowledge-Enhanced Intent-Driven Flow Scheduling (Wang 2026, IEEE) — congestion-aware+GNN+LEO
3. GRLR (Zhang 2025, TVT, 44cit) — GNN+RL mega LEO routing ✅ L01
4. GDRL-SFCR (Chen 2025, Sensors, 11cit) — GNN+DRL routing + SFC ✅ L05
5. GMR/GNN-MPTE (Huang 2024, TVT, 41-56cit) — GNN multipath TE ✅ L02
6. Inter-satellite routing GNN+DRL (Xu 2024, Access, 20cit) — delay+load joint
7. GraphSAGE+DQN LEO routing (Shi 2024, Appl Sci, 20cit) — inductive learning
8. GNN+DQN power control + load balancing (Fan 2026, Springer) — per-link ✅ L07
9. DPR (Greenwood 2026, Int J Satellite Comm) — GNN proactive congestion
10. DLBR (Ju 2025, TAES, 12-22cit) — GCN+LSTM+DRL load balancing
11. POMAP (Li 2025, IoT Journal, 2cit) — queue-aware MARL ✅ L03
12. CA-GAR (Liu 2026, Symmetry) — GAT congestion routing, non-satellite
13. FlexSATE (Liu 2024, GLOBECOM) — distributed TE + supervised
14. DTAR (Zhou 2026, arXiv) — GAT+PPO domain routing ✅ L06
15. Traffic-Aware Domain Partitioning (Zhou 2026, arXiv) — DTAR 完整版
