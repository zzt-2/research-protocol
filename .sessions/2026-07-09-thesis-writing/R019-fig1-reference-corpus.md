# [R019] Fig.1 架构图候选语料与类型预筛

> 2026-07-13 | 关联：2026-07-09-thesis-writing / D010 / S012
> 状态：三轮补样完成；前两轮 81 个已核验图位 + 1 个备用，第三轮新增 15 个全部可见的视觉语法候选，已完成主线程分级与视觉 Gate
> 呈现：候选全部采用纵向卡片，不使用横向表格；前两轮 60/82 张已生成本地 PNG，22 张明确标注预览暂缺。第三轮另增 15 张“设计感优先”候选，15/15 均有本地 PNG。

## 调研问题

是否已经找到足以支撑 Fig.1 后续信息架构研究的论文图型？哪些图值得进入深度分析，哪些只能借局部语法，哪些基本不对路？

## 判定口径

- **A — 强匹配**：至少覆盖目标 Fig.1 的两项核心关系，如主数据旁路、双候选分支、测量/阈值控制、selector 合流、端到端与局部拆图。
- **B — 局部可迁移**：只能迁移一种结构或视觉语法，具体系统关系不能照搬。
- **C — 基本不对路**：选择发生在发射端或跨帧反馈、主要展示硬件/性能时间条，或没有可迁移的数据流与控制流；不进入深度样本。
- Gate 记号：`S` 语义可迁移，`K` 结构可迁移，`V` 视觉层级可迁移，`E` 来源可核验。

目标 Fig.1 当前冻结的真实关系：接收信号保持连续主数据路径并进入 phase compensation；同一信号另行送入 DA/NDA 两个相位估计支路；块有效 SNR/质量量经固定阈值形成控制线；selector 选择相位估计量，不切断业务数据。

## 第一轮去重与 Gate A

- A1 13 张、A2 14 张、A3 14 张，共 41 张图、33 篇论文。
- 按“论文 + 图号”去重后仍为 41 张。Li et al. 2022 同时出现 Fig.1 与 Fig.8，承担不同结构作用，保留为两张。
- 主线程分级：A 13 张、B 21 张、C 7 张。
- 从 A/B 中保留的深度候选可满足：T1 系统总览 8 张、T2 DSP 管线 16 张、T3 自适应控制 16 张、T4 多尺度拆图 9 张；Gate A 数量与类型覆盖均通过。

## 在线预览墙

以下为有直接公开图源的代表样本；其余候选在后文提供图页或 PDF 精确页码。

### FSO 接收机与端到端层级

