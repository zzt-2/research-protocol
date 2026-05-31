# 对话提示词：参数溯源MVE（替代PROMPT-010）

> 产出文件: projects/thesis-fso/mve-report.md + 仿真代码
> 优先级: 高（证明技术可行性的实证依据）
> 依赖: PROMPT-011（检索）+ PROMPT-012（A0+参数溯源）完成后执行
> 预计耗时: 半天

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，三章共用一套仿真系统。

**本MVE替代之前有缺陷的PROMPT-010**。PROMPT-010的致命问题是：参数全部无溯源，湍流参数α=20（极弱湍流）会导致"DL没用"的错误结论，星地参数缺失导致结论不可外推。

**本MVE的核心改进**：所有参数来自 `feasibility_report.md` 的参数溯源表，每个值都有文献来源。

## 框架要求

本MVE对应 `stages/gw-feasibility.md` 维度D（最小可行实验）。

**MVE必须包含**：
1. 假设：一句话描述要验证的核心假设
2. 最小实例：能测试假设的最小问题规模
3. [FR-04] 实例保真度检查：简化实例必须保留与核心假设相关的结构属性
4. pass/fail标准：预定义什么结果算通过
5. 时间预算：≤1天
6. [FR-11] MVE架构摘要

**本方向的MVE假设**：
- 核心假设：在Gamma-Gamma大气湍流信道下，传统信号处理方法（LS/MMSE估计、CMA/DFE均衡、VV载波恢复）可以端到端工作，且不同湍流强度下各方法性能有明显差异
- 如果假设不成立（如CMA在强湍流下不收敛、或三种方法性能无差异），需要调整方向

## 前置条件

读取 PROMPT-011 和 PROMPT-012 的产出：
- `projects/thesis-fso/literature_notes.md`
- `projects/thesis-fso/feasibility_report.md`（§参数溯源部分）

## 参数来源

**所有参数必须从 feasibility_report.md 的参数溯源表获取，不硬编码。**

如果 feasibility_report.md 中某个参数缺失，用以下策略：
1. 优先用 literature_notes.md 中提取的值
2. 如果还没有，用 `bash tools/search` 查一篇文献确认
3. 最后才用论文中的典型值，但必须标注 [外推]

### 必须确认的参数清单（在写代码前先确认）

| 参数 | feasibility_report中的值 | 来源论文 | 置信度 |
|------|------------------------|---------|--------|
| GG弱湍流(α,β) | ? | | |
| GG中湍流(α,β) | ? | | |
| GG强湍流(α,β) | ? | | |
| 波长 | ? | | |
| 链路距离 | ? | | |
| 符号速率 | ? | | |
| SNR范围 | ? | | |
| 符号数/SNR点 | ? | | |
| CMA抽头数 | ? | | |
| CMA步长 | ? | | |
| VV窗长 | ? | | |
| 激光线宽 | ? | | |

**任何一个参数缺失都不能开始编码。** 先补参数再写代码。

## MVE实验设计

### Step 0: 参数确认 + 环境搭建

```bash
cd /mnt/d/code/study/research-protocol
mkdir -p projects/thesis-fso/simulation
~/.venvs/torch/bin/python -c "import numpy, scipy; print('OK')"
# 检查OptiCommPy是否安装
~/.venvs/torch/bin/python -c "import optic; print('OK')" 2>/dev/null || echo "Need to install OptiCommPy"
```

### Step 1: GG信道模型

```python
def gg_channel(N, alpha, beta):
    """Gamma-Gamma湍流信道 — 乘积法（避免Bessel溢出）"""
    from scipy.stats import gamma
    X = gamma.rvs(alpha, scale=1.0/alpha, size=N)
    Y = gamma.rvs(beta, scale=1.0/beta, size=N)
    return X * Y
```

**验证**：
- 用参数溯源表中的弱/中/强三档参数
- 统计 h 的均值（应≈1）、方差（弱<0.05, 中~0.3, 强>1.0）
- 画 h 的时间序列和直方图
- **与文献对比**：如果弱湍流下 h 的方差与 Andrews & Phillips 表格不符，参数有误

### Step 2: QPSK信号生成 + GG信道传输

```python
def qpsk_mod(bits):
    """QPSK调制，归一化功率"""
    symbols = (2*bits[0::2]-1 + 1j*(2*bits[1::2]-1)) / np.sqrt(2)
    return symbols

def transmit(symbols, h, snr_db):
    """经GG信道传输，加AWGN"""
    # snr_db 是每符号SNR (Es/N0)
    noise_power = 1.0 / (10**(snr_db/10))
    noise = np.sqrt(noise_power/2) * (np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols)))
    return symbols * h + noise
```

**验证**：无信道处理时BER vs SNR（理论QPSK BER = Q(sqrt(2*SNR))）

### Step 3: Ch2 信道估计（LS + MMSE）

实现LS和MMSE估计器，用参数溯源表中的导频参数。

