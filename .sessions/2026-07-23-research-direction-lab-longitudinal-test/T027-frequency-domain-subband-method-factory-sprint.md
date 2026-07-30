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
  control_epoch: 61
  action_class: PREFORMAL_METHOD_FACTORY
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
terminal verdict（见 §2.4 五选一）和一句结果。

**授权边界（user Phase-0 纠偏后冻结）**：
- `action_class = PREFORMAL_METHOD_FACTORY`，**仅授权本次 bounded 诊断 sprint**；不授权
  formal MVE、不授权 Step 5/Contract/Execute、不授权任何论文 claim、不授权任何 protected owner 修改。
- foreground 已显式允许本次 `PREFORMAL_METHOD_FACTORY`（epoch 61 / CP025），但仅覆盖本 sprint。

**最高纪律**：
1. **本任务只是诊断 factory sprint，不是 Groundwork Step 4a MVE**。claim ceiling =
   `DIAGNOSTIC_*`；**不得**写论文、不得作 formal Go/Kill、不得自动晋级、不得声称已超越
   任何真实竞品、不得把诊断冒充方法。
2. **冻结的传统 comparator = tuned per-symbol standard CMA（canonical Godard-with-z 梯度）**。
   其权重更新必须为 **Δw ∝ (R²−|z|²)·z·r\***（Godard 1980 原始 per-symbol 形式），
   provenance 指向 `cb1_cell_runner.standard_cma_godard_with_z`（`cb1_cell_runner.py:124-129`，
   即 `(eX * zx_blk)[:,None]*conj(rX_blk)`，正是 (R²−|z|²)·z·r* 的 per-block 平均）。
   **不得**用 `common/_cma.py` 的 `CMAEqualizer2x2` 冒充 comparator——该类实现 **scalar-error**
   梯度 Δw ∝ (R²−|z|²)·r*（`_cma.py:161-166`，缺 z 因子，`cb1_cell_runner.py:20-30` docstring
   已明示其无法通过 standard-CMA identity gate），它只能用来证明 block_size 是真实旋钮，
   不是 canonical 传统 comparator。comparator 的 μ **必须在 dev 上单独调谐**（公平给予调参机会）。
3. **门2 证据等级纠正（不得越界）**：sprint-001 §4/§8 把"块末更新几何是结构性吸引子原因"
   写成已确认机制——**该归因已在 CP018/D026/V052 被拒收**
  （`V052 REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO`）。
   正确表述：**块末更新是 source-backed、值得验证的疑似作用点**（`_cma.py:100-166` 块末更新是真旋钮；
   sprint-001 §4/§8 把它列为"疑似瓶颈"、逐符号变体列为"最有信息的下一杠杆"）。
   **T027 正是检验该疑似作用点因果性的诊断 sprint**，不是在已确认机制上做工程。
4. **严格 prefix-only 因果**：freeze 只读 calibration prefix，apply 只作用于 disjoint
   eval suffix；identity smoke 与方法构造**同包**，不得单立纯 smoke/formalization 包。
5. **复用共享 anchor，不改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、
   或任何 owner/session 文件；不 push**。**允许**：在隔离 sprint 目录内实现不同的更新粒度
   构造（不必、也不应改公共 CMA 文件）。
6. 若共享 testbed 的 identity/fairness 自身无法支持公平比较 → 终态记
   `BLOCKED_SHARED_TESTBED`，不强行收尾、不臆造 signal。
7. **传统 comparator 裁决终态**：若 tuned per-symbol Godard-with-z CMA 已消除 block-64 CMA
   的问题（如 inner-ring collapse），而新构造没有稳定超过它，必须判
   `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`——**这不是 METHOD_SIGNAL**，
   **不形成 active carrier**，只记录"传统算法在更细更新粒度下已解决问题"。

## 1. 背景（理解任务必需的；标"了解即可，不对照评价"）

> 以下仅为执行方理解任务上下文，**不要**拿这些数字/结论当作你的 comparator 或要复现的目标。
> 你要比较的对象是你自己在 §2.3 冻结的 comparator，不是下列历史数字。

