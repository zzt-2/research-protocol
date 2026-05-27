# 文献定位

## 1. 核心 6 篇论文完整条目

### L004 — When Adaptive Rewards Hurt: Causal Probing and the Switching-Stability Tradeoff in LEO Handover

- **作者**: 未详细记录（arXiv 预印本）
- **年份/来源**: 2026 / arXiv preprint
- **DOI/arXiv**: arXiv:2604.03562v1
- **核心方法**: PPO + MDP Architect（CUSUM 检测场景变化并生成奖励权重），对比固定/规则/MLP/LLM 四种 Architect
- **关键结论**: MLP architect 最优（已知 357.9 Mbps，未知 325.2 Mbps）；恒定权重 (342.1 Mbps) >> 动态权重 (103.3±96.8 Mbps)；LLM 在未知场景崩溃至 45.3±43.0 Mbps
- **Baseline**: M1 Fixed/M2 Rule/M3 MLP/M4 FT-LLM，均为自实现
- **开源代码**: 无
- **与本研究关系**: 直接相关——切换场景的 DRL 奖励设计方法论，揭示切换-稳定性困境
- **精读状态**: 精读

### L029 — Dueling DDQN-Based Adaptive Multi-Objective Handover Optimization for LEO Satellite

- **作者**: 未详细记录（获 NSTC 资助）
- **年份/来源**: 2026 / arXiv preprint
- **DOI/arXiv**: arXiv:2605.02416v1
- **核心方法**: Dueling DDQN（Q=V+A-mean(A)），多目标自适应加权和奖励，专家轨迹初始化
- **关键结论**: 吞吐量 +238% vs MVT，+100% vs MAC；近零阻塞；接近 Pareto 前沿
- **Baseline**: MVT, MAC, GBW, MSH, MSHBO, DDQN（自实现）
- **开源代码**: 无
- **与本研究关系**: 直接相关——Dueling DDQN 切换方案，B2 baseline 实现基础
- **精读状态**: 精读

### L018 — Collaborative Ground-Space Communications via Evolutionary Multi-Objective Deep Reinforcement Learning

- **作者**: Geng Sun 等（吉林大学团队）
- **年份/来源**: 2024 / IEEE JSAC Vol.42 No.12 pp.3395-3411
- **DOI**: 10.1109/JSAC.2024.3459029
- **核心方法**: DCB + LEO 选星 + 功率分配 + 切换控制三目标 MOMDP；EMODRL-ED3QN 进化多任务产出 Pareto 策略集
- **关键结论**: 上行速率 1.87×10^7 bps 接近 ARGP 上界，能耗和切换次数远低于 ARGP
- **Baseline**: Non-DCB, ARGP, EMODRL-D3QN/DDQN/PPO/TD3/SAC/Noisy-DQN
- **开源代码**: 无
- **与本研究关系**: 直接相关——多目标切换+DRL，引用中枢（47 前向引用），L016 前作
- **精读状态**: 精读

### L016 — Joint AoI and Handover Optimization in Space-Air-Ground Integrated Networks

- **作者**: Geng Sun 团队（L018 同组后续工作）
- **年份/来源**: 2026 / IEEE TMC (IEEE Transactions on Mobile Computing)
- **DOI**: 10.1109/TMC.2026.3668195
- **arXiv**: 2509.12716v1（预印本版本）
- **发表状态**: 正式发表
- **发表渠道**: IEEE TMC
- **核心方法**: DD3QN-AS——动作分解 + Transformer 状态编码器 (STE) + 扩散模型 (DLPG)，最小化 AoI 和切换频率
- **关键结论**: AoI -1.7%，切换频率 -15%（vs DDQN）；收敛最快方差最小
- **Baseline**: Random, EWG, RR, PPO/SAC/TQC/DQN/DDQN/D3QN
- **开源代码**: 无
- **与本研究关系**: 直接相关——LEO 切换+DRL+Transformer+扩散模型，L018 同团队后续
- **精读状态**: 精读

### L024 — Handover Protocol Learning for LEO Satellite Networks: Access Delay and Collision Minimization

