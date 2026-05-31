# [R001] Ch2 大气湍流信道建模与估计 — 可行性深研

> 2026-05-29 | 关联：thesis-direction-pivot

## 调研问题

Ch2"大气湍流信道建模与估计"作为硕士论文一章是否可行？具体技术路线、仿真方案和坑点是什么？

## 发现

### 一、信道模型对比

| 模型 | 适用 σ²_R 范围 | 参数数 | 核心优势 | 核心局限 |
|---|---|---|---|---|
| Lognormal | < 1（弱湍流） | 1 | 形式最简 | 强湍流尾部失真 |
| **Gamma-Gamma** | **全范围** | **2 (α, β)** | **事实标准，文献最丰富** | **不含指向误差** |
| 负指数 | >> 1（强极限） | 1 | K分布退化 | 仅强湍流 |
| **Exponentiated Weibull** | 全范围 | 3 | **含指向误差时更准确** | 参数略多 |
| Málaga (M) | 全范围 | 多 | 理论统一框架 | 参数过多，非主流 |

**推荐**：GG 为主线（标准、简单、文献多），EW 或 GG+pointing error 作为扩展场景。Málaga 不建议（硕士论文不需如此复杂的统一框架）。

GG 模型基于修正 Rytov 理论，接收光强 I = X × Y，X~Gamma(α,1/α)，Y~Gamma(β,1/β)。α、β 分别代表大/小尺度涡旋有效数量（Andrews & Phillips, 2005）。

### 二、信道估计方法对比

| 方法 | 所需先验 | 复杂度 | 性能特点 |
|---|---|---|---|
| **LS** | 仅导频结构 | O(N) | 低SNR恶化严重，高SNR≈MMSE |
| **MMSE** | 信道协方差矩阵 R_h + 噪声方差 σ²_n | O(N²) | 比LS好3-5 dB NMSE，但统计失配时崩溃 |
| **Kalman** | 状态转移矩阵 A（依赖相干时间） | O(N) | 适合时变信道（LEO），强湍流下被DL超越（Nature Sci. Rep., 2025） |
| **ML估计** | 参数化模型 | O(N) | 可达CRB，但需已知模型阶数 |
| **DL (DNN/LSTM)** | 训练数据 | 推理O(1) | 不需先验，强湍流/低SNR增益3-8 dB |

**关键结论**：传统方法在"统计模型已知 + 湍流较弱 + SNR 充分"条件下够用。DL 增益集中在**强湍流、低SNR、统计失配、时变剧烈**四个交叉场景。

### 三、星地链路特有挑战

1. **多普勒频移**：LEO 卫星相对地面站约 7.5 km/s，1550nm 光载波产生约 7-8 GHz 频移（ScienceDirect, 2024）
2. **分层湍流**：Cn² 随高度变化 3 个量级（地面 10⁻¹⁵~10⁻¹³ → 高空 10⁻¹⁷~10⁻¹⁶），**必须用 HV 模型沿路径积分**，单值 Cn² 仅适用于地面水平链路
3. **相干时间**：地面 FSO 典型 0.1-10 ms（Khalighi 综述, 2014），LEO 场景可降至亚毫秒
4. **CSI 反馈延迟**：LEO RTT 约 2-4 ms，与相干时间同量级 → 预均衡需谨慎，后均衡更适合下行
5. **上行 vs 下行不对称**：上行光束先穿越强湍流区再扩束，影响远大于下行

### 四、开源仿真资源

> 注：API 过载未实时搜索，基于已知信息整理。[推断]

| 资源 | 语言 | 功能 | 可用性 |
|---|---|---|---|
| MATLAB Communications Toolbox | MATLAB | 内置 AWGN/衰落信道 | ⭐⭐⭐ 但无GG模型 |
| GitHub "fso-simulation" 类仓库 | MATLAB/Python | GG信道+OOK/BPSK BER | ⭐⭐ 代码质量参差 |
| 用户本科毕设代码 | MATLAB | 调制解调仿真框架 | ⭐⭐⭐ 直接复用价值最高 |

**建议**：
- **优先复用本科毕设 MATLAB 代码**（调制解调框架已有）
- GG 信道模型用乘积法自行实现（几行代码），不依赖外部库
- DL 部分用 Python/PyTorch（已有 RTX 4070 环境）
- MATLAB 做传统方法仿真，Python 做 DL 对比

### 五、技术坑点清单

