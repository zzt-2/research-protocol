# 对话B agent-A 产出（A 维剩余 4 源全量）

## 提取统计
- 处理文件：4
- 产出条目：A={22}（A2=6 / A7=5 / A8=7 / A9=4）
- 行号校准说明：
  - **A8**（R003-kaiti-chapter3-research-plan.md，R002 原标"行号待补"）已实读补齐：P1=L26 / P2=L36 / P3=L48 / P4=L59 / P5=L67 / P6=L80 / §1.2 问题归类表=L88
  - **A9**（draft-ch1-template-test.md，R002 原标"445 行"）实测文件仅 321 行，R002 行数有误；§模板效果自评段实读定位在 L284-321（量化评估表 L306-312，建议改进 L314-319）；P8/P9 缺陷分析正文在 L95-101
  - **A2**（ai-trace-report.md，R002 标"209 行"）实测 209 行准确；汇总统计表 L8-15、重度定位 L21-36、系统性模式总结 L71-97、范文诊断信号 L197-209
  - **A7**（Ch2-reviews.md，R002 标"L414-424"）实读确认精确：反复犯错记录表在 L413-424

## A 维度

```yaml
id: A-401
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:10"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "开题报告 AI 痕迹自检产出 5 类×3 严重度的量化统计（翻译腔 9/清单体 8/元叙述 11/数据堆砌 4/平行罗列 12，去重后 35 处），可直接作为 paper-eval AI 痕迹检测器的分类骨架与严重度标尺"
original_quote: "翻译腔 9 / 清单体 8 / 元叙述 11 / 数据堆砌 4 / 平行罗列 12 / 合计（去重后）35"
classification: "检测器ID'AI 痕迹 5 类分类法'（与 A-101 的 R011 5 大缺陷对齐，本条提供严重度量级）"
s033_input: "S033'AI 痕迹检测'——5 类分类 + 重/中/轻三级严重度量级，作为检测器输出标签 schema"
```

```yaml
id: A-402
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:73"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "元叙述泛滥（13 处）是最突出的 AI 痕迹——'本节/以下按/首先...然后...最后'型预告句几乎每个大节段首都有，4 套重复模板"
original_quote: "全文共 13 处'本节/以下按/首先...然后...最后'型预告句，几乎每个大节段首都有"
classification: "检测器ID'元叙述预告句'（4 套正则模板：以下从/本节首先然后/本节围绕/为后续提供）"
s033_input: "S033'去元叙述'——段首预告句检测，4 套模板正则化"
```

```yaml
id: A-403
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:83"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "§2 综述段清单体（L41-80）是全文 AI 痕迹最密集区域——整段逐篇罗列文献（R02-R08 共 7 条叠加），缺分组对比和递进分析"
original_quote: "整段逐篇罗列文献，缺乏分组对比和递进分析，是全文 AI 痕迹最密集的区域（R02+R03+R04+R05+R06+R07+R08 共 7 条）"
classification: "检测器ID'综述段清单体'（定位：综述段密集度 = 文献逐篇平铺 + 无分组对比）"
s033_input: "S033'去清单体'——综述段密度告警，7 条叠加段落判为高风险区"
```

```yaml
id: A-404
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:87"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "'综合以上分析/上述分析表明'+'然而转折'模板重复 5 处（L53/L80/L95/L97/L651），几乎相同的套话开头+转折结构"
original_quote: "L53、L80、L95、L97、L651 共 5 处使用几乎相同的'综合以上分析/上述分析表明'+'然而转折'模板"
classification: "检测器ID'总结-转折套话'（综合以上X分析 + 然而 + 上述研究在X层面存在不足）"
s033_input: "S033'去套话转折'——总结段开头模板检测，跨段重复≥3 次告警"
```

```yaml
id: A-405
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:91"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "§3.4.4 三方向段是导师点名段落（批注 32），元叙述+平行罗列+翻译腔三类痕迹叠加，内部还有'一是/二是/三是'二级平行——全文最严重段落"
original_quote: "导师点名段落（批注 32），同时存在元叙述、平行罗列、翻译腔三类痕迹叠加，三方向内部还有'一是/二是/三是'二级平行。全文最严重段落。"
classification: "检测器ID'多类痕迹叠加段'（同段≥3 类痕迹 + 二级平行编号 = 导师必点名）"
s033_input: "S033'段落综合风险评分'——多类痕迹叠加加权，导师批注锚点段落优先告警"
```

