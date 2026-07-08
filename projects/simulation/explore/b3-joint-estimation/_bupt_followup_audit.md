# BUPT 课题组 2024+ 续作审计（防 BUPT 自吞 B3-Q2 增量）

> 来源: B3-Q2 对话 2（H002 派发）| 日期 2026-07-08
> 目的：防 BUPT 自吞 B3-Q2 增量（核查 Liqian Wang / Siqi Zhang / Kunfeng Liu 课题组 2024+ 是否已发星地分集联合估计续作，致使 B3-Q2 的 CPE 联合 / Doppler / 星地 三个增量切口被吞没）
> 执行准则：①只报告事实，不下 Go/Kill；②搜不到写"未检索到"，不臆造；③abstract 断言必须交叉验证，搜索摘要页推断标"未验证"；④单次≤15 分钟，查不完标注"未完成"
> 锚定论文：jphot.2023.3265847（Liqian Wang, Jichen Wang, Xinyu Tang，FSTS+两级 FOE+MRC）；oe.520452（Liqian Wang, Kunfeng Liu, Siqi Zhang, Shuang Ding，PRBS+循环 QPSK 混合 TS）
> B3-Q2 三个法定增量切口：① CPE 联合维度 ② Doppler 维度（打破 jphot-L208"缓变"假设）③ 星地场景迁移

---

## 1. 课题组身份确认

| 问题 | 结论 | 证据 |
|---|---|---|
| Liqian Wang / Kunfeng Liu / Siqi Zhang 是否同一 BUPT 课题组？ | **是（同一课题组）** | 两篇锚定论文作者群交集：oe.520452 作者 = Liqian Wang + Kunfeng Liu + Siqi Zhang + Shuang Ding；jphot 作者 = Liqian Wang + Jichen Wang + Xinyu Tang。Liqian Wang 为共同 PI/通讯。oe.520452 正文引用 jphot 为 [24]，自述同组延续。 |
| 续作是否归属该组？ | **是** | 2024+ 续作（TTQP Photonics 11(9):885、OE 33(10):21660、SSRN 6293357、OECC 2026）作者均含 Kunfeng Liu / Liqian Wang，单位 Beijing University of Posts and Telecommunications。2023 续作 JCSCR 作者含 Xinyu Tang（jphot 共作）+ Liqian Wang。 |
| 张思齐学位论文是否同组？ | **未检索到 / 未确认** | 见 §2 末"张思齐"条。 |

**结论：** BUPT 课题组身份确认无疑。Liqian Wang（PI）+ Kunfeng Liu + Siqi Zhang + Shuang Ding + Mengyao Chen + Xinyu Tang + Yiwei Zhao 构成同一 FSO 相干接收研究群。

---

## 2. 2024+ 续作清单（含 2023 JCSCR 基础作）

每条标注：① 验证等级（abstract-已验证 / 搜索摘要-未验证）；② 对四要素的覆盖标记
**(a) 星地/下行 FSO 分集　(b) CPE/载波相位联合　(c) Doppler 频偏联合　(d) 多孔径/望远镜阵列**

### 2.1 JCSCR — MDPI Photonics 10(4):389 (2023) 　【abstract-已验证】
- 标题：*A Low-Complexity Joint Compensation Scheme of Carrier Recovery for Coherent Free-Space Optical Communication*
- 作者：Xinyu Tang（jphot 共作）, Liqian Wang 等（BUPT）
- DOI/链接：10.3390/photonics10040389 ｜ https://www.mdpi.com/2304-6732/10/4/389
- 一句话：提出 JCSCR，**联合补偿载波恢复（carrier recovery = FOE + CPE）**，低复杂度，单链路相干 FSO（CFSO）。
- 验证方式：webReader 抓取 MDPI 页面 abstract，确认"joint compensation scheme of carrier recovery (JCSCR) for coherent free-space optical (CFSO) communication"。
- 覆盖：**(a)否　(b)是（FOE+CPE 联合）　(c)否　(d)否**（单链路、地面 CFSO）
- ⚠️ 关键风险点：标题"joint carrier recovery"= FOE+CPE 联合，**直接触及 CPE 切口**，但为单链路地面场景，非分集接收下。

### 2.2 TTQP — MDPI Photonics 11(9):885 (2024) 　【abstract 部分-已验证，场景冲突-未定】
- 标题：*Low Complexity Parallel Carrier Frequency Offset Estimation Based on Time-Tagged QPSK Partitioning ...*
- 作者：Siqi Zhang, Liqian Wang, Kunfeng Liu, Shuang Ding（BUPT）
- DOI/链接：10.3390/photonics11090885 ｜ https://www.mdpi.com/2304-6732/11/9/885
- 一句话：基于时间标签 QPSK 分区的低复杂度并行 CFO 估计，**含空间分集（spatial diversity）**。
- 验证方式：webReader 抓取确认作者群与"spatial diversity / parallel CFO"主题。
- 覆盖：**(a)存疑　(b)否（仅 FOE/CFO）　(c)否　(d)部分（空间分集，但未见多孔径阵列）**
- ⚠️ **场景证据冲突（必须复核）**：先前 read-note 记为"地面 z=10km"；但本次两次独立搜索（MDPI 标题片段）出现"...for Satellite-to-Ground Optical Communications"字样。两源冲突，**场景（地面 vs 星地）待复核**。若实为星地，则该作同时触及"分集 + 星地"组合。

