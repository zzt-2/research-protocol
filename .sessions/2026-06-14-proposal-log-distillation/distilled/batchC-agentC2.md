# batchC agent-C2 产出（C 维写作范例 few-shot 后半 9 素材源）

## 提取统计
- 处理素材源：9（其中 C14 = 3 文件算 1 批次，各提 2 条）
- 产出条目：C=24（C-501~C-524）
- id 区：C-5xx
- 行号校准：C14 三文件千行级读开头+代表性段；C15 S004模板L23-42/L46-70/L88-110；C16 L12-32/L48-63/L107-150；C17 实际258行全扫；C18 挑代表性5张；C19 L237-265；C20 实际321行（R002标445有误）；C21 L108-152；C22 L50-84

## C 维度

```yaml
id: C-501
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/writing-patterns-paragraph.md:14"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "章引言段两段式（董凡推荐模板）：第1段问题驱动（随着…不断提升，传统的…已难以满足…→然而…低复杂度也同样重要）→第2段前章回顾+本章预告（本论文在第X章中介绍了…，本章将…）"
why_good: "问题驱动开篇而非背景罗列，第2段用'第X章…本章将…'完成跨章衔接+本章预告三合一，是章首段黄金结构"
fewshot_target: "S033'段落衔接改写'——章引言段两段式骨架（问题驱动+前章回顾+本章预告）"
```

```yaml
id: C-502
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/writing-patterns-paragraph.md:108"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "节间过渡段三句式（董凡推荐）：前节效果总结（1句，'通过定时同步…有效提升了…'）→ 剩余问题（'仍将存在频率偏移和相位偏移'）→ 引出后节需求（'因此需要进一步设计…'）"
why_good: "过渡段不是空话衔接，而是'已完成什么+还剩什么+因此下一步做什么'的因果链，前节效果必须是后节需求的前提"
fewshot_target: "S033'段落衔接改写'——节间过渡段'前效→剩余→后需'三句式"
```

```yaml
id: C-503
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/writing-patterns-paragraph.md:746"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "参数优化段六步法骨架：①参数介绍(1句:名称+物理含义+影响范围)→②扫参设置(固定其他→变化目标→观测指标)→③结果描述('由图X可见，当参数取Y时性能最优')→④trade-off讨论(增大好处vs代价)→⑤最优值结论(明确推荐值)→⑥验证/讨论(可选)"
why_good: "把'调参叙述'结构化为六步，避免 AI 常犯的只描述趋势不给推荐值；trade-off 步是区分人写/AI 的关键——AI 只说'越来越好'，人写必给拐点和权衡"
fewshot_target: "S033'段落衔接改写'——参数优化段六步法骨架（含 trade-off 与最优值结论）"
```

```yaml
id: C-504
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/writing-patterns-sentence.md:13"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "公式引入基线句式：'经过[前置处理]之后的[物理量]（[限定条件]）可以表示为：[公式]' —— '可以表示为'语气中性，前面常带限定括注说明忽略了哪些因素"
why_good: "公式引入不直接甩公式，先用'经过…之后…可以表示为'交代前置处理和限定条件，让读者知道公式的适用边界"
fewshot_target: "S033'句式规范化'——公式引入句式骨架（前置处理+限定+可以表示为）"
```

```yaml
id: C-505
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/writing-patterns-sentence.md:273"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "数值嵌入对比句式：'在[条件]时，[方法A]和[方法B]在[门限]条件下的[指标]分别为X和Y' / '与传统[方法]相比，所提算法在[场景A]下[指标]提升了X%，在[场景B]下提升了Y%'"
why_good: "结果段数据嵌入有固定句式：先绝对值并列再差值，或多场景百分比压缩，避免 AI 的'取得了显著提升'空洞表述"
fewshot_target: "S033'去 AI 高频词'——结果段数值嵌入句式（分别为/提升了/降低了），替代'显著提升'"
```

