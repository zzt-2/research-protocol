# Literature Notes

## 研究方向

异构图注意力网络增强的卫星-地面协同边缘计算中 DAG 依赖任务卸载

---

## 核心论文（上一对话已精读）

### [K1] Wu et al. 2025 — Dependency-Aware Task Offloading via HGAT and DRL
- DOI: 10.1109/JIOT.2024.3514108
- **发表状态**: 正式发表
- **发表渠道**: IEEE Internet of Things Journal
- **核心贡献**: 提出 HGAT-PPO 框架，在车联网场景中用异构图注意力网络编码器解决 DAG 依赖任务卸载。设计双图编码器：Task Encoder（GAT 处理 DAG 有向图）+ Server Encoder（修改版 GAT 处理服务器竞争无向图，边特征增强注意力），PPO 做策略优化。
- **方法概述**: "HGAT"指两套独立 GAT 编码器，不是 HAN 意义上的多节点类型注意力。Task GAT 用标准多头注意力（已完成子任务动态 mask）；Server GAT 引入多维边特征（竞争强度），注意力接受 3F' 维输入。无显式节点类型嵌入。
- **DAG建模**: DAG_m=(V_m,E_m,R_m)，有向边表数据依赖。递归特征基于后继任务重要性自底向上计算。已完成子任务动态移除。
- **DRL算法**: PPO，Actor-Critic 共享 HGAT Encoder。Actor 逐 pair 输出 logit 支持可变动作空间。Invalid action masking。lr=2e-4, 2层GAT, 4头注意力, Adam, ~1500 gradient steps 收敛。
- **实验设置**: 车联网：5 ICV + 5 边缘服务器 + 1 云服务器，每车 16 子任务。daggen 生成 DAG。i7-12700 + RTX 3060Ti。自由空间路径损耗。
- **Baseline**: ALE, ROE, LPGO, VTSPO, ODCO, HGAT-A2C, HGCN-PPO, HGCN-A2C
- **关键结论**: HGAT-PPO 比 LPGO 成本降低 19.48%，比 HGCN-PPO 提升 3.33%（GAT 注意力优于 GCN 固定聚合）。推理 80 子任务 0.477s。
- **与本研究关系**: 方法可借鉴 — 双图编码器、边特征注意力、动态动作空间设计可迁移到卫星场景
- **实现关键细节**: Reward = C(s_t) - C(s_{t+1})（成本下降值），成本估计用贪心下界。状态分 ST(t)子任务/SC(t)服务器/SP(t)pair 三部分。
- **开源代码**: 无

### [K2/M01] Huang et al. 2026 — Cost-Aware Dependent Task Offloading for Satellite Edge Computing
- DOI: 10.1109/TMC.2025.3645456
- **发表状态**: 正式发表
- **发表渠道**: IEEE Transactions on Mobile Computing, Vol. 25, No. 6
- **核心贡献**: 提出 Graph-aware Asynchronous MAPPO (AMAPPO) + MATS 任务排序 + One-to-Many 匹配，解决卫星边缘计算中 DAG 依赖任务卸载和资源分配。四层架构：IoTD-UAV-LEO-CS。
- **方法概述**: **Plain GraphSAGE**（同构图神经网络，mean-pooling 聚合，无注意力机制）。所有节点（DAG 任务节点、UAV/LEO/CS 服务器节点）共享同一组 GraphSAGE 参数，不区分节点类型。DAG 图分别做上游/下游视图聚合（不同变换参数 W^us/W^ds），G_net 图用标准 mean-pooling。
- **DAG建模**: MATS 算法将多 IoTD 的 DAG 合并为一个大 DAG（虚拟入口/出口节点）。ERR（Expected Relative Residual Workload）递归计算 rank 值决定任务优先级。
- **DRL算法**: AMAPPO（MAPPO 异步版本）。多智能体按"收集点"划分。CTDE：Critic 全局状态，Actor 局部观测。异步 buffer 各 agent 独立存 transition。lr=0.0005, mini-batch=128, GAE, ~300 episode 收敛。
- **实验设置**: 100 IoTD (80遮挡+20开阔), 4 UAV, 8 LEO (500km), 1km×1km 区域, DAG 10-50 任务。Xeon 8370C + GTX 4090。G2U Rician, G2S/U2S Shadowed-Rician, ISL 自由空间。Alibaba cluster-trace-v2018。
- **Baseline**: MAPPO, MADDPG, A-PPO, IPPO, AMAPPO 基础版, AMAPPO+Match, AMAPPO+Match+MATS
- **关键结论**: AMAPPO+Match+MATS 比 MAPPO 能耗降低 ~10.3%，延迟降低 ~10.9%
- **与本研究关系**: **直接竞争** — 最接近竞争者，但用同构 GraphSAGE，HGAT 差异化完全成立
- **实现关键细节**: 部分卸载因子层层递减。决策辅助机制对不可用动作权重置零。
- **开源代码**: 无

