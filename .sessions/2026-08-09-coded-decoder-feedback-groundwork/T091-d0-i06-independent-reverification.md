# Task Brief: D0 I06 independent reverification after D012 repair

> 来源: step-135 FAIL / D012 / step-136 INCOMPLETE post-GREEN | 唯一产出: `projects/thesis-fso/worker-logs/step-137-d0-i06-independent-reverification.md`
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

- fresh non-author verifier；你提出 step-135 findings，但未实施 T090。只读 production/tests，任何缺陷只报告不修。
- `contract.py=35b20e922b9ea55c497b01fcf2d9b7bf92cf6e2f3386815dcec92911b21c7c8e`
- `channel.py=c90d6c4d2ae8d4a860a1f1c5167a92c2ded383f4cc3518da55659cd36ceda9f9`
- `test_contract=ad07d742f49efc9e814da4c4d67f305f27c3e79a035d60b636de5b9215561f89`
- `test_waveform_channel=11cba3e14ed83eb015418e4d59ae4cc080da923b92b11d7f1c7d6a8bc07725ff`
- `step-135=3815f424b3f33f64ebf374ff61ddf0a7b05178cc5adc8461da6fd8eeec9f284f`
- `step-136=f898536ff99cd48867134c9495be0db9c5bab6a00b6e098af1fa63a7b092c27a`
- `codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b`
- `waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f`
- `owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d`
- `D012 decisions=47acc58ac08fd7cbb970590923926761e45faaed0c5c15fdebc6862314da9d0a`
- `HEAD=715a65884b988ee737f21982f3bbf372860a1da8`

## 唯一允许写入

只创建 `projects/thesis-fso/worker-logs/step-137-d0-i06-independent-reverification.md`。不得修改 source/tests/governance。

## 独立验收

1. 完整读 T090/T091、D012、step-135/136、owner truth/receiver/physical段、step-094 §3.1、当前 source/tests；核 hashes、HEAD/staging/cache/p05。
2. 逐项重审 step-135 `P1-1/P1-2/P1-3/P2-1`，并检查派发后两项预审：
   - Receiver `(2,)` C_pre 必须只由每pol received/known prefix LS+RSS/31得出；Receiver/receipt不得含 physical SNR/noise value/derived alias；同输入唯一复算。
   - PayloadTruth必须 canonical `info→D0Codec.encode→coded→gray16_map→waveform.data_to_time` 全链一致；三处各做等 shape/count-preserving mutation并拒绝；不同合法 truth对应不同 waveform可通过，且对同一 valid physical realization只改变 evaluator truth不得引入 deployable truth读取。
   - correctness 初态必须显式 pending而非空array；唯一 finalizer从 decoded info逐CW计算 `(2,16)`，直接注入、重复finalize、错误shape/type/nonbinary全部拒绝；原 truth不可变。
   - slots/`__dict__`/mapping/dataclass/container递归、contract/code/seed/layout identity、array shape/finiteness、root int64/cell exact全部 fail closed。
3. 代码审查 canonical codec cache：不得缓存 message/decoder warm state，不能用 truth影响 Receiver物理/RNG；payload验证发生在物理 RNG消费前后均不得改变 named stream结果。channel import不得带 I/O/global RNG/sys.path副作用。
4. Fresh tests，固定 Windows命令：四 T090 exact nodes；完整 contract + waveform-channel；codec 7；当前 schemas file；然后全部现有 `test_d0_*.py` aggregate（若只含当前四文件，记录文件/unique test数）。0 fail/error/skip/xfail/warning。
5. Fresh mutation不少于：重放 step-135 28例；step-136结构/payload/finalizer/root-cell至少45例；另加 forged PayloadTruth subclass/direct dataclass replace、codec encode output mutation、waveform one-symbol mutation、per-pol C_pre swap/scalar collapse/physical-value injection、finalizer token/direct replace、contract seed/code/population精确类型变体。记录 rejected/accepted matrix；任何 owner-required mutation接受即 P1。
6. 独立复算四组物理数值与四组 per-pol C_pre，确认 WC equations/sharing未回归；static/import audit、`git diff --check`、source boundary、protected hashes、no cache delta。
7. findings-first `VERDICT/P0/P1/P2`；P0/P1任一非零 FAIL。不可因 tests GREEN 自动 PASS，不得复述 step-136代替检查。
8. ≤15分钟；不 benchmark/science/web/install/commit/push/stage。

## 返回

terminal=`I06_VERIFIED_READY_FOR_BATCH2`、`I06_VERIFICATION_FAIL` 或 `INCOMPLETE`；附 tests/mutations/static/hash/protection evidence。
