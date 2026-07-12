# [R014] 内容映射——对标集 A 组 5 篇内容构成 + 我方缺口（D-R014 产出）

> 2026-07-12 | 关联：专题 2026-07-09-thesis-writing / D-R014 任务 / R010 力度基准表（互补）/ benchmark-paper-set.md A 组
> 数据来源：3 子 agent 并发（A=词数统计 / B=Le Bidan 内容地图 / C=其余 4 篇内容地图）+ 主线亲自核验 W001/W002/W003 英文正文（FR-26）
> 5 篇 content.md 存在性已核验（268/872/148/150/258 行，与 R010 记录一致）

## 调研问题

正文写完但严重偏短（~1628 词，校验目标 1649 差 1.3%）。R010 力度基准表只记了"别人写到什么力度（1-2 句/段落/推导）"，没记"别人用什么**内容**填充"。本轮补这一层：①核实"到底差多少"的硬词数 ②提取每篇每节写什么内容 ③逐节对照找缺口。**只产出加厚依据，不给加厚方案**。

## 发现

---

### 产出 1：词数总表（量化标尺）

**统计方法**：Python 脚本按 markdown 标题切分，`wc -w` 按空白切分。正文词数不含 Abstract/References/引用元数据。公式块（`$$…$$`）词数按原 wc -w 未扣除（公式符号被计为词，Le Bidan §IV 35 公式块虚高最明显）。我方 3 篇只数英文正文段（中文元数据/交叉检查排除）。

| 论文 | venue | 正文词数 | Abstract | Intro | System/Model | Method | Results | Conclusion | 公式块 | 篇幅定位 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Johst** | WiSEE'24 | **4177** | 106 | 377 | 1508¹ | (融 II) | 669+737² | 91 | 0 | 含外场实验，体例特殊 |
| **Le Bidan** | ICSOS'23 | **7935** | 截断³ | 454 | 1334 | **5223** | (融 IV) | 183 | **35** | 期刊/长会议体例，**不可直接比** |
| **Panasiewicz** | MWP'22 | **2650** | 89 | 343 | 1129⁴ | (融 II-III) | 1007⁴ | 171 | 0 | **会议体最精简** |
| **OECC-PSC** | OECC'25 | **2247** | 33 | 424 | —⁵ | 926 | 547 | 350 | 0 | 无独立 SM 节 |
| **Paillier** | ICSOS'19 | **3025** | 144 | 507 | 399 | 1503 | 429 | 187 | 0 | **体例最像会议标准稿** |
| **我方(合计)** | CCISP'26 | **1628** | 165 | 361 | 268 | 281 | 400 | 153 | 5 | 校验 ≈1649 ✓ |

¹ Johst §II "DSP Design" 1508 词含帧结构+CFO+MIMO+CPE 多子节，兼 System Model+Method
² Johst Results = §III 仿真 669 + §V 外场 737（含外场装置/时序描述，体例特殊）
³ Le Bidan Abstract 在源 .md 被标题行吞掉，只剩 Index Terms 残行（≈11 词），真实 abstract 不可得
⁴ Panasiewicz §II(1129)+§III(1007) 含完整 OPLL 描述+结果，System Model 与 Method 融合
⁵ OECC 无独立 System Model，"Proposed MAP"(926) 兼方法+模型

**关键核实结论（回答"差多少"）**：
- **排除不可比项**：Le Bidan(7935, 期刊体例) 和 Johst(4177, 含外场) 不可作 4-6 页会议体例标尺
- **纯会议体例对标集 = Panasiewicz 2650 / OECC-PSC 2247 / Paillier 3025**（150-258 行，4-6 页）
- **我方 1628 词，比最精简的 OECC-PSC(2247) 还少 28%**，比 Panasiewicz(2650) 少 38%，比 Paillier(3025) 少 46%
- **提示词原估"约 3500 词"偏高**——3500 只有含外场的 Johst 达到。**合理目标 2500-3000 词**（对齐 Panasiewicz/Paillier），需加 **~900-1400 词**
- 逐节看：Intro(361)/Conclusion(153)/Abstract(165) **三项不偏短**（在对标集范围内）；偏短集中在 **System Model(268 vs Paillier 399)/Method(281 vs 对标集 926-1503)/Results 缺实验设置段**

