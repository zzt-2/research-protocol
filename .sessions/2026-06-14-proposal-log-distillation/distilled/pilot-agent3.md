# pilot agent-3 产出（失败案例 + 命名方法论 + 工作流蓝图）

## 提取统计
- 处理文件：6
  - 失败案例（序1）：S024-kf-stress-test.md + citation-verification/FINAL_OUTPUT.md
  - 命名方法论（序2）：cnki-thesis-survey.md + figure-composition-analysis.md
  - 工作流蓝图（序3）：S003-template-extraction-methodology.md
  - 工作流蓝图（序4）：PROMPT-001-writing-task-f.md
- 产出条目：A=2 B=6 C=6 D=8（合计 22）
- 行号校准说明：
  - R002 B9 原指针"S024 B2 段"无行号 → 已实读补齐 L147-162（B2 R 矩阵 FAIL）+ L310-320（D3 标准 PA-KF 反证）+ L286-291（D1 强湍流 KF 输给最优 Fixed）
  - R002 B12 原指针"FINAL_OUTPUT L26-31" → 已实读核对，Nguyen DOI 错误实际在 L59（错误 DOI）+ L62（正确 DOI），标题不匹配在 L60-63；原 L26-31 是 Castrillon 2015 段，行号已修正
  - R002 C10 原指针"L385-518 章节命名方法论" → 已实读确认 L385 起、L518 结束（§四 4.4 分节规律末）
  - R002 C5 原指针"第7节替换模板+第11节" → 已实读确认 L414-541（§七替换模板）、L638-678（§十一星地光链路示例）
  - R002 D1 原指针"S003 L1/L2/L3 + 11轮失败" → 已实读，L1/L2/L3 不是行号而是模板提取层级，11轮失败见 L11-33
  - R002 D2 原指针"PROMPT-001（24.6K）"无行号 → 已实读补齐 L1-30（对话隔离+token管理）、L140-253（5步循环）、L254-304（8维审查 R1-R8）

## A 维度

```yaml
id: A-301
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:59"
source_agent: "细扫B"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "AI 生成的引用元数据（DOI+标题）与真实论文完全不匹配——Nguyen 2020 的 DOI 错配到另一篇论文，标题也是编造的"
original_quote: "DOI: 10.1109/ACCESS.2020.2989012 ❌ 错误 / 标题: Phase Error (Tikhonov)... ❌ 错误"
classification: "新维度'AI 编造引用元数据'（检测器ID候选'引用存在性验证'）"
s033_input: "S033 引用检测器——必须验证 DOI+标题+期刊三件套与真实论文匹配，不能只验 DOI 格式"
```

```yaml
id: A-302
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S024-kf-stress-test.md:162"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "原本声称的核心创新'湍流感知 R 矩阵'经压力测试证伪——导频 h 估计对 R 无显著价值，增益来自 Kalman 跟踪机制本身"
original_quote: "判定: FAIL — 导频 h 估计对 R 矩阵无显著价值。KF 的增益主要来自 Kalman 跟踪机制本身（预测+更新），而非 h 感知的 R 矩阵。"
classification: "新维度'创新点有效性证伪'（检测器ID候选'压力测试 FAIL→结论砍掉'）"
s033_input: "S033 评估盲区——创新点声称需经过压力测试（消融/对照/边界）才能写入论文，未通过测试的贡献声称必须移除"
```

## B 维度

```yaml
id: B-301
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S024-kf-stress-test.md:374"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'核心贡献是否真实'——B2+D3 双重证伪，'湍流感知 R 矩阵'不是真实贡献"
original_quote: "B2+D3 双重验证 — \"湍流感知 R 矩阵\"不是真实贡献"
is_covered: "否"
covered_by: "N/A"
new_dimension: "压力测试 FAIL→结论证伪（贡献声称必须经消融/对照验证）"
```

```yaml
id: B-302
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S024-kf-stress-test.md:288"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'基线是否被公平设置'——Fixed 基线从未被正确优化（M_vv=64 远非最优 256），导致增益被人为放大"
original_quote: "强湍流下 KF pilot 输给最优 Fixed: 3.08% vs 2.22%，KF 反而差 1.4 dB"
is_covered: "否"
covered_by: "N/A"
new_dimension: "基线公平性审查（增益声称前必须验证对照基线已充分优化）"
```

