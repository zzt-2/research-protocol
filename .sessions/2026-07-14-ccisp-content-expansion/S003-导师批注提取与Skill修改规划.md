# [S003] 导师批注提取与 Skill 修改规划

> 2026-07-17 | 阶段：导师反馈提取 / Skill 规划前置 | 状态：IN PROGRESS

## 目标

从 `projects/simulation/paper/ccisp2026/ccisp_v1 批注.pdf` 中完整提取导师对 CCISP 论文的修改意见，保留用户补充的逐字纠正；在用户确认提取结果后，将意见甄别为论文局部修改、可复用检查项、高层写作原则、流程/Skill 漏检和格式硬门，形成 Skill 修改规划。当前阶段只做提取、证据定位和分类，不修改论文正文或 Skill。

## 用户原话（逐字记录）

### 2026-07-17：任务目标

> “老师给出了几十条修改意见。从长度，到删句，到格式，，到内容，到参考文献。非常全面。我需要有一个规划，去依照这批珍贵的反馈，修改我的skill。它们中有的或许可以拔高到更高层次，有的只是一些小小修改。你需要自己甄别。理解要做什么了吗？待会我给你”

> “非常多。但我自己手动写太慢。因此，你先让subagent提取一下，我看看然后给你补充或者纠正。”

输入文件：

`D:\code\study\research-protocol\projects\simulation\paper\ccisp2026\ccisp_v1 批注.pdf`

### 用户对首次提取结果的逐字补充/纠正

> “引言中从 **“This paper develops...” 到 “We evaluate...”** 的两段被高亮，一直到"on a common non-pilot payload."，这段后面的内容被划了。与此同时，老师提问"上一版的The remainder of the paper is organized as follows.怎么没有了"

> "Recent coherentFSO receiver studies address these impairments through digital phase-locked loops, adaptive optics, and multi-aperture DSP [3], [8], [9]."、"The square root is required because irradiance scales signal power, whereas the complex-baseband coefficient scales amplitude."被划掉了。（我只是补充一下，不知道你看没看见。）

> “图3的HD-FEC被圈出，问什么意思（最好别写？或者只在正文解释）”

> “图例应该在仿真图上标出来，而不是单独写。这个应该指的是图3、4、5”

> “我大概补的是可能没看清的，我也不知道你到底知不知道。”

### 用户对当前日志的要求

> “我补完了。你一定要写一个完整日志，把这次相关的一字不差的写进去，包括你的推演过程、分析过程。topic里一定要写明这次是什么”

> “然后，说要到第5页的最后一行，也就是整整好的5页
> 论文作者：张哲铜、吴浩（标注出通信作者，wuhao@bit.edu.cn）
> 论文作者：张哲铜、吴浩（标注出通信作者，wuhao@bit.edu.cn）”

> “你直接往下推吧？先改skill，然后规划怎么去改论文（要挖同类问题，不要再踩坑）。规划一个严谨的流程，再去推。尽量一次改好。（改完要逐条检查）”

## 记录

### 1. Skill 触发与执行边界

本轮使用 PDF 文档读取流程，先读取 PDF skill；由于用户要求先由 subagent 提取，且项目规则要求大量 PDF/全文消化委托给子 Agent，因此未由主控直接逐页消化批注。主控只负责范围、结构化整合和最终分类，不提前修改论文或 Skill。

派发的提取约束是：只提取原始意见，不做 Skill 设计；同时使用 pypdf/pdfplumber 检查 annotation 对象，并用页面渲染确认批注归属；区分批注文本、正文高亮/删除线和基于圈选的推断。

### 2. 批注 PDF 提取事实

Subagent 完成了 7 页 PDF 的对象提取和逐页视觉核对：

- 关联对象总数：75；
- Popup 批注气泡附属对象：30；
- 实际非 Popup 可见批注：45；FreeText 15、Ink 15、Highlight 8、StrikeOut 7；
- pypdf 对 4 个对象指向给出错误提示，但不影响 PyMuPDF 与页面渲染的可见批注核对；
- 首次提取概括为 20 条意见，后经用户补充修正引言高亮范围、删除线和图例适用范围。

### 3. 首次提取的意见清单（保留提取结果及证据等级）

