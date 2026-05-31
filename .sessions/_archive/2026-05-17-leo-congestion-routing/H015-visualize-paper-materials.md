# Handoff: P2 可视化重做 + P3 论文叙事材料

> 来源: H014 | 交接目标: 实验完备性收尾完成，可进入正式论文写作
> 文件名: H015-visualize-paper-materials.md

## 已完成边界

### P2 可视化重做
- 重写 `visualize_results.py`：SciencePlots `science` 样式，600 DPI，统一配色
- 数据源全面更新为 surge=1.0 权威文件（batch_eval, e01_v2, training_curves_v2, mlp_generalization）
- 12 张图全部重生成，尺寸 ~6 英寸宽（A4 适配），无冗余标注，无图内标题

### P3 论文叙事材料
- 新增 `paper-materials.md`，包含：
  - 章节叙事大纲（A+B 框架：故障弹性+在线逐流+跨规模部署）
  - DTAR Related Work 讨论文本 + 粒度对比表
  - TELGEN 方法特性对比表 + 差异化论证逻辑
  - Baseline（ECMP/MLP/SP）讨论文本
  - 核心数据摘要表（4 张表供论文直接引用）
  - 图表规划（12 张→建议论文保留 6-8 张）

### P0/P1（上轮完成）
- 复杂度报告：GNN 28,546 参数，288 节点故障响应比 ECMP 快 7.7×
- 训练曲线：GNN 800ep final MLU=1.252, MLP=1.596, GNN/MLP=0.785
- MLP 泛化评估：GNN 在所有规模赢 MLP，MLP 跨规模崩溃

## 不要做什么

- 不要与 TELGEN 正面竞争 size gen 新颖性
- 不要硬补 DTAR/GMR baseline（粒度差异，Related work 讨论即可）
- 不要宣称"结构泛化"（是 Walker delta 族内 scale robustness）
- 不要改仿真器加轨道动力学（投入太大）
- 不要使用 universal claim

## 必读

1. `projects/leo-congestion-routing/paper-materials.md` — 论文叙事+竞品讨论+数据表
2. `projects/leo-congestion-routing/master-state.md` — 全局进度+自检结果
3. `projects/leo-congestion-routing/contract.md` — 已冻结 Contract
4. `projects/leo-congestion-routing/literature_notes.md` — 文献笔记
5. `.sessions/2026-05-17-leo-congestion-routing/topic-index.md` — 完整进展线索

## 下一轮

### 论文写作（主线路）
1. 按 paper-materials.md 叙事大纲展开正式章节
2. 12 张图精选 6-8 张（建议保留：核心对比、泛化曲线、故障消融、训练曲线、密集泛化、架构消融）
3. 如中文论文：图标签改为中文

### 可选补强（不阻断写作）
4. E10/E11 多 seed（<2% 差异，4-6h GPU）
5. E12 故障模式对比（可降级为未来工作）
