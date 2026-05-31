# Handoff: 文献深度精读与补充检索（全论文 150 条目标）

> 来源: S016+S017+本对话 | 交接目标: 多轮对话完成文献精读、补充检索、组织整理，为 thesis-platform 绪论写作提供完整材料包
> 文件名: H008-literature-deep-reading-handoff.md

## 已完成边界

1. 论文方向已确定：星地激光通信信号处理关键技术研究（QPSK相干检测 + Gamma-Gamma湍流 + LEO星地链路）
2. 论文框架已写：Ch1 绪论完整稿（~5000字）+ Ch2-6 章节大纲，存于 `毕设/写作材料/thesis-framework.md`
3. 参考文献初步收集：87 篇列目（72 去重），70 条 bib 条目
4. 4 个公式提取文件已完成：Ch2/Ch3Ch4/Ch5 公式 + 符号表
5. 5 篇参考学位论文已下载转 markdown：张岱/闫佳欣/王锋/汤昕宇/陈欢
6. MVE 仿真代码已完成：sim_prototype.py / sim_direction_a.py / sim_ch3_precomp.py / sim_cascade_robustness.py
7. 4 个推导提示词已创建：PROMPT-001 至 PROMPT-004（Ch2-Ch5 原创公式推导）
8. thesis-platform 写作工具已验证：extract.py（风格提取）+ rewrite.py（改写管线），位于 `/home/zzt/code/thesis-platform/`

## 不要做什么

- **不要直接开始写绪论**——文献深度和数量都不够，现在写出来会很浅
- **不要用现有草稿直接跑 rewrite 管线**——原始素材质量不足，改写管线无法补事实
- **不要只补数量不补深度**——列出但不读的论文没有引用价值
- **不要一次对话试图完成所有工作**——这是一个 4-6 轮对话的大任务
- **不要凭记忆或 AI 猜测论文内容**——每篇引用必须有阅读证据支撑
- **不要忽略中文文献**——中文学位论文在中文硕论引用中占重要比例
- **不要跳过子方向缺口分析**——先分析缺什么再检索，不要盲目搜

## 核心问题：文献严重不足

### 数量差距

| 章 | 现有（去重） | 目标 | 缺口 | 说明 |
|---|------------|------|------|------|
| Ch1 绪论 | 25 | **60** | **+35** | 综述章，需全面覆盖所有子方向 |
| Ch2 系统与信道模型 | 10 | **20** | **+10** | GG模型、相干检测、链路预算、大气衰减 |
| Ch3 信道估计+级联 | 25 | **35** | **+10** | LS/MMSE/Kalman/DL + 预补偿 + 级联灵敏度 |
| Ch4 载波同步 | 18 | **30** | **+12** | FOE/CPR/DPLL + 多普勒 + 湍流自适应 |
| Ch5 FPGA | 9 | **18** | **+9** | FPGA实现、资源优化、DSP链 |
| 中文文献专项 | ~15 | **40-50** | **+30** | 独立于英文，需CNKI系统性补充 |
| **合计** | **~72** | **~150** | **~78** | 需新增约 80 篇独立论文 |

### 深度差距

当前 87 篇列目论文的阅读状态：

| 状态 | 数量 | 占比 | 含义 |
|------|------|------|------|
| ✅ 全文精读 | 23 | 26% | 有量化数据可直接引用 |
| ⬚ 有 abstract/摘要 | 45 | 52% | 知道核心结论但缺精确参数 |
| ❌ 仅检索条目 | 19 | 22% | 需获取全文确认内容 |

**目标：全文精读率从 26% 提升到 >70%**（即 105+ 篇有阅读笔记）。

### 组织差距

对比上一轮（thesis-final-review）的文献组织水平：

| 维度 | thesis-final-review | 本轮现状 | 差距 |
|------|-------------------|---------|------|
| 逐篇精读笔记 | R001(40K) + S006-S007 详细提取 | 无 | 极大 |
| 中文文献补充 | H005 专门补了 60 篇中文 | ~15 篇中文，零散 | 极大 |
| 分章文献分析 | S013(congestion routing full review) 等 | 仅 material-chapter-literature.md 列表 | 大 |
| 交叉引用校验 | S014 final consistency check | 无 | 大 |
| 总参考数 | ~130 篇（旧方向） | 72 篇 | 大 |

**结论：本轮文献工作量和组织水平远不如上一轮，到处是漏洞。必须系统补齐。**

## 必读

### Tier 1：理解当前状态（必读）

1. **本文件** — 全量上下文
2. `毕设/写作材料/material-chapter-literature.md` — 当前 87 篇文献清单，含阅读状态标记
3. `毕设/写作材料/references.bib` — 70 条 bib 条目
4. `毕设/写作材料/thesis-framework.md` — 论文框架（Ch1 完整稿 + Ch2-6 大纲）
5. `projects/thesis-fso/literature_notes.md` — 文献调研笔记（检索阶段完成，精读未开始）

