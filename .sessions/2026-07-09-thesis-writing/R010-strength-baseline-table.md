# [R010] 力度基准表——对标集 A 组 5 篇力度摸底（D-P0 产出）

> 2026-07-11 | 关联：专题 2026-07-09-thesis-writing / writing-campaign-plan.md §2 P0 / benchmark-paper-set.md A 组
> 数据来源：3 子 agent 并发提取（A=Johst / B=Le Bidan / C=Panasiewicz+OECC-PSC+Paillier），各篇 content.md 已主线亲自核验存在（268/872/148/150/258 行，FR-26 PASS）

## 调研问题

对标集 A 组 5 篇会议论文，每个技术点别人写到什么力度？我方 CCISP 2026 投稿（4-6 页）应该写到什么力度（不多不少，对齐领域惯例）？

## 发现

### 0. 总览表（5 篇对比）

| 论文 | venue | 行数 | 章节数 | 公式数 | 图数 | 表数 | 篇幅定位 |
|---|---|---|---|---|---|---|---|
| **Johst** | WiSEE'24 | 268 | 6（含实验节） | ~3（全定义级） | 6 | 0 | **卖点最贴**：DA vs blind 对比 + 低 SNR + 外场。重描述轻推导 |
| **Le Bidan** | ICSOS'23 | 872 | 6 | ~25（但**仅 1 个完整推导**：CMA 代价函数；其余参数赋值/符号定义） | ~12 | 0 | **CCISP 体例标尺**：方法节最厚(~340 行)，模块逐段叙述，结果轻 |
| **Panasiewicz** | MWP'22 | 148 | 4 | ~6（直接给） | 6 | 0 | 三项全中（相干+载波同步+湍流），两鉴相器对比 |
| **OECC-PSC** | OECC'25 | 150 | 4 | ~7（**完整推导链** PA→ML→MAP） | 2(含5子图) | 0 | pilot 频谱代价 vs ML/MAP + CRLB，**公式密度最高** |
| **Paillier** | ICSOS'19 | 258 | 5 | ~12（完整推导） | 6 | **2** | LEO+AO+DPLL，唯一有表的。无 BER 曲线，用相位误差方差替代 |

**横向规律**：
- **表极少**：5 篇中 4 篇 0 表（仅 Paillier 2 表环路参数/pull-in time）→ 我方加 1 张增益表是**增量亮点**非必需
- **公式数 3-25 但粒度两极**：要么定义级（Johst/Le Bidan 大多数），要么完整推导（OECC-PSC/Paillier）。**没人做半推导**
- **图 6 张是主流**（3/5 篇），2-5 子图
- **贡献声明全散文式 2-3 句**，5 篇无一用 bullet 列表
- **算法流程全文字/框图**，5 篇无一用伪代码

---

### 1. Intro 节

#### 1.1 背景介绍篇幅

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | 段落展开 ~9 行（L17-23），引文密集铺 FSO/馈电/湍流/多孔径动机 | §I |
| Le Bidan | 段落展开 ~50 行（§I L59-109），引 CNES/CCSDS/COTS/TBIRD，不堆综述 | §I |
| Panasiewicz | 2 段散文 ~10 行（L17-27），FSO 优势+OPLL/DSP 对比标准铺垫 | §I |
| OECC-PSC | **单段密集 ~5 行**（L23-27），400ZR→1.6Tbps 动机+pilot vs ML/MAP | §INTRO |
| Paillier | 3 段散文 ~14 行（L43-57），相干优势+OPLL→DPLL+Doppler 残差量级 | §I |

**【我方应到的力度】**：**1-2 段散文，~8-15 行**（对齐 Panasiewicz/Paillier）。Le Bidan 50 行是含设计目标的展开，我方 CCISP 4-6 页无此空间。背景铺到"星地 FSO 相干 + 湍流致相位噪声 + CPR 必要"即可，引 3-5 篇综述/标准。

