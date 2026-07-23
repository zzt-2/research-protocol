# Task Brief: Pilot-Jones complex-Jones/PMD/PDL 模型充分性救活大包

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 5
  action_class: PILOT_JONES_COMPLEX_MODEL_SALVAGE_PACKAGE
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S001 / formal D063 | 产出位置: `projects/thesis-fso/worker-logs/step-003-pilot-jones-complex-model-salvage.md`
> 日期: 2026-07-23
> 唯一任务文档: 执行方只需要本 T、仓库内列明的权威文件和现有 T002 闭包

## 0. TL;DR（执行方先读）

你在：

`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`

分支：

`codex/research-direction-lab-longitudinal-test`

起始 HEAD 应为本 T 所在提交；T002 执行提交为：

`0b642e9317d4494c481ecf4f1e8ceb07c866c04c`

**你的任务**：在一个 GLM 对话内回答：

> 物理上更充分的 complex Jones / PMD / PDL 信道，是否重新产生一个最强任务适配传统 baseline 无法关闭、且可形成方法的 Pilot-Jones 问题？

这不是单纯“加 PMD/PDL”的代码任务。你必须完成：

`物理证据 → 最小模型梯 → semantic smoke → task-matched baseline → 正确 oracle/headroom → 方法族 → 条件式 MVE → 双审查 → provisional verdict`

只要前置门通过，就在同包直接跑有界 MVE；不得停在文献综述、模型设计、方法列表或“下一轮再实验”。

