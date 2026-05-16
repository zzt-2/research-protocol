# Literature Notes — LEO Beam Hopping + GNN

## 方向概述
LEO 多波束卫星波束跳变调度——利用 GNN 建模小区间空间干扰图结构，替代 MA-DRL 的独立 agent 假设。

## 检索来源
- 一轮宽泛: `search-archive/2026-05-16/leo-satellite-spectrum-sharing-*.json`, `satellite-frequency-allocation-*.json`
- 二轮深搜: `search-archive/2026-05-16/leo-satellite-beam-hopping-*.json`, `satellite-beam-hopping-*.json`, `hts-beam-hopping-*.json`, `leo-satellite-time-slot-allocation-*.json`
- 辅助 GNN: `satellite-beam-hopping-gnn-*.json`

## 审查统计

| 优先级 | 数量 | 说明 |
|--------|------|------|
| 必读 | 13 | 近3年+正式发表+直接相关 |
| 建议读 | 30 | 近5年+正式发表+方法可借鉴 |
| 待确认 | 5 | 预印本+相关，需查正式版 |
| 备选 | 7 | 较早但基础性贡献 |
| 排除 | ~15 | 与BH/GNN方向无关 |
| **去重后总计** | **~70** | 满足≥20门槛 |

### 子方向覆盖

| 子方向 | 论文数 | 必读数 |
|--------|--------|--------|
| MA-DRL for BH（主流） | ~35 | 6 |
| 非DRL优化（Lyapunov/凸优化/MILP/遗传） | ~15 | 4 |
| GNN for 卫星通信（非BH，方法参考） | ~8 | 3 |
| 综述 | 2 | 0 |
| **GNN + BH** | **0** | **空白确认** |

### 质量门槛检查

- 去重后 ≥20 ✓ (~70)
- 覆盖 ≥3 搜索源 ✓ (S2, OpenAlex, arXiv, SerpAPI, Exa)
- 必读 ≥5 ✓ (13)
- 覆盖 ≥2 子方向 ✓ (4个子方向)
- 正式发表占比 ≥50% ✓ (~75%)

---

## 必读（13篇）

### A. 核心痛点与创新空白

**[M1] Yang et al. 2025 — Tyche: Hybrid Computation Framework for BH (JSAC)**
- 关键贡献：明确指出 **MA-DRL 在>40小区时收敛困难**，改用 MCTS-BH。37小区需12秒/决策。
- 对本方向价值：直接证实 MA-DRL 可扩展性瓶颈，是 GNN 切入点的核心论据。
- 来源文件：hts-beam-hopping-resource-allocation-multi-agent-rl.json

**[M2] Lin et al. 2025 — Novel RRA based on Graph Mapping + GAN (ICT Express)**
- 关键贡献：**唯一将图映射(graph mapping)用于BH的论文**，将无线资源特征转为图特征，再用GAN优化。
- 对本方向价值：图方法在BH领域的首次尝试，但未用GNN。我们可在此基础上引入GNN。
- 来源文件：satellite-beam-hopping-gnn-graph-neural-network.json

### B. 最新MA-DRL标杆（直接竞品）

**[M3] Gong et al. 2026 — Distributed BH-HMARL (QPLEX, TWC)**
- 分层QPLEX：卫星级小区关联 + 波束级资源调度，CRO解决离散干扰，CLA跨层注意力。
- 来源文件：leo-satellite-beam-hopping-scheduling-deep-reinforcement-lea.json

**[M4] Tesfaw & Juang 2026 — Multi-Agent DRL-Based Dynamic BH (MAPPO, TAES)**
- MAPPO + precoding 联合BH/带宽/功率/预编码，最大化最小流量满意度。
- 来源文件：satellite-beam-hopping-resource-allocation-gnn-drl.json

**[M5] Zhang et al. 2026 — Efficient Joint Beam Pattern & Power (MA Actor-Critic, TVT)**
- 分阶段：先确定波束模式最大化吞吐，再用PA agent动态分配功率。动态调整惩罚机制。
- 来源文件：hts-beam-hopping-resource-allocation-multi-agent-rl.json

**[M6] Meng et al. 2025 — Joint Beamforming & BH (MAPPO, WCL, 12 cit)**
- 混合宽波束覆盖，MAPPO解BH+功率分配。每agent只负责一个波束。
- 来源文件：hts-beam-hopping-resource-allocation-multi-agent-rl.json

### C. 高影响力/高引用基础工作

**[M7] Lin et al. 2024 — Satellite-terrestrial Coordinated QMIX-BH (90 cit)**
- 长期小区-卫星关联 + 短期QMIX多星BH决策。负载差降70%，延迟降50%。
- 来源文件：leo-satellite-beam-hopping-scheduling-deep-reinforcement-lea.json

**[M8] Zhao et al. 2025 — DT-empowered BH (TWC, 15 cit)**
- 数字孪生双层优化：DT层Actor-Critic优化BH模式，LEO层MADRL优化功率。负载差降72.5%。
- 来源文件：hts-beam-hopping-resource-allocation-multi-agent-rl.json

**[M9] Lei et al. 2024 — Spatial-temporal Resource Optimization (62 cit)**
- 自适应波束模式+灵活用户调度。帧级确定波束模式和用户关联，时隙级优化功率和调度。
- 来源文件：leo-satellite-time-slot-allocation-beam-pattern-optimization.json

### D. GNN方法参考（卫星通信，非BH）

**[M10] Zhang et al. 2025 — HGNN for LEO Downlink Interference (DynHGNN, IEEE)**
- 动态超图神经网络解决LEO下行链路干扰。构建动态超图干扰模型，HGNN优于GCN/HGNN/GNN-DDQN。
- 对本方向价值：GNN处理卫星多波束干扰的直接方法参考，图构建方式可借鉴。
- 来源文件：satellite-beam-hopping-gnn-graph-neural-network.json

**[M11] Geng et al. 2024 — Meta-learning GNN Power Allocation (IEEE, 8 cit)**
- GNN做LEO卫星功率分配，可扩展到任意波束数。Meta-learning提升不同流量分布的泛化能力。
- 对本方向价值：GNN在卫星资源分配中的成功应用，设计思路可借鉴。
- 来源文件：satellite-beam-hopping-gnn-graph-neural-network.json

**[M12] Huang et al. 2025 — GNN Empowered Wireless Communications Survey (MWC, 5 cit)**
- GNN在无线通信的全面综述：节点级/边级/图级任务分类，排列等变性、分布式部署、可扩展性分析。
- 来源文件：satellite-beam-hopping-gnn-graph-neural-network.json

**[M13] Wang et al. 2025/2026 — Cooperative Satellite BH (TWC, 35 cit)**
- 多星协作架构：DRL定BH模式，MM算法做资源分配，ISL做负载均衡。吞吐提升18.45%。
- 来源文件：satellite-beam-hopping-resource-allocation-gnn-drl.json

---

## 建议读（30篇，按子方向分组）

### MA-DRL for BH

