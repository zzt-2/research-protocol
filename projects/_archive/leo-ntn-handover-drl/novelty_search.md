# Contract 阶段 · 新颖性检索报告

> 2026-05-08，三路并行检索，评估三个候选 DRL 改进方案的新颖性。

## 检索结论

| 方案 | 新颖性 | 最强竞争者 | 竞争者级别 | 核心组合被覆盖度 |
|------|--------|-----------|-----------|----------------|
| A: LA-DDQN | 中 | ARTHF (Fan et al., MDPI Electronics 2025) | MDPI Electronics | Dueling+Attention+负载 三要素全被覆盖 |
| B: MA-CTDE | **低** | ILCHO (IEEE TMC 2026) + QMIX-PHO (ETRI 2025) | IEEE TMC 顶刊 | QMIX+CTDE+切换+负载 被顶刊完全覆盖 |
| C: GNN+DRL | **中高** | Yu et al. (MDPI Aerospace 2024) 仅部分重叠 | MDPI Aerospace | "二部图 GNN+DRL+多UE负载均衡"三元组合无人占据 |

**决策：方案 B 排除，方案 A 和 C 分别深入设计。**

---

## 方案 A：LA-DDQN（负载注意力 Dueling DDQN）

### 核心思路
在 B2 Dueling DDQN 基础上增加卫星负载注意力模块 + top-K 候选观测压缩（1585→41维）。

### 竞争者详情

**ARTHF (Fan et al., 2025, MDPI Electronics 14(15), 3040)**
- URL: https://www.mdpi.com/2079-9292/14/15/3040
- 架构：Self-attention → Dueling Rainbow DQN（含分布式 Q 值）
- Attention 机制：self-attention 消除候选卫星位置偏差，Q/K/V 投影 + softmax
- 负载感知：reward 联合切换频率+SNR+负载分布；LSTM 流量预测纳入负载代价
- 候选处理：zero-padding 到 M_max
- 决策范式：每个 TTG 独立 agent

**Dueling DDQN 多目标切换 (Chou et al., arXiv:2605.02416, 2026.05)**
- URL: https://arxiv.org/abs/2605.02416
- Dueling DDQN + 负载/阻塞感知，无 attention
- 已作为 B2 baseline 实现基础

### 差异化空间

| 差异点 | ARTHF | 方案 A 可做 |
|--------|-------|-----------|
| 候选处理 | zero-padding | **top-K 压缩**（文献中未见） |
| Attention 类型 | 通用 self-attention over all features | **专用负载注意力**（query=负载状态） |
| 流量预测 | LSTM 预测 | 可选（非核心差异） |
| RL 架构 | Rainbow DQN（重） | Dueling DDQN（轻） |

### 方案 A 深入设计待办
1. 精读 ARTHF 全文，确认 attention 模块具体架构
2. 设计专用负载注意力模块（与 ARTHF self-attention 区分）
3. 实现 top-K 候选压缩，设计消融实验 vs zero-padding
4. 确认 top-K 压缩的信息损失理论界（如有）

---

## 方案 C：GNN+DRL（二部图 GNN 编码 + DRL 决策）

### 核心思路
UE-卫星二部图 GNN 编码卫星/UE 邻居信息 → 图嵌入作为 DRL 观测 → Dueling DDQN 做切换决策。

### 竞争者详情（均为部分覆盖）

**Yu et al. (2024, MDPI Aerospace)**
- URL: https://www.mdpi.com/2226-4310/11/7/511
- MPNN（有向卫星切换图）+ DQN
- **差异**：有向图（非二部图），单用户场景
- 与方案 C 重叠度：低

**Lee et al. / L15 (2025, ICT Express)**
- URL: https://www.sciencedirect.com/science/article/pii/S259015442500062X
- GNN 二部图 + softmax 选星 + 卫星侧 ACK 负载控制
- **差异**：纯 GNN softmax（无 DRL），无 reward-based 学习
- 与方案 C 重叠度：中（图结构相同，决策机制不同）

**Kazzi et al. (2025, IEEE OJCS)**
- 加权二部图 + KM 匹配算法
- **差异**：无 ML/DRL，纯优化
- 与方案 C 重叠度：低

**其他相关（非直接竞争）**
- GAT 负载感知资源编排 (2024, 西安电子科技大学)：GAT for Service Function Chain 编排（非切换）
- 6G causality-aware DRL + attention (2025, ScienceDirect)：因果推理+attention for 资源编排

### 空隙确认

"UE-卫星二部图 GNN + DRL + 多 UE 联合负载均衡"三元组合在现有文献中**无人占据**。

### 方案 C 深入设计待办
1. 精读 Yu et al. (2024) 和 L15 (2025) 全文，确认 GNN 架构细节
2. 设计二部图结构：UE 节点特征、卫星节点特征、边特征
3. 选择 GNN 层类型（GCN/GAT/MPNN），分析训练稳定性
4. 确定与 DRL 的接口：GNN 输出 → DRL 观测空间
5. 评估 GNN 训练不稳定风险及缓解策略

---

## 可借鉴思路汇总

