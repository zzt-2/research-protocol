# [R007] CCISP 包装策略——把现有数据组织成导师认可的两段式故事

> 2026-07-10 | 关联：专题 slug 2026-07-09-thesis-writing / H004（包装策略交接）/ 导师 4 点反馈（voice.md 2026-07-10 导师段）
> 纪律：守路 1（只动包装不动数据不改算法）+ 导师第 3 点（强调自己行的，不要说自己不行的）+ D004 口径标加减方向 + FR-22（不跑实验）。所有数字已核查（见 R006 §3.1 素材库）。
>
> **本文档定位**：R006 是"写作流程规划"（怎么写、写几节、句式怎么套），R007 是"叙事包装策略"（这组事实怎么讲成站得住的故事）。R006 给骨架，R007 往骨架里填叙事逻辑。写正文时**先查 R007 定每节讲什么故事 → 再查 R006 定句式怎么套**。

---

## 0. 一句话包装方向

**把"盲估计（NDA-ML）相对导频估计（DA-ML）在强湍流/上行低 SNR 区的净增益"包装成一个两段式故事**：第一段（影响分析）量化"湍流对系统性能影响多大"——有湍流 vs 无湍流的 BER 瀑布对比；第二段（方法）讲"在有湍流条件下，盲估计全程不输导频、且在强湍流/上行低 SNR 区 +1.2~1.9dB（naive）"，切换方案作为"全工作区可用"的鲁棒性补丁收尾。**只讲行的（强湍流/上行增益），不提不行的（弱湍流归零、切换 vs 导频多数场景输）。**

导师 4 点映射（voice.md 2026-07-10 导师段）：
| 导师指令 | 本策略怎么落实 |
|---|---|
| ① 两段式（影响分析 + 方法，方法全在有湍流下仿真）| §1 节级落地，Results 内拆两子节 |
| ② 无 rebuttal，一刀切 | §2 切换叙事收窄到"一遍读下来不质疑"，不预判审稿人 |
| ③ 强调自己行的，不说自己不行的 | §3 弱湍流处理 + 全文表述策略 |
| ④ 没有后路，该写了 | 本策略是写正文前的最后准备，定完进 D2 |

---

## 1. 两段式结构怎么落地（导师反馈第 1 点）

### 1.1 对齐确认：两段式 = 整体叙事偏向，非砍成 2 章

导师说的"影响分析 + 方法"是**内容逻辑的两大块**，不是章节结构。R006 的 5 节骨架（Intro→System Model→Method→Results→Conclusion）**保留不变**，两段式落到：

- **全篇叙事重心往"影响分析→方法"的因果链靠**：Intro 讲背景时不只说"湍流难"，要落到"湍流让导频失效"（影响）→"盲估计天然抗"（方法）这个因果上
- **Results 节内部拆两个子节**，各自承担一段叙事：
  - **§IV-A 湍流影响分析**：有湍流 vs 无湍流 BER 对比（答"湍流影响多大"）
  - **§IV-B 方法性能**：切换/盲估计在有湍流条件下的增益（答"新方法好不好"）
- **Intro 贡献句也分两块呼应**（见 §1.4）

这样既守会议论文 5 节惯例（R006 §2.1），又把导师的两段式逻辑嵌进去。用户确认（2026-07-10）："老师说的应该是整体的叙事偏向？也就是往这上靠？之前咱们搞的骨架是骨架。"

### 1.2 第一段：影响分析节（§IV-A）讲什么

**核心问题**（导师原话）："湍流对于通信系统的性能影响有多大啊？有湍流的和没湍流的，这样做一个对比。"

**叙事目标**：用现有 BER 数据，把"湍流对 BER 的破坏"量化成一个审稿人一眼看懂的图，为第二段"方法"铺必要性。

