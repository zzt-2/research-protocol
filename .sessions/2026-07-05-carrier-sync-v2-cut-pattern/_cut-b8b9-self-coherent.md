# 切法元数据：B8+B9 自相干联读

> 提取人：子 agent | 日期：2026-07-05 | 范围：B8 RL+GS 自相干 + B9 虚拟载波+DRE 自相干
> 纪律：D018 中性提取（不判 Go/Kill）/ FR-26 证据链（落盘看全文，仅 abstract 标"信息不足"）/ 只标作者名不推断师承 / 切法 ≠ 方法配方 / dB 形态注意口径（dBm 灵敏度 vs SNR penalty dB 不可混，定稿 §3.3 警示 1）
> 落盘状态：B8 锚 jocn.468220 全文 603 行 / B9 锚 jlt.2023.3270673 全文 306 行；池 7 篇——photonics10050493 全文、lcomm.2024.3511129 全文、jocn.503484 仅 abstract、apn.3.3.036007 全文（Gold OA）、lpt.2026.3655104 全文、s24248036 全文（survey）、optlastec.110917 付费墙跳过
> 联读特征：B8（square-law+LPF 自消除 CFO/PN）+ B9（虚拟载波+DRE 自相干）**机制相关**——两点都在"绕开传统载波同步链"，B8/B9 池共享（jocn.503484 同时是 B4/B8 候选，已去重；apn 是 B9 跨场景参考非 cited-by 池主，但被纳入 B9 池因 DRE 机制源头）

---

## 1. B8 RL+GS 自相干切入点切法（6 维，含"绕开载波同步"特征）

**本体**：jocn.468220（Yejun Liu, Kun Chen, Song Song*, Yuan Pan, Yuchen Liu, Lei Guo，重庆邮电大学）。"Reinforcement learning aided geometric shaping and detection for a PAM4 self-canceling coherent FSO communication system." JOCN Vol.15 No.1 pp.16-28, Jan 2023。

**【特征标注——"绕开载波同步"】**：B8 主判定"**本篇无核心 Q#**"是事实（笔记 §7 主判定，如实标不强行凑 Q#）。机制 = IF 信号 I(t) 过 square-law device + LPF 后，频偏 w_if 与相位噪声 ϕ 在基带信号 I_sq'(t) 中"disappear in a self-cancellation way"（content.md 行 99-103 Eq.6），PAM4 因四幅度均正可从平方信号直接判决。**载波同步（CFO/CPR/OPLL）被整体绕过**——content.md 行 119 原文："the system does not have very stringent requirements for laser linewidth"。即 B8 不是"改进载波恢复"，而是"消除载波恢复需求"，与 B1-B5（均在改进 CFO/CPR）本质正交。

1. **大点锚**：自生大点（无外部载波同步大点锚）——B8 自己提出 SCD（self-canceling coherent detection）架构；引 Paillier 2020 [20] 仅作"homodyne 需高性 OPLL"反例（行 77），即 B8 用 heterodyne+square-law 规避 OPLL。**载波同步专题视角下 B8 不锚任何"载波恢复大点"，它本身就是"绕开载波同步"的反向参照**。
2. **切的角度**：**架构替换**（传统 heterodyne + blind estimation CFO/CPR → square-law + LPF 自消除）+ **工具借用**（RL 求最优 PAM4 电幅度集，对比 ACO/PSO/GA）。**两个角度里"架构替换"是载波同步相关的核心——它替换的不是某个载波同步算法，而是"是否需要载波同步"这件事本身**。
3. **dB 形态**：**B8 自身无 dB 性能数字**（全文核验）——性能以 BER 数量级表达（SCD vs DD ROP>-25dBm 低 ~2 orders of magnitude；GS-SCD vs SCD 降 1 order；weak-to-strong 湍流 GS 改善 up to 2 orders）+ SNR 解析式（SNR_PS ≥ SNR_TS whenever SNR_TS ≥ 0.125，行 119 Eq.8-9）。**与定稿 §3.3 警示一致**：BER 量级非 dB，不可与 jphot +2-3dB / L053 +2-3dB 直接横向比。设备参数 dB（MZM 插损 5dB / 消光比 30dB / receiver sensitivity -35dBm）非性能，标"设备参数非增益"。
4. **横向多样性**：在 B8 自己的 5 篇 cited-by 池里，**"绕开载波同步"切法是独占**——3 篇候选（photonics10050493 切 mixing efficiency 物理量 / lcomm.2024.3511129 切 GS 信息论 / jocn.503484 切 cooperative relay），**没有一篇 follow B8 的"自消除绕开载波同步"路线**（见 §4 横向多样性归纳）。B8 在自己池里是孤点。
5. **动机叙事**：**"绕开而非赢"套路**（定稿 §4 第四类 ~10%）——content.md 行 37/47 明言 coherent detection 的二维优势+DSP 复杂度（LO locking / IQ / FOE / CPE）"restrict practical use"，故用 square-law + LPF 让 CFO/PN "self-cancellation"，**不动传统 CFO/CPR 算法本体，换一个维度绕**。RL+GS 是附加维度（"PAM4 不同幅度符号经湍流后方差不同"行 167-175）。
6. **实现复杂度**：**纯仿真**（offline Tx + offline Rx，Fig.5 行 286 框图级，无硬件）——定稿 §5 第一档"最低门槛"。参数齐全（gamma-gamma 湍流 Cn² ∈ [1e-17,1e-13]，1km 地面 FSO，1550nm Tx/1549.84nm LO，linewidth 1kHz，20 Gbps PAM4，IF 20GHz/BPF 15GHz）。**AO/波前畸变未建模（mixing efficiency 假设理想，G 当常数 Eq.14-15 行 193）**——这是 B8 物理前提的相邻缺口。

