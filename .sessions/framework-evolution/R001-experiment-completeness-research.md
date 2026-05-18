# [R001] 实验完备性缺口调研

> 2026-05-18 | 调研 | active

## 目标

多角度调研"实验完备性"的外部知识，确定框架增强方案。来源：S006 诊断。

## 记录

### 角度 A：ML 顶会论文检查表（3 子 agent 并发）

**关键结论：**

1. **NeurIPS 最严**：16 项强制 checklist（缺一 desk reject），实验相关核心 5 项：Q4 可复现性、Q5 代码开放、Q6 实验设置细节、Q7 统计显著性（error bars/CI/检验）、Q8 计算资源
2. **ICML 特点**：无强制 checklist，但审稿表有 "Claims and Evidence" 结构化段（5 子问题），要求审稿人逐项验证 claims 是否被 evidence 支持——**最接近声称-证据审计的设计**
3. **ICLR 最松**：仅鼓励 1 段 Reproducibility Statement，审稿表为自由格式
4. **REFORMS**（Kapoor et al., Science Advances 2024, Princeton）：19 位跨学科研究者共识，32 项清单覆盖 8 维度。是目前**最系统的跨领域 ML 报告标准**。定位：ML-based science（非 methods research）
5. **演变趋势**：2019-2021 纯可复现性 → 2022-2023 加伦理/社会影响 → 2024 加 LLM usage

**现有 checklist 的实验完备性覆盖缺口：**

| 未覆盖维度 | 说明 |
|-----------|------|
| Baseline 选择合理性 | 无要求论证"为何选这些 baseline" |
| 消融实验完备性 | 无结构化要求 |
| 超参数敏感性分析 | 极少被要求 |
| 评估指标选择论证 | REFORMS 提到但会议未覆盖 |
| 数据泄漏检查 | REFORMS 独有 |
| 外部效度/泛化性论证 | REFORMS 独有，会议仅暗示 |

**核心判断：所有现有 checklist 都是 reporting-level（投稿前自查），不存在 design-level（实验设计阶段）的完备性框架。这正是我们要填补的空白。**

**关键来源：**
- NeurIPS Checklist: https://neurips.cc/public/guides/PaperChecklist
- ICML 2025 Reviewer Instructions: https://icml.cc/Conferences/2025/ReviewerInstructions
- REFORMS (Science Advances): https://www.science.org/doi/10.1126/sciadv.adk3452
- Pineau Checklist v2.0: https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf

---

### 角度 B：IEEE 通信期刊审稿标准（3 子 agent 并发）

**关键结论：**

1. **IEEE 无强制 checklist**：TWC/TCOM/JSAC 均以自由文本审稿为主，实验充分性嵌入 Technical Correctness 和 Methodological Rigor 隐性评判。Editor 拍板（非投票制）
2. **TWC 评估 7 维度**：Novelty / Technical Correctness / Significance / Contemporary Interest / Presentation Quality / Wireless Substance / Methodological Rigor
3. **JSAC 特点**：themed issue 模式，acceptance rate ~31%，强调审稿意见必须详实具体
4. **IEEE TCRTS 审稿指南最详细**：明确要求审稿人评估 "Is the experimental evaluation thorough and reproducible?"

**通信领域实验"行业标准"（审稿人期望）：**

| 维度 | 标准 |
|------|------|
| Monte Carlo 仿真 | 1,000-10,000 次独立信道实现；BER<10^-5 需更多 |
| DRL seed 数 | 至少 3-5 个，推荐 stratified bootstrap 95% CI（Agarwal et al., NeurIPS 2021） |
| 场景数 | 至少 2-3 种不同网络规模/拓扑/负载 |
| Baseline 数 | 至少 2-3 个，必须含近年 SOTA |
| 统计报告 | mean±std，error bar 或 CI，运行次数明确 |
| 收敛曲线 | 迭代/优化/DRL 算法必须展示 |
| 参数透明 | 完整参数表，可复现 |

