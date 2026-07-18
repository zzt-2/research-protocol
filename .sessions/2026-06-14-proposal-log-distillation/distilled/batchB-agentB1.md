# batchB agent-B1（重派）产出（B 维前半 7 源：公平性/铁律/诚实评估/引用可靠性/空白分级/学术诚信/硕士门槛）

> 2026-06-15 | B 维（评估标准）前半 7 份素材源全量蒸馏 | agent-B1 区 id 前缀 -4xx
> 上游：R002 素材源索引 B4/B7/B10/B13/B14/B15/B16
> 下游契约：D002 B-eval-criteria 字段
> 不变量：① 只读不改原文 ② 全量实读 ③ 每条带 file:line 回溯 ④ 跨 agent 可合并

## 提取统计
- 处理文件：8（B4=2 / B7=1 / B10=1 / B13=1 / B14=1 / B15=1 / B16=1）
- 产出条目：B=17（B-401~B-417）
- material_form 分布：审查rubric×6 / 规则清单×4 / 失败案例×3 / 批注原话×2
- 行号校准说明：
  - B4 advisor-brief.md：公平性审查三步法在 L35-43
  - B4 "不要全信"元标准：原话出自导师反馈，S023 L9 记录背景来源
  - B7 Ch2-reviews.md：H/M/L 三级分级框架 L158-376，铁律1-4 在 L367-375（pilot B-204/B-205 已提铁律1/3，本批补铁律2 L371 + 铁律4 L375 + H/M/L 分级框架 L167/L206/L279）
  - B10 S023 §5 100种子修正 L66-91，§6 诚实评估 L93-101
  - B13 VERIFICATION_SUMMARY.md 4 维 rubric 表 L103-109
  - B14 literature_notes.md 空白分级 rubric L184-189
  - B15 FINAL_OUTPUT.md 学术诚信 4 条 L137-140
  - B16 S006 硕士评审权重 L99-141

## B 维度

```yaml
id: B-401
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/advisor-brief.md:35"
source_agent: "粗扫2"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'增益是否真实'——增益声称须经三层公平性审查：①算法层（新方法是否用了旧方法没有的特权信息，如完美信道信息）②实现层（旧方法实现是否有 bug 被人为拉低）③预处理层（两者预处理是否一致），每层只改一个变量隔离验证"
original_quote: "算法层：发现新方法用了完美信道信息...实现层：发现卡尔曼滤波器的实现有bug...预处理层：发现两种方法都用了完美信道信息做信号均衡"
is_covered: "否"
covered_by: "N/A"
new_dimension: "公平性审查三步法（算法层/实现层/预处理层，每层单变量隔离验证）——与 B-302 基线公平性审查互补"
```

```yaml
id: B-402
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S023-ch4-systematic-simulation.md:9"
source_agent: "粗扫1"
material_form: "批注原话"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "导师元标准——对自己的仿真结果'不要全信'，默认假设里面有错误，主动找失败条件/验证增益真实性/定位崩溃边界，每条 PASS 需硬证据、每条 FAIL 需根因分析"
original_quote: "导师反馈 KF 结果'不要全信'...代码审查确认 3 个中等问题。战略性转向稳妥的系统性分析路线"
is_covered: "否"
covered_by: "N/A"
new_dimension: "导师硬底线'自我证伪心态'（元标准：默认结果不可信→主动压力测试，是 B-301 压力测试FAIL→证伪 的认知前提）"
```

```yaml
id: B-403
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:167"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "审查发现三级优先级分级框架——H（高，结构性问题，必须修正）/ M（中，文风问题，~20项核心）/ L（低，局部修正，~100项），据此分配修正资源"
original_quote: "高优先级（结构性，6项，必须修正）/ 中优先级（文风，~20项核心）/ 低优先级（局部修正，~100项，选列核心）"
is_covered: "否"
covered_by: "N/A"
new_dimension: "审查发现三级优先级分级 rubric（H结构性必改/M文风核心/L局部选改）——审查产出的分级机制本身"
```

```yaml
id: B-404
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:371"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "铁律 2——已定义符号直接使用，禁用'（定义见§X.X）'显式交叉引用格式，依赖上下文区分"
original_quote: "范文没有'（定义见§X.X）'格式。已定义符号直接使用，依赖上下文"
is_covered: "否"
covered_by: "N/A"
new_dimension: "交叉引用格式铁律（禁'定义见§X.X'，符号靠上下文复用）——与 pilot B-204 铁律1 / B-205 铁律3 同属范文验证铁律族"
```

```yaml
id: B-405
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:375"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "铁律 4——符号重用通过上下文区分不显式声明（如 α/β 在大气衰减和 GG 分布中重用直接用），但严重冲突时（如 γ）范文用换符号（κ）主动避免"
original_quote: "符号重用通过上下文区分，不显式声明...γ的冲突有范文用κ(kappa)表示衰减系数来主动避免"
is_covered: "否"
covered_by: "N/A"
new_dimension: "符号重用铁律（默认上下文区分，严重冲突才换符号）——补全范文验证铁律族第4条"
```

