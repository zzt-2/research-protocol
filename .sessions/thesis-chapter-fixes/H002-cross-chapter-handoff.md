# Handoff: 三章交叉整理交接

> 来源: S004 | 交接目标: 新对话做跨章交叉整理（符号统一、叙事一致性、贡献差异化、剩余实验规划）
> 文件名: H002-cross-chapter-handoff.md

## 已完成边界

### Ch1（路由 Size Generalization）— P0 实验完成，paper-materials 待重写

**实验完成**：full/A1/A2/A3 各 3 seed，same 2 seed。脚本 `run_experiments.py`。

核心结果（3 seed 均值±std）：

| 实验 | Stretch | Delay(ms) | ≤1.2x% | 训练精度 |
|------|---------|-----------|--------|---------|
| full (主) | 1.099±0.012 | 66.84 | 86.2 | 97.5% |
| A1 (无PE) | 1.006±0.002 | 61.13 | 99.9 | 40.2%≈随机 |
| A2 (单尺度) | 1.106±0.018 | 67.66 | 84.0 | 97.7% |
| A3 (双消融) | 1.058±0.002 | 63.32 | 92.2 | 40.2%≈随机 |
| same (720→720) | 1.000±0.000 | 60.80 | 100.0 | 98.6% |

Delay retention = 66.84/60.80 = 109.9%（跨规模多 ~10% 延迟开销）

**领域验证结论**：
- Size generalization 是 GNN 理论问题，非 LEO 路由公认挑战 → 叙事改为"将 GNN 技术迁移到 LEO 路由"
- Stretch 合法但非主指标 → E2E delay 为主，stretch 为辅
- Delay retention rate 为自造指标 → 标注为新指标
- Orbital PE 是标准领域特征工程 → 降级为工程选择
- 加权 Dijkstra 有先例（GDDR 2021）→ 增量创新

**待补实验**：
- random_pe（~20 min）：`python -u run_experiments.py --seeds 123 42 0 --experiments random_pe`
- E06 hotspot（~30 min）、E08 GNN 深度（~1-2h）：P1 优先级，投期刊时需要

**结果文件**：`projects/leo-mega-constellation-gnn-routing/simulator/results/ch1_multi_seed_results.json`

### Ch2（切换 Size Generalization）— 审计完成，补实验待做

审计报告在 `.sessions/chapter-quality-audit/S003-ch2-audit.md`。
待补：多 seed + N=30/40 + 乒乓切换率。审计估 ~6h，但 Ch1 经验表明时间估计可能偏高 10x，需实测。

### Ch3（拥塞/故障弹性路由）— 全部完成

拓扑升级（Walker-Delta inc=86.4°）+ E01-E12 全量 GPU 重跑 + paper-materials 全面重写。
核心：GNN/ECMP delay=0.80, MLU=0.96, GNN/MLP delay=0.37。
质量：学位论文章节绰绰有余，投期刊需补 delay 敏感性分析 + DRL baseline。

## 不要做什么

- **不要相信子 agent 对论文内容的声称**：Li 2026 事件证明子 agent 会幻觉论文内容。任何"论文 X 做了 Y"的声称必须用 abstract 原文交叉验证
- **不要用审计的时间估计做计划**：Ch1 审计估 2h/seed 实测 6 min/seed。所有 GPU 时间估计必须先实测 1 seed 再推算
- **不要暗示 size generalization 是 LEO 路由领域的开放问题**：这是 GNN 理论问题，LEO 路由综述中不存在
- **不要把 Ch1 贡献说成方法论创新**：这是已知技术的工程应用验证（监督+Dijkstra+PE+多尺度），创新在于组合和场景

## 必读

按优先级排序：

1. `.sessions/thesis-chapter-fixes/topic-index.md` — 专题总控，已更新到最新
2. `.sessions/chapter-quality-audit/S005-cross-chapter.md` — 跨章汇总审计
3. `projects/leo-congestion-routing/paper-materials.md` — Ch3 论文素材（已重写）
4. `projects/leo-mega-constellation-gnn-routing/simulator/results/ch1_multi_seed_results.json` — Ch1 新实验数据
5. `.sessions/chapter-quality-audit/S002-ch1-audit.md` — Ch1 审计报告（P0-P2 修复清单）
6. `.sessions/chapter-quality-audit/S003-ch2-audit.md` — Ch2 审计报告

## 跨章整理具体任务

### 任务 1：符号统一表

三章使用不同的符号表示类似概念，需统一。S005 已识别 4 个 HIGH 冲突：
- 拓扑参数（P/S/F vs N）、特征维度、奖励函数、baseline 命名
- 建议以 Ch3（最新最完整）为基准，Ch1/Ch2 对齐

