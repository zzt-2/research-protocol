# Task Brief: Q15 终局 Step 3.5 + 条件式 Step 4a 归一化审判

> 来源: S002 / live D030 / formal D039
> 产出位置: `projects/thesis-fso/worker-logs/step-023-q15-terminal-adjudication.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只拿到本 T；可读取本文列出的仓库文件、论文全文和代码

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 53
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP021
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

工作目录：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T022 已完成六篇独立核心精读，但独立验收发现比 D1/C1/C4 缺文更关键的
科学缺口：T020 的 M1 把功率比直接当振幅因子乘复信号，缺少平方根；当前
evaluator 又不恢复幅度尺度。因此 M4 的诊断收益可能只是补了常规 gain
normalization，而不是独立方法。

**你的任务**：

1. 完成真正定向的 Groundwork Step 3.5：纳入公开 D1，修正 D3 碰撞解释，
   补 gain/constellation normalization、regional/sliced MMA 与 dual-mode
   直接证据；
2. 只有 Step 3.5 形成四判据全过 Q# 时，继续同包完成 Step 4a；
3. Step 4a 必须用正确的平方根尺度基线对 M4 做一次终局公平审判；
4. 本包必须给出 Q15 的 `NO-GO` 或 `STEP4A_RECOMMENDATION_READY`，不得留下
   “再修一次”的下一包。

**最高纪律**：

1. 旧 T020 代码、raw、result、synthesis 均只读；在新隔离目录实现审判。
2. M2/M4 只能称 `monotone quantile/radius calibration`，不得称已证明的
   optimal transport。
3. D1 官方全文已知可公开获取，不能继续写成“不可得 mandatory debt”。
4. C1/C3/C4 不再机械全列 mandatory；按与目标 2×2 dual-pol 16QAM
   collapse/gain-normalization 的直接性裁决。
5. Phase A 未形成四判据全过 Q#，禁止运行 Phase B。
6. Phase B 只做 Step 4a，不进 Step 5、Contract、Execute，不写论文胜利。
7. 无论结果如何，本包后禁止第四个 Q15 repair/factory 包；失败即退出 Q15。
8. 全文精读、引用链批筛和 web 结果消化必须委托子 agent；主执行对话不直接
   WebSearch/webReader。
9. 不修改 `.sessions`、master-state、current YAML、旧 campaign artifacts、
   `common/` 或 `params.py`；不 push。

## 1. 必读、恢复与起点门

依次读取：

1. `AGENTS.md`
2. `stages/groundwork.md`
3. `stages/gw-supplement.md`
4. `stages/gw-feasibility.md`
5. `stages/glossary.md`
6. `domain-comms.md` 的 baseline、指标与实验完备性段
7. `thesis-lessons.md` 速查表、TL-20、TL-22、TL-23、TL-30–TL-33
8. `code-quality.md`
9. `.agents/skills/research-direction-lab/SKILL.md`
10. `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
11. `.agents/skills/research-direction-lab/references/baseline-adjudication.md`
12. `.agents/skills/research-direction-lab/references/method-production.md`
13. `projects/thesis-fso/worker-logs/step-020-causal-constellation-prior-shell-family.md`
14. `projects/thesis-fso/worker-logs/step-022-q15-step3-read.md`
15. `projects/thesis-fso/literature_notes.md` 的 Q15 Step 3 段
16. T020 的 contract、`src/methods.py`、`src/run_factory.py`、raw/result
17. `cb1_evaluator.py` 与 B01-R/C11 当前 baseline receipt