[Li et al. 2019 Fig.1 原图](https://www.mdpi.com/applsci/applsci-09-00836/article_deploy/html/images/applsci-09-00836-g001.png)

![Li et al. 2019 Fig.1](https://www.mdpi.com/applsci/applsci-09-00836/article_deploy/html/images/applsci-09-00836-g001.png)

[Li et al. 2021 Fig.1 原图](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g001.png)

![Li et al. 2021 Fig.1](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g001.png)

### 质量量驱动算法切换

[Li et al. 2021 Fig.4 原图](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g004.png)

![Li et al. 2021 Fig.4](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g004.png)

### CPR 内部层级与拆图

[Peng et al. 2024 Fig.2 原图](https://www.frontiersin.org/files/Articles/1452087/xml-images/fphy-12-1452087-g002.webp)

![Peng et al. 2024 Fig.2](https://www.frontiersin.org/files/Articles/1452087/xml-images/fphy-12-1452087-g002.webp)

### 同一输入进入两种接收算法并作选择

[Lee and Sim 2025 Fig.2 原图](https://mdpi-res.com/electronics/electronics-14-00335/article_deploy/html/images/electronics-14-00335-g002-550.jpg)

![Lee and Sim 2025 Fig.2](https://mdpi-res.com/electronics/electronics-14-00335/article_deploy/html/images/electronics-14-00335-g002-550.jpg)

## A — 强匹配，优先看（13 张）

### A1-03

- **来源与定位**：[Li et al., 2021, *Applied Sciences*](https://www.mdpi.com/2076-3417/11/6/2543), Fig.1，[原图](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g001.png)
- **类型**：T1/T2
- **可迁移点**：Tx→FSO/湍流信道→Rx→DSP 的横向总览最贴近当前系统
- **不适用 / 降级理由**：光学器件偏多，CPR 内部未展开
- **Gate**：S/K/V/E



![A1-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-03.png)

### A1-04

- **来源与定位**：同上 Fig.4，[原图](https://www.mdpi.com/applsci/applsci-11-02543/article_deploy/html/images/applsci-11-02543-g004.png)
- **类型**：T3
- **可迁移点**：Q 值评估后在两算法间切换，是“测量→判据→分支”的同域实例
- **不适用 / 降级理由**：是流程图，没有主数据旁路
- **Gate**：S/K/V/E



![A1-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-04.png)

### A1-07

- **来源与定位**：[Baeuerle et al., 2016, *Optics Express*](https://pdfs.semanticscholar.org/7831/1843d137c7264bded0e9b0993d3f3c26f70e.pdf), Fig.1，PDF p.5
- **类型**：T2/T3/T4
- **可迁移点**：总 CPR 流程与内部并行选择拆开表达
- **不适用 / 降级理由**：星座 inset 和公式偏多
- **Gate**：S/K/V/E


![A1-07 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-07.png)

### A1-08

- **来源与定位**：[Baeuerle et al., 2016, *Optics Express*](https://pdfs.semanticscholar.org/7831/1843d137c7264bded0e9b0993d3f3c26f70e.pdf), Fig.5，PDF p.8
- **类型**：T2/T3
- **可迁移点**：同一输入复制到并行候选，经 cost 与 selector 后进入补偿
- **不适用 / 降级理由**：候选是测试相位，不是 DA/NDA 异构估计器
- **Gate**：S/K/V/E


![A1-08 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-08.png)

### A1-12

- **来源与定位**：[Li et al., 2022, *IEEE Access*](https://www.researchgate.net/figure/a-The-setup-of-the-coherent-FSOC-system-b-Block-repeating-and-coherent-combining_fig1_362282434), Fig.1
- **类型**：T1/T2/T4
- **可迁移点**：FSOC setup、关键概念、DSP flow 三层并列
- **不适用 / 降级理由**：同图密度较高，具体 combining 模块不可迁移
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A2-01

- **来源与定位**：[Liu et al., 2017, *Optics Express*](https://pdfs.semanticscholar.org/d7ac/59776b99cb080dd8d0b60d30fc284a1055b0.pdf), Fig.1，PDF p.2
- **类型**：T2/T3/T4
- **可迁移点**：监测块从主 DSP 链取信号，再以控制线重配置后级模块
- **不适用 / 降级理由**：控制箭头较多，控制对象不是两个估计器
- **Gate**：S/K/V/E


![A2-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-01.png)

### A2-03

- **来源与定位**：[Rezaei et al., 2025](https://arxiv.org/pdf/2505.18534), Fig.2(a–c)，PDF p.3
- **类型**：T1/T3/T4
- **可迁移点**：phase-error detector、select signal 与相位控制的角色分得很清楚
- **不适用 / 降级理由**：模拟闭环控制 LO，不是数字前馈补偿
- **Gate**：S/K/V/E


![A2-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-03.png)

### A2-10

- **来源与定位**：[Maria V. Ionescu, *Digital Signal Processing for Sensing in Software Defined Optical Networks*, UCL PhD thesis, 2015](https://discovery.ucl.ac.uk/1472246/)，Chapter 5, Fig.5.1，PDF/printed p.83；关联期刊图为 [Ionescu et al., *Optics Express* 23, 25762 (2015), Fig.1](https://doi.org/10.1364/OE.23.025762)
- **类型**：T2/T3
- **可迁移点**：上排主 DSP 数据链、下排联合监测支路，层次非常干净
- **不适用 / 降级理由**：监测结果没有回接 selector；本地预览直接来自 thesis Fig.5.1，与期刊 Fig.1 的功能结构对应，但尚未完成图像级同一性确认
- **Gate**：S/K/V/E


![A2-10 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-10.png)

### A2-11

- **来源与定位**：[Faruk et al., 2014, *IEEE Photonics Journal*](https://www.researchgate.net/figure/Schematic-of-the-coherent-optical-receiver-and-typical-DSP-blocks-for-data-recovery_fig2_260522694), Fig.2，论文约 p.3
- **类型**：T2/T3
- **可迁移点**：OSNR estimator 抽取信号但不截断主链，直接约束原始信号旁路画法
- **不适用 / 降级理由**：只有单估计支路
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A3-01

- **来源与定位**：[Lee and Sim, 2025, *Electronics*](https://www.mdpi.com/2079-9292/14/2/335), Fig.2，[原图](https://mdpi-res.com/electronics/electronics-14-00335/article_deploy/html/images/electronics-14-00335-g002-550.jpg)
- **类型**：T2/T3
- **可迁移点**：同一输入进入 ZF/ML 两路，特征判决控制 receiver selection
- **不适用 / 降级理由**：DNN 细节和判据不可迁移
- **Gate**：S/K/V/E



![A3-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-01.png)

### A3-02

- **来源与定位**：[Shahabuddin et al., 2014, IEEE CROWNCOM](https://biblio.ugent.be/publication/5332671), Fig.6，PDF p.4
- **类型**：T2/T3
- **可迁移点**：channel estimator→selection→LMMSE/SSFE 两算法，结构接近目标
- **不适用 / 降级理由**：固定阈值没有在图上展开
- **Gate**：S/K/V/E


![A3-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-02.png)

### A3-05

- **来源与定位**：[El-Yamany and Petri, 2018](https://www.ursi.org/proceedings/procAT18/papers/AnAdaptiveIEEE802.11adIndoormmWaveInnerReceiverArchitecture.pdf), Fig.2，PDF p.2
- **类型**：T2/T3
- **可迁移点**：SNR-range 控制量向多个 DSP 模块扇出，控制线语义清楚
- **不适用 / 降级理由**：没有两条完整数据路径与合流
- **Gate**：S/K/V/E


![A3-05 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-05.png)

### A3-06

- **来源与定位**：[Huang et al., 2000, *IEEE TVT*](https://ir.lib.nycu.edu.tw/bitstream/11536/30532/1/000087471700018.pdf), Fig.6，PDF p.7
- **类型**：T2/T3/T4
- **可迁移点**：coherent/noncoherent 两类解调路径与控制反馈并存
- **不适用 / 降级理由**：老式图较密，切换依据不是逐块 SNR
- **Gate**：S/K/V/E



![A3-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-06.png)

### A 组主线程判断

没有一张完整同构目标 Fig.1。最接近的组合是：A1-03 提供系统总览，A2-11 提供主数据旁路，A1-08/A3-01/A3-02 提供并行候选与 selector，A2-01/A3-05 提供测量量与控制线。后续深度分析应研究这些语法怎样组合，而不是选一张照抄。

## B — 只迁移局部语法（21 张）

### A1-01

- **来源与定位**：[Li et al., 2019](https://www.mdpi.com/2076-3417/9/5/836), Fig.1，[原图](https://www.mdpi.com/applsci/applsci-09-00836/article_deploy/html/images/applsci-09-00836-g001.png)
- **类型**：T1/T2
- **可迁移点**：物理接收机→ADC/DSP 层级
- **不适用 / 降级理由**：无 Tx、双估计器和控制线
- **Gate**：S/K/V/E



![A1-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-01.png)

### A1-02

- **来源与定位**：同上 Fig.2，[原图](https://www.mdpi.com/applsci/applsci-09-00836/article_deploy/html/images/applsci-09-00836-g002.png)
- **类型**：T2/T3
- **可迁移点**：状态估计与递归依赖
- **不适用 / 降级理由**：单估计器反馈
- **Gate**：S/K/V/E



![A1-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-02.png)

### A1-05

- **来源与定位**：[Peng et al., 2024](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2024.1452087/full), Fig.2，[原图](https://www.frontiersin.org/files/Articles/1452087/xml-images/fphy-12-1452087-g002.webp)
- **类型**：T2/T4
- **可迁移点**：CPR 外框与内部 zoom-in
- **不适用 / 降级理由**：coarse/fine 串联而非并行选择
- **Gate**：S/K/V/E



![A1-05 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-05.png)

### A1-06

- **来源与定位**：同上 Fig.4，[原图](https://www.frontiersin.org/files/Articles/1452087/xml-images/fphy-12-1452087-g004.webp)
- **类型**：T1/T2/T4
- **可迁移点**：完整实验链与末端 DSP
- **不适用 / 降级理由**：光纤实验器件压过 CPR
- **Gate**：S/K/V/E



![A1-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-06.png)

### A1-09

- **来源与定位**：[Navarro et al., 2016](https://pdfs.semanticscholar.org/2725/d5ee5c3cc1c1b175ccb22a8d8eee9955f7bc.pdf), Fig.2，PDF p.3
- **类型**：T2/T4
- **可迁移点**：大框分组和少量星座 inset
- **不适用 / 降级理由**：两级依赖、五个 inset 过载
- **Gate**：S/K/V/E


![A1-09 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-09.png)

### A1-10

- **来源与定位**：[Perin et al., 2018](https://web.stanford.edu/~jkperin/OFC_DSP_free_coherent.pdf), Fig.1，PDF p.1–2
- **类型**：T1/T2
- **可迁移点**：optical front-end 与 carrier recovery 分区克制
- **不适用 / 降级理由**：模拟、双偏振、DSP-free
- **Gate**：S/K/V/E


![A1-10 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-10.png)

### A1-11

- **来源与定位**：[Perin et al., 2018](https://web.stanford.edu/~jkperin/OFC_DSP_free_coherent.pdf), Fig.2，PDF p.2
- **类型**：T2/T3/T4
- **可迁移点**：总控路径与 estimator 局部拆图
- **不适用 / 降级理由**：PLL 反馈语义会误导当前前馈结构
- **Gate**：S/K/V/E


![A1-11 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-11.png)

### A1-13

- **来源与定位**：[Zhang et al., 2021, *Nature Photonics*](https://www.nature.com/articles/s41566-021-00877-w#Fig1), Fig.1(a,b)
- **类型**：T1/T2/T3/T4
- **可迁移点**：两种架构并列、pilot/reference 角色清楚
- **不适用 / 降级理由**：是架构对比，不是运行时选择
- **Gate**：S/K/V/E


![A1-13 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A1-13.png)

### A2-02

- **来源与定位**：[García and Hueda, 2021](https://arxiv.org/pdf/2110.04216), Fig.1(a,b)，PDF p.2
- **类型**：T2/T3/T4
- **可迁移点**：信号旁路、并行通道、局部/总览拆分
- **不适用 / 降级理由**：电路线与公式密度过高
- **Gate**：S/K/V/E


![A2-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-02.png)

### A2-04

- **来源与定位**：[Rezaei et al., 2025](https://arxiv.org/pdf/2505.18534), Fig.4(a,b)，PDF p.3
- **类型**：T3/T4
- **可迁移点**：完整闭环与化简模型并列
- **不适用 / 降级理由**：控制论小信号模型，非端到端系统
- **Gate**：S/K/V/E


![A2-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-04.png)

### A2-05

- **来源与定位**：[Júnior et al., 2022](https://www.researchgate.net/publication/361322884_Advanced_Digital_Signal_Processing_and_Variable-Rate_Coding_for_Unrepeatered_Optical_Transmission), Fig.1，PDF p.2
- **类型**：T2/T3
- **可迁移点**：多算法路径共享前后级并重新合流
- **不适用 / 降级理由**：表示离线方案组合，不是实时 selector
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A2-07

- **来源与定位**：[Uddin et al., 2025](https://www.mdpi.com/1424-8220/25/16/5010), Fig.1(a,b)
- **类型**：T2/T3/T4
- **可迁移点**：两接收支路经旋转、加权与求和合流
- **不适用 / 降级理由**：两天线数据分支，不是两估计器
- **Gate**：S/K/V/E


![A2-07 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-07.png)

### A2-08

- **来源与定位**：[Uddin et al., 2025](https://www.mdpi.com/1424-8220/25/16/5010), Fig.2(a–c)
- **类型**：T1/T2/T4
- **可迁移点**：总系统、Tx DSP、Rx DSP 分面
- **不适用 / 降级理由**：三面板硬件细节多，控制流弱
- **Gate**：K/V/E


![A2-08 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-08.png)

### A2-09

- **来源与定位**：[Delgado Mendinueta et al., 2018](https://www.mdpi.com/2076-3417/8/11/2182), Fig.1
- **类型**：T1/T2
- **可迁移点**：Tx→多模信道→Rx 的横向总览
- **不适用 / 降级理由**：六空间通道重复，无 selector
- **Gate**：S/K/V/E


![A2-09 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-09.png)

### A2-12

- **来源与定位**：[Li et al., 2022](https://www.researchgate.net/figure/a-Experimental-Setup-b-Flow-chart-of-the-DSP-chain_fig7_362282434), Fig.8(a,b)
- **类型**：T1/T2/T4
- **可迁移点**：实验系统与 DSP flow 分开
- **不适用 / 降级理由**：线性 DSP 链，没有控制流
- **Gate**：K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A2-13

- **来源与定位**：[Kim and Lee, 2012](https://link.springer.com/article/10.1186/1687-1499-2012-238), Fig.1
- **类型**：T1/T3
- **可迁移点**：双模式、selector、独立低速反馈
- **不适用 / 降级理由**：选择下一次 Tx 模式，不是当前块 Rx 估计
- **Gate**：S/K/V/E


![A2-13 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-13.png)

### A2-14

- **来源与定位**：[Manzoor et al., 2025](https://www.mdpi.com/1999-4893/18/2/97), Fig.1
- **类型**：T1/T2/T3
- **可迁移点**：SNR estimator→threshold/mode selection
- **不适用 / 降级理由**：自适应调制系统过大
- **Gate**：S/K/V/E


![A2-14 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-14.png)

### A3-03

- **来源与定位**：[Mangione et al., 2021](https://iris.unipa.it/retrieve/handle/10447/516012/1232286/A_Channel-Aware_Adaptive_Modem_for_Underwater_Acoustic_Communications.pdf), Fig.1，PDF p.4
- **类型**：T1/T3/T4
- **可迁移点**：探测/反馈与数据通路分层
- **不适用 / 降级理由**：水声双向 modem 远离本地 CPR
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A3-04

- **来源与定位**：[Barua et al., 2022](https://mdpi-res.com/d_attachment/sensors/sensors-22-03436/article_deploy/sensors-22-03436.pdf), Fig.2，PDF p.9
- **类型**：T1/T2/T3/T4
- **可迁移点**：SNR estimation→mode selector→feedback
- **不适用 / 降级理由**：selector 控制下一帧 Tx 调制
- **Gate**：S/K/V/E


![A3-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-04.png)

### A3-11

- **来源与定位**：[Pinto et al., 2003](https://citeseerx.ist.psu.edu/document?doi=16519b3f2a0c5d894d37fce185a0310ee6dcf2e3&repid=rep1&type=pdf), Fig.1，PDF p.2
- **类型**：T2/T3
- **可迁移点**：参数识别控制多个 DSP 模块
- **不适用 / 降级理由**：无显式二选一且控制线交叉多
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A3-14

- **来源与定位**：[Rykaczewski et al., 2005](https://dokumen.pub/ieee-mtt-v053-i03b-2005-03-53-3bnbsped.html), Fig.1，论文 p.2
- **类型**：T2/T3
- **可迁移点**：共用前后级与可重构局部分支
- **不适用 / 降级理由**：RF/模拟前端细节多，无完整测量闭环
- **Gate**：K/V/E



- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

## C — 基本不对路，不进入深度样本（7 张）

### A2-06

- **来源与定位**：[van der Heide et al., 2022](https://www.researchgate.net/publication/359597971_Real-time_transmission_of_geometrically-shaped_signals_using_a_software-defined_GPU-based_optical_receiver), Fig.1，PDF p.3
- **可迁移点**：有 DSP chain 和并行 processing streams
- **不适用 / 降级理由**：核心信息是 GPU profiler/实时实现，既无 selector 也无可迁移控制流


![A2-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a1a2/A2-06.png)

### A3-07

- **来源与定位**：[Choi and Hanzo, 2003](https://eprints.soton.ac.uk/258405/1/bjc-lh-May03-TVT.pdf), Fig.1，PDF p.2
- **可迁移点**：有 channel quality、switching levels 和反馈线
- **不适用 / 降级理由**：选择发生在 Tx，图型是自适应调制闭环，不是本地接收机算法选择


![A3-07 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-07.png)

### A3-08

- **来源与定位**：[Prakash and McLoughlin, 2011](https://scispace.com/pdf/analysis-of-adaptive-modulation-with-antenna-selection-under-56h636lpa6.pdf), Fig.1，PDF p.1
- **可迁移点**：measurement→decision→switch 关系紧凑
- **不适用 / 降级理由**：决策对象是 Tx 天线/调制，且没有接收端合流


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A3-09

- **来源与定位**：[Vicario and Antón-Haro, 2005](https://www.eurasip.org/Proceedings/Ext/IST05/papers/308.pdf), Fig.1，PDF p.2
- **可迁移点**：三条并行模式和统一 configuration command
- **不适用 / 降级理由**：三路位于 Tx，共同进入信道；与目标数据方向相反


![A3-09 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-09.png)

### A3-10

- **来源与定位**：[Faezah and Sabira, 2009](https://www.researchgate.net/publication/220178881_Adaptive_modulation_for_OFDM_systems), Fig.2，PDF p.3
- **可迁移点**：有完整 Tx–channel–Rx 和 mode selector
- **不适用 / 降级理由**：反馈线拥挤、排版弱，仍是控制 Tx 调制而非接收机内部选择


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A3-12

- **来源与定位**：[Shen et al., 2024](https://www.arxiv.org/pdf/2408.06359), Fig.1，PDF p.3
- **可迁移点**：顶层系统与 adaptive feedback 子管线同图
- **不适用 / 降级理由**：核心是 CSI 压缩/反馈，没有并行估计器或本地补偿语义


![A3-12 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-12.png)

### A3-13

- **来源与定位**：[Liang and Zhang, 2015](https://arxiv.org/pdf/1507.07290), Fig.1，PDF p.2
- **可迁移点**：switch→parallel paths→combiner 的结构表面相似
- **不适用 / 降级理由**：RF switch 在处理前分配 ADC，且没有 measurement/threshold 控制链



![A3-13 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A3-13.png)

## 第一轮结论

Gate A 已证明四类所需图型存在，但最重要的发现是：**“同一接收信号→DA/NDA 两异构估计器→基于块有效 SNR 的 selector→选中相位估计量；原信号独立旁路到相位补偿”尚无一张完全同构样图。**

因此，下一轮补样应优先找 hybrid/adaptive CPE、接收机本地算法选择和克制的多面板系统图；不再扩大 Tx 自适应调制、跨帧反馈和纯硬件切换样本。

## 第二轮定向补样

### 数量与主线程分级

- A4 精确 hybrid/adaptive CPR：15 张正式候选 + 1 张高价值专利拆图。
- A5 高层级论文版式：12 张已核验候选 + 1 张订阅墙备用。
- A6 本地接收机自适应选择：12 张候选。
- 第二轮合计 40 个已核验图位 + 1 个备用图位；主线程分级为 A 13、B 25、C 3。
- 两轮合计：81 个已核验图位 + 1 个备用；A 26、B 46、C 10（含订阅墙备用）。

第二轮没有找到完整同构图，但实质补齐了四种第一轮相对薄弱的真实语法：业务数据旁路、估计支路回灌补偿、数据线/控制线分型、本地 detector/estimator selection。

### 第二轮实图预览

#### 总览 + receiver-local 算法放大

[Fang et al. 2024 Fig.2 原图](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-024-50439-1/MediaObjects/41467_2024_50439_Fig2_HTML.png)

![Fang et al. 2024 Fig.2](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-024-50439-1/MediaObjects/41467_2024_50439_Fig2_HTML.png)

#### 跨支路共享相位估计/控制

[Lundberg et al. 2020 Fig.1 原图](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-019-14010-7/MediaObjects/41467_2019_14010_Fig1_HTML.png)

![Lundberg et al. 2020 Fig.1](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-019-14010-7/MediaObjects/41467_2019_14010_Fig1_HTML.png)

#### 业务数据旁路 + training 相位支路

[Xiang Zhou 2014 Patent Fig.3 原图](https://patentimages.storage.googleapis.com/a2/ea/fa/ef815d66bbe04a/US20140169784A1-20140619-D00003.png)

![Xiang Zhou 2014 Patent Fig.3](https://patentimages.storage.googleapis.com/a2/ea/fa/ef815d66bbe04a/US20140169784A1-20140619-D00003.png)

#### equalized signal 分流到 pilot estimation，主路连续 phase correction

[Millar et al. Patent Fig.3B 原图](https://patentimages.storage.googleapis.com/c2/0d/1e/e7ff1a041a5bb3/US10554309-20200204-D00009.png)

![Millar et al. Patent Fig.3B](https://patentimages.storage.googleapis.com/c2/0d/1e/e7ff1a041a5bb3/US10554309-20200204-D00009.png)

## 第二轮 A — 强匹配，优先并入深度候选（13 张）

### A4-01

- **来源与定位**：[Cao et al., 2012, IEEE PTL](https://www.researchgate.net/publication/258655469_Decision-Aided_Pilot-Aided_Decision-Feedback_Phase_Estimation_for_Coherent_Optical_OFDM_Systems), Fig.1，PDF p.2
- **类型**：T2/T4
- **可迁移点**：DA、PA、DA+PA、DF 多类相位信息置于同一估计/补偿框图
- **不适用 / 降级理由**：加权融合与级联，不是阈值二选一
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-04

- **来源与定位**：[Zhang et al., 2014, *Optical Engineering*](https://www.researchgate.net/figure/Scheme-of-the-pilot-tone-aided-phase-noise-PN-compensation_fig2_273561538), Fig.2，PDF p.3
- **类型**：T2
- **可迁移点**：接收信号分成 pilot estimation 与 data 主路，估计量只作用于 data phase correction
- **不适用 / 降级理由**：只有一个 pilot 估计器
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-09

- **来源与定位**：[Börjeson and Larsson-Edefors, 2021, JLT](https://research.chalmers.se/publication/521892/file/521892_Fulltext.pdf), Fig.3，PDF p.4
- **类型**：T2/T3
- **可迁移点**：多个 phase candidates→distance→minimum/mux，局部 selector 结构很专业
- **不适用 / 降级理由**：候选是 BPS 试探相位，无 SNR 门控
- **Gate**：K/V/E，S 部分


![A4-09 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-09.png)

### A4-10

- **来源与定位**：[Börjeson and Larsson-Edefors, 2021, conference paper](https://research.chalmers.se/publication/527589/file/527589_Fulltext.pdf), Fig.1，PDF p.2
- **类型**：T2/T3
- **可迁移点**：实线数据、虚线控制；format/window control 进入 CPR 管线
- **不适用 / 降级理由**：控制窗口和格式，不选择估计器
- **Gate**：K/V/E，S 部分


![A4-10 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-10.png)

### A4-13

- **来源与定位**：[Millar et al., 2016, JLT](https://www.merl.com/publications/docs/TR2016-029.pdf), Fig.5，PDF p.6
- **类型**：T1/T2
- **可迁移点**：pilot sequences 独立进入 joint PA-CPE，业务数据继续 Demod/FEC
- **不适用 / 降级理由**：是训练态/pilot 态，不是逐块 DA/NDA
- **Gate**：S/K/V/E


![A4-13 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-13.png)

### A4-15

- **来源与定位**：[Xiang Zhou, 2014 patent](https://patents.google.com/patent/US20140169784A1/en), Fig.3，[原图](https://patentimages.storage.googleapis.com/a2/ea/fa/ef815d66bbe04a/US20140169784A1-20140619-D00003.png)
- **类型**：T2/T3
- **可迁移点**：data block 一路进入训练相位估计，另一路直接进入 BPS refine；最接近“旁路数据+估计量驱动”
- **不适用 / 降级理由**：training estimate 与 BPS 串联，无 SNR selector
- **Gate**：S/K/E，V 部分



![A4-15 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-15.png)

### A4-16

- **来源与定位**：[Millar et al., 2020 patent](https://patents.google.com/patent/US10554309B2/en), Fig.3B，[原图](https://patentimages.storage.googleapis.com/c2/0d/1e/e7ff1a041a5bb3/US10554309-20200204-D00009.png)
- **类型**：T2/T3/T4
- **可迁移点**：equalized signal 分至 pilot extraction/estimation，数据主路连续经过两次 phase correction
- **不适用 / 降级理由**：专利图线密，仍是串联估计/精化
- **Gate**：S/K/E，V 部分



![A4-16 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-16.png)

### A5-01

- **来源与定位**：[Fang et al., 2024, *Nature Communications*](https://www.nature.com/articles/s41467-024-50439-1/figures/2), Fig.2，[原图](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-024-50439-1/MediaObjects/41467_2024_50439_Fig2_HTML.png)
- **类型**：T1/T2/T3/T4
- **可迁移点**：总览、两种恢复方案、residual-carrier 估计回灌主数据流分层完整
- **不适用 / 降级理由**：六面板和频谱/星座过满，只学层级
- **Gate**：S/K/V/E



![A5-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-01.png)

### A5-02

- **来源与定位**：[Lundberg et al., 2020, *Nature Communications*](https://www.nature.com/articles/s41467-019-14010-7/figures/1), Fig.1，[原图](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-019-14010-7/MediaObjects/41467_2019_14010_Fig1_HTML.png)
- **类型**：T1/T3/T4
- **可迁移点**：独立估计、master-slave 控制和联合估计的跨支路信息流很清楚
- **不适用 / 降级理由**：多波长共享估计，不是 DA/NDA 二选一
- **Gate**：S/K/V/E



![A5-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-02.png)

### A5-03

- **来源与定位**：[Mazur et al., 2019, *Optics Express*](https://opg.optica.org/viewmedia.cfm?figure=oe-27-17-24654-g001&imagetype=pdf&uri=oe-27-17-24654), Fig.1
- **类型**：T2/T4
- **可迁移点**：frame/pilot 语义与 DSP 顺序链上下并列，单栏克制
- **不适用 / 降级理由**：没有 selector 或控制回灌
- **Gate**：S/K/V/E


![A5-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-03.png)

### A5-04

- **来源与定位**：[Boscolo et al., 2022, *Optics Express*](https://opg.optica.org/viewmedia.cfm?figure=oe-30-11-19479-g002&imagetype=pdf&uri=oe-30-11-19479), Fig.2(a)
- **类型**：T2/T3/T4
- **可迁移点**：主信号链、phase extraction/KAF 估计和补偿回灌分层真实
- **不适用 / 降级理由**：KAF 内部细节偏多
- **Gate**：S/K/V/E


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A5-05

- **来源与定位**：[Hu et al., 2023, *Optics Express*](https://opg.optica.org/viewmedia.cfm?figure=oe-31-20-32114-g001&imagetype=pdf&uri=oe-31-20-32114), Fig.1(a–c)
- **类型**：T1/T2/T4
- **可迁移点**：一条系统主链，Tx/Rx DSP 用局部面板放大
- **不适用 / 降级理由**：实验器件较多，无 selector
- **Gate**：S/K/V，E 部分


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A6-02

- **来源与定位**：[Chaudhari et al., 2019](https://arxiv.org/pdf/1910.05369), Fig.1，PDF p.3
- **类型**：T2/T3/T4
- **可迁移点**：多 candidate detectors 并列，在线 selector 选择 LLR，业务数据连续进入公共 LDPC 后级
- **不适用 / 降级理由**：selector 是 MLP，需简化成 effective-SNR threshold
- **Gate**：S/K/V/E



![A6-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-02.png)

## 第二轮 B — 局部可迁移（25 张）

### A4-02

- **来源与定位**：[Cao et al. Fig.2](https://www.researchgate.net/publication/258655469_Decision-Aided_Pilot-Aided_Decision-Feedback_Phase_Estimation_for_Coherent_Optical_OFDM_Systems)，PDF p.3
- **可迁移点**：完整 CO-OFDM Tx/Rx 与算法嵌入
- **不适用 / 降级理由**：OFDM 模块多，核心算法太小


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-03

- **来源与定位**：[Zhang et al. Fig.1](https://www.researchgate.net/figure/Architecture-of-the-proposed-scheme-a-System-setup-with-spectrum-of-the-transmitted_fig1_273561538)，PDF p.2
- **可迁移点**：system/Tx DSP/Rx DSP 三面板
- **不适用 / 降级理由**：光域 pilot-tone 器件链过重


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-05

- **来源与定位**：[Zhang et al., 2014, *Optical Engineering*](https://www.researchgate.net/publication/273561538_Optical_domain_scheme_of_pilot-tone-aided_carrier_phase_recovery_for_Nyquist_single-carrier_optical_communication_system), Fig.3，PDF p.3
- **可迁移点**：ML 相位估计与去旋转主线
- **不适用 / 降级理由**：单一估计器


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-06

- **来源与定位**：[Diniz et al., 2019](https://ira.lib.polyu.edu.hk/bitstream/10397/81086/1/Diniz_Carrier_Recovery_Principal.pdf), Fig.2，PDF p.3
- **可迁移点**：连续业务流、PC 提取、unwrap、phase compensation
- **不适用 / 降级理由**：单一 NDA PCPE


![A4-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-06.png)

### A4-07

- **来源与定位**：[Diniz thesis, 2019](https://backend.orbit.dtu.dk/ws/files/217356236/JulioDiniz_Thesis_Handed_in_2019_Feb_27.pdf), Fig.6.5，印刷 p.93
- **可迁移点**：coarse/fine stage 与补偿级分离
- **不适用 / 降级理由**：串联 PCPE+BPS


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A4-08

- **来源与定位**：[Börjeson and Larsson-Edefors Fig.2](https://research.chalmers.se/publication/521892/file/521892_Fulltext.pdf)，PDF p.4
- **可迁移点**：并行 lanes、buffer 与 phase compensation
- **不适用 / 降级理由**：固定串联，无控制层


![A4-08 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-08.png)

### A4-11

- **来源与定位**：[Li et al., 2018, *Optics Express*](https://ira.lib.polyu.edu.hk/bitstream/10397/107016/1/oe-26-12-14817.pdf), Fig.6，PDF p.14
- **可迁移点**：Rx DSP 分为同步、信道估计、载波恢复、数据恢复
- **不适用 / 降级理由**：图面未画 SNR/linewidth 反馈


![A4-11 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-11.png)

### A4-12

- **来源与定位**：[Yang thesis, 2024](https://discovery.ucl.ac.uk/10199265/1/PhD_Thesis_JYang_18148351_Correction.pdf), Fig.3.2，印刷 p.71
- **可迁移点**：conventional/pilot-based DSP 对照
- **不适用 / 降级理由**：对照方案，不是在线 selector


![A4-12 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-12.png)

### A4-14

- **来源与定位**：[Millar et al. Fig.8](https://www.merl.com/publications/docs/TR2016-029.pdf)，PDF p.7
- **可迁移点**：估计量串行处理阶段清楚
- **不适用 / 降级理由**：不含业务信号旁路


![A4-14 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a3a4/A4-14.png)

### A5-06

- **来源与定位**：[Sowailem et al., 2017](https://opg.optica.org/viewmedia.cfm?figure=oe-25-22-27834-g003&imagetype=pdf&uri=oe-25-22-27834), Fig.3
- **可迁移点**：Tx/Rx DSP 两条窄链，模块粒度克制
- **不适用 / 降级理由**：self-homodyne 无 CPR 控制支路


![A5-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-06.png)

### A5-07

- **来源与定位**：[Ji et al., 2020](https://opg.optica.org/viewmedia.cfm?figure=oe-28-15-22882-g001&imagetype=pdf&uri=oe-28-15-22882), Fig.1(a,b)
- **可迁移点**：数据路径与 APC feedback loop 分型
- **不适用 / 降级理由**：photonics 器件细节多


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A5-08

- **来源与定位**：[Karanov et al., 2019](https://opg.optica.org/viewmedia.cfm?figure=oe-27-14-19650-g001&imagetype=pdf&uri=oe-27-14-19650), Fig.1
- **可迁移点**：物理链与训练优化链分层
- **不适用 / 降级理由**：IM/DD+神经网络，语义离题


![A5-08 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-08.png)

### A5-09

- **来源与定位**：[Kumpera et al., 2015](https://opg.optica.org/viewmedia.cfm?figure=oe-23-10-12952-g003&imagetype=pdf&uri=oe-23-10-12952), Fig.3
- **可迁移点**：信号、LO、PLL 控制回路分层
- **不适用 / 降级理由**：实验器件多、版式较旧


![A5-09 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-09.png)

### A5-10

- **来源与定位**：[Zhang et al., 2024](https://www.nature.com/articles/s41467-024-52269-7/figures/4), Fig.4
- **可迁移点**：brief architecture + DSP modules 的克制多面板
- **不适用 / 降级理由**：主要是版式，控制流弱


![A5-10 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-10.png)

### A5-11

- **来源与定位**：[Chen et al., 2025](https://www.nature.com/articles/s44172-025-00505-3/figures/1), Fig.1
- **可迁移点**：总览 + receiver-local FNT-DSP
- **不适用 / 降级理由**：六面板带应用/功耗叙事，海报化风险


![A5-11 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-11.png)

### A5-12

- **来源与定位**：[Kakkar et al., 2017](https://www.nature.com/articles/s41598-017-00868-4/figures/1), Fig.1
- **可迁移点**：端到端链 + 少量波形 inset
- **不适用 / 降级理由**：无细 DSP 和控制支路


![A5-12 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A5-12.png)

### A6-01

- **来源与定位**：[Umamaheshwar et al., 2019](https://www.ijrte.org/wp-content/uploads/papers/v8i1/A3386058119.pdf), Fig.1，PDF p.2
- **可迁移点**：SNR→threshold→selector→ZF/MMSE 的完整骨架
- **不适用 / 降级理由**：图粗糙、低层级来源，技术方向可疑；只借结构


![A6-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-01.png)

### A6-03

- **来源与定位**：[Roger Varea thesis, 2008](https://riunet.upv.es/bitstreams/9e99eb67-296b-4df1-883b-14b5b40ce54c/download), Fig.4.2，PDF p.22
- **可迁移点**：指标估计、阈值和 decoder 控制/数据线分离
- **不适用 / 降级理由**：偏流程图，选择参数而非两套算法


![A6-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-03.png)

### A6-04

- **来源与定位**：[Bithas and Rontogiannis, 2014](https://www.researchgate.net/publication/264583253_Analysis_of_Threshold-Based_Selection_Diversity_Receivers), Fig.1
- **可迁移点**：极简 measurement→threshold→stay/switch
- **不适用 / 降级理由**：控制 diversity branch，无主数据链


![A6-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-04.png)

### A6-05

- **来源与定位**：[Wu et al., 2010](https://link.springer.com/article/10.1155/2010/893184), Fig.4
- **可迁移点**：公共输入、dual mode、公共 LLR 后级
- **不适用 / 降级理由**：mode register 非在线质量门限


![A6-05 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-05.png)

### A6-06

- **来源与定位**：[Galli, 2002](https://www.researchgate.net/publication/3160828_A_new_family_of_soft-output_adaptive_receivers_exploiting_nonlinear_MMSE_estimates_for_TDMA-based_wireless_links), Fig.2/3
- **可迁移点**：控制反馈、软估计和业务检测线分层
- **不适用 / 降级理由**：按训练/数据状态切换


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A6-07

- **来源与定位**：[Al-Dweik et al., 2008](https://www.researchgate.net/publication/220085928_A_Hybrid_Decoder_for_Block_Turbo_Codes), Fig.2
- **可迁移点**：switch、反馈、公共输出紧凑
- **不适用 / 降级理由**：顺序 decoder 切换，非质量门控估计器


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A6-08

- **来源与定位**：[Guimarães et al., 2014](https://link.springer.com/article/10.1186/1687-1499-2014-32), Fig.2
- **可迁移点**：质量检查不打断主码流，失败再启用复杂路径
- **不适用 / 降级理由**：两阶段串行，流程较长


![A6-08 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-08.png)

### A6-11

- **来源与定位**：[Umamaheshwar et al. Fig.2](https://www.ijrte.org/wp-content/uploads/papers/v8i1/A3386058119.pdf)，PDF p.2
- **可迁移点**：detector-selection unit 内部 zoom-in
- **不适用 / 降级理由**：线条/命名不规范，与 A6-01 同组


![A6-11 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-11.png)

### A6-12

- **来源与定位**：[Chaudhari et al. Fig.2](https://arxiv.org/pdf/1910.05369)，PDF p.4
- **可迁移点**：selector 控制器 zoom-in
- **不适用 / 降级理由**：单独使用会丢主数据路径



![A6-12 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-12.png)

## 第二轮 C — 不进入深度样本（3 张）

### A5-13

- **来源与定位**：[Suzuki et al., 2020, JLT](https://opg.optica.org/jlt/abstract.cfm?uri=jlt-38-3-668)，图号未公开复核
- **可迁移点**：T2/T3；计算传输与 DSP 并行 pipeline
- **不适用 / 降级理由**：订阅墙导致图号/图面不可核验；且主题是 GPU stream split，不是通信信号控制流


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A6-09

- **来源与定位**：[Matthaiou et al., 2008](https://ncrl.seu.edu.cn/_upload/article/files/22/03/93233bb8454a97d510b47265f6b9/667850d2-8002-4e3f-8d91-409f30de45d9.pdf)
- **可迁移点**：T3；condition-number threshold 选择 ZF/ML 的技术语义
- **不适用 / 降级理由**：论文没有架构图，只有性能图；不能作为视觉样本


- **本地预览**：暂缺。公开来源受限、目标图无法核验，或该候选本身没有架构图；保留上方来源与页码供手动查看。

### A6-10

- **来源与定位**：[Narasimha et al., 2010](https://shanbhag.ece.illinois.edu/publications/rajan-sips-2011.pdf), Fig.1
- **可迁移点**：T2/T3；主业务数据与 CDR/clock 控制线分离
- **不适用 / 降级理由**：连续 ADC/equalizer 参数自适应，无离散 selector 或双路径



![A6-10 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-a5a6/A6-10.png)

## 两轮合并后的优先阅读顺序

如果下一步进入深度分析，主线程建议先看以下 12 张，而不是平均分析全部 A/B：

1. Fang 2024 Fig.2：总览 + receiver-local algorithm zoom-in。
2. Cao 2012 Fig.1：同一图内多类相位信息与补偿关系。
3. Zhang 2014 Fig.2：业务数据旁路 + pilot estimation 回灌补偿。
4. Baeuerle 2016 Fig.5：并行 phase candidates + selector。
5. Faruk 2014 Fig.2：监测支路不截断主 CPE 数据链。
6. Chaudhari 2019 Fig.1：本地 receiver 内多算法选择 + 公共后级。
7. Börjeson 2021 programmable Fig.1：实线数据 / 虚线控制。
8. Xiang Zhou 2014 patent Fig.3：data bypass + training phase estimate。
9. Millar 2016 Fig.5：pilot 辅助 CPE 与业务数据恢复分层。
10. Boscolo 2022 Fig.2：估计支路→补偿主路。
11. Liu 2017 Fig.1：监测量驱动后级 DSP 重配置。
12. Li 2021 Fig.1：FSO 端到端系统上下文。

这 12 张仍不是 12 个“可照搬模板”，而是覆盖 6 种互补语法的最小阅读集。

## 第三轮：设计感优先的视觉语法补样

### 为什么要另开一轮

用户审阅前两轮后指出多数图“挺一般”“缺乏设计感”。该判断成立：前两轮 Gate A 证明了系统总览、DSP 管线、自适应控制和多尺度拆图等**图型存在**，但没有把视觉品质列为入选门槛。因此，第三轮不再扩大同题工程框图数量，而把“语义参考”和“风格参考”分开：前两轮负责技术正确，第三轮只补能迁移层级、留白、分面、控制/数据编码的视觉语法。

第三轮视觉 Gate 共 6 项：①缩小后主次仍清楚；②不是满屏同质方框；③主数据流与控制/反馈流可辨；④总览—局部层级清楚；⑤少量颜色具有语义且黑白可读；⑥适合紧凑论文版面。至少 4/6 才入选，并额外要求③或④至少一项 PASS。三个猎手共保留 15 张：4 张 6/6、10 张 5/6、1 张 4/6；全部有本地预览。另有 Neural-Fly Fig.2 虽初评 6/6，但公开 PDF 下载截断、无法可靠生成预览，故不作为候选卡收录。

### B1：顶刊总览与局部放大（6 张）

### B1-01

- **来源与定位**：[Learning diffractive optical communication around arbitrary opaque occlusions](https://www.nature.com/articles/s41467-023-42556-0)，*Nature Communications*, 2023，Fig.1，PDF p.3
- **图型**：端到端通信总览 + 编码器局部 + 接收解码器局部 + 对照面板
- **视觉 Gate**：6/6
- **可迁移点**：主面板先讲消息—信道—接收恢复，局部面板只展开需要解释的处理器；层级不依赖堆叠方框。
- **明显不适用点**：全光衍射解码与 CNN/图像样例不可迁移；只借整体叙事和分面层级。
- **判断**：本轮整体信息架构最强，适合定“系统主图 + receiver-local 放大”的版式上限。

![B1-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-01.png)

### B1-02

- **来源与定位**：[Multipurpose silicon photonics signal processor core](https://www.nature.com/articles/s41467-017-00714-1)，*Nature Communications*, 2017，Fig.1，PDF p.3
- **图型**：处理器总架构 + 可重构核心拓扑 + 单元级放大
- **视觉 Gate**：6/6
- **可迁移点**：光路、电子控制和内部核心用少量颜色分层；由总架构逐级放大到核心和单元。
- **明显不适用点**：六边形光子 mesh 不是接收算法；不能借具体造型，只借数据层/控制层分色和放大关系。
- **判断**：本轮最克制、最像高水平期刊成图的样本。

![B1-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-02.png)

### B1-03

- **来源与定位**：[Advancing theoretical understanding and practical performance of signal processing for nonlinear optical communications through machine learning](https://www.nature.com/articles/s41467-020-17516-7)，*Nature Communications*, 2020，Fig.4，PDF p.4
- **图型**：数字相干接收 DSP 的 Training/Testing 双泳道
- **视觉 Gate**：5/6（缺端到端总览）
- **可迁移点**：公共前后级对齐，差异只放在中间核心；辅助输入从侧面接入，不截断业务主链。
- **明显不适用点**：训练/测试不是 DA/NDA 在线切换；只能借泳道对齐与公共模块复用。
- **判断**：不华丽，但留白、对齐和职责分界很稳。

![B1-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-03.png)

### B1-04

- **来源与定位**：[Reduced-size lookup tables enabling higher-order QAM with all-silicon IQ modulators](https://opg.optica.org/oe/fulltext.cfm?uri=oe-27-17-24243)，*Optics Express*, 2019，Fig.2
- **图型**：中心实验系统 + 左右 Tx/Rx DSP 摘要 + 器件响应 inset
- **视觉 Gate**：5/6（单栏缩放风险）
- **可迁移点**：物理光路为视觉主干，DSP 作为两端附着的局部说明；物理域/数字域由位置和底色区分。
- **明显不适用点**：密度偏高且创新在发端；目标 Fig.1 不应照搬器件 inset。
- **判断**：适合借“实验系统中挂 DSP”的骨架，不宜借密度。

![B1-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-04.png)

### B1-05

- **来源与定位**：[Modified low-bandwidth sub-Nyquist sampling receiving scheme in an IM/DD OFDM system enabled by improved optical shaping](https://doi.org/10.1364/OE.462705)，*Optics Express*, 2022，Fig.3
- **图型**：端到端实验链 + 三处 DSP inset + 频谱语义小图
- **视觉 Gate**：5/6（局部面板接近密度上限）
- **可迁移点**：只在关键节点挂 DSP 局部，不把全部算法塞进系统主链。
- **明显不适用点**：五个 inset 过多；频谱证据与目标 Fig.1 无关。
- **判断**：与“系统总览 + DSP 局部”形态最同构，但必须显著减法。

![B1-05 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-05.png)

### B1-06

- **来源与定位**：[4-bit DAC based 6.9 Gb/s PAM-8 UOWC system using single-pixel mini-LED and digital pre-compensation](https://pubmed.ncbi.nlm.nih.gov/36236958/)，*Optics Express*, 2022，Fig.5
- **图型**：水下光通信实验总览 + Tx/Rx DSP 双局部
- **视觉 Gate**：5/6（横向过长）
- **可迁移点**：物理链居中，收发数字链分别附着两端，阅读顺序清楚。
- **明显不适用点**：PAM-8/IM-DD 与相干 CPR 技术语义较远，小模块需大幅删减。
- **判断**：设计感不及 B1-01/B1-02，但系统与 DSP 的职责边界干净。

![B1-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b1/B1-06.png)

### B2：自适应控制与判据驱动（5 张）

### B2-02

- **来源与定位**：[Adaptive Neural Networks for Efficient Inference](https://proceedings.mlr.press/v70/bolukbasi17a/bolukbasi17a.pdf)，ICML 2017，Fig.2，PDF p.3
- **图型**：多网络选择拓扑 + 逐层 early-exit 拓扑
- **视觉 Gate**：5/6（两面板是并列变体，不是总览—局部）
- **可迁移点**：confidence feedback 驱动 policy/selector，并决定跳转或输出；与 effective-SNR 阈值切换的局部逻辑接近。
- **明显不适用点**：原图是串级 early exit，不能把 CPR 误画成多级串行。
- **判断**：本轮最接近 selector 语义的样本，适合定判据节点和箭头语法。

![B2-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b2/B2-02.png)

### B2-03

- **来源与定位**：[Adapting Rapid Motor Adaptation for Bipedal Robots](https://hybrid-robotics.berkeley.edu/publications/IROS2022_AdaptingRMA_Biped.pdf)，IROS 2022，Fig.2，PDF p.2
- **图型**：三阶段训练 + deployment，旁路适配器驱动主策略
- **视觉 Gate**：6/6
- **可迁移点**：历史/测量旁路进入 adaptation module，再以低维估计驱动主快速路径；很适合表达 quality measurement 不承载业务数据。
- **明显不适用点**：训练阶段和机器人图标不能照搬；目标只借 deployment 的旁路层级。
- **判断**：复杂但不沉闷，是“旁路估计控制主链”的强视觉参考。

![B2-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b2/B2-03.png)

### B2-04

- **来源与定位**：[Adaptive Deep Neural Network Inference Optimization with EENet](https://openaccess.thecvf.com/content/WACV2024/papers/Ilhan_Adaptive_Deep_Neural_Network_Inference_Optimization_With_EENet_WACV_2024_paper.pdf)，WACV 2024，Fig.2，PDF p.4
- **图型**：重复推理主链 + score/threshold 判据 + scheduler
- **视觉 Gate**：5/6（单图缺系统总览）
- **可迁移点**：score→threshold→exit/continue 的菱形判据，可映射 effective SNR→固定阈值→DA/NDA 选择。
- **明显不适用点**：多级 early exit 需压缩为一个判据和两条候选路径。
- **判断**：本轮最干净的“数值判据控制数据流”局部样本。

![B2-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b2/B2-04.png)

### B2-05

- **来源与定位**：[DayDreamer: World Models for Physical Robot Learning](https://autolab.berkeley.edu/assets/publications/media/2022-12-DayDreamer-CoRL.pdf)，CoRL 2022，Fig.2，PDF p.2
- **图型**：现实系统—经验—模型—策略的极简闭环
- **视觉 Gate**：4/6（数据/学习/控制箭头未分型；无局部放大）
- **可迁移点**：主对象置底，轻量闭环在上方绕回；可以借“少框、强闭环”的构图。
- **明显不适用点**：跨迭代学习不是逐 block 控制，没有阈值或双算法路径；只借版式。
- **判断**：有记忆点但技术同构性最低，是边缘风格样本。

![B2-05 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b2/B2-05.png)

### B2-06

- **来源与定位**：[ROSA: a knowledge-based solution for robot self-adaptation](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1531743/full)，*Frontiers in Robotics and AI*, 2025，Fig.1
- **图型**：上层管理/反馈系统 + 下层业务系统
- **视觉 Gate**：5/6（模块数量偏多）
- **可迁移点**：measurement→criterion→selector 可作为控制平面，下层保留 Rx DSP 主数据链；控制平面不吞业务样本。
- **明显不适用点**：MAPE-K 和知识库语义过重，必须压缩到 4–6 个角色。
- **判断**：工程味仍较重，但控制层/业务层分离非常明确。

![B2-06 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b2/B2-06.png)

### B3：DSP/芯片管线与公共后级（4 张）

### B3-01

- **来源与定位**：[3.2 Gbps Channel-Adaptive Configurable MIMO Detector for Multi-Mode Wireless Communication](https://web.eecs.umich.edu/~zhengya/papers/sheikh_sips14.pdf)，IEEE SiPS 2014，Fig.7，PDF p.4
- **图型**：多级芯片流水线总览 + 上层自适应控制器
- **视觉 Gate**：6/6
- **可迁移点**：控制器在下方以 scheduling signal 驱动横向主数据通路；数据层和控制层分得很清楚。
- **明显不适用点**：原图改变各流水级参数，不是 DA/NDA 双完整支路。
- **判断**：本轮最成熟的“控制层 + 数据管线”黑白架构语法。

![B3-01 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b3/B3-01.png)

### B3-02

- **来源与定位**：同上，Fig.8，PDF p.5
- **图型**：单级 K-best 流水线局部放大
- **视觉 Gate**：5/6（单独缩小后全局主次不足）
- **可迁移点**：可作为总图中的 receiver-local CPR 内部放大，表现估计、旋转、缓冲或选择逻辑。
- **明显不适用点**：没有全局 selector 和公共后级，不能单独承担 Fig.1。
- **判断**：工程局部图合格，只应与 B3-01 成组使用。

![B3-02 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b3/B3-02.png)

### B3-03

- **来源与定位**：[A Residual Phase Noise Compensation Method for IEEE 802.15.4 Compliant Dual-Mode Receiver](https://people.iith.ac.in/raji/Cpapers/Residual%20Phase.pdf)，*IEEE Internet of Things Journal*, 2019，Fig.2，PDF p.5
- **图型**：共享前端 + 两条接收链 + 控制器/共享资源 + 公共解码
- **视觉 Gate**：5/6（控制线与数据线分型不足）
- **可迁移点**：语义上最接近双模式接收机：公共输入、两条算法链、共享资源与公共后级同时出现。
- **明显不适用点**：线密、造型老式，绝不能当审美模板；只借双支路和共享后级关系。
- **判断**：结构价值高、视觉价值低，必须明确“借语义不借造型”。

![B3-03 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b3/B3-03.png)

### B3-04

- **来源与定位**：[Channel-aware adaptive receivers for linearly precoded MIMO-OFDM systems with imperfect CSIT](https://link.springer.com/article/10.1186/1687-1499-2013-240/figures/3)，EURASIP JWCN 2013，Fig.3
- **图型**：自适应算法选择器 + 两类检测输出 + 公共译码后级 + 选择性反馈
- **视觉 Gate**：5/6（宽幅版面较拥挤）
- **可迁移点**：selector 汇流到公共 downstream，并保留差异化反馈；适合核对数据、选择控制和反馈三类箭头。
- **明显不适用点**：turbo receiver 模块过多，需删除 CPR 无关反馈环。
- **判断**：逻辑骨架清楚，但造型只能作为次级参考。

![B3-04 本地预览](../../projects/simulation/figures/fig1-reference-previews/batch-b3/B3-04.png)

### 第三轮视觉 Gate 结果

- **顶刊总览/局部放大**：6 张，PASS。代表为 B1-01、B1-02。
- **自适应判据/控制支路**：5 张，PASS。代表为 B2-02、B2-03、B2-04。
- **DSP/芯片管线与公共后级**：4 张，PASS。代表为 B3-01；B3-03 只承担语义参考。
- **本地可见性**：15/15 张有 PNG，PASS；1 张潜在线索因预览无法核验而排除。
- **主线程结论**：前两轮“多数一般”的问题得到定位，不应继续找更多同题老式工程框图。后续若获用户确认，应把 B1-01/B1-02 的总览—局部层级、B2-02/B2-04 的判据语法、B3-01 的控制/数据分层，与前两轮的真实 CPR 数据旁路语义组合研究；仍不能选一张照抄。

## 对决策的影响

不改变 D010。第三轮补齐了视觉风格参考，但当前仍只确认样图类型与优先级，不决定 Fig.1 信息架构，不选择 draw.io/SVG/TikZ/image，也不开始绘制。
