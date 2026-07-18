# [S038] residual-cascade GW Step 3 全文精读

> 2026-07-16 | Groundwork Step 3（gw-read）| 状态：PASS（5/5 全文已读；均为直接或方法邻近证据，未发现直接先例）

## 目标与边界

本轮只验证“standard-CMA always-online + additive NN residual”候选的文献证据链。逐篇读取 T003 指定的本地 `content.md`/PDF 转换文本，完成标题自检、M-C-A、输入输出、训练测试、信道与指标、baseline、复杂度和泄漏风险提取。本文不作 Step 4a Go/No-Go，不跑 MVE，不修改仿真代码。

## 1. 逐篇条目

### L01 — Blind Equalization and Channel Estimation in Coherent Optical Communications Using Variational Autoencoders

- **作者/年份/来源**：Lauinger et al.; 2022; IEEE Journal on Selected Areas in Communications。
- **源文件**：`papers/doi/10.1109_jsac.2022.3191346/content.md`（首行标题与正文一致；title check PASS）。
- **关系判定**：**adjacent（强邻近，不是 direct）**。论文训练完整 VAE-LE/VAE-NN，不是 `z_CMA + additive residual`；但明确以 CMA 作为盲均衡 baseline，并给出在线 mini-batch 更新机制。
- **问题 M-C-A**：M=CMA/FIR blind equalizer；C=DP、过采样、线性 ISI/PMD/CD、PCS 或时变 HV 相位；A=constant-modulus criterion 对多幅度/近高斯 PCS 先验失配，且相位不敏感，导致 PCS 收敛/载波恢复困难（正文 §§1、4、5，约行 9–13、176–180、220–276）。
- **方法**：VAE-LE 用 2×2 butterfly 复数 FIR；同时学习 equalizer 参数 Φ 和 channel-model 参数 θ，ELBO/soft-demapper 作为无监督目标。VAE-NN 是两层 1-D CNN，输出各幅度的 softmax 概率（约行 137–164）。
- **输入/输出与动作空间**：输入为接收复数双偏振序列 y；VAE-LE 输出均衡复符号和 soft-demapper 概率，VAE-NN 直接输出每符号各星座点概率；连续参数为 FIR taps/NN weights，无离散动作。
- **训练/测试协议**：在线自适应而非 train/validation/test 切分；连续缓存接收流，按 `N_B·N_os` mini-batch 更新，Adam 每 batch 更新；VAEflex 通过重叠窗口增加更新频率（约行 174–180）。默认 `N_run=10`，每次 170 个 10,000-symbol frame，移动平均 `F_ma=10`，每帧至少约 8,000 符号，SER<0.3 的 run 才纳入均值（约行 220–236）。这会把“训练数据”和“评估数据”合并，适合 online tracking，但不能直接作为独立泛化证据。
- **信道/数据**：AWGN+5-tap complex ISI；RRC roll-off α=0.1、`N_os=2`；DP 光纤线性频域 2×2 H(f)，含 `D_pmd=0.1 ps/√km, L_pmd=1000 km, β_cd=-26 ps²/km, L_cd=1 km, γ_hv=0.1π, φ_IQ=0.01π`；时变场景每 10,000 symbols 改变 HV phase。非线性和相噪被假定可忽略或由独立 DSP 补偿（约行 17–27、220）。
- **目标/公式**：ELBO 等价于最小化 `D_KL(P(x|y)||Q_Φ(x|y))`；soft demapper 使用 `q_i^c(y)=softmax(-(x̂_i^c1-A)^2/(2σ_w²)-νA_sq)`（约行 38–50、162–170）。无 RL reward。
- **Baseline 与主要数字**：No-ISI、CMA、非盲 DFE（FF/FB 各 10 taps）、线性 MMSE（20 taps）。CMA 对 uniform 64-QAM 明显劣于 MMSE，VAE-LE 接近 MMSE；PCS 场景 CMA 不能收敛，而 VAE-LE 在较高 SNR 接近 MMSE（约行 220–276）。论文未给 additive-residual 增益。
- **标签/泄漏风险**：VAE 是无监督，不需真实 x 标签；但 channel likelihood 需设定噪声/先验，且在同一流上训练和评估，存在适应过程混入指标的风险。无 pilot/CSI；以模型化 `H(f)`/noise prior 作为结构先验。
- **复杂度/延迟**：VAE-LE 需 equalizer 与 channel-model 两套 filter、soft-demapper 和反向传播；作者指出比 CMA 更新复杂，未来工作才讨论复杂度降低。batch 更新可比 CMA symbol-wise 更新更快（CPU 观察，约行 174–180）。
- **7 子表（L01）**：
  - 状态空间：接收复数样本、2 偏振、ISI/PMD/CD；归一化细节只给噪声方差与 MB prior，未统一列出输入标准化。
  - 动作空间：连续 FIR/NN 权重；无显式动作约束。
  - 奖励/损失：`ELBO = E_Q[log p_θ(y|x)] - D_KL(Q_Φ(x|y)||P(x))`；无权重表；Adam。
  - 建模假设：线性光纤主导；非线性/相噪独立补偿；PCS 符号独立、I/Q 条件独立。
  - 网络：VAE-NN 两个 1-D conv，第二 kernel 3–5，第一 kernel/估计 CIR 常约 29（2 sps）或 11（1 sps），ELU+softmax；VAE-LE butterfly FIR。
  - 适配性：可借鉴 online batch、same-taps DSP integration；不适配是完整 VAE 不能证明 additive residual 的增量信息，且复杂度高；改进方向是让 CMA 输出作为固定前端、NN 只估计 residual，并用独立 test stream。
  - 问题提取：Q1 通过 glossary 四判据（M/C/A 具体；VAE-LE 是可复用算法；CMA baseline；SER/SNR 可量化）。
