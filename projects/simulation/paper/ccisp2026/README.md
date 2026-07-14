# CCISP 2026 LaTeX 投稿骨架 / CCE-CC-002 版面探针

这是第一轮可编译版面探针，不是最终投稿稿。当前工作树中的正文已经是获批 `CCE-CC-002` 的扩展预览，不再是旧的 6 页占位骨架；因此不得把当前文件误读为 W001–W003 的逐字抽取版。工程使用 CCISP 官方投稿页提供的 `IEEE-Conference-LaTeX-template_7-9-18.zip` 中的 `IEEEtran.cls`；官方 ZIP SHA256：

`64CD0E9BD91A909530A9BD65F41622959CCD5D57A6344200FA70F967AF8A7ECD`

## 内容范围

- 当前 `sections/*.tex` 采用 D004/V003 修正后的 `sqrt(h)` 接收模型、100-symbol channel block / 256-sample DSP window、multi-pilot DA-LS、两层选择器、data-BER 和 BER-ratio 口径；旧 W 文件只读，不能直接覆盖回去。
- 当前工作树引用最新的 `fig1_system_model_v5.pdf`、`fig2_adaptive_cpr.pdf` 以及三张已有数据图；两张 PDF/SVG/PNG 已从当前 draw.io 编辑源重新导出。原 CCISP 首轮合同要求 Fig.1/Fig.2 使用显式占位框，这个偏离仍是阻塞债务，详见 `issues.md`，不表示图形方案已最终验收。
- 当前 7 个 BibTeX 条目均被正文引用；引用解析与构建已通过，但 `oracle` 图例语义、来源同步和投稿口径仍需独立收口。
- 当前作者栏为 `Anonymous Submission`，标题为工作标题；这不是最终作者/单位信息，也不等于已完成投稿元数据。

## 构建

在仓库根目录执行：

```powershell
$env:Path = "C:\\Program Files\\Git\\usr\\bin;C:\\Users\\zzt\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64;$env:Path"
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

如果当前环境优先解析到 Codex 的 `pdftoppm`/`pdfinfo` wrapper，逐页渲染和 PDF 检查使用 MiKTeX 路径中的同名可执行文件。不要把 `毕设/论文/ccisp/` 的示例正文复制进来；它只是同源模板样例。

## 当前状态

- 首轮目标：测量双栏版式页数、公式/图表溢出和引用债务；当前版式调整后的 fresh build 为 `latexmk` exit 0、`main.pdf` 7 页（1,029,589 bytes）。
- 当前标题为 `Received-Power-Aware Carrier Phase Estimator Selection for Turbulent Satellite--Ground FSO Links`；第 1 页标题自然换为两行。
- 当前日志无 LaTeX error、未定义引用、overfull box；有 1 个 `Underfull \\hbox`（`main.log:344`，badness 3158）和 1 个 `Underfull \\vbox`（`main.log:362`，badness 4634）。字体检查显示全部嵌入，PDF 为 Letter 纸张。
- 已使用 MiKTeX 绝对路径渲染并逐页检查当前 7 页 PDF；Fig.1 位于第 2 页顶部、Fig.2 位于第 3 页顶部，正文接续在图下；BER Fig.3 位于第 5 页并改为单栏，Fig.4/Fig.5 位于第 6 页，结论与参考文献跨第 6--7 页。未发现裁切、重叠或公式越界；第 7 页仍有参考文献尾部留白，记录在 `issues.md`。
- 当前 Fig.3 使用 `figure` + `width=\\columnwidth`；Fig.1/Fig.2 使用最新用户导出的 PDF，版位已按本轮要求调整，但其视觉方案仍不视为最终验收。
- 当前不锁定 CCISP 页数口径：官方投稿页写 5–10 页，既有任务口径写 4–6 页。
- 当前不运行仿真、不修改绘图脚本、不处理 Fig.1/Fig.2 最终视觉方案。

## 版式调整增量（2026-07-14）

- 将 Fig.1 的 `figure*` 声明放在 Abstract 之后、Introduction 之前；将 Fig.2 的声明放在 Introduction 之后、System Model 之前。这样 IEEEtran 实际排版为 Fig.1 第 2 页顶部、Fig.2 第 3 页顶部，且两页均有正文接续，不使用人为空白页。
- 将 `sections/results.tex` 的 BER 总览改为单栏 `figure`，图片宽度改为 `\\columnwidth`；没有修改图资产、图内容、正文数字或公式。
- 重新执行 `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`：exit 0，生成 7 页、1,029,589 bytes 的 Letter 双栏 PDF。无 LaTeX error、undefined citation/reference 或 overfull box；保留 1 个 Underfull hbox（badness 3158）和 1 个 Underfull vbox（badness 4634）。
- 已用 MiKTeX `pdftoppm` 逐页渲染 7 页检查；BER Fig.3 单栏图可读且未裁切。4--6 页旧任务口径仍超出 1 页；CCISP 官方页当前的 5--10 页口径则在范围内，二者仍未拍板。
