# Step 071 — CSSC-CPE 与 universal CS-DC B2 全文获取/精读

> 2026-08-09 | T025 | action=`FULLTEXT_READ` | CP009 / epoch 9
> Terminal: `B2_PAIR_UNRESOLVED_FULLTEXT`

## 1. Validator、范围与框架

Fresh task-control validator：`PASS`。本轮读取 `gw-acquire.md`、`gw-read.md`、`gw-supplement.md`、通信领域 baseline/信道/指标/反模式段、topic-index、D008、step-069，以及 RDL long-horizon/evidence/baseline 规则。只允许获取/精读两篇 B2；未修改中央 owner/治理/代码，未实验、提交或 push。

## 2. Acquisition / identity / 正文质量

| paper | channel 1 | channel 2 | channel 3 | identity | content gate |
|---|---|---|---|---|---|
| CSSC-CPE `10.1109/ACCESS.2019.2934224` | DOI/OA backend `all_failed` | search JSON IEEE PDF pointer `all_failed` | IEEE blit exact title：0 result | S2 + Crossref DOI identity consistent | PDF absent；`content.md` absent；0 行；title unverifiable |
| universal CS-DC `10.1364/OE.22.031167` | DOI/OA backend `all_failed` | search JSON DOI/OA pointer `all_failed` | Crossref Optica VOR resource 经 downloader `all_failed` | S2 + Crossref DOI identity consistent | PDF absent；`content.md` absent；0 行；title unverifiable |

`tools/download` bash wrapper 因 CRLF 解析失败，本轮使用 wrapper 指向的 canonical `tools/paper_download.py` 后端；没有修改工具。每篇均在三通道后停止，没有 web reader、publisher HTML 抓取或摘要拼接全文。

## 3. 全文状态与参数表

| paper | 正文状态 | 可全文冻结算法/参数 | 摘要级 locator（不等于冻结） | 必须 dev-tune / 全文核 |
|---|---|---|---|---|
| CSSC-CPE | `UNRESOLVED_FULLTEXT` | 无 | CPE-output cumulative averages；`δ` peak position/sign；QPSK weak turbulence | cumulative definitions、window、threshold、indexing、correction range、multi-slip、false action、latency/cost |
| universal CS-DC | `UNRESOLVED_FULLTEXT` | 无 | sliding average of twice estimated phase noise；minimum/threshold；reported residual `2×10^-7`；optional second window | statistic formula、two windows、thresholds、primary/secondary correction、fallback、failure/cost |

摘要值 `2×10^-7` 是作者仿真结果，不能冒充自然 coherent-FSO slip-rate 分布。两篇都没有可合法写入 Step 4a 的全文来源数值参数。

## 4. 八字段与 B2 implementability

### CSSC-CPE

| input | trigger | localization | action | decoder | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| 全文未决；摘要指 CPE output | 全文未决；摘要指 `δ` peak/threshold | 全文未决；摘要指 peak position/sign | 全文未决；correction span 不明 | 摘要称 non-data-aided | 未说明 | 未冻结 | 全文未决 |

### universal CS-DC

| input | trigger | localization | action | decoder | fallback | budget | output |
|---|---|---|---|---|---|---|---|
| 全文未决；摘要指 estimated phase noise | 全文未决；摘要指 sliding minimum/threshold | 精确粒度未决 | primary/secondary span 未决 | 摘要称 non-data-aided | 未说明 | one/two sliding stages，精确成本未决 | 全文未决 |

两篇共同裁决：

```text
B2_identity            = PROVISIONAL_ONLY
B2_implementability    = BLOCKED_FULLTEXT
algorithm_freeze       = NO
parameter_freeze       = NO
effort_estimate        = UNESTIMABLE_WITHOUT_METHOD_TEXT
```

## 5. Q1 collision

不能判吸收 Q1。摘要最多显示 receiver-only CPE metric 可定位/校正 slip；没有正文证明 decoder-evidence trigger、decoder re-evaluation、clean abstain/fallback 与相当预算，更不能证明八字段 exact match。反过来，全文不可得也不能作为“无碰撞”证据。

```text
CSSC_collision      = UNRESOLVED_FULLTEXT
universal_collision = UNRESOLVED_FULLTEXT
Q1_absorbed         = NOT_ADJUDICATED
exact_chain_closed  = false
```

## 6. Step 4a usable / not usable

可用（仅作为摘要级设计约束）：receiver-only CPE-output statistics 是合法 B2 信息类；QPSK/weak-turbulence 是 CSSC 的场景标签；universal 论文声称 modulation/CPE independence；第二 sliding stage 是 obvious cheap extension 候选。

不可直接使用：window、threshold、formula、correction angle/range、slip law/rate/burst、SNR/linewidth/turbulence 数值、多 slip spacing、false-alarm/abstain、运算量、buffer、latency。任何实现都必须先取得正文，或明确作为独立预注册 dev-tuned comparator，而不能标成论文复现。

## 7. 指定产出与保护

- `papers/_read_notes/10.1109_access.2019.2934224.md`
- `papers/_read_notes/10.1364_oe.22.031167.md`
- `projects/thesis-fso/worker-logs/step-071-c1-cssc-universal-b2-fulltext.md`

下载后端另在 canonical DOI 目录留下 `failed/all_failed` metadata，并有一份 Crossref VOR search receipt；它们不构成全文。未 stage/commit/push，未运行实验。

## 8. 终态

`B2_PAIR_UNRESOLVED_FULLTEXT`

- CSSC-CPE：`UNRESOLVED_FULLTEXT`
- universal CS-DC：`UNRESOLVED_FULLTEXT`
- provisional B2 冻结建议：保留 CSSC-CPE 为**身份级 provisional strongest B2**，不得冻结算法/参数；universal CS-DC 为 obvious receiver-only extension
- 是否吸收 Q1：`NOT_ADJUDICATED`（不得写成 yes/no）
