# Task Brief: D017 owner identity loader seal — independent verification

> 来源: D017 / V013 / T112 step-158 | 产出位置: `projects/thesis-fso/worker-logs/step-159-d0-owner-identity-loader-seal-independent-verification.md`
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

## Independence / terminal

- 独立验收T112 final bytes；禁止用step158 PASS、author mutation/helper或author diff断言。
- 只写step159；其他文件只读。≤12分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D017_OWNER_IDENTITY_LOADER_SEAL_INDEPENDENTLY_VERIFIED`；只有该PASS后才可把final owner authority交给schema compiler。

## Frozen final bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
identity_seal=68d21b4af54e43e34f23e882a3ebf0be8393d67487877471a787a8e2b3d4371f
scientific_projection=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
contract=50ae149a77588c34cedd2a2e8aab5078b6b4e3d4ea310ba85fe577f76f5ca170
tests=3da14d85a9a743726f985897ac65cd70f331069dcecdfefbd6d09296cba272be
pre_contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
step158=8822c12890d083e1a0ca720c0e9ebca24489715d3ffd566e092acfeab03a3dc5
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
decisions=b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8
verifications=beaa804651c37e0f2e33415bfc7cb2cf261f492f2121e9811696f34fa87dbfe8
R001=1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37
step157=bfab0aac3434a9aae22adb7b5e0d5e3963b2b5c534d3fb18ef85db7311057b78
```

## Fresh independent matrix

1. Static source proof：exact D0Contract四字段；new loader explicit I/O only；channel只接D0Contract。自行把final owner/identity两个constant各替回old值，重算source必须精确等于pre_contract；replacement count各1，无第三处production变化。
2. 独立canonical oracle从public frozen view复算128 literals、3 grid roots、8 anchors、final identity seal与scientific projection；D017 descriptors=`7/1,32/41/49,8 signatures`、S4七项、HMM manifest reference exact。
3. Fresh mutations至少36项：除author矩阵外增加dataclass replace/hash spoof、same-type descriptor swaps、phase/op map swaps、S4/HMM/reference、old owner/old identity seal混配；wrong accept/reject=0/0。
4. Fresh pytest：T112 exact四节点、mutation node、显式四文件全量；0 fail/error/skip/xfail/warning。
5. I06 additive regression：至少24 legal/illegal closed-world cases + static no-new-loader runtime reachability，mismatch=0。
6. begin/end owner/source/test、HEAD/staging、Frozen bytes、P05、cache、diff-check保护。

要求assertions>=400、mutations>=36、pytest全绿、I06 cases>=24、P0/P1/P2=0/0/0；否则FAIL/INCOMPLETE。

## Environment / return

Windows Python3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`，pytest `-B -m pytest -p no:cacheprovider`。step159记录命令、stdout/exit/SHA、全部计数与final log SHA。
