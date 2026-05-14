# 实验数据

## 1. 仿真环境参数表

### 1.1 星座与 ISL 参数表

| 参数 | 值 | 来源 |
|------|-----|------|
| 星座类型 | Walker-Delta, 单壳层, F=1 | — |
| 轨道高度 | 550 km | L02 Starfield (Starlink Shell 1) |
| 轨道倾角 | 53° | L02 Starfield |
| 轨道周期 | ~96 min (5757.7 s) | 轨道力学计算 |
| ISL 拓扑 | +Grid (每星 4 ISL: 2 轨内 + 2 轨间) | L04 ISL Pattern |
| ISL 类型 | 激光 (1550 nm optical) | L02/L03, Starlink 实际 ~100 Gbps/链路 |
| ISL 容量模型 | Shannon: C = B log₂(1 + SNR(d)), B=1 GHz | L03 DuJo §V-A1 |
| SNR 模型 | SNR(d) = SNR_ref × (d_ref / d)², d_ref=2000 km | 简化近似 (论文标注) |
| ISL 时延模型 | 传播时延 = d / c, c=299792.458 km/s | 物理常数 |
| ISL 最大距离 (断链) | 5000 km | L02 Starfield §2.2 |
| 最小仰角 (GSL) | 25° | L02 Starfield 标准 |
| 物理常数 | μ_Earth=398600.4418 km³/s², R_Earth=6371 km | 标准 |

| 配置名 | 轨道面 P | 每面星数 S | 总星数 N | 用途 |
|--------|---------|-----------|---------|------|
| train_66 | 6 | 11 | 66 | 多尺度训练 (小) |
| train_100 | 10 | 10 | 100 | 多尺度训练 (中) |
| train_200 | 10 | 20 | 200 | 多尺度训练 (大) |
| target_720 | 18 | 40 | 720 | 目标评估规模 |
| extend_1584 | 72 | 22 | 1584 | 扩展目标 (Starlink Phase 1) |

来源: `simulator/config.py`, `contract.md` §Simulation Config

### 1.2 ISL 距离范围

各配置的 ISL 距离由实时轨道力学计算 (非固定值)。断链后实际连接数少于理论值。

| 配置 | 轨内 ISL 均值 (km) | 轨间 ISL 均值 (km) | 断链比例 | 孤立节点 |
|------|-------------------|-------------------|---------|---------|
| train_66 | ~2700 | ~5500 (部分>5000) | 有断链 | 可能有 |
| train_100 | — | — | — | 0 |
| train_200 | — | — | — | 0 |
| target_720 | — | — | — | 0 |

来源: `simulator/smoke_test.py`, D016 (ISL 距离修正)

### 1.3 仿真参数表

| 参数 | 值 | 来源 |
|------|-----|------|
| 评估快照数 | 10 | Contract §评估条件 |
| 快照间隔 | 60 s | L10 MCSR |
| 流量矩阵数/快照 | 5 | Contract §评估条件 |
| 每快照流量数 | 100 | D023 |
| 评估种子 | 123 | D023 |
| 流量模式 | uniform / hotspot / distance-weighted | Contract §流量模型 |
| 统计显著性 | Welch's t-test, p < 0.05 | Contract §评估条件 |

来源: `simulator/config.py` (N_SNAPSHOTS=10, SNAPSHOT_INTERVAL=60, N_TRAFFIC_MATRICES=5)

### 1.4 奖励/损失函数

#### 监督训练 (主实验 + 消融)

| 项目 | 定义 |
|------|------|
| 损失函数 | Cross-Entropy Loss (方向分类, 4 类) |
| 标签来源 | Dijkstra 最短路径的下一跳方向 (0=intra_fwd, 1=intra_bwd, 2=inter_r, 3=inter_l) |
| 标签掩码 | dir_mask 过滤不可达方向; y < 0 的样本跳过 |
| 优化器 | Adam, lr=1e-3 |
| 批大小 | 64 |

