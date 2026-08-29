# Coherent FSO 共同平台物理 authority

> T039 | Groundwork Step 1 external authority | 2026-08-30

## 一句话结论

星地相干 FSO 共同平台应把 **Doppler/激光频差、激光相噪和大气幅度/波前起伏**视为真实损伤，把偏振自由度先建模为 **memoryless、可静态或缓慢变化的 2×2 Jones mixing**；**有限 2×2 FIR 仅在明确引入接收机滤波、I/Q timing skew 或其他有 authority 的频率选择性前端时才合法，不能借光纤 PMD 为自由空间通道杜撰 tap memory。**

## 检索与人工审查

- 执行了三组主查询：coherent FSO polarization/Jones、space-ground coherent receiver impairments、DP coherent 2×2 FIR/PMD/filter；对失败的 FIR 过约束查询只做同组关键词修复，并对偏振与时间记忆各做一次窄补检。
- 最终合并池人工审查 82 条元数据，其中正式发表 72 条、预印本 10 条；分级为必读 9、建议读 12、待确认 3、备选 5、排除 53。判断依据是 title、abstract、venue、year、citation count 与 publication status，不采用工具 relevance score 代替语义判断。
- 实际返回来源为 OpenAlex 与 arXiv；Semantic Scholar 多次限速，SerpAPI/Exa 未配置。两源覆盖足以完成本 T 的 bounded authority 判读，但第三独立元数据源仍记为 `UNKNOWN`，不伪装成三源 PASS。
- 可机读审查表：`search-archive/2026-08-30/coherent-fso-platform-authority.json`。

## 损伤 authority 表