### [K3] Cai/Cheng 2025 — GDRL for SAGIN Dynamic Resource Allocation
- DOI: 10.1109/JSAC.2024.3460086
- **发表状态**: 正式发表
- **发表渠道**: IEEE JSAC (SCI Q1)
- **核心贡献**: 提出 GDRL 框架，将 GCN 变体作为特征提取器（GFEN）嵌入 TRPO，设计 Action Mapping Network (AMN) + 编码方案处理离散/连续混合动作空间，集成 MAML 元学习实现环境参数快速适配。
- **方法概述**: **同构 GCN**，基于 Chebyshev 多项式近似的谱图卷积（K=1 简化为 Kipf-Welling 形式）。User/LEO/HAPS 三类节点**统一处理为同构图节点**，不区分类型。节点特征仅 2 维（位置+初始计算资源）。GFEN: 2层GCN + 4层MLP解码器。**无注意力机制，无边特征，无节点类型感知**。
- **DAG建模**: **无 DAG 建模**。任务为独立计算任务 Tu(t)={ou,su,vu,ιu}，无任务间依赖。支持三路径卸载（本地/LEO/HAPS，含两级卸载）。
- **DRL算法**: 修改版 TRPO + MAML 元学习。AMN: 2层LSTM + 4层MLP, lr=0.001。batch=128, horizon=1024, Sigmoid 激活, Adam。
- **实验设置**: SAGIN(LEO+HAPS+地面用户)，双时隙结构，双服务类型。DT任务8000-10000bits，DS任务200-500bits，ou∈[1000,3000]。LEO VM 100-130，HAPS VM 50-80，K=100子信道。B=15kHz, N0=-173dBm/Hz。三种资源场景（充沛/中等/紧缺）。Rician + UPA 阵列响应。
- **Baseline**: Random, TRPO, PPO, SAC, DDPG, GDRL w/o GFEN, GDRL w/o MAML
- **关键结论**: GDRL 在所有场景取得最高 return。On-policy（TRPO/PPO）整体优于 off-policy（SAC/DDPG）。GFEN 消融证实图结构特征显著提升。论文未来工作明确提出"考虑任务间关联性"。
- **与本研究关系**: **方法可借鉴** — AMN 混合动作空间设计、状态分离（静态/动态）模式、奖励函数约束惩罚结构。K3 未来工作"考虑任务间关联性"正是本研究方向。
- **实现关键细节**: 奖励分满足/不满足时延约束两种情况。动作编码 BOD(3bit)+LHI(log2(N+L)bit) 将指数空间压缩到多项式。
- **开源代码**: 无

---

## 必读论文

### [M02] Joint Offloading and Resource Allocation for Hybrid Cloud and Edge Computing in SAGINs
- DOI: 10.1109/JSAC.2024.3365899 | arXiv: 2401.01140
- **发表状态**: 正式发表
- **发表渠道**: IEEE JSAC 2024
- **核心贡献**: 提出 DM-SAC-H 算法（决策辅助混合动作空间多智能体 SAC），通过动作解耦将离散动作（用户配对、卫星选择、云选择）和连续动作（卸载比例、资源分配、UAV 轨迹）分配给不同智能体独立训练，再用 MAPPO 策略合并。四层 MEC 架构：地面用户-UAV-LEO-云。
- **方法概述**: **未使用 GNN**。完全基于全连接神经网络+SAC 框架。DAG 仅用于约束任务执行顺序，未利用拓扑信息作为网络输入特征。
- **DAG建模**: 每个地面用户多任务建模为 DAG，边表父子依赖。支持部分卸载（按比例分配到不同 MEC 单元）。DAG 随机生成，每用户 10 任务。**未用 GNN 处理 DAG 拓扑**。
- **DRL算法**: Multi-agent SAC with Hybrid Action Space (DM-SAC-H)。折扣因子 0.99, Adam, ~100,000 episodes。离散/连续各一套 SAC 网络。
- **实验设置**: TensorFlow-2, M=12用户, N=3 UAV, L=5 LEO(800km), K=3云。任务0.6-1.2MB, 3Gcycles。计算能力：地面0.1GHz, UAV 0.5GHz, LEO 1GHz, 云3GHz。G2U Rician, UAV-LEO 过时 CSI。
- **Baseline**: M-PPO, Parametrized DQN, A3C, DM-SAC-H NoCloud, DM-SAC-H NoISL NoCloud
- **关键结论**: DM-SAC-H 优于所有 baseline；云服务器和 ISL 对性能至关重要；用户数>11 时能耗急剧上升。
- **与本研究关系**: **高度相关但方法路径不同** — 同属 SAGIN+DAG+DRL，但用传统 SAC+FCN，本研究用异构图注意力网络。M02 的 DAG 仅做约束未做学习表示。
- **实现关键细节**: 部分卸载因子层层递减。决策辅助对不可用动作生成{s,a,0}训练对。
- **开源代码**: 无

