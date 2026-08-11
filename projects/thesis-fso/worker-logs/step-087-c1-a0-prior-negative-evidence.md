# Step 087 — C1 A0 §2–§6 先验覆盖、负面证据与 B2 audit

> 2026-08-10 | T041 / CP010 / epoch 10 | action=`FEASIBILITY_A0`
> Terminal: `A0_2_6_CONDITIONAL_NO_FATAL_CONFIRMED`

## 0. 控制、证据边界与结论

- fresh task-control validator：`PASS`。当前只允许 A0 分析、source audit、theoretical bound、baseline contract draft 与本地全文复核；没有运行 web/search、下载、代码、实验、adapter、MVE、提交或 push。
- 本包只回答 canonical Q1 的 A0 §2–§6。§0 已由 D008/Q1 4/4 闭合；§1/O1 理论 headroom 属 step-085，不在本包伪造。Step 3.5 的 `NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE` 只作 collision ceiling，不作可行性证据。
- **总裁决**：§2–§6 当前没有一个已被本地证据确认的致命信号，但也不能给 A0 PASS。最强风险是“小状态/全局重试/pilot/differential-FEC 已足够”与 “B2 已吸收 O1 headroom”；二者必须在另行授权的最小 defect smoke 中做 paired adjudication。
- `MDP=N/A_NON_RL`；`B2_absorption=UNKNOWN_REQUIRES_DEFECT_SMOKE`；`mission_method_delta=NONE`。

## 1. Findings first

1. **本问题不要求 ML，也未证明需要复杂优化。** 候选 action 是有限 phase class、候选 boundary、bounded segment/suffix 与 fallback 的确定性 receiver algorithm。其方法资格应来自“可观测地触发/定位 + 少算或少错 + clean no-op/fallback”，而不是状态空间大或学习泛化。若小状态 DP、pilot detector 或全局 retry 在同信息/成本下完成同一 action，C1-ext 被吸收。
2. **相邻成功先例很多，反而把增量压窄。** OFC 2014 whole-codeword Markov turbo、Tikhonov-mixture joint tracking、1704 SC-LDPC window、PAPU、OFC 2017 soft slip-state 与 2604 burst-state IBA 都证明 receiver-visible soft evidence 可改善 coded receiver；它们同时占用了泛称“decoder-aided/slip-aware/windowed/soft-state”的叙事。
3. **负面证据是机制级而非零结果。** ICTON 2016 明确显示 channel/decoder reliability contradiction 会造成 outer-loop oscillation、近 `1e-3` error floor 与错误帧 `>1000` bit；这直接否定“多一次 decoder feedback 必然增益”。
4. **strongest B2 不能冻结为一个未经正文支持的名字。** CSSC-CPE / universal CS-DC 仍为 `UNRESOLVED_FULLTEXT`，只能作 identity-level ceiling。可执行、全文承重的 B2 ladder 必须至少含：PAPU-like topology-matched pilot unwrap、OFC2017-like pilot soft-state LLR、IWCMC-like independently tuned global retry；differential-FEC/HTDD 是结构吸收对照。
5. **没有本项目 O1 分母，任何“已覆盖 90/95%”都不能作为文献事实。** 只存在 paper-internal proxies：OFC 2014 的 turbo gain `1.05 dB` 相对 3% pilot no-turbo→ideal gap `1.35 dB`，覆盖 `77.8%`、残余 `0.3 dB`；这不是 coherent-FSO Q1 的 O1。

## 2. A0 §2–§6 逐项裁决