```yaml
id: B-303
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:62"
source_agent: "细扫B"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'引用 DOI 是否指向真实论文'——Nguyen 2020 的 DOI 与标题完全不匹配（假 DOI 对应另一篇论文）"
original_quote: "DOI: 10.1109/ACCESS.2020.3036643 ✅ 正确 / 标题: Performance of Generalized QAM/FSO Systems..."
is_covered: "否"
covered_by: "N/A"
new_dimension: "DOI 存在性 + 标题匹配验证（不能只验 DOI 格式正确）"
```

```yaml
id: B-304
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:139"
source_agent: "细扫B"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'贡献声称是否绝对化'——AI 倾向写'首次/从无到有/完全空白'，但实际是'精细化提升'"
original_quote: "避免\"首次\"、\"空白\"等绝对化表述 / 强调我们的\"精细化\"贡献而非\"从无到有\""
is_covered: "是"
covered_by: "学术诚信'避免绝对化用语'"
new_dimension: "N/A"
```

```yaml
id: B-305
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md:96"
source_agent: "细扫B"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'研究空白声称是否精确'——'完全空白'被修正为'精细化建模空白'（JLT 2024 有 1 篇系统级分析）"
original_quote: "空白确认: H8需要从\"完全空白\"修正为\"精细化建模空白\""
is_covered: "否"
covered_by: "N/A"
new_dimension: "空白声明必须列反例（空白≠绝对零，需区分'无任何工作'与'无特定粒度工作'）"
```

```yaml
id: B-306
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S024-kf-stress-test.md:304"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
criticism_point: "评估'增益归因是否精确'——D2 消融揭示 VV 在所有场景有害、DPLL 才是真英雄，'Fixed 基线'因含 VV 被人为拉低"
original_quote: "FOE+VV 使 BER 从 10-13% 恶化到 27-30% / FOE+DPLL 单独达到 0.2-1.9%，是真正的核心贡献者"
is_covered: "否"
covered_by: "N/A"
new_dimension: "增益归因消融审查（每项增益必须拆解到具体模块，识别真英雄 vs 假贡献）"
```

## C 维度

```yaml
id: C-301
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:391"
source_agent: "细扫B"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "博士论文标题模式：[场景]+[技术]+关键技术研究 / [场景]+[问题]+研究 / [场景]+[子系统]+研究 / [技术方向]+算法研究/设计与实现"
why_good: "从 3 篇 FSO 博士论文归纳出 5 种可复用标题句式，新课题可直接套 [场景]+[技术]+关键技术研究 最常见模式"
fewshot_target: "S033'论文标题命名规范化'——学位论文标题句式选择"
```

```yaml
id: C-302
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:412"
source_agent: "细扫B"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "第一章绪论标准结构：1.1 研究背景及意义 / 1.2 国内外研究现状（1.2.1 领域现状 / 1.2.2 技术现状 / 1.2.3 子技术现状）/ 1.3 论文主要工作及内容安排"
why_good: "从多篇真实学位论文归纳的绪论三级结构，研究现状按 领域→技术→子技术 逐层收敛"
fewshot_target: "S033'章节命名规范化'——绪论章节结构与命名"
```

```yaml
id: C-303
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:432"
source_agent: "细扫B"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "中间核心章节命名规律：X.1 引言 / X.2 理论分析或模型建立（X.2.1 子问题1分析模型 / X.2.2 子问题2分析模型 / X.2.3 数值仿真与分析）/ X.3 核心方法 / X.4 实验验证 / X.5 本章小结"
why_good: "每章一个独立技术贡献的标准 5 段式结构，理论与仿真分节、实验可选、小结收束"
fewshot_target: "S033'章节命名规范化'——核心技术章节命名规律"
```

```yaml
id: C-304
source_ref: "/mnt/d/code/study/research-protocol/projects/thesis-fso/cnki-thesis-survey.md:474"
source_agent: "细扫B"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "均衡/预补偿/同步类章节命名模式：信道均衡=[场景]+信道均衡+技术/算法；相位同步=[同步对象]+同步/估计+方法/模块/算法；预补偿=[损伤类型]+补偿/校正/自适应+技术/方法"
why_good: "按技术类型分流的 3 套命名公式，覆盖 FSO 信号处理三大子领域，避免命名混乱"
fewshot_target: "S033'章节命名规范化'——技术子领域的章节标题句式"
```

