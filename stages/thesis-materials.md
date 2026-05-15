# 学位论文材料准备指南

> 框架产出如何映射到论文章节。写作不在框架范围内，但写作所需材料应在研究过程中积累。
> 与 `templates.md` 配合使用：本文件定义"需要什么、何时积累"，模板定义"怎么记"。

---

## 1. 多子问题组织方式

专硕论文通常有 2-3 个技术章节，每章解决一个子问题。框架默认按单 research question 设计，按以下方式适配：

### 组织原则

- **共享 Groundwork**：所有子问题共享一个 `literature_notes.md`（按子方向分节）
- **独立 Contract**：每个子问题独立 Contract（hypothesis、method、experiments）
- **独立 Execute**：每个子问题独立实验和结果

### 目录结构

```
projects/{name}/
├── literature_notes.md          # 共享，按子方向分节
├── feasibility_report.md        # 共享，每个子方向独立一节
├── baseline_report.md           # 共享
├── decision_log.md              # 共享
├── contract-ch1.md              # 子问题 1
├── contract-ch2.md              # 子问题 2
├── contract-ch3.md              # 子问题 3
├── data-flow-ch1.md
├── data-flow-ch2.md
├── data-flow-ch3.md
├── results-ch1/
├── results-ch2/
├── results-ch3/
└── paper_materials/             # 论文写作材料包
    ├── 00_workflow.md           # 提取工作流（通用版见框架模板）
    ├── 01_research_context.md   # 研究问题、动机、研究空白
    ├── 02_method.md             # 方法架构、公式、设计决策
    ├── 03_experiments.md        # 实验设置、全部结果数据、消融
    ├── 04_literature.md         # 相关工作分类、竞品对比、文献索引
    ├── 05_limitations.md        # 局限性与未来方向（EX 阶段积累）
    └── 06_formulas_symbols.md   # 公式汇总与符号约定
```

子问题之间如有依赖（如 Ch1 输出是 Ch2 输入），在对应 Contract 中声明。

### 执行节奏

```
Groundwork（共享）
  → Contract Ch1 → Execute Ch1
  → Contract Ch2 → Execute Ch2
  → Contract Ch3 → Execute Ch3
```

---

## 2. 材料包清单

以下清单映射框架各阶段产出到论文各章节。

`[MUST]` = 研究过程中必须积累，不可事后补记
`[POST]` = 写作阶段从已有材料提取即可

### 绪论

| 论文章节 | 框架产出 | 积累阶段 | 类型 |
|---------|---------|---------|------|
| 1.1 研究背景与意义 | literature_notes §研究背景概述 | GW Step 3 | MUST |
| 1.2 国内外研究现状 | literature_notes §综合分析（按子方向重组） | GW | POST |
| 1.3 研究内容与安排 | contract(s) 的 hypothesis + 章节安排 | CT 冻结后 | POST |

### 各技术章节（第 2-N 章）

