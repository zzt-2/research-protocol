# 对话C agent-C1 产出（C 维前半 8 源：Ch2范式/写作向导/贡献降级/新旧方向绪论/综述笔记/§1.3范文/开题第三章）

> 2026-06-15 | C 维（写作范例 few-shot）前半 8 源全量提取 | agent-C1 区 id 前缀 C-4xx
> 上游：R002 C3/C4/C7/C8/C9/C11/C12/C13
> 下游契约：D002 C-rewrite-fewshot 字段
> 不变量：① 只读不改原文 ② 全量实读 ③ 每条带 file:line 回溯 ④ 跨 agent 可合并

## 提取统计
- 处理文件：8
- 产出条目：C=21（C-401~C-421）
- 行号校准：C12 R002标"待补"→补齐（总起句L168-171/递进衔接L196-203/细节对比L239-248/推荐结构L115-141）；C13 C/D价值段定位（叙事策略L335-405/每节角色L449-472/措辞禁忌L480-498/防御性L522-528）

## C 维度

```yaml
id: C-401
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-星地激光通信系统与信道模型.md:23"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "相干检测的核心在于信号光与本振光的混频过程。接收信号光场可表示为：$$E_s(t)=A_s\\exp[-j(\\omega_s t+\\varphi_s)]$$"
why_good: "公式引入用'可表示为：'过渡，前一句点明物理含义（混频过程），公式紧随其后，符合范文铁律（pilot C-204 验证：去'写作'改'可表示为'）"
fewshot_target: "S033'公式引入句式规范化'——pivot 后唯一完成章节的'物理含义句+可表示为+公式'三段范式"
```

```yaml
id: C-402
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-星地激光通信系统与信道模型.md:31"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "式中，$A_s$和$A_{LO}$分别为信号光和本振光的振幅，$\\omega_s$和$\\omega_{LO}$分别为信号光和本振光的角频率（单位rad/s），$\\varphi_s$和$\\varphi_{LO}$为初始相位。"
why_good: "参数解释统一'式中，A为...，B为...'格式，一个'式中'统领全部符号，成对符号用'分别为'并联，单位括注紧跟——pilot B-205 铁律3 的实战范本"
fewshot_target: "S033'参数解释格式铁律'——多符号公式的'式中+分别为+单位括注'标准写法"
```

```yaml
id: C-403
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-星地激光通信系统与信道模型.md:53"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "其中，$s[k]$为第$k$个发射符号；$h$为归一化辐照度，表示大气湍流引起的光强起伏，满足$h\\geq 0$且$E[h]=1$，为实值标量而非复信道系数，其统计特性服从Gamma-Gamma分布，详见§2.3；$\\varphi[k]$为联合载波相位误差..."
why_good: "噪声/随机变量建模段：每个符号不只给定义，还附物理含义+约束+澄清易误解点，层层加限定防误读"
fewshot_target: "S033'信号模型建立段改写'——随机变量定义的'符号+物理含义+约束+澄清'四件套"
```

```yaml
id: C-404
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-guides.md:65"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "公式引入句式库：'...可以表示为：' / '对于QPSK信号而言，其...为：'；参数解释：'式中，A为...，B为...'；假设引入：'可以近似认为相邻符号之间...不变'；噪声建模：'可以建模为[概率模型]'"
why_good: "Ch2 写作向导把公式引入/参数解释/假设引入/噪声建模四类高频句式集中列为可复用模板"
fewshot_target: "S033'公式引入句式规范化'——四类数学表达句式的标准模板集"
```

```yaml
id: C-405
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-guides.md:69"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "系统描述句式：'[系统名]框图如图X所示，其中A主要由B组成'；节首铺垫禁回指，三个子节句式不雷同（§2.2.1描述性 / §2.2.2定义性 / §2.2.3分析性）"
why_good: "框图段链式结构；三子节强制句式分化避免机械重复——pilot B-204 铁律1 的预防性规则"
fewshot_target: "S033'段落衔接改写'——节首铺垫句式+三子节句式分化防雷同"
```