#### p1：标题与引言

1. 标题 “Received Power-Aware” 被划线；是否要求删除该短语尚待用户确认。
2. “This paper develops...” 到 “We evaluate...” 两段被高亮；首次提取理解为两段都是本文工作，应合并，避免工作段落拆散。用户随后明确范围延伸至 “...on a common non-pilot payload.”。
3. Introduction 第二段关于国内外研究现状的分析过少；该意见明确要求增加分析，不是简单堆引用。
4. “Data-aided (DA) and non-data-aided (NDA) carrier estimators offer complementary phase references.” 被批注：应写 DA 和 NDA 是两类方法，而不是用“互补”定义它们。
5. 老师问上一版的 “The remainder of the paper is organized as follows.” 为什么没有了；用户随后确认该结构概述句应恢复。
6. 方程（3）附近要求给出随机变量的数学分布，指向 epsilon_l 相位噪声增量及其参数。
7. 多处删除线包括标题首段、Recent coherent-FSO studies 段以及 “The receiver uses one parameter configuration across all three regimes and does not use the post-simulation curve crossover as an online input.”；应结合用户补充逐句判定，不能将全部删除线自动升级为通用规则。

#### p2：模型与公式

8. 方程（2）/湍流参数段旁要求有引用；映射和三档参数需要紧邻证据来源。
9. “The average pre-fading SNR ... separate experimental coordinate ...” 整段删除线；倾向删除重复的 SNR 坐标解释。

#### p3--p4：方法解释

10. DA/NDA 术语再次被高亮，与第 4 条同属术语定位问题。
11. CV 公式旁批注“需要解释”；不能只给定义，还要解释统计含义和为什么用于窗口筛选。

#### p5--p6：图与结果

12. Fig.3 图例及四小图被圈出，批注为：“1、图例应该在仿真图上标出来，而不是单独写”“2、这四个图的信息，能否放在一张图”。用户补充确认图例规则应适用于 Fig.3、Fig.4、Fig.5。
13. Fig.4 图例/标注被圈出，批注为：“1、不写约等号”“2、字不能互相遮挡”“3、标注这3个点的意义是什么，需要在正文中说明”；“同理”表示同类图表问题需统一处理。
14. AWGN 处批注“缩写在第一处出现解释，这里不是第一次出现”；首次出现应展开 additive white Gaussian noise (AWGN)，后续使用缩写。
15. Results 仿真设置/性能指标段被大范围圈选，但无明确文字；此项只能标作版面/组织推断，不能冒充老师明确原话。
16. “Two qualifications matter...” 整段被删除线；倾向删除防御性、元话语式说明。
17. Fig.5 图例被圈出；与第 12 条合并为三张定量图的统一图例门。
18. p6 批注“大幅降低对会议的引用”；期刊、Transactions、JLT、PTL 等高质量来源优先。
19. Results 末尾 “Both recovery branches are selected...” 和 “Together, the fixed and adaptive results...” 两段被删除线；倾向删除重复、防御性叙述及再次声称 stand-alone estimator 的内容。

#### p7：参考文献排版

20. 参考文献区域整体被圈出，批注“排版：双栏高度应一样”；末页参考文献双栏高度应尽量平衡。

### 4. 用户补充后对关键意见的重新解释

#### 4.1 “本文工作”段落范围

用户明确指出，高亮范围从 “This paper develops...” 一直到 “...on a common non-pilot payload.”。因此当前解释不是只合并两句方法介绍，而是把方法、评价设置和共同 payload 比较这一整段作为连续的本文工作段落处理。其后的 “The receiver uses one parameter configuration...” 被划线，不能继续作为独立防御性说明保留。

#### 4.2 结构概述句不能因压缩被误删

虽然部分结果/限制性句子被划掉，但老师特别追问上一版的 “The remainder of the paper is organized as follows.” 为什么消失。因此该句应作为论文组织导航保留，不能因为“压缩引言”而一并删除。

#### 4.3 两处删除线是明确删除信号

用户补充确认以下两句被划掉，而不是普通“需要改写”：

