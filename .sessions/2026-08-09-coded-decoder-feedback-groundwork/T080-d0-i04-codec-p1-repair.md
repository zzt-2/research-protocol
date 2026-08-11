# Task Brief: D0 I04 P1 repair — contract/output/noise fail-closed gates

> 来源: step-122 independent FAIL P1-1/P1-2/P1-3 | 产出位置: `projects/thesis-fso/worker-logs/step-126-d0-i04-codec-p1-repair.md`
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

## Review disposition / 否决条件

- 接受 P1-1：只核 1024/1536/20 无法证明 schema/epoch/CP/D/V/science-deny identity。
- 接受 P1-2：shape 正确但值为 2/0.5/NaN 的 backend 输出不是 hard information bits，cast 前必须拒绝。
- 接受 P1-3：Python/NumPy bool 不得充当物理噪声功率。
- 接受 verifier 对 repeated NLL 1 ULP 的非缺陷裁定，不为它改 reduction。
- 否决条件：改 contract/owner/旧链；修改 LLR/LDPC science semantics；用 test-only分支；或 15 分钟不收敛。

## 冻结输入

```text
codec.py=1f03b278054cb380c73b98e5211c0c5a37b41d2c47d5966f50bc5803d4e74dcb
test=38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef
step-122=2517832d5d31a84ff251bc1520e58b21b49143b825c655c28b23986130064247
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
step-120=1b79aad9be86027d6fef91ad9e9a3931bce0bf53aa7e6cbd86f8f9a1c13ab1b4
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/tests/test_d0_receiver_codec_methods.py`
2. Modify `projects/simulation/explore/coded-decoder-feedback/codec.py`
3. Create `projects/thesis-fso/worker-logs/step-126-d0-i04-codec-p1-repair.md`

## Test-first repair

1. production 前追加三个 exact tests：
   - `test_codec_rejects_wrong_contract_identity`：dataclasses.replace 分别 mutation schema、epoch、checkpoint、decision、verification、execution/science deny；matching code integers仍应拒绝。
   - `test_codec_rejects_nonbinary_backend_output`：shape `[1,1024]` 但 2、0.5、NaN、object/structured；均在 cast 前拒绝；合法 bool/int/float 0/1 可接受。
   - `test_codec_rejects_boolean_noise_power`：Python bool 与 `np.bool_` 拒绝；finite nonnegative real numeric仍按 `/2`。
2. 以 old production 跑三个新 nodes，取得目标 RED 并记录新 test/source/output SHA。说明新 file SHA 的 RED supersedes 旧 file-level receipt；原 RM07–10 tests 保持原文。
3. 最小 GREEN：
   - import/use `contract` 的 exact D0 type + frozen identity/action validator，构造 backend前验证 schema/epoch/CP012/D011/V005、execution/science false及 owner code identity；不重复漂移另一套模糊规则。
   - decoder raw output先检查 plain numeric/bool ndarray、shape、finite、所有值 `{0,1}`，再转 uint8；object/structured/non-numeric fail closed。
   - `per_real_noise_power` 在 float conversion 前拒绝 bool/np.bool_；保持 zero helper合法、demap zero仍拒绝。
4. 跑三个 new GREEN、原 RM07–10、full codec、I02 regression和 fresh import probe；无 skip/xfail/warning；不改变 NLL/LLR/Sionna metadata/state semantics。
5. 终检只三目标变化；p05/cache/staging/HEAD；不 benchmark/science/web/install/commit/push。≤15 分钟。

## 返回

RED/GREEN、full regression counts、三目标 SHA；terminal=`I04_REPAIR_READY_FOR_REVERIFICATION`、`INCOMPLETE` 或 named blocker。
