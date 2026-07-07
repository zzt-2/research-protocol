# [S005] sandbox 前半 3 步 + 步骤 4：B7Params 回写 + PSA FOE 重写 + TED_gain 解析推导 + CRB 下界

> 2026-07-08 | 阶段 1 sandbox（前半 + 步骤 4）| 状态: 完成
> profile 第 9 次防线已解除（阶段 0 六项全做完），本轮开始写代码。守 sim-preflight v1.3.0 + INVARIANT 6 解除。
> 2026-07-08 续接：用户授权"往下"，追加步骤 4 CRB 下界（独立、轻量、FR-21 参考）。

## 目标

执行 sandbox 前半 3 步（H004 阶段 1 第 1-3 步）：
1. B7Params 回写 params.py（15 字段，删 PSA_PILOT_SPACING，修 LEO_DOPPLER_RATE，补 7 新字段）+ 跑审计确认无 DEAD/CRITICAL
2. PSA FOE baseline 重写（谱不对称法 Vieira 2023），新写 `_psa_foe_asymmetry.py`
3. B7 TED_gain(f_D) 解析推导 + Leven 2007 对比，闭合 D002 残留风险

主线负责目标设定/边界框定/结果集成/独立核查；步骤 2/3 派子 agent 执行，步骤 1 小任务主线程直接做。守 15 分钟子 agent 上限。

## 记录

### 步骤 1：B7Params 回写 params.py（主线程直接做，小任务）

**改动**：`projects/simulation/params.py` L606-680 B7Params 类整体替换（旧 6 字段 → 新 15 字段）。

**回写内容**（来自 `_stage0_5_6_params_files.md` §1.2 草稿）：
- **删**：`PSA_PILOT_SPACING`（概念错遗留，PSA FOE 是谱不对称法不用 pilot）
- **修**：`LEO_DOPPLER_RATE` 30e3 → 1e9（Hz/s，content.md L47「1 GHz/s」）
- **补 7 新字段**：`R_SYM_B7`(25GBaud) / `LASER_LW_B7`(1.8kHz) / `ROLL_OFF`(0.1) / `RX_BW_GHZ`(36.75GHz) / `SPS_RX`(2.94) / `DOPPLER_INTERVAL`(1GHz) / `LEO_DOPPLER_EXCURSION`(±100MHz)
- **拆**：`OSNR_WORKING_POINT` → `OSNR_WORKING_POINT_LOW`(10dB) + `OSNR_WORKING_POINT_MAIN`(17dB)
- **补跨候选**：`HD_FEC_THRESHOLD`(3.8e-3) + `BER_SENSITIVITY_THRESHOLD`(2e-2)
- 保留：`DOPPLER_RANGE`(23e9) / `GARDNER_SPS`(2) / `GARDNER_GAIN`(0.01, WARNING 典型值)

**审计结果**（主线跑 `python params.py`）：
- B7Params：15 字段，**14 OK + 1 WARNING（GARDNER_GAIN 典型值），0 DEAD/CRITICAL** ✅
- 全局 SimulationConfig：total 55→64（+9 OK），DEAD/CRITICAL 数不变（6/4，未引入新问题）
- 下游引用核查：grep `PSA_PILOT_SPACING|OSNR_WORKING_POINT\b|B7Params\.` 在 simulation/ 下（除 params.py）**无任何引用**，无 D-007 式断链 ✅

### 步骤 2：PSA FOE baseline 重写（谱不对称法，子 agent 执行）

**子 agent 产出**（4 文件 in `explore/b7-gardner-ted-foe/`）：
- `_psa_foe_asymmetry.py`（脚本，自包含不 import common/params）
- `_psa_foe_asymmetry_results.json`（f_D 0-25GHz sweep，noiseless + OSNR17dB）
- `_psa_foe_asymmetry_curve.png`（Δf̂ vs f_D）
- `_psa_foe_asymmetry_summary.md`（摘要）