| 损伤 | 物理来源与星地相关性 | authority 给出的量级/时间尺度 | 可否主动扫描 | 直接证据 |
|---|---|---|---|---|
| SOP / Jones mixing | 双偏振发射与 polarization-diversity coherent receiver 的基底不一致、偏振光学器件和大气对 vector beam 的偏振扰动会形成 2×2 mixing。星地相关，但当前证据不支持把它自动写成多 tap 通道。 | Dong 2023 表明湍流下 Stokes/偏振波动存在，但整体弱于强度闪烁；星地 DP 链的 Jones 转速、相干时间与旋转角方差均未获得可引用数值。 | **仅允许结构性扫描**：静态/准静态、单位ary 或轻微非单位ary的单 tap Jones matrix。动态速率不扫描，直到 Step 2 获得星地实测或器件 authority。 | Dong et al., 2023, [“Stokes scintillations for vector beams in turbulence”](https://doi.org/10.3788/COL202321.100101)；Schranz & Udvary, 2021, [“Error probability in polarization sensitive communication systems…”](https://doi.org/10.1007/s11082-020-02690-1)；Roudas et al., 2009, [“Optimal Polarization Demultiplexing…”](https://doi.org/10.1109/JLT.2009.2035526)。 |
| PDL | 可来自偏振选择性耦合器、PBS、滤波器、探测器 responsivity/gain 不一致；不是由“存在双偏振”自动产生。星地相关性取决于实际光学前端。 | Yu 2013 的 1/3/5 dB 是 100-G PDM-QPSK **光纤仿真**的人为 PDL 扫描，不是星地接收机量级；本平台 PDL 数值为 `UNKNOWN`。 | **当前 NO**。没有接收机器件/链路预算 authority 前，不主动加 1–5 dB PDL 画 headroom。可在以后作为硬件敏感性附加轴，而非 Ch4 主损伤。 | Roudas et al., 2009, [JLT](https://doi.org/10.1109/JLT.2009.2035526) 给出 unitary/PDL 条件；Yu et al., 2013, [JLT](https://doi.org/10.1109/JLT.2013.2281100) 明确其 1/3/5 dB 扫描和长距 SSMF 场景。 |
| PMD / DGD | PMD 来自光纤随机双折射导致的差分群时延；检到的 coherent DSP 文献均在 SSMF/长距光纤语境使用 PMD。当前没有星地大气通道 PMD/DGD 的直接 authority。 | 星地量级 `UNKNOWN`；光纤论文数值不得迁移。 | **NO**。当前不把 PMD 作为 FSO 主动损伤，也不以它证明多 tap FIR 合法。 | Kuschnerov et al., 2009, [“DSP for Coherent Single-Carrier Receivers”](https://doi.org/10.1109/JLT.2009.2024963)；Yu et al., 2013, [JLT](https://doi.org/10.1109/JLT.2013.2281100)。两者都是光纤 authority，恰好限定了不可迁移边界。 |
| 接收滤波 / 等效 ISI | coherent receiver 的光/电滤波、ADC 任意 sampling phase、I/Q timing-delay skew 可产生 receiver-side memory；这与大气传播记忆是两件事。 | 经典实现以 2 samples/symbol 的 adaptive equalizer 工作；当前共同平台的 filter shape、3-dB bandwidth、group delay、skew 与所需 tap 数均为 `UNKNOWN`。 | **CONDITIONAL**。只有先冻结具体前端传递函数或 timing skew authority，才允许短 2×2 FIR；否则默认单 tap Jones，不扫描人工 ISI。 | Faruk & Kikuchi, 2011, [“Adaptive frequency-domain equalization…”](https://doi.org/10.1364/OE.19.012789)；Faruk & Kikuchi, 2013, [“Compensation for I/Q Imbalance…”](https://doi.org/10.1109/JPHOT.2013.2251872)；Kuschnerov et al., 2009, [JLT](https://doi.org/10.1109/JLT.2009.2024963)。 |
| CFO / Doppler | 卫星相对运动产生大 Doppler，Tx/LO 激光频差叠加其上；粗频偏估计后仍需细跟踪。星地下行直接相关。 | Paillier 2019 演示 digital PLL 补偿 300 MHz residual mismatch、收敛时间 <1 s；2020 JLT refined model 报告 PLL 在数百微秒收敛。Vieira 2023 说明 LEO optical Doppler 幅度可远高于光纤常见频偏而导数相对较低，但摘要未给出统一数值。 | **平台真实，但不作为 Ch4 主扫描轴**。testbed 应显式声明“coarse FOE 已完成”，仅保留固定、小残差给 Ch3 CPR/同步正确性检查；不得和 PDL/PMD/人工 residual 一起叠加制造 Ch4 收益。 | Paillier et al., 2019, [ICSOS](https://doi.org/10.1109/ICSOS45490.2019.8978983)；Paillier et al., 2020, [JLT](https://doi.org/10.1109/JLT.2020.3003561)；Vieira et al., 2023, [IEEE Access](https://doi.org/10.1109/ACCESS.2023.3287501)；Bernini et al., 2022, [ICSOS](https://doi.org/10.1109/ICSOS53063.2022.9749703)。 |
| 激光相噪 / turbulence-induced phase | Tx/LO laser phase noise、AO 后残余波前/相位波动进入 coherent carrier recovery。星地直接相关。 | Paillier 2020 将 residual amplitude fluctuation 与 laser phase noise 判为主要性能损伤，并报告 fine PLL 数百微秒收敛；目标 laser linewidth 与相位噪声 PSD 仍为 `UNKNOWN`。 | **平台真实，但由 Ch3 承重**。Ch4/Ch5 不再独立扫描；共同链只保持与 Ch3 已冻结模型一致的相噪参数。 | Paillier et al., 2020, [JLT](https://doi.org/10.1109/JLT.2020.3003561)；Bernini et al., 2022, [satellite coherent receiver architecture](https://doi.org/10.1109/ICSOS53063.2022.9749703)。 |

## 有限 2×2 FIR 判决

**判决：`CONDITIONAL`，并拆成一个默认 NO 与一个窄 YES。**

1. **默认 NO：不允许把星地大气传播写成任意多 tap 2×2 FIR。** 当前直接星地文献的核心损伤是湍流引起的幅度/波前起伏、Doppler/频差和激光相噪；没有得到星地 PMD/DGD 或 atmospheric baseband ISI 的量级 authority。Jones mixing 本身只推出 2×2 matrix，不推出 tap memory。
2. **窄 YES：接收机前端存在已定义的频率选择性时，可用有限 2×2 FIR。** 合法来源限于有明确传递函数/量级的 optical/electrical filter、ADC sampling phase、I/Q timing skew，或以后取得直接星地 authority 的其他差分时延。此时 FIR 的 claim 必须写成 receiver-front-end equalization，不写成 atmospheric PMD compensation。
3. **首轮共同 testbed 默认值：单 tap 2×2 complex Jones matrix。** 若要检验 Ch4 的多 tap 方法，Step 2 后必须补齐 filter type、normalized bandwidth、group delay/skew、sampling rate 与最短合法 tap span；任一项缺 authority，则多 tap 分支保持 `NOT_AUTHORIZED`。
4. **PDL 不为 FIR 自动背书。** PDL 使矩阵非 unitary，但仍可 memoryless；只有与 DGD/filter/skew 同时存在才需要时域 taps。

## Step 2 必读候选

| 优先级 | 文献 | 全文状态 | 为什么会改变 testbed 决策 |
|---|---|---|---|
| P0 | Paillier et al., 2020, [Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop](https://doi.org/10.1109/JLT.2020.3003561) | OA arXiv PDF 已有 URL，尚未下载入库 | 直接冻结星地下行损伤清单、粗/细 CFO 分工、PLL 时间尺度与相噪承重位置。 |
| P0 | Bernini, Fice & Bałakier, 2022, [Low-power-consumption coherent receiver architecture for satellite optical links](https://doi.org/10.1109/ICSOS53063.2022.9749703) | UCL institutional PDF 可取，尚未下载入库 | 独立核验卫星 coherent receiver 必须处理 Doppler/大气损伤，并约束前端 DSP 架构。 |
| P0 | Vieira, Pita & Mello, 2023, [Modulation and Signal Processing for LEO-LEO Optical Inter-Satellite Links](https://doi.org/10.1109/ACCESS.2023.3287501) | IEEE Access PDF URL 可取，尚未下载入库 | 给出 LEO Doppler 幅度/导数关系，决定 CFO 应作为同步前置而非 Ch4 headroom。 |
| P0 | Dong et al., 2023, [Stokes scintillations for vector beams in turbulence](https://doi.org/10.3788/COL202321.100101) | 身份与 DOI 可核；搜索元数据未给直接 PDF，待 Step 2 获取 | 限定“大气导致 SOP 扰动”的强度与 claim，不允许从偏振波动跳到高阶 FIR。 |
| P0 | Roudas et al., 2009, [Optimal Polarization Demultiplexing for Coherent Optical Communications Systems](https://doi.org/10.1109/JLT.2009.2035526) | 正式 JLT；当前无 OA PDF 指针，可能需机构访问 | 冻结无 PMD 时的 memoryless 2×2 模型、unitary 条件和 PDL 边界。 |
| P0 | Faruk & Kikuchi, 2011, [Adaptive frequency-domain equalization in digital coherent optical receivers](https://doi.org/10.1364/OE.19.012789) | DOI/OA 指针可取，尚未下载入库 | 证明 2 sps butterfly equalizer 合法，但其 taps 服务于接收/线性记忆，不证明 FSO PMD。 |
| P0 | Faruk & Kikuchi, 2013, [Compensation for In-Phase/Quadrature Imbalance in Coherent-Receiver Front End](https://doi.org/10.1109/JPHOT.2013.2251872) | IEEE PDF URL 可取，尚未下载入库 | 给出 receiver-side gain/phase/timing skew 的明确 FIR 来源，是多 tap 窄 YES 的核心依据。 |
| P1 | Kuschnerov et al., 2009, [DSP for Coherent Single-Carrier Receivers](https://doi.org/10.1109/JLT.2009.2024963) | TU/e institutional PDF 可取，尚未下载入库 | 系统区分 CD/PMD/PDL/XPM 的光纤来源与 DSP 模块，防止把 fiber memory 误移植到 FSO。 |

## 仍 UNKNOWN

1. 星地 DP coherent 接收机的实际 Jones rotation rate、coherence time、rotation-angle variance 与是否可按 codeword/frame 常值处理。
2. 共同平台具体 PBS/90° hybrid/photodiode/TIA/ADC 的 PDL、gain mismatch、I/Q phase error、timing skew 和 optical/electrical filter 传递函数。
3. 星地大气传播是否在本论文波特率、孔径和链路长度下产生可观的 differential delay/baseband ISI；当前证据没有确认，不能用光纤 PMD 代替。
4. 目标 Tx/LO laser linewidth、Doppler 全量程、coarse FOE 后 residual CFO 分布与 phase-noise PSD；目前只有 300 MHz residual 示例和 PLL 收敛时间锚。
5. Semantic Scholar 第三源因限速未返回新记录；这不改变本 T 的物理边界，但在正式 Step 1 receipt 中应标 `SOURCE_COVERAGE_PARTIAL`。

## 对 Ch4 / Ch5 的最小影响

- **Ch4**：首个合法对象是 memoryless 2×2 Jones demultiplexing；scaled-unitary/约束 LS 可以在 unitary 与轻微非-unitary矩阵上讨论。任何“时序正则/多 tap FIR”候选必须先取得前端 filter/skew authority，且 claim 限定为 receiver-front-end equalization。PDL、PMD、CFO 不进入首轮联合扫描。
- **Ch5**：继续消费均衡与 CPR 后符号。若后续启用 receiver FIR，demapper 需接收 post-equalization gain/noise covariance 或经验证的标量近似；CFO/相噪由同步/Ch3 清除，不在 Ch5 再造 residual 以制造 LLR/LDPC 收益。
- **共同平台最小冻结项**：DP-(8,8)-16APSK+BICM/LDPC、单 tap 2×2 Jones mixing、大气幅度/波前效应、coarse FOE 后 residual CFO、Ch3 相噪模型；其余 PDL/PMD/FIR memory 均保持关闭或条件态。
