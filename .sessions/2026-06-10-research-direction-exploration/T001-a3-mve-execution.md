# Task Brief: A3 §4a 维度 D（MVE）执行 — 导频前馈 CPE 抗 deep fade 相位失锁

> 来源: S011（A3 MVE 前置准备）+ S009（A3 四维度全过）+ H006 | 产出位置: `explore/a3-pilot-cpe-mve/`
> 日期: 2026-06-17 续 8
> **唯一文档**: 执行方只能拿到本 T001 + 可选读 `papers/_read_notes/cheng2013-papu-original.md`（PAPU 公式）。不要读其他 .sessions/ 文件——必要背景已全部内联在本 T001 中。

## 0. TL;DR（执行方先读）

你在本机 WSL Ubuntu，Python 路径 `~/.venvs/torch/bin/python`（torch 2.11+cu126，numpy/scipy/matplotlib 齐全）。
**你的任务**: 执行 A3 方向的 §4a 维度 D 最小可行实验（MVE）——用最小规模实证验证"导频前馈 CPE 在 deep fade 下相位估计优于 AGC+DPLL，且不触发 cycle slip"这一假设。
**产出**: 写到 `explore/a3-pilot-cpe-mve/`，含主脚本 + 结果 JSON + **自包含 README**（用户硬要求："哪怕完全没有上下文也能进行不同实验代码的整合"）。主对话只接收结果数字。
**最高纪律**:
1. **TL-22 红线**：A3 攻击的是 **deep fade 期间瞬态 SNR 骤降导致的相位估计方差暴增 → PLL 跌破 critical SNR 失锁**，**不是** AO 残留活塞相位。不要把 Paillier §IV-C "turbulent phase negligible" 当成"A3 没东西可做"——那是 AO 校正后、PLL 工作良好的稳态结论；A3 的增量在 deep fade 瞬态。见 §1.4。
2. **TL-20 红线**：跑任何实验前先写理论预期表（§3.5 已给），偏离即查，不要"结果看起来还行就推进"。
3. **TL-25 起飞检查单**（6 条强制）：共享信道 / 重生信道 / 自写（本项目无 common.py 可导入，全部新写在 `a3_channel.py`）/ 基线已优化 / 先写理论预期 / 输出含元数据。逐条确认。
4. **形态对照不锁死**：M1a（时域 frame-header pilot）和 M1b（频域连续 tone）都跑，数据决定。不要预设哪个赢。

## 1. 背景（理解任务必需的，"了解即可不对照评价"）

### 1.1 A3 是什么（一句话）

**A3 = 用导频做前馈 CPE（载波相位估计）替代 VV/AGC+DPLL 后 PLL 的相位估计角色**，幅度补偿仍归 AGC。增量论点（D006）：AGC 放大信号也放大噪声 → deep fade 瞬态 SNR 不改善 → PLL 可能跌破 critical SNR 失锁；前馈导频 CPE 无环路稳定性约束、无 critical SNR 失锁风险。**不是**"导频补幅度衰减本身"（与 AGC 冗余，已排除）。

### 1.2 为什么做 MVE（gw-feasibility §4a 维度 D）

A3 已过分析维度 A0/A'/A/B（S009），最后一道门是维度 D 实证 MVE。gw-feasibility.md 明文"组合新颖性（光纤 pilot CPE 迁移 FSO 湍流）不应跳过 MVE"。MVE 在 baseline 选定前执行，避免在不可行方向浪费复现资源。

### 1.3 信号模型（TL-01 锁定，照搬）

Paillier 2020 §III 离散接收信号（`papers/arxiv/1911.11851/content.md` ~L20300 verified）：

$$s_{RX}(k) = \sqrt{\rho(k)}\cdot \exp\!\big(j(\Delta\omega kT + \varphi_m(k) + \phi(k))\big) + n(k)$$