- “Recent coherent-FSO receiver studies address these impairments through digital phase-locked loops, adaptive optics, and multi-aperture DSP [3], [8], [9].”
- “The square root is required because irradiance scales signal power, whereas the complex-baseband coefficient scales amplitude.”

因此后续 Skill 规划应区分“删除无效泛化句”与“补充相关工作分析”两个动作，不能删除前者后又用同样空泛的一句话补回。

#### 4.4 Fig.3 的 HD-FEC

HD-FEC 被圈出且老师问“什么意思”。当前不应默认保留图中缩写。待正文修改时有两种候选：若该阈值对结果判断不可缺，则在正文第一次出现处写出全称并解释，图中只保留必要短标识；若不是论文核心指标，则从图中删除，避免图内出现未定义缩写。是否删除 HD-FEC 本身仍是论文局部决策。

#### 4.5 图例适用范围

用户明确确认老师关于“图例应该在仿真图上标出来，而不是单独写”的意见适用于 Fig.3、Fig.4、Fig.5，而非 Fig.3 单图。后续应建立统一图例规范，并分别检查图例位置、遮挡、marker/线型含义和正文解释。

#### 4.6 终稿页面与作者元数据

用户补充了硬格式要求：论文必须到第 5 页的最后一行，不能只满足“5 页以内”；作者为张哲铜、吴浩；吴浩应标注为通信作者；通信作者邮箱为 `wuhao@bit.edu.cn`。作者信息属于论文元数据核对，不自动提升为通用写作原则；“恰好填满 5 页”属于当前投稿格式硬门，后续需在 PDF 终验中单独检查。

### 5. 主控分析与分类（决策相关摘要，不伪装成隐藏推演）

本轮的分析不是把 20 条意见等量写进 Skill，而是按作用范围和可重复性分层：

1. **论文局部动作**：删除标题短语、恢复 remainder 句、删除两句明确划线文本、处理 HD-FEC、是否合并 Fig.3 panel、删除具体 SNR 解释段。它们必须先服务本篇论文，不能直接写成普遍规则。
2. **可复用写作检查项**：引言工作段不拆散；相关工作必须有方法关系分析；方法类别先定义再讨论关系；公式后解释统计意义；随机变量首次出现给出分布；缩写首次出现展开；图例直接嵌图且三图统一；图内标注不遮挡并在正文解释；删除防御性和重复性元话语。
3. **流程/Skill 漏检候选**：当前 Skill 可能缺少“批注删除线/高亮范围与正文段落职责联合审查”“图中缩写—正文定义交叉检查”“最终页面硬门与末页平衡”三个独立门。是否修改 Skill，必须先核对现有 Skill 是否已有同等规则以及为何未触发，不能重复加条款。
4. **高层规则候选**：意见共同指向信息层级、读者导航、图文职责和版面终验，而不是单纯“多写/少写”。后续应优先组织成少数高层原则，再落到可执行 checklist 和测试，不建立几十条孤立禁令。
5. **证据边界**：第 15 条 Results 大圈是视觉推断，不能写成老师明确要求；标题删除短语是否确定，仍需用户确认；HD-FEC 是删掉还是正文解释，也仍需用户拍板。

## 决策引用

- 无新 D### 决策。本轮完成导师反馈提取、用户纠正归档和 Skill 修改规划前置；具体 Skill 修改方案待用户确认后再建 D###。

## 范围确认

- 本轮是否在原 T018 论文闭环范围内：否，用户明确将当前范围扩大为“基于导师批注规划 Skill 修改”。
- 该范围扩展已由用户在本轮明确提出；当前只做记录和规划，不执行 Skill 修改，不改论文。

## 后续

1. 用户确认/纠正本日志中的 20 条意见、引言高亮范围、Fig.3--5 图例适用范围、正好 5 页硬门和作者信息。
2. 主控读取现有 `paper-writing`、`external-output` 和相关论文 QA Skill，建立“现有规则—老师意见—漏检原因”矩阵。
3. 将意见分成一次性论文改动、可复用规则、流程门控和测试/验证产物，提出 Skill 修改合同；未经用户确认不写入 Skill。

## 2026-07-17 续接：Skill 实施与论文统一修订合同

