# Task Brief: Pre-formal 方法工厂 Sprint 001

> 来源: S002 / D026
> 产出位置:
> `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-001/`
> 与 `projects/thesis-fso/worker-logs/step-019-preformal-method-factory-sprint-001.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只需本 T、仓库源码和本 T 指定的必读文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 48
  action_class: PREFORMAL_METHOD_FACTORY
  mission_checkpoint: CP017
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

此前长期 Goal 连续 17 个 package 的 `mission_method_delta` 全是 `NONE`；
formal active scientific carrier 为空，portfolio remap 为
`READY=0 / NEEDS_SMALL_ADAPTER=0`。Q14/T018 已由 D026 冻结，不执行。

**你的任务**：不要继续补文献/身份/形式化档案。选择一个仓库中已经能可靠运行的
共享 receiver 测试床，在同一个 sprint 内构造 3–5 个机制不同、receiver-visible、
可部署的最小方法，并用同一传统 baseline、paired realizations 和共享诊断 seeds
完成公平 smoke comparison。

**产出**：可运行代码、冻结合同、raw rows、聚合结果、方法卡和 worker log。

**最高纪律（违反任一条，本包废弃）**：

1. 这是 diagnostic-only 的 pre-formal 方法工厂，不是 GW Step 4a MVE；不得给出
   formal Go/Kill、论文可用数字、正式 promotion 或 family 结论。
2. 不执行或修订 T018，不做 Q14 Step 3.5，不下载/精读论文，不新开方向专题。
3. 不能只做审计或设计。只要共享测试床可用，本包必须实际构造至少 3 个方法并
   跑完公平比较；正常终态的 `mission_method_delta` 不得为 `NONE`。
4. 只用 receiver-visible、严格因果的部署输入。true channel/Jones、TX truth、
   future window、fixed-label BER、oracle branch 只能用于离线诊断，不能进入方法。
5. comparator 必须是同任务、已收敛的传统 receiver baseline；所有方法共享每个
   `(cell, seed)` 的同一次 realization。禁止各方法各造数据。
6. 不为制造增益修改公共物理参数、信道生命周期、调制映射、evaluator working
   region 或 baseline 调参债；不修改 `common/`、`params.py` 和 protected history。
7. 已明确 rejected 的轴不得换名重开。已有实现可作组件，但新 construct 必须有
   新的 deployable action 或组合结构，并写明与旧候选的差异。
8. executor 不更新 `.sessions`、mission-log、formal/current owner、registry、
   master-state 或 projects-overview；只写本任务产物与 worker log。
9. 不 push。结束时只提交本任务授权路径；若启动时 worktree 不 clean，先停止并
   报 `BLOCKED_SHARED_TESTBED`，不得把他人改动混入 commit。

允许的三个终态：

```text
DIAGNOSTIC_METHOD_SIGNAL
NO_DIAGNOSTIC_SIGNAL
BLOCKED_SHARED_TESTBED
```

---

## 1. 必读与当前边界

开始前依次读：

1. `.agents/skills/research-direction-lab/SKILL.md`
2. `.agents/skills/research-direction-lab/references/method-production.md`
3. `.agents/skills/sim-preflight/SKILL.md`
4. `stages/groundwork.md` 的 FR-22 窄例外
5. `thesis-lessons.md` 速查表与最近 3 条
6. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/S002-goal-zero-method-and-method-factory-redirection.md`
7. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D026`
8. `projects/thesis-fso/worker-logs/step-002` 至 `step-010` 的摘要、结论和
   failure mechanism；只读这些段落，不全文重演

先运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T019-preformal-method-factory-sprint-001.md
git status --short
```

任一失败即停止。不得把 conversation summary 当授权。

---

## 2. 执行步骤

### Phase A：15 分钟内冻结共享测试床

只在现有资产中选一个测试床，优先检查：

- `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/`
  下已完成 fairness/baseline-adjudication 的 runner；
- `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/`
  中已做过 source-equivalence 的 receiver slice。

不要默认它们有效。用既有 artifacts、测试与一个极小 rerun 确认：

- signal order、modulation mapping、paired realization 身份；
- baseline 能在注册 slice 内工作且无明显 divergence；
- primary metric 的定义与方向；
- 运行命令、runtime 和 raw-row 输出接口。

若两个入口都因已知 evaluator/物理身份问题不可用，写清证据后以
`BLOCKED_SHARED_TESTBED` 结束；不得转去修基础设施。

冻结 `factory-contract.v1.yaml`，至少包含：

- testbed source/hash 与运行命令；
- anchor、cells、diagnostic seeds 及 collision check；
- receiver-visible input/output contract；
- traditional baseline 与已冻结参数；
- primary/secondary metric；
- paired-realization 方法；
- runtime budget 与三个终态。

