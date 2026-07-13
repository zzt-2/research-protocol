# [S001] CCISP 2026 LaTeX 投稿骨架启动与 Gate 0 预检调度

> 2026-07-13 | 阶段：Gate 0 预检与首轮实施 | 状态：官方模板硬门 PASS；首轮骨架已编译，Gate 0 总体仍 PARTIAL（4 组引用 unresolved、投稿细则/页数口径未锁定）

## 目标

承接 H015，在独立专题 `2026-07-13-ccisp-submission-prep` 中先核验官方模板来源、正文与引用资产、以及本机构建链；只有三项均有证据后，才进入 `projects/simulation/paper/ccisp2026/` 的可编译骨架实施。

## 记录

### 专题启动与接收方验证

- 已完整读取原专题规定的 H015、topic-index、D008/D009/D011/D013/D014、W001–W003、R011、R016、R018、revision-queue、`.sessions/profile.md`。
- H015 声称 1：W001–W003 正文文件存在。**PASS**：三个文件均存在并已读取，路径分别为 `.sessions/2026-07-09-thesis-writing/W001-intro-system-model.md`、`W002-method-results.md`、`W003-conclusion-abstract.md`。
- H015 声称 2：V001 判定 Fig.2–4 数据图 PASS。**PASS**：`.sessions/2026-07-09-thesis-writing/verifications.md:3-21` 记载 V001，三个脚本运行 exit 0、Fig.3 21 个源数据值、Fig.4 交点 18.0129/16.8661/10.7026 dB、PDF 字体嵌入且 Fig.1 未修改。
- H015 声称 3：本地尚无 CCISP 官方 LaTeX 模板。**PASS（本地盘点层面）**：仓库内 `.cls/.sty/.tex` 文件只有 `毕设/graduate-thesis/bithesis.cls` 及其学位论文工程文件；未发现 CCISP/IEEE conference 工程。该事实不等于官方模板不存在，仍须由 Agent A 做官方来源核验。
- 已检查 `.sessions/_registry.yaml`：原写作专题 `2026-07-09-thesis-writing` 为 active、`conflicts_with: []`；新 slug 之前不存在；本专题登记为其材料依赖，不把 LaTeX 实施塞回原专题。
- 当前范围未违反原专题“明确不含”：本轮只建立独立投稿准备专题和 Gate 0 预检，不修改原正文、不跑实验、不画图。

### Gate 0 预检调度

并行派发三项只读任务，最多同时 3 个子 agent：

1. **Agent A / T001**：只查 CCISP 官网、会议作者指南或 IEEE 官方来源，核验专用模板、标准 IEEE 模板指向、页数/双栏/匿名/版权要求及下载文件。
2. **Agent B / T002**：只读盘点 W001–W003 正文边界和所有占位引用，映射两个现有 `.bib`、`papers/index.json` 与 benchmark-paper-set 路径；无法核验者标 unresolved。
3. **Agent C / T003**：只读盘点 latexmk/pdflatex/xelatex/bibtex/biber、PDF 渲染/字体工具及仓库可复用会议工程，明确排除毕业论文模板。

实施硬门：若 Agent A 不能提供 CCISP 官方模板，或不能提供 CCISP 官方页面指向 IEEE 标准模板的证据，则停止工程实施并向用户报告；不得用任意 IEEE 模板替代。其他缺口统一进入目标工程的 `issues.md`。

### 预检回传与 Gate 0 汇总

**Agent A：官方模板核验。**

