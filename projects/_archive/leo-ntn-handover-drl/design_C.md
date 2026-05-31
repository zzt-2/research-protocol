# 方案 C 技术设计：二部图 GNN + DRL 切换优化

> 2026-05-08，Contract 阶段设计文档。
> 基于 Yu et al. (2024, MDPI Aerospace) 和 Lee et al. / L15 (2025, ICT Express) 精读缓存完成。

---

## 1. 竞争者定位

### 1.1 Yu et al. (2024) — 有向切换图 + 边级 MPNN + DQN

| 模块 | 设计 |
|------|------|
| 图结构 | 有向图（卫星间切换路径），非二部图 |
| 消息传递 | 边级 MPNN：M(h_edge_i, h_edge_j)，RNN 更新 |
| DRL | DQN（非 Dueling），单用户 |
| 候选处理 | 零填充到固定 N |
| 奖励 | AHP 固定权重 [rate=0.58, delay=0.11, service_time=0.31] |
| 场景 | 15 星，电力巡检单用户 |

**与方案 C 的差异**：有向图（非二部图）、边级传递（非节点级）、单用户、RNN 更新。重叠度低。

### 1.2 Lee et al. / L15 (2025) — 二部图 + FCN 消息传递 + Softmax

| 模块 | 设计 |
|------|------|
| 图结构 | UE-卫星二部图 |
| 消息传递 | T=2，sat→UE / UE→sat 各用独立 FCN |
| 决策 | Softmax 选星（**无 DRL**） |
| 负载控制 | 卫星侧 ACK 硬决策 |
| 训练 | Adam lr=1e-5, 70 episodes, batch=4 |
| 规模 | 1584 星 / 50 UE |

> ⚠ L15 全文获取失败（ScienceDirect 403），以上基于摘要+片段。隐藏维度、FCN 层数等细节未知。

**与方案 C 的差异**：无 DRL（纯 softmax）、无 reward-based 长期优化、ACK 硬决策替代学习型负载均衡。重叠度中等。

### 1.3 空隙确认

| 组合要素 | Yu et al. | L15 | 方案 C |
|----------|-----------|-----|--------|
| 二部图 | ✗ | ✓ | ✓ |
| GNN 编码 | ✓ MPNN | ✓ FCN | ✓ MPNN-E |
| DRL 决策 | ✓ DQN | ✗ softmax | ✓ Dueling DDQN |
| 多 UE 联合负载均衡 | ✗ | ✓ | ✓ |
| Reward-based 学习 | ✓ | ✗ | ✓ |

**"二部图 GNN + DRL + 多 UE 联合负载均衡"三元组合无人占据。**

---

## 2. 二部图结构设计

### 2.1 图定义

每步决策时刻 t 构建动态二部图 G_t = (V_ue, V_sat, E)：

- **V_ue**：15 个 UE 节点（固定）
- **V_sat**：所有 UE 的 top-K=6 候选卫星并集（≤90 个，通常 20-40）
- **E**：UE-sat 可见边（elevation ≥ 20°）

### 2.2 top-K 候选选择

1. 对每个 UE，按 elevation 降序排列所有可见卫星
2. 取前 K=6 个（仿真器统计：avg 4.4 可见，max 6，K=6 零信息损失）
3. 不足 K 个时，用 dummy 边填充（特征全零）
4. V_sat 取所有 UE 候选的并集

**效果**：图规模从 396 卫星压缩到 ≤90 个活跃节点，边数 ≤90（15 UE × 6 候选）。

### 2.3 节点特征

**UE 节点（dim=4）**：

| # | 名称 | 范围 | 含义 |
|---|------|------|------|
| 0 | t_conn_norm | [0,1] | 连接时长 / 100 步（cap 1.0） |
| 1 | sinr_serving | [0,1] | 当前服务星的 R_norm |
| 2 | load_serving | [0,1] | 当前服务星的 load_norm |
| 3 | is_blocked | {0,1} | 是否被阻塞 |

**卫星节点（dim=2）**：

| # | 名称 | 范围 | 含义 |
|---|------|------|------|
| 0 | load_norm | [0,1+] | 连接 UE 数 / SAT_CAPACITY |
| 1 | orbit_phase | [0,1] | 轨道相位（编码运动趋势） |

