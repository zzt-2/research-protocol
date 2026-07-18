你是 CCISP 2026 论文写作专题的一个子对话执行者。本轮任务：建立 revision-queue.md——把所有待改项集中登记，为后续按 R013 批次改稿做准备。

## 背景

写作战役 + 加厚 + 数据用法调研全完成了。过程中积累了来自各方的待改项：① R013 原 Q1-Q6（3 个 TBD + F1 判断项）② F1 力度对照的遗留 ③ R014 加厚后的审查发现 ④ R015 数据用法差异清单 ⑤ 用户最近的方法论纠正（不报弱湍流归零数字）。这些散在各处，必须集中登记到 revision-queue.md，导师反馈来了 + 用户决策定了之后按 R013 批次一次性处理。

## 必读（读完再建 queue）
1. .sessions/2026-07-09-thesis-writing/R013-revision-protocol.md —— 改稿章程（L1-L6 分级 + 批次化流程 + 三条防错纪律）。queue 的格式和分级标准来自这里
2. .sessions/2026-07-09-thesis-writing/R015-data-usage-pattern.md —— 数据用法差异清单（产出 2 的 5 处差异，是待改项的重要来源）
3. .sessions/2026-07-09-thesis-writing/F001-strength-check-figures.md —— F1 修正遗留（3 个 TBD 标记区 + ⑤ hedging 是否跟导师同步）
4. .sessions/2026-07-09-thesis-writing/W005-expand-record.md —— 加厚后的状态（加厚引入什么/没引入什么）
5. .sessions/2026-07-09-thesis-writing/W002-method-results.md —— §IV-B 当前状态（四套数字挤一段的问题源头）
6. .sessions/2026-07-09-thesis-writing/R012-params-narrative.md —— 数字清单（判断数字去留时查溯源）
7. .sessions/2026-07-09-thesis-writing/decisions.md —— 已有决策（D002/D004 等涉及待改项的）

## 本轮目标

建立 .sessions/2026-07-09-thesis-writing/revision-queue.md，登记所有待改项。**只登记不改正文**（正文改是后续批次的事）。

### 待改项来源（逐源梳理，不遗漏）

**来源 A：R013 原 Q1-Q6**（已在 R013 末尾登记）
- Q1 §IV-A 纵轴范围（D003，TBD 标记区①）→ L2+L3，pending 导师定 A/B
- Q2 §IV-A 1e-5 解读措辞（D003，TBD 标记区②）→ L1，pending 导师定 A/B
- Q3 §IV-B 标题数字口径 naive/fair（D004，TBD 标记区③）→ L2，pending 导师定
- Q4 Tab.1 是否加 fair 对照列 → L3，pending 导师定
- Q5 ⑤ hedging（locally optimal→lower BER）是否需跟导师同步 → L1，pending 用户决定
- Q6 主对比文献（参考文献核心一条）→ L1，pending 导师定

**来源 B：R015 数据用法差异清单**（5 处差异 → 待改项）
- R015 差异 1：§IV-B 四套数字挤一段（naive+net+归零+分母29）密度高于主流 → L2+L3（重分配载体）
- R015 差异 2：Tab.1 与正文数字冗余（1.26/1.19/1.85 表里正文又列）→ L3（正文删冗余引"as in Table I"）
- R015 差异 3：逐点证据全列正文（对标集挑代表或进图）→ L3（逐点移 Tab.1/Fig，正文摘代表）
- R015 差异 4：增益 2 位小数（对标集 1 位+about/~）→ L1（精度调整 1.85→~1.8 等）
- R015 差异 5：naive+net 两口径同段混（对标集单一或分场景）→ L2（拆段或分场景标）

**来源 C：用户最近的方法论纠正**（最重要的一条新发现）
- **不报弱湍流归零数字**：弱湍流 0.09/0.18/0.19 是不利数字，按 R015 惯例不主动报。正文（§IV-B "reported transparently"+§V Conclusion "+0.09/+0.18/+0.19"）应删具体数字改定性表述（"gains concentrate in strong turbulence"）。底层 30seed 数据留仿真日志不进论文（数据诚实 ≠ 呈现诚实）。→ L2，**pending：这是对不变量 3 的细化，建 D### 记录"数据诚实 vs 呈现选择"的澄清**

