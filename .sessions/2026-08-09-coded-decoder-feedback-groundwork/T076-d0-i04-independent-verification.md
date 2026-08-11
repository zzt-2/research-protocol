# Task Brief: D0 I04 independent codec verification

> 来源: step-120 executor PASS / frozen I04 source+test | 产出位置: `projects/thesis-fso/worker-logs/step-122-d0-i04-independent-verification.md`
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

## 审查问题 / fail 条件

- 问题：独立上下文能否从 owner/source/live API 证明 I04 不是仅对四个 happy-path tests 过拟合，并且 Gray/LLR/LDPC/state/receipt/import 边界全部闭合？
- FAIL：任何 P0/P1；测试 SHA 漂移；metadata 只是无验证硬编码；legacy runtime import/import side effect；decode state 复用；shape/sign/non-finite/binary/identity fail-open；或新鲜 unit/regression 不全 GREEN。P2 可列但不得隐瞒。

## 冻结输入

```text
codec.py=1f03b278054cb380c73b98e5211c0c5a37b41d2c47d5966f50bc5803d4e74dcb
test=38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef
step-118=cccdfb0d149fbd925918d68957dd487b6d30921d126146e8b219f04d92df4fc3
step-120=1b79aad9be86027d6fef91ad9e9a3931bce0bf53aa7e6cbd86f8f9a1c13ab1b4
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
p08r_chain=174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

Create only `projects/thesis-fso/worker-logs/step-122-d0-i04-independent-verification.md`。production/tests/step-118/120 只读；不得修复。

## 独立验证

1. 先核冻结 SHA、branch/HEAD/staging/p05/cache；读 owner、step-094/105/106、P08-R2 source、codec/test/log。不要采信 executor 结论，按 P0/P1/P2 findings-first 审查。
2. fresh import-side-effect probe：新进程 import `codec` 前后检查 `sionna`/legacy modules、filesystem/cache；Sionna 必须保持未加载，legacy 永不加载，无 global path/I/O。
3. fresh 执行四 exact nodes、完整 I04 文件、I02 回归。记录 exact commands、exit/count/duration/output SHA、skip/xfail/warning。
4. 用临时 one-shot Python/pytest（不得落 repo 文件）做 owner 驱动负面矩阵，至少覆盖：
   - 16 labels roundtrip/four rotations；invalid state、shape mismatch、ambiguous zero reference 拒绝；
   - live 1024→1536→1024，BG2/Z104/1536 interleaver inverse；source inspection 判断 metadata receipt 是否实证而非纯字符串；
   - wrong contract identity、info/LLR shape、nonbinary info/coded backend、nonfinite LLR、duplicate/mismatched CW ids、empty candidate、invalid noise power fail closed；
   - counting backend 连续调用始终 `(None,None)`；坏 backend shape/binary output 被拒绝；receipt batch/restart/BP iterations/truth=false exact；
   - demap positive-for-bit1、preclip30/decoder clamp20、per-real variance只转换一次；NLL repeated same-bit denominator invariant。
5. 静态扫描 forbidden runtime legacy imports、truth correction、warm/message cache、import I/O、skip/fallback。区分“test 未覆盖但实现正确”和真实缺陷；每个 finding 给 owner oracle、复现证据和最小修复方向。
6. 终检只 verifier log 新增；保护项不变；不 benchmark/science/web/install/commit/push。15 分钟硬上限，时间不足返回 `INCOMPLETE` 而非 PASS。

## 返回

P0/P1/P2 counts；fresh test/negative counts；log SHA；terminal=`I04_VERIFIED_READY_FOR_BATCH1`、`I04_VERIFICATION_FAIL` 或 `INCOMPLETE`。
