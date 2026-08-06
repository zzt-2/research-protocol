# Step 3.5 new competitor acquire→read

> 日期：2026-08-06
> 任务：T008
> 范围：三篇新竞品的有界合法获取与全文 action-contract 裁决；不改 canonical 状态，不进入 Step 4a，不实现、不仿真、不提交。

## Acquisition receipts

三条路径上限按“最多三条适用且合法的独立路径”执行。dry-run 不计 acquisition path；`tools/blit` 不支持 Optica，故 P2/P3 第三路径只做 source-contract 适用性门，不伪装成 IEEE 请求。

| DOI | attempts | source/content | title | SHA | lines | verdict |
|---|---|---|---|---|---:|---|
| `10.1109/JLT.2025.3528909` | preflight DOI dry-run PASS；1 DOI downloader=`all_failed`；2 official arXiv exact-title 命中 `2410.10080v1`，arXiv dry-run 后 `arxiv_html` 成功 | `papers/arxiv/2410.10080v1/source.html` + `content.md` | 人工 H1 exact match，overlap `1.0`；自动 metadata=`unverifiable` | source `44f954fd67a7dae69e641cbde91f9d73fc382ab10c4d7d51236efe5f3af49593`；content `a767b560ec27750edbb1f52412a92004ce72ae1ca153fba6bbb9bb2f89c3ffe5` | 555 | `ACQUIRED_FULLTEXT_PASS` |
| `10.1364/OE.566136` | preflight DOI dry-run PASS；1 DOI downloader=`all_failed`；2 official arXiv exact-title=0；3 `blit` Optica applicability=`NOT_APPLICABLE_NOT_RUN` | DOI 目录仅失败 `metadata.json`，无 source/content | identity 仅沿用 T006 OpenAlex citation receipt；无全文 title gate | metadata `fea86425d70c45236338f67089ef3d3a3209e494b4dbea8983e008668d89b275`；arXiv receipt `892454a9a986821a90c2661153dee666efdd968848ab31f1a5915356d792973f` | N/A | `FULLTEXT_UNAVAILABLE_STOPPED` |
| `10.1364/JOCN.402591` | preflight DOI dry-run PASS；1 DOI downloader=`all_failed`；2 official arXiv exact-title=0；3 `blit` Optica applicability=`NOT_APPLICABLE_NOT_RUN` | DOI 目录仅失败 `metadata.json`，无 source/content | identity 由 T006 OpenAlex + Sun local reference receipt 支持；无全文 title gate | metadata `3a342b7257d061e77f53a2bde8fb951e905934ba77f49e7bb9bdef704e4376d6`；arXiv receipt `38ee5c0304d7d726ad56f317ca3b93e3f74b6abbe21ffaa7db24115613d99362` | N/A | `FULLTEXT_UNAVAILABLE_STOPPED` |

补充 receipt：P1 DOI-failure metadata SHA256 `cf4ea567900422f5d2d2824429a04d7bf023057eeb94cedfcf3d66775214cf71`；P1 arXiv exact-title receipt SHA256 `90411543888e0ce5e7cc6101a593d7cb8de27690647c7e55251da7dd5a3a3b8e`。三篇均未访问 ResearchGate/Google Scholar/publisher paywall，未绕过访问控制。

## Paper 1 action contract — Zhou et al., JLT 2025

| information | action/output | timing/order | joint objective? | Q1 collision | evidence lines |
|---|---|---|---|---|---|
| Preamble A two tones（X=`R_s/2`、Y=`R_s/4`） | sliding-window burst arrival + coarse CFO | pipeline 首步 | 否；tone search 与 CFO center-frequency calculation 是相邻独立动作 | 占用 compact preamble 的 coarse detect/CFO integration | `content.md:91-114` |
| Preamble A tones after SOP recovery | one-tap SOP；feed-forward SPO initial phase；fine CFO | SOP→MF/CDC→SPO/fine-FOE | 否；SPO=Eq. (5/6)，CFO=Eq. (8)，不同 metric/output | **直接占用 preamble-aided fractional-SPO initialization**，显著加强顺序 comparator | `content.md:119-197` |
| Preamble B three 64-symbol CAZAC blocks | frame position from timing peak | 在 Preamble-A timing/frequency处理之后 | 否；Eq. (9-11) 独立 correlation metric | 占用 short-CAZAC frame synchronization | `content.md:207-228` |
| Preamble B known/received spectra | MMSE/ZF MIMO tap initialization | frame sync 后接 CE/equalizer | 只有 CE 自身的 `J_X/J_Y` MSE；不含 SPO/CFO/frame | 与 Q1 exact action 无直接碰撞，但占用 integrated burst-DSP packaging | `content.md:233-349` |