### [M03] Deep Graph Fusion RL for Task Offloading in SAGIN
- DOI: 10.1109/GLOBECOM59602.2025.11432769
- **发表状态**: 正式发表
- **发表渠道**: IEEE GLOBECOM 2025
- **核心贡献**: 提出 GF-DRL 框架，核心创新是 Graph Fusion 机制——用 GCN 分别提取任务图和 UE 网络图特征，再通过 hard attention（LSTM+Gumbel softmax）和 soft attention（scaled dot-product）融合两张异构图。提出 AEGN 网络处理离散/连续混合动作空间。
- **方法概述**: **同构 GCN**（Kipf & Welling 2016）。网络图 G（UE+HAPS+LEO）和任务图 D（子任务+依赖边）分别 GCN 提取特征，IFE 步骤拼接节点特征，EC 步骤（hard+soft attention）构建跨图边，FM 步骤（GCN+FNN）生成融合特征。节点类型通过特征维度隐式编码（G节点2维、D节点3维），**非显式类型嵌入或异构图算子**。
- **DAG建模**: 每用户每时隙生成一个 task，含 J=30 子任务，parent-child 依赖边形成 DAG。子任务三元组(o_j,s_j,v_j)。依赖延迟取所有父任务完成时间最大值。
- **DRL算法**: 修改版 TRPO。batch=128, horizon=1024, Sigmoid, Adam。AEGN 用 autoencoder+MSE 训练动作映射。
- **实验设置**: U=10 UE, L=10 LEO, N=10 HAPS, J=30 子任务/task。消融用 J=20/40/50。
- **Baseline**: TRPO, PPO, SAC, DDPG, GF-DRL-UE（消融）, GF-DRL-Task（消融）
- **关键结论**: GF-DRL 任务完成率比最佳 baseline 高 16%。任务图特征比网络图特征更重要。
- **与本研究关系**: **高度相关但可差异化** — 同 SAGIN+DAG+GNN，但用同构 GCN+attention 拼接两张图，本研究用异构图注意力网络在消息传递层面实现跨类型交互。
- **实现关键细节**: 动作编码 BOD+LHI 压缩空间。奖励含任务完成/资源约束/频率违规三项加权。
- **开源代码**: 无

### [M04] Intelligent Collaborative Computing Offloading in Satellite-Cloud-MEC IoVs
- DOI: 10.1109/TCCN.2025.3548630
- **发表状态**: 正式发表
- **发表渠道**: IEEE TCCN, Vol. 11, No. 6, Dec. 2025
- **核心贡献**: 提出 LEO 星座辅助 IoV 的协作计算卸载与多维资源切片联合优化。双时间尺度 HMDP 框架（长期频谱切片+短期资源分配）。设计层次混合 Actor-Critic (HAC) 架构处理参数化动作空间，提出 HHDDPG 和 HHPPO 两种算法。
- **方法概述**: **不使用 GNN**。FCNN [200,64] + Tanh + Adam。状态为展平标量向量。核心创新在 DRL 框架设计（双时间尺度 HMDP + HAC）。
- **DAG建模**: **无 DAG**。每车辆每时隙独立任务，五条卸载路径（VM/VSM/VMC/VSMC/VSLC）。
- **DRL算法**: HHDDPG（off-policy, DDPG-based HAC）和 HHPPO（on-policy, PPO-based HAC）。HAC: Actor-Net1 离散 → 拼接状态 → Actor-Net2 连续。HHDDPG: gamma=0.8, tau=0.02; HHPPO: gamma=0.9, clip=0.3。
- **实验设置**: 800m 双车道, 1 MBS + 4 SBS, 2 LEO(550km)。车辆 Poisson 到达。任务50-100Mcycles, 5-50ms 延迟容忍。Sub-6GHz 4MHz, Ka-band 10MHz。~500 episodes 收敛。
- **Baseline**: PPO, DDPG, ER（等分+随机）, MSA（等分+最大SNR）
- **关键结论**: HHPPO 比 PPO 奖励高 7.63%，HHDDPG 比 DDPG 高 15.15%。低资源场景优势最大。
- **与本研究关系**: **间接相关** — 卫星边缘计算+卸载但无 GNN、无 DAG。双时间尺度分解思路和 HAC 混合动作架构可参考。
- **实现关键细节**: 长期 agent 奖励为短期 agent 累积奖励。STL 用 Rician(K=7)+Ka-band 路径损耗。
- **开源代码**: 无

### [M05] Optimizing Resource Utilization in LEO Satellite Edge Computing
- DOI: 10.1109/JIOT.2026.3668808
- **发表状态**: 正式发表
- **发表渠道**: IEEE IoTJ, Vol. 13, No. 10, May 2026
- **核心贡献**: 提出面向服务的 LEO 卫星边缘计算联合优化框架。双时间尺度：大时间尺度用改进原子轨道搜索（iAOS）启发式优化服务部署与资源配置，小时间尺度用方向选择性多智能体 DDQN（DS-MDDQN）实现实时任务路由。集成真实世界人口分布数据。
- **方法概述**: **不使用 GNN**。每颗卫星作为独立 DRL 智能体，观测空间含本星及四邻居资源/距离/可达性/任务特征，手工特征拼接 + MLP。双时间尺度分解：iAOS(分钟级) + DS-MDDQN(事件驱动)。
- **DAG建模**: **无 DAG**。任务为独立单体任务 {Zi,Li,Vm}，无任务间依赖。任务可在多卫星间多跳转发但路径是线性序列。
- **DRL算法**: DS-MDDQN（方向选择性多智能体 DDQN）。6维离散动作（local/up/down/left/right/cloud）。epsilon-greedy, 经验回放, 双网络。CTDE。lr=0.0001, batch=128。延迟奖励沿路径回传。
- **实验设置**: Iridium(66卫星/6轨道/780km) + OneWeb(648/18/1200km)。7000-19000用户，NASA GPWv4人口数据。STK 轨道动力学。大时间尺度窗口 T=5min。
- **Baseline**: AOS-MDDQN, PSO-MDDQN, HJO, OPT, FAG, RDO（联合对比）；PSO,FA,Random,Stationary（部署对比）；CDRL,IDRL,GA,Greedy,Random（卸载对比）
- **关键结论**: 19000用户时 CRU 超 AOS-MDDQN 15.5%，TFP 从 11.62% 降至 5.26%。DS-MDDQN 接近集中式上界（差距<6%）。本地计算>50%。
- **与本研究关系**: **场景重叠但任务建模差异大** — 同 LEO+任务卸载，但独立任务 vs 本研究的 DAG 依赖任务，不使用 GNN vs 本研究异构图注意力。双时间尺度思路可借鉴。
- **实现关键细节**: 服务热度 Zipf 分布，任务到达非齐次 Poisson，ISL 四链路拓扑，FCFS 排队。iAOS 修复机制按效用/资源比排序。
- **开源代码**: 无