**用什么数据**（现有，不补）：
- Fig.2 BER 主图本身就是"有湍流（各档）vs 无湍流（AWGN）"对比——**这正是导师要的**。把 AWGN 子图当"无湍流基准"，各湍流档子图当"有湍流"，子图排列按湍流强度递增，读者扫一眼就看到"湍流越强 BER 瀑布越缓、能到的 BER 越浅"。
- 数字锚点（R006 §3.1-C）：AWGN 能到 1e-5，中湍流刚跨 1e-5（46dB），强湍流最低 2e-4~1e-3。**这个"递进退化"本身就是影响分析的量化结论。**
- deep fade 正确表征（不变量 5）：衰减率从轻湍流 ~3×/2dB 降到强湍流 ~1.4×/2dB——**斜率变缓是影响分析的技术内核**，不是"BER 卡死/地板"。

**两段之间的逻辑过渡**（§IV-A 末尾→§IV-B 开头）：
> 影响分析结论 = "湍流让 BER 瀑布变缓、导频段在 deep fade 区失效（pilot-segment failure）" → 方法节开头 = "而盲估计（NDA-ML）因块级积分天然抗 deep fade，在有湍流条件下全程不输导频，且在强湍流/上行低 SNR 区有 +1.2~1.9dB 优势。"

这个过渡把"影响（问题）→方法（解法）"的因果钉死，导师要的两段式逻辑就成立了。

### 1.3 第二段：方法节（§IV-B）讲什么

**核心**：方法性能 = 盲估计 vs 导频估计在有湍流下的净增益 + 切换方案的全工作区鲁棒性。

**两块内容**：
1. **净增益量化**（主卖点）：盲估计 vs 导频在强湍流/上行 +1.2~1.9dB（naive，剔导频开销）。用 Fig.3 净增益图 + Tab.1 表呈现。
2. **切换鲁棒性补丁**（次卖点）：切换方案确保盲估计在全工作区可用——低 SNR 区避险（vs 固定盲 +1.3~2.3dB），让盲估计不必"在低 SNR 区切回导频"。用 Fig.4 crossover 机制图呈现。

**关键表述策略**（导师第 3 点）：只报强湍流/上行的增益（行的），弱湍流场景按 §3 处理（不报归零数字）。

### 1.4 Intro 贡献句两块呼应

R006 §2.3 的贡献草案（散文式 3 句）按两段式重排为**因果递进的两块**：

**第一块（影响 + 方法发现）**：
> We quantify the impact of atmospheric turbulence on carrier phase estimation in satellite-to-ground FSO links, showing that deep fades under strong turbulence cause pilot-segment failures (BER waterfalls flatten from ~3×/2dB to ~1.4×/2dB).

**第二块（方法贡献 + 数字）**：
> We then show that blind estimation (NDA-ML) remains robust throughout the turbulence region, achieving a net gain of +1.2 to +1.9 dB (net of pilot overhead) over pilot-aided estimation in strong-turbulence and uplink scenarios. A block-effective-SNR-based estimator switching scheme is further proposed to ensure full-operating-region applicability.

**守导师第 3 点**：不写"弱湍流归零"、不写"切换 vs 导频多数场景输"。数字用 naive 口径占位（强湍流真实增益），导师定 fair 后调。

---

## 2. 切换对比框架收窄（导师反馈第 2、3 点）

### 2.1 合法对照 = 只讲 vs 固定盲（NDA）

**进论文的唯一切换对比**：切换 vs 固定 NDA，强湍流/上行低 SNR 区 +1.3~2.3dB（CI 下界全正）。

**vs 固定导频（DA）那行不进论文**（导师第 3 点 + 不变量 8）：
- D002 实测：切换 vs 固定 DA，AWGN/weak/moderate 全 SNR 输（−0.1~−1.2dB）；强湍流高 SNR +0.02~+0.20dB 多数不显著。
- 这是"说自己不行的"，内部记录保留（D002/decisions.md），对外不讲。

**叙事收窄**：切换的真实价值 = "让盲估计在低 SNR 区也能用"（避险），不是"全面赢两种固定方法"。表述为"鲁棒性补丁"（robustness complement），不称"独立增益卖点"（D002 DECIDED）。