### 2.3 Single-tone TS — Optics Express 33(10):21660 (2025) 　【abstract-已验证】
- 标题：*Robust multifunctional single-tone training sequence for free-space optical communication in strong turbulence*
- 作者：Kunfeng Liu, Liqian Wang, Mengyao Chen（BUPT）
- DOI/链接：10.1364/OE.558198 ｜ https://opg.optica.org/oe/abstract.cfm?uri=oe-33-10-21660 ｜ PubMed https://pubmed.ncbi.nlm.nih.gov/40515057/
- 一句话：强湍流、低接收光功率下，**单一训练序列同时实现帧同步 + 鲁棒 FOE + 相位校正（phase correction）**，低开销。
- 验证方式：OE 原站 webReader 失败（-500 网络错误），改用 **PubMed 镜像 webReader 成功**，abstract 全文已读。
- 覆盖：**(a)否（地面强湍流 FSO）　(b)部分（"phase correction"贴近 CPE，但非显式 CPE 联合估计算法）　(c)否　(d)否**
- 备注：该作延续 oe.520452 的"单 TS 多功能"思路，但尚未跨入星地，亦未做 Doppler。

### 2.4 SSRN 卫星预印本 — SSRN abstract_id=6293357 (2025) 　【搜索摘要-未验证】
- 标题：*Joint frame synchronization and frequency offset estimation for satellite-to-ground optical communication under low received optical power*
- 作者：Kunfeng Liu, Liqian Wang 等（BUPT）
- 链接：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6293357 ｜ ResearchGate 镜像 https://www.researchgate.net/publication/401111437
- 一句话（据搜索摘要）：**星地（satellite-to-ground）** 光通信、低接收光功率下的**联合帧同步 + 频偏估计**。
- 验证方式：**未完成 abstract 级验证**。SSRN 页面 Cloudflare 安全验证拦截；ResearchGate（401111437）与 Semantic Scholar API 均 -500 网络错误。仅由 SSRN 列表页 + ResearchGate 镜像 + Liqian Wang 作品页**三处搜索摘要交叉印证**标题/作者/关键词（satellite-to-ground / low received optical power）。
- 覆盖：**(a)是（星地，但单链路非分集）　(b)否　(c)否（"frequency offset"指 CFO/FOE，非显式 Doppler 联合）　(d)否**
- ⚠️ **最高风险但最低可信度**：此作是 BUPT 首篇显式"星地"续作，直接触及切口③，但 abstract 未亲验。

### 2.5 OECC 2026 会议文 — 　【会议程序-未验证】
- 标题：*Synchronization for Pilot-Aided DSP in Coherent Optical Satellite Communication*（标题据程序 PDF 摘要）
- 作者：Kunfeng Liu, Liqian Wang, Yiwei Zhao（BUPT）
- 链接：OECC 2026 Final Program https://oecc2026.org/download/program/OECC%202026_Final_Program_260612.pdf （Session Mo1A / 编号 P3-56）
- 一句话（据程序摘要）：**相干光卫星通信**中导频辅助 DSP 的同步。
- 验证方式：**未完成 abstract 级验证**。会议程序 PDF webReader 失败（URL 格式/网络错误）；仅由 3 个版本程序 PDF（Advance 260518 / Final 260610 rev / Final 260612）搜索摘要交叉印证标题/作者/分会场。
- 覆盖：**(a)是（星地相干光，单链路）　(b)否　(c)否　(d)否**

### 2.6 张思齐学位论文 　【未检索到】
- 检索词："张思齐 光通信 载波同步 学位论文" / "张思齐 BUPT CPE 载波恢复"
- 结论：**未检索到**与 FOE↔CPE 联合方向直接对应的张思齐学位论文。
- "张思齐"与 oe.520452 作者"Siqi Zhang"是否同一人/同组：**未确认**（无直接证据）。搜索返回若干 BUPT CNKI 载波恢复相关学位论文，但无一可确认作者为张思齐。
- ⚠️ 此项为本次审计的**已知缺口**，建议主线另派中文库（CNKI/万方）专项核查。

---

## 3. B3-Q2 增量切口覆盖判断

