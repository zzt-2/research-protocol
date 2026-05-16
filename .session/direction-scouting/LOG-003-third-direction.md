# Log 003: 第三研究方向候选 — GNN 拥塞感知路由

> 2026-05-16 | 来源: BH 方向归档后的方向侦察

## 背景

论文需要 3 个关联问题组成三章主体。已完成：
- Ch1: GNN routing size generalization (leo-mega-constellation-gnn-routing, Execute 完成)
- Ch2: GNN handover size generalization (leo-ntn-handover-drl, Execute 完成)
- Ch3: **待定** — BH 归档后需要新方向

## 候选方向检索

4 轮检索（GNN+卫星 2025-2026、GNN+资源管理、GNN+TE/负载均衡、GNN+故障恢复），总计 ~500 条结果。

### 推荐方向：GNN 拥塞感知路由 + 负载均衡

| 维度 | 评估 |
|------|------|
| 创新空间 | GNN+拥塞路由+卫星仅 4-5 篇，近乎空白 |
| Size gen 天然性 | 高：66颗训练→1584颗部署，流量模式差异大 |
| Thesis 一致性 | 路由→切换→流量工程，共享 GNN size gen 框架 |
| 失败模式回避 | 非物理约束主导、非空间隔离、per-node 决策 |
| 代表论文 | GNN 多路径路由 (2024, 41cit), 拥塞感知 GAT 路由 (2026) |

### 与现有工作的区分

- 路由项目：per-flow 最短路径策略
- 切换项目：per-UE 接入控制
- 新方向：per-link 负载均衡策略（链路利用率/队列深度是全局分布信息）

### 风险

- leo-resilient-routing MVE 已证明"纯路由决策 GNN ≈ MLP"。拥塞感知路由需验证 GNN 消息传递对全局负载信息的聚合优势确实不同于局部特征
- 前期必须快速 MVE 验证

## 备选方向（未深入）

| 方向 | 论文量 | GNN 空白 | 风险 |
|------|--------|----------|------|
| 网络切片 + SFC 部署 | ~8-10 | 近空白 | 问题偏复杂（VNF放置+路由+资源分配） |
| 拓扑控制/链路激活 | ~15 | 3-4篇 | 物理约束耦合（A3 风险） |

## 下一步

1. 新对话启动 GW Step 1-2 检索（项目名建议：leo-congestion-routing）
2. 重点检索：GNN+拥塞控制+卫星、GNN+负载均衡+LEO、size generalization+流量工程
3. 快速 MVE（Step 4a）：验证 GNN 对全局负载信息的聚合是否优于 MLP+局部特征
