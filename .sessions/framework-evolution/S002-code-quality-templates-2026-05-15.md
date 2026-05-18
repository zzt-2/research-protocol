# [S002] 代码质量模板体系建设

> 日期：2026-05-15
> 触发：用户观察到 projects/ 下 6 个项目有大量相似实现（GNN、DRL、simulator），担心每次重写时质量参差不齐
> 状态：**第一批（修 bug）+ 第二批（新模板）待新对话执行**

---

## 一、背景

6 个研究项目在 `projects/` 下，均涉及卫星通信 + GNN/DRL，每个项目独立实现了 simulator/env/model/train/reward/verify 等模块。代码质量差异显著，且存在系统性缺陷（无一项目集成 wandb、无一项目有 early stopping）。

**目标**：提取最佳实践为共享模板，降低新项目的踩坑概率。

---

## 二、代码质量评审（三维度横向对比）

### 2.1 GNN 模型质量（25 分制）

评审维度：架构清晰度、输入处理、可复用性、代码整洁度、训练集成

| 排名 | 项目 | 分数 | 架构 | 输入 | 复用 | 整洁 | 集成 | 核心优势 | 核心问题 |
|------|------|------|------|------|------|------|------|----------|----------|
| 1 | **hgat-satellite-dag** | **24** | 5 | 4 | 5 | 5 | 5 | BaseActorCritic 抽象 + 模板方法 | hetero_to_homo 缺 None 检查 |
| 2 | mega-constellation | 17 | 4 | 3 | 3 | 3 | 4 | OrbitalPE 领域位置编码 | 三个类职责重叠，代码重复 |
| 3 | ntn-handover | 16 | 4 | 4 | 2 | 2 | 4 | mask 机制贯穿最佳 | 可复用性差，维度硬编码 |
| 4 | beam-hopping | 13 | 2 | 3 | 2 | 3 | 3 | 邻接矩阵归一化正确 | Actor/Critic 不共享 backbone |

**最佳实践清单（GNN）**：
1. `BaseActorCritic` 抽象接口：统一 `forward` / `get_action` / `evaluate_actions`（来源：hgat）
2. `_encode` + `_encode_batch` 双路径，避免逐样本循环（来源：hgat models_homo.py）
3. `_ensure_all_edge_types` 空边填充，HeteroConv 防御（来源：hgat models_hgat.py）
4. `OrbitalPE` 物理结构 sin/cos 编码注入节点 embedding（来源：mega-constellation）
5. `edge_dim` 边特征注入注意力计算（来源：mega-constellation）
6. mask 从图构建贯穿到 Q 值输出 `masked_fill`（来源：ntn-handover）
7. Dueling DQN 的 V/A 分解 `Q = V + A - mean(A)`（来源：ntn-handover）
8. LayerNorm 残差连接稳定多步 GNN 迭代（来源：ntn-handover）
9. `register_buffer` 管理静态图结构（来源：beam-hopping）
10. 差分学习率（GNN encoder vs RL head）（来源：ntn-handover）
11. 模板方法模式切换 GNN 变体 `_conv_cls` 类变量（来源：hgat）
12. config 集中管理 + 构造函数默认值回退（来源：hgat）

### 2.2 RL 训练循环质量（25 分制）

评审维度：训练稳定性、日志监控、Checkpoint 管理、Early Stopping、代码结构

