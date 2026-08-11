# Task Brief: D0 I06 independent channel/truth verification

> 来源: T084/T087 / step-130/133 | 唯一产出: `projects/thesis-fso/worker-logs/step-135-d0-i06-independent-verification.md`
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

- fresh independent verifier；不得参与 I06 修复，不得修改 production/tests。
- `channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde`
- `test_d0_waveform_channel.py=ce5b80b262612943ada9e5677ff27713bef8dafd9cf17c6f8e537d464da5c3b0`
- `step-130=7d787b55f12b84a654bd87c453669b8bd317f2da6cb2b02a1f2a267e1de706b7`
- `step-133=d0d8ca7b4b7c202289028ca52f2d43025b21ef75ad72a9766f68a89eb5a0bdc3`
- `contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713`
- `waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f`
- `owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d`
- `HEAD=715a65884b988ee737f21982f3bbf372860a1da8`

## 唯一允许写入

只创建 `projects/thesis-fso/worker-logs/step-135-d0-i06-independent-verification.md`。任何 production/test defect只报告，不修。

## 独立审查

1. 完整读 owner physical realization/RNG/ReceiverView/TruthView、step-094/095、T084/T087、step-130/133、channel/test/contract/waveform。核冻结 SHA、HEAD/staging/保护。
2. 代码审查：
   - six-name `SeedSequence.spawn(6)` + local PCG64，固定 order/receipt；访问/消费隔离；不触碰 global RNG。
   - GG source-bound GAR、`tau=1/(2π100)`、block100 `rho=exp(-100Ts/tau)`、field=`sqrt(intensity)`；GG/Wiener双pol共享，AWGN独立；identity SOP；supplied-waveform equation exact。
   - Wiener `variance=2πΔνTs`，effective linewidth只一次，theta[0]=首 innovation；AWGN per-real/complex units exact。
   - `build_views` 是唯一双侧 factory；Receiver direct fields/receipts递归无 truth，合法 CodeLayout/WaveformLayout metadata不误拒；Truth量完整；arrays defensive/read-only；contract identity/shape/nonfinite fail closed。
   - 无 legacy runtime import/sys.path/I/O/import side effect；I06 未偷做 equalizer/BPS。
3. 重跑 WC04–07 exact、full waveform-channel 9 tests、I02 6 tests，固定 Windows命令；0 skip/xfail/warning。
4. 在不改 tests 的独立脚本中做 fresh negative/mutation checks，至少：bool/float/negative/oversize root；unknown cell；wrong/nonfinite supplied waveform；forged contract/layout identity；global RNG state不变；named stream access重排/额外消费隔离；Receiver direct truth alias与 receipts 中 nested mapping/dataclass/slots/container alias拒绝，同时 `information_bits_per_cw`合法通过。
5. 独立数值复算至少 4 linewidth/seed/cell组合的 tau/rho/innovation/AWGN方程及 sharing matrix；不得只复述 step-133。
6. 输出 findings-first，`VERDICT/P0/P1/P2`，每个发现附 file:line、owner依据、复现命令；若无发现记录 mutation counts/hashes。P0/P1 任一非零即 FAIL。
7. ≤15分钟；不 benchmark/science/web/install/commit/push/stage。禁止改源码/测试后自验。

## 返回

terminal=`I06_VERIFIED_READY_FOR_BATCH2`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 tests/mutations/SHA/保护证据。
