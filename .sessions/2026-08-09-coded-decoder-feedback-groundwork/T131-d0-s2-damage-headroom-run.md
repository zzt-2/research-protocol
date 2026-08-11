# Task Brief: D0 S2 B1 damage / O1 headroom 正式执行

> 来源: S001 / D026 / V020 / CP015 | 产出位置: `projects/thesis-fso/worker-logs/step-203-d0-s2-damage-headroom.md`
> 日期: 2026-08-11
> 唯一文档: 本 brief + 冻结 owner YAML + 已验收 I01–I19 + T129 science.py

---

## 0. TL;DR

S1 已以 `262/480` 经独立终验 PASS。你的任务只是在现有 `science.py` 上做 S2 gate-specific 唯一 bounded repair，然后运行冻结 S2，得到 B1 damage 与 O1 recoverability 的 point、10,000-replicate seed-cluster CI、positive-cell count和 PASS/FAIL。

**最高纪律**：

1. 只做 S2 B1/O1；B2 虽是现有 raw schema 第三方法列，也不得在本门执行真实 B2 或裁 absorption。若 `reduce_s2` 强制 B2 row，使用合同允许的结构性占位必须有明确 `NOT_EVALUATED` 语义；不得制造 B2 数字。若 owner/schema 不能合法分离，立即报真实 blocker，不改指标。
2. exact workload：seeds `8150..8159`，cells=`hard/mid/clean`，2 polarizations，9 fixtures，fixture-aligned no-jump twins；不得缩 seed/cell/fixture/method/gate。
3. damage gate：macro B1-on ACWER − B1-off ACWER point≥0.10、seed-cluster 95% CI lower>0、positive cell points≥2。
4. recoverability gate：macro ratio-of-sums `(B1_on_errors-O1_on_errors)/B1_on_errors` point≥0.10、CI lower>0、positive cell points≥2。任何零分母/invalid fraction规则严格按 owner/statistics。
5. 只复用 canonical waveform/channel/common BPS/codec/B1/controlled fixture/O1/freeze/artifact APIs；truth 只进入 evaluator O1，deployable B1 不读 truth。
6. TDD：先写 expected RED，再最小实现；focused GREEN。checkpoint 每个 base seed-cell-target-pol cluster 原子落盘并可 resume/去重。Windows retry沿用 T129，不另扩通用平台。
7. full run 若超过15分钟：启动独立后台进程，返回 PID与首个 checkpoint；不前台死等、不缩 workload。
8. raw、summary、receipt 进 `projects/simulation/explore/coded-decoder-feedback/artifacts/science/s2-damage-headroom/`；完整 runtime 跨 resume 捕获不到就写 null，不能冒充。
9. `formal_science_disposition`、`mission_method_delta=NONE`、`thesis_method_disposition=NONE` 分开；本门不是方法 signal。
10. 不改 owner/common/S1 artifacts/S2以后代码，不 stage/commit/push，不碰 p05。

## 1. 必须先核实的合同/API

- owner：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- schema/reduction：`schemas.S2MethodRow`、`statistics.reduce_s2`、`statistics.bootstrap_paired`
- methods：`run_b0/run_b1/inject_controlled_fixture/freeze_deployable_outputs/evaluate_o1_inverse`
- channel/codec/freeze/artifacts 已验收接口；不得绕过 deployment seal 或 content owner。

## 2. RED/GREEN 与执行

Focused tests 至少覆盖：

- exact 10×3×2×9 S2 cluster plan；
- no-jump twin 9-to-1 owner sharing；
- B1 on/off 与 O1 evaluator row accounting；
- affected-CW boundary count与 info-bit total；
- damage/headroom macro与 seed-cluster bootstrap gate；
- truth boundary；
- checkpoint resume/conflict；
- B2 不被本门调用/裁决。

完成 GREEN 后立即 full run。若 S2 任一门 FAIL，报告并停止，不运行 B2。

## 3. 报告格式

`step-203` 必须含：

- `STATUS=DONE|BACKGROUND_RUNNING|BLOCKED`
- 变更文件、RED/GREEN命令/计数/耗时
- PID/checkpoint/raw/summary/receipt
- exact workload counts
- damage：point、CI、positive cells、PASS/FAIL
- recoverability：point、CI、positive cells、PASS/FAIL
- invalid replicate counts/terminals
- `S2_VERDICT=PASS|FAIL|RUNNING|INVALID`
- 三类 disposition 分列
- owner/common/p05/staging protection

## 4. 验收

- [ ] exact workload 与 gate 未改
- [ ] B2 未执行/未裁
- [ ] full raw 可由 typed schema + statistics fresh 复算
- [ ] 任一 S2 门 FAIL 后无下游运行
- [ ] 没有 method/thesis claim