orbit_phase 让 GNN 学习"即将离开可见区域"的模式，这是 flat observation 无法自然编码的信息。

### 2.4 边特征

**UE-Sat 边（dim=3）**：

| # | 名称 | 范围 | 含义 |
|---|------|------|------|
| 0 | sinr_norm | [0,1] | 链路归一化速率 R_norm |
| 1 | elev_norm | [0,1] | (elev - min_elev) / (90 - min_elev) |
| 2 | is_current | {0,1} | 是否当前服务链路 |

链路质量（SINR + 仰角）是切换决策的**主要信息源**。is_current 编码切换成本。

### 2.5 与 B2 flat obs 对比

| 维度 | B2 | C |
|------|-----|---|
| UE 特征 | 1 (t_conn) | 4 维节点特征 |
| 卫星特征 | 396×3 (全量零填充) | ≤90×2 (仅活跃) |
| 连接标记 | 396×1 | 边级 is_current |
| 总有效维度 | 1585 | 352 |
| 信息密度 | 1.1% | 高 |

---

## 3. GNN 层选型

### 3.1 候选对比

| 维度 | GCN | GAT | MPNN-E（选定） |
|------|-----|-----|---------------|
| 边特征 | ✗ | ✗ 标准版 | ✓ 原生 |
| 邻居权重 | 均等 | 学习注意力 | 学习消息函数 |
| 参数量 | 少 | 中 | 中 |
| 训练稳定性 | 高 | 中 | 中（需 LayerNorm） |
| 切换场景适配 | 差（忽略 SINR/elev） | 中（注意力间接学习） | **好（边特征直接进消息）** |
| 文献支撑 | 通用 | 通用 | Yu et al. 验证 |

### 3.2 选定：边条件化 MPNN（MPNN-E）

**理由**：边特征（SINR, elevation）是切换决策的主要信息源。GCN/GAT 标准版无法原生利用边特征；GAT 需要魔改才能加入边条件化注意力。MPNN 消息函数天然接收边特征，无需额外适配。

### 3.3 消息传递规则

二部图双向传递，每层分两步：

**Step 1: UE → Sat**
```
m_{ue_i→sat_j} = MLP_msg_ue([h_ue_i || h_sat_j || e_ij])    // (4+2+3)=9 → 32
h_sat_j' = MLP_update_sat([h_sat_j || mean({m_{ue→sat_j}})]) // (2+32)=34 → 2
h_sat_j' = LayerNorm(h_sat_j + h_sat_j')                      // 残差 + 归一化
```

**Step 2: Sat → UE**
```
m_{sat_j→ue_i} = MLP_msg_sat([h_sat_j' || h_ue_i || e_ij])  // (2+4+3)=9 → 32
h_ue_i' = MLP_update_ue([h_ue_i || mean({m_{sat→ue_i}})])    // (4+32)=36 → 4
h_ue_i' = LayerNorm(h_ue_i + h_ue_i')                         // 残差 + 归一化
```

**T=2 层**：重复 Step 1+2 共 2 次（L15 验证 T=2 足够，过平滑风险低）。

### 3.4 维度设计

| MLP | 输入 | 隐层 | 输出 |
|-----|------|------|------|
| MLP_msg_ue | 9 | 32 | 32 |
| MLP_update_sat | 34 | 32 | 2 |
| MLP_msg_sat | 9 | 32 | 32 |
| MLP_update_ue | 36 | 32 | 4 |

GNN 后 UE 节点嵌入维度仍为 4（原始维度），但编码了邻居信息。

**可选增强**：残差投影到 d=64 维增加表达能力：
```
h_ue' = LayerNorm(MLP_project(h_ue) + MLP_update(AGG(messages)))
```
最终 UE 嵌入为 64 维。参数量增加 ~4×64 = 256，可控。

---

## 4. GNN → DRL 接口

### 4.1 分解式 Q 函数

标准 Dueling DDQN 输出 |A|=396 个 Q 值，输出层巨大。

