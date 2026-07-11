# [R012] 参数+数字呈现+叙事结构（D-P2P3 产出）

> 2026-07-11 | 关联：专题 2026-07-09-thesis-writing / writing-campaign-plan.md §2 P2+P3 / H008 交接
> 数据来源：`_b11_params.py` all_traced_params_summary()（行 112-129）+ `_fair_gain_summary_30seed.json` + `_a4_switch_30seed_fixed.json` + `fair_comparison.py:109` 口径核验 + `/tmp/verify_logic_chain.py` crossover 核验 + `/tmp/switch_caliber_audit.py` 选对率核验

## 调研问题

把仿真参数填进 R011 符号表（标文献来源 TL-26）+ 定数字怎么呈现（口径/CI 策略）+ 把 R009 逻辑链分配到 5 节出大纲。P2（参数数字）和 P3（叙事结构）串行，P3 吃 P2 的数字布局当输入。

## 发现

---

## P2-A 参数表

参数溯源全部核对 `_b11_params.py`。每个参数标文献来源（TL-26 强制）。参数值对齐 D-007 单载波统一（删 B11 OFDM 场景的 25GBaud/500kHz）。

### A1. 信号 / 调制参数

| 符号 | 值 | 含义 | 来源（代码行 + 文献）|
|---|---|---|---|
| M₀ | 8 | 升幂次数（(8,8)-16APSK 每环 8 点）| `_b11_params.py:36 M0=8`；B11 行 75-77 |
| R_sym | 2.5 × 10⁹ sym/s | 符号率（2.5 GBaud）| `_b11_params.py:47`（params SystemParams.R_SYM）；design.md §3.1 |
| T_s | 4 × 10⁻¹⁰ s | 符号周期 = 1/R_sym | `_b11_params.py:48`（derived）；= 1/2.5e9 |
| E_s | （每符号能量，归一化）| 每符号能量 | SNR 定义基准（γ = E_s/N₀）|
| N_DFT | 256 | DSP 处理块长（逐块恢复块大小）| `_b11_params.py:35`；B11 行 155；MVE `_time_domain_crlb.py:118` |
| N_blk | 100 | 信道块长（h 恒定的符号数）| `_b11_params.py:39 CH_BLOCK=100`；params ExperimentParams.BLOCK=100 |
| BITS_PER_SYM | 4 | 每符号比特（(8,8)-16APSK）| `_b11_params.py:37` |

### A2. 信道参数

| 符号 | 值 | 含义 | 来源（代码行 + 文献）|
|---|---|---|---|
| α, β（weak）| (4.0, 3.0) | GG 形状参数（下行弱湍流）| `_b11_params.py:79`；params TurbulenceParams；SPEC §1.4 |
| α, β（moderate）| (2.5, 1.8) | GG 形状参数（下行中等湍流）| `_b11_params.py:80`；SPEC §1.4 |
| α, β（strong）| (1.5, 0.8) | GG 形状参数（下行强湍流）| `_b11_params.py:81`；SPEC §1.4 |
| α, β（up_mod）| (1.2, 0.9) | GG（上行中等，σ²_R≈0.15）| `_b11_params.py:91`；sat.1553 Table 1 |
| α, β（up_str）| (1.0, 0.7) | GG（上行强，σ²_R≈0.25）| `_b11_params.py:93`；sat.1553 Table 1 |
| σ²_R | （由 α,β 推算）| Rytov 方差（湍流强度度量）| Al-Habash 2001（α,β→σ²_R 标准映射）；Johst L201 用 σ²_I |
| Δν | 10 × 10³ Hz | 激光线宽（10 kHz）| `_b11_params.py:46 LASER_LW`；sat.1553 §4.2 L438（星地 FSO ECL 典型）；D-007 统一单载波 |
| σ²_θ | 2.51 × 10⁻⁵ | 每符号 Wiener 相位噪声方差 = 2πΔνT_s | `_b11_params.py:51 SIGMA2_P`；Viterbi 1963 标准激光 PN 模型；**首次出现注 "= σ²_p in [B11]"**（B11 用 σ²_p 符号）|

