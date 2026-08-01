# INVALIDATED BY P08-R2 (2026-08-01, D049/V075)

> 本目录 `projects/simulation/results/p08r_coded_chain_repair/` 的 P08-R 科学结论已被 P08-R2 取代。
> 本文件是标记，**不删除、不修改**任何 P08-R artifact（审计保留）。

## 为什么失效

P08-R (D048/V074) 修复了 H1-H6（GG provenance / runtime σ² / oracle action space / metric contract / coded identity / state lifecycle），但**漏审三项承重科学合同**（D049）：

- **H7**：`p08r_chain.py:341-360` `CodedRealizationR.equalize()` 读 `self.gamma_bar`（true SNR 循环变量）三处（盲 h 噪声底 / h_est / mmse_equalize 第 3 参）。数值复现（`p08r2_h7_reproduce.json`）：固定 realization 只翻 gamma_bar 12→18/8dB，max\|ΔeqX\| 高达 0.145、max\|ΔB0 LLR\| 高达 7.02——**deployable decide 间接消费 true SNR**。
- **H8**：`p08r_verify.py:109-129` check #5 只扫 `method_B0/B1/B2` 函数体字面，不递归进 `real.equalize()` → 漏审 H7。
- **H9**：MDE=0.2347 是固定 n=40 后的 power 阈值（非先验 MDE）；CI_lo=0 被当排除信号；`p08r_run.py:286 strongest_conv=np.minimum(B1,B2)` 是 post-hoc cherry-pick。

## 取代关系

- **P08-R V074 ACCEPT / `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` / G 族关闭 / accepted_valid 8**：被 **D049/V075** 取代，全部失效。
- **D048 的 GG/oracle/identity/H4-H6 修复 + D047 入口裁决**：继续 active，作 **PARTIAL reusable asset** 在 P08-R2 (`p08r2_chain.py`) 中 verbatim 复用（CodedContractR / CodecAdapterR / CalibrationPrefix / oracle ladder / get_gg_scenes / 真 3GPP interleaver）。

## P08-R2 在哪里

- 新脚本：`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_*.py`
- 新 artifacts：`projects/simulation/results/p08r2_receiver_info_repair/`
- 新决策/验证：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D049`、`verifications.md#V075`

## 重要

P08-R2 verdict 仍是 `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`（同物理机制：coded loss 主导不可恢复突发深衰落），但**这次在真正 gamma_bar-free 的 corrected receiver 链上得出**，且用先验 MDE + 新 seeds + 无 cherry-pick 的统计合同。P08-R 的数字**不得**进入论文或 harvest；只有 P08-R2 的数字可被引用。