| 排名 | 项目 | 算法 | 总分 | 稳定 | 日志 | Checkpoint | ES | 结构 |
|------|------|------|------|------|------|-----------|-----|------|
| 1 | **hgat-satellite-dag** | PPO | **17** | 5 | 2 | 4 | 1 | 5 |
| 2 | **hgat-satellite-dag** | DQN | 15 | 4 | 2 | 4 | 1 | 4 |
| 3 | beam-hopping | PPO+MLP | 13 | 4 | 2 | 3 | 1 | 3 |
| 3 | ntn-handover | B3 PPO | 13 | 4 | 3 | 1 | 1 | 4 |
| 5 | beam-hopping | PPO+GNN | 12 | 4 | 2 | 2 | 1 | 3 |
| 5 | mega-constellation | Pretrain | 12 | 3 | 3 | 2 | 1 | 3 |
| 5 | ntn-handover | B2 DDQN | 12 | 3 | 3 | 1 | 1 | 4 |
| 8 | ntn-handover | LA-DDQN | 11 | 3 | 3 | 1 | 1 | 3 |
| 9 | mega-constellation | GRLR AC | 10 | 2 | 2 | 3 | 1 | 2 |
| 10 | isl-scheduling | Wang MADRL | 9 | 2 | 2 | 1 | 1 | 3 |
| 11 | hgat-satellite-dag | MVE PPO | 7 | 2 | 1 | 1 | 1 | 2 |

**最佳实践清单（训练）**：
1. Reward normalization（Welford 在线算法），clip [-5,5]（来源：hgat train.py RewardNormalizer）
2. Advantage normalization `(adv - mean) / (std + eps)`（所有 PPO 项目）
3. Linear LR decay 随 total_updates 衰减（来源：hgat PPO `_decay_lr()`）
4. Soft target update (Polyak averaging, tau=0.005)（来源：hgat DQN）
5. Huber loss (smooth_l1) 替代 MSE（来源：hgat DQN、ntn B2）
6. Gradient clipping max_grad_norm=1.0（来源：hgat）
7. Obs normalization（RunningNormalizer + state_dict 可序列化）（来源：beam-hopping）
8. GAE(lambda=0.95)（所有 PPO 项目）
9. log_prob clamp(min=-20.0) 防 NaN（来源：ntn B3 PPO）
10. Abstract base class 统一接口（来源：hgat BaseActorCritic）
11. save/load 含 optimizer state_dict，支持 resume（来源：hgat）
12. Attention 可视化调试 debug_attention（来源：ntn LA-DDQN）

**常见缺陷清单（训练）**：
1. **全部项目无 wandb/tensorboard** — 6/6 缺失，训练不可观测
2. **全部项目无 early stopping** — 6/6 缺失，盲跑固定 episode 数
3. **大多数不保存模型权重** — ntn 群(B2/B3/LA)、isl Wang MADRL 训练完即丢
4. **大多数不支持 resume** — 仅 hgat 保存了 optimizer + step count
5. **gradient clipping 阈值不统一** — 0.5 到 10.0 差 20 倍，10.0 等于没 clip
6. **缺 LR scheduling** — 仅 hgat PPO 有 linear decay
7. **MVE 代码混入正式** — hgat mve/train.py entropy 近似错误 `-mean(log_prob)`
8. **Wang MADRL next_state bug** — isl-scheduling `_train_step` 第 420 行用 current_state 替代 next_state，破坏 Bellman 更新
9. **无 seed 管理** — beam-hopping `seed=global_ep * 7` 固定公式
10. **batch 化不足** — hgat DQN 逐样本 encode、LA-DDQN 逐 UE 串行、GRLR 每步 update

### 2.3 Simulator 公共层质量（5 分制）

| 排名 | 项目 | 整体 | config | env | channel | orbit | traffic | reward | 验证 | 解耦 |
|------|------|------|--------|-----|---------|-------|---------|--------|------|------|
| 1 | **isl-scheduling** | **4.4** | 2 | 3 | **5** | **5** | **5** | 4 | **5** | **5** |
| 2 | ntn-handover | 4.0 | 3 | 4 | 4 | 4 | — | **5** | 4 | 4 |
| 3 | beam-hopping | 3.8 | **4** | **5** | 3 | — | 4 | 3 | 3 | 4 |
| 4 | hgat-satellite-dag | 3.4 | 2 | 4 | 4 | 3 | — | 4 | 4 | 3 |
| 5 | mega-constellation | 2.6 | 3 | 2 | 2 | 4 | 2 | 2 | 2 | 3 |

**各组件最佳实践**：

