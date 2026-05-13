# Handoff 2026-05-13 (Contract 完成)

## 当前进度
- **阶段：Contract 全部完成，准备 Execute**
- 状态：Contract 已冻结（用户确认）
- 本轮完成：Contract Step 0-3（新颖性检索 + 假设 + 冻结 + 压力测试）

## Contract 关键内容
- **假设**: GNN + Orbital PE + 多尺度训练，66→720(11x) 零样本泛化，保留率 ≥80%
- **Success**: 保留率 ≥80% + 与 Dijkstra 差距 ≤20% + PE 贡献 ≥8pp（3 条同时满足）
- **Failure**: 同规模 GNN >1.5x Dijkstra / 跨规模 >1.8x 同规模 / PE 贡献 <3pp（任一条）
- **Baseline**: B1 Dijkstra + B2 GRLR(必须复现) + B3 GraphPR(推荐)
- **实验**: E01-E09，P0-E03 必做

## 关键上下文
- 新颖性确认：6 组检索 + 3 篇精读 + 2 组定向检索，size generalization for LEO routing 空白
- 最接近竞争者 TELGEN (IEEE/TON'25) 做 WAN TE 非卫星路由，可差异化
- Size Transferability (arXiv'26) 提供 RPEARL PE 理论，技术借鉴价值高
- GRLR 无开源代码，需自实现 + 论文图表验证（最耗时）
- 奖励函数需在仿真器设计确认时经用户审查（domain-comms §1.5）

## 文件索引
- Contract: `projects/leo-mega-constellation-gnn-routing/contract.md` (frozen)
- 竞争者摘要: `projects/leo-mega-constellation-gnn-routing/competitor_notes/` (3 文件)
- 检索存档: `search-archive/2026-05-13/contract-*.json` (8 文件)
- 决策日志: `projects/leo-mega-constellation-gnn-routing/decision_log.md` (D001-D013)

## 下一步：Execute 阶段
1. 读 `stages/execute.md`（框架流程）
2. 开发仿真器：Walker-Delta 星座 + ISL 模型 + 流量生成 + Dijkstra
3. 复现 GRLR：读 GRLR 论文全文，按架构实现 Actor-Critic + GNN
4. 实现核心方法：GNN + Orbital PE + 多尺度训练
5. 跑实验 E01-E09