#### 1.2 贡献声明写法

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **散文式无 bullet**，L23 给速率/调制/FEC 假设 + L25 分节路标，弱贡献声明 | §I |
| Le Bidan | **散文式无 bullet**，散落 §II.C 两句 + Abstract | §II.C/Abstract |
| Panasiewicz | **散文式无 bullet** 2-3 句"propose a fully digital OPLL" | §I L27 |
| OECC-PSC | **散文式无 bullet** 2-3 句，把 [5] 扩到 256-QAM+AOPN+块并行 | §INTRO L27 |
| Paillier | **散文式无 bullet** 2-3 句"preliminary study…design methodology" | §I L55-57 |

**【我方应到的力度】**：**散文式 2-3 句，不用 bullet**。5 篇 0/5 用 bullet——会议论文惯例是散文式。写作句式参照 writing-patterns-conference.md 的"In this paper, we..."句式（R006 §2.4）。**注**：R006 §2.4 已标注贡献列表→散文修正，此处 R010 实证支撑该修正。

#### 1.3 问题动机引出方式

5 篇均从"现有方法的局限"切入（Johst：blind CMA 低 SNR 不稳；OECC-PSC：pilot 牺牲频谱效率；Paillier：OPLL 残余 Doppler），1-2 句点出 gap 后引出本文方法。

**【我方应到的力度】**：**1-2 句引出 DA/NDA trade-off 的 gap**（对齐 R009 逻辑链第一段：教科书共识 DA 低 SNR 优/NDA 省 overhead）。不深挖，gap 作为方法动机。

---

### 2. System Model 节

#### 2.1 信道模型（Gamma-Gamma）深度

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **无 Gamma-Gamma 公式**，信道模型以图给出（Fig 2），文字列损伤源（AWGN/PDL/CFO/Wiener PN） | §II/§II.C |
| Le Bidan | **无 Gamma-Gamma 公式**，明确声明"大气湍流未显式仿真"(L178-184)，用 Wiener PN + ASE | §II.A |
| Panasiewicz | **段落展开**给 H-V 湍流模型 + Cn²(h) 三档 + 风速公式 vrms | §II |
| OECC-PSC | **公式较细**：eq(1)信号/eq(2)极坐标/eq(3)四分量叠加+协方差矩阵 | §PROPOSED |
| Paillier | **不建湍流信道模型**（声明恒幅，湍流推给 [9]），仅框图级描述 | §II |

**【我方应到的力度】**：**给 Gamma-Gamma 块衰落模型公式 + 块结构说明，1 段 + 1-2 个公式**。我方核心场景就是 GG 块衰落（R009 背景），且 benchmark 缺口 2 明确"库内 0 篇 GG+16APSK+星地 CPR 会议论文"——给 GG 公式既是惯例填补也是我方系统模型必要成分。对齐 Panasiewicz 的湍流模型深度 + OECC-PSC 的信号模型公式粒度。

#### 2.2 帧结构-信号模型描述

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | 文字描述帧结构 + Fig 1，给子序列长度/overhead 7.75% 等具体数字 | §II.A + Fig1 |
| Le Bidan | **专节 §III.B 帧格式**（L319-352），给开销公式 η=3.6% + 与 400ZR 对比 | §III.B |
| Panasiewicz | 功率链路预算数字（-16dBm/4dB margin） | §II-A |
| OECC-PSC | eq(1-3) 信号模型公式链 | §PROPOSED |

**【我方应到的力度】**：**帧结构文字描述 + 1 句 pilot overhead 数字（1.25dB=10log10(4/3)）**。对齐 Johst（文字+图给数字）+ Le Bidan（开销讨论）。pilot overhead 是我方卖点核心数字之一（R009 第4条），必须给出且引 Shieh-Djordjevic 2010。

