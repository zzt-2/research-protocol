# Task Brief: D0 owner binding-kind repair — independent reverification

> 来源: D016 / V010 / T106 step-152 | 产出位置: `projects/thesis-fso/worker-logs/step-153-d0-owner-binding-kind-independent-reverification.md`
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

## Independence / scope / terminal

- 独立验收T106最终owner字节；禁止用step-152 PASS作为断言、禁止导入schemas/author helper。
- 只写step-153；owner/source/tests/session只读，不跑pytest/benchmark/science/MVE。
- 允许复用并修订verifier自己在step-151保存的独立源码，但必须从step-153 fence经stdin fresh执行，不得创建临时脚本。
- PASS=`OWNER_IDENTITY_CONTRACT_INDEPENDENTLY_VERIFIED`，上限仅D015 owner transfer；不等于I05完成或科学授权。
- 目标8分钟、10分钟硬停止；任一必跑项未执行即INCOMPLETE。

## Frozen bytes

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
pre_repair_owner=9f12cd11d210aef10c08848ccf42f39183f1ebf5f061d7203d3879335278990d
final_owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
step151=c1b0f39ed0903735387d6d12aaf5963c6a400215da81fa649a4f0e9b9459e535
step152=d5432176e10190d0ad11f1dda177d11113bdd159e289b19795451522e91d242c
R001=ff229de3305c179521474ea37e37a748ed2189d824d75e6779708ac89f3992dd
decisions=ca4b7098e8b9ab77575b58ea2abed07e6e356566e38c0ed8901eb0cfabe0d6e7
verifications=7f76040ffe3e9ca0d21abda03f72b8bcdd3ba3e5cc14d950051a892e55485bcb
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
```

## Fresh single-process matrix

源码先用`apply_patch`保存到step-153的`<!-- verifier:start -->` fenced Python block；PowerShell只从文件提取并经stdin送`python.exe -B -`。记录完整stdout、exit code、stdout SHA与最终log SHA。

1. Strict duplicate YAML；指定2 anchors+2 aliases且无额外/chain；exact identity block placement/header/13 sections。
2. 128/128 literal逐项、3/3 roots、payload schemas/field orders/typed atoms/placeholders。
3. 11/11 authority exact：global schema + 8 projections的`exact_binding_kind`与2 golden inputs的`binding_kind`均唯一为`LOGICAL_COMPUTATION_ID`；递归census无其他authority值。
4. S2/BPS manifest builders必须从owner保存inputs读取`binding_kind`，禁止verifier硬编码；logical IDs与roots分别命中原值。
5. owner全部10个golden subcases、>=15 fresh mutations、6/6 counts；consumer/cache/ledger/runtime obligations。
6. raw删除新增11行还原`9f12cd11...`；parsed删除11 fields还原T106保存的prechange structure；identity block整体删除仍还原旧owner `c61c88e...`；science/permission/count/grid root drift none。
7. begin/end owner、HEAD/staging、全部frozen hashes、P05四值、cache `202/41/4`、diff-check=0。

要求assertions>=700、goldens=10/10、mutations>=15/15、counts=6/6、mismatch=0、P0/P1/P2=0/0/0；否则FAIL/INCOMPLETE，不得抽样PASS。

## Environment / return

Windows Python 3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；不得install/commit/push/stage。返回terminal、全量数字、owner/step153 SHA、exact written path。
