# 切法元数据：B12 频域 pilot（双视角）

> 提取人：子 agent | 日期：2026-07-05 | 范围：B12 频域 pilot 锚 TCOMM 2022 + MAP OECC 2025 双视角
> 纪律：D018 中性提取（不判 Go/Kill）/ FR-26 证据链（未落盘标"信息不足"不脑补）/ 切法 ≠ 方法配方 / 团队只标作者名不推断师承（MAP = Kam 团队 BNU-HKBU，**不推断师承**）/ dB 口径警示（MAP vs PA/PA ML 为"同族 dB"，§3.3 警示）
> 6 维定义：① 大点锚 ② 切的角度 ③ dB 形态 ④ 横向多样性 ⑤ 动机叙事 ⑥ 实现复杂度（与 `_cut-map-final.md` §2-5 八类切法角度 / dB 形态分布 / 动机叙事套路 / 复杂度档对齐）

---

## 1. B12 锚视角切法（Gävert&Eriksson TCOMM 2022 双频段 pilot）

**论文**：Björn Gävert (Ericsson AB) & Thomas Eriksson (Chalmers University of Technology). "Estimation of Phase Noise Based on In-Band and Out-of-Band Frequency Domain Pilots." IEEE TCOMM 2022, Vol.70 No.7 pp.4780–4792. DOI 10.1109/TCOMM.2022.3171809。content.md 590 行已落盘可检索。

1. **大点锚（被谁/什么切）**：B12 锚自己即"频域 CW pilot 相位估计理论"大点——它锚的是 [11]–[18] CW pilot practical studies 群（光域 pilot-tone 实测 + Lundberg 极化复用 pilot，行 41）的理论空白，自承"Earlier related papers on CW pilots have been focusing on practical aspects... we provide a solid foundation for the theory"（行 45）。**它被 COMST Survey 当作 CW pilot 理论代表引用（Ref [62]，content.md 行 531/1145）**——即 B12 锚是 cited-by 池里被切的大点本体，不是切别人者。
2. **切的角度**：**性能极限/理论框架**（三估计器 BLUE/ML/improved 相对 CRLB，improved 近似 MVU，行 277–333/451）+ **架构替换**（improved 滤 phasor 而非相位，避开 ML unwrap 噪声放大，行 277–333）+ **参数调度**（最优 SPR/β 解析，in-band vs out-of-band 分别数值求解最大化 SNDR，行 343–410）。三角度并重，理论框架为主。
3. **dB 形态**：**无 vs baseline dB gain**（全文无"赢 RF pilot/BPS/V-V/DD-PLL X dB"对比，仅内部估计器 vs CRLB + 最优 SPR 数值）。仅有的 dB 提及：① −10 dB（in-band）/ 10 dB（out-of-band）SPR 失效点（ML unwrap 在此 SPR 完全失败，行 429，**失效阈值非性能增益**）；② 18–19 dB OSNR（脚注 5 行 517，对应 σ_u²=0.01，与 [11][13] 实测对齐的**仿真条件非性能 dB**）。→ 落 `_cut-map-final.md` §3.1 **"无 dB 仅结构性"档**（与 L004 信息率界 / sat.1553 三切口 / L035 硬件 penalty 同档）。
4. **横向多样性**：在频域 pilot 路线池里属**理论框架独占**——给 CW pilot 解析最优 SPR + improved≈MVU 的理论框架是池里唯一（COMST Survey 把它标为 CW pilot 理论代表正是因为这点）。与时域 pilot 估计器（[9] Ip&Kahn feedforward CR / [19] Spalvieri&Barletta pilot-aided CR，行 257/325 自承表达式"due to modeling similarities"形似但机制不同）属**不同机制支线**。
5. **动机叙事**：**"前作有缺陷/空白 → 改进/补理论"套路**（`_cut-map-final.md` §4 ~15% 档）——CW pilot practical studies 群 ([11]–[18]) 有实测无理论 → B12 锚补 "solid foundation for the theory"。叙事证据链 = 行 45 自承句，立得住。
6. **实现复杂度**：**纯仿真/理论档**（`_cut-map-final.md` §5 最低门槛档，与 sat.1553/张思齐/jphot/oe/L024/L036 同档）——全数值仿真无硬件实验，典型参数 σ_Δ²=0.001（相位噪声创新）/ σ_u²=0.01（热噪声）（Fig 3/4/5/6），SPR 扫描，无星地/湍流/Doppler 建模。

