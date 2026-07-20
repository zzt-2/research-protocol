# Topic Index: Research Direction Lab 完整体系设计

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-07-20（Task 8 round 1 PASS）

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

## 已确认结论

### 不变量

- **Skill-first, code-guarded**：开放式研究判断和长期循环由 Skill/AI 负责；代码只硬化确定、可测试、错误代价高的不变量。
- **论文产出优先**：治理通过不能冒充科学进展；所有批次都必须进入论文收获或明确的可复用资产。
- **先全景后批跑**：从已有基点展开候选族，先归类和统一规划，再成批比较；少数 winner 才进入重型 Deep Evidence。
- **局部阻断不终止**：存在其他合法工作时，单候选失败、接口缺失、局部负面或 critic 退回都必须自动换路。
- **通用与领域解耦**：通用代码和核心 Skill 不包含具体通信项目语义；领域规则进入 Profile，项目事实进入 Adapter。
- **原话可追溯**：目标体系的长期约束必须能指回用户原话；执行提示词和用户自然原话分开标注。
- **唯一拥有者**：执行流程最终由一个主 Skill 拥有；项目文档只保存事实和状态，不复制流程全文。

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

## 未决项

- Task 9 shadow 是否授权（Task 8 round 1 PASS 仅授权"考虑"Task 9，不等于长期自动化可靠）。
- forward test scorer 的 B6/B1 fallback legality 当前由 forbidden-overlap 守卫保证，覆盖已有 forbidden_action 词表；未来出现词表外的非法动作需扩守卫。

## 当前位置

Task 1–7 已由 V001–V003 分阶段验证 PASS。Task 8 round 1 fresh-agent 盲测（5 类案例）已由 V004 独立终验 PASS：5 个独立 fresh agent 在只给 Skill + 原始案例事实的盲条件下，全部维持续跑、claim ceiling、harvest、组织、领域隔离不变量；scorer 实现缺陷已一次性批量修复，零 Skill 修订、零科学运行、protected history 18/18 hash 一致。Task 9 shadow、Task 10、live activation 和科学实验仍未授权；下一入口为用户决定是否授权 Task 9。
