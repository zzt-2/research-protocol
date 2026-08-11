# Step 067 — C1 Step 3.5 round-1 关键词矩阵

> 日期：2026-08-09  
> 任务：T021 / CP009  
> Terminal：`ROUND1_QUERY_MATRIX_COMPLETE`  
> 范围：仅 Groundwork Step 3.5 targeted supplement 的搜索、去重和 abstract-level 裁决；未获取/精读全文，未进入 Step 4a/adapter/实验。

## 1. Task-control 与恢复边界

| 检查项 | 结果 |
|---|---|
| schema / epoch / checkpoint | `rdl.task-control.v2 / 9 / CP009`，与 topic foreground control 一致 |
| action class | `TARGETED_SUPPLEMENT_SEARCH` 在 allowed actions 内 |
| validator | `PYTHONDONTWRITEBYTECODE=1 python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py .sessions\2026-08-09-coded-decoder-feedback-groundwork\T021-c1-step3_5-query-matrix.md` → `PASS` |
| 必读 | 已读 `stages/gw-supplement.md`、`tools-guide.md §1–2`、topic-index、D008、`literature_notes_coded_decoder_feedback.md` |
| recovery route | 本包不创造方法；它排除/发现完整链先行工作，是 Step 4a 前下一正向方法动作的强制门控；当前无 repeated repair/no-method streak，不转 factory/实验。 |
| forbidden boundary | 未改 central owner/治理/代码；未下载/精读全文；未运行实验；未 stage/commit/push；未进入 Step 3.5 之外步骤。 |

## 2. Query/command/source receipts

统一项目工具命令形态：

```text
PYTHONDONTWRITEBYTECODE=1 bash tools/search "<query>" --sources s2 openalex --max-per-source 8 --top 12 --sort relevance --output search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-qNN.json --format json
```

- project wrapper 的首批 S2+OpenAlex 聚合调用长时间不返回；按 15 分钟 stop rule 终止批等待。`q02.json` 留下 S2+OpenAlex `0` 结果 receipt。
- OpenAlex-only retry 在 34.1 秒 timeout；`q01.json` 留下 OpenAlex `0` 结果 receipt。之后未再对 wrapper 长等。
- direct Semantic Scholar Graph API fresh request → `HTTP 429`；direct OpenAlex Works API fresh request → `HTTP 429`。两项失败均保留在 raw JSON source receipts，未把 429 写成“检索无结果”。
- 合法 fallback：Crossref Works API（官方 DOI metadata/search）+ arXiv export API（官方 preprint metadata/abstract），均采用短超时批量执行；功能断言再用本地已落盘 fresh S2 abstract receipt 或官方 arXiv abstract 交叉验证。

### 2.1 九查询矩阵

| ID | 方法变体 | scenario/locality | query | Crossref | arXiv |
|---|---|---|---|---:|---:|
| q01 | decoder/code-aided detect-localize | coherent optical + boundary | `decoder code aided cycle slip boundary localization coherent optical` | 6 | 1 |
| q02 | decoder/code-aided detect-localize | change point + local segment + coded QAM | `decoder aided phase slip change point local segment coded QAM` | 6 | 2 |
| q03 | decoder/code-aided detect-localize | free-space optical / FSO | `code aided cycle slip detection free space optical FSO` | 6 | 5 |
| q04 | LDPC/syndrome phase-slip correction | coherent optical | `LDPC syndrome assisted phase slip correction coherent optical` | 6 | 3 |
| q05 | FEC/CRC ambiguity correction | cycle-slip boundary | `FEC CRC phase ambiguity correction cycle slip boundary` | 6 | 0 |
| q06 | syndrome/decoder ambiguity correction | local repair + suffix redecoding | `syndrome decoder phase ambiguity local repair suffix redecoding` | 0 | 5 |
| q07 | segment/suffix bounded repair | local reprocessing + decoder re-evaluation | `cycle slip local segment suffix reprocessing decoder re-evaluation` | 6 | 0 |
| q08 | segment/suffix bounded repair | bounded local redecoding + coherent optical | `bounded phase slip repair local redecoding coherent optical` | 6 | 5 |
| q09 | piecewise phase-state candidate repair | change point + coded PSK | `piecewise phase ambiguity change point decoder candidate repair coded PSK` | 6 | 1 |

