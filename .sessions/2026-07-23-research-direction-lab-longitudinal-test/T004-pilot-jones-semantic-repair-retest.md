# Task Brief: Pilot-Jones complex-model 语义修复、重测与条件式方法 MVE

> 来源: S001 / formal D064 / V038 | 产出位置: thesis-fso formal GW Step 4a
> 日期: 2026-07-23
> 唯一文档: 执行方只需拿到本 T；可读取本 T 指定的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 6
  action_class: PILOT_JONES_SEMANTIC_REPAIR_RETEST_PACKAGE
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在：

`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`

分支必须是：

`codex/research-direction-lab-longitudinal-test`

T003 提交 `5445a2e8899928b8f69d9df811212e913155f8f9` 不能按科学 PASS 接收。主控
V038/D064 已定位五项独立语义缺陷：component channel 施加在含噪 RX、PMD pilot
未经过 FIR、B3 tapped 做 RX→RX 自预测、PMD oracle 非 ceiling、problem gate 与
P1 success 混合。

**你的任务**：在一个 GLM 对话内完成 T003 失败复现 → 可失败 semantic tests →
隔离重建 signal/noise/pilot/channel → 合法 conventional baseline + oracle →
M0–M4 paired headroom 重测 → problem 存活时同包完成 2–3 个机制候选和有界 MVE →
双审查 → provisional verdict。

**这不是“修到旧结论重新 PASS”任务。** 修复后可能出现问题存活、方法失败、
stress-only、物理范围不成立或 scoped negative；按数据裁决。

### 最高纪律

1. 当前 formal step = **GW Step 4a 维度 D 的证据修复**；不得进入 Step 5、
   Contract 或 Execute。
2. **T003 目录、raw、result、synthesis immutable**。新建 repair 隔离闭包，
   不覆盖旧失败证据。
3. 先让 semantic tests 能在旧 T003 实现上复现 FAIL，再实现修复；测试未全过不得
   跑 headroom，更不得给科学 verdict。
4. `problem_survives` 与 `method_succeeds` 必须分离。P1/P2/P3 失败不能推出问题
   不存在。
5. Go 对手是 validation 冻结的**最强合法传统 baseline B\***；oracle 只作 ceiling/
   Kill。B\* 由结果选择时必须只用 validation，不得偷看 test。
6. verified physical range 与 `UNVERIFIED_STRESS_ONLY` 分开。stress 正信号不能
   支持正面物理 verdict。
7. 任一 receiver-visible arm 稳定优于“oracle”，立即停止 verdict，先修 oracle/
   metric/channel；不得以统计波动敷衍明显反常。
8. 不改 shared canonical generator、`common/`、`params.py`、protected history、
   Skill/controller；不复活 Scout/P03；不获取私有全文；不 push。
9. 不得因包大、tests/SHA/provenance 全绿就声称科学 PASS；C4/C6–C8、TL-02/
   TL-20/TL-22/TL-29 是科学门。
10. 一个 consolidated commit；回传只给四行。

---

## 1. 权威状态与必读

按顺序完整读取：