| 思路 | 来源 | 适用方案 |
|------|------|---------|
| Self-attention 消除候选位置偏差 | ARTHF | A |
| 拥塞度显式建模 cong(t)∈[0,1] | Hybrid Model-Aided (Luxembourg) | A/B/C |
| GNN 二部图 softmax 选星 + ACK 负载控制 | L15 | C |
| Greedy solver bootstrap 加速训练 | AAAI 2025 satellite assignment | C |
| 条件切换(CHO)距离触发 | ILCHO (IEEE TMC 2026) | — |
| 三态 Markov 信道模型 | IEEE TWC 2024 MADQN | A/C |
| Hysteretic Q-learning 抗多 agent 不稳定性 | IEEE TWC 2024 | — |
| LSTM 流量预测纳入状态 | ARTHF | A |

---

## 综合评估

| 维度 | A: LA-DDQN | C: GNN+DRL |
|------|-----------|-----------|
| 新颖性 | 中 | **中高** |
| 实现复杂度 | 中 | 高 |
| 训练稳定性风险 | 低 | **高**（GNN 训练不稳定） |
| 与现有 baseline 衔接 | 直接（B2 DDQN 扩展） | 需新增 GNN 模块 |
| 故事清晰度 | 中（需解释与 ARTHF 差异） | **高**（"结构化图编码让 DRL 更好地理解负载分布"） |
| 潜在折中 | GNN 编码替代 flat obs → DDQN 决策 | 同左 |

---

## 竞争者论文 URL 列表（供精读）

### 方案 A 相关
- ARTHF: https://www.mdpi.com/2079-9292/14/15/3040
- Dueling DDQN 多目标: https://arxiv.org/abs/2605.02416
- MADQN Mega-Constellation (IEEE TWC 2024): https://dl.acm.org/doi/abs/10.1109/TWC.2024.3407358

### 方案 C 相关
- Yu et al. GNN+DQN: https://www.mdpi.com/2226-4310/11/7/511
- L15 GNN 二部图: https://www.sciencedirect.com/science/article/pii/S259015442500062X
- Kazzi KM 匹配: https://www.sciencedirect.com/science/article/pii/S259015442500062X

### 方案 B 相关（已排除，仅供参考）
- ILCHO (IEEE TMC 2026): https://www.computer.org/csdl/journal/tm/2026/05/11295961/2ckEkdFBdRK
- QMIX-PHO (ETRI 2025): https://onlinelibrary.wiley.com/doi/10.4218/etrij.2025-0240

---
---

# 方案 C 完整技术设计

> 2026-05-08，基于竞争者精读（Yu et al. 全文 + L15 笔记）完成深入设计。

## C1. 竞争者架构摘要

### Yu et al. (2024, MDPI Aerospace 11(7):511)

**架构**：有向切换图 + 边级 MPNN + DQN

| 模块 | 设计 |
|------|------|
| 图结构 | 有向图（非二部图），节点=卫星切换路径 |
| 消息传递 | **边级** MPNN（非节点级）：边特征 [delay, rate, service_time, zero-padding] |
| 消息函数 | M(h_edge_i, h_edge_j) — 相邻路径间的消息 |
| 聚合 | A() = element-wise sum |
| 更新 | U() = RNN（跨时间步保持状态） |
| Readout | DNN 输出路径评分 |
| 动作空间 | 路径级选择（非直接选星） |
| 场景 | **单用户**，电力网场景 |
| 奖励权重 | AHP 导出 [throughput=0.1095, delay=0.3090, load=0.5815] |
| 收敛 | ~1700 episodes |

**关键差异**：有向图（非二部图）、单用户、边级传递（非节点级）、RNN 更新。

### L15 / Lee et al. (2025, ICT Express)

**架构**：二部图 + FCN 消息传递 + softmax 选星

| 模块 | 设计 |
|------|------|
| 图结构 | UE-卫星二部图 |
| 消息传递层数 | T=2 |
| 每层设计 | sat→UE: FCN_s(h_sats); UE→sat: FCN_u(h_ues)，每层每类节点独立 FCN |
| 选星 | softmax over satellite scores（**无 DRL**） |
| 负载控制 | 卫星侧 ACK 机制：超过容量拒绝连接 |
| 损失函数 | L = -1/\|B\| Σ[p·log₂(1+SINR)] + ω·Σ(ReLU(Σp - P)) |
| 训练 | Adam lr=1e-5, 70 episodes, batch=4 |
| 建边条件 | elevation ≥ 25° |
| 泛化 | 50 UE 训练可迁移到不同 UE 数量 |

**关键差异**：无 DRL（纯 GNN softmax）、ACK 负载控制（非 reward-based 学习）、无切换惩罚。

### 空隙确认（更新）

| 组合要素 | Yu et al. | L15 | 方案 C |
|----------|-----------|-----|--------|
| 二部图 | ✗（有向图） | ✓ | ✓ |
| GNN 编码 | ✓（MPNN） | ✓（FCN） | ✓ |
| DRL 决策 | ✓（DQN） | ✗（softmax） | ✓（Dueling DDQN） |
| 多 UE 联合负载均衡 | ✗（单用户） | ✓（50 UE） | ✓ |
| Reward-based 学习 | ✓ | ✗ | ✓ |

**"二部图 GNN + DRL + 多 UE 联合负载均衡"三元组合仍然无人占据。**

---

## C2. 二部图结构设计

### 图定义

在每一步决策时刻 t，构建动态二部图 G_t = (V_ue, V_sat, E)：

- **V_ue**：15 个 UE 节点
- **V_sat**：可见卫星子集（top-K 候选，K=6）
- **E**：UE-sat 可见边（elevation ≥ 20°）