### Tier 2：理解论文内容（按需）

6. `毕设/写作材料/formulas-ch2-system-model.md` — Ch2 公式提取（494行，36条公式）
7. `毕设/写作材料/formulas-ch3ch4-sync.md` — Ch3/Ch4 公式提取（521行，28条公式）
8. `毕设/写作材料/formulas-ch5-fpga.md` — Ch5 FPGA 公式提取（340行）
9. `毕设/写作材料/symbol-conventions.md` — 符号表（~100符号，14类）
10. `毕设/写作材料/material-section-content-cards.md` — 64 张节内容卡片
11. `毕设/写作材料/material-chapter-literature.md` — 分章文献清单
12. `毕设/写作材料/material-fso-sentence-examples.md` — FSO 句级范例

### Tier 3：参考论文全文（按需读取）

13. `projects/thesis-fso/cnki-downloads/星地相干激光通信大气信道特征及信号处理技术研究_张岱.md` — 332K，国防科大博士
14. `projects/thesis-fso/cnki-downloads/面向空间激光通信的实时信号处理算法研究与实现_闫佳欣.md` — 130K，电子科大硕士
15. `projects/thesis-fso/cnki-downloads/空间激光通信系统的调制与接收技术研究_王锋.md` — 270K
16. `.sessions/thesis-direction-pivot/北理工-夏兆宇-专硕学位论文【明审】(1).md` — 4799行
17. `projects/thesis-fso/cnki-downloads/汤昕宇_converted.md` — 2.9K（转换不完整）
18. `projects/thesis-fso/cnki-downloads/陈欢_converted.md` — 2.3K（转换不完整）

### Tier 4：已精读的英文论文 content.md

19. `papers/doi/10.1109_jlt.2023.3281082/content.md` — Fernandes 2023 (LEO多普勒数字补偿)
20. `papers/downloads/2026-05-29/1-s2.0-S0030401823000573-main.md` — Liu 2023 (VV/BPS星地载波恢复)
21. `papers/arxiv/1911.11851/content.md` — Paillier 2020 (星地相干AO+DPLL)
22. 其余 `papers/` 下已下载论文（见 `papers/downloads/` 和 `papers/doi/`）

### Tier 5：推导提示词（后续推导工作用）

23. `.sessions/thesis-direction-pivot/PROMPT-001-ch2-derivations.md` — Ch2 推导
24. `.sessions/thesis-direction-pivot/PROMPT-002-ch3-derivations.md` — Ch3 推导
25. `.sessions/thesis-direction-pivot/PROMPT-003-ch4-derivations.md` — Ch4 推导（最重要）
26. `.sessions/thesis-direction-pivot/PROMPT-004-ch5-derivations.md` — Ch5 推导

## 论文结构与各章内容概述

### 最终章节结构（导师确认 v4）

```
第一章 绪论
  1.1 研究背景与意义
  1.2 国内外研究现状
    1.2.1 大气湍流信道估计研究现状
    1.2.2 低轨卫星激光通信载波同步研究现状
    1.2.3 现有研究不足与本文切入点
  1.3 论文主要研究内容与章节安排
  1.4 本文创新点

第二章 星地激光通信系统与信道模型（含信道估计）
  2.2 星地激光通信系统模型
    2.2.1 相干检测系统组成
    2.2.2 QPSK信号模型
    2.2.3 接收端噪声模型与信噪比定义
  2.3 大气信道传输特性
    2.3.1 大气衰减
    2.3.2 大气湍流效应与Gamma-Gamma分布模型
    2.3.3 Gamma-Gamma模型参数确定
  2.4 星地链路预算分析
  2.5 本章小结

第三章 大气湍流信道估计技术
  3.2 湍流信道估计问题建模
  3.3 信道估计方法（LS/MMSE/Kalman/DL）
  3.4 估计精度对下游信号处理的影响分析
    3.4.1 估计误差对载波同步性能的影响
    3.4.2 估计误差对功率预补偿可行性的影响
    3.4.3 下游模块灵敏度差异分析
  3.5 仿真结果
  3.6 本章小结

第四章 低轨星地载波同步算法
  4.2 载波同步系统模型（Doppler+湍流+联合模型）
  4.3 湍流自适应频偏估计算法
  4.4 湍流自适应载波相位恢复算法
  4.5 仿真结果
  4.6 本章小结

第五章 接收端信号处理链FPGA设计与实现
  5.2 FPGA开发平台与设计流程
  5.3 自适应载波同步算法的FPGA实现
    5.3.1 系统总体架构设计
    5.3.2 FFT频偏估计模块实现
    5.3.3 载波相位恢复模块实现
    5.3.4 DPLL环路模块实现
  5.4 仿真验证与资源评估
  5.5 本章小结

第六章 总结与展望
```

### 各章核心贡献一句话

