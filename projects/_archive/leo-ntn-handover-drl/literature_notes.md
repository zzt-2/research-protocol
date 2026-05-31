# 文献调研记录

## 调研概况
- **研究方向**：LEO 卫星网络切换优化 + 深度强化学习方法
- **检索工具**：tools/search（S2 + OpenAlex + arXiv + SerpAPI）
- **检索关键词**：LEO satellite handover deep reinforcement learning; LEO satellite switching DRL; multi-agent DRL satellite handover; LEO NTN handover optimization
- **核心文献数**：6 篇（精读，有 content.md）
- **调研日期**：2026-05-07

## 综合分析

### 现有方法分类

**路线 A：标准 DRL 应用于切换优化**（L029, L024）
将切换决策建模为 MDP，选择合适 DRL 架构（Dueling DDQN、IMPALA）直接输出切换动作。核心在于状态/奖励设计。L029 采用 Dueling DDQN + 自适应多目标奖励；L024 采用 IMPALA + 跳过 MR 信令的协议重设计。

**路线 B：DRL + 奖励/元级优化**（L004）
不改变 DRL agent 本身架构（使用标准 PPO），而研究如何自适应设计奖励函数权重。发现权重稳定性比质量更关键的"切换-稳定性困境"，并提出 LLM 辅助奖励设计的混合架构。

**路线 C：进化/生成式 AI 增强 DRL**（L018, L016）
L018 采用进化多目标框架 + 多任务并行 DRL（EMODRL-ED3QN）产出 Pareto 策略集。L016 在 D3QN 基础上引入 Transformer 状态编码器和扩散模型进行表征增强。两者为同一核心作者团队的演进工作。

**路线 D：多 agent 协作 DRL**（L022, L018）
L022 提出双时间尺度协作框架（卫星大尺度 + UE 小尺度），利用 UE 算力辅助训练。L018 的分布式多任务框架也可视为多 agent 协作的一种形式。

### 已知局限

1. **仿真规模有限**：所有论文仿真规模（3-298 星、10-200 UE）与实际 mega-constellation（数千星、百万 UE）差距大
2. **无真实部署验证**：全部基于仿真（STK/自建），无硬件在环或真实卫星平台验证
3. **信道/环境简化**：多数假设 CSI 可获取、轨道模式已知固定、未考虑多小区干扰和 ISL
4. **可扩展性存疑**：DRL 训练随 UE/卫星数量增长，计算和样本复杂度问题未充分解决
5. **奖励设计缺乏理论**：L004 揭示自适应奖励的稳定性问题，多数论文的奖励函数设计依赖经验调参

### 2-3 年趋势

1. **从单一 DRL 到混合架构**：2023-2024 年以标准 DRL（DQN/PPO/DDQN）为主；2025-2026 年转向 DRL + Transformer/扩散模型/LLM 的混合架构
2. **从固定奖励到自适应奖励**：L029（2026）使用自适应多目标权重，L004（2026）系统探索奖励设计瓶颈，表明奖励工程正成为独立研究方向
3. **从单 agent 到多 agent 协作**：利用星地/星间分布式计算能力，通过时间尺度分解和任务卸载降低卫星端计算负担
4. **从协议改造到架构重设计**：L024 在 3GPP 框架内改进，L022/L018 重新设计协作架构

## 文献条目

### [L004] When Adaptive Rewards Hurt: Causal Probing and the Switching-Stability Tradeoff in LEO Handover
- **DOI/来源**：arXiv:2604.03562v1
- **年份/会议**：2026 / arXiv preprint
- **发表状态**：预印本
- **发表渠道**：arXiv preprint
- **核心贡献**：揭示 LEO 卫星调度中的"切换-稳定性困境"：PPO 需准稳态奖励信号收敛，任何自适应奖励权重调整都会反复重启收敛过程导致性能下降。近恒定权重 (GEN MLP, 342.1 Mbps) 大幅优于动态权重 (Oracle MLP, 103.3±96.8 Mbps)。提出单变量因果探测方法，发现切换惩罚权重具远超预期的杠杆效应。
- **方法概述**：双时间尺度架构——PPO agent 实时调度波束功率/带宽，MDP Architect 监控 KPI 用 CUSUM 检测场景变化并生成奖励权重。对比四种 Architect（固定/规则/MLP/LLM Qwen3-4B+LoRA）。奖励函数为五项加权和（速率、中断、切换惩罚、队列溢出、Jain 公平性）。
- **实验设置**：19 波束 Ka 频段卫星（600 km），含雨衰信道；4 种已知 + 3 种未知业务场景；PPO 3 层 MLP (256-256-128)，500k 步；3 随机种子。
- **使用的 Baseline 方法**：
  - M1 Fixed Weights: 离线优化静态权重（自实现）
  - M2 Rule-Based: KPI 阈值分类器（自实现）
  - M3 Learned MLP: 3 层 MLP KPI→权重（自实现）
  - M4 FT-LLM: Qwen3-4B+LoRA（自实现）
