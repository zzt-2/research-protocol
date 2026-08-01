# Worker Log: step-040 P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER

> Package: P10 (campaign 第 10 包 campaign-level 裁决)
> Authority: D039 campaign + D053 (P09 corrected) + 用户 P10 执行指令
> Date: 2026-08-01
> Verdict: **PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE**（不计有效包）
> Verifier: V080 13/13 ACCEPT
> D/V: D054 / V080 / CP045
> Commits: Commit 1 `56fee4c` (P09 纠偏 + P10 freeze receipt pre-test) + Commit 2 (pending, 治理同步)

## 任务

在同一对话端到端完成（用户合同）：
- A. 将 P09 从 EVIDENCE_INSUFFICIENT 纠正为 EXECUTION_INVALID/KILL_C3（独立语义审计 6 项缺陷）
- B. 执行 P10 = RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER

## Part A: P09 纠偏（已完成，D053/V079）

### 独立语义审计（agent_d4ffc6b4 fresh-context，6/6 PASS）

逐项 file:line + 数值复算证实六项承重缺陷：

1. **(8,8)-16APSK π/4 旋转对称**（`_modulation.py:199-201`）：旋转点集 k=1..7 全部与原点集双射 max|min_dist|<7e-16。
2. **B0 64 点含 8 组对称重复**（`p09_bps_methods.py:134,75-78`）：metrics[k] vs metrics[k+8] max|Δ|<4.5e-15（数值噪声级）→ 64 phase 实际只有 8 个独立相位。
3. **C3 记账欺骗**（`p09_bps_methods.py:329` 先 `bps_objective_matrix(rx_block, phases_all)` 全算 64×N，再 `:348 n_evals=B_used*N` 只计 B_used）：真实 FLOP=64 eval/sym，报告 8 eval/sym 是事后少报已发生计算。
4. **C3 非数据驱动 adaptive**（`p09_bps_methods.py:335-342`）：π/4 对称致 B_used 恒定=B_min（freeze receipt dev_summary C3 B_min=8 三档 thresh evals 全=8.0；独立验证 5 档 thresh×10 随机块 B_min=8 全 [8×10]）。
5. **resolve_m16apsk_blockwise 用 TX bits**（`_modulation.py:278,301,304-308` + `p09_bps_methods.py:381`）：接收 tx_bits 用 8 旋转选最低 BER → 输出 PI-BER/truth-resolved BER 非 fixed-label BER，违反 `p09_run.py:99 forbidden_information: TX symbols/bits in deployable decide`。
6. **mde_ber=0.005 比 0.10dB 真实换算宽 12×**（`p09_run.py:509`）：dBER/dSNR@18dB=-0.004178/dB → 0.10dB≈0.00042 BER，mde_ber=0.005 宽 12×；+ 无 paired Δ CI（`:310-318,468` 每 method 独立 bootstrap）。

### 综合结论

C3 "early-stop adaptive BPS" 是三重无效方法：①已在 `:329` 全算 64（记账欺骗）②B_used 因 π/4 对称恒定（非 adaptive）③对照基线 B0 含 8× 冗余（8× reduction 恰好等于去冗余）。**V078 11/11 ACCEPT 漏审全部 6 项**（"consistency≠correctness" 第四度重演 P07-R/D046 → P08/D048 → P08-R2/D049 → P09/V078）。

### 处理

- P09 科学终态 EVIDENCE_INSUFFICIENT → **EXECUTION_INVALID/KILL_C3**（D053/V079）
- D052/V078 保留（入口门裁决 + chronology 闭合 Commit 1 freeze receipt 模式仍有效作方法论资产）
- P09 artifacts 加 INVALIDATED_BY_D053.md 保留不删
- campaign 维持 7/10；H_BPS 轴关闭；新增 forbidden H_16APSK_CONFIDENCE_ADAPTIVE_BPS_FAMILY_REOPEN

## Part B: P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER（已完成，D054/V080）

### 入口四门（CONDITIONAL-PASS，`p10_entry_gate.md`）

| 门 | 判定 | 关键证据 |
|---|---|---|
| 1 fresh crossover 非 artifact | **CONDITIONAL-PASS** | D015/S017/S020 历史证据存在但方向与用户 premise A 相反；须 Phase A fresh dev 复现 |
| 2 两专家作用和信息合同不同 | PASS | ML `_ml_equalizer.py:104` vs CMA `prompt019:96`；D036 冻结 Godard-with-z |
| 3 单专家执行有真实价值 | PASS | RMpS=88 each，训练成本 ML~11× CMA，同时跑翻倍 |
| 4 强传统比较存在 | PASS | B0-B4 五个 deployable comparator（`p10_methods.py`）|
| 5 D036 不闭单专家选择 | PASS | D036 `:2168,2259` 只闭 CB1 更新粒度族 |
| 6 primary 不用 TX truth 消歧 | PASS | fixed-label BER 直接 label 对比 |

### chronology 闭合（V077 教训第二次落实，P09 模式复用）

Commit 1 (`56fee4c`) freeze receipt `test_started=false` 在任何 held-out test 前；source/contract hash 校验通过（contract_sha256=8e603bd4，9 文件 hash）；Phase A dev seeds 13000-13005 fresh disjoint；test seeds 14000-14039 未读。

### Phase A fresh crossover confirmation — FAIL

**executor 子 agent fresh-context（agent_8c4b53c6）**，只读 dev seeds 13000-13005（6 trajectory × 2 cell = 12 realization），12.6 min wall-clock，CUDA RTX 4070。

