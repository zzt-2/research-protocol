# [R004] 信号处理方向综述检索——研究方向切分调研

> 2026-06-03 | 关联：PROMPT-018 | 状态：完成
> 聚焦场景：星地激光通信（卫星到地面）

## 调研问题

Ch4 标题是"湍流下相干接收端信号处理方法研究"，但当前 §4.4 三个探索方向（环路参数解析设计 / 多源相位噪声联合补偿 / 编码辅助载波恢复）全部聚焦在载波同步子领域。

核心问题：
1. 别人怎么切分"FSO 相干接收端信号处理"这个领域的研究方向？
2. 有哪些比"载波同步"更大的研究主题？
3. 如何设计 3 个足够宽的"研究主题"使得后续论文中几乎所有信号处理工作都能装进去？

## 检索方法

### 英文搜索（7 组）

| # | 搜索关键词 | 结果质量 |
|---|-----------|---------|
| 1 | `survey "coherent receiver" "signal processing" "free space optical"` | 中等，找到 FSO enabling technologies survey (84c) |
| 2 | `survey "digital signal processing" "optical wireless" turbulence` | 一般，UWOC 论文混入 |
| 3 | `review "satellite-to-ground" optical communication DSP` | 差，主要是无人机 PPM |
| 4 | `survey "carrier synchronization" "channel coding" "joint" optical` | 一般，找到 PSAM frame 设计 |
| 5 | `survey "receiver architecture" "atmospheric turbulence" coherent FSO` | **好**，找到 236c JLT 综述 + Vannucci fibers-to-satellites |
| 6 | `coherent optical receiver "digital signal processing" chain survey review` | **好**，找到 Valjus 2025 星地 DSP 综述 + Savory 2009 DSP chain |
| 7 | `"satellite-to-ground" OR "ground-to-satellite" coherent optical "signal processing"` | 中等，找到 Paillier 2020 DPLL |

### CNKI 搜索（5 组）

| # | 搜索关键词 | 结果 |
|---|-----------|------|
| 1 | `星地激光通信 信号处理 综述` | 0 条 |
| 2 | `大气湍流 相干接收 综述` | 0 条 |
| 3 | `自由空间光通信 数字信号处理 进展` | 0 条 |
| 4 | `相干光通信 自由空间` | **20 条**，多篇相关硕士/博士论文 |
| 5 | `星地 激光通信 信号处理` | **5 条**，含关键博士论文 |

CNKI 前几组返回 0 是因为 `--source cnki` 参数错误，换用 `bash tools/blit --source cnki` 后正常返回。

### 所有搜索结果存档位置

```
search-archive/2026-06-03/
├── survey-coherent-receiver-signal-processing-free-space-optica.json
├── survey-digital-signal-processing-optical-wireless-turbulence.json
├── review-satellite-to-ground-optical-communication-dsp.json
├── survey-carrier-synchronization-channel-coding-joint-optical.json
├── survey-receiver-architecture-atmospheric-turbulence-coherent.json
├── coherent-optical-receiver-dsp-block-diagram-signal-processin.json
├── turbulence-mitigation-coherent-fso-receiver-signal-processin.json
├── coherent-detection-free-space-optical-phase-noise-or-frequen.json
├── free-space-optical-coherent-carrier-recovery-or-carrier-sync.json
├── satellite-to-ground-or-ground-to-satellite-coherent-optical-.json
```

---

## 发现的综述论文列表

### Tier 1：直接对标（星地/FSO 相干接收 DSP）

#### 1. Valjus et al. (2025) — "Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links"

- **期刊**: International Journal of Satellite Communications and Networking (Wiley), Vol.43, pp.229-250
- **DOI**: 10.1002/sat.1553
- **引用**: 9
- **开放获取**: 是 (CC BY 4.0)
- **作者**: Carl Valjus, Raphael Wolf (DLR, 德国航空航天中心)
- **本地路径**: `papers/downloads/2026-05-29/` 下已有全文 markdown
- **相关性**: ★★★★★ — 最直接对标的综述，专门讨论相干光卫星链路 DSP

**DSP 链结构（论文核心分类）**：

