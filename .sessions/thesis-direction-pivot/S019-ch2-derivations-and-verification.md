# [S019] Ch2 原创推导完成 + 参数统一 + 独立验证 + 对照实验 + Ch3整合验证

> 2026-05-30 | 推导+验证+实验+整合 | 已完成
> 续接 PROMPT-001（Ch2 系统与信道模型公式推导）
> 2026-05-30 续接：对照实验（压缩后）
> 2026-05-30 续接：Ch3 公式整合 + 三 agent 并行验证

## 目标

完成 PROMPT-001 中两项原创推导，并通过子 agent 独立验证：
1. GG 分布下 $E[1/h^2]$ 的发散性分析
2. 星地链路预算闭合公式

## 记录

### 推导1：$E[1/h^2]$ 发散性分析

**完成内容**（式 2.37–2.43，写入 `formulas-ch2-system-model.md` 第 502–586 行）：
- 从 GG PDF 出发，分析被积函数 $h^{-2}f(h)$ 在 $h\to 0^+$ 的渐近行为
- 利用 $K_\nu(x)$ 小宗量展开，证明 $f(h) \sim C \cdot h^{\min(\alpha,\beta)-1}$
- 收敛条件：$\min(\alpha,\beta) > 2$（式 2.41）
- 矩公式交叉验证一致
- 三档参数判断：弱(4.0,3.0) 收敛 E=12.0；中(2.5,1.8) 发散；强(1.5,0.8) 发散
- 数值验证：截断积分和蒙特卡洛均确认

**核心结论**：中强湍流下 $E[1/h^2]$ 发散，VV 算法固定窗口的理论方差无穷大 → Ch4 自适应机制的理论必然性。

### 推导2：星地链路预算闭合公式

**完成内容**（式 2.44–2.51，写入 `formulas-ch2-system-model.md` 第 590–695 行）：
- 完整推导从发射功率到瞬时 SNR 的闭合公式链
- 典型参数：1550nm, 1W, 10cm/25cm 孔径, LEO 500km
- 链路预算表：天顶 SNR=45.9dB, 30°仰角 SNR=36.7dB
- 湍流影响：强湍流 P1 SNR=-10.4dB, P(SNR<15dB)=9.28%
- 与 MVE 代码交叉验证：MVE 的 0-25dB 范围覆盖深衰落场景

### 三方独立验证（3 个子 agent 并行）

**Agent 1 — h 模型验证**：
- 确认论文采用约定 A（h 直接取 GG 分布值，SNR ∝ h²）
- $N_\text{opt} \propto h^{-4}$ 与 VV 四次方运算自洽
- 收敛条件 min(α,β)>2 正确

**Agent 2 — 链路预算验证**：
- Fernandes 2023 不在本地库，用 Paillier 2020/张岱/王锋替代验证
- SNR 数值完全可复现，与文献量级一致
- 发现：G_t/G_r 表用 η=1 计算，已加注释修正
- D_r=25cm 偏小（文献 40-100cm），对开题保守安全

**Agent 3 — MVE 代码审计**：
- SNR 定义（Es/N0）、GG 归一化均正确
- **关键发现**：MVE 湍流参数物理不自洽（weak (11.6,10.9) 无法由 σ_R² 生成）
- 论文参数 (4.0,3.0)/(2.5,1.8)/(1.5,0.8) 与 Trinh 2017 一致

### 参数统一

将所有活跃文件的湍流参数统一为 (4.0,3.0)/(2.5,1.8)/(1.5,0.8)：
- `sim_prototype.py` — TURB 字典
- `sim_cascade_robustness.py` — TURB1 字典
- `sim_direction_a.py` — TURB 字典
- `symbol-conventions.md` — 湍流分级表
- `formulas-ch3ch4-sync.md` — 参数定义 + 场景配置表
- `material-section-content-cards.md` — 3 处引用 + GG 参数表
- `formulas-ch2-system-model.md` — 增益注释 + 统一说明
- 未修改 `.sessions/` 历史文件

MVE 统一后运行正常，6 步全部 PASS。

### MVE 结果分析与风险识别

统一参数后 MVE 结果变差（预期中——新参数更接近真实湍流）：
- 中湍流 CMA 发散（err=18.3）
- Step6 端到端：est+VV (0.144) 比 est-only (0.103) 更差——VV 在有估计噪声时帮倒忙
- Step5 对照：用真实 h 补偿后 VV 有效（AWGN: 0.42→0.00）

**结论**：瓶颈在信道估计精度而非自适应窗口。Ch4 的自适应公式在给定准确 h 时有效，但需要 Ch3 的估计器提供足够精度。

## 决策引用

- 无新 D### 决策（参数统一是执行层面的修正）

## 范围确认

- 本轮在 scope boundary 内：完成 PROMPT-001 要求的两项推导 + 验证 + 参数统一

## 后续

