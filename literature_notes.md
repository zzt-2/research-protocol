# 文献调研记录

## 调研概况
- **研究方向**：LEO 卫星网络切换优化 + 深度强化学习
- **检索工具**：tools/search（S2 + OpenAlex + arXiv + SerpAPI）
- **检索关键词**：
  - 角度1: LEO satellite handover decision timing trigger optimization
  - 角度2: LEO satellite selection assignment strategy handover
  - 角度3: LEO NTN mobility management handover 3GPP
  - 角度4: LEO satellite handover heuristic fuzzy logic traditional optimization
- **核心文献数**：9 篇（精读，有 content.md）
- **调研日期**：2026-05-08

## 综合分析

### 现有方法分类

**路线 A：标准 DRL 应用于切换优化**（L02, L03）
将切换决策建模为 MDP，选择合适 DRL 架构直接输出切换动作。L02 采用 Dueling DDQN + 自适应多目标奖励（alpha/beta/gamma 动态权重），在 Telesat 298 星上吞吐量比 MVT 提升 238%；L03 采用 IMPALA 分布式训练跳过 MR 步骤的 DHO 协议，接入延迟比传统 HO 低 6.8x。

**路线 B：DRL + 奖励/元级优化**（L01）
不改变 DRL agent 架构（PPO），研究奖励函数权重的自适应设计。揭示"切换-稳定性困境"：近恒定权重 (GEN MLP, 342.1 Mbps) 大幅优于动态权重 (Oracle MLP, 103.3±96.8 Mbps)，权重平稳性比质量更关键。

**路线 C：进化/增强式 DRL**（L04, L05）
L05 采用进化多目标框架 + 多任务并行 DRL（EMODRL-ED3QN），通过等距离散权重替代连续功率变量，使动作空间与终端数无关，产出 Pareto 策略集。L04 在 D3QN 基础上引入 Transformer 状态编码器和扩散模型增强表征，降低 AoI 约 1.7%、切换频率降低 15%。

**路线 D：多 agent 协作 DRL**（L06, L05）
L06 提出双时间尺度协作框架（卫星大尺度 TRPO rollout + UE 小尺度策略更新），利用 UE 算力辅助训练，证明单调策略改进。L05 的分布式多任务框架也可视为多 agent 协作。

**路线 E：传统优化/启发式**（L07, L08）
L07（PreHO）将切换规划建模为 MILP + 动态规划，利用 UE 静止特性做预测性规划，平均切换延迟 22.5ms（传统 HO 约 260ms）。L08（HHS）提出多属性效用函数（SINR+仰角+负载归一化到 [0,1]）+ logistic 稳定性奖励，纯启发式算法，切换次数比 Highest SINR 减少 64%。

### 已知局限

1. **仿真规模有限**：所有论文仿真规模（3-298 星、10-200 UE）与实际 mega-constellation 差距大
2. **无真实部署验证**：全部基于仿真，无硬件在环或真实卫星平台验证
3. **信道/环境简化**：多数假设 CSI 可获取、轨道模式已知固定、未考虑多小区干扰和 ISL
4. **奖励设计缺乏理论**：L01 揭示自适应奖励稳定性问题；L02 自适应权重 alpha/beta/gamma 未给具体数值；多数论文奖励归一化细节缺失
5. **DRL 方法的可解释性差**：相比 L07（PreHO）的可解析优化和 L08（HHS）的透明效用函数

### 2-3 年趋势

1. **从固定奖励到自适应奖励**：L01（2026）系统探索奖励设计瓶颈，L02（2026）使用自适应多目标权重
2. **从单 agent 到多 agent 协作**：L06 双时间尺度协作、L05 多任务并行框架
3. **从纯 DRL 到混合架构**：L04 引入 Transformer+扩散模型增强、L05 进化框架
4. **传统方法仍有竞争力**：L07 预测性规划实现 11.6x 延迟降低、L08 效用函数在切换稳定性上优于简单 DRL

## 文献条目

### [L01] When Adaptive Rewards Hurt: Causal Probing and the Switching-Stability Dilemma
- **DOI/来源**：arXiv:2604.03562v1
- **年份/会议**：2026 / arXiv preprint
- **核心贡献**：揭示 LEO 卫星调度中的"切换-稳定性困境"：PPO 需准稳态奖励信号收敛，任何自适应权重调整都会重启收敛过程。近恒定权重 (GEN MLP, 342.1 Mbps) 大幅优于动态权重 (Oracle MLP, 103.3±96.8 Mbps)。提出单变量因果探测方法（±20% 扰动，50k 步）。
- **方法概述**：双时间尺度架构——PPO agent 实时调度波束功率/带宽，MDP Architect 监控 KPI 用 CUSUM 检测场景变化并生成奖励权重。对比四种 Architect（Fixed/Rule/MLP/FT-LLM Qwen3-4B+LoRA）。
- **实验设置**：19 波束 Ka 频段卫星（600 km），含雨衰信道；4 种已知 + 3 种未知业务场景；PPO 3 层 MLP (256-256-128)，500k 步；3 随机种子。
- **使用的 Baseline 方法**：
  - M1 Fixed: 静态离线优化权重（自实现）
  - M2 Rule-Based: KPI 阈值分类器（自实现）
  - M3 Learned MLP: 5-64-64-5 网络（自实现）
  - M4 FT-LLM: Qwen3-4B+LoRA rank=16 alpha=32（自实现）