- **Ch1**：综述背景 + 三个研究空白 + 三个创新点
- **Ch2**：统一模型基础（QPSK相干检测 + GG湍流 + 链路预算），含信道估计方法对比
- **Ch3**：核心创新一——级联灵敏度差异（载波同步鲁棒 vs 预补偿脆弱），NMSE→BER定量映射
- **Ch4**：核心创新二——三个湍流自适应公式（$N_\text{opt} \propto h^{-4}$、$M_\text{opt} \propto h^{-2/5}$、$B_\text{L,opt} \propto h^1$）
- **Ch5**：核心创新三——自适应算法 FPGA 实现验证（定点化+资源+时序）
- **Ch6**：总结

### 三个核心创新点

1. **级联灵敏度差异分析**：首次定量揭示载波同步对估计误差鲁棒、功率预补偿对估计误差脆弱（NMSE≥-10dB 时载波同步 6/6 PASS，预补偿全 FAIL）
2. **湍流自适应载波同步**：三个解析公式，三种 h 依赖形态（阈值/平滑/线性）
3. **FPGA 实现验证**：自适应算法硬件可行性

## 各章文献子方向分析与缺口

### Ch1 绪论（目标 60 篇）

绪论是综述章，需要覆盖所有子方向。按节分解：

#### 1.1 研究背景与意义（目标 12-15 篇）

需要的子方向和典型引用：

| 子方向 | 现有 | 需要 | 缺口 | 典型文献类型 |
|--------|------|------|------|-------------|
| LEO 星座发展（Starlink/OneWeb/中国星座） | 1 | 3-4 | +2-3 | 近期综述或新闻性文献 |
| FSO 通信优势（带宽/抗干扰/无需授权） | 2 | 3 | +1 | FSO综述（Khalighi 2014已有） |
| 星地激光通信工程验证（LCRD/EDRS/中国试验） | 0 | 3-4 | **+3-4** | NASA/ESA项目论文、中国试验报告 |
| 大气湍流对FSO的影响（20dB SNR→BER崩溃） | 1 | 2 | +1 | 湍流影响定量分析 |
| 信号处理作为技术路径（vs 自适应光学） | 0 | 1-2 | +1-2 | AO vs DSP 对比文献 |

**关键缺口**：星地激光通信工程验证项目（LCRD/EDRS）零引用，这是一个明显的遗漏。

#### 1.2.1 信道估计研究现状（目标 15 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| 传统FSO信道估计（LS/MMSE/Kalman） | 3 | 5-6 | +2-3 | 需补充Kalman在FSO中的应用 |
| DL信道估计（DNN/CNN/RNN/VAE） | 5 | 7-8 | +2-3 | 已有Amirabadi/Elfiky/Mohammed等 |
| FSO信道建模与参数估计（α,β,Cn²） | 2 | 3 | +1 | Kim 2025已列，需补充 |
| 信道估计精度对系统性能的影响 | 1 | 2-3 | +1-2 | 级联影响是本文核心，需更多支撑 |
| 下行链路估计方法（含导频设计） | 0 | 1-2 | +1-2 | 导频辅助估计的文献 |

#### 1.2.2 载波同步研究现状（目标 15 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| FFT频偏估计（光纤经典→FSO迁移） | 3 | 4-5 | +1-2 | 需补充FFT-FOE理论基础文献 |
| VV/BPS载波相位恢复 | 4 | 5-6 | +1-2 | VV1983经典、Neves 2023综述已有 |
| LEO多普勒补偿（星历预补偿+数字补偿） | 5 | 5 | 0 | Fernandes/Zhao/Wang覆盖较好 |
| DPLL在光通信中的应用 | 2 | 3-4 | +1-2 | 需补充DPLL理论文献 |
| 湍流对载波同步的影响 | 0 | 1-2 | **+1-2** | 关键缺口！本文核心动机 |
| 自适应参数调整（窗口/带宽自适应） | 0 | 1-2 | **+1-2** | 另一关键缺口 |

#### 1.2.3 研究不足与切入点（目标 5-8 篇）

| 子方向 | 现有 | 需要 | 缺口 |
|--------|------|------|------|
| 级联灵敏度/端到端分析 | 2 | 3 | +1 |
| 功率预补偿极限分析 | 2 | 2 | 0 |
| 湍流自适应载波同步 | 0 | 2-3 | **+2-3** |

#### 1.3 章节安排（无需独立文献）
#### 1.4 创新点（无需独立文献，引用Ch3-Ch5支撑文献）

