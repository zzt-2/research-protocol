# 任务：讨论三章 paper-materials 重新提取工作流

## 背景

学位论文三章终审（14 轮对话，~40 个子 agent）已全部完成。发现三章 paper-materials 均约两周前提取，未反映终审大量更新，需全部重做。

## 第一步：先看提取工作流

读 `/home/zzt/code/thesis-platform/.sessions/2026-05-20-material-preprocessing-workflow` 下的文件，了解两星期前的提取工作流设计。评估它是否仍适用，需要哪些调整。

## 三章当前状态

| 章 | 项目目录 | paper-materials 现状 |
|---|---------|-------------------|
| Ch1 | `projects/leo-mega-constellation-gnn-routing/` | `paper_materials/01-06` 分文件（6个，共~116K），内容过时 |
| Ch2 | `projects/leo-ntn-handover-drl/` | `paper_materials/01-06` 分文件（6个，共~97K），内容过时 |
| Ch3 | `projects/leo-congestion-routing/` | 单文件 `paper-materials.md`（22K），**从未按 01-06 拆分** |

## 未反映的更新（两周内的 14 轮终审产出）

### 全局性更新（影响三章）
- 元分析框架："探索性分化"（GNN 有效性取决于架构复杂度与任务需求匹配）
- 符号统一：7 类冲突 + 18 项公式修正（$N$→$N_{\text{sat}}$/$N_{\text{UE}}$/$N_{\text{node}}$ 等）
- 两种规模泛化命名：星座规模泛化(Ch1) vs 用户规模泛化(Ch2)
- 写法规范：18 篇硕博论文精读 → 贡献声称降级模板、局限性写法、统计惯例
- 统计补充：三章 stat_tests.json 已生成（bootstrap CI + Welch's t-test）
- 贡献定位校准：Ch1"系统性验证"、Ch2"规模适应性实证"、Ch3"故障弹性"

### Ch1 特有更新
- 3-seed 数据替换旧单 seed（stretch 1.083±0.015, delay 65.92±1.01）
- 领域验证：size generalization 是 GNN 理论问题非 LEO 路由公认挑战
- 贡献降级："首次创新"→"系统性验证+实证"
- 竞品补充：5 篇低威胁新论文，Li 2026 排除（非竞品）
- 消融故事：PE 是学习前提（非增强），多尺度贡献 2.3pp

### Ch2 特有更新
- eps_decay=5→20 修复：旧数据不可靠（固定 episode seed=单场景记忆）
- 同规模 50UE GNN +21.2% vs MLP (p=0.007)，20UE 持平 (p=0.76)
- Size gen：20→50 retention 218%, 20→100 retention 340%（GNN std 36.9% vs MLP 102.3%）
- 竞品：Xie 2023 + Yin 2022 先例需引用限定
- Lee & Lim 2025 为最直接竞争者（修正旧标记"非二部图"→实际用二部图）
- Jain's fairness 降级（通行率仅 17%），补 system throughput

### Ch3 特有（项目从 hgat 替换为 leo-congestion-routing）
- Ch3 = `leo-congestion-routing`（非 hgat-satellite-dag-offloading）
- 物理仿真拓扑：alt=550km, inc=86.4°, polar_gap_lat=70°
- 核心发现：故障是 GNN 优势激活条件（无故障 GNN≈ECMP，8%故障 delay -20%）
- E2E delay = 传播延迟 × 拥塞惩罚权重 1/(1-util)（非 M/M/1 排队）
- 跨规模：0.7x-4.4x 有效（delay 优势 17%-75%），10.9x 退化
- GNN vs ECMP MLU 不显著(p=0.26)，delay -20% 显著
- 合规 6/8 PASS，竞品 3 个空白仍成立

## 需要讨论的问题

1. **工作流是否适用**：两周前的提取流程是否需要调整？输入源有哪些变化？
2. **01-06 格式是否仍然合适**：Ch3 需要补齐，但 Ch1/Ch2 的拆分粒度是否合理？
3. **输入源清单**：每章提取时应该读哪些文件作为输入？
4. **跨章统一**：符号表、元分析框架、延迟模型差异如何嵌入各章？
5. **优先级**：三章并行还是顺序？先做哪章？

## 必读文件（按优先级）

1. `/home/zzt/code/thesis-platform/.sessions/2026-05-20-material-preprocessing-workflow/` — 旧提取工作流（**先读这个**）
2. `.sessions/thesis-final-review/topic-index.md` — 终审完整结论索引（61 条结论 + 不变量）
3. `.sessions/thesis-final-review/S014-final-consistency-check.md` — 一致性检查结果 + paper-materials 过时详情
4. `.sessions/thesis-final-review/S011-cross-chapter-unification.md` — 符号统一 + 元分析框架（⚠️ Ch3 部分是旧 hgat，以 S013 为准）
5. `.sessions/thesis-structure-research/R003-writing-norms-contribution-claims.md` — 写法规范（贡献声称模板）
6. `projects-overview.md` — 三章总览
