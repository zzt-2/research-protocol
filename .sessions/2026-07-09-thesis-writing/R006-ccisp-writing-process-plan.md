# [R006] CCISP 2026 会议论文写作流程规划

> 2026-07-10 | 关联：专题 slug 2026-07-09-thesis-writing / 简报 v4 / R002(叙事对标)/R004(BER调研)/R005(初版骨架)/D002(切换降级)/D003(10⁻⁵矛盾)/D004(口径)
> 目的：规划"怎么写"CCISP 2026 会议论文的流程——对标结论 + 写作骨架 + 素材库 + 多对话拆分。**不写正文**，只给写正文的人/AI 一份可执行的蓝图。
> 纪律：守 FR-22（写作准备不跑实验）+ external-output skill（正文写时再过 C1-C10）+ 数字口径标溯源（D004 教训）。
>
> **⚠️ 修订（2026-07-10 续）**：初版只做了外部对标（会议论文体例），**没查已有内部写作规范积累**——被用户纠偏"你有好好看看之前开题报告咋弄的吗？写作规范文档可没少说相关的"。本版补 §0.5「已有写作规范积累引用」，将历史积累的 4 层写作规范接入本流程规划。写正文时**必须先查这些文件**，不能只用本文件的外部对标结论。
>
> **⚠️ 二次修订（2026-07-10 续接 S004，Step 1 重做完成）**：初版 Step 1 的会议论文写法提取只到"体例统计"粒度，没到用户要的"句式骨架"粒度——被纠偏"像 writing-patterns-sentence.md 那样从会议论文逐条提取公式引入/参数解释/数值嵌入/方法对比的句式骨架"。本版补 §0.5 第五层（`writing-patterns-conference.md`，8 篇会议论文 ~80 条骨架）+ §2.4 每节句式映射。**写每节时先查 §2.4 映射到具体条目编号套骨架。**

---

## 0. 一句话定位

星地 FSO 强湍流下，盲载波相位估计（NDA-ML）相对导频估计（DA-ML）的净增益量化与归因——**先按 naive 口径写（强湍流 +1.2~1.9dB），切换方法当鲁棒性补丁进正文，BER 画到能到的最低+标注**。

- **三件等导师定的事**（不阻塞骨架搭建，但阻塞标题/主图/参考文献定稿）：
  1. 10⁻⁵ 底线含义 A/B（D003）→ 决定主图纵轴 + 主卖点成立性
  2. 增益口径主报 fair/naive（D004）→ 决定标题数字 + 表加粗
  3. 主对比文献（简报 §3）→ 决定参考文献核心一条

---

## 0.5 已有写作规范积累引用（写正文前必查）

> 来源：学位论文写作积累（thesis-writing-prep / thesis-writing / advisor-review-revision 三个专题）+ `毕设/写作材料/` 目录。
> 这些是从 6-7 篇同门范文 + 导师批注 + 12 子 agent 文风审查中提炼的**铁律级规范**，远比本文件的外部对标结论更具体、更强制。
> **写正文时每节必查，不能只用本文件 §Step1-2 的对标结论。**

### 第一层：写作质量规范（铁律级，不可违反）

**文件**：`毕设/写作质量规范.md`（730 行，16 节）

写正文前必读，写完每节后用附录 A 快速检查清单逐项打勾。核心：

| 规范节 | 内容 | 对 CCISP 会议论文的适用性 |
|---|---|---|
| §1 范文验证铁律（4 条） | 节首直接切入禁跨节回指 / 符号定义后直接用禁括号节码 / 参数解释"式中/其中"格式 / 符号重用上下文区分 | ✅ 全适用（会议论文更紧凑，回指更不该有） |
| §2 动词强度控制 | 引用现有模型用"介绍"非"建立" / 仿真结果用"表明"非"揭示" / 性能用"较好"非"最优" | ✅ 全适用（过强动词是审查最高频问题） |
| §2.5 AI 痕迹判定（5 类） | 翻译腔/清单体/元叙述/数据堆砌/平行罗列 → 出现即判机器语言 | ✅ 全适用（会议论文审稿人也查 AI 痕迹） |
| §3 措辞禁忌清单 | 禁"首次/填补空白" / 禁破折号 / 禁正文加粗 / 引用放句末句号前 | ✅ 全适用 |
| §3.3 文献综述自洽规则 | 总结段缺口描述不得与前文引用文献贡献矛盾 | ✅ 适用（Intro 的 related work 段） |
| §5 结构规则 | 每段 3-8 句 / 公式密集段每段≤2 公式 / 段落结构不雷同 / 节首直接切入 | ✅ 全适用（会议论文段落更短） |
| §5.5 段内过渡句 | 段尾纯指路句删除 / 禁"下一节将…" / 保留节首总领句 | ✅ 全适用 |
| §7 审查维度 R1-R8 | 语言质量/论断依据/技术常识/术语合规/符号一致/禁忌内容/图表公式/动词强度 | ✅ 全适用（每节写完过 R1-R8） |
| §9 子 agent 建议验证流程 | agent 建议"加 X 让读者更清楚"→ 先 grep 范文库，未命中则拒绝 | ✅ 全适用（防 LLM 加过渡加引用倾向） |
| §12 开题报告特有规则 | 未完成研究用"拟"前缀 / 创新点写含论证链的独立段落非平行编号 | ⚠️ 部分适用（CCISP 已完成研究不用"拟"；贡献表述见下） |
| §13 参考文献质量门槛 | 主引 IEEE Trans 系列 / 低 IF 期刊逐条评估 | ✅ 全适用 |
| §15 不顺句模式库 | 6 类模式（搭配不当/语义断裂/元语言/数值范围/术语句式/体例一致） | ✅ 全适用 |
| §16 公式排版规范 | 长公式用 aligned / 对齐锚点 &= / 续行运算符 &+ | ✅ 全适用 |
| 附录 A 快速检查清单 | 19 项逐项打勾 | ✅ 每节写完必过 |

### 第二层：句级句式库（写每句话时查）

**文件**：`毕设/写作材料/writing-patterns-sentence.md`（1020 行，17 大类 100+ 条骨架）

每条格式：`> 原文摘录` → `**骨架**：[可替换成分]` → `**用法**：场景说明`。从 7 篇同门范文（董凡/夏煜/丁爽/张思齐/惠佳欣/高悦/管路阳）提取。

**CCISP 论文最相关的句式大类**：

| 句式大类 | 编号范围 | 用在哪节 |
|---|---|---|
| §1 公式引入句式（16 条） | 1.1-1.16 | §II System Model（DA-ML/NDA-ML 公式引入） |
| §2 推导衔接句式（12 条） | 2.1-2.12 | §II/§III（公式间衔接） |
| §3 假设/近似引入句式（10 条） | 3.1-3.10 | §II（慢变近似/块衰落假设） |
| §4 参数解释句式（11 条） | 4.1-4.11 | §II（每个公式后的"式中，A为…"） |
| §5 数值嵌入句式（13 条） | 5.1-5.13 | §IV Results（增益数字怎么写进句子） |
| §7 方法对比句式（10 条） | 7.1-7.10 | §IV（DA vs NDA 对比、切换 vs 固定对比） |
| §11 章引言句式（7 条） | 11.1-11.7 | §I Introduction（问题背景→后果→必要性） |
| §12 章小结句式（8 条） | 12.1-12.8 | §V Conclusion |
| §14 递进评价链（11 条） | 14.1-14.11 | §I/§III（方法递进论证 A→局限→B） |
| §15 缺口/不足断言句式（4 条） | 15.1-15.4 | §I Introduction（Gap 声明） |

