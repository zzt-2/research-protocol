# 论文素材提取工作流（通用版）

> 本文档定义从项目原始材料中提取论文写作素材的多步流程。
> 产出供论文写作平台自动消费，每个文件独立可检索。
> 本文件是框架级模板，存放在 `stages/paper-materials-workflow.md`。
> 项目级材料包存放在 `projects/{name}/paper_materials/`，不在根目录。

---

## 目标

将 GW/CT/EX 阶段的碎片化产出提取为 6 个结构化素材文件（总计 50-100 KB），覆盖论文写作平台"蓝图→大纲→正文"三阶段所需的全部维度。

## 输入

- 项目文档：`projects/{name}/contract.md`（或 `contract-ch{N}.md`）, `decision_log.md`, `literature_notes.md`, `baseline_report.md`
- 实验报告：`projects/{name}/results/*.md` 或项目 Execute 产出
- 竞品笔记：`projects/{name}/competitor_notes/*.md`
- 论文原文：`papers/` 下已下载的论文（按需查阅）
- 过程积累：`projects/{name}/paper_materials/05_limitations.md`（Execute 阶段逐步追加）

## 产出

所有产出放在 `projects/{name}/paper_materials/` 目录下：

```
projects/{name}/paper_materials/
├── 01_research_context.md  # 研究问题、动机、研究空白
├── 02_method.md            # 方法架构、公式、设计决策
├── 03_experiments.md       # 实验设置、全部结果数据、消融
├── 04_literature.md        # 相关工作分类、竞品对比、文献索引
├── 05_limitations.md       # 局限性与未来工作（Execute 中逐步积累）
└── 06_formulas_symbols.md  # 公式汇总与符号约定
```

> 通用模板（本文件）在 `stages/paper-materials-workflow.md`，不需要复制到项目目录。

---

## 平台需求映射

写作平台三阶段需要不同维度的素材：

| 平台阶段 | 主要消费文件 | 需要的素材维度 |
|----------|------------|--------------|
| 结构蓝图 | 01, 04, 05 | 论证主线、Gap-Contribution 映射、章节定位、论证闭环 |
| 大纲 | 02, 03, 06 | 术语约定、图表规划、数据映射、公式呈现决策、引用规划 |
| 正文 | 02, 03, 04, 06 | 完整方法描述、实验数据表、文献引用细节、公式推导 |

---

## 执行步骤

### Step 1: 建立提取框架

读参考协议（如有），确定 01-06 每个文件的 section 骨架。质量门槛：覆盖蓝图板块 + 评价维度。

### Step 2: 提取研究上下文 → `01_research_context.md`

**输入**：decision_log, literature_notes, baseline_report, feasibility_report
**Section 骨架**：

1. **问题定义**：具体研究挑战 + 关键数据（表格化）
2. **现有方法局限**：每条局限配论文证据，来源标注到 literature_notes 条目编号
3. **研究空白**：检索证据 + 空白确认
4. **新颖性确认**：核心要素组合 + 竞品排除表
5. **论文叙事弧线**：实验设计的递进逻辑（如"小规模验证 → 规模扩展 → 核心优势展示"）
6. **论证主线建议稿**：1-2 段连贯叙述
7. **Gap-Contribution 闭环映射表**：每个 Gap → 方法组件 → 结论回应 → 数据证据

**格式要求**：每条论点标注来源文件+决策编号；关键数字用表格；区分事实与待补充。

### Step 3: 提取方法细节 → `02_method.md`

**输入**：contract.md, data-flow.md, decision_log 中的方法设计决策
**Section 骨架**：

1. **架构总览**：端到端流程描述（配 ASCII 架构图）
2. **核心数据结构**：输入/输出/中间表示的维度表
3. **核心算法公式**：完整展开（内联 LaTeX），附维度推导
4. **关键模块设计**：每个创新模块的动机 + 公式 + 设计理由
5. **设计决策记录**：结构化三栏表（选择 / 理由 / 排除的替代方案），引用 decision_log 编号
6. **参数量分解**：逐层对比核心方法 vs baseline
7. **训练不稳定风险缓解**（如适用）
8. **与 Baseline 的代码复用关系**

**格式要求**：公式用 `$...$` 和 `$$...$$`；设计决策用结构化三栏表。

