# [R009] Ch2+Ch3 关键基线论文验证

> 2026-05-29 | 研究验证 | 完成

## Ch2 论文验证结果

### Amirabadi 2019
- **是否找到**：是
- **实际标题**：Deep learning for channel estimation in FSO communication system
- **作者**：MA Amirabadi, MH Kahaei, SA Nezamalhosseini, VT Vakili
- **期刊/年份**：Optics Communications, 2019（预印本/在线版2019，正式出版2020）
- **引用数（实际）**：61（Semantic Scholar）~ 87（Exa），随时间增长
- **核心内容确认**：DNN 信道估计 GG 模型 FSO 系统，减少导频开销
- **与声称是否一致**：**基本一致**。年份略有歧义（2019在线/2020出版），引用数61对应较早快照。可用作基线。

### Elfiky 2024
- **是否找到**：是（需修正）
- **实际标题**：Symbol detection and channel estimation for space optical communications using neural network and autoencoder
- **作者**：A Elfiky, Z Rezki
- **期刊/年份**：**2023**（非声称的2024）；未检索到 IEEE TMLCN 期刊标识
- **引用数（实际）**：19（声称16）
- **核心内容确认**：NN 信道估计器 + 自编码器符号检测，空间光通信场景
- **与声称是否一致**：**年份不符**（2023≠2024），**期刊待确认**（声称 IEEE TMLCN 但搜索未显示具体 venue）。核心内容一致。需进一步确认是否为 IEEE TMLCN 正式发表版本。

### Rustum 2026
- **是否找到**：是
- **实际标题**：Hybrid STA With FNN and CNN Models for Robust Channel Estimation in Turbulent FSO and Doppler-Affected LEO OFDM
- **作者**：Saad Rustum, Usman Habib, Salman Ahmed, M Ahmad, Muhammad Ijaz
- **期刊/年份**：IET Communications, 2026
- **引用数**：0（新发表）
- **DOI**：10.1049/cmu2.70148
- **核心内容确认**：STA+DL（FNN/CNN）两阶段信道估计，FSO+LEO OFDM
- **与声称是否一致**：**完全一致**

### Mohammed 2026
- **是否找到**：是
- **实际标题**：Free space optical turbulent channel estimation based on the deep combined CNN and BiLSTM
- **作者**：Nidhal Abd Mohammed, Morteza Valizadeh, MC Amirani
- **期刊/年份**：Journal of Optical Communications, 2026
- **引用数**：0（新发表）
- **DOI**：10.1515/joc-2026-0012
- **核心内容确认**：CNN+BiLSTM 混合架构，强湍流下鲁棒信道估计
- **与声称是否一致**：**完全一致**

### 曹明华 2020（中文）
- **是否找到**：否（项目工具未检索到）
- **说明**：中文学术论文在英文检索工具中覆盖率低，不代表不存在。需通过 CNKI 或学校数据库手动验证。

### 孙晶 2018（中文）
- **是否找到**：否（同上）
- **说明**：同曹明华情况。

## Ch3 论文验证结果

### Almogahed 2022
- **是否找到**：是
- **实际标题**：Performance improvement of mode division multiplexing free space optical communication systems using decision feedback equalizer
- **作者**：A Almogahed, A Amphawan, F Mohammed
- **期刊/年份**：2022, DOI: 10.1080/23311916.2022.2034268
- **引用数（实际）**：37（声称28，引用数随时间增长属正常）
- **核心内容确认**：MMSE-DFE 用于 MDM-FSO，多模均衡
- **与声称是否一致**：**一致**。另有 2020 年前作（29引）和 2022 Optical Engineering 版本（12引），均为 DFE+MDM-FSO 方向。

### Ahmad 2026
- **是否找到**：是
- **实际标题**：Robust high-capacity free-space optical communication using OAM-based structured light and intelligent adaptive signal processing
- **作者**：M Ahmad, Babar Hayat, Ming Fang, Chao Wang, Guoda Xie 等
- **期刊/年份**：Scientific Reports, 2026
- **引用数**：0
- **DOI**：10.1038/s41598-026-40704-2
- **核心内容确认**：OAM+DNFIS 均衡+DCNN-TCSGm 湍流补偿，BER 降 55%，10 dB 增益
- **与声称是否一致**：**完全一致**（摘要直接确认 BER 降低 55%）

