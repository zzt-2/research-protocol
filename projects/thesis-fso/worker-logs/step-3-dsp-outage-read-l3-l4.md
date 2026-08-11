# Step 3 精读：JLT 2023 与 IEEE Photonics Journal 2020

> 执行：T008 fresh reader B｜日期：2026-08-11｜范围：只报告论文事实与候选问题证据，不作 Q# terminal 判断

## 标题门

| DOI | T008 指定对象 | 全文实际标题 | 结果 | 证据 |
|---|---|---|---|---|
| 10.1109/JLT.2023.3276637 | Liu et al., JLT 2023 | *Multi-Aperture Coherent Digital Combining Based on Complex-Valued MIMO 2N×2 Adaptive Equalizer for FSO Communication* | PASS | JLT `content.md` L5-L9，DOI L23 |
| 10.1109/JPHOT.2020.2977955 | Tu et al., IEEE Photonics Journal 2020 | *Phase Alignment With Minimum Complexity for Equal Gain Combining in Multi-Aperture Free-Space Digital Coherent Optical Communication Receivers* | PASS | JPHOT `content.md` L5-L13、L23-L33 |

## L3 — Liu et al., JLT 2023

### 标准字段（15/15）

1. **DOI**：10.1109/JLT.2023.3276637（L23）。
2. **source path**：`D:/code/study/research-protocol/papers/doi/10.1109_jlt.2023.3276637/content.md`。
3. **read status**：合格全文，fresh-context 全文精读完成；标题门 PASS。
4. **venue**：*Journal of Lightwave Technology*, Vol. 41, No. 18（L1-L5）。
5. **year**：2023；2023-05-16 online，2023-09-19 current version（L13）。
6. **贡献**：论文把 N 个孔径、每孔径双偏振的输入统一送入复值 MIMO 2N×2 自适应 FIR，以一个盲均衡器同时完成幅度缩放、相位旋转、偏振解复用、线性畸变补偿和多孔径数字合并（L43、L49-L51、L79-L85）。CMA（QPSK）/RDE（高阶 QAM）以 SGD 盲更新，无需训练符号，并在 10-Gbps PM-QPSK 的数值仿真与 2/4 孔径离线模拟湍流实验中验证（L85-L97、L119-L123、L219-L221）。
7. **方法概览**：每个孔径形成 H/V 两路复场序列；N 个 2×2 butterfly FIR 共同组成 2N×2→2 结构，输出解复用后的 X/Y 两路。共享 LO 使各支路具有共同 LO 相噪；均衡器前有 I/Q imbalance compensation 与 clock recovery，均衡器后仍需 frequency offset、phase offset compensation 和 QAM de-mapping（L49-L51、L61-L83）。
8. **实验设置**：10 Gbps、2.5 GBaud PM-QPSK；1550.32 nm、20 kHz linewidth、−3 dBm launch；5 GSa/s、8-bit ADC；64 Kbit 重复帧、每通道 1 M samples；25 MHz 共参考钟，MATLAB 离线 DSP（L121-L131）。湍流由 ATT 改变支路 OSNR 模拟 Gamma-Gamma irradiance，Rytov variance 0.5/1，各 100 次独立实验，四支路假定不相关（L175-L201）。
9. **baseline**：实验量化基准为单孔径、无湍流曲线及理论曲线（L201-L207）；引言中的方法邻居包括 MRC、relative-phase-recursive EGC、SC，以及 branch-block phase correction，后者需训练符号且随 skew/fading depth 增大而相位估计变差（L41）。论文没有同条件下与这些多孔径算法的端到端数值横比。
10. **结论**：线宽 0–10 MHz 不影响 CMA 均衡器本身的 MSE 收敛，但较大线宽会恶化后级 carrier phase recovery（L137-L145）。首支路 skew 为 0/400/800 ps 时最终 MSE floor 同为 −8.8 dB、Q² 曲线重合，但收敛分别需 12/20/28 K symbols；超过 5 samples（1000 ps）收敛概率显著下降或不收敛（L147-L167）。2/4 孔径相对单孔径在中湍流提升 1.4/3.2 dB、强湍流提升 2.1/3.6 dB（L201-L207、L219-L221）。
11. **与本专题关系**：直接的 estimator-changing competitor。它不是“先估各支路标量相位再 EGC”，而是以 2N×2 盲 FIR 的联合估计/均衡改变合并器输入到输出的映射；同时其已验证边界揭示它主要覆盖线性、准静态失配，未完成动态 outage/低可靠度下的专门门控。
12. **具体实现**：2 samples/symbol 进入 MIMO、1 sample/symbol 离开；每孔径四个复 FIR（hXX、hXY、hYX、hYY），CMA/RDE error 驱动 SGD，31 taps 用于 skew 仿真（L51、L79-L97、L117、L149-L161）。整数级序列同步由 maximum-cross-correlation pulse search 完成；I/Q 与频偏预补偿、Viterbi–Viterbi 残余相位恢复并非 2N×2 核心本身（L123-L131）。
13. **fit**：高。其 2N×2 butterfly 是 PM 多孔径联合合并的直接近期方法对象；但论文实验是光分路+ATT 模拟独立强度衰落、共享时钟/LO、离线处理，不等价于真实大气动态相位/SOP/outage（L121-L131、L175-L201）。
14. **code**：全文未给代码仓库或补充代码链接；按全文证据记为“无公开代码指针”。
15. **validation**：论文内 validation 包括 numerical simulation + offline hardware experiment；当前阅读验证为全文逐行审计，未做外部搜索/复现。

