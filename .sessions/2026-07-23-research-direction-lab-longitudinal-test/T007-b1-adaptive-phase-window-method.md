# T007：B1 自适应相位估计窗方法大包

> 执行环境：`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`
> 当前 formal step：Groundwork Step 4a
> 权威决策：`.sessions/2026-07-06-step4a-mve-execution/decisions.md#D013`
> 前台控制：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 9
  action_class: ADAPTIVE_PHASE_WINDOW_METHOD_PACKAGE
```
<!-- RDL-TASK-CONTROL:END -->

## 任务目标

在**一个 GLM 对话**中完成 B1 固定相位估计窗的结构性问题门，并在门通过时直接完成
三种 receiver-visible 自适应窗方法、paired test 和 provisional verdict。目标是形成
一个可包装的方法，不是再写候选分析；但若“最优窗不随条件稳定变化”或存在普适固定窗，
必须按预注册门立即 Kill，不得靠扩大非典型参数救方法。

问题来自已完成的 Step 1–3 证据，不是标题联想：

- M：固定窗 VV / pilot moving-average phase estimator；
- C：星地 Gamma-Gamma 湍流导致 block SNR 大幅波动，同时存在激光 Wiener phase noise；
- A：一个固定 N 无法同时平衡低 SNR 的噪声平均与高 phase-noise 的跟踪滞后；
- source open problem：sat.1553 明确说最优 N 由 SNR/phase-noise ratio 决定，并要求
  研究动态调整方法与量化收益。

## 开始前必须完整读取

1. 本文件与同目录 `topic-index.md` 顶部 `RDL-CONTROL`；
2. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` 的 D013；
3. `.sessions/2026-07-06-step4a-mve-execution/verifications.md` 的 V001；
4. `.sessions/2026-07-06-step4a-mve-execution/S015-t006-rejection-and-b1-window-activation.md`；
5. `projects/thesis-fso/master-state.md`；
6. `projects/thesis-fso/literature_notes.md` 的 L11/B1-Q1 与总表对应行；
7. 主仓库共享论文笔记
   `D:\code\study\research-protocol\papers\_read_notes\_B1-pilot-window-increment.md`
   和其指向的 sat.1553 `content.md` 相关原文；
8. `stages/groundwork.md`、`stages/gw-feasibility.md`；
9. `thesis-lessons.md` 速查表及 TL-20/TL-22/TL-23/TL-26/TL-27/TL-30–33；
10. `code-quality.md`、`.agents/skills/sim-preflight/SKILL.md`；
11. 现有 `projects/simulation/common/_recovery.py`、`_dual_pol_channel.py`、
    `_modulation.py`、`_config.py` 与已有 VV/BPS/pilot CPE 测试。

T006 的 B10/B12/channel helper 已由 V001 判为 scientific-invalid，**不得复制、导入或
以其结果作本包 baseline**。共享论文库在主仓库、不在 worktree 是正常布局。

## 授权边界

- 只在 GW Step 4a 内工作；不得进入 Step 5、Contract 或 Execute。
- 允许新建：
  - `projects/simulation/explore/adaptive-phase-window/`
  - `projects/simulation/results/adaptive-phase-window/`
  - `projects/simulation/tests/test_adaptive_phase_window.py`
  - `projects/thesis-fso/worker-logs/step-007-b1-adaptive-phase-window-method.md`
- 优先复用 existing common；不得改 shared generator、protected history、
  Direction Lab Skill/controller 或通用基础设施。
- 不修 T006，不恢复 Pilot-Jones/P03/Science Scout，不获取新私有全文。
- 全部技术细节写文件；聊天只返回最后四行。

## A. Source closure、理论预期与 frozen contract

任何 primary run 前写 `source-closure.yaml`、`MVE-SPEC.md` 和 `contract.yaml`：

1. 明确 VV 与 pilot moving-average 的窗口定义、block latency、相位模糊口径；
2. 把参数分成 paper-sourced / canonical-project / validation-tuned；
3. 理论预期必须写成可失败关系：
   - SNR 降低、phase-noise 固定时，最优 N 应倾向增大；
   - linewidth 增大、SNR 固定时，最优 N 应倾向减小；
   - 若趋势不稳定或一个固定 N 在所有 primary cells 内距 oracle-window
     `<0.3 dB`，则没有值得实现的自适应空间；
