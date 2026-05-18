# 文献调研记录

## 调研概况
- **研究方向**：GNN 双层图匹配 + SFC 依赖链约束的虚拟网络嵌入联合优化
- **检索工具**：Semantic Scholar, OpenAlex, arXiv, SerpAPI, Exa, Tavily
- **检索关键词**：GNN+VNE, GNN+SFC, GNN+NFV, DRL+VNE, virtual network embedding+size generalization, cross-scale VNE, GNN+DRL+NFV, SFC placement+DRL
- **核心文献数**：13 篇精读 + 11 篇浅读
- **调研日期**：2026-05-18

## 步骤进度

| Step | 状态 | 完成日期 | Commit | 备注 |
|------|------|----------|--------|------|
| 1 检索 | ✅ | 2026-05-18 | | 复用方向侦察搜索结果，25+搜索文件 |
| 2 获取 | ✅ | 2026-05-18 | | 17篇获取成功，0失败 |
| 3 精读 | ✅ | 2026-05-18 | | 9篇精读（含1篇综述）|
| 3.5 补充 | ✅ | 2026-05-18 | | Round 1 收敛，8篇新论文(4精读+4浅读) |
| 4a 可行性 | ⬜ | | | A0/A'/A/B已通过，D(MVE)待做 |
| 5 Baseline | ⬜ | | | |
| 4b 仿真可行性 | ⬜ | | | |
| 6 仿真器 | ⬜ | | | |
| 7 验证 | ⬜ | | | |

## 综合分析

### 现有方法分类

**1. 传统启发式 VNE（2008-2016）**
D-VINE/R-VINE (Chowdhury 2012) 开创 MIP 两阶段协调方法；GRC (Gong 2014) 全局资源容量节点排序+贪心；NeuroViNE (Blenk 2018) Hopfield 网络缩小搜索空间。性能有上限但速度快，作为 DRL baseline 仍被广泛使用。

**2. DRL + MLP/CNN VNE（2017-2020）**
早期 DRL 方法（DDQN-VNFPA、REINFORCE-CNN）用 MLP/CNN 编码网络状态，依赖人工特征工程。拓扑变化时性能崩溃（L02: DDQN-VNFPA 删节点后拒绝率从 0.35% 飙升），是 GNN 替代的核心动机。

**3. GNN + DRL VNE（2020-至今，主流范式）**
GNN 编码图拓扑 + DRL 做决策。代表：(a) GCN+A2C (L09, Rkhami ISNCC 2020)；(b) GCN+A3C (DVNE-GCN, L06)；(c) GAT+Seq2seq+PPO (HRL-ACRA, L04)；(d) DualGAT+PPO (Virne, L01)。GNN 在大规模网络上系统性优于 MLP/CNN（L01: DualGAT 在 BRAIN 161 节点上 RAC=78.1% > MLP）。

**4. 分层/层次化 RL VNE（2022-2024）**
解决 VNE 稀疏奖励问题。HRL-ACRA (L04) 上层 admission control + 下层 resource allocation；HRLOrch (L05) 下层单请求优化 + 上层全局协调。分层训练（先训下层再训上层）是共性范式。

**5. GNN 加速 VNE（2020）**
GraphViNE (L08) 用 ARVGA 聚类缩小搜索空间，GPU 并行加速 8-20x。GNN 不直接做决策，而是辅助启发式。与端到端 DRL 范式正交。

**6. Size Generalization（2020-至今，方法论层）**
SizeShiftReg (L03) 揭示 d-pattern 偏移是 GNN size generalization 失败的根因。当前 VNE 领域仅有初步尝试（L01 Virne 包含跨拓扑泛化评估），GNN×VNE×cross-scale 精确交叉仍为空白。

### 已知局限

1. **GNN 消融缺乏深度**：多数论文仅对比 GNN vs MLP，未分析 GNN 架构选择（层数、聚合方式）对 VNE 性能的影响
2. **规模验证不足**：L09 仅 24 节点，L06 仅 100 节点，L08 测到 1500 但用随机图。真实场景（数千节点）缺乏验证
3. **静态拓扑假设**：除 L06 的动态 VNE 外，多数假设 substrate 拓扑不变。LEO 卫星时变拓扑未被覆盖
4. **链路编码缺失**：L09 无边特征，L06 仅 fitness matrix，链路带宽/延迟未显式编码进 GNN
5. **SFC 依赖链约束处理粗粒度**：VNE 论文将 SFC 简化为 VNR（连接图），未显式建模 VNF 功能顺序约束
6. **GraphVNE 的图匹配不充分**：GraphVNE (2026) 用 IPFP 做软匹配但只提取行列和标量分数，匹配矩阵本身被丢弃；IPFP 不可微，链路映射非端到端；不处理 SFC 依赖链约束和跨规模泛化

### 2-3 年趋势

1. **DualGAT/DualGCN 成为主流架构**：Virne (L01) 证明 DualGAT（substrate+VNR 双图注意力）在大规模网络上最优，优于单图 GCN/GAT
2. **分层 RL 成熟**：HRL-ACRA (L04) 证明 admission control + resource allocation 分层架构比端到端单层 RL 效果好 10-27%
3. **仿真标准化**：Virne (ICLR 2026) 提供 Gym-style 标准化环境，VNE 领域正从"各自搭仿真"走向统一基准
4. **跨域/跨规模泛化受关注但未解决**：综述 (L07) 将"泛化与鲁棒性"列为开放问题 #3，GPG-VNE (2025) 从预训练角度尝试但未验证跨规模
5. **卫星 VNE 开始出现**：综述提及 STIN VNE 作为 6G 方向，但仅 1-2 篇论文且方法初级
6. **Graph matching 进入 VNE**：GraphVNE (2026, IoTJ) 首次引入可学习 graph matching module for VNE，但仅作为特征增强而非 assignment-based matching

### 研究背景概述

**VNE 领域发展脉络**：
- 2008-2012：问题定义与 MIP 建模（Rethinking VNE, D-VINE/R-VINE）
- 2013-2017：启发式成熟期（GRC, NeuroViNE, GA-PSO 等元启发式）
- 2018-2020：DRL 引入，MLP/CNN 编码（DDQN-VNFPA, A3C-GCN）
- 2020-2022：GNN 成为标配，GCN/GAT 替代 MLP/CNN（L06 DVNE-GCN, L09 GCN+A2C）
- 2022-2024：分层 RL 解决稀疏奖励（L04 HRL-ACRA, L05 HRLOrch）
- 2025-2026：标准化基准（Virne ICLR 2026）+ 规模泛化方法论（SizeShiftReg）

**核心技术挑战**：
1. NP-hard 组合优化：VNE 含节点映射 + 链路映射，搜索空间指数级
2. 稀疏奖励：episode 级奖励导致训练困难，需中间奖励/分层架构
3. 跨拓扑泛化：不同规模/结构的 substrate 网络间迁移能力差
4. SFC 约束：VNF 功能链序依赖增加了约束维度