```
相干光卫星接收机 DSP
├── Static Compensation（静态补偿，简述）
├── 1. Timing Recovery（定时恢复）                     [Section 3]
│   ├── 3.1 Feedback Algorithms（反馈式）
│   │   ├── Gardner 算法
│   │   ├── Godard 频域算法
│   │   ├── Gu 幅度无关算法
│   │   └── 其他反馈算法
│   ├── 3.2 Feedforward Algorithms（前馈式）
│   │   ├── Lee 前馈算法
│   │   └── Oerder-Meyer 前馈算法
│   ├── 3.3 Resampling Algorithms（重采样）
│   │   ├── Lagrange/Farrow 插值
│   │   ├── 线性插值
│   │   ├── 三角多项式插值
│   │   └── 频域重采样
│   └── 3.4 Analysis（四种场景仿真对比）
├── 2. Carrier Synchronization（载波同步）
│   ├── Carrier Phase Estimation（载波相位估计）       [Section 4]
│   │   ├── 4.1 Phase Estimation Algorithms
│   │   │   ├── Viterbi-Viterbi（M次幂法）
│   │   │   ├── 差分编码（软/硬 DQPSK）
│   │   │   ├── 导频辅助（pilot-aided）
│   │   │   ├── 盲相位搜索（BPS，简述）
│   │   │   └── PCA 法（简述）
│   │   └── 4.2 Analysis（四场景仿真）
│   └── Carrier Frequency Offset Compensation（频偏补偿）[Section 5]
│       ├── 5.1 Frequency Offset Estimation Algorithms
│       │   ├── 盲时域 M 次幂法
│       │   ├── 盲频域法
│       │   ├── Data-aided 训练序列法
│       │   ├── Schmidl-Cox 前导法
│       │   └── CRT 扩展 Schmidl-Cox
│       └── 5.2 Analysis
├── 3. Adaptive Equalizer（自适应均衡）                [Section 6]
│   ├── 6.1 Time Domain Equalization（时域）
│   │   ├── CMA（常数模算法）
│   │   ├── LMS / DA-LMS（数据辅助）
│   │   └── DD-LMS（判决指引）
│   ├── 6.2 Frequency Domain Equalization（频域）
│   │   └── MMSE 频域训练序列法
│   ├── 6.3 Equalizer Structures
│   │   ├── N-tap butterfly 结构
│   │   ├── 1+N 两级结构
│   │   └── N+1 两级结构
│   └── 6.4 Analysis
└── FEC / Decoding（简述，未独立成章）
```

**四场景信道模型**（Section 2）：
1. ISL（星间链路，无大气）
2. 下行链路（对数正态闪烁）
3. 上行链路弱湍流（σ_p = 0.15）
4. 上行链路强湍流（σ_p = 0.25）

**标注的开放问题**：
1. 定时恢复在真实大气信道中的长期稳定性未验证
2. 时钟抖动对高并行度/低滚降系统的影响未分析
3. **动态调整相位估计窗口**——"Further research is necessary to identify practical methods"
4. 低波特率系统（如 10 Gbaud）的频偏补偿更困难
5. **均衡器在深度衰落中发散到局部最优**——"probability of equalizer diverging... has not been analyzed"
6. **完整 DSP 链在真实条件下的联合评估**——"evaluating the complete DSP chain under realistic conditions is critical"
7. 子系统间协同设计——数据辅助算法依赖帧同步和定时恢复的正确对齐

**关键结论**：
- 载波同步被拆为相位估计和频偏补偿两个并列顶层章节
- 与定时恢复、自适应均衡并列为三大子系统
- **数据辅助（pilot-based）算法在 OSL 中优于盲算法**（低 SNR 下性能好、捕获快、复杂度低）
- 聚焦 QPSK 调制格式

#### 2. Kaushal & Kaddoum (2017) — "Optical Communication in Space: Challenges and Mitigation Techniques"

- **期刊**: IEEE Communications Surveys & Tutorials, Vol.19, No.1, pp.57-96
- **DOI**: 10.1109/COMST.2016.2603518
- **引用**: 1480
- **开放获取**: 是（ETS Montreal 仓库）
- **相关性**: ★★★★☆ — 经典综述，"挑战→缓解"二分法

**章节结构**：

