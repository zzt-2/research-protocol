# Execute（执行）

> 按 Contract 执行实验，产出完整实验结果集。
> 通信领域研究：额外阅读 `domain-comms.md` 中的指标体系、可视化范式和反模式清单。
> 反模式审查已在 Contract Step 5 完成。Execute 阶段只做实现级验证（代码是否忠实实现了设计）。

---

## 目标

按 Contract 执行实验，产出完整实验结果集。

## 输入

Contract（frozen）+ data-flow.md + Groundwork 产出

## 输出

`results/*.md` + `decision_log.md`（追加）

## 人介入点

- 假设判定为 FAIL 或 MARGINAL 时 → 通知用户，等待决策
- 补充实验范围变更 → 需用户确认
- 仿真环境缺陷需要修复重跑 → 需用户确认
- Contract Amendment（参数修正）→ 需用户确认

## Contract Amendment

Execute 阶段发现 Contract 参数事实性错误时，按 `stages/contract.md` "Contract 的效力"中的 Amendment 流程处理：

- 可修正：Simulation Config 中的参数值
- 不可修正：hypothesis / success_signal / failure_signal / fairness_rules
- 修正必须记录到 decision_log + contract.md amendment 注解 + 用户确认

---

## Step 0：Contract 审计 + 仿真器开发

### Step 0-前提：实验完备性审计

> 目的：在开始代码实现前，确认 Contract 的声称-证据映射和实验完备性自检清单已就绪。
> 此检查点防止"实验计划不完整就开始编码"导致 Execute 阶段返工。

[MUST] 逐项确认：

1. **声称-证据映射已建立**：Contract Step 2 的 Hermes 三列表是否已填写完整？每个 claimed contribution 是否有对应实验行？
2. **experiment_completeness_checklist.md Tier 1 全 pass**：Contract Step 5 的对标检查是否已完成？如有 fail 项，是否已修正？
3. **通信特有维度已覆盖**（如适用）：信道模型溯源、拓扑多样性、复杂度报告是否已纳入实验计划？

**检查结果**：

- 全部通过 → 继续 Step 0 仿真器开发
- 有未通过项 → **退回 Contract** 修正，不进入实现阶段
- 修正后重新审计通过方可继续

---

### Step 0-仿真器开发（逐模块验证）

按 `data-flow.md` 的模块划分逐步实现。每个模块写完后立即验证，不攒到一起。

### 逐模块验证节奏

```
模块 A 实现 → 跑 assertion（10 行以内）→ 确认通过 → 模块 B 实现 → ...
```

每个模块的 assertion 检查该模块的核心不变量：

| 模块            | 典型 assertion                                               |
| --------------- | ------------------------------------------------------------ |
| 星座/网络配置   | 节点数正确、坐标范围合理、轨道周期正确                       |
| 拓扑连接        | 度数分布符合预期、ISL 距离范围合理、断链率与 Step 3 验算一致 |
| 信道/链路       | 容量/时延范围合理、跨配置单调性正确                          |
| 流量生成        | 流量矩阵形状正确、OD 对数量匹配                              |
| 路由            | Dijkstra 路径存在性、时延范围合理                            |
| RL 环境         | 状态空间维度与 data-flow.md 一致、动作空间合法、奖励非零     |
| 模型            | 输入维度匹配、输出维度匹配、参数量合理                       |
| 集成 smoke test | 端到端一次 forward pass + 一次 Dijkstra baseline + 指标计算  |

[MUST] 每个模块的 assertion 结果记录到 decision_log（一行即可，如 `[AUTO] constellation.py assertion 通过：66/100/200/720 卫星坐标范围 [6771, 7121] km`）。

### 实现级反模式验证

代码实现完成后，对照 Contract Step 5 的反模式排查结果，验证代码是否忠实实现：

- 消融实验的零向量替代是否正确实现
- 共享数据集（拓扑快照 + 流量矩阵）是否在所有实验间复用
- 超参搜索预算是否一致

---

## Step 0.5：先验策略基线测试

写 RL 代码之前，先测 trivial policy（最近邻/随机+简单规则）的表现。

### 测试方法

在仿真器 smoke test 通过后、写 RL 模型之前：