```yaml
id: C-406
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-guides.md:72"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "术语规范：'载波频偏估计（FOE）'非'频偏估计'；'载波相位恢复（CPR）'非'相位恢复'；'内差（Intradyne）检测'首次出现注明；不用'我们'用'设...''可以认为...'；不用'所以'用'因此''从而'"
why_good: "术语首次出现给全称+缩写括注；自称用'设/可以认为'中文学术被动式替代'我们'；连接词用'因此/从而'替代口语'所以'——三条去 AI 味规则"
fewshot_target: "S033'去翻译腔'——术语全称括注+去'我们'+去'所以'的术语与连接词规范"
```

```yaml
id: C-407
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:184"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: "提出了一种新的 / 首次发现 / 创新性地 / 核心创新 / 首次组合"
rewritten_text: "验证并量化了 / 系统评估了 / 针对 XX 场景适配了 / 核心贡献 / 系统性组合迁移"
good_example: "贡献声称降级 5 条映射：'提出了一种新的'→'验证并量化了'；'首次发现'→'系统评估了'；'创新性地'→'针对 XX 场景适配了'；'核心创新'→'核心贡献'；'首次组合'→'系统性组合迁移'"
why_good: "5 条过度声称→诚实定位的系统性降级映射，覆盖'新颖性声称/发现声称/创新副词/定位词/组合声称'五类，方法论可继承到任何方向"
fewshot_target: "S033'贡献声称降级'——5 类过度声称的统一降级映射表"
```

```yaml
id: C-408
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:178"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: ""
rewritten_text: ""
good_example: "Size generalization 角色降级：从每章核心贡献 → 跨章共享优势（在论文总论/结论章统一讨论，不每章重复声称）"
why_good: "当某能力非单章独有，应从'每章核心贡献'降为'跨章共享优势'统一讨论，避免每章重复声称同一贡献——贡献去重的结构级策略"
fewshot_target: "S033'贡献声称降级'——跨章共享能力的去重定位"
```

```yaml
id: C-409
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:172"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: ""
rewritten_text: ""
good_example: "三章差异化定位表：每章列[旧定位→新定位/学习范式/规模迁移维度]四列，如 Ch1 监督学习路由（星座节点数66→720）/ Ch2 DRL切换（UE数20→100）/ Ch3 故障弹性路由（故障模式+节点数）"
why_good: "多章论文用表格显式区分各章的[学习范式+规模维度]，避免章间定位模糊重叠"
fewshot_target: "S033'章节定位精确化'——多章论文的差异化定位表模板"
```

```yaml
id: C-410
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-figures/开题报告.md:41"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: ""
rewritten_text: ""
good_example: "综述收口句式（先扬后抑）：'上述方法虽然在各自规模上取得了改进，但无一将训练与测试解耦到不同规模的星座。星座的渐进式部署要求路由策略在不重新训练的情况下适配新拓扑，这一需求在现有工作中尚未被回应，近期的综述也确认了这一判断'"
why_good: "综述段收口用'虽然...但...'先扬后抑 + '无一...'绝对化空白 + '这一需求...尚未被回应'收束到研究需求 + '综述也确认'背书——pilot C-102 先扬后抑模式的完整范文实例（导师通过版）"
fewshot_target: "S033'去清单体'——综述段先扬后抑+空白收口的完整范文段"
```

```yaml
id: C-411
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-figures/开题报告.md:79"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: ""
rewritten_text: ""
good_example: "三空白分层结构：'综合以上分析，LEO卫星网络中GNN的应用面临三个层面的研究空白。路由层面：...但跨规模零样本泛化能力完全未被探索。切换层面：...用户规模泛化在LEO切换领域完全空白。故障层面：...无同时验证的先例。三个空白指向同一个核心问题：GNN的有效性取决于什么条件？'"
why_good: "研究空白分三层逐层陈述，每层'层面名+已有工作+but+空白'，最后三空白收敛到一个核心问题——漏斗结构"
fewshot_target: "S033'研究空白陈述'——三层空白分层+收敛到核心问题的漏斗式写法"
```

