# Topic Index: Research Direction Lab 完整体系设计

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-07-21（D011/V010 PASS；全局同步完成；未运行科学实验）

## 专题信息

- **slug**: `2026-07-20-research-direction-lab-system`
- **title**: Research Direction Lab 完整体系设计
- **性质**: 目标体系蓝图与分阶段实施；Task 1–7 已验证，当前等待提交与 Task 8 授权决定，不运行科学实验

## 范围边界

### 原始目标（冻结）

一次性规划一套能从零或从已有稳固地基出发、长期自动寻找并验证研究方向、组织清晰不过重、持续积累毕业论文素材的完整体系；明确 Skill、通用代码、领域 Profile、项目 Adapter、项目状态和用户决策的职责边界。

### 当前范围

- 审计既有 `method-family-batch-exploration`、Direction Lab v0.3、governance pilot、Portfolio Autopilot 和用户原话；
- 冻结目标体系蓝图、资产迁移表、实施顺序和验收场景；
- Task 1–3 已完成；Task 4–5 的确定性安全小工具与只读历史 replay 已实现并由 V002 独立终验 PASS；
- Task 6 的只读项目投影、Task 7 的旧 scheduler 迁移审计和不计为行为 PASS 的桌面使用推演已由 V003 验证；
- Task 8 round 1 fresh-agent 盲测（5 类案例）已由 V004 独立终验 PASS；首轮 scorer 实现缺陷已一次性批量修复，无 Skill 修订、无重跑；
- 本阶段不修改现有 controller、campaign core、仿真器、baseline 或科学证据。
- 基于首轮正式 SCIENCE_SCOUT 的真实失效，允许以 RED→GREEN 修订主 Skill 的 baseline 充分性判断；不借此运行新实验或改写历史证据。
- 基于 C01–C04 的 comparator/readiness 失配，允许最小修订两层 baseline 公平性与重实施前的有界机制级候选扩图；不借此扩展通用 scheduler 或运行科学实验。

### 明确不含

- 不修补 V037 的资源匹配或继续扩展 Portfolio Autopilot；
- 不启动 B004、ML 训练、P03 后续实验或新科学批次；
- 不改写 B001–B003、P03 Atlas、canonical state 或历史 receipt；
- 不把目标态蓝图写成当前架构现状；
- 不在蓝图审定前迁移目录或删除旧流程文件。

### 范围变更记录

- 2026-07-20，D003：用户认可蓝图后，从“只设计”扩展为隔离实施 Task 1–3；仍明确排除科学实验、shadow 和旧控制器迁移。
- **[2026-07-20] D004**：从 Phase 1 扩展到实施 Task 4–5。
  - 原因：V001 已验证 Phase 1；用户按 H001 指示继续。
  - 新范围：五个确定性安全小工具及测试、只读历史 replay cases/tests。
  - 影响的未决项：Task 4–5 从未开始改为进行中；Task 6–10 继续未授权。
- **[2026-07-20] D005**：从 Phase 2 扩展到实施 Task 6–7，并加入只读桌面使用推演。
  - 原因：V002 已 PASS；用户按 H002 继续并要求推演实际使用。
  - 新范围：只读 Adapter/portfolio/harvest/status、旧 scheduler 逐函数审计与 no-scheduler 测试、非评分桌面演练。
  - 影响的未决项：Task 6–7 从未授权改为进行中；Task 8–10、shadow 和科学运行继续未授权。
- **[2026-07-20] Task 8 授权（本轮执行提示词）**：用户明确授权 Task 8 fresh-agent forward tests。
  - 原因：V003 已 PASS；H003 冻结了入口；用户在本轮提示词中明确授权。
  - 新范围：5 类案例的 fresh-agent 盲测、预注册 scorer、独立 reviewer + verifier 复核、最多一次批量 Skill 修订（实际未触发）、一次性提交。
  - 明确排除：Task 9 shadow、B004、ML 训练、科学实验、修改 B001–B003/P03 Atlas/canonical state/baseline/receipt、把盲测回答写入论文、push/merge。
  - 影响的未决项：Task 8 从未授权改为已完成（V004 PASS）；Task 9–10、shadow、live activation 继续未授权。
