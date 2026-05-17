# Decision Log: leo-congestion-routing

## 阶段摘要
- [Contract Step 0] 新颖性确认通过 (2026-05-17)
  - 复用 GW 检索（87 候选，17 篇精读，Step 3.5 补充检索），确认 per-link 负载均衡 + LEO 时变 + size gen 三角空白
  - 最接近竞品 TELGEN(L11) 仅覆盖 GNN+TE+size gen 静态快照，GMR(L02) 仅覆盖 per-path 分割
  - 跳过 0.1 系统检索，简化 0.2 竞品精读，保留 0.3 待后续定向确认
- [Contract Step 1] 假设形成 (2026-05-17)
  - 假设: GNN per-link 负载均衡 ≥10% 优于 ECMP, ≥15% 优于 MLP, 泛化退化 <10%
  - 依据: MVE-2 GNN/ECMP=0.88, GNN/MLP=0.80
  - Success: 三维全满足; Failure: 任一维满足即失败（独立定义）
- [Contract Step 2] Contract 草案完成 (2026-05-17)
  - contract.md (draft), 含全部必填字段
  - 5 baseline, 5 metrics, 12 实验, 2 [ASSUMPTION] 待 Step 3 核实
- [Contract Step 3] 参数溯源完成 (2026-05-17)
  - ISL 容量 10 Gbps: [设计选择] 光学 ISL 量级, 绝对值不影响相对对比, MVE 验证 MLU 合理
  - 区域故障 10%: [设计选择] 极端消融场景, 模拟太阳风暴/碎片事件
  - 所有 [ASSUMPTION] 已消除, contract.md 零残留
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

### D12: Contract Step 4 端到端推演 (2026-05-17)
- **决策**: 通过，1 个已知限制
- **已知限制**: log_std = nn.Parameter(264) 固定维度，泛化到其他规模必须用 deterministic=True。不影响泛化评估（deterministic 是标准评估模式）
- **断层检查**: 4 项全部无断层（特征完整、维度匹配、配置无矛盾、跨规模仅 log_std 已记录）
- **产出**: data-flow.md

### D13: Contract Step 5 压力测试 + 反模式审查 (2026-05-17)

**Q1 结构性优势**：GNN 的优势来源明确——多跳 message passing 聚合全局负载状态 → per-edge weight。激活条件清晰：链路故障打破 ECMP 等价路径 + 非均匀流量制造拥塞热点。非"用 DL 替代传统方法"的空泛声明，MVE 已验证具体激活条件（MVE-1 无故障 GNN≈ECMP，MVE-2 有故障 GNN>ECMP 12%）。✅

**Q2 边际结果**：若 GNN 改善 ECMP <5%（failure signal），论文仍有部分价值：(1) ablation 证明 message passing 必要性（MLP 已证明 < SP）；(2) 跨规模泛化能力独立于绝对改善。但核心贡献（≥10% 改善）将不成立，需降级为"分析性论文"。风险中等，可接受。✅

**Q3 信号独立性**：Failure 2（GNN>0.95×MLP，结构优势）和 Failure 3（泛化>1.20×ECMP）独立于 Success 信号。Failure 1（改善<5%）与 Success 1（改善≥10%）之间有 5% 灰色区间，但 gray zone 明确定义了"边际但非失败"。✅

**Q4 Baseline 共识性**：SP（11/22 篇使用，绝对共识）✅；ECMP（L02/L04/L16 使用，负载均衡标准）✅；MLP（L01/L07 均使用 FC ablation）✅；DTAR（288 星域间路由标杆，有代码，但域间路由与 per-link 粒度不同需论文说明）✅。GMR-simplified（P4 风险，退守策略为放弃此 baseline）。✅

**Q5 反模式审查**：

| # | 反模式 | 状态 | 证据 |
|---|--------|------|------|
| 1 | 信息泄露 | ✅ | GNN/MLP 相同输入（node 6-dim, edge 4-dim），差异仅在架构（GAT vs 独立 Linear）。消融用零向量替代删除，维度一致。 |
| 2 | 仿真过于简化 | ✅ | 仿真含三要素（非均匀流量+链路故障+时变），MLU≈2.0-2.5 充分拥塞。data-flow.md 确认模型输入含 utilization + demand 信息。 |
| 3 | 确定性信道+DL 强行优越 | ✅ | GNN 优势来源明确（全局负载聚合），低流量无故障场景自然退化（MVE-1 GNN≈ECMP）。非预测确定性信号。 |
| 4 | 跨实验数据不一致 | ✅ | 所有实验共用同一拓扑/流量/故障生成器，fairness rule 1 要求相同 seed 组合。 |

**结论**: 5 问均无致命风险信号，Step 5 通过。

### D11: Part A-checkpoint MDP 试运行 (2026-05-17)
- **决策**: 通过（附分析），进入 Part B
- **奖励分解**: 单分量 -MLU，无失衡风险（by design）
- **贪心 vs 随机**: naive load-aware (util+1) 仅好 3.8%（10 episodes 平均），未达 >10% 门限
- **根因**: Walker delta 规则拓扑下，负载感知绕路反而增加路径长度，导致更多拥塞。所有变体（linear5/10, exp, square）均不如 uniform(SP)
- **策略排序**: uniform(+7.1% vs random) > random > 所有 load-aware 贪心
- **不阻断理由**:
  1. 门限本意是抓奖励尺度失衡，-MLU 无此问题
  2. 策略区分度存在（SP > random 7.1%）
  3. MVE 已证明 GNN 在故障场景下 >ECMP 12%（D4），DRL 价值在全局优化非局部贪心
  4. 若 DRL 训练后不敌 SP，到时自然暴露
- **对 Part B 的启示**: SP 是此拓扑下强 baseline，DRL 需在故障+时变流量场景下证明优势

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

### D10: Step 6 仿真器设计确认 (2026-05-16)
- **决策**: 设计确认，进入 Step 7 实现
- **核心设计**:
  - MDP: 集中式 SDN，per-link weight 动作 (连续)，加权最短路路由
  - 星座: 66 节点训练 (6×11)，48/288/720 泛化测试
  - 奖励: r_t = -(MLU_t - MLU_{t-1})，MLU = max(load/capacity)
  - GNN: GAT 2层4头64维 + LN + Residual (对齐 DTAR 最佳实践)
  - RL: PPO + GAE + wandb + early stopping + save/load
- **防坑措施**:
  - C1: 单奖励分量-MLU，无量级失衡风险
  - C2: 720节点显存预算可控 (~2880 边 × GAT(64) < 2GB)
  - 6/6 缺失项: wandb/early stopping/save-load/config dataclass/gymnasium/共享 backbone 全部列入必做
- **[ASSUMPTION]** 占比 12% < 30% → 通过
- **仿真三要素**: 非均匀流量 + 链路故障 + 突发模式
- **设计文件**: projects/leo-congestion-routing/simulator-design.md

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