**诚实标注的不确定性**：
1. 公式块未扣词：我方 5 个 + Le Bidan 35 个公式块的符号被计为词，Le Bidan §IV 5223 词有公式虚高成分
2. 图表 caption / OCR 文本：Johst/Le Bidan 含图片 OCR 文字块被计入，少量虚高
3. 节名不统一：5 篇无统一节名（DSP Design/Link Model/Coherent Receiver/Proposed Estimator），总表按"功能最接近"对齐，未强行归并

---

### 产出 2：内容地图（每节每段写什么）

#### Le Bidan（最完整，872 行，重点 Method ~340 行/5223 词）

**§I Introduction（4 段 ~454 词）**：
- 段1 [背景铺垫]：卫星降每比特成本，RF→光学 feeder。引[1][2]
- 段2 [背景铺垫]：CNES 2018 立项 GEO 光 feeder，选 56-GBaud DP-QPSK。CCSDS Optical WG 拟纳入相干
- 段3 [动机建立]：COTS 相干收发机为光纤设计(高 SNR)，空间链路功率受限/低 SNR(<0dB)，复用性存疑。引 TBIRD[3]+自定义接收机[4][5]
- 段4 [贡献声明]：**散文式**(无 bullet)+逐节导读 Sec II–V

**§II Link Model（A/B/C，~1334 词，本文无独立 SM，此节即信道/系统模型）**：
- §II-A [方法描述]：离散过采样信道模型，图1(CFO/PN/ASE/PDL)；**明言大气湍流不仿真**(时间尺度≫帧长，靠 AO/FEC/交织)
- §II-B [参数交代]：Es/N0=−6dB、∆ν=600kHz、CFO±5GHz、PDL 5dB、X-Y skew 0.25ns、时钟±30ppm、ROP −60~−55dBm（全套参数）
- §II-C [设计目标陈述]：两目标(提方案+评估)；低延迟/可并行/开销<5%

**§III Frame Format & RX Arch（A/B/C/D，~741 词）**：
- §III-A [对比讨论]：对比 DVB-S2X[8] 与 OIF 400ZR[9]——400ZR 低 SNR 帧捕获失败
- §III-B [参数交代]：帧=前导 H+I 包；η=3.6%；引 400ZR pilot 间距对比
- §III-C/D：架构概述+启动时序(<100µs)

**§IV DSP Algorithms（A–H 八子节，~340 行/5223 词，重点展开）**：
填满 Method 节靠**每个子模块四件套**（动机+算法出处+图/公式+参数数值）+**替代方案对比弃用理由**：
- §IV-A 粗 CFO [动机+方法+参数]：动机=滚降0.1使 CFO>±0.05Rs 滤波失配；用[10]开环 NDA；参数 M=6 候选/N0=4096
- §IV-B 匹配滤波：FSO 无色散=匹配滤波，频域 overlap-save[6][7]
- §IV-C 定时恢复 [方法+图]：图5 框图+图6 MSE vs MCRB；引 Lee[11]
- **§IV-D CMA 均衡（最厚）**[方法+参数+理由]：正则化 CMA 代价函数 **eq(1)**；参数 16抽头/µ=10⁻³/λ=0.7/收敛<30µs；**为何盲非 DD**：低 SNR 错误传播
- §IV-E 帧同步：差分相关度量[16]抗 CFO/PN
- §IV-F 精 CFO [方法+图+理由]：Mengali&Morelli[17]，理由=逼近 ML；图9 MSE vs MCRB
- **§IV-G CPR（对比弃用重点）**[方法+对比]：**V&V[18] 与 BPS[19] 在 Es/N0<5dB 崩溃**(V&V 四次方噪声放大、BPS 错误传播)→改用 pilot-ML[20]+线性插值
- §IV-H 符号检测：算 LLR 软判（极简）

**§V Results（~400 词，2 图无表）**：
- 段1 [实验设置]：指标=未编码 BER+GMI[21]；帧 4160(4.8%开销)；400训练+300捕获+512测量；图11 GMI+图12 BER
- 段2 [现象解释]：主要损伤源分析（8 pilot 跟踪 PN/CFR 负 SNR 劣化/PDL 用 lumped Jones 模型）

