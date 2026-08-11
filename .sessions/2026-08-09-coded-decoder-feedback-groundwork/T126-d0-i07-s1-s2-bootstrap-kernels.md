# Task Brief: D0 I07 slice A — S1/S2/bootstrap kernels

> 来源: d0-implementation-plan I07 / SS03–SS07 / T125 | 产出位置: `projects/thesis-fso/worker-logs/step-172-d0-i07-s1-s2-bootstrap-kernels.md`
> 日期: 2026-08-11

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_UNIT_TEST
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Scope / terminal

- 仅新建 `projects/simulation/explore/coded-decoder-feedback/statistics.py`，修改 `projects/simulation/tests/test_d0_schemas_statistics.py`，写 step-172。其他只读。
- 15分钟硬停；禁止 I/O、owner/YAML读取、scientific seed/artifact、benchmark/science/MVE、install/stage/commit/push。
- 首先写并真实运行 SS03 RED；新模块首个 `ModuleNotFoundError` 是允许的 bootstrap RED。文件名与stdlib `statistics`冲突，测试必须按绝对文件位置加载，不得污染全局 import。
- PASS=`D0_I07_S1_S2_BOOTSTRAP_GREEN`，只表示 I07 slice A；SS08–10留给同文件串行 slice B。

## SS03–SS07 exact acceptance

1. `reduce_s1(rows)`：只接受 `20*12*2=480` 或 `50*12*2=1200` 个已验证 typed S1 rows；`event_present iff transition_count>0`、array长度、seed/cell/pol exact coverage；返回 point event count/rate。fixture 480行2 events => `1/240`。
2. `reduce_s2(rows)`：验证每个 off `(seed,cell,pol)` 恰9 fixture projections、同一 physical/computation/content/random owner且只计费一次；on方法恰 B1/B2/O1，off恰B1。先在每个 cell pool integer numerators/denominators，再 hard/mid/clean 等权，禁止 row mean/global pooling。
3. SS05 hand fixture exact：hard `(B1on,off,O1,B2)=(9,3,3,5)/12`，mid=`(4,0,2,3)/8`，clean=`(1,0,0,0)/4`；macro damage=`5/12`（非`11/24`），recoverability=`13/18`（非`9/14`），coverage=`13/18`（非`2/3`）。
4. `bootstrap_paired(blocks,reducer,*,seed=2026081001,draws=10000,invalid_terminal=None)`：每个 stratum重新初始化 `Generator(PCG64(seed))`，不触碰global RNG；NumPy percentile `method='linear'`。10-block首两draw indices必须为 `[1,8,2,9,1,3,0,8,9,2]` 与 `[5,7,3,1,8,3,1,2,8,4]`。
5. 10,000 replicates 中invalid/NA `500`时 valid=9500 可产CI；`501`必须 fail closed。recoverability terminal=`UNSTABLE_DAMAGE_DENOMINATOR`，coverage terminal=`UNSTABLE_HEADROOM`；valid-only CI不填充、不裁剪（样本1.2保留1.2）。
6. 结果用 frozen/slotted typed dataclass；模块只依赖NumPy和I05 typed rows/constants/`SchemaError`。相同rows唯一复算，不池化strata。
7. fresh negatives至少10项：S1少行/seed/cell/pol重复或缺失/event mismatch；off拆成两个computation；wrong on/off method；row/global pool sentinel；500/501 boundary；global RNG污染。wrong accept/reject=0/0。

## Commands / receipt

- RED：`...python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_schemas_statistics.py::test_s1_coverage_event`
- GREEN：只跑 SS03–07 nodes，再显式跑现有 SS01/SS02/SS11 + SS03–07；不要跑包含219s FULL node的整文件。
- 固定 `PYTHONDONTWRITEBYTECODE=1`,`PYTHONHASHSEED=0`。step-172记录RED/GREEN、test totals/time/stdout SHA、goldens/negative counts、文件SHA、HEAD/staging/P05保护、P0/P1/P2。