```yaml
id: C-506
source_ref: "/mnt/d/code/study/research-protocol/毕设/写作材料/archive/writing-patterns-ch2ch3.md:17"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "方法论可继承-技术作废"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "范文质量排名方法论（5维度25分制）：推导深度+公式密度+段落组织+段间衔接+图表配合，对 7 篇参考论文打分排序后定向提取（如张思齐 Ch2 #1 提'分步推导模式'，董凡 Ch3 #1 提'算法设计递进+定量对比表'）"
why_good: "范文不是整篇仿写，而是先 5 维度打分定位每篇最强项，再按'最强项→提取内容'定向取材，避免无差别模仿"
fewshot_target: "S033'范文取材方法论'——5 维度打分 + 定向提取最强项（方法论可继承，ch2ch3 正文已被重写故技术作废）"
```

```yaml
id: C-507
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S004-template-extracted-xiazhaoyu.md:37"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "句间逻辑链标注体系（v3）：P1(背景)=行业现状→[然而]→现有不足→[同时]→衍生挑战→[为应对]→新方向→[这种]→核心特征；挑战段=具体现象→[导致]→直接后果→[传统方法]→局限→[DL方法]→优势→[然而]→不足→[因此]→空白"
why_good: "把段落级衔接从'感觉'变成可标注的逻辑链：每句话跟前句必须有明确逻辑关系（转折/递进/因果/回指/定义），去掉衔接词句子断了=逻辑链断了"
fewshot_target: "S033'段落衔接改写'——句间逻辑链 DEF/CLAIM/EVAL/TRANS 标注法，按逻辑序列填句"
```

```yaml
id: C-508
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S004-template-extracted-xiazhaoyu.md:96"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "现有信道估计方法…LS估计器…MMSE估计器…数据驱动方法…（逐篇平铺，无分类框架）"
rewritten_text: "P3[归纳句先行] 现有信道估计方法按是否依赖信道统计先验可分为两类：基于统计模型的方法和基于数据驱动的方法。前者以LS、MMSE和Kalman滤波为代表，后者以神经网络为主。"
good_example: "P3 分类是灵魂：没有分类就是'清单体'。综述段必须先用归纳句给分类框架（按是否依赖…可分为两类），再 P4/P5 分述每类优缺点"
why_good: "归纳句先行把散乱文献装进分类框架，是'综述'与'清单'的根本区别；P7 只展开最相关 2-3 篇，其余在综述表中概括"
fewshot_target: "S033'去清单体'——综述段 P3 归纳句先行 + 分类框架 + P7 只展开 2-3 篇"
```

```yaml
id: C-509
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S004-template-extracted-xiazhaoyu.md:103"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "某论文没做XX；某论文也没考虑YY（逐篇挑错，停留在单篇层面）"
rewritten_text: "P8[从方法论层面] 尽管DL方法在特定场景下展示了优势，现有研究存在两个根本性不足。P9 第一，…未考虑…时变特性。第二，…融合不足…导致泛化性差。"
good_example: "缺陷分析必须上升到方法论层面（'两个根本性不足'），不能只说'某论文没做XX'；用'第一/第二'编号 + 每条一句话定性 + 展开"
why_good: "单篇挑错是 AI 综述的通病；上升到方法论层面才证明作者有整体判断力，也才是真正的研究空白论证"
fewshot_target: "S033'综述缺陷段改写'——从单篇挑错上升到方法论层面的'根本性不足'"
```

```yaml
id: C-510
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S001-annex-paragraph-template.md:24"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "1.1 研究背景段落功能模式：P1宏观背景(代际演进→为什么需要这个领域)→P2本文主题定位+整体挑战概述→P3-P5三个挑战(每个:传统局限→DL不足→'亟需研究')→P6过渡句'为解决上述问题…'→P7-9三项工作(每项:'针对[问题]，设计[方法]，实现[目标]')"
why_good: "把绪论 1.1 拆成 9 段固定功能位，P3-P5 三挑战与 P7-9 三工作一一对应，P6 过渡句回指三挑战——结构对称且每段功能唯一"
fewshot_target: "S033'章节命名规范化'/'段落衔接改写'——绪论 1.1 九段功能位模板（挑战与工作一一对应）"
```