**范围状态**：**out（地面 FSO）**——terrestrial 1km，Cn² 地面量级，无 LEO Doppler / 星地几何 / pointing error。

---

## 2. B9 虚拟载波+DRE 自相干切入点切法（6 维，含"绕开载波同步链"特征）

**本体**：jlt.2023.3270673（Rajesh K. Patel, Gonçalo A. Domingues, Nuno J. Muga, Armando N. Pinto, Marco A. Fernandes, Gil M. Fernandes, Paulo P. Monteiro, Fernando P. Guiomar）。"Simplified Self-Coherent FSO Transmission Boosted by Digital Resolution Enhancer." JLT Vol.41 No.?? pp.5958-5965, 2023（OFC 2023 [22] 扩展版）。Aveiro 大学 + Instituto de Telecomunicações 联合。

**【特征标注——"绕开载波同步链"】**：B9 自相干架构"绕开"传统 CFO/CPE 链——虚拟载波同源于**数字域生成 + 同一激光器**（content.md 行 23/55 "in the digital domain, avoiding additional hardware to generate and lock the optical carrier"），无 LO → 无独立激光器线宽/频偏对冲问题 → 无传统 OPLL/Costas/V-V 需求；相位恢复走 RX-DSP 后处理（CCF 估计 → DC-Value/KK 相位重建 → DC remover → 上下变频 zero-IF → LMS 51 taps → 判决），**不依赖前馈/反馈载波环路**。虚拟载波既是"功率参考"又是"相位参考"，CSPR≥峰值信号功率是相位可重建硬条件。**与 B1-B5（DSP FOE / OPLL / Gardner TED）正交**——B9 在"用架构替代载波同步"赛道，不在"载波同步算法改进"赛道。

1. **大点锚**：自生大点（OFC 2023 [22] + 自前作 KK-FSO [9] 续作）——B9 是 Patel/Guiomar 团队自前作 KK-FSO [9] 的简化续作（用 virtual carrier 替 optical carrier + DRE 替 RO + DC-Value 替 KK transform）。**载波同步专题视角下 B9 不锚"载波恢复大点"，它锚的是"自相干架构替代载波同步"**。
2. **切的角度**：**架构替换**（optical carrier → virtual carrier 省锁相硬件；KK transform → DC-Value 降 oversampling/CSPR）+ **工具借用**（DRE = Digital Resolution Enhancer，动态量化+block-wise Viterbi 求 MSQE(qeff) 最小，把量化噪声从带内挤到带外）。**DRE 与载波同步正交**（content.md 行 237 RX-DSP 链不感知 DRE，DRE 仅改 SNR 不改 carrier tone 频率/相位）——DRE 是 SNR/量化噪声维度，不是载波同步维度。
3. **dB 形态**：**~3 dB SNR 增益 @ 3 PNOB DAC + DRE**（content.md 行 241 + 行 253 Conclusion 双处一致）+ **~1 dB @ 4 PNOB** + **~0.5 dB @ 5 PNOB**（行 241/253）+ **~0.8 dB @ 5 PNOB 长期测量**（行 245 明确标"可吸收 atmospheric turbulence 随机 SNR 变化"）。**注意口径**：这些是 **SNR 增益 dB**（DRE vs w/o DRE 内部对照，同 virtual carrier 架构），**非"赢传统相干载波同步 baseline 几 dB"**——D005 标尺下需注明"DRE 是 SNR/量化噪声维度增益，非载波同步环路增益"（与定稿 §3.3 警示 1 一致，dB 口径不可混）。**virtual vs optical carrier 架构差**：0.28 GMI penalty @ 4 PNOB / 1.12 GMI @ 3 PNOB（行 109）——这是 GMI（广义互信息）非 dB，再一个口径。
4. **横向多样性**：在 B9 自己的 8 篇 cited-by 池里，**"绕开载波同步链"切法是独占**——4 篇候选（apn 跨场景 DRE IM/DD / lpt FTER ML 量化噪声恢复 / survey 综述重述 / optlastec THz/FSO relaying 跳过），**没有一篇 follow B9 的"虚拟载波自相干绕开载波同步"路线**（见 §4）。B9 在自己池里是孤点，与 B8 同构。
5. **动机叙事**：**"绕开而非赢"+"前作有缺陷→改进"复合套路**——content.md 行 9/23/33 明言 coherent FSO 高速但"high-cost and power consumption"，故用 virtual carrier self-coherent 简化；自前作 KK-FSO [9] 仍有 optical carrier 锁相硬件负担 + KK transform 高采样率，故用 virtual carrier（数字域插入）+ DRE（低 PNOB DAC）+ DC-Value（降 CSPR/oversampling）三件套进一步简化。**典型"不动传统 CFO/CPE 算法本体，用架构替代整个载波同步链"**。
6. **实现复杂度**：**实验室 + outdoor 实测**（地面 42m FSO 链 + clear weather + 6h 长期白天测量，content.md 行 245）——定稿 §5 第四档"高"。参数齐全（30 GBaud PCS-36QAM net 80/100Gbps，roll-off 0.2，CSPR 扫 3-18dB，PNOBs 3/4/5，DRE L=3/5 M=3，LMS 51 taps，AWG Keysight M8194A 8bit 120GSa/s 45GHz BW，SHF 807 放大，IQ MZM，F810APC-1550 collimator，Tektronix RTO）。**未涉深湍流/LEO 长距**——42m 含轻量大气扰动但非典型星地 LEO-地面深湍流信道。

