# Task Brief: D0 owner canonical identity contract v1 — fresh retry

> 来源: T102/step-148 recovered evidence + R001 / D015 | 产出位置: `projects/thesis-fso/worker-logs/step-149-d0-owner-canonical-identity-contract-retry.md`
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

## Scope / terminal

- 从未改owner重新执行完整transfer；不得把step-148的root复算当prechange RED或owner PASS。
- 只写owner与step-149；不改session/source/tests/schemas，不跑pytest/benchmark/science/MVE。
- PASS上限`OWNER_IDENTITY_CONTRACT_READY_FOR_INDEPENDENT_VERIFICATION`；独立verifier PASS前不得实现schema bindings。
- 目标12分钟，15分钟硬停止；不能原子闭合则保持owner未改并返回INCOMPLETE。

## Frozen receipt

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
R001=679e437b052f5b664f2aae1a42f7268482612c396d9a613d6ea6c18e1d285a4d
D015 decisions=376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0
V009 verifications=16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f
step-148=c089a52190988b7695e6df66a153984ef1bf06f8ade98132a63145490eea31af
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
step-147=a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f
```

## Exact recovered grid payload（不得再猜）

Standalone payload exact shape：

```json
{"schema":"coded_decoder_feedback.d0.float64_grid.v1","name":"p_s","values":[{"index":0,"float64_hex":"0x0.0p+0"}]}
```

`values`实际必须分别内嵌全部122/6个升序literal；sigma `name="sigma_e2"`。Combined exact shape：

```json
{"schema":"coded_decoder_feedback.d0.hmm_grid_commitment.v1","p_s":<完整standalone p_s payload>,"sigma_e2":<完整standalone sigma_e2 payload>}
```

Canonical bytes为UTF-8、`sort_keys=true`、compact separators、`ensure_ascii=false`、`allow_nan=false`、无尾换行。三个root必须分别为：

```text
bfc3cef2c8e6fc800b6a40f9da778ab98b666ec57e5e12ae1f0c8b9f25b78864
0f37cdf467a04283bbf03792c5654545947ce759c052ed11e98c20c2618401ca
0cdb5e547e31997cd931a97f97f681ff5eeae28c372810eb12f593f4dca99fdf
```

历史原始证据与fresh复算见step-148和R001；owner内combined嵌套payload必须与两份standalone payload深等。

## Mandatory RED before edit

1. strict duplicate-key parse当前owner并保存prechange解析结构hash；核全部frozen hashes、HEAD/staging/P05/cache。
2. 在任何owner编辑前运行缺失`identity_binding_contract`与D015 required fields的断言，必须非零；把命令、output与output SHA先写step-149。
3. 若RED不红，停止；不得修改owner。

## Atomic owner transfer

在`statistical_contract_repair`之后、`strata`之前新增唯一top-level `identity_binding_contract`，header固定：

```yaml
schema_version: coded_decoder_feedback.d0.identity_binding.v1
decision_ref: D015
scientific_contract_change: none
```

完整无placeholder地冻结：

1. canonical serialization、typed atom `{type,value}` 与只允许`str/int/bool/none/float64_hex`；JSON float、alternate hex、negative zero、NaN/Inf拒绝。
2. 122项p_s与6项sigma literal authority、provenance、anchors、standalone/combined payload schema与三个roots；runtime禁止重算authority。
3. 所有domain-separated payload的完整version/field order：consumer PK、HMM member key、HMM computation binding、logical computation identity、computation-ID manifest、runtime aggregate content；lowercase SHA256(canonical bytes)。
4. HMM chunk/group envelope、clean=`seed`、target/sentinel=`seed→fixture legal order`、10/90/90、ordinal/multiplicity、unique exact set；outer envelope禁止跨grid/role/cell迁移。
5. ledger/accounting：263,520 chunks；22,800 per-pol trajectory full-grid logical rows；16,689,600 logical primitive；9,600 executed trajectory rows；7,027,200 materialized primitive；13,200 cache rows；无cost-bearing group ledger、无pair ledger；X charge=732/Y=0，每trajectory primitive=732，materialized仅EXECUTED。
6. direct cache：M2_N100 canonical executed owner；M3_N100直接读M2；sentinel先归一到same seed/cell/row-pol clean再做N归一；M3 sentinel直接指M2 clean；source必须EXECUTED、禁chain、保留logical ID；跨M仅content-identical waveform/BPS/HMM，B2 decode禁跨M。
7. consumer `(table, exact typed PK)→logical ID` projections：S2 off省fixture并nine-to-one→B04；S2 on保留fixture/method；S3保留split/seed/cell/target/fixture/candidate；BPS省pol；B2 clean省pol；B2 controlled省row-pol；HMM chunk→manifest；S4 standalone；forward+reverse/no orphan-extra/same-phase swap拒绝/source-content相等。
8. runtime content root绑定computation manifest、ordered resolved content hashes、exact numerator/denominator power、member count；preexecution root禁止runtime content，普通order-dependent float sum禁止。
9. 至少八类可复算golden：三个grid/anchors、clean10、target90、sentinel90→clean、M3_N100→M2 direct、S2 off nine-to-one、BPS dual-pol shared；每个含足够输入与canonical JSON SHA，不能只有opaque hash。
10. validator obligations覆盖literal/root/field order/type/domain/version/counts/direct source/content/logical/materialized/reverse；拒绝等量member替换、group/hex/source交换、cache chain、logical ID吞并及public digest重算。

## Fresh author verification

- strict YAML duplicate-key parse；required assertions≥80。
- 独立重算122+6 literals、三个root、全部goldens与六个count formulas；mismatch=0。
- 删除新block后与prechange解析结构deep-equal、结构hash相同；`scientific_field_drift=none`。
- source/tests/schemas/R001/D015/step-148/HEAD/staging/P05/cache保护；`git diff --check=0`。
- step-149保存RED、postchange PASS、assertion/golden/count/drift数字及最终owner/log SHA；缺任何fresh证据则INCOMPLETE。

## Environment / forbidden

Windows Python 3.11；`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`。不得install/commit/push/stage，不得修改四个P05 log或既有cache。

## Return

terminal、RED receipt、assertions/mismatches/goldens/counts/drift/protection、owner与step-149 SHA、exact written paths。
