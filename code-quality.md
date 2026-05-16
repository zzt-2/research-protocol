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

**[FR-08] 范式对齐检查**：选算法前必须与该领域 top-3 成功论文的学习范式做对齐。偏离范式须在 Step 4a 维度 A 中显式论证：(a) 为什么需要偏离？(b) 偏离后为什么仍可行？无法回答 → 默认跟随成功论文范式。踩坑案例：beam-hopping 用 Gaussian policy 偏离成功论文的无监督范式，3/5 seeds 崩溃。

| 图结构 | 动作空间 | 推荐学习范式 | 风险范式 |
|--------|----------|-------------|----------|
| 静态小图 (N<50) | 离散 | PPO+GNN, DQN+GNN | -- |
| 静态大图 (N>100) | 离散 | 监督学习+GNN, PPO+GNN | REINFORCE（方差过大） |
| 动态图 | 离散 | PPO+GNN | Vanilla AC |
| Bipartite 子图 | 离散选择 top-K | DDQN+MPNN | Gaussian policy（top-K 不连续） |
| 任意 | 连续 | PPO+Gaussian/Score | -- |

踩坑案例：beam-hopping 用 Gaussian policy + top-K 选择导致 3/5 seeds 崩溃（成功论文全用监督学习）。

**[FR-09] GNN encoder 与全局状态 mixer 信息冗余检查**：当 mixing network（QMIX/QPLEX 等）已接收全局状态作为输入时，GNN encoder 的邻居消息传递提供的信息可能完全冗余甚至引入噪声。选 GNN encoder 前 must 验证：(a) mixer 是否有全局状态？(b) 若有，GNN 提供什么增量信息？(c) 邻居状态是否能预测邻居动作（干扰）？无法回答 → GNN encoder 可能无效。踩坑案例：BH QMIX+GNN 在 2 个项目 × 4 种算法 × 2 种规模上全部失败，GNN 始终不如 FC。

**[FR-10] 同时决策 vs 顺序决策的约束传播**：空间隔离类约束（"不照亮邻居"）需要显式执行（顺序选择 + 遮蔽邻居），不能通过 RL 隐式学习。原因是同时决策场景下 agent 看到邻居状态但看不到邻居决策意图，而干扰取决于邻居动作不取决于邻居状态。需显式约束时，优先考虑：(a) 顺序选择 + 遮蔽（IA-Greedy 模式）；(b) 将约束编码到动作空间（mask invalid actions）；(c) 监督学习从最优解学习。踩坑案例：BH 方向 IA-Greedy（顺序选择）比所有 RL 方法（同时决策）高 30-50%，6 种 RL 方法全部 ≤ Random。

### 已验证失败组合

选算法前对照，命中任一组合直接排除：

| 动作空间特征 | 算法 | 失败原因 | 验证项目 | 失败模式 |
|-------------|------|----------|----------|----------|
| 连续分数 + top-K 选择 | PPO (Normal 分布) | top-K 不可微切断梯度 | ISL(D017), BH(D011) | A1 |
| 离散选择 + 图结构信号 | Gaussian policy | 信用分配稀疏，噪声破坏稳定 | BH(D011) | A1, A3 |
| 高维连续 (100+ 维) | A2C | 能力不足，训练不稳定 | RIS(D007, 竞品撤稿) | D1 |
| 空间隔离约束 + 同时决策 | 任意 RL | agent 看不到邻居动作意图，无法避免干扰 | BH(D011,D013,D007) | A3, A5 |
| GNN encoder + 全局状态 mixer | QMIX/QPLEX | 信息冗余，GNN 引入噪声无增益 | BH(D007) | A5 |

## reward balance gate 标准

仿真器验证中 reward 函数必须通过的三项 gate，不通过时禁止进入 baseline 复现阶段：

1. **策略分化**：greedy reward > random reward（至少 1.5x）
2. **分量平衡**：各奖励分量占比 < 80%（domination threshold 从 95% 降至 80%）
3. **信号非恒定**：奖励跨 episode 方差 > 1e-6

根因：domination_threshold=95% 太宽松，实际 80% 以上就足以让学习失败（4/6 项目中招）。
检验方法：verify.py 中 verify_reward_balance 函数。

## 失败模式记录

> 从 6 个项目的 decision_log 提取，按模式类别组织。每条记录对应具体决策 ID 可溯源。
> 新发现的模式追加到对应类别末尾。
> 更新时间: 2026-05-16

### A. RL 训练失败