### Phase B：一次构造 3–5 个机制不同的方法

先写一张简表再编码。每个 construct 必须包含：

- `mechanism`：它改变 receiver 的哪一步；
- `deployable_action`：运行时实际做什么；
- `receiver_visible_inputs`；
- `cheap_alternative`；
- `difference_from_rejected_axes`；
- `primary_packaging` 与 `fallback_packaging` 的一句话草案。

候选必须来自不同机制族，例如稳健代价/更新律、因果状态调度、多起点与
receiver-visible 选择、传统模块的条件级联、低复杂度后处理；这只是例子，
不得为了凑数硬用。至少 3 个必须真正进入 runner，禁止只写伪代码或候选清单。

实现放在：

`projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-001/src/`

尽量以 adapter 复用现有 runner，不复制整套 simulator。

### Phase C：同包 semantic smoke + 公平比较

先做每个 construct 的输入敏感性与 action identity smoke：不同合法输入应能
导致预期不同动作；关闭新组件应退化到 frozen baseline。失败的 construct 可以
在本包内修一次，仍失败则标 `INVALID_CONSTRUCT`，但只要仍有至少 3 个合法
construct 就继续。

随后用同一 cells、同一 paired realizations、同一 diagnostic seeds 比较：

- frozen traditional baseline；
- 3–5 个合法 constructs；
- 每个 construct 的最强 cheap alternative（能共用时只跑一次）。

保存逐 `(method, cell, seed)` raw rows，不得只留 aggregate。至少报告：

- primary metric paired delta；
- 每 cell/seed help-hurt-tie；
- median、trimmed mean 和 bootstrap CI；
- divergence/invalid count；
- clean/easy boundary 的退化；
- runtime 或复杂度代理。

诊断信号必须同时满足：

1. 不依赖单 seed、单 cell 或明显 evaluator artifact；
2. primary paired delta 的方向在两个不重叠 seed halves 中一致；
3. 相对传统 baseline 有正 median，且 help 数大于 hurt 数；
4. 无不可接受的 clean-boundary collapse；
5. receiver-visible 与 causal contract 通过。

这是晋级筛选，不是论文显著性门。边缘结果保留为
`WEAK_DIAGNOSTIC_SIGNAL`，不得强行 Kill。

### Phase D：综合与停机

- 至少一个 construct 满足诊断信号门：
  `DIAGNOSTIC_METHOD_SIGNAL`，列出最多 2 个 winner。
- 已公平比较至少 3 个合法 construct，但均无信号：
  `NO_DIAGNOSTIC_SIGNAL`。
- 无法建立可靠共享测试床：
  `BLOCKED_SHARED_TESTBED`。

不得在本包继续给 winner 补论文、跑正式 seeds 或扩测试域。

---

## 3. 强制产物

目录：

```text
projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-001/
  factory-contract.v1.yaml
  method-map.v1.md
  src/
  tests/
  artifacts/raw-rows.v1.csv
  artifacts/result.v1.json
  synthesis.v1.md
```

worker log：

`projects/thesis-fso/worker-logs/step-019-preformal-method-factory-sprint-001.md`

`result.v1.json` 至少包含：

```json
{
  "status": "DIAGNOSTIC_METHOD_SIGNAL | NO_DIAGNOSTIC_SIGNAL | BLOCKED_SHARED_TESTBED",
  "mission_method_delta": "CONSTRUCT_CREATED | FAIR_COMPARISON_RUN | METHOD_SIGNAL | NONE",
  "testbed_identity": {},
  "constructs_built": [],
  "constructs_compared": [],
  "paired_results": {},
  "diagnostic_winners": [],
  "claim_ceiling": "DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE",
  "next_formal_action": null
}
```

正常完成 Phase B/C 时：

- 至少建 3 个：`mission_method_delta >= CONSTRUCT_CREATED`
- 至少公平比较 3 个：`mission_method_delta >= FAIR_COMPARISON_RUN`
- 有 winner：`mission_method_delta = METHOD_SIGNAL`

只有 `BLOCKED_SHARED_TESTBED` 可为 `NONE`。

---

## 4. 验收

- [ ] control validator PASS，启动时 worktree clean；
- [ ] T018/Q14 未执行或修改；
- [ ] 共享测试床、baseline 与 paired realization 有可复查证据；
- [ ] 3–5 个机制不同 construct 中至少 3 个实际运行；
- [ ] 无 privileged/future/TX-truth 部署输入；
- [ ] raw rows、aggregate、smoke tests 与 source hashes 齐全；
- [ ] 正常终态的 method delta 不是 `NONE`；
- [ ] 结论明确标为 diagnostic-only；
- [ ] 未更新 owner/mission/session 文件；
- [ ] 只提交本任务授权路径，未 push。

---

## 5. 最终回传（只回这五项）

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