用户已明确批准从规划进入实施。主控先对现有 `paper-writing` 与项目 `external-output` 做了旧版压力测试，确认旧流程会系统性漏掉：把“正好 5 页”降级为“不超过 5 页”、只改批注点而不扫描全文同类问题、以“互补”定义 DA/NDA、三图统一但图例仍在图外、只数引用不核论证职责、先做排版再修论证，以及作者元数据与末页双栏平衡漏检。

已实施的 Skill 变更包括：新增导师/审稿反馈证据账本、批注证据层级、逐条 disposition 与同类扫描、项目专属硬门和可复用规则分层、先结构与证据后版面、实际阅读顺序缩写检查、图内图例/标注/裁切检查、作者元数据与精确末页占用检查、fresh build 与独立 reviewer 核销。旧版 RED 与新版 GREEN 压力测试均已保存，新版可稳定提出本次 45 条批注驱动的完整修订状态机。

论文修订冻结为一个统一批次，顺序为：

1. 先锁论证链与全文同类问题：标题/方法身份、DA/NDA 类别定义、贡献—评价段合并、相关工作关系分析、明确删除线、随机变量/CV/SNR 职责、内部验证语言外溢。
2. 再修三张定量图：图例入图并统一，Fig.3 的 HD-FEC 去除或在首次可见处自包含，Fig.3 单轴合并只做可读性 spike，Fig.4 去近似号并消除标注碰撞。
3. 再按论证职责与来源质量精简会议引用；不机械删除 Transactions/JLT/PTL，不以引用数量代替相关工作分析。
4. 内容稳定后才处理作者元数据与正好 5 页版式，最后 fresh build、逐页视觉 QA、确定性 grep、21 项账本逐条核销和独立 reviewer 终验。

冻结边界：不改仿真参数、selector、算法、seed/window/metric、正式数据与结果；不覆盖用户维护的 Fig.1/Fig.2 drawio；不以灌水、弱引用、过度缩图、负间距或删除有效性边界凑页。标题划线虽有批注明确信号，但修改日志保留其证据性质；作者单位只采用仓库已有正式证据，绝不猜测。

## 决策引用（续接）

- D024：批准导师批注驱动的 Skill 门禁升级与论文统一修订合同（新建）。

## 2026-07-17 实施闭环：Skill、论文、正式重跑与逐条终验

本轮没有把导师批注机械翻译成几十条孤立禁令，而是先做旧 Skill 压力测试，再把共性归并为五个可复用门：批注证据账本与证据层级、逐条 disposition 及全文同类扫描、论证/证据先于版面、图文与实际阅读顺序检查、fresh build 后的精确页数/末行/独立 reviewer 核销。`paper-writing` 新增 `reviewer-feedback.md` 与 advisor-feedback pressure cases，`external-output` 新增论文场景和出门检查项；RED 旧版确实漏掉精确五页、同类问题扫描、图内图例、作者元数据和末页平衡，GREEN 新版均能触发。

论文按 D024 的单一批次完成：标题落在 adaptive CPR algorithm；DA/NDA 定义为两类 carrier-recovery algorithms；贡献与评价段合并并恢复 remainder 句；删除导师划线句和 Results 中三段无职责元话语；相关工作按方法关系与缺口组织；补齐随机变量分布、CV 统计意义和公平性职责；去除 uplink、26/29、HD-FEC 与旧代理数字；保留 18 条实际引用且 conference=0；作者为 Zhetong Zhang、Hao Wu，Hao Wu 标注通信作者及 `wuhao@bit.edu.cn`。Fig.1/Fig.2 用户权威资产未覆盖。

三张定量图统一为图内图例。Fig.3 为单轴 12 曲线，横轴严格 5--35 dB、2 dB 主刻度，图例使用专业缩写 `AWGN`，不含 HD-FEC；Fig.4 标出并解释 14.5/16.0/16.9 dB 三个 DA--NDA BER 交点；Fig.5 使用正式 paired common-payload BER-ratio reduction 与 95% CI。

