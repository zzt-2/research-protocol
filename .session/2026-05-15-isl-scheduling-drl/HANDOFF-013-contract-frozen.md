# Handoff 2026-05-15 (Round 13) — Contract 冻结

## 当前进度
- **阶段：Contract 已冻结，待进入 Execute**
- Contract 状态：**frozen**（用户确认 2026-05-15）
- 本轮完成：方案新颖性验证、假设形成、Contract 起草、参数溯源（0 ASSUMPTION）、端到端推演、压力测试
- 2 次 commit：Contract 产物 + handoff

## 项目背景

LEO 巨型星座（Starlink Phase I, 24×66=1584 星）ISL 调度问题。核心约束 N_LCT=3（每卫星最多 3 条跨轨 ISL），固定贪心 M1=17.09%，无限 ISL M1=28.19%，gap=11.1%。GNN-DRL 方法用 GATv2 做拓扑感知边级评分，PPO 在线学习 ISL 选择策略。

### 问题重设定（D012，关键上下文）
原问题 B1 无限 ISL（4752 边/6.0 每星）M1=28.19%，DRL 无优化空间。多路径路由仅 +5.3% 确认瓶颈在拓扑非路由。加 N_LCT 约束后：
- N_LCT=4 gap 仅 1.9%（不够）
- **N_LCT=3 gap=11.1%（甜点）**
- N_LCT=2 gap=20.0%（太极端）
- 参数鲁棒性扫描 9/9 配置 gap>5%，平均 11.3%

### GW 产出（已完成）
- 15 篇文献（12 精读 + 3 浅读），GNN+DRL 细粒度 ISL 调度为文献空白
- 仿真器 8 模块全部实现并验证（orbit/visibility/channel/traffic/router/reward/metrics/environment）
- B1(+Grid/Fixed) 和 B2(Wang MADRL) 已复现
- 代码质量模板体系：`code-quality.md` + `reference/sim-template/`

## Contract 核心摘要

### 假设与信号
- **假设**: GAT-PPO 拓扑感知 ISL 调度（逐边评分 + top-3）在 N_LCT=3 下 M1≥25%
- **Success**: M1≥25% AND GNN 消融≥3pp AND 训练稳定（3/5 种子收敛）
- **Failure**: M1<19% OR GNN 消融<1pp OR 训练不稳定（≥2/5 种子失败）

### Baselines
- B1: +Grid/Fixed（5 篇共识，已复现，M1=17.09% @N_LCT=3 全规模）
- B2: Wang TCOM MADRL（IEEE TCOM Q1，已实现，测试规模未优于 B1，全规模待验证）

### 奖励函数
- r = 1.0·R_tput − 0.3·C_switch − 0.2·C_setup
- R_tput = delivered/total_demand ∈ [0,1]
- C_switch = n_changed/n_active_prev ∈ [0,1]
- C_setup = total_setup_delay/max_possible ∈ [0,1]
- 范围 [-0.5, 1.0]
- **注意**：M5(公平性)仅作评估指标，不参与奖励（D013 修正）

### 消融计划
| 编号 | 消融 | 预期 |
|------|------|------|
| A1 | GNN→FC（3层MLP替换GATv2） | 大幅下降 ≥3pp |
| A2 | 细粒度→粗粒度（top-3→8选1固定候选集） | 中等下降 1-3pp |
| A3 | 移除切换惩罚（奖励去掉 w₂·C_switch） | M3 升高 |
| A4 | 无参数共享（每卫星独立网络） | 收敛变慢 |

### 实验列表
E01: 核心对比(P0) | E02: A1(P0) | E03: A2(P1) | E04: A3(P1) | E05: 参数鲁棒(P1) | E06: 规模泛化(P2)

### 关键参数
- 星座: 24×66=1584, 550km, 53°
- ISL: Gaussian beam, λ=1.55μm, P₀=20W, B=1GHz, σ_J=10μrad
- N_LCT=3, Z_MAX=3000km, demand=10Gbps, N_GS=100
- Episode: 50步 × τ=10s
- GNN: GATv2 4-head 64-dim × 3层, PPO lr=3e-4
- 评估: 5 随机种子, 配对 t 检验 p<0.05

## 已有仿真器代码

