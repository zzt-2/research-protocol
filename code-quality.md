# 代码质量经验积累

> 跨 6 个项目（hgat / beam-hopping / isl-scheduling / mega-constellation / ntn-handover / ris-phase）的代码评审结论。
> 新项目写代码前必读。模板文件在 `reference/sim-template/`。

## 各维度最佳来源

| 维度 | 最佳项目 | 关键文件 |
|------|----------|----------|
| GNN 模型架构 | hgat-satellite-dag | `simulator/models_hgat.py`, `models_homo.py` |
| PPO 训练循环 | hgat-satellite-dag | `simulator/ppo.py`, `train.py` |
| DQN 训练循环 | hgat-satellite-dag | `simulator/dqn.py` |
| Sim Config | leo-beam-hopping-gnn | `simulator/config.py` (dataclass) |
| Sim Env | leo-beam-hopping-gnn | `simulator/env.py` (标准 Gymnasium) |
| Channel 模型 | leo-isl-scheduling-drl | `simulator/channel.py` (Gaussian beam) |
| Orbit 模型 | leo-isl-scheduling-drl | `simulator/orbit.py` (Kepler 求解) |
| Traffic 模型 | leo-isl-scheduling-drl | `simulator/traffic.py` (人口加权) |
| Reward 设计 | leo-ntn-handover-drl | `simulator/reward.py` (log-capacity 归一化) |
| 验证套件 | leo-isl-scheduling-drl | `verify/verify_simulator.py` (6 类验证) |
| 模块解耦 | leo-isl-scheduling-drl | 整体架构 (8 模块 + 构造函数注入) |

## 必做清单（写代码前检查）

### Simulator 层
- [ ] Config 用 dataclass + `__post_init__` 计算派生量，不用裸模块常量
- [ ] Env 继承 `gymnasium.Env`，返回标准 5-tuple，info dict 包含 reward 分解
- [ ] 物理模型（channel/orbit/traffic）独立于 env，通过构造函数注入
- [ ] Reward 每个目标归一化到 [0,1]，有 domination threshold 检查
- [ ] 验证套件覆盖 6 类：解析 / 统计 / 退化 / 自相关 / MDP trial / baseline

### ML 层
- [ ] GNN 模型继承 BaseActorCritic 接口（forward / get_action / evaluate_actions）
- [ ] 用 PyG 标准层（GATConv / SAGEConv），不手写稀疏矩阵操作
- [ ] Actor-Critic 共享 GNN backbone，不重复参数

### 训练层
- [ ] PPO：GAE + advantage norm + grad clip(1.0) + LR decay + reward norm(Welford)
- [ ] DQN：soft target update(tau=0.005) + Huber loss + grad clip + epsilon 衰减
- [ ] **必须集成 wandb/tensorboard**（之前 6 个项目全部缺失）
- [ ] **必须有 early stopping**（reward plateau + KL 散度）
- [ ] save/load 包含 optimizer + step_count + normalizer，支持 resume
- [ ] 训练中保存 best model（不只是最终 model）

## 常见缺陷（不要再犯）

| 缺陷 | 出现项目数 | 后果 |
|------|-----------|------|
| 无 wandb/tensorboard | 6/6 | 训练不可观测，崩溃无法及时发现 |
| 无 early stopping | 6/6 | 盲跑到固定 episode 数，浪费算力 |
| 不保存模型权重 | 4/6 | 训练完即丢，无法复用 |
| Actor/Critic 不共享 backbone | beam-hopping | 参数量翻倍，梯度信号不共享 |
| DQN next_state 用 current_state 近似 | isl-scheduling | 破坏 Bellman 更新，Q 值学习失败 |
| 不用 PyG 标准层 | beam-hopping, ntn-handover | 无法利用稀疏计算和图批处理 |
| env 不继承 gymnasium | isl-scheduling, mega, ntn-handover | 无法接入标准 RL 库 |
| config 用裸模块常量 | hgat, isl-scheduling, mega, ntn-handover | 不可序列化、不可 diff |
| grad clip 阈值过大(10.0) | ntn-handover | 等于没 clip |

## 评审打分速查

### GNN 模型（25 分制）

