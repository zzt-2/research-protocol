# Task Brief: RML-FSTS Step 4a 公式与方法身份审计

> 来源: S004 | 产出位置: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`
> 日期: 2026-08-09
> 唯一文档: 执行方先读本 T，再读取本 T 明列的本地论文/笔记；不得读取其他 session 历史推断任务

---

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。共享论文库在 `D:/code/study/research-protocol/papers/`，不在 worktree 内。
**你的任务**：fresh-context 核对 Wang 2023/Enhanced 2024 的 FSTS fixed-lag/`B_L` 方法身份、精确公式、参数与可复现最小动作空间，为 Step 4a semantic smoke 提供 source-grounded identity。
**产出**：只写 `projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`，返回状态与该路径；不改代码、治理 owner、论文正文或其他文件。

**最高纪律（违反一条即无效）**：
1. 核心公式须从共享 canonical PDF/源文件核对，标页码+公式号；`content.md` 的 picture omitted 不可凭文字补公式。
2. 区分 frame-sync correlation 与 fine CFO estimator；不得把现有 `frame_sync_fsts.py` 的模板相关冒充 Wang fine FOE。
3. 只报告 FACT/INFERENCE/UNKNOWN，不设计 controller、不下 Go/Kill、不声称 novelty。
4. 明确 `B_L`/lag 的含义、可扫集合、PM-4/16QAM 的论文默认值、320-symbol TS 结构和 CFO-MSE/outage 可计算口径。
5. 总耗时不超过 15 分钟；遇到 PDF 公式不可辨认，记录具体 blocker，不自行重建。

## 1. 背景（了解即可，不要在产出中对照评价）

Q1：M=Wang/Enhanced fixed-lag/fixed-`B_L` FSTS；C=PM-4/16QAM、320-symbol FSTS、receiver power/SNR、弱/强湍流；A=固定 lag/`B_L` 的最优值或排序可能随 receiver-visible condition 改变，产生 normalized CFO-MSE/outage regret。Step 3.5 只给 provisional survivor，不是 Go/METHOD_SIGNAL。

共享 canonical：
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/source.pdf`
- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`
- `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/source.pdf`
- `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/content.md`
- 既有结构化 owner：`projects/thesis-fso/literature_notes_rml_fsts.md`
- 既有 read notes：在共享 `papers/_read_notes/` 中按 DOI/title 检索。

## 2. 任务详情

### 2.1 必答问题

1. Wang/Enhanced 的方法身份：训练序列结构、FS/coarse FOE/fine FOE 的调用顺序与各自输入输出。
2. fine FOE 的精确式：每个 lag/`B_L` 的 correlation、phase/angle、range/variance tradeoff；公式号、页码、符号定义。
3. `B_N`/`B_L`/总 TS 长度关系；PM-4/16QAM、320 symbols 的论文 default 参数与可合法 sweep action set。
4. 信道/损伤/重复次数/功率、湍流、CFO、linewidth 等承重参数及原文数值与行/页证据。
5. 是否能只用 receiver samples + known TS 运行 fixed action；哪些 truth 只允许 scoring/oracle。
6. 现有 worktree `projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py` 与原方法的 identity gap，逐项给 file:line。
7. 最小 faithful semantic smoke 要实现什么；哪些内容可以安全简化，哪些不能。

### 2.2 执行方式

- 完整阅读两篇论文与必要 read-note；核心公式优先 PDF。
- 用 `rg -n`/行号或 PDF 页码建立证据指针。
- 检查现有 `frame_sync_fsts.py`，但不修改。
- 输出前自查：每个公式、参数、身份断言都有证据；无法确认标 UNKNOWN。

### 2.3 产出格式（强制）

```markdown
# RML-FSTS formula/identity audit
## Status
PASS / PARTIAL / BLOCKED
## Method identity
## Exact formulas
| component | equation | page/eq | symbols | implementation implication |
## Parameter provenance
| parameter | value/range | source pointer | role |
## Legal action space
## Deployable information boundary
## Existing-code identity gap
| requirement | existing file:line | gap | consequence |
## Minimum faithful smoke
## FACT / INFERENCE / UNKNOWN
## Blockers
```

## 3. 已知陷阱

- Wang `B_L` 既影响 fine range 又影响 phase-noise suppression；不能只把它当数组 lag 名。
- 320-symbol 关系可能因 PDF 转换符号丢失；不可凭 `BN×BL` 猜。
- `frame_sync_fsts.py` 顶部已自称单极化简化；不能据其可运行性宣称 testbed ready。
- 共享 papers 路径与 worktree 相对路径不同；路径缺失不等于全文缺失。

## 4. 验收

- [ ] 两篇论文 identity 与公式都有 source pointer
- [ ] 明确合法 action set 与 320-symbol约束
- [ ] 明确 truth/deployable 边界
- [ ] 对现有代码给出可核查 identity gap
- [ ] 没有设计 controller/Go/Kill/novelty 声称

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`
