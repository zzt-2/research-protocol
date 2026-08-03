# Decisions — Research Direction Lab 完整体系设计

## D001: 目标体系采用 Skill-first、code-guarded

> status: active
> date: 2026-07-20
> 取代：`2026-07-17-direction-lab-governance-pilot/D007` 中“Skill 只导航、脚本/状态机负责流程允许与阻断”的目标设计；`S078/D060-D061` 中通用 Portfolio scheduler 的目标设计
> 被取代：无
> 依据：验证: V035/V037 + 用户原话: 本专题 `voice.md` 2026-07-20 + 历史原话: `2026-07-10-dual-pol-osl-groundwork/voice.md`、`2026-07-17-direction-lab-governance-pilot/voice.md`

### 决策

Research Direction Lab 的开放式研究流程、候选生成与排序、自动换路、域扩展、科学解释和论文收获由 Skill/AI 负责；通用代码只承担确定性证据完整性、历史保护、状态事实、重复/stale 检查和小型执行工具。

### 理由

研究方向、候选覆盖和“何时足够”依赖不完整证据与上下文判断。把它们编码为固定 slots、最小批次数、资源匹配和 work-conservation 后，控制核连续产生新的开放世界反例，并把主要工作从科学实验转成治理修补。用户原始目的始终是让 AI 长期、批量、可恢复地寻找论文内容，脚本控制只是需要实测的手段，不是最终目标。

### 排除的替代方案

- **代码中心的通用研究调度器**：拒绝；会把开放式科学判断伪装成闭合约束问题，已由 V035/V037 证明补丁会继续增长。
- **纯 Skill、无确定性代码**：拒绝；历史保护、receipt/hash、stale、路径边界和可重建事实需要确定性保障。
- **继续维护多份普通流程文档**：拒绝；最终执行流程必须由一个主 Skill 拥有，项目文档只保留事实与入口。

### 影响范围

影响未来主 Skill、通用小工具、Communications Profile、Project Adapter、项目运行目录和现有 Direction Lab 资产迁移。当前代码和历史证据保持不变；本决策不授权实验或实现。

### 来源

S001 / 用户纠正 / V035-V037。

## D002: 冻结 U01–U15 的来源与目标拥有者

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户原话: 本专题 `voice.md` 2026-07-20 + 项目安全: `AGENTS.md`「文档职责边界」与「voice.md」治理规则

### 决策

U01–U15 只有在同时具备原话来源指针、可接受的依据类别和唯一目标架构拥有者时才视为冻结；历史执行提示词只可作为标注为 `[转述:执行提示词]` 的辅助来源，不得冒充用户自然原话，也不在本专题复制历史全文。没有用户原话、证据完整性或项目安全依据的设计规则不得进入实施合同。

### 理由

用户明确要求既有原话中在意的内容必须被考虑，并指定回看 governance pilot 的 `voice.md`。仅列需求 ID 无法证明需求来自哪里，也无法防止后续把执行提示词、设计者偏好或无来源阈值误当成用户要求；同时，需求若没有唯一架构拥有者，会再次造成 Skill、代码、Profile、Adapter 和项目状态职责重叠。

### 排除的替代方案

- **在本专题复制三份历史 `voice.md` 全文**：拒绝；会制造重复原话源并使后续纠偏难以维护。
- **只保留 U01–U15 的摘要、不记录行级来源**：拒绝；无法区分自然原话、执行提示词和设计推导。
- **把无来源的精确阈值先冻结、以后再验证**：拒绝；无来源规则不得先进入实施合同。

### 影响范围

影响蓝图 U01–U15 的冻结判据、后续 Skill/代码/Profile/Adapter/状态文件的责任验收，以及执行提示词的引用格式；蓝图 §18 是本决策的产出而非依据。不修改现有控制器、仿真器、历史科学产物或运行授权。

### 来源

S001 / 用户原话来源审计。

## D003: 批准进入目标体系第一阶段实施

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户原话: 本专题 `voice.md` 2026-07-20「认可」

### 决策

在隔离 worktree 中实施 Task 1–3：冻结需求溯源、建立经 RED 基线约束的精简 Skill，以及 Communications Profile / Project Adapter schema。当前不进入确定性工具迁移、项目实例迁移、shadow 或科学实验。

### 理由

用户已认可完整蓝图；先把流程 owner 与通用/领域/项目边界做成最小可验证实体，可在不污染历史研究状态的前提下检验设计是否真能落地。

### 排除的替代方案

- **继续只写普通流程文档**：拒绝；不能验证 Skill 是否可触发、可恢复和可路由。
- **一次完成全部十项任务**：暂不采用；先独立复核第一阶段，避免目标架构未经使用就继续膨胀。
- **直接开始科学实验**：拒绝；本决策未授权 shadow 或新科学运行。

### 影响范围

更新本专题当前范围并创建 `.agents/skills/research-direction-lab/` 的第一阶段文件；不修改历史科学产物、canonical baseline 或现有控制器。

### 来源

S002 / 用户批准。

## D004: Phase 2 仅实施确定性工具与历史 replay

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户授权: 当前对话“继续吧” + 计划边界: H001 + 验证: V001

### 决策

在同一干净隔离 worktree 中继续实施 Task 4–5：Task 4 只提供确定性 hash/receipt/event/reducer/status 小工具，Task 5 只建立指向不可变历史证据的 replay fixtures；不进入项目实例、forward test、shadow 或科学运行。

### 理由

Phase 1 已由 V001 证明结构与职责边界成立；H001 已把 Task 4–5 固定为下一阶段。先验证安全内核和历史回放，可以在不污染项目状态的前提下判断目标体系是否真正可用。

### 排除的替代方案

- **直接建立双偏振 OSL project adapter 实例**：暂不采用；属于 Task 6，必须等安全工具和 replay 先通过。
- **同时修旧 campaign scheduler**：拒绝；违反 D001 与 H001，不属于确定性安全内核。
- **开始 live shadow 或科学实验**：拒绝；Task 8–9 和 `sim-preflight` 前置尚未满足。

### 影响范围

