# 端到端数据流推演

> 产出阶段：Contract Step 4
> 最后更新: 2026-05-26 — P0 修正：节点特征对齐代码、封顶值修正、延迟模型重新定位
> 用途：仿真器开发的设计文档，Execute 阶段对着此文件写代码

## 1. 网络配置 → 节点位置

- **输入**：SimConfig(n_planes=6, sats_per_plane=11, altitude=550km, inclination=86.4°, F=1, polar_gap_lat=70°)
- **处理**：Walker-Delta 星座物理仿真。node_id = plane × sats_per_plane + sat_index。轨道坐标由 Kepler 方程计算，ISL 距离基于卫星间几何距离。极地间隙（polar_gap_lat=70°）已实现：高纬度卫星断开 inter-plane ISL。
- **输出**：N=66 个节点

> **设计选择**：物理仿真拓扑替代原简化网格模型。distance_km 由卫星间欧几里得距离计算（非固定 1.0）。Polar gap 已实现：纬度 > 70° 的卫星 inter-plane ISL 断开。propagation delay = distance_km / c（光速），用于 E2E 延迟计算。

## 2. 拓扑连接 → 链路属性

- **输入**：66 节点（含轨道坐标）
- **处理**：
  - Intra-plane ring（etype=0）：每轨道面 11 节点成环，双向 → 11×2×6 = **132 条有向边**
  - Inter-plane ISL（etype=1）：相邻轨道面同 index 卫星，双向 → 11×2×6 = **132 条有向边**（扣除极地间隙后实际 < 132）
  - 极地间隙：纬度 > polar_gap_lat=70° 的卫星断开 inter-plane ISL，减少高纬度连接
  - 总计 E ≤ **264 条有向边**（具体数量取决于极地间隙裁剪）
- **输出**：
  - edge_index: (2, E) int64 — 有向边端点
  - edge_features（topology 输出）: (E, 4) = [cap_norm=1.0, etype∈{0,1}, dist_km=实际距离, propagation_ms]
  - env.__init__ 重映射为 spec 格式: (E, 4) = [utilization=0.0, edge_type, is_failed=0.0, capacity_norm=1.0]

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

### 4a. 节点特征 (N, 7)

| 列 | 特征名 | 来源 | 范围 | 说明 |
|----|--------|------|------|------|
| 0 | in_load_norm | link_load / capacity | [0, ∞) | 入边总负载归一化（t=0 时为 0） |
| 1 | out_load_norm | link_load / capacity | [0, ∞) | 出边总负载归一化（t=0 时为 0） |
| 2 | is_current_src | 1.0 if n == current_flow.src | {0, 1} | 当前待路由流的源节点标记 |
| 3 | is_current_dst | 1.0 if n == current_flow.dst | {0, 1} | 当前待路由流的目的节点标记 |
| 4 | current_demand_norm | demand / capacity | [0, ∞) | 当前流的流量需求归一化（同时赋给 src 和 dst） |
| 5 | is_hotspot | 1.0 if n ∈ popular | {0, 1} | 热点目的地标记 |
| 6 | degree_norm | base_deg / max_deg | (0, 1] | 拓扑度数归一化（物理拓扑下因极地间隙节点度数不同） |

> **与旧版文档的差异**：旧版记录了 demand_as_src/dst_norm（聚合需求）和 lat_norm（纬度），实际代码实现为 is_current_src/dst（当前流标记）+ current_demand_norm（当前流需求）。代码版本更直接：GNN 需要知道"此刻要路由哪条流"而非"本节点累计有多少需求"。

**时序注意**：t=0 时 in_load/out_load=0（首次路由前无负载信息）。模型第一步仅靠 current_src/dst + demand + is_hotspot + degree 做决策，第二步起才有负载反馈。

### 4b. 边特征 (E, 4)

| 列 | 特征名 | 来源 | 范围 | 说明 |
|----|--------|------|------|------|
| 0 | utilization | link_load / capacity | [0, ∞) | 当前链路利用率（每步更新） |
| 1 | edge_type | etype from topology | {0, 1} | 0=intra-plane, 1=inter-plane |
| 2 | is_failed | failures.py | {0, 1} | 故障标记（reset 时设置，episode 内不变） |
| 3 | capacity_norm | 1.0 | {1.0} | 归一化容量（当前所有 ISL 相同） |

**故障处理**：故障边保留在 edge_index 中（is_failed=1.0），路由时赋权重 1e9（等效断开）。不移除边以保持模型参数维度固定。

## 5. 模型输入

- **输入**：obs dict {node_feat(N,7), edge_index(2,E), edge_feat(E,4), paths, flow, n_valid}
- **处理**：
  1. GATEncoder.in_proj: Linear(7, 64) → h=(N, 64)
  2. GAT Layer ×2: GATConv(h, edge_index, edge_attr) → LayerNorm → ELU + Residual → h=(N, 64)
  3. PathScoringHead: 对每条候选路径 path ∈ paths[:n_valid]:
     mean(node_emb[path_nodes]) → MLP(64→32→1) → scalar score
     n_valid < K 的位置填充 -1e9 (无效动作 mask)
  4. ValueHead: cat(node_emb[src], node_emb[dst]) → FC(128→64→1) → scalar

