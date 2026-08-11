# Task Brief: D0 owner identity typed loader — independent verification

> 来源: T108 / step-154 / D015 / V011 / V007 | 产出位置: `projects/thesis-fso/worker-logs/step-155-d0-owner-identity-loader-independent-verification.md`
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

## Independence / scope / terminal

- 独立审查 T108 final bytes；不得把 step-154 的 PASS、作者 mutation helper 或作者 expected 派生当结论。
- 只写 step-155；source/tests/owner/session 只读。禁止 install/commit/push/stage/benchmark/science/MVE。
- 目标 12 分钟，15 分钟硬停止。任一必跑项未执行即 `INCOMPLETE`。
- PASS terminal=`OWNER_IDENTITY_TYPED_LOADER_INDEPENDENTLY_VERIFIED`；上限只接收 loader，并 fresh 重封 I06 additive regression，不等于 I05 bindings 完成。

## Frozen final bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
contract_tests=745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6
step154=0a33ec8011faf929a56956cc6d13b6e9f77f02fc6281f2bd81a923c08a850a7a
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
R001=ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd
decisions=ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7
verifications=848ea9e3e97e6937ceb1dbcecf98350b09cfea135447d35f4815a607dfd785ea
step153=39ded7d15e32bd43e625782b143406e45e8390ef451279d1c05ed239491b8443
```

## Mandatory fresh review

1. Static diff：`D0Contract` 仍 exact 四字段；`load_contract` signature/return与既有解析行为不变；new loader/wrapper只 additive；schema/channel/runtime不引用或触发 new loader；import 无 I/O；通用 `_deep_freeze` string-key规则未放宽。
2. Public boundary：exact `IdentityBindingContract`、`D0OwnerIdentityAuthority`、`load_owner_identity_authority` 与 public revalidation；direct forged/dataclasses.replace wrapper、hash string spoof、nested replacement均 fail closed。
3. 独立 canonical oracle：不用 production canonical/hash helper，从 exposed view复算 122+6 literals、连续index/canonical positive finite hex、两 standalone+combined roots，命中 D015 三值；两处 integer-key anchors 已 typed tuple 化且 exact 4 anchors。
4. Closed-world structure：13 identity sections exact；header exact；无 JSON float；owner/identity/scientific projection seals exact；两个 fresh loads不共享 nonprimitive mutable state；外部写入/assignment拒绝。
5. Fresh mutations至少20项，且不得只依赖作者16项：duplicate key、omitted/extra/top-level order/type、anchor index/hex、literal bool index/negative zero/noncanonical/duplicate/order/count/root、combined deep drift、payload order、binding kind、ledger counts、cache source、forged wrapper/replacement。每项调用 public boundary并按独立预标 expected，错误接受=0、错误拒绝=0。
6. Fresh pytest：四个 T108 exact nodes；随后显式四文件 `test_d0_contract_views.py test_d0_receiver_codec_methods.py test_d0_schemas_statistics.py test_d0_waveform_channel.py` 全量，0 fail/error/skip/xfail/warning。Windows 不得把 glob 当字面量。
7. I06 source reseal：静态证明 `channel.py` 仍只接 `D0Contract`；抽查既有 closed-world owner/truth/receipt合法与非法cases，至少24 cases、mismatch=0；无需重跑 scientific waveform或任何 benchmark。
8. begin/end SHA、HEAD/staging、owner/session/schema/test/step153、P05四值、cache census、`git diff --check`；tracked pycache不得新增漂移。

## Environment / return

`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11 `-B -m pytest -p no:cacheprovider`。step-155记录命令、完整输出/摘要、stdout SHA、assertion/mutation/test/case counts、P0/P1/P2与最终log SHA。只能返回 PASS terminal、`FAIL` 或 `INCOMPLETE`。
