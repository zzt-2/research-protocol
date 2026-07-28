# Step 024 — G1 safe-gated normalization Groundwork 闭合 + 条件式 formal confirm

> Task: T024 (CANDIDATE_FORMALIZATION, CP022, control epoch 54)
> Date: 2026-07-28
> Status: `G1_FORMAL_CONFIRM_NO_GO` | mission_method_delta: `NONE`
> claim ceiling: G1 未过预注册 activation-CI 正式门（seed-cluster bacc CI_lo=0.50
> NOT >0.5）；核心安全/恢复机制独立确认成立（诊断级正向证据，非 formal method）。
> **本包后无第二个 G1 repair。不进 Step 5/Contract/Execute。不 push。**
> Artifacts: `projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/`

## 0. Task boundary（纪律自检）

- 仅做 G1 的 candidate-specific Groundwork Step 1→2→3→3.5 + 条件式 Step 4a formal
  confirm。G1 = Q15-derived fallback（prefix-gated identity + per-pol correct sqrt
  scalar），**不是** Q15 nonlinear-map repair；**未恢复/调参 M4 map**。
- T023 Phase B 只作 hypothesis-generating diagnostic，**未复用** 其 old/fresh seeds
  作确认（本包用全新 token-clean seeds 261-280）。
- 四判据全过才同包运行 formal Step 4a（A4 PROCEED）。
- 全文精读（D1）、引用链批筛、web 结果消化、MVE 执行**全部委托子 agent**；主对话
  未直接 WebSearch/webReader。
- **未修改** `.sessions/**`（owner/mission/log/decisions/master-state/current YAML）、
  T019–T023 artifacts、`common/`、`params.py`、`cb1_evaluator.py`、`cb1_cell_runner.py`。
- **未进入** Step 5 / Contract / Execute / 论文声称；**未 push**。

## 1. Preflight

- `python .agents/skills/research-direction-lab/scripts/validate_task_control.py
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T024-g1-safe-gated-normalization-formal-confirm.md`
  → **PASS**
- `git status --short`（worktree 起点）→ clean。

## 2. Candidate contract 冻结（先于 seed）

`g1-safe-gated-normalization-confirm/contract.yaml` 冻结：

```text
positive_method_target: receiver-visible prefix detector activates correct sqrt
  amplitude normalization only when collapse risk is present; otherwise identity
minimal_construct: T020-frozen gate + per-pol correct sqrt scale
primary_packaging: collapse-triggered safe normalization layer
fallback_packaging: low-complexity risk/performance trade-off and operating boundary
```

理论预期（先于 seed）：correct sqrt `a=sqrt(Ps/Pz_hat)` 精确恢复 amplitude（z=c·s，
audit SER=0 all c）；identity branch healthy bit-identical；always-on correct scalar
healthy 退化 0.015625–0.027344 >MDE（V058 修正，executor 原"<MDE"是数量级错误）——
这是 G1 要保护的 headroom。T023 越门 diagnostic 数字只作 motivation，不作 formal win。

## 3. Phase A — G1-specific Groundwork Step 1→2→3→3.5

### A0. 继承边界表

| Step | 可继承 | 不可继承 / 本轮新闭合 |
|---|---|---|
| 1 检索 | Q15 的系统锚点、通用关键词、既有 search raw（26 非空文件 ~180 hits） | G1 的 gate+identity+correct-scale action、safe-normalization problem、direct/cheap-alt 候选覆盖与收敛 |
| 2 获取 | 已有 canonical Q15/D1 本地全文及合法 provenance（D1 EURASIP 已在 T023 获取） | 每个 G1 must-read 的 canonical receipt；Li 2024 TCCN 不可得入 gap |
| 3 精读 | CMA/MMA/radius-map 的一般机制背景（8 篇已读：D1/D2/D3/D3'/D4/D4'/D5/C2/C6） | G1 direct collision、recent baseline、safe-gating/AGC/restart/bypass 的逐篇 read-note/read-log（D1 global read-note 本包补齐） |
| 3.5 补充 | 无自动继承 | 双向引用链、C1/C3/C4 债务裁决、四判据与 collision/cheap-alt closure（本包全闭合） |

### A1. 证据债与 lineage

- Q15 nonlinear map formal No-Go 与 G1 Q15-derived fallback lineage 边界已写清（contract.yaml
  lineage 段 + lit notes MASTER ACCEPTANCE AMENDMENT）。
