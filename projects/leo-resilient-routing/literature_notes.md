# Literature Notes

## 方向概述
LEO 巨型星座故障感知抗毁路由——利用 GNN 拓扑感知能力实现故障无关泛化性恢复策略。

## 调研概况
- **研究方向**：LEO 巨型星座 GNN+DRL 故障感知抗毁路由
- **检索工具**：tools/search（S2 + arXiv + Exa + Firecrawl）
- **检索关键词**：7 组（satellite network resilience/fault recovery/GNN routing/LEO fault tolerant/mega constellation survivability/rerouting failure/link failure deep learning）
- **核心文献数**：7 篇精读 + 4 篇待确认验证
- **调研日期**：2026-05-16

## 步骤进度

| Step | 状态 | 完成日期 | 备注 |
|------|------|----------|------|
| 1 检索 | ✅ | 2026-05-16 | 7 JSON, 210 条 |
| 2 获取 | ✅ | 2026-05-16 | 10/11 篇下载成功，L04(JOCN)未获取 |
| 3 精读 | ✅ | 2026-05-16 | 6 必读+1竞品(FCRMJ) |
| 3.5 补充 | ⬜ | | |
| 4a 可行性 | ⬜ | | |

## 检索来源
- 一轮检索: `search-archive/2026-05-16/satellite-network-resilience-fault-recovery-*.json`, `leo-satellite-fault-tolerant-*.json`
- 二轮深搜: `search-archive/2026-05-16/leo-satellite-fault-tolerant-*.json`, `satellite-network-link-failure-*.json`, `satellite-network-rerouting-*.json`, `satellite-network-resilience-rerouting-*.json`, `mega-constellation-satellite-survivability-*.json`, `satellite-network-survivability-disruption-*.json`
- 总计 7 个 JSON 文件，210 条原始结果

## AI 候选审查 (2026-05-16)

### 质量门槛检查
| 指标 | 结果 | 门槛 | 状态 |
|------|------|------|------|
| 去重后总数 | 168 | ≥20 | ✓ |
| 相关候选(非排除) | 37 | ≥20 | ✓ |
| 必读 | 7 | ≥5 | ✓ |
| 正式发表占比 | 62% (23/37) | ≥50% | ✓ |
| 搜索源 | 7 | ≥3 | ✓ |
| 子方向覆盖 | 4 | ≥2 | ✓ |

### 优先级分布
- 必读: 7 篇
- 建议读: 20 篇
- 待确认: 4 篇
- 备选: 6 篇
- 排除: 131 篇

### 子方向覆盖
| 子方向 | 篇数 | 代表论文 |
|--------|------|----------|
| A: DRL故障容忍路由 | 4 | DRL-driven FCRMJ(2026), Faulty Links Fast Recovery(2025), RRS-DRL(2023) |
| B: GNN+DRL卫星路由(method baseline) | 9 | GRLR(2024,58cit), TVT GNN-MARL(2025,20cit), ToN 时空GNN(2026) |
| C: 网络抗毁性/生存性分析 | 6 | 巨型星座节点故障抗毁(2025,9cit), 熵理论抗毁评估(2025,6cit), MegaReduce(2024,22cit) |
| D: 重路由/恢复机制 | 5 | SKYLINK(2026), FlexDATE(2022,24cit), WDM GNN恢复(2025) |

## 关键发现
- GNN+LEO 故障恢复仅 GROGU(2025, DTN场景非LEO ISL) 和 GNN链路可靠性(2024, SD-LEO切换非恢复) 接近，**方法空白确认**
- DRL 是当前故障恢复主流方法（90%），但缺乏拓扑感知能力
- GNN+DRL LEO 路由已有成熟工作（GRLR 58cit, TVT 20cit），方法框架可复用

---

## 精读笔记

