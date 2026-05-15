# 文献调研记录

## 调研概况
- **研究方向**：RIS/IRS 辅助通信中的相移优化，用 DRL 方法
- **检索工具**：tools/search（S2 + SerpAPI + Exa + arXiv + OpenAlex + Firecrawl + Tavily）
- **检索关键词**：
  - "RIS phase shift optimization deep reinforcement learning"
  - "IRS intelligent reflecting surface reinforcement learning beamforming"
  - "reconfigurable intelligent surface DRL resource allocation wireless MIMO"
- **核心文献数**：8 篇精读
- **调研日期**：2026-05-13

## 综合分析

### 现有方法分类

**1. 值函数方法（DQN/DDQN 系列）**
L06 采用 DDQN+GA 混合框架，将大规模 RIS 的离散相移优化建模为列级选择问题，动作空间从 $2^{N}$ 压缩至 $\sqrt{N}+1$，嵌入贪心算法恢复元素级精度。L01 提出 LSTM-DDQN，在 CNN 编码器后插入 LSTM 层捕获时序依赖，配合优先经验回放（PER）优化卫星-空-地网络中的 RIS 相移+UAV 轨迹。F1 设计双 DDQN 结构（PER-TDDQN），分别优化 UAV 轨迹和波束赋形/相移，共享能量效率奖励函数。F7 采用联邦 DRL（AF-DRL），两级 MDP 架构分别用 DDPG 和 DDQN 处理全局轨迹和局部相移/波束赋形。值函数方法的核心优势是天然支持离散动作空间（离散相移），但连续相移需量化处理导致信息损失。

**2. Actor-Critic 方法（DDPG/TD3/SAC）**
L02 使用 DDPG 联合优化 RIS 相移和预编码矩阵，创新点在于基于长期 CSI（角度信息）而非瞬时 CSI 训练，降低信道估计开销。F3 提出 AB-TD3，在标准 TD3 的 Actor 网络中嵌入 8 头 self-attention 建模状态元素间依赖关系，配合 batch normalization 稳定训练，在空中 IRS 场景下显著优于标准 TD3/DDPG。F4 采用 SAC（含自动温度调节）优化 RIS-UAV 中继系统的波束赋形+轨迹+相移，利用最大熵框架提升探索效率。Actor-Critic 方法天然支持连续动作空间，适合连续相移优化，但训练稳定性不如值函数方法。

**3. 混合策略方法（PPO + 离散/连续分离）**
L05 提出 Hybrid PPO（H-PPO），为 Active RIS+CoMP-NOMA 系统设计分离的离散 Actor（UAV 移动）和连续 Actor（相移/放大因子/功率分配），共享 Critic 网络。这是唯一涉及 Active RIS（含放大矩阵优化）的工作，也是唯一使用 PPO 的论文。

**4. 启发式+DRL 混合**
L06 的 DDQN+GA 是唯一将传统优化算法（贪心搜索）嵌入 DRL 执行循环的工作。每步 DDQN 选择待优化的 RIS 列，GA 对该列元素逐一精细优化。这种"粗调+细调"的两阶段思路对大规模 RIS 有重要参考价值。

### 已知局限

1. **完美 CSI 假设**：8 篇论文全部假设完美 CSI 已知（L02 虽用长期 CSI 降低估计频率，但仍假设角度信息完美获取），与实际信道估计误差、反馈延迟和导频开销的现实差距显著。
2. **直连链路忽略**：L06、F3、F4、F1 假设 BS-UE 直连链路完全遮挡，简化了系统模型但降低了实用性。
3. **小规模 RIS 实验**：F4 仅用 9 个 RIS 单元（3×3），F3 用 32-64 个，L06 用 100 个。实际部署的大规模 RIS（数百至千级元素）的动作空间挑战尚未充分探索。
4. **复现性差**：8 篇论文无一开源代码，且普遍缺失关键实现细节——L02 和 F1 未给出网络层数/维度，L05 未给出任何网络架构细节，F3 和 F4 缺少奖励函数中的缩放因子数值。
5. **奖励函数归一化缺失**：L02、L05、F1、F7 的奖励函数未做显式归一化，可能导致 DRL 训练不稳定（domain-comms.md §1.5 已记录此陷阱）。
6. **信道模型简化**：F4 假设纯 LoS 信道（Rician 因子→∞），F7 仅说"随机生成"而未指定衰落模型。