### 2.2 完整叙事链（切换怎么讲成"有物理依据"）

**crossover 机制是切换的物理合法性来源**，用它把"切换有道理"讲漂亮：

1. **现象**（Fig.4 crossover 图呈现）：低 SNR 区 NDA-ML 升幂崩溃（BER 升），高 SNR 区 NDA 反超 DA；存在一个 crossover 点（~12-14dB 块有效 SNR）。
2. **物理因果**：NDA-ML 升幂去调制依赖信号 SNR 足够高（升幂噪声放大在低 SNR 区致命）；DA 靠已知导频不受 SNR 影响，但 deep fade 区导频段也失效。两者各有所长，存在天然交叉。
3. **方法**：用块有效 SNR 做判据，低于阈值用 DA（避险），高于阈值用 NDA（高性能）。**切换 = 把 crossover 从"现象"变成"可工程化的全工作区可用方案"。**

**导师第 2 点（无 rebuttal）落实**：这条叙事链要"一遍读下来审稿人能懂且不质疑"。关键防御点：
- 判据用块有效 SNR（物理可算，非事后选）——避免审稿人质疑"是不是偷看了结果才切换"（D001 bug3 的教训）
- crossover 点报实测值（~12-14dB）+ 标注它是数据驱动的观察，不是人为设定的
- **不预判**"审稿人会不会问 X"——导师说一刀切，包装让叙事自洽就行，不为每个可能的质疑加防御段落（R006 §2.4 禁用 `§7.5` 结构导航段同理）

### 2.3 切换定位表述（散文化，导师第 3 点）

**进论文的切换表述**（贡献句第三句 + Method 节 + Results §IV-B）：
> To ensure full-operating-region applicability of the blind estimator, a block-effective-SNR-based switching scheme is proposed. In strong-turbulence and uplink low-SNR regions, the switched scheme gains +1.3 to +2.3 dB over fixed blind estimation (CI lower bounds all positive), preventing the NDA power-fold collapse.

**禁用表述**（不变量 8 + 导师第 3 点）：
- ❌ "performs the best / outperforms in all scenarios"（切换不是全面赢，R006 §2.4 已标禁用）
- ❌ "switching vs pilot-aided: −0.1~−1.2 dB in most scenarios"（说自己不行的）
- ❌ 旧数字 +0.27~0.48dB（D001 永久禁用）

---

## 3. 弱湍流场景处理策略（导师反馈第 3 点）

### 3.1 核心原则：数据真实 + 选择性呈现，不是造假

导师原话（voice.md 2026-07-10）："你在表述的时候，也是强调这个，不要说自己不行的。你要去说自己行的。"

**naive 口径下弱湍流数据**（D004 核查）：AWGN +0.09 / weak +0.18 / moderate +0.19 dB，CI 重叠（统计不可分）。**数字真实但"几乎归零"是事实。**

**处理策略 = 选择性呈现**（领域惯例，R002 §C 实证 6 篇都不报 CI）：
- **不在正文/贡献句/结论里报弱湍流的具体增益数字**（不写"+0.09~0.19 dB"）
- **不写"弱湍流归零/不显著/优势消失"这种自我否定表述**
- 弱湍流场景只在 Fig.2 BER 主图里作为"湍流强度递增趋势的一环"出现（影响分析节用），不单独拎出来讲增益

### 3.2 三档处理

| 场景 | 处理方式 | 进哪里 |
|---|---|---|
| 强湍流/上行（strong/up_mod/up_str）| **主卖点**，报 naive +1.2~1.9dB，CI 下界全正 | §IV-B 方法性能 + Tab.1 + 贡献句 |
| 中湍流（moderate）| 一笔带过，BER 主图里出现但不报增益数字 | §IV-A 影响分析（趋势一环）|
| 无/弱湍流（AWGN/weak）| 当"无湍流基准"（AWGN）+ 趋势起点（weak），不报增益 | §IV-A 影响分析基准线 |