### A3. 帧结构 / pilot 参数

| 符号 | 值 | 含义 | 来源（代码行 + 文献）|
|---|---|---|---|
| pilot spacing | 每 4 符号 1 pilot | 导频间距 | `_b11_params.py:65 DA_PILOT_SPACING=4`；D-S5-01 + B11 帧结构 |
| pilot overhead | 25%（带宽占比）| 导频开销 | derived = 1/spacing = 1/4 |
| pilot power penalty | 1.249 dB | 导频功率代价 = 10log10(4/3) | `_b11_params.py:68 PILOT_OVERHEAD_DB`；derived；Shieh-Djordjevic 2010 |

### A4. 实验矩阵

| 符号 | 值 | 含义 | 来源（代码行 + 文献）|
|---|---|---|---|
| γ（AWGN 扫描）| 5, 8, 10, 12, 14, 16, 18, 20 dB | AWGN 场景 SNR 扫描点 | `_b11_params.py:103 SNR_AWGN_DB`；design.md §3.4 / MVE |
| γ（湍流扫描）| 5, 10, 15, 20, 22, 24, 26 dB | 湍流场景 SNR 扫描点 | `_b11_params.py:104 SNR_TURB_DB`；扩至 26dB 覆盖 HD-FEC 交叉点 |
| N_blocks | 400 | 仿真块数（400×256=102400 ≥ 1e5）| `_b11_params.py:101 N_BLOCKS`；FR-21（N≥1e5）|
| seeds | 30（基准配置）/ 3（其他）| 蒙特卡洛种子数 | 基准配置 30seed；其他 3seed（债务）|
| HDFEC | 3.8 × 10⁻³ | 7% HD-FEC 门限 BER | `_b11_params.py:64 HDFEC`；B11 行 181/191 |

### A5. 不进参数表的（背景，进正文一句话）

| 参数 | 值 | 处理 |
|---|---|---|
| 调制 | (8,8)-16APSK（DVB-S2X 族）| 进 System Model 一句话引 B11 |
| 信道 | Gamma-Gamma 块衰落 | 进 System Model（引 Al-Habash 2001）|
| 相干检测 | 相干 FSO | 进 Intro 背景一句话 |

---

## P2-B 数字呈现方案

### B1. 口径定义（D004/D005 已定，代码行核验过）

**口径核验（fair_comparison.py:109）**：`gain_hdfec = (s_da_d + pilot_overhead_db) - s_nda_d`
- **fair_gain（JSON 字段）= DA 总能量 γ_tot − NDA 总能量**（DA data-SNR + 1.249dB overhead）。**含** pilot overhead，是系统总账，**大数**
- **naive = fair_gain − 1.249 dB** = 减去导频开销后的纯物理增益，**小数**
- 方向验证：strong fair=2.509 → naive=2.509−1.249=**1.260** ✓（与 D004 一致）；up_str fair=3.101 → naive=3.101−1.249=**1.852** ✓

**主报口径 = naive**（D004/D005 倾向，剔导频水分后纯物理增益，不易被审稿人质疑）。

### B2. 数字清单（每条标进正文/表/图 + 口径 + 来源 + 验证状态）

