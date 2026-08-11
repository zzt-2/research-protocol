# Task Brief: D0 owner ordinary consumer identity completion（D017）

> 来源: D017 / V012 / compiler-readiness reviews | 产出位置: `projects/thesis-fso/worker-logs/step-156-d0-owner-ordinary-identity-completion.md`
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

## Scope / hypothesis / terminal

- 只改 final owner YAML 与 step-156；source/tests/schemas/session/P05只读。不跑pytest/benchmark/science/MVE。
- 假设：D017的identity-only additive completion可让七类ordinary consumer logical IDs与HMM manifest reference完全由owner生成，同时保持科学投影、grid/HMM/S2/BPS既有roots及全部账本总量不变。
- 否决条件：任一新literal无法由D017唯一给出、必须改变科学字段/既有root/ledger粒度、或15分钟内不能完成全量静态门；触发即`INCOMPLETE`，不得猜值或扩到schemas。
- PASS上限=`OWNER_ORDINARY_IDENTITY_COMPLETION_READY_FOR_INDEPENDENT_VERIFICATION`；不等于loader seal刷新或I05完成。
- 目标12分钟、15分钟硬停止；禁止install/commit/push/stage。

## Frozen receipt

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
branch=codex/rdl-method-production-v2
pre_owner=ca2c8146dec5edec62984cdadf678d808291cb6b2a736fd99059651fc7a50535
contract=0df83a86105a9ff5f8c76d2d937b7ac2a99f51f7d97783f7d3f4260c4d5bfc94
contract_tests=745ccbe5732816c8100ad9187a181d6acf6f2072269795e32e58487b66cce4f6
schemas=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
schema_tests=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
R001=1882c9d51a43a75efd3d56cb708edde2a1d88b06e850ba0dbe63821402095d37
decisions=b20e8ffc5c28a0335ccf5da3791e3e462bbfdd7e1ed49682cc986350497a5bc8
verifications=fb3173c6db7809d44f67d2c03619eb9ad3b3901b44cbd10bb9fea7daadaea67e
topic_index=1e8469aa2f10ad53f57d2d2819b6e58909648b8a74fb01ea022d8f96cf836ef6
step154=0a33ec8011faf929a56956cc6d13b6e9f77f02fc6281f2bd81a923c08a850a7a
step155=ce5edec6a9e8102bea6840abfff028bf8d36ca73d75e3dd9e6bab8078dfdfde9
```

P05四值与tracked pycache均须保持；staging为空。

## Mandatory pre-edit RED

先写step-156内独立 declarative checker 源码并从fence经stdin fresh执行；在owner编辑前必须以非零退出，且至少逐项报告：

- 七类ordinary projection缺失 exact typed `consumer_pk_fields/phase_rule/operation_rule/work_key_fields`；五类缺owner work-key kind。
- HMM仍错误带`exact_binding_kind=LOGICAL_COMPUTATION_ID`且缺manifest `reference`。
- S4缺exact七check IDs；validator obligations缺D017门。

RED output、exit code、stdout SHA必须先写step-156。RED不红即停止。

## Exact owner repair

### Common shape

`consumer_bindings.rule`改成exact mapping：

```yaml
rule:
  ordinary: each_raw_consumer_exact_typed_primary_key_maps_to_one_declared_logical_computation_id
  HMM_chunk: each_HMM_chunk_exact_typed_primary_key_maps_to_one_computation_ids_manifest_sha256
```

七类ordinary保留`exact_binding_kind: LOGICAL_COMPUTATION_ID`。每个`consumer_pk_fields`和`work_key_fields`都是有序list，每项exact key order=`[name, source, atom_type]`，source只允许`raw.<field>`或`literal.B04_K1`，atom只允许`str/int/bool`。已有`consumer_pk_order/work_key_order/omitted/preserved/cardinality/binding`不得删除，且须与typed descriptors一致。

### Seven ordinary identities

```yaml
S2_off:
  consumer_pk_fields:
    - {name: record_type, source: raw.record_type, atom_type: str}
    - {name: seed, source: raw.seed, atom_type: int}
    - {name: cell_id, source: raw.cell_id, atom_type: str}
    - {name: target_polarization, source: raw.target_polarization, atom_type: str}
    - {name: fixture_id, source: raw.fixture_id, atom_type: str}
    - {name: jump_present, source: raw.jump_present, atom_type: bool}
    - {name: method_id, source: raw.method_id, atom_type: str}
  phase_rule: {kind: literal, value: S2}
  operation_rule: {kind: literal, value: B1_DECODE}
  work_key_kind: S2_B1_OFF_CANONICAL_B04
  work_key_fields:
    - {name: seed, source: raw.seed, atom_type: int}
    - {name: cell_id, source: raw.cell_id, atom_type: str}
    - {name: target_polarization, source: raw.target_polarization, atom_type: str}
    - {name: jump_present, source: raw.jump_present, atom_type: bool}
    - {name: method_id, source: raw.method_id, atom_type: str}
    - {name: canonical_owner_fixture_id, source: literal.B04_K1, atom_type: str}
S2_on:
  consumer_pk_fields: same_7_typed_fields_as_S2_off
  phase_rule: {kind: literal, value: S2}
  operation_rule:
    kind: enum_map
    source: raw.method_id
    values:
      GLOBAL_FOUR_ROTATION_DECODER_SELECTION: B1_DECODE
      OFC17_16QAM_EXTFRAME_V1: B2_DECODE
      TRUTH_BOUNDARY_ROTATION_CORRECTION: O1_DECODE
  work_key_kind: S2_ON_METHOD_DECODE
  work_key_fields: [seed:int, cell_id:str, target_polarization:str, fixture_id:str, jump_present:bool, method_id:str]
