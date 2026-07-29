# Task Brief: CB1 16QAM 逐符号/更新粒度均衡族 pre-formal method-factory sprint（仅诊断）

> 来源: S003 → 2026-07-29 入口纠偏（D035 / V061） | 产出位置: `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`
> 日期: 2026-07-29（入口纠偏后重写）
> 唯一文档: 执行方只能拿到这一个文档 {+ 仓库下既有 sprint-001/002 产物与 CB1 testbed 源码（只读复用）}
> 版本史: 本文件**原为频域/子带均衡族** sprint，经 problem-bearing testbed preflight（D035/V061）判定
> 该族**物理自由度不存在**（当前 channel 源码无色散/多径/FIR/频率选择性，见 §1 证据），故**入口撤回**。
> **原位重写**为唯一四门全过的替代入口——**逐符号/更新粒度均衡族**。频域方向作 rejected task brief 保留，
> 不运行、不删除。文件名沿用 T027 以保留血缘（见 §0 版本史与 §3.1 被撤回理由）。

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 60
  action_class: METHOD_FACTORY_TASK_PREPARATION
  mission_checkpoint: CP025
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR（执行方先读）

你在 RDL 长程 live-test mission（thesis-fso 双偏振星地 OSL / blind equalization），
手上有已验证的 **CB1 16QAM shared testbed**（corrected μ=0.03 fixed-μ **块末更新** CMA
基线、共享 realization、fresh disjoint seed 集）和 sprint-001/002 的全部产出（只读复用，**不修改**）。

**你的任务**：在共享 anchor（同一 paired realization、16QAM、PI-SER、seed 集）上，对
**逐符号/更新粒度均衡这一机制不同族**做一次 bounded pre-formal method-factory sprint——
实现 3–5 个机制不同的最小构造（全部是更细的 receiver 更新步，而非 z-only 标量后处理变体），
做严格 prefix-only causal 的公平比较，并产出一份诊断级 synthesis。

**产出**：一个 `preformal-method-factory-sprint-003/` 目录（contract / method-map /
src / artifacts / synthesis / tests），回传到上述位置；聊天只回 commit、worker-log 路径、
terminal verdict（`DIAGNOSTIC_METHOD_SIGNAL` / `NO_DIAGNOSTIC_SIGNAL` /
`BLOCKED_SHARED_TESTBED`）和一句结果。

**最高纪律**：
1. **本任务只是诊断 factory sprint，不是 Groundwork Step 4a MVE**。claim ceiling =
   `DIAGNOSTIC_*`；**不得**写论文、不得作 formal Go/Kill、不得自动晋级、不得声称已超越
   任何真实竞品、不得把诊断冒充方法。
2. **批次内必须含至少一个真实、不同、已调谐、传统、任务适配、同信息的 receiver-visible
   comparator**——本轮首选为**逐符号（或更小块）随机梯度 CMA**（Godard 1980 原始形式即为逐符号）。
   它不得是 blind_affine（前序欠拟合）、post-CMA 恒等占位、TX-truth oracle 或任何任务不匹配 expert。
3. **严格 prefix-only 因果**：freeze 只读 calibration prefix，apply 只作用于 disjoint
   eval suffix；identity smoke 与方法构造**同包**，不得单立纯 smoke/formalization 包。
4. **复用共享 anchor，不改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、
   或任何 owner/session 文件；不 push**。**允许**：在隔离 sprint 目录内实现不同的更新粒度
   构造（不必、也不应改公共 CMA 文件）。
5. 若共享 testbed 的 identity/fairness 自身无法支持公平比较 → 终态记
   `BLOCKED_SHARED_TESTBED`，不强行收尾、不臆造 signal。

## 1. 背景（理解任务必需的；标"了解即可，不对照评价"）

> 以下仅为执行方理解任务上下文，**不要**拿这些数字/结论当作你的 comparator 或要复现的目标。
> 你要比较的对象是你自己在 §2.3 冻结的 comparator，不是下列历史数字。

- 本 mission 的目标（上层筛选，**非本轮可执行问题**）：判断 ML 是否在双偏振星地 OSL
  接收机链任意处提供真实、合法可比的信息增量。本轮只做诊断构造比较。
