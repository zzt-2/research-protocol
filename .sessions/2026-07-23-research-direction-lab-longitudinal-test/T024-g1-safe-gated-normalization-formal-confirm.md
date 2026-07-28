# Task Brief: G1 安全门控归一化 Groundwork 闭合 + 条件式正式确认

> 来源: S002 / live D031 / formal D040
> 产出位置: `projects/thesis-fso/worker-logs/step-024-g1-safe-gated-normalization.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只拿到本 T；可读取本文列出的仓库文件、论文与代码

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 54
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP022
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T023 的 binding Step 4a 已被主控拒收：它在四判据未全过时越过 A4/B0。
但独立重算得到一个真实的诊断级方法信号：

- Q15 nonlinear radius map 不优于同门控 correct-sqrt scalar；
- `gated_scalar` 在 old/fresh 相对 tuned CMA 的 ΔPI-SER 为
  `−0.087444/−0.139286`，两组 CI 均低于 0；
- `gated_scalar` healthy-worst=`0`，而 always-on correct normalization 为
  `0.015625–0.027344`，实际大于 MDE=`0.005`。

**你的任务**：把这个 Q15-derived fallback / salvaged component 登记为
`G1_SAFE_GATED_NORMALIZATION`，做一次终局合法闭合。必须显式重入
candidate-specific Groundwork Step 1→2→3→3.5；只有四判据全部 PASS，
才同包运行一次正式 Step 4a fresh confirm。

**最高纪律**：

1. G1 不是 Q15 nonlinear-map repair；禁止恢复/调参 M4 map。
2. T023 Phase B 只作 hypothesis-generating diagnostic，不得当 formal Go 或
   复用其 old/fresh seeds 作确认。
3. 四判据任一非 PASS，立即 `G1_GROUNDWORK_NO_GO`；不得用实验反向闭合判据。
4. Phase B 必须使用全新未观察 seeds，并保存逐 pair 的 gate、prefix feature、
   scale、offline class 与 metric raw。
5. 目标是低复杂度“安全层/风险约束 trade-off”，不是强行宣称平均 PI-SER
   胜过所有 always-on normalization。
6. 本包必须给出 `G1_FORMAL_RECOMMENDATION_READY` 或顶层 `NO_GO`；不留修复包，
   不进 Step 5/Contract/Execute，不写论文胜利，不 push。
7. 全文精读、web 结果消化、引用链批筛和 MVE 执行按项目规则委托子 agent；
   主执行对话只集成结构化结果。
8. 不修改 `.sessions/**`、master-state/current YAML、T019–T023 artifacts、
   `common/`、`params.py` 或 evaluator。

## 1. 必读与启动门

依次读取：

1. `AGENTS.md`
2. `stages/groundwork.md`
3. `stages/gw-read.md`
4. `stages/gw-supplement.md`
5. `stages/gw-feasibility.md`
6. `stages/glossary.md`
7. `domain-comms.md` 的 baseline/指标/实验完备性段
8. `thesis-lessons.md` 速查表、TL-20、TL-22、TL-23、TL-30–TL-33
9. `code-quality.md`
10. `.agents/skills/research-direction-lab/SKILL.md`
11. RDL references：
    `evidence-and-claims.md`、`baseline-adjudication.md`、
    `method-production.md`
12. T020/T022/T023 worker logs
13. T023 的 contract、methods、runner、raw/result/synthesis
14. `projects/thesis-fso/literature_notes.md` 与 `feasibility_report.md`
    顶部/底部 MASTER ACCEPTANCE AMENDMENT
15. live V058、D031 与 formal D040

启动：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T024-g1-safe-gated-normalization-formal-confirm.md
git status --short
```

validator 非 PASS 或起点不 clean，立即返回
`BLOCKED_CONTROL_OR_DIRTY_START`。

先写 candidate contract，冻结：

```text
positive_method_target:
  receiver-visible prefix detector activates correct sqrt amplitude
  normalization only when collapse risk is present; otherwise identity
minimal_construct:
  T020-frozen gate + per-pol correct sqrt scale
primary_packaging:
  collapse-triggered safe normalization layer
fallback_packaging:
  low-complexity risk/performance trade-off and operating boundary
```

## 2. Phase A：G1-specific Groundwork Step 1→2→3→3.5

### A0. 继承边界与顺序门

Q15 的既有材料只能减少重复劳动，不能自动把 G1 提升到后续 Step。先在
worker log 写出下表并附具体文件指针；没有证据的格一律写 `NOT_INHERITED`：

| Groundwork Step | 可继承 | 不可继承 / 本轮必须新闭合 |
|---|---|---|
| Step 1 检索 | Q15 的系统锚点、通用关键词、既有 search raw | G1 的 gate+identity+correct-scale action、safe-normalization problem、direct/cheap-alt 候选覆盖与收敛 |
| Step 2 获取 | 已有 canonical Q15/D1 本地全文及合法 provenance | 每个 G1 must-read 的 canonical receipt；缺关键全文不得假装闭合 |
| Step 3 精读 | CMA/MMA/radius-map 的一般机制背景 | G1 direct collision、recent baseline、safe-gating/AGC/restart/bypass 的逐篇 read-note/read-log |
| Step 3.5 补充 | 无自动继承 | 双向引用链、C1/C3/C4 债务裁决、四判据与 collision/cheap-alt closure |

严格按以下顺序过门，任一步 FAIL/PARTIAL 都停止为
`G1_GROUNDWORK_NO_GO`，不得借 Phase B 补证：

1. **Step 1**：≥2 个真实结构化来源；§A2 的五类 query 全覆盖；形成
   direct/cheap-alt/must-read inventory；最多 3 轮且最后一轮新增
   must-read/recommended=`0`。
2. **Step 2**：所有 G1 must-read 均有合法 canonical 全文与 provenance
   receipt；关键 direct/cheap-alt 全文缺失即 No-Go，不把 abstract 当全文。
3. **Step 3**：每篇 must-read 均完成 canonical read-note/read-log，并逐篇
   提取 action、information、problem、comparator、适用条件和与 G1 的关系。
4. **Step 3.5**：完成最近 direct competitor 的双向引用链、C1/C3/C4
   债务裁决、四判据和 cheap-alt closure；满足 A4 才可进入 Step 4a。

### A1. 证据债与 lineage

先确认并写清：

- Q15 nonlinear map formal No-Go 与 G1 Q15-derived fallback lineage 的边界；
- T023 diagnostic 只用于提出 G1，不能支持正式结论；
- D1 是 related/partial prior，不写“零碰撞”；补齐 D1 canonical
  read-note + read-log；
- 核查 T023 提到的 C1/C3/C4。只有与 G1 action/information/problem 直接相关
  才升级 must-read；不能无证据宣布 closure，也不能机械全列 mandatory。

### A2. 定向检索与精读

至少 8 个组合，覆盖：

- blind/decision-directed AGC 或 amplitude normalization + CMA/RDE/MMA；
- collapse/divergence detector + equalizer fallback/bypass/restart；
- gated/selective/safe normalization + coherent 16QAM；
- burst-mode/prefix-based gain estimation + dual-polarization receiver；
- receiver-visible confidence/reliability gate + DSP safety layer。

要求：

- ≥2 个真实结构化来源；
- 对最接近的 recent competitor 做一次双向引用链；
- 最多 3 轮，最后一轮新增 must-read/recommended=0；每篇候选有逐条
  include/exclude receipt；
- 新增 direct/cheap-alt 才获取和精读，全文按 `gw-read.md` 写 canonical
  read-note/read-log；
- 搜索 raw、引用链 raw、canonical paper receipt 均进入可提交路径；
- 不把 abstract 当全文，不获取私有全文。

### A3. 四判据的正确语义

输出 G1 的精确 M-C-A 和四判据：

1. **具体矛盾**：always-on gain normalization 在 healthy 输出上可造成
   >MDE 退化，而裸 CMA 缺少 receiver-visible 的安全 activation；
2. **方法产出形态**：prefix detector + identity fallback + correct sqrt scalar
   是可实现算法；此项不由实验输赢定义；
3. **近期 baseline**：必须给出具体 2019+ 论文/方法作为 task-matched comparator，
   不能只写“近期论文使用 CMA”；
4. **可量化对标**：collapse recovery、healthy safety、overall PI-SER、
   activation precision/recall、复杂度可测。

同时输出：

- direct collision：action × information × problem；
- cheap alternative：always-on normalization、threshold-free AGC、restart/
  bypass、target-matched recent method；
- primary/fallback packaging 的文献边界。

### A4. Phase A 硬门

只有以下全部满足才进入 Phase B：

- 检索、引用链、read-note/read-log、raw receipt 全闭合并收敛；
- G1 四判据 `PASS/PASS/PASS/PASS`；
- 无 exact action+information+problem collision；
- strongest target-matched comparator 已确定且可忠实实现；
- `literature_notes.md` 已追加 G1 Groundwork 综合段。

否则输出 `G1_GROUNDWORK_NO_GO`，停止，不运行 seed，不留下一包。

## 3. Phase B：条件式 Step 4a formal confirm

仅在 A4 全过后执行。创建隔离目录：

`projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/`

至少包含：

- `contract.yaml`
- `src/`
- `tests/`
- `artifacts/raw-rows.csv`
- `artifacts/prefix-receipt.csv`
- `artifacts/result.json`
- `synthesis.md`

### B0. 写代码/seed 前的 Step 4a 门

按 `gw-feasibility.md` 顺序写入 `feasibility_report.md`：

1. A0 §0–§6；
2. A′ 竞争维度；
3. A 结构优势；
4. B 新颖性/可行性解耦与三项零假设；
5. 冻结 FR-11/12/14/15/18/20/21。

任一致命项输出 `G1_STEP4A_A0_NO_GO`，不得运行维度 D。

### B1. 方法与公平对照

必须包含：

1. tuned fixed-μ CMA `μ=0.03` identity；
2. always-on correct pooled sqrt-RMS；
3. always-on correct per-pol sqrt-RMS；
4. always-on robust/median scalar；
5. **G1**：T020-frozen receiver-visible gate + per-pol correct sqrt scalar；
6. Q15 M4 map，仅作 lineage ablation，不调参；
7. Step 3.5 认定的 strongest target-matched direct/cheap-alt comparator；
8. oracle 仅作 offline label/Kill，不作 Go 对手。

若 strongest comparator 无法忠实实现，输出
`G1_BLOCKED_TARGET_COMPARATOR_NO_GO`，不得用简化版冒充。

### B2. fresh seeds、信息与 raw

- 7 个 T023 cells 保持不变；参数不为 G1 改场景；
- G1 gate 阈值完全继承 T020 diagnostic freeze，不用 T023 或新 test 调参；
- 用父提交做 exact-token seed scan，选择 20 个全新、连续、互斥 seeds；
  T019–T023、任务文本、测试和任何已观察 token 全排除；
- 每 `(cell,seed)` realization 只生成一次，跨方法共享；
- calibration prefix=`128`，所有 freeze/gate 只读 prefix，suffix 只评分；
- seed-cluster 为统计单位；10k bootstrap 95% CI；MDE=`0.005`；
- `raw-rows.csv` 保存逐 `(cell,seed,method)` metrics；
- `prefix-receipt.csv` 保存逐 `(cell,seed)`：
  `gate_policy,gate_active,mean_abs2,spread,a_x,a_y,
  offline_4category,offline_binary_label,baseline_pi_ser,oracle_pi_ser,
  oracle_gap,baseline_diverged,baseline_metric_finite,oracle_metric_finite,
  label_caller,label_window`；非有限值必须使用可往返重算的显式 null/flag
  编码，不得静默丢 row；
- result 保存 source hashes、seed receipt、formula receipt、method identity 和
  relative-comparator statistics。
- fresh seed 运行前冻结：
  - primary always-on comparator=`robust_scalar`（由 T023 diagnostic 预选，
    formal fresh 不再重选）；
  - strongest target-matched comparator（由 Phase A 文献决定）；
  - G1 正式分层使用 **task-native recoverability label**，精确继承
    `preformal-method-factory-sprint-002/src/run_factory.py::_offline_label`，
    不把 B01-R `μ=0.001` anchor 的 z² 阈值迁移到本轮 `μ=0.03`：
    - caller：`standard_cma_godard_with_z`，`n_tap=11, μ=0.03,
      R2=1.32, block_size=64`；
    - `baseline_pi_ser`：对该 tuned-CMA 输出只在 suffix
      `[calibration_end,eval_end)` 做 `hard_16qam` 和同一 PI-SER evaluator；
    - `oracle_pi_ser`：只用 calibration prefix
      `[eval_start,calibration_end)` 的 TX truth 拟合 frozen oracle affine，
      应用于同一 suffix 并以同一 evaluator 评分；oracle 仅作 offline label，
      不进入任何 deployable gate/action；
    - 若 baseline/oracle metric 缺失或非有限，或
      `baseline_diverged=True`，先强制标 `ambiguous`；
    - `healthy` 当 `baseline_pi_ser<0.1`；
      `awgn_dominated_error` 当 `baseline_pi_ser>=0.1 AND
      oracle_gap<0.005`；
      `recoverable_failure`（下文简称 collapse stratum）当
      `baseline_pi_ser>=0.1 AND oracle_pi_ser<0.1 AND
      oracle_gap>=0.005`；其余 `ambiguous`。
    - B01-R 的 `μ=0.001` 全轨迹标签只作 provenance 对照：其 contract
      “sustained”与可执行函数 `min<0.3 OR mean<0.3` 不一致，且该 `0.3`
      threshold 未验证可迁移到 tuned CMA，因此禁止用它决定 G1 strata。
    上述 caller、窗口、truth 边界或输入任一无法逐 row 重算，输出
    `G1_LABEL_IDENTITY_BLOCKED_NO_GO`；
  - binary classification 仅定义 `recoverable_failure=1`、`healthy=0`；
    `awgn_dominated_error/ambiguous` 只从 precision/recall/balanced-accuracy
    分母排除，但仍进入 overall performance、类别计数和安全报告；
  - healthy/collapse 分层 population 和 cluster unit。

### B3. semantic smoke

正式比较前全部 PASS：

- `z=c*s`：correct sqrt 精确恢复；旧功率比公式在强缩放上失败；
- G1 identity branch bit-identical；
- 固定 prefix、扰动 suffix 不改 gate/scale；
- 两个不同 prefix 触发合理不同 gate；
- QPSK identity regression；
- evaluator population/denominator/fixed-label/PI 口径一致；
- offline label 对正常、baseline-diverged、baseline/oracle nonfinite 三类
  synthetic receipt 均可逐 row 重算，且后两类固定为 `ambiguous`；
- shared realization 与 reset lifecycle；
- raw prefix receipt 可从调用链重算。

任一失败输出 `G1_IDENTITY_OR_RECEIPT_BLOCKED_NO_GO`，不留修复包。

### B4. 预注册终局门

G1 的主张是“健康安全约束下的 collapse recovery”，不是 always-on 平均性能
冠军。先按 healthy degradation `<=MDE` 筛出安全可行集，再在安全集内比较
collapse recovery；不得用事后加权总分或事后挑 comparator。

`G1_FORMAL_RECOMMENDATION_READY` 必须同时满足：

1. **类别支持**：fresh 中至少 5 个 seed-cluster 含 healthy pair、至少 5 个
   seed-cluster 含 `recoverable_failure` pair（即下文 collapse stratum）；不足则
   `G1_BLOCKED_CLASS_SUPPORT_NO_GO`，不外推。
2. **G1 vs tuned CMA（collapse stratum）**：paired seed-cluster mean
   ΔPI-SER `<=-0.005`、95% CI upper `<0`、help>hurt。
3. **healthy safety 硬约束**：G1 每个 healthy pair degradation
   `<=0.005`；同时报告 healthy cluster mean/CI、false activation 数和完整分布。
   任一 pair 超过 MDE 即不进入安全可行集，无另设“catastrophic”模糊门。
4. **安全可行集内最强**：对 CMA、M4、primary robust always-on、其余
   always-on 和 target-matched comparator 逐一先应用相同 healthy safety
   约束。任何通过安全约束的对手若在 collapse stratum 相对 G1 改善
   `>0.005` 且 paired CI lower `>0`，G1 被吸收并 No-Go。
5. **G1 vs M4 lineage ablation**：collapse-stratum
   `G1−M4` mean `<=0`，95% CI upper `<=0.005`；机制证据支持收益来自
   gate+correct-scale，不来自 nonlinear map。
6. **activation 非退化**：gate 在 fresh 中必须同时出现 identity 与 active，
   且至少命中一个 offline collapse pair；在上述固定二分类 population 上，
   point precision `>0.5`、point recall `>0.5`、balanced accuracy 的
   cluster-bootstrap 95% CI lower `>0.5`。三者及完整 CI/denominator 全量
   报告；这是 detector 非退化门，不替代实际 safety/recovery endpoints，
   也不得在 fresh 上选择分类阈值。
7. **recent comparator**：target-matched comparator 若满足 healthy safety 且
   在 collapse stratum 显著优于 G1（规则同第 4 条），则
   `G1_ABSORBED_BY_TARGET_COMPARATOR_NO_GO`。

所有分层效应的独立单位固定为 seed-cluster：先在每个 seed 内，对该 stratum
出现的 cells 等权求 paired ΔPI-SER 均值；一个 seed 即使含多个同类 cell 也只
贡献一个 cluster value；随后只对这些 seed-level values 做 10k bootstrap。
禁止把 `(cell,seed)` pair 当独立样本。

任一不满足，输出 `G1_FORMAL_CONFIRM_NO_GO`。不得通过重调 gate、改 cells、
选择 seed 子集或降低阈值救活。

统计计划必须预注册并双报：

- overall、healthy、collapse 三层 paired seed-cluster effect + 10k CI；
- healthy false activation 与 degradation distribution；
- collapse activation precision/recall/balanced accuracy 的 cluster-bootstrap CI；
- 类别为空/支持不足按第 1 条 No-Go；
- 所有 always-on 方法双报，不因 fresh 表现改变 primary comparator。

recommendation-ready 时写 method card：

- technical action / legal inputs；
- comparator 与 fresh evidence；
- primary/fallback packaging；
- operating boundary；
- complexity/latency；
- claim ceiling=`CANDIDATE/LOCAL_SLICE`；
- 下一步只请求主控/用户确认，不进 Step 5。

## 4. 交付与回执

必须更新/新增：

- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/feasibility_report.md`（仅 Phase B 进入时）
- `projects/thesis-fso/decision_log.md` 的 executor proposal
- G1 search/citation/read receipts；
- G1 隔离目录（仅 A4/B0 允许时）；
- `projects/thesis-fso/worker-logs/step-024-g1-safe-gated-normalization.md`

worker log 必须包含：

- Phase A 四判据、collision、coverage/convergence；
- Phase A/B0 gate；
- 若运行 Phase B：公式、raw/prefix closure、relative paired statistics、
  safety、mechanism、strongest comparator；
- `formal_science_disposition` 与 `mission_method_delta` 分开；
- changed files、验证命令、真实限制；
- 明确“本包后无 G1 repair”。

worker log 的 commit 字段固定写 `EXTERNAL_RECEIPT_REQUIRED`。全部验证后单次
commit，不 push；最终只返回：

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
