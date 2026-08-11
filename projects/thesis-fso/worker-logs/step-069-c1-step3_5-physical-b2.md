# Step 069 — C1 Step 3.5 coherent-optical/FSO 物理 occurrence 与 strongest B2

> 2026-08-09 | T023 | fresh validator | `TARGETED_SUPPLEMENT_SEARCH` / CP009
> Terminal: `PHYSICAL_B2_SEARCH_COMPLETE`

## 1. 范围与证据上限

本轮只做摘要级物理 occurrence/model 与 B2 候选补检；未下载或阅读全文，未运行实验，未改中央 owner、治理、代码或 p05。task-control validator 返回 `PASS`。功能与参数结论只采用 S2 摘要；8 个 DOI 由 Crossref 再核身份，其中 PAPU 与 CV-DD-LMS 两篇还取得 Crossref 摘要复核。无摘要或正文才可能给出的字段均记为 `FULLTEXT_REQUIRED`，不能据题名裁 exact collision。

## 2. Query / command / source receipts

| # | 命令/查询 | 来源 | 结果 | receipt |
|---|---|---|---|---|
| Q1 | `bash tools/search "coherent optical free space optical cycle slip phase noise carrier recovery turbulence fade" --sources s2 openalex arxiv ...` | S2/OpenAlex/arXiv | 94 s 超时，写入空 receipt | `coded-decoder-c1-step3_5-physical-b2-occurrence.json` |
| Q2 | `bash tools/search "coherent optical cycle slip detection correction FEC" --sources s2 ...` | S2 | 10 篇 | `coherent-optical-cycle-slip-detection-correction-fec.json` |
| Q3 | `bash tools/search "coherent free space optical carrier phase recovery phase noise atmospheric turbulence fading cycle slip" --sources s2 ...` | S2 | 7 篇 | `coded-decoder-c1-step3_5-physical-b2-fso-s2.json` |
| Q4 | `bash tools/search "coherent optical cycle slip phase noise FEC correction" --sources openalex ...` | OpenAlex | 429/超时，无结果文件；保留失败事实，不再死等 | 本日志 |
| Q5 | `bash tools/search "coherent optical cycle slip phase noise carrier phase recovery" --sources arxiv ...` | arXiv | 0 篇 | `coded-decoder-c1-step3_5-physical-b2-arxiv.json` |
| Q6 | `bash tools/search "Cycle slip mitigating turbo demodulation LDPC coded coherent optical communications" --sources s2 ...` | S2 | 3 篇 | `coded-decoder-c1-step3_5-physical-b2-exact-chain-s2.json` |
| X1 | Crossref `/works/{doi}`，8 DOI | DOI/Crossref | 8/8 身份确认；2 篇返回摘要 | 标注 JSON `source_receipts` |

结构化标注与逐条路径见 `search-archive/2026-08-09/coded-decoder-c1-step3_5-physical-b2-annotated.json`。本轮真实论文来源不低于 6 篇；检索 API 实际成功来源为 S2，DOI 身份交叉源为 Crossref。OpenAlex/arXiv 的失败/零结果不冒充有效证据。

## 3. 物理事实与参数边界