**范围状态**：**in 倾向（地面 FSO 42m）→ 待迁移**（星地深湍流自相干 vs 传统相干对照论证待做）。

---

## 3. B8 池 3 篇 + B9 池 4 篇逐篇 6 维

> 落盘状态说明：B8 池 3 篇（photonics10050493 全文 / lcomm.2024.3511129 全文 / jocn.503484 仅 abstract）；B9 池 4 篇（apn.3.3.036007 全文 Gold OA / lpt.2026.3655104 全文 / s24248036 survey 全文 / optlastec.110917 付费墙）。**去重说明**：jocn.503484 同时是 B4/B8 候选——B4 池把它归"参数调度/场景迁移"类（同 Liu 团队 cooperative），B8 池归"同团队延伸标注非载波同步"，**B4/B8 池共享此篇已去重**。

### 3.1 B8 池

#### 篇 1：photonics10050493 — Effect of Wavefront Distortion on the Performance of Coherent Detection Systems
**DOI/标题**：10.3390/photonics10050493（Photonics 2023, 10, 493，MDPI OA）。Shangjun Yang, Tian Xing, Chenghu Ke, Jingyuan Liang, Xizheng Ke*（西安理工大学 Xi'an University of Technology）。全文 23 页落盘。

1. **大点锚**：自生大点（相干检测 mixing efficiency/gain 的波前畸变理论+实验）——**不锚 B8 的"自消除"点**，锚的是 coherent detection 前端物理量（mixing efficiency η、mixing gain、D/r₀、Zernike 校正阶数）。与 B8 的关系是"直击 B8 盲点"（B8 假设 G 常数，本篇实测 η 仅 36-68%）。
2. **切的角度**：**性能极限/物理建模**（建立 wavefront distortion-mixing efficiency-mixing gain 数学模型 + AO 校正极限分析）+ **硬件实现/实验验证**（Haso4 NIR + DM 40 室内外实验）。**载波同步视角**：本篇在 coherent detection 前端物理层，不在载波同步链——它揭示的是"自相干/相干检测的物理前提（空间相位匹配）在湍流下退化"，是 B8 自消除方案的相邻缺口而非载波同步候选。
3. **dB 形态**：**homodyne 比 heterodyne mixing gain 高 ~3 dB**（abstract 行 19 + content 行 341/367 多处："homodyne detection mixing gain is higher than heterodyne detection of about 3 dB"）；mixing efficiency 校正后室内 36%/47%/62%（tilt/defocus/astigmatism）、室外 36%/51%/68%（abstract 行 19）。**口径警示**：这里 "3 dB" 是 **mixing gain**（homodyne vs heterodyne 检测灵敏度结构差），**非 SNR penalty dB 也非 receiver sensitivity dBm**——与定稿 §3.3 警示 1 同类口径陷阱，横向比"赢 baseline 几 dB"时不可直接套。
4. **横向多样性**：在 B8 5 篇池里属**物理建模独占**（唯一系统量化 wavefront distortion→mixing efficiency→mixing gain 链条 + 室内外实验对照）。
5. **动机叙事**：**"补相干检测物理前提的量化空白"套路**——content 行 45/47 明言 AO 校正"under-compensation 致性能损失 / over-compensation 增复杂度"，故系统建 mixing efficiency/gain 模型 + AO 校正阶数极限 + 室内外实验。
6. **实现复杂度**：**实验室 + outdoor 实测**（室内 LC-SLM 模拟波前畸变 + 室外真实大气，D/r₀=2，D=105mm，λ=1550nm，L=1000m，NKT Photonics 1550nm 窄线宽激光器 + Haso4 NIR + DM 40 + Kylia COH24 + BPDV2150R）——定稿 §5 第四档。**纯仿真部分**：D/r₀ ∈ {0.2,2,5,8} 数值计算 mixing efficiency/gain 极值。

#### 篇 2：lcomm.2024.3511129 — Geometric Constellation Shaping for Wireless Optical Intensity Channels
**DOI/标题**：10.1109/lcomm.2024.3511129（IEEE COMMUNICATIONS LETTERS Vol.29 No.1 Jan 2025）。Suhua Zhou, Tianqi Li, Zhaoxi Fang, Jing Zhou*, Wenyi Zhang（北京信息科技大学 / 绍兴文理学院 / 中科大）。全文落盘。