### 7 个结构段

#### state

N 个孔径各自的 H/V 双偏振离散复序列及其 FIR tap history；论文不是 DRL，不存在 MDP state。严格信号位置是 I/Q imbalance compensation 与 clock recovery 之后、FOC/phase recovery 之前（L49-L51、L117-L131）。

#### action

非 DRL，**N/A**。算法动作等价物为更新 4N 组复 FIR taps，并用这些 taps 对各支路做幅度、相位、SOP/偏振串扰与有限时延的联合线性变换（L51、L79-L97）。

#### reward/objective

非 DRL，reward **N/A**。优化目标为通过 SGD 最小化 constant-modulus cost；QPSK 用 CMA，高阶 QAM 用 RDE，均无需 training symbols（L85-L97）。

#### model assumptions

- 每孔径信道可由 2×2 线性传递矩阵描述，2N×2 FIR memory 足以覆盖所评估的串扰/失真/skew（L53-L83）。
- 各接收机共享 LO；MIMO 后仍单独做 frequency/phase offset compensation（L49-L51）。
- 硬件实验共享 25 MHz reference clock，先做整数序列同步，因而 MIMO skew 试验主要针对剩余的有限采样错位（L123-L131）。
- 湍流实验将 Gamma-Gamma irradiance 映射为 ATT 控制的支路 OSNR；支路假定充分分离而相互独立（L175-L201）。
- 论文声称处理 time-varying gain/phase/SOP 的需求（L9、L41），但公开实验实际扫描的是静态 skew、手动 polarization controller 和逐次 ATT 设定；未给相干时间内动态跟踪速率实验。

#### network/algorithm

非神经网络。N 个 2×2 butterfly FIR 汇成 2N×2→2：输入 `{Hrx,i,Vrx,i}_{i=1}^N`，输出 `X_hat,Y_hat`；CMA/RDE error 逐符号盲更新 taps（L61-L97、L117）。

#### fit

- 适配：PM 双偏振、多孔径、低单支路 OSNR、支路 gain/phase/SOP/skew 联合线性处理。
- 不适配/未证实：真实大气动态相位与动态 SOP、非共同 LO/clock、大于 FIR memory 的 skew、outage 支路的显式拒绝/可靠度门控。
- 候选证据用途：可作为“改变 estimator/combiner 结构”的近期 baseline，而不是相位对齐公式的同类 neighbor。

#### problem extraction（M-C-A + glossary 四判据）

**论文已解决的问题**：传统单偏振 MRC/EGC/SC 或基于训练的 branch-block phase correction（M），在多孔径 PM 相干 FSO、支路存在 gain/phase/SOP/skew（C）时，因方法不含双偏振联合对齐且训练式相位估计随 skew/fading depth 退化（A），难以稳健合并（证据：L41-L43）。