| 编号 | 论文 | 年份 | 会议/期刊 | 要点 |
|------|------|------|-----------|------|
| S1 | Xie et al. AoI-Aware Hierarchical DRL BH | 2025 | VTC | 分层PPO：卫星级BH模式+波束级RB分配 |
| S2 | Zhang et al. DRL-Based BHS Satellite Internet | 2025 | Electron Lett | DRL调度，改善平均排队延迟和容量利用率 |
| S3 | Liang et al. Dynamic Enhanced RA with RSMA | 2025 | EEICE | RSMA+DRL跨层动态资源优化 |
| S4 | Zhao et al. MA-DQN Geographical Clustering | 2025 | EEICE | 卫星聚类+MA-DRL，增强系统容量和负载均衡 |
| S5 | Kim et al. EABH-DQN for LEO BH | 2025 | IEEE | 3GPP信道模型+有效动作选择策略 |
| S6 | Lee et al. Optimizing BH with MARL | 2025 | VTC | 联合考虑动态流量、可见卫星数和仰角 |
| S7 | Gao et al. Service Priority-Driven BH | 2025 | APNOMS | FAHP+EWM计算静态权重，PPO优化BH+功率 |
| S8 | Guo et al. Two-Stage Optimization AdaDRL | 2025 | GLOBECOM | SA做小区关联+AdaDRL做多目标BH，负载差降77.1% |
| S9 | Zhang et al. Hierarchical DRL Access Control | 2025 | ICCC | 分层MDP：接入决策+资源调度分离 |
| S10 | Liu et al. User-Level Dynamic BH DRL+GA | 2024 | VTC | 用户级BH设计，DRL估计长期值+GA定BH模式 |
| S11 | Wen et al. MA-DQN LEO BH Interference Avoidance | 2024 | IEEE | 干扰避免MA-DQN，全频复用场景 |
| S12 | Xu et al. MA-BH DT-based LEO | 2024 | Globecom Wkshps | 数字孪生+MARL，负载均衡和队列延迟 |
| S13 | Kim & Lee LSTM-DQN BH Optimization | 2026 | IEEE | 真实移动网络数据+LSTM流量预测+双agent DQN |
| S14 | Ren et al. MARL Cooperative BH LEO | 2025 | WCNC | CTDE算法，重叠覆盖区协作BH |
| S15 | Kim et al. DQN-Based Scheduling | 2025 | WCL | DQN时隙分配+高效功率分配，降功耗和复杂度 |
| S16 | Ngo et al. MA-DDPG Cognitive GEO-LEO | 2025 | LNET | 认知卫星网络，MADDPG联合BH+资源，吞吐+45% |
| S17 | Ouyang et al. Dependency-Elimination MADRL | 2025 | TCOMM | 消除feeder/user-link依赖，性能+57.7%训练复杂度-50% |
| S18 | Wang & Bu QoS-Aware MAPPO | 2025 | ICCC | MAPPO带宽+功率分配，降功耗 |
| S19 | Xu et al. Service-Driven BH MARL-VDN | 2025 | Electronics | VDN多agent协作，空间隔离抗干扰 |
| S20 | Tesfaw & Juang Multi-Agent DRL BH+Precoding | 2026 | TAES | 同M4 |

### 非DRL优化

| 编号 | 论文 | 年份 | 会议/期刊 | 要点 |
|------|------|------|-----------|------|
| S21 | Wang et al. Lyapunov Coordinated BH | 2026 | TWC | Lyapunov漂移+惩罚分解，SCA交替优化 |
| S22 | Wang et al. Dynamic Power Allocation Lyapunov | 2025 | ICC | 多星协作Lyapunov功率分配 |
| S23 | Gao et al. Joint BH Pattern & Power | 2024 | WCNC | 两步法：先BH后功率，最大最小流量满意度 |
| S24 | Abudureheman et al. BH + Frequency Reuse | 2026 | IoTJ | DRL+角度约束聚类，联合波束激活和频率分配 |
| S25 | Tang et al. Spectrum Sharing MA-LSTM-DRL | 2026 | LCOM | Dec-POMDP+CTDE+LSTM捕获时序依赖 |
| S26 | Ma et al. Multi-Satellite Cooperative Coverage | 2025 | TCOMM | 三子问题分解：波束放置、关联+功率、时隙分配 |
| S27 | Yuan et al. Joint Beam Direction Control | 2024 | TVT, 41cit | 匹配+SCA迭代，波束方向+频/时/功率联合 |
| S28 | Zamacola et al. MILP Joint Illumination+Power+Band | 2026 | IEEE | MILP整合所有自由度，时间分裂降低复杂度 |
| S29 | Jia et al. Lyapunov-based BH NGSO | 2025 | TVT, 17cit | Lyapunov在线BH+带宽+功率，队列稳定约束 |
| S30 | Zhao et al. Joint BH & RA Load Balancing DT | 2025 | ICC | DT+HPPO双层，负载差降83% |

### 特殊主题

| 编号 | 论文 | 年份 | 会议/期刊 | 要点 |
|------|------|------|-----------|------|
| S31 | Huang et al. Hybrid BH Anti-Jamming | 2025 | IEEE | 统计规划+MF-MAPPO抗干扰，势博弈+Mean-Field |
| S32 | Jeon et al. Grant-Free Random Access BH | 2025 | IEEE | BH for免授权接入，ADMM优化 |
| S33 | Geng et al. Zero-shot RGNN Beam Prediction | 2022 | IEEE | RGNN预测波束方向，参数仅60个(vs GRU 30000+) |

---

## 待确认（5篇预印本）

| 编号 | 论文 | 年份 | 来源 | 说明 |
|------|------|------|------|------|
| P1 | Xie et al. Multi-Satellite BH PPO (arXiv 2501.02309) | 2025 | arXiv, 8cit | PPO混合动作空间，需查是否已正式发表 |
| P2 | Wang et al. Resource Allocation Cooperative Satellite | 2024 | IEEE Xplore | 无DOI但有IEEE URL(10791442)，可能已正式发表 |
| P3 | Xu et al. DeepBeam Joint BH + Coverage | 2022 | IEEE Xplore (9955995) | 68cit，可能已正式发表 |
| P4 | Lin et al. Satellite-terrestrial QMIX-BH | 2024 | IEEE Xplore (10456554) | 90cit，可能已正式发表 |
| P5 | Zhang et al. DynHGNN LEO Downlink | 2025 | IEEE Xplore (11080232) | 需查正式发表状态 |

---

## 备选（7篇基础性贡献）

| 编号 | 论文 | 年份 | 引用 | 说明 |
|------|------|------|------|------|
| B1 | Lin et al. MADRL Dynamic Beam Pattern | 2022 | 169 | MA-DRL for BH开创性工作，TVT |
| B2 | Ortiz-Gomez et al. Cooperative MA-DRL VHTS | 2021 | 24 | 早期MA-DRL卫星资源管理 |
| B3 | Guo et al. Efficient Multi-Dimensional RA | 2022 | 20 | 多维资源分配(时/频/功率)，遗传算法 |
| B4 | Zhang et al. Interference Avoidance BH GEO-LEO | 2023 | 19 | GEO-LEO频谱共享+BH干扰避免 |
| B5 | Wang et al. Adaptive Beam Pattern NOMA | 2022 | 18 | NOMA+自适应波束模式，容量差降37.8% |
| B6 | Jiang et al. Low Service Latency BH DFSVO | 2023 | 1 | 公平性+时延联合优化，beam-cluster方案 |
| B7 | Geng et al. Zero-shot Beam Management LEO | 2024 | 6 | GRNN+Twin DQN零样本波束管理 |