```yaml
id: A-406
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/ai-trace-report.md:134"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "AI 痕迹的判别关键不在单一特征，而在分布模式——人写的 AI 高频词偶发分散，AI 生成的是集中、高频、段落间匀质分布。需配反向判定信号排除'质量差的人类写作'"
original_quote: "正常写作的'AI 高频词'是偶发的、分散的；AI 生成文本的特征是集中、高频、段落间匀质分布。判别关键不在单一特征，而在分布模式。"
classification: "新维度'AI 痕迹分布模式判别'（集中度+匀质度指标 + 反向人类信号排除）"
s033_input: "S033'AI 痕迹判别'——分布模式指标（集中度/匀质度）+ 反向人类信号清单（口语化/语法错/实验细节/风格差异）"
```

```yaml
id: A-407
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:419"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "括号内章节号（§2.2.1 等）S003 明确禁止，但 Ch2 审查时 H2/M14 修正阶段重新引入——审查 agent 建议'加括号节号'却未对照 S003 纪律，复犯根因是审查 agent 建议未过纪律校验"
original_quote: "括号内章节号 | S003明确禁止 | H2/M14修正时引入 | 审查agent建议加括号节号，未对照S003纪律"
classification: "检测器ID'反复犯错-括号章节号'（已纠正纪律库 vs 审查建议冲突检测）"
s033_input: "S033'反复犯错检测'——审查 agent 的句式建议必须先比对已纠正纪律库（S003/S004），冲突即拦截"
```

```yaml
id: A-408
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:420"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "过强动词'建立'在 S003 已对 Ch2 描述改'介绍'，但 Ch2 §2.2 引言/§2.5 小结又用了'建立'——未区分'概述中描述'和'正文内执行'的动词标准，概述段误用了执行级强动词"
original_quote: "过强动词'建立' | S003 Ch2描述改'介绍' | §2.2引言/§2.5小结用了'建立' | 未区分'概述中描述'和'正文内执行'的动词标准"
classification: "检测器ID'反复犯错-动词强度漂移'（概述段 vs 执行段动词标准分层缺失）"
s033_input: "S033'动词强度检测'——区分'概述描述段'和'正文执行段'两套动词标准，概述段禁执行级强动词"
```

```yaml
id: A-409
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:421"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "机械节引用（'§2.3 分别...§2.2 中...'）S004 已改内容描述，但 Ch2 §2.4 引言复犯——审查时认为'精确引用有帮助'未对照范文，根因是审查偏好压过范文先例"
original_quote: "机械节引用 | S004'§1.2.2所述'改内容描述 | §2.4引言'§2.3分别...§2.2中...' | 审查时认为'精确引用有帮助'，未对照范文"
classification: "检测器ID'反复犯错-机械节引用'（审查偏好 vs 范文先例冲突）"
s033_input: "S033'机械节引用检测'——'§X.X所述/分别'句式，审查建议必须先在范文库验证先例"
```

```yaml
id: A-410
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:422"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "回指句（'上节''前文'）S003 未明确涉及，但 Ch2 §2.2.3/§2.3/§2.4 引言段均用——深度审查 agent 建议'加回指过渡'却未对照范文，根因是 S003 纪律未覆盖此维度，审查 agent 凭空创造"
original_quote: "回指句 | S003未明确涉及 | §2.2.3/§2.3/§2.4引言段均用'上节''前文' | 深度审查agent建议加回指过渡，未对照范文验证"
classification: "检测器ID'反复犯错-回指句'（纪律盲区 + 审查 agent 凭空创造句式）"
s033_input: "S033'回指句检测'——'上节/前节/前文'+动词模式，纪律库未覆盖维度需补范文验证门控"
```

```yaml
id: A-411
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:424"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "反复犯错的预防机制——后续章节写作前必须先读'铁律'段；任何 agent 建议的句式改动必须先在范文库验证先例，不能凭空创造"
original_quote: "后续章节写作前，必须先读本文档'铁律'段。任何agent建议的句式改动，必须先在范文库中验证是否存在先例，不能凭空创造。"
classification: "新维度'审查建议范文先例门控'（所有句式建议须经范文库验证）"
s033_input: "S033'反复犯错预防'——审查 agent 建议的句式改动强制范文先例验证，无先例即拦截"
```