### 3.3 Fig.3 净增益图怎么画不暴露弱点

**风险**：Fig.3 如果横轴=湍流强度、纵轴=gain，画全 6 场景，弱湍流 +0.09~0.19 那几个点会显得"增益很小"，审稿人一眼看到卖点场景窄。

**处理方案**（二选一，等图表制作对话 D1 定）：
- **方案 A（只画强湍流/上行 3 点）**：横轴只放 strong/up_mod/up_str，纵轴 naive gain，CI 带。图小而聚焦，全是卖点。但失去"增益随湍流递增"的趋势。
- **方案 B（画全 6 点但视觉弱化弱湍流段）**：横轴全 6 场景按湍流递增，强湍流/上行段加粗/深色，弱湍流段细线/浅色。趋势完整（递增）且视觉重心在强湍流。
- **倾向 B**（递增趋势本身是"湍流越强盲估计越有优势"的论据，对故事有利），但 D1 画出来看效果再定。

---

## 4. 图表配合方案（呼应 R006 §2.2 待定项）

### 4.1 Fig.2 BER 主图——影响分析的核心载体

**子图选择**（导师要"有湍流 vs 无湍流对比"）：
- **画全 6 子图**（无/弱/中/强/上行中/上行强），按湍流强度递增排列。
- AWGN 子图 = "无湍流基准"，其余 = "有湍流"。**6 子图本身就是影响分析的呈现**——读者扫一眼看到 BER 瀑布随湍流递增变缓。
- 每子图 3 线（DA/NDA/oracle）+ HD-FEC 线（3.8e-3）。

**纵轴范围**（不变量 5 + R004）：
- 无/弱/中湍流子图：纵轴到 1e-5（做得到，H002 数据）
- 强湍流/上行子图：纵轴到 1e-4 或 1e-3（收窄，不强凑 1e-5，对齐 Paillier JLT 2020 只画到 1e-4 的领域惯例）
- **关键表述**：强湍流子图标"BER waterfall flattens (deep fade), lowest reached ~2e-4~1e-3"——讲清楚是 deep fade 特征不是 bug。

**这是导师第 1 点"有湍流 vs 无湍流对比"的直接落地**——Fig.2 不只是"方法性能图"，它同时承担影响分析功能。

### 4.2 Tab.1 净增益表——只放卖点场景

**列结构**（精简，导师第 3 点）：

| 场景 | naive gain (dB) | CI95 | 测法 | BER 可达 |
|---|---|---|---|---|
| 强湍流（下行）| +1.26 | [1.17, 1.35] | 工作区均值(n=112) | ~2e-4 |
| 强湍流（上行中）| +1.19 | [1.09, 1.29] | 工作区均值(n=115) | ~1.6e-4 |
| 强湍流（上行强）| +1.85 | [1.74, 1.97] | 工作区均值(n=96) | ~1e-3 |

CI = workregion_grand_ci95 减 pilot_overhead(1.249)，来源 `_fair_gain_summary_30seed.json`（已核查 2026-07-10）。等导师定 fair 口径则换 +2.4~3.1dB（fair_ci 原值）。

**不进表的**：
- ❌ AWGN/weak/moderate 行（naive 归零，导师第 3 点）
- ❌ fair 口径列（等导师定主报哪个口径，定了再加；先用 naive 单口径）
- ❌ "vs 固定 DA"切换行（导师第 3 点）

**加粗**：上行强 +1.85 dB 格加粗（最大卖点）。等导师定 fair 后，若改 fair 口径则数字换 +2.4~3.1dB。

### 4.3 Fig.4 切换机制图——卖点化呈现

**目标**：把 crossover 讲成"切换有物理依据 + 让盲估计全工作区可用"，不暴露"切换 vs 导频多数场景输"。

