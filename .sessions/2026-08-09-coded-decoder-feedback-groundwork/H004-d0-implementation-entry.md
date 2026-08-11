# Handoff: D0 v3 只进入实现、单测与工程吞吐门

> 来源: S001 | 交接目标: 按 D011/V005/CP012 实现并验证 v3 D0 shell；不得运行 S1–S4 科学诊断
> 日期: 2026-08-10
> 文件名: H004-d0-implementation-entry.md
> 当前 handoff: 是；取代 H003 的当前入口地位，H003 作为 CP011 历史保留

## 已完成边界

A0/A′/A/B scientific contract 已由 step-091 `PASS 0/0/0` 接收。其后的资产闭合链为：step-094–100 完成 coded-chain/source/physical/B2/stat/budget 映射；step-101 对 v2 给出 `FAIL 0/2/0`；step-102 给出不重开 scientific fields 的 additive repair；step-103 对 v3 给出 `PASS 0/0/0`、两项 P1 CLOSED、`94/94` 静态断言 PASS，终态为 `ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER`。

D011/V005/CP012 接收的是实现前静态合同，只开放 `D0_TESTBED_IMPLEMENTATION`、`D0_UNIT_TEST`、`ENGINEERING_THROUGHPUT_BENCHMARK`、`SOURCE_AUDIT`、`CONTRACT_STATIC_CHECK`。当前 D0=`NOT_RUN`、method signal=`NONE`、`>7D_HARD_BLOCKER=NOT_ESTABLISHED`；没有 scientific raw rows、aggregate、CI 或 gate verdict。

## 不要做什么

1. 不运行 `DEFECT_SMOKE`、S1–S4、任何 scientific seed 或 scientific estimand；工程 benchmark 不能用缩小的科学批次冒充。
2. 不建设 adapter/C1 policy、trigger、accept/reject、fallback、applied local action、MVE、held-out、Contract/Execute 或论文声称。
3. 不修改 `common/`、旧 P08/P08-R/P08-R2 资产或四个 protected `p05_run*.log`；不暂存 p05，不 push。
4. 不删除 seed/cell/tuple/grid/fixture/candidate、改 threshold/gate 或复用 decoder message state来挤预算。
5. 不覆盖 step-101 `FAIL 0/2/0` 历史；step-103 PASS 只关闭资产合同 P1，不是 scientific PASS。

## 必读

1. `.sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md` 的 CP012 控制块、范围边界与不变量。
2. `.sessions/2026-08-09-coded-decoder-feedback-groundwork/decisions.md` D011 与 `verifications.md` V005。
3. `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml` v3（唯一机器 owner）与 `d0-asset-preflight.md`。
4. `projects/thesis-fso/worker-logs/step-101-d0-asset-contract-verifier.md`、`step-102-d0-dev-freeze-artifact-audit.md`、`step-103-d0-dev-freeze-reverifier.md`。
5. `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md`；`stages/groundwork.md`、`stages/gw-feasibility.md`、`domain-comms.md`、`code-quality.md`、`thesis-lessons.md` 与 `reference/sim-template/` 对应模板。

## 接口变更（如有代码改动）

尚无代码改动；以下为 v3 必须实现的冻结接口：

```yaml
control:
  epoch: 12
  checkpoint: CP012
  decision: D011
  verification: V005
  implementation_authorized: true
  unit_test_authorized: true
  engineering_benchmark_authorized: true
  execution_authorized: false
  scientific_experiment_authorized: false
required_dev_freeze_artifacts:
  - dev_manifest.json
  - raw_bps_dev.jsonl
  - hmm_grid_dev_chunks.jsonl
  - raw_b2_tuple_clean_dev.jsonl
  - raw_b2_tuple_controlled_dev.jsonl
  - dev_freeze.json
  - dev_freeze_receipt.json
freeze_cardinality:
  bps_pairs: 5
  statistic_pairs: 5
  final_b2_tuple: 1
test_path:
  fit_functions_reachable: false
implementation_root: projects/simulation/explore/coded-decoder-feedback/
test_glob: projects/simulation/tests/test_d0_*.py
common_edits: forbidden
```