---

## 综述（2篇）

| 编号 | 论文 | 年份 | 说明 |
|------|------|------|------|
| R1 | Kashyap & Gupta. Resource Allocation Multibeam Satellites | 2025 | BH+功率+带宽+波束宽度四维度综述 |
| R2 | Huang et al. GNN Empowered Wireless Comms (同M12) | 2025 | GNN+无线通信全面综述 |

---

## 关键发现与覆盖度分析

### 1. GNN+BH 完全空白确认
- 5个JSON文件共~150条原始结果，去重后~70条相关
- **0篇将GNN用于BH调度**
- 最接近的论文：Lin 2025 (graph mapping + GAN)，用图但非GNN
- GNN在卫星通信的成功应用（M10-M12）证明方法可行性

### 2. MA-DRL可扩展性瓶颈确认
- Yang 2025 (Tyche, JSAC) 明确指出>40小区MA-DRL收敛困难
- 多篇论文采用分层/分解策略缓解（QPLEX分层、两阶段优化等），但仍是agent-based
- 独立agent假设忽略小区间天然图结构（同频干扰边、邻接关系边）

### 3. 方向密度分析
- BH+ML领域2025年爆发增长（30+篇2025-2026年发表）
- MA-DRL（MAPPO/QMIX/QPLEX/DDPG/DQN）占52%，同质化严重
- 非DRL方法（Lyapunov/凸优化/MCTS）开始重新受到关注

### 4. 覆盖度缺口评估
- **已充分覆盖**：MA-DRL for BH、非DRL优化、GNN for satellite
- **无需补充的方向**：中文文献（BH方向以英文为主）、抗干扰（边缘主题）
- **如需深化**：GNN for terrestrial graph-based scheduling（地面网络GNN调度方法参考），但属于Step 3精读范围

### 5. 二轮深搜验证
方向侦察阶段二轮深搜已确认：119条追加检索中GNN+BH=0。本轮Step 1-2复用已有结果并补充AI审查，结论一致。

---

## 精读笔记

### [L01] Tyche: A Hybrid Computation Framework of Illumination Pattern for Satellite Beam Hopping
- **DOI/来源**：arXiv: 2512.09312
- **发表状态**：正式发表
- **发表渠道**：IEEE JSAC (SCI Q1, IF 16.x)
- **年份/会议**：2025 IEEE Journal on Selected Areas in Communications
- **核心贡献**：(1) 提出 Tyche 混合计算框架，将波束跳变照亮模式计算分为在线（贪心-BH，毫秒级）和离线（MCTS-BH，高吞吐量）两条路径；(2) 设计 MCTS-BH 算法将照亮模式计算转化为序贯小区选择问题，用 MCTS 搜索树逐个选择服务小区；(3) 实验验证 MADRL-BH 在 >40 小区时无法收敛，首次用实证数据指出 DRL 方法的可扩展性瓶颈
- **方法概述**：MCTS-BH 将照亮模式分解为 K 次 MCTS，每次选择 1 个服务小区，通过随机游走仿真评分，UCB 选择-扩展-仿真-回传四步循环。滑动窗口评分算法将 CCI 计算复杂度从 O(n²) 降至 O(n)，剪枝算法加速 MCTS 收敛（迭代次数减少最高 74%）。
- **实验设置**：GEO 卫星 H=36000km, Ka 20GHz; 小区数 N={37,61,91,127}, 波束数 K=N/4; 时隙 100ms; 波束功率 27dBW; 3dB波束宽度 1.5°; 发射增益 40.3dBi, 接收增益 31.6dBi; TTL=20 时隙; 天线方向图参考 3GPP TR 38.811; MCTS 最大迭代 {200,300,400}; GA 种群 500/代数 50
- **使用的 Baseline 方法**：
  - R-BH（随机选 K 个小区）: 自实现
  - P-BH（轮询调度）: 自实现
  - G-BH（贪心选业务量最大 K 个小区）: 自实现
  - GA-BH（遗传算法，种群500/代数50）: 自实现
  - MADRL-BH（参考论文复现，仅37小区场景）: 引用后自实现
- **关键结论**：(1) MADRL-BH 在 37 小区/9 波束吞吐量最差，部分低于 R-BH，验证 >40 小区不可用；(2) MCTS-BH 在 127 小区吞吐量比 GA-BH/R-BH/G-BH/P-BH 分别提升 20.85%/49.90%/81.97%/98.76%；(3) 优化后 MCTS-BH 在 127 小区计算时间比 GA-BH 减少 81.09%
- **与本研究关系**：直接相关（痛点论证）— MA-DRL >40小区收敛困难的核心证据
- **实现关键细节**：
  - 评分归一化：$S' = \sum_{n=1}^{N} \omega_t^n / \omega_{max}$，最大值归一化
  - 剪枝选择值：$\mu_i = d_t^n/d_{max} + \sum_{j \in N'} D_{i,j}/D_{max}$，最大值归一化
  - SINR：$P_k |h_{k,n}|^2 / (k_B T_{rx} B_k + \sum_{l \in S} P_l |h_{l,n}|^2)$，全频复用
  - 信道容量：Shannon 公式 $C_t^n = x_t^n \cdot B_k \cdot \log_2(1+\text{SINR}_n^t)$
  - 等功率分配 $P_k^b = P_{tot}/K$
- **结构化提取**：
  - **状态空间**：各小区队列数据量 $d_t^n$（归一化: 除以 $\omega_{max}$）| 已选小区集合 $N'$ | 未选小区集合
  - **动作空间**：离散，每次 MCTS 选 1 个小区加入已选集合 | 维度随未选小区递减 | 剪枝后仅保留 top-K 候选
  - **奖励函数**：$S' = \sum \omega_t^n / \omega_{max}$（最大值归一化）| 无权重项，纯吞吐量求和
  - **建模假设**：GEO 单星静止轨道（无轨道动力学）| 每小区单用户聚合 | 全频复用+空间隔离 | 等功率分配 | TTL=20 时隙 | 3GPP TR 38.811 天线方向图
  - **网络架构**：非 DL 方法。MCTS: UCB 选择 + 剪枝扩展 + 随机游走仿真 + 累积评分回传
- **信道模型参数表**：
  | 链路类型 | 模型 | 关键参数 | 来源 |
  |---------|------|---------|------|
  | 前向链路 | 自由空间路径损耗+天线增益 | f_c=20GHz, H=36000km, P_b=27dBW, θ_b=1.5°, G_m=40.3dBi, G_rx=31.6dBi | §IV-A Eq.(3), Table II |
  | SINR | 干扰受限 | 全频复用, S 为同频波束集合 | §IV-A Eq.(4) |
  | 信道容量 | Shannon | $C_t^n = x_t^n B_k \log_2(1+\text{SINR})$ | §IV-A Eq.(5) |
- **适配性分析**：
  - 适配点：MA-DRL >40小区收敛困难的实证数据，直接支持 GNN 切入点论据；MCTS 序贯决策框架可启发 GNN+DRL 混合架构
  - 不适配点：GEO 静态拓扑 vs LEO 动态拓扑；MCTS 计算时间长（127小区~159s 优化后），不适合 LEO 在线决策
  - 改进方向：将 MCTS 仿真评分替换为 GNN 快速评估，$O(n)$ 仿真降为 $O(1)$ 前向推理
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L02] Interference-Suppressed Joint Channel and Power Allocation for Downlinks in Large-Scale Satellite Networks: A Dynamic Hypergraph Neural Network Approach
- **DOI/来源**：10.1109/twc.2025.3586230
- **发表状态**：正式发表
- **发表渠道**：IEEE TWC (SCI Q1)
- **年份/会议**：2025 IEEE Transactions on Wireless Communications
- **核心贡献**：(1) 提出基于动态超图（Dynamic Hypergraph）的干扰建模方法，将多波束 LEO 卫星下行链路中的波束间干扰和波束内干扰统一建模为超边，精确刻画多波束覆盖和用户参与变化导致的干扰关系演化；(2) 设计 HGNNRA 算法，通过 Dyn-HGNN（GRU 驱动的权重演化 + HGNN 卷积层）联合优化信道分配（离散 one-hot）和功率分配（连续 Sigmoid 缩放）
- **方法概述**：将 LEO 多波束下行干扰问题建模为动态超图，每个时隙构建一个超图快照，超边聚合所有对某用户产生干扰的用户节点。使用 HGNN 卷积提取超图特征，GRU 跨时隙演化 HGNN 权重矩阵，通过两个 MLP 头分别输出功率和信道分配。
- **实验设置**：卫星数 K∈{2,3,4}，每颗卫星波束数 I=2，总波束 4~8；轨道高度 500km (Starlink)；载波 20GHz (Ku/Ka)，带宽 20MHz，子信道 M=4；天线口径 D=1m，3dB角 10.5°，接收增益 31.6dBi；每波束用户 U∈{3,4,5}；噪声 -120~-80dBm；训练快照 T=1000，epoch 500
- **使用的 Baseline 方法**：
  - GCN: 引用 Marwani & Kaddoum 2024，自实现
  - HGNN: 引用 Liu et al. 2024，静态 HGNN 功率分配，自实现+扩展
  - GNN-DDQN: 引用 GNN+DDQN RL 方法，自实现
  - GCNRA: 将 HGNNRA 的 HGNN 层替换为 GCN 层（消融），自实现