**贡献条写法**（本文件 §2.3 贡献条表述应参照）：
- 写作质量规范 §12.7 创新点写法：**每条写成含完整论证链的独立段落（问题→方法→效果）**，差异化各条表述结构，禁"针对X拟Y"模板复制多条
- 但会议论文体例（§Step1 对标结论）是散文式 3 句不用 bullet list——**两者结合**：会议用散文式，但每句含论证链（问题→方法→效果数字），不用"针对…提出…"模板复制

### 第三层：段落级模式卡（写每段时查）

**文件**：`毕设/写作材料/writing-patterns-paragraph.md`（1460 行）

含：§0 通用段落类型（章引言/章小结/节引言/节间过渡）+ §1-§4 各章段落类型 + §附录A 量化基准 + §附录B 结构决策表 + §附录C 写作顺序 + §附录D 范文映射。

**CCISP 论文最相关的段落类型**：

| 段落类型 | 文件位置 | 用在哪节 |
|---|---|---|
| §0.1 章引言段 | paragraph.md §0.1 | §I Introduction（背景→问题→本章内容预告） |
| §0.3 节引言段 | paragraph.md §0.3 | 每节开头（1-3 句让读者知道本节讲什么） |
| §0.4 节间过渡段 | paragraph.md §0.4 | 节与节之间（前节效果→剩余问题→后节需求） |
| §1.1 系统模型引入段 | paragraph.md §1.1 | §II System Model（框图→信号流描述） |
| §1.2 信号/信道推导段 | paragraph.md §1.2 | §II（GG 湍流信道推导 + DA/NDA 信号模型） |
| §1.3 概率分布/统计模型段 | paragraph.md §1.3 | §II（GG 分布 PDF 引入） |
| §2.2 算法推导段 | paragraph.md §2.2 | §III Proposed Method（切换判据推导） |
| §2.5 仿真结果分析段 | paragraph.md §2.5 | §IV Results（现象→数字→机理三层结构） |
| §3.4.2 方法对比段 | paragraph.md §3.4.2 | §IV（DA vs NDA 四种对比结构） |
| §3.4.3 参数优化段 | paragraph.md §3.4.3 | §IV（线宽敏感性扫参） |
| §0.2 章小结段 | paragraph.md §0.2 | §V Conclusion（两段式：问题+方法→验证+数字） |

**量化基准**（paragraph.md §附录A，7 篇范文统计）：
- 公式密度：Ch2 均值 3.9/千字，Ch3 均值 4.5/千字 → 会议论文公式密度可对标（但总量少，4-6 页只给 2-3 个核心式）
- 引用密度：Ch2 均值 3.2/千字，Ch3 均值 1.3/千字 → 会议论文 Intro 引用密度高，Method/Results 低
- 空洞占比：应控制 ≤5%

### 第四层：各节详细写作大纲（写每节前查）

**文件**：`毕设/写作材料/section-outline.md` + `subsection-content-outline.md`

每节含：段落数 / 每段功能 / 字数 / 公式数 / 图表数 / 模板来源（哪篇范文哪节）/ 句式编号（查 sentence.md 哪条）。

**CCISP 论文映射**（学位论文章节 → 会议论文章节）：

| 会议论文章节 | 对应学位论文章节 | section-outline 参考节 | 段落模式参考 |
|---|---|---|---|
| §I Introduction | Ch1 绪论 + Ch4 章引言 | section-outline §1.3 + paragraph §0.1 | sentence §11+§15 |
| §II System Model | Ch2 系统模型 | section-outline §2.2+§2.3 | paragraph §1.1+§1.2+§1.3 |
| §III Proposed Method | Ch4 载波同步（算法推导部分） | section-outline §4.2+§4.3 | paragraph §2.2+§3.3 |
| §IV Results | Ch4 仿真对比（§4.6）+ Ch3 仿真验证（§3.5） | section-outline §4.6+§3.5 | paragraph §2.5+§3.4.2 |
| §V Conclusion | Ch 章小结 | section-outline 各章 §X.N | paragraph §0.2 + sentence §12 |

### 第五层：会议论文写法模式库（写英文会议正文时优先查）

**文件**：`毕设/写作材料/writing-patterns-conference.md`（2026-07-10 新建，8 篇 IEEE 会议论文提取，~80 条骨架）

**这是本 CCISP 论文最直接的句式参照**——从 5 篇 FSO 强相关（ICSOS 2025/2019、MWP 2022、OFC 2026、OECC 2025）+ 3 篇检索补充（APCCAS 2022、OECC 2024、ICUMT 2015）会议论文全文逐条提取，格式与第二层句式库完全一致（`> 英文原文 → 骨架 → 用法`）。

**为什么需要单独一份会议版**：第二/三层句式库是从**中文长篇学位论文**（董凡/夏煜等 7 篇范文）提取的，体例跟英文 4-6 页会议论文不同——会议论文贡献是散文不是 bullet list、Conclusion 单段、无"下一节将…"回指、公式少而精、Related work 只 3-5 句。通用句式（公式引入/参数解释/方法对比的骨架）能复用，但**贡献表述、段落过渡、数值嵌入的句式必须从会议论文重新提取**。

**8 大类句式 + 每类写哪节**（详见本文件 §Step2.4 章节写法映射）：

| 会议版大类 | 条数 | 写哪节 |
|---|---|---|
| §1 公式引入句式 | 15 | §II System Model（DA-ML/NDA-ML 公式引入） |
| §2 参数解释句式 | 11 | §II（公式后 where ... denotes/is/represents） |
| §3 数值嵌入句式 | 12 | §IV Results（增益数字怎么嵌进句子） |
| §4 方法对比句式 | 11 | §IV（DA vs NDA / 切换 vs 固定对比） |
| §5 章引言句式 | 10 | §I Introduction（背景→问题→必要性） |
| §6 章小结句式 | 9 | §V Conclusion |
| §7 段落过渡模式 | 11 | 各节内部/节间（无回指衔接） |
| §8 贡献表述模式 | 7 | §I Introduction 末段（散文式带数字） |

**写正文时查文件顺序**：先查第五层（会议版，定体例+句式骨架）→ 通用规则查第一层（写作质量规范，过 R1-R8）→ 段落结构查第三层（段落模式卡，适配到会议短段落）→ 各节大纲查第四层。

### 文献提取规范

**文件**：`毕设/写作材料/literature-notes-ch1-ch2.md` + `material-chapter-literature.md` + `references.bib`

写 related work / 文献综述时：
- 每篇文献提取：核心贡献 + 与本文关系 + 档级（Trans/顶会/低IF）
- 综述段用**递进评价**（§14 递进评价链），不平行罗列（§2.5 清单体禁忌）
- 文献综述自洽规则（写作质量规范 §3.3）：总结段缺口描述不得与前文引用文献贡献矛盾
- 参考文献质量门槛（§13）：主引 Trans 系列，低 IF 逐条评估

**已有的文献提取积累**（`毕设/写作材料/literature-notes-ch1-ch2.md`）：
- Ch1-Ch2 文献已提取（旧方向：信道估计+载波同步），含核心贡献+与本文关系
- CCISP 论文文献清单（本文件 §3.3）应与此对齐，补 FSO 强湍流 + NDA/DA-ML 方向的新文献

### 写作流程方法论（写作质量规范 §11）