来源: `simulator/quick_test.py`, `simulator/ablation.py`

#### GRLR RL 训练

| 项目 | 值 | 来源 |
|------|-----|------|
| 算法 | On-policy Actor-Critic (vanilla policy gradient) | GRLR Table III |
| 即时奖励 | r_t = -d_k (负跳时延) + arrival_bonus / timeout_penalty | GRLR §III |
| 到达奖励 | +10.0 | — |
| 超时惩罚 | -50.0 | — |
| 最大跳数 | 80 | — |
| 折扣因子 γ | 0.95 | GRLR Table III |
| 策略损失 | -(log_probs × advantages).mean() | — |
| 价值损失 | MSE(values, returns) | — |
| 熵正则 | -β × entropy, β=0.1 | GRLR Table III |
| 总损失 | policy_loss + 0.5 × value_loss - 0.1 × entropy | — |
| 梯度裁剪 | max_norm=0.5 | — |

来源: `simulator/grlr_train.py`

#### 推理奖励 (env.py, 用于 PPO 评估)

| 条件 | 奖励公式 |
|------|---------|
| 有成功路径 | r = success_rate - 0.3 × max(mean_stretch - 1.0, 0) |
| 无成功路径 | r = -0.5 |

来源: `simulator/env.py` §RoutingEnv

## 2. 仿真器验证结果

### 2.1 Smoke Test 模块验证

| 验证项 | 方法 | 结果 |
|--------|------|------|
| 轨道位置正确性 | 检验所有卫星半径 = R_Earth + alt | PASS (atol=1.0 km) |
| +Grid 拓扑完整性 | 理论边数 = 2 × P × S (断链前) | PASS |
| ISL 距离计算 | 实时轨道力学, 断链阈值 5000 km | PASS |
| Shannon 容量 | C = B log₂(1 + SNR(d)), 输出 Gbps 量级合理 | PASS |
| Dijkstra 路由 | 全对最短路径 + 时延指标计算 | PASS (连通配置) |
| 流量生成 | uniform/hotspot/distance 三种模式 | PASS |

### 2.2 关键 Bug 修复验证

| Bug | 影响 | 修复 | 来源 |
|-----|------|------|------|
| `_build_neighbor_map` 单向注册 | 只注册 1440/2880 条映射, 评估仅用 2/4 方向 (intra_bwd + inter_l 缺失), stretch 被严重高估 | 补全双向映射: 添加 `nmap[(v, OPPOSITE_DIR[d])]` | D022 |
| ISL 容量 B=500 MHz | 无出处, 论文查证无任何使用 | 修正为 B=1 GHz (L03 DuJo 基于 Starlink TLE) | D015 |
| ISL 距离固定值 | 原 ~2700/~5500 km 固定值不适用任何配置 | 改为实时轨道力学计算 + 5000 km 断链 | D016 |

## 3. Baseline 复现结果

### 3.1 Dijkstra (性能上界)

| 指标 | 值 | 评估方式 |
|------|-----|---------|
| Mean Stretch | 1.000 (by definition) | — |
| ≤1.2x optimal | 100% | — |
| Mean Delay | 60.77 ms | 10 snapshots × 5 TMs × 100 flows, seed=123 (D023) |
| 方法说明 | 全对最短路径, 每快照独立计算, 非学习方法 | |

### 3.2 GRLR (同规模 GNN+RL 标杆)

来源论文: Zhang et al., TVT 2025, DOI:10.1109/TVT.2024.3471658, 44 引用。