- **关键结论**：(1) HGNNRA 在传输速率上显著优于所有 baseline，最大提升约 130Mbps；(2) 动态架构是性能关键：GCNRA > 静态 HGNN/GCN，说明动态性比图类型更重要；HGNNRA > GCNRA 说明超图建模更精确；(3) HGNNRA 在高功率场景 SINR 饱和，速率稳定在 ~700Mbps
- **与本研究关系**：方法可借鉴—超图干扰建模+GRU 动态权重演化+双 MLP 头（离散+连续）架构设计
- **实现关键细节**：
  - 损失函数：$\mathcal{L} = -\frac{1}{T}\sum_t \frac{1}{U^t}\sum_u (2R_u^t - R_u^*)$，按时间和用户平均
  - 功率输出：Sigmoid × p*，映射到 (0, p*)
  - 信道输出：Softmax → one-hot（argmax）
  - 优化器：Adam, lr=1e-5, weight_decay=1e-6
  - 隐藏层 n_h=32, HGNN 层数 L=2
  - 超图拉普拉斯归一化：$D_v^{-1/2}HWD_e^{-1}H^TD_v^{-1/2}$
- **结构化提取**：
  - **状态空间**：节点特征 n_i=4 (CSI, R_u*, C_u^t, 干扰用户数) | 未归一化直接输入
  - **动作空间**：混合（M=4 子信道离散 one-hot + 1 维连续功率）| 约束：单用户单波束单子信道，功率 ≤ p*
  - **奖励函数**：非 RL，直接优化 $\max \sum_u R_u^t$ | 归一化：1/T × 1/U^t | 权重：速率项 2，需求项 -1
  - **建模假设**：所有波束宽度相同 | 完美 CSI | 用户随机选波束（不做关联优化）| 每卫星固定 2 波束 | 星间信息传输忽略开销 | CCU 集中式训练推理
  - **网络架构**：HGNN 卷积×2 (n_i=4→n_h=32→32) + GRU 权重演化 + MLP-f (32→n_h→M=4, Softmax) + MLP-p (32→n_h→1, Sigmoid×p*)
- **信道模型参数表**：
  | 链路类型 | 模型 | 关键参数 | 来源 |
  |---------|------|---------|------|
  | 卫星→用户 | 自由空间损耗+天线增益 | f_c=20GHz, h=500km, D=1m, θ_3dB=10.5°, G_rx=31.6dBi | §III.A.1, Table II |
  | SINR | 含波束内+波束间干扰 | $\gamma_u = \|pha\|^2/(\sigma^2 + I_u)$ | §III.A.3 Eq.(8) |
  | 容量 | Shannon | $R_u = B\log_2(1+\gamma_u)$, B=5MHz/子信道 | §III.A.3 Eq.(10) |
- **适配性分析**：
  - 适配点：超图干扰建模方法（超边=一对多干扰关系）可直接迁移到 BH 场景；GRU 跨时隙权重演化机制适合 LEO 动态拓扑
  - 不适配点：监督学习直接优化，非序贯决策框架；规模过小（4~8 波束，12~20 节点）；不做用户关联优化
  - 改进方向：将超图建模+GRU 动态机制嵌入 DRL 框架，用超图表征状态空间干扰拓扑，DRL 做序贯调度决策
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L03] Meta-Learning for Graph Neural Network-Based Power Allocation in LEO Satellite Communications
- **DOI/来源**：10.1109/tvt.2024.3477601
- **发表状态**：正式发表
- **发表渠道**：IEEE TVT (SCI Q2)
- **年份/会议**：2024 IEEE Transactions on Vehicular Technology
- **核心贡献**：(1) 提出基于 GNN 的功率分配策略，将 LEO 卫星多波束干扰拓扑建模为图（节点=通信链路，边=干扰链路），利用领域知识设计聚合函数为干扰功率求和（SUM），使 GNN 可扩展到任意波束数；(2) 引入 meta-learning（soft combination 更新规则）训练 GNN，在未见流量分布场景下 zero-shot 即达接近有监督训练的性能
- **方法概述**：将多波束功率分配建模为图上函数逼近 p=F(r,H)，用 MPNN 学习从流量需求和信道增益到功率分配的映射。无监督损失（最大化满足的速率总和），通过 meta-learning 在多种流量分布上训练获得强泛化能力。
- **实验设置**：Starlink LEO 卫星，高度 1150km，载频 11.45GHz；天线阵列 49×49 (2401 单元)；最大发射功率 40dBm，噪声功率 -97dBm；19 小区（默认），3dB 波束宽度 2.15~2.45°；三种流量分布（均匀/指数/空间相关）；Meta-training: I_meta=3 轮，每轮 N_sgd=5000 步 SGD，每步 N_B=50 样本
- **使用的 Baseline 方法**：
  - FNN（全连接网络）: 自实现，输入 [r_i, |h_i^H w_i|^2, 干扰增益和]，输出 N_C 功率值
  - EPA（等功率分配）: 自实现，p_i = p_max / N_C
  - WMMSE: 引用 Shi et al. 2011 (IEEE TSP)
  - Upper Bound: 理论上界 = sum(r_i)
