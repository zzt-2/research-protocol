# Task Brief: D0 I03 P1 repair — WaveformBuild relational gate

> 来源: step-123 independent FAIL P1-1 | 产出位置: `projects/thesis-fso/worker-logs/step-125-d0-i03-waveform-p1-repair.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Review disposition / 否决条件

- 接受 P1-1：公开 `WaveformBuild` 是 `apply_persistent_rotation` 的直接输入类型，仅 frozen/read-only 不能证明 registered layout；N=999/shape-map 不一致复现确实 fail-open。
- 修复边界：只在 owning `WaveformBuild` construction boundary 闭合 registered N/shape/schedule/maps/known/finite invariants，并加入 regression；不重写 prefix/pilot/rotation 算法，不扩到 channel。
- 否决条件：需改 contract/owner/其他模块；靠隐藏 constructor 或 test-only flag；破坏合法 rotated build；或 15 分钟未形成 RED/GREEN，则停在 test boundary。

## 冻结输入

```text
waveform.py=bab2a491e0afb1b32b188ea0ce1465b9b6fe2a1ee08593c2c2544c1fe3c2b748
test=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-123=c899f896ebb7a4d59c7031688295ab26af3f99f16e9a3f72164e508f62778d72
repro=82146072a89a046d00d90e597c93c8bae850cc1076e9434643ddf811314f53a3
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/waveform.py`
3. Create `projects/thesis-fso/worker-logs/step-125-d0-i03-waveform-p1-repair.md`

## Test-first repair

1. 先只追加 `test_waveform_build_relational_validation_fail_closed`，覆盖 step-123 exact repro，并逐类 mutation：N、waveform/known/mask/map shape，map duplicate/out-of-range/inverse/schedule，known mask/symbol schedule，nonfinite waveform；同时合法 base 与 24 rotated builds 仍构造成功且 read-only。
2. production 改动前跑该 exact node，必须因 invalid constructor 被接受而 assertion FAIL；记录新 test SHA、old source SHA、command/output SHA。说明 append 改变 file SHA，故本 regression RED **取代**旧 file-level receipt；原四 tests 在新 file 中保持原文并在后续全量跑。
3. 最小 GREEN：`WaveformBuild.__post_init__` defensive-copy 后验证：N exact registered；owner-derived expected total/schedule；`waveform`/`known_symbols=(2,total)`、mask/time map=(total)、data map=(6144)；finite；data ranks exact bijection/inverse；nondata exact `-1` 且等于 known mask；prefix/pilot/terminal known reference schedule exact、data known-symbol slots zero。校验必须允许 controlled rotation 后 waveform 与 unrotated known reference不同。
4. 不改 public API；`apply_persistent_rotation` 继续只接受 fully validated type。跑 regression GREEN、原 WC01/02/03/08、full waveform、I02 regression；记录 counts/output SHA，无 skip/xfail/warning。
5. 终检只三目标变化；p05/cache/staging/HEAD 保护；不 benchmark/science/web/install/commit/push。≤15 分钟。

## 返回

RED/GREEN、full regression counts、三目标 SHA；terminal=`I03_REPAIR_READY_FOR_REVERIFICATION`、`INCOMPLETE` 或 named blocker。
