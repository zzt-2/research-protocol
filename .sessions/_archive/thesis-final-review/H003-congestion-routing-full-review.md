# Handoff: leo-congestion-routing 完整终审

> 来源: S012 | 交接目标: 对 leo-congestion-routing 执行与 Ch1/Ch2 同等标准的完整终审（对标 S001-S011）
> 文件名: H003-congestion-routing-full-review.md

## 已完成边界

1. Ch1（leo-mega-constellation-gnn-routing）终审完成（S001-S011）
2. Ch2（leo-ntn-handover-drl）终审完成（S001-S011）
3. **Ch3 已确认变更为 leo-congestion-routing**（S012 决策，基于 H002 快速对比）
4. hgat-satellite-dag-offloading 已从论文移除，不再作为论文章节
5. leo-congestion-routing 已通过早期审计（chapter-quality-audit + thesis-chapter-fixes），质量评估"学位论文章节够用"

## Ch3 项目信息

- **项目目录**: `projects/leo-congestion-routing/`
- **方向**: GNN 在 LEO 故障弹性路由中的鲁棒性验证
- **核心技术**: Walker-Delta 物理仿真(alt=550km) + M/M/1排队延迟模型 + GNN message passing
- **实验状态**: Execute 全部完成，12 组实验，3 seed
- **核心结论**: GNN/ECMP delay=0.80 (GNN 延迟 -20%), 故障场景 11/12 胜率
- **贡献结构**: ~80% 来自故障场景。无故障时 GNN≈ECMP，故障是 GNN 优势的必要激活条件

## 不要做什么

1. **不要按 hgat 的标准来审** — hgat 是 GW 阶段项目，congestion-routing 是 Execute 完成的成熟项目，起点不同
2. **不要重新跑实验** — 数据已完整（12 组 × 3 seed 全量 GPU 重跑完成）
3. **不要质疑"两章路由"的合理性** — S012 已决策，Ch1(规模泛化/无故障) vs Ch3(故障弹性/故障驱动)重叠风险低
4. **不要照搬 S001-S011 的流程编号** — 参考其覆盖维度，但按 congestion-routing 的实际情况组织
5. **不要漏掉 Ch1 重叠隔离验证** — 这是 Ch3 作为论文章节的最大风险点，必须仔细评估叙事隔离是否充分

## 必读

按优先级排列：

### 项目核心文件

1. `projects/leo-congestion-routing/master-state.md` — 项目编排状态
2. `projects/leo-congestion-routing/decision_log.md` — 决策历史
3. `projects/leo-congestion-routing/paper_materials/03_experiments.md` — 实验结果（最关键）
4. `projects/leo-congestion-routing/paper_materials/01_research_context.md` — 研究背景
5. `projects/leo-congestion-routing/paper_materials/02_method.md` — 方法设计
6. `projects/leo-congestion-routing/paper_materials/06_formulas_symbols.md` — 公式符号
7. `projects/leo-congestion-routing/literature_notes.md` — 文献笔记
8. `projects/leo-congestion-routing/baseline_report.md` — 基线报告
9. `projects/leo-congestion-routing/feasibility_report.md` — 可行性报告

### 早期审计记录

10. `.sessions/chapter-quality-audit/` — Ch3 审计报告（leo-congestion-routing 作为 Ch3 的审计）
11. `.sessions/thesis-chapter-fixes/topic-index.md` — Ch3 修复记录
12. `.sessions/thesis-structure-research/S003-three-chapter-audit.md` — 三章审计

### 参照标准（Ch1/Ch2 终审覆盖了什么）

13. `.sessions/thesis-final-review/topic-index.md` — 完整结论列表，理解终审覆盖的维度
14. `.sessions/thesis-final-review/S001-ch2-competitor-methodology.md` — Ch2 竞品+方法论审查范例
15. `.sessions/thesis-final-review/S002-ch1-ch3-competitor-methodology.md` — Ch1 竞品+方法论审查范例（注意：这里的 Ch3 指 hgat，不是 congestion-routing）
16. `.sessions/thesis-final-review/S006-ch1-ch2-technical-review.md` — Ch1+Ch2 技术审查范例
17. `.sessions/thesis-final-review/S008-ch2-ch3-data-confirmation.md` — 数据确认+统计补充范例

### 数据文件

18. `projects/leo-congestion-routing/results/` — 实验数据目录
19. `projects/leo-congestion-routing/simulator/` — 仿真器代码

## 需要覆盖的终审维度（对标 S001-S011）

以下维度按 S001-S011 对 Ch1/Ch2 的覆盖标准列出。每个维度建议 1-2 个子 agent。

### Phase 1: 竞品 + 方法论（对标 S001-S003）

| # | 维度 | 子 agent 任务 | 参考 |
|---|------|-------------|------|
| 1 | 竞品检索验证 | 验证 literature_notes 的竞品覆盖是否完整（GNN+拥塞路由+卫星、GNN+故障弹性+LEO） | S001-1a, S002-2a |
| 2 | 方法论精读 | 读 3-4 篇代表论文，检查 congestion-routing 的实验设计是否达到通行标准 | S001-1c, S002-2c |
| 3 | 跨章叙事定位 | 验证 Ch3 故障弹性定位与 Ch1 规模泛化的隔离是否充分；三层叙事如何适配 | S003-3d |