矩阵满足：3 个机制变体，每个交叉至少 2 类 scenario/locality，总查询 9；实际结果覆盖 Crossref 与 arXiv 两个真实来源。q07 的 Crossref 结果均为词义假阳性，没有相关候选；这保留为检索事实，不机械改词把它包装成命中。

## 3. 去重与筛选

| 项目 | 数值/规则 |
|---|---|
| raw rows | 70 |
| unique records | 63 |
| duplicate rows | 7 |
| dedup key | lowercase DOI；否则 arXiv id 去 version；否则 normalized title |
| shortlist | 10 |
| new MUST_FULLTEXT | 2 |
| new SHOULD_FULLTEXT | 5 |
| abstract-level exact complete chain | 0 |

`MUST/SHOULD` 仅表示必须/建议进入后续 acquire→fulltext-read；**不是**碰撞裁决。题名命中但无 abstract 的字段全部记 `UNKNOWN` 或 `AI推断，未验证`。

## 4. Shortlist 八字段与 abstract 交叉验证

| ID / class | receiver-visible input | trigger | localization | candidate action | decoder interaction | fallback | complexity/latency | output | abstract pointer / OA |
|---|---|---|---|---|---|---|---|---|---|
| `10.1364/OFC.2014.M3A.3` / **MUST_FULLTEXT** | coded coherent-optical observations；exact messages `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | cycle-slip-mitigating turbo demodulation（题名；机制未验证） | LDPC turbo demodulation（题名）；calls `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | local fresh S2=`abstract:null` + Crossref；OA unknown |
| `arXiv:1204.2660` / **MUST_FULLTEXT** | LDPC observations + joint phase/code factor-graph messages | unconditional joint inference；event trigger未述 | abstract states slip treatment；boundary未述 | approximate Bayesian message passing + directional-statistics clustering | joint phase/LDPC decoding factor graph | `UNKNOWN` | abstract says complexity analysis exists；numeric budget未述 | decoded LDPC performance；boundary output未述 | official arXiv abstract；OA available/not downloaded |
| `arXiv:1704.04618` / **SHOULD_FULLTEXT** | differential coherent QPSK + LDPC messages | iterative demod/decoding；无 event trigger | windowed SC-LDPC stated；slip boundary未述 | modified differential decoder accounts for slips | iterative differential demodulation + LDPC/SC-LDPC | `UNKNOWN` | qualitative simple windowed decoder | decoded data；boundary未述 | official arXiv + fresh S2 abstract；OA available/not downloaded |
| `10.1109/ECOC.2014.6963875` / **SHOULD_FULLTEXT** | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | phase-slip-tolerant FEC（题名；AI推断，未验证） | LDPC/FEC named；interface unknown | `UNKNOWN` | “low-complexity”题名声称；账本未知 | `UNKNOWN` | Crossref no abstract；OA unknown |
| `10.1109/ACCESS.2019.2934224` / **SHOULD_FULLTEXT** | blind-CPE output + cumulative averages | thresholded peak of difference between two cumulative-average segments | peak position/location + sign/direction | self-correction；exact repaired region未述 | none stated / NDA | no-op/failure fallback未述 | cumulative segment metric；latency未述 | slip location/direction + corrected phase | fresh S2 abstract；IEEE Access OA expected/not acquired |
| `10.1364/OE.22.031167` / **SHOULD_FULLTEXT** | twice-estimated phase-noise sequence from arbitrary CPE | sliding-average minimum + threshold | sliding minimum；boundary error definition未述 | appendable CS correction；exact phase action未述 | none stated / NDA | optional second window stage；failure fallback未述 | window/threshold + optional second stage | corrected phase / residual slip probability | fresh S2 abstract；fulltext not acquired |
| `10.1364/OFC.2015.TH3E.6` / **SHOULD_FULLTEXT** | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | slip-tolerant differential decoding（题名；AI推断，未验证） | SC-LDPC named | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Crossref no abstract；OA unknown |
| `10.1364/ECEOC.2012.MO.1.A.5` / **STRONG_NEIGHBOR** | differential coherent DP-QPSK + LDPC | none；comparative failure study | none in abstract | classical soft vs turbo differential decode | LDPC turbo differential decoding | none stated | `UNKNOWN` | phase-slip resilience / decoding performance | indexed abstract + Crossref identity；OA unknown |
| `10.1109/IPCON.2012.6358547` / **STRONG_NEIGHBOR** | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | cycle-slip compensation（题名；AI推断，未验证） | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Crossref no abstract；OA unknown |
| `arXiv:2511.21340` / **BASELINE** | whole-frame OFDM + decoder extrinsic evidence | once after EM initialization | whole frame / constant ambiguity | finite PSK-symmetry global bank | decoder selects global candidate | not stated | one invocation；详见既有全文 note | global estimate + decoded frame | official arXiv；already fulltext-read, not new |

