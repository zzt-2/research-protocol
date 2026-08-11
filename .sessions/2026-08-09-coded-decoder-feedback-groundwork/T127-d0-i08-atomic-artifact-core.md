# Task Brief: D0 I08 — canonical JSONL and atomic artifact core

> 来源: d0-implementation-plan I08 / AC01–AC06 / T125 | 产出位置: `projects/thesis-fso/worker-logs/step-173-d0-i08-atomic-artifact-core.md`
> 日期: 2026-08-11

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

- 仅新建 `projects/simulation/explore/coded-decoder-feedback/artifacts.py`、`projects/simulation/tests/test_d0_artifacts_cost_s4.py`、step-173。其他只读；import不得mkdir。
- 15分钟硬停；禁止写真实project artifacts/results/cache，禁止benchmark/science/MVE/install/stage/commit/push。
- 先写 AC01真实RED；新模块首次 `ModuleNotFoundError`是允许bootstrap RED。随后一次最小实现闭合AC01–06。
- PASS=`D0_I08_ATOMIC_ARTIFACT_CORE_GREEN`；随后与I07合并做一次独立batch verifier，不单开readiness review。

## AC01–AC06 exact acceptance

1. 七个 dev 文件精确有序：`dev_manifest.json`,`raw_bps_dev.jsonl`,`hmm_grid_dev_chunks.jsonl`,`raw_b2_tuple_clean_dev.jsonl`,`raw_b2_tuple_controlled_dev.jsonl`,`dev_freeze.json`,`dev_freeze_receipt.json`。
2. canonical JSON：UTF-8、sorted keys、compact separators、`ensure_ascii=False`,`allow_nan=False`；JSONL每record canonical bytes + exact LF，末行也有LF。拒绝NaN/Inf、非str dict key、bytes/Path/opaque/cycle；sort key重复/非法拒绝；输入乱序仍同bytes/hash。
3. 所有 row/PK/FK/cardinality/finite/manifest validation 和完整materialize/encode/hash必须发生在mkdir/mkstemp/open之前。validator失败时0 FS write，旧target exact bytes不变。
4. 单文件协议：same-dir temp → write → flush → file fsync → close → `os.replace` → dir fsync；任一 pre-replace failure清temp且旧target不变。dir fsync unsupported必须明确receipt状态，不得伪称成功。
5. receipt hash只取实际落地 exact bytes，不信 caller hash；绑定owner/contract/source/code/manifest/raw/chunk/freeze/selection/seed/summary/ledger logical names和byte_count/record_count。
6. bundle data先落并复核，receipt最后。中断时不能产生partial PASS；无receipt、漏/多/改单byte、wrong logical name、假SHA、receipt先落全部 fail closed。若root已有完整bundle，注入失败后旧完整bundle仍须可读；不得以“torn被识别”偷换“旧完整保留”，可用最小immutable generation+atomic pointer/receipt或等价可证机制。
7. generic writer要能承载D020 sidecars：`decoder_hard_outputs.jsonl`按lowercase hard-root排，`ordinary_consumer_provenance.jsonl`按logical computation id排；它们不替代七个dev文件。I05 validator/API直接复用，MappingProxy显式转plain JSON tree。
8. 最小 public API可包含 frozen/slotted `ArtifactReceipt`,`BundleReceipt`，`canonical_json_bytes`,`canonical_jsonl_bytes`,`write_jsonl_atomic`,`write_bundle_atomic`,`validate_complete_bundle`；不复制I05 schema，不提前实现I11 cost/S4逻辑。
9. fresh failure/negative至少18项，wrong accept/reject=0/0；用fake FS/spies证明调用顺序、0-write validation、temp cleanup、failure preservation、receipt-last。

## Commands / receipt

- RED：`...python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_artifacts_cost_s4.py::test_seven_dev_artifacts_named`
- GREEN：整份新测试文件 AC01–06；另跑I02/I05受影响窄节点（owner frozen view、raw strict、PK/FK、S4），总计应为秒级，不跑FULL。
- 固定 `PYTHONDONTWRITEBYTECODE=1`,`PYTHONHASHSEED=0`。step-173记录RED/GREEN、test totals/time/stdout SHA、negative counts、atomic event trace、file hashes、HEAD/staging/P05保护、P0/P1/P2。