| glossary 判据 | 结果 | 论文内证据 |
|---|---|---|
| 1. M-C-A 具体技术矛盾 | ✅ | L41 明确 M 与失效原因，L43 给目标 C 与替代结构 |
| 2. 有可复用方法产出 | ✅ | 2N×2 butterfly FIR + CMA/RDE 更新架构，L61-L97 |
| 3. 有近期 baseline 可对标 | ⚠️ | 论文列出 MRC/EGC/SC 与 2022 branch-block correction（L41、ref [11] L245），但实验只量化对单孔径/理论曲线，不是完整算法横比（L201-L207） |
| 4. 能量化对标 | ✅（对单孔径基准） | Q²/BER/FEC threshold、MSE、收敛 symbols 与 skew 扫描，L137-L167、L201-L221 |

**候选而非 terminal 的残余问题证据**：2N×2 CMA/RDE（M）在较大 skew 或大线宽/快速相位变化（C）下，因有限 FIR memory/盲更新收敛变慢且 carrier phase tracking 位于后级（A），出现 >5 samples 不收敛或后级 phase recovery 性能下降（L145、L149-L167）。该陈述已有 M-C-A 和量化失效点，但本文未提供一个“解决该残余问题”的近期新方法 baseline 横比，故这里只保留为 Step 3 候选证据。

### 通信参数表

| 链路/模块 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| 调制/速率 | PM-QPSK | 10 Gbps；2.5 GBaud | L9、L121-L123 |
| 光载波 | shared-LO coherent | 1550.32 nm；Tx linewidth 20 kHz；launch −3 dBm | L51、L123 |
| ADC/DSP | offline coherent DSP | 5 GSa/s；8 bit；2 sps→MIMO→1 sps；1 M samples/channel | L51、L123 |
| skew 仿真 | first-branch delay | 0/400/800 ps；31 taps；>1000 ps（5 samples）显著不收敛 | L149-L167 |
| linewidth 仿真 | common linewidth sweep | 0–10 MHz 对 CMA MSE 基本无影响；Q²例示 0/40/100/200 kHz | L137-L145 |
| turbulence | Gamma-Gamma irradiance | Rytov variance 0.5/1；max OSNR fade 11/16 dB；100 independent experiments | L175-L201 |
| receiver/FEC | AWGN receiver characterization | FEC BER 1e−3，对应 Q² 9.8 dB；hardware penalty 0.8 dB | L171-L173 |

### 实验完备性（≤20 行）

1. Claims：blind joint PM combining、skew relaxation、linewidth sensitivity、2/4-aperture turbulence gain；均受 10-Gbps PM-QPSK、shared LO/clock、offline setup 限定。
2. 统计：湍流结果 100 independent experiments；未报告置信区间、error bars、显著性检验或随机 seed（L199-L207）。
3. Baseline：单孔径无湍流+理论曲线；无 MRC/EGC/SC/branch-block correction 同条件算法横比（L201-L207）。
4. 消融/扫描：linewidth、skew、aperture count、Rytov variance；没有 tap length/step size/核心模块 removal 消融。
5. 信道：AWGN 用于 linewidth/skew；Gamma-Gamma 强度衰落由 ATT 离线模拟，孔径独立。
6. 拓扑：1/2/4 aperture；没有不同孔径间距/相关性拓扑。
7. 复杂度：只作定性“hardware and algorithm complexity higher”，无 O()、FLOPs、latency（L209-L217）。
8. VVUQ：Verification 2/3（仿真+离线硬件）；Validation 1/3（非真实大气链路）；Uncertainty 1/3（100 trials 但无 interval/test）。

### 精确动作签名

`{I/Q-compensated, clock-recovered Hrx,i/Vrx,i complex sequences at 2 sps}_{i=1..N} -> CMA(QPSK)/RDE(QAM) error triggers SGD updates of 4N complex FIR filters in a 2N×2 butterfly -> X_hat/Y_hat at 1 sps, jointly amplitude-scaled, phase-rotated, polarization-demultiplexed, finite-skew/linear-distortion compensated and coherently combined -> downstream FOC + carrier-phase recovery + demapping`

**边界**：不是对“未经任何预处理的 raw ADC samples”直接操作；整数序列同步、I/Q imbalance、clock recovery 在前，FOC/phase recovery 在后（L49-L51、L123-L131）。已量化 skew 保障仅到 4 samples，>5 samples 可能不收敛；动态 gain/phase/SOP 的追踪速率未被实验量化（L149-L167）。

### 写作架构摘要（≤20 行）

