# PROMPT-003: Ch4 载波同步自适应公式推导

> 用途：新对话中完成 Ch4 三个核心自适应公式的严格推导
> 前置：PROMPT-001（Ch2 模型）+ PROMPT-002（Ch3 精度需求）完成
> 验证代码：`sim_direction_a.py`（6场景数据）+ `sim_cascade_robustness.py`（含噪声数据）
> 重要性：**最高**，这是论文的核心创新

## 论文背景

Ch4 提出湍流强度自适应的载波同步算法，核心是三个解析公式，使载波同步参数（FFT窗口、VV窗口、DPLL带宽）随瞬时信道状态 $h$ 自适应调整。

## Ch4 章节结构

```
4.2 载波同步系统模型（Doppler+湍流+联合模型）
4.3 湍流自适应频偏估计算法
4.4 湍流自适应载波相位恢复算法
4.5 仿真结果
```

## 三个核心公式（必须严格推导）

### 核心公式1：FFT 频偏估计自适应窗口（4.3 节）

$$N_\text{opt}(h) = \frac{80}{\bar\gamma \cdot h^4}$$

**物理意义**：FFT 窗口长度 $N$ 需要足够大以获得频率分辨率，但深衰落下 $h$ 很小时四次方信噪比 $\gamma \cdot h^4$ 太低导致检测失败。该公式在分辨率和检测可靠性之间取最优折中。

**需要推导**：
1. FFT 四次方频偏估计的方差公式（$\text{var}(\hat{f})$ 与 $N$ 和 SNR 的关系）
2. 频偏分辨率公式（$\Delta f_\text{res} = 1/(N \cdot T_s)$）
3. 总误差 = 估计方差 + Doppler 漂移误差，对 $N$ 求最小值
4. 解出 $N_\text{opt}(h)$ 的解析形式
5. **关键近似条件**：在 Gsps 符号率下，Doppler 漂移仅 61 Hz，可忽略。主导因素是深衰落下四次方 SNR 过低 → 解释了 $h^{-4}$ 的阈值依赖形态

**验证数据**：
- `sim_direction_a.py` 中的自适应 N 映射：`N_map = {弱: 4096, 中: 16384, 强: 65536}`
- 6 场景 PASS/FAIL 数据

### 核心公式2：VV 载波相位恢复最优窗口（4.4 节）

$$M_\text{opt}(h) = K_M \cdot (\bar\gamma \cdot h^2)^{-1/5} \cdot (\Delta f \cdot T_s)^{-2/5}$$

**物理意义**：VV 算法对 $M$ 个符号取平均估计相位。$M$ 大则噪声平滑好但 Doppler 漂移引入额外误差。最优 $M$ 平衡两者。

**需要推导**：
1. VV 相位估计方差 $\sigma_\phi^2 \approx 1/(2M \cdot \gamma \cdot h^2)$（噪声项）
2. Doppler 漂移导致的相位误差 $\approx \pi \Delta\dot{f} T_s^2 M$（漂移项）
3. 总相位误差 MSE = 噪声项 + 漂移项²
4. 对 $M$ 求最小值，解出 $M_\text{opt}$
5. 解释 $h^{-2/5}$ 的平滑依赖形态（vs $h^{-4}$ 的阈值形态）

**验证数据**：
- `sim_direction_a.py` 中的 VV 窗口映射
- 固定 vs 自适应 BER 对比数据

### 核心公式3：DPLL 最优环路带宽（4.4 节）

$$B_\text{L,opt}(h) = B_0 \cdot h = \sqrt{\frac{\pi \Delta\nu_L \bar\gamma}{T_s}} \cdot h$$

**物理意义**：二阶 DPLL 的环路带宽 $B_L$ 控制跟踪速度和噪声抑制的折中。$h$ 大（信道好）时用大带宽快速跟踪，$h$ 小（深衰落）时用小带宽抑制噪声。

**需要推导**：
1. 二阶 DPLL 的稳态相位误差方差（与 $B_L$ 和 $h$ 的关系）
2. Doppler 跟踪误差（与 $B_L$ 的关系）
3. 总跟踪误差对 $B_L$ 求最小值
4. 解释 $h^1$ 的线性依赖形态（最简单的依赖关系）
5. 与 Zhao 2025 固定 $B_L = 8$ Mrad/s 的对比：我们自适应 88 Mrad/s（好信道）→ 小值（坏信道）

**验证数据**：
- `sim_direction_a.py` 中的 DPLL 带宽映射
- 自适应 vs 固定参数的 BER 差异（最强场景 +14.75 dB）

## 三个公式的统一解读

| 公式 | $h$ 依赖 | 形态 | 物理解释 |
|------|---------|------|---------|
| $N_\text{opt}$ | $h^{-4}$ | 阈值效应 | 深衰落下四次方SNR崩溃，需指数级增大窗口 |
| $M_\text{opt}$ | $h^{-2/5}$ | 平滑效应 | 噪声平滑与Doppler漂移的权衡，灵敏度适中 |
| $B_\text{L,opt}$ | $h^1$ | 线性效应 | 信道好→大带宽快跟踪；信道差→小带宽抑噪声 |

这三种不同的 $h$ 依赖形态本身就是重要的研究发现。

## 载波恢复链完整架构

还需要推导/描述完整的载波恢复链：

$$r[k] \to \text{星历预补偿} \to \text{FFT-FOE}(\hat{f}_\text{res}) \to \text{二阶DPLL} \to \text{VV/BPS CPR}(\hat{\phi}) \to \text{判决}$$

每一步的信号模型和误差传播需要清晰描述。

## 验证要求（最高标准）

1. **解析验证**：每步推导必须数学正确，不能跳步
2. **数值验证**：用 Python 实现解析公式，与 `sim_direction_a.py` 的仿真结果比对
   - 固定参数 vs 自适应参数的 BER 差异
   - 三个公式的最优值 vs 代码中的映射值是否一致
3. **含噪声验证**：用 `sim_cascade_robustness.py` 数据，验证在 NMSE=-10dB 噪声下自适应公式是否仍然有效（STRONG PASS 6/6）
4. **与 Ch3 衔接**：确认 Ch3 给出的精度需求（NMSE ≥ -10dB）与 Ch4 公式的适用范围一致

验证用的 Python 环境：`~/.venvs/torch/bin/python`

## 输出

追加到：`毕设/写作材料/formulas-ch3ch4-sync.md` 的 Ch4 原创推导节。

## 必读文件

1. `毕设/写作材料/formulas-ch3ch4-sync.md` — 标准公式 + 已提取的代码公式
2. `毕设/写作材料/formulas-ch2-system-model.md` — Ch2 推导结果
3. `毕设/写作材料/symbol-conventions.md` — 符号表
4. `毕设/写作材料/thesis-framework.md` — Ch4 概述段
5. `projects/thesis-figures/simulation/sim_direction_a.py` — 载波同步 MVE（**最关键**）
6. `projects/thesis-figures/simulation/sim_cascade_robustness.py` — 级联鲁棒性数据
7. `.sessions/thesis-direction-pivot/S011-direction-a-mve.md` — 载波同步 MVE 结论
8. `.sessions/thesis-direction-pivot/S015-cascade-robustness-mve.md` — 级联鲁棒性结论
9. `papers/doi/10.1109_jlt.2023.3281082/content.md` — Fernandes 2023 (Doppler参考)
10. `papers/downloads/2026-05-29/1-s2.0-S0030401823000573-main.md` — Liu 2023 (VV参考)