| # | 数字 | 进正文/表/图 | 口径 | 来源 | 验证状态 |
|---|---|---|---|---|---|
| 1 | 净增益 strong +1.26 dB | **正文 + Tab.1** | naive（= fair 2.509 − 1.249）| `_fair_gain_summary_30seed.json` strong workregion_grand_mean=2.509；D004 | ✅ 已核验 |
| 2 | 净增益 up_str +1.85 dB | **正文 + Tab.1** | naive（= fair 3.101 − 1.249）| JSON uplink_strong workregion=3.101；D004 | ✅ 已核验 |
| 3 | 净增益 up_mod +1.19 dB | Tab.1 | naive（= fair 2.443 − 1.249）| JSON uplink_moderate workregion=2.443 | ✅ 已核验 |
| 4 | 净增益 awgn/weak/mod naive +0.09/0.18/0.19 dB | **正文诚实标注**（不强进表）| naive（= fair 1.339/1.428/1.439 − 1.249）| JSON awgn/weak/moderate gain_mean | ✅ 已核验。**CI 重叠归零**（不变量 3，诚实标注）|
| 5 | 切换 vs 固定 NDA（低 SNR 避险）+1.3~2.3 dB | **正文** | net（switch_vs_nda，CI 下界全正）| `_a4_switch_30seed_fixed.json`：weak@5=+1.81/weak@10=+2.30/mod@5=+1.65/mod@10=+1.98/strong@5=+1.30/strong@10=+1.29 | ✅ 已核验（D002 修复版）|
| 6 | 切换 vs 固定 DA | **不进论文**（导师第3点：vs 导频输不写）| net | switch_vs_da_net 多数 CI 跨 0 不显著 | ✅ 已核验（D002）|
| 7 | 切换选对率 26/29（90%）| **正文贡献句** | data 口径 | `/tmp/switch_caliber_audit.py`：awgn 8/8 + weak 7/7 + mod 7/7 + strong 4/7 | ✅ 已核验 |
| 8 | crossover SNR：weak 17.9 / mod 16.8 / strong 10.7 dB | **正文 + Fig.4** | data 口径（线性插值交叉点）| `/tmp/verify_logic_chain.py` 断言1 | ✅ 已核验（**只呈现数据不附物理归因**，R009）|
| 9 | pilot overhead 1.25 dB（= 10log10(4/3)）| **正文 §II** | 定义值 | `_b11_params.py:68`；Shieh-Djordjevic 2010 | ✅ |
| 10 | M₀ = 8 | 正文 §II | 定义值 | B11 L75-77 | ✅ |

### B3. 口径标注规则（D004 教训 + R011 net SNR gain 脚注模板）

每次报增益，读者必须能看出是 naive 还是 fair：
- **脚注模板**（首次报 net SNR gain 时加）："All reported gains are net of the pilot power penalty of 1.25 dB (10log10(4/3)); the bit error rate is computed over data symbols (768 bits per block) unless otherwise stated."
- Tab.1 列名标 "net gain (dB)"
- 正文报数字时跟一句 "(naive, net of pilot overhead)" 或 "(fair, including pilot overhead)"

### B4. CI 策略（R002§C 实证）

- **不报 CI 是领域惯例**（6 篇样本实证：全不报 CI/误差棒，连蒙特卡洛都不做单次 PRBS）
- **30seed+CI 不当主卖点**。如需提及，用"湍流随机性需多 seed 表征分布"正当化（非"更严谨"）
- 30seed 严谨性可作差异化低调提及（R002§C 结论，一句话带过）
- CI 数字在论文里不出现（Tab.1 只放 mean 值），但所有报的数字背后有 30seed CI 支撑（诚实底线）

### B5. 数字-图表映射

| 图/表 | 表达什么论点 | 放哪些数字 |
|---|---|---|
| **Tab.1** 增益汇总 | 净增益量化归因（强湍流/上行显著，弱湍流归零诚实）| 只放强湍流 3 行 naive：strong +1.26 / up_mod +1.19 / up_str +1.85 dB（R010 §4.2 增量亮点）|
| **Fig.2** BER 主图 | DA/NDA 各自 BER 曲线 + crossover 自然呈现 | BER vs SNR(dB)，6 子图（3 下行 + 2 上行 + AWGN），不标数字（图自己说话）|
| **Fig.4** crossover | 切换跨场景自动选优（data 口径多场景 BER 曲线叠加）| crossover 点视觉呈现（weak 17.9/mod 16.8/strong 10.7 在图中可读）|

---

## P3-A 5 节大纲

R009 逻辑链（DA/NDA trade-off → 数据印证 → 切换机制）分配到 5 节。每节标论点（段落级）/ 数字 / 公式 / 图表占位。篇幅对齐 R010。

### §I Introduction（1-2 段，~8-15 行，R010 §1.1）