允许新增 `.agents/skills/research-direction-lab/scripts/` 下五个通用小工具、对应测试和 Task 5 replay case/test；仍保护 controller、campaign core、项目实例、canonical state 与历史科学 evidence。

### 来源

S004 / H001 / 用户继续指令。触发原话不入 `voice.md`：按 voice 规范，“继续吧”属于零信息推进语。

## D005: 进入只读项目投影与 scheduler 审计阶段

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：验证: V002 + 用户原话: voice.md 2026-07-20 + 计划: Task 6–7

### 决策

实施 Task 6–7：创建只读项目 Adapter/portfolio/harvest/status 投影并审计旧 scheduler；附带一次只读桌面使用推演，但不提前执行 Task 8 行为测试或任何科学运行。

### 理由

V002 已验证通用 Skill、Profile、schema、确定性工具与历史 replay 地基。项目只读投影是检验这些抽象能否承载真实研究事实的下一最小步骤；桌面推演可帮助用户看懂未来实际使用方式，但不能冒充新鲜行为验证。

### 排除的替代方案

- **直接进入 Task 8 forward tests**：暂不采用；Task 6 项目事实投影与 Task 7 旧控制面审计尚未完成。
- **把桌面推演计为 Skill PASS**：拒绝；演练是解释和设计核查，不是盲测或独立行为证据。
- **顺便启动 B004/ML/科学 batch**：拒绝；当前仍无 `sim-preflight` 合同和科学运行授权。

### 影响范围

允许新增 Task 6 规定的四个项目投影、其测试、Task 7 审计与 no-scheduler 测试，以及只读使用推演记录；继续保护历史批次、canonical、baseline、runner 和正式论文材料。

### 来源

S006 / 用户授权 / V002。

## D006: Task 6 增补最小 thesis-spines 状态文件

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：契约审计: .superpowers/sdd/task-6-source-map.md + schema: project-adapter-schema.yaml + 布局职责: project-layout.md

### 决策

Task 6 在原四个投影文件之外增补 `harvest/thesis-spines.v1.md`，作为 `paths.thesis_spines` 的唯一拥有者；初始内容只声明当前无满足 promotion 条件的论文主线。

### 理由

ProjectAdapterV1 的闭合 schema 要求 `paths.thesis_spines`，而项目布局明确把 thesis spines 与 harvest ledger 分为两个事实 owner。省略文件会形成悬空路径，用 ledger/README 代替会重新制造职责混叠；把 schema 改成 nullable 又会削弱已批准架构。

### 排除的替代方案

- **让 `thesis_spines` 指向 ledger 或 README**：拒绝；两个文件职责不同。
- **把 schema 字段改成可空或可缺省**：拒绝；没有科学理由削弱合同。
- **提前编造候选论文主线**：拒绝；当前证据只支持若干 harvest，尚未支持 promotion。

### 影响范围

只新增一个短小的只读投影文件及对应测试；不改变 Task 6 科学边界、Adapter schema、历史证据或运行授权。

### 来源

S006 / 技术合同审计。触发原话：无（技术推导）。

## D007: STATUS 采用有界八问 view-model

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：critic: task-6-review 两轮对抗审查 + 使用推演: S007 + 用户原话: voice.md 2026-07-20

### 决策

`render_status()` 保持四类事实输入，但 STATUS 只呈现有界的八问摘要和详情指针；所有展示值受 UTF-8 byte-aware 限制，阻断轴必须直接列出，正式状态、当前允许动作和禁止动作必须分层显示。

### 理由

首版 512 行全量 JSON dump 虽然信息完整，却把内部组织成本转嫁给用户；仅限制行数又可被超长字段绕过。STATUS 是唯一日常入口，必须让用户不翻四份文件也能恢复全局，同时让完整证据继续留在各自 owner 中。

### 排除的替代方案

- **继续 dump 完整 Adapter/portfolio/harvest**：拒绝；入口过重且重复事实。
- **只限制行数**：拒绝；超长单行可产生 MB 级输出。
- **只写一句“有 blocked axes”**：拒绝；用户仍需下钻才能知道实际阻断面。
- **删除底层完整投影以换取轻量**：拒绝；轻量入口不等于丢失证据。

### 影响范围

影响通用 `render_status.py`、其确定性/对抗测试、项目 STATUS 和使用恢复合同；不改变科学授权、候选判断或历史证据。

### 来源

S007 / task-6-review。触发原话已记录于 `voice.md` D005/D007。

## D008: 授权 Task 9 live shadow 并条件性扩展到 Task 10 cutover（含 AGENTS.md 最小路由）

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户授权: 2026-07-20 执行提示词 §一~§九（明确授权 Task 9 shadow + Task 9 PASS 后条件性执行 Task 10 cutover） + 计划边界: Task 9 Step 4 PASS 标准 + Skill: recovery-and-rotation.md + thesis-lessons TL-30 (不跳框架)

### 决策

1. 在隔离 worktree `research-direction-lab-shadow`（分支 `codex/research-direction-lab-shadow`，从 `f79cb1b` 创建）执行 Task 9 live shadow，时间预算为本对话内连续推进最长 ~2h。
2. shadow 工作严格在 dual-pol OSL 现有地基 + 合法 Project Adapter 范围内；不运行新科学实验，不创建 B004，不修改 protected history；性能数字只能留在 `shadow/` 下的 sandbox artifact。
3. 先冻结 Shadow Contract + Foundation Certificate，再驱动 Skill 7-phase loop 收集 5 类行为证据（OBS-BLOCK / OBS-ROTATE / OBS-SCOPE / OBS-HARVEST / OBS-RECOVER）。
4. 自然科学工作未覆盖 5 类时可 replay 已冻结历史，不能伪造新科学 batch。
5. **范围扩展**：plan Task 9 Step 5 + Task 10 cutover 在本轮授权下扩展为包含 AGENTS.md 最小路由——AGENTS.md 只增加指向 research-direction-lab Skill 的路由和边界索引行（"开放式找方向用 research-direction-lab Skill；Groundwork/Contract/Execute 是正式证据形成层；Direction Lab 的 Scout/Sandbox 不等于 GW 完成"），不复制 Skill 内容；旧 method-family-batch-exploration Skill 标 superseded 但保留历史不删；process.md 成为短入口，STATUS 成为日常唯一人类入口。
6. AGENTS.md 路由必须解决"stages/groundwork 是唯一合法研究路径"（FR-22）与 Direction Lab 的表面冲突：正确解释是 Direction Lab 是正式晋级前的候选发现/批量筛选层，晋级候选仍必须走 GW/Contract/Execute。
7. 实现上下文与独立 verifier 上下文分离；Task 9 和 Task 10 分别独立终验。
8. 整个对话只在收尾时一次 consolidated commit，不 push。

