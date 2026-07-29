# Task Brief: CB1 16QAM 频域/子带均衡族 pre-formal method-factory sprint（仅诊断）

> 来源: S003（入口选择） | 产出位置: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`
> 日期: 2026-07-29
> 唯一文档: 执行方只能拿到这一个文档 {+ 仓库下既有 sprint-001/002 产物与 CB1 testbed 源码（只读复用）}

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 59
  action_class: METHOD_FACTORY_TASK_PREPARATION
  mission_checkpoint: CP025
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR（执行方先读）

你在 RDL 长程 live-test mission（thesis-fso 双偏振星地 OSL / blind equalization），
手上有已验证的 **CB1 16QAM shared testbed**（corrected μ=0.03 fixed-μ CMA 基线、共享
realization、fresh disjoint seed 集）和 sprint-001/002 的全部产出（只读复用，**不修改**）。

**你的任务**：在同一 testbed 上，对**频域/子带均衡这一机制不同族**做一次 bounded
pre-formal method-factory sprint——实现 3–5 个机制不同的最小构造，做严格 prefix-only
causal 的公平比较，并产出一份诊断级 synthesis。

**产出**：一个 `preformal-method-factory-sprint-003/` 目录（contract / method-map /
src / artifacts / synthesis / tests），回传到上述位置；聊天只回 commit、worker-log 路径、
terminal verdict（`DIAGNOSTIC_METHOD_SIGNAL` / `NO_DIAGNOSTIC_SIGNAL` /
`BLOCKED_SHARED_TESTBED`）和一句结果。

**最高纪律**：
1. **本任务只是诊断 factory sprint，不是 Groundwork Step 4a MVE**。claim ceiling =
   `DIAGNOSTIC_*`；**不得**写论文、不得作 formal Go/Kill、不得自动晋级、不得声称已超越
   任何真实竞品、不得把诊断冒充方法。
2. **批次内必须含至少一个真实、不同、已调谐的 receiver-visible comparator**（非
   blind_affine、非 post-CMA 恒等占位）。这是不可省的硬要求——见 §2.3 与 §3，理由直接来自
   两个前序 signal 的转化失败。
3. **严格 prefix-only 因果**：freeze 只读 calibration prefix，apply 只作用于 disjoint
   eval suffix；identity smoke 与方法构造**同包**，不得单立纯 smoke/formalization 包。
4. **复用既有 testbed**，不改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、
   或任何 owner/session 文件；**不 push**。
5. 若 shared testbed 的 identity/fairness 自身无法支持公平比较 → 终态记
   `BLOCKED_SHARED_TESTBED`，不强行收尾、不臆造 signal。

## 1. 背景（理解任务必需的；标"了解即可，不对照评价"）

> 以下仅为执行方理解任务上下文，**不要**拿这些数字/结论当作你的 comparator 或要复现的目标。
> 你要比较的对象是你自己在 §2.3 冻结的 comparator，不是下列历史数字。

- 本 mission 的目标（上层筛选，**非本轮可执行问题**）：判断 ML 是否在双偏振星地 OSL
  接收机链任意处提供真实、合法可比的信息增量。本轮只做诊断构造比较。
- 共享 testbed 的 inherited verdict = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`：block-end
  固定 μ Godard CMA 在 16QAM 上存在 inner-ring collapse（headroom 0.31–0.33），对 N 与
  MMA 不变。该 headroom 是方法 factory 的合法前提（仅它允许 method 类探索）。
- 前两个 sprint 结论（**只读参考**）：
  - sprint-001：5 个 z-only 后处理/触发/初始化族 **NO_DIAGNOSTIC_SIGNAL**；明确指出"第六
    未测族 = 频域/子带均衡"。
  - sprint-002：corrected μ=0.03 baseline 下，M4（prefix-gated identity/transport policy）
    产 `DIAGNOSTIC_METHOD_SIGNAL`，但**最强合法 receiver-visible comparator blind_affine
    反而劣于 baseline（0.318 vs 0.314）**，使该 signal 无法满足 promotion preflight 的
    "真实不同 comparator"要求。
