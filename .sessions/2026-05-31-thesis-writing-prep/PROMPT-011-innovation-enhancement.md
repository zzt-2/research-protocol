# PROMPT-011: 创新点增强实验 — 提示词总文档

> 专题: thesis-writing-prep | 优先级: P0
> 创建: 2026-06-02 | 状态: 待审核，未开跑
> 关联: PROMPT-010（后续总提示词）、innovation-points.md（创新点 v5）
> 目的: 逐个对话跑实验，增强 IP1/IP2 的信息量和学术深度

---

## 必读文件（每次实验对话开始时读）

1. **`毕设/master-state.md`** — 全局状态
2. **`毕设/CONCLUSIONS.md`** — 结论注册表（所有数字从这里取）
3. **`毕设/innovation-points.md`** — 创新点 v5 + 被否决方案
4. **`thesis-lessons.md`**（项目根目录）— 教训文档（TL-01~25）
5. **`毕设/design-decisions.md`** — 设计决策（INVARIANT 项不可违反）
6. **`本文件`** — 每个实验的目标、理论预期、代码指引、风险

---

## 背景问题

当前两个创新点面临"退化"风险——结论太 trivial：

- **IP1 (Ch3)**：QPSK 对 CE 误差免疫（C3-02，最大退化 0.12dB），"精度设计准则"退化为"LS 精度就够了"
- **IP2 (Ch4)**：DPLL 固定 ω_n=20×10⁶ rad/s 在所有湍流下接近最优（C4-06），"参数设计准则"退化为"用 DPLL 设 20MHz"

**目标**：通过实验和解析推导，让创新点从"研究半天发现不用设计"变成"揭示了有价值的工程洞察"。

---

## 不可违反的约束（铁律）

从教训文档和设计决策中提取的硬约束：

### 信号模型（TL-01, B02/D15）

```
r = sqrt(h) * s * exp(j*phi) + n
gamma = gamma_bar * h（线性，不是 h²）
h = 实值归一化辐照度（GG 分布，不是复信道系数）
```

### 禁止触碰（否决方向）

| 禁止 | 原因 | 教训 |
|------|------|------|
| "自适应"载波同步 | 物理上无效（准静态信道） | TL-03/06/07 |
| "湍流感知 R 矩阵" | 4 种 R 差异 <13% | X-01, C4-08 |
| 复数 h_est | FSO 中不物理 | X-07, TL-22 |
| BER floor 声称新颖 | B05/B11 锁定为经典结果 | design-decisions B05/B11 |
| "首次"/"填补空白" | 禁忌词 | E01 INVARIANT |
| "oracle CSI" | 禁忌词 | 开题通用规则 |
| KF 统一载波同步路线 | 已被 A06 取代 | design-decisions A06 |
| 增益 >5dB 不经审查就接受 | 强制审查 | TL-12/17/23 |

### 仿真流程铁律（TL-25 起飞检查单）

每个新实验脚本头部必须加：
```
# TL-25 checklist:
# 1. 共享信道: generate_shared_realization → [确认/不适用]
# 2. 重生信道: 改物理参数时重新生成 → [确认/不适用]
# 3. 从 common.py 导入: 不自建核心函数 → [确认]
# 4. 基线已优化: 对比用 FIXED_CFG_OPTIMAL → [确认/不适用]
# 5. 先写理论预期: 见本文件对应实验节 → [确认]
# 6. 输出含元数据: save_results() 保存 → [确认]
```

### 措辞规则

- 创新点用"拟提出/拟建立"，不用"提出了"
- 解析贡献 > 系统性分析 > 场景延伸 > 算法创新（TL-19）
- 不写"最优"精确到单值（C4-06 边界条件）
- h 叫"归一化辐照度"，不叫"信道增益"
- ω_n 单位 rad/s

---

## 实验清单

按优先级排列，每个实验独立成对话。

### 实验 1: 16-QAM NMSE 灵敏度仿真（增强 IP1）

**优先级**: P0（最确定的杠杆）
**目标**: 证明 CE 误差对 QAM 有显著影响，将 IP1 从"没影响"重塑为"调制依赖性"
**类型**: 场景延伸（TL-19 优先级 3）

#### 理论预期（TL-20 强制）