**§VI Summary（1 段 ~183 词）**：证明 −6dB 可靠链路+<5%开销；列改进方向；未仿真湍流但计入余量；future hang-up/LEO 适用性

**五问速答**：①Method 340 行靠 A–H 八子模块×四件套(动机+出处+图/公式+参数)+对比弃用，CMA 均衡与 CPR(弃 V&V/BPS)最厚；②Intro 背景铺到项目级(CNES)，贡献散文无 bullet；③System Model=§II，Wiener+ASE，**湍流不仿真**，参数全列；④Results=2 图(GMI+BER)无表无 baseline 对比曲线；⑤Conclusion 单段~4句。

#### Johst（268 行，卖点最贴，DA vs blind）

**Intro（3 段 377 词）**：段1 FSO 背景[1-4]；段2 多孔径分集+post-DSP 合并需低 SNR DSP[5-9]+FEC 阈值 BER≤2·10⁻²+net 100/200Gb/s；段3 预告节

**§II DSP Design（1508 词，兼 SM+Method）**：
- **DA vs blind 对比段（重点，2 段）**[动机/对比]：①blind(CMA[10])收敛慢/低 SNR 不稳/调制格式相关[11][12]；②data-aided 用已知训练符号，**信道估计完全独立于 payload 调制格式**[12][13]——核心论点。选 DA 以减少反馈路径
- 帧结构[参数]：同步 header+CE header 1024 samples+payload+pilot 每 100 符号(≈1% OH)，总 OH≈7.75%。Fig.1
- II-A 帧同步[14]；II-B CFO 两级(coarse±500MHz+fine±62.5MHz)[14]；II-C MIMO CE(OFDM[15]奇偶子载波分极化，ZF≈MMSE)；II-D CPE 两阶段[18](pilot 粗+BPS[17]细，cycle slip 由 pilot 纠正)

**§III Simulation（669 词，低 SNR 稳定性重点）**[数据]：信道 AWGN+PDL+CFO+PN(Wiener)Fig.2；BER-SNR Fig.3(100 MC，BER≥0.44 标 DSP outage 黑点)；**DSP-outage threshold=0dB**，inlay 图 outage 随 SNR 降单调增，-6dB 达≈50%[局限]

**§IV-V 外场（795+737 词）**[参数/数据]：Fig.4 COTS 链路(Tx-DSP/AWG 64GS/s/ECL 1550nm/EDFA/3150m/接收 tracking)；Fig.5 Precv+σI² 时序；**点 A DSP-outage threshold**：DP-16QAM -1.2dB/DP-4QAM -1.8dB 近仿真；段5[局限] SNR<-1dB 孔径 outage 需丢弃

**Conclusion（91 词）**：鲁棒调制无关 DSP 可工作低于 FEC 阈值；future 降 outage+多孔径验证

#### Panasiewicz（148 行，最精简——靠砍了什么）

**Intro（3 段 343 词）**：FSO 优势[1][2]；长距用相干[3]+OPLL 星间[4]，模拟 PD[5][6]不适 fading；提出全数字 OPLL+数字 PD

**§II Coherent Receiver（1129 词）**：A. LEO slant path(仰角20°/700km/Precv -16dBm)；B. 湍流模型(Cn² H-V 三档[2]+风速 ITU-R)；C. OPLL(TIA+OVCO+ADC/DAC+二阶 LF+M2M4 SNR[8])；**相位检测器**：旧法 lookup table 增益依赖 Ps 致不稳→**改进=MAF+atan2**(V&V 变体)，无近似

**§III Implementation（1007 词，含结果）**：A. OPLL 参数(延迟 ADC12ns+atan2 15ns+MAF 10tap→总30ns；Bn 优化[13]=2MHz)；B. Results：Fig.5 strong+60m/s 对比 atan2 vs sine PD（sine 延迟>6ns 不稳，atan2 稳至 30ns）；Fig.6 BER-风速三湍流(各 30 事件均值)

**Conclusion（171 词）**：atan2 PD 可跟踪 fading+容忍延迟；future 硬件实现