### 2-3 年趋势

1. **DRL 算法升级**：2023 年主流是 DQN/DDQN，2024-2025 年快速转向 TD3、SAC、PPO 等 Actor-Critic 和策略梯度方法，同时对网络架构做增强（attention、LSTM、batch normalization）。
2. **联合优化维度扩展**：从单纯的 RIS 相移优化，扩展到相移+波束赋形+UAV 轨迹+NOMA/RSMA 功率分配的联合优化。但这增加了动作空间维度和训练难度。
3. **Active RIS 崛起**：L05 引入 Active RIS（含放大矩阵），克服了被动 RIS 的乘性衰落效应，是被动 RIS 的重要替代方向。
4. **大规模 RIS 的动作空间压缩**：L06 的列级选择+贪心细化方案，以及 L02 的长期 CSI 减少决策频率方案，是应对大规模 RIS 动作空间爆炸的两条技术路线。
5. **联邦学习引入**：F7 的联邦 DRL 框架支持多 UAV/RIS 分布式协同，是系统级扩展的重要方向。

## 文献条目

### [L01] Deep RL-Based Energy Efficiency Optimization for RIS-Aided Integrated Satellite-Terrestrial Relay Networks
- **DOI/来源**：10.1109/TCOMM.2024.3370618
- **发表状态**：正式发表
- **发表渠道**：IEEE Transactions on Communications (TCOMM, SCI Q1)
- **年份**：2024
- **核心贡献**：(1) 提出 RIS-UAV 辅助星-空-地一体化中继网络（ISATRNs）下行模型，卫星经 FSO→HAP→RIS→IoT 链路传输。(2) 改进 LSTM-DDQN 算法，CNN 编码器后插 LSTM 层捕获时序依赖，配合 PER 加速收敛，联合优化 UAV 轨迹+RIS 相移+波束赋形。
- **方法概述**：MDP 建模，LSTM-DDQN 处理离散动作（相移 11 级增量 + 波束 3 级增量 + UAV 6 方向），PER 按 TD-error 优先采样。
- **实验设置**：GEO 卫星，HAP 20km，UAV 5km，6 个 IoT 设备，RIS 16/32 元素，FSO 1550nm/1280MHz + RF 2GHz/10MHz
- **使用的 Baseline 方法**：
  - RIS-NOMA DDQN: 无 LSTM，传统 DDQN
  - RIS-OMA LSTM-DDQN: 本文算法 + OMA 接入
  - RIS-OMA DDQN: 传统 DDQN + OMA
  - 随机相移: 对照组
- **关键结论**：LSTM-DDQN 约 1200 episodes 收敛，NOMA 优于 OMA，增加 RIS 元素数显著提升 EE
- **与本研究关系**：方法可借鉴
- **实现关键细节**：相移增量 $\Delta\theta_m \in \{-5\pi/10, ..., 5\pi/10\}$ 共 11 级；网络含 CNN encoder + LSTM + FC；Adam 优化器；PER 用 TD-error 优先级 + 重要性采样；$\gamma=0.99$；训练 10000 episodes
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**结构化提取 — 状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|------------|
| UAV 位置 $\mathbf{q}[t]$ | 3D 连续，高度 ≤5km | [NOT_FOUND] |
| HAP-RIS 信道 $\mathbf{h}_{HR}$ | Rician, $K_1$ 因子 | [NOT_FOUND] |
| RIS-IoT 信道 $\mathbf{g}_{RG}$ | Rician, $K_2$ 因子 | [NOT_FOUND] |
| HAP-IoT 直射信道 $\mathbf{G}_k$ | Nakagami-m | [NOT_FOUND] |
| UAV 能耗 $E_{UAV}$ | $E_{UAV} \leq E_{max}$ | [NOT_FOUND] |
| 上一步动作 $a_{t-1}$ | 离散 | [NOT_FOUND] |