1. **大点锚**：自生大点（光强度信道 GS 信息论方法）——**不锚 B8 的"自消除"或"载波同步"点**，锚的是 IM/DD 强度信道的几何整形（exponential-like constellation）。与 B8 的关系是"GS 维度对齐但信道模型 IM/DD 非相干"（B8 是 SCD 相干 PAM4，本篇是 IM/DD PAM/连续）。
2. **切的角度**：**性能极限/信息论界**（从 information-theoretic 视角构造 asymptotic optimal exponential-like constellation，high-SNR capacity 可被逼近）+ **参数调度**（constellation levels 用 basic level + b+2 bits 表示，降 DAC 分辨率需求）。**载波同步视角**：本篇完全不涉载波同步——IM/DD 无 LO 无 CFO 无 CPR，是"载波同步需求天然不存在"的极端参照。
3. **dB 形态**：**GS shaping gain 0.65 dB**（abstract 行 9 + content 行 33/51，16-level LDPC coded modulation，IM/DD 强度信道）+ **ultimate shaping gain 1.33 dB**（content 行 33，e/2，理论极限）。**口径警示**：这是 **average optical power shaping gain dB**（exponential-like vs standard PAM，信息论 SNR gap），**非 receiver sensitivity dBm 也非 SNR penalty dB**——定稿 §3.3 警示 1 同类，与 jphot/oe 的 dBm 灵敏度、与 B9 的 SNR 增益 dB **三口径不可直接相加**。
4. **横向多样性**：在 B8 5 篇池里属**信息论独占**（唯一从 capacity asymptotic optimality 角度做 GS）。
5. **动机叙事**：**"标准 PAM 信息论次优→指数型分布逼近 capacity"套路**——content 行 33 明言 AWGN 高斯分布得 capacity、光强度信道 exponential 分布 asymptotic optimal，故用 geometric shaping（equiprobable 非均匀间距）构造 exponential-like constellation。
6. **实现复杂度**：**纯理论 + 仿真**（achievable information rate 评估 + 16-level LDPC coded modulation 仿真，无 hardware demo）——定稿 §5 第一档。

#### 篇 3：jocn.503484 — DRL-enabled cooperative FSO with elastic optical splitter（仅 abstract）
**DOI/标题**：10.1364/jocn.503484（JOCN Vol.16 No.2 pp.193- Jan 2024，订阅闭）。Yejun Liu, Xi Wang, Shasha Liao, Qiming Sun, Shuhua Feng, Lei Guo（**与 B8 锚 jocn.468220 同团队 Liu 等**，重庆邮电大学）。**仅 abstract 可得**（订阅闭，全文未下）。

1. **大点锚**：自生大点（cooperative FSO relay + elastic optical splitter）——**不锚 B8 的"自消除/载波同步"点**，锚的是 cooperative communication 的光功率分配。同团队延伸（B8 锚 Liu 团队的续作）。
2. **切的角度**：**参数调度**（elastic optical splitter 动态调光功率分配 + DRL 做 relay selection/power allocation）+ **架构替换**（fixed splitter → elastic splitter）。**载波同步视角**：本篇完全不涉载波同步——是 cooperative relay + power allocation 赛道。
3. **dB 形态**：**信息不足（abstract 级）**——abstract 只给"BER 改善 1-2 orders of magnitude vs fixed splitter + adaptive scheme 进一步改善 >25%"，**BER 量级非 dB**（与 B8 锚同维度），无 sensitivity/SNR dB。
4. **横向多样性**：在 B8 5 篇池里属**同团队延伸**（唯一与 B8 锚同作者群），主题（cooperative relay）与 B8（self-canceling detection）正交。
5. **动机叙事**：**"前作 fixed splitter 光功率利用不足→elastic + DRL"套路**——abstract 明言"fixed splitter uniformly distribute optical power... insufficient utilization when relay links have different channel statuses"。
6. **实现复杂度**：**信息不足（abstract 级）**——abstract 未明说仿真 vs 硬件，按同团队 B8 锚惯例推断纯仿真，但**未脑补标"待全文"**。

### 3.2 B9 池

#### 篇 1：apn.3.3.036007 — Beyond 200-Gb/s O-band IM/DD with joint LUT predistortion and DRE（Gold OA，跨场景参考）
**DOI/标题**：10.1117/1.APN.3.3.036007（Advanced Photonics Nexus Vol.3(3) May/Jun 2024，Gold OA）。Qi Wu, Zhaopeng Xu*, Yixiao Zhu*, Tonghui Ji, Honglin Ji, Yu Yang, Junpeng Liang, Chen Cheng, Gang Qiao, Zhixue He, Jinlong Wei, Qunbi Zhuge, Weisheng Hu（PCL 深圳 + SJTU 上海交大）。全文 440 行落盘。**跨场景参考**（O-band IM/DD 数据中心 SSMF，非 FSO 非自相干）。