- **作者**: 未详细记录
- **年份/来源**: 2023 / IEEE TWC (IEEE Transactions on Wireless Communications)
- **DOI**: 10.1109/TWC.2023.3342975
- **arXiv**: 2310.20215（预印本版本）
- **发表状态**: 正式发表
- **发表渠道**: IEEE TWC
- **核心方法**: DRL 切换协议 DHO，跳过 MR 步骤，serving-SAT 预测 UE 信道；IMPALA + V-trace
- **关键结论**: RB 充足时接入时延 -6.8x vs 传统 HO；IMPALA 高维动作空间收敛稳定性 >> DQN
- **Baseline**: Conventional HO (3GPP A3), Random, DHO-Centralized, DQN/PPO/A3C
- **开源代码**: 无（仅伪代码）
- **与本研究关系**: 直接相关——LEO 切换协议+DRL，协议层创新
- **精读状态**: 精读

### L022 — Collaborative Deep Reinforcement Learning for Resource Optimization in Non-Terrestrial Networks

- **作者**: 未详细记录
- **年份/来源**: 2023 / IEEE PIMRC
- **DOI**: 10.1109/PIMRC57407.2023.10294047
- **arXiv**: 2402.04056v2（预印本版本）
- **发表状态**: 正式发表
- **发表渠道**: IEEE PIMRC
- **核心方法**: 双时间尺度协作 DRL——卫星大尺度（波束+RB 候选集）+ UE 小尺度（接收波束+RB），TRPO + 卫星有限步 rollout
- **关键结论**: 顺序策略更新 >> 独立训练；卫星端仅需有限步 rollout
- **Baseline**: Independent DRL, Single-estimation, BFS-Greedy/MAB, PBU-Greedy/MAB
- **开源代码**: 无（仅伪代码）
- **与本研究关系**: 方法可借鉴——双时间尺度 MDP 建模和协作 DRL 框架
- **精读状态**: 精读

## 2. 四路线分类体系

| 路线 | 论文 | 核心特征 | 局限 |
|------|------|---------|------|
| A: 标准 DRL 切换 | L029 (Dueling DDQN), L024 (IMPALA) | 切换建模为 MDP，选择 DRL 架构直接输出动作，核心在状态/奖励设计 | 可扩展性受限（L029 flat obs 1585 维，L024 高维动作空间）|
| B: DRL + 奖励/元级优化 | L004 (PPO + Architect) | 不改 DRL 架构，研究奖励权重自适应设计 | 揭示权重稳定性比质量更关键的悖论，自适应反而有害 |
| C: 进化/生成式 AI 增强 | L018 (EMODRL-ED3QN), L016 (DD3QN-AS) | 进化多目标框架产出 Pareto 集 / Transformer+扩散模型增强表征 | 同组工作演进，仿真规模小（10 UE），无开源代码 |
| D: 多 agent 协作 | L022 (双时间尺度), L018 (分布式多任务) | 时间尺度分解降低卫星计算 / 多任务并行协作 | UE 端承担训练负担，实际部署挑战大 |

## 3. 竞品精确区分

### 3.1 Lee & Lim 2025 (ICT Express) — **最直接竞争者**

- **标题**: Handover strategy for LEO satellite communication using graph neural network
- **DOI**: 10.1016/j.icte.2025.01.009
- **完整方法描述**: UE-卫星二部图建模，分布式 GNN（T=2 层 FCN 消息传递），softmax 输出选星概率，卫星侧 ACK 负载控制（超过容量拒绝连接）。训练 50 UE × 9600 samples，Adam lr=1e-5，batch=4，损失函数 L = -1/|B| Σ[p·log₂(1+SINR)] + ω·Σ(ReLU(Σp - P))。仿真 22×72=1584 星 + STK，建边条件 elevation ≥ 25°。
- **与本研究重叠要素**: UE-卫星二部图结构、GNN 编码、多 UE 联合决策、负载均衡目标
- **缺失要素**: (1) 无 DRL——纯 GNN softmax 选星（分布式决策），无 Q 值或策略梯度学习；(2) 无 size generalization 实验或理论分析——可扩展性声明仅基于 GNN 固有置换不变性；(3) 无切换惩罚——奖励函数不含切换成本项；(4) 全文未获取，架构细节未完全确认
- **与本研究的关键差异**: (1) **决策机制**: Lee & Lim 采用分布式 softmax 监督学习，每个 UE 独立通过 GNN 输出选星概率；本研究采用集中式 Dueling DDQN，中心控制器统一决策，具备时序信用分配能力；(2) **学习范式**: 监督学习 vs 强化学习——本研究通过 reward 信号端到端优化切换策略（含阻塞惩罚和切换惩罚），Lee & Lim 的损失函数仅优化 SINR+负载；(3) **可扩展性验证**: 本研究提供 size generalization 实验验证（20→100 UE），Lee & Lim 仅为 GNN 固有性质声明
- **威胁级别**: 低-中（最直接竞争者：二部图 GNN 先例）。图结构重叠但决策机制根本不同（分布式监督学习 vs 集中式 DRL），可扩展性仅为声明而非实验贡献

