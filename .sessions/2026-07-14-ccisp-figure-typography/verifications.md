# Verifications — CCISP 五张论文图字体与排版统一

## V001: 五图最终论文尺寸字体与结构验收

> date: 2026-07-14
> 关联：S001 / D001

### 验证项

- [x] 最终有效字号：独立提取 `main.pdf` span → Fig.1 9.986/9.020 pt；Fig.2 10.010/8.974 pt；Fig.3–Fig.5 9.963/8.967 pt。
- [x] 字体嵌入：检查五图 PDF 与 `main.pdf` → 全部字体嵌入，无 Type 3、Helvetica、DejaVu Sans。
- [x] 科研语义：逐数组/阈值/场景/样式与 HEAD 对比 → 三张数据图语义不变，crossover 仍为 18.0129/16.8661/10.7026 dB。
- [x] draw.io 结构：对比 cell/edge ID、source/target、资产哈希 → Fig.1 64 cells/8 edges/7 assets，Fig.2 49 cells/17 edges，拓扑与资产不变。
- [x] 构建与页面：fresh `latexmk -g`、逐页渲染 7 页 → 无错误、undefined、overfull、裁切、重叠或不可读浮动。
- [x] 回归测试：运行 typography 与 Fig.2 结构测试 → 18 passed。

### 证据

```text
18 passed in 1.06s
main.pdf: 7 pages, 974686 bytes
mtime: 2026-07-14 22:33:05 +08:00
SHA-256: 9D2101AED83E4DB0D4185EDAB55684B2D27240DFAFF678060880C02FAAC682A8
build: exit 0
warnings: Underfull hbox badness 3000; Underfull hbox badness 2253
fonts: all embedded; no Type 3 / Helvetica / DejaVu Sans
independent verifier: typography gate PASS; P0/P1/P2 findings 0
```

### 结论

PASS

## V002: Fig.3 A2 视觉返工最终验收

> date: 2026-07-15
> 关联：S001 / D002

### 验证项

- [x] 权威源：仅修改 `plot_fig2_ber.py` 的视觉编码并覆盖当前 PDF/PNG，无 v2/v3 候选。
- [x] 语义冻结：数据数组、插值函数、六场景、HD-FEC 数值与 3×2 单栏结构未变。
- [x] A2 规格：三方法均为无标记实线；横轴主/次刻度加密；HD-FEC 仅在 (a) 直接标注；底部无框三列图例。
- [x] 字体嵌入：Fig.3 PDF 的 Times New Roman/STIX 全部嵌入，无 Type 3、Helvetica、DejaVu Sans。
- [x] 最终页面：fresh `latexmk -g` 生成 7 页 PDF；第 5 页 2× 渲染无裁切、遮挡、重叠或不可读文字。
- [x] 回归测试：`python -m pytest projects/simulation/tests/test_ccisp_figure_typography.py -q` → 14 passed。
- [x] 独立审查：规格符合性 PASS；代码/视觉质量 PASS；Critical/Important/Minor 均为 0。

### 证据

```text
14 passed in 1.58s
main.pdf: 7 pages, 968063 bytes
mtime: 2026-07-15 01:05:59 +08:00
SHA-256: FE2FAE71DA52E293DD2994F32851E6A20012CD3810A47CA42F561471FFF15C00
build: exit 0
warnings: Underfull vbox badness 10000 on page 2; no Fig.3 layout warning
fonts: all embedded; no Type 3 / Helvetica / DejaVu Sans
independent reviewer: spec PASS; quality PASS; findings 0
```

### 结论

PASS