**常见实验相关拒稿原因：**

| 原因 | 表现 |
|------|------|
| Baseline 不足 | 未对比 SOTA，或用弱 baseline 膨胀改进 |
| 统计不严谨 | 无 error bar/CI，运行次数过少 |
| 场景单一 | 仅一个拓扑/参数设置 |
| 对比不公平 | baseline 未在相同条件下调优 |
| 假设不现实 | 信道/移动/流量模型过度简化 |
| 缺乏收敛分析 | 迭代算法无收敛曲线 |

**通信 vs ML 关键差异：**
- 通信以仿真为主无 benchmark 排行榜，对比公平性靠审稿人判断
- 代码分享鼓励但不强制
- 理论贡献权重高于实验增量

**关键来源：**
- TWC Policies: https://www.comsoc.org/publications/journals/ieee-transactions-wireless-communications/policies
- JSAC Policies: https://www.comsoc.org/publications/journals/ieee-jsac/policies-guidelines
- IEEE TCRTS Reviewer Guidelines: https://cmte.ieee.org/tcrts/guidelines-for-reviewers/
- Emil Bjornson (IEEE AE 经验): https://ma-mimo.ellintech.se/2023/01/01/peer-review-an-inside-story/
- Deep RL at the Statistical Precipice: https://arxiv.org/abs/2108.13264

---

### 角度 C：学术论证方法论（3 子 agent 并发）

**关键结论：**

1. **Toulmin 模型**：6 组件（Claim/Grounds/Warrant/Backing/Qualifier/Rebuttal）可映射到论文章节结构，但**局限明显**——无实验设计维度、无统计显著性概念、无对比基线概念、无复现性评估。适合做论证结构骨架，不适合单独作为实验完备性框架
2. **Hermes Pipeline 的 Claim-Experiment-Evidence 表格**：最实用的声称-证据映射格式。核心规则："If an experiment doesn't map to a claim, don't run it." 三列结构：Claim | Experiment | Expected Evidence
3. **Walton 的 96 种论证模式 + Critical Questions**：每种论证模式配一组必答问题，回答完毕即可判断论证是否成立。**可直接移植为"证据充分性检查清单"**
4. **GRADE（医学，最成熟）**：5 个降级维度（偏倚风险、不一致性、间接性、不精确性、发表偏倚）+ 3 个升级维度。**升降级机制适合设计自动化证据评估**
5. **Wang et al. (2021, JASIST)**：对 40 篇论文全文本标注 17 类论证组件，发现不同学科证据类型分布不同（生物医学偏 factual evidence 58%，信息科学偏 theoretical evidence）

**可直接借用的概念：**

| 概念 | 来源 | 适用方式 |
|------|------|---------|
| 升降级机制 | GRADE | 初始评级 + 明确维度逐一调整 |
| Critical Questions | Walton | 每种论证模式配必答问题 |
| Claim-Experiment-Evidence 表 | Hermes | 声称-实验-预期证据三列映射 |
| 间接性（indirectness） | GRADE/NHMRC | 仿真环境与真实场景的匹配度评估 |
| Width vs Depth | Liu & Xiong | 多角度并行证据 + 层级递进证据 |
| 多维度矩阵 | NHMRC | 独立维度分别评级，非单一分数 |

**关键来源：**
- Liu & Xiong 2024 (Nature): https://www.nature.com/articles/s41599-024-03151-w
- Hermes Pipeline: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-research-paper-writing
- Walton Argumentation Schemes (Cambridge): https://www.cambridge.org/core/books/argumentation-schemes/
- GRADE 六框架对比: https://www.ncbi.nlm.nih.gov/books/NBK121300/
- Wang et al. 2021 (JASIST): 论文论证结构分析

---

### 角度 D：论文拒稿原因分析（3 子 agent 并发）

**关键结论：**

