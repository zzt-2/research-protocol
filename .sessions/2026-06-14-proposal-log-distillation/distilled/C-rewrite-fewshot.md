# C 维度：写作范例 few-shot（C-rewrite-fewshot）

> 2026-06-15 | pilot + 对话 B + 对话 C 全量合并 + 对话 D verifier 交叉验证 | 状态：**定稿**
> 覆盖：R002 C 维 22 源全部（C1-C22）
> 条目数：**62 条**（无合并去重，全保留互补）
> 对话 D 变更：① C-102/410/413 推翻 H004 合并判断改为保留互补（verifier 发现 C-413 why_good 依赖"新旧方向对照"证据，物理合并会丢信息）② C-101/507 确认互补（修正草稿 L106 自相矛盾的"合并"标注）③ C-508/509 标注混合形态
> 下游契约：D002 C-rewrite-fewshot 字段
> 跨 repo 消费路径：`/mnt/d/code/study/research-protocol/.sessions/2026-06-14-proposal-log-distillation/distilled/C-rewrite-fewshot.md`

## 字段 schema（FROZEN，见 scan-template.md）

每条 C 维条目含 11 字段：`id / source_ref / source_agent / material_form / date_validity / direction / original_text / rewritten_text / good_example / why_good / fewshot_target`

## 形态分布

C 维 62 条按 material_form 分布：
- **命名方法论 28 条**（句式库/段落模板/章节结构模式，填 good_example）
- **规则清单 16 条**（公式引入/参数解释/术语规范句式集，填 good_example）
- **diff对比 12 条**（前后改写对，填 original_text/rewritten_text）
- **失败案例 6 条**（反例）

> **混合形态标注（对话 D verifier 发现）**：C-508/C-509 标"命名方法论"但实际同时填了 original_text/rewritten_text（diff 形态字段）和 good_example（纯范例形态字段）。agent-C2 自检已说明"主映射是命名方法论范式故统一标"。下游消费方按 material_form 取字段时，这两条需同时读 original/rewritten 和 good_example。

## 分类索引（按 fewshot_target 聚合，便于下游检索）

### 一、公式/符号改写族（公式引入+参数解释+符号消歧）

| ID | fewshot_target | 来源 |
|----|---------------|------|
| C-101 | 句子功能序列重组段落（DEF/FACT/CLAIM/EVAL/TRANS/GAP/NEED/CITE） | R011 |
| C-201 | 动词强度改写（已有模型去"建立"化） | Ch2-reviews |
| C-202 | 论断依据补强（定量数字补推导） | Ch2-reviews |
| C-204 | 公式引入句式规范化（去"写作"改"可表示为"） | Ch2-reviews |
| C-401 | 公式引入三段范式（物理含义句+可表示为+公式） | Ch2 正文 |
| C-402 | 参数解释格式铁律（式中+分别为+单位括注） | Ch2 正文 |
| C-403 | 信号模型建立段四件套（符号+物理含义+约束+澄清） | Ch2 正文 |
| C-404 | 四类数学表达句式模板集 | Ch2-guides |
| C-504 | 公式引入句式骨架（前置处理+限定+可以表示为） | writing-patterns-sentence |
| C-518 | 符号消歧策略库（加下标/换字母/换花体 15 条） | symbol-conventions |
| C-519 | 符号写作 5 建议（每章小表+首次定义+附录闭环） | symbol-conventions |

### 二、综述段改写族（去清单体+先扬后抑+研究空白陈述）

