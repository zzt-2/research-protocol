# [S001] Coded decoder-feedback 方法主线激活

> 2026-08-09 | Groundwork 恢复/候选收敛 | complete
> 2026-08-09 续接：T001–T003 验收完成，进入 Step 1
> 2026-08-09 续接：T007 终验 FAIL，限定为 Step 1 证据包修复
> 2026-08-09 续接：T008 修复完成，进入 T009 独立复验
> 2026-08-09 续接：T009 因主控错误哈希合同 FAIL，进入 T010 权威基线复验
> 2026-08-09 暂时收口：T010 artifact/protection PASS；后由 staged review 撤回语义关闭
> 2026-08-09 续接：D004 修正 terminal mapping，进入 T011 复验
> 2026-08-09 收口：T011/V002 PASS，CP005 关闭专题

## 目标

在指定证据 worktree 中恢复 T010 与 P08/R/R2 权威证据，登记显式 scope change，收敛最多两个机制不同候选，并从 canonical Groundwork Step 1 连续推进到公平比较或合法终态。

## 记录

### Session Start Confirmation

- **Current topic**：`2026-08-09-coded-decoder-feedback-groundwork`（查重后新建）。
- **Original goal**：形成可写入 Ch4 的 coded decoder-feedback 方法，而非继续支持性审计。
- **Current scope**：候选收敛 → GW Step 1–3/必要 3.5 → Step 4a → 最小 adapter → 公平比较。
- **Invariants**：canonical GW 顺序、receiver-visible-only、旧 P08 结论不恢复、adapter 不算方法、oracle 不作 Go 对手。
- **Active topic conflicts**：注册表无同名/同义 active 专题，`conflicts_with=[]`。
- **Dependency status**：RDL system 与 longitudinal-test 均 dormant、历史产物可读；thesis-writing active，只提供 Ch4 槽位与论文结构约束。
- **User voice**：本专题已建立 4 条 2026-08-09 原话映射。
- **Collaboration profile**：既有 durable 画像已覆盖“方法章必须有可命名动作链”“深耕已有基础并自动轮换”“不让用户兜底技术判断”；本轮无新的稳定画像信号。
- **Scope check**：是；本轮就是用户明确要求的新 scope。

### 新鲜事实

1. `git rev-parse HEAD`=`1d76f917a89c719614aeefd7a165ab9819425978`，与用户指定起点一致。
2. `git status --short --branch` 仅显示四个既有未跟踪 `p05_run*.log`；本轮冻结为 protected，不修改、不暂存。
3. `.sessions/_registry.yaml` 与目录名检索均未发现 coded decoder-feedback 专题；新建本专题合法。
4. `ch4-decoder-feedback-method-preflight.md` 的唯一终态为 `CODED_CHAIN_ASSET_BLOCKED`：三卡能定义 decoder 信息与 causal action，但旧合同把 ≥2 类新接口视为超过 ≤1 天预算；它明确“不构成科学 Kill，也不授权 GW/实现/仿真”。
5. 本轮用户显式把预算改为 3–7 天并要求 canonical Groundwork，因此 D001 只重开 readiness/scope，不修改旧证据或复活旧科学数字。

### T001–T003 验收与候选收敛

1. **Lineage**：D051/V077/D058 是 current authority；P08/P08-R 科学数字为 INVALID，P08-R2 数字仅为 PARTIAL local diagnostic。可复用项只含 corrected codec/interleaver、prefix-LS/receiver boundary、metamorphic pattern 与统计 schema。
2. **候选**：C2 true-extrinsic soft-symbol CPR 与 C1 finite phase-hypothesis re-evaluation 以 `HYPOTHESIS_ONLY` 进入 Step 1。C3 与 C1/D047 同为 detection→relock/hypothesis-switch，不再独立成卡。
3. **接口**：Sionna 2.0.1 支持 soft output、message state、iteration override 和 v2c/c2v callback；当前 adapter 以 `hard_out=True` 单次解码且未启用这些能力。coded-bit↔16QAM 映射可逆，decoder 侧预计是 bounded adapter work。
4. **当前 blocker**：P08-R2 不含 carrier phase/CFO impairment、CPR state 或 hypothesis/relock/recovery callee，decoder evidence 当前没有可改变的载波动作。该 blocker 只有在 Step 1–4a 后仍无法在 3–7 天内建立最小 receiver-only action anchor 时才可升级为终态。
5. **主控独立核证**：重查了 D028 stale rollback 的 dwell=11/BER 0.0176→0.1226、D047 observation-only detection→relock family、P05 standard-CMA 0.00018/0.00117 的局部边界、P08-R2 single-pass caller、Sionna return_state=`msg_v2c` 语义以及 T001–T003 task-control validator PASS。