1. **实验相关拒稿原因排序**（综合多方来源）：
   - Missing baselines（未对比 strong baseline / 不公平调参）
   - Weak or missing ablation studies
   - Insufficient experiments / limited datasets（仅 1-2 个 benchmark）
   - Lack of statistical significance（无 error bars / CI / multiple seeds）
   - Data leakage / evaluation shortcuts
   - Overclaiming from narrow evidence
   - Reproducibility gap
   - Incremental without statistical significance

2. **Rebuttal 阶段最常要求的补充**：补充 ablation、补充 strong baseline、多数据集验证、统计显著性报告、计算开销分析、超参数敏感性、代码开源

3. **系统性分析数据集**：
   - RbtAct（arXiv 2603.09723）：75,542 条审稿-回复对，Experiments 是最大批评类别之一
   - PeerRead（Kang 2018）：14.7K 篇审稿数据
   - Wu et al. 2024：5,036 篇拒稿的 LDA 主题分析，Methodology 是高影响期刊首要拒稿维度
   - Jung et al. 2025：28K+ ICLR 投稿分析，rebuttal 阶段决定性超过初始评分

4. **核心验证**：**不存在"实验充分性"的统一操作化定义**，因此没有量化研究与录用率的关联。NeurIPS 一致性实验显示审稿一致率仅 22-26%

5. **RbtAct 关键发现**：实验相关批评被 defend-without-change 比例 45.4%（远高于写作类的 20.9%），作者最抗拒实验修改

**关键来源：**
- RbtAct: https://arxiv.org/abs/2603.09723
- Manusights ML Review Matrix: https://manusights.com/blog/pre-submission-review-machine-learning
- Alignment Forum ML Writing Guide: https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/
- Wu et al. 5K 拒稿分析: https://www.sciencedirect.com/science/article/pii/S277242472400012X
- Jung et al. ICLR 28K 分析: https://openreview.net/forum?id=iSqOXQ7bCc

---

### 角度 E：实验设计最佳实践（3 子 agent 并发）

**关键结论：**

1. **好实验的核心原则**（综合 Alignment Forum / ICML Best Practices）：
   - Quality > Quantity：1-2 个 truly compelling 实验远胜一堆 loosely relevant 实验
   - Claim-driven：每个实验必须服务于验证某个具体 claim
   - Extensive red-teaming：自己主动找漏洞，preemptively 排查 alternative explanations
   - Diverse lines of evidence：qualitatively different 的证据线指向同一结论比 similar methodology 的实验更有说服力

2. **可复现性检查表全景**：

| 检查表 | 来源 | 特点 |
|--------|------|------|
| REFORMS | Princeton, 2024 | 32 项/8 类，最全面，面向 ML-based science |
| NeurIPS Checklist | 2021 起 | 16 项强制，面向 methods research |
| NERVE-ML | Carlson 2025, J. Neural Eng. | **唯一同时关注复现性与结论有效性**，验证策略必须匹配科学问题 |
| ML Reproducibility | Piech 2019 | 聚焦实验报告完整性 |

3. **核心洞察**："可复现的错误结论仍然是错误的"（REFORMS/NERVE-ML 共识）。可复现性是完备性的必要非充分条件

4. **不存在 methodology-level 框架**：所有现有倡议都是 reporting-level（投稿前自查），无"claim → evidence type → experiment design"的系统映射。最接近的是：
   - NERVE-ML（验证策略匹配科学问题）
   - VVUQ（科学计算：verification → validation → uncertainty quantification 分层结构）

5. **不可复现典型案例**：EEG 随机标签 AUC=0.979（数据泄漏）、93 篇 DL-in-SE 论文重跑均无法复现、SMOTE oversampling 泄漏

**好实验 vs 差实验对比：**