1. Introduction：从 coherent FSO turbulence penalty → AO 成本 → multi-aperture diversity → PM combining 缺口推进。
2. 竞品压缩在一个段落：MRC/EGC/SC 的单偏振边界，training-based block phase correction 的 skew/fading 边界（L41）。
3. 贡献段直接给“system model + 2N×2 + blind SGD/CMA + simulation/experiment”四件套（L43-L47）。
4. Section II 同时放 system architecture、信号模型、butterfly FIR 和 update equations。
5. Fig.1 用端到端 DSP block diagram + 多孔径 constellation 小图，把系统位置与收益放同一图。
6. Fig.2 单独展开 2N×2 butterfly taps，支撑可复现性。
7. Section III 先声明 simulation settings follow experiment，再集中给实验器件/采样参数。
8. Results 先做算法边界扫描（linewidth、skew），后做硬件 receiver sanity check，再做 turbulence end-to-end gain。
9. Fig.4/5 是 mechanism/boundary figures；Fig.6 是 receiver validation；Fig.7/8 是 channel distribution 与 system outcome。
10. Conclusion 重复三类量化锚点：linewidth、skew、moderate/strong turbulence gains（L219-L221）。

## L4 — Tu et al., IEEE Photonics Journal 2020

### 标准字段（15/15）

1. **DOI**：10.1109/JPHOT.2020.2977955（L13、L29）。
2. **source path**：`papers/doi/10.1109_jphot.2020.2977955/content.md`。
3. **read status**：合格全文，fresh-context 全文精读完成；标题门 PASS。
4. **venue**：*IEEE Photonics Journal*, Vol. 12, No. 2（L7、L19-L23）。
5. **year**：2020；published 2020-03-03，current version 2020-03-26（L31）。
6. **贡献**：论文推导 phase-alignment averaging length/complexity、OPO estimation RMSE 与 EGC combining loss 之间的解析关系，使给定输入 OSNR 与允许 combining loss 时可直接选择最小所需 symbol count `M`（L33、L53、L165-L189、L257-L259）。它以大范围 OSNR、2/4 branches 的 Monte Carlo 仿真验证解析式，并量化把允许 CL 从 0.1 dB 放宽到 0.5 dB 可在一个四支路案例中降低约 80% 计算复杂度（L193-L255）。
7. **方法概览**：DCR 恢复各支路复光场并理想完成 time alignment 后，按 OSNR 从高到低，将 running coherent sum 与下一支路用 M 个 1-sps symbols 估计相对 OPO；下一支路乘 `exp(-j*phi_hat_n)` 后相加，递归至 N 支路（L55-L83、L245）。解析式由噪声统计给出 OPO RMSE 和平均 CL，从输入 OSNR、目标 CL 反求 M（L83-L189）。
8. **实验设置**：纯 numerical simulation；10-Gbps NRZ-BPSK，随机 OPO ∈ [−π,π]，input OSNR 跨 >33 dB、最低 −20 dB；20-GHz fourth-order Gaussian OBPF、10-GHz electrical LPF；LO 10 dBm、LFO 500 MHz、linewidth 10 kHz、calibration μ=1.2（L193-L195）。
9. **baseline**：解析 prediction 对 Monte Carlo；N=2 时 CL=0.1/0.5 dB，N=4 三组 OSNR vectors。引言定性比较 analog phase locking、MRC、EGC、SC，并引用 EGC 在较低复杂度下接近 MRC，但本文没有新的 phase-alignment algorithm baseline 横比（L51-L53、L197-L255）。
10. **结论**：M 由两输入信号总体质量决定；高 OSNR 可低至 M=1，低 OSNR 可高至 5000（L211-L225）。多数 N=2 区域中，CL=0.1 dB 时真实与目标 CL 偏差 <0.03 dB；CL=0.5 dB 时多数区域 <0.1 dB（L241-L243）。N=4 三案例解析与仿真最大 CL 误差 <0.05 dB、曲线尾端 <0.02 dB（L245-L255）。
11. **与本专题关系**：phase-alignment neighbor。其可调量是 estimator window M，不改变 EGC 的递归合并拓扑；它提供“可靠 phase estimate 的代价—损失”设计准则及不应合并的约 20-dB OSNR imbalance 边界（L225-L227）。
12. **具体实现**：PAA 按 symbol rate 采样；用 M 个 symbols 的复相关/累积估相对相位，旋转新支路再并入 running sum；N 支路递归。以输入 OSNR 和 prescribed CL 算 M，且 EGC 按高 OSNR→低 OSNR、只在 net gain positive 时执行（L77-L83、L165-L189、L245）。
13. **fit**：中高。可作为前置 phase-alignment estimator 的解析设计 neighbor，但假设 ideal time alignment、common narrow-linewidth LO、对应 symbols 具有相同 laser phase noise，且没有 turbulence time series/outage gating（L53-L57、L83-L89）。
14. **code**：全文未给代码仓库或补充代码链接；按全文证据记为“无公开代码指针”。
15. **validation**：论文 validation 为 analytical-vs-Monte-Carlo numerical validation；无硬件/现场实验。当前阅读验证为全文逐行审计，未做外部搜索/复现。

