# 导师沟通材料 — Ch4方向A确认

> 准备时间：2026-05-30 | 用于导师会议

---

## 一句话定位

**Ch4方向**：湍流强度自适应的LEO星地载波同步——从GG模型参数到最优FOE/CPR参数的解析设计与验证

## 文献空白确认

| 子方向 | 文献量 | 评估 |
|--------|--------|------|
| LEO多普勒补偿(射频+光) | ≥20篇 | 拥挤 |
| LEO FSO多普勒补偿 | ~10-15篇 | 少量偏多 |
| 相干光星地载波恢复 | ~8-10篇 | 少量 |
| **LEO Doppler + 湍流 + 载波同步三联合** | **0-1篇** | **近零空白** |

核心差异化：无人做过湍流强度→载波恢复参数的解析优化。

## Paillier 2020负面证据回应

Paillier声称"湍流对载波同步可忽略"**仅限完整AO**：
- 有AO：通量惩罚-4.5dB，DPLL正常工作
- **无AO：通量惩罚-23dB，载波同步数据=零**（从未测试）
- 结论：无/弱AO场景是完全空白，是我们的创新入口

## MVE仿真验证结果

6种联合场景（3湍流×2仰角），固定Zhao配置 vs 自适应DPLL带宽：

| 场景 | 固定BER | 自适应BER | 增益 | 判定 |
|------|---------|----------|------|------|
| 弱湍流 | 5.9% | 0.2% | **+14.8 dB** | PASS |
| 中湍流 | 13.3% | 9.0% | **+1.7 dB** | PASS |
| 强湍流 | 22.3% | 19.9% | **+0.5 dB** | PASS |

**总判定：5/6场景≥0.5dB → 方向A可行**

### 关键发现

1. DPLL环路带宽是主要增益来源：理论最优88Mrad/s vs Zhao固定8Mrad/s
2. MMSE信道补偿避免深衰落噪声爆炸（传统ZF补偿的问题）
3. Doppler变化率差异（150 vs 30 MHz/s）在2.5Gsps下影响可忽略

## 3项需确认决策

### 决策1：Ch4切换到方向A

**建议：是**
- 从"FOE+CPR自适应参数微调"→"湍流强度自适应LEO载波同步"
- 理由：文献空白真实（三联合0-1篇），MVE已通过，理论深度锚点已建立
- 风险可控：弱湍流增益可能偏乐观，但中强湍流增益确定

### 决策2：是否需要DL/DRL元素

**建议：不需要**
- 方向A是纯传统信号处理（解析推导+自适应环路）
- 创新点"湍流统计特性→最优参数的解析关系"本身是理论贡献
- 如果需要，可加DL对比实验（如LSTM预测最优参数），但不作为主线

### 决策3：Ch5 FPGA衔接

**建议：方向A更适合FPGA验证**
- Doppler补偿（NCO+累加器）是FPGA标准模块
- DPLL（数字环路滤波器）直接映射到FPGA
- VV窗口可变平均器也适合硬件实现
- 比原方向（自适应FOE/CPR窗口）更有说服力

## 四章衔接

```
Ch2: GG湍流信道建模 + 信道估计 → 提供h_est
Ch3: 功率自适应预补偿（MMSE） → 处理幅度维度
Ch4: 湍流感知载波同步（方向A） → 处理频率/相位维度
Ch5: FPGA验证（Doppler补偿+DPLL+VV）
```

Ch3处理幅度，Ch4处理频率/相位，两者正交且互补。

## 产出物清单

| 产物 | 路径 |
|------|------|
| 解析推导 | `.sessions/thesis-direction-pivot/R016-analytical-formula-derivation.md` |
| MVE仿真代码 | `projects/thesis-figures/simulation/sim_direction_a.py` |
| MVE结果图 | `projects/thesis-figures/simulation/mve_direction_a.pdf` |
| SNR扫描图 | `projects/thesis-figures/simulation/mve_snr_sweep.pdf` |
| 参数曲线图 | `projects/thesis-figures/simulation/adaptive_params.pdf` |
| Session记录 | `.sessions/thesis-direction-pivot/S011-direction-a-mve.md` |