---

## 2. B12 MAP 视角切法（OECC/PSC 2025 MAP Phase Recovery 256-QAM）

**论文**：Ma / Liu / Du (BNU-HKBU 珠海) + Wang (ZJUT) + Kam (CUHK-SZ). "MAP Phase Recovery for 256-QAM"（OECC/PSC 2025 WP-B-26，4 页 digest）。DOI 10.23919/OECC-PSC62146.2025.11109607。content.md 150 行已落盘（用户 2026-07-04 手动下破 IEEE 订阅墙）。**Kam 是 MAP 相位估计领域经典作者（与 Wang Ref[5] 同源），团队标 Kam 团队 BNU-HKBU/ZJUT/CUHK-SZ，不推断师承**。

1. **大点锚（被谁/什么切）**：MAP 锚的是 **Wang Ref[5] joint ML/MAP sinusoid estimation 框架（QPSK）**——MAP 把它扩展到 256-QAM + AOPN 模型（行 27）。**MAP 引 B12 锚作 Ref[4]**（行 25 "pilot-aided (PA) phase noise estimation methods use dedicated pilots... but sacrifice spectral efficiency [4]"），把 B12 锚归类为"频域 pilot 牺牲频谱效率"的**对照方向标**（citer 关系，非直接频域延伸）。即 MAP 同时锚 Wang [5]（算法源）+ B12 锚 [4]（对照方向）。
2. **切的角度**：**架构替换**（Wang [5] QPSK 框架 → 256-QAM + AOPN 复合相位噪声模型，行 27/45–53）+ **参数调度**（子块长 L_sub=1 性能最优 + block-wise 并行架构提计算效率，行 27/75–97/113）。
3. **dB 形态**：**同族 dB**（`_cut-map-final.md` §3.3 警示 5 类口径陷阱之一，引用时必须标"同族 dB"）——① MAP SNR penalty 4 dB @ 100 GBaud/150 kHz 线宽 **vs PA ML 5 dB**（差 1 dB，落 D005 边际）/ **vs PA 7.5 dB**（差 3.5 dB，落 D005 2–4 dB 区间内，行 115）；② 64 GBaud 下 MAP 几乎不变 vs PA ML 6.2 dB / PA 11 dB（差 ~7 dB，行 115）；③ BER 7% HD-FEC @ SNR 32 dB（100 GBaud）/ 33 dB（64 GBaud）（行 115）。**baseline 是 PA/PA ML 同族内部**（非传统 V-V/BPS/DD-PLL），D005 标尺下需注明"同族 dB"——与 LCOMM +0.9 dB Q-factor（vs 自身 PTJ）/ L008 MSE 4× 改善同属"vs 内部对照"档（`_cut-map-final.md` §3.1 第二档"边际够格"）。
4. **横向多样性**：在 pilot-aided 大类里属**时域 pilot-aided + MAP 估计器路线独占**——与 B12 锚频域 CW pilot 是 **pilot-aided 相位恢复的两条正交机制支线**（时域占符号位 vs 频域占连续频位）。MAP 的 block-wise 并行 + AOPN 模型组合在池里独占。
5. **动机叙事**：**"X 已被研究但 Y 场景/维度未覆盖"套路**（`_cut-map-final.md` §4 ~35% 绝对主流档）——Wang [5] 框架限 QPSK + 频域 pilot [4] 牺牲频谱效率 → MAP 扩 256-QAM + AOPN + block-wise 并行保连续。叙事立得住（行 25/27 自承）。
6. **实现复杂度**：**纯仿真/理论档**（与 B12 锚同档）——256-QAM 100/64 GBaud 数值仿真，激光线宽 100/150/500 kHz，SNR 32–40 dB 扫描，L_block=128/L_sub=1，无硬件实验，无星地/湍流/Doppler 建模（DCI 相干光背景）。

---

## 3. B12 锚与 MAP 机制对比（频域 pilot vs 时域 pilot-aided）

