# 仿真器设计规格: leo-congestion-routing

> GNN per-link 负载均衡 for LEO Walker delta 星座

## 1. 问题建模

**MDP 公式化**（集中式 SDN 控制器视角，与 GMR/PathGNN 范式对齐）：

- **状态 S**: 全图状态 = {节点特征 (N×d_n), 边特征 (E×d_e), 流量需求矩阵 (F×3)}
- **动作 A**: 全局路由决策 = 对每条有向边输出一个权重，加权最短路路由
- **奖励 R**: -(MLU_after)，每步计算
- **转移 P**: 确定性（路由决策 → 链路负载更新 → 下一流量需求）

**与 MVE 的关键区别**：
| | MVE | 正式仿真器 |
|---|---|---|
| 决策粒度 | per-flow 选路径 (离散) | per-link 权重 (连续) |
| 动作空间 | K 选 1 (K=4 paths) | E 维连续向量 |
| 路由方式 | 逐流选路 | 加权最短路/分流 |
| 拓扑 | 静态 Walker delta | 时变（可选，见 §5） |
| 规模 | 24/66 节点 | 48/66/288/720 节点 |

## 2. 模块清单

### 2.1 拓扑生成器 (topology.py)
- Walker delta 星座 → networkx 有向图
- 4 ISL/sat: 2 intra-plane (ring) + 2 inter-plane
- 极缝处理: 纬度 > 阈值时禁用 inter-plane ISL [ASSUMPTION]
- 输出: Graph + edge_index (PyG 格式) + edge_features
- **扩展自**: mve_env.py `build_topology()`

### 2.2 流量生成器 (traffic.py)
- 非均匀流量: 热点目的地 + 重型流 + 轻型流（继承 MVE）
- **新增**: 突发模式（DTAR surge factor）+ 时变强度（NHPP，ST-QoS）
- 流量矩阵: F 个 (src, dst, demand) 三元组
- **扩展自**: mve_env.py `_generate_flows()`

### 2.3 链路故障注入器 (failures.py)
- 每 episode 随机移除 p_f 比例的 ISL
- **新增**: 故障模式可配置（随机 / 区域性 / 级联）
- **扩展自**: mve_66.py `RoutingEnv66.reset()`

### 2.4 路由环境 (env.py)
- 核心: 接收 per-link 权重 → 加权最短路路由 → 计算链路负载 → 计算 MLU
- 分流模式: 加权最短路 (主) 或多路径比例分流 (可选)
- **新增**: 与 MVE 的 per-flow 选路不同，per-link 权重控制全局路由
- **扩展自**: mve_env.py `RoutingEnv`

### 2.5 GNN 模型 (model.py)
- GAT/GIN encoder → Readout → FC decoder
- 输入: node_feat (N×d_n) + edge_index + edge_feat (E×d_e)
- 输出: per-directed-edge weight (E 维连续向量)
- 参考: L06 DTAR (GAT+LN+Residual), L02 GMR (MPNN+GRU)
- **扩展自**: mve_train.py `GNNActorCritic`

### 2.6 训练循环 (train.py)
- PPO with GAE + entropy bonus + grad clip
- **新增**: wandb/tensorboard logging, early stopping, save/load with optimizer
- **扩展自**: mve_66.py `train_model()`

### 2.7 Baseline 实现 (baselines/)
- SP: Dijkstra 最短路径
- ECMP: 等价多路径（等代价路径间均匀分配）
- MLP: 同架构但无 message passing（消融）
- DTAR: 适配 DTAR 代码到本仿真器
- GMR-simplified: 简化 MPNN+DDPG（去 PER, K=2 固定路径）

## 3. 关键参数表

### 3.1 星座参数

