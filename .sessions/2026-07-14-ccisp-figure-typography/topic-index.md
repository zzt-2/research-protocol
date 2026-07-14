# Topic Index: CCISP 五张论文图字体与排版统一

> slug: 2026-07-14-ccisp-figure-typography
> status: closed | created 2026-07-14 | last_updated 2026-07-14

## 专题定位（一句话）

在不改变任何科研语义的前提下，使 Fig.1–Fig.5 在最终 IEEEtran 双栏 PDF 中形成以正文 10 pt Times 系字体为锚点的统一排版体系。

## 范围边界

### 原始目标（冻结）

只统一 Fig.1–Fig.5 的字体、数学排版、字号层级和最终嵌入尺寸下的图内排版，并完成 fresh PDF 与独立验证。

### 当前范围

- 审计 fresh `main.pdf` 中五图的字体、嵌入、有效字号、裁切与可读性。
- 修改三张 Matplotlib 绘图脚本的字体配置、字号、子图排布、边距和导出参数。
- 局部修改 Fig.1/Fig.2 draw.io 的字体层级与数学标签排版；用户手调后的 draw.io 是唯一编辑源。
- 从同一权威源重导 PDF/PNG，并在当前 LaTeX 嵌入尺寸下验证。

### 明确不含

- 不修改数据、结果 JSON、曲线点、插值算法、crossover 判定、阈值、图例语义或线型含义。
- 不增删 Fig.1/Fig.2 节点，不改节点 ID、语义、连接、控制逻辑、技术图元或论文论点；允许字体排版所需的标签/容器几何微调。
- 不运行、恢复或重建 Fig.1 的历史 builder；不运行会改写嵌入资产的旧脚本。
- 不修改论文正文、caption、数字、公式语义或引用。
- 不创建或保留新的 v2/v3 图形候选文件。

### 范围变更记录

- 无。

## 已确认结论

### 不变量

1. 字体验收以最终 PDF 中的有效字号为准，不以 Matplotlib/draw.io 源字号为准。
2. IEEEtran 当前正文为 10 pt；子图标题、坐标轴标题和 Fig.1/Fig.2 主节点文字以最终有效 10 pt 为锚点，次级文字不得低于 8 pt。
3. 普通文字使用 Times New Roman 或可靠的 Times-compatible serif；数学使用 STIX/Times-compatible 数学排版，不能用普通 Times 文本冒充公式。
4. PDF 字体必须嵌入，不得混入 Helvetica、DejaVu Sans 或 Type 3。
5. Fig.5 也纳入统一修改和验证，但保持单栏结构与数据语义。

### 其他结论

- Fig.3/Fig.4 当前宽图缩入单栏导致有效字号约 4.2–4.5 pt，是本轮首要排版缺陷。
- 优先保持当前单栏嵌入位置，通过原生单栏排版解决可读性；若无法在不破坏图义的情况下达到契约，则停止并回报，不擅自改双栏。

## 进展线索

- **S001**：完成五图基线审计、字体契约、权威源修改、稳定 PDF/PNG 重导、fresh 论文构建与独立验证；V001 为 PASS。

## 未决项

- 无。

## 当前位置

当前位置：CLOSED。最终 `main.pdf` 五图 typography gate 已由独立 verifier 判定 PASS；正文并发修改及其论点/指标一致性不属于本专题。