| 切口 | 覆盖状态 | 关键证据 | 置信度 |
|---|---|---|---|
| **① CPE 联合维度** | **部分覆盖（单链路地面级）** | JCSCR(2023, 已验证) 已做 FOE+CPE 联合 carrier recovery，但**单链路、地面 CFSO**，非"分集接收下 CPE 联合"。B3-Q2 切口 = CPE 联合 **在分集接收下** → 该具体组合未被任一篇展示。 | 中-高（JCSCR abstract 已验证） |
| **② Doppler 维度** | **未覆盖（负证据）** | 已验证 abstract（JCSCR/TTQP/OE-single-tone）**无一提及 Doppler 联合估计**；星地续作（SSRN/OECC）的"frequency offset"指 CFO/FOE，非显式 Doppler。jphot-L208"频偏缓变"假设**尚未被任一 Doppler 联合方案推翻**。（注：ResearchGate 383164286 "Coarse FOE short-time spectrum"涉卫星激光 Doppler 仿真，但非联合估计算法。） | 中（基于负证据） |
| **③ 星地场景迁移** | **部分覆盖（场景已入，但单链路非分集）** | BUPT **确已跨入星地**：SSRN 2025(未验证) + OECC 2026(未验证) 均为 satellite-to-ground 相干光，聚焦低接收功率下的 FS+FOE。但**均为单链路**，未见多孔径/分集；亦未叠加 CPE/Doppler 联合。B3-Q2 切口 = 星地 **+ 分集 + (CPE/Doppler 联合)** → 该汇合点未被任一篇覆盖。 | 中-低（关键星地作未验证） |

**关键判读（事实层，非 Go/Kill）：**
- 三切口**均未被单篇 BUPT 续作完整吞没**。B3-Q2 的增量在于**四要素汇合**（FS+FOE+CPE+Doppler，在强湍流分集接收 + 星地场景下）；BUPT 续作目前是**分块占领**：CPE 联合(JCSCR，单链路地面) / 分集 FOE(TTQP，场景存疑) / 星地 FS+FOE(SSRN+OECC，单链路)。
- **但存在"迫近自吞"风险**：BUPT 已集齐全部构件（CPE 联合、空间分集、星地 FS+FOE），2025-2026 持续产出，**12 个月内出现"星地分集 + CPE/Doppler 联合"汇合论文的概率非低**。此为需向主线提示的收敛风险（事实陈述，不含 Go/Kill 建议）。

---

## 4. 结论

1. **BUPT 课题组身份确认**：Liqian Wang / Kunfeng Liu / Siqi Zhang / Shuang Ding / Mengyao Chen / Xinyu Tang / Yiwei Zhao 属同一 BUPT FSO 相干接收研究群，2024-2026 持续产出续作。
2. **2024+ 续作至少 5 篇**：JCSCR(2023,CPE联合) / TTQP(2024,分集FOE) / OE-single-tone(2025,强湍流单TS) / SSRN-卫星(2025,星地FS+FOE) / OECC2026(星地导频DSP)。其中后 2 篇 abstract 未亲验（未验证）。
3. **三切口覆盖**：CPE 联合=部分覆盖(单链路地面)；Doppler=未覆盖；星地=部分覆盖(场景已入、单链路非分集)。**汇合点（四要素 in 星地分集）未被任一篇吞没**。
4. **张思齐学位论文**：未检索到；与"Siqi Zhang"同组关系未确认（已知缺口，建议 CNKI 专项）。
5. **风险提示（事实层）**：BUPT 构件齐全、产出活跃，"迫近自吞"风险存在；具体 Go/Kill 判定属主线职责，本审计不下结论。

---

## 5. 证据可信度声明

| 证据等级 | 论文 | 说明 |
|---|---|---|
| **abstract-已验证**（webReader/PubMed 直读 abstract） | JCSCR 2023（webReader/MDPI）；OE single-tone 2025（PubMed 镜像）；TTQP 2024（webReader/MDPI，作者+主题已验，**场景待复核**） | 可作覆盖判断主依据。 |
| **搜索摘要-未验证**（多引擎交叉但 abstract 未亲验） | SSRN 6293357 2025；OECC 2026 | SSRN 受 Cloudflare 拦截；ResearchGate/Semantic Scholar 均 -500 网络错误；OECC 程序 PDF 抓取失败。仅 2-3 搜索引擎摘要交叉印证，**不得单独作 Go/Kill 依据**。 |
| **证据冲突-待复核** | TTQP 场景（地面 z=10km vs "Satellite-to-Ground"）；OE 520452 标题（搜索摘要误植"satellite-to-ground"，与 read-note 地面 20km 冲突，疑搜索引擎混淆） | 以已验证 read-note 为准，搜索摘要存疑。 |
| **未检索到** | 张思齐学位论文 | 无任何命中，不臆造。 |

**执行完成度声明：**
- 本次执行聚焦 abstract 交叉验证与覆盖判断，**主体已完成**。
- **未完成项**：SSRN 6293357 与 OECC 2026 的 abstract 级亲验（网络/反爬受阻），已按准则③标记"未验证"；张思齐学位论文 CNKI 专项核查未做（本工具无中文库能力），已标记"未检索到/已知缺口"。
- 本审计**仅报告事实，不含 Go/Kill 建议**（准则①）。所有"未验证"条目在主线决策前应补验。