### 7 个结构段

#### state

非 DRL。算法输入状态等价物是已理想 time-aligned 的 running coherent sum `b_n`、下一支路 `b_{n+1}`、其输入 OSNR/幅度比、目标 combining loss，以及用于估计的 M-symbol block（L55-L83、L165-L189）。

#### action

非 DRL，**N/A**。算法动作等价物：估计 `phi_hat_n`，将下一支路乘 `exp(-j phi_hat_n)`，然后与 running sum 相加；设计动作是选择最小 M（L77-L83）。

#### reward/objective

非 DRL，reward **N/A**。显式 objective：在任意 input OSNR 下满足 prescribed average combining loss，同时最小化 PAA computation complexity（即 M）（L33、L53、L257-L259）。

#### model assumptions

- time alignment ideal；本文只研究 phase alignment（L53）。
- 多支路 DCR 共享 common narrow-linewidth LO；对应 symbols 的 laser phase noise 假定相同（L55-L57、L83-L89）。
- ASE 为不同放大器产生的独立 circular complex Gaussian noise（L83-L103）。
- 小角近似要求 `M A1 A2` 相对噪声扰动充分大；OPO RMSE >40° 的极端不平衡区域会破坏近似（L121-L145、L225-L227）。
- M-symbol duration 必须小于 atmospheric coherence time 与 laser coherence time；文中最大 11000 symbols=1.1 μs，小于约 1–10 ms 与 100 μs（L225）。

#### network/algorithm

非神经网络。串行 recursive EGC：one signal → estimate phase to next signal → rotate next → add to running sum，因 running sum SNR 随递归增加而优于 parallel/binary tree（L55-L83）。解析式预测每一步 OPO RMSE 与累计 average CL（L165-L189）。

#### fit

- 适配：给已 time-aligned 多孔径复场做低复杂度相位对齐；可从 OSNR 与 loss budget 直接定 M。
- 不适配/未覆盖：time/skew recovery、PM 双偏振/SOP、动态 block 内 phase drift、真实 turbulence/outage、硬件 latency。
- 候选证据用途：作为“phase estimator window adaptation”的 neighbor，而非 2N×2 joint equalizer competitor。

#### problem extraction（M-C-A + glossary 四判据）

**论文已解决的问题**：固定或未经解析设计的 PAA averaging length M（M），在多孔径高速 EGC-DCC、输入 OSNR 可低至 −20 dB且必须实时实现（C）时，因 OPO estimation error、combining loss 与计算量的耦合未被量化（A），无法在 loss budget 下选择最低复杂度（L51-L53、L193-L225）。

| glossary 判据 | 结果 | 论文内证据 |
|---|---|---|
| 1. M-C-A 具体技术矛盾 | ✅ | L51-L53 明确实时复杂度障碍与未讨论的 minimization problem |
| 2. 有可复用方法产出 | ✅ | OPO-RMSE/CL/M 解析设计公式族，L141-L189、L257-L259 |
| 3. 有近期 baseline 可对标 | ⚠️ | 以既有 recursive EGC PAA [7] 为 M（L55-L83），但实验对手是 Monte Carlo 而非另一近期 PAA |
| 4. 能量化对标 | ✅ | prescribed-vs-real CL、RMSE、M、complexity reduction，L197-L255 |

**候选而非 terminal 的残余问题证据**：其解析 PAA（M）在两支路 OSNR 相差约 20 dB或 OPO RMSE >40°（C）时，因小角近似失效且 EGC 会引入负净 OSNR gain（A），该区域应不执行 EGC（L225-L227、L243）。论文仅给“按 OSNR 排序且 net gain positive 才合并”的规则（L245），未处理观测 OSNR 不可靠或动态 outage 的判断误差。