### 3.2 Eydian et al. 2025 (IEEE OJCOMS)

- **标题**: 加权二部图匹配 + 滞后余量 LEO 切换
- **DOI**: 10.1109/OJCOMS.2025.3541962
- **完整方法描述**: 加权二部图建模 UE-卫星关联，使用 KM (Kuhn-Munkres) 匹配算法求最优分配，结合滞后余量 (hysteresis margin) 控制切换频率
- **与本研究重叠要素**: 二部图建模思路
- **缺失要素**: (1) 无 GNN——经典图匹配优化；(2) 无 RL——完全非学习方法；(3) 无 size generalization
- **威胁级别**: 低。经典优化方法，与本研究学习方法路线完全不同

### 3.3 Yu et al. 2024 (MDPI Aerospace)

- **标题**: A Graph Reinforcement Learning-Based Handover Strategy for Low Earth Orbit Satellites under Power Grid Scenarios
- **DOI**: 10.3390/aerospace11070511
- **URL**: https://www.mdpi.com/2226-4310/11/7/511
- **完整方法描述**: 有向切换路径图（非二部图），边级 MPNN 消息传递（M 函数为 FCN，聚合为逐元素求和，更新为 RNN），DQN 输出路径级选择。单用户电力巡检场景，AHP 固定权重奖励 [throughput=0.1095, delay=0.3090, load=0.5815]，SGD lr=0.001，buffer=4000，收敛约 1700 episodes
- **与本研究重叠要素**: GNN + DRL 切换决策
- **缺失要素**: (1) 有向图非二部图——图语义完全不同（路径选择 vs 关联匹配）；(2) 单用户场景——无多 UE 竞争和负载均衡；(3) 边级传递非节点级——消息传递对象不同；(4) 无 size generalization；(5) 仿真规模极小（15 星）
- **威胁级别**: 低-中。GNN+DRL 组合重叠，但图结构、场景、规模均不同

### 3.4 Kim et al. 2022 (IEEE TWC, BGNN)

- **标题**: BGNN — 二部图 GNN 波束赋形 + 跨规模可扩展
- **DOI/arXiv**: arXiv:2207.05364
- **完整方法描述**: 二部图 GNN 用于 MISO 干扰信道的波束赋形，利用 GNN 置换等变性实现跨用户数规模的可扩展部署。前向引用 50 篇，其中 3 篇有代码（ICGNN TMC 2025、Recursive GNNs TMLCN 2024、GNN Beamforming TWC 2024）
- **与本研究重叠要素**: 二部图 GNN 架构思想、跨规模可扩展性叙事
- **缺失要素**: (1) 非切换场景——波束赋形问题；(2) 无 DRL——纯 GNN 方法；(3) 无 LEO 卫星——地面 MISO 信道
- **威胁级别**: 低-中（理论先驱，非直接竞争者）。BGNN 奠定了二部图 GNN 可扩展性的理论基础，本研究将其迁移到切换+DRL 场景

### 3.5 空隙确认总表

| 要素 | Yu 2024 | Lee 2025 | Kim 2022 | 本研究 |
|------|---------|----------|----------|--------|
| 二部图 | ✗（有向路径图） | ✓ | ✓ | ✓ |
| GNN 编码 | ✓（边级 MPNN） | ✓（FCN 消息传递） | ✓（二部图 GNN） | ✓（MPNN-E） |
| DRL 决策 | ✓（DQN） | ✗（softmax） | ✗（纯 GNN） | ✓（Dueling DDQN） |
| 多 UE 负载均衡 | ✗（单用户） | ✓（50 UE） | ✓（多用户） | ✓（20-100 UE） |
| Size generalization | ✗ | ✗（仅声明） | ✓（波束赋形） | ✓（切换场景，实验验证） |
| Reward-based 学习 | ✓ | ✗ | ✗ | ✓ |

**空隙结论**: "二部图 GNN + DRL + 多 UE 负载均衡 + size generalization"四要素组合在 LEO 切换领域无完全先例。

## 4. GNN Size Generalization 理论支撑

### Shen et al. 2020

- **标题**: Graph Neural Networks for Scalable Radio Resource Management
- **来源**: IEEE TWC（引用 460）
- **核心贡献**: 理论分析 GNN 在无线资源管理中的泛化性，证明 GNN 的置换等变性使其在小规模网络训练后可迁移到大规模网络。奠基性工作。
- **与本研究关系**: 提供 GNN 无线泛化的理论基础，支撑 size generalization 叙事

