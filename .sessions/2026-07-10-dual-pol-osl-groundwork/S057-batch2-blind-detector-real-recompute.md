# [S057] Batch2 盲 detector 真实短重算

> 2026-07-16 | Batch2 证据链复核 | 状态：进行中（待 V017 独立审查）

## 目标

将 evaluator 接入可复现的短序列 scout，避免旧 summary 缺 trace 造成不可审计结论。

## 记录

旧 scout summary 没有 trace，转换测试明确拒绝直接重算。新增 `recompute_blind_scout.py`，重新生成 N=100k、rates=`4e-6/1e-5`、seeds41–43 的短 scout；`blind_detector_evaluator.py` 负责 control-only P99、warmup=1 block、persistence、oracle 后验汇总。定向测试 4 passed。结果文件：`projects/simulation/results/cma-fade-divergence/batch2_blind_detector_recompute_short_real_warmup1.json`。

初步结果与原 scout 一致：1e-5 有 seed41/43 两个 oracle failure；三种基础盲信号 recall=0/2、lead=null；每种信号在 control 的 3 seeds 中各 1 个误报。

## 决策引用

- D048：evaluator provenance 修复后再决定换族。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

等待 V017。若审计 PASS，基础 detector 支线正式关闭，转 H/状态跟踪族；不再扩大该三种统计量。
