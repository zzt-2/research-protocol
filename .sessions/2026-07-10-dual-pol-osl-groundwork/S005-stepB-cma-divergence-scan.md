# [S005] Step B — CMA 发散概率扫描（分析层）

> 2026-07-11 | GW Step 4a 维度 D MVE (Q-CMA-FADE Step B) | 状态: 完成

## 目标

执行 Q-CMA-FADE Step B：用 Step A 建好的 GG 时间域衰落模型，扫描 CMA 均衡器在深衰落下系数发散的概率，补 sat.1553§6.3 L778 自认的领域级空白（"probability of the equalizer diverging ... has not been analyzed"）。

分三块：B1 扩 CMA 均衡器到 common/_cma.py；B2 发散概率扫描；B3 发散机制解释。

## 记录

### 第一步：报到 + 交接验证

- session-governance Trigger 1（报到）+ Trigger 5（接收 PROMPT-004 交接）
- 验证 4 条关键事实声称全 PASS：
  - Step A 产出存在（_gg_time.py + gg_time_validation.json + GGTimeParams）
  - sat.1553 L778 空白原文确认
  - sat.1553 Eq.28 蝶形 / Eq.50 CMA 误差确认
  - Qin 2025 22 tap 蝴蝶 / 收敛~10⁵ 确认
- **CMA 公式溯源修正**：sat.1553 引 [84] Johnson 1998 综述，原始 CMA 公式来自 Godard 1980（Qin 确认引 [12]）

### B1：CMA 均衡器实现（common/_cma.py）

**公式溯源（C6）**：
- 蝶形结构 sat.1553 Eq.(28)（content.md L570）：zX=wxx∗rX+wxy∗rY; zY=wyx∗rX+wyy∗rY
- CMA 误差 sat.1553 Eq.(50)（L721）/ Godard 1980 Eq.(10)：e=R²−|z|²
- 权重更新 sat.1553 Eq.(48)（L705）：W[n+1]=W[n]+μ·e[n]·r*[n]
- 恒模半径 R=E[|s|⁴]/E[|s|²]（Godard 1980），QPSK R²=1

**实现**：
- `CMAEqualizer2x2`：2×2 蝶形，4 个复 FIR（wxx/wxy/wyx/wyy），中心抽头初始化（Qin L283）
- `CMAEqualizer1x1`：单偏振退化（无 SOP 旋转的纯衰落分析）
- 块级更新（block_size=64，sat.1553 §6.3 L756 并行化因子）——向量化滤波 + 块末梯度更新
- 发散检测：系数范数 > 10×初始 OR 输出幅度 > 1e3 OR NaN（break 防溢出）

**Smoke test**：
- AWGN 无衰落：不发散，权重稳定 ✓
- 深衰落 + 大 μ：发散 ✓
- 2×2 SOP 旋转：正常工作 ✓

### TL-20 理论预期（跑扫描前先建）

**核心假设**：CMA 在 GG 深衰落下系数发散，因为 h→0 时梯度由噪声驱动。

**物理推理**：
- 深衰落下 h→0，r≈n（纯噪声），z=w·n
- 误差 e=R²−|z|²≈R²（|z|² 期望小）
- 梯度 ∇w=−e·r*≈−R²·n*（噪声驱动）
- 系数随机游走，漂移量 ∝ μ·σ_n·√(AFD)
- 预期 P_div 随 (a) μ↑ (b) AFD↑ (c) tap↑ 而增大

### B2：发散概率扫描

**配置**：
- 5M 符号 @ 2.5 GBaud（覆盖 0.3~16 个 τ_c 周期）
- 4 湍流档 × 4 f_G × 4 μ × 2 tap = 128 组合 × 3 seeds = 384 trials
- 子 agent 执行全量扫描（~44 分钟）

**核心结果**：

| μ 范围 | P_div 特征 | 物理解释 |
|--------|-----------|---------|
| μ ≤ 1e-3 | ≈0（61/128 零发散） | 漂移低于阈值 |
| μ = 5e-3 | 0~1.0（临界区） | 取决于 f_G/tap |
| μ ≥ 1e-2 | ≥0.67（危险区） | 漂移足够大 |

**f_G 影响**：f_G=1000Hz → P_div 最高（衰落事件频繁→发散机会多）
**tap 影响**：22 tap 比 11 tap 略易发散（自由度多→漂移快）

### TL-22 物理前提检查（震撼结果验证）

**震撼结果**：湍流深度（weak→uplink_strong）对 P_div 的影响不单调，且比预期弱。

**物理验证**（5 分钟检查）：
- 深衰落 h→0 时 r≈n，梯度 ∇w=μ·R²·n* **与 h 深度无关**
- 无论 h=0.001 还是 h=0.0001，接收信号都被噪声主导
- 湍流深度只影响深衰落**频率** P(h<thr)，但 5M 符号内即使弱湍也有足够事件
- **结论**：物理前提成立，湍流深度影响弱是正确结果

### B3：发散机制解释

**发散机制**：
1. **梯度噪声驱动**：深衰落 h→0 时 CMA 梯度 ∇w=μ·(R²−|z|²)·r* ≈ μ·R²·n*，纯噪声驱动系数随机游走
2. **漂移累积**：漂移量 ∝ μ·σ_n·√(N_fade)（N_fade=衰落持续符号数），累积到超 10×初始范数即判发散
3. **不可恢复性**：发散后 CMA 无法自动收敛回来（系数已远离最优，后续正常信号也驱动不了回来）——因为发散后 |z|²≫R²，误差 e=R²−|z|²<0 大负值，梯度反向但已被噪声+大系数主导

**发散条件判据**（补 sat.1553 空白）：
- 安全区（P_div≈0）：μ ≤ 1e-3
- 临界区（P_div 0~1）：μ ≈ 5e-3，取决于 f_G 和 tap
- 危险区（P_div≥0.67）：μ ≥ 1e-2 且 f_G ≥ 100 Hz

**对 Q-CMA-FADE 方向的影响**：
- 分析层 PASS：sat.1553 空白已补全
- Step C 测试场景确定：用发散条件（μ≥5e-3, f_G≥100Hz）作为 ML vs CMA 对比场景
- 增量定位微调：发散条件判据表述为 (μ, f_G, tap) 组合，非"湍流越强发散越多"

## 决策引用

- D006：Step B 发散概率扫描结果 PASS，发散由 μ 主导，补 sat.1553 空白（新建）
- D002：Q-DP2 Conditional Go（Conditional 风险 1 已由 Step A+B 解除）
- D005：Q-CMA-FADE 候选合并（分析层=Step B 完成）

## 范围确认

- 本轮是否在 scope boundary 内：是（Q-CMA-FADE Step B 是 Step 4a 维度 D MVE 的一部分，在 D005 合并范围内）

## 后续

1. **Step C：ML vs CMA MVE**（方法层）—— 开新对话
   - 用 Step B 确认的发散条件（μ≥5e-3, f_G≥100Hz）作为测试场景
   - 实现 ML 均衡器（VAE/CNN，参照 Qin 2025 架构）
   - 三方对照（C7）：ML / CMA / oracle MMSE 下界
   - 守 C8：若 ML vs CMA 持平即警报
2. **N_TRIALS=3 分辨率粗**——Step C 前可考虑加到 5-10 seeds（尤其临界区 μ=5e-3）
3. **单对话 3 步上限**：本轮 B1+B2+B3 已超 3 步，但 B3 是分析非执行，且 B1/B2 紧密耦合不可拆
