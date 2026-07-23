# Task Brief: Pilot-Jones Step 4a 单对话大包

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 4
  action_class: PILOT_JONES_STEP4A_PACKAGE
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S001 / formal D062 | 产出位置: `projects/thesis-fso/worker-logs/step-002-pilot-jones-step4a-big-package.md`
> 日期: 2026-07-23
> 唯一任务文档: 执行方只需要本 T、仓库内列明的权威文件，以及指定只读 source worktree

## 0. TL;DR（执行方先读）

你在：

`D:\code\study\research-protocol\.worktrees\research-direction-lab-longitudinal-test`

分支应为：

`codex/research-direction-lab-longitudinal-test`

**你的任务**：在一个 GLM 对话内完成 Pilot-Jones 的 GW Step 4a 大包，关闭“它是否存在结构性方法增量并值得继续”这一科学不确定性。包内按 `A0 → A′ → A/B → D` 推进；前置门通过时必须同包直接运行有界 MVE，不能停在纯分析或“建议下一轮实验”。

**产出**：完整 Step 4a 证据包、可复现 MVE 闭包（若前置门通过）、provisional verdict、formal/current 状态更新、worker-log 和一个 consolidated commit。聊天中只返回四行：`status`、`commit`、`worker_log`、`anomaly`。

**最高纪律（违反一条即失败）**：

1. D062 是一次性带债豁免，不是把 Step 3.5 或 4 篇全文写成 PASS。4 篇始终保持 `BLOCKED_NO_FULLTEXT`。
2. 正面结果最高只能是 `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`；不得进入 Step 5、Contract 或 Execute。
3. generic `pilot → Jones → inverse compensation` 已被占据；“换成 OSL/GG”“EMA α=.9”“多调几个参数”都不是方法贡献。
4. A0/A′/A/B 任一致命项成立时立即停止性能 MVE并给 Pivot/Kill 建议；否则必须继续到 D，不因写完分析就停。
5. 历史 EMA09 15/15 不是新 MVE 结果；其源码闭包不完整，必须先做 source-closure 审计，再用当前 worktree 的新闭包和 fresh seeds 验证。
6. baseline 必须正确、任务适配且得到公平调参；主对手是传统 block/frame pilot Jones inversion，oracle 只能作上界/Kill 工具，不能作 Go 对手。
7. 所有方法共享 realization、pilot/data mask、评估窗口、调制、SNR、SOP/GG 参数和统计口径；fixed-label 与 PI 指标必须并报。
8. 只使用接收端可部署信息形成方法；true `h/theta/Jones/TX data/future symbols/post-hoc BER` 只能用于明确标记的诊断或 oracle。
9. 不修改/清理指定 source worktree；不恢复 Scout/P03，不建通用基础设施，不改 Skill/controller/protected history，不 push。
10. 一个对话内完成；只在真实致命门、source closure 无法修复、独立执行环境不可用或预算耗尽时提前停。提前停必须给精确 blocker，不得用“工作量较大”作理由。

## 1. 已授权事实（不要重新请求用户许可）

formal owner：

`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D062`

D062 已经授权：

- 选择 H017 选项 (c)，带债进入 Step 4a；
- Step 3.5=`WAIVED_TO_STEP4A_WITH_BLOCKING_DEBT`，不是 PASS；
- 一包完成 A0/A′/A/B/D；
- A0/上界/MVE 负面可支持 Pivot/Kill；
- 正面最高 Conditional Go，且等主控验收和用户确认；
- 不进入 Step 5。

当前 Q2：

- **M**：传统 block/frame pilot Jones inversion——短 pilot LS 估计 2×2 Jones，再 inverse derotation；
- **C**：dual-pol OSL，GG 湍流 + SOP 时变 + ≤10% pilot budget；
- **A**：短 pilot 下 Jones 估计受噪声、病态和动态失配影响，fixed-label recovery 不稳定；
- **关键裁决**：若只是场景迁移或 EMA 参数差异 → Kill；只有 GG/低 pilot 引入需要改变估计或稳定化结构的失效，才允许形成方法。

文献边界：

- 已全文精读：OE 2021 `10.1364/oe.419574`、LCOMM 2026 `10.1109/LCOMM.2026.3651445`；
- 4 篇仅摘要/metadata，禁止冒充全文：
  - `10.1109/TCOMM.2024.3522036`
  - `10.1109/JLT.2025.3640695`
  - `10.1109/JLT.2022.3224805`
  - `10.1109/JLT.2023.3284489`
