# Coded decoder-feedback 方法主线 Groundwork

> 状态：closed | 创建：2026-08-09 | 当前阶段：Groundwork Step 4a S2 science terminal

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 16
  role: METHOD_PRODUCTION_GROUNDWORK
  mission: produce one thesis-usable Ch4 coded decoder-feedback method or a canonical evidence-backed terminal
  active_lane: GROUNDWORK_STEP4A_S2_SCIENCE_TERMINAL
  authority_pointer: projects/thesis-fso/master-state.md
  decision_gate: D027/V021 verify S2 damage and recoverability FAIL; sequential science chain terminates
  allowed_actions: []
  forbidden_actions:
    - DEFECT_SMOKE
    - D0_B2_S4_SCIENTIFIC_EXECUTION
    - ADAPTER_IMPLEMENTATION
    - C1_POLICY_IMPLEMENTATION
    - MVE
    - HELDOUT_EXPERIMENT
    - NON_D0_SCIENTIFIC_EXPERIMENT
    - CONTRACT
    - EXECUTE
    - THESIS_CLAIM
  mission_log_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/mission-log.md
  mission_checkpoint: CP016
  next_legal_action: none; science terminal verified
```
<!-- RDL-CONTROL:END -->

## 范围边界

**原始目标**：以“形成可写入毕业论文章节的方法”为明确目标，完成 coded decoder-feedback 候选收敛、Groundwork、Step 4a、最小 adapter 和公平方法比较的连续推进；除真实硬 blocker 外，不以入口检查、计划、单个上游步骤或 adapter identity 作为终点。

**当前范围**：

- Ch4 coded carrier-recovery / decoder-feedback 方法章槽位；最多保留两个机制不同候选。
- receiver-local、因果合法的 decoder extrinsic、syndrome/CRC、iteration callback、bounded recovery/re-evaluation 所需最小接口。
- 总任务授权硬上限 `13.0d`；冻结投影为 D0 `10.819450931739858d` + post-D0 C1/公平比较 `2.0d` = `12.819450931739858d`，不得再次扩大。
- B0/B1/B2/O1/C1/C2 baseline ladder、defect smoke、paired fair comparison、机制消融和 fresh-context verifier。
- C1 reference-method extension 可由 estimator extension、局部化、触发、调度、反馈策略或有界计算图构成；方法身份按完整 deployable action chain 判断，不要求全新动作原子。

**明确不含**：

- 不恢复 P08 LLR calibration 或 P08/P08-R 旧科学结论。
- 不把 coded-chain correctness、信息边界修复、adapter identity 或 deterministic validator 包装成方法。
- 不扩建完整通用通信平台；不修改 `common/` 或原 coded-chain 资产来掩盖 adapter 身份。
- 不允许 TX payload truth、true phase/CFO/h/SNR 或 post-hoc final correctness 进入 deployable decide path。
- 不修改或暂存四个既有 `p05_run*.log`；不 push；默认本对话统一一次提交。

**范围变更记录**：

- **[2026-08-09] [决策 D001]**：把 T010 旧“design-only / ≤1 天 adapter”资产阻断扩为独立的 3–7 天 coded decoder-feedback 方法生产 Groundwork。
  - 原因：用户明确把 Ch4 方法产出设为本轮目标，并授权建设最小 method-bearing adapter/testbed。
  - 新范围：允许在 canonical Step 1–3/必要 3.5/4a 通过后建设实际需要的 decoder 中间信息与外层 callback/recovery 接口，并运行公平比较。
  - 影响的未决项：T010 `CODED_CHAIN_ASSET_BLOCKED` 保留为旧授权下的 readiness 事实；C1/C2/C3 需重新核对，不自动晋级、不恢复旧科学数字。
- **[2026-08-09] [决策 D005]**：撤回“核心 phase-hypothesis action 已碰撞就必然终止 reference-method extension”的解释，以 C1 为 reference baseline 从 Step 2 重开。
- **[2026-08-09] [决策 D006]**：固定 shortlist 取得 5 篇合格全文、2 篇保留全文债；可得全文无 exact complete-chain collision，进入 Step 3 Q# formation。
- **[2026-08-09] [决策 D007]**：Q1 暂为 3/4；因项目要求 2019+ 顶刊 baseline，定向精读 corpus 内 TVT 2025 后再裁 Step 3。
  - 原因：D004/V002 只闭合摘要级核心动作碰撞，未读全文、未形成 Q#、未比较局部 repair 的完整链；用户明确要求按完整 deployable action chain 裁决。
  - 新范围：固定 C1 为唯一主入口，允许在 Step 3/3.5/4a 依次通过后建设最小 decoder callback/recovery adapter；不要求发明新动作原子，C2 仅在 C1 hard terminal 后做一次入口裁决。
  - 影响的未决项：H001/CP005 的“必须出现不同 action 原子”重开条件失效；D004/V002 的 corpus、core collision 与 `NOT_EVALUATED_NO_Q_FORMED` 事实继续有效。
- **[2026-08-09] [决策 D008]**：TVT ICE-CEM 全文闭合近期顶刊 baseline，Q1 冻结为 canonical 4/4；立即进入 mandatory Step 3.5，范围仍只限文献补检/全文裁决，adapter 与实验继续冻结。
- **[2026-08-11] [决策 D025]**：用户接受现有底座并把总授权从 7 日上调为 13 日硬上限；D024/V019 的完整 workload 与工程验收事实保留，旧七日 science 封锁撤销。严格按 S1→S2→S3→S4 逐门 fail-stop，四门全过后才允许 C1 与 FAIR_COMPARISON_RUN；不缩 workload、不换指标、不做新 readiness/HMM 优化/平台泛化。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. Groundwork 顺序是唯一合法路径；Step 3 与 Step 4a 是硬门控，上游不通过即按 canonical terminal 收口。
2. 问题必须是具体 `M-C-A`：传统载波恢复方法在 coded/phase impairment 条件下因可观测机制产生可恢复 decoder failure，decoder-visible 信息能驱动不同且合法的 recovery action。
3. adapter 只提供方法所需接口；receiver-visible-only 信息边界、no-feedback identity、callback lifecycle、metamorphic test 和 raw receipt 必须可执行验证。
4. oracle 只作 headroom/Kill；Go 对手是经独立调谐、任务匹配、同信息的 conventional comparator，且必须测试 strongest cheap alternative。
5. 公平比较使用 fresh disjoint dev/test seeds、paired realizations、raw codeword/trajectory rows、cluster CI、固定标签 coded metrics、复杂度与迭代账本。
6. `FAIR_COMPARISON_RUN` 是最低方法生产增量；只有科学门 FAIL、执行无效/证据不足或 `13.0d` 总硬上限内无法解除的真实当前门 blocker 可提前终止。D024 的旧 7 日预算门已被 D025 取代。

### 其他结论

1. 旧 T010 的 `CODED_CHAIN_ASSET_BLOCKED` 只证明当时 ≤1 天资产预算不够，不是 decoder-feedback 科学 Kill。
2. C2 旧卡在动作身份上碰撞最少，但仍须与 turbo/iterative carrier recovery 直接竞品、P08 scalar calibration 和 hard-DD/CMA cheap alternative 重新核对。
3. D002 将 C2 true-extrinsic soft-symbol CPR 与 C1 finite phase-hypothesis re-evaluation 保留为仅供 Step 1 证伪的 `HYPOTHESIS_ONLY` 预卡；C3 因 recovery action 与 C1/D047 同族，不再作为独立候选。
4. Sionna 2.0.1 的 soft output、message state、iteration override、callback 与 coded-bit↔16QAM 映射属于 bounded adapter work；当前 corrected P08-R2 缺载波 phase/CFO impairment、CPR state 和可调用 recovery action anchor。该事实是当前 testbed blocker，不是已证明超出 3–7 天的终态 hard blocker。
5. D003/T008 的 repaired integrated Step 1 语料质量门 PASS（93 annotated rows→66 unique，7 source families，必读 6，正式发表 50/66=75.76%）；自动镜像 28/28 已处置为 duplicate 8 / irrelevant 10 / strong neighbor 4 / baseline 2 / unknown 4。C1/C2 均保持 `CORE_ACTION_EXACT`，replacement=0；local terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR`。
6. CP005 终态来自摘要级 direct-action collision，不是 testbed hard blocker、传统 baseline 性能结论或 P08 旧数字；D005 只撤销其“因此不得进入 Step 2”的解释，adapter 仍须等 Step 3/3.5/4a 门控。
7. D004 撤销 D003 的 `NO_VALID_PROBLEM` 映射：本轮未进入 Step 2/3、未形成 canonical M-C-A Q#，因此 problem disposition=`NOT_EVALUATED_NO_Q_FORMED`；“候选动作无 survivor”不能重定义成“问题无效”。
8. D005 将 C1 的全局一次性 finite phase-hypothesis decoder selection 固定为 reference baseline M；完整链碰撞必须按 input/trigger/localization/action/decoder/fallback/budget/output 全签名比较。
9. TVT ICE-CEM 是 2019+ 正式顶刊的具体 global code-aided CFO/CPO baseline；其状态是 per-frame/per-satellite global CFO/CPO，完整链为 `STRONG_NEIGHBOR`，不含 local slip boundary 或 bounded segment/suffix repair。
10. Q1 已通过 Step 3 四判据；这只授权 mandatory Step 3.5，不代表 local defect occurrence、observability、recoverability 或 method contribution 已成立。
11. Step 3.5 已由 V003 接收：三轮终态为 `ROUND3_CAP_REACHED_WITH_NEW`，唯一新增 OFC 2017 已全文裁为 non-exact；正式上限只到 bounded-slice 未确认完整链碰撞，不是领域级 novelty closure。
12. A0/A′/A/B 预检已由 step-091 以 `PASS / P0/P1/P2=0/0/0` 完成独立复核；其结论只支持冻结 D0 诊断，不证明自然 defect、recoverable headroom、B2 未吸收、decoder 信息增量或方法贡献。
13. D0 v2 资产合同在 step-101 以 `FAIL / 0/2/0` 暴露 dev-freeze 权重/artifact 两项 P1；v3 additive repair 经 step-103 `PASS / 0/0/0` 接收，只形成实现前静态合同。当前预算分类为 `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`，没有建立 `>7D_HARD_BLOCKER`。
14. I05 FULL manifest 草稿经独立预审仍有 forged-manifest、HMM/ledger binding 与 positive-oracle 四项 P1，step-134 为 `INCOMPLETE`。I06 历经 step-135/137/139 三次 FAIL 后，T094 closed-world repair由 T097 在最终字节上以 exact 4/4、aggregate 43/43、126-case mismatch=0、C_pre 8/8 验收为 `PASS 0/0/0`；V007 已接收 I06，历史失败与 T095/T096 操作障碍保留。
15. I05 T098 authority-only实现虽有3/13/46 GREEN，T099仍发现object-returning compiler cache与被验FULL共享canonical reference，改变缓存实例后digest不一致对象被接受，step-145=`FAIL 0/1/0`；D014/V008拒绝该cache路线，authority尚未接收。
16. T100 primitive-only cache修复经T101验收：tests 2/15/48、700对nonprimitive共享0、56 cases mismatch=0，step-147=`PASS 0/0/0`；V009接收FULL authority。R001/D015冻结22,800条trajectory-grid ledger与分层HMM/consumer identity设计，待owner YAML transfer。
17. T102因R001遗漏combined payload exact shape而在owner写入前按时间盒停止，step-148=`INCOMPLETE_OWNER_IDENTITY_TIMEBOX`、owner未变、prechange RED未运行；历史原始tool/PASS记录已恢复唯一shape并fresh复算三个root PASS，R001已补证据，下一步从冻结owner重开transfer。
18. T103 owner author gate为330 assertions全绿；T104因Windows code 206全项NOT_RUN。T105以文件内源码→stdin完成720项独立验证，除S2/BPS manifest缺`binding_kind` authority导致golden 8/10外，128 literals、3 roots、15 mutations、6 counts、projection/permission/protection均PASS，裁为`FAIL 0/2/0`；D016/V010只开放owner窄修。
19. T106以11/11缺失RED补齐`LOGICAL_COMPUTATION_ID` authority；T107 final-byte独立验证729 assertions、11/11 authority、128/128 literals、3/3 roots、10/10 goldens、15/15 mutations、6/6 counts、mismatch=0，`PASS 0/0/0`；V011接收D015 owner transfer。
20. T108–T109以真实4/4 RED后闭合typed owner loader；fresh verifier为430 assertions、31/31 mutations、四文件52/52、I06 34+7 cases mismatch=0，V012=`PASS 0/0/0`。
21. 两路schema-readiness审查发现ordinary identity descriptors与HMM reference类型仍不自足；D017冻结7类ordinary canonical identity与1类HMM manifest reference，须先owner-only repair并刷新loader seal。
22. T110以41项真实RED完成owner-only D017 repair；T111独立920 assertions、58/58 mutations、10/10 goldens、6/6 counts、mismatch=0，V013接收final owner `02d471a...`，loader seal刷新仍OPEN。
23. D018 将 ordinary canonical identity/binding 与 raw consumer cache provenance 分层：前者可按 `42967/27487` 精确编译；后者因 B2-controlled shared-ID 与现有单值 ledger 冲突继续 OPEN，禁止 executor 猜测。
24. T112–T113 以1107 assertions、48/48 mutations、I06 35 cases与4+1+53 pytest独立复核final loader seal；V014=`PASS 0/0/0`，T114 ordinary identity compiler已开放。
25. T114作者侧counts/回归全绿，但T115以module-global candidate替换复现1080个未授权identity，V015=`FAIL 0/1/0`；D019改用full-owner已认证字段的窄typed domain projection，不改owner bytes。
26. T116–T117 关闭domain authority：438313 assertions、9/9 global attacks、22/22 mutations、42967/27487逐条oracle、22+54 pytest全绿；V016=`PASS 0/0/0`，ordinary identity compiler正式接收。
27. D020 冻结hard-output content store + per-logical provenance sidecar；base raw/scientific projection不改，先做identity-block-only owner transfer，loader/schema/FULL继续OPEN。
15. D012 冻结 TruthView 因果两阶段生命周期：payload info/coded/symbol/waveform 关系必须由 canonical codec/map 绑定，逐偏振 `C_pre` 是 typed receiver-derived 主字段；final correctness 只能由 evaluator 在 deployable output freeze 后从 decoded bits 计算，空数组或预填真假均禁止。

