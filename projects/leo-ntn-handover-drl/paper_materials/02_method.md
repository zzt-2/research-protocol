# 方法架构

## 1. 架构总览

端到端流程分为四个阶段：

1. **环境仿真**：Walker-delta 星座（396 卫星）产生每步的 UE-卫星信道状态（SINR、仰角、负载等）。
2. **Graph Builder**：对每个 UE 按仰角降序取 top-K=6 候选卫星，构建动态二部图 $G_t = (V_{ue}, V_{sat}, E)$。
3. **GNN Encoder**：T=2 层边条件化 MPNN（MPNN-E）对二部图做双向消息传递，输出 UE 嵌入 $h_{ue} \in \mathbb{R}^{64}$、卫星嵌入 $h_{sat} \in \mathbb{R}^{64}$、边嵌入 $h_{edge} \in \mathbb{R}^{32}$。
4. **Dueling Q-Network**：分解式 Q 函数 $Q(UE_i, sat_j) = V(h_{ue_i}) + A(h_{ue_i}, h_{sat_j}, h_{edge_{ij}}) - \text{mean}_j(A)$，经 $\varepsilon$-greedy + 候选 mask 选择动作。

```
[Environment]
     │  每步输出: SINR, elevation, load, ...
     ▼
[Graph Builder]  top-K=6, G_t=(V_ue, V_sat, E)
     │  UE(≤N)×4, Sat(≤N×6)×2, Edge(≤N×6)×3
     ▼
┌──────────────┐
│  GNN Encoder │  T=2 MPNN-E, d=64
│  13,120 params│
└──────┬───────┘
       │  h_ue(N×64), h_sat(≤N×6 ×64), h_edge(≤N×6 ×32)
       ▼
┌──────────────┐
│  Dueling Q   │  分解式: V(s) + A(s,a) - mean(A)
│  12,738 params│
└──────┬───────┘
       │  Q(UE_i, sat_j), j ∈ candidates
       ▼
  [ε-greedy + mask]
       │
       ▼
  [Environment.step()]
```

来源：design_C.md §6；contract.md §GNN+DDQN 架构。

---

## 2. 二部图定义

### 2.1 图结构

每个决策时刻 $t$ 构建动态二部图：

$$G_t = (V_{ue},\ V_{sat},\ E)$$

- $V_{ue}$：所有 UE 节点（数量 $N$，随场景规模可变）
- $V_{sat}$：所有 UE 的 top-K 候选卫星并集（$\leq N \times K$ 个，通常远小于总卫星数 396）
- $E$：UE-sat 可见边（仰角 $\geq 20°$）

**top-K=6 候选选择规则**（来源：D012）：

1. 对每个 $UE_i$，按仰角降序排列所有可见卫星
2. 取前 $K=6$ 个
3. 不足 $K$ 个时用 dummy 边填充（特征全零）
4. $V_{sat}$ 取所有 UE 候选的并集

选择 $K=6$ 的依据：仿真器统计平均 4.4 颗可见卫星，最大 6 颗，$K=6$ 实现零信息损失。

效果：图规模从 396 卫星压缩到 $\leq N \times 6$ 个活跃节点，边数 $\leq N \times 6$。

### 2.2 节点特征表

**UE 节点（dim=4）**：

| # | 名称 | 范围 | 含义 | 设计理由 |
|---|------|------|------|---------|
| 0 | `t_conn_norm` | [0, 1] | 连接时长 / 100 步（cap 1.0） | 编码切换紧急度，连接时间越长切换成本越高 |
| 1 | `sinr_serving` | [0, 1] | 当前服务星的归一化速率 $R_{norm}$ | 当前服务质量，与候选链路比较 |
| 2 | `load_serving` | [0, 1] | 当前服务星的归一化负载 $load_{norm}$ | 服务星负载状态，感知是否过载 |
| 3 | `is_blocked` | {0, 1} | 是否被阻塞 | 阻塞 UE 需优先重连 |

**卫星节点（dim=2）**：

| # | 名称 | 范围 | 含义 | 设计理由 |
|---|------|------|------|---------|
| 0 | `load_norm` | [0, 1+] | 连接 UE 数 / SAT_CAPACITY | 负载感知的核心信号，支持负载均衡决策 |
| 1 | `orbit_phase` | [0, 1] | 轨道相位 | 编码卫星运动趋势，让 GNN 学习"即将离开可见区域"的模式（来源：D014, 消融 A4 验证 -0.4% 影响） |