| 维度 | 好 | 差 |
|------|---|---|
| Baselines | SOTA + 经典，均充分调参 | 弱 baseline 或不调参 |
| 统计 | mean±std，多次运行，显著性检验 | 单次运行结果 |
| Ablation | 系统化逐一移除，量化贡献 | 无或一次改多变量 |
| 诚实度 | 报告失败案例和 limitations | 只报最好结果，cherry-pick |
| 设计逻辑 | 每个实验对应一个明确 claim | 罗列实验不解释 why |

**关键来源：**
- ICML Best Practices: https://icml.cc/Conferences/2022/BestPractices
- Alignment Forum ML Writing: https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/
- NERVE-ML: https://pmc.ncbi.nlm.nih.gov/articles/PMC11948487/
- arXiv 2511.21354 Best Practices for ML Experimentation

---

## 五角度综合分析

### 核心发现

1. **不存在 design-level 的实验完备性框架**（5 个角度一致确认）。所有现有工具都是 reporting-level checklist
2. **创新空间**：claim → evidence type → experiment design 的系统映射是空白
3. **可借鉴组件**：
   - NeurIPS Q7（统计显著性）+ ICML Claims & Evidence 段 → 声称-证据审计
   - Hermes Pipeline 的三列表 → 映射格式
   - GRADE 升降级机制 → 自动化评估
   - Walton critical questions → 检查清单生成
   - VVUQ 分层结构 → 验证框架
   - NERVE-ML 验证策略匹配 → 结论有效性
4. **通信领域特殊需求**：仿真为主无 benchmark 排行榜、对比公平性靠审稿人判断、理论贡献权重高

### 对框架设计的初步方向（待与用户讨论）

1. **提取层（gw-read）**：精读时增加"实验完备性提取"维度——指标清单/统计检验/baseline 矩阵/消融/鲁棒性/声称-证据对应
2. **对标层（Contract）**：从竞品论文实验设计推导领域标准，与自身实验计划交叉审计
3. **声称-证据映射**：Hermes 三列表格式，从 Contract 声称出发倒推实验需求
4. **审计层（Execute）**：代码实现与 Contract 声明的一致性检查

### 待讨论：竞品论文实证分析角度

5 角度调研完成后，需要从已有论文库中系统提取实验完备性维度。具体分析角度待与用户讨论确认。

### 角度 1：声称-证据架构映射（3 子 agent × 8 篇论文 = 24 篇）

**方法**：每篇论文提取 intro/conclusion 中显式声称 → 映射到具体实验/表/图 → 分析声称 scope 是否匹配证据 scope。

**24 篇论文 88 个声称的统计：**
- Match: 67 (76%)
- Overclaim: 12 (14%)
- Partial/Underclaim: 9 (10%)

**按论文来源分层：**
- arXiv 预印本（16 篇）：overclaim 率约 20%
- DOI 期刊论文（8 篇）：overclaim 率约 5%

**最普遍的 overclaim 模式（按频率）：**
1. **仿真规模 vs 声称泛化**（~10/24 篇）：小规模验证但声称 practical/large-scale 适用性。典型案例：200m×200m 12 用户声称 SAGIN 适用；3BS 3 用户声称 NTN 高效方案
2. **条件泛化**（~4/24 篇）：单一网络/场景结果泛化为 universal 声称
3. **前瞻性声称**（~2/24 篇）：基于观察提出"potential"但无实验验证

**最可靠的声称类型（overclaim 风险最低）：**
1. 理论保证 + 实验验证（LISL Matching、Two-time-scale DRL）— 0% overclaim
2. 工具/系统论文的量化声称（xeoverse：wall-clock time、% error vs real data）
3. 使用 bounded 限定词（"up to X%"）而非 universal 声称

**验证充分性排名（Top 5）：**
1. Starfield (2601.10083) — 真实星座+多流量+鲁棒性+消融+理论下界
2. LARRI (10.1109_ton) — 6 个真实拓扑+7 个 baseline
3. PathGNN (10.1109_jsac) — 链路故障场景评估+泛化验证
4. LISL Matching (2601.21914) — 收敛定理+大规模验证
5. Adaptive Rewards (2604.03562) — 因果探测+多 seed+冷启动区分