### 目录结构
```
projects/leo-isl-scheduling-drl/
├── simulator/
│   ├── config.py        # 模块常量（N_LCT=2 需改为 3）
│   ├── environment.py   # ISLEnvironment（已实现完整 MDP）
│   ├── orbit.py          # OrbitPropagator（二体力学）
│   ├── visibility.py     # VisibilityConnectivity（LoS+距离+FOR）
│   ├── channel.py        # ChannelModel（Gaussian beam）
│   ├── traffic.py        # TrafficGenerator（GHS-POP）
│   ├── router.py         # Router（Dijkstra，含多路径）
│   ├── reward.py         # RewardCalculator（3项归一化）
│   └── metrics.py        # MetricsCollector（M1-M5）
├── baselines/
│   ├── grid_fixed.py     # B1 +Grid/Fixed（含 N_LCT 约束）
│   └── wang_madrl.py     # B2 Wang TCOM MADRL
├── verify/               # 验证脚本
├── contract.md           # frozen Contract
├── data-flow.md          # 8步端到端推演
├── decision_log.md       # D001-D014
├── baseline_report.md    # B1+B2 复现报告
└── literature_notes.md   # 15篇文献精读
```

### 环境 API（environment.py）
```python
env = ISLEnvironment(n_planes=24, sats_per_plane=66, seed=42)
obs, info = env.reset()

# obs 结构：
#   node_features: (N, 6) — [supply, demand, lat, lon, n_active, n_setup] 归一化到 [0,1]
#   edge_features: (E, 7) — [capacity, distance, is_active, is_in_setup, setup_remaining, duration, outage_prob]
#   candidate_edges: [(i, j, distance_km), ...]
#   n_candidates: int

# step 输入：
scores = model(obs)  # (E,) ∈ [0,1]，每条候选边一个分数
obs, reward, terminated, truncated, info = env.step(scores)

# 环境内部 _apply_lct(scores) 自动做 top-N_LCT per satellite
# ISL 状态机：inactive → in_setup → active，有 setup delay (2-30s)
```

### config.py 需更新项
- `N_LCT = 2` → `N_LCT = 3`（第 19 行）

## 下一步：Execute 阶段

### 恢复文件（按顺序）
1. 本文件（HANDOFF-013）
2. `stages/execute.md`（Execute 阶段流程）
3. `code-quality.md`（必做清单）+ `reference/sim-template/`（模板代码）
4. `projects/leo-isl-scheduling-drl/data-flow.md`（8步推演，含维度表）
5. `projects/leo-isl-scheduling-drl/contract.md`（frozen，需要时查参数）

### Execute Step 0 实现任务
1. **更新 config.py**: N_LCT=2→3
2. **实现 GATv2ActorCritic 模型**（新文件 `simulator/model_gat.py`）：
   - 继承 `reference/sim-template/model_gnn.py` 的 BaseActorCritic 接口
   - 但**重写** `_encode`：不做 global pooling，改为返回节点嵌入 (N, 64)
   - Actor 分支：edge decoder（concat src+dst → MLP 128→64→32→1 → sigmoid）输出边级分数
   - Critic 分支：global_mean_pool → MLP 64→32→1 输出 value
   - GATv2Conv 4-head 64-dim × 3 层，edge_dim=64（边特征投影后维度），LayerNorm + 残差
   - `get_action`：输出 scores (E,)，不做 Categorical 采样（环境自己 top-K）
   - `evaluate_actions`：返回 (log_probs, values, entropy)
3. **实现 PPO 训练循环**（新文件 `simulator/train.py`）：
   - 直接用 `reference/sim-template/train_ppo.py` 的 PPO + RolloutBuffer + RewardNormalizer + EarlyStopping
   - 关键适配：env.step(scores) 接收连续 scores 而非离散 action，需在 train loop 中处理
   - 必须有 wandb + early stopping + save best model
4. **逐模块验证**（每模块 10 行 assertion，记入 decision_log）

### Execute Step 1-4
- Step 1: Quick Test（24×20 小规模，验证训练收敛）
- Step 2: E01 核心对比（24×66 全规模，5 种子）
- Step 3: 假设判定
- Step 4: 消融（E02-E04）+ 鲁棒性（E05）

### 代码质量必做项（来自 code-quality.md）
- [ ] GNN 模型继承 BaseActorCritic 接口
- [ ] 用 PyG 标准层（GATv2Conv），不手写稀疏操作
- [ ] Actor-Critic 共享 GNN backbone
- [ ] PPO: GAE + advantage norm + grad clip(0.5) + LR decay
- [ ] 集成 wandb/tensorboard
- [ ] early stopping（reward plateau + KL 双条件）
- [ ] save/load 包含 optimizer + step_count + normalizer
- [ ] 训练中保存 best model

### 已知坑
- 同轨 ISL 是否包含在 candidate_edges 中需确认（data-flow.md 已标记）
- 缺少链路级负载特征和流量目的地 PE（标记为已知限制，消融可测）
- 环境不继承 gymnasium.Env（可工作但非标准，Execute 阶段不改）