1. 实现最简单的启发式策略（贪心/最近邻/随机+简单规则）
2. 跑 3-5 episodes 记录核心指标
3. 计算 trivial policy 与 Contract success_signal 的比率

### 风险判定

| trivial policy 达标率 | 判定   | 动作                                                            |
| --------------------- | ------ | --------------------------------------------------------------- |
| < 30%                 | 正常   | 继续写 RL 代码                                                  |
| 30% - 70%             | 需关注 | 检查 trivial policy 是否恰好命中了问题结构，评估 RL 增量空间    |
| ≥ 70%                 | 高风险 | RL 大概率无法显著超越先验，需重新评估 RL 价值主张或调整叙事方向 |

先例：ISL active_bias 达 B1 的 75%（PPO 仅 +0.6%）；Routing 贪心推理 97.6% 方向精度；Handover top-K 压缩做主功。

[MUST] 基线测试结果记录到 decision_log。

---

## Step 1：Quick Test + MVE 对比

仿真器集成 smoke test 通过后，跑小规模 Quick Test 验证核心假设方向。

### Quick Test

- 小规模训练 + 小规模推理，判断核心方法是否"有信号"
- 如果 Quick Test 完全失败（如 loss 不收敛、精度随机），回到 Contract 检查 data-flow.md 是否有遗漏

### MVE 对比

[MUST] 如果 Groundwork 阶段做过 MVE（`feasibility_report.md` §D），Quick Test 完成后必须与 MVE 结果对比。

- 差异 <10pp：正常，记录即继续
- 差异 ≥10pp：**必须**写一段差异分析（可能原因：监督 vs RL？特征设计不同？评估口径不同？）再继续
- 差异分析记录到 decision_log

### [FR-18] 环境保真度竞争格局检查

如果仿真环境已从 MVE 简化版升级到正式版（拓扑真实化、流量模型复杂化等），[MUST] 在 MVE 对比时额外检查：

1. MVE 中各方法的相对排名是否在正式环境中保持？
2. 如果 baseline 在正式环境中变强了 → 分析原因（如简化环境人为限制了 baseline 的发挥）
3. 如果主方法优势来源是简化环境的结构性偏差 → 必须在 decision_log 中记录，并重新评估贡献叙事

> 先例：leo-congestion-routing Ch3 拓扑从 4-regular 抽象网格升级为 Walker-Delta 物理仿真后，ECMP 因极地间隙减少路由选择空间反而变强（GNN/ECMP MLU 从 0.78 变为 0.96）。MVE 阶段没有分析简化拓扑对 baseline 竞争力的影响。

### 信号方向熔断

[MUST] 如果首次完整执行 run 的结果与 MVE 或 GW 预测方向相反（如 MVE 显示新方法 > baseline，但 Execute 显示 baseline > 新方法），必须停止并做组件级信息流追踪：

1. 暂停后续实验
2. 对每个 proposed 架构组件，做 FR-16 信息增量审计（两个不同输入 → 是否产生不同输出）
3. 如果发现组件信息增量为零 → 根因已定位，回到 Contract 调整架构设计
4. 如果信息增量非零但 RL 仍学不好 → 转入 Step 4.5 死胡同检测

> 先例：nfv-sfc-vne 的 E1 seed=0 显示 MatchingGAT R2C=0.790 < DualGAT+ R2C=0.801，与 GW 训练指标方向相反。根因是 cross-attention 的 uniform modulation 信息增量为零。如果当时有信号方向熔断，会在 D022 就定位根因而非继续跑完 E1。

---

## Step 2：核心实验

仿真分级执行：**smoke → quick → full**，每级通过后才进下一级。

- **smoke**：验证逻辑正确性。失败只改代码不改设计
- **quick**：小规模数据判断方向
- **full**：完整数据出发表级结果

各级时间预算由研究者根据仿真复杂度自定，不设硬性上限。卫星系统级仿真单次可达小时级，时间限制不现实。

### 实验执行纪律

[MUST] 每次跑实验前遵守以下三条：

1. **报时间预估**：跑之前先算 `单步耗时 × 步数 × episode 数 = 预计 X 分钟`。单步耗时用已测过的数据（如上一次对话的 env.step 计时）。如果预估 >30 分钟，告知用户并建议用 `run_in_background`。