> 中性机制独立性分析，不判 Go/Kill。

| 维度 | B12 锚（频域 CW pilot） | MAP（时域 pilot-aided） | 机制关系 |
|---|---|---|---|
| **pilot 占位** | 连续频位（CW tone 注入已知 f_CW，占通信带宽内/外） | 符号位（每块首符作 PA pilot） | **正交**（频域 vs 时域） |
| **pilot 代价** | in-band 需高 pilot 功率（双重污染 σ_w²=σ_u²+σ_x²）/ out-of-band 牺牲带宽容量（行 107/509/511） | 牺牲频谱效率（占符号开销）（MAP 行 25 自承 [4] 即 B12 锚的代价） | 代价形态不同（功率/带宽 vs 开销） |
| **估计器结构** | 前馈频域：CW pilot → RX 频移 + LPF → 三估计器（BLUE/ML/improved）观测窗 2K+1 加权滤波 | 前馈时域 + 块并行：PA 粗估 → PA ML 细估 → 联合 ML（初始 θ）+ MAP（Wiener θ_k）子块迭代 | **均前馈无环路 TF、无 OPLL**（Q1/Q2 不撞 D006 的依据） |
| **相位噪声模型** | Wiener（Δ_n ~ N(0,σ_Δ²)，行 117–121） | Wiener + AOPN（AWGN 致相位噪声高斯近似叠加，行 45–53） | MAP 多一层 AOPN 复合建模 |
| **理论标尺** | CRLB（improved 近似 MVU 趋近 CRLB） | BCRLB（联合 ML/MAP 收敛到 BCRLB，行 17/75） | 均理论界驱动 |
| **dB 形态** | 无 vs baseline dB（仅内部估计器 vs CRLB + SPR 失效点） | 同族 dB（vs PA ML 1 dB / vs PA 3.5–7 dB） | B12 锚结构性理论增量 / MAP 边际够格同族 dB |
| **citer 关系** | 被 MAP 引为 Ref[4]"频域 pilot 牺牲频谱效率"对照方向 | 引 B12 锚作对照方向，算法源 = Wang [5] | **citer/对照方向，非直接延伸** |

**机制独立性结论**：B12 锚频域 CW pilot 与 MAP 时域 pilot-aided 是 **pilot-aided 相位恢复大类的两条正交机制支线**——频域占连续频位（功率/带宽代价）vs 时域占符号位（开销代价）；两者均前馈无环路 TF、无 OPLL（不撞 D006）；MAP 引 B12 锚作"牺牲频谱效率"对照方向标，但 MAP 算法源是 Wang [5] joint ML/MAP sinusoid（非频域 CW pilot 延伸）。**双视角机制独立性清晰**（B12 笔记关键发现 4/§附确认）。

---

## 4. B12 池 3 篇 cited-by 逐篇 6 维

> 池规模：B12 锚 TCOMM 2022 union **9 篇** cited-by（S002 §2.1 实测），候选 3 篇 = COMST Survey / acp.ipoc63121 / MAP OECC。MAP 与双视角重合（§2 已提取），本节不重复，只标"= §2"。故本节独立提取 2 篇（COMST + acp.ipoc63121）。

### 篇 1：10.1109/COMST.2024.3443158 — Modeling, Estimation, and Applications of Phase Noise in Wireless Communications: A Survey

**论文**：Zikai Chang / Yuntao Xu / Junjie Chen / Ning Xie / Yejun He / Hongbin Li. IEEE COMST 2024 (Vol.27 No.2 pp.912–, published 2025). content.md 1288 行已落盘可检索。**c=9**（S002 §2.1 实测 cited-by 池规模）。