- **实验完备性**：声称限于仿真线性/时变 DP；10 runs、约 80k–100k symbols/frame 的 moving-average，baseline 包含 CMA/MMSE/DFE；无消融 residual；无 pilot；复杂度仅定性/CPU 观察；VVUQ：V=2, Vd=2, U=1（噪声/信道假设敏感性未系统扫描）。

### L02 — Soft-Demapping for Short Reach Optical Communication: A Comparison of Deep Neural Networks and Volterra Series

- **作者/年份/来源**：Maximilian Schaedler, Georg Böcherer, Stephan Pachnicke; 2021; IEEE Journal of Lightwave Technology（本地 DOI 文本包含 arXiv HTML 标记，但正文标题自洽；title check PASS）。
- **关系判定**：**adjacent**。SDNNE 是完整 nonlinear soft-demapper，不是 CMA 前端加 residual。
- **问题 M-C-A**：M=5th-order Volterra nonlinear equalizer（VNLE）；C=92-GBd dual-polarization 64-QAM、950 Gb/s back-to-back、光电器件非线性主导；A=高阶 Volterra kernel 数量/乘法数导致复杂度和内存开销，且训练矩阵可病态（§II-A、§III–IV）。
- **方法/输入输出**：比较 MSE-trained VNLE 与 bit-wise soft DNN equalizer（SDNNE）。输入为接收时域窗口，输出为每比特 LLR/soft-demapping；训练损失为 bit-wise equivocation，等价 binary cross entropy（Eq. 13、18，约行 466–512）。不是“符号 residual”输出。
- **训练/测试协议**：92-GBd DP-64QAM back-to-back measurements；摘要给出比较在 15% OH FEC limit，复杂度/OSNR 曲线覆盖多个网络和 VNLE kernel 配置。训练使用 transmitted/received data 识别 kernels；论文未报告多随机 seed、独立跨信道 test 或统计检验，需标 UNKNOWN。
- **信道/指标**：真实 BtB 光电链路，系统性非线性；主要指标 OSNR gain、achievable rate/FEC limit、乘法数。结论：等性能时 SDNNE 比 VNLE 少 65% multipliers；等复杂度时 OSNR 提升 0.35 dB（摘要、结论约行 42、466–469）。剪枝 VNLE 平均复杂度再降 25%，SDNNE 低复杂度剪枝约 20–45%（约行 443、451）。
- **Baseline**：5th-order full/pruned VNLE；不同 memory/order 的 VNLE envelope；无 CMA baseline，无 residual ablation。
- **标签/泄漏风险**：监督式，需传输 bit/符号作为标签；若训练与评估使用同一 BtB 分布，泛化到新信道、功率、OSNR 未被证明。无 pilot/CSI 的在线盲更新；训练数据依赖真实发送序列。
- **网络/复杂度**：正文强调层数/hidden neurons 与乘法数的 trade-off；具体每个 architecture 以图表标注，未在转换文本中完整保留所有层宽，故不可补写。复杂度按乘法数和 sparsity 报告。
- **7 子表（L02）**：状态=时域接收窗口/bit labels；动作=连续 NN weights 或 VNLE kernels；损失 `L(b,ℓ)=log(1+exp(-ℓ))` for b=0 / `log(1+exp(ℓ))` for b=1（Eq.13）；假设=BtB器件非线性、训练标签可用；网络=SDNNE，具体层宽仅部分可见；适配=复杂度/soft loss 可作为 residual head 的上限参照，不适配=非盲监督且无 CMA 前端；问题提取 Q2 通过四判据（但 C 是 BtB，迁移至 dual-pol OSL 仍 UNKNOWN）。
- **实验完备性**：声称限于 92-GBd BtB；baseline 矩阵充分（VNLE order/memory/pruning），无 seed/error bars/显式消融，信道单一，复杂度报告较完整；VVUQ：V=2, Vd=2, U=1。

