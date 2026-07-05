# 切法元数据：B4/B5 Paillier 43 大池

> 提取人：子 agent | 日期：2026-07-05 | 范围：B4 双反馈环 + B5 短时谱粗频偏 + Paillier 43 池筛 12 篇
> 纪律：D018 中性提取（不判 Go/Kill）/ FR-26 证据链（abstract 看不出标"信息不足"）/ 只标作者名不推断师承 / 切法 ≠ 方法配方

## 1. Paillier 大点本身（为什么被反复切）

**论文**：Paillier, Conan, Le Bidan, Artaud, Védrenne, Jaouën. "Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop." IEEE JLT 2020. DOI 10.1109/jlt.2020.3003561（arXiv 1911.11851）。ONERA + CNES + IMT Atlantique + Télécom Paris 联合 PhD 工作。

**核心贡献（按 JLT 笔记 + B4 笔记）**：
1. **端到端建模框架**：Hufnagel-Valley Cn² 剖面 + Bufton 风剖面 + Zernike AO（up to mode 91）数值相位传播生成真实湍流时间序列（2s）+ intradyne BPSK 10 GBaud 数字相干接收机。
2. **分治架构（不是双反馈环，是单环 DPLL + 光/电辅助）**：AO（光域湍流振幅+波前）‖ AGC（电域残余振幅，匹配 Kd=1）‖ DPLL（数字域多普勒残频 100 MHz + 残余相位）。三模块串行级联，环路内不联合建模。
3. **关键发现："湍流相位对载波同步可忽略"（条件性）**——残余 piston mode ~1ms 相干时间远慢于 10 GBaud 符号率，DPLL 能顺带 track，不需专门湍流相位补偿模块。**条件性**：依赖 BPSK 单一调制 + 高符号率 + 理想 timing + AGC 恒幅 + AO 校正后。
4. **量化基线**：湍流致 2.3 dB BER penalty（BER=1e-4 vs AWGN）；幅度起伏致 5 dB SNR 退化（临界 SNR -9→-4 dB）；AO flux penalty -4.5 dB；100 MHz 残频 pull-in ms 量级。

**为什么被 43 篇反复切**（中性观察）：
- **它是一个"完整可引用的星地相干下行 ground receiver 参考架构"**——同时给出系统模型 + 信道模型 + 同步方法 + 量化基线，被引者几乎都能从中找到一个可锚的子点。
- **被切的子点高度多样**：从 AO 补偿 / DPLL 设计 / 湍流建模方法 / 星地链路场景 / 相干 vs IM/DD 比较 / 接收机硬件 / 仿真框架，几乎每个模块都被独立切过。
- **"分治够用"的条件性留了缝**——后续工作可在"假设不成立的条件"（高阶调制 / 强湍流 / 低 SNR / 上行链路）上切，但 43 池中真正切这条缝的不多（多数是"借框架 + 换场景/换方法"）。

---

## 2. B4 切入点的切法动作（双反馈环 OPLL）

**B4 本体**：optcom.2023.129312（Na Liu, Cheng Ju 等，"Carrier recovery for satellite-to-ground coherent laser communication systems using double feedback loop and Viterbi–Viterbi feedforward cascade structure"）。

- 团队：Na Liu / Cheng Ju / Dongdong Wang / Xuefeng Zhang / Changhong Li（BUPT 团队，与 B5 本体、L016/L017/L038 同团队，**只标作者名不推断师承**）。
1. **大点锚（Paillier 哪个点）**：Paillier 单环二阶 DPLL（BPSK MAP 相位检测器 + loop filter + NCO + AGC 恒幅）。B4 把 Paillier 当**单环 baseline**，本体做"双环 vs 单环"对比——外环 PADE 角度差分鉴频跟大动态 Doppler + 内环 V–V RFO 精跟残余频偏 + 前馈 V–V 相位级联。
2. **切的角度**：**架构替换**（单环 → 双反馈环粗细分工）+ **硬件实现**（FPGA Arria 10 资源共享，V–V 相位与第二级 RFO 共享逻辑）。
3. **dB 形态**：**绝对指标 + 内部对照**——归一化 MSE 2.0×10⁻⁶→5.1×10⁻⁷（残频 σ 3.5→1.75 MHz）；动态跟踪 285 GHz/s；最大跟踪范围 ±920 MHz @ 0.5 dB 灵敏度代价；FPGA 9.1K+1.4K ALE；12-bit 定点 0 dB 代价。**无与外部具名 baseline 的 BER/OSNR dB 级增量**（仅自报绝对值 + 定性对比"前馈类"）。
4. **横向多样性**：在 43 池里属**架构替换主流**（与 L008 自身 + L036 ODPLL 同路线），但"双反馈环 + V–V 前馈级联 + FPGA 资源共享"组合在池中较独占（多数 cited-by 不做双环）。
5. **动机叙事**：前馈 FOE 跟踪范围窄（1/8 baud 上限）+ 单环难兼顾"大动态跟 Doppler + 小动态精跟相位噪声"两尺度 → 双环解。**典型"X 已有但 Y 不足"套路**。
6. **实现复杂度**：FPGA 实时实现（Arria 10，12-bit 定点），实验室硬件级（非现场实测，无湍流建模）。