**结构化提取 — 动作空间**：
| 类型 | 维度 | 合法动作约束 |
|------|------|-------------|
| 离散（三部分） | 11(M个相移) + 3(K个波束) + 6(UAV方向) | 相移 $|\exp(j\theta_m)|=1$；功率约束；飞行区域约束 |

**结构化提取 — 奖励函数**：
$r^{(t)} = EE = C(\mathbf{q}, \mathbf{w}, \Phi) / (E_{UAV} + \text{others})$，归一化 [NOT_FOUND]，权重 [NOT_FOUND]

**结构化提取 — 网络架构**：
CNN encoder [NOT_FOUND 维度] → LSTM [NOT_FOUND 隐藏单元] → FC → 输出 Q 值；激活 ReLU；Adam；$\gamma=0.99$

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| 卫星→HAP (FSO) | Gamma-Gamma | $(\alpha,\beta)=(2.902,2.51)$；$\lambda_F=1550$nm；$B_F=1280$MHz | Table I, Eq.9-10 |
| HAP→RIS (RF) | Rician | $K_1$ [NOT_FOUND]；$d_{HR}^{-2}$ | Eq.16-17 |
| RIS→IoT (RF) | Rician | $K_2$ [NOT_FOUND] | Eq.18-19 |
| HAP→IoT 直射 | Nakagami-m | $m_k$ [NOT_FOUND] | Eq.11-15 |

---

### [L02] Spectral Efficiency Optimization for RIS-Aided Multiuser MISO System Using DRL
- **DOI/来源**：10.1109/ACCESS.2024.3450578
- **发表状态**：正式发表
- **发表渠道**：IEEE Access (SCI Q2)
- **年份**：2024
- **核心贡献**：(1) 基于长期 CSI（角度信息）而非瞬时 CSI 设计联合波束赋形+相移方案，最大化最小遍历用户速率（max-min fairness）。(2) DDPG 利用 Rician 分布离线生成信道样本训练，长期 CSI 不变期间仅需一次前向传播。
- **方法概述**：DDPG 联合优化预编码 W 和相移 Phi，Actor 输出 W 实虚部+N 个相移角度增量，Critic 估计 Q 值。
- **实验设置**：BS 8 天线，RIS 80 元素（收敛）/变化值（性能），10 用户（收敛）/4 用户（性能），Rician 因子 $\delta=2.2, \varepsilon_k=3.75, \eta_k=2.2$
- **使用的 Baseline 方法**：
  - Instantaneous CSI-based scheme: 传统每 CCTI 估计完整瞬时 CSI 优化
- **关键结论**：长期 CSI 方案的 MAUR 随 N 单调递增，瞬时 CSI 方案先增后减（pilot 开销）；计算复杂度远低
- **与本研究关系**：方法可借鉴 + 对比 baseline 候选
- **实现关键细节**：W 经功率归一化 $\mathbf{W} \leftarrow \sqrt{P_t}\mathbf{W}/\|\mathbf{W}\|_F$；相移角度增量乘 $\pi$；奖励 $\min_k R_k^{(t)}$ 无归一化
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**结构化提取 — 状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|------------|
| 预编码矩阵 W 实虚部 | 功率归一化后 | 实虚分离拼接 |
| 相移 Phi 角度 | $[0, 2\pi]$ | 角度表示 |
| CSI 实虚部 | Rician 生成 | [NOT_FOUND] |

