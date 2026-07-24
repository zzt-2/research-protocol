# Task Brief: Pilot-Jones component 时间语义与复现闭包终审

> 来源: live-test S001 / formal D065 / V039 | 产出位置: thesis-fso formal GW Step 4a
> 日期: 2026-07-24
> 唯一文档: 执行方只需拿到本 T；可读取本 T 指定的仓库文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 7
  action_class: PILOT_JONES_TEMPORAL_SEMANTICS_ADJUDICATION_PACKAGE
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`

分支：

`codex/research-direction-lab-longitudinal-test`

T004 commit `9a250e1589bdd583ad2df2ca788eaa43c71aadfd` 只按工程 PARTIAL
接收。其唯一正面 PDL problem gate 依赖每 64 symbols iid 重抽 component Jones
U/V；固定器件反事实已把 impairment-added headroom 降到约 0.015/0.004 dB。
同时 T004 使用 Python `hash(model_id)`，同 seed 跨 process 不复现；contract 的
N/seed 数与 runner 不一致，`contract_sha256` 只是文件名。

**你的任务**：在一个 GLM 对话内，闭合 component Jones/PSP 的时间语义与
deterministic provenance，按 fixed-primary 重跑 M0/M2/M3 的 paired headroom，
给出该 complex-component rescue axis 的 provisional Go/Kill/Unresolved。

**本包不找新方法。** 重点是判断“问题是否真的存在”，不是把 T004 的 0.77 dB
包装成方法。

### 最高纪律

1. formal step 仍是 **GW Step 4a**；不进 Step 5/Contract/Execute。
2. T003/T004 source、raw、result、synthesis 均 immutable；新建 T005 隔离闭包。
3. primary component PDL/PMD truth **跨整个 frame 固定**。canonical h/theta 继续
   时变。除非已有仓库来源明确给出 component temporal law，否则不得引入慢变；
   iid-per-block 只能复现为 `UNVERIFIED_STRESS_ONLY`，不能支持正面 verdict。
4. 禁止内建 `hash()` 参与 seed。相同参数/seed 在两个独立 Python process 必须
   fingerprint bit-identical。
5. contract、runner、raw 的 N、seed pools、cells、pilot count 必须逐字段相同；
   SHA256 必须是真 hash，不是路径字符串。
6. 不运行 P1/P2/P3/P4，不新增 tracker/KF/RLS/FDE“方法”。只比较合法 conventional
   B* 与 truth-assisted reference。
7. B* 在 validation 冻结；test 不调参。M0/M2/M3 使用同 canonical base realization。
8. 一个 consolidated commit；worktree 初始不 clean 即停止，不得清理用户改动；
   不改 protected/shared generator/common/params/Skill/controller，不 push。

## 1. 必读与保护边界

完整读取：

1. 本 T；
2. `projects/thesis-fso/master-state.md` 顶部、§2、GW Progress；
3. formal `decisions.md` D064/D065；
4. formal `verifications.md` V038/V039；
5. S081 与 T004 worker-log/synthesis/contract/source/raw/result；
6. `stages/groundwork.md`、`stages/gw-feasibility.md` Step 4a；
7. `thesis-lessons.md` 速查与 TL-20/TL-22/TL-23/TL-29–33；
8. `.agents/skills/sim-preflight/SKILL.md` + MVE validation rules；
9. `code-quality.md` 与对应 simulation template。

记录 start HEAD、branch、clean status、T004 15 个文件 SHA、protected SHA。

Protected/immutable：

- T003 `pilot-jones-complex-salvage/`、对应 results/tests；
- T004 `pilot-jones-complex-repair/`、对应 results/tests、S081、worker-log；
- `projects/thesis-fso/direction-lab/STATUS.v1.md`
- `projects/thesis-fso/direction-lab/project.v1.yaml`
- `projects/thesis-fso/direction-lab/canonical-state.yaml`
- `projects/thesis-fso/direction-lab/state/completion-events.jsonl`
- `projects/simulation/common/`、`projects/simulation/params.py`
- `.agents/skills/`

## 2. Phase A：先复现 V039，不跑正式 grid

在新 tests 中先锁四项：

1. 导入 T004，证明 M2 的 `jones_truth[b]` 在相邻 blocks 不同；记录 block duration
   `64 × 0.4 ns = 25.6 ns`。
2. 两个独立 Python subprocess 用同 seed/model/params 运行 T004，fingerprint 不同；
   test 必须证明旧行为失败。
3. T004 contract N=50000 vs runner N=20000、10 test seeds vs 8、假
   `contract_sha256`，全部变成 executable regression。
4. 按 V039 反事实重算固定 1 dB PDL，方向必须与 V039 一致：
   impairment-added headroom 远低于原 iid-block model。允许数值因新 deterministic
   orientation 略变，但若仍 ≥0.5 dB，先停下 root-cause，不得直接正式跑。

输出 `t004-temporal-failure-reproduction.json`。

## 3. Phase B：冻结 T005 contract

新建：

`projects/simulation/explore/pilot-jones-temporal-adjudication/`

至少包含：

- `contract.yaml`
- `temporal_channel.py`
- `baselines_and_oracle.py`
- `run_probe.py`
- `run_all.py`
- `synthesis.md`

### 3.1 primary temporal model

```text
canonical TX
  -> time-varying sqrt(h) R(theta)
  -> one fixed passive component Jones / fixed PSP+DGD for the whole frame
  -> same post-component AWGN