### 理由

V001-V004 已分阶段验证 Task 1-8（Skill 结构 + 通用工具 + 历史 replay + 只读项目投影 + scheduler 审计 + 5 类案例 fresh-agent 盲测）；用户本轮明确授权进入 Task 9 live shadow 以获取长期自动化行为的真实观察证据。条件性扩展到 Task 10 + AGENTS.md 最小路由是因为旧路由仍指向 method-family-batch-exploration Skill，正式激活前必须收敛到唯一 owner；用户原话："只有独立 verifier 明确判定 Task 9 PASS，才继续 Task 10 cutover"，所以 Task 10 是严格条件性的。

### 排除的替代方案

- **跳过 Task 9 直接 Task 10 cutover**：拒绝；forward test 只验证 5 类已覆盖行为，shadow 才提供长期证据（S008 后续）。
- **借 shadow 跑新科学实验或创建 B004**：拒绝；违反用户提示词 §一/§二/§八；新科学仍需 sim-preflight 合同和独立授权。
- **把 shadow 派生的 SHADOW-H010..H017 自动晋升到 main ledger**：拒绝；main ledger V003-anchored 到 H001-H009，强制晋升破坏 V003 测试；晋升需单独授权 + 重新 hash 绑定 + thesis-spines 更新。
- **AGENTS.md 复制 Skill 全文**：拒绝；违反"唯一拥有者"不变量；AGENTS.md 只加路由行。
- **删除 method-family-batch-exploration Skill**：拒绝；用户要求"标记 superseded 但保留历史"。
- **把 shadow/sandbox 数字写入正式论文材料**：拒绝；用户提示词 §二明确禁止。
- **scheduler 或复杂状态机补丁**：拒绝；D001 不变量。

### 影响范围

允许在 shadow worktree 内新增 `projects/thesis-fso/direction-lab/shadow/` 下 contract / observation / harvest-derived / foundation-certificate；允许更新 STATUS（通过 renderer 保持 LF bytes）；允许新增 S009 + D008 + voice 条目；允许更新 `_registry.yaml`。Task 9 PASS + 独立 verifier 终验后，Task 10 cutover 修改 process.md / projects/thesis-fso/direction-lab/README.md / `C:/Users/zzt/.agents/skills/method-family-batch-exploration/SKILL.md`（标 superseded） / 新增 docs/architecture/research-direction-lab.md（doc-steward mode）/ AGENTS.md 加最小路由索引行（不复制 Skill 内容）。继续保护 18 个 protected history 文件的字节、B001-B003 raw artifacts、canonical baseline、historical receipts。

### 来源

S009 / 用户 2026-07-20 执行提示词 §一~§九。触发原话：见 voice.md 2026-07-20 段。

## D009: 消费者部署收口——integration worktree + 全局 Skill 安装 + 悬空 superseded 指针消除

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户授权: 2026-07-20 执行提示词 §一~§八（明确授权消费者部署收口） + 验证: V005/V006 + Skill: using-git-worktrees + Skill: writing-skills（字节一致审计）

### 决策