```
I. Introduction
   A-F: 分类、FSO优势、波长选择、相关综述、论文组织
II. Challenges in Space-Based Optical Communication
   A. FSO Uplink/Downlink（8子项）
      (I) 吸收与散射损耗
      (II) 大气湍流
      (III) 光束扩散
      (IV) 背景噪声与天空辐射
      (V) 闪烁模型
      (VI) 云遮挡
      (VII) 大气视宁度
      (VIII) 到达角起伏
   B. Inter-satellite Links（4子项）
      (I) 瞄准超前角(PAA)
      (II) 多普勒频移 ← 载波同步在此
      (III) 卫星振动与跟踪
      (IV) 背景噪声源
III. Acquisition, Tracking and Pointing (ATP)
IV. Mitigation Techniques
   A. Physical Layer Methods（9类）          ← 关键分类
      (I) 孔径平均
      (II) 分集技术（空间/时间/频率/波长）
      (III) 中继传输
      (IV) 自适应光学
      (V) 调制（OOK/PPM/DPPM/PIM/BPSK/DPSK/SIM）
      (VI) 编码（FEC/交织/LDPC/Turbo）
      (VII) 抖动隔离与抑制
      (VIII) 背景噪声抑制
      (IX) 混合 RF/FSO 链路
   B. TCP Upper Layer Methods（4类）
      (I) 重传
      (II) 重配置与重路由
      (III) QoS控制
      (IV) 其他（重放、DTN）
V. Orbital Angular Momentum (OAM) for FSO
VI. FSO Backhaul Communication
VII. Future Scope
VIII. Conclusions
```

**载波同步的定位**：
- **不是独立研究方向**，仅作为"星间链路 → 多普勒频移"的子项
- 引用了 OPLL [182]、OIPLL [183-184]、homodyne 多普勒补偿器 [185-187]
- 在"调制"章节讨论了 homodyne/heterodyne 需"perfect phase alignment"

**关键发现**：
- 载波同步在该论文中被归入"挑战"而非"缓解技术"
- 物理层缓解技术 9 类中没有"同步"——说明在 2017 年，同步被视为已知解决方案（OPLL），不是研究方向
- 调制和编码是独立的大方向

#### 3. "Coherent free-space optical communications: Opportunities and challenges" (2022)

- **期刊**: Journal of Lightwave Technology, Vol.40, No.10, pp.3173-3190
- **DOI**: 10.1109/JLT.2022.3164736
- **引用**: 236（部分来源显示 145）
- **相关性**: ★★★★☆ — 相干 FSO 领域最重要的综述

**摘要核心内容**：
- 讨论"ever-increasing data rate demand"推动光无线解决方案
- 覆盖相干 FSO 的机遇和挑战
- 由于 API 过载，子 agent 两次未成功获取全文
- 从搜索结果推断：应包含接收机架构、DSP 链、分集方案等内容

**待补充**：后续对话应尝试获取此论文全文，提取完整章节结构。

### Tier 2：相关但不专门针对星地

#### 4. Khalighi & Uysal (2014) — "Survey on Free Space Optical Communication: A Communication Theory Perspective"

- **期刊**: IEEE Communications Surveys & Tutorials, Vol.16, No.4
- **DOI**: 10.1109/comst.2014.2329501
- **引用**: 2382（FSO 领域被引最多）
- **相关性**: ★★★☆☆ — 通信理论视角，2014 年较早

#### 5. Savory (2009) — "DSP for Coherent Single-Carrier Receivers"

- **期刊**: JLT
- **DOI**: 10.1109/JLT.2009.2024963
- **引用**: 297
- **相关性**: ★★★☆☆ — 光纤 DSP chain 经典文献
- **摘要**: 覆盖 CD、PMD、PDL、XPM 补偿，"single DSP receiver modules"

#### 6. "Carrier-phase recovery for coherent optical systems" (2023)

- **期刊**: JLT
- **DOI**: 10.1109/JLT.2023.3340010
- **引用**: 22-39（不同数据源）
- **相关性**: ★★★☆☆ — 载波相位恢复算法综述

#### 7. "Review on Modulation Formats and Channel Coding in FSO" (2026)

- **期刊**: JLT
- **DOI**: 10.1109/JLT.2026.3664749
- **引用**: 3
- **相关性**: ★★★★☆ — 最新（2026），直接讨论调制和编码两个大方向