- 两条 signal（M4 与派生 G1）的 promotion preflight 均为 `STRATEGIC_GATE`，共同 blocker：
  collapse-recovery / z-stream 后处理族在当前切片**没有真实、不同、已调谐的合法
  comparator**。
- 本轮因此选频域/子带均衡族（portfolio 明示 `REOPENED` 且从未测过），并**把"自带真实
  comparator"内化为 factory 的硬要求**，使任何 signal 一旦产生即满足 preflight 该项。

## 2. 任务详情

### 2.1 要回答的问题

在冻结的 CB1 16QAM 切片上，**频域/子带均衡族**是否能产生稳定、非伪信号、值得回正式
Groundwork Step 1–3/3.5/4a 的诊断 signal——**且该 signal 自带一个真实、不同、已调谐的
receiver-visible comparator**？

### 2.2 执行方式

1. **Phase A — 共享 testbed identity gates（复用，不重建）**：复用 sprint-002 已通过的
   identity gates（QPSK regression / eval population identity / prefix-only freeze
   invariance），确认基线 = corrected **μ=0.03** fixed-μ CMA（字节级与
   `cb1_cell_runner.standard_cma_godard_with_z` 一致，μ 继承自
   `frozen-params-b01r-v1.yaml`，**不得**回退到旧 μ=0.001）。
2. **Phase B — 构造 3–5 个机制不同的频域/子带均衡最小构造**。每个必须是**不同的 receiver
   步骤**（在 CMA 之后/之前做频域处理），不是 z-only 标量后处理变体。机制来源建议（执行方
   自行 dedup 后择优）：每偏振 DFT 后按子带做幅度/相位校正、子带增益 reassignment、
   frequency-domain MMSE-style 去噪、carrier/spurious 子带 notch、子带判决反馈等。**全部
   仅消费 receiver-visible 信息**（prefix + 公共 16QAM 星座几何 + 冻结公共参数），禁止
   TX-truth/oracle/future-suffix 进 freeze/gate。
3. **Phase C — dev freeze + fresh disjoint test 比较**：dev prefix 子集（与 sprint-002 一致
   的 dev/test 切分策略，**不得**复用测试 seed；禁用已污染的 seeds 71–80）。raw 行逐
   (cell,seed,method) 保存；统计单位 = seed-cluster（同 sprint-002），MDE=0.005。
4. **同包 identity/语义 smoke**：每个构造需过"输出与基线不同""恒等配置再现不变系统"
   "prefix/eval 因果隔离""constant/trivial 解不能同时满足目标"等适用项；smoke 结果必须
   写进 terminal result artifact，**不得**被 compare 覆盖。

### 2.3 comparator 硬要求（不可省）

- 冻结一个**真实、任务适配、已调谐**的 receiver-visible comparator 作为本轮的"最强合法
  对照"。它**不得**是：blind_affine（前序欠拟合）、对 CMA 输出的恒等占位、TX-truth oracle、
  任何已知 task-mismatched 的非法 expert。
- 推荐：在频域族内选一个结构最不同、且在 dev 上**单独调谐**（公平给予调参与验证机会，
  非"机械套相同超参"）的构造作为合法对照；或退而在同族内用"块内全量频域校正 vs prefix
  估计频域校正"这类**真正不同信息边界**的对照。若发现该切片上频域族同样凑不出真实不同
  comparator，诚实记为 `BLOCKED_SHARED_TESTBED` 并说明，**不要**用恒等/欠拟合占位冒充。

### 2.4 产出格式（强制，给模板）

目录 `preformal-method-factory-sprint-003/` 下：
- `factory-contract.v3.yaml`：testbed identity、frozen baseline、seed 切分、comparator 定义、
  diagnostic signal gate、claim ceiling。
