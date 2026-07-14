# [S003] 参考文献从 12 条扩到 20 条 + 官方要求核实

> 2026-07-15 | 阶段：投稿准备（参考文献扩展） | 状态：完成

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

## 决策引用

- 无新建 D###（本轮无架构/方向决策，纯执行）
- topic-index 未决项 1+4 已更新（官方要求核实结果）

## 范围确认

- 本轮是否在 scope boundary 内：是（参考文献扩展属本专题"引用资产"范围，不动正文数字/口径/方法描述——不变量 7 守住）

## 后续

- 8 条新补文献的引用位置都是单点补引（每个补引点加 1-2 条 cite），未改动正文任何句子结构或数字
- 待主办方确认：2026 是否进 IEEE Xplore / 双盲匿名措辞（不阻塞当前投稿，但正式投稿前需确认）
- 第 7 页参考文献尾部留白（S002 已登记的债务）本轮未处理——补 8 条后参考文献区变长，留白应减小，但未专门做版面优化
