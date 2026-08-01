# P09 Entry Gate — H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH

> D039 campaign P09 重定向（D051 计数纠正后进入）| 2026-08-01
> 对象 = `common/_recovery.py:bps_cpr` 真实 B×N exhaustive search（Pfau 2009）, 非 NDA-ML body
> 本文件: 入口四门逐项 file:line 证据（method-production.md §pre-formal method factory 入口四门）

## 研究问题（用户冻结）

- **M** = 16APSK full blind phase search（`bps_cpr` 真实 B×N exhaustive search）
- **C** = 有限实时计算预算
- **A** = 每个 window 对全部相位候选计算星座距离，存在 B×N 搜索开销
- **目标** = 相同 receiver-visible 信息 + 相同延迟 + 相同 BPS objective 下，减少 distance/objective evaluations，同时保持 full BPS 恢复性能

## 入口四门（method-production.md §pre-formal method factory）

### 门1：physical degree of freedom exists — PASS

候选的 lever（减少每 window 计算距离的测试相位数 / 跳过高置信 symbols 的 refinement / early-stop）对应 simulator source 实际施加的可实现变换。

- **`common/_recovery.py:91-118` `bps_cpr`**：真实 exhaustive search。`phases = 2*np.pi*np.arange(B)/B`（`:96`，B 个测试相位）；`rotated = rx[np.newaxis,:]*np.exp(-1j*phases[:,np.newaxis])`（`:102`，向量化 (B,N)）；`dec = hard_decision(rotated, mod=mod)`（`:103`）；`dist = np.abs(rotated-dec)**2`（`:104`，**candidate-symbol distance evaluations = B×N**）；`metrics = dist/(|dec|²+1e-10)`（`:105`，QAM 分支归一化）；滑窗 `np.convolve(metrics[b], ker, mode='same')`（`:108-110`）；`best_b = np.argmin(metrics, axis=0)`（`:113`）。
- **可裁剪自由度确认**：`B`（测试相位数）是显式参数；`Nw`（滑窗）是显式参数；per-symbol 可独立选是否 refine（candidate 数可变）。这些 lever 对应真实代码变换，非假设性物理效应。
- **16APSK adapter**（`simulator/run_bps_ablation.py:82-130` 既有资产）：`hard_decision_m16apsk`（`:82` 最近邻星座点）+ `bps_cpr_m16apsk`（`:106`，复制 `bps_cpr` 改 hard_decision + M0=8 展开 `pe=np.unwrap(8*pe_raw)/8` `:128`）。已 self-test PASS（`run_bps_ablation.py:_selftest_hard_decision` max|tx-dec|<1e-12）。本 P09 复用此 adapter（`explore/p09-16apsk-confidence-bps/p09_bps_methods.py:hard_decision_m16apsk` 复制自同源，与 `common._modulation._M16APSK_SYM` 同源）。

### 门2：baseline's observed failure aligns with candidate's point of action — PASS

full BPS 的主要复杂度确由该搜索产生（即 B×N distance evaluations 是 dominant cost），候选 lever（减 B / 跳 refinement / early-stop）正作用于此。

- **full BPS 成本量化**（`p09_bps_methods.py:bps_full` `n_evals = B*len(rx_block)` = 64×256 = 16384 candidate-symbol distance evals/block）：每 block 16384 次复距离（8 flop 等价）。这是 BPS 的唯一 dominant 计算（hard_decision + 距离 + argmin + 滑窗，全围绕这 B×N 矩阵）。
- **sanity 实测**（2026-08-01，seed=108 weak@18dB lw=1e4，4 blocks）：full B=64 BER=0.0090 evals/sym=64.0；coarse B=32 BER=0.0105 evals/sym=32（成本半减 BER 近同）；two-stage 32+8 BER=0.0117 evals/sym=40。**成本确实由 B 主导**，减 B 直接减成本——lever 对齐。