- `method-map.v3.md`：每个构造的 deployable_action / prefix_input / frozen_params /
  **difference_from_rejected_axes**（逐条对 C04/C09/C12/C14/C15/C16/M1–M5 dedup）。
- `src/`：freeze/apply 拆分的实现 + identity/因果 TDD 测试（≥5/5 PASS）。
- `artifacts/`：raw-rows（逐 cell,seed,method）、prefix-receipt、dev-freeze-receipt、
  terminal `result.json`（含 smoke 字段、不可被 compare 覆盖）。
- `synthesis.v3.md`：TL;DR / boundary / identity gates / constructs / 公平比较结果表 /
  为什么赢家赢输家输 / 4 类标签仅 offline / acceptance check / caveats / terminal verdict。

terminal verdict 三选一，写到 synthesis §0 与 result.json：
- `DIAGNOSTIC_METHOD_SIGNAL`：至少一个构造在真实不同 comparator 下稳定、非伪、值得 formal 化；
- `NO_DIAGNOSTIC_SIGNAL`：批次在冻结切片下无可用 signal；
- `BLOCKED_SHARED_TESTBED`：共享 evaluator/baseline/comparator 不能支持公平诊断比较。

## 3. 已知陷阱（基于历史失败的具体案例）

1. **comparator 占位/欠拟合陷阱（本轮首要）**：sprint-002 的 blind_affine 劣于 baseline、
   G1 的 D4 是恒等映射，直接导致两条 signal 无法转化。**任何看起来"赢了"的结果，先查
   comparator 是不是恒等/欠拟合/任务不匹配**；如是，记 diagnostic-only，不当 signal。
2. **因果泄漏陷阱**：sprint-001 M3/M5 用 eval-window 统计做选择（V052 拒收）。freeze 必须
   只读 prefix，apply 只作用 suffix，suffix 不回灌任何 selection。
3. **baseline 回退陷阱**：sprint-001 用旧 μ=0.001 导致 17 包假结论。本轮基线必须是
   μ=0.03，不得回退。
4. **smoke 被覆盖陷阱**：单独跑的 smoke、其 receipt 被 compare 覆盖，不闭环包。smoke 必
   须写进 terminal result。
5. **跨族混淆陷阱**：不要把 z-only 标量/半径后处理当"频域均衡"重做——那与 M1–M5 同族。
   本轮构造必须落在**不同的 receiver 步骤（频域）**。
6. **过度归因陷阱**：诊断级结论不得外推到"频域均衡解决 collapse"等领域声称；claim ceiling
   严守 `DIAGNOSTIC_*` / 当前切片。
7. **种子污染**：seeds 71–80 已失 held-out 状态（被 ≥6 批复用），本轮禁用。

## 4. 验收（主线拿到产出后怎么检查）

- [ ] task-control 块存在且 `validate_task_control.py` PASS（epoch 59 / CP025 / 动作类合法）。
- [ ] 基线确为 corrected μ=0.03，无 μ=0.001 回退证据。
- [ ] ≥3 个构造实际跑通，且全部 prefix-only 因果（TDD ≥5/5 PASS）。
- [ ] **含一个真实、不同、已调谐的 comparator**（非 blind_affine / 非恒等占位）——若不满足
      且无正当理由，记为执行缺陷而非 NO_SIGNAL。
- [ ] raw/aggregate 以 seed-cluster 为单位；smoke 写进 terminal result 未被覆盖。
- [ ] terminal verdict ∈ {`DIAGNOSTIC_METHOD_SIGNAL`, `NO_DIAGNOSTIC_SIGNAL`,
      `BLOCKED_SHARED_TESTBED`}，且 synthesis 对"为什么赢家赢/输家输/有无伪信号"有机制解释。
- [ ] 未改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、任何 owner/session；
      未 push；未把诊断当方法/Go/论文数。

## 附：产出回传位置

`projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`
（worker-log 写到 `projects/thesis-fso/worker-logs/step-027-*.md`，commit 在当前 fork 分支）
