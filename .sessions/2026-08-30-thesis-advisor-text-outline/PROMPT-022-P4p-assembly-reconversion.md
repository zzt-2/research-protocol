# PROMPT-022: P4' 组装批增量重转——扩容/加密后六章 → BIThesis LaTeX 全量重编译

> 来源: S015 + D027/D037—D043 | 日期: 2026-09-07
> 前提: E1—E5 扩容 + F1/F2 加密 + C 落位/修正全部完成（worktree 9048ab7）；治理编号本批 = S016 / D044 / V033
> 性质: **全量重转而非增量补丁**——md 相对 v1 组装版已增 ~2.4 万字/71 公式实例/14 表/101 引用键，逐处补丁比重转贵且易漏

## 提示词正文（用户粘贴到新对话）

请把学位论文章节稿（扩容+加密后）全量重转进 BIThesis LaTeX 并编译出新版 main.pdf。全程自主推进不中途提问；拿不准的记入"待用户拍板项"。**用户将拿这份 PDF 配合迭代改版式，所以交付质量以"可直接翻阅挑问题"为准**。

**启动时使用 session-governance 报到**，读：`topic-index.md`、最新 S###、`decisions.md` 的 D022—D043（重点 D027 组装裁量先例）、`voice.md`、`.sessions/profile.md`。专题目录：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.sessions\2026-08-30-thesis-advisor-text-outline\`。

**两个目录（角色不同）：**
- 模板与产出（在此工作）：`D:\code\study\research-protocol\毕设\正文\latex\`（v1 组装已在库，含 CONVERSION-SPEC.md 转换规范与已修好的 main.tex——defernumbers 注释/连字符编号导言区/Ch1—6 接线/封面待填占位全部保留）
- 章节稿源（只读，权威文本）：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\毕设\论文\导师讨论稿\章节稿\01—06*.md`

**必读：** `毕设/正文/latex/CONVERSION-SPEC.md`（v1 规范，沿用）+ 本文件"与 v1 的差异"节。

## 任务

1. **逐章重转** md → `chapters/chapter1—6.tex`（覆盖旧版；正文照搬不改；Ch1 点号制→连字符制替换继续适用，含 F2 新增的表 1.1—1.6）。
2. **main.bib 重抽**：从主仓 `毕设/写作材料/references.bib`（238 条，注意 alhabash2001 已补三作者）抽取正文 135 唯一键；DOI 同文双键注释条目若被引只收被引键。
3. **编译**：xelatex→biber→xelatex×2 零 error；产出 main.pdf。**若 main.pdf 被阅读器锁定写不进，用 -jobname=main_v3 出临时版并在交付说明注明**（先例：v1 修复时被锁）。
4. **确定性对账（全过才算完）**：
   - 公式：tex 编号公式环境实例数（含 subequations a/b 展开）= md \tag 实例数 124（Ch2 36/Ch3 33/Ch4 42/Ch5 13）；字面"式（N-M）"引用断链=0（逐章比对 md 引用集）；
   - 表：27 张题注全部成 table 环境，表引用断链=0；
   - 图：22 个占位 figure 环境（placeholder.png）；
   - 引用：\cite 唯一键=135，biber undefined=0；
   - 编号制：PDF 文本层"图 N.N/表 N.N"点号残留=0；
   - 数字抽查：0.8–1.5 dB/0.87/0.12/δ=0.1/13 dB/768 bit 在位。
5. **warning 台账**：Overfull \hbox 逐条定位到文件（v1 为 11 处，本轮公式增多预计上升）；记入交付说明，不修（修复触碰排版/文字，留给用户配合改版式时定）。

## 与 v1 的差异（重点注意）

- **公式量大增**：subequations a/b 组（Ch2 8 组/Ch5 2 组）按规范用 subequations+align；新增式含 `\qquad` 两段式的照搬；长式按 aligned 防溢出（超出边界的记 warning 不改文字）。
- **表 27 张**：宽表（Ch4 切片配置 6 行、Ch2 符号口径 16 行）可能需要 \small 或 tabularx——形态调整允许，单元格内容照搬。
- **引用形态**：`[@a; @b]` → `\cite{a, b}`；Ch5/Ch6 零引用保持。
- **Ch1 图表点号→连字符**：不止旧 5 处，F2 新表 1.1—1.6 与正文引用一并替换。
- **misc/0_symbols.tex**：v1 是 20 项手汇——本轮**先保持不动**（F1 新增了新符号清单在各批日志，符号表更新留独立小批，不在本批范围；记待拍板）。
- 摘要/封面/成果清单/附录：保持 v1 待填占位不动。

## 硬边界

- 正文文字零改动（Ch1 编号字样替换除外）；事实/数字/引用语义不动；计划态保持。
- 修改仅限 `毕设/正文/latex/` 与治理文件；章节稿 md 只读。
- 治理收尾：S016/D044/V033、voice、topic-index；主仓 commit 一次（latex 目录已入库，正常 add）。
- 不宣称定稿——PDF 交付后由用户翻阅配合迭代。

## 交付说明

报告：PDF 路径与页数、对账六项结果、Overfull 台账（按文件分组计数）、与前版（88 页/30 键）的变化摘要、待拍板项（含符号表更新、Ch6 conclusion 排法仍沿用编号章先例）。