| 来源 | 摘要支持的事实 | 可引用参数 | 不能越过的边界 |
|---|---|---|---|
| `10.1364/OE.22.031167` | coherent system 可由 estimated phase noise 的滑动统计检测/校正 cycle slip；window 与 threshold 影响检测 | 单载波仿真残余 CS 概率 `2×10^-7`；第二级不同 window 再降至少一数量级 | window/threshold 数值、跳变量与 slip-rate 均 `FULLTEXT_REQUIRED` |
| `10.1109/ACCESS.2019.2934224` | coherent wireless optical QPSK 的 blind CPE 会出现 cycle slip；摘要把压力源指向 atmospheric turbulence 与 laser linewidth；累计均值差 `δ` 的峰位置/符号给位置/方向 | QPSK；weak turbulence（定性） | 湍流强度、linewidth、SNR、slip-rate、精确 correction rule 均 `FULLTEXT_REQUIRED` |
| `10.3390/APP9132749` | continuous CS 会恶化 post-FEC；VVPE+PAPU 是明确 pilot B2 | 56 Gbit/s QPSK；pilot overhead `0.78%`；filter length `8/16/20`；摘要给 pre/post-FEC OSNR gain 与 FEC-limit 数字 | pilot 间隔、slip 注入/统计模型 `FULLTEXT_REQUIRED` |
| `10.1364/OE.505931` | coherent FSO atmospheric-turbulence receiver 在 low SNR 有 CS 风险；CV-DD-LMS combining+CPR 可避免 CS（论文摘要自陈） | 三输入、2.5 Gbit/s QPSK；VOA 模拟 `100 kHz` power fluctuation | VOA 深度、SNR 门限、自然 fade 映射、linewidth `FULLTEXT_REQUIRED` |
| `10.1109/JLT.2020.3003561` | satellite-ground coherent model同时含 turbulence、AO、laser phase noise、Tx/Rx frequency mismatch；残余幅度波动和 laser phase noise 为主导 impairments | DPLL 收敛尺度为数百微秒（摘要定性量级） | 数值湍流、linewidth、frequency offset 与离散 slip 模型 `FULLTEXT_REQUIRED` |
| `10.3390/APP8050664` | FSO coherent recovery 可用 Málaga irradiance turbulence、non-zero-boresight pointing error 与 Tikhonov phase noise 联合建模 | 模型族可引用 | 各分布 shape/concentration 参数 `FULLTEXT_REQUIRED` |

成因分级：laser phase noise/linewidth、atmospheric turbulence、low-SNR/power fluctuation 与 blind-CPE slip 有摘要级直接关联；`decision-error propagation`、pilot-spacing 诱发、loss-of-lock 状态机、离散 `±2π/M` jump、piecewise-constant boundary/burst law 在本轮摘要中**未确认**，只能作为待核假设，不能当文献事实。

## 4. Provisional strongest conventional B2：CSSC-CPE

选择 `10.1109/ACCESS.2019.2934224`，而不是 BPS、pilot PAPU、DD-PLL 或题名级 FEC-assisted candidate，原因是它在摘要层已经闭合 receiver-only、non-data-aided、coherent-WOC、定位与方向四项，和 Q1 的 local-slip 条件最任务匹配；同时不读取 decoder evidence，可作为所提 decoder-local repair 必须击败的传统吸收方案。它只是 provisional B2，全文前不能冻结具体预算。

| 完整八字段 | CSSC-CPE 摘要级签名 |
|---|---|
| input | blind-CPE output；无 pilot、无 decoder evidence |
| trigger | 两段 cumulative average 的差 `δ` 做 peak/threshold 判定 |
| localization | `δ` peak position 定位；peak sign 给 slip direction |
| action | self-correct detected CS；是否严格只改 segment/suffix，摘要未说明 |
| decoder interaction | none；纯 front-end receiver-only |
| fallback | `NOT_STATED_IN_ABSTRACT`；Step 4a 若实现 comparator，须预注册 threshold 未越过时 no-correction |
| budget | cumulative averages + discriminant sequence + peak/threshold；运算数、buffer、latency `FULLTEXT_REQUIRED` |
| output | corrected carrier-phase estimate / symbol stream，随后才进 decoder |

已知 failure mode：摘要只验证 weak turbulence；多 slip、deep fade、false correction、threshold calibration 及 exact fallback 未闭合。通用 CS-DC (`10.1364/OE.22.031167`) 是并列强邻居：modulation-independent 且可 append 至任意 CPE，但其摘要没有 decoder interaction，也未给 Q1 所需的 bounded suffix 规则。

## 5. Complete-chain shortlist（9 篇，未以摘要裁 exact）

