# PROMPT-009: 组装批——章节稿填入 BIThesis LaTeX 模板

> 来源: S005（长跑 R0—R5 完成）+ 用户 2026-09-06 指示 | 日期: 2026-09-06
> 前提: 语言层修复长跑已完成（commit 2e60ac3/a3f4c3e），章节稿为当前最权威版本

## 提示词正文（用户粘贴到新对话）

请把学位论文章节稿组装进 BIThesis LaTeX 模板并编译通过。全程自主推进，不中途提问；拿不准的记入"待用户拍板项"。

**两个目录（角色不同）：**

- 模板与产出（直接在此工作，未入 git，无分支冲突）：
  `D:\code\study\research-protocol\毕设\正文\latex\`（BIThesis master 模板，xelatex→biber→xelatex×2，见 main.tex 头部与 README.md）
- 章节稿源（只读，权威文本）：
  `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\毕设\论文\导师讨论稿\章节稿\01—06*.md`（六章，长跑后最新版）

**启动时必须使用 session-governance 报到**（专题 `.sessions/2026-08-30-thesis-advisor-text-outline/`，读 topic-index、S005 末两节、D022—D026、voice.md、profile.md；该 .sessions 在 worktree 路径下）。

## 任务

1. **逐章转换** md → `chapters/chapter1.tex … chapter6.tex`（新建 chapter3—6）：
   - 正文文字**照搬不改**（章节稿是 12 轮打磨后的权威文本；任何"顺手润色"禁止）。
   - 标题层级：`##`→`\section`、`###`→`\subsection`、`####`→`\subsubsection`；（1）（2）条目保持条目式不升级为标题。
   - 公式：`$$…$$`→`equation`/`align`（长公式按规范 §16 用 aligned 防溢出）；md 中的 `\tag{2-1}` 去掉（编号由 LaTeX 自动生成），正文引用"式（2-1）"保留连字符制（见下）。
   - 图：md 中【图 X 占位】→ `\includegraphics` 占位（figures/ 放 1:1 灰底 PNG 或 draft 模式）+ 题注照搬；**不画图**（图后置，用户已定）。
   - 表：md 表 → 三线表（booktabs），表题照搬。
   - 算法框（算法 3-1/4-1）：转 `algorithm`+`algorithmicx`，步骤文字照搬。
   - 引用：`[@key]` / `[@a; @b]` → `\cite{key}` / `\cite{a, b}`。
2. **编号制统一为连字符制**（D022 已拍板，D023 债务在组装批清偿）：bithesis 支持则用模板设置（查 bithesis.pdf/cls 的 equation/figure/table 编号格式选项）；不支持则导言区自定义 `\renewcommand{\thefigure}{\thechapter-\arabic{figure}}` 等。**Ch1 正文文字中的"图 1.1/表 1.1"字样随之改写为"图 1-1/表 1-1"——这是编号制替换，非内容改动，允许**；除此之外 Ch1（对应 1.1 冻结区）文字零改动。
3. **参考文献（最小动作）**：从 `D:\code\study\research-protocol\毕设\写作材料\references.bib`（141 条）中抽取章节稿实际使用的 40 个键并入 `reference/main.bib`（模板自带的形状记忆聚氨酯示例条目删除）。**缺键登记不编造**——完整文献批由 PROMPT-010 另行执行。
4. **封面/摘要/其他 misc**：`main.tex` 的 title/author/school/supervisor 等用户信息**留占位并在交付说明中列出待填清单**，禁止编造；abstract.tex、misc/1_conclusion.tex（用 06 章）、2_reference.tex 等按模板结构接好；0_symbols.tex 可从各章符号定义整理（只汇总不新增）。
5. **编译验证**：xelatex→biber→xelatex×2，零 error（warning 记录）；产出 main.pdf。逐项检查：六章齐全、图表编号连字符制、式引用零断链（grep 正文"式（"与 equation 计数对账）、\cite 零 undefined（biber log）。
6. **确定性对账**：转换后逐章 grep 抽查关键数字（0.87/0.12/0.8–1.5 dB、9 dB、13 dB、768 bit、256/192/64、τ=0.5/1.0、δ=0.1）与 md 一致；引用键集合 md 与 tex 相同。

## 硬边界

- 正文文字零改动（编号字样替换除外）；事实/数字/引用语义不动；Ch5 计划态保持。
- 不新增参考文献（仅搬运已用键）；不画正式图。
- 修改仅限 `毕设/正文/latex/`（主仓）与治理文件（S005 追加组装记录、topic-index 更新、日志）。

## 运行纪律

- subagent 并发 ≤3；正文转换可按章派 subagent（任务书给"照搬不润色"硬约束），主对话集成与编译。
- 完成后 commit 一次（主仓 latex 目录未入 git，**首次需 git add**；若不希望入库则至少备份 zip——默认 git add 入库）。
- 治理收尾：S005 追加组装记录、topic-index 当前位置更新、清单外裁量记 D###（顺延）、V### 登记；写一份给用户的简短交接（pdf 在哪、待填封面信息清单、待拍板项）。
- 不宣称"定稿"——正文验收门仍是用户朗读，1.1 验收仍未明示通过。
