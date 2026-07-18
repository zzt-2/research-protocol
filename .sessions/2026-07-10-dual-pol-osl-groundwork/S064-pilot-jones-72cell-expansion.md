# [S064] Pilot Jones derotation 72-cell 扩展

> 2026-07-16 | E 族扩展验证 | 状态：进行中（待 V022 独立审查）

## 目标

按 S063 预注册验证 pilot Jones derotation 的跨 seed/rate/pilot-count 稳定性。

## 记录

结果 `pilot_derotation_grid_N100k_seeds41-48_rates4e-6_8e-6_1e-5.json`，72 cells；三个 rate checkpoint 均保留。每 pilot count 有 24 cells，其中 baseline failure=15、clean=9。

| pilots/block | overhead | failure改善 | clean退化 | 平均相对改善 |
|---|---:|---:|---:|---:|
| 2 | 3.125% | 11/15 | 1/9 | -817% |
| 4 | 6.25% | 14/15 | 0/9 | 82.0% |
| 6 | 9.375% | 15/15 | 0/9 | 89.37% |

2 pilots 最大 derotation BER .4086，淘汰。4 pilots 各 rate 改善2/3、5/5、7/7，最大 derotation BER约.0171。6 pilots各 rate改善3/3、5/5、7/7，最大约.01143。theta mean/P95平均：2p .0791/.2049、4p .0523/.1308、6p .0417/.1035 rad。

## 决策引用

- D052：扩展门槛为 failure改善≥50%、clean不退化、overhead≤10%。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

待 V022 对汇总算法、公平性、checkpoint 和门槛逐项审计。通过后6-pilot晋级正式GW，4-pilot作开销敏感性，2-pilot登记失败。
