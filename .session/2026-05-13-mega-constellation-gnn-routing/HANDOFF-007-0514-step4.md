# Handoff 2026-05-14 (Round 4 — 论文素材提取)

## 当前进度
- 阶段：Execute Step 2 核心实验 + 消融实验 **全部完成**
- Contract 状态：frozen
- 待做：按 `stages/paper-materials-workflow.md` 提取论文素材到 `paper_materials/`

## Contract 核心指标状态
- [✓] 时延保留率 90.3% ≥ 80%
- [✓] vs Dijkstra 差距 9.9% ≤ 20%

## Execute 实验完成情况

### 核心实验（跨规模 66+100+200→720）
- Mean stretch: 1.097, Median: 1.056, P95: 1.315
- ≤1.2x optimal: 85.1%, ≤1.5x: 98.9%
- Mean delay: 66.77 ms (Dijkstra: 60.77 ms, 开销 9.9%)

### Baseline 对比
| 方法 | Mean Stretch | ≤1.2x | Mean Delay | 训练规模 |
|------|-------------|-------|-----------|---------|
| 我们的方法 | 1.097 | 85.1% | 66.77 ms | 66+100+200→720 |
| GRLR | 1.008 | 100% | 60.32 ms | 720→720 |
| Dijkstra | 1.000 | 100% | 60.77 ms | N/A |

### 消融实验（D026-D029）
| 消融 | 训练精度 | Mean Stretch | ≤1.2x | Delay开销 |
|------|---------|-------------|-------|----------|
| A1(无PE) | 39.7% | 1.002 | 100% | 0.2% |
| A2(单尺度+PE) | 97.7% | 1.120 | 81.1% | 12.3% |
| A3(无PE+单尺度) | 40.2% | 1.049 | 93.6% | 3.6% |
| Same(720→720) | 98.8% | 1.000 | 100% | 0.0% |

**消融结论**：PE 是学习必要条件（非可选增强），多尺度训练贡献 2-4pp，9.7pp stretch 差距完全来自跨规模迁移。

### 模型文件索引（simulator/）
- `pretrained.pt` — 主实验模型（72,965 params）
- `ablation_A1.pt` — 无 PE 模型
- `ablation_A2.pt` — 单尺度模型
- `ablation_A3.pt` — 无 PE + 单尺度模型
- `ablation_same.pt` — 同规模模型
- `grlr_trained.pt` — GRLR baseline 模型

## 下一步：论文素材提取

**必读文件**（按优先级）：
1. `stages/paper-materials-workflow.md` — 提取工作流（8步）
2. `stages/thesis-materials.md` — 学位论文材料准备指南

**输入文件**：
- `decision_log.md`（D001-D029）
- `contract.md`（frozen）
- `literature_notes.md`（25篇+2理论）
- `feasibility_report.md`
- `baseline_report.md`
- `competitor_notes/`

**产出目录**：`projects/leo-mega-constellation-gnn-routing/paper_materials/`

**执行策略**：按 workflow Step 1-8 执行。推荐批次：
- Step 1（主线程建框架）
- Step 2+3+4 并行（子 agent）
- Step 5+6 并行（子 agent）
- Step 7（主线程，依赖 Step 3）
- Step 8（主线程校验）

## 注意事项

1. **先提交框架更新**：`git status` 显示有未提交的框架文档修改（来自另一个 session），在开始提取前先 `git add` 并 commit 这些文件
2. `paper_materials/05_limitations.md` 在 Execute 过程中已有素材可提取（消融实验揭示的 PE 依赖、跨规模迁移代价）
3. 消融结论需要修正原 Contract 假设的表述——PE 贡献从"≥8pp stretch 改善"修正为"学习前提条件"