1. 诊断"消费者部署断链"：shadow 分支 V005/V006 PASS 的工作从未进入消费者可达路径，全局 `research-direction-lab` Skill 不存在，旧 `method-family-batch-exploration` 的 `superseded_by` 指针悬空。
2. 集成策略：因 `merge-base(97473a2, 6ca142e) = 97473a2`（fast-forward），从 `6ca142e` 创建新 worktree `.worktrees/research-direction-lab-integration`（分支 `codex/research-direction-lab-integration`）即可获得 Task 1-10 完整历史链和全部资产，无需 merge/rebase/cherry-pick，无冲突。
3. 全局 Skill 安装：从 integration worktree 的 `.agents/skills/research-direction-lab/` 复制 36 文件到 `C:\Users\zzt\.agents\skills\research-direction-lab\`，字节级 hash 全等，`quick_validate` PASS。
4. 旧 Skill superseded 指针消除：全局 `research-direction-lab` Skill 已存在且验证通过，旧 `method-family-batch-exploration` 的 `superseded_by: research-direction-lab` 不再悬空；保留旧 Skill 历史不删（沿用 D008 §5）。
5. 普通用户 dirty 根目录完全不动；用户正式使用开放式研究方向探索应从 integration worktree（分支 `codex/research-direction-lab-integration`）开始。
6. 整个对话只在收尾时一次 consolidated commit，不 push。

### 理由

V005/V006 已在 shadow worktree 验证 Task 9/10 PASS，但 shadow 是 isolated 分支从未回流——消费者（普通新对话）打开普通项目根时既看不到 Skill（不在 `.agents/skills/`），也读不到 FR-27（普通根 AGENTS.md 仍是 `97473a2` 旧版无 FR-27），即使读到了旧 `method-family-batch-exploration` Skill 也会被指向不存在的 `research-direction-lab`。本决策用最小、无冲突的 worktree 隔离 + 文件复制完成部署，不动用户 dirty 工作目录、不重做 Task 9/10 科学内容、不触发 push/merge。

### 排除的替代方案

- **直接在 dirty 普通根目录 merge `codex/research-direction-lab-shadow`**：拒绝；用户提示词 §二明确禁止，且 dirty 改动会被卷入合并。
- **cherry-pick 单个 `6ca142e` 到 `feat/title-consistency-check`**：拒绝；会丢失 Task 1-8 的中间历史（cfb29f0/61b623d/e2f42e8/f79cb1b），且 dirty 根目录不允许。
- **rebase shadow 到普通根**：拒绝；同上 dirty 问题，且 fast-forward 关系下与新建 integration 分支等价但更脏。
- **只安装全局 Skill，不建立 integration worktree**：拒绝；只解决 Skill 发现，但普通根仍无 Skill 本体、STATUS、Project Adapter、shadow artifacts、Task 8 forward tests、Task 9/10 cutover 改动——消费者从普通根启动时仍读不到完整资产。
- **删除旧 `method-family-batch-exploration` Skill**：拒绝；用户要求保留历史（D008 §5），且旧内容是 candidate-family batch 部分的可复用原型。
- **把 shadow 派生的 SHADOW-H010..H017 晋升到 main ledger**：拒绝；超出本轮范围，需单独授权。
- **运行新科学实验或创建 B004**：拒绝；用户提示词 §一/§二/§八明确禁止。

### 影响范围

允许新增 `.worktrees/research-direction-lab-integration/`（已 gitignore）；允许在 integration worktree 内重渲染 STATUS（renderer 输出 LF，符合 V006 anchor 4790 bytes）；允许新增 S011 + D009 + V007 + voice 条目到 `.sessions/2026-07-20-research-direction-lab-system/`；允许在 integration worktree 单次 consolidated commit（不 push）；允许在 `C:/Users/zzt/.agents/skills/research-direction-lab/` 安装 36 文件（git 不跟踪，记录在 S011/D009/V007）。继续保护 dirty 普通根目录、18 个 protected history 文件字节、B001-B003 raw artifacts、canonical baseline、historical receipts、B004 absence。

### 来源

S011 / 用户 2026-07-20 执行提示词 §一~§八。触发原话：见 voice.md 2026-07-20 段。

## D010: Direction Lab 采用务实的 baseline 充分性裁决

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据：用户原话: 本专题 `voice.md` 2026-07-20 + 验证: `.agents/skills/research-direction-lab/tests/forward/runs/pragmatic-baseline-adjudication/round-red.md` 与 `round-green.md` + 科学事件: `2026-07-20-direction-lab-science-scout/S002-cb1-baseline-atlas-headroom.md`

### 决策

候选进入 ML 或新方法 Scout 前，必须证明问题经过一个实现正确、任务适配、相关领域广泛采用且对当前有限主张公平的传统 baseline 后仍然存在；baseline 默认不要求当前 SOTA，也不要求穷举全部传统变体。

### 理由

旧 Skill 能识别 buggy comparator，却没有覆盖“实现正确但任务不适配或明显欠收敛”的弱 baseline，也没有 baseline 搜索的务实停止条件。RED fresh-agent 因而把补证扩张为多传统方法、多长度和全 Atlas 扫描；GREEN fresh-agent 在新增充分性规则后，收敛为一个主传统 comparator、一个直接相关的低成本扩展和共享收敛核验，同时保留 Portfolio 继续准备其他机制候选。

### 排除的替代方案

- **默认追逐当前 SOTA**：拒绝；除非论文主张、领域惯例、导师或审稿要求明确依赖 SOTA，否则会把 Scout 变成无止境竞品工程。
- **只要实现正确就接受 baseline**：拒绝；任务失配、欠收敛和信息不公平仍会制造假研究问题。
- **穷举所有广泛使用 baseline**：拒绝；当前有限主张有一个充分 comparator 且显而易见的廉价替代解释已处置后即停止。
- **把通信例子写进通用核心**：拒绝；具体算法和调制仍属于 Communications Profile 与 Project Adapter。

### 影响范围

新增 `references/baseline-adjudication.md`，轻量更新主 Skill 的路由与 Portfolio/Batch/Evidence/Harvest contracts；Communications Profile 只保存领域稳定解释。`AGENTS.md` 不复制规则。当前科学事件须重新裁决，但不改写历史实验字节。

### 来源

S011 续接 / 用户纠正 / RED-GREEN forward test。

## D011: 采用两层 baseline 公平性与有界机制级候选扩图

> status: active
> date: 2026-07-21
> 取代：无
> 被取代：无
> 依据：用户原话: `voice.md` 2026-07-21 + 验证: `.agents/skills/research-direction-lab/tests/forward/cross-output-portfolio-fairness.yaml` + 真实失效: `2026-07-20-direction-lab-science-scout/portfolio-refresh.v2-addendum.yaml`

### 决策

Direction Lab 将共同系统锚点与任务专属 comparator 分开：不同输出或主张必须使用同任务、同合法信息的 comparator；公平调参采用相当机会而非强制相同超参数。候选池过窄、集中于单一机制或 readiness 仅由共享数据推断时，重实施前先做一次有界的机制级扩图，随后立即选择小型 `READY` 批次运行。

### 理由

本轮真实 SCIENCE_SCOUT 把检测、控制和修正候选统一绑定到 nearest-16QAM + MMA，且把缺少动作接口的 C03 标为 `Y_with_compute`。共同 receiver anchor 能比较端到端结果，却不能替代检测器、控制策略或修正器各自的传统 comparator；共享输入也不能证明候选 runnable。另一方面，只有 C01–C04 四个同源候选会再次形成单机制隧道，但穷举或实现整个开放候选空间又会拖慢科学运行。

### 排除的替代方案

- **所有候选共用完全相同 baseline 列表**：拒绝；输出和主张不同会造成任务失配。
- **所有算法强制相同超参数**：拒绝；表面一致不等于公平，应给予相当调参预算并在 held-out 评估前冻结。
- **只运行当前排名第一候选**：拒绝；当前候选池过窄且 readiness 有误标，容易重新单点深挖。
- **先实现十几个候选再运行**：拒绝；扩图只建立机制全貌和 readiness，执行仍限于小型可比较 `READY` 批次。
- **用固定全局候选数量证明完整**：拒绝；候选地图保持开放，局部数量由信息价值和成本决定。

### 影响范围

最小更新 `references/baseline-adjudication.md`、`candidate-portfolio.md`、`batch-and-atlas.md` 及主 Skill 路由；新增一个 forward fixture 和结构测试。下一科学对话先短时扩图、纠正 readiness 与 comparator，再运行首批；不修改 protected history、baseline 数字或既有科学 artifacts。

### 来源

S011 续接 / 用户纠正 / RED-GREEN forward test。

## D012: 大规模科学运行前先完成 Probe 分层与恢复记录体系重设计

> status: active
> date: 2026-07-21
> 取代：无
> 扩展：D001 的 Skill-first 目标架构、D011 的有界扩图
> 被取代：无
> 依据：用户原话 `voice.md` 2026-07-21 + S012 + 科学审计 S010/D016/V005

### 决策

暂停新的大规模科学 campaign。先完整设计 `Probe → Scout → Deep Evidence` 的成本分层、科学语义门、单一恢复投影、current-view/lineage 分离、harvest 当前状态索引和抗膨胀目录；再用历史失败与 fresh-agent 场景推演；设计固定后才修改主 Skill、做独立 forward test，最后启动大规模运行。

### 理由

现有流程能保护来源和历史，却出现“秒级科学运行、绝大多数时间用于治理”，并让错误训练目标在完整证据链中被高置信解释为机制负面。继续局部加规则会触发约束过载；直接大规模跑会放大语义错误和恢复混乱。需要先重划层级与记录热路径，而不是再补一个调度器。

### 排除的替代方案

- **立即修改 Skill**：拒绝；职责蓝图、目录形态和恢复投影尚未经反例推演。
- **先继续跑、以后再整理**：拒绝；旧 H009 已证明错误当前态会进入交接与 harvest。
- **把所有规则做成强脚本门**：拒绝；开放科学判断继续由 Skill/AI 负责，代码只做轻量确定性检查。
- **删除历史减负**：拒绝；历史 append-only 保留，当前视图与 lineage 解耦。
- **另开一个平行方法论专题**：拒绝；本专题就是完整体系唯一拥有者，继续 S012，避免重复体系。

### 影响范围

当前范围扩展到体系设计、失败场景推演、Skill 修订与独立验证的后续阶段；本轮仅立项。明确不含新科学实验、旧 artifact 改写、复杂 scheduler 和立即修改 Skill。

### 来源

S012 / 用户 2026-07-21 原话（见 `voice.md`）。

## D013: 正式采用三层工作强度、语义先行与单一当前投影

> status: active
> date: 2026-07-21
> 取代：无
> 扩展：D001、D011、D012
> 被取代：无
> 依据：S012 + 设计文档 + 三类 RED/GREEN forward fixtures + Skill TDD

### 决策

Research Direction Lab 正式采用 `Probe → Scout → Deep Evidence` 三层成本模型。任何扩算力前先验证科学语义，再验证证据完整性；跨对话恢复以一组有界 current projections 为热路径，显式 amendment/disposition 血缘优先于 mtime 和旧叙述。harvest 必须评估但不强制产生条目，普通 Probe 不默认进入 session 治理链。

### 理由

旧流程把秒级问题自动放大为完整批次证据链，并能在 hash、receipt、独立复核全部通过时遗漏常数最优解或目标错位。恢复又依赖旧 handoff、synthesis 和大量日志，当前有效结论不够醒目。三层模型把成本与声明强度绑定；current view 把“现在相信什么”从“历史发生过什么”中解耦，同时保留 lineage 可审计性。

### 排除的替代方案

- **每个试验都走完整 batch/receipt/verifier**：拒绝；低风险前置问题只需 Probe compact record。
- **只靠完整 provenance 证明科学有效**：拒绝；integrity PASS 与 semantic validity 必须分开。
- **按最新修改时间决定当前结论**：拒绝；只有显式 `amends/supersedes/invalidates/restores` 关系能改变有效状态。
- **每个工作单元强制造 harvest**：拒绝；会制造低价值文档，改为强制 assessment、按耐久价值落条目。
- **把开放判断写入 scheduler**：拒绝；通用脚本只投影项目已记录事实，不替 AI 做科学选择。
- **为新体系另建平行流程**：拒绝；继续由 `research-direction-lab` Skill 单一拥有。

### 影响范围

更新主 Skill、现有 references、Project Adapter schema、state reducer、STATUS renderer、forward fixtures 与测试；不复制流程到 AGENTS.md，不引入领域项目术语，不运行科学实验，不改写历史 artifacts。

### 来源

S012 / 用户原话（见 `voice.md`）/ RED→GREEN 行为证据。

## D014: 长期协作采用四层记忆与极短中转

> status: active
> date: 2026-07-23
> 取代：无
> 扩展：D001、D013
> 被取代：无
> 依据：用户原话: voice.md 2026-07-23 + 项目目录规范: `AGENTS.md` worker-logs / `.sessions` 职责边界

### 决策

长期主控—GLM 协作采用“当前快照、长程控制日志、单项工作日志、原始证据”四层记忆；聊天只中转任务书路径和四项完成索引，完整工作细节不得因缩短聊天而删除。

### 理由

Codex 上下文和压缩机制不适合反复搬运完整执行报告，但仅保留当前快照和长程摘要会丢失命令、失败尝试、参数、异常和复现信息。分层后，主控按指针读取磁盘即可恢复，用户不需要理解或手工同步技术细节；各层又有唯一 owner，不会把同一事实复制进 state、S、H、D、V。

### 排除的替代方案

- **只保留一个巨型长期日志**：拒绝；恢复成本随历史线性增长，当前状态难以定位。
- **只保留当前摘要和 artifact**：拒绝；具体执行过程、失败尝试和偏离原因会丢失。
- **每个工作包都生成 S/D/V/H 全套文件**：拒绝；轻量工作被治理产物淹没，职责重复。
- **继续由用户搬运完整 GLM 报告**：拒绝；占用主控上下文并把用户变成人工状态同步器。

### 影响范围

影响未来 `T###`、GLM 最终回传、`projects/{project}/worker-logs/`、本专题 S 记录和主控恢复路径；不改变科学证据合同、项目 raw artifacts 或现有历史文件。

