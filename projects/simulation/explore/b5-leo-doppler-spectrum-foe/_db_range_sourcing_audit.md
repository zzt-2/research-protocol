# 阶段 0.2 dB/范围溯源核查 — B5-Q1 关键参数文献来源审计

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 来源: S002（工作对话对话 1）| 日期: 2026-07-08
> 纪律: INVARIANT 12（B5 特殊·饱和池警示）+ TL-26（参数溯源强制）+ FR-26（读原文数值不只引位置）+ V6（v1.3.0 读原文数值）+ 核查机制中性双向
> 守: 阶段 0 不写代码，本文件只做溯源核查

## 核查目标

1. ±4.5GHz 出处（B5 锚 abstract/intro/experiment/conclusion 四处一致声称——0.1a 已修正为五处不含 conclusion）
2. 残频指标全读原文数值（σ<140MHz / <5MHz / ±312.5MHz 精估范围 / BER 1e-3 −48dBm）
3. **[60] Leven 7dB penalty 数字真正出处**（0.1a 发现 B5 锚全文无此数字，需溯源到 [60] Leven 原文或 sat.1553 综述）
4. 残频上限公式 Δfm=fs/8N 出处（sat.1553 引 [60] Leven 公式 27）

## 1. ±4.5GHz 出处溯源（B5 锚全文）

### 主线独立 grep 核查结果

`grep -n "4.5 GHz" papers/doi/10.1016_j.optcom.2024.130981/content.md`：

| 行号 | 段落 | 原文片段 | 语义 |
|---|---|---|---|
| L23 | abstract | "Doppler frequency offset... is as high as ±4.5 GHz" | Doppler 物理范围 |
| L23 | abstract | "frequency offsets capture range is extended to ±4.5 GHz, covering the Doppler frequency offset range" | B5 capture range |
| L29 | intro | "these effects can cause the frequency shift of the received signal within the range of ±4.5 GHz" | Doppler 物理范围 |
| L47 | intro | "capture and track signals in the frequency offset range of [−4.5 GHz, +4.5 GHz]" | B5 capture range |
| L143 | experiment | "the range of Doppler frequency shift under this condition is about [−4.5 GHz, +4.5 GHz]" | Doppler 物理范围（建模自 Ref [6]）|
| L149 | results | "can effectively compensate the Doppler frequency shift up to [−4.5 GHz, +4.5 GHz]" | B5 capture range |

**conclusion L167 不含 ±4.5GHz**（主线 sed 验证 L163-168，conclusion 只复述 ±312.5MHz 精估范围 + ±250MHz 粗补偿残频）。

### 溯源结论

- **±4.5GHz 在 B5 锚五处出现**（L23×2 / L29 / L47 / L143 / L149），数值字面一致 PASS
- **Doppler 物理范围 ±4.5GHz** 出处：L23（abstract）+ L29（intro）+ L143（experiment，建模自 Ref [6] Shoji JLT 2012 OIPLL LEO-to-ground downlink）
- **B5 capture range ±4.5GHz** 出处：L23（abstract）+ L47（intro）+ L149（results）
- **H001 声称"四处含 conclusion"修正**：实际五处，不含 conclusion。这是 H001 的小事实错误，不影响范围优势核心判定（±4.5GHz 在 abstract/intro/experiment 三段确实一致）
- **Doppler 变化率 56 MHz/s** 出处：L147（experiment，建模自 Ref [6] NEO 600km 轨道）

## 2. 残频指标溯源（B5 锚全文，全读原文数值）

