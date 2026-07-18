# [R009] residual cascade GW Step 1 检索与撞车审计

> 2026-07-16 | 关联：2026-07-10-dual-pol-osl-groundwork / D042

## 调研问题

检索 2019--2026 年双偏振相干光通信中“CMA/自适应线性前端 + neural residual/post-equalizer”的直接命中与强邻近，区分完整替换、级联、残差学习和参数预测；检查 FSO/Gamma--Gamma/SOP 直接覆盖，并判断当前候选是否形成可证伪的 M-C-A。

## 发现

### 1. 检索覆盖与去重数量

按任务要求执行六组 `tools/search`，JSON 均落盘于 `search-archive/2026-07-16/`：

| 查询 | 来源 | 去重结果 |
|---|---|---:|
| dual polarization coherent optical CMA neural network residual equalizer | s2 | 26 |
| CMA assisted neural network equalizer coherent optical | openalex | 22（原始 30，过滤 8） |
| hybrid CMA neural post equalizer optical communication | s2 | 30 |
| adaptive linear equalizer neural post equalizer dual polarization | openalex | 21（原始 30，过滤 9） |
| residual learning coherent optical equalization polarization | arxiv | 0 |
| FSO CMA neural equalizer Gamma Gamma SOP | s2 | 1 |

合并后按 DOI/标题去重约 70 条；搜索索引更新出现一次临时文件 rename 警告，但各查询 JSON 已成功保存。arXiv 查询为零不能解释为绝对空白。

### 2. 直接命中

未发现严格直接命中（标准 CMA 始终在线、NN 仅输出 `g(z_cma)` 并以加法残差合成）。最接近的是：

| 论文 | 年份/venue | pipeline | 信息访问 | 对本候选影响 | abstract/DOI 证据 |
|---|---|---|---|---|---|
| *Demonstration of 144-Gbps Photonics-Assisted THz Wireless Transmission at 500 GHz Enabled by Joint DBN Equalizer* | 2022, Micromachines | **级联/联合替换**：J-DBN 方案“mainly optimized based upon CMA and DD-LMS”；NN 作为联合 equalizer，不是 residual add-on | DOI 10.3390/mi13101617，OpenAlex 摘要落盘 | 强邻近但非撞车；显示 CMA+NN 组合已有先例，必须证明 residual 约束带来额外信息 | 摘要明确写 “optimized based upon CMA and DD-LMS”，未称 residual |
| *Blind Equalization and Channel Estimation in Coherent Optical Communications Using Variational Autoencoders* | 2022, JSAC | **完整替换**：VAE blind equalizer 直接做信道估计/载波恢复，含 DP、oversampling、PCS | DOI 10.1109/JSAC.2022.3191346 | 不能作为 residual 命中；提示 blind NN 已覆盖“从接收信号直接恢复”路线 | 摘要描述 adaptive blind equalizer/VAE channel estimation，无 CMA 前端 |
| *Convolutional Neural Network-Aided DP-64QAM Coherent Optical Communication Systems* | 2022, JLT | **完整非线性补偿**：CNN 结合一阶扰动特征图，直接作 NN equalizer | DOI 10.1109/JLT.2022.3146839 | 增益来自 Kerr 非线性；当前 FSO 信道无 Kerr 时不可直接迁移 | 摘要明确 375-km DP-64QAM、optical nonlinearity |

没有论文摘要同时给出“CMA 输出作为 NN 输入、NN 只学习误差并与 CMA 相加”的明确结构，因此“无人直接做过”仅作为撞车审计结果，不能作为 Go 理由。

### 3. 强邻近与简单 baseline

- *Soft-Demapping for Short Reach Optical Communication: A Comparison of DNNs and Volterra Series* (2021, JLT, DOI 10.1109/JLT.2021.3056869)：DP-64QAM 实测，DNN 与五阶 Volterra 对比；是 post-equalization/soft-demapping，非 CMA residual。摘要报告同等性能复杂度降低 65%、同等复杂度 OSNR 提升 0.35 dB。
- *Performance versus Complexity Study of Neural Network Equalizers in Coherent Optical Systems* (2021)：实验主导 Kerr 与器件缺陷，比较 CNN/BNN 等 NN equalizer，属于完整 NN 后均衡，不是 residual。
- *Neural Networks-Based Equalizers for Coherent Optical Transmission: Caveats and Pitfalls* (2022, JSTQE, DOI 10.1109/JSTQE.2022.3174268)：总结 NN equalizer 指标、损失和泛化陷阱；支持 pilot/训练公平性审查。
- *A Nonlinear Concurrent Butterfly Equalizer* (2021, OpenAlex)：传统 DSP，比较 CMA、MCMA、CMA-SDD，针对 PMD 与稳态 MSE/BER；说明无需 ML 的自适应增强已覆盖部分“CMA 残差”。
- 查询结果还反复出现 DD-LMS、Volterra、MMA/MCMA、DFE/FFE 等简单基线。候选若推进，至少要与 DD-LMS/RDE/MMA 及 Volterra/线性 MMSE 对比，否则无法证明残差 head 的增量。

