# P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER — Verdict

> Package: P10 (campaign 第 10 包 campaign-level 裁决)
> Authority: D039 campaign + D053 (P09 corrected) + 用户 P10 执行指令
> Date: 2026-08-01
> Phase A 完成，Phase B/C 不运行（gate 顺序：Phase A FAIL → 终态）

## 终态: `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE`（不计有效包，campaign 维持 7/10）

## Phase A fresh crossover confirmation — FAIL

**冻结 crossover cells**（基于 D015/S017/S020 证据方向，fixed-label BER PRIMARY + PI-BER secondary）:

| cell | config | mean ML fx_late | mean CMA fx_late | Δ(ML−CMA) | ml_wins | crossover_pass |
|---|---|---|---|---|---|---|
| ML_favored | N=2M, fg=30, SOP=1e-7, strong | 3.3e-07 | 6.1e-05 | -6.1e-05 | 6/6 | **False** (|Δ|≪MDE=0.02) |
| CMA_favored | N=5M, fg=1000, SOP=4e-7, strong | 0.4896 | 0.0396 | +0.4500 | 0/6 | True (CMA 占优) |

- `cma_div_frac = 0.00` 两 cell（无共同退化）
- `crossover_directions_consistent = False`
- `phase_a_verdict = FAIL`

## 为什么 Phase A FAIL（诚实物理归因）

crossover 无法在 fixed-label BER PRIMARY 口径下复现，两 cell 各有原因：

1. **ML_favored cell 走 P05 老路**：在短 N (2M) + 小 SOP (1e-7, 累积旋转 ~11.5°) 下，corrected StandardCMA (Godard 1980 with-z) 已经在 fixed-label 上解决 swap（ML fx≈0, CMA fx≈6e-5，两者都接近完美）。D015 历史 ML 优势（N=2M ML=0.050 vs CMA=0.219）针对的是当时**不同的 CMA 变体**（scalar-error 缺 z 的 current-CMA），而 corrected standard-CMA 在 fixed-label 下已无 ML 优势空间。这与 P05 `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER` 同构。

2. **CMA_favored cell 的 CMA 优势是 swap artifact**：长 N (5M) + 高 f_G (1000) + 大 SOP (4e-7) 下，ML fixed-label BER≈0.49（swap 崩到 random），CMA fixed-label BER≈0.04。但 **PI-BER 显示两者相当**（ML_pi=0.024 vs CMA_pi=0.040，Δ_pi=-0.016）—— ML 的 fixed-label 失败是 π 级 polarization swap，CMA 在线跟踪能跟随，ML 冻结权重无法跟随；而 PI-BER 重排标签后抹掉 swap 影响（不变量 10：PI-BER 对 swap 结构性失明）。因此这个"CMA 占优"是 swap artifact，不是干净的可路由 ranking 反转。

**两 cell 在 fixed-label 和 PI-BER 双口径下方向不一致** → Phase A 诚实判 FAIL。

## 为什么不是其他终态

- **非 PROBLEM_RESOLVED_BY_SIMPLE_ROUTING**：该终态隐含"crossover 存在 + 简单路由规则已解决"。Phase A crossover 不存在，未到 Phase B 判简单规则。
- **非 NO_DIAGNOSTIC_METHOD_SIGNAL**：该终态隐含"crossover 存在 + 候选无增量"。Phase A crossover 不存在，未到 Phase C 候选。
- **非 EVIDENCE_INSUFFICIENT**：CI 宽度不是瓶颈（两 cell Δ 都远离 MDE，ML_favored Δ=6e-5 远小于 MDE=0.02；CMA_favored Δ=0.45 远大于 MDE）。问题是 crossover 本身不存在（非信号弱）。
- **非 STRATEGIC_GATE**：入口门四门 CONDITIONAL-PASS（门1 conditional 已诚实标注须 fresh dev 复现），Phase A 是 fresh dev 复现，结果是 crossover 不存在，属 PROBLEM_ABSENT 非 STRATEGIC_GATE（入口门已过）。
- **非 EXECUTION_INVALID**：合同执行合法（chronology 闭合 + fixed-label PRIMARY 口径正确 + dev seeds fresh disjoint），无合同违反。
- **PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE 是唯一合法诚实终态**：crossover 在 fixed-label PRIMARY 下不成立（P05 老路：corrected standard-CMA 已解决 swap），且 CMA_favored cell 的 CMA 优势是 swap artifact 非 ranking 反转。这是用户合同 §入口门明文允许的 fresh-dev-fail 终态（"若 fresh dev 不能复现 crossover，或 configuration-only rule 已经无遗憾解决，终止为 PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE"）。

## chronology 闭合（V077 教训第二次落实，P09 模式复用）

- Commit 1 (`56fee4c`): P09 纠偏 + P10 frozen contract + pre-test receipt（`test_started=false` 在任何 held-out test 前）
- Phase A 只读 dev seeds 13000-13005（fresh disjoint from 全部 campaign history: P09 11000-11019/12000-12039, P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, P05 1000-1011）
- **未读 test seeds 14000-14039**（Phase A FAIL，Phase B/C 不运行，无 held-out test 需要）
- freeze receipt `test_started` 维持 false（无 held-out test 执行）

## 处理

- P10 终态 `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE`，**不计有效包**（crossover 不存在非有效科学 negative，是入口门 fresh-dev-fail；count_excludes=entry_phase_A_fail 同 P09 NDA-ML STRATEGIC_GATE 模式但更严格——P09 STRATEGIC_GATE 是入口门未过，P10 是 Phase A fresh dev 复现失败）
- campaign `accepted_valid_packages` **维持 7/10**（D053 纠正后正确计数）
- `current_package` P10（完成，verdict 非 signal）
- Phase B/C 不运行（gate 顺序：Phase A FAIL 直接终止）
- 不建立 method card（verdict 非 METHOD_SIGNAL）
- claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC
- 无 protected owner/formal/Skill/thesis framework 改动、**无 push**

## campaign-level 裁决（P10 是第 10 包）

P10 是 D039 campaign 的第 10 个包（campaign_level_decision_at: P10）。P10 PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE 不计有效包，但作为 campaign-level 裁决点：
- campaign 总计 7/10 有效包（P01-P07-R + P08-R2 PARTIAL）+ P09 EXECUTION_INVALID + P10 PROBLEM_ABSENT
- 仍 0 active carrier（无 RISK_BUDGETED_ROUTER_METHOD_SIGNAL）
- **campaign-level 结论**：D039 授权的 10-有效包探索完成，所有候选 Honest negative 0 signal。crossover-based single-expert router 方向在 fixed-label PRIMARY 下不成立（corrected standard-CMA 已解决 swap，PI-BER CMA 优势是 swap artifact）。campaign 诚实终止，0 active carrier。

## artifact

- `p10_phaseA_dev_raw.json`（Phase A 两 cell × 6 dev seeds raw rows + aggregates + verdict）
- `p10_phaseA_crossover.py`（Phase A executor script）
- `p10_phaseA_dev_run.log`（run log）
- `p10_freeze_receipt.json`（test_started=false 维持，dev_summary 追加 Phase A 结果）
- `p10_entry_gate.md`（入口四门 CONDITIONAL-PASS 证据）
- `p10_methods.py`（ML/CMA expert wrappers + router C1/C2/C3 + comparator B0-B4，Phase B/C 未用但保留作方法论资产）
- `p10_run.py`（freeze receipt + contract + verify）
