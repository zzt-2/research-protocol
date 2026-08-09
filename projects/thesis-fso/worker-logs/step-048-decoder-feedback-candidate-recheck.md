# Step 048 — Candidate recheck

> 2026-08-09 | T002 | `PORTFOLIO_MAP` | local-only / design-only
> task-control validator: `PASS`
> 边界：未做外部检索、未实现、未运行实验；只写本 worker-log，不修改 owner/source/artifact。

## Current contribution/dead-end map

1. **Ch3 与 Ch5 已有真实动作，Ch4 方法槽仍开放。** CCISP 的方法动作是 receiver-visible statistic 驱动 DA/NDA 分支选择；Ch5 工程方法把同一 command 提前为“只执行被选分支”，没有改变 selector 或恢复估计器（`projects/thesis-fso/direction-lab/harvest/ccisp-select-before-execute-single-branch-method-package.md:39-72`）。因此 decoder-feedback 候选必须改变 decoder 之后的 CPR/recovery 决策，不能只是再命名一个 selector、调参数或安排执行顺序。
2. **P08-R2 是可复用 corrected coded-chain，不是方法正证据。** 当前 authority 将其定为 `STOPPED_WITH_PARTIAL_ASSET`：prefix-LS、receiver-visible noise/MMSE、metamorphic/AST 与公平账本可复用，但 coded-LLR 科学包因 chronology 缺陷不能升级（`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3089-3105`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:4007-4033`）。现 caller 只做一次 equalize→demap→decode；B0/B1/B2 的动作止于 global sigma、temperature、clip/decoder normalization/offset（`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py:150-194`; `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_run.py:65-74`）。
3. **F4-A 不能给 decoder-feedback 提供稳定正上界。** corrected analytic GMI 仅 `+0.008907 bits/sym`，且 smoothing=2/8/32 时为 `+0.0331/+0.0102/+0.0032`，最后一档 CI 跨 0；authority 是 BOUNDARY，不是 Kill，也不是方法信号（`.sessions/2026-07-20-direction-lab-science-scout/decisions.md:880-900`; `.sessions/2026-07-20-direction-lab-science-scout/verifications.md:384-401`）。
4. **CRC/final-label repair 已有明确 dead end。** H1 的 CRC 翻标签把 fixed BER 从 `0.4996` 降到 `8.936e-5`，但精确等于既有 PI-BER 消歧，所以“最终 CRC 后挑排列/翻标签”被否为独立方法（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:2292-2304,2317-2334`）。
5. **generic detection→recovery 已在历史候选域出现。** D047 只到 observation-only 侦察：先要求检测早于 failure，再决定 relock/DD/state-switch，且保留 baseline/oracle/no-event 对照；它没有形成既有方法，但构成动作族碰撞（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:2708-2731`; `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md:465-482`）。D028 进一步只否决“检测后回滚历史 equalizer snapshot”：近期 snapshot 已在 swap 盆地，早期 snapshot 随持续 SOP 过时，dwell 中位 11 块或 BER `0.0176→0.1226`（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:1591-1617,1631-1646`）；它不等价于否决当前帧重新估计的 phase update。
6. **P05 是必须处置的 cheap alternative，但其结论有条件边界。** corrected standard-CMA continuation 在该 dual-pol swap slice 把 fixed-label BER 恢复到 `0.00018/0.00117`，故该对象被 conventional online equalizer 解决（`projects/thesis-fso/worker-logs/step-032-p05-ml-ood-online-adaptation.md:52-74,88-96`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2676-2697`; `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md:3688-3705`）。该事实要求 decoder 候选先证明缺陷没有被 hard-DD/CMA 吸收，但不能跨场景臆推为所有 coded CPR defect 均已解决。

## Card-by-card matrix

| field | C1 — Decoder-aided finite phase-hypothesis re-evaluation | C2 — True-extrinsic soft-symbol CPR update | C3 — Syndrome-triggered bounded recovery |
|---|---|---|---|
| 具体 M-C-A | **M**：single-pass CCISP/coded receiver 在 decoder evidence 出现前固定相位假设；**C**：有限相位模糊/cycle-slip 仍处于可译码、且 front-end likelihood 不能可靠区分；**A**：early decoder consistency 对冻结有限假设集重评分，只允许一次 switch/keep。 | **M**：single-pass CPR→demap→decode；**C**：残余 phase/CFO 在 decoder 可纠正区内，hard/front-end statistic 对 CPR 更新噪声大；**A**：以真正 `L_ext=L_post-L_apriori` 形成 soft symbol，做一次连续 phase/CFO state update。 | **M**：CCISP 单分支后无 decoder-failure 控制；**C**：部分可恢复 slip/错误锁定在早期 syndrome trajectory 中先出现；**A**：early syndrome predicate 触发一次 relock-and-hypothesis-switch。 |
| deployable input→action→output | receiver-visible early extrinsic/syndrome score per current-frame hypothesis → one finite hypothesis switch/keep → re-demapped LLR、final bits/FER、switch receipt。禁止 TX truth/true phase/最终正确性择优。 | receiver-visible posterior 与 a-priori → deinterleave/map 为 soft-symbol mean/reliability → one weighted phase/CFO update → re-demapped LLR、final bits/FER、state-delta receipt。 | receiver-visible early syndrome/CRC trajectory → one frozen recovery command → final bits/FER、trigger lead-time、recovery/latency receipt。 |
| decoder runtime 时点 | 第一段 BP iteration 结束、最终 bits 产生前；在一次 hypothesis switch 与第二次 demap/decode 之前。当前 decoder `hard_out=True`，公开面只在 full decode 后回 hard bits/configured-iteration diag（`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:123-175`）。 | 第一段 BP 后读取 posterior/extrinsic，严格在一次 CPR update 前；第二段用剩余总 iteration budget。当前接口无 posterior/extrinsic，也无 resumable iteration callback。 | 冻结 early iteration checkpoint，必须早于 final decoder outcome；若改成 next-block action，须另冻 state lifecycle，不能在本卡中混用 same-frame/next-block。当前接口无 syndrome trajectory/callback。 |
| 实际改变的 CPR/recovery 决策 | 在当前帧冻结 hypothesis bank 中改变一次 phase hypothesis；不回滚历史 equalizer state。 | 连续改变一次 phase/CFO estimate/state；不是 LLR scalar、threshold 或 branch schedule。 | 改变一次 relock/hypothesis-switch command；由于该动作与 C1 和 D047 同族，本卡没有独立 action identity。 |
| P08/F4/P05/CCISP/turbo/CRC 碰撞 | 不等于 P08 scalar calibration；若 final CRC 后挑最好即撞 F4-C/D039；不等于 CCISP 前置 DA/NDA gate，但“检测→state-switch”撞 D047。不得采用 D028 stale snapshot。P05 仅在同 swap slice 是 must-beat cheap alternative。decoder-aided phase-hypothesis/turbo competitor **未检索、unknown**。 | 若只改 temperature/clip/offset即撞 P08 B1/B2/F4-A；若退化 hard-DD/CMA 即被 P05 cheap alternative 吸收；真实 continuous CPR update 与 CCISP gate/Ch5 schedule 不同。iterative/turbo carrier-recovery exact competitor **未检索、碰撞风险高**。 | trigger 信息虽不同，但 action 与 D047 detection→relock/state-switch、C1 one-switch 同形；final CRC repair 撞 D039/F4-C；rollback 撞 D028；仅报告 failure 是 monitoring，不是方法。CRC-aided slip/recovery direct competitor **未检索、unknown**。 |
| strongest conventional comparator | 同一 hypothesis bank、相同额外 front-end 调用与总 BP/latency budget的 **receiver-only likelihood phase-hypothesis selector**；具体传统实现身份 `unknown`，须 Step 1 冻结。 | 同一次 update、同额外 front-end调用和总 BP/latency budget的 **hard/soft decision-directed iterative CPR**；具体传统算法/公式 `unknown`，须 Step 1 冻结。 | 同一 recovery action/budget、由 receiver-only front-end confidence 触发的 causal relock；具体实现 `unknown`。 |
| strongest cheap alternative | corrected single-pass coded chain 的 B2（clip + normalization/offset）叠加原 CCISP/no-feedback；统一 caller 尚不存在。若 defect 是 dual-pol swap，另加 corrected standard-CMA continuation。 | hard-DD/receiver-only weighted phase update + P08-R2 B2；若目标落到 equalizer swap，standard-CMA continuation 必须进入 ladder。现仓库无统一 caller，不能写成已跑。 | 原 CCISP/no-feedback + P08-R2 B2；若是 swap，再加 standard-CMA continuation。final CRC flag 只能是监测/下界，不是公平 causal recovery comparator。 |
| 最小 adapter（不实现） | soft/syndrome evidence 面；冻结 hypothesis bank；分段/可恢复 decoder；one-switch controller；code/net-rate/BP/front-end/latency ledger；no-feedback identity/metamorphic gate。3–7 天是否足够仍须 T003/readiness 证据，不在本包认定。 | soft-output/posterior 与 a-priori 面；真实 extrinsic 差分；coded-bit→symbol 反映射；一次 CPR callback；分段 decoder；固定总预算 ledger 与 no-feedback identity。3–7 天可行性未由本包验证。 | syndrome trajectory + causal timestamp；一次 recovery controller；same-frame 或 next-block lifecycle 二选一；公平 ledger。即便接口可建，独立 action collision 仍未解除。 |
| 主图 / 承重消融 / fallback | 图：gate→branch→hypothesis bank→early BP evidence→switch/keep→final decode 时序；消融：decoder-evidence vs receiver-only likelihood，在同 bank/预算下；fallback：若动作无增量，仅保留 coded-interface/negative，不成章。 | 图：两轮 unfolded decoder↔CPR chain + FER/phase-error 随 impairment；消融：true-extrinsic vs posterior-as-extrinsic vs hard-DD，同预算；fallback：若 hard-DD 等价或无 defect，仅作 feedback boundary/supporting。 | 图：NORMAL→EARLY_CHECK→ONE_RECOVERY→FINAL；消融：syndrome vs front-end trigger vs final-CRC-only；fallback：monitoring/false-trigger boundary，不能占方法章。 |
| 当前分类 | **`HYPOTHESIS_ONLY` / KEEP PROVISIONALLY**。旧 asset-budget 拒绝被 D001 放宽，但动作新颖性与 direct competitor 均未闭合；只能进 Step 1。 | **`HYPOTHESIS_ONLY` / KEEP PROVISIONALLY（rank 1）**。内部动作碰撞最少、章节链最完整，但 turbo/iterative direct competitor 与 baseline defect 均 unknown；只能进 Step 1。 | **`REJECT` as independent card**。其唯一具体 recovery action 与 C1/D047 同族；syndrome 可作为 C1 的信息/消融候选，不能另算第三方法。 |

## Action-signature collision receipts

| action signature | original hit | interpretation | effect |
|---|---|---|---|
| `LLR scalar/noise calibration → same decoder` | P08 B1/B2 只改 temperature、clip、normalization/offset（`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py:164-194`）；current authority 仅保留 PARTIAL engineering asset（`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3102-3105`） | calibration/correctness 不改变 CPR decision | C1/C2 必须产生可观测的 CPR state/hypothesis delta；否则 reject |
| `oracle soft scale → GMI` | F4-A `+0.008907` 且 smoothing-fragile（`.sessions/2026-07-20-direction-lab-science-scout/verifications.md:384-396`） | scoring boundary，不是 deployable feedback evidence | 三卡均不得引用该数作 Go/headline |
| `final CRC/BER → flip/select labels` | H1 flip=PI-BER（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:2302-2304,2317-2334`） | post-hoc ambiguity resolution，无新增方法动作 | C1/C3 若使用最终 CRC 择优，直接 reject |
| `online blind update → recover swap` | standard-CMA continuation fixed-BER `0.00018/0.00117`（`projects/thesis-fso/worker-logs/step-032-p05-ml-ood-online-adaptation.md:52-74`） | 只对该 dual-pol swap slice 成立，但构成真实 cheap alternative | 目标 defect 若被其吸收，则三卡不得成方法 |
| `receiver statistic → select/execute branch` | CCISP/Ch5 明确只选择并执行 DA/NDA 分支（`projects/thesis-fso/direction-lab/harvest/ccisp-select-before-execute-single-branch-method-package.md:41-72`） | 前置 branch selection/scheduling 已有贡献 | C1 仅在 decoder 后改变 phase hypothesis 才可区分；C2 continuous update 区分最清楚 |
| `detection → relock/DD/state switch` | D047 observation-only route（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:2718-2731`） | 不是既有方法，但已占用 generic action family | C3 与其精确同族而 reject；C1 仅以“有限 current-frame decoder-scored hypothesis update”窄化后留待 Step 1 |
| `detection → rollback historical state` | D028 dwell=11 或 early snapshot BER `0.0176→0.1226`（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:1601-1617`） | stale-state 物理 dead end，非参数问题 | 三卡禁用 snapshot rollback；current-frame fresh re-estimation 不被该条自动 Kill |