**精简分析（重点）**——148 行靠砍了：
- ❌ 无系统级信道模型图细节(只给参数值)
- ❌ 无多格式(仅 QPSK)
- ❌ 无外场实验(纯仿真)
- ❌ 无帧同步/MIMO/CPE 等 DSP 子模块(OPLL 单点)
- ❌ 无 BER-SNR 全曲线(只给 BER-风速)
- ❌ 无 outage/penalty 细拆
保留不能砍的：
- ✅ 湍流模型(Cn²/风速=FSO 身份)
- ✅ OPLL 核心结构(LF transfer function/PD 公式)
- ✅ 对比锚点(atan2 vs sine)
- ✅ 延迟分析(卖点)
- ✅ 三场景×多风速参数扫描(结果密度)

#### OECC-PSC（150 行，公式密度最高，pilot 代价论证）

**Intro（2 段 424 词）**：100G→1.6Tbps+400ZR[1]标准化；高阶 QAM 受相噪限制(256-QAM 最小欧氏距离仅 16-QAM 的 1/4)；**pilot 代价 vs ML/MAP**：PA[4]用 pilot 牺牲谱效；Wang[5] joint ML+MAP——本文扩至 256-QAM+AOPN

**Proposed MAP（926 词，公式密度最高，无独立 SM）**：信号模型 eq(1-3) 极坐标+协方差；PA 估计器 eq(4)→ML eq(5)→ML/MAP 联合 eq(6)→sub-block 重构 eq(7) 完整推导链；**sub-block 尺寸=复杂度/性能权衡关键**

**Numerical Results（547 词）**：Fig.1(b) BER vs 块长(MAP 最优 PA 最差)；Fig.2(a) sub-block 长；Fig.2(b) BER-SNR(达 7% HD-FEC limit SNR≈32dB)；**Fig.2(c) SNR-penalty vs 线宽**（对比重点）：100GBaud/150kHz 时 MAP/PA-ML/PA≈4/5/7.5dB
**注**：abstract 称"收敛至 BCRLB"为理论上界声明，**正文未显式画/推导 BCRLB 曲线**，改以估计器横向 BER/SNR-penalty 对比实证

**Conclusion（350 词，偏长含 future 细节）**

#### Paillier（258 行，唯一有表，体例最像会议标准稿）

**Intro（4 段 507 词）**：相干优于 IM/DD[1][2]；星间已运营[3][4]；星地实验[5]；OPLL 补大频偏[6][7]+OIPLL for LEO[8](9GHz)；**本步假设粗频偏已预补偿，残差由 DPLL 处理**；假设信号功率恒定(fading 留[9])

**§II Coherent Receiver+AO（399 词）**：BPSK 差分+intradyne；AO[5][10]补偿幅相退化；数字接收=AGC+DPLL+detector+diff decoder(Fig.1)

**§III DPLL（1503 词，设计句式重点）**：
- A. Overall：Fig.2 PD+LF+NCO；PD=BPSK MAP[12] eq(1)；低 SNR tanh≈x 得 eq(2)；LF 二阶；NCO 一阶
- **B. Design（公式密集，句式=引模拟 PLL 惯例[13][14]→映射数字→给中间变量→定义指标→讨论权衡）**：线性化→识别 ξ,ωnT；定义 hold-in/pull-in range/pull-in time Tp；**CRB 下界[12]**；BPSK squaring loss SL eq(11/12)；Fig.3 phase error variance vs SNR(BLT=0.005/0.0005)；cycle-slip；**BLT=噪声敏感 vs 收敛速度权衡**

**§IV Design Example（429 词，两表所在）**[参数/数据]：起点 BLT=0.0005；**Table I（环路参数）**：fL 10GHz/BL 5MHz/ΩPO 14MHz/K1 1.3e-3/K2 6.7e-4（功能=固化设计）；比较 30/100/300MHz；Fig.4-6 acquisition；**Table II（pull-in time）**：30MHz→0.12ms/100MHz→1.4ms/300MHz→12ms（功能=验证模拟公式估 Tp 准确）

**Conclusion（187 词）**：AO+DPLL 架构；pull-in time 可用模拟 PLL 公式估；<1s 可行；fading 留[9]

---

### 产出 3：逐节缺口清单（对标集驱动，不是拍脑袋）

**判定规则**：3/5 或以上对标集有、我方没有 → **明确缺口**（加厚依据强）；2/5 有 → **可选缺口**；≤1/5 → 不是缺口。**缺口清单只列"别人有我没"，不给加厚方案。**