- **待做**：论文正文中需明确声明 h 的物理含义约定（GG 分布信道增益，SNR ∝ h²）
- **待做**：D_r 可能需要从 25cm 调至 40cm（与文献一致），但不紧急
- **待做**：PROMPT-002/003（Ch3/Ch4 推导）

### 对照实验（压缩后续接）

**目标**：分离"估计瓶颈"和"自适应瓶颈"——用真实 h 做补偿 + VV，确认自适应窗口在完美 CSI 下的改善。

**实验设计**（5 条件，三档湍流 × 5 SNR × 30 trials）：
- A: |LS est| 幅度补偿 → 解调（无 VV）
- B: |LS est| 幅度补偿 → 固定窗口 VV → 解调
- C: 真实 h 补偿 → 解调（无 VV）
- D: 真实 h 补偿 → 固定窗口 VV → 解调
- E: 真实 h 补偿 → 自适应 VV（h^8 加权滑动平均）→ 解调

**关键修正**：
1. LS 估计 `h_est = rx[pilot]/pilot` 实际估计了 `h·exp(jφ)`（含载波相位），直接除以 h_est 隐式完成载波补偿。修正为 `|h_est|` 纯幅度估计，保证 A 和 C 的公平对比。
2. 自适应窗口从"分块变窗长"（相位解缠绕断裂）改为"|h|^8 加权滑动平均"（全局卷积，无边界问题）。

**结果 @ 20dB**：

| 条件 | 弱 | 中 | 强 |
|------|------|------|------|
| A: est-only | 0.333 | 0.337 | 0.359 |
| B: est+VV | 0.077 | 0.175 | 0.263 |
| C: true-h | 0.333 | 0.337 | 0.359 |
| D: true+VV(fix) | 0.089 | 0.162 | 0.261 |
| E: true+VV(adapt) | 0.075 | 0.119 | 0.212 |

**关键发现**：
1. **A = C（est penalty = 0 dB）**：8 符号导频间距的 LS 幅度估计与真实 h 完全等价——估计不是瓶颈。
2. **VV 有效（B < A, D < C）**：固定 VV 在三档均显著改善，弱湍流最佳（5.7 dB）。
3. **自适应 VV 优于固定 VV（E < D）**：h^8 加权在三档均有效——弱 0.7 dB、中 1.3 dB、强 0.9 dB。中湍流增益最大。
4. **B ≈ D（est+VV ≈ true+VV）**：因为 A=C，est 和 true-h 下 VV 表现一致。

**核心结论**：自适应 VV 机制有效，增益来源是降低深衰落样本的权重（|h|^8），而非窗口长度调整。论文 Ch4 的理论必然性（E[1/h²] 发散）得到实验验证。

### Ch3 公式整合 + 三 agent 并行验证

**整合工作**：将 S002（另一对话）的新 Ch3 推导整合为正式公式文件 `formulas-ch3-link-performance.md`（~280 行，F3.1-F3.21）。

**三个子 agent 并行验证结果**：

**Agent 1（数学正确性）**：21/21 公式全部 PASS。
- 2 个数值问题：F3.18 表格 3/4 行 $\sigma_\phi$ 上限有误；F3.19 惩罚 4.0 vs 4.21 dB（方法差异）

**Agent 2（文献交叉验证）**：
- Petkovic 2023 下载失败，Eq.14/19 编号无法核实
- Hu 2025 (JPHOT) 完全不在库里，bib 里的 `hu2025` 是另一篇论文
- material-section-content-cards.md 2.2.3/4.2.2 写的 $\gamma=\bar\gamma \cdot h^2$ 与新 Ch3 矛盾

**Agent 3（物理一致性）**：**致命发现——跨章 SNR 约定不一致**

| 章节 | SNR 约定 | 来源 |
|------|---------|------|
| Ch2 链路预算 | $\gamma \propto h^2$ | S019 |
| Ch4 自适应公式 | $\gamma \propto h^2$ → $N_{opt} \propto h^{-4}$ | R016 |
| **新 Ch3** | **$\gamma = \bar\gamma \cdot h$** | S002 |

相干检测物理上 $\gamma \propto h$ 正确（GG 建模辐照度，信号幅度 $\propto \sqrt{h}$，SNR $\propto h$）。但 Ch2/Ch4 用的 $\gamma \propto h^2$ 是 IM/DD 约定。影响：
- Ch4 的 $N_{opt} \propto h^{-4}$ 在相干模型下应为 $\propto h^{-2}$
- F3.21 "$B_L \propto h$ 与 $\gamma \propto h$ 抵消"在 $\gamma \propto h^2$ 下不成立
- 所有仿真代码需统一约定
- E[1/h²] 发散性论证：相干模型下应用 E[1/h]，收敛条件 min(α,β)>1，中湍流(2.5,1.8)收敛，仅强湍流发散——论证弱化

**已决策（D010）**：全文统一为 $\gamma \propto h$（相干检测），修改 Ch2/Ch4，保持 Ch3 不动。

