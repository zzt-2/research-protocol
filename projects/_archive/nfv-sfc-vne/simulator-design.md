# 仿真器设计规格 — nfv-sfc-vne

> GW Step 6 产出 | 待用户确认后进入 Step 7

## 1. 扩展策略

**基于 Virne 仿真器扩展**，不自建。原因：
- Virne 已提供完整的 VNE gym-style 环境、47 个 solver、标准化评估流程
- B1-B5 全部 Virne 内置，零自实现成本
- MVE 已验证 Virne 在 RTX 4070 上可用（GRC 21s, pg_mlp ~170s/ep, DualGAT+ ~412s/ep）

扩展方式：在 `virne/` 目录内新增模块，不修改核心代码（仅注册新组件）。

```
projects/nfv-sfc-vne/Virne/
├── virne/
│   ├── network/
│   │   ├── virtual_network.py          # 不改，通过子类扩展
│   │   └── sfc/                        # 新增：SFC 数据模型和生成器
│   │       ├── sfc_chain.py            # SFC DAG 数据结构
│   │       └── sfc_vnr_generator.py    # SFC VNR 生成器
│   ├── solver/
│   │   └── learning/
│   │       └── matching_gnn/           # 新增：matching-style GNN solver
│   │           ├── matching_policy.py  # cross-graph matching encoder
│   │           └── sfc_solver.py       # SFC-aware solver 注册
│   └── ...
└── settings/
    └── sfc_setting.yaml                # 新增：SFC 配置
```

---

## 2. SFC 数据模型

> **关键设计决策**：VNR 拓扑保持 random graph（与 MVE 一致），SFC 约束作为叠加层。
> 不采用纯 chain 拓扑，因为 chain 结构过于简单（无拓扑复杂度），GNN 优势会消失（B3 模式）。

### 2.1 SFC 约束叠加模型

VNR 保持 Virne 原有的 random graph 拓扑，在此基础上叠加 SFC 约束：

- **VNR 图结构**：random (Erdos-Renyi, p=0.5)，与 Virne 默认一致
- **SFC 叠加**：VNR 中一部分节点被标记为 SFC VNF，具有功能类型和顺序约束
- **非 VNF 节点**：普通计算/存储节点，无顺序约束

示例：8 节点 random graph，其中 4 个组成 SFC 链（firewall→NAT→IDS→proxy），其余 4 个为普通节点。

| 属性 | 说明 | 来源 |
|------|------|------|
| sfc_ratio | SFC VNF 占 VNR 总节点比例 | 默认 0.6 |
| vnf_types | 每个 VNF 的功能类型 | 从预定义 VNF 池采样 |
| sfc_chain | 有序 VNF 节点 ID 列表 | 按拓扑序从 VNR 中选取 |
| sfc_edges | SFC 相邻 VNF 间的链路 | VNR 图中对应的边 |

### 2.2 VNR 结构对比

| 属性 | 原始 Virne VNR | SFC-enhanced VNR（本设计） |
|------|---------------|--------------------------|
| 拓扑 | random (Erdos-Renyi, p=0.5) | **相同**（random graph） |
| 节点属性 | cpu: U[0,20] | cpu: U[0,20] + **vnf_type: int** (0=非VNF, 1..N=VNF) |
| 链路属性 | bw: U[0,50] | bw: U[0,50] + **is_sfc_link: bool** |
| 图级属性 | 无 | **sfc_chain: ordered list of VNF node IDs** |

### 2.3 约束类型

1. **资源约束**：同原始 Virne（节点 CPU、链路带宽）
2. **VNF 顺序约束**（新增）：SFC 链中 vnf_i 必须在 vnf_{i-1} 之后放置，且物理路径可达
3. **链路延迟约束**（可选）：SFC 链中相邻 VNF 间的端到端延迟不超过阈值
4. **非 VNF 节点**：无额外约束，按原始 Virne 规则放置

---

## 3. 模块清单

### M1: SFC-enhanced VNR 生成器

- **功能**：在 Virne 原有 random graph VNR 基础上叠加 SFC 约束层
- **实现**：继承 Virne VirtualNetwork，生成流程：(1) 生成 random graph（复用 Virne），(2) 随机选取 sfc_ratio 比例的节点标记为 VNF，(3) 按 SFC 链顺序标注 vnf_type
- **配置**：sfc_ratio=0.6、vnf_type 池大小=5、延迟阈值
- **引用**：L01 Virne (VNR 生成器) + L12 CONAL (约束建模)

### M2: SFC 约束环境

- **功能**：在 Virne InstanceRLEnv 基础上加入 SFC 约束
- **实现**：继承 `JointPRStepInstanceRLEnv`，重写：
  - `generate_action_mask()`: 对 SFC VNF 节点加入可达性约束（当前 VNF 必须能到达已放置的上一个 VNF）；非 VNF 节点保持原始 action mask
  - 节点排序：SFC VNF 节点按 SFC 拓扑序优先，非 VNF 节点按 node_ranking_method
