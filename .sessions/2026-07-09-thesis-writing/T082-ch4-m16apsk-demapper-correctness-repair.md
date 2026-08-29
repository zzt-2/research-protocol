# Task Brief: Ch4 共用 16APSK hard demapper correctness repair

> 来源: S028 / D061 / V036 / T081 | 产出位置: `projects/simulation/common/_modulation.py`、Ch4 seam tests/note、worker log
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 23
  action_class: CH4_DEMAPPER_CORRECTNESS_REPAIR
  mission_checkpoint: CP023
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

以 RED→GREEN TDD 将公共 `m16apsk_demod` 修正为其 docstring/星座合同声称的全 16 点欧氏最近邻 hard decision，并记录对历史 raw 的兼容边界。本任务只修 correctness，不运行任何 BER replay、cell、smoke 或 production。

## 开始前强制读取

1. active topic-index CP023、D061/V036、T081 与 production-evidence design/plan Task 1；
2. `sim-preflight`、`thesis-lessons.md` 速查表与最近三条、`code-quality.md`；
3. `projects/simulation/common/_modulation.py` 的 16APSK mapper/demapper、Ch4 `development.py` 调用链、历史 confirmation manifest/raw identity 和相关 tests；
4. 运行 task-control validator；失败立即停止。

## TDD 合同

1. 先创建 `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_m16apsk_ml_demod.py`，至少包含：
   - 全部 16 个 normalized constellation points 的 label round-trip；
   - 冻结反例：`r=0.9155`、first inner-point ray，brute-force label=`0000`，历史实现错误选 outer label；
   - 固定 deterministic off-boundary complex cloud，与独立构造的全部 16 点 brute-force argmin labels 完全一致。
2. 在修改实现前运行 focused test 并保存 RED 证据；至少冻结反例必须 FAIL。
3. 最小实现只删除 radius-forced outer choice，使 ring 选择完全由 `d_outer_min < d_inner_min` 决定；同步修正 docstring 中“先按半径判环”的旧说明。不得改变调制器、radii、Gray labels、normalization 或 tie rule。
4. GREEN 后运行 Ch4 local tests、`projects/simulation/tests/test_common.py`、APSK ring-gated 与 APSK LLR correctness tests；从 repo root fresh `rg -l "m16apsk_demod" projects/simulation -g "test_*.py"` 记录直接测试 census。

## 历史与 scope 边界

- 不修改 `confirmation_*`、`development_*`、Ch3 results/figures、params、receiver actions、reducers 或论文包。
- 不跑 T081 A1；旧 T071/Ch3 raw 继续代表其历史 commit 下的结果，不静默重写。
- 新建 `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper-correction-note.md`，记录旧条件、反例、RED/GREEN 命令与历史兼容债务。
- 新建 `projects/thesis-fso/worker-logs/step-082-ch4-m16apsk-demapper-correctness-repair.md`，facts-first 汇总修改、测试与 terminal。

## 验证与终态

- 运行 focused/direct-caller tests、`py_compile`、task-control validator、精确文件白名单与 `git diff --check`。
- 由未参与实现的 reviewer 独立构造至少一组新 complex points，用 brute-force 16 点 oracle 核对；内容审查不能只看测试绿灯。
- terminal 仅允许：
  - `DEMAPPER_CORRECTNESS_REPAIR_PASS`；
  - `DEMAPPER_CONTRACT_CONFLICT`；
  - `DEMAPPER_REPAIR_INVALID`。

通过只表示 CP024 可讨论 A1 historical-observation replay；不得转述为 C4 BER 信号仍在或方法已成立。一次任务不 commit、不 push，由主控统一接入。
