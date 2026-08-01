# [S007] P08-R2 receiver 信息边界 + AST 门 + 统计功效合同三根因修复

> 2026-08-01 | campaign P08-R2 / SCIENCE_INTEGRITY_REPAIR | 状态: done（V075 19/19 ACCEPT）
> 来源: S006 续做（P08-R 漏审三项承重科学合同）

## 目标

执行用户 P08-R2 最终科学修复指令：修复 P08-R (D048/V074) 漏审的三项承重缺陷（H7 equalize true-SNR 上游泄漏 / H8 AST verifier 不递归 / H9 MDE post-hoc + CI_lo=0 + min(B1,B2) cherry-pick），在真正 gamma_bar-free 的 corrected receiver 链上重新裁决 coded-LLR-calibration 问题。P09 继续暂停，不另计编号。本轮必须在同一对话完成：旧缺陷复现→campaign 回退→receiver 完整去除 true-SNR→metamorphic 信息门→正确功效设计→fresh crossing 实验→条件式方法工厂→独立 verifier→一次统一 commit。不 push。

## 记录

### Route check（三句）
1. 本轮不是 P09，是修复 P08-R 漏审的三项承重科学合同（P08-R2, SCIENCE_INTEGRITY_REPAIR，不计有效包数，同 P07-R/D046 与 P08-R/D048 模式）。
2. P08-R 的 GG/oracle/identity/H4-H6 修复有效，作 PARTIAL reusable asset 保留；但 P08-R 科学结果（V074 ACCEPT / `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` / G 族关闭 / accepted_valid=8）无效——它在 receiver 仍消费 true SNR 的链上得出。
3. 只有修复后实验有效，才能恢复 accepted_valid 到 8/10；在此之前维持 7/10、G 族不关闭、P09 暂停。

### Phase 1 根因复现（prefail evidence，修复前确定性证据）
H7 数值复现脚本 `p08r2_h7_reproduce.py`：固定 rX/rY/sX/sY/h/theta/prefix/codeword/noise realization，只翻 `real.gamma_bar` 12→18/8dB，max\|ΔeqX\| 高达 **0.145**、max\|Δprefix_resid\| 高达 0.108、max\|ΔB0 LLR\| 高达 **7.02**（远超 tol 1e-12/1e-9）。**H7 CONFIRMED**：deployable decide 间接消费 true SNR。H8（V074 check #5 只扫 method 函数体不递归）+ H9（MDE=0.2347 是固定 n 后 power 阈值 / CI_lo=0 / min(B1,B2)）逐 file:line + 数值复现全部确认。证据存 `p08r2_prefail_evidence.md` + `p08r2_h7_reproduce.json`。

### Phase 2 治理纠偏（D049）
- accepted_valid 8→7；current=P08-R2；P09 继续暂停；G 族重开（coded-LLR-calibration 不再判 PROBLEM_ABSENT）。
- V074 标"16/16 consistency + H1-H6 PASS 但 H7/H8/H9 漏审"，保留不删；旧 artifacts 加 INVALIDATED_BY_P08R2.md。
- D048 GG/oracle/identity/H4-H6 修复 + D047 入口裁决继续 active 作 PARTIAL reusable asset。

### Phase 3 receiver 信息边界根修（p08r2_chain.py + metamorphic 门，旧 p08r_* 不动）
- `estimate_pre_eq_noise_from_prefix()`：用 32-sym 已知 prefix 对 2×2 effective channel 做 LS 解 H_eff（4 复未知数 / 64 复方程，60 dof 残差），返回 receiver-visible σ²_pre。**不读 gamma_bar**。
- `CodedRealizationR2.equalize()`：盲 h 估计噪声底用 σ²_pre（替代 1/(2γ)）；MMSE 第 3 参用 γ_vis=1/σ²_pre（替代 gamma_bar）；amp_limit(3.0) 固定绝对 clip 保留。
- B0/B1/B2 的 `estimate_sigma2_from_prefix`（post-eq σ² for demap）不变——σ²_pre 喂 equalize，post-eq σ² 喂 demap，互补。
- **metamorphic 信息门**（`p08r2_metamorphic_gate.py`）：固定 realization 只改隐藏 gamma_bar (6/9/12/15/18/22 dB)，断言 max\|Δeq\|<1e-12 且 max\|ΔLLR\|<1e-9。**门 PASS**：所有 cell worst max\|ΔeqX\|=0.00e+00, worst max\|ΔLLR_X\|=0.00e+00（精确零）。