### [M06] Dependency-Aware Task Offloading Strategy via HGAT (IoTJ 2025)
- DOI: 10.1109/JIOT.2025.3549441
- **发表状态**: 正式发表
- **发表渠道**: IEEE IoTJ, Vol. 12, No. 13, July 2025
- **作者**: Jinming Wu et al. (北京理工大学)
- **核心贡献**: 提出 HGAT-PPO 框架，在多用户多服务器云辅助 MEC 场景下实现 DAG 依赖感知端到端任务卸载。两套独立 GAT 编码器（Task DAG + Server 竞争图），PPO 联合决策子任务选择与服务器核心分配，无需启发式排序。训练 5+5 场景直接泛化到 20+10。
- **方法概述**: **"HGAT" = 两套独立 GAT 编码器，非 HAN 意义上的多节点类型注意力**。Task Encoder: 标准 GAT 处理 DAG，已完成子任务动态 mask。Server Encoder: 修改版 GAT 处理无向竞争图，注意力引入多维边特征变换。两套独立权重，无显式类型嵌入。异构性体现在图结构不同（有向vs无向）和注意力机制不同，非元路径驱动。
- **DAG建模**: DAG_m=(V_m,E_m,R_m)，节点属性{D^prog, C^l/e/c, D^out, OA}，有向边表数据依赖。感知/执行类子任务必须本地执行。状态随调度逐步收缩。
- **DRL算法**: PPO, clip surrogate, GAE, invalid action masking, Adam, lr=2e-4, 2层GAT, 4头注意力, ~1500 steps 收敛。Actor 逐 pair 输出 logit。
- **实验设置**: Python 3.10 + PyTorch 2.4, i7-12700 + 32GB + RTX 3060Ti。5 ICV + 5 边缘 + 1 云。daggen: node=16, fat=0.6, density=0.4。CPU周期 U(1e9,3e9)。可扩展性：训练 5+5，测试到 20+10。
- **Baseline**: ALE, ROE, LPGO, VTSPO, ODCO, HGAT-A2C, HGCN-PPO, HGCN-A2C
- **关键结论**: 比 LPGO 成本降低 19.48%。GAT 优于 GCN（3.33%提升）。通信量增大时优势更明显。可扩展到 20+10 仍保持 >11% 优势。
- **与本研究关系**: **核心差异化** — M06 车联网 MEC，本研究卫星边缘计算。M06 的"HGAT"是两套独立 GAT，本研究若用真正基于类型嵌入的多关系注意力即构成显著差异化。与 K1 同一作但不同论文（DOI 不同）。
- **实现关键细节**: F 值递归从入口任务正向传播。Server Graph 边权重=共同竞争候选子任务特征之和，动态更新。Reward=成本下降值（贪心下界估计）。
- **开源代码**: 无（DAG 生成用 daggen 库）

### [M07] Dynamic Caching Dependency-Aware Task Offloading in MEC
- DOI: 10.1109/TC.2025.3533091
- **发表状态**: 正式发表
- **发表渠道**: IEEE Transactions on Computers, Vol. 74, No. 5
- **核心贡献**: 提出 CachOf 方案，首次在 MEC 中同时考虑 DAG 任务依赖、动态边缘缓存、任务卸载和资源分配联合优化。基于 DAG 拓扑的子任务优先级计算（执行优先级+卸载优先级），0-1 背包动态缓存策略，DDPG 处理连续动作空间卸载决策。
- **方法概述**: **不使用 GNN**。DAG 仅用于优先级排序和缓存决策，不学习图结构表示。三阶段流水线：DAG 优先级计算 → 动态缓存更新 → DDPG 卸载决策。
- **DAG建模**: DAG={V,E,U}，节点 v_{m,i}={d,c,t}，有向边表前驱-后继依赖，边权重为数据传输量。执行优先级按拓扑层级赋值，卸载优先级按 LST 计算。同优先级可并行。
- **DRL算法**: DDPG, 4层 FCN, tanh。经验池 6400, batch 64, actor lr=0.0001, critic lr=0.001, gamma=0.99, 1000 episodes。
- **实验设置**: Python 3.7。10 异构 RSU(2.0-2.8GHz, 缓存20-30MB)。本地设备 0.5GHz。子任务0.8-1.2MB, 0.1-1.0Gcycles。延迟约束 10s。10 次独立运行平均。
- **Baseline**: StCach, RdmOf, CachDQN, CachGA, G+DQN[Li TVT 2023]
- **关键结论**: CachOf 优于所有 baseline。500 episode 收敛。缓存容量/计算能力增大、子任务数减少时优势更明显。
- **与本研究关系**: **方法可借鉴** — DAG 优先级计算方案（执行+卸载分离）可参考。但无 GNN、地面 MEC 场景，与本研究差异大。
- **实现关键细节**: 动态缓存按优先级时间槽划分，每槽重算内容流行度。负载均衡分配给负载较低服务器。
- **开源代码**: https://github.com/NetworkCommunication/CachOf