来源：design_C.md §2.3。

### 2.3 边特征表

**UE-Sat 边（dim=3）**：

| # | 名称 | 范围 | 含义 | 设计理由 |
|---|------|------|------|---------|
| 0 | `sinr_norm` | [0, 1] | 链路归一化速率 $R_{norm}$ | 链路质量主信号，直接决定吞吐量 |
| 1 | `elev_norm` | [0, 1] | $(elev - elev_{min}) / (90 - elev_{min})$ | 仰角越高链路越稳定、持续时间越长 |
| 2 | `is_current` | {0, 1} | 是否当前服务链路 | 编码切换成本——保持当前连接 vs 切换新卫星 |

链路质量（SINR + 仰角）是切换决策的**主要信息源**，这也是选择 MPNN-E（原生支持边特征）的核心动因。

来源：design_C.md §2.4；D010。

### 2.4 观测空间对比

| 维度 | B2（flat obs） | C（bipartite graph） |
|------|----------------|---------------------|
| UE 特征 | 1（`t_conn`） | 4 维节点特征 |
| 卫星特征 | 396×3（全量零填充） | $\leq N \times 6 \times 2$（仅活跃） |
| 连接标记 | 396×1 | 边级 `is_current` |
| **总有效维度** | **1585**（信息密度 1.1%） | **$N \times (4 + 6 \times 2 + 6 \times 3) = 34N$** |
| 信息密度 | 极低（99% 零填充） | 高（仅活跃节点） |
| 规模可扩展性 | 固定维度，不可扩展 | 随 UE 数量线性增长，天然支持 size generalization |

来源：design_C.md §2.5；D029。

---

## 3. MPNN-E 消息传递

### 3.1 层选型对比

| 维度 | GCN | GAT | **MPNN-E（选定）** |
|------|-----|-----|-------------------|
| 边特征支持 | 不支持 | 标准版不支持 | **原生支持** |
| 邻居权重 | 均等 | 学习注意力权重 | 学习消息函数 |
| 参数量 | 少 | 中 | 中 |
| 训练稳定性 | 高 | 中 | 中（需 LayerNorm） |
| 切换场景适配 | 差（忽略 SINR/仰角） | 中（注意力间接学习） | **好（边特征直接进消息）** |
| 文献支撑 | 通用图学习 | 通用图学习 | Yu et al. 卫星切换验证 |

选择理由：边特征（SINR, elevation）是切换决策的主要信息源，GCN/GAT 标准版无法原生利用；MPNN 消息函数天然接收边特征，无需额外适配。

来源：D010。

### 3.2 消息传递公式

二部图双向传递，每层分两步。使用 $\mathbf{h}$ 表示节点嵌入，$\mathbf{e}$ 表示边特征，$\mathcal{N}$ 表示邻居集合。

**Step 1: UE → Sat**

消息函数（拼接源节点、目标节点、边特征后通过 MLP）：

$$\mathbf{m}_{ue_i \to sat_j} = \text{MLP}_{msg\_ue}\!\Big(\big[\,\mathbf{h}_{ue_i}\ \|\ \mathbf{h}_{sat_j}\ \|\ \mathbf{e}_{ij}\,\big]\Big) \quad (4+2+3=9 \to 32)$$

聚合（对所有以 $sat_j$ 为目标的 UE 取均值）：

$$\bar{\mathbf{m}}_{sat_j} = \frac{1}{|\mathcal{N}_{ue}(sat_j)|} \sum_{i \in \mathcal{N}_{ue}(sat_j)} \mathbf{m}_{ue_i \to sat_j}$$

更新 + 残差 + LayerNorm：

$$\hat{\mathbf{h}}_{sat_j} = \text{LayerNorm}\!\Big(\mathbf{h}_{sat_j} + \text{MLP}_{update\_sat}\!\Big(\big[\,\mathbf{h}_{sat_j}\ \|\ \bar{\mathbf{m}}_{sat_j}\,\big]\Big)\Big) \quad (2+32=34 \to 2)$$

**Step 2: Sat → UE**