- **[2026-07-20] Task 9 shadow + Task 10 cutover 授权（D008）**：用户明确授权 Task 9 live shadow + Task 9 PASS 后条件性 Task 10 cutover（含 AGENTS.md 最小路由）。
  - 原因：V004 已 PASS；用户 2026-07-20 执行提示词 §一~§九 明确授权；Task 9 提供 shadow 长期自动化行为证据，Task 10 收敛流程拥有者到唯一 owner。
  - 新范围：隔离 worktree `research-direction-lab-shadow` 内运行 shadow（不跑新科学，只 replay + 派生 harvest + rotation 演示）；cutover 修改 AGENTS.md（加 FR-27 路由索引）/ process.md（加 SUPERSEDED 头）/ README.md（加流程入口）/ method-family-batch-exploration SKILL.md（加 superseded frontmatter）/ docs/architecture/research-direction-lab.md（doc-steward mode 架构文档）。
  - 明确排除：跳过 Task 9 直接 Task 10；借 shadow 跑新科学或创建 B004；shadow 派生物自动晋升到 main ledger；AGENTS.md 复制 Skill 全文；删除 method-family-batch-exploration Skill；shadow/sandbox 数字写入论文材料；scheduler 或复杂状态机补丁；push/merge。
  - 影响的未决项：Task 9 从未授权改为已完成（V005 PASS, 11/11）；Task 10 从未授权改为已完成（V006 PASS, 11/11, live-activation authorized）；本对话收尾做单次 consolidated commit。
- **[2026-07-20] 消费者部署收口（D009）**：用户明确授权修复"shadow 已 PASS 但消费者入口断链"问题。
  - 原因：V005/V006 PASS 后，shadow 分支从未回流到消费者可达路径——普通根目录无 Skill 本体/STATUS/Project Adapter/Task 9-10 cutover 改动；全局 `research-direction-lab` Skill 不存在；旧 `method-family-batch-exploration` 的 `superseded_by` 指针悬空。
  - 新范围：建立 integration worktree（`.worktrees/research-direction-lab-integration`，分支 `codex/research-direction-lab-integration`，从 `6ca142e` fast-forward）+ 全局 Skill 安装到 `C:\Users\zzt\.agents\skills\research-direction-lab\`（36 文件 hash 全等）+ fresh-agent discovery smoke + 独立 verifier 终验（V007）。
  - 明确排除：dirty 普通根目录合并/cherry-pick/rebase；删除旧 method-family Skill；SHADOW-H010..H017 晋升；运行新科学或创建 B004；修改 protected history/canonical baseline/B001-B003/P03 Atlas；复制 Skill 内容到 AGENTS.md；push/merge；开 Goal。
  - 影响的未决项：消费者部署断链从未授权改为已完成（V007 pending → 待 verifier PASS）；用户正式使用开放式研究方向探索应从 `codex/research-direction-lab-integration` 分支开始；dirty 普通根目录保持不动。
- **[2026-07-20] baseline 充分性修订（D010）**：用户明确要求 baseline 以“说得过去、广泛采用”为准，不默认追当前最好；允许更新主 Skill、测试和两层治理记录。
  - 原因：正式 SCIENCE_SCOUT 把实现正确但 16QAM 任务不适配/可能欠收敛的单模 baseline 当成 ML headroom 起点。
  - 新范围：务实 baseline ladder、`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 门、四类候选来源和 forward test。
  - 明确排除：SOTA 穷举、运行新科学实验、训练 ML、改写 protected history、复制规则到 AGENTS.md。

## 已确认结论

### 不变量