---

## 3. B5 切入点的切法动作（短时谱粗频偏）

**B5 本体**：optcom.2024.130981（Jiamin Fan, Cheng Ju, Na Liu 等，"Coarse frequency offset estimation and compensation based on short-time spectrum analysis in FSO communication system"）。

- 团队：Jiamin Fan / Cheng Ju / Na Liu / Qingsong Luo 等（BUPT 同团队，与 B4 同作者群，**只标作者名**）。
1. **大点锚（Paillier 哪个点）**：Paillier 把 Doppler 总频偏（~9 GHz）"主要部分由 coarse frequency estimator 预补偿，DPLL 只 track 残频（仿真用 100 MHz constant offset）"——B5 切的就是 Paillier 框架里**那个被推给但未细化的"coarse frequency estimator"子环节**。即 B5 切的是 Paillier 的"粗频偏预补偿"模块，而非 DPLL 本体。
2. **切的角度**：**架构替换**（粗 CFO 子环节用"分块 FFT + 正负功率谱面积比 + 星历预测"替代传统 Mth-power 时域相位增量 [60] Leven）+ **场景迁移**（谱分析 CFO 原仅光纤，B5 首次搬到星地 LEO Doppler ±4.5 GHz）。
3. **dB 形态**：**无 dB 增益对比（绝对指标维度）**——捕获范围 ±4.5 GHz / 粗补偿后残频标准差 <140 MHz（最大 250 MHz）/ 精确补偿后残频 <5 MHz / BER 1e-3 接收灵敏度 -48 dBm。**只给绝对指标未 vs 某 baseline 给"改善 X dB"**。范围维度 ±4.5 GHz 覆盖 LEO Doppler 全量程是结构性优势。
4. **横向多样性**：在 43 池里属**场景迁移独占**——切"短时谱/功率比 CFO"的只有 B5 自身，池中没有同类；与 L032（粗到细谱监测，IoT 非星地）/ L034（Gardner TED 估 Doppler）属不同机制。
5. **动机叙事**：M-power FPGA 资源消耗大且适用 M-PSK / 训练序列有数据开销 / 改进传统估计范围有限 → 谱分析类不依赖 MIMO 等 DSP、低复杂度、无 pilot，**首次搬星地 LEO Doppler**。**典型"X 类有 Y 限制，本类首次搬 Z 场景"套路**。
6. **实现复杂度**：实时实验（2.5-GBaud PM-QPSK，Intel Arria 10 FPGA，5 GSa/s ADC 8bit，1024 组 16 点 FFT 均值滤波），实验室 B2B 硬件 demo（非现场实测，无湍流信道仿真）。

---

## 4. Paillier 43 池切法角度分布速览

> 说明：43 篇按 abstract 能看出的"切的角度"主分类（一篇可能多类，按主导角度归一类）。abstract 缺失（L008/L027/L022/L030 无 abstract）按标题 + 团队已知笔记归类。统计中性观察非穷尽。