#### 2.3 估计器（DA/NDA）数学表述粒度

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **直接给结论+引文**，无推导。MIMO ZF vs MMSE 一句"性能相近"带过 | §II.C |
| Le Bidan | **CMA 给完整代价函数 eq(1)**（§IV.D）；其余 7 模块全"引用+参数+一段文字"，无推导 | §IV（~340行）|
| Panasiewicz | 公式直接给+一句话解释：K_D sin(Mθ)、Im[Xk^M]、atan2、M2M4 SNR | §II-B |
| OECC-PSC | **完整推导链** eq(4-7) PA→ML→MAP 三级递进 | §PROPOSED |
| Paillier | **完整推导**：MAP-BPSK 鉴相/环路滤波器/NCO/CRB eq(11)/squaring loss eq(12) | §III |

**【我方应到的力度】**：**给 DA/NDA 两个估计器的核心公式（直接给结论级），不推导**。对齐 Panasiewicz（公式直接给+一句话解释）。具体：
- DA：`θ̂_DA = angle(r_pilot · p*)`（直接除法去调制，R009 第2条，代码 `_recovery.py:153`）
- NDA：`θ̂_NDA = (1/M₀) angle(Σ r^M₀)`（升幂去调制，R009 第1条，代码 `_recovery.py:213`）
- 两个公式各 1 行，各跟一句话解释。**不推导 squaring loss**（引 V&V 1983 即可，R009 原则：引教科书结论不深挖）。
- 切换判据 per-block SNR 公式 1 个（R009 待查术语，倾向显式定义）。

---

### 3. Method 节

#### 3.1 切换机制描述方式（判据/阈值/算法流程）

5 篇无一直接对标"切换"（benchmark 缺口 3）。参照 B 组 He(骨架)+Wang(机制)+Xu(迟滞)。

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | blind vs DA 对比是**文字段落**（§II 开头 L29-31），非切换机制 | §II |
| Le Bidan | CMA+DA 是**级联**非切换，文字逐模块叙述 | §IV |

**【我方应到的力度】**：**文字段落 + 1 个框图 + 判据公式**（不用伪代码——5 篇 0/5 用伪代码）。描述：①per-block SNR 计算 ②阈值/判据 ③选 DA 或 NDA。对齐领域惯例（文字+框图）。框图可复用 S006 Fig.1 系统框图。

#### 3.2 创新点定位力度

5 篇创新点均在"方法节给出自己提出的新公式/新参数选择"，用 1-2 段集中说明。

**【我方应到的力度】**：**1-2 段说明切换是"per-block SNR 驱动的 DA/NDA 自适应选择"**，定位=量化归因型（R009/S010 用户拍板）。不夸成"提出新算法"，强调"跨场景自动选优 26/29"（R008 措辞）。创新点力度对齐 Johst（弱声明）——会议论文不吹。

---

### 4. Results 节

#### 4.1 BER 曲线呈现（子图数/纵轴/横轴）

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | Fig3 仿真 **2 子图**（DP-4QAM/DP-16QAM），纵轴 BER 10⁻⁵-10⁰ 对数，横轴 SNR(dB) -5~30，5 条损伤叠加曲线 + SD-FEC 阈值线 + AWGN 理论线 + inset outage ratio | Fig3 |
| Le Bidan | Fig11 GMI + Fig12 uncoded BER，**2 子图**，横轴 SNR(dB) -7~10 | §V |
| Panasiewicz | **单图** Fig6 BER vs 风速，三档湍流一条曲线，30 事件均值 | Fig6 |
| OECC-PSC | Fig1(b) BER vs 块长 + Fig2 三子图（子块长/BER vs SNR/SNR惩罚 vs 线宽） | Fig1-2 |
| Paillier | **无 BER 曲线**，用 Fig3 相位误差方差 vs SNR（理论 vs 仿真）+ Fig4-6 频偏收敛时域波形 | §IV |

**【我方应到的力度】**：**BER vs SNR 主图，2-6 子图分场景**（S006 Fig.2 已有 3×2 纵向 6 子图方案）。纵轴 BER 对数（不硬凑 1e-5，对齐 Paillier 画到能画到的，R004/H002 结论），横轴 SNR(dB)。加 AWGN 理论线作隐式 baseline（对齐 Johst）。**crossover 在图中自然呈现**（Fig.4 已有，R009 只呈现数据事实）。