```yaml
id: C-511
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S001-annex-paragraph-template.md:107"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "核心技术章统一模式：X.1引言(P1本章任务重要性→P2当前挑战'然而…面临…双重挑战…缺乏可解释性'→P3本文方法概述'为此，针对…提出…'+框架图) / X.2理论基础(X.2.1基础架构→X.2.2适配性与局限性分析，一张适配性表+一张不适配性表) / X.3-X.4核心方法 / X.5实验方案 / X.6实验结果(主实验+消融)"
why_good: "每章一个独立技术贡献的标准结构，X.2.2 用'适配性表+不适配性表'双表论证方法选择合理性，而非直接套用"
fewshot_target: "S033'章节命名规范化'——核心技术章 X.1-X.6 统一段落功能模式（含双表论证方法选择）"
```

```yaml
id: C-512
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-fso-sentence-examples.md:14"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "T1 漏斗收束式开篇：代际规律(1G-5G)→[然而]当前瓶颈(5G不足)→[同时]需求驱动(IoT/AI)→[为应对]引出方向(6G研究)。衔接词链：[然而]→[同时]→[为应对这些挑战]"
why_good: "开篇用'过去规律→然而转折→同时递进→为应对引出'四步漏斗，每步有固定衔接词，逻辑链完整可逐句仿写"
fewshot_target: "S033'段落衔接改写'——漏斗收束式开篇四步法（规律→然而→同时→为应对）"
```

```yaml
id: C-513
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-fso-sentence-examples.md:45"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "T2 让步转折论证（论证空白黄金模式）：先肯定(理论最优性)→[然而]转折(依赖先验+计算复杂)→再给替代方案(基于特征)→[但]再转折(性能上限受限)。两层让步转折嵌套，每类方法都给'优点+局限'完整论证"
why_good: "先扬后抑是论证研究空白的黄金模式，两层嵌套（A 优→然而→B 替代→但→B 也局限）比单层转折更有说服力"
fewshot_target: "S033'去清单体'——文献综述让步转折两层嵌套（先扬后抑论证空白）"
```

```yaml
id: C-514
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-fso-sentence-examples.md:233"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "衔接词速查表（从范文提取）：然而=让步转折(段内中后部)/同时=并列递进/因此=因果收束(段末)/此外=补充递进/为此=目的因果(段首章首)/这导致=因果展开/这种=回指衔接/一方面…另一方面=对比展开/不仅…也是=递进并列/从而=手段目的/进而=因果递进"
why_good: "把衔接词按功能+典型位置分类，写作时按段内位置查表选词，避免 AI 的'然而/此外/因此'三件套堆砌"
fewshot_target: "S033'去翻译腔/段落衔接'——衔接词功能速查表（按位置选词，降三件套密度）"
```

```yaml
id: C-515
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-section-content-cards.md:83"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "1.4 创新点卡片 7 维信息模板：功能(明确列出创新点2-3条)/核心论点(每条:做什么+给什么)/支撑文献/可用数据(具体公式或实验值)/衔接上/衔接下/约束(措辞策略:场景创新型用'首次系统研究''场景迁移''解析推导'，避免'提出新方法')"
why_good: "每节用 7 维卡片（功能/论点/文献/数据/衔接/约束/篇幅）把'写什么'显性化，约束维内置措辞策略，防创新点过度声称"
fewshot_target: "S033'章节命名规范化'——逐节 7 维内容卡片模板（功能+论点+文献+数据+衔接+约束+篇幅）"
```

```yaml
id: C-516
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-section-content-cards.md:355"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "3.4.2/3.4.3 卡片叙事关键约束：不是'预补偿不好'，是'预补偿在真实估计噪声下不可行'——用'同一h_est，两个下游模块命运完全不同'(同步鲁棒 vs 预补偿脆弱)论证 Ch4 接收端载波同步的必要性"
why_good: "内容卡片的'约束'维不只列禁忌，还给出叙事关键句（正反对比 + 必要性论证），把实验结论转化为论证主线"
fewshot_target: "S033'论证主线改写'——内容卡片约束维的叙事关键句（正反对比论证必要性）"
```