```yaml
id: C-305
source_ref: "/mnt/d/code/study/research-protocol/figure-composition-analysis.md:422"
source_agent: "粗扫3"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "研究路线图标题模板：{研究对象}{核心能力}{任务目标}技术研究，例'星地相干光链路湍流鲁棒接收与质量评估技术研究'——三要素（对象+能力+任务），不写背景原因"
why_good: "标题只含研究对象+技术能力+任务目标，背景原因留给正文，避免标题变文献综述"
fewshot_target: "S033'图表叙事改写'——研究路线图/总览图的标题命名"
```

```yaml
id: C-306
source_ref: "/mnt/d/code/study/research-protocol/figure-composition-analysis.md:507"
source_agent: "粗扫3"
material_form: "命名方法论"
date_validity: "有效"
direction: "当前(FSO)"
original_text: ""
rewritten_text: ""
good_example: "关键技术层命名格式：{约束条件}下{核心任务}技术，三项分别对应 识别/表征、估计/恢复/增强、评估/决策/综合优化——三章关键技术横向递进"
why_good: "关键技术命名统一带约束条件（如'弱光闪烁条件下'），且三章功能递进不割裂，配绿色横向箭头显式串联"
fewshot_target: "S033'图表叙事改写'——关键技术条 + 研究内容层的命名与递进"
```

## D 维度

```yaml
id: D-301
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S003-template-extraction-methodology.md:196"
source_agent: "粗扫1"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "从参考论文提取写作模板的方法论：模板格式经三方交叉审查（architect 结构完整性 + critic 防坑能力 + planner 可用性）迭代到最终格式"
step_group: "S003 模板提取方法论"
step_order: 1
vs_paperwrite: "paper-write 现无'三方交叉审查模板格式'机制，蓝图/大纲协议未经防坑角度检验"
optimization: "模板格式设计应引入 architect/critic/planner 三视角审查，避免单视角遗漏跨节问题"
```

```yaml
id: D-302
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S003-template-extraction-methodology.md:16"
source_agent: "粗扫1"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "反面教训：'让 LLM 写全文'策略失败——11 轮提示词调优后否定规则遵守率仅 30-50%，加 few-shot 后约 70% 仍不够；翻译腔 27+、清单体 7 段、超长句 22 处等系统性残留"
step_group: "S003 模板提取方法论"
step_order: 2
vs_paperwrite: "paper-write 若采用'LLM 写全文'策略会重蹈 11 轮失败的覆辙"
optimization: "采用'人写 LLM 查'策略（D009），人写第一稿，LLM 只负责文献检索/格式排版/一致性检查——翻译腔/AI 味风险显著降低"
```

```yaml
id: D-303
source_ref: "/mnt/d/code/study/research-protocol/.sessions/thesis-direction-pivot/S003-template-extraction-methodology.md:231"
source_agent: "粗扫1"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "最终模板格式：元信息（3 行）+ 论证主线（3-5 句）+ 全局约定表（术语/时态/自称/引用风格）+ 逐节四列表格（功能/衔接/示例/约束+自查）+ 可选跨节数据分布表 + 可选分层全局检查（L1 句子级 grep / L2 段落级 / L3 全局级）"
step_group: "S003 模板提取方法论"
step_order: 3
vs_paperwrite: "paper-write 蓝图协议有论证主线+章节功能定位，但缺'全局约定表'和'分层全局检查'，跨节数据分布未显式管理"
optimization: "蓝图/大纲协议补'全局约定表'（低工作量高影响）+ 分层检查（写完后 grep 用），防数据三重出现/术语不一致/机械句式"
```

```yaml
id: D-304
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md:13"
source_agent: "粗扫3"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "对话隔离写作：每对话写 1 章，串行 Ch2→Ch3→Ch4→Ch5；token 管理硬规范——主对话严禁直接读 section-outline/writing-patterns 等大文件（任一都会撑爆上下文），全由子 agent 消化浓缩后返回"
step_group: "PROMPT-001 对话隔离写作流"
step_order: 1
vs_paperwrite: "paper-write 若在单次调用塞入全部大文件会触发上下文溢出；需内置 token 预算与子 agent 消化机制"
optimization: "设计子 agent 消化协议：大文件（>500 行）禁止主对话直读，由子 agent 按节提取~50 行写作向导返回；主对话只持有 prompt + 向导 + 审查结果 + 产出"
```

