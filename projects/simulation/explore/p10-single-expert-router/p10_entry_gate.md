# P10 Entry Gate (4-gate file:line proof)

> Package: P10 = RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER
> Authority: D039 campaign + D053 (P09 corrected) + 用户 P10 执行指令
> Date: 2026-08-01

## 入口门 1: fresh 条件下确有 ML/CMA 排名反转，且不是 metric/swap artifact

**历史证据 (D015/S017/S020/D022)**:
- D015 `ML_LONG_SEQ_FAILURE_REPORT.md:18,21` Q1 表 (固定 fg=30/SOP=4e-7/strong/20dB/QPSK 扫 N):
  - N=2M: ML BER=0.050 **赢** CMA BER=0.219 (ML 占优 4.4×)
  - N=8M: ML BER=0.309 **输** CMA BER=0.037 (CMA 占优 8.4×)
- D015 Q2 SOP 扫描 `:37,40`: SOP=1e-7 ML=0.039 赢 CMA=0.057; SOP=1e-6 ML=0.109 赢 CMA=0.498
- S017 N=2M 反预期 `topic-index.md:108`: N=5M late SOP 大→CMA 漂错解→ML 优势显著; N=2M late SOP 小→standard-CMA 完美锁定→ML 监督残余误差反更差
- S020 post-compaction `:15`: f_G=1000 CMA 反超 ML (PI 0.0021 vs 0.0417)

**注意: 用户指令 §二 premise A 描述 "长慢变 ML 占优, 短快变 CMA 占优" 与上述证据方向相反**:
- 证据显示: 短 N + 小 SOP 累积旋转 (<~14°) → ML 占优; 长 N + 大 SOP 累积旋转 (~90°) / OOD f_G → CMA 占优
- P05 (`p05_ood_online_adaptation.json`) 在 N=5M default params.py (4.2,1.4) + fixed-label PRIMARY 口径下: in-dist + OOD 两 cell 都 PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER (CMA 两边都恢复 swap, ML 两边都 swap fixed≈0.5)
- **门 1 不能直接判 PASS**——须 Phase A fresh dev 用 fixed-label PRIMARY 口径独立复现 crossover 真实方向. fresh dev 不能复现 → PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE (用户合同 §入口门)

**crossover cells (合同冻结)**:
- `ML_favored_hypothesis`: N=2M, f_G=30, SNR=20dB, SOP_RATE=1e-7, strong (基于 D015 N=2M + S017 N=2M)
- `CMA_favored_hypothesis`: N=5M, f_G=1000, SNR=20dB, SOP_RATE=4e-7, strong (基于 D015 N=8M 方向 + S020 fg1000)

**门 1 判定**: **CONDITIONAL-PASS** (历史 crossover 存在但方向与用户 premise A 相反; 须 fresh dev 复现真实方向; 非 metric/swap artifact 须用 fixed-label PRIMARY 口径). Phase A 是 fresh dev 的第一道硬门.

## 入口门 2: 两专家作用和信息合同真实不同

**file:line 证据**:
- ML expert: `common/_ml_equalizer.py:104` `ButterflyCNNEqualizer2x2` (8 实值 1D-CNN 蝶形 4 复 FIR, MSE 监督训练后前馈推理, **不在线更新权重**)
- CMA expert: `explore/cma-fade-divergence/prompt019_mu_compress_mve.py:96` `StandardCMA2x2` (Godard 1980 with-z 梯度 `Δw ∝ (R²-|z|²)·z·r*`, **在线更新权重**)
- 信息合同: ML 训练消费 known pilot/training symbols (合法), 推理只用 rx; CMA 不读 TX truth, 只用 rx + 自身恒模代价. 两专家**机制完全不同** (监督学习 vs 盲恒模在线).
- D036 `decisions.md:2192-2197` 已冻结 Godard-with-z 为 canonical standard-CMA (含 z 因子, `_cma.py` scalar-error 缺 z 不能冒充).

**门 2 判定**: **PASS**.

## 入口门 3: 部署时只执行一个专家具有真实计算或延迟价值

**file:line 证据**:
- ML expert `compute_rmps(n_tap=11)=88` (`_ml_equalizer.py:425`) real mult/sym; CMA 8×n_tap=88 real mult/sym + online update cost. 两专家单跑 ~88 RMpS, 同时跑 ~176 RMpS + 训练成本翻倍.
- ML 训练成本: n_epochs × n_chunks × batch × RMpS × 3 (fwd+bwd), P05 `ml_long_seq_failure.py ML_PARAMS` n_epochs=15 batch=1024 → 训练 ~15 × 488 × 1024 × 88 × 3 ≈ 1.98e9 FLOP per realization (prefix=0.5×N=1M).
- CMA 训练成本: prefix 长度 × 88 × 2 (online update) ≈ 1M × 176 = 1.76e8 FLOP (CMA 比 ML 训练便宜 ~11×).
- **真实延迟价值**: ML 训练 ~79s/seed (P05 measured), CMA ~9s/seed. payload 前只跑一个专家省 ~50% 训练+推理 wall-clock (vs 同时跑两专家后选).

