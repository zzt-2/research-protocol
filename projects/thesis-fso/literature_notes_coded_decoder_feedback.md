# Coded decoder-feedback Literature Owner

> 独立 owner：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/`
> 研究对象：C1 finite global phase-hypothesis decoder selection 的 reference-method extension
> 当前状态：Step 3.5 已由 V003 独立验收并带限制完成；当前只进入 Step 4a A0 §0–§6 分析预检，adapter/defect smoke/MVE/实验仍禁止。

## GW Progress

| Step | 状态 | 日期 | 证据 | 下游门控 |
|---|---|---|---|---|
| 1 search | ✅ PASS / REFERENCE ENTRY | 2026-08-09 | integrated v2.1=93→66；D003–D005/V002 | 固定 shortlist，不重做 broad search |
| 2 acquire | ✅ COMPLETE | 2026-08-09 | 5 篇合格全文 + 2 unresolved；Step 2 coverage report；step-058–065 | 允许 Step 3 Q# |
| 3 read | ✅ COMPLETE / Q1 4/4 | 2026-08-09 | 六份 qualified fulltext read note + full-chain synthesis + D008/step-066 | 允许 mandatory Step 3.5 |
| 3.5 supplement | ✅ COMPLETE / VERIFIED WITH LIMITS | 2026-08-10 | D009/V003；step-067–083；`step3_5-supplement-report.md` | 只允许 Step 4a A0 分析，不等于 defect PASS |
| 4a feasibility | 🔄 A0 §0–§6 IN PROGRESS | 2026-08-10 | D009/CP010/H002 | A0 PASS 后另立决策才允许 defect smoke |

## Step 2 固定输入

| ID | 方法角色 | 可承重全文事实 | 证据上限 |
|---|---|---|---|
| L01 arXiv 2511.21340 | C1 reference M | whole-frame PSK `C` candidates；one-shot decoder evidence；global rotation | preprint/global constant phase |
| L02 TSP 2006 | published global finite-hypothesis M | whole-frame phase/delay bank；per-candidate decoder metrics；explicit iteration cost | AWGN coded burst，不含 local slip |
| L03 GLOBECOM 2012 | B2 continuous decoder-aided CPR | per-symbol PLL state，whole-codeword outer iterations，hard/soft decisions | constant CFO/QPSK；无 slip trigger |
| L04 IWCMC 2023 | recent global coarse B2 | 27 syndrome points→5 decoder-CMF candidates→global EM；+5 decoder iterations | AWGN/QPSK/CCSDS；whole-frame only |
| L05 TWC 2004 | historical direct decoder-extrinsic CPR | APPA extrinsic likelihood、whole-window iterative phase update、optional 2/4 global banks | block-constant phase；无 local action |
| L06 TVT 2025/2026 | recent top-journal global CA CFO/CPO baseline | ICE global stochastic coarse candidates + Polar posterior-LLR CEM；Eqs. 14–45 / Algorithms 1–2 | per-frame/per-satellite global state；`STRONG_NEIGHBOR`，无 local slip chain |
| U01 SPIE 2025/2026 | coherent-optical cycle-slip comparator candidate | `UNRESOLVED_FULLTEXT` | 不裁 B2/collision |
| U02 ACCESS 2026 | recent partial-metric synchronization candidate | `UNRESOLVED_FULLTEXT` | 不裁 local chain/B2 |

各单篇结构化参数、十问、M/C/A 原料、实验完备性与八字段矩阵见 `papers/_read_notes/`；获取和执行审计见 `projects/thesis-fso/worker-logs/step-058-*` 至 `step-066-*`。

## Step 3.5 核心新增全文

| ID | 方法角色 | 可承重全文事实 | 完整链 verdict / 上限 |
|---|---|---|---|
| L07 OFC 2014 | discrete-slip turbo demodulation neighbor | Markov slip trellis + LDPC soft feedback；whole-codeword fixed turbo | `PARTIAL_CORE_ONLY`；无 explicit boundary/local carrier repair/fallback |
| L08 ICTON 2016 | decoder-schedule neighbor | layered LDPC + unsatisfied-check rollback/stop | `STRONG_NEIGHBOR`；无 carrier localization/action |
| L09 TCOM 2015 / arXiv 1306 | joint phase-decoder neighbor | Tikhonov-mixture per-symbol tracker + full-sequence decoder loop | `STRONG_NEIGHBOR`；无 detected local repair |
| L10 arXiv 1204 | joint phase/LDPC core neighbor | whole-codeword message passing + per-symbol confidence | `PARTIAL_CORE_ONLY`；无 boundary/range/fallback |
| L11 ECOC14 / OFC15 / arXiv1704 family | phase-slip-tolerant FEC family | block-symmetric or slip-BCJR + LDPC/SC-LDPC code-graph window | `STRONG/PARTIAL`；码图窗不是 slip-local repair |
| L12 OFC 2015 Tu3B.2 | differential-aware FEC neighbor | HTDD 固定 TDD→plain-LDPC cleanup；differential coding 限制 error propagation | `STRONG_NEIGHBOR`；无 boundary/sample repair |
| L13 arXiv 2604.07004 | burst-state + LDPC feedback neighbor | GE Markov-modulated Wiener state；逐符号 G/B posterior + IBA | `PARTIAL_CORE_ONLY`；burst 非 discrete slip，无 carrier action |
| L14 PAPU 2019 | topology-matched B2 | 0.78% pilot、per-127、filter `{4,8,16,20,32,48}` | `STRONG_NEIGHBOR / B2_TASK_MATCHED`；exact equations 有债 |
| L15 OFC 2017 | no-feedback pilot soft-state B2 | pilots + 4-state slip probability + fully-parallel LLR marginalization | `STRONG_NEIGHBOR`；明确 no decision feedback，无 boundary/local re-decode |
| L16 JLT 2020 | coherent-FSO physical anchor | HV/Bufton/TURANDOT+AO、paired 2 s `rho/phi`、100 MHz CFO、fading penalty | `NOT_COMPARABLE`；不证明 turbulence 导致 discrete slip |

新增全文、三轮 query/citation receipts 和身份血缘见 `projects/thesis-fso/coded-decoder-feedback-groundwork/step3_5-supplement-report.md` 与 `projects/thesis-fso/worker-logs/step-067-*` 至 `step-081-*`。

## Complete-chain synthesis

| 链字段 | L01/L02 global finite bank | L03/L05 iterative CPR | L04 global syndrome/CMF | 当前未覆盖项 |
|---|---|---|---|---|
| receiver input | whole-frame samples + decoder evidence | samples + hard/soft/extrinsic decision | samples + syndrome + decoder LLR | local evidence source需冻结 |
| trigger | fixed initialization / fixed `I_H` | unconditional outer iteration | unconditional per-frame acquisition | event/defect trigger |
| localization | whole frame | per-symbol state或fixed window，无boundary label | whole frame phase/NFO | detected slip boundary/affected region |
| action | global finite rotation/selection | continuous whole-window/PLL update | global grid correction+EM | bounded segment/suffix repair |
| decoder | per-candidate global decode | iterative decoder↔estimator | shortlist decode+global EM | touched-CW bounded re-evaluation |
| fallback | absent/abstain细节不足 | NDA initialization；无failure branch | absent | clean no-op + B1/B2 fallback |
| budget | explicit global decode equivalents | 4–50 whole-window iterations | 27 cheap +5 decode +3 EM | matched local cost/latency ledger |
| output | global phase/model + decoded frame | phase trajectory/window estimate + bits | global phase/NFO + bits | boundary/local repair outcome |

Bounded-slice provisional verdict：`NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE`。三轮上限内唯一最终新增 OFC 2017 已全文裁为 `STRONG_NEIGHBOR`；这仍不是领域级 novelty closure，CSSC/CS-DC、U01/U02 和 source-recall 限制必须随 claim 保留。

## P08-R2 reuse boundary

- reusable：`k=1024,n=1536,rate=2/3` 5G-NR LDPC component、Gray-16QAM、on-air interleaver、known prefix、receiver-visible equalization、paired/raw schema patterns。
- bounded adapter：soft full-codeword output、iteration override、`msg_v2c` state、observation callbacks、restricted receiver-view schema、touched-CW restart。
- absent：carrier phase/CFO/slip impairment、phase action callee、localized rollback/redecode、persistent controller。
- truth denylist：TX payload、true phase/CFO/h/SNR/slip boundary、oracle action、final correctness、BER/FER 不得进入 trigger/action。
- fresh estimate：method-local minimal chain 5–6.5 日；`>7D_BLOCKER=NOT_ESTABLISHED`。

## Step 3 输入边界

可作为 M 的事实：L01/L02 的一次性全局有限候选 decoder selection，以及 L04 的 global syndrome/CMF coarse selection。可作为 A 的结构性原料：单一 whole-frame phase hypothesis 无法同时对齐一个 frame 内两个不同 constellation orientations；这仍须形成可证伪 Q#，不能先写成 target coherent-FSO defect 已发生。

近期顶刊 baseline gate 由 TVT 2025/2026 ICE-CEM 闭合；2023 IWCMC 提供 recent conference global syndrome/CMF 成本锚，historical direct comparators 由 TSP 2006/TWC 2004/GLOBECOM 2012 闭合。量化对象包括 FER/post-BER/goodput、boundary localization、candidate/decoder calls、latency 与 clean/no-slip safety。

Step 3 必须显式区分：`FACT=global/window assumptions and algorithms`；`INFERENCE=local slip would violate one-global-hypothesis assumption`；`UNKNOWN=合法 coherent-FSO occurrence, observability, recoverability, B2 absorption`。

## Canonical Q1 与四判据

**Q1**：arXiv 2511.21340 / TSP 2006 型整帧单一 finite phase-hypothesis decoder selection M，在 coherent-FSO coded receiver 的单帧内发生一次局部 constellation-symmetry phase slip / piecewise ambiguity C 下，因 M 假设整帧共享同一 phase class、不能同时对齐 slip 前后两段且不输出 boundary A，可能产生可恢复的 FER/goodput 损失；是否能以 receiver-visible decoder metric 触发并定位一个 boundary，只对 bounded segment/suffix 重评候选，clean frame no-op 并回退 B1/B2？

| 判据 | 状态 | 证据/缺口 |
|---|---|---|
| 1 具体 M-C-A | PASS | M 的 global assumption 与输出由 L01/L02 全文；C/A 是可证伪结构假设，occurrence/observability/recoverability留给 Step 3.5/4a |
| 2 方法产出形态 | PASS | 可复用的 trigger→localize→bounded repair→fallback→cost 完整算法链 |
| 3 近期顶刊 baseline | **PASS** | TVT DOI `10.1109/TVT.2025.3600028` / arXiv `2309.12828`；正式顶刊、具体 ICE-CEM global code-aided CFO/CPO baseline |
| 4 可量化对标 | PASS | B1/B2/O1/C1-ext 的 FER/post-BER/goodput、paired CI、decode/CPR/latency、clean safety |

Q1 已是 canonical 4/4，Step 3 COMPLETE。TVT 完整链为 `STRONG_NEIGHBOR`，不是 exact collision；D008 只授权 mandatory Step 3.5，adapter、defect smoke、MVE 与实验继续禁止。

## Step 3.5 执行合同

- 关键词矩阵：至少 3 个方法变体，每个交叉至少 2 个 scenario/locality term，总查询数至少 8，覆盖至少 2 个真实来源。
- 引文链：选择最高引用的核心竞品，完成 forward + backward，筛查至少 10 篇 abstract 并保留 receipt。
- 物理/B2：补 coherent-optical/FSO cycle-slip occurrence/model/参数与 strongest conventional pilot/BPS/DD/FEC-assisted B2。
- 所有功能断言用 Semantic Scholar/DOI abstract 交叉验证；摘要不支持时标 `AI推断，未验证`。
- 新 must/should 候选必须获取/精读全文；最后一轮新增 must/should=0 才可判收敛，最多 3 轮。

## Step 3.5 执行 receipt 与暂定入口

- Round 1 query matrix：raw/unique=`70/63`，新增 MUST/SHOULD=`2/5`；双向引用链筛 12 篇摘要，新增=`0/1`。
- Round 2：raw/unique=`101/97`，新增=`0/2`；arXiv 2604.07004 与 OFC 2015 Tu3B.2 均已全文裁为 non-exact。
- Round 3：raw/unique=`82/79`，新增=`0/1`，形式终态=`ROUND3_CAP_REACHED_WITH_NEW`；唯一新增 OFC 2017 已全文关闭为 `STRONG_NEIGHBOR`，没有启动第 4 轮。
- 物理锚：OFC 2014 measured optical stress 中 pre-FEC BER>`1e-2` 时 slip-rate 可>`1e-3`；ICTON synthetic PCS=`1e-3`–`4e-3`；这些只给相邻 order，不可直接声明 coherent-FSO occurrence。
- B2：PAPU topology 与 OFC 2017 pilot soft-state/LLR route 均进入 Step 4a cheap-alternative audit；CSSC/CS-DC 仍为全文债。
- 当前 disposition：达到 3 轮上限、全部新增 MUST/SHOULD debt 已处理、未确认 exact complete-chain collision；step-082/083 两路 fresh verifier 均 `PASS 0/0/0`，D009/V003 已带限制进入 Step 4a A0 分析预检。
- Step 4a 仍须实证 occurrence、B0/B1 loss、O1 recoverability、B2 absorption、decoder observability 与 3–7 日 adapter 预算；这些均未由文献步骤预设为 PASS。
