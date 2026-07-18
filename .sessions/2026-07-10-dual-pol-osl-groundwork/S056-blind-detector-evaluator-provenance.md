# [S056] 盲 detector evaluator 可复现性补齐

> 2026-07-16 | 证据链修复 | 状态：进行中（待 V016 独立审查）

## 目标

修复 V015 指出的 evaluator 未入源码/SHA 债务，不扩展长实验。

## 记录

新增 `projects/simulation/explore/cma-fade-divergence/blind_detector_evaluator.py` 与 `projects/simulation/tests/test_blind_detector_evaluator.py`。源码明确 control-only quantile calibration、warmup 排除、连续 persistence、oracle 仅 post-hoc 匹配，以及 recall/lead/false-alarm 汇总。定向 TDD 2 tests passed。synthetic smoke `projects/simulation/results/cma-fade-divergence/blind_detector_evaluator_smoke.json` 含 source SHA 与 warmup=0/1 对照；尚未重跑长 scout，因此 S055 的 FAIL 不被改写。

## 决策引用

- D048：先补 evaluator provenance，再决定重跑或换族。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

等待 V016；若源码审计 PASS，再用固定 evaluator 重算短 scout。若 recall 仍为 0，停止基础统计量 detector，转 H/状态跟踪族。
