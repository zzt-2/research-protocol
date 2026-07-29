# Step 025 — G1 有边界毕业方法包装

> Task: T025 (THESIS_METHOD_PACKAGING, CP023, control epoch 56)
> Date: 2026-07-29
> 来源: S002 / live D032 / formal D041 / V060
> Status: `PACKAGING_BOUNDARY_READY_FOR_MASTER_REVIEW` | mission_method_delta: `PACKAGING_BOUNDARY`
> **只做写作包装；不补实验 / 检索 / 全文 / formal repair；不 push。**

## 0. Task boundary（纪律自检）

- 本步只把既有算法动作、可信局部数字、适用边界与证据债整理成方法包，供主控 / 论文
  后续选用。
- **未做**：新增实验、检索、全文精读、formal repair；未修 T024；未改任何科学代码；
  未晋级正式主线。
- **只新增两个授权文件**：
  - `projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md`
  - `projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md`（本文件）
- **未改**：`.sessions/**`、master-state、current YAML、T019–T024 artifacts、`common/`、
  `params.py`、`cb1_evaluator.py`、`cb1_cell_runner.py` 等任何其他文件。

## 1. 启动门与 clean 起点

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T025-g1-bounded-thesis-packaging.md
# → PASS
git status --short   # → clean（起点无改动）
```

Validator PASS，起点 clean，满足起飞硬门。

## 2. 实际读取的证据

按任务 §1 顺序读取：

1. `AGENTS.md`
2. `.agents/skills/research-direction-lab/SKILL.md`、`references/evidence-and-claims.md`、
   `references/thesis-harvest.md`
3. `thesis-lessons.md` 速查表 + TL-20 / TL-22 / TL-23 / TL-30–TL-33
4. `.sessions/.../topic-index.md`、`verifications.md` 的 V060、`decisions.md` 的 D032
5. `.../g1-safe-gated-normalization-confirm/src/methods.py`（`gated_scalar_*`）
6. `.../artifacts/{result.json, raw-rows.csv, prefix-receipt.csv, synthesis.md}`
7. `projects/thesis-fso/worker-logs/step-024-g1-safe-gated-normalization.md`
8. external-output skill（`SKILL.md` + `rules/claims.md` + `rules/translation.md`）

## 3. 证据冲突核查（Gate6 CI 口径）

任务 §2.2/§2.3 与 T024 的 `result.json` 残留审计文字在 Gate6 CI 上存在表述冲突。
按任务"数字以 V060 独立复核为准"的指示核对 V060 / D032 全文后确认：

- **正确口径**：seed-cluster pooled bootstrap 95% CI ≈ `[0.885, 1.000]`（V060、D032 接收）。
- **禁用口径 1**：`[0.5, 0.6579]`——执行器把单类 seed 缺失 recall 记 0 后算 per-seed
  balanced accuracy，不是任务 §B4 的 pooled seed-cluster estimand。
- **禁用口径 2**：`[0.8905, 1.0]`（pair-bootstrap）——违反冻结的 seed-cluster 单位。

本包正文判别 CI 一律采用正确口径，并在 provenance appendix 与证据矩阵脚注中说明两个
禁用字段为何禁用。**无未解决的证据冲突。**

## 4. Package 文件路径

`projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md`

包含任务 §3 要求的全部结构：总判断（三档，推荐第 2 档）、方法定义（问题 / 思想 / 输入输出
与因果边界 / 公式 / 伪代码 / 复杂度 / 与两种朴素方案机制区别）、论文叙事（3 标题 / 中文
摘要 / 3 候选贡献带可写强度 / 2 句克制英文 / 3 放置位置 + 禁用措辞）、证据矩阵（claim–
evidence–scope–debt 四列，每数字附仓库路径）+ 图表计划（规划不生成）、不可声称项与升级
最小证据清单、provenance appendix（内部代号仅在此处）。

## 5. 使用 / 拒绝的全部数字

### 使用（均经 V060 或 result.json 复核一致）

| 数字 | 来源 | 用法 |
|---|---|---|
| eligible 49 对；混淆 TP/FP/FN/TN = 19/1/1/28 | result.json `activation` + V060 | 判别诊断 |
| point balanced accuracy = 0.957759 | result.json `activation` | 判别诊断（非泛化精度）|
| seed-cluster pooled bootstrap CI ≈ [0.885, 1.000] | V060（正确口径）| 判别 CI |
| collapse ΔPI-SER −0.559796，CI [−0.6947, −0.4064]，help/hurt 12/0 | result.json `cluster_stats.collapse.gated_scalar` + V060 | 塌缩恢复（条件子集）|
| healthy worst = 0；healthy cluster 均值 −0.0028409，CI [−0.0085, 0.0]；误激活 1/29 | result.json `cluster_stats.healthy.gated_scalar` + `activation` | 健康零退化 |
| G1−M4 collapse −0.035457，CI [−0.0466, −0.0243] | result.json `g1_vs_m4_collapse` | 谱系消融（仅 ablation）|
| 门控阈值 collapse=0.6 / spread=0.1；前缀 128 符号；截尾 10% | methods.py `gated_scalar_freeze` | 方法定义 |

### 拒绝（不写进正文或明确标注禁用）

| 数字 | 来源 | 拒绝原因 |
|---|---|---|
| Gate6 CI [0.5, 0.6579] | result.json `bacc_ci_95_seed_cluster_CORRECT` | 非 pooled seed-cluster estimand（V060 禁用），仅在 provenance 说明 |
| Gate6 CI [0.8905, 1.0]（pair-bootstrap）| result.json `bacc_ci_95` | 违反冻结 seed-cluster 单位（V060 禁用）|
| D4 作"已超越直接竞品" | result.json D4 Δ=0 / Gate7 | D4 apply 是恒等占位，非 likelihood-gated tap-update，不能当直接竞品胜利 |
| 精确 FLOP / 硬件时延 | 无依据 | 不臆造，复杂度只作定性描述 |
| 全样本平均收益（overall mean_delta）| result.json `cluster_stats.overall` | collapse 是条件子集，不可当全样本收益 |

## 6. 主张边界检查（对照任务 §2.3 / §3.5）

- [x] 未声称四判据 / novelty / collision 已正式关闭（Phase A 闭包未成，不可独立复核）。
- [x] 未声称已赢直接竞品（D4 为恒等占位）。
- [x] 未把 conditional result（collapse stratum）写成 overall result。
- [x] 未暗示 formal Go（当前 disposition =
      `G1_GROUNDWORK_EVIDENCE_INCOMPLETE / PHASE_B_NONBINDING_DIAGNOSTIC`）。
- [x] 未使用"首次 / 显著优于 / state of the art / 普遍适用 / 已验证可部署 / 解决了盲均衡"。
- [x] 对外正文（§1–§5）无内部代号 G1 / T024 / V060 / D032 / Gate6；仅 provenance appendix（§6）保留。
- [x] 证据强度统一标 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。

## 7. Changed files

```text
projects/thesis-fso/direction-lab/harvest/g1-safe-gated-normalization-package.md   (新增)
projects/thesis-fso/worker-logs/step-025-g1-bounded-thesis-packaging.md           (新增，本文件)
```

无其他文件改动。

## 8. 独立 reviewer 审查

已委托独立 reviewer 对 package 做只读审查，6 项检查（公式一致性 / 数字一致性 / conditional
是否被写成 overall / 是否暗示 formal Go·novelty·竞品胜利 / 对外正文是否去掉内部治理语言 /
是否只新增两个授权文件）。

### 初审结论：P0=0 / P1=2 / P2=0，判 FAIL（P1>0）

- 公式一致性（criterion 1）：PASS — 与 `methods.py` `gated_scalar_*` 逐项一致。
- 数字一致性（criterion 2）：PASS — 全部数字与 `result.json` + V060 一致。
- conditional 是否写成 overall（criterion 3）：PASS — collapse 数字始终标为条件子集。
- 是否暗示 formal Go / novelty / 竞品胜利（criterion 4）：PASS — 判别 CI 采用 V060 正确口径
  [0.885, 1.000]；D4 未声称被超越；证据强度标 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。
- 对外正文是否去掉内部治理语言（criterion 5）：**FAIL（P1×2）** — §4.1 中出现内部代号
  `G1−M4`（证据表 cell）与 `V060`（统计口径脚注）。
- 是否只新增两个授权文件（criterion 6）：PASS — `git status` 仅两个授权新文件。

### 修复（针对 2 个 P1）

- §4.1 证据表 cell：`ΔPI-SER(G1−M4)` → `ΔPI-SER(本方法 − 非线性半径重映射)`。
- §4.1 统计口径脚注：`本包统一采用 V060 独立复核确认的正确 ... CI ≈ [0.885, 1.000]`
  → `本包统一采用独立复核确认的正确 ... CI ≈ [0.885, 1.000]（独立复核记录编号见 §6
  provenance appendix）`。

### 复审结论：P0=0 / P1=0 / P2=0，判 PASS

用确定性 grep（TL-21）扫描 §1–§5（Provenance appendix 之前）对 `G1 / M4 / T024 / V060 /
D032 / D041 / Gate6 / Phase A / Phase B / FR-21 / FR-25` 做词边界匹配：**0 命中**。
内部代号已全部收敛到 §6 provenance appendix。公式与数字未改动（初审已 PASS），故无需
复审数值正确性。

**最终：P0/P1/P2 = 0/0/0，审查通过。**

## 9. 验证命令

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T025-g1-bounded-thesis-packaging.md
git diff --check
git status --short
```

确认只新增两个授权文件。每个对话只做一个 consolidated commit，commit message 概括
G1 bounded thesis packaging；不 push。