逐节循环（每节 5 步）：
1. 派 3 个写作向导子 agent（结构/公式/语言）并行提取指南 → **查上述 4 层文件**
2. 主对话写正文
3. 派 8 个审查子 agent（R1-R8）并行审查
4. 汇总修正
5. 下一节

章级顺序：
1. 先写正文各节（跳过引言和小结）
2. 写章引言（概括+衔接+预告）
3. 写章小结（两段式总结+引出下章）
4. 引言和小结也过 R1-R8

**会议论文适配**：会议论文无"章"概念，但 §I Introduction 最后写、§V Conclusion 最后写的顺序仍然适用（先有正文才能概括）。

---

## Step 1：对标研究——别人怎么写

### 1.1 对标样本来源（三层覆盖）

| 层 | 样本 | 数量 | 覆盖维度 |
|---|---|---|---|
| **会议论文**（本次新增） | ICSOS 2025/2019、MWP 2022、OFC 2026、OECC/PSC 2025（本地全文）+ APCCAS 2022、OECC 2024、ICUMT 2015（检索全文）+ OFC 2025、ICWOC 2025（摘要） | 10 篇 | 章节骨架/图数/贡献表述/参考文献数 |
| **期刊论文**（R002 §B/§C 已有） | Wang 2025 OE / Paillier 2020 JLT / Wang 2024 OE / A 两阶段CPE / E hybrid switching / C format-transparent | 6 篇 | 机制+数字闭环/Complexity收子节/贡献用数字 |
| **学位论文**（R002 主体，仅供量级对标） | 郭欣宇 / 张思齐 | 2 篇 | 量级对标（不再参考叙事体例） |

### 1.2 会议论文体例核心发现（10 篇实证）

**章节骨架**：
- 5 页主流 = **5 节**：I Intro → II System/Setup → III Method/Proposed → IV Results → V Conclusion
- 3 页超短 = **4 节**：Intro → Setup(含 Method) → Results → Conclusion
- 与期刊差异：**无独立 Related Work 节**（并入 Intro）、**无 Discussion 节**、**Conclusion 仅 1 段**
- 理论型会多 1-2 节（ICUMT 6 节含非线性分析），工程型更紧凑（APCCAS 5 子模块塞一节）

**贡献表述**：
- **几乎不用 bullet list**，统一是 Intro 末尾**散文式 3-4 句**，句式 "We propose... It achieves... Additionally..."
- 会议对贡献措辞容忍度高，可直接写性能数字（"18 clock cycles"、"1-MHz range"）
- 期刊（R002 §B）则更硬：用数字立贡献，不写 contributions 列表（除非 Frontiers 体例要求）

**图安排**（页数 ↔ 图数经验公式）：
- 3 页 ≈ 3 图；4 页 ≈ 6-8 图；5 页 ≈ 8-10 图
- **标配组合**：1 张系统/算法框图（Fig.1，必放）+ 机制图（中段）+ BER/星座图（Results 节）
- 表可有可无（3-4 张：资源、对比、参数）

**参考文献**：
- **6-12 篇为主**（3 页 ~10 篇，4 页 ~12 篇，理论型可少到 6 篇）
- 远少于期刊（25-40 篇），允许混引会议+期刊

**会议 vs 期刊写法差异（关键）**：

| 维度 | 会议（4-6 页） | 期刊（8-12 页） |
|---|---|---|
| Related Work | 并入 Intro（3-5 句） | 独立段/章 |
| 公式推导 | 只给 2-3 个核心式 | 完整推导 |
| Discussion | 无（并入 Results 或 Conclusion） | 独立节 |
| Conclusion | 1 段复述贡献+核心数字 | 总结+展望详述 |
| 致谢 | 简短或省 | 标准段 |
| 参考文献 | 6-12 篇 | 25-40 篇 |

**省略技巧**：用 inline 公式、图多占版面替文字、Method 揉进 Setup、Intro 只引最核心 3-5 篇。

### 1.3 期刊论文体例核心发现（R002 §B/§C 已有，6 篇实证）

- **机制+数字闭环**：Method 30-45%，每机制点配 dB/% 量级，机制→数字同节闭环
- **Complexity 收 Results 子节**（不单列章）
- **贡献用数字不用句式**：abstract+intro 亮数字，不写 contributions 列表
- **30seed+CI 不能当"更严谨"卖点**（领域惯例不报 CI，6 篇全不报）→ 用"湍流随机性需多 seed 表征分布"正当化
- **切换型特有 framing**："跨工况可移植性"（跨湍流强度/per-block 有效 SNR 区间）

### 1.4 对标结论——我们该怎么写（会议+期刊混合体例）

CCISP 是 IEEE 会议（4-6 页），但目标是 EI+Scopus 检索，质量要求不低。采用**会议骨架 + 期刊的"机制配数字闭环"纪律**：

1. **5 节骨架**（Intro→Channel Model→Method→Results→Conclusion），无独立 Related Work/Discussion
2. **Method 30-40%**：讲清 DA-ML/NDA-ML 两法 + 切换判据，每点配 dB 数字
3. **贡献用散文式 3 句带数字**（会议体例），放 Intro 末段
4. **Complexity 收 Results 子节**（期刊体例）
5. **图 4-6 张**：1 系统框图 + 1 机制图 + 2-3 BER/增益曲线 + 0-1 可选
6. **参考文献 10-15 篇**
7. **30seed+CI 用"湍流随机性"正当化**，不当主卖点
8. **公式 3-5 个编号式**（信号模型 + DA-ML + NDA-ML升幂 + 净增益定义 + 可选切换判据），辅少量 inline
   - **【已定 2026-07-10，用户拍板】**：① 公式数 3-5 编号式（对标 OECC2025 的 7 式，我们 4-6 页给 3-5 式）② 推导只给最终式不展开推导链（会议论文半推导是主流，完整推导链是期刊做法）③ 编号格式右圆括号 (N) 正文用裸 (N)（8 篇 100% 统一）④ 参数解释 where…denotes 同段（8 篇 100% 统一）
   - 事实依据：子 agent 提取 8 篇会议论文公式用法（对照表见本轮 S004 记录）。短篇(≤150行)全 inline 不编号；≥150行含推导才用编号式。我们是建模+推导+实验型(接近 OECC2025/ICSOS2019)

---

## Step 2：写作骨架

> **📌 叙事包装策略见 R007**（`R007-packaging-strategy.md`，2026-07-10 新建）——导师反馈 4 点后专门做的包装策略。写正文时**先查 R007 定每节讲什么故事（两段式影响分析+方法、切换收窄、弱湍流处理、图表配合）→ 再查本节定句式怎么套**。R006 给骨架，R007 往骨架里填叙事逻辑。R007 的关键更新：Results 内部拆 §IV-A 影响分析 + §IV-B 方法性能两子节（导师第 1 点）、切换只讲 vs 固定盲 +1.3~2.3dB（导师第 3 点）、弱湍流不报归零数字（导师第 3 点）。

### 2.1 章节结构（5 节，按 5 页预算，可压到 4 页）

| 节 | 标题 | 篇幅 | 写什么 | 等导师？ |
|---|---|---|---|---|
| I | Introduction | ~0.8 页 | 星地FSO背景 + 强湍流挑战 + DA/NDA两法 + Gap(导频在deep fade失效) + 贡献3句 | 贡献句等口径定 |
| II | System Model | ~0.8 页 | GG湍流信道(3档) + 16APSK信号模型 + 块结构 + DA-ML/NDA-ML公式 + 公平对照坐标γ_tot | σ²_R核对 |
| III | Proposed Method | ~0.8 页 | 块有效SNR判据 + 切换逻辑 + crossover物理因果 | **整节等导师定切换进不进** |
| IV | Results & Discussion | ~1.8 页 | BER曲线(6场景) + 净增益表(1张) + 切换crossover图 + 线宽敏感性 + Complexity子节 | 纵轴/口径/子图数 + **图表包装策略待专门对话定** |
| V | Conclusion | ~0.3 页 | 贡献重述 + 核心数字 + 未来工作 | — |
| | References | ~0.5 页 | 10-15 篇 | 主对比文献 |