#### 4.2 增益数字怎么报（表/正文/口径）

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **正文 dB 口径**，无汇总表。如 DSP-outage 阈值-1.2dB | §III/§V |
| Le Bidan | **正文 dB 口径**（-6dB 最低 SNR、收敛<100µs），无汇总表 | §V |
| Panasiewicz | **正文口径**，无表 | §III |
| OECC-PSC | **正文口径**（100GBaud/150kHz 时 MAP 4dB vs PA-ML 5dB vs PA 7.5dB） | §RESULTS |
| Paillier | **两表**：TABLE I 环路参数、TABLE II pull-in time（唯一有表的） | §IV |

**【我方应到的力度】**：**正文报关键 dB + 1 张增益汇总表（Tab.1，只放强湍流 3 行 naive 口径）**。5 篇仅 1 篇有表，我方加 1 表是**增量亮点**。口径必须用代码行验证（D004 教训），主报 naive（强湍流 +1.26~1.85dB，D004）。报前验证 fair=naive+1.249（fair_comparison.py:109）。

#### 4.3 baseline 对比怎么写

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **段落展开式**，§II 开头文字对比 blind CMA vs data-aided（收敛慢/低 SNR 不稳/调制相关），无对比图无对比表 | §II |
| Le Bidan | **段落式定性对比**（§III.A 比 DVB-S2/400ZR；§IV.G 比 V&V/BPS 并弃用），不专列对比节 | §III/§IV |
| Panasiewicz | 两鉴相器 Fig5 波形叠加 + 文字定性，不给定量增益表 | §II-C |
| OECC-PSC | PA/PA-ML/MAP 三估计器同图对比，无单独表 | §RESULTS |
| Paillier | 模拟 PLL 公式 vs 数字仿真自洽验证，非多算法横比 | §IV |

**【我方应到的力度】**：**DA/NDA 两曲线同图 + 文字段落说明各自优势区 + 切换曲线**（S006 Fig.4 crossover 已有）。对齐 OECC-PSC（多估计器同图对比）。不专列 baseline 对比节（5 篇 0/5 专列），对比融在 Results 文字段。

---

### 5. Conclusion 节

| 论文 | 力度 | 来源 |
|---|---|---|
| Johst | **1 段 3 句**，复述贡献+指出未来改进（更低 outage 阈值/多孔径合并实验） | §VI |
| Le Bidan | **一段**，复述贡献+局限（湍流未仿/hang-up 待解决/可推广 LEO） | §VI |
| Panasiewicz | **5 句**，复述贡献+future hardware | §IV |
| OECC-PSC | **3 句**，简述 | §CONCL |
| Paillier | **5 句**，复述+湍流留给 [9] | §V |

**【我方应到的力度】**：**1 段 3-5 句，复述贡献+一句 future/局限**。对齐 Johst/Le Bidan（一段）。会议论文 Conclusion 单段式（writing-patterns-conference.md 已标）。可点局限（弱湍流 naive 增益归零，诚实标注，不变量 3）+ future（更强判据/更多湍流场景）。

---

## 公式力度专项（贯穿各节）

| 粒度 | 谁这么做 | 我方是否采用 |
|---|---|---|
| **定义级**（只给符号/参数值） | Johst（3 个全定义）、Le Bidan（25 个中绝大多数） | 系统模型参数用此粒度 |
| **直接给结论**（公式+一句话解释） | Panasiewicz、Le Bidan（CMA 外的模块） | ✅ **DA/NDA 估计器核心公式用此粒度**（主力） |
| **完整推导** | OECC-PSC（PA→ML→MAP 链）、Paillier（环路+squaring loss 推导） | ❌ 不推导。squaring loss 引 V&V 1983 即可（R009 原则） |