### 通信参数表

| 链路/模块 | 模型 | 关键参数 | 来源 |
|---|---|---|---|
| 调制/速率 | NRZ-BPSK | 10 Gbps；PAA at 1 sample/symbol | L81、L193-L195 |
| OPO | random branch phase | uniform −π to π | L193-L195 |
| OSNR | ASE-loaded per branch | span >33 dB；minimum −20 dB | L193-L195 |
| optical filter | 4th-order Gaussian OBPF | 20 GHz 3-dB bandwidth | L193-L195 |
| electrical filter | 4th-order Gaussian LPF | 10 GHz 3-dB bandwidth | L193-L195 |
| LO/laser | common LO | LO 10 dBm；LFO 500 MHz；linewidth 10 kHz | L193-L195 |
| estimator | M-symbol phase estimate | M≈1 to 5000 in shown N=2 maps；tested max ≤11000 | L211-L225 |
| validation | Monte Carlo | 500 runs/data point for OPO RMSE；N=4 CL uses 300 runs | L227、L245 |

### 实验完备性（≤20 行）

1. Claims：解析式实现 prescribed-CL 下的 minimum-complexity M selection；范围限 EGC、ideal time alignment、common LO、simulation。
2. 统计：N=2 OPO RMSE 500 MC/data point；N=4 average CL 300 MC；无 confidence interval/test（L227、L245）。
3. Baseline：analytical expressions vs Monte Carlo；无 alternative PAA algorithm baseline。
4. 消融/扫描：N=2/4、CL=0.1/0.5 dB、OSNR plane/three 4-branch vectors、M sweep。
5. 信道：独立 complex Gaussian ASE；未模拟 atmosphere fading time process，只解释 OSNR range 对应 turbulence fades。
6. 拓扑：2 branches 与 4 branches；4-branch OSNR vectors 三组。
7. 复杂度：以 M 代表 PAA computation complexity；case 1 从 CL 0.1→0.5 dB 约降 80%，无 gate count/latency/O()（L245-L255）。
8. VVUQ：Verification 2/3（解析与 MC 一致）；Validation 1/3（无硬件/现场）；Uncertainty 2/3（300/500 MC，但无 interval/test）。

### 精确动作签名

`{digitally recovered complex fields, ideal time-aligned, running coherent sum b_n, next branch b_(n+1), input OSNRs, prescribed CL} -> analytical OSNR/CL relation selects minimum M; M-symbol complex phase estimator produces phi_hat_n -> rotate b_(n+1) by exp(-j phi_hat_n) -> add to running sum in descending-OSNR order if net EGC gain is positive -> final coherently combined field + predicted OPO RMSE/average CL`

**位置与输出**：PAA 位于 parallel DCR field recovery 和理想 time alignment **之后**、每一次 recursive EGC addition **之前**；它输出已相位旋转的新支路并形成更新后的 running coherent sum（L55-L83）。它不输出 time/skew correction，也不处理双偏振 SOP。

## 跨论文事实对照（不作方向判定）

| 维度 | JLT 2023 | JPHOT 2020 |
|---|---|---|
| estimator/combiner 形态 | 2N×2 blind joint FIR estimator/equalizer/combiner | M-symbol scalar relative-phase estimator + recursive EGC |
| 输入位置 | I/Q compensation、clock recovery 后的 N×(H/V)复序列 | DCR field recovery、ideal time alignment 后的 running sum + next branch |
| 输出 | 两路 PM demultiplexed coherent-combined symbols | 单路（BPSK）更新后的 coherent running sum |
| gain/phase/SOP/skew | 联合线性处理；有限 FIR/skew，动态跟踪未量化 | 只 phase；time alignment ideal，不含 SOP/skew |
| outage/弱支路边界 | 无显式 reject/gating；低 OSNR 通过 joint CMA 合并 | OSNR差约20 dB时 EGC可能负净增益，应跳过；假定 OSNR已知 |
| 关键证据 | JLT L49-L51、L85-L97、L149-L167 | JPHOT L53-L83、L211-L255 |

## 证据路径

- `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2023.3276637/content.md`
- `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/papers/doi/10.1109_jphot.2020.2977955/content.md`
- 既有 JLT note 仅作审计参考、未替代全文：`D:/code/study/research-protocol/papers/_read_notes/10.1109_JLT.2023.3276637.md`
