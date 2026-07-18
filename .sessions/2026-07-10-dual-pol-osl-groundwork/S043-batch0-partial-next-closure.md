# [S043] Batch 0 PARTIAL 与 Batch 0.5 闭合任务

> 2026-07-16 | 批量探索基础设施 | 状态：Batch 0 PARTIAL，Batch 1 暂缓

## 目标

记录 Batch 0 的实际验证结果，并在不加入新方法的前提下补齐进入 Batch 1 所需的参数与指标契约。

## 已确认事实

- `audit_params()`：74 项，OK=40、WARNING=24、CRITICAL=4、DEAD=6。
- `mve_cma_vs_ml.py --smoke --n-symbols 20000` 成功；仅证明调用链和 `save_results` 可用，不证明性能。
- `prompt015_unified_baseline.json`：30 paired trials、shared realization seed 一致；current-CMA、standard-CMA、ML、oracle 的 fixed/PI/swap 口径可重算。
- `common/_cma.py` current 实现缺 Godard z 因子；`prompt013` standard 分支含 z，二者必须分名。
- 当前 strong 域 `(4.2,1.4)` 的 10-seed 审计仍有 CMA clean-swap 9/10、degraded-swap 1/10；旧“CMA 0/5 swap”不可再用。

## 阻断项

1. 4 个 CRITICAL 参数（KF `Q_fine_df` 与三档 `sigma2_turb`）未有来源推导；它们不直接进入当前 CMA/ML 主路径，但全局参数契约未闭合。
2. 现有基线没有统一 recovery-delay 字段；不能只用 BER/PI-BER 代替 fade 后恢复行为。
3. 旧 `r7_freeze_quantification.py` 存在 `SOP_RATE=1e-4` 等脚本级参数，需先做参数真相源审计，不能直接当 Batch 1 合法输入。

## Batch 0.5 任务

- 只审计并闭合 Batch 1 将用到的参数和 recovery-delay 定义；不修改算法、不新增方向。
- 对每个候选脚本检查参数是否来自 `params.py`、是否使用 shared realization、是否能输出统一事件指标。
- 若 CRITICAL 参数不进入 CMA/fade 路径，明确记录“路径外债务”，不得用它阻断所有探索；若进入，先停下做来源推导。

## 判定

当前 Batch 0 = **PARTIAL**；Batch 1 不是永久禁止，而是等待 Batch 0.5 完成上述闭合后再跑。所有现有数字标 provisional。

## 决策引用

- D045：候选族先地图，再批量排跑。
- S041：Batch 0–5 计划。

## 范围确认

- 本轮是否在 scope boundary 内：是。
