# 对话提示词：最小仿真原型 — 端到端验证

> 产出文件: R010-simulation-prototype.md
> 优先级: 高（证明技术可行性）
> 注意：此对话在验证对话(PROMPT-008/009)完成后再开

## 背景

硕士论文"星地激光通信信号处理关键技术研究"，三章共用一套仿真系统。

**已确认的统一仿真方案**：
- 平台：Python（NumPy/SciPy/OptiCommPy/PyTorch）
- 系统模型：相干检测 + QPSK调制 + Gamma-Gamma大气湍流信道
- 学生本科代码：完整相干检测MATLAB仿真（PLL载波同步、Gardner定时、CMA均衡），可参考逻辑
- 最大缺口：GG大气湍流信道模型（约20行）

**目标**：用最短时间跑通一条完整信号链，证明三章的技术路线都可行。

## 仿真任务

### Step 1: GG信道模型（~20行）

```python
# Gamma-Gamma大气湍流信道模型
# 参数：alpha (弱湍流~20, 强湍流~2), beta
# 方法：乘积法避免Bessel函数溢出
import numpy as np
from scipy.stats import gamma

def gg_channel(N, alpha, beta):
    """Gamma-Gamma湍流信道衰落系数"""
    X = gamma.rvs(alpha, scale=1.0/alpha, size=N)
    Y = gamma.rvs(beta, scale=1.0/beta, size=N)
    h = X * Y  # 乘积法
    return h
```

**验证**：
- 弱湍流(α=20, β=20)：h 应接近1，方差小
- 强湍流(α=2, β=2)：h 应有大幅波动，可能出现深度衰落
- 三档湍流参数参照：弱(α=11.6, β=10.9)、中(α=4.0, β=1.9)、强(α=2.0, β=1.5)

### Step 2: QPSK信号生成 + GG信道传输

```python
# QPSK调制
def qpsk_mod(bits):
    symbols = 2*(bits[0::2]) - 1 + 1j*(2*(bits[1::2]) - 1)
    return symbols / np.sqrt(2)

# 信道传输
def channel(symbols, h, snr_db):
    noise_power = 1.0 / (10 ** (snr_db / 10))
    noise = np.sqrt(noise_power/2) * (np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols)))
    return symbols * h + noise
```

**验证**：不同SNR下的BER曲线（无信道处理时应有高误码）

### Step 3: Ch2 信道估计验证（LS + MMSE）

```python
# LS估计
def ls_estimate(rx, pilots, pilot_idx):
    h_ls = rx[pilot_idx] / pilots
    # 插值到所有符号
    return h_interpolated

# MMSE估计（需要信道统计信息）
def mmse_estimate(rx, pilots, pilot_idx, snr, h_cov):
    # MMSE公式
    ...
```

**验证**：
- 画 NMSE vs SNR 曲线（LS vs MMSE）
- 不同湍流强度下的估计误差
- **关键问题**：DL方法(MLP)在此步骤能否跑通？即使效果不好，能跑通就行

### Step 4: Ch3 信道均衡验证（CMA）

```python
def cma_equalize(rx, num_taps=21, mu=0.001, num_iter=1000):
    """CMA盲均衡"""
    w = np.zeros(num_taps, dtype=complex)
    w[num_taps//2] = 1.0
    for i in range(num_iter):
        x = rx[i:i+num_taps]
        y = np.dot(w, x)
        error = (abs(y)**2 - 1) * y
        w = w - mu * error * np.conj(x)
    return w
```

**验证**：
- 均衡前后的星座图对比
- 均衡后BER改善
- **关键问题**：CMA在强GG湍流下能否收敛？

### Step 5: Ch4 载波恢复验证（VV算法）

```python
# 尝试用OptiCommPy的VV实现
# from optic.dsp.carrierRecovery import viterbi
# 或者手动实现VV算法
```

**验证**：
- 加入频偏和相位噪声后，VV能否恢复
- 收敛前后的相位误差
- **关键问题**：GG湍流导致的相位波动是否在VV的处理范围内？

### Step 6: 端到端BER曲线

三种场景：
1. 理想信道（AWGN only）→ 基线BER
2. GG湍流 + 无处理 → 高BER
3. GG湍流 + 估计 + 均衡 + 载波恢复 → 应接近基线

**画图**：BER vs SNR（dB），三条曲线

## 成功标准

| 指标 | PASS标准 | 意义 |
|------|---------|------|
| GG模型运行 | 弱/中/强三档参数都能跑 | Ch2基础 |
| LS估计NMSE | < 0dB at 20dB SNR | 最简方法可用 |
| CMA收敛 | 星座图明显收敛 | Ch3基础 |
| VV恢复 | 相位误差<10° | Ch4基础 |
| 端到端BER | 处理后比无处理改善>5dB | 整体可行 |

## 产出格式

```markdown
# [R010] 最小仿真原型

## 环境
- Python版本：
- 关键包版本（numpy, scipy, opticommpy）：
- GPU/CPU：

## 各步骤结果

### Step 1: GG信道模型
- 代码行数：
- 弱/中/强三档参数运行结果（h的均值、方差）
- [附图：三档湍流下h的时间序列]

### Step 2: QPSK+GG传输
- [附图：无信道处理时不同SNR的星座图]

### Step 3: Ch2信道估计
- LS vs MMSE的NMSE曲线
- [附图]

### Step 4: Ch3 CMA均衡
- 收敛过程
- 均衡前后星座图
- [附图]

### Step 5: Ch4 VV载波恢复
- 相位恢复效果
- [附图]

### Step 6: 端到端BER
- [附图：三条BER曲线]

## 失败记录
[任何步骤失败，记录失败现象、错误信息、可能原因]

## 结论
1. 三章技术路线是否端到端可行？
2. 哪些步骤有问题需要特别关注？
3. 预估完整仿真需要多少工时？
```

## 约束

- Python环境：`~/.venvs/torch/bin/python`
- 代码写在 `projects/thesis-figures/simulation/` 目录下
- 图保存为PDF格式（方便论文使用）
- 每个Step独立可运行
- 不要追求完美，**能跑通就行**——这是可行性验证，不是最终实验
- 产出文件：`.sessions/thesis-direction-pivot/R010-simulation-prototype.md`
- 如果OptiCommPy安装有问题，VV算法手写（~30行）