| cell | config | mean ML fx_late | mean CMA fx_late | Δ(ML−CMA) | ml_wins | crossover_pass |
|---|---|---|---|---|---|---|
| ML_favored | N=2M, fg=30, SOP=1e-7, strong | 3.3e-07 | 6.1e-05 | -6.1e-05 | 6/6 | **False** (|Δ|≪MDE=0.02) |
| CMA_favored | N=5M, fg=1000, SOP=4e-7, strong | 0.4896 | 0.0396 | +0.4500 | 0/6 | True (CMA 占优) |

- `cma_div_frac = 0.00` 两 cell（无共同退化）
- `crossover_directions_consistent = False`
- `phase_a_verdict = FAIL`

### 物理归因（诚实）

1. **ML_favored cell 走 P05 老路**：短 N (2M) + 小 SOP (1e-7, 累积旋转 ~11.5°) 下，corrected StandardCMA (Godard 1980 with-z) 已经在 fixed-label 上解决 swap（ML fx≈3e-7, CMA fx≈6e-5，两者都接近完美）。D015 历史 ML 优势（N=2M ML=0.050 vs CMA=0.219）针对的是 scalar-error 缺 z 的 current-CMA，corrected standard-CMA 在 fixed-label 下已无 ML 优势空间。与 P05 PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER 同构。

2. **CMA_favored cell 的 CMA 优势是 swap artifact**：长 N + 高 f_G + 大 SOP 下 ML fixed-label BER≈0.49（swap 崩到 random），CMA fx≈0.04；但 PI-BER 显示两者相当（ML_pi=0.024 vs CMA_pi=0.040，Δ_pi=-0.016）。ML 的 fixed-label 失败是 π 级 polarization swap，CMA 在线跟踪能跟随，ML 冻结权重无法跟随；PI-BER 重排标签后抹掉 swap 影响（不变量 10）。**swap artifact 非 ranking 反转**。

### 终态裁决

**PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE**（用户合同 §入口门明文允许的 fresh-dev-fail 终态，唯一合法诚实）。Phase B/C 不运行（gate 顺序）。

### premise A 反转诚实标注

用户指令 §二 premise A 描述"长慢变 ML 占优，短快变/OOD CMA 占优"与历史证据（D015/S017/S020）方向**相反**——证据显示"短 N + 小 SOP → ML 占优；长 N + 大 SOP/OOD → CMA 占优"。Phase A 用证据支持的方向（ML_favored=短 N 小 SOP；CMA_favored=长 N 大 SOP）测试，结果两方向都不成立 crossover。**无论用哪个方向的 premise，crossover 在 corrected standard-CMA fixed-label PRIMARY 下都不成立**——这是 P05 老路的根本性结论。

## V080 独立 verifier（13/13 ACCEPT）

1. Commit 1 早于 held-out ✓ 2. receipt/source/contract hash 闭合 ✓ 3. Phase A fresh seeds ✓ 4. test_started 维持 false ✓ 5. Phase A crossover 判据诚实 ✓ 6. CMA_favored swap artifact 确认 ✓ 7. ML_favored P05 老路确认 ✓ 8. fixed-label PRIMARY 口径正确（无 P09 缺陷5 truth-resolution）✓ 9. 完整 deployable 调用图无 truth leakage ✓ 10. raw→aggregate relErr=0 ✓ 11. terminal verdict 唯一 ✓ 12. premise A 反转诚实标注 ✓ 13. campaign 计数正确 + campaign-level 裁决完成 ✓

## campaign-level 裁决（P10 是第 10 包）

D039 授权的 10-有效包探索完成：
- **7 有效包 honest negative**: P01 NO_SIGNAL / P02 RESOLVED_REGION / P03 RESOLVED_UNIFORM / P04 ABSENT / P05 RESOLVED_BY_CONVENTIONAL / P06 NO_CAUSAL_HISTORY_INCREMENT / P07-R PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION
- **P08-R2 PARTIAL asset**（chronology 缺陷降级，G 族 STOPPED_WITH_PARTIAL_ASSET）
- **P09 EXECUTION_INVALID**（C3 三重无效 + V078 漏审）
- **P10 PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE**（Phase A crossover 不成立）

**0 active carrier, 0 METHOD_SIGNAL**。campaign 维持 7/10，诚实终止。

## artifact

- `results/p10_single_expert_router/p10_freeze_receipt.json`（test_started=false, dev_summary Phase A 结果）
- `results/p10_single_expert_router/p10_freeze_receipt.sha256`
- `results/p10_single_expert_router/p10_phaseA_dev_raw.json`（Phase A 两 cell × 6 dev seeds raw + aggregates + verdict）
- `results/p10_single_expert_router/p10_verdict.md`
- `explore/p10-single-expert-router/p10_methods.py`（ML/CMA wrappers + router C1/C2/C3 + comparator B0-B4，Phase B/C 未用但保留作方法论资产）
- `explore/p10-single-expert-router/p10_run.py`（freeze receipt + contract + verify）
- `explore/p10-single-expert-router/p10_phaseA_crossover.py`（Phase A executor）
- `explore/p10-single-expert-router/p10_entry_gate.md`（入口四门 CONDITIONAL-PASS 证据）

## 不建立 method card

verdict 非 METHOD_SIGNAL（PROBLEM_ABSENT）。claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。

## 不修改

- protected owner / formal owner / Skill / thesis framework / controller
- common/ frozen 文件、prompt019_mu_compress_mve.py
- 不 push