| 参数 | 值 | 来源 | 理由 |
|------|-----|------|------|
| 训练星座 | 6×11=66 节点 | L02 GMR (Iridium 66) | MVE 已验证，跨规模泛化起点 |
| 泛化测试 1 | 4×12=48 节点 | L02 GMR (GlobalStar 48) | 与 GMR 对齐，验证小规模泛化 |
| 泛化测试 2 | 12×24=288 节点 | L06 DTAR (288 sat) | 中等规模，验证 4× 泛化 |
| 泛化测试 3 | 36×20=720 节点 | L01 GRLR (720 sat) | 大规模，验证 10× 泛化 |
| 轨道高度 | 780 km | L02 GMR (Iridium) | Iridium 标准轨道 |
| 倾角 | 86.4° | Iridium specification | 近极轨 |
| ISL 容量 | 10 Gbps | [ASSUMPTION] | 合理值，与 MVE 对齐 |
| ISL 带宽 | 500 MHz | L06 DTAR:ISL 500MHz | Ka 频段 ISL |

### 3.2 流量参数

| 参数 | 值 | 来源 | 理由 |
|------|-----|------|------|
| 流数量 (66节点) | 40 | MVE 配置 | 已验证 |
| 重型流数 | 10 (25%) | MVE 配置 | 80/20 分布近似 |
| 重型需求 | 3-5 Gbps | MVE 配置 | 接近 ISL 容量 50% |
| 轻型需求 | 0.1-1.0 Gbps | MVE 配置 | 较小流量 |
| 热点目的地数 | 3 (占全部节点 ~5%) | MVE 配置 | 非均匀性来源 |
| 突发因子 μ | 5× | L06 DTAR:surge indicator | 验证拥塞适应 |
| 时变模式 | NHPP sin(2πt/T) | L10 ST-QoS | 周期性强度变化 |

### 3.3 故障参数

| 参数 | 值 | 来源 | 理由 |
|------|-----|------|------|
| 故障率 | 8% (默认), 5%/10% 消融 | MVE-2 配置 | GNN 优势激活条件 |
| 故障模式 | 随机独立 | MVE-2 | 基础模式 |
| 区域故障 | 10% 节点周围链路全断 | [ASSUMPTION] | 极端场景消融 |

### 3.4 训练参数

| 参数 | 值 | 来源 | 理由 |
|------|-----|------|------|
| GNN 架构 | GAT, 2层, 4头, h=64 | L06 DTAR:GAT(64,4头)+LN+Res | 当前最佳实践 |
| RL 算法 | PPO | L06 DTAR, L01 GRLR | 领域主流 |
| PPO clip ε | 0.2 | L03 POMAP, 标准 | 默认值 |
| Learning rate | 3e-4 | MVE 配置 | Adam 默认 |
| Entropy coeff | 0.01 | MVE 配置 | 探索-利用平衡 |
| Episodes | 500 (66节点) | MVE 150→增大 | 更复杂任务需更多 |
| Seeds | ≥3 | MVE 配置 | 统计显著性 |
| 评估 episodes | 50 | MVE 20→增大 | 更稳定评估 |

## 4. 奖励函数设计

### 4.1 奖励结构

主奖励: **负 MLU 变化量**（per-step）

```
r_t = -(MLU_t - MLU_{t-1})
```

MLU = max(link_load_e / capacity_e) for all edges e

**备选方案**: Episode-level reward
```
R = -MLU_final - α·CV - β·overflow_count
```
CV = 负载变异系数 (负载均衡质量), overflow = 超容量链路数

### 4.2 归一化分析

| 项 | 原始范围 | 归一化方式 | 归一化后范围 |
|-----|---------|-----------|------------|
| MLU | [0, +∞) | 除以 capacity → [0, +∞) | MVE 实测 [0.5, 1.5] |
| MLU 变化 | [-∞, +∞) | 自然范围 | MVE 实测 [-0.1, +0.1] |
| CV | [0, +∞) | 自然范围 | 预估 [0, 0.5] |

**风险检查**: MLU 变化量已在自然范围内（~0.1 量级），无量级失衡风险。若加入 CV 或 overflow 惩罚项，需确保与主奖励同量级。

### 4.3 文献对齐

| 论文 | 奖励 | 归一化 | 本项目采用 |
|------|------|--------|-----------|
| L01 GRLR | -delay | 无 | 不采用（延迟非主指标） |
| L02 GMR | σ₁·f̄ - σ₂·d̄ | 无 | 不采用（吞吐量/延迟非主指标） |
| L03 POMAP | -λ^T·c_norm | min-max | 参考（MLU 天然归一化） |
| L07 Fan | α·TP/TP_max - β·D/D_max | 除最大值 | 参考（MLU/capacity 即此方式） |