消息函数：

$$\mathbf{m}_{sat_j \to ue_i} = \text{MLP}_{msg\_sat}\!\Big(\big[\,\hat{\mathbf{h}}_{sat_j}\ \|\ \mathbf{h}_{ue_i}\ \|\ \mathbf{e}_{ij}\,\big]\Big) \quad (2+4+3=9 \to 32)$$

聚合：

$$\bar{\mathbf{m}}_{ue_i} = \frac{1}{|\mathcal{N}_{sat}(ue_i)|} \sum_{j \in \mathcal{N}_{sat}(ue_i)} \mathbf{m}_{sat_j \to ue_i}$$

更新 + 残差 + LayerNorm：

$$\mathbf{h}_{ue_i}' = \text{LayerNorm}\!\Big(\mathbf{h}_{ue_i} + \text{MLP}_{update\_ue}\!\Big(\big[\,\mathbf{h}_{ue_i}\ \|\ \bar{\mathbf{m}}_{ue_i}\,\big]\Big)\Big) \quad (4+32=36 \to 4)$$

**T=2 层**：Step 1 + Step 2 重复执行 2 次。L15 验证 T=2 足够，消融 A3 确认 T=2 比 T=1 多 +1.8%（来源：D023）。

可选增强：残差投影到 $d=64$ 维增加表达能力：

$$\mathbf{h}_{ue}' = \text{LayerNorm}\!\Big(\text{MLP}_{project}(\mathbf{h}_{ue}) + \text{MLP}_{update}(\bar{\mathbf{m}})\Big)$$

最终 UE 嵌入维度为 64。

来源：design_C.md §3.3。

### 3.3 维度设计表

| MLP | 输入维度 | 隐层维度 | 输出维度 | 说明 |
|-----|---------|---------|---------|------|
| `MLP_msg_ue` | 9 | 32 | 32 | 拼接 $[h_{ue}\|h_{sat}\|e_{ij}]$ |
| `MLP_update_sat` | 34 | 32 | 2 | 拼接 $[h_{sat}\|\bar{m}]$ |
| `MLP_msg_sat` | 9 | 32 | 32 | 拼接 $[\hat{h}_{sat}\|h_{ue}\|e_{ij}]$ |
| `MLP_update_ue` | 36 | 32 | 4 | 拼接 $[h_{ue}\|\bar{m}]$ |

来源：design_C.md §3.4。

---

## 4. 分解式 Dueling Q 函数

### 4.1 动机

标准 Dueling DDQN 对每个 UE 输出 $|A|=396$ 个 Q 值（每颗卫星一个），输出层参数量巨大（$\sim$490K），且 99% 的动作为无效卫星（不在可见范围内）。即使使用 Q mask 将无效动作设为 $-\infty$，探索效率仍然极低。

分解式 Q 函数将 $Q(UE_i, sat_j)$ 拆解为状态价值 $V$ 和卫星选择优势 $A$，利用 GNN 已有的结构化嵌入，将输出维度从 396 降至 top-K 个候选。

来源：D011。

### 4.2 公式

$$Q(UE_i, sat_j) = V(\mathbf{h}_{ue_i}) + A(\mathbf{h}_{ue_i},\ \mathbf{h}_{sat_j},\ \mathbf{h}_{edge_{ij}}) - \frac{1}{|\mathcal{J}_i|} \sum_{j \in \mathcal{J}_i} A(\mathbf{h}_{ue_i},\ \mathbf{h}_{sat_j},\ \mathbf{h}_{edge_{ij}})$$

其中 $\mathcal{J}_i$ 为 $UE_i$ 的候选卫星集合（$\leq K$ 个）。

- **$V(\mathbf{h}_{ue_i})$**：状态价值网络 `MLP_v`，仅依赖 UE 嵌入，输出标量。架构：$64 \to 64 \to 1$。
- **$A(\mathbf{h}_{ue_i}, \mathbf{h}_{sat_j}, \mathbf{h}_{edge_{ij}})$**：优势网络 `MLP_a`，拼接三方嵌入后输出标量。架构：$(64+64+32)=160 \to 64 \to 1$。

减去 $\text{mean}_j(A)$ 是标准 Dueling 技巧，确保 $V$ 和 $A$ 的可辨识性。

