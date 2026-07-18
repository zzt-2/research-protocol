# [S052] Clip 压力域 1M fallback batch

> 2026-07-16 | Batch 1 压力筛选 | PASS（fallback observation only）

## 目标

在 N=5M 受环境内存限制无法完成的情况下，明确降级为 N=1M 的可运行压力批；不把它冒充 S051 的 5M 替代，也不直接作最终性能 Go/Kill。

## 记录

S051 的低内存 runner 已通过小 N 对照，保证逐臂重生成同 seed、fingerprint 一致、评估后释放；但 N=5M 三臂执行仍在约 30s/内存限制前被杀。seed41 单臂 baseline/P95/P99 均 valid=4,999,936、BER=0、无 divergence，P95 clip=1547 blocks、P99=0；这只是 partial。

本 fallback 固定 μ=1e-2、N=1,000,000、seeds41–45、baseline/clip-P95/clip-P99，使用 prefix-stable generator 和 sequential runner。结果标签必须写 `fallback_N=1000000`，不能与 5M 结果混合。

## 决策引用

- D046：prefix-stable GG generator。
- S051：5M 受环境阻塞，未降 N 静默继续。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

独立审计已通过：5 seeds唯一、三臂 schema/source/config SHA/finite 全部通过；所有 BER=0、无 divergence/swap/fade，P95/P99 仅机制触发不同。判为 observation-only/inconclusive，不冒充 5M；下一步需真正流式 5M 或换 stress 条件。
