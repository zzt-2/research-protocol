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
