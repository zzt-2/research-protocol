# Handoff: Ch3 拥塞/故障弹性路由 质量审计

> 来源: S001 | 交接目标: 对 Ch3 做全面质量审计，输出问题清单+修复建议
> 文件名: H003-ch3-handoff.md

## 已完成边界

- S003 三章审查已完成，Ch3 判定：核心 WARN(数据版本已统一)、漏洞修复 WARN(F5/E12已补)、Ch1差异化 WARN
- 核心实验 E01-E11 全完成，E10/E11 补了多 seed(3 seed, 6 配置)，E12 故障模式对比已补(3模式×4故障率)
- paper-materials.md 已统一为 surge=1.0 数据
- 待决项：DTAR/GMR 未直接对比（降级为 Related Work 讨论）

## 不要做什么

- 不要写论文正文
- 不要跑新实验（除非审计发现必须补做且用户同意）
- 不要修改已有实验数据
- 不要在主对话做大量文件阅读——全部委托子 agent

## 必读

1. `.sessions/chapter-quality-audit/topic-index.md`（专题总控）
2. `.sessions/thesis-structure-research/S003-three-chapter-audit.md`（前置审查结论）
3. `projects/leo-congestion-routing/paper-materials.md`（素材包，单文件）
4. `projects/leo-congestion-routing/contract.md`（假设+amendment+实验计划）
5. `projects/leo-congestion-routing/decision_log.md`（D1-D21）
6. `projects/leo-congestion-routing/literature_notes.md`（17 篇精读）
7. `projects/leo-congestion-routing/data-flow.md`（数据流设计）
8. `projects/leo-congestion-routing/master-state.md`（当前状态）

## Ch3 核心信息摘要

### 核心声称（3条，A+B框架）
1. **故障弹性路由（主）**：GNN per-flow K-path 框架在 0-15% 故障率和 5x 流量突发下全面优于 ECMP（GNN/ECMP=0.77-0.88）
2. **在线逐流决策（次）**：每条流到达时独立路由，单次前向传播 1-2ms CPU，故障响应比 ECMP 重算快 7.7x
3. **跨规模零样本部署（辅）**：66星训练→48-720星部署，GNN/ECMP≤1.014，同架构 MLP 跨规模崩溃

### 实验清单
- ✅ E01: 核心对比（66星, 8% fault, surge=1, 3 seeds, p<0.0001）
- ✅ E02: 无故障基线（0% fault）
- ✅ E03: 突发鲁棒性（8% fault, surge=5）
- ✅ E04-E06: 跨规模泛化（48/288/720 节点）
- ✅ E08: 故障率消融（0-15%，5 点）
- ✅ E09: 流量模式消融（均匀到重型）
- ✅ E10: GNN 层数消融（L=1/2/3, 3 seeds）
- ✅ E11: 注意力头数消融（H=2/4/8, 3 seeds）
- ✅ E12: 故障模式对比（random/regional/cascading × 4 故障率，11/12 GNN 赢）
- E07: GNN vs MLP 消融（在 E04-E06 中已部分覆盖）

### 指标
M1 MLU(主), M2 CV(负载均衡), M3 Overflow Ratio(拥塞), M4 Generalization Gap, M5 Convergence Speed

