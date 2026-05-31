# PROMPT-002: Ch3 信道估计 + 级联灵敏度推导

> 用途：新对话中完成 Ch3 的原创公式推导
> 前置：PROMPT-001 完成（需要 Ch2 的 $E[1/h^2]$ 发散性结论）
> 验证代码：`sim_prototype.py` + `sim_ch3_precomp.py` + `sim_cascade_robustness.py`

## 论文背景

Ch3 对比 LS/MMSE/Kalman/DL 四类估计方法，核心贡献是**级联灵敏度分析**：定量揭示估计精度对载波同步（鲁棒）和功率预补偿（脆弱）的截然不同的影响。

## Ch3 章节结构

```
3.2 湍流信道估计问题建模
3.3 信道估计方法（LS/MMSE/Kalman/DL）
3.4 估计精度对下游信号处理的影响分析
  3.4.1 估计误差对载波同步性能的影响
  3.4.2 估计误差对功率预补偿可行性的影响
  3.4.3 下游模块灵敏度差异分析
3.5 仿真结果
```

## 标准公式（直接引用）

LS/MMSE/Kalman 估计器标准公式见：`毕设/写作材料/formulas-ch3ch4-sync.md` Ch3 部分。

## 需要自己推导的公式

### 推导1：NMSE → BER 级联影响的数学框架（3.4.1 节）

**目的**：建立从信道估计误差（NMSE）到载波同步误码率（BER）的定量映射。这是本章核心创新之一。

**已知**：
- 信道估计：$\hat{h} = h + e$，其中 $e$ 为估计误差
- 载波同步中用 $\hat{h}$ 做 MMSE 补偿：$r \cdot \frac{\hat{h}^*}{|\hat{h}|^2 + 1/\bar\gamma}$
- 载波同步最终输出 BER

**要求**：
1. 推导估计误差 $e$ 通过 MMSE 补偿传播到等效 SNR 损失的解析表达式
2. 建立NMSE与等效SNR损失的关系
3. 推导NMSE与BER的关系曲线（理论预测）
4. 用 `sim_cascade_robustness.py` 的数据验证（Ch5 6/6 PASS @ NMSE=-10dB）

### 推导2：功率预补偿在估计噪声下失效的解析证明（3.4.2 节）

**目的**：严格证明为什么功率预补偿（$P_{tx} \propto 1/\hat{h}^2$）在存在估计噪声时完全崩溃。

**已知MVE结论**（需解析证明）：
- 纯预补偿：$\tau \geq 5$ms 时全面失效
- AR预测：完美信道信息下弱湍流 WEAK PASS
- 加入估计噪声后：AR预测增益归零，$\rho$ 估计从 0.99 崩到 0.7

**要求**：
1. 推导 $1/\hat{h}^2 = 1/(h+e)^2$ 的期望值，证明当 $e$ 非零时期望值发散或严重偏移
2. 分析 AR(1) 模型中，估计噪声如何通过 $\ln(\hat{h})$ 变换放大，破坏 $\rho$ 的估计
3. 给出"预补偿不可行"的数学结论，论证接收端处理（载波同步）是必要路径

### 推导3：下游模块灵敏度差异的统一定量框架（3.4.3 节）

**目的**：统一解释为什么载波同步对估计误差鲁棒、预补偿对估计误差敏感。

**要求**：
1. 分析两类方法对 $\hat{h}$ 的函数依赖：载波同步用 $\hat{h}^*/(|\hat{h}|^2+1/\bar\gamma)$（有正则化），预补偿用 $1/\hat{h}^2$（无正则化）
2. 用泰勒展开或灵敏度分析比较两者对 $e$ 的一阶/二阶灵敏度
3. 给出工程指导：估计器设计应满足什么精度就够用

## 验证要求

每个推导完成后：
1. **解析验证**：推导步骤正确性
2. **数值验证**：用 MVE 数据交叉验证
   - `sim_cascade_robustness.py` 的级联数据（NMSE vs BER）
   - `sim_ch3_precomp.py` 的预补偿失效数据
3. **一致性检查**：与 Ch2 的 $E[1/h^2]$ 发散结论衔接

验证用的 Python 环境：`~/.venvs/torch/bin/python`

## 输出

追加到：`毕设/写作材料/formulas-ch3ch4-sync.md` 的 Ch3 原创推导节。

## 必读文件

1. `毕设/写作材料/formulas-ch3ch4-sync.md` — 标准公式
2. `毕设/写作材料/formulas-ch2-system-model.md` — Ch2 推导结果（特别是 $E[1/h^2]$ 发散性）
3. `毕设/写作材料/symbol-conventions.md` — 符号表
4. `毕设/写作材料/thesis-framework.md` — Ch3 概述段
5. `projects/thesis-figures/simulation/sim_cascade_robustness.py` — 级联鲁棒性代码
6. `projects/thesis-figures/simulation/sim_ch3_precomp.py` — 预补偿代码
7. `.sessions/thesis-direction-pivot/S015-cascade-robustness-mve.md` — MVE 实验结论
8. `.sessions/thesis-direction-pivot/S013-ch3-mve-precomp.md` — 预补偿 MVE 结论