| 组件 | 最佳 | 关键文件 | 核心模式 |
|------|------|----------|----------|
| config | BH | `simulator/config.py` | dataclass + `__post_init__` 派生量 + 文献溯源注释 |
| env | BH | `simulator/env.py` | 继承 gymnasium.Env，5-tuple，super().reset(seed=)，rich info dict |
| channel | ISL | `simulator/channel.py` | Gaussian beam + Rayleigh pointing jitter + outage probability 解析 |
| orbit | ISL | `simulator/orbit.py` | Kepler 方程 Newton 求解 + 完整 Keplerian-to-ECI 旋转矩阵 |
| traffic | ISL | `simulator/traffic.py` | GHS-POP 人口加权 + 重力模型 + visibility 映射 |
| reward | HO | `simulator/reward.py` | log-capacity 归一化 + domination threshold + decompose_reward |
| 验证 | ISL | `verify/verify_simulator.py` | 6 类验证：解析/统计/退化/自相关/MDP trial/baseline 对比 |
| 解耦 | ISL | 整体架构 | 8 独立模块 + 构造函数注入 + `__init__.py` 接口管理 |

---

## 三、已创建的交付物

### 3.1 代码质量经验文档

**文件**：`code-quality.md`（90 行）
**内容**：各维度最佳来源表、必做清单（Simulator/ML/训练层）、常见缺陷表（出现项目数+后果）、评分速查表

### 3.2 代码模板（7 个文件，reference/sim-template/）

| 文件 | 行数 | 来源项目 | 核心模式 |
|------|------|----------|----------|
| config.py | 65 | BH | dataclass + 派生量 + 范围校验 |
| env.py | 130 | BH | 标准 Gymnasium 5-tuple + action masking + rich info |
| reward.py | 117 | HO | log-capacity 归一化 + domination threshold + 分解 |
| model_gnn.py | 169 | HGAT | BaseActorCritic 抽象 + GATConv 编码器 |
| train_ppo.py | 495 | HGAT | PPO 全套 + wandb + early stopping + checkpoint |
| train_dqn.py | 271 | HGAT | DQN + soft target + Huber + wandb + checkpoint |
| verify.py | 254 | ISL | 6 类验证套件骨架 |

### 3.3 CLAUDE.md 更新

- 目录结构新增 `reference/sim-template/` 和 `code-quality.md`
- 文档职责边界表新增「代码质量」和「代码模板」两行
- 文件路径规则表新增代码质量经验和代码模板条目
- 新增「代码质量强制规范」章节：[MUST] 写代码前必读 code-quality.md 和模板

---

## 四、模板质量复查（三个独立视角）

### 4.1 Code Reviewer 发现（28 个问题）

**CRITICAL（5 个，必须修）**：

| # | 文件 | 问题 | 影响 |
|---|------|------|------|
| 1 | model_gnn.py:93 vs train_ppo.py:435 | `get_action` 返回 3 元组，train_ppo.py 解构为 4 | ValueError |
| 2 | model_gnn.py 无 forward_batch vs train_dqn.py:182,187 | `forward_batch` 方法不存在 | AttributeError |
| 3 | env.py:36-38 vs model_gnn.py:84-93 | env action_space 连续 Box，model 输出离散 int | 组合崩溃 |
| 4 | train_ppo.py:446-460 | RolloutBuffer 每个 episode 重建，update_interval > 1 时只更新最后 1 个 | 逻辑 bug |
| 5 | verify.py 5 个空函数 | 打印 [TEMPLATE] 不输出 FAIL，用户误以为验证通过 | 虚假安全感 |

**HIGH（8 个，应该修）**：