#### 8. "Optical communications in turbulence: a tutorial" (2023)

- **期刊**: Optical Engineering
- **DOI**: 10.1117/1.OE.63.4.041207
- **引用**: 14
- **相关性**: ★★★★☆ — 湍流下光通信教程

#### 9. Paillier et al. (2020) — "Space-Ground Coherent Optical Links: Ground Receiver Performance With AO and DPLL"

- **期刊**: JLT
- **DOI**: 10.1109/jlt.2020.3003561
- **引用**: 35
- **相关性**: ★★★★★ — 星地相干链路 + DPLL，直接对标当前论文的 Paillier 参考

#### 10. Vannucci et al. (2022) — "From fibers to satellites: lessons to learn and pitfalls to avoid"

- **会议**: Asilomar Conference
- **引用**: 2
- **相关性**: ★★★★☆ — 光纤到 FSO 的迁移经验

**摘要核心**：
- 讨论将光纤相干技术适配到 FSO 的可行性
- 覆盖接收机架构、分集方案、波长分集
- 建议在相干接收机中使用波长分集（2-4 dB 增益）

### Tier 3：CNKI 中文论文

#### 11. 张岱 (2018) — "星地相干激光通信大气信道特征及信号处理技术研究"

- **来源**: 国防科技大学（博士论文）
- **引用**: 8
- **相关性**: ★★★★★ — 直接对标，星地+相干+信道+信号处理

**CNKI 链接**: https://kns.cnki.net/kcms2/article/abstract?v=t_h3i5Pmq2xqpr47EvvUfqmP18jkbVLHBfTzWgSPir6MjESBkErE6twqzBo27LB2v9yb1UWE6cT2mNQeY-cZ5Fr_SI9agSil22IMMUUAeEAfcvtW1BquDBm5pU9hPHLsw7tyaDNx-BzXu3JC1R_aZdpMKmabLYRDwUL_LhJbLAXPRIPcAmyNvPRWid5oErL4

**待补充**：应下载并阅读此博士论文的目录结构，看其如何切分"信号处理"章节。

#### 12. 闫佳欣 (2024) — "面向空间激光通信的实时信号处理算法研究与实现"

- **来源**: 电子科技大学
- **引用**: 2
- **相关性**: ★★★★☆ — 实时信号处理

#### 13. 管路阳 (2024) — "空间激光通信系统中高阶调制信号损伤抑制算法研究"

- **来源**: 青岛大学
- **相关性**: ★★★☆☆ — 高阶调制损伤抑制

#### 14. 李发明 (2022) — "基于时间分集与FEC编码技术的可变速率相干激光通信系统设计"

- **来源**: 华中科技大学
- **相关性**: ★★★★☆ — 分集+编码+相干

#### 15. "空间相干激光通信技术" (2022/2023) — 孙建锋等

- **来源**: 人民邮电出版社（专著）
- **引用**: 4
- **相关性**: ★★★★☆ — 专著级别的技术综述

---

## 综合分析

### 核心发现：所有综述的共识

**载波同步是顶层方向，不是任何更大方向的子集。**

在所有找到的综述中，载波同步的定位如下：

| 综述 | 载波同步的层级 | 与其他方向的关系 |
|------|---------------|-----------------|
| Valjus 2025 (DLR) | **顶层**（与定时恢复、均衡并列） | 三大子系统之一 |
| Kaushal 2017 | **非独立方向**（归入"多普勒频移"子项） | 物理层缓解技术 9 类中无"同步" |
| Savory 2009 | **顶层**（与 CD 补偿、偏振恢复、FEC 并列） | fiber DSP chain 中的一个模块 |
| CNKI 张岱 2018 | **待确认**（论文标题含"信号处理"） | 需下载确认章节结构 |

**不存在比"载波同步"更大的、包含它作为子集的研究主题。** 载波同步与定时恢复、信道均衡、FEC 是同一层级的并列方向。

### 不同综述的切分维度对比

综述论文对信号处理方向有多种切分方式：

#### 维度 1：按 DSP 处理模块（Valjus 2025, Savory 2009）

这是最自然的切分——按信号在接收端经过的处理步骤：