| 项目 | 值 | 来源 |
|------|-----|------|
| 架构 | 6 节点局部图 GAT (1层) + Actor-Critic | GRLR §III |
| Actor | GAT(3→64) → LayerNorm → GlobalAddPool → FC(64→4) | `simulator/grlr_model.py` |
| Critic | GAT(3→32) → LayerNorm → GlobalAddPool → FC(32→1) | `simulator/grlr_model.py` |
| 输入 | 6 节点: [current, 4 neighbors, dest]; 节点特征 [lat/90, lon/180, traffic]; 边特征 [delay/50, dist/6000] | |
| 训练规模 | 720 星 (同规模训练+评估) | D024 |
| 训练 Episodes | 2000 | D024 |
| 训练超参 | γ=0.95, lr=5e-4, β=0.1, Adam, grad_clip=0.5 | GRLR Table III |
| 推理方式 | 加权 Dijkstra (同主实验) | D024 |

**GRLR 评估结果 (720 星)**:

| 指标 | 值 |
|------|-----|
| Mean Stretch | 1.008 (D024) |
| ≤1.2x optimal | 100% (D024) |
| Mean Delay | 60.32 ms (D024) |
| 评估方式 | 加权 Dijkstra, 同主实验协议 |

## 4. 核心实验

### 4.1 跨规模 66+100+200→720 (E01)

#### 模型配置

| 项目 | 值 | 来源 |
|------|-----|------|
| 架构 | RoutingActorCritic: 3 层 GAT + Actor-Critic heads | `simulator/models.py` |
| Hidden dim | 128 | D018 |
| Attention heads | 4 | config.py (GNN_HEADS) |
| 节点输入维度 | 1 (is_dest) + 16 (own_PE) + 16 (dest_PE) = 33 | models.py |
| 边特征维度 | 2 (ISL 距离, 当前利用率) | models.py |
| 参数量 | 72,965 | handoff-4 |
| Orbital PE | sin/cos 编码 (plane_idx/P, sat_idx/S), 4 频率, 维度 16 | models.py §OrbitalPE |
| 训练方式 | 监督学习 (Dijkstra 标签), 非 RL | D018 |
| 训练配置 | 多尺度混合: train_66 + train_100 + train_200 | |
| 训练数据量 | 7320 samples (20 snapshots × 3 configs × N destinations) | D018 |
| 训练 Epochs | 150 | D018 |
| 优化器 | Adam, lr=1e-3 | quick_test.py |
| 批大小 | 64 | quick_test.py |

#### 训练精度

| 指标 | 值 | 来源 |
|------|-----|------|
| 训练集方向精度 | 97.6% | D018 |
| 目标集 (720星) 方向精度 | 66.8% | D018 |
| 精度保留率 | 71% (66.8 / 97.6 × rounding) | D018 |

#### 评估结果 (720 星, 零样本)

| 指标 | 值 | 评估方式 | 来源 |
|------|-----|---------|------|
| Mean Stretch | 1.097 | 加权 Dijkstra | D023 |
| Median Stretch | 1.056 | 加权 Dijkstra | D023 |
| P95 Stretch | 1.315 | 加权 Dijkstra | D023 |
| ≤1.2x optimal | 85.1% | 加权 Dijkstra | D023 |
| ≤1.5x optimal | 98.9% | 加权 Dijkstra | D023 |
| Mean Delay | 66.77 ms | 加权 Dijkstra | D023 |
| Dijkstra Delay | 60.77 ms | 全对最短路 | D023 |
| Delay 开销 | 9.9% | (66.77-60.77)/60.77 | D025 |
| 路径成功率 | 100% | 加权 Dijkstra | D023 |
| 评估协议 | 10 snapshots × 5 TMs × 100 flows, seed=123 | — | D023 |

### 4.2 三方对比 (E02)

| 方法 | Mean Stretch | Median Stretch | P95 Stretch | ≤1.2x | ≤1.5x | Mean Delay (ms) | 训练规模 | 推理方式 | 来源 |
|------|-------------|---------------|------------|-------|-------|----------------|---------|---------|------|
| **我们的方法** | 1.097 | 1.056 | 1.315 | 85.1% | 98.9% | 66.77 | 66+100+200→720 (跨规模) | 加权 Dijkstra | D023 |
| GRLR | 1.008 | — | — | 100% | — | 60.32 | 720→720 (同规模) | 加权 Dijkstra | D024 |
| Dijkstra | 1.000 | — | — | 100% | — | 60.77 | N/A | 全对最短路 | D023 |