- **Skill-first, code-guarded**：开放式研究判断和长期循环由 Skill/AI 负责；代码只硬化确定、可测试、错误代价高的不变量。
- **论文产出优先**：治理通过不能冒充科学进展；所有批次都必须进入论文收获或明确的可复用资产。
- **先全景后批跑**：从已有基点展开候选族，先归类和统一规划，再成批比较；少数 winner 才进入重型 Deep Evidence。
- **局部阻断不终止**：存在其他合法工作时，单候选失败、接口缺失、局部负面或 critic 退回都必须自动换路。
- **通用与领域解耦**：通用代码和核心 Skill 不包含具体通信项目语义；领域规则进入 Profile，项目事实进入 Adapter。
- **原话可追溯**：目标体系的长期约束必须能指回用户原话；执行提示词和用户自然原话分开标注。
- **唯一拥有者**：执行流程最终由一个主 Skill 拥有；项目文档只保存事实和状态，不复制流程全文。
- **baseline 充分而非最强**：Go comparator 必须正确、任务适配、广泛采用且公平；当前 SOTA 仅在主张或外部要求依赖时才成为义务。
- **公平按主张分层**：共同系统锚点用于端到端比较，不替代不同输出的任务专属 comparator；公平是相当调参与验证机会，不是机械使用相同超参数。
- **有界扩图后立即批跑**：候选过窄或集中于单一机制时先做短时机制级扩图和 readiness 事实审计；不证明完整、不实现全池，随后立即运行小型 `READY` 批次。

### 其他结论

- 现有 `method-family-batch-exploration` 是候选族批量部分的可复用原型。
- Direction Lab 的 receipt/hash/stale/history protection 等确定性资产可保留。
- `science_slots`、固定最小批次数求解和通用资源匹配不进入目标体系。

## 进展线索

