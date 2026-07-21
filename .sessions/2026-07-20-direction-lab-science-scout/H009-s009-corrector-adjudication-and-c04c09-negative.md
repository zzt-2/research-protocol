# Handoff: S009 完成 — corrector residual-headroom VERDICT A → C04/C09 EXACT MECHANISM NEGATIVE

> 来源: S009 / D012 / D013 / D014 / D015 / V004 | 交接目标: 用户审 S009 全链条结果；通过后开新对话决定下一轮 rotation
> 日期: 2026-07-21
> 文件名: H009-s009-corrector-adjudication-and-c04c09-negative.md
> 取代: H008（H008 不删除，标 amended by H009——C11 scope-narrow + 新批结果叠加；H008 的 C11 数值结论仍有效）

## 到哪了（状态）

用户 brief 要求的 SCIENCE_SCOUT 连续链条已完成：

- **C11 状态收口（D012）**：verdict 标签 scope-narrow 到 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT` / claim ceiling = LOCAL_SLICE / DIAGNOSTIC。数值结论（macro +0.01445、2/7 long cells 显著更差、4/7 阳性撤回）**不变**。修了 2 个 P1（UTF-8 可移植性 + source closure hash），8 audit issues 全独立核验为真但无一改变 verdict 方向。19/19 tests PASS（原 13 + 新 6 portability/provenance gate）。
- **Corrector residual-headroom adjudication（D013）= VERDICT A_LEARNED_CORRECTOR_TARGET_READY**：在 fresh paired seeds（val [61-65] / test [71-80]，与所有先前批次 disjoint）+ 同 z-stream / 同 eval window / 同 paired realization 下：
  - macro H_total = +0.0617 CI [+0.0024, +0.1210]（recoverable headroom 存在）
  - macro G_blind = **-0.0084**（blind affine **净负面**，CI [-0.0153, -0.0025]）
  - macro H_residual = +0.0664 CI [+0.0147, +0.1270]
  - 6/7 cells H_residual ≥ MDE
  - 12/12 信息边界测试 PASS
- **C04/C09 shared corrector batch（D014）= 两个 candidate 均 CANDIDATE_BLOWS_UP（EXACT MECHANISM NEGATIVE）**：shared adapter（`apply_correction(z_eval, A, b) = z_eval @ A.T + b`），C04_mlp（context=summary stats）+ C09_gru（context=time series）。train [81-90] / val [91-95] / test [71-80]（= D013 test slice，paired comparison）；training cells disjoint from held-out；HP grid non-discriminating。两 candidate macro PI-SER_candidate ≈ 0.928（near 16QAM random ceiling 0.9375）；macro Δ(cand−blind) = +0.624 CI [+0.483, +0.753]；0/7 cells beat blind；worst degradation vs fixed_cma = +0.78。**Context-dependent affine hypothesis REJECTED**：fixed-μ CMA 已抽 channel affine 结构，residual 是非-affine，z_calib 不含识别 corrective affine 的信息。
- **独立 verifier V004 8/8 CONFIRM**：0 P0，2 P1（Batch 1 synthesis 双 macro 约定 footnote + Batch 2 test typo），都已修复。

git HEAD：S009 三批产物待 stage（corrector-residual-headroom-v1/ + c04-c09-shared-corrector-v1/ + c11-legality-batch-v1 的 amendment 文件 + .sessions 治理更新），consolidated commit。

## 关键科学发现

1. **"exists vs learnable" gap = thesis-grade 发现**。D013 证明 residual EXISTS（oracle affine closes H_total ≈ 6% PI-SER）；D014 证明 residual NOT LEARNABLE from receiver-visible signals。Oracle 用 TX truth 才能识别该 affine；receiver-visible proxy（z-derived pseudo-labels）太 noisy。这是可毕业的负面论文材料。
2. **blind affine 在 fixed-μ CMA 收敛后是净负面**（G_blind = -0.0084，6/6 cells）。z-derived pseudo-labels 拟合出的 affine 有害。这是第二个独立角度的证据，与 D014 的 learned-corrector negative 互证。
3. **C04/C09 candidate PI-SER ≈ 0.928** = 16QAM random-decision ceiling 0.9375。candidate 学到的 (A, b) scramble z_eval。训练 loss plateau 在 1.3084（每个实坐标距 grid ~1.1）= 模型可达下界，无 useful target 可拟合。
4. **C11 verdict 不变**（D012 只 scope-narrow claim label，不改数值）；protected history 全未改（V004 确认）。

## 不要做什么

1. **不要**重启 C04/C09 借口"调参不够"：HP grid 显示 non-discriminating（所有 8 组合 plateau 在同一 val_loss）；用户 brief 明示 "若两者均失败，记录 exact mechanism negative，并轮转，不继续做网络微调"。
2. **不要**把 D013 VERDICT A 解读成 "learned corrector 必定能赢"：A 只证明 residual target 存在 + blind 未关闭；D014 已证明 receiver-visible learned affine 也无法拟合该 residual。
3. **不要**改 anchor 或 channel 试图救活 corrector：超出本轮 scope；D014 的 negative 是 "在 fixed-μ CMA μ=0.03 + 16QAM atlas 下" 的 LOCAL_NEGATIVE。
4. **不要**修改 B01 raw / B01-R raw / B001-B003 / P03 / CB1 raw / canonical-state / c11-legality-batch-v1 的 `result.v1.json`（V004 已确认全未改；这些是 protected history）。
5. **不要**用 D013/D014 数字直接进论文正文：scope-ceiling = LOCAL_RESULT_SLICE；晋级须用户明确 strategic 决策。
6. **不要**把 C04 和 C09 当两个独立机制方向：它们是同 corrector 任务的函数类变体（用户 brief 明示）；D014 的 negative 覆盖整个 "context-dependent learned affine" 假设，不只 MLP 或 GRU。

## 必读（按优先级）

1. `.sessions/2026-07-20-direction-lab-science-scout/H009-s009-corrector-adjudication-and-c04c09-negative.md`（本文件）
2. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/corrector-residual-headroom-v1/artifacts/synthesis.v1.md`（§0 TL;DR + §3 headroom 表 + §4 verdict）
3. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c04-c09-shared-corrector-v1/artifacts/synthesis.v1.md`（§0 TL;DR + §3 results + §5 exact mechanism negative）
4. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` D012 / D013 / D014 / D015
5. `.sessions/2026-07-20-direction-lab-science-scout/verifications.md` V004（8/8 CONFIRM）
6. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（D012-amended + D013 + D014 + D015 + S009 进展线索）
7. `.agents/skills/research-direction-lab/references/evidence-and-claims.md` + `baseline-adjudication.md`（不变）