**关键洞察：声称 scope 控制是区分好论文和差论文的最显著因素。好论文用"up to"/"in tested scenarios"等限定词；差论文用"all"/"practical"/"efficient"等宽泛声称。**

---

### 角度 2：证据多样性 vs 证据冗余（3 子 agent × 8 篇论文 = 24 篇）

**方法**：对每篇论文分类证据类型、评分多样性(1-5)和冗余性(1-5)、判断是否存在"diverse lines of evidence"。

**24 篇论文统计：**
- 平均多样性：3.75/5（大多数论文有 3-4 种证据类型）
- 平均冗余性：3.6/5（大多数论文核心维度不冗余）
- Diverse lines 存在：~63%（15/24 篇）

**多样性评分分布：**
- 5 分（6 篇）：Starfield、LISL Matching、xeoverse、GNN Multicast、LLM-DRL、LARRI、PathGNN
- 4 分（5 篇）：Two-time-scale DRL、Multi-Sat BH、SAGIN AoI、DeepLaDu、Tyche
- 3 分（9 篇）：多数常规 DRL 论文
- 2 分（4 篇）：DHO、Microservice GNN、GKAE/SDN、RIS Phase

**高分论文的共性特征：**
1. 至少含一条"非标准"证据线（因果探针/真实数据验证/与最优解对比/理论收敛保证）
2. 理论证明 + 实验验证的双重支撑
3. 超越"收敛+对比+消融"模板化的实验设计

**关键洞察：大多数论文的"diverse evidence"实际上是模板化的（收敛曲线+性能对比表+消融实验），而非真正从 qualitatively different 的角度验证结论。真正多样的证据（如与最优解对比、真实数据交叉验证、因果机制分析）在领域中仍然稀缺。**

---

### 角度 3：统计规范性 + Baseline 合规性（3 子 agent × 8 篇论文 = 24 篇）

**方法**：逐篇审计统计报告（seed/error bar/检验/运行次数）和 baseline 合规性（数量/类型/来源/公平调参）。

**24 篇论文汇总（触目惊心）：**
- **统计规范性平均分：1.35/5**
- **Baseline 合规性平均分：2.35/5**

**统计规范性详情：**
| 维度 | 报告比例 |
|------|---------|
| Random seed 数量 | 1/24（LLM-DRL: 3 seeds） |
| Error bar / CI | 2/24（LLM-DRL: mean±std; PathGNN: 消融部分 std） |
| Formal 统计检验 | 0/24 |
| 独立运行次数 | 2/24（2510.11109: 20 instances; 2501.06482: 1000 随机化） |

**Baseline 合规性详情：**
| 维度 | 报告比例 |
|------|---------|
| 实现来源声明 | 2/24（xeoverse: 开源工具; Dueling DDQN: 自实现+适配声明） |
| 公平调参声明 | 2/24（Dueling DDQN: offline→online 适配; PathGNN: 共享 CLF 训练数据） |
| Baseline 数量 ≥5 | ~10/24 |
| 含 DRL/ML baseline | ~15/24 |

**例外（评分最高的论文）：**
- LLM-DRL (2604.03562)：统计 4/5，baseline 3/5 — 唯一使用多 seed + std 的论文
- xeoverse (2406.11366)：统计 1/5，baseline 4/5 — 明确声明公平比较条件
- PathGNN (10.1109_jsac)：统计 2/5，baseline 4/5 — 消融有 std + 声明共享训练数据
- Dueling DDQN (2605.02416)：统计 1/5，baseline 4/5 — 明确声明 offline→online 适配

**核心判断：LEO 卫星 + ML/DRL 领域的统计规范性基本为零。几乎所有论文的性能对比都无法判断统计显著性。这是一个系统性问题，不是个别论文的缺陷。**