- **S001**：完成既有三代方案与两份 voice 的责任边界诊断，开始目标体系蓝图和迁移计划。
- **D001**：冻结 `Skill-first, code-guarded` 作为目标架构；取代“Skill 只导航、脚本/状态机决定整个流程”的设计方向。
- **S002**：四个无 Skill 压力场景均未复现目标判断失败，因此删减冗余行为规则，把 Skill 聚焦于恢复、组织、证据边界和收获闭环。
- **D002**：冻结 U01–U15 的来源准入与唯一 Primary owner，清理自指和无来源硬阈值。
- **D003**：批准在隔离 worktree 中实施 Task 1–3，不授权科学运行。
- **S003**：Task 1–3 已实现并分别通过独立复核；等待全阶段验证与统一提交。
- **V001**：全阶段独立终验 PASS；10 项新体系测试与 62 项原 baseline 测试全绿，范围审计无科学/历史污染。
- **H001**：冻结下一轮只读恢复入口与 Task 4–5 边界。
- **S004 / D004**：H001 接收核验通过，授权只实施 Task 4–5。
- **S004（续）**：Task 4–5 已实现；分任务审查与整阶段终验发现的并发断链、失败原子性、Atlas claim ceiling 和 report-source 合同问题均已修复，随后整阶段复审 PASS。
- **S005 / V002**：Phase 2 修复后独立终验 PASS；48 项 Skill 测试通过、1 项环境型 skip，旧 baseline 62/62 通过。
- **H002**：冻结 Task 6–7 的只读项目投影与 scheduler 审计入口，未授权 forward test 或科学运行。
- **S006 / D005**：H002 接收核验通过，Task 6–7 与只读桌面推演获授权。
- **D006**：Task 6 增补最小 `thesis-spines.v1.md`，补齐闭合 Adapter 的唯一拥有者，不虚构论文路线。
- **S007 / D007**：完成真实只读使用推演；STATUS 从 512 行全量 dump 收敛为 58 行有界八问入口，并明确分层授权与六个 blocked axes。
- **V003**：Task 6–7 与只读推演修复后独立终验 PASS；完整 Skill `60 passed, 1 skipped`，旧 baseline `62 passed`。
- **H003**：冻结下一轮 Task 8 fresh-agent blind forward tests 的入口与纪律。
- **R001 / S008 / V004**：Task 8 round 1 fresh-agent 盲测 5 类案例全 PASS；首轮 scorer 实现缺陷一次性批量修复（含 B6/B1 合法性加固），无 Skill 修订、无需重跑；独立 reviewer 与独立 verifier 复核均确认 prompt 盲、fixture 无泄漏、零 Skill 编辑、未跑科学实验、protected 18/18 hash 一致、全套测试 139 passed + 1 skipped。
- **S009 / D008 / V005**：Task 9 live shadow 在隔离 worktree `research-direction-lab-shadow`（分支 `codex/research-direction-lab-shadow`，从 `f79cb1b` 创建）执行；Foundation Certificate PASS（18/18 protected history hash 一致，standard-CMA 含 Godard z）；驱动 Skill 7-phase loop 在既有 READ_ONLY_MIGRATION_PREVIEW 地基上 replay + 派生 8 个 SHADOW-H010..H017 harvest entries（全部 CONTRACT/SLICE 级，DOMAIN/FAMILY 0 越界）；五类行为证据齐全（OBS-BLOCK 6 真实 blockers / OBS-ROTATE R1-R5 100% 续跑率 / OBS-SCOPE 最小 ceiling / OBS-HARVEST 每批 ≥1 / OBS-RECOVER session 启动恢复）；独立 verifier 11/11 PASS。
- **S010 / V006**：Task 10 cutover 完成；AGENTS.md 加 FR-27 路由索引（单行）；process.md / README.md 加 Skill 指针段；method-family-batch-exploration SKILL.md 加 superseded frontmatter（保留原文）；docs/architecture/research-direction-lab.md doc-steward mode 架构文档（锚定 13 个真实路径）；FR-22 vs Direction Lab 表面冲突解决（Direction Lab = 晋级前候选发现层，晋级仍必须走 GW/Contract/Execute）；独立 verifier 11/11 PASS，**live-activation authorized**。
- **S011 / D009 / V007 (pending)**：消费者部署收口。根因诊断 = shadow V005/V006 PASS 后从未回流消费者路径，导致普通根目录无 Skill/STATUS/Adapter/cutover 改动、全局 Skill 不存在、旧 Skill superseded 指针悬空。集成策略 = fast-forward（`merge-base(97473a2, 6ca142e) = 97473a2`，shadow 多 114 文件少 0 文件），从 `6ca142e` 创建 integration worktree 无冲突包含 Task 1-10 全部资产。全局 Skill 安装 36 文件字节级 hash 全等；fresh-agent discovery smoke（agent_a702565b）仅凭 AGENTS.md FR-27 自行发现 Skill 并正确回答 5 问。
- **S011 续接 / D010**：真实 SCIENCE_SCOUT 暴露“弱但正确 baseline 制造假问题”和“补证过重”双风险；完成新 pressure fixture、RED/ GREEN fresh-agent 测试和最小 Skill 修订。GREEN 行为已满足：不默认追 SOTA、一个主传统 comparator + 一个直接相关廉价扩展、ML 前必须达到 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`、Portfolio 不因仲裁单点停滞。
- **V008**：首次独立终验 PARTIAL 暴露逐字行为证据/scorer 与注册表缺口；修复后复验 PASS。Skill 测试 `67 passed, 1 skipped`，RED FAIL/GREEN 6/6 PASS，无残留 P0/P1/P2。
- **V009**：repo 与全局消费者 Skill 42 文件 SHA256 全等；全局 quick validation 与可移植测试 17/17 PASS。全局全套另有 3 项预期 repo-context failure，同项在 canonical repo 3/3 PASS，不阻断部署。
- **S011 续接 / D011 / V010**：真实 C01–C04 计划暴露“共同 system anchor 冒充任务专属 baseline”“共享输入冒充 runnable”及候选过窄问题；RED→GREEN、自动 scorer、独立复验和全局同步均 PASS。

## 未决项

- ~~Task 9 shadow 是否授权~~（已授权并完成，V005 PASS）。
- ~~Task 10 cutover 是否授权~~（已授权并完成，V006 PASS）。
- forward test scorer 的 B6/B1 fallback legality 当前由 forbidden-overlap 守卫保证，覆盖已有 forbidden_action 词表；未来出现词表外的非法动作需扩守卫。
- shadow 派生的 SHADOW-H010..H017 是否晋升到 main ledger：**未授权**；晋升需单独授权 + 重新 hash 绑定 + thesis-spines 更新。
- canonical-state 内部 stale self-checksums（event_log_sha256 / simulator.sha256）：正式激活前清理。
- Windows symlink / POSIX flock 动态测试覆盖：跨平台 CI 前补跑。

## 当前位置

Task 1–10、消费者部署、D010 与 D011 均已验证；全局消费者同步完成。下一科学阶段从 H004 续接：不直接只训 C01，先短时扩展机制级候选、纠正 readiness 与任务专属 comparator，再立即运行首批 `READY` 候选。
