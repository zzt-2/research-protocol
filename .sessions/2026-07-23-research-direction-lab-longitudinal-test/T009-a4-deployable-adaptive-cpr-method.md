# T009：A4 可部署自适应 CPR 方法生产与科学身份终审

> 来源：R001 / live D003 / formal D015 / mission CP008
> 执行环境：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> 基线提交：以本文件所在 clean HEAD 为准
> 当前 formal step：Groundwork Step 4a
> 产出：隔离 A4-v2 实现、raw artifacts、method card、synthesis、worker-log、单次 commit

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 14
  action_class: A4_DEPLOYABLE_ADAPTIVE_CPR_METHOD_PACKAGE
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你是执行者，不是主控。在**一个 GLM 对话**内终审并直接生产 A4 方法：

1. 把旧 A4 的 common-payload、pilot/ambiguity、receiver-visible input 与 comparator
   identity 写成可失败 smoke；只允许一次有界修复；
2. identity 通过后，同包冻结并比较 P1 现有两级规则、P2 monotone validation
   selector、P3 confidence-safe selector；
3. 用 fresh paired mixed-condition traces 判断是否形成 `METHOD_SIGNAL`，否则严格报
   `PACKAGING_BOUNDARY`、`METHOD_FAIL_WITH_SPACE` 或 `BLOCKED_IDENTITY`。

不得只做审计、只补测试、只复述旧论文、只写下一轮计划。旧论文、旧 +dB、26/29
选对率和 common-768 数据只作 diagnostic input，不自动构成科学结论。

## 1. 起飞检查

### 1.1 控制、Goal 与 formal owner

1. 确认当前目录、分支、HEAD、clean 状态；不得换到主 worktree。
2. 完整读取本文件、同专题 `topic-index.md` 顶部控制块、`mission-log.md` 全表、
   `R001`、`decisions.md#D003`。
3. 运行：

   ```powershell
   python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
     .sessions/2026-07-23-research-direction-lab-longitudinal-test/T009-a4-deployable-adaptive-cpr-method.md
   ```

   非 PASS 立即停止并回执 `BLOCKED_TASK_CONTROL`。
4. 读取：
   - `projects/thesis-fso/master-state.md` 当前控制面；
   - formal `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D015`；
   - formal S011、S013、A4 bugfix H003、thesis-writing D001/D002/D004–D008；
   - 旧 A4 fixed/common-768/per-regime 脚本、JSON 与报告；
   - formal S011 中已通过 smoke 的 task-matched conventional DPLL 及其实现/结果；
   - `projects/thesis-fso/literature_notes.md` 的 B11/NDA-ML/DA 条目；
   - `stages/groundwork.md`、`stages/gw-feasibility.md` Step 4a；
   - `thesis-lessons.md` 速查与 TL-20/22/23/26/27/29–33；
   - `code-quality.md`；
   - `sim-preflight` 的 constraints、run、add、adaptation-scan、
     mve-validation、param-source、doc-discipline、usage-log。
5. 当前是 GW Step 4a，不进入 Step 5/Contract/Execute。不得更新 formal/current
   owner、mission-log 或论文。

若 formal carrier 不是 `A4_DEPLOYABLE_ADAPTIVE_CPR`，停止为
`BLOCKED_STAGE_OWNER`，不得自行改 owner。

### 1.2 历史结论的继承边界

必须继承为**失效证据**：

- 原 `+0.27–0.48 dB` 全场景增益来自混合分母与 post-hoc oracle，对外禁用；
- `da_full=ne_da/1024` 不是物理公平 data BER；
- pilot on/off goodput 路线已由 D006 Kill，不得复活；
- 固定 13 dB 阈值不是 per-regime measured crossover；
- 旧 selector 使用 nominal/true SNR、TX-label ambiguity resolve 或不同 evaluation
  population 时，不是 deployable method evidence。

可以作为 diagnostic input、但必须 fresh 重验：

- DA/NDA 在不同 SNR/湍流条件下存在 ordering crossover；
- old common-768 selector 对 fixed NDA 的低 SNR 改善；
- per-block oracle 与旧 selector 之间仍有 regret。

旧 A4 全目录只读；v2 必须写独立路径。

## 2. 正向方法合同

- `positive_method_target`：只读取当前/历史接收端可获得统计，在统一 pilot-bearing
  waveform 与 common data mask 上，为每个处理块因果选择 DA 或 NDA CPR。
