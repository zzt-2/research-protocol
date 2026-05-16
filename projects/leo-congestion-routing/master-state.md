# Master State: leo-congestion-routing

> 最后更新: 2026-05-16

## 基本信息
- **项目名**: leo-congestion-routing
- **方向**: GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座
- **阶段**: Groundwork
- **当前步骤**: Step 1 完成 → Step 2（论文获取）
- **方法类型**: [DRL] + [监督]

## 进度追踪

| 步骤 | 状态 | 产出文件 |
|------|------|----------|
| Step 1 检索+初筛 | ✅ | search-archive/2026-05-16/gnn-congestion-*.json 等 9 个文件 |
| Step 2 论文获取 | ⬜ | papers/ 目录 |
| Step 3 精读 | ⬜ | literature_notes.md 更新 |
| Step 3.5 定向补充 | ⬜ | literature_notes.md 更新 |
| Step 4a 可行性预判 | ⬜ | feasibility_report.md |
| Step 5 Baseline选定 | ⬜ | decision_log.md 更新 |
| Step 4b 执行可行性 | ⬜ | feasibility_report.md 更新 |
| Step 6 仿真器设计 | ⬜ | 设计规格 |
| Step 7 Baseline复现 | ⬜ | baseline_report.md |

## 关键决策
- D1: R1+R2 搜索策略，87 条候选，覆盖充分
- D2: 差异化定位 = per-link 负载均衡决策（vs 现有 per-flow/per-path）
- D3: 继承 resilient-routing 失败教训，MVE 必须含非均匀流量场景

## 核心风险
1. **[高] GNN ≈ MLP 风险**: resilient-routing MVE 两次证明路由决策 GNN 无优势。新方向赌拥塞/负载信息需全局聚合，需 Step 4a MVE 验证
2. **[中] 论文池竞争**: GNN-ASSSP/GMR/DTAR 等近期竞品活跃，需精读确认差异化空间
3. **[低] Size gen 可行性**: 无先例将 size gen 应用于拥塞路由，可能需要新的泛化机制

## Thesis 一致性
- Ch1: GNN routing size gen (leo-mega-constellation-gnn-routing, Execute 完成)
- Ch2: GNN handover size gen (leo-ntn-handover-drl, Execute 完成)
- Ch3: **GNN congestion-aware load balancing size gen (本项目)**
- 共享框架: GNN size generalization，per-node/per-link 决策，Walker delta 星座

## FR 检查清单
- [ ] FR-01~08: 待 Step 4a 评估
- [ ] FR-09 GNN 信息冗余: 待精读后评估（resilient-routing 失败与此相关）
- [ ] FR-10 空间隔离约束: 非物理约束主导方向，风险较低
