# Master State: leo-congestion-routing

> 最后更新: 2026-05-16

## 基本信息
- **项目名**: leo-congestion-routing
- **方向**: GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座
- **阶段**: Groundwork
- **当前步骤**: Step 4b 完成 → Step 6（仿真器设计）
- **方法类型**: [DRL] + [监督]

## 进度追踪

| 步骤 | 状态 | 产出文件 |
|------|------|----------|
| Step 1 检索+初筛 | ✅ | search-archive/2026-05-16/gnn-congestion-*.json 等 9 个文件 |
| Step 2 论文获取 | ✅ | 10 篇论文 content.md 已就绪 |
| Step 3 精读 | ✅ | literature_notes.md（10 篇精读 + 3 篇写作架构 + 综合分析） |
| Step 3.5 定向补充 | ✅ | L11 TELGEN + 4 篇新竞品发现 + 定位修订 |
| Step 4a 可行性预判 | ✅ MVE Pass | mve_env.py, mve_train.py, mve_66.py（D4 决策记录）|
| Step 5 Baseline选定 | ✅ | SP+ECMP+MLP+DTAR+GMR(D8) |
| Step 4b 执行可行性 | ✅ | feasibility_report.md (D9) |
| Step 6 仿真器设计 | ⬜ | 设计规格 |
| Step 7 Baseline复现 | ⬜ | baseline_report.md |

## 关键决策
- D1: R1+R2 搜索策略，87 条候选，覆盖充分
- D2: 差异化定位 = per-link 负载均衡决策（vs 现有 per-flow/per-path）
- D3: 继承 resilient-routing 失败教训，MVE 必须含非均匀流量场景
- D4: 10 篇精读完成，GMR(L02)架构最接近本研究（MPNN+DDPG per-path 流量分割+跨拓扑泛化）
- D5: 研究定位确认：per-link 负载均衡 + size generalization 填补空白
- D6: 竞品共引文献 10 篇待 Step 3.5 定向补充（RouteNet, DRL-TE, GNN-ASSSP 等）
- D7: MVE-1(24节点) GNN/MLP=0.83 但 GNN≈ECMP; MVE-2(66节点+8%故障) GNN/ECMP=0.88 → **Go**

## 核心风险
1. **[已缓解] GNN ≈ MLP 风险**: MVE 验证通过。24节点 GNN≈ECMP，但 66节点+链路故障下 GNN 低 ECMP 12%
2. **[高] TELGEN 竞品风险**: Zhou 2025 ToN 已做完整 GNN+TE+size gen（20x 泛化）。差异化必须聚焦 LEO 时变拓扑（TELGEN future work）。纯 size gen for TE 不再是空白
3. **[中] 论文池竞争**: GNN-ASSSP/DeepLaDu/GRL-RR 等近期竞品活跃，需 DeepLaDu 精读确认差异化空间
3. **[低] Size gen 可行性**: 无先例将 size gen 应用于拥塞路由，可能需要新的泛化机制

## Thesis 一致性
- Ch1: GNN routing size gen (leo-mega-constellation-gnn-routing, Execute 完成)
- Ch2: GNN handover size gen (leo-ntn-handover-drl, Execute 完成)
- Ch3: **GNN congestion-aware load balancing size gen (本项目)**
- 共享框架: GNN size generalization，per-node/per-link 决策，Walker delta 星座

## FR 检查清单
- [x] FR-01~08: MVE 验证 GNN 全局聚合在链路故障场景下有效（Step 4a Pass）
- [ ] FR-09 GNN 信息冗余: 待精读后评估（resilient-routing 失败与此相关）
- [ ] FR-10 空间隔离约束: 非物理约束主导方向，风险较低