完整逐字段 JSON 在 `coded-decoder-c1-step3_5-qm-annotated-round1.json`。最强新候选是 `10.1364/OFC.2014.M3A.3`：题名同时命中 cycle slip、turbo demodulation、LDPC 与 coherent optical，但 S2/Crossref 都没有 abstract，所以只能判 `MUST_FULLTEXT / exact-chain unresolved`，不能判 `EXACT_CHAIN_CANDIDATE_FOUND`。

## 5. Abstract crosscheck 与下一轮术语

| 功能断言 | 交叉验证状态 |
|---|---|
| arXiv 1204.2660 的 phase-slip-aware joint LDPC inference | official arXiv abstract `SUPPORTED` |
| arXiv 1704.04618 的 modified differential decoder + windowed SC-LDPC | official arXiv + fresh S2 abstract `SUPPORTED` |
| ACCESS 2019 的 cumulative-segment trigger、location/direction | fresh S2 abstract `SUPPORTED` |
| Optics Express 2014 的 sliding-average CS detection/correction | fresh S2 abstract `SUPPORTED` |
| OFC 2014 M3A.3 / ECOC 2014.6963875 / OFC 2015 TH3E.6 的具体 action chain | abstract unavailable，`AI推断，未验证`；只凭题名晋级 acquire/read，不裁碰撞 |

下一轮新术语：`turbo differential decoding phase-slip resilience`、`phase-slip tolerant LDPC FEC`、`cumulative-average segment discriminant`、`sliding average twice estimated phase noise`、`windowed SC-LDPC phase-slip decoding`。

本包不能判 Step 3.5 收敛：round 1 新增 MUST/SHOULD=7，后续必须先 acquire/read，再以新术语运行 convergence round；最多三轮规则仍有效。

## 6. 产出与异常

- raw/API：`search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-api-round1.json`
- q05/q06 raw supplement：`search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-api-q05-q06.json`
- annotated：`search-archive/2026-08-09/coded-decoder-c1-step3_5-qm-annotated-round1.json`
- wrapper timeout receipts：`coded-decoder-c1-step3_5-qm-q01.json`、`coded-decoder-c1-step3_5-qm-q02.json`
- worker log：`projects/thesis-fso/worker-logs/step-067-c1-step3_5-query-matrix.md`

异常：project wrapper timeout；S2/OpenAlex direct API 均 429；raw round1 首次 PowerShell 聚合将 q04 的 arXiv rows 附在同一 query object 且漏了 q05/q06，故另建 `qm-api-q05-q06.json` 补齐。annotated 文件以实际 9 个 query receipts 为准，未删除原始异常证据。

## 7. Git 与 p05 保护

- 未 stage、未 commit、未 push；未修改 central owner/治理/代码。
- fresh p05 check 与派遣基线一致：
  - `p05_run.log` 641 bytes / `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log` 2417 bytes / `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log` 929 bytes / `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log` 1430 bytes / `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
