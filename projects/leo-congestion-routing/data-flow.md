# 端到端数据流推演

> 产出阶段：Contract Step 4
> 用途：仿真器开发的设计文档，Execute 阶段对着此文件写代码

## 1. 网络配置 → 节点位置

- **输入**：SimConfig(n_planes=6, sats_per_plane=11, altitude=780km, inclination=86.4°)
- **处理**：Walker delta 星座。node_id = plane × sats_per_plane + sat_index。无实际轨道坐标计算（简化模型，使用静态拓扑）
- **输出**：N=66 个节点

> **设计选择**：不计算实际轨道坐标和 ISL 几何。distance_km 统一设为 1.0。原因：per-link weight 策略由 GNN 学习全局权重，不依赖物理距离。Polar gap（高纬度断开 inter-plane ISL）也未实现，由随机故障注入近似补偿。

## 2. 拓扑连接 → 链路属性

- **输入**：66 节点
- **处理**：
  - Intra-plane ring（etype=0）：每轨道面 11 节点成环，双向 → 11×2×6 = **132 条有向边**
  - Inter-plane ISL（etype=1）：相邻轨道面同 index 卫星，双向 → 11×2×6 = **132 条有向边**
  - 总计 E = **264 条有向边**
- **输出**：
  - edge_index: (2, 264) int64 — 有向边端点
  - edge_features（topology 输出）: (264, 4) = [cap_norm=1.0, etype∈{0,1}, dist_km=1.0, 0.0]
  - env.__init__ 重映射为 spec 格式: (264, 4) = [utilization=0.0, edge_type, is_failed=0.0, capacity_norm=1.0]

## 3. 流量生成

- **输入**：N=66, config（n_flows=40, n_heavy=10, n_popular=3, surge_factor=5, tv_amplitude=0.3）
- **处理**（traffic.py）：
  1. 首次调用随机选 3 个热点目的地（缓存到 `_popular`）
  2. 10 条重型流：src∈[0,66), dst∈hotspots, demand~U(3,5) Gbps
  3. 30 条轻型流：src,dst∈[0,66) 随机, demand~U(0.1,1.0) Gbps
  4. NHPP 时变调制：demand × (1 + 0.3·sin(2πt/T))
  5. 突发：每条流 10% 概率 demand × 5
- **输出**：list[(src, dst, demand)]，长度 40，每步重新生成

> **维度验证**：demand 范围 [0.1, 25] Gbps（5×突发后上限），ISL 容量 10 Gbps → 单条重型突发流可占满一条 ISL。热点目的地（3/66≈5%）制造非均匀性。✓

## 4. 状态构造

### 4a. 节点特征 (N, 6)

| 列 | 特征名 | 来源 | 范围 | 说明 |
|----|--------|------|------|------|
| 0 | in_load_norm | link_load / capacity | [0, ∞) | 入边总负载归一化（t=0 时为 0） |
| 1 | out_load_norm | link_load / capacity | [0, ∞) | 出边总负载归一化（t=0 时为 0） |
| 2 | demand_as_src_norm | Σdemand(src=n) / capacity | [0, ∞) | 本节点作为源的总需求 |
| 3 | demand_as_dst_norm | Σdemand(dst=n) / capacity | [0, ∞) | 本节点作为目的的总需求 |
| 4 | is_hotspot | 1.0 if n ∈ popular | {0, 1} | 热点目的地标记 |
| 5 | degree_norm | deg(n) / max_deg | (0, 1] | 度数归一化 |

**时序注意**：t=0 时 in_load/out_load=0（首次路由前无负载信息）。模型第一步仅靠 demand 模式做决策，第二步起才有负载反馈。

### 4b. 边特征 (E, 4)

| 列 | 特征名 | 来源 | 范围 | 说明 |
|----|--------|------|------|------|
| 0 | utilization | link_load / capacity | [0, ∞) | 当前链路利用率（每步更新） |
| 1 | edge_type | etype from topology | {0, 1} | 0=intra-plane, 1=inter-plane |
| 2 | is_failed | failures.py | {0, 1} | 故障标记（reset 时设置，episode 内不变） |
| 3 | capacity_norm | 1.0 | {1.0} | 归一化容量（当前所有 ISL 相同） |

**故障处理**：故障边保留在 edge_index 中（is_failed=1.0），路由时赋权重 1e9（等效断开）。不移除边以保持模型参数维度固定。

## 5. 模型输入

- **输入**：PyG Data(x=(N,6), edge_index=(2,E), edge_attr=(E,4))
- **处理**：
  1. GATEncoder.in_proj: Linear(6, 64) → h=(N, 64)
  2. GAT Layer ×2: GATConv(h, edge_index, edge_attr) → LayerNorm → ReLU + Residual → h=(N, 64)
  3. EdgeWeightDecoder: MLP(emb_u∥emb_v∥edge_feat) = MLP(64+64+4=132 → 64 → 1) → softplus → weight=(E,)
  4. ValueHead: mean_pool(h, dim=0) → FC(64,64) → ReLU → FC(64,1) → scalar

