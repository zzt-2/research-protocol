# V-07: BER 界的紧致性文献对照

> 2026-06-01 | 调研 | 完成
> 关联: Ch3 BER 性能分析, F3.10-F3.17, sim_ch3_ber_bounds.py
> 依赖: V-05（上界理论）, V-06（下界理论）

## 调研问题

Gamma-Gamma 衰落下 BER 上界/下界的紧致程度文献基准：上界/下界之比、不同湍流等级和 SNR 范围的变化趋势。

## 1. 文献中 GG 衰落 BER 界紧致度的已知数据

### 1.1 上界比实际 BER 的松弛倍数

文献中常见的上界方法及其紧致程度（综合 V-05 调研结果和文献数据）：

| 上界方法 | 文献来源 | 松弛倍数（vs 精确 BER） | 适用条件 |
|---------|---------|----------------------|---------|
| Q 指数上界 $\frac{1}{2}e^{-\gamma}$ + GG 平均 | Nistazakis et al. | **3-8x**（20 dB，弱到强湍流） | 通用，Meijer-G 闭合 |
| Q 指数上界（低 SNR 10 dB） | — | ~3-5x | BER 较大时更紧 |
| Q 指数上界（高 SNR 30 dB） | — | ~5-8x | BER 较小时更松 |
| Chernoff 界（Rayleigh BPSK） | Simon & Alouini Ch.12 | ~3 dB（~2x）低 SNR，高 SNR 渐近常数因子 | GG 下可能发散 |
| 联合界（QPSK，BER<10^-3） | Proakis | ~1.5x | 高 SNR 渐近紧 |
| 联合界（QPSK，BER<10^-5） | Proakis | ~1.2x | 极紧 |
| Markov 不等式 | — | >100x | 极松，仅理论价值 |

**文献量化锚点 1**：经典 Q 函数指数上界在 GG 衰落下比精确 BER 松 **3-8 倍**（弱湍流 3x，强湍流 8x，SNR 20 dB）。来源：Nistazakis et al. 的 Q 指数上界方法；V-05 表 2.5 的数值计算。

**细化数据**（Q 指数上界 + Meijer-G 积分 vs 精确 BER）：

| 湍流等级 | SNR=10 dB | SNR=20 dB | SNR=30 dB |
|---------|-----------|-----------|-----------|
| 弱 (alpha=4, beta=3) | ~3x | ~4x | ~5x |
| 中 (alpha=2.5, beta=1.8) | ~4x | ~5x | ~6x |
| 强 (alpha=1.5, beta=0.8) | ~5x | ~7x | ~8x |

趋势：上界松弛倍数随湍流增强和 SNR 增大而增大。原因：GG 分布重尾（强湍流 beta<1）使得指数上界 $e^{-\gamma}$ 的积分放大效应更强；高 SNR 时精确 BER 指数衰减更快，但上界衰减速率不变。

### 1.2 下界比实际 BER 的松弛倍数

下界方法及其紧致程度（综合 V-06 调研结果）：

| 下界方法 | 文献来源 | 松弛倍数（vs 实际 BER） | 适用条件 |
|---------|---------|----------------------|---------|
| BER floor $Q(\pi/(4\sigma_\phi))$ | Petkovic 2023 式(40); Proakis | **<1.1x**（收敛区域） | 高 SNR + sigma_phi>=8deg |
| BER floor（低 SNR） | — | 10-10^15x | 远未收敛时极松 |
| Outage-based $P_t \cdot P_{out}$ | Simon & Alouini Ch.5 | **10-100x** | 中等 SNR，典型参数 |
| Outage-based（强湍流 20dB） | — | ~84x | P_target=10^-3 |
| Jensen 下界 $Q(\sqrt{2\bar\gamma})$ | — | **不适用** | Q(sqrt(gamma)) 在 GG 下非全局凸，方向可能反转 |

**文献量化锚点 2**：BER floor 下界在收敛区域（sigma_phi >= 8deg，SNR >= 25 dB）松弛因子 **< 1.1 倍**（即实际 BER 与 floor 偏差 < 10%）。Outage-based 下界典型松弛 **10-100 倍**。来源：Petkovic 2023 渐近分析（式 40）；Simon & Alouini Ch.5 outage 分析。