**决策依据**：
1. Ch3 已经是 γ∝h 且 280 行公式验证通过，改它要重新推导 Meijer-G 闭合形式——工作量最大
2. Ch2/Ch4 的改动是机械换指数（E[1/h²]→E[1/h]，N_opt∝h⁻⁴→h⁻²），结构不变
3. γ∝h 物理正确，答辩无风险；γ∝h²（IM/DD 约定）对相干检测物理上站不住
4. 论证变弱但可接受：中湍流 (2.5,1.8) 下 E[1/h] 收敛（min=1.8>1），仅强湍流发散。自适应 VV 的实验改善（0.7-1.3 dB）仍成立

**待执行改动**：
- Ch2：E[1/h²]→E[1/h]，发散条件 min(α,β)>2→>1；链路预算 γ∝h²→∝h
- Ch4：N_opt∝h⁻⁴→h⁻²，VV 权重 h⁸→h⁴，M_opt/B_L 指数相应调整
- 仿真代码：γ = γ̄·h² → γ̄·h，权重指数改，重跑实验
- Ch3：不动

### D010 执行前审计：3 个子 agent 跨维度扫雷

> 2026-05-30 续接：物理模型 / 仿真代码 / 公式链 三个 agent 并行审计

**致命级（4 项）**：

| # | 问题 | 影响 |
|---|------|------|
| F1 | `awgn(tx*h, snr)` 噪声功率固定、信号功率∝h²，物理上就是 IM/DD 模型。**4 个时域仿真全部受影响**（prototype/direction_a/cascade/control） | 改 γ∝h 不只是换指数，信号+噪声生成方式要重设计，全部实验重跑 |
| F2 | `sim_ch3_ber_bounds.py` 仍用 h² 计算 SNR，与同目录 closed_form（用 h）直接矛盾 | BER 数值错误 |
| F3 | BER floor 定义混用：bounds 用 `2·Q(...)`（SER），其他用 `Q(...)`（BER），差 2 倍 | 设计结论偏差 ~3dB |
| F4 | Ch2 推导 2 链路预算 (2.44)-(2.51) 全部基于 h²，数值表（天顶 45.9dB 等）需重算 | 链路预算数据作废 |

**严重级（7 项）**：

| # | 问题 |
|---|------|
| S1 | VV unwrap 公式 3 文件写法不同：cascade `*4/4` 抵消退化，control `/M*M` 退化。应统一为 `unwrap(angle*M)/M` |
| S2 | 激光线宽：strengthening 100kHz vs 其他 10kHz，差 10 倍，影响 DPLL B₀ |
| S3 | 符号率：precomp 1 Gsps vs 其他 2.5 Gsps |
| S4 | 湍流参数：precomp/cascade_exp2 用 (2.0,2.0)/(4.0,4.0)，未同步 Trinh 参数 |
| S5 | 旧 Ch3 公式文件 `formulas-ch3ch4-sync.md` F3.14 参数表仍是旧参数，未标注废弃 |
| S6 | Ch4 VV M_opt 应为 (γ̄h)^{-1/5} 非 (γ̄h²)^{-1/5}；FOE N_opt 中 h⁴ 物理来源需重新表述 |
| S7 | Ch2 噪声模型 F14→F15 跳跃太大，缺"LO 噪声主导→AWGN 成立"过渡说明 |

**轻微级（4 项）**：多普勒光频/电域描述模糊、激光线宽 10kHz 偏实验室参数、F4.8 LaTeX 括号错误、awgn() 缺 SNR 含义注释。

**关键判断**：

1. **F1 是最大隐藏坑**：D010 执行范围比预估大——不是"改指数+重跑"，而是信号模型要重新设计。`awgn(tx*h, snr)` 产生的是 γ̄·h²（IM/DD），改成 γ̄·h 需要重新设计噪声生成方式
2. **MVE 数据全部需要重跑**：S011(5/6 PASS)、S015(STRONG PASS) 的数值作废，但框架结论（自适应结构有效）应不变
3. **ber_bounds.py 和 closed_form.py 互相矛盾**：同一目录下两个文件对 SNR 定义完全相反，不能同时引用

### 12-agent 文献验证（Batch 1-2 已完成）

> 2026-05-30 续接：12 个 agent 分 4 批文献验证，Batch 1-2 已完成（6/12）

#### Batch 1：物理模型根基（3 agent）

**Agent 1（SNR 约定）**：文献一致确认 γ∝h（相干）vs γ∝h²（IM/DD）。
- Petkovic 2023 公式(2)：γ = I·C_c（线性），引用 Ansari 2016
- 王敏艳 2026：统一公式 γ = μ_r·h^r，r=1（相干）r=2（IM/DD）
- Colavolpe（DLR）：相干 eq.(5) Y=√H·P·X+W，IM/DD eq.(1) Y=H·P·X+W
- **结论**：γ∝h 对相干检测正确，零争议

