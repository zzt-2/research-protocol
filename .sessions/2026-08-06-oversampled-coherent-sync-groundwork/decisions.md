# Decisions — 过采样相干 FSO 联合同步前端 Groundwork

## D001: 冻结新研究对象与有界 Step 1–2 路线

> status: active
> date: 2026-08-06
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-08-06 + 上游 RDL system D028 + stages/groundwork.md / gw-search.md / gw-acquire.md

### 决策

将正式研究对象扩展为含 RRC、≥2 sps、fractional timing、SCO/drift、frame offset、CFO、Wiener
phase noise 与 Gamma-Gamma fading 的相干 FSO 同步前端；本轮只执行 Phase 0、GW Step 1 与条件式
Step 2。Step 2 后停在用户覆盖面确认门。

### 理由

上游 RDL 已在 D027 确认既有 carrier-recovery caller 与本地候选源短缺；用户本轮显式选择“改变
research object”，引入真实 waveform/timing/frame 自由度。该变化必须从正式 GW Step 1 重新取证，
不能把旧 caller 缺失直接当否决，也不能跳过 Step 3/4a 直接试方法。

### 排除的替代方案

- 不自动把所有 impairment 绑成一个大而全方法；
- 不把 Tang/Wang/Fan 直接换成 FSO/GG 场景；
- 不以无来源极端参数制造问题；
- 不进入 Step 3、Step 3.5、Step 4a、实现、MVE 或仿真；
- 不把 Step 1 摘要判断写成四判据已闭合。

### 影响范围

建立本专题与独立 literature notes/coverage report；上游 system 进入 D028 scope change。仅当 Step 1
形成至少两个机制不同候选 Q# 且未触发停止条件时，才允许 Step 2 获取至少 5 篇 CORE 全文。

### 来源

S001；用户 2026-08-06 执行提示词。

## D002: 接收 Step 1 gate 与 Step 2 覆盖，停在用户确认门

> status: superseded
> date: 2026-08-06
> 取代：无
> 扩展：D001
> 被取代：D003
> 依据：S001 + Step 1 report/receipt + Step 2 coverage/receipt + testbed BOM

### 决策

接收两张机制不同的候选问题预卡进入全文覆盖：Q1 为 receiver-known preamble 驱动的 sample-level
frame/fractional-timing/CFO acquisition；Q2 为 GG fade 与 SCO 下 timing/carrier lock maintenance 和
有界 reacquisition。当时以 6 篇 CORE 判断覆盖面门达到；独立 V001 随后指出最接近的 clock/frame/FOE
直接竞品全文缺失，因此该接收结论由 D003 修正。

### 理由

六个 Step 1 停止条件均未闭合；两张预卡具有不同输入、动作与失败机制。全文核查显示 Tang 2022、
Wang 2023 与 OE 2024 已覆盖 frame+CFO，但在 1 sps 或下采样后工作，不包含同等 sample-level
fractional timing/SCO 动作；这只排除当前证据池内的 exact collision，不等于新颖性成立。Q2 仍缺双环
共同失锁与恢复增益的量化证据，必须保留为预卡。

### 排除的替代方案

- 不把“帧同步+CFO”包装为新贡献；
- 不用元数据替代未获取的 JLT 2025 直接竞品全文；
- 不把设计/仿真参数误写成外场测量；
- 不因 CORE 数量达标而声称四判据闭合或进入方法设计。

### 影响范围

该段为被 D003 取代的历史影响范围：当时计划确认当前文献池，或补充/替换 Gu 2019、OE 2022、
JLT 2025 等全文；Step 3、Step 3.5、Step 4a、实现与仿真禁止。

### 来源

S001；`projects/thesis-fso/oversampled-sync-groundwork/step1-search-report.md`；
`projects/thesis-fso/oversampled-sync-groundwork/step2-coverage-report.md`。

## D003: 补齐最近直接竞品后重裁 Step 2 为用户确认门

> status: active
> date: 2026-08-06
> 取代：D002
> 被取代：无
> 依据：V001 FAIL + direct-competitor acquisition receipt + 修订后的 Step 2 coverage/receipt

### 决策