- **关键结论**：MLP architect 最优（已知 357.9 Mbps，未知 325.2 Mbps）；LLM 因数值振荡在未知场景崩溃至 45.3±43.0 Mbps。
- **与本研究关系**：直接相关——奖励设计方法论的核心参考
- **实现关键细节**：奖励 R_w = w_r * R_bar - w_o * O - w_s * S - w_q * Q + w_f * F，R_bar 为归一化总速率（具体归一化公式论文未明确给出）。MLP 权重范围 w_o∈[0.94,1.57]（CV=0.19），LLM 权重在 0.005~0.50 振荡（CV=0.87）。观测：各波束需求估计/信道/队列长度。动作：带宽分配 a∈[0,1]^{N_b}，sum≤1。PPO lr=3e-4, MLP Architect 5-64-64-5 Softplus 输出。CUSUM W=10, h=1.0 std, 权重裁剪[0.01,2.0], cooldown 50 步。
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L02] Dueling DDQN-Based Adaptive Multi-Objective Handover Optimization for LEO Satellite
- **DOI/来源**：arXiv:2605.02416v1
- **年份/会议**：2026 / arXiv preprint
- **核心贡献**：将 LEO 切换建模为多目标优化（吞吐量/阻塞概率/切换成本），Dueling DDQN 自适应多目标方案。Dueling 架构分解 Q=V+A-mean(A) 适合重叠覆盖区多候选卫星效用相近时的稳定价值估计。MSHBO 专家轨迹初始化缓解冷启动。
- **方法概述**：Telesat Lightspeed 298 星，MDP：状态=候选速率/负载/上一关联；动作=选卫星；奖励=alpha*r_th - beta*r_blk - gamma*r_sw。DDQN 解耦选择与评估。
- **实验设置**：Telesat 298 星，STK，仰角 20°，UE 10-30，卫星容量 1-9。300 episodes，buffer 200k，batch 256，lr 1e-3，10 次独立运行。
- **使用的 Baseline 方法**：
  - MVT (Maximum Visible Time): 引用 Papapetrou 2004
  - MAC (Maximum Available Channels): 引用
  - GBW (Graph-Based Weighting): 引用 Hozayen 2022
  - MSH/MSHBO: 引用 Kang ICC 2024
  - DDQN: 自实现
- **关键结论**：吞吐量比 MVT 提升 238%，比 MAC 提升 100%；典型条件下近零阻塞。
- **与本研究关系**：直接相关——Dueling DDQN 切换方案，潜在 baseline 候选
- **实现关键细节**：奖励 r_u(t) = alpha(t)*r_th(t) - beta(t)*r_blk(t) - gamma(t)*r_sw(t)。**r_th(t) = Shannon 容量 Mbps，未做归一化**（这是上次试跑 F5 奖励失衡的根因——rate~10^6 vs 阻塞惩罚~1）。r_blk 为二元指示器，r_sw 为二元指示器。alpha/beta/gamma 为自适应权重但**论文未给出具体数值或自适应规则**。观测：R_u(t) 候选速率集合、S_u(t) 候选集、L(t) 负载向量、s_u(t-1) 前一步服务卫星。动作：从候选集选一颗。lr=1e-3, gamma=0.99, batch=256, buffer=200k, episodes=300, target_update=1000, eps_start=0.2→0.01 指数衰减。
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L03] Handover Protocol Learning for LEO Satellite Networks (DHO)
- **DOI/来源**：arXiv:2310.20215
- **年份/会议**：2023 / arXiv preprint（IEEE 期刊）
- **核心贡献**：提出 DRL 驱动切换协议 DHO，跳过传统 HO 中 Measurement Report 步骤，由 serving-SAT DRL agent 利用预训练轨道模式预测 UE 信道状况。IMPALA 分布式训练处理 J×K multi-discrete 动作空间。
- **方法概述**：serving-SAT 为 agent，状态=时间索引+已接入 UE 指示+上一步动作，动作=K 轨道面选择（0=等待），奖励=-(接入延迟+nu*碰撞率)。
- **实验设置**：3 轨道面（550km），1000×1000m²，UE 10-200，S-band/Ka-band。IMPALA lr 1e-4~5e-4，episodes 1000-8000。
- **使用的 Baseline 方法**：
  - Conventional HO: 3GPP 5G-NR A3 事件标准协议（按 3GPP 标准实现，含 L3 IIR 滤波 RSRP，beta_L3=0.5, A3 offset=1dB）
  - Random: 随机选择（自实现）
