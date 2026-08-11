# Task Brief: D0 I06 step-135 P1/P2 truth-boundary repair

> 来源: T089 / step-135 `FAIL 0/3/1` / D012 | 产出位置: `projects/thesis-fso/worker-logs/step-136-d0-i06-truth-boundary-repair.md`
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

## Review disposition / architecture decision

- 接受 step-135 P1-1、P1-2、P2-1；接受 P1-3 的完整 info/coded payload 缺失。
- 对 P1-3 的 final correctness 按 D012 修复：解码前不可知，禁止预填真假；用显式 pending（`None`/typed state，不得再用空尺寸数组）+ evaluator-only finalizer 从 decoded information bits 计算新冻结 TruthView。
- 此任务不实现 receiver equalizer/BPS、methods/evaluator runner 或 science；只修 view/channel boundary。

## 假设 / 否决条件

- 假设：typed payload truth、receiver-only prefix residual estimate、exact D0 identity/shape guards和两阶段 finalization可在现有四文件内闭合。
- 否决：必须把 physical SNR/noise truth继续传入 Receiver；必须预知/伪造 correctness；需要改 owner/common/legacy；或15分钟不收敛。

## 冻结输入

```text
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test_contract=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
test_waveform_channel=ce5b80b262612943ada9e5677ff27713bef8dafd9cf17c6f8e537d464da5c3b0
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
step-133=d0d8ca7b4b7c202289028ca52f2d43025b21ef75ad72a9766f68a89eb5a0bdc3
step-135=3815f424b3f33f64ebf374ff61ddf0a7b05178cc5adc8461da6fd8eeec9f284f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
D012 decisions=47acc58ac08fd7cbb970590923926761e45faaed0c5c15fdebc6862314da9d0a
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/contract.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/channel.py`
3. Modify `projects/simulation/tests/test_d0_contract_views.py`
4. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
5. Create `projects/thesis-fso/worker-logs/step-136-d0-i06-truth-boundary-repair.md`

不得修改 waveform/codec/schemas/owner/common/legacy；不得创建 runner/artifact/result/cache。

## Strict TDD

### 派发后独立预审补充（必须执行）

- `PayloadTruth` 不得只做 shape/binary 检查：至少必须验证 coded bits 的 Gray-16QAM 映射与 supplied waveform 的 6144 data positions exact。information bits 与 coded bits 还必须由 canonical codec encode 关系绑定；若需修改 codec/factory 而超出本任务唯一写集，本任务应诚实返回 `INCOMPLETE_PAYLOAD_CODEC_BINDING`，由下一切片关闭，不能宣称 READY。
- owner 的 `C_pre` 是逐偏振 receiver-visible 值；ReceiverView 的 typed 主字段必须保留 exact shape `(2,)` 的 per-pol estimate（或语义等价的显式 per-pol字段）。不得只保留 scalar aggregate、把逐偏振值藏在 receipt 后让 I09 临时读取。
- “改变 Truth 不影响 Receiver”只验证因果隔离，不等于 Truth 可与 waveform/code 不一致；两类 gate 都必须存在。

1. 完整读本任务、D012、step-135、owner truth/physical/receiver段、step-094 §3.1、当前四文件。核冻结 hashes/保护。
2. production 前新增 exact nodes（名称 exact）：
   - `test_i06_receiver_noise_is_observation_only`
   - `test_i06_view_contract_mutations_fail_closed`
   - `test_i06_payload_truth_lifecycle_complete`
   - `test_i06_seed_cell_scalar_bounds`
   当前 production 上四节点必须实际 RED；立即先写 step-136 receipt（test/source SHA、output hash），再改 production。
3. `PayloadTruth`（命名可等价）必须 frozen/slotted/defensive，information bits exact `(2,16,1024)`、coded bits exact `(2,16,1536)`、binary uint8语义；`build_views` 将其设为必填 keyword并复制进入 TruthView。不得从 symbols反推 bits或用空数组。
4. Truth lifecycle：
   - `build_views` 返回 `final_codeword_correctness=PENDING`（建议 `None`），禁止 `(2,0)` 等空数组；
   - 提供 evaluator-only pure finalizer，输入 decoded information bits exact `(2,16,1024)` binary，内部与 truth information bits逐CW全位比较，返回新 frozen TruthView，其 correctness exact `(2,16)` bool；caller不得直接传 correctness；原 truth不变；重复/错误shape/nonbinary/nonfinite拒绝。
5. Receiver noise：从 `received prefix` 和 registered known prefix按 owner LS `g=sum(conj(x)r)/sum|x|²`、per-pol `RSS/31` 计算 receiver-visible complex residual；Receiver scalar estimate可为两pol明确聚合，但 receipt必须写 estimator ID与receiver-derived per-pol values。禁止把 `physical.complex_noise_power`、SNR变换值或其别名写入 Receiver/receipt；同 received/known input必须唯一复算。
6. Fail-closed：
   - recursive truth guard覆盖 Mapping/dataclass/standard containers、generic `__slots__`（含继承/单字符串slots/循环保护）及必要 `__dict__`；CodeLayout/WaveformLayout只按显式 allowlist跳过；nested event/fade/phase/payload/coded/final aliases拒绝。
   - `PhysicalCell` 严格 int（非bool）且有限合理；root严格 `0..2**63-1`；float等值 cell/oversize root拒绝。
   - 增加 exact frozen D0 contract identity guard并由 `build_views` 调用：schema/control、code `(BG2,1024,1536,16,384,6144,20)`、population modulation/pols/symbol rate/SNR/linewidth和全部 seed ranges不容 forged replace。
   - ReceiverView 校验 code/layout exact、registered N/total formula、received/equalized/phase/prefix/pilot shapes与numeric finiteness；TruthView校验payload shapes/binary、physical arrays同 `(2,Ntime)`/finite、noise samples shape/finite及 correctness pending/finalized状态。`dataclasses.replace` 不能绕过。
7. 更新所有旧 build_views fixtures显式提供 deterministic synthetic PayloadTruth；旧 WC04–07物理 oracles不弱化。测试 `information_bits_per_cw`合法 metadata仍通过；payload mutations不得改变 Receiver bytes/receipt。
8. 跑四新 nodes、CV01–05/09完整 contract file、WC01–08完整 waveform-channel、I02/I03相关 regressions；重放 step-135 23+5 mutations并新增 payload/finalizer至少12例。结构审计无 truth/value leak、无 global RNG、无 legacy/I/O。
9. 日志逐项 disposition P1-1/P1-2/P1-3/P2-1；若任何一项未闭，terminal INCOMPLETE，不得 READY。Windows固定命令；≤15分钟；无 benchmark/science/web/install/commit/push/stage。

## 返回

RED/GREEN、mutation counts、noise/payload/finalization receipts、五 SHA；terminal=`I06_READY_FOR_INDEPENDENT_REVERIFICATION`、`INCOMPLETE` 或 blocker。