- QPSK 免疫根因：W = sqrt(h)/(h+c) > 0 → sign() 判决对正缩放免疫（C3-02）
- 16-QAM 判决依赖幅度：h_est 误差引入的缩放偏移导致判决边界偏移
- 预期结果：NMSE 0~-20dB 对 16-QAM BER 有渐进影响（NMSE 越差 BER 越高）
- 预期影响量级：NMSE=0dB 时退化可能 1-5dB（幅度判决对缩放敏感），NMSE=-20dB 时退化 <0.5dB
- 量化锚点：如果 16-QAM 下 NMSE=0dB 退化 <0.5dB，则 QAM 也不敏感，增强失败

#### 代码指引

1. **在 common.py 中新增**（不要自建，TL-25 第 3 条）：
   ```python
   def qam16_mod(bits):
       """16-QAM 调制: 4 bits/symbol, 归一化平均功率=1"""
       # Gray mapping: 00→-3, 01→-1, 11→+1, 10→+3
       # 每符号 4 bits: bits[4k:4k+2] → I, bits[4k+2:4k+4] → Q
       ...

   def qam16_demod(s):
       """16-QAM 解调"""
       ...

   def ber_count_qam16(tx_bits, rx):
       return np.mean(tx_bits != qam16_demod(rx))

   def resolve_qam16(rx, tx_bits):
       """QAM 版 resolve: 试 8 个 π/4 旋转取最优（覆盖残余相位模糊）
       注意：如果 FOE 改用导频辅助，残余模糊可能只有 π/2，
       可改为试 4 个旋转。根据实际 FOE 方案调整。"""
       best = 1.0
       for r in np.arange(0, 2*np.pi, np.pi/4):
           b = ber_count_qam16(tx_bits, rx * np.exp(-1j*r))
           if b < best: best = b
       return best
   ```

2. **基于 sim_nmse_turbulence_sweep.py 改写**：
   - 信号生成：`qam16_mod` 替代 `qpsk_mod`
   - 评估：`resolve_qam16` 替代 `resolve_qpsk`
   - ⚠️ **FOE 问题**（确定性问题，不是风险）：`fft_foe` 使用 `rx**4`（4 次方鉴相器），这对 QPSK 有效（恒包络，4 次方消除调制），但 16-QAM 是非恒包络，`rx**4` **不能消除调制**。必须改用其他 FOE 方案：
     - **方案 A（推荐）**：导频辅助 FOE — 在信号前端插入已知导频符号，用导频做频偏估计
     - **方案 B**：差分 FOE — 利用连续符号间的相位差估计频偏
     - **方案 C**：假设 FOE 已完成（oracle FOE）— 简化实验，只关注 NMSE 对 CPR 的影响
   - ⚠️ **CPR 鉴相器问题**：`dpll_track` 和 `vv_cpr` 的鉴相器内部使用 4 次方运算（`rx[k]**4` / `seg**4`），这是 QPSK 专用的。16-QAM 不兼容。解决方案：
     - **DPLL**：改用 DD（判决导引）鉴相器 — 对接收符号做硬判决，用判决结果消除调制。在信噪比足够高时（SNR > 15dB）DD 鉴相器对 QAM 有效
     - **VV**：4 次方鉴相器不适用于 QAM。**实验 1 中不对比 VV**，只对比 DPLL(DD) 和 KF pilot
   - 实验范围调整：对比方法改为 **DPLL(DD)** 和 **KF pilot**（均有 QAM 兼容路径），不对比 VV/BPS

3. **参数空间**：
   ```
   调制: 16-QAM
   湍流: weak, moderate, strong
   SNR: [10, 15, 20, 25, 30] dB（16-QAM 需要更高 SNR）
   NMSE: [-20, -10, -5, 0] dB
   方法: DPLL(DD), KF pilot（VV/BPS 因鉴相器不兼容 QAM，不纳入对比）
   FOE: 导频辅助（方案 A）或 oracle FOE（方案 C，简化）
   种子: 10（range(1000, 1010)）
   ```

4. **输出**：
   - `projects/simulation/results/nmse_qam16_turbulence_sweep.json`
   - 对比 QPSK 数据：同条件下的退化差异

#### 风险与退路