- **关键结论**：奖励权重平稳性比质量更重要；MLP architect 全面最优（已知 357.9 Mbps，未知 325.2 Mbps）；LLM 因数值振荡在未知场景崩溃至 45.3±43.0 Mbps。
- **与本研究关系**：直接相关——切换场景的 DRL 奖励设计方法论
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L029] Dueling DDQN-Based Adaptive Multi-Objective Handover Optimization for LEO Satellite
- **DOI/来源**：arXiv:2605.02416v1
- **年份/会议**：2026 / arXiv preprint（获 NSTC 资助）
- **发表状态**：预印本
- **发表渠道**：arXiv preprint
- **核心贡献**：将 LEO 切换建模为多目标优化（吞吐量/阻塞概率/切换成本），提出 Dueling DDQN 自适应多目标切换方案。Dueling 架构将 Q 函数分解为状态价值流和优势函数流，适合重叠覆盖区多候选卫星效用相近时的稳定价值估计。使用专家轨迹 (MSHBO) 初始化缓解冷启动。
- **方法概述**：基于 Telesat Lightspeed（298 星），MDP 建模：状态=候选卫星速率/负载/上一关联；动作=选卫星；奖励=三目标自适应加权和。Dueling DDQN（Q=V+A-mean(A)），DDQN 解耦选择与评估。
- **实验设置**：Telesat Lightspeed 298 星，STK 平台，最小仰角 20°，UE 10-30，卫星容量 1-9。训练 300 episodes，buffer 200k，batch 256，lr 1e-3，10 次独立运行。
- **使用的 Baseline 方法**：
  - MVT (Maximum Visible Time): 选可见时间最长卫星（引用 Papapetrou 2004）
  - MAC (Maximum Available Channels): 选可用信道最多卫星（引用）
  - GBW (Graph-Based Weighting): 图加权优化方法（引用 Hozayen 2022）
  - MSH (Minimum Satellite Handover): 最小化切换启发式（引用 Kang ICC 2024）
  - MSHBO: MSH+阻塞感知扩展（引用）
  - DDQN: 标准 Double DQN（自实现）
- **关键结论**：吞吐量比 MVT 提升 238%，比 MAC 提升 100%；典型条件下近零阻塞概率；阻塞概率-切换频率接近 Pareto 前沿。
- **与本研究关系**：直接相关——Dueling DDQN 切换方案，潜在 baseline 候选
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L018] Collaborative Ground-Space Communications via Evolutionary Multi-Objective Deep Reinforcement Learning
- **DOI/来源**：10.1109/JSAC.2024.3459029
- **年份/会议**：2024 / IEEE JSAC Vol.42 No.12 pp.3395-3411
- **发表状态**：正式发表
- **发表渠道**：IEEE JSAC (SCI Q1, IF ~16)
- **核心贡献**：提出分布式协作波束成形(DCB)+LEO 卫星选择+功率分配+切换频率控制的三目标 MOMDP 框架。通过等距离散权重参数替代连续功率变量，使动作空间维度与终端数量无关。EMODRL-ED3QN 框架通过进化多任务机制产出 Pareto 策略集。
- **方法概述**：Lemma 1 证明单时隙加权和优化凸性，DRL 只需输出权重索引和卫星选择。Enhanced D3QN + 合法动作掩码 + 进化多目标框架（MMD3QN + TPU + TS）。Warm-up + Evolutionary 两阶段迭代。
- **实验设置**：110 颗 LEO（80×500km + 30×1000km），10 地面终端，2.4GHz，60 分钟。N=10 学习任务，300 进化代，warm-up 80 次。Q 网络 2×2048。
- **使用的 Baseline 方法**：
  - Non-DCB: 单终端直连（自实现）
  - ARGP: 可达速率贪心策略（自实现，上界）
  - EMODRL-D3QN/DDQN/PPO/TD3/SAC/Noisy-DQN: 同框架不同 DRL 变体（自实现/引用）
