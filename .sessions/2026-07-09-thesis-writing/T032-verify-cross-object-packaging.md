# [T032] 跨对象章级包装独立终验

> 来源: S024 | 回传给主线程
> 日期: 2026-08-13

## 0. TL;DR

只读核验 R026 是否忠实、保守地综合 P11/P05/P08-R2 深挖回传，特别检查三项 `PACKAGEABLE_NOW_WITH_LIMITS` 是否违反真实性底线。禁止修改文件、实验、脚本、联网、Groundwork和新候选。

## 1. 必查

1. 三项正式动作链和 baseline 是否准确；
2. P11 是否只写 fixed-20dB/X-output/runner-defined BER/goodput proxy，保持 CMA unresolved；
3. P05 是否明确独立 CMA receiver、15-epoch frozen FIR baseline、fixed-label而非 PI-BER增益；
4. P08-R2 是否只把 alpha/offset 当新增动作，不把 prefix/clip冒充增益；
5. “无需补实验即可有限包装”是否只基于现有有限命题真实公平，而非放弃真实性；
6. CPR＋均衡＋coded receiver 的跨对象分组是否合理；
7. 是否仍保持执行暂停与 exact duplicate NOT_CHECKED。

## 2. 返回

给 PASS/PARTIAL/FAIL、七项逐条结论和 P0/P1/P2；不要提供新研究方向。