### Wu, Sun & Yang 2024

- **标题**: On the Size Generalizability of GNNs
- **来源**: Science China Information Sciences, 2024（引用 13）
- **DOI**: 10.1007/s11432-023-3880-y
- **核心贡献**: 首个系统分析 GNN 规模泛化机制，揭示 mean aggregator + 激活函数选择对跨规模泛化性能的关键影响。提供 GNN 跨规模泛化的充分条件。
- **与本研究关系**: 直接指导 GNN 架构设计（为何选择 mean aggregation），理论支撑 size generalization 的合理性

### Zhou et al. 2025 (CL-GNN)

- **标题**: CL-GNN: Continual Learning + GNN for Dynamic Resource Allocation
- **来源**: IEEE TVT（引用 4）
- **核心贡献**: 持续学习 + GNN 框架，实现"小网训练 → 大网部署"范式。在动态环境中验证 GNN 的跨规模可迁移性。
- **与本研究关系**: 最直接可借鉴的"小规模训练、大规模部署"范式，但其在资源分配场景非切换场景

### Garcia Camargo et al. 2025

- **标题**: 稀疏随机几何图上的 GNN 可迁移性形式化证明
- **来源**: 未检索到正式 DOI
- **核心贡献**: 在稀疏随机几何图上形式化证明 GNN 的可迁移性，为 GNN 在网络规模变化时的性能保持提供严格数学保证。
- **与本研究关系**: 理论背书——LEO 切换图可建模为稀疏几何图，其可迁移性结论直接适用

## 5. GNN vs MLP 优势阈值文献证据

| UE/Agent 规模 | GNN vs MLP 表现 | 来源论文 |
|---------------|----------------|---------|
| N ≤ 10 | MLP 够用，GNN 优势有限 | Lee et al. 2023 (Frontiers) |
| 10 < N < 30 | GNN 开始显著优于 MLP | Lee et al. 2023, Shen et al. 2019 (IGCNet) |
| N ≥ 30-40 | MLP 可能崩溃，GNN 不可替代 | Lee et al. 2023, Eisen & Ribeiro 2020 (REGNN) |
| N=50 (本研究) | GNN +61.5% over MLP（迁移场景）| 本研究实验 (D029) |
| N=100 (本研究) | GNN +34% reward, -58% 阻塞率（同规模训练）| 本研究实验 (D028) |

关键文献说明：
- **Lee et al. 2023**: 多智能体防御，N=2→50 实验数据，N>40 时 MLP 甚至劣于随机（DOI: 10.3389/fcteg.2023.1104745, Frontiers in Control Eng.）
- **Shen et al. 2019 (IGCNet)**: 无线功率控制，MLP 在大规模网络性能急剧退化（DOI 待补）
- **Eisen & Ribeiro 2020 (REGNN)**: REGNN 参数化实现规模无关（引用 379）

## 6. 中等重叠论文列表

### 6.1 D032 新增 4 篇

| 论文 | 核心方法 | 缺失要素 | 威胁级别 |
|------|---------|---------|---------|
| **Lee 2025** (ICT Express, DOI:10.1016/j.icte.2025.01.009) | GNN + 分布式 LEO 切换 + 负载均衡（使用 UE-卫星二部图） | 无 DRL（softmax 监督学习）、size gen 仅声明（无实验验证） | **低-中（最直接竞争者：二部图 GNN 先例，差异在决策机制）** |
| **Eydian 2025** (IEEE OJCOMS, DOI:10.1109/OJCOMS.2025.3541962) | 加权二部图匹配 + 滞后余量 LEO 切换 | 无 GNN、无 RL、经典优化 | 低 |
| **Chou 2026** (arXiv:2605.02416) | Dueling DDQN 多目标 LEO 切换 | 无 GNN、无二部图、无 size generalization | 低-中 |
| **Kim 2022** (arXiv:2207.05364, IEEE TWC) | 二部图 GNN (BGNN) 波束赋形 + 跨规模可扩展 | 非切换场景、无 DRL | 低-中（理论先驱） |

### 6.2 Baseline Report §6.3 新增论文

