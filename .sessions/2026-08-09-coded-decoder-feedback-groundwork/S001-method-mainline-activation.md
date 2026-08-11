# [S001] Coded decoder-feedback 方法主线激活

> 2026-08-09 | Groundwork 恢复/候选收敛 | complete
> 2026-08-09 续接：T001–T003 验收完成，进入 Step 1
> 2026-08-09 续接：T007 终验 FAIL，限定为 Step 1 证据包修复
> 2026-08-09 续接：T008 修复完成，进入 T009 独立复验
> 2026-08-09 续接：T009 因主控错误哈希合同 FAIL，进入 T010 权威基线复验
> 2026-08-09 暂时收口：T010 artifact/protection PASS；后由 staged review 撤回语义关闭
> 2026-08-09 续接：D004 修正 terminal mapping，进入 T011 复验
> 2026-08-09 收口：T011/V002 PASS，CP005 关闭专题
> 2026-08-09 重开：用户 scope-change，D005/CP006 进入 Step 2 reference-baseline acquire/read
> 2026-08-11 收口：D024/V019/CP013 接收正式 I20 `GREATER_THAN_7D_HARD_BLOCKER`
> 2026-08-09 续接：D006/CP007 接收 5 篇全文 + 2 项全文债，进入 Step 3 Q# formation
> 2026-08-09 续接：D007/CP008 将 Q1 冻结为 provisional 3/4，定向补 TVT 2025 顶刊 baseline
> 2026-08-09 续接：D008/CP009 接收 TVT 顶刊 baseline，Q1 canonical 4/4，进入 mandatory Step 3.5
> 2026-08-10 续接：D009/V003/CP010 接收 Step 3.5 bounded-slice 证据包，限权进入 Step 4a A0 §0–§6
> 2026-08-10 续接：D011/V005/CP012 接收 D0 v3 静态资产合同，只开放实现、单测与后置非科学吞吐门

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

### D005 scope change 与 H001 接收核证