1. **大点锚（被谁/什么切）**：**自己是综述大点**——B12 锚在其中作 Ref [62]（content.md 行 1145），被归类为 CW pilot 理论分析代表（行 531 "Gävert and Eriksson provided a more comprehensive theoretical analysis for the phase-noise estimation [62]... BLUE/ML/approximate MVU... approximate MVU always outperforms BLUE and has lower complexity than ML"）。即 COMST Survey 把 B12 锚当作"频域 CW pilot 理论分支"的代表节点纳入相位噪声方法地图。
2. **切的角度**：**综述延伸**（`_cut-map-final.md` §2 ~3 篇档，与 sat.1553 自报 / L001 综述+demo / L026 综述同档）——相位噪声建模 + 估计 + 应用三块地图，CW pilot 是估计块下的一个子分支（行 521–571 时域 pilot vs 频域 pilot 分类 + ML/MAP 算法 stepwise reception）。
3. **dB 形态**：**综述本身无 dB**（汇总各方法 dB，B12 锚被它标"无 dB 仅结构性"——COMST 行 531 复述 B12 锚结论"approximate MVU 趋近 CRLB 但大相位噪声区偏离"，未给 B12 锚 vs baseline dB）。→ 与 `_cut-map-final.md` §3.1 "无 dB 仅结构性"档一致。
4. **横向多样性**：**综述地图类独占**——频域 pilot 路线池里唯一综述（其余 cited-by 多为方法/实验论文）。
5. **动机叙事**：**"open problem 自报 → 填空白"套路**（`_cut-map-final.md` §4 ~5% 档，证据链最强但稀少）——行 17 abstract 自承"There is a surprising lack of a comprehensive overview... we conduct the first comprehensive survey on the modeling, estimation, and applications of phase noise in wireless communications"。
6. **实现复杂度**：**纯文献综述档**（无实验，无仿真）——与 sat.1553 综述（OSL DSP 算法地图）同档。

### 篇 2：10.1109/ACP/IPOC63121.2024.10809580 — Simplified Coherent DSP Short-Reach with Freq Domain Pilot Tone（待核）

**论文**：ACP/IPOC 2024 会议论文（标题取自 S002 §2.1 cited-by 候选清单）。**目录无 content.md，未落盘，未核**（B12 笔记 §附 cited-by 处理行 110 明确"acp.ipoc63121（频域 pilot tone，目录无 content.md，未核）"）。

1. **大点锚（被谁/什么切）**：**信息不足（未落盘）**——按标题推测锚 B12 锚频域 CW pilot（短距相干光 DSP 简化），**待全文核验**。
2. **切的角度**：**信息不足（未落盘）**——按标题推测**场景迁移**（频域 pilot tone 从长距/通用搬到 short-reach）+ **硬件实现/简化**（"Simplified Coherent DSP"），**待全文核验**。
3. **dB 形态**：**信息不足（未落盘）**——无法核 vs baseline dB / 绝对指标 / 无 dB，**待全文核验**。
4. **横向多样性**：**信息不足（未落盘）**——按标题推测属"场景迁移 + 硬件简化"组合，**待全文核验**。
5. **动机叙事**：**信息不足（未落盘）**——按标题推测"short-reach 需简化 DSP → 频域 pilot tone 低复杂度"（`_cut-map-final.md` §4 "X 已被研究但 Y 场景未覆盖"或"绕开而非赢"套路），**待全文核验**。
6. **实现复杂度**：**信息不足（未落盘）**——标题暗示 short-reach 工程实现档（与 L035 VLSI / B4/B5 FPGA demo 同档？），**待全文核验**。

> **FR-26 诚实标注**：篇 2 全 6 维均"信息不足"，不脑补。S002 §2.1 标它为候选（abstract 高相关频域 pilot tone short-reach），但全文未下无法提取切法元数据，是已知债务。

### 篇 3：10.23919/OECC-PSC62146.2025.11109607 — MAP Phase Recovery 256-QAM（= §2 MAP 视角，不重复提取）

**说明**：MAP OECC 2025 既是 B12 池 cited-by 之一，又是双视角之 MAP 视角。6 维切法见 **§2**（Kam 团队 BNU-HKBU/ZJUT/CUHK-SZ，不推断师承；同族 dB vs PA ML 1 dB / vs PA 3.5–7 dB）。**不重复提取**（B12 笔记步骤 2 明确"MAP 既是 cited-by 又是双视角之一，不重复提取"）。

---

## 5. 频域 pilot 模式归纳（中性，不判 Go/Kill）