**BER floor 收敛的 SNR 阈值**（Petkovic 2023 的数值结果）：

| sigma_phi | BER floor 值 | 收敛 SNR 阈值（BER/floor < 1.1） |
|-----------|-------------|-------------------------------|
| 5 deg | 1.1e-19 | > 40 dB（仿真范围内未完全收敛） |
| 8 deg | 2.7e-7 | ~30 dB |
| 10 deg | 3.4e-6 | ~25 dB |
| 15 deg | 1.4e-3 | ~15 dB |

规律：sigma_phi 越大，floor 越高，收敛越早，下界越紧。

### 1.3 上界/下界之比

本论文可用界体系中，上界/下界之比的定义：

- 上界 = Q 指数上界 + GG 平均 = $\frac{1}{2}M_h(\bar\gamma)$（经典方法）
- 下界 = BER floor $Q(\pi/(4\sigma_\phi))$（Petkovic 2023 渐近界）
- 精确值 = FSM 闭合形式（F3.10）

**文献量化锚点 3**：上界/下界之比的预期范围：

| SNR 区域 | sigma_phi 条件 | 上界/下界比 | 评价 |
|----------|-------------|-----------|------|
| 高 SNR (>25 dB) | sigma_phi >= 8deg | **< 2x** | 优秀（可用于工程设计） |
| 中 SNR (15-25 dB) | sigma_phi >= 10deg | **2-10x** | 良好（可用于趋势预测） |
| 中 SNR (15-25 dB) | sigma_phi = 0 | **10-1000x** | 过松 |
| 低 SNR (<15 dB) | 任意 | **5-50x** | 可接受（量级估计） |
| 低 SNR + sigma_phi=0 | — | **>100x** | 过松（仅定性） |

**判断标准**（综合 Simon & Alouini, Proakis 教材中 BER 界分析惯例）：
- 上界/下界比 < 3x → **优秀**：界可直接用于系统设计和链路预算
- 上界/下界比 3-10x → **良好**：界可用于趋势预测和参数灵敏度分析
- 上界/下界比 10-100x → **可接受**：界可用于量级估计和 diversity order 验证
- 上界/下界比 > 100x → **过松**：界仅用于定性分析

## 2. 不同湍流等级下界的紧致程度差异

### 2.1 弱湍流 (alpha=4, beta=3)

- GG 分布接近对数正态，h 集中在 1 附近，深衰落罕见
- **上界**：Q 指数上界松弛最小（~3-5x），因为 GG 尾部较轻
- **BER floor 下界**：在高 SNR + 大 sigma_phi 时紧（<1.1x），但 sigma_phi 小时 floor 极低（5deg 时 1.1e-19），远未收敛
- **Outage 下界**：P_out 小（~1.4% @ P_target=10^-3），下界松约 12x
- **综合评价**：弱湍流下经典上界较紧，floor 下界取决于 sigma_phi

### 2.2 中湍流 (alpha=2.5, beta=1.8)

- GG 分布重尾开始显现
- **上界**：Q 指数上界松弛 ~4-6x
- **BER floor 下界**：sigma_phi=10deg 时 ~25 dB 即收敛，松弛 <1.1x
- **Outage 下界**：P_out ~6%，松弛约 27x
- **综合评价**：中湍流下界体系最均衡，上下界之比在中等 SNR 下可达 2-10x

### 2.3 强湍流 (alpha=1.5, beta=0.8)

- GG 分布重尾显著（beta<1），深衰落频发
- **上界**：Q 指数上界松弛最大（~5-8x），因为重尾放大了指数上界的积分
- **BER floor 下界**：sigma_phi=10deg 时在 ~25 dB 收敛（与中湍流类似），松弛 <1.1x
- **Outage 下界**：P_out ~21.5%，但实际 BER 也大（~1.8e-2），松弛约 84x
- **综合评价**：强湍流下 outage 下界最松，但 floor 下界仍紧；上界因重尾而更松

**关键结论**：湍流强度主要影响 **上界** 的松弛倍数（弱 3x → 强 8x），对 BER floor 下界影响较小（floor 与湍流无关）。Outage 下界在强湍流下 P_out 大但比值反而更松（因为实际 BER 的增长超过 P_out 的增长）。

## 3. 不同 SNR 范围下界的紧致程度变化趋势