| 论文 | 来源 | 核心方法 | 与本研究关系 |
|------|------|---------|-------------|
| Li et al. JSAC 2026 | 前向引用 L018 | LLM 协调器 + DRL 多层 LEO (FSO/RF) | JSAC 顶刊，方法前沿，间接竞争 |
| Tong et al. IEEE TAES 2025 | find-similar | A2C 五因素切换，-58% 切换 | 航空顶刊，对比基线候选 |
| Sun et al. IEEE Comm Letters 2024 | find-similar | MODQN 多目标切换 | 多目标切换直接相关 |
| Jang et al. WiOpt 2025 | find-similar | CNN-LSTM 预测 + MADQN | 预测+多 Agent 新颖 |
| DS-PPO (arXiv:2603.16470) | find-similar | 双阶段 PPO 多卫星 | MARL 方法论参考 |
| Zhu & Pan 2026 | GNN 搜索 | Graph + RL 6G 卫星波束管理 | 最新，方向一致但非切换 |
| Handover for Multi-Beam LEO | 前向引用 L018 | 多目标 RL 多波束切换（IEEE Comm Letters 2024，c=14） | 直接竞品 |
| DQN-Based Conditional HO LEO | 前向引用 L024 | DQN 条件切换 (ICET 2025) | DQN+CHO 协议相关 |

## 7. 引用格局统计

### 核心 6 篇前向引用分布表

| 论文 | 前向引用 | 说明 |
|------|---------|------|
| L018 EMODRL (JSAC 2024) | **47** | 唯一有效引用中枢，多数来自同组扩展（Geng Sun 团队） |
| L024 IMPALA DHO | 1 | — |
| L004 自适应奖励 | 0 | 太新（2026-04） |
| L029 Dueling DDQN | 0 | 太新（2026-05） |
| L016 Transformer+扩散 | 0 | 较新（2025-09） |
| L022 双时间尺度协作 | 0 | 领域小众 |

### 引用中枢识别

- **L018 EMODRL (JSAC 2024, 47 引用)**: 唯一有效引用中枢。LEO 切换直接相关约 5 篇（Multi-Beam HO c=14, LLM+DRL JSAC 2026, IoT Journal 2026, Hybrid Precoding, LAM-Guided DRL）
- **BGNN (Kim 2022, 50 引用)**: 二部图 GNN 理论先驱，前向引用中 3 篇有代码（ICGNN TMC 2025, Recursive GNNs TMLCN 2024, GNN Beamforming TWC 2024），均为波束赋形方向

### 代码仓库生态表

**最接近可复用仓库（非直接竞品）**:

| 仓库 | Stars | 场景 | 可借鉴内容 |
|------|-------|------|-----------|
| Shadab442/dqn-leo-handover-python | 57 | DQN LEO 切换 | Gym 环境可直接复用 |
| XuyangCaoUCSD/LeoEM | 133 | LEO 网络仿真器 | 实时仿真 testbed |
| SatCom-TELMA/MA-DRL_Routing_Simulator | 143 | MA-DRL 卫星路由 | 多 Agent DRL 架构参考 |
| kit-cel/HandoverOptimDRL | 16 | PPO 地面切换 | 训练 pipeline 参考 |

**GNN 方法锚点（有代码）**:

| 仓库 | 论文 | GNN 类型 | Size Generalization | 可用性 |
|------|------|---------|---------------------|--------|
| LSJ-BUAA/GNN-Scheduling-Precoding | IEEE TWC 2026 | 二部图 GNN | 有专门 `generalization/` 测试代码 | 高 |
| GraphmindDartmouth/DISGEN | ICML 2024 | 模型无关框架 | 核心贡献 | 高 |
| UNIC-Lab/GNN-Routing | arXiv 2510 | GAT+LSTM+RL | 验证大规模拓扑泛化 | 中高 |

## 8. 竞争格局确认

LEO 切换 + DRL 领域**零开源代码论文**。核心 6 篇前向引用中 0 篇附带代码。48 篇前向引用 + 57 篇 find-similar 检索中无任何开源实现。GitHub 上的 LEO 切换 DRL 代码均为独立非论文工作。

可借鉴仓库见 §7 代码仓库生态表。

## 9. 文献索引