## Direct-competitor unknowns for Groundwork Step 1

本包没有外部检索，下列全部是**检索问题，不是“未发现竞品”结论**：

1. C2：是否已有同信息合同的 turbo/iterative carrier phase recovery，用 decoder extrinsic soft symbols 反哺 phase/CFO estimator；需核 exact `L_post-L_apriori`、迭代时点、总预算和 optical/FSO 条件。
2. C1：是否已有 code-aided phase ambiguity/cycle-slip hypothesis testing，以 parity/syndrome/extrinsic 对有限相位假设重评分并触发一次 current-frame switch。
3. C3：CRC/syndrome-aided cycle-slip detection/correction、relock/reacquisition 是否已覆盖相同 trigger→action；由于 C3 已与本地 D047/C1 同动作族，只有发现机制不同的 recovery action 才有重开理由。
4. 三卡共同：strongest conventional comparator 的具体算法身份、公式、公开实现与可调参数均 `unknown`；当前只能冻结 comparator contract，不能声称“传统 turbo/CRC repair 不存在”。
5. baseline defect 也 `unknown`：必须先证明 corrected B0/B1 与独立调谐 B2/receiver-only CPR 在同一 receiver-visible slice 留下可恢复 failure；P08-R2 的 partial diagnostic 数字不构成该证明。