- V035：JLT 2022 backward refs=21、screened=7、new=0，PASS；
- generic pilot-assisted Jones/SOP tracking、FPT/block pilot 和 feed-forward compensation 已强占点。

## 2. 开始前必读与角色分离

按顺序读取：

1. 本 T；
2. `projects/thesis-fso/master-state.md` §2 + 方法层重开轨表；
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` 的 D055/D056/D061/D062；
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/H017-pilot-jones-step35-partial-4paper-blocked.md`；
5. `projects/thesis-fso/literature_notes.md` 中 Pilot-Jones Q2/L06–L10；
6. `stages/glossary.md`、`stages/groundwork.md`、`stages/gw-feasibility.md`；
7. `thesis-lessons.md` 速查表、TL-20、TL-22、TL-23、TL-26、TL-27、TL-30–TL-33；
8. `code-quality.md` 与 `reference/sim-template/` 相关模板；
9. `.agents/skills/sim-preflight/SKILL.md` 的阶段边界，以及 `rules/mve-validation.md`、`rules/adaptation-scan.md`。MVE 以 `gw-feasibility.md §D` 为 owner；不要误进 Execute。

若支持子 agent：

- 最多同时 3 个；
- MVE 执行必须放到 executor 子 agent，单 agent ≤15 分钟；较长网格拆批；
- 最终 integrity verifier 与 science critic 必须使用不同上下文，不能由实现者自审。

若环境不支持独立子 agent：

- worker-log 写 `INDEPENDENT_AGENT_UNAVAILABLE`；
- 允许完成分析、代码与确定性测试；
- 不得把 provisional verdict 标为 independently verified；总状态最高 `PARTIAL`。

## 3. Phase 0：输入基线与 source closure（必须先做）

### 3.1 Git 与保护边界

记录：

- `git status --short`
- `git branch --show-current`
- `git rev-parse HEAD`
- 指定 source worktree 的 status（只读）

保护路径，必须 byte-unchanged：

- `projects/thesis-fso/direction-lab/STATUS.v1.md`
- `projects/thesis-fso/direction-lab/project.v1.yaml`
- `projects/thesis-fso/direction-lab/canonical-state.yaml`
- `projects/thesis-fso/direction-lab/state/completion-events.jsonl`
- B001–B003 全部 artifacts/projections
- P03 Atlas 全部 artifacts
- `.agents/skills/`、个人 Skill、controller

### 3.2 只读历史资产

只读 source worktree：

`D:\code\study\research-protocol\.worktrees\unified-batch-runner`

不得修改、提交、清理或移动其中任何文件。先核验 SHA256：

| 文件 | 预期 SHA256 |
|---|---|
| `projects/simulation/explore/cma-fade-divergence/pilot_assisted.py` | `f9293b72df0b84b434ced0a75913b09eb0a48ef87c7878485449e97168c24464` |
| `.../pilot_integration_runner.py` | `b147bbd57bd362158656469e75119323256ee8d057fbd55ca8c3da37eb3ea2ef` |
| `.../batch1_fade_methods.py` | `d8e280b480bbf67938d4bd3160ac298af3e2c1f10080ef3ff12b997a6bf8a97a` |
| `projects/simulation/common/_batch_metrics.py` | `7ff4c9d6fbcf7eef075fd4f88f2d42097cf75bca8640b150d69faa583d905cd0` |
| `projects/simulation/tests/test_pilot_assisted.py` | `f1f2b0d2446602594cce59cb2a38b4f5545b4da63ba6d375c9d32ec0535f982e` |
| `projects/simulation/tests/test_pilot_integration_runner.py` | `5f4656266464a214479c47aceeafa9778152ac7cbbfcafc3154d386d21868218` |
| `projects/simulation/results/cma-fade-divergence/pilot_6p_ema09_full24_N100k.json` | `aef153e7fe1d082a108c1730e904e71d18a630cf1d83035bb0f73dedf5b8c1a7` |

必须明确记录这个已知 provenance 断裂：

- 历史 JSON 声称 `batch1_fade_methods.py` SHA256=`09b1fe2de6c5363c4a213147a35cbe403017dabb19747730ddad55ed61ef3d91`；
- 当前唯一找到的文件为 `d8e280…`；
- 因此历史 `15/15` **不可 exact replay**，只作为 diagnostic prior。

### 3.3 建立当前 worktree 的最小闭包

在当前 worktree 新建：