JLT 2025 DOI `10.1109/JLT.2025.3533197` 的官方 arXiv `2409.14400` 全文补入第 7 篇 CORE，满足
“最接近拟议联合方法的直接竞品”角色。重新固定 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。
JOCN 2026 在三路径止损后仍无全文，作为 `UNRESOLVED_HIGH_RISK` 显式交由用户决定是否接受，不能在
Step 3 或任何新颖性 claim 中静默忽略。

### 理由

JLT 2025 的同一 burst preamble 支撑 clock/frame/frequency 的泛化表述已经占用，但全文显示 clock
recovery 使用 TS-A/Godard，frame synchronization 与 FOE 使用 TS-B，属于顺序、分区动作且未覆盖 SCO；
因此当前没有证实 Q1 的同信息—同动作—同任务完全碰撞。JOCN 2026 官方摘要更接近同一 preamble 的
clock/frame/FOE 三动作，全文缺失使 exact collision 仍不可裁决，故只能停在用户覆盖面确认门。

### 排除的替代方案

- 不再用 OE 2024 的“同场景”替代最接近动作竞品；
- 不把 JLT 2025 的顺序处理误写成联合 fractional timing/SCO 方法；
- 不据 JOCN 摘要宣称碰撞或新颖性；
- 不因补齐角色 5 而自动进入 Step 3。

### 影响范围

Step 2 CORE=7；用户确认项明确包含 JOCN 2026 全文缺口。RDL control、master-state 与专题索引同步到
D003；V001 保留为失败历史，需 fresh-context V002 复验后才能提交。

### 来源

S001；`independent-verifier-report.md`；`direct-competitor-acquisition-receipt.json`；
`step2-coverage-report.md`。

## D004: 接受 7 篇 CORE 并授权 Step 3→条件式 Step 3.5

> status: active
> date: 2026-08-06
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-08-06 + 验证: V003 + `step2-coverage-report.md`

### 决策

接受当前 7 篇 CORE 覆盖面，允许进入 GW Step 3；只有至少一个 Q# 通过 canonical 四判据，才继续
Step 3.5。完成 Step 3.5 后停止，不进入 Step 4a、方法实现、testbed 或仿真。

### 理由

V003 已核验 7 篇 CORE 的身份、正文质量和 provenance。JOCN 2026 全文仍缺，但用户明确接受其作为
Q1 的 `HIGH_RISK` novelty/collision blocker：该缺口不阻止正文精读，却限制 Q1 的 claim ceiling。

### 排除的替代方案

- 不等待 JOCN 2026 无限重试后才开始 Step 3；
- 不用 JOCN 2026 abstract 冒充全文裁决；
- 不把 Step 3 survivor 称为 `METHOD_SIGNAL`、Go 或论文方法成立；
- 不在本轮越过 Step 3.5 进入 Step 4a 或任何实现/实验。

### 影响范围

更新本专题 scope boundary、literature notes 的 GW 进度与 registry 当前状态；Step 3.5 对 JOCN 2026
仅做有界重试。若仍失败，Q1 不得宣称 exact-action novelty closure。

### 来源

S001 续接；用户 2026-08-06 主控裁决。

## D005: Step 3 无 canonical survivor，禁止触发 Step 3.5

> status: superseded
> date: 2026-08-06
> 取代：无
> 被取代：D006（仅取代 terminal 与 Q1/Q2 判据 1；其余事实和边界保留）
> 依据：调研: `step3-deep-read-report.md` + worker logs A/B/C + `stages/glossary.md`
> 触发原话：无（技术推导）

### 决策

Q1、Q2 均未通过 canonical 四判据，Step 3 terminal 固定为 `STEP3_NO_VALID_PROBLEM`。D004 的
Step 3.5 条件门未满足，故不执行定向检索、引用链筛查或 JOCN 2026 新一轮获取。

### 理由

Q1 有 2019+ 强顺序 comparator 与可量化产出形态，但 CORE 没有证明该链在目标 C 下因具体 A 失效；
Q2 没有共同失锁/cheap comparator 不足的正文证据，也没有 2019+ integrated baseline。两者均不能把
待证假设或跨论文拼接当成 canonical 问题。

### 排除的替代方案

- 不把 Q1 的共享 preamble、框图合并或模块调序写成真正联合动作；
- 不把 Q2 的单环 fade 失稳与独立 timing 结果拼成共同失锁事实；
- 不因 JOCN 2026 仍有风险而跳过 survivor 门直接做 Step 3.5；
- 不把“方法产出形态可想象”替代判据 1/3 的证据缺口。