## Provisional convergence

| rank | card | class | keep/reject | why | Step-1 falsifier |
|---|---|---|---|---|---|
| 1 | C2 true-extrinsic soft-symbol CPR | `HYPOTHESIS_ONLY` | **KEEP** | continuous CPR state update；与 P08 scalar、CCISP gate、Ch5 schedule、CRC relabel 的本地动作身份最清楚，且能形成流程图/主图/承重消融 | exact-action turbo/iterative competitor 已覆盖同 input→update→output；或 corrected conventional baseline 没有可恢复 defect；或 hard-DD/CMA 在同预算下吸收 |
| 2 | C1 finite phase-hypothesis re-evaluation | `HYPOTHESIS_ONLY` | **KEEP** | current-frame finite hypothesis update可避开 D028 stale rollback；相对 C2 是离散 hypothesis selection，机制不同 | code-/CRC-aided hypothesis switch 已是传统直接方法；或 decoder evidence 不改变 receiver-only likelihood 的选择；或实现退化为 final CRC/post-hoc best-of |
| 3 | C3 syndrome-triggered recovery | `REJECT` | **REJECT / merge trigger into C1 ablation** | 冻结为 relock+hypothesis-switch 后与 C1、D047 同动作族；只换 syndrome 信息源不足以形成独立方法，final CRC/monitoring 又分别撞 D039/U47 | 只有新的、不同于 hypothesis switch/relock/rollback 的 recovery action 且有 receiver-causal时点，才允许未来另卡；本包没有该证据 |