#### A1. 连续分数 + top-K 动作空间与 PPO 不匹配 [×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | beam-hopping (D011) [致命], isl-scheduling (D017-D021) [严重] |
| 表现 | beam-hopping: 19 维输出仅 5 维有梯度，6 种方法全败归档；isl-scheduling: 小 std KL 爆炸、大 std 策略退化，PPO 无法超越先验 (M1=0.078 vs 0.0774) |
| 根因 | top-K 不可微切断梯度；探索噪声破坏拓扑稳定性 |
| 教训 | 遇到连续分数 + top-K 直接排除 PPO，优先离散动作（keep-drop-swap）或进化策略 |

#### A2. 先验 > RL 学习（梯度信号不足）[×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | isl-scheduling (D021) [严重], mega-constellation (D021) [中等] |
| 表现 | PPO 微调无法超越监督/启发式 baseline；80 轮后 stretch 持平或恶化 |
| 根因 | 路径级 reward vs 逐节点 action 的 credit assignment 困难；greedy reward 太稀疏（99% 路径失败） |
| 教训 | 路径级决策问题优先监督学习 + 启发式推理；设计 RL reward 时确保 action-reward 局部对应 |

#### A3. 方法与问题根本不匹配 [×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | beam-hopping (D011, D013) [致命], leo-beam-hopping (D007) [致命] |
| 表现 | 前一轮：6 种学习方法（PPO+GNN, DiffGNN v1/v2, REINFORCE+softmax, REINFORCE γ=0.7）全败；第二轮：QMIX+GNN 再次失败，GNN(tp=6.58) < FC(tp=7.42) < Random(tp=7.63)，IA-Greedy(tp=10.38) 远超所有方法 |
| 根因 | 干扰是 beam pair 物理关系需直接计算；成功论文全用监督学习非 RL；空间隔离约束需顺序选择+遮蔽（IA-Greedy），同时决策的 RL agent 看不到邻居动作意图；GNN 邻居状态（队列/TTL）不预测邻居决策（是否照亮） |
| 教训 | MVE 训练崩溃必须深究根因（算法稳定性 vs 问题-方法不匹配），不能假设"换个算法就好"；选方法前检查成功论文方法谱系；空间隔离约束类问题优先顺序选择+显式遮蔽或监督学习 |

#### A4. 逐跳贪心推理误差累积 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | mega-constellation (D019) [严重] |
| 表现 | 方向精度 97.6%，但贪心推理路径成功率仅 22-30%（target 1.7%） |
| 根因 | 逐跳精度之积累积（97.6%^10 ≈ 78% 上限） |
| 教训 | 多跳路径问题引入全局推理（加权 Dijkstra），不用逐跳贪心 |

#### A5. GNN encoder 与全局状态 mixer 信息冗余 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | leo-beam-hopping (D007) [致命] |
| 表现 | QMIX+GNN(tp=6.58) < QMIX+FC(tp=7.42) < Random(tp=7.63)；IA-Greedy(tp=10.38) 远超所有 RL 方法；GNN 在 2 层 GCN、独立 DQN、reward shaping 等多种变体中始终不如 FC |
| 根因 | QMIX mixer 已接收全局状态（所有 cell 状态拼接），GNN 的邻居消息传递提供的信息完全冗余；GNN 通过带噪声的队列状态反而引入额外噪声；同时决策场景下邻居状态不预测邻居动作（干扰取决于动作不取决于状态） |
| 教训 | 加 GNN encoder 前必须检查 mixer 是否已有全局状态输入；若有，GNN 的信息增益为零甚至为负；空间隔离约束需显式执行（顺序选择+遮蔽），不能通过 RL+GNN 隐式学习 |

### B. 方向判断失败

#### B1. 假蓝海 / 浅搜误判 [×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | beam-hopping [致命], mega-constellation (D003) [严重] |
| 表现 | beam-hopping 零 GNN 竞争经 2 个项目 × 4 种 RL 算法 × 2 种规模全部验证为"不值得做"；mega Step 3.5 发现 6 篇直接竞争者 |
| 根因 | "零竞争"的空白有结构性原因（空间隔离约束不适合 RL 隐式学习），不是机会 |
| 教训 | MVE 是判断蓝海真伪的最有效工具；"零竞争"可能是问题不适合的信号；多算法失败后应果断 Pivot/Kill 而非继续尝试 |

#### B2. 创新点被推翻需重新定位 [×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | mega-constellation (D003) [严重], ris-phase (D005-D006) [中等] |
| 表现 | mega 从 GNN+RL 转向 size generalization；ris-phase 回退 Step 1 重做定向检索 |
| 教训 | 新颖性验证必须做定向检索（5+ 组聚焦关键词）+ 精读最接近 2-3 篇正面排除 |

#### B3. 小规模场景复杂组件退化 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | ntn-handover (D021, D022) [严重] |
| 表现 | DLA cross-attention 无贡献（FC 已过剩）；GNN 仅 +0.8%（15 UE 时与 MLP 接近） |
| 根因 | 场景规模不足以让复杂模块发挥作用（GNN 优势阈值 N>20-30） |
| 教训 | 创新点验证必须在该创新点预期发挥作用的条件下进行；消融应在大场景做 |

