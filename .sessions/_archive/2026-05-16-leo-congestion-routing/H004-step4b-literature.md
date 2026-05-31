# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 4b 完成 → Step 6（仿真器设计）
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：5 篇论文 PDF 转换+归档 + 6 篇精读(L12-L17) + literature_notes.md 更新 + index.json 注册

## 本轮产出文件
- `papers/doi/10.1016_j.ast.2026.112361/` — GNN-ASSSP (He 2026)
- `papers/doi/10.1109_TAES.2025.3571400/` — DLBR (Ju 2025)
- `papers/doi/10.1109_TON.2025.3607939/` — LARRI (Ye 2026)
- `papers/doi/10.1109_GLOBECOM52923.2024.10901096/` — FlexSATE (Liu 2024)
- `papers/doi/10.1109_TAES.2026.3652971/` — Fan 2026 / GRL-TE
- `projects/leo-congestion-routing/literature_notes.md` — L12-L17 精读结果已写入

## 关键上下文

### L12-L17 精读结论（影响 Step 6 设计）

**无直接竞品做 per-link 负载均衡 + DRL + LEO 时变**：
- L13 GNN-ASSSP：最直接竞品，但纯 SL（非 DRL），只做路径选择不做 per-link 流量分配
- L17 GRL-TE：GNN+DRL 范式重叠，但多层卫星+per-path 流量比，非 LEO 单层 per-link
- L12 DeepLaDu：问题不同（拓扑设计 vs 负载均衡），Lagrangian 对偶思路可借鉴
- L14 LARRI：固定拓扑 SL，不适配 LEO
- L15 DLBR：GNN 仅用于预测，路由用 D3QN（MLP），逐跳离散选择
- L16 FlexSATE：GLOBECOM 4 页短文，SL 模仿 MCF

### 仿真器设计的关键约束（来自精读）
- GNN-ASSSP 的边特征设计（距离+拥塞+方位角+带宽）证明物理特征有效 → 仿真器需支持多维边特征
- GRL-TE 的 MPNN path-edge-node 三层消息传递 → 可作为 GNN 架构参考
- DLBR 的流量预测辅助思路（α·当前+β·预测） → 可选模块
- DeepLaDu 的 Starlink 相干时间 ~0.52s（99.9%）→ 推理延迟约束

### 已完成步骤汇总
- Step 4a MVE Pass：24 节点 GNN≈ECMP，66 节点+链路故障 GNN 低 ECMP 12%（D7）
- Step 5 Baseline：SP + ECMP + MLP + DTAR + GMR（D8）
- Step 4b 可行性：feasibility_report.md（D9）

### 待补
- ALIDT/ADRLRM (Gao 2025/2026) 和 GRL-RR (Bai 2025) 未获取，不阻塞 Step 6
- FR-09（GNN 信息冗余）和 FR-10（空间隔离约束）待评估

## 下一步
1. 读 `stages/groundwork.md` Step 6 部分
2. 读 `code-quality.md` 和 `reference/sim-template/` 模板代码
3. 设计仿真器架构（env/config/model/train/reward/verify）
4. 重点关注：时变拓扑建模、per-link 负载均衡动作空间、拥塞感知状态空间

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md` — Master 编排状态
- `projects/leo-congestion-routing/literature_notes.md` — 文献笔记（L01-L17）
- `projects/leo-congestion-routing/feasibility_report.md` — 可行性报告
- `projects/leo-congestion-routing/decision_log.md` — 决策日志