| A0 项 | 非 ML 适配问题 | 本地证据 | 裁决 | 致命条件 |
|---|---|---|---|---|
| §2 问题结构适配 | 是否需要 deterministic local method，而非“是否需要 ML” | finite symmetry bank/global retry 已成熟；Tikhonov order 1–3 可接近 DP；PAPU/OFC2017 不用 decoder feedback | `WARNING_SIMPLE_METHOD_MAY_SUFFICE`；尚非 fatal | exact/小状态 scan 或 strongest B2 在相当预算下达到同 output、clean safety 与 fallback；C1-ext 无性能/成本第二维增量 |
| §3 相邻先例 | 同类 soft-state / decoder-assisted / local-tolerance 方法是否有成功与失败先例 | OFC2014、Tikhonov/1704、2604 为成功；ICTON 为明确失稳；PAPU/OFC2017 为 no-feedback 成功 | `PASS_PRIORS_EXIST / CROWDING_HIGH` | 不因“有先例”致命；若完整 action 只重命名已占用链，则 collision/无增量致命 |
| §4 MDP 非平凡性 | 非 DRL，不写伪 S/A/R/P；改审 finite-search triviality | boundary × symmetry candidate × fallback 是有限结构；状态数、candidate 数与合法 decoder-call 上界尚未冻结 | `MDP=N/A_NON_RL / FINITE_SEARCH_WARNING` | exhaustive/DP/global retry 在 3–7 日 testbed 上可满足相同 latency/calls，或最优策略退化为单阈值/固定 retry 且无新的 trade-off |
| §5 负面证据 | feedback/no-feedback、model mismatch、rare defect、FEC absorption | ICTON oscillation；PAPU/HTDD/differential-FEC 吸收；高 OSNR slip rare；Step1 generic C1 core exact collision | `NEGATIVE_EVIDENCE_MATERIAL`；不构成领域 Kill | 目标 slice defect 不发生；receiver metric 无增量；feedback 加剧失稳；或 FEC/B2 已消除可恢复损失 |
| §6 先验覆盖 | strongest simple ladder 对 FER/post-BER/goodput/clean/cost 的覆盖 | 可冻结方法身份与若干 paper-specific gain/cost；无同 slice O1 比率 | `UNKNOWN_90_95_REQUIRES_PAIRED_SMOKE` | primary metric `coverage_B2>=95%` 且无次指标空间；或 90–95% 后 C1-ext 仍无预冻结 practical signal |

框架原文的 §2–§4 是 ML/MDP 问法（`stages/gw-feasibility.md:57-73`）；本任务是 non-ML reference-method extension，因此保留“简单方法是否足够/策略是否平凡”的实质门，不伪造 ML 必要性。§6 的 `>=90%` 预警与 `>=95% + 无次维度` 致命线来自 `stages/gw-feasibility.md:80-85`。

## 3. 结构相似先例与差异

| 先例 | 成功/失败事实 | 与 Q1 相似处 | 关键差异 / 对 C1-ext 的含义 |
|---|---|---|---|
| OFC 2014 `10.1364/OFC.2014.M3A.3` | Markov slip trellis + LDPC soft feedback；3% pilot 下 gain `1.05 dB`，距 ideal `0.3 dB` | coded receiver、slip state、decoder soft feedback | 固定 whole-codeword turbo，无 event trigger/boundary/local action/fallback；证明 feedback 可有效，也可能把剩余 headroom 压到不足 0.5 dB（`content.md:13,29-31,307-311`） |
| ICTON 2016 `10.1109/ICTON.2016.7550341` | 1/2 inner 时 error floor 近 `1e-3`，错误帧平均 `>1000` bit；reliability contradiction 引起 oscillation；`P_CS>2e-3` 失稳 | decoder/soft reliability 与 slip 交互、rollback/stop | 未把 phase recovery 纳入 loop；其失败机制要求 C1-ext 预注册 abstain/fallback，而非假设 feedback 单调改善（`content.md:71,93-101,113,127`） |
| TCOM 2016 / arXiv 1306.3693 | limited/reduced Tikhonov mixture order 2/3 接近 DP；order-1 在 32PSK 因 recovery 也接近 DP；大幅低于 DP operations | 多模 phase trajectory、LDPC soft information、bounded mixture | 连续 full-sequence tracking + pilot recovery，无 abrupt boundary/local rollback；提示小状态近似可能已足够（`content.md:388-430`） |
| OFC2015→1704 family | slip-aware BCJR + SC-LDPC window；固定 `w=4/7/16`、等效 18 LDPC iterations/bit | slip-aware state、windowed computation、decoder exchange | window 是码图 decoding wave，不是 detected boundary；clean `gamma=0` 仍 always-on。不能以“window/local”本身作为增量（`1704.04618/content.md:900-914,950`） |
| PAPU 2019 `10.3390/app9132749` | 0.78% pilot、per 127 symbols；post-FEC gains `3/1/0.5 dB`；连续 slips 被大幅抑制 | local phase unwrap/correction、coded output、低复杂前馈 | 无 decoder feedback；离散 AWGN slips 交给 FEC；是 topology-matched strongest executable B2（`source.md:21,45,68,80-86,121-127`） |
| OFC 2017 `10.1364/OFC.2017.W2A.56` | pilots→4-state Markov soft slip probability→fully-parallel LLR；GMI gain `0.5–0.8 dB`，soft vs hard `0.3–0.6 dB` | per-symbol soft slip state、LLR action | 明确 no decision feedback，无 event boundary/local sample repair；同样可吸收 decoder-localization 以外的大部分收益（`7937400.md:43,47-53`） |
| arXiv 2604.07004 | GE burst-state BCJR + LDPC IBA；BER/PER 最多降低两数量级 | per-symbol state posterior、decoder feedback、三轮后饱和 | burst 是 innovation-variance state，不是 discrete slip；always-on full-codeword。证明 state feedback 可成功，不证明 Q1 local repair（`content.md:78,114,438-442,568,655`） |