- T023 diagnostic 只用于提出 G1，不当正式结论。
- **D1 canonical read-note + read-log 本包补齐**（V058 debt 闭合）：子 agent 全文精读
  `papers/manual/eurasip-2007-d1-shell-partitioned-mma/content.md`（271 行），写
  `papers/_read_notes/eurasip-2007-d1-shell-partitioned-mma.md`（155 行，14 字段 + 7
  结构化子表 + 4-axis G1 collision 表），read-log 追加 1 行。D1 collision with G1 = **NONE**
  （tap-update cost 非 post-proc / always-online 非 prefix-frozen / SISO 256/1024 非
  DP-16QAM / 无 identity branch；eq.5→6→24 + Edge-MSE λ_E=0.98 指针可核）。
- C1/C3/C4（T022 留下的 cheap-alt 债）：abstract 级裁决（不获取私有全文，不把 abstract
  当全文——仅作 cheap-alt 排除证据）：C1 null-space init（init 层）/ C3 MMA steady-state
  （理论）/ C4 analytical MMA（tap-update cost 变体）全 **DOES_NOT_ABSORB**。

### A2. 定向检索与精读

A2 五类全覆盖（见 `search-archive/2026-07-28/g1-step1-coverage-summary.md`）：
1. blind/decision-directed AGC + CMA/RDE/MMA（继承 radius-MMA/RDE raw，~70 hits）
2. collapse/divergence detector + restart/bypass（继承 CMA-singularity/restart raw）
3. gated/selective/safe normalization + coherent 16QAM（继承 dual-mode-gated 2 hits）
4. burst-mode/prefix-based gain estimation（本包新增 2 query，**全 0 命中**）
5. receiver-visible confidence/reliability gate + DSP safety layer（本包新增 1 query，
   12 hits **全 off-topic**：地震监测/无人机交通异常/车辆网安）

G1-specific 最接近动作轴（prefix-frozen gate + correct sqrt scalar + identity safety +
receiver-only post-proc）：6 条 query 全 **0 命中** → 强收敛信号（与 T023 Step 3.5 一致）。

源覆盖：S2 + OpenAlex（2 结构化源）+ IEEE/blit 继承第三源。最多 3 轮（继承 Q15 2 轮 +
G1 新增 1 轮），最后一轮新增 must-read/recommended = **0**。

