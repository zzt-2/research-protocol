# Ch5 单格 target-residual occurrence

> T066 / D047 / V021 | GW Step 4a 维度 D | 2026-08-30

## 事实与裁决

- terminal：`DETECTABLE_OCCURRENCE`。
- 完整窗口：`64/64`；calibration=`0..31`，evaluation=`32..63`。
- bounded development：`允许`。
- 本格只判断自然 residual covariance occurrence，不包含 BER/GMI/FER、LDPC 或 C5-1 方法结论。

## D1/D2 simultaneous 95% window-cluster bootstrap CI

| group | samples | D1 estimate | D1 CI | D2 estimate | D2 CI |
|---|---:|---:|---|---:|---|
| pol0_inner | 1024 | 0.159268116 | [-0.046740002, 0.31491229] | -0.0261500857 | [-0.182638477, 0.149764681] |
| pol0_outer | 1024 | 0.75183289 | [0.408545634, 0.975701079] | -0.0894258598 | [-0.138043608, -0.0246987521] |
| pol1_inner | 1024 | 0.351314193 | [-0.0568549735, 0.570375089] | -0.0243395961 | [-0.146300108, 0.0808521083] |
| pol1_outer | 1024 | 0.632659524 | [0.296053666, 0.819383221] | 0.220856478 | [0.020269989, 0.344052572] |

每个 evaluation window 每组样本数：`32`。

### Evaluation point counts（按 group）

- pol0_inner point_counts：`[128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0]`
- pol0_outer point_counts：`[0, 0, 0, 0, 0, 0, 0, 0, 128, 128, 128, 128, 128, 128, 128, 128]`
- pol1_inner point_counts：`[128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0]`
- pol1_outer point_counts：`[0, 0, 0, 0, 0, 0, 0, 0, 128, 128, 128, 128, 128, 128, 128, 128]`

逐 window residual、realization/bundle hash 见 raw/aggregate JSON。

## D3 held-out covariance NLL

- `NLL_B1-NLL_full` mean：`0.0870608267`。
- 普通 95% evaluation-window cluster CI：`[0.0642673878, 0.111283003]`。
- covariance 仅由 calibration windows 拟合；evaluation residual 不参与拟合、阈值或分支选择；统一 floor=`1e-10`。

## Bootstrap 与 provenance

- PCG64 seed=`2026083001`，resamples=`2000`，cluster=`evaluation_window`（32 个）。
- manifest hash：`561a828b2480aed9bde8c9101302f8e67076857c2f0928250bc7d437a4117ec1`。
- frozen config hash：`6f57c57b865561ce4703377237a106fb9d07e542aa3864727c4f14c26339d256`。
- unique realization/bundle hashes：`64/64`。

## 唯一下一步

`Main controller may dispatch C5-1 bounded development.`
