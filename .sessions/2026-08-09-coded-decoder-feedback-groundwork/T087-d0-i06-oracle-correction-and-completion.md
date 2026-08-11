# Task Brief: D0 I06 test-oracle correction and completion

> 来源: T084 / step-130 `INCOMPLETE_AT_WC06` / 主线程 test-oracle 裁决 | 产出位置: `projects/thesis-fso/worker-logs/step-133-d0-i06-oracle-correction-and-completion.md`
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

## Review disposition / evidence rule

- step-130 的四个 `channel.py=ABSENT` RED 仍是生产实现的历史 bootstrap RED；不得删除、改写或倒签。
- WC06 当前失败属于 test-oracle 假阳性：对整个 `ReceiverView repr` 搜索 `information_bits`，误命中 owner 允许的嵌套 `CodeLayout.information_bits_per_cw`。
- 本任务只把泄漏 oracle 收窄到 `ReceiverView` 的**直接字段名**和 `receipts` 对象图。修正后的 WC06 在当前生产代码上直接 GREEN 是预期结果，不得伪称或制造 superseding RED。
- 若 WC07 或新增的、真正不同的行为测试暴露 production 缺陷，才按 TDD 取得新 RED、先写 receipt，再修 production。

## 冻结输入

```text
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test_waveform_channel.py=ba5ebbacdeab3904554772fec70f3a4d73f1809f0a0d7f35ea8074c4201bd13a
step-130=7d787b55f12b84a654bd87c453669b8bd317f2da6cb2b02a1f2a267e1de706b7
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_waveform_channel.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/channel.py` **仅当 WC07 或负面测试取得真实 RED**
3. Create `projects/thesis-fso/worker-logs/step-133-d0-i06-oracle-correction-and-completion.md`

不得修改 contract/waveform/owner/legacy；不得创建 runner/artifact/result/cache。

## 执行要求

1. 完整读本任务、T084、step-130、owner 的 Receiver/Truth 字段契约与现有 test/channel；先核冻结 SHA、HEAD、三目标保护。
2. 仅修正 WC06 leakage oracle：
   - 从 dataclass/slots 等结构化接口取得 `ReceiverView` **直接字段名**；以下 direct truth fields 必须不存在：
     `information_bits,coded_bits,transmitted_symbols,true_phase,channel_h,physical_snr_db,fade,noise_receipt,event_label,final_codeword_correctness`。
   - 递归检查 `receiver.receipts` 的 mapping keys、dataclass/slots field names 与容器成员，拒绝上述 truth aliases；需要循环保护，不能只检查顶层。
   - 明确允许合法嵌套 `CodeLayout`/`WaveformLayout` 的元数据字段（包括 `information_bits_per_cw`），不得用 substring/repr oracle。
   - 不借机扩大 WC06 或隐藏生产字段；记录“oracle correction, no new RED expected”。
3. 用冻结 Windows 命令运行 corrected WC06；预期当前 production GREEN。若失败，先判定是否仍为 test defect；只有确认生产缺陷后才取得新 RED、先在 step-133 写精确 receipt 后改 channel。
4. 运行 WC07。核验：`tau=1/(2π100)`，`rho=exp(-100*Ts/tau)`；10k/20k/80k innovation variance=`2πΔνTs` 且 effective linewidth只计一次；theta[0] 是首个 innovation；AWGN per-real与complex power精确。若真实缺陷，严格 test-first/receipt-before-production。
5. 跑 WC04–WC07、完整 waveform-channel 文件（预期 9 tests）、I02 contract regression；增加/执行输入防御检查：root/cell/shape/nonfinite/contract identity fail closed，且 NamedStreams 的局部 RNG 不污染全局 RNG。
6. 对 sharing/truth split 做结构化终检：shared GG/Wiener bytes；独立 AWGN；supplied waveform 方程闭合；Receiver无 truth leakage；Truth承载真实量；arrays frozen/defensive；无 legacy runtime import/sys.path/I/O/import side effect。
7. step-133 必须区分：step-130 历史 RED、WC06 oracle 裁决、是否产生任何新 production RED、所有命令/count/output/SHA/保护检查。不得把测试修正伪写成 production repair。
8. 使用：
   `$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'`
   `C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...`
9. ≤15 分钟；不 benchmark/science/web/install/commit/push/stage。到时按 test-ID boundary 停止并返回 INCOMPLETE。

## 返回

WC06 corrected、WC07、WC04–07、full、I02 与负面测试 counts；生产是否修改；source/test/log SHA；terminal=`I06_READY_FOR_INDEPENDENT_VERIFICATION`、`INCOMPLETE_AT_WCxx` 或 blocker。
