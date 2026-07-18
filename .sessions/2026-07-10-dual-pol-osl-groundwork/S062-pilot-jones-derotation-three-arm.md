# [S062] Pilot-informed Jones derotation 三臂短跑

> 2026-07-16 | E 族方法短跑 | 状态：进行中（待 V021 独立审查）

## 目标

让 pilot-derived 2×2 Jones estimate 真正作用于 data，并与 baseline、naive pilot 注入做同 realization 三臂消融。

## 记录

新增 `pilot_integration_runner.py` 与测试；相关定向 tests 4 passed。runner 保存 same-realization fingerprint、shared data mask、`observation_only=true`。`derotate_data_with_estimates` 每 block 对 4-pilot LS Jones matrix 取 pinv，只作用 data，pilot 位置不参与 BER。

结果 `pilot_jones_derotation_three_arm_N100k_rate1e-5_seeds41-43.json`：

| seed | baseline fixed | naive pilot | pilot derotation |
|---|---:|---:|---:|
| 41 | .0039853 | .0043027 | 0 |
| 42 | 0 | 0 | 0 |
| 43 | .0061060 | .0064901 | 0 |

PI 与 fixed 一致；三臂无 divergence。naive pilot 未改善而 derotation 清零，初步支持增益来自 Jones estimate 被消费，不是插入 pilot 本身。

## 决策引用

- D051：pilot-assisted 最小候选。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

待 V021；通过后扩新 seeds/邻近 rate，并加入无噪声/估计误差/开销敏感性。当前不作 Go。
