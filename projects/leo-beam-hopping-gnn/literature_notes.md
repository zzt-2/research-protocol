# Literature Notes — Beam Hopping + GNN

> 项目: leo-beam-hopping-gnn | 方向: 多波束LEO卫星Beam Hopping + GNN建模波束间空间干扰耦合
> 更新: 2026-05-15 | 精读: 8篇

---

## 核心论文精读

### [L01] Meta-Learning for GNN-Based Power Allocation in LEO Satellite Communications
- DOI/来源: 10.1109/TVT.2024.3477601
- 发表状态: 正式发表
- 发表渠道: IEEE TVT (SCI Q1/Q2), Vol. 74, No. 2, Feb 2025
- 年份/会议: 2025, IEEE TVT
- 核心贡献: 针对LEO卫星多波束功率分配，提出基于GNN的无监督策略，利用领域知识设计聚合函数（邻居干扰功率之和）。引入元学习实现zero-shot泛化到未见流量分布，+30%数据速率。
- 方法概述: 非RL/MDP方法。每个波束作为图节点，特征=[需求r_i, 信道增益|h_i^H w_i|^2]，边=干扰链路增益。GNN N层消息传递后softmax输出功率分配。元学习在16种流量分布上meta-training。
- 实验设置: Starlink 1150km, Ku 11.45GHz, 49×49 UPA, p_max=40dBm, σ_n²=-97dBm, 默认19波束(测试7/37/61)
- 使用的 Baseline 方法:
  - FNN: 自实现，输入NC×3
  - EPA: p_i=p_max/N_C，自实现
  - WMMSE: Shi 2011 TSP，自实现
- 关键结论: GNN+meta比EPA/WMMSE提升30%；GNN从19波束训练直接部署到7/37/61（可扩展）；meta-training后zero-shot无需额外样本
- 与本研究关系: 方法可借鉴 — GNN图构建（节点=波束，边=干扰，聚合=干扰功率和）可直接迁移到BH场景
- 实现关键细节: 损失L(Θ)=-E[Σmin(s_i,r_i)]；功率通过softmax归一化；聚合消息a_i=Σ|h_i^H w_j|^2（领域知识设计）
- 开源代码: 无
- 验证状态: 已验证

**结构化提取：**

1. 状态空间（GNN输入，非RL）:
   | 维度名 | 范围/取值 | 归一化 |
   |--------|----------|--------|
   | 需求r_i | 均匀/指数/空间相关 | 原始值 |
   | 信道增益\|h_i^H w_i\|^2 | Rician信道 | 原始值 |
   | 干扰增益\|h_i^H w_j\|^2 | 邻居波束 | 聚合为a_i |

2. 动作空间: 连续，N_C维，softmax归一化后×p_max

3. 目标函数: L(Θ)=-E[Σᵢmin(ŝᵢ,rᵢ)]，ŝᵢ=log₂(1+SINRᵢ)

4. 建模假设: 全频复用→所有波束间存在干扰；Rician衰落；码本预编码；单链路/波束

5. 网络架构: FNN(Φ功率更新)+FNN(U embedding)+FNN(Ω输出softmax)，N层消息传递。SGD优化，I_meta=3, N_sgd=5000

6. 适配性分析: 适配—图构建方式和领域知识聚合函数可迁移；不适配—连续功率分配非离散BH调度；改进—将GNN编码器接入DRL策略网络输出BH决策

7. 信道模型: 下行自由空间+Rician(g_i~Rice(...))+UPA阵列响应(49×49)+码本预编码。Ku 11.45GHz, h=1150km

---

### [L02] Interference-Suppressed Joint Channel/Power Allocation: Dynamic Hypergraph NN
- DOI/来源: 10.1109/TWC.2025.3586230
- 发表状态: 正式发表
- 发表渠道: IEEE TWC (中科院1区TOP/JCR Q1), Vol. 25, 2026
- 年份/会议: 2026, IEEE TWC
- 核心贡献: 提出动态超图NN(HGNNRA)用于大规模LEO下行联合信道+功率分配。超边建模many-to-many干扰关系（超边=所有对某用户产生同频干扰的节点集合），GRU驱动权重时序演化适应时变拓扑。
- 方法概述: 非RL方法。动态超图构建（Algorithm 1）→DynHGNN卷积（HGNN层+GRU权重演化）→MLP-p(Sigmoid输出功率)+MLP-f(Softmax+one-hot输出信道)。端到端监督学习。
- 实验设置: Starlink 500km, Ka 20GHz, B=20MHz, 4子信道×5MHz, D=1m天线, K∈{2,3,4}星×2波束, U∈{3,4,5}/波束, σ²∈{-120,-80}dBm
- 使用的 Baseline 方法:
  - GCN: pairwise边建模干扰
  - HGNN: 静态超图，仅功率优化
  - GNN-DDQN: GNN+RL
  - GCNRA: HGNN→GCN消融