- 本 mission 的目标（上层筛选，**非本轮可执行问题**）：判断 ML 是否在双偏振星地 OSL
  接收机链任意处提供真实、合法可比的信息增量。本轮只做诊断构造比较。
- 共享 testbed 的 inherited verdict = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`：**块末**
  固定 μ Godard CMA 在 16QAM 上存在 inner-ring collapse（headroom 0.31–0.33），对 N 与
  MMA 不变。该 headroom 是方法 factory 的合法前提（仅它允许 method 类探索）。
- 前两个 sprint 结论（**只读参考**）：
  - sprint-001：5 个 z-only 后处理/触发/初始化族 **NO_DIAGNOSTIC_SIGNAL**；其 synthesis §4/§8
    把"块末更新几何 + 信道时间变化"**列为疑似吸引子成因**、把冻结块末协议列为"疑似瓶颈"、
    逐符号/更新粒度变体列为"最有信息的下一杠杆"。**注意（门2 纠正）**：sprint-001 §4 的
    "结构性吸引子 + receiver-recoverable gap≈0"广义归因**已被 CP018/D026/V052 拒收**
    （`V052 REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO`，理由：未做
    basin/state-space 扫描、构造与既有候选高度重合）。因此块末更新**不是已确认的因果机制**，
    而是**source-backed、值得验证的疑似作用点**——这正是本 sprint 要检验的因果假设。
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
- **门2 基线失败与候选作用点一致（疑似、非已确认机制）**：sprint-001 `synthesis.v1.md`
  §4（L97-130）把 collapse 诊为疑似"块末更新几何 + 信道时间变化"吸引子；§8（L176-179）把
  冻结的块末协议（block_size=64, μ）列为"疑似瓶颈"，逐符号变体列为"最有信息的下一杠杆"
  ——与基线失败点精确重合。**注意门2 证据等级**：sprint-001 §4 的"结构性吸引子 +
  receiver-recoverable gap≈0"广义因果归因已被 V052 拒收（未做 basin 扫描、与既有候选重合），
  故门2 只证明"候选作用点与基线**观察到的失败位置**一致、且旋钮真实存在"，**不证明块末更新是
  collapse 的已确认成因**。本 sprint 的科学价值正是**用 tuned 传统 comparator 检验该因果性**：
  若 per-symbol Godard-with-z CMA 消除了 collapse，则块末更新确是成因、且问题被传统算法解决
  （判 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`）；若 per-symbol 也 collapse 且新构造
  稳定超越它，才是 `DIAGNOSTIC_METHOD_SIGNAL`。
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
   （更新频率/粒度不同，而非 z-only 标量后处理变体）。本批至少包含以下三类（执行方可在
   其中增补，但不得少于）：
   - **(a) inherited tuned block-64 CMA shared anchor**：corrected μ=0.03 的块末 Godard-with-z
     CMA，即继承基线本身（provenance 同 §2.3，block_size=64）。它既是 anchor 也是 identity 基准。
   - **(b) tuned per-symbol Godard-with-z CMA 传统 comparator**：见 §2.3 冻结定义，dev 单独调 μ。
   - **(c) ≥2 个不同于传统 comparator 的可部署候选**：机制来源建议（执行方自行 dedup 后择优）
     逐符号 stochastic-gradient CMA 的不同变体、更小块（如 block_size=8/16）块末更新、
     块内分段更新、事件触发（divergence/innovation-gated）即时更新、sliding-window recursive
     更新等。**必须与 (b) 机制不同**（不得只是 (b) 换 μ）。
   全部仅消费 receiver-visible 信息（prefix + 公共 16QAM 星座几何 + 冻结公共参数），禁止
   TX-truth/oracle/future-suffix 进 freeze/gate。