| ID | 第一作者 | 年份 | 标题 | DOI/arXiv | URL | 精读状态 |
|----|---------|------|------|-----------|-----|---------|
| L004 | — | 2026 | When Adaptive Rewards Hurt: Causal Probing and the Switching-Stability Tradeoff in LEO Handover | arXiv:2604.03562v1 | — | 精读 |
| L016 | Sun | 2026 | Joint AoI and Handover Optimization in Space-Air-Ground Integrated Networks | 10.1109/TMC.2026.3668195 | — | 精读 |
| L018 | Sun | 2024 | Collaborative Ground-Space Communications via Evolutionary Multi-Objective Deep Reinforcement Learning | 10.1109/JSAC.2024.3459029 | — | 精读 |
| L022 | — | 2023 | Collaborative Deep Reinforcement Learning for Resource Optimization in Non-Terrestrial Networks | 10.1109/PIMRC57407.2023.10294047 | — | 精读 |
| L024 | — | 2023 | Handover Protocol Learning for LEO Satellite Networks: Access Delay and Collision Minimization | 10.1109/TWC.2023.3342975 | — | 精读 |
| L029 | Chou | 2026 | Dueling DDQN-Based Adaptive Multi-Objective Handover Optimization for LEO Satellite | arXiv:2605.02416v1 | https://arxiv.org/abs/2605.02416 | 精读 |
| C-ARTHF | Fan | 2025 | Joint Traffic Prediction and Handover Design for LEO Satellite Networks with LSTM and Attention-Enhanced Rainbow DQN | 10.3390/electronics14153040 | https://www.mdpi.com/2079-9292/14/15/3040 | 精读 |
| C-Lee | Lee & Lim | 2025 | Handover strategy for LEO satellite communication using graph neural network | 10.1016/j.icte.2025.01.009 | https://www.sciencedirect.com/science/article/pii/S259015442500062X | 粗读（全文未获取） |
| C-Yu | Yu | 2024 | A Graph Reinforcement Learning-Based Handover Strategy for LEO Satellites under Power Grid Scenarios | 10.3390/aerospace11070511 | https://www.mdpi.com/2226-4310/11/7/511 | 精读 |
| C-Kim | Kim | 2022 | BGNN: Bipartite Graph Neural Network for Beamforming | arXiv:2207.05364 | — | 仅检索 |
| C-Eydian | Eydian | 2025 | Bipartite Graph + Hysteresis Margin LEO Handover | 10.1109/OJCOMS.2025.3541962 | — | 仅检索 |
| SG-Shen | Shen | 2020 | Graph Neural Networks for Scalable Radio Resource Management | — (IEEE TWC, c=460) | — | 仅检索 |
| SG-Wu | Wu | 2024 | On the Size Generalizability of GNNs | 10.1007/s11432-023-3880-y (Science China Inf. Sci., c=13) | — | 仅检索 |
| SG-Zhou | Zhou | 2025 | CL-GNN: Continual Learning + GNN for Dynamic Resource Allocation | — (IEEE TVT, c=4) | — | 仅检索 |
| SG-Garcia | Garcia Camargo | 2025 | Sparse Random Geometric Graph GNN Transferability | DOI 待补 | — | 仅检索 |
| SG-Eisen | Eisen | 2020 | REGNN: Scalable Graph Neural Networks for Radio Resource Management | — (c=379) | — | 仅检索 |
| SG-Lee2023 | Lee | 2023 | Multi-Agent Defense GNN vs MLP Threshold | 10.3389/fcteg.2023.1104745 (Frontiers in Control Eng.) | — | 仅检索 |
| SG-Shen2019 | Shen | 2019 | IGCNet: GNN Wireless Power Control | DOI 待补 | — | 仅检索 |
| SG-Guo | Guo | 2023 | Size-Generalizable GNN for Precoding | 10.1109/VTC2023-Fall60731.2023.10333362 (IEEE VTC 2023, c≈7) | — | 仅检索 |
| S-Li | Li | 2026 | LLM-Guided DRL for Multi-Tier LEO (FSO/RF) | DOI 待补 (arXiv:2505.11978, IEEE JSAC) | — | 仅检索 |
| S-Tong | Tong | 2025 | A2C-based LEO Handover | DOI 待补 (IEEE TAES) | — | 仅检索 |
| S-Sun | Sun | 2024 | Multi-Objective RL Handover (MODQN) | DOI 待补 (IEEE Comm Letters) | — | 仅检索 |
| S-Jang | Jang | 2025 | CNN-LSTM Prediction + MADQN | — (WiOpt) | — | 仅检索 |
| S-DS-PPO | — | 2026 | DS-PPO for Multi-Satellite | arXiv:2603.16470 | — | 仅检索 |
| S-Zhu | Zhu | 2026 | Hybrid Graph-RL for Beam Management | — | — | 仅检索 |
| S-MultiBeam | — | 2024 | Multi-Beam LEO Multi-Objective RL Handover | — (IEEE Comm Letters, c=14) | — | 仅检索 |
| S-CHO | — | 2025 | DQN-Based Conditional HO for LEO | — (ICET) | — | 仅检索 |
| S-Fan2026 | Fan | 2026 | GNN + DQN ISL Routing + Power Control | — (Springer) | — | 仅检索 |
| S-Jayarajan | Jayarajan | 2025 | GNN Satellite-Cell-Gateway Assignment (GT Thesis) | — | — | 仅检索 |
| S-Wang2025 | Wang | 2025 | GNN-HLS UE-UAV Access Link Handover | — (IEEE ICCC Workshop) | — | 仅检索 |
| S-Wiriya | Wiriya | 2025 | Bipartite + D2C Satellite Handover | 10.1109/GLOBECOM59602.2025.11431740 (IEEE GLOBECOM 2025) | — | 仅检索 |

