# Task Brief: D0 typed decoder hard-output write anchor

> 来源: D020–D022 / T120 / I05 closure map | 产出位置: `projects/thesis-fso/worker-logs/step-167-d0-hard-output-write-anchor.md`
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

- 实际代码片A。只改 `schemas.py`、`codec.py`、`test_d0_receiver_codec_methods.py` 与step-167；owner/contract/session/其他tests/P05/cache只读。
- 12分钟目标、15分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_TYPED_HARD_OUTPUT_WRITE_ANCHOR_READY_FOR_BATCH_VERIFICATION`；独立验收推迟到I05三代码片完成后的单次batch verifier。

## Required behavior

1. TDD RED first，至少覆盖：两个owner hard-output golden、`decode_fresh`立即返回typed ref、非binary/shape/forged root拒绝、fresh state不回归。
2. 在`schemas.py`实现最小immutable/opaque hard-output authority：exact payload与store-record schema；canonical JSON SHA256；16×1024 binary bits按CW-major C-order、MSB-first pack为2048 bytes、RFC4648 base64长2732且恰一个`=`；public factory只接受bits，不接受caller hash；public assertion重新解码/复算root；store validator做root唯一与forward/reverse exact-set gate。
3. `DecoderHardOutputRef`必须由factory生成、内容不可变、fresh materialization不共享可变对象；伪造dataclass/object/root/payload均fail closed。允许保留只读兼容`info_bits`视图，但其修改不得改变authority或下次读取。
4. `D0Codec.decode_fresh`在backend hard bits完成shape/dtype/finiteness/binary检查后立即调用factory；`DecodeBatch`持有typed ref。D0 owner固定每次16 CW，因此runtime decode batch exact `(16,1024)`；更新旧unit fixtures为16 CW，不新增通用batch语义。
5. Owner goldens exact：all-zero root=`1c04a714a23a42c1d32f0b1bab3c1ff5469b5c1f2183f57c3afcaf5407299960`；first-bit root=`9668fc189c6a3678df8b88d3a1effa221d4fa2968d5e884e6a8f85c36e837a0e`。
6. GREEN只跑本文件；要求0 fail/error/skip/xfail/warning。至少12 fresh negative/mutation cases，wrong accept/reject=0/0；静态检查codec只能由bits调用factory，不能传任意hash。

## Protection / receipt

- `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Python3.11 `-B -p no:cacheprovider`。
- step-167记录RED/GREEN命令、exit/count/stdout SHA、goldens、mutations、file hashes、HEAD/staging/P05/cache保护、P0/P1/P2。
- 最多一次语法/fixture修正；发现需要改owner/contract或超过三代码文件即FAIL/INCOMPLETE，不扩范围。