```yaml
id: D-305
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md:144"
source_agent: "粗扫3"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "逐节 5 步循环：Step1 派 3 个写作向导子 agent 并行（结构向导+公式向导+语言向导，各读 2 文件）→ Step2 主对话合并写正文 → Step3 派 8 个审查子 agent 并行（R1-R8）→ Step4 逐条修正 → Step5 推进下一节"
step_group: "PROMPT-001 对话隔离写作流"
step_order: 2
vs_paperwrite: "paper-write 需对照此 5 步循环设计；现状多为'一次性生成'，缺'向导→写→审查→修正'的闭环"
optimization: "每节写作内置 5 步循环，向导/审查子 agent 并行化，审查返回问题清单不打分（避免程度判断不可靠）"
```

```yaml
id: D-306
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md:258"
source_agent: "粗扫3"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "8 维审查 rubric R1-R8（每节写完并行派出）：R1 语言质量 / R2 论断依据 / R3 技术常识 / R4 术语合规（读 TERMS.md）/ R5 符号一致（读 symbol-conventions.md）/ R6 禁忌内容（旧方向+绝对化）/ R7 图表公式编号 / R8 动词强度（对照动词降级表）"
step_group: "PROMPT-001 对话隔离写作流"
step_order: 3
vs_paperwrite: "paper-write 现无这 8 维并行审查；动词强度（R8）和禁忌内容（R6）是最易遗漏的维度"
optimization: "把 R1-R8 做成可并行调用的审查 agent 池，每节生成后自动触发；动词强度表内置为规则（引用现有模型禁'建立/提出'改'介绍'）"
```

```yaml
id: D-307
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md:317"
source_agent: "粗扫3"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "全章写完后跨章一致性审查（必做）：动词一致性（本章动词强度与已降级章节一致）+ 术语+符号一致性（读 cross-chapter-notes.md）+ 章节描述对齐（本章对其他章的描述与§1.3 一致）+ DeepSeek 外部评审（§1.1 实测获 92 分验证有效）"
step_group: "PROMPT-001 对话隔离写作流"
step_order: 4
vs_paperwrite: "paper-write 需补跨章一致性层；现状多为单章质量，跨章动词/术语漂移无机制"
optimization: "维护 cross-chapter-notes.md 作为跨章状态文件（术语/符号/已确认表述/待后续章注意），每章结束追加，后续章向导子 agent 必读"
```

```yaml
id: D-308
source_ref: "/mnt/d/code/study/research-protocol/.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md:561"
source_agent: "粗扫3"
material_form: "工作流蓝图"
date_validity: "有效"
direction: "当前(FSO)"
workflow_step: "范文验证铁律 1-4（4 篇范文交叉验证）：铁律1 节首第一句直接切入禁'上节/前节/前文+动词'回指；铁律2 已定义符号直接用禁'（定义见§X.X）'；铁律3 参数解释统一'式中/其中，A为...，B为...'；铁律4 符号重用靠上下文区分不显式声明"
step_group: "PROMPT-001 对话隔离写作流"
step_order: 5
vs_paperwrite: "paper-write 需内置这 4 条铁律作为硬约束（经范文交叉验证，非主观偏好）"
optimization: "铁律 1-4 做成 grep 可检测的规则（如搜索'上节|前节|前文'+'动词'即报铁律1违规），嵌入 L1 句子级检查"
```

## 可合并性自检
- [x] 所有 material_form 字符串匹配 7 形态枚举（失败案例 10 条 / 命名方法论 6 条 / 工作流蓝图 6 条，均属 7 形态枚举）
- [x] 所有 source_ref 含行号（22 条全部带 :line，WSL 路径 /mnt/d/...）
- [x] 所有 date_validity/direction 已标注（22 条全部填"有效"+"当前(FSO)"）
- [x] id 前缀均为 -3xx（A-301/302、B-301~306、C-301~306、D-301~308）
- [x] 3 形态（失败案例/命名方法论/工作流蓝图）schema 统一，字段结构与其他 agent 一致（同维度字段顺序与 scan-template.md FROZEN schema 完全一致）
- [x] D 维度工作流已拆 step + step_group + step_order（S003 组 3 步 D-301/302/303；PROMPT-001 组 5 步 D-304~308）
