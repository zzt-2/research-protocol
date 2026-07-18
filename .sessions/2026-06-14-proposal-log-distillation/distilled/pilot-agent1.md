# pilot agent-1 产出（规则清单 + 批注原话）

## 提取统计
- 处理文件：4
- 产出条目：A={4} B={7} C={4} D={4}
- 行号校准说明：
  - R002 B1（开题批注）原标"行号待补"——已实读 `毕设/开题报告/开题报告v2-导师批注.md`，行号落在该批注汇总文件本身（20 批注按序 L10-215），非 kaiti-report.md 行号
  - R002 B3（S001 四底线）原无行号——已实读 `S001-advisor-meeting-and-direction-framework.md`，四底线在 L34-39，导师批评原文在 L15-22
  - R002 C1（R011）原标"全文"——已实读定位：5 大缺陷在 L290-331，句子功能标注体系在 L375-419
  - R002 D4（innovation-points R1-R7）原标 L11-46——已实读确认精确（R1=L11/R2=L17/R3=L21/R4=L25/R5=L32/R6=L39/R7=L46）

## A 维度

```yaml
id: A-101
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:290"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "AI 生成中文论文有 5 大系统性缺陷（翻译腔/清单体/段落衔接断裂/数据堆砌/元叙述），根因是自回归生成机制与中文表达习惯的结构性冲突"
original_quote: "AI最顽固的缺陷：翻译腔、清单体、段间断裂，根因是自回归生成机制与中文表达习惯的结构性冲突"
classification: "检测器ID'AI 5大缺陷'"
s033_input: "S033'翻译腔/清单体/段落衔接'检测器——5 类缺陷根因与修复方向"
```

```yaml
id: A-102
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:241"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "AI 高频使用模糊化/翻译腔用词（显著提升/具有重要意义/被视为/提供了…的能力/使…成为/一定程度上/填补了空白），无法验证且空洞"
original_quote: "显著提升→具体数字；具有重要意义→直接说意义；被视为→谁视为？；填补了空白→描述具体贡献"
classification: "检测器ID'AI 高频词黑名单'"
s033_input: "S033'去 AI 高频词'改写——7 词黑名单及替代"
```

```yaml
id: A-103
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:99"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "创新点措辞反复迭代 6 版（v1 查表选算法→v5 性能分析框架），根因是'方法'一词在中文学术语境被误解为算法，分析类贡献误用算法类动词"
original_quote: "'方法'在中文学术语境下常被理解为'提出新算法'，但实际交付物是分析框架+设计准则（非新算法）"
classification: "新维度'创新点措辞敏感性'"
s033_input: "S033'措辞改写'——中文'方法'歧义检测，分析类 vs 算法类动词谱系"
```

```yaml
id: A-104
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:116"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "公式 bug 导致错误结论（VV 公式 B 误用 unwrap(angle(avg)*M)/M，使弱/中湍流 BER 膨胀 100-1800 倍），据此声称 VV 全湍流有害被证伪"
original_quote: "根因是 VV 相位恢复公式 bug：使用了 unwrap(angle(avg)*M)/M（公式 B）而非正确的 unwrap(angle(avg))/M（公式 A）"
classification: "检测器ID'公式 bug 致证伪'（CONCLUSIONS X-05/X-08）"
s033_input: "N/A（技术核验类，非写作改写）"
```

## B 维度

```yaml
id: B-101
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/开题报告v2-导师批注.md:120"
source_agent: "粗扫3"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师判定通篇 AI 代写痕迹重，AI 仅应辅助、本人须逐句深入思考"
original_quote: "AI应仅为辅助，不能照搬AI高生成度结果，本人应深入思考、逐句思考"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师硬底线'去 AI 代写痕迹'"
```

```yaml
id: B-102
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/开题报告v2-导师批注.md:156"
source_agent: "粗扫3"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师判定综合验证类实验（3.6.3/3.6.4）属学习教学，不属科学研究——学术定位判据"
original_quote: "3.6.3和3.6.4属于学习教学，不属于科学研究"
is_covered: "是"
covered_by: "Popper 可证伪性判据（R001）"
new_dimension: "N/A"
```

```yaml
id: B-103
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/开题报告v2-导师批注.md:215"
source_agent: "粗扫3"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师要求参考文献以 trans 期刊为主（Tier-1），所引期刊水平低，且格式不符学校规范"
original_quote: "所引用期刊水平低，应以 trans 为主；格式不符合学校规范"
is_covered: "是"
covered_by: "引用质量 rubric（B11，GB7714 + Tier 分级）"
new_dimension: "N/A"
```

```yaml
id: B-104
source_ref: "/mnt/d/code/study/research-protocol/毕设/开题报告/开题报告v2-导师批注.md:171"
source_agent: "粗扫3"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师判定可行性分析末尾的底线交付声明是机器语言（AI 生成的套话），须人工逐句理顺"
original_quote: "机器语言"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师判据'机器语言检测'（可行性套话/AI 兜底句）"
```

```yaml
id: B-105
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S001-advisor-meeting-and-direction-framework.md:17"
source_agent: "粗扫1"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师判定 AI 全权代写（学生自认 AI 精读文献），质疑理解归属——学位授予人不是 AI"
original_quote: "谁精读了？AI精读了还是你精读了？；学位是授予张哲铜，不是授予张哲铜的AI"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师硬底线'AI 辅助边界'（与 B-101 互补：B-101 是写作层，本条是理解层）"
```