- **输出**：mean_weights=(E,), value=scalar

**参数量**：
- GATEncoder: in_proj(6×64=384) + 2×GATConv(~16K each) + 2×LN(128) ≈ 33K
- EdgeWeightDecoder: MLP(132×64+64+64×1) ≈ 8.5K + 8.5K ≈ 9K
- ValueHead: 64×64+64+64×1 ≈ 4.2K
- log_std: 264
- **总计 ≈ 47K 参数**

## 6. 模型输出 → 动作 → 路由

- **模型输出**：mean=(E,) 正权重（softplus 保证 >0）
- **训练时动作**：sample ~ Normal(mean, exp(log_std))，clamp > 1e-6
- **推理时动作**：deterministic=True，直接用 mean
- **路由**：
  1. 构建 nx.DiGraph，action[i] 为边 i 的权重
  2. 故障边权重设为 1e9（等效不可达）
  3. 对每条 flow (src, dst, demand)：Dijkstra 最短路，累加 link_load
  4. MLU = max(link_load_e / capacity_e)
- **输出**：link_load dict, MLU float, n_overflow int

**关键设计**：所有流用**同一组权重同时路由**（非逐流），符合 SDN 集中控制器范式。

## 7. 奖励/损失计算

- **奖励**：r_t = -MLU_t（单分量，无量级失衡风险）
- **回报**：G_t = Σ_{k=0}^{T-t} γ^k · r_{t+k}
- **优势**：A_t = GAE(δ_t, λ=0.95)，δ_t = r_t + γ·V(s_{t+1}) - V(s_t)
- **PPO 损失**：
  - actor: -min(ratio·A, clip(ratio, 0.8, 1.2)·A) - 0.01·entropy
  - critic: 0.5·(V_pred - G)^2
  - 总计: L_actor + 0.5·L_critic

## 8. 跨规模泛化

### 维度变化表

| 规模 | P × S | N | E | 流量 |
|------|-------|---|---|------|
| 训练 | 6×11 | 66 | 264 | 40 |
| 泛化 | 4×12 | 48 | 192 | 29 |
| 泛化 | 12×24 | 288 | 1152 | 173 |
| 泛化 | 36×20 | 720 | 2880 | 432 |

### 泛化流程

1. 创建目标规模 SimConfig → RoutingEnv → obs=(N_new, 6), edge_index=(2, E_new), edge_attr=(E_new, 4)
2. 加载 66 节点训练的模型
3. **GATEncoder**：Linear(6→64) 维度无关 ✓；GATConv 操作任意大小图 ✓
4. **EdgeWeightDecoder**：per-edge MLP(emb_u∥emb_v∥edge_feat) 与边数无关 ✓
5. **ValueHead**：mean_pool → FC，维度无关 ✓
6. **log_std**：固定 264 维 → **不能用于 E≠264 的图** → 泛化必须用 deterministic=True ✓
7. Dijkstra 路由在 env 内完成，模型只输出权重，拓扑无关 ✓

### 泛化时的特征一致性

- 节点特征 (N, 6)：全部归一化（/capacity 或 /max_degree），与规模无关 ✓
- 边特征 (E, 4)：同上，全部归一化 ✓
- 流量：按 0.6 × N_nodes 缩放，demand 范围不变 ✓

### 已知限制

1. **log_std 维度固定**：训练时 E=264 → log_std 是 nn.Parameter(264)。泛化到其他规模必须用 deterministic 模式，不能做随机采样。这意味着泛化评估没有探索策略，只评估贪心策略。
2. **极地间隙未实现**：config 有 polar_gap_lat=70° 但 topology/failures 未使用。真实 LEO 星座在高纬度断开 inter-plane ISL。当前简化模型通过随机故障近似此效果。
3. **distance_km=1.0**：所有链路距离相同，模型无法学习距离感知路由。per-link weight 方案不依赖物理距离，但若未来引入距离相关特征需修正。

## 断层检查

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 特征缺失 | ✅ 无断层 | 模型有 demand_as_dst 和 is_hotspot 提供目的地信息；有 utilization 提供负载信息 |
| 2 | 维度不匹配 | ✅ 无断层 | GNN 模型全部维度无关；消融实验 MLP 与 GNN 共享接口；log_std 固定维度已记录为已知限制 |
| 3 | 配置矛盾 | ✅ 无断层 | demand/capacity 比率在 MVE 验证范围内（MLU 0.8-1.5）；故障率 8% 与 MVE-2 一致 |
| 4 | 跨规模断裂 | ⚠ 已记录 | log_std 维度固定 → 泛化必须 deterministic，已记录。其余模块全部维度无关 |