```yaml
id: C-517
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/material-section-content-cards.md:13"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "卡片'衔接上/衔接下'双字段设计：每节显式标注承接哪节(如 1.1 衔接下='为1.2提供问题框架:三大损伤')、为哪节铺垫(如 1.2.3 衔接下='直接引出1.3研究内容和1.4创新点')，形成全文章节衔接网"
why_good: "把跨节衔接从隐性'感觉'变成显式双字段，写每节时强制回答'承接谁/铺垫谁'，防段间断裂"
fewshot_target: "S033'段落衔接改写'——内容卡片衔接上/衔接下双字段（全文章节衔接网）"
```

```yaml
id: C-518
source_ref: "/mnt/d/code/study/research-protocol/毕设/symbol-conventions.md:239"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "h 既表示归一化辐照度，又表示蝶形抽头系数，还表示海拔高度（三义冲突）"
rewritten_text: "蝶形抽头始终写 h_xx 带下标；海拔高度改用 z（普朗克常数改用 h_P）；正文 h 统一为归一化辐照度 E[h]=1"
good_example: "符号消歧策略：α,β(GG参数/DPLL系数/大气衰减)→DPLL加下标α_DPLL,β_DPLL，大气衰减改σ_a,σ_s；h(辐照度/海拔/普朗克)→海拔改z，普朗克改h_P；L(传播距离/OFDM符号数)→距离改d_link；R(响应度/相关)→响应度改花体𝓡"
why_good: "符号首次定义段改写有系统策略（加下标/换字母/换花体），15 条消歧覆盖全文冲突点，C 高价值因符号冲突是 AI 写作高频 bug"
fewshot_target: "S033'符号一致性改写'——符号消歧策略库（加下标/换字母/换花体 15 条）"
```

```yaml
id: C-519
source_ref: "/mnt/d/code/study/research-protocol/毕设/symbol-conventions.md:261"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "符号写作 5 建议：①每章首段列'本章符号'小表(3-5个最常用)避免翻找 ②首次出现给完整定义(含单位)后续直接用 ③跨章符号首次使用注明'(定义见第X章)' ④歧义符号严格按消歧表执行不混用 ⑤全文完成后整理为附录A'符号表'"
why_good: "把符号管理做成 5 条可执行规则（每章小表+首次定义+跨章注明+消歧+附录），配合 §13 消歧表形成符号一致性闭环"
fewshot_target: "S033'符号一致性改写'——符号写作 5 建议（每章小表+首次定义+附录符号表闭环）"
```

```yaml
id: C-520
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:11"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "方法论可继承-技术作废"
direction: "当前(FSO)"
original_text: "（模板测试稿 P1）随着全球信息化进程加速，卫星通信成为弥补地面网络覆盖不足的关键手段…激光通信…被视为下一代星地链路的核心技术[Kaushal,2016]"
rewritten_text: "（自评:每段标 P# 功能标签对照模板；P1 宏观背景→卫星→激光，P2 主题+挑战，P3-P5 三挑战，P6 过渡，P7-9 三工作——结构对齐 S004 模板）"
good_example: "模板测试稿方法论：每段标注【P#:功能】标签对照模板功能位，写完逐段自评是否对齐（如 P3=挑战1→P7=工作1 一一对应）；引用用 [Author,Year] 占位待转 GB7714"
why_good: "P# 功能标签 + 逐段自评是把模板从'参考'变成'约束'的方法论，可复用（信道均衡框架虽作废，标签自评法可继承）"
fewshot_target: "S033'模板对齐改写'——P# 功能标签逐段自评法（方法论可继承，信道均衡技术作废）"
```

