# Topic Index: Research Direction Lab 完整体系设计

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-07-20

## 专题信息

- **slug**: `2026-07-20-research-direction-lab-system`
- **title**: Research Direction Lab 完整体系设计
- **性质**: 目标体系蓝图与分阶段实施；Task 4–5 已终验 PASS，不运行科学实验

## 范围边界

### 原始目标（冻结）

一次性规划一套能从零或从已有稳固地基出发、长期自动寻找并验证研究方向、组织清晰不过重、持续积累毕业论文素材的完整体系；明确 Skill、通用代码、领域 Profile、项目 Adapter、项目状态和用户决策的职责边界。

### 当前范围

- 审计既有 `method-family-batch-exploration`、Direction Lab v0.3、governance pilot、Portfolio Autopilot 和用户原话；
- 冻结目标体系蓝图、资产迁移表、实施顺序和验收场景；
- Task 1–3 已完成；Task 4–5 的确定性安全小工具与只读历史 replay 已实现并由 V002 独立终验 PASS；
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

## 未决项

- 是否授权 Task 6–7 的只读项目投影与旧 scheduler 迁移审计。
- 现有 `campaign_core.py/campaignctl.py` 中哪些小函数值得提取，留到 Task 7 逐函数审计。

## 当前位置

Task 1–3 已由 V001 验证并提交；Task 4–5 已由 V002 独立终验 PASS，等待一次性提交。Task 6–10、project adapter 实例、forward behavior、shadow 和科学实验均未开始；下一入口为 H002。
