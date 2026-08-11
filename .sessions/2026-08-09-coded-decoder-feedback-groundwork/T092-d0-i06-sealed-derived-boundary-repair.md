# Task Brief: D0 I06 sealed finalization / derived C_pre / immutable receipt repair

> 来源: T091 / step-137 `FAIL 0/3/0` / D012 | 产出位置: `projects/thesis-fso/worker-logs/step-138-d0-i06-sealed-derived-boundary-repair.md`
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

## Review disposition / frozen design

- 接受 step-137 三项 P1，不弱化、不转为 P2。
- D012 两阶段 truth 因果边界保持不变，但去掉任何 caller-visible capability token：pending `TruthView` 构造路径永远不能接收 correctness；evaluator 返回一个独立 frozen/slotted evaluated wrapper，其 correctness 只能在 `__post_init__` 内由 decoded information bits 与 truth information bits逐码字计算，字段 `init=False`。
- Receiver 的逐偏振 `C_pre` 必须由同一对象内的 `received_samples[:, :32]` 与 `known_prefix` 按 owner LS + RSS/31 自动派生，字段 `init=False`；调用方、channel 与 receipt 均不能注入该值。`dataclasses.replace` 改 received/known 时必须重算。
- 任意 generic `__slots__` / `__dict__` 对象不得原样进入冻结 receipt。优先 fail closed；若实现 detached immutable plain tree，必须证明源对象后续变异不影响 receiver bytes/receipt。
- 此任务不扩大至 I05、methods、runner、artifact、benchmark 或 science。

## 假设 / 否决条件

- 假设：三个 P1 可仅在既有四个 I06 文件与一个日志内，通过 init-free derived state 和 fail-closed receipt policy 闭合。
- 否决条件：仍需 module-readable token/private sentinel 才能授权 correctness；Receiver 仍需 caller 传入 C_pre；generic mutable object 必须保留引用；需改 codec/waveform/schemas/owner/common/legacy；或 15 分钟内不能完成全审计。命中任一项即 `INCOMPLETE`，不得宣称 READY。

## 冻结输入

```text
contract.py=35b20e922b9ea55c497b01fcf2d9b7bf92cf6e2f3386815dcec92911b21c7c8e
channel.py=c90d6c4d2ae8d4a860a1f1c5167a92c2ded383f4cc3518da55659cd36ceda9f9
test_contract=ad07d742f49efc9e814da4c4d67f305f27c3e79a035d60b636de5b9215561f89
test_waveform_channel=11cba3e14ed83eb015418e4d59ae4cc080da923b92b11d7f1c7d6a8bc07725ff
step-136=f898536ff99cd48867134c9495be0db9c5bab6a00b6e098af1fa63a7b092c27a
step-137=29918182abc1a21bf76830bb318ee8d2b05d1829a01a347663ba4ea2ea9d9409
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
D012 decisions=bde22e6ca455fd5986d0de14777abe2f3b44adfb604bf610a527cc71b75f51fb
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/channel.py`
3. Modify `projects/simulation/tests/test_d0_contract_views.py`
4. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
5. Create `projects/thesis-fso/worker-logs/step-138-d0-i06-sealed-derived-boundary-repair.md`

不得修改 codec/waveform/schemas/owner/common/legacy/governance；不得创建 runner/artifact/result/cache。不得 install/commit/push/stage。

## Strict TDD

1. 完整读本任务、D012、step-137、step-136 与当前四文件；先核全部冻结 SHA、HEAD、staging、P05 与 pycache 保护状态。
2. production 前新增下列 exact nodes：
   - `test_i06_truth_finalization_is_constructor_sealed`
   - `test_i06_receiver_noise_estimate_is_init_free_derived`
   - `test_i06_generic_receipt_objects_fail_closed`
   三节点必须在当前 production 上实际 RED。立即把命令、失败原因、test/source SHA 和 output SHA 写入 step-138 receipt；此后才允许改 production。
3. Truth lifecycle：
   - 删除 `_TRUTH_FINALIZER_TOKEN` 或任何模块可读取/可复制的同类能力；pending `TruthView` 对 correctness 没有 init 参数，且构造后恒为 `None`。
   - evaluator pure function只接收 pending truth view 与 decoded information bits，返回独立 frozen/slotted `EvaluatedTruthView`（命名可等价）。wrapper 的 `final_codeword_correctness` 必须 `init=False`，由 `__post_init__` 内逐 CW 全位相等计算 exact `(2,16)` bool；caller 无 token、无 correctness 参数。
   - 直接构造 correctness、`dataclasses.replace` correctness、`object.__setattr__` 后再经公开 validator/finalizer、重复 finalize、错误 shape/type/nonbinary 均拒绝。原 pending truth 与 payload bytes 不变。
4. Receiver-derived `C_pre`：
   - `ReceiverView.receiver_noise_estimate`（或语义等价 typed per-pol字段）必须 `init=False`，在 `__post_init__` 从自身 `received_samples[:, :32]` 和 registered `known_prefix` 按 `g=sum(conj(x)r)/sum(abs(x)^2)`、`RSS/31` 自动计算 exact `(2,)` finite float。
   - `build_views`/channel 不得把 C_pre 作为 Receiver 构造参数；receipt 中若保留逐偏振值，只能由 ReceiverView 内部刚计算的 detached immutable值生成，不能接受外部重复字段。
   - `dataclasses.replace(receiver, received_samples=...)` 与改 `known_prefix` 的合法路径必须重算；swap/inject physical/stale/scalar/wrong-shape 等 caller mutation无入口或被拒绝。不得把 physical SNR/noise truth写入 receiver/receipt。
5. Generic receipt policy：
   - `_deep_freeze` 对任意非 allowlisted generic `__slots__` / `__dict__` 对象 fail closed；不得把原对象或其可变引用塞进 frozen dataclass。
   - 继续支持既有必要 Mapping/list/tuple/set/ndarray 的 detached immutable转换与循环保护；CodeLayout/WaveformLayout仅显式 allowlist。
   - 覆盖单字符串 slots、继承 slots、dict object、nested object、构造后源对象变异；任何 truth/value alias均拒绝，且合法 plain-tree receipt仍通过。
6. 测试既要验证 API 无注入口，也要做 mutation：module token lookup/forgery、direct/replace correctness、receiver C_pre direct/replace/swap/physical值、generic object post-mutation至少各 4 例。不得只用 `repr` 子串 oracle。
7. 跑三 exact nodes；完整 contract + waveform-channel；codec 7；schemas current file；全部现有 `test_d0_*.py` aggregate。要求 0 fail/error/skip/xfail/warning。
8. 重放 step-137 9 个 bad accepts并确认 9/9 reject；fresh mutation 总数不少于 30。独立复算至少四组 per-pol C_pre；做 static/import audit、`git diff --check`、source boundary、HEAD/staging/cache/P05保护核验。
9. 日志 findings-first，逐项 disposition step-137 P1-1/P1-2/P1-3；记录 RED/GREEN、mutation matrix、命令、hashes和剩余风险。任一未闭即 `INCOMPLETE`。

## 固定执行环境

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

不运行 benchmark/science/MVE/web；单次任务不超过 15 分钟。

## 返回

RED/GREEN、step-137 9 个 bad accepts closure、fresh mutation counts、per-pol C_pre receipts、五个写入文件 SHA；terminal=`I06_READY_FOR_INDEPENDENT_REVERIFICATION`、`INCOMPLETE` 或 blocker。
