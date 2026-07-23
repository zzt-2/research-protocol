# Task Brief: D061 current owner reconciliation

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 2
  action_class: STATE_RECONCILIATION
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-001-current-owner-reconciliation.md`
> 日期: 2026-07-23
> 唯一任务文档: 执行方只需要本 T、仓库内列明的权威源和待协调文件

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`，分支应为 `codex/research-direction-lab-longitudinal-test`。

**你的任务**：把 D061/H017 已经确定的 current/formal routing 事实同步到 5 个可变 current views，消除 “P03 尚待选择”“backward 终验未完成”“LCOMM 2026 abstract-only” 等 stale current 表述。

**产出**：修改后的 5 个 current views、一个完整 worker-log、一个 consolidated commit。完成后聊天中只返回四行：`status`、`commit`、`worker_log`、`anomaly`。

**最高纪律（违反一条即失败）**：

1. 这是状态协调，不是科学研究；禁止仿真、Probe、Scout、MVE、全文检索/下载/精读和方法设计。
2. 不改变任何科学结论、candidate disposition、formal step 或 D061；只让 current routing 与已存在权威证据一致。
3. 不修改 protected history：`STATUS.v1.md`、`project.v1.yaml`、`canonical-state.yaml`、completion events、B001–B003、P03 Atlas artifacts。
4. 不修改 `master-state.md`、dual-pol formal topic 的 S/D/V/H、RDL Skill、session-governance 或 live-test control/T 文件。
5. 不把 Step 3.5 写成 PASS，不进入 Step 4a；不恢复 P03 或 dormant science-scout。
6. 一个对话内完成核查、修改、验证和一次提交；不 push。

## 1. 背景（了解即可，不要重新裁决）

权威事实链：

- `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D061`
  - P03 已选选项①：`PAUSED_RETURNED_TO_PORTFOLIO`，不是 Kill，family 不关闭。
  - Pilot-Jones 是 thesis-fso 当前 formal Groundwork 工作线。
  - 当前 step 是 GW Step 3.5 `PARTIAL/BLOCKED`，不是 Step 4a。
- `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md#V035`
  - JLT2022 backward chain PASS：refs=21、screened=7、new=0。
- `.sessions/2026-07-10-dual-pol-osl-groundwork/H017-pilot-jones-step35-partial-4paper-blocked.md`
  - OE 2021 与 LCOMM 2026 已完成全文精读。
  - 真正缺全文的是 4 篇：TCOMM `10.1109/TCOMM.2024.3522036`、JLT2025 `10.1109/JLT.2025.3640695`、JLT2022 `10.1109/JLT.2022.3224805`、JLT2023 `10.1109/JLT.2023.3284489`。
  - 4 篇均 `BLOCKED_NO_FULLTEXT`；下一合法边界是用户选择机构访问、作者邮件、显式带债豁免或等待 OA。
- `projects/thesis-fso/master-state.md` §2 和方法层重开轨表是 formal current owner，已正确反映 D061。
- `projects/thesis-fso/direction-lab/state/current.yaml` 的 authorization 块已写 Scout dormant / formal Pilot-Jones，但 recovery 与 next-action 字段仍部分 stale。

这些事实已经裁决；不要重新评价 Pilot-Jones 是否值得做，也不要提出新方向。

## 2. 任务详情

### 2.1 要关闭的状态不确定性

回答并落实：以下 5 个可变 current views 是否都能让下一次恢复得到同一 routing？

1. `projects-overview.md`
2. `projects/thesis-fso/direction-lab/README.md`
3. `projects/thesis-fso/direction-lab/state/current.yaml`
4. `projects/thesis-fso/direction-lab/portfolio/current.yaml`
5. `projects/thesis-fso/direction-lab/harvest/current.yaml`

### 2.2 执行方式

1. 开始前记录 `git status --short`、分支、HEAD，并确认工作树只含 T/control 准备提交后的干净基线。
2. 读取 D061、V035、H017、`master-state.md` §2；逐条建立“stale 字段 → 权威替换”表。
3. 只修改上述 5 个 current views：
   - `projects-overview.md`：更新 thesis-fso 当前 formal/Scout/P03/下一边界；不动其他项目内容。
   - Direction Lab `README.md`：当前状态和下一合法边界改为 D061；保留 Scout/P03 历史与层级说明。
   - `state/current.yaml`：更新 current header/source、`last_recovery_entry` 和 `next_action`；保留全部 effective conclusions/dispositions。
   - `portfolio/current.yaml`：更新 `recovery_entry` 和 `next_action`；不改 candidate status/notes。
   - `harvest/current.yaml`：只更新 `current_view.recovery_entry`、current source/next-action routing；不改 harvest dispositions、spines、claim ceilings。
4. 新建 `projects/thesis-fso/worker-logs/step-001-current-owner-reconciliation.md`，完整记录证据映射、修改字段、验证命令、未改边界和异常。
5. 使用独立 verifier 上下文复核；若环境无法提供独立 verifier，必须在 worker-log 明记 `INDEPENDENT_VERIFIER_UNAVAILABLE`，并执行下面全部确定性验收，不得伪称独立审查。
6. 所有验证通过后创建一个 consolidated commit；不 push。

### 2.3 强制产出格式

worker-log 必须包含：

```markdown
# Worker Log: D061 current owner reconciliation

## 输入基线
## 权威事实与 stale 字段映射
## Changed files
## Protected / excluded paths
## Validation
## Independent verifier
## Result
## Anomaly
```

`Result` 只能是 `PASS`、`PARTIAL` 或 `FAIL`。任何 protected/formal/scientific 语义被改，结果必须为 `FAIL`。

## 3. 已知陷阱

1. `STATUS.v1.md` 和 `project.v1.yaml` 虽然明显 stale，但 D061 明确保护；不能为了“全一致”修改它们。可变 current views 应明确把它们标为 historical/stale protected。
2. 不要把 V035 backward-chain PASS 误写成 Step 3.5 整体 PASS；4 篇全文门仍 BLOCKED。
3. 不要沿用旧文本 “LCOMM 2026 abstract-only”；已全文精读的是 OE 2021 + LCOMM 2026。
4. P03 是 PAUSED，不是 Kill；DOMAIN/CANDIDATE/FAMILY 仍 OPEN。
5. 不要把 “下一步 Step 4a” 写成已授权动作；下一边界仍是全文获取路径的战略选择。
6. 不得借整理 current view 顺手重写历史 conclusions、candidate cards 或 harvest 内容。

## 4. 验收

- [ ] 5 个目标 current views 对 formal=Pilot-Jones Step 3.5 PARTIAL/BLOCKED、P03=PAUSED、Scout=DORMANT 三项一致。
- [ ] state/portfolio/harvest 的 current recovery pointer 指向 H017 或明确引用 D061/H017。
- [ ] current next-action 明确 V035 backward PASS、4 篇具体 BLOCKED、OE2021+LCOMM2026 已全文精读、Step 4a 未授权。
- [ ] YAML 可由 `yaml.safe_load` 解析。
- [ ] `rg` 不再在 5 个 current-routing 段落中发现 “P03 用户决策未选”“backward 终验缺失”“LCOMM 2026 abstract-only”。
- [ ] `git diff --check` PASS。
- [ ] protected/formal/Skill/live-test control/T 均无 diff。
- [ ] worker-log 列出 exact changed files、验证输出和 verifier 状态。
- [ ] 单次 commit 成功，提交后工作树 clean；未 push。

## 附：回传格式

聊天中只返回：

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-001-current-owner-reconciliation.md
anomaly: <one line or NONE>
```
