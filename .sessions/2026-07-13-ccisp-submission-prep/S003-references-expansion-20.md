# [S003] 参考文献从 12 条扩到 24 条 + 官方要求核实 + venue 结构调整

> 2026-07-15 | 阶段：投稿准备（参考文献扩展 + venue 调整） | 状态：完成
> 2026-07-15 续接 1（venue 结构调整：补现代 IEEE Transactions）
> 2026-07-15 续接 2（再补 Trans：第 2 轮深度检索 + 库内重评）

## 目标

①核 CCISP 2026 官方投稿硬约束（页数/篇数/模板/截稿）；②若篇数允许，把参考文献从 12 条扩到 20 条，含金量 IEEE 优先，格式零误差。

## 记录

### Step 1：官方要求核实（子 agent）

派子 agent 从 ccisp.org 官方来源核实，结论：

| 项 | 官方硬约束（来源 ccisp.org/sub.html） | 当前状态 |
|---|---|---|
| 页数 | 5-10 页（明文 "no less than 5, no longer than 10"），含参考文献 | 7 页 ✅ |
| 篇数上限 | **官方未规定** | 12→20 无约束 |
| 截稿 | 7/20（WikiCFP + special session 页交叉印证） | 与用户一致 |
| 模板 | 官方提供 LaTeX 模板下载，未明文 IEEEtran（S001 已核硬门通过） | IEEEtran conference 在用 |

- "4-6 页"非官方要求（旧任务口径），争议解决。topic-index 未决项 1+4 已更新。
- 待主办方确认项（不阻塞参考文献扩展）：2026 是否进 IEEE Xplore / 双盲匿名措辞 / 官网首页未更新到 2026。

### Step 2：缺口盘点

**库内扫描**（explore agent 扫 papers/ 全树 ~362 个 content.md）：找到 30 篇候选（17 篇 IEEE），全部 8 主题有覆盖。

**Shieh-Djordjevic 教材缺口核实**：system_model.tex eq:pilot-energy-coordinate 的 `Δp=10log10(4/3)=1.249dB` 是从 pilot 密度 ρ=1/4 直接推导的基本数学，**不需引教材来源**——提示词标的这个"缺口"不成立，不补。

**He SPIE'24 / Xu PTL'26**：库内无 content.md（download failed），按"不引未核实文献"原则不补。

**二次引用**（用户 fallback 提示）：本轮库内候选充足（30 篇），未启用二次引用路径。

### Step 2b：确定 8 条 + 元数据核实

按"补引点有明确学术理由，不硬塞"原则，从候选中选 8 条，每个对应一个自然补引位置：

| # | citekey | venue | IEEE? | 补引位置 | 学术理由 |
|---|---------|-------|-------|---------|---------|
| 1 | taylor2009phase | JLT 2009 | ✓ | intro "CPR central function" | CPR DSP 方法经典综述 |
| 2 | guiomar2022coherent | JLT 2022 | ✓ | intro "coherent reception attractive" | 相干 FSO 机会与挑战综述 |
| 3 | wang2022jointml | TSP 2022 | ✓ | intro "extends to APSK" | Kam 组 ML/MAP 相位估计理论 |
| 4 | du2021jointml | JLT 2021 | ✓ | intro "extends to APSK" | du2025nda 前置期刊版 |
| 5 | liu2023multiaperture | JLT 2023 | ✓ | sys_model "Gamma-Gamma model" | 多孔径相干 FSO+GG 湍流 |
| 6 | conroy2018geouplink | Appl Opt 2018 | ✗ | sys_model "scintillation slower" | GEO feeder 上行相干+湍流 |
| 7 | horst2023tbit | Light:S&A 2023 | ✗ | sys_model "HD-FEC 3.8e-3" | Tbit/s 相干 feeder link 用 HD-FEC（Nature 子刊） |
| 8 | martins2021dualstage | OSA Continuum 2021 | ✗ | method "M0th-power" | 双级 pilot+BPS CPR，DA/盲混合原始方法 |

IEEE 5 / 非 IEEE 3。非 IEEE 3 条含金量足：Conroy 是 Applied Optics 经典外场实验，Horst 是 Light: Science & Applications（Nature 子刊），Martins 是 OSA Continuum 的 DA/盲混合方法原始文献。