```

- M0：identity；
- M2：单个 fixed `U diag(1,10^(-1/20)) Vᴴ`，复制到全 frame；
- M3：单个 fixed PSP basis，DGD=6 ps；forward/oracle 同一 FFT/guard convention；
- iid-per-block M2 只作旧伪影 reproduction，不进 primary table/verdict。

若仓库现有已读全文明确给出 component 随时间演化，允许新增一个
`SOURCED_SLOW_SENSITIVITY`；必须附 file:line 和时间尺度。没有来源就不加，不能
WebSearch 补故事。

### 3.2 deterministic seed

使用显式稳定映射，例如固定整数 model id + seed；禁止 Python hash。要求：

- 同 process 重跑 bit-identical；
- 两个 subprocess bit-identical；
- Windows/Linux 字节序差异不在本包要求，但 dtype/shape 必须冻结。

### 3.3 冻结 grid

两个已注册条件：

- operational：`alpha=4.2,beta=1.4,gamma_bar=100`；
- adversarial：`alpha=2.0,beta=1.0,gamma_bar=50`。

共同：

- block=64，T_S=0.4 ns，f_g=100，sop_rate=8e-6；
- N 选一个本包可完成值（建议 20000 或 50000），**先写 contract 再跑且代码必须一致**；
- pilots `{4,6}`；
- validation seeds `7400..7409`；
- fresh test seeds `7500..7509`；
- 与 T002–T004 seeds 做 assert disjoint；
- cells：M0、M2 PDL=1 dB、M3 DGD=6 ps。

总 grid 不得偷偷删 cell。若预算不足，应在跑前缩 N 并同步冻结，不得跑后改
contract。

## 4. Phase C：合法 baseline 与 reference

部署型 conventional 候选至少：

- B1：single-tap pilot LS + EMA09；
- B2：single-tap Tikhonov，lambda 只在 validation grid 调；
- 可选 B_static/pooled 只能在明确 task-matched 时加入，不为凑数。

B* 按 `(condition, pilot_count, model)` 在 validation 上冻结，test 只复用。

Truth-assisted reference：

- M0/M2：使用每 symbol 的 true full channel。对 dual-QPSK 至少实现 16 个联合
  symbol pair 的 exact ML/nearest-channel search，避免把 colored-noise inverse
  冒充绝对 ceiling；
- M3：true fixed PSP/DGD 的 exact frequency-domain inverse；说明其 unitary PMD
  噪声保持性质和 h/theta ordering。若无法证明是合法 reference，状态必须
  `PARTIAL_ORACLE_INVALID`，不能 Kill。

所有臂同 pilot overhead、data mask、eval window 和 base realization。fixed-label
BER/Q² 为 primary，PI-BER secondary。

## 5. Phase D：正式 headroom 与裁决

对每个 primary cell 报：

- B* identity、validation config；
- B*/O aggregate BER、Q²；
- 同 seed paired M0 与 impairment 的
  `headroom_impairment - headroom_M0`；
- per-seed raw、bootstrap 95% CI；
- 4 vs 6 pilot sensitivity；
- operational vs adversarial；
- oracle anomaly、mask denominator、zero-error bound。

### 预注册裁决

- 若 M2 与 M3 在两条件、4/6 pilots 的 primary
  `impairment-added headroom` 点估计及 95% CI 上界均 `<0.5 dB`：
  `KILL_COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY`。
- 任一 verified primary 的点估计 `≥0.5 dB` 且 CI/paired direction 支持：
  `PROBLEM_SURVIVES_FIXED_COMPONENT`，但本包**仍不跑方法**，交主控另判。
- CI 跨 0.5 dB 或 reference 不闭合：
  `UNRESOLVED_TEMPORAL_PRIMARY` / `PARTIAL_ORACLE_INVALID`。
- iid-per-block stress 无论多大都不能触发 positive。

不关闭整个 Pilot-Jones family；4 篇全文债继续 BLOCKED；不进 Step 5。

## 6. 审查与产出

若支持分离上下文，使用：

- integrity verifier：determinism、真实 SHA、contract/run/raw、seed/mask/raw→aggregate、
  protected/T003/T004 immutable；
- science critic：component 时间尺度、double-count SOP、M2 ML oracle、M3 ordering、
  B* 公平、0.5 dB CI 和 claim ceiling。

若独立审查不可用，状态最高 PARTIAL，写明原因，不自称“双审查 PASS”。

新增：

- `projects/thesis-fso/worker-logs/step-005-pilot-jones-temporal-semantics-adjudication.md`
- `projects/simulation/explore/pilot-jones-temporal-adjudication/*`
- `projects/simulation/results/pilot-jones-temporal-adjudication/probe_val.json`
- `projects/simulation/results/pilot-jones-temporal-adjudication/probe_test.json`
- `projects/simulation/results/pilot-jones-temporal-adjudication/result.json`
- `projects/simulation/tests/test_pilot_jones_temporal_adjudication.py`

不修改 formal D/V/current owners；provisional verdict 由主控接收后登记。

必须运行并记录：

- fresh pytest（含旧 T004 25 tests + 新 tests）；
- YAML/JSON parse；
- 两 subprocess determinism；
- raw→aggregate 独立重算；
- actual SHA closure；
- protected/T003/T004 diff；
- `git diff --check`。

一个 consolidated commit，未 push，结束时 worktree clean。

## 7. 回传

聊天只返回：

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-005-pilot-jones-temporal-semantics-adjudication.md
anomaly: <one line or NONE>
```

完整细节全部写文件。