**top-K 候选选择规则**：
1. 对每个 UE，按 elevation 降序排列所有可见卫星
2. 取前 K=6 个（仿真器统计：平均 4.4 颗可见，最大 6 颗，K=6 覆盖全部）
3. 不足 K 个时，用 dummy 边填充（特征全零）

### 节点特征

**UE 节点特征（dim=4）**：

| 维度 | 名称 | 范围 | 含义 |
|------|------|------|------|
| 0 | t_conn_norm | [0,1] | 当前连接时长 / 100 步（cap at 1.0） |
| 1 | sinr_serving | [0,1] | 当前服务卫星的 R_norm |
| 2 | load_serving | [0,1] | 当前服务卫星的 load_norm |
| 3 | is_blocked | {0,1} | 是否被阻塞 |

设计理由：UE 特征编码"当前状态"——连接多久了、信号多好、负载如何、是否被阻塞。这些是 UE 做切换决策时需要知道的自身状态。

**卫星节点特征（dim=2）**：

| 维度 | 名称 | 范围 | 含义 |
|------|------|------|------|
| 0 | load_norm | [0,1+] | 当前连接 UE 数 / SAT_CAPACITY |
| 1 | orbit_phase | [0,1] | 轨道相位（用于编码卫星运动趋势） |

设计理由：卫星的关键信息是其负载状态。orbit_phase 帮助 GNN 学习"即将离开可见区域的卫星"模式（高 phase → 卫星正在远离），这是 flat observation 无法自然编码的信息。

**orbit_phase 计算**：phase = (sat_orbit_position_in_period) / orbit_period，标准化到 [0,1]。同一轨道面的卫星共享相位偏移，不同轨道面有固定 phase_offset。

### 边特征

**UE→Sat 边特征（dim=3）**：

| 维度 | 名称 | 范围 | 含义 |
|------|------|------|------|
| 0 | sinr_norm | [0,1] | 该 UE-sat 链路的归一化速率 R_norm |
| 1 | elev_norm | [0,1] | 归一化仰角 (elev - min_elev) / (90 - min_elev) |
| 2 | is_current | {0,1} | 是否为当前服务链路 |

设计理由：链路质量（SINR + 仰角）是切换决策的**主要信息**。is_current 让 GNN 知道"当前连接是谁"，用于编码切换成本。

### 与当前 B2 观测空间的对比

| 维度 | B2 flat obs | C bipartite graph |
|------|------------|-------------------|
| UE 特征 | 1 (t_conn_norm) | 4 维独立节点特征 |
| 卫星特征 | 396×3 (sinr, elev, load) | K=6 卫星 × 2 维节点特征 |
| 连接标记 | 396×1 (is_current) | 6 条边的 is_current |
| 总有效维度 | 1585 | 15×4 + 6×2 + 15×6×3 = 352 |
| 信息密度 | 低（大量不可见卫星零填充） | **高（仅可见卫星）** |

**关键改进**：从 1585 维冗余向量 → 352 维结构化图表示，且自然编码了 UE 间竞争关系。

---

## C3. GNN 层选型

### 候选方案对比

| 维度 | GCN | GAT | **MPNN-E**（选定） |
|------|-----|-----|-------------------|
| 边特征利用 | ✗ | ✗（标准 GAT） | ✓ 原生支持 |
| 邻居权重 | 均等 | 学习注意力 | 学习消息函数 |
| 参数量 | 少 | 中 | 中 |
| 训练稳定性 | 高 | 中 | 中（需 LayerNorm） |
| 切换场景适配 | 差（SINR/elev 被忽略） | 中（注意力可间接学习） | **好（边=SINR+elev 直接进消息）** |
| 文献支撑 | 通用 | 通用 | Yu et al. 验证 + L15 FCN 验证 |

### 选定方案：边条件化 MPNN（MPNN-E）

**理由**：
1. 边特征（SINR, elevation）是切换决策的**主要信息源**，MPNN 原生利用
2. Yu et al. 在卫星切换中验证了 MPNN（有向图，但消息传递框架相同）
3. L15 在二部图中验证了 FCN 消息传递（MPNN 的特例）
4. 比 GAT 更自然——不需要人为设计注意力机制，消息函数自动学习

### MPNN-E 消息传递规则

**二部图方向性**：UE↔Sat，分两步传递

**Step 1: UE → Sat**
```
m_{ue_i → sat_j} = MLP_msg_ue([h_ue_i || h_sat_j || e_ij])    // 边条件化消息
h_sat_j' = MLP_update_sat([h_sat_j || mean({m_{ue→sat_j}})])   // 聚合所有 UE 消息
h_sat_j' = LayerNorm(h_sat_j + h_sat_j')                        // 残差 + 归一化
```

**Step 2: Sat → UE**
```
m_{sat_j → ue_i} = MLP_msg_sat([h_sat_j' || h_ue_i || e_ij])  // 用更新后的 sat 表示
h_ue_i' = MLP_update_ue([h_ue_i || mean({m_{sat→ue_i}})])      // 聚合所有 sat 消息
h_ue_i' = LayerNorm(h_ue_i + h_ue_i')                           // 残差 + 归一化
```

**T=2 层**：重复上述 Step 1+2 共 2 次（L15 验证 T=2 足够）。

**维度设计**：