1. **大点锚**：自生大点（DRE + LUT 联合 for beyond 200Gb/s IM/DD）——**DRE 源头同 B9**（Yoffe 2019 [38] / 2020 [42]，apn 与 B9 共用 DRE refs），但 apn 是 IM/DD 单载波 PAM 链，B9 是 virtual carrier + KK/DC-Value 自相干链，**链路结构不同，DRE 跨链路迁移代价未量化**（笔记"场景迁移论证待做"）。
2. **切的角度**：**工具借用**（DRE 动态量化把量化噪声从带内挤到带外，与信道+MF 低通响应协同）+ **参数调度**（LUT memory=3 消 SOA PDE + DRE 省 1 bit DAC）+ **性能极限/记录**（Table 1 IM-DD 低 bit DAC 系统 net data rate 记录：235.3 Gb/s PAM-4 / 289.7 Gb/s PAM-6 / 294.7 Gb/s PAM-8 @ 2km；117.6/173.8/231.8 Gb/s OOK/PAM-3/PAM-4 @ 40km）。**载波同步视角**：IM/DD 无载波同步，DRE 是 SNR/量化噪声维度与载波同步正交（与 B9 一致）。
3. **dB 形态**：**PNoB=4 + DRE → ~0.5 dB ROP sensitivity 增益 @ KP4-FEC**（content 行 179，124-GBd PAM-4 @ 2km，vs w/o DRE 内部对照）；DRE 省 1 bit DAC（行 179）；3-bit DAC + DRE @ ROP -4dBm 达 BER 1.4e-4 < KP4-FEC 2.4e-4（行 179）。**口径警示**：这是 **ROP sensitivity dBm 增益**（vs w/o DRE 内部对照），**非 SNR penalty dB**——定稿 §3.3 警示 1 同类，与 B9 锚的 SNR 增益 dB 不同口径。
4. **横向多样性**：在 B9 8 篇池里属**DRE 机制跨场景延伸独占**（唯一系统验证 DRE 在 IM/DD 单载波 PAM 多调制格式的效果 + Table 1 文献全对比）。
5. **动机叙事**：**"PDE + 量化噪声双瓶颈→LUT+DRE 联合"套路**——content 行 45/49 明言 O-band 衰减需 SOA 但 SOA 引 PDE、LUT/THP/pre-eq 致 PAPR↑→SQNR↓需低 bit DAC 但 DAC 贵，故 DRE 把量化噪声挤带外。
6. **实现复杂度**：**实验室硬件 demo**（DFB + AWG + MZM + SSMF 2/40km + SOA + VOA + PD + Keysight UXR0594AP RTO 62GHz BW，124/112 GBd PAM-4/6/8 + OOK/PAM-3/4）——定稿 §5 第三档。**无 FSO 信道、无湍流**（纯光纤 IM/DD）。

#### 篇 2：lpt.2026.3655104 — Frequency-Temporal Enhanced Recovery (FTER) for ultra-low-resolution ACO-OFDM OWC（ML 路线跨方向参考）
**DOI/标题**：10.1109/lpt.2026.3655104（IEEE PHOTONICS TECHNOLOGY LETTERS Vol.38 No.9 May 2026）。Siyu Bai, Zehua Xu, Chengshang Lyu, Yibin Li, Qian Li, H.Y. Fu*（清华大学深圳国际研究生院 Tsinghua Shenzhen + 港城大 + 北大深圳）。全文落盘。

1. **大点锚**：自生大点（FTER = TCN + 随机森林频域特征选择做量化噪声恢复）——**与 B9 DRE 是机制并列**（DRE 是 DSP 路线 TX 侧预处理，FTER 是 ML 路线 RX 侧后处理），**跨方向参考非 follow**。
2. **切的角度**：**工具借用**（TCN dilated convolution 建模 OFDM 子载波间长程依赖 + 随机森林选频域特征）+ **架构替换**（传统 RO-ZF 接收 → FTER 频域特征+TCN 恢复）。**载波同步视角**：本篇做量化噪声恢复，**不涉载波同步**（ACO-OFDM IM/DD，无 LO 无 CFO）；但与 B9 DRE 同属"低 bit DAC 量化噪声缓解"赛道，机制（DSP vs ML）并列。
3. **dB 形态**：**4-bit + 64-QAM @ 0.75GBaud BER 7.2e-3 → 3.7e-3**（FTER vs RO，content 行 9/121）；3-bit + 32-QAM @ 0.625GBaud BER 9.11e-3 → 3.52e-3（行 105）；**无 dB 数，BER 改善倍数表达**——D005 标尺下与 B8 锚同维度（BER 量级非 dB）。
4. **横向多样性**：在 B9 8 篇池里属**ML 路线独占**（唯一用 TCN+随机森林做量化噪声恢复，与 DRE DSP 路线机制并列）。
5. **动机叙事**：**"传统 DSP（ZF/MMSE）治线性不治量化噪声 + CNN 感受野有限→TCN 长程依赖"套路**——content 行 27/29/43 明言 ZF/MMSE 不能压 QN（非线性信号相关）、CNN 局部感受野难建模 OFDM 子载波长程依赖，故用 TCN dilated + 随机森林频域特征选择。
6. **实现复杂度**：**实验室硬件 demo**（1m VCSEL 680nm OWC 链 + AWG 3-6GSa/s + Tektronix MSO73304DX 6/12.5GSa/s，ACO-OFDM 32/64-QAM 0.375-0.75GBaud，~0.5M 参数 ~20MFLOPs/frame）——定稿 §5 第三档。**1m 短距 OWC，无湍流建模**。

#### 篇 3：s24248036 — Beyond-5G FSO Survey（综述泛指）
**DOI/标题**：10.3390/s24248036（MDPI Sensors 2024, 24, 8036，OA）。Ibrahim A. Alimi, ... Paulo P. Monteiro（**Instituto de Telecomunicações, University of Aveiro——与 B9 锚同机构**）。全文 3364 行落盘（survey，泛指未深读全，但已 grep 锁定 B9 相关段落）。

