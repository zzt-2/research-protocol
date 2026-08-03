# Topic Index: Research Direction Lab 完整体系设计

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v1
  control_epoch: 11
  role: RDL_MASTER
  mission: 将 2A/2B 两个论文方法候选各自闭合到可用终态
  active_lane: PARALLEL_THESIS_BOUNDED_CLOSURES
  authority_pointer: .sessions/2026-07-20-research-direction-lab-system/decisions.md#D022
  decision_gate: V016 PASS；只允许 T004/T005，各自一个包、一次确定性修复、终态即停
  allowed_actions:
    - PROTOCOL_AUDIT
    - THESIS_BOUNDED_PACKAGE_EXECUTION
  forbidden_actions:
    - NEW_DIRECTION_DISPATCH
    - OLD_CAMPAIGN_REOPEN
    - COMMON_PARAMS_MUTATION
    - FORMAL_STAGE_CHANGE
  next_legal_action: 创建两个隔离执行任务，分别执行 T004/T005，持续到各自 terminal disposition
```
<!-- RDL-CONTROL:END -->

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-08-03（D022/V016：2A/2B bounded closure 任务书终验 PASS，待派发）

## 专题信息

- **slug**: `2026-07-20-research-direction-lab-system`
- **title**: Research Direction Lab 完整体系设计
- **性质**: 目标体系蓝图、分阶段实施与真实运行复盘；Task 1–10、消费者部署和 D010–D013 已验证，真实 campaign 已 SCIENCE_FREEZE，当前先审计设计承诺与实际运行差距

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
- 基于 S009 的科学语义审计，当前范围扩展为 Probe/Scout/Deep Evidence 分层、单一恢复投影、current-view/lineage、harvest 状态索引和抗膨胀目录的设计、推演、Skill 实施与独立验证；不借此运行科学实验。
- 基于真实 science-scout campaign 的 SCIENCE_FREEZE，当前先冻结四层记忆与双日志，复盘 system 设计在真实长跑中的兑现差距；不改变 Pilot-Jones 正式 Groundwork。
- R002 完成后，先记录并分析一次真实压缩恢复跑偏，设计、演练和审查轻量长程运行协议；用户认可后以 fork 做真实纵向运行，设计完成前不修改 Skill/controller、不派具体科学方向。
- 基于 live-test R009 对 T001–T026 的效果审计，允许只修恢复三问、方法工厂硬路由、signal promotion preflight 与真实恢复 receipt；不新增 controller，不改变科学 verdict。
- 基于 H003/R004 的历史回归，只补 executable semantic gates、contribution tiers 与 lightweight persistence；不增加第四类 patch，不修改既有科学 verdict 或 formal owner。
- 基于长程 campaign 与 12 篇硕士论文包装审计，允许最小增加论文方法章保留门，并对 2A/2B 做 RED→GREEN；不放松 scientific/formal 门，不运行实验，不修改既有科学 verdict。
- 基于 D022 用户显式授权，允许在两个隔离 worktree 各执行一个已冻结的 2A/2B bounded packaging closure，直至得到章节就绪、支持材料、拒绝或真实外部阻塞终态；不开放新方向、不修改 common/params、不恢复旧 campaign。

### 明确不含

- 不修补 V037 的资源匹配或继续扩展 Portfolio Autopilot；
- 不启动 B004、ML 训练、P03 后续实验或新科学批次；
- 不改写 B001–B003、P03 Atlas、canonical state 或历史 receipt；
- 不把目标态蓝图写成当前架构现状；
- 不批量迁移或删除旧科学目录；新布局渐进采用，旧历史继续 append-only 保留。

### 范围变更记录

- **[2026-08-03] D022**：从 2A/2B 只读包装诊断扩展为两个隔离 bounded closure 执行包。
  - 原因：T002/T003 均判 `NEEDS_ONE_BOUNDED_PACKAGE`，用户明确要求两个单独对话持续执行直到得到确实可用的终态。
  - 新范围：T004 只闭合 calibration-aware robust CPR；T005 只闭合 fixed-point branch-routed CPR；允许必要的 sandbox 代码、仿真、benchmark、raw evidence、独立 verifier 和分支内提交。
  - 影响的未决项：2A/2B 从“待决定是否派实验”改为“各执行一个包”；旧 campaign、其他轴、正式阶段与论文正文继续冻结。

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
- **[2026-07-21] Probe 与恢复体系重设计（D012）**：用户要求先记清当前状态，再优化记录/恢复/文件组织，推演固定后才改 Skill 并大规模运行。
  - 原因：S009 出现完整可复现链未发现目标函数常数塌缩，且“极小”工作反复扩成重流程。
  - 新范围：体系蓝图、目录与 current projection、成本分层、历史反例与 fresh-agent 恢复推演、后续 Skill 修订验证。
  - 明确排除：本轮直接改 Skill、运行科学实验、重跑 C04/C09、构建复杂 scheduler、删除历史。
- **[2026-07-21] Probe 与恢复体系实施（D013）**：D012 的设计和 RED 推演完成后，用户明确要求当前对话继续完成 Skill 并交付下一工作提示词。
  - 新范围：主 Skill/references、可选 current-view adapter 路径、显式 disposition reducer、STATUS current-harvest 指针、forward fixtures、测试、全局消费者同步和下一 campaign 交接。
  - 明确排除：运行新科学实验、改写旧 artifacts、复杂 scheduler、固定候选数、把领域科学判断写入通用代码。
- **[2026-07-23] 长程运行复盘（D015）**：用户要求先整理此前整个过程，避免在未理解真实失效前继续派工或补规则。
  - 新范围：只读审计旧方法论、governance pilot、system 落地、science-scout、项目控制面和 Git 轨迹，形成 R002。
  - 明确排除：继续修改 Skill/controller、恢复 Direction Lab 科学 campaign、改动 Pilot-Jones 正式状态或运行新实验。
- **[2026-07-23] 运行协议设计与 fork 纵向测试（D016）**：R002 后的首次压缩恢复现场复现主线偏离，用户要求先落日志、仔细设计，不根据单次事故急改规则。
  - 新范围：分析 S014 现场故障及历史同类，比较并演练少量轻量运行协议候选；设计获认可后再一次性落到唯一 owner，并 fork 当前对话真实运行。
  - 明确排除：当前直接修改 Skill/controller、派 Pilot-Jones 或其他科学方向、把单次事故直接固化成全局规则。
- **[2026-07-29] T001–T026 效果审计后的最小修订（D019）**：用户确认基本每次交互都会压缩，并授权审计后修改。
  - 原因：CP001–CP017 方法增量 0/17；T019 后出现 2 个 signal，但 formal 转化仍为 0/2，且 current snapshot 已混入 package history。
  - 新范围：只改 RDL 恢复路由、方法工厂硬触发、promotion preflight、真实恢复 receipt 和 live current-view 压缩。
  - 影响的未决项：下一 live test 以至少一个 signal 转为 active carrier/`PROMOTION_READY` 为成功，不以包装或写作材料替代。
- **[2026-08-02] 三类 Skill 最小 patch 与历史回归（D020）**：用户明确授权接收 H003 后修改 Research Direction Lab Skill。
  - 原因：真实 campaign 暴露 scale/action 语义门、贡献分层与长程记录减负三个缺口。
  - 新范围：只改 executable semantic gates、contribution tiers、lightweight persistence 及既有 receipt validator/测试，并同步个人运行副本。
  - 影响的未决项：本轮 patch 在 V014 PASS 后冻结；不启动 AMC、不修科学包、不创建 P12、不改变 formal owner。
- **[2026-08-03] 论文方法章保留门（D021）**：用户明确要求记录当前失效、调整 Skill，保证可包装内核不因未达主方法信号而丢弃，并另开两个对话分别研究 2A/2B。
  - 原因：长程运行擅长纠错但新方法产出为零；最新同行论文与内部资产审计确认 2A/2B 均有方法形状，只各缺一个 bounded package。
  - 新范围：双门分账、当前 Skill RED、最小 Skill patch、GREEN/独立终验、两个隔离只读包装任务。
  - 影响的未决项：D020 的科学诚信、贡献分层和轻量持久化继续有效；只解冻“不得再改 Skill”，不解冻科学实验或旧方向。

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
- **成本随声明升级**：前置不确定性默认用单问题 Probe；多候选公平比较才进入 Scout；只有稳定且论文重要的信号进入 Deep Evidence。
- **语义先于完整性**：objective/label/output/metric、平凡解、identity、output support、最小过拟合和信息边界未通过时，不得用 provenance PASS 升级科学结论。
- **当前视图优先恢复**：current projection 是恢复入口，append-only lineage 是审计与复现入口；显式 disposition 优先于 mtime 和旧 prose。
- **双日志不丢细节**：长程 S 只记裁决和轨迹，worker-log 记完整单项过程，raw artifacts 保存原始证据；聊天只传索引。

### 其他结论

- 现有 `method-family-batch-exploration` 是候选族批量部分的可复用原型。
- Direction Lab 的 receipt/hash/stale/history protection 等确定性资产可保留。
- `science_slots`、固定最小批次数求解和通用资源匹配不进入目标体系。
- harvest 逐单元评估但不逐单元强制造条目；普通 Probe 不默认生成完整治理文档链。
- `T###` 是不可变任务书，H 只用于主控续接；不得为每个轻量工作包机械生成 S/D/V/H 全套。
- 方法产出分为 `THESIS_MAIN_METHOD`、`THESIS_ENGINEERING_COMPONENT`、`SUPPORTING_MATERIAL`；支持材料不成为 active carrier，真实且公平的 B 级工程组件保留合法入口。
- 科学主方法门与论文方法章门分账：未达 `METHOD_SIGNAL` 不自动等于 `SUPPORTING_ONLY`；语义有效的中粒度内核先做章节能力判定，invalidated evidence 仍不得晋级。

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
- **S012 / D012**：S009 外部语义审计暴露“极小探针扩成重证据链”和“artifact fidelity 掩盖目标函数常数塌缩”。冻结新顺序：先设计 Probe/Scout/Deep Evidence 分层、单一恢复投影、current-view/lineage、harvest 状态索引与抗膨胀目录；推演固定后再改 Skill 和大规模运行。本轮仅立项。
- **S012 续接 / D013 / V011**：完成三层成本、语义先行、current projection、轻量 harvest 与抗膨胀目录的设计和实施；首轮/二轮独立审查发现的行为证据、lineage、current harvest 与 Scout conditional 冲突全部修复；Skill `90 passed, 1 skipped`，repo/global 56/56 hash 全等，V011 PASS。
- **S013 / D014-D015**：在最新谱系冻结四层记忆、双日志和主控—GLM 极短中转；H004/T001 不再是本专题当前入口，下一步先以控制链全读、关键转折深读和原始证据抽查形成 R002 历史复盘。
- **H005**：为新主控对话冻结 R002 只读复盘入口；要求先核验最新 worktree/HEAD/编号谱系，不修改 Skill、不运行实验。
- **R002**：完成旧方法论、governance pilot、system、science-scout、项目 current views 与 Git 轨迹的证据化复盘。主因不是规则缺失，而是单轮合规/replay/provenance 验收替代了多轮科学优先级，semantic smoke 晚于完整证据链，且 current/release/formal owner 未原子收敛；建议先拍板 owner/current release 是否已满足纵向测试前置，再按 D013/D014 实测，仅按观察到的具体失败修唯一 owner。
- **S014 / D016**：R002 后首次真实压缩恢复中，主控把“Pilot-Jones 是正式候选”误推成“下一步推进 Pilot-Jones”，越过 system-design gate；用户纠正后撤回。该现场故障成为 R003/D017 的 RED 样本。实现后本对话再次自动压缩，主控按 epoch 2 控制块恢复并仅继续终验，形成首个真实正向恢复样本（1/1，不足以宣称长程 PASS）。
- **R003**：承接 S014 的详细设计分析，完成必要能力/非目标/owner 边界、四种架构比较和两轮历史组合场景演练；提出轻量协议 v0.1 与纵向事件验收。详细设计从长程 S 下沉到 R，避免 S014 膨胀。
- **D017 / implementation**：采用 R003 的轻量前台控制接口；guard 与 Skill 路由完成 TDD/回归（repo 97 passed, 1 skipped），59 个非缓存 Skill 文件已与个人消费者镜像逐字节一致，消费者 guard 6/6 PASS。longitudinal live-test mission 仅以 Recover/Map 权限准备，不携带科学授权。
- **D018 / v2 amendment**：phase-1 审计确认无严重跨 lane，但 mission success 漂移为反证/修复闭包。v2 改用正向方法合同、formal/method 双账、固定 `mission-log.md` 三层记录、checkpoint guard 和 master-only owner 更新；不建 controller。
- **V012**：独立终验 PASS；两项初审 P2（旧 checkpoint 缺证据指针、registry epoch 过期）已关闭，P0/P1/P2=0。
- **live R009 / D019**：T001–T026 审计确认方法工厂改善近端发现，但 signal→formal 为 0/2；授权 v2.1 最小路由修订，不重写体系。
- **R004 / D020 / V014**：接收 H003 后完成六案修改前后盲测；只补五门 executable evidence contract、三层贡献合同与三层轻量持久化，个人运行副本同步且独立终验 PASS（P0/P1/P2=0）。
- **S015 / R005 / D021 / V015**：长程效果与同行包装审计确认剩余缺口是正常包收尾缺少独立章节能力检查；结构 RED、盲测 GREEN 与独立终验均已闭合。
- **D022 / T004 / T005 / V016**：用户授权两个隔离对话各执行一个 bounded closure；任务合同独立终验 PASS，正面结果不预设，但必须闭合到可用 terminal disposition。