### 假设与截断合同

| 预卡 | 假设 | 否决条件 | 当前迭代计数 |
|---|---|---|---|
| C2 | true extrinsic 对 residual phase/CFO 的一次连续更新具有超出 hard/soft-DD 与 scalar calibration 的信息增量 | exact-action competitor 已覆盖；或 conventional 同预算完全解决；或 Step 3 无四判据问题 | candidate batch 1；scientific package 0 |
| C1 | decoder consistency 对有限 current-frame hypotheses 的重评分具有超出 receiver-only likelihood 的选择增量 | direct competitor 已覆盖；或选择不变；或退化为 final-correctness best-of | candidate batch 1；scientific package 0 |

本轮尚未运行任何 scientific package、adapter 或实验；失败截断计数为 0。

### Step 1 两轮检索与独立整合

1. C2 路由：37 raw / 30 unique / 3 actual sources / 正式发表 86.67%；2004 TWC APPA 摘要确认 `extrinsic LLR -> iterative ML phase estimation`，route terminal=`C2_EXACT_COLLISION_FOUND`。
2. C1 路由：28 raw / 19 unique / ≥6 source families / 正式发表 84.21%；官方 arXiv `2511.21340` 摘要确认 `decoder evidence -> finite candidates -> one selection`，route terminal=`C1_EXACT_COLLISION_FOUND`。该执行轮超出 15 分钟，已中断后用独立纯落盘轮收口；违规不抹除。
3. T006 fresh-context integration 独立把 TSP 2006 从 route exact 降为 strong neighbor，并确认 C1/C2 两个 core action exact。合并口径为 65 annotated rows→46 unique；39 published、6 must-read、7 source families；quality gate PASS。
4. 主控确定性复算解释了 46/39 与纯标题 47/40 的差异：DOI `10.1109/IDC.2007.374550` 的短/长题名是同一论文；分层合并只计一次。
5. replacement 门接受 0；没有 corpus-supported 且动作不同的新卡。D003 当时误映射为 `NO_VALID_PROBLEM`；D004 后续撤销该映射，但保留“不进入 Step 2 或 adapter”的 local terminal。

### T007 terminal verifier FAIL 与最小修复

1. T007 fresh-context verifier 结论为 `FAIL`，严重度计数 P0/P1/P2=`0/2/1`；它不推翻 C1/C2 collision receipt，也不授权重开 Step 2 或实现。
2. 核心 P1 是 `search-archive/2026-08-09/code-aided-phase-ambiguity-finite-phase-hypothesis-ldpc-deco.json` 的 28 条自动镜像未进入 T006 集成裁决。按 DOI/arXiv/规范化题名只与 integrated 46 精确重合 4 条，剩余 24 条必须逐条解释，当前 `replacement=0` 尚不可独立验收。
3. 另一个 P1 是 T007 超过 task brief 的 8 分钟硬上限；P2 是 registry/topic 展示元数据仍停留在 CP001/入口恢复。
4. 唯一允许的修复是：T008 在不联网、不新检索、不读全文的前提下逐条标注该 28 条镜像，合并生成可追溯的 integrated v2 并重新裁决 replacement；随后由新的 T009 在 8 分钟内按冻结检查项复验。
5. 若 T008 发现真正不同且有 evidence 的 carrier-recovery action，必须忠实改变 replacement/terminal 并进入显式再决策；禁止为了保住 D003 反向贴标签。若没有，则 D003 保持暂定，直至 T009 PASS。

