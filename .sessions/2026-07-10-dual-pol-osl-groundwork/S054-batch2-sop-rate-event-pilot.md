# [S054] Batch2 SOP rate 事件侦察

> 2026-07-16 | Batch2 事件覆盖侦察 | 状态：PASS（observation-only）

## 目标

扫描 SOP rate，寻找真实 failure 事件域，并严格区分 BER tracking failure、lock-swap、fade 和 divergence。

## 记录

结果文件：`projects/simulation/results/cma-fade-divergence/batch2_sop_rate_event_pilot_seeds41-43_prefix_stable_v2.json`。

- rates `4e-7/1e-6/4e-6`：9/9 cells fixed=PI=0，无 swap/divergence/fade。
- rate `1e-5`：seed41 fixed=PI=0.00400128，221/1563 非零 BER windows，P99=0.078125、max=0.121094；seed43 fixed=PI=0.00608445，240/1563，P99=0.113281、max=0.152344；seed42 仍为 0。
- 12 cells 均 `first_swap=null`、swap windows=0、`diverged=false`、`fades=[]`。

独立审查 PASS：config SHA `cc511c18…` 一致，7 个 source SHA 一致，字段与 finite 检查通过。

## 决策引用

- D045：候选族按批次排跑。
- D047：把 `1e-5` 作为高速 SOP failure 侦察域，不称为 lock-swap Go（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

先做盲、因果的 failure detector/recovery 最小试验；必须保留 `4e-6` 无事件对照、oracle/post-hoc 上界和 baseline。若检测只依赖 genie 或无提前量，立即换 DFE/Kalman/接受式 H 族。
