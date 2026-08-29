# Ch5 structured-covariance 有界 BER/GMI 开发

> T067 / D048 / V022 | `PROVISIONAL` ceiling | Groundwork Step 4a dimension D

## 事实与数字

- Round 1：`64/64` windows；tune `0..31`，evaluation `32..63`。
- 调参冻结：C1 `kappa=64.0`；B3 `shrinkage=1.0`。
- terminal：`NO_METHOD_SIGNAL`；strongest structured comparator：`B2`。
- Round 2 authorized：`false`；provisional grade：`D`。

### Evaluation arms（32 window clusters）

| arm | mean GMI | mean BER | errors / bits | held-out NLL | max condition | floor rate | runtime (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| B1 | 2.8071407007 | 1.0335286458e-01 | 5080 / 49152 | 2.2522531684 | 1 | 0 | 0.366506 |
| B2 | 2.8055749299 | 1.0300699870e-01 | 5063 / 49152 | 2.3464706648 | 24.0451 | 0 | 0.364884 |
| B3 | 2.5267912891 | 1.0784912109e-01 | 5301 / 49152 | 1.6284560821 | 1 | 0 | 0.352010 |
| C1 | 2.8044384292 | 1.0306803385e-01 | 5066 / 49152 | 2.2157285735 | 34.8099 | 0 | 0.366895 |

### Paired differences（candidate − baseline）

- `B2_vs_B1`：GMI Δ=-0.0015657708, 95% CI [-0.0143401862, 0.0111921078], wins=15/32；BER Δ=-3.4586588542e-04, 95% CI [-1.4246622721e-03, 6.1035156250e-04], wins=11/32。
- `B3_vs_B1`：GMI Δ=-0.2803494116, 95% CI [-0.3949681426, -0.1836614962], wins=1/32；BER Δ=4.4962565104e-03, 95% CI [7.5225830078e-04, 8.1385294596e-03], wins=8/32。
- `C1_vs_B1`：GMI Δ=-0.0027022715, 95% CI [-0.0143139940, 0.0083123623], wins=12/32；BER Δ=-2.8483072917e-04, 95% CI [-1.5055338542e-03, 8.1380208333e-04], wins=12/32。
- `C1_vs_B2`：GMI Δ=-0.0011365007, 95% CI [-0.0073790939, 0.0037069830], wins=15/32；BER Δ=6.1035156250e-05, 95% CI [-4.0690104167e-04, 5.2897135417e-04], wins=9/32。
- `C1_vs_B3`：GMI Δ=0.2776471401, 95% CI [0.1797075733, 0.3933846864], wins=31/32；BER Δ=-4.7810872396e-03, 95% CI [-8.4838867188e-03, -1.2207031250e-03], wins=25/32。

## 实现真相三联卡

- `information_access`：bridge/estimator 只读本 window known pilots、接收 observation、冻结 constellation/arm/config；payload labels/bits 仅在离线 BER/GMI/NLL scorer 中消费。
- `metric_signature`：每 evaluation window 含 2 polarizations × 192 payload symbols × 4 bits；BER 分子为 hard-LLR bit errors、分母为 1536；GMI 使用同一 payload bits/LLR；聚合单位与 bootstrap cluster 均为 window。
- `state_lifecycle`：每 seed 独立 window；同 window 的 Ch4 preamble + observation 共用连续 scalar→Jones→AWGN realization；Ch4/Ch3 state 每 window 重置，不跨 window 或 polarization pooling。

## 裁决

`NO_METHOD_SIGNAL`。本结果等级上限为 `D`，不是 FINAL，也不是 confirmation。

唯一下一步：Close C5-1 and return to C5-0 Groundwork Step 2.

## 禁止边界

未运行 LDPC/FER grid、第二湍流级、新损伤、第三轮、扩展参数/SNR/seeds、fresh confirmation；未修改 common/、params.py、Skill/controller 或论文正文。