```yaml
id: B-406
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S023-ch4-systematic-simulation.md:83"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'结论叙事是否被种子数不足掩盖'——小样本（单种子/几种子）下'全面优于'的声称经 100 种子验证后被推翻，修正为'仅在强湍流且仅 62-71% 种子成立'，弱/中湍流前馈反而优 3.5-10 dB"
original_quote: "初始报告强调'DPLL 全面优于 VV/BPS'是不准确的...正确叙事：DPLL 在强湍流下提供可靠性...但弱/中等湍流下前馈方法更优"
is_covered: "否"
covered_by: "N/A"
new_dimension: "种子数充分性审查（结论声称须经≥100 种子鲁棒性验证，识别'仅部分条件成立'的边界，避免小样本过度声称）"
```

```yaml
id: B-407
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S023-ch4-systematic-simulation.md:95"
source_agent: "粗扫1"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "诚实评估范式——对自身贡献按'创新性/发现价值/对开题支撑/对最终论文支撑'四维自评并给出诚实分级（创新性弱/价值中/开题勉强够/最终论文不够），不掩饰短板"
original_quote: "创新性：弱...发现的价值：中等...对开题报告的支撑：勉强够用...对最终论文的支撑：不够"
is_covered: "否"
covered_by: "N/A"
new_dimension: "贡献诚实自评 rubric（创新性/价值/开题支撑/论文支撑 四维分级，主动暴露不足）"
```

```yaml
id: B-408
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/VERIFICATION_SUMMARY.md:103"
source_agent: "细扫B"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'引用是否可靠'——4 维度评分：①存在性（论文是否真实存在）②内容匹配（引用所述内容是否与论文实际一致）③场景匹配（论文场景是否与引用声称场景一致）④总体可靠性（综合），每维分高/中/低"
original_quote: "存在性 | 内容匹配 | 场景匹配 | 总体可靠性（Oh 2001 全高 / Nguyen 2020 存在性中、标题不匹配、总体中）"
is_covered: "是"
covered_by: "引用质量 rubric（B11，GB7714 + Tier 分级）——4 维可靠性是内容层验证补充"
new_dimension: "N/A"
```

```yaml
id: B-409
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/VERIFICATION_SUMMARY.md:109"
source_agent: "细扫B"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'引用内容是否与论文实际匹配'——存在性高≠内容匹配：Nguyen 2020 论文真实存在（存在性中），但引用标题与实际论文不匹配（内容匹配=标题不匹配），单验存在性不够"
original_quote: "Nguyen 2020 | ⚠️ 中（存在性）| ⚠️ 标题不匹配（内容匹配）| ✅ FSO（场景）| ⚠️ 中（总体）"
is_covered: "是"
covered_by: "DOI 存在性 + 标题匹配验证（pilot B-303）——本条强调 4 维中'内容匹配'独立于'存在性'"
new_dimension: "N/A"
```

```yaml
id: B-410
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:184"
source_agent: "细扫B"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'研究空白是否成立'——空白分 4 级类型：①确认空白（去重结果无一满足三重组合）②部分空白（非绝对零，有1篇但系统性方法为零）③文献空白（无综述但专题研究已充分）④组合空白（三重组合无），每级配验证结论+创新潜力星级"
original_quote: "空白类型：方法空白/场景空白/组合空白/文献空白；验证结论：部分空白（非绝对零...）/确认空白（无一满足）/文献空白"
is_covered: "否"
covered_by: "N/A"
new_dimension: "研究空白 4 级分级 rubric（确认/部分/文献/组合 + 创新潜力★星级）——是 pilot B-305'空白声明列反例'的分级框架本体"
```

```yaml
id: B-411
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/literature_notes.md:186"
source_agent: "细扫B"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'空白表述是否精确'——'部分空白'级要求显式列出反例论文（如 JLT 2024 有1篇 MDM-MIMO / 张岱2018博士论文），并精确界定'系统性方法论文为零'的子粒度，区分'绝对零'与'特定粒度零'"
original_quote: "部分空白：非绝对零（JLT 2024有1篇MDM-MIMO，张岱2018博士论文需精读），但'GG湍流+相干PSK+导频辅助信道估计'系统性方法论文为零"
is_covered: "是"
covered_by: "空白声明必须列反例（pilot B-305）——本条提供'部分空白'级的精确表述模板"
new_dimension: "N/A"
```