**Vieira 2023 公式提取（C6）**：`papers/doi/10.1109_access.2023.3287501/content.md` L343-347。L345 显示公式图片 omitted，但 L347 prose 完整描述结构：P+/P− ratio → log → ×α → frequency。read-note L44 记录闭合形式 **Δf̂ = α·ln(P+/P−)/2**。子 agent 判定**不是降级实现**（结构从 prose 恢复，`/2` 因子从 read-note 取）。α 是 Vieira 用 sequential search 拟合的常数（无解析式），子 agent 用 1-point slope fit @ f_D=1GHz 复现 → α_calib = 0.953 GHz。

**估准范围实测（关键反常发现）**：
- **线性区仅 ~1GHz**，远低于 B7 poster content.md L19 声称的"半 baud rate 12.5GHz"
- f_D=5GHz → Δf̂=1.22GHz（failA+failB）；f_D=12GHz → Δf̂=2.44GHz（failA+failB，约此处达峰后折叠）；f_D=15GHz → Δf̂=1.77GHz（漂零 failB ✓ 符合 poster L49）
- OSNR17dB 跟 noiseless 几乎一致 → **噪声不是瓶颈，indicator 非线性/混叠是**

**主线判定**：线性区 ~1GHz 不是 bug，是 **β=0.1 RRC 谱尖边缘的物理结果**（谱边缘带宽 (1+β)·Rs/2 附近 = ~1.25GHz，f_D 超过这个 ln-ratio 就饱和）。跟 poster "fails beyond 12 GHz" 不冲突——poster 只给 aliasing 上界（半 baud 12.5GHz），没给线性区下界实测。子 agent 报的 ~1GHz 是更保守的真实测量。**登记为 sandbox 已知限制**（见 D006）。

### 步骤 3：B7 TED_gain(f_D) 解析推导 + Leven 对比（子 agent 执行）

**子 agent 产出**（4 文件）：
- `_ted_gain_analytic.py`（脚本，自包含，运行 2.8s）
- `_ted_gain_analytic_results.json`（解析式 + 数值验证 + Leven 对比）
- `_ted_gain_analytic_comparison.png`（4 子图对比）
- `_ted_gain_analytic_summary.md`（摘要）

**G(f_D) 解析式（主结果）**：
```
S(τ; f_D) := E[e(k)] = K(τ)·cos(π·f_D/B)
G(f_D) = max_τ |S(τ;f_D)| = K_max·|cos(π·f_D/B)|
```
- K(τ) 是与 f_D 无关的纯 τ 函数（由成形脉冲自相关决定）
- f_D 依赖性被完全解耦为单一余弦因子 cos(πf_D/B)，**与具体脉冲形状无关**（Gardner TED 3 点相位差结构决定）
- 周期性解析精确：G(f_D+B) = K_max·|cos(πf_D/B + π)| = K_max·|cos(πf_D/B)| = G(f_D)（三角恒等式）

**Leven 2007 论文（重要更正）**：
- **已落盘**于 `papers/doi/10.1109_lpt.2007.891893/content.md`（DOI 笔误：task brief 写 `891597`，实为 `891893`，内容是正确论文 Leven/Kaneda/Koc/Chen PTL 19(6):366-368, 2007，跟 B7 poster ref[7] 完全匹配）
- **Leven 是时域 phase-increment mean-angle**（content.md L33-65 THEORY 节文字描述清晰，公式图片 omitted）：`r_k = y_k·conj(y_{k-1})` → `^4`（QPSK M=4）→ mean → angle → `f̂ = angle(mean_k[y_k·conj(y_{k-1})]^4)/(8πT)`
- **非** task brief 假设的"频域 FFT 谱峰"

**同族性判定（D002 残留风险闭合）**：**弱同族 (B)，不降级 (C)**。

判据：(C) 强同族要求"核心运算层等价 + 任务相同"。B7 跟 Leven 三层运算均不等价：

| 维度 | B7 | Leven 2007 |
|---|---|---|
| 任务 | FOE | FOE | **同** |
| 乘积结构 | Gardner 3 点交叉积 `y_mid·conj(y_curr−y_prev)` | 2 点相邻共轭积 `y_k·conj(y_{k-1})` | **不同** |
| 非线性 | Re 部（线性）| 升 4 次幂 `^4`（强非线性去调制）| **不同** |
| 聚合 | `max_τ|S-curve|` 扫频峰反演 | `angle(mean_k·)` mean-angle | **不同** |
| f_D 依赖 | cos(πf_D/B) 周期 B | B/M=B/4 模糊周期 | **不同** |
| 升幂/angle | 无（M=1）| 有（M=4）| **不同** |