#### §I Introduction 缺口

| 内容项 | Le Bidan | Johst | Panas. | OECC | Paillier | 我方 | 缺口判定 |
|---|---|---|---|---|---|---|---|
| FSO/卫星通信大背景 | ✓ 段1 | ✓ 段1 | ✓ 段1 | ✓ 段1 | ✓ 段1 | ✓ 段1 | 5/5 都有，不是缺口 |
| 湍流/相干检测技术背景 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5/5 都有 |
| 具体项目/标准化背景(CNES/400ZR/多孔径需求) | ✓ 段2 | ✓ 段2 | ✗ | ✓ 段1 | ✗ | ✗ | **3/5 有→可选缺口**（我方学术定位可能不合） |
| 现有方法局限/gap | ✓ COTS 复用存疑 | ✓ blind 低 SNR 不稳 | ✓ 模拟 PD 不适 fading | ✓ pilot 牺牲谱效 | ✓ OPLL 残余 Doppler | ✓ DA/NDA trade-off | 5/5 都有 |
| 贡献声明(散文式) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5/5 都有 |
| 逐节路标 | ✓ 段4 | ✓ 段3 | ✗ | ✗ | ✓ 段4 | ✓(简短) | 3/5 有，我有 |

**§I 缺口结论**：Intro 主体内容项全覆盖。唯一可选缺口是"具体项目/标准化背景"（3/5 有），但与我方学术方法论文定位（非项目报告）可能不契合——**可选，非明确缺口**。词数 361 不偏短（对标集 Intro 343-507，我方在范围内接近 Panasiewicz 343）。

#### §II System Model 缺口

| 内容项 | Le Bidan | Johst | Panas. | OECC | Paillier | 我方 | 缺口判定 |
|---|---|---|---|---|---|---|---|
| 信道模型(湍流/GG/Cn²) | ✓(声明不仿真) | ✓(图给) | ✓(Cn² H-V) | ✓(信号模型) | ✗(推[9]) | ✓(GG+αβ) | 5/5 有，我有 |
| 信号模型公式(r=...+n) | ✗ | ✗ | ✗ | ✓ eq1-3 | ✓ | ✓ r_k | 3/5 有，我有 |
| 参数列表/链路预算 | ✓(全套) | ✓ | ✓(-16dBm) | ✓ | ✓ | ✓(进正文) | 5/5 有，我有 |
| 帧结构(pilot/overhead) | ✓ §III-B | ✓ Fig.1 | ✗ | ✗ | ✗ | ✓ | 3/5 有，我有 |
| 相位噪声模型(Wiener/线宽) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | 4/5 有，我有 |
| 接收机架构/框图 | ✓ | ✓ | ✓ | ✗ | ✓ Fig.1 | ✓ Fig.1 占位 | 4/5 有，我有 |
| 链路几何(仰角/距离/轨道) | ✗ | ✗ | ✓(20°/700km) | ✗ | ✓(LEO) | ✗ | **2/5 有→可选缺口**（块衰落仿真只依赖 αβ，不依赖几何） |

**§II 缺口结论**：SM 主体内容全覆盖。唯一可选缺口"链路几何"(2/5)与我方块衰落仿真设定有关（只依赖 αβ 不依赖具体仰角/距离）。词数 268 偏薄（Paillier 399），但内容项不缺。

#### §III Method 缺口（最大缺口区）

