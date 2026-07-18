# [S058] Batch2 接收端几何特征侦察

> 2026-07-16 | Batch2 候选筛选 | 状态：进行中（待 V018 独立审查）

## 目标

在不使用 TX、信道真值或 post-hoc assignment 的前提下，测试接收端 `rX/rY` 几何特征是否能提前识别高速 SOP failure。

## 记录

代码 `geometry_feature_scout.py` 仅从 `rX/rY` 计算 cross-correlation magnitude、covariance eigenvalue ratio、Stokes-like ratio；TDD 1 passed。结果文件：`batch2_geometry_feature_scout_sop4e-6-vs1e-5_seeds41-43_prefix_stable_v2.json`，rates=`4e-6/1e-5`、seeds41–43、warmup=1、persistence=2、control-only P99。

- cross-correlation：recall 0/2，control false alarm 0/3。
- covariance eigen ratio：recall 1/2，lead=487 blocks，control false alarm 1/3。
- Stokes-like ratio：recall 2/2，lead=351/604 blocks，control false alarm 0/3。

## 决策引用

- D049：基础统计量关闭，转接收端几何特征。
- D050：暂保留 Stokes-like 进入短 pilot（待 V018 后新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

仅 Stokes-like 进入短 pilot/因果性复核；其余两特征不扩展。仍不进入 recovery 性能 Go。
