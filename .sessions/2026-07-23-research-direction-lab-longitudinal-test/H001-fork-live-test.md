# Handoff: 启动长程真实运行测试

> 来源: S001 | 交接目标: fork 主控恢复权威状态并准备第一个受 guard 约束的 decision package
> 文件名: H001-fork-live-test.md

## 已完成边界

D017 的轻量控制接口已经进入实现与验证收口。本 topic 是独立 live-test mission，不是科学方向；顶部控制块 epoch 1 只允许 Recover/Map/Reconcile/T 准备，明确禁止科学实验、formal 变化、Skill 修改和基础设施建设。system design topic 保留为审查基线。

## 不要做什么

- 不从 conversation summary、候选名或“formal candidate”字样推导当前下一方向。
- 不运行科学实验、改变 formal stage、修改 Skill 或建设基础设施。
- 不为证明流程有效而伪造失败、正信号或固定批次数。
- 不把 blocked 当作 failed，不因候选变化新开 topic。

## 必读

1. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
2. `.sessions/2026-07-20-research-direction-lab-system/decisions.md#D017`
3. `.sessions/_registry.yaml` 中本 topic 的依赖与冲突项
4. `projects-overview.md`
5. `projects/thesis-fso/master-state.md`
6. Direction Lab 的 current projections；具体路径由恢复时从项目状态确认

## 接口变更（如有代码改动）

```yaml
foreground_control:
  owner: mission topic-index
  schema: rdl.foreground-control.v1
task_binding:
  owner: T work package
  schema: rdl.task-control.v1
validator:
  path: .agents/skills/research-direction-lab/scripts/validate_task_control.py
```

## 失败数据附录（如涉及路线失败）

system S014 已记录一次真实失败：压缩后将“Pilot-Jones 是 formal candidate”误推导为当前下一动作，越过 system-design gate；未运行实验或修改科学状态。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| scientific carrier 尚未选择 | 科学动作必须来自现有 owner 授权 | 初始 epoch 仅允许 Recover/Map/T 准备 | 完成 owner 恢复和合法 carrier 比较 |
| 长程稳定性尚未实证 | 只用真实事件验收 | 仅有一次负面故障和一次压缩恢复 | 多个真实包后由 system design 对话审计 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| control recovery | role、epoch、gate、allowed/forbidden 与磁盘一致 | D017/R003 | 首次恢复 1/1，尚不足以宣称长程 PASS |
| T authorization | control ref、epoch、action class 经 guard PASS | D017 | 尚无真实 T |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证至少 3 条关键事实：
  - 声称1：顶部控制块 role=LIVE_TEST、epoch=1 → [PASS/FAIL + 文件证据]
  - 声称2：初始 forbidden actions 包含 SCIENTIFIC_EXPERIMENT 和 FORMAL_STAGE_CHANGE → [PASS/FAIL + 文件证据]
  - 声称3：system D017 不授权具体 scientific carrier → [PASS/FAIL + 文件证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

1. 完成接收方验证。
2. 恢复 current/formal owners，区分 system mission、dormant science-scout 和 formal lane。
3. 形成至少两个机制或工作形态不同的合法 carrier/decision-package 选项；若权威状态只允许一个，明确说明原因。
4. 选择信息增量最高且授权合法的第一包，先更新 control block，再写含 control binding 的 T，并运行 guard。
5. 当前阶段止于 Recover/Map 和 T 准备；科学工作必须等现有 owner 授权并写入递增 epoch。