| 内容项 | Le Bidan | Johst | Panas. | OECC | Paillier | 我方 | 缺口判定 |
|---|---|---|---|---|---|---|---|
| 逐子模块/步骤叙述 | ✓(8 模块 A-H) | ✓(5 子节) | ✓(OPLL 组件) | ✓(MAP 推导步) | ✓(PD/LF/NCO) | ✗(仅 DA/NDA/切换 3 点) | 5/5 有我没→**明确缺口**¹ |
| 每步动机(为什么需要) | ✓(每模块) | ✓ | ✓ | ✓ | ✓ | ✗ | 5/5 有我没→**明确缺口** |
| 算法出处/文献引用 | ✓(密集) | ✓ | ✓ | ✓ | ✓ | ✓(V&V) | 有但**稀疏**(我方仅引 V&V，对标集每步引多处) |
| 参数数值 | ✓(多) | ✓ | ✓ | ✓ | ✓ | ✓(M₀/γ_th) | 有但**少** |
| **替代方案对比+弃用理由** | ✓(弃 V&V/BPS) | ✓(DA vs blind) | ✓(atan2 vs sine) | ✓(PA/ML/MAP) | ✗ | ✗ | **4/5 有我没→明确缺口** |
| **设计权衡讨论** | ✓ | ✓ | ✓(延迟) | ✓(复杂度/性能) | ✓(BLT 权衡) | ✗ | 5/5 有我没→**明确缺口** |
| 公式(估计器核心) | ✓ eq1 CMA | ✗(定义级) | ✓(PD 公式) | ✓(推导链) | ✓(环路) | ✓(3 公式) | 4/5 有，我有 |

¹ "逐子模块"缺口需打折看：对标集 Method 长是因为方法本身复杂（完整 DSP 链/OPLL 环路），**我方方法本质简洁（DA/NDA 二选一+切换），没有 8 个子模块可写**。这是方法简洁性决定，不完全是缺内容。但"替代方案对比"和"设计权衡"是真实可加厚的缺口。

**§III 明确缺口**：
1. **替代方案对比+弃用理由**（4/5 有）：对标集都讨论"为什么选这个不选那个"——Le Bidan 弃 V&V/BPS 因低 SNR 崩溃、Johst 选 DA 因独立于调制格式、Panasiewicz 选 atan2 因增益不依赖 Ps。**我方 §III 只说"rather than introducing a new estimator"，未展开"为何切换方案优于纯 DA/纯 NDA/其他判据"**
2. **设计权衡讨论**（5/5 有）：γ_th 阈值选择的权衡、切换的代价/复杂度/延迟。**我方完全未讨论**
3. 算法出处引用稀疏（我方仅引 V&V 1983 一处，对标集每步引多处文献）

词数 281 严重偏薄（即使方法简单，对标集最短的也 ~400 词）。

#### §IV Results 缺口

| 内容项 | Le Bidan | Johst | Panas. | OECC | Paillier | 我方 | 缺口判定 |
|---|---|---|---|---|---|---|---|
| **实验设置段(参数/seed/扫描范围)** | ✓(帧4160/400训练/512测量) | ✓(100 MC) | ✓(VPI+Python) | ✓(参数) | ✓(SNR10dB) | ✗(参数散在§II，无独立设置段) | **5/5 有我没→明确缺口** |
| BER/性能曲线图描述 | ✓ 图11/12 | ✓ Fig.3 | ✓ Fig.6 | ✓ Fig.1/2 | ✓ Fig.3 | ✓ Fig.2 | 都有 |
| 关键数字+口径(dB 增益/FEC 门限) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 都有 |
| 现象解释/结果解读 | ✓ 段2(损伤源) | ✓(PDL penalty) | ✓(风速vs湍流主导) | ✗ | ✗ | ✗(只报数字) | 3/5 有→**可选缺口**² |
| baseline/对比曲线 | ✗ | ✓(AWGN 线) | ✓(atan2 vs sine) | ✓(PA/ML/MAP 同图) | ✗ | ✓(AWGN+DA/NDA 同图) | 3/5 有，我有 |
| 表 | ✗ | ✗ | ✗ | ✗ | ✓(2 表) | ✓(Tab.1) | 1/5 有，我有(增量亮点) |
| 局限/outage 说明 | ✓ | ✓(outage threshold) | ✗ | ✗ | ✓(fading 留[9]) | ✓(弱湍流归零) | 3/5 有，我有 |

² "现象解释"3/5 有，但 **R009 不变量 7 已定 crossover 只呈现数据不附归因**（用户拍板轻讲）——这是设计选择，**不计为缺口**。

**§IV 明确缺口**：
1. **实验设置段**（5/5 有）：对标集都有一段交代"实验怎么跑的"——Le Bidan(帧结构/训练/测量符号数)、Johst(蒙特卡洛次数)、Panasiewicz(仿真工具)、Paillier(SNR/初始频偏)。**我方无独立设置段**（30 seed/扫描范围/N_blocks 等散见§II 或未提）。这是明确缺口且容易加厚。