- **输出**：logits=(K,) 用于 Categorical 分布, value=scalar

**参数量**：
- GATEncoder: in_proj(7×64=448) + 2×GATConv(~16K each) + 2×LN(128) ≈ 33K
- PathScoringHead: MLP(64×32+32+32×1) ≈ 2.1K
- ValueHead: FC(128×64+64+64×1) ≈ 8.3K
- **总计 ≈ 43K 参数**（无 log_std，离散动作空间不需要）

## 6. 模型输出 → 动作 → 路由

- **模型输出**：logits=(K,) 候选路径评分
- **训练时动作**：sample ~ Categorical(logits)，返回 int ∈ [0, K)
- **推理时动作**：deterministic=True，直接 argmax(logits)
- **路由**：
  1. 取第 action 条候选路径 path = paths[action]
  2. 对 path 中每条边 (u,v)：link_load[(u,v)] += demand, link_load[(v,u)] += demand
  3. MLU = max(link_load.values()) / capacity
- **Episode**：逐流顺序路由，共 n_flows=40 步，每步路由一条流

**关键设计**：逐流顺序路由，每步从 K=4 条候选路径中选择一条。候选路径由 nx.shortest_simple_paths 在去掉故障边的无向图上生成。

## 7. 奖励/损失计算

- **奖励**：r_t = -(MLU_after - MLU_before)，增量式，鼓励每步最小化 MLU 增量
- **E2E 延迟**：E2E delay = Σ(propagation × 1/(1-util))，拥塞惩罚权重。propagation = dist_km / c，util = link_load / capacity。当 util ≥ 1 时延迟因子取 CONGESTION_DELAY_CAP=100.0（溢出惩罚，避免无穷大）。此函数是拥塞放大因子而非物理排队延迟模型（仿真为确定性逐流路由，非泊松到达）。
- **回报**：G_t = Σ_{k=0}^{T-t} γ^k · r_{t+k}
- **优势**：A_t = GAE(δ_t, λ=0.95)，δ_t = r_t + γ·V(s_{t+1}) - V(s_t)
- **PPO 损失**：
  - actor: -min(ratio·A, clip(ratio, 0.8, 1.2)·A) - 0.01·entropy
  - critic: 0.5·(V_pred - G)^2
  - 总计: L_actor + 0.5·L_critic

**与 per-edge 范式的区别**：奖励从绝对 -MLU 改为增量 -(MLU_after - MLU_before)。增量奖励更适合逐流路由：每步的奖励直接反映该步路由决策的质量。

## 8. 跨规模泛化

### 维度变化表

| 规模 | P × S | N | E | 流量 |
|------|-------|---|---|------|
| 训练 | 6×11 | 66 | 264 | 40 |
| 泛化 | 4×12 | 48 | 192 | 29 |
| 泛化 | 12×24 | 288 | 1152 | 173 |
| 泛化 | 36×20 | 720 | 2880 | 432 |

### 泛化流程

1. 创建目标规模 SimConfig → RoutingEnv → obs with new N, E
2. 加载 66 节点训练的模型
3. **GATEncoder**：Linear(7→64) 维度无关 ✓；GATConv 操作任意大小图 ✓
4. **PathScoringHead**：per-path MLP(mean(node_emb[path])) 与图规模无关 ✓
5. **ValueHead**：cat(src_emb, dst_emb) → FC，维度无关 ✓
6. **无 log_std**：离散动作空间，无需固定维度参数 ✓（解决了 per-edge 范式的泛化限制）
7. 候选路径由 env 的 nx.shortest_simple_paths 生成，模型只做评分选择 ✓

### 泛化时的特征一致性

- 节点特征 (N, 7)：全部归一化（/capacity），与规模无关 ✓
- 边特征 (E, 4)：同上，全部归一化 ✓
- 流量：按 0.6 × N_nodes 缩放，demand 范围不变 ✓

### 已知限制

1. **极地间隙已实现**：polar_gap_lat=70° 已在拓扑构建中生效，高纬度卫星的 inter-plane ISL 被断开。
2. **距离感知路由**：distance_km 由物理仿真计算（非固定 1.0），propagation delay 用于 E2E 延迟计算。模型可学习距离感知路由。
3. **路径缓存**：K 候选路径缓存于 (src, dst) 对，不跨 episode。大规模图路径生成可能成为瓶颈。

## 断层检查

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 特征缺失 | ✅ 无断层 | 模型有 is_current_src/dst 和 is_hotspot 提供当前流信息；有 utilization 提供负载信息 |
| 2 | 维度不匹配 | ✅ 无断层 | GNN + PathScoringHead 全部维度无关；消融实验 MLP 与 GNN 共享 env obs 接口 |
| 3 | 配置矛盾 | ✅ 无断层 | demand/capacity 比率在 MVE 验证范围内；故障率 8% 与 MVE-2 一致 |
| 4 | 跨规模断裂 | ✅ 已解决 | K-path 离散动作空间无需 log_std，泛化无需 deterministic 限制 |