**篇幅弹性**：
- 若切换**降附录**：III 压缩到一段（0.3 页），IV 扩到 2.3 页
- 若切换**不提**：III 删，II 扩到 1.1 页（补两法对比分析），IV 扩到 2.3 页
- 若 4 页版：II+III 合并为 "System Model and Method"（1.2 页），Conclusion 压到 0.2 页

### 2.2 图表清单（4-6 图 + 1 表，Tab.2 已砍）

> **【已定 2026-07-10】**：Tab.2 切换表砍掉并进 Fig.4 机制图。表格总数 2→**1 张**（Tab.1 净增益表）。但 Tab.1 列结构 + Fig.2-4 呈现策略**已由 R007 §4 定**（包装策略，2026-07-10）：
> - Fig.2 画全 6 子图（影响分析核心载体，有湍流 vs 无湍流）
> - Tab.1 只放强湍流/上行 3 行（naive 口径，不报弱湍流归零）
> - Fig.4 crossover 卖点化（只标 vs 固定盲 +1.3~2.3dB，不标 vs 导频负数）
> - 详见 R007 §4.1/§4.2/§4.3

| # | 图/表 | 类型 | 内容 | 数据来源 | 状态 |
|---|---|---|---|---|---|
| Fig.1 | 系统框图 | 框图 | 星地FSO链路(发射→湍流信道→接收) + DA-ML/NDA-ML两估计器位置 + 切换判据位置 | — | ⏳ 待画（design-paper-figures skill） |
| Fig.2 | BER vs SNR 主图 | 数据图 | 6子图(无/弱/中/强/上行中/上行强)，每子图3线(DA/NDA/oracle) + HD-FEC线 | 30seed主实验 + H002补点 | 🟡 有初版 `fig2_ber_ext_merged.png`，需重排 |
| Fig.3 | 净增益 vs 湍流强度 | 数据图 | 横轴=湍流强度(6场景)，纵轴=gain(dB)，双线(naive/fair) + CI带 | `_fair_gain_summary_30seed.json` | ⏳ 待画 |
| Fig.4 | 切换机制图 | 机制图 | crossover：横轴=块有效SNR，纵轴=DA/NDA BER，切换点~12-14dB汇聚 | 主实验数据 | ⏳ 待画（若切换进正文） |
| Fig.5 | 线宽敏感性 | 数据图 | 横轴=线宽(kHz)，纵轴=增益(dB)，证10kHz已在最优区间 | `linewidth_sweep_summary.json` | ⏳ 可选 |
| Tab.1 | 净增益表 | 表 | 强湍流3场景×{naive,CI,测法,BER可达} | D004 表 + summary JSON | 🟡 **列结构已由 R007 §4.2 定**（只放强湍流/上行3行，naive口径，上行强加粗）。数据齐待口径最终定加粗 |
| ~~Tab.2~~ | ~~切换vs固定表~~ | ~~表~~ | ~~4场景×{vs DA,vs NDA,CI}~~ | `_a4_switch_30seed_fixed.json` | ❌ **【已定 2026-07-10 砍】** 并进 Fig.4 机制图（事实依据：8 篇会议论文 5/8 零表格，性能对比倾向用图不用表；切换数据本就适合可视化为 crossover 图） |

> **✅ 表格+图包装策略已定（R007 §4，2026-07-10）**——原"专门开一个对话定"已完成，产出 `R007-packaging-strategy.md`：
> - Fig.2 画全 6 子图（按湍流递增排列，AWGN 当无湍流基准），强湍流子图纵轴收窄不硬凑 1e-5（对齐 Paillier JLT 2020 领域惯例）
> - Tab.1 只放强湍流/上行 3 行（naive +1.26/+1.19/+1.85dB），不报弱湍流归零（导师第 3 点"强调自己行的"）
> - Fig.4 crossover 卖点化（标 vs 固定盲 +1.3~2.3dB，不标 vs 导频负数）
> - 难点"怎么把切换多数场景输/naive弱湍流归零/BER到不了1e-5 包装成故事"已解：两段式（影响分析承担湍流影响 + 方法节只讲强湍流卖点）+ 选择性呈现（导师第 3 点，领域惯例 R002§C 实证 6 篇不报 CI）

**导师图方向**（voice.md S003 导师原话）："系统框图可分两个也可合一个...仿真结果图大概三四个...哪个效果好就用哪个"

**⚠️ 等导师定的图相关项**（R007 已给倾向方案，导师定后终稿）：
- ~~子图数 4(下行) vs 6(含上行)~~——**R007 §4.1 已定画全 6 子图**（影响分析需要"有湍流 vs 无湍流"全档对比）
- 强湍流子图纵轴范围（收窄到 1e-4~1e-1 还是统一 1e-5~1e-1）——**R007 倾向收窄**（对齐 Paillier 只画到 1e-4），等 10⁻⁵ 解读最终确认
- ~~切换图(Fig.4)是否存在~~——**R007 §4.3 已定存在**（crossover 卖点化，切换当鲁棒性补丁进正文）

### 2.3 贡献条表述（防御性写法——导师没定的部分用宽描述）

> **📌 R007 §1.4 已按导师两段式反馈重排贡献句**（影响分析→方法的因果递进两块，2026-07-10）。写正文 Intro 时优先用 R007 §1.4 的两块式版本，本节候选草案作为 fair 口径备选参考。

**写法**：Intro 末段散文式 3 句（会议体例），带数字。口径未定处用宽描述不选死。
**句式参照**：`writing-patterns-sentence.md` §11 章引言句式 + §14 递进评价链 + 写作质量规范 §12.7 创新点写法（含论证链的独立段落，非模板复制）。

**候选草案**（naive 口径版，导师定 fair 后调数字）：

> In this paper, we quantify and attribute the net gain of blind carrier phase estimation (NDA-ML) over pilot-aided estimation (DA-ML) under strong atmospheric turbulence in satellite-to-ground FSO links. Monte Carlo simulations (30 seeds, 95% CI) show that the blind estimator achieves a net gain of +1.2 to +1.9 dB (net of pilot overhead) in strong turbulence and uplink scenarios, where deep fades cause pilot-segment failures while block-wide integration remains robust. Additionally, a block-effective-SNR-based estimator switching scheme is proposed as a robustness complement, ensuring full-operating-region applicability of the blind estimator.

**防御性要点**：
- "net gain of +1.2 to +1.9 dB (net of pilot overhead)" —— naive 口径，括号标明"net of pilot overhead"。若导师定 fair，改为 "+2.4 to +3.1 dB (including pilot power penalty)"
- "robustness complement" —— 切换不称"独立增益卖点"，定位是补丁（D002）
- "ensuring full-operating-region applicability" —— 切换的真实价值（低 SNR 避险）
- **不写** "first to" / "novel" / "outperform"（R002 §B：期刊用数字不用句式；且切换相对 DA 多数场景输，不能写 outperform）

