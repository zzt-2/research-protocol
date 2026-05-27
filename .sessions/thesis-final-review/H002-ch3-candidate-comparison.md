# Handoff: Ch3 候选项目快速对比

> 来源: S010+S011 | 交接目标: 对比 leo-congestion-routing 和 hgat-satellite-dag-offloading，决定哪个作为论文第三章
> 文件名: H002-ch3-candidate-comparison.md

## 已完成边界

thesis-final-review 已完成 S001-S011（11 个对话），覆盖三章的竞品分析、方法论审查、技术修复、数据确认、统计补充、符号统一、元分析框架。

**但发现严重章节分配不一致**：
- 早期专题（direction-scouting、thesis-structure-research、chapter-quality-audit、thesis-chapter-fixes）将 **leo-congestion-routing** 作为 Ch3
- thesis-final-review（S001-S011）将 **hgat-satellite-dag-offloading** 作为 Ch3
- **无任何决策记录说明替换原因**
- 两个项目均已完成实验，数据可用

## 不要做什么

1. **不要跑完整终审** — 本轮只做快速对比，不是完整 review
2. **不要同时改两个项目** — 先决定用哪个
3. **不要仅凭"数据多"判断** — 重点看贡献强度、与 Ch1/Ch2 的差异化、叙事连贯性
4. **不要忽略"与 Ch1 重叠"问题** — congestion-routing 和 Ch1 都是路由方向，这是最大的结构性风险
5. **不要假设 hgat 已审完就一定更好** — hgat 的贡献本身很弱（peak 无优势），congestion-routing 可能更有价值

## 必读

按优先级排列：

### 已有 hgat 终审结论（了解基线）

1. `.sessions/thesis-final-review/topic-index.md` — 完整结论列表，重点看"其他结论"第 4 条（Ch3 零样本失败）和结论 44（Ch3 贡献校准）
2. `.sessions/thesis-final-review/S009-ch3-training-data-recovery.md` — Ch3 训练误判修正，含 D019 完整数据
3. `.sessions/thesis-final-review/S008-ch2-ch3-data-confirmation.md` — Ch3 合规结果（2/8 PASS, 4 FAIL）

### congestion-routing 审计结论（需提取）

4. `projects/leo-congestion-routing/master-state.md` — 项目当前状态
5. `projects/leo-congestion-routing/decision_log.md` — 决策历史
6. `projects/leo-congestion-routing/paper_materials/03_experiments.md` — 实验结果
7. `.sessions/chapter-quality-audit/` 下 congestion-routing 相关的审计报告
8. `.sessions/thesis-chapter-fixes/topic-index.md` — Ch3 修复记录
9. `.sessions/thesis-structure-research/S003-three-chapter-audit.md` — 三章审计（congestion-routing 作为 Ch3）

### 两个项目的数据

10. `projects/leo-congestion-routing/results/` — congestion-routing 实验数据
11. `projects/hgat-satellite-dag-offloading/simulator/results/results_summary.json` — hgat 数据

### 竞品信息

12. `projects/leo-congestion-routing/literature_notes.md` — 竞品和文献
13. `projects/hgat-satellite-dag-offloading/literature_notes.md` — 竞品和文献

## 接口变更

无代码改动。此 handoff 仅为评估和决策交接。

## 快速对比维度（~5-8 个子 agent）

### Agent 1: 数据完备性对比
- congestion-routing: 有多少实验？几个 seed？数据是否完整？
- hgat: 6 模型×3 seed ✅，但零样本数据缺失
- 输出：数据完备性对比表

### Agent 2: 贡献强度评估
- congestion-routing: GNN vs ECMP/MLP 的优势有多大？故障弹性结果如何？
- hgat: peak 无优势（-11.6~-12.0），仅训练稳定性 2.4x
- 输出：贡献强度评级（强/中/弱）

### Agent 3: 与 Ch1/Ch2 差异化分析（最关键）
- congestion-routing 与 Ch1（leo-mega-constellation-gnn-routing）都是 LEO 路由问题。差异在哪？是否能论证为"不同问题"？
- hgat 是计算卸载问题，天然不同于路由和切换
- 输出：差异化评估 + 重叠风险

### Agent 4: 方法论合规对比
- hgat: 2/8 PASS, 4 FAIL（缺 DAG 变体/多指标/环境扫描/统计报告）
- congestion-routing: 需查（chapter-quality-audit 有记录）
- 输出：合规对比表

### Agent 5: 竞品威胁对比
- hgat: HGAT+DAG+卫星 CNKI 零结果 ✅
- congestion-routing: 需查（TELGEN Zhou'25 ToN 是最强竞品，projects-overview 有记录）
- 输出：竞品威胁评估

### Agent 6: 叙事连贯性分析
- hgat 作为 Ch3: 规模不变(Ch1) → 排列等变(Ch2) → 类型感知(Ch3)
- congestion-routing 作为 Ch3: 规模不变(Ch1) → 排列等变(Ch2) → ???(Ch3)
- 三章统一论点 "When does GNN work?" 在两种选择下分别如何展开？
- 输出：两种叙事路径的对比

## 评估标准

| 维度 | 权重 | 优先考虑 |
|------|------|---------|
| 与 Ch1/Ch2 差异化 | 最高 | 越不同越好 |
| 贡献强度 | 高 | 越强越好 |
| 竞品空白 | 高 | 越空越好 |
| 数据完备性 | 中 | 够用就行 |
| 方法论合规 | 中 | 可补就行 |
| 叙事连贯性 | 中 | 能串就行 |

## 决策输出

对比完成后，给出明确建议：

- **A: 用 congestion-routing** → 后续跑完整终审（~30 子 agent）
- **B: 用 hgat** → 维持现有 thesis-final-review 结论，不再重审
- **C: 两个都不行** → 需要找新的 Ch3 方向（严重情况）
- **D: 需要更多信息** → 指出缺什么

## 已知债务

| 债务 | 说明 |
|------|------|
| hgat 零样本数据缺失 | D020 的数值未验证，eval_generalize.py 可随时重跑 |
| congestion-routing 终审未做 | 如果选它需要补完整终审流程 |
| 三章符号统一只覆盖了 hgat 版 | 如果换 congestion-routing，S011 的符号修正需重做 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已读取 S003 three-chapter-audit（congestion-routing 作为 Ch3 的审计）
- [ ] 已读取 chapter-quality-audit 中 congestion-routing 的审计报告
- [ ] 已确认两个项目的 projects-overview 状态

## 下一轮

1. **快速对比**（本对话）：5-8 个子 agent 并行，产出对比表 + 建议
2. **决策**：用户选择 A/B/C/D
3. **如选 A**：开新对话跑 congestion-routing 完整终审
4. **如选 B**：回到主线，继续开题准备
5. **如选 C/D**：讨论替代方案
