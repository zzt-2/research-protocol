# [T031] 深挖 P08-R2 编码 FSO 接收方法

> 来源: S024 | 回传给主线程
> 日期: 2026-08-13

## 0. TL;DR

只审 P08-R2：receiver-visible prefix residual calibration、MMSE/LLR 与冻结 decoder tuning 的 coded-FSO receiver。追到章级包装或真实性硬阻断。禁止实验、脚本、联网检索、Groundwork、新候选和文件修改。

## 1. 冻结事实与标准

- corrected B0 已包含 32-symbol prefix residual calibration；B2 相对 B0 的实际新增是冻结 LLR clipping 与 normalized offset-min-sum 参数。
- 单一 weak/1000 Hz/12 dB slice：FER `0.1546875→0.1484375`；oracle O2 `0.1390625`；B0−B2 CI 为正但效应小于旧 MDE。
- hidden gamma 已通过 metamorphic gate 排除；相同 X/Y prefix 使完整 2×2 channel identification 说法不成立。
- chronology 不是 pristine confirmation；O2 使用 payload truth，只能作 oracle。
- 小增益、经典 prefix-LS/decoder tuning 不自动否决；但不得把 B2 增益归因于 prefix-LS 单独作用。
- 它需要作为 coded receiver 技术对象，与 CPR 和均衡方法族相独立。

## 2. 必答问题

1. 从源码还原 corrected B0/B2 的完整 receiver chain、输入输出和真正新增动作。
2. 找出最合适的经典 baseline 以及 B2 相对它的真实改善命题。
3. 判断单 slice、小 FER delta、chronology debt 是否仍足够硕士级章节；不要沿用旧 MDE 自动 Kill。
4. 若可包装，给章标题、3–5 小节、框图、主图/主表、三条有限 contribution 与限制。
5. 若不足，唯一最小补证是什么、最长多久、PASS/FAIL 后如何处理；不得执行。
6. 给三态终局：`PACKAGEABLE_NOW / PACKAGEABLE_AFTER_ONE_BOUNDED_STEP / CANNOT_PACKAGE_HONESTLY`。

## 3. 禁止的停止理由

不得仅因动作是参数调优、效果小于旧 MDE、oracle 更强、旧 terminal=`EVIDENCE_INSUFFICIENT` 或外部查重未做而停止。硬阻断必须落在真实性、动作链、正确 baseline 或真实改善缺失上。

## 4. 验收

- [ ] B0 已含 prefix calibration 的事实不混淆；
- [ ] B2 增益归因正确；
- [ ] receiver-visible/oracle 边界清楚；
- [ ] chapter dossier 或硬阻断具体。
