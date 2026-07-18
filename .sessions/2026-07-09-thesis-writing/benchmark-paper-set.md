# 写作对标论文集（CCISP 2026 投稿标尺）

> 2026-07-11 | 来源：S010 §10 三批子 agent 调查（R006 评估 + 库内新筛 + 切换检索）
> 用途：论文所有前置工作（术语/公式/力度/句式/数字呈现）的"对齐领域惯例"标尺来源
> 核验：content.md 存在性已主线亲自核验（FR-26），见下表"库内状态"列

## 接近标准（判定时用）

**必须对上**（不对上没参照意义）：
1. 相干检测（coherent），不是 IM/DD
2. 载波相位/频率同步（CPR / FOE），不是别的 DSP
3. 有湍流场景（turbulence / fading）

**越像越好**（排序用）：
4. 星地链路（satellite/LEO）vs 地面 FSO
5. 估计器对比（pilot vs blind / DA vs NDA）—— 卖点相关
6. 会议论文（conference），体例要对
7. 16-APSK / M-APSK 调制
8. 切换/自适应机制（adaptive / switching）

---

## A. 核心内容对标（5 篇会议，全有 content.md）

这 5 篇是术语/公式/力度/句式的**主要标尺**。

| # | 简称 | venue | 库内路径 | 接近度 | 对标什么 | 库内状态 |
|---|---|---|---|---|---|---|
| 1 | **Johst** | WiSEE 2024 | `papers/doi/10.1109_wisee61249.2024.10850117/` | ★★★★★ | **卖点最贴**：明确对比 blind(CMA) vs data-aided、低 SNR(0dB)稳定性、卫星馈电+湍流+外场 3.2km。DA vs NDA 论证范式、低 SNR 结果呈现 | ✅ 268行 |
| 2 | **Le Bidan** | ICSOS 2023 | `papers/doi/10.1109_icsos59710.2023.10490279/` | ★★★★★ | frame format + pilot(5%开销) + blind CMA 前级 + DA 精载波、低至 -6dB。pilot 开销讨论、DA 段写法、**CCISP 体例最像**（篇幅/结构） | ✅ 872行 |
| 3 | **Panasiewicz** | MWP 2022 | `papers/doi/10.1109_mwp54208.2022.9997784/` | ★★★★ | **唯一三项必须全中**（相干+载波同步+湍流）+ 两鉴相器对比 + M2M4 SNR 估计器。"湍流下比较两估计器"叙事结构、per-block SNR 概念锚 | ✅ 148行 |
| 4 | **OECC-PSC** | OECC/PSC 2025 | `papers/doi/10.23919_oecc-psc62146.2025.11109607/` | ★★★★ | 256-QAM 相位恢复、显式讨论 pilot 频谱代价 vs ML/MAP、CRLB。**DA 频谱代价论证**、性能界(CRLB)写法 | ✅ 150行 |
| 5 | **Paillier** | ICSOS 2019 | `papers/doi/10.1109_icsos45490.2019.8978983/` | ★★★★ | LEO 星地相干 + AO 抑湍流 + DPLL、粗频偏预补偿+精跟踪两级。系统模型、PLL 设计章节句式 | ✅ 258行 |

## B. 切换写法对标（1 会议骨架 + 2 机制参照）

"切换机制这段怎么写"的标尺。库内会议层缺直接对标（见下"缺口"），靠这 3 篇拼。

| # | 简称 | venue | 库内路径 | 对标什么 | 库内状态 |
|---|---|---|---|---|---|
| 6 | **He** | SPIE CSTA 2024 | （DOI 10.1117/12.3036565）| **写法骨架**：SNR 阈值定义切换点 + 中断概率/编码增益图对比固定方案。会议体例 + SNR 判据 + 定量增益 | ⏳ **待用户手动下**（tools/download fail，不 OA）|
| 7 | **Wang** | Opt. Express 2025 | `papers/doi/10.1364_oe.564097/` | **机制最贴**：MSDM 决策指标驱动 SSD/MSD 检测器切换，与 per-block SNR 驱动 DA/NDA 几乎同构 | ✅ 428行 |
| 8 | **Xu** | PTL 2026 | （DOI 10.1109/LPT.2026.3676909）| **迟滞机制**：双阈值迟滞防抖动（BPSK↔QPSK 切换）。切换判据描述可借鉴 | ⏳ **待用户手动下**（IEEE Xplore document/11454624/，不 OA）|

**注**：He 和 Xu 的写法要点子 agent 已从 abstract 提炼（见 S010 §10"三个写法启发"），不依赖全文。待补全文是"写切换段时如需细节再查"，不阻塞前置工作。