- **关键结论**：(1) GNN 比 EPA 和 WMMSE 高出最多 30% 可达速率，接近上界；(2) 非均匀流量下 WMMSE 最差（优化 sum-rate 而非 min(s_i,r_i)）；(3) GNN 在 19 小区训练后可直接部署到 7/19/37/61 小区，保持 20~30% 增益；FNN 不可扩展；(4) Meta-learning 后 zero-shot 性能接近 fully-trained，随机初始化需 3000+ 迭代才收敛
- **与本研究关系**：方法可借鉴—GNN 建模干扰拓扑+无监督学习+meta-learning 泛化框架可直接迁移
- **实现关键细节**：
  - 损失函数（无监督）：$L(\Theta) = -\mathbb{E}_{r,H}\sum_{i=1}^{N_C}\min(s_i, r_i)$
  - 用户容量：$s_i = \log_2(1 + |\sqrt{p_i}h_i^Hw_i|^2 / (\sum_{j\neq i}|\sqrt{p_j}h_i^Hw_j|^2 + \sigma_n^2))$
  - 功率输出：softmax 归一化后 × p_max，天然满足总功率约束
  - Meta 更新：$\Theta^{<l+1>} = \rho\Theta^{<l>} + (1-\rho)\frac{\sum_{k\in B_l}\Theta_{l,k}}{|B_l|}$
  - 消息聚合用 SUM（干扰功率求和）替代通用 FNN，减少参数量
  - 嵌入维度=8，隐藏层=16/32
- **结构化提取**：
  - **状态空间**：节点特征 (r_i, |h_i^Hw_i|^2) | 边特征 (|h_i^Hw_j|^2) | 未归一化直接输入
  - **动作空间**：连续，N_C 维功率值 | softmax × p_max 保证 sum(p_i) ≤ p_max
  - **奖励函数**：无监督 $-\sum_i\min(s_i, r_i)$ | 无额外权重
  - **建模假设**：每小区正交子信道（小区内无干扰）| Rician 衰落 LoS 为主 | 码本波束成形（预编码固定）| 全频复用 | 准静态信道 | 流量分布固定
  - **网络架构**：MPNN: Phi(8→16→1) + SUM 聚合 + U(10→16→8) + Omega(9→32→32→1) | SGD, lr 未明确
- **信道模型参数表**：
  | 链路类型 | 模型 | 关键参数 | 来源 |
  |---------|------|---------|------|
  | 卫星→用户 | 自由空间路径损耗+Rician | f_c=11.45GHz, h=1150km, K_R (Rician) | §II.B Eq.(1) |
  | 天线阵列 | UPA 49×49 | 2401 单元，Kronecker 积阵列响应 | §II.B Eq.(2)-(4) |
  | 波束预编码 | 码本波束成形 | $w_i = \sqrt{N_A N_Z}\cdot v(\psi_A^i, \psi_Z^i)$ | §II.B Eq.(5) |
  | 系统参数 | — | p_max=40dBm, σ_n²=-97dBm, θ_3dB=2.15~2.45° | §IV.A, Table II |
- **适配性分析**：
  - 适配点：GNN 干扰拓扑建模方式（节点=链路，边=干扰）可迁移到 BH（节点=波束，边=同频干扰）；无监督损失+meta-learning 框架不需标签且处理分布漂移
  - 不适配点：连续功率分配 vs BH 离散调度；单卫星静态场景，不考虑 ISL/路由
  - 改进方向：将 GNN 拓扑建模+meta-learning 与离散动作空间结合，用 GNN 作为 DRL 策略网络骨干输出离散调度决策
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L04] A Novel RRA Scheme for Beam-Hopping 6G Satellite Internet Network Based on Graph Mapping and GAN
- **DOI/来源**：10.1016/j.icte.2025.03.002
- **发表状态**：正式发表（开放获取 CC BY-NC-ND）
- **发表渠道**：ICT Express (SCI Q2)
- **年份/会议**：2025 ICT Express
- **核心贡献**：(1) 首次将 BH 无线电资源特征（时隙、频率、波束数、覆盖面积、服务状态）映射为柱状图视觉特征（柱宽、柱高、柱数、底面积、颜色），实现 RR 的连续动态多维特征描述；(2) 两级 GAN 架构：GAN1 通过对抗学习模仿 MCIR 专家策略生成候选方案，GAN2 在约束条件下通过策略梯度优化输出最优 RRA
- **方法概述**：将 RR 分配转换为柱状图优化问题，通过 graph mapping 建立 RR 特征到图像特征的映射。GAN1 学习 MCIR 调度策略分布生成候选方案，GAN2 以环境向量为输入通过策略梯度优化生成最优 RRA 向量，discriminator 提供标量奖励信号。
- **实验设置**：Ka 20GHz, LEO H=600km, 带宽 400MHz, 时隙 10ms, 窗口 256 时隙, 小区/波束数 [1,10], 每小区 10 用户, 总功率 30dBW, 发射增益 38.5dBi, PDF-U 二维高斯+泊松业务流, 训练 1300 epoch×500 步, Adam
- **使用的 Baseline 方法**：
  - MCIR (Maximum Carrier-to-Interference Ratio): 自实现（同时作为 GAN1 专家策略源）
  - RR (Round Robin): 引用 Xiong et al. 2022
  - DRL-RRA: 自实现（仅收敛对比中出现）
- **关键结论**：(1) GAN-RRA 平均用户满意度 ~98%，MCIR ~76%，提升 ~22%；(2) 吞吐量相比 MCIR 提升 ~15%；(3) 收敛优于 DRL-RRA，25000 迭代后 RMSE~0.11；(4) 低负载灵活 BHP 保证公平性，高负载受同频干扰限制
- **与本研究关系**：直接相关—唯一图方法 BH 论文，graph mapping 思想（RR特征→结构化表示）可迁移到 GNN 节点/边特征编码
- **实现关键细节**：
  - 目标函数：$\min \frac{1}{T}\sum_i |R_{B_i}^{req} - R_{B_i}^{alloc}|^2$（吞吐量差距）
  - QoS 满意度：$\max \frac{1}{T}\prod_i (R_{B_i}^{alloc}/R_{B_i}^{req})^{w_i}$
  - GAN 对抗损失：标准 min-max (Eq.14)
  - GAN2 策略梯度：$\nabla_{\theta}\eta = \frac{1}{s}\sum R_{\theta_d}(I) \times \nabla_{\theta}\log\pi_s(I;\theta)$ (Eq.15)
  - 约束：C0 时隙上限 256 | C1 分配≤需求 | C2 总功率≤30dBW | C3 干扰功率约束 | C4 波束间距≥4r
  - GAN2 架构：180×2→192→96→48→24→12，输出 RRA 向量
  - 优化器 Adam, 1300 epoch, 500 步/epoch