```
接收信号 → 定时恢复 → 载波同步（频偏+相位）→ 均衡 → FEC → 输出
```

每个模块是一个独立的研究方向。**优点**：清晰、不重叠。**缺点**：各模块间的关系和联合优化不好处理。

#### 维度 2：按挑战类型（Kaushal 2017）

```
挑战（大气效应、平台效应）→ 缓解技术（调制、编码、分集、AO...）
```

**优点**：问题驱动，每类缓解技术直接对应一类挑战。**缺点**：载波同步不作为独立缓解技术。

#### 维度 3：按设计层次（本文推荐）

```
分析方法/准则 → 参数设计方法 → 联合处理方法
```

**优点**：每个层次都能容纳不同模块的工作，天然支持扩展。**缺点**：不如按模块切分那么直观。

### 与当前论文的关系

当前论文 Ch4 的内容分布：

| 当前章节 | 内容 | 对应 Valjus 2025 的模块 |
|---------|------|------------------------|
| §4.2 载波同步方法概述 | VV/BPS/DPLL 算法 | Section 4: Carrier Phase Estimation |
| §4.3 湍流下载波同步性能分析 | 方法对比+参数敏感性 | Section 4.2: Analysis |
| §4.4.1 环路参数解析设计 | ω_n 设计公式 | Section 4/5: Parameter design (开放问题) |
| §4.4.2 多源相位噪声联合补偿 | 联合补偿 | Section 4+5: Joint (开放问题) |
| §4.4.3 编码辅助载波恢复 | code-aided | 跨 Section 4 + FEC (开放问题) |

可以看到，当前内容基本只覆盖了 Valjus 2025 的 Section 4（载波相位估计），Section 3（定时恢复）和 Section 6（自适应均衡）完全没有涉及。

---

## 推荐方案：Route A（设计层次切分）

### 决策依据

1. **文献不支持"载波同步是某个更大方向的子集"**——所有综述都将载波同步视为顶层模块
2. **Route B（扩展到多模块）改动太大**——当前工作全部是载波同步，扩展到均衡/定时需要新的仿真和分析
3. **Route A 保持载波同步核心**，但将三个方向从"具体方法"升级为"设计层次"
4. **Route A 天然支持未来扩展**——"联合处理"方向可以容纳任何跨模块工作

### Route A：三个设计层次

| 方向 | 定位 | 一句话描述 | 当前已有内容 | 未来可装什么 |
|------|------|-----------|-------------|-------------|
| ① 分析方法与设计准则 | "怎么评价" | 建立湍流条件下同步方法的系统性分析框架和选择准则 | §4.3 方法对比+参数敏感性+C4-01~09 | 任何新方法的湍流性能评估；指标扩展 |
| ② 参数设计方法 | "怎么配" | 研究湍流条件下的参数解析设计方法 | ω_n 设计公式(C4-11 P_frame模型)、ζ扫参 | VV 窗口长度设计、导频方案设计、其他同步参数配置 |
| ③ 联合处理方法探索 | "怎么跨模块协作" | 拟探索跨模块/跨功能的信号处理联合方案 | 多源相位噪声补偿、编码辅助恢复 | 均衡-同步联合、导频-估计联合、迭代检测-译码等任何跨模块工作 |

### 与旧方案的区别

| 旧方案 | 问题 | 新方案 | 改进 |
|--------|------|--------|------|
| 环路参数解析设计 | 只是方向②的一个子项 | ② 参数设计方法 | 层级提升，可容纳更多参数设计工作 |
| 多源相位噪声联合补偿 | 只是方向③的一个具体方法 | ③ 联合处理方法 | 从"具体方法"升级为"设计理念" |
| 编码辅助载波恢复 | 也是方向③的一个具体方法 | 合并到③ | 不单独列出，作为③的实例之一 |

### 与 Route B 的兼容性

Route A 的方向③"联合处理方法"天然覆盖 Route B 的所有内容：

| Route B 内容 | 在 Route A 中的归属 |
|-------------|-------------------|
| 信道均衡方法 | ③ 联合处理（均衡-同步联合） |
| 定时恢复方法 | ② 参数设计（定时参数配置）或 ③ 联合处理 |
| 差错控制编码 | ③ 联合处理（编码辅助信号处理） |
| FEC 优化 | ③ 联合处理（检测-译码联合） |
| 导频辅助处理 | ③ 联合处理（估计-同步联合） |

