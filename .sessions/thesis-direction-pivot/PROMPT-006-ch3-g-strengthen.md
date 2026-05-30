# PROMPT-006: 方向 G 加深 — 设计准则 + 估计误差 + EGG 对比

> 用途：新对话中加强方向 G，使其不只是"参数替换"
> 前置：S002 推导已完成（BER floor + 中断概率 + σ_φ 关系）
> 验证代码：`projects/thesis-figures/simulation/sim_ch3_ber_bounds.py`

## 方向 G 当前状态

**已完成**（`.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md`）：
- 平均 BER 闭合级数解（Fourier 级数法 + Meijer-G）
- BER floor = Q(π/(4σ_φ))，MC 验证 median 误差 0.6%
- 中断概率 = F_GG(h_th)，γ_th 数值验证
- σ_φ 与 B_L/M 的关系链（连接 Ch4）

**核心问题**：当前贡献偏薄——GG 是 Málaga 的 ρ=0 特例，高斯相位是 Tikhonov 简化版，审稿人可能说"就是 Petkovic 2023 换个信道模型"。

## 需要完成的三个加强项

### 加强 1：湍流自适应设计准则（最重要，半天）

**目的**：从 BER 分析反推出工程可直接使用的设计约束表。

**具体产出**：
1. 分湍流强度的 σ_φ 容限表（已有雏形，需扩展）：
   - 三档湍流（弱/中/强）× 多个 P_target（1e-3 到 1e-6）的 σ_φ 上限
   - 每个组合对应的 SNR 惩罚（dB）
2. 分湍流强度的 B_L 和 M 设计范围：
   - 从 σ_φ ≤ σ_φ_max 反推 B_L ≤ B_L_max(h) 和 M ≥ M_min(h)
   - 与 Ch4 的三个自适应公式建立定量衔接
3. "不可用区域"标注：哪些湍流+SNR 组合下即使完美同步也无法达标

**验证**：与 Ch4 的 sim_direction_a.py 参数对比，确认设计准则与实际自适应参数一致。

### 加强 2：信道估计误差对 BER 的影响（1-2 天，核心创新）

**目的**：将 Ch2 的信道估计误差引入 BER 分析，展示估计不完美导致的性能偏离。这使 Ch3 从纯理论变成"系统级分析"。

**具体产出**：
1. 模型扩展：$\hat{h} = h + e$（e 为估计误差），推导 $P_b(\hat{h}, \phi)$ vs $P_b(h, \phi)$ 的偏离
2. NMSE → BER 偏离的定量关系：
   - 在 NMSE = -5dB, -10dB, -15dB, -20dB 下，BER 曲线偏移多少 dB
   - 与 `sim_cascade_robustness.py` 的级联数据交叉验证（载波同步 6/6 PASS @ NMSE=-10dB）
3. BER floor 在估计误差下的变化：
   - 估计误差是否引入新的 BER floor？
   - 估计误差 + 相位误差的联合 floor 表达式

**踩坑预警**：
- Meijer-G 嵌套积分在估计误差模型下可能收敛困难——先用 MC 仿真验证趋势，再尝试解析
- 如果解析不可行，用数值积分 + 曲线拟合给出工程近似公式也可以

### 加强 3：与 Hu 2025 (EGG) 对比（半天）

**目的**：展示 GG 模型选择的影响，证明"在大气湍流场景下 GG 比 EGG 更合适"。

**具体产出**：
1. 复现 Hu 2025 的 EGG 结果（从论文中提取参数）
2. 同参数下 GG vs EGG 的 BER 对比曲线
3. 定量说明：GG 和 EGG 在哪些湍流参数下差异显著，为什么 GG 是大气 FSO 的更佳选择

## 与 Ch4 的衔接（核心叙事）

加强后的 Ch3 叙事链：

```
Ch3 产出：
  1. GG+相位误差 BER 闭合解 → "性能有多差"
  2. BER floor → "瓶颈是载波同步精度"
  3. 分湍流设计准则 → "σ_φ 需要控制在多少"
  4. 估计误差影响 → "估计精度也需要保证"
         ↓
Ch4 输入：
  - σ_φ 设计目标（来自第 3 点）
  - h 估计值（来自 Ch2，精度要求来自第 4 点）
  - 自适应公式 N_opt, M_opt, B_L,opt 直接满足设计准则
```

## 输出

追加到 `S002-ber-closed-form-derivation.md` 的新节：
- §7 湍流自适应设计准则
- §8 信道估计误差对 BER 的影响
- §9 GG vs EGG 对比
- 更新 §6 σ_φ 关系链（加入加强 1 的设计表）

仿真代码追加到 `sim_ch3_ber_bounds.py` 或新建 `sim_ch3_estimation_impact.py`。

## 必读文件

1. `.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md` — 已完成推导
2. `.sessions/2026-05-30-ch3-direction-exploration/H001-ch3-direction-g-handoff.md` — 方向 G 交接
3. `projects/thesis-figures/simulation/sim_ch3_ber_bounds.py` — 已有仿真
4. `projects/thesis-figures/simulation/sim_cascade_robustness.py` — 级联鲁棒性数据（验证加强 2）
5. `projects/thesis-figures/simulation/sim_direction_a.py` — Ch4 自适应参数（验证加强 1）
6. `毕设/写作材料/formulas-ch3ch4-sync.md` — Ch4 公式（σ_φ 关系链）
7. `毕设/写作材料/formulas-ch2-system-model.md` — Ch2 符号和参数

## 验证环境

```bash
~/.venvs/torch/bin/python
```