**收敛边界**：survivor=`2`，且两者**仅允许进入 canonical Groundwork Step 1，不是 Go、不是 active carrier、不是 `METHOD_SIGNAL`、不授权 adapter/实验**。

## Thesis chapter capability checkpoint

- **C2**：章节形潜力最高——可写明确 M-C-A、decoder↔CPR 两轮算法、主图、三路承重消融与 fallback；但 direct competitor、problem-bearing conventional baseline、adapter feasibility 都未闭合，故当前**不具备**正式 `thesis_method_disposition`，不能误标 `NEEDS_ONE_BOUNDED_PACKAGE`。
- **C1**：具备离散控制链与时序图，但与 Ch3 selector 叙事、D047 generic state-switch 和传统 code-aided ambiguity resolution 的边界尚未闭合；当前同样只是 pre-GW design candidate。
- **C3**：作为独立章节方法 `REJECT`；其 early-syndrome 信息可在不增加候选数的前提下成为 C1 的 trigger/ablation，或失败后成为 monitoring/supporting material。
- 当前 Ch4 方法槽仍开放；`mission_method_delta=NONE`。本次 portfolio 收敛是 Step 1 输入，不是论文方法进展。

## Master verification list

- [x] task-control validator 为 `PASS`，action class 为 `PORTFOLIO_MAP`。
- [x] C1/C2/C3 均覆盖 M-C-A、I→A→O、runtime、实际 decision、碰撞、comparator、cheap alternative、adapter、图/消融/fallback、classification。
- [x] P08、F4-A/F4-C、P05、CCISP、D047、D028 均回到原始 source/D/V/worker-log 的 `file:line`，未只转述 inventory。
- [x] provisional survivors 为 2，且机制不同：C1 离散 finite-hypothesis re-evaluation；C2 连续 soft-state update。
- [x] traditional turbo/CRC direct competitors 与 exact comparator 明确标 `unknown`，留给 Groundwork Step 1。
- [x] 未外部检索、未实现、未实验、未修改 owner/source/artifact。

## Terminal

`CANDIDATES_CONVERGED`
