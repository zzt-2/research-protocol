# Step 3.5 RML-FSTS R2 must-read acquisition/fulltext 裁决

> Task: `.sessions/2026-08-08-rml-fsts-groundwork/T005-step3-5-r2-must-read.md`
> Date: 2026-08-09
> Terminal: `BLOCKED_ON_FULLTEXT`

## Acquisition/identity table

| DOI | Crossref / publisher identity | 年份 | 实际获取通道 | identity 结论 |
|---|---|---:|---|---|
| `10.1364/OE.561252` | Crossref title 与 R1 title 完全一致；publisher resource 指向 Optica `oe-33-10-21660` | 2025 | `tools/download` wrapper；等价 `paper_download.py`；Crossref VOR；Optica issue/PDF；in-app browser | `MATCH` |
| `10.1109/ACP/IPOC63121.2024.10809664` | Crossref title 与 R1 title 完全一致；resource 指向 IEEE document `10809664` | 2024 | `tools/download` wrapper；等价 `paper_download.py`；IEEE stampPDF/direct PDF；Crossref staging VOR；author-copy search | `MATCH` |
| `10.2139/SSRN.6293357` | Crossref title 与 R1 title 完全一致；resource 指向 SSRN abstract `6293357` | 2026 | `tools/download` wrapper；等价 `paper_download.py`；SSRN indexed/alternate delivery；author/institution search | `MATCH` |

R1 本地 evidence：`search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json:131`、`:137`、`:143`。Crossref identity endpoints 与 publisher resource 已逐项固化在本任务 receipt；未发现重复 DOI、未来年份矛盾或 title/content 错配，因此不是 `IDENTITY_BLOCKED`。

## Fulltext receipt table

| DOI | status | canonical path / SHA / bytes | 失败证据 | 可否全文裁决 |
|---|---|---|---|---|
| `10.1364/OE.561252` | `FULLTEXT_UNAVAILABLE` | `null / null / null` | wrapper 因 CRLF 未进入网络；等价 Python 为 `all_failed`；Optica VOR 返回 553-byte JS challenge，`/oe` PDF 路径转 Radware CAPTCHA；browser backend 不可用 | 否 |
| `10.1109/ACP/IPOC63121.2024.10809664` | `FULLTEXT_UNAVAILABLE` | `null / null / null` | wrapper CRLF；等价 Python `all_failed`；IEEE stamp/direct PDF 为 HTTP 418；Crossref staging VOR TLS 失败；作者副本搜索仅见 request-full-text | 否 |
| `10.2139/SSRN.6293357` | `FULLTEXT_UNAVAILABLE` | `null / null / null` | wrapper CRLF；等价 Python `all_failed`；SSRN indexed delivery 与 `abstractid` 端点 HTTP 403；无合法 alternate fulltext | 否 |

没有 qualified PDF，因此没有运行 `tools/convert`，也没有创建伪 canonical `content.md` / read-note。搜索引擎暴露的 abstract、publisher-indexed snippet 与 program excerpt 均未冒充全文。

## Action extraction

### 10.1364/OE.561252

- estimator/training action：`UNKNOWN_FROM_QUALIFIED_FULLTEXT`。仅 abstract/index snippet 可知它使用 single-tone TS 做 FOE 和 branch phase correction；这不足以穷尽正文中的 lag/window/`B_L` 定义。
- information source、decision granularity、candidate set、selection/weighting rule、fixed/adaptive：全部 `UNKNOWN`。
- 与 Wang FSTS、Cheng/Tang/Enhanced 的比较角色：`UNKNOWN`。
- 正文 evidence lines：无；全文不可得。

### 10.1109/ACP/IPOC63121.2024.10809664

- estimator/training action：`UNKNOWN_FROM_QUALIFIED_FULLTEXT`。标题/会议程序摘要只支持“single short symbol block FOE”，不能证明它是离线固定长度，也不能证明存在 condition-aware selector。
- information source、decision granularity、candidate set、selection/weighting rule、fixed/adaptive：全部 `UNKNOWN`。
- 与 Wang FSTS、Cheng/Tang/Enhanced 的比较角色：`UNKNOWN`。
- 正文 evidence lines：无；全文不可得。

### 10.2139/SSRN.6293357

- estimator/training action：`UNKNOWN_FROM_QUALIFIED_FULLTEXT`。官方 abstract 只支持 low received power 下 joint FS/FOE 与 short training sequence；“场景为低功率”不等价于“功率/可靠性作为在线 selector input”。
- information source、decision granularity、candidate set、selection/weighting rule、fixed/adaptive：全部 `UNKNOWN`。
- 与 Wang FSTS、Cheng/Tang/Enhanced 的比较角色：`UNKNOWN`。
- 正文 evidence lines：无；全文不可得。

## Collision classification

| DOI | classification | exact collision | cheap lookup equivalent | 理由 |
|---|---|---|---|---|
| `10.1364/OE.561252` | `UNRESOLVED_FULLTEXT_DEBT` | `UNKNOWN` | `UNKNOWN` | single-tone/branch phase correction 是相邻架构信号，但无全文不能排除或确认 receiver-visible condition → lag/`B_L`/multi-lag weight |
| `10.1109/ACP/IPOC63121.2024.10809664` | `UNRESOLVED_FULLTEXT_DEBT` | `UNKNOWN` | `UNKNOWN` | “optimized short block”不能仅凭标题归类为 offline fixed，也不能判成 adaptive |
| `10.2139/SSRN.6293357` | `UNRESOLVED_FULLTEXT_DEBT` | `UNKNOWN` | `UNKNOWN` | low-power condition 是场景描述，abstract 不足以确定 selector input 与粒度 |

本轮没有确认 exact collision，也没有确认 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup 等价物；这两个 boolean 均保留 `UNKNOWN`，而不是误写为 `false`。

## R2 disposition

- `10.1364/OE.561252` must-read debt：**未关闭**，阻塞于 qualified fulltext。
- `10.1109/ACP/IPOC63121.2024.10809664` must-read debt：**未关闭**，阻塞于 qualified fulltext。
- `10.2139/SSRN.6293357` must-read debt：**未关闭**，阻塞于 qualified fulltext。
- R2 terminal：`BLOCKED_ON_FULLTEXT`；`QUALIFIED_READ=0/3`，`FULLTEXT_UNAVAILABLE=3/3`。本任务不据此宣称 Step 3.5 收敛。

## Files changed and boundaries

- 新增 `projects/thesis-fso/worker-logs/step-3-5-rml-r2-must-read.md`。
- 新增 `search-archive/2026-08-09/rml-fsts-step3-5-r2-must-read-receipt.json`。
- 下载器创建的 3 个空-title failed `papers/index.json` 条目已用精确 patch 移除；保留并发任务的 `10.1016/J.OPTCOM.2024.130981` 条目，恢复文件末尾换行。
- 本任务产生的 3 个 failed paper 目录仅含失败 metadata/挑战 HTML；收束时删除，不作为 canonical paper。
- 未修改 topic-index、literature notes、decisions、master/current views；未触碰 p05/pyc；未进入 Step 4a、未比较数值胜负、未设计方法。
