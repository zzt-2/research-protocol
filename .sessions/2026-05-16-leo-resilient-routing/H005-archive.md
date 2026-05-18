# Handoff 2026-05-16

## 当前进度
- 阶段：**已归档**
- 状态：GW Step 4a MVE 三轮失败，归档决策已确认
- Contract 状态：未开始（已终止）

## 归档原因
LEO 故障感知抗毁路由方向，三轮 MVE 均失败：
1. **MVE-1/2**（GNN vs MLP）：GNN MLU 差 5.8%/4.2%，消息传递不优于手工特征
2. **MVE-3 Part A**（MARL 课程学习）：课程 +2.2% 一致但未达 5% 门槛（CONDITIONAL）
3. **MVE-3 Part B**（主动预路由）：主动 -1.3%，反而更差（FAIL）

根本原因：Walker 星座网格拓扑太规则，贪心最短路径 92% 投递率，RL 仅 5%。与 beam-hopping/ISL-scheduling 归档模式一致：物理约束主导的问题不适合 ML。

## 已更新文件
- `projects-overview.md`：已归档项目区新增 leo-resilient-routing
- `directions-registry.md`：已归档 #7，已排除更新，覆盖范围更新
- `decision_log.md`：追加归档决策和 MVE-3 结果
- `feasibility_report.md`：保留完整（含 Pivot 记录，供未来参考）
- `literature_notes.md`：保留完整（12 篇精读笔记仍可复用）

## 产出文件（归档保留）
- `projects/leo-resilient-routing/mve_gnn_vs_mlp.py` — MVE-1/2 脚本
- `projects/leo-resilient-routing/mve_marl_curriculum.py` — MVE-3 脚本
- `projects/leo-resilient-routing/mve3_results.json` — MVE-3 数值结果
- 12 篇精读论文 content.md（见 literature_notes.md 路径表）

## 跨项目教训（已记录）
- LEO 网络三个子方向（路由泛化/ISL调度/波束跳/抗毁路由）全部归档或受限
- 物理约束主导 + 正则拓扑 = 启发式够用 = ML 无优化空间
- GNN 拓扑感知优势需特定任务结构支撑，非通用卖点