### 来源

S013 / 用户纠正与拍板。

## D015: Direction Lab 下一入口改为历史复盘

> status: active
> date: 2026-07-23
> 取代：无
> 扩展：D012、D013
> 被取代：无
> 依据：用户原话: voice.md 2026-07-23 + 真实运行: `.sessions/2026-07-20-direction-lab-science-scout/S014-campaign-level-science-freeze.md` / D022 / V012

### 决策

Research Direction Lab 专题暂不继续修改 Skill、恢复其科学 campaign 或生成新的 Direction Lab 科学 GLM 工作包；先对既有方法论、治理 pilot、system 落地和真实 science-scout campaign 做一次只读、有抽样策略的历史复盘，再决定最小修补和下一工作包。

### 理由

已有体系经过大量设计、Task 1–10、局部 forward test 和恢复体系重设计，却在真实运行后仍出现“工作很多但有效主方法未形成”、科学结论撤回、状态冲突和流程重型化。若不先重建因果链，直接继续派工或再写规则，很可能重复此前“发现问题—补流程—继续膨胀”的循环。

### 排除的替代方案

- **立即恢复 Direction Lab campaign 或继续找新候选**：暂不采用；尚未解释为什么现有机制在真实 campaign 中失效。
- **把全部历史原始文件从头到尾平均精读**：拒绝；成本过高且会再次陷入细节，采用控制链全读与关键转折抽查。
- **丢弃现有 Skill 后重新设计**：拒绝；已有候选族、证据分层、轮转和收获机制可复用，当前先找运行差距。
- **仅做口头复盘、不留证据指针**：拒绝；无法在后续压缩或新对话中稳定复用。