| 风险 | 概率 | 应对 |
|------|------|------|
| FOE 对 16-QAM 不工作 | **已确定** | `rx**4` 对非恒包络 QAM 不适用（数学事实），改用导频辅助 FOE 或 oracle FOE |
| DPLL/VV 鉴相器不兼容 QAM | **已确定** | DPLL 改用 DD 鉴相器；VV/BPS 不纳入对比（4 次方鉴相器 QAM 专用） |
| QAM 下 NMSE 也不敏感 | 低 | W>0 仍然成立，但幅度判决不免疫。物理论证支持有影响 |
| 结果只是"温和影响"（0.5-2dB） | 中 | 即使温和也是信息：建立了调制依赖的定量边界。足够支撑 IP1 |
| 16-QAM 在低 SNR 下 BER 太高没意义 | 中 | 只看高 SNR（20-30dB），这是 QAM 的工作区域 |
| DD 鉴相器在深衰落中不可靠 | 中 | TL-10 已记录此问题；可在高 SNR（≥15dB）下验证 DD 是否足够可靠 |

---

### 实验 2: DPLL 锁相稳定边界解析推导（增强 IP2）

**优先级**: P1（子 agent 评估为"安全且高价值"）
**目标**: 推导 ω_n_max = f(α, β, γ̄) 的解析公式，与 C4-06 仿真数据交叉验证
**类型**: 解析贡献（TL-19 优先级 1，最安全）

#### 理论基础

1. **二阶 DPLL 稳态相位方差**（已有，V-16/V-09）：
   σ_φ² = B_L · T_s / (2 · γ̄ · h)，其中 B_L = 0.53 · ω_n

2. **锁相失效的物理机制**（C4-06 观察）：
   - 不是经典线性失稳（ω_n·T_s 远在约束内，V-16 确认）
   - 是非线性效应：大 ω_n → 大 B_L → 深衰落块中噪声放大超过信号 → 环路失锁
   - 失锁判据：σ_φ > π/4（QPSK 判决边界）→ BER 灾难性上升

3. **推导路径**：
   - 令 σ_φ² = B_L · T_s / (2 · γ̄ · h) < (π/4)²
   - 解出 B_L < (π/4)² · 2 · γ̄ · h / T_s
   - B_L = 0.53 · ω_n → ω_n < (π/4)² · 2 · γ̄ · h / (0.53 · T_s)
   - h 取 GG 分布的某个低分位数（如 1% 或 5%），即 h_min = F_GG⁻¹(p; α, β)
   - 最终：**ω_n_max = (π/4)² · 2 · γ̄ · h_min(α, β, p) / (0.53 · T_s)**

4. **验证**：
   - C4-06 数据：强湍流 **15dB** 锁相失败在 ω_n = 50MHz（8/10 失败）、100MHz（10/10 失败）
   - 推导应给出 ω_n_max 略低于 50MHz（强湍流 15dB 条件）
   - 弱湍流应给出更高的 ω_n_max（与 C4-06 弱湍流 100MHz 仍稳定的观察一致）
   - ⚠️ 注意：线性化公式给出的是**必要条件**（下界），非线性效应可能使实际失锁点更低。定位为"线性近似下界"而非精确公式。与 E06 (TENTATIVE) 的线性化局限已知，在文档中明确标注适用范围。

#### 代码指引

1. **解析计算脚本**（不需要仿真，纯数学）：
   ```python
   from scipy.special import gamma as gamma_func
   from scipy.stats import gamma as gamma_dist
   import numpy as np

   def gg_percentile(alpha, beta, p):
       """GG(alpha, beta) 分布的 p 分位数"""
       # GG = Gamma(alpha, 1/alpha) × Gamma(beta, 1/beta)
       # 需要数值计算 CDF 的逆
       ...

   def omega_n_max(gamma_bar_db, turb_name, p_fail=0.05):
       """推导 DPLL 锁相稳定的 ω_n 上界"""
       gamma_bar = 10 ** (gamma_bar_db / 10)
       alpha, beta = TURB[turb_name]
       h_min = gg_percentile(alpha, beta, p_fail)
       T_s = 1 / 2.5e9
       omega_max = (np.pi/4)**2 * 2 * gamma_bar * h_min / (0.53 * T_s)
       return omega_max
   ```

2. **与 C4-06 对比**：
   - 将推导结果与 `projects/simulation/results/dpll_omega_sweep.json` 中的失锁阈值对比
   - 画对比图：解析 ω_n_max vs 仿真观察到的失锁点