- **关键结论**：RB 充足时接入延迟比传统 HO 低 6.8x；自适应网络条件（充足时 93.7% 发送请求，不足时 91.8% 等待）。
- **与本研究关系**：直接相关——3GPP A3 传统 baseline 的实现参考
- **实现关键细节**：奖励 r[n] = -(D_bar + nu*C_bar[n])，D_bar 为平均接入延迟（tau 的倍数），C_bar 为碰撞率，nu 为权衡系数（nu=5 延迟优先，nu=1/20 碰撞规避）。**无显式归一化**。观测 s[n] = {n, a_HO[n], a[n-1]}，时间索引作为 fingerprint 稳定经验回放。动作：每个 UE 选 a_j∈{0,...,K-1} one-hot。IMPALA + V-Trace，gamma=0.85~0.99, batch=10000, steps_per_ep=20。
- **开源代码**：无（仅伪代码）
- **验证状态**：已通过学术搜索工具验证

### [L04] Joint AoI and Handover Optimization in Space-Air-Ground Integrated Networks
- **DOI/来源**：arXiv:2509.12716v1
- **年份/会议**：2025 / arXiv preprint
- **核心贡献**：AoI 感知 SAGIN 下行架构（LEO-HAP-地面），DD3QN-AS 算法引入动作分解（证明功率子问题凸性）、Transformer 状态编码器(STE)、扩散模型潜在提示生成(DLPG)。DRL 只输出卫星选择，功率由凸求解器独立完成。
- **方法概述**：MDP 含三级 AoI 信息状态。STE 替代 MLP 编码时空特征；DLPG 4 步去噪生成增强表征。
- **实验设置**：10 LEO（500-1800km），1 HAP（20km），10 用户。STE 2 层 Transformer + 4 头注意力。Dueling Q 3 层 MLP (256-256-128)。lr 3e-4，buffer 1e5。
- **使用的 Baseline 方法**：
  - Random: 等概率随机（自实现）
  - EWG: 加权贪心（自实现）
  - RR: 轮询（自实现）
  - PPO/SAC/TQC/DQN/DDQN/Standard D3QN: 多种 DRL 算法（引用）
- **关键结论**：DD3QN-AS AoI 降低约 1.7%、切换频率降低 15%（vs 最优 baseline DDQN）。去噪步数 M=4 最优。
- **与本研究关系**：直接相关——LEO 切换+DRL
- **实现关键细节**：奖励 r_t = -rho_1*sum(Delta_i) - rho_2*N_t + rho_3*sum(R_j)，**rho_1/rho_2/rho_3 为归一化参数调至同量级**（论文未给出具体数值）。Delta_i 为 AoI，N_t 为切换次数，R_j 为可达速率。观测 s_t = {c_t^S, c_t^U, theta[t], delta[t], Delta[t]}，含卫星/用户位置、AoI 信息。STE: 2 层 Transformer 4 heads 64-dim。DLPG: 正弦时间嵌入+32-dim prompt, 4 步去噪。Dueling Q: 3 层 MLP (256,256,128), ReLU。lr=3e-4, batch=128, buffer=1e5, gamma=0.99, tau=0.005, eps-greedy。
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L05] Collaborative Ground-Space Communications via Evolutionary Multi-Objective Deep Reinforcement Learning
- **DOI/来源**：10.1109/JSAC.2024.3459029
- **年份/会议**：2024 / IEEE JSAC Vol.42 No.12 pp.3395-3411
- **核心贡献**：DCB+LEO 卫星选择+功率分配+切换频率控制的三目标 MOMDP。等距离散权重替代连续功率变量使动作空间与终端数无关。EMODRL-ED3QN 进化多任务框架产出 Pareto 策略集。
- **方法概述**：Lemma 1 证明单时隙加权和优化凸性，DRL 只输出权重索引和卫星选择。Enhanced D3QN + 合法动作掩码 + 进化多目标框架。
- **实验设置**：110 LEO（80×500km + 30×1000km），10 终端，2.4GHz，60 分钟。N=10 任务，300 进化代，warm-up 80 次。Q 网络 2×2048。
- **使用的 Baseline 方法**：
  - Non-DCB: 单终端直连（自实现）
  - ARGP: 速率贪心上界（自实现）
  - EMODRL-D3QN/DDQN/PPO/TD3/SAC/Noisy-DQN: 同框架不同 DRL 变体
