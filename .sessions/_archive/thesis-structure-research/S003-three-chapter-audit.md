# [S003] 三章论文全面审查

> 2026-05-21 | 论文结构 | active
> 续接 thesis-structure-research 专题，对三章论文做 cross-project 审查

## 目标

对已完成/接近完成的三个项目做一次全面审查，验证：
1. 实验数字是否支撑叙事
2. 三章是否形成连贯的论文结构
3. 竞品风险和差异化是否充分
4. 每章的薄弱环节和补救方案

## 审查对象

### Ch1: leo-mega-constellation-gnn-routing（路由 size gen）

- **状态**: Execute 完成
- **核心叙事**: 小星座训练→Starlink 级零样本泛化，跨规模时延保留率 90.3%
- **关键数字**: 跨规模时延保留率 90.3%，PE 是学习必要条件，9.7pp stretch 差距纯来自跨规模迁移
- **审查重点**:
  - 90.3% 保留率的实验条件（什么规模→什么规模？基线是什么？）
  - "PE 是必要条件"的消融是否充分（仅无 PE vs 有 PE？中间态呢？）
  - 9.7pp stretch 差距是否可接受（与竞品比较）

**必读文件**:
1. `projects/leo-mega-constellation-gnn-routing/master-state.md`
2. `projects/leo-mega-constellation-gnn-routing/decision_log.md`
3. `projects/leo-mega-constellation-gnn-routing/feasibility_report.md`
4. `projects/leo-mega-constellation-gnn-routing/baseline_report.md`
5. `.sessions/2026-05-13-mega-constellation-gnn-routing/H008-0514-step5.md`
6. 项目下 `results/` 目录的实验数据
7. 项目下 `paper_materials/`（如有）

### Ch2: leo-ntn-handover-drl（切换 size gen）

- **状态**: Contract 冻结 + 素材提取完成
- **核心叙事**: 二部图 GNN + DDQN 实现 LEO 切换 size generalization
- **关键数字**: GNN 20UE→100UE reward 35,699（正），MLP 迁移崩溃 -9,710；top-K 压缩 reward 2x，GNN 仅 +0.8%
- **审查重点**:
  - **GNN 贡献只有 +0.8%**——这是致命弱点还是可以包装？叙事如何讲？
  - top-K 压缩是决定性改进（2x），但这是方法贡献还是工程 trick？
  - 20UE→100UE 的迁移实验设计是否严格（训练集规模、测试集独立性？）
  - 与 Ch1 的 size gen 叙事是否重复？差异化在哪？

**必读文件**:
1. `projects/leo-ntn-handover-drl/master-state.md`
2. `projects/leo-ntn-handover-drl/decision_log.md`
3. `projects/leo-ntn-handover-drl/contract.md`
4. `projects/leo-ntn-handover-drl/feasibility_report.md`
5. `projects/leo-ntn-handover-drl/baseline_report.md`
6. 项目下 `paper_materials/`（6 文件 ~95K）

### Ch3: leo-congestion-routing（拥塞路由）

