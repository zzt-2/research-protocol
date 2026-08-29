# Task Brief: 独立验证 Ch4 gated-RDE 有界开发

> 来源: S028 / D046 / T052–T053 / T056 / T058 / T059 | 产出位置: `projects/thesis-fso/polarization-demux-groundwork/step4a-c4-2-development-verification.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 8
  action_class: INDEPENDENT_SCIENTIFIC_VERIFICATION
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 T059 已集成的 Ch4 C4-2 gated-RDE bounded-development 包做独立科学验证。只审 correctness、公平性、统计重算和预注册停机判断；不得修改实现，不得重跑五分钟 development matrix，不得读取 `54301+` confirmation seeds，不得补第三轮/第三种 gate，不得轮换候选或写论文正文。

## 必读与启动门

1. 先运行 task-control validator；读取本 brief、D046、T052 §4.1、T056 §7、T059。
2. 读取 `core.py`、`run_development.py`、`development_manifest.yaml`、raw/aggregate/receipt/report、correctness smoke receipt 和两份 Ch4 tests。
3. 本任务触发 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`verification-before-completion`。只允许新增指定验证报告与必要 usage log；不得改任何研究实现或结果文件。

## 必须独立回答

1. Manifest 是否严格冻结 D1–D3、D4–D6、payload、block、tune/eval/confirmation seed firewall；raw 最大 seed 是否确为 54206，Round 2 是否确实未生成。
2. `B0*=min(LS-only,tuned plain)` 是否逐 cell 正确；各 arm 是否共享 symbol/Jones/noise realization hash；tune split 是否与 eval split隔离。
3. canonical RDE radius、cheap/candidate/oracle gate、truth firewall 是否与 T059 一致；oracle 是否只决定 gate，不进入 deployable update radius/step/tuning。
4. `wrong_ring` 是否由 predicted ring 与 truth ring 定义，ring/decision/combined AUROC 标签是否正确；D2 无 wrong-ring 正样本时 N/A 是否合法。
5. count-matched arm 是否按每 256 symbols、每偏振实际 accepted count 抽取，复用对应 gated `mu`；从 raw 独立核对至少全部 3 cells × 6 eval seeds的计数相等。
6. 从 raw 独立重算每个 arm 的 error/total/Jeffreys BER、candidate/cheap 相对 B0*、oracle headroom、paired wins、AUROC 聚合和 Round-1 decision；不得只相信 aggregate/report。
7. 三格是否均非 UNDERPOWERED；`winner=none`、`D/STOP_NO_METHOD_SIGNAL`、`NO_ORACLE_HEADROOM` 与 `NO_PREREGISTERED_GATE_SIGNAL` 是否是冻结规则的唯一合法结论。
8. 明确区分：correctness PASS 与 C4-2 科学 STOP。不得把无 headroom 写成实现失败，也不得因 AUROC 高而忽略 BER/oracle 停机门。

## Fresh 验证

- fresh 运行本 brief 的 task-control validator。
- fresh 跑两份 Ch4 tests（预期 12 tests）与 correctness smoke；不运行 `run_development.py`。
- 用一次性只读 Python probe 从 `development_raw.json` 重算上述统计和 hash/count invariants；不得落新结果文件。
- `git diff --check`，确认验证动作没有改研究实现/结果（correctness smoke 若只刷新时间戳，验证后恢复为 HEAD 内容或不要暂存）。

## 判定与交付

- `PASS`：正确性、公平性、raw→aggregate 重算、seed firewall 与停机规则全部成立；授权主控把 C4-2 记为科学 STOP 并轮换 C4-1。
- `PARTIAL`：最终 STOP 方向仍成立，但存在不影响结论的报告/审计缺口；列最小修复，仍不得自行修。
- `FAIL`：truth 泄漏、baseline/paired realization/count-match/统计错误，或预注册门被错误执行；不得轮换前把错误包当证据。

验证报告必须给出：结论、fresh 命令证据、raw 独立重算表、问题按严重度排序、是否接受科学 STOP、是否允许轮换 C4-1、唯一下一动作。一次 commit、不 push；commit 只能包含验证报告和必要 sim-preflight usage log。