**若切换不进正文的备选**（删第三句，贡献只留两条）：
> ...remains robust; in weak turbulence, the gain is statistically insignificant (+0.1 dB, CI overlapping), honestly acknowledging the scenario-dependent nature of the advantage.

**若需第三条补强**（线宽敏感性）：
> A linewidth sensitivity analysis confirms the gain is robust to laser phase noise at the 10 kHz operating point.

### 2.4 每节怎么写（基于会议论文写法模式库的句式映射）

> 以下把 R006 骨架的 5 节，逐节映射到「会议论文写法模式库」（`writing-patterns-conference.md`）的具体条目编号 + 该节段落组织要点。
> 写每节时：① 查映射到的句式条目套骨架 → ② 段落组织按下方要点 → ③ 写完过第一层写作质量规范 R1-R8。

#### §I Introduction（~0.8 页，3 段）

**段落组织**（3 段，对照 paragraph.md §0.1 章引言段 + 会议体例压缩）：
1. **背景段**：星地 FSO 趋势 → 强湍流挑战（散文，不分小节综述）
2. **Gap 段**：DA/NDA 两法 + 导频在 deep fade 失效（1-2 句 Related work）
3. **贡献段**：散文式 3 句带数字（见 §2.3）

**句式映射**：
- 背景段首句 → `conference.md §5.1`（"The deployment of ... is expanding to support ..., thereby requiring ..."）或 `§5.4`（"FSO has recently emerged as a promising ... However, ... propagation is affected by ..."）或 `§5.5`（"have undergone a revolutionary evolution ... with ... surging from ... to beyond ..."）
- 问题陈述段 → `§5.2`（"However, the [问题]—caused by [原因]—introduces ... This ... leads to ..., severely degrading ..."）
- Related work 极简句（1-2 句）→ `§4.11`（"[方法A] is commonly used in [场景]. [方法A] provides poor ... for [场景B] since ..."）或 `§4.7`（"Unlike the [基线], which [局限], [本方法] also use ... thereby"）
- 贡献段 → `§8.1`（OFC 2026 四步递进 discover→propose→demonstrate→enhances）或 `§8.2`（OECC 2025 "Unlike the prior work, we extend ... Simulations demonstrate ..."）

**禁用**：`§7.5` 结构导航段（"The paper is organized as follows..."）——CCISP 短篇省略。

#### §II System Model（~0.8 页）

**段落组织**（对照 paragraph.md §1.1 系统模型引入段 + §1.2 信号推导段，会议体例压缩到 2-3 段）：
1. **信道模型段**：GG 湍流（3 档）PDF 引入 + σ²_R 参数声明
2. **信号模型段**：16APSK 块结构 + DA-ML/NDA-ML 两公式（公式 1/2 from §3.2）
3. **公平对照坐标段**：γ_tot 定义（公式 3 from §3.2）+ 导频开销 1.25dB 声明

**句式映射**：
- 信号模型公式引入 → `§1.2`（"In the presence of [损伤], the [信号] is modeled as:"）或 `§1.9`（"can be described as"）或 `§1.7`（"the [物理量] can be estimated using the [手段]:"）
- DA-ML 估计公式 → `§1.7`（"For each block, the phase offset can be estimated using the pilot symbol:"）
- NDA-ML 升幂 → `§1.3`（"We can further express the [物理量] in [域] as:"）
- 参数解释（公式后）→ `§2.1`（"where [变量A] denotes ... while [变量C] represents ... [引用]"）或 `§2.5`（带单位密集列举）或 `§2.9`（6+ 符号密集列举）
- 近似假设 → `§2.4`（"The approximation is valid considering that ..."）或 `§2.7`（"where we assume unit gain"）
- 导频开销声明 → `§3.12` 句式变体（"is X dB down ... compared to"）

#### §III Proposed Method（~0.8 页，整节等导师定切换进不进）

**段落组织**（对照 paragraph.md §2.2 算法推导段）：
1. **判据推导段**：块有效 SNR 定义 + 切换逻辑
2. **crossover 物理因果段**：低 SNR 区 DA 赢、高 SNR 区 NDA 赢的机制解释

**句式映射**：
- 判据公式 → `§1.5`（"is obtained by calculating"）或 `§1.1`（"can be approximately derived as"）
- crossover 机制 → `§4.3`（"This advantage arises from exploiting ..."）—— 把切换优势归因到 crossover 机制
- 段内过渡 → `§7.1`（"A residual [问题] still remains ... It is then the role of the [本文模块] to ..."）或 `§7.3`（"Thus, considering the tradeoff between [维度A] and [维度B], we set ...")
- 级联步骤衔接 → `§7.6`（"After [前级处理], we use [算法] to refine ...")

#### §IV Results & Discussion（~1.8 页，最长节）

**段落组织**（对照 paragraph.md §2.5 仿真结果分析段 + §3.4.2 方法对比段 + Complexity 收子节）：
1. **BER 曲线分析段**：6 场景主图，现象→数字→机理三层（照画 BER 不凑 1e-5，R004 做法 a）
2. **净增益表分析段**：Tab.1 两口径并列，naive 主报
3. **切换 vs 固定对比段**：Tab.2 或 Fig.4，诚实标注多数场景不显著
4. **线宽敏感性段**（可选）：Fig.5，证 10kHz 在最优区间
5. **Complexity 子段**（期刊体例收子节）：DA/NDA 计算复杂度对比

**句式映射**：
- BER 曲线引图分析 → `§4.4`（"It can be seen from Fig. X that [方法] performs the best. ... Obviously, [方法] has better [指标A] ..."）—— ⚠️ 注意：本文切换相对 DA 多数场景输/不显著，**不能用 "performs the best / Obviously better"**，改用 `§4.1`（"Compared to the [基线], the [对比方法] exhibits a higher ..."）中性句式或 `§4.8`（"Compared to ... this paper proposed ... more accurately"）
- 净增益数值嵌入 → `§3.3`（"are about 4 dB, 5 dB and 7.5 dB, respectively" 三场景列举）或 `§3.2`（"enhances receiver sensitivity by X dB and enables ... even under ..."）
- HD-FEC 达标点 → `§3.4`（"reaches 7% HD-FEC limit at SNR = X dB"）或 `§3.11`（"can be recovered below X% FEC threshold at ..."）
- 切换 vs 固定对比 → `§4.2`（"... always loses lock during ... while the proposed ... keeps the system locked"）—— ⚠️ 仅限低 SNR 避险场景用此强对比；高 SNR 区用 `§4.9`（"The difference is that ... while ..."）中性差异句
- 不显著场景诚实表述 → `§4.11` 句式变体（"[方法A] provides [中性指标] for [场景] since [原因]"）+ R006 §2.3 防御性写法

#### §V Conclusion（~0.3 页，单段）

**段落组织**（对照 paragraph.md §0.2 章小结段 + 会议体例单段式）：
- 单段：贡献重述（1 句）→ 核心数字（1-2 句）→ 切换定位（1 句，若进正文）→ 未来工作（1 句）

**句式映射**：
- 贡献重述开头 → `§6.2`（"In this paper, we proposed ... The simulation results show that ..."）或 `§6.1`（"We discovered ... and leveraged this correlation to propose ..."）或 `§6.3`（被动语态 "A [方法] was presented ..."）
- 核心数字嵌入 → `§3.7`（"The results demonstrate the possibility to design [方法] with a [指标] ... thereby offering ..."）
- 简化假设声明（10⁻⁵ 达不到）→ `§6.6`（"The whole study was conducted here assuming ... However, ... has been investigated in [ref]."）—— 体现学术审慎
- 未来工作收尾 → `§6.4`（"Future work is underway to ..."）或 `§6.5`（"To the best of our knowledge, no ... has been reported yet."）