**Agent 2（GG 分布 h 含义）**：
- Al-Habash 2001 原文："I denotes irradiance (intensity)"
- E[I]=1 归一化确认，h = I/E[I] = 归一化辐照度
- α = 有效大尺度散射单元数，β = 有效小尺度散射单元数
- 闪烁指数 σ_I² = 1/α + 1/β + 1/(αβ)

**Agent 3（噪声模型）**：确认相干检测 AWGN 合理，LO 散粒噪声主导→噪声与信号解耦。
- **关键发现**：Colavolpe eq.(5) 明确信号模型 Y = √(p·H)·P·X + W
- 即相干检测中信号幅度 ∝ √h（√辐照度），不是 ∝ h
- **仿真应为 `rx = tx * sqrt(h) + noise`，不是 `tx * h + noise`**

**Batch 1 核心结论**：信号模型有三层要改（不仅是 SNR 指数）：

| 层 | 当前（错） | 应改为 |
|---|-----------|--------|
| 信号 | rx = tx·h + noise | rx = tx·√h + noise |
| SNR | γ = γ̄·h² | γ = γ̄·h |
| VV 四次方 | (√h)⁴ = h² | SNR₄ ∝ h²（因(√h)⁴=h²） |

#### Batch 2：Ch2 公式验证（3 agent）

**Agent 4（E[1/h²] 发散性）**：**意外结论——如果 h 是辐照度且信号模型是 r=h·s+n，则 E[1/h²] 分析正确**。
- VV 四次方后精确推导：Var(θ̂) = 1/(4Mγ̄h²)
- E[Var(θ̂)] ∝ E[1/h²]，收敛条件 min(α,β)>2
- **但**：如果改信号模型为 r=√h·s+n（物理正确），瞬时 SNR=γ̄·h，VV 方差 ∝ 1/(γ̄h)，则 E[1/h]，条件 min>1
- **关键**：发散性分析的正确性取决于信号模型的选择，而信号模型的选择取决于 h 的物理定义

**Agent 5（链路预算）**：
- 天线增益/自由空间损耗/大气透射率——全部正确，不用改
- 式(2.44)/(2.50)/(2.51) 的 h²→h 需要改
- 晴空 SNR 数值（45.9dB）不受影响（h=1 时无差异）
- 步骤9 湍流瞬时 SNR 分布表需重算

**Agent 6（GG 参数 Cn² 映射）**：
- 三档参数闪烁指数：弱 0.583/中 0.956/强 2.083——分类正确
- **重要发现**：Andrews 公式不可能产生 β<2.27 的参数！中/强湍流参数超公式范围
- 建议论文标注"参数取自文献[Trinh 2017]"而非"由 Andrews 公式计算"
- β<1 在 GG 数学定义内合法（Al-Habash 2001 确认），但不在 Andrews 解析公式范围内

**核心矛盾**：所有问题归结为信号模型 `r = h·s + n` 还是 `r = √h·s + n`。这决定了一切指数。Batch 3-4 待继续。

#### Batch 3：Ch3 公式验证（3 agent）

**Agent 7（BER 闭合解）**：全部公式与 Petkovic 2023 一致，γ∝h 正确嵌入 Meijer-G 系数。
- F3.5 条件 BER、F3.6 Fourier 系数、F3.8 SEP、F3.10 精确 BER、F3.11 BER floor——全部 PASS
- F3.10 精确 BER 的积分 $\int_{-3\pi/4}^{\pi/4}\cos(n\psi)d\psi = (2/n)\sin(n\pi/2)\cos(n\pi/4)$ 手算验证通过
- γ∝h 在 Meijer-G 闭合形式中已正确处理（Petkovic Eq.(2) 确认 γ=I·C_c）
- F3.18 表格 4 行中 3 行 σ_φ 上限数值偏小（设计偏保守，不致命）

**Agent 8（BER floor + 中断概率）**：
- BER floor $Q(\pi/(4\sigma_\phi))$ 正确：Hu 2025 Eq.(35) 独立确认，Petkovic Section 3.4 也确认
- 中断概率 $P_{out} = F_{GG}(\gamma_{th}/\bar\gamma)$ 推导链无懈可击
- **"SNR 惩罚与湍流无关"是代数恒等式**：9 组（3 湍流×3 P_out）spread=0.00 dB
- **F3.19 数值问题**：P_target=10⁻⁵ 声称 6.84 dB，精确值 8.91 dB（梯形积分 N_phi=150 精度不足）
- 修复：N_phi 从 150 提高到 1000 或改用 scipy.integrate.quad

