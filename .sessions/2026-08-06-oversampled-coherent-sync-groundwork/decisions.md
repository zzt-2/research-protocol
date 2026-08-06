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

> status: active
> date: 2026-08-06
> 取代：无
> 被取代：无
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