### 影响范围

本专题停在 Step 3；无 Step 4a 入口、METHOD_SIGNAL、Go、方法实现、testbed 或仿真授权。JOCN 2026
继续保留 `UNRESOLVED_HIGH_RISK`，但当前 terminal 由更上游的 canonical FAIL 决定。

### 来源

S001 续接；`projects/thesis-fso/oversampled-sync-groundwork/step3-deep-read-report.md`。

## D006: Step 3 canonical 语义门纠偏并启动 Q1 Step 3.5

> status: active
> date: 2026-08-06
> 取代：D005 的 terminal 与 Q1/Q2 判据 1 结论
> 被取代：无
> 依据：用户原话: voice.md 2026-08-06 + 对照: `.sessions/2026-08-02-fso-amc-groundwork/decisions.md` D005 + `stages/glossary.md` L22-31 + `stages/gw-read.md` + `stages/gw-supplement.md`

### 决策

D005 将“CORE 尚未量化证明 baseline M 在条件 C 下因 A 失效”当作 canonical 判据 1 FAIL，错误地把
Step 4a/MVE 的 problem-truth 责任前移至 Step 3。Canonical 判据 1 只要求 M/C/A 明确、句子级、可解；
Step 3 要求 A 可证伪，不要求 A 已被实验或 MVE 证实。按 owner 重判：Q1 四项均 PASS，成为
`STEP3_SURVIVOR` 并立即进入 Step 3.5；Q2 判据 1 改为 PASS，但判据 3 仍 FAIL，故不成为 survivor。
当前过渡 terminal 为 `STEP3_5_IN_PROGRESS_Q1_SURVIVOR`。

### Canonical 四判据重判

| Q# | M/C/A | 判据 1 | 判据 2 | 判据 3 | 判据 4 | Step 3 verdict |
|---|---|---|---|---|---|---|
| Q1 | M=`Le Bidan 2-sps 顺序 acquisition chain + Sun/Wang frame–FOE`；C=`RRC、≥2 sps coherent FSO，fractional timing、frame、CFO 同时未知`；A=`顺序 timing-first 处理在同时未知状态下可能传播误差或产生错误峰/误锁` | PASS：M/C/A 明确、句子级、可解且 A 可证伪；不要求已有 MVE 证明 | PASS：joint/coarse-to-fine estimator 或 design rule | PASS：Le Bidan 2023 + Sun/Wang 2019+ task-matched comparator | PASS：acquisition、误锁、估计误差、BER、开销、时延、复杂度 | `STEP3_SURVIVOR` |
| Q2 | M=`timing/carrier 独立 maintenance/reacquisition`；C=`≥2-sps RRC coherent OSL，SCO/PN/CFO + dynamic deep fade`；A=`fade 可能使双环共同/异步失锁且廉价 shared-freeze/fixed-restart 可能不足` | PASS：M/C/A 明确、句子级、可解且 A 可证伪；“共同失锁尚未实验证实”不属于 Step 3 FAIL 理由 | PASS：shared-confidence FSM / lock rule | FAIL：现有 Gu/Paillier/Valjus 仅为 timing、carrier 或综述，跨论文拼接不能构成 2019+ integrated baseline M | PASS：error/slip/BER/recovery time | 非 survivor |

### 保留 D005 中继续有效的事实与边界

1. 7 篇 CORE 全文精读与 identity/provenance/read-note 事实；
2. baseline/action/information/timing 边界；
3. generic shared-preamble/resource reuse、框图合并或模块调序不构成真正 joint estimator；
4. JOCN 2026 (`10.1364/JOCN.587273`) 全文缺失为 exact-action novelty/collision blocker；
5. Q1 最强廉价 comparator 必须包含 polyphase/Farrow timing bank 与 sequential Le Bidan/Sun/FSTS/STSB chain；
6. 禁止 Step 4a、方法实现、testbed、MVE、仿真、METHOD_SIGNAL/Go/论文方法 claim。

### 理由