启动：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T023-q15-terminal-step35-step4a-adjudication.md
git status --short
```

validator 非 PASS 或起点不 clean，立即停止并返回
`BLOCKED_CONTROL_OR_DIRTY_START`。

先把理论预期写进新 contract：

```text
若 z 的 prefix 功率估计为 Pz、公开 16QAM 目标功率为 Ps，
正确的复振幅乘子 a 满足 |a|² Pz = Ps，
因此 a = sqrt(Ps/Pz)，不是 Ps/Pz。
```

逐 caller/callee 核查并记录：

- `methods.py` M1 实际公式；
- M1/M2/M4 如何送入 evaluator；
- evaluator 是否恢复尺度；
- information access、metric signature、state lifecycle。

## 2. Phase A：Groundwork Step 3.5

### A1. D1 正式纳入

优先使用 EURASIP 官方公开 PDF：

`https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a4p-h07.pdf`

必须走项目 `tools/download`/`tools/convert` 规范保存，不得自搓 PDF 转换。
若 URL 暂时失败，可用 DOI/会议 proceedings/citation chain 寻找同一正式来源；
身份不明则停止为 `BLOCKED_D1_IDENTITY`。

精读并明确：

- ShMMA 的 shell 定义；
- Edge-MSE 观测量；
- MMA→ShMMA soft switch；
- 是否 prefix-frozen、是否 identity passthrough、是否 post-processing；
- 与 Q15 的 action / information boundary / problem 三维碰撞程度。

### A2. 定向矩阵与引用链

从 T022 新认知构造至少 8 个组合，覆盖：

- conventional gain/amplitude/constellation normalization；
- regional/sliced/shell MMA/RDE；
- dual-mode/gated blind equalization；
- post-equalization radial/quantile calibration；

并与以下问题词交叉：

- dual-polarization 16QAM collapse / singularity；
- receiver-visible prefix / blind scale ambiguity；
- safe fallback / identity bypass；
- CMA inner-ring collapse。

要求：

- ≥2 个结构化搜索源；
- 对 D1 或最接近的近期核心竞品做一次双向引用链；
- 最多 3 轮，最后一轮新增必读/建议读=0，或如实记未收敛；
- 新增真正 direct/cheap-alt 论文才获取和精读，禁止为凑数量下载；
- C1/C3/C4 只有被全文/abstract 证实能改变目标判断时才升级为必读。

### A3. 修正综合结论

更新 `literature_notes.md`：

1. D3 的 \(R_n=|z_n-\hat{s}_n|\) 是 decision-error radius，不是星座 shell
   radius；重写其 collision 等级；
2. D1 不再列“全文缺失”；
3. Q15 判据 1 从旧“PASS”回到 `PARTIAL`，直到 standard dual-pol 16QAM 的
   M-C-A 有直接证据；
4. 判据 2 只能由可执行构造 + 相对合法常规链的信息增量支持，不能把
   prefix-only、identity fallback、post-proc 的结构差异自动当信息增量；
5. 判据 3 可为 PASS 仅表示存在 comparator；不表示 comparator 已公平实现；
6. 输出精确 Q# 表、direct collision、cheap-alt、写作包装边界。

### A4. Phase A 硬门

只有同时满足下列条件才进入 Phase B：

- Step 3.5 检索充分性全部达标；若达到三轮上限仍未收敛，必须输出
  `Q15_STEP35_NONCONVERGED_NO_GO` 返回主控/用户，不得自动进入 Phase B；
- D1 已精读且非 exact action+information+problem collision；
- Q15 四判据全部 PASS，证据指针可核；
- conventional normalization 被确定为 Phase B 必测强简单先验；
- `literature_notes.md` 已更新并给出可核 evidence pointer；`master-state.md`
  由主控接收后同步，executor 不修改。

否则终态：

`Q15_STEP35_NO_Q_NO_GO`

停止，不运行任何 seed，不建议第二个 Q15 包。

## 3. Phase B：条件式 Groundwork Step 4a

仅在 A4 全过后执行。创建隔离目录：

`projects/thesis-fso/direction-lab/scout/q15-step4a-normalization-adjudication/`

至少包含：

- `contract.yaml`
- `src/`
- `tests/`
- `artifacts/raw-rows.csv`
- `artifacts/result.json`
- `synthesis.md`

不得修改 T020 目录；可以只读复用 generator/evaluator/CMA。

### B0. Step 4a 内部起飞硬门

在写方法实现或运行任何 seed 前，必须按 `gw-feasibility.md` 的顺序完成并写入
`feasibility_report.md`：

1. A0 §0：确认 Q15 已是 literature_notes 中四判据全过的 Q#；
2. A0 §1–§6：性能间隙、问题结构、跨域先例、非平凡性、负面证据、最强简单
   先验覆盖；
3. A′：竞争维度分解；
4. A：相对增强 traditional comparator 的结构优势；
5. B：新颖性/可行性解耦与三项空白零假设。

任一致命信号输出 `Q15_STEP4A_A0_NO_GO`，不得创建/运行维度 D。

上述分析门通过后，还必须在 seed 前冻结：

- FR-11 架构摘要：输入、action space、决策粒度、信息边界、
  objective/metric、identity fallback；
- FR-20 每个物理参数的来源表；全部继承 T020/B01-R，不为让 Q15 有用改场景；
- FR-21 oracle affine 的适用性与上界预判，只作 Kill，不作 Go 对手；
- FR-18 testbed 简化/升级对所有 comparator 的竞争格局影响；
- FR-12 本 MVE 与未来 formal 架构差异；实质差异直接阻止 recommendation-ready；
- FR-14/FR-15：最强简单先验和贡献目标 comparator 的明确清单。

只有 B0 全过，才允许进入维度 D 的 B1–B4。

### B1. 必备三方及消融

所有方法只读同一 128-symbol calibration prefix，并把参数冻结后应用于相同
suffix：

1. fixed-μ CMA `μ=0.03` identity；
2. **correct pooled sqrt-RMS**：
   `a=sqrt(E|s|² / robust_mean(|z_prefix|²))`；
3. **correct per-polarization sqrt-RMS**；
4. **gated scalar ablation**：复用 M4 的同一 prefix gate，但触发时只应用
   correct sqrt scale；
5. **robust scalar**：median/trimmed estimator，公式和公开 16QAM target
   逐项可核；
6. M2 monotone quantile/radius calibration；
7. M4 prefix-gated identity/M2 policy；
8. C11 legal causal 与 blind-affine 继承 comparator；
9. oracle affine 仅作离线标签/Kill bound。

若 Step 3.5 认定 nearest-shell、regional MMA、RDE 或其他方法是 target-matched
最强 direct/cheap-alt comparator，必须忠实纳入最强一个。若仓库没有且本包内
无法按原文实现，输出 `Q15_BLOCKED_TARGET_COMPARATOR_NO_GO`；不得用拍脑袋
简版冒充，也不得给 recommendation-ready。

### B2. 公平性与 seeds

- contract 必须忠实实现 B0 冻结的 A0/A′/A/B/D 与 FR-11/12/14/15/18/20/21
  条目，不得跑代码后补叙事；
- 共享 realization；同 `(cell,seed)` 只生成一次；
- 7 个 T020 cells 保持不变；
- M4 gate 参数完全继承 T020 dev freeze，不重新看 test；
- 先在 T020 seeds `201–220` 重建原信号并加入新 comparator，作为 post-hoc
  mechanism adjudication；
- 再扫描全仓选择一组全新、互斥的连续 20 seeds；优先 `241–260`，若命中历史
  token 则顺延并记录；
- 新 baseline 不以新 test 调参；仅允许公式确定的 robust estimator；
- seed-cluster 为统计单位，7 cells 不是 7 个独立样本；
- primary metric PI-SER，MDE=`0.005`，10k seed-cluster bootstrap 95% CI；
- 保存逐 `(cell,seed,method)` raw、gate、prefix features、scale/map 参数与
  offline 四分类；smoke receipt 不得被 compare 覆盖。

### B3. 语义 smoke

正式比较前全部通过：

- synthetic `z=c*s` 上 correct sqrt scale 恢复幅度，旧功率比公式必须在
  `c != 1` 时 FAIL；
- identity 配置 bit-identical；
- 固定 prefix、扰动 suffix 不改变 scale/map/gate；
- QPSK identity regression；
- evaluator population、metric denominator、fixed-label/PI 双报；
- 每个 comparator 对两个不同输入产生合理不同输出；
- no-op、clean/healthy 不退化。

任一失败：`Q15_BASELINE_OR_EVALUATOR_IDENTITY_BLOCKED_NO_GO`，不修第二包。

### B4. 终局判据

以“最强合法 conventional normalization comparator”为主要对手，不以裸 CMA
或 oracle 作 Go 对手。

`Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`：

- M4 相对最强 correct normalization 未同时达到
  mean ΔPI-SER `<= -0.005`、95% CI upper `<0`、help>hurt；或
- 原 T020 信号主要被 correct/gated scalar 解释；或
- fresh seeds 方向不稳定；或
- clean/healthy 出现 >MDE 灾难退化。

此时：

- Q15 退出，不给 repair；
- 可收获 evaluator/normalization 方法论教训；
- `mission_method_delta=NONE`。

`Q15_STEP35_NONCONVERGED_NO_GO`、`Q15_STEP4A_A0_NO_GO`、
`Q15_BLOCKED_TARGET_COMPARATOR_NO_GO` 和
`Q15_BASELINE_OR_EVALUATOR_IDENTITY_BLOCKED_NO_GO` 均属于本任务顶层
`NO-GO` disposition：返回主控/用户但不建议下一次 Q15 repair。

`Q15_STEP4A_RECOMMENDATION_READY`：

- D1/Step 3.5 非 exact collision；
- M4 在旧 slice 和 fresh slice 都显著胜最强 correct normalization；
- 相对 C11/blind-affine 不退化；
- clean/healthy 安全；
- 机制消融显示增益来自非线性 monotone radius map，而非单纯 scale/gate。

此时：

- 形成完整 Step 4a A0/A′/A/B/D 报告；
- 写 thesis-facing method card：
  - primary：collapse-triggered causal monotone radius calibration；
  - fallback：低复杂度 gated normalization/safety layer；
- `mission_method_delta=PACKAGING_BOUNDARY`；
- 只返回主控请求用户确认 Go/No-Go，不进 Step 5。

## 4. 交付

必须更新/新增：

- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/feasibility_report.md` 的 Q15 Step 4a 段（仅 Phase B 运行时）
- `projects/thesis-fso/decision_log.md` 的候选建议（不是用户最终 Go）
- Step 3.5 search JSON、D1 canonical paper/read note；
- Phase B 隔离目录（仅 A4 通过时）；
- `projects/thesis-fso/worker-logs/step-023-q15-terminal-adjudication.md`

worker log 必须 facts-first，包含：

1. Step 3.5 coverage/convergence 与 D1 receipt；
2. D3、D1、Q15 四判据修正；
3. Phase A gate；
4. 若运行 Phase B：公式单测、方法表、raw closure、旧/fresh 两套 paired 数字、
   strongest comparator、机制消融、clean safety；
5. formal science disposition 与 `mission_method_delta`；
6. changed files、验证命令、commit receipt 字段；
7. 明确“本包后无 Q15 repair”。

worker log 的 commit 字段固定写：

`EXTERNAL_RECEIPT_REQUIRED`

原因：Git commit SHA 由包含 worker log 在内的树计算，不能在同一 commit 内
自包含自己的最终 SHA。禁止为追逐自引用 SHA 反复 amend。

测试、YAML/JSON、`git diff --check` 全通过后单次 commit，不 push。commit 后读取
真实 HEAD，只在最终五项回执的 `commit:` 返回；主控随后把 SHA 写入接收记录。

最终只回传：

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
