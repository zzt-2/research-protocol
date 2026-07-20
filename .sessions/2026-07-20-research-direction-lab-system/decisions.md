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