**结构化提取 — 动作空间**：
| 类型 | 维度 | 合法动作约束 |
|------|------|-------------|
| 连续 | $2MK + N$ | W 功率归一化；Phi 角度增量 $\phi_n^a + a_i\pi$ |

**结构化提取 — 奖励函数**：
$r^{(t)} = \min_k R_k^{(t)}$，$R_k^{(t)} = \log_2(1 + \text{SINR}_k)$；归一化 [NOT_FOUND]；无权重

**结构化提取 — 网络架构**：
Actor/Critic 均为 DNN，层数/宽度/激活 [NOT_FOUND]；tanh 输出；软更新率 $\eta$ [NOT_FOUND]

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| BS→RIS | Rician | $\delta=2.2$；$I$ LoS 链路数 | Section II+IV |
| RIS→User | Rician | $\eta_k=2.2$ | Section II+IV |
| BS→User | Rician | $\varepsilon_k=3.75$ | Section II+IV |
| 路径损耗 | 自由空间 | $PL_0=-30$dB，$d_0=1$m，$\alpha$ [NOT_FOUND] | Section IV |

---

### [L05] Deep RL Optimized Intelligent Resource Allocation in Active RIS-Integrated TN-NTN Networks
- **DOI/来源**：arXiv:2501.06482
- **发表状态**：预印本
- **发表渠道**：arXiv preprint
- **年份**：2025
- **核心贡献**：(1) 混合 PPO（H-PPO）同时处理离散动作（UAV 5 方向）和连续动作（RIS 相移、Active RIS 放大因子、NOMA 功率分配）。(2) 双 RIS 系统（地面+UAV 搭载）+ CoMP-NOMA，Active RIS 放大矩阵克服乘性衰落。
- **方法概述**：离散 Actor（softmax）+ 连续 Actor（高斯）独立优化，共享 Critic；Active RIS 相移 $\theta_k \in [-\pi,\pi)$，放大因子 $p_k \in [1, \mathcal{S}]$。
- **实验设置**：3 BS，3 用户，载频 2.4GHz，带宽 10MHz，RIS 元素数 {30,70,120,200}，路径损耗指数 2.2-3.7
- **使用的 Baseline 方法**：
  - H-PPO P-RIS: 同算法，被动 RIS
  - DRL NOMA (w/o fairness): 无公平性
  - DRL NOMA (w/ fairness): 有公平性
  - OMA: 正交多址
- **关键结论**：Active RIS + NOMA + H-PPO 相比 Passive RIS 提升 33% sum rate；Active RIS 能效峰值 11500 bit/J
- **与本研究关系**：方法可借鉴（Active RIS 方向）
- **实现关键细节**：网络架构完全缺失；奖励 $R_{sum} + \xi_{dist}(C/d_{R,U})\zeta - \xi_{OOB}\mathbb{I}(OOB)$，$\xi$ 值 [NOT_FOUND]
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| BS→用户 (NLoS) | Rayleigh | $\beta_n=2.2$ | §II-B |
| BS→RIS (LoS) | Rician | $\kappa$ [NOT_FOUND] | §II-B |
| Active RIS 噪声 | 复高斯 | $\sigma^2$ | §II-C |

---

### [L06] A Heuristic-Integrated DRL Approach for Phase Optimization in Large-Scale RISs
- **DOI/来源**：arXiv:2505.04401
- **发表状态**：预印本
- **发表渠道**：arXiv preprint（Letter 体例，可能投向 IEEE WCL/CL）
- **年份**：2025
- **核心贡献**：(1) DDQN + GA 混合框架，将大规模 RIS 离散相移优化的动作空间从 $2^{NR_\theta}$ 降至 $\sqrt{N}+1$。(2) 每步 DDQN 选择 RIS 列索引后嵌入 GA 对该列元素逐一细化，恢复元素级自由度。
- **方法概述**：DDQN 列级粗调（$T$ 步/episode，每步选一列增量调整），GA 对选中列内元素遍历离散相移值保留最优；累积动作完成全 RIS 配置。
- **实验设置**：室内 8m×8m×6m，RIS 10×10=100 元素，1-bit（$\{0,\pi\}$），FBS 4 天线，2 用户，载频 5.25GHz，$P_{max}=25$dBm，$\sigma^2=-94$dBm
- **使用的 Baseline 方法**：
  - Flat: $\Theta=\mathbf{0}$
  - Random: 随机相移
  - DQN [3]: 传统 DQN，动作空间 $2^{\sqrt{N}}$
  - DDQN [8]: 传统 DDQN，动作空间 $2^{\sqrt{N}}$
  - PSO [17]: 粒子群优化+量化