- `minimal_construct`：
  - **P1 frozen two-stage rule**：复刻现有 CV + effective-SNR 逻辑，但所有阈值只在
    validation 冻结，输入必须 deployable；
  - **P2 monotone selector**：validation-frozen 单调浅表/等距分箱，显式编码
    低可靠度偏 DA、高可靠度允许 NDA，不使用 test label；
  - **P3 confidence-safe selector**：低置信度退回 validation-frozen global best，
    可加一阶 hysteresis，禁止深度模型和通用训练框架。
- `fair_comparator`：
  - fixed DA；
  - fixed NDA；
  - formal S011 已通过 smoke 的 task-matched conventional DPLL；
  - 从 fixed DA、fixed NDA、DPLL 中，仅用 validation 跨全部注册混合条件选出的
    单一 global fixed strategy `B*`；
  - 从同一三者中选出的 per-condition validation-frozen fixed strategy `B-cond`
    （强对照）；
  - per-block oracle 只作 headroom/regret ceiling，不作 Go baseline。
- `primary_packaging`：接收功率感知、块级、可部署的 DA/NDA adaptive CPR。
- `fallback_packaging`：NDA 低可靠区的有界 safeguard、operating boundary 或
  complexity/robustness trade-off；只有满足 §7 才可记 `PACKAGING_BOUNDARY`。
- `next_positive_action`：identity smoke 通过后立即跑 P1–P3 fresh paired
  comparison，不再另派方法实现包。

## 3. 先冻结 A4-v2 contract

在 `projects/simulation/explore/a4-deployable-adaptive-cpr-v2/` 创建并在任何
primary test 前冻结：

- `source-closure.yaml`
- `MVE-SPEC.md`
- `contract.yaml`
- `seed-census.yaml`
- `theory-expectation.md`

### 3.1 Fresh seed 与混合条件

用确定性脚本盘点旧 A4、T002–T008 及相关 results 中已观察 seed。冻结：

- validation seeds ≥10；
- test seeds ≥10，二者和历史观察池两两不交；
- `(condition, seed, block)` realization 在所有 arm 间成对共享；
- test 开始后不得改阈值、bin、feature、fallback、condition weight 或 comparator。

primary 是预注册的 **mixed-condition traces**，至少覆盖 weak/moderate/strong 和
低/中/高 SNR 的有来源 working region。condition 序列与 dwell-time 在 contract
冻结；selector 不得读取 turbulence label、test cell id 或 future block。单 cell
曲线只作分解，不能替代 mixed-trace 主判据。

### 3.2 统一信号与评价 population

- 所有 arm 使用同一 transmitter waveform、pilot pattern、总能量、通道 realization、
  common data mask、latency 和 BER denominator；
- 若固定 pilot pattern 存在，NDA 可以忽略 pilot 值，但不得把 pilot 位置当额外 data；
- DA/NDA 的 ambiguity 必须由同一组已知 pilot/causal decision 规则解决；TX truth
  只能用于 evaluator 计错和明确标记的 oracle，不能进入 deployable arm；
- selector 的 SNR/noise/power 输入必须由 receiver-visible estimate 得到；不得直接
  读取 simulator `gamma_db/gamma_lin`、true h、true turbulence 或 TX bits；
- actual required-SNR 只能由覆盖 FEC crossing 的曲线插值得到；无 crossing 时报告
  raw/log-BER 与 `UNRESOLVED_NO_CROSSING`，不得造 proxy dB；
- pilot overhead 单列为 spectral-efficiency/complexity 账，不用错误分母奖励任一 arm。

## 4. REQUIRED identity smoke

以下全过才可运行 primary；只允许一次有界修复，仍失败则
`BLOCKED_IDENTITY`：

1. **source/algorithm identity**：DA 与 NDA 公式、phase sign、frequency stage、
   16-APSK ambiguity、pilot spacing 和 processing latency 逐项对照原正式来源；
   公式带页码/编号，缺公式不得凭文字重建。DPLL 必须复用/核验 formal S011 的
   DD 闭环实现身份：用最近邻 16-APSK hard decision adapter，VCO 状态在完整
   mixed trace 上跨 block 连续累积，禁止逐块重置。
2. **waveform/information identity**：同一 waveform 和 common mask；deployable
   方法不读 true SNR/h/phase/turbulence/TX labels/future block。