- 共享 testbed 的 inherited verdict = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`：**块末**
  固定 μ Godard CMA 在 16QAM 上存在 inner-ring collapse（headroom 0.31–0.33），对 N 与
  MMA 不变。该 headroom 是方法 factory 的合法前提（仅它允许 method 类探索）。
- 前两个 sprint 结论（**只读参考**）：
  - sprint-001：5 个 z-only 后处理/触发/初始化族 **NO_DIAGNOSTIC_SIGNAL**；其 synthesis §4
    明确把 collapse 定性为"块末更新几何 + 信道时间变化"导致的**结构性吸引子**，并在 §8 指出
    **逐符号/更新粒度变体**是最有信息的下一杠杆（仅被 identity parity 暂缓）。
  - sprint-002：corrected μ=0.03 baseline 下，M4 产 `DIAGNOSTIC_METHOD_SIGNAL`，但最强合法
    receiver-visible comparator blind_affine 反而劣于 baseline（0.318 vs 0.314），使该 signal
    无法满足 promotion preflight 的"真实不同 comparator"要求。
- 两条 signal（M4 与派生 G1）的 promotion preflight 均为 `STRATEGIC_GATE`，共同 blocker：
  collapse-recovery / z-stream 后处理族在当前切片**没有真实、不同、已调谐的合法 comparator**。

### 1.1 为什么是"逐符号/更新粒度"族，不是"频域/子带"族

本轮经 problem-bearing testbed preflight（D035/V061，四门）：

- **门1 物理自由度存在**：更新粒度是真实可调旋钮——`projects/simulation/common/_cma.py:100-166`
  的 `equalize` 在 `block_size=64` 块内向量化滤波、**块末**用块内平均梯度更新权重；更细的更新
  粒度（逐符号 / 更小块）是该代码真实施加的变换。（频域族**失败**：`_dual_pol_channel.py:127-132`
  仅有逐符号 GG 幅度 `h`、SOP 旋转、AWGN，**无色散/多径/FIR/频率选择性**，频域/子带没有可作用
  的物理自由度。）
- **门2 基线失败与候选作用点一致**：sprint-001 `synthesis.v1.md` §4（L97-130）把 collapse 诊断为
  "块末更新几何 + 信道时间变化"的结构性吸引子；§8（L176-179）明确冻结的块末协议
  （block_size=64, μ）是"疑似瓶颈"，逐符号变体是"最有信息的下一杠杆"——与基线失败点精确重合。
- **门3 存在命名、同任务、同信息、可独立调谐的传统 comparator**：**逐符号（或更小块）随机梯度
  CMA**——Godard 1980 原始形式即逐符号；任务相同（同一 z-stream 盲均衡）；同信息
  （receiver-visible，无 TX truth）；可独立调谐（自有 μ、validation freeze）。
- **门4 每门有 file:line 证据**：见上。

### 1.2 identity parity 不是禁止不同算法的理由

按 `baseline-adjudication.md` §"Shared anchor and claim-specific fairness"：共享 anchor
（同一 paired realization、调制、metric、seed 集）保端到端可比；identity parity（保持**继承
基线**的块末粒度）只保护已跑历史包的比较连续性，**不是对"跑一个不同的传统算法"的科学禁令**。
当候选作用在更细的 receiver 步上时，把"逐符号/更小块 CMA"选作任务适配的传统 comparator 是合法的、
经 re-adjudication 的 comparator 变更，不是重开已关闭轴，也不是 identity parity 违例。
**本轮必须保持共享 anchor；允许、且应当引入逐符号这一不同的传统更新粒度作为合法对照。**

## 2. 任务详情

### 2.1 要回答的问题

在冻结的 CB1 16QAM 切片（共享 anchor）上，**逐符号/更新粒度均衡族**是否能产生稳定、非伪信号、
值得回正式 Groundwork Step 1–3/3.5/4a 的诊断 signal——**且该 signal 自带一个真实、不同、已调谐、
传统、同信息的 receiver-visible comparator**？

### 2.2 执行方式

1. **Phase A — 共享 anchor identity gates（复用，不重建）**：复用 sprint-002 已通过的
   identity gates（QPSK regression / eval population identity / prefix-only freeze
   invariance），确认继承基线 = corrected **μ=0.03** fixed-μ **块末** CMA（字节级与
   `cb1_cell_runner.standard_cma_godard_with_z` 一致，μ 继承自
   `frozen-params-b01r-v1.yaml`，**不得**回退到旧 μ=0.001）。
2. **Phase B — 构造 3–5 个机制不同的"更新粒度"最小构造**。每个必须是**更细的 receiver 更新步**
   （更新频率/粒度不同，而非 z-only 标量后处理变体）。机制来源建议（执行方自行 dedup 后择优）：
   逐符号 stochastic-gradient CMA、更小块（如 block_size=8/16）块末更新、块内分段更新、
   事件触发（divergence/innovation-gated）即时更新、sliding-window recursive 更新等。
   **全部仅消费 receiver-visible 信息**（prefix + 公共 16QAM 星座几何 + 冻结公共参数），禁止
   TX-truth/oracle/future-suffix 进 freeze/gate。
3. **Phase C — dev freeze + fresh disjoint test 比较**：dev prefix 子集（与 sprint-002 一致
   的 dev/test 切分策略，**不得**复用测试 seed；禁用已污染的 seeds 71–80）。raw 行逐
   (cell,seed,method) 保存；统计单位 = seed-cluster（同 sprint-002），MDE=0.005。
4. **同包 identity/语义 smoke**：每个构造需过"输出与基线不同""恒等配置再现不变系统"
   "prefix/eval 因果隔离""constant/trivial 解不能同时满足目标"等适用项；smoke 结果必须
   写进 terminal result artifact，**不得**被 compare 覆盖。

### 2.3 comparator 硬要求（不可省）

- 冻结一个**真实、任务适配、已调谐、传统**的 receiver-visible comparator 作为本轮的"最强合法
  对照"。首选 = **逐符号（或更小块）随机梯度 CMA**，在 dev 上**单独调谐**（公平给予调参与验证
  机会，非"机械套相同超参"）。
- 它**不得**是：blind_affine（前序欠拟合）、对 CMA 输出的恒等占位、TX-truth oracle、
  任何已知 task-mismatched 的非法 expert。
- 若发现该切片上逐符号族同样凑不出真实不同 comparator，诚实记为 `BLOCKED_SHARED_TESTBED`
  并说明，**不要**用恒等/欠拟合占位冒充。

### 2.4 产出格式（强制，给模板）

目录 `preformal-method-factory-sprint-003/` 下：
- `factory-contract.v3.yaml`：共享 anchor identity、frozen 继承基线、seed 切分、comparator 定义、
  diagnostic signal gate、claim ceiling、**更新粒度族自由度证据（file:line）**。
- `method-map.v3.md`：每个构造的 deployable_action / update_granularity / prefix_input /
  frozen_params / **difference_from_rejected_axes**（逐条对 C04/C09/C12/C14/C15/C16/M1–M5
  及 §3.1 被撤回的频域族 dedup）。
- `src/`：freeze/apply 拆分的隔离实现 + identity/因果 TDD 测试（≥5/5 PASS）。
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
3. **baseline 回退陷阱**：sprint-001 用旧 μ=0.001 导致 17 包假结论。本轮继承基线必须是
   μ=0.03，不得回退。
4. **smoke 被覆盖陷阱**：单独跑的 smoke、其 receipt 被 compare 覆盖，不闭环包。smoke 必
   须写进 terminal result。
5. **跨族混淆陷阱**：不要把 z-only 标量/半径后处理当"更新粒度均衡"重做——那与 M1–M5 同族。
   本轮构造必须落在**不同的 receiver 更新步（更新粒度）**。
6. **过度归因陷阱**：诊断级结论不得外推到"更新粒度解决 collapse"等领域声称；claim ceiling
   严守 `DIAGNOSTIC_*` / 当前切片。
7. **种子污染**：seeds 71–80 已失 held-out 状态（被 ≥6 批复用），本轮禁用。

### 3.1 被撤回入口（频域/子带族）的拒绝理由（不要重做）

本文件首版选的是**频域/子带均衡族**，经 problem-bearing testbed preflight 撤回，理由：
- **门1 失败**：`projects/simulation/common/_dual_pol_channel.py:127-132` 的信道只有逐符号
  GG 幅度 `h`、SOP 旋转 `theta`、AWGN，**无色散/多径/FIR/频率选择性**——频域/子带均衡没有
  可作用的物理自由度（频域处理对一个 memoryless、flat 信道退化为恒等/标量）。
- **门2 失败**：sprint-001/002 的基线失败机制（块末更新几何 + 信道时间变化吸引子）与频域
  作用点不重合。
- **门3 失败**：原 T027 未冻结一个真实、传统、同信息的频域 comparator，只把它留给 executor。
- 该方向不重开、不删除，作 rejected task brief 保留血缘。

## 4. 验收（主线拿到产出后怎么检查）

- [ ] task-control 块存在且 `validate_task_control.py` PASS（epoch 60 / CP025 / 动作类合法）。
- [ ] 继承基线确为 corrected μ=0.03 块末 CMA，无 μ=0.001 回退证据。
- [ ] ≥3 个构造实际跑通，且全部 prefix-only 因果（TDD ≥5/5 PASS）。
- [ ] **含一个真实、不同、已调谐、传统的 comparator**（首选逐符号 stochastic-gradient CMA，
      非 blind_affine / 非恒等占位 / 非特权方法）——若不满足且无正当理由，记为执行缺陷而非
      NO_SIGNAL。
- [ ] raw/aggregate 以 seed-cluster 为单位；smoke 写进 terminal result 未被覆盖。
- [ ] terminal verdict ∈ {`DIAGNOSTIC_METHOD_SIGNAL`, `NO_DIAGNOSTIC_SIGNAL`,
      `BLOCKED_SHARED_TESTBED`}，且 synthesis 对"为什么赢家赢/输家输/有无伪信号"有机制解释。
- [ ] 未改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、任何 owner/session；
      未 push；未把诊断当方法/Go/论文数。
- [ ] method-map 逐条对 §3.1 被撤回的频域族 dedup（不得把频域/子带当"更新粒度"重做）。

## 附：产出回传位置

`projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`
（worker-log 写到 `projects/thesis-fso/worker-logs/step-027-*.md`，commit 在当前 fork 分支）