#### B4. AI 幻觉伪造论文功能 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | mega-constellation (D004) [中等] |
| 表现 | Web 搜索声称 GRLR 涉及 size generalization，S2 API 验证后确认为幻觉 |
| 教训 | Web search 对论文的断言必须用 S2 API / DOI 查 abstract 交叉验证 |

### C. 仿真器 / 实现失败

#### C1. 奖励函数分量失衡 [×4 项目，系统性问题]

| 维度 | 内容 |
|------|------|
| 项目 | beam-hopping (D009) [严重], ntn-handover (D005) [中等], hgat (D011) [中等], ris-phase (文献分析) [中等] |
| 表现 | fairness 占 82%（beam-hopping）；吞吐量/阻塞惩罚差 10^5:1（ntn-handover）；E_norm 占 97.9%（hgat） |
| 根因 | 归一化分母/权重设计不当，未做量级估算 |
| 教训 | 训练前量化各分量占比，>80% 即危险；归一化分母取实际值域非论文定义 |
| 注 | 与上方"reward balance gate"规则互补，此处为案例库 |

#### C2. 全规模扩展崩溃 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | isl-scheduling (D022) [中等] |
| 表现 | 1584 节点时边数量 12x 增长，显存逼近 8GB 上限 |
| 教训 | GW 阶段估算全规模资源需求；边二次增长需候选边预筛选；显存预算在 Contract 阶段量化 |

#### C3. 仿真器边界条件 bug [×2 项目]

| 维度 | 内容 |
|------|------|
| 项目 | hgat [严重], mega-constellation (D022) [中等] |
| 表现 | hgat: DAG 入口跳过上传时间 + 不可达路径返回 1 bps + seed 不变；mega: neighbor_map 单向映射 stretch 虚高 |
| 教训 | 不可达路径应 mask 非返回小正数；图结构双向性在所有数据结构中一致维护；seed 需 episode_counter 递增 |

#### C4. 架构级设计遗漏 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | hgat [严重] |
| 表现 | 单 IoTD 设计无法体现多 IoTD 竞争，需 8-10 天重写整个环境 |
| 教训 | 多实体必须为架构一级设计决策；逐条对照竞品论文系统模型，不能只在参数表列出数量 |

#### C5. 规模扩展时 buffer 不足 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | ntn-handover (D027) [中等] |
| 表现 | 50 UE 时 buffer=50K 仅存 1.4 episode，GNN reward 崩溃至 -4,857 |
| 教训 | buffer_size >= min_episodes × (num_agents × steps_per_episode)，规模变化前主动检查 |

### D. 其他模式

#### D1. 竞争论文撤稿揭示算法风险 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | ris-phase (D007) [中等] |
| 教训 | 分析撤稿原因确认自己方案能克服；撤稿≠方向不可行，而是算法选择警告 |

#### D2. PPO 更新过激进导致策略退化 [×1 项目]

| 维度 | 内容 |
|------|------|
| 项目 | isl-scheduling (D017-D018) [严重] |
| 表现 | 100ep M1 从 0.078 降至 0.057；v2 训 15ep 比 v4 训 100ep 更好 |
| 教训 | 先验有效时减少更新次数比调学习率更有效 |

### 模式检索索引

遇到问题时的快速查表：

| 症状 | 可能的模式 | 参考 |
|------|-----------|------|
| PPO 训练完全不收敛 | A1 (top-K), A3 (方法不匹配) | beam-hopping, isl-scheduling |
| RL 无法超越简单先验 | A1, A2 (信号不足) | isl-scheduling, mega-constellation |
| 多算法全部失败 | A3 (问题-方法不匹配), A5 (信息冗余) | beam-hopping (×2 项目) |
| GNN encoder 不如 FC encoder | A5 (mixer 全局状态冗余) | leo-beam-hopping (D007) |
| 空间隔离约束 RL 学不会 | A3, FR-10 (需显式约束) | beam-hopping (IA-Greedy >> RL) |
| 奖励被单一分量主导 | C1 (分量失衡) | 4/6 项目 |
| 小规模有效全规模崩溃 | C2 (规模), C5 (buffer) | isl-scheduling, ntn-handover |
| "零竞争"但感觉不对 | B1 (假蓝海) | beam-hopping |
| 创新点搜到竞争论文 | B2 (创新点被推翻) | mega-constellation, ris-phase |
| 仿真器跑出离谱数值 | C3 (边界 bug) | hgat, mega-constellation |
| GNN 消融几乎无贡献 | B3 (规模不匹配), A2, A5 | ntn-handover, beam-hopping |