- 关键结论: 超图优于图(HGNNRA>GCNRA)；动态优于静态；波束过多反而下降(干扰加剧)
- 与本研究关系: 方法可借鉴 — 超图建模可直接迁移到BH(节点=波束-时隙，超边=同频干扰约束)
- 实现关键细节: 节点特征4维(CSI,需求,覆盖波束数,干扰节点数)；功率Sigmoid映射(0,1)×p*；信道Softmax→argmax→one-hot；超边权重全1(等权)
- 开源代码: 无
- 验证状态: 已验证

**结构化提取：**

1. 状态空间: 4维节点特征(CSI h, 需求R_u*, 覆盖波束数|C_u|, 干扰节点数)
2. 动作空间: 混合—功率1维Sigmoid连续+信道M维Softmax离散
3. 损失函数: L=-(1/|U|)ΣR_u + 平衡项，非RL
4. 建模假设: 等波束宽度；圆形覆盖近似；完美CSI；等权超边
5. 网络架构: HGNN卷积×2(ni=4→nh=32→no=32)+GRU(每层1个)+MLP-p(32→1,Sigmoid)+MLP-f(32→4,Softmax)。Adam lr=1e-5, wd=1e-6, 500 epoch
6. 适配性分析: 适配—超边建模和GRU动态机制可迁移；不适配—固定子信道数M=4非BH pattern；改进—将超边权重从标量扩展为特征向量(含干扰强度)
7. 信道模型: 自由空间+Bessel天线增益(A_D=31.6dBi)。Ka 20GHz, h=500km, AWGN

---

### [L03] Distributed BH Scheduling for LEO Mega-Constellation via Hierarchical MADRL
- DOI/来源: 10.1109/TWC.2026.3659941
- 发表状态: 正式发表
- 发表渠道: IEEE TWC (SCI Q1), Vol. 25, 2026
- 年份/会议: 2026, IEEE TWC
- 核心贡献: 分层MADRL框架(BH-HMARL)，上层QPLEX+CRO做卫星-小区关联(长期)，下层QPLEX做波束调度(短期5ms)，CLA注意力跨层融合。吞吐量+16-74%。
- 方法概述: CTDE范式。上层离散选择每星服务小区(约束|a|≤K)，下层连续+离散分配波束。QPLEX值分解+GELU激活+CRO冲突消解+CLA注意力加权Q值。在线滑动窗口微调。
- 实验设置: Walker-Delta(12面×22星, 53°, 550km), 每星8波束, 648小区, 需求20-700Mbps, 全频复用, BHTP双层(T_H≈15s, T_slot≈5ms)
- 使用的 Baseline 方法:
  - BH-QMIX: Lin TWC 2024
  - BH-QPL: 队列长度优先贪心
  - BH-P: 固定轮询
  - BH-HDP: 需求量贪心
  - BH-JBSPO: 集中式优化
  - BH-VDN: 值分解
- 关键结论: 全面超越6种baseline；星座越大优势越显著；单星执行4ms<5ms约束；消融CRO/CLA/ASS降13-38%
- 与本研究关系: 直接相关 — 核心竞品baseline。Q-learning系不建模波束间空间关系，正是GNN切入点
- 实现关键细节: 奖励r_t=(1-β-γ)Γ/Γ_norm - βΨ/Ψ_norm - penalty + γ(1-|l-l̄|²)；功率均分P/K；GELU激活
- 开源代码: 无
- 验证状态: 已验证

**结构化提取：**

1. 状态空间: 5维矩阵(D_t需求, Q_t排队, Δ_t延迟, H_t信道, L_t负载)，维度N×R_n×{1,T,1,K,1}
2. 动作空间: 混合—上层离散选≤K个小区，下层连续+离散(波束分配+功率)
3. 奖励函数: r_t=(1-β-γ)Γ(t)/Γ_norm - βΨ(t)/Ψ_norm - penalty(C₁Σmax(0,冲突数)) + γ(1-|l(t)-l̄(t)|²/R_n)
4. 建模假设: 全频复用；功率均分P/K(不可调)；自由空间+天线增益(无衰落)；复合泊松业务；ITU-R S.1528/S.465-6天线方向图
5. 网络架构: QPLEX双Q网络(隐藏d维,GELU)+CLA注意力(W_q,W_k投影,1/√d缩放)+CRO启发式优化器。Soft update β_soft
6. 适配性分析: 适配—BH MDP建模和分层架构可参考；不适配—QPLEX非GNN，无空间关系建模；改进—保留分层框架，GNN替代QPLEX做波束调度层骨干
7. 信道模型: 自由空间+ITU-R S.1528发射+ITU-R S.465-6接收。Shannon容量。h=550km, Walker-Delta

