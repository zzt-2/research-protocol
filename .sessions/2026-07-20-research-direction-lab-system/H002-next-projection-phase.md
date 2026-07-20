# Handoff: Research Direction Lab 只读项目投影阶段

> 来源: S005 | 交接目标: 决定并实施 Task 6–7，不进入 forward test 或科学运行
> 日期: 2026-07-20

---

## 到哪了（状态）

Task 1–3 已由 V001 验证并提交；Task 4–5 已由 V002 独立终验 PASS。当前通用 Skill、Communications Profile、ProjectAdapterV1 schema、五个确定性工具和四个历史 replay fixtures 已具备；项目 Adapter 实例、portfolio/harvest 投影和旧 scheduler 迁移审计尚未创建。

## 下一步干什么

先读实施计划 Task 6–7、S005 与 V002，核验 `project.v1.yaml` 仍不存在和历史保护仍成立。若用户授权，先按 TDD 建立只读 `READ_ONLY_MIGRATION_PREVIEW`，再逐函数审计旧 scheduler；不得把旧调度逻辑直接搬入通用脚本。

## 纪律（续接者必须注意的）

- 用户原话：“代码只做比较轻量的控制以及那些碎片步骤。流程尽可能靠skill？”
- 用户原话：“咱们这次最好先一次把整个体系都规划好？”
- Task 6 只做事实投影，不授权候选选择、batch、B004、ML 或论文数字。
- Task 7 先审计再迁移；任何 candidate/resource matching、固定完整性计数或科研 stop decision 都不得保留为通用控制逻辑。

## 接口变更

```yaml
contracts:
  - id: C002
    type: interface-change
    description: "确定性安全工具与历史 replay fixture 合同"
    location: ".agents/skills/research-direction-lab/"
    change: "新增 hash/receipt/event/reducer/status API 与四个只读历史案例"
    consumed_by: "Task 6 read-only project projection and Task 8 forward tests"
    verification_result: PASS
    verified_by: V002
```

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Windows symlink 动态覆盖 | 路径边界需跨平台证据 | 当前主机权限导致 1 skip | 在可创建 symlink 的 Windows/POSIX 环境补跑 |
| POSIX `flock` 动态覆盖 | append 并发锁需跨平台证据 | Windows 上仅静态复核 | 首次 POSIX CI/运行前补跑 |
| `jsonschema` 元模式验证 | Adapter 实例消费前验证 schema 规范合法 | 尚未安装可选依赖 | Task 6 创建实例前处理 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 通用隔离 | generic Skill/scripts 通信项目词与 scheduler API 均 0 命中 | D001 / U11 | Phase 1–2: PASS |
| 历史保护 | protected science/canonical 变更为 0 | 项目安全 | Phase 1–2: PASS |
| 安全工具 | 完整 Skill tests 全绿，环境能力型 skip 显式记录 | Task 4 / V002 | 48 passed, 1 skipped |
| 旧 baseline | 三个 targeted suite 全绿 | 工作树基线 | 62/62 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1: `project.v1.yaml` 不存在 → [PASS/FAIL + 证据]
  - 声称2: Skill tests 基线为 `48 passed, 1 skipped` → [PASS/FAIL + 证据]
  - 声称3: B001–B003/P03/canonical 无 Phase 2 diff → [PASS/FAIL + 证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”