1. **大点锚**：survey 自身即大点——**直接引用并重述 B9 锚**（[33] Patel et al. 2023 JLT，content 行 2349 refs）+ [26] Muga 2019 ICTON self-coherent + [27] Alimi 2021 Appl. Sci. self-coherent transceivers review（同团队综述）。**B9 锚在 survey §2.3.3 "Self-Coherent FSO Systems"（行 235-257）被作为"DRE+virtual carrier 简化 KK-FSO"的代表例重述**。
2. **切的角度**：**综述延伸**（non-coherent / coherent / self-coherent FSO 三类系统全景对比，Table 1 行 259）+ **场景迁移泛指**（Beyond-5G FSO 全应用谱：UAV/数据中心/星地/水下/deep-space）。**载波同步视角**：survey 行 231-233 给出 coherent detection 的 carrier synchronization 挑战叙述（homodyne 需精确 OPLL / heterodyne intradyne 用 DSP 后处理 FOE+CPR）——**这是把 B1-B5 的载波同步赛道当 background 摆**，self-coherent（B8/B9）作为"绕开"分支单列。
3. **dB 形态**：**survey 自身无原创 dB**——重述他人结果。其中与自相干相关：行 744 POLSK 比 OOK 好 ~3 dB sensitivity / 比 IM 好 ~3 dB（differential detection 免 phase tracking）；行 664 KK receiver 替代 coherent receiver 在 6-mode fiber 下 average received power gain ~6 dB over SMF / 比 SMF-based heterodyne 好 5-6 dB（moderate-to-strong 湍流）。**口径警示**：这些是 survey 转述他人 dB，**口径混杂**（sensitivity dB / power gain dB / heterodyne vs KK 架构差），横向比需回溯原文。
4. **横向多样性**：在 B9 8 篇池里属**综述延伸独占**（唯一把 B9 锚纳入 self-coherent FSO 全景分类的 survey）。
5. **动机叙事**：**"摆全景 + 给基线"套路**（定稿 §4 第五类）——content 行 25/93 abstract 明言 comprehensive survey of enabling technologies/challenges/trends，self-coherent 作为 coherent vs IM/DD 的折中分支。
6. **实现复杂度**：**不适用**（综述无实验，定稿 §5 第一档理论维度）。

#### 篇 4：optlastec.110917 — Mixed THz/FSO Relaying（付费墙跳过）
**DOI/标题**：10.1016/j.optlastec.2024.110917（Optics & Laser Technology, Elsevier，付费墙未下）。标题："Performance analysis of 5G and beyond mixed THz/FSO relaying communication systems"。**metadata 仅 abstract 级，全文付费墙跳过**。

1. **大点锚**：**信息不足**（仅标题+abstract 级 metadata）——按标题推断是 mixed THz/FSO relaying 性能分析，**不涉载波同步也不涉自相干**，是 relaying/性能分析赛道。
2. **切的角度**：**信息不足**——按标题推断是性能分析（outage/BER），属**性能极限/系统级建模**类，但未落盘不可定档。
3. **dB 形态**：**信息不足（付费墙未下）**。
4. **横向多样性**：**信息不足**——按标题是与 B9 自相干正交的 THz/FSO relaying，**池中独占 THz/FSO 混合角度**（中性观察）。
5. **动机叙事**：**信息不足**——按标题推断"5G and beyond THz/FSO 混合 relaying 性能"。
6. **实现复杂度**：**信息不足**——按 Optics & Laser Technology 性质推断多为解析/仿真性能分析，未落盘不强行定档。

---

## 4. 自相干模式归纳（中性，不判 Go/Kill）

### 4.1 大点分布：自相干架构被切的子点
- **B8 锚（square-law 自消除）**：自身就是"绕开载波同步"的大点。被切的子点 = 自身无 follow（5 篇 cited-by 无人 follow 自消除路线）；相邻被切的是**物理前提**（photonics10050493 切 mixing efficiency 波前畸变）+ **GS 维度**（lcomm 切信息论 GS）+ **同团队延伸**（jocn.503484 cooperative relay，非载波同步）。
- **B9 锚（virtual carrier+DRE 自相干）**：自身是"绕开载波同步链"的大点。被切的子点 = **DRE 机制跨场景延伸**（apn IM/DD 数据中心）+ **DRE 机制 ML 路线并列**（lpt FTER）+ **综述重述**（survey §2.3.3 self-coherent 全景）+ **正交 relaying**（optlastec THz/FSO，信息不足）。
- **联读共性**：B8/B9 两点的 cited-by 池里**没有任何一篇 follow"绕开载波同步"本身**——所有 cited-by 都切的是相邻维度（物理前提 / 机制并列 / 跨场景 / 综述 / 同团队延伸），**自相干"绕开"切法在自己池里是孤点独占**。

### 4.2 dB 形态分布：自相干点 dB 多在哪个形态
| 篇 | dB 形态 | 口径 |
|---|---|---|
| B8 锚 | **无 dB（BER 量级）** | BER orders of magnitude |
| B9 锚 | **SNR 增益 dB**（~3/~1/~0.5/~0.8 @ 3/4/5 PNOB + 长期） | SNR dB（vs w/o DRE 内部对照，非传统相干 baseline） |
| photonics10050493 | **mixing gain dB**（homodyne vs heterodyne ~3 dB） | mixing gain 结构差（非 SNR penalty 非灵敏度 dBm） |
| lcomm.2024.3511129 | **shaping gain dB**（0.65 dB / ultimate 1.33 dB） | average optical power SNR gap（信息论） |
| jocn.503484 | **BER 量级**（1-2 orders） | BER orders（abstract） |
| apn.3.3.036007 | **ROP sensitivity dBm 增益**（~0.5 dB @ KP4-FEC） | dBm 灵敏度（vs w/o DRE 内部对照） |
| lpt.2026.3655104 | **无 dB（BER 倍数）** | BER 倍数（7.2e-3→3.7e-3） |
| s24248036 | **survey 转述他人 dB**（POLSK 3dB / KK 6dB，口径混杂） | 转述，需回溯原文 |
| optlastec.110917 | **信息不足** | 付费墙 |

