# Topic Index: 框架演进与问题追踪

> 状态: active（2026-06-20 重新激活，LOG-001 框架根本缺陷发现） | 创建: 2026-05-15 | 最后更新: 2026-07-17（R002 设计草案及旧日志闭环审查）

## 专题信息

- **slug**: framework-evolution
- **title**: 框架演进与问题追踪
- **性质**: 跨项目长期专题（不按日期另开）

## 范围边界

- **原始目标**：框架规则改进、流程问题日志
- **当前范围**：追踪研究协议框架（stages/ + AGENTS.md + templates）的缺陷，记录改造方案，监督执行
- **明确不含**：
  - 不直接改框架文件（改文件在各项目专题或独立改造专题做，本专题只诊断+记录方案）
  - 不管具体项目的研究内容（那是各项目专题的事）
- **范围变更记录**：
  - 2026-05-18：首次关闭（20+ issues 处理完）
  - 2026-06-20：重新激活。thesis-fso 5 次殊途同归 + agent 连犯 3 错暴露框架根本缺陷（未定义"问题/方法/空白"概念），LOG-001 新建

## 不变量

- **框架文件职责边界**：每条内容只有一个拥有者文件，其他只引用（AGENTS.md 已定，本专题监督执行）
- **glossary.md 将是术语唯一拥有者**（LOG-001 改造 1 待执行）

## 已确认结论

### 不变量
- 框架缺陷的诊断必须基于证据（grep + Read 原文），不能凭记忆（TL-31）
- 改造方案必须"先改根因（A 概念层）再改 B（流程）最后 C（状态）"，不能倒序

### 其他结论
- 框架当前把"空白"当 Contract 假设来源（contract.md L86-88）是制度性缺陷，5 次失败是照框架执行的结果
- "问题"四判据（具体矛盾 + 有方法产出 + 有 baseline + 能对比）已定稿，待写入 glossary.md

## 进展线索

- **历史 issues**（2026-05-15 ~ 05-18，已 closed 时处理）：20+ P0/P1/P2 框架问题，详见 git 历史
- **LOG-001**（新建 2026-06-20）框架根本缺陷：未定义"问题/方法/空白"。三条证据链（contract.md L86-88 空白当假设来源 / 全文无问题定义 / master-state.md 缺失无跨 Step 门控）。三改造方案（glossary.md 定义问题 + GW 问题清单产出 + master-state.md 强制化）。严重度 P0。详见 `LOG-001-problem-method-definition-gap.md`
- **R001**（新建 2026-06-21）外部方法论对照：Supervisor-Skills（港科广骆昱宇 repo）。**状态：待激活归档，不进本轮执行路径**。调研了它的 5 维框架 / 致命缺陷表 F1-F10 / idea-evaluator 工程化，技术判断比我们在 idea 质量评估工程化和找切入点操作层上成熟。但**本轮（批评汇总方法论首次验证）跑完前禁止借鉴**——"看到外部更成熟框架就搬"与 thesis-fso 的"看到空白就填"是同一根源（对自有方法没定力）的第二层变体。详见 `R001-external-methodology-comparison-supervisor-skills.md`
- **LOG-002**（新建 2026-07-10，跨专题登记）search-archive 索引机制上线：`tools/litsearch/search_index.py` 增量索引 + `tools/backfill_index.py` 一次性回填。**根因**：`_auto_save` 只落盘 JSON 无索引层，3.6 万条目沉默躺 46 个日期目录——"扔那不看"制度性根因。**已实施**：回填 19166 篇唯一论文 → `search-archive/_index/all-papers.jsonl`（35MB），下次 `tools/search` 自动增量更新。**专题起步范式**：子 agent 从 JSONL 扫关键词 → 生成 `by-topic/{topic}-seed.md`（均衡层专题已用，117 篇 FSO×均衡种子）。**AGENTS.md 文件路径规则表**已加 3 行索引。改造落在均衡层专题 S003，所有专题受益
- **R002**（新建 2026-07-17，Direction Lab 设计草案）：用户确认将候选族批量探索提升为默认方向发现轨道；旧 GW 降级为 winner 之后按需调用的 Deep Evidence 模块。设计重点是唯一机器状态、evidence ledger、dead-end registry、Process Warden、抗膨胀目录和从零/从地基双入口。旧日志审查又补出 P0 状态源分裂、证据等级门控、provenance/stale 传播、discovery ledger、component registry、全景排序门和 salvage lineage；已形成五个核心 schema 冻结草案。详见 `R002-direction-lab-design.md`；未实施、待用户审阅

## 未决项

- **LOG-001 三改造待执行**（优先级 A→B→C）：
  - 改造 1：新建 glossary.md 定义问题 + contract.md L86-88 重写 + FR-23 展开 + gw-search/gw-read 问题提取段
  - 改造 2：GW Step 3 产出"问题清单"段 + Contract Step 1 引用机制
  - 改造 3：master-state-template.md 加 GW Progress 段 + groundwork.md 跨 Step 门控声明 + thesis-fso 补建 master-state.md
- **改造执行专题归属**：是本专题内做，还是开独立改造专题（如 2026-06-21-framework-glossary-rework），待定
- **R001 待激活借鉴**（**硬约束：批评汇总 `2026-06-20-problem-driven-redirection` 验证产出结果前不触发**）：激活后对照 R001 借鉴清单逐条 D### 决策（致命缺陷聚合表 / 5 维切入点生成器 / 能力×生命周期匹配 / Integrity gate inspection 分类 / 范式跃迁探针）

## 当前位置

当前主线为 R002 设计审阅：先补齐状态、证据、发现覆盖、代码契约和失效传播的 schema，再决定是否进入实现专题。旧 LOG-001 的 A→B→C 改造暂不与本轮混做。
