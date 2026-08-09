# Step 3.5 直接竞品获取与 provenance 修复

> 任务：T004 | 日期：2026-08-09 | 范围：仅 acquisition / identity / provenance / 限定动作提取

## 旧状态与实际尝试

| DOI | 旧状态 | 本轮实际命令/通道 | 返回与裁决 |
|---|---|---|---|
| `10.1016/J.OPTCOM.2020.126046` | canonical 仅有 `failed/all_failed` metadata | `bash tools/download --doi ...`；等价入口 `tools/paper_download.py --doi ... --force --dry-run` 后正式 `--force`；Crossref Elsevier text-mining URL；实际请求 Elsevier Article API | wrapper 被 CRLF 语法错误阻断；等价项目工具正式返回 `all_failed`；Crossref identity PASS，但 text/plain API 返回 HTTP 400。`FULLTEXT_UNAVAILABLE`。 |
| `10.1364/OE.505931` | canonical 仅有 `failed/all_failed` metadata | 同上项目下载两阶段；S2/Crossref；官方 Optica `viewmedia.cfm?URI=oe-31-24-40705&seq=0` | 项目工具 `all_failed`；S2 HTTP 429；Crossref identity PASS；官方 URL 返回 HTTP 202、`text/html`、553 bytes（非 PDF）。`FULLTEXT_UNAVAILABLE`。 |
| `10.1364/OE.448956` | canonical 仅有 `failed/all_failed` metadata | 同上项目下载两阶段；S2/Crossref；官方 Optica `viewmedia.cfm?URI=oe-30-5-7854&seq=0` | 项目工具 `all_failed`；S2 identity PASS 且标 `GOLD/CCBY`；Crossref identity PASS；官方 URL 被重定向至 Radware bot manager，得到 15,077-byte HTML（非 PDF）。`FULLTEXT_UNAVAILABLE`。 |
| `10.1109/JPHOT.2022.3161795` | PDF/content 存在且身份通过，但 metadata=`failed/all_failed` | 校验 PDF magic、bytes/SHA、正文题名/DOI；核对 `search-archive/2026-08-05/_step2_receipt.json` 和 Shared-M0 Step 2 报告；Crossref identity | provenance 能闭合为 2026-08-05 `blit-ieee` 获取。以保留 `previous_status/conflict_note` 的新 metadata 修复，`QUALIFIED_FULLTEXT`。 |
| `10.1109/WiSEE61249.2024.10850117` | shared-library PDF/content 存在，但 metadata=`failed/all_failed`；目标 worktree 尚无 canonical 副本 | 校验 PDF magic、bytes/SHA、正文题名；核对 2026-07-10 session 下载记录及 `read-log.md:27`；Crossref identity；复制不变字节到目标 canonical path | provenance 能闭合为 IEEE doc `10850117` 经 `blit-ieee` 获取、`tools/convert` 归档。保留原始冲突并写新 metadata，`QUALIFIED_FULLTEXT`。 |

补充说明：`blit` 仅对 IEEE 通道适用；三篇缺失项属于 Elsevier/Optica，因此未伪装执行不适用的 blit。`tools/download --force` 还曾清空 `papers/index.json` 中 OE.505931/OE.448956 的既有 title/batches 并新增 Cheng 空条目；该非证据副作用已用精确补丁恢复，最终 `papers/index.json` blob 与 HEAD 均为 `f8c2d6b7894b97894585b27d43b3a4540337b2ae`。

## Identity/provenance table