`stages/glossary.md` L28 的判据 1没有“失效已被量化证明”要求；`gw-read.md` 要求的是具体、可证伪的
失效假设，实证闭合属于后续 Step 4a。AMC Groundwork D005 已对同一错位作出确定性纠偏：把
`problem_truth`/“A 已证明”当 Step 3 terminal gate 会形成循环门控。Q1 原判据 2/3/4 已 PASS，因此
移除错误的判据 1附加要求后必须成为 Step 3 survivor。Q2 不能因同一语义错误继续 FAIL 判据 1，但其
判据 3是独立 baseline 身份问题，不能随判据 1纠偏而自动通过。

### 排除的替代方案

- 不继续沿用“正文未证明失效/MVE 未跑”作为 Step 3 判据 1 FAIL；
- 不把 Step 3 survivor 写成 Go、METHOD_SIGNAL 或问题已在 Step 4a 被证实；
- 不把 Q2 的多篇单环文献拼成 integrated baseline；
- 不因 JOCN 全文缺失而跳过有界 Step 3.5，也不以摘要完成 exact-action 裁决；
- 不推翻 D005 所记录的 7 CORE 事实、动作边界与实现/仿真禁令。

### 影响范围

`step3-deep-read-report.md`、`literature_notes_oversampled_sync.md`、V004、H001、topic-index、master/RDL
current state 需按该血缘纠偏。Step 3.5 限于最多三轮关键词矩阵、最高相关竞品双向引用链、JOCN 有界
获取以及高相关新论文 acquire→read；完成后必须停止在新的 Step 3.5 terminal，不进入 Step 4a。

### 来源

S001 续接；用户 2026-08-06 确定性语义纠偏指令。

## D007: 完成 Q1 Step 3.5 并冻结 exact-action 全文 blocker

> status: active
> date: 2026-08-06
> 取代：无
> 扩展：D006
> 被取代：D008（仅 terminal 与 blocker 数量/处置）
> 依据：调研: `step3-5-supplement-report.md` + T005–T011 worker logs + Sun 双向引用链 + 3 篇新增全文 read notes
> 触发原话：无（技术推导）

### 决策

Q1 完成 Step 3.5 后仍为 `STEP3_SURVIVOR`。两轮检索已收敛，当前全文池没有同信息、同动作、同任务的
joint `(frame index, fractional τ, CFO)` estimator；但 JOCN 2026 `10.1364/JOCN.587273` 与 JLT 2025
`10.1109/JLT.2025.3581618` 仍缺全文，exact-action novelty closure 保持 blocked。正式 terminal 冻结为
`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`。Q2 仍因判据 3 FAIL 而非 survivor。

### 理由

Round 2 真正新增 must/should=0，检索充分性达到收敛门；Sun 2025 双向引用链完整。新增全文证明：
Zhou 2025 是分区 preamble 的顺序链；LPT 2017 joint 解 integer frame+CFO、无 fractional τ；JLT 2021
joint 解 τ+CFO+CPO、无 frame 且 task/waveform 不匹配。它们关闭 generic 方法先例和最强顺序 comparator，
但都不是 exact collision。两个 primary direct candidates 无全文，故不能把“未确认碰撞”升级成新颖性闭合。

### 排除的替代方案

- 不把 shared preamble、多模块框图或 module ordering 称为 true joint action；
- 不把 LPT 2017/JLT 2021 的窄 joint 输出扩写成 exact 三参数 collision；
- 不用 JOCN/JLT IQ-skew 摘要裁 exact jointness；
- 不因 Step 3.5 收敛而自动进入 Step 4a、实现、testbed、MVE 或仿真；
- 不把 strongest cheap comparator composite 伪称为单篇 baseline identity。

### 影响范围

更新 Step 3 report、literature notes、topic/master/RDL current state；写 V005/H002。下一合法动作仅为
补齐/显式接受两个 primary-fulltext blocker；之后另起会话重读 `gw-feasibility.md` 再讨论 Step 4a。

### 来源

S001 续接；`projects/thesis-fso/oversampled-sync-groundwork/step3-5-supplement-report.md`。

## D008: 接收用户提供 JLT 2025 全文并关闭 coverage-decision gate

> status: active
> date: 2026-08-06
> 取代：D007 的 terminal 与两个 primary-fulltext blocker 计数
> 扩展：D007 的 action/collision 边界
> 被取代：无
> 依据：用户原话: voice.md 2026-08-06 + 全文精读: T013 worker log/read note + PDF identity/SHA/render receipt

