# 对话提示词：Ch2+Ch3 核心论文下载精读 + 参数提取

> 产出文件: 结论写入 `.sessions/thesis-direction-pivot/S006-ch2-ch3-deep-review.md`
> 优先级: 高
> 依赖: S005 框架审查结果
> 预计耗时: 45-60分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。框架审查发现"零全文精读"和"参数溯源零"两个高风险遗漏。本对话负责 Ch2+Ch3 的核心论文下载和精读。

**当前方案**：
- Ch2: GG大气湍流信道建模 + LS/MMSE/DL信道估计 (SP-QPSK, 相干检测)
- Ch3: 反馈驱动功率自适应预补偿 (SP-QPSK, 反馈信道驱动)

**框架审查最高风险项**（本对话需部分解决）：
1. A0问题-方法适配性：DL vs 传统方法差距是否≥5%？
2. 参数溯源：GG模型三档参数(弱/中/强湍流α,β)是否有文献依据？
3. 增强基线(FR-03)：如果传统方法加合理特征工程，DL还有优势吗？

## 必须下载并精读的论文

### Ch2 信道估计（5篇）

| # | 论文 | DOI/查找信息 | 精读重点 |
|---|------|-------------|---------|
| 1 | Amirabadi 2019, "Deep Learning for channel estimation in FSO" | 需搜索 `tools/search --query "Amirabadi deep learning channel estimation free space optical"` | DL在GG信道估计的标杆，提取：DL架构、输入特征、训练数据量、与MMSE差距 |
| 2 | Rustum 2026, "Hybrid STA with FNN/CNN for robust CE" | DOI: 10.1049/cmu2.70148 | 最新LEO-OFDM方案，提取：STA原理、DL输入、LEO场景参数 |
| 3 | Mohammed 2026, "CNN+BiLSTM CE" | DOI: 10.1515/joc-2026-0012 | CNN+BiLSTM组合，提取：网络结构、湍流参数范围 |
| 4 | 曹明华 2020, "GG+FTN" | CNKI搜索，需用 `tools/search --source cnki` | GG模型中文高引，提取：GG三档参数(α,β)、Cn²范围、仿真参数表 |
| 5 | 孙晶 2018, "相干+GG分集" | CNKI搜索 | 相干检测+GG，提取：相干检测系统参数、BER曲线基准 |

### Ch3 预补偿（5篇）

| # | 论文 | DOI/查找信息 | 精读重点 |
|---|------|-------------|---------|
| 1 | Almogahed 2022, "MMSE-DFE in MDM-FSO" | DOI: 10.1080/23311916.2022.2034268 | DFE在FSO标杆，提取：DFE结构、抽头数、收敛条件 |
| 2 | Ahmad 2026, "DNFIS+DCNN均衡" | DOI: 10.1038/s41598-026-40704-2 | 最新DL均衡，提取：BER改善幅度、对比方法列表 |
| 3 | 佟欣 2020, "CMA-LMS空间激光" | CNKI搜索 | CMA在空间激光，提取：CMA收敛参数、步长选择 |
| 4 | **100G field trial LoRa feedback 2024** | 需搜索 `tools/search --query "100G FSO field trial LoRa feedback power adaptability"` | **外场试验！**提取：功率自适应方案、LoRa反馈延迟、实际BER改善 |
| 5 | Safi 2019, "Adaptive Power FSO" | 需搜索 `tools/search --query "Safi adaptive channel coding power control FSO"` | 自适应功率理论，提取：中断概率改善、功率约束模型、GG参数 |

## 操作步骤

### Step 1: 查找DOI（有DOI的跳过）

对没有DOI的论文，用 `tools/search` 搜索获取DOI或arxiv ID：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "论文标题关键词" --max 5 --source s2
```

### Step 2: 下载论文

```bash
bash tools/download --doi "DOI"           # DOI论文
bash tools/download --arxiv "arxiv_id"    # arXiv论文
```

中文论文如果无法自动下载，记录"需手动下载"并列出CNKI链接。

### Step 3: 转换PDF（如需要）

```bash
bash tools/convert papers/doi/路径/source.pdf
```

### Step 4: 精读每篇论文

读 content.md，提取以下信息：

```
## [论文名]

### 基本信息
- 问题：论文解决什么问题？
- 方法：用什么方法？
- 场景：FSO/光纤/其他？星地/星间/地面？调制格式？

### 关键结果
- 核心性能数据（BER改善、NMSE等）
- 对比方法列表及各自性能
- DL vs 传统方法差距（如果涉及）

### 参数提取（用于我们的仿真）
- GG模型参数：α, β, Cn², 链路距离
- 调制格式：符号率、波长
- SNR范围
- 仿真符号数

### 与我们工作的关系
- 直接可参考的部分
- 需要差异化避开的结论
- A0适配性判断：传统方法离理论上界差多少？DL能否补这个差？
```

### Step 5: 汇总

读完所有论文后，产出汇总：

1. **参数溯源表**：列出从文献提取的GG三档参数(α,β,Cn²)，标注来源
2. **A0初步评估**：
   - Ch2: LS/MMSE vs DL差距是多少dB？是否≥5%？
   - Ch3: 固定功率 vs 自适应功率差距是多少？
3. **增强基线预判**：如果传统方法加合理优化（如robust MMSE），DL还有多大优势？
4. **空白零假设初步**：为什么前人没做我们打算做的事？（3条原因+反驳）

## 约束

- 必须用 `tools/search` 和 `tools/download`，禁止 WebSearch
- 中文输出
- 如果45分钟内做不完全部10篇，优先完成 Ch3 #4(外场试验) 和 Ch2 #1(Amirabadi) + #4(曹明华参数)
- 每篇精读控制在10分钟内
- 下载失败的论文不阻塞，记录后跳过