- **结构化提取**：
  - **状态空间**：环境向量 s 含 PDF-U 参数(σ,μ,λ_k)、服务等级(β_k,6级)、小区/波束索引 | 未明确归一化
  - **动作空间**：连续，12 维 RRA 方案向量 | 约束 C0-C4 通过 graph mapping 转换为图像约束
  - **奖励函数**：GAN 框架，非 RL。Discriminator 输出 $R_{\theta_d}(I)$ 基于 Eq.9/10 | 服务等级权重 $w_i$ 具体数值未给出
  - **建模假设**：单 LEO 卫星覆盖 | 用户分布二维高斯+泊松业务 | 一波束一小区互斥 | 同频干扰来自相邻波束 | 6 级服务等级
  - **网络架构**：GAN1: Conv(128→256→512)+FC(512→256→1) | GAN2: FC(360→192→96→48→24→12) | 激活函数/归一化未说明
- **信道模型参数表**：
  | 链路类型 | 模型 | 关键参数 | 来源 |
  |---------|------|---------|------|
  | 卫星→用户 | 自由空间+阴影+多径 | $h_{i,u}=L_{iu}\cdot F_{iu}\cdot M_{iu}$ | §2.2 Eq.(2) |
  | SINR | 含波束间同频干扰 | 详见 Eq.SINR | §2.2 |
  | 系统参数 | — | f_c=20GHz, H=600km, B=400MHz, P=30dBW, G_tx=38.5dBi, G_rx=0dBi | Table 2 |
- **适配性分析**：
  - 适配点：graph mapping 思想可直接迁移为 GNN 节点/边特征编码；BH 约束体系（C0-C4）可复用为 GNN 方案约束基线
  - 不适配点：GAN 框架非 RL，无法提供奖励设计参考；网络架构参考价值低（FC+Conv vs GNN）；关键超参数缺失
  - 改进方向：将 graph mapping 手工特征替换为 GNN 自动图结构学习（小区=节点，干扰=边），将 GAN 优化替换为 DRL（PPO）实现在线决策
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

---

## 综合分析

### 现有方法分类

**1. MA-DRL for BH（主流，~52%文献）**
MAPPO/QMIX/QPLEX/DDPG/DQN 等多 agent 架构，每个 agent 负责一个波束/小区。代表性工作：Gong 2026 分层 QPLEX [M3]、Tesfaw 2026 MAPPO [M4]、Lin 2024 QMIX-BH [M7]。核心瓶颈：独立 agent 假设忽略小区间天然图结构，>40 小区时收敛困难（Yang 2025 Tyche JSAC [L01] 实证）。

**2. 非DRL优化（Lyapunov/凸优化/MCTS/MILP，~21%）**
不依赖学习的传统优化方法。Yang 2025 Tyche [L01] 用 MCTS 序贯决策替代 DRL，127 小区吞吐量提升 20.85%~98.76%；Wang 2026 Lyapunov [S21]、Zamacola 2026 MILP [S28] 分别用数学规划方法。特点：可扩展性好但计算时间长（MCTS 127 小区 ~159s 优化后）。

**3. 图方法（萌芽期，<1%）**
仅 Lin 2025 graph mapping + GAN [L04] 将 RR 特征映射为柱状图视觉特征再用 GAN 优化，用户满意度从 76% 提升至 98%。但非 GNN，手工设计映射规则，不可端到端学习。

**4. GNN for 卫星通信（非BH，方法参考）**
Zhang 2025 DynHGNN [L02] 用动态超图+GRU 权重演化处理 LEO 下行干扰，HGNNRA 比 GCN/HGNN 最大提升 130Mbps。Geng 2024 Meta-GNN [L03] 用 MPNN+meta-learning 做功率分配，zero-shot 泛化到不同小区数保持 20~30% 增益。证明 GNN 在卫星资源分配中有效且可扩展。

### 已知局限

1. **可扩展性**：MA-DRL 在小区数>40 时无法收敛（[L01] 实证），分层/分解策略仅缓解不解决；MCTS 计算时间长（>100s）不满足实时需求
2. **同质化严重**：MA-DRL 方向 MAPPO/QMIX/QPLEX 反复堆叠，创新空间压缩
3. **图结构利用不足**：小区间同频干扰、邻接关系天然构成图，现有 MA-DRL 方法全部忽略这一先验结构
4. **泛化能力弱**：FNN 等固定维度方法不可扩展到训练外规模（[L03] 对比），MA-DRL 需随小区数调整 agent 数
5. **实时性瓶颈**：MCTS/GA 等非学习方法计算时间过长（[L01]: GA 127 小区 ~3873s），只能离线使用

### 2-3 年趋势

1. **2024-2025 年 BH+ML 爆发**：30+ 篇论文集中发表，MA-DRL 成为事实标准但同质化严重
2. **非DRL方法回归**：MCTS（Tyche [L01]）、Lyapunov（Wang 2026）、MILP（Zamacola 2026）重新受到关注，反映对 DRL 可扩展性的反思
3. **图方法萌芽**：Lin 2025 [L04] 首次将图表示引入 BH，虽非 GNN 但开辟了新范式
4. **GNN 在卫星通信成熟化**：DynHGNN [L02]、Meta-GNN [L03]、GNN survey [M12] 表明 GNN 处理卫星干扰/资源分配的技术栈已成熟
5. **GNN+BH 仍为零**：精读 4 篇+初筛 70 篇+二轮深搜 119 篇全部确认零 GNN+BH 工作，是明确的创新空白

### 研究背景概述

**时间线**：2022 年 Lin MADRL-BH [B1] (TVT, 169 cit) 开创 MA-DRL for BH 方向 → 2023-2024 年 MAPPO/QMIX/QPLEX 各种变体涌现（Lin QMIX-BH 90cit, Lei 时空优化 62cit）→ 2024 年底 GNN for 卫星通信开始成熟（Geng Meta-GNN [L03]）→ 2025 年 BH 方向爆发（30+篇）同时可扩展性质疑浮现（Yang Tyche [L01] JSAC），非 DRL 方法回归 → 2025-2026 年图方法首次尝试（Lin graph mapping [L04]）但 GNN+BH 仍为零。

**核心技术挑战**：(1) BH 是离散组合优化（选哪些波束照亮），状态空间随小区数指数增长；(2) 小区间同频干扰构成天然图结构，但 MA-DRL 的独立 agent 假设无法利用；(3) LEO 动态拓扑导致图结构时变，静态图方法不适用。

**本研究定位**：在 GNN+BH 空白中填入第一个系统工作——用 GNN 编码小区间干扰图拓扑，替代 MA-DRL 的独立 agent，实现可扩展、可泛化的 BH 调度。与 [L02] 的超图干扰建模、[L03] 的 meta-learning 泛化、[L04] 的 graph mapping 思想形成方法组合。