- `projects/simulation/explore/pilot-jones-step4a/`
- `projects/simulation/results/pilot-jones-step4a/`

最小文件职责：

- `source-closure.yaml`：源路径、原 SHA、依赖图、采用/拒绝理由；
- `mve-contract.yaml`：运行前冻结；
- `pilot_jones_methods.py`：baseline 和候选方法，不混 runner；
- `run_pilot_jones_mve.py`：paired realization、运行、保存；
- `synthesis.md`：机制结论和 provisional verdict；
- `result.json`：raw cells + aggregate，必须可由 raw 重算；
- `projects/simulation/tests/test_pilot_jones_step4a.py`：信息边界、mask、同 realization、算法公式、raw→aggregate。

可以参考只读文件，但不得机械复制。必须：

- 追完 transitive imports；
- 选用当前分支可追溯的 canonical dual-pol generator；
- 核对 standard complex Godard-z CMA 更新包含 `e*z*conj(x)`；
- 对每个恢复/改写文件记录来源 SHA 和新 SHA；
- 用测试证明 pilot 只替换 pilot positions、data metric 排除 pilot、pilot overhead≤10%、无 future/TX-truth 泄漏。

若 90 分钟内仍无法建立最小闭包，停止性能 MVE，返回：

`PARTIAL / INFRASTRUCTURE_BLOCKED_SOURCE_CLOSURE`

但仍完成 A0/A′/A/B、方法候选和精确缺件清单。不得扩建通用 runner。

## 4. Phase 1：Step 4a A0（先决定是否值得做方法）

在 `projects/thesis-fso/feasibility_report.md` 新增 Pilot-Jones 专节，逐项完成：

### 4.1 §0 四判据

分别判断并给 `PASS/FAIL/UNKNOWN`：

1. 具体 M-C-A；
2. 可复用方法产出形态；
3. 2019 至今顶刊 baseline；
4. 可量化对标。

第 2 或第 3 条若只能靠“OSL 没人做过”成立，判 FAIL。

### 4.2 A0 六项致命检查

必须回答：

- 性能差距是否真实，还是 historical runner/provenance/metric 产物；
- 是否一定需要新结构，还是 fixed EMA、Tikhonov、condition guard、weighted LS 已覆盖；
- receiver-visible 信息是否足以驱动自适应；
- 既有负面证据是否解释了沉默；
- 为什么此前直接竞品没有做：场景假设差异、技术限制，还是无价值；
- 最强简单方法是否覆盖主指标。

运行任何性能网格前先做 semantic smoke：

- noiseless Jones recovery；
- singular/ill-conditioned pilot matrix；
- deep-fade block；
- clean block；
- causality；
- fixed-label/PI metric signature。

任一致命项成立：停止 D，给 Pivot/Kill。

## 5. Phase 2：A′ / A / B 与方法成形

### 5.1 竞争维度

至少拆成：

- pilot overhead；
- per-block estimation variance；
- matrix conditioning/deep-fade stability；
- temporal tracking lag；
- fixed-label assignment stability；
- compute/state complexity。

指出哪些维度已被 generic pilot/FPT/EMA/regularization 占据，剩余维度必须具体到“输入信息 × 作用点 × 输出动作”。

### 5.2 形成 2–3 个机制不同的方法

必须至少比较：

1. **固定 EMA09**：当前简单参考，不是新方法；
2. **condition-aware regularized LS**：使用 pilot Gram/condition/receiver noise proxy 调节 inverse regularization；
3. **uncertainty-aware temporal tracker**：用 receiver-visible innovation/condition 让当前 block 与历史估计自适应融合。

可增加第 4 个，但禁止把多个 α、多个 λ 当不同方法。

每个候选写：

`legal inputs | state | update equation/algorithm | output | causal timing | complexity | expected mechanism | cheap alternative | falsifier | packaging claim`

必须回答：

- 它是否只是 EMA 换参数？
- 它是否需要 true h/theta/Jones？
- 它能否解释 deep fade 与动态失配之间的权衡？
- 最简单的 reviewer objection 是什么？

选择一个 strongest proposed method 进入 D。若没有一个候选比 fixed EMA/regularized LS 多出结构性信息，判 Kill，不跑性能 MVE。

## 6. Phase 3：冻结 MVE contract 与前置上界

`mve-contract.yaml` 必须在性能运行前写入并计算 SHA256，至少包含：