**Agent 9（DPLL 抵消论证）**：
- 抵消数学正确：$\sigma_\phi^2 = B_0 h T_s/(2\bar\gamma h) = B_0 T_s/(2\bar\gamma)$，$h$ 精确抵消
- **关键发现：$B_L \propto h$ 不是 Wiener 最优！** Wiener 最优给出 $B_L \propto \sqrt{h}$，此时抵消不成立
- 论文应明确 $B_L \propto h$ 是设计选择（实现抵消），非物理最优
- $\sigma_\phi^2 = B_L T_s/(2\gamma)$ 中的因子 2 需标注 SNR 定义（单边/双边），Paillier 2020 CRB 公式无此因子
- B₀ = √(π·Δν_L·γ̄/T_s) 来源为 R016 内部推导，推导过程不在本地
- "BER ratio = 1.000" 严格 > 1（Jensen 不等式），MC 精度内不可区分，建议改为 "<1.01"

**Batch 3 核心结论**：Ch3 公式体系数学正确，但有两个数值问题（F3.18 表格、F3.19 惩罚值）和一个定位问题（$B_L \propto h$ 是设计选择非最优）。

#### Batch 4：Ch4 + 仿真信号模型（3 agent）

**Agent 10（VV 四次方 SNR）**：
- 模型 B（r=√h·s+n）下确认：SNR₄ = γ̄·h/8（不是 h⁴/8）
- VV 方差 = 1/(2Mγ̄h)，需要 E[1/h]，收敛条件 min(α,β)>1
- 中湍流(2.5,1.8)：min=1.8>1，E[1/h]收敛（值=3.75，等效 SNR 损失 ~5.7 dB）
- 强湍流(1.5,0.8)：min=0.8<1，E[1/h]发散
- **发现 R016 代数错误**：噪声功率 16h⁶σ² 误简为 8h⁴/γ̄（应为 8h⁶/γ̄），导致模型 A 下 SNR₄ 也算错（γ̄h⁴/8 应为 γ̄h²/8）

**Agent 11（DPLL + FOE 自适应公式）**：

| 模块 | 模型 A（当前） | 模型 B（正确） |
|------|-------------|-------------|
| FOE N_opt | 80/(γ̄·h⁴) | **80/(γ̄·h)** |
| VV M_opt | (γ̄h²)⁻¹/⁵ | **(γ̄h)⁻¹/⁵** |
| DPLL B_L | B₀·h | **B₀·√h**（Wiener 最优） |

- B₀ = √(πΔν_Lγ̄/T_s) ≈ 89 MHz，远超 clip 上限 20 MHz——自适应在大部分工况下被截断
- 需修改公式文件 F3.1/F3.5/F4.5/F4.6/F4.9/F4.10/F4.14

**Agent 12（FSO 相干仿真文献调研）— 解决性发现**：
- 所有文献确认物理信号 `y = √(ηh)·x + n`，瞬时 SNR = γ̄·h（线性）
- **但**：等效基带模型可重定义 h'=√h（幅度），使 r=h'·s+n 成立，h'²=h ~ GG
- Petkovic 2023 Eq.(1) 信号 ∝ √I，但 SNR=I·C_c（跳过 √h，直接在 SNR 层面操作）
- Hu 2025 Eq.(1) 明确写 y=(ηh)^{1/2}·x+n，SNR=ηh/N₀
- **Ch3 闭合解代码 `gamma = snr_lin * h` 正确**——不需要显式写 √h
- 时域仿真 `rx = tx * h + noise` 中 h 实际是 h'（幅度），h'² = h（辐照度）~ GG

### 12-agent 全局定论

**核心结论：问题归结为 h 的定义声明，而非公式重写。**

| 方案 | h 定义 | 信号模型 | SNR | VV 方差 | E[1/h^n] | 代码改动 |
|------|--------|---------|-----|---------|----------|---------|
| A | h=辐照度 | r=√h·s+n | γ̄·h | ∝1/h | E[1/h], min>1 | 大（加√h） |
| B | h=幅度(h²=辐照度) | r=h·s+n | γ̄·h² | ∝1/h² | E[1/h²], min>2 | 无（当前代码） |

**Agent 12 的发现提供了第三条路**：
- 声明 h = "等效基带信道系数"（幅度），h² 服从 GG 分布
- 信号模型 r = h·s+n 自然成立（h 是幅度，直接乘符号）
- SNR = γ̄·h² 保持不变（代码不用改）
- E[1/h²] 分析保持不变（中/强湍流发散，论证最强）
- **只需在 Ch2 加一段声明，明确 h 的物理含义和与 GG 分布的关系**

**但**：此方案下 DPLL 抵消论证需要调整——γ=γ̄·h² 下 B_L∝h 不再精确抵消（需要 B_L∝h² 才抵消），而 Wiener 最优给出 B_L∝h（不是 h²）。

**待用户决策**：选择哪个方案。三个方案的权衡：

| | 物理严谨性 | 论证强度 | 代码改动 | 答辩风险 |
|---|-----------|---------|---------|---------|
| A（h=辐照度） | 最高 | 弱化（中湍流收敛） | 大（√h+全部重跑） | 低 |
| B（h=幅度） | 中（GG 本是辐照度分布） | 最强（中湍流发散） | 无 | 中（需解释为何 h~GG） |
| Agent12 路（h=等效基带系数） | 中 | 强 | 无 | 中（同上） |

