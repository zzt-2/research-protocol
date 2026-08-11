# Task Brief: D0 v3 implementation plan minimal-repair fresh re-review

> 来源: step-107 FAIL / D011 / V005 / CP012 / revised d0-implementation-plan | 产出位置: `projects/thesis-fso/worker-logs/step-108-d0-implementation-plan-rereview.md`
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

- 假设：revised plan 只做 additive repair，已关闭 step-107 四个 P1，同时保持 87/87 test IDs 唯一归属、v3 physics/artifact/science boundary 与实施前置门不漂移。
- 否决条件：CV06–08/DF11 仍可在真实 subject 不存在时假闭合；RED seam 依赖 placeholder/空 registry/missing-module acceptance；显式 DAG/parallel read-write 不稳定；I19 任一 reviewer 无可信≤15分钟 stop point；7 日方程重复计时、遗漏固定 2.00d post-D0 C1/contingency/owner line items；或修复引入任何新覆盖缺口、science/benchmark 越权，均 FAIL。

## 冻结输入

```text
revised plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-107=72b561d7cd69f276113dcf9c866ff85d2fe448890a9a90a27ead5aa09439b4e1
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
v3 owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
```

## 任务

1. 完整读取 T062、revised plan、step-107、step-106 和 v3 owner；不得只读摘要。
2. 对 step-107 P1-1：确认 I02/I13 只闭本地 IDs；I17A 在所有真实 subjects 后，CV06–08/DF11 对缺 phase/callable/模块 fail closed，RED seam 与 gate 不接受 placeholder/空 registry/missing module。
3. 对 P1-2：确认 I09 显式依赖 I04；I11 完成后 I10 才读取 finalized `artifacts.py`；所有 batch 依赖闭合、读写稳定且≤3路。
4. 对 P1-3：确认 I19A/B/C 文件和 axes 边界足以各自≤15分钟，I19D 只做全局集成复核但不盲信 shards；输出 schema、超时 terminal、修复后重审规则完整。
5. 对 P1-4：逐项复算 owner `4.50 + 2.00 + 0.50 = 7.00`；确认 receipt/EB08/EB10/I20 使用无交无漏的 consumed+remaining D0 partition，固定 post-D0 2.00d，正确扣减/保留 contingency，无 double count/false PASS。
6. 回归审查：从 step-106 重建 CV/WC/RM/B2/SS/DF/AC/EB 87 IDs 的唯一 task/file/RED→GREEN/gate；审 frozen physics、runtime、no-science/no-benchmark-before-review 和环境命令未漂移。
7. 输出 `PASS/FAIL, P0/P1/P2` 与逐项 closure table。只有 `0/0/0` 可写 `D0_IMPLEMENTATION_PLAN_READY_FOR_TDD_EXECUTION`；review 不授权实际 benchmark/science。
8. 终检冻结输入初末 SHA、p05 4/4、staging=0、唯一写入。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-108-d0-implementation-plan-rereview.md`。
- 只读 parse/hash/grep/确定性覆盖审查；禁止 import 项目、pytest、D0/benchmark/science、web/search/download、plan/owner/其他治理/源码/测试/结果修改、commit/push、p05/pycache触碰。
- 10 分钟目标，15 分钟硬上限；到时未闭合写 `INCOMPLETE`，不得超时续跑。