**论点（段落级）**：
1. 背景：星地激光通信相干检测 + 大气湍流致相位噪声 + 载波相位恢复（CPR）必要（1 段，引 3-5 篇综述/标准）
2. Gap + 动机：DA/NDA trade-off 的 gap（DA 低 SNR 精度高但花 25% 带宽；NDA 省带宽但受 squaring loss 影响低 SNR 差）。引出本文：per-block SNR 驱动的自适应估计器切换（1-2 句，对齐 R010 §1.3）
3. 贡献声明（散文式 2-3 句，R010 §1.2 实证 5/5 篇不用 bullet）：
   - "we propose a per-block SNR-driven estimator switching scheme that selects between a data-aided (DA) and a non-data-aided (NDA) carrier phase estimator"
   - **切换 framing = 自适应选优**（R008）："selecting the locally optimal estimator in 26 of 29 operating points"
   - 净增益量化："yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"

**用哪些数字**：贡献句放 26/29 选对率 + 1.85 dB（naive）
**用哪些公式**：无（Intro 不放公式）
**用哪些图表**：无

### §II System Model（1-2 段，R010 §2.1/§2.2）

**论点（段落级）**：
1. 信道模型：Gamma-Gamma 块衰落 + 块结构说明（h 块内恒定 N_blk=100，块间独立）。引 Al-Habash 2001。（对齐 R010 §2.1：给 GG 模型名 + 块结构，不给完整 PDF）
2. 信号模型 + 帧结构：接收信号 r_k = h_b · s_k · e^{jθ} + n_k；pilot spacing 每 4 符号 1 pilot = 25% overhead = 1.25 dB。引 Shieh-Djordjevic 2010。（对齐 R010 §2.2）
3. 相位噪声模型：Wiener PN，σ²_θ = 2πΔνT_s（一句话，首次出现注 "= σ²_p in [B11]"）

**用哪些数字**：pilot overhead 1.25 dB；M₀=8；α,β/Δν/N_blk/N_DFT 进参数表（P2-A，正文不列全表，引"parameters are summarized in Table I"——注：Tab.1 是增益表不是参数表，参数在正文一句话给关键值）
**用哪些公式**：GG 模型 + pilot overhead 用**文字 + 数字**（不编号公式）；σ²_θ = 2πΔνT_s 参数定义级一句话
**用哪些图表**：Fig.1 系统框图（占位，S006 已有 SVG）

### §III Method（1-2 段，R010 §3.1/§3.2）

**论点（段落级）**：
1. DA 估计器（公式 1）：θ̂_DA = angle(r_p · p*)，用已知 pilot 除调制。代码 `_recovery.py:153`。一句话解释。（对齐 R010 §2.3 = 直接给结论级）
2. NDA 估计器（公式 2）：θ̂_NDA = (1/M₀)angle(Σ r_k^{M₀})，升 M₀=8 次幂去调制。代码 `_recovery.py:213,232-233`。一句话解释。引 V&V 1983 + squaring loss 文字结论（**不推导**）。
3. per-block SNR + 切换规则（公式 3）：γ_blk = |h_b|²E_s/N₀；切换规则（文字）："select θ̂_DA when γ_blk < γ_th, else θ̂_NDA"。切换 = **自适应选优**（R008），用文字 + 框图描述（不用伪代码，R010 §3.1）。
4. 创新点定位（1 段，R010 §3.2）：切换是"per-block SNR 驱动的 DA/NDA 自适应选择"，定位=量化归因型。不夸"提出新算法"。

**用哪些数字**：M₀=8（公式里）；切换选对率 26/29 可在这提一句或留 Results
**用哪些公式**：公式 1（DA）+ 公式 2（NDA）+ 公式 3（per-block SNR + 切换规则）
**用哪些图表**：Fig.1 框图已在 §II；切换流程用文字（R010 §3.1：文字+框图非伪代码）

### §IV Results（两段式，R007 落点，R010 §4）