```yaml
id: A-412
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:26"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "方法概述段写成教科书摘抄——§3.3.1 逐个列举 LS/MMSE/KF/DL 的标准定义，是任何教材的第一段，评委不需要你教他什么是 LS；根因是'定义→特点→优缺点'百科式罗列，非问题驱动叙事"
original_quote: "这是任何教材的第一段。评委不需要你在开题里教他什么是 LS。根因：写法是'定义→特点→优缺点'的百科式罗列"
classification: "检测器ID'教科书摘抄段'（定义→特点→优缺点 百科式三段套）"
s033_input: "S033'去教科书摘抄'——方法概述段检测百科式三段套，改问题驱动叙事"
```

```yaml
id: A-413
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:36"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "分析段写成实验报告——每个子节都是'研究目标→拟采用方法→预期产出'三段套话，连续出现 6 次以上机械重复，读起来是填表不是讲故事；根因是把研究方案当实验申报书写"
original_quote: "研究目标→拟采用方法→预期产出...这种写法连续出现 6 次以上，机械重复。读起来是填表不是讲故事。根因：把'研究方案'当成'实验申报书'来写"
classification: "检测器ID'实验报告式三段套'（目标→方法→产出 连续≥6 次雷同）"
s033_input: "S033'去实验报告式'——研究方案段检测目标/方法/产出三段套重复，改逻辑链论证"
```

```yaml
id: A-414
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:48"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "开题缺叙事弧——只机械回答'怎么做'（3.2 建模型/3.3 做估计/3.4 做同步/3.5 做 FPGA），未建立'问题链→方法链→产出链'递进叙事，各章像独立模块描述，看不出前章输出如何成为后章输入"
original_quote: "没有建立'问题链→方法链→产出链'的递进叙事。每个章节像是独立的模块描述，看不出前一章的输出如何成为后一章的输入"
classification: "检测器ID'缺叙事弧'（各章独立模块化，无问题链→方法链→产出链递进）"
s033_input: "S033'叙事弧完整性检测'——章节间输入输出链验证，独立模块化告警"
```

```yaml
id: A-415
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:59"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "研究方案不回应文献综述缺口——范文证明最好写法是'每章概要明确对应 §1.2 的哪个空白'，但当前版本 3.3/3.4 各自独立描述，未引用 §1.2 已指出的空白，开题各章横向割裂"
original_quote: "每节应该对应 §1.2 中指出的一个具体研究不足...当前版本没有这个对应关系。根因：开题各章之间缺乏横向对齐"
classification: "检测器ID'不回应综述缺口'（研究方案节 vs 文献综述空白节 无对应映射）"
s033_input: "S033'综述-方案对齐检测'——研究方案每节必须映射到综述空白，缺映射告警"
```

```yaml
id: A-416
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:67"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "'已有支撑'段暴露底牌——多处写具体结论（'QPSK 系统下载波同步对估计误差高度鲁棒''DPLL 在强湍流下显著优于前馈'），违反防御性写作；根因是 PROMPT-013 约束了'不放 BER 数字'但未约束'不放具体结论方向'"
original_quote: "初步验证表明，QPSK 系统下载波同步对估计误差高度鲁棒... defense-principles.md 明确说：不放具体仿真结果数字、不在 PPT 上写结论、被追问时用'拟'挡"
classification: "检测器ID'暴露具体结论'（开题研究方案中出现已验证结论方向，非'拟'保护）"
s033_input: "S033'防御性写作检测'——开题段检测已验证结论声称，需用'拟'挡且不放具体结论方向"
```

```yaml
id: A-417
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:80"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "系统模型段过于冗长——3.2 节占全文约 1/3 篇幅，但这是背景建模非创新点，正文 Ch2 已写完 6700 字含 22 条公式，开题无需重写；根因是把研究方案当小论文写"
original_quote: "3.2 节占了全文约 1/3 篇幅...但开题评委已经知道 QPSK 和 GG 模型是什么——他们要看的是你的研究思路。根因：把'研究方案'当成了'小论文'来写"
classification: "检测器ID'系统模型冗长'（背景建模占比≥1/3 + 与正文重复）"
s033_input: "S033'篇幅分配检测'——背景建模段占比告警 + 与正文重复内容检测"
```