## 接口变更（本轮新增，下一对话可复用）

```yaml
# corrector-residual-headroom-v1/run_corrector_adjudication.py（新模块）
evaluate_one_cell_one_seed(cell, *, seed, ridge, eval_window) -> dict
  # ONE CMA run, ONE window, 3 comparators (fixed_cma / blind / oracle).
  # Returns pi_ser + fixed_label_ser for all 3, plus pi_ber for transparency.
  # All three comparators share the SAME z-stream, SAME eval window, SAME paired realization.

# corrector-residual-headroom-v1 的 frozen params（写入 frozen-params.v1.yaml）
fixed_mu_cma_mu: 0.03            # inherited from B01-R HF6
blind_affine_best_ridge: 1.0e-08 # validation-tuned on [61-65]
validation_seeds: [61, 62, 63, 64, 65]
test_seeds: [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
mde: 0.005

# c04-c09-shared-corrector-v1/src/corrector_adapter.py（新模块）
MLPCorrector(hidden_dim) / GRUCorrector(hidden_dim, gru_layers)
  # Both expose: calibrate(z_calib), get_correction() -> (A [2,2] complex, b [2] complex)
apply_correction(z_eval, A, b) -> z_corrected = z_eval @ A.T + b[None, :]
_summary_statistics(z_calib) -> 10-dim real feature vector
_z_to_real_features(z_calib) -> [N, 4] real array

# c04-c09-shared-corrector-v1 的 frozen params
blind_affine_ridge_frozen: 1.0e-08  # from corrector-residual-headroom-v1
training_seeds: [81..90]   # NEW, disjoint from all prior
validation_seeds: [91..95] # NEW
test_seeds: [71..80]       # = D013 adjudication test slice (paired)
training_cells: 4 validation cells (disjoint from held-out)
hp_grid: {hidden_dim: [32, 64], learning_rate: [1e-3, 3e-3], weight_decay: [0, 1e-4]}
  # HP non-discriminating; train ONE representative HP per class
n_epochs: 30, early_stop_patience: 5

# c11-legality-batch-v1 amendments（D012）
# run_c11_legality_batch.py + tests/test_c11_legality.py:
#   - 4 处 open() 加 encoding="utf-8"
#   - 新增 _source_closure_hashes() + metadata.source_closure_sha256（9 源文件 SHA-256）
#   - 新增 TestPortabilityAndProvenance 类（6 tests）
```

下一对话若要复用 corrector adjudication 流程，import `corrector-residual-headroom-v1.run_corrector_adjudication`。若要复用 shared corrector adapter，import `c04-c09-shared-corrector-v1.src.corrector_adapter`。

## 失败数据附录