**【我方公式总数建议】**：**2-3 个核心公式**（R009/writing-campaign-plan P1 已定）：
1. DA 估计器 `θ̂_DA = angle(r_pilot · p*)`（直接给，代码 `_recovery.py:153`）
2. NDA 估计器 `θ̂_NDA = (1/M₀) angle(Σ r^M₀)`（直接给，代码 `_recovery.py:213`）
3. per-block SNR / 切换判据（待 P1 定符号后给，显式定义）

**系统模型参数**（GG 信道 αβ、M₀=8、pilot spacing 等）用定义级，进参数表（P2 活）不进正文公式。

---

## 图表力度专项

| 论文 | 图 | 表 |
|---|---|---|
| Johst | 6（帧结构+框图+信道模型+BER仿真+外场装置+功率时序+BER实验） | 0 |
| Le Bidan | ~12（多框图+少性能图） | 0 |
| Panasiewicz | 6（链路+Cn²+OPLL框图+SNR时变+VCO频率+BER） | 0 |
| OECC-PSC | 2（含5子图） | 0 |
| Paillier | 6（架构+DPLL框图+相位误差方差+频偏收敛×3） | 2 |

**【我方图表数建议】**：**4-6 图 + 1 表**（writing-campaign-plan F2 + S006 已有 4 图方案）：
- Fig.1 系统框图（S006 已有 SVG）
- Fig.2 BER 主图 3×2 或 2×3 子图（S006 已有）
- Fig.3 净增益方案（S006 已有）
- Fig.4 crossover（S006 已有，只呈现数据事实）
- （可选）Fig.5/6 线宽扫描或选对率
- Tab.1 增益汇总（只强湍流 3 行 naive，增量亮点）

---

## 结论

力度基准表建成。5 节 × 3-5 技术点 = **20 条基准**（1.1/1.2/1.3/2.1/2.2/2.3/3.1/3.2/4.1/4.2/4.3/5 + 公式专项 + 图表专项），每条标来源论文+我方应到力度+依据。总览表 5 篇完整。

**核心标尺结论**：
1. **力度主标尺 = Johst + Le Bidan**（DA/NDA 对比力度 + CCISP 体例）+ Panasiewicz（公式直接给粒度）
2. **公式粒度 = 直接给结论级**（对齐 Panasiewicz），不推导（OECC-PSC/Paillier 的完整推导是少数派，且我方 R009 原则要求引教科书结论不深挖）
3. **贡献声明 = 散文式 2-3 句**（5/5 篇如此，bullet 是反惯例）
4. **表是增量亮点**（4/5 篇 0 表，加 1 表强化数字呈现）
5. **算法流程 = 文字+框图**（5/5 篇无伪代码）
6. **BER 曲线 = 主图标尺**，纵轴不硬凑 1e-5（对齐 Paillier），加 AWGN 理论线隐式 baseline（对齐 Johst）

**后续活怎么用这张表**：
- **P1（用语符号公式）**：查 §2.3 估计器表述粒度 + 公式专项 → DA/NDA 公式直接给，2-3 个，不推导
- **P2（参数数字）**：查 §4.2 增益数字报法 → 正文 dB + 1 表（Tab.1 naive 强湍流）
- **P3（叙事结构）**：查各节篇幅 + §1.2 贡献散文式 → 5 节大纲，Intro 不超 2 段，Method 不专列对比节
- **W1-W5（正文）**：每节查对应小节"我方应到的力度"
- **F1（力度第二轮）**：逐点对照本表检查讲多了还是少了

## 对决策的影响

- **不新建 D###**：本文件是 research note，不改方向/架构决策。所有力度建议基于已验证的 benchmark-paper-set.md A 组 + R009 逻辑链。
- **R006/R007 印证**：R006 §2.4"贡献列表→散文"修正获 R010 实证支撑（5/5 篇散文）。R007 两段式（影响分析+方法）落在 Results 内 §IV-A/§IV-B 不变。
- **守质量红线**：①每条标来源（不凭印象）②不做技术精读（只提取力度）③守 FR-22（只读已有 content.md）④我方应到力度建议有依据（对齐 X 论文 Y 节因为 Z）。