**元数据核实**（两批子 agent，Crossref + Semantic Scholar 交叉验证）。发现并修正的差异：
- taylor2009phase：**单作者** Michael G. Taylor，year **2009**（非 2008，DOI 含 2008 是在线发表年），vol 27 no 7 pp 901-914
- liu2023multiaperture：标题 "2N²" 应为 **"2N × 2"**（乘号 U+00D7），Crossref/S2 双源确认，库内正文亦通篇用 "2N × 2"
- conroy2018geouplink：末页 5103→**5101**（Optica 落地页 + S2 确认），作者全名展开（Philip/Janis/Juraj/Ramon），复合姓 Mata Calvo
- martins2021dualstage：Crossref 只返回首页 3157，库内全文页眉证实完整范围 **3157-3175**
- guiomar2022coherent：DOI 原未知（manual 目录），已定位 **10.1109/JLT.2022.3164736**

### Step 3：补到 20 + 格式零误差自检

**citekey 集合核对**（python 脚本）：bib 20 条 = 被引 20 条，**零闲置零缺漏**。

**fresh latexmk compile**（clean 后重编）：
- PDF 7 页（满足官方 5-10 页）
- `.blg`：0 警告 0 错误
- `.log`：0 undefined citation，0 overfull/underfull，0 LaTeX Warning
- 字体全部嵌入（emb=yes + sub=yes）
- `.bbl` 逐条抽查 8 条新条目：作者缩写/venue 斜体/页码/year/重音字符全部正确

### Step 4：venue 结构调整（续接，补现代 IEEE Transactions）

**触发**：用户指出 venue 构成问题——"参考论文不能一大片的会议；transactions 目前只有 2 篇，其中 1 篇还是 1983 年的"。

**venue 分类盘点**（22 条最终状态前，20 条时）：
| 类型 | 篇数 | 备注 |
|------|------|------|
| IEEE Transactions | 2 | viterbi1983(TIT,1983) + wang2022jointml(TSP,2022)——**现代仅 1 篇** |
| JLT | 6 | paillier/smith/taylor/guiomar/du2021/liu2023 |
| PTL | 1 | du2025nda |
| 其他期刊 | 6 | valjus/alhabash/wang2025/horst/conroy/martins |
| 会议 | 5 | johst/lebidan/panasiewicz/ma/pech |

**补强**（用户选"新检索 IEEE Transactions 补强"）：
- 派子 agent 用 tools/search 检索（7 条查询归档 search-archive/2026-07-15/）。命中 3 篇候选：Liu/Du TCOM 2025（ML 相位估计，最对口）、Zedini TWC 2026（FSO+IRS，偏离核心，不引）、Qin TCOM 2026（VAE 盲均衡，偏离，不引）。
- 库内 gavert TCOMM 2022（pilot 相位噪声估计，有 content.md）作保底。
- 最终补 **gavert2022pilot (TCOMM 2022) + liu2025tdml (TCOM 2025)** 两篇，均为 IEEE Transactions on Communications，与论文 pilot/ML 相位估计方法论直接相关，非凑数。
- liu2025tdml 库内无 content.md，Crossref+S2 双源确认真实存在（IEEE doc 10813584, vol 73 no 7 pp 5018-5034 2025）。
- IRS 和 VAE 两篇明确**不引**（偏离论文核心 DA/NDA 切换方法，凑数风险高）。

**补引位置**（不硬塞，学术理由明确）：
- gavert2022pilot → intro 第 2 段 "A DA receiver inserts known pilot symbols... fit the carrier evolution"（pilot 相位噪声估计理论）
- liu2025tdml → intro "extends to APSK" ML 理论 cite 群（跟 wang2022jointml/du2021jointml 同群，时域 ML 相位估计）

**自检**：citekey 22=22 零闲置零缺漏；fresh compile **8 页**（Conclusion 在第 7 页，参考文献溢出到第 8 页——正文未变多，是 20→22 条 ref 自然溢出），0 overfull/0 underfull，blg clean，0 undefined，字体全嵌入，.bbl 两条新条目格式正确。

**venue 分布改善**（20→22）：
| 类型 | 调整前 | 调整后 |
|------|--------|--------|
| IEEE Transactions | 2（现代 1） | **4（现代 3）** |
| 会议 | 5 | 5（不动，对标核心） |

### Step 5：再补 Trans——第 2 轮深度检索 + 库内重评（续接）

**触发**：用户"没办法再多点吗"——希望现代 Trans 更多。