## 4. 主动负面证据

### 4.1 strongest simple alternative 可能已够

- **PAPU-like**：完全前馈，不读 decoder；0.78% pilot、per-127、在其 fiber/QPSK slice 对连续 CS 给 3/1/0.5 dB post-FEC gain。高 OSNR `>17.5 dB` 时两方案 slip probability 已 `<1e-7`，说明合法目标 cell 可能根本无方法 headroom（`source.md:86`）。
- **OFC2017-like**：无需 decision feedback 或 sequential update，pilots+Markov transition 可并行 refine bit LLR；必须排除“decoder metric 的增量只是一个更贵的 soft slip-state estimator”。
- **IWCMC global retry**：27 个 cheap syndrome grid→5 decoder-CMF candidates→whole-frame EM；只多 5 decoder iterations，论文称为一个 EM process 的 17%（`10.1109_iwcmc58020.2023.10182805/content.md:163-217,237,267`）。若同预算 global retry 解决 affected cell，local chain 不成立。
- **differential-FEC/HTDD/SC-LDPC**：可把 slip 后果局部化或直接容忍，但付出约 20–25% coding overhead/always-on schedule。它们可能在 FER 上吸收 C1-ext，却仍留下 goodput/latency 第二维。

### 4.2 decoder feedback 可能失败或无增量

1. **model mismatch/reliability loop**：ICTON 的 channel sequence、DD 与 LDPC a-priori 相互矛盾，形成 oscillation；C1-ext 若用同一受污染 decoder evidence 排候选，可能自证错误候选。
2. **information non-increment**：TWC2004、OFC2014、1204、1704、2604 已让 decoder soft information进入 phase/state inference。只有 boundary/range、selective action、clean/fallback/cost 带来新信息或新 trade-off 才是增量；generic decoder feedback 已碰撞（Step1 v2.1=`93→66`, C1/C2 core exact, replacement=0）。
3. **FEC absorption**：PAPU 正文明确离散 AWGN slips 可由 FEC 修正；HTDD/differential/outer cleanup 把 slip 错误限制/清理。若 B0/B2 已低 FER，局部 carrier correction可能只增加 calls/false actions。
4. **rare/absent defect**：PAPU 高 OSNR cell slip `<1e-7`；JLT2020 FSO 全文不建 discrete slip，且其结果认为 turbulent phase 对 carrier sync negligible。禁止把 turbulence/fading 自动当 Q1 occurrence。
5. **small-state saturation**：Tikhonov有限阶接近 DP、2604 三轮饱和、OFC2017 fully parallel no-feedback 均提示复杂局部链可能只有很小剩余空间。

## 5. prior coverage matrix

`F`=正文事实；`U`=本项目同 slice 未知；“可能覆盖”不是 O1 比率结论。