S3:
  consumer_pk_fields: [record_type:str, seed:int, cell_id:str, target_polarization:str, fixture_id:str, candidate_id:str]
  phase_rule:
    kind: enum_map
    source: raw.record_type
    values: {S3_CANDIDATE_DEV: S3_DEV, S3_CANDIDATE_TEST: S3_TEST}
  operation_rule: {kind: literal, value: CANDIDATE_DECODE}
  work_key_kind: S3_CANDIDATE_DECODE
  work_key_fields: [record_type_as_split<-raw.record_type:str, seed:int, cell_id:str, target_polarization:str, fixture_id:str, candidate_id:str]
BPS:
  consumer_pk_fields: [record_type:str, tuple_id:str, B:int, Nw:int, seed:int, cell_id:str, polarization:str]
  phase_rule: {kind: literal, value: BPS_DEV}
  operation_rule: {kind: literal, value: B1_DECODE}
  work_key_kind: BPS_DUAL_POL_SHARED
  work_key_fields: [tuple_id:str, B:int, Nw:int, seed:int, cell_id:str]
B2_clean:
  consumer_pk_fields: [record_type:str, tuple_id:str, seed:int, cell_id:str, polarization:str]
  phase_rule: {kind: literal, value: B2_DEV}
  operation_rule: {kind: literal, value: B2_DECODE}
  work_key_kind: B2_CLEAN_DUAL_POL_SHARED
  work_key_fields: [tuple_id:str, seed:int, cell_id:str]
B2_controlled:
  consumer_pk_fields: [record_type:str, tuple_id:str, seed:int, cell_id:str, target_polarization:str, fixture_id:str, row_polarization:str]
  phase_rule: {kind: literal, value: B2_DEV}
  operation_rule: {kind: literal, value: B2_DECODE}
  work_key_kind: B2_CONTROLLED_DUAL_POL_SHARED
  work_key_fields: [tuple_id:str, seed:int, cell_id:str, target_polarization:str, fixture_id:str]
S4:
  consumer_pk_fields: [record_type:str, check_id:str]
  phase_rule: {kind: literal, value: S4}
  operation_rule: {kind: literal, value: OTHER_S4_CHECK}
  work_key_kind: S4_STANDALONE_CHECK
  work_key_fields: [check_id:str]
  exact_check_ids: exact_deep_copy_of_owner_serialization_enums_s4_check_id_in_same_order
```

上面方括号简写在实际YAML中一律展开为exact `{name,source,atom_type}` mapping；普通raw field的source=`raw.<same name>`，只有S3首项name/source不同。不得把简写字符串直接写入owner。

### HMM reference

删除仅`HMM_chunk.exact_binding_kind`这一项；global consumer-binding schema和七类ordinary值保持。HMM写：

```yaml
consumer_pk_fields: # 8 exact descriptors
  - {name: record_type, source: raw.record_type, atom_type: str}
  - {name: tuple_id, source: raw.tuple_id, atom_type: str}
  - {name: p_s_index, source: raw.p_s_index, atom_type: int}
  - {name: sigma_e2_index, source: raw.sigma_e2_index, atom_type: int}
  - {name: stratum_role, source: raw.stratum_role, atom_type: str}
  - {name: cell_id, source: raw.cell_id, atom_type: str}
  - {name: polarization, source: raw.polarization, atom_type: str}
  - {name: chunk_id, source: raw.chunk_id, atom_type: str}
reference:
  kind: COMPUTATION_IDS_MANIFEST_SHA256
  raw_field: computation_ids_manifest_sha256
  payload_schema: coded_decoder_feedback.d0.computation_id_manifest.v1
  rule: exact_typed_chunk_primary_key_equals_group_consumer_primary_key
  logical_member_authority: hmm_authority.logical_computation
```

### Owner self-check obligations

向`consumer_bindings.coverage`加入typed descriptor、ordinary/HMM分离与S4 exact-set要求；向`validator_obligations.required`加入3个对应requirement；向`reject_mutations`加入至少12类D017 mutation（binding kind、phase map、operation map、work kind、same-type source swap、atom drift、B04 literal、PK order、PK atom、S4 order/substitution、HMM reference kind/raw field/payload schema）。字符串可简明但必须唯一表达上述类别。

## Fresh author gate

- strict duplicate YAML；D017 exact shape/deep types/order；ordinary/HMM counts=`7/1`，work descriptors=`32`，consumer-PK descriptors=`41/49`，unique phase-operation signatures=`8`。
- 复算全部128 literals、3 grid roots、10既有goldens、6 accounting counts；S2/BPS logical IDs与roots必须原值，HMM clean/target/sentinel/M3 roots必须原值。
- 独立枚举owner descriptors确认ordinary bindings/logical IDs=`42,967/27,487`、HMM logical/chunk=`22,800/263,520`、ledger total=`50,287`；不生成science rows。
- 至少18 mutations全部fail closed，含D017 12类；错误接受/拒绝=0/0。
- identity block之外parsed tree deep equal；scientific raw projection SHA仍`c61c88e...`；permission/grid/count/science drift none。
- begin/end owner、全部Frozen receipt、P05、cache、HEAD/staging/diff-check；只写owner+step156。

## Environment / return

Windows Python3.11，`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；verifier源码先写step-156 fence再经stdin执行，避免Windows command length。返回terminal、RED、assertions/counts/goldens/mutations/drift、final owner与step156 SHA、P0/P1/P2。
