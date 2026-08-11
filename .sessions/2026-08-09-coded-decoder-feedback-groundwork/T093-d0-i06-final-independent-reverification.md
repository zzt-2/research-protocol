# Task Brief: D0 I06 final-bytes independent reverification

> 来源: T091 / T092 / step-137 FAIL / step-138 INCOMPLETE | 唯一产出: `projects/thesis-fso/worker-logs/step-139-d0-i06-final-independent-reverification.md`
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

## 身份与冻结输入

- 你是 non-author independent verifier：不得修改 production/tests/governance；不得复述作者旧 GREEN 代替 fresh final-bytes evidence。
- T092 作者因最后静态收紧未 fresh rerun而准确返回 `INCOMPLETE`；本任务从最终字节独立重验。

```text
contract.py=1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240
channel.py=ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd
test_contract=9ff8edd59fc0f76ad268b37eb3c0182eb9089e6516d0bd8538c8fe31a9358206
test_waveform_channel=02bab0fc430853ccdb1c565995763bbfc25d5133438535a010be0f41fb88c296
step-137=29918182abc1a21bf76830bb318ee8d2b05d1829a01a347663ba4ea2ea9d9409
step-138=d94965345384387dfee88ebd0be23f750ca9f8e3ef88d70763aab744e20b3104
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
D012=bde22e6ca455fd5986d0de14777abe2f3b44adfb604bf610a527cc71b75f51fb
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

只创建 `projects/thesis-fso/worker-logs/step-139-d0-i06-final-independent-reverification.md`。不得修改 source/tests/session/governance/其他日志。

## Fresh independent acceptance

1. 完整读 T091/T092、D012、step-137/138、owner truth/receiver/physical段与当前 final source/tests；核 frozen hashes、HEAD、staging、P05、cache。
2. Findings-first code review，至少逐项证明：
   - module 不再存在 token/InitVar/可复制 capability；pending `TruthView` 无 correctness init入口，evaluated wrapper frozen+slotted且 correctness `init=False`、只能由 decoded info在 `__post_init__` 计算；直接构造/replace/re-finalize/tamper均 fail closed。
   - Receiver per-pol C_pre exact `(2,)`、`init=False`，只从对象自身 received prefix + registered known prefix按 LS + RSS/31复算；channel/receipt无 caller C_pre 注入口，无 physical SNR/noise alias；replace received/known重算。
   - generic slots/dict/dataclass对象 fail closed；必要 plain containers/arrays完全 detached；allowlist exact-type，不接受 subclass；NumPy scalar不保留引用；cycle拒绝。
3. Fresh fixed-env tests：三个 T092 exact nodes；完整 contract + waveform-channel；codec file；schemas file；全部 `test_d0_*.py` aggregate。记录收集文件数、unique node数、0 fail/error/skip/xfail/warning。
4. Fresh mutation至少 45 例，不得只调用现有测试 helper 自证。必须包含并明确列出：
   - 重放 step-137 的 9 个 bad accepts，要求 9/9 reject；
   - token/module lookup、direct/replace/object-setattr correctness、repeat finalization、wrong decoded bits；
   - C_pre direct/replace/swap/scalar/physical value/stale receipt、received/known replace重算；
   - slots single-string/inherited、dict/dataclass/nested/cycle、post-construction source mutation、allowlist subclass、NumPy scalar；
   - physical-noise aliases、payload canonical info→codec→coded→Gray→waveform mutations、contract/code/seed/layout exact-type mutations。
   任一 owner-required mutation被接受即 P1。
5. 独立复算至少四组、每组两偏振 C_pre；核同 received/known唯一确定、与 physical noise truth不等价。复核 physical equations与 sharing未回归。
6. Static/import audit：无 truth/value leak、无 global RNG/I/O/sys.path/legacy、无 mutable receipt引用；`git diff --check`；source boundary；final hash/protection再核。
7. `VERDICT/P0/P1/P2`。P0/P1任一非零=`FAIL`；任何 required command/审查未完成=`INCOMPLETE`。仅 final bytes 的全套 fresh evidence + P0=P1=0 方可 PASS。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

≤15分钟；不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

terminal=`I06_VERIFIED_READY_FOR_BATCH2`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 final-bytes tests/mutations/static/hash/protection evidence与 step-139 SHA。
