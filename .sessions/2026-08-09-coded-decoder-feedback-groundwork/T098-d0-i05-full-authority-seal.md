# Task Brief: D0 I05 FULL authority seal (positive raw oracle remains pending)

> 来源: T088 / step-134 preview P1-1 + P1-4 | 产出位置: `projects/thesis-fso/worker-logs/step-144-d0-i05-full-authority-seal.md`
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

## Scope / terminal ceiling

- 本切片只关闭 forged FULL authority：generic `RelationalManifest` 只能表示 `EXPLICIT_PARTIAL`；FULL 使用独立 opaque type与factory；validator从存储的冻结 authority inputs重新 canonical compile并逐字段比较，不信任 manifest 自报 digest/seal。
- 本切片不构造 FULL raw positive bundle，不关闭 step-134 P1-4；不实现 HMM float/member binding或 consumer-ledger binding。
- 即使全部 GREEN，terminal上限也只能是 `FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`，不得宣称 I05 READY。

## 假设 / 否决条件

- 假设：authority type split + canonical recompile可在schemas/test两文件内独立闭合，不依赖未冻结的 D014 identity细节。
- 否决条件：必须依赖 caller token/secret；validator仍只比较公开 digest；需改 owner/contract/其他模块；或15分钟不收敛。命中即 `INCOMPLETE`。

## 冻结输入

```text
schemas.py=a72bcf273a81db5fd7feba84c72455c2b6f1754e2a57669b87a6de969c064e61
test_schemas=35bc5d6682b17adeeef0a3aeb7de3bcb91946c5616d422178045f90ee3a0cd97
step-134=81e94ed47c2ac46c7bc9d8b1056f569d8edb5ca17f9661b9e3282d8d6ca6e04c
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
step-143=1470d822ee3570fdeb85fdba58360a7635c403985f1a3ebf72748cb72c181c1e
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
2. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
3. Create `projects/thesis-fso/worker-logs/step-144-d0-i05-full-authority-seal.md`

不得修改 contract/channel/codec/waveform/owner/governance/common/legacy；不得创建 raw bundle/artifact/result/cache；不得 install/commit/push/stage。

## Strict TDD

1. 完整读本任务、T088、step-134、current schemas/tests及 owner table/coverage/manifest段；核 frozen hashes、HEAD/staging/P05/cache。
2. production 前新增 exact nodes：
   - `test_full_manifest_factory_seal_rejects_forged_full`
   - `test_full_manifest_authority_recompiles_after_tamper`
   - `test_relational_manifest_is_partial_only`
   三节点必须在当前 production上真实 RED；立即先写 step-144 RED receipt（commands/failures/source+test SHA/output SHA），再改 production。
3. 类型/API：
   - `RelationalManifest` 构造后scope恒为 `EXPLICIT_PARTIAL`；任何 `FULL_D0_ARTIFACT` 参数、replace/object tamper经partial/full validator均拒绝。
   - 新增 frozen/slotted `FullManifestSpec`（或严格等价）持有 canonical recompilation所需全部 authority：exact owner contract/owner identity、literal S1 extent、typed HMM plan、typed computation plan及必要 version/schema identity。
   - 新增 frozen/slotted `FullRelationalManifest(init=False)`（或严格等价 opaque type）；公开 direct constructor失败。唯一正常入口仍为 `build_full_relational_manifest(...)`。
4. Authority不依赖 secret/token：
   - factory私有 canonical compiler从spec生成 cell domains、seed sets、10 table expectations、coverage/authority seal；FULL对象保存spec与编译产物。
   - `validate_relations`首先 exact-type检查，然后从manifest保存的spec重新运行同一 canonical compiler，逐字段比较spec-derived canonical FULL与manifest现值，再验证rows。caller重算公开 `full_coverage_sha256` 或改tables+digest不能产生authority。
   - `assert_frozen_d0_identity(owner_contract)`必须由factory和recompile path调用；schema/control/code/population/seed drift均拒绝。
   - 使用`object.__new__`、`object.__setattr__`、dataclasses.replace/字段替换的forgery，只要不等于canonical compiler完整输出就拒绝；若字节/语义完全等于canonical输出，则不是绕过。
5. 当前 HMM/computation plan仍只是authority input envelope；本切片不得声称其内部per-group/consumer binding已正确。设计需允许后续 typed plan additive closure后重编译，而不回退generic FULL。
6. Negative matrix≥30，至少含：generic FULL direct/replace/tamper、Full direct construct、scope/extent/owner/owner SHA/plan/plan field/table/projection/count/key SHA/multiplicity SHA/coverage/seal、FIRST↔MAX、drop/add/replace table，以及改表后重算公开coverage。保留合法 PARTIAL正例与factory创建的canonical FULL结构正例（只验证authority结构，不冒充raw validation正例）。
7. Fresh final bytes：三 exact；完整 schemas file；完整 contract views regression；aggregate当前 `test_d0_*.py`。0 fail/error/skip/xfail/warning。static/import审查、`git diff --check`、boundary/hash/P05/cache/HEAD/staging保护。
8. 日志明确 step-134 disposition：P1-1 authority CLOSED或OPEN；P1-4 raw positive保持OPEN；HMM/ledger两项保持OPEN。任何final delta未fresh rerun则 `INCOMPLETE`。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

≤15分钟；不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

RED/GREEN、negative matrix、authority receipts、三文件 SHA；terminal=`FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`、`INCOMPLETE` 或 blocker。
