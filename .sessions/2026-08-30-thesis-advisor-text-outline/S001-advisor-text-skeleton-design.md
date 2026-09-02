# [S001] 导师文字版有限样稿设计

> 2026-08-30 | 讨论与任务交接 | active

## 目标

把“交老师看一版无图文字”的模糊想法收缩成独立专题和专用任务书；本轮不生成导师稿正文，只锁定其用途、证据入口、两阶段停机点及需要比较的有限样稿方案。

## 记录

### 用户要解决的不是普通写作问题

导师稿不只是让老师看目录是否顺眼，还要让老师判断：

1. “两个方法章 + 一个 FPGA 工程章”是否足以支撑题目“星地激光通信信号处理关键技术研究”；
2. 第三章和第四章各自的方法强度是否达到硕士学位论文的方法章要求；
3. 第三章载波相位恢复与第四章双偏振解复用是否需要按接收链物理顺序互换；
4. 第五章应做到何种 FPGA 实现深度，才能名副其实地使用“信号处理链”。

因此，成稿不能只给目录，也不能在结构未确认时铺满全文。它需要展示足够的“方法身份与证据密度”，同时把高修改成本部分留空。

### 已有材料入口

- 开题阶段风格与表述：`毕设/开题报告/kaiti-report.md`、`开题报告v2-导师批注.md`、`开题报告v2-带批注提取.md`、`03-研究方案.md`、`material-section-content-cards.md`。
- 写作规范与结构：`毕设/写作质量规范.md`、`毕设/写作材料/section-outline.md`、`subsection-content-outline.md`、`writing-patterns-paragraph.md`、`writing-patterns-sentence.md`。
- 当前论文骨架：`.sessions/2026-07-09-thesis-writing/decisions.md` 的 D074，以及 S026、S028。
- 第三章事实：`projects/simulation/paper/ccisp2026/README.md`、`main.tex` 与 `sections/`。
- 第四章事实：`projects/thesis-fso/thesis-packages/ch4-scaled-unitary-demux/README.md`、`author-material-index.md`、`chapter-blueprint.md`、`fact-matrix.md`、`claim-and-citation-ledger.md`。
- 同行包装尺度：`peer-thesis-method-packaging-audit.md`、`packaging-recipe-library.md`、`thesis-method-spines.md`。

### 有限样稿的两种候选

**方案 A：字面执行。** 第一章至第六章各写第一个二级节，其余二级标题仅占位。优点是形式整齐；缺点是第一章 1.1 往往是背景、重复开题报告，第六章 6.1 往往是全文总结，而当前第五章尚未完成。这两节对导师判断方法强度的帮助有限，还容易制造“已经写定”的假象。

**方案 B：按判断功能抽样。** 先写一页以内的总体说明；第一章只写“本文主要研究内容与章节安排”；第二至第五章写各章引言；第六章仅列标题。第三、第四章引言必须包含问题、baseline、方法动作链、已有证据、主张边界和本章角色；第五章明确使用计划时态。其余二级标题仅写“待结构确认后撰写”。该方案更直接服务导师判断，预计修改成本更低。

本轮不替用户拍板，T001 要求新对话先完成对照分析与精确内容合同，然后以 `WAIT_USER_APPROVAL` 停机。

## 决策引用

- D001：新建；导师文字版采用两阶段门控，当前只授权内容合同，不授权成稿。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

用户在新对话粘贴 T001。新对话完成 Phase A 后必须停止；用户明确选择样稿结构、篇幅和交付路径后，才能进入 Phase B。