### Phase 2: 技术审查（对标 S005-S006）

| # | 维度 | 子 agent 任务 | 参考 |
|---|------|-------------|------|
| 4 | 仿真参数审查 | 逐项检查 config/env 参数合理性，对比文献范围 | S006-5a, S005-6a |
| 5 | 公式/指标审查 | 检查核心公式正确性、指标定义一致性、排队模型描述准确性 | S006-5b/5d, S005-6b |
| 6 | 跨章公式一致性 | 与 Ch1/Ch2 的 Shannon/FSPL/星座参数对比 | S005-6c |

### Phase 3: 数据确认 + 统计（对标 S008-S009）

| # | 维度 | 子 agent 任务 | 参考 |
|---|------|-------------|------|
| 7 | 数据溯源 | 全量 JSON 与 paper_materials 逐条核对 | S008-7a |
| 8 | 统计补充 | 计算 bootstrap 95% CI + Welch's t-test（如已有则验证） | S008-7f |
| 9 | 合规 checklist | 按 S001-S002 合规标准逐项检查 | S008-7e |

### Phase 4: 符号统一 + 贡献校准（对标 S011）

| # | 维度 | 子 agent 任务 | 参考 |
|---|------|-------------|------|
| 10 | 符号统一 | 与 Ch1/Ch2 的 06_formulas_symbols 对齐，修正冲突项 | S011-8a/8g |
| 11 | 贡献校准 | 基于故障激活贡献结构，校准 Ch3 创新点定位 | S011-8f |

### Phase 5: 可视化

| # | 维度 | 子 agent 任务 | 参考 |
|---|------|-------------|------|
| 12 | 图表生成 | 生成 Ch3 核心结果图（故障率消融、故障模式对比等） | S008-7g |

## 特别关注项

### 1. Ch1 重叠隔离验证（最高优先级）

congestion-routing 作为 Ch3 的最大风险是"两章路由"。必须验证：
- Ch3 的实验结果能否完全用"故障场景"支撑，而非依赖正常场景？
- E02（无故障基线 GNN/ECMP=1.018，ECMP 赢）是否已在 paper_materials 中诚实报告？
- 标题/摘要/贡献是否明确强调"故障弹性"而非"路由优化"？

### 2. 排队模型描述

projects-overview 写"M/M/1排队延迟模型"，但 S005 结论 1 指出 hgat 的排队模型是确定性 FIFO 非 M/M/1。congestion-routing 的排队模型需要确认：
- 如果也是确定性 FIFO，paper_materials 必须修正描述
- 如果确实是 M/M/1（泊松到达+指数服务），需说明为什么合理

### 3. TELGEN 竞品威胁

projects-overview 标记"TELGEN (Zhou'25 ToN) 是最强竞品"。需评估：
- 与 TELGEN 的差异化是否充分（LEO 时变拓扑 vs 静态？故障场景 vs 正常？）
- 是否需要额外引用或对比

### 4. K-path 范式

projects-overview 记录"K-path 范式迁移（D15）是关键架构决策——从 per-flow 路由改为 per-edge 权重"。需确认：
- paper_materials 是否准确描述了这个范式
- 与 Ch1 的决策范式（监督分类）是否足够不同

## 验证阈值

| 验证项 | PASS 标准 |
|--------|----------|
| 数据完整性 | 12 组实验全部有结果，3 seed 一致 |
| 统计报告 | bootstrap CI + t-test 已计算 |
| 合规率 | ≥ 6/8 PASS（hgat 为 2/8，congestion-routing 应更高） |
| Ch1 隔离 | 故障场景贡献 ≥ 60% |
| 竞品覆盖 | 无高威胁遗漏 |
| 公式正确 | 核心 P0 项 = 0 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已读取 S003 three-chapter-audit（congestion-routing 作为 Ch3 的审计）
- [ ] 已读取 chapter-quality-audit 中 congestion-routing 的审计报告
- [ ] 已读取 projects/leo-congestion-routing/master-state.md
- [ ] 已读取 projects/leo-congestion-routing/paper_materials/03_experiments.md
- [ ] 已确认贡献结构（故障场景~80%）与 H002 快速对比一致

## 下一轮

1. **Phase 1**（3 个子 agent）：竞品验证 + 方法论精读 + 跨章叙事定位
2. **Phase 2**（3 个子 agent）：参数审查 + 公式审查 + 跨章一致性
3. **Phase 3**（3 个子 agent）：数据溯源 + 统计补充 + 合规检查
4. **Phase 4**（2 个子 agent）：符号统一 + 贡献校准
5. **Phase 5**（1 个子 agent）：图表生成
6. 完成后回到主线：最终一致性检查（对话14）→ 开题报告