```yaml
id: B-412
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:137"
source_agent: "细扫B"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "学术诚信 4 条检查清单框架——①所有 DOI 必须经过验证 ②标题和期刊信息必须准确 ③避免'首次/空白'绝对化表述 ④强调'精细化'贡献而非'从无到有'"
original_quote: "所有DOI必须经过验证 / 标题和期刊信息必须准确 / 避免'首次'、'空白'等绝对化表述 / 强调我们的'精细化'贡献而非'从无到有'"
is_covered: "是"
covered_by: "学术诚信'避免绝对化用语'（pilot B-304 提取第③条）——本条是 4 条完整框架，补①②④"
new_dimension: "N/A"
```

```yaml
id: B-413
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:138"
source_agent: "细扫B"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "学术诚信第①②条——DOI 必须验证（不能只验格式正确，须验指向真实论文）+ 标题/期刊信息必须准确（引用元数据三件套 DOI+标题+期刊须与真实论文一致），与 pilot B-303 互补"
original_quote: "所有DOI必须经过验证 / 标题和期刊信息必须准确"
is_covered: "是"
covered_by: "DOI 存在性 + 标题匹配验证（pilot B-303）+ 引用质量 rubric 4 维（B-408）"
new_dimension: "N/A"
```

```yaml
id: B-414
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:140"
source_agent: "细扫B"
material_form: "规则清单"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "学术诚信第④条——贡献定位须'精细化'而非'从无到有'，强调区分式/精细化建模贡献，与'避免绝对化'配套（第③条管措辞，第④条管贡献定位的实质内容）"
original_quote: "强调我们的'精细化'贡献而非'从无到有'"
is_covered: "否"
covered_by: "N/A"
new_dimension: "贡献定位'精细化'原则（与避免绝对化互补：措辞层去绝对化 + 实质层定位精细化）"
```

```yaml
id: B-415
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:105"
source_agent: "细扫C"
material_form: "审查rubric"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "评估'硕士论文是否够格'——学位条例第五条门槛是'一定的新见解或新内容'（非'重大创新'），硕士与博士的根本分界线；配 6 维评审权重表（选题15-20%/文献综述10-15%/研究方法15-20%/创新性20-25%/工作量15-20%/写作规范10-15%）"
original_quote: "《学位条例》第五条——'一定的新见解或新内容'。不是'重大创新'，这是硕士与博士的根本分界线"
is_covered: "是"
covered_by: "导师硬底线（pilot B-101~107）+ 专硕标准（pilot D-104）——本条提供官方法律依据+6维量化权重"
new_dimension: "N/A"
```

```yaml
id: B-416
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:118"
source_agent: "细扫C"
material_form: "规则清单"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "硕士级创新门槛 4 类（满足任意一条即可）——①应用创新（已有方法到新领域，最常见门槛最低）②方法改进（针对性改进/组合）③数据/场景创新（方法不新但数据/场景首次）④集成创新（多方法首次系统性整合），创新点 2-3 条即可"
original_quote: "应用创新：已有方法应用到新领域...方法改进...数据/场景创新...集成创新...创新点2-3条即可"
is_covered: "是"
covered_by: "专硕标准（pilot D-104'分析→准则→设计方法'层级足够）——本条是创新门槛的 4 类操作化分类"
new_dimension: "N/A"
```

```yaml
id: B-417
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md:128"
source_agent: "细扫C"
material_form: "失败案例"
date_validity: "方法论可继承-技术作废"
direction: "旧(NTN/DRL)"
criticism_point: "评估'论文是否会因常见原因不通过'——硕士不通过 Top5：①创新性不足（最高频，主要工作仅为调参和对比）②工作量不够（实验单薄缺消融/统计检验）③文献综述薄弱（仅罗列不分析）④写作质量问题（逻辑混乱）⑤研究方法缺陷（baseline 不充分）"
original_quote: "创新性不足（最高频）——主要工作仅为调参和对比 / 工作量不够——缺少消融和统计检验 / 文献综述薄弱——仅罗列不分析"
is_covered: "是"
covered_by: "Popper 可证伪性（①创新性不足）+ 基线公平性（⑤baseline 不充分，B-302）+ 增益归因消融（②消融，B-306）"
new_dimension: "N/A"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（审查rubric×6 / 规则清单×4 / 失败案例×3 / 批注原话×2）
- [x] 所有 source_ref 含行号（17/17 条均带 :line，WSL 路径 /mnt/d/...）
- [x] 所有 date_validity/direction 已标注（B4/B7/B10/B13/B14/B15 "有效"+"当前(FSO)"；B16 "方法论可继承-技术作废"+"旧(NTN/DRL)"）
- [x] id 前缀均为 -4xx（B-401~B-417）
- [x] 与 pilot 无重复：B-404/B-405 补铁律2/4（pilot B-204/B-205 是铁律1/3，互补）；B-410 空白分级框架（pilot B-305 是"列反例"）；B-412 4条框架（pilot B-304 仅第③条）；B-409 内容匹配维度细化（pilot B-303 是 DOI+标题）
- [x] is_covered 判定与 pilot 一致（已有 rubric 不重复造 new_dimension）
- [x] 同形态跨 agent 字段结构一致可拼接