### Ch2 系统与信道模型（目标 20 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| 相干检测原理（外差/零差混频） | 1 | 3-4 | +2-3 | 经典光学通信教材/综述 |
| QPSK信号模型 | 0 | 2-3 | **+2-3** | 数字通信教材 |
| 噪声模型（热噪声/散粒噪声/LO噪声） | 1 | 2-3 | +1-2 | 光接收机噪声理论 |
| Gamma-Gamma 分布 | 3 | 4-5 | +1-2 | 需补充原始论文（Al-Habash 2001） |
| 大气衰减（Beer-Lambert） | 0 | 2 | **+2** | 基础公式来源 |
| Rytov方差/Cn²模型 | 1 | 2-3 | +1-2 | Kolmogorov湍流理论 |
| 链路预算 | 2 | 3-4 | +1-2 | LEO星地链路预算文献 |
| 信道估计方法（LS/MMSE/Kalman/DL） | 3 | 5-6 | +2-3 | 与Ch3重叠，但Ch2侧重模型 |

**关键缺口**：QPSK信号模型（0篇）、大气衰减基础公式（0篇）、GG分布原始论文

### Ch3 信道估计+级联（目标 35 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| LS估计（FSO场景） | 1 | 3 | +2 | 需FSO特化文献 |
| MMSE估计（FSO场景） | 1 | 3 | +2 | 同上 |
| Kalman滤波（时变FSO信道） | 1 | 2-3 | +1-2 | AR模型+卡尔曼 |
| DL信道估计（CNN/RNN/MLP/VAE） | 6 | 8-9 | +2-3 | 已有较好覆盖 |
| 功率预补偿/自适应功率 | 5 | 6 | +1 | Brandao/Safi/Correia/Nguyen |
| 级联灵敏度分析（估计→下游） | 2 | 3-4 | +1-2 | Safi 2019是唯一近似的 |
| 预补偿失效分析 | 2 | 2-3 | +0-1 | 反馈延迟+估计噪声 |

### Ch4 载波同步（目标 30 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| FFT频偏估计理论与实现 | 3 | 5-6 | +2-3 | 需补充经典FOE论文 |
| VV算法（经典+改进） | 2 | 4-5 | +2-3 | VV 1983经典论文+改进 |
| BPS算法 | 1 | 2-3 | +1-2 | 需补充BPS原始论文 |
| Pilot-aided CPR | 0 | 2-3 | **+2-3** | 完全缺失 |
| LEO Doppler补偿 | 5 | 5 | 0 | 覆盖较好 |
| DPLL理论 | 2 | 4 | +2 | 二阶环理论+光通信应用 |
| 载波同步性能分析（SNR/BER关系） | 2 | 3-4 | +1-2 | |
| 湍流对同步的影响 | 0 | 2 | **+2** | 关键缺口 |
| 自适应算法（参数自适应调整） | 0 | 2 | **+2** | 关键缺口 |

**关键缺口**：Pilot-aided CPR（0篇）、湍流对同步影响（0篇）、自适应参数调整（0篇）

### Ch5 FPGA（目标 18 篇）

| 子方向 | 现有 | 需要 | 缺口 | 说明 |
|--------|------|------|------|------|
| 星地/FSO相关FPGA实现 | 2 | 4-5 | +2-3 | Wang 2025 + 闫佳欣论文 |
| 光通信DSP全链路FPGA | 4 | 5-6 | +1-2 | DP-QPSK/QAM接收机 |
| 定时恢复FPGA | 3 | 3-4 | +0-1 | Gardner等 |
| CPR硬件实现 | 2 | 3 | +1 | VV/BPS硬件 |
| FPGA资源优化/定点化 | 0 | 2-3 | **+2-3** | 完全缺失 |
| 星地相干光链路DSP综述 | 1 | 2 | +1 | |

**关键缺口**：FPGA定点化/资源优化文献完全缺失

### 中文文献专项（目标 40-50 篇）

现有中文文献约 15 篇，分布在 bib 中的 `caominghua2020`、`sunjing2018`、`lixueliang2018`、`lixiaoyan2017`、`hanliqiang2011`、`madongtang2004`、`zhangdai2018`、`yanxu2022`、`zhaoyuanfan2024`、`guanhaijun2019`、`xuwenjing2021`、`zhuyong2003`、`gaoyue2023`、`wuying2026`、`zhouhaijun2020`、`tongxin2020` 等。

需要补充的中文文献子方向：

| 子方向 | 现有 | 需要 | 缺口 | 搜索关键词建议 |
|--------|------|------|------|---------------|
| 星地激光通信系统/综述 | 2 | 5-6 | +3-4 | 星地激光通信、空间光通信 |
| 相干检测技术 | 2 | 5 | +3 | 相干光通信、相干检测、零差/外差 |
| 大气湍流信道建模 | 3 | 6-7 | +3-4 | 大气湍流、Gamma-Gamma、光强闪烁 |
| 载波同步/相位恢复 | 3 | 6-7 | +3-4 | 载波同步、载波恢复、相位估计 |
| FPGA/DSP实现 | 1 | 4-5 | +3-4 | 光通信FPGA、实时信号处理 |
| 信道估计 | 2 | 4-5 | +2-3 | 光通信信道估计、湍流信道估计 |
| 链路预算/系统设计 | 0 | 3-4 | **+3-4** | 星地链路预算、光学链路设计 |

