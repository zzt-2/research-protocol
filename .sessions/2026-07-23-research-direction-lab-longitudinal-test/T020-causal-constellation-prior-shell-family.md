# Task Brief: Corrected-baseline 因果星座先验方法工厂 Sprint 002

> 来源: S002 / D027 / V052
> 产出位置:
> `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/`
> 与 `projects/thesis-fso/worker-logs/step-020-causal-constellation-prior-shell-family.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只需本 T、仓库源码和本 T 指定的必读文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 50
  action_class: PREFORMAL_METHOD_FACTORY
  mission_checkpoint: CP018
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T019 虽完成 5 构造比较，但科学 verdict 被 V052 拒收：它用了过时
`μ=0.001` baseline，M3/M5 非严格因果，且 smoke receipt 未闭合。唯一值得保留
的是 M5 的弱迹象（15 help / 5 hurt / 40 tie），不是 method signal。

**任务**：以当前公平 baseline `fixed-μ CMA μ=0.03` 为起点，在一个包内构造并
比较 3–4 个严格 prefix-only、公开 16QAM 星座先验驱动的 causal
shell-distribution 方法，用 fresh dev/test seeds 判断该弱迹象能否成为真正
diagnostic method signal。

**本包不是修 T019 文档，也不是重跑旧 M5。**

最高纪律：

1. 不使用 T019 的 `μ=0.001` anchor 作 Go comparator。
2. mapping、selection、gate、normalization 只能由 calibration prefix 冻结；
   scored eval suffix 不得参与自身变换选择。
3. 至少实现并运行 3 个统计结构不同的方法；正常终态 delta 不得为 `NONE`。
4. fresh test 结果才可产生 signal；dev 只调小量阈值，禁止 test 反调。
5. 按 seed 聚类统计，不能把同一 seed 的 7 个 cell 当 7 个独立样本。
6. 不修改 common/、params.py、旧 T019/B01-R/C11 artifacts 或任何 `.sessions`
   owner；不执行 T018/Q14。
7. 本包失败即退出 CB1 z-only/post-processing 轴，不得建议第三包。
8. 不 push；启动不 clean 立即停止。

终态：

```text
DIAGNOSTIC_METHOD_SIGNAL
WEAK_DIAGNOSTIC_SIGNAL
NO_DIAGNOSTIC_SIGNAL_EXIT_CB1_Z_ONLY
BLOCKED_CURRENT_TESTBED
```

---

## 1. 必读

1. `.agents/skills/research-direction-lab/SKILL.md`
2. `.agents/skills/research-direction-lab/references/method-production.md`
3. `.agents/skills/sim-preflight/SKILL.md`
4. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D027`
5. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md#V052`
6. `projects/thesis-fso/worker-logs/step-019-preformal-method-factory-sprint-001.md`
7. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/fairness-batch-b01r/`
   的 contract、frozen params、`run_fixed_mu_cma`
8. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c11-legality-batch-v1/`
   的 contract、合法 causal comparator 与最终 verdict

