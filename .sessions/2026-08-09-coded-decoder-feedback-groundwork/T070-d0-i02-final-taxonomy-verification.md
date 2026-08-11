# Task Brief: D0 I02 iteration-2 final fresh taxonomy verification

> 来源: step-115 / S001 mandatory exit / I02 iteration-2 candidate | 产出位置: `projects/thesis-fso/worker-logs/step-116-d0-i02-final-taxonomy-verification.md`
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

## Hypothesis / mandatory terminal

- 假设：iteration 2 已把 owner forbidden 四类转成组合 taxonomy，并闭合 I02。
- 若任何 owner-equivalent generated case通过：`FAIL / DENYLIST_ROUTE_REJECTED / NEXT=TYPED_ALLOWLIST_REDESIGN`，不得建议第四轮词表补丁。
- 若 generated forbidden 全拒、safe controls全收、6 tests/immutability/action全部通过：`PASS / I02_VERIFIED_READY_FOR_BATCH1`。

## 冻结输入

```text
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
test=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
step-115=1fc7ef00bc03ce13f0d62ea60ea17508eea4a41541599ae11a56798c906b0695
step-114=505dc4bc42f37d880e954a85ddc93ef7b085b2718551893aa302c6f11b4f4324
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## Fresh verification

1. 完整读 T070、S001 counter、T065/T069、step114/115、owner views、candidate/tests；核 hashes/protection。
2. fresh完整 pytest：6 passed，0 skip/xfail/warning。
3. 生成而非手列一小撮的 OS-inline matrix（不写 repo），每个 semantic base 至少 snake/UPPER/hyphen/dot 四种 normalization：
   - TX：payload；`{info,information}×{bit,bits}`；`coded×{bit,bits}`；`data×{symbol,symbols}`；`{tx,transmitted}×{bit,bits,info,information,coded,data,symbol,symbols,payload}`。
   - physical：snr/cfo/fade with prefixes/suffixes；exact h；`channel×{true,physical,actual,oracle,realization,gain,coefficient,response,state,fade,h}`；`phase×{truth,true,physical,channel,oracle,actual}`。
   - event：slip/event with label/boundary/rotation；`{injected,injection,natural}×{label,fixture,boundary,rotation,event}`。
   - correctness：correct/correctness；`final×{cw,codeword,frame,bit,bits}×{error,errors,status,correct,correctness}`。
   每个 key 放在至少三层 nested mapping 后构造 ReceiverView；任何 accepted row列明。
4. Object/structured/non-numeric ndarray拒绝；plain numeric/bool defensive-copy/read-only。嵌入 TruthView拒绝。
5. safe controls逐项 nested 接受：`received_samples`, `equalized_samples`, `known_prefix`, `periodic_pilots`, `receiver_noise_estimate`, `common_cpr_phase_trace`, `global_rotation_state`, `bps_state`, `source_sha256`, `code_sha256`, `content_sha256`, `channel_source_sha256`。不得只调用 private predicate，必须走真实 ReceiverView constructor。
6. action exact five、five-minus-one、identity/science拒绝；CV06–08 absent；no import-I/O/runner/scope drift。
7. 给 step112 P1-1/2/3 与 step114 P1-1 最终 disposition；终检 only step116、p05/cache/staging/HEAD。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-116-d0-i02-final-taxonomy-verification.md`；不得修 candidate/test。
- Windows Python `-B` / no-cache/no-bytecode；禁止 benchmark/science/web/search/download/commit/push。
- 目标 10 分钟，15 分钟硬上限。
- 返回 verdict/P0P1P2、generated counts、terminal、log SHA/protection。