| MLP | 输入 dim | 隐藏 dim | 输出 dim |
|-----|---------|---------|---------|
| MLP_msg_ue | 4+2+3=9 | 32 | 32 |
| MLP_update_sat | 2+32=34 | 32 | 2 |
| MLP_msg_sat | 2+4+3=9 | 32 | 32 |
| MLP_update_ue | 4+32=36 | 32 | 4 |

最终 UE 节点嵌入维度 = 4（原始特征）→ GNN 后仍为 4，但编码了邻居信息。

**可选增强**：在残差连接中增加投影维度：
```
h_ue_i' = LayerNorm(MLP_project(h_ue_i) + MLP_update_ue(AGG(messages)))
```
投影到 d=64 维以增加表达能力。这将使最终 UE 嵌入为 64 维。

---

## C4. GNN → DRL 接口设计

### 核心思路：分解式 Q 函数

标准 Dueling DDQN 输出 |A| 个 Q 值（|A|=396），需要巨大的输出层。

**方案 C 采用分解式 Q 函数**：
```
Q(UE_i, sat_j) = V(h_ue_i) + A(h_ue_i, h_sat_j, h_edge_ij) - mean_j(A(h_ue_i, h_sat_j, h_edge_ij))
```

- **V(h_ue_i)**：状态价值，仅依赖 UE 嵌入（全局视角）
- **A(UE_i, sat_j)**：卫星选择优势，依赖 UE+卫星+链路三方嵌入

### 网络架构

```
输入：二部图 G_t
  ↓
[GNN Encoder (T=2 MPNN-E)]
  → h_ue_i ∈ R^64 (per UE)
  → h_sat_j ∈ R^64 (per visible sat)
  → h_edge_ij ∈ R^32 (per UE-sat edge)
  ↓
[Dueling Q-Network]
  V(h_ue_i) = MLP_v(h_ue_i) → scalar        // 共享，所有 UE 用同一个 MLP_v
  A(ue_i, sat_j) = MLP_a([h_ue_i || h_sat_j || h_edge_ij]) → scalar  // 共享
  Q(i,j) = V(i) + A(i,j) - mean_j(A(i,j'))
  ↓
[Action Selection]
  mask: 仅 visible satellites
  action_i = argmax_{j ∈ visible} Q(i,j)    // ε-greedy exploration
```

### 参数量对比

| 网络 | 参数量 | 说明 |
|------|--------|------|
| B2 DDQN | 1585×256 + 256×128 + 128×396 ≈ 712K | flat obs → flat Q |
| C MLP_v | 64×64 + 64×1 ≈ 4K | UE 嵌入 → 标量 V |
| C MLP_a | (64+64+32)×64 + 64×1 ≈ 10K | 三方嵌入 → 标量 A |
| C GNN | ~15K | 4 个小 MLP + LayerNorm |
| **C 总计** | **~29K** | **比 B2 少 25×** |

参数效率来源：GNN 参数在所有 UE/sat 对之间**共享**，分解式 Q 避免了巨大的输出层。

### 动作空间

| 属性 | B2 (flat) | C (graph) |
|------|-----------|-----------|
| 动作空间大小 | 396（所有卫星） | K+1 ≤ 7（top-K 候选 + 保持当前） |
| 无效动作处理 | Q 值 mask 为 -∞ | 自然排除（不在候选集中） |
| 探索效率 | 低（396 选 1） | **高（≤7 选 1）** |

---

## C5. 训练稳定性评估与缓解策略

### 风险清单

| ID | 风险 | 严重度 | 可能性 | 影响 |
|----|------|--------|--------|------|
| R1 | GNN 过平滑（over-smoothing） | 低 | 低 | T=2 层，L15 已验证 |
| R2 | 图拓扑非平稳（可见卫星每步变化） | **高** | 高 | 卫星运动导致节点/边每步不同 |
| R3 | 梯度爆炸/消失 | 中 | 低 | 2 层 GNN + LayerNorm + 残差 |
| R4 | 多 UE 信用分配 | 中 | 中 | 15 UE 共享卫星容量，决策相互影响 |
| R5 | GNN 与 DRL 联合训练不稳定 | **高** | 中 | GNN 编码质量直接影响 DRL 输入 |
| R6 | 小图过拟合 | 中 | 中 | 15 UE + 6 sat，图规模小 |

### 缓解策略

**MS1: 两阶段训练**

- **Phase 1 — GNN 预训练**（~50 episodes, ~30 min）：
  - 目标：用监督学习训练 GNN 编码器
  - 辅助任务 1：预测每个 UE 下一步是否被阻塞（二分类）
  - 辅助任务 2：预测每个卫星下一步负载变化（回归）
  - 损失：L_aux = BCE(block_pred, block_true) + MSE(Δload_pred, Δload_true)
  - 目的：强制 GNN 学会编码负载相关信息，避免 DRL 训练初期收到噪声编码

- **Phase 2 — 联合 GNN + DRL 训练**（~300 episodes, ~12h）：
  - GNN lr = 1e-4（10× 小于 DRL lr = 1e-3）
  - DDQN 框架 + experience replay（复用 B2 的 buffer/batch 设计）
  - GNN 梯度裁剪：max_norm = 0.5

**MS2: 拓扑非平稳处理**

- 每步重新构建图（不做跨步图缓存）
- 节点特征归一化到 [0,1]（已设计）
- orbit_phase 提供位置连续性（即使节点 ID 变化，同轨道面的卫星有相似的 phase 模式）
- 可选：卫星节点 ID embedding（固定，dim=8），让 GNN 区分不同卫星

