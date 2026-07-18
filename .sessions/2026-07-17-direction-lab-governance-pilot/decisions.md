# Decision Records — Direction Lab 可遵守性与控制器试运行

## D001: 采用审计账本背书的最小 decision receipt 与 evidence gate

> status: active
> date: 2026-07-17
> 取代：无
> 被取代：无
> 依据：调研: `.sessions/framework-evolution/R002-direction-lab-design.md` + 验证: V002/V003 + 用户原话: `voice.md` 2026-07-17

### 决策

每次 controller 决策生成绑定 `decision_id`、`run_id`、`action`、canonical manifest hash 与 allow/blocked 状态的 receipt；operation 仅通过 `execute()` 返回携带 receipt 的结果 envelope；evidence gate 只接收能与审计账本逐字段核对的 receipt，并按 evidence ledger、promotion board、formal materials 三类目标限制动作。

### 理由

纯内存 token 无法支持恢复测试；完整签名/可信 registry 超出本轮最小 pilot。审计账本背书可用确定性接口验证“走过 controller”，同时保留跨实例恢复能力。

### 排除的替代方案

- 不采用纯内存 opaque token：新上下文或新进程无法恢复。
- 不采用自声明 receipt：调用方可伪造，不能证明经过 controller。
- 本轮不采用签名、密钥管理或不可变数据库：范围和复杂度超过 pilot。

### 影响范围

仅影响 `projects/simulation/verify/direction_lab_pilot/`、对应测试与本专题记录；不修改 canonical baseline、正式实验入口或论文材料。

### 来源

S002 / 用户明确任务约束

## D002: execute 结果必须有审计 execution 记录并防止 replay

> status: active
> date: 2026-07-17
> 取代：无
> 被取代：无
> 依据：验证: V004/V005 + critic: 独立 verifier 复核

### 决策

在 D001 receipt 之外，`execute()` 必须为实际 operation 结果写入 execution audit event 与 `result_hash`；evidence gate 必须同时核对结果 hash、execution event 和 destination 幂等性，篡改结果标记 `UNTRUSTED`，同一 receipt 在同一目标重放标记 `REPLAY`。

### 理由

V004 黑盒复核证明仅凭合法 decision receipt 可以承载伪造 result，也可以重复写入 ledger；这直接违反“只有 controller.execute 产生的结果可验收”。execution event 是不引入签名系统的最小 provenance 绑定，replay 门避免账本污染。

### 排除的替代方案

- 不把“调用方保证不篡改 envelope”当作验收门：黑盒已证明不可靠。
- 不在本轮引入签名、密钥管理或不可变数据库：仍列为完整性债务。

### 影响范围

仅影响 pilot controller、evidence gate、定向测试和本专题运行产物；不改变 canonical baseline 或正式材料。

### 来源

S002 / V004 独立 verifier 发现 / V005 修复后复核

触发原话：无（技术推导）

## D003: 真实地基是约束与证据源，不是 ML 候选边界

> status: active
> date: 2026-07-17
> 取代：H004 初版的窄候选解释
> 被取代：无
> 依据：用户范围纠正 + 双偏振 OSL 地基 D042 的软件 DSP/ML 开放范围

### 决策

真实运行的目标是系统寻找 ML 在双偏振星地 OSL 场景完整处理链中的任何合理应用、方法和改进。既有 CMA-fade/SOP/pilot 候选地图只作为种子和负面证据，不是封闭全集；旧 Kill 只约束原具体 M-C-A、实现和有效域，不自动否决整个 ML 方法族。

### 理由

若把“复用地基”解释为只续跑既有候选，会再次形成单点锚定，违背 Candidate Universe 先全景后排序的设计。地基应冻结已知事实和避免重复踩坑，同时允许从完整接收/处理链枚举新的 ML 应用点、方法族和改进维度。

### 影响范围

修正 H004 的候选生成与排序范围；不改变双偏振星地 OSL 场景边界、canonical baseline、证据门和论文输出门。

### 来源

用户原话见 `voice.md` 2026-07-17。

## D005: B001 v1 流程结论降级并以不可变 v2 门控重跑

> status: active
> date: 2026-07-17
> 取代：无
> 被取代：无
> 依据：验证: V008 + critic: current-state independent verifier

### 决策

B001 v1 的运行完整性继续保留，但“完整流程已闭环”降为 PARTIAL；不得原地改写已被 manifest 哈希冻结的 CandidateMap/BatchQueue/runner。新建 v2 Map/Queue 和无标签 clean-control AE，通过独立 pre-run gate 后运行替代批次，再由独立 verifier 与 Batch Synthesis 收尾。