2. **先跑 1-2 episode 烟雾测试**：确认代码能跑通（无 import 错误、维度不匹配、OOM）再跑完整实验。不要写完全部代码后一次性跑完整实验——bug 修起来浪费时间翻倍。

3. **后台长任务用 `run_in_background`**：预估 >5 分钟的实验用 Bash 的 `run_in_background` 参数，不要用 `timeout=600000` 前台阻塞。后台任务用 TaskOutput 读取结果。

### 随机种子要求

| 仿真类型                                       | 最低种子数 | 理由                 |
| ---------------------------------------------- | ---------- | -------------------- |
| 确定性仿真 + 可控随机噪声                      | ≥3 组      | 主随机源只有噪声种子 |
| 含多随机成分（流量模型、用户分布、信道随机化） | ≥5 组      | 随机源多需要更多样本 |

### 结果记录

结果记录到 `results/{实验名}.md`（模板见 `templates.md`）。

---

## Step 3：假设判定

对照 Contract 判定：

| 判定     | 条件                | 动作                                 |
| -------- | ------------------- | ------------------------------------ |
| PASS     | 达到 success_signal | 继续补充实验                         |
| MARGINAL | 方向对但幅度不够    | 分析原因，决定是否继续               |
| FAIL     | 未达 success_signal | 诊断：实现问题 → 指标问题 → 方法问题 |

**简单方法优于 DL**：这不是 FAIL，但 [MUST] 调整叙事。可选叙事方向：

- "可行性验证"：ISL 信道可预测性验证
- "条件边界分析"：什么条件下 DL 有优势
- "对比基准"：系统对比 DL vs 传统方法

[MUST] FAIL 或 MARGINAL 判定时通知用户，等待决策。

---

## Step 4：补充实验（PASS 后执行）

- **对比实验**：核心方法 vs 全部 baseline（必要）
- **消融实验**：按 Contract 中的 ablation_plan（必要）
- **鲁棒性验证**：参数敏感性、场景泛化（按需）
- **可视化论证**：消融实验除定量结果外，[SHOULD] 准备可解释性图表（SHAP 特征重要性、Grad-CAM 热力图、案例分析图等），路径记录在 experiment_result 的"可视化"字段
- **[FR-19] 指标模型假设敏感性测试**：如果评估指标依赖模型假设（如排队模型、传播模型），必须做至少一组替代假设的对比，证明结论稳健或声明条件范围（定义见 `contract.md` Step 2 FR-19）
- **达标即停**：核心 + 对比 + 消融完成 → 停止

[MUST] 补充实验范围变更需用户确认。

---

## Step 4.5：防死胡同检测（穿插于 Step 1-3）

### 触发条件

连续 3 次迭代（调参/修复/bias 注入等）后，核心指标改善 <5%，即触发。

核心指标定义：Contract 中 success_signal 对应的指标（如 M1 吞吐量、reward、准确率等）。

### 触发后必须做的事

1. **暂停当前实验**，不再继续调参
2. **写 decision_log 分析**，包含：
   - 已尝试的方案列表和每次的核心指标值
   - 根因判断（RL 信号太弱 / 问题建模错误 / 仿真器缺陷 / 其他）
   - 跨项目类似失败检索（读 `projects-overview.md` 的"跨项目教训"段 + 其他项目的 decision_log）
   - 当前最佳结果与 Contract 目标的差距
3. **写 PROMPT 文件**到 `.sessions/`，交接给新对话做深度调研：
   - 文献调研：竞品论文的 RL 设计（action space / reward / 训练策略）具体是怎么做的
   - 跨项目失败模式匹配：哪些项目遇到过类似问题，怎么解决的
   - 替代方案提出：至少 2 个不同的解决方向（不是调参，是换思路）
4. **通知用户**，说明当前状况和交接安排

### 不做的事

- 不在当前对话继续调参（上下文已被失败尝试污染）
- 不自行宣布"方法不可行"（交给新对话调研后判断）
- 不跳过 decision_log 直接开新对话（新对话需要分析记录作为输入）

### 典型死胡同模式