- **关键结论**：EMODRL-ED3QN 上行速率 1.87×10^7 bps 接近 ARGP 上界，同时能耗和切换次数远低于 ARGP。DCB 使低于阈值终端实现有效上行。
- **与本研究关系**：直接相关——多目标切换+DRL，L016 的前作
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L016] Joint AoI and Handover Optimization in Space-Air-Ground Integrated Networks
- **DOI/来源**：10.1109/TMC.2026.3668195 (arXiv: 2509.12716)
- **年份/会议**：2025 / IEEE Transactions on Mobile Computing
- **发表状态**：正式发表
- **发表渠道**：IEEE TMC (SCI Q1, IF ~7.5)
- **核心贡献**：提出 AoI 感知的 SAGIN 下行架构（LEO-HAP-地面），利用 HAP 作智能中继。联合优化卫星选择+功率分配，最小化 AoI 和切换频率。DD3QN-AS 算法引入三项增强：动作分解（Theorem 1 证明功率子问题凸性）、状态 Transformer 编码器(STE)、扩散模型潜在提示生成(DLPG)。
- **方法概述**：MDP 建模含三级 AoI 信息状态。DRL 只输出卫星选择（离散），功率由凸求解器独立完成。STE 替代 MLP 编码时空特征；DLPG 在训练时通过 4 步去噪生成增强表征。训练 5000 episodes。
- **实验设置**：10 颗 LEO（500-1800km），1 HAP（20km），10 地面用户。STE 2 层 Transformer + 4 头注意力。Dueling Q 3 层 MLP (256-256-128)。lr 3e-4，buffer 1e5。
- **使用的 Baseline 方法**：
  - Random: 随机选星（自实现）
  - EWG: 加权贪心启发式（自实现）
  - RR: 轮询（自实现）
  - PPO/SAC/TQC/DQN/DDQN/Standard D3QN: 多种 DRL 算法（引用）
- **关键结论**：DD3QN-AS AoI 降低约 1.7%、切换频率降低 15%（vs 最优 baseline DDQN）。收敛最快且方差最小。去噪步数 M=4 最优。
- **与本研究关系**：直接相关——LEO 切换+DRL，L018 同团队后续工作
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L024] Handover Protocol Learning for LEO Satellite Networks: Access Delay and Collision Minimization
- **DOI/来源**：10.1109/TWC.2023.3342975 (arXiv: 2310.20215)
- **年份/会议**：2023 / IEEE Transactions on Wireless Communications
- **发表状态**：正式发表
- **发表渠道**：IEEE TWC (SCI Q1, IF ~10)
- **核心贡献**：提出 DRL 驱动切换协议 DHO，针对再生型 LEO 卫星网络设计。核心创新：跳过传统 HO 中的 Measurement Report (MR) 步骤，由 serving-SAT 的 DRL agent 利用局部可观测信息直接预测 UE 信道状况并发起 HO Request。采用 IMPALA 分布式训练框架处理高维状态/动作空间。
- **方法概述**：MDP 建模，serving-SAT 为 agent，状态=时间索引+已接入 UE 指示+上一步动作，动作=K 轨道面选择（one-hot），奖励惩罚接入时延和碰撞率（系数 ν 平衡）。IMPALA + V-trace 处理离策略学习。
- **实验设置**：1000×1000 m² 区域，10-200 UE，1 serving-SAT + 2 target-SAT（550km），3GPP NR 参数。IMPALA lr 1e-4~5e-4，1000-8000 episodes。
- **使用的 Baseline 方法**：
  - Conventional HO: 3GPP 5G-NR A3 事件标准协议（自实现）
  - Random: 随机选择（自实现）
  - DHO-Centralized: 集中式消融上界（自实现）
  - DQN/PPO/A3C: DRL 算法对比（自实现，Appendix B）