4. primary conditions 只用有来源的代表区间：
   - clean/control：10 kHz linewidth；
   - operational：20 kHz；
   - adversarial-sourced：80 kHz；
   禁止用 200 kHz–1 MHz 作为 sole/primary 正信号；可做 stress secondary；
5. window grid 至少覆盖 `{8,16,32,64,128,256}`，但所有方法和 fixed baseline
   必须用同一候选集合；
6. uniform 16-QAM、canonical Gamma-Gamma channel、相同 block/pilot overhead/
   realization/data mask/有效 BER denominator；
7. validation seeds 至少 5、test seeds 至少 10，fresh disjoint 且与 T002–T006
   seed pools assert 不相交；
8. SNR grid 必须覆盖 HD-FEC waterfall 两侧，validation 定位后冻结，test 不调参；
9. primary metric：
   - BER=`3.8e-3` 处所需 SNR 的插值差；
   - paired raw BER / log-BER、wins、95% CI；
   - median 与 20% trimmed mean；
   Q² 仅作 secondary，禁止让 BER 接近 0.5 的 seed 经非线性变换主导 verdict；
10. oracle-window 只作 Kill/headroom bound，绝不作 deployable Go 对手。

## B. 必须先过的 semantic 与结构门

### B1. Semantic smoke

至少覆盖：

- noiseless/zero-phase 与 known constant phase；
- known Wiener phase 下 window 增大确实改变平滑/跟踪 trade-off；
- phase sign、linewidth→per-symbol variance、block boundary；
- 16-QAM 的已知 fourth-power `pi/4` deterministic bias 与 `pi/2` ambiguity 分开；
  deployable code 显式校正固定 bias，evaluation 只允许合法 `pi/2` global resolve，
  不得再用“文档 4 rotations、代码 8 rotations”的口径；
- pilot/data mask、equal energy/overhead；
- block-buffered 方法只可读取当前 block，不能读取下一 block；若用 centered window，
  报告固定 latency，并让所有 comparator 享有同等 latency；
- receiver-visible 方法签名不得含 tx bits、true h、true phase、true SNR；
- 每个 method 的 window path 必须随至少两个输入条件发生非退化变化。

任一 semantic gate FAIL：先在本对话修复；若 source identity 仍不能闭合，停止并报
`BLOCKED_SOURCE_IDENTITY`，不得跑 primary。

### B2. Source-native window-optimum sweep

先在静态 AWGN + Wiener PN slice 上扫：

- SNR 至少 `{10,14,18,22}` dB；
- linewidth `{10,20,80}` kHz；
- window grid `{8,16,32,64,128,256}`；
- validation seeds ≥5。

报告每 cell 的最佳 N、第二名 gap、跨 seed 一致性、SNR/linewidth 单调趋势。然后在
canonical GG block fading 上重复最小结构 sweep，判断 oracle per-block window 相对
validation-optimal global fixed N 的合法空间。

**结构门 KILL 条件（满足任一即停止，不实现 C 段）：**

1. 最优 N 对 SNR/linewidth 的方向与理论预期在多数 cells 不一致，且组件追踪不能
   解释；
2. 一个 fixed N 在所有 primary working cells 的 required-SNR regret `<0.3 dB`；
3. oracle per-block window 相对 fixed B* 的 median 或 20% trimmed gain
   `<0.5 dB`，或信号只来自 BER `>=0.2` 的 collapse/out-of-work-region cells；
4. 最优 N 虽变化，但 receiver-visible features 的 held-out prediction
   Spearman `|rho|<0.5` 且 exact-window accuracy 不优于 majority-fixed baseline。

结构门通过才进入 C；失败仍须落 raw rows、tests、synthesis、worker-log，并裁决
`KILL_NO_ADAPTIVE_WINDOW_SPACE`。

## C. 门通过后同包实现三个有界方法

所有映射/阈值只用 validation，test 完全冻结。