#### 风险与退路

| 风险 | 概率 | 应对 |
|------|------|------|
| 推导与仿真不吻合 | 中 | 调整 h_min 分位数或失锁判据，半解析也够用 |
| 公式形式太简单被质疑 | 低 | 物理推导过程是贡献，公式简洁反而是优点 |
| 与 V-16/V-09 理论重复 | 低 | 那些是稳态方差，这里是稳定边界，不同角度 |

#### 填补的创新点空白

innovation-points.md 表格中"ω_n 最优值 vs 湍流参数的解析关系——状态：未做"→ 本实验填补。

---

### 实验 3: E[1/h] 发散性判据推导（增强 IP2）

**优先级**: P1（纯解析，零仿真成本，最快出成果）
**目标**: 推导前馈方法（VV/BPS）在 GG 湍流下的理论失效判据
**类型**: 解析贡献（TL-19 优先级 1）

#### 理论基础

1. **GG 分布的 E[1/h]**：
   - h ~ GG(α, β) = Gamma(α, 1/α) × Gamma(β, 1/beta)
   - E[1/h] = E[1/X·Y] 其中 X~Gamma(α,1/α), Y~Gamma(β,1/β)
   - E[1/h] = E[1/X] · E[1/Y]（独立性）
   - E[1/X] = α/(α-1)（α > 1 时收敛）
   - E[1/Y] = β/(β-1)（β > 1 时收敛）
   - **E[1/h] 发散 ⟺ α ≤ 1 或 β ≤ 1**

2. **当前湍流参数**（common.py TURB）：
   | 湍流 | α | β | β > 1? | E[1/h] | 验证 |
   |------|---|---|--------|--------|------|
   | 弱 | 4.0 | 3.0 | 是 | 2.00 | MC: 2.001 |
   | 中 | 2.5 | 1.8 | 是 | 3.75 | MC: 3.757 |
   | 强 | 1.5 | 0.8 | **否** | **+∞** | MC: 130.6 (发散) |

3. **与前馈方法失效的因果链**：
   - VV 相位估计方差 ∝ E[1/(M·γ̄·h)] = (1/(M·γ̄)) · E[1/h]
   - E[1/h] 发散 → 平均相位估计方差无穷大 → 前馈方法理论上不可用
   - C4-01 验证：强湍流 VV BER 39.2%（灾难性），与理论一致

4. **理论判据**：
   > **当 GG 参数 β < 1 时，VV/BPS 等前馈方法的平均相位估计方差发散，方法理论上失效。**

5. **与 C16 互补**：
   - C16: E[1/h²] 发散（β < 2 或 α ≤ 2）→ 自适应窗口理论必然性
   - 本实验: E[1/h] 发散（β < 1）→ 前馈方法理论失效
   - 两者形成递进：β < 2 需要自适应窗口，β < 1 前馈方法本身失效

#### 代码指引

1. **解析推导脚本**（纯数学，不需要仿真）：
   ```python
   import numpy as np
   from scipy.special import gamma as gamma_func

   def gg_E_inv_h(alpha, beta):
       """计算 E[1/h] for GG(alpha, beta)"""
       if alpha <= 1 or beta <= 1:
           return np.inf
       return (alpha / (alpha - 1)) * (beta / (beta - 1))

   # 验证 C4-01 数据的因果链
   for name, (a, b) in TURB.items():
       E_inv_h = gg_E_inv_h(a, b)
       print(f"{name}: α={a}, β={b}, E[1/h]={E_inv_h:.2f}")
   ```

2. **验证**：
   - 用 C4-01 的 VV BER 数据验证：弱 0.015%（正常）、中 0.15%（可用）、强 39.2%（灾难）
   - 用 C4-03 的 VV 二态数据验证：中湍流 Nw=64 的 60% 失败率
   - 对比 E[1/h] 值与 VV BER 的相关性

#### 风险与退路

| 风险 | 概率 | 应对 |
|------|------|------|
| β < 1 太苛刻，实际只有强湍流触发 | 中 | 正好说明"强湍流需要闭环方法"的设计准则 |
| 被质疑"E[1/h] 发散"只是数学，不代表实际失效 | 低 | 有 C4-01/C4-03 的仿真数据直接验证 |
| 推导太简单，被认为"显而易见" | 中 | 包装为"理论判据"而非"新发现"——价值在于系统性地建立判据框架 |