| 切的角度 | 篇数 | 代表 ID/DOI |
|---|---|---|
| **场景迁移**（搬 Paillier 星地框架到新场景：UAV/HAP/ISL/feeder/underwater/mid-IR/语义通信） | 11 | L002 HAP relay / L004 satellite cluster / L007 mid-IR 3.6µm / L011 underwater electric field / L014 RIS-SLIPT UAV / L018 HAGS all-optical LEO / L028 satellite OBS switching / L033 semantic vector beams / L042 DVB-S2 feeder / L009 space MDI-QKD / L025 RF photonic |
| **硬件实现 / 接收机器件**（μICR 空间鉴定 / 光 pin beam / 多孔径 combining / photonic lantern / silicon photonic / compound eye） | 10 | L003 silicon photonic adaptive / L012 optical pin beam / L016/L017 multi-aperture MIMO combining / L029 photonic lantern / L030 compound eye / L038 TIR equalizer FPGA / L040 multimode combiner / L041 μICR space qualification / L035 inverse design demux |
| **AO / 波前校正工具**（借 Paillier AO 框架做新 AO 算法） | 5 | L006 AO+OAM MPDA / L022 AO Technology 综述 / L031 phase contrast Gerchberg-Saxton AO / L039 feeder link AO+digital / L043 Paillier 自己 ICSOS 2019 会议版 |
| **架构替换 / 同步算法本体**（DPLL→OPLL/双环/ODPLL/Z 域模型/phasemeter） | 6 | L008 双反馈环 V–V（B4 本体）/ L019 third-order OPLL chaos / L020 dual-quadrature phasemeter / L021 Z 域 OPLL 模型 / L027 短时谱 CFO（B5 本体）/ L036 ODPLL Z-transform / L037 dual-quadrature phasemeter conf |
| **联合建模 / 系统级建模**（information-theoretic coherent vs IM/DD / 仿真框架 / DSP 评估） | 4 | L001 coherent FSO 综述+实验 / L010 IT coherent vs IM/DD / L015 self-coherent DRE / L023 10 Gbps coherent receiver DSP / L024 RL geometric shaping / L026 fibers-to-satellites 综述 |
| **参数调度 / 自适应**（symbol-rate / rate adaptation / launch power 自适应） | 4 | L005 PCS+symbol-rate（jlt.2023.3281082）/ L002 rate adaptation relay / L013 attention NN launch power+rate / L014 adaptive rate QoS |
| **性能极限 / 理论分析**（chaos / IT bound / CRB） | 2 | L019 OPLL chaos bifurcation / L010 IT outage capacity |
| **工具借用**（神经网络 / RL / semantic / attention 借到 FSO） | 3 | L013 attention NN / L024 RL geometric shaping / L032 coarse-to-fine NN spectrum / L033 semantic PVQAE |
| **综述延伸**（Paillier 当综述引用点之一） | 3 | L001 / L022 / L026 |
| **信息不足（abstract 空无法归类）** | 4 | L008 / L022 / L027 / L030 |

**横向分布观察**（中性）：场景迁移（11）+ 硬件实现（10）= 池子过半，**这两类是 Paillier 池的"安全区"**（被反复切的拥挤区）。架构替换/同步算法本体（6）相对中等密度。真正切 Paillier "分治够用条件性"这条缝的（即换 Paillier 假设不成立的条件做改进）**几乎为零**——多数 cited-by 是"借框架 + 换场景/换硬件"，不是"挑战 Paillier 的条件性结论"。

---

## 5. 筛出的切法多样子集（12 篇）逐篇 6 维

> 筛选原则：覆盖 6+ 类角度（场景迁移 / 硬件实现 / 架构替换 / 工具借用 / 参数调度 / 性能极限 / 综述延伸 / 联合建模），每类 1-3 篇代表，不重复同团队同类。

### 5.1 L005 — Digitally Mitigating Doppler Shift in High-Capacity Coherent FSO LEO-to-Earth Links（jlt.2023.3281082）
- 团队：Marco A. Fernandes / Pedro A. Loureiro / Gil M. Fernandes / Paulo P. Monteiro / Fernando P. Guiomar（Portugal 团队，与 L001/L015 同组）。
1. **大点锚**：Paillier 的"全数字 CFO 估计 + DPLL 跟残频"框架；引 [30] Pita two-stage freq + [31] OPLL 作为"数字方案不够 / 光学方案贵"对照。
2. **切的角度**：**参数调度**（PCS + 符号率自适应绕开非对称电滤波，非做新 CFO 算法）。
3. **dB 形态**：吞吐维度 dB 等价——自适应符号率 vs 固定 80 Gbaud，极端 ±15 GHz Doppler 下 ABR 维持 ~600 Gbps（**+70~100 Gbps 增量**）。**增益维度错位（吞吐 vs 同步 dB）**。
4. **横向多样性**：参数调度类代表，池中该角度 4 篇之一，中等密度。
5. **动机叙事**：纯数字 CFO 未处理 Doppler+电滤波非对称响应 / OPLL 贵 → 用 PCS+符号率自适应绕开。**"绕开而非赢"套路**。
6. **实现复杂度**：实验室硬件 demo（600 Gbps PCS-64QAM，Doppler ±15 GHz 扫描，Gamma-Gamma 湍流仿真）。