**本研究定位**：在 GNN+DRL VNE 主流范式下，通过 Node-Edge 联合嵌入（matching-style）建模双层图匹配 + SFC 依赖链约束，填补"GNN×VNE×cross-scale"精确交叉空白。

## 文献条目

### [L01] Virne: A Comprehensive Benchmark for RL-based Network Resource Allocation in NFV
- **DOI/来源**：arXiv 2507.19234v2
- **发表状态**：预印本（投稿 ICLR 2026）
- **发表渠道**：ICLR 2026（AI 顶级会议）
- **年份/会议**：2025 / ICLR
- **核心贡献**：Virne 是目前最全面的 NFV-RA 基准框架。提供 gym-style 仿真环境，支持 cloud/edge/5G 等场景；集成 30+ 算法（含 10+ 非 RL），覆盖 PG/A3C/PPO/MCTS 等训练方法与 MLP/CNN/GCN/GAT/DualGAT/HeteroGAT 等策略架构；设计多维度评估协议（可解性/泛化性/可扩展性）。
- **方法概述**：事件驱动仿真，NFV-RA 建模为序贯 MDP（逐步选物理节点放虚拟节点）。统一管线 6 模块：instance-level environment、reward function、feature constructor、neural policy、experience memory、training method。支持 Constrained MDP 和 Multi-task MDP。
- **实验设置**：WX100(Waxman 100节点)、GEANT(23节点)、BRAIN(161节点)；节点/链路资源 U(50,100)；VN规模 U(2,10)，需求节点U(0,20)带宽U(0,50)，连接概率50%；到达率 Poisson；默认 PPO + DualGAT + fixed=0.1 中间奖励 + (S,T) features + action masking
- **使用的 Baseline 方法**：
  - PPO-MLP/CNN/ATT/GCN/GAT/GCN&S2S/GAT&S2S/DualGCN/DualGAT/HeteroGAT: 不同策略架构
  - MCTS: 蒙特卡洛树搜索
  - NRM, GRC, RW-MaxMatch, Neural-RW 等 10+ 传统启发式
- **关键结论**：(1) PPO-DualGAT 在 WX100 RAC=78.1% 最优；(2) fixed=0.1 中间奖励 > 自适应 > 无中间奖励；(3) GNN 策略在大规模网络优于 MLP/CNN；(4) PPO 效率远优于 A3C/PG
- **与本研究关系**：直接相关 — VNE 核心基准框架，直接用于实验对比和 MVE
- **实现关键细节**：评估指标 RAC(接受率)/LRC(收益成本比)/LAR(长期平均收益)/AST(求解时间)；优化目标 max R2C(S) = (x*REV(S))/COST(S)；MDP state=VN+PN嵌入, action=物理节点集, link mapping=最短路径；最佳配置 PPO+DualGAT+[fixed,0.1]+(S,T)+action_masking
- **适配性分析**：
  - 适配点：(1) Gym API 可直接对接自定义 RL 算法；(2) 内置 DualGAT 等策略作为对比基准
  - 不适配点：(1) 静态图，不支持时变拓扑；(2) 无 SFC 依赖链约束
  - 改进方向：在 Virne 框架上扩展 LEO 拓扑生成器 + SFC 约束模块
- **开源代码**：有 — https://github.com/GeminiLight/Virne
- **验证状态**：已通过学术搜索工具验证
- **实验完备性**：
  - **声称清单**：C1=提供最全面NFV-RA基准框架(30+算法)，C2=PPO+DualGAT最优配置组合，C3=fixed=0.1中间奖励效果最好，C4=GNN在大规模网络系统性优于MLP/CNN
  - **声称 scope**：bounded（特定拓扑和算法范围内验证）
  - **统计规范性**：seeds=未声明 | error bar=无 | 统计检验=无 | 运行次数=30 epochs训练+10测试
  - **Baseline 矩阵**：数量=18 | 类型=DRL(5)+元启发式(5)+传统启发式(8)+精确方法 | 来源声明=有 | 公平调参=部分（统一框架内对比）
  - **消融设计**：对象=参数扫描(reward类型/feature组合) | 方式=替换
  - **信道模型**：不适用（VNE/NFV-RA，非无线通信）
  - **拓扑多样性**：多配置（WX100 100节点/GEANT 23节点/BRAIN 161节点/WX500 500节点+异构资源/时延感知场景）
  - **复杂度报告**：有（求解时间对比+可扩展性分析）
  - **VVUQ**：V=2, V'=3, U=1

### [L02] Combining Deep Reinforcement Learning With Graph Neural Networks for Optimal VNF Placement (DeepOpt)
- **DOI/来源**：10.1109/LCOMM.2020.3025298
- **发表状态**：正式发表
- **发表渠道**：IEEE Communications Letters（SCI Q2，通信短文顶刊）
- **年份/会议**：2021 年 1 月
- **核心贡献**：首次将 Graph Network(GN) 与 DRL(REINFORCE) 结合解决 VNF 放置。DeepOpt 框架在 SDN 网络用 GNN 处理拓扑信息。相比 MLP 方案(DDQN-VNFPA)，GNN 在拓扑变化时显著泛化优势。拒绝率 0.22% vs DDQN-VNFPA 0.35%。
- **方法概述**：Graph Network 架构，节点属性=处理+存储资源利用率，边属性=带宽利用率+延迟。REINFORCE 策略梯度训练。动作空间为每节点 2 维输出经 softmax 选择。
- **实验设置**：ns3gym + TF 1.12；TOTEM 拓扑(23节点37链路)；Google cluster traces 转 SFC(3 VNF)；训练约5h
- **使用的 Baseline 方法**：
  - DDQN-VNFPA: DRL+前馈网络，网络分区缓解动作空间
  - MSGAS: 基于可访问范围的启发式搜索
  - Eigendecomposition: 矩阵特征分解匹配