- `question/hypothesis/falsifier`
- `method_equations`
- `information_access`
- `state_lifecycle`
- `metric_signature`
- `canonical_generator`
- `shared_realization_rule`
- `baseline_ladder`
- `parameter_sources`
- `observed_seed_exclusion`
- `fresh_validation_seeds`
- `fresh_test_seeds`
- `cells`
- `primary_metric`
- `secondary_metrics`
- `pass/fail thresholds`
- `time_budget`
- `stop_conditions`

### 6.1 Baseline ladder

同一 pilot overhead 下至少有：

- B0：block LS + pinv，无 temporal smoothing；
- B1：fixed EMA09；
- B2：最强廉价 simple alternative（Tikhonov/condition guard/weighted LS 中经 validation 选一）；
- P：strongest proposed method；
- A0：naive pilot/module-off ablation；
- O：true Jones oracle，只作 scoring upper bound。

候选 P 必须超过 B2；只超过 B0 不算方法信号。

### 6.2 参数与 seeds

- 先盘点仓库所有已观察 seeds；41–48 和任何历史/调参 seed 不得进入 test；
- validation 与 test 必须 disjoint；
- 参数优先来自当前项目 truth source 和已读全文；
- 未溯源参数明确写 `UNVERIFIED_RANGE`，不可只取有利端；
- 至少覆盖 clean 与 failure/deep-fade 条件，以及不止一个 SOP rate；
- 核心 MVE 可固定 6 pilots/block；至少增加一个 4-pilot sensitivity，不把敏感性当主结果。

### 6.3 判据

执行前必须给出可审计阈值及来源。最低逻辑门：

- P 在 primary metric 上超过 B2，而非只超过 B0；
- paired cell/seed 结果方向一致，报告 exact win counts 和置信/检验；
- clean controls 不出现材料性退化；
- module-off/zero-adaptation 消融移除增益；
- gain 不由不同 denominator、mask、future data 或 oracle information 产生；
- receiver-visible trigger/state 与改善存在机制对应。

若无法从历史门槛、MDE、领域指标或统计功效得到 defensible threshold，停止并报：

`PARTIAL / BLOCKED_THRESHOLD_NOT_JUSTIFIED`

不得事后看结果定阈值。

### 6.4 Oracle/headroom

先估：

- B2 → true-Jones oracle 的可关闭 headroom；
- scoring oracle 使用的信息；
- headroom 在 fixed-label 与 PI 口径是否一致；
- 是否只是 TX-label/permutation calibration gap。

若预注册实用 headroom 不足，直接 Kill，不跑完整 MVE。oracle 结果不得作为 Go。

## 7. Phase 4：条件式 MVE

只有 Phase 1–3 全部通过才运行。

要求：

- MVE executor 与实现者分离；每个子任务≤15分钟，必要时按 cell 分批；
- 先跑 tiny deterministic smoke，再 validation，再冻结 P/B2，最后 test；
- test 不重新调 α、λ、阈值、初始化或 method selection；
- paired realization 每 `(cell, seed)` 只生成一次，所有臂共享；
- 保存 raw rows，不只 aggregate；
- 每个 raw row 带 config SHA、source SHA、contract SHA、realization fingerprint、information class、denominator；
- 输出 fixed-label BER/SER、PI-BER/SER、pilot overhead、divergence、condition/innovation diagnostics；
- 所有结果用项目正式保存方式；不得裸写无 provenance JSON；
- 若结果与理论预期方向相反，先做组件级信息流追踪，不靠调参救。

MVE 架构摘要必须写：

- 输入/信息访问；
- 状态；
- 输出动作；
- 决策粒度；
- 对比范式；
- 目标函数；
- 最强简单先验；
- 已知简化偏差及对 baseline/主方法的相反影响。

## 8. Phase 5：双审查、综合与状态落盘

### 8.1 Integrity verifier

独立核查：

- source/contract/config hash；
- raw→aggregate 重算；
- paired realization；
- seeds disjoint；
- mask/denominator；
- information access；
- protected history；
- tests 和 exact commands。

### 8.2 Science critic

独立攻击：

- 是不是场景换皮；
- 是不是 EMA/regularization 参数调优；
- strongest simple comparator 是否公平；
- oracle 是否偷做 Go；
- fixed-label gain 是否只是 assignment calibration；
- GG/SOP 参数是否人为放大；
- MVE 简化是否削弱 baseline；
- 4 篇全文债务对 claim ceiling 的影响；
- 方法是否有可写进论文的清晰算法形态。

