# [T030] 深挖 P05 固定流标签在线 CMA 均衡

> 来源: S024 | 回传给主线程
> 日期: 2026-08-13

## 0. TL;DR

只审 P05：强 GG/SOP 双偏振 FSO 中，独立在线 standard CMA receiver 相对 frozen supervised Butterfly equalizer 维持固定流标签。追到章级包装或真实性硬阻断。禁止实验、脚本、联网检索、Groundwork、新候选和文件修改。

## 1. 冻结事实与标准

- 旧名 `Online-CMA-Continued Butterfly Equalizer` 错误；实现没有加载、串接或继续更新 Butterfly 权重。
- 实际是从原始 RX 独立运行 Godard-with-z CMA；fixed-label BER 约 `0.4992→1.76e-4/1.17e-3`，PI-BER无稳定优势。
- 现有两 cell 均为 20 dB，每格 3 paired seeds；15/20 epoch identity、Phase A/B seed复用和 JSON `mean_pi` 字段误名必须披露。
- CMA 经典不自动否决；但不得把“标准 CMA 在该场景胜 frozen ML”冒充新 CMA 原子。
- 它需要作为双偏振均衡对象，与 CPR 方法族相独立。

## 2. 必答问题

1. 能否形成一个真实的方法章问题：固定流标签连续性为何是接收机目标，为什么 PI-BER 会掩盖 swap？
2. 给完整 input-action-output、更新方程、baseline 契约与公平性账本。
3. 判断贡献究竟是“场景迁移方法”“接收机替换方法”还是仅“baseline/负面分析”；只能按实际动作链命名。
4. 若可包装，给章标题、3–5 小节、框图、主图/主表、三条有限 contribution 和必须披露的限制。
5. 若不足，唯一最小补证是什么、最长多久、PASS/FAIL 后如何处理；不得执行。
6. 给三态终局：`PACKAGEABLE_NOW / PACKAGEABLE_AFTER_ONE_BOUNDED_STEP / CANNOT_PACKAGE_HONESTLY`。

## 3. 禁止的停止理由

不得仅因 CMA 传统、旧 terminal=`PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`、存在更强方法或外部查重未做而停止。真正硬阻断只能来自实际动作不存在、baseline 不公平、结果 artifact、truth leakage 或无法形成诚实改善命题。

## 4. 验收

- [ ] 不再称 continuation；
- [ ] fixed-label 与 PI-BER 身份清楚；
- [ ] 方法章结构具体；
- [ ] 结论不依赖旧治理标签。