独立 reviewer 首轮发现 A/B JSON 的 `params_sha256=a1d5f051...` 已落后于当前 `params.py=fac6d229...`。漂移仅来自后来新增 fixed-SNR 网格常量，但 T018 的整文件权威签名合同不允许手改元数据，因此主控在不改参数、selector、CV、1.10 margin、13 dB、seed/window/metric 的前提下原样重跑 route A 与 route B，各 990 cells。正式 verifier 随后 PASS；A/B/fixed 均绑定 `fac6d229...`，A/B 990/990 exact，route B 的 fixed-NDA/oracle/gain 结构性字段均为 null。

最终 clean build 恰为 5 页。bibliography-only 采用温和的 1.03 baseline stretch，不增加灌水文字、不缩正文、不用负间距；末页最深文本 y=713.219 pt，距同模板最后正文带 5.63 pt，小于一个正文基线，进入最后允许行带。左右底线差约一个参考文献基线，视觉可接受；无 overfull、undefined citation/reference。最终测试 37 passed、1 个用户 Fig.1 原资产已知 xfail；21 项导师反馈账本经独立 reviewer 全部 PASS。

## 决策引用（实施闭环）

- D024：按导师批注升级 Skill，并以统一修订合同执行全文同类问题扫描和逐条终验。
- D019：三档参数冻结不变；本轮重跑只恢复当前真相源的权威签名。

## 范围确认（实施闭环）

- 本轮是否在扩展后的 scope boundary 内：是。
- 未覆盖用户维护的 Fig.1/Fig.2 drawio，未重新选择参数，未调整 selector 或实验口径。

## 后续（实施闭环）

无。论文与 Skill 修改均已达到 V026 PASS；后续由用户按最新版全文挑选新的内容问题。

## 2026-07-17 续修：Fig.2 页位纠正与引用/专业性复核

用户复核提出两点：确认 Transactions 不能被误删、文字专业性需再核对，并要求 Fig.2 从第 4 页回到第 3 页。实际 PDF/BibTeX 检查确认 IEEE Transactions on Communications、IEEE Transactions on Information Theory、IEEE Transactions on Signal Processing 等条目仍在；当前实际引用 18 条，conference=0。

页位根因是双栏 `figure*` 在 System Model 内容之后排队，而第 3 页仍承载 System Model 尾部，因而原先只能到第 4 页。直接把图提前会使其落到第 2 页并扩成 6 页，因此被否决。最终采用最小布局修复：保持 Fig.2 在 System Model 之后，将 System Model 中两处重复性分区说明等义压缩，使其不再溢出到第 3 页；Fig.2 随即落在第 3 页顶部。没有改图资产、参数、结果、方法逻辑或引用职责。

fresh build 仍为 5 页；第 3 页顶部可见 Fig.2，随后进入 Method；无 overfull、undefined citation/reference。针对当前源重跑图形/正式契约测试为 35 passed、1 known xfail；独立 reviewer 待对页位改动进行最后只读核验。

## 决策引用（续修）

- D024：图表与专业性门禁继续有效。
- 无新架构决策；本次为已批准论文版式与等义压缩修复。

## 范围确认（续修）

- 本轮是否在 scope boundary 内：是。

## 后续（续修）

独立 reviewer 完成当前 PDF 的第 3 页 Fig.2 页位和全文版式回归后，更新 V027。

## 2026-07-17 续修：摘要/正文缩写首次定义

用户确认标题中的 FSO 不处理，并要求按“摘要和正文分别定义一次”修复缩写。按 PDF 实际阅读顺序完成：摘要内部定义 CPR、DA、NDA；正文 p1 依次定义 FSO/CPR、DA/NDA/APSK、DSP/SNR/BER、16APSK/CV/AWGN。AWGN 与 CV 的正文定义放在引言贡献段，早于 p2 Fig.1 和 p3 Fig.2 的图内缩写；图注及后续 System Model/Method/Results 不再重复展开。

fresh build 仍为 5 页，Fig.1 p2、Fig.2 p3；35 passed、1 known xfail。独立 reviewer 按标题、摘要、正文、图和图注的实际顺序复核后判定 PASS；APSK 为通用调制族、16APSK 为具体 16 阶格式，分别定义不属于重复。

## 决策引用（缩写续修）

- 无新决策；标题 FSO 是本轮用户明确豁免项。

## 范围确认（缩写续修）

- 本轮是否在 scope boundary 内：是。

## 后续（缩写续修）

无。