**§IV-A 影响分析（湍流对 DA/NDA 各自性能的影响）**：
1. BER 曲线呈现（Fig.2，6 子图）：DA/NDA 各自 BER vs SNR，分场景。纵轴不硬凑 1e-5（对齐 Paillier，R004/H002）。加 AWGN 理论线隐式 baseline（对齐 Johst）。
2. crossover 数据事实（Fig.4）：DA/NDA BER 曲线有交叉点，交叉点随湍流左移（weak 17.9 / mod 16.8 / strong 10.7 dB）。**只呈现数据不附物理归因**（R009）。

**§IV-B 方法增益（切换的增益数字）**：
1. 切换 vs 固定 NDA（低 SNR 避险）+1.3~2.3 dB（正文，net 口径，CI 下界全正）
2. 净增益量化归因（Tab.1）：强湍流/上行 naive +1.26~1.85 dB；弱湍流 naive 归零诚实标注（+0.09/0.18/0.19，CI 重叠，不变量 3）
3. 切换选对率 26/29（data 口径，R008）

**用哪些数字**：crossover 17.9/16.8/10.7（§IV-A）；切换 vs NDA +1.3~2.3 / 净增益 +1.26~1.85 / 选对率 26/29（§IV-B）
**用哪些公式**：无（Results 不放新公式，引用 §III 的）
**用哪些图表**：Fig.2（BER 主图）+ Fig.3（净增益方案）+ Fig.4（crossover）+ Tab.1（增益汇总）

### §V Conclusion（1 段，3-5 句，R010 §5）

**论点（段落级）**：
1. 复述贡献：per-block SNR 驱动的自适应估计器切换，26/29 选对率，净增益强湍流 +1.85 dB（naive）
2. 诚实标注局限：弱湍流 naive 增益归零（不变量 3）
3. Future：更强判据 / 更多湍流场景 / 上行链路验证

**用哪些数字**：26/29 + 1.85 dB（复述）
**用哪些公式/图表**：无

---

## P3-B 两段式落点确认

R007 两段式（影响分析 + 方法）落在 **Results 内拆 §IV-A / §IV-B**（不是砍成两章，是叙事偏向）：
- **§IV-A 影响分析**：湍流对 DA/NDA 各自性能的影响（Fig.2 BER 曲线 + Fig.4 crossover 数据载体）。先建立"湍流怎么影响两法"的认知。
- **§IV-B 方法增益**：切换的增益数字（vs 固定 NDA +1.3~2.3 / 净增益 Tab.1 / 选对率 26/29）。在影响分析基础上讲切换怎么兑现增益。

**叙事逻辑**：先讲"湍流让两法各有优势区"（影响分析）→ 再讲"切换跨场景自动选优"（方法增益）。导师第 1 点（两段式）+ 第 4 点（切换重新定位）落地。

---

## P3-C 切换 framing 确认

切换定位 = **"跨场景自适应选优"**（R008），全篇统一：
- Intro 贡献句："selecting the locally optimal estimator in 26 of 29 operating points"
- Method §III：切换 = per-block SNR 驱动的自适应选择
- Results §IV-B：切换 vs 固定 NDA 避险增益 + 选对率
- Conclusion：复述自适应选优

**禁用措辞**（grep 确认全篇无残留）：❌ "鲁棒性补丁" / "robustness patch" / ❌ "切换是闭环必要环节"（D002 已推翻）/ ❌ "crossover 物理归因"（R009）

---

## 交叉检查

### 检查 1：P3 大纲用的数字 = P2-B 数字清单里的

| P3 引用的数字 | P2-B # | 一致？|
|---|---|---|
| 26/29 选对率 | #7 | ✅ |
| 1.85 dB（naive）| #2 | ✅ |
| 1.26 dB（naive）| #1 | ✅ |
| crossover 17.9/16.8/10.7 | #8 | ✅ |
| 切换 vs NDA +1.3~2.3 | #5 | ✅ |
| 弱湍流 naive +0.09/0.18/0.19 | #4 | ✅ |
| pilot overhead 1.25 dB | #9 | ✅ |
| M₀=8 | #10 | ✅ |

无"大纲写了但数字清单没有"的数字。✅