### 5.2 L008 — Carrier recovery using double feedback loop and Viterbi–Viterbi feedforward cascade（optcom.2023.129312，B4 本体）
- 团队：Na Liu / Cheng Ju / Dongdong Wang / Xuefeng Zhang / Changhong Li（BUPT）。
1. **大点锚**：Paillier 单环 DPLL 作为单环 baseline；B4 做双环对比。
2. **切的角度**：**架构替换**（单环 → 双反馈环）+ **硬件实现**（FPGA 资源共享）。
3. **dB 形态**：绝对指标 + 内部对照（MSE 4× 改善 / ±920 MHz @ 0.5 dB / 285 GHz/s）；**无外部 baseline dB 增量**。
4. **横向多样性**：架构替换主流（与 L036 ODPLL 同路线），双环+V–V 级联组合较独占。
5. **动机叙事**：前馈 FOE 范围窄 + 单环难兼顾两尺度 → 双环解。
6. **实现复杂度**：FPGA 实时（Arria 10，12-bit 定点），无湍流建模。

### 5.3 L027 — Coarse CFO based on short-time spectrum analysis in FSO（optcom.2024.130981，B5 本体）
- 团队：Jiamin Fan / Cheng Ju / Na Liu 等（BUPT，与 B4 同组）。
1. **大点锚**：Paillier 框架里"coarse frequency estimator 预补偿"那个被推给未细化的子环节。
2. **切的角度**：**架构替换**（粗 CFO 子环节用分块 FFT + 正负功率谱面积比）+ **场景迁移**（谱分析 CFO 从光纤搬到星地 LEO）。
3. **dB 形态**：**无 dB 增益对比**（绝对指标 ±4.5 GHz 范围 / 残频 <140 MHz / 灵敏度 -48 dBm）。
4. **横向多样性**：场景迁移独占（短时谱/功率比 CFO 池中仅此一篇）。
5. **动机叙事**：M-power 资源大且限 M-PSK / 训练序列有开销 → 谱分析首次搬星地 LEO。
6. **实现复杂度**：实时 FPGA demo（Arria 10，B2B 无湍流信道）。

### 5.4 L036 — Z-Transform Model of a Coherent Receiver Under High Doppler Rates（ICSOS 2025）
- 团队：Sophonie Pech / F. Destic / Arnaud Dion / A. Rissons（法国 ISAE/ONERA 圈，**Paillier 同圈作者，只标名**）。
1. **大点锚**：Paillier DPLL 的 Z 域建模（Paillier 用模拟 PLL 经验式迁移 pull-in 公式，L036 改用 Z 变换建 hybrid ODPLL 模型）。
2. **切的角度**：**架构替换**（DPLL → hybrid ODPLL，光域模拟处理 + 数字域频率跟踪控制）+ **工具借用**（Z 变换建模方法论）。
3. **dB 形态**：**信息不足**——abstract 只说"achieves successful QPSK demodulation under strong Doppler rates + realistic received power"，无 dB 数字。
4. **横向多样性**：架构替换 + 工具借用组合，与 L021（Z 域 homodyne OPLL）同类，池中中等密度。
5. **动机叙事**：LEO Doppler 漂移致相干解调难 + 系统延迟需考虑 → Z 域建模 ODPLL + FPGA 实现。**典型"补 Paillier 没细化的建模维度"**。
6. **实现复杂度**：仿真 behavioral model（标未来 FPGA + photonic 集成），尚非硬件 demo。

