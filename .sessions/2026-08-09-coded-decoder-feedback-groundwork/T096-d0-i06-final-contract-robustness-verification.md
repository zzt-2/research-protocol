# Task Brief: D0 I06 final contract robustness verification

> 来源: T095 verifier platform interruption（无 step-141）/ T094 READY | 唯一产出: `projects/thesis-fso/worker-logs/step-142-d0-i06-final-contract-robustness-verification.md`
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

## 身份、目的与冻结输入

- non-author independent verifier；只读 final production/tests，任何缺陷只记录不修复。
- T095 已 fresh 跑完五组 pytest 后因平台内容过滤中断，未写 step-141、无可接收终态；本任务必须自行重跑，不继承其结论。
- 本任务是普通本地单元测试与数据契约鲁棒性验证，不涉及网络、安全系统或外部目标。

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

只创建 `projects/thesis-fso/worker-logs/step-142-d0-i06-final-contract-robustness-verification.md`。不得修改 source/tests/governance/其他日志。

## 独立验收

1. 完整读 T094/T096、D012–D013、step-139/140、owner truth/receiver/physical段和 final source/tests；核 frozen hashes、HEAD/staging/P05/cache。
2. Fresh code review：
   - evaluated wrapper没有 correctness field/slot/cache；只读 property由 pending truth与已验证 decoded bits重算，普通赋值、底层属性赋值、constructor/replace均不能直接设 correctness；property返回数组的修改不影响后续读取。
   - Receiver metadata为 closed-world exact-type tree；所有允许容器/array均 detached immutable，cycle与 subclasses拒绝。
   - Receiver noise key采用稳定 normalization与 exact safe derived keys；TruthView物理 noise receipt仍合法，channel不把物理 noise/SNR写入 Receiver。
   - root seed在归一化前只接受 exact Python int；contract/code/layout/payload/C_pre旧门不回归。
3. Fresh fixed-env tests：四个 T094 exact节点；完整 contract+waveform；codec；schemas；aggregate全部 `test_d0_*.py`。记录文件/unique node数，要求0 fail/error/skip/xfail/warning。
4. 在临时内存脚本中独立构造不少于80个“应拒绝输入 + 应接受控制”数据契约用例，不修改仓库测试。至少覆盖：
   - correctness：普通/底层属性设置、constructor/replace、property返回值改动、重复 finalize、decoded shape/type/binary错误；另有合法不同 decoded output正例。
   - metadata类型：bytearray、memoryview、range、object、deque、array.array、mappingproxy、UserDict/UserList、自定义 Mapping/Sequence/Set、dataclass、slots/dict对象、generator/iterator、nested/cycle、源对象构造后变化、allowlist subclass、ndarray subclass、NumPy scalar；另有合法 plain tree/array正例。
   - Receiver keys：noise/awgn/n0/snr/variance/power/sample 的 camel/case/separator/plural/数字/嵌套变体；safe receiver-derived keys、无关 metadata 与 TruthView physical receipt正例。
   - root：bool/np.bool_、各宽度 NumPy signed/unsigned int、float/string/negative/oversize拒绝；exact Python int边界正例。
   - payload info→codec→coded→Gray→waveform、contract/code/seed/layout、C_pre replace/recompute回归。
   每例记录 EXPECT_REJECT/EXPECT_ACCEPT 与实际结果；任一 owner-required bad input被接受即P1，合法 control被拒也必须计 finding。
5. 独立复算四组 physical equations/sharing和每组两偏振 C_pre；确认 payload不一致被拒、合法truth变化不泄漏到deployable receiver bytes。
6. Static/import audit、`git diff --check`、source boundary与 final hashes/protection census。无 global RNG/I/O/sys.path/legacy/mutable receipt引用。
7. findings-first `VERDICT/P0/P1/P2`。P0/P1任一非零=`FAIL`；required项未完成=`INCOMPLETE`；只有 final bytes fresh全验且P0=P1=0方可 PASS。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

≤15分钟；不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

terminal=`I06_VERIFIED_READY_FOR_I05`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 final tests/contract-cases/static/hash/protection evidence与 step-142 SHA。