### [M08] Dependency-Aware Task Offloading for Satellite Mobile-Edge Computing
- DOI: 10.1109/JIOT.2025.3596638
- **发表状态**: 正式发表
- **发表渠道**: IEEE IoTJ, Vol. 12, No. 20, Oct. 2025
- **核心贡献**: 提出三层卫星-地面协同计算卸载框架（地面 IoT/LEO MEC/云），DDAG-CHSS-DDPG 算法：动态 DAG 拓扑排序生成合法执行序列 + 簇头选择策略优化设备-卫星关联 + DDPG 混合动作空间决策。平均延迟降低 18.07%，能耗降低 21.15%。
- **方法概述**: **不使用 GNN**。DAG 依赖通过传统拓扑排序（Kahn 算法）处理，不学习图结构表示。全连接网络做 DRL 策略。簇头选择用 K-means + 加权评分（启发式）。
- **DAG建模**: DAG G=(Ti,L)，有向边表依赖。DDAG 模块拓扑排序生成执行序列 O(Ki)。延迟按关键路径（critical path）最大值计算。子任务属性 {ri,k, ci,k, t_max_i}。DAG 数据来自 Alibaba Cluster Trace 2018。
- **DRL算法**: DDPG, Actor 3层(400-128-64) ReLU+tanh, Critic 同构。混合动作：Actor 输出 [0,2] 连续值 rounding 到 {0,1,2}（本地/LEO/云）。buffer 20000, batch 128, tau=0.01, gamma=0.99, actor lr=0.001, critic lr=0.002。集中式训练（云）+ 分布式执行。
- **实验设置**: 200km×200km，Walker 15×15 星座，STK 仿真，扫描角 45°。IoT 0.2-0.7GHz，LEO 2.0-2.4GHz。NOMA 上行。ISL 最多 2 跳协作。Alibaba Cluster Trace v2018。
- **Baseline**: BDAG-CHSS-DDPG, Local-Only, LEO-Only, DDAG-noCHSS-DDPG, DDAG-DCHSS-DDPG, DDAG-CHSS-AC, DDAG-CHSS-Dueling-DQN, DDAG-CHSS-DQN, DDAG-CHSS-GA
- **关键结论**: DDAG 拓扑排序优于 BFS。CHSS 比无簇头奖励高 37.93%。DDPG 在混合动作空间优于 AC/DQN/GA。
- **与本研究关系**: **互补性强，可直接差异化** — 同卫星+DAG+DRL，但不用 GNN（拓扑排序），缺乏图结构学习能力。本研究用异构图注意力学习 DAG 和系统拓扑的 embedding。M08 的三选一卸载和启发式簇头选择可做对比 baseline。
- **实现关键细节**: 离散动作连续化（rounding）。状态归一化（除以最大值后加权）。覆盖时间约束确保任务在 LEO 覆盖时间内完成。
- **开源代码**: 无（DAG 数据：Alibaba Cluster Trace v2018）

### [M09] UGV-Assisted Task Allocation for UAVs: HGRL (U2GNet)
- DOI: 10.1109/TSC.2026.3651622
- **发表状态**: 正式发表
- **发表渠道**: IEEE TSC, Vol. 19, No. 1, Jan/Feb 2026
- **核心贡献**: 提出 U2GNet 框架，双层 HGAT 架构处理 UAV-UGV 异构协作。Group-specific encoder + type-specific V 投影 + 两阶段图（观测图/通信图）+ GRU 处理部分可观测性 + IPPO。数据收集率提升 16.90%，任务完成率提升 10.81%。
- **方法概述**: **分组 GAT，非 HAN/HGT 元路径机制**。(1) UAV/UGV 各有独立 MLP encoder；(2) 第一层 HGAT（观测图，4头注意力，V 矩阵 type-specific）；(3) Inter-group FC 融合；(4) 第二层 HGAT（通信图）；(5) GRU 整合历史。异构性体现在分组 encoder + type-specific projection + 双层图分离。
- **DAG建模**: **无 DAG**。任务为数据采集+处理两阶段流水线，按连续比例卸载（zeta_u 本地 + zeta_v 各 UGV）。
- **DRL算法**: IPPO, 每个 agent 独立 policy + 共享 value。GAE(λ=0.95), 熵正则, buffer 50000, mini-batch 128, lr=1e-4, gamma=0.99。
- **实验设置**: 1km×1km, 25 UAVs + 5 UGVs。UAV 高度 100m, 速度 25m/s。NOMA+SIC, R_obs=90m, R_comm=150m。FC/GRU 256 units, HGAT 2层×4头。单步决策 ~20.18ms。
- **Baseline**: CommNet, DGRL, DDQN, Random, HGN, EHCAMAN
- **关键结论**: HGAT > GAT（任务完成率差 20.4%），证实 type-specific 建模必要性。GRU 贡献显著（去掉降 ~10.65%）。扩展到 25+15 时 ~24.5ms，近似 O(M)。
- **与本研究关系**: **方法可借鉴** — type-specific encoder/projection 设计范式、双层图分离观测与通信的思路可迁移到卫星场景（卫星-地面站-用户多类型节点）。但无 DAG、无卫星场景、简化分组 GAT 而非真正 HAN/HGT。
- **实现关键细节**: 连续动作空间（卸载比例+计算资源+DVFS）。奖励四项加权和（归一化 w_i）。Air-to-Ground LoS/NLoS 概率模型。通信 dropout 鲁棒训练。
- **开源代码**: 无