### 决策

用户提供的 JLT 2025 IQ-skew 全文 `10.1109/JLT.2025.3581618` 已完成 acquire→read。正文证明它是
shared-preamble 上的顺序多模块 DSP：TS-A 承载 frame detection、IQ-skew、SOP、timing recovery 与
FOE，TS-B 再做 frame synchronization/channel estimation；IQ-skew 由独立 tone/Godard phase detector
输出。不存在单一 `(frame index, fractional τ, CFO)` objective/search，故 verdict=`NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`。

JLT blocker 已消解；JOCN 2026 `10.1364/JOCN.587273` 仍无全文。用户明确“我拿不到就是拿不到了”并
只取得 JLT 一篇，因此 JOCN 记为 `USER_CONFIRMED_FULLTEXT_UNAVAILABLE`，停止任何获取重试。该用户
coverage decision 关闭工作流 blocker，但不等于 JOCN action 已被全文裁决，也不支持 exact-action
novelty/“首次”声称。新 terminal 为
`STEP3_5_COMPLETE_Q1_SURVIVOR_JOCN_FULLTEXT_UNAVAILABLE_NO_CONFIRMED_EXACT_COLLISION`。

### 理由

Fig. 2、§II-A 与 Eq. 16–23 显示多个 output 共享训练资源但各自由不同模块/metric 顺序产生；摘要的
“simultaneously enables”不能替代 estimator coupling 证据。用户已用其可用访问权完成最后一次人工
获取并确认另一篇不可得，继续重试没有合法信息增量。覆盖面门可按“显式接受已知缺口”处置，但科学
claim ceiling 必须永久保留 JOCN 未读限制。

### 排除的替代方案

- 不把 shared TS-A、多模块列表或零额外 skew overhead 称为 joint 三参数 estimator；
- 不因 JLT 无 exact collision 就宣称 novelty closure；
- 不再重试 JOCN、绕过访问控制或用 abstract 裁 jointness；
- 不在本轮进入 Step 4a、实现、testbed、MVE 或仿真。

### 影响范围

更新 literature notes、Step 3.5 report、H002、topic/master/RDL current state。formal topic 仍 closed；
下一合法动作是在新会话重读 `stages/gw-feasibility.md`，只讨论是否进入 Step 4a，不自动转阶段。

### 来源

S001 续接；T013；`projects/thesis-fso/worker-logs/step-3-5-jlt-iq-skew-fulltext-read.md`。

## D009: 受限重开 Q1 Step 4a preflight discussion

> status: active
> date: 2026-08-07
> 取代：无
> 被取代：D011（仅 semantic-smoke 执行禁令）
> 依据：用户原话: voice.md 2026-08-07 + H003 + D006–D008 + `stages/gw-feasibility.md`

### 决策

将已关闭专题仅为 Q1 的 Step 4a preflight discussion 受限重开。本轮范围只包含 A0 §0–§6、A′/A/B
竞争分析和维度 D 的 ≤1 天 deterministic semantic smoke 设计；不执行 semantic smoke/MVE，不建
5.5–7.5 日 acquisition testbed，不实现方法、不跑仿真。Q2 保持非 survivor，不进入本轮。

本轮仍禁止修改 `common/`、`params.py`、旧实验、Skill 或四个 `p05_run*.log`，禁止 push；只在所有
文档与独立验证完成后做一次 commit。

### 理由

H003、RDL D032/control 与 master-state 已把“新会话重读框架并做 Step 4a preflight discussion”登记为
唯一下一合法动作；用户本轮给出显式授权和更窄边界。旧 topic-index 的“明确不含 Step 4a”属于上轮
Step 3.5 的冻结范围，必须用范围变更记录解除 discussion 层禁令，而不能静默越界。

### 排除的替代方案

- 不沿用 closed topic 的旧范围直接写 Step 4a 结论；
- 不把 preflight discussion 解释为正式 Step 4a、Go、Conditional Go 或 MVE 授权；
- 不讨论 Q2，不顺手搭平台或实现 B0/B1/B2/C；
- 不因用户要求实验设计就实际运行任何脚本。

### 影响范围

新增 S002 与 `step4a-preflight-discussion.md`；更新 topic-index、voice、registry、master/RDL current state。
本轮完成后专题重新 closed，等待用户决定是否授权 semantic smoke。