## 已有材料清单（按文件）

### 写作材料（毕设/写作材料/）

| 文件 | 行数 | 内容 | 质量 |
|------|------|------|------|
| thesis-framework.md | ~500 | Ch1完整稿+Ch2-6大纲 | Ch1可用但需文献支撑升级 |
| references.bib | ~500 | 70条bib | 部分条目缺volume/pages |
| material-chapter-literature.md | ~193 | 87篇分章文献清单+阅读状态 | 目录完整，深度不够 |
| material-section-content-cards.md | ~826 | 64张节内容卡片 | 结构参考，待文献补充后更新 |
| material-fso-sentence-examples.md | ~24K对应 | 21个FSO句级范例 | 写作风格参考 |
| formulas-ch2-system-model.md | 494 | 36条公式+参数表 | 标准公式提取完成 |
| formulas-ch3ch4-sync.md | 521 | 28条公式+交叉验证表 | 部分待推导 |
| formulas-ch5-fpga.md | 340 | FPGA架构+资源表 | 参考数据提取完成 |
| symbol-conventions.md | 236 | ~100符号14类 | 待随写作更新 |

### 参考学位论文（projects/thesis-fso/cnki-downloads/）

| 论文 | 作者 | 学校 | 大小 | 可提取内容 |
|------|------|------|------|-----------|
| 星地相干激光通信大气信道特征及信号处理技术研究 | 张岱(2018) | 国防科大博士 | 332K | 绪论结构+信道模型+信号处理 |
| 面向空间激光通信的实时信号处理算法研究与实现 | 闫佳欣 | 电子科大硕士 | 130K | FPGA实现+资源数据 |
| 空间激光通信系统的调制与接收技术研究 | 王锋 | — | 270K | 调制解调+接收技术 |
| 汤昕宇 | — | — | 2.9K | 转换不完整，目录可参考 |
| 陈欢 | — | — | 2.3K | 转换不完整，目录可参考 |
| 北理工-夏兆宇-专硕学位论文 | 夏兆宇 | 北理工 | 4799行 | 绪论写作模板已提取 |

### 英文论文（papers/）

- `papers/doi/` 下有多篇已精读论文
- `papers/downloads/2026-05-29/` 和 `2026-05-30/` 下有新下载论文
- `papers/arxiv/` 下有约 20 篇 FSO 相关论文
- 共计约 30-40 篇英文论文有 content.md

### 仿真代码（projects/thesis-figures/simulation/）

| 文件 | 内容 | 用途 |
|------|------|------|
| sim_prototype.py | 端到端原型仿真 | GG模型验证+链路参数 |
| sim_direction_a.py | 载波同步MVE（方向A） | 6场景PASS/FAIL数据 |
| sim_ch3_precomp.py | 预补偿MVE | 预补偿失效数据 |
| sim_cascade_robustness.py | 级联鲁棒性 | NMSE vs BER数据 |

### 推导提示词（.sessions/thesis-direction-pivot/）

| 文件 | 内容 | 依赖 |
|------|------|------|
| PROMPT-001-ch2-derivations.md | Ch2: E[1/h²]发散性+链路预算 | 无 |
| PROMPT-002-ch3-derivations.md | Ch3: NMSE→BER级联+预补偿失效证明 | PROMPT-001 |
| PROMPT-003-ch4-derivations.md | Ch4: 三个自适应公式推导（**最重要**） | 001+002 |
| PROMPT-004-ch5-derivations.md | Ch5: 定点化+资源预估+时序约束 | PROMPT-003 |

### thesis-platform 写作工具

位置：`/home/zzt/code/thesis-platform/`

| 组件 | 路径 | 功能 |
|------|------|------|
| extract.py | `src/extract.py` | 从论文提取写作风格规则（YAML输出） |
| rewrite.py | `src/rewrite.py` | 用规则改写草稿（LLM驱动） |
| global-rules.yaml | `output/global-rules.yaml` | 9维度写作规则（D1-D9） |
| extraction-product.yaml | `schema/extraction-product.yaml` | 提取产物schema |

**关键经验**（来自 8cdf0b34 对话）：
- 规则堆砌（dumping all rules）效果差，少量精准规则+few-shot示例更好（M4模式）
- 改写天花板取决于输入素材质量——没有原始材料，prompt 编不出事实
- 正确做法：先手动做出一版高质量文本，再逆向工程提取规则

## 工作计划（4-6 轮对话）

### R1a: Ch1 缺口分析 + 补充检索（1 对话）

**目标**：将 Ch1 文献从 25 篇扩充到 60 篇