| 指标 | 数值 | 行号 | 原文片段 |
|---|---|---|---|
| 粗补偿后残频标准差 | σ < 140 MHz | L23 / L47 | "the standard deviation of the residual frequency offset after coarse frequency offset compensation is less than 140 MHz" |
| 粗补偿后残频最大值 | 250 MHz | L149 / L167 | "the maximum value of the residual frequency offset is 250 MHz... firstly, the laser will have a 250 MHz frequency jitter, and secondly, the algorithmic compensation has errors" |
| 精确补偿后残频 | < 5 MHz | L149 | "the residual frequency offset of the system after precise compensation is approximately less than 5 MHz [20]" |
| 精估范围 | ±312.5 MHz（=B/8）| L57 / L95 / L149 / L167 | L57 "most FOE algorithms compensate for frequency offsets in the range of [−B/8, +B/8], where B is the baud rate [13,15]"；L149 "compensate the Doppler frequency shift up to [−4.5GHz,+4.5GHz] to within [−B/8,+B/8] (corresponding to [−312.5MHz,+312.5MHz])" |
| BER 1e-3 接收灵敏度 | −48 dBm | L149 | "the BER of 1 × 10⁻³ can be obtained at a receiver sensitivity of −48 dBm" |
| 接收功率测试区间 | −51 ~ −10 dBm | L93 / L127 | L93 "For B2B measurement, the system uses ATT1 to adjust the received power from −51 to −10 dBm"；L127 "received power of −10, −45, −48, and −51 dBm" |
| 收敛迭代 | 8 点 FFT 第 4 次 / 16 点 FFT 第 3 次 | L129 / L141 | L129 "reached the precise compensation range at the fourth iteration"；L141 "achieved by the third iteration when the number of points of the FFT is 16 points" |
| 循环周期 | 3 s | L93 | "The process cycles every 3 s" |
| 系数 α | 6×10⁸ | L85 | "the value of α is 6 × 10⁸" |
| 均值滤波 | 1024 组 16 点 FFT | L87 | "1024 sets of 16-point FFT data for mean filtering" |
| 理论估计范围 | ±B/2 | L117 | "the method can theoretically estimate a frequency offset range of [−B/2, +B/2] without considering the coherent receiver bandwidth limitation" |
| 接收机锁定能力 | ≥9 GHz | L147 | "this terrestrial receiver has a locking capability at least in the frequency range of 9 GHz" |
| 预补偿后残频 | 可达 500 MHz | L57 | "the residual frequency offset can still be up to 500 MHz after precompensation is completed" |
| 3dB 带宽 | 1.33 GHz | L115 | "the frequency bandwidth corresponding to a power attenuation of 3 dB is 1.33 GHz" |

### 溯源结论

- **所有残频指标全在 B5 锚全文，标行号 PASS**（FR-26 读原文数值）
- **±312.5MHz 精估范围 = B/8 = 2.5Gbaud/8**：B5 锚 L57 引 [13,15] 定义传统 FOE 范围 [−B/8,+B/8]，L149 换算为 ±312.5MHz。这是传统 FOE 的标准范围定义，B5 的精估范围跟传统 FOE 一致
- **σ<140MHz vs ±312.5MHz 关系**：B5 粗补偿后残频 σ<140MHz（最大 250MHz）< ±312.5MHz 精估范围 → 残频落精估范围保证后续 DSP 可接。这是 B5 范围优势的工程可用性证据
- **250MHz 最大残频含激光 250MHz 抖动**：L149 明确"the laser will have a 250 MHz frequency jitter, and secondly, the algorithmic compensation has errors"——250MHz 最大值不是纯算法误差，含激光器自身抖动。这是 B5 的诚实标注

## 3. [60] Leven 7dB penalty 数字溯源（0.1a 关键修正项）

### 0.1a 发现

子 agent 核查 + 主线独立 grep 确认：**B5 锚全文无 "7 dB" / "penalty" / "Leven" / "[60]"**（grep 全 0 命中，B5 最大 ref [28]）。`_B5-...-increment.md:43` 提到的"[60] Leven differential decoding 500MHz 致 7 dB penalty（L123）"数字**不来自 B5 锚**。

### 主线溯源核查

核查 [60] Leven 原文 `papers/doi/10.1109_lpt.2007.891893/content.md`：

**L123 原文**："OSNR penalty of about 7 dB can be observed for a frequency offset of 500 MHz."

**L111-123 上下文**：
- L111 "There is no penalty due to LO and transmit laser frequency offset observable. This is true for both block phase estimation and differential detection"（有 FE 时无 penalty）
- L123 "In the case of block phase estimation, we were not able to recover any data for frequency offsets larger than 100 MHz. As discussed above, the differential detector is more robust with respect to frequency offset, but an OSNR penalty of about 7 dB can be observed for a frequency offset of 500 MHz."（无 FE 时 block PE >100MHz 失效，differential decoding 500MHz 致 7dB penalty）