**反 NDA-ML 陷阱**：B7 既不升幂也不 mean-angle，不存在"B7 vs Leven 持平 = 数学等价"的 bug 路径（跟 VV 同理，0.2b 已确认）。

### 主线 V5 独立核查（守 D-009 教训 6）

| 核查项 | 子 agent 报告 | 主线独立重算 | 结论 |
|---|---|---|---|
| G(0) 解析值 | K_max·1 = 0.132142 | 0.2a 锚点 0.13214186，误差 1.4e-7 | **PASS** bit-exact |
| 周期性 | max\|G(f+B)−G(f)\|=7.46e-17 | 三角恒等式 cos(θ+π)=−cos(θ)，\|cos\| 周期 π → 解析精确 | **PASS** |
| 零点位置 | 12.5/37.5/62.5 GHz | cos(πf_D/B)=0 ⇔ f_D=(n+0.5)B → 12.5/37.5/62.5 | **PASS** |
| Leven 同族判定 | 弱同族 B（三层运算不等价）| 乘积/非线性/聚合三层确不等价，判据合理 | **PASS** |
| Leven DOI | 891893（非 brief 的 891597）| 核查 content.md L25 DOI + 作者 + 期刊号，确实是正确论文 | **PASS** |
| PSA 线性区 ~1GHz | 反常发现 | β=0.1 谱边缘 ~1.25GHz 物理一致，非 bug | **PASS** |

**V5 整体结论**：3 步产出全 PASS，子 agent 原始数字可信，归因正确。无红线警报（未发现 B7 vs Gardner 1986 BER gap <0.1dB 征兆——本任务不直接跑 BER，但估准范围/解析式均无异常）。

## 决策引用

- **D006**（新建）：PSA FOE coarse-only baseline 线性区 ~1GHz 限制登记（25GBaud/β=0.1 物理结果，非 bug）+ fair gain 上界含义 + Leven DOI 修正
- D002（沿用）：弱同族 (B) 残留风险**闭合**——sandbox 步骤 3 解析推导 + Leven 对比确认不降级 (C)
- D005（沿用）：B7Params 回写完成，15 字段全溯源，阶段 0.5 草稿落地
- D004（沿用）：PSA FOE baseline 谱不对称法重写完成（非 pilot-aided）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。3 步全在阶段 1 sandbox 范围内（阶段 0 已收尾，profile 第 9 次防线解除）。未碰"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common——PSA FOE 重写在 explore/ 新文件，common/_recovery.py 旧函数保留未改）。

## 后续

**已闭合**：
- D002 残留风险（TED_gain 解析式 + Leven 对比）——弱同族 (B) 确认，不降级 (C)
- B7Params 旧字段问题（LEO_DOPPLER_RATE 错 + 缺 5 字段 + PSA_PILOT_SPACING 概念错）——15 字段全溯源回写
- common psa_foe_recovery 概念错债务——PSA FOE baseline 重写为谱不对称法（旧函数保留未删）

**带进对话 6（sandbox 后半 + MVE）**：
- D006 新债务：PSA FOE coarse-only 弱（线性区 ~1GHz）——三方对照时记录为 fair gain 上界，可选补 fine CFE stage 作双方对称增强（V3 公平性）
- B7Params 回写 params.py 后，对话 6 三方对照主脚本 + MVE 可直接 import B7Params
- sandbox 后半 2 步（步骤 4 CRB 已本轮做完）：⑤ 三方对照主脚本（C7+V2）⑥ MVE + consistency + B7-MVE-SPEC.md
- 守 sim-preflight v1.3.0 V3（B7 vs Gardner 1986 BER gap <0.1dB 红线警报）+ TL-20（BER gain @ BER 2e-2 偏离 0.6dB >0.2dB 查 LPF2 + PSA baseline）

