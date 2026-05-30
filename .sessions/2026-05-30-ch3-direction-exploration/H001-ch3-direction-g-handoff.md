# Handoff: Ch3 方向 G 确认 + 仿真验证完成

> 来源: S001 | 交接目标: 新对话继续 Ch3 推导和论文框架更新
> 文件名: H001-ch3-direction-g-handoff.md

## 已完成边界

1. **6 个候选方向检索完成**：A(级联灵敏度)、B(AMC)、C(Doppler)、D(信号检测)、E(信道跟踪)、G(性能界)
2. **E 和 G 两个方向精读完成**：各 4-5 篇核心论文结构化提取
3. **方向 G 确认**：用户选择"大气湍流信道下 QPSK 相干检测链路性能分析"作为 Ch3
4. **补充检索完成**：GG-BER 经典论文（Al-Habash, Zedini, Bhatnagar, Sandalidis, Petkovic, Hu 等）
5. **BER floor 蒙特卡洛验证通过**：2Q(π/(4σ_φ)) 在 AWGN 下偏差 <5%
6. **仿真代码**：`projects/thesis-figures/simulation/sim_ch3_ber_bounds.py`（4 个实验）

## 不要做什么

- **不要重新考虑已排除方向**（A/D 已淘汰，B/C 降为备选）
- **不要在推导前跳过文献精读**——Petkovic 2023 和 Hu 2025 的推导流程必须读
- **不要自己发明 Meijer-G 恒等式**——必须从 Wolfram/Gradshteyn 表中查到标准恒等式
- **不要忽略 σ_φ 与环路参数的关系**——这是 Ch3→Ch4 衔接的核心

## 必读

1. `.sessions/2026-05-30-ch3-direction-exploration/S001-candidate-search.md` — 完整检索+精读+可行性记录
2. `.sessions/2026-05-30-ch3-direction-exploration/topic-index.md` — 专题状态和约束
3. `毕设/写作材料/formulas-ch2-system-model.md` — 符号和公式系统（GG 模型、SNR 定义）
4. `毕设/写作材料/formulas-ch3ch4-sync.md` — 载波同步公式（σ_φ 来源）
5. `projects/thesis-figures/simulation/sim_ch3_ber_bounds.py` — 已完成的仿真代码

## 核心数学框架（待推导）

### 已验证
- BER floor = 2Q(π/(4σ_φ)) ✓（MC 验证，AWGN 收敛 24-30 dB）
- QPSK 条件 BER: P_b(γ,φ) = Q(√(2γ)cos(φ+π/4)) + Q(√(2γ)cos(φ-π/4))

### 待推导
1. **平均 BER 闭合解**：∫∫ P_b(γ,φ) · f_φ(φ) · f_GG(I) dφ dI，用 Meijer-G 表示
   - f_GG(I) 的 Meijer-G 形式已知（Zedini 2015）
   - Q 函数的 Meijer-G 形式已知
   - 关键步骤：相乘后的 Meijer-G 积分恒等式
2. **BER floor 与环路参数关系**：σ_φ = f(B_L, γ, 导频密度)
   - 对于 DPLL: σ_φ² ≈ B_L · T_s / (2·SNR)（线性化模型）
   - 对于 VV/BPS CPE: σ_φ² ≈ 1/(2·M·SNR)（M = 平均窗长）
3. **中断概率**：P_out = P(BER > BER_target) = P(I < I_th 或 |φ| > φ_th)

### 关键参考论文推导流程
- **Petkovic 2023**：Málaga + Tikhonov → Fourier 级数法 → SEP 闭合级数
- **Hu 2025**：EGG + 高斯相位误差 → 精确 BER + BER floor + 高 SNR 渐近
- 两者方法可组合：GG（替换 EGG）+ 高斯相位误差（保留 Hu 的模型）→ 闭合解

## 接口变更

新增文件：
- `projects/thesis-figures/simulation/sim_ch3_ber_bounds.py`
- `projects/thesis-figures/simulation/fig_ch3_ber_floor.png`
- `projects/thesis-figures/simulation/fig_ch3_ber_turbulence.png`
- `projects/thesis-figures/simulation/fig_ch3_floor_vs_sigma.png`
- `projects/thesis-figures/simulation/fig_ch3_ber_awgn_floor.png`
- `.sessions/2026-05-30-ch3-direction-exploration/` (topic-index, S001, H001)

## 验证阈值

| 验证项 | PASS 标准 | 当前状态 |
|--------|----------|---------|
| BER floor 公式 | MC vs 理论偏差 <5% | ✓ 通过 |
| 6 方向检索 | 每方向 ≥5 组关键词 | ✓ 通过 |
| 精读 | E+G 各 ≥3 篇 | ✓ E:4篇, G:4篇 |
| 文献空白确认 | GG+高斯相位+QPSK = 0 | ✓ 已确认 |

## 下一轮

1. **精读 Petkovic 2023 和 Hu 2025 的推导流程**（子 agent 逐公式读）
2. **推导 GG + 高斯相位误差 + QPSK 的平均 BER 闭合解**
3. **推导中断概率闭合表达式**
4. **建立 σ_φ → B_L 关系链**（连接 Ch3→Ch4）
5. **更新 thesis-framework.md Ch3 部分**
6. **更新开题报告 Ch3 内容**
