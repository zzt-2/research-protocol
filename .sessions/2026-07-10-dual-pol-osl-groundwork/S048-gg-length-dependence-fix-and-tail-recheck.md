# [S048] GG 生成器长度依赖修复与 tail 复核

> 2026-07-16 | Batch 1 前置诊断 | PASS（修复/诊断；freeze 仍 DEFER）

## 目标

解释 100k 与 5M pilot 同 seed 前缀不一致，修复根因后重做 h-tail 观察，避免把生成器伪影当作 fade 机制证据。

## 记录

失败测试先复现：同 seed、同参数下 `gg_time_envelope(100000)` 与 `gg_time_envelope(5000000)[:100000]` 全部不一致，最大差约 0.149。追踪 `_gg_time.py` 后确认：同一 RNG 先抽完整 big AR 序列，再抽 small AR 序列；N 改变会改变 small 流起点。

修复：big/small 改用 `SeedSequence(seed).spawn(2)` 的独立子流。前缀测试 GREEN；相关回归 `103 passed in 21.36s`。

修复后 5M h-tail pilot（seeds41–43）通过独立审计：N100k→5M 前缀 exact（max diff=0）；CMA64 pooled 234375 blocks、channel100 pooled 150000 blocks，`h<0.1` 均为 0、segments=0，min=`0.260929867`，P1=`0.3348275`，P5=`0.4497675`，P50=`0.9841192`。配置/source SHA 均可重算。

因此旧未修复的“54.14% low-h”数字作废；freeze threshold=0.1 在当前域列低信息/DEFER，而非性能 KILL。clip 候选保留。

## 决策引用

- D046：修复长度依赖并暂缓 freeze。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

优先扩大 clip 单轴 paired 批，或在进入 freeze 性能实验前先选择能产生真实 `h<0.1` 的参数条件并单独做事件语义验证。