**MS3: 残差 + LayerNorm + 梯度裁剪**

- 每层 GNN 残差连接：h' = LayerNorm(h + update(AGG(messages)))
- 全局梯度裁剪：max_norm = 1.0
- 与 B2 一致的经验回放稳定机制（target network, double Q-learning）

**MS4: 消融实验设计**

| 实验组 | 变量 | 目的 |
|--------|------|------|
| C-full | 完整方案 C | 主结果 |
| C-no-pretrain | 跳过 Phase 1 | 验证预训练价值 |
| C-T1 | T=1 层 GNN | 验证消息传递深度 |
| C-no-orbit | 去掉 orbit_phase | 验证轨道编码价值 |
| C-gat | 替换为 GAT-E | 对比 GNN 层类型 |
| B2-topK | B2 + top-K 压缩 | 隔离 top-K vs GNN 的贡献 |

---

## C6. 完整架构总览

```
[Environment] ──每步──→ [Graph Builder]
                           │
                    构建 top-K=6 二部图
                    UE(15)×4, Sat(≤90)×2, Edge(≤90)×3
                           │
                    ┌──────▼──────┐
                    │  GNN Encoder │  T=2 MPNN-E
                    │  (预训练+微调) │  dim=64
                    └──────┬──────┘
                           │
                 h_ue(15×64), h_sat(≤90×64), h_edge(≤90×32)
                           │
                    ┌──────▼──────┐
                    │ Dueling Q   │  分解式: V(s) + A(s,a) - mean(A)
                    │ (共享 MLP)   │  ~14K params
                    └──────┬──────┘
                           │
                 Q(UE_i, sat_j) for j ∈ visible
                           │
                    [ε-greedy + mask]
                           │
                    action ∈ {0, ..., K}
                           │
                    [Environment.step()]
```

### 与 B2 的代码复用

| 模块 | 复用 | 新增 |
|------|------|------|
| 仿真器 | 100% | — |
| 奖励函数 | 100% | — |
| Experience replay | 100% | — |
| ε-greedy 调度 | 100% | — |
| Q-network | V(s) 复用 Dueling 结构 | 分解式 A(s,a) |
| **GNN 编码器** | — | **新增 ~15K params** |
| Graph builder | — | **新增** |
| 预训练循环 | — | **新增** |

---

## C7. 方案 A vs C 最终对比

| 维度 | A: LA-DDQN | C: GNN+DRL |
|------|-----------|-----------|
| **新颖性** | 中（ARTHF 覆盖 Dueling+Attention+Load 三要素） | **中高**（三元组合无人占据） |
| 实现复杂度 | 中（attention + top-K） | 高（GNN + 分解式 Q + 预训练） |
| 训练稳定性 | 低（DDQN 扩展） | 中（两阶段训练缓解） |
| 参数量 | ~712K | **~29K（25× 少）** |
| 故事清晰度 | 中（需解释与 ARTHF 差异） | **高**（"结构化图编码 → 负载感知决策"） |
| 可扩展性 | 低（固定 obs 大小） | **高**（图大小可变，可迁移） |
| 与 L15 差异化 | N/A | **清晰**（L15 无 DRL，C 加 DRL） |
| 与 Yu et al. 差异化 | N/A | **清晰**（Yu 有向图+单用户，C 二部图+多 UE） |
| 预期训练时间 | ~10h | ~12h（+30min 预训练） |
| 仿真器改动 | 小（top-K 预处理） | 中（新增 graph builder） |

### 最终推荐：方案 C（GNN+DRL）

**核心理由**：

1. **新颖性优势显著**：三元组合"二部图 GNN + DRL + 多 UE 负载均衡"在文献中无竞争者。方案 A 的差异化空间窄（top-K + 专用注意力 vs ARTHF 的 self-attention + Rainbow DQN）。

2. **故事更具说服力**：论文叙事 = "flat observation 将 UE-satellite 关系展平为向量，丢失了结构化的负载竞争信息。二部图 GNN 通过消息传递让 UE 自然感知邻居卫星的负载状态，使 DRL 做出负载均衡的切换决策。"

3. **方案 A 的 top-K 可作为 C 的预处理**：top-K 候选压缩不是 LA-DDQN 专属，GNN 方案同样受益（图规模从 396 降到 6）。

4. **参数效率带来更好的泛化性**：29K vs 712K 参数，GNN 参数在所有 UE/sat 对间共享。这支持"可迁移性"的叙事（L15 已验证 50 UE 训练可迁移）。

5. **风险可控**：两阶段训练 + T=2 层 + 残差 + LayerNorm 的组合，参考 L15 的稳定训练经验。消融实验可量化每个设计选择的贡献。

---

# 方案 A 完整技术设计：LA-DDQN

> 2026-05-08，基于 ARTHF 全文精读（DOI:10.3390/electronics14153040）完成深入设计。

## A1. ARTHF 架构深度解析

### A1.1 Self-Attention 模块（Eq. 26-28）

```
输入: S_e ∈ R^{M_max×7}（zero-pad 到 M_max=8）
特征: [service_status, elevation, distance, remaining_time, SNR, demand_weight, load_Ψ]

投影:  q_m = s_m · W_Q    (s_m = S_e 的第 m 行)
       k_m = s_m · W_K
       v_m = s_m · W_V
       输出维度 D

注意力分数: α_{m,n} = exp(q_m · k_n / D) / Σ_{n=1}^{M_k^t} exp(q_m · k_n / D)
                          ⚠ 分母求和范围是 M_k^t（有效卫星），不是 M_max

输出: z_m = Σ_{n=1}^{M_k^t} α_{m,n} · v_n    →    Z ∈ R^{M_max × D}
```