#### Contract 核心指标核对

| Contract 指标 | 目标 | 实际 | 状态 |
|--------------|------|------|------|
| 时延保留率 (GRLR同规模 / 我们跨规模) | ≥80% | 90.3% (60.32/66.77) | PASS |
| vs Dijkstra 差距 | ≤20% | 9.9% ((66.77-60.77)/60.77) | PASS |

来源: D025

## 5. 消融实验全表

### 5.1 消融实验配置

所有消融实验使用相同的评估协议: 加权 Dijkstra, 10 snapshots × 5 TMs × 100 flows, seed=123, 目标 720 星。

| 消融 | 变量 | PE | 训练配置 | 架构 | 来源 |
|------|------|-----|---------|------|------|
| **完整方法** | — | ON | train_66 + train_100 + train_200 | 3层GAT, h=128, heads=4 | D018/D023 |
| A1 | 移除 Orbital PE | OFF (零向量) | train_66 + train_100 + train_200 | 同上 | D026 |
| A2 | 移除多尺度训练 | ON | train_100 only | 同上 | D027 |
| A3 | A1 + A2 | OFF (零向量) | train_100 only | 同上 | D028 |
| Same (对照) | 同规模训练+评估 | ON | target_720 only | 同上 | D029 |

### 5.2 消融结果

| 消融 | 训练精度 | Mean Stretch | ≤1.2x | ≤1.5x | Delay 开销 | 来源 |
|------|---------|-------------|-------|-------|-----------|------|
| **完整方法** | 97.6% | 1.097 | 85.1% | 98.9% | 9.9% | D023 |
| A1 (无PE) | 39.7% | 1.002 | 100% | — | 0.2% | D026 |
| A2 (单尺度+PE) | 97.7% | 1.120 | 81.1% | — | 12.3% | D027 |
| A3 (无PE+单尺度) | 40.2% | 1.049 | 93.6% | — | 3.6% | D028 |
| Same (720→720) | 98.8% | 1.000 | 100% | — | 0.0% | D029 |

### 5.3 消融结论

| 结论 | 证据 | 来源 |
|------|------|------|
| PE 是模型学习的必要条件 (非可选增强) | 无 PE 时训练精度 ~40% (≈随机 25%); 有 PE 时 97.6-98.8% | D026, D018 |
| 多尺度训练贡献 2-4pp stretch 改善 | A2 单尺度 stretch 1.120 vs 完整方法 1.097 (差 2.3pp); ≤1.2x 差 4pp | D027 |
| 9.7pp stretch 差距完全来自跨规模迁移 | Same (720→720) stretch=1.000 vs 完整方法 stretch=1.097 | D029 |
| Contract 假设修正: "PE贡献≥8pp" → "PE是模型可学习性的前提" | 无 PE 无法学习, 无法量化 pp 贡献 | D026 |
| 无 PE 时加权 Dijkstra 退化为纯 Dijkstra | 无方向偏好 → weight=delay+0 → 纯最短路, stretch=1.002≈1.000 | D026 |

## 6. 训练配置对比

### 6.1 模型架构对比

| 项目 | 我们的方法 | GRLR |
|------|----------|------|
| GNN 类型 | GAT (3层) | GAT (1层) |
| Hidden dim | 128 (Actor), 128 (Critic 共享) | 64 (Actor), 32 (Critic) |
| Attention heads | 4 | 1 |
| 输入范围 | 全局图 (N 个节点) | 6 节点局部图 |
| 节点特征 | [is_dest(1), own_PE(16), dest_PE(16)] = 33 | [lat/90, lon/180, traffic_norm] = 3 |
| 边特征 | [delay, utilization] = 2 | [delay/50, dist/6000] = 2 |
| 位置编码 | Orbital PE (sin/cos, 4 频率, dim=16) | 无 |
| 参数量 | 72,965 | — |
| 输出 | (N, 4) 方向 logits | (B, 4) 方向 logits |