```yaml
id: B-106
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S001-advisor-meeting-and-direction-framework.md:36"
source_agent: "粗扫1"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师四条不可谈判底线之一——必须在 Word 模板上直接写，不能 markdown+pandoc"
original_quote: "必须在Word模板上直接写"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师硬底线'交付形态=Word 模板直写'（D002 决策来源）"
```

```yaml
id: B-107
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S001-advisor-meeting-and-direction-framework.md:19"
source_agent: "粗扫1"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师判定写作质量低于本科毕设水平，且结构错误（首节须是研究背景与意义非研究现状）"
original_quote: "我提溜任何一块出来，都有很大问题；你现在写的这个不如你当年的本科毕设"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师判据'通篇机器味 + 结构规范'"
```

## C 维度

```yaml
id: C-101
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:375"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "S1[CLAIM]为实现这一愿景…需要具备远超5G的性能指标 → S2[FACT]峰值速率大于100吉比特… → S3[TRANS]此外… → S5[NEED]因此…迫使… → S9[GAP]这使得…面临…问题，亟须要打破…"
why_good: "句子功能标注体系 DEF/FACT/CLAIM/EVAL/TRANS/GAP/NEED/CITE 把'写什么位置'显性化，仿写时按功能序列填内容即可复现人写节奏"
fewshot_target: "S033'段落衔接改写'——按句子功能序列重组段落"
```

```yaml
id: C-102
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:104"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "A做了X，B做了Y，C做了Z，但仍有不足（AI 清单体，逐篇平铺）"
rewritten_text: "先扬后抑：正面成果(1-2句)→让步转折(1句'虽然/尽管…但…')→不足/空白(1句)→收束到研究需求(1句)"
good_example: "虽然这些架构为…提供了指导思想，但智能化方案在实际部署过程中仍面临…因此，…是亟待解决的问题"
why_good: "先扬后抑是论证研究空白的黄金模式，暗示作者对领域有整体判断而非逐篇罗列"
fewshot_target: "S033'去清单体'——综述段改写为先扬后抑"
```

```yaml
id: C-103
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:211"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "文献[1]指出…[大段复述]；文献[2]做了Y…（AI 反模式：引用当论述起点）"
rewritten_text: ""
good_example: "移动通信系统每十年都会迎来一次巨大技术变革[1]（先用自己的话说清楚，引用附句末做背书）"
why_good: "引用是论断的'签证'不是论述的起点——归纳句用自己的话概括共性→展开最相关 1-2 篇→一句带过其余"
fewshot_target: "S033'引用嵌入改写'——引用后缀模式，去'文献[X]指出'"
```

```yaml
id: C-104
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/R011-chinese-academic-writing-patterns.md:173"
source_agent: "粗扫1"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "高质量中文论文衔接词密度远低于 AI 生成文本——靠语义承接（时间锚点/专有名词当路标/数据密度推进），而非连接词堆砌"
why_good: "低衔接词密度+高信息密度是人写特征；AI 靠'然而/此外/因此'堆砌，反而暴露"
fewshot_target: "S033'去翻译腔/段落衔接'——降衔接词密度，改语义承接"
```

## D 维度

```yaml
id: D-101
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:11"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "R1 开题阶段创新点只说方向不说结果——写'拟提出/拟建立/拟研究'，不写'实现了 XX dB 增益'，承诺做不到即挖坑"
step_group: "innovation-points 创新点写作 7 规则自检"
step_order: 1
vs_paperwrite: "paper-write 无开题阶段措辞门控，会把结果写进开题"
optimization: "加'开题 vs 论文'措辞阶段门控：开题禁结果声称"
```

```yaml
id: D-102
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:17"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "R2 创新点描述必须宽到能降级——'提出方法'做不出可退到'建立准则'，不能只写一条路"
step_group: "innovation-points 创新点写作 7 规则自检"
step_order: 2
vs_paperwrite: "paper-write 无退路宽度检查"
optimization: "加'退路宽度自检'：每条创新点须列≥2 级降级路径"
```

```yaml
id: D-103
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:25"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "R4 创新点不得与已证伪教训矛盾——禁碰符号级自适应(TL-03)/禁声称 KF 全湍流增益/禁声称 VV 全湍流有害/禁声称'湍流感知 R 矩阵'是贡献"
step_group: "innovation-points 创新点写作 7 规则自检"
step_order: 4
vs_paperwrite: "paper-write 无与已证伪结论库的交叉检查"
optimization: "加'已证伪清单(CONCLUSIONS X-xx)交叉门控'：声称自动比对证伪库"
```

```yaml
id: D-104
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:32"
source_agent: "细扫A"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "R5 专硕标准——不需提出全新理论，'分析→准则→设计方法'层级足够，对标曾嘉/Han2022/Wang2025 均为性能分析类贡献"
step_group: "innovation-points 创新点写作 7 规则自检"
step_order: 5
vs_paperwrite: "paper-write 无学位层级定位，会过度声称创新"
optimization: "加'学位层级(专硕/学硕/博士)声称门控'：专硕禁'全新理论'声称"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（本 agent 仅用"规则清单"+"批注原话"两种，均在枚举内）
- [x] 所有 source_ref 含行号（19/19 条均带 :line，已实读校准）
- [x] 所有 date_validity/direction 已标注（全"有效"/"当前(FSO)"，因 4 文件均 pivot 后）
- [x] id 前缀均为 -1xx（A-101~104 / B-101~107 / C-101~104 / D-101~104）
- [x] 同形态 2 份字段结构一致可拼接（规则清单：R011 的 A/C 条 + innovation-points 的 A/D 条字段顺序一致；批注原话：开题批注 B + S001 B 字段顺序一致）