## 未决项

- ~~Task 9 shadow 是否授权~~（已授权并完成，V005 PASS）。
- ~~Task 10 cutover 是否授权~~（已授权并完成，V006 PASS）。
- forward test scorer 的 B6/B1 fallback legality 当前由 forbidden-overlap 守卫保证，覆盖已有 forbidden_action 词表；未来出现词表外的非法动作需扩守卫。
- shadow 派生的 SHADOW-H010..H017 是否晋升到 main ledger：**未授权**；晋升需单独授权 + 重新 hash 绑定 + thesis-spines 更新。
- canonical-state 内部 stale self-checksums（event_log_sha256 / simulator.sha256）：正式激活前清理。
- Windows symlink / POSIX flock 动态测试覆盖：跨平台 CI 前补跑。
- ~~H004/T001 已冻结下一科学 campaign 的恢复入口~~（D015 暂停执行；仅保留为历史入口，不再作为当前 next action）。
- 新科学项目首次采用 current layout 时，需要渐进生成 `state/current.yaml`、`portfolio/current.yaml`、`harvest/current.yaml`；禁止为了迁移整洁批量改写旧 artifacts。
- ~~R002 历史复盘尚未执行~~（已完成）：见 `R002-long-horizon-runtime-retrospective.md`。
- D021/V015 已完成；D022 仅授权 T004/T005 两个 bounded closure，不构成旧 campaign 或新方向的普遍解冻。

## 当前位置

H003 已接收，R004/D020 只补 executable semantic gates、contribution tiers 与
lightweight persistence。六案审计重放、自动测试、个人 Skill 同步与 V014 独立
终验均 PASS（P0/P1/P2=0）；既有科学 verdict、dormant longitudinal topic 与
formal owner 未变。

**2026-08-03 当前入口**：T002/T003 已完成只读诊断，均为
`NEEDS_ONE_BOUNDED_PACKAGE`。D022 已将控制面递增到 epoch 11；当前只允许在两个
隔离 worktree 执行 T004/T005，各自一个 bounded closure、一次确定性修复，并闭合到
明确终态。V016 已确认 P0/P1/P2=0；任何新方向、common/params 修改、正式阶段变化仍禁止。
