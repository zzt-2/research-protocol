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

## Step 0：仿真器开发（逐模块验证）

> 起源：leo-mega-constellation-gnn-routing 项目中，6 个仿真器模块全部写完才做 smoke test，积累了 4 个 bug（方向 mask 单向、batch PE 维度错误等）。逐模块验证能更早发现，不增加总验证时间。

按 `data-flow.md` 的模块划分逐步实现。每个模块写完后立即验证，不攒到一起。

### 逐模块验证节奏

```
模块 A 实现 → 跑 assertion（10 行以内）→ 确认通过 → 模块 B 实现 → ...
```

每个模块的 assertion 检查该模块的核心不变量：

| 模块 | 典型 assertion |
|------|---------------|
| 星座/网络配置 | 节点数正确、坐标范围合理、轨道周期正确 |
| 拓扑连接 | 度数分布符合预期、ISL 距离范围合理、断链率与 Step 3 验算一致 |
| 信道/链路 | 容量/时延范围合理、跨配置单调性正确 |
| 流量生成 | 流量矩阵形状正确、OD 对数量匹配 |
| 路由 | Dijkstra 路径存在性、时延范围合理 |
| RL 环境 | 状态空间维度与 data-flow.md 一致、动作空间合法、奖励非零 |
| 模型 | 输入维度匹配、输出维度匹配、参数量合理 |
| 集成 smoke test | 端到端一次 forward pass + 一次 Dijkstra baseline + 指标计算 |

[MUST] 每个模块的 assertion 结果记录到 decision_log（一行即可，如 `[AUTO] constellation.py assertion 通过：66/100/200/720 卫星坐标范围 [6771, 7121] km`）。

### 实现级反模式验证

代码实现完成后，对照 Contract Step 5 的反模式排查结果，验证代码是否忠实实现：
- 消融实验的零向量替代是否正确实现
- 共享数据集（拓扑快照 + 流量矩阵）是否在所有实验间复用
- 超参搜索预算是否一致

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

> 起源：leo-mega-constellation-gnn-routing 项目中，MVE 报告 83-87% 保留率，Quick Test 只有 62-70%。13pp 差异未分析就继续推进，导致后续对 RL 突破 80% 的预期缺乏依据。

---

## Step 2：核心实验

仿真分级执行：**smoke → quick → full**，每级通过后才进下一级。

- **smoke**：验证逻辑正确性。失败只改代码不改设计
- **quick**：小规模数据判断方向
- **full**：完整数据出发表级结果

各级时间预算由研究者根据仿真复杂度自定，不设硬性上限。卫星系统级仿真单次可达小时级，时间限制不现实。

### 随机种子要求

| 仿真类型 | 最低种子数 | 理由 |
|---------|-----------|------|
| 确定性仿真 + 可控随机噪声 | ≥3 组 | 主随机源只有噪声种子 |
| 含多随机成分（流量模型、用户分布、信道随机化） | ≥5 组 | 随机源多需要更多样本 |

### 结果记录

结果记录到 `results/{实验名}.md`（模板见 `templates.md`）。

---

## Step 3：假设判定

对照 Contract 判定：

| 判定 | 条件 | 动作 |
|------|------|------|
| PASS | 达到 success_signal | 继续补充实验 |
| MARGINAL | 方向对但幅度不够 | 分析原因，决定是否继续 |
| FAIL | 未达 success_signal | 诊断：实现问题 → 指标问题 → 方法问题 |

**简单方法优于 DL**：这不是 FAIL，但 [MUST] 调整叙事。可选叙事方向：
- "可行性验证"：ISL 信道可预测性验证
- "条件边界分析"：什么条件下 DL 有优势
- "对比基准"：系统对比 DL vs 传统方法

> isl-acm-pred 教训：同轨面 ISL SNR 标准差仅 0.30 dB，滑动平均 MAE 0.25 dB 优于 GRU 0.45 dB。这不是方法失败，而是信道本身太确定性。

[MUST] FAIL 或 MARGINAL 判定时通知用户，等待决策。

---

## Step 4：补充实验（PASS 后执行）

- **对比实验**：核心方法 vs 全部 baseline（必要）
- **消融实验**：按 Contract 中的 ablation_plan（必要）
- **鲁棒性验证**：参数敏感性、场景泛化（按需）
- **可视化论证**：消融实验除定量结果外，[SHOULD] 准备可解释性图表（SHAP 特征重要性、Grad-CAM 热力图、案例分析图等），路径记录在 experiment_result 的"可视化"字段
- **达标即停**：核心 + 对比 + 消融完成 → 停止

[MUST] 补充实验范围变更需用户确认。

---

## Step 5：结果自检

[MUST] 每个实验完成后回答 4 问：

1. 结果与 Contract 的 success/failure signal 是否一致？
2. 本实验与之前实验的结果有无矛盾？
3. 如现在必须停下，结果是否足够清晰可复现？
4. 实验设计是否存在信息泄露？

每完成 3 个实验，额外检查：当前方法是否偏离 Contract 定义（方法论漂移检测）。

> 为什么需要漂移检测：leo-iot-ra 在 E003 失败后重设计 E003-v2，属于必要的方法论修正而非漂移。但如果没有这个检查，容易滑入无计划的"看到结果后改方法"。

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