- **关键结论**：EMODRL-ED3QN 上行速率 1.87×10^7 bps 接近 ARGP 上界，同时能耗和切换次数远低于 ARGP。
- **与本研究关系**：直接相关——多目标切换+DRL
- **实现关键细节**：向量奖励 r(t) = [rho_1*R_hat, -rho_2*sum(P_i*DeltaT), -rho_3*kappa_t]。**R_hat = R(t) if R(t)>=R_bar else 0**（低于阈值置零，非 [0,1] 归一化）。rho_1/rho_2/rho_3 归一化参数调至同量级（具体值未给）。观测仅 2 维：{t, s_{t-1}}（时间索引+前卫星），与终端数无关。动作：{k_t, s_t}，k_t 为离散权重选择，s_t 为卫星选择，不可用卫星被 mask。Q 网络 2×2048 tanh。lr=1e-4, batch=256, buffer=1e5, gamma=0.96, N_tasks=10, T_evo=300, T_warm=80。合法动作掩码 + 种群多样性 buffer + Pareto 策略存档。
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L06] Collaborative Deep Reinforcement Learning for Resource Optimization in NTN
- **DOI/来源**：arXiv:2402.04056v2
- **年份/会议**：2024 / arXiv preprint
- **核心贡献**：双时间尺度协作 DRL：卫星（大尺度 T 时隙 TRPO rollout）和 UE（小尺度每时隙策略更新）。UE 端基于两个 agent 策略优势之和用 TRPO 更新，卫星端仅有限步 rollout。证明协作框架保证单调策略改进。
- **方法概述**：Multi-time-scale MDP，卫星每 T 时隙决策波束方向+RB 候选集，UE 每时隙调整接收波束+RB。两阶段顺序更新。
- **实验设置**：60 RB（3 组），卫星 30 dBW/30 dBi，4GHz S-band，仰角 π/6，RB 180kHz。UE 策略 300×200×200，价值 400×300×200。
- **使用的 Baseline 方法**：
  - Independent DRL: 无协作（自实现）
  - Single-estimation: 单优势估计变体（自实现）
  - BFS-Greedy/MAB: 暴力搜索波束+贪心/MAB（引用+自实现）
  - PBU-Greedy/MAB: 周期波束更新+贪心/MAB（引用+自实现）
- **关键结论**：顺序策略更新显著优于独立训练；卫星端仅需有限步 rollout，计算负担远低于暴力搜索。
- **与本研究关系**：方法可借鉴——双时间尺度 MDP 建模和协作 DRL 框架（聚焦波束管理+RB 分配，非切换决策）
- **实现关键细节**：UE 奖励 R_L^i = (sum(b*c))/(sum(b)) + eta*Omega_i，除以 sum(b) 得到每 RB 平均速率（隐式归一化），Omega_i = min[sum(b*c)-D, 0] 为需求缺口惩罚。LEO 奖励 R_H^k = 仅满足约束时隙的平均可达速率。**无显式全局归一化**。LEO 观测：位置+上一周期各时隙 RB 平均 SNR（T+3 维）。UE 观测：各 RB SNR+天线信号强度（M+N_r 维）。UE 策略 300×200×200 MLP, 价值 400×300×200。TRPO + rollout, gamma=0.99, LEO replay=1200, UE replay=9600。FIFO reward buffer 平滑。
- **开源代码**：无（仅伪代码）
- **验证状态**：已通过学术搜索工具验证

### [L07] PreHO: Predictive Handover for LEO Satellite Networks
- **DOI/来源**：arXiv:2603.07987v1
- **年份/会议**：2026 / arXiv preprint (Fudan University)
- **核心贡献**：提出预测性切换机制，利用 UE 静止+信道可预测特性，将反应式切换转为主动预规划，消除 MR 和 RACH 过程。引入 HPF 网络功能做全局协调优化。建模为 MILP（NP-hard），提出交替优化+动态规划近似算法。
- **方法概述**：将时间划分为规划区间（10min，T=200 时隙，每时隙 3s），HPF 收集 UE 位置+星历，通过交替优化+DP 确定切换决策（目标 S-gNB + 精确时间），一次性分发执行。
- **实验设置**：Starlink 1584 卫星 550km，100 UE [35-38N, 122-125E]，最小仰角 40°，可见 S-gNB M=39。alpha-fairness (alpha=1 对数效用)，gamma=2e-3。原型 UERANSIM+Open5GS。
- **使用的 Baseline 方法**：
  - BHO: 5G 标准切换（自实现）
  - BHO-GS: 地面站辅助切换（引用 Han 2016）
  - BHO-A: 加速切换（引用 Wu 2024 INFOCOM）
  - LSS: SINR 高 50% 触发（自实现）
  - LST: 最长服务时间（自实现）
  - Greedy: 逐时隙贪心（自实现）
