# Task Brief: D0 I06 named RNG, physical channel and truth split (TDD)

> 来源: step-128 I03 VERIFIED / plan I06 / step-106 WC04–WC07 | 产出位置: `projects/thesis-fso/worker-logs/step-130-d0-i06-channel-truth-split.md`
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

- 假设：owner 的 six-name SeedSequence/PCG64、shared GG+Wiener、independent per-pol AWGN、effective-linewidth equations及唯一 Receiver/Truth split factory可在 identity-SOP supplied-waveform channel中精确实现。
- 否决：需 runtime import P08/P08-R2/2×2 LS；linewidth TX+LO redoubling；Receiver含 truth；共享/独立矩阵不闭合；只靠 global RNG；需改 waveform/contract；或15分钟不收敛。

## 冻结输入

```text
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
test_waveform=f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157
step-125=092f535d64781f1ef9a0353ee70b85c55bb176cecd2b2327d2c0b79731b4974e
step-128=4b0b1257c7964724821fb94f6141e39cd3ef542133e567e2f73e10836a56959f
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/channel.py`
2. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
3. Create `projects/thesis-fso/worker-logs/step-130-d0-i06-channel-truth-split.md`

不得修改 waveform/contract/owner/legacy；不得创建 runner/artifact/result/cache。

## TDD 任务

1. 完整读 T084、plan I06、step-106 WC04–07、step-105 channel interface、step-094/095 physical/source maps、owner physical_realization/view fields与 I03 repaired evidence。核 hashes/protection。
2. **先追加 tests，不写 channel.py**；名称 exact：
   - `test_named_seedsequence_spawn_receipt`（WC04）：root=999901；order `payload_x,payload_y,gamma_gamma,wiener,awgn_x,awgn_y`；root entropy、NumPy version、child spawn_key、pool_size、generate_state(4,uint32)稳定且六子互异；无 global RNG。
   - `test_stream_consumption_isolation`（WC05）：同 root 两次；一侧额外消耗 payload_x，GG/Wiener/AWGN-X/Y 的首批 bytes仍各自与 control相同；named order不因访问顺序改变。
   - `test_shared_gg_wiener_independent_awgn`（WC06）：16-symbol supplied two-pol input；GG intensity/field fade与phase bytes X=Y，AWGN X≠Y；同 root重跑全 bytes identical；received符合 identity-SOP逐偏振 `sqrt(I)*x*exp(j theta)+n`；`build_views` Receiver/Truth frozen split，无 truth key进入 Receiver。
   - `test_gamma_gamma_wiener_formulas`（WC07）：`Ts=1/2.5e9`；`tau=1/(2π*100)`；block100 rho=`exp(-100*Ts/tau)`；linewidth 10k/20k/80k innovation variance=`2πΔνTs` exact；theta[0]=first innovation（不是额外 zero），effective linewidth仅一次；AWGN per-real=`1/(2*10^(snr_db/10))`、complex power=`1/gamma`。
3. 在 `channel.py=ABSENT` 时跑四 exact nodes取得有效 RED（module absent可接受，collection/fixture/dependency error不可）；**立即先写 step-130 receipt** 后才能 production。追加改变 test SHA，由本次 RED supersede先前 file-level receipt；原五 waveform tests保留原文。
4. 最小实现：
   - frozen/slotted `NamedStreams`/receipt/physical realization value types，arrays defensive/read-only；`spawn_named_streams(root_seed)` 只用 `SeedSequence.spawn(6)`+PCG64 local generators；
   - pure equation helpers与 deterministic generation；GG method/source-bound按 owner/step-095，不自创分布；phase/GG跨pol共享，AWGN独立；SOP identity，无 cross-pol；
   - `build_views(contract,waveform,*,root_seed,physical_cell,event_fixture=None)->(ReceiverView,TruthView)` 是唯一同时观察两侧的 factory；Receiver只含 received/known/layout/noise estimate/receipts，Truth承载真实 fade/phase/noise/tx/event；调用 contract recursive guard，拒绝 leakage；本 I06 不实现 receiver equalizer/BPS。
   - no legacy runtime import/sys.path/I/O/global RNG/import side effects。
5. 不改 tests，四 GREEN后跑 full waveform-channel（应9 tests）及 I02 contract regression；负面 invalid root/cell/shape/nonfinite/contract identity fail closed。记录 source/test/log SHA、counts/output、无 skip/xfail/warning。
6. 终检三目标、p05/cache/staging/HEAD；不 benchmark/science/web/install/commit/push。≤15 分钟；到时 test-ID boundary INCOMPLETE。

## 返回

WC04–07 RED/GREEN、full counts、三 SHA、sharing/truth receipts；terminal=`I06_READY_FOR_INDEPENDENT_VERIFICATION`、`INCOMPLETE_AT_WCxx` 或 blocker。
