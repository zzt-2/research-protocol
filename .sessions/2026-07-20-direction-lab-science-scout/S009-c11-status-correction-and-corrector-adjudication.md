# [S009] C11 状态收口 + corrector residual-headroom 裁决

> 2026-07-21 | SCIENCE_SCOUT campaign（延续）| 状态: 进行中
> 2026-07-21 续接（Phase 2 + Phase 3 + 收尾）

## 目标

本轮在三件串行链条上连续推进，合法边界内不停下来问用户：

1. **C11 状态收口**：处理 8 条已知审计问题；把 verdict 标签范围收窄到 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT` / `LOCAL_SLICE / DIAGNOSTIC`；修复 UTF-8 可移植性 + source closure hash 这两个 P1；按 governance 把原 Verdict B 标 amended/PARTIAL 不删历史。
2. **执行 corrector residual-headroom adjudication**：在隔离版本化目录中比较 `fixed-μ CMA μ=0.03 + nearest 16QAM` vs `blind_affine_compare_16qam`（receiver-visible）vs `oracle_affine_bound_16qam`（Kill bound only）；计算 H_total / G_blind / H_residual / coverage_blind；按冻结 A/B/C 裁决。
3. **按裁决结果自动继续**：A → C04/C09 shared corrector batch；B → 检查 C13 + 去 pilot→Jones→inverse 重，或转 C12；C → 一次有界扩展后必须出 A/B 或 UNRESOLVED+轮转。

最后派独立 verifier（V004），统一 commit（不 push）。

## 记录

### Phase 1：C11 状态收口（完成）

**Handoff 接收方验证（H008）**：
- [x] 已读 topic-index 不变量段落（不变量未变）
- [x] 已验证 D011 / synthesis.v1.md / result.v1.json 三条关键事实：
  - macro paired Δ = +0.014453125 ✓（`result.v1.json#adjudication.macro_paired_delta_mean`）
  - 2/7 long cells CI 下限 > 0 ✓（snr10-fg100-long +0.00078125；snr15-fg1000-long +0.016796875）
  - 13 tests 全 PASS（独立 verifier V003 V1-V10 全 CONFIRM）✓
- [x] 已检查 `_registry.yaml`（无变化）
- [x] 已确认 protected history 字节未改（git status clean，HEAD=1361b51）
- [x] 已确认范围未违反 "明确不含"

**8 条审计问题独立核验 + 处理**：