### 5.5 L001 — Coherent FSO Communications: Opportunities and Challenges（JLT 2022 综述+实验）
- 团队：Fernando P. Guiomar / Marco A. Fernandes / José L. Nascimento / Vera Rodrigues / Paulo P. Monteiro（Portugal，与 L005/L015 同组）。
1. **大点锚**：Paillier 作为星地相干下行 ground receiver 代表性引用点之一（综述级锚）。
2. **切的角度**：**综述延伸** + **联合建模**（in-depth 实验分析湍流+pointing 对超高速 FSO 影响）。
3. **dB 形态**：绝对指标——48 小时 outdoor demo 800+ Gbps over ~42 m；无 vs baseline dB 增量（综述+demo 性质）。
4. **横向多样性**：综述延伸类，池中 3 篇之一，与 L026/L022 同类。
5. **动机叙事**：光纤→无线融合 + 湍流/pointing 是关键挑战 → 48h outdoor demo 量化。**综述"摆全景+给基线"套路**。
6. **实现复杂度**：outdoor 现场实测（42 m 链路，48 小时），池中实现复杂度最高档之一。

### 5.6 L010 — IT Comparison Between Coherent and IM/DD for FSO（JSAC 2024）
- 团队：Ayman Zahr / Giulio Colavolpe / Tommaso Foggi / Balázs Matuz / Armando Vannucci（Mitsubishi Electric RCE / 意大利 Prisma 圈）。
1. **大点锚**：Paillier 作为"相干检测星地可行"的代表引用，作 coherent 侧 baseline 之一。
2. **切的角度**：**性能极限**（information-theoretic：mutual information + outage capacity + shaping gain 量化 coherent 相对 IM/DD 的 SNR gain）。
3. **dB 形态**：**vs 内部对照**（coherent vs IM/DD 的 SNR gain 量化，techno-economical 比较），具体 dB 数 abstract 未给。
4. **横向多样性**：性能极限类，池中独占（IT 视角分析 coherent vs IM/DD 仅此一篇）。
5. **动机叙事**：相干贵但 gain 未量化 → IT 视角给 SNR gain 上界 + shaping gain 分析。
6. **实现复杂度**：纯理论/仿真（无 hardware demo）。

### 5.7 L013 — Self-Adaptive All-Optical Feedback FSO With Attention-Enhanced Turbulence Awareness（JLT 2025）
- 团队：Ruizhe Jin / Jiazheng Ding / Mingfeng Xu 等（中科院光电所 Luo课题组）。
1. **大点锚**：Paillier 的"AO + 自适应接收"框架；切"自适应 launch power + 通信率"调度子环节。
2. **切的角度**：**工具借用**（attention NN 融合光场强度+相位特征检测湍流强度）+ **参数调度**（自适应 launch power + rate）+ **架构替换**（all-optical feedback link 简化 receiver）。
3. **dB 形态**：**vs 内部对照**——平均有效率提升 58.4% / 平均可靠性 gain 最高 34.2% / 6h 三波长 135 Gbps；最强 vs 最弱湍流慢衰落差 11 dB。**多维度 gain（率+可靠性+衰落差）非单一同步 dB**。
4. **横向多样性**：工具借用 + 参数调度组合，池中该组合较独占（attention NN + 全光反馈）。
5. **动机叙事**：湍流+pointing 致可靠性波动 → attention NN 检测湍流 + 自适应调整 power/rate。**"借 ML 工具做自适应"套路**。
6. **实现复杂度**：实验室 10 m FSO 链路 hardware demo（非现场实测，7 级湍流 time-varying）。

### 5.8 L024 — RL Aided Geometric Shaping and Self-Canceling Coherent Detection for PAM4 FSO（JOCN 2022）
- 团队：Yejun Liu / Kun Chen / Song Song 等（中国地质大学）。
1. **大点锚**：Paillier coherent detection 框架；切"coherent detection 结构简化 + 几何整形"子环节。
2. **切的角度**：**工具借用**（RL 求最优 PAM4 幅度集）+ **架构替换**（self-canceling coherent detection 中频信号过平方律器件消相位噪声+频偏）。
3. **dB 形态**：**vs 内部对照**——coherent vs direct detection BER 提升最高 1 个数量级；几何整形在弱到强湍流下 BER 提升 2 个数量级。**BER 量级维度非 dB**。
4. **横向多样性**：工具借用（RL+几何整形）类，池中独占（PAM4 + RL geometric shaping 仅此一篇）。
5. **动机叙事**：PAM4 FSO 抗湍流 + 性能 vs 复杂度 trade-off → RL 几何整形 + 简化相干检测。
6. **实现复杂度**：理论分析 + 仿真（abstract 未提 hardware demo）。