---

### [L04] Multi-Satellite Coordinated BH for Interference Mitigation: Graph-Theoretic Approach
- DOI/来源: 10.1109/LWC.2026.3676112
- 发表状态: 正式发表
- 发表渠道: IEEE WCL (SCI Q1), 2026
- 年份/会议: 2026, IEEE WCL
- 核心贡献: 揭示倾斜波束干扰足迹不规则性，将多星BH调度建模为动态图着色问题（图拓扑和顶点着色都是优化变量）。两阶段MCMF-TS-GC算法：最小费用最大流获取初始SCA，禁忌搜索+图着色联合优化SCA和BHSA。
- 方法概述: 纯图论+启发式，不使用NN。干扰图基于精确倾斜波束足迹，HEAD算法求解图着色。外层单调可行性测试提升干扰门限。
- 实验设置: 10800星mega LEO(510km+980km双高度), 148/928小区, 8/32波束, fc=2GHz, B=30MHz, Pb=50W, BH周期T=13~29 slots
- 使用的 Baseline 方法:
  - WMIS: 加权最大独立集 [8]
  - Greedy: 最小化激活波束数 [11]
  - NITB: 忽略倾斜波束干扰的MCMF-TS-GC
  - Gurobi: 商业求解器上界
- 关键结论: T=19时满足Case 1几乎所有小区(>16dB SINR)；接近Gurobi上界；倾斜波束建模关键(优于NITB)
- 与本研究关系: 直接相关 — 图论BH方法是与GNN BH最接近的非NN基线，干扰图构建方式可被GNN增强
- 实现关键细节: 干扰指示器J(s,c,i)基于门限I_thr；MCMF margin ΔL=30；TS N_n=20邻域, N_it=10迭代；等功率50W
- 开源代码: 无
- 验证状态: 已验证

**结构化提取：**

1-3. 非RL方法。优化变量为BH模式矩阵X∈ℕ^(C×T)，目标max min SINR
4. 建模假设: 全频复用；等功率；全向接收G_r=1；DFT波束赋形；晴空无雨衰
5. 网络架构: 不使用NN。MCMF(Edmonds-Karp)+TS+HEAD图着色
6. 适配性分析: 适配—干扰图G_c(s)构建可直接用于GNN图定义；动态图着色→GNN节点分类；不适配—无学习能力需每次重解；改进—GNN替代HEAD实现端到端学习
7. 信道模型: 自由空间+UPA增益+DFT波束赋形。fc=2GHz, B=30MHz, 3GPP TR 38.821

---

### [L05] Demand-Aware BH and Power Allocation in DT Empowered LEO
- DOI/来源: 10.1109/TWC.2025.3545745
- 发表状态: 正式发表
- 发表渠道: IEEE TWC (SCI Q1), Vol. 24, No. 6, 2025
- 年份/会议: 2025, IEEE TWC
- 核心贡献: DT赋能的两层RL框架：DT层MA3C做多星BH决策(A3C异步训练)+LSTM预测需求；LEO层MADDPG做多波束功率分配。吞吐量比RBH-FP提升96.7%。
- 方法概述: BH子问题(P1): MA3C选择每星K个小区照射；PA子问题(P2): MADDPG分配K个波束功率。集中训练分散执行。
- 实验设置: Ka 20GHz, 780km, 12星×4波束, 19小区/星共168小区, B=100MHz, P_tot=39dBW, P_max=30dBW, 小区半径39km, 时隙2ms, BHTP=64×T_slot
- 使用的 Baseline 方法:
  - RBH-FP: 随机BH+等功率
  - RBH-DP: 随机BH+按需求比例功率
  - FPA: 负载均衡BH+固定功率
  - DPA: DT辅助BH+离散化功率联合
- 关键结论: BH层负载差异最小82.13Mbps；总吞吐量比RBH-FP +96.7%，比FPA +10.2%；1200 episodes收敛
- 与本研究关系: baseline候选 — MA3C+MADDPG框架可参考，但干扰建模粗糙(仅距离约束C5+惩罚Γ)，GNN可改进
- 实现关键细节: BH层奖励含干扰惩罚Γ；α=β=0.5；MADDPG探索噪声N₀=0.2；soft update τ=0.001；干扰距离约束ω≥ϖ
- 开源代码: 无
- 验证状态: 已验证(arXiv 2411.08896与正式版一致)

