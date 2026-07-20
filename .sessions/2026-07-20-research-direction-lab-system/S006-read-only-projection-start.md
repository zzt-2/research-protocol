# [S006] 只读项目投影与使用推演启动

> 2026-07-20 | Task 6–7 实施 | 进行中

## 目标

按 H002 实施 Task 6–7：建立双偏振 OSL 的只读项目 Adapter/portfolio/harvest/status 投影，逐函数审计旧 scheduler；同时做一次不产生行为评分的桌面使用推演。

## 记录

H002 接收核验：

- 当前位于 linked worktree `codex/research-direction-lab-system`，工作树干净。
- `project.v1.yaml` 不存在；Skill 基线为 `48 passed, 1 skipped`。
- B001–B003、P03 与 canonical 相对 HEAD 无改动。
- 当前专题依赖均存在，`conflicts_with=[]`。

用户“继续。顺便推演一下使用？”授权 Task 6–7，并要求检查实际使用形态。为保持与 H002/计划的边界一致，本轮“推演”仅展示只读恢复、状态阅读、收获记录与局部阻断换路的数据流，不运行 Task 8 的盲测/评分，不触发科学 runner。

Task 6 事实源盘点发现：闭合 Adapter schema 强制要求独立 `paths.thesis_spines`，而原计划只列四个投影文件。按唯一拥有者原则，新增一个最小 `harvest/thesis-spines.v1.md`，只记录当前无可晋级 spine；不以 ledger/README 冒充，也不为迁就文件清单削弱 schema。见 D006。

## 决策引用

- D005：批准 Task 6–7，并把本轮使用推演限定为只读桌面演练（新建）。
- D006：用最小空状态文件补齐 thesis-spines 唯一拥有者（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；见 topic-index 2026-07-20 / D005 范围变更。

## 后续

先并行盘点 Task 6 事实源、Task 7 旧 scheduler 接口与桌面演练边界；随后按 TDD 分任务实施并独立审查。本轮不进入 Task 8–10。