**关键发现**：attention softmax 仅在有效卫星间计算（Eq.27 用 M_k^t），positional bias 问题被论文夸大。Self-attention 真正作用是**捕获卫星间关系**。

### A1.2 FC + 掩码（Eq. 29）

```
Z → FC(256, ReLU) → FC(128, ReLU) → FC(64, ReLU) → H ∈ R^{M_max×64}
掩码: o_m = 1 if S_e(m,:) ≠ 0, else 0 → H' = H ⊙ o
```

**问题**：FC 处理所有 M_max=8 行（含 zero-pad），浪费 ~40% 计算。

### A1.3 Dueling 架构（Eq. 30-31）

```
Value:   h_avg = (1/M_k^t) Σ H'(m,:) → FC → v
Advantage: H → FC → A ∈ R^{M_max × |atoms|}
         ⚠ A 从 H（非 H'）计算，含 zero-pad 行

Q(m,:) = v^T + A(m,:) - (1/M_k^max) Σ A(n,:)
         ⚠ Advantage 中心化使用 M_k^max（含 zero-pad），引入数值偏差
```

ARTHF 实为 **Rainbow DQN + attention**（分布式 Q 51 atoms + n-step + 优先回放 + noisy nets），非普通 DQN。

### A1.4 LSTM 流量预测

2 层 stacked LSTM，输入 [T_l=3, F_l=3]，每层 3 单元 → FC(128,64,32,1) → 流量预测。

### A1.5 奖励函数（Eq. 25）

r_t = Σ_k [Λ_k^t + β·SNR_{k,m}^t + γ·Ψ_{k,m}^t]。⚠ SNR 未归一化（dB 量级 ~10-30）。

### A1.6 仿真设置

| 参数 | 值 |
|------|------|
| 星座 | 4408 星（5 子星座，仿 Starlink） |
| 频段 | Ka 20GHz，400MHz |
| TTG | 20×20=400，25km 网格 |
| 决策间隔 | 15s |
| 最小仰角 | 40° |
| 训练 | lr=0.001, γ=0.95, 1000 episodes |
| 对比方法 | **仅 Rainbow DQN 变体，无传统方法** |

---

## A2. ARTHF vs LA-DDQN 精确对比

| 维度 | ARTHF | LA-DDQN | 差异性质 |
|------|-------|---------|---------|
| RL 骨干 | Rainbow DQN（重） | Dueling DDQN（轻） | 架构选型 |
| Attention 类型 | Self-attention（Q/K/V 同源） | **Cross-attention**（Q=负载上下文） | **结构性** |
| Attention 目的 | 消除位置偏差 + 卫星间关系 | **负载驱动特征选择** | 语义 |
| 候选处理 | Zero-padding M_max=8 | **Top-K 压缩** K=8 | **方法论** |
| 观测维度 | 56 维/TTG | 41 维/UE | 效率 |
| 负载感知 | 负载作为特征之一 + 奖励 Ψ | **负载驱动 attention query** + 奖励 L_norm | **结构性** |
| Advantage 中心化 | 含 zero-pad 行 ⚠ | 仅有效行 | 数值准确 |
| 对比方法 | 3 个 Rainbow 变体（弱） | HHS + DDQN + Random + 消融（强） | 全面 |

**三个核心差异**：
1. **Cross-attention vs Self-attention**：Q 来源不同（负载 vs 卫星特征），结构层面差异
2. **Top-K vs Zero-padding**：信息密集 vs 稀疏填充，影响 FC 效率和 attention 质量
3. **轻量骨干 vs Rainbow DQN**：训练更快，部署更容易

---

## A3. DLA（Dedicated Load Attention）模块设计

### A3.1 核心思想

ARTHF self-attention 的 Q/K/V 全部来自卫星特征，attention 权重**不受负载状态驱动**。DLA 的原则：**让负载分布主动驱动注意力**。

### A3.2 架构

```
┌───────────────────────────────────────────────────────────┐
│            Input: Top-K Candidates (K, 5)                  │
│     [sinr_norm, load_norm, elev_norm, rem_t_norm, is_svc]  │
└─────────────────────────┬─────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
      ┌─────┴──────┐             ┌──────┴──────┐
      │ Load Stats │             │ Sat Feats   │
      │ l_avg      │             │ all 5 feats │
      │ l_max      │             │  per row    │
      │ l_std      │             │  (K, 5)     │
      │ n_svc      │             └──────┬──────┘
      └─────┬──────┘                    │
            │                     ┌──────┴──────┐
      ┌─────┴──────┐              │ W_K → K_mat │
      │ W_q → q    │              │ W_V → V_mat │
      │  (1, d)    │              │   (K, d)    │
      └─────┬──────┘              └──────┬──────┘
            │                            │
            └──────────┬─────────────────┘
                       │
             ┌─────────┴──────────┐
             │  Cross-Attention    │
             │  α = softmax(q·Kᵀ/√d) │
             │  z = Σ_m α_m · V_m  │
             │     Shape: (1, d)   │
             └─────────┬──────────┘
                       │
            ┌──────────┴──────────────┐
            │  Per-satellite Fusion    │
            │  h_m = [sat_feat[m] ; z] │
            │     Shape: (K, 5+d)      │
            └──────────┬──────────────┘
                       │
            ┌──────────┴──────────────┐
            │ FC(256)→FC(128)→FC(64)  │
            │       H ∈ (K, 64)       │
            └──────────┬──────────────┘
                       │
            ┌──────────┴──────────────┐
            │   Dueling Architecture   │
            │ Value: mean(H)→FC→v      │
            │ Advantage: H→FC→A ∈ R^K  │
            │ Q(m) = v+A(m)-mean(A)    │
            └─────────────────────────┘
```