聊天中最终只返回四行：

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-003-pilot-jones-complex-model-salvage.md
anomaly: <one line or NONE>
```

### 最高纪律

1. T002 只支持 `UNITARY_REAL_ROTATION_MCA_KILLED`；禁止写成 Pilot-Jones family 已 Kill。
2. 不得复用 T002 的错误门：`BER≤2×oracle` **不等于** `<0.5dB`。若使用 Q²/SNR dB，必须写明公式、零误码处理和适用调制。
3. complex phase 本身仍可保持 unitary/cond=1；必须区分：
   - frequency-flat complex unitary；
   - non-unitary PDL；
   - frequency-selective PMD/DGD 或 2×2 memory。
4. 引入 PMD/PDL 后，single-tap block inverse 可能成为任务错配 baseline。Go 对手必须包含 task-matched conventional 2×2 tapped/FDE/pilot-Jones baseline；只赢 single-tap 不算方法信号。
5. 参数必须来自当前项目 truth source、已读全文或明确可核验来源。为了制造 headroom 而拍的极端范围标 `UNVERIFIED_STRESS_ONLY`，不能支撑正面结论。
6. 不改 shared canonical generator、`common/` 或 `params.py`。所有模型与 runner 隔离在 T003 专属目录；不建设通用信道框架。
7. 所有方法共享 realization、pilot pattern、data mask、evaluation window、modulation、channel parameters 和 denominator；validation/test seeds 分离。
8. deployable 方法只用 RX、known pilots、自身历史和合法配置；true channel/taps/Jones/TX data/future symbols 仅供明确标记的 oracle/diagnostic。
9. 4 篇 D056 竞品继续 `BLOCKED_NO_FULLTEXT`，不得冒充已读；正面最高 `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`。
10. 止于 Step 4a provisional verdict；不得进入 Step 5、Contract、Execute，不复活 Scout/P03，不改 protected history/Skill/controller，不 push。

## 1. 已接受事实与必须修正的 T002 遗留

formal owner：

`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D063`

必须继承：

- T002 code/raw integrity 基本可信，directed tests 10/10 PASS；
- canonical generator：
  `sqrt(h) * [[cosθ,sinθ],[-sinθ,cosθ]]`；
- 当前真实矩阵（去掉标量幅度）为 unitary real rotation，cond=1；
- T002 raw：
  - B1 mean `0.005308261178836862`
  - P mean `0.005335549069145674`
  - oracle mean `0.0044654026343545344`
  - P win/tie/loss vs B1 = `0/6/4`
- T002 contract 仍残留 `0/7/3`，不得继承；
- `B1/O=1.19` 只是 BER ratio，不是 0.19 dB，也不是 0.5 dB；
- 当前最小裁决：`UNITARY_REAL_ROTATION_MCA_KILLED / PILOT_JONES_FAMILY_UNRESOLVED`。

T003 不是修 T002 历史 artifact。保留原文件作为执行快照，在 T003 synthesis 和新验证记录中做 amendment。

## 2. 开始前必读与角色分离

按顺序读取：

1. 本 T；
2. `projects/thesis-fso/master-state.md` §2 + 方法层重开轨；
3. formal D055/D056/D061/D062/D063；
4. S079、V036、V037；
5. T002：
   - `source-closure.yaml`
   - `mve-contract.yaml`
   - `synthesis.md`
   - `pilot_jones_methods.py`
   - `run_pilot_jones_mve.py`
   - `result.json`
   - directed tests；
6. `projects/thesis-fso/literature_notes.md` 的 Pilot-Jones L01/L06–L10、PMD/PDL/Jones 相关条目；
7. `stages/glossary.md`、`stages/groundwork.md`、`stages/gw-feasibility.md`；
8. `thesis-lessons.md` 速查表及 TL-20/TL-22/TL-23/TL-26/TL-27/TL-30–33；
9. `code-quality.md`、`reference/sim-template/`；
10. `.agents/skills/sim-preflight/SKILL.md` + `rules/mve-validation.md` + `rules/adaptation-scan.md`。

### 子 agent

若支持，最多并行 3 个：

- evidence agent：只做 PMD/PDL/complex Jones 参数和传统 baseline 的证据提取；
- model/executor agent：模型闭包、smoke、MVE；
- verifier/critic：必须与实现上下文分离。

论文全文精读、web 信息消化、MVE 执行遵守 AGENTS.md 子 agent 规则，单 agent ≤15 分钟。主线程负责集成和裁决。

若独立 agent 不可用，总状态最高 `PARTIAL_INDEPENDENT_REVIEW_UNAVAILABLE`，但仍尽量完成模型、smoke、baseline 和 raw evidence。

## 3. Phase 0：输入完整性与 T002 amendment

### 3.1 基线

记录：

- branch / HEAD / `git status --short`；
- T002 contract/result SHA；
- protected paths SHA；
- observed seeds 全集；
- T002 raw 重算 `0/6/4`。

在新 synthesis 明确：

- T002 stale count；
- BER ratio 与 dB 不可直接互换；
- V037 对 V036 的 claim-scope 修正。

不得回写 T002 contract/result 伪装原执行无缺陷。

### 3.2 保护路径

byte-unchanged：

- `projects/thesis-fso/direction-lab/STATUS.v1.md`
- `projects/thesis-fso/direction-lab/project.v1.yaml`
- `projects/thesis-fso/direction-lab/canonical-state.yaml`
- `projects/thesis-fso/direction-lab/state/completion-events.jsonl`
- B001–B003 / P03 Atlas artifacts
- `.agents/skills/`、controller
- T002 `mve-contract.yaml`、`result.json`

## 4. Phase 1：物理模型充分性证据

建立：

`projects/simulation/explore/pilot-jones-complex-salvage/model-evidence.yaml`

逐项回答并给精确 file:line / DOI / section：

1. 目标星地 coherent OSL 是否需要考虑 PDL、PMD/DGD、X/Y skew、频率相关 Jones 或复数 phase；
2. 哪些是光纤收发机/器件 impairment，哪些来自自由空间传播，哪些属于接收机 DSP；
3. 在当前符号率、带宽、帧长、pilot budget 下，DGD/PDL 的量级是否足以影响 single-tap Jones；
4. 已读 OE2021/LCOMM2026/sat.1553 等各自包含什么、排除什么；
5. 4 篇 BLOCKED 摘要最多支持什么，不支持什么；
6. 最强 conventional baseline 应是 single-tap、2×2 tapped CMA/LMS、frequency-domain pilot Jones，还是别的；
7. 模型升级是否仍在原 dual-pol OSL 场景内，还是偷换成纯光纤问题。

至少形成一个参数表：

`parameter | value/range | unit | source | source scope | VERIFIED/UNVERIFIED_STRESS_ONLY | expected effect`

### 物理门

以下任一成立，停止性能 MVE并给 `PIVOT_MODEL_NOT_JUSTIFIED`：

- PMD/PDL 只来自不在目标链路内的光纤段，且接收机前已有合法补偿；
- 有来源量级在当前时间/带宽窗内低于估计分辨率 ≥3 数量级；
- 只能靠无来源极端参数制造 conditioning/memory；
- task-matched conventional baseline 已由直接文献完整覆盖且无可分离失效。

## 5. Phase 2：最小模型梯与理论 smoke

在当前 worktree 新建：

`projects/simulation/explore/pilot-jones-complex-salvage/`

至少实现四级模型：

- **M0 control**：T002 real unitary rotation；
- **M1 complex-unitary flat Jones**：复数相位/任意 unitary，理论 cond=1；
- **M2 non-unitary PDL Jones**：
  `H = U diag(g1,g2) Vᴴ`，PDL dB 有来源；
- **M3 first-order PMD/DGD Jones**：频率相关 2×2 Jones 或等价短 2×2 FIR memory，DGD 有来源；
- **M4 combined**：只在预算允许且 M2/M3 至少一项通过物理门时运行。

文件职责：

- `complex_jones_channel.py`：模型，不混 receiver；
- `conventional_baselines.py`：single-tap 与 task-matched conventional；
- `salvage_methods.py`：提出方法；
- `run_salvage.py`：paired runner；
- `model-evidence.yaml`
- `salvage-contract.yaml`
- `synthesis.md`
- `projects/simulation/tests/test_pilot_jones_complex_salvage.py`
- `projects/simulation/results/pilot-jones-complex-salvage/result.json`

### 必做理论/语义测试

- M0 与 T002 control 在冻结配置下兼容；
- M1 `HᴴH=I`、cond=1；
- M2 理论 cond 与 PDL dB 映射一致；
- M3 在 DGD=0 时退化为 memoryless；非零 DGD 产生可测 memory/frequency selectivity；
- noiseless true-model oracle 可恢复；
- pilot mask、overhead≤10%、data denominator；
- no future/TX truth；
- paired realization；
- zero impairment / clean control；
- extreme stress 与 verified range 分开；
- raw→aggregate。

先画/列理论预期：

`model → expected cond/memory → which baseline should fail → which baseline should survive`

结果与预期相反时先查实现，不调参救。

## 6. Phase 3：问题存活门与 baseline adjudication

### 6.1 Baseline ladder

每个模型至少：

- B0：single-tap block pilot LS + pinv；
- B1：single-tap fixed EMA09；
- B2：validation-tuned regularization/condition guard；
- **B3 task-matched conventional**：
  - PMD/memory：2×2 tapped CMA/LMS、pilot-aided tapped LS 或 frequency-domain Jones；
  - PDL flat：正确的 regularized/polar-decomposition/whitening baseline；
- P：提出方法；
- O：true model/taps oracle，只作上界/Kill。

B3 必须：

- 与模型任务匹配；
- validation 调参，test 冻结；
- 给予不低于 P 的状态长度/决策粒度；
- 复杂度、pilot overhead 与信息访问明确；
- 能复现 clean/no-impairment。

只赢 B0/B1、却不赢 B3，不算方法信号。

### 6.2 指标与阈值纠偏

在运行 test 前冻结：

- fixed-label BER/SER；
- PI-BER/SER；
- Q² dB（如使用）；
- outage/divergence/recovery；
- pilot overhead；
- complexity/state。

若从 BER 转 Q² dB，必须声明公式，例如：

`Q = sqrt(2) * erfcinv(2*BER)`，`Q²_dB = 20*log10(Q)`

并处理：

- BER=0：使用基于 error count/denominator 的单侧上界或增加样本，禁止记无限 Q；
- BER≥0.5：Q 指标无效；
- QPSK/16QAM 适用性；
- fixed 与 PI 分开转换；
- 不能把 BER ratio 当 dB。

正式 oracle headroom Kill 优先使用项目 FR-21 的 **0.5 dB Q²/SNR-equivalent**，但必须证明转换合法。若项目文档、MDE、同领域论文给出更合适阈值，审计后冻结；不得看 test 后改。

若找不到 defensible threshold：

`PARTIAL_BLOCKED_THRESHOLD_NOT_JUSTIFIED`

不得再用 2× BER 代替。

### 6.3 问题存活

先用 validation/smoke 判断：

1. verified physical range 下，B3→oracle 是否仍有实用 headroom；
2. headroom 是否出现在多个非极端条件，而非单 seed；
3. receiver-visible condition/innovation/energy/memory proxy 是否与 failure 同步；
4. fixed-label 改善是否只是 permutation calibration；
5. complex model 是否同时削弱 B3 和 P，还是人为只伤 baseline。

若 B3 已关闭 oracle headroom，结论为：

`KILL_PILOT_JONES_STABILIZATION_AFTER_TASK_MATCHED_BASELINE`

若只有 stress-only 范围有 gap：

`PIVOT_UNVERIFIED_PHYSICAL_RANGE`

若问题存活，立即进入 Phase 4。

## 7. Phase 4：方法形成与条件式 MVE

至少形成 2–3 个机制不同候选，不把 λ/α 网格当方法：

- P1：condition/energy-aware shrinkage 或 covariance-weighted Jones estimate；
- P2：uncertainty-aware temporal state tracker；
- P3：physics-structured tapped/frequency-domain tracker（若 PMD 门成立）。

每个写：

`legal inputs | state | equation/algorithm | output | causal timing | complexity | mechanism | strongest cheap alternative | falsifier | packaging claim`

必须回答：

- 是否只是 B3 的参数自适应；
- 是否需要 true taps/Jones；
- 是否比 conventional Kalman/RLS/LMS/FDE 多出信息或约束；
- reviewer 最容易说“已有”的地方；
- 如果方法不新，是否仍有可写的模型/边界贡献。

选择 strongest P；contract 冻结后运行：

- tiny deterministic smoke；
- validation；
- 冻结 B3/P；
- fresh test；
- clean + verified PDL + verified PMD + 至少一个 joint/sensitivity；
- 4-pilot 和 6-pilot 至少各一 sensitivity；
- paired realization；
- raw rows + aggregate；
- exact win counts + effect + interval/test；
- module-off/zero-adaptation；
- complexity。

正面最低逻辑门：

- P 超过 B3，不是只超过 B0/B1；
- effect 达到预注册实用阈值；
- paired 方向稳定；
- clean 不材料性退化；
- 消融移除增益；
- receiver-visible state 与机制对应；
- 非 stress-only；
- 独立 critic 未找到 baseline mismatch。

## 8. Phase 5：双审查与 provisional verdict

### Integrity verifier

独立核查：

- model equations 与 limiting cases；
- parameter provenance；
- source/contract/result SHA；
- seeds/mask/denominator；
- information boundary；
- B3 fairness；
- raw→aggregate；
- BER→Q² 公式；
- protected paths；
- exact tests/commands。

### Science critic

独立攻击：

- 是否偷换成光纤问题；
- PDL/PMD 是否物理相关；
- single-tap 稻草人是否污染结论；
- B3 是否充分调参；
- 提出方法是否只是 RLS/Kalman/FDE 别名；
- oracle 是否包含 P 无法获得的信息；
- 正信号是否只在 stress-only；
- 4 篇全文债务是否限制 novelty；
- 结果能否形成明确、务实的论文方法或边界材料。

### 允许 verdict

只能选：

- `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`
- `KILL_PILOT_JONES_AFTER_PHYSICAL_MODEL_AND_TASK_MATCHED_BASELINE`
- `PIVOT_MODEL_NOT_JUSTIFIED`
- `PIVOT_UNVERIFIED_PHYSICAL_RANGE`
- `PARTIAL_INFRASTRUCTURE_BLOCKED`
- `PARTIAL_BLOCKED_THRESHOLD_NOT_JUSTIFIED`
- `PARTIAL_INDEPENDENT_REVIEW_UNAVAILABLE`

不得写普通 GO；不得进入 Step 5。

## 9. Durable harvest

无论结果都必须沉淀：

- 模型充分性表；
- real-unitary / complex-unitary / PDL / PMD 的适用边界；
- task-matched baseline 选择规则；
- 正确 BER/Q² headroom 口径；
- runner/tests；
- 正面方法、Pivot 资产或扩大范围后的负面结论；
- 若无论文材料，写 `NO_DURABLE_HARVEST` 及原因。

## 10. 必须产出与允许更新

必须新增：

- `projects/thesis-fso/worker-logs/step-003-pilot-jones-complex-model-salvage.md`
- `projects/simulation/explore/pilot-jones-complex-salvage/model-evidence.yaml`
- `projects/simulation/explore/pilot-jones-complex-salvage/salvage-contract.yaml`
- `projects/simulation/explore/pilot-jones-complex-salvage/synthesis.md`
- `projects/simulation/explore/pilot-jones-complex-salvage/complex_jones_channel.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/conventional_baselines.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/salvage_methods.py`
- `projects/simulation/explore/pilot-jones-complex-salvage/run_salvage.py`
- `projects/simulation/results/pilot-jones-complex-salvage/result.json`
- `projects/simulation/tests/test_pilot_jones_complex_salvage.py`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/S080-pilot-jones-complex-model-salvage.md`