3. **Phase C — dev freeze + fresh disjoint test 比较 + 消融**：
   - dev prefix 子集（与 sprint-002 一致的 dev/test 切分策略：dev seeds 181–190 / test seeds
     201–220，**fresh disjoint**）。**禁用已污染 seeds 71–80**（被 ≥6 批复用，失去 held-out 状态）。
   - **公平调谐**：block_size、μ、更新预算（updates-per-symbol）分别在各方法的 dev 集上公平调谐，
     **不得通过多更新次数或错误梯度白占优势**（一个有更多更新的方法若赢，必须在"相同有效更新
     预算"下仍赢，否则只记为更新预算优势、非机制 signal）。
   - **dev 调谐后冻结，再跑 fresh disjoint held-out**；held-out 不回灌任何选择。
   - raw 行逐 (cell,seed,method) 保存；统计单位 = seed-cluster（同 sprint-002），MDE=0.005，
     paired cluster-bootstrap CI（10k resamples, 95%）。
   - **block size × μ / 有效更新预算消融**（必做）：对赢家（若有）补一张 ablation，判断收益究竟
     来自 (i) 更新粒度本身、(ii) 更多更新次数（updates-per-symbol）、还是 (iii) 调参。若收益
     完全可由"更多更新次数"解释，则判 NO_DIAGNOSTIC_SIGNAL（机制无增量），不得判 signal。
4. **同包 identity/语义 smoke**：每个构造需过"输出与基线不同""恒等配置再现不变系统"
   "prefix/eval 因果隔离""constant/trivial 解不能同时满足目标"等适用项；smoke 结果必须
   写进 terminal result artifact，**不得**被 compare 覆盖。
5. **闭合性要求（全闭合）**：paired realization、seed-cluster 统计、raw rows 可复算、
   prefix-only 冻结 receipt、identity/semantic smoke 全部写进同一 terminal `result.json`，
   任一不闭合不得判 signal。

### 2.3 comparator 硬要求（不可省）

- **冻结的传统 comparator = tuned per-symbol standard CMA，canonical Godard-with-z 梯度**。
  权重更新必须为 **Δw ∝ (R²−|z|²)·z·r\***（Godard 1980 原始 per-symbol 形式，每个符号即时更新一次权重）。
  **provenance 必须指向 canonical `cb1_cell_runner` 实现/公式**——即
  `cb1_cell_runner.py:124-129` 的 `(eX * zx_blk)[:,None]*conj(rX_blk)`（标准 CMA 的 per-block 平均
  形式），执行方据此把更新粒度从"块末用块内平均梯度"改为"逐符号即时梯度"，公式身份不变。
- **禁止冒充**：不得用 `common/_cma.py` 的 `CMAEqualizer2x2` 当 comparator。该类实现 **scalar-error**
  梯度 Δw ∝ (R²−|z|²)·r*（`_cma.py:161-166`），**缺 z 因子**，`cb1_cell_runner.py:20-30` docstring
  已明示它无法通过 standard-CMA identity gate。它只能证明 block_size 是真实旋钮，**不得**冒充
  canonical 传统 comparator。
- comparator 的 μ **必须在 dev 上单独调谐**（公平给予调参与验证机会，非"机械套相同超参"）。
  μ 候选网格建议沿用 B01-R interior-optimum 附近（如 {1e-3, 3e-3, 1e-2, 3e-2, 1e-1}，注意 1e-1
  在长 cell 可能发散），选 dev 最优后冻结，再上 held-out。
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

terminal verdict **五选一**，写到 synthesis §0 与 result.json（严格按下列判据，不得越界）：
- `DIAGNOSTIC_METHOD_SIGNAL`：**仅当**至少一个新候选在 tuned per-symbol Godard-with-z
  conventional comparator 下**稳定超过**它，且该优势**非调参、非更新预算、非梯度身份伪影**
  （由 §2.2 消融排除三类替代解释），才可判此。否则不得判 signal。
- `NO_DIAGNOSTIC_SIGNAL`：批次在冻结切片下无可用 signal（新候选未稳定超过 tuned 传统
  comparator，但传统 comparator **未**消除 collapse）。
- `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`：**tuned per-symbol Godard-with-z CMA 已消除
  block-64 CMA 的问题（如 inner-ring collapse）**，而新构造没有稳定超过它。此时**判此终态**，
  **不是 METHOD_SIGNAL**，**不形成 active carrier**，只记录"传统算法在更细更新粒度下已解决该问题"。
  （本终态正是对门2 疑似作用点的因果裁决：块末更新确是 collapse 成因，但传统 per-symbol 更新已解。）