---

### 实验 4: VV Nw_min 半解析模型（增强 IP2）

**优先级**: P2（与实验 2 配对，但解析难度更高）
**目标**: 建立 Nw_min = f(α, β, γ̄) 的半解析模型
**类型**: 半解析（GG 统计 + 仿真拟合）

#### 理论基础

1. **VV 失效机制**（C4-03）：
   - 深衰落块 h < h_critical 时，SNR_4 = γ̄·h/8 < 1
   - 4 次方鉴相器输出信噪比不足，unwrap 发生 2π 跳变
   - h_critical ≈ 0.08 @20dB（V-14 A5 锚点）

2. **失效概率分解**：
   P(VV 失败) = P(窗口内存在深衰落块) × P(unwrap 崩溃 | 深衰落)
   = [1 - (1 - F_GG(h_critical))^n_blocks] × p_unwrap(h_critical, Nw)

   其中：
   - F_GG(h_critical) = P(h < h_critical)：GG CDF，可解析计算
   - n_blocks = N_symbols / Nw：窗口内独立衰落块数
   - p_unwrap：条件概率，需要仿真拟合

3. **C4-05 数据**：
   | SNR | 弱 | 中 | 强(VV) |
   |-----|---|---|--------|
   | 10dB | ≥256 | ≥256 | ≥512 |
   | 15dB | ≥128 | ≥128 | ≥512 |
   | 20dB | ≥64 | ≥128 | ≥256 |

4. **Nw_min 的物理含义**：
   - Nw 增大 → 平均更多符号 → 噪声角度方差下降 → unwrap 更稳定
   - Nw_min 是使 P(unwrap 失败) < 目标阈值的最小窗口

#### 代码指引

1. **GG CDF 计算**（Meijer-G 闭合形式）：
   ```python
   from scipy.special import gamma as gamma_func
   import numpy as np

   def gg_cdf(h, alpha, beta):
       """GG(alpha, beta) 的 CDF — Meijer-G 闭合形式"""
       # 参考 formulas-master.md 的 Ch3 推导
       ...
   ```

2. **拟合 p_unwrap**：
   - 从 C4-05 的 nw_sweep.json 提取失败率数据
   - 拟合 p_unwrap(h_critical, Nw) 的参数化模型

3. **验证**：与 C4-05 的阈值表对比

#### 风险与退路

| 风险 | 概率 | 应对 |
|------|------|------|
| unwrap 失效是非线性事件，解析近似不精确 | 高 | 接受"半解析"定位，不追求精确公式 |
| p_unwrap 拟合泛化性差 | 中 | 在三种湍流下分别拟合，标注适用范围 |
| 被质疑"只是数据拟合不是理论" | 中 | GG CDF 部分是严格解析的，拟合只补最后一步 |

#### 填补的创新点空白

innovation-points.md 表格中"Nw 最优值 vs 湍流参数的解析关系——状态：未做"→ 本实验填补。

---

### 实验 5: Ch3 BER 闭合解预测 Ch4 DPLL 性能（跨章连接）

**优先级**: P2（补充验证，增强 Ch3→Ch4 递进叙事）
**目标**: 证明 Ch3 的 BER 闭合解可以精确预测 Ch4 DPLL 的实际性能
**类型**: 验证性实验

#### 理论基础

1. **Ch3 BER 闭合解**（C3-01）：
   BER_no_phase_error = E_h[Q(sqrt(2·γ̄·h))]

2. **Ch4 DPLL 在 20dB 下的 BER**（C4-06）：
   强湍流 DPLL BER ≈ 1.88%

3. **假设**：DPLL 在 20dB 下 σ_φ 极小（V-09 估算 ~2.6°），BER 主要由 SNR 调制决定
4. **预期**：BER 闭合解预测值 ≈ DPLL 实测 BER（偏差 <10%）

#### 代码指引

```python
# 用 Ch3 闭合解计算无相位误差的理论 BER
from scipy.integrate import quad
from scipy.special import gamma as gamma_func

def ber_closed_form(gamma_bar_db, alpha, beta):
    """GG 衰落下 QPSK BER 闭合解"""
    ...

# 与 C4-06 的 DPLL BER 对比
dpll_ber_strong_20db = 0.0188  # C4-06
predicted_ber = ber_closed_form(20, 1.5, 0.8)
ratio = predicted_ber / dpll_ber_strong_20db
print(f"预测 {predicted_ber:.4f} vs 实测 {dpll_ber_strong_20db:.4f}, 比值 {ratio:.2f}")
```