**第 2 轮深度检索**（换 3 角度共 12 条查询：JOCN 专向 / 光纤 CPR 方法论经典 / OJ-COMS+DA-NDA 切换概念）：**0 合格候选**。两轮共 19 条查询挖尽，确认领域现实——相干 FSO + CPR 的 IEEE Transactions 级文献本身稀疏，方法论源头几乎全在 JLT/Optica 系（Kikuchi、Faruk&Savory、Zhang&Kam、Du/Kam 系列）。

**库内重评**（用户选"补 qin TCCN + 放宽引 JLT"）：
- **qin2026blindvae**（IEEE TCCN 2026）：上轮因"VAE"否决过严。重看 content.md 发现是**双偏振相干 FSO + 湍流 + blind 均衡**（对抗 CMA/CMMA），基金含"星地激光通信"，跟 NDA(blind) 分支有真实交集。补入，现代 Trans 3→4。
- **zhang2010decisionaided**（JLT 2010）：Decision-Aided Carrier Phase Estimation，"decision-aided"直击 DA 概念源头。放宽 venue 规则引作方法论溯源。Crossref 核实修正：标题是"...for Coherent Optical Communications"（非 QPSK），**4 作者**（Shaoliang Zhang, P.-Y. Kam, C. Yu, Jian Chen），vol 28 no 11 pp 1597-1607。

**补引位置**：qin2026 → intro NDA/blind 描述句（modulus-based equalizer 并行方向）；zhang2010 → intro DA pilot 句（跟 gavert 同群，DA 方法论源头）。

**自检**：citekey 24=24 零闲置零缺漏；fresh compile 8 页，0 overfull/0 underfull，blg clean，0 undefined，字体全嵌入，.bbl 两条新条目格式正确。

**venue 分布最终态**（24 条）：IEEE Transactions **5**（现代 4：wang2022/gavert/liu2025/qin2026）/ JLT 7 / PTL 1 / 其他期刊 6 / 会议 5。现代 IEEE Transactions 从最初 0→4。

**领域现实结论**：19 条查询挖尽后确认，5 篇 IEEE Transactions 已是该细分领域 Trans 资源的合理上限，再补只能凑数（IRS/VAE/水下/中继等偏离核心）。JLT 虽不带 Transactions 名但是该领域顶刊，zhang2010 作 DA 方法论溯源补入合理。

## 决策引用

- 无新建 D###（本轮无架构/方向决策，纯执行）
- topic-index 未决项 1+4 已更新（官方要求核实结果）

## 范围确认

- 本轮是否在 scope boundary 内：是（参考文献扩展属本专题"引用资产"范围，不动正文数字/口径/方法描述——不变量 7 守住）

## 后续

- 12 条新补文献（Step 3 的 8 条 + Step 4 的 2 条 + Step 5 的 2 条）的引用位置都是单点补引，未改动正文任何句子结构或数字
- 待主办方确认：2026 是否进 IEEE Xplore / 双盲匿名措辞（不阻塞当前投稿，但正式投稿前需确认）
- PDF 8 页（参考文献 20→24 自然溢出，正文仍到第 7 页 Conclusion），8 页在官方 5-10 页范围内
- venue 结构已大幅改善（现代 IEEE Transactions 0→4），19 条查询挖尽确认 5 篇 Trans 是领域上限，会议 5 篇为 R016 对标核心不宜动
- 领域现实：相干 FSO + CPR 的 IEEE Transactions 级文献本身稀疏，方法论源头在 JLT/Optica 系，不宜为凑 Trans 数而引偏离核心的论文


## 决策引用

- 无新建 D###（本轮无架构/方向决策，纯执行）
- topic-index 未决项 1+4 已更新（官方要求核实结果）

## 范围确认

- 本轮是否在 scope boundary 内：是（参考文献扩展属本专题"引用资产"范围，不动正文数字/口径/方法描述——不变量 7 守住）

## 后续

- 8 条新补文献的引用位置都是单点补引（每个补引点加 1-2 条 cite），未改动正文任何句子结构或数字
- 待主办方确认：2026 是否进 IEEE Xplore / 双盲匿名措辞（不阻塞当前投稿，但正式投稿前需确认）
- 第 7 页参考文献尾部留白（S002 已登记的债务）本轮未处理——补 8 条后参考文献区变长，留白应减小，但未专门做版面优化