### Step 4: 提取实验数据 → `03_experiments.md`

**输入**：results/*.md, baseline_report, contract.md, decision_log
**Section 骨架**：

1. **仿真环境参数表**：完整参数，每个参数标注来源（contract/计算/文献）
2. **仿真器验证结果**：逐项 PASS 详情
3. **Baseline 复现结果**：全部 baseline 全部指标 + 与论文对比
4. **核心实验**：按实验编号逐个列出（指标表 + gap% + 来源）
5. **消融实验全表**：每项含变量/结果/结论
6. **训练配置对比**：核心方法 vs baseline 超参表
7. **数据一致性检查**：跨文件数字差异标注

**格式要求**：全部用表格；每个实验标注 seed 数、评估方式。

### Step 5: 提取文献定位 → `04_literature.md`

**输入**：literature_notes, competitor_notes/, baseline_report, novelty_search（如有）
**Section 骨架**：

1. **核心论文完整条目**：标题/作者/年份/来源/DOI/方法/结论/与本研究关系
2. **技术路线分类体系**：每条路线含论文列表 + 特征摘要
3. **竞品精确区分表**：每篇竞争论文的覆盖要素/缺失要素/威胁等级
4. **理论支撑文献**（如有）
5. **适配性分析汇总**：从 literature_notes 中提取每篇核心论文的适配点/不适配点/改进方向
6. **文献索引**：全部提及论文的 DOI/arXiv/URL 汇总

**格式要求**：每篇论文结构化条目；索引表按 ID 排序；标注精读/浅读状态。

### Step 6: 提取局限性 → `05_limitations.md`

**输入**：literature_notes §已知局限, contract.md, decision_log, Execute 阶段逐步追加的局限性记录
**Section 骨架**：

1. **仿真简化清单**：每项含现状/影响/可改进方向/相关文献
2. **规模上限讨论**（如适用）
3. **方法论局限**
4. **扩展方向**：每项含参考文献指向
5. **与最新工作的技术差距**

**格式要求**：每项配具体证据和文献引用。

> 注意：05_limitations.md 在 Execute 过程中就应开始积累（见 `stages/thesis-materials.md` §3），本步骤是系统化整理，不是从零开始。

### Step 7: 汇总公式与符号 → `06_formulas_symbols.md`

**输入**：02_method.md（Step 3 产出）、contract.md、data-flow.md
**Section 骨架**：

1. **核心公式及各项解释**
2. **关键算法公式**（完整 LaTeX）
3. **维度设计表**（每个模块的输入/隐层/输出）
4. **符号约定表**（符号/含义/单位/范围/首现章节）

**格式要求**：全部 LaTeX；符号表覆盖核心变量。

### Step 8: 交叉校验

**操作**：
- 逐文件检查来源标注完整性
- 跨文件数字一致性
- 覆盖度检查（蓝图板块 + 评价维度）
- 矛盾项标注
- 生成总索引

---

## 执行策略

| 步骤 | 执行者 | 可并行 |
|------|--------|--------|
| Step 1 | 主线程 | — |
| Step 2 | 子 agent | ✅ |
| Step 3 | 子 agent | ✅ |
| Step 4 | 子 agent | ✅ |
| Step 5 | 子 agent | ✅ |
| Step 6 | 子 agent | ✅ |
| Step 7 | 主线程 | 依赖 Step 3 |
| Step 8 | 主线程 | 依赖全部 |

并行限制：一次最多 3 个子 agent。推荐批次：Step 2+3+4 并行 → Step 5+6 并行 → Step 7 → Step 8。

---

## 质量门槛

- [ ] 每个文件 5-25 KB
- [ ] 总计 50-100 KB
- [ ] 每个文件可独立阅读
- [ ] 关键论点均有来源标注（文件名 + 决策编号/行号）
- [ ] 关键数字均用表格呈现
- [ ] 公式均用 LaTeX
- [ ] 文献均含 DOI 或 arXiv ID
- [ ] 无未标注的数据矛盾
- [ ] 04_literature.md 包含适配性分析汇总（适配点/不适配点/改进方向）
- [ ] 05_limitations.md 包含 Execute 阶段积累的局限性记录