| prior | FER / post-BER | goodput | clean safety | decode calls | latency | overhead | O1 90/95 判断 |
|---|---|---|---|---|---|---|---|
| B0 conventional CPR→decode | `U`；必须先确认 local-slip defect | 无额外 method overhead，理论上最高 | 预期 identity，但需实测 | normal pipeline，具体数待 BOM owner | `U` | 0 method overhead | **可能 95–100% only if defect absent**；这实际是 zero-headroom fatal，不是方法成功 |
| B1 global one-shot finite bank | TSP2006/global ambiguity 有效；Q1 local slip `U` | 无 pilot可选，但 candidate cost | 无 event no-op/abstain证据 | TSP turbo例：12 candidates×1 iter + winner 9 iter | 未报告 | code/pilot按实现 | OFC2014 paper-internal proxy 77.8%、residual 0.3 dB；不得外推 Q1 O1 |
| independently tuned global retry（IWCMC-like） | global constant phase/NFO 接近 EM optimum；local slip `U` | global重算可能降 throughput | always-on，每帧运行 | 27 cheap grid→5 candidate decodes；+5 decoder iterations=`17%` one EM | 未测 | 无额外 pilots；有 preamble/frame sync假设 | **高吸收候选**；同 slice ratio `U` |
| PAPU-like topology B2 | `F`：post-FEC gain 3/1/0.5 dB；连续 slips显著缓解 | pilot OH与 filter cost；但可减少长 filter | always-on pilot unwrap；false-action未量化 | downstream decode only；无 feedback re-decode | feed-forward，绝对 latency未报 | pilot 0.78% / per127 | **最可能达到 ≥90/95 的 executable B2**，但无 O1 denominator，必须 paired smoke |
| OFC2017-like soft-state B2 | `F`：GMI gain 0.5–0.8 dB；非 coded FER | pilot interval trade-off | always-on；无 abstain/fallback | one downstream FEC；no feedback | fully parallel；绝对值未报 | `N=10/20/100/200`, `M=2/3` pilots | **高吸收候选**；GMI 不能换算 O1 FER coverage |
| CSSC/CS-DC identity ceiling | 摘要声称 detect/correct；正文不可得 | `U` | threshold/false action `U` | no decoder indicated | `U` | NDA/receiver-only identity | 不能实现或量化；`UNRESOLVED_FULLTEXT`，不得判吸收/不吸收 |
| differential-FEC / HTDD / BS-LDPC / SC-LDPC | 可容忍/局部化 error event；具体 Q1 FER `U` | coding OH 显著 | always-on，无 event false action | fixed iterative schedule | 未报 absolute | 约20–25% OH，可能需 interleaver/outer code | FER 可能 ≥90%，但 goodput/latency第二维明显；需作为结构吸收对照 |
| C1-ext | 尚无数据 | 目标是只重评 touched region，可能保 goodput | 目标 clean no-op + B1/B2 fallback | 目标 bounded candidate/decode calls | 目标 bounded-local | 无新增 pilot为理想；未冻结 | 只有相对上述 max-B2 的 paired data 才可判 |

## 6. 90/95% 定义、B2 absorption kill 与 practical signal

### 6.1 统一 headroom coverage（建议合同，不是文献事实）

对 lower-is-better metric `L`（FER/post-BER/latency/calls）：

`coverage(P;L) = clamp((L_B1 - L_P) / (L_B1 - L_O1), 0, 1)`。

对 higher-is-better metric `G`（goodput）：

`coverage(P;G) = clamp((G_P - G_B1) / (G_O1 - G_B1), 0, 1)`。

分母为 0 或方向异常时不报百分比，直接记 `ZERO_HEADROOM / ANOMALY`。O1 必须是 receiver-truth-free 评估 oracle（truth只用于离线上界），不能作为 deployable best-of。

### 6.2 B2 absorption kill rule