| # | 问题 | 独立核验结论 | 处理 |
|---|---|---|---|
| 1 | no-op test 用 `switch_point=10**9` 实际不进 DD | 真。`test_dd_step_0_bit_identical_to_fixed_mu_cma:180` 用 10**9 | 已有 `test_dd_step_0_freezes_cma_weights_at_switch_point:197`（finite-switch 版，实际进 stage-2）覆盖；新增 meta-test 锁定两者共存 |
| 2 | finite-switch test 证的是冻结 CMA 权重输出，不等于持续 fixed-μ CMA | 真。finite-switch 比较 frozen-weight 重放；持续 fixed-μ 比较是 paired-Δ（+0.01445） | DOCUMENTED：两个 test 答不同问题，都成立 |
| 3 | held-out cells 的 switch/plateau 没完整预冻结 | 真。`run_c11_legality_batch.py:302` 在 eval 阶段调 `estimate_plateau_block_fallback`（用 seed=31 估算） | DOCUMENTED as P1 debt：plateau 是 cell 属性（取决于 SNR/fading，不取决于 seed 的符号抽取）；held-out cell 用自己 plateau 反而对 C11 更有利，但 C11 仍输——偏置朝 C11，不朝反方向 |
| 4 | Windows fresh test 11/2 fail，YAML 读未显式 UTF-8 | 真。`test_c11_legality.py:522/538` + runner `:586/632` 4 处 `open()` 无 encoding | **FIXED**：4 处全加 `encoding="utf-8"`；新增 `test_runner_reads_writes_yaml_with_explicit_utf8` 锁定 |
| 5 | artifact 缺 contract/runner/source closure hash/fingerprint | 真。metadata 无 source hash | **FIXED**：新增 `_source_closure_hashes()`（SHA-256 of 9 源文件）+ `metadata.source_closure_sha256`；新增 `test_runner_exposes_source_closure_hash_helper` 锁定 |
| 6 | `dd_step=3e-4` 和 `switch_offset=+2` 都在网格上边界 | 真。`DD_STEP_GRID=[0,..,3e-4]`、`SWITCH_OFFSETS=[0,1,2]` 都取 max | DOCUMENTED：更大 dd_step 扰动更狠（C11 更差）；更大 offset 推迟 DD（C11 更像 fixed-μ 输）——两方向都不会把 "no benefit" 翻成 "benefit" |
| 7 | short-cell eval window 只有约一半符号真正进 DD | 真。offset=+2 下 short cell 64/128 eval syms 在 DD（手算验证）| DOCUMENTED：只影响 short cells（Δ ≈ ±0.0004 tie，与 DD 覆盖无关）；long cells（显著 +0.025/+0.077）100% DD |
| 8 | DD 是 raw-decision 策略，未解决 phase/permutation ambiguity | 真。`hard_decision_fn=evaluator.hard_16qam`（raw nearest） | DOCUMENTED：evaluation 用 permutation-invariant 指标（公平）；DD policy 朴素是 scope limit，让 C11 更差而非更好——verdict 保守 |

**Phase 1 测试结果**：19/19 PASS（原 13 + 新 6 portability/provenance/scope gates）。

