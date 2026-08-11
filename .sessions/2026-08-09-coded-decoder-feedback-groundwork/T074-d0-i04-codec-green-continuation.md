# Task Brief: D0 I04 codec GREEN continuation from valid RED

> 来源: step-118 `I04_INCOMPLETE_AT_RM07` / frozen RED test SHA / plan I04 | 产出位置: `projects/thesis-fso/worker-logs/step-120-d0-i04-codec-green-continuation.md`
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

- 假设：冻结的四个 valid RED nodes 可由一个 lazy、source-bound、PyTorch Sionna 2.0.1 `codec.py` 最小实现依序转 GREEN，且不修改测试或旧链。
- 否决条件：测试 SHA 漂移；必须 runtime import 旧 `p08*`；Sionna live BG/Z/interleaver 不符；正 LLR 语义/shape/fresh state 不能闭合；需 truth correction/skip/fallback；或 15 分钟到期，则停在最近一个完整 RM GREEN 边界，写 `INCOMPLETE`，不仓促放宽。

## 冻结输入与既有 RED

```text
test=38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef
step-118=cccdfb0d149fbd925918d68957dd487b6d30921d126146e8b219f04d92df4fc3
codec.py=ABSENT
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
p08r_chain=174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
RED_RM07=110375e54809bc793598a3ed1010610ff4c1a4e2e706fc157a86fd255b13d466
RED_RM08=59b9e3ee69f07023fd656182991fe0eac81bbf96b92bafbb19bc541b280f8de2
RED_RM09=8bc5495a0a00b129ba84bc4d5d232d29470efb2b706fb1b6eb3920f1afb4a52a
RED_RM10=a3b0bc4a51014bd8e1074d7dcdf42646d3528ffd7d062efbb72bcb6c88ba50c2
```

## 唯一允许写入

1. Create `projects/simulation/explore/coded-decoder-feedback/codec.py`
2. Create `projects/thesis-fso/worker-logs/step-120-d0-i04-codec-green-continuation.md`

`test_d0_receiver_codec_methods.py` 是冻结 oracle，禁止修改；step-118 只读。不得创建其他文件。

## 实现与验证

1. 先核所有冻结 SHA、production ABSENT、保护基线；完整读完 step-118 PENDING、owner、step-105、P08-R2 source 的 codec 语义。Sionna 2.0.1 是 PyTorch 路线，不再探 TensorFlow。
2. 最小实现按 RM07→RM08→RM09→RM10 顺序：
   - public Gray map/hard demap/four-state rotation/rotation-state，bit order `[b0,b1,b2,b3]`，axis exact；
   - `D0Codec` import/lifecycle lazy，无 import-I/O；live `LDPC5GEncoder(k=1024,n=1536,num_bits_per_symbol=4)` 与 fixed-20 `LDPC5GDecoder`；shape/sign/clipping validation；live metadata 从构造对象/source receipt 得出，猜测或不符即 FAIL；
   - encoder/backend object 可缓存；每 `decode_fresh` 显式 `message_state=None,warm_state=None`，不保存 decoder message；receipt=`cw_batch/restart/20*CW/truth_correction=False`；
   - exact re-encode NLL 与 single `complex_noise_power/2` helper。
3. 每完成一个 RM 节点立即以冻结 test 跑 exact node并写 GREEN output SHA/count/duration；若失败，用 systematic diagnosis，仅在 `codec.py` 内修根因。若证明测试与 owner/live API 冲突，返回 named `TEST_CONTRACT_BLOCKER`，不得修改 test。
4. 四节点 GREEN 后跑完整 `test_d0_receiver_codec_methods.py`，再跑现有 `test_d0_contract_views.py` 回归。记录 live version/BG/Z/interleaver、source/test SHA、无 skip/xfail/warning。
5. 终检只两个目标变化；p05 4/4、cache census、staging=0、HEAD 不变；无 legacy runtime import、benchmark/science/web/install、commit/push。

## 命令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider <exact node or file> -q
```

15 分钟硬上限。

## 返回

`PASS/FAIL/INCOMPLETE`；RM07–RM10 逐项 GREEN 状态；`codec.py`/step-120 SHA；live metadata/protection receipt；terminal=`I04_READY_FOR_INDEPENDENT_VERIFICATION`、`I04_INCOMPLETE_AT_RMxx` 或 named blocker。