- **框架事实**：simple prior 覆盖 primary optimum `>=95%` 且无次指标可竞争即致命；90% 是强覆盖预警（`gw-feasibility.md:80-85`）。
- **本项目建议**：在预注册 defect cells 的 paired realizations 上，取 `B2*=max(PAPU-like, OFC2017-like, global retry, differential-FEC applicable branch)`：
  1. `coverage(B2*; primary)>=0.95` 且 C1-ext 不满足任一 secondary practical signal → `B2_ABSORBS_Q1 / KILL_OR_PIVOT`；
  2. `0.90<=coverage<0.95` → 不自动 Kill，但 C1-ext 必须满足至少一个预冻结 secondary signal；
  3. primary denominator对应的 B1→O1 headroom `<0.5 dB` 或等价 practical gap → 依 FR-21 作为收尾 Kill 候选，不作为 Go 依据。

### 6.3 C1-ext practical-signal 候选阈值（**建议，非文献事实**）

满足 clean-safety gate 后，下列任一条可作为“值得进入正式比较”的务实信号；最终数值由主控与 step-085/086 合并冻结：

1. 固定 FER/post-BER 下相对 strongest B2 的 OSNR gain `>=0.5 dB`，或 paired FER relative reduction `>=10%` 且 95% cluster CI 不跨 0；
2. net goodput 相对 strongest B2 `>=5%`，已扣 pilot/coding/extra decode/rollback overhead；
3. 在 FER 非劣（建议 upper CI 不超过 5% relative regression）时，decoder-equivalent calls 或 measured latency `>=25%` reduction，形成 engineering-component 备选；
4. clean cells false action `<=1%`、net-goodput loss `<=1%`，且任何失败都确定性 fallback 至 frozen B1/B2；
5. 受影响 cell 的增益必须由 `boundary localization + bounded local action` 消融保留；若退化为 fixed retry/global bank 等效，则 method delta=NONE。

这些阈值不取代论文事实：OFC2014 的 0.3 dB residual、PAPU 的 0.5–3 dB post-FEC gains、OFC2017 的 0.5–0.8 dB GMI 与 IWCMC 的 17% extra-iteration cost只作量级锚，不能跨场景直接验收。

## 7. 必须由 defect smoke 关闭的未知项

1. **Occurrence**：合法 coherent-FSO factorized slice 下 B0/B1 是否真实出现 within-frame symmetry slip，而不是人为注入后才有问题。
2. **Headroom**：B1→O1 在 coded FER/post-BER/goodput上是否非零且实用；uncoded boundary bound不能替代 FEC结果。
3. **Observability**：receiver-visible decoder metric 是否比 receiver-only CPE/pilot metric增加 boundary/range信息；interleaver后能否映射到 touched codeword/parity ownership。
4. **B2 absorption**：PAPU-like、OFC2017-like、independently tuned global retry 与 differential-FEC适用支路在同 realization、同信息/预算下的 max envelope。
5. **Stability**：反馈是否出现 ICTON 式 reliability contradiction/oscillation；须有 abstain、rollback、fallback 和错误候选 ledger。
6. **Clean safety/cost**：no-slip cells 是否 no-op；false action、decoder-equivalent calls、latency、buffer、pilot/coding overhead 与 net goodput。
7. **Nontriviality**：exact scan/小状态 DP/固定阈值是否等价；若等价，C1-ext 只剩实现细节而非方法链。

本包不授权 smoke。只有主控合并 step-085 理论 headroom 与 step-086 source/BOM 后，另立 control decision 才可开放。

## 8. A0 B 空白零假设原料（不作 novelty closure）