### A3.3 与 ARTHF Self-Attention 的结构对比

```
ARTHF Self-Attention:
  Query: 卫星 m 的特征 s_m           ← 每颗卫星独立 query
  Key:   卫星 n 的特征 s_n           ← 卫星间互查
  Value: 卫星 n 的特征 s_n
  输出:  Z ∈ R^{M_max × d}          ← 每颗卫星独立输出
  语义:  "卫星 m 应该关注哪些其他卫星"

DLA Cross-Attention:
  Query: 负载统计 [l_avg,l_max,l_std,n_svc]  ← 全局负载上下文
  Key:   卫星 m 的特征                       ← 卫星被查询
  Value: 卫星 m 的特征
  输出:  z ∈ R^{1 × d}                       ← 单一负载感知上下文
  语义:  "给定当前负载分布，哪些卫星特征最重要"
```

**本质区别**：ARTHF 的 query/key 同源（卫星特征）= self-attention。DLA 的 query 来自负载、key 来自卫星 = cross-attention。**结构性差异，非超参调优。**

### A3.4 参数规格

| 参数 | 值 | 理由 |
|------|------|------|
| K（候选数） | 8 | ≥ max 可见（avg 4.4, max ≈ 6-7） |
| d（注意力维度） | 64 | 与 FC 最后一层一致 |
| W_q 输入 | 4 维 [l_avg, l_max, l_std, n_svc] | 负载统计 |
| W_K/W_V 输入 | 5 维 [sinr, load, elev, rem_t, is_svc] | 完整卫星特征 |
| FC 层 | 256→128→64 | 与 B2 DDQN 一致 |
| 额外参数 | ~640 | 极轻量 |

### A3.5 DLA 预期行为

- **低负载**：l_avg 低 → 权重趋均匀 → 退化为 SINR 主导
- **高负载**：l_avg 高 → 权重偏向低负载卫星 → 负载均衡优先
- **单星高负载**：l_max 高但 l_avg 低 → 权重回避高负载卫星
- **核心**：DLA 自动在"信号优先"和"负载优先"之间切换，无需显式规则

---

## A4. Top-K 候选压缩分析

### A4.1 当前问题

obs = 396×4 + 1 = 1585 维，有效数据 avg 4.4 颗 × 4 ≈ 18 维，利用率 1.1%。

### A4.2 压缩方案

Top-K obs = K×5 + 1 = 41 维（K=8），压缩 97.4%。

排序准则：score_m = w_s·sinr_norm(m) + w_r·rem_t_norm(m)，取 top-K。**负载不参与排序**（留给 DLA）。

### A4.3 信息损失

| K | 损失 | 理由 |
|---|------|------|
| K≥7 | **零** | 所有可见卫星均包含 |
| K=5 | 低 | 丢弃 0-2 颗最弱候选 |
| K=3 | 中 | 可见 5+ 颗时丢弃排序末尾 |
| K=2 | 高 | 过激进 |

### A4.4 vs Zero-padding

| 维度 | Zero-padding | Top-K |
|------|-------------|-------|
| 有效信息密度 | 55% | 100% |
| FC 浪费 | ~45% | 0% |
| Advantage 偏差 | 含 zero-pad 行 | 无 |
| 可扩展性 | M_max 固定 | K 固定，与星座无关 |

推荐 K=8（零损失 + 与 ARTHF M_max=8 对齐）。

---

## A5. 消融实验设计

### A5.1 实验组

| # | 名称 | Attention | 候选 | RL | 目的 |
|---|------|-----------|------|-----|------|
| A1 | B2 DDQN | 无 | 全量 396×4 | Dueling DDQN | 基线 |
| A2 | Top-K only | 无 | Top-K K=8 | Dueling DDQN | 压缩独立贡献 |
| A3 | Self-Attn+Top-K | Self-attention | Top-K K=8 | Dueling DDQN | ARTHF 风格复现 |
| A4 | DLA+Full | Cross-attention | 全量 396×4 | Dueling DDQN | DLA 独立贡献 |
| A5 | **LA-DDQN** | Cross-attention | Top-K K=8 | Dueling DDQN | **完整方法** |
| A6 | LA-DDQN K=3 | Cross-attention | Top-K K=3 | Dueling DDQN | 激进压缩 |
| A7 | LA-DDQN K=5 | Cross-attention | Top-K K=5 | Dueling DDQN | 中等压缩 |
| A8 | LA-DDQN K=10 | Cross-attention | Top-K K=10 | Dueling DDQN | 宽松压缩 |

+ B1 HHS（传统）+ B4 Random（下界）。

### A5.2 指标

吞吐量、阻塞率、切换次数、Jain 公平指数、训练收敛速度、单步推理时间。

### A5.3 预期排序