## 进展线索

- **S001 / D001 / CP001**：证据 worktree HEAD 与用户起点一致；目标专题查重为无；登记 3–7 天 scope change 并激活 RECOVER_MAP。
- **S001 / D002 / CP002**：T001–T003 三路恢复完成并由主控核证；候选收敛为 C2、C1 两张 Step-1 预卡，C3 合并为 C1 的 syndrome evidence/ablation；控制面进入 GROUNDWORK_STEP1_SEARCH。
- **S001 / D003 / CP003（历史 mapping，已由 D004 取代）**：T004–T006 完成两轮检索与独立整合；C1/C2 core action 均 exact collision、0 replacement；当时写入的 terminal mapping=`NO_VALID_PROBLEM` 已撤销，Step 2/adapter 冻结事实保留。
- **S001 / T007 / CP003**：fresh-context 终验为 FAIL（P0/P1/P2=`0/2/1`）；C1/C2 collision receipts 与 65→46 合并口径通过，但发现一个 28-result 自动镜像只与 integrated corpus 精确重合 4 条，剩余 24 条未逐条处置；当前仅允许 T008 补齐镜像裁决和 integrated v2，随后另起 T009 复验。
- **S001 / T008 / CP003**：自动镜像 28/28 已逐条处置，独立分类反馈纠正了一次摘要指纹过合并；最终 integrated v2=93→66、50/66 published、6 must-read、7 sources，4 个 unknown 均不含可识别 action，replacement=0 与 D003 不变；进入 T009 独立复验。
- **S001 / T009 / CP003**：A/B/C 均 PASS，D 因主控把压缩摘要中的哈希缩写错误扩写为不存在的完整 SHA 而 FAIL（P0/P1/P2=`0/1/0`）。HEAD 内三组权威记录与 fresh 日志完全一致，确认不是文件变化；改由 T010 动态读取 HEAD receipt 复验。
- **S001 / D003 / V001 / H001**：T010 动态读取 HEAD receipt/T022 后 A/B/C/D 全 PASS，P0/P1/P2=`0/0/0`；其 artifact/protection 结论保留，但 staged reviewer 发现 canonical mapping 与 H/V/T/report 治理问题，原关闭状态撤回。
- **S001 / D004 / CP004**：staged reviewer 无 Critical、4 个 Important；D004 保留 local terminal、撤销 `NO_VALID_PROBLEM` 映射，problem disposition 改为 `NOT_EVALUATED_NO_Q_FORMED`；T009 恢复派发快照，H checklist 复位，V001 降为 PARTIAL，报告 v1 标历史，进入 T011。
- **S001 / D004 / V002 / H001 / CP005**：T011 在 `00:04:08.356` 内完成最终复查，P0/P1/P2=`0/0/0`、A/B/C/D 全 PASS；三层语义、integrated v2.1、current/history、T/H/V 模板、HEAD/staging 与 p05 4/4 均接收，专题关闭。
- **S001 / D005 / CP006**：用户显式 scope-change 重开 C1 reference-method extension；D004/V002 的历史事实保留，完整链碰撞取代新动作原子门，控制面进入 Step 2 acquire/read，adapter/实验继续冻结。
- **S001 / D006 / CP007**：T012–T019 完成固定 shortlist 获取/精读；5 篇合格全文、2 篇 unresolved，accessible slice 无 exact complete-chain collision；P08-R2 为 5–6.5 日 `TESTBED_GAP`，控制面进入 Step 3。
- **S001 / D007 / CP008**：provisional Q1 判据 1/2/4 PASS、判据 3 PENDING；只补读 TVT 2025 / arXiv 2309.12828，不以 IWCMC conference 或 ACCESS metadata 凑顶刊门。
- **S001 / D008 / CP009**：TVT 2025/2026 正式顶刊全文给出 ICE-CEM global code-aided CFO/CPO 具体 baseline，判据 3 PASS；Q1 canonical 4/4，进入三路 mandatory Step 3.5 定向补检。
- **S001 / D009 / V003 / H002 / CP010**：Step 3.5 query matrix、双向引文链、physical/B2、三轮上限及所有新增全文债闭合；step-082/083 两路 fresh verifier 均 PASS 0/0/0。带 CSSC/CS-DC/U01/U02 与 recall 限制进入 Step 4a，仅开放 A0 §0–§6 分析预检。
- **S001 / D010 / V004 / H003 / CP011**：A0 中央 report + D0 YAML 经 step-088→091 三轮修订/独立复核，最终 step-091 PASS 0/0/0；只开放四 strata D0 testbed/diagnostic，C1 adapter、MVE 与 held-out 继续冻结。
- **S001 / D011 / V005 / H004 / CP012**：step-094–100 闭合资产/物理/B2/统计/预算接口；step-101 FAIL 0/2/0 被 v3 additive repair 关闭，step-103 PASS 0/0/0 接收静态实现合同。当前只开放实现、单测和独立代码审查后的非科学吞吐门，S1–S4 未授权。
- **S001 / D012 / T088–T089 / step-134–135**：I05 FULL 草稿因四项 canonical-binding P1 保持 INCOMPLETE；I06 独立复核 FAIL 0/3/1。D012 只冻结 truth lifecycle 修复方向，不改变 CP012 科学冻结。
- **S001 / D013 / V006 / T092–T093 / step-138–139**：T092 的旧 9 项 9/9 CLOSED、aggregate 39/39 GREEN，但最终字节 fresh adversarial 73 例出现 10 个新错误接受，step-139=`FAIL 0/4/0`；I06 继续 FAIL，只开放四项结构窄修复。
- **S001 / V007 / T094–T097 / step-140–143**：T094 真实 RED后关闭四类结构缺口；T097 final-byte fresh exact 4/4、aggregate 43/43、126-case mismatch=0、C_pre 8/8，`PASS 0/0/0`。I06 已接收，下一焦点回到 I05 FULL authority/HMM/ledger。
- **S001 / D014 / V008 / T098–T099 / step-144–145**：authority-only常规路径全绿，但shared cached canonical一致性失败使step-145=`FAIL 0/1/0`；只开放fresh-recompile窄修复，raw positive与bindings继续OPEN。
- **S001 / V009 / T100–T101 / step-146–147**：fresh authority graph在700对递归对象上共享0，56 cases mismatch=0，`PASS 0/0/0`；FULL authority seal CLOSED。
- **R001 / D015 / T102 / step-148**：冻结binary64 literal commitments、分层HMM member/computation roots、22,800 trajectory-grid ledger、direct-to-executed cache与consumer-PK binding；T102未改owner即按时间盒停止，combined exact payload已从原始tool/PASS记录恢复并补入R001，下一步从冻结owner重开transfer。
- **S001 / D016 / V010 / T103–T105 / step-149–151**：author owner有330项全绿，但fresh verifier以720项裁出S2/BPS `binding_kind` authority缺失，`FAIL 0/2/0`；只开放统一literal `LOGICAL_COMPUTATION_ID`的owner-only窄修，两个既有root保持。
- **S001 / V011 / T106–T107 / step-152–153**：11项owner窄修经final-byte 729 assertions全量复核为`PASS 0/0/0`；D015 owner transfer CLOSED，下一步进入I05 raw FULL positive与HMM/member/consumer-ledger schema TDD。
- **S001 / V012 / T108–T109 / step-154–155**：typed owner loader经430 assertions、31/31 fresh mutations、52/52 pytest及I06 mismatch=0独立接收；只闭合loader边界。
- **R001 / D017 / compiler-readiness review**：ordinary consumer缺hash-bearing phase/operation/kind/typed PK authority，HMM chunk应绑定manifest root而非ordinary logical-ID manifest；先做owner-only completion与loader seal刷新，I05仍OPEN。
- **S001 / V013 / T110–T111 / step-156–157**：D017 owner completion由独立920 assertions与58/58 mutations接收；final owner=`02d471a...`，下一步仅刷新loader exact seals，compiler仍未开放。
- **S001 / D018 / T114 compiler-readiness**：两路只读审查确认 ordinary identity bytes 已自足，但 B2-controlled per-consumer provenance 无法由现有单值 ledger 表达；先做 additive identity-only compiler，FULL/provenance 迁移保持 OPEN。
- **S001 / V014 / T112–T113 / step-158–159**：final loader seal独立1107 assertions、48/48 mutations、I06 mismatch=0、4+1+53 pytest全绿；D017 owner authority正式开放给T114 schema compiler。
- **S001 / D019 / V015 / T114–T116**：T114作者侧42967/27487与53回归通过，但fresh global mutation证明domain authority缺口；当前只开放typed ordinary-domain projection+compiler rewiring，T117通过前不得继续FULL。
- **S001 / V016 / T116–T117 / step-162–163**：sealed full-owner domain projection与compiler rewiring经438313 assertions、9/9 globals、22/22 mutations和22+54 pytest独立接收；下一焦点为ordinary consumer output/provenance。
- **S001 / D020 / runtime-content design**：两轮独立审查后冻结typed hard-output store、embedded output provenance、codec write anchor与27487/42967 runtime counts；T118先做owner-only transfer。
- **S001 / D021 / V017 / T118–T120**：owner transfer后fresh复核命中10/10新golden与11/11 version mutations、P0/P1=0/0，但50-case矩阵因时间盒为PARTIAL；不单独重跑，遗留覆盖并入loader final-byte终验，随后I05压缩为三个实际代码切片。
- **S001 / D022 / T120–T121**：T120真实RED后取得42/42 mutations与显式五文件62/62 GREEN；取消未派发的loader-only终验，把其独立验证债并入I05三代码片后的唯一batch verifier，当前直接进入typed hard-output实现。
- **S001 / D023 / T121–T124**：hard-output与ordinary provenance已GREEN；HMM owner compiler以22,800/263,520及4/4 goldens GREEN，但FULL positive因ordinary全图被重复重建三遍在364.1秒超时。T124只修issued-fingerprint hotpath，不重开设计。
- **S001 / V018 / T125 / step-171**：唯一fresh I05 batch实跑五文件`71 passed / 686.12s`、118项负向0错收/错拒；FULL incremental=`17.895242s`、authority精确。I05 implementation/unit正式接收，science仍NOT_RUN/NONE；当前进入I07/I08。
- **S001 / T126–T128 / step-172–174 / H005**：I07 SS01–11 focused=`10/10`，I08 AC01–06+窄回归=`19/19`，author P0/P1/P2均0/0/0。下一对话一次合并focused verifier后直接I09/I11；禁止重复I05/readiness链。
- **S001 / D024 / V019 / CP013 / step-175–200**：I07/I08合并快验后完成I09–I19；I19D=`189 passed / P0/P1=0/0`，EB=`36 passed`。正式I20的25个slice与artifact SHA完整，`incomplete_reasons=[]`，冻结workload投影D0=`10.819450931739858d > 7.0d`，裁为`GREATER_THAN_7D_HARD_BLOCKER`；science与FAIR_COMPARISON_RUN均NOT_RUN。
- **S001 / D025 / CP014**：用户显式 scope-change 将总授权冻结为 `13.0d`，保留 D024/V019 全部测量事实但撤销旧 7 日 science 封锁；当前直接进入 S1 natural occurrence，后门按 PASS 顺序释放。
- **S001 / D026 / V020 / CP015 / step-201–202**：S1 final raw=`480`，persistent events=`262`、rate=`0.5458333333333333`，覆盖17 seeds/12 cells；独立终验`PASS 0/0/0`，只开放 S2 damage/headroom。
- **S001 / D027 / V021 / CP016 / step-203–206**：S2 exact 1620 rows；damage=`0.06944`、recoverability=`0.04008`均未过冻结门，证据独立终验`PASS 0/0/0`、science=`FAIL`。B2及后续全部NOT_RUN，专题科学终止。