### [L05] Distributed Beam-Hopping Scheduling for LEO Mega-Constellation Networks Based on Hierarchical Multi-Agent Deep Reinforcement Learning
- **DOI/来源**：10.1109/TWC.2026.3659941
- **发表状态**：正式发表
- **发表渠道**：IEEE TWC (SCI Q1)
- **年份/会议**：2026 IEEE TWC
- **核心贡献**：(1) HMARL 分层框架：上层卫星级 cell 关联 + 下层波束级资源调度，QPLEX 单调值分解支持分布式执行；(2) Cross-Layer Attention (CLA) 注意力机制融合两层特征，Chemical Reaction Optimization (CRO) 解决离散 cell 关联冲突
- **方法概述**：分层 QPLEX + CRO + CLA 三模块协同。上层 QPLEX 输出 Q 值引导 CRO 搜索最优 cell 关联，下层 QPLEX 处理连续波束资源分配，CLA 通过注意力融合两层特征后经 monotonic mixing 输出全局 Q 值。
- **实验设置**：12 轨道×22 星 (264 星), 648 cell, 流量 20-700Mbps (Poisson), 每星最多 8 beam, 全频复用, BHTP 周期 15s, 时隙 5ms, 训练 500 episodes, batch 32, lr=1e-4, discount 0.99
- **使用的 Baseline 方法**：
  - BH-QMIX: 引用 Lin 2024 TWC，自实现
  - BH-QPL (队列长度优先): 引用，自实现
  - BH-P (周期轮询): 引用，自实现
  - BH-HDP (高需求优先): 引用，自实现
  - BH-JBSPO (集中式联合调度): 引用，自实现
  - BH-VDN: 引用，自实现
- **关键结论**：(1) 吞吐量提升 16.38%~73.65%；(2) 星座从 6×12 扩到 15×22 时平均增益从 12.38% 升至 58.24%；(3) 单 agent 执行 4.25ms < 5ms 约束；(4) 消融：去 CRO 降 13%~30%，去 CLA 降 10%~35%，去 ASS 降 21%~38%
- **与本研究关系**：直接相关（最新竞品）— 2026 TWC 分层 MA-DRL 标杆
- **实现关键细节**：
  - 奖励：$r_t = (1-\beta-\gamma)\frac{\Gamma(t)}{\Gamma_{norm}} - \beta\frac{\Psi(t)}{\Psi_{norm}} + \gamma(1-\frac{\|l(t)-\bar{l}_{N_n}(t)\|_2}{\sqrt{R_n}}) - \text{penalty}$
  - 网络架构：共享编码 FC{512,256}+GELU → 上层 Q(128)+下层 Q(128) → CLA (4-head attn, embed 64) → Mixing FC(128) → Q_tot
  - 优化器 Adam, lr=1e-4, discount 0.99
  - CRO: 分解阈值 0.8, 碰撞阈值 0.3
- **结构化提取**：
  - **状态空间**：o_t^n = [D_t^n; Q_t^n; Δ_t^n; H_t^n; L_t^n; L_t^{N_n}]，含流量需求、队列、延迟、CSI、负载、邻居负载
  - **动作空间**：混合（上层离散 cell 关联 | 下层连续波束调度），K_max=8 beams/cell
  - **奖励函数**：吞吐量(归一化Γ_norm) + 延迟惩罚(归一化Ψ_norm) + 负载均衡(L2距离) + 冲突penalty，权重 β,γ 自适应
  - **建模假设**：全频复用 | 功率均分 P/K | 复合 Poisson 流量 | 自由空间+天线方向图(无雨衰/闪烁) | Walker-Delta 星座 | 上层每 BHTP 周期更新，下层每时隙
  - **网络架构**：FC(512→256)GELU + QPLEX(128)×2 + CLA(4-head,64) + Mixing(128)，Adam lr=1e-4
- **信道模型参数表**：
  | 参数 | 值 | 来源 |
  |------|-----|------|
  | 星座 | 12面×22星, 550km, 53° | Table III |
  | 天线增益 | ITU-R S.1528 (发射), S.465-6 (接收) | Eq.(7)-(8) |
  | SINR | 含星内+星间干扰 | Eq.(9) |
  | 全频复用 | 所有活跃波束共享频段 | §II-B |
  | 功率分配 | P_n^{beam} = P_n/K (均分) | §II-B |
- **适配性分析**：
  - 适配点：分层解耦架构（长期关联+短期调度）可借鉴；QPLEX 分布式执行范式适合 LEO 自主决策
  - 不适配点：纯 FC 网络，无图结构建模；全频复用假设过强；功率均分过于简化；上层动作空间随 cell 数变化处理粗糙（null padding）
  - 改进方向：用 GAT/GIN 替换 FC+GRU 建模 cell 间邻接干扰关系，加入连续功率分配决策
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L06] Satellite-Terrestrial Coordinated Multi-Satellite Beam Hopping Scheduling Based on Multi-Agent Deep Reinforcement Learning
- **DOI/来源**：10.1109/TVT.2024.10456554
- **发表状态**：正式发表
- **发表渠道**：IEEE TVT (SCI Q2, 90 cit)
- **年份/会议**：2024 IEEE TVT
- **核心贡献**：(1) 两阶段星地协同框架：长期 cell-satellite 关联（NOCC 贪心+迭代优化）+ 短期 QMIX 多星 BH 决策；(2) 空间隔离 BH pattern 缩减动作空间，参数共享降低模型开销
- **方法概述**：NOCC 端做长期 cell-satellite 关联实现负载均衡与干扰规避；每颗卫星部署 QMIX agent（GRU+mixing network+hypernetwork），DDQN 训练，slot-by-slot BH pattern 决策。CTDE 范式。
- **实验设置**：9 星 LEO 1500km, 76 cell, 每星 15 cell, 最多 3 spotbeam; Ku 11.7GHz, 200MHz, 全频复用; 功率 13dBW 均分; Poisson 流量 RT 20-100/NRT 100-700 Mbps; 时隙 2ms, TTL=40; 训练 7000 episodes×128 步, lr=0.001, γ=0.98
- **使用的 Baseline 方法**：
  - R-BH (随机 BH): 自实现
  - P-BH (周期轮询): 自实现
  - QLP-BH (队列长度优先): 自实现
  - QDP-BH (队列延迟优先): 自实现
  - USWG-BH (最大用户服务权重增益): 引用 Wu 2022
- **关键结论**：(1) 负载均衡：负载差距降低 ~70%；(2) 网络延迟降低 ~50%；(3) 吞吐量比 R-BH 提升 92%；(4) 执行时间 ~1ms < 2ms 时隙约束
- **与本研究关系**：直接相关（基础工作）— MA-DRL for BH 高引基础，QMIX 多星 BH
- **实现关键细节**：
  - 奖励：$r_t = (1-\alpha)\frac{\sum\Gamma_t}{\Gamma_{norm}} - \alpha\frac{\sum\tau_t}{|N||I|\Psi_{norm}} - \text{penalty}$，Γ_norm=270 Mbit, Ψ_norm=40, α=0.7
  - Agent: FC(4M+|A|+N → 64)ReLU → GRU(64) → FC(64→|A|) 线性 Q 值，参数共享
  - Mixing: FC(N→64)ELU → FC(64→1)，Hypernetwork 从全局状态生成权重(Abs 保证非负)
  - DDQN, Adam lr=0.001, γ=0.98, ε-greedy 0.5→0.01, target 每 200 episodes 更新
  - 空间隔离 BH pattern: K_max=3 个 spotbeam 不相邻，大幅缩减动作空间