| 空白可能原因 | 反驳/证据 | 当前状态与 falsifier |
|---|---|---|
| R1：pilot/differential/global turbo 已把实用问题解决，没必要做 exact local chain | PAPU/HTDD/OFC2014确实强，但分别付 pilot/coding/whole-codeword always-on cost，且多不输出 boundary/clean fallback；因此仍可能有 goodput/latency/local-cost维度 | `PARTIAL_REBUTTAL`；若 B2 envelope≥95%且无第二维，R1成立并 fatal |
| R2：decoder evidence 经 interleaving/error propagation后不能局部定位，所以前人只做 whole-codeword | 1204/Tikhonov/2604/OFC2017证明可形成 per-symbol confidence/state posterior；但它们不证明 P08-R2 mapping 保留 boundary ownership | `UNRESOLVED_SOURCE_DEPENDENT`；step-086若证明无 receiver-visible local mapping，则 fatal |
| R3：bounded change-point本质是小状态 scan/DP，学术增量太平凡 | Tikhonov有限阶接近 DP、IWCMC少量global candidates与OFC2017 fully-parallel均支持该担忧；反面是 explicit clean trigger + local calls + fallback + cost trade-off 尚未由同一链闭合 | `WARNING`；若 exact/simple search匹配输出与成本，method delta=NONE |
| R4：coherent-FSO 合法工况中 discrete local slip 极少/不存在，因此没有论文 | coherent-optical fiber有 `1e-3` order stress evidence；但JLT2020 FSO不建slip且不支持 turbulence→slip因果，PAPU高OSNR又显示 `<1e-7` | `UNRESOLVED_OCCURRENCE`；factorized defect smoke若 B0/B1无defect，直接 fatal |

三轮补检只说明 bounded slice 未确认 exact complete-chain collision；R1–R4 均未被文献彻底反驳，所以不能写“空白因没人想到”或领域 novelty closure。

## 9. Evidence pointers

- Framework：`stages/gw-feasibility.md:57-85`（§2–§6 与 90/95 fatal rule）。
- Current owner：`.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md`（CP010、UNKNOWN 与禁止实验）；`decisions.md:374-390`（D009 coverage limits/A0-only gate）。
- Corpus receipts：`projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md`（v2.1 93→66、core collision/replacement=0）；`step3_5-supplement-report.md:20-89`（三轮、全文家族、B2限制与 Step4a unknowns）。
- Direct fulltexts：
  - `papers/doi/10.1364_ofc.2014.m3a.3/content.md:13-31,131-137,307-311`
  - `papers/doi/10.1109_icton.2016.7550341/content.md:71-101,113,127`
  - `papers/doi/10.3390_app9132749/source.md:21,45,68,80-86,121-135`
  - `papers/doi/10.1364_ofc.2017.w2a.56/7937400.md:43-53`
  - `papers/doi/10.1109_iwcmc58020.2023.10182805/content.md:163-217,237-271`
  - `papers/arxiv/1704.04618/content.md:900-950`
  - `papers/arxiv/1306.3693/content.md:388-446`
  - `papers/arxiv/2604.07004/content.md:78,114,438-442,568,655`
- Structured reads：`projects/thesis-fso/worker-logs/step-070`–`step-081`；CSSC/CS-DC unresolved ceiling=`step-071-c1-cssc-universal-b2-fulltext.md`。

## 10. Final verdict

```text
A0_2_6_VERDICT                = CONDITIONAL_NO_FATAL_CONFIRMED
SECTION_2                     = WARNING_SIMPLE_METHOD_MAY_SUFFICE
SECTION_3                     = PASS_PRIORS_EXIST_CROWDING_HIGH
SECTION_4                     = MDP_NA_NON_RL_FINITE_SEARCH_WARNING
SECTION_5                     = NEGATIVE_EVIDENCE_MATERIAL
SECTION_6                     = UNKNOWN_90_95_REQUIRES_PAIRED_SMOKE
STRONGEST_EXECUTABLE_B2       = MAX(PAPU_LIKE, OFC2017_LIKE, GLOBAL_RETRY)
IDENTITY_LEVEL_B2_CEILING     = CSSC_CS_DC_UNRESOLVED_FULLTEXT
FATAL_SIGNAL_CONFIRMED_NOW    = NONE
FATAL_SIGNAL_CANDIDATES       = DEFECT_ABSENT | ZERO_HEADROOM | B2_COVERAGE_GE_95_NO_SECONDARY | NO_LOCAL_OBSERVABILITY | SIMPLE_SEARCH_EQUIVALENT | FEEDBACK_INSTABILITY
MISSION_METHOD_DELTA          = NONE
DEFECT_SMOKE_AUTHORIZED       = NO
```