- `BLOCKED_SHARED_TESTBED`：共享 evaluator/baseline/comparator 不能支持公平诊断比较。
- `EXECUTION_INVALID`：执行本身违反合同（identity gate 不过、因果泄漏未修、comparator 用了
  scalar-error `_cma.py` 冒充 canonical、smoke 被覆盖未闭合、或 verifier 不通过且包内一次
  修复仍无法闭合）。

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
7. **门2 因果越界陷阱（本轮新增）**：sprint-001 §4 的"块末更新几何 = 结构性吸引子成因"
   已被 V052 拒收。**不得**把"块末更新是 collapse 成因"当已确认事实写进 synthesis；
   它只是疑似作用点，是否成立由本 sprint 的 tuned 传统 comparator 检验。
8. **comparator 梯度身份陷阱（本轮首要）**：`common/_cma.py` 的 `CMAEqualizer2x2` 是
   scalar-error 梯度（缺 z），用它冒充 canonical Godard-with-z comparator 会使整个比较的
   梯度身份错误 → 判 `EXECUTION_INVALID`。comparator 必须用 `cb1_cell_runner` 的
   Godard-with-z 公式（`cb1_cell_runner.py:124-129`）。
9. **更新预算伪影陷阱**：逐符号/更小块方法天然有更多更新次数。若赢家优势完全来自"更多
   更新次数"而非更新粒度机制，判 NO_SIGNAL 或 PROBLEM_RESOLVED，不得判 signal（见 §2.2 消融）。
10. **PROBLEM_RESOLVED 误判陷阱**：tuned 传统 comparator 已解决问题时，**不得**为了让 sprint
    "出 signal"而强行把它标 NO_SIGNAL 或用欠拟合 comparator 衬托出新候选的赢。问题被传统
    算法解决是合法终态，直接判 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`。
11. **种子污染**：seeds 71–80 已失 held-out 状态（被 ≥6 批复用），本轮禁用。本轮 fresh
    dev/test = 181–190 / 201–220（同 sprint-002，已 collision-scan 过零命中）。

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

- [ ] task-control 块存在且 `validate_task_control.py` PASS（epoch 61 / CP025 / `PREFORMAL_METHOD_FACTORY` 合法）。
- [ ] 继承基线确为 corrected μ=0.03 块末 Godard-with-z CMA，无 μ=0.001 回退证据。
- [ ] ≥3 个构造实际跑通（含 inherited block-64 anchor、tuned per-symbol 传统 comparator、≥2 个
      可部署候选），且全部 prefix-only 因果（TDD ≥5/5 PASS）。
- [ ] **传统 comparator = tuned per-symbol Godard-with-z CMA**，provenance 指向
      `cb1_cell_runner.py:124-129` 公式（canonical，含 z 因子），μ 在 dev 单独调谐；**不得**用
      scalar-error `_cma.py` 冒充——若发现用错梯度身份，直接判 `EXECUTION_INVALID`。
- [ ] block size × μ / 有效更新预算消融已做，赢家优势已排除"调参/更多更新次数/梯度身份"三类伪影。
- [ ] raw/aggregate 以 seed-cluster 为单位；smoke 写进 terminal result 未被覆盖；raw→aggregate 可复算。
- [ ] terminal verdict ∈ {`DIAGNOSTIC_METHOD_SIGNAL`, `NO_DIAGNOSTIC_SIGNAL`,
      `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`, `BLOCKED_SHARED_TESTBED`,
      `EXECUTION_INVALID`}，且 synthesis 对"为什么赢家赢/输家输/有无伪信号/传统 comparator 是否
      已解决问题"有机制解释。`DIAGNOSTIC_METHOD_SIGNAL` 仅在"稳定超过 tuned 传统 comparator +
      非伪影"时判。
- [ ] 未改 `common/`、`params.py`、baseline-atlas、B01/B01-R、C11 raw、任何 owner/session；
      未 push；未把诊断当方法/Go/论文数；未用 seeds 71–80。
- [ ] method-map 逐条对 §3.1 被撤回的频域族 dedup（不得把频域/子带当"更新粒度"重做）。

## 附：产出回传位置

`projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-003/`
（worker-log 写到 `projects/thesis-fso/worker-logs/step-027-*.md`，commit 在当前 fork 分支）
