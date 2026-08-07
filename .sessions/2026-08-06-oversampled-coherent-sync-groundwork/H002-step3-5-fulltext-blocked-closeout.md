# Handoff: Q1 Step 3.5 收敛，等待 exact-action 全文覆盖决定

> **SUPERSEDED by H003 / D008**：JLT 2025 全文已取得并裁为非 exact collision；JOCN 由用户确认不可得。

> 来源: S001 | 交接目标: 补齐或显式接受两个 primary-fulltext 缺口后，再决定是否讨论 Step 4a
> 日期: 2026-08-06

## 到哪了（状态）

D006 已纠正 D005 把 Step 4a/MVE problem-truth 前移到 Step 3 的 semantic-gate 错误：Q1 四判据
PASS，Q2 仅判据 3 FAIL。D007 已完成 Step 3.5：Round 2 真正新增 must/should=0，Sun 2025 双向
引用链完成，3 篇新增全文完成 action-contract 精读。Q1 保留唯一 survivor，当前全文池无 confirmed
exact `(frame,fractional τ,CFO)` collision；terminal=
`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`。
V005 已由 fresh-context verifier 对照 canonical glossary 与 AMC D005 复验 PASS；专题据此关闭，
本文件取代 H001，成为唯一恢复入口。

## 下一步干什么

优先取得 JOCN 2026 `10.1364/JOCN.587273` 与 JLT 2025 IQ-skew `10.1109/JLT.2025.3581618` 全文，
并按 acquire→read 核验 information/action/output/timing；或者由用户显式接受这两个 coverage gaps。
只有该门处理后，另起会话重读 `stages/gw-feasibility.md`，才可讨论是否进入 Step 4a。

## 纪律

- 不把“当前全文池未确认 collision”写成“exact-action novelty 已闭合”；
- 不把 shared preamble、模块调序或 composite comparator 写成 true joint method/单篇 baseline；
- Q1 survivor 不是 METHOD_SIGNAL、Go 或论文方法成立；
- 不修改 `common/`、`params.py`、旧实验/Skill/四个 `p05_run*.log`，不自动实现或仿真。

## 失败数据附录

### Primary-fulltext blockers

- JOCN 2026：DOI downloader=`all_failed`；official arXiv exact-title=0；blit 无 Optica source contract；
  无 source/content，摘要不得裁 exact jointness。
- JLT 2025 IQ-skew：DOI/OA=`all_failed`；official arXiv exact-title=0；IEEE blit exact-title bounded timeout
  且无 PDF/content；无 read note，摘要不得裁 exact jointness。

### 已排除的 exact collision 误判

- Zhou 2025：分区 preamble 顺序模块链，不是单一三参数 objective；
- LPT 2017：joint integer frame+CFO，入口 1 sps，无 fractional τ/SCO；
- JLT 2021：joint integer τ+CFO+CPO，无 frame，OFDM/fiber task 不匹配。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 两篇 primary direct candidates 无全文 | exact-action novelty/collision 必须用全文 | `FULLTEXT_BLOCKED` | 用户提供合法全文、新 OA/preprint 入口，或显式接受 coverage gaps |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：D006 的 canonical 四判据重判 → 检查 glossary L22-31、AMC D005、formal D005/D006
  - 声称2：Round 2 真正新增 must/should=0 → 检查 T011 log 与 3 个 R2 JSON
  - 声称3：三篇新增全文均非 exact collision → 检查 T008–T010 logs、read notes 与 content evidence lines
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
