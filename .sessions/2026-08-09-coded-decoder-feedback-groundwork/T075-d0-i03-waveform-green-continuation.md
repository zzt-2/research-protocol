# Task Brief: D0 I03 waveform GREEN continuation from valid RED

> 来源: step-117 `INCOMPLETE_VALID_RED_ONLY_15_MIN_HARD_STOP` / frozen WC test | 产出位置: `projects/thesis-fso/worker-logs/step-121-d0-i03-waveform-green-continuation.md`
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

## Hypothesis / 否决条件

- 假设：冻结 WC01–03/WC08 oracle 可由 owner/source-bound registered assets 与纯映射实现全部 GREEN，无需改测试或其他模块。
- 否决条件：测试 SHA 漂移；只能硬编码预期 SHA 而非生成注册 bytes；pilot schedule/terminal sentinel 无 owner 依据；copy-on-write 或 6144 bijection 不闭合；需改 contract/other files；或 15 分钟到期，则在最近完整 WC GREEN 边界写 `INCOMPLETE`。

## 冻结输入与 RED

```text
test=b54bb185203fe3a9fa8c3bb7ba85c4688c5efa1e7e4d7dd02957378e62e7404d
step-117=9dd643651980c812ae7ef1dd4852faf1849b7b5043656b1d4106deb97b936bbb
RED_output=6f15c28fa57ce080fdb4bebd8f27237f3956b5aaad12ec5f3570bba2bf0ab3b6
waveform.py=ABSENT
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/waveform.py`
2. Create `projects/thesis-fso/worker-logs/step-121-d0-i03-waveform-green-continuation.md`

冻结 `test_d0_waveform_channel.py` 禁止修改；step-117 只读。不得创建其他文件。

## 实现与验证

1. 核冻结 SHA/production ABSENT/保护基线；复用 T071 已读 owner、step-094/105/106 和 source semantics。
2. 实现 frozen/slotted asset/build value types，array defensive copy + read-only；public API exact：`registered_prefix()`、`registered_pilots(N)`、`build_waveform(data_symbols, *, N)`、`apply_persistent_rotation(build, *, target_pol, boundary_after_data, k)`。无 import-I/O/global RNG。
3. 生成而非伪造 registered bytes：local `Generator(PCG64(987654321))` 的 prefix bits；Gray axis/bit order owner exact；four-symbol pilot cycle与展开 schedule owner exact；prefix 32 + 6144 data + periodic pilots + terminal sentinel。`data_to_time`/`time_to_data` 使用 int64，known 为 `-1`。
4. rotation 只接受 `target_pol in {0,1}`、`boundary_after_data` 合法边界、`k in {0,1,2,3}`；从目标 time suffix 开始复制后旋转，包含 later pilots；原 build、另一偏振、pre-boundary、known symbols/maps byte-identical。
5. 按 WC01→WC02→WC03→WC08 跑冻结 exact nodes并记录每项 GREEN output SHA/count/duration；测试失败按 systematic diagnosis 只改 production。若测试/owner 冲突，named blocker，不改 test。
6. 四项 GREEN 后跑完整新文件及 `test_d0_contract_views.py` 回归。终检只两个目标变化；p05/cache/staging/HEAD保护；无 benchmark/science/web/install/commit/push。

## 命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact node or file> -q
```

15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；四 WC 逐项 GREEN；`waveform.py`/step-121 SHA；protection receipt；terminal=`I03_READY_FOR_INDEPENDENT_VERIFICATION`、`I03_INCOMPLETE_AT_WCxx` 或 named blocker。