- **关键结论**：DDQN-GA 比纯 DDQN 高 30%，比 DQN 高 24%；PSO 量化后严重退化；可扩展至 50×50 RIS
- **与本研究关系**：**直接相关** + 对比 baseline 候选
- **实现关键细节**：动作空间 $\sqrt{N}+1$（如 $N=100$ 则 11）；奖励 $r_t = \omega \cdot \mathcal{R}_{sum}(\Phi_t)$（$\omega=2$ 用于最终步）；网络 512→256→128→$\sqrt{N}+1$；$\epsilon$ 从 1 衰减至 0.001（率 0.0001）；DDQN lr=1e-3，DDQN-GA lr=5e-4
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**结构化提取 — 状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|------------|
| $\Re(\mathbf{G})$ FBS-RIS 信道实部 | $\mathbb{R}^{N \times M}$ | [NOT_FOUND] |
| $\Re(\mathbf{H})$ RIS-Users 信道实部 | $\mathbb{R}^{N \times K}$ | [NOT_FOUND] |
| $\Im(\mathbf{G})$, $\Im(\mathbf{H})$ | 同上 | [NOT_FOUND] |
| $\Theta_{t-1}$ 上一步相移 | $\{0, 180\}$ (1-bit) | [NOT_FOUND] |
| $\Theta'_{t-1}$ GA 细化后相移（DDQN-GA） | $\{0, 180\}$ | [NOT_FOUND] |

**结构化提取 — 动作空间**：
| 类型 | 维度 | 合法动作约束 |
|------|------|-------------|
| 离散 | $a_t \in \{0, 1, ..., \sqrt{N}\}$ | $a_t=0$ 不变；$a_t=c$ 增量调整第 $c$ 列 |

**结构化提取 — 奖励函数**：
$r_t = \omega \cdot \mathcal{R}_{sum}(\Phi_t)$（$t=T$ 时 $\omega=2$，否则 $\omega=1$）；$\mathcal{R}_{sum} = \sum_k B \log_2(1+\text{SINR}_k)$；归一化 [NOT_FOUND]

**结构化提取 — 网络架构**（DDQN-GA）：
| 层 | 维度 | 激活 | 归一化 | 优化器 |
|----|------|------|--------|--------|
| FC1 | $N(2M+2K+2)$ → 512 | [NOT_FOUND] | [NOT_FOUND] | lr=5e-4 |
| FC2 | 512 → 512 | [NOT_FOUND] | [NOT_FOUND] | |
| FC3 | 512 → 256 | [NOT_FOUND] | [NOT_FOUND] | |
| FC4 | 256 → 128 | [NOT_FOUND] | [NOT_FOUND] | |
| Output | 128 → $\sqrt{N}+1$ | [NOT_FOUND] | [NOT_FOUND] | |

$\gamma=0.99$，buffer=8000，batch=512，target update=2000

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| FBS→RIS | Rician | $\varepsilon_G=5$；ITU-R P.1238-12 室内 LoS | Section IV |
| RIS→User | Rician | $\varepsilon_h=5$ | Section IV |
| FBS→User 直连 | 阻断 | — | Section II |

---