### L03 — Neural Networks-based Equalizers for Coherent Optical Transmission: Caveats and Pitfalls

- **作者/年份/来源**：Pedro J. Freire, Antonio Napoli, Bernhard Spinnler, Nelson Costa, Sergei K. Turitsyn, Jaroslaw E. Prilepsky; 2021 arXiv preprint 2109.14942（`metadata.json` real_title 与正文标题一致；title_check=unverifiable，但前 20 行明确主题，继续）。
- **关系判定**：**adjacent/methodology**。它不是一个 residual 算法，而是对 NN equalizer 设计、训练和指标的系统性反例/指南。
- **问题 M-C-A**：M=NN-based nonlinear equalizer（MLP/biLSTM/classifier/regressor）；C=高精度 coherent optical equalization、有限 PRBS/DAC memory、不同 QAM cardinality 和 mini-batch；A=过拟合、学习噪声/周期性、局部极小、batch 与 constellation amplitude 覆盖不足、复杂度/延迟错配。
- **方法/输入输出**：对比 MLP、biLSTM、分类器/回归器；输出为均衡复符号或分类结果。重点不是新算法，而是改变 loss、数据分割、PRBS、batch size、复杂度估计以避免假增益。
- **训练/测试协议与数据**：模拟 SSMF `16×60 km`，5 dBm launch power，34.4 GBd；QAM 8/16/32/64/128，batch 8/16/32/64/128/2048。对 16-QAM，biLSTM 从 batch 8 到 2048 的 Q-factor 提升约 3 dB；128-QAM 从 3.54 提升到 4.27 dB（正文约行 381–399）。讨论“jail window”即训练集噪声/周期性被学入，训练/测试 loss gap 仍可能很小。
- **Baseline/指标**：MLP 与 biLSTM 相互对比，参考 Q-factor；同时讨论 BER 约 `10^-3–10^-2` 的光通信要求和 pre-FEC 阈值（约行 27–39）。无 CMA residual baseline。
- **标签/泄漏风险**：监督训练使用发送序列标签；PRBS 低阶、重复 pattern、训练/测试相关性会造成泄漏。明确建议检查跨数据、跨信道泛化。无 pilot/CSI要求，但训练阶段需要完整标签。
- **复杂度/延迟**：论文给出 DSP 乘法/参数与 processing latency 的分析框架；转换文本中未保留全部网络尺寸，不能自行补值。指出 mini-batch 过大可能导致 sharp minima，过小导致 constellation coverage 不足。
- **7 子表（L03）**：状态=接收窗口、constellation/QAM cardinality、batch；动作=NN weights；损失含 MSE/CEL 等但本文不钉死单一公式；建模=SSMF 16×60 km、非线性；网络=MLP/biLSTM；适配=直接支撑 residual 训练的泄漏/批大小门控，不适配=并未证明 residual head；问题 Q3 可形成“有限训练/批次覆盖导致 NN equalizer 失效”的可量化问题，但需明确 baseline 与场景迁移。
- **实验完备性**：参数 sweep 覆盖 QAM 与 batch，给出 Q-factor 曲线和 constellation；未见多 seed/统计显著性；信道为单一高非线性 SSMF 例；复杂度框架较强；VVUQ：V=2, Vd=2, U=2（batch/PRBS/模型假设均可能影响结论）。