- $\rho(k)$ = 混合效率（湍流幅度，TURANDOT 波动光学 35 层产出 → σ²_I=0.684）。**MVE 用 Gamma-Gamma 块衰落近似**（见 §2.2 保真度声明）
- $\Delta\omega kT$ = 多普勒残余频偏（Paillier 测到 100 MHz）
- $\varphi_m(k)$ = 调制相位（BPSK: {0,π}；MVE 用 QPSK 或 16-QAM）
- $\phi(k)$ = 湍流相位（AO 校正后，Paillier §IV-C 实证 negligible——但见 §1.4）
- $n(k)$ = AWGN（shot noise 主导，σ² = 1/(2·γ)，γ=Es/N0）

### 1.4 ⚠ TL-22 红线：A3 到底在跟踪什么相位？（必读，否则白跑）

Paillier §IV-C 结论"turbulent phase negligible"是**有条件**的：AO 校正后 + PLL 工作在良好稳态。A3 的攻击点是 **deep fade 瞬态**——σ²_I=0.684 意味着 ρ(k) 偶尔骤降到接近 0，此时：
- 瞬态 SNR = γ·ρ(k) 骤降（可能跌破 PLL 的 critical SNR，Paillier L190 实测 +5dB critical SNR elevation）
- PLL 失锁 → 相位估计方差暴增 → BER 恶化（Paillier L200 实测 2.3 dB power penalty @ BER=1e-4）
- 这个"deep fade 瞬态相位估计恶化"**不是 AO 残留活塞相位**，是 deep fade 期间的相位估计噪声放大

A3 增量：前馈导频 CPE 在 deep fade 瞬态**不依赖环路锁定**（开环），故无 critical SNR 失锁。**MVE 要测的就是这个**——deep fade 瞬态下 pilot CPE vs PLL 的相位估计方差与 BER 差距。

### 1.5 性能间隙（A0-1 实证锚点，[实证]）

- Paillier `content.md:200`：deep fade 致 **2.3 dB power penalty @ BER=1e-4**（AGC+DPLL vs AWGN 理论）[实证]
- Paillier `content.md:190`：critical SNR **+5 dB elevation**（DPLL 锁定门限）[实证]
- Paillier `content.md:206`：结论段**主动呼吁**"open-loop carrier synchronization algorithms should be investigated"[实证]
- 增益预期锚：**Valjus 2025 综述实测 pilot +1dB 量级**（`10.1002/sat.1553`，OSL deep-fade 场景 pilot 比 VV+差分 +1dB）[实证]。**不要锚 Wang 4 支路 +19dB**（那是分集贡献，不是 pilot CPE）

### 1.6 四条边界约束（BC-1~4，MVE 必须处理，gw-feasibility FR-14/15 + D006）

| BC | 内容 | MVE 如何处理 |
|----|------|-------------|
| BC-1 | A3（数字前馈 CPE）须与 PASC 路线（self-coherent 光域共轭补偿）显式区分 | M4 = PASC 数字近似 baseline（FR-15 目标基线）。记录 A3 与 PASC 的差距 |
| BC-2 | VV M-次方盲估计在湍流块边界失效（TL-18: BER 10-13%→27-30%），须 MVE 实证 pilot CPE 不失效 | M3 = VV 盲 CPE，作失效参照。须复现 VV 失效 + pilot 不失效 |
| BC-3 | residual carrier 竞争方案（Deng 2026）纳入 baseline | MVE 阶段实现成本高，用"无 pilot + DPLL"作 residual carrier 近似上界，记录差距（gw-feasibility L136 允许）|
| BC-4 | 前馈 CPE 通用失效 = phase unwrap cycle slip（low SNR + deep fade）。**pilot CPE 不豁免**，须含 PAPU 类应对 + MVE 验证 deep fade 下不触发 | M1a/M1b 含 Cheng 2013 Eq.(5) CS 修正（§3.3 给公式）。须测 cycle slip 率 < VV |

## 2. 任务详情

### 2.1 要回答的问题（MVE 核心假设，一句话）