- **引用**：L12 CONAL (CMDP 约束建模) + L01 Virne (JointPR 环境)
- **关键设计**：
  - 环境对**所有** solver 强制 SFC 约束（通过 action masking），确保公平对比
  - Baseline solver 不感知 SFC 结构（不做 SFC 特征输入），仅通过 action mask 被动遵守
  - Our method 通过 GNN 编码 SFC 链结构（vnf_type + 位置编码），主动利用 SFC 信息做更好决策
  - 非 VNF 节点无额外约束，保留了原始 VNE 问题的复杂度

### M3: Matching-style GNN Policy

- **功能**：Node-Edge 联合嵌入的跨图 matching GNN encoder
- **实现**：替换 Virne BiGnnBaseModel，核心架构：
  1. **双图独立编码**：p_net_encoder + v_net_encoder（同 DualGAT，3 层 GATConv）
  2. **跨图 matching 层**：p-v 跨图注意力（每个 v_node attend to all p_nodes），输出 matching matrix (|p| × |v|)
  3. **边编码**：链路带宽/延迟编码进 edge_attr，参与 GNN 消息传递
  4. **SFC 链位置编码**：v_node embedding 加入 SFC 序号的位置编码（sinusoidal or learnable）
  5. **输出**：matching score → 逐节点选择（与 MVE 一致的 sequential 决策）
- **注册**：`@ActorCriticRegistry.register('matching_gat')`
- **引用**：L10 GraphVNE (matching 思想) + L01 Virne (DualGAT 架构)

### M4: 评估指标

| 指标 | 定义 | 来源 |
|------|------|------|
| AC (Acceptance Rate) | 成功嵌入 VNR 比例 | L01 Virne, 全部论文 |
| R2C (Revenue-to-Cost) | 嵌入收益 / 资源消耗 | L01 Virne, 全部论文 |
| SFC-IR (Chain Integrity Rate) | SFC VNF 链完整嵌入比例（所有 VNF 按序放置且链路连通） | 新增，核心差异化指标 |
| E2E-Latency | SFC 链端到端延迟（可选开启延迟约束时） | L12 CONAL |
| Inference Time | 单 VNR 求解时间 | L01 Virne |

### M5: 训练管线

- 基于 Virne 的 PPO 训练管线（`rl_core/` + `instance_agent.py`）
- 新增：wandb 集成、early stopping（reward plateau + KL 散度）、best model 保存
- 所有 solver（含 baseline）使用相同训练超参框架

### M6: 验证套件

- 解析验证：已知参数下 R2C 计算正确性
- 统计验证：VNR 到达时间 Poisson 分布检验
- 退化测试：固定 VNR 序列 → 确定性结果
- SFC 专项：chain integrity 在无约束环境 = AC；约束越严 IR < AC

---

## 4. 关键参数表

### 4.1 拓扑参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| WX100 节点数 | 100 | L01 Virne:Table I | ✅ Virne 内置 |
| WX100 边数 | ~500 (Waxman α=0.5, β=0.2) | L01 Virne | ✅ Virne 内置 |
| GEANT 节点数 | 23 | L01 Virne | ✅ Virne 内置 |
| BRAIN 节点数 | 161 | L01 Virne | ✅ Virne 内置 |
| WX500 节点数 | 500 | L01 Virne | ✅ Virne 内置 |
| PN 节点资源 | CPU: U[50,100] | L01 Virne:Table I | ✅ |
| PN 链路资源 | BW: U[50,100] | L01 Virne:Table I | ✅ |

### 4.2 VNR/SFC 参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| VNR 数量 | 1000 | L01 Virne:Table I | ✅ |
| VNR 规模 | U[2,10] | L01 Virne:Table I | ✅ |
| VNR CPU 需求 | U[0,20] | L01 Virne:Table I | ✅ |
| VNR BW 需求 | U[0,50] | L01 Virne:Table I | ✅ |
| VNR 连接概率 | 0.5 (random) | L01 Virne | ✅ 保持不变 |
| 到达率 | Poisson λ=0.04 | L01 Virne | ✅ |
| 生命周期 | Exp(500) | L01 Virne | ✅ |
| SFC VNF 比例 | 0.6 | [ASSUMPTION] | 待验证 |
| VNF 类型池大小 | 5 | [ASSUMPTION] | 待验证 |
| SFC 链拓扑 | 线性链（VNR 子集） | L12 CONAL, L14 ICC2025 | ✅ |