来源：design_C.md §4.1；contract.md §GNN+DDQN 架构。

### 4.3 动作空间对比

| 属性 | B2（flat 396-action） | C（top-K ≤7） |
|------|----------------------|--------------|
| 动作空间大小 | 396 | $\leq K+1=7$（top-K + 保持当前） |
| 有效动作比例 | ~1.1%（avg 4.4 可见 / 396） | **~100%** |
| 无效动作处理 | Q mask 设 $-\infty$ | 自然排除（不在候选集中） |
| 探索效率 | 低 | **高** |
| 50+ UE 可行性 | CUDA 崩溃（D031） | 正常运行 |

来源：design_C.md §4.4；D031。

---

## 5. top-K 候选压缩

**排序准则**：对每个 UE 按仰角（elevation）降序排列所有可见卫星，取前 $K$ 个。

**K=6 选择理由**（来源：D012）：
- 仿真器统计：平均 4.4 颗可见卫星，最大 6 颗
- $K=6$ 覆盖全部可见卫星，**零信息损失**
- 图规模可控：$N \times 6$ 条边（15 UE → 90 条边）

**不足 K 个的处理**：用 dummy 边填充（特征全零），保持批处理维度一致。

**与 zero-padding 方案（B2）对比**：

| 维度 | B2 zero-padding | C top-K |
|------|----------------|---------|
| 填充对象 | 全部 396 卫星，零填充不可见卫星 | 仅活跃候选，不足 K 个时填充 dummy |
| 填充比例 | ~99% | ~0%（极少不足 K 的情况） |
| 计算浪费 | FC 层在零填充维度上做无效计算 | GNN 仅在活跃边上传递消息 |
| Dueling advantage 中心化 | 受 zero-pad 影响（数值偏差） | 不受影响（均值仅在实际候选上计算） |

来源：D012；design_C.md §2.2。

---

## 6. 两阶段训练策略

### Phase 1: GNN 预训练

- **目标**：监督学习训练 GNN 编码器，使其学会负载相关编码
- **辅助任务 1**：预测每个 UE 下一步是否被阻塞（二分类，BCE loss）
- **辅助任务 2**：预测每个卫星下一步负载变化（回归，MSE loss）
- **损失函数**：

$$\mathcal{L}_{aux} = \text{BCE}(block\_pred,\ block\_true) + \text{MSE}(\Delta load\_pred,\ \Delta load\_true)$$

- **训练量**：约 50 episodes，约 30 分钟
- **优化器**：Adam, lr=$10^{-3}$

目的：避免 DRL 初期收到 GNN 噪声编码，强制 GNN 先学会编码负载相关信息。

来源：D013；design_C.md §5.1。

### Phase 2: 联合 GNN + DRL 训练

| 超参数 | 值 | 说明 |
|--------|-----|------|
| GNN 学习率 | $10^{-4}$ | 10× 小于 DRL，保护预训练编码 |
| DRL 学习率 | $10^{-3}$ | 来源：contract.md 最佳配置 |
| Discount factor $\gamma$ | 0.99 | |
| Replay buffer | 200K | 50+ UE 需要（D027 验证） |
| Batch size | 128 | |
| GNN 梯度裁剪 | max_norm = 0.5 | |
| 全局梯度裁剪 | max_norm = 1.0 | |
| Target network 更新 | 每 3000 步 | |
| $\varepsilon$-greedy | $1.0 \to 0.01$ 指数衰减 | eps_decay=40 |
| 训练 episodes | 100（50+ UE）/ 50（15-20 UE） | |
| 评估 seeds | 3（100, 200, 300） | |

来源：D013；contract.md §GNN+DDQN 架构；D027（buffer 扩大）。

---

## 7. 设计决策记录