**结论：选择 Route A 不限制未来扩展到 Route B 的任何内容。**

### PPT 标签建议（5-8 字）

| 方向 | 标签选项 |
|------|---------|
| ① | 性能分析方法 / 分析框架与准则 / 方法分析与选择 |
| ② | 参数设计方法 / 湍流参数设计 / 解析设计方法 |
| ③ | 联合处理方法 / 跨模块联合处理 / 跨模块协同方法 |

### 与 §1.2 文献综述的衔接

§1.2.2 "湍流下相干接收端信号处理研究现状"（已更新为 v5 标题）的文献铺垫应为：
- 引用 Valjus 2025 建立三子系统框架（定时/载波/均衡）
- 说明本文聚焦载波同步子系统，但探索方向采用设计层次划分
- 引用 Paillier 2020（DPLL 星地）、Kaushal 2017（挑战-缓解框架）支撑分析框架
- 引用 Zhang 2018 NUDT 博士论文（星地相干+信号处理）补充中文文献

### 不变量（动任何一条必须重新讨论）

1. 载波同步是 Ch4 的核心内容，不可削弱
2. 三个方向必须有清晰的层次递进关系（分析→设计→联合）
3. 方向③的边界最宽，不能写得比①②窄
4. 不使用禁词（自适应/优化/增强/首次/填补空白）——"联合处理"用"探索/研究"，不用"优化"
5. 聚焦星地场景（不是星间、不是光纤）

---

## 待后续对话补充的工作

### 必须补充

1. **下载张岱 2018 博士论文**（国防科大），提取其"信号处理"章节的目录结构——这是最直接对标的中文论文
2. **下载孙建锋专著**"空间相干激光通信技术"，看其信号处理章节如何组织
3. **获取 2022 JLT 236 引用综述全文**——子 agent 两次因 API 过载失败，需要重试
4. **确认 §1.2.2 文献铺垫段落**如何引用上述综述

### 建议补充

5. 下载 "Optical communications in turbulence: a tutorial" (2023, doi:10.1117/1.OE.63.4.041207)——湍流下光通信教程
6. 检查 "Review on Modulation Formats and Channel Coding in FSO" (2026, doi:10.1109/JLT.2026.3664749)——最新的 FSO 调制+编码综述
7. 搜索更多中文博士论文的信号处理章节结构（国防科大、电子科大、哈工大是主要来源）

### 影响 PROMPT-013/016/017 的工作

本调研的输出将影响：
- `毕设/innovation-points.md` IP2 的"包括但不限于"后三个方向 → 按新方案重写
- `毕设/thesis-status.md` Ch4 §4.4 的三个子节标题 → 按新方案更新
- `毕设/开题报告/draft-s1.2-v5.md` §1.2.2 L3 的文献铺垫段落 → 引用新找到的综述
- `毕设/开题PPT/ppt-content-decisions.md` 技术路线图的分支标签 → 按新标签更新

---

## 附录：Valjus 2025 论文的关键数据

### 引用统计

- 发表于 2025 年，International Journal of Satellite Communications and Networking
- DLR（德国航空航天中心）出品，Open Access CC BY 4.0
- 引用数 9（截至检索时）

### 摘要原文

> Coherent optical satellite links enable high-throughput communication and high accuracy ranging to and between satellites. Due to the ever-increasing demand for throughput, wavelength division multiplexing of polarization multiplexed optical signals is being considered as a solution to provide high data rate communication. In this article, the signal processing of coherent optical satellite receivers is investigated. The signal processing of coherent optical satellite receivers can be divided into three key subsystems: timing recovery, carrier synchronization, and equalization. We review state-of-the-art algorithms for each subsystem, compare them by means of simulations in four representative satellite scenarios, and discuss their interactions.

### 关键引文（可用于 §1.2）

1. "The signal processing of coherent optical satellite receivers can be divided into three key subsystems: timing recovery, carrier synchronization, and equalization."
   → 支撑"三子系统"框架

2. "it remains to be proven experimentally that these digital timing recovery algorithms can remain stable over long periods of time in real atmospheric channels"
   → 支撑定时恢复在湍流下的开放问题