1. 本 T；
2. `projects/thesis-fso/master-state.md` 顶部、§2 与 GW Progress；
3. formal `decisions.md` D062/D063/**D064**；
4. formal `verifications.md` V036/V037/**V038**；
5. S079、S080（含主控 amendment）；
6. T003：
   - `complex_jones_channel.py`
   - `conventional_baselines.py`
   - `salvage_methods.py`
   - `run_salvage.py`
   - `run_all.py`
   - `salvage-contract.yaml`
   - `result.json`
   - directed tests
   - worker-log/synthesis；
7. `stages/groundwork.md`、`stages/gw-feasibility.md` Step 4a；
8. `thesis-lessons.md` 速查表与 TL-02/11/13/20/22/23/25/26/27/29–33；
9. `code-quality.md` 与 `reference/sim-template/` 对应模板；
10. `.agents/skills/sim-preflight/SKILL.md`，并确认本包属于 GW MVE，使用
    `rules/mve-validation.md`、`rules/adaptation-scan.md`，不套 Execute 状态迁移。

记录 branch、start HEAD、`git status --short`、T003 source/result SHA 和以下
protected SHA。若 worktree 初始不 clean，只能停止并报告，不得清理用户改动。

### protected / immutable

- `projects/thesis-fso/direction-lab/STATUS.v1.md`
- `projects/thesis-fso/direction-lab/project.v1.yaml`
- `projects/thesis-fso/direction-lab/canonical-state.yaml`
- `projects/thesis-fso/direction-lab/state/completion-events.jsonl`
- `.agents/skills/`
- T002 全部 contract/result
- T003 `projects/simulation/explore/pilot-jones-complex-salvage/`
- T003 `projects/simulation/results/pilot-jones-complex-salvage/`
- T003 `projects/simulation/tests/test_pilot_jones_complex_salvage.py`

---

## 2. Phase 0：把 T003 五项失败变成可执行 regression

新建：

`projects/simulation/tests/test_pilot_jones_complex_repair.py`

先写测试/诊断，证明旧 T003 会失败。至少覆盖：

1. **noise placement FAIL**：对同一 clean signal/noise，旧实现执行
   `J(clean+noise)` 后再 `J^-1`，输出与 M0 恒等；证明 PDL-flat 是 construction
   identity，而非 impairment absence。
2. **PDL passivity FAIL**：旧 `g=[cond,1]` 在 PDL>0 时最大奇异值>1；primary
   passive PDL 应满足 `σmax≤1` 且 `cond=10^(PDL_dB/20)`。
3. **pre-channel pilot FAIL**：非零 PMD 下，旧 pilot RX 不等于“将含 pilot 的完整
   TX frame 经过相同 PMD channel + same noise”。
4. **tapped target FAIL**：静态/行为两种证据确认旧 B3 的 training target 是 RX
   center，不是已知 TX pilot。
5. **PMD oracle ceiling FAIL**：从 T003 result 精确断言 M3 6/40 ps 有
   `B1 BER < oracle BER`；新修复 smoke 中不得复现这一结构反常。
6. **gate separation FAIL**：构造“problem gap 存活但 P 全输”的 synthetic
   summary，旧 `decide()` 不得被允许输出 model-not-justified。
7. **trend definition FAIL**：构造随 impairment 单调增长但起点低于 M0 的序列，
   旧 gate 不得把“相对 M0 每点>0.05”冒充 monotonic trend 定义。

测试可以通过显式 `xfail(strict=True)` 或单独 legacy-regression mode 证明旧实现
失败；最终 repair tests 必须对新实现 PASS。不得修改旧代码让 legacy failure 消失。

Phase 0 结束先写 `semantic-failure-reproduction.json`，包含每项
`old_behavior | expected_semantics | reproduced | source_line`。

---

## 3. Phase 1：冻结正确 signal/noise/pilot/channel contract

新建隔离目录：

`projects/simulation/explore/pilot-jones-complex-repair/`

至少包含：

- `repair-contract.yaml`
- `semantic_channel.py`
- `pilot_and_baselines.py`
- `repair_methods.py`
- `run_repair.py`
- `run_all.py`
- `synthesis.md`

### 3.1 primary 信号链

在 contract 中明确 primary 模型：

```text
TX full frame（先替换 pilot）
  -> sqrt(h) R(theta) atmospheric clean signal
  -> passive component Jones / PMD / PDL channel
  -> post-component receiver AWGN（复用 canonical 同一 noise draw）
  -> receiver
```

从 canonical realization 分离：

```text
clean_original = sqrt(h) R(theta) @ s_original
n_post = r_canonical - clean_original
```

对含 pilot 的完整 TX frame 重新计算 `clean_pilot`，再执行 component channel，最后
加同一 `n_post`。**不得把 component channel 乘到 `n_post` 上。**

若物理证据支持 component 前噪声，允许增加一个明确标为 sensitivity 的
`PRE_COMPONENT_NOISE` 模型；不得与 primary 混合，也不得用它替换 post-component
结论。没有来源时不加。

### 3.2 PDL

primary passive PDL 使用：

```text
singular values = [1, 10^(-PDL_dB/20)]
cond = 10^(PDL_dB/20)
```

任意 average-power normalization 只能作为单独 sensitivity，不能偷改 primary
SNR。报告总 insertion loss、两路 gain 和 noise covariance。

### 3.3 PMD / M4

- PMD 必须作用于**完整含 pilot 的 frame clean signal**，不能只替换 pilot 样点。
- DGD=0 必须退化为同一 memoryless Jones。
- 卷积边界不能用每 block edge replication 人为清除跨边界 ISI；使用显式 guard/
  overlap 或在 metric denominator 中排除有理论依据的 transient，并报告排除数。
- M4=PDL+PMD 必须复用同一可组合 channel operator。至少完成 limiting-case
  semantic smoke；若要把 verdict 扩到 joint axis，必须有合法 joint oracle/B\*。

### 3.4 paired realization

每 `(cell,seed)` 只生成一次 h/theta/TX/noise/component truth，所有 B/P/O 共享。
verified、stress、validation、test seeds 全部显式 disjoint，且不与 T002/T003
observed seeds 重叠。

---

## 4. Phase 2：可失败 semantic gates

在任何 headroom probe 前，以下必须全 PASS：

1. M0 repaired primary 与 canonical 在 zero component impairment 下 byte-compatible。
2. `n_post` 在不同 PDL/PMD strength 下逐样点相同；component 只作用 clean signal。
3. passive PDL `σmax≤1`、cond/dB exact；PDL 增大时弱 PSP 的 received SNR 不可反常
   增大。
4. pre-channel pilot：pilot/data 均走同一 operator；PMD 下改变一个 pilot 会按 FIR
   支撑影响邻近输出，不只影响该样点。
5. DGD=0 no-op；非零 DGD 有频选/ISI；transient denominator 明确。
6. tapped baseline 训练映射必须是 `RX window -> known TX pilot target`；源码和行为
   双检。
7. noiseless exact-truth oracle 对 M0/M1/M2/M3/M4 在允许 transient 外恢复误差
   `<1e-10`；做不到的模型不得进入 headroom。
8. receiver-visible B3 在 synthetic noiseless PMD 上必须优于 identity/no-op；
   否则 B3 task fit FAIL。
9. oracle dominance sanity：
   - noiseless：O 不得输任何 receiver-visible arm；
   - noisy paired validation：若 B/P 平均 BER 显著优于 O，标
     `ORACLE_INVALID`，停止科学 verdict并 root-cause；
   - 不用单 seed 微小波动硬作 deterministic ceiling。
10. fixed-label/PI-BER、BER→Q²、zero-error bound、mask/denominator 校准 PASS。
11. problem gate 与 method gate 的 unit tests 完全独立。
12. M4 未闭合时，claim ceiling 自动排除 joint axis，不能写“family/complex model
    已关闭”。

任一 FAIL：允许同包修一次；仍 FAIL → `PARTIAL_SEMANTIC_REPAIR_BLOCKED`，停止
performance probe，不得通过增加 seeds 掩盖。

---

## 5. Phase 3：合法 conventional baseline ladder

至少实现并 validation 调参：

- B0：no-op / identity diagnostic；
- B1：single-tap block pilot LS + frozen EMA09（历史 conventional）；
- B2：regularized single-tap/polar inverse；
- B3-PDL：passive-PDL task-matched regularized inverse/whitening；
- B3-PMD：真正的 2×2 tapped pilot-LS/LMS，target=known TX pilots；
- B4-FDE（若 pilot budget/实现允许）：conventional frequency-domain/tapped
  equalizer，用同样 legal pilots/state；
- O：true full channel + noise variance 的 ZF/MMSE oracle，只作 ceiling/Kill。

### baseline adjudication

1. B\* 是每个 model family 在 validation 上冻结的最强合法传统 baseline，候选至少
   包括 B1 和 task-matched B3/B4；不得因为名字叫 B3 就自动当 strongest。
2. B\* 与 P 具有同 pilot overhead、同 data mask、同 eval window、同 channel/noise、
   可比 tuning budget。公平是 equal opportunity，不是强迫同超参数。
3. 报告：
   `claim | B* identity | task fit | information | tuning grid | selected config |
   convergence | obvious cheap extension | stop reason`。
4. 若 B1 胜 B3，则 B1 就是该 slice 的 B\*，同时诊断 B3 为什么不适配；不得隐藏。
5. 若没有一个 B3/B4 能在 synthetic PMD semantic case 超过 no-op，状态为
   `BASELINE_INVALID`，不能进行 method verdict。

---

## 6. Phase 4：分离 problem-survival 与 method-success

### 6.1 problem-survival probe（不含 P 判据）

paired 比较 B\* 与有效 O：

- M0 control；
- M1 complex-unitary；
- M2 verified PDL + 至少 2 个 stress PDL；
- M3 verified DGD + 至少 2 个 stress DGD；
- M4 verified/joint sensitivity（semantic + oracle 均闭合才纳入 verdict）；
- clean + 至少两个 SNR/湍流条件；
- pilot 4/6 sensitivity，若 block size 不容 6 则说明。

分别报告：

- absolute B\*→O BER/Q² headroom；
- paired impairment increment：
  `(headroom_impairment - headroom_M0)`，同 seed/同基础 realization；
- headroom vs impairment strength 的单调趋势与不确定性；
- outage/block-error/失败边界（A5/A6）；
- verified 与 stress-only。

`problem_survives` 只能基于：

1. semantic gates 全 PASS；
2. 合法 B\* 到 O 有预注册实用 gap；
3. gap 相对 paired M0 是 impairment-added，而非 common deep-fade floor；
4. 多 seed 方向稳定；
5. verified physical range 支持正面物理裁决。

找不到 defensible 0.5 dB Q²/SNR-equivalent 映射时，标
`PARTIAL_BLOCKED_THRESHOLD_NOT_JUSTIFIED`，不得用 BER ratio 代替。

### 6.2 方法包（仅 problem 存活时）

先执行 adaptation-scan A1–A6，避免锁死 P1。至少形成并比较 2–3 个机制不同候选，
可从下列选取但须写清是否只是 B\* 参数化：

- P1：pilot reliability/covariance-weighted Jones/tapped estimate；
- P2：uncertainty-aware temporal tracker（RLS/KF/innovation state）；
- P3：physics-structured joint PDL/PMD tracker/equalizer；
- P4：若发现有物理 crossover，可做 condition-aware B1/B3 switch。

每个必须写：

`M-C-A | legal inputs | causal state | equation/source | output | complexity |
strongest cheap alternative | ablation | falsifier | packaging claim`

不是为了凑 3 个；数学同族/别名立即合并。至少包括：

- B\*；
- proposed full；
- mechanism-off/naive ablation；
- 最显然的 conventional ancestor（RLS/KF/LMS/FDE 中适用者）。

### 6.3 条件式 MVE

problem 存活后，本包直接完成 frozen validation → fresh test：

- primary fixed-label BER/Q²；
- PI-BER、outage/block error、per-block variance、recovery/convergence；
- paired exact W/T/L + effect + interval/test；
- clean non-regression；
- 4/6 pilot sensitivity；
- component-off、adaptation-off；
- complexity/state；
- raw rows + aggregate。

P 输 B\*：`METHOD_CANDIDATES_FAIL_ON_SURVIVING_PROBLEM`，不是 model-not-justified。

---

## 7. Phase 5：双审查

若支持独立 agent，至少两个分离上下文：

### Integrity verifier

- old-failure reproduction；
- channel operator 与 noise placement；
- pre-channel pilot；
- passive PDL；
- PMD/M4 limiting cases；
- B3 RX→TX target；
- oracle dominance；
- source/contract/result SHA；
- seeds/mask/denominator；
- raw→aggregate；
- gate separation；
- protected/immutable paths；
- tests、YAML/JSON、`git diff --check`。

### Science critic

攻击：

- post/pre-noise 选择是否偷造方法空间；
- passive PDL 是否把 insertion loss 与 polarization conditioning 混淆；
- blockwise PMD 边界是否假造/抹除 ISI；
- contiguous 4/6 pilots 是否足够训练 tapped baseline；
- B\* 是否真是 validation 最强传统方法；
- oracle 是否仍漏 SOP/h/PMD ordering；
- problem gap 是否只是 metric/permutation/transient；
- P 是否只是 B\*/RLS/KF/FDE 别名；
- positive 是否仅 stress-only；
- M4 缺失是否限制 claim；
- 4 篇全文债对 novelty ceiling 的影响。

