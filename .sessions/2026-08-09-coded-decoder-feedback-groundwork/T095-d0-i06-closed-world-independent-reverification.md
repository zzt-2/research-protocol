# Task Brief: D0 I06 closed-world final independent reverification

> 来源: T093 FAIL / T094 READY / step-139–140 / D012–D013 | 唯一产出: `projects/thesis-fso/worker-logs/step-141-d0-i06-closed-world-independent-reverification.md`
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

- non-author independent verifier；只读 final production/tests，缺陷只报告不修。
- 不得复用作者 step-140 的 GREEN/mutation结论代替 fresh evidence。

```text
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
channel.py=af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6
test_contract=30fe6b67b6b26c9fc962476fef8287159b10e95bb046a67b0ee25cdf76b47779
test_waveform_channel=f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
step-139=959fe9bffaa795633fcd4e0f9a72d08025f5573d67d631158e6128baa6a937b0
step-140=c54866255c88bbb379e597bdc45f88135a6ca403b864245cce2bb995d303af73
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

只创建 `projects/thesis-fso/worker-logs/step-141-d0-i06-closed-world-independent-reverification.md`。不得修改 source/tests/governance/其他日志。

## 独立验收

1. 完整读 T093–T095、D012–D013、step-139/140、owner truth/receiver/physical段和 final source/tests；核 frozen hashes、HEAD/staging/P05/cache。
2. Fresh code review逐项确认：
   - evaluated wrapper没有 correctness field/slot/cache；property重算、无 setter，property返回值修改不持久；direct/object setattr/constructor/replace correctness无入口。decoded bits本身 exact/defensive，pending/evaluated chronology不退化。
   - Receiver tree为 closed-world exact types，不是 opaque-type denylist；所有允许容器/array均 detached immutable，cycle与 subclasses fail closed。
   - Receiver noise gate使用 stable semantic normalization + exact safe derived keys，不靠四个新词；truth noise receipt仍合法、physical noise/SNR值不进入 Receiver。
   - root seed在任何归一化前 exact Python int；PhysicalCell及contract/code/layout identity不回归。
3. Fresh fixed-env tests：四 T094 exact；完整 contract+waveform；codec；schemas；aggregate全部 `test_d0_*.py`。记录 collected/unique file/node数，0 fail/error/skip/xfail/warning。
4. Fresh adversarial mutation≥80，不得只调用现有 tests/helper。必须重放 step-139 10项并新增 near-neighbors：
   - correctness普通/object setattr、property result mutation、constructor/replace、repeat finalize、decoded wrong shape/type/nonbinary；明确区分“合法不同 decoded output”与“caller直接注入 correctness”。
   - bytearray/memoryview/range/object、deque/array.array/mappingproxy/UserDict/UserList/custom Mapping/Sequence/Set、dataclass/slots/dict/generator/iterator、nested/cycle/post-source mutation、allowlist subclass、ndarray subclass/np scalar。
   - noise/awgn/n0/snr/variance/power/sample 的 camel/case/separator/plural/数字/嵌套 variants；safe derived keys正例；unrelated metadata正例；TruthView physical receipt正例。
   - bool/np.bool_/各宽度 np signed/unsigned int/float/string/negative/oversize root；exact Python int boundaries正例。
   - canonical payload info→codec→coded→Gray→waveform、contract/code/seed/layout、C_pre replace/recompute旧门回归。
   任一 owner-required bad mutation接受即 P1；合法 control拒绝也按P1/P2影响评估，不能只报“全部拒绝”。
5. 独立复算四组 physical equations/sharing与每组两偏振 C_pre；验证Receiver bytes不含 physical truth、payload mutations不影响 deployable bytes但不一致链被拒绝。
6. Static/import audit、`git diff --check`、source boundary、hash/protection final census。无 global RNG/I/O/sys.path/legacy/mutable receipt引用。
7. findings-first `VERDICT/P0/P1/P2`。P0/P1任一非零=`FAIL`；required项未完成=`INCOMPLETE`；只有 final bytes fresh全验、P0=P1=0方可 PASS。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

≤15分钟；不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

terminal=`I06_VERIFIED_READY_FOR_I05`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 final tests/mutation/static/hash/protection evidence与 step-141 SHA。