```yaml
id: C-521
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:91"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "方法论可继承-技术作废"
direction: "当前(FSO)"
original_text: "（P7 文献例举）这些工作均采用神经网络架构…Rustum等[2026]…Mohammed等[2026]…Zhou等[2024]…（逐篇展开）"
rewritten_text: "（P7 先归纳后展开）这些工作均采用神经网络架构，在GG湍流信道下取得了优于传统方法的估计精度。其中，Rustum等[2026]…Mohammed等[2026]…Zhou等[2024]…（归纳句先行→只展开最相关3篇→每篇带量化）"
good_example: "文献例举段模式：开头归纳句说共同点（'均采用神经网络架构，取得了优于传统方法'）→'其中'展开最相关 2-3 篇→每篇 1 句含方法+场景+量化结果（NMSE≈10⁻³/MSE降低35%）"
why_good: "归纳句先行 + 只展开 3 篇 + 每篇量化，是 S004 模板 P7 的实操落地，避免逐篇平铺清单体"
fewshot_target: "S033'去清单体'——文献例举段归纳先行 + 量化展开（方法论可继承）"
```

```yaml
id: C-522
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:119"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "PPT 综述支撑页模板（H7/H8）：一页一主张 + 逐条溯源（• 作者 年份: 贡献一句话 (期刊)）+ 空白箭头收束（⇒ 但[精细场景]完全空白/仍有待展开 ✈）。例 H7:'编码辅助载波恢复已有坚实基础(RF+光纤): • Oh 2001… • Lottici 2004… • Castrillon 2015… ⇒ 但FSO湍流场景完全空白 ✈'"
why_good: "支撑页结构化：主张→3 条溯源（作者+年份+贡献+期刊）→空白箭头收束，一页完成'领域有基础+本文填空白'论证，每条可溯源验证"
fewshot_target: "S033'综述支撑页改写'——PPT/报告一页一主张+逐条溯源+空白箭头收束模板"
```

```yaml
id: C-523
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:54"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "创新点 IP1(Ch3) 表述范例：'拟建立…影响分析框架，推导…传播边界，分析…影响，给出…设计准则' + 6 维配套(文献对标 Han2022/Petkovic2023 / 退路:准则可宽可窄 / 递进:Ch3→Ch4 / 已有支撑:C3-01~05 / 风险:低-数学事实 / 措辞:对标 analytical framework→design criterion，不声称新算法)"
why_good: "创新点不只写一句话，而是 6 维配套（对标/退路/递进/支撑/风险/措辞），'拟建立…框架…准则'用分析类动词谱系，避免'方法'歧义"
fewshot_target: "S033'创新点措辞改写'——分析类创新点 6 维配套表述（框架+准则，去'方法'化）"
```

```yaml
id: C-524
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:66"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "创新点 IP2(Ch4) 宽壳策略：标题写宽('信号处理方法研究')，内容先塞载波同步分析，'包括但不限于'不锁定方向；三级退路(闭合解析公式→半解析+仿真查表→经验设计准则)；'联合处理方法探索'用'拟'字保护不绑定具体方向"
why_good: "宽壳策略是创新点防挖坑核心：标题宽到能降级，内容窄到可交付，'拟'字+'包括但不限于'留退路，与 D-102 退路宽度自检呼应"
fewshot_target: "S033'创新点措辞改写'——宽壳策略（标题宽+内容窄+'拟'字保护+三级退路）"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举：命名方法论 18 条（C-501~511/512~517/522~524）、规则清单 2 条（C-518/519）、diff对比 4 条（C-508/509/520/521——注：C-508/509 同时填了 original/rewritten 和 good_example，属混合形态，落盘时 material_form 统一为"命名方法论"因主映射是命名方法论范式）
- [x] 所有 source_ref 含行号（24/24 条均带 :line）
- [x] 所有 date_validity/direction 已标注：C-506（ch2ch3）+ C-520/521（draft-ch1）标"方法论可继承-技术作废"；余"有效"+"当前(FSO)"
- [x] id 前缀均为 C-5xx（C-501~C-524）
- [x] diff 形态（C-520/521）填 original_text + rewritten_text；纯范例形态填 good_example
- [x] fewshot_target 24 条全部填写