### 佟欣 2020（中文）
- **是否找到**：否（项目工具未检索到）
- **说明**：中文期刊论文，需通过 CNKI 手动验证。

### Balakrishnan 2026
- **是否找到**：是
- **实际标题**：Reliable equalization aided long-distance OFDM-FSO performance analysis over Gamma-Gamma turbulence
- **作者**：R Balakrishnan, S Senthilkumar
- **期刊/年份**：2026
- **引用数**：0
- **核心内容确认**：GG 湍流模型下 OFDM-FSO 系统的 ZF 均衡性能分析
- **与声称是否一致**：**一致**

## 创新空白验证

### Ch2 空白：星地链路 DL 信道估计的系统性研究不足，传统 LS/MMSE/Kalman 在 GG 下对比缺失
- **搜索结果摘要**：检索"LS MMSE Kalman channel estimation comparison Gamma-Gamma FSO"返回 20 条结果，绝大多数为 DL 方法（CNN/BiLSTM/ELM）的单一论文，未发现将 LS、MMSE、Kalman 等传统方法在 GG 湍流模型下做系统性对比的研究。仅有个别论文涉及参数估计（moment-based estimation for GG fading parameters, 2025, 12引），但不涉及信道估计算法对比。
- **空白是否确认**：**是**。GG 模型下传统信道估计算法的系统性对比确实稀缺，DL 方法的改进也缺乏传统方法基线参照。

### Ch3 空白：GG 湍流+相干 PSK+多种均衡方法(CMA/MMSE/DFE/MLP)的系统性对比几乎找不到
- **搜索结果摘要**：检索"CMA MMSE DFE equalization comparison coherent FSO turbulence"返回 20 条结果，均为单一均衡方法（DFE/MMSE）在特定场景（MDM/OAM）的应用论文，未发现将 CMA、MMSE、DFE 等多种方法在同一 GG 湍流+相干 PSK 框架下进行系统性对比的研究。"equalization comparison coherent PSK atmospheric turbulence FSO"的结果同样如此。
- **空白是否确认**：**是**。GG 湍流下相干 PSK 系统的多均衡方法对比确实存在显著空白。

## 综合结论

### 1. 确认可用作基线的论文

| 论文 | 章节 | 状态 |
|------|------|------|
| Amirabadi 2019/2020 | Ch2 | 确认可用（注意年份标2020更准确） |
| Rustum 2026 | Ch2 | 确认可用 |
| Mohammed 2026 | Ch2 | 确认可用 |
| Almogahed 2022 | Ch3 | 确认可用 |
| Ahmad 2026 | Ch3 | 确认可用 |
| Balakrishnan 2026 | Ch3 | 确认可用 |

### 2. 需修正或待确认的论文

| 论文 | 问题 | 建议 |
|------|------|------|
| Elfiky 2024 | 年份实际为2023，期刊 IEEE TMLCN 未确认 | 核实是否为 TMLCN 发表版或会议/预印本版本 |
| 曹明华 2020 | 中文论文，工具未检索到 | CNKI 手动验证后使用 |
| 孙晶 2018 | 中文论文，工具未检索到 | CNKI 手动验证后使用 |
| 佟欣 2020 | 中文论文，工具未检索到 | CNKI 手动验证后使用 |

### 3. 创新空白验证结论

- **Ch2 空白确认**：GG 湍流下传统信道估计方法（LS/MMSE/Kalman）系统性对比缺失，空白真实
- **Ch3 空白确认**：GG+相干PSK+多均衡方法对比的研究空白真实，检索未发现任何系统性对比工作

### 4. 对开题报告写作的建议

1. **英文论文全部可直接引用**，引用信息以本次验证的实际数据为准（修正年份/引用数差异）
2. **Elfiky 论文需标注2023**，引用时查实期刊是否为 IEEE TMLCN
3. **中文论文**（曹明华、孙晶、佟欣）需在 CNKI 确认后补充引用信息，建议优先在知网检索
4. **创新空白叙述可信**：两个空白均经工具检索验证，可作为开题报告研究动机的核心论据
5. **引用数差异属正常**：Almogahed（28→37）和 Amirabadi（61→87）引用增长属时间推移正常现象，建议引用时使用检索时的实际数字