### [M10] Nash-regularized Heterogeneous Graph Transformer for Task Offloading
- DOI: 10.5267/j.ijdns.2025.9.009
- **发表状态**: 正式发表
- **发表渠道**: IJDNC, Vol. 10, pp. 415-432, 2026
- **核心贡献**: 提出 HGT-DQN-NEI，将超图 Transformer + Dueling DQN + Nash 均衡博弈三者整合。超图建模异构网络拓扑，DQN 损失函数嵌入 Nash 均衡正则化（KL 散度约束策略向博弈均衡收敛），虚拟博弈迭代计算分布式 Nash 均衡。6G 智慧城市场景下延迟降低 23.4%，能效提升 31.7%。
- **方法概述**: **超图 + Transformer 注意力**（非传统 HAN/HGT）。网络建模为超图 H(t)=(V,E,W)，超边可连接多元关系。多头超图注意力（16头, hidden=1024），类型特定变换矩阵 W_e^(h)。Dueling DQN（3个并行策略头集成）处理部分可观测。Deep Transformer Q-Network (DTQN) 序列建模。
- **DAG建模**: **无 DAG**。独立任务，三选一卸载（local/edge/cloud）+ 连续资源分配。任务间无依赖。
- **DRL算法**: Dueling DQN + 多头策略头集成。经验回放 100000, 目标网络 tau=0.005, cosine annealing LR, epsilon 衰减 0.997, 梯度裁剪 1.0。Nash 正则化权重 λ=0.05。
- **实验设置**: 50 设备 + 10 边缘 + 3 云。可扩展性测试 10-70 设备。5 实际场景（Urban/Suburban/Highway/Industrial/Rural）。120-200 episodes, 50-60 steps/episode。
- **Baseline**: Random, Greedy local, Greedy edge, Load balancing, Threshold, Lyapunov, Standard DQN
- **关键结论**: 注意力机制贡献最大（消融）。Nash 正则化主要作用在收敛稳定性。声称 O(n^0.01) 复杂度但实验仅测到 70 设备。
- **与本研究关系**: **间接相关** — 超图+Transformer 方法可借鉴，但无 DAG、地面 6G 场景、baseline 层次浅。IJDNC 非顶刊，结果可信度需谨慎（可扩展性数据异常一致）。
- **实现关键细节**: 虚拟博弈每 10-15 episodes 更新，40-80 次迭代。状态向量 32 维。Python Enhanced6GEnvironment 仿真。
- **开源代码**: 无

### [M11] Graph-Based RL for Privacy-Preserving Task Offloading in Satellite-Terrestrial Networks
- DOI: 10.1109/Satellite67108.2025.11430442
- **发表状态**: 正式发表
- **发表渠道**: IEEE ICSC/Satellite 2025（会议论文，中山大学 + 北京控制工程研究所）
- **核心贡献**: 提出 PGPPO 框架，首次在星地网络任务卸载中建模两类隐私威胁（任务语义暴露 + 路径重构风险）。GNN 编码时变网络拓扑，Constrained MDP 建模性能-隐私权衡，PPO-Lagrangian 求解。
- **方法概述**: **同构 GNN**，标准 message-passing 范式（MLP 融合源/目标/边特征 → 置换不变聚合 → MLP 更新）。**非异构图网络，无注意力机制**。节点含用户/卫星/云三类但统一处理。
- **DAG建模**: **无 DAG**。独立任务三元组 (d, c, Δ_max)，三个卸载目的地。
- **DRL算法**: PPO-Lagrangian（多头 PPO），拉格朗日乘子动态调整。组合优势函数 A_hat_L = A_hat_R - Σ μ_i * A_hat_Ci。
- **实验设置**: 用户数 60-200。具体卫星参数因篇幅未详述。公式因 PDF 转换丢失。
- **Baseline**: 标准 PPO（无隐私）, Static-Privacy（固定非自适应）
- **关键结论**: PGPPO 性能接近无隐私 PPO，隐私风险远低于 PPO。
- **与本研究关系**: **不构成直接竞争** — 同构 GNN、无 DAG、核心创新在隐私保护而非调度优化。GNN 编码时变卫星网络的方法（快照图+节点/边特征设计）可参考。
- **实现关键细节**: 时变图快照模型。节点四元组(类型α,可信度τ,算力ρ,队列ω)，边二元组(可行性λ,带宽b)。
- **开源代码**: 无

