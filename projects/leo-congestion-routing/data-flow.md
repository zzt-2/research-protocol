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

- **输入**：obs dict {node_feat(N,6), edge_index(2,E), edge_feat(E,4), paths, flow, n_valid}
- **处理**：
  1. GATEncoder.in_proj: Linear(6, 64) → h=(N, 64)
  2. GAT Layer ×2: GATConv(h, edge_index, edge_attr) → LayerNorm → ELU + Residual → h=(N, 64)
  3. PathScoringHead: 对每条候选路径 path ∈ paths[:n_valid]:
     mean(node_emb[path_nodes]) → MLP(64→32→1) → scalar score
     n_valid < K 的位置填充 -1e9 (无效动作 mask)
  4. ValueHead: cat(node_emb[src], node_emb[dst]) → FC(128→64→1) → scalar

- **输出**：logits=(K,) 用于 Categorical 分布, value=scalar

**参数量**：
- GATEncoder: in_proj(6×64=384) + 2×GATConv(~16K each) + 2×LN(128) ≈ 33K
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
3. **GATEncoder**：Linear(6→64) 维度无关 ✓；GATConv 操作任意大小图 ✓
4. **PathScoringHead**：per-path MLP(mean(node_emb[path])) 与图规模无关 ✓
5. **ValueHead**：cat(src_emb, dst_emb) → FC，维度无关 ✓
6. **无 log_std**：离散动作空间，无需固定维度参数 ✓（解决了 per-edge 范式的泛化限制）
7. 候选路径由 env 的 nx.shortest_simple_paths 生成，模型只做评分选择 ✓

### 泛化时的特征一致性

- 节点特征 (N, 6)：全部归一化（/capacity），与规模无关 ✓
- 边特征 (E, 4)：同上，全部归一化 ✓
- 流量：按 0.6 × N_nodes 缩放，demand 范围不变 ✓

### 已知限制

1. **极地间隙未实现**：config 有 polar_gap_lat=70° 但 topology/failures 未使用。真实 LEO 星座在高纬度断开 inter-plane ISL。当前简化模型通过随机故障近似此效果。
2. **distance_km=1.0**：所有链路距离相同，模型无法学习距离感知路由。
3. **路径缓存**：K 候选路径缓存于 (src, dst) 对，不跨 episode。大规模图路径生成可能成为瓶颈。

## 断层检查

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 特征缺失 | ✅ 无断层 | 模型有 is_current_src/dst 和 is_hotspot 提供当前流信息；有 utilization 提供负载信息 |
| 2 | 维度不匹配 | ✅ 无断层 | GNN + PathScoringHead 全部维度无关；消融实验 MLP 与 GNN 共享 env obs 接口 |
| 3 | 配置矛盾 | ✅ 无断层 | demand/capacity 比率在 MVE 验证范围内；故障率 8% 与 MVE-2 一致 |
| 4 | 跨规模断裂 | ✅ 已解决 | K-path 离散动作空间无需 log_std，泛化无需 deterministic 限制 |
