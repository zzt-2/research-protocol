# pilot agent-2 产出（diff 对比 + 审查 rubric）

## 提取统计
- 处理文件：4
- 产出条目：A={0} B={8} C={7} D={0}
- 行号校准说明：R002 标"行号待补"的 Ch2-reviews.md 各段已实读校准——L22-27(R1 diff)/L117-122(R2 §2.4 diff)/L36-38(R8 动词强度)/L4-17(R1-R8 汇总表)/L367-375(铁律1-4)；CONCLUSIONS.md L8-15(安全等级)/L393-405(证伪表)/L418-424(用语表)；R003 L108-134(Before→After 三组表) 全部实读确认。

## A 维度

（本 pilot 未从这 4 份文件提取 A 维度条目——A 痛点主要源在 innovation-points/S017/advisor-revision，非本次 4 份 diff/rubric 形态文件的主映射维度）

## B 维度

```yaml
id: B-201
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:6"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "user 自审 8 维度体系——R1 语言质量作为审查维度存在，量化发现 17+0+2 项问题"
original_quote: "R1 语言质量 | 17 | ✅已修正"
is_covered: "是"
covered_by: "8 维 R1-R8 自审 rubric"
new_dimension: "N/A"
```

```yaml
id: B-202
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:8"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "R8 动词强度维度——已有模型/他人工作用'建立/实现'是过强动词，应降为'介绍/给出'"
original_quote: "建立信号模型→介绍信号模型；建立了...定量关系→给出了"
is_covered: "是"
covered_by: "8 维 R1-R8 自审 rubric（R8 动词强度）"
new_dimension: "N/A"
```

```yaml
id: B-203
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:117"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "R2 论断依据——定量结论必须带推导/数据支撑，无支撑的程度词必须删除或补据"
original_quote: "约11 dB→加推导 20log10(1700/500)≈10.7 dB；显著下降缺数据→下降"
is_covered: "是"
covered_by: "8 维 R1-R8 自审 rubric（R2 论断依据）"
new_dimension: "N/A"
```

```yaml
id: B-204
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:369"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "铁律 1——范文无'上节/前节/前文+动词'回指句，节首直接切入新内容不回指"
original_quote: "范文没有'上节/前节/前文+动词'回指句...节首第一句直接切入新内容，不先回指"
is_covered: "否"
covered_by: "N/A"
new_dimension: "回指句禁忌（范文对照铁律级）"
```

```yaml
id: B-205
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:373"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "铁律 3——参数解释统一'式中/其中，A 为...，B 为...'格式，高度一致无其他变体"
original_quote: "参数解释统一'式中/其中，A为...，B为...'格式。高度一致，无其他变体"
is_covered: "否"
covered_by: "N/A"
new_dimension: "参数解释格式铁律"
```

```yaml
id: B-206
source_ref: "/mnt/d/code/study/research-protocol/毕设/CONCLUSIONS.md:10"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "结论安全等级 4 级 rubric——✅可写/⚠️需限定/❌不可写/🔄待重验，决定每条结论能否入论文"
original_quote: "✅可写:理论+仿真双重支撑|⚠️需限定:需标注边界条件|❌不可写:已证伪/不可靠"
is_covered: "否"
covered_by: "N/A"
new_dimension: "结论安全等级 rubric（写作门控）"
```

```yaml
id: B-207
source_ref: "/mnt/d/code/study/research-protocol/毕设/CONCLUSIONS.md:395"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "已证伪结论 X-01~X-09 清单——'湍流感知 R 矩阵'等 9 条原声称已被证伪，不得入论文"
original_quote: "X-01:湍流感知R矩阵是贡献|X-05:VV在所有湍流下有害(基于VV公式bug)"
is_covered: "否"
covered_by: "N/A"
new_dimension: "已证伪声称清单（写作黑名单）"
```

```yaml
id: B-208
source_ref: "/mnt/d/code/study/research-protocol/毕设/CONCLUSIONS.md:418"
source_agent: "细扫A"
material_form: "审查rubric"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "写作统一用语表——归一化辐照度 h（禁'信道增益'）/GG 湍流衰落模型（禁'GG 分布模型'）/光强起伏（禁'闪烁'）"
original_quote: "归一化辐照度h|禁止:信道增益；Gamma-Gamma湍流衰落模型|禁止:GG分布模型"
is_covered: "是"
covered_by: "8 维 R1-R8 自审 rubric（R4 术语合规）"
new_dimension: "N/A"
```

## C 维度

```yaml
id: C-201
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:36"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "建立信号模型 / 建立噪声模型 / 建立了...定量关系"
rewritten_text: "介绍信号模型 / 删除总领句直接从来源切入 / 给出了...定量关系"
good_example: ""
why_good: "已有模型/他人工作用弱动词'介绍/给出'，'建立'专用于原创推导，动词强度匹配实际贡献"
fewshot_target: "S033'动词强度改写'——已有模型去'建立'化"
```