- **状态**: Execute Step 6 完成，12 张可视化图已生成
- **核心叙事**: GNN message passing 实现 per-link 负载均衡，拥塞感知路由
- **关键数字**: GNN vs ECMP +18.2%，GNN vs MLP +17.8%，跨规模 ≤5% 退化
- **审查重点**:
  - **与 Ch1 都是路由问题**——如何论证是独立问题？差异化在哪？
  - +18.2% vs ECMP 的实验条件——ECMP 是公平基线吗？有没有更强的路由基线？
  - TELGEN (Zhou'25 ToN) 竞品风险——"LEO 时变拓扑"差异化够不够？
  - K-path 范式（D15）的设计合理性——为什么从 per-flow 改成 per-edge？
  - 跨规模泛化 ≤5% 是什么范围（0.7×~10.9×）？下界 0.7× 是否太小？

**必读文件**:
1. `projects/leo-congestion-routing/master-state.md`
2. `projects/leo-congestion-routing/decision_log.md`
3. `projects/leo-congestion-routing/contract.md`
4. `projects/leo-congestion-routing/feasibility_report.md`
5. `projects/leo-congestion-routing/baseline_report.md`
6. `projects/leo-congestion-routing/data-flow.md`（如有）
7. 项目下 `results/` 目录

## 整体审查维度

### 1. 论文结构连贯性

根据 R001 的分析，层次递进型最优（正常态→优化态→异常态）。当前三章：
- Ch1: 路由 size gen（正常态：基础路由）
- Ch2: 切换 size gen（正常态→过渡态：用户接入切换）
- Ch3: 拥塞路由（优化态：负载均衡）

**问题**: Ch1 和 Ch3 都是路由，Ch2 是切换。递进逻辑是否自然？
- 替代叙事: "图方法的跨规模泛化 for 卫星通信" → 三个不同问题（路由/切换/拥塞路由）→ 统一方法 + 不同场景
- 需要检查 R001 中"场景拓展型"的建议

### 2. 方法统一性

三章的方法是否足够统一又各有递进？
- Ch1: GraphSAGE + 位置编码
- Ch2: 二部图 GNN + DDQN + top-K
- Ch3: GNN message passing + K-path

方法差异较大（不同的 GNN 变体、不同的 RL 算法），统一叙事是什么？

### 3. Size generalization 叙事一致性

- Ch1: 跨星座规模（节点数泛化）
- Ch2: 跨用户规模（UE 数泛化）
- Ch3: 跨网络规模（节点数泛化）

泛化维度是否足够差异化？还是读者会觉得是同一件事做三遍？

### 4. 竞品风险矩阵

每章最强的 1-2 个竞品是什么？差异化是否站得住？

## 记录

### Per-Chapter 审查汇总

#### Ch1: leo-mega-constellation-gnn-routing（路由 size gen）

| 维度 | 判定 | 核心理由 |
|------|------|---------|
| 核心数字（90.3%/9.9%/stretch） | **PASS** | 数字自洽，neighbor_map bug修复后数据可靠，评估协议统一 |
| 消融充分性 | **WARN** | A1/A2/A3完成，但缺随机PE对照；A4/A5(P2)未执行；PE是前提条件非渐进贡献，Contract假设需修正 |
| Baseline公平性 | **PASS** | 不公平之处已声明且合理；GraphPR未复现但仅为"推荐"级 |
| 竞品风险 | **PASS** | 25篇精读+63篇引用链确认size gen空白；TELGEN做TE非路由 |
| PPO无效/加权Dijkstra | **WARN** | 叙事需从"RL+PE+多尺度"调整为"PE使跨规模学习成为可能"；多尺度仅2-4pp，降为辅助策略 |
| 中文引用 | **FAIL** | 学位论文硬性要求，完全未补充 |
| 论文写作 | **WARN** | 素材包6文件109KB就绪，正文零进度 |

**关键发现**：加权Dijkstra推理在A1消融中退化为纯Dijkstra（stretch=1.002），证明GNN的PE确实在指导路由。可定位为"神经-符号混合推理"。

**最大风险**：论文叙事调整（从RL调整为监督学习+PE）+ 中文引用缺失。

#### Ch2: leo-ntn-handover-drl（切换 size gen）

| 维度 | 判定 | 核心理由 |
|------|------|---------|
| GNN +0.8% | **WARN** | 叙事转向合理，但50UE同规模GNN仍负于MLP(+4.9%)，缺N=30-40拐点数据 |
| top-K定位 | **WARN** | top-K贡献>>GNN绝对性能贡献；三级叙事分工逻辑成立，但需谨慎避免"top-K做了99%的工作"印象 |
| Size gen严谨性 | **WARN** | 核心实验OK；缺50UE绝对数值；"GNN迁移35,699 > MLP同规模33,843"是杀手论点但未被挖掘 |
| 竞品风险 | **PASS(附条件)** | 四要素无完全先例；Lee 2025需精确技术区分论证 |
| 薄弱环节 | **WARN** | sat_capacity调整和buffer扩大需进入论文正文；B2不可扩展是架构缺陷 |
| Ch1差异化 | **PASS** | 问题域/图结构/学习范式/泛化维度均不同 |

**关键发现**：GNN迁移(35,699)优于MLP同规模训练(33,843)——这个论点未被充分利用。论文应显式强调。

**最大风险**：top-K vs GNN贡献分配悬殊 + 50UE处GNN不如MLP的尴尬事实。

#### Ch3: leo-congestion-routing（拥塞/故障弹性路由）

| 维度 | 判定 | 核心理由 |
|------|------|---------|
| 核心数字 | **WARN** | E01坚实(3 seeds, p<0.0001)，但+18.2%/+17.8%是旧数据(surge=5.0)，实际应为+22.2%/+19.2%(surge=1.0)，需统一 |
| 漏洞修复 | **WARN** | F1/F2/F3/M2/M3已修；F4已分析弱化声称；F5(消融多seed)未修 |
| K-path迁移 | **PASS** | Contract amendment记录充分，技术理由清晰 |
| Ch1差异化 | **WARN** | 六维差异存在，但"同为GNN+路由+size gen"表层相似性易被质疑 |
| 竞品风险 | **WARN** | TELGEN泛化指标全面领先；DTAR不补做有风险 |
| 实验完备性 | **WARN** | Tier 1仅3/6通过；消融单seed；E12故障模式缺失 |
| 薄弱环节 | **WARN** | 优势窗口6-15%较窄；288节点ECMP更优(ratio=1.014)；pivot方向正确但E12缺失 |

**关键发现**：288节点(12×24)和96节点(8×12)异常值暴露Walker delta族内泛化并非单调。论文Table 2跳过96节点，审稿人若要求完整曲线会暴露。

**最大风险**：E12故障模式对比缺失（pivot为"故障弹性"却没有故障模式实验）+ Ch1同质化风险。

---

### Cross-Chapter 综合审查

#### 1. 论文结构连贯性

**当前布局**: Ch1路由(正常态) → Ch2切换(过渡态) → Ch3拥塞路由(优化态)

**问题**: Ch1和Ch3都是路由问题，R001推荐的层次递进型（正常态→优化态→异常态）中Ch3实际承担了"异常态"角色（故障弹性），与原定位"拥塞路由/优化态"不同。

**建议叙事调整**:
- Ch1: **基础路由的跨规模部署** — 正常态，离线规划，监督学习
- Ch2: **用户接入切换的跨规模扩展** — 接入层，在线DRL，UE数泛化
- Ch3: **故障弹性路由的跨规模在线决策** — 异常态，在线DRL，故障感知

递进逻辑：离线路由规划 → 在线接入决策 → 在线故障适应。从简单到复杂，从静态到动态，从监督到DRL。这个递进比"路由→切换→路由"更自然。

#### 2. 方法统一性

| | Ch1 | Ch2 | Ch3 |
|---|---|---|---|
| GNN类型 | GraphSAGE/GAT | 二部图MPNN | GAT |
| 学习范式 | 监督学习 | DDQN | PPO |
| 推理方式 | 加权Dijkstra | top-K+贪心 | K-path选择 |
| 泛化机制 | Orbital PE | 二部图等变性 | message passing |
| PE/位置信息 | Orbital PE(核心) | 边特征(SINR/elevation) | 无显式PE |

**统一叙事**: "图神经网络实现卫星通信跨规模泛化"——三章用不同GNN变体解决不同子问题，共享"GNN的结构化编码使零样本规模迁移成为可能"这一核心假设。

**递进**: Ch1证明PE使跨规模学习成为可能 → Ch2证明等变GNN使UE数泛化成为可能 → Ch3证明message passing使故障感知泛化成为可能。每章揭示GNN泛化的一个新维度。

**风险**: 方法差异较大，可能被审稿人视为"三个独立项目拼在一起"而非"统一框架的递进"。建议在绪论增加"GNN泛化机制谱"的概念图，展示PE/等变性/message passing三种机制的互补关系。

#### 3. Size generalization 叙事一致性

| | Ch1 | Ch2 | Ch3 |
|---|---|---|---|
| 泛化维度 | 卫星节点数 | UE数 | 卫星节点数 |
| 训练规模 | 66+100+200 | 20UE | 66 |
| 目标规模 | 720 (11×) | 100UE (5×) | 48-720 (0.7-10.9×) |
| 保留/退化 | 90.3%保留 | reward +467% vs MLP崩溃 | ≤10%退化 |
| 泛化机制 | Orbital PE | permutation equivariance | GNN结构化编码 |

**最大问题**: Ch1和Ch3都做卫星节点数泛化，且规模范围接近（Ch1: 66→720 11×, Ch3: 66→720 10.9×）。读者会问：这两章的泛化实验有什么本质区别？

**差异化论证**:
- Ch1: 泛化的是**路由策略**（方向偏好），核心贡献是Orbital PE使GNN学到规模无关的下一跳偏好
- Ch3: 泛化的是**负载均衡能力**，核心贡献是message passing在故障场景下的结构化信息传播
- 关键区别：Ch1无故障场景、监督学习；Ch3有故障场景、DRL、在线决策

**建议**: 在Ch3开头显式引用Ch1："第X章已证明GNN+PE可实现跨规模路由策略迁移，但假设无故障的理想网络。本章进一步挑战在线故障弹性场景下的规模泛化问题。"

#### 4. 竞品风险矩阵

| 竞品 | 威胁章 | 威胁等级 | 核心差异 | 风险点 |
|------|--------|---------|---------|--------|
| TELGEN (Zhou'25 ToN) | Ch1, Ch3 | **中-高** | TE vs 路由，WAN vs 卫星 | Ch3泛化指标全面落后(20x vs 10.9x, <3% vs ≤10%) |
| Lee 2025 (ICT Express) | Ch2 | **中** | 无DRL，无显式size gen | 二部图GNN+切换架构极接近 |
| GRLR (TVT'25) | Ch1 | **低** | 无size gen | 已复现并直接对比 |
| Kim 2022 BGNN (TWC) | Ch2 | **低-中** | 波束赋形非切换 | 二部图GNN+跨规模理论先驱 |
| GNN-ASSSP/DeepLaDu | Ch3 | **低-中** | 无故障弹性+无size gen | 活跃竞品 |

**总体竞品风险**: TELGEN是三章共同的最强竞品。建议在论文中统一处理TELGEN对比，而非每章分别讨论。

---

### 三章共同薄弱环节

1. **中文论文引用**: Ch1完全缺失(FAIL)，Ch2已补充(18篇)，Ch3未确认——学位论文硬性要求
2. **论文写作进度**: 三章全部素材就绪但正文零进度
3. **统计严谨性**: Ch2缺统计检验，Ch3消融单seed，Ch1仅单seed但核心实验充分
4. **数据版本不一致**: Ch3多处引用surge=5.0旧数据(+18.2%/+17.8%)，实际surge=1.0应为+22.2%/+19.2%

### 优先修复清单（按紧迫度）

1. **Ch3数据统一**: ~~所有文档改用surge=1.0数据~~ ✅ paper-materials.md 已使用正确数据
2. **Ch1中文引用补充**: ~~CNKI检索15-20篇~~ ✅ CN01-CN17 已存在于 04_literature.md (commit 71020c0)
3. **Ch3 E10/E11多seed**: ✅ 6配置×3seed全完成，全赢ECMP(ratio<0.80)，std<0.016，架构鲁棒性确认
4. **Ch3 E12故障模式对比**: ✅ 11/12 GNN赢ECMP。新增级联故障模式，修复regional不随fault_rate变化
5. **Ch2补N=30-40拐点**: 待用户决定（可跳过，Limitations中承认即可）

### 代码变更清单

| 文件 | 变更 |
|------|------|
| `simulator/failures.py` | 新增 `_inject_cascading()` 级联故障模式；修复 `_inject_regional()` 使用 failure_rate |
| `simulator/config.py` | failure_mode 注释更新 |
| `run_e12.py` | 新建：E12 故障模式对比实验脚本 |
| `run_e10_e11_multiseed.py` | 新建：E10/E11 多 seed 消融脚本 |

### E12 最终结果

| 模式 | 5% | 8% | 10% | 15% |
|------|-----|-----|------|------|
| random | 0.882 ✅ | 0.826 ✅ | 0.867 ✅ | 0.830 ✅ |
| regional | 0.867 ✅ | 0.915 ✅ | 0.867 ✅ | 0.873 ✅ |
| cascading | 0.915 ✅ | 0.937 ✅ | 1.070 ❌ | 0.901 ✅ |

cascading 10% 是唯一 GNN 输 ECMP 的场景（MLU=0.75，网络严重退化）。论文 Limitations 中讨论。

### E10/E11 多 seed 最终结果

| 配置 | MLU (mean±std) | GNN/ECMP |
|------|----------------|----------|
| L1 | 1.1433±0.016 | 0.773 |
| L2 | 1.1469±0.007 | 0.775 |
| L3 | 1.1584±0.016 | 0.783 |
| H2 | 1.1402±0.004 | 0.771 |
| H4 | 1.1571±0.011 | 0.782 |
| H8 | 1.1503±0.011 | 0.778 |

架构选择影响 <1.5pp，方法对超参高度鲁棒。

## 后续

1. 用户确认审查结论后，确定修复优先级和分工
2. 修复完成后进入三章论文写作
3. 绪论章节关系图 + "GNN泛化机制谱"概念图需在写作前设计
