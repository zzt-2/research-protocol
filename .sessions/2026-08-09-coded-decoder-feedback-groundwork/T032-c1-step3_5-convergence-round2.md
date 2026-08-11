# Task Brief: C1 Step 3.5 convergence round 2

> 来源: S001 / D008 / step-067–076 | 产出位置: `projects/thesis-fso/worker-logs/step-078-c1-step3_5-convergence-round2.md`
> 日期: 2026-08-09

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: TARGETED_SUPPLEMENT_SEARCH
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

用 round-1 全文浮出的精确术语做 Step 3.5 round 2 收敛检索，目标是判断新增 `MUST_FULLTEXT/SHOULD_FULLTEXT` 是否为 0。不得重报 OFC 2014/2015、ECOC 2014、ICTON 2016、arXiv 1204/1306/1704、CSSC/CS-DC、PAPU、TVT/TWC/TSP 等已知家族为“新增”。

## 1. 纪律

1. 先读 gw-supplement、tools-guide §1–2、topic-index、D008、step-067–076 与相应 read notes；fresh validator PASS 后执行。
2. 使用短超时项目工具/API，设置 `PYTHONDONTWRITEBYTECODE=1`；JSON 只写 `search-archive/2026-08-09/`。S2/OpenAlex 若仍429，保留一次 receipt后直接用 Crossref+arXiv，不死等。
3. 只做 search/abstract crosscheck，不下载全文、不改中央/代码、不实验/提交/push/触碰 p05；15 分钟收口。

## 2. 八组新术语

至少执行下列 8 组，允许按 API 语法轻微收缩但不得丢机制：

1. `Markov cycle-slip state turbo demodulation LDPC boundary localization`
2. `phase-slip-aware differential BCJR SC-LDPC windowed local repair`
3. `block-symmetric LDPC phase-slip transparent segment correction`
4. `Tikhonov mixture slip confidence decoder change point recovery`
5. `pilot phase unwrapping cycle-slip PAPU FEC local correction`
6. `unsatisfied parity check syndrome cycle-slip localization`
7. `cumulative-average phase-slip boundary decoder reprocessing`
8. `decoder anomaly phase candidate suffix selective re-decode`

实际有效来源 ≥2；所有功能断言必须由 S2/DOI/arXiv abstract交叉验证，不支持标 `AI推断，未验证`。

## 3. 收敛裁决

- raw去重后与 round1/integrated corpus按 DOI/arXiv/title去重；列 ≤10 条真正新候选。
- 逐条八字段快速筛选；只有可能命中 explicit boundary + bounded local carrier action + decoder interaction 才标 MUST，明确的近邻方法才标 SHOULD。
- 若新增 MUST/SHOULD=0，terminal=`ROUND2_CONVERGED_ZERO_NEW`；若非0，给完整身份、abstract pointer、可能命中字段和下一全文优先级，不得靠摘要判 exact。

## 4. 产出

- JSON：`search-archive/2026-08-09/coded-decoder-c1-step3_5-convergence-r2-*.json`
- worker log：`projects/thesis-fso/worker-logs/step-078-c1-step3_5-convergence-round2.md`

worker log 含8-query/source receipts、raw/unique/known/new计数、≤10新候选八字段、MUST/SHOULD数、coverage limitations 与保护检查。

聊天只回 terminal、新增 MUST/SHOULD、最强新候选、计数和路径；≤650 字。
