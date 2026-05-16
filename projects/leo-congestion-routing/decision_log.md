# Decision Log: leo-congestion-routing

## 阶段摘要
- [Groundwork Step 1] 检索+初筛完成 (2026-05-16)
  - R1: 7个JSON文件 180条原始 + R2: 2个JSON文件 50条
  - 去重后 87 条独立候选
  - 必读15 / 建议读20 / 待确认6 / 备选9 / 排除37
  - 质量门槛全部通过
  - R2 定向检索确认: size generalization × 拥塞路由交叉为真空
  - GNN + 拥塞感知路由 + LEO 三角交集有论文但无 per-link 负载均衡竞品
- [Groundwork Step 2] 论文获取完成 (2026-05-16)
  - 成功获取 10 篇 content.md（arXiv 3 + DOI OA 2 + blit IEEE 4 + 已存在 1）
  - 必读覆盖：#4 GDRL-SFCR, #5 GMR, #8 Fan, #14 DTAR, #3 GRLR, #11 POMAP, #16 PathGNN
  - 建议读覆盖：ST-QoS routing
  - 待确认覆盖：PRIMAL, QueueMARL
  - 下载失败：GNN-ASSSP(ScienceDirect), DLBR(IEEE TAES搜索未匹配), LARRI(IEEE ToN未下载), FlexSATE, CA-GAR(MDPI)
  - 修复：gw-acquire.md 和 tools-scenarios.md 补充了 blit --download 作为 IEEE 下载 fallback

## 决策记录

### D4: MVE 验证 — GNN vs MLP 拥塞路由 (2026-05-16)
- **决策**: MVE Pass → Go
- **MVE-1 (24节点, 无故障)**:
  - GNN MLU: 0.809 ± 0.040 (3 seeds × 150 eps)
  - MLP MLU: 0.979 ± 0.047
  - GNN/MLP = 0.83 → GNN 低 17%
  - 但 ECMP (0.80) ≈ GNN → GNN 未超越简单基线
- **MVE-2 (66节点, 8%链路故障)**:
  - GNN MLU: 1.096 ± 0.126
  - ECMP MLU: 1.244 ± 0.180
  - MLP MLU: 1.373 ± 0.216
  - SP MLU: 1.474 ± 0.220
  - **GNN/ECMP = 0.88 → GNN 低 12%**
  - GNN/MLP = 0.80 → GNN 低 20%
- **关键洞察**: 24节点小拓扑中 ECMP 足够好（等价路径多），但链路故障打破等价路径后，ECMP 盲目轮询失效，GNN 全局负载感知胜出
- **Go 条件**: 后续仿真器必须包含链路故障场景（验证 GNN 在更广泛条件下的优势）

### D9: Step 4b 执行可行性 Go (2026-05-16)
- **决策**: Go
- **维度 C 仿真条件**: ✅ MVE 已验证非均匀流量+链路故障为 GNN 优势激活条件。正式仿真器需确保三要素（非均匀流量+链路故障+时变拓扑）
- **维度 E 资源风险**: ✅ 3/5 baseline 有代码或无需代码，总投入 ~2-3 周，失败可回收（对比基准+仿真器+综述）
- **已记录风险**: (1) TELGEN 竞品聚焦 LEO 差异化 (2) GMR P4 复现风险 (3) 仿真三要素缺一不可
- **结论**: 所有维度无致命信号，继续 Step 6 仿真器设计

### D8: Baseline 选定 (2026-05-16)
- **决策**: 选定 5 个 baseline
- **核心 baseline (3)**:
  1. **SP (Dijkstra)** — 领域绝对共识（11/22 篇使用），MVE 已有
  2. **ECMP** — 负载均衡标准方法，MVE 验证 GNN 超 12%，本研究核心对照
  3. **MLP** — 消融对照，证明 GNN message passing 结构性优势，MVE 已有
- **竞品 baseline (2)**:
  4. **DTAR (L06)** — 有开源代码 (GitHub)，域间路由，先跑快速出结果
  5. **GMR 简化版 (L02)** — 最接近竞品（MPNN per-path splitting），自实现简化版（去 PER，固定 K=2）
- **备选**: LP Optimal (Gurobi 上界，非必须)
- **理由**: SP+ECMP 覆盖传统共识，MLP 做 GNN ablation，DTAR+GMR 覆盖 GNN 竞品对比。田野调查（40 篇扫描 12 篇相关）交叉验证 SP 为绝对共识，ECMP 在 LEO 路由领域非标准但在负载均衡研究中是核心对照
- **风险**: GMR 属 P4（无代码+缺超参），简化版复现精度不确定；DTAR 域间路由与 per-link 建模有差异，论文需说明

### D1: 搜索策略与覆盖度 (2026-05-16)
- **决策**: R1 四角度检索 + R2 两个定向补充（size gen × TE, 方法论迁移）
- **理由**: 方向侦察已确认 GNN+拥塞路由+卫星仅 4-5 篇，正式 GW Step 1 需要系统化覆盖
- **结果**: 87 条候选，覆盖充分；size gen × 拥塞交叉为真空（潜在核心贡献）

### D2: 核心空白与差异化定位 (2026-05-16)
- **决策**: 定位为 "GNN 全局负载聚合 → per-link 负载均衡决策"，区别于现有工作
- **理由**:
  - 与项目1（per-flow 最短路径）和项目2（per-UE 接入控制）形成问题层次差异
  - 最接近竞品 GNN-ASSSP 做 edge weight learning，GMR 做 per-path splitting，均非 per-link 决策
  - Thesis 三章一致性：路由 → 切换 → 流量工程，共享 GNN size gen 框架
- **风险**: leo-resilient-routing MVE 证明 GNN ≈ MLP for routing。拥塞/负载信息的全局聚合是否真正需要 GNN message passing，需 Step 4a MVE 验证

### D3: 继承的失败教训 (2026-05-16)
- **来源**: leo-resilient-routing 归档
- **教训**: Walker delta 网格拓扑过于规则，贪心路由 92% 投递率，RL 仅 5%
- **对本方向的影响**: 拥塞感知路由不依赖拓扑不规则性，而是依赖全局负载分布信息的聚合。如果负载分布高度不均匀（非均匀流量），GNN message passing 可能有优势。但如果负载均匀，则等价于纯路由问题，GNN 优势消失
- **应对**: MVE 必须包含非均匀流量场景，且对比 GNN vs MLP+局部负载特征