### T008 镜像处置与 integrated v2

1. T008 在 `00:06:40.037` 内完成，本地操作边界合规：无联网、新检索、全文、Step 2、adapter、实现或实验；原 28-result 自动镜像未覆盖写回。
2. 镜像 28/28 已逐条处置：`DUPLICATE=8`、`IRRELEVANT=10`、`STRONG_NEIGHBOR=4`、`BASELINE=2`、`UNKNOWN=4`。四个 UNKNOWN 的 metadata/abstract 均不能识别 carrier-recovery action，因此不构成 corpus-backed replacement，但仍保留 unknown 身份。
3. 初稿曾想以摘要指纹把 `Phase Estimation by Message Passing` 并入 Springer 版本；独立分类反馈指出它没有共同 DOI/arXiv 且规范化题名不同，主执行方在时限内按冻结键纠正为独立 strong neighbor。最终计数由错误草案 93→65 修正为 **93→66**。
4. integrated v2 确定性复算：93 raw annotated、66 hierarchical unique、50/66 published=75.76%、must-read 6、source families 7、C1/C2 R2=`2/2`；17 个 input paths 与 93 个 provenance pair 全覆盖且无重复。
5. 新增可行动线索仍属于 joint iterative decoding/phase estimation、soft-decision PLL 或 conventional synchronization 邻域，不提供与 C1/C2/C3/D047/P08/P05/CCISP/Ch5 不同的 carrier-recovery action。C1/C2 collision 和 replacement=0 均保持，D003 待 T009 验收。

### T009 false protection alarm 与根因

1. T009 在 `00:04:43.000` 内完成，A/B/C 均 PASS；D 因当前四个 `p05_run*.log` 与任务书手写 SHA 不符而 FAIL，P0/P1/P2=`0/1/0`。
2. 主控随后从 HEAD 只读核查 `step4a-reopen-input-receipt.json`、T022 task brief、`step-3-rml-fsts-verifier.md` 等既有权威记录；它们的完整 SHA 与当前四个文件逐字一致，bytes=641/2417/929/1430，mtime 仍为 2026-07-30，且文件保持 untracked/unstaged。
3. 根因不是日志被修改，而是主控把压缩恢复摘要中的首尾缩写 `7843…F11 / 735E…38B / C768…34D / 95A1…1DE` 错误扩写成不存在的完整哈希并写入 T009。step-055 的 FAIL 作为执行历史保留，但不得作为 file-mutation evidence。
4. T010 必须从 `git show HEAD:projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-reopen-input-receipt.json` 动态读取 `protected_log_sha256`，再 fresh 比较；禁止继续手抄完整哈希。A/B/C 也须快速重跑，防止治理修订后漂移。

### T010/V001 artifact/protection 验收（语义结论后降为 PARTIAL）

1. T010 fresh-context 终验 A/B/C/D 全 PASS，P0/P1/P2=`0/0/0`。HEAD receipt、HEAD T022 与 fresh `p05_run*.log` bytes/SHA 4/4 一致；T009 根因正式裁为 `INVALID_TASK_CONTRACT`。
2. step-056 冻结检查窗口 `00:03:17.899`，agent 最终回执总耗时 `00:04:23.396`，两种口径均小于 8 分钟硬上限。
3. V001 原先接收 `STEP1_NO_METHOD_ACTION_SURVIVOR / NO_VALID_PROBLEM`；staged reviewer 证实后半映射越过 Step 3 Q# 语义门，故 V001 降为 PARTIAL。T010 对 JSON coverage、collision、Git/protection 的 PASS 仍保留。
4. H001 固化 future reopen 条件。当前没有 Q#、adapter identity、defect smoke 或 fair comparison 数字；它们均为 `NOT_RUN / NOT_AUTHORIZED`，不是零值或负结果。
5. 原关闭状态撤回，只为修复语义/治理并运行 T011；没有科学步骤重开。

### Staged review 与 D004 语义/治理修复