---

## Step 3：写作素材库

### 3.1 数字清单（每个数字标来源+口径+验证状态）

> ⚠️ D004 教训：数字口径必须标加减方向。fair_gain = naive + 1.25dB（fair 是大数，naive 是小数）。
> 每个数字标注：来源文件 + 计算口径 + 验证状态（✅ 已核查 / ⚠️ 待核查）

#### A. 净增益数字（主卖点）

| 场景 | naive (dB) | fair (dB) | CI95 (naive) | 测法 | BER可达1e-5? | 来源 | 验证 |
|---|---|---|---|---|---|---|---|
| 无湍流 AWGN | **+0.09** | +1.34 | [1.327,1.352](fair) | HD-FEC单点 | ✅ | `_fair_gain_summary_30seed.json` L11-21 | ✅ D004核查 |
| 弱湍流(下行) | **+0.18** | +1.43 | [1.351,1.505](fair) | 单点 | ✅ | 同上 L22-32 | ✅ |
| 中湍流(下行) | **+0.19** | +1.44 | [1.283,1.596](fair) | 单点(17seed有效) | ✅(46dB刚跨) | 同上 L33-43 | ✅ |
| **强湍流(下行)** | **+1.26** | +2.51 | [2.415,2.603](工作区) | 工作区均值 | ❌(最低2e-4) | 同上 L44-62 | ✅ |
| **强湍流(上行中)** | **+1.19** | +2.44 | [2.343,2.543](工作区) | 工作区均值 | ❌(最低1.6e-4) | 同上 L63-81 | ✅ |
| **强湍流(上行强)** | **+1.85** | +3.10 | [2.989,3.214](工作区) | 工作区均值 | ❌(最低1e-3) | 同上 L82-100 | ✅ |

**口径换算公式**（D004 核查 `fair_comparison.py:109`）：
- `fair_gain = naive + pilot_overhead_db`，其中 `pilot_overhead_db = 10·log10(4/3) = 1.249 dB`
- **加减方向**：fair = naive **+** 1.25（fair 是罚了导频 overhead 的系统总账=大数；naive 是剔掉导频水分的纯性能差=小数）
- naive = fair **−** 1.25

**两种测法**：
- HD-FEC 单点（前 3 场景）：在 BER=3.8×10⁻³ 处测 γ_tot 差
- 工作区均值（后 3 场景）：HD-FEC 物理不可达，取 γ_tot≥15dB 区间逐点 fair_gain 的 grand mean

**⚠️ BER→0 增益坍塌**（D003）：naive gain @ 1e-5 插值 = AWGN +0.2 / weak 0 / moderate −0.3 dB（信息论必然，BER→0 时两法都趋零差错）。**"增益在 1e-5 仍显著为正"无论哪个口径都不成立**。

#### B. 切换方法数字（次卖点/鲁棒性补丁）

| 切换 vs | 场景/SNR | 增益(dB) | CI95 | 显著性 | 来源 | 验证 |
|---|---|---|---|---|---|---|
| **vs 固定NDA** | 强湍流/上行,低SNR(5-15dB) | **+1.3~+2.3** | CI下界全正 | ✅显著 | `_a4_switch_30seed_fixed.json` | ✅ D002/H003 |
| vs 固定NDA | 高SNR区 | ≈0 | — | 持平 | 同上 | ✅ |
| vs 固定DA | 无/弱/中湍流,全段 | **−0.1~−1.2** | CI上界多为负 | ❌切换输 | 同上 | ✅ |
| vs 固定DA | 强湍流高SNR(15-26dB) | +0.02~+0.20 | 仅strong@24显著(+0.20[+0.1,+0.3]) | 多数不显著 | 同上 | ✅ |

**口径**：net 口径（全块 bit，pilot overhead 在 BER 口径内扣 1.249dB）。vs DA 增益必须用 net 口径。
**旧数字禁用**：+0.27~0.48dB（switch_vs_max oracle）已永久禁用（D001 不变量 8）。

#### C. BER 补点数字（主图数据）

| 场景 | 最低BER(补到50dB) | 到1e-5? | 衰减率(/2dB) | 来源 | 验证 |
|---|---|---|---|---|---|
| 无湍流 | 远超(26dB+全零错) | ✅ | ~3× | `_ber_ext_5seed.json` | ✅ H002 |
| 弱湍流 | 远超(40dB全零错) | ✅ | ~3× | 同上 | ✅ |
| 中湍流 | 8.3×10⁻⁶(46dB) | ✅(刚跨) | — | 同上 | ✅ |
| 强湍流(下行) | 2.0×10⁻⁴ | ❌ | ~1.4× | `_ber_ext2_5seed.json` | ✅ |
| 强湍流(上行中) | 1.6×10⁻⁴ | ❌ | ~1.4× | 同上 | ✅ |
| 强湍流(上行强) | 1.0×10⁻³ | ❌ | ~1.4× | 同上 | ✅ |

**deep fade 正确表征**（不变量 5）：BER 斜率变缓（~1.4×/2dB vs 轻湍流 ~3×/2dB），**不是 BER 地板/卡死**。外推 1e-5 需 64-81dB（物理无意义）。

#### D. 线宽敏感性数字

| 线宽 | naive gain(strong) | 来源 | 验证 |
|---|---|---|---|
| 10kHz(工作点) | 在NDA最优区间 | `linewidth_sweep_summary.json` | ✅ R003 |
| 500kHz | 崩溃 −0.82dB | 同上 | ✅ |

**结论**：10kHz 已在 NDA 最优区间，增益非调参花招。

#### E. 仿真参数数字（System Model 节用）

| 参数 | 值 | 来源 | 验证 |
|---|---|---|---|
| 符号率 R_SYM | 2.5 Gsps | `params.py` SystemParams | ✅ |
| 光载波波长 | 1550 nm (C-band) | `params.py` F_CARRIER | ✅ |
| 激光线宽 Δν | 10 kHz | `params.py` LASER_LW (Valjus sat.1553 §4.2) | ✅ |
| 调制 | (8,8)-16APSK | `params.py` / `_b11_params.py` | ✅ |
| 升幂阶数 M₀ | 8 | `_b11_params.py` M0 (B11 行75-77) | ✅ |
| DFT块大小 N_DFT | 256 | `_b11_params.py` N_DFT (B11 行155) | ✅ |
| 块数 N_BLOCKS | 400 | `_b11_params.py` (FR-21 N≥1e5) | ✅ |
| 符号数/点 | 102400 | N_BLOCKS×N_DFT | ✅ |
| 导频间距 | 4 (每4符号1pilot=25% overhead) | `_b11_params.py` DA_PILOT_SPACING | ✅ |
| 导频开销 | 1.249 dB | `10·log10(4/3)` derived | ✅ |
| HD-FEC阈值 | 3.8×10⁻³ | `params.py` HD_FEC_THRESHOLD (B11 行181) | ✅ |
| 蒙特卡洛seed数 | 30 | 主实验 | ✅ |
| GG湍流参数(弱) | α=4.0, β=3.0 | `params.py` TurbulenceParams | ⚠️ source标"典型值"无具体文献 |
| GG湍流参数(中) | α=2.5, β=1.8 | 同上 | ⚠️ 同上 |
| GG湍流参数(强) | α=1.5, β=0.8 | 同上 | ⚠️ 同上 |
| GG湍流参数(上行中) | α=1.2, β=0.9 | `params.py` (参考sat.1553 σ²_R≈0.15) | ⚠️ assumption |
| GG湍流参数(上行强) | α=1.0, β=0.7 | `params.py` (参考sat.1553 σ²_R≈0.25) | ⚠️ assumption |