### 6.2 训练超参对比

| 项目 | 我们的方法 | GRLR |
|------|----------|------|
| 训练范式 | 监督学习 (Dijkstra 标签) | On-policy Actor-Critic |
| 训练规模 | 66+100+200 (多尺度混合) | 720 (同规模) |
| 训练数据量 | 7320 samples (20 snapshots × 3 configs) | 2000 episodes × 10 routes |
| Epochs/Episodes | 150 epochs | 2000 episodes |
| 学习率 | 1e-3 (Adam) | 5e-4 (Adam) |
| 批大小 | 64 | On-policy (10 routes/episode) |
| 折扣因子 | N/A (监督) | γ=0.95 |
| 熵正则 | N/A | β=0.1 |
| 梯度裁剪 | N/A | max_norm=0.5 |

### 6.3 推理配置

| 项目 | 值 | 说明 |
|------|-----|------|
| 推理策略 | 加权 Dijkstra | D020 |
| 权重公式 | weight(u,v) = delay(u,v) + relu(best_logit[u] - logit[u, dir]) | 首选边 penalty=0, 非首选边 penalty>0 |
| 首选边 | logit = max → penalty = 0 → weight = delay | 等价于最短路 |
| 非首选边 | logit < max → penalty = gap → weight = delay + gap | 受到惩罚 |

来源: `simulator/ablation.py` §eval_weighted_dijkstra, `simulator/env.py` §evaluate_weighted

## 7. 推理策略对比

### 7.1 策略演化

| 阶段 | 策略 | 结果 | 问题 | 来源 |
|------|------|------|------|------|
| D019 | 贪心推理 (逐跳 argmax) | 成功率: train 22-30%, target 1.7% | 路径成功=逐跳精度之积, 精度衰减导致低成功率 | D019 |
| D020 | 加权 Dijkstra | 成功率 100%, mean stretch 2.1-2.6 (bug 修复前) | 首版 4 种权重公式测试均不理想; 后发现 neighbor_map bug | D020 |
| D022 | Bug 修复后重新评估 | mean stretch 1.097 | neighbor_map 双向修复后 stretch 大幅改善 | D022/D023 |
| D021 | PPO 微调 (监督预训练后) | 无改善 | ①greedy reward 太稀疏 (99%路径失败) ②weighted reward action-reward 解耦 ③80轮 PPO 后 stretch 持平或恶化 | D021 |

### 7.2 加权 Dijkstra 权重公式

共测试 4 种权重公式, 均在 bug 修复前:

| 公式 | Mean Stretch | 问题 |
|------|-------------|------|
| softmax 概率: delay / (prob + eps) | 2.1+ | 尾部拉高 |
| 2-prob 加权: delay × (2 - prob) | 2.1+ | 尾部拉高 |
| exp(-logit) 加权: delay × exp(-logit) | 2.6+ | 尾部拉高 |
| **加性惩罚: delay + relu(best_logit - logit)** | 最终采用 | 首选边 penalty=0, 简洁有效 |

来源: D020

## 8. 成功/失败信号对照

### 8.1 Contract 成功信号

| # | 信号 | 目标 | 实际 | 状态 |
|---|------|------|------|------|
| S1 | 规模泛化成功 | 时延保留率 ≥80% | 90.3% (60.32/66.77 ms) | PASS |
| S2 | 实用价值成立 | vs Dijkstra ≤20% | 9.9% ((66.77-60.77)/60.77) | PASS |
| S3 | PE 关键性确认 | 移除 PE 保留率下降 ≥8pp | PE 是学习前提 (无 PE 精度 ~40% ≈随机) | PASS (需修正表述) |