**在 deep fade（σ²_I=0.684，Paillier §IV-C 条件）下，对比 (a) 时域 frame-header pilot + PAPU vs (b) 频域连续 tone + PAPU vs (c) AGC+DPLL：① pilot CPE 相位估计方差 < AGC+DPLL；② BER 改善 ≥0.5dB；③ cycle slip 不触发（BC-4）；④ 数据决定 A3 pilot 形态选型。**

### 2.2 信道保真度声明（FR-04，方案 B = Paillier 复现）

**用户已选方案 B**：重新生成 σ²_I=0.684 deep fade 时序。

**保真度诚实声明（必写进 README）**：
- Paillier 用 ONERA TURANDOT 波动光学（35 层相位屏 + AO 闭环仿真），**无法精确复现**（专有代码）
- MVE 用 **Gamma-Gamma 块衰落模型近似**：α=1.5, β=0.8（强湍流，σ²_I≈0.684 量级），block size = Paillier 相干时间
- **保留的核心结构属性**（FR-04 关键）：① deep fade 瞬态（ρ 骤降）② 块间相位跳变（VV 失效机制来源）③ 多普勒残余频偏 100 MHz 量级
- **省略项 + 影响**：AO 残留活塞相位（A3 不攻此，§1.4）；精细 AO 闭环动态（用静态 GG 近似）。预判真实化后若 M1 仍 < M2 结论可信，若 M1 失效触发 BC-4 深入

**Gamma-Gamma 参数**（复现 σ²_I≈0.684 量级）：
- strong: α=1.5, β=0.8（σ²_I≈0.684 目标）
- moderate: α=2.5, β=2.0（对照，σ²_I≈0.3）
- weak: α=4.0, β=4.0（对照，σ²_I≈0.1）
- 实现参考（旧方向 `projects/thesis-figures/simulation/sim_kf_stress_common.py` 的 `gg_block`）：
  ```python
  from scipy.stats import gamma as gamma_dist
  def gg_block(N, a, b, bs=BLOCK):
      nb = (N + bs - 1) // bs
      return np.repeat(
          gamma_dist.rvs(a, scale=1/a, size=nb) *
          gamma_dist.rvs(b, scale=1/b, size=nb), bs)[:N]
  ```
  **注意**：这是 block-fading 近似（每 bs symbol 一个常数 h）。Paillier 是逐 symbol 时变，但 deep fade 瞬态结构保留。BLOCK 取 Paillier 相干时间量级（~100 symbol 量级，先试 64）。

### 2.3 五个对比方法（FR-14/15 + 4 BC）

| 方法 | 角色 | 实现要点 |
|------|------|---------|
| **M1a 时域 frame-header pilot + PAPU**（Cheng 2013 Eq.1-5）| 主方法候选 A | frame length L=64，1 pilot header/frame（1.56% overhead）；pilot 用已知 BPSK 训练序列；Eq.(2) 估 pilot 相位 → 插值 → Eq.(5) CS 修正 |
| **M1b 频域连续 tone + PAPU**（Cheng 2013 Eq.5 迁移）| 主方法候选 B | 在频谱边带插连续 pilot tone（不占数据 symbol，但占带宽/功率预算——记录占多少）；N_data→0 极限每 symbol 有 pilot 参考；Eq.(5) 直接用（不需插值）|
| **M2 AGC+DPLL** | FR-14 最强简单先验 | AGC = 幅度归一化（除以 √ρ̂，ρ̂ 用滑窗估）；DPLL = 二阶环（参考旧 `dpll_track`，omega_n/zeta 先网格搜索）|
| **M3 VV 盲 CPE** | BC-2 失效参照（TL-18）| M=4 次方（QPSK）或 M=8（16-QAM），块平均窗 16/32/64；参考旧 `fft_foe` 做频偏估计 + VV 相位估计 |
| **M4 PASC 数字近似** | FR-15 目标基线（BC-1）| PASC = self-coherent 光域共轭补偿。数字近似 = pilot tone + 理想光域共轭（无 PLL，直接用 pilot 相位抵消）。实现简化版：用 pilot tone 估相位后**直接减**（不做 unwrap，不做 PAPU）——近似 PASC 的"光域即时补偿"特性，记录与真 PASC 差距 |