- **关键结论**：(1) 拓扑变化时 DeepOpt 稳定，DDQN-VNFPA 大幅下降；(2) GNN 拓扑泛化是关键优势；(3) 计算时间为 MSGAS 的 2.1%
- **与本研究关系**：方法可借鉴 — GNN+DRL 用于网络资源优化的早期代表，验证 GNN>MLP
- **实现关键细节**：状态=(处理利用率比, 存储利用率比)+3空位；边=(带宽利用率, 延迟)；奖励 r=-Cost(psi)-penalty-beta*sum(delay(f))；GNN 2个更新函数(phi_e, phi_v)+1个聚合函数(rho_e->v)；REINFORCE max sum(gamma^t*r_t)
- **适配性分析**：
  - 适配点：(1) GNN 处理图拓扑的范式可迁移；(2) 拓扑变化鲁棒性实验值得参考
  - 不适配点：(1) 规模极小(23节点)；(2) REINFORCE 效率低；(3) 无开源代码
  - 改进方向：GN→GAT/DualGAT，配合 PPO 训练
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L03] From Local Structures to Size Generalization in Graph Neural Networks (SizeShiftReg)
- **DOI/来源**：arXiv 2010.08853
- **发表状态**：正式发表
- **发表渠道**：NeurIPS 2020（AI 顶级会议）
- **年份/会议**：2020 / NeurIPS
- **核心贡献**：揭示 GNN size generalization 失败根因为 d-pattern 分布偏移。证明 d 层 GNN 输出在相同 d-pattern 节点上恒定(Thm 2)，可为任意 d-pattern 独立设定输出值(Thm 3)，训练/测试分布存在未见 d-pattern 时存在坏全局最小点(Thm 4-5)。提出 pattern-tree SSL 方法，高 TV 数据集平均提升 5.4%。
- **方法概述**：定义 d-pattern 刻画 GNN 表达力边界。理论+实证双重分析。在合成(G(n,p), PA)和真实(7数据集)数据上验证。提出 pattern-tree SSL pretext task 对齐源/目标域 d-pattern 表示。
- **实验设置**：合成 G(n,p) 训练 n∈[40,50] p=0.3 测试 n=100 p=0.05~0.5；真实数据按大小划分 50%最小训练/10%最大测试；GNN 1-3层 宽度32/64 Adam lr=1e-3 wd=0.1 10 seeds
- **使用的 Baseline 方法**：
  - Vanilla: 标准训练
  - GAE: 图自编码器 SSL
  - NM: 节点掩码 SSL(10%)
  - NML: 节点度量学习
  - CL: 对比学习(边扰动5%)
- **关键结论**：(1) GNN 系统性失败于 size generalization；(2) 更深网络泛化更差(3层>2层>1层)；(3) np=const 时泛化改善验证 d-pattern 假说；(4) 仅1个目标域标注样本即可显著改善
- **与本研究关系**：方法可借鉴 — size generalization 理论基础和 SSL 解决方案
- **实现关键细节**：d-pattern递归定义 0-pattern=节点特征, d-pattern=((d-1)-pattern, multiset{邻居(d-1)-pattern})；1-pattern=度；GNN宽度上界 max{(N+1)^d*|C|, 2*sqrt(|P|)}；SSL: d-pattern tree 各层特征直方图计数；Pretraining先训SSL head+GNN再冻GNN训main head
- **适配性分析**：
  - 适配点：(1) LEO 拓扑随轨道参数变化导致度分布偏移属 d-pattern 偏移场景；(2) pattern-tree SSL 可作为 size generalization 增强手段
  - 不适配点：(1) 假设离散节点特征需扩展连续特征；(2) LEO 拓扑非随机图
  - 改进方向：分析 LEO 拓扑在不同卫星数量下的 d-pattern 分布，设计针对性 SSL task
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L04] Joint Admission Control and Resource Allocation of VNE via Hierarchical Deep Reinforcement Learning (HRL-ACRA)
- **DOI/来源**：arXiv 2406.17334
- **发表状态**：正式发表（IEEE TSC 2024）
- **发表渠道**：IEEE Transactions on Services Computing（CCF-B / JCR Q1）
- **年份/会议**：2024
- **核心贡献**：提出分层 RL 框架 HRL-ACRA：上层 admission control(二值决策)+下层 resource allocation(Seq2seq 迭代节点映射)。上层用 average reward method 解决无限时境，下层设计多目标内在奖励(revenue-to-cost ratio+节点负载均衡)缓解稀疏奖励。GAT+initial residual+identity mapping 深 GNN 编码器。
- **方法概述**：上层 agent 观察 VNR+物理网络状态→二值接纳决策；下层 Seq2seq(GNN encoder+GRU decoder+position encoder)逐虚拟节点生成映射，link mapping 最短路径。PPO 训练，先预训练下层再冻住训练上层。
- **实验设置**：Waxman 100节点/500链路，资源 U[50,100]，1000 VNRs，到达率4/100单位，VNR节点U[2,10]，资源U[0,50]，寿命Exp(1000)。GNN 5层/128维，GRU 128维，lr actor=0.001/critic=0.0005，batch=256，gamma=0.99
- **使用的 Baseline 方法**：
  - GRC: 全局资源容量排序+贪心+BFS
  - NRM: 多维资源度量+最短路径
  - PL: 节点邻近感知+路径评估
  - MCTS: 蒙特卡洛搜索树+UCB
  - A3C-GCN: GCN+A3C
  - REINFORCE-CNN: CNN+REINFORCE
  - GAE-BFS: 图自编码器聚类+BFS
- **关键结论**：到达率0.08时 AC_Ratio 比 GRC/A3C-GCN/GAE-BFS 高 18.93%/10.31%/5.33%，LA_Rev 高 26.91%/13.15%/11.88%。GEANT/BRAIN 真实拓扑上同样最优。
- **与本研究关系**：直接相关 — 分层 RL+GNN 的 VNE 方法，admission control 思想可借鉴
- **实现关键细节**：上层奖励=(Rev/Cost)*Rev(成功)或-0.1(接纳失败)或0(拒绝)；下层内在奖励 δ=(1/|Nv|)*(Rev_t/Cost_t+0.01*ψ(at))；beam search 推理；mask 向量过滤不可用节点
- **适配性分析**：
  - 适配点：(1) 分层 RL 解决稀疏奖励范式通用；(2) GNN+Seq2seq VNE 编码方式可复用
  - 不适配点：(1) 传统 VNE 非卫星场景；(2) 在线到达无时间窗口
  - 改进方向：分层架构迁移到 LEO 拓扑，上层加入时间维度
- **开源代码**：有 — https://github.com/GeminiLight/hrl-acra
- **验证状态**：已通过学术搜索工具验证
- **实验完备性**：
  - **声称清单**：C1=HRL-ACRA在acceptance ratio和long-term average revenue上优于SOTA，C2=资源受限场景显著提升性能，C3=可扩展到大规模稀疏拓扑
  - **声称 scope**：bounded（"约18.93%提升"/"26.91%提升"等具体百分比）
  - **统计规范性**：seeds=未明确 | error bar=无 | 统计检验=无 | 运行次数=1000 episodes训练+1000 timesteps测试
  - **Baseline 矩阵**：数量=7 | 类型=经典启发式(GRC/NRM/PL)+DL(MCTS)+DRL(A3C-GCN/REINFORCE-CNN/GAE-BFS) | 来源声明=有 | 公平调参=声称与原始论文一致
  - **消融设计**：对象=逐模块 | 方式=删除/替换（Upper+GRC/Only Lower/Basic Reward/GAT替换/PPO替换）
  - **信道模型**：不适用（VNE问题，非无线通信）
  - **拓扑多样性**：多配置（Waxman随机图100节点/GEANT 40节点/BRAIN 161节点）
  - **复杂度报告**：推理延迟（处理1000 VNRs平均运行时间）
  - **VVUQ**：V=2, V'=3, U=1

