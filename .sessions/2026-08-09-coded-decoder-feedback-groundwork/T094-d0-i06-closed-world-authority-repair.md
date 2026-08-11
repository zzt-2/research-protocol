# Task Brief: D0 I06 closed-world receipt and derived-authority repair

> 来源: T093 / step-139 `FAIL 0/4/0` / D012 / D013 | 产出位置: `projects/thesis-fso/worker-logs/step-140-d0-i06-closed-world-authority-repair.md`
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

## Review disposition / frozen repair design

- 接受 step-139 四项 P1，不弱化、不解释为“Python 无法防御”。公开对象经 owner-required mutation 后仍给出伪权威值即 fail-open。
- evaluated correctness 不再作为 stored authority：wrapper 不得拥有可写 correctness slot/field；公开只读 property（或严格等价机制）每次由其冻结 pending truth 与 decoded bits重算，`object.__setattr__(obj, "final_codeword_correctness", ...)` 必须失败。
- Receiver receipt/b2 tree 改为 closed-world exact-type policy：仅明确允许的 immutable built-in tree 与 detached ndarray/NumPy scalar归一化；所有其他类型 fail closed。不得继续“已知坏类型 denylist”。
- Receiver-side physical-noise key采用 safe-schema + semantic-family gate；只有明确的 receiver-derived C_pre keys可出现。TruthView 的物理 noise receipt不受此 Receiver 禁令误伤。
- root seed 在任何 `int()` 归一化前必须 `type(value) is int`；`np.int64`/`np.bool_`/bool均拒绝。
- 不扩到 I05/methods/runner/artifact/benchmark/science。

## 假设 / 否决条件

- 假设：四项 P1 可在现有 I06 四文件内以移除 stored authority、closed-world树和 exact scalar gate 闭合。
- 否决条件：仍需保存可覆写 correctness 副本；Receiver 必须接受开放世界对象；需修改 codec/waveform/schemas/owner/common/legacy；或15分钟内未取得 final-bytes fresh evidence。命中即 `INCOMPLETE`。

## 冻结输入

```text
contract.py=1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240
channel.py=ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd
test_contract=9ff8edd59fc0f76ad268b37eb3c0182eb9089e6516d0bd8538c8fe31a9358206
test_waveform_channel=02bab0fc430853ccdb1c565995763bbfc25d5133438535a010be0f41fb88c296
step-138=d94965345384387dfee88ebd0be23f750ca9f8e3ef88d70763aab744e20b3104
step-139=959fe9bffaa795633fcd4e0f9a72d08025f5573d67d631158e6128baa6a937b0
D013 decisions=63242551efd01a8b53989952a949cd742f2728ff4cb348f3955431b73f77effc
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/channel.py`
3. Modify `projects/simulation/tests/test_d0_contract_views.py`
4. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
5. Create `projects/thesis-fso/worker-logs/step-140-d0-i06-closed-world-authority-repair.md`

不得修改 codec/waveform/schemas/owner/common/legacy/governance；不得 install/commit/push/stage。

## Strict TDD

1. 完整读本任务、D012/D013、step-139/138 与 current source/tests；核 frozen hashes、HEAD/staging/P05/cache。
2. production 前新增 exact nodes：
   - `test_i06_evaluated_correctness_is_derived_not_stored`
   - `test_i06_receipt_closed_world_rejects_opaque_builtins`
   - `test_i06_receiver_noise_alias_family_fails_closed`
   - `test_i06_root_seed_requires_exact_builtin_int`
   四节点在当前 production 上必须真实 RED；立即先写 step-140 RED receipt（command/failure/source+test SHA/output SHA），再改 production。
3. Correctness authority：
   - `EvaluatedTruthView` 不再声明/存储 `final_codeword_correctness` dataclass field、slot、cache或caller参数；property每次从 pending truth information bits 与 canonical validated decoded bits逐CW计算新 read-only `(2,16)` bool。
   - `object.__setattr__(evaluated, "final_codeword_correctness", forged)`、普通 setattr、dataclasses.replace correctness、constructor correctness全部失败；property结果 mutation不能影响下次读取。
   - decoded bits仍 exact `(2,16,1024)` binary、defensive read-only；pending truth仍无 correctness init入口；repeat finalize拒绝；旧 payload/chronology gate不弱化。
4. Closed-world Receiver tree：
   - 输入只接受 exact `None/bool/int/float/complex/str/bytes`（仅实际需要者）、exact `dict/list/tuple/set/frozenset`，以及明确支持的 ndarray/NumPy scalar；容器递归转换为 detached immutable tree，cycle拒绝，mapping key规则显式。
   - `bytearray`、`memoryview`、`range`、bare `object`、arbitrary Mapping/Sequence/Set subclasses、dataclass、generic slots/dict、generator/iterator全部拒绝；不把其引用或 buffer view保留在 Receiver。
   - ndarray复制并 write-protect；NumPy scalar先 `.item()` 再进入 exact allowlist。必要 CodeLayout/WaveformLayout仍 exact-type explicit allowlist，subclass拒绝。
5. Receiver noise semantics：
   - 对 Receiver `receipts`/`b2_parameters` 的所有 mapping keys做稳定 token normalization（camelCase、大小写、连字符、下划线、数字边界）；physical/noise/AWGN/N0/SNR/variance/sample等 truth语义族一律拒绝，除 exact safe keys `receiver_noise_estimator_id` 与 `receiver_noise_estimate_per_pol`，后两者仍由 Receiver内部覆盖生成。
   - 至少覆盖 `noise_samples`、`awgn_samples`、`physical_awgn_samples`、`n0` 及 camel/case/separator variants；同时证明合法 receiver-derived keys与无关 plain metadata可通过。
   - channel 不得传 physical noise/SNR truth到 Receiver；TruthView `noise_receipt`仍保存完整物理 truth且形状/finite检查不回归。
6. Root/cell scalar：`spawn_named_streams` 与 `build_views` root entry均在归一化前只接受 exact Python `int` 且 `0..2**63-1`；拒绝 bool、NumPy integer/bool、float、string、oversize。PhysicalCell现有 exact bounds不弱化。
7. 重放 step-139 10 个错误接受，要求 10/10 reject；fresh mutation总数≥40，四类各≥8并含合法 controls。不得只调用 production helper作为 oracle或只做 repr substring。
8. Fresh final-bytes tests：四 exact；完整 contract+waveform；codec 7；schemas current；aggregate全部 `test_d0_*.py`。0 fail/error/skip/xfail/warning。四组 per-pol C_pre与 payload chain复算；static/import audit、`git diff --check`、boundary/hash/P05/cache/HEAD/staging保护。
9. findings-first 日志逐项 disposition step-139 P1-1..4；若 final delta未 fresh rerun，终态必须 `INCOMPLETE`。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

≤15分钟；不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

RED/GREEN、step-139 10/10 closure、fresh mutation matrix、C_pre/payload receipts、五 SHA；terminal=`I06_READY_FOR_INDEPENDENT_REVERIFICATION`、`INCOMPLETE` 或 blocker。
