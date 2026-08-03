# Task Brief: 2A Calibration-Aware Robust CPR bounded closure

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 11
  action_class: THESIS_BOUNDED_PACKAGE_EXECUTION
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S015 / D022 | 产出位置: 本任务独立 worktree 的 2A sandbox、results、worker-log 与 harvest dossier
> 日期: 2026-08-03
> 唯一任务: 把 2A 从 `NEEDS_ONE_BOUNDED_PACKAGE` 闭合到明确终态

## 0. TL;DR

你在从 `codex/rdl-method-production-v2` 最新提交创建的隔离 worktree 中。执行且只执行一个 2A 包：

`receiver-visible pilot-SNR estimate → frozen operating-point calibration → unchanged CCISP DA/NDA branch action`

从恢复、preflight、合同冻结、实现、dev、held-out、独立 verifier、harvest 到提交全部在本对话完成。不得以“还差一轮”结束。终态只能是：

- `THESIS_METHOD_READY`
- `SUPPORTING_ONLY`
- `REJECT`
- `EXTERNAL_BLOCKED`（只允许真实外部权限、环境或超出 D022 授权的 core contract 问题）

### 最高纪律

1. 不保证正面结果；保证可信终态和可复现资产。
2. 一个 package，最多一次确定性 repair。语义、方法、指标、信息边界或 test contract 改变时，旧 held-out 作废，必须新 receipt + 全新 test seeds；不得修到通过。
3. 不修改 `projects/simulation/common/`、`params.py`、正式论文、system topic、formal owner 或旧 artifacts。需要这些改动即 `EXTERNAL_BLOCKED(reason=STAGE_SCOPE_EXCEEDED)`。
4. true SNR、真实 GG label、TX payload、true h/phase、branch error 或 post-hoc label 不得进入 deployable action。TX truth 只用于计分。
5. `cand_rank` 与 `ref=9→11 dB` 不是新方法。最强 conventional region retune 必须作为 Go comparator。
6. 不开第二个候选、不扩新方向、不恢复旧 campaign。完成后不 push。

## 1. 恢复与阶段身份

开始前完整读取并遵守：

1. `.sessions/2026-07-20-research-direction-lab-system/topic-index.md`、D021/D022、V015、S015；
2. 本 T004 与 T002；
3. `.agents/skills/research-direction-lab/SKILL.md` 及 `references/method-production.md`、`evidence-and-claims.md`、`baseline-adjudication.md`；
4. `.agents/skills/sim-preflight/SKILL.md`，以及 `scenarios/recover.md`、`scenarios/run.md`、`scenarios/add.md`、`rules/constraints.md`、`tech.md`、`param-source.md`、`mve-validation.md`、`doc-discipline.md`、`usage-log.md`、`interrupt.md`；
5. `projects-overview.md`、`projects/thesis-fso/master-state.md`、`thesis-lessons.md` 速查表与最近三条；
6. `code-quality.md` 与相关 simulation template；
7. P01/P02 worker logs、raw/result artifacts、CCISP method/results 源码与论文源。

本任务是 D022 特批的 `RDL Deep Evidence / thesis bounded closure`，不是新方向 Groundwork，也不改变 formal science disposition。若实际工作要求新物理模型、新核心算法或 formal stage 变化，停止为 `EXTERNAL_BLOCKED(reason=STAGE_SCOPE_EXCEEDED)`，不要自行绕过 FR-22。

先运行 `validate_task_control.py` 并按 sim-preflight 场景 D 完成恢复声明与 usage log；然后才可进入实验。

## 2. Phase 0：事实与语义起飞门

沿 caller→callee 重新核实，不信任历史摘要：

- P01 五个 harm cells、0.32–0.70 dB 损害、adapter 4/5 恢复的 raw→aggregate；
- P02 `cand_rank` 被 dev-tuned region retune 吸收的真实方法定义与数字；
- pilot-SNR estimator 只读 receiver-known pilots，且输出确实进入 calibration/action；
- original CCISP、global retune、region retune 与完整 2A 的参数自由度和 tuning opportunity；
- common-payload metric signature、paired realization、state lifecycle；
- physical parameter truth source、seed history 与现有实现是否能在不改 common/params 的情况下运行。

建立 executable smoke：至少两个不同 receiver-visible pilot observations 必须产生不同校准状态；identity/no-op/constant-map 必须被检测；翻转 true SNR/GG label 而保持接收输入不变时 deployable decision 必须 bit-exact 不变。

任一承重事实不成立：不要补故事。若可在既有 sandbox 内一次确定性修复则修；否则按证据给 `SUPPORTING_ONLY` 或 `REJECT`。

## 3. 冻结方法与 comparator

只允许以下梯子：

- `B0 original_CCISP`：使用 nominal SNR 的继承方法；
- `B1 global_calibration`：dev 上冻结一个全局静态校准参数；
- `B2 region_retune`：最强 conventional cheap alternative，包含 P02 的 dev-tuned region/ref=11 解释；不得用 test truth 逐 cell 选最优；
- `M full_2A`：当前窗 pilot-SNR estimate 驱动与 B2 同容量的冻结 calibration map，再驱动 unchanged CCISP；
- `O true_SNR_oracle`：只报 headroom/Kill，不作 Go 对手。