### 4.3 训练参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| 算法 | PPO | L01 Virne | ✅ |
| GNN 层数 | 3 | L01 Virne:learning.yaml | ✅ |
| Embedding 维度 | 128 | L01 Virne:learning.yaml | ✅ |
| Actor LR | 0.001 | L01 Virne:learning.yaml | ✅ |
| Critic LR | 0.001 | L01 Virne:learning.yaml | ✅ |
| Gamma | 0.99 | L01 Virne:learning.yaml | ✅ |
| GAE Lambda | 0.98 | L01 Virne:learning.yaml | ✅ |
| PPO clip | 0.2 | L01 Virne:learning.yaml | ✅ |
| Batch size | 128 | L01 Virne:learning.yaml | ✅ |
| Grad clip | 0.5 | L01 Virne:learning.yaml | ✅ |
| 训练 epochs | 50 | L01 Virne | ✅ |
| Seeds | ≥3 | 领域惯例（文献笔记 VVUQ 汇总） | ✅ |

[ASSUMPTION] 比例：2/18 ≈ 11%，低于 30% 门槛。✅

---

## 5. 奖励函数设计

### 5.1 奖励结构

沿用 Virne `fixed_intermediate` 奖励，不额外添加 SFC 奖励分量。

| 状态 | 奖励值 | 说明 |
|------|--------|------|
| VNR 嵌入成功 | `v_net_r2c_ratio` | 收益成本比，典型 0.5-2.0 |
| 中间步骤成功（节点放置+链路路由） | 0.1 | 固定中间奖励 |
| 步骤失败 | -0.1 | 惩罚 |
| 拒绝 | 0（episode 结束） | 无额外惩罚 |

### 5.2 为什么不加 SFC 奖励分量

1. **SFC 约束由环境强制执行**（action masking），不需要通过奖励学习
2. **避免奖励失衡风险**（C1 模式，4/6 项目中招）：新增分量需要仔细平衡量级
3. **与 baseline 公平对比**：所有 solver 使用相同奖励函数
4. **SFC 差异通过指标体现**：SFC-IR 作为评估指标而非奖励项

### 5.3 量级分析

| 分量 | 典型值范围 | 占比估算 |
|------|-----------|---------|
| 成功 R2C | 0.5-2.0（episode 终） | ~60-80% |
| 中间奖励 | ±0.1（每步）× 2-10 步 | ~20-40% |

无可独占分量（<80% 门槛），沿用 MVE 已验证的配置。✅

### 5.4 MDP 试运行检查（Step 7 Part A-checkpoint）

进入训练前，必须执行 `gw-experiment.md §impl Part A-checkpoint`：
1. 跑 1 episode 随机策略 + 1 episode 贪心策略
2. 验证：无单一项 >95%、策略区分度 >10%、关键指标可优化

---

## 6. 验证标准

### 6.1 仿真器验证

| 验证类型 | 检查内容 | 通过标准 |
|---------|---------|---------|
| 解析验证 | 已知 VNR+PN 参数下 R2C 计算 | 与手动计算一致（±1e-6） |
| 统计验证 | VNR 到达时间分布 | KS 检验 Poisson(0.04), p>0.05 |
| 退化测试 | 固定种子 + 固定 VNR 序列 | 结果完全确定性 |
| SFC 专项 | 无 SFC 约束时 SFC-IR == AC | 100% |
| SFC 专项 | 强 SFC 约束（不可达节点多）| SFC-IR < AC |

### 6.2 Baseline 复现验证

| 验证类型 | 检查内容 | 通过标准 |
|---------|---------|---------|
| 趋势验证 | GRC vs pg_mlp vs DualGAT+ 性能排序 | 与 MVE 一致（DualGAT > MLP > GRC）|
| 数值级 | MVE 数值在新环境下可复现 | AC/R2C 在 ±5% 范围内 |

### 6.3 训练验证

| 验证类型 | 检查内容 | 通过标准 |
|---------|---------|---------|
| 收敛性 | PPO reward 曲线 | 单调上升后平稳 |
| WandB 集成 | 指标实时记录 | AC/R2C/loss 可视化正常 |
| Early stopping | reward plateau 检测 | 连续 5 epoch 无改善时触发 |

---

## 7. FR-12 MVE vs Formal 架构差异