| 论文章节 | 框架产出 | 积累阶段 | 类型 |
|---------|---------|---------|------|
| X.1 引言 | competitor_notes + feasibility_report §gap | GW | POST |
| X.2 基础理论 | literature_notes 结构化提取 | GW | POST（需补数学推导） |
| X.2.x 适配性与局限性 | literature_notes 每篇 §适配性分析 | GW 精读时 | MUST |
| X.3-X.4 核心方法 | data-flow.md + contract.md | CT | POST（需补数学推导） |
| X.5 实验方案 | contract §Simulation Config + 数据集设计 | CT 冻结时 | MUST |
| X.6 实验结果 | results/*.md + 可视化图表 | EX | MUST |

### 结论

| 论文章节 | 框架产出 | 积累阶段 | 类型 |
|---------|---------|---------|------|
| N.1 全文总结 | 各 contract hypothesis + results | EX 结束后 | POST |
| N.2 工作展望 | paper_materials/05_limitations.md | EX 过程中 | MUST |

### 写作补充材料

| 材料 | 用途 | 来源 | 类型 |
|------|------|------|------|
| 各模块数学推导 | 方法章节的理论推导 | data-flow + 自行补充 | POST（写作时） |
| 可视化论证图表 | 消融实验的直观证据 | Execute 消融实验 | MUST |
| 案例分析图 | 正例/负例对比 | Execute 实验中 | MUST（如适用） |

### 引用质量要求（学位论文 [MUST]，期刊论文 [SHOULD]）

学位论文参考文献需满足以下质量标准。这些检查应在 GW 文献收集阶段和素材提取阶段分别执行。

**语言多样性**：
- 中文学术期刊引用 ≥ 10 篇（通信领域典型中文源：通信学报、电子学报、宇航学报、电子与信息学报）
- 纯学位论文引用不计入中文期刊数量（学位论文 vs 期刊论文是不同类型）
- 检索工具：`tools/search --doc-types chinese_journal`、`tools/blit --source wanfang`、`tools/blit --source cbpt --journal {期刊代码}`
- 检索时机：GW Step 1（检索阶段）就应包含中文源，不应留到素材提取时才补

**预印本率控制**：
- 核心引用（直接对比和基线相关）预印本率 ≤ 30%
- 全部引用预印本率 ≤ 40%
- 预印本已被正式接收但尚未见刊的，按正式发表计数（需有 DOI 或 venue 信息）
- 预印本状态验证流程见 `gw-read.md` §预印本发表状态验证

**引用目标 vs 下载来源**：
- 文献的"发表渠道"字段记录的是**引用目标**（读者应 cite 的 venue），不是下载来源
- 即使只下到 arXiv PDF，若已确认被 IEEE 接收，引用信息仍标 IEEE
- 仅无正式版本的纯预印本才标 "arXiv preprint"

---

## 3. 中间过程记录钩子

以下材料在对应阶段有强制记录点，确保写作时不需从零重组。

### Groundwork：研究背景概述 + 适配性分析

**研究背景概述**：精读完成后，在 `literature_notes.md` 综合分析末尾新增一节：
- 领域发展脉络（时间线：关键节点和标志性工作）
- 核心技术挑战（从精读论文的 motivation 提取）
- 本研究的定位（一句话）
- 多子问题时，按子方向分别概述

**适配性分析**：每篇精读论文新增结构化提取（模板见 `templates.md`）。

### Contract：数据集设计

自建数据集时，Contract 中必须包含"数据集设计"节（模板见 `templates.md`）。

### Execute：局限性与可视化论证

**局限性记录**：Execute 过程中发现以下情况时，追加到 `paper_materials/05_limitations.md`：
- 未覆盖的场景或条件
- 方法假设的适用边界
- 性能退化的触发条件
- 消融实验揭示的模块依赖

**可视化论证**：消融实验除定量结果外，准备可解释性图表：
- 特征重要性图 / 注意力热力图 / 决策边界图 / 案例分析图
- 路径记录在 experiment_result 的"可视化"字段

---

## 4. 材料包提取流程

Execute 完成后（或写作前），从项目原始材料中提取结构化素材到 `projects/{name}/paper_materials/`。提取流程详见 `stages/paper-materials-workflow.md`（通用版模板）。

核心思路：将 GW/CT/EX 的碎片化产出（literature_notes、contract、decision_log、results 等）重组为论文写作可直接消费的 6 个结构化文件（01-06），每个文件独立可检索。

**与中间过程记录的关系**：
- 中间过程记录（GW 的适配性分析、EX 的局限性记录）→ 写入项目原始文档（literature_notes、05_limitations）
- 材料包提取（00_workflow）→ 从原始文档中**二次提取**到 01-06 文件，按论文章节重组
- 两者不冲突：中间记录保证不丢信息，提取流程保证写作时方便消费

---

## 5. 与现有框架文件的修改点

本指南涉及对以下文件的最小化补充：

| 文件 | 补充内容 | 章节 |
|------|---------|------|
| `templates.md` | literature_notes 增加"适配性分析"字段 | §literature_notes |
| `templates.md` | contract 增加"数据集设计"节 | §contract |
| `templates.md` | experiment_result 扩展"可视化"字段 | §experiment_result |
| `stages/gw-read.md` | 结构化提取增加第 6 项"适配性分析" | §结构化提取 |
| `stages/groundwork.md` | 完成条件增加"研究背景概述" | §完成条件 |
| `stages/contract.md` | Step 2 增加"数据集设计"要求 | §Step 2 |
| `stages/execute.md` | Step 4 增加可视化论证、Step 5 增加局限性记录 | §Step 4, 5 |
| `overview.md` | 文档系统引用本文件 | §文档系统 |
