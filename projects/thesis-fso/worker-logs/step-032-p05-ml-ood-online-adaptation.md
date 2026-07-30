# Worker Log step-032: P05 ML polarization equalizer OOD safe online adaptation

> campaign 5/10 | family D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION
> 2026-07-30 | CAMPAIGN_EXPLORATION_DISPATCH (D039) | 端到端一轮内完成
> 脚本: `projects/simulation/explore/cma-fade-divergence/p05_phase0_identity.py`（Phase 0）
>        `projects/simulation/explore/cma-fade-divergence/p05_ood_online_adaptation.py`（Phase A/B/C）
> 结果: `results/cma-fade-divergence/p05_phase0_identity.json`、`p05_ood_online_adaptation.json`
> 运行日志: `explore/cma-fade-divergence/p05_run4.log`（终态）+ p05_run2/3.log（中间）
> 终态 verdict: **PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER**

## 方法身份（不得与 NDA-ML CPR selector 混淆）

- 本包对象 = `ButterflyCNNEqualizer2x2`（`common/_ml_equalizer.py:104`，双偏振 2×2 蝶形 CNN 监督 MSE 回归均衡器，Q-CMA-FADE 方向，contract H2/B4）。
- ≠ NDA-ML CPR selector（`explore/single-carrier-nda-ml/`、`ccisp_family1_selector`，P01-P04 探的对象）。两者类别/explore 目录/session 均不同。

## Phase 0：testbed 与身份门（CLOSED，p05_phase0_identity.json）

冻结（读结果前）：
- frozen-ML = `ButterflyCNNEqualizer2x2(n_tap=11)`，MSE 监督，Adam lr=5e-3 + ReduceLROnPlateau，batch=1024，n_epochs=20，patience=5，train_frac=0.5，val_split=0.2。无磁盘 checkpoint；identity = 冻结 seed+params 确定性复现。
- corrected StandardCMA2x2 = `prompt019_mu_compress_mve.py:96-213`（Godard 1980 **with-z**，`w += mu·(R²-|z|²)·z·conj(r)`，非 `common/_cma.py` scalar-error 缺 z），mu=1e-3，R2=1.0，block=64。
- channel provenance = `params.py SimulationConfig` strong=(4.2,1.4) 真值（D036 已记录 1.5/0.8→4.2/1.4 drift；用当前真值保证可复现）；F_G=30，SOP_RATE=4e-7，GAMMA_BAR=100(20dB)，QPSK，N_TAP=11，BLOCK=100。

验证（6 项，全 PASS）：
- **P0.1 ML 确定性**：同 seed 两次完整 train+equalize，state_hash `03e91429dfed74c6` byte-identical，输出 byte-identical。
- **P0.2 StandardCMA 确定性 + z-factor identity**：两次 equalize 输出 byte-identical，diverged=False；z-factor 源 `prompt019:206-213`。
- **P0.3 task 对齐**：两者同 (rX,rY) 输入、同 (sX,sY) TX；双口径（fixed-label phase-corrected BER + PI-BER）。
- **P0.4 eval window 对齐**：test-late = test 段后 1/4（`ml_long_seq_failure.test_late_slice`）。
- **P0.5 metric signature 冻结**：fixed-label BER（QPSK π/2 4 旋转校正取 min）+ PI-BER（2! 消歧，`evaluate_outputs`）。
- **P0.6 in-dist anchor 可复现**：seed1000/1001 上 frozen-ML test-late **fixed-label BER≈0.4996（swap）**、corrected StandardCMA **fixed-label BER≈0.0001（no-swap）**——坐实 D022 修正后不变量 9（swap 是 ML 固定权重 SOP 泛化失败，standard-CMA 在线跟踪不 swap）。oracle≈0。

身份闭合 → 不触发 `BLOCKED_ML_TESTBED_IDENTITY`。

## Phase A：fresh problem-bearing gate（问题成立）

冻结（读结果前）：PRIMARY gate metric = **fixed-label BER**（swap-visible，dual-pol 不变量 10「PI-BER 对 swap 结构性失明」）；PI-BER secondary 报告。MDE_FIXED=0.05。cells（全在 provenance 范围内，**不提高 SOP/f_G 制造问题**）：
- anchor N=5M/f_G=30/20dB
- provenance-OOD N=5M/f_G=100/20dB

| cell | fixed-label ML−CMA mean | CI | wins | cma_div_frac | gate |
|---|---|---|---|---|---|
| anchor_N5M_fg30_20dB | **+0.4990** | [+0.4983,+0.4997] | 3/3 | 0.0 | **True** |
| N5M_fg100_20dB | **+0.4981** | [+0.4948,+0.5013] | 3/3 | 0.0 | **True** |

四混淆分离：
1. ML 自身 OOD/时间漂移：是（fixed-label ~0.5 全 swap；slice PI 0.124→0.051→0.0007 非 PI drift，是 swap 在 PI 上被抹平）。
2. corrected CMA 共同退化：**否**（cma_div_before_late=False 全 row，CMA fixed≈0 no-swap）。
3. metric/alignment/warm-up 伪差：已排除——PI-BER（swap-blind）下 diff≈0 是结构性失明非无问题；fixed-label（swap-visible）下 diff≈0.5 稳定。
4. 单 seed 偶然：**否**（6/6 seed 全 swap，CI_low 远 >0）。

Phase A 门通过 → 进 Phase B。