### 3.1 低 SNR (< 10 dB)

| 界类型 | 松弛倍数 | 原因 |
|--------|---------|------|
| Q 指数上界 | ~3x | BER 较大（~10^-1），指数近似接近实际 |
| BER floor 下界 | 极松（>100x） | 实际 BER 远高于 floor |
| Outage 下界 | 紧（2-5x） | P_out 接近 1，低界接近实际 BER |

低 SNR 特征：上界和 outage 下界都较紧，floor 下界因远未收敛而极松。上界/下界比 ~5-50x。

### 3.2 中 SNR (10-25 dB)

| 界类型 | 松弛倍数 | 原因 |
|--------|---------|------|
| Q 指数上界 | ~4-6x | 指数近似偏离增大 |
| BER floor 下界 | 1.5-10x（取决于 sigma_phi） | 开始向 floor 收敛 |
| Outage 下界 | 10-50x | P_out 快速下降 |

中 SNR 特征：三种界的紧致度中等。若 sigma_phi >= 10deg，floor 在 25 dB 附近已收敛，上界/下界比 ~5-10x。

### 3.3 高 SNR (> 25 dB)

| 界类型 | 松弛倍数 | 原因 |
|--------|---------|------|
| Q 指数上界 | ~5-8x | 指数近似在高 SNR 固有松弛 |
| BER floor 下界 | <1.1x（sigma_phi >= 8deg） | 已完全收敛到 floor |
| Outage 下界 | 极松（P_out → 0） | outage 事件极少 |

高 SNR 特征：floor 下界极紧（sigma_phi >= 8deg 时），上界/下界比取决于上界松弛度。在 sigma_phi=10deg、SNR=30 dB 时，上界/下界比 ~2x（优秀）。

### 3.4 趋势总结

```
SNR 增大方向 →
上界松弛倍数:  缓慢增大 (3x → 5x → 8x)
Floor 下界松弛: 快速减小 (极松 → 1.1x → <1.01x)  [sigma_phi >= 8deg]
Outage 下界松弛: 先减小后急剧增大 (紧 → 10x → 极松)
上界/下界比:   先减后增再减 [floor 收敛后由上界主导]
```

最佳上界/下界比出现在 **高 SNR + 大 sigma_phi** 区域，此时 floor 下界已紧收敛，上界虽有松弛但在 dB 尺度上偏差有限（~0.5-1 dB）。

## 4. 本论文界体系与文献基准的对比

### 4.1 本论文的做法

本论文（Ch3）使用 **精确计算路线**，不依赖经典上界/下界近似：
1. FSM 精确 BER（F3.10）：截断误差 < 10^-4（5 项，强湍流 sigma_phi=15deg）
2. MC 蒙特卡洛验证：500k 符号，与 FSM 偏差 < 1%
3. BER floor（F3.11）：渐近分析，作为高 SNR 物理极限

### 4.2 与文献做法的一致性

| 对比维度 | 文献主流做法 | 本论文做法 | 一致性 |
|---------|------------|----------|--------|
| BER 计算 | MGF/Meijer-G 精确闭合形式 | FSM 精确级数 | 一致（均为精确方法） |
| 截断精度 | Simon & Alouini: < 5% (BER>10^-4) | Petkovic FSM: < 10^-4 (5-10 项) | 一致（FSM 更精确） |
| BER floor 验证 | Petkovic 2023: 式(40) 精确渐近 | F3.11 = Q(pi/(4sigma_phi)) | 一致（相同公式） |
| MC 验证精度 | 文献惯例: 10^5-10^6 符号 | 500k 符号 | 一致 |
| 上界近似 | 部分文献用 Q 指数界 | 不使用（精确计算） | 更优 |

### 4.3 本论文界体系的紧致度评价

由于本论文使用精确 FSM 计算，不存在"上界松弛"问题。紧致度评价主要针对：

1. **FSM 截断精度 vs 精确值**：截断误差 < 10^-4（5-10 项），远优于经典上界的 3-8x 松弛
2. **MC vs FSM 精度**：< 1% 偏差，远优于文献中 5% 的常见标准
3. **BER floor 紧致度**：在收敛区域 < 1.1x，属于"优秀"等级

## 5. 量化锚点汇总

