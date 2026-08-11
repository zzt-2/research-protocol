# Task Brief: D0 owner identity loader seal refresh after D017

> 来源: D017 / V013 / T108–T111 | 产出位置: `projects/thesis-fso/worker-logs/step-158-d0-owner-identity-loader-seal-refresh.md`
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

## Scope / terminal

- 只改`contract.py`中两个frozen seal常量、`test_d0_contract_views.py`中对应expected与D017 tests/mutations，并写step-158。owner/schemas/channel/session/P05只读。
- 不重构loader、不改D0Contract/load_contract/public signatures、不补schema compiler。
- 目标8分钟、10分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D017_OWNER_IDENTITY_LOADER_SEAL_REFRESH_READY_FOR_INDEPENDENT_VERIFICATION`；不等于I05完成。

## Frozen receipt / new seals

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
old_owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
old_identity_seal=29d1fc77bc3028861df04e3442de07ffabc0d72a68a2e4666f3b318b98b48ec6
final_owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
final_identity_seal=68d21b4af54e43e34f23e882a3ebf0be8393d67487877471a787a8e2b3d4371f
scientific_projection=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
pre_contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
pre_tests=745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
decisions=b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8
verifications=beaa804651c37e0f2e33415bfc7cb2cf261f492f2121e9811696f34fa87dbfe8
R001=1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37
topic_index=bb95bb1c3497abd306d76b35018245c4eac7bcd5be7c5b6226a20a26a8b6c51a
master_state=92e800b48986b5de6d42977ed3fa9a506cb1d2d727746c6de0971e42f02ca178
step157=bfab0aac3434a9aae22adb7b5e0d5e3963b2b5c534d3fb18ef85db7311057b78
```

## Strict RED then exact repair

1. 先只编辑tests：新增`test_owner_identity_d017_descriptors_and_hmm_reference_exact`，独立断言7 ordinary+1 HMM、32/41/49 descriptors、8 signatures、S4七项、HMM无LOGICAL binding且reference exact。
2. 运行该节点加现有exact frozen/grid/runtime三个节点；生产源码仍旧seal时必须4/4 FAIL、exit非零，并先写RED receipt。
3. 仅替换production/test中的old owner seal→final owner seal、old identity diagnostic seal→final identity seal。scientific/grid roots与任何其他production line不得改变。
4. 扩充现有owner mutation matrix至少12项D017 mutations：ordinary kind/phase/op/source/atom/order、method/split/B2 swap、S4、HMM reference；总数至少28，全部fail closed。
5. exact四节点GREEN；全部`test_d0_contract_views.py`与显式四文件回归GREEN，0 fail/error/skip/xfail/warning。
6. 静态证明production diff除两个constant values外无变化；D0Contract仍四字段、channel只接D0Contract、import无I/O。
7. owner/session/schema/step157/P05/cache/HEAD/staging/diff-check保护。

## Environment / return

Windows Python3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、`-B -m pytest -p no:cacheprovider`。step158记录RED/GREEN/全量counts、mutations、stdout SHA、source/test/log SHA、P0/P1/P2；只能返回PASS terminal、FAIL或INCOMPLETE。