**门 3 判定**: **PASS**.

## 入口门 4: 存在强传统比较 (always-CMA/always-ML/best-global/config-rule/threshold)

**file:line 证据** (`p10_methods.py`):
- B0 `BaselineAlwaysCMA` (`:270`): 固定选 CMA
- B1 `BaselineAlwaysML` (`:276`): 固定选 ML
- B2 `BaselineBestGlobal` (`:281`): dev-tuned 全局最优单专家 pick (frozen at test)
- B3 `BaselineConfigRule` (`:289`): N >= N_thresh -> CMA else ML (deployable config only, 镜像 D015 crossover 轴 N)
- B4 `BaselineThreshold` (`:299`): 单 receiver-visible stat 阈值 (dev-tuned)
- 全部 5 个 comparator 都是 deployable (只用 receiver-visible 信息), 同信息同延迟预算, dev-only tune.

**门 4 判定**: **PASS**.

## 入口门 5: D036 只关闭轨迹内切换，没有关闭执行前单专家选择

**file:line 证据** (`decisions.md:2168-2272` D036 全文):
- D036 标题 `:2168`: "...接收 sprint-003 (NO_DIAGNOSTIC_SIGNAL): 纠正门2 证据等级、冻结 Godard-with-z comparator、action_class 改为 PREFORMAL_METHOD_FACTORY、新增 PROBLEM_RESOLVED 终态"
- D036 影响范围 `:2259`: "CB1 更新粒度均衡族轴关闭 (method-factory 纪律: 无 signal 即退出, 不强行收尾)"
- D036 关闭的具体对象: inherited block-64 anchor / tuned per-symbol Godard-with-z comparator / block-8 / block-16 / sliding-window recursive — **全部是 CMA 内部的更新粒度变体** (block size / per-symbol / sliding window).
- D036 全文 grep "single expert"/"router"/"执行前选择"/"ML vs CMA 选择" **零命中**.
- topic-index `forbidden_actions` 列表 (`:20-43`) 无 SINGLE_EXPERT_ROUTER / PRE_EXECUTION_EXPERT_SELECTION / ML_VS_CMA_ROUTER 条目. 最接近的 CB1_COLLAPSE_RECOVERY_FAMILY 是 D036 关闭的轴 (CMA 更新粒度), P10 不是 collapse-recovery.

**门 5 判定**: **PASS** (D036 不阻塞 P10).

## 入口门 6: primary 指标不使用 TX truth 进行部署决策或消歧

**file:line 证据**:
- primary metric = fixed-label BER (swap-visible 不变量 10, `dual-pol-osl-groundwork/topic-index.md:96-100`)
- router decide 只用 receiver-visible feature (`p10_methods.py:prefix_features :160-220`): rx_power/amp_std/cov/ac1/fade_depth/cma_diag_convergence, 不读 TX payload / true h/SNR/phase/fG.
- payload TX truth 只用于最终计分 (`p10_run.py CONTRACT primary_metric.decision_rule`): "router 只用 receiver-visible feature, payload TX truth 只用于最终计分".
- fixed-label ambiguity resolution: P05 用 `evaluate_outputs` (`prompt012_longseq_audit.py`) 的 fixed_label_ber (不依赖 TX 选择旋转, 直接 label 对比); **注意: P05 fixed-label 实际用了 compute_ber_phase_corrected(zx, sx, 0.0)** — 这是真 fixed-label (不试 8 旋转选最低), 不是 PI-BER/truth-resolved. 见 `p05_ood_online_adaptation.py:130` `fixed_ber_slice`.

**门 6 判定**: **PASS** (primary fixed-label BER 不用 TX truth 消歧, router decide 不读 TX truth).

## 总结

| 门 | 判定 | 关键证据 |
|---|---|---|
| 1 fresh crossover 非 artifact | **CONDITIONAL-PASS** | D015/S017/S020 历史证据存在但方向与用户 premise A 相反; 须 Phase A fresh dev 复现真实方向 |
| 2 两专家作用和信息合同不同 | PASS | ML `_ml_equalizer.py:104` vs CMA `prompt019:96`; D036 冻结 Godard-with-z |
| 3 单专家执行有真实价值 | PASS | RMpS=88 each, 训练成本 ML~11× CMA, 同时跑翻倍 |
| 4 强传统比较存在 | PASS | B0-B4 五个 deployable comparator |
| 5 D036 不闭单专家选择 | PASS | D036 只闭 CB1 更新粒度族, P10 不在范围 |
| 6 primary 不用 TX truth 消歧 | PASS | fixed-label BER 直接 label 对比, router feature 不读 TX truth |

**入口四门 CONDITIONAL-PASS (门 1 conditional, 2-6 PASS)**. 进入 Phase A fresh crossover confirmation. Phase A 不能复现 → PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE.