| # | 锚点 | 数值 | 来源 | 适用范围 |
|---|------|------|------|---------|
| A1 | Q 指数上界 vs 精确 BER | **3-8x 松弛**（弱→强湍流，20 dB） | Nistazakis et al.; V-05 表 2.5 | SNR 10-30 dB |
| A2 | BER floor 下界 vs 精确 BER | **< 1.1x 松弛**（收敛区域） | Petkovic 2023 式(40); V-06 锚点 A1-A3 | sigma_phi >= 8deg, SNR >= 25 dB |
| A3 | Outage 下界 vs 精确 BER | **10-100x 松弛**（中等 SNR） | Simon & Alouini Ch.5; V-06 锚点 A5-A6 | SNR 15-25 dB |
| A4 | 联合界 vs 精确 BER (QPSK) | **1.2-1.5x 松弛**（高 SNR） | Proakis | BER < 10^-3 |
| A5 | FSM 截断 vs 精确值 | **< 10^-4 绝对误差** | Petkovic 2023 收敛证明 | N >= 5 项 |
| A6 | MC vs FSM | **< 1% 相对偏差** | V-05 锚点 1 | 500k 符号 |
| A7 | 上界/下界比（最优区域） | **< 2x**（高 SNR + sigma_phi>=8deg） | 综合 A1+A2 | sigma_phi >= 8deg, SNR >= 25 dB |

## 6. Phase 2 仿真验证检查清单

- [ ] 锚点 A1: 验证 Q 指数上界松弛倍数在 3-8x 范围内（不同湍流，20 dB）
- [ ] 锚点 A2: 验证 BER floor 收敛后松弛因子 < 1.1x（sigma_phi=10deg，SNR>=25dB）
- [ ] 锚点 A3: 验证 outage 下界松弛因子在 10-100x（中湍流 20dB，P_target=10^-3）
- [ ] 验证弱/强湍流下上界松弛倍数的差异方向：强湍流 > 弱湍流
- [ ] 验证 SNR 增大时 floor 下界收敛趋势：25-30 dB 区间收敛（sigma_phi=10deg）

## 7. 参考文献

1. **Petkovic 2023**, "Error Probability of a Coherent M-Ary PSK FSO System Influenced by Phase Noise", Mathematics 2023, 11, 121 — FSM 方法原始文献，收敛分析（Dirichlet 准则），截断误差上界（式 31-32），SEP floor 渐近公式（式 40）
2. **Simon & Alouini**, "Digital Communication over Fading Channels" — Ch.5 outage 分析与 BER 界，Ch.12 Chernoff 界系统性讨论，MGF 方法精确闭合形式
3. **Proakis**, "Digital Communications" — QPSK BER 联合界（松 ~1.5x），BER floor 经典结果，Markov 不等式方法
4. **Nistazakis et al.**, FSO QPSK BER 上界的 Q 指数界方法（松 3-8x，Meijer-G 闭合形式）
5. **Tsiftsis et al. 2009** (IEEE TWC) — GG 衰落 BER 精确闭合形式（Meijer-G），SIM-BPSK/QPSK
6. **Han et al. 2022** (JLT, doi:10.1109/JLT.2022.3167035) — FSO 系统 outage/BER 联合分析，渐近表达式
7. **V-05**（本系列）— 上界理论调研，Q 指数上界松弛比表
8. **V-06**（本系列）— 下界理论调研，outage 下界松弛因子表

## 8. 结论

1. **经典上界（Q 指数界）在 GG 衰落下松 3-8 倍**，强湍流更松（重尾放大效应）。联合界对 QPSK 在高 SNR 下较紧（1.2-1.5x）。

2. **BER floor 是已知最紧的下界**——在收敛区域（sigma_phi >= 8deg, SNR >= 25 dB）松弛因子 < 1.1 倍。Outage-based 下界松弛 10-100 倍，仅可用于量级估计。

3. **湍流强度主要影响上界松弛度**（弱 3x → 强 8x），对 BER floor 下界影响小（floor 与湍流无关）。

4. **上界/下界比的最优区域出现在高 SNR + 大 sigma_phi**，此时 floor 已紧收敛，比值 < 2x。本论文使用 FSM 精确方法规避了经典界的松弛问题，截断精度远优于文献中 3-8x 的上界松弛。
