# CCISP 2026 首轮问题清单

> 工程范围：第一轮可编译投稿骨架的引用与版面问题跟踪
> 审计日期：2026-07-13
> 规则：未完成核验的引用不进入 `references.bib`；本清单不替正文拍板，不替代导师或会议最终口径。

## 状态定义

| 类别 | 含义 |
|---|---|
| **BLOCKING** | 影响正文语义、正式引用或投稿合规；未解除前不能作为最终投稿稿处理。 |
| **DRAFT DEBT** | 首轮骨架可以暂留，但定稿或视觉验收前必须处理。 |
| **INFO** | 已记录的事实或证据，不表示问题已经解决，也不要求本轮改正文。 |

## 当前工作树快照（2026-07-14，覆盖旧版构建快照）

- 当前 `sections/*.tex` 是 `CCE-CC-002` 扩展预览，不是 W001–W003 的逐字抽取版；W001–W003 本轮保持只读。
- fresh build：`latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`，exit 0；`main.pdf` 为 7 页、Letter、双栏，构建时间为 2026-07-14 15:34（Asia/Shanghai）。
- `main.log` 未检出 LaTeX error、undefined citation/reference 或 overfull box；有 1 个 `Underfull \\hbox`（log 第 337 行）。`pdffonts` 显示字体均嵌入。
- `texcount -inc -sum=1 sections/*.tex`：纯 text 3,241 词、headers 42、captions/其他 222、displayed equations 8、floats 5；把 headers 和 captions/其他相加后为 3,505，不能把该总口径写成纯正文词数。
- 当前正文引用 7 个 BibTeX key，均在 `references.bib` 中存在；这是当前扩展预览的引用解析状态，不代表旧骨架的历史 unresolved 债务已完成治理。
- 当前工作树实际嵌入 `fig1_system_model_v5.pdf` 与 `fig2_adaptive_cpr.pdf`，另有三张既有数据图；这与首轮“Fig.1/Fig.2 只放占位框”的原始硬边界不一致，列为当前阻塞项。
- 逐页 PNG 检查未见裁切、重叠或公式越界；第 6–7 页有明显 float 留白，暂不通过排版手段回收页数。

## 本轮新增/更新阻塞项

| ID | 状态 | 问题 | 证据与当前处理 | 解除条件 |
|---|---|---|---|---|
| B-08 | BLOCKING | 当前工作树是 CCE 扩展预览，实际使用 Fig.1/Fig.2，而不是原 CCISP 首轮要求的显式占位框；标题/作者也已从 DRAFT 占位改成工作标题/匿名提交。 | `sections/system_model.tex:5`、`sections/method.tex:8` 直接 `includegraphics`；`main.tex:13-15` 使用工作标题和 `Anonymous Submission`。本轮不回滚这些已有未提交改动，只把偏离显式暴露。 | 明确选择“保留 CCE 扩展预览并允许实际 Fig.1/Fig.2”，或恢复首轮骨架的占位框/DRAFT 元数据；完成独立视觉验收后才可解除。 |
| B-09 | PARTIAL | CCE-CC-002 的 3,500 词验收口径尚未闭合。 | fresh `texcount` 纯 text 为 3,241；含 headers 与 captions/其他为 3,505；R002/V001 的计划值约 3,570。当前不能把 3,505 报成纯正文词数，也不能用图注/标题冒充正文增量。 | 明确 D001 采用的词数口径，并按该口径补足或接受当前正文；不得靠浮动图、参考文献或留白补足。 |

## 当前独立验证结论（V003）

| Gate | 结论 | 证据 |
|---|---|---|
| 构建/源新鲜度 | PASS | fresh `latexmk` exit 0；`main.pdf` 7 页且 PNG 晚于 PDF。 |
| PDF/字体/可读性 | PASS | Letter、双栏、字体全部嵌入；7 页逐页未见裁切或重叠。 |
| LaTeX warnings | PARTIAL | error/undefined/overfull 为 0；`main.log:337` 有 1 个 Underfull，badness 3158。 |
| 数字/公式/引用 | PARTIAL | D004/V003 关键口径一致，7 个 cite key 闭合；全部代表数字的逐项 source/data/code 溯源仍未写入当前稿。 |
| Fig.1/Fig.2 首轮边界 | BLOCKED | 当前为实际图，不是原专题要求的显式占位框。 |
| external-output C1–C10 | PARTIAL | C1/C5/C6/C7/C8/C9 PASS；C2/C3/C4/C10 PARTIAL，涉及 `DA-ML/NDA-ML/oracle`、缩写首次展开和数字溯源。 |
| 总 gate | BLOCKED | 当前是可编译 7 页扩展预览，不是可称最终投稿稿的版本。 |

