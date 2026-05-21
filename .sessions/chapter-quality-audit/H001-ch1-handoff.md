# Handoff: Ch1 路由 Size Generalization 质量审计

> 来源: S001 | 交接目标: 对 Ch1 做全面质量审计，输出问题清单+修复建议
> 文件名: H001-ch1-handoff.md

## 已完成边界

- S003 三章审查已完成，Ch1 判定：核心 PASS、消融 WARN、中文引用 FAIL（后补充完成）、论文写作零进度
- 核心实验 E01-E05 全部完成，E06-E09 未做
- 中文引用 CN01-CN17 已补充至 04_literature.md
- 素材包 6 文件 109KB 就绪

## 不要做什么

- 不要写论文正文
- 不要跑新实验（除非审计发现必须补做且用户同意）
- 不要修改已有实验数据
- 不要在主对话做大量文件阅读——全部委托子 agent

## 必读

1. `.sessions/chapter-quality-audit/topic-index.md`（专题总控）
2. `.sessions/thesis-structure-research/S003-three-chapter-audit.md`（前置审查结论）
3. `projects/leo-mega-constellation-gnn-routing/paper_materials/`（6 文件，素材包）
4. `projects/leo-mega-constellation-gnn-routing/contract.md`（假设+实验计划）
5. `projects/leo-mega-constellation-gnn-routing/decision_log.md`（D01-D21）
6. `.sessions/2026-05-13-mega-constellation-gnn-routing/topic-index.md`（Ch1 专题结论）

## Ch1 核心信息摘要

### 核心声称（4条）
1. GNN 路由策略小星座监督训练后零样本泛化到 720 星（11x），时延保留率 90.3%
2. 加权 Dijkstra 推理用 GNN logits 构造边权重，解决贪心推理成功率极低
3. Orbital PE 是模型可学习性的前提条件（非可选增强）
4. 多尺度混合训练贡献 2-4pp stretch 改善

### 实验清单
- ✅ E01: 核心跨规模泛化（66+100+200→720）
- ✅ E02: 三方对比（Ours vs GRLR vs Dijkstra）
- ✅ E03-E05: 消融 A1(无PE) / A2(无多尺度) / A3(无PE+无多尺度)
- ❌ E06: 不同流量模式鲁棒性
- ❌ E07: 不同规模因子（5x/11x/24x, 1584星）
- ❌ E08: GNN 深度消融（A4）
- ❌ E09: PE 类型对比消融（A5）

### 指标
M1 平均端到端时延(ms), M2 最大链路利用率(%), M3 P95时延(ms), M4 规模泛化保留率, M5 路径最优性比(%)

### Baseline
B1 Dijkstra✅, B2 GRLR(TVT'25)✅, B3 GraphPR(TVT'25)❌未复现

### 竞品
GRLR(同规模路由标杆), TELGEN(WAN TE非卫星), GPN(TMC'25, 30→50节点), Scaling Swarm(AI'25, 3x简单场景)

### 已知风险
1. 单 seed(123) 评估——Contract 规定 5 seed
2. E06-E09 四个实验未做——论文缺鲁棒性和 PE 类型消融
3. M2/M3/M5 指标在实验中未被报告
4. PE 贡献叙事需从"渐进增强"转为"必要条件"
5. 最后文献检索 2026-05-13（距今 9 天）

## 审计执行计划

### Phase 1: 文献新鲜度 & 新颖性（2 个子 agent 并行）

**Agent 1A — 最新文献检索**
- 输入：Ch1 的核心关键词组合（GNN + LEO routing + size generalization / zero-shot transfer / cross-scale）
- 执行：用 `bash tools/search` 做 4-6 组检索（arXiv + Semantic Scholar），时间范围 2026-01 至今
- 输出：新发表论文列表（标题+年份+摘要+与我们的重叠度判定：HIGH/MEDIUM/LOW/NONE）
- 约束：单 agent ≤15min，检索结果保存到 `projects/leo-mega-constellation-gnn-routing/search-archive/`

**Agent 1B — 已有竞品深化核查**
- 输入：读 `projects/leo-mega-constellation-gnn-routing/literature_notes.md` + `04_literature.md`
- 任务：
  1. 列出所有已识别竞品（含 S003 中提到的 TELGEN、GRLR 等）
  2. 对每个竞品，提取其核心 method + experiment 范围
  3. 判定我们的差异化是否仍然成立（SAFE / AT RISK / COMPROMISED）