方案 C 采用分解式 Q 函数：
```
Q(UE_i, sat_j) = V(h_ue_i) + A(h_ue_i, h_sat_j, h_edge_ij) - mean_j(A(i,j))
```

- **V(h_ue_i)**：状态价值，仅依赖 UE 嵌入（全局视角）
- **A(UE_i, sat_j)**：卫星选择优势，依赖 UE + 卫星 + 链路三方嵌入

### 4.2 网络架构

```
输入：二部图 G_t
  │
  ├──→ [GNN Encoder, T=2 MPNN-E]
  │      → h_ue_i ∈ R^64    (per UE)
  │      → h_sat_j ∈ R^64   (per visible sat)
  │      → h_edge_ij ∈ R^32 (per UE-sat edge)
  │
  └──→ [Dueling Q-Network]
         V(h_ue) = MLP_v(h_ue) → scalar
         A(ue, sat, edge) = MLP_a([h_ue || h_sat || h_edge]) → scalar
         Q(i,j) = V(i) + A(i,j) - mean_j(A(i,j))
  │
  └──→ [Action Selection]
         mask: 仅 visible satellites
         action_i = argmax_{j ∈ visible} Q(i,j)    // ε-greedy
```

### 4.3 参数量估算

| 网络 | 参数量 | 说明 |
|------|--------|------|
| B2 DDQN (对比) | ~712K | 1585×256 + 256×128 + 128×396 |
| C MLP_v | ~4K | 64→64→1 |
| C MLP_a | ~10K | (64+64+32)→64→1 |
| C GNN | ~15K | 4 个小 MLP + LayerNorm |
| **C 总计** | **~29K** | **比 B2 少 25×** |

参数效率来源：GNN 参数在所有 UE/sat 对间**共享**，分解式 Q 避免了巨大输出层。

### 4.4 动作空间

| 属性 | B2 | C |
|------|-----|---|
| 动作空间大小 | 396 | ≤7 (top-K + 保持当前) |
| 无效动作处理 | Q mask -∞ | 自然排除（不在候选集） |
| 探索效率 | 低 | **高** |

---

## 5. 训练策略

### 5.1 两阶段训练

**Phase 1 — GNN 预训练**（~50 episodes, ~30 min）

- 目标：监督学习训练 GNN 编码器
- 辅助任务 1：预测每个 UE 下一步是否被阻塞（二分类，BCE）
- 辅助任务 2：预测每个卫星下一步负载变化（回归，MSE）
- 损失：L_aux = BCE(block_pred, block_true) + MSE(Δload_pred, Δload_true)
- 优化器：Adam lr=1e-3

目的：强制 GNN 学会编码负载相关信息，避免 DRL 初期收到噪声编码。

**Phase 2 — 联合 GNN + DRL 训练**（~300 episodes, ~12h）

- GNN lr = 1e-4（10× 小于 DRL），DRL lr = 1e-3
- DDQN 框架 + experience replay（复用 B2 的 buffer/batch 设计）
- GNN 梯度裁剪：max_norm = 0.5
- 全局梯度裁剪：max_norm = 1.0
- Target network 更新频率：每 1000 步
- ε-greedy：1.0 → 0.01 指数衰减
- Discount factor γ = 0.99

### 5.2 GNN 训练不稳定风险缓解

| ID | 风险 | 严重度 | 缓解措施 |
|----|------|--------|---------|
| R1 | 过平滑 | 低 | T=2 层，L15 已验证 |
| R2 | 拓扑非平稳 | 高 | 每步重建图；orbit_phase 提供位置连续性 |
| R3 | 梯度爆炸/消失 | 中 | LayerNorm + 残差 + 梯度裁剪 |
| R4 | 多 UE 信用分配 | 中 | 分解式 Q 隔离每个 UE-sat 对的贡献 |
| R5 | GNN+DRL 联合不稳定 | 高 | 两阶段训练 + 差异化学习率 |
| R6 | 小图过拟合 | 中 | 参数共享 + LayerNorm 正则化 |

### 5.3 消融实验设计

