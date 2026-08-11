# Decisions — Coded decoder-feedback 方法主线 Groundwork

## D001: 激活 3–7 天 decoder-feedback 方法生产 Groundwork

> status: active
> date: 2026-08-09
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-08-09 + 调研: projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md

### 决策

新建独立 `2026-08-09-coded-decoder-feedback-groundwork` 专题，把旧 T010 的 ≤1 天资产 readiness 阻断扩为 3–7 天最小 method-bearing adapter/testbed 授权；但所有科学动作必须从 Groundwork Step 1 重走，旧 P08 结论与旧 concept-card verdict 不自动恢复。

### 理由

旧预检已证明 C1/C2/C3 均可写出 decoder-visible input→carrier-recovery action→output，但其 `REJECT` 的共同硬因是旧预算只允许 READY/≤1 天 adapter。用户本轮明确改变的是工程预算和 Ch4 方法生产优先级，不是科学证据，因此应重开正式 Groundwork、验证问题与竞品，而不是把旧阻断直接当 Go 或继续做支持性审计。

### 排除的替代方案

- 继续只做 inventory/callback readiness 审计：不产生方法动作，违反本轮目标。
- 直接实现 C1/C2/C3：跳过 Step 1–3/4a，违反 FR-22/TL-30。
- 把 P08 prefix-LS/LLR calibration 或 adapter correctness 包装成方法：与既有 supporting-only authority 冲突。
- 扩建通用 coded receiver 平台：超出 3–7 天最小 testbed 范围，且会制造基础设施漂移。

### 影响范围

- 激活本专题、`projects/thesis-fso/master-state.md` 的新 Groundwork 入口及 T001–T003 恢复任务。
- 允许后续在问题门通过后创建 `projects/thesis-fso/coded-decoder-feedback-groundwork/` 与 `projects/simulation/explore/coded-decoder-feedback/`。
- 不修改 dormant system/longitudinal-test 中 D040/V023/P08-R2 的历史裁决。

### 来源

S001 / 用户 2026-08-09 启动指令。

---

## D002: 两张机制不同预卡进入 Groundwork Step 1；C3 不再独立成卡

> status: superseded
> date: 2026-08-09
> 取代：T010 C1/C2/C3 在旧 ≤1 天预算下的本轮入口分类（不修改其历史记录）
> 被取代：D003
> 依据：projects/thesis-fso/worker-logs/step-047-coded-decoder-lineage-recovery.md + step-048-decoder-feedback-candidate-recheck.md + step-049-coded-chain-interface-readiness.md

### 决策

保留两张且仅两张 `HYPOTHESIS_ONLY` 预卡进入 canonical Groundwork Step 1：

1. **C2 true-extrinsic soft-symbol CPR update（rank 1）**：decoder 真 extrinsic 形成 soft-symbol expectation/reliability，只允许一次连续 phase/CFO state update，并在固定总 BP、front-end 与 latency 预算下重译码。
2. **C1 finite phase-hypothesis re-evaluation（rank 2）**：第一段 decoder consistency 对同一接收帧的冻结有限 phase hypothesis bank 重评分，只允许 keep/one switch，不回滚历史 equalizer state。

C3 syndrome-triggered recovery 不再作为独立方法卡；其 syndrome/early-stall 信息只能作为 C1 的 evidence source 或承重消融，除非未来发现与 hypothesis switch/relock 不同的 recovery action。两张 survivor 均不是 Q#、Go、METHOD_SIGNAL 或 adapter 授权。

### 理由

- C2 改变连续 CPR state，和 P08 scalar calibration、CCISP branch gate、Ch5 scheduling、final CRC relabel 的动作签名区分最清楚；其 falsifier 是 exact-action turbo/iterative competitor 已覆盖同一输入与更新，或 hard-DD/CMA 在同预算下完全吸收。
- C1 的 current-frame fresh hypothesis re-evaluation 不等于 D028 被 Kill 的 stale snapshot rollback；但它仍与 D047 detection→relock/state-switch 同动作族，必须由直接竞品和 decoder-evidence load-bearing 证据进一步证伪。
- C3 只更换 syndrome 信息源，却沿用 C1/D047 的 recovery action，不能仅靠 trigger 名称形成第三个方法。
- T003 证明 decoder soft/state/callback 与 bit-symbol mapping 是 bounded adapter work，也证明当前 P08-R2 没有载波 action callee。后者尚未被证明在 3–7 天内不可解除，因此只形成 Step 1/后续 testbed 约束，不形成提前终止。

### 否决条件

- C2：直接竞品已实现等价 `decoder soft/extrinsic → continuous CPR update` 且本轮没有新的具体 M-C-A；或 strongest conventional hard/soft-DD iterative CPR 在同信息同预算下解决目标 defect。
- C1：直接竞品已实现等价 `decoder consistency → finite current-frame phase-hypothesis switch`；或 decoder evidence 不改变 receiver-only likelihood 选择；或实现退化为 post-hoc final-correctness/list best-of。
- 两者共同：Step 1 质量门不通过，或 Step 3 无 canonical Q# 四判据全过，则按 `NO_VALID_PROBLEM` 收口，不建设 adapter。

### 排除的替代方案

- 同时保留 C3：违反最多两个机制不同候选，并重复同一 recovery action。
- 因当前 P08-R2 无载波 action anchor 立即报终态 blocker：尚未核对文献 comparator/testbed，也未证明 3–7 天不可解除。
- 先搭通用 coded carrier platform：跳过 Groundwork 且超出最小 adapter 边界。

### 影响范围

- 控制面从 CP001/RECOVER_MAP 转为 CP002/GROUNDWORK_STEP1_SEARCH。
- Step 1 检索必须覆盖 decoder-aided/turbo CPR、syndrome/cycle-slip、iterative demap/decode synchronization、coded residual CFO/CPE、optical/coherent decoder feedback 与 strongest conventional pilot/DD/iterative baseline。
- Step 2 及以下仍禁止，直至 Step 1 独立质量门通过。

### 触发原话

无（技术推导；本决策在 D001 已登记的用户范围内收敛候选）。

### 来源

S001 / T001–T003 / 主控对 D028、D047、P05、P08-R2 caller 与 Sionna 2.0.1 source 的独立核证。

---

## D003: Step 1 两张核心动作均精确碰撞，0 replacement，终止为 NO_VALID_PROBLEM

> status: superseded（仅 canonical mapping 被 D004 取代；collision、survivor=0 与 local terminal 保留）
> date: 2026-08-09
> 取代：D002 的 C1/C2 `HYPOTHESIS_ONLY` survivor 状态
> 被取代：D004（只取代 `NO_VALID_PROBLEM` 映射）
> 依据：projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md + projects/thesis-fso/worker-logs/step-050-c2-step1-search.md + step-051-c1-step1-search.md + step-052-step1-integrated-adjudication.md + step-053-coded-decoder-terminal-verification.md + step-054-step1-mirror-evidence-repair.md + step-056-coded-decoder-authority-terminal-verification.md + V001

### 决策

Groundwork Step 1 terminal 定为 `STEP1_NO_METHOD_ACTION_SURVIVOR`，映射 canonical `NO_VALID_PROBLEM`。C1/C2 survivor=0，replacement=0；Step 2、全文获取、Step 3/3.5/4a、adapter 与实验均不授权。

- **C2 = CORE_ACTION_EXACT**：DOI `10.1109/TWC.2004.837407` 的完整摘要明确 `turbo decoder extrinsic LLR -> iterative maximum-likelihood phase estimation`，覆盖 C2 的核心连续反馈动作；2025 FCN 与 2026 ACCESS 是近期强邻近。
- **C1 = CORE_ACTION_EXACT**：官方 arXiv API 对 `2511.21340` 的摘要明确 `decoder extrinsic model evidence -> PSK-symmetry finite candidates -> decoder selects most likely candidate once after initialization`，覆盖 C1 的有限候选一次选择核心。TSP 2006 只保留 `STRONG_NEIGHBOR`，不以题名过度声称精确时点/预算。
- **Step 1 corpus 足够**：T008 将遗漏的 28-result 自动镜像逐条处置并纳入 integrated v2；最终 93 annotated rows→66 unique，7 source families，必读 6，正式发表 50/66=75.76%，两条机制路线与各 2 组二轮查询均闭合。质量 PASS 只说明足以裁候选，不产生 survivor。

### T007/T008 evidence repair

- T007 对原 prefixed corpus、collision receipts 与 scope ceiling 的检查通过，但因自动镜像 28 条中 24 条未处置而判 `FAIL`，D003 当时不得视为已终验。
- T008 对镜像 28/28 逐条处置：`DUPLICATE=8`、`IRRELEVANT=10`、`STRONG_NEIGHBOR=4`、`BASELINE=2`、`UNKNOWN=4`。四个 UNKNOWN 都没有可识别 carrier-recovery action，故不提供 corpus-backed replacement，也未被强行标成 irrelevant。
- `Phase Estimation by Message Passing` 无共同 DOI/arXiv 且规范化题名不同，按冻结键单列为 strong neighbor；不得仅凭摘要指纹并入可能的 Springer alias。修正后 integrated v2 为 93→66、50 published。
- 镜像可行动线索仍落在 iterative joint decoding/phase estimation 或 conventional synchronization 同族，没有形成与既有动作库存不同的新 carrier-recovery action；replacement 保持 0。最终 acceptance 仍须修正合同后的 fresh-context verifier PASS。
- T009 的 A/B/C 均 PASS；D 的 hash mismatch 来自主控错误扩写压缩摘要中的缩写，而非受保护日志变化。HEAD 内 `step4a-reopen-input-receipt.json` 等权威记录与 fresh 文件一致；因此最终 acceptance 改由 T010 使用 `git show HEAD:<receipt>` 动态基线复验，不追溯改写 T009 FAIL。

### 理由

本轮允许构造最多两张 replacement，但现有 corpus 没有同时具备 problem/action evidence 且动作不同于 C1/C2、C3/D047 relock/state-switch、D028 rollback、F4-C relabel、P08 scalar、P05 CMA、CCISP/Ch5 selection/scheduling 的对象。把 trigger、阈值、FSO 场景、一次/多次、soft-symbol mapping、公平账本或计算调度改名，不产生新的 carrier-recovery action identity。

### 排除的替代方案

- 进入 Step 2 精读以“再找差异”：两张卡的预注册核心动作 falsifier 已在 Step 1 触发，精读只能细化碰撞，不能把场景/实现差异自动升级为新动作。
- 以当前 P08-R2 缺 carrier callee 报 testbed blocker：终止原因是 action collision，不是 3–7 天工程不可解。
- 退回 C3 或 decoder-stall/feedback scheduling：前者重复 D047/C1 recovery action，后者只换 trigger/调度且碰撞 Ch5，不满足方法动作门。
- 建 adapter 后再看：adapter 只提供接口，不能修复新颖性/问题身份缺失。

### 影响范围

- `projects/thesis-fso/master-state.md` 的 coded decoder-feedback Step 1 标为 terminal；所有下游门冻结。
- P08/P08-R/P08-R2 科学 ceiling、D028/D047/P05/F4-C 的局部边界保持，不扩大为领域负面。
- Ch4 方法槽仍未由本专题形成方法；`mission_method_delta=NONE`，贡献层级=`NONE`。

### 触发原话

无（技术证据触发；用户已在 D001 明确允许 canonical negative 时诚实终止）。

### 来源

S001 / T004–T008 / integrated JSON v2 `search-archive/2026-08-09/coded-decoder-step1-integrated.json`。

## D004: 撤销 Step 1 到 NO_VALID_PROBLEM 的越级映射，保留候选集耗尽终态