### [L01] GRLR: Routing with Graph Neural Network and Reinforcement Learning for Mega LEO Satellite Constellations
- **DOI/来源**：10.1109/TVT.2024.3471658
- **发表状态**：正式发表
- **发表渠道**：IEEE TVT (SCI Q1/Q2)
- **年份/会议**：2025, IEEE TVT Vol.74 No.2
- **核心贡献**：将 mega LEO 星座路由建模为 MDP（最小化端到端时延），提出分布式 GRLR 算法：GAT 特征提取 + Actor-Critic 框架，4 方向转发概率输出，支持地站集中训练、星上分布式执行。
- **方法概述**：每颗卫星构建局部有向图（自身+4邻居+目的=6节点），GAT 聚合邻居信息后 Graph Norm + Global Add Pooling 得到图级嵌入，FC 决策网络输出 4 方向概率。奖励为负单跳时延 + 到达奖励/超时惩罚。
- **实验设置**：Walker-delta 720星(36×20), 570km, 70°, 4 ISL/星, 100MHz 带宽, U(0,300)包流量
- **使用的 Baseline 方法**：
  - CR (Centralized Dijkstra): 自实现，理想上界
  - DR (DRA, Ekici 2001): 引用[15], 最小跳数分布式
  - DisCoRoute (Stock 2022): 引用[17], 最短距离分布式
  - RLR (FC 替换 GAT): 自实现（消融）
- **关键结论**：GRLR ~200 episode 收敛，中位时延介于 CR 和 DR 间；GNN 特征提取消融证明 GAT 显著优于 FC。
- **与本研究关系**：方法可借鉴（GAT+Actor-Critic 分布式路由架构核心 baseline）
- **实现关键细节**：
  - 状态：经度/纬度/业务量 + ISL 距离/中断概率，Graph Norm 归一化
  - 动作：离散 4 方向（同轨±1, 跨轨±1），Softmax 采样
  - 奖励：$r_t = -d_k(i,j)$，终止时 $+\varepsilon_1$(到达)/$-\varepsilon_2$(超时)，$\gamma=0.9$
  - 网络：GAT(64) + FC(64→4), Adam lr=0.001
- **适配性分析**：
  - 适配点：局部图+GAT+Actor-Critic 分布式架构设计简洁可迁移；负时延+到达/惩罚奖励结构可参考
  - 不适配点：仅单包单路径，未考虑多流/负载均衡/ISL 容量；MSN 拓扑假设过强
  - 改进方向：扩展动作空间为 ISL 级调度，引入链路容量和多流冲突
- **开源代码**：无
- **验证状态**：已通过 DOI 确认 IEEE TVT 发表

### [L02] Fully-Distributed Dynamic Packet Routing for LEO Satellite Networks: A GNN-Enhanced MARL Approach (GraphPR)
- **DOI/来源**：10.1109/TVT.2024.3499933
- **发表状态**：正式发表
- **发表渠道**：IEEE TVT (SCI Q1/Q2)
- **年份/会议**：2025, IEEE TVT Vol.74 No.3
- **核心贡献**：提出 GraphPR 算法，LEO 路由建模为 POMDP，GAT 编码一跳感知信息，隐藏状态在邻居间共享隐式获取多跳信息，RSPH（残余最短路径跳数）机制引导探索避免环路。
- **方法概述**：每星配备 GraphPR agent（GAT 编码+4 层 FCNN DQN），GAT 隐藏状态周期性共享实现多跳信息传播。奖励含 RSPH 引导项+延迟项+终止奖励/惩罚。
- **实验设置**：倾角 70°, 570/970/1370km, 45/70/120 星, 23.28GHz, 25MHz, 包 1500B, 队列 640, TTL 30
- **使用的 Baseline 方法**：
  - DT-TTAR: 集中式 Dijkstra 快照路由
  - FDR-MARL: 分布式 MADRL，残余传播延迟引导
  - DQN-IR: 分布式 DQN，空间位置+排队延迟