### 仿真修复执行（3 agent 并行）

> 2026-05-30 续接：用户选择方案 A，派 3 个 executor 并行修复 5 个仿真文件

#### 决策 D011：选择方案 A

**决策**：统一为 h=辐照度（方案 A），信号模型 r=√h·s+n，SNR=γ̄·h。

理由：
1. 相干 FSO 文献主流约定（Petkovic 2023, Zedini 2014, Trinh 2024）
2. Ch3（最复杂推导）已正确使用 γ=γ̄·h，无需修改
3. 物理透明——审稿人不会质疑
4. 代码改动是机械操作（加 √h + 改噪声生成）

#### 修复范围

6 个文件中 5 个需修复，1 个已正确：

| 文件 | 状态 | 改动 |
|------|------|------|
| sim_prototype.py | 需修 | 8 处 `tx*h` → `tx*√h` |
| sim_ch3_ber_bounds.py | 需修 | 2 处 `γ=γ̄·h²` → `γ̄·h` |
| sim_ch3_precomp.py | 无需改 | 内部已用 h=√I，物理等价正确 |
| sim_cascade_robustness.py | 需修 | 信号生成 + MMSE 均衡器 |
| sim_control_experiment.py | 需修 | 信号生成 + VV 补偿 |
| sim_direction_a.py | 需修 | 信号生成 + 3 个自适应公式 |
| sim_ch3_ber_closed_form.py | 不动 | 已正确 |
| sim_ch3_strengthening.py | 不动 | 已正确 |

#### 修复结果

3 个 executor 并行执行，全部完成。

**Agent 1（prototype + ber_bounds + precomp）**：

sim_prototype.py：
- 8 处改动：Step2-6 所有信号生成 `tx*h` → `tx*√h`，定义 `h_eff = np.sqrt(h)`
- MLP 训练目标从 `ht[pidx]` 改为 `h_eff[pidx]`（估计的是幅度系数，不是辐照度）
- 运行 5.0s PASS，BER 合理（AWGN 0.5→~0，GG raw ~0.3，Est+VV 0.06）

sim_ch3_ber_bounds.py：
- 2 处：`gamma = snr_lin * h**2` → `snr_lin * h`
- 运行 PASS，BER floor theory 2.70e-3 vs MC 2.73e-3（完美匹配）

sim_ch3_precomp.py：无需修改。内部变量 h = √I（幅度），SNR = I·snr_lin = γ̄·irradiance，物理正确。

**Agent 2（cascade + control）**：

sim_cascade_robustness.py：
- Exp1：信号 `tx*√h*exp(jφ)` + 恒定噪声方差 `1/(2γ̄)`，替换 awgn
- MMSE 均衡器：`rx*conj(√h)/(h+1/γ̄)`（信道系数 √h，|coeff|²=h）
- Exp2：无需改（已用辐照度 SNR）
- 运行 12.4s，H006 判定 STRONG PASS 6/6，自适应 DPLL 弱湍流增益 12.9 dB

sim_control_experiment.py：
- 信号 `tx*√h*carrier` + 恒定噪声，补偿 `rx/√h`（除信道系数非辐照度）
- VV 自适应加权用 √h 非 h
- 运行 PASS，VV 增益弱湍流 7.2 dB / 强湍流 4.7 dB

**Agent 3（direction_a）**：

sim_direction_a.py（28K，最复杂）：
- 3 处信号生成：`awgn(tx*h*carrier)` → 显式 `signal=tx*√h*carrier` + `noise_var=1/(2γ̄)`
- MMSE 均衡器修正（信道系数 √h，|coeff|²=h）
- 自适应公式更新：

| 公式 | 旧（IM/DD） | 新（相干） |
|------|------------|-----------|
| FOE N_opt | 80/(γ̄·h⁴) | 80/(γ̄·h²) |
| VV M_opt | (γ̄·h²)^(-1/5) | (γ̄·h)^(-1/5) |
| DPLL B_L | B₀·h | B₀·h（不变，设计选择注释） |

- 修复 block 级 BER 计算的预存在 shape mismatch bug
- 运行 PASS，新模型 BER 全面优于旧模型（e.g. trial 0: 0.394→0.221）

#### 修复后全局约定一致性