### 2.4 pass/fail 标准（量化阈值，预定义不可后改）

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| 相位方差 | M1a/M1b < M2（deep fade σ²_I=0.684）| Paillier 2.3dB gap |
| BER | M1a/M1b > M2 ≥0.5dB（@ BER=1e-3 或 1e-4）| Valjus +1dB 锚 |
| BC-2 | M3 deep fade 复现失效（BER 10-13%→27-30% 量级，TL-18），M1a/M1b 不失效 | TL-18 |
| BC-4 | M1a/M1b cycle slip 率 < M3，且 deep fade 下 < 1e-2 | Cheng 2013 |
| FR-14 | M1a/M1b > M2（非仅 > M3/无处理）| gw-feasibility |
| FR-15 | M1a/M1b ≥ M4 近似（或记录差距）| gw-feasibility |
| **形态选型** | M1a vs M1b 在 BC-2/BC-4 差异显著→数据定；不显著→默认 M1b（频域 tone，A3 设想 + 非平凡性）| 本任务决策 |

**Go/Conditional-Go/Pivot/Kill 判定**（gw-feasibility §4a 决策表，由主线判定，执行方只报数字）：
- Go = A0通过 + MVE通过（相位方差+BER+BC-2+BC-4 全 PASS）
- Conditional Go = MVE 部分通过（某项退化但有解释和改善路径）
- Pivot = MVE 失败但有调整方向
- Kill = 核心假设无法修复

### 2.5 时间预算

≤1 天。临时脚本，不建正式仿真环境。建议拆成两个子任务（见 §5）。

## 3. 执行方式（具体到公式和步骤）

### 3.1 Cheng 2013 PAPU 完整公式（M1a/M1b 直接用，全部 verified）

**Eq.(1) 信号模型**：`s(k) = c(k)·exp(jθ(k)) + n(k)`，θ 为 Wiener（variance = 2π·Δν·T）

**Eq.(2) Pilot header 相位估计**（M1a）：
$$\hat\phi(m) = \arg\!\Big(\sum_{i=0}^{P-1} d^*(i)\cdot s(m\cdot P + i)\Big)$$
- d*(i) = 第 i 个已知 pilot symbol 复共轭；P = pilot header length
- m = frame index
- 插值得连续参考 $\hat\phi'(k)$（linear 或 zero-order hold）

**Eq.(3)(4) Unwrap 算子**（等价 numpy.unwrap）：
$$\hat\phi^{u}_{k} = \hat\phi^{u}_{k-1} + \text{rng}\cdot f_{\text{rng}}(\hat\phi^{r}_{k} - \hat\phi^{u}_{k-1})$$
$$f_{\text{rng}}(z) = \begin{cases} z & |z|<\text{rng}/2 \\ z+\text{rng} & z<-\text{rng}/2 \\ z-\text{rng} & z>\text{rng}/2 \end{cases}$$
- rng = π/2（QPSK partitioning）

