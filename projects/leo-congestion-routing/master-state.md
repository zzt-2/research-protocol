# Master State: leo-congestion-routing

> 最后更新: 2026-05-17

## 基本信息
- **项目名**: leo-congestion-routing
- **方向**: GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座
- **阶段**: Execute (Contract Amendment)
- **当前步骤**: 漏洞修复 Batch 1 完成，E01-v2 全量重跑通过。待重跑 E02-E09 (surge=1.0)
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
| Step 6 仿真器设计 | ✅ | simulator-design.md (D10) |
| Step 7 仿真器+Baseline | ✅ 28/28 验证通过 | simulator/, baselines/, verify/, baseline_report.md |
| Contract Step 0 新颖性 | ✅ | decision_log (复用 GW) |
| Contract Step 1 假设 | ✅ | contract.md |
| Contract Step 2 草案 | ✅ draft | contract.md |
| Contract Step 3 参数溯源 | ✅ | contract.md 零 ASSUMPTION |
| Contract Step 4 端到端推演 | ✅ | data-flow.md（1 个已知限制：log_std 维度固定） |
| Contract Step 5 压力测试 | ✅ | decision_log D13（5 问+4 反模式全通过） |
| Contract Step 6 冻结 | ✅ | contract.md (frozen), 用户确认 2026-05-17 |
| Execute Step 1 Quick Test | ✅ | worker-logs/step1-quick-test.md |
| Execute Step 2 E01 seed 0 | ⚠️ MARGINAL | GNN/ECMP=1.07 FAIL, GNN/MLP=0.84 PASS |
| 根因分析 | ✅ | MVE 用 K-path, 正式模型用 per-edge weight，架构不一致 |
| 范式迁移决策 D15 | ✅ | 迁移到 K-path 范式, 需 Contract amendment |
| Contract Amendment | ✅ | 动作空间 K-path + 奖励 delta MLU (D16) |
| K-path 迁移执行 | ✅ | env/model/train/baselines/verify 全部完成 (D16) |
| K-path Quick Test | ✅ PASS | GNN/ECMP=0.77 (23.4% 改善), 100ep, 163s GPU |
| E01 核心实验 | ⚠️ MARGINAL | GNN/ECMP=0.8588 PASS, GNN/MLP=0.8632 FAIL (差0.013), 79.3min |
| E04 泛化验证 | ✅ KEY FINDING | MLP跨规模崩溃(MLU+33.9%), GNN稳定(GNN/MLP=0.69) |
| E01-v2 重跑 (surge=5.0) | ✅ 双PASS | GNN/ECMP=0.818, GNN/MLP=0.822 |
| E01-v3 重跑 (surge=1.0) | ✅ **双PASS更强** | GNN/ECMP=0.778, GNN/MLP=0.808, std=0.012, 统计显著 p<0.0001 |
| E02 无故障 (surge=1.0) | ✅ **F2反转** | GNN/ECMP=0.845 — 无故障GNN仍赢ECMP(旧surge=5.0=1.095) |
| E03 surge鲁棒性 | ✅ | GNN/ECMP=0.767 — 无surge训练模型在surge=5下仍赢23% |
| E04 48节点 (surge=1.0) | ✅ PASS | GNN/ECMP=0.801 (0.7× scale) |
| E05 288节点 (surge=1.0) | ✅ PASS | GNN/ECMP=1.014 (4.4× scale) ≤ 1.10 |
| E06 720节点 (surge=1.0) | ✅ PASS | GNN/ECMP=0.932 (10.9× scale) ≤ 1.10 |
| E08 故障率消融 (surge=1.0) | ✅ | 全部GNN赢: 0%=0.845, 5%=0.855, 8%=0.797, 10%=0.881, 15%=0.837 |
| E09 流量消融 (surge=1.0) | ✅ 全GNN赢 | 均匀=0.857, 中等=0.811, 默认=0.797, 重型=0.843 |
| E10 层数消融 (surge=1.0) | ✅ <2%差异 | L1=0.777, L2=0.795, L3=0.792 |
| E11 头数消融 (surge=1.0) | ✅ <1%差异 | H2=0.771, H4=0.775, H8=0.779 |
| Execute Step 3 假设判定 | ✅ PASS | D19: 三维 Success Signal 全部满足，Failure Signal 全部未触发 |
| Execute Step 6 可视化 | ✅ | simulator/figures/fig1-10, simulator/visualize_results.py |
| 训练曲线实验 | ✅ | training_curves.json (GNN 500ep + MLP 300ep) |
| 密集消融实验 | ✅ | dense_ablation_results.json (故障率8点+流量8点+规模7点) |
| E10 层数消融 | ✅ | e10_e11_results.json, L3最优(0.803)但差异<3% |
| E11 头数消融 | ✅ | e10_e11_results.json, 差异<1.5pp，架构鲁棒 |