### 检查 2：P3 大纲用的公式 = R011 公式清单里的（符号一致）

| P3 引用的公式 | R011 公式 | 符号 | 一致？|
|---|---|---|---|
| §III 公式 1 DA | R011 #1 θ̂_DA=angle(r_p·p*) | θ̂_DA, r_p, p* | ✅ |
| §III 公式 2 NDA | R011 #2 θ̂_NDA=(1/M₀)angle(Σr^M₀) | θ̂_NDA, M₀, r_k | ✅ |
| §III 公式 3 per-block SNR | R011 #3 γ_blk=\|h_b\|²E_s/N₀ | γ_blk, h_b, E_s, N₀ | ✅ |

✅ 无新公式引入

### 检查 3：篇幅对齐 R010

| 节 | R010 基准 | P3 大纲 | 一致？|
|---|---|---|---|
| Intro | 1-2 段 ~8-15 行 | 2 段（背景+gap+贡献）| ✅ |
| System Model | GG 模型 + 块结构 + 帧结构 | 1-2 段（GG+信号+帧+PN）| ✅ |
| Method | 文字+框图，非伪代码 | 1-2 段（DA+NDA+切换，文字+框图）| ✅ |
| Results | BER 主图 + 文字段对比 | 两段式 §IV-A/§IV-B | ✅ |
| Conclusion | 1 段 3-5 句 | 1 段（复述+局限+future）| ✅ |

✅ 不多不少

### 检查 4：切换 framing 全篇统一"自适应选优"

全大纲（§I-§V）切换描述统一用"per-block SNR-driven estimator switching" + "selecting the locally optimal estimator"。无"鲁棒性补丁"残留。✅

**交叉检查全部通过 ✓**

---

## 结论

D-P2P3 完成。P2 + P3 串行产出：

1. **参数表**（P2-A）：4 类参数（信号调制/信道/帧结构/实验矩阵），每个标 `_b11_params.py` 行号 + 文献来源（TL-26）。σ²_θ 首次出现注 B11 对应关系。
2. **数字呈现方案**（P2-B）：口径主报 naive（代码行核验 fair=naive+1.249）；10 条数字清单标进正文/表/图 + 口径 + 来源 + 验证状态；口径标注脚注模板；CI 策略（不报 CI 是领域惯例）；数字-图表映射。
3. **5 节大纲**（P3-A）：R009 逻辑链分配到 Intro/SM/Method/Results/Conclusion，每节标论点/数字/公式/图表占位。
4. **两段式落 Results §IV-A/§IV-B**（P3-B）：影响分析 + 方法增益，叙事逻辑"湍流影响→切换兑现"。
5. **切换 framing = 自适应选优**（P3-C）：全篇统一，禁"鲁棒性补丁"。

交叉检查 4 项全过（数字/公式/篇幅/framing 一致）。

## 对决策的影响

- **不新建 D###**：本文件是 research note（D-P2P3 产出），不改方向/架构决策。所有数字来自已验证的 D002/D004/D005 + 代码行核验。
- **口径加减方向代码行核验通过**（fair_comparison.py:109）：fair = naive + 1.249，naive = fair − 1.249。strong naive=1.260 ✓ / up_str naive=1.852 ✓。
- **等导师 3 项不阻塞**：①10⁻⁵ 纵轴（D003，已定对齐 Paillier 不硬凑）②口径 fair/naive（D004，已定主报 naive）③主对比文献（不阻塞叙事结构）。
- **θ vs φ 决定记录**：沿用 R011 决定，正文用 θ/θ̂，§II 首次出现注 "= σ²_p in [B11]"（σ²_θ 对应 B11 的 σ²_p）。
- **守质量红线 8 条全过**：①参数溯源（标文献）②口径代码行验证（fair_comparison.py:109）③数据真实（弱湍流归零不藏）④不自造词（用 R011 术语）⑤不深挖（crossover 只呈现数据）⑥力度对齐 R010 ⑦守 FR-22（只读代码和数据）⑧切换 framing 统一自适应选优。