3. **ambiguity identity**：pilot/causal resolve 在 held-out data 上可运行；
   去除 evaluator TX truth 后基线仍在可靠 working region。
4. **comparator identity**：fixed DA、fixed NDA 与 formal S011 已通过 smoke 的
   task-matched conventional DPLL 均进入候选集。DPLL 的 `omega_n`/其他环路参数
   只在 validation 冻结，不得用 primary test 调参；B* 仅由 validation 跨注册
   混合条件冻结，B-cond 也只读 validation；禁止 per-seed/per-test 重选。
5. **metric identity**：BER population、FEC crossing、pilot overhead 与 oracle
   candidate 对所有 arm 一致；旧 mixed/full/data 口径不得混用。
6. **mechanism identity**：至少两个有来源条件下 DA/NDA ordering 不同，且差异不由
   单 seed、BER≥0.2、no-crossing 或 evaluator collapse 制造。
7. **causality/non-degeneration**：改变当前 block 的 receiver-visible power/innovation
   时 P1–P3 输出能发生预期变化；改变 future block 不影响当前动作。

primary 前还必须独立复现 formal S011 的 DPLL working-region smoke：在 S011 原
16-APSK/AWGN/18 dB 身份下，连续 VCO 的 BER 落入预期 `0.003–0.006`，且逐块
重置必须表现出 S011 已记录的明显恶化（历史锚点约 `4.1e-3 → 7.5e-3`）。该 smoke
只验证实现身份，不用于 T009 调参或方法增益；无法复现则直接
`BLOCKED_IDENTITY`，不得运行 primary。

另做 noiseless、known phase/frequency、AWGN、pilot corruption、π/2 branch、
block boundary、raw→aggregate、deterministic subprocess、UTF-8 与 source-hash tests。
consistency PASS 不能替代上述算法正确性。

## 5. 同包完成三个方法

identity 全过后：

### P1 frozen two-stage rule

- 从旧 A4 迁移 CV/effective-SNR 思路，不迁移 true-SNR 输入；
- validation 冻结阈值与 fallback；禁止按 regime/test 重标 13 dB；
- 报 selector action、switch rate、latency、per-condition confusion 与 regret。

### P2 monotone validation selector

- 只用 2–3 个已证明 receiver-visible 的浅特征；
- 采用单调表、isotonic/浅分箱或等价可解释规则；复杂度上限写入 contract；
- 若单调约束与 validation ordering 冲突，记录冲突，不用高容量模型硬拟合。

### P3 confidence-safe selector

- 低置信度回退 B*；可用 validation-frozen margin 与一阶 hysteresis；
- 与无 confidence、无 hysteresis、majority/global-fixed 做消融；
- 不能用 oracle label replay、test calibration 或 post-hoc condition weighting。

先做小 mechanism slice；只要 identity 已通过，不得因 P1 表现差就跳过 P2/P3。
随后直接跑完整 fresh paired test。

## 6. Cheap alternatives 与物理攻击

必须正面回答：

1. always-DA 是否已经支配自适应策略；
2. always-NDA 是否在同 overhead/common mask 下等价；
3. 已通过 smoke 的 task-matched conventional DPLL 是否支配 DA/NDA 自适应策略；
4. B-cond 若有条件标签时能达到什么上界；
5. 简单单阈值相对 P2/P3 是否已足够；
6. 增益是否只来自 pilot bookkeeping、TX-label ambiguity、test condition weighting、
   collapse cells 或单 seed；
7. selector 的额外 complexity/latency 是否值得其收益。

若 P 只胜 fixed NDA、却被 always-DA、DPLL 或 validation-frozen B* 支配，最高
`PACKAGING_BOUNDARY`，不得报 `METHOD_SIGNAL`；若 DPLL 是 B*，则必须直接以
DPLL 作为下述增益判据的分母。

## 7. 裁决与 method delta

`METHOD_SIGNAL` 必须同时满足：

- 至少一个 P 相对从 fixed DA、fixed NDA、DPLL 冻结得到的 strongest-conventional
  B*，在至少两个 non-stress primary subconditions 的合法 required-SNR gain
  `>=0.5 dB`，且 mixed-trace aggregate 同方向；
