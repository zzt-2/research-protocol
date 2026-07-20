# Handoff: Research Direction Lab 盲测阶段待授权入口

> 来源: S007 | 交接目标: 在新上下文恢复 Task 8 边界并等待用户明确授权
> 日期: 2026-07-20
> 授权状态: 本 H 只冻结入口，不构成 Task 8 执行授权

---

## 到哪了（状态）

Task 1–7 已分阶段实现并由 V001–V003 独立终验 PASS。真实双偏振 OSL 只读 Adapter/portfolio/harvest/STATUS 已存在，但仍是 `READ_ONLY_MIGRATION_PREVIEW`；旧 scheduler 仅被审计，未删除或改写；科学运行和 B004 仍未授权。

## 下一步干什么

新对话先读 Task 8、V003、S007 和五个 replay 输入（四个历史 + 一个非通信），恢复 blind-test 设计与边界；只有用户在该对话明确授权 Task 8 后，才可在与本轮实现上下文分离的 fresh agent 上跑 blind prompts。聚合全部失败后只允许一次批量 Skill 修订，再用全新上下文重跑。不要把 S007 桌面演练算进 forward-test 样本。

## 纪律（续接者必须注意的）

- 用户原话：“继续。顺便推演一下使用？”——S007 已完成“看起来怎么用”，Task 8 要回答“fresh AI 实际会不会这样做”。
- H003 不是执行授权；用户未明确批准 Task 8 前只能只读恢复和说明测试设计。
- 不把期望答案、候选排名或失败机制透露给被测 agent。
- 一批测完再改 Skill，不逐案例打补丁；新增硬规则必须证明现有判断原则不足。
- Task 8 不运行科学实验，不创建 B004，不把测试回答写入论文或项目 canonical state。

## 接口变更

```yaml
contracts:
  - id: C003
    type: interface-change
    description: "只读 ProjectAdapterV1 投影与 compact STATUS CLI"
    location: "projects/thesis-fso/direction-lab/project.v1.yaml"
    change: "新增真实项目事实投影、portfolio、harvest、thesis-spines、58行STATUS与四输入stdout-only renderer CLI"
    consumed_by: "Task 8 forward-test prompts and Task 9 shadow recovery"
    verification_result: PASS
    verified_by: V003
  - id: C004
    type: interface-change
    description: "no-scheduler semantic contract"
    location: ".agents/skills/research-direction-lab/tests/test_no_scheduler_contract.py"
    change: "拒绝候选选择、资源匹配、完整性证明和停止合法性进入通用脚本"
    consumed_by: "all later Skill/script revisions"
    verification_result: PASS
    verified_by: V003
```

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 尚无 fresh-agent 行为证据 | Skill 应能自动续跑且守 claim scope | 只有结构、fixtures 和桌面演练 | Task 8 必须闭合 |
| 尚无 live shadow | 长期恢复/换路需真实观察 | Task 9 未开始 | Task 8 PASS 后另行授权 |
| Windows symlink / POSIX flock 动态覆盖 | 跨平台路径与锁应有动态证据 | V002/V003 保留债务 | 对应平台首次启用前补跑 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| P0 history/scope | 0 次 | Task 8 计划 | 未测 |
| 合法替代存在时继续 | 100% | U04 / Task 8 | 未测 |
| harvest/status 输出 | 每个案例均产生 | U07 / Task 8 | 未测 |
| 非通信领域隔离 | core 输出 0 项项目专属术语 | U11 / Task 8 | 未测 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1: `project.v1.yaml` mode 仍为 `READ_ONLY_MIGRATION_PREVIEW` → [PASS/FAIL + 证据]
  - 声称2: 完整 Skill 基线为 `60 passed, 1 skipped` → [PASS/FAIL + 证据]
  - 声称3: B004 不存在且 protected diff 为 0 → [PASS/FAIL + 证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”