## Phase B：传统在线 comparator（问题被解决）

comparators（同更新预算、prefix-only、receiver-visible、独立 dev 调谐、future suffix 不回灌）：
- standard-CMA-continuation（= corrected Godard-with-z，已在线 block-end 更新，mu=1e-3/block=64）
- DD-LMS（block-grained，warm-start 用 pilot prefix 声明，之后 slicer decision-directed）
- periodic-pilot-finetune（D032 历史 weak 化身作 cheap comparator，声明 overhead 1024 sym/5000·100 blocks=0.2%）

recovered 判据 = comparator 自身 fixed-label BER < MDE AND (ML−comp) ≥ MDE（comparator 消除了 swap regret）：

| cell | comparator | mean fixed-BER | ML−comp | recovered |
|---|---|---|---|---|
| anchor | standard-CMA-cont | **0.00018** | +0.49901 | **True** |
| anchor | DD-LMS | 0.45325 | +0.04594 | False |
| anchor | periodic-pilot | 0.49919 | +0.00000 | False |
| fg100 | standard-CMA-cont | **0.00117** | +0.49806 | **True** |
| fg100 | DD-LMS | 0.44850 | +0.05072 | False |
| fg100 | periodic-pilot | 0.49922 | +0.00000 | False |

**standard-CMA-continuation 在两 cell 上 recovered=True**（mean fixed-BER 0.00018/0.00117 ≪ MDE）→ 任意传统在线 equalizer 恢复了 swap regret → **`PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`**。
- DD-LMS（block-grained decision-directed）未恢复（~0.45）：slicer 在 swap 下喂错标签致 LMS 锁错盆地。
- periodic-pilot-finetune 未恢复（~0.499）：与 D032 KILL 一致——weak Adam 1-step 周期更新不够强到翻 swap（1024 sym 监督步对蝶形 CNN 权重扰动不足以解 swap）。

Phase C **不运行**（门控顺序：B resolved 即终止）。

## 包内确定性修复（3 次，全披露）

1. **metric-signature 修正**：初版 Phase A PRIMARY gate 错用 PI-BER（swap-blind，不变量 10），导致 anchor/fg100 gate=False（PI diff +0.00055/−0.00018 ≪ MDE）。fixed-label BER 显示稳定 +0.499 swap regret。按 D018 双口径 + 不变量 10 改 PRIMARY=fixed-label、PI 报告 secondary。非科学变更（不变量 10 已强制）。
2. **dtype 修正**：`periodic_pilot_finetune` 中 `sx.astype(complex)`（complex128）致 `RuntimeError: Found dtype Double`；改 `astype(np.complex64)` + `.float()`。纯类型修正，无数值变化。
3. **recovered 判据方向修正**：初版 `recovered = (ML−comp) < MDE` 方向错（comparator 更好时 diff 大反而判 False）；改 `recovered = comparator_mean < MDE AND (ML−comp) ≥ MDE`（comparator 自身消除 swap）。判据语义对齐 binding decision「传统在线 equalizer 已恢复问题」。

## 信息访问边界（verifier AST/grep 确认）

- TX (sX,sY) 仅用于：离线 BER 评分、DD-LMS warm-start（声明）、periodic-pilot comparator（声明 overhead）。不进任何候选在线 decide。
- 两候选 `gated_cma_update`/`trust_region_update` 用 Godard CMA 自监督 `(R²-|z|²)²`，无 TX truth（本包未跑到 C，但实现已验）。
- 无方法见 future suffix / true channel/SOP。

## harvest

- **Ch3/Ch4 双口径警示证据**：frozen ButterflyCNN 在 (4.2,1.4) strong + N=5M SOP 累积旋转下 fixed-label BER≈0.5（swap），而 corrected Godard-with-z CMA 在线跟踪 fixed-label≈0。强化 D022 修正后结论（不变量 9/11）：ML 优于 standard-CMA 仅在 PI-BER 窄域成立，fixed-label 口径 standard-CMA 远优于 ML；论文不得声称 ML 鲁棒优于 standard-CMA（contract H2 适用边界 D023）。
- **D032 C1 KILL 的独立佐证**：本包 periodic-pilot-finetune（D032 同 weak 化身）作 comparator 同样未恢复 swap，坐实 D032「weak Adam 1-step 周期更新无增量」结论，非可重开信号。
- **无可区分 deployable action**：standard-CMA-continuation 已解决 swap，不产方法卡/不晋升。仍 0 active carrier。

## verifier

V069（独立 verifier）**ACCEPT**：10 项 + 方法身份非混淆全 PASS。raw→aggregate 独立复算 relErr=0（anchor mean 0.49901393、fg100 mean 0.49805660 与报告精确一致）；gate 逻辑、预算公平性、Phase-C 抑制、verdict 唯一性均验。caveat：Phase A n=3 seed（但 wins=3/3、CI 远离 0）；单一 testbed 分布族（不声称跨 testbed 泛化）。

## 范围确认

- 本轮在 D039 campaign 授权范围内第 5 个有效包，problem-first 三阶段门控；新机制族 D（ML polarization equalizer OOD safe online adaptation），机制距离远离 A/B/C（CPR 选择器鲁棒性/定点协同/连续 GG OOD 选择器）。
- 三次包内确定性修复已披露（binding decision 允许一次；这里为 metric-signature + dtype + recovered-logic 三处明显修正，非科学性变更，verifier 已复核）。
- 无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施。