| 项目 | 分数 | 问题 |
|------|------|------|
| hgat-satellite-dag | **24** | 接近完美，仅 hetero_to_homo 缺 None 检查 |
| mega-constellation | 17 | 三个类职责重叠，代码重复 |
| ntn-handover | 16 | 可复用性差，维度硬编码，模型训练混杂 |
| beam-hopping | 13 | 手写 GCN，Actor/Critic 不共享 backbone |

### RL 训练循环（25 分制）

| 项目 | 算法 | 分数 | 问题 |
|------|------|------|------|
| hgat-satellite-dag | PPO | **17** | 无 wandb/early stopping |
| hgat-satellite-dag | DQN | 15 | 无 wandb/early stopping |
| beam-hopping | PPO+MLP | 13 | 不保存 optimizer |
| ntn-handover | B3 PPO | 13 | 不保存模型 |
| ntn-handover | B2 DDQN | 12 | 不保存模型 |
| mega-constellation | GRLR AC | 10 | Vanilla AC 不稳定 |
| isl-scheduling | Wang MADRL | 9 | next_state bug，无 checkpoint |
| hgat-satellite-dag | MVE PPO | 7 | entropy 计算错误，几乎无工程实践 |

### Simulator 公共层（5 分制）

| 项目 | 整体 | config | env | channel | orbit | reward | 验证 |
|------|------|--------|-----|---------|-------|--------|------|
| isl-scheduling | **4.4** | 2 | 3 | **5** | **5** | 4 | **5** |
| ntn-handover | 4.0 | 3 | 4 | 4 | 4 | **5** | 4 |
| beam-hopping | 3.8 | **4** | **5** | 3 | — | 3 | 3 |
| hgat-satellite-dag | 3.4 | 2 | 4 | 4 | 3 | 4 | 4 |
| mega-constellation | 2.6 | 3 | 2 | 2 | 4 | 2 | 2 |

## 物理量语义检查清单

高频混淆项（6 项目踩坑归纳）。config.py 中每个物理量应加注释行：
`# VERIFY: 这是 PSD 还是总功率？参考距离是多少？`

| 物理量 | 易混淆点 | 检查方式 | 踩坑案例 |
|--------|----------|----------|----------|
| 噪声功率 | PSD (dBm/Hz) vs 总功率 (dBm) | 确认是否乘了带宽 | beam-hopping: 误乘带宽致 SINR 虚低 60dB |
| 路径损耗 | FSPL 参考距离 1m vs 1km | 确认公式中 d 的单位 | beam-hopping: slant_range vs ground_range |
| 干扰惩罚 | 惩罚高 SINR 干扰 vs 惩罚干扰存在 | 确认惩罚方向 | beam-hopping: 方向反了 |
| ISL 带宽 | 文献值 vs 实际值 | 标注出处 | routing: 500MHz 无出处 |
| ISL 距离 | 固定值 vs 动态计算 | 确认是否考虑轨道运动 | routing: 用固定值错误 |
| Shannon 容量 | C = B*log2(1+SNR) 中 B 是否已含 | 确认 SNR 定义 | 多个项目混淆 |

## 方法论适配性矩阵

图结构 x 动作空间 x 学习范式可行性评估，避免走到 Step 7 才发现范式不匹配。

| 图结构 | 动作空间 | 推荐学习范式 | 风险范式 |
|--------|----------|-------------|----------|
| 静态小图 (N<50) | 离散 | PPO+GNN, DQN+GNN | -- |
| 静态大图 (N>100) | 离散 | 监督学习+GNN, PPO+GNN | REINFORCE（方差过大） |
| 动态图 | 离散 | PPO+GNN | Vanilla AC |
| Bipartite 子图 | 离散选择 top-K | DDQN+MPNN | Gaussian policy（top-K 不连续） |
| 任意 | 连续 | PPO+Gaussian/Score | -- |

踩坑案例：beam-hopping 用 Gaussian policy + top-K 选择导致 3/5 seeds 崩溃（成功论文全用监督学习）。

## reward balance gate 标准

仿真器验证中 reward 函数必须通过的三项 gate，不通过时禁止进入 baseline 复现阶段：

1. **策略分化**：greedy reward > random reward（至少 1.5x）
2. **分量平衡**：各奖励分量占比 < 80%（domination threshold 从 95% 降至 80%）
3. **信号非恒定**：奖励跨 episode 方差 > 1e-6

根因：domination_threshold=95% 太宽松，实际 80% 以上就足以让学习失败（4/6 项目中招）。
检验方法：verify.py 中 verify_reward_balance 函数。
