# Task Brief: D0 I06 fresh final verifier

> 来源: T095 platform interruption / T096 timebox INCOMPLETE / T094 final bytes | 唯一产出: `projects/thesis-fso/worker-logs/step-143-d0-i06-fresh-final-verifier.md`
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

## 身份与目的

- 你是 fresh non-author verifier，只做普通本地 Python 数据契约/数值单元验证。
- T095 无日志，T096 只有 pytest、没有完整合同矩阵；二者均不可接收。你必须从最终字节自行建立完整证据。
- 目标在 12 分钟内完成，15 分钟硬停止；缺一项即 `INCOMPLETE`，不扩展范围。

## 冻结输入

```text
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
channel.py=af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6
test_contract=30fe6b67b6b26c9fc962476fef8287159b10e95bb046a67b0ee25cdf76b47779
test_waveform_channel=f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
step-140=c54866255c88bbb379e597bdc45f88135a6ca403b864245cce2bb995d303af73
step-142=e76f76de0751c4dce29a0067c98e1052410b444a9b89c7b0a90f2cc123984ffc
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

只创建 `projects/thesis-fso/worker-logs/step-143-d0-i06-fresh-final-verifier.md`。不得修改 source/tests/governance/其他日志。内存校验脚本通过 PowerShell here-string pipe 到 Python stdin，不创建仓库脚本。

## 最小完整验收

1. 读本任务、step-140/142、D012–D013、final source/tests及 owner 对应 truth/receiver/physical 段；核 frozen hashes、HEAD/staging/P05/cache。
2. 固定环境运行：
   - 四个 T094 exact nodes；
   - aggregate `projects/simulation/tests/test_d0_*.py`。
   两个命令均要求0 fail/error/skip/xfail/warning，并记录 exact/aggregate node数与 output SHA。
3. 用一个 Windows PowerShell here-string pipe 到 Python stdin的内存脚本完成不少于80个独立数据契约 cases，输出每类 accepted/rejected/control计数和总 output SHA。必须含：
   - correctness 10+：无公开 field/slot/setter，constructor/replace/直接属性设置拒绝，property结果修改不持久，错误 decoded shape/type/binary拒绝，合法不同 decoded output接受。
   - metadata 30+：opaque built-ins、标准库容器、custom protocol/dataclass/slots/dict、nested/cycle、构造后源变化、subclass/NumPy类型；不允许类型拒绝，合法 exact plain tree/array detached且接受。
   - Receiver keys 20+：noise/awgn/n0/snr/variance/power/sample 的大小写/camel/分隔/复数/嵌套变体拒绝；两个 exact receiver-derived safe keys、无关 metadata与TruthView physical receipt接受。
   - root scalar 15+：bool/NumPy bool/各宽度 NumPy signed+unsigned/float/string/negative/oversize拒绝；0与`2**63-1` exact Python int接受。
   - 至少5个 payload/contract/C_pre回归 cases。
   每个 case预先标 EXPECT_REJECT 或 EXPECT_ACCEPT；任何期望错位都逐项记录。
4. 同一内存脚本或单独只读命令，独立复算4组、每组双偏振 C_pre与物理 equations/sharing；要求8/8 C_pre match，payload chain valid，receiver bytes不含 physical truth。
5. 轻量 static/import审查、`git diff --check`、最终 source/hash/protection census；确认无 global RNG/I/O/sys.path/legacy/mutable receiver metadata引用。
6. findings-first `VERDICT/P0/P1/P2`：任一 expected bad被接受或承重合法 control被拒=`P1`；P0/P1非零=`FAIL`；required项未完成=`INCOMPLETE`。只有全部完成且P0=P1=0才 PASS。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

不 benchmark/science/MVE/web/install/commit/push/stage。

## 返回

terminal=`I06_VERIFIED_READY_FOR_I05`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 tests/cases/numeric/static/hash/protection evidence与 step-143 SHA。