### 背景引用储备（用于第一章引言、方法背景等）

| ID | 第一作者 | 年份 | 标题 | DOI/venue | 建议用途 |
|----|---------|------|------|-----------|---------|
| B-Luong2019 | Luong | 2019 | Applications of Deep Reinforcement Learning in Communications and Networking: A Survey | IEEE COMST, c=2500 | 第一章 DRL 无线背景 |
| B-Ye2022 | Ye | 2022 | Graph Neural Networks for Wireless Communications: From Theory to Practice | IEEE Wireless Comm., c=263 | 第一章 GNN 无线背景 |
| B-6GSurvey | Zhang | 2023 | On the Road to 6G: Visions, Requirements, Key Technologies, and Testbeds | 10.1109/comst.2023.3249835 (IEEE COMST, c=1883) | 第一章 NTN/6G 背景概述 |
| B-GNNSurvey | Zhou | 2022 | Survey of Graph Neural Networks and Applications | 10.1155/2022/9261537 (c=133) | 第一章 GNN 通用背景 |
| B-GNNIoT | Asif | 2024 | Survey of GNN for IoT and NextG Networks | 10.1109/COMST.2025.3625399 (IEEE COMST, c=19) | 第一章 GNN 下一代网络 |
| B-GraphRM | Shen | 2025 | A Survey of Graph-Based Resource Management in Wireless Networks Part II: Learning Approaches | 10.1109/TCCN.2024.3508777 (IEEE TCCN, c=30) | 第一章/方法 GNN 资源管理 |
| B-DRLSatHO | Huo | 2021 | Deep RL-based Satellite Handover Scheme for Satellite Communication | 10.1109/WCSP52459.2021.9613411 (c=51) | 第一章 DRL 卫星切换先例 |
| B-AgenticGNN | — | 2026 | Agentic GNN for Wireless Communications and Networking Toward Edge AI | 10.1109/comst.2026.3651990 (IEEE COMST) | 方法章 GNN 前沿趋势 |
| B-GNNNetMgmt | — | 2022 | GNN for Intelligent Modelling in Network Management and Orchestration | 10.3390/electronics11203371 (Electronics, c=48) | 方法章 GNN 网络管理 |
| B-HybridGNN | — | 2026 | Hybrid GNN-Centric Architectures for AI-Native 6G Wireless Networks | 10.1109/COMST.2026.3681198 (IEEE COMST) | 方法章 GNN 架构趋势 |

注：B-Luong2019 和 B-Ye2022 的 DOI 未被 API 返回，使用前需手动补查（分别为 IEEE COMST 2019 和 IEEE Wireless Comm. 2022）。

### 中文期刊引用储备（学位论文必需，≥10 篇）

#### LEO 卫星切换/选星

| ID | 第一作者 | 年份 | 标题 | DOI/venue | 建议用途 |
|----|---------|------|------|-----------|---------|
| CN-01 | 朱洪涛 | 2024 | 基于用户群组的低轨卫星网络多星切换策略 | 10.11959/j.issn.1000-0801.2022078 (通信学报) | 引言/相关工作 |
| CN-02 | — | 2022 | 低轨卫星互联网多属性切换控制方法 | 10.12018/j.issn.2097-0730.20211202001 (陆军工程大学学报) | 引言/相关工作 |
| CN-03 | 郑爽 | 2024 | 低轨卫星通信网络路由技术综述 | 10.11959/j.issn.2096-8930.2022037 (天地一体化信息网络) | 引言 |

#### DRL + 卫星网络