| # | 文件 | 问题 |
|---|------|------|
| 1 | env.py:78 | reward 硬编码为 0.0，用户跑通但 reward 始终为零 |
| 2 | env.py:76-77 | RewardCalculator 引用被注释掉，未实际 import 和使用 |
| 3 | reward.py:39 | `_log_capacity_norm` 是死代码，compute_reward 未调用 |
| 4 | train_dqn.py:127 | `_get_init_kwargs` 用反射克隆 target_net，脆弱不可靠 |
| 5 | config.py | 缺 device/seed/total_training_steps 等训练基础设施参数 |
| 6 | train_dqn.py | 无 train() 主循环骨架，只有 DQNAgent 类 |
| 7 | train_dqn.py | 无 early stopping 骨架（train_ppo.py 有但 DQN 没有） |
| 8 | verify.py | 缺 verify_reward 类别（奖励是最容易出错的部分） |

**接口不一致汇总**：

| 文件 A | 文件 B | 不一致 |
|--------|--------|--------|
| model_gnn.py:93 | train_ppo.py:435 | get_action 3 元组 vs 解构 4 元素 |
| model_gnn.py | train_dqn.py:182 | forward_batch 不存在 |
| config.py:32-34 | reward.py:25-27 | 权重命名 reward_alpha vs w_throughput |
| env.py:36-38 | model_gnn.py:84-93 | action_space Box(连续) vs Discrete(离散) |
| train_ppo RewardNormalizer | train_dqn:136-159 | Welford 实现公式不同 |
| config.py:35 | reward.py:28 | sinr_max_db 无传递路径 |

### 4.2 Analyst 踩坑分析（从 6 个 decision_log 归纳）

**反复出现的 3 大杀手**：

**杀手 1：奖励函数尺度失衡（4/6 项目中招）**
- handover：吞吐量 ~10^6 vs 阻塞惩罚 10，DRL 退化为贪心（D005）
- beam-hopping：fairness 占 82% 奖励不可学，interference 仅 7%（D011）
- HGAT：E_norm 占 97.9%，η_t 需从 0.5 调至 5.0（D011）
- ISL：权重需要 sweep 验证才能找到平衡
- **根因**：domination_threshold=95% 太宽松，实际 80% 以上就足以让学习失败
- **预防**：MDP 试运行必须包含 reward balance gate（greedy > random + 各分量占比 < 80% + 信号非恒定）

**杀手 2：物理量语义混淆（3/6 项目中招）**
- beam-hopping：噪声功率误乘带宽致 SINR 虚低 60dB（D008）
- beam-hopping：路径损耗误用 slant_range 多算 14dB（D008）
- beam-hopping：干扰惩罚方向反了（D008）
- routing：ISL 带宽 500MHz 无出处需修正为 1GHz（D015）
- routing：ISL 距离用固定值错误（D016）
- **根因**：config 有范围校验但不检查语义（dB vs dBm、PSD vs 总功率）
- **预防**：新增物理量语义检查清单，config 中每个物理量标注含义

**杀手 3：方法论选择偏离成功论文（2/6 项目中招）**
- beam-hopping：走到 Step 7 Part B 才发现 GNN+RL（Gaussian policy）根本不行，成功论文全用无监督（D011/D012）
- handover：方案 A DLA 消融全面否定（D021），好在有方案 C 兜底
- **根因**：框架在 Step 4a/4b 审查方向可行性但不审查"学习方法是否与问题结构匹配"
- **预防**：Step 6 新增方法论适配性检查，对比 top-3 成功论文的学习范式

**其他反复出现的问题**：
- 维度/形状不匹配 bug（HGAT 多 IoTD action space 不匹配、routing neighbor_map 单向注册）
- Baseline 复现结果与预期不符（ISL B2 未优于 B1、handover B2 50 UE CUDA 崩溃）
- 训练不稳定/不收敛（beam-hopping MVE 3/5 seeds 崩溃、routing greedy 成功率 1.7%）
- 参数缺失需假设/溯源不足（HGAT η_t/η_e/λ 论文未披露、RIS 大量 NOT_FOUND）

### 4.3 Architect 缺口分析（从研究全流程视角）

**核心判断**：当前 7 个模板是"组件级骨架"，缺少"流程级骨架"。框架定义了"做什么"，模板提供了"用什么积木"，缺少"怎么搭"。

**缺失的 5 个模板（按优先级）**：