## C. 技术源头（3 篇，引文献用）

不精读，作理论/方法引用源头。

| # | 简称 | venue | 库内路径 | 角色 | 库内状态 |
|---|---|---|---|---|---|
| 9 | **B11** | PTL 2025 | `papers/doi/10.1109_lpt.2024.3523478/` | **方法源头**：NDA-ML + M-APSK + FSO + CRLB，最强技术对标。NDA 段写法 + 性能界 | ✅ |
| 10 | **V&V** | IEEE TIT 1983 | （DOI 10.1109/TIT.1983.1056713）| **理论源头**：Mth-power / squaring loss 祖师爷。squaring loss 引用 | ❌ 不在库（引文献即可，不需全文）|
| 11 | **sat.1553** | Int. J. Sat. Comm. 2025 | `papers/doi/10.1002_sat.1553/` | **综述/分类**：相干光卫星链路 DSP 综述，术语/分类框架、引文骨架 | ✅ |

## D. 句式补充

| # | 简称 | venue | 库内路径 | 角色 | 库内状态 |
|---|---|---|---|---|---|
| 12 | **Pech** | ICSOS 2025 | `papers/doi/10.1109_ICSOS66026.2025.11443174/` | 接收机架构 + 同步链描述句式（Z-transform ODPLL）| ✅ |

---

## 从 R006 换掉的（技术偏离）

R006 原 8 篇里这 3 篇技术内容偏离，不再作内容对标（句式库 writing-patterns-conference.md 如已提取仍可用，但不作内容参照）：

| 简称 | 偏离原因 |
|---|---|
| OECC 2024（10.1109/10975630）| 数据中心 DSP-free 模拟 Costas 环，场景方法双偏 |
| APCCAS 2022（10.1109/10090345）| FPGA 硬件实现 BPS-CPR，我们不做硬件 |
| ICUMT 2015（10.1109/7382400）| 星间真空 OPLL 理论分析，无大气湍流，BPSK |

---

## 缺口（诚实记录，影响写作策略）

三次独立调查（R006 评估 + 库内新筛 + 切换检索）都指向同一组缺口：

1. **没有"DA(pilot) vs NDA(Mth-power) 直接 BER 对比 + 基于 SNR 切换"的会议论文** —— 我们卖点。最接近的 Le Bidan'23 和 Johst'24 都是"blind+DA 级联"不是"切换"。**创新性正面证据**，写作时把"级联 vs 切换"差异当贡献切入点。
2. **(8,8)-16APSK + Gamma-Gamma 块衰落 + 星地相干 CPR 会议论文：库内 0 篇**。APSK 仅在 B11（letter，OFDM）和 sat.1553（综述）。Gamma-Gamma 多见于 IM/DD 或容量分析。**系统模型段无 1:1 对标**，术语/公式要对齐 B11 + sat.1553 + 教科书。
3. **切换/自适应估计器机制会议论文：库内 0 篇直接命中**。靠 He(骨架)+Wang(机制)+Xu(迟滞) 拼。

---

## 用法说明（给后续前置工作活用）

**术语活**：从 A 组 5 篇 + C 组提取每个词的标准英文写法 + 用法例句。重点对照 Johst（DA vs blind 术语）+ OECC-PSC（pilot 频谱代价术语）+ B11（NDA-ML 术语）。

**公式活**：粒度对齐 A 组 5 篇——别人给到什么程度（完整推导 vs 直接给结论）。Le Bidan 872 行最完整可参照。

**力度活（第一轮摸底）**：用 A 组 5 篇建基准表——每节/每技术点别人写到什么程度。重点 Johst（DA vs blind 对比力度）+ Le Bidan（CCISP 体例力度）。

**句式活**：writing-patterns-conference.md 已提取（R006 来源），但来源论文里 OECC'24/APCCAS'22/ICUMT'15 已换掉。句式库本身仍可用（句式跟技术内容无关），但如要补新句式，从 A 组 5 篇提。

**切换段写法**：He(骨架) + Wang(机制) + Xu(迟滞)，三个写法启发见 S010 §10。

---

## 待办

- [ ] 用户手动下载 He SPIE'24（10.1117/12.3036565）—— SPIE 链接 https://www.spiedigitallibrary.org/conference-proceedings-of-spie/3036565
- [ ] 用户手动下载 Xu PTL'26（10.1109/LPT.2026.3676909）—— IEEE 链接 https://ieeexplore.ieee.org/document/11454624/
- [ ] 下载后放 `papers/downloads/2026-07-11/`，用 `tools/convert` 转 markdown
- [ ] V&V'83 如需引用细节，按需补下（引文献不阻塞）
