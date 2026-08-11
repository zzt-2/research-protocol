# Task Brief: D0 I02 repair fresh re-verification

> 来源: step-112 FAIL / step-113 repair / I02 repaired candidate | 产出位置: `projects/thesis-fso/worker-logs/step-114-d0-i02-repair-reverification.md`
> 日期: 2026-08-10

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

## Hypothesis / finding disposition oracle

- 假设：T067 关闭真实 P1-1/P1-2 的类别根因，而非只补已知 13 case；I02/CV04/05/09 可进入 Batch1。
- P1-3 复核 oracle：T065 原文要求 permission mutation 后“**相应 action** fail closed”。true→false 后 capability set 变为原集合的严格子集，不是 fail-open；只有 CP/D/V/epoch/action-class 漂移或 execution/science 变 true 才应清空全部。若实现符合该单调最小权限语义，step112 P1-3 必须标 `DISPOSED_NON_DEFECT`，不得要求 all-or-nothing。
- 否决条件：known或unseen owner-equivalent alias仍过；object/structured/nonplain ndarray过或共享 mutable；普通 numeric/bool broken；safe receiver names误杀；fresh tests非6/6；权限出现新增 action；或保护漂移，均 FAIL。

## 冻结输入

```text
contract.py=b61b26c3488ff4cc851b5c57b00827a3895a896473f0db7e8f29692348ff6c50
test=c3948e072213afe23bca0700f77b3feb354a0516a7de4549842a34fccd97f9b5
step-113=2f170dce2da26871a96033fe2ab952f5dd6a562ae665a64242dd37d361556470
step-112=9f906374838236e9d2ac95b52f23b936a9cad92e6af3c5508bb824c8dd7b6342
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 任务

1. 完整读取 T068、T065/T067、step112/113、owner views、candidate/tests；核 frozen hashes/protection。
2. fresh run完整 test 文件 6/6；静态审 semantic predicate、plain ndarray gate、safe-name exceptions、recursive traversal、action subset。
3. 用独立 inline matrix（不写 repo）验证：
   - step112 9 aliases + 4 ndarray cases全拒绝；all original literal aliases仍拒绝。
   - **未写入 candidate tests 的类别抽样**至少包含 `info_bits`, `data_symbols`, `true_channel`, `physical_channel_receipt`, `channel_realization`, `injected_label`, `natural_label`, `final_cw_errors`。逐项依据 owner category判断；若某项可合理是 receiver-visible，必须给具体字段语义后剔除，不能静默通过。
   - punctuation/case/nesting variants；benign `TruthView` under safe key拒绝；plain numeric/bool defensive copy/read-only。
   - safe controls至少 `received_samples`, `equalized_samples`, `common_cpr_phase_trace`, `receiver_noise_estimate`, `global_rotation_state`, `bps_state`, `source_sha256`, `code_sha256`, `content_sha256`, `channel_source_sha256` 接受，防止 denylist 过宽。
   - exact five actions accept；每个正 permission false 后集合恰为 five-minus-one且绝不新增；identity/execution/science mutation清空；scientific/unknown拒绝。
4. 对 step112 P1-1/2/3 逐项给 CLOSED / OPEN / DISPOSED_NON_DEFECT；只有无 open P0/P1/P2 才 PASS。
5. 终检 candidate/test/owner/plan hashes、only step114新增、p05/cache/staging/HEAD、不运行 benchmark/science。

## 边界与返回

- 只写 `projects/thesis-fso/worker-logs/step-114-d0-i02-repair-reverification.md`；不得修 code/test。
- Windows Python `-B`，no bytecode/cache；禁止 benchmark/science/web/search/download/commit/push。
- 目标 8 分钟，15 分钟硬上限。
- 返回 `PASS/FAIL/INCOMPLETE, P0/P1/P2`；只有 `0/0/0` 可写 `I02_VERIFIED_READY_FOR_BATCH1`。