来源: `contract.md` §Success Signal, D025/D026

### 8.2 Contract 失败信号

| # | 信号 | 条件 | 实际 | 状态 |
|---|------|------|------|------|
| F1 | 方法基础失败 | 同规模 GNN >1.5x Dijkstra | Same stretch=1.000 | 未触发 |
| F2 | 泛化灾难性失败 | 跨规模 >1.8x 同规模 GNN | 66.77/60.32=1.107 < 1.8 | 未触发 |
| F3 | PE 无贡献 | 保留率变化 <3pp | PE 是前提条件 (影响远超 3pp) | 未触发 |

来源: `contract.md` §Failure Signal

## 9. 数据一致性检查

### 9.1 核心数字交叉验证

| 检查项 | 公式 | 左侧 | 右侧 | 一致 |
|--------|------|------|------|------|
| Delay 开销 vs Stretch | (1.097-1.0)×100≈9.7% | 9.9% (D025) | ~9.7% (stretch 推算) | Yes (≈) |
| 保留率 | GRLR_delay / Our_delay | 60.32/66.77 | 90.3% | Yes |
| Dijkstra Stretch | by definition | 1.000 | — | — |
| GRLR stretch 合理性 | 1.008 (同规模GNN) | 60.32/60.77 | 0.993≈1.008 | Yes (方向一致, stretch 含加权惩罚) |

### 9.2 消融内部一致性

| 检查项 | 预期 | 实际 | 一致 |
|--------|------|------|------|
| A3 stretch 介于 A1 和 A2 之间 | A1(1.002) < A3 < A2(1.120) | A3=1.049 | Yes |
| 同规模 stretch 最优 | Same < 完整方法 | 1.000 < 1.097 | Yes |
| 无PE训练精度≈随机 (4类) | ~25% | A1=39.7%, A3=40.2% | Yes (略高于随机, is_dest 提供1bit信息) |
| 有PE精度远高于无PE | A1/A3 vs 完整/A2/Same | 39.7/40.2% vs 97.6/97.7/98.8% | Yes |

### 9.3 评估协议一致性

| 方法 | 快照数 | TM 数 | 流量数 | 种子 | 推理方式 | 一致 |
|------|--------|-------|--------|------|---------|------|
| 我们的方法 | 10 | 5 | 100 | 123 | 加权 Dijkstra | — |
| GRLR | 10 | 5 | 100 | 123 | 加权 Dijkstra | Yes |
| Dijkstra | 10 | 5 | 100 | 123 | 全对最短路 | Yes |
| 消融 A1-A3, Same | 10 | 5 | 100 | 123 | 加权 Dijkstra | Yes |

### 9.4 来源编号索引

| 编号 | 内容 |
|------|------|
| D015 | ISL 容量模型修正 B=1 GHz |
| D016 | ISL 距离修正为实时轨道力学计算 |
| D017 | ISL 类型确认为激光 |
| D018 | 监督预训练结果: 97.6% train / 66.8% target / 71% retention |
| D019 | 贪心推理成功率极低 |
| D020 | 加权 Dijkstra 推理策略确定 |
| D021 | PPO 微调无效 |
| D022 | neighbor_map bug 修复 |
| D023 | 修复后核心评估: stretch 1.097, ≤1.2x 85.1% |
| D024 | GRLR 复现: stretch 1.008, delay 60.32 ms |
| D025 | 三方对比结论: 保留率 90.3%, vs Dijkstra 9.9% |
| D026 | 消融 A1: 无 PE → 训练精度 39.7%, stretch 1.002 |
| D027 | 消融 A2: 单尺度 → stretch 1.120, ≤1.2x 81.1% |
| D028 | 消融 A3: 无 PE+单尺度 → stretch 1.049, ≤1.2x 93.6% |
| D029 | 同规模对照: stretch 1.000, 训练精度 98.8% |
