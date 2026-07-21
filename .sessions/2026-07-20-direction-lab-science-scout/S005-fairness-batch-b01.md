# [S005] Fairness Batch B01 — 机制级扩图 + 公平调参 + 首批科学运行

> 2026-07-21 | SCIENCE_SCOUT phase 3 (Map→Plan→Prepare→Run→Synthesize→Harvest) | 状态: 完成
> 来源: H004 续接

## 目标

按 H004 / D007 的三个宏阶段连续推进：
A. 机制级 Portfolio 扩图（12-18 候选，纠正 readiness/comparator）
B. baseline 公平性收口 + 立即运行首批 READY 候选
C. synthesis + harvest + 独立 verifier + 治理更新

## 记录

### 阶段 A：Portfolio v3 扩图（portfolio-refresh.v3-fairness.yaml）

从 C01-C04 扩到 **13 个机制级候选**（C01-C13），覆盖 **9 个功能簇**：

1. 失败可观测性（C01/C02/C05）
2. 异常/OOD/置信度（C06）
3. 重初始化/算法切换（C03/C07）
4. 自适应步长/窗口/block（C08）
5. 输出修正（C04/C09）
6. 均衡器结构/更新（C10/C11）
7. soft-output/LLR/coded（C12，blocked）
8. CSI/pilot/闭环（C13）
9. 基础设施阻断高价值（C03/C12）

**Readiness 纠正**（D007 §5）：
- C01/C02/C04/C06/C09/C10/C13 → NEEDS_SMALL_ADAPTER（共享 causal feature stacker 或新 runner variant）
- C03/C07/C12 → INFRASTRUCTURE_BLOCKED（action hook / coded evaluator）
- **C05/C08/C11 → READY**（无 ML，无 adapter）

**Comparator 分层**（D007 §5）：
- 共同 system anchor = `cb1_dual_pol_osl_16qam`（end-to-end PI-SER）
- 任务专属 comparator：检测器族用 C05；控制器族用 C07；修正器族用 blind_affine；均衡器结构族用 anchor

### 阶段 B：Fairness Batch B01 运行

**合同**：`batch-contract.v1.yaml`（运行前冻结）
- 候选：{C05, C08, C10, C11}
- 共享 question："坍塌是否在公平调参 + 结构变化 + 级联下存活？"
- 公平协议：per-method tuning budget（4 validation cells × 5 seeds × 5 hyperparameter candidates），divergence penalty，frozen-before-held-out

**实现**（`b01_candidates.py`，7/7 sanity tests PASS）：
- C05: CUSUM (Page 1954) + threshold on output_power/(2·R²)
- C08: LinUCB (Li WWW 2010) 选 μ per batch
- C10: per-symbol SGD CMA (block_size=1)
- C11: CMA + DD-LMS cascade (Sato 1975)

**运行**（11 cells × 10 paired seeds × 4 candidates，43-59s）：

| cell | anchor | C08 | C10 | C11 | anchor_head | C11_head |
|---|---:|---:|---:|---:|---:|---:|
| snr20-nominal-long | 0.3055 | 0.2992 | 0.3070 | **0.3023** | 0.2324 | 0.2289 |
| snr15-fg1000-long | 0.3219 | 0.3141 | 0.3277 | **0.3102** | 0.1477 | 0.1352 |
| snr10-fg100-long | 0.4273 | 0.4094 | 0.4371 | **0.3984** | 0.0547 | **0.0234** |
| (short cells) | ≈anchor | ≈anchor | ≈anchor | -0.002~-0.003 | 0.31-0.33 | 0.31-0.33 |

**关键结果**：
- **PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT**：held-out 7 cells 上 anchor/C08/C10/C11 各只关闭 1/7（snr=5 AWGN floor）
- **C11 是最佳变体**：long cells 改善 0.01-0.03 PI-SER，headroom 减半但远未关闭（仍 ≥6×MDE）
- **C10 per-symbol 略差于 anchor**（H021 基础设施缺口假设 **不被支持**）
- **C05 detector pooled AUROC=0.6546**（28 collapsed / 82 healthy），long cells 上 AUROC=1.000
- **0 divergence** 跨所有 110 seeds（公平调参生效）

### 阶段 C：综合 + 收获 + 独立复核

**Synthesis**：`fairness-batch-b01-v1-synthesis.md`，结论 PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT + 条件授权 B02

**Harvest**（H023-H028）：
- H023 BASELINE_ADJUDICATION：坍塌在公平调参/结构/级联下存活
- H024 FAILURE_MECHANISM：per-symbol CMA 不优于 anchor（H021 不支持）
- H025 METHOD_SIGNAL：C05 detector AUROC=1.000 在可分 cells，pooled 0.6546
- H026 REUSABLE_ASSET：b01 代码 + tuning 协议可复用
- H027 EVALUATION_INSIGHT：AUROC 条件依赖 convergence length
- H028 LOCAL_NEGATIVE：简单 LinUCB bandit 不显著优于固定 μ

**独立 verifier**：CONFIRM，HIGH confidence，20/20 检查 PASS（identity gate / fairness / numerical / history / claim scope / contract）。2 个 minor 程序性建议（tuning grid drift 已修复 + headroom 定义澄清）已处理。

### D007 公平性债务处置总结

| 债务 | 处置 | 状态 |
|---|---|---|
| #1 same mu | per-method tuning budget（C08/C10/C11 各自 grid） | CLOSED |
| #2 convergence N | long validation cell + long held-out cells | PARTIALLY_CLOSED（坍塌在 long 上仍存活） |
| #3 block-end causality | C10 per-symbol 直接测试 | CLOSED（H024：per-symbol 不帮助） |
| #4 oracle recoverability | C05 detector 证明 receiver-visible 部分可检测 | PARTIALLY_CLOSED（AUROC=0.65 pooled） |
| #5 task-specific comparators | cluster-level（C05/C07/C11） | CLOSED |
| #6 candidate narrowness | v3 扩图到 13 候选 9 簇 | CLOSED |

## 决策引用

- D008：B01 完成 + 条件授权 B02 ML detector batch（本 session 新建）
- D007：被本 session 部分超越（公平性债务闭合，但 B02 授权条件已更新）
- 无其他新决策

## 范围确认

- 本轮是否在 scope boundary 内：**是**（H004 的 A/B/C 三宏阶段全部完成；未修改 protected history；未训练 ML；未 push）

## 后续

- **B02 ML detector batch 已条件授权**（C05 pooled AUROC=0.6546 ∈ [0.65, 0.85) → narrowed claim "ML improves lead time / calibration"）
- 候选：C01/C02/C06，任务 comparator = C05
- 共享 adapter sprint：causal feature stacker（half-day）
- 若 B02 FAIL → rotate 到 C13（pilot-aided，不同信息类）
- 若 B02 PASS → B03 learned correctors {C04, C09}（task comparator = blind affine）
