# dB 口径对齐 + 复杂度分析（写论文 framing 的事实基础）

> 日期: 2026-07-08 | 来源: 用户选路线 A（方法工具引用）后的两项硬前提核查
> 数据: `results/sc_nda_ml_main/_fair_gain_summary.json` + B11 原文 + 解析推导

## 一、dB 口径拆解（关键发现）

### 我们的 fair_gain 拆成两部分

fair_gain（总能量公平）= pilot_overhead（架构性，固定 1.249dB）+ naive（DA 算法层劣势）

| 场景 | fair_gain | = pilot_oh | + naive(算法层) |
|---|---|---|---|
| AWGN | 1.351 dB | 1.249 | **+0.102 dB** |
| weak 湍流 | 1.529 dB | 1.249 | +0.280 dB |
| moderate 湍流 | 1.712 dB | 1.249 | +0.463 dB |
| strong（工作区）| 2.515 dB | 1.249 | +1.266 dB |

**核心发现**：我们的 fair_gain 里，**pilot overhead 占绝大部分**（AWGN 占 92%，湍流占 55-73%）。纯算法层 DA 劣势（naive）只有 0.1~0.5dB（AWGN/弱中湍流），strong 湍流因 deep fade pilot 崩溃才到 1.27dB。

### B11 的 +2dB 是什么口径

B11 原文 L159-161："DA ML method is highly sensitive to phase noise, especially with high constellation density. At 200 kHz CLW, the DA ML method exhibits a 2 dB SNR drop"

- B11 的 DA = **decision-feedback DA-ML**（引 [10] Cao 2012），靠判决反馈再估相位
- B11 **没算 pilot overhead 到总能量**（OFDM 用 pilot subcarrier，口径不同）
- +2dB 原因 = **纯算法层**（DA 对 PN 敏感 + 密星座判决错误传播）

### 口径对齐

| | B11 +2dB | 我们 fair_gain |
|---|---|---|
| **DA 类型** | decision-feedback | pilot-aided (sp=4) |
| **含 pilot overhead?** | 否 | 是（1.249dB）|
| **物理原因** | DA 对 PN 敏感 + 判决错误传播 | pilot 架构代价 + deep fade pilot 崩溃 + 少量 PN 敏感 |
| **重叠** | 都是"DA 算法层劣势" | naive 项（0.1~0.5dB）|

**关键差异**：我们的 naive 项（0.1~0.5dB）远小于 B11 的 2dB——因为**我们的 pilot-aided DA 比 B11 的 decision-feedback DA 强**（sp=4 近最优，不受判决错误传播影响）。

### 写作含义

- ❌ **不能直接引 B11 +2dB 说"我们也赢了 2dB"**——口径不同（B11 不含 pilot overhead，DA 类型不同）
- ✅ **可以引 B11 作"DA-ML 对 PN 敏感是领域共识"**的旁证（naive 项的背景）
- ✅ **我们 fair_gain > B11 +2dB 是合理的**——我们口径更宽（含架构代价 + 场景更恶劣含湍流）
- ⚠️ **诚实措辞**：写"vs pilot-aided DA-ML 在总能量公平下 +1.35~2.5dB"，注明"含 pilot overhead 1.25dB 架构代价"

## 二、复杂度分析（意外发现：NDA-seg 不比 VV 复杂）

### 每符号实数乘法粗估（N=256, M0=8，不计吞吐）

| 方法 | 实乘/symbol | 吞吐 | 特点 |
|---|---|---|---|
| **NDA-seg (K=8)** | **~16** | 100% | 块结构，K 段可并行 |
| **VV (Nw=64) 递推** | **~24** | 100% | 滑窗，递推有数据依赖 |
| DA-ML (sp=4) | ~5.5 | **75%** | 计算最低，但吃 pilot |

拆解：
- **升 M0=8 快速幂**：三者都要，3 次复乘 = 12 实乘/symbol（共同项）
- **NDA-seg**：段内 mean（摊到每符号~0）+ 段间插值补偿（4 实乘）= 16 实乘
- **VV 递推**：滑窗递推 mean（2 复乘 = 8 实乘）+ angle+exp（4 实乘）= 24 实乘
- **DA-ML**：pilot 处 angle+回归（10 实乘/pilot，1/4 密度）+ 数据处补偿（4 实乘×3）= 5.5 实乘

### 意外发现：NDA-seg 反而比 VV 简单（16 vs 24）

之前担心"NDA 比 VV 复杂"——**不成立**。NDA-seg 的块结构（K 段独立 mean）比 VV 的滑窗递推（每符号都要更新窗）计算量略低。而且：
- **NDA-seg 块结构天然并行**（K 段独立估，可 K 路并行）
- **VV 滑窗有数据依赖**（递推必须串行，除非用流水线）
- **FPGA 实现友好**：NDA-seg 定长块，VV 滑窗变长

### 写作含义（路线 A 第三卖点成立）

- ✅ **复杂度维度 NDA-seg 不输 VV**（甚至略优 + 可并行）——这可以作为"选 NDA-ML 不选 VV"的一个工程理由
- ⚠️ 但要注意：这个优势很小（16 vs 24），且 VV 也有快速实现变体。不能过度宣称
- ✅ **真正的复杂度优势是 vs DA-ML 的吞吐**（100% vs 75%），但这已在 fair_gain 里算过（pilot overhead）

## 三、给用户想 framing 的事实清单

基于以上，路线 A（方法工具引用）能用的**诚实卖点**：

| 卖点 | 强度 | 证据 | 诚实边界 |
|---|---|---|---|
| **vs DA-ML 免导频**（架构性）| 最强 | fair_gain 1.35~2.5dB（含 1.25dB overhead）| 不能引 B11 +2dB 旁证（口径不同）|
| **星地湍流场景适配** | 强 | B11 假设湍流已补偿，我们建模了 + deep fade 鲁棒性 | 场景增量非方法增量 |
| **复杂度不输 VV** | 中 | 16 vs 24 实乘/symbol + 可并行 | 优势小，不过度宣称 |
| **LEO Doppler 适配**（待验证）| 待定 | 两阶段 FOE 框架已就绪 | 需跑 LEO 场景验证 |

**不能用的**：
- ❌ "NDA-ML 算法层优于 VV"（A2 + 物理推导已证持平）
- ❌ "我们赢了 B11 报的 2dB"（口径不同）
- ❌ "方法创新"（路线 A 定位是工具引用，方法不是贡献）

## 数据指针
- 主实验 fair_gain: `results/sc_nda_ml_main/_fair_gain_summary.json`
- DA-ML 实现: `common/_recovery.py:136-168`
- 公平对照框架: `simulator/fair_comparison.py:84-157`
- B11 原文: `papers/doi/10.1109_lpt.2024.3523478/content.md` L159-161
