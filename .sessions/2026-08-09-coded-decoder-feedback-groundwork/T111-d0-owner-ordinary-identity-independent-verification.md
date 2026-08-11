# Task Brief: D0 owner ordinary identity completion — independent verification

> 来源: D017 / T110 step-156 / V012 | 产出位置: `projects/thesis-fso/worker-logs/step-157-d0-owner-ordinary-identity-independent-verification.md`
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

## Independence / scope / terminal

- 独立验证T110 final owner；不得把step-156 PASS、author checker或其expected派生当断言。
- 只写step-157；owner/source/tests/session/P05只读。不跑pytest/benchmark/science/MVE。
- verifier源码先写入step-157 fence，再经stdin fresh执行；目标10分钟、12分钟硬停止。
- PASS=`OWNER_ORDINARY_IDENTITY_COMPLETION_INDEPENDENTLY_VERIFIED`；上限只接收D017 owner bytes，不等于loader seal或I05完成。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
pre_owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
final_owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
contract_tests=745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
R001=1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37
decisions=b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8
verifications=fb3173c6db7809d44f67d2c03619eb9ad3b3901b44cbd10bb9fea7daadaea67e
step155=ce5edec6a9e8102bea6840abfff028bf8d36ca73d75e3dd9e6bab8078dfdfde9
step156=387e3840bdf7ba0acaf839515070e5da1cc931e1a42392eb91440974ca613419
```

## Fresh independent matrix

1. Strict duplicate YAML、exact owner begin/end SHA；identity仍13 top-level sections、schema/header/alias policy不漂移。
2. 不看author builder，直接从D017与outer owner table PK/enums构造七类ordinary expected descriptors：projection/key order、exact `{name,source,atom_type}`、phase/operation rules、7 unique work kinds、S2 method map、S3 record→phase map与raw record_type_as_split、S4 exact七IDs。
3. HMM必须无`exact_binding_kind`；reference exact kind/raw_field/payload_schema/rule/logical_member_authority；证明它不实例化consumer-binding manifest且chunk PK fields为8项typed descriptors。
4. Exact counts：ordinary/HMM=`7/1`、work descriptors=32、PK descriptors=`41/49`、unique phase-operation signatures=8；ordinary bindings/logical IDs=`42,967/27,487`、HMM logical/chunks=`22,800/263,520`、ledger=50,287。
5. Fresh独立复算128 literals、3 grid roots、全部10个既有goldens、6 accounting counts；S2/BPS IDs+roots及四组HMM roots逐字节不变。
6. Fresh mutations至少24项并预标expected：七类逐项kind/phase/op/source/atom/order漂移、S2 method op swap、S3 phase swap、B2 clean/controlled same-type kind swap、B04 literal、S4 missing/duplicate/order/substitute、HMM reference kind/raw field/schema/rule/member authority、HMM误加LOGICAL binding、PK same-type swap。wrong accept/reject=0/0。
7. 结构化删除T110 additions、恢复rule/HMM旧field/coverage/validator lists后必须deep-equal pre-owner parsed structure；raw scientific projection仍`c61c88e...`。permission/science/grid/count/golden drift none。
8. begin/end owner、HEAD/staging、Frozen bytes、P05、cache census、`git diff --check`；除step157外无写入。

要求assertions>=250、mutations>=24、goldens=10/10、counts=6/6、mismatch=0、P0/P1/P2=0/0/0；否则FAIL/INCOMPLETE。

## Environment / return

Windows Python3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；禁止install/commit/push/stage。step-157记录完整命令/output/exit/stdout SHA、final log SHA、terminal与全部计数。
