# Handoff: Research Direction Lab 下一实施阶段

> 来源: S003 | 交接目标: 在已验证的 Skill/Profile/Schema 地基上决定是否实施 Task 4–5
> 文件名: H001-next-phase.md

## 已完成边界

Task 1–3 已在隔离 worktree `D:/code/study/research-protocol/.worktrees/research-direction-lab-system` 完成并经 V001 独立终验 PASS：U01–U15 溯源、精简主 Skill、七个 reference、Communications Profile、ProjectAdapterV1 schema。没有创建项目 adapter 实例，没有迁移历史状态，没有科学运行。

用户关键约束原话：

- “感觉，是skill的能力和代码的能力混了？代码只做比较轻量的控制以及那些碎片步骤。流程尽可能靠skill？”
- “咱们这次最好先一次把整个体系都规划好？”

## 不要做什么

- 不回头修 V037 scheduler，不添加 `science_slots`、candidate/resource matching 或 work-conservation solver。
- 不把通信术语或双偏振 OSL 项目事实写进通用 Skill/scripts/schema 字段名。
- 不因四个无 Skill 基线场景已经表现良好，继续堆叠案例式 if/then 规则。
- 不在未完成历史 replay 和 shadow 前宣布新体系已正式激活。
- 不运行 B004、ML 或其他科学实验，除非新对话明确加载 `sim-preflight`、冻结合同并获得执行授权。

## 必读

1. `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`
2. `.sessions/2026-07-20-research-direction-lab-system/S003-first-implementation-phase.md`
3. `.sessions/2026-07-20-research-direction-lab-system/verifications.md`
4. `docs/superpowers/specs/2026-07-20-research-direction-lab-system-blueprint.md`
5. `docs/superpowers/plans/2026-07-20-research-direction-lab-system-implementation.md`
6. `.agents/skills/research-direction-lab/SKILL.md`

## 接口变更（如有代码改动）

```yaml
skill_owner: .agents/skills/research-direction-lab/SKILL.md
domain_profile: .agents/skills/research-direction-lab/references/profiles/communications.md
project_adapter_contract: .agents/skills/research-direction-lab/references/project-adapter-schema.yaml
project_adapter_v1_required_fields:
  - project_id
  - formal_goal
  - anchor
  - components
  - paths
  - runnable_axes
  - blocked_axes
  - historical_counterexamples
  - commands
  - budgets
```

## 失败数据附录（如涉及路线失败）

四个 Skill 前 blind baseline 场景均未复现目标判断失败；这不是 Skill PASS 证据，而是删减规则的依据。Task 1–3 首轮审查发现的多 owner、自指、虚假精确 RED 日志、弱负向结构测试和不可发现 Profile 路由均已整改并复审通过。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 尚无确定性 safety tools | code 只硬化确定性不变量 | Task 4 未开始 | 用户/下一对话批准 Task 4 |
| 尚无历史 replay fixtures | Skill 行为需真实历史回放 | Task 5 未开始 | Task 4 工具边界稳定后 |
| 尚无项目 adapter 实例与 shadow | 目标架构不能直接冒充现状 | Task 6/8/9 未开始 | Task 4–5 通过并另开隔离执行 |
| `jsonschema` 元模式未验证 | schema 消费前应验证规范合法性 | 结构测试 PASS；依赖缺失 | 首次创建 adapter 实例前 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 历史保护 | protected science/controller/canonical 变更为 0 | 项目安全 | Phase 1: PASS |
| 通用隔离 | generic core/scripts 通信禁词为 0 | U11 / D001 | Phase 1: PASS |
| Skill 结构 | 官方 validator PASS，结构测试全绿 | skill-creator / Task 2 | Phase 1: PASS |
| 旧 baseline 回归 | 三个 targeted suite 全绿 | worktree 创建基线 | 62/62 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

先只读恢复并确认是否授权 Task 4–5。若授权，Task 4 只实现 hash/receipt/append-event/reducer/status 等确定性小工具；Task 5 只建立只读历史 replay fixtures。不得顺手创建双偏振 OSL 项目实例或运行科学实验。
