# Handoff: Ch2 领域归属验证

> 来源: S005-cross-chapter + 本轮文档审查 | 交接目标: 新对话做 Ch2 领域验证（与 Ch1/Ch3 同等深度）
> 文件名: H003-ch2-domain-verify.md

## 已完成边界

### 三章文档全面审查 + 更新（本轮）

派 24 个子 agent 交叉审查三章全部文档（对话历史、项目文档、代码/结果、专题日志、根目录文档），然后派 9 个 executor 更新了 13 个文件。修复了：
- Ch1 JSON 结果文件不完整（从日志重建）
- Ch1 master-state 事实错误（GraphSAGE→GAT）
- Ch1 JSON 缺逐流数据（去掉脚本过滤，重跑 full×3seed 获取 per_flow_stretches + loss_history）
- Ch3 四个文档基于旧拓扑（全部更新为 Walker-Delta 物理仿真）
- 审计专题修复状态标注不准

### Ch1 领域验证（S004）方法论

Ch1 做了完整的领域归属验证，方法论可复用：

1. **问题归属验证**：查 LEO 路由领域综述，确认 size generalization 是否被列为该领域的开放问题 → 结论：是 GNN 理论问题，不是 LEO 路由领域公认的挑战
2. **指标归属验证**：查 ≥5 篇同子领域论文，确认所用指标是否为领域通行指标 → 结论：stretch 合法但非主指标，E2E delay 为主
3. **自造指标标注**：delay retention rate 无文献先例 → 标注为新提出的指标
4. **技术先例检查**：orbital PE 是标准领域特征工程，加权 Dijkstra 有先例（GDDR 2021）
5. **竞品排除**：Li 2026 子 agent 幻觉，实际做意图编译（教训：任何论文声称必须用 abstract 交叉验证）

### Ch3 指标归属验证

- MLU ratio 是互联网 TE 指标，LEO 路由领域主流用 E2E delay、throughput、CV
- 叙事已从 MLU 转为 delay 为主

## Ch2 待验证问题清单

### 问题 1：LEO 切换领域是否将"跨规模泛化"列为挑战？

- Ch1 已确认 size generalization 是 GNN 理论问题
- Ch2 的切换场景下，"跨规模泛化"（从 20UE 泛化到 100UE）是否有切换领域的文献支持？
- 需查：LEO handover / NTN handover 领域综述，看是否列出此问题
- 影响叙事定位：可能也需要改为"跨领域技术迁移"

### 问题 2：top-K 动作压缩是否为领域标准做法？

- Ch2 使用 top-K 动作压缩（从连续/大动作空间压缩到 top-K 个候选）
- 这在 DRL 切换领域是否有先例？
- 影响贡献定位：如果是标准做法则降级为工程选择

### 问题 3：二部图 GNN 建模切换是否有文献基础？

- Ch2 用二部图（用户节点 + 卫星节点）建模切换问题
- 这种建模方式在切换领域是否有文献先例？
- 影响新颖性判断

### 问题 4：所用指标是否为切换领域通行指标？

- Ch2 使用 reward、切换次数、Jain's fairness 等
- 需查 ≥5 篇 LEO/NTN 切换论文确认指标是否主流
- Jain's fairness 在切换领域是否标准？还是网络资源分配领域的指标？

### 问题 5：DDQN 用于切换的先例

- Ch2 用 DDQN（Double Deep Q-Network）
- LEO 切换领域用 DRL 的先例很多，但 DDQN 具体是否有？
- 影响方法选择的新颖性论证

### 问题 6：切换率/掉话率等关键指标

- LEO 切换领域的核心指标通常是：切换率(handover rate)、掉话率(call drop rate)、ping-pong rate
- Ch2 是否覆盖了这些？是否有缺失的核心指标？

## 必读

1. `.sessions/chapter-quality-audit/S003-ch2-audit.md` — Ch2 审计报告（指标完整性 FAIL）
2. `projects/leo-ntn-handover-drl/decision_log.md` — Ch2 决策记录（D001-D034）
3. `projects/leo-ntn-handover-drl/master-state.md` — Ch2 当前状态
4. `projects/leo-ntn-handover-drl/contract.md` — Ch2 Contract 冻结版本（假设和指标定义）
5. `.sessions/thesis-chapter-fixes/S004-ch1-domain-verify` 相关内容 — Ch1 领域验证方法论参考（在 topic-index.md 的进展线索中）
6. `projects/leo-ntn-handover-drl/literature_notes.md` — Ch2 文献笔记
7. `projects/leo-ntn-handover-drl/paper-materials/` — Ch2 论文素材（6 个文件）

## 不要做什么

- **不要相信子 agent 对论文内容的声称**：Li 2026 事件证明子 agent 会幻觉论文内容。任何"论文 X 做了 Y"必须用 abstract 原文交叉验证
- **不要把 Ch1 的结论直接套用到 Ch2**：Ch1 的问题是"size gen 不是 LEO 路由问题"，但 Ch2 的切换场景可能不同，需要独立验证
- **不要跳过指标验证**：Ch3 MLU ratio 事件证明每个核心指标都要查 ≥5 篇同子领域论文确认

## 验证方法（复用 Ch1）

1. 派 3 个子 agent 并行调研：
   - Agent A: LEO/NTO handover 领域综述 → 确认"跨规模泛化"是否被列出
   - Agent B: 切换领域指标调研 → 查 ≥5 篇论文确认指标通行性
   - Agent C: 技术先例调研 → 二部图 GNN、top-K 压缩、DDQN 在切换领域的先例
2. 每个子 agent 返回 ≤500 词结构化摘要
3. 主对话交叉验证、做决策、更新文档

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Ch2 领域验证未做 | 问题定位要诚实 | 未开始 | 本对话 |
| Ch2 补实验未做 | 统计严谨性 | 审计完成 | 领域验证后决定范围 |
| Ch2 paper-materials 审计问题 | 数据一致性 | 6 项待修 | 补实验完成后统一更新 |

## 下一轮

1. 读取本交接文档 + Ch2 项目文档
2. 派 3 个子 agent 并行做领域调研
3. 汇总发现，做 Go/No-Go 判定
4. 更新 Ch2 decision_log 和 paper-materials
5. 同步更新 thesis-chapter-fixes topic-index
