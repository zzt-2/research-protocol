# Task Brief: 导师文字版结构与方法强度请示

> 来源：S001 / D001
> 工作区：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> 当前授权：仅 Phase A；完成后必须输出 `WAIT_USER_APPROVAL` 并停机
> 预期成稿位置（Phase B 才可创建）：`毕设/论文/导师讨论稿/论文整体思路与章节内容说明.md`

## 0. 任务目的

为硕士论文《星地激光通信信号处理关键技术研究》设计一份交导师预审的无图文字版。它不是论文正文初稿，而是一份低修改成本的“结构 + 有限样稿”，用于请导师判断：

1. “两个方法章 + 一个 FPGA 工程章”的总体结构是否合适；
2. 第三章、第四章的方法强度是否足以分别承担硕士论文的方法章；
3. 第三章与第四章是否应按接收机物理处理顺序互换；
4. 第五章需要怎样的 FPGA 实现深度，才能使用“接收端信号处理链”的章名。

用户明确要求：参考开题时期已有材料；不要直接全篇生成；先讨论并锁定内容合同。

## 1. 必须使用的 Skill 与专题纪律

开始时完整读取并遵守：

- `session-governance`：接收本专题，核对 `topic-index.md`、D001、S001、`voice.md`，后续若写 `.sessions/` 文件按其规范更新；
- `paper-writing`：当前处于 PROPOSE，不得越过内容合同进入 DRAFT；
- `external-output`：目标读者是导师，文字要让导师快速作判断，不把内部流程语言和治理术语带出去。

这不是研究方向执行任务。不要调用 `research-direction-lab` 或 `sim-preflight` 去恢复任何实验、检索或 Groundwork。

## 2. 必读材料（按顺序）

### A. 当前专题与章节基线

1. `.sessions/2026-08-30-thesis-advisor-text-outline/topic-index.md`
2. `.sessions/2026-08-30-thesis-advisor-text-outline/S001-advisor-text-skeleton-design.md`
3. `.sessions/2026-08-30-thesis-advisor-text-outline/decisions.md` 的 D001
4. `.sessions/2026-08-30-thesis-advisor-text-outline/voice.md`
5. `.sessions/2026-07-09-thesis-writing/decisions.md` 的 D074
6. `.sessions/2026-07-09-thesis-writing/S026-thesis-title-story-fit-and-ccisp-acceptance.md`
7. `.sessions/2026-07-09-thesis-writing/S028-three-lane-strategic-research-controller.md`

### B. 开题时期的命名和行文风格

8. `毕设/开题报告/kaiti-report.md`
9. `毕设/开题报告/开题报告v2-导师批注.md`
10. `毕设/开题报告/开题报告v2-带批注提取.md`
11. `毕设/开题报告/03-研究方案.md`
12. `毕设/开题报告/material-section-content-cards.md`
13. `毕设/写作质量规范.md`
14. `毕设/写作材料/section-outline.md`
15. `毕设/写作材料/subsection-content-outline.md`
16. `毕设/写作材料/writing-patterns-paragraph.md`
17. `毕设/写作材料/writing-patterns-sentence.md`

读取这些材料的目的不是照抄开题报告，而是提取：标题长度、二级标题节奏、段落密度、导师曾批评的写法、用户习惯的专业程度。

### C. 方法与证据事实

第三章：

18. `projects/simulation/paper/ccisp2026/README.md`
19. `projects/simulation/paper/ccisp2026/main.tex`
20. `projects/simulation/paper/ccisp2026/sections/` 下与方法、结果和结论有关的文件

第四章：

21. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/README.md`
22. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/author-material-index.md`
23. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/chapter-blueprint.md`
24. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/fact-matrix.md`
25. `projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/claim-and-citation-ledger.md`

同行硕士包装尺度：