### 任务 2：拓扑差异声明

- Ch1/Ch2：inc=53° Walker-Delta（标准倾角，无极地间隙）
- Ch3：inc=86.4° Walker-Delta（近极地轨道，polar_gap_lat=70°）
- 差异原因：Ch3 需要极地间隙产生拓扑不对称以测试故障弹性
- 论文中需显式声明并解释差异原因

### 任务 3：贡献差异化

S005 判定 CONDITIONAL PASS，需加强：
- Ch1：零样本规模泛化（静态拓扑，监督学习）
- Ch2：零样本规模泛化（动态切换场景，DRL）
- Ch3：拥塞/故障弹性路由（在线自适应，PPO）
- 统一叙事："GNN 结构化编码使零样本规模迁移成为可能"（不变量）

### 任务 4：Ch1 paper-materials 重写

基于 3-seed 数据 + 领域验证结论重写。关键叙事调整：
- E2E delay 为主指标，stretch 为辅助
- Size generalization 定位为"从 GNN 理论迁移到 LEO 路由"
- Delay retention rate 标注为新提出的指标
- Orbital PE 定位为工程选择而非核心贡献
- 720 星不称"mega-constellation"（改称"OneWeb 规模"），强调 11x 泛化倍数

### 任务 5：Ch2 补实验 + paper-materials

先实测 1 seed 确认实际耗时，再决定补实验范围。

## 关键教训（跨对话有效）

| 教训 | 触发事件 | 如何避免 |
|------|---------|---------|
| 子 agent 会幻觉论文内容 | Li 2026 被声称做 size generalization，实际是意图编译 | 任何论文声称必须用 abstract 原文交叉验证 |
| 审计时间估计不可信 | Ch1 估 2h/seed 实测 6 min | 先跑 1 seed 实测再推算总量 |
| 指标子领域归属要验证 | Ch3 MLU ratio 是互联网 TE 指标非 LEO 路由 | 每个核心指标查 ≥5 篇同子领域论文确认 |
| 问题定位要诚实 | Ch1 size gen 不是 LEO 领域开放问题 | 查领域综述确认问题是否被列出 |

## 接口变更

- 新增 `projects/leo-mega-constellation-gnn-routing/run_experiments.py`：支持 6 种实验 × 多 seed 批量运行

## 失败数据附录

- Li 2026 竞品误报：3 个子 agent 中有 1 个幻觉了"零样本跨星座泛化"，实际论文做意图编译，GNN 仅用于同规模 Dijkstra 蒸馏加速。Abstract 中无 size generalization / zero-shot transfer 关键词。根因：子 agent 基于 GNN+Dijkstra+LEO 的表面相似性推断功能。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Ch1 random_pe 未跑 | 消融完整性 | 0/3 seed | 论文写作前补跑（~20 min） |
| Ch1 E06/E08 未跑 | 实验完备性 | 未启动 | 投期刊时补（学位论文可选） |
| Ch2 补实验未做 | 统计严谨性 | 审计完成 | 下一个 GPU 时间窗口 |
| Ch1 paper-materials 未更新 | 数据一致性 | 仍是旧单 seed 数据 | 交叉整理时重写 |
| Ch3 DRL baseline 未复现 | Baseline 完整性 | P2 可选 | 投期刊时补 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| Ch1 多 seed 稳定性 | stretch std < 0.05 | 实测 std=0.012 ✅ |
| Ch1 消融逻辑 | A1≈Dijkstra, A2>full, same=1.0 | 实测全部自洽 ✅ |
| 跨章符号一致性 | 4 个 HIGH 冲突归零 | S005 审计标准 |
| 拓扑差异声明 | 三章拓扑参数有明确文档 | S005 审计标准 |

## 接收方验证

- [x] 已读取 topic-index 的不变量段落
- [x] 已验证 Ch1 实验数据（ch1_multi_seed_results.json 存在且包含 14 轮结果）
- [x] 已确认 Li 2026 非竞品（用户亲自读 abstract 确认）
- [x] 已确认当前范围：交叉整理 + Ch1 paper-materials + Ch2 补实验

## 下一轮

1. 读取 topic-index + 本交接文档
2. 先补跑 random_pe（~20 min，验证论证关键）
3. 重写 Ch1 paper-materials（3-seed 数据 + 领域验证叙事调整）
4. Ch2 先实测 1 seed 确认耗时
5. 跨章符号统一表 + 拓扑差异声明 + 贡献差异化