| rank | DOI / 条目 | 标签 | 八字段摘要判读 | OA/公开全文指针* |
|---:|---|---|---|---:|
| 1 | `10.1109/ACCESS.2019.2934224` CSSC-CPE | `SHOULD_FULLTEXT` `PHYSICAL_SOURCE` `B2_BASELINE` | receiver-only detect/localize/direction/correct；无 decoder/fallback | 是 |
| 2 | `10.1364/OE.22.031167` universal CS-DC | `SHOULD_FULLTEXT` `PHYSICAL_SOURCE` `B2_BASELINE` | sliding detect/correct + optional second stage；无 decoder | 是 |
| 3 | `10.1364/OFC.2014.M3A.3` turbo demodulation | `MUST_FULLTEXT` `NEIGHBOR` | 题名命中 LDPC-coded coherent optical + CS mitigation；摘要缺失，八字段未决 | 是 |
| 4 | `10.1109/ICTON.2016.7550341` layered LDPC/turbo differential | `MUST_FULLTEXT` `NEIGHBOR` | 题名命中 LDPC + cycle slips；摘要缺失，八字段未决 | 否 |
| 5 | `10.3390/APP9132749` VVPE+PAPU | `SHOULD_FULLTEXT` `PHYSICAL_SOURCE` `B2_BASELINE` | pilot unwrap + post-FEC evaluation；非 decoder-triggered reevaluation | 是 |
| 6 | `10.1002/9781119078289` coherent-optical coding chapter | `SHOULD_FULLTEXT` `NEIGHBOR` | differential coding + iterative differential demod/LDPC；摘要无 local boundary/segment/fallback | 是 |
| 7 | `10.1364/OE.505931` CV-DD-LMS | `PHYSICAL_SOURCE` `B2_BASELINE` | diversity combining+DD CPR；无 explicit slip-repair chain | 是 |
| 8 | `10.1109/JLT.2020.3003561` AO+DPLL | `PHYSICAL_SOURCE` `B2_BASELINE` | 物理/model 与 classical PLL anchor；无 local repair/decoder | 是 |
| 9 | `10.3390/APP8050664` Málaga/Tikhonov FSO | `PHYSICAL_SOURCE` | 物理统计模型 anchor | 是 |

\* 仅统计搜索元数据中的 OA/license/PDF/arXiv 指针，本轮未打开或下载全文。计数：`MUST_FULLTEXT=2`，`SHOULD_FULLTEXT=4`，shortlist `9`，OA/公开全文指针 `8/9`。

最强 exact-chain candidate 是 OFC 2014 `10.1364/OFC.2014.M3A.3`，但当前状态只能是 `UNRESOLVED_FULLTEXT`：题名不能证明 `localize → segment/suffix correction → FEC re-evaluation → fallback`，因此**没有发现可判定的 exact complete-chain collision**。ICTON 2016 为第二候选，同样不能越过题名。

## 6. Step 4a truth-free stress slice：可用 / 不可用

摘要已足够支持的最小输入：QPSK；weak-turbulence/low-SNR 作为定性压力轴；Málaga irradiance + Tikhonov phase-noise 作为模型族；`100 kHz` VOA fluctuation 只作为实验室功率波动切片（不得冒充自然 fade 统计）；CSSC 使用 receiver-visible CPE-output cumulative averages 和 `δ` peak/sign，触发不读取 truth；pilot B2 可用 `0.78%` overhead、filter length `8/16/20`。

不可直接开跑的参数：离散 `±2π/M` jump law、piecewise boundary distribution、slip rate/burst/multiple-slip spacing、numeric linewidth/normalized linewidth、SNR/fade-depth/turbulence-strength、pilot spacing、CSSC windows/threshold/correction/fallback。它们必须全文核实或在 Step 4a 明示为预注册 sweep；不得伪装成文献参数。物理 occurrence 也不等于 decoder-local repair 可行，仍须由 Step 4a defect/headroom 与 B2 absorption 分开验证。

## 7. 终态

`PHYSICAL_B2_SEARCH_COMPLETE`

- physical source count：`6`
- MUST / SHOULD：`2 / 4`
- provisional strongest B2：CSSC-CPE (`10.1109/ACCESS.2019.2934224`)
- strongest exact-chain candidate：OFC 2014 (`10.1364/OFC.2014.M3A.3`), `UNRESOLVED_FULLTEXT`