| 决策编号 | 选择 | 理由 | 排除的替代方案 |
|---------|------|------|--------------|
| D010 | 边条件化 MPNN（MPNN-E）作为 GNN 层 | 边特征（SINR, elevation）是切换决策的主要信息源，GCN/GAT 原生不支持 | GCN（忽略边特征）、GAT（需魔改才能加入边条件化注意力） |
| D011 | 分解式 Q 函数 | 参数量 12,738 vs flat Q ~490K；天然支持变长候选集；是 MPNN 边级嵌入到动作空间的最直接映射 | Flat 396-action Q（输出层巨大）、Per-UE 独立 Q 网络 |
| D012 | top-K=6 候选压缩 | 仿真统计 avg 4.4 可见卫星，K=6 零信息损失；396→6 使图规模可控 | Zero-padding 到固定 N（浪费计算，Dueling advantage 中心化偏差） |
| D013 | 两阶段训练 | 缓解 GNN+DRL 联合训练不稳定风险（R5）；预训练强制 GNN 学会负载相关编码 | 端到端直接训练（GNN 初期噪声编码导致 DRL 不稳定） |
| D014 | 方案 C（GNN+DRL）作为主攻 | 新颖性优势（三元组合无人占据）；故事更清晰；参数效率 25,858 vs 490,125；top-K 从方案 A 并入 | 方案 A LA-DDQN（与 ARTHF 差异窄，D021 验证 DLA 无效后方案 A 死亡） |
| D025 | Contract 叙事转向 size generalization | 三阶段递进：(1) 20 UE 基线 GNN≈MLP，(2) 50-100 UE GNN>>MLP，(3) 小规模训练直接大规模部署 | "GNN 提升绝对性能"叙事（15 UE 下 GNN 仅 +0.8%，不够显著） |

来源：decision_log.md D010-D014, D025。

---

## 8. 参数量分解

| 组件 | 参数量 | 说明 |
|------|--------|------|
| GNN Encoder | 13,120 | 4 个小 MLP + LayerNorm，参数在所有 UE/sat 对间共享（源码实测） |
| `MLP_v`（状态价值） | 4,225 | $64 \to 64 \to 1$ |
| `MLP_a`（优势） | 8,513 | $(64+64+3)=131 \to 64 \to 1$ |
| **C 总计** | **25,858** | |
| **B2 DDQN（对比）** | **~490K** | $1585 \times 256 + 256 \times 128 + 128 \times 396$（含偏置 = 490,125） |
| **压缩比** | **19×** | |

参数效率来源：(1) GNN 参数在所有 UE/sat 对间**共享**（permutation equivariance），(2) 分解式 Q 避免了 396 维巨大输出层。

来源：design_C.md §4.3。

---

## 9. 训练不稳定风险缓解

| ID | 风险 | 严重度 | 缓解措施 |
|----|------|--------|---------|
| R1 | 过平滑（over-smoothing） | 低 | T=2 层，L15 已验证足够；消融 A3 确认 T=2 比 T=1 多 +1.8% |
| R2 | 拓扑非平稳（卫星进出可见域导致图结构剧变） | 高 | 每步重建图；`orbit_phase` 提供位置连续性 |
| R3 | 梯度爆炸/消失 | 中 | LayerNorm + 残差连接 + 梯度裁剪（GNN max_norm=0.5，全局 max_norm=1.0） |
| R4 | 多 UE 信用分配（联合决策中难以归属贡献） | 中 | 分解式 Q 隔离每个 UE-sat 对的贡献 |
| R5 | GNN+DRL 联合训练不稳定 | 高 | 两阶段训练 + 差异化学习率（GNN $10^{-4}$ vs DRL $10^{-3}$） |
| R6 | 小图过拟合 | 中 | 参数共享 + LayerNorm 正则化 |

来源：design_C.md §5.2。

---

## 10. 与 Baseline 的代码复用

| 模块 | 复用程度 | 说明 |
|------|---------|------|
| 仿真器 | 100% | Walker-delta 星座、信道模型完全复用 |
| 奖励函数 | 100% | $w_r \cdot R_{norm} + w_l \cdot L_{norm} - w_b \cdot B - w_h \cdot H$ |
| Experience replay | 100% | Buffer + 采样逻辑完全复用 |
| $\varepsilon$-greedy 调度 | 100% | 衰减策略复用 |
| Q-network（Dueling 部分） | 部分 | $V(s)$ 复用 Dueling 结构，$A(s,a)$ 改为分解式 |
| GNN 编码器 | **新增** | MPNN-E 编码器，13,120 参数 |
| Graph builder | **新增** | top-K 候选选择、二部图构建 |
| 预训练循环 | **新增** | Phase 1 监督学习循环 |

来源：design_C.md §6。