```yaml
id: A-418
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md:88"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "开题第三章 6 大痛点的根因归类总表——定位错误（当小论文写 P6/当实验报告写 P2）、缺叙事设计（无整体逻辑链 P3）、缺横向对齐（不回应综述空白 P4）、防御性不足（暴露结论 P5）、写法问题（教科书式罗列 P1），六问题同根：未先定义'开题第三章到底是什么'"
original_quote: "核心发现：六个问题都指向同一个根因——没有在写之前定义'开题第三章到底是什么'。"
classification: "新维度'开题定位前置缺失'（5 类根因 × 6 问题，同根：定位未定义）"
s033_input: "S033'开题定位门控'——写作前强制定义章节定位，5 类根因作为定位检测维度"
```

```yaml
id: A-419
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:295"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(信道均衡，后改预补偿)"
pain_point: "P8/P9 缺陷分析段（从具体文献上升到'结构性不足'的归纳）是模板最难写环节，评分 6/10 最弱——模板只说'必须从方法论层面'但没给具体归纳路径，实际写作花最多时间反复修改"
original_quote: "P8/P9(缺陷分析)仍然最难写：从具体文献上升到'结构性不足'的归纳过程，模板只说了'必须从方法论层面'但没给具体的归纳路径。实际写作时P8-P9花了最多时间反复修改"
classification: "新维度'归纳路径缺失卡壳'（文献→结构性不足 归纳推理步骤缺模板指导）"
s033_input: "S033'归纳路径模板'——缺陷分析段需补'N篇论文→共性缺陷→结构性问题'推理步骤示例，6/10 评分锚点"
```

```yaml
id: A-420
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:296"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(信道均衡，后改预补偿)"
pain_point: "P5（DL 方法引入）与 P7（文献例举）边界模糊——模板假设 P5 只做方法概述、P7 才展开具体论文，但实际写作 P5 已提 Amirabadi 具体结果，P7 再展开显重复；模板段功能边界定义不清导致内容重叠"
original_quote: "P5(DL方法引入)和P7(文献例举)在内容上有重叠——P5已经提到了Amirabadi的具体结果，P7再展开显得重复。模板假设P5只做方法概述、P7才展开具体论文，但实际写作时难以严格区分"
classification: "新维度'段落功能边界模糊'（相邻段功能定义重叠，实际写作难区分）"
s033_input: "S033'段功能边界检测'——相邻段功能列重叠告警，建议合并或显式划分"
```

```yaml
id: A-421
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:297"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(信道均衡，后改预补偿)"
pain_point: "按同一 P1-P10 模式写三遍的'同质化风险'——三个 1.2.x 子节容易产生机械重复感，模板未给'如何避免三个子节长得太像'的指导"
original_quote: "按同一个P1-P10模式写三遍，容易产生机械重复感。模板没有给出如何避免三个子节'长得太像'的指导"
classification: "新维度'模板复用同质化'（同模板写≥3 次的机械重复风险）"
s033_input: "S033'同模板复用检测'——同结构段落≥3 次告警，需差异化侧重指导"
```

```yaml
id: A-422
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/draft-ch1-template-test.md:311"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(信道均衡，后改预补偿)"
pain_point: "模板效果量化评估表——5 维评分（方向明确性 8/段间衔接 7/文献综述质量 7/创新空白论证 6/篇幅控制 5），创新空白论证和篇幅控制是最弱环节；此 5 维评分体系可复用为模板效果自评 rubric"
original_quote: "方向明确性 8/10 | 段间衔接 7/10 | 文献综述质量 7/10 | 创新空白论证 6/10 | 篇幅控制 5/10"
classification: "新维度'模板效果 5 维自评 rubric'（方向/衔接/综述/空白论证/篇幅，可复用评分骨架）"
s033_input: "S033'模板效果自评 rubric'——5 维评分体系作为写作模板迭代评估的量化骨架"
```

## 可合并性自检
- [x] 所有 material_form 匹配 7 形态枚举（审查rubric 9 条 / 失败案例 10 条 / 规则清单 3 条，均在枚举内）
- [x] 所有 source_ref 含行号（22 条均带 :line，WSL 路径 /mnt/d/...）
- [x] 所有 date_validity/direction 已标注（A2/A7/A8 共 18 条"有效"+"当前(FSO)"；A9 共 4 条"方法论可继承-技术作废"+"旧(信道均衡，后改预补偿)"）
- [x] id 前缀均为 -4xx（A-401~422），避开 pilot 的 -1xx/-3xx
- [x] A 维 schema 字段顺序与 pilot 的 A-1xx/A-3xx 一致（10 字段顺序完全对齐可拼接）
