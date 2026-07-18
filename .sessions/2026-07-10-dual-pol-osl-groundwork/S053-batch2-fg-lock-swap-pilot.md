# [S053] Batch2 fG lock/swap 事件侦察

> 2026-07-16 | Batch2 事件覆盖侦察 | 状态：PASS（observation-only）

## 目标

在修复后的 canonical generator 上，扫描 fG=30/100/1000，确认当前参数域是否能产生 lock/swap 事件。

## 记录

`batch2_lock_swap_event_pilot_seeds41-43_fg30-100-1000_prefix_stable_v2.json` 完成 9 cells（3 fG×3 seeds，N=100k，standard prompt013，μ=1e-3）。每 cell 1563 windows、99968 valid samples；config/source SHA 已独立重算。全 9 cells fixed=PI=0、swap assignment windows=0、first_swap=null、diverged=false、fades=[]。

## 决策引用

- D045：候选族按批次排跑。
- D047：本批无事件，转高速 SOP failure 侦察（后续批次新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

fG 轴在当前短批无事件覆盖，不作 lock/swap Go；不继续在该轴盲目扩展，保留为无事件对照。