### [L05] GNN-Based Hierarchical DRL for NFV Resource Orchestration in Elastic Optical DCIs (HRLOrch)
- **DOI/来源**：10.1109/JLT.2021.3125974
- **发表状态**：正式发表
- **发表渠道**：IEEE Journal of Lightwave Technology（JCR Q1，光通信顶刊）
- **年份/会议**：2022
- **核心贡献**：HRLOrch 用 GNN(GGS-NN+GRU) 编码弹性光数据中心互联(EO-DCI)图结构，分层 DRL：下层最小化单个 vNF-SC 资源消耗，上层协调所有 vNF-SC 最小化阻塞率。下层先训练收敛再训练上层。zero-shot 跨拓扑泛化仅 500 请求即超越启发式。
- **方法概述**：GNN encoder 提取 EO-DCI 特征（节点=可用IT+vNF剩余处理能力，邻接矩阵=最短路径最大可用频隙块），LSTM 记忆已确定 vNF 放置序列，attention decoder 选节点。J 轮 message passing + GRU 聚合。
- **实验设置**：NSFNET(14节点)/USB(24节点)，F=358频隙，DC IT 100单位，5种 vNF(4-8单位)，vNF-SC 2-4 vNF，带宽 U[20,100]Gb/s。GNN hidden=128，lower batch=8，upper batch=20，α=10 β=γ=1
- **使用的 Baseline 方法**：
  - GP-SPR: 贪心+最短路径
  - MRP-SSR: 最大化 vNF 重用+频谱节省路由
  - BP-SPR: 均衡放置+最短路径
  - SRLOrch: 同结构单层 DRL
  - GCN-PNN: GCN 替代 GGS-NN
  - DNN-PNN: DNN 替代 GNN
- **关键结论**：NSFNET 阻塞率收敛至~1.1e-3；USB zero-shot 仅500请求超越启发式；运行时间随规模增长1.32倍(启发式1.65-2.55倍)
- **与本研究关系**：方法可借鉴 — GNN+分层 DRL 组合架构、零样本跨拓扑泛化
- **实现关键细节**：下层奖励 r_k=-α(失败)或 β*ψ_k+γ*φ_k(成功)，ψ=IT消耗 φ=光路跳数；上层 r=1/-1；policy gradient 更新；GGS-NN J轮迭代；邻接矩阵编码频谱可用性
- **适配性分析**：
  - 适配点：(1) 分层训练范式通用；(2) GNN 编码图结构方法可迁移
  - 不适配点：(1) 面向弹性光网络非通用 VNE；(2) vNF-SC 非通用虚拟网络拓扑
  - 改进方向：GNN 编码方式（邻接矩阵带链路带宽）迁移到 LEO VNE
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L06] Dynamic Virtual Network Embedding Algorithm Based on RL and GCN (DVNE-GCN)
- **DOI/来源**：arXiv 2202.02140
- **发表状态**：正式发表（IEEE IoT Journal 2022）
- **发表渠道**：IEEE Internet of Things Journal（JCR Q1，CCR 1）
- **年份/会议**：2022
- **核心贡献**：GCNN+A3C 结合动态 VNE，定义 fitness matrix 追踪物理节点剩余 CPU。GCNN 在谱图理论上做 Fourier 变换提取特征，自动学习拓扑表征。长期平均收入比 NodeRank/MCST-VNE/GCN-VNE 高 38.8%/22.5%/24%。
- **方法概述**：GCNN 利用图 Laplacian 特征向量做 Fourier 变换，K 阶多项式卷积核，softmax 输出物理节点选择概率。A3C 并行训练。Fitness matrix 记录剩余 CPU 指导动态重映射。
- **实验设置**：100节点/600链路，CPU/带宽 U[50,100]，1000 VNRs(Poisson 5/100单位)，虚拟节点 U[2,12]，连接概率0.5，CPU/带宽需求 U[1,50]，寿命指数分布
- **使用的 Baseline 方法**：
  - NodeRank: 随机游走节点排序+BFS
  - MCST-VNE: MCTS+多商品流/最短路径
  - GCN-VNE: DRL+GCNN+多目标奖励
- **关键结论**：长期平均收入比 NodeRank/MCST-VNE/GCN-VNE 高 38.8%/22.5%/24%。动态 fitness value 减少资源碎片化。
- **与本研究关系**：对比 baseline 候选 — 动态 VNE+GCNN 方法
- **实现关键细节**：奖励 r(at)=R(GiV)*(R/C)；fitness matrix F(t)=[f_ij(t)]，f_ij=剩余CPU或∞(不满足)；GCNN 输出经 softmax 得|NP|维概率分布；K阶谱卷积核 g=Σ α_k*λ_v^k*f
- **适配性分析**：
  - 适配点：(1) 动态 VNE 机制适合卫星场景请求变化；(2) GCNN 特征提取思路通用
  - 不适配点：(1) 谱域 GCNN 需计算 Laplacian 特征分解，拓扑变化时重算；(2) 未考虑链路带宽显式编码；(3) 100节点未测试跨拓扑泛化
  - 改进方向：替换谱域 GCNN 为空域 GNN(GAT/GIN)，加入链路特征编码
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L07] AI-Empowered Virtual Network Embedding: A Comprehensive Survey
- **DOI/来源**：10.1109/COMST.2024.3424533
- **发表状态**：正式发表
- **发表渠道**：IEEE Communications Surveys & Tutorials（中科院一区/IF~30，顶刊综述）
- **年份/会议**：2025 (online 2024)
- **核心贡献**：AI-VNE 全面综述，6维分类体系，RL/DRL 算法详尽对比，STIN 展望+9大开放挑战。180+ 引用覆盖 2013-2024 主流 AI-VNE 工作。
- **方法概述**：综述论文。梳理 RL-based(Q-learning/SARSA/MCTS/TD)和 DRL-based(PG/DQN/DDQN/A3C/DDPG/SAC)方法，汇总 GNN/GCN 在 VNE 中的应用。
- **实验设置**：综述论文无自有实验。汇总各论文拓扑(GT-ITM/BtEurope/Internet)和评价指标。
- **使用的 Baseline 方法**：
  - D-VINE: MIP 两阶段协调 MCF
  - GRC: 全局资源容量排序
  - NeuroViNE: Hopfield 网络预处理
  - R-VINE: 随机节点选择
  - First Fit / Best Fit: 贪心