| ID | fewshot_target | 来源 |
|----|---------------|------|
| C-102 | 去清单体（综述段改为先扬后抑） | R011 |
| C-103 | 引用嵌入改写（引用后缀模式，去"文献[X]指出"） | R011 |
| C-104 | 去翻译腔/段落衔接（降衔接词密度改语义承接） | R011 |
| C-205~207 | 贡献声称降级/避免绝对化/结果定位精确化（旧 GNN diff） | R003 |
| C-407 | 贡献声称降级 5 类映射表 | S006 |
| C-410 | 综述收口先扬后抑+空白收口（旧 GNN 范文） | 开题报告 |
| C-411 | 三空白分层+收敛到核心问题漏斗式 | 开题报告 |
| C-413 | FSO 方向综述收口（与 C-410 新旧对照） | thesis-framework |
| C-414 | FSO 三不足"其一/其二/其三"分层 | thesis-framework |
| C-416 | 参数溯源表模板（每数字带来源） | literature_notes |
| C-417 | 综合分析三层结构+空白声称带验证条数 | literature_notes |
| C-420 | 开题第三章方法罗列→问题驱动改写 | R003-kaiti |
| C-421 | 开题已有支撑段防御性写法（说方向不说结论） | R003-kaiti |
| C-508 | 综述段 P3 归纳句先行+分类框架 | S004 |
| C-509 | 综述缺陷段从单篇挑错上升到方法论层面 | S004 |
| C-513 | 文献综述让步转折两层嵌套（先扬后抑论证空白） | material-fso-sentence |
| C-521 | 文献例举段归纳先行+量化展开 | draft-ch1 |
| C-522 | PPT 综述支撑页（一页一主张+逐条溯源+空白箭头） | FINAL_OUTPUT |

### 三、段落衔接/章节结构族

| ID | fewshot_target | 来源 |
|----|---------------|------|
| C-301~304 | 章节命名规范化（标题句式/绪论结构/中间章节/技术子领域） | cnki-survey |
| C-305~306 | 图表叙事改写（研究路线图/关键技术命名） | figure-composition |
| C-405 | 节首铺垫句式+三子节句式分化防雷同 | Ch2-guides |
| C-406 | 术语全称括注+去"我们"+去"所以" | Ch2-guides |
| C-408 | 跨章共享能力去重定位 | S006 |
| C-409 | 多章差异化定位表模板 | S006 |
| C-412 | 可行性分析四段式（理论/方法数据/初步验证/风险应对） | 开题报告 |
| C-415 | FSO 创新点三条分析类措辞（系统分析+交付物） | thesis-framework |
| C-418 | §1.3 总起句三模板（研究定位/问题导向/指标型） | R002-section-1-3 |
| C-419 | 章间递进衔接句五模板 | R002-section-1-3 |
| C-501 | 章引言段两段式（问题驱动+前章回顾+本章预告） | writing-patterns-paragraph |
| C-502 | 节间过渡段三句式（前效→剩余→后需） | writing-patterns-paragraph |
| C-503 | 参数优化段六步法（含 trade-off 与最优值结论） | writing-patterns-paragraph |
| C-505 | 结果段数值嵌入句式（分别为/提升了/降低了） | writing-patterns-sentence |
| C-506 | 范文取材方法论（5 维度打分+定向提取最强项） | writing-patterns-ch2ch3 |
| C-507 | 句间逻辑链 DEF/CLAIM/EVAL/TRANS 标注法 | S004 |
| C-510 | 绪论 1.1 九段功能位模板（挑战与工作一一对应） | S001-annex |
| C-511 | 核心技术章 X.1-X.6 统一段落功能模式 | S001-annex |
| C-512 | 漏斗收束式开篇四步法 | material-fso-sentence |
| C-514 | 衔接词功能速查表（按位置选词） | material-fso-sentence |
| C-515 | 逐节 7 维内容卡片模板 | material-section-content-cards |
| C-516 | 内容卡片约束维叙事关键句（正反对比论证） | material-section-content-cards |
| C-517 | 内容卡片衔接上/衔接下双字段（章节衔接网） | material-section-content-cards |
| C-520 | P# 功能标签逐段自评法 | draft-ch1 |
| C-523 | 分析类创新点 6 维配套表述（框架+准则去"方法"化） | innovation-points |
| C-524 | 宽壳策略（标题宽+内容窄+"拟"字保护+三级退路） | innovation-points |

---

## 条目正文（62 条 yaml，按 id 排序）