### L04 — Convolutional Neural Network-Aided DP-64 QAM Coherent Optical Communication Systems

- **作者/年份/来源**：Chao Li et al.; 2022; IEEE Journal of Lightwave Technology 40(9)。源文件 `papers/doi/10.1109_jlt.2022.3146839/9695357.md`，首行标题、DOI、实验正文一致；title check PASS。
- **关系判定**：**adjacent**。它将 CNN 学习目标设为 `b−a`（接收符号减发送符号），形式上是 error/residual target，但输入是基于一阶扰动构造的 feature map，且 CNN 完整替代 NLE，不是 `standard CMA always-online + additive residual`。
- **问题 M-C-A**：M=perturbation-based/fully-connected nonlinear compensation；C=375 km（5×75 km）120-Gbit/s DP-64QAM，光纤 Kerr 非线性；A=非线性记忆与高维 FUs 使传统 FC/Volterra 乘法和空间复杂度高，且忽略 FU 的实虚/位置相关性会丢信息（约 PDF 文本页 2881–2883）。
- **方法/输入输出**：从接收 `b_x/y[k]` 构造复 FUs，保留 real/imag 两通道，`S=5` 得 11×11×2 feature map；CNN conv1=16 channels, 6×6 kernel；conv2=128 channels, 6×6；FC=64、10 neurons；leaky-ReLU、batch normalization、无 pooling/padding。Classifier 输出 64 类 softmax；regressor 输出 2 维，监督目标 `b_x/y[k]−a_x/y[k]`，推理以 `b−ŷ` 完成补偿（约 PDF 文本页 2882–2884）。
- **训练/测试与标签**：每个 launch optical power 约 65k symbols，80% train/20% test，两部分归一化互相关 ≤0.5%；dropout 0/0.3/0.5/0.7 sweep。强监督，标签直接使用发送符号；不是 blind/online。
- **信道/指标/结果**：G.652D 5×75 km；AWG 25 GSa/s、DPO 100 GSa/s、ECL linewidth 100 kHz；launch power 扫描。channel size 11 时 classifier 最佳 BER 0.0012（1 dBm），regressor 0.0020（0 dBm）；均可低于 7% HD-FEC threshold 0.0038（约 −3–3 dBm）；channel size 15 在 −4/4/5 dBm 可低于 0.0020。相对 FC(2392-64-64)，time complexity 约降 25%，space 约降 50%（摘要）。
- **Baseline**：perturbative NLE、FC NN、CNN classifier/regressor；没有 CMA、MMA、RDE 或 blind baseline。
- **泄漏/复杂度**：发送标签及 80/20 split 是核心监督信息；虽然 train/test 低相关，但跨 launch/channel 未验证。dropout 防过拟合；复杂度有明确相对数字，但未报告在线每符号延迟。
- **7 子表（L04）**：状态=11×11×2 engineered FU；动作=连续 CNN weights；损失=classifier cross-entropy，regressor `MSE + λ||ω||²`（公式图片在转换文本中缺失，保留公式类型而不补权重）；假设=一阶 perturbation/FU 足以表征 Kerr；网络如上；适配=残差标签和复杂度分析可借鉴；不适配=监督、静态离线、非 CMA 前端；Q4 通过四判据但迁移到 GG/SOP 条件为 UNKNOWN。
- **实验完备性**：80/20 split、dropout sweep、功率 sweep，baseline 有 FC 和两种 CNN；无多 seed/统计检验；单一 375-km link；复杂度报告强；VVUQ：V=2, Vd=2, U=1。