### 核心失败机制

1. CandidateMap v1 的分数由人工录入，缺少按声明 weights 的确定性校验，导致多项 score 与排序算术不一致，独立门控误报 PASS。
2. `C24-SSL-AE` 实现以 train fixed-label `y==0` 筛 clean rows，虽然没有 test leakage，但机制实际是 oracle-supervised clean-row reconstruction，而不是预注册的无 event-label self-supervised detector。

### 否决了什么

- 否决把 V007 的 runtime-integrity PASS 扩张为整个 Map→Queue→Run 流程 PASS。
- 否决把旧 AE 的 `RETIRE_SPECIFIC` 扩张到真正 self-supervised/generative 方法族。
- 否决通过原地修订 v1 Map/Queue 或结果文件来追溯性“修好”旧 gate。

### 可复用部分

- B001 的 30 cells、standard-CMA baseline、fixed/PI 指标、controller receipt、EvidenceGate、17-file source closure 和监督式两候选结果继续作为 exact-domain sandbox evidence。
- U24 在按声明 weights 重算后仍是第一候选，因此可在 v2 中保留同一问题族与共享实验合同。

### 具体数据

- score 例：U24 文件值 4.15、按声明 weights 为 4.20；U18 文件值 3.00、按声明 weights 为 3.25。
- 旧 AE 在 control-rate test 的 false alarm 为 0.40、event recall 为 0；该经验失败只适用于 oracle-label-filtered clean reconstruction 实现。

### 影响范围

新增 v2 Map/Queue、评分 gate、无标签 AE 和替代批次；formal Step 3.5/4a、canonical baseline 与论文材料仍不变并保持 BLOCKED。

### 来源

S004 / V008

触发原话：无（技术推导）

## D004: pilot 扩展为真实地基 sandbox 运行但不等同正式 Groundwork 晋级

> status: active
> date: 2026-07-17
> 取代：topic-index 原“只测治理、不寻找新算法”的当前范围与对应不变量
> 被取代：无
> 依据：用户显式 scope change + H004 live foundation run

### 决策

本专题从纯治理 shadow pilot 扩展为真实研究地基上的 Direction Lab sandbox：先建立完整 ML Candidate Universe，再形成 CandidateMap、BatchQueue，并在门控通过后运行一个小型 paired batch。运行结果仍只进入隔离的 Direction Lab 证据链，不自动进入正式 Groundwork、论文材料或 canonical baseline。

### 理由

用户已明确要求“把 Direction Lab pilot v1 用到真实研究地基上”并连续跑完第一批；继续把“只测治理”当硬阻断会与本轮授权直接冲突。保留 sandbox、receipt、evidence gate 和论文晋级隔离，可在不篡改原 Groundwork 状态的前提下执行真实候选。

### 影响范围

允许创建 `projects/thesis-fso/direction-lab/` 下的 anchor、候选全景、地图、队列和隔离批次产物；不允许把 current-CMA/no-z 当 baseline，不允许修改 canonical baseline，不允许绕过 thesis-fso 当前 Step 3.5/Step 4a 门控。

### 来源

用户原话见 `voice.md` 2026-07-17。

## D006: v3 显式区分 operative 与 audit-only 运行字段

> status: active
> date: 2026-07-18
> 取代：无
> 被取代：无
> 依据：验证: `projects/thesis-fso/direction-lab/tests/test_v3_governance.py`（12 passed）+ 独立 verifier 对 v3 的最新复核 + 用户原话 `voice.md` 2026-07-18

### 决策

v3 contract 继续显式声明 `channel_block、r2、fade_threshold_h、clip_norm、t_s、method`；其中 `fade_threshold_h` 与 `clip_norm` 在 canonical standard-CMA 路径中明确标记为 `audit_only/non-operative`，不得被解释为影响 baseline 数值的可操作参数。

### 理由

独立复核确认这两个字段会进入 config，但 canonical `prompt013` 的 standard-CMA 计算不消费它们。把它们标为 operative 会造成“合同声明”和“实现真相”不一致；修改 canonical baseline 又违反不可变地基约束。显式标记 audit-only 可以保留参数可追溯性，同时阻止伪造性能归因。

### 排除的替代方案

- 不修改 canonical baseline 以强行消费两个字段；canonical baseline 是冻结地基。
- 不静默保留为“好像生效”的默认字段；这会形成语义污染。
- 不从 v3 合同删除字段；当前治理要求六个字段显式声明，删除会重新引入合同不完整。

### 影响范围

