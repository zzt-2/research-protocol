# [S008] P02/U10 与 P03/U19 Capability Triage

> 2026-07-18 | Scout / Capability Triage | 状态：完成（B：均未达到 SCOUT_CONTRACT_READY）

## 目标

按 DL-Process v0.3 的 Universal Core + Communications Profile + dual-pol OSL Project Adapter，对 P02/U10 和 P03/U19 做能力、因果输入、输出、runner 承载和最小 smoke 可行性分诊；不启动 B004，不建立 Queue/Registry/fingerprint，不改 B001–B003。

## 记录

### 输入与分层

- 读取并核对 `projects/thesis-fso/direction-lab/process.md`、`profiles/communications.yaml`、`adapters/dual-pol-osl.yaml`、`anchor.yaml`、`candidate-universe.yaml`、`candidate-map.v2.yaml`、`batch-plan.v1.yaml`、standard-CMA runner、双偏振信道和现有 failure/defer 证据。
- 新建 `scout/capability-triage.v1.yaml` 及两个候选 Scout contract。没有新建 Queue、Registry 或 fingerprint。
- P01/U25 只继承 D010 的具体失败证据，状态标签按用户要求改为 `DEFERRED_ARCHITECTURE`；没有修改 P01 代码或 U24 runner。

### P02/U10

能力为 `observational + estimative`，只产生 receiver-only lock-loss/cycle-slip score、事件类型、持久性和 warning lead，不改变 receiver state。合法 runtime 必须来自双偏振 standard-CMA 后的常规 CPR 输出、phase estimate、innovation、confidence/residual 和当前时间索引；TX truth、true h/Jones、未来窗口和 BER 只能留在验证侧。

已有资产是单载波 FOE/DPLL/VV/BPS、邻接 phase-noise generator 和单载波 tracker；当前双偏振 generator 只有 GG envelope、SOP rotation 和 AWGN，现有 v3 artifact 只有 CMA blind trace 四个统计字段，不能把这些字段改名为 CPR event。缺口是整段双偏振 carrier impairment → CPR → receiver trace → event library/persistence validator，因此 runner path 为 `NOT_RUNNABLE`，状态为 `NOT_RUNNABLE`（资产层 `PARTIAL`）。

### P03/U19

能力为 `estimative`，残差失配扫描可以先作 `observational` 诊断；不改变 receiver state。合法 runtime 输入是 standard-CMA 当前/历史 `zX/zY` complex window、块起止索引，以及明确来源的 receiver-side CSI/noise estimate（第一版可声明 `CSI_NONE`）；sX/sY、TX bits、true h/theta/Jones 和 fixed/PI BER 只能训练/评估使用。

`run_b001.py` 的真实 standard-CMA adapter 确实生成 `zX/zY`，但 `run_v3.py` 和 B003 artifact 只持久化 blind trace/派生特征；现有 ML detector 也只消费标量 trace。缺口是 z-window causal adapter、残差 artifact、合法 CSI/noise contract、同信息量 analytic comparator 及 calibration/tail metrics。因此 runner capability 为 `PARTIAL`，但 triage status 仍为 `NOT_RUNNABLE`。

P03 是两者中的最短闭合路径，但当前还不能把 Scout contract 说成已通过；最小 smoke 必须先能从一个真实 standard-CMA `z` window 产生带 source pointer 的 receiver-only artifact，拒绝 oracle/future/post-hoc 字段，并与同信息量 analytic detector 确定性对比。

### 决定

结果为 `B_ALL_CANDIDATES_NOT_RUNNABLE`。不是因为方法族被 Kill，而是因为两个候选都缺可执行的完整输入—因果边界—可复现输出—合法 comparator—最小 smoke 闭合链。下一步优先补 P03 的最小闭合；若失败，再回 Candidate Universe 检查 U23 连续质量估计是否能作为不同输出头形成独立信息增量。

## 决策引用

- D011：DL-Process v0.3 下的能力分诊与 P01 延后（新建）
- D010：P01 当前 standard-CMA 接口的具体阻断证据
- D044：residual cascade 的历史 DEFER 仅作用于原具体路线/域，不自动否决 U19 新机制

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

仅允许写 P03 gap-closure contract 或回到开放 Universe 做下一机制族 triage；在新的 Scout contract 真正通过前，不得创建 PASS Queue、Registry/fingerprint 或启动 B004。

## 续接：P03 Interface Closure Sprint（2026-07-18）

### 目标

在不启动 B004、不创建正式性能 cell、不修改 B002/B003/canonical baseline 的前提下，把 P03/U19 的多个相互依赖接口作为一个完整 Sprint 连续闭合到 `SCOUT_CONTRACT_READY` 或给出真实阻断。

### 记录

- z-window adapter 已接入真实 `run_b001._default_runner` standard-CMA 输出；仅接收 `zX/zY/valid_mask/blind_trace`，输出固定 `direction-lab.p03-z-window.v1`，显式记录 shape/dtype/unit/时间索引/causal availability/source pointer；TX truth、true h/Jones、future、BER/post-hoc 字段递归拒绝。
- `CSI_NONE` 路径已真实运行；`RECEIVER_ESTIMATED_CSI` 仅保留有 provenance 和可用时间约束的声明 schema，当前 comparator 不伪装支持该等级。
- analytic comparator 为同信息量固定 QPSK nearest-neighbour，输入只用 z-window 与显式 alphabet amplitude；零轴 tie 规则、复杂度、state mutation、确定性和 monotonicity 均测试。
- residual artifact 固定 `z - comparator_predicted_mean` 定义，输出 conditional moments、显式阈值 tail mass 和跨 cell stability；fixed-label BER 与 PI-BER 作为 evaluation-only 分离字段，one-cell 状态为 `NOT_ESTIMABLE_ONE_CELL`，没有把残差数值写成性能或 ML headroom 结论。
- isolated deterministic smoke 通过 frozen dual-pol generator → frozen standard-CMA runner → adapter → comparator → residual artifact，使用显式 512 symbol / eval `[133,389)` 参数；只生成 `scout/.../artifacts/interface-smoke-v2/`，不写 evidence ledger、Queue、Registry、canonical state 或论文材料。
- 独立 verifier 发现并促成两项真实修正：JSON hash 改为 bytes 写入以消除 Windows newline hash 漂移；residual builder 强制绑定合法 comparator ID、receiver state 不变和 z input contract。补强后 P03 专项测试为 35 passed。
- `candidate-components.v1.yaml` 是 candidate-level snapshot，不是 canonical registry；`scout-contract.v2.yaml` 达到 `SCOUT_CONTRACT_READY`，sandbox 仍 `NOT_ENTERED`。

### 范围确认

- 本续接是否在 scope boundary 内：是。仍为 Scout/interface smoke；没有 Queue、Sandbox batch、B004 或论文晋级。

### 后续

- 进入下一轮前仍需实现真实 U19 ML mechanism、multi-cell diagnostic budget、evaluation-only fixed/PI evaluator binding，并重新设计机制级 Sandbox comparison；未满足前不得创建 PASS Queue。