### Phase 4 正确功效设计（p08r2_phaseA.py，修 H9）
- **MDE 先验化**：mde_fer=0.05（按 D005 务实路线 + 论文级 FER delta），NOT post-hoc power 阈值。power 分析改为"在登记 MDE 下算 n_required≈814（p=0.17）；实际 n_test=40（INSUFFICIENT 但 CI_hw≤MDE/2 仍可判）"。
- **去 min(B1,B2)**：B2 为单一预登记 conventional comparator；B0-B1 / B0-B2 两条独立 delta 分别报。
- **evidence_insufficient 终态**：CI_hw > MDE/2 报此态不报 absent。

### Phase 5 fresh crossing 实验（p08r2_run.py，新 dev 9000-9019 + 新 test 8000-8039）
- chosen_cell = weak/1000Hz/12dB（dev B0 FER≈0.15，在 operating region [0.1,0.3]）。
- test 40 fresh trajectories × 6 方法 paired，424.8s。
- mean FER: B0=0.155 / B1=0.155 / B2=0.148 / O0=0.155 / O1=0.153 / O2=0.139（全聚集，无 LLR 校准信号）。
- delta_B0_minus_B2: mean=+0.0063 CI=[+0.0008,+0.0141] hw=0.0066（CI_lo>0 但 ≪ MDE=0.05）。
- delta_B2_minus_O2: mean=+0.0094 CI=[+0.0016,+0.0195] hw=0.0090（≪ MDE）。
- evidence_sufficient=True（CI_hw≤MDE/2）；conv_helps=False；oracle_headroom=False。
- mechanism：3/40 B0 all-cw-fail（deep burst），O2 也 2/40 不可恢复；O2 partial rescue 6/40。
- verdict：**`PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`**（同 P08-R 物理机制，但这次在真正 γ-free corrected 链 + 先验 MDE + 新 seeds + 无 cherry-pick 下得出）。

### 独立 verifier V075
脚本 `p08r2_verify.py` 19 项确定性检查全 PASS + 独立 sub-agent（fresh context，不信任 executor 自述）沿 caller→callee **递归** AST 检查科学信息边界，逐项核 H7/H8/H9 + metamorphic 门 + 统计合同，最终 **ACCEPT**。

## 决策引用

- D049：P08-R2 三根因修复（新建）——冻结 P08-R 科学结论 H7/H8/H9，campaign 8→7，重做 gamma_bar-free corrected chain。
- V075：P08-R2 独立 verifier 19/19 ACCEPT（新建）——取代 V074 科学层。
- CP040：mission-log checkpoint（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D047 scope-change 授权 coded-chain 场景扩展 + S006 P08-R 续做，本轮修复 P08-R 漏审的三项承重缺陷，未扩范围；P09 入口准备是 D047 既定 next_legal_action）。

## 后续

- campaign accepted_valid 恢复 8/10，G 族关闭。
- 仍 0 active carrier；claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。
- P09 入口准备（不运行）：必须换不同机制族（G 已关闭），候选 coded operating-boundary / receiver-ranking，须重新过 problem gate。
- 旧 P08-R 数字不得进入论文或 harvest，除非被 P08-R2 新结果重新支持（新结果支持同一物理归因但 corrected chain）。
- TL 教训：P07-R/D046 → P08/D048 → P08-R2/D049 是 "consistency≠correctness" 教训三度重演——verifier 必须递归遍历 deployable 调用图（不只复述合同/扫函数体字面）+ 跑运行时 metamorphic 门。此条已记入 V075。
