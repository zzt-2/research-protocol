# Literature Notes: leo-congestion-routing

> GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座

## 步骤进度

| 步骤 | 状态 | 日期 | Commit |
|------|------|------|--------|
| Step 1 检索+初筛 | ✅ 完成 | 2026-05-16 | TBD |
| Step 2 论文获取 | ⬜ | | |
| Step 3 精读 | ⬜ | | |
| Step 3.5 定向补充 | ⬜ | | |
| Step 4a 可行性预判 | ⬜ | | |
| Step 5 Baseline选定 | ⬜ | | |
| Step 4b 执行可行性 | ⬜ | | |
| Step 6 仿真器设计 | ⬜ | | |
| Step 7 Baseline复现 | ⬜ | | |

## Step 1 检索结果摘要

### 检索策略
- R1: 4 组关键词（GNN+congestion+satellite, GNN+load balancing+satellite, GNN+congestion general, non-GNN congestion+LEO）
- R1 已有方向侦察结果补充（3 个相关文件）
- R2: 2 组定向检索（size generalization+TE, GNN congestion adaptive routing）

### 质量统计
- 去重前: 180 条（R1 7文件）+ 50 条（R2 2文件）
- 去重后: 87 条独立论文
- 必读 15 / 建议读 20 / 待确认 6 / 备选 9 / 排除 37
- 正式发表占比: ~70%
- 覆盖子方向: GNN+LEO路由, GNN+负载均衡(通用), LEO拥塞控制(非GNN), GNN+TE

### 核心空白确认

**"GNN + 拥塞感知路由 + LEO"三角交集区**：有论文但无直接竞品做 per-link 负载均衡决策。

最接近竞品：
| 论文 | 方法 | 与本研究的差异 |
|------|------|---------------|
| GNN-ASSSP (He 2026) | GAT+Transformer, congestion-aware edge weights | per-edge weight learning，非 per-link 负载均衡决策 |
| GMR (Huang 2024, TVT, 41cit) | GNN multipath TE | per-path traffic splitting，非 per-link |
| DTAR (Zhou 2026) | GAT+PPO domain routing | 域间路由，非全网 per-link |
| DLBR (Ju 2025, TAES) | GCN+LSTM+DRL load balancing | GNN 仅用于流量预测，非路由决策 |

**Size generalization × 拥塞路由交叉**：完全真空。无任何论文同时涉及 GNN size generalization 和拥塞感知路由/TE。这是 thesis 框架一致性的关键空白，也是潜在核心贡献。

### 关键风险

**[已继承] leo-resilient-routing MVE 两次证明 GNN ≈ MLP for routing decisions。**
新方向的核心赌注：拥塞/负载信息需要全局聚合（不同于纯拓扑路由），GNN message passing 在这个维度上有优势。
必须在 Step 4a MVE 中优先验证此假设。

## 必读论文清单（15 篇）

1. GNN-ASSSP (He 2026, Aerospace Sci Tech) — 最直接竞品
2. Knowledge-Enhanced Intent-Driven Flow Scheduling (Wang 2026, IEEE) — congestion-aware+GNN+LEO
3. GRLR (Zhang 2025, TVT, 44cit) — GNN+RL mega LEO routing
4. GDRL-SFCR (Chen 2025, Sensors, 11cit) — GNN+DRL routing + SFC
5. GMR/GNN-MPTE (Huang 2024, TVT, 41-56cit) — GNN multipath TE
6. Inter-satellite routing GNN+DRL (Xu 2024, Access, 20cit) — delay+load joint
7. GraphSAGE+DQN LEO routing (Shi 2024, Appl Sci, 20cit) — inductive learning
8. GNN+DQN power control + load balancing (Fan 2026, Springer) — per-link
9. DPR (Greenwood 2026, Int J Satellite Comm) — GNN proactive congestion
10. DLBR (Ju 2025, TAES, 12-22cit) — GCN+LSTM+DRL load balancing
11. POMAP (Li 2025, IoT Journal, 2cit) — queue-aware MARL
12. CA-GAR (Liu 2026, Symmetry) — GAT congestion routing, non-satellite
13. FlexSATE (Liu 2024, GLOBECOM) — distributed TE + supervised
14. DTAR (Zhou 2026, arXiv) — GAT+PPO domain routing
15. Traffic-Aware Domain Partitioning (Zhou 2026, arXiv) — DTAR 完整版

## 建议读论文（R1 19 + R2 1 = 20 篇）

16. PathGNN (Ye 2025, JSAC, 4cit) — path-based GNN TE
17. LARRI (Ye 2026, ToN) — GNN adaptive range routing
18. MAGNNETO (Bernárdez 2023, TCCN, 44cit) — multi-agent GNN TE
19. TELGEN (Zhou 2025, ToN) — GNN generalizable TE, 5000 nodes
20. 3DQR (Kołakowski 2025, Electronics, 3cit) — hierarchical MADRL+GNN
21. Hierarchical Routing FSO LEO (Mao 2024, IEEE Network, 148cit) — M/M/1/m queuing
22. CALB+SGC-LB (Ning 2023, JOCN, 11-13cit) — congestion-aware load balancing
23. DHBP (Han 2023, Sensors, 10-12cit) — distributed back-pressure
24. SDN Load-Balanced Routing (Roth 2022, IEEE, 27cit)
25. ATLB (Liu 2023, ICCC, 4cit) — adaptive timescale LB
26. MADQN-MQ congestion+routing (Tang 2024, IEEE, 7cit)
27. Classic LEO LB routing (Liu 2020, Access, 91cit)
28. Extended link states LB (Dong 2022, China Comm, 65cit)
29. GNN routing survey (Jiang 2024, Sustainability, 71cit)
30. GAT+LSTM+DQN distributed routing (Chou 2026, arXiv)
31. QoS-Physics-Aware optical routing (Dabiri 2025, arXiv)
32. Queue-Aware MARL (Liaq 2026, arXiv)
33. Service-Oriented GNN+RL multipath (Fan 2026, IEEE)
34. DRL adaptive TE satellite (Roth 2025, ASMS/SPSC)
35. Aries: Adaptive Cluster Routing (Qin 2026, TAES) — [R2新增] MEO/LEO cluster+congestion avoidance
