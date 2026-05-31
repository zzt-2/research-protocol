# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 6 完成 → Step 7（仿真器搭建 + Baseline 复现）
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：Step 5 (Baseline选定 D8) + Step 4b (可行性 D9 Go) + Step 6 (仿真器设计 D10)

## 关键上下文

### 本轮决策摘要

**D8 Baseline 选定**: SP + ECMP + MLP (核心) + DTAR (有代码竞品) + GMR 简化版 (最接近竞品)
- 田野调查交叉验证：SP(11/22篇)绝对共识，ECMP非LEO标准但是负载均衡核心对照

**D9 Step 4b Go**: 仿真条件可支撑，资源风险可控(3/5有代码)，失败可回收

**D10 仿真器设计确认**:
- MDP: 集中式 SDN，per-link weight 动作（连续），加权最短路路由
- 训练: 66 节点 (6×11)，泛化: 48/288/720
- 奖励: r_t = -(MLU_t - MLU_{t-1})
- GNN: GAT 2层4头64维 + LN + Residual
- RL: PPO + GAE + wandb + early stopping

### 防坑清单（从 code-quality.md 提取）

**6/6 项目缺失项，必须集成**:
1. wandb/tensorboard 训练日志
2. early stopping (reward plateau + KL 散度)
3. save/load 含 optimizer + step_count + normalizer
4. Config 用 @dataclass + __post_init__
5. Env 继承 gymnasium.Env
6. Actor-Critic 共享 GNN backbone

**其他必做**:
- PyG 标准层 (GATConv)，不手写稀疏矩阵
- grad clip = 1.0 (不是 10.0)
- reward balance gate: 策略分化 >1.5x, 分量 <80%, 非恒定
- MDP 试运行: 随机 vs 贪心，奖励分解，确认无单一项 >95%
- 验证套件 6 类: 解析/统计/退化/自相关/MDP trial/baseline
- 不可达路径 mask 非 return 小正数

### 项目文件索引

| 文件 | 说明 |
|------|------|
| `projects/leo-congestion-routing/master-state.md` | Master 编排状态 (D1-D10) |
| `projects/leo-congestion-routing/decision_log.md` | 决策日志 |
| `projects/leo-congestion-routing/literature_notes.md` | 文献笔记 (10 篇精读) |
| `projects/leo-congestion-routing/feasibility_report.md` | 可行性报告 (A0/A'/A/B/C/D/E) |
| `projects/leo-congestion-routing/simulator-design.md` | 仿真器设计规格 |
| `projects/leo-congestion-routing/mve_env.py` | MVE 环境 (可扩展基础) |
| `projects/leo-congestion-routing/mve_train.py` | MVE 训练 (GNN/MLP 模型) |
| `projects/leo-congestion-routing/mve_66.py` | MVE-2 66节点+故障 |
| `reference/sim-template/` | 代码模板 (config/env/model/train) |
| `code-quality.md` | 踩坑记录和必做清单 |

### Baseline 实现参考

| Baseline | 代码状态 | 实现参考 |
|----------|---------|---------|
| SP (Dijkstra) | 无需代码 | mve_env.py eval_baseline(strategy="sp") |
| ECMP | MVE 已有 | mve_env.py eval_baseline(strategy="ecmp") |
| MLP | MVE 已有 | mve_train.py MLPActorCritic |
| DTAR | GitHub: https://github.com/ChenZ-code/DTAR_Routing | 需适配到本仿真器 |
| GMR 简化版 | 无代码 | 需自实现 MPNN+DDPG, 去PER, K=2 |

### 核心风险
1. **[高] TELGEN 竞品**: 差异化必须聚焦 LEO 时变拓扑
2. **[中] GMR 复现**: P4 级，可退守 DTAR 单一竞品
3. **[中] 仿真三要素**: 非均匀流量+链路故障+突发模式缺一不可

## 下一步

1. **读 `stages/gw-experiment.md` §impl**（仿真器搭建+验证规范）
2. **读 `reference/sim-template/` 模板代码**（config.py, env.py, model_gnn.py, train_ppo.py）
3. **读 `code-quality.md` 必做清单**
4. **搭建仿真器**: 基于 simulator-design.md 和 sim-template，创建 simulator/ 目录
5. **验证仿真器**: 6 类验证 + MDP 试运行 + reward balance gate
6. **复现 Baseline**: 先 SP/ECMP/MLP (MVE 扩展)，再 DTAR (适配代码)，最后 GMR (自实现)
7. **更新 master-state.md 和 literature_notes.md 进度**