- **关键结论**：(1) VNE 是 NP-hard，DRL+GCN 是主流；(2) 多数仅验证小规模，可扩展性是首要开放问题；(3) STIN VNE 是 6G 方向但方法初级；(4) 泛化与鲁棒性是开放问题 #3
- **与本研究关系**：直接相关 — 领域综述，提供分类体系、baseline 列表、开放方向
- **实现关键细节**：VNE NP-hard 引用[Rost & Schmid, IEEE/ACM ToN 2020]；VNE 通用公式 G=(N,L,A)；指标 embedding cost/revenue, R2C, acceptance rate, utilization, time, delay；VNE 与 SFC 关系：SFC 是 VNE 约束子问题(增加 VNF 功能链序约束)
- **适配性分析**：
  - 适配点：(1) VNE NP-hard 本质与 GNN 表征学习天然适配；(2) 6D 分类体系为问题定位提供框架
  - 不适配点：(1) 未涉及 LEO 卫星场景；(2) GNN 方法占比小未深入消融
  - 改进方向：将 VNE 方法迁移到 LEO 时变拓扑，结合时变特征
- **开源代码**：无（综述）
- **验证状态**：已通过学术搜索工具验证

### [L08] Accelerating Virtual Network Embedding with Graph Neural Networks (GraphViNE)
- **DOI/来源**：10.23919/CNSM50824.2020.9269128
- **发表状态**：正式发表
- **发表渠道**：IFIP/IEEE CNSM 2020
- **年份/会议**：2020
- **核心贡献**：GraphViNE 基于 ARVGA(对抗正则化变分图自编码器)对物理服务器聚类缩小搜索空间。GNN 聚类后 BFS 嵌入。GPU 并行加速 8-20x，acceptance ratio 比 NeuroViNE +20%、FirstFit +100%。
- **方法概述**：2层空间 GNN(GraphSAGE风格)编码器+MLP解码器+对抗判别器→K-means聚类→BFS搜索。聚合函数融合邻居资源+链路带宽权重。
- **实验设置**：100-1500节点 Erdos-Renyi(p=0.4)，VN 4-10节点(p=0.7)，CPU+GPU+RAM 三维资源，到达率2/unit，2000时间单位
- **使用的 Baseline 方法**：
  - FirstFit: 第一个满足资源的节点
  - BestFit: CPU最大节点
  - GRC: 节点排序(单资源)
  - NeuroViNE: Hopfield+GRC
- **关键结论**：(1) GPU 加速 8x 均值/20x 最优，运行时间随规模近乎恒定；(2) R2C: GraphViNE=1.87 > NeuroViNE=1.57 > GRC=1.37；(3) GNN 聚类"引导"而非"排除"
- **与本研究关系**：方法可借鉴 — GNN 聚类加速 VNE 思路
- **实现关键细节**：编码器 2层空间GNN 输入=R(资源维) 输出=16；聚合 W1*x_k-1(n)+sum_m(W2*x_k-1(m)*b(l))；判别器 3层Dense(16-32-16) ReLU；聚类簇数4-6 elbow method；BFS alpha=30节点 beta=3跳；更新阈值 kappa1=10%资源 kappa2=10%带宽
- **适配性分析**：
  - 适配点：(1) GNN 聚类替代启发式预处理可迁移；(2) 空间 GNN 并行化对大规模有价值
  - 不适配点：(1) 静态网络无拓扑时变；(2) GNN 用于聚类非端到端 DRL 决策
  - 改进方向：ARVGA 聚类+时变拓扑更新机制结合
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L09] On the Use of Graph Neural Networks for Virtual Network Embedding
- **DOI/来源**：10.1109/ISNCC49221.2020.9297270
- **发表状态**：正式发表
- **发表渠道**：IEEE ISNCC 2020
- **年份/会议**：2020
- **核心贡献**：VNE 建模为 episodic MDP，端到端 GCN+A2C 框架。三层编码：GCN 节点级→注意力图级→NTN 关系编码。消融表明 64 hidden units 最优。
- **方法概述**：状态=(SN图, VNR图)，节点特征含 CPU/带宽和/放置标志；GCN 3层+tanh；注意力层加权求和得图表示；NTN(K=8)建模 SN-VNR 交互；A2C 训练。
- **实验设置**：BtEurope(24节点37链路)，资源[50,100]；VN Erdos-Renyi 资源[1,10]；30VN/episode, 3000episodes, 5seeds；PyTorch+DGL
- **使用的 Baseline 方法**：
  - Random Agent: 随机+最短路径
  - First Fit: 按序+最短路径
- **关键结论**：(1) GCN+Attention+NTN 显著优于 Random/FirstFit；(2) 64 hidden 最优(128无明显提升)；(3) FirstFit 贪心占带宽导致后续拒绝率高
- **与本研究关系**：方法可借鉴 — GCN+Attention+NTN 三层编码架构、VNE-MDP 建模
- **实现关键细节**：GCN 3层 tanh；SN/GCN/VNR GCN 独立模块；SN节点=(CPU, 带宽和)，VNR节点=(CPU需求, 带宽需求, 当前标志, 已放置标志)；NTN K=8；hidden=64；lr=1e-3 gamma=0.99 Adam
- **适配性分析**：
  - 适配点：(1) GCN+DRL 决策范式直接适用；(2) 注意力基于"当前待放置节点"可迁移
  - 不适配点：(1) 24节点规模小未验证可扩展性；(2) 仅对比 Random/FirstFit 无强 baseline；(3) 无边特征
  - 改进方向：加入边特征(链路带宽/延迟)，扩大规模，增加 GRC/D-VINE 强 baseline
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

### [L10] GraphVNE: Graph-Level Matching for Efficient Virtual Network Embedding in Edge Computing
- **DOI/来源**：10.1109/JIOT.2026.3656629
- **发表状态**：正式发表
- **发表渠道**：IEEE Internet of Things Journal（JCR Q1）
- **年份/会议**：2026
- **核心贡献**：首次将 graph-level matching 引入 VNE 决策，通过 GMM（Graph Matching Module）计算虚拟-物理网络结构兼容性分数。IPFP 求解器生成软匹配矩阵，行列投影为 node-to-graph 分数作为 RL 状态增强。R2C 比最强 baseline FlagVNE 提升 13.1%。
- **方法概述**：三阶段架构。Bilevel Feature Embedding：2层 GCN(node-level) + GMM(graph matching via IPFP) + GPM(mean pooling)。Feature Fusion：0.7 inner-graph + 0.3 cross-graph 权重。Bidirectional Action：先选虚拟节点再选物理节点，PPO 训练。
- **实验设置**：GEANT(40节点61链路), WX100(100节点500链路)；资源归一化0-20/0-50；VNR 2-10节点50%连接；Poisson到达；RTX 4090
- **使用的 Baseline 方法**：FlagVNE(IJCAI 2024), A3C-GCN, DDPG-Attention, NEA-VNE, NRM-VNE, GRC-VNE, RW
- **关键结论**：(1) GMM+GPM互补，小网络GMM更重要大网络GPM更重要；(2) R2C 在 GEANT 提升 13.1% vs FlagVNE；(3) 图匹配作为特征增强有效但不是真正的 assignment
- **与本研究关系**：直接竞品 — graph matching for VNE，但方法本质不同（特征增强 vs assignment-based matching）
- **实现关键细节**：IPFP 最多50轮迭代；affinity matrix 用高斯核；双向选择降动作空间为|NV|+|NP|；奖励 r=φ·(R2C-β·(1-Ψ))，φ=1/|NV|
- **适配性分析**：
  - 适配点：(1) GMM 跨图匹配思路可参考；(2) 双向动作选择降低动作空间复杂度
  - 不适配点：(1) IPFP 不可微，匹配信号被截断；(2) 无 SFC 依赖链约束；(3) 无跨规模泛化；(4) 链路映射非端到端
  - 改进方向：用 attention-based matching 替代 IPFP 实现端到端可微；加入 SFC 依赖链建模
