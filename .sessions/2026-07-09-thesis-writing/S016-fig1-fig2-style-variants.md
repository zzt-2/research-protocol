# [S016] Fig.1/Fig.2 三版 draw.io 风格候选预览

> 2026-07-13 | 视觉候选阶段 | 已完成（结构不足，转 S017）

## 目标

把 D013 的 draw.io 编辑源路线落实为每张图三种可比较版式，并用不放表格的纵向 Markdown 预览交给用户挑选；本文件不是最终论文图，也不替用户决定风格。

## 记录

### 通过门

- Fig.1 v2a/v2b/v2c 与 Fig.2 v2a/v2b/v2c 共六版均通过独立视觉复核。
- 六份 draw.io 源可解析，六份 SVG 可解析；PNG 均为 2148 px 宽，Fig.1 为约 7.16 × 2.5 in，Fig.2 为约 7.16 × 3.53 in，未见边缘裁切。
- Fig.2 三版的 control rail 与 selected-estimate 交叉处均加入可编辑的白色 bridge mask；复核确认读作跨越而非 junction。
- 预览逐张独占一段，不放进 Markdown 表格；每张图下方同时给出 PNG、draw.io 和 SVG 链接。

### Fig.1 候选

#### Fig.1-A — 极简期刊链

强调 Tx → FSO channel → Coherent Rx → Adaptive CPR → Common downstream DSP 的单一主链；CPR 用局部加重，Fig. 2 作为弱关联入口。

![Fig.1-A：极简期刊链](../../projects/simulation/figures/fig1_system_overview_v2a.png)

[打开 PNG](../../projects/simulation/figures/fig1_system_overview_v2a.png) · [draw.io 源](../../projects/simulation/figures/fig1_system_overview_v2a.drawio) · [SVG](../../projects/simulation/figures/fig1_system_overview_v2a.svg)

#### Fig.1-B — receiver-side shell

用右侧虚线 shell 把 Coherent Rx、Adaptive CPR 和 downstream DSP 组成接收机侧局部系统；CPR 入口更突出。左上孤立残线已删除。

![Fig.1-B：receiver-side shell](../../projects/simulation/figures/fig1_system_overview_v2b.png)

[打开 PNG](../../projects/simulation/figures/fig1_system_overview_v2b.png) · [draw.io 源](../../projects/simulation/figures/fig1_system_overview_v2b.drawio) · [SVG](../../projects/simulation/figures/fig1_system_overview_v2b.svg)

#### Fig.1-C — signal ribbon / raw spine

用浅色 signal ribbon 作为主数据骨架，模块边框减弱，Adaptive CPR 保持唯一强视觉焦点；ribbon 只承担视觉骨架，深蓝箭头才是数据路径。

![Fig.1-C：signal ribbon / raw spine](../../projects/simulation/figures/fig1_system_overview_v2c.png)

[打开 PNG](../../projects/simulation/figures/fig1_system_overview_v2c.png) · [draw.io 源](../../projects/simulation/figures/fig1_system_overview_v2c.drawio) · [SVG](../../projects/simulation/figures/fig1_system_overview_v2c.svg)

### Fig.2 候选

#### Fig.2-A — shared-column / three-lane

最明确地分出 phase-estimate、data、control 三条横向带；DA/NDA 共用列锚点，适合强调并行估计器与统一后级。

![Fig.2-A：shared-column / three-lane](../../projects/simulation/figures/fig2_adaptive_cpr_v2a.png)

[打开 PNG](../../projects/simulation/figures/fig2_adaptive_cpr_v2a.png) · [draw.io 源](../../projects/simulation/figures/fig2_adaptive_cpr_v2a.drawio) · [SVG](../../projects/simulation/figures/fig2_adaptive_cpr_v2a.svg)

#### Fig.2-B — hub-and-spoke

以 Estimator selector 为中心 hub，DA/NDA 对称汇入；Fixed SNR threshold 紧邻 selector 下方，控制线从右侧回接。

![Fig.2-B：hub-and-spoke](../../projects/simulation/figures/fig2_adaptive_cpr_v2b.png)

[打开 PNG](../../projects/simulation/figures/fig2_adaptive_cpr_v2b.png) · [draw.io 源](../../projects/simulation/figures/fig2_adaptive_cpr_v2b.drawio) · [SVG](../../projects/simulation/figures/fig2_adaptive_cpr_v2b.svg)

#### Fig.2-C — staged pipeline / control side rail

把 DA/NDA 放入 candidate grouping 容器，形成阶段式 pipeline；右侧 control side rail 更像机制图，但局部标签间距比 A/B 紧。

![Fig.2-C：staged pipeline / control side rail](../../projects/simulation/figures/fig2_adaptive_cpr_v2c.png)

[打开 PNG](../../projects/simulation/figures/fig2_adaptive_cpr_v2c.png) · [draw.io 源](../../projects/simulation/figures/fig2_adaptive_cpr_v2c.drawio) · [SVG](../../projects/simulation/figures/fig2_adaptive_cpr_v2c.svg)

### 当前结论

六版都已过 Gate A/视觉门，没有需要阻断选择的硬问题。差异现在主要是信息层级的表达偏好：Fig.1 选“主链极简 / 接收机外壳 / signal ribbon”之一，Fig.2 选“三带共享列 / 中心 hub / 阶段式容器”之一。

## 决策引用

- D013：draw.io 作为编辑源，SVG/PDF 作为交付格式。
- D015：恢复三版候选与独立视觉复核（新建）。
- R020/R022：视觉语法、语义不变量与缩小验收门。

## 范围确认

- 本轮是否在 scope boundary 内：是。只完成 Fig.1/Fig.2 候选预览与独立验收；不跑实验、不进 Contract、不改正式正文或 Fig.3--5。

## 后续

本轮三版仅作为结构不足的对照样本保留，不再要求用户从中选择；后续以 S017/D016 的 v3 单原型为新底稿。
