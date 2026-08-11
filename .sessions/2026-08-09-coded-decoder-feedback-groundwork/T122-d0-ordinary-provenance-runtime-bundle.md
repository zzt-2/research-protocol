# Task Brief: D0 ordinary provenance runtime bundle

> 来源: D020–D022 / T121 / I05 closure map | 产出位置: `projects/thesis-fso/worker-logs/step-168-d0-ordinary-provenance-runtime-bundle.md`
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

- 实际代码片B。只改`schemas.py`、`test_d0_ordinary_identity.py`、`test_d0_schemas_statistics.py`与step-168；codec/owner/contract/session/其他tests/P05/cache只读。
- 12分钟目标、15分钟硬停；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_ORDINARY_PROVENANCE_RUNTIME_BUNDLE_READY_FOR_BATCH_VERIFICATION`；独立验收在I05三片后的唯一batch verifier。

## Frozen input

```text
schemas=80e69a63ded7f7385c6aef8c4806ec53bc51bdcc2f86743e1cdc124a49dcb1cc
codec=5c45cf1765a3a9f295105da7fba284d4509de053c414739a2e4a86232b9f4331
codec_tests=28401d747ff13143ca828753cf910aac88974f52e0d672edc96d2916767a6d6e
step167=cac69b021dd06cbaee7ab353b94b4170b4fab17bf0405095e49439cf97296810
```

## Required implementation

1. TDD RED first：新增focused tests，至少因7类consumer output、provenance record/bundle API缺失而真实失败；禁止用import/syntax错误冒充RED。
2. 在`schemas.py`新增最小frozen typed variants：S2-off、S2-on、S3、BPS、B2-clean、B2-controlled、S4。所有non-S4 variant必须持有T121已签发`DecoderHardOutputRef`，序列化时才取root，public API不接受caller hash；S3/BPS float64 hex、rotation、S4计数/evidence exact fail closed。
3. 新增typed provenance entry/payload/store record与aggregate-ledger binding，以及`build_ordinary_runtime_bundle(...)`/`assert_ordinary_runtime_bundle(...)`（命名可等价但职责不可少）。输入必须是已认证`OrdinaryIdentityPlan`、final owner authority与exact `outputs_by_pk`；重新认证plan/owner，禁止caller提供status/source/root/count。
4. 由plan canonical推导group/order/source：S2-off 9项B04 owner；S2-on/S3/S4 singleton；BPS X/Y且M3_N100 direct cache到M2_N100同pol；B2-clean X/Y exec；B2-controlled TARGET→SENTINEL，sentinel direct cache到matching clean row-pol。source必须命中EXECUTED leaf、两字段exact、output canonical deep equal、禁止chain。
5. Full ordinary exact totals必须由实际图枚举得到：records/aggregate=`27487`、entries=`42967`、EXECUTED=`30247`、CACHE_READ=`12720`、edges=`480+1440+10800`、groups=`12427 singleton +60 nine +15000 two`、aggregate=`26767 EXECUTED +720 CACHE_READ`；不得以只检查硬编码总数代替逐entry生成。
6. Bundle生成canonical provenance payload/store root；aggregate `content_sha256`等于payload root。抽取全部non-S4 hard roots并调用T121 store validator做exact forward/reverse、无orphan；hard store cardinality仅为distinct referenced roots。
7. 8个owner provenance goldens须由production builder命中（S2-off/on、S3、BPS M2/M3、B2 clean/controlled、S4）。全量positive测试可共享zero/first-bit refs，但golden指定项须用owner inputs精确复现。
8. 至少18 fresh negative/mutation：missing/extra output PK、arbitrary root/string、wrong variant/field/float/rotation/S4、entry order/ordinal、status/source direction/PK/chain/leaf/output mismatch、count/root reseal、hard-store orphan/missing、partial masquerade。wrong accept/reject=0/0。

## Test/protection gate

- GREEN只跑`test_d0_ordinary_identity.py`与`test_d0_schemas_statistics.py`的新增focused nodes及这两整文件；不跑五文件回归（留给final batch）。
- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python3.11 `-B -p no:cacheprovider`；0 fail/error/skip/xfail/warning。
- step-168记录RED/GREEN命令、counts/goldens/mutations、elapsed/stdout SHA、file hashes与HEAD/staging/P05/cache保护。
- 若15分钟内完整全量bundle来不及，优先交付可运行的7 variant + golden/group builder并诚实INCOMPLETE；禁止写第二套owner或缩减counts。