**步骤**：
1. 按 1.1/1.2.1/1.2.2/1.2.3 四节的子方向分别盘点缺口（用上面的分析表）
2. 针对每个缺口设计搜索关键词（中英文各一组）
3. 用 `tools/search`（英文，6源）和 `tools/blit --source cnki`（中文）批量检索
4. 筛选、去重、评估引用数和相关性
5. 将新论文加入 material-chapter-literature.md 和 references.bib
6. 尝试下载 TOP 优先级论文

**产出**：
- 更新后的 `material-chapter-literature.md`（Ch1 部分 60 篇）
- 更新后的 `references.bib`（新增 ~35 条）
- 新下载论文的 content.md 文件

**搜索关键词建议（Ch1 各子方向）**：

1.1 背景部分：
- "LEO satellite optical communication" / "space optical communication system"
- "LCRD laser communication relay" / "EDS European data relay"
- "星地激光通信 试验/验证" / "空间光通信 进展"
- "free space optical communication survey 2023 2024 2025"

1.2.1 信道估计：
- "FSO channel estimation Kalman" / "optical wireless channel estimation pilot"
- "大气湍流 信道估计" / "光通信 信道估计 深度学习"
- "GG channel parameter estimation" / "turbulence parameter identification"

1.2.2 载波同步：
- "carrier phase recovery QPSK optical" / "Viterbi Viterbi algorithm"
- "blind phase search coherent detection" / "pilot-aided carrier recovery optical"
- "载波恢复 相干光通信" / "载波同步 QPSK"
- "DPLL optical communication tracking"
- "adaptive carrier synchronization optical"

1.2.3 研究不足：
- "cascade performance estimation synchronization optical"
- "turbulence adaptive carrier recovery"
- "end-to-end signal processing FSO satellite"

### R1b: Ch2-Ch5 缺口分析 + 补充检索（1 对话）

**目标**：各章补到目标数量（Ch2→20, Ch3→35, Ch4→30, Ch5→18）

**步骤**：与 R1a 相同，按章分别检索。特别注意：
- Ch2 缺 QPSK 信号模型、大气衰减基础公式、GG 原始论文
- Ch4 缺 Pilot-aided CPR、湍流对同步影响、自适应参数调整
- Ch5 缺 FPGA 定点化/资源优化

**产出**：各章文献清单更新 + bib 新增 ~32 条

### R1c: 中文文献专项补充（可与 R1a/R1b 并行）

**目标**：中文文献从 ~15 篇扩充到 40-50 篇

**步骤**：
1. 用 `tools/blit --source cnki --doc-type master` 搜索
2. 按子方向分批搜索（见上面中文缺口表的关键词）
3. 下载高相关性硕士/博士论文的摘要页
4. 去重后加入 bib

**产出**：中文文献新增 ~30 条

### R2: 精读批次1 — Ch1 全部 + Ch2 关键论文（1-2 对话）

**目标**：Ch1 的 60 篇全部有阅读笔记，Ch2 的 ~15 篇关键论文精读

**方法**：
- 子 agent 并行精读（每批 3-5 篇，每篇 ≤15min）
- 已有 content.md 的直接读，没有的先用 `tools/blit` 下载
- 每篇提取：方法/结论/关键数据/与本文关系/可引用段落

**产出**：`literature-notes-ch1-ch2.md`

**笔记格式**（每篇）：
```markdown
### [作者年份] 简短标题
- **期刊**: xx, 引用数: xx
- **方法**: 一句话
- **关键结论**: 1-3个带数据
- **与本文关系**: 支撑哪个论点/哪一节
- **可引用数据**: 具体数字/公式
- **阅读状态**: ✅全文 / ⬚摘要 / 引用方式
```

### R3: 精读批次2 — Ch3 + Ch4 关键论文（1-2 对话）

**目标**：Ch3 的 ~30 篇 + Ch4 的 ~25 篇有阅读笔记

**同 R2 方法**

**产出**：`literature-notes-ch3-ch4.md`

### R4: 精读批次3 — Ch5 + 补漏（1 对话）

**目标**：Ch5 的 ~18 篇有阅读笔记 + 回填 R2/R3 遗漏

**产出**：`literature-notes-ch5.md` + 各章补漏

### R5: 整合交付（1 对话）

**目标**：合并所有笔记，准备 thesis-platform 材料包

**步骤**：
1. 合并 literature-notes-ch*.md → `literature-notes-final.md`
2. 更新 `references.bib`（补全 volume/pages/DOI）
3. 从张岱论文提取绪论部分纯文本，作为风格标杆
4. 整理 thesis-framework.md Ch1 草稿
5. 打包到 `/home/zzt/code/thesis-platform/workflows/materials/`

**产出**：
- `literature-notes-final.md` — 150 篇逐篇笔记
- 更新后的 `references.bib` — 150 条
- 绪论风格标杆文本
- Ch1 草稿
- thesis-platform 材料包

## 环境和工具

### Python 环境