| 文件 | h 含义 | 信号 | SNR | 噪声 | 状态 |
|------|--------|------|-----|------|------|
| sim_prototype.py | 辐照度 | tx·√h | γ̄·h | awgn(已验证正确) | ✅ |
| sim_ch3_ber_bounds.py | 辐照度 | N/A（解析） | γ̄·h | N/A | ✅ |
| sim_ch3_precomp.py | 幅度(√I) | tx·h | γ̄·I=γ̄·h² | 恒定 | ✅ |
| sim_cascade_robustness.py | 辐照度 | tx·√h | γ̄·h | 恒定 | ✅ |
| sim_control_experiment.py | 辐照度 | tx·√h | γ̄·h | 恒定 | ✅ |
| sim_direction_a.py | 辐照度 | tx·√h | γ̄·h | 恒定 | ✅ |
| sim_ch3_ber_closed_form.py | 辐照度 | N/A | γ̄·h | N/A | ✅ |
| sim_ch3_strengthening.py | 辐照度 | N/A | γ̄·h | N/A | ✅ |

**残留问题**：
1. ~~sim_prototype.py awgn 问题~~：已验证自定义 awgn 函数用固定噪声方差（非信号功率自适应），`awgn(tx*√h, snr)` 给出瞬时 SNR=γ̄·h，无需修改。
2. sim_direction_a.py 的 DPLL 跟踪 + 自适应参数触底问题是 PROMPT-009 已识别的遗留问题。
3. 模拟参数未统一（线宽 10/100kHz、符号率 1/2.5 Gsps、湍流参数），待后续统一。

### 公式文件修复（2 agent 并行）

> 2026-05-30 续接：修复 Ch2/Ch4 公式文件，统一 γ=γ̄·h 约定

#### formulas-ch2-system-model.md（8 处）

- 文件开头新增 h 定义声明：h=辐照度~GG，r=√h·s+n，γ=γ̄·h，噪声恒定
- 推导2 链路预算：5 处 h²→h
  - 式(2.44)：`h_total = h_l·h²` → `h_l·h`
  - 式(2.50)/(2.51)：最终因子 `T_atm·h²` → `T_atm·h`
  - 说明文字：`h²为湍流衰落因子` → `h为湍流衰落因子（归一化辐照度，GG分布）`
  - 步骤9：`瞬时SNR = 晴空SNR × h²` → `× h`
- 推导1 重构（3 处）：
  - 目的段落：从"E[1/h²]发散→自适应必然性"改为"E[1/h]性能退化+动态范围→自适应"
  - 步骤5 表格新增 E[1/h] 列：弱 1.17 / 中 3.75 / 强 +∞（β=0.8<1 发散）
  - 核心结论重写：E[1/h] 收敛但值大（弱 0.7dB / 中 5.7dB 等效 SNR 损失），强湍流发散；瞬时 SNR 动态范围 56dB，固定参数无法全范围优化
  - 步骤1-4 的 E[1/h²] 数学推导本身正确，未修改

#### formulas-ch3ch4-sync.md（14 处，12 个位置）

- 旧 Ch3 添加废弃声明（F3.1-F3.14 使用旧约定，新 Ch3 见 formulas-ch3-link-performance.md）
- F3.1：`h[k]·s[k]` → `√h[k]·s[k]`，说明 h=辐照度，√h=幅度系数
- F3.5：`γ̄·|h[k]|²` → `γ̄·h[k]`
- F3.11：MMSE 分母 `|ĥ|²+1/γ̄` → `ĥ+1/γ̄`（信道系数 √h，|coeff|²=h）
- F3.13：`BER(γ·|h|²)` → `BER(γ̄·h)`
- F4.5：`SNR₄ = γ̄·h⁴/8` → `γ̄·h/8`
- F4.6：`N_opt = 80/(γ̄·h⁴)` → `80/(γ̄·h²)`，参数示例重算
- F4.9：`(γ̄·h²)^{-1/5}` → `(γ̄·h)^{-1/5}`，h 依赖 h⁻²/⁵→h⁻¹/⁵
- F4.10：添加"B₀·h 是设计选择（实现h抵消），非Wiener最优（B₀·√h）"注释
- F4.14 表格+代码块+依赖图全部同步更新

#### 决策引用

- D011：选择方案 A（h=辐照度，γ=γ̄·h），理由见上（新建）

#### 后续

1. ~~修复 sim_prototype.py 的 awgn~~ — 已验证正确，无需修改
2. ~~更新 Ch2 公式文件~~ — 已完成
3. ~~更新 Ch4 公式文件~~ — 已完成
4. ~~标记旧 Ch3 公式~~ — 已在 formulas-ch3ch4-sync.md 添加废弃声明
5. ~~统一仿真参数~~ — 已完成
6. ~~修复 R016 代数错误~~ — F4.5 已在公式文件中更新为正确值 SNR₄=γ̄·h/8
7. ~~修复 F3.18/F3.19 数值~~ — 已完成

### 仿真参数统一（1 agent）

> 2026-05-30 续接

3 个文件 4 处参数不一致修复：

| 文件 | 参数 | 旧值 | 新值 |
|------|------|------|------|
| sim_ch3_strengthening.py | LASER_LW | 100 kHz | **10 kHz** |
| sim_ch3_precomp.py | R_SYM | 1 Gsps | **2.5 Gsps** |
| sim_ch3_precomp.py | GG params | (4.0,4.0)/(2.0,2.0)/(1.5,1.5) | **Trinh** |
| sim_cascade_robustness.py | TURB2 GG | (4.0,4.0)/(2.0,2.0)/(1.5,1.5) | **Trinh** |