词数 400 不偏短（接近 Le Bidan ~400 / Paillier 429）。

#### §V Conclusion + Abstract 缺口

| 内容项 | 5 篇普遍 | 我方 | 判定 |
|---|---|---|---|
| Conclusion 复述贡献+局限+future | 5/5(1段3-5句) | ✓(1段3句) | 无缺口 |
| Abstract 问题+方法+结果 | 5/5 | ✓(4句) | 无缺口 |

**§V+Abstract 无缺口**，对齐对标集。词数 Conclusion 153 / Abstract 165 均在范围。

---

## 结论

### 偏短多少（核实"3500 词"目标）

- **"约 3500 词"目标偏高**：只有含外场实验的 Johst(4177) 达到。纯会议体例（150-258 行）对标集 = OECC 2247 / Panasiewicz 2650 / Paillier 3025
- **我方 1628 词**，比最精简会议对标集(OECC 2247)少 28%
- **合理目标 2500-3000 词**（对齐 Panasiewicz/Paillier），需加 ~900-1400 词
- 偏短**不在 Intro/Conclusion/Abstract**（三项在范围内），集中在 **Method(281) + Results 缺实验设置段 + SM(268) 偏薄**

### 主要缺口在哪几节

**明确缺口**（加厚依据强，对标集 4/5~5/5 有、我方无）：
1. **§III 替代方案对比+弃用理由**（4/5 有）——为何切换优于纯 DA/纯 NDA/其他判据
2. **§III 设计权衡讨论**（5/5 有）——γ_th 选择权衡、切换代价/复杂度
3. **§IV 实验设置段**（5/5 有）——仿真怎么跑(seed/扫描/评估指标)

**可选缺口**（2/5~3/5 有，或受设计约束）：
4. §I 具体项目/标准化背景（3/5 有，学术定位可能不合）
5. §II 链路几何（2/5 有，块衰落仿真设定约束）
6. §IV 现象解释（3/5 有，但 R009 已定不附归因=设计选择非缺口）

**不是缺口的偏短**：Intro/Conclusion/Abstract 内容项全覆盖且词数在范围；§III "逐子模块"缺口需打折（方法本质简洁，非缺内容）。

### 内容 vs 力度（与 R010 的互补关系）

R010 记"别人写到什么**力度**"（1-2 句/段落/推导），本轮记"别人用什么**内容**填充"。两者互补：
- R010 已确保我方**力度对齐**（公式直接给不推导/贡献散文式/文字非伪代码）—— 这些不是缺口
- R014 发现的缺口是**内容项缺失**（对标集有某类内容、我方没有），力度对齐解决不了内容缺失

## 对决策的影响

- **不新建 D###**：本文件是 research note，不改方向/架构决策。缺口判定严格基于"对标集有没有"，不基于"我觉得该写"（守纪律 1）
- **不给加厚方案**：本轮只产出依据（缺口清单 + 词数标尺），**加不加/怎么加是后续用户+主控的决策**（守纪律 2）。本文件不替用户定加厚方案
- **加厚决策的下一步**：等用户/主控基于本缺口清单 + R010 力度基准 + R009 逻辑链，决定①是否加厚（对齐 2500-3000 词目标）②加哪些明确缺口（§III 对比/权衡 + §IV 实验设置段最具性价比）③加多少（不破坏 R010 力度对齐）
- **守 FR-22**：只读已有 content.md + W001/W002/W003，未下载未联网
- **与 R013 改稿章程关系**：R013 是导师反馈后的改稿流程，本缺口清单是"主动加厚"依据（非导师反馈驱动），两者独立。若用户决定加厚，可按 R013 L1-L6 分类纳入批次处理

## 附：加厚决策待用户/主控定（本轮不替定）

缺口清单已给，以下问题留给后续决策（不在本轮范围）：
1. 目标词数定 2500 还是 3000？（对齐 OECC/Panasiewicz 下限还是 Paillier 中位）
2. 三个明确缺口（§III 对比/权衡 + §IV 实验设置）全加还是选加？
3. §III "逐子模块"要不要补（需权衡方法简洁性 vs 篇幅）？
4. 可选缺口（项目背景/链路几何）是否服务我方逻辑链？