- **关键结论**：RB 充足时接入时延比传统 HO 低 6.8x；自适应网络条件（资源充足时 93.7% 发送请求，不足时 91.8% 等待）；IMPALA 在高维动作空间中收敛稳定性显著优于 DQN。
- **与本研究关系**：直接相关——LEO 切换协议+DRL
- **开源代码**：无（仅伪代码）
- **验证状态**：已通过学术搜索工具验证

### [L022] Collaborative Deep Reinforcement Learning for Resource Optimization in Non-Terrestrial Networks
- **DOI/来源**：10.1109/PIMRC57407.2023.10294047 (arXiv: 2402.04056)
- **年份/会议**：2023 / IEEE PIMRC 2023
- **发表状态**：正式发表
- **发表渠道**：IEEE PIMRC (旗舰会议)
- **核心贡献**：提出双时间尺度协作 DRL 方案用于地球固定小区 LEO 波束管理和资源分配。将高维联合优化分解为卫星（大时间尺度 T 时隙）和 UE（小时间尺度每时隙）两级 MDP。UE 端承担主要训练负担（TRPO），卫星端仅有限步 rollout。证明协作框架保证单调策略改进。
- **方法概述**：Multi-time-scale MDP (MMDP)，卫星每 T 时隙决策波束方向+RB 候选集，UE 每时隙调整接收波束+RB。两阶段顺序更新：UE 基于 agent 优势之和用 TRPO 更新，生成轨迹→卫星有限步 rollout 近似价值函数并更新。
- **实验设置**：60 RB（3 组），卫星 30 dBW/30 dBi，4GHz S-band，仰角 π/6，每 RB 180kHz。UE 策略网络 300×200×200，价值网络 400×300×200。
- **使用的 Baseline 方法**：
  - Independent DRL: 无协作（自实现）
  - Single-estimation: 单优势估计变体（自实现）
  - BFS-Greedy/MAB: 暴力搜索波束+贪心/MAB（自实现）
  - PBU-Greedy/MAB: 周期波束更新+贪心/MAB（引用+自实现）
- **关键结论**：顺序策略更新显著优于独立训练；协作方案在所有权重组合下加权最优；卫星端仅需有限步 rollout，计算负担远低于暴力搜索。
- **与本研究关系**：方法可借鉴——双时间尺度 MDP 建模和协作 DRL 框架
- **开源代码**：无（仅伪代码）
- **验证状态**：已通过学术搜索工具验证

## Baseline 交叉验证

### Baseline 出现频率统计
| 方法名 | 被几篇论文使用 | 使用该 baseline 的论文 | 代码状态 | 算法描述质量 | 推荐优先级 |
|--------|--------------|----------------------|---------|------------|-----------|
| D3QN/Dueling DQN | 3 篇 | L029, L018, L016 | 无 | 详细（网络结构+超参） | 1 |
| PPO | 4 篇 | L004(核心), L016, L018, L024(对比) | 无 | 详细 | 2 |
| DQN | 3 篇 | L016, L024, L029(DDQN基础) | 无 | 详细 | 3 |
| DDQN | 2 篇 | L016, L029 | 无 | 中等 | 4 |
| SAC | 2 篇 | L016, L018 | 无 | 中等 | 5 |
| 传统规则(A3/MVT/Greedy) | 4 篇 | L029, L024, L018, L022 | 无但算法简单 | 详细（公式明确） | 必选 |
| Random | 3 篇 | L016, L024, L022 | 自实现简单 | 简单 | 下界 |

### Baseline 候选
| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: 传统 A3/MVT 切换规则 | L024, L029 | 无但算法明确（3GPP 规范） | 1 | 被 L024 和 L029 使用，代表传统方法基线，算法来自 3GPP 标准可复现 |
| B2: D3QN/Dueling DDQN | L029, L018, L016 | 无 | 2 | 被 3 篇论文使用，是领域共识 DRL baseline，网络结构描述充分 |
| B3: PPO | L004, L016, L018, L024 | 无 | 3 | 被 4 篇论文使用（含 1 篇核心），是最广泛使用的 on-policy DRL baseline |