- **关键结论**：平均切换延迟 22.5ms，比 BHO（~260ms）快 11.6x。规划算法目标值比 LSS 至少提升 57x。150 UE 运行时间 <40s（Python）。
- **与本研究关系**：对比 baseline 候选——传统优化方法的代表，可借鉴预测性规划思想
- **实现关键细节**：目标 min N_HO - gamma*U_UE，gamma=2e-3。效用 alpha-fairness alpha=1（对数效用 u=log(D)）。资源分配 y∈[0,1] 通过 KKT 解析或二分搜索。用户关联 x∈{0,1} 每时隙每 UE 恰好一个 S-gNB。交替优化+DP，复杂度 O(T^3*M) 或 O(T*M*N)。**无 DRL 训练**：传统优化方法。约束：仰角≥40°, 带宽≤20MHz。
- **开源代码**：无（UERANSIM+Open5GS 原型）
- **验证状态**：已通过学术搜索工具验证

### [L08] A Low-Complexity Hybrid Handover Strategy for LEO NTN: Balancing Stability and Link Quality
- **DOI/来源**：10.3390/s26051449
- **年份/会议**：2026 / Sensors (MDPI)
- **核心贡献**：提出 HHS 低复杂度多属性效用函数切换算法，集成 SINR、仰角、负载三个指标归一化到 [0,1] 加权求和，引入 logistic-decay 稳定性奖励抑制乒乓效应。提供乒乓概率上界的数学分析（Chebyshev/Cantelli 不等式）。真实 Starlink TLE 数据驱动仿真。
- **方法概述**：纯启发式算法。每轮计算可见卫星多属性效用：SINR/仰角/负载各自 min-max 归一化到 [0,1]，加权求和得 base utility，当前服务卫星加 logistic 稳定性奖励、非服务卫星加固定惩罚。三级级联决策：强制切换/机会升级/退化响应。
- **实验设置**：Starlink 真实 TLE（SGP4），Riyadh 静止终端，Ku 10.75GHz 250MHz。50 runs×2h，决策间隔 10s。信道含 FSPL+ITU-R P.676+P.838 雨衰+3GPP TR 38.811 阴影+P.618 闪烁+干扰。
- **使用的 Baseline 方法**：
  - LVT (Longest Visibility Time): TTT=240ms, 迟滞 3.0 dB（自实现）
  - HEA (Highest Elevation Angle): 迟滞 4.0°（自实现）
  - Highest SINR: 迟滞 2.0 dB（自实现）
- **关键结论**：平均 140.9 次切换，比 Highest SINR (390.9) 减少 64%。SINR 8.8 dB。服务可用性 90.2%。复杂度 O(N_v)。
- **与本研究关系**：**对比 baseline 候选**——传统启发式方法 SOTA，多属性效用函数+稳定性奖励设计可借鉴
- **实现关键细节**：归一化 q_i = clip((gamma_i-gamma_min)/(gamma_max-gamma_min), 0, 1)，e_i = clip((theta_i-theta_min)/(theta_max-theta_min), 0, 1)，l_i = 1-rho_i。**三项全部归一化到 [0,1]，量级一致**。Base utility U_base = 0.5*q + 0.15*e + 0.25*l。稳定性奖励 psi = 1/(1+exp(-0.2*(t_conn-15)))，w_stab=0.1。切换惩罚 P_ho=0.03。最终 U = U_base + I[cur]*w_stab*psi - I[!cur]*P_ho。机会升级阈值 delta_U_th=0.02，退化阈值 gamma_th=8.0dB，决策间隔 10s。**纯启发式，无 DRL 训练超参**。
- **开源代码**：无（Algorithm 1 伪代码完整）
- **验证状态**：已通过学术搜索工具验证

### [L09] Mobility and Handover Management in 5G/6G Networks: Challenges, Innovations, and Future Directions
- **DOI/来源**：10.3390/technologies13080352
- **年份/会议**：2025 / Technologies (MDPI) — Review
- **核心贡献**：5G/6G 切换和移动性管理结构化综述，覆盖迟滞/TTT/CIO 优化、模糊逻辑、元启发式、ML/DRL、SDN/NFV 等方向。提供切换参数分类框架（HODP/HCP/KPI）。对 4 种算法在 6 种移动速度下仿真对比。
- **方法概述**：综述论文。分类梳理传统方法、AI/ML 方法、SDN 方法的切换优化方案。NTN/LEO 部分较浅（仅 Section 7.7 一段）。
- **实验设置**：MATLAB 2020a，15 UE，50ms 周期，6 种速度场景。对比 Dis/FLC/HPI/WPHPO。
- **使用的 Baseline 方法**：
  - Dis: 距离感知 HPSO（引用）
  - FLC: 模糊逻辑控制器（引用）
  - HPI: 切换性能指标（引用）
  - WPHPO: 加权性能优化（论文改进）
- **关键结论**：AI/ML 方法在 HO 率/延迟/资源效率上优于传统方法。高速场景 HO 概率和 RLF 显著增加。
- **与本研究关系**：仅供参考——切换方法分类和 KPI 框架参考；NTN 部分内容浅
- **实现关键细节**：综述论文无具体算法实现细节。引用 DRL 方法：PPO 用于网络切片减少 HO，DQN 用于 LEO 切换。无奖励函数/观测/动作/训练超参具体数值。
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

