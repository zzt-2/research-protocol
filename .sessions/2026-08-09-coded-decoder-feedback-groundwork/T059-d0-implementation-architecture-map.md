# Task Brief: D0 v3 implementation architecture map

> 来源: D011 / V005 / H004 / v3 owner | 产出位置: `projects/thesis-fso/worker-logs/step-105-d0-implementation-architecture-map.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: SOURCE_AUDIT
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：D0 可在 `projects/simulation/explore/coded-decoder-feedback/` 内以 truth-separated shell + imported numerical kernels实现，不修改 `common/` 或旧 P08 文件，并能拆成测试优先、低耦合的原子任务。
- 否决条件：必须修改 common/旧资产、TruthView 必须进入 receiver path、B2 无法在 one-way LDPC 内复刻、typed artifact 无法分层实现、或任一必需组件没有明确文件/依赖/test seam，则标 BLOCKER，不以泛化模块名掩盖。

## 任务

1. 完整读取 v3 owner、asset-preflight、H004、step-094/095/098/099/100，以及 `code-quality.md` 和 `reference/sim-template/` 中与 config/verify/result 有关的模板。
2. 逐文件读取可复用源码：`p08_coded_chain.py`、`p08r_chain.py`、`p08r2_chain.py`、`p08r2_metamorphic_gate.py`、`projects/simulation/common/_recovery.py`；只识别 kernel/接口，不继承旧 scientific conclusion。
3. 给出建议的新文件树（精确文件名）、每个文件职责、public type/function signatures、依赖方向、ReceiverView/TruthView 隔离点和禁止 import/caller path。
4. 把实现拆成最小 TDD 切片：contract/types → waveform/channel/BPS → coded chain/B0/B1/O1 → typed artifact/dev-freeze/statistics → B2 → runner/verify integration。每片列 RED test seam、GREEN 最小实现、可独立审查的完成判据。
5. 标出可直接复用、必须 wrapper、必须新写的函数；特别审计 P08-R2 prefix LS rank deficiency、P08 per-real sigma2、legal 4-state rotation、fresh decoder restart、no common edits。
6. 提供对 plan owner 可直接采用的任务依赖图和并行边界；指出任何预计 >15 分钟的执行任务如何再切片。
7. 输出 `IMPLEMENTATION_ARCHITECTURE_READY / BLOCKED` 与 blocker；不得写代码、测试或计划 owner。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-105-d0-implementation-architecture-map.md`。
- 只读源码/文档；禁止 pytest、import 项目执行、D0/benchmark/science、web/search/download、owner/治理/源码修改、commit/push、p05/pycache触碰。
- 10 分钟目标，15 分钟硬上限。
