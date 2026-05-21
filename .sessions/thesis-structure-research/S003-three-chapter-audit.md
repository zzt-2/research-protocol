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

无（新对话填写）

## 后续

无（新对话填写）
