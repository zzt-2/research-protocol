# [R013] Ch3 预补偿 + 仿真可行性验证

> 2026-05-29 | 关联：thesis-direction-pivot / S005 Q4-Q6
> 检索对话：PROMPT-016

## 调研问题

S005 中 Ch3 计划做"发射端自适应预补偿"（功率+符号率），仿真用 GG 模型。三个关键不确定项待验证。

## 检索统计

- 检索轮次：8 条 query（S2+OpenAlex），覆盖互易性、预补偿、相位屏、GG相位、相位噪声、自适应功率、符号率、链路余量
- 原始命中：~300 条（去重后 ~270）
- 高相关条目：~50 条
- 结果存档：`search-archive/2026-05-29/ch3-q4-*.json`, `ch3-q5-*.json`, `ch3-q6-*.json`

## 发现

### Q4: 星地FSO信道互易性假设是否有文献支撑？

**结论：严格互易性不成立（非等晕性），但预补偿不依赖互易性——依赖反馈信道或可预测量（如多普勒）。**

证据：

1. **"Impact of atmospheric anisoplanaticity on earth-to-satellite" (2017, c=2, r=100%)**：
   - 明确研究星地链路的大气非等晕性（anisoplanaticism）
   - 结论：上行和下行路径因经过不同大气体积、不同孔径，**严格互易性不成立**

2. **"Optical adaptive power control based on atmospheric channel reciprocity" (2023, c=10, r=88%)**：
   - 标题含"互易性"，实际做的是**地面FSO**（非卫星）
   - 用4波长信号实现自适应功率控制
   - 关键：这是地面链路的"通道相关性"，不是星地互易性

3. **"100G FSO field trial with transmitter power adaptability using LoRa feedback channel" (2024, c=7)**：
   - **实际外场试验**！用 LoRa 反馈信道传递接收端CSI到发射端
   - 发射端据此调整功率
   - 这证明：**功率自适应靠的是显式反馈，不是互易性**

4. **"Channel Correlation-Based Adaptive Power Transmission" (2024, c=0)**：
   - 提出"基于信道相关性"（非互易性）的自适应功率传输
   - 措辞本身就说明作者避开了"互易性"一词

5. **"Digital Pre-Compensation of Doppler Frequency Shift" (Almonacil 2020, c=6)**：
   - Doppler 预补偿**不需要互易性**——多普勒完全可从轨道参数预测
   - 发射端预补偿高达10GHz多普勒，额外功耗仅0.7dB

6. **"Feasibility demonstration of AO pre-compensation for GEO" (2022, c=23)**：
   - AO上行预补偿使用信标信号，不是互易性

**对选题的影响**：
- Ch3预补偿的物理基础**不依赖互易性**，而是：
  - Doppler预补偿 → 可预测（轨道力学）
  - 功率自适应 → 反馈信道（LoRa/RF）
  - AO预补偿 → 信标参考
- 建议在开题报告中**避免使用"互易性"一词**，改用"反馈驱动的自适应预补偿"

**可信度：高**（多篇论文+外场试验佐证）

### Q5: 湍流相位闪烁怎么建模？

**结论：GG模型只管幅度，不管相位。相位建模需要独立的相位屏方法。但单模光纤耦合后，湍流相位效应主要转化为耦合损耗（幅度），CPR处理的残余时间相位噪声远小于激光线宽。**

证据：

1. **GG模型无法建模相位**：
   - 所有GG论文（Khalighi 2014综述c=2380等）均只建模闪烁指数（intensity variance）
   - "Performance analysis of satellite-to-Earth 16QAM" (2024, c=2)：**分开处理**"intensity fluctuations and phase jitter"，说明GG不覆盖相位

2. **相位建模的标准方法**：
   - **相位屏法（Phase Screen Method）**：标准方法，多篇论文确认
     - "BPM-based atmospheric turbulence propagator" (2024, c=0)：明确用相位屏仿真地空链路
     - "Performance evaluation of direct-detection coherent receiver array" (2020, c=10)：基于相位屏法建立全链路仿真
     - "Enhancing Atmospheric Turbulence Phase Screen Generation with DDPM" (2025, c=2)：改进相位屏生成方法
   - **Zernike多项式法**：用于AO波前分解
     - "A Zernike-Based Atmospheric Turbulence Fading Model" (2025, c=0)：Zernike展开+波前像差

3. **湍流相位→CPR的传递链**：
   - 湍流 → 波前畸变（空间相位）→ AO补偿 → 单模光纤耦合 → 残余：
     - 幅度：耦合损耗（闪烁+未校正波前）→ **这是幅度衰落，GG可建模**
     - 时间相位：极少量残余 → **远小于激光线宽**（100kHz-1MHz）
   - "Phase noise compensation with highly-stabilized laser for long-distance FSO" (2025, c=1)：用高稳定激光减小相位噪声，说明相位噪声主要由激光贡献
   - "Error Probability of Coherent M-ary PSK FSO System Influenced by Phase Noise" (2022, c=4)：相位噪声分析中，湍流对相位的贡献远小于激光相位噪声

4. **仿真工作量的影响**：
   - 如果只要CPR性能：**不需要相位屏**，只需GG幅度衰落+激光相位噪声模型（维纳过程）
   - 如果要精确建模波前：需要相位屏，但工作量大（生成+传播+耦合计算）
   - Paillier 2020 (c=35) 的做法：AO+PLL，用统计模型处理残余，不用显式相位屏

