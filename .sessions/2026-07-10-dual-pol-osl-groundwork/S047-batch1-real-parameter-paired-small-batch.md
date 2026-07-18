# [S047] Batch 1 真实参数 paired small batch

> 2026-07-16 | Batch 1 参数冻结与执行 | PASS（small-batch contract only）

## 目标

用 pilot 已观察到的真实分布冻结首个小批参数，比较 standard-CMA baseline、fade-freeze、gradient-clip(P99/P95) 四个单轴臂；只做 paired 诊断，不据此宣称性能 Go/Kill。

## 记录

Pilot（N=100k、seeds 41/42/43、strong α=4.2/β=1.4、f_G=30、SOP=4e-7、standard Godard-z、block=64）显示：4686 个 h block 中 `h<0.1` 为 0；update norm pooled P50=`2.41157e-4`、P95=`5.86987e-4`、P99=`2.37826e-3`、max=`4.15647e-3`。因此：

- freeze threshold 冻结为 `0.1`，预期在真实 pilot 域不触发；若小批触发，先查 realization/口径，不直接解释为收益。
- clip 主臂阈值冻结为 P99=`0.002378256`；clip 敏感性臂为 P95=`0.000586987`。选择理由是分别约影响 pooled 更新的 1% 和 5%，来自 pilot 分布而非拍参。
- paired seeds：41–45，N=`100000`；四臂共享每 seed 的 canonical realization 和 valid mask。

预注册观察项：机制触发计数、divergence、first swap、recovery/censor、fixed/PI BER。退出条件：任一方法输出契约/共同 mask/事件 schema 失败，或出现未解释的非 finite；触发则停，不比较性能。

## 决策引用

- D045：候选族先地图，再批量排跑。
- 无新性能决策；本文件只冻结小批参数与观察项。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

5 paired seeds 已完成，独立 verifier 对 schema/provenance/finite/valid mask/机制计数审计 PASS；但该批生成于 D046 RNG 修复之前，数值观察全部标 stale，仅保留 schema/管线证据，不能作物理或性能结论。修复后需重跑同一配置再决定是否扩大正式统计批或截断某单轴。