**结构化提取：**

1. 状态空间: BH层全局s^t=[vec(D̂^t);vec(H^t)]维度2NC，局部o_n^t=[D_n^t;H_n^t]维度2C；PA层s^t=(D̄_n^t,H̄_n^t)维度2K
2. 动作空间: BH层—离散x_{n,c}∈{0,1}，Σx=K=4；PA层—连续p∈[0,P_max]，Σp≤P_tot
3. 奖励函数: BH层R^t=-[α(maxL-minL)/Q_max+(1-α)(maxτ-minτ)/J_max+Γ]，PA层R^t=βΣTh/Th_max-(1-β)(maxτ-minτ)/J_max，α=β=0.5
4. 建模假设: 全频复用(星内+星间干扰)；3GPP TR 38.811天线方向图；晴空无雨衰；每小区每slot最多一颗星服务
5. 网络架构: BH层Actor(C维softmax,2×128FC)+Critic(标量V,2×256FC)；PA层Actor(K维连续+OU噪声,2×128)+Critic(2×256,输入所有agent)。Adam lr=1e-5/1e-4
6. 适配性分析: 适配—多星多波束BH+PA框架和LSTM预测可参考；不适配—干扰建模粗糙无图结构，K=4波束规模小；改进—GNN替代Actor显式建模干扰图
7. 信道模型: 自由空间+3GPP TR 38.811天线方向图。Ka 20GHz, h=780km, B=100MHz

---

### [L06] Learning Wideband User Scheduling and Hybrid Precoding with GNN
- DOI/来源: arXiv 2503.04233
- 发表状态: 预印本
- 发表渠道: arXiv preprint, 2025
- 年份/会议: 2025, arXiv
- 核心贡献: 提出三层超边图构建(RB-天线-用户)和4种邻域聚合+注意力机制的3D-GNN，用于联合用户调度+混合预编码。SPSD理论指导GNN表达力设计。SoftTop实现可微离散选择。
- 方法概述: 将调度问题建模为超图上的节点选择问题。3D-GNN在RB-天线-用户三元组上做消息传递，输出调度概率+预编码矩阵。端到端监督训练。
- 实验设置: MISO下行, N_t=64天线, K=20用户, F=4RB, SPSD-guided架构设计
- 使用的 Baseline 方法: WMMSE, random scheduling等
- 关键结论: GNN调度接近最优(与WMMSE差距<5%)；可泛化到不同用户数；SPSD理论保证表达力
- 与本研究关系: 方法可借鉴 — 3D超边图构建和SoftTop可微离散选择可迁移到BH pattern设计。**有开源代码**
- 实现关键细节: 3D超边图(RB×天线×用户)；4种邻域聚合+注意力；SoftTop可微top-k选择
- 开源代码: **有（论文附带）**
- 验证状态: 已验证

**适配性分析:** 适配—3D超边图构建和SPSD理论可迁移，将RB维度替换为BH时隙；SoftTop替代argmax实现可微BH pattern选择；改进—将用户替换为小区，在天线维度建模波束间干扰

---

### [L07] Joint Beam Scheduling and Power Optimization for BH LEO (势博弈)
- DOI/来源: 10.23919/JCC.ja.2022-0864 / arXiv:2312.01292
- 发表状态: 正式发表
- 发表渠道: China Communications (SCI Q2), 2023
- 年份/会议: 2023, China Commun.
- 核心贡献: 势博弈+内点法联合BH调度+功率优化，+45%吞吐量。将BH建模为势博弈证明纳什均衡存在，内点法求解功率分配。
- 方法概述: BH调度用势博弈(每颗星独立决策，博弈收敛到NE)，功率分配用内点法。两层交替优化。
- 实验设置: Ka 20GHz, 508km, 61波束, B=200MHz, 小区半径25km, 用户均匀/非均匀分布
- 使用的 Baseline 方法: EPA, 等时间分配, greedy等
- 关键结论: 势博弈+内点法比贪心+45%吞吐量；Bessel天线方向图精确建模CCI
- 与本研究关系: baseline候选 — 传统优化方法作为非ML基线对比。仿真参数详细可参考
- 实现关键细节: Bessel函数天线方向图；SOD(Stackelberg-Orthogonal-Descent)代价函数；CCI同信道干扰精确建模
- 开源代码: 无
- 验证状态: 已验证

**信道模型:** 自由空间+Bessel天线方向图(A_max=48.7dBi, θ_3dB=1.4°)。Ka 20GHz, h=508km, 61波束, B=200MHz

---