**决策**: 采用 -MLU 变化量（per-step），MLU 本身已除以 capacity 归一化。与 MVE 一致，简单有效。

## 5. 时变拓扑（可选增强）

> 优先级: P2（先跑静态拓扑验证核心方法，成功后加入时变）

基于轨道力学（二体模型）计算 ISL 长度变化：
- Walker delta 轨道面内 ISL 长度恒定
- 轨道面间 ISL 长度随纬度变化（赤道最长，极地最短）
- 极区（纬度 > 阈值）inter-plane ISL 不可用

来源: L01 GRLR (STK 轨道模型), L06 DTAR (极区断链)

## 6. 验证标准

### 6.1 解析验证
- [ ] 2 节点 1 链路: 1 个流 demand=5, capacity=10 → MLU=0.5 ✓
- [ ] 4 节点环形: 对称流 → ECMP MLU = 理论计算值 ✓
- [ ] 加权最短路: 给定权重 → 验证路由路径 = 预期路径 ✓

### 6.2 统计验证
- [ ] 流量需求分布: 重型流 U(3,5), 轻型流 U(0.1,1) → 检验分布参数
- [ ] 链路故障数: 8% rate → 检验实际故障比例 ≈ 8% ± 2%
- [ ] MLU 分布: 50 episodes → 检验无退化（均值/方差合理）

### 6.3 退化测试
- [ ] 固定种子 + 固定故障 → 确定性输出
- [ ] 去掉非均匀性（所有流同 demand）→ ECMP ≈ 最优，GNN 无显著优势

### 6.4 自相关预警
- [ ] 流量时序 lag-1 自相关 < 0.95（引入 NHPP 波动后）
- [ ] MLU 时序 lag-1 自相关 < 0.95

## 7. 评估场景矩阵

| 场景 | 星座 | 故障率 | 流量模式 | 目的 |
|------|------|--------|---------|------|
| S1 基础 | 66 节点 | 8% | 非均匀+热点 | 核心对比 |
| S2 无故障 | 66 节点 | 0% | 非均匀+热点 | ECMP 对照 |
| S3 突发 | 66 节点 | 8% | 非均匀+突发 5× | 拥塞适应 |
| S4 小规模泛化 | 48 节点 | 8% | 非均匀+热点 | Size gen 小→中 |
| S5 中规模泛化 | 288 节点 | 8% | 非均匀+热点 | Size gen 4× |
| S6 大规模泛化 | 720 节点 | 8% | 非均匀+热点 | Size gen 10× |

## 8. [ASSUMPTION] 统计

| 参数 | 值 | 标记 |
|------|-----|------|
| ISL 容量 10 Gbps | 10 Gbps | [ASSUMPTION] — 无直接论文来源，综合 L07(200Mbps)~L10(300Mbps) 取高值 |
| 极缝阈值 | 待定 | [ASSUMPTION] — 需查轨道力学 |
| 区域故障模式 | 10% 节点周围 | [ASSUMPTION] — 无直接来源 |

[ASSUMPTION] 占比: 3/25 ≈ 12% < 30% → 通过

## 9. 文件组织

```
projects/leo-congestion-routing/simulator/
├── config.py          # Config dataclass（星座/流量/训练参数）
├── topology.py        # Walker delta 拓扑生成
├── traffic.py         # 流量生成（非均匀+突发+时变）
├── failures.py        # 链路故障注入
├── env.py             # 路由环境（per-link 权重 → 加权路由 → MLU）
├── model.py           # GNN Actor-Critic (GAT/GIN + PPO)
└── train.py           # 训练循环 (PPO + wandb + early stopping)

projects/leo-congestion-routing/baselines/
├── sp.py              # Shortest Path
├── ecmp.py            # ECMP
├── mlp.py             # MLP ablation
├── dtar_adapter.py    # DTAR 代码适配
└── gmr_simplified.py  # GMR 简化版

projects/leo-congestion-routing/results/
└── (实验结果)
```