全部 8 个仿真文件参数现在一致：线宽 10kHz、符号率 2.5 Gsps、Trinh 湍流参数。

### F3.18/F3.19 数值修复（1 agent）

**F3.18 σ_φ 上限表**：4 行全部用 `Q⁻¹(P_target)` 精确重算。主要变化：10⁻³: 18.2°→14.6°, 10⁻⁵: 9.1°→10.6°, 10⁻⁶: 7.3°→9.5°。

**F3.19 设计表**：σ=10° 列 SNR 值用 `scipy.integrate.quad` 精确重算，弱/中/强分别 +0.2 dB 修正。

**F3.20 SNR 惩罚**：关键修正 P_target=10⁻⁵ 从 6.84→**8.91 dB**（原梯形积分 N_phi=150 精度不足）。10⁻³/10⁻⁴ 也有小幅修正。

**R016 代数错误**：F4.5 已在 formulas-ch3ch4-sync.md 中更新为正确值 SNR₄=γ̄·h/8。原推导中的 16h⁶σ²→8h⁴/γ̄ 错误已绕过，完整正确推导待补充（已在缺失项列表中）。

### 最终验证清单

以下为 D011 执行后的完整检查清单：

**仿真代码（8 文件）**：
- [x] sim_prototype.py：√h + awgn(固定噪声方差) ✅
- [x] sim_ch3_ber_bounds.py：γ=γ̄·h ✅
- [x] sim_ch3_precomp.py：参数统一 ✅
- [x] sim_ch3_ber_closed_form.py：原本正确 ✅
- [x] sim_ch3_strengthening.py：线宽 10kHz ✅
- [x] sim_cascade_robustness.py：信号√h + MMSE + Trinh参数 ✅
- [x] sim_control_experiment.py：信号√h + VV补偿 ✅
- [x] sim_direction_a.py：信号√h + 自适应公式 + 恒定噪声 ✅

**公式文件（4 文件）**：
- [x] formulas-ch2-system-model.md：h定义声明 + 推导1重构 + 推导2 h²→h ✅
- [x] formulas-ch3-link-performance.md：F3.18/F3.19/F3.20 数值修正 ✅
- [x] formulas-ch3ch4-sync.md：废弃声明 + F3.1/F3.5/F3.11/F3.13 + F4.5/F4.6/F4.9/F4.10/F4.14 ✅
- [x] formulas-ch5-fpga.md：不涉及SNR约定 ✅

**参数一致性**：
- [x] 激光线宽：全部 10 kHz ✅
- [x] 符号率：全部 2.5 Gsps ✅
- [x] 湍流参数：全部 Trinh (4.0,3.0)/(2.5,1.8)/(1.5,0.8) ✅

**已验证**：
- [x] BER floor theory vs MC 匹配（2.70e-3 vs 2.73e-3）
- [x] 自适应增益保持（弱湍流 12.9 dB）
- [x] 新模型 BER 全面优于旧模型

**遗留（非本次 scope，已在其他地方记录）**：
- sim_direction_a.py DPLL 跟踪 + 自适应参数触底（PROMPT-009）
- SNR₄ 完整正确推导待补充（缺失项列表）
- VV unwrap 公式 3 文件写法不统一（S1，非致命）

### 最终验证扫描 + 遗漏修复

> 2026-05-30 续接：验证 agent 扫描发现遗漏

**发现遗漏**：
1. sim_ch3_strengthening.py 4 处 VV 公式仍用旧约定 `(gamma_bar*h²)^{-0.2}`
2. 6 个材料/公式文件仍含旧约定（material-section-content-cards.md, thesis-framework.md, thesis-status.md, formulas-ch5-fpga.md, formulas-ch3ch4-sync.md 缺失项, symbol-conventions.md）

**修复**（2 agent 并行）：

- sim_ch3_strengthening.py：4 处 `(gamma_bar * h**2)**(-0.2)` → `(gamma_bar * h)**(-0.2)`，运行 0.4s PASS
- material-section-content-cards.md：10+ 处 h⁴→h², h⁻⁴→h⁻², h⁻²/⁵→h⁻¹/⁵
- thesis-framework.md：3 处创新点声明
- thesis-status.md：2 处 h 依赖描述
- formulas-ch5-fpga.md：4 处 FOE 公式
- formulas-ch3ch4-sync.md：1 处缺失项列表
- symbol-conventions.md：2 处（grep 额外发现）

**最终 grep 验证**：`毕设/写作材料/` 目录下所有旧模式（h^4/h⁻⁴/h⁻²/⁵/(γ̄·h²)^{-1/5}）为零匹配。**全部 D011 修复完毕。**
