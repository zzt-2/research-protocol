# Task Brief: Ch4 canonical formal raw production

> 来源: S028 / D068 / V043 / T088 | 产出: 唯一canonical formal raw与独立raw-only结构验收
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 30
  action_class: CH4_CANONICAL_FORMAL_RAW_PRODUCTION
  mission_checkpoint: CP030
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在scientific manifest与replacement execution lock双锁下，唯一运行一次无override的128-latent canonical formal production，生成`ch4_formal_raw.json`后立即停机；由独立reviewer在不导入runner的条件下复核raw结构与provenance。不得在本任务运行canonical reducer、计算grade、作图或解释BER。

## 冻结输入

- scientific manifest SHA=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；
- execution lock SHA=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`；
- runner/reducer/entry/tests及四项dependencies、HEAD、environment必须与lock actual match；
- IDs=`30000..30127`，每ID 119 actual cells、5 arms与1 delta0 reference；总census=`128/384/15232/76160/ref128`。

## 文件白名单

- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_checkpoint.json`（仅运行中；成功后必须消失）
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_raw.json`（唯一canonical输出）
- `projects/thesis-fso/worker-logs/step-089-ch4-canonical-formal-raw-production.md`
- 独立reviewer写 `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/canonical-formal-raw-independent-verification.md`

所有代码、tests、manifest、lock、T086/T087/T088 artifacts均只读。

## 执行前门

1. 完整读取sim-preflight、T089、D068/V043、scientific manifest、replacement lock、step-087/088与两份independent reports；task-control CP030/epoch30 PASS。
2. fresh focused tests=`19/19`、五文件pycompile、manifest/lock/bound hashes/HEAD/environment actual match。
3. canonical raw与checkpoint均必须不存在；aggregate/receipt也必须不存在。任何已有文件立即停机。
4. 记录开始时间、预期census与唯一exact命令；不得运行试探性cell或第二个smoke。

## 唯一运行

仅运行一次：

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_ch4_formal_production.py --formal`

禁止任何其他CLI参数。成功条件：exit=0、stdout终态=`CH4_FORMAL_PRODUCTION_COMPLETE`、raw存在、checkpoint消失。不得因运行中间进度或partial BER停止、改参数或另开总体。

如外部中断且checkpoint存在，不自动恢复；先停机并由独立reviewer核binding、自摘要与已完成latent唯一性。若科学/代码/schema错误则不恢复、不删checkpoint、不重跑。

## 实现者成功后只读检查

- 只核raw SHA、文件大小、purpose、ID集合、top-level/scene/cell/row/reference census与双锁header；
- 不汇总BER、不调用reducer、不计算crossing/bootstrap/grade，不选cell或曲线；
- 写step-089 log后停机。

## 独立raw-only复核

- reviewer不得导入runner，不运行formal命令；用标准库/独立脚本从raw核128 IDs、三scene、119 cells/ID、5 roles、tau、bits、truth marker、namespace、same-scene/cross-Np pairing、delta0 exact/no-row、all hashes与双锁bindings；
- 可导入pure reducer仅做结构validation，但不得发布canonical aggregate、grade或科学summary；
- replacement lock与bound files在raw生成后必须保持exact；fresh focused仍19/19；
- 给P0/P1/P2与`CH4_CANONICAL_FORMAL_RAW_READY`或`CH4_FORMAL_RAW_INVALID`。

## 禁止

- 不运行canonical reducer，不生成aggregate/receipt，不计算或报告grade/正式BER结果；
- 不作图、写正文、检索、改Groundwork/Skill/controller、恢复Ch5或新方向；
- 不重跑formal、不补seed、不删不利rows、不跨scene pooling。

## 终态

- `CH4_CANONICAL_FORMAL_RAW_READY`：唯一raw、exact census/provenance/pairing/truth与独立P0/P1=0；
- `CH4_FORMAL_RAW_INVALID`：任一binding/census/schema/pairing/truth失败；禁止reduction与重跑。