- **开源代码**：无
- **验证状态**：已精读全文验证
- **实验完备性**：
  - **声称清单**：C1=通过图级匹配提升VNE性能(R2C提升13.1%)，C2=高请求密度场景鲁棒性强，C3=支持可扩展边缘服务
  - **声称 scope**：bounded（GEANT/WX100，λ范围0.001-0.006/0.06-0.16）
  - **统计规范性**：seeds=未明确 | error bar=无 | 统计检验=无 | 运行次数=30 epochs训练+10测试，1000 VNRs/epoch
  - **Baseline 矩阵**：数量=7 | 类型=DL(FlagVNE/A3C-GCN/DDPG-Attention)+启发式(NEA-VNE/NRM-VNE/GRC-VNE/RW) | 来源声明=有 | 公平调参=有（lr=0.001，w=0.7统一）
  - **消融设计**：对象=逐模块（GLE/GMM/GPM） | 方式=删除（free变体）
  - **信道模型**：理想化（纯图拓扑，无信道模型）
  - **拓扑多样性**：多配置（GEANT: 40节点61链，WX100: 100节点500链）
  - **复杂度报告**：理论O()（多项式时间，GMM为主导项）
  - **VVUQ**：V=2, V'=2, U=1

### [L11] FlagVNE: Flexible and Generalizable RL Framework for VNE
- **DOI/来源**：arXiv 2404.12633
- **发表状态**：正式发表（IJCAI 2024）
- **发表渠道**：IJCAI（CCF-A，AI 顶级会议）
- **年份/会议**：2024
- **核心贡献**：MAML meta-RL 框架实现跨 VNR size 泛化。不同 VNR size 视为不同 task，meta-policy 学习跨 size 共享初始化，fine-tune 得到 size-specific 子策略。解决了"one-size-fits-all"策略在大 VNR 上的局部最优问题。
- **方法概述**：GCN + residual 编码 VN/PN。Hierarchical decoder：high-level MLP 选虚拟节点(ordering) + low-level MLP 选物理节点(placement)。MAML meta-training + curriculum scheduling。
- **实验设置**：GEANT(40节点), WX100(100节点), WX500(500节点)；VNR 2-10训练，size=12测试(unseen)；资源归一化
- **使用的 Baseline 方法**：A3C-GCN, DDPG-Attention, NEA-VNE, NRM-VNE, GRC-VNE
- **关键结论**：(1) RAC 比A3C-GCN +10.4%，LT-R2C +12.8%；(2) meta-RL 快速适应 unseen VNR size；(3) WX500 大规模验证有效
- **与本研究关系**：间接竞品 — VNE 泛化性方向，但仅跨 VNR size 不跨 PN 拓扑
- **实现关键细节**：VN/PN 分别编码不共享参数不构建跨图连接；泛化仅 VNR size 维度；meta-policy fine-tune 而非 zero-shot
- **适配性分析**：
  - 适配点：(1) meta-RL 训练策略可参考；(2) VNR size 泛化思路可扩展到 PN scale
  - 不适配点：(1) 仅跨 VNR size 不跨 PN；(2) 无 SFC 约束；(3) GCN 编码无跨图交互
  - 改进方向：将 meta-RL 从 VNR size 扩展到 PN scale
- **开源代码**：有
- **验证状态**：已精读全文验证
- **实验完备性**：
  - **声称清单**：C1=双向动作MDP提升搜索空间探索灵活性，C2=层次化解码器确保高效训练，C3=元RL支持多尺寸策略快速适应，C4=课程调度缓解次优收敛，C5=多指标优于SOTA
  - **声称 scope**：bounded（GEANT/WX100，VNR规模2-10，特定到达率范围）
  - **统计规范性**：seeds=未明确 | error bar=无 | 统计检验=无 | 运行次数=20次meta-learning+10次fine-tuning
  - **Baseline 矩阵**：数量=7 | 类型=启发式(NRM-VNE/NEA-VNE/PSO-VNE/MCTS-VNE)+DRL(PG-CNN/A3C-GCN/DDPG-Attention) | 来源声明=有 | 公平调参=未明确
  - **消融设计**：对象=逐模块（5变体：UniActionNEA/MetaFree-Single/MetaFree-Multi/MetaPolicy/NoCurriculum） | 方式=替换/删除
  - **信道模型**：不适用（网络资源分配，非无线通信）
  - **拓扑多样性**：2种拓扑（GEANT: 40节点64链路；WX100: 100节点500链路）
  - **复杂度报告**：推理延迟=有（GEANT 10.08s/WX100 28.21s）
  - **VVUQ**：V=2, V'=2, U=1

### [L12] CONAL: Constraint-Aware Learning for VNE
- **DOI/来源**：arXiv 2410.22999
- **发表状态**：预印本
- **发表渠道**：未知（Virne 团队前作）
- **年份/会议**：2024
- **核心贡献**：Violation-tolerant CMDP + reachability-guided optimization (REACH) + adaptive reachability budget (ARB)。允许约束违反继续构建解以保留梯度，用 HJ reachability 分析确保 state-wise zero violation。
- **方法概述**：三层约束处理：CMDP 允许违规 → REACH 基于 HJ reachability 最大化 reward 同时满足约束 → ARB 用 greedy surrogate 估计可解性动态调整 budget。基于 Virne 基准开发。
- **实验设置**：Virne benchmark (WX100, GEANT, BRAIN)；异构图建模 VN+PN 融合+跨图链接
- **使用的 Baseline 方法**：Virne 内置 baseline
- **关键结论**：(1) 约束违反率显著降低；(2) 可解性差的实例不会导致训练崩溃
- **与本研究关系**：方法可借鉴 — CMDP+reachability 框架可适配 SFC 依赖链约束
- **实现关键细节**：异构图建模(VN+PN融合+cross-graph links)；path-bandwidth contrastive learning (Barlow Twins)；greedy surrogate 估计可解性
- **适配性分析**：
  - 适配点：(1) CMDP 处理约束的思路通用；(2) 异构图跨图建模方式可参考
  - 不适配点：(1) 仅处理标准 VNE 约束(资源/带宽)，不处理 SFC 依赖链；(2) 非卫星场景
  - 改进方向：将 CMDP 框架扩展到 SFC 依赖链约束