**L147 最大容许频偏**："the maximum allowable frequency offset without frequency estimator is 125 and 625 MHz for block phase estimation and differential detection, respectively."

### 溯源结论

- **[60] Leven 7dB penalty 数字溯源 PASS**：数字确实来自 [60] Leven 原文 L123，是 differential decoding **无 FE** 时 500MHz 频偏的 OSNR penalty
- **详评笔记 `_B5-...-increment.md:43` 的"[60] Leven differential decoding 500MHz 致 7 dB penalty（L123）"标注正确**，L123 确实是 [60] Leven 原文行号
- **此数字不是 B5 锚的数字**：B5 锚全文无此数字，详评笔记是引入 [60] Leven 作 B5 对照 baseline 时带的对照数字
- **语义警示**：7dB penalty 是"differential decoding 无 FE 时"的 penalty，不是"B5 vs [60] Leven"的直接对比。B5 vs [60] Leven 的 dB 对比需重新设计实验（[60] Leven 有 FE 时无 penalty，B5 是粗 CFO 不是 FE）。**路径 B 补 dB 对比时不能直接引"7dB penalty"作 B5 增量，需论证对比公平性**

## 4. 残频上限公式 Δfm=fs/8N 溯源（sat.1553 引 [60] Leven 公式 27）

### 主线溯源核查

核查 sat.1553 `papers/doi/10.1002_sat.1553/content.md` L548-559 段：

**sat.1553 L549**："blind methods can actually estimate offsets up to 3.5 GHz, which could be sufficient if large Doppler shifts are precompensated. In addition, the subsequent phase estimation stage can typically handle a small residual carrier frequency offset error, so it is sufficient for the carrier frequency offset compensation to provide only coarse compensation of the carrier frequency offset."

**sat.1553 L549-553**："the maximum residual frequency offset Δfm for the phase estimation stage can be approximated for QPSK as [60]" → 公式 27：**Δfm = fs / 8N**（其中 N 是相位估计用的样本数，fs 是符号率）

**sat.1553 L553**："Most phase estimation algorithms estimate the phase using less than 100 symbols per estimate, so the maximum residual frequency offset is approximately Δfm = 10⁻³ fs"

**sat.1553 L555**："the carrier frequency will drift very slowly relative to the baud rate, for example, at worst up to approximately 1 GHz/s due to the Doppler effect in ISLs [72]"

核查 [60] Leven 原文 L127-147：[60] Leven 给出最大容许频偏公式（基于 M 次幂操作的相位模糊范围），L147 给出实测值 125MHz（block PE）/ 625MHz（differential detection）。

### 溯源结论

- **Δfm=fs/8N 公式出处**：sat.1553 引 [60] Leven（公式 27 是 sat.1553 的公式编号，[60] Leven 原文无此编号但给出同义公式）
- **B5 ±312.5MHz 精估范围 = B/8 = 2.5Gbaud/8 跟 Δfm=fs/8N 是同一公式族**：B5 的精估范围就是 [60] Leven 定义的残频上限（N=1 时 fs/8）。B5 的"残频落 ±312.5MHz 精估范围即完成任务"跟 [60] Leven 粗补偿定义一致——粗 CFO 只需把残频降到精估范围（Δfm）内，后续相位估计级接手
- **sat.1553 "粗补偿即可"结论**：sat.1553 L549 明确"CFO 补偿只需提供粗补偿"，跟 B5 的粗 CFO 定位一致。这是 B5 粗 CFO 的工程动机背书
- **sat.1553 "blind 最适 OSL"结论**：sat.1553 L557 "blind carrier offset methods appear to be the best option for OSL"——B5 是 blind 算法（无 pilot），跟 sat.1553 结论对口
- **sat.1553 SNR penalty 体系**（L353/L416/L424）：sat.1553 用"SNR penalty vs 完美同步系统"作统一评估口径（BER 1e-3 参照）。这是 B5 路径 B 补 dB 对比可参考的公平对照框架——B5 vs [60] Leven 的 dB 对比可用"SNR penalty vs 完美同步"口径