> 完整 yaml 内容见各源文件：
> - pilot-agent1.md（C-101~104）
> - pilot-agent2.md（C-201~207）
> - pilot-agent3.md（C-301~306）
> - batchC-agentC1.md（C-401~421）
> - batchC-agentC2.md（C-501~524）
>
> **下游消费方按 id 到对应源文件取 yaml 块**。
>
> **对话 D 合并去重定稿（D004，verifier 交叉验证后）**：
> - **C 维 62 条全部保留，无合并**。3 组语义近邻经 verifier 判定全部互补：
>   - **C-101 vs C-507（句式标注族）**：互补保留。C-101 是 R011 **句子级单标签** 8 类功能体系（DEF/FACT/CLAIM/EVAL/TRANS/GAP/NEED/CITE，每句贴一个功能标签，用于段落内节奏仿写）；C-507 是 S004 **句间逻辑关系链**标注（[然而]/[同时]/[为应对]/[这种]，标注相邻两句逻辑关系，用于整段衔接链构建）。**粒度不同（句内功能 vs 句间关系），用途不同，合并会抹平关键差异**。（注：草稿曾误标"语义高度重叠合并"，verifier 实读 yaml 后推翻）
>   - **C-102 + C-410 + C-413（综述先扬后抑族）**：⚠️ **推翻 H004 合并判断，改为保留互补**。C-102 是 R011 抽象节奏公式（正面成果→让步转折→不足→收束），C-410 是旧 GNN 方向导师通过版完整范文实例，C-413 是 FSO 当前方向范文实例。合并会丢失"新旧方向句式普适性对照验证"证据（C-413 的 why_good 显式依赖"新旧对照"）。保留 3 条，fewshot_target 交叉引用。
>   - **C-402 vs C-518/519（符号参数族）**：互补保留。C-402 是单条公式参数解释写法（式中+分别为+单位括注），C-518 是符号冲突消歧策略库（15 条加下标/换字母映射），C-519 是全文符号管理建议（每章小表+首次定义+附录闭环）。三层正交不重叠。

## 与下游 paper-eval S033 的输入映射

| S033 改写目标 | 输入 C 条目 |
|--------------|------------|
| 公式引入句式规范化 | C-204, C-401, C-404, C-504 |
| 参数解释格式铁律 | C-402, C-403 |
| 符号一致性改写 | C-518, C-519 |
| 去清单体（综述段） | C-102, C-408, C-410, C-413, C-420, C-508, C-509, C-513, C-521 |
| 去翻译腔/段落衔接 | C-104, C-406, C-501, C-502, C-507, C-512, C-514, C-517 |
| 引用嵌入改写 | C-103 |
| 贡献声称降级 | C-205, C-207, C-407, C-408, C-415, C-421, C-523, C-524 |
| 避免绝对化 | C-206, C-421 |
| 研究空白陈述 | C-411, C-414, C-417, C-509 |
| 章节命名规范化 | C-301~304, C-305~306, C-418, C-419, C-510, C-511, C-515 |
| 论断依据补强 | C-202, C-416 |
| 动词强度改写 | C-201 |
| 可行性分析写法 | C-412 |
| 结果段数值嵌入 | C-503, C-505 |
| 综述支撑页改写 | C-522 |
| 模板对齐改写 | C-520 |
| 论证主线改写 | C-516 |

## 已知限制

1. **C 维合并去重已完成（对话 D 定稿）**——3 组语义近邻经 verifier 判定全部互补保留，无合并。句式标注族（C-101/507 粒度不同）、综述先扬后抑族（C-102/410/413 新旧方向对照证据）、符号参数族（C-402/518/519 三层正交）正文均独立，索引段交叉引用。
2. **C-205~207/C-407~409/C-410~412/C-506/C-520~521 标"方法论可继承-技术作废"**——旧方向（GNN/信道均衡）技术内容作废，但写作范例价值不失效，下游消费注意 direction 字段。
3. **R002 C 维全覆盖确认**：C1(R011)=C-101~104, C2(Ch2 diff)=C-201~204, C3(Ch2 正文)=C-401~403, C4(Ch2-guides)=C-404~406, C5(figure-composition)=C-305~306, C6(R003 diff)=C-205~207, C7(S006 降级)=C-407~409, C8(开题报告 GNN)=C-410~412, C9(thesis-framework FSO)=C-413~415, C10(cnki-survey)=C-301~304, C11(literature_notes)=C-416~417, C12(R002-section-1-3)=C-418~419, C13(R003-kaiti)=C-420~421, C14(writing-patterns)=C-501~506, C15(S004)=C-507~509, C16(S001-annex)=C-510~511, C17(material-fso-sentence)=C-512~514, C18(material-section-cards)=C-515~517, C19(symbol-conventions)=C-518~519, C20(draft-ch1)=C-520~521, C21(FINAL_OUTPUT PPT)=C-522, C22(innovation-points v6)=C-523~524。**22 源全覆盖**。