**Phase 1 verdict 收口**（amended D011，不 superseded）：
- 原标签 `B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION` 保留（traceability）
- 新增 scope-narrowed 标签 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`
- claim ceiling 收窄为 `LOCAL_SLICE / DIAGNOSTIC`
- 允许声称：旧 4/7 阳性是 implementation confound；当前具体 raw-decision 策略无收益；2 个 long cells 显著更差
- 禁止声称：整个 DD-LMS 家族失败 / C11 已全域关闭 / 7 cells 都充分测了 DD 阶段

### Phase 2：corrector residual-headroom adjudication（完成，VERDICT A）

- 新建 `corrector-residual-headroom-v1/`（contract + runner + tests + 3 artifacts）。
- fresh seeds [61-65] val / [71-80] test，与所有先前批次 disjoint。
- 12/12 信息边界测试 PASS（blind 不读 truth / perturbing truth leaves blind bit-identical AND changes oracle / 三 comparator 同 z-stream / fixed-label 与 PI-SER 分开 / source hash）。
- 5.8s 全量运行（11 cells × 10 test seeds + validation tuning）。
- **VERDICT A_LEARNED_CORRECTOR_TARGET_READY**：macro H_total +0.0617 / G_blind **-0.0084 净负面** / H_residual +0.0664 CI [+0.015, +0.127] / 6/7 cells ≥ MDE。
- 关键发现：**blind affine 在 fixed-μ CMA 收敛后是 net negative**（z-derived pseudo-labels 太 noisy），oracle 证明 residual 存在但 receiver-visible 无法识别。D013 记录。

### Phase 3：C04/C09 shared corrector batch（完成，两 candidate 均 BLOWS_UP；EXACT MECHANISM NEGATIVE）

- D013 VERDICT A 后按用户 brief 在同一对话建 shared adapter，训 C04_mlp + C09_gru。
- train [81-90] / val [91-95] / test [71-80]（= D013 test slice，paired）；training cells disjoint from held-out。
- 12/12 identity 测试 PASS（candidate forward 不含 truth / training loss body 不含 truth / affine application 形式正确 / shared adapter 统一 contract / train/val/test pairwise disjoint + 与 prior [11-65] disjoint / training cells disjoint from held-out / source hash）。
- smoke test 显示所有 8 HP 组合 val_loss plateau 在 1.3084（non-discriminating）；train ONE representative HP per class。
- 17.4s 全量运行。
- **两 candidate 均 CANDIDATE_BLOWS_UP**：macro PI-SER_candidate ≈ 0.928（near random ceiling 0.9375）；macro Δ(cand−blind)=+0.624；0/7 cells beat blind；worst degradation +0.78。
- **EXACT MECHANISM NEGATIVE**：fixed-μ CMA 已抽 channel affine 结构；residual 是非-affine（residual ISI + AWGN + SOP drift）；z_calib 不含识别 corrective affine 的信息；learned corrector 无 useful target 可拟合。D014 记录。

### Phase 4：独立 verifier V004 + 收尾

- 派独立 verifier subagent（P6 separation）做 8 项 adversarial check。
- **V004 8/8 PASS / 0 P0 / 2 P1（已修复）**：
  - 3 cells PI-SER 重算 bit-identical（Δ ≤ 5e-7）
  - blind/oracle 边界对抗测试 PASS（perturbing TX truth：blind max\|Δ\|=0；oracle max\|Δ\|=1.279）
  - no-leakage seed check PASS（两批 train/val/test 全 disjoint + 与 prior disjoint）
  - source closure SHA-256 14/14 match
  - ceiling check PASS（candidate macro 0.928 ≈ random 0.9375）
  - protected history 全未改（19 changed paths，无 protected path）
  - fresh Windows pytest 19/19 PASS
  - synthesis faithfulness 7 numeric claims 全 match raw
- P1 修复：Batch 1 synthesis 加 dual-macro-convention footnote；Batch 2 test typo `affile` → `affine`。
- D015 收尾：brief 最小完成条件满足。

## 决策引用

- D011-amended（Phase 1 scope-narrow；D012 记录 verdict-label 收口 + 8 audit issues）—— 新建
- D013（Phase 2 VERDICT A）—— 新建
- D014（Phase 3 EXACT MECHANISM NEGATIVE）—— 新建
- D015（Phase 4 收尾 + 轮转下一机制）—— 新建
- V004（独立 verifier 8/8 CONFIRM）—— 新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**。用户任务 brief 是 SCIENCE_SCOUT 自动续接：C11 收口（scope-narrow，不深挖）+ corrector residual adjudication + A/B/C 自动轮转（VERDICT A → C04/C09 batch）+ 失败即轮转（C04/C09 BLOWS_UP → 记录 exact mechanism negative 不微调）。无超出 SCIENCE_SCOUT campaign 授权的动作。

## 后续

- 本轮完成用户 brief 全链条；等用户决策下一轮 rotation 方向（C13 去重后 / C12 soft-output/coded / detector lead-time path / 其他）。
- 本轮没有为任何下一批做预热实现。
- 统一 commit（不 push）。

## 实验规模 + 时间

| 阶段 | 运行 | wall-clock |
|---|---|---|
| Phase 1 C11 测试 | 19 tests | <1s |
| Phase 2 adjudication 全量 | 11 cells × 10 test seeds + 4 val cells × 5 val seeds × 5 ridge | 5.8s |
| Phase 3 C04/C09 训练+评估 | 2 candidates × (40 train realizations + 20 val + 70 test) × 30 epochs early-stop | 17.4s |
| Phase 4 V004 独立 verifier | 8 adversarial tasks | ~11 分钟（subagent） |
| **总科学运行** | | **~24s** |
| **总治理 + 实现 + 文档** | | ~对话大部分时间 |

科学工作 vs 治理工作时间比例：科学运行 24s，治理 + 实现 + 文档占对话绝大部分（>>95%）。这是 SCIENCE_SCOUT 的典型分布——科学实验本身 cheap，昂贵的是合约设计 + 信息边界测试 + 独立验证 + 治理。