## Baseline 交叉验证

### Baseline 出现频率统计

| 方法名 | 作为对比方法 | 作为核心方法 | 使用论文 | 代码状态 | 算法描述质量 | 推荐优先级 |
|--------|-------------|-------------|---------|---------|------------|-----------|
| MVT (Maximum Visible Time) | 1 篇 | 0 | L02 | 无但算法简单 | 引用 Papapetrou 2004，描述清晰 | 2 |
| A3 事件 (3GPP 标准) | 1 篇 | 0 | L03 | 无但按 3GPP 标准实现 | 详细（L3 IIR, beta_L3=0.5, offset=1dB） | 1 |
| Highest SINR / LSS | 2 篇 | 0 | L07, L08 | 无但算法简单 | 详细（含迟滞值） | 3 |
| LVT (Longest Visibility Time) | 1 篇 | 0 | L08 | 无但算法简单 | 详细（TTT=240ms, 迟滞 3.0dB） | 4 |
| Random | 2 篇 | 0 | L03, L04 | 自实现简单 | 简单 | 下界 |
| HHS (多属性效用函数) | 0 | 1 篇 | L08 | 伪代码完整 | 非常详细（归一化公式+权重） | 5 |
| D3QN/Dueling DQN | 3 篇 | 3 篇 | L02,L04,L05 | 无 | 详细（网络结构+超参） | DRL baseline |
| PPO | 2 篇 | 1 篇 | L01(核心),L04,L03(对比) | 无 | 详细 | DRL baseline |

### Baseline 候选

| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: HHS (多属性效用函数) | L08 | 伪代码完整（Algorithm 1），归一化公式明确 | 1 | 传统启发式 SOTA，归一化到 [0,1] 量级一致，真实 Starlink TLE 验证，与 DRL 形成传统 vs AI 的核心对比 |
| B2: A3 事件 (3GPP 标准) | L03 | 按 3GPP TS 38.331 标准 | 2 | 领域标准方法，L03 给出详细参数（IIR beta=0.5, offset=1dB），被引用作为传统 baseline |
| B3: MVT (最长可见时间) | L02 | 算法简单（选可见时间最长卫星） | 3 | 被 L02 使用，引用 Papapetrou 2004，但需轨道几何计算 |

### 下载失败的重要传统方法论文

以下论文未能自动下载，如用户能获取将显著改善传统方法路线覆盖：

| 优先级 | 标题 | DOI | 路线 |
|--------|------|-----|------|
| P1 | Handover Using Bipartite Graph and Hysteresis | 10.1109/OJCOMS.2025.3541962 (OA) | 图论+迟滞 |
| P1 | GNN Handover Strategy | 10.1016/j.icte.2025.01.009 (OA) | 图神经网络 |
| P1 | TOPSIS Multi-Criteria Handover | 10.3390/network5020015 (OA) | 多属性决策 |
| P1 | Markov Chain-Guided Simulated Annealing | 10.3390/network5040049 (OA) | 优化方法 |

---

## 用户手动补充论文（7 篇，2026-05-08 追加）

### [L10] Learning When and Where to Handover: A Hierarchical RL Framework
- **DOI/来源**：10.1109/TWC.2026.3667917
- **年份/会议**：2026 / IEEE TWC
- **核心贡献**：HRL 解耦"何时切换"(PPO+GRU 时间层)和"切换至哪颗"(DQN 空间层)。QoS评分 Theta=0.4*负载+0.3*SINR+0.3*服务时长，各项归一化。
- **方法概述**：时间层 GRU 提取 SINR/负载/服务时长时序特征输出二元切换触发；空间层 DQN 从可见卫星选目标。
- **实验设置**：Starlink 1584星 550km，100UE，可见3-6星，泊松业务λ=0.1/s。
- **使用的 Baseline 方法**：MO-RL(非分层)/SL-RL(仅负载)/SQ-RL(仅信号)/ST-RL(仅服务时长)：自实现
- **关键结论**：切换成功率~0.95-0.99，平衡权重(0.4,0.3,0.3)最优。
- **与本研究关系**：直接相关——HRL 解耦切换时机+目标选择
- **实现关键细节**：奖励4种Case（不切换/kappa*delta_QoS/mu*delta_QoS-Omega/-penalty）。QoS各项归一化：负载=D_s/C_s∈[0,1]。时间层 PPO+3层GRU(256,256,128)+2层FC(128,64)，lr=3e-4,clip=0.2,gamma=0.99。空间层DQN 4层FC(256,128,128,64)，lr=1e-3,eps 1.0→0.01线性衰减0.995。
- **开源代码**：无

