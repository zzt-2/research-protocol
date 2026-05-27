# Handoff: 论文精读 → 文档叙事修改

> 来源: S006-ch2-domain-verify-and-thesis-positioning | 交接目标: 新对话精读学位论文后执行文档叙事修改
> 文件名: H004-thesis-reading-and-doc-update.md

## 已完成边界

### Ch2 领域归属验证（6 个问题全部完成）

| 问题 | 结论 | 影响 |
|------|------|------|
| Q1 跨规模泛化是切换领域挑战？ | **否**。5 篇综述均未列出 | 叙事必须改为"技术迁移" |
| Q2 top-K 是标准做法？ | 有先例非标准（2 篇） | 降为工程选择 |
| Q3 二部图 GNN 有先例？ | 接近标准（4+ 篇），Lee & Lim 2025 最直接竞争者 | 必须显式区分架构差异 |
| Q4 指标是通行指标？ | 部分覆盖。Jain's 非通行(17%)，缺 system throughput | Jain's 降级+补 throughput |
| Q5 DDQN 有先例？ | 标准做法（4+ 篇） | 不构成贡献 |
| Q6 核心指标覆盖？ | 缺 system throughput(58%通行率) 和 ping-pong rate | 需补 |

### 论文定位调整

- **旧主线**："GNN 结构化编码使零样本规模迁移成为可能"
- **新主线**："GNN 在 LEO 卫星网络中的系统性应用研究——覆盖路由、切换、故障弹性三个场景"
- **Size generalization**：从每章核心贡献 → 跨章共享优势
- **三章差异化**：Ch1 监督学习路由（拓扑规模迁移）→ Ch2 DRL 切换（UE 规模迁移）→ Ch3 故障弹性路由（故障鲁棒性+规模）

### 硕士论文标准确认

- 要求"一定的新见解或新内容"，非"重大创新"
- 当前项目工程量和实验规范远超同方向够格线
- 参照：Shi 2024 用 14 节点 3 baseline 无消融发了 SCI
- 真正风险在叙事不在实验

### 事实错误已修正（5 处）

1. Ch2 decision_log: Lee 2025 "非二部图" → 实际用二部图 ✅
2. Ch3 master-state E06: PASS → 退化（新拓扑下 720 节点 GNN/ECMP MLU=1.108）✅
3. Ch3 master-state E12: 10/12 → 11/12 ✅
4. Ch1 06_formulas_symbols: retention 范围 [0,1] → (0,+inf) ✅
5. （注：04_literature.md 本身正确描述了 Lee 使用二部图，无需修改）

## 不要做什么

- **不要在精读前做叙事类修改**：贡献声称降级、措辞调整等需要先看别人怎么写
- **不要声称方法论突破**：领域验证已确认三项核心技术（二部图 GNN、top-K、DDQN）各单项都不新颖
- **不要把 size generalization 声称为领域挑战**：Ch1 和 Ch2 的领域验证一致确认这是 GNN 理论性质
- **不要把 Jain's fairness 作为切换领域主指标**：通行率仅 17%，属资源分配领域
- **不要忽视 Lee & Lim (2025)**：这是 Ch2 最直接竞争者，必须在 related work 显式讨论

## 必读

按优先级排列：

1. **`.sessions/thesis-chapter-fixes/S006-ch2-domain-verify-and-thesis-positioning.md`** — 本轮完整记录（领域验证+标准调研+扫描结果）
2. **`.sessions/thesis-chapter-fixes/topic-index.md`** — 更新后的不变量和结论
3. **`projects/leo-mega-constellation-gnn-routing/paper_materials/01_research_context.md`** — Ch1 贡献声称最集中的文件
4. **`projects/leo-ntn-handover-drl/paper_materials/04_literature.md`** — Ch2 竞品分析（Lee & Lim 讨论）
5. **`projects/leo-congestion-routing/paper-materials.md`** — Ch3 叙事（已重写，作为参照）
6. **`projects-overview.md`** — 三章总览（定位需更新）

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| P0 文档修改 14 处（叙事/措辞类） | 贡献声称要诚实 | 精读后执行 | 精读完成确定写法 |
| P1 文档修改 22 处 | 文档质量 | 精读后执行 | P0 完成后 |
| Ch2 补实验（全部） | 实验完整性 | 未开始 | 精读+文档修改后 |
| 跨章元分析框架 | 论文结构 | 未开始 | 文档修改后 |
| 每章失败/边界分析 | 分析深度 | 未开始 | 文档修改后 |
| Ch1 paper-materials 重写 | 数据+叙事更新 | 未开始 | P0 修改后 |

## 下一轮

### Phase 1: 精读学位论文（新对话）

1. 在 `.sessions/thesis-structure-research/` 专题下续接
2. 精读 ≥5 篇通信/网络方向学位论文（博士+优秀硕士），重点关注：
   - 应用型论文如何声称贡献（不声称创新时的写法）
   - 系统性研究类论文的结构和叙事
   - 多章论文如何避免重复感
   - 失败/边界分析的写法
   - 贡献降级措辞的学术表达方式
3. 输出：写法规范文档（具体措辞模板+结构参考）

### Phase 2: 执行文档修改（同一对话或后续）

基于精读确定的写法规范，批量执行 P0+P1 修改：

**P0（14 处叙事/措辞类，必须改）**：
- Ch1: "核心创新"→"核心贡献"（01/04_research_context），"首次实证"→"首次系统性验证"，Orbital PE 标注标准特征工程，加权 Dijkstra 补 GDDR 2021 先例，E2E delay 为主指标+stretch 降级，delay retention 标注自造指标
- Ch2: contract M4 Jain's 降级+补 throughput，03_experiments 补 throughput 列+Jain's 标注辅助，01_research_context 强调集中式 DRL 差异
- Ch3+: projects-overview 三章定位更新，topic-index 不变量已更新

**P1（22 处，建议改）**：详见 S006 完整记录

### Phase 3: Ch2 补实验

全部做（多多益善）：
- System throughput 独立报告（代码已有，加输出行）
- Ping-pong rate（需改仿真代码）
- 多 seed 验证（~6 min/seed）
- N=30/40 规模扩展

### Phase 4: 跨章元分析 + 失败分析

- 结论章统一讨论"GNN 在什么条件下有效"
- 每章 worst-case 分析
- 三章数据横向对比

## 验证阈值

| 验证项 | PASS 标准 | 来源 |
|--------|----------|------|
| 精读覆盖 | ≥5 篇学位论文 | 硕士论文标准调研 |
| 写法规范 | 有具体措辞模板（≥10 条 before→after） | 精读产出 |
| P0 修改 | 全部 14 处完成 | S006 扫描 |
| 三章定位 | 不变量段落描述一致 | topic-index |