> status: superseded（V002 对历史事实的验证继续有效；下游冻结与重开条件由 D005 取代）
> date: 2026-08-09
> 取代：D003 的 `canonical_mapping=NO_VALID_PROBLEM` 字段
> 被取代：D005（只取代“核心动作碰撞必然终止 reference-method extension”及其下游冻结解释）
> 依据：`stages/glossary.md` 的 Problem/M-C-A 四判据定义 + `stages/gw-search.md` Step 1 职责边界 + staged diff reviewer（Important #1）+ T008 integrated v2.1

### 决策

保留 local terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR` 与 framework disposition=`STEP1_CANDIDATE_SET_EXHAUSTED`；撤销 `NO_VALID_PROBLEM` 映射。Problem disposition 定为 `NOT_EVALUATED_NO_Q_FORMED`。

- C1/C2 core action exact collision、survivor=0、replacement=0 的 Step 1 事实不变。
- 本轮未进入 Step 2/3、未形成 canonical M-C-A Q#，因此不能对 Problem 四判据给出 PASS/FAIL，更不能把 action survivor=0 重定义为“问题无效”。
- Step 2 与全部下游仍不授权：没有候选方法动作可供获取/精读，不代表某个已形成问题被证明无效。
- adapter、defect smoke、公平比较、实验、贡献均保持 `NOT_RUN / NOT_AUTHORIZED / NONE`。

### 理由

`stages/glossary.md` 将 Problem 定义为具体方法 M 在条件 C 下因机制 A 不足的对象，并要求四判据逐项审查；该对象在 Step 3 精读后形成。Step 1 只负责检索和候选方向筛选。当前证据足以淘汰两张 action card，却没有合法 Q# 可供问题判定。使用 `NO_VALID_PROBLEM` 会把 Step 3 的语义门前移到 Step 1，违反 FR-22/FR-23。

### 排除的替代方案

- 继续保留 `NO_VALID_PROBLEM` 但加 scope ceiling：scope 限定不能修复概念层级错误，仍会让 future reader 把“无动作 survivor”当作“问题四判据失败”。
- 为了获得 problem verdict 进入 Step 2/3：两张卡的核心动作 falsifier 已在 Step 1 触发，继续投入全文不能自动产生不同动作；这会违反候选门。
- 删除 D003：不删除历史错误；通过血缘链只取代错误 mapping，保留其 collision/repair 证据。

### 影响范围

- integrated JSON 升级 v2.1：`canonical_mapping=null`、`problem_disposition=NOT_EVALUATED_NO_Q_FORMED`。
- registry/topic/master/mission/S001/V/H/report 的当前投影只使用 local terminal 与 problem NOT_EVALUATED；T006–T010/step-052–056 中的旧 mapping 作为历史执行事实保留，并由 D004 明确取代。
- 专题暂时恢复 active，仅允许 T011 语义/治理复验；不重开任何科学步骤。

### 触发原话

无（独立 staged review 与 framework owner 的技术冲突触发）。

### 来源

S001 / staged diff reviewer / `stages/glossary.md` / `stages/gw-search.md` / integrated JSON v2.1。

---

## D005: 以完整 deployable action chain 重开 C1 reference-method extension

> status: active
> date: 2026-08-09
> 取代：D004（只取代 downstream freeze/reopen-condition interpretation；D004/V002 的 collision 与 problem-not-evaluated 事实继续有效）
> 被取代：无
> 依据：用户原话: voice.md 2026-08-09 + 调研: projects/thesis-fso/coded-decoder-feedback-groundwork/step1-integrated-adjudication.md + 官方流程: .agents/skills/research-direction-lab/references/method-production.md

### 决策

撤回“没有全新 carrier-recovery action 原子或核心 phase-hypothesis action 已碰撞，就必须终止 reference-method extension”的解释；把 C1 有限 phase/ambiguity 候选加 decoder evidence 的全局一次性选择降为 reference baseline M，从 Groundwork Step 2 开始以完整 deployable action chain 裁决其 extension，而不要求发明从未出现过的动作原子。

完整碰撞签名冻结为：

`receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`。

只有直接竞品已覆盖同信息、同粒度、同局部修复、相当预算的完整链，才能以 exact complete-chain collision 终止 C1。estimator extension、局部化、触发、调度、反馈策略或有界计算图，只要组成可部署完整链并解决合法条件下已复现的 baseline 缺陷，均可作为学位论文方法候选。

### 理由

- D004/V002 只验证了摘要级核心动作碰撞、Step-1 corpus 计数和“未形成 Q#”；`step1-integrated-adjudication.md` 明确承认未读全文、未验证公式、粒度、预算、baseline defect 或完整链等价性。
- Research Direction Lab 的 reference-method extension 允许从可复现 reference baseline 与 defect contract 出发；完整方法链不因其估计原子已有文献而自动失去方法身份。
- 本轮新颖性由“baseline M 在 coherent FSO coded receiver 条件 C 下的具体局部 slip/时变 ambiguity 缺陷 A + 有界局部 repair 完整链”承担。A 目前只是待验证假设，必须由全文、Step 3 Q#、mandatory Step 3.5 和 Step 4a defect smoke 依次闭合。
- 用户明确把最低正常终点设为 `FAIR_COMPARISON_RUN`；摘要级 action collision、全文获取、Q# 形成、adapter identity 或 deterministic validator 都不是新的停止点。

### 排除的替代方案

- 删除或否认 D004/V002：不选。93→66 corpus、C1/C2 core action exact、replacement=0、problem=`NOT_EVALUATED_NO_Q_FORMED` 都是真实历史事实。
- 直接把局部 repair 写成已成立方法：不选。目标 defect、decoder observability、recoverability 与 strongest cheap alternative 尚未通过全文和 Step 4a。
- 为规避碰撞发明新 estimator 原子：不要求，也不以“从未出现过”为正向判据。
- 同时展开 C1/C2：不选。C1 是唯一主入口；只有 C1 达到 exact complete-chain collision、defect 不存在、无 recoverable headroom、B2 已解决或 adapter 真实超预算等 hard terminal，才允许对 C2 做一次入口裁决。
- 扩成通用 coded receiver 平台：继续排除。只允许 C1 所需的最小 callback/recovery adapter。

### 影响范围

- 本专题由 `CP005 / CLOSED` 重开为 `CP006 / GROUNDWORK_STEP2_ACQUIRE_READ`；registry、topic-index、mission-log 与 `projects/thesis-fso/master-state.md` 同步更新。
- Step 1 的 search/corpus 资产直接复用；Step 2 优先获取并精读 arXiv `2511.21340`、DOI `10.1109/TSP.2006.874844`、DOI `10.1117/12.3107192` 及 2–3 篇 strongest conventional comparator，不做新一轮广泛搜索。
- 在 Step 3 合法 Q#、mandatory Step 3.5 complete-chain collision closure 与 Step 4a A0/defect smoke 通过前，adapter、MVE、科学实验、Contract/Execute 与论文方法声称继续禁止。
- H001/CP005 保留为旧终态快照；其“必须出现新 action 原子才可重开”条款由本决策取代，不回写历史 handoff。

### 来源

S001 / 用户 2026-08-09 scope-change 与连续推进指令。

---

## D006: Step 2 五篇全文覆盖通过，带两项全文债进入 Step 3

> status: active
> date: 2026-08-09
> 取代：D005 的 `GROUNDWORK_STEP2_ACQUIRE_READ` 执行状态（D005 的完整链判据继续有效）
> 被取代：无
> 依据：`projects/thesis-fso/coded-decoder-feedback-groundwork/step2-coverage-report.md` + `projects/thesis-fso/literature_notes_coded_decoder_feedback.md` + step-058–065 worker logs

### 决策

Groundwork Step 2 以 `STEP2_COMPLETE_STEP3_AUTHORIZED` 通过：固定 7 篇 shortlist 中 5 篇取得并完成全文精读，2 篇在三轮合规通道后为 `UNRESOLVED_FULLTEXT`。当前可得全文没有与拟议局部 repair 同 trigger、同 boundary/localization、同 segment/suffix action、同 fallback 和相当 budget 的 `EXACT_COMPLETE_CHAIN`；控制面进入 Step 3，基于全文形成 canonical M-C-A Q#。

- arXiv 2511.21340、TSP 2006、IWCMC 2023、TWC 2004 为 `PARTIAL_CORE_ONLY`；GLOBECOM 2012 为 `STRONG_NEIGHBOR`。
- SPIE `10.1117/12.3107192` 与 ACCESS `10.1109/ACCESS.2026.3653159` 只保留 unresolved claim ceiling，不得被改写为无碰撞。
- P08-R2 fresh audit 证明 decoder adapter 可有界、carrier/action 仍是 `TESTBED_GAP`；5–6.5 日 bounded path 尚未触发 `>7D_BLOCKER`。
- Step 3 只允许形成/裁决 Q#；adapter、defect smoke、MVE 与科学实验继续冻结。

### 理由

用户已经把“一两篇全文不可得不自动 NO ENTRY”和“不能在 Step 2 停下”写入连续推进合同。五篇全文覆盖了 global finite decoder selection、recent syndrome/CMF coarse acquisition、decoder-extrinsic iterative CPR 与 conventional hard/soft-DD CPR，足以形成具体 reference M、近期 comparator 和量化对象。尚缺的 coherent-optical occurrence/physical slice 与 exact local-chain prior art 应由 mandatory Step 3.5 定向补齐，而不是把摘要缺口伪装成结论或把 Step 2 变成永久停止点。

### 排除的替代方案

- 因 SPIE/ACCESS 缺全文停止：违反用户已冻结的连续推进与缺口处理规则。
- 直接宣布完整链新颖：五篇可得全文只支持 fixed-slice 非碰撞；两篇全文债和定向 Step 3.5 尚未关闭。
- 直接建设 adapter：Q#、Step 3.5 与 Step 4a defect/recoverability/observability 门均未通过。

### 影响范围

- 控制面由 CP006/epoch 6 升为 CP007/epoch 7，进入 `GROUNDWORK_STEP3_Q_FORMATION`。
- 新建项目 owner `literature_notes_coded_decoder_feedback.md` 与 Step 2 coverage report。
- Step 3 若至少一个 Q# 四判据全过，必须立即进入 mandatory Step 3.5；不在 Q# 形成后等待用户。

### 触发原话

“若没有 exact complete-chain collision，带限制进入 Step 4a；不得因仍有一两篇全文不可得自动 NO ENTRY。”

### 来源

S001 / T012–T019 / 用户连续推进合同。

---

## D007: Q1 暂为 3/4，定向补 TVT 2025 顶刊 baseline 后再裁 Step 3

> status: superseded
> date: 2026-08-09
> 取代：D006 的“直接形成并裁决 Q#”下一动作（D006 的 Step 2 PASS 继续有效）
> 被取代：D008
> 依据：`stages/glossary.md` 四判据 + `projects/thesis-fso/master-state.md` 项目参数 + integrated v2.1 的 DOI `10.1109/TVT.2025.3600028` / arXiv `2309.12828`

### 决策

冻结一个 provisional Q1，但在取得并精读 2019+ 顶刊 direct comparator 前不宣称 canonical 4/4：

> **Q1（provisional）**：arXiv 2511.21340 / TSP 2006 型“对整帧使用一个有限 phase-hypothesis、以 decoder evidence 一次选择”的 reference M，在 coherent-FSO coded receiver 的单帧内出现一次局部 constellation-symmetry phase slip / piecewise phase ambiguity 条件 C 下，因 M 假设整帧共享同一 phase class、不能同时对齐 slip 前后两段且不输出 boundary A，可能产生可恢复的 FER/goodput 损失；能否以 receiver-visible decoder metric 触发并定位一个 boundary，只对 bounded segment/suffix 重评候选、clean frame no-op 并回退 B1/B2？

四判据暂定：判据 1 PASS（具体、可证伪 M-C-A；occurrence/observability/recoverability 仍待 Step 4a）；判据 2 PASS（可复用 trigger/localization/repair/fallback/cost 算法链）；判据 3 **PENDING**（项目要求 2019+ 顶刊，现有可读 recent direct item IWCMC 2023 是会议）；判据 4 PASS（B1/B2/O1/C1-ext 的 FER/post-BER/goodput/cost 与 paired CI）。

只执行一次定向 baseline repair：获取并精读 integrated corpus 已有的 2025 IEEE Transactions on Vehicular Technology 正式版 `10.1109/TVT.2025.3600028`（arXiv `2309.12828`）。它若能作为具体 recent top-journal code-aided CFO/CPO comparator，回到 Q1 四判据；若不匹配，按 glossary 才决定是否继续定向 search，不能用会议/预印本凑判据。

### 理由

`master-state.md` 已把判据 3 冻结为“2019 年至今顶刊”。IWCMC 2023 虽是近期、可复现且方法相关，但 venue 不满足该项目参数；ACCESS 2026 全文不可得也不能承担可实现 baseline。TVT 2025 已在 Step 1 integrated corpus 中，身份和 arXiv alias 均明确，读取它是最小修复，不是 broad search。

### 否决条件

- TVT 2025 全文不含可对标的 code-aided carrier phase/frequency method，或正式版身份/title 不一致：判据 3 仍 PENDING，不能宣称 Q1 4/4。
- TVT 2025 已覆盖同 trigger、local boundary、bounded local repair、fallback 与相当 budget：触发 exact complete-chain collision 审查，而不是为了过判据忽略。

### 影响范围

- 控制面升为 CP008/epoch 8，lane=`GROUNDWORK_STEP3_BASELINE_REPAIR`；仅允许该固定论文的全文获取/精读与 Q1 判据修复。
- adapter、defect smoke、MVE 与科学实验继续冻结。

### 触发原话

无（glossary 四判据与项目参数的技术门控）。

### 来源

S001 / D006 / literature owner / integrated v2.1。

---

## D008: TVT 顶刊 baseline 闭合 Q1 四判据，强制进入 Step 3.5

> status: superseded（Q1 canonical 4/4 与 TVT/complete-chain 事实继续有效；CP009 执行状态由 D009 取代）
> date: 2026-08-09
> 取代：D007 的 provisional 3/4 与 `GROUNDWORK_STEP3_BASELINE_REPAIR` 执行状态
> 被取代：D009（只取代 Step 3.5 执行状态与下一控制 lane）
> 依据：`papers/_read_notes/2309.12828.md` + `projects/thesis-fso/worker-logs/step-066-tvt2025-recent-baseline-read.md` + `stages/glossary.md` 四判据 + `stages/gw-supplement.md`

### 决策

将 Q1 冻结为 canonical 4/4，并完成 Groundwork Step 3：

> **Q1（canonical）**：arXiv 2511.21340 / TSP 2006 型“对整帧使用一个有限 phase-hypothesis、以 decoder evidence 一次选择”的 reference M，在 coherent-FSO coded receiver 的单帧内出现一次局部 constellation-symmetry phase slip / piecewise phase ambiguity 条件 C 下，因 M 假设整帧共享同一 phase class、不能同时对齐 slip 前后两段且不输出 boundary A，可能产生可恢复的 FER/goodput 损失；能否以 receiver-visible decoder metric 触发并定位一个 boundary，只对 bounded segment/suffix 重评候选、clean frame no-op 并回退 B1/B2？

四判据裁决：

1. **PASS — 具体问题**：M 的 whole-frame state/selection 与无 boundary 输出由 L01/L02 全文固定；C/A 是有明确反证条件的结构假设。coherent-FSO occurrence、receiver observability、recoverable headroom 仍是 Step 3.5/4a 待闭合项，不被提前写成事实。
2. **PASS — 方法产出形态**：可形成 `trigger → localization → bounded segment/suffix candidate action → decoder re-evaluation → clean no-op/fallback → budgeted output` 的完整算法链，而非只做场景分析。
3. **PASS — 近期顶刊 baseline**：TVT DOI `10.1109/TVT.2025.3600028`（2025 DOI/early identity，2026 正式卷期）全文给出 ICE-CEM equations、Algorithms 1–2 与参数，是 2019+ 正式顶刊的具体 global code-aided CFO/CPO baseline。
4. **PASS — 可量化对标**：B0/B1/B2/O1/C1-ext 可在同一 coded receiver slice 比较 FER/post-BER/goodput、boundary、clean safety、decoder/CPR calls、latency 与 paired cluster CI。

TVT 方法的完整链裁为 `STRONG_NEIGHBOR`，不是 `EXACT_COMPLETE_CHAIN`：它用 Polar posterior LLR 驱动每帧/每卫星的 global CFO/CPO coarse-to-fine estimation，但没有 within-frame slip trigger、boundary localization、bounded segment/suffix repair、clean no-op 或 failure fallback。因此判据 3 已闭合，完整链 novelty 尚未闭合。

按框架和用户连续推进合同，控制面立即进入 mandatory Step 3.5。第一轮只允许三条定向证据链：关键词矩阵、最高引用核心竞品的前后向引文链、coherent-optical/FSO 物理 occurrence 与 strongest B2。新高相关候选必须先获取/精读全文再裁碰撞；若没有 exact complete-chain collision，完成收敛轮后直接进入 Step 4a，不等待用户。

### 否决条件

- Step 3.5 全文确认直接竞品覆盖相同 receiver-visible input、trigger、boundary/localization、segment/suffix action、decoder interaction、fallback、相当 complexity/latency budget 与 output：C1 触发 `EXACT_COMPLETE_CHAIN_COLLISION` hard terminal，再按用户合同决定是否只做一次 C2 入口裁决。
- 仅有摘要级邻近部件、一个不可得全文、场景名称相同或“decoder-aided carrier recovery”泛称：不足以触发完整链 terminal，只形成 claim ceiling 或 acquisition debt。
- 在 Step 3.5 收敛前建设 adapter、运行 defect smoke/MVE 或把局部 repair 写成已成立贡献：继续禁止。

### 影响范围

- 控制面由 CP008/epoch 8 升为 CP009/epoch 9，lane=`GROUNDWORK_STEP3_5_SUPPLEMENT`。
- Step 3 状态改为 `COMPLETE / Q1_CANONICAL_4_OF_4`；Step 3.5 改为 `IN_PROGRESS`。
- 允许 `TARGETED_SUPPLEMENT_SEARCH`、`CITATION_CHAIN_ANALYSIS`、`ABSTRACT_CROSSCHECK`、`FULLTEXT_ACQUIRE` 与 `FULLTEXT_READ`；adapter、defect smoke、MVE、科学实验、Contract/Execute 与论文声称继续冻结。

### 触发原话

“若形成合法 Q#，继续 mandatory Step 3.5；不得完成 Step 3 后停下等待用户。”

### 来源

S001 / T020 / 用户连续推进合同。

---

## D009: 接收 Step 3.5 bounded-slice 非碰撞证据，限权进入 Step 4a A0

> status: active
> date: 2026-08-10
> 取代：D008 的 `GROUNDWORK_STEP3_5_SUPPLEMENT` 执行状态（D008 的 Q1 4/4、TVT baseline 与完整链判据继续有效）
> 被取代：无
> 依据：验证: V003 + 调研: `projects/thesis-fso/coded-decoder-feedback-groundwork/step3_5-supplement-report.md` + critic: step-082/step-083 fresh-context 审查 + 用户原话: voice.md 2026-08-10

### 决策

接受 Groundwork Step 3.5 证据包，正式结论限定为：

`NO_EXACT_COMPLETE_CHAIN_CONFIRMED_IN_BOUNDED_SLICE / ROUND3_CAP_REACHED_WITH_NEW_AND_DEBT_CLOSED`。

关键词矩阵、最高引用核心竞品双向引用链、coherent-optical/FSO physical+B2 补检与 3 轮上限均已执行；Round 3 新增 SHOULD 非零，故不能写成 `CONVERGED_ZERO_NEW`。唯一新增 OFC 2017 已全文裁为 `STRONG_NEIGHBOR`，全部新增 MUST/SHOULD acquisition/read debt 已关闭。CSSC/CS-DC、U01/U02 与 source-recall 限制继续 fail-closed，禁止据此声称领域级 novelty。

控制面只进入 `GROUNDWORK_STEP4A_A0_PREFLIGHT`：先围绕 canonical Q1 完成 A0 §0–§6 的分析、理论 headroom/先验覆盖、negative evidence 与 testbed/B2 合同草案。A0 未通过或未冻结假设/否决条件前，`DEFECT_SMOKE`、MVE、adapter 与科学实验仍禁止；通过后须另立控制决策才能执行最小 defect smoke。

### 理由

- 两个 fresh-context verifier 分别独立复建 6 篇全文八字段与三轮 receipts/physical anchors，均为 `PASS, P0/P1/P2=0/0/0`；可承重结论只到 bounded slice，无 exact chain confirmed。
- OFC 2017 全文明确其 soft decision 来自 pilots、无 decision feedback/sequential update；2604 的 burst 是 GE 调制 Wiener 方差状态；1704 的 window 是 SC-LDPC 码图 decoding wave。三者均未覆盖 decoder-anomaly trigger、explicit boundary/range、bounded local carrier action、selective redecode 与 fallback 的全组合。
- 框架规定最多 3 轮；第三轮仍有新 SHOULD 时应记录覆盖限制。用户已预先明确“若没有 exact complete-chain collision，带限制进入 Step 4a”，且不可得一两篇全文不自动 NO ENTRY。唯一新 SHOULD 此后已全文闭债，继续第 4 轮只会违反上限。
- Step 3.5 不能证明 target defect 发生、O1 headroom、decoder observability 或 B2 未吸收；这些必须在 Step 4a 分层证伪，不能由文献非碰撞替代。

### 排除的替代方案

- 写成 `CONVERGED_ZERO_NEW`：不选。Round 3 的 MUST/SHOULD=`0/1`，只能使用三轮上限终态。
- 因 Round 3 非零而启动第 4 轮：不选。违反 `gw-supplement` 三轮上限；唯一新增已全文闭债，无 exact collision。
- 因 CSSC/CS-DC/U01/U02 全文债终止 C1：不选。债务被 fail-closed 且现有 metadata 未支持完整链；用户明确禁止以一两篇不可得全文自动 NO ENTRY。
- 立即运行 defect smoke 或建设 adapter：不选。Step 4a A0 §0–§6、理论预期、B2/physical/testbed 合同尚未冻结，FR-22 仍禁止编码与实验。
- 宣称完整链新颖或方法成立：不选。bounded-slice 非碰撞只是 prior-art ceiling，不是 novelty closure、defect PASS 或贡献证据。

### 影响范围

- 控制面由 CP009/epoch 9 升为 CP010/epoch 10，lane=`GROUNDWORK_STEP4A_A0_PREFLIGHT`。
- Step 3.5 状态改为 `COMPLETE / VERIFIED_WITH_COVERAGE_LIMITS`；Step 4a 改为 `A0 §0–§6 IN PROGRESS`。
- 允许只读/分析型 `FEASIBILITY_A0`、`SOURCE_AUDIT`、`THEORETICAL_BOUND`、`BASELINE_CONTRACT_DRAFT` 与必要本地全文复核；`DEFECT_SMOKE`、MVE、adapter、held-out/科学实验、Contract/Execute、论文声称继续冻结。
- 下一控制决策只在 A0 §0–§6 完成且无致命信号后产生；若 A0 出现致命信号，则按 Step 4a 直接 Pivot/Kill，而不是用 MVE 抢救。

### 触发原话

“若没有 exact complete-chain collision，带限制进入 Step 4a；不得因仍有一两篇全文不可得自动 NO ENTRY。”

### 来源

S001 / T021–T037 / step-067–083 / V003 / 用户连续推进合同。

---

## D010: A0 条件通过，只授权冻结的 D0 defect smoke

> status: superseded（A0 scientific gates 与 C1 hard-terminal 逻辑继续有效；implementation/execution authority 与“合同已可直接执行”解释由 D011 取代）
> date: 2026-08-10
> 取代：无（承接 D009 的下一个控制决策；D009 的 Step 3.5 结论继续有效）
> 被取代：D011（只取代当前 implementation/execution authority 与 asset-contract readiness；不改 population、seed、threshold、gate、strata 合取或 post-D0 边界）
> 依据：验证: V004 + critic: step-088–091 独立审查 + 调研: `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md` + 数值合同: `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` + 用户原话: voice.md 2026-08-10

### 决策

接受 C1 canonical Q1 的 A0/A′/A/B 分析预检，裁决为：

`A0_VERIFIED_CONDITIONAL_PASS / D0_DEFECT_SMOKE_ONLY_AUTHORIZED / METHOD_SIGNAL=NONE`。

只允许在 CP011/epoch11 下实现、单测并执行 `d0-defect-smoke-contract.yaml` 冻结的四 strata D0 与 B0/B1/B2/O1 diagnostic ladder。D0 不是 MVE，不定义 trigger/accept/fallback/applied local action，也不实例化 adapter/C1-ext。S1 occurrence、S2 coded damage/recoverability/B2 absorption、S3 decoder-information increment、S4 diagnostic identity/information/cost 必须合取；任一关键 gate 失败即形成 C1 的真实 hard terminal，不得靠扩搜索、改门槛或先建 C1 policy 抢救。

### 理由

- step-090 全量审查已关闭 B2 source contract、strata/exposure、symmetry、truth boundary、预算与 A0/A′/A/B ceiling；其三个残余 finding 由 step-091 窄复核全部 CLOSED，最终 `PASS / P0/P1/P2=0/0/0`。
- 唯一数值 owner 已冻结 raw-row schema、seed cluster bootstrap、invalid denominator terminals、S3 fusion dev objective/tie-break、B2 exact source adaptation、7.00 日总预算与 D0/post-D0 边界；同 raw rows 不再允许得到相反裁决。
- A0 的承重结论仍是条件性的：自然 defect、coded headroom、B2 未吸收与 decoder evidence 信息增量都没有实验事实。D0 是关闭这些 UNKNOWN 的最小合法动作，而不是贡献证明。
- 用户已预先授权在 A0 与 testbed 判据冻结后连续进入 defect smoke，并要求关键条件失败时诚实终止，不构造复杂方法。

### 排除的替代方案

- 直接建设 C1 adapter/policy：不选。违反“只有 defect smoke 通过后才建设”的顺序，也会让 action policy 污染 D0 diagnostic estimand。
- 把 step-091 PASS 当 Step 4a Go 或方法信号：不选。它只验证合同可复刻，不证明任何 scientific gate。
- 继续修改 A0 合同而不运行 D0：不选。全部 residual findings 已关闭，继续纸面迭代不增加 occurrence/headroom/observability 证据。
- 合并 natural/controlled strata 或用 truth 驱动候选：不选。前者破坏因果职责，后者违反 receiver-visible 不变量。
- 在 D0 失败后放宽 gate 或先做 C1：不选。预冻结 terminal 必须 fail-closed；若预算仍有余量，只能按用户合同对 C2 做一次独立入口裁决。

### 影响范围

- 控制面由 CP010/epoch10 升为 CP011/epoch11，lane=`GROUNDWORK_STEP4A_D0_DEFECT_SMOKE`。
- 允许 `D0_TESTBED_IMPLEMENTATION`、`D0_UNIT_TEST`、`DEFECT_SMOKE`、`SOURCE_AUDIT`、`CONTRACT_STATIC_CHECK`；禁止 adapter/C1 policy、MVE、held-out、非 D0 科学实验、Contract/Execute 与论文声称。
- D0 的代码/测试/raw/aggregate/receipt 必须位于既有项目路径 `projects/simulation/explore/coded-decoder-feedback/` 及本专题产物目录，不修改 `common/` 来掩盖 testbed 身份。
- 只有 D0 四 strata 全部通过并经新的 D/V/CP 接收，才可授权最小 adapter/C1-ext；否则记录 C1 hard terminal，并按预算决定是否触发一次 C2 入口裁决。

### 触发原话

“先完成 A0 §0–§6，再冻结 testbed 和判据。”

“若任一关键条件失败，诚实终止，不构造复杂方法。”

### 来源

S001 / T039–T045 / step-085–091 / V004 / 用户连续推进合同。

---

## D011: 接收 D0 v3 资产合同，只开放实现、单测与工程吞吐门

> status: active
> date: 2026-08-10
> 取代：D010 的当前 implementation/execution authority 与“冻结合同已可直接执行”解释（D010 的 A0 scientific gates、D0 合取与 C1 hard-terminal 逻辑继续有效）
> 被取代：无
> 依据：验证: V005 + critic: step-101 FAIL / step-102 repair / step-103 PASS + 实现 owner: `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` v3 + 资产报告: `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-asset-preflight.md`

### 决策

接收 D0 v3 为**实现前静态合同**，裁决限定为：

`ASSET_CONTRACT_ACCEPTED_FOR_IMPLEMENTATION_AND_UNIT_TEST / SCIENTIFIC_EXECUTION_NOT_AUTHORIZED / D0=NOT_RUN / METHOD_SIGNAL=NONE`。

控制面升至 CP012/epoch12，lane=`GROUNDWORK_STEP4A_D0_IMPLEMENTATION_PREFLIGHT`。当前只允许 `D0_TESTBED_IMPLEMENTATION`、`D0_UNIT_TEST`、`ENGINEERING_THROUGHPUT_BENCHMARK`、`SOURCE_AUDIT` 与 `CONTRACT_STATIC_CHECK`。其中 12 分钟吞吐门只能在实现、单测和独立代码审查通过后运行，且必须是无科学 seed、无 scientific estimand/裁决的工程基准。

`DEFECT_SMOKE` 与 S1–S4 scientific execution 明确关闭。只有 D0 实现、deterministic/unit gates、独立代码审查和有界工程吞吐门均 PASS，并由新的 D/V/CP 接收，才能再次授权科学 D0。adapter/C1-ext、MVE、held-out、非 D0 科学实验、Contract/Execute 与论文声称继续禁止。

### 理由

- step-101 对 v2 给出 `FAIL / P0/P1/P2=0/2/0`：HMM clean/controlled 权重与 BPS/B2 dev-freeze typed artifact 两项未闭；该失败历史必须保留。
- step-102 给出不重开科学设计的 additive repair；v3 固定 `0.5 clean + 0.5 controlled-target`、sentinel exclusion/receipt/cost、七个具名 artifact、五 BPS + 五 statistic + 一 final tuple 与 test-path chronology lock。
- step-103 fresh narrow reverifier 给出 `PASS / P0/P1/P2=0/0/0`、两项 P1 全部 CLOSED、`94/94` 静态断言通过，并在抽核范围内未发现 scientific-field drift；其终态仅为 `ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER`，没有自行授权实现或实验。
- 静态成本只能裁为 `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`；当前没有证据建立 `>7D_HARD_BLOCKER`，也没有证据证明 4.50 日点估计必然可达。先实现/单测/代码审查，再跑限定工程吞吐门，是不偷删 scientific exposure 的最小合法路径。

### 排除的替代方案

- 直接沿用 D010 运行 S1–S4：不选。v3 新增的是尚待实现和验证的接口；step-103 明确没有授权科学执行。
- 把 step-101 FAIL 删除或改写成已通过：不选。失败血缘解释了 v3 为何增加 dev-freeze typed artifacts，必须可审计。
- 仅凭静态算术宣布预算 PASS 或 `>7D` hard blocker：不选。两者都需要真实 kernel 路径的有界工程吞吐证据。
- 先运行小规模 scientific seed 当作 benchmark：不选。那会绕过科学授权并污染 `NOT_RUN`；benchmark 必须使用专用无科学裁决切片。
- 在实现阶段顺手建设 C1 policy/adapter：不选。D0 仍是无 trigger/accept/fallback/applied action 的 diagnostic shell。

### 影响范围

- 控制面由 CP011/epoch11 升为 CP012/epoch12，lane=`GROUNDWORK_STEP4A_D0_IMPLEMENTATION_PREFLIGHT`。
- v3 owner 的 control metadata 改为 implementation/unit/engineering-benchmark authorized，execution/science 均 false；scientific population、seed、tuple/grid、threshold、gate、logical/materialized exposure、预算数字不改。
- 实现根目录固定为 `projects/simulation/explore/coded-decoder-feedback/`，D0 单测位于既有 `projects/simulation/tests/test_d0_*.py`；不得修改 `common/` 或旧 P08 资产。
- 只有下一轮独立验证 PASS 才能授权 `DEFECT_SMOKE`；若工程吞吐投影超过 7 日且不能靠允许的 vectorization/batch/cache/checkpoint 调整解除，则登记真实 hard blocker，不删 gate。

### 触发原话

无新增；沿用 D010 已登记于 `voice.md` 的“先完成 A0 §0–§6，再冻结 testbed 和判据”“若任一关键条件失败，诚实终止，不构造复杂方法”“只有 defect smoke 通过后才建设”。本决策是这些既有边界下的技术资产闭合，不新增用户 scope。

### 来源

S001 / T048–T057 / step-094–103 / V005 / D010 的连续推进合同。

---

## D012: TruthView 采用因果两阶段完成，不伪造解码后正确性

> status: active
> date: 2026-08-10
> 取代：I06 初稿中空数组占位和把物理 SNR 派生值写入 ReceiverView 的实现解释；不取代 D011 的授权边界
> 被取代：无
> 依据：step-135 independent verification `FAIL 0/3/1` + owner truth boundary + step-094 §3.1

### 决策

接受 step-135 的 receiver-SNR 泄漏、结构化 fail-closed 与 payload truth 缺失 findings。I06 修复必须让 `build_views` 显式接收并冻结完整 `[2,16,1024]` information bits 与 `[2,16,1536]` coded bits；ReceiverView 的 noise estimate 只能由接收样本与 registered known prefix 计算，不能复制或变换 physical SNR/noise truth。

完整 payload truth 还必须绑定 `information bits → canonical codec encode → coded bits → Gray-16QAM data symbols → supplied waveform data positions`；仅有合法 shape/binary 但关系不一致的 truth 必须拒绝。owner 的 `C_pre` 是逐偏振量，ReceiverView 的 typed 主字段必须保留两个逐偏振 receiver-derived 值，不能只存 scalar aggregate并把逐偏振值藏在 receipt。

`final_codeword_correctness` 在 deployable decode 完成前因果上不可知，因此不接受“为满足非空形状而预填全真/全假”的方案。TruthView 采用两阶段生命周期：channel factory 返回完整 channel/payload truth，并把 final correctness 明确标为 `PENDING_EVALUATION`；pending TruthView 的构造器永不接受 correctness。只有 evaluator 在 deployable outputs freeze 后，使用 decoded information bits 与 pending TruthView information bits 逐码字比较，才能返回 init-free、计算所得 `[2,16]` correctness 的新冻结 evaluator view。不得以 module token/caller-supplied correctness 绕过，空尺寸数组也不再表示 pending。

逐偏振 `C_pre` 必须由 ReceiverView 自身根据 `received_samples[:, :32]` 与 `known_prefix` 在构造/replace时复算，作为 init-free 派生字段；receipt 中的副本也必须由同一复算结果生成或删除，不能接受 caller 提供值。ReceiverView 的 receipt/b2 参数只接受能深冻结为内建 immutable tree 的数据；任意 generic slots/`__dict__` 对象若不能转换为彻底脱离外部引用的 immutable tree，必须 fail closed。

### 理由

- owner 要求 final correctness 仅位于 evaluator-only TruthView；它不是 channel 生成时已知的物理量。预先填值会制造后验 oracle 或错误 ground truth。
- step-094 的最小 TruthView 明确要求完整 info/coded bits；当前 `(2,0,k/n)` 是实质缺口，必须由 typed payload 输入关闭。
- 显式 pending + evaluator 计算使 chronology 可测试，并保持 `build_views` 为唯一 physical receiver/truth split factory；deployable caller 仍只接收 ReceiverView。

### 排除的替代方案

- 保留空数组占位：不选。它把缺失数据伪装成合法冻结 truth，并已被独立复核判为 P1。
- 在 channel 构造时预填全真/全假或由 caller 直接传 correctness：不选。前者是假数据，后者允许后验结论绕过 evaluator 计算。
- 把 physical SNR 或真实 AWGN variance改名后继续写入 ReceiverView：不选。信息泄漏是值来源问题，不是字段名问题。
- 让 deployable receiver 接收 TruthView 后再补值：不选。违反 receiver-only 不变量。

### 影响范围

- 只修复 `contract.py/channel.py` 的 view/type/factory 边界及其单测；不改变 scientific population、seed、gate、estimand 或 CP012 权限。
- I06 在新的独立复核 PASS 前保持 FAIL；I07/I08 不因本决策自动开放。
- D0 仍为 `NOT_RUN`，method signal 仍为 `NONE`。

### 触发原话

无；这是 step-135 缺陷证据触发的纯技术推导。

### 来源

S001 / T089 / step-135 / step-094 §3.1 / D011。

---

## D013: 拒绝把 T092 最终字节视为 I06 闭合，保留 D012 并转入四项结构窄修复

> status: rejected（被拒对象是“T092 final bytes 已闭合 I06”的实现路线；D012 因果边界继续 active）
> date: 2026-08-10
> 取代：无
> 被取代：无
> 依据：T093 / step-139 independent reverification `FAIL 0/4/0`

### 决策

不接收 T092 最终字节为 I06 完成证据。step-137 的 9 个已知错误接受虽已 9/9 关闭，fresh 73-case adversarial harness 又发现 10 个错误接受，聚为四项 P1：stored evaluated correctness 可被 `object.__setattr__` 改写；`bytearray`/`memoryview` 等 opaque built-ins 可绕过 immutable-tree 边界并保留可变引用；`noise_samples`/`awgn_samples`/`physical_awgn_samples`/`n0` 等物理 truth alias 未被语义门拒绝；`np.int64` root seed 绕过 exact built-in-int 门。

后续只允许在 D012 原边界内做结构窄修复：correctness 改为由冻结 decoded bits 与 pending truth 在读取/验证时不可覆写地重算，不保存可被篡改的权威副本；receipt 输入采用 closed-world immutable built-in tree，非明确允许类型一律拒绝；physical-noise alias 使用规范化 token/语义族封闭而非追加单个字符串；root/cell scalar 在任何归一化前先做 exact Python built-in type 检查。I06 在新的独立复核 `P0=P1=0` 前保持 FAIL。

### 理由

- 39/39 单测 GREEN 只覆盖已知断言，不能覆盖 fresh adversarial mutation；step-139 的 73 例是最终字节上的独立证据。
- frozen dataclass 不是 `object.__setattr__` 的安全边界；若 correctness 是存储权威，底层写入会直接改变答案。派生属性/公开验证时重算可消除第二权威副本。
- “尝试冻结任意对象”是开放世界策略，遗漏的 builtin/协议类型会继续产生同族缺口；receiver receipt 只需要有限数据树，应使用 closed-world allowlist。
- noise truth 泄漏的风险由语义来源决定，不由四个已知拼写决定；门必须覆盖规范化 token 族。

### 排除的替代方案

- 以 aggregate 39/39 为由接收 T092：不选。它与 10 个 fresh bad accepts 同时成立，不能推翻独立 P1。
- 再补四个字段名、四个 builtin 特例：不选。会重复开放世界 denylist 的同族遗漏。
- 允许 stored correctness 并依赖 frozen dataclass：不选。`object.__setattr__` 已提供反例。
- 扩到 methods/runner/science 一并修：不选。当前缺陷仅属于 I06 boundary，CP012 仍禁止科学执行。

### 影响范围

- 只允许修复 `contract.py`、`channel.py` 及对应 I06 单测；不改 owner、scientific estimand、population、seed、gate 或授权。
- I05 与后续 batch 不因本记录自动开放；工程 benchmark 仍须等全部 unit 与独立代码审查通过。
- D0=`NOT_RUN`，method signal=`NONE`。

### 触发原话

无；这是 step-139 fresh adversarial evidence 触发的纯技术失败记录。

### 来源

T092–T093 / step-138–139 / D012 / V006。

---

## D014: 拒绝共享缓存 canonical 对象作为 FULL authority

> status: rejected（被拒对象是 T098 中 object-returning cached compiler 路线；I05 authority repair继续）
> date: 2026-08-10
> 取代：无
> 被取代：无
> 依据：T099 / step-145 independent verification `FAIL 0/1/0`

### 决策

不接收 T098 当前 FULL authority 实现。虽然 exact/schema/aggregate与常规88-case矩阵全部通过，但 canonical compiler 使用 `lru_cache` 返回同一冻结对象实例；该实例经低层属性赋值改变后，factory与validator共同读取被改变的缓存对象，导致 digest不一致的FULL对象仍被 authority gate 接受。

后续 canonical recompile不得与被验对象共享任何可改变的对象引用。允许两种实现：每次从authority spec fresh构造完整canonical对象；或仅缓存真正immutable的canonical bytes/digest，再从其/authority inputs fresh构造比较对象。禁止缓存并复用dataclass/table/projection/plan等对象实例作为“独立重编译”结果。

### 理由

- frozen/slotted dataclass不是独立authority；低层属性赋值可改变已有slot。
- validator与factory共享同一reference时，双方相等只证明共享污染，不证明manifest匹配独立canonical source。
- 公开coverage重算已被T098关闭，但shared-reference路径绕过的是更上游的authority独立性。

### 排除的替代方案

- 仅在validator前清cache：不选。factory返回的对象与其他调用仍可共享，且时序依赖不可审计。
- 给缓存对象再加token/secret：不选。module-level capability不提供独立canonical事实。
- 忽略低层赋值并以88-case GREEN接收：不选。step-145已给出digest不一致仍接受的直接反例。

### 影响范围

- 仅修复schemas FULL authority compiler与对应单测；raw FULL positive、HMM/member、consumer-ledger三项继续OPEN。
- 不改变owner科学合同、CP012授权或I06 V007结论；benchmark/science继续禁止。

### 触发原话

无；这是step-145 fresh数据一致性证据触发的纯技术失败记录。

### 来源

T098–T099 / step-144–145 / V008。

---

## D015: 冻结 D0 dev-manifest/HMM/consumer-ledger canonical identity binding v1

> status: active
> date: 2026-08-10
> 取代：schemas T088草稿中的opaque namespace与管道拼串实现解释；不取代D011科学/授权边界
> 被取代：无
> 依据：R001 + step-134四项P1 + owner v3 identity/cost缺口

### 决策

接收R001的additive identity closure：保留owner现有数学网格、member/exposure/cache科学语义与全部logical/materialized总量，只新增可独立复算的binary64 literal commitments、domain-separated canonical payloads、ordered HMM member/computation manifests、exact consumer-PK→ledger bindings与direct-to-executed cache source规则。

HMM computation ledger粒度固定为22,800条per-pol trajectory full-grid logical computations；263,520个chunk是aggregate receipts，不新增cost-bearing group ledger；禁止16,689,600条pair-level ledger。`computation_ids_manifest_sha256`必须同时绑定完整group/grid envelope和10/90个ordered logical computation IDs及cache/source，runtime content root另行闭合resolved content与exact sum。

N100 HMM canonical executed owner固定为`M2_N100`；M3直接读M2。Sentinel规范化到同physical-content clean source，再做N规范化；source必须direct EXECUTED、禁止chain，logical ID保留。跨M复用只适用于已证明content-identical的waveform/BPS/HMM，downstream B2 decode禁止复用。Dual-pol HMM accounting由X行charge pair、Y行0，primitive逻辑计数每trajectory均保留。

完整schema/payload/golden以owner YAML为唯一执行定义；R001保存推导和独立复算证据。owner transfer未独立PASS前，schemas不得实现D015，也不得宣称HMM/ledger binding闭合。

### 理由

- 当前opaque namespace只锁“某个hash存在”，不能拒绝等量member替换、group交换或same-phase consumer交换。
- group-only ID不证明member完整性；member-only root可跨group迁移；分层payload同时关闭两类缺口。
- trajectory-grid粒度用22,800条ledger即可表达16,689,600 logical与7,027,200 materialized primitive scores，避免百万级ledger。
- cache source方向、chain规则和dual-pol charge owner此前未唯一，必须先写owner，不能由executor临场猜。

### 排除的替代方案

- 运行时重新调用logspace当authority：不选。binary64身份会依赖环境；authority必须是literal hex+root。
- 单一group computation ID或全局namespace SHA：不选。不能证明10/90 member与cache provenance。
- 每parameter pair一条ledger：不选。产生16,689,600条，违背lossless chunk设计。
- cache chain、source ID替代logical ID：不选。会让方向/曝光漂移且难以审计。
- 把runtime content hash放进preexecution identity root：不选。执行前未知；应由runtime ledger/content gate关闭。

### 影响范围

- 允许先更新并独立验收owner YAML的`identity_binding_contract`，再实施I05 HMM/ledger schema TDD。
- scientific_contract_change=`none`：population、seed、grid数学值、gate、estimand、logical/materialized totals与CP012权限不变。
- D0仍`NOT_RUN`、method signal仍`NONE`；benchmark/science继续禁止。

### 触发原话

无；这是step-134缺陷与owner复刻性缺口触发的纯技术推导。

### 来源

R001 / T088 / step-134 / D011 / owner v3。

---

## D016: 拒绝省略 consumer binding kind authority 的 owner transfer

> status: rejected（被拒对象是T103最终owner字节作为D015完整transfer；D015 identity路线继续）
> date: 2026-08-10
> 取代：无
> 被取代：无
> 依据：T104–T105 / step-150–151 / V010

### 决策

不接收owner `9f12cd11...`为D015闭合证据。T105在720项fresh静态断言中仅有S2与BPS consumer-binding manifest两项P1：logical computation IDs均精确命中，但hash-bearing `binding_kind`未在projection authority和golden raw inputs中冻结，独立verifier只能猜值，manifest root不可由owner自足复算。

后续只允许owner-only additive窄修：所有`consumer_binding_manifest.binding_kind`统一冻结exact literal `LOGICAL_COMPUTATION_ID`，并在每个consumer projection与相关golden inputs中显式保存。该literal从T103原始author构造恢复，并用owner其余inputs fresh复算精确命中S2 root `ed1a721...`和BPS root `51d43e...`；因此保留两个既有root，不生成新root。修后必须重跑完整独立owner verifier，不得只复验两项。

### 理由

- manifest schema把`binding_kind`纳入canonical hash；缺少字面量就不是自足owner。
- 两个logical IDs已独立一致，问题只在最后manifest payload输入，不需要改变consumer PK投影或ledger语义。
- T104的Windows code 206和alias=P0自增规则均非owner失败；T105已用文件内源码→stdin完成全量验证，并按D015/R001/T103权威将alias门收窄为指定2 anchors+2 aliases。

### 排除的替代方案

- 删除`binding_kind`字段：不选。会改变已冻结payload schema与domain separation。
- 接受author-only隐含值：不选。违反golden必须由保存inputs独立复算。
- 用verifier猜测值后直接把T105改判PASS：不选。当前owner仍未保存authority，FAIL必须保留。
- 重生成两个root：不选。恢复出的exact literal已命中原root，无需制造identity漂移。

### 影响范围

- 只改owner identity block与对应静态receipt；不改schemas/tests/science population/seed/grid/gate/estimand/exposure totals。
- owner repair独立PASS前，D015 schema bindings继续禁止；D0仍`NOT_RUN`、method signal仍`NONE`，benchmark/science继续禁止。

### 触发原话

无；这是step-151 fresh独立验证触发的纯技术失败记录。

### 来源

R001 / T103–T105 / step-149–151。

---

## D017: 补齐 ordinary consumer canonical identity authority，并分离 HMM manifest reference

> status: active
> date: 2026-08-10
> 取代：D016“八个 projection 均解释为 consumer-binding manifest”的过宽实现解释；不取代 D015 的 HMM/ledger 粒度、cache、grid 或科学语义
> 被取代：无
> 依据：T108–T109 / step-154–155 / owner compiler-readiness 两路独立审查

### 决策

V011 接收的是 final owner transfer，不等于 compiler-readiness。T108 typed loader 与 T109 独立验证后，fresh schema-readiness 审查确认：ordinary projections 尚未自足冻结 logical identity 的 `phase/operation/work_key.kind/typed fields`；HMM chunk 的右值是 `computation_ids_manifest_sha256`，不能实例化字段名固定为 `logical_computation_id` 的 `consumer_binding_manifest`。

冻结以下唯一解释：

1. 七类 ordinary projections（S2_off、S2_on、S3、BPS、B2_clean、B2_controlled、S4）使用 `binding_kind=LOGICAL_COMPUTATION_ID`，并各自显式保存 ordered `consumer_pk_fields` 与 ordered `work_key_fields`；每项 exact `{name, source, atom_type}`，atom 只取 `str/int/bool`。
2. S2_off=`S2/B1_DECODE/S2_B1_OFF_CANONICAL_B04`；S2_on phase=`S2`，method→operation 为 `GLOBAL...→B1_DECODE`、`OFC17...→B2_DECODE`、`TRUTH...→O1_DECODE`，kind=`S2_ON_METHOD_DECODE`。
3. S3 的 phase 由 raw record_type exact 映射 `S3_CANDIDATE_DEV→S3_DEV`、`S3_CANDIDATE_TEST→S3_TEST`；operation=`CANDIDATE_DECODE`；kind=`S3_CANDIDATE_DECODE`；work field `record_type_as_split` 的值直接取 raw `record_type`，不另造 DEV/TEST transform。
4. BPS=`BPS_DEV/B1_DECODE/BPS_DUAL_POL_SHARED`；B2_clean=`B2_DEV/B2_DECODE/B2_CLEAN_DUAL_POL_SHARED`；B2_controlled=`B2_DEV/B2_DECODE/B2_CONTROLLED_DUAL_POL_SHARED`；S4=`S4/OTHER_S4_CHECK/S4_STANDALONE_CHECK`，work key 仅 `check_id:str`，并 exact 保存 owner 既有七个 check_id 及顺序。
5. Work-key ordered fields固定为：S2_off=`seed,cell_id,target_polarization,jump_present,method_id,canonical_owner_fixture_id`；S2_on=`seed,cell_id,target_polarization,fixture_id,jump_present,method_id`；S3=`record_type_as_split,seed,cell_id,target_polarization,fixture_id,candidate_id`；BPS=`tuple_id,B,Nw,seed,cell_id`；B2_clean=`tuple_id,seed,cell_id`；B2_controlled=`tuple_id,seed,cell_id,target_polarization,fixture_id`；S4=`check_id`。各 raw schema int64/string/boolean 分别映射 canonical atom `int/str/bool`；S2_off 最后一项来自 literal `B04_K1:str`。
6. Consumer PK typed fields固定为 owner table PK 原顺序：S2 7项、S3 6项、BPS 7项、B2_clean 5项、B2_controlled 7项、S4 2项；HMM 8项。ordinary 共41 descriptors，含 HMM 共49；work-key descriptors 共32。
7. HMM_chunk 不使用 `consumer_binding_manifest`。其 reference exact 为 `kind=COMPUTATION_IDS_MANIFEST_SHA256`、raw field=`computation_ids_manifest_sha256`、payload schema=`coded_decoder_feedback.d0.computation_id_manifest.v1`、rule=`exact_typed_chunk_primary_key_equals_group_consumer_primary_key`；logical member authority继续唯一引用 `hmm_authority.logical_computation`。
8. 不新增 owner golden root。既有 S2_off/BPS logical IDs 与 manifest roots逐字节保持；后续 independent FULL oracle必须枚举全量 42,967 ordinary bindings、27,487 ordinary logical IDs、22,800 HMM logical IDs与263,520 HMM chunk roots。总 ledger identity仍为50,287。

### 理由

- `logical_computation_identity` 哈希包含 phase、operation 与 typed work key；缺一项都会允许执行者临场猜字符串并产生不同 ID。
- typed consumer PK 同样进入 canonical payload；只保存字段名而不保存 atom 类型，不能证明 identity bytes 唯一。
- HMM chunk 指向 manifest root，普通 consumer 指向 logical ID；把二者强塞进同一 payload 会造成字段语义与实际 raw field 不一致。
- 本修复只补 identity bytes authority，不改变任何 scientific population/seed/grid/gate/estimand、ledger粒度或成本总量。

### 排除的替代方案

- 让 schemas.py 从现有实现映射自行推断 phase/operation/kind/type：不选。实现不能反向成为 owner authority。
- 给 HMM 伪造一个 group logical ID：不选。D015 已冻结 chunk→computation-manifest 分层，且禁止新增 cost-bearing group ledger。
- 为五类新 kind 任意复用 S2/BPS kind：不选。会发生 domain collision，无法拒绝 same-phase exchange。
- 为本次 identity-only completion 重生成既有 S2/BPS/HMM roots：不选。现有 canonical inputs不变；新域由后续全量独立 oracle验收。

### 影响范围

- 先 owner-only additive repair并独立验证，再刷新 typed loader 的 exact owner/identity seals；其后才允许 ordinary/HMM schema compiler TDD。
- V012 接收的 loader结构与 I06 additive regression保留，但其 current-owner SHA seal会被本决策有意更新，必须 fresh reverify后才能供 schema 使用。
- D0仍=`NOT_RUN`、method signal=`NONE`；benchmark/science继续禁止。

### 触发原话

无；这是 schema-readiness 两路独立审查触发的纯技术 identity 缺口。

### 来源

R001 / D015–D016 / V011–V012 / owner 1413–1801 / step-153–155 / schemas.py 1109–1124。

---

## D018: ordinary identity compiler 与 consumer provenance 分层

> status: active
> date: 2026-08-10
> 取代：D015/D017 中“ordinary logical identity 与 raw consumer cache provenance 可由现有单层 ledger 同时实例化”的实现解释；不取代其 canonical identity、HMM、cache 科学语义或计数
> 被取代：无
> 依据：T114 compiler-readiness 两路只读审查 / owner 755–763、949–984、1413–1501、1696–1969 / schemas.py 1156–1175

### 决策

先以 additive TDD 实现七类 ordinary consumer 的 canonical identity/binding compiler，只闭合 owner 已自足定义的 typed consumer PK、phase、operation、typed work key、logical computation ID 与正反 binding；本切片不生成或宣称 cache/materialization provenance ledger。

精确规模固定为：S2-off `540/60`、S2-on `1620/1620`、S3 `10800/10800`、BPS `7200/3600`、B2-clean `1200/600`、B2-controlled `21600/10800`、S4 `7/7` 个 binding/logical ID，总计 `42967/27487`。T114 只新增 owner-authority-only API 与独立测试，不切换现有 FULL factory；compiler 独立 PASS 后，下一原子切片必须修正 owner-owned per-consumer provenance / aggregate ledger 表达，再迁移 FULL factory 并删除 caller-forgeable plan。

### 理由

- B2-controlled 的 target/sentinel 两个 consumer PK 按 D017 必须共享一个 dual-pol logical ID，但 raw sentinel 又必须指向 clean source；现有 ledger 每 ID 只有一组 `cache_status/source`，validator 还强制每个 raw consumer 与该组值完全相同，无法同时表达 target=`EXECUTED` 与 sentinel=`CACHE_READ`。
- 修改 identity 粒度以绕过矛盾会违反 D017 的 21600→10800 shared-ID 约束；在 executor 中猜 provenance 又会违反 owner-first。
- identity bytes 与 provenance 是可独立验收的两层。先关闭确定层可形成真实代码增量，同时保留后续原子迁移，不把过渡 API 冒充 FULL closure。

### 排除的替代方案

- 在 T114 给 target/sentinel 生成两个 logical ID：不选，直接违反 D017 与 11400 个 B2 dual-pol logical frames。
- 把同一 logical ID 的 cache 状态硬选为 EXECUTED 或 CACHE_READ：不选，必然使另一 consumer 的 provenance 失真。
- 本切片同时重写 FULL factory/HMM/provenance：不选，无法保持最小 TDD 切片，并会一次打断既有 53 项回归。

### 影响范围

- T114 只允许改 `schemas.py`、新增 ordinary identity 单测与 step-160；旧 FULL API 暂留但不得长期双 authority。
- D0仍=`NOT_RUN`、method signal=`NONE`；benchmark/science/MVE继续禁止。

### 触发原话

无；这是 owner 与现有 ledger validator 的结构矛盾触发的纯技术分层。

### 来源

D015–D017 / R001 / owner final `02d471a...` / schemas.py / T114 两路 compiler-readiness 审查。

---

## D019: ordinary enumeration domain 必须来自已认证 owner projection

> status: active
> date: 2026-08-10
> 取代：T114 使用 schemas 模块常量或局部 literal 枚举 ordinary raw domain 的实现；不取代 D017–D018 canonical identity/provenance 分层
> 被取代：无
> 依据：T115 / step-161 / V015 / final owner既有 controlled_fixture、statistics enums 与 dev-freeze fields

### 决策

拒绝 T114 当前 final bytes 作为 authority-complete compiler。`CANDIDATES` 被等基数替换后，同一 authenticated owner/seals 仍生成并接受 1080 个未授权 identity，证明 42967/27487 计数本身不能替代 domain authority。

最小修复不改 owner YAML 字节：typed loader 已对整份 owner bytes 做 frozen SHA 验证，后续从现有 owner 字段提取窄 `OrdinaryDomainAuthority`，至少包含 controlled cell alias order、polarization/fixture/candidate/S2-method/S4-check order、tuple/B/Nw order与各 ordinary table record-type domain。该 projection 以独立 canonical SHA256 frozen seal绑定，并纳入 `D0OwnerIdentityAuthority` 的 fresh assertion；schema compiler 只能消费此 typed projection与现有 identity binding/contract seed view，禁止读取 `schemas.py` 全局枚举或局部 domain literals。

T116 允许在一个原子 TDD 切片内完成 domain projection、loader assertion 与 compiler rewiring，因为 owner bytes及其 scientific/identity seals均不改变；最终仍须由独立 T117 同时复算 projection seal、global-mutation invariance、全量 identities 与旧回归。

### 理由

- aliases、candidate、B/Nw 等值已存在于同一 frozen owner，只是 T108 loader 没有暴露；新增窄 typed projection比再次复制到 identity YAML 更少漂移。
- 单独 seal让 dataclass replace 与 digest spoof fail closed；只检查 owner总SHA字段而不重算 projection仍会信任可替换字段。
- 合并 loader/compiler repair可减少无科学变更的重复 transfer轮次，同时保留真实 RED、fresh final verifier 与失败血缘。

### 排除的替代方案

- 保留 globals，仅静态断言当前值：不选。global可在运行时替换，public build/assert会共同漂移。
- 再向 identity YAML 复制同一 domains：不选。现有 frozen owner已具备单一来源，重复保存制造双 owner。
- 把整份 YAML dict暴露给schemas：不选。边界过宽且丢失typed/frozen projection审计。

### 影响范围

- 只开放 contract loader/domain view、ordinary compiler及其tests/log；owner bytes、旧FULL API、provenance/HMM/raw FULL不变。
- D0=`NOT_RUN`、method signal=`NONE`；benchmark/science/MVE继续禁止。

### 触发原话

无；这是T115 fresh runtime mutation触发的纯技术authority失败。

### 来源

T114–T115 / step-160–161 / owner 436–440、524–536、545–635、827–836 / contract.py 1240–1276 / schemas.py 1277–1336。

---

## D020: ordinary runtime content 采用 hard-output store + provenance sidecar

> status: active
> date: 2026-08-10
> 取代：D018 后续实现中“由raw receipt或raw新增hash字段直接代表可复用decoder output”的假设；不取代D017–D019 identity/domain与HMM设计
> 被取代：无
> 依据：V016后两轮output/provenance独立审查 / codec hard-output边界 / owner raw schemas与truth lifecycle

### 决策

ordinary runtime content 使用两个 identity-block-owned sidecar，不修改base raw schema：

1. `decoder_hard_outputs.jsonl` 保存content-addressed decoder hard-output payload。payload固定16×1024 information bits，CW-major/C-order展平，每字节MSB-first、2048 bytes、RFC4648 standard base64、编码长2732且恰一个`=`、禁止空白/换行、round-trip exact；store record为`{schema, decoder_hard_output_sha256, payload}`，root只hash payload。
2. `ordinary_consumer_provenance.jsonl` 每ordinary logical ID恰一条，store record为`{schema, ordinary_consumer_provenance_manifest_sha256, payload}`；payload exact=`{schema, logical_computation_id, entries}`。entry exact=`{ordinal, consumer_primary_key, consumer_output, cache_status, source_computation_id, source_consumer_primary_key}`，consumer_output嵌完整typed variant payload。
3. S2 output=`schema+hardroot`；S3另含pilot/decoder score canonical float64 hex；BPS另含selected rotation与normalized NLL canonical float64 hex；B2 clean/controlled共用`schema+hardroot`；S4=`schema+tested+failed+passed+evidence_sha256`。PK、receipt、truth、cost、ledger/provenance root均不得进入output payload。
4. `D0Codec.decode_fresh()`返回binary hard bits后立即canonicalize/hash为immutable typed ref；sidecar/raw/provenance builder只能接收该ref，不能接受任意hash字符串。写序固定为hard-output temp→provenance/raw/ledger→bundle全验→统一原子发布→最终receipt绑定owner/source/code/dev-freeze/seed、两sidecar、全部raw与ledger。
5. provenance exact grouping：S2-off按fixture owner序，B04_K1 EXECUTED、其余8项同ID direct cache到B04 PK；S2-on/S3/S4 singleton EXECUTED；BPS按X/Y，M3_N100 direct cache到M2_N100同pol，其余EXECUTED；B2-clean按X/Y均EXECUTED；B2-controlled严格按TARGET_INCLUDED→SENTINEL_EXCLUDED，sentinel direct cache到同tuple/seed/cell/row-pol clean PK。source必须命中EXECUTED leaf、canonical output hash相等、禁止chain。
6. ledger aggregate：任一entry EXECUTED→`EXECUTED/null`；全cache且唯一source→`CACHE_READ/source`，否则拒绝；ordinary ledger `content_sha256`=provenance payload root。HMM继续走独立manifest，不实例化本sidecar。

静态锚为：manifests/ledger=`27487`、entries=`42967`、EXECUTED=`30247`、CACHE_READ=`12720`、cache edges=`480+1440+10800`、group=`12427 singleton +60×9 +15000×2`、aggregate ledger=`26767 EXECUTED +720 CACHE_READ`；含HMM总ledger仍`50287`。hard-output store cardinality为被引用root的distinct count，不硬编码；所有42,960 non-S4 entries forward命中，store reverse无orphan。

### 理由

- 当前raw误码计数不足以证明decoded bits相同；同误码数可对应不同bit pattern，receipt又可能含PK/fixture元数据，二者都不能作为cache content authority。
- 当前codec唯一可观察输出是fresh binary `[B,1024]` info bits；不保存LLR/state/convergence，避免伪造不可观察信息。
- sidecar以typed PK连接现有raw，避免给42,960 raw rows新增字段；全部新增定义位于identity block，删除该block后scientific projection保持原字节。
- provenance root绑定output、status与source，而hard-output root绑定真实decode bytes，链路无循环。

### 排除的替代方案

- 直接用`result_receipt_sha256/evidence_sha256`作可复用content：不选；receipt语义含元数据且未证明跨projection相等。S4 evidence只作为S4 output字段保留。
- 只保存误码/成功CW统计：不选；无法拒绝同计数异bits。
- 给base raw表统一新增hardroot字段：不选；sidecar已提供双向FK，且会无必要改变scientific projection与全部fixture。
- 把LLR、decoder state或cost写入hard output：不选；它们不是当前decode_fresh输出或content语义。

### 影响范围

- 先owner identity-block-only transfer+independent verification；其后刷新loader seals，再TDD实现typed hard-output ref/store与ordinary provenance。旧FULL与partial在迁移前继续存在但不得冒充authority。
- owner base scientific projection、population/seed/gate/estimand与domain projection不变；D0=`NOT_RUN`、method signal=`NONE`，benchmark/science继续禁止。

### 触发原话

无；这是B2/S2 shared logical identity与runtime content可复刻性触发的纯技术设计。

### 来源

D015–D019 / V016 / owner 561–672、741–825、856–984、1043–1064、1411–1969 / codec.py 149–158、273–323。

---

## D021: implementation cadence 收敛，剩余 owner 覆盖并入 loader 终验

> status: active
> date: 2026-08-10
> 取代：D020 中“owner transfer 必须先单独取得完整独立 PASS，随后再另做 loader seal”的执行切片安排；不取代 D020 数据语义、独立验证或任何 scientific gate
> 被取代：无
> 依据：T118–T119 / step-164–165 / 用户对十小时级推进速度的明确质疑

### 决策

T119 在硬时间盒内已独立复算 10/10 新 golden、拒绝 11/11 version mutations，确认 final owner 无 P0/P1；唯一缺口是未完成 `>=50` 全 mutation/protection/旧 authority 矩阵，因此记录为 V017 PARTIAL，不重跑一个只读 owner 专题。

剩余 owner 矩阵一次性并入 D020 loader final-byte 独立终验：作者侧只允许“两枚 seal 常量 + focused tests”，随后一个 fresh verifier 同时完成 owner 遗留覆盖、loader exact view、旧回归与保护。该终验 PASS 前不得实现 runtime sidecar；若出现任一 P0/P1，立即回到相应最小修复，不能用合并验证掩盖。

loader 通过后，I05 只保留三个有实际代码产出的切片：typed hard-output write anchor、ordinary provenance/runtime bundle、HMM runtime + FULL positive integration。每片一个 author gate，按依赖合并一次独立验收；没有新 P0/P1 时禁止再派纯 owner/schema-readiness 复审。后续 implementation batch 同样以“实际代码增量 + 一次 fresh verifier”为单位，15 分钟硬停。

### 理由

- 当前延迟主要匹配 M4（约束过载造成重复 transfer/review），并已产生 M6 风险（产出节奏偏离最低 `FAIR_COMPARISON_RUN` 目标）。
- T119 已把唯一已知疑点定位为 author-oracle coverage defect，而不是 final-owner defect；重复相同 owner 验证不会增加功能代码。
- 合并终验仍保持生成/审查分离和 fail-closed，不降低科学门控，只减少无新信息的上下文轮次。

### 排除的替代方案

- 把 T119 的 PARTIAL 直接升级为 PASS：不选；旧 authority、完整 mutation 与 protection 尚未执行。
- 再开一个完全相同的 owner-only verifier：不选；会重复已通过的 golden/version 工作且不产生运行时实现。
- 因赶进度直接跳过 loader/sidecar/FULL 验证运行 D0：不选；违反 CP012。

### 影响范围

- 仅调整实现/验证切片粒度；owner bytes、D020 语义、CP012 权限、D0=`NOT_RUN` 与 science 禁令不变。

### 触发原话

- "所以我问问，你干了十几小时，做出了啥？不会一次代码没跑吧？"
- "快点吧？你这点玩意真的值得跑十个小时吗？"

### 来源

T118–T120 / step-164–165 / V017 / voice.md。

---

## D022: loader独立复核并入I05最终batch，不再作为实现前阻塞

> status: active
> date: 2026-08-10
> 取代：D021 中“runtime sidecar前先做一次独立loader final-byte终验”的顺序；保留D021的一次性独立验收原则
> 被取代：无
> 依据：T120真实RED与62/62回归 / V017 P0/P1=0/0 / 用户再次质疑全天级过度慎重

### 决策

取消未派发的owner/loader-only T121。T120已完成真实RED、两枚production seal更新、42/42 mutation与显式五文件62/62 GREEN；V017虽因覆盖不足为PARTIAL，但没有P0/P1。该未闭验证债与hard-output/provenance/HMM-FULL三个实际代码片在I05末尾由一个fresh batch verifier一次验收。

这不是把PARTIAL改称PASS：loader在最终batch PASS前仍不宣称独立关闭，benchmark/science继续禁止；但它不再阻塞可逆的实现与单测工作。任何新P0/P1仍立即中断并最小修复。

### 理由

- 单独再跑一次相同loader矩阵不会产生功能代码；T120已有可重复的RED/GREEN与62项回归。
- 当前关键路径是让codec输出真实content authority并贯通FULL，不是继续证明同两枚字符串。
- 将相邻实现一次性独立复核，仍满足生成/审查分离，同时直接纠正M4/M6。

### 影响范围

- I05执行顺序改为hard-output→ordinary provenance→HMM-FULL→一次fresh batch verifier；科学权限与D020语义不变。

### 触发原话

- "你干一天了啊？？？？？？？真的有必要这么慎重吗???????"

### 来源

T119–T121 / step-165–166 / V017 / voice.md。

---

## D023: authenticated FULL wrapper 使用factory-issued外部fingerprint快验

> status: active
> date: 2026-08-11
> 取代：T123在FULL build与assert中各自调用ordinary full canonical recompilation的实现
> 被取代：无
> 依据：T123/step-169的364.1秒timeout与schemas.py调用链

### 决策

保留`assert_ordinary_runtime_bundle`作为final batch的独立深验；authenticated FULL build/assert不再重复生成27,487/42,967全图，而只接受同进程public factory签发的exact bundle，并通过不可由caller提供的外部issuance record校验owner seal与current structural fingerprint。deep mutation、copy/unissued、owner swap均必须fail closed。

### 理由

FULL positive的364.1秒不是263,520 chunk identity编译造成：HMM focused仅6.04秒。正向node先构造ordinary全图，FULL build再深重建一次，FULL assert又深重建一次，恰形成三遍约120秒路径。重复同一canonical graph没有增加信息，却触发超时。

### 排除的替代方案

- 直接跳过ordinary验证：不选，caller可伪造bundle。
- 信任bundle内部自带hash：不选，字段可与伪造内容一起改写。
- 全局删除public fresh recompilation：不选，唯一batch verifier仍需独立深验。

### 影响范围

- 只优化authenticated FULL组合热路径；ordinary/HMM语义、counts、science权限不变。

### 触发原话

无；这是T123可复现timeout的技术根因。

### 来源

T123–T124 / step-169–170 / schemas.py 2519–2575。

---

## D024: D0 工程吞吐超过七日上限，C1 在 science 前硬终止

> status: active
> date: 2026-08-11
> 取代：无；执行 D011/CP012 的 `>7D_HARD_BLOCKER` 分支
> 被取代：无
> 依据：验证 V019 + step-191/198–200 + 用户原话 voice.md 2026-08-11

### 决策

正式 I20 工程吞吐门在 owner workload、四类允许工程调整和逻辑 manifest 均冻结不变时，完整投影 D0=`10.819450931739858` 日，超过冻结上限 `7.0` 日；因此 C1 终止为 `GREATER_THAN_7D_HARD_BLOCKER`。S1–S4、adapter、MVE、held-out 与 FAIR_COMPARISON_RUN 均保持 `NOT_RUN / NOT_AUTHORIZED`，不得用缩减 scientific population、seed、cell、tuple、grid、fixture、candidate 或 gate 来回避终态。

### 核心失败机制

生产规模 HMM workload 在实测最优 `batch_size=2` 后仍需 `0.07931844999742073 s/trajectory`；冻结物化投影保持 `7,027,200` 个 HMM primitive polarization-trajectory-parameter-pair scores，剩余 D0 由此投影为 `6.8194509317398575` 日。已允许的 vectorization、batch size、exact-content cache 与 checkpoint chunk size 均已实际测量；cache 因无重复 owner content 为 `NOT_APPLICABLE`，其余调整不能把总 D0 压回七日内。

### 否决了什么

- 否决在当前 3–7 日 mission budget 内继续执行 D0 science 或建设 C1 policy/adapter。
- 否决把工程底座、typed artifact、validator 或 adapter identity包装成方法增益。
- 否决为取得 PASS 而缩小 owner workload 或改写冻结 scientific gate。

### 可复用部分

I01–I19 的 truth-separated harness、receiver/BPS/B2/HMM kernels、typed artifacts、freeze 与 benchmark receipts 可保留为工程资产；它们不产生 BER/goodput/方法增益结论，也不构成 Ch4 方法贡献。

### 具体数据

- I19D final integration：`189 passed / 488.73s`，P0/P1=`0/0`。
- I20 EB final regression：`36 passed / 74.05s`。
- 正式 I20：shell wall=`25.7s`，runner elapsed=`11.26600000000326s`，`incomplete_reasons=[]`。
- 官方预算：consumed=`4.0d`，remaining=`6.8194509317398575d`，projected D0=`10.819450931739858d`，terminal=`GREATER_THAN_7D_HARD_BLOCKER`。

### 排除的替代方案

- 继续优化直到出现 PASS：不选。冻结 owner 只允许四类调整，四类已全部实测或证实 N/A；继续扩优化范围会违反预设退出判据。
- 先跑 S1–S4 再看结果：不选。D011 明确要求工程吞吐门先于 science，且本门已形成真实 hard terminal。
- 把 `INCOMPLETE` 当终态：不选。正式 receipt 的 `incomplete_reasons=[]`，25 个 slice 与两个 artifact SHA 均闭合。

### 影响范围

专题控制面关闭于 Groundwork Step 4a D0 engineering terminal；method signal=`NONE`，BER/goodput/方法增益=`NOT_MEASURED`，不进入 Contract/Execute 或论文方法声称。未来重开必须是显式 scope change，并提供不缩减 owner workload 的新工程证据足以关闭至少 `3.819450931739858` 日预算缺口。

### 触发原话

见 `voice.md` 2026-08-11；用户要求只接受 FAIR_COMPARISON_RUN 或真实 hard terminal，并对底座膨胀作出纠偏。

### 来源

S001 / V019 / CP013 / step-191、198–200 / 官方 `benchmark-receipt.jsonl`。

---

## D025: 总授权上调至十三日，按冻结科学链直接重开 S1

> status: active
> date: 2026-08-11
> 取代：D024 的 `7.0d` 预算上限、science 禁令与 closed terminal；不取代 D024/V019 的工程测量、冻结 workload 或 I01–I19 验收事实
> 被取代：无
> 依据：用户显式 scope change；D024/V019 完整 workload receipt

### 决策

总任务授权硬上限由 `7.0d` 上调为 `13.0d`，不得再次扩大。沿用 D024 的完整投影：已消耗 `4.0d`，冻结 D0 总投影 `10.819450931739858d`；预留 post-D0 C1/公平比较 `2.0d` 后，总投影 `12.819450931739858d`，预算余量 `0.180549068260142d`。因此 D024 的 `GREATER_THAN_7D_HARD_BLOCKER` 作为历史预算终态保留，但不再阻止当前科学执行。

控制面进入 `GROUNDWORK_STEP4A_D0_S1_NATURAL_OCCURRENCE`。严格按 S1→S2→S3→S4 顺序运行：S1 测自然 slip occurrence；通过后才测 B1 damage/O1 headroom；再通过才测 B2 absorption；前三门通过后才测 decoder-information increment。任一门 FAIL 立即形成科学终态，不为跑完整链继续执行。四门全部 PASS 后才允许实现 C1，并在同一冻结合同下完成一次 `FAIR_COMPARISON_RUN` 与必要消融。

I01–I19 原样复用。不得缩减 population/seed/cell/tuple/grid/fixture/candidate/gate，不换指标，不用 dev 冒充 test。除当前科学门的真实运行时阻断外，不再做预算审计、HMM 优化、底座泛化、治理扩写或 readiness/preflight；每个真实阻断最多一次 bounded repair，修完立即继续该门。

`formal_science_disposition`、`mission_method_delta`、`thesis_method_disposition` 分开记录。取得 `FAIR_COMPARISON_RUN/METHOD_SIGNAL` 前，method delta 与 thesis contribution 均不得宣称。

### 理由

D024 已把科学链工程成本完整测量为 `10.819450931739858d`，超过旧 7 日上限但低于本次 13 日总授权；用户明确接受底座现状并要求直接找方法。因此不再重复工程优化或平台审查，当前唯一增加科学信息的动作是运行 S1。

### 排除的替代方案

- 再优化 HMM 或重审平台：不选；用户明确禁止，且 I01–I19 已由 V019 接收。
- 为省时缩小冻结 workload：不选；会改变科学合同并使结果不可比较。
- 并行或跳序运行 S2–S4：不选；后门依赖前门成立，失败后继续只会浪费预算。
- 以底座 PASS 声称方法：不选；尚无 `FAIR_COMPARISON_RUN/METHOD_SIGNAL`。

### 影响范围

专题由 closed 重开为 active，control epoch 升至 14，checkpoint 为 CP014。当前只授权 S1；后续权限由每个科学门的正式 PASS 顺序释放。研究对象保持 coded decoder-feedback C1，不得转向其他对象。

### 触发原话

- "赶紧接着干？底座就这样了，赶紧去找方法？"

### 来源

用户 scope change / D024 / V019 / CP013 / 官方 `benchmark-receipt.jsonl`。

---

## D026: S1 自然 occurrence 成立，顺序开放 S2 damage/headroom

> status: active
> date: 2026-08-11
> 取代：D025 中“当前只授权 S1”的临时执行权限；不取代 13 日硬上限、顺序 fail-stop 或任何冻结科学合同
> 被取代：无
> 依据：V020 / step-201–202 / S1 final raw artifacts

### 决策

冻结 S1 first stage 完成 480 个 polarization trajectories，检测到 `262` 个 persistent-slip events，event rate=`0.5458333333333333`；事件覆盖 `17/20` seed clusters 与 `12/12` physical cells。三个门槛 `262≥12`、`17≥4`、`12≥2` 全部通过，V020 独立终验为 `PASS 0/0/0`。

正式 science disposition 为 `S1_NATURAL_OCCURRENCE_ESTABLISHED`。这只证明自然缺陷存在，不是方法增益或论文贡献；`mission_method_delta=NONE`、`thesis_method_disposition=NONE`。

按 D025 顺序只开放 S2 的 B1 damage/O1 headroom。S2 任一 damage 或 recoverability 门 FAIL 即科学终止；均 PASS 后才开放 B2 absorption。不得提前运行 B2/S3/S4/C1。

### 运行边界

S1 runner 缺失是本门唯一 bounded repair；三次实跑暴露的 CLI import、Windows atomic replace 与 strict mapping order 都在同一入口修复内以 RED→GREEN 闭合。最终 raw/checkpoint 480 行 byte-identical，focused fresh=`6 passed`；完整跨 resume wall time 未捕获并明确记为 null，不以 finalization 时间冒充。

### 触发原话

无新原话；执行 D025 已登记的“赶紧接着干？底座就这样了，赶紧去找方法？”。

### 来源

`projects/thesis-fso/worker-logs/step-201-d0-s1-natural-occurrence.md`；`step-202-d0-s1-independent-verification.md`；S1 raw/summary/receipt。

---

## D027: S2 damage/headroom 双门失败，C1 科学链终止

> status: active
> date: 2026-08-11
> 取代：D026 的 S2 执行中权限；不取代 D025 的顺序 fail-stop 与冻结科学合同
> 被取代：无
> 依据：V021 / step-203–206 / S2 final raw artifacts

### 决策

冻结 S2 exact workload 完成 `1620/1620` unique typed rows，B2 rows=`0`。B1 damage point=`0.06944444444444449`，10k seed-cluster CI=`[0.017361111111111122, 0.13055555555555556]`，positive cells=`3/3`；因 point `<0.10`，damage gate FAIL。O1 recoverability point=`0.04008151917073723`，CI=`[-0.11234968338626876, 0.19036462197308052]`，positive cells=`3/3`；因 point `<0.10` 且 CI lower `≤0`，headroom gate FAIL。

V021 对 final raw、typed reduction、10k bootstrap、affected-CW 计数、truth boundary 与 hash 做独立复算，证据 verdict=`PASS 0/0/0`，science verdict=`FAIL`。因此按 D025 顺序门立即形成 `S2_DAMAGE_OR_HEADROOM_FAILED` 科学终态，不运行 B2 absorption、decoder-information increment、S4、C1、FAIR_COMPARISON_RUN 或消融。

### 分离 disposition

- `formal_science_disposition=S2_DAMAGE_OR_HEADROOM_FAILED`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`

S1 occurrence PASS 继续是有效事实，但不足以建立可恢复、可成方法的 defect。I01–I19 与 S1/S2 artifacts 可复用为工程/负结果证据，不构成论文方法贡献。

### 失败血缘

T131 暴露旧 full reducer 把 B2 与 B1/O1 强耦合；T132 以等价窄 reducer关闭顺序接口。首个 S2 run 又暴露 bit-error 数误写 affected-CW count，T133 用 per-CW any-error TDD 修复并从零重跑；最终 1620 rows 无 errors-over-total。bool sort-key 只做本地 deterministic-key 修复并从完整 checkpoint finalization。上述工程失败不改变最终科学 FAIL 数字。

### 触发原话

无新原话；执行 D025 已登记的 scope-change 与 fail-stop纪律。

### 来源

`projects/thesis-fso/worker-logs/step-203-d0-s2-damage-headroom.md`；`step-204-d0-s2-sequential-reducer-repair-and-run.md`；`step-205-d0-s2-affected-cw-count-repair-rerun.md`；`step-206-d0-s2-independent-verification.md`；S2 raw/summary/receipt。