| DOI | exact title | source/channel | canonical path | bytes / SHA256 | title/DOI evidence | status / 承重 |
|---|---|---|---|---|---|---|
| `10.1016/J.OPTCOM.2020.126046` | Training-aided joint frame and frequency synchronization for free space optical communication signals with low OSNR | Crossref DOI identity；Elsevier API 未取得正文 | `papers/doi/10.1016_j.optcom.2020.126046/metadata.json` | 无全文 | Crossref title+DOI | `FULLTEXT_UNAVAILABLE` / 否 |
| `10.1364/OE.505931` | Real-time low-complexity diversity combining algorithm for free space coherent optical communication systems over atmospheric turbulence channel | Crossref + Optica official viewmedia（非 PDF） | `papers/doi/10.1364_oe.505931/metadata.json` | 无全文 | Crossref title+DOI | `FULLTEXT_UNAVAILABLE` / 否 |
| `10.1364/OE.448956` | Performance analysis of a spatial diversity coherent free-space optical communication system based on optimal branch block phase correction | S2/Crossref + Optica official viewmedia（bot block） | `papers/doi/10.1364_oe.448956/metadata.json` | 无全文 | S2/Crossref title+DOI | `FULLTEXT_UNAVAILABLE` / 否 |
| `10.1109/JPHOT.2022.3161795` | Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication | `blit-ieee`; DOI landing `https://doi.org/10.1109/JPHOT.2022.3161795` | `papers/doi/10.1109_jphot.2022.3161795/{source.pdf,content.md,metadata.json}` | PDF 2,413,149 / `E7D281...DAD1CE`; content 36,071 / `DB526B...FB69` | `content.md:5` title；`:21` DOI；Crossref；2026-08-05 receipt | `QUALIFIED_FULLTEXT` / 是 |
| `10.1109/WiSEE61249.2024.10850117` | Data-Aided Multi-Format DSP for Robust Free-Space Coherent Optical Communication | `blit-ieee`, IEEE doc `10850117`; `https://ieeexplore.ieee.org/document/10850117` | `papers/doi/10.1109_wisee61249.2024.10850117/{source.pdf,content.md,metadata.json}` | PDF 1,185,870 / `87222B...340CE`; content 35,131 / `214343...14E` | `content.md:3` title；Crossref DOI identity；2026-07-10 acquisition record | `QUALIFIED_FULLTEXT` / 是 |

## Fulltext action table

| DOI | method action | information source / granularity | condition inputs | online/offline | lag/window/`B_L` 可变？ | exact collision? / 证据 |
|---|---|---|---|---|---|---|
| Tang 2022 | 两阶段：对称训练块相关定位 frame start，再用已定位训练块和其对称序列估计/补偿该 training period 的 CFO | receiver-visible 1-sps 样本 + known `[A,B,A*,B*]`；按 training period 决策 | 无 condition-to-parameter 输入；功率/湍流仅用于评测 | 接收 DSP 动作；实验/仿真处理 | 否。训练结构与 `N` 固定；固定 training period 后仅首周期 localization，主 FOE 比较 `N=1024` | **否**。没有 condition→lag/`B_L` selection 或 multi-lag weighting。证据 `content.md:45-85,109-161`。 |
| WiSEE 2024 | 固定 frame header 做 sample-exact frame sync；A/B 两级 coarse/fine CFO；每 frame data-aided MIMO equalization；pilot+BPS 两级 CPE | known header/pilots；frame 32768 symbols；header B=4×256，A=32；每100 symbol CPE pilot | SNR/PDL/PN/CFO 是输入损伤或离线性能轴，不驱动 lag/window 选择 | 算法按 frame 动作；外场数据块离线 Rx-DSP | 否。A/B/CE header/pilot spacing 固定；论文只说明可人工改短 A 扩 acquisition range，不是 receiver-condition 自适应选择 | **否**。generic data-aided low-SNR DSP/adjacent evidence，不是 exact action。证据 `content.md:33-72,86-98,171-173`。 |

## Unavailable evidence blockers

- Cheng 2020：项目 OA/Unpaywall 管线无全文；Elsevier Crossref text-mining link实际请求 HTTP 400。只有 metadata/abstract，不作 method action、online/conditioned 或 collision 结论。
- OE.505931：官方 Optica viewmedia 返回 553-byte HTML，不是 PDF；无一手全文，不把 abstract 中 CV-DD-LMS/CPR 描述升级为 exact-action 结论。
- OE.448956：虽被 S2 标为 GOLD/CCBY，但官方 Optica URL 被 Radware 阻断；本轮没有合法可审计 PDF 字节，故仍不可承重。

## Files changed

- `projects/thesis-fso/worker-logs/step-3-5-rml-acquisition-provenance.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-acquisition-receipt.json`
- `papers/doi/10.1109_jphot.2022.3161795/metadata.json`
- `papers/doi/10.1109_wisee61249.2024.10850117/{source.pdf,content.md,metadata.json}`
- 三篇 unavailable 的 `metadata.json`：仅恢复被 `--force` 清空的 task identity/title，保留 `failed/all_failed`。

`papers/index.json` 曾被工具改坏但已恢复为 HEAD 同一 blob，因此不属于最终 changed files。

## Boundaries

- 未改 topic index、literature notes、decisions、master/current views。
- 未进入 Step 4a，未比较数值胜负，未设计 adaptive lag，未运行仿真/MVE。
- 未读取、修改或删除四个 `p05_run*.log`；未触碰 `common/`、`params.py`、正式论文或 dormant campaign。