| 模式                | 表现                                                            | 先例                                        |
| ------------------- | --------------------------------------------------------------- | ------------------------------------------- |
| RL 梯度信号太弱     | 手写先验 > RL 学习，PPO 更新反而损害策略                        | ISL scheduling, beam-hopping                |
| 探索破坏稳定解      | 大噪声导致每步都改变决策，无法建立稳定策略                      | ISL scheduling v1                           |
| 规模扩展失败        | 小规模有效但全规模崩溃（维度/内存/速度）                        | ISL scheduling 全规模 import 错误           |
| KL 约束与学习的矛盾 | KL 限制太严学不动，太松策略崩溃                                 | ISL scheduling v2-v4                        |
| 机制信息归零        | proposed mechanism 对所有决策选项产生相同信号，学习依赖残余路径 | nfv-sfc-vne (uniform cross-attn modulation) |

[MUST] 每个实验完成后回答 4 问：

1. 结果与 Contract 的 success/failure signal 是否一致？
2. 本实验与之前实验的结果有无矛盾？
3. 如现在必须停下，结果是否足够清晰可复现？
4. 实验设计是否存在信息泄露？

每完成 3 个实验，额外检查：当前方法是否偏离 Contract 定义（方法论漂移检测）。

### 局限性与未来方向记录

Execute 过程中发现的局限性和未探索方向，[MUST] 追加到 `paper_materials/05_limitations.md`（支撑论文结论"工作展望"节）：

- 未覆盖的场景或实验条件
- 方法假设的适用边界
- 性能退化的触发条件
- 消融实验揭示的模块依赖关系

记录时机：每个实验判定完成后，在自检 4 问中自然发现时立即记录，不攒到 Execute 结束。

---

## Step 6：结果可视化

[MUST] 遵循领域标准图表范式（通信领域图表模板和自检清单见 `domain-comms.md`）。

### 通用可视化要求

- 误差棒必须添加（随机实验）
- 所有 baseline 在同一图上
- 图例完整，曲线可区分（颜色 + 标记）
- 统计显著性已标注
- 仿真参数已标注（数据量、种子数、置信水平）

---

## 完成条件

- [ ] 核心实验完成，假设已判定
- [ ] 至少 1 组 baseline 对比完成
- [ ] 至少 1 组消融实验完成
- [ ] 所有结果与 Contract 无矛盾
- [ ] 达标判定通过
- [ ] 所有实验在同一数据集上执行
- [ ] MVE 对比已完成（如适用）
- [ ] **路径合规**：结果在 `projects/{name}/results/`，不在其他位置

---

## 设计决策记录

> 以下段落记录框架规则的设计背景，供理解"为什么这样规定"。不影响执行。

**Step 0 逐模块验证**：leo-mega-constellation-gnn-routing 项目中，6 个仿真器模块全部写完才做 smoke test，积累了 4 个 bug（方向 mask 单向、batch PE 维度错误等）。逐模块验证能更早发现，不增加总验证时间。

**Step 1 MVE 对比**：leo-mega-constellation-gnn-routing 项目中，MVE 报告 83-87% 保留率，Quick Test 只有 62-70%。13pp 差异未分析就继续推进，导致后续对 RL 突破 80% 的预期缺乏依据。

**Step 2 实验执行纪律**：leo-isl-scheduling-drl REINFORCE 方案测试，写完 model+train+test 后直接跑完整 20 episode，结果超时/OOM 被杀，来回 5 轮任务管理才定位问题。如果先跑 1-2 episode 就能提前发现。

**Step 3 简单方法优于 DL**：isl-acm-pred 教训——同轨面 ISL SNR 标准差仅 0.30 dB，滑动平均 MAE 0.25 dB 优于 GRU 0.45 dB。这不是方法失败，而是信道本身太确定性。

**Step 4.5 防死胡同检测**：leo-isl-scheduling-drl Execute 阶段，agent 在"PPO 无法改善手写先验"的根本性瓶颈上迭代 v1→v2→v4→v5 共 1000+ 行对话，每次仅边际改善。类似模式在 beam-hopping（6种方法全部失败）中也曾出现。

**方法论漂移检测**：leo-iot-ra 在 E003 失败后重设计 E003-v2，属于必要的方法论修正而非漂移。但如果没有这个检查，容易滑入无计划的"看到结果后改方法"。
