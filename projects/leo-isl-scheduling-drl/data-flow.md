# 端到端数据流推演 — LEO ISL Scheduling GNN-DRL

> 产出阶段：Contract Step 4
> 用途：Execute 阶段实现 GNN-DRL 的设计文档

---

## 1. 网络配置 → 节点位置

- **输入**：N_PLANES=24, SATS_PER_PLANE=66, altitude=550km, inclination=53°
- **处理**：OrbitPropagator 按 Walker Delta 构型初始化 1584 颗卫星的 ECI 坐标，每步用二体力学外推 τ=10s
- **输出**：positions (1584, 3) ECI 坐标矩阵

验证：24×66=1584 ✓，RAAN 间隔 15° ✓

## 2. 拓扑连接 → 候选链路属性

- **输入**：positions (1584, 3)
- **处理**：VisibilityConnectivity 计算 LoS（地球遮挡）+ 距离 < Z_MAX=3000km + FOR 角度 < 60° → 生成候选 ISL 列表
- **输出**：candidate_edges = [(i, j, distance_km), ...]，约 3000-4000 条（N_LCT=3 时约 3072 条）

注意：同轨 ISL（环形永久连接）不占 N_LCT 配额，仅跨轨 ISL 参与 DRL 决策。当前实现中同轨/跨轨混合，需在 Execute 阶段确认同轨链路是否包含在 candidate_edges 中。

## 3. 流量生成

- **输入**：positions（ECI→LLA 转换）、N_GS=100
- **处理**：TrafficGenerator 使用 GHS-POP 重力模型分布地面站，生成 (src_sat, dst_sat, demand_gbps) 流量对。每颗卫星关联最近的地面站作为源/目的。
- **输出**：flows = [(src, dst, demand), ...]，约 50-200 条活跃流

## 4. 状态构造

- **输入**：candidate_edges, isl_state, flows, positions
- **节点特征** (per satellite, 6-dim)：
  | 维度 | 名称 | 范围 | 含义 |
  |------|------|------|------|
  | 0 | supply | [0,1] | 归一化出流量（supply/max_sd）|
  | 1 | demand | [0,1] | 归一化入流量（demand/max_sd）|
  | 2 | lat | [-1,1] | 归一化纬度（lat/(π/2)）|
  | 3 | lon | [-1,1] | 归一化经度（lon/π）|
  | 4 | n_active | [0,1] | 归一化活跃 ISL 数（n_active/N_LCT）|
  | 5 | n_setup | [0,1] | 归一化建链中 ISL 数（n_setup/N_LCT）|
- **边特征** (per candidate, 7-dim)：
  | 维度 | 名称 | 范围 | 含义 |
  |------|------|------|------|
  | 0 | capacity | [0,1] | 归一化链路容量（cap/max_cap）|
  | 1 | distance | [0,1] | 归一化距离（d/Z_MAX）|
  | 2 | is_active | {0,1} | 当前是否活跃 |
  | 3 | is_in_setup | {0,1} | 当前是否在建链中 |
  | 4 | setup_remaining | [0,1] | 归一化剩余建链时间 |
  | 5 | active_duration | [0,1] | log 归一化已持续时间 |
  | 6 | outage_prob | [0,1] | 中断概率 |
- **输出**：node_feat (1584, 6), edge_feat (E, 7), edge_index from candidate_edges

### 断层检查

- ✅ 所有特征已归一化到 [0,1] 或 [-1,1]
- ✅ 维度固定（6 + 7），不随规模变化
- ⚠️ 缺少**链路级负载**特征（当前 ISL 上承载的流量）。GNN 可从 supply/demand + 拓扑推断，但显式特征可能帮助收敛。标记为已知限制，消融实验可测试。
- ⚠️ 缺少**流量目的地**的显式编码（目的地 PE）。当前 supply/demand 隐含流量模式，但对多源多目路由可能不够。标记为 Execute 阶段快速验证项。

## 5. 模型输入（GNN）

- **输入**：node_feat (N, 6), edge_feat (E, 7), edge_index (2, E)
- **处理**：
  1. 将 candidate_edges 转为 PyG 格式 edge_index (2, E) LongTensor
  2. 节点特征投影：Linear(6, 64) → node_embed (N, 64)
  3. 边特征投影：Linear(7, 64) → edge_embed (E, 64)
  4. GATv2 × 3 层（4-head, 64-dim）消息传递 → 更新 node_embed (N, 64)
  5. 边解码器：concat(src_embed, dst_embed) (E, 128) → MLP(128→64→32→1) → sigmoid → edge_score (E,) ∈ [0,1]
  6. Critic 分支：global_mean_pool(node_embed) (1, 64) → MLP(64→32→1) → value_scalar
