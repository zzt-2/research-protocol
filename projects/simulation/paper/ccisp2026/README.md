# CCISP 2026 LaTeX 投稿骨架（DRAFT）

这是第一轮可编译版面探针，不是最终投稿稿。工程使用 CCISP 官方投稿页提供的 `IEEE-Conference-LaTeX-template_7-9-18.zip` 中的 `IEEEtran.cls`；官方 ZIP SHA256：

`64CD0E9BD91A909530A9BD65F41622959CCD5D57A6344200FA70F967AF8A7ECD`

## 内容范围

- `sections/abstract.tex` 与 `sections/introduction.tex`–`sections/conclusion.tex` 只抽取 W001–W003 的 Abstract 与 §§I–V 正文。
- `Fig.1`/`Fig.2` 只保留显式占位框；三张已有数据图使用 `../../figures/` 下的 PDF。
- 未核验引用保留为红色显式债务，不生成伪造 BibTeX；详见 `issues.md`。
- 标题、作者、单位为 DRAFT 占位，不推断个人信息。

## 构建

在仓库根目录执行：

```powershell
$env:Path = "C:\\Program Files\\Git\\usr\\bin;C:\\Users\\zzt\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64;$env:Path"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

如果当前环境优先解析到 Codex 的 `pdftoppm`/`pdfinfo` wrapper，逐页渲染和 PDF 检查使用 MiKTeX 路径中的同名可执行文件。不要把 `毕设/论文/ccisp/` 的示例正文复制进来；它只是同源模板样例。

## 当前状态

- 首轮目标：测量双栏版式页数、公式/图表溢出和引用债务。
- 实测结果：`latexmk` exit 0，`main.pdf` 为 6 页；最终日志无 LaTeX error、未定义引用、overfull/underfull box，字体检查显示全部嵌入。
- 已使用 MiKTeX 绝对路径渲染并逐页检查 PDF；图表、公式和占位框未发现裁切。浮动图位造成第 4 页和第 6 页留白，记录在 `issues.md` 的 D-05，暂不在首轮自行优化。
- 当前不锁定 CCISP 页数口径：官方投稿页写 5–10 页，既有任务口径写 4–6 页。
- 当前不运行仿真、不修改绘图脚本、不处理 Fig.1/Fig.2 最终视觉方案。