## 5. B5 vs B4 dB 形态对照（饱和池警示，INVARIANT 12）

| 维度 | B5 | B4 | 对照 |
|---|---|---|---|
| dB 形态 | 绝对指标无 dB 对比 | 内部对照 dB（±920MHz @ 0.5dB 灵敏度代价）| B5 比 B4 在 dB 维度更弱 |
| 范围 | ±4.5GHz（15× 传统）| ±920MHz（~3× 传统 ±312.5MHz）| B5 范围远大于 B4 |
| 残频 | σ<140MHz / <5MHz | σ 3.5→1.75 MHz（MSE 4× 改善）| B4 残频更优 |
| 实验形态 | B2B + Arria 10 + PM-QPSK 2.5GBaud | B2B + Arria 10 + PM-QPSK 10Gbps | 同模板（BUPT 团队）|
| 团队 | 青岛大学+CETC 34 所（Jiamin Fan/Cheng Ju/Na Liu）| 同（Na Liu/Cheng Ju）| 同团队 |
| 池定位 | 饱和池 §A 跟 B4 共锚 Paillier 43 篇 | 同 | 切法地图 §C 警示"饱和池是 dB 最难出区" |

**饱和池警示在 B5 的适用性**（INVARIANT 12）：
- 切法地图 §C 警示"Paillier 安全区恰恰是 dB 最难出区"（`_cut-map-final-b1-b12.md:230` 核验后 5 篇落盘 0 篇出 dB）
- B5 走范围维度（不是 dB），路径 C 鲁棒性够格——**B5 不直接跟饱和池的 dB 竞争**，范围 15× 是结构性优势
- **但需 sandbox 验证**：路径 C 的范围优势在湍流下是否仍成立（阶段 0.3 架构定性前置 + sandbox 三方对照验证）

## 6. 参数真相源汇总表（B5Params 草稿前置，阶段 0.5 用）

| 参数 | 数值 | source_type | source | audit_flag | 原文行号 |
|---|---|---|---|---|---|
| Doppler 范围 | ±4.5 GHz | anchor_paper | B5 锚 optcom.2024.130981 | PASS（五处一致）| L23/L29/L47/L143/L149 |
| Doppler 变化率 | 56 MHz/s | anchor_paper | B5 锚 引 Ref [6] Shoji JLT 2012 | PASS | L147 |
| 符号率 | 2.5 GBaud | anchor_paper | B5 锚 | PASS | L23/L47/L89/L91/L93/L109/L167 |
| 波长 | 1550 nm | anchor_paper | B5 锚 | PASS | L23/L29 |
| 轨道高度 | 600 km | anchor_paper | B5 锚 引 Ref [6] NEO | PASS | L143 |
| 精估范围 | ±312.5 MHz（=B/8）| traditional_def | B5 锚 引 [13,15] + [60] Leven 公式 27 | PASS | L57/L95/L149/L167 |
| 粗补偿残频 σ | < 140 MHz | anchor_paper | B5 锚 | PASS | L23/L47 |
| 粗补偿残频 max | 250 MHz（含激光抖动）| anchor_paper | B5 锚 | PASS | L149/L167 |
| 精补偿残频 | < 5 MHz | anchor_paper | B5 锚 | PASS | L149 |
| BER 1e-3 灵敏度 | −48 dBm | anchor_paper | B5 锚 | PASS | L149 |
| 系数 α | 6×10⁸ | anchor_paper | B5 锚 | PASS | L85 |
| 激光线宽 | 20 kHz | anchor_paper | B5 锚（TTX1995）| PASS | L93 |
| ADC 采样率 | 5 GSa/s 8bit | anchor_paper | B5 锚 | PASS | L93/L95 |
| FFT 配置 | 1024 组 16 点 | anchor_paper | B5 锚 | PASS | L87 |
| FPGA 时钟 | 312.5 MHz | anchor_paper | B5 锚 | PASS | L95 |
| [60] Leven 7dB penalty | 7 dB @ 500MHz 无 FE | reference_paper | [60] Leven lpt.2007.891893 | PASS（L123）| L123 |
| [60] Leven 最大容许频偏 | 125MHz（block PE）/ 625MHz（diff decode）无 FE | reference_paper | [60] Leven | PASS | L147 |
| sat.1553 残频上限公式 | Δfm=fs/8N（QPSK, N<100 → 10⁻³fs）| review_paper | sat.1553 引 [60] Leven 公式 27 | PASS | sat.1553 L549-553 |
| sat.1553 blind 估计范围 | 3.5 GHz @ 28 Gbaud | review_paper | sat.1553 | PASS | sat.1553 L549 |
| sat.1553 ISL Doppler rate | ≤1 GHz/s | review_paper | sat.1553 引 [72] | PASS | sat.1553 L555 |