**来源 D：其他审查发现**（从前面对话梳理）
- 29 分母未定义（正文 5 处"26 of 29"但没定义 29 怎么来）→ L2，pending：补定义 or 改表述（涉及 R008 贡献措辞，可能建 D###）
- 30-seed 反复当卖点（§IV-B "within the 30-seed confidence interval" + Conclusion 同）→ L1，收敛到设置段提一次
- DA pilot 用法需核实（单 pilot 还是多 pilot？h_b 怎么估？）→ **需先派 agent 查代码确认事实，再定改不改**，pending 核实
- γ_th 怎么定的需核实（代码里 crossover 取法）→ 同上，pending 核实

### queue 格式

```markdown
# Revision Queue——CCISP 2026 待改项登记

> 建于 2026-07-12 | 按 R013 批次化处理 | 改一条删一行（或标 done）

## 待改项总表

| # | 来源 | 待改项 | 初判级别 | 涉及决策 | 状态 | 改法方向（待定）|
|---|---|---|---|---|---|---|
| Q1 | R013 | §IV-A 纵轴范围 | L2+L3 | D003 | pending 导师定 A/B | A=硬凑1e5/B=画到能画到 |
| ... |

## 需先核实事实的（派 agent 查代码后再定）
| # | 核实项 | 查什么 | 影响 |
|---|---|---|---|
| F1 | DA pilot 用法 | _recovery.py 单/多 pilot | §III DA 估计器描述准不准 |
| F2 | h_b 估计 | 代码里 h_b 怎么估的 | §II/§III 信号模型描述 |
| F3 | γ_th 取法 | γ_th 在代码里怎么定的 | §III 切换判据描述 |

## 批次触发条件（R013 §批次化）
满足任一即开批次处理：
1. 导师说"反馈完了"
2. 攒到 ≥3 条实质性（pending→ready）
3. deadline 倒推只剩改稿+转 LaTeX 时间
4. 用户主动决定"够了，开改"

## 批次处理顺序（R013，从底层到表层）
L6 定位 → L5 逻辑链 → L4 公式 → L2 数字/L3 图表 → L1 措辞 → 统一交叉检查
```

### 登记原则
1. **只登记不改正文**——本轮建 queue，正文改是后续批次
2. **逐源梳理不遗漏**——A/B/C/D 四个来源逐个过，每条进 queue
3. **初判级别标清楚**（L1-L6），但标注"初判，批次处理时再确认"
4. **涉及已有决策的标清楚**（D002/D004/R008/R009/不变量3），这类不能顺手改
5. **需核实事实的单列**（DA pilot/h_b/γ_th），标"pending 核实"
6. **状态用 pending/ready/done**——pending=等信息（导师/用户/核实），ready=可改，done=已改

## 输出
路径：.sessions/2026-07-09-thesis-writing/revision-queue.md
格式：如上模板（总表 + 需核实项 + 批次触发条件 + 批次顺序）

## 质量要求
1. **四源全覆盖**（A R013原Q1-Q6 / B R015差异 / C 用户纠正 / D 其他审查），不遗漏
2. **每条标级别 + 涉及决策 + 状态**，不能只列待改项不分类
3. **需核实项单列**，不混进总表（核实前不能定改法）
4. **不改正文**——只建 queue

## 完成判据
- queue 总表覆盖四源所有待改项（预计 12-15 条）
- 需核实项 ≥3 条（DA pilot/h_b/γ_th）
- 每条标级别/涉及决策/状态
- 批次触发条件 + 批次顺序写明

## 完成后做什么
1. 更新 topic-index.md「进展线索」新增一条"revision-queue.md 建立"（不算 R/W 编号，是治理文件）。
2. **在 revision-queue.md 末尾加一段「本轮总结」**（给旧对话审阅用）：
   - 本轮做了什么（一句话）
   - queue 共登记多少条（总数 + 分级别统计 + 分来源统计）
   - **重点请旧对话审查的 3 点**：①四源梳理有没有遗漏的待改项 ②初判级别合不合理（有没有该 L4 的标成 L1）③需核实项是否完整（DA pilot/h_b/γ_th 之外还有没有要查代码的）
3. commit（本对话统一提交一次，消息概括"revision-queue 建立"）。