## 关键决策
- D1: R1+R2 搜索策略，87 条候选，覆盖充分
- D2: 差异化定位 = per-link 负载均衡决策（vs 现有 per-flow/per-path）
- D3: 继承 resilient-routing 失败教训，MVE 必须含非均匀流量场景
- D4: 10 篇精读完成，GMR(L02)架构最接近本研究（MPNN+DDPG per-path 流量分割+跨拓扑泛化）
- D5: 研究定位确认：per-link 负载均衡 + size generalization 填补空白
- D6: 竞品共引文献 10 篇待 Step 3.5 定向补充（RouteNet, DRL-TE, GNN-ASSSP 等）
- D7: MVE-1(24节点) GNN/MLP=0.83 但 GNN≈ECMP; MVE-2(66节点+8%故障) GNN/ECMP=0.88 → **Go**
- D11: Part A-checkpoint 通过（贪心仅+3.8%未达10%门限，但 SP>random 7.1%，MVE 已证 GNN>ECMP 12%）
- Baseline 结果: ECMP(1.97) > SP(2.37) > MLP(2.52)，MLP<SP 证明 message passing 必要性

## 核心风险
1. **[已缓解] GNN ≈ MLP 风险**: MVE 验证通过。24节点 GNN≈ECMP，但 66节点+链路故障下 GNN 低 ECMP 12%
2. **[高] TELGEN 竞品风险**: Zhou 2025 ToN 已做完整 GNN+TE+size gen（20x 泛化）。差异化必须聚焦 LEO 时变拓扑（TELGEN future work）。纯 size gen for TE 不再是空白
3. **[中] 论文池竞争**: GNN-ASSSP/DeepLaDu/GRL-RR 等近期竞品活跃，需 DeepLaDu 精读确认差异化空间
3. **[低] Size gen 可行性**: 无先例将 size gen 应用于拥塞路由，可能需要新的泛化机制

## 漏洞审计与修复（2026-05-17）

| 漏洞 | 状态 | 修复结果 |
|------|------|----------|
| F1: surge 始终激活 | ✅ 已修复 | surge=1.0 结果更好(GNN/ECMP=0.778 vs 旧0.818) |
| F2: GNN 正常条件劣于 ECMP | 📝 叙事调整 | 定位为"弹性路由"而非通用负载均衡，需论文层面调整 |
| F3: ECMP 不标准 | ✅ 已修复 | True ECMP(BFS全最短路)仅好1.35%，旧结果可信 |
| F4: 泛化声称误导 | ✅ 分析完成 | 推荐"Walker delta族内scale gen"+极地间隙测试(可选) |
| F5: 消融单seed | ⏳ 待修复 | 需GPU重跑消融(1-2天) |
| M2: MLP不公平 | ✅ 已修复 | 800ep/LR decay/奖励归一化/hidden=64 |
| M3: 无统计检验 | ✅ 已修复 | bootstrap p<0.0001, Cohen's d=-0.86 vs ECMP |
| m4: 只有MLU指标 | ✅ 已修复 | M1-M5全实现，env暴露per-link数据 |

详见 H012(审计) + H013(修复) + analysis_f4_generalization.md

## Thesis 一致性
- Ch1: GNN routing size gen (leo-mega-constellation-gnn-routing, Execute 完成)
- Ch2: GNN handover size gen (leo-ntn-handover-drl, Execute 完成)
- Ch3: **GNN congestion-aware load balancing size gen (本项目)**
- 共享框架: GNN size generalization，per-node/per-link 决策，Walker delta 星座

## FR 检查清单
- [x] FR-01~08: MVE 验证 GNN 全局聚合在链路故障场景下有效（Step 4a Pass）
- [ ] FR-09 GNN 信息冗余: 待精读后评估（resilient-routing 失败与此相关）
- [ ] FR-10 空间隔离约束: 非物理约束主导方向，风险较低