### 8.3 Provisional verdict

只能选一个：

- `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`
- `PIVOT`
- `KILL`
- `PARTIAL_INFRASTRUCTURE_BLOCKED`
- `PARTIAL_INDEPENDENT_REVIEW_UNAVAILABLE`

不得写普通 `GO`。不得进入 Step 5。

### 8.4 Durable harvest

无论结果：

- 正面：方法算法、机制、可量化信号、claim ceiling；
- Pivot：可复用 runner/metric/baseline 与下一问题；
- Kill：失败机制、排除的方法族、可复用负面/边界材料；
- 无材料：明确 `NO_DURABLE_HARVEST` 原因。

## 9. 允许修改/新增的文件

必须产出：

- `projects/thesis-fso/worker-logs/step-002-pilot-jones-step4a-big-package.md`
- `projects/simulation/explore/pilot-jones-step4a/source-closure.yaml`
- `projects/simulation/explore/pilot-jones-step4a/mve-contract.yaml`
- `projects/simulation/explore/pilot-jones-step4a/synthesis.md`
- `projects/simulation/results/pilot-jones-step4a/result.json`（若 MVE 未运行，写明确的 blocked manifest，不伪造 cells）
- `projects/simulation/tests/test_pilot_jones_step4a.py`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/S079-pilot-jones-step4a-big-package.md`

按实际需要新增：

- `projects/simulation/explore/pilot-jones-step4a/pilot_jones_methods.py`
- `projects/simulation/explore/pilot-jones-step4a/run_pilot_jones_mve.py`

按结果更新：

- `projects/thesis-fso/feasibility_report.md`
- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/master-state.md`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
- `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md`（只有独立 verifier 实际执行才新增 V036）
- `projects-overview.md`
- Direction Lab 5 个可变 current views（只更新 formal routing/result，不改变 Scout/P03 disposition）

禁止：

- 修改 D062 或 T002；
- 新建最终 D063（provisional verdict 等主控/用户确认后再决定）；
- 修改 protected paths；
- 修改 source worktree；
- 修改 shared `common/` 或 `params.py`，除非当前闭包完全无法实现且 worker-log 先给出必要性。即使必要，也只允许最小修复并必须有回归测试；禁止顺手重构。

## 10. Worker-log 强制结构

```markdown
# Worker Log: Pilot-Jones Step 4a big package

## Input baseline and authorization
## Source closure and provenance debt
## Step 4a A0
## Step 4a A-prime / A / B
## Method candidates and selected method
## Frozen MVE contract
## Oracle / headroom gate
## MVE execution
## Integrity verification
## Science critic
## Provisional verdict
## Durable harvest
## Changed files
## Protected paths
## Commands and results
## Anomaly
```

每个未执行段写明确原因，不得省略。

## 11. 验收

- [ ] D062 debt waiver 被正确继承，4 篇全文仍为 BLOCKED。
- [ ] 一包确实关闭一个科学不确定性，而不只是改状态/列方法。
- [ ] A0/A′/A/B/D 均有结论；若 D 未运行，有前置致命门或精确 blocker。
- [ ] 至少 2–3 个机制不同方法被比较，不以超参数冒充方法。
- [ ] strongest proposed method 与 fixed EMA09、最强 simple alternative 分开。
- [ ] historical 15/15 provenance mismatch 被记录，未冒充 exact replay。
- [ ] source closure、contract、raw/result、tests、synthesis 可从当前 commit 恢复。
- [ ] fresh validation/test seeds 与全部 observed seeds 不相交。
- [ ] fixed-label 与 PI 口径、pilot overhead、denominator 全部明确。
- [ ] oracle 只作 upper bound，不作 Go。
- [ ] integrity 与 science review 分离；不可用时诚实降级。
- [ ] provisional verdict 属允许枚举，正面不超过 Conditional Go。
- [ ] 不进入 Step 5/Contract/Execute，不复活 Scout/P03。
- [ ] protected paths byte-unchanged。
- [ ] YAML/JSON 可解析；raw→aggregate 可重算；定向 pytest PASS；`git diff --check` PASS。
- [ ] 只有一次 consolidated commit，提交后工作树 clean；未 push。

## 12. 回传格式

聊天中只返回：

```text
status: PASS|PARTIAL|FAIL
commit: <sha-or-NONE>
worker_log: projects/thesis-fso/worker-logs/step-002-pilot-jones-step4a-big-package.md
anomaly: <one line or NONE>
```