### [M12] Accuracy-Aware MLLM Task Offloading in UAV-Assisted Satellite Edge
- DOI: 10.3390/drones9070500
- **发表状态**: 正式发表
- **发表渠道**: Drones 2025, 9(7), 500 (MDPI, Open Access)
- **核心贡献**: 提出 UAV 辅助卫星边缘计算中的 MLLM 推理框架，联合优化任务卸载与资源分配（MINLP）。AD-SAC 算法处理混合离散-连续动作空间（离散卸载+连续功率/UAV轨迹）。MLLM 精度约束：UAV 部署小模型(3B)、LEO 部署大模型(13B)，按 IoTD 精度需求匹配节点。
- **方法概述**: **不使用 GNN**。3层 FC [256,256,256] + ReLU。AD-SAC 将 Q 函数拆分为离散 agent 和连续 agent，各自独立 SAC（共 8 个网络），MAPPO 整合解耦策略。
- **DAG建模**: **无 DAG**。独立 MLLM 任务，全卸载（binary offloading），不拆分不多跳。
- **DRL算法**: AD-SAC。离散+连续 agent 各 4 网络。actor/critic lr=0.001, batch=64, buffer=10000, gamma=0.995, tau=0.01, 1000 epochs。
- **实验设置**: 500m×500m, K=10 IoTDs, M=3 UAVs(40-60m), N=4 LEO(500km)。UAV Jetson Orin NX, LEO Jetson AGX Orin。MMMU benchmark。3s 时隙, 100 时隙/episode。Xeon 8370C + GTX 4090。Rician + Rician-Shadowed 信道。
- **Baseline**: Random, PPO, D3QN, DDPG, Hybrid-PPO, AD-SAC-D(消融), AD-SAC-C(消融)
- **关键结论**: AD-SAC 优于所有 baseline。精度要求 0.5→0.6 是转折点（系统从 UAV 为主切到卫星为主）。解耦设计必要（消融证实）。
- **与本研究关系**: **互补差异大** — 无 GNN、无 DAG、核心创新在 MLLM 精度约束。AD-SAC 混合动作空间解耦思路可参考。
- **实现关键细节**: LEO 可见窗口纳入 MDP 状态。ISL 多跳用指示函数。精度约束作为 hard constraint。奖励 = beta_r / (eta_l*T + eta_e*E)。
- **开源代码**: 无

---

## 综合分析

### 1. 现有方法分类

**A. 卫星/空天地场景 + DRL（无 GNN）**
- M02 (JSAC 2024): 多智能体 SAC + 动作解耦，SAGIN 四层架构
- M04 (TCCN 2025): 双时间尺度 HMDP + HAC 混合 Actor-Critic
- M05 (IoTJ 2026): DS-MDDQN + iAOS 启发式，Iridium 星座
- M08 (IoTJ 2025): DDPG + 拓扑排序 DAG + 簇头选择，Walker 星座
- M12 (Drones 2025): AD-SAC + MLLM 精度约束
- 共同特点：全连接网络策略，不利用图结构信息

**B. 卫星/空天地场景 + GNN + DRL（同构 GNN）**
- K2/M01 (TMC 2026): **同构 GraphSAGE** + AMAPPO，卫星 DAG 任务卸载 — 最直接竞争者
- K3 (JSAC 2025): **同构 GCN** + TRPO + MAML，SAGIN 独立任务
- M03 (GLOBECOM 2025): **同构 GCN** + Graph Fusion（hard+soft attention 融合双图），SAGIN DAG 任务
- M11 (Satellite 2025): **同构 GNN** + PPO-Lagrangian，星地网络隐私保护
- 共同特点：不区分节点类型，共享参数，无类型嵌入/类型感知消息传递

**C. 地面/UAV 场景 + "异构图" + DRL**
- K1/M06 (IoTJ 2025): 两套独立 GAT 编码器（Task DAG + Server 竞争），车联网 DAG — 名不副实的"HGAT"
- M09 (TSC 2026): 分组 GAT + type-specific V 投影 + 双层图，UAV-UGV — 简化分组 GAT
- M10 (IJDNC 2026): 超图 Transformer + Nash 正则化，6G 地面 — 非传统 HAN/HGT
- 共同特点：都不是真正的 HAN（Wang et al. WWW 2019）意义上的基于元路径/关系类型的多节点类型注意力

**D. 地面 MEC + DAG + DRL（无 GNN）**
- M07 (TC 2025): DDPG + 拓扑排序 + 动态缓存
- 共同特点：DAG 仅用规则驱动处理，不学习图结构表示

### 2. 已知局限

1. **同构 GNN 无法区分节点类型**（K2/M01, K3, M03）：卫星/UAV/地面站/IoT 计算能力、移动性、能量约束差异巨大，同构 GNN 共享参数导致信息损失
2. **DAG 依赖未学习表示**（M02, M08, M07）：仅用拓扑排序等规则方法处理 DAG，无法捕获 DAG 拓扑的高阶语义特征
3. **"异构图"名不副实**（K1/M06）：两套独立 GAT ≠ 真正的异构图注意力（无类型嵌入、无类型感知消息传递、无元路径）
4. **缺乏跨场景 DAG + 异构图方法**：现有 HGAT 方法（K1/M06, M09, M10）均在地面/UAV 场景，无一应用于卫星边缘计算；卫星场景的 DAG 方法（M08, K2/M01）均用同构 GNN 或无 GNN
5. **卫星动态性建模不足**：多数方法假设静态或准静态拓扑，未充分处理 LEO 高移动性带来的间歇连接和拓扑时变

### 3. 2-3 年趋势