1. **P1 analytic ratio rule**
   用 receiver-visible `SNR_hat / phase_innovation_hat` 映射到有限 window grid；
   映射方向必须符合 B1 理论关系，带上下界，不可读取 oracle 最佳 N。
2. **P2 validation lookup + hysteresis**
   对 `(SNR_hat, phase_innovation_hat)` 分箱查表；相邻 block 只有跨过滞回边界才换窗，
   防 window chatter。报告 switch rate 与 latency。
3. **P3 confidence-safe controller**
   用 validation 学到的 per-window regret/confidence 选择 N；低置信度必须退回
   fixed B*，不能用 test labels。模型限定为 frozen ridge/logistic/shallow table，
   不建设深度学习或训练框架。

先做 mechanism slice，必须显示：

- 至少两个物理条件选到不同 N；
- P2 的 hysteresis 比无滞回版本减少 chatter；
- P3 低置信度真的 fallback，且不退化为 oracle label replay；
- block 边界 phase continuity 不因换窗产生跳变。

slice 通过后直接跑完整 primary paired test，不另开下一对话修小毛病。

## D. Baseline 与预注册裁决

Baseline ladder：

- `B* fixed`：validation 上全条件 aggregate 最优的单一 fixed N；
- `fixed-per-condition`：每个 registered condition 用 validation 选一个 fixed N，
  作为更强但仍 deployable comparator；
- legal pilot moving-average CPE；
- validation-tuned BPS；
- oracle per-block N：Kill-only。

裁决：

- `GO_ADAPTIVE_WINDOW_METHOD`：至少一个 P 相对 `B* fixed` 在至少两个 non-stress
  primary conditions 的 FEC-crossing required-SNR gain `>=0.5 dB`，95% CI 下界
  `>0` 或 paired wins `>=7/10`；同时相对 `fixed-per-condition` 不为负，clean
  degradation `<=0.1 dB`，并关闭 oracle-window regret 的至少 50%。
- `ROBUSTNESS_ONLY`：未到 0.5 dB，但显著降低 worst-decile BER/cycle-slip 或扩大
  FEC-working coverage；只能作次级/防御性材料，不包装成主方法。
- `METHOD_FAIL_WITH_SPACE`：oracle window 空间存在，但 P1–P3 均不能稳定关闭。
- `KILL_NO_ADAPTIVE_WINDOW_SPACE`：B2 结构门失败。
- `UNRESOLVED`：FEC crossing/CI/identity 不闭合；不得强判 Go/Kill。

任何正面 verdict 必须同时报告 mean、median、trimmed mean、seed rows、collapse
sensitivity；单个 seed 对 aggregate gain 贡献 `>40%` 时，正面 verdict 自动降为
`UNRESOLVED_OUTLIER_DOMINATED`。

## 证据与测试

至少落盘：

- source-closure、MVE-SPEC、contract；
- source、runner、raw validation/test rows、aggregate/result JSON；
- synthesis、worker-log；
- source/contract SHA、Python/依赖/真实参数。

测试至少覆盖：

- semantic smoke 全项；
- theoretical direction tests；
- legal pi/4 bias correction + pi/2 ambiguity；
- no future/no truth；
- fixed/condition-fixed/oracle 身份分离；
- feature mapping 不退化；
- validation/test isolation；
- raw→aggregate bit-identical；
- median/trimmed/outlier verdict boundaries；
- deterministic subprocess fingerprint；
- UTF-8 explicit read/write；
- T002–T006/protected/shared immutability。

## 收尾

- 本对话只做一次 consolidated commit，不 push。
- 运行并记录：task guard、定向 tests、相关 regression、YAML/JSON parse、
  raw recomputation、source SHA、protected diff、`git diff --check`、`git status`。
- 不更新 formal owner、live control 或 master-state；由主控接收。
- 若支持独立 critic/verifier，使用分离上下文；若不支持，诚实把 final status 上限
  设为 `PARTIAL`，但仍完成全部主包。

最终聊天只返回：

```text
status: PASS|PARTIAL|BLOCKED|FAIL
commit: <40-char SHA>
worker_log: projects/thesis-fso/worker-logs/step-007-b1-adaptive-phase-window-method.md
anomaly: <NONE or one concise anomaly>
```