### [L11] Handover Strategy Using Bipartite Graph and Hysteresis Margin
- **DOI/来源**：10.1109/OJCOMS.2025.3541962
- **年份/会议**：2025 / IEEE OJ-COMS
- **核心贡献**：加权二分图+Kuhn-Munkres最大权重匹配实现负载均衡。迟滞余量(HM)机制：当前增益≥初始值-HM时权重乘σ=10dB优先保持连接。
- **方法概述**：每时隙构建卫星-网关站二分图，权重=信道增益，HM条件满足时乘大常数σ，KM算法求最优匹配。
- **实验设置**：Starlink 1584星 550km，3网关站(Montreal)，仰角15°，45分钟，12GHz。
- **使用的 Baseline 方法**：MWM(Feng 2020)/Shortest Path(Wu 2016)/MST：引用
- **关键结论**：3dB HM 最优——切换次数比0dB减少45-50%，数据率接近MWM。
- **与本研究关系**：方法可借鉴——经典优化方法+HM 减少乒乓
- **实现关键细节**：权重λ=G*FH，HM满足时FH=σ(10dB)否则=1。HM条件：G>=G'_init-H。信道含FSPL+大气+Rician(K=20dB或随机-10~25dB)。KM复杂度O((N'*M)^3)。3dB HM最优平衡。
- **开源代码**：无

### [L12] Proactive HO via Multi-Agent DRL (QMIX-PHO, ETRI)
- **DOI/来源**：10.4218/etrij.2025-0240
- **年份/会议**：2026 / ETRI Journal
- **核心贡献**：CNN-LSTM预测RSRP轨迹(T_p=2步) + QMIX多agent CTDE切换决策。每个MT独立agent，单调性约束mixing网络协调。
- **方法概述**：先CNN-LSTM预测未来RSRP，再QMIX框架基于预测RSRP+本地观测做切换决策。训练中心化，推理去中心化。
- **实验设置**：Walker-delta 10500星(50面×210) 600km + 19站地面网，10-20MT，20GHz/2GHz。
- **使用的 Baseline 方法**：MHO(3GPP TR38.821)/PSAHO(Lu 2022)/IQL-PHO(Tampuu 2017)：引用
- **关键结论**：QMIX-PHO所有速度下最高吞吐量最低HO频率，T_p=2最优。
- **与本研究关系**：直接相关——多agent DRL CTDE范式+RSRP预测
- **实现关键细节**：奖励r=D_rate+omega2*T_conn(D>=D_min)或(D-D_min)(D<D_min)。omega1/omega2未给具体值。观测含数据率+连接时长+候选RSRP序列(T_p=2)+用户数+HO数。动作|A|=N*T_p+1=5。CNN-LSTM:lr=0.001,batch=64。QMIX:5000ep,lr=0.0005,gamma=0.95,eps 1→0.0001,buffer=500ep,batch=32,RMSProp。
- **开源代码**：无

### [L13] Evaluation of TOPSIS Algorithm for Multi-Criteria Handover
- **DOI/来源**：10.3390/network5020015
- **年份/会议**：2025 / Network (MDPI)
- **核心贡献**：SD-TOPSIS首次引入LEO切换，四指标(上传/下载速率、延迟、丢包)灵敏度分析。
- **方法概述**：向量归一化+标准差赋权+正负理想解欧氏距离+相对接近度r∈[0,1]。
- **实验设置**：Starlink-on-the-Road真实数据，10星，无仿真器。
- **使用的 Baseline 方法**：Entropy-TOPSIS/Importance-TOPSIS：自实现
- **关键结论**：SD-TOPSIS鲁棒性最优，变化率29.69% vs Entropy 31.85%。
- **与本研究关系**：方法可借鉴——TOPSIS多准则可作为传统baseline
- **实现关键细节**：向量归一化a_norm=a/sqrt(sum(a^2))。SD权重：sigma/sigma_sum。SD权重值：upload 0.2943, download 0.2151, ping 0.2954, loss 0.1950。接近度r=dist^-/(dist^++dist^-)。
- **开源代码**：数据集公开 sys-uos/Starlink-on-the-Road

### [L14] Real-Time HO via Markov Chain-Guided Simulated Annealing (MCSA)
- **DOI/来源**：10.3390/network5040049
- **年份/会议**：2025 / Network (MDPI)
- **核心贡献**：MCSA将用户-卫星分配建模为带SLA约束的二值组合优化，马尔可夫链引导退火状态转移+自适应冷却。复杂度O(k*|U|*|S|)。
- **方法概述**：熵权法对RT/DR/AR三指标加权→min-max归一化→Score驱动Markov转移+Metropolis准则→自适应冷却。
- **实验设置**：Starlink 550km 10星可见 1000UE城市峡谷，Ku 10.7GHz 120MHz，STK 17.1。
- **使用的 Baseline 方法**：ILP(精确)/GA(种群50,交叉0.8,变异0.1)：自实现
- **关键结论**：用户满意度~97%，比GA高10%，运行时可扩展性优于ILP和GA。k=10~20收敛稳定。
- **与本研究关系**：直接相关——非RL启发式优化，强baseline候选
- **实现关键细节**：Score=w_rt*RT_norm+w_dr*DR_norm+w_ar*AR_norm，**三项min-max归一化到[0,1]**。熵权KMeans标准化后计算。退火T_0=随机邻域差异均值(接受概率~0.8)，alpha自适应[min,max]，N=k*|U|*|S|，早停>=0.1*N无改进。约束：仰角≥20°, DR∈[DR_min,DR_max], 每用户一星, 容量限制。信道：FSPL+O2+H2O+3GPP LoS/NLoS(A=2.5,B=20)。
- **开源代码**：无