---

### 角度 4：消融设计模式 + Alternative Explanation 覆盖（3 子 agent × 8 篇论文 = 24 篇）

**24 篇论文汇总：**

| 维度 | 比例 |
|------|------|
| 真正逐模块消融 | ~4/24（17%） |
| 任何形式的"消融"（含参数扫描） | ~15/24（63%） |
| Alternative explanation 排除 | ~6/24（25%） |
| Red-teaming | 1/24（4%） |

**消融设计模式（按频率）：**
1. **参数扫描冒充消融**（最常见）：变化 GNN 层数/学习率/discretization 等，但不拆解组件
2. **替换为简化版本**：GNN→FC、active→passive RIS、with→without attention
3. **子系统删除**：移除 cloud/ISL 等子系统
4. **逐模块替换**（最罕见但最有价值）：如 2510.11109 分别替换 GAT/LSTM/Pointer

**系统性盲点：**
- State/observation space 特征维度消融**完全缺失**（无一篇做）
- 无一篇讨论"性能提升可能来自更大模型容量而非方法本质"
- 无一篇讨论"GNN 性能可能来自更大 receptive field 而非拓扑建模"
- 所有论文将性能提升直接归因于提出方法，无例外

**例外论文：**
- LLM-DRL (2604.03562)：唯一做 red-teaming 的论文（整篇论文就是证明 adaptive reward 有害）
- PathGNN (JSAC)：主动分析 MARL-GNN 的 failure mode
- LARRI (TON)：主动指出 "prediction accuracy ≠ routing performance"

---

### 角度 5：通信领域特有维度（3 子 agent × 8 篇论文 = 24 篇）

**24 篇论文通信特有维度覆盖率：**

| 维度 | 覆盖率 | 典型问题 |
|------|--------|---------|
| 信道模型真实性 | ~25% | 多数简化为 FSPL+AWGN，雨衰/闪烁/仰角衰落几乎无人建模 |
| 拓扑多样性 | ~30% | 多数仅单一星座配置，极少跨星座（不同轨道高度/倾角/密度） |
| 收敛曲线 | ~85%(DRL) | DRL 论文普遍展示但多定性描述 |
| 参数敏感性 | ~60% | 多数仅 1-2 个变量，缺乏系统扫描 |
| 复杂度 vs 性能 | ~50% | 理论 O() 较多，实际推理延迟极少 |

**信道模型分层：**
- **真实**（3GPP/ITU-T/物理模型）：DeepLaDu(FSO+Rayleigh)、SAGIN AoI(Gamma-Gamma+Nakagami)、xeoverse(ITU-T+天气)、GNN Scheduling(3GPP UMa)
- **中等**（路径损耗+基本衰落）：多数论文
- **理想化**（纯带宽/延迟模型）：DLBR、RIS Phase

**拓扑多样性分层：**
- **多样**（≥3 种配置）：ISL Patterns(10+pattern)、xeoverse(25-1584 sat)、Starfield(多星座)、LISL Matching(多星座)、DeepLaDu(100-1584)
- **单一**：其余多数论文

**核心判断：通信论文的物理层建模普遍不足。LEO 卫星 DRL 论文在信道模型真实性上与 IEEE 审稿人期望存在系统性差距。**

---

### 角度 6：VVUQ 分层覆盖（3 子 agent × 8 篇论文 = 24 篇）

**方法**：Verification（代码正确性）→ Validation（模型与现实一致性）→ Uncertainty Quantification（不确定性量化），每层 1-3 分，总分 3-9。

**24 篇论文 VVUQ 平均分：5.8/9**

| VVUQ 层 | 平均分 | 主要问题 |
|---------|--------|---------|
| V1 Verification | 2.0/3 | 多数仅做 baseline 对比，无解析解/单元测试 |
| V2 Validation | 2.1/3 | 有真实参数但极少实测交叉验证 |
| V3 Uncertainty | 1.4/3 | 全面薄弱，几乎无 CI/统计检验/极端条件 |

