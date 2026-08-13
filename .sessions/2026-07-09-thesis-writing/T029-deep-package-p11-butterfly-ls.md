# [T029] 深挖 P11 少导频 Complex-LS Butterfly FIR

> 来源: S024 | 回传给主线程
> 日期: 2026-08-13

## 0. TL;DR

只审 P11 双偏振少导频 complex-LS Butterfly FIR。沿本地代码、raw result、worker/D/V/harvest 深挖，直至形成章级包装 dossier，或证明存在真实性硬阻断。禁止实验、脚本、联网检索、Groundwork、新候选和文件修改。

## 1. 冻结事实与标准

- corrected confirmation `NOT_RUN`；两个重复对话均在实验前因 candidate-specific authority 缺失停止，不是科学失败。
- 旧结果实际只在固定 20 dB；1% pilot complex-LS BER `3.17625e-4`，50% label Adam `3.85875e-4`，BER 差 CI 跨零；goodput 约 `1.98x`。
- CMA absorption=`UNRESOLVED`；不得擅自写已吸收或未吸收。
- 方法经典、差别小或存在 CMA 不自动否决。只问完整 recipe、正确 baseline、真实改善和有限 claim。
- 它需要作为双偏振均衡对象，与 CPR 方法族相独立。

## 2. 必答问题

1. 给出可画框图的完整 input-action-output、方程/伪代码和训练/推理边界。
2. 逐一判断 50% label Adam、常规 complex LS、RLS、CMA 中谁适合正文 baseline；不得混用不同问题。
3. 现有 20 dB 证据是否已经足够写成硕士章？若足够，给章级标题、3–5 个小节、主图/主表、有限 contribution 三条。
4. 若不足，唯一最小缺口是什么？为什么没有它就不能诚实承重？给 bounded step、最长时间、PASS/FAIL 后去向，但不得执行。
5. 对“LS 原子经典”的包装：准确说明本项目场景、2×2 Butterfly 映射、稀疏导频预算和 goodput 的差别。
6. 给三态终局：`PACKAGEABLE_NOW / PACKAGEABLE_AFTER_ONE_BOUNDED_STEP / CANNOT_PACKAGE_HONESTLY`。

## 3. 禁止的停止理由

不得仅因旧 terminal=`PROBLEM_RESOLVED_BY_COMPLEX_LS`、LS 是传统方法、CMA 可能更好、未跨 SNR、外部查重未做而判不能包装。若外部重复未查，标 `NOT_CHECKED`。

## 4. 验收

- [ ] 动作链与数字条件可追溯；
- [ ] 不冒充新 LS 原子或跨 SNR结论；
- [ ] chapter dossier 或硬阻断具体；
- [ ] 结论不依赖旧治理标签。