## BLOCKING

| ID | 状态 | 问题 | 证据与当前处理 | 解除条件 |
|---|---|---|---|---|
| B-01 | PARTIAL | W002 §III 源文档仍同时把 `gamma_th` 写成 BER 曲线 crossover 和固定 effective-SNR threshold。 | `W002-method-results.md:24` 将 `gamma_th` 定义为曲线交点；`:28` 又写成 fixed effective-SNR value。`decisions.md:D008`（约 `:260-275`）明确选择固定 effective-SNR 阈值，并排除 measured crossover/per-regime calibration。目标 LaTeX 已按 D008 做最小分离：`gamma_th` 是固定切换阈值，crossover 只作为观测现象描述。 | 上游 W002 与最终口径仍需在定稿前统一；当前骨架不再让两种说法共用同一符号语义。 |
| B-02 | OPEN | 正文 crossover 数字与重画图的统一插值数字冲突。 | W002 §IV-A（约 `:38-40`）仍为 `17.9/16.8/10.7 dB`；R018（`:155`, `:178`）记录可复现插值值 `18.013/16.866/10.703 dB`，显示为 `about 18.0/16.9/10.7 dB`。 | 明确锁定一套数字并同步正文、图注、表格和版面诊断；本轮不擅自拍板。 |
| B-03 | OPEN | 正文仍有四组占位引用没有可接受的完整证据链。 | `[Paillier]`：`paillier2020` 的 DOI/题名与 benchmark/index 记录冲突；`[Johst]`：候选 DOI `10.1109/WiSEE.2024.3456789` 与索引 DOI `10.1109/WiSEE61249.2024.10850117` 冲突；`[B11]`：DOI `10.1109/LPT.2024.3523478`，无可用 BibTeX key，索引状态 failed；`[Shieh-Djordjevic 2010]`：未找到匹配的 BibTeX 或本地论文资产。四组均未写入本工程 `references.bib`。 | 为每组找到作者、题名、 venue、年份和 DOI/论文路径一致的证据后，才能新增正式条目并改为 `\cite{}`；在此之前保留为 unresolved，不编造条目。 |
| B-04 | OPEN | CCISP 页数口径未锁定。 | CCISP 官方投稿页 [`sub.html`](https://www.ccisp.org/sub.html) 当前写 full paper `5--10` pages；既有项目材料仍使用 `4--6` pages（`projects/simulation/ADVISOR_BRIEFING_2026-07-09_v2_ccisp.md:19`）。 | 以会议最新作者指南/投稿系统说明确认最终范围；在确认前，骨架只能报告实测页数，不能把 `4--6` 或 `5--10` 当作已拍板规则。 |
| B-05 | OPEN | 正文结果数字与源文档交叉检查表存在 `1.9 dB` / `1.85 dB` 精度口径差异。 | W001/W002 正文及当前 LaTeX Abstract/Introduction/Conclusion 使用 `about 1.9 dB`；W001/W003 的交叉检查表和 W002 的数字表写 `1.85 dB`。首轮按正文抽取，未自行改数字。 | 锁定正文与交叉检查表的统一精度和 fair/naive 口径，再同步 Abstract、Conclusion、表格、图注和验证材料。 |
| B-06 | OPEN | DA 估计器文字声称对块内 `N_p` 个导频求平均，但公式只写单个 `r_p p^*`。 | W002 `:16` 与目标 `sections/method.tex:4-7` 都保留该组合；LaTeX 未新增这一不一致。 | 明确公式是否应展开导频求和/平均，或把文字改为与公式一致；需回到方法定义后再改。 |
| B-07 | CLOSED | fixed benchmark 与 Fig.3 横轴已统一。 | D021/V017：四场景正式 fixed 均为 5--35 dB、2 dB 步长，图轴显式为 5--35 dB；A/B adaptive 仍为 5--25 dB。 | 已由 1920-cell formal runner、独立 verifier 和 fresh build 闭合。 |

## DRAFT DEBT

| ID | 状态 | 问题 | 证据与当前处理 | 解除条件 |
|---|---|---|---|---|
| D-01 | OPEN | `naive` 是否适合作为对外论文术语尚未审查。 | W001/W002/W003 使用 `naive, net of pilot overhead`；该词需要按 `.agents/skills/external-output/SKILL.md` 的 C1--C10 审查，特别是术语定义、数字口径、对照对象、首次出现自包含性和规范表达。 | 明确定义 `naive` 与 fair/其他口径的关系，或替换为审稿人可直接理解的标准术语；同步标题、摘要、正文、表格和脚注。 |
| D-02 | OPEN | HTML TBD、导师未定口径、纵轴范围和 Table I 冗余均未收口。 | W002 §IV-A/§IV-B 保留 TBD：纵轴范围、`10^{-5}` 解读、标题/数字口径；Table I 的行列与正文重复程度也未最终确认。 | 收到导师口径后集中处理，删除所有 HTML 注释，锁定纵轴范围、表格内容和数字呈现；首轮不自行扩写或补数字。 |
| D-03 | OPEN | Fig.1/Fig.2 尚未完成视觉验收。 | H015/R018 规定首轮不继续绘图；LaTeX 只允许放显式尺寸合理的占位框，不得把占位框当作最终图形。 | 完成独立视觉验收并获得明确拆图/合图决定后，再替换占位框；本轮不锁死图形结构。 |
| D-04 | PARTIAL | 构建链已可用，但 Codex 的 `pdftoppm`/`pdfinfo` wrapper 仍存在路径遮蔽。 | MiKTeX 的 `pdflatex`/`latexmk`/`bibtex`/`biber` 已可用；`pdftoppm`/`pdfinfo` 的默认命令解析到 wrapper。本轮已使用 MiKTeX 绝对路径完成 PDF 检查和渲染。 | 修正 PATH 优先级或为项目固定一套可审计的工具路径配置。 |
| D-05 | PARTIAL | 首轮浮动图版面仍有末页留白，但本轮已按用户指定把 Fig.1/Fig.2 放到第 2/3 页并将 BER Fig.3 改为单栏。 | 当前 fresh build 7 页：Fig.1 第 2 页顶部、Fig.2 第 3 页顶部、BER Fig.3 第 5 页单栏；第 7 页仍只有参考文献尾部，存在明显留白。逐页渲染未发现裁切或重叠。 | 在正文口径、图形视觉验收和投稿页数口径锁定后，再单独处理末页留白与整体 float/图尺寸优化。 |
| D-06 | OPEN | Fig.3 图例含 Oracle 曲线，但当前 caption 未解释 Oracle 的含义。 | 独立 verifier 发现 `ccisp_fig2_ber.pdf` 的图例包含 Oracle；目标 `sections/results.tex:9` 的 caption 只写 DA/NDA。 | 在图例语义和 baseline 定义锁定后补充自包含 caption；不在本轮猜测 Oracle 的方法含义。 |
| D-07 | OPEN | external-output C1–C10 尚未全部通过。 | 独立 verifier 的 V001 结论：C1/C5/C6/C7/C10 为 PARTIAL，C2/C3/C4 为 DEBT，C8/C9 PASS（C9 为 N/A）；主要债务是 `naive`、缩写首次定义、阈值语义、4 组 unresolved 引用及数字口径。 | 完成正式术语/引用/数字/缩写审查后，再将 C1–C10 逐项关闭。 |

## INFO

| ID | 状态 | 已确认事实 | 证据 |
|---|---|---|---|
| I-01 | RECORDED | CCISP 官方页面提供模板 ZIP 直链：[`IEEE-Conference-LaTeX-template_7-9-18.zip`](https://www.ccisp.org/file/IEEE-Conference-LaTeX-template_7-9-18.zip)。记录的 SHA256 为 `64CD0E9BD91A909530A9BD65F41622959CCD5D57A6344200FA70F967AF8A7ECD`；内部模板为 `IEEEtran.cls`，文件头标注 `2015/08/26 version V1.8b`。 | 官方投稿页 [`sub.html`](https://www.ccisp.org/sub.html)；本工程 `IEEEtran.cls:2` 与官方 ZIP 记录的版本头一致。ZIP 哈希与 class 文件哈希不是同一个对象，不混用。 |
| I-02 | RECORDED | 本工程 `references.bib` 首轮白名单仅包含 `valjus2025dsp`、`alhabash2001`、`viterbi1983` 三条已有证据支持的记录。 | `毕设/写作材料/references.bib` 对应完整字段；DOI 分别为 `10.1002/sat.1553`、`10.1117/1.1386641`、`10.1109/TIT.1983.1056713`。 |
| I-03 | RECORDED | 三张既有数据图使用 PDF 资产；首轮 Fig.1/Fig.2 仍是占位策略，不在本清单中假设视觉验收已完成。 | `projects/simulation/figures/ccisp_fig2_ber.pdf`、`ccisp_fig3_gain.pdf`、`ccisp_fig4_crossover.pdf`；图形最终编号交给 LaTeX 自动生成。 |

## 引用审计快照

| 正文占位 | 状态 | 当前可验证证据 | 本轮动作 |
|---|---|---|---|
| `[sat.1553]` | RESOLVED | `valjus2025dsp`; DOI `10.1002/sat.1553`; `papers/doi/10.1002_sat.1553/` | 已纳入 `references.bib`。 |
| `[Al-Habash 2001]` | RESOLVED | `alhabash2001`; DOI `10.1117/1.1386641`; `papers/doi/10.1117_1.1386641/` | 已纳入 `references.bib`。 |
| `[V&V 1983]` | RESOLVED | `viterbi1983`; DOI `10.1109/TIT.1983.1056713`; `papers/doi/10.1109_tit.1983.1056713/` | 已纳入 `references.bib`。 |
| `[Paillier]` | UNRESOLVED | `paillier2020` 与 benchmark/index 的 DOI、题名记录冲突 | 不复制、不编造；见 B-03。 |
| `[Johst]` | UNRESOLVED | 候选 DOI `10.1109/WiSEE.2024.3456789` 与索引 DOI `10.1109/WiSEE61249.2024.10850117` 冲突 | 不复制、不编造；见 B-03。 |
| `[B11]` | UNRESOLVED | DOI `10.1109/LPT.2024.3523478` 无可用 key，索引状态 failed | 不复制、不编造；见 B-03。 |
| `[Shieh-Djordjevic 2010]` | UNRESOLVED | 未找到匹配的 BibTeX 或本地论文路径 | 不复制、不编造；见 B-03。 |

## 构建与版面快照（2026-07-13）

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`：exit 0，生成 `main.pdf`。
- `pdfinfo`：6 页，Letter 纸张（612 x 792 pt），未加密，PDF 1.5；`documentclass[conference]{IEEEtran}` 产生双栏版式。
- `pdffonts`：列出的字体全部为 `emb=yes`，未发现未嵌入字体。
- 最终 `main.log`：未发现 LaTeX error/fatal、未定义引用/交叉引用、Overfull hbox 或 Underfull；仅保留 MiKTeX 的“尚未检查更新”非 LaTeX 提示。
- 已用 MiKTeX 绝对路径的 `pdftoppm` 渲染 6 页并逐页检查：双栏、公式、表格和三张数据图均可读，未发现裁切或越界；第 4 页及第 6 页存在由浮动图排版造成的明显留白，见 D-05。
- 页数诊断：相对既有任务口径 `4--6`，当前为上限 6 页（超出 0 页）；相对 CCISP 官方投稿页的 `5--10`，当前位于范围内、距下限多 1 页。两种口径仍未拍板，见 B-04。

## 首轮关闭标准

- [ ] B-01：`gamma_th` 的固定阈值/观测交点语义已按 D008 统一。
- [ ] B-02：正文与重画图的 crossover 数字已选定并同步。
- [ ] B-03：四组 unresolved 引用均有可验证完整条目，或从正文删除。
- [ ] B-04：CCISP 官方页数口径已确认。
- [ ] D-01--D-04：外部术语、TBD/表格/图形验收和构建工具路径债务已处理。
- [ ] D-05：浮动图位与末页留白已在正式版面优化轮处理。
- [ ] D-06：Fig.3 的 Oracle 曲线含义已写入自包含 caption。
- [ ] D-07：external-output C1–C10 已完成审查并关闭债务。

## 标题版增量构建（2026-07-14）

- `main.tex:13` 已改为 `Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links`；主线程只改标题，不涉及 W001–W003、实验数字或公式；用户同时更新了 Fig.1/Fig.2 的 draw.io 导出源。
- 最新 fresh build 命令：`latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`；exit 0，`main.pdf` 为 8 页 Letter 双栏，1,029,955 bytes。
- 第 1 页标题自然换为两行；日志无 LaTeX error、undefined citation/reference 或 overfull box；有 1 个 `Underfull \\hbox`（`main.log:337`，badness 3158）和 1 个 `Underfull \\vbox`（`main.log:361`，badness 1895）。
- 逐页渲染观察：Fig.1 当前在第 3 页，Fig.2 在第 4 页，BER 图在第 6 页，结论/参考文献在第 8 页。两张系统图已用 `figure* [t]`，但 Fig.1 的声明位于 `system_model.tex` 的 section 之后；要放到第 2 页顶部，应将该浮动声明移到 `main.tex` 的 introduction 之后、system model 之前。
- 当前源已引用 `fig1_system_model_v5.pdf` 与 `fig2_adaptive_cpr.pdf`；当前 Fig.3（BER 总览）仍为双栏 `figure*`，此前“缩小到单栏”的版式约束尚未实施。

## 版式调整增量（2026-07-14）

- 用户本轮要求 Fig.1 放第 2 页、Fig.2 放第 3 页，并将 Fig.3 缩小为单栏；本轮只实现这三项，不修改正文、数字、公式、图资产、仿真或绘图脚本。
- `main.tex` 现在按 Fig.1 → Introduction → Fig.2 的浮动声明顺序组织，实际渲染为 Fig.1 第 2 页顶部、Fig.2 第 3 页顶部，且正文接在图下；`system_model.tex` 与 `method.tex` 不再重复声明两张系统图。
- `sections/results.tex:4--9` 的 BER 总览使用单栏 `figure` 和 `width=\\columnwidth`，实际为第 5 页 Fig.3；Fig.4/Fig.5 在第 6 页。
- fresh `latexmk` exit 0，`main.pdf` 7 页（1,029,589 bytes），Letter 双栏；无 LaTeX error、undefined citation/reference 或 overfull box；`main.log:344` 有 Underfull hbox badness 3158，`:362` 有 Underfull vbox badness 4634。逐页 PNG 检查未发现裁切、重叠或公式越界。
- 4--6 页旧任务口径仍超出 1 页；第 7 页参考文献尾部留白和 Fig.1/Fig.2 实际图越过原始占位硬边界仍是债务。

## 独立 verifier 快照（V001）

- **正文保真：PARTIAL/PASS**。未发现 W001–W003 实质段落、主要公式或结论被遗漏/擅改；HTML TBD 被省略并已登记。W002 源文档中的 Figure 2 在目标 PDF 中因 Fig.1/Fig.2 占位而自动成为 Fig.3，这是结构性编号变化，不是正文改写。
- **数字/公式/引用：PARTIAL**。3 条已核验引用一致，4 组 unresolved 被完整暴露为 11 处红色标记；B-01 的上游 W002 口径、B-02、B-05、B-06、B-07 仍未解除，且本轮未跑仿真，因此不对数字真实性作新验证。
- **图形：PASS（首轮策略）**。Fig.1/Fig.2 是显式占位框，三张既有 PDF 图成功嵌入并自动编号为 Fig.3–Fig.5；未发现缺图、裁切或重叠。
- **PDF：PASS（当前构建产物）**。`main.pdf` 6 页、Letter、字体嵌入、可读；最终日志无 LaTeX error/undefined ref/overfull/underfull。独立 verifier 未再次运行 latexmk，最新编译证据以本轮命令和 `main.log` 为准。
- **D008 delta 复核：PASS**。独立 delta verifier 确认 `sections/method.tex:34,38` 只把 `gamma_th` 用作固定 effective-SNR switching threshold，并明确 observed crossover 不用于重新估计；最新版 PDF 仍为 6 页且日志无 LaTeX error/undefined ref/overfull/underfull。

### external-output C1–C10

| 检查 | 结论 |
|---|---|
| C1 | PARTIAL：未见内部方法代号，但 unresolved `B11` 仍是内部引用别名。 |
| C2 | DEBT：`naive` 未定义；上游 W002 仍有 effective-SNR/crossover 口径债务，目标骨架已按 D008 分离二者。 |
| C3 | DEBT：SNR/FSO/AWGN/HD-FEC/BER 等缩写的首次展开与自包含性不完整。 |
| C4 | DEBT：数字存在 `1.9/1.85`、`17.9/18.0` 等冲突，且本轮未跑仿真。 |
| C5 | PARTIAL：Results 指向固定 NDA baseline，但 Abstract/Introduction 的 1.9 dB 尚未明确 baseline。 |
| C6 | PARTIAL：尚未充分区分切换方法增益与 DA/NDA 固有互补性。 |
| C7 | PARTIAL：3 条正式引用可用，4 组 unresolved 引用阻塞正式稿。 |
| C8 | PASS：未发现明显文学化或内部讨论措辞。 |
| C9 | PASS（N/A）：论文正文没有“请老师决定”类问询。 |
| C10 | PARTIAL：DA/NDA 基本自包含，但 unresolved 引用、`naive`、阈值和缩写债务仍影响首次阅读。 |