若独立 reviewer 不可用，总状态最高
`PARTIAL_INDEPENDENT_REVIEW_UNAVAILABLE`，不得自称“双审查 PASS”。

---

## 8. 允许 provisional verdict

只能选最贴近证据的一项：

- `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`
- `KILL_COMPLEX_AXIS_AFTER_VALID_SEMANTICS_AND_CONVENTIONAL_BASELINE`
- `PIVOT_UNVERIFIED_PHYSICAL_RANGE`
- `PROBLEM_SURVIVES_METHOD_CANDIDATES_FAIL`
- `PARTIAL_SEMANTIC_REPAIR_BLOCKED`
- `PARTIAL_BASELINE_INVALID`
- `PARTIAL_ORACLE_INVALID`
- `PARTIAL_BLOCKED_THRESHOLD_NOT_JUSTIFIED`
- `PARTIAL_INDEPENDENT_REVIEW_UNAVAILABLE`

禁止：

- 复用 `PIVOT_MODEL_NOT_JUSTIFIED` 而不说明 D064 修复后新证据；
- 因 P 输就说 problem 不存在；
- M4 未测却关闭 joint/family；
- 进入 Step 5。

---

## 9. 必须产出

新增：

- `projects/thesis-fso/worker-logs/step-004-pilot-jones-semantic-repair-retest.md`
- `projects/simulation/explore/pilot-jones-complex-repair/repair-contract.yaml`
- `projects/simulation/explore/pilot-jones-complex-repair/semantic-failure-reproduction.json`
- `projects/simulation/explore/pilot-jones-complex-repair/semantic_channel.py`
- `projects/simulation/explore/pilot-jones-complex-repair/pilot_and_baselines.py`
- `projects/simulation/explore/pilot-jones-complex-repair/repair_methods.py`
- `projects/simulation/explore/pilot-jones-complex-repair/run_repair.py`
- `projects/simulation/explore/pilot-jones-complex-repair/run_all.py`
- `projects/simulation/explore/pilot-jones-complex-repair/synthesis.md`
- `projects/simulation/results/pilot-jones-complex-repair/result.json`
- `projects/simulation/tests/test_pilot_jones_complex_repair.py`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/S081-pilot-jones-semantic-repair-retest.md`

按实际结果允许更新：

- formal `verifications.md` 新增 V039（独立审查实际完成才写）；
- `projects/thesis-fso/feasibility_report.md`
- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/master-state.md`
- formal `topic-index.md`
- `projects-overview.md`
- `.sessions/_registry.yaml`