```
~/.venvs/torch/bin/python  — torch 2.11+cu126, CUDA RTX 4070
pip 镜像: -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

### 文献检索工具

从项目根目录调用：`cd /mnt/d/code/study/research-protocol && bash tools/search ...`

| 工具 | 用途 | 命令示例 |
|------|------|---------|
| tools/search | 英文文献检索（Semantic Scholar/OpenAlex/arXiv等6源） | `bash tools/search "FSO channel estimation" --limit 20` |
| tools/blit | 论文下载+转换 | `bash tools/blit --doi 10.1109/xxx` |
| tools/blit --source cnki | 中文文献检索+下载 | `bash tools/blit --source cnki "星地激光通信" --doc-type master` |
| tools/convert | PDF转markdown | `bash tools/convert papers/downloads/xxx.pdf` |

### 论文存储路径

| 类型 | 路径 |
|------|------|
| arXiv | `papers/arxiv/{id}/content.md` |
| DOI | `papers/doi/{doi_path}/content.md` |
| 手动下载 | `papers/downloads/{date}/` |
| CNKI学位论文 | `projects/thesis-fso/cnki-downloads/` |

## 导师约束与写作规则

### 导师硬性要求

1. 必须在 Word 模板上直接写
2. 第一节必须叫"研究背景与意义"
3. 所有符号必须定义
4. 参考肖小雨博士论文逐段结构
5. Ch3（大气湍流信道估计）合并到 Ch2
6. 新增 Ch3（TBD，"和另外两章相关但还不确定"），开题答辩后再定
7. 开题答辩前需写好开题报告 Word + PPT

### 当前实际结构（vs 开题报告）

**开题报告用的结构**（导师最新确认）：
```
Ch1 绪论
Ch2 星地激光通信系统与信道模型（含信道估计）
Ch3 TBD（占位，开题中按信道估计内容写）
Ch4 低轨星地载波同步算法
Ch5 接收端信号处理链FPGA设计与实现
Ch6 总结与展望
```

**注意**：开题报告中 Ch3 先按原内容写，标注"具体结构待答辩后确定"。最终结构可能调整。

### 写作质量要求

- 用户对 LLM 生成文本质量不满意（历史反馈："很烂"）
- 用户偏好：先讨论→先澄清→先锁边界→再执行
- facts-first：先列事实和发现，再补总结
- 规范书面中文
- 不先给结论再补事实

## thesis-platform 写作工具使用方法

### 工具位置

`/home/zzt/code/thesis-platform/`

### 输入材料要求

thesis-platform 的 rewrite 管线需要：
1. **原始草稿**（Markdown）— 我们有 thesis-framework.md Ch1
2. **global-rules.yaml** — 已有（9维度写作规则）
3. **风格标杆文本** — 需要从张岱论文提取绪论部分
4. **extraction-product.yaml** — 需要用 extract.py 从标杆论文提取

### 使用流程

```
1. 准备标杆文本（张岱绪论.md）
2. python src/extract.py --input 张岱绪论.md --output output/zhangdai-extraction.yaml
3. python src/rewrite.py --draft thesis-framework-ch1.md --rules output/global-rules.yaml --extraction output/zhangdai-extraction.yaml --output output/ch1-v2.md
```

### 关键经验

- extract.py 用 Gemini Flash 做 LLM 调用（需要 API key）
- rewrite.py 的 v2 prompt（example-driven）比 v1（rule-heavy）好很多
- 最终决定：先手动做一版高质量的，再逆向工程提取规则
- **不要把规则全堆进 prompt**——少量精准规则 + few-shot 示例效果最好

## 已有 bib 的引用覆盖分析

### 当前 bib 中 70 条按主题分布

| 主题 | 数量 | 代表文献 |
|------|------|---------|
| FSO 综述/系统 | 4 | khalighi2014, kaushal2016 |
| 信道估计（传统） | 5 | dabiri2017, kim2025 |
| 信道估计（DL） | 8 | amirabadi2020, elfiky2024, mohammed2026 |
| Gamma-Gamma/湍流建模 | 5 | caominghua2020, sunjing2018, hanliqiang2011 |
| 载波同步/频偏估计 | 10 | fernandes2023, zhao2025, liu2023, paillier2020 |
| CPR（VV/BPS） | 5 | neves2023, hu2025, xuwenjing2021 |
| 多普勒补偿 | 4 | wang2025a, almonacil2020 |
| 功率预补偿/自适应 | 4 | safi2019, brandao2024, correia2026, nguyen2024 |
| FPGA/DSP实现 | 8 | fpga*系列 |
| 均衡 | 3 | almogahed2022, ahmad2026 |
| 链路预算 | 3 | nguyen2024, xu2025 |
| 中文学位论文 | 7 | zhangdai2018等 |
| 时钟/定时恢复 | 4 | alltiming2019, fpgaclock2025 |

### 明显薄弱/缺失的主题

1. **QPSK信号模型基础** — 0 篇
2. **大气衰减（Beer-Lambert）** — 0 篇
3. **相干检测原理（混频/外差/零差）** — 1 篇
4. **星地激光通信工程验证（LCRD/EDRS）** — 0 篇
5. **Pilot-aided CPR** — 0 篇
6. **FPGA定点化/量化** — 0 篇
7. **VV 1983经典论文** — 0 篇
8. **GG分布原始论文（Al-Habash 2001）** — 0 篇
9. **Kolmogorov湍流理论** — 0 篇
10. **DPLL二阶环理论** — 0 篇

这些都是各章的基础引用，必须在补充检索中获取。

## Ch1 现有草稿评估

### 当前草稿位置

`毕设/写作材料/thesis-framework.md` 的"第一章 绪论"部分（约5000字）

### 草稿优点

- 结构完整（1.1-1.4 四节全覆盖）
- 论证链清晰（背景→现状→不足→本文工作）
- 三个创新点表述完整
- 章节安排有递进关系说明
- 已有具体数据引用（如 20dB SNR→BER 0.34）

### 草稿问题

1. **引用密度不足**：~5000字只引用了约15篇文献，60篇目标需要平均每80字一个引用
2. **部分论断缺引用支撑**：如"LCRD项目"、"EDRS系统"、"中国的星地激光通信试验"均无引用
3. **文献综述深度不够**：1.2.1 和 1.2.2 的综述偏概括，缺少具体方法的量化对比数据
4. **研究空白论证可加强**：需要更多"已有方法做了什么、还差什么"的具体证据
5. **中文文献引用极少**：应适当引用中文学位论文和期刊

### 草稿不在本轮修改范围内

草稿在文献精读完成后，交给 thesis-platform 的 rewrite 管线处理。本轮只负责准备充分的材料。

## 接口变更

无代码改动。本轮工作是纯文献检索和阅读。

## 验证阈值

| 验证项 | PASS 标准 | 当前状态 |
|--------|----------|---------|
| 总参考文献数 | ≥150 条 bib | 70 条（❌） |
| Ch1 参考文献数 | ≥60 条 | 25 条（❌） |
| 全文精读率 | ≥70%（105+ 篇有笔记） | 26%（23 篇）（❌） |
| 中文文献占比 | 25-33%（38-50 篇） | ~20%（15 篇）（⚠️） |
| 各章子方向覆盖 | 无零覆盖子方向 | 10+ 子方向零覆盖（❌） |
| 每篇有阅读笔记 | 150 篇各有方法/结论/关系 | 仅 23 篇有（❌） |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 汤昕宇/陈欢论文转换不完整 | 参考论文应有全文可查 | 仅2-3K残缺 | 需要其内容时重转 |
| bib 条目缺 volume/pages | 完整引用格式 | ~20条不完整 | R5 整合时 CrossRef API 补全 |
| Ch3 TBD 结构未定 | 导师说"答辩后再定" | 占位 | 答辩后确认 |
| 肖小雨博士论文未获取 | 导师指定参考对象 | 未获取 | 用户手动提供 |
| 夏师兄开题报告未获取 | 导师指定参考对象 | 未获取 | 用户手动提供 |

## 失败数据附录

### 历史失败经验（thesis-final-review）

- "让LLM写全文"策略失败——11轮修复108个问题
- 规则堆砌（constraint overload）降低输出质量
- 自审自验失效——LLM说自己写的好，用户说很烂

### 本轮已知失败

- 汤昕宇 CAJ→PDF 转换：libjbigdec.so 路径问题已解决，但转换结果仍不完整
- 陈欢论文同上
- 部分 CNKI 论文下载失败（曹明华、孙晶、佟欣后通过 blit 成功）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取本文件全文
- [ ] 已读取 `material-chapter-literature.md` 了解当前文献列表
- [ ] 已读取 `thesis-framework.md` 了解论文框架
- [ ] 已确认工作轮次（R1a/R1b/R1c/R2/R3/R4/R5 中的哪一个）
- [ ] 已检查 `.sessions/_registry.yaml` 中 thesis-direction-pivot 的状态
- [ ] 已确认搜索工具可用（`bash tools/search` 和 `bash tools/blit`）

## 下一轮

**从 R1a 开始**：Ch1 缺口分析 + 补充检索

具体步骤：
1. 读取 `material-chapter-literature.md` 的 Ch1 部分（25 篇清单）
2. 按 1.1/1.2.1/1.2.2/1.2.3 四节子方向分别统计缺口
3. 设计搜索关键词（英文 tools/search + 中文 tools/blit --source cnki）
4. 批量检索，筛选去重
5. 下载高优先级论文
6. 更新 material-chapter-literature.md 和 references.bib

**重要**：先做缺口分析再检索，不要盲目搜。用本文件"各章文献子方向分析与缺口"一节中的分析表作为起点。