| 现象 | 失败模式 | 数据 |
|---|---|---|
| C04/C09 candidate 在所有 7 cells 上 PI-SER ≈ 0.928 | learned (A, b) scramble z_eval | macro Δ(cand−blind)=+0.624 CI [+0.483, +0.753]；worst Δ(cand−fixed_cma)=+0.78 |
| 训练 loss 不论 HP plateau 在 1.3084 | 模型无 useful target 可拟合 | 8 HP 组合 val_loss 全在 1.3084 ± 1e-4；1.31 ≈ 每坐标距 grid ~1.1 |
| blind affine 在 6/6 cells 上 net negative | z-derived pseudo-labels 拟合出的 affine 有害 | macro G_blind=-0.0084 CI [-0.0153, -0.0025]；coverage_blind=-0.19 |
| H_residual 在 snr05-short 上为负 | oracle 在该 cell 也无力（H_total=0） | snr05-short H_residual mean=-0.0156 CI [-0.0242, -0.0074]；oracle_PI=0.62 vs fixed_PI=0.59 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| C11 audit #1/#2/#3/#6/#7/#8 未 FIX（只 DOCUMENTED） | scope 限制不构成缺陷 | DOCUMENTED（D012 §10 表） | 未来若重评 DD-LMS 需先解决 |
| C04/C09 corrector 路线 CLOSED | EXACT MECHANISM NEGATIVE | CLOSED（D014） | 若换信息访问（soft-output / coded）或换 anchor 可重开 |
| Oracle affine 是 TX-truth bound | FR-21/FR-25 | INVARIANT | 永远不当 Go baseline |
| C12 soft-output/coded INFRASTRUCTURE_BLOCKED | 需 soft-FEC evaluator | BLOCKED | 建基础设施后可启动 |
| C13 pilot-aided 未去重 | 可能与 pilot→Jones→inverse 微变体重 | PENDING | 下一对话先去重 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| corrector-residual-headroom 信息边界测试 (12) | 全 PASS | batch-contract identity_tests | 12/12 PASS（V004 独立复核） |
| H_residual macro ≥ MDE | ≥ 0.005 PI-SER | batch-contract Verdict A | PASS（+0.066） |
| H_residual macro CI 下限 > 0 | statistically significant | batch-contract Verdict A | PASS（+0.015） |
| H_residual ≥ MDE 在 ≥ 5/7 cells | stable | batch-contract Verdict A | PASS（6/7） |
| C04/C09 worst degradation ≤ MDE | 不退化 | batch-contract BEATS_STABLY | FAIL（+0.78） → BLOWS_UP |
| No-leakage seed split | train/val/test pairwise disjoint + 与 prior disjoint | AGENTS.md / contract | PASS（代码 assert + V004 复核） |
| Source closure SHA-256 | 14 files match | AGENTS.md / contract | PASS（V004 重算 14/14 match） |
| Protected history 字节未改 | git diff 在 protected paths 上空 | AGENTS.md / contract | PASS（V004 git diff 复核） |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（不变量未变；新增 oracle 边界、H_total/G_blind/H_residual 定义在 D013）
- [ ] 已验证 D013 / D014 / V004 至少 3 条关键事实：
  - [ ] macro H_residual = +0.066350（`corrector-residual-headroom-v1/artifacts/result.v1.json#adjudication.macro_h_residual`）
  - [ ] macro G_blind = -0.008371（同上 `macro_g_blind`）
  - [ ] C04_mlp macro Δ(cand−blind) = +0.623940（`c04-c09-shared-corrector-v1/artifacts/result.v1.json#adjudications.C04_mlp.macro_delta_candidate_minus_blind`）
- [ ] 已检查 `_registry.yaml`（无变化）
- [ ] 已确认 protected history 未改（V004 已确认；续接方可 git log --oneline 查最新 commit + git diff HEAD~1 --name-only 在 protected paths 上为空）
- [ ] 已确认当前范围未违反 "明确不含"

## 下一轮

**不自动启动**——等用户战略决策。合法的下一轮候选：

1. **C13 pilot-aided**：需先去重已否决的 pilot→Jones→inverse 微变体。如果 C13 只是该微变体，直接跳过；否则选 C13 中真正不同的信息机制。
2. **C12 soft-output/coded**：INFRASTRUCTURE_BLOCKED；若启动需先建 soft-FEC evaluator 基础设施（bounded adapter sprint 允许，但若成本超预估登记 INFRASTRUCTURE_BLOCKED 再轮转）。
3. **Detector lead-time path（C01/C02/C06）**：H007 ready，unblocked；task comparator = min_z2_ratio（AUROC=1.000 ceiling）；Go metric = positive mean lead time on ≥ 2 two-class cells without AUROC regression。
4. **其他 portfolio 项**：用户可选。

本轮**没有**为任何下一批做预热实现。S009 完成 C11 收口 + corrector adjudication（VERDICT A）+ C04/C09（EXACT MECHANISM NEGATIVE）三件事，满足用户 brief 最小完成条件（1 adjudication + 1 mechanism negative）。