- 输出：竞品-差异化矩阵（竞品名 | 我们声称 | 竞品做了什么 | 差异判定 | 论证要点）

**Phase 1 汇总**：主线程合并 1A+1B，写入新颖性判定结论。

### Phase 2: 实验完备性对标（2 个子 agent 并行）

**Agent 2A — 领域 Top 论文实验清单提取**
- 输入：精读 2-3 篇领域标杆论文（GRLR TVT'25, TELGEN ToN'25, GPN TMC'25）的 experiment 章节
- 任务：逐项提取每篇的实验维度——
  - Baseline 数量和类型（启发式/学习方法/最优解）
  - 消融实验项数和覆盖维度
  - 统计检验方法（seed 数、CI、p-value）
  - 可视化类型（收敛曲线、heatmap、CDF 等）
  - 指标集合
  - 泛化/鲁棒性实验设计
- 输出：标杆实验 checklist 表

**Agent 2B — 我们的实验覆盖度自检**
- 输入：读 Ch1 的 contract.md + paper_materials/ 全部文件
- 任务：按 Agent 2A 提供的 checklist 模板逐项对比
  - 每项标注：✅ COVERED / ⚠️ PARTIAL / ❌ MISSING
  - MISSING 项评估影响：CRITICAL（必须补）/ IMPORTANT（建议补）/ NICE-TO-HAVE（可跳过）
- 输出：覆盖度矩阵 + 缺失影响评估

### Phase 3: 指标完整性 + 数据自洽性（2 个子 agent 并行）

**Agent 3A — 指标完整性**
- 输入：读 Ch1 paper_materials + 领域 top 论文的指标列表
- 任务：
  1. 列出该领域标准指标全集
  2. 标注我们已报 / 未报
  3. 未报指标：能否从现有数据计算？需补实验？
- 输出：指标矩阵（指标名 | 我们有 | 来源 | 补救方案）

**Agent 3B — 数据自洽性验证**
- 输入：读 Ch1 paper_materials/ 全部 6 文件 + results/ 目录原始数据
- 任务：
  1. 提取 paper-materials 中所有定量声称（数字+上下文）
  2. 追溯每个数字到原始实验结果文件
  3. 同一数字在不同文档中是否一致
  4. 实验条件描述是否与 contract 一致
- 输出：数据溯源表 + 矛盾清单

### Phase 4: 汇总与输出

主线程合并 Phase 1-3 结果，输出以下文档：

1. **审计报告**（写入 `.sessions/chapter-quality-audit/S002-ch1-audit.md`）：
   - 新颖性判定（SAFE/AT RISK/COMPROMISED）+ 证据
   - 实验覆盖度 checklist
   - 指标矩阵
   - 数据自洽性报告
   - Baseline 合法性评估

2. **问题清单**（按优先级排序）：
   - P0 CRITICAL：必须修复才能投稿
   - P1 IMPORTANT：强烈建议修复
   - P2 NICE-TO-HAVE：锦上添花

3. **更新 H001 交接文档**：补充审计发现

## 接口变更

无

## 失败数据附录

无

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 单 seed 评估 | Contract 规定 5 seed | 仅 seed=123 | 审计判定为 CRITICAL 则补跑 |
| E06-E09 未做 | 实验完备性 | 未启动 | 审计判定缺少鲁棒性数据则补做 |
| M2/M3/M5 未报 | 指标完整性 | 有数据未提取 | 审计判定需报告则从 results 提取 |
| GraphPR 未复现 | Baseline 合法性 | Contract 标"推荐" | 审计判定需对比则复现 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| 新颖性 | 核心声称无实质性重叠 | GW S4 |
| 实验覆盖 | Top 论文实验维度 80%+ 覆盖 | Contract S5 |
| 指标完整 | 领域标准指标 90%+ 报告 | domain-comms.md |
| 数据自洽 | 0 矛盾 | 框架通用要求 |
| Baseline 公平 | 声称的超越有公平对照 | GW S4-7 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 S003 中 Ch1 的审查结论（核心 PASS、消融 WARN）
- [ ] 已确认当前范围：只做审计不做写作
- [ ] 已检查必读文件中至少 3 个存在且可读

## 下一轮

1. 新对话读取本交接文档 + topic-index
2. 按 Phase 1→2→3→4 顺序执行，每 Phase 内子 agent 并行
3. 审计报告写入 S002，问题清单更新到本交接文档
4. 完成后更新 topic-index 进展线索