| ID | 第一作者 | 年份 | 标题 | DOI/venue | 建议用途 |
|----|---------|------|------|-----------|---------|
| CN-04 | 李学华 | 2025 | 面向低轨卫星通信网络的联邦深度强化学习智能路由方法 | 10.11999/JEIT250072 (电子与信息学报) | 方法对比 |
| CN-05 | 陈前斌 | 2023 | 基于迁移深度强化学习的低轨卫星跳波束资源分配方案 | 10.11999/JEIT211457 (电子与信息学报) | 方法对比 |
| CN-06 | 张晨 | 2025 | 基于多智能体深度强化学习的低轨星座跳波束资源调度研究 | 10.11959/j.issn.1000-436x.2025009 (电子学报) | 方法对比 |
| CN-07 | 刘雪芳 | 2024 | 基于深度强化学习的空天地一体化网络资源分配算法 | 10.11999/JEIT231016 (电子与信息学报) | 方法对比 |
| CN-08 | 王朝炜 | 2024 | 基于决策性能评估的多波束低地球轨道卫星网络资源分配算法 | 10.11959/j.issn.1000-436x.2024040 (电子学报) | 实验对比 |

#### GNN + 无线通信

| ID | 第一作者 | 年份 | 标题 | DOI/venue | 建议用途 |
|----|---------|------|------|-----------|---------|
| CN-09 | 李硕朋 | 2021 | 图神经网络及其在通信网络领域应用综述 | 10.11936/bjutxb2021010003 (北京工业大学学报) | 方法背景 |
| CN-10 | 申滨 | 2023 | 基于加权二部图及贪婪策略的蜂窝网络D2D通信资源分配 | 10.11999/JEIT220029 (电子与信息学报) | 方法 |
| CN-11 | 杨家辉 | 2026 | 一种基于图神经网络的认知用户功率分配算法 | 10.3969/j.issn.1000-386x.2025.12.039 (计算机工程与应用) | 方法 |

#### 星地融合 / NTN

| ID | 第一作者 | 年份 | 标题 | DOI/venue | 建议用途 |
|----|---------|------|------|-----------|---------|
| CN-12 | 徐晖 | 2024 | 面向天地融合的卫星网络架构和传输关键技术 | 10.11959/j.issn.2096-8930.20200201 (天地一体化信息网络) | 引言 |
| CN-13 | 袁硕 | 2024 | 软件定义的星地融合智能无线网络 | 10.11959/j.issn.1000-0801.2021123 (通信学报) | 引言 |
| CN-14 | 彭木根 | 2024 | 面向星地融合的6G云雾化自组网 | 10.11959/j.issn.1000-0801.2024083 (通信学报) | 引言 |
| CN-15 | 武燕燕 | 2025 | 6G天地一体通感算智能协同网络资源管理技术综述 | 10.11999/JEIT250140 (电子与信息学报) | 引言 |
| CN-16 | 张美蓉 | 2024 | 高低轨卫星异构网络资源管控策略与技术研究 | 10.11959/j.issn.2096-8930.2021045 (天地一体化信息网络) | 引言/实验对比 |
| CN-17 | 郑斌 | 2025 | 密集低轨卫星网络辅助地面通信的鲁棒波束赋形方法 | 10.11999/JEIT240732 (电子与信息学报) | 实验对比 |
| CN-18 | 程一凡 | 2022 | 低轨卫星物联网场景下基于吸引子选择算法的多星负载均衡算法 | 10.12305/j.issn.1001-506X.2022.04.34 (系统工程与电子技术) | 实验对比 |

中文期刊统计：18 篇（电子与信息学报 6、通信学报 3、电子学报 2、天地一体化信息网络 3、其他 4），年份 2021-2026。

---

### 预印本发表状态验证（2026-05-16）

| ID | arXiv ID | 查询结果 | 正式发表状态 | Venue |
|----|---------|---------|-------------|-------|
| L004 | 2604.03562 | S2 venue="", CrossRef 无匹配 | **仍为预印本** | — |
| L029 | 2605.02416 | S2 venue="", CrossRef 无匹配 | **仍为预印本** | — |
| C-Kim | 2207.05364 | CrossRef DOI 10.1109/twc.2022.3193138 | **已正式发表** | IEEE TWC 2023 |
| S-DS-PPO | 2603.16470 | arXiv 无 DOI/journal metadata | **仍为预印本** | — |

核心引用预印本率：2/6 = 33.3%（L004, L029，均为 2026 年极新论文）
全文引用预印本率：3/40 = 7.5%

---

> 文献元数据最后更新：2026-05-16（改动 1：追加 18 篇中文期刊引用储备；改动 2：预印本发表状态验证完成；改动 3：C-Kim 确认 IEEE TWC 2023 正式发表）