## 当前状态

- 当前模式：`closed / Groundwork Step 4a S2 science terminal / VERIFIED`。
- 当前 Q#：Q1 canonical 4/4；Step 3 与 Step 3.5 COMPLETE。local slip occurrence/observability/recoverability 与 strongest B2 absorption 仍是 UNKNOWN，只能由 Step 4a 分层闭合。
- 当前 carrier：C1 reference-method extension；C1 原核心动作为 reference baseline M，不计本项目创新。
- 当前 method delta：`NONE`；BER/goodput/method gain=`NOT_MEASURED`。
- 历史 local/framework terminal：`STEP1_NO_METHOD_ACTION_SURVIVOR / STEP1_CANDIDATE_SET_EXHAUSTED`（V002 PASS，仅作 core-action collision 历史事实）。
- 当前 problem disposition：`Q1_CANONICAL_STEP3_PASS / STEP3_5_VERIFIED_WITH_LIMITS / A0_VERIFIED_CONDITIONAL_PASS / GREATER_THAN_7D_HARD_BLOCKER`；D0 science=`NOT_RUN`。
- 当前授权：无。B2/S3/S4、C1、FAIR_COMPARISON_RUN 均因 S2 fail-stop 禁止。

## 未决项

1. 无当前合法执行项。S1 occurrence 成立，但 S2 damage/headroom 双 FAIL，不能支持 C1 方法构造。
2. B2 absorption、decoder-information increment、C1与FAIR_COMPARISON_RUN均保持NOT_RUN。

## 当前位置

`CP016 / GROUNDWORK_STEP4A_S2_SCIENCE_TERMINAL_VERIFIED`：S1 occurrence PASS；S2 damage=`0.06944`、recoverability=`0.04008`双 FAIL，V021证据PASS。B2及后续NOT_RUN，`METHOD_SIGNAL=NONE`，next action=`NONE`。
