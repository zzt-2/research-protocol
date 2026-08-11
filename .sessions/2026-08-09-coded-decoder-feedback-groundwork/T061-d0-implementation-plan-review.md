# Task Brief: D0 v3 implementation plan fresh independent review

> 来源: D011 / V005 / CP012 / step-104–106 / d0-implementation-plan | 产出位置: `projects/thesis-fso/worker-logs/step-107-d0-implementation-plan-review.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：plan 已把 v3 owner、step-105 架构和 step-106 全测试地图无遗漏地转成 test-first、文件责任唯一、每任务≤15分钟、最多三路并发且不越过 CP012 的可执行计划。
- 否决条件：缺任一 frozen invariant/test family；测试后置；parallel tasks 写同文件或依赖倒置；单任务显然超15分钟且无分点；环境/命令不可执行；runtime import旧副作用模块；Truth/fit/science 可达；benchmark可先于 code review；或任何 S1–S4/adapter/heldout 偷渡，均 FAIL。

## 冻结输入

```text
plan=13d0d5a8242b65f97748446e5caa8f8f7a79b169bf317bfdecc7f97eb5e1bdcd
step-104=6db4a529fa8c9227e68375184636c3c7315a6e5005b62116760311e8d069098d
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
v3 owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
```

## 任务

1. 完整读取 T061、plan、v3 owner、H004、step-104/105/106；不得只读摘要。
2. 建 coverage matrix：CV/WC/RM/B2/SS/DF/AC/EB 每个 ID 是否恰有 owner task、production file、RED→GREEN、completion gate；标 duplicate/gap。
3. 审 dependency/parallel map：同批文件必须 disjoint、依赖先完成、最多3路；I01–I20 每项是否可在15分钟内按明确 test-ID分点中止。
4. 审 architecture：scalar per-pol RSS/31、no SOP/2×2 LS、Cpost/N0 per-real除2、four legal states、fresh LDPC、exact HMM、typed seven artifacts、five/five/one、no-refit、atomic receipt-last、dual costs与benchmark完整。
5. 审 environment/commands：Windows Python/Sionna事实、no-pyc/no-cache、PowerShell file-list expansion、无隐式 install/skip；不运行命令。
6. 审 CP012 boundary：plan/code files不得含 scientific runner；I20只能在 unit+fresh code-review PASS 后；benchmark不触及 scientific ranges/estimands；science需新D/V/CP。
7. 给 `PASS/FAIL, P0/P1/P2` 与逐项 actionable findings。只有 `0/0/0` 可写 `D0_IMPLEMENTATION_PLAN_READY_FOR_TDD_EXECUTION`；本 review不授权 benchmark/science。
8. 终检输入初末SHA、p05 4/4、staging与唯一写入。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-107-d0-implementation-plan-review.md`。
- 只读 parse/hash/grep/确定性覆盖审查；禁止 import项目、pytest、D0/benchmark/science、web/search/download、plan/owner/治理/源码/测试修改、commit/push、p05/pycache触碰。
- 10 分钟目标，15 分钟硬上限。