影响 `batch-queue.v3.yaml` 的 `runtime_field_effects`、v3 validator 与 verifier 门控；不改变 B002、v2、canonical baseline 或论文材料状态。正式性能批只有在该声明进入 Queue gate 后才可继续。

### 来源

S004 续接 / 独立 verifier 最新复核 / 用户纠偏。

## D007: 将 Direction Lab 固化为三层机制族批量流程

> status: active
> date: 2026-07-18
> 取代：R002 中仅作为设计草案的单一重流程解释
> 被取代：无
> 依据：B002/B003 verifier 与 synthesis 对照 + `projects/thesis-fso/direction-lab/process.md` + 用户原话："你把咱们目前的流程文档（理论上之后要弄成skill，我不知道现在是什么形态，你给更新一下）"

### 决策

Direction Lab 采用 `Scout → Sandbox Batch → Promotion/Deep Evidence` 三层流程。Scout 负责一次性完成机制族全景、覆盖审计和 BatchPlan；Sandbox 负责共享合同下的轻量批量运行；只有稳定 winner 才进入重型 GW/Contract 与正式材料门控。脚本/状态机负责允许与阻断，skill 未来只负责导航和调用。

### 理由

B003 的治理链验证通过，但其 U24 数字与 B002 exact contract 重合，新增研究信息很少。若每个微变体都重复 Queue、Registry、独立复核和 synthesis，治理成本会压过方向探索。分层可以保留 provenance 硬门，同时把重流程留给真正晋级候选。

### 新增不变量

- `projects/thesis-fso/direction-lab/process.md` 是项目级执行规范的唯一拥有者；README 与 implementation-plan 只做入口/里程碑摘要。
- `canonical-state.yaml` 的完成状态必须通过 append-only completion event + state reducer 更新；不能用事后修改运行快照的方式解决状态债务。
- B002/B003 exact-domain U24 结果不得作为下一批“新方向”重复运行。

### 影响范围

影响 Direction Lab 后续 Scout、Sandbox Batch 和 Promotion 的排序与门控；不改变双偏振星地 OSL 场景、canonical baseline、B002/B003 历史产物或 formal Groundwork 当前 BLOCKED 状态。

### 来源

用户原话见 `voice.md` 2026-07-18；B003 verifier/synthesis；`process.md`。

## D008: completion event 是事实源，canonical-state 是 reducer 投影视图

> status: active
> date: 2026-07-18
> 取代：无
> 被取代：无
> 依据：`projects/thesis-fso/direction-lab/state/completion-events.jsonl`、`state/projections/821415346437f47de064966fdaa768242c63d2d660ea189e88a4a0dfb51995b0.yaml`、`tests/test_state_reducer.py`（5 passed）、B003 独立 post-run verifier

### 决策

运行完成事实只允许追加到 `state/completion-events.jsonl`；`canonical-state.yaml` 不再作为运行源码快照，而是由 immutable content-addressed pre-state projection 与严格 hash-chain reducer 物化的当前视图。B003 的旧 canonical bytes 保留为 SHA=`821415346437f47de064966fdaa768242c63d2d660ea189e88a4a0dfb51995b0` 的 projection，B003 completion event 的 head 为 `39d85d029a90cf6719d4b03cffc4cce811006d8faec4663c3d2ef3889e8de976`，当前 projection SHA=`5967ea38e676b46cb092c98060bec5b470b5a03625f21e65218cf3b2ae3a88af`。

### 理由

B003 原运行链把可变 `canonical-state.yaml` 纳入 source closure：不更新则状态停在 B002，更新则 B003 的历史 source SHA 失配。内容寻址 pre-state、append-only event 和 materialized view 解开这个循环，同时保留现有文件式消费者。

### 硬边界

- 不修改、删除或覆盖 B002/B003 manifest、result、execution-status、ledger、verifier 或 synthesis。
- reducer 只能更新 sandbox completion/history；baseline、metric、simulator、formal state 和 promotion 字段逐字段保持不变。
- 事件必须顺序连续、`prev_event_hash` 严格链接、证据指针和 hash 可验证；重复 event/run/batch、stale pre-state、未知 schema 或非法 delta 均 hard fail。
- B004 暂不运行；未来 runner 另建 v4 contract，manifest 用 `pre_state` 引用 projection/head，不把 mutable top-level projection 放入 source closure。

### 影响范围

新增 `direction-lab/state/` 和 `tools/reduce_state.py`；运行流程由 `process.md` 唯一拥有者更新。B002/B003 历史 provenance 通过旧 SHA projection 回退，不回写历史文件。