**⚠️ σ²_R 待核对**（R004 提醒）：我们的湍流强度可能比 Paillier(σ²_I=0.684) 更深。需核对 σ²_R→α/β 映射，避免审稿人质疑工况设定。

### 3.2 公式清单（3-5 个编号式，只给最终式不展开推导链，会议体例）

> **【已定 2026-07-10，用户拍板】**：① 公式数 3-5 编号式（对标 OECC2025 的 7 式，我们给 3-5 式）② **推导只给最终式不展开推导链**（会议主流是半推导，完整推导链是期刊做法）③ 编号格式右圆括号 (N) 正文用裸 (N) ④ 参数解释 where…denotes 同段。
> 事实依据：8 篇会议论文公式用法对照表（S004 记录）。OECC2025（同方向最近样本）= 信号模型(1)起步 + 估计器推导 + where同段解释 + 0表 + 图为主。

#### 公式 1：信号模型（来源 `_recovery.py` 接收信号结构）

> ⏳ 待补——对标 OECC2025 式(1) `r[k]=α[k]e^{jθ}e^{jθ[k]}+n[k]`。我们给 GG 湍流信道下 16APSK 接收信号模型，引入块结构 + DA/NDA 两法共用的信号基础。

#### 公式 2：DA-ML 导频辅助估计（来源 `_recovery.py:136-168`）

给定 pilot 在位置 $n_p$，接收信号 $r(n_p) = s_p \cdot e^{j(\phi + 2\pi \Delta f \cdot n_p T_s)}$。

多 pilot 时用最小二乘（线性回归相位 vs 时间）闭式估 $(\phi, \Delta f)$：

$$\hat{\theta}_p = \angle\left(\frac{r(n_p)}{s_p}\right) \approx \phi + 2\pi \Delta f \cdot n_p T_s$$

$$\hat{\Delta f} = \frac{\text{Cov}(n, \hat{\theta})}{\text{Var}(n) \cdot 2\pi T_s}, \quad \hat{\phi} = \overline{\hat{\theta}} - 2\pi\hat{\Delta f}\cdot\bar{n}\cdot T_s$$

**来源溯源**：Cao 2012 PTL [B11 ref 10] decision-aided pilot-aided ML。代码 `_recovery.py:136`。

#### 公式 3：NDA-ML 盲估计升幂去调制（来源 `_recovery.py:171-185`）

$$r^{M_0} = |r|^{M_0} \cdot e^{j M_0(2\pi\tau k/N + \phi + 2\pi\Delta f \cdot k T_s)} \cdot \text{noise}$$

其中 $M_0 = 8$（(8,8)-16APSK 升 $M_0$ 次幂去调制，$M_0\xi(k)$ 为 $2\pi$ 整数倍→零相位）。升幂后相位是 $k$ 的线性函数 → 单复正弦的频率+相位估计（FFT 找频率 + 线性回归估相位），解卷绕除以 $M_0$。

**来源溯源**：B11 (10.1109/LPT.2024.3523478) 行 75-121 + Wang 2022 T-SP。代码 `_recovery.py:171`。

#### 公式 4：净增益定义（来源 `fair_comparison.py:109` + D004）

$$\text{fair\_gain} = \gamma_{\text{DA}}^{\text{tot}}\big|_{\text{HD-FEC}} + \text{pilot\_overhead} - \gamma_{\text{NDA}}^{\text{tot}}\big|_{\text{HD-FEC}}$$

$$\text{naive\_gain} = \text{fair\_gain} - \text{pilot\_overhead} = \gamma_{\text{DA}}^{d}\big|_{\text{HD-FEC}} - \gamma_{\text{NDA}}^{d}\big|_{\text{HD-FEC}}$$

其中 $\text{pilot\_overhead} = 10\log_{10}(4/3) = 1.249$ dB，$\gamma^d$ = 数据 SNR（BER 曲线轴），$\gamma^{tot}$ = 总发射 SNR（DA 含导频功率开销）。

**加减方向**（D004 核查）：fair = naive **+** 1.25。fair 是系统总账（大数），naive 是纯性能差（小数）。

**来源溯源**：`fair_comparison.py:109` `gain_hdfec = (s_da_d + pilot_overhead_db) - s_nda_d`。

#### 公式 5（可选）：切换判据——块有效 SNR（来源切换逻辑，若切换进正文）

> ⏳ 可选，取决于切换定位（等导师 + 专门包装对话定）。块有效 SNR 定义 + 阈值切换逻辑。对标 OECC2025 的判据式风格。若切换不进正文则砍此式，公式总数降到 4。

### 3.3 文献清单（10-15 篇，标角色+状态）

| # | 角色 | 文献 | venue | 状态 | 本地路径 |
|---|---|---|---|---|---|
| 1 | 方法源头(DA/NDA-ML) | Du et al. "An Optimum Signal Detection..." | JLT 2021 | ✅有 | `papers/doi/10.1109_JLT.2020.3042546/` |
| 2 | 强湍流对照(DPLL异族) | Paillier et al. "Space-Ground Coherent..." | JLT 2020 | ✅有 | `papers/doi/10.1109_JLT.2020.3003561/` |
| 3 | 综述(领域基准) | Valjus et al. "Review and Analysis of DSP..." | IJSCN 2025 | ✅有 | `papers/doi/10.1002_sat.1553/` |
| 4 | 导频功率理论 | Gävert & Eriksson "Estimation of Phase Noise..." | TCOM 2022 | ✅有 | `papers/doi/10.1109/TCOMM.2022.3171809/` |
| 5 | 导频类背景 | Zhou et al. "Efficient Joint CFO and PN..." | JLT 2013 | ✅有 | `papers/doi/10.1109/JLT.2013.2257688/` |
| 6 | 同族盲(V&V) | Viterbi & Viterbi | IEEE TIT 1983 | ✅有(经典) | — |
| 7 | 同族盲(BPS) | Blind Phase Search | 2009 | ✅有(经典) | — |
| 8 | B11锚方法 | Cao et al. (16APSK NDA-ML) | PTL 2024(?) | ✅有 | `_b11_params.py` ref |
| 9 | 强湍流BER+outage | IEEE TCOMM 2020 | TCOM 2020 | ✅R004引 | DOI 10.1109/TCOMM.2020.3008459 |
| 10 | BER floor立项 | Opt. Express 2026 | OE 2026 | ✅R004引 | DOI 10.1364/oe.596556 |
| 11 | OFC 2026(FOE相邻) | "Digital Estimation of Doppler..." | OFC 2026 | ✅有 | `papers/doi/10.1364_ofc.2026.w2a.62/` |
| 12 | OECC/PSC 2025(MAP CPE) | "MAP Phase Recovery..." | OECC 2025 | ✅有 | `papers/doi/10.23919_oecc-psc62146.2025.11109607/` |
| 13 | ICSOS 2019(AO+DPLL) | Paillier et al. ICSOS 2019 | ICSOS 2019 | ✅有 | `papers/doi/10.1109_icsos45490.2019.8978983/` |
| 14 | 强湍流BER+outage(TVT) | IEEE TVT 2024 | TVT 2024 | ✅R004引 | DOI 10.1109/TVT.2024.3399408 |
| **15** | **⏳主对比方法** | **待导师指定** | — | **⏳缺** | R005 补搜候选 L009/L010 |