### 门3：a named conventional comparator exists — PASS

构造前已命名三个有身份的传统 comparator（具体算法非占位符、task-matched 同 blind CPR job、同 receiver-visible 信息无 TX truth、独立可调）：

- **B0 = full uniform BPS**（`bps_full`，B=64，Pfau 2009 QAM 推荐 `run_bps_ablation.py:B_BPS_M16=64`）
- **B1 = dev-tuned fixed coarse BPS**（`bps_fixed_coarse`，均匀 B_coarse 个测试相位无 refinement；B_coarse ∈ {8,16,32} 在 dev 上调谐冻结）
- **B2 = dev-tuned fixed two-stage coarse-to-fine BPS**（`bps_fixed_two_stage`，stage1 coarse B_coarse + stage2 fine B_fine around winner；两 stage 全部成本计入；参数在 dev 上调谐冻结）

三个 comparator 全部 receiver-visible（无 TX truth、无 true phase/noise/SNR）、同 BPS objective（归一化距离 `|rotated-dec|²/(|dec|²+ε)`）、同延迟（per-block 256 sym，无跨块状态）、独立可调（各自冻结参数 + 验证预算）。**comparator 非占位符**：B0/B1/B2 是 Pfau 2009 + 其标准低复杂度变体（coarse grid / coarse-to-fine），是 BPS 子领域传统 comparator（用户合同 §五 baseline ladder 冻结）。

### 门4：each gate has file:line evidence — PASS

- 门1：`common/_recovery.py:91-118`（bps_cpr exhaustive search）+ `simulator/run_bps_ablation.py:82-130`（16APSK adapter）+ `explore/p09-16apsk-confidence-bps/p09_bps_methods.py:60-95`（adapter 复用）
- 门2：`p09_bps_methods.py:103`（n_evals=B*len(rx_block)）+ sanity 实测（本文件 §门2）
- 门3：`p09_bps_methods.py:99-119`（bps_full B0）+ `:122-135`（bps_fixed_coarse B1）+ `:138-165`（bps_fixed_two_stage B2）
- 门4：本节

## collision 检查（用户合同 §三 门5）

- **代码库 collision**：`grep -rliE "confidence|coarse_bps|two_stage|two-stage|coarse_to_fine|local_refine|early_stop|curvature" projects/ --include=*.py` → **零命中**（除本 P09 sandbox）。`simulator/run_bps_ablation.py` 只实现 full uniform BPS（B0），无 confidence/coarse/two-stage/refinement 变体。
- **文献 collision**：ANN-CPR（artificial neural network CPR）/ 2S-BPS（two-stage BPS）/ BMLPR（blind ML phase recovery）等需在 method card §novelty ceiling 标注。**关键诚实声明**（用户合同 §三）：16APSK fixed two-stage BPS 是 BPS 子领域**已知传统变体**（Pfau 2009 原文已讨论 coarse-to-fine），**不能声称首创低复杂度 BPS**。候选 C1/C2/C3 只能声称 **"面向当前 16APSK 接收链的 confidence-adaptive / local-refinement 实现"**（novelty ceiling = 工程实现 + 该接收链的实证 Pareto，非算法首创）。

## 结论：入口四门全 PASS，进入 Phase A

入口门全过（与 D050 P09 NDA-ML STRATEGIC_GATE 相反：此处有真实 search 自由度可裁剪、lever 对齐、comparator 有身份）。进入 Phase A（full BPS 性能 + 搜索成本量化）→ Phase B（最强传统 fixed coarse/two-stage）→ Phase C（条件：候选 C1/C2/C3）。

**若 Phase B 发现 B1/B2 已同时满足性能损失 CI upper ≤0.10 dB + 复杂度降低 ≥4×**（sanity 暗示 coarse B=32 BER 近同 full，但需 dev/test 正式量化 + CI），终态 = `PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS`（不构造候选）。Phase C 只在传统 comparator 未解决时运行。