### L05 — Multi-Aperture Coherent Digital Combining Based on Complex-Valued MIMO 2N×2 Adaptive Equalizer for FSO Communication

- **作者/年份/来源**：Na Liu, Cheng Ju, Dongdong Wang, Danshi Wang, Peng Xie; 2023; IEEE Journal of Lightwave Technology 41(18), DOI 10.1109/JLT.2023.3276637。
- **源文件**：`papers/doi/10.1109_jlt.2023.3276637/content.md`；正文首行标题与 DOI/作者一致，title check PASS（任务 brief 的“CMA-based … FSO”是简称，不是正式标题）。
- **关系判定**：**adjacent**。这是 standard CMA/RDE blind MIMO combiner 的直接邻近 baseline，但没有 NN residual。
- **问题 M-C-A**：M=2N×2 complex-valued MIMO butterfly equalizer with CMA (QPSK)/RDE (higher QAM) tap updates；C=2/4-aperture coherent FSO、Gamma–Gamma moderate/strong turbulence、branch skew；A=静态 skew、时变 gain/phase/SOP 和 turbulence fading 使光学对准/单 aperture 接收困难。论文证明 CMA tap adaptation 可电子补偿 skew，但不是 residual 学习问题。
- **方法/输入输出**：每个 aperture branch 的 X/Y complex samples 输入 2N×2 butterfly；SGD 更新 tap，误差由 CMA 或 RDE radius error 定义；输出合并后的 X/Y symbols。公式 (5)–(10)，约正文行 85–117。
- **训练/实验协议**：10-Gbps PM-QPSK，64K bits repeated，1550.32 nm、20 kHz linewidth、−3 dBm launch；ADC 5 GSa/s/8-bit，1M samples/branch；仿真评估 linewidth/skew，离线实验评估 1/2/4 apertures。平均 BER 用 100 个独立 Gamma–Gamma turbulence experiments；Rytov variance 0.5/1，最大 fading 11/16 dB（约行 119–131、177–201）。
- **Baseline/数字结果**：single aperture no turbulence benchmark；两/四 aperture 对比。FEC threshold 等效 OSNR：Rytov 0.5 时 11.2/7.1 dB，Rytov 1 时 13.8/9 dB；在单 aperture 3.4 dB 等效 OSNR，Q² penalty 5.4/6.7 dB；两/四 aperture Q² 增益分别 1.4/3.2 dB（中等）与 2.1/3.6 dB（强），约行 201–221。
- **标签/泄漏风险**：盲 CMA/RDE，无 pilot/CSI；实验中共享 25-MHz clock 并预先用 cross-correlation 做整数同步，Viterbi–Viterbi 做残余相位恢复，故不等于“全盲端到端”。四 aperture turbulence branches 假设独立 Gamma–Gamma fades。
- **复杂度/延迟**：多 aperture 使硬件和算法复杂度提高；skew<4 samples 无 OSNR penalty 但 convergence 变慢；skew 0/400/800 ps 需要 12/20/28 K symbols 收敛，超过 5 samples 可能不收敛（约行 149–167）。
- **7 子表（L05）**：状态=各 aperture 2N×2 complex tap/input；动作=连续 tap coefficients，SGD step μ；损失/MSE=`10 log10((1/M)Σ|ε_x/y(k)|²)`，Q² 由 `20 log10(√2 erfcinv(2 BER))`；假设=Gamma–Gamma、独立 aperture、共享时钟；网络=线性 butterfly FIR；适配=提供 current standard-CMA online 前端和 turbulence/skew stress test；不适配=没有 NN residual/监督 labels；Q5 是 CMA 在 FSO C 下改善 skew/turbulence 的问题，四判据中方法产出与 baseline 对标成立，但与本 residual 候选直接性低。
- **实验完备性**：100 independent turbulence trials，2/4 aperture 对照，linewidth/skew sweeps，Q²/BER 指标；无 NN 消融/seed report；信道参数与硬件细节完整；复杂度只定性；VVUQ：V=3, Vd=2, U=2。