- **结构化提取**：
  - **状态空间**：全局 s_t∈R^{4NJ} (队列×2+延迟+CSI)，局部 o_t^n∈R^{4M} (304维)，agent 输入=[o_t^n; a_{t-1}^n; e_n]
  - **动作空间**：离散 BH pattern 索引，空间隔离缩减后 |A_n| | 约束 K≤3, spotbeam 不重叠
  - **奖励函数**：吞吐量(权重 1-α=0.3) + 延迟惩罚(权重 α=0.7) + penalty | 归一化: Γ_norm=270, Ψ_norm=40
  - **建模假设**：每星覆盖等量 cell | 功率均分 | 全频复用 | 每波束每时隙单用户 | Poisson 流量 | 无信道时变性(无衰落) | 短期固定覆盖
  - **网络架构**：FC→GRU→FC (64维) + Mixing(64→1) + Hypernetwork(Abs), Adam lr=0.001
- **信道模型参数表**：
  | 参数 | 值 | 来源 |
  |------|-----|------|
  | 轨道 | 9 星, 1500km | — |
  | 频段 | Ku 11.7GHz, 200MHz | DVB-S2X |
  | 功率 | 13 dBW 均分 | — |
  | 天线 | 3dB宽 3°, G_max^T=34.3dBi, G_max^R=33.8dBi (0.4m口径) | ITU-R S.1528, S.465-6 |
  | 噪声温度 | 300K | — |
  | SINR | 含星内+星间 CCI | 全频复用 |
- **适配性分析**：
  - 适配点：两阶段分解（长期关联+短期 BH）架构清晰可迁移；奖励吞吐量-延迟加权框架可直接迁移
  - 不适配点：MLP+GRU 无图结构感知；空间隔离 pattern 枚举不灵活（小区数增大需重新生成）
  - 改进方向：用 GNN 替换 GRU 捕获 cell 间空间关系和干扰拓扑；加入轨道运动建模做动态关联
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L07] Resource Allocation and Load Balancing for Beam Hopping Scheduling in Satellite-Terrestrial Communications: A Cooperative Satellite Approach
- **DOI/来源**：10.1109/TWC.2024.3508741
- **发表状态**：正式发表
- **发表渠道**：IEEE TWC Vol.24 No.2 (SCI Q1, 35 cit)
- **年份/会议**：2025 IEEE TWC (早期版 GLOBECOM 2024)
- **核心贡献**：(1) 多星协作 BH 三层解耦：DQN 定 BH pattern → MM 算法做频率+功率分配 → ISL 负载均衡（低负载最小化延迟，高负载均衡负载）；(2) Per-cell Q-value 降维：为每个小区输出一个 Q 值再取 top-Nb，动作空间从 C(|Ω|,Nb) 降为 |Ω|
- **方法概述**：Multi-agent Double DQN 做 BH 调度（每星一个 agent，参数共享），确定波束指向后用 MM 算法迭代解频率+功率分配，ISL 定期（每 Tb 时隙）重新规划流量分配。三层在不同时间尺度交替执行。
- **实验设置**：16 星 (4×4) LEO 1000km, 每星覆盖 37 cell (19 cell 比较), Nb=4 beam; Ka 20GHz, 8 频段×125MHz=1GHz; 时隙 10ms; 流量 35~105Mbps 随机游走; β=0.7, ρ=0.9, Tth=10, Tb=50; 仿真 2000 时隙
- **使用的 Baseline 方法**：
  - Lin 2023 Pre-scheduling BH (TCOM): 引用
  - Lin 2024 Multi-agent DRL+adjacent beam avoidance (TWC): 引用
  - Wu 2022 Maximum USWG (VTC-Spring): 引用
  - Original Benchmark (贪心最大队列优先): 自实现
  - Without DRL (贪心替代 DRL): 自实现
  - Without Resource Allocation (去掉 MM): 自实现
  - Without Load Balancing (去掉 ISL 均衡): 自实现
- **关键结论**：(1) 吞吐量比贪心基准提升 18.45%；(2) DRL 对吞吐量影响最大，负载均衡对延迟影响最大；(3) 邻星协作 vs 全网协作性能差距 <0.8%；(4) 高负载时全面占优，低负载时 USWG 延迟指标更好
- **与本研究关系**：直接相关（多星协作标杆）— per-cell Q-value 降维、三层解耦架构、邻星协作策略可借鉴
- **实现关键细节**：
  - 奖励：$r_s(n) = \frac{\beta}{Y_0}\sum_{k=1}^{N_b}y_{s,k}(n) - \frac{1-\beta}{\Gamma_0}\Delta\tau_s(n)$，β=0.7
  - 延迟指标：$\Delta\tau = \bar{\tau} - \underline{\tau} + \kappa\bar{\tau}$（最大最小延迟差+惩罚）
  - 干扰：$I_{s,k,l} = \sum_{r\neq s}\sum_j|h_{[r,j]s,k}|^2 P_b f_{r,j,l} + \sum_{j\neq k}|h_{[s,j]s,k}|^2 P_b f_{s,j,l}$（含星间+星内）
  - SINR：$\gamma_{s,k,l} = |h_{[s,k]s,k}|^2 P_b f_{s,k,l} / (B_0 n_0 + I_{s,k,l})$
  - DQN: FC(370→512→256→128→64→32→37) ReLU, Double DQN, 参数共享
- **结构化提取**：
  - **状态空间**：缓冲区队列 D_s(n) ∈ R^{|Ω|×Tth} (37×10=370) | 未归一化
  - **动作空间**：离散，输出 |Ω|=37 维 Q 值取 top-Nb=4 | 约束：单波束单小区，覆盖范围内
  - **奖励函数**：吞吐量(β=0.7, Y_0归一化) - 延迟(0.3, Γ_0归一化) | ρ=0.9
  - **建模假设**：每星覆盖等量 cell | 数据包固定 1Mbit | Poisson 到达 | 初始路由等概率 | ISL 传输单时隙完成 | 频率分配可解耦为单星 MDP | DQN 参数共享
  - **网络架构**：FC(370→512→256→128→64→32→37)×6 层 ReLU, Double DQN, 参数共享
- **信道模型参数表**：
  | 参数 | 值 | 来源 |
  |------|-----|------|
  | 星座 | 16 星 4×4, 1000km | — |
  | 频段 | Ka 20GHz, 8×125MHz=1GHz | Table I |
  | 天线 | 口径半径 0.1m | — |
  | SINR | 含星间+星内干扰 | Eq.(7)-(8) |
  | 容量 | Shannon $B_0\log_2(1+\gamma)$ | Eq.(9) |
- **适配性分析**：
  - 适配点：per-cell Q-value 降维策略适用于任意规模小区覆盖；三层解耦（DRL→优化→负载均衡）可复用；邻星协作开销可控
  - 不适配点：全连接 DQN 无空间拓扑感知；无路由感知（仅流量再分配）；单时间尺度未利用轨道周期性
  - 改进方向：用 GNN 替换 FC-DQN 利用小区邻接图做空间聚合；BH 调度与路由联合优化
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证
