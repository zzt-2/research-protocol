# PROMPT-013 研究报告：ML vs CMA 交换质量机制

## TL;DR

在 `N=5M`、SOP=`4e-7`、`f_G=30 Hz`、strong、20 dB 的冻结切片上，监督 ML 相对当前 scalar-error CMA 的交换后质量差异真实：30 个共享 seed 中 ML 的超额 PI-BER 逐 seed 30/30 更低，双侧精确 Wilcoxon `W=0, p=1.8626e-9`。但预注册机制验证没有支持“恒模目标天然留下残余”或“在线更新把映射推坏”：H_a 被证伪，H_b 严格判为 unknown 且 freeze 主效应 0/3 达标。更关键的是，补入输出因子 `z` 的 standard CMA 在两个高差 seed 上把 PI-BER 从约 `0.033/0.032` 降到约 `4.4e-5/4.7e-5`。因此当前证据只能说明 **ML 优于项目中的 scalar-error CMA 实现**，不能写成 ML 相对经典 CMA 的机制贡献。

## Q1：差异真实性（30 seeds）

30 个 seed（1000–1029）完整、无重复、无非有限数，所有方法共享同一 realization。PI-BER 均值为 CMA `0.0213144`、ML `0.00775071`、oracle `0.00659673`；相对 oracle 超额均值为 CMA `0.0147177`、ML `0.00115397`，相差 `12.75×`。配对结果为 ML/CMA/tie=`30/0/0`，达到预注册的 `p<0.05` 且 ML 胜场≥25/30，Q1 PASS。新增 holdout 20 seeds 仍为 20/20，`p=1.9073e-6`。

阈值分类仅作描述：clean≤0.05 时 CMA/ML 为 `25/5`、`29/1`（clean/degraded）；clean<0.01 时为 `20/10`、`25/5`。结论不依赖这两个硬阈值。PI-BER 仍需 pilot/帧头完成偏振流标识，不是免费恢复。

## Q2：机制

固定高差 seed 为 1006/1017/1011，低差 seed 为 1024/1028/1029；1004 作为极端离群事实保留，不进入机制组。

- **H_a（目标函数错位）：证伪。** Current CMA 的高/低组 NMSE 中位比仅 `1.984`、泄漏比 `0.999`，同时 `J_CM` 比 `4.189`、CM 梯度比 `1.791`，不满足“重构残差≥3×而两种 CM 信号≤1.5×”。Standard CMA 的 NMSE/泄漏比为 `0.874/0.797`，方向也不一致。
- **H_b（在线更新推坏映射）：严格 unknown，但有强否证证据。** 12 个 variant×seed 的 oracle Spearman 中 10 个因 oracle 窗口恒定而不可定义，按三态门控不能把缺失当支持。仅看冻结主阈值，current 与 standard 的高差组均 0/3 达标；current 最大绝对改善仅 `0.0054984`，低于预注册 `0.01`，其余近零或变差。
- **H_c（表达容量差异）：排除。** 两者均为 4 个 11-tap 复 FIR、88 个实自由度、无 bias/非线性。不过 ML 的 `wxy/wyx` 中心实际初始化为 1，而注释称 0，且 CMA 交叉支路为 0；这是未解除的训练路径混杂。

## 对主控决策的建议

不要把“ML 的 MSE 让交换更干净”或“固定权重优于在线 CMA”写成论文机制贡献，也不要把 Q1 的 30-seed 优势泛化为对经典 CMA 的胜出。若继续该方向，下一门控应先统一合法 baseline：修正/明确 standard CMA 与 ML 交叉支路初始化，再在相同 30 seeds 上比较 current CMA、standard CMA、ML；未完成前保持 GW Step 4a，不进 Contract。

## 产出路径

- Q1：`prompt013_swap_quality_q1.py`；结果 `results/cma-fade-divergence/prompt013_swap_quality.json`
- Q2：`prompt013_swap_mechanism_q2.py`；结果 `results/cma-fade-divergence/prompt013_swap_mechanism.json`
- 测试：`tests/test_prompt013_swap_quality_q1.py`、`tests/test_prompt013_swap_mechanism_q2.py`

独立验证：Q1/Q2/P12 long/short 共 60 passed，相关脚本 `py_compile` 通过。P12 divergence suite 因工作树中范围外的 `r_lcr_ber_impact.py` 已删除 `BLOCK/T_S` 导出而在 collection 阶段失败；该项不是 PROMPT-013 执行路径，未在本轮修复。