3. "dynamically adjusting the number of symbols used for phase estimation should improve system performance... Further research is necessary to identify practical methods"
   → 支撑动态窗口调整的必要性

4. "the probability of the equalizer diverging to a local optimum during deep fades has not been analyzed"
   → 支撑均衡器在湍流下的开放问题

5. "evaluating the complete DSP chain under realistic conditions is critical"
   → 支撑联合评估的必要性

6. "Data-aided algorithms are generally preferred in OSL due to their fast acquisition, low SNR performance, and low complexity"
   → 支撑数据辅助方法的优势

---

## 方向标签统一更新——交接文本（2026-06-03）

Route A 已确认，方向标签已在 `innovation-points.md` 和 `thesis-status.md` 中更新。以下为其他对话需要传播的统一标签和具体指令。

### 统一方向标签（Route A）

§4.4 三个子方向按**设计层次**切分，替换旧的三个具体方法：

| 编号 | 旧方向 | 新方向 | 一句话定位 |
|------|--------|--------|-----------|
| 4.4.1 | 环路参数解析设计方法 | **同步方法分析与设计准则** | 怎么评价 |
| 4.4.2 | 多源相位噪声联合补偿 | **参数设计方法** | 怎么配 |
| 4.4.3 | 编码辅助载波恢复策略 | **跨模块联合处理方法探索** | 怎么跨模块协作 |

§4.4 总标题：~~面向湍流条件的信号处理优化方案~~ → **面向湍流条件的信号处理方法探索**

### 禁词提醒

- 不使用：自适应、优化、增强、首次、填补空白
- 联合处理方向用"探索/研究"，不用"优化"
- 旧方向名（环路参数解析设计、多源相位噪声联合补偿、编码辅助载波恢复）不再作为独立方向出现，具体方法可作为③的实例提及

### IP2 统一段落（已更新）

> 拟研究 Gamma-Gamma 湍流下相干 FSO 同步技术，建立系统性性能分析框架并给出同步方法选择与参数设计准则；在此基础上，**分三个设计层次展开：①分析方法与设计准则，②参数设计方法，③跨模块联合处理方法探索。**

### 各对话具体任务

#### PROMPT-016 / §1.2 对话

**文件**: `毕设/开题报告/draft-s1.2-v5.md`

修改 §1.2.2 L3 段落（当前描述旧三个方向）：
- 将"环路参数解析设计/多源相位噪声联合补偿/编码辅助载波恢复"替换为三个设计层次
- §1.2.3 "现有研究不足与本文切入点"中对齐新标签
- 引用 Valjus 2025 建立三子系统框架（定时/载波/均衡），说明本文聚焦载波同步，探索方向按设计层次划分

#### PROMPT-013 / 研究方案对话

**文件**: `毕设/开题报告/03-研究方案.md`

修改 §3.4.5 三个子节：
- §3.4.5.1 标题：~~环路参数解析设计~~ → **同步方法分析与设计准则**
- §3.4.5.2 标题：~~多源相位噪声联合补偿~~ → **参数设计方法**
- §3.4.5.3 标题：~~编码辅助载波恢复~~ → **跨模块联合处理方法探索**
- 内容适配：旧的具体方法描述可保留为③的实例，但方向定位要升级为设计层次

#### PPT 对话

**文件**: `毕设/开题PPT/ppt-content-decisions.md`

技术路线图分支标签更新：
- 分支 1：**分析方法与准则**（或"性能分析与准则"）
- 分支 2：**参数设计方法**
- 分支 3：**联合处理方法探索**（或"跨模块协同方法"）

### 文献支撑（§1.2 可引用）

| 综述 | 用途 | 引文 |
|------|------|------|
| Valjus 2025 (DLR) | 三子系统框架(定时/载波/均衡) + 7个开放问题 | Valjus & Wolf, IJSCN 2025, doi:10.1002/sat.1553 |
| Kaushal 2017 | 挑战-缓解框架(1480c) | Kaushal et al., IEEE COMST 2017 |
| Paillier 2020 | 星地相干+DPLL | Paillier et al., JLT 2020 |
| 张岱 2018 | 中文直接对标(国防科大博士) | 待下载 |
