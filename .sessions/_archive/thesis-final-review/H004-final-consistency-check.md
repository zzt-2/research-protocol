# Handoff: 最终一致性检查

> 来源: S013 | 交接目标: 三章论文最终一致性检查 + 开题准备
> 文件名: H004-final-consistency-check.md

## 已完成边界

1. **三章终审全部完成**：S001-S013（13 个对话，~40 个子 agent）
2. **所有 P0 已修复**：Ch1(4项)、Ch2(3项)、Ch3(4项)
3. **统计补充完成**：三章 stat_tests.json 均已生成
4. **元分析框架确定**："探索性分化"（S012 决策）

## ⚠️ 关键警告（必须首先阅读）

**S001-S011 中的"Ch3"全部指 hgat-satellite-dag-offloading（已废弃）。只有 S012-S013 中的 Ch3 指 leo-congestion-routing。**

具体影响：
- S001-S011 的 Ch3 结论（结论 #2/#4/#9/#11/#12/#22/#23/#28/#30/#34/#36-#38）全部针对 hgat，**不适用于当前 Ch3**
- S011 的 18 项公式修正针对 hgat，**不适用于 leo-congestion-routing**
- 结论 #39-#45（符号冲突/公式修正）中的 Ch3 相关修正也针对 hgat
- 结论 #46-#61 是 S012-S013 的，适用于当前 Ch3(leo-congestion-routing)

## 三章项目映射

| 章节 | 项目目录 | paper-materials 位置 | 符号文件 |
|------|---------|---------------------|---------|
| Ch1 | `projects/leo-mega-constellation-gnn-routing/` | `paper_materials/` 目录（01-06 分文件） | `paper_materials/06_formulas_symbols.md` ✅ |
| Ch2 | `projects/leo-ntn-handover-drl/` | `paper_materials/` 目录（01-06 分文件） | `paper_materials/06_formulas_symbols.md` ✅ |
| Ch3 | `projects/leo-congestion-routing/` | `paper-materials.md`（单文件） | **缺失**（P1-10：需创建） |

## 不要做什么

1. **不要把 S001-S011 的 Ch3(hgat) 结论应用到 leo-congestion-routing**——上面警告已说明
2. **不要重新跑实验**——三章数据均已完成，stat_tests 均已生成
3. **不要质疑 Ch3 = leo-congestion-routing 的决策**——S012 已决策，基于 H002 六维度对比
4. **不要处理 P1/P2 项**——这些属于写作阶段

## 必读（按优先级）

### 交接文件
1. `.sessions/thesis-final-review/topic-index.md` — 完整终审结论索引（注意上述警告）
2. 本文件（H004）

### 三章核心数据
3. `projects/leo-mega-constellation-gnn-routing/paper_materials/03_experiments.md` — Ch1 实验结果
4. `projects/leo-ntn-handover-drl/paper_materials/03_experiments.md` — Ch2 实验结果
5. `projects/leo-congestion-routing/paper-materials.md` — Ch3 实验结果（单文件，含 Tables 1-8）

### 符号/公式
6. `projects/leo-mega-constellation-gnn-routing/paper_materials/06_formulas_symbols.md` — Ch1 符号
7. `projects/leo-ntn-handover-drl/paper_materials/06_formulas_symbols.md` — Ch2 符号
8. Ch3 无此文件（P1-10 待创建）

### 跨章相关
9. `.sessions/thesis-final-review/S011-cross-chapter-unification.md` — 符号统一+元分析框架（注意：Ch3 部分需按 leo-congestion-routing 重新评估）
10. `.sessions/thesis-final-review/S013-ch3-congestion-routing-full-review.md` — Ch3 终审完整记录

## 验证阈值

| 验证项 | PASS 标准 |
|--------|----------|
| 三章星座参数 | alt=550km 一致；inclination 差异(53° vs 86.4°)有说明 |
| 主指标一致性 | 三章主指标定义清晰无矛盾 |
| 符号冲突 | $N$, $h$, $B$, $H$ 等多义符号已区分 |
| 跨章叙事 | "探索性分化"框架三章适配无矛盾 |
| 数据来源 | 三章 stat_tests.json 均存在且数值与 paper-materials 一致 |

## 接收方验证

- [ ] 已阅读"关键警告"段落
- [ ] 已确认三章项目路径映射
- [ ] 已读取 topic-index.md 的不变量段落
- [ ] 已确认 Ch3 = leo-congestion-routing（非 hgat）

## 下一轮

### 对话14：最终一致性检查

检查维度：
1. **参数一致性**：三章星座参数（alt/inc/容量/流量）交叉对比
2. **指标一致性**：三章主指标/辅助指标定义是否矛盾
3. **符号一致性**：多义符号（$N$, $h$, $B$, $H$, $L$）跨章冲突是否已解决
4. **叙事一致性**：元分析框架"探索性分化"是否三章适配
5. **数据完整性**：stat_tests.json 与 paper-materials 数值最终核对
6. **Ch1/Ch3 隔离验证**：确认两章路由贡献无重叠

### 之后：开题报告

- 输入：~15-20 个精选文件（literature_notes + paper_materials + 终审结论）
- 用 thesis-platform 预处理工作流 → 写作工作流产出
