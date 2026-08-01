# INVALIDATED — P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH

> 状态: **EXECUTION_INVALID/KILL_C3**（D053/V079，2026-08-01）
> 取代: D052 EVIDENCE_INSUFFICIENT 科学结论（D052 入口门裁决 + chronology 闭合 Commit 1 freeze receipt 模式仍有效作方法论资产）
> 保留原因: 历史可追溯 + chronology 闭合模式（V077 教训首次落实）供后续 P10 复用；不删不覆盖

## 六项承重缺陷（独立语义审计 6/6 PASS，agent_d4ffc6b4 fresh-context）

1. **(8,8)-16APSK π/4 旋转对称** — `_modulation.py:199-201`，旋转点集 k=1..7 max|min_dist|<7e-16
2. **B0 64 点含 8 组对称重复** — `p09_bps_methods.py:134,75-78`，metrics[k] vs metrics[k+8] max|Δ|<4.5e-15 → 64 点实际 8 独立相位
3. **C3 记账欺骗真实成本仍 64 eval/sym** — `p09_bps_methods.py:329` 先 `bps_objective_matrix(rx_block, phases_all)` 全算 64×N，`:348` 只计 B_used×N → 报告 8 eval/sym 是事后少报已发生 FLOP
4. **C3 非数据驱动 adaptive 是恒定截断** — `p09_bps_methods.py:335-342`，π/4 对称致 B_used 恒定=B_min（freeze receipt dev_summary 证实 B_min=8 三档 thresh evals 全=8.0）
5. **resolve 用 TX bits → truth-resolved BER 违反 forbidden_information** — `_modulation.py:278,301,304-308` + `p09_bps_methods.py:381`，resolve_m16apsk_blockwise 接收 tx_bits 选最低 BER 旋转 → 输出 PI-BER 非 fixed-label BER，违反 `p09_run.py:99` 合同
6. **0.10dB↔0.005BER 换算差 12× + 无 paired Δ CI** — `p09_run.py:509,513,522`，实际 0.10dB≈0.00042 BER（dBER/dSNR@18dB=-0.004178），mde_ber=0.005 宽 12×；`:310-318,468` bootstrap_ci 每 method 独立非 paired ΔBER

## 综合结论

C3 "early-stop adaptive BPS" 是三重无效方法：①已在 `:329` 全算 64（记账欺骗）；②B_used 因 π/4 对称恒定（非 adaptive）；③对照基线 B0 含 8× 冗余（8× reduction 恰好等于去冗余）。所有性能/复杂度结论不可信。

## V078 漏审（"consistency ≠ correctness" 第四度重演）

V078 11/11 ACCEPT 但漏掉全部 6 项承重缺陷：check 5 误判 resolve 用 tx_bits 为"不反馈进相位估计"（但 forbidden_information 是"不进 deployable decide"，resolve 是 decide 一部分）；check 6 只对 B_used×N 公式不查 `:329` 是否先全算；check 9 不核 mde_ber 换算；缺失运行时 metamorphic 门。模式同 P07-R/D046 → P08/D048 → P08-R2/D049。

## 处理

- P09 代码和 artifact 保留不删（本标记 + D053/V079 记录纠正）
- campaign 维持 7/10（EXECUTION_INVALID 不计有效包）
- H_BPS 轴关闭：只剩"将搜索域缩到 π/4 基本域"的传统实现纠错资产（非方法）
- 禁止 P09-R、禁止扩大 n、禁止把 fixed basic-domain BPS 包装成方法（用户合同）
- 见 D053/V079 完整记录