| 维度 | MVE (§D 架构摘要) | Formal (本设计) | 影响 model→baseline 对比？ |
|------|-------------------|-----------------|---------------------------|
| 动作空间 | 离散节点选择（双向：先选虚拟节点再选物理节点） | 离散节点选择（SFC VNF 按拓扑序优先，非 VNF 按 node_ranking_method） | **是** — SFC VNF 节点的排序约束。**论证**：baseline 同样受此约束（环境强制），公平性不受影响。对比"在相同约束下，SFC-aware GNN vs SFC-blind GNN/MLP/启发式"。**可证伪**：如果 SFC 排序导致所有方法性能系统性下降（AC 低于无约束场景 >20%），则论证不成立 → 回退到全 node_ranking_method |
| 决策粒度 | per-VNR（逐请求处理，每请求内逐节点放置） | per-VNR（相同） | 否 |
| 对比范式 | PPO-DualGAT+ vs pg_mlp vs GRC | PPO-MatchingGAT(ours) vs PPO-DualGAT+(B2) vs pg_mlp(B3) vs GRC(B1) vs CONAL(B4) vs PPO-DualGCN(B5) | 否 — baseline 方法不变，仅增加我们方法和 2 个 baseline（B4/B5） |
| 奖励语义 | fixed intermediate (0.1) + episode-level R2C | 相同 | 否 |
| VNR 拓扑 | random (Erdos-Renyi, p=0.5) | **相同**（random graph + SFC 约束叠加层） | **否** — VNR 图拓扑不变，仅叠加 SFC 节点标签和顺序约束。MVE 证据完全适用 |
| 环境 | PlaceStepInstanceRLEnv | JointPRStepInstanceRLEnv + SFC 约束 | **是** — 从 PlaceStep 改为 JointPR。**论证**：(1) JointPR 是 DualGAT+ 的标准环境变体（MVE 的 `ppo_dual_gat+` solver 已使用 JointPR）；(2) 所有 baseline 同样运行在 JointPR 上。**可证伪**：如果 JointPR 导致某 baseline 训练不收敛，则需切换环境变体 |

### 门控结论

2 项"是"（从 3 项降至 2 项），均有可证伪论证。VNR 拓扑保持不变是关键改进——消除了"GNN 优势依赖拓扑复杂度"这一最大风险。

**无需新 MVE，进入 Step 7。**

---

## 8. 实验配置

### 8.1 实验场景矩阵

| 场景 | 拓扑 | VNR 规模 | VNR 数量 | 目的 |
|------|------|---------|---------|------|
| S1 | WX100 | U[2,10] | 1000 | 主实验（对标 MVE） |
| S2 | GEANT | U[2,10] | 1000 | 真实拓扑小规模 |
| S3 | BRAIN | U[2,10] | 1000 | 真实拓扑大规模 |
| S4 | WX500 | U[2,10] | 1000 | 大规模随机拓扑 |

### 8.2 Solver 对比矩阵

| Solver | ID | GNN 类型 | SFC 感知 | 来源 |
|--------|-----|---------|---------|------|
| GRC | B1 | 无（启发式） | 否 | Virne 内置 |
| PPO-DualGAT+ | B2 | DualGAT | 否 | Virne 内置 |
| pg_mlp | B3 | MLP | 否 | Virne 内置 |
| CONAL | B4 | GNN+CMDP | 否 | Virne 内置 |
| PPO-DualGCN | B5 | DualGCN | 否 | Virne 内置 |
| **PPO-MatchingGAT** | **Ours** | **MatchingGAT** | **是** | **本设计** |

### 8.3 消融实验

| 消融 | 说明 | 目的 |
|------|------|------|
| Ours - SFC 位置编码 | 去掉 SFC 序号位置编码和 vnf_type 特征 | 验证 SFC 感知的贡献 |
| Ours - 跨图 matching | 替换为独立编码（=DualGAT） | 验证 matching 层的贡献 |
| Ours - 边编码 | 去掉 edge_attr | 验证边信息的贡献 |
| sfc_ratio 扫描 | sfc_ratio ∈ {0.3, 0.6, 0.9} | 验证 SFC 约束强度对方法差异的影响 |

---

## 9. 风险预判

| 风险 | 概率 | 缓解 |
|------|------|------|
| SFC 约束过严导致 action mask 过窄，所有方法趋同 | 中 | 先跑 GRC 在 SFC 环境下确认有非零 AC；sfc_ratio 可调（0.4-0.8） |
| Matching GNN 训练不收敛 | 低 | 回退到 DualGAT 架构 + SFC 位置编码（降级贡献） |
| Virne 扩展导致接口不兼容 | 低 | 通过子类继承而非修改源码 |
| GNN 在 SFC VNF 子集上的优势不够显著 | 中 | 消融实验对比 SFC-aware vs SFC-blind，量化 SFC 信息增益 |

---

## 10. 时间估计

| 阶段 | 时间 | 说明 |
|------|------|------|
| SFC 数据模型 + VNR 生成器 | 2-3 天 | 新模块，不涉及核心修改 |
| SFC 约束环境 | 2-3 天 | 继承 JointPRStepInstanceRLEnv |
| Matching-style GNN policy | 3-4 天 | 核心创新点，需调试 |
| 训练 + 超参搜索 | 5-7 天 | RTX 4070, 4 拓扑 × 6 solver |
| 实验运行 + 分析 | 3-5 天 | 消融 + 统计 |
| **总计** | **~3-4 周** | 与 §E 估计一致 |