**全文 action verdict**：`SEQUENTIAL_MODULAR_ESTIMATION_WITH_PARTITIONED_PREAMBLE_REUSE`。正文明确先后执行多个模块；不存在 single objective/metric 同时搜索并输出 `(frame index, fractional timing tau, CFO)`。Preamble A/B 同属一个约 10 ns designed preamble 是资源级集成，不是 estimator-level jointness。

**对 Q1 的约束**：该文比 Sun 2025 更直接，已经把 SPO、frame synchronization、CFO 放在同一 Co-BM-DSP 总链，并用 preamble-A SPO 初始化 Godard timing recovery。Q1 不得再声称“首次用一个 preamble 支持 timing/frame/CFO”“首次快速初始化 timing recovery”或仅凭框图合并称 joint；最低合法 comparator 应升级为本论文的完整 sequential chain（或等价实现）+ polyphase/Farrow 扫描/插值。剩余 exact delta 仅能是同一 objective/搜索空间耦合 `(frame,tau,CFO)`，并需后续证据证明其必要性与收益。

## Paper 2 action contract — Jin et al., OE 2025

| information | action/output | timing/order | joint objective? | Q1 collision | evidence lines |
|---|---|---|---|---|---|
| 摘要筛查仅列 polarization-independent preamble | FS/FOE/CE（摘要级） | **UNRESOLVED** | **UNRESOLVED_FULLTEXT_UNAVAILABLE** | 不得据摘要判定是否遗漏 timing action；exact collision 未闭合 | 无全文；只见 T006 citation receipt |

**exact-action verdict**：`UNRESOLVED_FULLTEXT_UNAVAILABLE`。摘要只能标作 generic multi-action preamble screen，不能分类为 sequential 或 true joint。

## Paper 3 action contract — Zhang et al., JOCN 2021

| information | action/output | timing/order | joint objective? | Q1 collision | evidence lines |
|---|---|---|---|---|---|
| 摘要/引用筛查仅表明早期 designed preamble | FS/SOP/FOE（摘要级） | **UNRESOLVED** | **UNRESOLVED_FULLTEXT_UNAVAILABLE** | 可作早期 multi-action preamble lineage；不得裁 timing boundary/exact jointness | 无全文；identity 见 Sun `content.md:536` 与 T006 citation receipt |

**exact-action verdict**：`UNRESOLVED_FULLTEXT_UNAVAILABLE`。不能把多动作列表升级为 coupled estimator。

## Generic reuse vs sequential vs true joint

| class | 判据 | 本批论文 |
|---|---|---|
| generic/shared preamble reuse | 多动作读取同一总 training resource，但不同字段/子段/metric | P1 明确有资源复用；P2/P3 仅摘要筛查候选，不能全文裁决 |
| sequential modular estimation | 前一模块输出/补偿后，后一模块再估计；各自 objective/output 可分离 | **P1 PASS**：burst detect/coarse CFO→SOP→SPO/Godard + fine CFO→frame sync→CE |
| true joint estimator | 单一 objective/metric/search 同时输出 frame、fractional timing、CFO | **本批全文证据 0 篇**；P1 明确否，P2/P3 unresolved |

## Global read notes / read-log updates

- 全局 read note：`papers/_read_notes/2410.10080v1.md`
- 项目 read-log：`projects/thesis-fso/read-log.md` 已追加 `2410.10080v1`，alt ID=`10.1109/JLT.2025.3528909`
- P2/P3 未取得全文，不创建伪 read note、不追加 read-log。

## Coverage gaps

- `10.1364/OE.566136`：两条适用获取路径失败，Optica 不在 blit source contract；timing action、处理顺序与 joint objective 全部未决。
- `10.1364/JOCN.402591`：同上；只能维持 early multi-action preamble lineage，不能作 exact-action裁决。
- T006 已止损的 JOCN 2026 `10.1364/JOCN.587273` 本轮未重复获取；其 `UNRESOLVED_HIGH_RISK` blocker 不因 P1 精读而自动消失。

## Conclusion and claim ceiling

1. P1 全文把最强廉价 comparator 从“独立 timing + frame/FOE chain”具体化为一个 2025 integrated preamble-driven sequential pipeline；这是 Q1 comparator collision，必须吸收。
2. P1 不是 true joint `(frame,tau,CFO)` estimator：SPO、CFO、frame 分别使用独立公式/metric，并按模块顺序处理。
3. 本批没有全文证据证明 exact joint action 已被占用；但 P2/P3 和既有 JOCN 2026 仍是 coverage gaps。因此 claim ceiling 只能到：**P1 exact action 已裁为 sequential；全局 exact-action novelty/collision 尚未闭合**。
4. 未修改 canonical decisions/topic/master/literature notes，未进入 Step 4a、实现、testbed、MVE 或仿真，未提交。
