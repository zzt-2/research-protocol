# Task Brief: D0 I03 independent waveform reverification after P1 repair

> 来源: step-123 FAIL + step-125 TDD repair | 产出位置: `projects/thesis-fso/worker-logs/step-128-d0-i03-waveform-reverification.md`
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

## 审查问题

独立证明 step-123 P1 public-constructor fail-open 已在唯一 owning boundary 根治，且 registered assets、四 N、24 rotations 和合法 controlled output 无回归。

## 冻结输入

```text
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
test=f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157
step-123=c899f896ebb7a4d59c7031688295ab26af3f99f16e9a3f72164e508f62778d72
step-125=092f535d64781f1ef9a0353ee70b85c55bb176cecd2b2327d2c0b79731b4974e
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

Create only `projects/thesis-fso/worker-logs/step-128-d0-i03-waveform-reverification.md`；source/tests只读不修。

## Fresh reverify

1. 核 SHA/保护；重放 step-123 exact invalid object及 T079 每类 N/shape/map/inverse/schedule/known/nonfinite mutation，均必须在 constructor fail closed。
2. fresh 跑新 regression、原 WC01/02/03/08、full waveform、I02 regression。
3. 重跑四 N schedule/bytes/read-only、24 rotation cases/k0 copy、global RNG/import/static audit。特别验证 legitimate rotated waveform 与 unrotated known reference可构造，防止过严 gate。
4. 补一组绕过 happy path的普通 public constructor cases：完全一致合法 object接受；单独篡改任一关系拒绝。Prefix/Pilot constructors只有在能直接到达 production consumer且违反 owner时才判，不扩大 P1。
5. Findings-first P0/P1/P2；任何 fail-open或合法回归 => FAIL。终检只 step-128，保护不变；≤15 分钟；无 benchmark/science/web/install/commit/push。

## 返回

P0/P1/P2、fresh counts/matrix、log SHA；terminal=`I03_VERIFIED_READY_FOR_BATCH1`、`I03_VERIFICATION_FAIL` 或 `INCOMPLETE`。