### 5.9 L003 — Self-adaptive integrated photonic receiver for turbulence compensation（Sci Reports 2024）
- 团队：A. Martinez / G. Cavicchioli / S. SeyediNavadeh / F. Zanetto / A. Melloni 等（米兰理工 silicon photonics 组）。
1. **大点锚**：Paillier 的"AO + multi-aperture 相干接收"思路；切 receiver 前端 silicon photonic 集成化。
2. **切的角度**：**硬件实现**（silicon photonic chip 2D optical antenna array + MZI mesh programmable optical processor 实时补偿 scintillation）。
3. **dB 形态**：**信息不足**——abstract 只说"effectiveness demonstrated with 10 Gbit/s indoor FSO under turbulence stronger than outdoor"，无 dB 数字。
4. **横向多样性**：硬件实现类主流（池中 10 篇之一），但 silicon photonic MZI mesh 集成方案在池中独占。
5. **动机叙事**：多孔径相干合成抗湍流 + 集成化降功耗/成本 → silicon photonic 自适应 receiver。
6. **实现复杂度**：实验室 indoor FSO hardware demo（10 Gbit/s，湍流强于 outdoor 数百米级）。

### 5.10 L041 — Qualifying an integrated coherent receiver for space applications（LASE 2022）
- 团队：Christopher Foy / J. Minch / Derrick Feld 等（MIT Lincoln / Draper 圈）。
1. **大点锚**：Paillier 的"星地相干接收机 ground receiver"框架；切"商用 μICR 空间鉴定"工程化子环节。
2. **切的角度**：**硬件实现**（μICR 商用器件空间鉴定：辐照 100 krad / 热循环 -40~70°C / 振动 28 GRMS / 冲击 1201g / 热真空）。
3. **dB 形态**：**无 dB（结构性指标）**——环境测试后 EO 性能无退化（pass/fail 维度），非 dB gain。
4. **横向多样性**：硬件实现类，池中"空间鉴定"角度独占（其他硬件类做新器件，此篇做鉴定）。
5. **动机叙事**：商用 μICR 低 SWAP 但未空间鉴定 → 环境测试模拟 LEO 轨道条件。
6. **实现复杂度**：实验室环境测试（非通信链路 demo，纯器件鉴定）。

### 5.11 L019 — Phase error oscillations in third-order OPLL and slave OPLL（Opt Eng 2022）
- 团队：Manaj Dandapathak / Saumen Chakraborty（印度）。
1. **大点锚**：Paillier DPLL/OPLL 框架；切"高阶 OPLL 非线性动力学"理论子环节。
2. **切的角度**：**性能极限**（三阶 OPLL resonant loop filter 的稳定区 + period doubling bifurcation 致混沌相位误差 + master-slave OPLL 跟踪）。
3. **dB 形态**：**信息不足**——abstract 只说"stable synchronous zone estimated analytically + chaotic oscillation via period doubling"，无 dB 数字。
4. **横向多样性**：性能极限/理论分析类，池中独占（OPLL 混沌动力学仅此一篇）。
5. **动机叙事**：OPLL 稳定区外动力学未明 → 解析+数值估稳定区 + master-slave 跟踪混沌。
6. **实现复杂度**：纯理论/数值仿真（无 hardware demo）。