### [F1] Deep RL-Based Energy Efficiency Optimization of RIS-UAV-Assisted Communication System
- **DOI/来源**：10.1109/VTC2025-Fall65116.2025.11310192
- **发表状态**：正式发表
- **发表渠道**：IEEE VTC2025-Fall（会议论文）
- **年份**：2025
- **核心贡献**：(1) PER-TDDQN 双 DDQN 结构分别优化 UAV 轨迹和波束赋形/RIS 相移，最大化能量效率。(2) 优先经验回放按 TD-error 分配采样优先级加速收敛。
- **方法概述**：DDQN-1 处理 UAV 3D 飞行距离（连续动作），DDQN-2 处理波束赋形变化量+相移变化量，共享 EE 奖励函数。
- **实验设置**：1500m×1500m 区域，UAV 高度 300m，BS (300,600,40)，RIS 50 元素，6 用户，2MHz 带宽，$P=500$mW
- **使用的 Baseline 方法**：
  - RIS-UAV: 不优化波束赋形
  - UAV-NR: 无 RIS
  - Dueling DQN: 单网络
  - DDQN/DQN: 标准算法
- **关键结论**：联合优化轨迹+相移+波束赋形优于部分优化；PER-TDDQN 优于 Dueling DQN/DDQN/DQN
- **与本研究关系**：方法可借鉴
- **实现关键细节**：网络架构/超参数全部缺失；奖励 $r = \sum R_k / P_{total} - p_0 \mathbb{I}[\text{违规}]$；相移连续 $[0, 2\pi)$
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| BS→RIS-UAV | LoS + ULA 阵列响应 | $\alpha_{BR}$ [NOT_FOUND] | §II-A |
| RIS-UAV→User | LoS + ULA 阵列响应 | $\alpha_{RE}$ [NOT_FOUND] | §II-A |
| BS→User 直连 | 阻断 | — | §II-A |

---

### [F3] Self-Attention-Based Deep RL for Joint Beamforming and Phase Shift Design in Aerial IRS Networks
- **DOI/来源**：10.1109/ICC52391.2025.11160846
- **发表状态**：正式发表
- **发表渠道**：IEEE ICC 2025, Mobile and Wireless Networks Symposium（会议论文）
- **年份**：2025
- **核心贡献**：(1) AB-TD3 框架：Actor 嵌入 8 头 self-attention 建模状态元素依赖 + batch normalization 稳定训练。(2) 城市环境仅反射链路的 MU-MISO 系统，TD3 最大熵双 Q 网络联合优化波束赋形+相移。
- **方法概述**：AB-TD3 在标准 TD3 基础上加 attention（多头注意力提取状态特征）和 BN（稳定训练），连续动作空间直接输出波束赋形+相移实虚部。
- **实验设置**：BS 天线 M={8,12}，IRS 元素 N={32,64}，用户 K={8,12}，Rician $\kappa=15$dB，$P_{max}=30$dBW，lr=1e-3，$\gamma=0.99$，$\tau=1e-3$，hidden=400，8 heads
- **使用的 Baseline 方法**：
  - B-TD3: 去掉 attention，仅保留 BN
  - TD3: 标准双 Q 网络
  - DDPG: 标准 DDPG
- **关键结论**：AB-TD3 在所有场景下最优（~15 bps/Hz）；BN 是收敛关键（去掉则不收敛）；attention 额外贡献 ~2 bps/Hz
- **与本研究关系**：**直接相关** + 对比 baseline 候选（AB-TD3 性能上界）
- **实现关键细节**：Actor: input→8-head attention→BN→MLP(400,tanh,BN)→output；Critic×2: input(s,a)→MLP(400,tanh,BN)→Q；lr=1e-3，buffer=1e5，batch=32
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**结构化提取 — 状态空间**：
| 维度名 | 范围/取值 | 归一化方法 |
|--------|----------|------------|
| 波束赋形 $G_{t-1} \in \mathbb{C}^{M \times K}$ | $\|G\|_F^2 \leq P_{max}$ | 实虚分离；BN 内部归一化 |
| 相移 $\Phi_{t-1}$ | $\phi_n \in [0, 2\pi)$ | 实虚分离 |
| BS-IRS 信道 $H_1 \in \mathbb{C}^{N \times M}$ | Rician | 实虚分离 |
| IRS-UE 信道 $H_2 \in \mathbb{C}^{N \times K}$ | Rician | 实虚分离 |
| 发射/接收功率 | 实数矩阵 | 直接输入 |