## 7. 溯源核查结论

1. **±4.5GHz 五处一致 PASS**（abstract/intro/experiment/results，不含 conclusion——H001 小事实错误已修正）
2. **残频指标全读原文数值 PASS**（σ<140MHz / 250MHz / <5MHz / ±312.5MHz / BER 1e-3 −48dBm 全标行号）
3. **[60] Leven 7dB penalty 溯源 PASS**：数字来自 [60] Leven 原文 L123（differential decoding 无 FE 时 500MHz 频偏的 OSNR penalty），不是 B5 锚的数字。详评笔记 `_B5-...-increment.md:43` 标注正确
4. **残频上限公式 Δfm=fs/8N 溯源 PASS**：sat.1553 引 [60] Leven，B5 ±312.5MHz 精估范围跟此公式同族（N=1 时 fs/8）。B5 粗 CFO 定位跟 sat.1553 "粗补偿即可"结论一致
5. **B5 vs B4 dB 形态对照**：B5 比 B4 在 dB 维度更弱（B5 无 dB 对比，B4 有 ±920MHz @ 0.5dB 内部对照），但 B5 范围远大于 B4（±4.5GHz vs ±920MHz）
6. **饱和池警示适用性**：B5 走范围维度不直接跟饱和池 dB 竞争，但需 sandbox 验证范围优势在湍流下仍成立

## 8. 对阶段 0.3-0.6 的影响

- **阶段 0.3 架构定性**：[60] Leven 是时域 Mth-power 精细 FE（有 FE 时无 penalty），B5 是频域粗 CFO（残频落精估范围即完成任务）。两者任务环节不同，路径 B 补 dB 对比需论证公平性。前馈归一化后 B5 范围优势是否仍成立是路径 C 的关键前提
- **阶段 0.4 公平对照框架**：sat.1553 "SNR penalty vs 完美同步系统"口径可作 B5 vs [60] Leven 公平对照框架参考。baseline 选 [60] Leven Mth-power 还是传统 FFT FOE 需 0.4 定。工作点 BER 1e-3（B5 锚 + sat.1553 + [60] Leven 一致）vs HD-FEC 3.8e-3（跨候选可比）需 0.4 定
- **阶段 0.5 参数真相源**：B5Params 草稿 20 字段全溯源 PASS（本文件 §6 表），可直接进 0.5 草拟
- **阶段 0.6 文件组织**：short_time_spectrum_foe 接口定义需参考 fft_foe_m0_omega（sc_nda_ml_sim.py:137）作起点骨架，核心算法"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"需新写

## 来源

- S002（本轮工作对话）
- 主线独立 grep 核查（B5 锚全文 ±4.5GHz + 7dB/penalty/Leven + [60] Leven L123/L147 + sat.1553 L548-559）
- `papers/doi/10.1016_j.optcom.2024.130981/content.md`（B5 锚全文 252 行）
- `papers/doi/10.1109_lpt.2007.891893/content.md`（[60] Leven 原文）
- `papers/doi/10.1002_sat.1553/content.md`（sat.1553 综述）
- `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md:43`（详评笔记 7dB penalty 标注，溯源 PASS）
- `_cut-b4b5-paillier-pool.md:30,44`（B4/B5 dB 形态对照）
- `_cut-map-final-b1-b12.md:230`（饱和池警示核验后仍坚挺）
- TL-26（参数溯源强制）+ FR-26（读原文数值）+ V6（v1.3.0 读原文数值）