```
阻塞率:  B4 < A5 < A3 < A2 < A1 ≈ A4 < B1
吞吐量:  A5 > A3 ≈ A4 > A2 > A1 > B4 > B1
Jain's:  A5 > A4 > A3 > A2 ≈ A1 > B1 >> B4
训练速度: A2 > A5 > A3 > A4 >> A1
```

**核心对比**：A5 vs A3（DLA vs Self-attention）、A5 vs A2（DLA 独立贡献）、A6-A8 vs A5（K 值敏感度）。

---

## A6. 方案 A 贡献可行性评估

### A6.1 贡献强度

| 贡献 | 内容 | 强度 |
|------|------|------|
| 方法论 | Cross-attention 负载驱动 vs Self-attention | **中** |
| 工程 | Top-K 97.4% 降维 + 零损失 | **中低** |
| 实证 | 8 组消融 + 多 baseline | **中** |
| 故事 | "负载驱动的注意力让 DRL 理解负载分布" | **中** |

### A6.2 诚实评估

- **MDPI 级（Electronics, Sensors, IEEE Access）**：可行。差异化清晰，消融全面。
- **IEEE TWC/JSAC 级**：困难。incremental over ARTHF。
- **vs 方案 C**：C 创新性更强（三元组合无人占据），故事更有力，但风险更高。

### A6.3 最终评估

```
方案 A: ★★★☆☆ (3/5)
  创新性: 中 | 风险: 低 | 工作量: 中（2-3周）| 发表: 高(MDPI)/中低(TMC)

方案 C: ★★★★☆ (4/5)
  创新性: 中高 | 风险: 高 | 工作量: 高 | 发表: 取决于 GNN 训练成功
```

**建议**：
- 确保**发表** → 选 A
- **强贡献**且能承受风险 → 选 C
- 时间充裕 → 先 A 保底，C 作为跟进

---

## Size Generalization 方向检索（2026-05-09）

> 方案 A 被消融否定（DLA 无独立贡献），方案 C 在 15 UE 下 GNN 仅 +0.8%。
> 核心贡献需要从"绝对性能提升"转向"可扩展性"。
> 本轮检索确认 size generalization 叙事的新颖性和文献支撑。

### 文献检索

四组系统检索，使用 `v2/tools/literature_search.py`：

| 搜索 | 关键词 | 结果数 | 存档 |
|------|--------|--------|------|
| scale-gnn | "LEO satellite handover GNN graph neural network scalability user" | 30 | contract-scale-gnn.json |
| scale-bipartite | "satellite handover load balancing DRL multi-user bipartite graph" | 30 | contract-scale-bipartite.json |
| size-generalization | "GNN size generalization wireless resource allocation scalable" | 30 | contract-size-generalization.json |
| scale-dense | "LEO NTN handover dense multi-user load-aware neural network" | 30 | contract-scale-dense.json |

### GNN vs MLP 优势阈值（文献证据）

| UE/Agent 规模 | GNN vs MLP | 来源 |
|---------------|-----------|------|
| N ≤ 10 | MLP 够用，GNN 优势有限 | Lee et al. 2023 (Frontiers) |
| 10 < N < 30 | GNN 开始显著优于 MLP | Lee et al. 2023, Shen et al. 2019 |
| N ≥ 30-40 | MLP 可能崩溃，GNN 不可替代 | Lee et al. 2023, Eisen & Ribeiro 2020 |

关键文献：
- **Lee et al. 2023**：多智能体防御，N=2→50 实验数据，N>40 时 MLP 甚至劣于随机
- **Shen et al. 2019 (IGCNet)**：无线功率控制，MLP 在大规模网络性能急剧退化
- **Wu et al. 2022**：GNN size generalization 理论，mean aggregator 的跨规模泛化条件
- **Garcia Camargo et al. 2025**：稀疏随机几何图上的 GNN 可迁移性形式化证明

### 直接竞争者精读（3 篇 P0/P1）

| 论文 | 问题域 | 图结构 | 方法 | 重叠度 |
|------|--------|--------|------|--------|
| Fan et al. 2026 (Springer) | ISL 路由 + 功率控制 | 同构图（卫星-卫星） | GNN + DQN | **低** |
| Jayarajan 2025 (GT 硕士论文) | 卫星-小区-网关分配 | 异构图（3类节点） | GNN + 约束损失（无RL） | **低** |
| Wang et al. 2025 (IEEE ICCC Workshop) | UE-UAV 接入链路切换 | UE-UAV（推测） | GNN + 整数规划 | **低** |

三篇全部不是 UE 粒度的 LEO 卫星切换。问题域、图结构、学习方法均不同。

### 新颖性结论

"**二部图 GNN + DDQN + size generalization + 多 UE 负载均衡切换**"在 LEO 切换领域：
- 无直接竞争者
- Size generalization 在 LEO 切换中完全空白（Jayarajan 做了初步 100→200 但在网络侧分配，非切换）
- "UE 数量对切换算法性能影响"是明确研究空白

### 论文叙事（修订）

从"GNN 消息传递提升性能"转向三步递进：
1. **可行性**：20 UE 下 GNN+top-K ≈ MLP+top-K（基线建立）
2. **Scaling advantage**：50-100 UE 下 MLP 退化，GNN 保持稳定（核心贡献）
3. **Size generalization**：20 UE 训练的 GNN 直接部署到 50/100 UE（工程实用性）
