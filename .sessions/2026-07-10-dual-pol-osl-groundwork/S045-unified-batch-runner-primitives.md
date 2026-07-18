# [S045] 统一 Batch runner 事件/指标原语

> 2026-07-16 | Batch 0.5 实施 | PASS

## 目标

按 S044 的准入合同建立统一 Batch runner 最小基建，先闭合参数签名、共享 realization 调用边界、fade 事件字段与双流 fixed/PI 指标；不启动新方法长实验。

## 记录

在隔离 worktree `.worktrees/unified-batch-runner`（branch `codex/unified-batch-runner`）中以 TDD 新增：

- `projects/simulation/common/_batch_events.py`：多 fade 提取、恢复窗口起点、右删失、block→symbol 显式映射；channel fade 关闭不伪造 BER recovery，`recovery_symbol` 留给 method-aware evaluator。
- `projects/simulation/common/_batch_metrics.py`：双流 fixed-label BER 与 PI-BER 分离；PI 遍历 2! 个流排列及两流各 4 个 QPSK 相位，保存 assignment/phase。
- `projects/simulation/explore/cma-fade-divergence/batch_runner.py`：显式 `BatchConfig`、有限数校验、SHA-256 `config_signature`、单次 shared realization factory 与结果 metadata。
- `projects/simulation/tests/test_batch_events_metrics.py`：覆盖多事件、右删失、symbol 字段、相位/排列、配置冻结和单 realization 调用。

定向回归最终为 `95 passed in 13.71s`（`test_batch_events_metrics.py` + `test_common.py` + `test_prompt015_unified_baseline.py`）。独立复核先后发现并促成：恢复边界偏移、缺 symbol schema/finite 校验、channel recovery 冒充 BER recovery、缺 method-aware recovery、shared ID 未含配置签名。等价性门首次 RED 又暴露新 fixed-label BER 未沿用 prompt012 每流 QPSK 相位校正；修正后，同 seed canonical/legacy channel 六数组逐元素完全一致，fixed/PI 终态口径一致。旧 `params.py`、历史 runner 和结果未改。worktree 中另有两项用户既有 SVG 修改，不属于本轮。

canonical `generate_shared_realization_dp()` 单次调用、`save_results()` seam、Godard-with-z callable 声明门、method-aware recovery 与旧 baseline 等价性已接入。随后补齐统一 `cma_block` 窗口网格和每方法 fixed/PI/assignment/swap/fade/divergence/recovery/censor 输出；`standard_cma_adapter` 真实调用 prompt013 `mode="standard"` 并显式传入冻结参数。512-symbol canonical+standard-CMA+实际保存端到端 smoke 通过，总定向回归更新为 99 项。是否达到 Batch 1 首个小批准入，以 V006 最终独立逐条审查为准；正式长跑仍不得自动启动。

## 决策引用

- D045：候选族先地图，再批量排跑。
- 无新决策；本轮实现 S044 已决定的准入基建。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

V006 已逐条 PASS。下一步只准入 Batch 1 首个短序列/少 seed 小批；先验证新方法输出 schema 和事件，再决定是否扩大 paired seeds，不能直接长跑。