> 样本规模提示：B12 池 cited-by 候选 3 篇（COMST + acp.ipoc63121 + MAP），其中 acp.ipoc63121 未落盘，有效样本 = 锚(B12) + MAP + COMST = 3 篇 + 1 篇待核。样本密度低，归纳为"中性观察"非统计结论（与 `_cut-map-final.md` §8 B6-B12 稀池债务标注一致）。

- **大点分布（频域 pilot 被切的子点）**：
  - **理论框架子点**（B12 锚自切 + COMST Survey 归类）：CW pilot 解析最优 SPR + improved≈MVU vs CRLB——理论维度独占。
  - **算法扩展子点**（MAP）：Wang [5] joint ML/MAP 从 QPSK 扩 256-QAM + AOPN——架构替换维度。
  - **场景迁移/硬件简化子点**（acp.ipoc63121，待核）：频域 pilot tone 搬 short-reach 简化 DSP——若属实则与 Paillier 池"场景迁移+硬件实现"安全区模式（`_cut-map-final.md` §2/§3.2）同构。
  - **未被子点**（中性观察）：in-band vs out-of-band trade-off 在星地/湍流场景的迁移（Q1 候选）、频域 CW pilot + 时域 pilot-aided 联合架构（Q3 候选）——cited-by 池里未出现，是潜在独占空间（只标不推荐）。

- **dB 形态分布（频域 pilot 点 dB 多在哪个形态）**：
  - B12 锚 = **无 dB 仅结构性**（`_cut-map-final.md` §3.1 第四档）。
  - MAP = **同族 dB / vs 内部对照**（§3.1 第二档"边际够格"，baseline 是 PA/PA ML 非传统 V-V/BPS）。
  - COMST Survey = 综述无 dB。
  - acp.ipoc63121 = 信息不足。
  - **中性观察**：频域 pilot 路线 dB 形态偏"结构性/同族 dB"，**无一篇给出 vs 传统 baseline（V-V/BPS/DD-PLL）明确 SNR/BER dB 增量**——与 Paillier 安全区"5 篇落盘 0 篇出 vs 外部 baseline dB"（`_cut-map-final.md` §3.2）模式同构。频域 pilot 路线若要走 D005 第一梯队（vs 传统 baseline 几 dB），需补传统 baseline 对照（当前缺口）。

- **横向多样性（频域 pilot vs 时域 pilot-aided 在池里的分布）**：
  - 频域 CW pilot 支线：B12 锚（理论）+ acp.ipoc63121（short-reach，待核）= 2 篇。
  - 时域 pilot-aided 支线：MAP（256-QAM + AOPN）= 1 篇。
  - **机制正交**（§3 已证），池里频域支线略密于时域支线（2:1，但样本小）。
  - **联合架构**（频域 + 时域双重导频）= 0 篇（Q3 候选探索方向，池里未出现，独占空间，只标不推荐）。

- **动机叙事（频域 pilot 点常用什么叙事）**：
  - B12 锚 = **"前作有缺陷/空白 → 补理论"**（`_cut-map-final.md` §4 ~15% 档）。
  - MAP = **"X 已被研究但 Y 维度未覆盖"**（§4 ~35% 绝对主流档）。
  - COMST = **"open problem 自报 → 填空白"**（§4 ~5% 档，证据链最强）。
  - acp.ipoc63121 = 信息不足（按标题推测"short-reach 需简化"属场景迁移叙事）。
  - **中性观察**：频域 pilot 路线叙事偏"补理论/扩维度"，非"赢 baseline 几 dB"——与 dB 形态偏"结构性/同族"一致。

- **实现复杂度（频域 pilot 点常在哪个档）**：
  - B12 锚 + MAP = **纯仿真/理论档**（`_cut-map-final.md` §5 最低门槛档）。
  - COMST = 纯文献综述档。
  - acp.ipoc63121 = 信息不足（标题暗示 short-reach 工程实现档，待核）。
  - **中性观察**：频域 pilot 路线落盘 2 篇均在纯仿真/理论档，**无 FPGA demo / 无 outdoor 实测**——与 Paillier 池"硬件实现 ~8 篇 + outdoor ~3 篇"（§5）对比，频域 pilot 路线工程实现维度空（只标不推荐）。

