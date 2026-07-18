# [S059] Batch2 Stokes-like 短 pilot

> 2026-07-16 | Batch2 候选复核 | 状态：PARTIAL（阈值前提失效，停止该支线）

## 目标

验证 Stokes-like ratio 是否跨 seed、跨 SOP rate 稳定，并满足 control-only 校准与误报门槛。

## 记录

结果 `batch2_stokes_short_pilot_rates4e-6_8e-6_1e-5_seeds41-48_prefix_stable_v2.json`：18 cells（3 rates×6 seeds），geometry tests 2 passed，config/source SHA 和 finite 审计通过。control rate `4e-6` 的 seed47 在 block0、seed48 在 block325 已有 oracle events，control-only 阈值前提被破坏。Stokes raw recall=0.2、false alarm=3/6；covariance recall=0.3、false alarm=2/6。按预注册条件停止，不进入 recovery 长跑。

## 决策引用

- D050：Stokes-like 只获准短 pilot，非性能 Go。
- D051：control 污染且跨 seed 不稳定，回到 E pilot-assisted/H 候选族。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

保留 observation，不挑 seed 重包装；优先盘点 E 稀疏 pilot-assisted SOP/Jones 估计，H 仅作 oracle 事件标注。
