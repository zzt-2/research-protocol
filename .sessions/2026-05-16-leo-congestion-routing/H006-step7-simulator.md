# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 7（仿真器搭建 + Baseline 复现）
- 状态：Part A 完成（仿真器搭建 + 6 类验证全通过）
- Contract 状态：未开始
- 本轮完成：完整仿真器代码实现（8 个模块 + 3 个 baseline）

## 本轮产出文件

### 仿真器核心（`projects/leo-congestion-routing/simulator/`）
| 文件 | 行数 | 职责 |
|------|------|------|
| `config.py` | 79 | SimConfig dataclass，所有参数带默认值 |
| `topology.py` | 88 | Walker delta 拓扑生成，TopologyData(nx.DiGraph + edge_index + edge_features) |
| `traffic.py` | 79 | 非均匀流量生成（重型/轻型 + 热点 + 时变 NHPP + 突发） |
| `failures.py` | 111 | 链路故障注入（random/regional）+ rebuild_edge_structures |
| `env.py` | 278 | RoutingEnv(gymnasium.Env)，per-link 连续权重 → 加权最短路路由 → MLU |
| `model.py` | 222 | RoutingActorCritic（GAT encoder + EdgeWeightDecoder + Gaussian policy） |
| `train.py` | 670 | PPO 训练循环（连续版）+ RolloutBuffer + RewardNormalizer + EarlyStopping + wandb |
| `verify.py` | 683 | 6 类验证套件（解析/统计/退化/自相关/MDP trial/reward balance） |

### Baselines（`projects/leo-congestion-routing/baselines/`）
| 文件 | 行数 | 算法 |
|------|------|------|
| `sp.py` | 56 | Shortest Path（hop-count 权重全 1.0） |
| `ecmp.py` | 78 | Equal-Cost Multi-Path（nx.all_shortest_paths 均匀分配） |
| `mlp.py` | 345 | MLP 消融（无 message passing）+ 自含 PPO 训练 |
| `run_all.py` | 72 | 统一运行入口 |

## 验证结果（全部 PASS）
- 解析验证：reward = -MLU 精确匹配（2 节点 MLU=0.5）
- 统计验证：KS test p>0.01，故障率 8.33%≈8%
- 退化验证：确定性复现（同 seed 同 MLU），均匀流量 MLU=0.16
- 自相关验证：lag-1 ρ=-0.02 << 0.95
- MDP Trial：3 episodes 正常终止，reward 有限，obs 非空
- Reward Balance：策略有区分度（random vs uniform），方差=1.62

## 关键设计决策

1. **固定边集**：故障边保留在 edge_index 中（is_failed=1.0），不移除。原因：model.py 的 log_std 参数大小固定（264 for 66-node），移除边会导致 Normal 分布 mean/std 维度不匹配
2. **连续动作空间**：E 维正权重向量（softplus 保证正值），Dijkstra 加权最短路路由
3. **同时路由**：所有流用同一组权重同时路由（非逐流），符合 SDN 控制器范式
4. **env.py 列重映射**：topology.py 输出 [cap_norm, etype, dist_km, 0.0]，env.__init__ 重映射为 [utilization, edge_type, is_failed, capacity_norm]

## 已知问题（待修复）
- ECMP baseline 只计算第一步流量，未迭代 t_slots（与 SP 评估不一致）
- verify_analytical 中 2 节点测试因 n_planes=1 只产生 intra-plane 边（ring），不是严格的 2 节点 1 链路

## 下一步
1. **Part A-checkpoint: MDP 试运行**（gw-experiment.md §impl）
   - 跑 1 episode 随机策略 + 1 episode 贪心策略
   - 检查奖励分量占比（本项目只有 -MLU 单分量，应通过）
   - 质量门槛：贪心 > 随机 >10%，无单一项 >95%
2. **Part B: Baseline 复现**
   - 修复 ECMP 使其迭代 t_slots
   - 运行 SP + ECMP + MLP baseline，确认 DRL > 传统 > 随机
   - 写 baseline_report.md
3. **更新 master-state.md** Step 7 状态

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md` — Master 编排状态
- `projects/leo-congestion-routing/simulator-design.md` — 仿真器设计规格
- `projects/leo-congestion-routing/literature_notes.md` — 文献笔记（L01-L17）
- `projects/leo-congestion-routing/feasibility_report.md` — 可行性报告
- `projects/leo-congestion-routing/decision_log.md` — 决策日志