**验证**：
- 画 NMSE vs SNR 曲线（LS vs MMSE）
- 三档湍流下的估计误差对比
- **pass标准**：MMSE NMSE < -5dB at 20dB SNR（需确认这个阈值有文献依据）

### Step 4: Ch3 信道均衡（CMA）

用参数溯源表中的CMA抽头数和步长（不是21和0.001）。

**验证**：
- 均衡前后星座图对比
- 三档湍流下CMA收敛情况
- **关键pass标准**：CMA在强湍流下能否收敛？如果不能，记录失败现象
- **如果CMA不收敛**：这是重要发现，说明需要换均衡方法或参数

### Step 5: Ch4 载波恢复（VV）

用参数溯源表中的VV窗长和频偏参数。

```python
# 优先用OptiCommPy: from optic.dsp.carrierRecovery import viterbi
# 如果不可用则手写VV算法
```

**验证**：
- 加入残余频偏（多普勒预补偿后）+ 相位噪声（维纳过程）
- VV恢复前后的相位误差
- 三档湍流下VV性能
- **pass标准**：相位误差 < X度（X需从文献确认）

### Step 6: 端到端BER

```python
# 三条曲线：
# 1. AWGN only（基线）
# 2. GG湍流 + 无处理
# 3. GG湍流 + 估计 + 均衡 + 载波恢复
```

**pass标准**：处理后比无处理 BER 改善 ≥5dB。

### Step 7: 湍流强度 × 方法 性能矩阵

这是最重要的输出——**不同湍流强度下各方法的性能差异**。

| 湍流 | SNR@BER=10^{-3}(无处理) | SNR@BER=10^{-3}(+LS+CMA+VV) | SNR@BER=10^{-3}(+MMSE+DFE+VV) | 改善 |
|------|------------------------|----------------------------|-------------------------------|------|
| 弱 | ?dB | ?dB | ?dB | ?dB |
| 中 | ?dB | ?dB | ?dB | ?dB |
| 强 | ?dB | ?dB | ?dB | ?dB |

**如果三种方法在所有湍流下性能相同 → 创新点"方法对比"不成立，需调整方向**

## MVE架构摘要 [FR-11]

```markdown
### MVE 架构摘要
- 系统模型: 相干检测 + QPSK + GG大气湍流信道
- 信道模型: Gamma-Gamma乘积法, 参数来自[论文X]
- 估计方法: LS / MMSE (导频辅助)
- 均衡方法: CMA (盲均衡), 参数来自[论文Y]
- 载波恢复: Viterbi-Viterbi, 参数来自[论文Z]
- 对比范式: 相同信道条件下不同方法组合的BER vs SNR
- 链路参数: λ=XXXnm, L=XXXkm, Rs=XXXGbps (来自[论文W])
- 先验对照: 无处理BER vs 处理后BER, 比值=XX
- 已知简化偏差: 无自适应光学/无分集/无编码/无定时同步(假设理想)
```

## 产出格式

### 代码

放在 `projects/thesis-fso/simulation/` 下：
- `channel.py` — GG信道模型
- `modem.py` — QPSK调制解调
- `estimation.py` — LS/MMSE信道估计
- `equalization.py` — CMA均衡
- `carrier.py` — VV载波恢复
- `mve_main.py` — 主程序（端到端运行）
- `figures/` — 输出图片（PDF格式）

### 报告

```markdown
# MVE报告 — 星地激光通信信号处理

## 参数溯源
[每个参数的值和来源]

## 实验结果

### Step 1: GG信道模型验证
[统计量 + 图]

### Step 2: QPSK+GG基线BER
[图 + 与理论值对比]

### Step 3: Ch2信道估计
[NMSE vs SNR 图]

### Step 4: Ch3 CMA均衡
[星座图 + 收敛曲线]

### Step 5: Ch4 VV载波恢复
[相位误差图]

### Step 6: 端到端BER
[三条BER曲线]

### Step 7: 湍流×方法矩阵
[性能矩阵表]

## 失败记录
[任何步骤的失败现象、错误信息、分析]

## MVE架构摘要 [FR-11]
[按上述格式]

## 结论
1. 三章技术路线是否端到端可行？
2. CMA在强GG湍流下是否收敛？
3. 不同方法在不同湍流下是否有性能差异？
4. 如果有失败，推荐的调整方向是什么？
```

## 约束

- **所有参数从 feasibility_report.md 获取**，不硬编码
- Python环境：`~/.venvs/torch/bin/python`
- 代码写在 `projects/thesis-fso/simulation/` 下
- 图保存为PDF格式
- **不要追求完美，能跑通就行**——这是可行性验证
- 如果某步骤失败，详细记录失败现象（比成功更有价值）
- 产出文件：`projects/thesis-fso/mve-report.md`
- 如果OptiCommPy没安装，VV手写（~30行）
- **不要跳过Step 0参数确认**——缺参数就先补参数再写代码