1. **DAG 依赖建模从规则驱动走向学习驱动**：2023-2024 年用拓扑排序/启发式处理 DAG（M07, M08），2025-2026 年开始用 GNN 学习 DAG 表示（K2/M01 GraphSAGE, M03 GCN Graph Fusion），但尚未有人用异构图注意力统一建模网络拓扑和任务 DAG
2. **图神经网络从同构走向异构**：2024-2025 年卫星边缘计算论文主要用同构 GNN（GraphSAGE/GCN），2025-2026 年地面/UAV 场景出现"异构图"方法（HGAT, HGT），但均非真正的 HAN/HGT，且尚未迁移到卫星场景
3. **DRL 算法从单智能体走向多智能体 + 混合动作空间**：趋势从 DDPG/DQN 到 MAPPO/PPO，从纯离散/连续到混合动作空间（离散卸载+连续资源分配）
4. **场景从单一 SAGIN 走向异构协同**：从单纯的地面 MEC 到 SAGIN 三层架构，再到卫星-地面协同边缘计算，节点异构性日益突出但建模方法未跟上
5. **本文定位在趋势交汇点**：DAG 学习表示 + 真正异构图注意力 + 卫星边缘计算 + 多智能体混合动作空间 — 正好填补现有文献的空白三角

---

## 差异化定位矩阵

| 维度 | K2/M01 | K3 | M03 | M08 | K1/M06 | M09 | M10 | **本文** |
|------|--------|-----|-----|-----|--------|-----|-----|---------|
| 场景 | 卫星 | SAGIN | SAGIN | 卫星 | 车联网 | UAV-UGV | 6G地面 | **卫星边缘** |
| DAG | 有 | 无 | 有 | 有 | 有 | 无 | 无 | **有** |
| GNN | GraphSAGE | GCN | GCN | 无 | 双GAT | 分组GAT | 超图Trans | **HGAT** |
| 异构? | 同构 | 同构 | 同构 | - | 伪异构 | 简化异构 | 超图 | **真正异构** |
| 类型嵌入 | 无 | 无 | 无 | - | 无 | type-specific V | 类型矩阵 | **类型嵌入+类型感知注意力** |
| DRL | MAPPO | TRPO | TRPO | DDPG | PPO | IPPO | DQN | **待定** |

**核心差异化**：唯一同时具备 (1) 卫星边缘计算场景、(2) DAG 依赖任务建模、(3) 真正异构图注意力网络（类型嵌入+类型感知消息传递）的方法。

---

## Baseline 交叉验证

### Baseline 出现频率统计

**共识 DRL 算法（作为对比方法出现）：**

| 方法 | 作为 baseline | 作为核心方法 | 使用论文 | 代码状态 | 算法描述质量 | 推荐优先级 |
|------|-------------|-------------|---------|---------|------------|-----------|
| PPO (vanilla) | 5 篇 | 3 篇 (K1/M06, M11) | K3, M03, M04, M11, M12 | 自实现 | 标准 | 共识 baseline |
| DQN/DDQN/D3QN | 4 篇 | 0 | M08, M09, M10, M12 | 自实现 | 标准 | 共识 baseline |
| DDPG | 3 篇 | 2 篇 (M07, M08) | K3, M03, M12 | 自实现 | 标准 | 共识 baseline |
| SAC | 2 篇 | 2 篇 (M02, M12) | K3, M03 | 自实现 | 标准 | — |
| TRPO | 1 篇 | 2 篇 (K3, M03) | M03 | 自实现 | 标准 | — |

**论文特有方法（均为核心方法，未被其他论文用作 baseline）：**

| 方法 | 作为 baseline | 作为核心方法 | 来源 | 代码状态 | 算法描述质量 | 推荐优先级 |
|------|-------------|-------------|------|---------|------------|-----------|
| AMAPPO+GraphSAGE | 0 | 1 | K2/M01 (TMC 2026) | 无 | 高 | **1** |
| GDRL (GCN+TRPO+MAML) | 0 | 1 | K3 (JSAC 2025) | 无 | 高 | **2** |
| DDAG-CHSS-DDPG | 0 | 1 | M08 (IoTJ 2025) | 无 | 中 | 3 |
| CachOf (DDPG+DAG priority) | 0 | 1 | M07 (TC 2025) | 有(GitHub) | 高 | 4 |
| GF-DRL (GCN+GraphFusion) | 0 | 1 | M03 (GLOBECOM 2025) | 无 | 中 | 5 |

> 注：论文特有方法均为 2025-2026 年前沿工作，尚未被广泛采纳为领域 baseline，但它们是与本文最直接的可对比方法。精读 14 篇 > 8 篇门槛，无需降级策略。

### Baseline 候选

| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: AMAPPO+GraphSAGE | K2/M01 | 无(domain-comms优先级3) | 1 | 最直接竞争者：卫星+DAG+同构GNN，差异化定位矩阵唯一共享全部三个问题域特征的方法；MVE已验证HGAT>GraphSAGE(+10.7% avg) |
| B2: GDRL(GCN+TRPO简化) | K3 | 无(domain-comms优先级3) | 2 | JSAC顶刊+K3未来工作"考虑任务间关联性"即本研究方向，叙事链强；GCN vs GAT对比验证类型感知注意力价值；简化实现(砍MAML)约2天 |
| PPO (vanilla) | 共识(5篇) | 自实现 | 共识 | 领域最广泛使用的on-policy DRL baseline |
| DDPG (vanilla) | 共识(3篇) | 自实现 | 共识 | 领域最广泛使用的off-policy DRL baseline |
| Random + Greedy | 通用 | 自实现 | 共识 | 无学习/启发式下界 |

**简化决策记录**：K3 砍掉 MAML 元学习（价值在"快速适配新环境参数"，与本文对比目标无关），仅实现 GCN+TRPO+AMN 混合动作空间。M07 CachOf 代码仅用于管线验证，不作正式 baseline。M08/M03 视时间追加。