| 优先级 | 文件 | 行数 | 覆盖环节 | 解决什么 |
|--------|------|------|----------|----------|
| P0 | `run.py` | ~150 | GW Step 7B, Execute 1-4 | 统一 CLI 入口 + 模型注册表 + 多 baseline × 多种子调度 + 结果汇总 |
| P0 | `baselines/base.py` | ~120 | GW Step 7B, Execute 4 | Baseline 抽象基类 + 统一执行 + 趋势验证 + 内置 Random/Greedy |
| P1 | `experiment.py` | ~100 | Execute 2-5 | 配置快照 + git hash + 指标记录 + 结构化 JSON 输出 |
| P1 | `evaluate.py` | ~200 | Execute 4, 6 | 训练后评估 + Contract 指标计算 + 统计检验 + 标准图表 |
| P2 | `ablation.py` | ~100 | Execute 4 | 消融变体声明式定义 + 共享训练协议 + 自动与主实验对比 |

**编排层缺失的根因**：
- hgat `train.py:48-61` 的 `_make_model()` 是每个项目自建的模型注册表
- hgat `train.py:136-164` 的 `evaluate_baseline()` 是每个项目自建的评估框架
- beam-hopping `baselines/evaluate.py:12-127` 和 ntn `baselines/b1_traditional.py:82-173` 实现了相同模式但互不兼容
- leo-mega `ablation.py`（305 行）是完全定制的消融实验，核心模式可模板化

**从模板到 Contract/Execute 的 5 个障碍**：
1. Part B baseline 复现无代码指导（baselines/ 目录结构从何而来？）
2. Contract 冻结后 config 参数无双向链接（config 应有 `to_contract_table()` 方法）
3. 消融实验的维度管理无指导（如"去掉 PE 用零向量而非删除维度"的细节）
4. 训练结果 → experiment_result 模板的产出断层
5. 多 baseline 并行训练的工程问题（串行循环跑 models × seeds）

---

## 五、待执行行动（两批）

### 第一批：修现有模板 bug + 最痛缺口

**P0 — 修复 4 个 CRITICAL 接口 bug**：

1. **统一 get_action 返回值**：
   - model_gnn.py `get_action` 返回 3 元组 `(action, log_prob, value)`
   - train_ppo.py 第 435 行改为解构 3 元素
   - 或 model 端也返回 4 元素（加 entropy）

2. **统一 action_space 离散/连续语义**：
   - env.py 改为 `spaces.Discrete(N)`（与 model 匹配）
   - 或 env.py 保留 Box 但加注释说明"连续空间需配连续策略头"
   - **建议**：同时提供 Discrete 和 Box 两种占位符，用注释标注选择依据

3. **补充 forward_batch 或标注 DQN 所需接口**：
   - 在 model_gnn.py 的 BaseActorCritic 中增加 `forward_batch` 方法
   - 或在 train_dqn.py 中明确注释"DQN 需要 model 实现 forward_batch(obs_list)"

4. **修复 RolloutBuffer 跨 episode 累积逻辑**：
   - train_ppo.py 的 `buf = RolloutBuffer()` 应在 episode 循环前创建一次
   - 每个 episode 追加到同一个 buffer，update 后清空

**P0 — 增强 verify.py**：

5. **新增 `verify_reward_balance` 函数**：
   - 用 greedy/random/constant 三种策略各跑 N episode
   - 检查：(a) greedy reward > random reward（策略分化）；(b) 各奖励分量占比 < 80%；(c) 奖励跨 episode 方差 > 阈值
   - 不通过时输出 FAIL 并建议修正

6. **verify.py 空函数改为显式 FAIL**：
   - 5 个 `[TEMPLATE]` 打印改为 `check("模板未实现", False, ...)`
   - 让用户一眼看到哪些验证还没定制

**P1 — 新增两个核心模板**：

7. **新增 `run.py`（实验入口/编排模板）**：
   - argparse CLI：`--model {name}`、`--seeds 42 123`、`--episodes N`、`--config {name}`、`--device cuda`
   - model registry（dict 映射名字到类）
   - baseline registry
   - 多模型 × 多种子循环调度
   - 结果汇总到标准 JSON