## D009: P01 先冻结 U25 因果动作接口，再补运行绑定

> status: active
> date: 2026-07-18
> 取代：无
> 被取代：无
> 依据：技术推导: `batch-plan.v1.yaml`、`u25-action-contract.v1.yaml`、`test_u25_action_contract.py`；触发原话: 无（技术推导）

### 决策

U25 的第一步只冻结 Scout contract：在线事件的必需字段、因果可用性检查、`NO_OP/Safe_Baseline/RESET` 动作集合、固定安全策略比较器、无动作恒等性和确定性回放。该 contract 不提供物理字段默认值，不读 oracle 或未来信息，也不创建 PASS Queue。事件生成器、fork-replay 数据、runner/registry binding 和 Sandbox 指标仍是后续门控。

### 理由

B003 只有 U24 causal detector trace，没有 U25 的动作、恢复和安全代价证据。先把动作信息接口与回放性质冻结，才能避免把 detector 分数误当成 safe-fallback 实现；同时保持 B004 禁止和 standard-CMA canonical baseline 不变。

### 排除的替代方案

- 不把 B003 detector 分数直接包装成 U25 action policy。
- 不在缺少事件生成器、共享 fork-replay 和 runner fingerprint 时创建 Sandbox-ready queue。
- 不把 adjacent 16-APSK fallback prototype 当作本场景实现。

## D010: P01/U25 在当前 standard-CMA 链上阻断并转查 P02

> status: active
> date: 2026-07-18
> 取代：无
> 被取代：无
> 依据：验证: `tools/u25_sandbox_preflight.py`、`tests/test_u25_action_contract.py`、`tests/test_u25_sandbox_preflight.py`、独立 verifier；用户原话见 `voice.md` 2026-07-18

### 决策

P01/U25 标记为 `P01_BLOCKED`，不创建 Queue/Registry，不进入 Sandbox。阻断依据是当前 standard-CMA runner 没有 receiver state snapshot、per-decision action hook 或 post-action output，因此 `SAFE_BASELINE/RESET` 无法产生真实可观测干预；`run_v3.py` 仍硬编码 U24，不能用 U25 contract 文件掩盖 runner 未就绪。P02/U10 改为下一候选，但只允许做 carrier-impairment、双偏振 CPR 和 receiver-only event contract 的轻门控，不允许直接跑性能批。

### 失败机制

- `u25_action_contract.apply_action` 只改变 Python metadata state，不改变 CMA weights、`zX/zY` 或后续 receiver path。
- standard-CMA blind trace 只有 `output_start/output_end/cm_error/output_power/update_norm`；可生成 receiver-only proxy event，但不能证明真实 lock state 或 action effect。
- `run_v3`/validator/registry/source closure 仍绑定 U24，U25 没有合法的通用入口。

### 可复用资产

- B003 artifact 中真实 standard-CMA blind trace 与字段来源；
- U25 event schema、source pointer 和 oracle/future/post-hoc 拒绝测试；
- fixed-safe-policy contract 与 deterministic replay contract；
- prompt013 的 online/frozen diagnostic branch（仅作结构参考，不宣称 U25 action 已生效）。

### 排除的替代方案

- 不把 `1/(1+cm_error)` proxy 叫作已验证的物理 lock score。
- 不把 prompt013 的 frozen branch 或 U24 detector 数字直接包装成 U25 safe fallback 结果。
- 不修改 standard-CMA canonical baseline 或回写 B002/B003。

## D011: DL-Process v0.3 下 P01 延后，P02/P03 先做能力分诊

> status: active
> date: 2026-07-18
> 取代：D010 中将 P01 表述为普通 BLOCKED 的后续执行标签；D010 的具体失败证据仍保留
> 被取代：无
> 依据：`projects/thesis-fso/direction-lab/process.md` §2、`profiles/communications.yaml`、`adapters/dual-pol-osl.yaml`、`scout/capability-triage.v1.yaml`、P02/P03 只读核对

### 决策

从现在起采用 Universal Core + Communications Profile + dual-pol OSL Project Adapter。P01/U25 的当前状态固定为 `DEFERRED_ARCHITECTURE`：不再修补 U24 runner，不伪造 state/action/replay。P02/U10 和 P03/U19 只进入 Capability Triage，不创建 Queue/Registry/fingerprint，不运行 B004 或性能实验。

本轮分诊结果为 `B_ALL_CANDIDATES_NOT_RUNNABLE`：P02/U10 是 observational + estimative，但双偏振载波受损、CPR、phase/innovation/confidence trace 和真实事件库未闭合；P03/U19 是 estimative（残差诊断可作 observational 前置），虽有 standard-CMA 内存 `zX/zY`，但现有 v3 artifact 丢弃它们，且合法 CSI/noise 来源、残差 artifact 和同信息量解析 comparator 未绑定。