#### 风险

| 风险 | 概率 | 应对 |
|------|------|------|
| 预测与实测不吻合 | 低 | V-02 已有锚点显示 ~1.8% vs 1.88%，应该吻合 |
| 被质疑"这只是验证了已知的结论" | 中 | 定位为"分析框架预测能力验证"而非"新发现" |

---

## 实验调度建议

每个实验建议独立对话完成。按依赖关系排序：

```
实验 3 (E[1/h] 判据)     ← 纯解析，0 仿真，最快完成
  ↓
实验 2 (DPLL ω_n_max)    ← 解析+数据对比，无需新仿真
  ↓
实验 1 (16-QAM NMSE)     ← 需要新仿真代码，工作量最大
  ↓
实验 4 (VV Nw_min)       ← 半解析，依赖实验 2 的方法论
  ↓
实验 5 (跨章验证)        ← 补充验证，快速完成
```

### 产出更新

每个实验完成后需要更新：

1. **`毕设/CONCLUSIONS.md`** — 新增结论条目（标注代码来源）
2. **`毕设/innovation-points.md`** — 更新 §4 技术内容表（"未做"→"已完成"）
3. **`毕设/开题PPT/ppt-content-decisions.md`** — 如有影响 PPT 内容的发现

### 每对话提交规则

每个实验对话结束时统一 commit 一次，commit 消息格式：
```
feat(thesis): 创新点增强实验 N — [简要描述结果]
```

---

## 附录 A: 教训速查（每个实验对话必查）

| 想做什么 | 先检查什么 | 教训 |
|---------|-----------|------|
| 推导新公式 | 信号模型声明 + 文献确认 | TL-01 |
| 发现"震撼结果" | 先花 5 分钟查物理前提 | TL-22 |
| 报告增益数字 | 基线已优化？多种子？ | TL-14, TL-17 |
| 写入文档 | 验证完毕再写 | TL-23 |
| 跑新仿真 | TL-25 起飞检查单 6 条 | TL-25 |
| 从旧脚本引用结论 | 必须用 common.py 重验 | TL-24 |

## 附录 B: 关键文件路径

| 文件 | 路径 | 用途 |
|------|------|------|
| 教训文档 | `thesis-lessons.md` | 防坑 |
| 设计决策 | `毕设/design-decisions.md` | INVARIANT 约束 |
| 创新点 | `毕设/innovation-points.md` | 被否决方案+空白表 |
| 结论注册表 | `毕设/CONCLUSIONS.md` | 已有数据 |
| 公式总表 | `毕设/formulas-master.md` | Ch3/Ch4 公式 |
| 仿真核心 | `projects/simulation/common.py` | 信号生成+载波恢复 |
| NMSE 扫参 | `projects/simulation/experiments/sim_nmse_turbulence_sweep.py` | 实验 1 基础 |
| DPLL 扫参 | `projects/simulation/experiments/sim_dpll_omega_sweep.py` | 实验 2 验证数据 |
| Nw 扫参 | `projects/simulation/experiments/sim_nw_sweep.py` | 实验 4 验证数据 |
| PPT 内容 | `毕设/开题PPT/ppt-content-decisions.md` | PPT 定稿 |
| master-state | `毕设/master-state.md` | 全局状态 |

## 附录 C: 已否决方向（不要重新探索）

| 方向 | 否决原因 | 否决者 |
|------|---------|--------|
| 自适应载波同步 | 物理上无效（TL-03） | TL-03/06/07 |
| 湍流感知 R 矩阵 | 差异 <13% | X-01, C4-08 |
| 复数 h_est | 不物理 | X-07, TL-22 |
| BER floor 声称新颖 | B05/B11 INVARIANT | design-decisions |
| 省略 VV 模块 | 弱湍流有用 | innovation-points 否决 v2 |
| 解析自适应 | 收益薄 | innovation-points 否决 v3 |
| "设计与优化方法"措辞 | 过度承诺 | innovation-points 否决 v4 |
| KF 统一载波同步 | 导师否决 | A06 |
