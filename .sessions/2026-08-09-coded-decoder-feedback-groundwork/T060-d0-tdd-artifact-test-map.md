# Task Brief: D0 v3 TDD、artifact 与 benchmark test map

> 来源: D011 / V005 / H004 / step-096→103 | 产出位置: `projects/thesis-fso/worker-logs/step-106-d0-tdd-artifact-test-map.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：v3 的 physical/B2/stat/dev-freeze/artifact 合同可全部转成 deterministic/unit/roundtrip/hash/chronology tests，且 12 分钟 benchmark 可与 scientific S1–S4 完全隔离。
- 否决条件：任一冻结 invariant 没有可自动判定 oracle；测试需要 TruthView 泄漏到 receiver；freeze winner 依赖顺序相关 float sum；test path 可 refit；benchmark 必须用 scientific seed/estimand；或测试总线无法分成单个 ≤15 分钟批次，则标 BLOCKER。

## 任务

1. 完整读取 v3 owner 的 physical realization、B2 implementation、statistical contract、dev-freeze artifact、S4 和 runtime throughput gate；完整读取 step-096/097/099/101/102/103、H004、`code-quality.md` 与现有相关 tests/verify templates。
2. 设计 `projects/simulation/tests/test_d0_*.py` 的精确文件名与 test-case 清单；每项列输入 fixture、断言/oracle、预期 RED 原因、对应 owner 路径、预计耗时。
3. 必须覆盖：immutable Receiver/Truth；registered prefix/pilot hashes；GG/Wiener/AWGN SeedSequence；RSS/31；legal 4-state BPS；mapping/rotation metamorphic；LDPC fresh restart；B1 exact NLL；B2 factor-2/Dirac/no-epsilon/state permutation/rotation covariance/uniform-state identities；raw schema；lossless binary64 aggregates；seven artifacts；five+five+one freeze；test chronology/no-refit；atomic write/receipt；cost ledger。
4. 设计 RED→GREEN receipt 规则，避免“先实现后补测试”；列每个测试批的命令、环境变量、no-cache/no-pyc 约束和 ≤15 分钟分批点。
5. 单列 12 分钟非科学 benchmark 的 fixtures、watchdog、decoder batch `{4,8,12,16}`、六格 BPS、B2 ten-view、HMM chunk、I/O receipt、PASS/FAIL projection 与不得触及的 scientific seeds/estimands。
6. 给出最小独立 code-review checklist，重点检查 truth leakage、message-state reuse、cache偷减 exposure、ordinary float sum、test-time refit 和 common edits。
7. 输出 `TDD_TEST_MAP_READY / BLOCKED`；不得创建测试/源码/plan owner，不得运行 pytest或 benchmark。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-106-d0-tdd-artifact-test-map.md`。
- 只读源码/文档；禁止 pytest、import 项目执行、D0/benchmark/science、web/search/download、owner/治理/源码修改、commit/push、p05/pycache触碰。
- 10 分钟目标，15 分钟硬上限。
