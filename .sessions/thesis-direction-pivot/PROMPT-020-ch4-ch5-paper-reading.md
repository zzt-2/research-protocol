# 对话提示词：Ch4+Ch5 核心论文下载精读 + 参数提取

> 产出文件: 结论写入 `.sessions/thesis-direction-pivot/S007-ch4-ch5-deep-review.md`
> 优先级: 高
> 依赖: S005 框架审查结果
> 预计耗时: 45-60分钟

## 背景

硕士论文"星地激光通信信号处理关键技术研究"。框架审查发现：
- **Ch4致命信号候选**：VV/BPS在QPSK下增益<1dB，传统方法可能已达≥95%最优
- **但Ch4方案是FOE+CPR联合**（重点是LEO多普勒频偏估计），FOE创新空间可能独立于CPR天花板
- 需要精读验证：FOE部分的创新空间是否真实存在

**当前方案**：
- Ch4: 联合FOE+CPR — LEO载波同步 (SP-QPSK)
  - 方法：粗FOE(FFT-based) + 精CPR(VV/BPS)
  - 创新点：湍流自适应两阶段参数优化
- Ch5: 多普勒+湍流联合FPGA验证 (半章)
  - 接收端DSP链：Gardner定时+FOE+CPR

**框架审查关键风险项**（本对话需解决）：
1. Ch4 A0致命信号：VV/BPS在QPSK下增益是否真的<1dB？来源是哪篇文献？
2. FOE创新空间：LEO多普勒补偿的文献基础是否足够？有多少改进空间？
3. 联合优化的合理性：FOE和CPR分开做 vs 联合优化，差距有多大？

## 必须下载并精读的论文

### Ch4 载波同步（5篇）

| # | 论文 | DOI/查找信息 | 精读重点 |
|---|------|-------------|---------|
| 1 | **Liu 2023, "Carrier recovery for satellite-to-ground coherent laser comms"** | DOI: 10.1016/j.optcom.2023.129312 | **核心对照论文！** 提取：VV/BPS具体差距dB数、湍流条件、是否测了FOE |
| 2 | Yan 2026, "Doppler estimation satellite coherent optical" | 需搜索 `tools/search --query "Yan Doppler estimation compensation coherent optical satellite 2026"` | 最新多普勒方案，提取：Doppler范围、补偿精度、残留频偏 |
| 3 | Zhao 2025, "Joint Doppler phase noise compensation inter-satellite" | 需搜索 `tools/search --query "Zhao joint Doppler phase noise compensation inter-satellite coherent laser 2025"` | 联合补偿先例，提取：联合 vs 分离处理的差距 |
| 4 | 管海军 2019, "QPSK FSO相位恢复" | CNKI搜索 `tools/search --source cnki --query "QPSK 自由空间 相干光通信 数字相位恢复"` | QPSK FSO直接参考，提取：QPSK下VV性能数据 |
| 5 | **Paillier 2020, "Space-Ground coherent optical links with adaptive optics"** | 需搜索 `tools/search --query "Paillier space ground coherent optical links adaptive optics performance 2020"` | 系统级参考，提取：湍流对相干接收影响的定量数据 |

### Ch5 FPGA验证（5篇）

| # | 论文 | DOI/查找信息 | 精读重点 |
|---|------|-------------|---------|
| 1 | FPGA AFC多普勒补偿 2024 (Optics Letters) | 需搜索 `tools/search --query "real-time FPGA Doppler frequency shift compensation DSP-assisted AFC optical 2024"` | 多普勒FPGA核心，提取：AFC架构、资源利用率、频偏补偿范围 |
| 2 | FPGA LEO Doppler tracking 2025 (ACP) | 需搜索 `tools/search --query "real-time Doppler shift tracking LEO satellite ground links FPGA 2025"` | LEO实时跟踪，提取：跟踪精度、硬件平台、延迟 |
| 3 | FPGA SP-16QAM全链路 2022 (OE) | 需搜索 `tools/search --query "real-time FPGA 15GBaud SP-16QAM coherent receiver clock recovery equalization 2022"` | 单FPGA全链路参考，提取：资源表、模块划分、时钟频率 |
| 4 | **星地DSP综述 2025** | 需搜索 `tools/search --query "review analysis digital signal processing coherent optical satellite links 2025"` | **写作必备综述！** 提取：DSP链完整框图、各模块复杂度对比 |
| 5 | FPGA FSO湍流分集合并 2023 (OE) | 需搜索 `tools/search --query "real-time low-complexity diversity combining free space coherent optical turbulence FPGA 2023"` | 湍流FPGA处理，提取：湍流场景FPGA实现要点 |

## 操作步骤

### Step 1: 查找DOI

对没有DOI的论文，用 `tools/search` 搜索：
```bash
cd /mnt/d/code/study/research-protocol
bash tools/search --query "论文标题关键词" --max 5 --source s2
```

### Step 2: 下载论文

```bash
bash tools/download --doi "DOI"
bash tools/download --arxiv "arxiv_id"
```

### Step 3: 转换PDF

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
- 场景：FSO/光纤？星地/星间？调制格式？符号率？

### 关键结果
- 核心性能数据
- 对比方法列表及各自性能
- 具体dB数（CPR增益、FOE精度等）

### Ch4致命信号验证（核心！）
- VV/BPS在QPSK下增益是多少dB？来源是这篇吗？
- FOE在LEO场景的残留频偏是多少？
- 联合FOE+CPR vs 分离处理的差距？

### 参数提取
- LEO轨道高度 → 多普勒频移范围
- 激光器线宽 → 相位噪声参数
- VV窗口大小 / BPS测试相位数
- FPGA资源：LUT/FF/BRAM/DSP
- 时钟频率、符号率

### 与我们工作的关系
- 直接可参考的部分
- Ch4创新点是否成立？（FOE+CPR联合优化是否真有空间）
- 需要差异化避开的结论
```

### Step 5: 汇总（最重要的产出）

读完所有论文后，**必须回答以下问题**：

1. **Ch4致命信号判定**：
   - VV/BPS在QPSK下增益<1dB这个结论来自哪篇文献？是光纤还是FSO场景？
   - 在FSO湍流场景下，VV/BPS差距是否变大？
   - **如果CPR增益确实<1dB，FOE部分的创新空间是否足够撑起整章？**

2. **FOE创新空间评估**：
   - LEO多普勒频偏范围（GHz级？具体数值？）
   - 现有FOE方法的残留频偏是多少？
   - 湍流对FOE精度的影响？（这是我们的创新切入点）
   - 联合优化（FOE参数+CPR窗口同时调整）是否有文献做过？

3. **参数溯源表**：
   - LEO多普勒参数（轨道高度、载波频率、最大频偏）
   - VV窗口大小推荐值
   - 激光器线宽典型值

4. **FPGA可行性确认**：
   - 完整DSP链的资源估算
   - 各模块FPGA先例的具体参数

## 约束

- 必须用 `tools/search` 和 `tools/download`，禁止 WebSearch
- 中文输出
- **如果45分钟内做不完，优先顺序**：
  1. Liu 2023（Ch4核心对照，致命信号验证）
  2. 星地DSP综述 2025（Ch5写作必备）
  3. Zhao 2025（联合补偿先例）
  4. FPGA AFC 2024（多普勒FPGA核心）
  5. 其余
- 下载失败的论文不阻塞，记录后跳过
- Ch4致命信号的判定必须基于精读的论文内容，不能靠推理