### 5.12 L039 — Experimental assessment of optical communication chains for high-capacity optical feeder links（ICSOS 2023，VERTIGO 项目）
- 团队：A. Maho / S. Lévêque / A. Le Kernec 等 + **L. Paillier** / N. Védrenne / D. Matter / M. Sotom（法国 ONERA/CNES/Thales 圈，**Paillier 自引**）。
1. **大点锚**：Paillier 自己的星地相干下行框架延伸到 feeder link；**Paillier 是共同作者（自引延伸）**。
2. **切的角度**：**场景迁移**（星地→feeder link / VHTS gateway）+ **联合建模**（atmospheric channel emulator + 25 Gbps OOK/DPSK + RF analog 实验评估）。
3. **dB 形态**：**vs 传统 baseline**——25 Gbps DPSK 达 state-of-the-art sensitivity；BER 曲线 + detection sensitivity + power penalty；具体 dB abstract 未全给。
4. **横向多样性**：场景迁移+联合建模组合，池中 feeder link 角度独占。
5. **动机叙事**：VHTS feeder link 需求 + 湍流缓解 → VERTIGO 项目 rack 单元 lab+outdoor 评估。
6. **实现复杂度**：实验室 + outdoor trial（Jungfraujoch-Zimmerwald 瑞士野外链路），实现复杂度最高档。

---

## 6. Paillier 大点切法模式小结（中性，不判 Go/Kill）

- **大点内部被切的子点分布**：43 篇集中在 **Paillier 的"系统级参考架构"地位**（被当星地相干下行 ground receiver 标准引用），其次是 **AO/波前校正模块**（5 篇直接切 AO 算法）、**接收机硬件**（10 篇切器件）、**DPLL/OPLL 同步本体**（6 篇切架构）。**真正切 Paillier "分治够用条件性"这条缝的几乎为零**——多数 cited-by 是"借框架 + 换场景/换硬件/换工具"，不是"挑战 Paillier 的条件性结论"（即换 BPSK/10 GBaud/理想 timing/AGC 恒幅/AO 校正后这些假设不成立的条件做改进）。**这条缝在 cited-by 池里是空白**（中性观察）。

- **dB 形态分布**（12 篇子集 + 43 池印象）：
  - **vs 传统 baseline**：L039（state-of-the-art sensitivity）/ L010（coherent vs IM/DD SNR gain）≈ 2/12
  - **vs 内部对照**：L005（+70~100 Gbps）/ L013（58.4% / 34.2%）/ L024（BER 1-2 量级）/ L001（800 Gbps demo）≈ 4/12
  - **绝对指标无 dB 增益**：L008（MSE/范围/资源）/ L027（±4.5 GHz / 残频）/ L041（pass/fail）≈ 3/12
  - **无 dB 仅结构性**：L003 / L041 ≈ 2/12
  - **信息不足（abstract 无 dB）**：L036 / L019 ≈ 2/12
  - **结论**：abstract 级 dB 形态分布偏散，**"绝对指标无外部 dB 增量"占比偏高**（与 B4/B5 自身一致——这俩本体也都无外部 baseline dB 增量）。

- **横向多样性（角度集中度）**：
  - **拥挤区（安全区，被反复切）**：场景迁移（11）+ 硬件实现（10）= 池子过半。
  - **中等密度**：架构替换/同步算法本体（6）/ AO 工具（5）/ 参数调度（4）。
  - **独占区（池中少有人切）**：性能极限/IT（L010/L019）/ 工具借用 NN（L013/L024/L033）/ 短时谱 CFO（L027）/ ODPLL Z 域（L036）/ 空间鉴定（L041）。
  - **中性观察**：独占区角度被切得少 ≠ 推荐，只标"别人没切过的角度集中在这里"。

- **动机叙事常见套路**（abstract 级归纳）：
  - **"X 已被研究但 Y 未覆盖"**（最常见，~40%）：L005/L008/L027/L013/L024 等。"Paillier 已证 OPLL/DPLL 在 X 场景可行，本工作扩展到 Y"或"传统 X 类有 Y 限制，本类首次 Z"。
  - **"绕开而非赢"**（~15%）：L005 PCS+符号率自适应绕开非对称滤波；L024 self-canceling 绕开相位噪声。**切的是"不动 Paillier 同步本体，换一个维度绕"**。
  - **"借 ML/NN 工具"**（~15%）：L013 attention / L024 RL / L032 coarse-to-fine NN / L033 semantic。**借工具到 FSO 的迁移叙事**。
  - **"摆全景 + 给基线"**（综述/demo，~10%）：L001/L026/L022。
  - **"补 Paillier 没细化的建模维度"**（~10%）：L036 Z 域 ODPLL / L019 OPLL 混沌 / L021 Z 域 homodyne。