- **关键结论**：70 星场景丢包率降 3.90%-91.54%，交付时间降 6.47%-40.46%；120 星推理时间 4.86ms vs DT-TTAR 76.71ms。
- **与本研究关系**：方法可借鉴（GAT+MADRL 分布式架构、RSPH 环路避免）
- **实现关键细节**：
  - 状态：轨道/轨道内索引, 3D坐标, 平均队列长度(4维), 邻居隐藏状态($R^{F'}$)
  - 动作：离散 4 方向，epsilon-greedy(ε₀=0.99→0.001)
  - 奖励：$r = 0.6 \cdot RSPH/H_k + 0.55 \cdot (\tau^q+\tau^\eta)/(\lambda_1\tau^q+\lambda_2\tau^\eta) + 0.45 \cdot \Psi/\Phi$，$\lambda_1=0.55, \lambda_2=0.45$
  - 网络：单层 GAT + 4 层 FCNN(256), DQN, lr=0.001, γ=0.9, batch=2048
- **适配性分析**：
  - 适配点：GAT 一跳编码隐式获取多跳信息机制；RSPH 距离引导设计思路
  - 不适配点：路由问题（包级逐跳转发），非 ISL 调度；每星独立 DQN 无参数共享，扩展性差
  - 改进方向：引入参数共享，利用 GNN 置换不变性
- **开源代码**：无
- **验证状态**：已通过 DOI 确认 IEEE TVT 发表

### [L03] Multi-Stage Survivable Network Slicing With Load Balancing for LEO Mega-Constellation (MS-SNS)
- **DOI/来源**：10.1109/tccn.2026.3665891
- **发表状态**：正式发表
- **发表渠道**：IEEE TCCN
- **年份/会议**：2026, IEEE TCCN Vol.12
- **核心贡献**：提出三阶段生存性网络切片框架：负载系数贪心区域选择→SAC 切片映射→贪心生存性重映射。不预留资源的恢复策略适配 LEO SWaP 约束。
- **方法概述**：CNN 滑窗将 24×66 星座划为 88 个目标区域，SAC 执行节点映射（link 映射用 BFS），故障后基于"重映射代价"（带宽×跳数）贪心重映射。
- **实验设置**：Starlink 1584星(24×66), 550km, 53°, 4500 个 5G NS(eMBB/URLLC/mMTC), Poisson 故障
- **使用的 Baseline 方法**：NRNS, NRMNS, DTANS, CDRLNS, GCNRLNS, CeDisRLNS, FLNS（共 7 个）
- **关键结论**：MS-SNS 三项指标（长期收益、收益成本比、接受率）均优于全部 7 个 baseline；负载均衡对长期性能至关重要。
- **与本研究关系**：直接相关（LEO 生存性机制，恢复策略可借鉴）
- **实现关键细节**：
  - 状态：区域局部观测 R^{100×4}（存储/计算/带宽/延迟），max-min 归一化
  - 动作：离散二值选择（Softmax 映射概率）
  - 奖励：长期平均收益-成本比
  - 网络：Actor(3FC:400-300-100), 2 Q-Critic(3FC:400-300-1), V-Critic
  - 超参：lr_V=0.001, lr_Q=0.001, lr_π=0.0003, γ=0.9, τ=0.01, batch=128
- **适配性分析**：
  - 适配点：不预留资源的恢复策略；混合启发式-RL 框架思路
  - 不适配点：网络切片（虚拟网络嵌入），非路由问题；故障模型简化（独立节点故障）
  - 改进方向：将生存性机制扩展到路由层面抗毁路径保护/恢复
- **开源代码**：无
- **验证状态**：已通过 DOI 确认 IEEE TCCN 发表

### [L05] Resilience of Mega-Satellite Constellations: How Node Failures Impact Inter-Satellite Networking over Time
- **DOI/来源**：10.1109/TCOMM.2025.3610221 / arxiv 2509.06766
- **发表状态**：正式发表
- **发表渠道**：IEEE TCOM
- **年份/会议**：2025
- **核心贡献**：提出 SATB（Service-Aware Temporal Betweenness）指标量化节点时间演变重要性；发现星座动态拓扑具有内在抗毁性，重路由是释放完整抗毁潜力的关键。
- **方法概述**：基于 contact plan 的离散时间图建模（60s 窗口），故障定义为 F=(t_f, S_f)。SATB 统计每个窗口经过该卫星的活跃服务最短路径条数。评估单/多/大规模故障对服务连通率/路径时延/其他节点 SATB 的影响。
- **实验设置**：Starlink 2000星(32+8 轨道面), 30 城市地面小区, LOS 阈值 2500km, 24h 仿真
- **使用的 Baseline 方法**：无传统 baseline（对照实验：无故障基准/单节点/多节点/大规模/大规模+重路由/地理聚集故障）
- **关键结论**：(1) 卫星网络具内在抗毁性，单/多节点故障连通率可在数窗口恢复至 100%；(2) 重路由至关重要——300 星失效仍可恢复至 100%；(3) 地理聚集故障恢复更快(~10 窗口)。
- **与本研究关系**：直接相关（巨型星座抗毁性分析框架，故障建模基础）
- **实现关键细节**：
  - 故障模型：节点(卫星)永久故障 F=(t_f, S_f)，支持单/多/大规模
  - 评估指标：SATB, 服务连通率, 路径时延, 关键节点集
  - 星座：2000 Starlink 星, 40 轨道面, LOS 动态连接(阈值 2500km)
  - 路由：Dijkstra 最短时延路径
- **适配性分析**：
  - 适配点：SATB 指标可作为 DRL 奖励信号组件；离散时间图建模方法可复用
  - 不适配点：仅最短路径路由，不考虑多路径/负载均衡；故障模型简单（仅永久节点故障）
  - 改进方向：将 SATB 扩展为 DRL 奖励组件，结合更丰富故障模型
- **开源代码**：无
- **验证状态**：已通过 arxiv+DOI 确认 IEEE TCOM 发表

### [L06] Faulty Links' Fast Recovery Method Based on Deep Reinforcement Learning (DDPG-LBBP)
- **DOI/来源**：10.3390/a18050241
- **发表状态**：正式发表
- **发表渠道**：MDPI Algorithms, 2025, 18(5), 241 (OA)
- **年份/会议**：2025
- **核心贡献**：提出 DDPG-LBBP（GRU 替换 DDPG 扩展网络）用于 SDN-WAMS 故障链路快速恢复，联合优化时延+链路利用率+丢包率；最大不相交备份路径+Backup Tag 实现数据平面快速切换。
- **方法概述**：DDPG 的 4 个网络均用 GRU 替换扩展层，Agent 输出每条链路权重 action，SDN 控制器基于权重 Dijkstra 计算。故障时通过预装的最大不相交备份路径+Backup Tag 标签快速重路由。
- **实验设置**：IEEE 30/57 节点拓扑, i7-13700H+RTX 4060, TensorFlow 1.8, Mininet+Ryu, 链路带宽 1Gbps
- **使用的 Baseline 方法**：
  - (1+2ε)-BPCA: 近似备份路径构建(Duan & Dinavahi, IEEE TII 2022)
  - FFRLI: 基于链路重要性快速故障恢复(Zhu et al., Computer Networks 2023)
  - LIR: 低中断比链路故障恢复(Liang et al., P2P NAA 2021)
- **关键结论**：IEEE 30 恢复时延 1.9-3.1ms，丢包率 ~3.8%，恢复成功率 94.5%；消融实验 ANOVA p<0.001。
- **与本研究关系**：方法可借鉴（DRL 故障恢复完整框架，多目标奖励设计思路）
- **实现关键细节**：
  - 状态：链路时延(归一化)、利用率、丢包率，$s_t = [delay_t, bandwidth_t, Loss_t]$
  - 动作：连续，每条链路一个权重值
  - 奖励：$r = 0.4 \cdot Delay' + 0.3 \cdot Loss + 0.3 \cdot Bandwidth$，时延归一化 $\frac{maxDelay - Delay}{maxDelay}$
  - 故障模型：单链路故障，SDN 检测，数据平面预装备份路径快速切换
- **适配性分析**：
  - 适配点：DRL 故障恢复完整框架；联合优化时延+负载+丢包的多目标奖励设计
  - 不适配点：SDN-WAMS 地面网络（静态拓扑），非 LEO 卫星网络；无轨道动力学/ISL 可见性
  - 改进方向：借鉴状态编码（时延+利用率+丢包）扩展为卫星网络状态（ISL 可见性+传播时延+队列）
- **开源代码**：无（Data available on request）
- **验证状态**：已通过 DOI 确认 MDPI Algorithms 发表

### [L07] Toward the Age in Forwarding: DRL Routing via Spatial-Temporal GNN (ADRLRM)
- **DOI/来源**：10.1109/TON.2025.3597928
- **发表状态**：正式发表
- **发表渠道**：IEEE ToN (CCF-A / 中科院一区)
- **年份/会议**：2026, IEEE ToN Vol.34
- **核心贡献**：提出 RAoI（Routing-aware Age of Information）新鲜度指标；PTSA 两步自适应快照切分 + STGNN（GCN+LSTM）时空特征提取；首个将 AoI 与 DRL+GNN 卫星路由结合的工作。
- **方法概述**：PTSA 先事件驱动切分拓扑（ISL 通断），再按链路距离变化度子切分。3 层 GCN 提取空间特征 + LSTM 提取时间特征，拼接后输入 DQN 逐跳 next-hop 选择。
- **实验设置**：Walker 星座 5×8=40(缩比) / 20×50=1000(大规模), 550km, 53°, STK 生成 contact table
- **使用的 Baseline 方法**：
  - OSPF: Dijkstra + TVG
  - DQN-IR: DQN 路由无 GNN (Zuo et al., VTC-Fall 2021)
  - GraphPR: GAT+DRL 无时间维度 (Ran et al., TVT 2025, 即 L02)
- **关键结论**：1000 节点场景端到端延迟降低 30-40% vs OSPF；RAoI 在所有条件下最低；跨规模(300/500/1000)泛化性良好。
- **与本研究关系**：方法可借鉴（时空 GNN 卫星路由最新工作，GCN+LSTM 架构可迁移）
- **实现关键细节**：
  - 状态：ISL 距离/可用连接时长/节点容量/队列长度/天线调整时间，经 STGNN 编码后输入 DQN
  - 动作：离散 next-hop 选择（邻居数随拓扑变化），合法动作 mask（容量不足/连接时长不够）
  - 奖励：$r_f = -\frac{1}{K}\sum_{k=1}^K \Lambda_k^{(f)}$（负 RAoI 均值），无显式归一化
  - PTSA：事件驱动(链路通断) + 距离子切分(Δd/d ≥ λ, λ=0.3)
  - 网络：3 层 GCN(MPNN) + LSTM + FC, DQN(lr=0.0001, γ=0.9, ε-decay=0.998)
- **适配性分析**：
  - 适配点：PTSA 快照策略适合拓扑动态处理；STGNN(GCN+LSTM)时空联合提取框架；局部信息路由适合分布式
  - 不适配点：RAoI 指标专用性强（面向信息新鲜度）；单智能体 DQN 扩展性受限
  - 改进方向：保留 PTSA+STGNN 特征提取，将路由 DQN 替换为适合调度动作空间的策略网络
- **开源代码**：无
- **验证状态**：已通过 DOI 确认 IEEE ToN 发表

### [P1] DRL-driven Fault-tolerant Routing Strategy in LEO Mega-constellation (FCRMJ) — 最直接竞品
- **DOI/来源**：10.1109/CISCE69494.2026.11504878
- **发表状态**：正式发表
- **发表渠道**：IEEE CISCE 2026 会议
- **年份/会议**：2026
- **核心贡献**：提出 FCRMJ 故障-拥塞耦合风险感知路由框架，首次在 LEO 星座中同时建模故障域强度和结构性拥塞敏感度；基于 Dueling D3QN 的故障域感知 DRL 路由，风险评分预筛路径集合。
- **方法概述**：故障域强度 z（故障节点=1，一跳邻居=γ 衰减）+ 节点风险系数 θ（度中心性）→ 综合风险评分 R(p)。先风险评分过滤安全路径子集，再 D3QN 选最优路径。
- **实验设置**：GW-A59 星座 480 星, Q_max=64, H_max=30, 故障率 1%-5%, PyTorch
- **使用的 Baseline 方法**：
  - Dijkstra: 经典最短路径
  - DBPR: 距离度量动态负载均衡路由
  - CPFAR: DQN + 预计算路径 + 链路状态
- **关键结论**：故障率 1%-5% 下队列和丢包率显著低于所有 baseline；代价为跳数增约 2%。
- **与本研究关系**：直接竞品（LEO 故障容忍路由 + DRL）
- **实现关键细节**：
  - 状态：队列利用率(归一化), 故障域强度向量, 度中心性风险系数, 源-目的对
  - 动作：离散路径选择（从风险评分预筛的安全路径子集中选）
  - 奖励：$r = -(0.2 \cdot Q_k + 0.3 \cdot H_k + 0.5 \cdot \rho_k)$，三项均归一化 [0,1]
  - 网络：Dueling D3QN, 2FC(256→128), ReLU, lr=0.0003, γ=0.99, τ=0.005
  - 故障模型：静态故障场景（固定故障率 1%-5%），无动态注入
- **适配性分析**：
  - **与本研究关键差异**：
    1. MLP 无拓扑感知 vs 我们用 GNN 编码器——最本质架构差异
    2. 手工设计故障域衰减系数 vs GNN 消息传递自动传播故障影响
    3. 静态故障测试 vs 动态故障注入——我们更贴近真实
    4. DQN 单 agent vs 可用 PPO/MARL——扩展性和策略表达更强
  - **本研究优势空间**：GNN 拓扑感知、可学习故障传播、动态故障场景、端到端学习拥塞风险
  - **差异化设计要求**：奖励函数必须与 FCRMJ 线性加权有明显区别；故障模型支持动态注入/恢复；强调 GNN 在未见故障模式下的泛化能力
- **开源代码**：无
- **验证状态**：已通过 DOI 确认 IEEE CISCE 2026 发表

---

## 待确认论文验证结果

### [待确认-1] DRL-driven FCRMJ → 已确认为正式发表
- **DOI**：10.1109/CISCE69494.2026.11504878
- **发表渠道**：IEEE CISCE 2026 会议论文
- **精读状态**：已完成（见上方 P1 笔记）
- **结论**：最直接竞品，使用 MLP+D3QN，无 GNN 拓扑感知，为我们留下明确差异化空间

### [待确认-2] GDRL-SFCR (2025, 16cit)
- 已确认为 MDPI Sensors OA 论文（DOI: 10.3390/s25041232），已下载但未精读
- DRL+服务功能链路由，约束建模可借鉴，非核心竞品

### [待确认-3] GROGU (2025)
- 已确认为 IEEE WiSEE 2025 会议论文（DOI: 10.1109/WiSEE57913.2025.11229839），已下载但未精读
- GNN+DRL DTN 路由，DTN 非 LEO ISL 但方法架构可迁移

### [待确认-4] Queue-Aware MARL (2026)
- 已确认为 arXiv preprint (2605.04448)，已下载但未精读
- MARL LEO 弹性路由，直接相关

---

## 综合分析

### 现有方法分类

**A. 传统/启发式路由**：Dijkstra 最短路径、DRA 最小跳数分布式（Ekici 2001）、DisCoRoute（Stock 2022）。这些方法不考虑流量负载和故障，在拥塞和故障场景下性能急剧下降，但作为经典 baseline 仍有价值。

**B. DRL 路由（无 GNN）**：DQN-IR（Zuo 2021）用 DQN 基于局部状态做逐跳路由决策；FCRMJ（Kuang 2026, CISCE）用 Dueling D3QN + 风险评分预筛做故障域感知路由；DDPG-LBBP（2025, Algorithms）用 GRU+DDPG 做 SDN 链路权重优化。共同局限是使用 MLP/FC 特征提取器，缺乏拓扑结构感知能力。

**C. GNN+DRL 路由**：GRLR（Zhang 2024, TVT, 58cit）用 GAT+Actor-Critic 做分布式 LEO 路由；GraphPR（Ran 2025, TVT, 20cit）用 GAT+DQN 做全分布式包路由；ADRLRM（2026, ToN）用 GCN+LSTM+DQN 做时空感知路由优化 AoI。这些工作证明了 GNN 在卫星路由中的有效性，但均未涉及故障场景。

**D. 生存性/抗毁性分析**：SATB（2025, TCOM）分析节点故障对巨型星座 ISL 网络的时间演变影响；MS-SNS（2026, TCCN）做生存性网络切片的重映射恢复。这些工作提供了故障模型和抗毁性评估方法，但未将 GNN 与故障恢复结合。

**E. 故障恢复机制**：FCRMJ 用风险评分预筛路径；DDPG-LBBP 用最大不相交备份路径；MS-SNS 用贪心重映射。当前故障恢复的主流方法是 DRL（90%），但缺乏拓扑感知。

### 已知局限

1. **拓扑感知缺失**：FCRMJ、DDPG-LBBP 等故障恢复方法使用 MLP，无法感知拓扑结构变化（如故障导致的邻域重组），在未见故障模式下泛化能力差。
2. **静态故障假设**：FCRMJ 仅测试固定故障率（1%-5%），不模拟动态故障注入/恢复过程，无法评估实时恢复能力。
3. **手工特征工程**：故障域强度（γ衰减系数）和节点风险系数（度中心性）依赖人工设计，难以适应不同故障模式。
4. **GNN 路由未覆盖故障**：GRLR、GraphPR、ADRLRM 三篇 GNN+DRL 路由工作均假设网络无故障运行，未验证故障场景下的性能退化。
5. **动作空间限制**：多数工作用 4 方向离散动作（假设规则网格拓扑），不适用于 ISL 动态切换/非规则拓扑。
6. **评估不充分**：多数论文缺少跨规模泛化、多种故障模式、动态故障注入的系统性评估。

### 2-3 年趋势

1. **GNN 成为卫星路由标配特征提取器**：从 2024 GRLR（GAT）到 2025 GraphPR（GAT+MARL）到 2026 ADRLRM（GCN+LSTM 时空），GNN 在卫星路由领域的采用呈加速趋势，证明其在处理动态拓扑上的优势。
2. **DRL 故障恢复从"绕行"走向"感知"**：早期工作（2023 RRS-DRL）仅让 DRL 学习避开故障节点，2025 DDPG-LBBP 引入备份路径，2026 FCRMJ 首次建模故障域影响——从被动规避到主动感知故障影响范围。
3. **时空建模日益重要**：2025 年前的工作主要关注空间特征（GNN 编码拓扑），2026 ADRLRM 引入 LSTM 做时间特征，反映卫星网络动态性需同时捕获时空两个维度。
4. **方法空白明确**：截至 2026 年 5 月，尚无工作将 GNN 拓扑感知能力与故障恢复结合——这正是本研究的定位。

### 研究背景概述

**领域发展脉络**：
- 2021-2022：传统分布式路由（DRA/DisCoRoute）主导，DRL 路由起步（DQN-IR）
- 2023-2024：GNN+DRL 路由突破，GRLR（TVT 2024, 58cit）成为方法 baseline 标杆
- 2025：GNN+MARL 成熟（GraphPR TVT 20cit），故障恢复 DRL 方法出现（DDPG-LBBP）
- 2026：时空 GNN 登顶（ADRLRM ToN），故障感知路由出现（FCRMJ CISCE）但无 GNN

**核心技术挑战**：
1. 动态拓扑下的拓扑表征（GNN 输入随轨道运动持续变化）
2. 故障场景的泛化（训练时未见的故障位置/规模/组合）
3. 分布式决策的信息瓶颈（局部观测 vs 全局最优）
4. 实时性约束（星上推理延迟 ≤ ms 级）

**本研究定位**：填补 GNN+DRL 路由与故障恢复之间的空白——利用 GNN 的拓扑感知和消息传递能力实现故障无关泛化性恢复策略，区别于 FCRMJ 的 MLP+手工风险评分方法。
