# PROMPT-001: B 批执行（含 subagent 编排）+ 审查对话备用

> 来源: S005（D017 后编排确认）| 用途: 用户开新对话粘贴执行；审查段为本对话失效时的备用
> 日期: 2026-09-03

## 一、B 批执行提示词（粘贴到新对话）

请执行以下任务书：

D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.sessions\2026-08-30-thesis-advisor-text-outline\T003-harmonization-batch.md

实际工作目录是：

D:\code\study\research-protocol\.worktrees\rdl-method-production-v2

启动时必须使用 session-governance 报到（读 topic-index、S005 全部执行记录节、decisions.md 的 D009—D017、voice.md、.sessions/profile.md）。正文修订使用 paper-writing。

**开题写作规范（用户开题期沉淀，强制读）**：
1. `毕设/写作质量规范.md`——至少读 §1 范文验证铁律、§2 动词强度控制、§3 措辞禁忌、§7 审查维度、§8 反复犯错预防、§9 子 agent 建议验证流程、§10 跨章一致性；
2. `毕设/写作材料/writing-patterns-sentence.md` §6（条件分析/图表引用句式）与 `毕设/写作材料/writing-patterns-paragraph.md` §1（Ch2 系统模型段落类型）——B 批涉及表 2.1 与图 2.2 描述段。
3. **旧路线隔离警告**：上述规范成文于开题期，其中章节对象映射（Ch3 信道估计主线、Ch4 VV/BPS 载波同步等）是旧规划——只复用句式、段落模式与质量规则本身；NMSE 主线、VV/BPS/DPLL 对比、联合 BER、四层挑战链等旧路线内容不得回流正文。

本轮只做 B 批（第二章）：
1. 表 2.1 五列宽表收窄为三列（处理模块｜主要输入｜主要输出），默认按 D012 先例"不删，收窄"，若收窄后信息增量过低再停下提删除建议；"前端校正与符号定时"行删（2.2.2 已声明不讨论该环节）；
2. "论文章节"映射信息全节只保留一处（优先 2.2.3 正文段，图 2.2 描述段末句删除，见 T003 §B1/§D4）；
3. 同步修订图表与公式合同中表 2.1 语义行，记 D###（当前最大号 D017，顺延）。

**subagent 编排（用户指定模式）**：
- 并发上限 3（AGENTS.md）；修改本体由主对话完成（B 批改面小）；subagent 用于改前证据扫描（三处重复信息定位）与改后独立复查（四个对齐逐条 + 规范违例 grep + 通读第二章）——生成与审查分离；
- 任何 subagent 评分/检查表不得替代用户朗读验收，禁止宣称"已顺"。

做完停下：确定性复查（引用键不变、无新增数字/事实、Ch5 计划态、旧路线零回流）→ 治理落盘（S005 追加执行记录、新 D###、topic-index 更新）→ 一次 commit → 报告改动了什么，等用户带回主对话审查。不要顺手进入 C 批，不得动第一章。

## 二、审查对话备用提示词（主对话失效时用；否则直接回主对话说"B 批跑完了"）

工作目录：D:\code\study\research-protocol\.worktrees\rdl-method-production-v2

你是 B 批产物的独立审查者（生成与审查分离）。启动用 session-governance 报到：读 topic-index、decisions.md 的 D012—D017、S005 的 B 批执行记录、T003 §B 批定义。

审查对象：`毕设/论文/导师讨论稿/章节稿/02-系统与信道模型.md` 最近一次 B 批 commit 的改动（git log/diff 自查）。

审查维度：
1. 四个对齐逐条（位置职责唯一/粒度贴位置/形式贴同门惯例/语言自然）；
2. 开题规范违例（`毕设/写作质量规范.md` §2 动词强度、§3 措辞禁忌、§7 审查维度；writing-patterns 句式对照）；
3. 事实未动（引用键集合、数字、Ch5 计划态、旧路线零回流——确定性 grep）；
4. 与第一章新形态（D015/D016 后）的衔接一致性。

产出：逐条 PASS/问题清单（引用行号），登记 verifications.md（V###），只诊断不改稿；问题清单交用户拍板。禁止用检查表宣称"顺"。