- **开源代码**：有 — https://github.com/GeminiLight/conal-vne
- **验证状态**：已精读全文验证
- **实验完备性**：
  - **声称清单**：C1=CONAL实现高可行性和训练稳定性，C2=优于现有启发式和RL方法，C3=有效处理复杂约束和不可解实例，C4=泛化/扩展/实用性强
  - **声称 scope**：混合（有界声明+大规模验证500节点）
  - **统计规范性**：seeds=10（测试时固定0/1111/.../9999） | error bar=有（标准误，mean±SE格式） | 统计检验=无 | 运行次数=每η训练多次，测试10次
  - **Baseline 矩阵**：数量=10 | 类型=经典(3)+启发式(2)+RL/DL(5)+消融(5) | 来源声明=有（官方代码/Virne库/复现） | 公平调参=有
  - **消融设计**：对象=逐模块（HM/PC/REACH/ARB 4个组件） | 方式=删除/替换
  - **信道模型**：不适用（NFV资源分配，非无线通信）
  - **拓扑多样性**：多配置（WX100/WX500/GEANT/BRAIN+变化请求频率/分布）
  - **复杂度报告**：理论 O(|Nv|·K·(|Lp|d + |Np+Nv|d²))，推导见Appendix D.6
  - **VVUQ**：V=3, V'=3, U=2

### [L13] GPG-VNFE: Towards Foundation Models via Graph Pretraining for Generalizable VNF Embedding
- **DOI/来源**：10.23919/CNSM67658.2025.11297510
- **发表状态**：正式发表
- **发表渠道**：IFIP/IEEE CNSM 2025
- **年份/会议**：2025
- **核心贡献**：GraphCL-LP（对比学习+VGAE 生成数据增强策略）预训练 GNN 编码器，下游 GAT+Transformer Actor-Critic 做 one-shot VNF-FG 放置。接受率比 GRC 提升 57.45%。
- **方法概述**：两阶段。预训练：GraphCL-LP 用 VGAE 学习数据增强策略，两个独立 GNN 分别编码物理网络和 VNF-FG。下游：GAT(物理网络)+Transformer(VNF-FG) → Actor-Critic one-shot 放置所有 VNF。
- **实验设置**：Waxman 100节点500链路；VNF-FG 含依赖链；非卫星场景
- **使用的 Baseline 方法**：GRC, GRU-A3C, TDRL-DDPG(前作)
- **关键结论**：(1) 预训练显著提升泛化性；(2) VNF-FG 依赖链通过流守恒约束处理
- **与本研究关系**：方法可借鉴 — VNF-FG 依赖链建模和图预训练思路
- **实现关键细节**：VNF-FG 依赖通过 ILP 流守恒约束建模；两个独立编码器无跨图交互；one-shot 放置非顺序
- **适配性分析**：
  - 适配点：(1) VNF-FG 依赖链建模方式可参考；(2) 图预训练提升泛化性
  - 不适配点：(1) 独立编码器无跨图匹配交互；(2) 非卫星场景
  - 改进方向：加入跨图匹配交互机制
- **开源代码**：无
- **验证状态**：已浅读验证

### [L14] ReViNE: Reinforcement Learning-Based Virtual Network Embedding in Satellite-Terrestrial Networks
- **DOI/来源**：10.1109/TCOMM.2024.3400911
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Communications（JCR Q1）
- **年份/会议**：2024
- **核心贡献**：星地融合网络 VNE+SFC，DQN 选端到端路径，VNF 按顺序映射到路径上剩余资源最多的卫星节点。考虑 ISL 容量和连接持续时间约束。接受率比 TS-MAPSCH 提升 19.95%。
- **方法概述**：每个源-目的对一个独立 DQN。状态=候选路径上最大可用处理资源。动作=源-目的间公共路径集合。奖励综合服务收益、部署成本、链路稳定性和剩余链路容量。
- **实验设置**：Iridium NEXT(75 LEO, 6轨道面, 780km)；1441时隙每时隙1分钟；70地面站
- **使用的 Baseline 方法**：TS-MAPSCH, 固定 VNE
- **关键结论**：(1) 接受率+19.95% vs TS-MAPSCH；(2) VNF 重映射应对拓扑变化有效
- **与本研究关系**：领域竞品 — 卫星 VNE+SFC，但方法偏传统（DQN+手工特征，无 GNN）
- **实现关键细节**：ISL 连通性=二值(可见性+最小仰角+天线重定向)；链路稳定性=剩余持续时间；无 GNN
- **适配性分析**：
  - 适配点：(1) 卫星 VNE+SFC 问题建模完整；(2) ISL 约束建模方式可参考
  - 不适配点：(1) 无 GNN，手工特征；(2) DQN 能力有限；(3) 每源-目的一个 DQN 不可扩展
  - 改进方向：用 GNN 替代手工特征，统一 agent
- **开源代码**：无
- **验证状态**：已浅读验证

### [L15] Service Continuity-Aware SFC Embedding in Satellite Networks: A Scalable DRL Approach
- **DOI/来源**：10.1109/ICC52391.2025.11161746
- **发表状态**：正式发表
- **发表渠道**：IEEE ICC 2025
- **年份/会议**：2025
- **核心贡献**：GNN + DiffPool + PPO 用于 LEO 卫星 SFC 嵌入。提出 RTTM（Remaining Time to Migration）指标引导 agent 选择服务生命周期更长的嵌入方案。SFC 重配置比例减少 60%。
- **方法概述**：两个独立 GNN 分别处理卫星网络图和 SFC 图，DiffPool 降维后拼接为状态表示。PPO Actor-Critic。动作=迷宫式移动(水平/垂直+放置 VNF)。
- **实验设置**：Starlink Phase I-a(1600卫星, 32轨道面)；区域 40N-0N / -135W至-80W；DiffPool 两层各压缩到25%
- **使用的 Baseline 方法**：ILP(仅优化接受率)
- **关键结论**：(1) RTTM 比 ILP 提升约 80%；(2) SFC 重配置减少 60%；(3) 接受率下降不到10%
- **与本研究关系**：直接竞品 — GNN+DRL+SFC in LEO，但无 graph matching，无显式 SFC 依赖链建模
- **实现关键细节**：RTTM = SFC 所有 VNF 所在卫星在 MHP 区域内最短剩余时间；DiffPool 两层降维；SFC 图用标准 GNN 无依赖链约束
- **适配性分析**：
  - 适配点：(1) 卫星 SFC 嵌入场景直接相关；(2) RTTM 指标设计思路可参考
  - 不适配点：(1) 无跨图匹配机制；(2) SFC 图用标准 GNN 无依赖约束嵌入；(3) DiffPool 降维可能丢失结构信息
  - 改进方向：加入 matching-style GNN + SFC 依赖链约束嵌入