子 agent `g1-candidate-screen` 对全部 search-archive/2026-07-28/*.json 去重+on-topic
过滤 → 30 on-topic unique candidates，**0 HIGH collision**（candidate-map 见同目录
`g1-step1-candidate-map.md`）。最强 recent（2019+）task-matched competitor = **D4 Di Rosa
JLT 2021**（已精读）；最强 un-read recent = Li 2024 TCCN（#10）。

### A3. 四判据 + collision/cheap-alt/packaging（写入 literature_notes.md "G1 Groundwork 综合段"）

G1 M-C-A：M = tuned CMA μ=0.03（塌缩无 safety）+ always-on correct sqrt（healthy
退化 >MDE）；C = DP-coherent 16QAM prefix-frozen post-proc；A = always-on 隐含"healthy
零代价"假象 + 裸 CMA 隐含"不需安全激活"假象。

四判据：1 PASS（M-C-A 句子级）/ 2 PASS（collapse-triggered safe normalization layer
是可复用算法，**贡献是 gate+identity safety layer 结构增量，不是 correct normalization
本身**——后者已被 always-on 吸收）/ 3 PASS（tuned CMA + always-on correct + D4 Di Rosa
JLT 2021 task-matched）/ 4 PASS（collapse recovery/healthy safety/activation/复杂度可测）。

direct collision：0 HIGH（candidate-screen 30 + 6 G1-specific 0-hit query + D4 双向引用链
forward 9 / backward 26 无新增）。cheap-alt：always-on correct scalar **部分**（恢复塌缩
但 healthy >MDE，正是 G1 headroom）；C1/C3/C4/D4/VAE 全 DOES_NOT_ABSORB → closure RESOLVED。

primary packaging：collapse-triggered safe normalization layer（CANDIDATE/LOCAL_SLICE）。
fallback：healthy-safety vs collapse-recovery trade-off + operating boundary。

### A4. Phase A 硬门 → PROCEED

四判据 PASS/PASS/PASS/PASS；0 exact collision；strongest target-matched comparator
（D4）已确定且可忠实实现；检索/引用链/read-note/raw receipt 全闭合并收敛；
literature_notes.md 已追加 G1 Groundwork 综合段。→ **进入 Phase B**。

## 4. Phase B — 条件式 Step 4a formal confirm

隔离目录 `g1-safe-gated-normalization-confirm/`（contract.yaml / src/{methods.py,
run_g1_confirm.py} / tests/test_g1_semantic_smoke.py / artifacts/{raw-rows.csv,
prefix-receipt.csv, result.json, synthesis.md, seed-freeze-receipt.md}）。

### B0. 起飞硬门（先于 seed）

`feasibility_report.md` "G1 Step 4a" 段写：A0 §0（G1-Q1 + 四判据全过）、§1 性能间隙
[FR-02]（healthy 退化 0.015625 ≈ 3.1×MDE，>5% 相对 gap）、§2-§6、A′ 竞争维度（healthy
safety 低覆盖 + ≥3×MDE headroom）、A 结构优势（identity branch bit-identical）、B 新颖性
+ 4 个空白零假设全反驳。seed 前冻结 FR-11/12/14/15/18/20/21（全继承 T020/B01-R，不为
G1 改场景/参数）。**A0/A'/A/B 无致命信号**。

### B1. 方法与公平对照（8 方法，全 prefix-only frozen）

1. baseline_cma_mu0p03（M，tuned fixed-μ CMA identity）
2. correct_pooled_sqrt_rms（always-on）
3. correct_per_pol_sqrt_rms（always-on）
4. robust_scalar（always-on median；**pre-frozen primary always-on comparator**）
5. **G1 = gated_scalar**（T020 gate {0.6,0.1} + per-pol correct sqrt scale；候选）
6. M4_gated_policy（Q15 nonlinear map，lineage ablation ONLY，read-only import，不调参）
7. **D4_likelihood_gated_rde**（Di Rosa JLT 2021，faithful 实现：gate CMA tap-update by
   Rician-amplitude likelihood α，preserve known-TX-PDF assumption；output z 仍 post-CMA
   layer 评分）
8. oracle_affine_bound（TX-truth prefix-fit，Kill-only，FR-21/FR-25）

D4 可忠实实现（read-note 足够）；无 `G1_BLOCKED_TARGET_COMPARATOR_NO_GO`。

### B2. fresh seeds、信息与 raw

- **FRESH = 261-280**（token-clean：strict seed-context scan 0 hits vs T019-T023；
  receipt `artifacts/seed-freeze-receipt.md`；261 作为 eval-window symbol index 是不同
  namespace，作 seed 干净；disjoint asserts 写入 runner）。
- 7 T020 cells 不变；G1 gate 阈值完全继承 T020 dev freeze，不重看 test。
- 每 (cell,seed) realization 生成一次，跨方法共享（同 T023 `_realization`）。
- calibration prefix=128；freeze 只读 prefix，apply 只读 suffix，无反馈。
- task-native recoverability label 精确继承 run_factory.py::_offline_label（healthy
  b<0.1 / awgn b≥0.1&(b−o)<0.005 / recoverable_failure b≥0.1&o<0.1&(b−o)≥0.005 /
  ambiguous）；**不迁移 B01-R μ=0.001 z² 阈值**。label 逐 row 可重算。
- binary classification：recoverable_failure=1 / healthy=0；awgn/ambiguous 从
  precision/recall 分母排除但计入类别计数。
- `raw-rows.csv` 1120 rows（8×7×20），逐 (cell,seed,method) metrics + gate + scale +
  offline label；`prefix-receipt.csv` 140 rows（7×20）逐 (cell,seed) prefix receipt；
  非有限值用显式 null/flag 编码，无静默丢 row；deterministic（重跑 byte-identical）。

### B3. semantic smoke（先于 compare，TDD）

`tests/test_g1_semantic_smoke.py` 9 测试，`pytest` → **9 passed**：
correct sqrt 恢复 amplitude（SER=0 all c，旧功率比过校正）/ G1 identity bit-identical /
prefix-freeze invariance / 两 prefix 触发不同 gate / QPSK identity regression /
evaluator 口径一致 / offline label 3 类 synthetic receipt 可重算（diverged & nonfinite
→ ambiguous）/ shared realization + reset lifecycle / raw prefix receipt 可重算。
无 `G1_IDENTITY_OR_RECEIPT_BLOCKED_NO_GO`。

### B4. 预注册终局门 + **master 独立重算**

统计单位 = seed-cluster（每 seed 内对同 stratum cells 等权求 paired ΔPI-SER 均值，一
seed 一 cluster value，10k bootstrap 95% CI）。**主控用确定性 Python 从 raw-rows.csv
独立重算全部 B4 统计（TL-21/P6），非采信 executor 自报**：

| 门 | executor 自报 | master 重算 | final |
|---|---|---|---|
| 1 class support | PASS | PASS（11 healthy / 13 collapse seeds） | PASS |
| 2 G1 vs CMA collapse | PASS | PASS（−0.5598, CI_upper −0.4031<0, 12>0 hurt） | PASS |
| 3 healthy safety | PASS | PASS（G1 worst=0.0；always-on 0.0156–0.0195 全 FAIL>MDE 独立确认） | PASS |
| 4 strongest safe-feasible | PASS | PASS（safe={CMA,M4,G1,D4}；均不优于 G1；always-on+oracle 因 safety FAIL 排除） | PASS |
| 5 G1 vs M4 ablation | PASS | PASS（G1−M4 −0.0355, CI_upper −0.0242≤0.005） | PASS |
| **6 activation non-degeneracy** | **PASS（pair-bootstrap bacc CI_lo 0.8905）** | **FAIL — seed-cluster bacc CI_lo=0.50 NOT >0.5** | **FAIL** |
| 7 D4 target comparator | PASS | PASS（D4 healthy-safe 但 collapse 不优于 G1） | PASS |

**GATE6 unit 错误详记**：executor 用 pair-bootstrap pooled bacc（CI_lo=0.8905），违反
task §B4 的 seed-cluster unit（formula_receipt 声明 `stat_unit=seed_cluster` 但 GATE6
计算用了 pair-bootstrap，内部不一致）。master 独立重算 seed-cluster bacc：per-seed
bacc 中 16/19 单类 seed 饱和到 0.5（healthy 与 collapse 罕在同 seed 共现，仅 3 seed
含两类），CI_lo = **0.50**（NOT strictly >0.5）。point precision/recall=0.95/0.95、
bacc_point=0.958 强，但不满足预注册 CI 门。

**Step 4a 决策：`G1_FORMAL_CONFIRM_NO_GO`**（6/7 PASS，GATE6 FAIL）。按 §B4 "任一不满足
即 NO_GO，不得通过重调 gate、改 cells、选 seed 子集或降阈值救活"。**未救活**：未放宽
到 pair-bootstrap，未改 unit，未挑 seed，未降阈值。result.json/synthesis.md 已由 master
修正（保留 executor 原值作审计 trail）。

## 5. formal_science_disposition 与 mission_method_delta

- **formal_science_disposition**: `G1_FORMAL_CONFIRM_NO_GO`（预注册 activation-CI 门
  在正确 seed-cluster unit 下未达；6/7 PASS）。
- **mission_method_delta**: `NONE`（机制证据方向稳定且独立确认，但未过 formal 门，
  非方法进展、非 PACKAGING_BOUNDARY）。
- 两者分开记录（method-production 规范）。

## 6. changed files、验证命令、commit receipt

### changed files（本包产出）

**gitignored（保留 worktree，不提交）**：
```text
papers/manual/eurasip-2007-d1-shell-partitioned-mma/{source.pdf,content.md,metadata.json}  (T023 已建，本包 read-note 引用)
papers/_read_notes/eurasip-2007-d1-shell-partitioned-mma.md   (D1 read-note, V058 debt)
projects/thesis-fso/search-archive/2026-07-28/g1-*.json        (G1-specific search raw + citation chain raw)
projects/thesis-fso/search-archive/2026-07-28/g1-step1-coverage-summary.md
projects/thesis-fso/search-archive/2026-07-28/g1-li2024-acquisition-receipt.md
projects/thesis-fso/search-archive/2026-07-28/g1-step1-candidate-map.md  (subagent 产出)
```

**tracked（提交，与 T023 同 convention：scout 工作目录入库）**：
```text
projects/thesis-fso/literature_notes.md           (新增 "G1 Groundwork 综合段")
projects/thesis-fso/feasibility_report.md         (新增 "G1 Step 4a" A0/A'/A/B/D + NO_GO 决策)
projects/thesis-fso/decision_log.md               (新增 G1 executor proposal)
projects/thesis-fso/read-log.md                   (追加 D1 一行)
projects/thesis-fso/worker-logs/step-024-g1-safe-gated-normalization.md  (本文件)
projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm/  (隔离目录全量：
  contract.yaml, src/{methods.py,run_g1_confirm.py}, tests/test_g1_semantic_smoke.py,
  artifacts/{raw-rows.csv,prefix-receipt.csv,result.json,synthesis.md,seed-freeze-receipt.md})
  — 不含 __pycache__/.pytest_cache（gitignore）
```

### 验证命令（全过）

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T024-g1-safe-gated-normalization-formal-confirm.md
# → PASS

# smoke（T023 同环境：~/scoop python311 numpy2.4+pytest9.1+scipy；torch venv 无 pytest）
cd projects/thesis-fso/direction-lab/scout/g1-safe-gated-normalization-confirm
python -m pytest tests/test_g1_semantic_smoke.py -v   # → 9 passed

python -m json.tool artifacts/result.json > $null     # → VALID JSON

# master 独立 B4 重算（确定性，从 raw-rows.csv）
# → gates 1/2/3/4/5/7 PASS, gate6 FAIL (seed-cluster bacc CI_lo=0.50)

git diff --check   # → (no whitespace errors)
```

### commit receipt

`EXTERNAL_RECEIPT_REQUIRED`

（Git commit SHA 由包含 worker log 在内的树计算，不能在同一 commit 内自包含自己的最终
SHA。禁止为追逐自引用 SHA 反复 amend。主控随后把真实 HEAD SHA 写入接收记录。）

## 7. 终态

- **status**: `G1_FORMAL_CONFIRM_NO_GO`
- **mission_method_delta**: `NONE`
- **未进入**: Step 5 / Contract / Execute / 论文声称
- **未给**: Step 4a recommendation / thesis-facing method card（NO_GO）
- **未改**: `.sessions/**`、master-state、current YAML、T019–T023 artifacts、common/、
  params.py、cb1_evaluator.py、cb1_cell_runner.py
- **允许修改的文件全部落在授权路径**（§6 清单），未 push。
- **本包后无第二个 G1 repair**——G1 退出（待主控接收 binding 终态）。
- 机制证据（healthy zero-regression + collapse recovery + M4 ablation）独立确认成立，
  作 fallback packaging 诊断级正向证据，由主控/用户决定是否进 thesis harvest。

## 8. 真实限制与已知债务

- **GATE6 是 data/population 属性而非 bug**：healthy 与 collapse 在 20 fresh seeds 中
  罕在同 seed 共现（仅 3/19 seed 含两类），seed-cluster per-seed bacc 饱和到 0.5。
  更多 seeds 或更宽 cell 矩阵可能让两类共现上升——但**禁止在本包 post-hoc 扩 seed/cell
  救活**（§B4）。
- **executor GATE6 unit 错误**：pair-bootstrap vs seed-cluster。master 已修正；建议主控
  在 RDL skill 记一条"统计 unit 声明必须与计算一致"方法论教训（与 V058 同主题）。
- **Li 2024 TCCN 不可得**：IEEE paywall + blit 0-hit，入 coverage gap；D4（已读）作
  strongest task-matched comparator 已足够（baseline-adjudication: 不追逐每篇 recent）。
- **claim ceiling = CANDIDATE/LOCAL_SLICE**：单 testbed（CB1）、7 cells、20 seeds、
  DP-coherent 16QAM after tuned fixed-μ CMA。

## 9. 验收 checklist（task §4）

- [x] Phase A 四判据、collision、coverage/convergence（§3 A3/A4；lit notes）
- [x] Phase A/B0 gate（§4 B0；feasibility_report）
- [x] Phase B：公式单测（§4 B3，9/9 PASS）、方法表（§4 B1，8 方法）、raw/prefix closure
      （artifacts 1120+140 rows）、relative paired statistics（§4 B4 master 重算）、
      safety、mechanism、strongest comparator（D4）、D1 read-note/read-log（V058 debt 闭合）
- [x] formal_science_disposition 与 mission_method_delta 分开（§5）
- [x] changed files、验证命令、commit receipt（§6）
- [x] 明确"本包后无第二个 G1 repair"（§7）