禁止新建最终 D065；provisional verdict 由主控接收后再决定。

### worker-log 结构

```markdown
# Worker Log: Pilot-Jones semantic repair + retest

## Input authority and immutable baseline
## T003 failure reproduction
## Signal/noise/pilot contract
## Semantic gates
## Baseline adjudication
## Oracle validation
## Problem-survival probe
## Adaptation scan and method candidates
## Conditional MVE
## Integrity verifier
## Science critic
## Provisional verdict and claim ceiling
## Durable harvest
## Changed files
## Protected/immutable verification
## Commands and exact results
## Anomaly
```

---

## 10. 验收

- [ ] control guard epoch/action PASS。
- [ ] T003 五项失败均有可执行 reproduction，不只文字承认。
- [ ] T003 artifacts byte-unchanged。
- [ ] pilots 在 channel 前插入，pilot/data 走同一 PMD/PDL operator。
- [ ] primary PDL passive，noise placement 明确且测试化。
- [ ] tapped baseline target=known TX pilots。
- [ ] M0–M4 noiseless oracle/limiting cases按 claim scope闭合。
- [ ] 无 receiver-visible arm 系统性优于 oracle；若有则正确停机。
- [ ] B\* 从 validation 合法选择，包含 B1，不按名字指定 B3。
- [ ] problem gate 完全不读取 P 结果。
- [ ] method gate 只在 problem 存活后触发。
- [ ] verified/stress、fixed/PI、raw/aggregate、mask/denominator 明确。
- [ ] M4 未闭合时 claim ceiling 自动收窄。
- [ ] semantic tests + directed tests + YAML/JSON + source SHA +
      `git diff --check` PASS。
- [ ] protected paths与 shared generator/common/params 未改。
- [ ] 独立审查真实可用；不可用则如实降级。
- [ ] 一个 consolidated commit，worktree clean，未 push。

---

## 11. 回传格式

聊天中只返回：

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-004-pilot-jones-semantic-repair-retest.md
anomaly: <one line or NONE>
```

完整事实、数字和解释全部写文件，不在聊天中展开。