### [L08] Multi-Satellite BH and Power Allocation Using DRL (Xie PPO)
- DOI/来源: arXiv 2501.02309
- 发表状态: 预印本
- 发表渠道: arXiv preprint, 2025
- 年份/会议: 2025, arXiv
- 核心贡献: PPO混合离散-连续动作空间做多星BH+功率分配。5颗LEO卫星×161小区，Ku频段。扁平MLP处理966维状态空间。
- 方法概述: 单agent PPO，动作空间为混合(离散BH模式+连续功率)。全连接MLP策略网络。
- 实验设置: 5星, 161小区, Ku频段, 多种流量分布
- 使用的 Baseline 方法: greedy, random等
- 关键结论: PPO在多种流量分布下优于贪心；但扁平MLP无法捕获空间干扰耦合
- 与本研究关系: 直接相关 — 最直接的对比baseline。扁平MLP→GNN正是本研究切入点
- 实现关键细节: 966维状态空间(全连接MLP)；混合动作空间(离散+连续)；PPO算法
- 开源代码: 无
- 验证状态: 已验证

**适配性分析:** 适配—仿真环境和MDP建模可直接参考；不适配—扁平MLP无空间关系建模；改进—GNN替代MLP编码器，在966维状态上建立波束间图结构

---

## 综合分析

### 1. 现有方法分类

**A. DRL-based BH调度 (核心竞品)**
- QPLEX分层MADRL [L03]: 值分解，4ms实时，但不建模空间关系
- MA3C+MADDPG [L05]: DT+两层RL，LSTM预测需求，干扰建模粗糙
- PPO混合动作 [L08]: 扁平MLP，966维状态空间，无图结构
- (Lin TWC 2024 QMIX: 值分解多星BH，未获取)

**B. 图论/优化方法 (传统基线)**
- 动态图着色 [L04]: 精确干扰足迹建模，但无学习能力需每次重解
- 势博弈+内点法 [L07]: 理论保证NE存在，+45%吞吐量，但计算复杂度高

**C. GNN方法 (方法借鉴，非BH)**
- GNN+元学习功率分配 [L01]: 图构建+领域知识聚合函数，zero-shot泛化
- 动态超图NN [L02]: 超边建模many-to-many干扰，GRU时序演化
- 3D-GNN调度 [L06]: 三层超边图+SoftTop可微选择，SPSD理论，**有开源代码**

### 2. 已知局限

| 方法类型 | 共同局限 | 来源 |
|---------|---------|------|
| DRL扁平MLP | 不建模波束间空间干扰耦合，大规模时性能差 | L03/L08 conclusion |
| Q-learning系(QPLEX/QMIX) | 值函数方法不适合直接嵌入GNN，连续动作空间需额外处理 | L03 分析 |
| 传统优化(势博弈/图着色) | 计算复杂度高，无泛化能力，需每个快照重解 | L04/L07 |
| 现有方法普遍 | 干扰建模粗糙(距离约束或惩罚项)，未精确利用波束空间拓扑 | L03-L05 |
| 全频复用假设 | 所有波束共享频率，干扰最严重，但多数论文采用此假设 | 全部 |

### 3. 2-3年趋势

- **2023**: 传统优化为主(势博弈[Zheng])，DRL初入BH(PPO/MADRL)
- **2024**: DRL成为主流(QMIX[Lin], MAPPO)，开始探索多星协调
- **2025-2026**: 分层MADRL成热点[QPLEX, MA3C]；GNN开始进入卫星通信(功率分配[Geng]，信道分配[Zhang])；**GNN for BH = 零篇**
- 预测：GNN+BH是2026-2027的明确空白，结合超图/动态图着色的图结构+GNN学习是自然演进方向

### 4. 研究背景概述

**领域脉络:**
- BH问题起源于HTS(高通量卫星)时代，传统方法为固定pattern或贪心调度
- 2020s DRL引入后快速发展：PPO→MAPPO→MADRL→分层MADRL
- 2024-2025 GNN在卫星通信(功率分配、信道分配、路由)取得突破，但**尚未应用于BH调度**

**核心技术挑战:**
1. 多波束空间干扰耦合的精确建模（现有DRL方法均忽略）
2. BH pattern设计的混合动作空间（离散时隙分配+连续功率）
3. 大规模场景可扩展性（波束数从4到61+）

**本研究定位:**
- 在L03(L04图论方法)和L01/L02(GNN方法)之间架桥
- 用GNN替代扁平MLP(QPLEX/PPO)编码波束间空间关系
- 图构建借鉴L01(节点=波束/边=干扰)或L02(超边=同频干扰组)或L04(精确干扰足迹)
- 分层框架参考L03(上层关联+下层调度)