| # | 名称 | 变量 | 目的 |
|---|------|------|------|
| C1 | C-full | 完整方案 | 主结果 |
| C2 | C-no-pretrain | 跳过 Phase 1 | 验证预训练价值 |
| C3 | C-T1 | T=1 层 | 验证消息传递深度 |
| C4 | C-no-orbit | 去掉 orbit_phase | 验证轨道编码价值 |
| C5 | C-gat | 替换为 GAT-E | 对比 GNN 层类型 |
| C6 | B2-topK | B2 + top-K 压缩 | 隔离 top-K vs GNN 贡献 |

+ B1 HHS（传统）+ B2 DDQN（DRL baseline）+ B4 Random（下界）。

**核心对比**：C1 vs C2（预训练）、C1 vs C3（GNN 深度）、C1 vs C6（GNN 整体贡献）。

---

## 6. 完整架构总览

```
[Environment] ──每步──→ [Graph Builder]
                           │
                    top-K=6 二部图
                    UE(15)×4, Sat(≤90)×2, Edge(≤90)×3
                           │
                    ┌──────▼──────┐
                    │  GNN Encoder │  T=2 MPNN-E, d=64
                    │  Phase 1 预训练│  ~15K params
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
| Q-network | V(s) 复用 Dueling | 分解式 A(s,a) |
| GNN 编码器 | — | 新增 ~15K params |
| Graph builder | — | 新增 |
| 预训练循环 | — | 新增 |

---

## 7. 贡献评估

### 7.1 贡献清单

| # | 贡献 | 类型 | 强度 |
|---|------|------|------|
| 1 | 二部图 + MPNN-E 编码 UE-卫星负载竞争 | 方法论 | **中高** |
| 2 | 分解式 Q 函数适配变长候选集 | 方法论 | **中** |
| 3 | 两阶段训练（GNN 预训练 + DRL 联合） | 工程方法 | **中** |
| 4 | 29K vs 712K 参数效率 + 可扩展性 | 实证 | **中** |
| 5 | top-K 候选压缩 + GNN 图构建 | 工程 | **中低** |

### 7.2 论文叙事

> "Flat observation 将 UE-卫星关系展平为向量，丢失了结构化的负载竞争信息。二部图 GNN 通过消息传递让 UE 自然感知邻居卫星的负载状态，使 DRL 做出负载均衡的切换决策。分解式 Q 函数使参数量从 712K 降至 29K，天然支持变长候选集和星座规模扩展。"

### 7.3 目标期刊

| 级别 | 期刊 | 可行性 |
|------|------|--------|
| MDPI | Sensors, Aerospace, Electronics | 高 |
| IEEE | Access, TVT, TMC | 中高 |
| IEEE 顶刊 | TWC, JSAC | 中低（需 GNN 训练稳定 + 显著优于 B2） |

### 7.4 风险评估

- **主风险**：GNN 训练不稳定导致性能不如 B2 baseline
- **缓解**：两阶段训练 + 消融实验量化各组件贡献
- **退路**：方案 A（LA-DDQN）设计已就绪，可降级

---

## 8. 与方案 A 对比

| 维度 | A: LA-DDQN | C: GNN+DRL |
|------|-----------|-----------|
| **新颖性** | 中（ARTHF 覆盖三要素） | **中高**（三元组合无人占据） |
| 实现复杂度 | 中 | 高 |
| 训练稳定性 | 低 | 中（两阶段缓解） |
| 参数量 | ~712K | **~29K（25× 少）** |
| 故事清晰度 | 中（需解释与 ARTHF 差异） | **高**（"结构化图编码 → 负载感知决策"） |
| 可扩展性 | 低（固定 obs） | **高**（图大小可变，可迁移） |
| 预期训练时间 | ~10h | ~12h（+30min 预训练） |
| 发表风险 | 低（保底 MDPI） | 中（依赖 GNN 训练成功） |

### 最终推荐：方案 C 主攻，方案 A 备选

1. **新颖性优势**：三元组合在文献中无竞争者
2. **故事更有力**：结构化图编码 → 负载感知决策，叙事弧线完整
3. **参数效率**：29K vs 712K，支持可扩展性叙事
4. **方案 A 的 top-K 可并入 C**：不丢失 A 的工程优点
5. **风险可控**：两阶段训练 + T=2 + 残差 + LayerNorm，消融实验可回退定位
