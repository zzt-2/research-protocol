# Task Brief: D0 S1 natural-occurrence 唯一 bounded repair 与正式执行

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-201-d0-s1-natural-occurrence.md`
> 日期: 2026-08-11
> 唯一文档: 执行方只能依赖本 brief、下列冻结合同/源码/测试与 D024/V019 artifacts

---

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，I01–I19 底座已验收，但工程计划曾明确“不创建 science runner”。用户现已由 D025/CP014 把总授权上调到 13 日并要求直接跑科学链。

**你的任务**：把“缺少 S1 可执行入口”作为当前门唯一一次 bounded repair，用 TDD 补齐最小 S1 runner，然后立即运行冻结的 S1 first stage（20 seeds × 12 cells × 2 polarizations = 480 rows），给出第一个真实 occurrence 数字和 PASS/FAIL。

**产出**：生产 runner、测试、raw/artifact/receipt、step-201 日志；若运行超过本 agent 的 15 分钟时间盒，必须以可恢复 checkpoint + 独立后台进程启动完整 S1，并在日志中写 PID、命令、输出路径和监控方法，绝不能缩 workload。

**最高纪律（违反一条就废了）**：

1. 只做 S1；不运行或实现 S2–S4/C1，不再做 readiness、预算审计、HMM 优化或平台泛化。
2. 冻结合同唯一 owner：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`；不得改 population/seed/cell/metric/gate。S1 first-stage 必须正好 480 typed raw rows。
3. S1 gate 原样：event trajectories ≥12、distinct seed clusters ≥4、distinct physical cells ≥2；若 first stage 不足，按合同是否允许 maximum escalation 裁决并明确记录，禁止自创阈值。
4. event definition 原样：每 polarization trajectory 基于 evaluator-only true phase 与 common-CPR phase，四态最近 π/2 residual；每侧 32 symbols 窗、各至少 28 same-state、前后状态不同；32 symbols 内 transitions 合并。deployable path 不得读 truth。
5. TDD：先写最小 runner contract/test 并亲眼取得 expected RED，再写 production；记录精确 RED/GREEN 命令和结果。不要重跑 I05 十一分钟链；只跑覆盖新增入口的 focused tests + 必需窄回归。
6. 复用现有 `contract.py/waveform.py/channel.py/receiver.py/schemas.py/statistics.py/artifacts.py/freeze.py/verify.py`，不得修改 `common/`，不得改 owner YAML。
7. raw rows、summary、receipt 必须原子写入 repo 内 `projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/`；支持 checkpoint/resume，重复恢复不得重算或重复计数已完成 row。
8. 不用 dev 结果冒充 test；S1 不产生方法 signal。日志必须分别写 `formal_science_disposition`、`mission_method_delta=NONE`、`thesis_method_disposition=NONE`。
9. 不 commit、不 stage、不 push；不得触碰四个 `p05_run*.log`。
10. 单 agent 最多 15 分钟。到时完整运行未结束就启动后台进程并返回，不在前台死等。

## 1. 背景

- D024/V019 测得冻结 D0 总投影 `10.819450931739858d`，旧 7 日门曾终止 science。
- D025 保留该测量与 I01–I19，改为总硬上限 `13.0d`，当前只开放 S1。
- S1 不调用 decoder/HMM；其目标仅是自然 persistent slip occurrence。
- 现有 `statistics.reduce_s1` 已 enforce 480/1200 rows、seed/cell/polarization exact Cartesian coverage 与 event/count relation。

## 2. 任务详情

### 2.1 实现/执行

1. 先读冻结 YAML 的 `event_definition`、`strata.S1_natural_occurrence`、seed plan、population、raw schema、artifact/freeze requirements，以及现有源码公开 API。
2. 设计最小公开入口，优先新增单一 `science.py`（或若现有命名要求更合适则同等单文件）及单一 focused test file；不要建设通用 orchestrator。
3. RED 至少覆盖：缺失入口；persistent-transition 纯函数的无事件/单事件/32-symbol merge；480-row exact reduction/gate；checkpoint 去重/resume；拒绝 wrong seed/cell/cardinality 或未授权 phase。
4. GREEN 后运行 first-stage full 480 rows。每完成一个物理 frame 原子 checkpoint，完整 run 可被外部 watchdog 恢复。
5. 生成 raw JSONL、summary JSON、receipt JSON（含 contract SHA、source SHA/HEAD、seed/cell domains、480 row count、event count/rate、distinct event seeds/cells、gate verdict、wall time、resume count、artifact SHA）。
6. 若 first stage 已可直接 PASS/FAIL，按冻结合同裁决；不得为“多跑点”擅自进入 maximum。若合同明确 first-stage不足才升级 maximum，记录 trigger 后让主控决定/继续。

### 2.2 产出格式

`step-201-d0-s1-natural-occurrence.md` 必须含：

- `STATUS=DONE|BACKGROUND_RUNNING|BLOCKED`
- 变更文件与一句话设计
- RED/GREEN 原始命令、计数、耗时
- 正式执行命令、PID（若后台）、checkpoint/raw/summary/receipt 路径
- `observed_trajectories`、`event_count`、`event_rate`、`distinct_event_seed_clusters`、`distinct_event_physical_cells`
- `S1_VERDICT=PASS|FAIL|RUNNING|INVALID`
- `formal_science_disposition`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`
- git status 与 p05 4/4 SHA protection 结果

## 3. 已知陷阱

- `d0-implementation-plan.md` 的“不创建 science runner”是旧 CP012 权限，不是当前设计要求；D025 只取代权限，不取代源码/测试事实。
- 不能把 BPS 的离散选择状态直接当 truth event；event 必须由冻结 evaluator-only residual state 定义。
- common BPS phase trace 与 true phase 的符号/时间对齐要从现有 receiver/channel 语义核实，不能凭直觉。
- 一帧是 dual-pol，但 S1 row 是 polarization trajectory；240 frames 应产生 480 rows。
- 不要用 synthetic/injected slip 跑 S1；`injection:none`。

## 4. 验收

- [ ] owner YAML 未修改；population/seeds/cells/gate exact。
- [ ] 有真实 expected RED 与 focused GREEN。
- [ ] full S1 已完成，或完整 480-row 后台运行已启动且可恢复。
- [ ] 若完成，数字能由 raw JSONL + `statistics.reduce_s1` 独立复算。
- [ ] 未触碰 S2–S4/C1/common/p05，未 stage/commit/push。

## 附：关键路径

- 合同：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- 实现：`projects/simulation/explore/coded-decoder-feedback/*.py`
- 测试：`projects/simulation/tests/test_d0_*.py`
- 原工程 receipts：`projects/simulation/explore/coded-decoder-feedback/artifacts/engineering-throughput/`
- 报告：`projects/thesis-fso/worker-logs/step-201-d0-s1-natural-occurrence.md`