**归纳**：自相干联读 9 篇里，**dB 口径极度碎片化**——BER 量级（B8 锚 / jocn.503484 / lpt）/ SNR 增益 dB（B9 锚）/ mixing gain dB（photonics）/ shaping gain dB（lcomm）/ ROP sensitivity dBm（apn）/ survey 转述混杂（survey）/ 信息不足（optlastec）。**至少 5 种不同口径的 dB**，**横向比"赢 baseline 几 dB"几乎不可直接做**——这与定稿 §3.3 警示 1（dBm 灵敏度 vs SNR penalty dB 不可混）一致，但 B8/B9 联读的口径碎片化比 B1-B5 更严重（B1-B5 主要是 dBm vs dB 两口径，B8/B9 是 5+ 口径）。

### 4.3 横向多样性："绕开载波同步"切法在池里是主流还是独占
**结论：独占（孤点）。**

- B8 5 篇 cited-by 池：0/3 篇候选 follow"自消除绕开载波同步"（photonics 切物理前提 / lcomm 切信息论 GS / jocn.503484 切 cooperative relay）。
- B9 8 篇 cited-by 池：0/4 篇候选 follow"虚拟载波自相干绕开载波同步链"（apn 切 DRE 跨场景 IM/DD / lpt 切 FTER ML 并列 / survey 综述重述 / optlastec THz/FSO 正交）。
- **两点合并 7 篇候选池（jocn.503484 去重）：0/7 follow"绕开载波同步"本身**。所有 cited-by 都切的是相邻/并列/延伸维度。
- **与 B1-B5 对比的关键差异**：B1-B5 的 Spalvieri/Paillier 大池里"载波同步算法改进"是被反复切的主流（场景迁移 11 + 硬件实现 10 + 架构替换 6 + ...），**cited-by 都在 follow 大点的载波同步子环节**；B8/B9 的"绕开载波同步"大点**没有任何 cited-by follow 这条路线**——自相干"绕开"是一个**被引用但不被接力切**的大点。

### 4.4 动机叙事：自相干点常用什么叙事
- **B8/B9 锚共用"绕开而非赢"套路**（定稿 §4 第四类 ~10%，B1-B5 池里是少数派）——B8 行 37/47"coherent DSP 复杂度 restrict practical use → square-law 自消除"、B9 行 9/23"coherent 高成本高功耗 → virtual carrier self-coherent 简化"。**两点都用"不动传统 CFO/CPR 算法本体，换一个维度绕"**。
- **B9 锚叠加"前作有缺陷→改进"套路**（自前作 KK-FSO [9] 简化）。
- **cited-by 池叙事多样**：photonics（补物理前提量化空白）/ lcomm（信息论 capacity 渐近最优）/ jocn.503484（前作 fixed splitter 不足→elastic+DRL）/ apn（PDE+量化噪声双瓶颈→LUT+DRE）/ lpt（传统 DSP+CNN 不足→TCN）/ survey（摆全景给基线）。**cited-by 池叙事与 B8/B9 锚的"绕开"叙事基本不重叠**——cited-by 切的是各自赛道，不是接力"绕开载波同步"。

### 4.5 实现复杂度：自相干点常在哪个档
| 档 | 篇 |
|---|---|
| 纯仿真/理论 | B8 锚 / lcomm / （optlastec 待定）|
| 实验室硬件 demo | apn / lpt |
| 实验室 + outdoor/野外实测 | B9 锚（42m 6h）/ photonics（室内+室外）|
| 综述（不适用） | survey |

**归纳**：B8/B9 联读 9 篇实现复杂度梯度完整覆盖定稿 §5 四档。**B8 锚纯仿真（最低门槛）+ B9 锚 outdoor 实测（最高档之一）形成对照**——同是"绕开载波同步"切法，实现复杂度可从纯仿真（B8）到 outdoor 6h 长期实测（B9）。**cited-by 池无人 follow 锚点的实现路径**（无人做"自消除 outdoor 实测"或"虚拟载波纯仿真扩展"）。

### 4.6 与 B1-B5 对比：自相干切法 vs 传统载波同步切法的差异
| 维度 | B1-B5（传统载波同步切法） | B8/B9（自相干"绕开"切法） |
|---|---|---|
| **大点性质** | 改进 CFO/CPR/OPLL/TED 算法（载波恢复需求存在）| 消除载波恢复需求（载波同步被绕过）|
| **cited-by follow 度** | 高（Spalvieri 85 池 / Paillier 43 池团队自切密集，场景迁移+硬件实现过半）| **零**（B8 5 池 / B9 8 池 0/7 follow"绕开"本身）|
| **Q# 产出** | 有（B1-Q1 自适应 N / B3-Q2 +2-3dB / B4 双环 / B5 短时谱 CFO / B6 OPLL / B7 Gardner TED）| **B8 无核心 Q#（自消除使需求冗余，事实）/ B9 有 Q1-Q3 但 DRE 与载波同步正交** |
| **dB 形态** | 主流两口径（dBm 灵敏度 vs SNR penalty dB，定稿 §3.3 警示 1）| **5+ 口径碎片化**（BER 量级 / SNR 增益 / mixing gain / shaping gain / ROP sensitivity dBm / survey 转述混杂）|
| **D005 够格难度** | 架构替换/工具借用/联合建模有 dB（jphot +2-3dB / L053 +2-3dB 是样本）| **B8 无 dB / B9 ~3dB SNR 但 vs 内部对照非传统相干 baseline**——D005 够格更难（需补传统相干对照）|
| **动机叙事** | "X 已被研究但 Y 未覆盖"绝对主流（~35%）| **"绕开而非赢"主导**（B8/B9 锚都用，定稿 §4 第四类 ~10% 少数派）|
| **赛道定位** | 在"载波同步算法改进"赛道内拥挤（Paillier 安全区场景迁移+硬件实现过半）| **在"用架构替代载波同步"赛道，独占孤点**（无 cited-by 接力）|