```yaml
id: C-202
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:118"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "约 11 dB"
rewritten_text: "约 10.7 dB（加注 20log10(1700/500)≈10.7 dB）"
good_example: ""
why_good: "定量结论必须带推导链，数字从'约'升级为'可验算'，消除无支撑断言"
fewshot_target: "S033'论断依据补强'——定量数字补推导"
```

```yaml
id: C-203
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:121"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "远高于 / 显著下降"
rewritten_text: "高于 / 下降"
why_good: "无数据支撑的程度副词必须删除，避免绝对化"
fewshot_target: "S033'避免绝对化'——无数据去程度副词"
```

```yaml
id: C-204
source_ref: "/mnt/d/code/study/research-protocol/毕设/正文/Ch2-reviews.md:244"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "接收信号光场写作："
rewritten_text: "接收信号光场可表示为："
why_good: "范文库无'写作'引入公式，统一用'可表示为'，避免自创偏离范文"
fewshot_target: "S033'公式引入句式规范化'——去'写作'改'可表示为'"
```

```yaml
id: C-205
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-mega-constellation-gnn-routing/paper_materials/_sources/R003-writing-norms-contribution-claims.md:112"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: "本文创新性地提出了基于 GNN 的路由算法"
rewritten_text: "本文针对 LEO 卫星网络路由场景，设计并验证了基于 GNN 的路由方案"
good_example: ""
why_good: "去'创新性地提出'，改为'针对场景设计并验证'——场景适配贡献定位，动词匹配非新颖方法"
fewshot_target: "S033'贡献声称降级'——应用型研究去'创新性'，改场景适配定位"
```

```yaml
id: C-206
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-mega-constellation-gnn-routing/paper_materials/_sources/R003-writing-norms-contribution-claims.md:114"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: "首次将 GNN 应用于 LEO 卫星网络"
rewritten_text: "据作者所知，本文首次在 [具体条件] 下系统评估了 GNN 在 LEO 网络中的表现"
good_example: ""
why_good: "绝对化'首次'加'据作者所知'限定+具体条件收窄，避免无界过度声称"
fewshot_target: "S033'避免绝对化'——'首次'加限定语和条件收窄"
```

```yaml
id: C-207
source_ref: "/mnt/d/code/study/research-protocol/projects/_archive/leo-mega-constellation-gnn-routing/paper_materials/_sources/R003-writing-norms-contribution-claims.md:133"
source_agent: "细扫C"
material_form: "diff对比"
date_validity: "方法论可继承-技术作废"
direction: "旧(GNN/路由)"
original_text: "GNN 在所有指标上全面超越 ECMP"
rewritten_text: "GNN 在 E2E delay 上相比 ECMP 降低 20%，MLU 改善有限（4%）"
good_example: ""
why_good: "'全面超越'改为分指标量化，诚实区分显著改善(E2E -20%)和有限改善(MLU 4%)，不掩盖弱项"
fewshot_target: "S033'结果定位精确化'——'全面超越'改分指标量化"
```

## D 维度

（本 pilot 未从这 4 份文件提取 D 维度条目——D 工作流主要源在 S003/PROMPT-001/CONCLUSIONS-VERIFY-PLAN，非本次 diff/rubric 形态文件的主映射维度）

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（本文件用：审查rubric×5、diff对比×7、失败案例×1）
- [x] 所有 source_ref 含行号（12 条均带 :Lxx）
- [x] 所有 date_validity/direction 已标注（pivot 2026-05-29；当前 FSO / 旧 GNN 标"方法论可继承-技术作废"）
- [x] id 前缀均为 -2xx（B-201~208 / C-201~207）
- [x] 同形态 2 份字段结构一致可拼接：diff 形态（Ch2-reviews C-201~204 + R003 C-205~207）original_text/rewritten_text/why_good/fewshot_target 四字段齐全；rubric 形态（Ch2-reviews B-201~205 + CONCLUSIONS B-206~208）criticism_point/is_covered/covered_by/new_dimension 四字段齐全，跨文件同形态可直拼

## 模板容量验证结论
- **diff 形态**：模板 C 维度 original_text/rewritten_text 双字段完美适配前后对比；Ch2-reviews（FSO 当前方向，术语/动词类）和 R003（GNN 旧方向，贡献声称类）两类 diff 均能装入，date_validity 字段区分有效 vs 方法论可继承。
- **审查 rubric 形态**：模板 B 维度 criticism_point + is_covered + covered_by/new_dimension 四字段完美适配；Ch2-reviews 8 维 R1-R8 和 CONCLUSIONS 安全等级/证伪表/用语表三套 rubric 均能装入，is_covered=是→映射已有 rubric、否→new_dimension 两种分支都验证通过。
- **无 schema 装不下的情况**。唯一边界：C 维度 good_example 字段对 diff 形态为空（diff 用 original/rewritten 二元），纯范例形态才填 good_example——模板已用"diff 形态必填；纯范例形态可只填 good_example"说明覆盖，无歧义。
