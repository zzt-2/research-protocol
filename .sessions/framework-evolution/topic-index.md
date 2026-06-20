# Topic Index: 框架演进与问题追踪

> 状态: active（2026-06-20 重新激活，LOG-001 框架根本缺陷发现） | 创建: 2026-05-15 | 最后更新: 2026-06-20

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

## 未决项

- **LOG-001 三改造待执行**（优先级 A→B→C）：
  - 改造 1：新建 glossary.md 定义问题 + contract.md L86-88 重写 + FR-23 展开 + gw-search/gw-read 问题提取段
  - 改造 2：GW Step 3 产出"问题清单"段 + Contract Step 1 引用机制
  - 改造 3：master-state-template.md 加 GW Progress 段 + groundwork.md 跨 Step 门控声明 + thesis-fso 补建 master-state.md
- **改造执行专题归属**：是本专题内做，还是开独立改造专题（如 2026-06-21-framework-glossary-rework），待定

## 当前位置

LOG-001 诊断 + 改造方案已完成。下一动作：按 A→B→C 顺序执行改造 1（最根本，先动 glossary.md + contract.md）。改造前需 grep 确认 contract.md L86-88 无其他文件依赖。