### 影响范围

把本专题下一入口从 H004/T001 的大规模科学使用改为完成 R002 历史复盘；不运行实验，不改科学 artifacts，不触碰 protected history，也不改变 Pilot-Jones 正式 Groundwork 的独立状态。

### 来源

S013 / 用户明确要求先整理此前整个过程。

## D016: 先完成运行协议设计，再以 fork 做真实纵向运行

> status: active
> date: 2026-07-23
> 取代：无
> 扩展：D014、D015
> 被取代：无
> 依据：调研: R002 + 用户原话: voice.md 2026-07-23 + 现场故障: S014

### 决策

R002 后不立即修改 Skill、建立 controller 或派具体科学方向；先在当前主控对话基于现场故障和历史失效仔细设计、演练并审查一套轻量长程运行协议，用户认可后 fork 当前对话做真实运行，运行一段时间后再由设计/审查对话根据磁盘证据复盘。

### 理由

本次压缩恢复已经现场证明：即使持久日志存在，主控仍可能把“当前正式候选”误推为“当前下一动作”，越过尚未完成的 system-design gate。若立即把单次事故写成规则，容易继续复制“发现问题—补流程—流程变重”的旧模式；若立即开科学方向，又会让未定的轮换、专题生命周期、恢复约束和 owner 问题带入真实运行。先完成有证据的设计，再用 fork 分离设计上下文与运行反馈，可以直接检验方案而不把设计阶段无限延长。

### 排除的替代方案

- **立即推进 Pilot-Jones 或其他具体方向**：拒绝；长期运行协议和状态门尚未设计完成。
- **根据本次事故立刻追加大量 Skill 规则**：拒绝；单个样本不足以决定正确 owner 和最小约束。
- **先实现强 controller 再测试**：拒绝；R002 已表明规则数量不是主要瓶颈，且强控制器可能固化错误判断。
- **只做口头讨论、不落持久日志**：拒绝；上下文可能再次压缩，必须让当前主线可从磁盘恢复。
- **设计完成后仍在同一上下文直接长期运行**：不采用；用 fork 分离设计基线和真实运行，便于后续对照审计。

### 影响范围

更新本专题 S014、topic-index、voice 和 registry。后续设计仍在本专题内进行；在设计获用户认可前，不修改 `research-direction-lab` Skill、`session-governance`、controller、项目 scientific current 或 Pilot-Jones 正式状态，也不生成科学执行任务。

### 来源

S014 / R002 / 用户 2026-07-23 连续纠正与拍板。

## D017: 采用轻量前台控制块与 T 授权 guard

> status: active
> date: 2026-07-23
> 取代：无
> 扩展：D013、D014、D016
> 被取代：无
> 依据：调研: R003 + 验证: RDL Skill 97 passed, 1 skipped + 用户原话: voice.md 2026-07-23

### 决策

长期 Research Direction Lab mission 采用 topic-index 顶部前台控制块、T 的 control ref/epoch/action class 绑定和极小确定性 guard；设计完成后建立一个独立 longitudinal live-test mission/worktree，由 fork 主控和执行 GLM 串行使用。

### 理由

S014 已证明“日志存在”不足以阻止压缩后跨 lane：system design、dormant science-scout 和 formal candidate 可以同时为真，但摘要推断可能让错误 owner 接管下一动作。R003 两轮历史场景演练表明，一个只保存 role/lane/gate/allowed/forbidden/next legal action 的小控制块足以绑定前台；guard 只校验已记录授权一致性，不替代科学判断。独立 live-test mission/worktree 又能保持设计基线与运行反馈分离。

### 排除的替代方案

- **只补 Skill/checklist**：拒绝；S014 已复现规则存在但未形成约束。
- **每个 fork 建 run manifest**：v1 拒绝；当前只有一个串行 live fork，会增加平行状态源。
- **强 controller 或自动候选状态机**：拒绝；会固化开放科学判断并重复 R002 的治理膨胀。
- **控制块复制 candidate/formal 科学状态**：拒绝；只保留 authority pointer，科学事实仍由原 owner 拥有。
- **设计完成即授权某个科学方向**：拒绝；live fork 必须先 Recover/Map，并从现有 owner 获得合法 authorization。

### 影响范围

- `research-direction-lab` Skill 新增长程控制 reference 和 `validate_task_control.py`；
- RDL mission 的 topic-index 可选用前台控制块；不修改所有普通专题模板；
- 新建一个 longitudinal live-test topic，初始只允许 Recover/Map/Reconcile/T 准备；
- system design topic 和 live-test topic 分离；一个 live-test worktree 串行承载 fork master 与 executor；
- 不改变 science-scout dormant 状态、Pilot-Jones formal 状态或任何科学结论。