- paired-bootstrap 95% CI lower `>0`，paired win fraction `>=0.70`；
- 相对 B-cond 不显著为负，clean degradation `<=0.1 dB`；
- 关闭 per-block oracle regret 至少 50%，单 seed/cell 贡献不超过 40%；
- cheap-alternative、identity、physical-cause 与 independent verifier 攻击通过。

`PROMOTION_READY`：`METHOD_SIGNAL` + 传统 estimator/参数消融稳健 + method card
完整 + 独立重算一致；执行方不得自行写 formal owner。

`PACKAGING_BOUNDARY`：未达到 `METHOD_SIGNAL`，但以合法 comparator 显著扩大
FEC-working coverage、降低 worst-decile/cycle-slip，或形成可 defensible 的 NDA
safeguard；必须明确 always-DA 的代价/优势，不能把“只胜弱对手”写成主方法。
若被 task-matched DPLL 支配，只能在上述 boundary 证据独立成立时使用该裁决，
不得报 `METHOD_SIGNAL` 或 `PROMOTION_READY`。

`METHOD_FAIL_WITH_SPACE`：合法 oracle 空间存在，但 P1–P3 均不能稳定关闭。

`BLOCKED_IDENTITY`：一次有界修复后仍有任一 §4 基础身份失败。

worker-log 必须分别写：

- `formal_science_disposition`
- `mission_method_delta`：`NONE / CONSTRUCT_CREATED / FAIR_COMPARISON_RUN /
  METHOD_SIGNAL / PACKAGING_BOUNDARY / PROMOTION_READY`
- 建议的 same-axis、repair、no-method streak 与 drift（主控最终裁决）

测试 PASS、negative result、evaluator 修复或治理闭包不得记为方法增量。

## 8. 文件边界

允许新建/修改：

- `projects/simulation/explore/a4-deployable-adaptive-cpr-v2/**`
- `projects/simulation/results/a4-deployable-adaptive-cpr-v2/**`
- `projects/simulation/tests/test_a4_deployable_adaptive_cpr_v2.py`
- `projects/thesis-fso/worker-logs/step-009-a4-deployable-adaptive-cpr-v2.md`
- `.sessions/sim-preflight-log/usage-2026-07.md`（只追加本次一行日志）

禁止修改：

- 所有旧 A4/NDA sandbox 源码、JSON、报告；
- T001–T008、旧 worker-log/artifacts；
- `projects/simulation/common/**`、`params.py`、formulas-master、CONCLUSIONS；
- CCISP 论文正文、图和表；
- portfolio/state/harvest/master-state、formal decisions/verifications；
- live topic、mission-log、Skill/controller、protected history；
- B1、B10/B12、Pilot-Jones、P03/Scout。

必须改 shared common、params、论文或 owner 才能继续时，停止为
`BLOCKED_SHARED_CHANGE_REQUIRED`。

## 9. 产出与验证

必须落盘：

- source closure、theory expectation、frozen contract、seed census、source hashes；
- A4-v2 implementation、tests 与 raw validation/test rows；
- selection manifest、aggregate/result；
- fixed DA、fixed NDA、DPLL、B* 与 B-cond 的逐条件和 mixed-trace 对照结果；
- method card：technical action、deployable inputs、comparators、mechanism、
  cheap alternatives、boundary、claim ceiling、primary/fallback packaging；
- synthesis；
- worker-log。

验证至少覆盖：

- task guard；
- §4 七类 identity；
- no-truth/no-future；
- seed isolation、paired realization、real crossing/no-crossing discipline；
- raw→aggregate 独立重算；
- deterministic rerun、YAML/JSON parse、UTF-8；
- forbidden-path diff、`git diff --check`；
- sim-preflight usage-log 追加。

实现与 verifier 分离；若无法独立验证，科学正面最高 `PARTIAL`。本对话只做一次
consolidated commit，不 push，commit 后 worktree clean。

## 10. 给主控的极短回执

用户只需转发以下四行，不读取技术日志：

```text
STATUS: <DONE|BLOCKED>
COMMIT: <sha|none>
WORKER_LOG: projects/thesis-fso/worker-logs/step-009-a4-deployable-adaptive-cpr-v2.md
VERDICT: <METHOD_SIGNAL|PROMOTION_READY|PACKAGING_BOUNDARY|METHOD_FAIL_WITH_SPACE|BLOCKED_IDENTITY|BLOCKED_STAGE_OWNER|BLOCKED_TASK_CONTROL|BLOCKED_SHARED_CHANGE_REQUIRED>
```
