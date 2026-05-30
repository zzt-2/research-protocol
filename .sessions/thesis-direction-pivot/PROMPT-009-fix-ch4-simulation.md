# PROMPT-009: 修复 Ch4 自适应载波同步仿真，验证 L2 级增益

> 用途：新对话中修复并重跑 sim_direction_a.py
> 目标：产出能支撑"湍流自适应载波同步三个公式"论文声称的仿真数据
> 判据：强湍流下自适应 vs 固定参数增益 ≥2 dB → L2 成立；<1 dB → L1 确认

## 背景

硕士论文 Ch4 声称三个湍流自适应公式：
1. FOE 窗口：$N_\text{opt} \propto h^{-4}$（深衰落下四次方 SNR 过低→阈值效应）
2. VV 窗口：$M_\text{opt} \propto h^{-2/5}$（平滑效应）
3. DPLL 带宽：$B_\text{L,opt} \propto h$（线性效应）

**当前仿真只测了第 3 个公式（DPLL 带宽自适应），FOE 和 VV 窗口仍是固定值。** 因此强湍流下增益只有 0.5 dB，不支持论文声称。

## 当前仿真结果（有缺陷）

| 场景 | 固定 BER | 自适应 BER | 增益 |
|------|---------|-----------|------|
| 弱湍流 | 0.0586 | 0.0020 | 14.7 dB |
| 中湍流 | 0.1328 | 0.0899 | 1.7 dB |
| 强湍流 | 0.2234 | 0.1990 | 0.5 dB |

## 需要修复的三个问题

### 修复 1：全三公式自适应（最关键）

`carrier_recovery_adaptive`（第 256-272 行）目前只自适应 DPLL 带宽。需要改为同时使用三个自适应参数：

```python
# 现状（错误）：
def carrier_recovery_adaptive(rx, h_est, ...):
    fo_est = fft_foe(rx, N_fft=FIXED_CFG['N_fft'])  # ← 固定
    ...
    rx_pll, _ = dpll_track(rx_comp, omega_n=omega_n_adapt)  # ← 自适应
    rx_cpr, _ = vv_cpr(rx_pll, Nw=FIXED_CFG['M_vv'])  # ← 固定

# 应该改为：
def carrier_recovery_adaptive(rx, h_est, ...):
    N_adapt, M_adapt, wn_adapt = adaptive_params(h_est, ...)
    fo_est = fft_foe(rx, N_fft=N_adapt)  # ← 自适应
    ...
    rx_pll, _ = dpll_track(rx_comp, omega_n=wn_adapt)  # ← 自适应
    rx_cpr, _ = vv_cpr(rx_pll, Nw=M_adapt)  # ← 自适应
```

### 修复 2：去掉 MMSE 预补偿

当前 `run_mve_trial`（第 303-305 行）在载波恢复前做了 MMSE 信道补偿。这是非标准处理流程，且给了两方不公平的优势。应该改为标准的接收链路：

```
标准链路：接收信号 → FFT FOE → DPLL → VV CPR → 判决
当前链路：接收信号 → MMSE补偿 → FFT FOE → DPLL → VV CPR → 判决（错误）
```

但有个问题：没有 MMSE 补偿的话，深衰落下信号幅度很小，载波恢复可能完全失效。解决方案：
- **方案 A**：不做 MMSE，让自适应 FOE 在深衰落时用更短的 N_fft（这是 h^{-4} 公式的本意）
- **方案 B**：只做幅度归一化（rx / |rx|），不做 MMSE，保留相位信息

建议用方案 A（最标准）。

### 修复 3：增加仿真长度和统计量

- Ns 从 2000 增到 10000-20000 符号（让 Doppler 动态有足够时间体现）
- n_trials 从 20 增到 50
- 添加 SNR 扫描：10-30 dB，步进 2 dB
- 产出三档湍流各自的 BER vs SNR 曲线图（固定 vs 自适应）

## 额外实验（如果时间允许）

### 实验 4：逐公式消融

分别测：只自适应 FOE / 只自适应 VV / 只自适应 DPLL / 全部自适应。这能定量展示每个公式的贡献。如果 h^{-4} FOE 在强湍流下贡献最大，这是论文最强证据。

### 实验 5：分块分析

在强湍流下，把衰落块按 h 大小分组（h<0.3 / 0.3<h<1 / h>1），分别统计 BER。预期：自适应方案在 h<0.3 的深衰落块中大幅优于固定方案。

## 输出要求

1. **修复后的仿真代码**：更新 `sim_direction_a.py`
2. **数值结果**：
   - 三档湍流 × 固定/自适应 BER 对比表
   - 强湍流下的增益（dB）
   - SNR 扫描曲线
3. **图表**（存到 `projects/thesis-figures/simulation/`）：
   - BER vs SNR 曲线（三档湍流，固定 vs 自适应）
   - 增益柱状图
   - （可选）消融实验图
4. **结论**：L2 成立 or L1 确认

## 判据

| 增益 | 判定 | 对论文影响 |
|------|------|-----------|
| ≥3 dB（强湍流） | **L2 成立** | Ch4 是方法级创新，论文底气足 |
| 1-3 dB | L1→L2 边界 | 能写，但答辩可能被追问 |
| <1 dB | **L1 确认** | 需要调整创新点定位，降低声称 |

## 仿真参数（保持一致）

```python
R_SYM = 2.5e9          # 符号率 2.5 Gsps
T_S = 1 / R_SYM        # 0.4 ns
LASER_LW = 10e3        # 激光线宽 10 kHz
F_RESIDUAL = 1e6       # 预补偿后残余频偏 ~1 MHz
DOPPLER_HIGH = 150e6   # 低仰角频偏变化率
DOPPLER_LOW = 30e6     # 高仰角频偏变化率
TURB = {'weak': (4.0, 3.0), 'moderate': (2.5, 1.8), 'strong': (1.5, 0.8)}
BLOCK = 100            # 块衰落大小
FIXED_CFG = {'N_fft': 1024, 'M_vv': 64, 'omega_n': 8e6, 'zeta': sqrt(2)/2}
```

## 必读文件

1. `projects/thesis-figures/simulation/sim_direction_a.py` — 当前仿真代码
2. `毕设/写作材料/formulas-ch3ch4-sync.md` — 三个自适应公式推导
3. `毕设/写作材料/thesis-status.md` — 全局状态看板

## 验证环境

```bash
~/.venvs/torch/bin/python
```