| 坑 | 严重程度 | 应对 |
|---|---|---|
| GG PDF 的 Bessel 函数溢出 | 高 | **不用 PDF 计算，用乘积法生成**：X~Gamma(α,1/α), Y~Gamma(β,1/β)，numpy.random.gamma 直接调 |
| 星地 Cn² 不能用地面值 | 高 | 用 HV 模型沿路径积分，或直接引用文献中星地 σ²_R 典型值 |
| APD 噪声是信号相关的 | 中 | 先用 AWGN 简化跑通，再加 APD 模型 |
| OOK 判决阈值不在中点 | 中 | APD 下最优阈值需数值求解，不能简单取 0.5×幅度 |
| GG 模型均值不一定为 1 | 低 | α<2 或 β<2 时需归一化 E[I]=1 |
| 背景辐射（日光）噪声 | 低 | 白天场景不可忽略，但可先做夜间场景 |

### 六、最小可行仿真方案（2-3天）

| 组件 | 建议 |
|---|---|
| **信道模型** | GG，三种湍流强度：弱(α=4,β=4)、中(α=2.5,β=2)、强(α=1.5,β=1) |
| **调制格式** | OOK（IM/DD，最简单，与本科毕设衔接） |
| **估计方法** | ① LS（导频估计）② MMSE（需信道协方差）③ 简单 DNN（2层FC，输入接收序列，输出信道增益） |
| **SNR 范围** | 0~30 dB，步进 2 dB |
| **符号数** | 10⁶ symbols/次（BER 可估到 10⁻⁵） |
| **蒙特卡洛** | 10³ 独立信道实现取平均 |
| **指标** | BER vs SNR + NMSE vs SNR |
| **预期图表** | 1 张 BER-SNR 主图（3湍流×3方法=9线）+ 1 张 NMSE-SNR 图 |

**工期估算**：Day 1 GG 信道模型+OOK 系统（4h），Day 2 LS/MMSE 估计（4h），Day 3 DNN 对比（6h）。

## 结论

### Go/No-Go：**GO，置信度 4/5**

**理由**：
1. GG 信道模型成熟，乘积法生成避开了数值稳定性问题
2. OOK+AWGN+GG 仿真链 2 天可跑通，第 3 天加 DL
3. 信道估计对比（LS vs MMSE vs DNN）是成熟的论文范式
4. 与本科毕设（调制解调）直接衔接，学习曲线平缓

**风险等级：中**

| 风险 | 概率 | 应对 |
|---|---|---|
| DL 在高SNR无增益 | 高 | 设计强湍流+低SNR场景展示DL优势 |
| APD 噪声模型增加复杂度 | 中 | 先用 AWGN 跑通再加 |
| 星地参数选取不当 | 中 | 直接引用 Khalighi 综述/Andrews 教材典型值 |
| 与本科毕设区分度不够 | 低 | 明确场景差异（星地 vs 地面，湍流建模 vs 调制解调） |

### 对决策的影响

- D006 建议：Ch2 确认为 Go，仿真方案建议先 OOK+AWGN+GG 跑通 baseline，再逐步添加真实噪声源
- 预均衡（Ch3）的 CSI 来自 Ch2 估计结果 → Ch2 必须输出时变信道增益序列，不能只做静态 BER 曲线
- 相干时间 0.1-10 ms 意味着 block fading 模型合理，一个块内信道近似恒定

## 参考文献

1. Andrews, L.C. & Phillips, R.L., *Laser Beam Propagation through Random Media*, 2nd ed., SPIE, 2005.
2. Barrios, R. & Dios, F., "Exponentiated Weibull distribution family under aperture averaging," *Optics Express*, 21(3), 2013.
3. Yang, L. et al., "Generic evaluation of FSO system over Malaga turbulence channel," *IET Communications*, 2020.
4. Khalighi, M.A. & Uysal, M., "Survey on Free Space Optical Communication: A Communication Theory Perspective," *IEEE Communications Surveys & Tutorials*, 16(4), 2014.
5. Li, B. et al., "Free space optical channel estimation based on deep learning," *IEEE ICC Workshops*, 2023.
6. Elamassie, M. et al., "A sparse wavelength aware learning framework for robust FSO channel estimation," *Scientific Reports*, Nature, 2025.
7. Zheng, X. et al., "A statistical evaluation of coherence time for non-terrestrial communications," *arXiv:2405.07005*, 2024.
8. IOP Science, "Analysis of LSE and MMSE pilot based channel estimation," *IOP Conf. Series*, 1084, 2021.
9. Singh, M. et al., "BER and channel capacity performance of an FSO communication system," *Sensors*, 21(10), 2021.
10. Ansari, I.S. et al., "Performance analysis of FSO links over Malaga turbulence channels with pointing errors," *IEEE Trans. Vehicular Technology*, 2016.