```yaml
id: C-412
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-figures/开题报告.md:256"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: ""
rewritten_text: ""
good_example: "可行性分析四段式：理论可行性（Graphon理论基础+文献验证）/ 方法与数据可行性（仿真常规方法+软件硬件+训练范式先例）/ 已验证的初步结果（指向第七节）/ 风险分析与应对（主要风险+退路+统计严谨性）"
why_good: "可行性分析按'理论/方法数据/初步验证/风险应对'四段展开，风险段给出退路——四段式可行性模板"
fewshot_target: "S033'可行性分析写法'——四段式（理论/方法数据/初步验证/风险应对）可行性模板"
```

```yaml
id: C-413
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/thesis-framework.md:29"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "综述收口到空白：'总体而言，现有信道估计研究关注估计器本身的NMSE指标，但NMSE与载波同步等下游模块性能之间的定量级联关系尚未被建立。信道估计器的输出并非最终目标，其精度需满足后续载波同步的工作要求。估计器设计缺乏面向系统级性能的指导准则，这是当前研究的核心空白之一。'"
why_good: "FSO 当前方向的综述收口：'总体而言...但...尚未被建立'先扬后抑 + '输出并非最终目标'点明级联盲区 + '缺乏...指导准则，这是核心空白之一'收束——与 C8 C-410 新旧对照"
fewshot_target: "S033'去清单体'——FSO 方向综述收口（与 C8 旧方向 C-410 对照验证句式普适性）"
```

```yaml
id: C-414
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/thesis-framework.md:41"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "三不足分层：'综合以上分析，当前星地激光通信信号处理研究存在三方面不足。其一，湍流信道下的链路性能分析不够完善...其二，载波同步缺乏湍流场景下的系统性参数优化...其三，从信道建模分析到载波同步算法的设计指导缺失。'"
why_good: "用'其一/其二/其三'显式分层陈述三不足，每条'主题+现有假设+but+缺失'，与 C8 C-411 新旧对照——三不足分层结构跨方向稳定"
fewshot_target: "S033'研究空白陈述'——FSO 方向三不足'其一/其二/其三'分层（与 C8 对照）"
```

```yaml
id: C-415
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/thesis-framework.md:67"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "创新点三条（分析类措辞）：'(1)系统分析了...链路性能与信号处理基础问题...为后续...提供了精度需求和性能基线。(2)系统分析了...载波同步性能...给出了分湍流强度的参数配置建议和性能对比。(3)完成了关键载波同步算法的FPGA设计与实现验证...'"
why_good: "三条创新点用'系统分析了/给出了/完成了'动词，分析类贡献用'系统分析'非'提出'，交付物明确（基线/参数建议/验证），与 pilot D-104 专硕标准一致——FSO 当前方向创新点措辞范本"
fewshot_target: "S033'创新点措辞改写'——分析类贡献的'系统分析+交付物'措辞（与 pilot C-205 应用型对照）"
```

```yaml
id: C-416
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:202"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "参数溯源表四类分表+来源类型标注：GG湍流参数(α,β/Cn²)/链路参数(距离/波长/符号速率)/均衡器参数(抽头数/步长)/载波同步参数(窗口/线宽/多普勒)；每条参数列[参数|值|来源论文|来源类型]，来源类型枚举[实证/理论/实测/建模/标准/实验/工程/理论+实证]"
why_good: "把全文用到的参数按技术领域分四表，每参数溯源到具体论文+标注来源类型，下游写作时每个数字可回溯"
fewshot_target: "S033'论断依据补强'——参数溯源表模板（每数字带来源论文+来源类型）"
```

```yaml
id: C-417
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:242"
source_agent: "细扫C"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "综合分析三层结构：领域概况（两条技术路线IM/DD vs 相干）/ 核心挑战（体制错位/场景缺失/参数获取）/ 研究定位（每章填补什么空白+经多少条结果验证确认）"
why_good: "综述笔记的综合分析按'概况→挑战→定位'三层递进，定位层每章明确'填补XX空白'+'经N条结果验证确认'，空白声称带验证证据"
fewshot_target: "S033'研究空白陈述'——综合分析三层结构+空白声称带验证条数"
```