### 来源

S002；用户 2026-08-07 明确执行范围。

## D010: Q1 preflight 终态为 EVIDENCE_GAP 并冻结 semantic smoke 合同

> status: active
> date: 2026-08-07
> 取代：无
> 被取代：D011（仅 awaiting-approval gate）；D012（preflight terminal）
> 依据：分析: `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md` + 调研: `literature_notes_oversampled_sync.md` / `step3-5-supplement-report.md` / `testbed-bom.md` + critic: `projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-independent-verifier-report.md`
> 触发原话：用户原话: voice.md 2026-08-07

### 决策

Q1 通过 A0 §0，但当前 Step 4a preflight 终态冻结为 `STEP4A_PREFLIGHT_EVIDENCE_GAP`。本候选默认是
传统解析/DSP estimator，不预设 ML；B0/B1/B2/C 的 receiver-visible input 均为同一 receiver-known
preamble samples，唯一主要贡献维度为 `wrong-basin false-lock rate`；本 smoke 的 `miss=N/A`。

当前不能推荐正式 micro-MVE，原因是：(1) 没有 B0/B1/B2 相对 visible-only global joint oracle 的差距
数字或稳定错误峰区域；(2) 若 B1 在 timing bank 上使用与 C 相同的全局 likelihood，二者在离散网格上
可能数学等价，C 相对增强传统 baseline 的不可替代结构增量尚未成立；(3) 顺序链近似最优、联合收益小、
preamble 参数近似正交和 coarse preprocessing 已解耦四个零假设均未被反驳；(4) 本地材料未完成专门的
coupled-acquisition 负面证据搜索，A0 该项仍为 `EVIDENCE_GAP`。

冻结 `step4a-preflight-discussion.md` §4 的 ≤1 天 deterministic semantic smoke 合同。只有后续用户显式
批准后才可派子 agent 执行；本决策本身不授权运行。

### 理由

一般 RRC preamble likelihood 对 frame index、fractional timing 与 CFO 非可分，但“解析上非可分”不等于
目标 preamble/coarse-CFO 工作点有足够数值耦合。B1/B2 是 FR-03/FR-01 要求的增强传统 baseline，必须
先排除其对 joint gain 的廉价吸收。现有材料明确把强顺序链失效留作 Step 4a 待证假设，不能用
“无人 exact collision”替代 problem-truth。

### 排除的替代方案

- 不把“A 尚未被 MVE 证明”重新当前门；Q1 已合法进入 A0；
- 不硬套 ML、MDP 或 RL；不把有限维估计问题包装成学习问题；
- 不以一般 likelihood 非可分直接推荐 micro-MVE；
- 不因没有现成数字而拍 ≥5%/≥15% headroom；
- 不把 JOCN 不可得当无碰撞证据，也不声称“首次”；
- 不给 Go/Conditional Go，不建正式 testbed。

### 影响范围

formal topic terminal、RDL foreground control、master-state 与 handoff 更新为等待用户批准 semantic smoke。
若 smoke 显示 objective 可分、B1/B2 覆盖 ≥95%、无稳定错误峰或 joint 上界 <5%，转
`STEP4A_PREFLIGHT_KILL_OR_PIVOT`；只有非可分且存在 B1/B2 不能廉价吸收的稳定差距，才可转
`STEP4A_PREFLIGHT_RECOMMEND_MICRO_MVE`。

### 来源

S002；`projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-discussion.md`。

## D011: 用户批准执行受限 deterministic semantic smoke

> status: active
> date: 2026-08-07
> 取代：D009 的 semantic-smoke 执行禁令；D010 的 awaiting-approval gate
> 扩展：D010 的 ≤1 天 semantic smoke 合同
> 被取代：D012（execution/result gate）
> 依据：用户原话: voice.md 2026-08-07 + 验证: V007 + H004
> 触发原话：用户原话: voice.md 2026-08-07

### 决策

用户以“执行”明确批准运行 D010/H004 已冻结的 ≤1 天 deterministic semantic smoke。专题受限恢复为
active，只允许 Groundwork Step 4a 维度 D 的 Probe：执行前完成本地负面证据有界核查与参数来源清单，
随后用同一 paired realization 比较 B0/B1/B2/C-oracle，执行 identity、truth-isolation、score-comparability
和真实计算量门控，并按 D010 的三个科学终态裁决。

