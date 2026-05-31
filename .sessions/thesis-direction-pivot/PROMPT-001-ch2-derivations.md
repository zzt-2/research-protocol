# PROMPT-001: Ch2 系统与信道模型公式推导

> 用途：新对话中完成 Ch2 所有原创/需要自己推导的公式
> 前置：无（基础章）
> 验证代码：`projects/thesis-figures/simulation/sim_prototype.py`

## 论文背景

硕士论文《星地激光通信信号处理关键技术研究》，QPSK相干检测，Gamma-Gamma大气湍流信道，LEO星地链路。

Ch2 是基础建模章，为后续章节提供统一的模型和参数体系。

## Ch2 章节结构

```
2.2 星地激光通信系统模型
  2.2.1 相干检测系统组成
  2.2.2 QPSK信号模型
  2.2.3 接收端噪声模型与信噪比定义
2.3 大气信道传输特性
  2.3.1 大气衰减
  2.3.2 大气湍流效应与Gamma-Gamma分布模型
  2.3.3 Gamma-Gamma模型参数确定
2.4 星地链路预算分析
2.5 本章小结
```

## 标准公式（直接引用，不需推导）

这些是教科书/经典论文公式，直接引用原始出处即可：
- QPSK 信号模型、相干混频、I/Q 输出
- Beer-Lambert 大气衰减
- Kolmogorov 2/3 定律、Rytov 方差公式
- Gamma-Gamma 分布 PDF
- Hufnagel-Valley Cn² 剖面模型
- 自由空间损耗公式

标准公式的 LaTeX 写法和引用来源见：`毕设/写作材料/formulas-ch2-system-model.md`

## 需要自己推导的公式

### 推导1：GG 分布下 $E[1/h^2]$ 的发散性分析（2.3.2 节核心结论）

**目的**：证明在 Gamma-Gamma 分布下，当湍流强度达到中强时，$E[1/h^2]$ 发散。这是 Ch4 湍流自适应机制的**理论必然性基础**——如果这个矩发散，固定参数 VV 算法的方差就是无穷大，自适应参数就是必须的。

**要求**：
1. 从 GG 分布 PDF 出发，写出 $E[1/h^2] = \int_0^\infty h^{-2} f(h) dh$ 的积分表达式
2. 分析积分收敛条件（与 $\alpha, \beta$ 参数的关系）
3. 给出弱/中/强湍流下是否发散的具体判断（用我们论文的湍流参数：弱 $\alpha=4.0, \beta=3.0$；中 $\alpha=2.5, \beta=1.8$；强 $\alpha=1.5, \beta=0.8$）
4. 用数值积分验证（Python 代码，与 MVE 参数一致）

**输出格式**：论文风格的推导段落，带公式编号（从式(2.X)开始），每步有文字解释。

### 推导2：星地链路预算闭合公式（2.4 节）

**目的**：建立从发射功率到接收端 SNR 的完整公式链，给出典型 LEO 参数下的数值结果。

**要求**：
1. 推导端到端 SNR：$\gamma = P_t \cdot G_t \cdot G_r \cdot (\lambda/4\pi d)^2 \cdot h_{atm} \cdot |h_{turb}|^2 / (N_0 \cdot B)$
2. 代入典型参数（1550nm, LEO 500km, 仰角 30°-90°, 发射孔径, 接收孔径, 大气衰减系数）
3. 给出不同仰角和湍流下的 SNR 范围表
4. 与 MVE 代码中的参数交叉验证

**参数来源**：
- 参考论文参数：`毕设/写作材料/formulas-ch2-system-model.md` 末尾的参数表
- MVE 代码参数：`projects/thesis-figures/simulation/sim_prototype.py` 中硬编码的值
- 参考论文：Fernandes 2023 (`papers/doi/10.1109_jlt.2023.3281082/content.md`) 和 Nguyen 2024

## 验证要求

每个推导完成后：
1. **解析验证**：检查推导步骤的数学正确性
2. **数值验证**：用 Python 计算具体数值，与 MVE 仿真结果比对
3. **文献交叉验证**：与参考论文中的结论对比（如 Fernandes 2023 的 SNR 范围是否一致）

验证用的 Python 环境：`~/.venvs/torch/bin/python`

## 输出

将推导结果追加到：`毕设/写作材料/formulas-ch2-system-model.md` 的"原创推导"节。

## 必读文件

1. `毕设/写作材料/formulas-ch2-system-model.md` — 标准公式清单和参数表
2. `毕设/写作材料/symbol-conventions.md` — 统一符号表
3. `毕设/写作材料/thesis-framework.md` — Ch2 概述段（了解整体叙事）
4. `projects/thesis-figures/simulation/sim_prototype.py` — MVE 仿真代码（参数和模型实现）
