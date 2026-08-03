# Task Brief: 2B Fixed-Point Branch-Routed CPR bounded closure

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 11
  action_class: THESIS_BOUNDED_PACKAGE_EXECUTION
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S015 / D022 | 产出位置: 本任务独立 worktree 的 2B sandbox、results、worker-log 与 harvest dossier
> 日期: 2026-08-03
> 唯一任务: 把 2B 从 `NEEDS_ONE_BOUNDED_PACKAGE` 闭合到明确终态

## 0. TL;DR

你在从 `codex/rdl-method-production-v2` 最新提交创建的隔离 worktree 中。执行且只执行一个完整链方法包：

`Q-format receiver statistic/controller → preselect → execute one DA or NDA branch → one corrected output`

从恢复、preflight、合同冻结、实现、性能/成本执行、独立 verifier、harvest 到提交全部在本对话完成。不得以“还差 timing/综合/一轮实验”结束。终态只能是 `THESIS_METHOD_READY / SUPPORTING_ONLY / REJECT / EXTERNAL_BLOCKED`。

### 最高纪律

1. 不保证正面结果；保证可信终态和可复现资产。
2. 一个 package，最多一次确定性 repair。改方法、指标、成本边界、信息边界或 held-out contract 时，旧 test 作废，必须新 receipt + fresh seeds。
3. 不修改 `projects/simulation/common/`、`params.py`、正式论文、system topic、formal owner 或旧 artifacts。需要这些改动即 `EXTERNAL_BLOCKED(reason=STAGE_SCOPE_EXCEEDED)`。
4. 必须计完整 caller path 的 controller/preselect/dispatch/branch 成本；禁止先跑双支再少记一支。
5. Q(8,6) 是 controller 实现点，不是新 selector；P03 的 `0/132000` 是 float-bypass/identity 语境，禁止误写成 Q(8,6) 全链零失配。
6. 无合法 FPGA synthesis 就不声称 LUT/DSP/面积/功耗/硬件吞吐；禁止复活 74.6% 总接收机复杂度下降。
7. 不开第二包、不扩硬件平台、不 push。

## 1. 恢复与阶段身份

开始前完整读取并遵守：

1. system topic-index、D021/D022、V015、S015、本 T005 与 T003；
2. Research Direction Lab Skill 及 method-production/evidence/baseline references；
3. sim-preflight 主文件、recover/run/add 场景与 constraints/tech/param-source/mve-validation/doc-discipline/usage-log/interrupt；
4. `projects-overview.md`、`projects/thesis-fso/master-state.md`、`thesis-lessons.md` 速查与最近三条；
5. `code-quality.md`、simulation templates、P03 worker-log/raw、route-A/route-B caller、CCISP method source。

本任务是 existing CCISP 的 `RDL Deep Evidence / thesis implementation closure`，不是新的 branch-selection 算法。若必须改 core receiver、信号模型或 formal stage，停止为 `EXTERNAL_BLOCKED(reason=STAGE_SCOPE_EXCEEDED)`。

先验证 foreground control，完成 sim-preflight 场景 D 恢复与 usage log，再执行。

## 2. Phase 0：真实调用链与算法身份门

沿 caller→callee 独立核实：

- route A 是否真实执行 DA+NDA 后 mux；route B 是否在两个 CPR 前决定并只调用一支；
- 990/990 identity 的实际 metric、grid、seed 与 output 含义；
- P03 Q(8,6) 的 bit-true quantizer、overflow/saturation、gain-bearing regret 与 mixed-precision negative；
- `0/132000` 的真实身份，不得错误归给 Q(8,6)；
- NDA ambiguity resolver、TX truth 和 BER scoring 是否位于 timed deployable boundary 外；
- metric signature、state lifecycle、parameter source、seed history；
- 完整链可否在不改 common/params 下 instrument 与执行。

建立 unit/metamorphic tests：route A/B 对同一 frozen branch command 的 selected output 一致；翻转 post-hoc truth 不改变 timed kernel；typed operation counters 对微型手算样例吻合；Q-format saturation/rounding 与 bit-true 定义一致。

## 3. 冻结三方法与成本边界

只允许：

- `A-F`：route-A dual-branch float reference；
- `B-F`：route-B preselect single-branch float，隔离 scheduling 增量；
- `B-Q8,6`：route-B + uniform Q(8,6) statistic/controller，fixed-point 子链；
- `B-Q ladder` 与 `two-exp(8,6)`：只作位宽/negative 消融，不得事后替换 primary。

Timed kernel 必须从预生成 256-sample raw window + receiver-visible config 开始，到 single carrier-corrected output 结束。排除 channel generation、I/O、BER scoring 与 truth-assisted ambiguity resolution；但所有方法排除项完全相同。

Typed operations 至少分：abs²、real/complex add/multiply、divide、sqrt/log/LUT、compare、quantize、saturate、FFT、dispatch/mux。另报 controller storage bits、branch workspace、selected-output buffer 与 peak live bytes。route A 使用内存合理的顺序双支实现，不能故意劣化 baseline。

## 4. Dev、receipt 与 held-out chronology

### 4.1 Dev/pre-benchmark

- 审计历史 seed ledger，选 fresh dev/test ranges；
- 复现 existing formal grid：三种 downlink GG regime × SNR {5,7,...,25} dB × 30 seed clusters × 400 windows，若源码权威网格不同则以 source receipt 为准并说明；
- dev 只用于 instrument 校准、batch size、warm-up/repetition、CPU affinity 与 runtime 预算；
- 做短 pilot，确认 timing variance 可控和 B-F 相对 A-F 的方向符合 operation expectation。若偏离，先查 caller path，不直接扩大样本。

### 4.2 Freeze Commit 1

