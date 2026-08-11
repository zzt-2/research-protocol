# Task Brief: D0 I02 fresh independent verification

> 来源: T065 / step-111 / I02 candidate | 产出位置: `projects/thesis-fso/worker-logs/step-112-d0-i02-independent-verification.md`
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

## Hypothesis / 否决条件

- 假设：I02 candidate 真实闭合 immutable/disjoint/recursive truth denylist 和 exact CP012 action set，无未测试的等价 truth alias 或 mutable-object ndarray 旁路。
- 否决条件：fresh 6 tests 非全绿；source/nested state仍可变；Receiver 能通过 `payload/payload_bits/snr_db/channel_gain/phase_truth/cfo/slip_rotation/final_cw_correctness` 等 owner-equivalent alias；object/structured ndarray 可藏 mutable truth；`TruthView` 可嵌入 safe key；allowed CPR/SHA 被误杀；action/identity mutation fail-open；或范围/保护漂移，均 FAIL。

## 冻结输入

```text
contract.py=be3ede121a7434e432b41f5ebd5b5794cbb106b1010e2ed922cc19ca18c90797
test=c248cda3a2a3623ef0807d9cc11c40010663869fd3b43aa6700b728380d27437
step-111=17bc5ac48d2350826ee6b40a43e291bfa54a633d3127086b956730d07ce9a2d0
step-110=efbb860af0711228e9e15f5918ab16e0071d51f0e7bdb19eeb3d0ed4f91f8760
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 任务

1. 完整读取 T066、plan I02、step-105/106 CV04/05/09、owner views/control、candidate/test/step-111；核 hashes/protection。
2. 静态审 dataclass fields/types、deep-freeze implementation、recursive cycle handling、truth alias normalization、action identity/permission logic、import-I/O/scope；明确指出“test green但 owner-equivalent alias未覆盖”的差距。
3. fresh run完整测试文件，要求 6 passed、0 skip/xfail/warning。
4. 在 OS temp/inline process 运行 mutation matrix，不写 repo：
   - existing exact aliases 与等价 aliases `payload`, `payload_bits`, `tx_information_bits`, `snr_db`, `channel_gain`, `phase_truth`, `cfo`, `slip_rotation`, `final_cw_correctness` 作为任意深 nested mapping keys，均必须拒绝；若某个不能由 owner forbidden category推出，须逐项说明而非放宽整组。
   - `TruthView` under a benign mapping key 必须拒绝。
   - object-dtype/structured ndarray 内嵌 `{"true_phase": ...}` 或 mutable list：必须拒绝或被真正递归 immutable copy；只把 container `writeable=False` 但内部对象仍可变视为 FAIL。
   - source ndarray/list/dict 改动不影响 stored；stored numeric arrays不可写；mapping/list/set/dataclass nested immutable。
   - `common_cpr_phase_trace`, `source_sha256`, `code_sha256`, `content_sha256` 必须接受。
   - exact five engineering actions accept；scientific/unknown及 CP/D/V/epoch/permission mutation reject。
5. 重建 TDD receipt内部一致性，保持证据等级克制；终检冻结 SHA、只新增 step112、p05/cache/staging/HEAD。

## 命令/边界

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
& 'C:\Users\zzt\scoop\apps\python311\current\python.exe' -B -m pytest -p no:cacheprovider 'projects/simulation/tests/test_d0_contract_views.py' -q
```

- 只写 `projects/thesis-fso/worker-logs/step-112-d0-i02-independent-verification.md`；不得修 code/test。
- 禁止 benchmark/science、web/search/download、commit/push、p05/cache修改。
- 目标 8 分钟，15 分钟硬上限。
- 返回 `PASS/FAIL/INCOMPLETE, P0/P1/P2`；只有 `0/0/0` 可写 `I02_VERIFIED_READY_FOR_BATCH1`。