### [L15] GNN Handover Strategy (ICT Express)
- **DOI/来源**：10.1016/j.icte.2025.01.009
- **年份/会议**：2025 / ICT Express 11 pp.239-244
- **核心贡献**：GNN二部图(卫星+UE) T=2层message passing分布式选星+卫星侧ACK负载控制。基于3GPP Rel-16 CHO协议。
- **方法概述**：UE用GNN softmax选目标卫星(边特征=接收功率)，卫星侧按负载(α+β vs P)接受/拒绝。CHO两阶段(preparation+execution)。
- **实验设置**：Starlink 1584星 550km，50UE，11.9GHz 10MHz/UE，负载P=10，CHO HOM=3dB TTT=0s。
- **使用的 Baseline 方法**：MRSP(最大信号)/MWM(KM匹配)/LAGA(负载感知贪心)：引用+自实现
- **关键结论**：负载均衡违反率0.38%(MRSP 100%)，50UE训练可迁移。
- **与本研究关系**：方法可借鉴——GNN分布式选星+负载控制
- **实现关键细节**：Loss=-1/|B| sum[p*log2(1+SINR)] + omega*sum(ReLU(sum(p)-P))。GNN T=2层，每层sat FCN+UE FCN。softmax选星argmax p。ACK三case：全接受/全拒绝/接受信号最强(P-α)个。Adam lr=1e-5, 70ep, batch=4。仰角≥25°建边。
- **开源代码**：无

### [L16] Orbit Aware-Based Satellite Selection (OB-Aware)
- **DOI/来源**：10.1109/ACCESS.2026.3657599
- **年份/会议**：2026 / IEEE Access
- **核心贡献**：两次RTT测量(间隔1s)估计轨道变化率delta，选max(delta)卫星最大化通信时长。Gen.1(4408星)达理论值98.4%，Gen.2(29988星)达87.5%。
- **方法概述**：基于AODV扩展。RREQ广播测RTT(1-hop)+RREP获RTT(total)→差值得RTT(2-hop)。delta=min(|ΔRTT_1hop|,|ΔRTT_2hop|)，选max delta。
- **实验设置**：ns-3 LEO module，Gen.1 4408星/Gen.2 29988星，仰角40-140°，bent-pipe。
- **使用的 Baseline 方法**：AODV(ns-3默认)/C-GSG(最近GSG)/F-GSG(最远GSG)：引用+自实现
- **关键结论**：Gen.1通信时长达理论值98.4%(AODV 68.5%)，Gen.2达87.5%(AODV 40.74%)。
- **与本研究关系**：方法可借鉴——轻量传统规则，**有开源代码**
- **实现关键细节**：delta(i)=min(|RTT_1hop^(1)-RTT_1hop^(2)|, |RTT_2hop^(1)-RTT_2hop^(2)|)，选argmax。RTT_2hop=RTT_total-RTT_1hop。测量开销1秒。GSG判定：RTT^(2)<RTT^(1)则正在靠近。
- **开源代码**：https://github.com/kei-wagi/OB-Aware-Method

---

## 更新后的 Baseline 交叉验证（16 篇版）

### 新增传统方法

| 方法名 | 作为对比方法 | 核心方法 | 使用论文 | 代码 | 推荐优先级 |
|--------|-------------|---------|---------|------|-----------|
| KM+HM(二分图) | 0 | 1 | L11 | 无 | 6 |
| TOPSIS(SD/Entropy) | 0 | 1 | L13 | 无 | 7 |
| MCSA(Markov SA) | 0 | 1 | L14 | 无 | 5 |
| GNN二部图 | 0 | 1 | L15 | 无 | 8 |
| OB-Aware(RTT变化率) | 0 | 1 | L16 | **GitHub开源** | 4 |
| HRL(PPO+GRU/DQN) | 0 | 1 | L10 | 无 | DRL候选 |

### Baseline 选定（经用户确认）
- **B1: HHS** (L08) — 传统启发式 SOTA，归一化到[0,1]
- **B2: Dueling DDQN** (L02) — DRL baseline
- **B3: Random** — 下界

### 降级说明更新
16篇≥8篇，频率门槛恢复为"≥2篇使用"。但16篇中传统方法无重叠使用（各自只出现1次），DRL中D3QN/Dueling DDQN有3篇交叉验证证据。