P03 是最短闭合路径，但“短”不等于已就绪。只有补齐 z-window adapter、合法 CSI/无 CSI 声明、残差 artifact 和 analytic comparator 后，才可再判定 `SCOUT_CONTRACT_READY`。若该闭合失败，再回到开放 Candidate Universe，优先检查 U23 连续质量估计是否能形成与 U24 不重复的输出头；不把它默认视为可运行。

### 硬边界

- 不修改、删除或重跑 B001–B003；不修改 canonical baseline。
- 不把 SOP/Jones/CMA 失败重命名为 carrier lock/cycle-slip。
- 不把 B003 blind trace 当作 U10 CPR trace；不把 `h/theta/TX/BER` 当 runtime CSI 或事件输入。
- 不建立 PASS Queue，不创建 registry/fingerprint，不启动 B004。

### 触发原话

- “P01/U25 保持 DEFERRED_ARCHITECTURE，不要继续为 U25 修补当前 U24 runner，也不要为了让它通过而伪造 state/action/replay 接口。”
- “不要先写完整 Queue、Registry 或 fingerprint。”
- “本轮目标不是跑 B004，而是完成一次跨候选 Capability Triage，并得到一个明确结果。”

### 来源

本轮 Capability Triage 只读核对与 `scout/capability-triage.v1.yaml`。

## D012: P03/U19 Interface Closure 只晋级 Scout Contract

> status: active
> date: 2026-07-18
> 取代：D011 中 P03 尚未闭合的具体状态；不取代 P01 `DEFERRED_ARCHITECTURE` 或 B004 禁止
> 依据：`scout/P03-U19-residual-headroom/readiness-report.yaml`、独立 verifier V018、35 项 P03 专项测试

### 决策

P03/U19 达到 `P03_SCOUT_CONTRACT_READY`，但保持 `sandbox_status: NOT_ENTERED`。CSI_NONE 的真实 receiver-visible z-window、同信息量 analytic comparator、residual artifact 与 deterministic one-cell interface smoke 已闭合；receiver-estimated CSI 仍是 `DECLARED_NOT_BOUND`。candidate component snapshot 仅为 `scout-candidate`，不得创建 PASS Queue、Registry binding、B004 或正式性能 cell。

### 理由

本轮闭合的是候选接口和可复现最小 smoke，不是 U19 ML 方法性能。把 Scout contract PASS 直接当 Sandbox PASS 会跳过真实 ML mechanism、multi-cell diagnostic budget、evaluation-only BER binding 和机制级 shared comparator 门控。

### 纠错记录

独立 verifier 发现 Windows 文本换行导致 artifact hash 与磁盘字节不一致，以及 residual builder 未验证 comparator identity 的 oracle 替换漏洞；两项均已修复并新增回归测试。该经历作为流程纠错保留，不修改任何 B002/B003 历史产物。

### 触发原话

- “不要在完成一个 adapter 后再次停下来。”
- “下一步要把‘多个相互依赖的接口补齐’作为一个完整 Sprint，而不是一个接口一个对话。”

## D013: governance pilot 转 dormant，研究状态回归项目目录

> status: active
> date: 2026-07-18
> 取代：把正式研究 Scout 微步骤持续追加到 governance pilot 的工作方式
> 被取代：无
> 依据：S010；用户要求控制面收口并明确状态职责；V006 恢复覆盖仍 PARTIAL

### 决策

Direction Lab governance pilot 生命周期转为 `dormant`。正式研究状态只由 `projects/thesis-fso/master-state.md` 入口解释；Direction Lab sandbox 机器状态只由 `canonical-state.yaml` + completion events + reducer 解释；当前 Scout 由 capability triage 和 candidate contract/readiness 解释。后续 `.sessions` 只记录里程碑、决策和跨对话交接，不承载逐接口、逐 smoke 的当前状态。

### 理由

治理专题已经完成 controller、EvidenceGate、真实 B001–B003 sandbox、state reducer 和 P03 interface closure 的压测，但恢复阈值覆盖仍有 PARTIAL，因此不标 closed。继续把研究微步骤堆进该专题会让用户无法从少量入口判断“在列批次还是已开跑”。

### 触发原话

- “说实话我感觉，现在真的是越来越乱了。我不知道你在跑啥，甚至不知道有没有在跑。”
- “感觉咱们先停下来，整理一下情况？”