总维度：$2(MK+N+NM+NK)+M+K$

**结构化提取 — 动作空间**：
| 类型 | 维度 | 合法动作约束 |
|------|------|-------------|
| 连续 | $2(MK+N)$ | 功率约束 $\text{tr}(GG^H) \leq P_{max}$；$\phi_n \in [0,2\pi)$ |

**结构化提取 — 奖励函数**：
$r_t = \sum_{k=1}^{K} \log_2(1 + \text{SINR}_k)$；归一化 [NOT_FOUND]；无额外权重

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| BS→IRS | Rician | $\kappa_1=15$dB | Table I |
| IRS→UE | Rician | $\kappa_2=15$dB | Table I |
| BS→UE | 不建模（遮挡） | — | Section II-A |

---

### [F4] Robust Beamforming and Phase Shift Control in RIS-UAV Relay System Using Deep RL
- **DOI/来源**：10.1109/iWRFAT65352.2025.11102822
- **发表状态**：正式发表
- **发表渠道**：IEEE IWFAT 2025（workshop）
- **年份**：2025
- **核心贡献**：(1) 机载 RIS-UAV 中继系统联合优化波束赋形 + UAV 3D 轨迹 + RIS 相移，SAC 算法求解。(2) 动作归一化映射（$\delta \in [0,1]$ → 物理量）+ 波束赋形功率约束后处理。
- **方法概述**：SAC（双 Q 网络 + 自动温度调节），BS 作为唯一智能体，接收 B2R/R2U 信道状态，输出归一化速度/航向/俯仰/相移/波束赋形。
- **实验设置**：BS 60m 高，9 天线 UPA；RIS 3×3=9 元素 UPA；GU 移动 10m/s；UAV (100,100,100) 起飞；$C_0=-30$dB，$\beta=2.8$，$P_T=10$dBm，$\sigma_0^2=-170$dBm/Hz；Actor lr=1e-3，Critic lr=3e-4
- **使用的 Baseline 方法**：
  - DDPG: 同场景同目标
  - Fixed RIS: 固定安装 RIS，无 UAV
- **关键结论**：SAC 比 DDPG 高 16.2%，比固定 RIS 高 64.9%；收敛更快更稳
- **与本研究关系**：方法可借鉴（SAC 框架 + 动作归一化策略）
- **实现关键细节**：动作 $\delta \in [0,1]$ 映射：$v_r=\delta_v V_{max}$，$\phi_r=\delta_\phi 2\pi$，$\theta_n=\delta_\theta 2\pi$；波束赋形 $\mathbf{w}=\mathbf{v}/\|\mathbf{v}\| \cdot \sqrt{P_T}$；奖励 $r=\lambda R_{sys} - a\mathbb{I}(z<z_{min})$，$\lambda,a$ [NOT_FOUND]
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| BS→RIS | 纯 LoS（Rician→∞） | $C_0=-30$dB，$\beta=2.8$ | Table I |
| RIS→User | 纯 LoS（Rician→∞） | 同上 | Table I |

---