**核心差异**：传统载波同步切法（B1-B5）是**被引用也被接力切**的活跃大点（团队自切密集、cited-by follow 大点子环节）；自相干"绕开"切法（B8/B9）是**被引用但不被接力切**的孤点大点（cited-by 都切相邻维度，无人 follow"绕开"本身）。**这一差异使 B8/B9 在载波同步专题中不直接产出"载波同步改进"型 Q#**（B8 主判定无核心 Q# 是事实），但提供"载波同步在哪些场景被自相干架构替代"的反向参照。

---

## 5. 自评

### 5.1 6 维缺失率
- **维度 1（大点锚）**：缺失率低——9 篇都能定锚（B8/B9 自生大点 + cited-by 各自大点清晰）。
- **维度 2（切的角度）**：缺失率低——9 篇都能定角度（optlastec 信息不足除外）。
- **维度 3（dB 形态）**：**缺失率最高 + 口径最碎**——optlastec 付费墙（1/9 信息不足）；落盘 8 篇 dB 口径 5+ 种（BER 量级 / SNR 增益 / mixing gain / shaping gain / ROP sensitivity dBm / survey 转述），**横向比几乎不可直接做**。与 B4/B5 池（abstract 级 30-40% 无 dB）不同——B8/B9 池不是"无 dB"而是"dB 口径碎片化"。
- **维度 4（横向多样性）**：缺失率低——9 篇都能定横向位置。
- **维度 5（动机叙事）**：缺失率低——8 篇落盘都能定叙事（optlastec 信息不足）。
- **维度 6（实现复杂度）**：缺失率中等——optlastec + jocn.503484（abstract）2/9 信息不足；落盘 7 篇能定档。

### 5.2 自相干"绕开"切法对"我也想水一篇"的启示（中性观察非推荐）
- **启示 1（孤点风险）**：B8/B9"绕开载波同步"是**被引用但不被接力切**的孤点大点——若想"水一篇"切这条路线，**cited-by 池里没有可接力的密集参考**（不像 Paillier 安全区场景迁移+硬件实现过半有模板）。独占空间大但参考少。
- **启示 2（dB 口径碎片化风险）**：自相干联读 dB 口径 5+ 种，**D005"赢 baseline 几 dB"标尺下横向比极难**——若想做出 D005 够格梯度（赢传统 baseline 几 dB），自相干赛道比传统载波同步赛道更难锚定统一 dB（B8 无 dB / B9 ~3dB 但 vs 内部对照）。
- **启示 3（叙事套路少数派）**：B8/B9"绕开而非赢"叙事在 B1-B5 池里是 ~10% 少数派——若用此叙事，**intro 立得住但不是主流**（主流是"X 已被研究但 Y 未覆盖"~35%）。
- **启示 4（实现复杂度可调档）**：B8（纯仿真最低门槛）+ B9（outdoor 6h 最高档）同是"绕开"切法——**"绕开"切法的实现复杂度可从纯仿真到 outdoor 实测全档覆盖**，给"水一篇"的档位选择空间大（不像 B4/B5 必须 FPGA demo）。
- **启示 5（B8 主判定"无核心 Q#"是事实非缺陷）**：B8 自消除使载波同步需求冗余，**不强行凑 Q#**（纪律 6）——若切 B8 路线，需接受"不产出载波同步改进型 Q#"，产出的是"载波同步在 PAM4 一维调制场景被替代"的反向参照。

### 5.3 守纪律自检
- **只提取不判断**：§4 横向多样性结论"独占孤点"是中性分布描述非 Go/Kill（不判"该不该切"）。
- **不脑补**：optlastec 付费墙 + jocn.503484 abstract 标"信息不足"，未强行定档（FR-26）。
- **切法 ≠ 方法配方**：未抄 B8 square-law 推导 / B9 DRE Viterbi 算法细节，只标切法角度。
- **团队维度只标作者名**：B8 锚 Liu 团队（重庆邮电）/ B9 锚 Patel-Guiomar 团队（Aveiro+IT）/ survey 同 IT Aveiro 机构 / jocn.503484 同 B8 锚 Liu 团队——**只标作者名+机构，不推断师承**。
- **dB 口径警示**：§4.2 表格逐篇标口径（BER 量级 / SNR 增益 / mixing gain / shaping gain / ROP sensitivity dBm / survey 转述），与定稿 §3.3 警示 1 一致（dBm 灵敏度 vs SNR penalty dB 不可混），且发现 B8/B9 口径碎片化比 B1-B5 更严重（5+ vs 2 口径）。
- **B8 主判定"无核心 Q#"如实标**：§1 特征标注 + §5 启示 5 均如实标，不强行凑 Q#（纪律 6）。