## 失败数据附录（如涉及路线失败）

- step-101=`FAIL / P0/P1/P2=0/2/0`：P1-1 HMM clean/controlled likelihood-fit 权重不唯一；P1-2 BPS/B2 dev-freeze 缺具名 typed、可复算 artifacts。不是 scientific failure。
- step-102=`MINIMAL_ADDITIVE_REPAIR_REQUIRED / NO_SCIENTIFIC_REOPEN`。
- step-103=`PASS / P0/P1/P2=0/0/0`：两项 P1 CLOSED，`SCIENTIFIC_FIELD_DRIFT=NONE_FOUND_IN_CHECKED_FAMILIES`。
- pre-transfer SHA256：owner `6924842c5696e80bcf8efa24bc63f005d7a78ba63f959c768e0183de85c81f54`；asset report `e008c0f0b78772a80201d4969359ed34d655d79ed37614652746e911ebbc01f1`；step-103 `6ad845f009a64c0a5d93671bf98354a17a1dd83cf3882aecaa43f5e7f73a5ab9`。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| v3 七个 artifacts 尚未存在 | 每个 dev selection 必须 typed、可复算、hash-bound | CONTRACT_ACCEPTED / CODE_NOT_WRITTEN | TDD 实现、schema/roundtrip/hash/chronology tests PASS |
| truth-separated shell 尚未存在 | ReceiverView 与 TruthView 必须 immutable 隔离 | DESIGN_FROZEN / CODE_NOT_WRITTEN | deterministic leakage/identity/metamorphic tests PASS |
| B2 source transfer 尚未运行 | OFC17-like pilot state→16QAM LLR→one-way LDPC 必须逐项复刻 | CONTRACT_FROZEN / CODE_NOT_RUN | source/math/unit tests + independent code review PASS |
| 4.50 日 D0 点估计未实测 | 必要工作加 contingency 必须守 7 日硬上限 | BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK | 12 分钟工程吞吐门给出投影；超限且允许优化不能解除则 blocker |
| S1–S4 scientific UNKNOWN | 只有冻结 scientific run 能关闭 A0 fatal | NOT_RUN / NOT_AUTHORIZED | 工程四门 PASS 后另立 D/V/CP |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| v3 静态资产合同 | 两项 step-101 P1 CLOSED；duplicate-key parse；scientific no-drift | step-103 / V005 | `PASS 0/0/0`，94/94 |
| deterministic/unit gates | Receiver/Truth 隔离、mapping/rotation、LDPC fresh restart、BPS 六格、B2 factor-2/Dirac/state/covariance、artifact exact aggregate/freeze chronology 全部 PASS | v3 owner + step-099/102 | N/A（未实现） |
| 独立代码审查 | P0/P1=0；所有 P2 有明确处置；no common/p05/science drift | D011 / P6 分离审查 | N/A |
| 12 分钟非科学吞吐门 | 覆盖 decoder batch `{4,8,12,16}`、六格 BPS、一个 B2 ten-view slice、一个 HMM grid chunk、atomic JSONL/receipt；完整必要工作+已记工程时间投影≤7日 | v3 `engineering_budget_days.runtime_throughput_gate` | N/A |
| scientific S1–S4 | 当前不适用；禁止运行 | D011/CP012 | N/A（NOT_RUN） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称（列出验证了哪些）
- [ ] 已检查 `_registry.yaml` 中本专题的 `depends_on` 和 `conflicts_with`
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

先写 `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-implementation-plan.md`，由独立 reviewer 审查任务依赖、RED→GREEN 证据、文件边界与 scientific no-run 边界。计划 PASS 后，按 TDD 分块实现 contract/types → waveform/channel/BPS → coded chain/B0/B1/O1 → typed artifact/dev-freeze/statistics → B2 → runner/verification integration。实现与单测通过后另派独立 code reviewer；只有 reviewer PASS 才运行 12 分钟非科学吞吐门。工程四门全部 PASS 后再立新的 D/V/CP，届时才能讨论 S1–S4。
