# Task Brief: C1 Step 3.5 convergence round 3（final cap）

> 来源: S001 / D008 / T032–T033 | 产出位置: `projects/thesis-fso/worker-logs/step-080-c1-step3_5-convergence-round3.md`
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

执行 Step 3.5 第 3 轮、也是框架允许的最后一轮收敛检索。查询只使用 T033 全文确认的真实术语，检查是否仍有新增 `MUST_FULLTEXT/SHOULD_FULLTEXT`。不得把同一论文版本、会议→期刊/书章扩展、或只做全序列联合译码/容错编码的已知家族重复计为新增。

## 1. 纪律

1. 先读 `stages/gw-supplement.md`、`tools-guide.md` §1–2、topic-index、D008、step-067/068/078/079 及 T031 race note；fresh validator PASS 后执行。
2. 使用项目检索工具/结构化 API，设置 `PYTHONDONTWRITEBYTECODE=1`；所有 JSON 只写 `search-archive/2026-08-09/`。有效来源必须 ≥2；S2/OpenAlex 若 429/timeout，保留 receipt 后用 Crossref + arXiv，不死等。
3. 只做 search/abstract crosscheck；不下载全文、不改中央 owner/治理/代码、不实验、不提交/push、不触碰四个 p05 日志；15 分钟内收口。
4. 功能断言必须由 DOI/arXiv/S2 abstract 支持；无摘要或摘要不支持时标 `UNKNOWN/AI推断，未验证`，不得靠标题裁 exact collision。

## 2. Final-round 精确查询

至少执行以下 8 组；允许按源语法收缩，但须保留机制交叉项：

1. `"Gilbert-Elliott" "bursty differential phase noise" LDPC local repair`
2. `"windowed BCJR" "channel-state estimation" LDPC phase boundary`
3. `"burst-aware" LDPC "channel estimation" segment reprocessing`
4. `"decoder LLR" "channel-state posterior" cycle slip localization`
5. `"hybrid turbo differential decoding" cycle slip localization repair`
6. `"differential encoding aware" soft-decision FEC cycle slip correction`
7. `syndrome parity-check cycle-slip boundary suffix re-decode`
8. `decoder-aided phase-slip change-point bounded local phase hypotheses`

若实际 source query 不支持引号，记录 exact submitted string。不得用泛化的 `phase noise LDPC` 单独扩池。

## 3. Known-family 去重与八字段筛选

- 按 `DOI > arXiv > normalized title/alias` 与 integrated corpus、round1/round2、现有 read notes 去重。
- 明确合并：OFC15 TH3E.6→2016 book chapter→arXiv1704；ECOC14→JLT15；PAPU 2013/2014/2019；TVT2309/2025；Tikhonov 1204/1306；T033 两篇及其版本。
- 对真正新候选逐条筛：receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output。
- `MUST` 仅限摘要支持可能同时命中 explicit local boundary、bounded local carrier action、decoder re-evaluation；`SHOULD` 仅限与该链直接相邻且身份确新的方法。只做 burst model、whole-sequence BCJR/LDPC、slip-tolerant code/differential decoding，不计 actionable new。

## 4. 终态与产出

- 新增 MUST/SHOULD=0：`ROUND3_CONVERGED_ZERO_NEW`。
- 非 0：`ROUND3_CAP_REACHED_WITH_NEW`，列完整身份、摘要指针、字段命中/未知、是否需全文；不得自行超出 3 轮。按用户既有授权只记录覆盖限制，是否足以阻断交由主线程完整链裁决。

产出：

- `search-archive/2026-08-09/coded-decoder-c1-step3_5-convergence-r3-*.json`
- `projects/thesis-fso/worker-logs/step-080-c1-step3_5-convergence-round3.md`

worker log 必含：8 组 query/source receipt、raw/unique/known/new、真正新候选（≤10）八字段、MUST/SHOULD 数、三轮累计收敛判断、coverage limitations、p05 4/4 hash 与 staging-empty 检查。聊天只回 terminal、计数、最强新增（若有）、路径；≤650 字。