启动：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T020-causal-constellation-prior-shell-family.md
git status --short
```

---

## 2. Phase A：冻结 current testbed，不另立修复包

创建 `factory-contract.v2.yaml`，必须明确：

- primary baseline：B01-R current fixed-μ CMA，`μ=0.03`；
- legal comparators：C11 legality 的严格因果版本、真正
  `blind_affine_compare_16qam`；
- B01-R 的 7 个 held-out cells 与四分类标签逻辑；
- dev/test seeds：先全仓 collision scan；优先 dev 10 个、test 20 个 fresh
  disjoint seeds。若 `[181..190]`、`[201..220]` 有碰撞，顺延选择并冻结；
- 同一 `(cell,seed)` 只生成一次 realization；
- calibration prefix、calibration_end 和 scored eval suffix；
- oracle/TX truth 只用于离线四分类与评估，绝不进入方法。

必须做三个身份门：

1. `μ=0.03` runner 与 B01-R current implementation/hash 对齐；
2. baseline/C11/legal blind-affine 的 eval population 完全相同；
3. 改变 eval suffix、保持 prefix 不变时，方法冻结出的参数和 gate 必须
   bit-identical。

任一身份门无法成立才允许 `BLOCKED_CURRENT_TESTBED`；不能转去修基础设施。

---

## 3. Phase B：构造 3–4 个 causal shell-distribution 方法

共同信息源只能是：

- calibration prefix 的 receiver-visible `z`；
-公开 16QAM alphabet、shell radii 和理论 occupancy；
- frozen public receiver parameters。

至少实现以下三类：

1. **Prefix scalar calibration**：由 prefix 估计一个稳健全局 scale，eval
   仅应用该冻结 scale。它是最强 cheap control。
2. **Prefix quantile shell transport**：从 prefix radial CDF 构造单调映射，
   向公开 16QAM 的 0.25/0.50/0.25 shell occupancy 传输；eval 只应用冻结映射。
3. **Constrained three-shell mixture calibration**：prefix-only 拟合受 public
   shell radii/priors 约束的低参数 mixture 或 monotone calibration，再应用 eval。

可选第 4 类：

4. **Prefix-gated identity/transport policy**：仅用 prefix 特征选择 identity、
   方法 2 或方法 3；gate 在 dev seeds 冻结，在 test 不修改。

不得把整段 eval 的均值、CDF、聚类或性能用于自身变换。不得复刻 T019 的
per-symbol nearest-shell remap。

每个方法先写：

- deployable action；
- prefix 输入；
- 冻结参数；
- 与旧 M5/C15/C14/blind-affine 的区别；
- primary/fallback thesis packaging 草案。

实现使用 TDD：先写 causal-leakage、identity-off 和 mapping-monotonicity 的失败
测试，再实现最小代码。

---

## 4. Phase C：dev 冻结与 fresh held-out 比较

### Dev

只允许在 dev seeds：

- 选择极小的 gate/regularization grid；
- 选择方法 2/3 的有限参数；
- 冻结全部配置并写 receipt。

不得改 baseline 参数，不得按 test 结果回调。

### Test

在 7 cells × 20 fresh test seeds 上比较：

- fixed-μ CMA `μ=0.03`；
- legal causal C11；
- receiver-visible blind-affine；
- 3–4 个新方法。

保存逐 `(method,cell,seed)` raw rows、prefix-only parameters/gate receipts、
四分类标签和 divergence。

统计以 seed 为 cluster：

- 每 seed 先跨 cell 聚合 paired delta；
- cluster bootstrap CI；
- help/hurt/tie seeds；
- 每 cell 仅作异质性描述；
- inner-ring / AWGN / healthy / ambiguous 四类分别报告，但不能据 oracle
  标签决定部署动作。

Signal 分级：

- `DIAGNOSTIC_METHOD_SIGNAL`：相对 `μ=0.03` CMA 的 seed-cluster mean
  ΔPI-SER ≤ −0.005，95% CI upper < 0，help seeds > hurt seeds；同时相对
  strongest legal receiver-visible comparator 不显著退化，clean/healthy 无
  catastrophic regression。
- `WEAK_DIAGNOSTIC_SIGNAL`：方向一致且 help seeds > hurt seeds，但 CI 或
  MDE 尚未同时通过；必须明确下一步是 formalize 还是 harvest，不能自动三修。
- 否则 `NO_DIAGNOSTIC_SIGNAL_EXIT_CB1_Z_ONLY`。

所有 smoke、causality tests 和统计都必须写进同一个 terminal result artifact，
禁止 `--smoke` 后被 `--compare` 覆盖。

---

## 5. 产物

```text
projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/
  factory-contract.v2.yaml
  method-map.v2.md
  src/
  tests/
  artifacts/dev-freeze-receipt.v1.json
  artifacts/raw-rows.v2.csv
  artifacts/result.v2.json
  synthesis.v2.md
```

worker log：

`projects/thesis-fso/worker-logs/step-020-causal-constellation-prior-shell-family.md`

正常跑完比较：

```text
mission_method_delta = FAIR_COMPARISON_RUN
```

只有达到强 signal：

```text
mission_method_delta = METHOD_SIGNAL
```

---

## 6. 验收

- [ ] current baseline 确为 `μ=0.03`，没有历史 anchor 回退；
- [ ] ≥3 个新方法实际运行；
- [ ] prefix/eval 因果隔离测试 PASS；
- [ ] dev/test seeds fresh、disjoint、冻结；
- [ ] raw/aggregate 以 seed-cluster 为独立单位；
- [ ] smoke 写入 terminal result；
- [ ] 四分类只用于离线解释；
- [ ] 正常终态 delta 非 NONE；
- [ ] 无第三包暗示、无 formal/论文越界；
- [ ] 只提交授权路径，未 push。

---

## 7. 最终只回传

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