按结果更新：

- `projects/thesis-fso/feasibility_report.md`
- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/master-state.md`
- formal `topic-index.md`
- formal `verifications.md`（独立审查实际完成才新增 V038）
- `projects-overview.md`
- Direction Lab 可变 current views（只同步 formal routing/result）

禁止：

- 修改 D063、T003、T002 contract/result；
- 新建最终 D064（provisional verdict 等主控验收）；
- 修改 shared canonical generator/common/params；
- 修改 protected history；
- push。

## 11. Worker-log 结构

```markdown
# Worker Log: Pilot-Jones complex-model salvage

## Input baseline and D063 authorization
## T002 amendment
## Physical model evidence
## Parameter provenance
## Model ladder and limiting-case tests
## Metric and threshold adjudication
## Task-matched baseline adjudication
## Oracle/headroom gate
## Method candidates
## Conditional MVE
## Integrity verification
## Science critic
## Provisional verdict
## Durable harvest
## Changed files
## Protected paths
## Commands and results
## Anomaly
```

未执行段必须写原因。

## 12. 验收

- [ ] T002 只按局部 Kill 继承，stale count 与 dB 错误已 amendment。
- [ ] PMD/PDL 参数有来源，verified 与 stress-only 分开。
- [ ] 四级模型 limiting cases 全测试。
- [ ] B3 是 task-matched conventional，不以 single-tap 当唯一对手。
- [ ] BER/Q² 转换有公式、零误码处理和测试。
- [ ] oracle 只作上界/Kill。
- [ ] 问题门通过时同包完成方法比较和 test；未通过时有精确物理/baseline Kill。
- [ ] fresh val/test/observed seeds disjoint。
- [ ] raw 可重算，fixed/PI/overhead/denominator 明确。
- [ ] 双审查分离；不可用时诚实降级。
- [ ] verdict 属允许枚举，不进 Step 5。
- [ ] protected byte-unchanged。
- [ ] tests、YAML/JSON、`git diff --check` PASS。
- [ ] 一个 consolidated commit，worktree clean，未 push。

## 13. 回传格式

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-003-pilot-jones-complex-model-salvage.md
anomaly: <one line or NONE>
```