8. **新增 `baselines/base.py`（Baseline 评估框架）**：
   - `Baseline` 抽象基类：`run_episode(env, seed) -> dict` 接口
   - `BaselineSuite`：注册多个 baseline → 统一跑 N episode × M seed → mean/std → 趋势验证 → JSON/表格
   - 内置 `RandomBaseline` 和 `GreedyBaseline`

### 第二批：经验积累 + 防坑

9. **新增 `experiment.py`（实验记录器）**：
   - `ExperimentRecorder`：`start(config, model_name, seed)` → `log_metrics(dict)` → `finish()` → 生成 JSON
   - 包含：完整配置快照、git hash、timestamp、指标、训练曲线

10. **新增 `evaluate.py`（训练后评估）**：
    - `Evaluator`：加载模型 → eval env 跑 N episode → Contract 指标计算 → 配对 t 检验 → 标准图表
    - 输出与 `templates.md` 的 `experiment_result` 模板对齐

11. **更新 `code-quality.md` 加入踩坑清单**：
    - 物理量语义检查清单（dB vs dBm、PSD vs 总功率、参考距离等高频混淆项）
    - 方法论适配性矩阵（图结构 × 动作空间 × 学习范式的可行性评估）
    - reward balance gate 标准
    - config 每个 [ASSUMPTION] 标记和消解决策追踪

12. **更新 `verify.py` 新增 `verify_shape_propagation`**：
    - 构造最小 batch obs → model.forward() → 逐层 shape 检查 → 与 config 预期维度对比
    - edge_index 双向完整性检查

---

## 六、已创建文件清单

| 文件 | 行数 | 状态 |
|------|------|------|
| `code-quality.md` | 90 | 已完成 |
| `reference/sim-template/config.py` | 65 | 待修（缺 device/seed/total_training_steps） |
| `reference/sim-template/env.py` | 130 | 待修（action_space 语义 + reward 占位符 + RewardCalculator 集成） |
| `reference/sim-template/reward.py` | 117 | 待修（_log_capacity_norm 死代码 + throughput 可超 1.0 + 缺 state_dict） |
| `reference/sim-template/model_gnn.py` | 169 | 待修（get_action 返回值 + forward_batch + hidden_dim 整除校验） |
| `reference/sim-template/train_ppo.py` | 495 | 待修（get_action 解构 + RolloutBuffer 累积逻辑 + wandb step 统一） |
| `reference/sim-template/train_dqn.py` | 271 | 待修（forward_batch 引用 + 反射克隆 + Welford 统一 + 加 train() 骨架） |
| `reference/sim-template/verify.py` | 254 | 待修（空函数改 FAIL + 加 verify_reward_balance + 加 verify_shape_propagation） |
| `reference/sim-template/run.py` | ~150 | 待新建 |
| `reference/sim-template/baselines/base.py` | ~120 | 待新建 |
| `reference/sim-template/experiment.py` | ~100 | 待新建 |
| `reference/sim-template/evaluate.py` | ~200 | 待新建 |
| CLAUDE.md | — | 已更新（目录结构+职责表+路径规则+强制规范章节） |

---

## 七、新对话提示词模板

```
继续代码质量模板体系建设。

日志：.sessions/framework-evolution/S002-code-quality-templates-2026-05-15.md

当前状态：7 个模板文件已创建但有 4 个 CRITICAL 接口 bug 需修复，另有 4 个新模板待创建。

任务：
1. 读取 S002 第五节，按优先级执行修复和新建
2. 第一批：修 4 个 CRITICAL bug + 增强 verify.py + 新增 run.py + baselines/base.py
3. 第二批：新增 experiment.py + evaluate.py + 更新 code-quality.md 踩坑清单
4. 每修完一个文件，用 `ast.parse` 验证语法，用 import 测试接口一致性
5. 全部完成后更新 S002 状态为"已完成"
```