```yaml
id: C-418
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R002-section-1-3-reference-analysis.md:168"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "§1.3 总起句三模板：研究定位型'本文以[核心技术领域]为研究对象，主要研究内容包括：[技术1]、[技术2]、[技术3]。'/ 问题导向型'本论文面向[趋势]，针对[核心问题]，结合[研究现状]，对[研究对象]进行了深入探讨...'/ 研究定位+指标型'本研究以[出发点]为出发点，探索一种应用于[场景]的[方案]，拟定系统指标如表X所示。'"
why_good: "从 4 篇有效学位论文归纳的 §1.3 总起句三模板，按'研究定位/问题导向/指标型'分流——经范文交叉验证的章节安排句式库"
fewshot_target: "S033'章节安排写法'——§1.3 总起句三模板选择"
```

```yaml
id: C-419
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R002-section-1-3-reference-analysis.md:196"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "章间递进衔接句式库（全部实例）：'为后续XX环节提供有效的先验信息'（夏兆宇）/ '在XX提供的XX基础上'（夏兆宇）/ '为理解后续章节铺垫基础'（董凡）/ '结合第二章的研究结论'（吴志航）/ '本章将第四章提出的算法框架扩展到XX场景'（张思齐）"
why_good: "从 4 篇范文提取的章间递进衔接句全部实例，按'前章→后章输入/基础/铺垫/扩展/依赖'五种关系分流——经范文验证"
fewshot_target: "S033'段落衔接改写'——章间递进衔接句五模板"
```

```yaml
id: C-420
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:374"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "§3.3.1 开头：'拟采用导频辅助方案，对比研究以下四类估计方法：LS……MMSE……KF……DL……'（方法罗列式）"
rewritten_text: "§3.3.1 开头：'湍流信道估计的精度直接影响下游载波同步性能。本节首先分析估计误差如何通过级联结构传播到BER，然后确定"精度需要做到多少"，最后分析"哪些估计方法在什么条件下可用"。'（问题驱动式）"
good_example: ""
why_good: "方法罗列（逐个介绍LS/MMSE是什么）→ 问题驱动（先说回答什么问题，再说需要什么方法）——开题第三章核心叙事策略 diff"
fewshot_target: "S033'去清单体'——开题第三章方法罗列→问题驱动改写"
```

```yaml
id: C-421
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:383"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "初步验证表明QPSK系统下载波同步对估计误差高度鲁棒 / DPLL在强湍流下显著优于前馈方法（暴露具体结论）"
rewritten_text: "课题组已完成初步验证，为核心研究结论提供了初步支撑 / 初步验证表明，不同方法在不同湍流条件下呈现差异性表现，具体结论将在论文中展开（只说有支撑/有差异，不说结论）"
good_example: ""
why_good: "开题阶段防御性写作：已有支撑段只说'有支撑'不说'结论是什么'，避免在开题暴露底牌——方法论可继承到任何开题写作"
fewshot_target: "S033'避免绝对化'——开题已有支撑段防御性写法（说方向不说结论）"
```

## 可合并性自检
- [x] 所有 material_form 匹配 7 形态枚举（规则清单×16 / 命名方法论×2 / diff对比×2）
- [x] 所有 source_ref 含行号（21 条全部带 :Lxx）
- [x] 所有 date_validity/direction 已标注（C-407~412 旧方向标"方法论可继承-技术作废"+"旧(GNN/路由)"；其余"有效"+"当前(FSO)"）
- [x] id 前缀均为 C-4xx（C-401~421）
- [x] C 维 schema 11 字段齐全（diff 形态填 original/rewritten；纯范例填 good_example）
- [x] fewshot_target 全部填 S033 改写目标
- [x] 与 pilot 无重复（C8/C9 绪论范文与 pilot C-101~104 R011句式不重叠；C7 降级清单与 pilot C-205~207 单条 diff 互补）
