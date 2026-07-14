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