**缺口**：主对比方法文献（星地FSO场景+近年+导频辅助CPR+可复现）。R005 已补搜 4 候选（L009 JLT 2024 / L010 OE 2024 最契合），但 abstract 级未深核实。**等导师定"主对比要什么类型"再深核实**。

### 3.4 领域惯例参考（R004 调研结论，写 Discussion/Limitations 用）

- **强湍流 BER 降不到 1e-5 是领域已知现象**（Paillier JLT 2020 σ²_I=0.684 也只画到 1e-4）
- **pre-FEC 通行基准是 1e-3**（sat.1553）/ 1e-4（Paillier），1e-5 = post-FEC 工作门槛
- **导师原话"在有编译码的情况下，10⁻⁵ 是底线"** → "有编译码"指向 post-FEC（R004 证据支撑解读 B）
- **呈现做法对齐**：照画 BER 不凑 1e-5（Paillier）+ 锚定 1e-3 工作点（sat.1553）

---

## Step 4：多对话拆分建议

### 4.1 拆分原则

- 每对话 ≤3 步（AGENTS.md 单对话步骤上限）
- 写正文时必过 external-output skill C1-C10
- 等导师的 3 项不阻塞前期写作（Intro 背景/System Model/图初版可先做）
- 中文草稿→英文翻译分对话

### 4.2 对话拆分方案（5 个对话，含等导师节点）

| 对话 | 任务 | 输入 | 产出 | 等导师？ |
|---|---|---|---|---|
| **D1: 图表制作** | 画 Fig.1 系统框图 + 重排 Fig.2 BER主图 + 画 Fig.3 净增益图 + Fig.4 机制图 | 本文档图表清单 + 数据文件 | 4 张图初版（PNG） | 否（可并行） |
| **D2: 中文草稿上** | 写 Intro + System Model | 本文档骨架 §2.1 + 素材库 §3 | §I + §II 中文草稿 | 否 |
| **⏧ 等导师节点** | 问导师 3 件事：10⁻⁵含义 / 口径 / 主对比文献 | 简报 v4 + R004 定心丸 | 导师反馈 | **是** |
| **D3: 中文草稿下** | 写 Method + Results + Conclusion（用导师反馈定口径/纵轴/切换定位） | D2 产出 + 导师反馈 + 素材库 | §III + §IV + §V 中文草稿 + 填 Tab.1 | **是**（导师反馈后） |
| **D4: 过 C1-C10 + 英文翻译** | 中文定稿过 external-output skill 审查 → 翻英文 | D2+D3 中文全稿 | 英文终稿 | 否 |
| **D5: 排版+终审** | IEEE 模板排版 + 参考文献 IEEE 格式 + 终审 | D4 英文终稿 | 投稿包 | 否 |

### 4.3 关键路径与并行

```
D1(图表) ──────────────────────────────┐
D2(Intro+SysModel) ────────────────────┤
                                        ├──⏧等导师──→ D3(Method+Results+Conclusion)──→ D4(审查+翻译)──→ D5(排版)
简报v4 + R004(带去问导师) ──→ 导师反馈 ─┘
```

- D1 和 D2 可**并行**（图表和文字独立）
- D3 必须等导师反馈（口径/纵轴/切换定位决定 Method 和 Results 怎么写）
- D3 是最长对话（写 3 节），若超 3 步可拆 D3a(Method) + D3b(Results+Conclusion)

### 4.4 每对话的 handoff 要点

- **D1→D3**：图的纵轴范围和线条标注等 D3 定（导师反馈后）
- **D2→D3**：Intro 贡献句的口径占位符等 D3 填
- **D3→D4**：中文全稿 + 导师反馈记录 + 素材库数字溯源
- **D4→D5**：英文终稿 + C1-C10 审查记录

---

## 5. 风险与预案

| 风险 | 概率 | 影响 | 预案 |
|---|---|---|---|
| 导师=解读A(10⁻⁵要增益) | 中 | 主卖点绝症 | 转"工作范围鲁棒性"叙事，但需导师认可；预案见 D003 |
| 切换降级后卖点不够 CCISP | 中 | 投稿被拒 | 主卖点维持净增益量化归因(不依赖切换)；切换当鲁棒性补丁补全方案完整性 |
| 主对比文献找不到 | 中 | 参考文献核心缺 | R005 已补搜 4 候选(L009/L010最契)；请导师指 |
| σ²_R 工况被质疑 | 低 | System Model 被审稿人问 | R004 提醒核对 σ²_R→α/β 映射；§II 标注参数来源 |
| 7/20 截稿剩 10 天 | 高 | 时间紧 | D1+D2 并行先跑，等导师同时做图和写背景 |
| 口径搞反（D004 第3次） | 中 | 数字错误 | 素材库 §3.1 已标加减方向+来源代码行；写时必查 `fair_comparison.py:109` |

---

## 6. 等 vs 不等导师清单（更新 R005 §3）

### 必须等导师（3 项，卡标题/主图/主对比）

1. **10⁻⁵ 底线含义 A/B** → 决定主图纵轴 + 主卖点成立性 + Discussion 怎么写
2. **口径主报 fair/naive** → 决定标题数字 + Tab.1 加粗 + 贡献句数字
3. **主对比文献** → 决定参考文献核心一条 + Intro 对比方法描述

### 不等导师，现在/并行能做

1. ✅ 本流程规划文档（本文件）
2. ⏳ 系统框图初版（Fig.1，design-paper-figures skill）
3. ⏳ BER 主图重排（Fig.2，数据齐）
4. ⏳ 净增益图画初版（Fig.3，两口径都画，导师定后选）
5. ⏳ 中文草稿 Intro 背景 + System Model（D2，不涉及口径的段落）
6. ⏳ 素材库数字溯源核查（本文件 §3.1 已做，写时复用）

---

## 7. 与 R005 初版骨架的差异

R005 是初版骨架（7/10 上午写），本文件 R006 是基于对标研究后的修正版：

| 维度 | R005 初版 | R006 修正版 | 修正依据 |
|---|---|---|---|
| 章节数 | 6 节(含独立 Discussion) | **5 节**(Discussion 并入 Results/Conclusion) | 会议体例(10篇实证) |
| 贡献表述 | 列表式 2-3 条 | **散文式 3 句带数字** | 会议体例(Intro末段散文) |
| 图数 | 5 图(含线宽可选) | **4-6 图**(含机制图可选) | 会议3页≈3图/4页≈6-8图经验式 |
| 参考文献 | 15-20 条 | **10-15 条** | 会议体例(6-12篇为主) |
| 公式 | 未明确数量 | **只给核心 2-3 个** | 会议体例(只给关键式) |
| 素材库 | 无 | **完整数字/公式/文献清单+溯源** | D004教训(口径标加减方向) |
| 多对话拆分 | 5 步执行顺序 | **5 对话+并行+等导师节点** | AGENTS.md 3步上限+关键路径 |

---

## 对决策的影响

- **不新建 D###**：本文件是写作流程规划（R### research note），不改方向/架构决策。所有数字口径来自已核查的 D004，骨架基于已确认的 R005+对标研究。
- **范围确认**：本文件在专题 scope 内（写作准备，不跑实验，不写正式正文）。会议论文结构规划是"写作准备"的合理延伸（topic-index 不变量 2："写作专题定位=GW阶段写作准备辅助"）。
- **后续**：D1(图表)+D2(Intro+SysModel) 可立即启动（不等导师）；D3 等导师反馈。