## 2. 跨论文七个子表

### 2.1 M-C-A 映射

|论文|M|C|A|对 residual-cascade 的证据|
|---|---|---|---|---|
|L01|CMA|DP/PCS、ISI/PMD/CD、时变|constant-modulus/phase-blind mismatch|直接证明 CMA 失效条件，但 VAE 是替代，不是 residual|
|L02|5th-order VNLE|92-GBd DP-64QAM BtB|复杂度/病态 kernel|说明 residual head 必须过复杂度门；非 CMA|
|L03|NN equalizer|高精度、有限 PRBS/batch|overfit、局部极小、覆盖不足|为训练公平/泄漏审计提供强证据|
|L04|FC/perturbative NLE|375 km DP-64QAM Kerr|高维记忆与复杂度|`b-a` residual target 的邻近先例；非 online/blind|
|L05|CMA/RDE MIMO|FSO Gamma–Gamma、skew、SOP|fading/skew|提供标准 CMA 在线前端 stress 条件|

### 2.2 Baseline 对照

|论文|传统 baseline|NN/新方法|指标|
|---|---|---|---|
|L01|CMA、MMSE、DFE、No-ISI|VAE-LE/VAE-NN|SER/SNR|
|L02|full/pruned VNLE|SDNNE|OSNR/FEC/乘法数|
|L03|MLP、biLSTM互比|训练规范分析|Q-factor、BER|
|L04|FC perturbative NLE|CNN classifier/regressor|BER、复杂度|
|L05|single-aperture/no turbulence|2/4 aperture CMA/RDE combiner|BER/Q²/OSNR|

### 2.3 输入输出/动作空间

|论文|输入|输出|是否 residual|
|---|---|---|---|
|L01|双偏振复序列|均衡符号/soft probabilities|否|
|L02|接收窗口+labels|bit LLR|否|
|L03|接收窗口|复符号/类别|否|
|L04|FU 11×11×2|类别或 `b−a` 估计|目标 residual，非 additive cascade|
|L05|多 aperture 复序列|合并符号|否|

### 2.4 训练/测试公平性

|论文|训练信息|独立测试|统计/泄漏风险|
|---|---|---|---|
|L01|无监督同一接收流在线更新|无独立 train/test|适应过程进入评估|
|L02|监督 transmitted/received|未明确跨信道独立性|seed/CI 未报告|
|L03|监督 labels、PRBS/batch|强调应隔离但具体跨场景有限|过拟合/周期泄漏核心风险|
|L04|约65k symbols，80/20，corr≤0.5%|有 test split|labels 可用；跨功率/信道未知|
|L05|盲 CMA/RDE|100 independent turbulence trials|共享时钟/同步/相位模块为隐藏先验|

### 2.5 信道/扰动

|论文|信道|扰动范围|对本候选启示|
|---|---|---|---|
|L01|AWGN/DP linear H(f)|PMD/CD/时变 HV/PCS|先验证 CMA residual 是否存在于线性+PCS|
|L02|92-GBd DP BtB|器件非线性|residual 增益可能依赖未建模器件非线性|
|L03|SSMF 16×60 km|Kerr、QAM cardinality/batch|必须分离模型误差与训练伪影|
|L04|G.652D 5×75 km|Kerr、launch power|残差监督可借鉴，但目标不同|
|L05|Gamma–Gamma FSO|Rytov 0.5/1、skew、linewidth|CMA 前端需覆盖 fading/SOP，不可只测 GG 无 skew|

### 2.6 指标口径