- **官方来源硬门 PASS**：CCISP 官方投稿页 [CCISP 2026 Submission](https://www.ccisp.org/sub.html) 提供官方 LaTeX 模板链接，直链为 `https://www.ccisp.org/file/IEEE-Conference-LaTeX-template_7-9-18.zip`。
- 官方页摘要：英文论文、全文 5–10 页、遵循模板、double-blind review、通过 Microsoft CMT 提交全文或摘要；注册页说明 5 页以内免费、超过 5 页有额外页费。
- **页数冲突需保留**：用户任务指定按“CCISP 4–6 页要求”报告页数差距，但当前 CCISP 官方投稿页明确写 5–10 页；首轮不能把 4–6 当官方事实，待用户/会议页面进一步确认后在 `issues.md` 标明两种口径。
- 未核验项：纸张尺寸、双栏、版权栏、匿名元数据、PDF/源文件包细则；官方页未明确指向 IEEE 官方模板页。模板 ZIP 内部尚未检查，不能把文件名 `7-9-18` 当正式版本日期。

**Agent B：正文与引用资产。**

- 正文边界：W001 §I–§II；W002 §III–§IV（排除 HTML TBD）；W003 §V 与 Abstract。W001 无独立 Abstract；W003 Abstract 是唯一 Abstract 正文。
- 共 7 个去重占位符、20 次正文出现。已核验：`[sat.1553]` → `chen2025dsp`/`valjus2025dsp`、DOI `10.1002/sat.1553`；`[Al-Habash 2001]` → `alhabash2001`、DOI `10.1117/1.1386641`；`[V&V 1983]` → `viterbi1983`、DOI `10.1109/TIT.1983.1056713`。
- 必须列 unresolved：`[Paillier]`（Bib 与 benchmark/index 指向不同论文）、`[Johst]`（Bib DOI 与 benchmark/index DOI 冲突）、`[B11]`（无 BibTeX key、索引状态 failed）、`[Shieh-Djordjevic 2010]`（两个 Bib 与索引均无匹配）。
- 不复制 session 元数据、交叉检查表或 HTML TBD；Agent B 未修改文件。

**Agent C：构建环境。**

- `latexmk`、`pdflatex`、`xelatex`、`bibtex`、`biber` 均 missing。
- `pdftoppm`、`mutool`、`gs`/`gswin64c`、`pdfinfo`、`pdffonts`、`fc-list` 均 missing。
- 仓库只发现 `毕设/graduate-thesis/` 的 BIThesis 学位论文工程（`bithesis.cls`、`main.tex` 等 12 个文件），没有 IEEE/conference/CCISP 工程；目标路径尚不存在。

**原始 Gate 0 结论：PARTIAL / BLOCKED。** 官方模板来源硬门已通过，正文/引用资产位置已明确但存在 4 组 unresolved；初始本机构建链不可用，因此当时不能进入工程实施、编译或 PDF 交付。该历史结论保留，后续恢复情况见下节。

### 构建链恢复（用户授权安装后）

- 已按用户授权安装用户级 MiKTeX 25.12；核心命令位于 `C:\\Users\\zzt\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64`。
- 已验证：`pdflatex` 4.23、`bibtex` 4.2、`biber` 可执行、`xelatex`/`lualatex` 可执行，`latexmk` 4.88。
- `latexmk` 依赖 Perl；本机已有 Git for Windows 的 Perl 5.38.2（`C:\\Program Files\\Git\\usr\\bin\\perl.exe`），已验证 `latexmk --version` 返回 exit 0。
- 已安装用户级 Poppler 25.07.0-0；当前 MiKTeX 路径中的 `pdftoppm`、`pdfinfo`、`pdffonts` 已验证可执行（Poppler 24.04.0）。
- MiKTeX 用户配置已设置 `[MPM]AutoInstall=1`，避免首次编译因缺少宏包停在交互安装窗口。
- `biber` 首次调用有 Git Perl locale warning，但 exit 0；后续编译时须把该 warning 与 LaTeX warning 分开记录。
- 重开终端后，`perl`、`pdflatex`、`latexmk`、`bibtex`、`biber` 已可由 PATH 直接解析；`pdftoppm`/`pdfinfo` 被 Codex runtime 的同名 wrapper 抢先解析且 wrapper 报路径错误，使用 MiKTeX 绝对路径时二者均 exit 0。后续渲染固定使用 MiKTeX 路径或显式调整命令优先级。
- **当前 Gate 0 状态更新为 PARTIAL**：构建链缺口已解除，但 4 组引用 unresolved、官方模板细则和页数口径冲突仍未解除，因此还不能宣称 Gate 0 全部通过。

### 现有 `毕设\\论文\\ccisp` 页数探针

- 只读盘点发现 5 个文件：`conference_041818.tex`、`conference_041818.pdf`、`IEEEtran.cls`、`IEEEtran_HOWTO.pdf` 和 `.DS_Store`。
- `conference_041818.tex` 使用 `\\documentclass[conference]{IEEEtran}`，正文是 IEEE 模板说明文字，不是本研究论文；其配套 PDF 为 3 页。因此，这个 PDF 只能证明已有 IEEEtran conference 版式样例，不能作为当前稿件页数。
- 对 W001–W003 抽取的 Abstract 与 §§I–V 做只读词量统计，去除 HTML 注释后约 2,384 个英文词元，尚未计入正式参考文献。
- 在现有双栏样例上做的初步版面估计是：正文、3 张数据图、Fig.1/Fig.2 占位、Table I 和参考文献合计约 5–6 页；这是页数探针，不是 LaTeX 编译实测。
- 本机 LaTeX 工具链已安装并完成命令级核验，但尚未在目标论文工程中编译，因此上述估计仍不是实测页数；也不把该目录的旧 `IEEEtran.cls` 直接升级为 CCISP 最终模板。

### 官方 ZIP 检查与首轮工程实施

- 从 CCISP 官方投稿页下载的 ZIP 为 `IEEE-Conference-LaTeX-template_7-9-18.zip`，SHA256 为 `64CD0E9BD91A909530A9BD65F41622959CCD5D57A6344200FA70F967AF8A7ECD`。
- ZIP 只包含 `.DS_Store`、`conference_041818.tex`、`conference_041818.pdf`、`IEEEtran_HOWTO.pdf` 和 `IEEEtran.cls`；`IEEEtran.cls` 文件头为 IEEEtran V1.8b。与仓库已有 `毕设\\论文\\ccisp` 样例逐文件哈希比较，`.tex`、`.cls`、HOWTO 均一致，因此目标工程使用的是可追溯的官方 ZIP class，而不是任意 IEEE 模板。
- 已创建 `projects/simulation/paper/ccisp2026/`，包含 `main.tex`、`sections/abstract.tex`、`introduction.tex`、`system_model.tex`、`method.tex`、`results.tex`、`conclusion.tex`、`references.bib`、`issues.md`、`README.md` 和 `IEEEtran.cls`。
- W001–W003 保持只读；目标工程只抽取 Abstract 与 §§I–V，未复制 session 元数据、HTML 注释、检查表或旧版本对照表。标题/作者/单位仍为 DRAFT 占位；Fig.1/Fig.2 为显式占位框；已有三张数据图使用 PDF 资产并由 LaTeX 自动编号。
- `references.bib` 首轮只纳入 3 条已核验条目；4 组 unresolved 引用保留红色显式债务，未伪造 BibTeX。

### 首轮实测编译与版面诊断

- 在目标工程执行 `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`，exit 0，生成 `main.pdf`。
- `pdfinfo` 实测 6 页、Letter（612 x 792 pt）、未加密；`pdffonts` 列出的字体全部 `emb=yes`。
- 最终 `main.log` 未发现 LaTeX error/fatal、未定义引用/交叉引用、Overfull hbox 或 Underfull。MiKTeX 更新提示为环境提示，不计作 LaTeX warning。
- 用 MiKTeX 绝对路径的 `pdftoppm` 渲染 6 页并逐页检查：双栏、公式、表格、占位框和三张 PDF 图均可读，未见裁切；第 4 页和第 6 页因浮动图排版留白明显，登记为目标工程 D-05，不在首轮擅自压缩。
- 页数结论：相对既有任务口径 `4--6`，6 页正好处于上限；相对 CCISP 官方投稿页 `5--10`，6 页位于范围内。两种口径仍并存，不把任一口径写成最终合规结论。

### 当前已知冲突与转换规则

- W002 §III 同时出现“固定 effective-SNR 值”和“γ_th 是 BER 曲线 crossover SNR”的两种含义；以 D008 为准，目标 LaTeX 不让两种说法并存，并在 `issues.md` 保留源文件冲突证据。
- 正文历史 crossover 17.9/16.8/10.7 dB 与 R018/重画图统一插值约 18.0/16.9/10.7 dB 并存；首轮列为冲突，不擅自拍板。
- `naive` 对外术语、HTML TBD、导师未定口径、纵轴范围、Table I 冗余和 Fig.1/Fig.2 未视觉验收，均必须在 `issues.md` 暴露。

## 决策引用

- D008：固定 effective-SNR 阈值与事后观测 crossover 分离；目标稿不能两种说法并存。
- D009：Fig.2–4 数据图使用既有重画资产；Fig.1 延期。
- D011：Fig.1 系统总览与 Fig.2 自适应 CPR 机制的双图方案暂不在 LaTeX 首轮锁死。
- D013：未来恢复图工作时保留 draw.io 编辑源、SVG/PDF 交付路线；本轮不执行。
- D014：LaTeX 骨架优先，独立专题实施。
- 无本 session 新建 D### 决策。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

- 等待独立 verifier 对正文保真、数字/公式/引用、占位图、PDF 可读性和 external-output C1–C10 做复核；依据复核结果更新 `verifications.md`（如形成新的验证记录）。
- 4 组 unresolved 引用、D008 语义冲突、crossover 数字冲突、`naive` 术语、TBD/Table I/图形视觉验收、官方页数口径和末页留白继续留在目标工程 `issues.md`，本轮不擅自拍板。

### 独立复核回传

- 已形成 `verifications.md:V001`，结论为 PARTIAL：正文实质保真、Fig.1/Fig.2 占位、三张 PDF 图嵌入和当前 PDF 可读性通过；数字/公式/引用与 external-output C1–C10 仍有明确债务。
- verifier 额外指出三项源稿自身冲突并已写入 `issues.md`：`1.9/1.85 dB` 精度、DA 公式与 `N_p` 导频平均文字、结果 SNR 扫描范围与 BER 图横轴范围。
- 已形成 `verifications.md:V002`，结论为 PASS（delta）：独立 verifier 确认 `gamma_th` 在目标 LaTeX 中只表示固定 effective-SNR switching threshold，observed crossover 已明确不用于重新估计；最新版 6 页 PDF、日志和 Fig.1/Fig.2 占位均通过复核。