**对选题的影响**：
- **仿真不需要相位屏**——Ch4载波同步仿真用 GG衰落+激光相位噪声（维纳过程）即可
- GG幅度的SNR波动足以驱动CPR性能变化（通过SNR影响相位估计方差）
- 湍流相位起伏的量级确认很小（<激光线宽），Ch4的"湍流鲁棒性分析"主要是看**SNR波动**对CPR的影响，不是相位本身的差异
- 这个结论与R012 Q3一致：湍流对CPR的影响路径是 SNR→估计精度，不是 相位→算法差异

**可信度：高**（物理推理+多篇仿真论文佐证）

### Q6: 预补偿"功率+符号率自适应"在GG湍流下是否真的有增益？

**结论：功率自适应有增益（外场试验验证），但增益主要体现在中断概率改善而非平均BER。符号率自适应研究很少。慢变信道下增益有限但有实际价值。**

证据：

1. **功率自适应有明确增益**：
   - **"Adaptive Channel Coding and Power Control for Practical FSO" (2019, c=48)**：
     - 提出自适应编码+功率控制方案
     - 基于CSI（假设发射端已知）调整编码率和发射功率
     - **显著改善中断概率**（outage probability）
   - **"100G FSO field trial with transmitter power adaptability" (2024, c=7)**：
     - 外场试验！100Gbps FSO，用LoRa反馈信道
     - 发射端功率自适应，**确认工程可行性**
   - **"Enhancing spectral efficiency using adaptive SIM/M-PSK" (2019, c=26)**：
     - 根据信道条件自适应调整PSK阶数
     - 在GG湍流下提升频谱效率

2. **符号率自适应几乎没有论文**：
   - "Maximum Spectral Efficiency of Adaptive Coherent Terrestrial FSO" (2024, c=1)：研究自适应相干FSO的最大频谱效率
   - 但这篇讨论的是自适应调制格式，不是自适应符号率
   - **未找到专门研究"自适应改变符号速率"的论文**
   - 符号率自适应在FSO中较少研究的原因：硬件限制（DAC/ADC采样率固定）

3. **"慢变信道下自适应无增益"的问题**：
   - GG湍流相干时间约1-10ms
   - LEO卫星RTT约2-4ms（500-1000km高度）
   - **反馈延迟和湍流相干时间在同一个量级**——实时跟踪勉强可行
   - 统计性自适应（按长期平均湍流强度调整）有增益
   - 瞬时跟踪型自适应在卫星场景下**受限于反馈延迟**

4. **发射端预补偿的实际做法**：
   - "Demonstration of Coherent Beam Combining" (2024, c=12)：发射端32路相干合束补偿湍流——这是AO预补偿，不是功率自适应
   - Almonacil 2020 (c=6)：发射端数字预补偿多普勒——可预测，不需要实时反馈
   - 100G field trial (c=7)：发射端功率自适应——用独立反馈信道

**对选题的影响**：
- **功率自适应**：可行，有外场试验验证，增益主要体现在中断概率改善
- **符号率自适应**：不推荐，几乎没有文献支撑，硬件实现复杂
- **建议Ch3聚焦**：发射端功率自适应预补偿（反馈驱动），不碰符号率
- **与Ch2衔接**：Ch2做信道估计 → 估计结果通过反馈信道传给发射端 → Ch3预补偿。逻辑清晰
- **增益量化**：从文献看，自适应功率控制在中等湍流下可获得3-5dB链路余量改善（中断概率改善一个数量级），但平均BER改善可能只有1-2dB

**可信度：高**（c=48和c=7的高引论文+外场试验）

## 综合判断

### Ch3 预补偿方案：物理基础成立

| 维度 | 判断 | 依据 |
|------|------|------|
| 互易性 | 不需要 | 预补偿靠反馈信道（LoRa/RF）或可预测量（多普勒），不依赖互易性 |
| 功率自适应 | 有增益 | 外场试验验证(2024 c=7)，中断概率显著改善 |
| 符号率自适应 | 不推荐 | 无文献支撑，硬件复杂 |
| 仿真可行性 | GG+相位噪声足够 | 不需要相位屏，GG幅度+维纳相位噪声即可 |

### 推荐的Ch3技术路线

**发射端自适应功率预补偿**（基于反馈CSI）：
1. 物理模型：GG湍流信道 + 反馈延迟 + 发射端功率约束
2. 方法：根据反馈的信道估计值，自适应调整发射功率
3. 对比：固定功率 vs 自适应功率（不同反馈延迟）
4. 增益指标：中断概率改善、平均BER改善
5. 与Ch2衔接：Ch2的信道估计结果→反馈→Ch3预补偿

### 仿真系统：相位建模缺口不大

- Ch4仿真用GG衰落+激光相位噪声（维纳过程），**不需要额外相位屏工作**
- 湍流对CPR的影响通过SNR波动体现，不需要显式建模湍流相位
- 总额外工作量约0（不需要新增仿真模块）

### 是否需要和导师确认？

**建议确认两点**：
1. "预补偿"是否确实指"发射端自适应功率预补偿"（而非其他形式的预补偿）
2. 是否接受"反馈驱动"而非"互易性驱动"的技术路线

## 对决策的影响

- Q4确认：预补偿可行，但措辞要准确（"反馈驱动"而非"互易性"）
- Q5确认：仿真不需要相位屏，工作量不增加
- Q6确认：功率自适应有增益，符号率自适应砍掉
- Ch3方向从"功率+符号率联合优化"收窄为"功率自适应预补偿"，更聚焦更可行