- **开源代码**：无
- **验证状态**：已浅读验证

### [L16] DRL-Based Bandwidth-Aware Service Function Chaining (DRL-BSFC)
- **DOI/来源**：10.3390/electronics15010227
- **发表状态**：正式发表
- **发表渠道**：Electronics (MDPI, OA)
- **年份/会议**：2026
- **核心贡献**：Seq2Seq 编码 SFC 排序信息 + GCN 提取物理网络特征 + 改进 A3C。显式建模 SFC 中 VNF 的有序序列。带宽成本显式加入奖励函数，带宽受限场景带宽成本降低约 20.5%。
- **方法概述**：GCN(CPU/RAM/ROM+链路带宽) + Seq2Seq(编码SFC有序序列) + A3C(master-worker并行)。Actor 输出物理节点选择概率。
- **实验设置**：100节点500链路 Waxman；SFC 含 VNF 顺序约束
- **使用的 Baseline 方法**：DRL-SFCP
- **关键结论**：(1) 带宽受限时接受率+4%，R2C+5%；(2) Seq2Seq 有效捕获 SFC 排序但顺序解码误差累积
- **与本研究关系**：方法可借鉴 — SFC 排序的显式建模，但 Seq2Seq 有局限
- **实现关键细节**：部署带宽=虚拟链路带宽×路径跳数；带宽成本=虚拟链路带宽×(跳数-1)；Seq2Seq 编码-解码 VNF 序列
- **适配性分析**：
  - 适配点：(1) SFC 排序显式建模思路值得参考；(2) 带宽成本建模方式
  - 不适配点：(1) Seq2Seq 顺序解码误差累积且无法并行；(2) 非卫星场景；(3) A3C 效率低于 PPO
  - 改进方向：GNN 一次前向传播并行考虑所有 VNF，替代 Seq2Seq
- **开源代码**：无
- **验证状态**：已浅读验证

## Baseline 交叉验证

### Baseline 出现频率统计
| 方法名 | 被几篇使用 | 使用该 baseline 的论文 | 代码状态 | 推荐优先级 |
|--------|-----------|----------------------|---------|-----------|
| GRC | 4 | L04, L07, L08, L01(Virne内置) | Virne 内置 | 1 |
| First Fit | 3 | L07, L08, L09 | 易实现 | 2 |
| NeuroViNE | 2 | L07, L08 | 无代码 | 3 |
| D-VINE | 2 | L07, L01(Virne内置) | Virne 内置 | 4 |
| NRM | 2 | L04, L01(Virne内置) | Virne 内置 | 5 |
| MCTS | 2 | L04, L01(Virne内置) | Virne 内置 | 6 |
| A3C-GCN | 2 | L04, L01(Virne内置) | Virne 内置 | 7 |
| Random Agent | 1 | L09 | 易实现 | 8 |
| FlagVNE | 1 | L11 | 有 | 9 |
| CONAL | 1 | L12 | Virne 内置 | 10 |

### Baseline 候选
| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: GRC | L04, L07, L08 | Virne 内置 | 1 | 4篇论文使用，传统启发式代表，Virne 内置 |
| B2: PPO-DualGAT | L01 | Virne 内置 | 2 | Virne 最优策略，GNN+DRL 当前 SOTA |
| B3: First Fit | L07, L08, L09 | 易实现 | 3 | 最简贪心基线，验证 ML 增量 |
| B4: HRL-ACRA | L04 | GitHub 开源 | 4 | 分层 RL+GNN 直接竞品 |
| B5: DVNE-GCN | L06 | 无代码 | 5 | GCN+DRL 动态 VNE，需自实现 |
| B6: D-VINE | L07, L01 | Virne 内置 | 6 | MIP 传统方法标杆 |
| B7: FlagVNE | L11 | 有 | 7 | MAML meta-RL，跨 VNR size 泛化，IJCAI 2024 |

## 实验完备性对标汇总

> 基于 5 篇核心竞品论文（L01 Virne / L04 HRL-ACRA / L10 GraphVNE / L11 FlagVNE / L12 CONAL）的实验完备性提取。

### VVUQ 评分汇总

| 论文 | V (Verification) | V' (Validation) | U (Uncertainty) | 总分 |
|------|:---:|:---:|:---:|:---:|
| L01 Virne (ICLR 2026) | 2 | 3 | 1 | 6 |
| L04 HRL-ACRA (IEEE TSC) | 2 | 3 | 1 | 6 |
| L10 GraphVNE (IEEE IoTJ) | 2 | 2 | 1 | 5 |
| L11 FlagVNE (IJCAI 2024) | 2 | 2 | 1 | 5 |
| L12 CONAL (预印本) | 3 | 3 | 2 | 8 |
| **平均** | **2.2** | **2.6** | **1.2** | **6.0** |

### 领域实验惯例

1. **统计规范性普遍薄弱**：5 篇中仅 CONAL 报告了 seeds(10) 和 error bar(mean±SE)，其余 4 篇均无。无一篇做统计显著性检验。
2. **消融设计**：逐模块消融已成标配（5/5），但仅 CONAL 做到了严格逐组件+参数扫描（V=3）。
3. **拓扑多样性**：3+ 种拓扑是主流（Virne/HRL-ACRA/CONAL），2 种拓扑（GraphVNE/FlagVNE）偏弱。
4. **Baseline 规模**：平均 10 个 baseline，最少的 GraphVNE/FlagVNE 7 个，最多的 CONAL 10 个。公平调参声明普遍缺失或模糊。
5. **复杂度报告**：3/5 有（推理延迟或理论 O()），2/5 无。
6. **声称 scope 控制**：全部使用 bounded 声称，领域惯例良好。

### 盲点（无一论文做到）

- 无一篇做统计显著性检验
- 无一篇报告 seed 数量的合理性（如基于功效分析）
- 无一篇做 cross-dataset 泛化（跨领域数据集）
- 无一篇做因果分析或机制解释

### 对标基线（Contract 阶段应达到）

- **最低要求**（Tier 1）：≥3 seeds + error bar + 逐模块消融 + ≥3 种拓扑 + 声称 scope 控制
- **竞争力目标**（对标 CONAL）：统计检验 + 4 种拓扑 + 复杂度报告 + 理论分析