本授权不等于正式 MVE、Go/Conditional Go、testbed、方法实现或仿真平台建设；不授权新 Web 检索。
新 Web 检索如确有必要，须另获用户授权并由子 agent 执行。

### 理由

D010 已把当前不确定性压缩为一个可由 ≤1 天 Probe 回答的语义问题，V007/H004 已独立确认合同可执行但
尚未运行。用户已越过 H004 记录的唯一人工批准门，因此可以解除等待状态，但不能扩大已冻结的 waveform、
比较对象、主要指标或退出阈值。

### 排除的替代方案

- 不把“执行”解释为正式 MVE、完整 Step 4a Go/No-Go 或 Step 5 入口；
- 不建 5.5–7.5 日 acquisition testbed，不接入 production runner；
- 不修改 `projects/simulation/common/`、`params.py`、旧实验、Skill 或四个 `p05_run*.log`；
- 不讨论 Q2，不引入 ML，不扩 seed/cell 规模来追逐正结果；
- 不 push；本对话仍只做一次最终 commit。

### 影响范围

新增 S003、受控 T015、临时 Probe 实现/测试/结果与 worker log；formal topic、master-state 与 RDL control
从 awaiting approval 切换到 authorized/preparing。执行结果须由独立 verifier 验收后，主控才能建立新的
科学 terminal、V/H 与下游建议。

### 来源

S003；用户 2026-08-07 明确回复“执行”。

## D012: Q1 Step 4a preflight Kill/Pivot，不进入正式 MVE 或 testbed

> status: active
> date: 2026-08-07
> 取代：D010 的 `EVIDENCE_GAP` terminal；D011 的 Probe execution gate
> 扩展：D010 的方法身份、单一指标、阈值与 claim ceiling
> 被取代：无
> 依据：T015 artifacts + `semantic-smoke-report.md` + 验证: V008 / T016
> 触发原话：无（技术验证结论）

### 决策

Q1 Groundwork Step 4a preflight 正式终态冻结为 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`。不得建立正式 MVE、
5.5–7.5 日 acquisition testbed，不进入 Step 5、Contract 或 Execute。

本次 Probe 的四项 semantic gates 全 PASS；但 operational B1 timing bank 与 C-grid 在 180/180 cells 上使用
相同 receiver-visible input、候选集、normalized GLRT、窗口与 lexicographic tie-break 后 exact-equivalent。
noiseless residual 中四法均 0/75 false locks；-6 dB diagnostic residual 中 B0/B2=58/75、B1/C=59/75，
C 相对 B0 的 `G_C=-1.7241%`；两层均无可用正 headroom，B0 也没有稳定相邻 2×2 wrong-basin 区。
surface 数值非 exact-separable，但该耦合没有形成 C 相对 B1/B2 的不可替代动作增量。

### 理由

D010 的任一硬退出已满足：B1/C common-grid exact equivalence；noiseless B0 零 false lock；没有稳定 2×2
错误盆；C 的主指标改善低于 5%（noiseless 0%，-6 dB 为负）。继续建 testbed 只会扩大一个已被廉价
hypothesis bank 吸收的搜索实现问题，不能支撑“coupled estimator”独立方法贡献。

### 排除的替代方案

- 不把一般 likelihood 非可分或 AIR 非零解释成方法可行性；
- 不以换 preamble、扩 seed、加更低 SNR 或更细 grid 追逐正结果；
- 不把 B1/C 的有限网格等价外推成连续 estimator 等价；
- 不把 deterministic grid false-lock frequency 外推为外场概率或论文数字；
- 不将“工程组件”直接包装成独立方法节。若以后转 latency/complexity，必须作为新的 M-C-A 问题重新过
  Step 1–4a，并证明相对 B1/B2 的 caller-path 结构增量；不能沿用本 Q1 的方法 claim。

### 影响范围

formal topic 关闭；Q1 不再拥有 semantic-smoke、正式 MVE 或 testbed 入口。Probe 代码/artifacts 只保留为
negative-evidence receipt。RDL 转为等待用户决定“归档 Q1”或“另立 complexity pivot 问题”；两者都不是
自动授权。

### 来源

S003；T015；V008；`projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-independent-verifier-report.md`。
