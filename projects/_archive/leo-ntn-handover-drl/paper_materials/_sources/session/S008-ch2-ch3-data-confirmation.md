# [S008] Ch2+Ch3 数据确认 + 技术修复 + 统计补充

> 2026-05-26 | Phase 3 | 完成

## 目标

对话 8: Ch2+Ch3 全量数据溯源、合规检查、技术问题修复、统计指标补充、可视化图生成。

## 记录

### 子 agent 执行摘要

3 批共 7 个子 agent 并行执行。

### Batch 1 (3 agents): 数据验证

| # | 任务 | 状态 | 关键结论 |
|---|------|------|---------|
| 7a+7b | Ch2 全量数据溯源 + 旧数据检查 | CONDITIONAL PASS | 12 个 d20 数据全部一致; E4-100-c25 用 eps_decay=5 但 paper 已正确标记 |
| 7c+7d | Ch3 公平性 + 零样本叙事 | PASS / 需补充 | homo 调参合理; 零样本失败推荐在 limitations 讨论 |
| P0/P1 | 技术问题修复方案确认 | 部分已修 | P0-3/P1-1 已修(对话4); P0-4/P1-2/P1-3 需修 |

### Batch 2 (3 agents): 合规 + 统计 + K1 DOI

| # | 任务 | 状态 | 关键结论 |
|---|------|------|---------|
| 7e | Ch2/Ch3 合规 checklist | 完成 | Ch2: 7/7 PASS; Ch3: 2/8 PASS, 4 FAIL |
| 7f | bootstrap CI + Welch's t-test | 完成 | 三章 stat_tests.json 已保存; Ch2 20UE 不显著(p=0.76), 50UE 显著(p=0.007) |
| K1 DOI | 核实 K1 与 M06 关系 | 完成 | K1=M06 同一论文(早期访问 vs 正式版), 已添加说明 |

### Batch 3 (1 agent): 可视化

5 张图生成到 `projects/thesis-figures/`:
- fig_ch1_method_comparison.pdf/png
- fig_ch2_blocking_rate.pdf/png
- fig_ch2_size_generalization.pdf/png
- fig_ch3_reward_comparison.pdf/png
- fig_ch1_ablation.pdf/png

### 技术修复 (7h)

| 问题 | 状态 | 修复内容 |
|------|------|---------|
| P0-1 noise_power | RESOLVED | K2/M01 原文也用 -100dBm 统一，无需改代码 |
| P0-2 antenna_gain | 文档标注 | G2S 直连被 UAV 中继自然规避 |
| P0-3 Ch2 retention | 已修(对话4) | — |
| P0-4 Ch1 retention 方向 | **本对话修复** | run_experiments.py:400 full/same → same/full |
| P1-1 Ch2 eps-greedy | 已修(对话4) | — |
| P1-2 Ch1 边特征 | **本对话修复** | 03_experiments.md: utilization → dist(2处) |
| P1-3 Ch1 注意力公式 | **本对话修复** | 06_formulas:65 分母 [Wh_w‖Wh_v] → [Wh_u‖Wh_w] |
| K1 DOI | **本对话修复** | literature_notes K1 条目添加 M06 DOI 说明 |

### 关键统计发现

**Ch1**:
- Full vs Same stretch: t=7.62, p=0.017 ✅ 显著
- Full vs A1(无PE): t=6.98, p=0.018 ✅ 显著
- Full vs A2(单尺度): t=-1.52, p=0.203 ❌ 不显著
- Full vs A3(无PE+单尺度): t=2.23, p=0.153 ❌ 不显著

**Ch2**:
- 20UE GNN vs MLP reward: t=-0.33, p=0.759 ❌ 不显著
- 50UE GNN vs MLP reward: t=6.16, p=0.007 ✅ 显著
- 50UE GNN vs MLP blocking: t=-8.18, p=0.001 ✅ 显著

**Ch3**:
- 训练不稳定严重：多数 GNN 模型仅 3 episodes
- HGAT seed42 有 80 episodes，seed123 有 44 episodes

## 决策引用

- 无新决策

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

- **Ch3 遗留 4 项 FAIL**: 多指标分拆、DAG 拓扑变体、环境扫描、统计报告完整
- **Ch3 训练不稳定**: 需排查原因并重跑
- **Ch2 20UE GNN vs MLP 不显著**: 论文叙事需侧重 50UE 规模差异和 size gen 稳定性
- **对话 9**: 跨章符号统一 + 元分析框架
- **对话 10**: 最终一致性检查