**VVUQ 分层覆盖关键数据：**
- 解析解/最优解对比：4/24（17%）
- 真实数据交叉验证：3/24（12.5%）— xeoverse、LARRI、PathGNN
- 因果机制分析：1/24（4%）— Adaptive Rewards
- 置信区间/统计检验：1/24（4%）— Adaptive Rewards

---

## 六角度综合结论

### 领域实验完备性现状（24 篇 LEO 卫星通信论文）

| 角度 | 核心指标 | 数值 | 评级 |
|------|---------|------|------|
| 声称-证据映射 | Overclaim 率 | 14% | 中 |
| 证据多样性 | 平均多样性评分 | 3.75/5 | 中 |
| 统计规范性 | 平均评分 | **1.35/5** | 极差 |
| Baseline 合规性 | 平均评分 | 2.35/5 | 差 |
| 消融设计 | 真正逐模块消融率 | 17% | 差 |
| Alt-Explanation 覆盖率 | 25% | 差 |
| 信道模型真实性 | 使用标准模型率 | 25% | 差 |
| 拓扑多样性 | 多拓扑测试率 | 30% | 差 |
| 复杂度报告 | 覆盖率 | 50% | 中 |
| VVUQ 总分 | 平均 | 5.8/9 | 中 |
| Red-teaming | 覆盖率 | 4% | 极差 |

### 三层框架维度（对框架设计的直接输入）

**Tier 1: 必做（>50% 论文缺失，不做会被审稿人质疑）**
- 多 seed + error bar / CI
- Baseline 实现来源声明
- Baseline 公平调参声明
- 逐模块消融（非参数扫描冒充）
- 信道模型参数溯源（引用 3GPP/ITU-T 标准）
- 声称 scope 控制（用"up to"/"in tested scenarios"而非"all"/"practical"）

**Tier 2: 应做（>70% 论文缺失，做了显著提升论文质量）**
- 统计显著性检验
- Alternative explanation 排除
- 声称-证据 scope 匹配审计
- Diverse lines of evidence
- 跨拓扑/星座验证
- 计算复杂度 + 推理延迟报告

**Tier 3: 加分（>90% 论文缺失，做了是亮点）**
- Red-teaming / 自我找漏洞
- 真实数据交叉验证
- 因果机制分析（causal probing）
- 与最优解对比（DP/理论下界）
- 极端条件测试
- 系统性不确定性量化

### 框架增强方案（待下一对话实施）

1. **提取层（gw-read）**：精读时增加"实验完备性提取"模板，对标 Tier 1-2 维度
2. **对标层（Contract）**：从竞品论文实验设计推导领域标准，与自身实验计划交叉审计
3. **声称-证据映射**：Hermes 三列表格式 + scope 匹配检查
4. **审计层（Execute）**：代码实现与 Contract 声明的一致性检查

## 后续

- 调研全部完成，写入 PROMPT 文件供下一对话实施框架改动
- **框架改动已实施完成**（H007，2026-05-18）：7 个文件已修改
  - templates.md：增加 3 个模板（实验完备性提取 / 声称-证据映射表 / 自检清单）
  - gw-read.md：增加"实验完备性提取"维度（3-5 篇核心竞品论文）
  - domain-comms.md：增加 §7 通信特有实验维度（信道模型分级/拓扑多样性/DRL 收敛/复杂度）
  - contract.md：Step 2 增加声称-证据初步映射，Step 5 增加实验完备性对标检查（Tier 1 门控）
  - execute.md：Step 0 增加 Contract 审计前置检查点
  - overview.md：增加"实验完备性对标"原则
  - CLAUDE.md：跨阶段护栏表增加索引行
- 下一个使用框架的项目验证改动效果