**★ Eq.(5) CS 修正核心公式**（M1a/M1b 都用）：
$$\boxed{\hat\phi^{u}_{k} = \hat\phi^{0,u}_{k} - \text{round}\!\Big[\frac{\hat\phi^{0,u}_{k} - \hat\phi'(k)}{2\pi}\Big]\cdot 2\pi}$$
- $\hat\phi^{0,u}_{k}$ = Eq.(3)(4) 普通 unwrap 后相位（可能带整数倍 2π CS）
- $\hat\phi'(k)$ = pilot 参考（M1a: 插值；M1b: 连续 tone 直读）
- round = 四舍五入到最近整数
- 机制：差 > π/2（round 出 ±1）则 ±2π 修正；差 < π/2（round 出 0）不动

**CS 检测阈值（三层，Cheng 2013 verified）**：
- π/2（round 隐含边界）
- π/3（工程防 false fluctuation）
- π/2（仿真统计检测：估计相位 vs 真值绝对差 > π/2 计为 CS）

### 3.2 M1b 频域连续 tone 实现要点

- 在数据频谱边带加连续单音（如 subcarrier），每 symbol 都能提取相位参考
- $\hat\phi'(k)$ 直接从 tone 的瞬时相位读（不需插值）
- Eq.(5) 直接套用（这是 S011 验证的关键迁移性：Eq.5 symbol-by-symbol，不依赖 pilot 插值形态）
- **功率预算**：tone 占总功率一份，记录占比（如 5%）。M1a 的 pilot header 也占功率（1.56%），公平比较时归一到相同总功率

### 3.3 五方法共享信道（TL-25 #1 强制）

所有方法必须用同一组 (ρ(k), φ_doppler(k), n(k), bits)。写 `generate_shared_realization(Ns, gamma_bar, turb, seed)` 返回 dict，5 方法都吃同一 dict。**禁止各方法自己 np.random**。

### 3.4 baseline 优化（TL-25 #4，TL-14）

- M2 DPLL：omega_n ∈ {1e6, 4e6, 8e6, 1.6e7}，zeta ∈ {0.5, 0.707, 1.0}，网格搜索选 deep fade 下最优
- M3 VV：块平均窗 ∈ {16, 32, 64}，选最优
- **先优化 baseline 再跑主对比**（否则 pilot 增益被低 baseline 虚高，TL-18 教训）

### 3.5 理论预期表（TL-20，跑前先写，偏离即查）

| 指标 | 预期 | 锚点 |
|------|------|------|
| AWGN 下所有方法 | BER ≈ 理论 QPSK BER（无 pilot penalty 时）| Shannon/理论 |
| weak 湍流 | M1a/M1b ≈ M2（无 deep fade，pilot 无增量）| Valjus |
| strong 湍流 | M1a/M1b > M2 约 0.5-1.5 dB | Valjus +1dB / Paillier 2.3dB gap |
| M3 VV | strong 湍流 BER 恶化到 20-30%（TL-18 复现）| TL-18 |
| M3 VV | weak 湍流 ≈ M2（无失效）| TL-18 |
| BC-4 cycle slip | M3 > M1a/M1b（pilot PAPU 应抑制）| Cheng 2013 |
| M1a vs M1b 差异 | 预期不明（数据决定），若接近默认 M1b | 本任务 |
| **异常触发** | 任何方法 BER > 50%（随机猜）= 严重 bug；任何方法 BER 优于 AWGN 理论 = bug；M1 增益 > 5dB = 可疑（超 Valjus 锚）| — |

### 3.6 扫描设计

- 湍流：weak / moderate / strong（3 级）
- γ̄（平均 SNR）：覆盖 BER 从 1e-1 到 1e-4 的范围，建议 [-5, 0, 5, 10, 15, 20] dB（6 点）
- 种子：5 个（seed 42/43/44/45/46），结果报均值±std
- 总运行点：3 × 6 × 5 × 5 方法 = 450 点。先 smoke test 单点确认管道通，再全扫

## 4. 已知陷阱（基于历史失败的具体案例）

1. **TL-22（最高优先级）**：不要把 A3 理解成"补 AO 残留活塞相位"——那是 B1 死因。A3 攻 deep fade 瞬态相位估计恶化。若结果"所有方法 BER 一样，pilot 无用"，**先查信道是否真的有 deep fade 瞬态**（ρ(k) 是否真骤降），而不是结论"pilot 无用"。
2. **TL-18**：VV 在强湍流必须复现失效（BER 恶化）。若 VV 在 strong 湍流表现正常 = 信道没块衰落结构 / VV 实现错了。**这是管道正确性的自检**。
3. **TL-20**：M1 增益若 > 5dB 立即查（超 Valjus +1dB 锚）。最可能原因：M2 baseline 没优化（TL-14）/ 信道不共享（TL-25 #1）/ SNR 惯例错（毕设 σ²=1/(2γ) vs 自洽 σ²=1/γ，参考 N1 MVE 的 bug1）。
4. **SNR 惯例**：用 γ = Es/N0（σ² = 1/γ），与 Shannon 直接对应。**不要**用 γ = Es/2N0（σ² = 1/(2γ)），那会让实际 SNR 翻倍。AWGN uniform BER 须 < 理论值（N1 MVE bug1 教训）。
5. **PAPU 公式别抄错**：Eq.(5) 是 `round[(φ0u - φ')/2π]·2π`，**不是** `round[(φ0u - φ')/π]·π`。抄错会让 CS 修正阈错。
6. **M1b tone 功率预算**：tone 占功率会让数据 SNR 略降。公平比较时 M1a pilot header（1.56%）和 M1b tone（如 5%）归一到相同总功率，否则 M1b 虚高。
7. **cycle slip 统计**：用 Cheng 2013 仿真阈值（估计相位 vs 真值绝对差 > π/2 计 CS）。真值 θ(k) 已知（信道生成时记录），不是估计。
8. **不要把 MVE 当正式仿真**：§4a MVE 是临时验证脚本，结果支撑 §4a 决策即可。代码质量够跑、能复现就行，不追求论文级工程化。

## 5. 执行拆分（应对 ≤900s/子 agent 限制）

本任务单 agent 跑不完（450 点 + 5 方法 + baseline 网格搜索）。**建议拆两阶段**（主线决定是否拆，执行方接到的是某一阶段）：

**阶段 A（信道 + baseline + 管道验证，约 400s）**：
- 写 `a3_channel.py`（generate_shared_realization + gg_block + doppler_phase）
- 写 `a3_baselines.py`（M2 AGC+DPLL 网格搜索 + M3 VV + M4 PASC 近似）
- smoke test：单点（strong, γ=10dB, seed=42）跑 M2/M3/M4，确认 VV 复现失效、BER 物理合理
- 产出：`smoke_results.json` + baseline 最优参数

**阶段 B（主方法 + 全扫描 + 形态对照，约 600s）**：
- 写 `a3_pilot_cpe.py`（M1a frame-header pilot + Cheng 2013 Eq.1-5；M1b 频域 tone + Eq.5）
- 用阶段 A 的信道和 baseline 最优参数
- 全扫描 3 湍流 × 6 γ × 5 seed × 5 方法
- 产出：`a3_mve_results.json` + `README.md`

**若主线只派一个 agent**：让它先跑阶段 A smoke 通过再继续 B，单 agent 内串行。超时则回传已跑部分 + 明确卡在哪。

## 6. 产出格式（强制，给模板）

### 6.1 `explore/a3-pilot-cpe-mve/` 目录结构

```
explore/a3-pilot-cpe-mve/
├── README.md                    # ⭐ 自包含说明（用户硬要求）
├── a3_channel.py                # 信道生成（generate_shared_realization + gg_block + doppler_phase）
├── a3_baselines.py              # M2 AGC+DPLL + M3 VV + M4 PASC 近似
├── a3_pilot_cpe.py             # M1a frame-header pilot + M1b 频域 tone（Cheng 2013 Eq.1-5）
├── a3_mve_main.py              # 主入口：扫描 + 聚合
├── _smoke.py                    # 管道验证（单点）
├── a3_mve_results.json         # 全扫描结果
└── baseline_optimal_params.json # baseline 网格搜索结果
```

### 6.2 `README.md` 必须包含（自包含，无外部上下文）

```markdown
# A3 §4a 维度 D MVE — 导频前馈 CPE 抗 deep fade 相位失锁

## 实验目的
[一句话：验证 pilot 前馈 CPE 在 deep fade 下优于 AGC+DPLL，且不触发 cycle slip]

## 信号模型
[s_RX(k) 公式 + 各项含义，照搬本 T001 §1.3]

## 信道保真度声明（FR-04）
[Gamma-Gamma 近似 Paillier §IV-C，保留/省略项，照搬本 T001 §2.2]

## 五个方法
[M1a/M1b/M2/M3/M4 一句话各 + 角色]

## pass/fail 标准
[照搬本 T001 §2.4 表]

## 运行命令
[自包含：wsl -e bash -c "cd /mnt/d/.../explore/a3-pilot-cpe-mve && ~/.venvs/torch/bin/python a3_mve_main.py"]

## 依赖
[numpy / scipy（gg_block 用 gamma_dist）/ 无外部数据]

## 结果摘要
[跑完后填：strong 湍流 γ=10dB 各方法 BER + cycle slip 率]

## 元数据
[git hash + md5 + 运行时间]
```

### 6.3 `a3_mve_results.json` 结构

```json
{
  "metadata": {
    "git_hash": "<填>",
    "timestamp": "<填>",
    "tl25_checklist": {"shared_channel": true, "regen_channel": true, ...6 条},
    "fidelity_note": "Gamma-Gamma 块衰落近似 Paillier TURANDOT..."
  },
  "results": [
    {
      "turb": "strong", "gamma_db": 10, "seed": 42,
      "M1a": {"ber": 0.xxx, "phase_var": 0.xxx, "cycle_slip_rate": 0.xxx},
      "M1b": {...}, "M2": {...}, "M3": {...}, "M4": {...}
    },
    ...
  ],
  "theoretical_expectation_check": {
    "awgn_uniform_ber_lt_theory": true,
    "vv_strong_turb_degradation_reproduced": true,
    "m1_gain_lt_5db": "<填 true/false + 若 false 原因>"
  }
}
```

## 7. 验收（主线拿到产出后怎么检查）

- [ ] README 自包含（不看 .sessions/ 能理解实验）
- [ ] TL-25 六条 checklist 全 true（metadata 里）
- [ ] AWGN 控制实验：uniform BER < 理论值（SNR 惯例对）
- [ ] VV 在 strong 湍流复现失效（BER 恶化到 20-30% 量级）——管道自检
- [ ] M1 增益 < 5dB（超 Valjus 锚则查 baseline 是否优化）
- [ ] M1a/M1b 都跑了（形态对照，不是单形态）
- [ ] cycle slip 率有数字（BC-4）
- [ ] M4 PASC 近似有数字（FR-15/BC-1）
- [ ] 5 seed 有均值±std
- [ ] 理论预期偏离项有记录（TL-20）

## 8. 附：产出回传位置

`explore/a3-pilot-cpe-mve/` 全部文件 + 主消息回传结果数字摘要（strong 湍流 γ=10dB 各方法 BER + cycle slip 率 + 形态对照结论）。主线据数字做 Go/Conditional-Go/Pivot/Kill 判定。

## 9. 不要做（Dead Ends）

- ❌ 把 A3 理解成补 AO 残留活塞相位（B1 死因，TL-22）
- ❌ 用毕设旧 common.py 的载波恢复代码（那是旧方向，TL-09/TL-13 教训；信道生成可参考但载波恢复必须新写）
- ❌ 只跑 M1b（用户明确要形态对照，数据决定）
- ❌ 跳过 baseline 网格搜索（TL-14，会虚高 pilot 增益）
- ❌ 抄错 Cheng 2013 Eq.(5)（round[(φ0u-φ')/2π]·2π）
- ❌ 各方法自己生成信道（TL-25 #1）
- ❌ 把 MVE 结果当论文级仿真（§4a MVE 是临时验证）
- ❌ 在结果未对齐理论预期时就下结论（TL-20）
