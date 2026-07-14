# Topic Index: CCISP 2026 LaTeX 投稿骨架

> slug: 2026-07-13-ccisp-submission-prep
> status: active | created 2026-07-13 | last_updated 2026-07-14

## 专题定位（一句话）

在官方模板来源可核验、正文与引用资产可追溯、且本机构建链可用的前提下，为 CCISP 2026 建立第一轮可编译 LaTeX 投稿骨架；本轮只做组装、诊断和债务登记，不做最终定稿。

## 原始目标（冻结）

建立 `projects/simulation/paper/ccisp2026/` 下的 CCISP 2026 双栏论文 LaTeX 骨架，抽取 W001–W003 的 Abstract 与 §I–§V 正文，接入可核验引用和已有 PDF 数据图，保留 Fig.1/Fig.2 为显式占位，并完成编译、渲染和独立验证。

## 范围边界

### 当前范围

- 核验 CCISP/IEEE 官方模板、页数、双栏、匿名、版权栏等投稿要求。
- 盘点正文源文件、占位引用、BibTeX、论文索引和 benchmark 论文路径。
- 盘点本机构建链与可复用工程；毕业论文模板不能冒充会议模板。
- 创建首轮 LaTeX 工程、章节文件、引用文件、issues.md 和 README.md。
- 使用现有 PDF 数据图；Fig.1/Fig.2 只放合理尺寸的显式占位框。
- 用 latexmk 编译、渲染逐页检查、记录页数/警告/引用/盒子溢出，并由独立 verifier 复核。

### 明确不含

- 不运行仿真，不修改仿真参数、绘图脚本或结果 JSON。
- 不修改 W001、W002、W003、R011、R016、R018 或原写作专题的正文/规格文件。
- 不继续绘制、编辑或锁死 Fig.1/Fig.2 的最终方案。
- 不重写研究故事、不扩写内容、不改实验数字、不擅自选择 fair/naive 口径。
- 不推断作者、单位、导师或其他个人信息；不把毕业论文工程当会议模板。
- 官方模板无法从 CCISP/IEEE 官方来源核验时，停止实施，不拿任意 IEEE 模板冒充最终模板。
- 不处理范围外旧文件或旧专题遗留事项。

### 范围变更记录

- 无。D014 已将 LaTeX 实施明确转入本独立专题；本专题不回写原写作专题。

## 已确认结论

### 不变量

1. 官方模板来源是实施硬门；无 CCISP 官方模板或 CCISP 官方指向 IEEE 标准模板的证据，就不能进入工程实施。
2. W001–W003 只读；LaTeX 目标只抽取 Abstract 与 §I–§V 正文，不复制 session 元数据、HTML 注释、检查表或旧版本对照表。
3. Fig.1/Fig.2 暂不定稿；LaTeX 只放显式占位框，语义 label 和自动编号优先。
4. 所有引用必须可核验；无法映射到真实 BibTeX/DOI/论文路径的条目进入 `issues.md`，不得编造。
5. 首轮交付是可编译骨架和版面诊断，不是最终投稿定稿。

### 其他结论

- 建议工程路径为 `projects/simulation/paper/ccisp2026/`。
- 已有数据图使用 `ccisp_fig2_ber.pdf`、`ccisp_fig3_gain.pdf`、`ccisp_fig4_crossover.pdf`。
- D008 要求把固定 effective-SNR 阈值与事后观测 crossover 严格分开；不能在 LaTeX 中让两种含义并存。
- Table I 口径尚未锁定，首轮使用结构化占位，不填未经确认的 fair/naive 选择。
- 官方投稿页当前写 5–10 页，而用户任务要求按 4–6 页报告差距；两种页数口径待进一步确认，不能在工程中擅自选定。

## 进展线索

- **S001**：完成 H015 接收方验证、新专题注册、三项 Gate 0 预检、构建链安装、官方 ZIP 检查和首轮骨架实施；核心编译链可用，两个 Codex Poppler wrapper 仍有路径债务，MiKTeX 绝对路径可用；官方模板硬门通过，引用有 4 组 unresolved，Gate 0 总体仍为 PARTIAL。目标 `main.pdf` 已实测 6 页；最终日志无 LaTeX error/undefined ref/overfull/underfull，字体全部嵌入。第 4、6 页有浮动图造成的留白，见目标工程 `issues.md` D-05。
- **T001–T003**：分别派发官方模板、正文/引用资产、构建环境只读预检。
- **V001**：独立 verifier 完成首轮复核，结论 PARTIAL；正文实质保真、占位图、现有 PDF 图和当前 PDF 可读性通过，数字/公式/引用与 external-output C1–C10 债务已补入目标 `issues.md`。
- **V002**：独立 delta verifier 复核 D008 语义修正，结论 PASS；`gamma_th` 已只表示固定 effective-SNR switching threshold，最新版 PDF/日志和 Fig.1/Fig.2 占位通过。
- **S002**：接收当前工作树的 CCE-CC-002 扩展预览并强制重建；最新版式增量 fresh `latexmk` exit 0，PDF 7 页、Letter、字体嵌入；Fig.1 已排第 2 页顶部、Fig.2 已排第 3 页顶部，BER Fig.3 已缩为第 5 页单栏，逐页检查无裁切/重叠。仍有 1 个 `Underfull \\hbox`、1 个 `Underfull \\vbox` 和第 7 页参考文献尾部留白。当前目标已实际嵌入 Fig.1/Fig.2，故与本专题原始占位硬边界存在 B-08；纯 text 3,241、非正文项合计后约 3,505，词数口径列 B-09。
- **V005**：独立 verifier 复核本轮三项版式改动，结论 PARTIAL；图位、单栏 Fig.3、PDF 属性、字体和错误诊断通过，Underfull 与末页留白保留为债务。

## 未决项

1. CCISP 2026 官方模板的具体投稿细则（纸张、匿名元数据、版权栏、最终源文件/PDF要求）是否还需从会议/IEEE指南补证。
2. 占位引用到真实 BibTeX/DOI/论文路径的映射完整度。
3. Table I 的最终口径与 Fig.2 纵轴范围等导师项。
4. Fig.1/Fig.2 的目标页位已完成；第 7 页参考文献尾部留白及整体 7 页（旧 4--6 页口径超 1 页）是否需要在正式版面优化轮处理。
5. `naive` 术语以及 external-output C1–C10 的独立复核结论。
6. 当前 CCE 扩展预览是否允许替代本专题的首轮占位骨架；实际 Fig.1/Fig.2 与 DRAFT 元数据仍未获得本专题范围内的明确确认。
7. D001 的 3,500 词验收采用纯 text 还是含标题/图注的总口径。

## 当前位置

当前位置：Gate 0 官方模板硬门 PASS，构建链可用；当前工作树已存在 CCE-CC-002 扩展预览，fresh PDF 为 7 页。S002 已完成用户指定的 Fig.1/Fig.2 第 2/3 页排版和 BER Fig.3 单栏调整；原始 Fig.1/Fig.2 占位边界、末页留白、词数口径、Oracle/术语语义和投稿页数仍未收口，当前交付仍不是最终投稿稿。
