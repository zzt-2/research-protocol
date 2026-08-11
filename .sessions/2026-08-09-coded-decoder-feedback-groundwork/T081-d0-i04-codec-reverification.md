# Task Brief: D0 I04 independent codec reverification after P1 repair

> 来源: step-122 FAIL + step-126 process-deviation repair | 产出位置: `projects/thesis-fso/worker-logs/step-127-d0-i04-codec-reverification.md`
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

## 审查问题

独立证明 step-122 三个 P1 已根治且 RM07–10 无回归；同时诚实裁定 step-126 late receipt：不得把它称为 receipt-before-production，但 step-122 的独立旧-source frozen reproduction 可作为 pre-repair RED 锚点。若代码证据 PASS，terminal 中仍要显式写明 process deviation 如何被外部 RED + 本轮 independent GREEN 补偿闭环。

## 冻结输入

```text
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
test=4045a68843400518c999db836533528c1452af9c5f8b9e940c2fd24b24b90348
step-122=2517832d5d31a84ff251bc1520e58b21b49143b825c655c28b23986130064247
step-126=e9fcc41c2bb65a5ae904069f2a5b067734cb9adac08bdeca3a4115b41fa8f313
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

Create only `projects/thesis-fso/worker-logs/step-127-d0-i04-codec-reverification.md`；source/tests/logs只读，不修复。

## Fresh reverify

1. 核 SHA/保护并逐项重放 step-122 repro：schema/epoch/CP/D/V/execution/science mutation；backend outputs 2/0.5/NaN/object/structured/wrong shape；Python+NumPy bool noise。合法 0/1 bool/int/float、finite powers保持通过。
2. fresh 跑三个 repair nodes、RM07–10 exact、full codec file、I02 regression；记录 counts/duration/output SHA，无 skip/xfail/warning。
3. 重跑 import/lazy Sionna、live BG2/Z104/interleaver、state reset/receipts、LLR/NLL/noise one-conversion negative matrix。静态检查修复是否复用 contract frozen validator，是否引入 test-only分支/legacy import/I/O。
4. Findings-first P0/P1/P2。任何 step-122 repro仍接受、回归、或新 P1 => FAIL。1 ULP NLL 不重开。
5. 证据裁定：明确列 `step-126 receipt timing=late`；不得改写历史。只有 `step-122 independent pre-repair RED` + 本轮 `independent post-repair GREEN/negative` 都完整，才可标 deviation compensated；否则 FAIL/INCOMPLETE。
6. 终检只 step-127；p05/cache/staging/HEAD；不 benchmark/science/web/install/commit/push。≤15 分钟。

## 返回

P0/P1/P2、fresh counts、deviation disposition、log SHA；terminal=`I04_VERIFIED_READY_FOR_BATCH1_WITH_RECORDED_PROCESS_DEVIATION`、`I04_VERIFICATION_FAIL` 或 `INCOMPLETE`。