- **实现复杂度梯度**（12 篇子集）：
  - **纯理论/仿真**：L010 / L019 / L024 ≈ 3/12
  - **仿真 behavioral model（标未来 hardware）**：L036 ≈ 1/12
  - **实验室 hardware demo（FPGA / indoor FSO / 器件鉴定）**：L008 / L027 / L003 / L013 / L041 ≈ 5/12
  - **实验室 + outdoor/野外实测**：L001（42 m 48h）/ L039（Jungfraujoch-Zimmerwald）≈ 2/12
  - **吞吐 demo（非同步硬件）**：L005 ≈ 1/12
  - **结论**：abstract 级实现复杂度梯度信息密度尚可（~75% 能判档），但具体参数（FPGA 型号 / 链路长度 / 湍流强度）缺失率高。

- **"安全区"信号**（中性观察非推荐）：
  - **场景迁移 + 硬件实现** = Paillier 池的"安全区"（被反复切的拥挤区）。新人若想"水一篇"，这两类是别人切过的密集区，**但也是 dB 增量最难做出来的区**（多数 cited-by 在这两类只给绝对指标或 demo 性能，无 vs baseline dB）。
  - **架构替换 + 工具借用** = 中等密度，**有空间做"赢 baseline 几 dB"的 dB 增量**（B4/B5/L013/L024 都在这类）。
  - **性能极限 + Paillier 条件性缝** = 独占区，**被切得最少**，但 abstract 信息密度最低（最难从 cited-by abstract 看出 dB）。

---

## 7. 自评

- **6 维里哪几维信息缺失率高**：
  - **维度 3（dB 形态）缺失率最高**——abstract 级 dB 数字分布参差，12 篇子集里 2 篇完全无 dB（L036/L019），3 篇仅绝对指标无 vs baseline（L008/L027/L041）。**43 池整体估计 30-40% abstract 无可用 dB 数字**。
  - **维度 6（实现复杂度）次高**——abstract 普遍只说"experimental/simulated"，具体 FPGA 型号 / 链路长度 / 湍流强度常缺，需落盘全文才能精确分档。
  - **维度 1（大点锚）缺失率中等**——abstract 不明说引 Paillier 哪个点，需结合标题 + 团队已知笔记推断（如 L008/L027 靠 B4/B5 笔记锁定）。
  - **维度 2/4/5（切的角度 / 横向多样性 / 动机叙事）缺失率低**——这三维 abstract 信息密度足够支撑。

- **abstract 级筛是否够支撑切法提取**：
  - **够支撑维度 2/4/5**（切的角度 / 横向多样性 / 动机叙事）——这三维本质是"论文怎么定位自己"，abstract 就是定位声明，足够。
  - **不够支撑维度 3/6**（dB 形态 / 实现复杂度）——这两维需落盘全文的实验章节才能精确。**abstract 级只能给粗档（有无 dB / 仿真 vs 硬件），不能给细档（vs 哪个 baseline / FPGA 型号 / 链路长度）**。
  - **结论**：abstract 级筛**够支撑"切法地图"主线**（切法多样性是核心目标），但 dB 形态/实现复杂度维度建议主线汇总时**降维或标"待全文核验"**，不强填。

- **是否建议主线汇总时降维**：
  - **建议保留 6 维但维度 3/6 标"abstract 级粗档"**——不删，因为 dB 形态/实现复杂度是切法多样性的重要组成（"绕开 vs 赢 baseline"是不同切法）；但标"粗档，细档待全文"。
  - **维度 1（大点锚）建议主线汇总时补 Paillier JLT 笔记交叉验证**——本批次靠 B4/B5/JLT 三份笔记锁定大点锚，其他 B 点批次若无对应笔记，维度 1 缺失率会更高。
  - **横向多样性（维度 4）的"安全区/独占区"判断建议跨批次汇总后再定**——单批次 43 池的分布可能不代表整个 cited-by 池的全貌。

- **本批次筛选覆盖度自评**：12 篇子集覆盖 7 类角度（场景迁移 / 硬件实现 / 架构替换 / 工具借用 / 参数调度 / 性能极限 / 综述延伸/联合建模），每类 1-3 篇代表，**未选的 31 篇集中在已覆盖类别的同类重复**（如硬件实现类另 5 篇多孔径 combining / 场景迁移类另 7 篇 UAV/HAP/ISL 变体），不影响切法多样性覆盖。