任何 held-out performance/timing 前提交 immutable receipt：method/source hashes、exact grid、seed ranges、timed boundary、typed-op schema、Q-format、metric/MDE、platform/affinity/thread env、warm-up/repetition、AB/BA 顺序、test_started=false、信息/metric/lifecycle cards。

runner 必须在 test 前验证 receipt/source hashes；Commit 1 后不得改方法或判据。

### 4.3 并发与 timing 隔离

T004 可能同时运行。可以并行做代码审计、功能测试和非 headline performance，但 headline CPU timing 必须在无其他重负载仿真/训练进程时运行：

- 记录进程、CPU load、频率/电源模式、线程环境与 affinity；
- 发现竞争则先做非 timing 工作，并以不超过 60 秒的轮询间隔等待；不得在竞争状态下接受 headline；
- 计时稳定门在 receipt 前冻结为：3 个 pilot batch 的 `T_B-F/T_A-F` ratio CV `≤5%`，且 A-F absolute median timing CV `≤10%`；最多 6 次 pilot 尝试或累计 45 分钟（先到者为止），不得挑最好一轮；耗尽仍不稳定则 `EXTERNAL_BLOCKED(reason=UNRESOLVED_TIMING_CONTENTION)`；
- 每 seed-cell 至少 3 次 untimed warm-up、5 次 measured repetitions，AB/BA 或 randomized paired order；使用 batch timer。

### 4.4 Held-out

保存每个 `(cell, seed, method)` 的 performance 与 timing rows、branch counts、operation/storage rows。所有方法共享 realization、输入、pilot/payload mask 与 evaluation wrapper。

## 5. 冻结裁决

### 5.1 Performance

- `A-F` vs `B-F`：held-out 全 grid 的 branch command 与 selected output 必须 0 mismatch；否则 `REJECT`。
- Q primary：paired common-768 end-to-end BER penalty `ΔQ=10log10(BER_B-Q8,6/BER_B-F)`；gain-bearing subset 与三个 9 dB headline cells 的 one-sided 95% CI upper 均不超过 0.15 dB。
- 完整 grid 全报，不得只截通过区域。若零误码导致比值不可定义，使用 pre-registered count model/upper bound，不得静默丢 cell。

### 5.2 Cost

- scheduling primary timing ratio `RT_sched=T_B-F/T_A-F`；paired cluster 95% CI upper `≤0.95`（至少 5% 完整 kernel 降低）；
- `B-F` operation table 必须显示只执行一支，证明收益来自真实 scheduling；`B-Q8,6/T_A-F` timing 另报，不能替代 scheduling primary；
- typed operation、latency、throughput、controller bits 与 peak memory 全部报告。若 memory 不降，只声称 execution/latency。

### 5.3 Disposition

本 package 内分开裁决两个 action lineage，不增加第二包：

- **Scheduling lineage（A-F→B-F）**：identity 0 mismatch、`RT_sched` 过门、完整 cost table 与 verifier 通过，即足以使 2B 总终态为 `THESIS_METHOD_READY / THESIS_ENGINEERING_COMPONENT`；合法 claim 仅为 preselection single-branch execution。
- **Q(8,6) sublineage（B-F→B-Q8,6）**：performance 非劣、bit-true identity/overflow 与 verifier 通过，才附加 fixed-point claim；失败则该子链标 `SUPPORTING_ONLY`，不得反向 Kill 已通过的 scheduling lineage。

若 scheduling lineage 的 timing MDE 失败，则 2B 总终态 `SUPPORTING_ONLY`，保留 route identity、operation analysis 和 fixed-point feasibility，不换分母、不追加综合。若成本记账欺骗、truth leak、route identity 失败或不可恢复 chronology 错误：`REJECT`。

## 6. 可用交付物

只写：

- `projects/simulation/explore/2b-fixed-point-branch-routed-cpr-closure/`
- `projects/simulation/results/2b_fixed_point_branch_routed_cpr_closure/`
- `projects/thesis-fso/worker-logs/step-044-2b-fixed-point-branch-routed-cpr-closure.md`
- `projects/thesis-fso/direction-lab/harvest/2b-fixed-point-branch-routed-cpr-method-package.md`
- `projects/simulation/results/2b_fixed_point_branch_routed_cpr_closure/sim-preflight-usage-entry.md`（任务专属片段；不得直接修改共享月志，由主控接收后串行并入）

method-package 无论正负都包含：方法名、M-C-A、I-A-O、算法伪代码、控制流/数据流框图节点、完整 cost table、主图数据、位宽消融、claim ceiling、不能说什么、最终 disposition。

fresh-context verifier 必须独立走 caller→callee、手算至少一个 typed-op 微例、重算 raw→aggregate、核 timing 污染与 Q8,6 身份。最后 Commit 2，不 push。

## 7. 自动继续与最终回复

本地 bug、序列化、统计、instrument 或 runtime 问题自动在一次 repair 内闭合。只在外部硬件/权限、持续不可消除的机器竞争或需要 common/params/formal stage 变化时允许 `EXTERNAL_BLOCKED`。

最终只汇报：

1. terminal disposition；
2. A-F/B-F/B-Q8,6 的性能、timing ratio/CI、typed operations/storage；
3. 方法包能否直接用作 Ch5，合法 claim；
4. artifact/worker-log/verifier 路径；
5. Commit 1/2 SHA、未 push、工作树状态。

## 8. 验收

- [ ] caller path 真实先选后算，成本含 controller/preselect
- [ ] Q(8,6) identity/性能口径不混淆
- [ ] CPU timing 无并发污染且可复现
- [ ] performance 与 cost 双门独立通过才晋级
- [ ] 正负结果都有可用 dossier
- [ ] 不以“还差一轮/综合”结束