1. Fresh staged reviewer 结论 `Ready to commit: No — With fixes`，无 Critical、4 个 Important：`NO_VALID_PROBLEM` 越级、T009 回写破坏快照、H001 接收清单预勾选、V001/central report 模板与 current-vs-history 不清。
2. Framework 复核确认：`stages/glossary.md` 的 Problem 是 Step 3 形成的 M-C-A 四判据对象；本轮没有 Q#，只能裁 `STEP1_NO_METHOD_ACTION_SURVIVOR / STEP1_CANDIDATE_SET_EXHAUSTED`，problem=`NOT_EVALUATED_NO_Q_FORMED`。
3. D004 只取代 D003 的 mapping；C1/C2 exact collision、93→66、50/66、replacement=0 和下游冻结不变。
4. T009 已恢复派发时快照；错误 hash 根因留在 S001/D004/T010/step-056/V001。H001 receiver checklist 已复位为未勾选；V001 按 V 模板重构为 PARTIAL；central report 把 65→46 标为 historical v1，current authority 为 v2.1。
5. 当前唯一合法动作是 T011 fresh-context semantic/governance verification；PASS 后才允许 V002/H001/closed 收口。

### T011/V002 最终接收

1. T011 fresh-context verifier 在 `00:03:34.523` 完成冻结检查、`00:04:08.356` 完成最终复查，P0/P1/P2=`0/0/0`，A/B/C/D 全 PASS。
2. integrated v2.1 三层语义与数字独立复算通过：local=`STEP1_NO_METHOD_ACTION_SURVIVOR`、framework=`STEP1_CANDIDATE_SET_EXHAUSTED`、`canonical_mapping=null`、problem=`NOT_EVALUATED_NO_Q_FORMED`；93→66、50/66、6、7、R2 2/2、replacement=0。
3. current/history 分离、T009 派发快照、H001 未勾选接收清单、V001 PARTIAL 模板和 central report v1 supersession 全部通过。
4. HEAD=`1d76f917a89c719614aeefd7a165ab9819425978`；p05 HEAD receipt/T022/fresh bytes/SHA=`4/4 MATCH`，verifier 未改变 staging，唯一写入 step-057。
5. V002 正式接收 D004；专题在 CP005 关闭。方法产出=`NONE`，没有 Q#、adapter、fair comparison 或论文方法声称；未来只可凭不同 action 的新证据加显式 scope change 重开。

### 连续执行设计（用户规格已视为批准）

1. `Recover/Map`：P08/R/R2 lineage、T010 C1/C2/C3、贡献与 dead-end inventory、caller→callee interface 三路并行恢复。
2. `Converge`：按具体 M-C-A、runtime timing、action identity、direct competitor、strongest comparator、adapter BOM、章节图/消融/fallback 只留最多两个预卡。
3. `Groundwork`：严格执行 Step 1 search、Step 2 acquire、Step 3 子 agent 全文精读和必要 Step 3.5；至少一个 canonical Q# 四判据全过才进入 Step 4a。
4. `Step 4a`：先冻结 A0 并做 defect smoke；只有 B0/B1 真 failure、O1 可恢复、B2 未解决、decoder 信息可观测且语义门全过才建 adapter。
5. `Adapter/Comparison`：TDD 建最小接口，同包完成 semantic smoke 和 fair comparison；最终由 fresh-context verifier 独立验收。

## 决策引用

- D001：激活 3–7 天 coded decoder-feedback 方法生产 Groundwork（新建）。
- D002：两张机制不同预卡进入 Groundwork Step 1；C3 不再独立成卡（新建）。
- D003：Step 1 两张核心动作均精确碰撞、0 replacement、local terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR`；其 `NO_VALID_PROBLEM` mapping 被 D004 取代（新建）。
- D004：撤销 Step 1 到 `NO_VALID_PROBLEM` 的越级映射，problem 改为 `NOT_EVALUATED_NO_Q_FORMED`（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

无自动科学下一步。专题已按 D004/V002/H001/CP005 关闭；本对话只剩 staged diff 独立复审、最终确定性验证和统一一次提交，不 push。