- **频域 pilot 路线对"水一篇"的启示（中性观察非推荐）**：
  - 频域 pilot 路线当前 dB 形态偏"结构性/同族 dB"，**无一篇 vs 传统 baseline 明确 dB**——若目标是 D005 第一梯队（赢传统 baseline 几 dB），频域 pilot 路线需补传统 baseline 对照（当前缺口即潜在切口空间，只标不推荐）。
  - 频域 CW pilot（B12 锚）+ 时域 pilot-aided（MAP）联合架构 + 星地湍流迁移 = cited-by 池未出现的独占组合（Q3 候选），理论框架已齐（B12 锚最优 SPR + MAP block-wise 并行）但湍流 non-Wiener 扩展 + Doppler 致 pilot 频偏跟踪是技术债（只标不推荐）。
  - **一句话启示**：频域 pilot 路线是"理论框架已齐（B12 锚）+ 工程实现维度空（无 FPGA/实测）+ vs 传统 baseline dB 缺口"的稀池——切法空间在场景迁移/硬件实现（Paillier 安全区同构）或补传统 baseline dB 对照（D005 第一梯队切口），但样本密度低（3 篇有效），独占空间大但参考少（与 `_cut-map-final.md` §7"未饱和子大点切口多但参考少"尺子一致）。

---

## 6. 自评

- **6 维缺失率**：
  - B12 锚视角（§1）：0% 缺失（content.md 590 行全文到位，6 维全细档）。
  - MAP 视角（§2）：0% 缺失（content.md 150 行全文到位，6 维全细档；dB 标"同族 dB"口径警示）。
  - COMST Survey（§4 篇 1）：6 维中 dB 形态/横向多样性/复杂度依赖行 531/1145 + 综述性质推断，缺失率 ~0%（综述类 6 维本就偏"无 dB/综述档"，非信息不足）。
  - acp.ipoc63121（§4 篇 2）：**100% 缺失**（未落盘，全 6 维标"信息不足"，FR-26 诚实标注，是已知债务）。
  - **整体 4 篇独立 6 维（锚+MAP+COMST+acp）平均缺失率 ~25%**（acp.ipoc63121 拉高，若排除则 0%）。

- **双视角机制独立性是否清晰**：
  - **清晰**（§3 机制对比表 7 维度逐项对照）——频域 CW pilot（连续频位，功率/带宽代价）vs 时域 pilot-aided（符号位，开销代价）正交；均前馈无环路 TF 不撞 D006；citer 关系 = MAP 引 B12 锚作"牺牲频谱效率"对照方向标，MAP 算法源是 Wang [5]（非频域延伸）。**双视角是 pilot-aided 大类的两条正交机制支线**，非同源延伸。

- **守纪律自检**：
  - ✅ 只提取不判断（§5 归纳全用"中性观察非推荐"/"只标不推荐"，无 Go/Kill 判定）。
  - ✅ 不脑补（acp.ipoc63121 全 6 维标"信息不足"，FR-26 诚实标注）。
  - ✅ 切法 ≠ 方法配方（6 维聚焦"切的动作"——大点锚/角度/dB 形态/横向/叙事/复杂度，未抄 BLUE/ML/improved 算法推导或 PA/PA ML/MAP 估计器公式）。
  - ✅ 团队只标作者名不推断师承（MAP = Kam 团队 BNU-HKBU/ZJUT/CUHK-SZ，标 3 处不推断师承；B12 锚 = Gävert Ericsson + Eriksson Chalmers）。
  - ✅ dB 口径警示（MAP vs PA 3.5 dB / vs PA ML 1 dB 全标"同族 dB"，与 `_cut-map-final.md` §3.3 警示 5 类口径陷阱对齐）。

- **已知债务**：
  - acp.ipoc63121（10.1109/ACP/IPOC63121.2024.10809580）全文未下，§4 篇 2 全 6 维"信息不足"，是补下候选（S002 §2.1 标 abstract 高相关，下后可补全 6 维）。
  - B12 锚 cited-by union 9 篇里仅 3 篇候选已提取（COMST + MAP + acp.ipoc63121），其余 6 篇未进候选池（S002 §2.1 实测规模，本批次范围外）。