26. `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md`
27. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
28. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`

## 3. 冻结事实与措辞边界

一级章名以 D074 为基线：

1. 第一章 绪论
2. 第二章 星地激光通信系统与信道模型
3. 第三章 基于接收功率感知的自适应载波相位恢复方法
4. 第四章 基于结构约束的短导频双偏振解复用方法
5. 第五章 接收端信号处理链的FPGA设计与实现
6. 第六章 总结与展望

同时遵守：

- 第三章方法已经 CCISP 录用；CCISP 是会议名，不是方法名，不写“CCISP 方法”。
- 第四章已有正式作者材料包，但不要把其主张扩大为 SOTA、全面领先或击败所有强邻居。
- 第三章和第四章尚未完成端到端联合验证，不得这样暗示。
- 物理处理顺序是双偏振解复用后再做每偏振载波相位恢复；章序是否互换要请导师判断，不得自行改章名顺序。
- 第五章尚未执行，只能写“拟开展、计划实现、预期验证”。若最终只有独立算法模块，没有真实级联链，应提示章名回退为“接收端关键算法的FPGA设计与实现”。
- 对外稿要诚实、克制、专业；不隐瞒已知关键事实，也不把内部最严苛的否决清单整套搬给导师、主动削弱表达。

## 4. Phase A：本轮唯一授权工作

只做分析与内容合同，不创建 `毕设/论文/导师讨论稿/`，不写任何可冒充成稿的完整章节段落。

### A1. 先给 findings，不先给结论

用简洁表格归纳：

- 开题材料体现的标题与行文风格；
- 导师批注中需要延续或避免的写法；
- Ch3、Ch4 各自能让导师判断“方法强度”的最小事实；
- Ch5 当前只能承诺到什么程度；
- 当前章序与物理链路顺序的关系。

每项给文件证据指针，不进行网络检索。

### A2. 比较两种有限样稿

必须比较而不是直接选择：

- **方案 A：逐章第一节。** 第一至第六章各写第一个二级节，其余二级标题只占位。
- **方案 B：功能样稿。** 一页以内总体说明；第一章只写“本文主要研究内容与章节安排”；第二至第五章写各章引言；第六章只列标题。其余二级标题只占位。

比较维度：导师能否判断方法强度、是否重复开题报告、是否制造 Ch5 已完成假象、后续改章序/改定位的返工量、整体看起来是否专业完整。给出明确推荐，但不得代替用户批准。

### A3. 给出精确内容合同

输出以下内容：

1. 建议的完整一级、二级标题目录；暂不展开三级标题。
2. 每个二级节标记为：`本轮写` / `仅列标题` / `暂不出现`。
3. 对每个“本轮写”的部分，给 3–6 条内容卡，不写完整段落。
4. 为 Ch3、Ch4 的章节引言各列一份“方法强度展示合同”，至少包括：问题与场景、经典 baseline、receiver-visible 输入—动作—输出链、已有公平对比证据、方法独立性、claim ceiling、该章在论文主线中的角色。
5. 给出整体篇幅预算。建议区间可从 3000–5000 中文字、约 4–6 页起评估，但必须根据既有开题风格修正。
6. 给出将要明确问导师的 4 个问题，措辞应短、可直接回答，不让导师替我们做资料整理。
7. 指明哪些数字值得在无图稿中保留，哪些应留到图表版；不得为了“显得强”篡改、挑选或新跑数字。

### A4. 强制停机

完成 A1–A3 后：

- 汇报推荐方案、预计成稿长度、拟写节和四个导师问题；
- 最后一行单独输出：`WAIT_USER_APPROVAL`；
- 停止，不创建成稿文件，不继续 Phase B。

## 5. Phase B：只有用户明确批准后才能执行

若用户明确批准 Phase A 的内容合同，才允许：

1. 创建 `毕设/论文/导师讨论稿/论文整体思路与章节内容说明.md`；
2. 只撰写合同中标记为“本轮写”的部分；
3. 其余保留的二级标题下统一写 `（待结构确认后撰写）`，不生成半成品段落；
4. 不插图，不补文献，不跑实验，不改论文正文；
5. 对第五章全程使用计划时态；
6. 完成后按 `external-output` 做一次面向导师的出门审查，再汇报具体文件与仍待导师判断事项。

## 6. 禁止事项

- 不运行仿真、实验或绘图脚本。
- 不搜索、下载或补充论文。
- 不新建候选，不补 P01/P11 Groundwork，不恢复方法生产。
- 不修改 Skill、controller、仿真代码、CCISP 论文或学位论文正文。
- 不生成完整六章正文，不因为读到材料充分就越过 Phase A。
- 不把流程合规、材料数量或会议录用本身当成方法强度的唯一依据。
- 不自动提交 git。

## 7. Phase A 回报格式

1. 事实与证据
2. 方案 A / B 对比
3. 推荐的一级—二级目录及写作状态
4. Ch3 / Ch4 方法强度展示合同
5. 篇幅与数字使用合同
6. 给导师的四个问题
7. 需要用户拍板的事项
8. `WAIT_USER_APPROVAL`
