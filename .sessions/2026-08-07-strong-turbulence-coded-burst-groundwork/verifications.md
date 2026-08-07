# Verifications — 低仰角强湍流 coded-burst reliability Groundwork

## V001: Step 1 terminal 与证据闭合独立验证

> date: 2026-08-07
> 关联：S001 / D002 / R005

### 验证项

- [x] 启动身份：独立 verifier 重算 HEAD 为 `12c54b3409dcc46c3bf4bf202380a38eae069562` → PASS。
- [x] query receipt：2 组本地 query + 4 组固定 JSON，无第 7 组 → PASS。
- [x] JSON count/SHA：20/7/20/0，四项 SHA256 与 R004 一致 → PASS。
- [x] 检索源门：四 JSON 仅 S2+OpenAlex，本地全文不能冒充第三 API → 正确记录为未过。
- [x] physical-support：大天顶角强起伏/GG 有推导，但 target occurrence+threshold-conditioned AFD 未闭合 → PASS。
- [x] baseline coverage：2019+ strict task-matched baseline=1，不是 0，也未达到 2 → PASS。
- [x] testbed BOM：lifecycle=PARTIAL、controllability=NO、schema=PARTIAL、metric=NO 有源码支持 → PASS。
- [x] outage 语义：target oracle/AFD/weak-block count 仍 UNKNOWN，没有误判为 outage terminal → PASS。
- [x] Step 2：无 papers 变化、5 个 CORE 候选目录不存在、无 coded-chain 新结果 → PASS（未执行）。
- [x] forbidden paths：`common/`、`params.py`、旧 raw/result、Skill、四个 `p05_run*.log` 未改 → PASS。
- [x] terminal alternatives：排除 `OUTAGE_NOT_INTERLEAVING_PROBLEM`、`NO_2019_PLUS_TASK_MATCHED_BASELINE`、`TESTBED_SCOPE_EXCESSIVE` → PASS。
- [x] 治理一致性：registry/topic/master-state 均为 closed/Step 1 evidence insufficient/Step 2 not run → PASS。

### 证据

```text
fresh verifier: ACCEPT; blocker=0
HEAD: 12c54b3409dcc46c3bf4bf202380a38eae069562
JSON counts: 20 / 7 / 20 / 0
strict 2019+ task-matched baseline: 1
terminal: STEP1_EVIDENCE_INSUFFICIENT

coded-fso-correlated-interleaving.json
  ac06590665000c45e31c73aa580274f3982d05dfd0d50a63033cf97f31f94972
coded-fso-channel-aware-mapping.json
  e29f269e4ab22623eea5cd28a283e50737209fa7ab2c2decb23debbe5d36f932
coded-fso-parity-placement.json
  37a3988ea807251e63995ed53b4f7ee176de0cc0fdb289b6835b1a6ca6f86232
coded-fso-recent-baselines.json
  c40794548a87b0d37a0b2c509ba2f77dbaf5e6e0f4b04f317b725f10da5f7747

source-level spot checks: 13
acceptance checks: 14/14 PASS
forbidden-path changes: 0
Step 2 acquisitions: 0
```

完整独立复算与 13 条原始事实见 R005。

### 结论

PASS

### 后续（FAIL/PARTIAL 时）

无。科学 terminal 已闭合；新证据只能触发 Step 1 缺口补证，不能直接进入 Step 2。