### 来源

S014 / R003 / 用户认可后要求继续实施。

### 实施验证

- 仓库 Skill：`97 passed, 1 skipped`；`quick_validate.py` PASS；脚本 compileall PASS。
- 消费者同步：repo/global 共 59 个非缓存文件，相对路径与 SHA256 全部一致。
- 消费者 smoke：`test_long_horizon_control.py` 6/6 PASS，个人 Skill 解析真实 live control PASS。
- 自动压缩后的真实恢复：1/1 按 control epoch/lane 继续终验；样本不足，不宣称 longitudinal PASS。

## D018: v2 改为方法生产与三层长程记录

> status: active
> date: 2026-07-26
> 取代：无
> 扩展：D014、D017
> 被取代：无
> 依据：只读 phase-1 审计 `4af6f9d..aab425d` + 用户 2026-07-26 确认

### 决策

长程 RDL 同时维护科学裁决和方法增量，不再把可靠 Kill/修复 PASS 当作方法进展。运行记录固定为三层：

1. `topic-index.md` 保存当前快照；
2. `mission-log.md` 每包追加一行整链 checkpoint；
3. T/worker-log/artifact/commit 保存单包细节。

普通包不再追加 S；executor 不更新 formal/current/mission owner。下一 T 必须绑定当前 mission checkpoint，连续同轴、repair、no-method 或 UNDERWEIGHT 触发整链比较，但不使用自动 scheduler。

### 理由

Phase 1 没有严重跨 lane，却把 mission 成功逐渐降级成问题存活、修复闭包和 scoped Kill。T003/T004/T006 也证明测试/一致性 PASS 不保护科学语义。固定 mission-log、formal/method 双账和正向方法合同能直接修正这两个缺口，且比新增 controller 更轻。

### 排除

- 不用 S002 充当日常流水账；
- 不把全链复制进 topic-index；
- 不新增方法评分器、自动轮换器或固定包数成功标准；
- 不修改 phase-1 科学结论。

### 来源

用户：“前两个是不是最好别加Sxxx？直接固定文件名，以后别的专题都在这？”以及“核心是别一个劲堆复杂度，没啥用的可以省省”。

### 实施验证

- 仓库 Skill：`102 passed, 1 skipped`；`quick_validate.py` 与 compileall PASS。
- v2 guard：新增 checkpoint、缺失 mission-log、v1/v2 错配回归；v1 历史接口保持可用。
- 三层恢复：live control epoch 11 与 `CP007`、`mission-log.md` 一致；旧包已补 worker-log/commit 指针。
- 消费者同步：repo/个人 Skill 60 个非缓存文件 SHA256 全部一致。
- 独立终验：V012 PASS；不含 T008、科学实验或 phase-1 科学产物修改。

## D019: 以真实 T001–T026 审计最小修订压缩恢复与方法转化路由

> status: active
> date: 2026-07-29
> 取代：无
> 被取代：无
> 依据：调研: live-test R009 + 对照: mission-log CP001–CP025 + 用户原话: system voice.md 2026-07-29

### 决策

保留 D018 的三层记录、formal/method 双账、独立审查和方法工厂，只做三项最小修订：

1. 压缩恢复后必须用三问检查下一动作是否构造、比较、晋级或写作方法，以及是否已触发换路；
2. 无 active carrier 且 `READY=0 / NEEDS_SMALL_ADAPTER=0` 时，方法工厂或战略 gate 是硬路由；
3. accepted `METHOD_SIGNAL` 先做一次 promotion preflight，再决定进入有界 formal workline、降为 harvest，或进入战略 gate。

真实压缩/fork/主控替换只记一次极简 recovery receipt；普通包不新增治理项。task/interface 未通过且未执行的 brief 记 setup incident，不计 accepted scientific checkpoint。

### 理由

CP001–CP017 为 17/17 `mission_method_delta=NONE`；T019 后方法工厂第 2 包产生 signal，但两个 signal 的 formal 转化率仍为 0/2。事实说明 D018 的发现机制有效，缺口在恢复后的动作路由与 signal→formal 转化，不需要重写 Skill 或新增 controller。

### 排除的替代方案

- 不重建强 controller、scheduler、自动候选评分或固定包数成功标准；
- 不把更多 checklist 加到每个普通包；
- 不把 `PACKAGING_BOUNDARY/WRITING_MATERIAL` 当作 formal method；
- 不因本次流程修订重开 G1、Q15、B1 或其他已关闭科学轴。

### 影响范围

更新 `research-direction-lab` 的 `SKILL.md`、`long-horizon-control.md`、`method-production.md` 及对应测试；压缩 live-test `topic-index.md` 当前视图；同步个人 Skill。既有科学 verdict、formal owner、protected history 与论文框架不变。

### 来源

R009；用户 2026-07-29 对“基本每次交互都会发生压缩”及“改完之后继续”的确认。

## D020: 以历史回归补强三类 Research Direction Lab 契约

> status: active
> date: 2026-08-02
> 取代：无
> 后续扩展：D021（仅增加独立论文方法章保留门；本决策其余契约继续 active）
> 被取代：无
> 依据：调研: R004 + 验证: V014 + 用户原话: voice.md 2026-08-02

### 决策

Research Direction Lab 只补三类最小契约：把 semantic smoke 落为五门 executable evidence contract；把论文收获分为 `THESIS_MAIN_METHOD`、`THESIS_ENGINEERING_COMPONENT`、`SUPPORTING_MATERIAL`；把长程状态固定为 topic-index、mission-log、detail 三层轻量持久化，并在既有 receipt validator 中实现最小 hash/时序/seed fail-close。

### 理由

R004 的六案修改前盲测只有 Case 1 出现真实新增失效，但真实 campaign 同时暴露方法层级漂移和专题记录膨胀。三处改动分别关闭“语义未执行即扩样/晋级”“负面或包装冒充方法且工程贡献被压成零”“current snapshot 与细节层重复”三个不同缺口；其余五案作为历史防回归，不夸大旧 Skill 的失败范围。

