# Task Brief: D0 ordinary runtime-content owner transfer

> 来源: D020 / V016 / output-provenance review | 产出位置: `projects/thesis-fso/worker-logs/step-164-d0-ordinary-runtime-content-owner-transfer.md`
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

- 只改owner `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`与step-164。code/tests/session/P05只读。
- 只能改现有`identity_binding_contract`块内部；13个identity顶层key及顺序不变。删除该块后的scientific projection必须byte-exact命中`c61c88e...`；domain projection/seal `15c88476...`不变。
- 目标12分钟、15分钟硬停止；禁止install/commit/push/stage/pytest/benchmark/science/MVE。
- PASS=`D0_ORDINARY_RUNTIME_CONTENT_OWNER_READY_FOR_INDEPENDENT_VERIFICATION`；不等于loader/schema/FULL完成。

## Frozen pre-state

```text
owner=02d471a200a1dce17f2c43dd36ca90b050ebdc943c7c045483e816a07162d140
scientific_projection=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
identity_seal=68d21b4af54e43e34f23e882a3ebf0be8393d67487877471a787a8e2b3d4371f
ordinary_domain_seal=15c88476676b727ba338d4cb5acc196dce336f3856818c1557bcfb729b6d0c69
contract=cb16867116324bcacb373869649322958749ec56888e1fea1f8bb0b35e58853a
schemas=1d782ea4fdf187ad8c57646a65bd025de0b8a3c588c03f5e939d94063ac79a20
step163=1e0c25214e4fb2d69862dfb5da858492c788831430de01def21ec994779a31fa
```

## Strict RED then owner patch

1. 先以独立只读oracle对pre-owner运行缺口矩阵：hard-output/store/provenance/output variants/sidecars/write anchor/group-source rules/counts/goldens/obligations均缺失，至少32项真实RED、exit非零，先写receipt。
2. 只在identity block内补以下exact definitions：
   - hard-output payload：fields=`schema,cw_count,information_bits_per_cw,cw_order,bit_packing,decoded_information_bits_base64`；常量16/1024/`TRANSMITTED_CW_INDEX_0_THROUGH_15`/`CW_MAJOR_MSB_FIRST_RFC4648_BASE64`；16384 bits、2048 bytes、base64 length2732、exact one`=`、standard alphabet、no whitespace、round-trip。
   - hard-output store record=`schema,decoder_hard_output_sha256,payload`，root只hash payload；JSONL按root小写字典序，每record canonical JSON后exact LF（含末行）。
   - 7类consumer-output exact schemas/field order：S2/B2 hardroot；S3 hardroot+pilot/decoder float64 hex；BPS hardroot+rotation+NLL hex；S4含tested/failed/passed/evidence SHA。
   - provenance payload=`schema,logical_computation_id,entries`；entry=`ordinal,consumer_primary_key,consumer_output,cache_status,source_computation_id,source_consumer_primary_key`；store record=`schema,ordinary_consumer_provenance_manifest_sha256,payload`，root只hash payload；JSONL按logical ID小写字典序、canonical LF。
   - D020七类group/order/source/aggregate-ledger/write-anchor/FK/no-chain/leaf-equality/sidecar/receipt规则与全部静态counts。
3. 所有新增required files/hash fields只放identity `runtime_content`；base raw table/artifact contract不改。
4. 新增10个完整golden inputs+literal roots：zero hard output、first-bit hard output、S2-off 9→1、S2-on singleton、S3 singleton、BPS M2 source、BPS M3 cache、B2 clean、B2 controlled target+sentinel、S4 singleton。旧10 roots逐字节不变；不得只写生成规则。
5. validator obligations/mutations补全：hard bits/base64、store root/FK/orphan、output variant、entry order/ordinal、B04/BPS/B2 source方向与PK、status/source/chain/leaf、manifest reseal、sidecar/bundle/receipt、partial冒充FULL。

## Author gate / protection

- fresh owner-only oracle：13 keys/order、old 128 literals/3 grids/10 goldens/6 HMM counts、new payload shapes/counts/10 goldens全部PASS；至少30新mutations fail closed。
- begin/end code/tests/session/HEAD/staging/P05/cache不变；owner diff全部位于identity block，scientific+domain projections不变。
- step-164记录RED、canonical commands、全部root/count/mutation、new owner/identity SHA、log SHA与P0/P1/P2。只返回PASS/FAIL/INCOMPLETE。