### [F7] Energy Efficiency Optimization in RIS-assisted ISATRNs with RSMA: A Federated DRL Approach
- **DOI/来源**：10.1109/WCNC57260.2024.10570820
- **发表状态**：正式发表
- **发表渠道**：IEEE WCNC 2024（会议论文）
- **年份**：2024
- **核心贡献**：(1) RIS 辅助 RSMA 使能的 ISATRN 系统模型，联合优化波束赋形+RIS 相移+功率分裂+UAV 轨迹。(2) AF-DRL 联邦框架：全局 DDPG 优化 UAV 轨迹，局部 DDQN 优化相移/波束/功率，联邦聚合。
- **方法概述**：两级 MDP，全局阶段 DDPG 处理离散 UAV 移动，局部阶段 DDQN 处理混合动作（11 级相移增量 + 3 级波束增量 + 连续功率分裂比 via tanh）。
- **实验设置**：GEO 卫星，2GHz/15MHz，UAV 高度 1000m，6 用户，RIS 16 元素，$\gamma=0.9$，训练 20000 episodes
- **使用的 Baseline 方法**：
  - MRT scheme: 最大比发送
  - RIS random: 随机相移
- **关键结论**：RSMA 优于 NOMA/OMA；AF-DRL 收敛更快奖励更高；联邦框架可扩展
- **与本研究关系**：方法可借鉴（联邦框架 + 两级 MDP + tanh 动作映射）
- **实现关键细节**：相移增量 $\Delta\theta_m$ 同 L01 的 11 级方案；连续动作 $\chi_i = \frac{1}{2}(1+\tanh(x_i))$ 映射到 (0,1)；局部奖励 $r_L = SEE \times (\Omega_{POW} \cdot \Omega_{COM} \cdot \Omega_{UAV} \cdot \Omega_{QoS})$，各 $\Omega$ 值 [NOT_FOUND]
- **开源代码**：无
- **验证状态**：已通过学术搜索工具验证

**信道模型参数**：
| 链路 | 模型 | 关键参数 | 来源 |
|------|------|----------|------|
| 卫星→HAP (FSO) | 标量衰落 | $P_S$，$\delta_{OE}$，$\sigma_{SH}^2$ | §II-A |
| HAP→设备/RIS | 随机生成 | 引用 [13][14]，具体模型未给 | §II-A |

## Baseline 交叉验证

### Baseline 出现频率统计
| 方法名 | 被几篇论文使用 | 使用该 baseline 的论文 | 代码状态 | 算法描述质量 | 推荐优先级 |
|--------|--------------|----------------------|---------|------------|-----------|
| Random phase shift | 3 篇 | L06, L01, F7 | 无需代码 | 简单 | 4（最基础对照） |
| DDPG | 2 篇（含自实现） | L02(提出), F4(baseline) | 无 | 中等（L02 有动作设计细节） | 1 |
| DDQN | 4 篇 | L06, L01, F1, F7 | 无 | 中等（L06 最详细） | 2 |
| DQN | 2 篇 | L06(baseline), F1(baseline) | 无 | 低 | 3 |
| TD3 | 1 篇（含变体） | F3(AB-TD3) | 无 | 高（超参完整） | 1 |
| SAC | 1 篇 | F4(提出) | 无 | 中等（有学习率） | 2 |

### Baseline 候选
| 候选 | 来源文献 | 代码状态 | 选择优先级 | 选择理由 |
|------|---------|---------|-----------|---------|
| B1: DDPG | L02 | 无，需自实现 | 1 | 被L02和F4交叉使用，连续动作空间的标准方案，MDP 建模有参考 |
| B2: AB-TD3 | F3 | 无，需自实现 | 1 | attention+BN 增强的 TD3，超参最完整（lr, γ, τ, hidden, heads 全有） |
| B3: DDQN+GA | L06 | 无，需自实现 | 2 | 离散相移优化 SOTA，动作空间压缩方案有创新，网络架构+超参较完整 |
| B4: SAC | F4 | 无，需自实现 | 3 | 最大熵框架，Actor lr=1e-3/Critic lr=3e-4 有参考值 |
| B5: Random phase | 通用 | 无需代码 | 4 | 最基础对照，3 篇论文使用 |