|论文|主指标|统计口径|风险|
|---|---|---|---|
|L01|SER/SNR|10 runs、moving-average、成功 run 均值最小值|选择 min 可能偏乐观|
|L02|OSNR/FEC/乘法数|FEC threshold 曲线|无多 seed/CI|
|L03|Q-factor/BER|batch/QAM sweep|部分指标为场景特定|
|L04|BER/FEC/complexity|功率/feature-map sweep|无 CI，FEC threshold 需统一|
|L05|BER/Q²/OSNR|100 turbulence trials|Q² 转换与 BER denominator 需统一|

### 2.7 可复现实验条件

|论文|可复现强项|缺口|
|---|---|---|
|L01|信道参数、filter taps、batch、run 数明确；有 source-code 引用|未验证 source availability；非线性被排除|
|L02|92 GBd、DP-64QAM、FEC/复杂度数字明确|网络层宽/训练 seed 不完整|
|L03|SSMF、功率、symbol rate、batch/QAM sweep 明确|部分模型/数据集细节不全|
|L04|375 km、采样率、网络层、65k/80-20、dropout 明确|公式图片缺失；optimizer/epoch/seed不全|
|L05|10 Gbps、linewidth、ADC、Gamma–Gamma、100 trials 明确|部分硬件 DSP 依赖未开源|

## 3. residual-cascade 候选四判据审查（不作 Go/No-Go）

候选暂表述为：`z_cma = CMA(y)`，`z_out = z_cma + g_φ(z_cma, context)`，其中 g 只学残差、训练标签为 `s−z_cma`，并与 CMA-only/raw-ML/fixed+PI/oracle 比较。

|判据|状态|证据/缺口|
|---|---|---|
|1 具体技术矛盾 M/C/A|**PASS（候选可写成）**|L01 给出 CMA 在 PCS/多幅度 C 下因 constant-modulus/phase-blind A 失效；L05 给出 SOP/skew/turbulence C。需在 Step 4a 固定单一 C，避免把多个条件拼成空泛问题。|
|2 有可复用方法产出|**UNKNOWN**|L04 支持 residual target 的可复用形式，L01 支持 online CMA 前端；但尚无文献证明 additive residual 在当前 GG+SOP/线性模型中有稳定信息增量，不能以邻近证据代替。|
|3 有近期 baseline M|**PASS**|CMA/RDE/ML/VAE-LE 具备可实现 baseline；L01/L05 给出标准 CMA 在线与 MIMO 结构。目标 baseline 需按项目标准选定，不能把 VAE 当传统 CMA 对手。|
|4 可量化对标|**PASS（协议尚未冻结）**|候选可比较 BER/SER/Q²/OSNR、swap rate、收敛符号数和 MAC/latency；L01/L04/L05 提供指标口径，但需要同一 denominator、pilot/CSI budget 与 test stream。|

**精读结论（仅 Step 3）**：5/5 文件均已全文读取并完成结构化提取；没有找到“standard CMA always-online + additive NN residual”的直接先例。证据链最强的组合是 L01（CMA 失效条件与 online adaptive DSP）、L04（监督 residual target 的邻近形态）、L05（CMA 在 FSO 扰动下的压力测试）；L03 负责训练公平性/泄漏门控，L02 负责复杂度门控。候选仍需 Step 4a 验证“残差是否在当前信道中有可辨识增量”，本文件不越权判 Go/No-Go。

## 决策引用

- D042：主控可在软件 DSP/ML 的 A–E+H 范围内自主排名、停止或换方向。
- D043：严格 equivariance/e2cnn 不能作为固定标签解；本轮只评估 residual cascade。

## 范围确认

- 本轮是否在 scope boundary 内：是。未跑 MVE、未进入 Step 4a、未修改代码。

## 后续

主控需将 Q1–Q5 证据写入候选问题清单，先完成 Step 4a A0/A′/A 的单一 C 冻结和信息增量判据；若 residual 不能在当前模型中形成稳定可量化增益，应按 D042 选择下一条软件 DSP 路线。 