### 排除的替代方案

- 不增加第四类 patch，不重写主 Skill，不新增 controller、scheduler、README、CHANGELOG 或新治理层；
- 不用更多 seeds/cells 或统计显著性修复 semantic FAIL；
- 不把 negative、partial、writing material、旧 claim 及其纠偏升级为 active carrier；
- 不修 P07–P11/G1、不创建 P12、不启动 AMC 或科学仿真、不改变 formal science owner；
- 不修改 session-governance、sim-preflight 或其他 Skill。

### 影响范围

仅影响 `.agents/skills/research-direction-lab/` 的既有 evidence、method-production、thesis-harvest、long-horizon-control、receipt validator 与对应测试，并同步个人运行副本；系统专题记录 R004/D020/V014。既有科学 verdict、dormant longitudinal topic 与 formal owner 不变。

### 来源

H003；R004；用户 2026-08-02 执行指令。

## D021: 科学主方法门与论文方法章门分账

> status: active
> date: 2026-08-03
> 取代：无
> 扩展：D020（局部增加第四个、但独立且轻量的论文方法章保留门；不改写 D020 其余三类契约）
> 被取代：无
> 依据：调研: `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md` + `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml` + 对照: CCISP 方法形成史 + 用户原话: voice.md 2026-08-03

### 决策

Research Direction Lab 保留现有科学诚信与 formal promotion 门，另增一个轻量论文方法章保留门。语义有效但尚未达到 `METHOD_SIGNAL` 的中粒度内核，必须先判定 `THESIS_METHOD_READY / NEEDS_ONE_BOUNDED_PACKAGE / SUPPORTING_ONLY / REJECT`，不得仅因不是科学主方法而自动降为 supporting material。

### 理由

长程 campaign 得到 7 个可靠局部负面/边界包却没有新增方法，手工 CCISP 则从一个可部署 estimator/gate/branch action 形成了完整会议方法。12 篇硕士论文精读进一步确认，校准器、阈值、分支、计算图和字长都可能成为方法章，关键是形成完整动作链与有界证据，而不是必须先满足顶层 `METHOD_SIGNAL`。当前 Skill 已区分 contribution tier，却仍把 thesis-facing method card 放在 accepted `METHOD_SIGNAL` 之后，造成包装启动过晚。

### 排除的替代方案

- 不放松 artifact、truth leakage、metric、lifecycle、成本与授权门；
- 不把所有工程组件写成主方法，不用章节数量制造贡献；
- 不新增 controller、评分器、固定包数或重型治理链；
- 不重开 G1/P09/P07/P08 等 invalidated 结果；
- 不在本轮运行 2A/2B 仿真或写正式论文。

### 影响范围

只允许最小修改 `research-direction-lab` 的主路由、`method-production.md`、`thesis-harvest.md` 和对应行为回归；同步个人运行副本。新增 2A/2B 两个隔离只读包装任务。既有 scientific verdict、formal owner、dormant campaigns 与论文正文不变。

### 来源

S015；用户 2026-08-03 明确要求先记录、修正 Skill，保证可包装内核不被丢弃，并另开两个对话分别研究 2A/2B 包装。

## D022: 授权 2A/2B 各一个持续到终态的 bounded closure

> status: active
> date: 2026-08-03
> 取代：无
> 扩展：D021（只把已判 `NEEDS_ONE_BOUNDED_PACKAGE` 的 2A/2B 从只读诊断推进到各一个执行包）
> 被取代：无
> 依据：调研: T002/T003 两个独立包装诊断 + 验证: V015 + 用户原话: voice.md 2026-08-03

### 决策

在两个隔离 Codex worktree 中分别执行 T004（calibration-aware robust CPR）与 T005（fixed-point branch-routed CPR）。每个对话自主完成 preflight、合同冻结、实现/运行、独立 verifier、harvest 和分支内提交，持续到 `THESIS_METHOD_READY / SUPPORTING_ONLY / REJECT / EXTERNAL_BLOCKED` 之一，不得以“还差一轮”结束。

“保证确实能用”定义为保证结论与资产可用，不预设正面结果：PASS 必须产生可复现方法包、算法/框图/主图数据、baseline/消融/claim ceiling；FAIL 必须产生可复用边界证据并立即降级。每个包最多一次确定性修复；修改方法语义、指标、信息边界或测试合同则须新 receipt 与全新 test seeds，不能修到通过。

### 理由

T002/T003 均证明已有证据形成了真实动作链，但各缺一个决定性闭包。继续开新方向会再次绕过最接近论文成章的资产；直接宣布方法成立又会重复历史 consistency≠correctness 与包装自欺。两个隔离包可并行推进事实审计和实现，但 T005 的 headline CPU timing 必须避开其他重负载进程，以免 T004 并发污染。

### 排除的替代方案

- 不保证两个包都得到正面方法；保证的是得到可信终态和可复用资产。
- 不允许同一标签追加第二、第三个包装包；一次确定性修复后必须裁决。
- 不恢复 dormant longitudinal campaign，不重开 G1/P09/P07/P08/AMC，不派第三个候选。
- 不修改 `projects/simulation/common/` 或 `params.py`；若必须修改，终止为 `EXTERNAL_BLOCKED(reason=STAGE_SCOPE_EXCEEDED)` 并交主控重新授权。
- 不在两个执行分支修改本 system topic、正式论文正文或 formal owner，避免并行治理冲突。

### 影响范围

新增 T004/T005；system foreground control 升到 epoch 11。两个执行分支仅可写各自 sandbox/results/worker-log/harvest dossier、任务专属 sim-preflight usage-entry fragment 和验证产物，并按长实验 chronology 允许 pre-test receipt commit + final commit；不直接修改共享月志、不 push。两个 fragment 由主控接收结果时串行并入月志。

### 来源

S015 续接；用户 2026-08-03 原话：“那要不两个单独对话，一直跑直到完成？保证确实能用？”
