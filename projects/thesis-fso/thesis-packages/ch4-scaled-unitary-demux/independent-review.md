# Independent review — Ch4 scaled-unitary demux package

## P0（科学事实 / 数字 / 身份错误）

未发现 P0。

- raw→CSV 独立 spot-check：未导入 `plot_ch4_results.py`，直接读取 `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/confirmation_raw.json`，逐格重算 `B0/B1/B2/C4/O1` 的 `Σbit_errors/Σpayload_bits`、逐 window `C4−B2`、PCG64 seed `2026083004` 的 2000 次 paired bootstrap，并重算 pooled Np=2。结果与 `data/ch4-confirmation-summary.csv:2-6` 的最大绝对差为 `4.8633e-11`（10 位小数序列化误差），且逐值匹配 `.sessions/2026-07-09-thesis-writing/verifications.md:687-693` 的 V027；256 个 seed、realization hash、observation hash 均唯一。
- B2/C4 身份核对：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls/development.py:154-169` 显示 B2 在 `tau=1` 时把两个奇异值均置为 `s1`，而 `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/scaled_unitary.py:61-85` 显示 C4 使用 `g=(s1+s2)/2`；两者均为同一 `UV^H` 方向。独立复矩阵探针得到归一化方向残差 `1.47e-16`（B2）与 `1.14e-16`（C4），只支持公共尺度差异，不支持“新偏振旋转”。包内 `fact-matrix.md:24`、`algorithm-box.md:35-37`、`claim-and-citation-ledger.md:10,15-16,28-30` 均保持该身份边界。

## P1（关键交付 / 证据链 / 语义错误）

未发现 P1。

- 九类交付齐全：`README.md`；`fact-matrix.md`；`chapter-blueprint.md`；`algorithm-box.md`；`claim-and-citation-ledger.md`；`data/ch4-confirmation-summary.csv`；`plot_ch4_results.py` + `figures/ch4-ber-comparison.{svg,png}`；`method-figure-semantic-brief.md` + `figures/ch4-method-flow.{svg,png}`；`verification.md`。
- 证据链闭合：`fact-matrix.md:17-31` 将公式、实现、metric、比较对象和禁止外推绑定到源；`chapter-blueprint.md:29-74,94-145` 将其落到 baseline、推导、复现、结果和边界；`algorithm-box.md:27-50` 与 `claim-and-citation-ledger.md:3-44` 分别冻结算法身份、复杂度和 claim/citation ceiling。未发现 truth 泄漏、metric signature 混用、state lifecycle 夸大或场景越界。
- 图件语义与可编辑性合格：两张 PNG 实际查看均无文字截断或错误箭头端点；结果图保持四格、B2/C4 主比较、B0/O1 上下文和零起点；方法图区分蓝色实线数据流与橙色点划控制流，未画 PDL/PMD/FIR/LDPC/CFO 等未验证模块。SVG 分别含 24/27 个 `<text>` 节点，尺寸为 `633.6×316.8 pt` 与 `620.244×287.064 pt`，保留矢量文本/形状；结果图 hatch 与方法图线型提供黑白区分。

## P2（局部视觉 / 措辞）

1. `generate_method_figure.py:65,74`：从缩放酉投影到解复用的橙色点划控制箭头实际穿过“可见诊断：rho=s1/s2；仅报告适用性，不驱动本章分支”文字，确认存在压字。修复建议：把诊断文字限制为 SVD 框下方的两行短文本并留出右侧控制流走廊，或将控制箭头改为绕开文字的折线路径；只局部重排，不改冻结标签与节点骨架。
2. `plot_ch4_results.py:195-198`：增益标注高度只按 `max(B2,C4)+0.0032` 计算，实际 PNG 中前三格文字落在更高的 B0 柱体上，降低局部清晰度。修复建议：标注高度改为四个已绘 arm 的全局柱顶最大值加固定余量，或使用统一轴坐标注释放在柱群上方；保持纵轴从 0 起和四格全展示。

`P0/P1/P2=0/0/2`
`verdict=PASS_WITH_P2`

## Fix re-review

- **P0=0**：在包目录 fresh 运行 `python plot_ch4_results.py --check-only`，exit code `0`，输出 `PASS: raw-only CSV/figure derivation matches D052/V027`。`plot_ch4_results.py:196-198` 仅改变标注的视觉高度计算，不改变 raw reducer、数值、metric 或身份；`generate_method_figure.py:65-66,74` 仅改变文字位置，不改变控制箭头源/目标或算法语义。
- **P1=0**：指定两处修改均保持原语义合同。`plot_ch4_results.py:196` 现在按四个已绘 arm 的实际柱顶取最大值；fresh `figures/ch4-ber-comparison.png` 中四个增益标注均与柱体分离，四格、零起点、B0/B2/C4/O1 和 hatch 均保留。`generate_method_figure.py:65-66,74` 将“可见诊断”移到左侧空白走廊并抬高“估计 W”；fresh `figures/ch4-method-flow.png` 中橙色点划控制箭头仍从缩放酉投影指向解复用，且不再压住任何文字。
- **P2=0**：原 P2-1（结果图标注压住 B0）与 P2-2（橙色控制箭头压住“可见诊断”）均已由上述 fresh PNG 视觉复核关闭；未见新增文字截断、箭头误接、黑白区分退化或局部重叠。

`remaining P0/P1/P2=0/0/0`
`verdict=PASS`