- **输出**：
  - actor_output: edge_scores (E,) ∈ [0,1]
  - critic_output: value scalar

### 维度推演

| 层 | 输入 | 输出 |
|----|------|------|
| NodeProjection | (N, 6) | (N, 64) |
| EdgeProjection | (E, 7) | (E, 64) |
| GATv2-1 | (N, 64) + edge_index | (N, 64) |
| GATv2-2 | (N, 64) + edge_index | (N, 64) |
| GATv2-3 | (N, 64) + edge_index | (N, 64) |
| EdgeDecoder | (E, 128) [concat src+dst] | (E, 1) → sigmoid |
| CriticPool | (N, 64) | (1, 64) |
| CriticMLP | (1, 64) | (1, 1) |

### 注意

- GATv2 消息传递使用 edge_feat 作为边属性（edge-aware attention），需确认 PyG GATv2Conv 支持 edge_attr 参数。标准 GATv2Conv 支持，但需要设置 edge_dim=64。
- 边解码器 concat(src_embed, dst_embed) 是无序的（edge i→j 和 j→i 得到不同输入），但 edge_index 中每条边只出现一次（无向图），因此无问题。

## 6. 模型输出 → 动作映射

- **输入**：edge_scores (E,) ∈ [0,1]
- **处理**：环境 `_apply_lct(scores)` 方法：
  1. 按卫星分组候选边
  2. 每颗卫星按 score 降序排列
  3. 每颗卫星取 top-N_LCT=3 条
  4. 所有卫星的选中边合并为 selected 集合
- **输出**：selected edge set，满足每卫星 ≤ 3 条跨轨 ISL

### 动作空间说明

- 候选边数 E 随时间步动态变化（~3000-4000）
- 每颗卫星的候选数不等（赤道多、极区少）
- top-K 选择保证 N_LCT 约束硬满足
- 训练时可用 Gumbel noise 探索

## 7. 奖励/损失计算

- **输入**：routing result, n_changed, n_new, setup_delays, n_active_prev
- **处理**：
  - R_tput = delivered / total_demand ∈ [0,1]
  - C_switch = n_changed / n_active_prev ∈ [0,1]
  - C_setup = total_setup_delay / max_possible ∈ [0,1]
  - reward = 1.0·R_tput − 0.3·C_switch − 0.2·C_setup ∈ [-0.5, 1.0]
- **输出**：标量 reward + breakdown dict

### Contract 修正

Contract 原写奖励为 `w₁·M1 − w₂·M3 + w₃·M5`（含公平性），但实现使用 `w₁·R_tput − w₂·C_switch − w₃·C_setup`（含 setup 成本）。**以实现为准**修正 Contract：
- M5 (公平性) 作为评估指标，不参与奖励（避免训练不稳定）
- C_setup (建链延迟成本) 反映 L04 的 setup delay 物理约束，应保留在奖励中

## 8. 评估指标

- **输入**：MetricsCollector 每步累积的数据
- **处理**：
  - M1 = Σ delivered / Σ total_demand（吞吐量）
  - M2 = Σ (hop_count × hop_delay + prop_delay) / n_flows（平均时延）
  - M3 = Σ n_changed / Σ n_active（切换率）
  - M4 = 1 − M1（阻塞率）
  - M5 = Jain 公平指数 = (Σ throughput_i)² / (N × Σ throughput_i²)
- **输出**：metrics dict {M1, M2, M3, M4, M5}

## 跨规模泛化

- **训练配置**：24×66=1584（全规模训练，与评估规模一致）
- **辅助训练**：24×20=480（快速验证和消融实验用）
- **推理配置**：24×66=1584
- **变化维度**：
  - 节点数 N：480 → 1584（GNN 消息传递与 N 无关）
  - 候选边数 E：~1200 → ~3000（动作空间动态，top-K 处理）
  - 特征维度：固定 6-dim node + 7-dim edge（不变）
- **处理方式**：GNN 天然支持变图规模，无需特殊处理。唯一注意：归一化中的 max_cap/max_sd 随规模变化，已使用 per-step 归一化。

## 已知限制

1. **同轨 ISL 处理**：当前 candidate_edges 可能包含同轨永久链路。Execute 阶段需确认同轨链路是否从 DRL 决策中排除（固定保持，不占 N_LCT 配额）。
2. **链路级负载缺失**：状态不含当前 ISL 上承载流量，GNN 需从全局信息推断拥塞。
3. **流量目的地编码**：缺少显式 destination PE，可能影响多源多目路由场景。