1. 用户显式撤回“exact action collision 必然终止 reference-method extension”的解释，把 C1 全局一次性 finite phase-hypothesis decoder selection 降为 reference baseline M；方法身份改按 `input→trigger→localization→action→decoder→fallback→budget→output` 完整签名裁决。
2. H001 关键事实 fresh 核证：`search-archive/2026-08-09/coded-decoder-step1-integrated.json` 为 schema v2.1，计数 93→66、published=50、must-read=6、sources=7，C1/C2 collision 仍为 `CORE_ACTION_EXACT`；`git status --short` 仅四个 protected `p05_run*.log` 未跟踪且未暂存；registry 中三项依赖分别为 dormant/dormant/active，current topic `conflicts_with=[]`。三项均 PASS。
3. 起点 HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`，分支=`codex/rdl-method-production-v2`，是 linked worktree；四个 p05 日志保持唯一未跟踪项。
4. D005 只取代 H001/CP005 的“必须出现新动作原子才可重开”和 downstream freeze 解释；D004/V002 的 corpus、core collision、`canonical_mapping=null` 与 `NOT_EVALUATED_NO_Q_FORMED` 继续有效。
5. 当前恢复路线检查：下一动作本身不创建方法，但全文精读是形成合法 Q#、区分完整链碰撞并授权 defect smoke 的必要门；same-axis/repair/no-method streak 均为 0，不触发 rotation 或 factory。

### 连续执行设计（用户规格已视为批准）

1. `Recover/Map`：P08/R/R2 lineage、T010 C1/C2/C3、贡献与 dead-end inventory、caller→callee interface 三路并行恢复。
2. `Converge`：按具体 M-C-A、runtime timing、action identity、direct competitor、strongest comparator、adapter BOM、章节图/消融/fallback 只留最多两个预卡。
3. `Groundwork`：严格执行 Step 1 search、Step 2 acquire、Step 3 子 agent 全文精读和必要 Step 3.5；至少一个 canonical Q# 四判据全过才进入 Step 4a。
4. `Step 4a`：先冻结 A0 并做 defect smoke；只有 B0/B1 真 failure、O1 可恢复、B2 未解决、decoder 信息可观测且语义门全过才建 adapter。
5. `Adapter/Comparison`：TDD 建最小接口，同包完成 semantic smoke 和 fair comparison；最终由 fresh-context verifier 独立验收。

### Step 2 全文包与 P08-R2 fresh audit

1. T012–T019 均通过 epoch 6/CP006 task-control；5 篇正文质量合格：arXiv 2511.21340、TSP 2006、GLOBECOM 2012、IWCMC 2023、TWC 2004。SPIE 12.3107192 与 ACCESS 2026 经三轮合规通道仍为 `UNRESOLVED_FULLTEXT`。
2. arXiv/TSP/IWCMC/TWC 只覆盖 whole-frame/window 的 decoder-aided global selection/update，均为 `PARTIAL_CORE_ONLY`；GLOBECOM continuous DD-PLL 为 `STRONG_NEIGHBOR`。可得全文没有 event-triggered boundary localization + bounded segment/suffix repair 的完整链。
3. IWCMC 2023 给出 27 个 global phase/NFO syndrome 点→5 个 decoder-CMF 候选→全帧 EM，成为 recent global B2 与明确成本锚；GLOBECOM/TWC 占据 decoder soft/extrinsic iterative CPR，禁止把“decoder 信息进入相位估计器”当创新。
4. P08-R2 fresh source audit把 decoder primitive 定为 `BOUNDED_ADAPTER`、carrier/action 定为 `TESTBED_GAP`；method-local最小链估算 5–6.5 日，尚无 `>7D_BLOCKER`。
5. D006 以用户预授权接受“5 篇全文 + 2 项债”的覆盖，并保持 adapter/实验冻结；控制面进入 Step 3，local defect 的 occurrence/observability/recoverability 仍未裁。

### Q1 provisional 四判据与最小修复

Q1 的具体 M-C-A、可复用完整动作链产出和 FER/goodput/cost 对标均可由全文形成；但项目判据 3 明确要求 2019 年至今顶刊，IWCMC 2023 不能因方法相关就冒充顶刊，ACCESS 2026 metadata 也不能承担可实现 baseline。因此 D007 暂记 3/4，只补读已在 integrated corpus 的 TVT 2025/arXiv 2309.12828，再回到 Step 3 裁决。

### TVT baseline repair 与 mandatory Step 3.5

1. T020 全文确认 DOI `10.1109/TVT.2025.3600028` 与 arXiv `2309.12828` 是同一工作的改题演进；2025 DOI/early identity、2026 正式卷期均满足 2019+，正文包含 ICE-CEM equations、Algorithms 1–2 与关键搜索参数。
2. ICE-CEM 的 code-aided evidence 是 Polar posterior LLR；状态仅为每帧、每卫星一个 global CFO/CPO。它没有 within-frame slip trigger、boundary localization、bounded segment/suffix repair、clean no-op 或 fallback，故为 `STRONG_NEIGHBOR` 而非 `EXACT_COMPLETE_CHAIN`。
3. D008 将 Q1 四判据裁为 4/4：Step 3 完成，但 occurrence/observability/recoverability/B2 absorption 仍未成为事实；只授权 Step 3.5 文献补检。
4. CP009 按框架立即派发关键词矩阵、最高引用核心竞品前后向引文链、coherent-optical/FSO 物理与 strongest B2 三路；adapter、defect smoke 与实验仍冻结。

### Step 3.5 三轮上限、全文闭债与独立验收

1. T021 query matrix 完成 9 组/两有效来源：raw 70、unique 63、MUST/SHOULD=2/5；T022 对最高引用可读核心 L05 做 forward 58/backward 21，引文摘要共筛 12；T023 建立 coherent-optical physical 与 pilot/non-data-aided B2 候选。
2. 新增全文家族包括 OFC2014 Markov turbo、ICTON layered rollback、Tikhonov 1204/1306、ECOC/OFC/1704 slip-tolerant FEC、PAPU、HTDD、2604 burst-aware LDPC 与 OFC2017 pilot soft-state。共同缺口仍是 decoder-anomaly trigger、explicit boundary/range、bounded local carrier action、selective re-decode、conditional fallback 与 local repair output 的全组合。
3. 收敛轮为 R2=`101 raw / 97 unique / 0 MUST / 2 SHOULD`，两篇全文均 non-exact；R3=`82/79 / 0/1`，故形式终态不是 zero-new，而是 `ROUND3_CAP_REACHED_WITH_NEW`。唯一 OFC2017 已全文确认 pilots→4-state soft slip probability→parallel LLR refinement，明确 no decision feedback，裁为 `STRONG_NEIGHBOR`。
4. T034 首个 Round-3 agent 超过 15 分钟且未落盘，已中断；step-080 salvage 只读现有 receipts 独立复算并记录该操作债。arXiv1704 的 downloader/read race 也已在 step-077 用正文 SHA 关闭，未把时序错误冒充 acquisition blocker。
5. T036/step-082 独立抽核 6 篇全文八字段，T037/step-083 独立复算全部轮次并抽核 OFC/PAPU/JLT 物理锚；两路均 `PASS, P0/P1/P2=0/0/0`。V003 接收 bounded-slice 非碰撞与 claim ceiling，CSSC/CS-DC/U01/U02 继续 fail-closed。
6. D009 把 Step 3.5 改为 `COMPLETE / VERIFIED_WITH_COVERAGE_LIMITS`，控制进入 CP010/epoch10 的 `GROUNDWORK_STEP4A_A0_PREFLIGHT`。只开放 A0 §0–§6 分析、理论上界、source audit 与 B2/testbed contract draft；defect smoke/MVE/adapter/实验继续禁止。

### A0 预检、三轮审查修复与 D0 限权开放

1. T039–T041/step-085–087 分别闭合理论 headroom/Gray-16QAM 映射、P08-R2 coded chain/TruthView/BOM，以及 prior/negative/B2 coverage 边界。A0 的稳定上限是：Q1 合法；uncoded symmetry loss 可解析；coded occurrence/headroom/B2 absorption/observability 仍为 UNKNOWN；候选是 non-ML deterministic finite search，不能借 ML 规则给出 Go。
2. step-088 首审 `FAIL 0/2/0`，指出 D0 gate 不定量与多-B2 envelope/BOM 冲突；step-089 复审 `FAIL 0/3/0`，继续指出 controlled exposure/合取、symmetry-tied comparator 与 B2 source contract 不可唯一执行。
3. 主控把 `d0-defect-smoke-contract.yaml` 冻结为唯一数值 owner：single source-explicit OFC2017-like B2、共享 pilot-bearing waveform、S1–S4 互斥职责、seed ranges、raw-row schema、B0/B1/B2/O1 ladder、truth boundary、成本与 7.00 日总预算。
4. step-090 全量 fresh verifier `FAIL 0/2/1`，但确认此前 B2/strata/exposure/symmetry/budget 等问题均 CLOSED；残余只剩 bootstrap/invalid replicate、S3 fusion objective/tie-break 与 report 的 post-D0 safety 误写。
5. 修订后 YAML 唯一冻结 10,000 次 PCG64 seed-cluster percentile bootstrap、逐 cell→equal-cell macro、NA/0.05/9500/双 terminal、pilot/decoder score normalization 与 dev-only lexicographic lambda selection；report 把 clean false-action/fallback/goodput safety移回 post-D0。
6. T045/step-091 窄复核只检查上述三项，结论 `PASS / P0/P1/P2=0/0/0`，P1-1/P1-2/P2-1 全部 CLOSED；owner 初末 SHA、YAML parse、task-control、staging 与 p05 4/4 均 PASS。
7. V004 接收 step-091；D010/CP011 只开放冻结 D0 testbed/diagnostic。当前 method signal 仍为 NONE，四 strata 全过前禁止 adapter/C1-ext/MVE/held-out；任一关键合取失败即 C1 hard terminal。
8. D010 的三条触发原话均逐字来自本轮用户原始合同 `C:\Users\zzt\.codex\attachments\121c6695-cba7-4963-a946-21f10e677f58\pasted-text.txt`：第 147 行“先完成 A0 §0–§6，再冻结 testbed 和判据。”、第 170 行“若任一关键条件失败，诚实终止，不构造复杂方法。”、第 174 行“只有 defect smoke 通过后才建设。”；`voice.md` 保持逐字记录，不标 `[转述]`。

### D0 资产闭合、失败血缘与实现限权

1. T048–T054/step-094–100 完成 coded-chain 资产映射、OFC17 B2 来源映射、raw/stat 修复、physical constructor、B2 数学复核与预算双账；结论是现有 kernel 可复用，但必须新建 truth-separated D0 shell，不修改 `common/`。
2. step-101 对 v2 给出 `FAIL 0/2/0`：HMM clean/controlled 权重未唯一绑定、BPS/B2 dev-freeze 只有 opaque hash。该失败不是 scientific terminal，且没有重开 scientific population/seed/gate。
3. step-102 给出纯 additive 修复；v3 冻结 clean/controlled-target `0.5/0.5`、sentinel 排除 objective 但仍 receipt/cost、七个具名 artifacts、五 BPS + 五 statistic + 一 final tuple，以及 test runner 不可达 fit functions。
4. T057/step-103 fresh narrow reverifier 给出 `PASS 0/0/0`、两项 P1 CLOSED、`94/94` 静态断言通过，抽核范围内 scientific-field drift=`NONE_FOUND`；pre-transfer owner/report SHA 分别为 `6924842c...c81f54` / `e008c0f0...bc01f1`。
5. V005 接收上述失败→修复→复核血缘；D011/CP012 只开放 D0 implementation、unit test 和实现/单测/独立代码审查后的 12 分钟非科学 throughput benchmark。`DEFECT_SMOKE`/S1–S4 仍关闭，D0=`NOT_RUN`、method signal=`NONE`。

### I02 truth-boundary 分层试错计数器

- `iteration 0 / FAIL / step-112`：literal alias denylist 与 opaque ndarray 外壳使 9 个 owner-equivalent truth 名和 object/structured ndarray 绕过；否决“6/6 当前测试即闭合”的假设。
- `iteration 1 / PARTIAL FAIL / step-114`：T067 已关闭 step-112 的已知 9+4 cases，但 fresh unseen taxonomy 抽样仍有 8 类、24 个变体被接受；否决“补已知词并加少量 token rule 即具备类别完备性”的假设。
- `iteration 2 / PASS / step-116`：owner taxonomy 组合规则经 fresh 生成矩阵验证，forbidden `740/740` 全拒、safe controls `12/12` 全收、object/structured/non-numeric ndarray `4/4` 拒绝、fresh tests `6/6`；denylist 路线在退出阈值前闭合。
- **否决条件 / 退出判据**：iteration 2 若仍接受任一可从 owner `views.ReceiverView.forbidden` 推出的同义字段，立即截断 denylist 路线，改为 typed/allowlisted receiver metadata；禁止第四轮词表补丁。
- action permission 的 step-112 P1-3 经 T065 原始 oracle 复核为 `DISPOSED_NON_DEFECT`：true→false 只移除对应 capability，是严格子集而非 fail-open；CP/D/V/epoch/action-class 或 execution/science 漂移仍清空全部。

### I05/I06 独立审查后的实现状态

1. I05 partial exact coverage 已在 step-132 关闭，但 T088 的 FULL 草稿虽有 10/10 schema 与 6/6 I02 GREEN，独立预审仍发现 forged FULL、HMM group binding、consumer-ledger binding 和 positive oracle 四项 P1；step-134 因此诚实收口 `INCOMPLETE`，P1-1b 继续 open。
2. I06 作者侧 step-133 为 9/9 waveform-channel、6/6 I02、8/8 negative GREEN；step-135 fresh verifier 仍给出 `FAIL 0/3/1`。物理方程/RNG/sharing 通过，失败集中在 physical-SNR 值泄漏、slots/shape/finiteness/identity fail-closed、payload truth 空占位与 scalar bounds。
3. D012 接受上述缺陷，并冻结因果两阶段 TruthView：info/coded bits 在 channel 构造时完整且必须绑定 canonical encode/Gray-map/waveform data positions；逐偏振 `C_pre` 保持 typed receiver-derived 主字段；final correctness 只能在 deployable output freeze 后由 evaluator 从 decoded bits 计算。不得以空数组或预填真假冒充 pending。
4. T090 取得 36/36 aggregate GREEN 后，step-137 仍以 64 个 fresh mutation 找到 9 个错误接受，裁为 `FAIL 0/3/0`：module token 可伪造 correctness、`C_pre` 可与 received prefix脱钩、generic receipt对象可事后变异。D012 因此进一步冻结 init-free derived fields与 immutable-tree-only receipt；I06 仍未接收。
5. T092 关闭 step-137 旧 9 项并取得 39/39 aggregate GREEN，但其最后静态收紧未获作者侧 fresh rerun，诚实停为 INCOMPLETE。step-139 对最终字节 fresh 重跑仍为 39/39 GREEN，却在 73 个独立 mutation 中发现 10 个新错误接受，裁为 `FAIL 0/4/0`：stored correctness、opaque mutable built-ins、physical-noise alias 与 NumPy integer root 四类结构缺口。D013/V006 保留失败血缘；I06 继续 FAIL。
6. T094 以真实 4/4 RED关闭上述四类缺口；T095 因平台过滤无日志、T096 因时间盒只有 pytest 证据，均未接收。T097 对最终字节 fresh 验证 exact 4/4、aggregate 43/43、126-case mismatch=0、C_pre 8/8，裁为 `PASS 0/0/0`；V007 接收 I06，只开放继续 I05 与后续实现单测，不开放 benchmark/science。
7. I05 authority切片T098取得3/13/46 GREEN与34项作者负例，但T099在88个正常cases后发现shared cached canonical instance可被改变并让factory/validator共同接受digest不一致对象，裁为`FAIL 0/1/0`。D014/V008拒绝object-returning cache路线；raw positive、HMM/member、consumer-ledger仍OPEN。
8. T100将cache降为primitive tuple并fresh materialize完整authority graph；T101 final-byte验证tests 2/15/48、700对nonprimitive共享0、56 cases mismatch=0，裁为`PASS 0/0/0`，V009接收FULL authority。R001/D015同时冻结后续HMM/consumer-ledger canonical identity v1；owner YAML transfer未验收前不得实现bindings。
9. T102在owner写入前发现R001只保存了combined root、未保存exact payload shape，按15分钟硬时间盒以step-148=`INCOMPLETE_OWNER_IDENTITY_TIMEBOX`停止；owner保持`c61c88e...`且未执行prechange RED。随后从历史原始tool/PASS记录恢复`hmm_grid_commitment.v1`嵌套完整`p_s`/`sigma_e2` standalone payload的唯一shape，并fresh复算三个root均PASS；R001已补持久证据，D015与science identity均不变，须从未改owner另开作者任务。
10. T103 author-side 330项全绿后，T104因Windows code 206在Python启动前停为INCOMPLETE；T105用step-log fence→stdin完成720项独立验证，128/128 literals、3/3 roots、15/15 mutations、6/6 counts及保护均PASS，但S2/BPS两个manifest因hash-bearing `binding_kind`未落owner authority而为8/10 golden、`FAIL 0/2/0`。D016/V010拒绝接收当前owner，只开放统一literal `LOGICAL_COMPUTATION_ID`的owner-only窄修；该值fresh复算命中两个既有root。
11. T106以11/11缺失RED后补global+8 projections+2 golden inputs；T107对最终owner `ca2c8146...`独立执行729 assertions，authority 11/11、literals 128/128、roots 3/3、goldens 10/10、mutations 15/15、counts 6/6、mismatch=0，裁为`PASS 0/0/0`。V011接收D015 owner transfer；只开放I05 raw FULL positive与HMM/member/consumer-ledger schema TDD，benchmark/science仍冻结。
12. T108以4/4真实RED实现additive typed owner loader；T109对final bytes fresh执行430 assertions、128 literals、3 roots、8 anchors、31/31 mutations、四文件52/52与I06 34+7 cases mismatch=0，裁为`PASS 0/0/0`。V012接收loader结构与当前owner seal。
13. Schema-readiness两路独立审查随后发现ordinary projections缺phase/operation/work-key kind/typed PK authority，且HMM chunk实际引用manifest root而非logical ID。D017冻结七类ordinary exact identity descriptors并分离HMM manifest reference；owner-only repair及loader seal刷新前不得实施compiler。
14. T110从41项pre-edit RED补齐D017 owner；T111不复用作者helper，fresh执行920 assertions、58/58 mutations、descriptors 32/41/49、10/10 goldens、6/6 counts与全部identity总量，裁为`PASS 0/0/0`。V013接收owner `02d471a...`；下一步只刷新loader seals。
15. T112刷新final owner/identity seals；T113以1107 assertions、48/48 mutations、I06 35 cases及4+1+53 pytest裁为`PASS 0/0/0`，V014接收final typed authority。两路compiler-readiness审查同时发现B2-controlled shared logical ID与现有单值ledger provenance冲突；D018只开放ordinary identity-only T114，不允许猜cache语义。
16. T114作者侧RED 4/4后取得42967/27487、24/24 mutations、53/53回归；T115却在同一owner/seals下替换module `CANDIDATES`并生成/接受1080个未授权identity，裁为`FAIL 0/1/0`。D019/V015只开放从已认证full owner提取独立sealed typed ordinary-domain view并rewire compiler。
17. T116不改owner bytes提取sealed ordinary-domain view并rewire compiler；T117独立复算15字段/domain seal、9/9 globals、22/22 mutations与42967/27487逐条identity，共438313 assertions，pytest 22+54全绿，裁为`PASS 0/0/0`。V016正式接收ordinary identity compiler。
18. 两轮provenance/output审查确认raw统计或receipt不能证明decoder content；D020冻结16×1024 hard-output content store、per-logical provenance sidecar、codec immediate typed-ref write anchor与七类cache/source规则，保持base raw/scientific projection不变。
19. T118完成D020 owner transfer；T119在硬停前独立重算10/10新golden并拒绝11/11 version mutations，P0/P1=0/0，但完整50-case矩阵仅11项，V017=`PARTIAL 0/0/1`。D021识别M4/M6节奏风险，取消重复owner-only轮次，把遗留覆盖并入T120后的fresh loader终验；之后I05只保留三个实际代码切片。
20. T120以2/2真实RED更新两枚loader seal，随后42/42 mutations、16项contract与显式五文件62/62 GREEN。用户再次质疑全天级过度慎重后，D022取消未派发的loader-only T121，把全部独立验证债并入I05三代码片后的唯一batch verifier；T121编号改用于typed hard-output实际实现。
21. T121–T124完成typed hard-output、ordinary provenance、HMM runtime/FULL positive与重复编译hotpath修复；T125唯一fresh batch实跑五文件`71 passed / 686.12s`、118项负向0错收/错拒、FULL incremental 17.895242s，V018=`PASS 0/0/0`正式接收I05。D0 science仍`NOT_RUN/NONE`，当前并行进入I07/I08 implementation/unit。
22. T126/T128完成I07，SS01–11局部门`10/10`；T127完成I08，AC01–06+窄回归`19/19`。两者author gate均`PASS 0/0/0`，下一对话只做一次合并focused verifier，随后直接I09/I11；H005取代H004成为当前入口。
23. I07/I08合并快验`25/25`后，I09–I17A按真实RED→GREEN完成receiver/BPS、ledger/S4、dev-freeze/HMM、B0/B1/O1、freeze chronology、B2、engineering benchmark与deployment seal；I18 aggregate=`133/133`。
24. I19A/B/C独立审查发现7项P1并完成最小修复；I19D final integration=`189/189`、P0/P1=`0/0`。I20四类允许调整实测后，EB final=`36/36`。
25. 正式I20仅运行一次，shell wall=`25.7s`、`incomplete_reasons=[]`；owner workload投影D0=`10.819450931739858d > 7.0d`。D024/V019/CP013裁为真实`GREATER_THAN_7D_HARD_BLOCKER`；S1–S4/FAIR_COMPARISON_RUN保持NOT_RUN，method signal=`NONE`。

## 决策引用

- D001：激活 3–7 天 coded decoder-feedback 方法生产 Groundwork（新建）。
- D002：两张机制不同预卡进入 Groundwork Step 1；C3 不再独立成卡（新建）。
- D003：Step 1 两张核心动作均精确碰撞、0 replacement、local terminal=`STEP1_NO_METHOD_ACTION_SURVIVOR`；其 `NO_VALID_PROBLEM` mapping 被 D004 取代（新建）。
- D004：撤销 Step 1 到 `NO_VALID_PROBLEM` 的越级映射，problem 改为 `NOT_EVALUATED_NO_Q_FORMED`（新建）。
- D005：保留 core-action collision 事实，以完整 deployable action chain 重开 C1 reference-method extension（新建）。
- D006：Step 2 五篇全文覆盖通过，带两项全文债进入 Step 3（新建）。
- D007：Q1 暂为 3/4，定向补 TVT 2025 顶刊 baseline 后再裁 Step 3（新建）。
- D008：TVT 顶刊 baseline 闭合 Q1 四判据，强制进入 Step 3.5（新建）。
- D009：Step 3.5 三轮与全部新增全文债经 V003 接收，带 claim 限制进入 Step 4a A0 分析预检（新建）。
- D010：A0 条件通过时开放冻结 D0；其 scientific gates/terminal 继续有效，当前执行授权被 D011 取代（新建）。
- D011：接收 v3 实现前静态合同，只开放实现、单测与后置非科学吞吐门；S1–S4 继续冻结（新建）。
- D012：TruthView 采用 payload 构造时完整、final correctness evaluator 后置计算的因果两阶段生命周期（新建）。
- D013：拒绝把 T092 最终字节视为 I06 闭合，只允许在 D012 内做四项结构窄修复（新建，rejected-route record）。
- D014：拒绝共享缓存canonical对象作为FULL authority；recompile必须fresh或只缓存immutable bytes/digest（新建，rejected-route record）。
- D015：冻结D0 dev-manifest/HMM/consumer-ledger canonical identity binding v1；先转入owner再实施schema（新建）。
- D016：拒绝省略consumer `binding_kind` authority的owner transfer；统一冻结`LOGICAL_COMPUTATION_ID`并保持两个既有root（新建，rejected-route record）。
- D017：补齐ordinary consumer canonical identity authority，并把HMM chunk分离为computation-manifest reference（新建）。
- D018：ordinary canonical identity/binding先独立编译；per-consumer provenance与aggregate ledger后置原子修复（新建）。
- D019：ordinary枚举domain必须来自已认证owner projection，禁止schemas globals/literals充当authority（新建）。
- D020：ordinary runtime content采用hard-output content store与per-logical provenance sidecar，禁止raw receipt冒充可复用content（新建）。
- D021：owner遗留覆盖并入loader终验；I05收敛为三个实际代码切片，禁止无新P0/P1时继续纯readiness复审（新建）。
- D022：取消loader-only实现前阻塞；三代码片完成后一次性fresh验收loader+I05（新建）。
- D023：FULL wrapper只消除已认证ordinary bundle的重复全量编译，public deep verifier与science权限保持不变（新建）。
- D024：正式I20完整投影D0超过七日冻结上限，C1在science前硬终止；禁止缩减workload或把工程底座包装成方法（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

D024/V019/CP013已接收正式I20真实hard terminal；无合法science/adapter/FAIR_COMPARISON_RUN下一步。未来只有显式scope change且有不缩减owner workload的新工程证据时可重开。