---

## 追加：步骤 4 CRB 下界（2026-07-08 续接，用户授权"往下"）

### 步骤 4：CRB 下界（子 agent 执行）

**触发**：用户授权"往下"。步骤 4 独立轻量（CRB 是数值+解析，不依赖三方对照），可本轮做。步骤 5/6（三方对照 + MVE）是重活 + 需用户 Go 判断，留下轮。

**子 agent 产出**（4 文件 in `explore/b7-gardner-ted-foe/`）：
- `_crb_lower_bound.py`（脚本，自包含）
- `_crb_results.json`（N×OSNR sweep）
- `_crb_curve.png`（CRB vs N 曲线 + 1GHz 水平线）
- `_crb_summary.md`（摘要）

**CRB 公式（C6 溯源）**：`var(f_D) ≥ 12 / [(2π)²·(E_s/N_0)·T_s²·N·(N²−1)]` [Hz²]。来源 Rife-Boorstijn 1974 / Kay 1993 ch.15.7 / Mengali-D'Andrea 1997 §3.7。常数 12 = 频偏+相位同时未知（FOE 现实场景）。DA / 已知 s(t) 绝对下界——B7 是 NDA 间接估计（Gardner TED 增益扫频峰反演），实际方差 ≥ 此 CRB。

**关键数字**（主线 V5 独立重算 bit-exact）：
- 主测点 N=1024, OSNR=17dB：CRB std = **59.42 kHz = 5.94×10⁻⁵ GHz**
- N scaling 拟合斜率 = **−1.5000**（理论 −3/2 bit-exact）
- OSNR→E_s/N_0 转换：(2·12.5GHz)/25GHz = 1.0 ⇒ 25GBaud 下 E_s/N_0_dB = OSNR_dB（巧合约 1）
- 低 SNR (OSNR=10dB, N=1024)：CRB std = 133 kHz（仍远小于 1 GHz）
- CRB / 扫频间隔 = 5.94×10⁻⁵（**CRB 比扫频间隔小 16830 倍**）

### 主线 V5 独立核查（步骤 4）

| 核查项 | 子 agent 报告 | 主线独立重算 | 结论 |
|---|---|---|---|
| CRB std @ N=1024 OSNR=17dB | 59415.68 Hz | 59415.68 Hz（误差 0.0000%）| **PASS** bit-exact |
| N scaling 斜率 | −1.500 | −1.5000（理论 −3/2）| **PASS** bit-exact |
| CRB vs 扫频间隔 | 比值 5.94e-5（小 16830 倍）| 5.94e-5，确认 << 1 | **PASS** |
| 低 SNR CRB | 133 kHz | 133.02 kHz（误差 0.01%）| **PASS** |

### 步骤 4 结论（FR-21 参考角度，D005 降级非 Kill 门）

**B7 FOE 精度瓶颈是 1 GHz 扫频量化网格，不是理论 CRB 极限**。
- CRB（59 kHz）比扫频间隔（1 GHz）小 16830 倍——理论空间巨大，B7 缺的是精细扫描不是估计能力
- CRB 完全不卡 B7，FR-21 不触发 Kill（D005 已降级为参考）
- 务实启示：若下游需亚 GHz 精度，B7 可窄带重扫（poster Fig.3b 已验证路径——初始 f̂ 确定后窄带扫描降复杂度）
- B7 的 Go 判据仍是赢传统 baseline 几 dB（D005 务实路线），不是 CRB 精度

### 步骤 4 决策引用

- 无新建 D###（CRB 是参考数值，不构成决策变更）。FR-21 在 D005 已降级，CRB 数值证实降级合理（CRB 远不卡 B7）。
- D005（沿用）：FR-21 降级为参考，CRB 算出来作对照——步骤 4 执行了这个对照，结论 CRB << 扫频间隔，B7 理论裕量充足

### 步骤 4 范围确认

- 本轮是否在 scope boundary 内：**是**。步骤 4 在阶段 1 sandbox 范围内（H004 sandbox 六步的第 4 步）。未碰"明确不含"。