不得增加 candidate zoo。`M` 必须在 dev 结束前冻结方法名、公式、区间/参数数、输入输出和 computational cost；与 B2 的唯一区别应是 current receiver-visible information，而非更多自由参数。

## 4. 两阶段执行与 immutable receipt

### 4.1 Dev

- 先审计全历史 seed ledger，自动选择与历史完全不相交的连续 dev/test seed ranges；不得照抄已用 seeds。
- primary cells 固定为 P01 五个 harm cells：weak@5/7/9 with δ=-3 dB，weak@11 with δ=+3 dB，moderate@13 with δ=+3 dB。
- coverage guard 默认使用 weak/moderate/strong × SNR {5,7,9,11,13} × δ {-3,0,+3}。若 fresh runtime smoke 证明预算过大，可在看 held-out 前缩为覆盖三种 turbulence、五个 SNR、三种 δ 的分层代表集，但五个 primary cells 不得删；缩约须写 sample-power/rationale。
- dev 只用于 tuning、选择唯一 strongest cheap comparator 和 runtime/sample-size 估算，不产生最终数字。

### 4.2 Freeze Commit 1

在任何 held-out test 前写并提交 immutable receipt：

- contract、method map、primary/safety cells、metric signature、MDE、PASS/FAIL 顺序；
- source hashes、runner hash、parameter provenance、method identities；
- dev/test seed ranges 与 history-disjoint assertion；
- `test_started=false`；
- information-access card、state-lifecycle card、paired-realization contract；
- sample-size rationale 与预估 runtime。

runner 在 test 前必须 fail-close 校验 receipt/source hashes。Commit 1 后不得改方法或判据。

### 4.3 Held-out

按 paired seed-cluster 统计，保存每个 `(cell, seed, method)` 的原始行与聚合。所有方法共享同一 realization、窗口、pilot/payload mask 和评估链。结果通过项目 `save_results()` 或等价项目 owner 写入，禁止无 provenance 的裸 JSON。

## 5. 冻结裁决

Primary metric 沿用 P01 的 common-payload gain dB。先在 dev 冻结 `B*` 为 B1/B2 中唯一 strongest cheap comparator，test 不得按 cell 取 min。

`THESIS_METHOD_READY` 必须全部满足：

1. primary 五 cell 的 seed-cluster mean `M−B* ≥ 0.15 dB`，paired 95% CI lower `>0`；
2. leave-one-cell-out 后方向仍为正，不由单 cell 承重；
3. coverage guard 无 `M−B* ≤ -0.30 dB` 且 CI upper `<0` 的灾难退化；
4. weak@9 sentinel 不得显著劣于 B* 0.15 dB 以上；
5. calibration map 非常数，且 M 与 B* 在非零比例 held-out 窗口产生不同 branch command；
6. shuffled-pilot-estimate 或 global-mean replacement 消融显著削弱收益，证明 current information load-bearing；
7. 信息边界、metric、lifecycle、raw→aggregate、source/receipt、传统 comparator 全部通过独立 verifier。

若 B* 吸收收益、map 退化、在线信息无增量或 primary 未过：`SUPPORTING_ONLY`，保留 mismatch boundary 与 static retune rule。若 truth leak、artifact、虚假 action、不可恢复 chronology/metric 错误：`REJECT`。

## 6. 可用交付物

只在本任务 worktree 写：

- `projects/simulation/explore/2a-calibration-aware-cpr-closure/`
- `projects/simulation/results/2a_calibration_aware_cpr_closure/`
- `projects/thesis-fso/worker-logs/step-043-2a-calibration-aware-cpr-closure.md`
- `projects/thesis-fso/direction-lab/harvest/2a-calibration-aware-cpr-method-package.md`
- `projects/simulation/results/2a_calibration_aware_cpr_closure/sim-preflight-usage-entry.md`（任务专属片段；不得直接修改共享月志，由主控接收后串行并入）

无论正负，method-package 都要包含：方法名、M-C-A、I-A-O、算法伪代码、框图节点、baseline ladder、消融、主图数据路径、claim ceiling、不能说什么、最终 disposition。PASS 时标 `THESIS_ENGINEERING_COMPONENT / THESIS_METHOD_READY`；FAIL 时明确降级，不能写成正面方法。

由 fresh-context 独立 verifier 沿真实调用图复核科学正确性，不只核 checklist/一致性。最后写 Commit 2（结果、verdict、worker-log、dossier、verifier），不 push。

## 7. 自动继续与最终回复

本地 bug、缺字段、序列化、测试失败、runtime 过大等均自动选择安全的 bounded repair/缩约，不向用户询问。只有外部权限、硬件不可用、需要 common/params/formal stage 变化时才允许 `EXTERNAL_BLOCKED`。

最终只汇报：

1. terminal disposition；
2. B* 与 M 的关键数字/CI、online information 是否 load-bearing；
3. 方法包是否可直接用作 Ch4，合法 claim；
4. artifact/worker-log/verifier 路径；
5. Commit 1/2 SHA、未 push、工作树状态。

## 8. 验收

- [ ] control/preflight/chronology/seed/source receipt 全闭合
- [ ] strongest conventional comparator 不缺位
- [ ] current information 增量被消融验证
- [ ] 正负结果都有可用 dossier
- [ ] 独立 verifier 查算法正确性、信息边界与 raw 数字
- [ ] 不以“还差一轮”结束