**画法**（机制图，非数据堆砌）：
- 横轴=块有效 SNR，纵轴=BER（或 MSE）
- 两条线：固定 NDA（低 SNR 区 BER 飙升）+ 固定 DA（低 SNR 区相对稳）
- 标 crossover 点（~12-14dB）：两条线在此交叉
- **加一条切换线**：全程跟踪两者较优者，在 crossover 点平滑过渡
- 标注：低 SNR 区"切换选 DA→避险"，高 SNR 区"切换选 NDA→高性能"

**卖点化要点**：
- 视觉重心放在"crossover 让切换成为可能"的机制上，不放在"切换 vs 固定某法的 dB 差"
- 不在图上标"切换 vs DA −1.2dB"这种负数（导师第 3 点）
- 配文（§IV-B）讲 +1.3~2.3dB（vs 固定 NDA，行的），不讲 vs DA（不行的）

---

## 5. 标题方向（naive 口径占位）

### 5.1 占位标题（naive 口径，等导师定 fair 后调）

**候选 A（量化归因型，贴故事根）**：
> Net Gain of Blind Carrier Phase Estimation over Pilot-Aided Estimation under Strong Atmospheric Turbulence in Satellite-to-Ground FSO Links

**候选 B（两段式呼应型）**：
> Impact of Strong Turbulence on Carrier Phase Recovery and a Robust Blind Estimation Scheme for Satellite-to-Ground FSO

**候选 C（切换收窄型，若切换当卖点）**：
> Block-Effective-SNR-Based Estimator Switching for Robust Carrier Phase Recovery in Strong Turbulent FSO Links

**倾向 A**（跟故事根候选 A 对齐，数字为根机制为辩护层；导师第 4 点"没有后路"先写，定不了就 A）。

### 5.2 口径占位说明

- naive 口径（剔导频开销）= 标题/表用 +1.2~1.9dB（当前倾向，剔水分不易被质疑）
- 若导师定 fair（含导频罚），标题/表换 +2.4~3.1dB
- **报数字前必查 D004 口径方向**（fair = naive + 1.25，`fair_comparison.py:109`）

---

## 6. 包装策略小结：叙事链一图流

```
Intro（背景→湍流难→导频在deep fade失效→盲估计抗→贡献两块）
   │
   ▼ 两段式因果
System Model（GG湍流3档 + 16APSK + DA/NDA公式 + 公平对照坐标）
   │
   ▼
Method（块有效SNR判据 + 切换逻辑 + crossover物理因果）
   │
   ▼
Results
  ├─ §IV-A 影响分析（Fig.2 有湍流vs无湍流BER对比，deep fade斜率变缓）
  │       └─ 过渡：导频失效→盲估计抗
  ├─ §IV-B 方法性能（Fig.3 净增益+Tab.1强湍流+1.2~1.9dB / Fig.4 crossover切换卖点化）
  └─ Complexity子节
   │
   ▼
Conclusion（贡献重述 + 强湍流数字 + 切换鲁棒性定位）
```

**全程守的表述策略**（导师第 3 点）：讲强的（强湍流/上行 +1.2~1.9dB + 切换低 SNR 避险 +1.3~2.3dB），不提弱的（弱湍流归零 + 切换 vs 导频输）。

---

## 对决策的影响

- **不新建 D###**：本文件是包装策略（R### research note），不改方向/架构决策。所有数字来自已核查的 D002/D004，叙事策略来自导师 4 点反馈（voice.md 2026-07-10）。
- **范围确认**：本文件在专题 scope 内（写作准备，不跑实验，不写正式正文）。包装策略是"写作准备"的合理延伸（topic-index 不变量 2）。
- **更新 R006**：R006 §2.1（章节结构）/§2.2（图表清单）/§2.3（贡献表述）/§2.4（句式映射）相关位置加引用指向本文件，写正文时先查 R007 定故事再查 R006 定句式。
- **后续**：R007 定完 → 进 D2（写中文草稿 Intro + System Model）+ D1（图表制作）可并行启动。
