# Task Brief: D0 owner canonical identity contract v1

> 来源: R001 / D015 / step-134 open bindings | 产出位置: `projects/thesis-fso/worker-logs/step-148-d0-owner-canonical-identity-contract.md`
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

## Scope / authority / terminal

- 只把D015完整转入唯一owner YAML；不改schemas/tests，不运行任何D0/science/benchmark。
- 新block是additive implementation identity closure，`scientific_contract_change: none`；原population/seed/grid数学值/gate/estimand/exposure totals必须deep-equal无漂移。
- PASS上限`OWNER_IDENTITY_CONTRACT_READY_FOR_INDEPENDENT_VERIFICATION`；verifier PASS前不得实施schema bindings。

## 冻结输入

```text
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
R001=8ad172ff3e3d51531f04d0798d118a47d0dea5771ace124ddb30927e61762be1
D015 decisions=376c3e740a6e4987734bcb64ebf96ffe417d5566ce4342a01e2f20ca2f5674b0
V009 verifications=16957db808e656f5c13bb982aa3c4477846f6264af2668abbe6ad85207d6d56f
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
step-147=a08213733ba451cca0e66da4a5582b455aed071b296abb448d05dd760821041f
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
2. Create `projects/thesis-fso/worker-logs/step-148-d0-owner-canonical-identity-contract.md`

不得修改session/governance/source/tests/其他owner；不得 install/commit/push/stage。

## Prechange receipt

1. 完整读T102、R001、D015、owner现有serialization/ledger/exposure/BPS/HMM/dev_manifest段；核frozen hashes/保护。
2. 编辑owner前运行strict duplicate-key YAML parse + assertions，证明top-level `identity_binding_contract`缺失且D015 required fields不可执行；命令应因缺失而exit非零。先把owner SHA、assertions/output SHA写入step-148，再编辑owner。

## Owner block requirements

在`statistical_contract_repair`之后、`strata`之前新增唯一top-level：

```text
identity_binding_contract:
  schema_version: coded_decoder_feedback.d0.identity_binding.v1
  decision_ref: D015
  scientific_contract_change: none
```

完整定义必须包含：

1. Canonical serialization：UTF-8、sort keys、compact separators、ensure_ascii false、allow_nan false、无尾换行；JSON float禁止。Typed atom exact schema固定为`{type,value}`，只允许`str/int/bool/none/float64_hex`，int为exact Python/int64语义，float只用canonical hex。
2. Grid authority：
   - 生成provenance固定NumPy 2.4.3 float64 `[0.0]+logspace(-7,-1,121)`，但runtime禁止重算，authority为owner内完整122个`{index,float64_hex}` literals。
   - 完整6个sigma literals；canonical/strict-increasing/no-negative-zero/no-duplicate规则。
   - commitment payload schemas与三个roots exact：`bfc3cef...78864`、`0f37cdf...01ca`、`0cdb5e...9fdf`；含R001四个p_s anchors。
3. Domain-separated payload schemas及完整field order：consumer primary key、HMM member keys、HMM computation bindings、logical computation identity、computation-ID manifest、runtime aggregate content。每个schema使用完整version string；hash为lowercase SHA256 of canonical bytes。
4. HMM authority：chunk PK/group envelope含tuple、p/sigma index+hex、role、cell、pol、chunk ID/pilot count；member order clean=`seed`，target/sentinel=`seed→fixture legal order`；counts 10/90/90；member manifest保留ordinal/multiplicity并另验unique exact set。
5. Ledger granularity/accounting：22,800条per-pol trajectory full-732-grid logical computations；chunk是aggregate receipt、无额外cost-bearing group row、无pair-level ledger。逐项冻结263,520/22,800/16,689,600/9,600/7,027,200/13,200计数公式；X为dual-pol pair charge owner(732)，Y=0；每logical trajectory primitive=732，materialized只汇总EXECUTED。
6. Cache/source：M2_N100是N100 canonical executed owner；M3_N100 direct CACHE_READ→M2；sentinel先到same seed/cell/row-pol clean physical content再做N normalization；M3 sentinel direct→M2 clean；source必须EXECUTED、禁止chain；logical ID保留；复用仅限content-identical waveform/BPS/HMM，B2 decode禁止跨M。
7. Consumer bindings：按R001逐表冻结exact PK projection与保留/省略字段；S2 off九行→B04 canonical owner；HMM chunk PK→computation manifest root；S4 standalone。要求forward+reverse coverage、no orphan/extra、same-phase交换拒绝、source/content相等。
8. Runtime content：preexecution identity root不含执行后content；runtime content root绑定computation manifest、ordered resolved content hashes、exact numerator/denominator power、member count；普通order-dependent float sum禁止。
9. Golden vectors：至少包含并在author-side独立脚本重算：三个grid roots与anchors；一个clean10 chunk/member/computation manifest；一个target90；一个sentinel90→clean source；一个M3_N100→M2 direct source；S2 off nine-to-one；BPS dual-pol shared；所有golden必须保存canonical JSON SHA与足够输入，不能只写opaque hash。
10. Validator obligations：完整literal/root/field order/type/domain/version、counts、direct source/content、logical/materialized/reverse coverage；任何等量member替换、group/hex/source交换、cache chain、logical ID吞并或public digest重算均拒绝。

若任何payload字段/ordering/source无法唯一冻结，停止并返回`INCOMPLETE_OWNER_IDENTITY_AMBIGUITY`，不得留placeholder/TODO。

## Fresh static verification

1. Strict duplicate-key parse；required assertions≥80。
2. 独立重算122+6 literals、三个grid roots、全部goldens与六个count formulas；mismatch=0。
3. Deep-copy before/after projection：删除新block后，owner原有全部解析内容必须与prechange结构hash一致；`scientific_field_drift=none`。
4. 核source/tests/schemas/R001/D015未变，HEAD/staging/P05/cache保护，`git diff --check=0`。
5. 日志记录prechange RED、postchange PASS、owner SHA、goldens、assertions、drift/protection；无final fresh证据则INCOMPLETE。

## 固定环境与禁令

使用Windows Python 3.11、`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`；目标12分钟、15分钟硬停止。不运行pytest/benchmark/science/MVE/web。

## 返回

terminal=`OWNER_IDENTITY_CONTRACT_READY_FOR_INDEPENDENT_VERIFICATION`、`INCOMPLETE`或blocker；附RED/static/golden/drift/protection与owner/step-148 SHA。