### 4. FSO 直接覆盖

FSO 查询仅返回 *Symbol detection and BER analysis in wireless and free space optical networks using low complexity neural equalizer* (2025, Wireless Networks, DOI 10.1007/s11276-025-03916-4)，摘要为宽泛 6G/无线与 FSO 神经检测，未出现 CMA、Gamma--Gamma 或 SOP 漂移细节，故标为**假/弱命中**。

在 DP-SC FSO 相关结果中，*ANN-Based Equalization of Polarization Mixing and MZM Nonlinearity for Dual-Polarization Self-Coherent Transceivers in Free Space Optical Communications*（2026，搜索结果摘要）直接涉及 DP FSO、偏振混合和 MZM 非线性，但其 ANN 从 3PD 电流直接学习符号，替代 matrix-inversion DSP；摘要明确 pointing error/scintillation 未建模，也无 CMA 前端或 residual 结构。因此是场景邻近而非直接命中。

### 5. 本地信道是否包含可学残差

候选临时 A（CMA 有限步长/taps/恒模准则留下稳定可学习残差）在现有检索中没有外部证据支持。可迁移的文献残差来源主要是 Kerr 非线性、器件非线性、PMD/色散、相位恢复或 ADC 缺陷；任务背景的本地 GG 湍流 + 连续 SOP 漂移若仅含线性 Jones/SOP 变化、AWGN 与 scintillation，而不含 Kerr/器件非线性，则上述 NN 增益不能直接外推。现有 D040 数字（fixed BER≈2e-4、oracle≈3.5e-5）只能说明存在性能 gap，不能说明 gap 具备稳定、低维、pilot 可学习结构。

## 结论

### 候选 Q#（M-C-A）

Q#：在双偏振相干 FSO 的 GG 湍流与连续 SOP 漂移条件 C 下，合法 standard-CMA（M）虽保持 fixed tributary label，但有限 taps/步长导致的残余误差是否具有跨块稳定结构，使小型监督 residual head 学得 `g(z_cma)` 并以 `z_out=z_cma+g(z_cma)` 在固定标签约束下把 BER 从约 2e-4 推近 oracle（约 3.5e-5），且优于 DD-LMS/RDE/MMA 等非 ML 增强？

### 四判据

1. **问题具体性：暂过。** M、C、A 已可写成上述机制链，但 A（可学习残差来源）尚无实证。
2. **重要性：暂过。** D040 gap 约 5.7×，但为单一当前域数字，尚未证明跨 seed/块稳定。
3. **可证伪性：过。** 可用 fixed-label BER、oracle gap、残差预测增益和跨块泛化检验；若无增益或触发 swap 即失败。
4. **非平凡性/新颖性：不充分。** 检索未见严格 residual 命中，但已有 CMA+NN 联合/后均衡和大量简单 DSP；“没人直接做过”不能替代机制性新颖性。

### Step 1 判定：DEFER

不建议直接进入 MVE。候选可保留至 Step 2 获取/Step 3 精读，前提是先补齐： (i) 近邻论文全文中是否存在隐含 residual/级联实现；(ii) 本地信道是否确实产生非线性或有限-tap 记忆结构；(iii) 非 ML baseline 是否已消除 gap。若 Step 2/3 证明残差来源仅为模型不存在的 Kerr/器件损伤，或 DD-LMS/RDE 已达到同等 BER，则应 KILL；若能确认 SOP 漂移下存在跨块稳定、低维残差且 residual > 传统 baseline，才可转 Step 4a。

## 对决策的影响

- 支持 D042 的谨慎方向：standard-CMA 必须永在线、固定标签优先，不能把完整 ML 替换或 detector-triggered switching 计为同一候选。
- 新增检索证据：CMA+NN 组合已有（J-DBN/CMA/DD-LMS）但非 residual；DP-FSO ANN 也已有但无 CMA、无 Gamma--Gamma/SOP 完整建模。
- 依据 FR-23/FR-25，当前只能给 DEFER，不得以“空白”直接 Go，也不得启动 MVE。
