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

> status: active（verified by V002）
> date: 2026-08-09
> 取代：D003 的 `canonical_mapping=NO_VALID_PROBLEM` 字段
> 被取代：无
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