### Baseline
B1 SP(Dijkstra)✅, B2 ECMP✅, B3 MLP(消融对照)✅, B4 DTAR(Zhou'26,降级为Related Work), B5 GMR-simplified(降级为可选)

### 竞品
TELGEN(Zhou'25 ToN, GNN+TE+20x泛化, 最强竞品), GMR(MPNN+DDPG per-path,架构最接近), DTAR(GAT+PPO域间路由), GNN-ASSSP(GAT+Transformer), DeepLaDu(GATv2 per-edge), PathGNN(path-link二部图)

### 已知风险
1. TELGEN 泛化指标全面领先（20x vs 10.9x, <3% vs ≤10%）
2. DTAR/GMR 未直接对比，仅在 Related Work 讨论
3. 288 节点(12×24)和 96 节点(8×12)异常值（Walker delta 族内泛化非单调）
4. Ch1 同质化风险（同为 GNN+路由+size gen）
5. 最后文献检索 2026-05-16（距今 6 天）
6. 消融已有 3 seed（E10/E11），核心 E01 有 3 seed，其他仍单 seed
7. cascading 10% 故障率下 GNN 输 ECMP（唯一输的场景）

### 独特挑战：Ch1 差异化论证
Ch1 和 Ch3 都做卫星节点数泛化，且规模范围接近。审计需验证以下差异化是否充分：
- Ch1：泛化路由策略（方向偏好），监督学习，无故障
- Ch3：泛化负载均衡能力，DRL，故障感知
- 关键句式："第X章已证明GNN+PE可实现跨规模路由策略迁移，但假设无故障的理想网络。本章进一步挑战在线故障弹性场景下的规模泛化问题。"

## 审计执行计划

### Phase 1: 文献新鲜度 & 新颖性（2 个子 agent 并行）

**Agent 1A — 最新文献检索**
- 关键词组合：GNN + congestion-aware routing + LEO / satellite + fault-resilient / failure-aware + load balancing + size generalization
- 执行：`bash tools/search` 做 4-6 组检索，时间 2026-01 至今
- 特别关注：TELGEN 是否有后续工作或应用扩展
- 输出：新论文列表 + 重叠度判定

**Agent 1B — 已有竞品深化核查**
- 输入：读 `literature_notes.md`（17 篇）
- 任务：
  1. TELGEN 深度对比：逐维度（场景/方法/泛化范围/指标），我们的优势在哪
  2. GMR 架构对比：per-path 流量分割 vs 我们 per-flow K-path，粒度差异论证
  3. DTAR 差异化：域间路由 vs 域内负载均衡
  4. 验证"故障弹性路由 + 跨规模泛化"组合是否仍为空白
- 输出：竞品-差异化矩阵

### Phase 2: 实验完备性对标（2 个子 agent 并行）

**Agent 2A — 领域 Top 论文实验清单提取**
- 精读 2-3 篇：TELGEN(ToN'25), GMR(JSAC或TWC), GNN-ASSSP(TCOM 或类似)
- 提取维度同 H001
- 特别关注：
  - 负载均衡/TE 论文的标准基线是什么？（ECMP 是否足够强？）
  - 故障弹性论文的标准实验设计？
  - 跨规模泛化的标准评估协议？

**Agent 2B — 我们的实验覆盖度自检**
- 读 Ch3 contract.md + paper-materials.md + data-flow.md
- 特别检查：
  - ECMP 作为唯一路由基线是否足够？（DTAR/GMR 降级是否合理？）
  - 故障模式覆盖是否充分（random/regional/cascading 三种，但 cascading 10% 有失败场景）
  - 跨规模实验是否有"跳跃"（96 节点缺失，Table 2 跳过）
  - K-path 范式迁移后的实验是否完整覆盖新范式

### Phase 3: 指标完整性 + 数据自洽性（2 个子 agent 并行）

**Agent 3A — 指标完整性**
- 负载均衡/TE 领域标准指标：MLU、吞吐量、时延、丢包率、链路利用率分布、公平性、收敛时间
- 故障弹性额外指标：恢复时间、故障检测率、路径可用性
- 我们报了哪些？缺哪些？能补吗？

**Agent 3B — 数据自洽性验证**
- 重点检查：
  1. paper-materials.md 中所有数字是否统一为 surge=1.0
  2. E10/E11 多 seed 结果（6 配置 × 3 seed）与 paper-materials 是否一致
  3. E12 故障模式结果（3 模式 × 4 故障率）是否完整记录
  4. 跨规模数字：48=0.801, 288=1.014, 720=0.932 是否与原始 results/ 一致
  5. 288 节点异常值(ratio=1.014)是否在论文中讨论
  6. contract 中 12 个实验编号 vs paper-materials 中实际列出的实验编号是否一一对应

### Phase 4: 汇总与输出

同 H001 Phase 4 格式，审计报告写入 `.sessions/chapter-quality-audit/S004-ch3-audit.md`。

额外输出：
1. **Ch1 差异化论证方案**——如何在论文中区分 Ch1 vs Ch3
2. **TELGEN 对比策略**——统一处理而非回避
3. **DTAR/GMR 降级合理性论证**——如果审计认为需要直接对比，评估工作量

## 接口变更

无

## 失败数据附录

- cascading 10% 故障率 GNN 输 ECMP（MLU=0.75，网络严重退化），论文 Limitations 中讨论

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| DTAR 未直接对比 | Baseline 合法性 | 降级为 Related Work | 审计判定 CRITICAL 则适配（~1-2 天）|
| GMR 未直接对比 | Baseline 合法性 | 降级为可选 | 审计判定需对比则自实现（~2-3 天）|
| 96 节点缺失 | 实验完备性 | Table 2 跳过 | 审计判定需补充则补跑 |
| E02/E03/E08/E09 单 seed | 统计严谨性 | 核心E01已3seed | 审计判定需补充则补跑 |
| Ch1 同质化 | 三章差异化 | 有论证但待验证 | 审计判定论证不足则重写过渡段 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| 新颖性 | 故障弹性+跨规模泛化组合仍为空白 | Contract S0 |
| 实验覆盖 | TE/负载均衡领域 top 论文 80%+ | Contract S5 |
| 指标完整 | 负载均衡+故障弹性标准指标 90%+ | domain-comms.md |
| 数据自洽 | 0 矛盾 | 框架通用要求 |
| Ch1 差异化 | 六维差异经得起追问 | S003 审查建议 |
| TELGEN 对比 | 差异化论证充分 | 竞品风险矩阵 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 S003 中 Ch3 的审查结论（核心 WARN、E12 已补、数据已统一）
- [ ] 已确认 E10/E11 多 seed 结果和 E12 故障模式结果已记录
- [ ] 已检查必读文件中至少 3 个存在且可读

## 下一轮

1. 新对话读取本交接文档 + topic-index
2. 按 Phase 1→2→3→4 顺序执行
3. 审计报告写入 S004，问题清单更新到本交接文档
4. 完成后更新 topic-index 进展线索
