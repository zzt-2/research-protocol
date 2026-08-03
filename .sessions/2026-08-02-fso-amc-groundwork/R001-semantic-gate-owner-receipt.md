# [R001] Semantic-Gate Owner Receipt — 四判据权威 owner 逐字核对

> 2026-08-03 | 关联：专题 `2026-08-02-fso-amc-groundwork` / D005（Step 3 语义门纠偏）/ TL-31 + TL-33
> worktree: `.worktrees/rdl-method-production-v2` @ `482d9ad19a00d72a0fb3bbc5e56ba9022577c410`
> 复算环境：`~/.venvs/torch/Scripts/python.exe`（仅用于 sha256，无网络）

## 调研问题

D004/V005/S004/literature_notes_amc §6 在 GW Step 3 终态判定中，使用了**自创的四判据标签** `problem_truth / actionability / novelty / thesis_fit` 作为 Step 3 terminal gate（5 候选 Q# 逐条评这 4 项，无一全过 → STEP3_NO_VALID_PROBLEM）。

本 receipt 回答：**协议唯一合法的"问题四判据"权威 owner 是哪些文件、哪几行、SHA256 是什么、原文是什么**？以及 **Step 3 / Step 3.5 / Step 4a 各自的职责边界**——哪些判断必须留给 Step 4a/MVE，不能前移到 Step 3。

## 发现

### A. 四判据权威 owner（唯一合法来源）

按 `AGENTS.md` 文档职责边界表，"核心术语"的唯一 owner = `stages/glossary.md`；"模板定义"的唯一 owner = `templates.md`。本 receipt 逐字核对二者。

| owner 文件 | 相对路径 | SHA256（本轮实测） | 四判据定义行号 |
| --- | --- | --- | --- |
| 核心术语 owner | `stages/glossary.md` | `eafa43e3b0c941d90b36e4469e28346621ee82ee83d6fed558410073f610e74b` | L22-31（"四条判据"小节） |
| 模板 owner | `templates.md` | `bdc93d41a5e4eac726074d2754c45a2d563ca48bebb0e76a3edef01caa7b9e41` | L301（Q# 表头）+ L308/L311（填表规则）+ L371（每篇提取） |

### B. 四判据原文（逐字，glossary.md L22-31）

> ### 四条判据（必须同时满足）
>
> 一个问题必须**同时**满足以下四条。任一不满足 = 不是问题。
>
> | # | 判据 | 反例 |
> |---|------|------|
> | 1 | **具体技术矛盾**：M / C / A 三要素都明确，是句子级、可解的陈述 | … |
> | 2 | **有方法产出形态**：解决它会长出可被他人复用的产出（设计公式/准则/算法/框架/可引用的闭合解族），不只是孤立的一次性数值计算 | … |
> | 3 | **有近期 baseline 可对标**：问题里天然嵌着具体 SOTA 方法 M，改进它（对标**近期顶刊**，年份范围由项目 `voice.md` 确认） | … |
> | 4 | **能做可量化对标**：自己的产出 vs baseline M 有可量化的对照（算法对算法、公式对公式、或曲线族对曲线族；每章/篇 1-2 个对标对象） | … |

templates.md L301 的 Q# 表头与此一一对应：`判据1 矛盾 | 判据2 产出形态 | 判据3 近期baseline | 判据4 可量化对标`。L308 填表规则："四判据逐条标 ✅/❌ + 一句话理由（❌ 要说清缺什么）"。

### C. 自创标签 vs canonical 四判据的映射

| 自创标签（错误，D004/V005/S004 用） | canonical 判据 | 是否等价 |
| --- | --- | --- |
| `problem_truth` | 判据 1（具体技术矛盾 M-C-A） | **不等价** — problem_truth 被我用来要求"A 的失效已被证明"，远超判据 1（只要求 M-C-A 明确、可证伪）。这是把 Step 4a/MVE 的证据前移 |
| `actionability` | 判据 2（方法产出形态） | 近似等价 |
| `novelty` | （无直接对应；最近邻 = 升级规则 + 三概念对照 + 空集处置） | **不属四判据** — 新颖性是 glossary"问题 vs 空白"对照表的内容，由 Step 3.5 竞争闭包 + Step 4a 维度 B 处理，不是 Step 3 terminal gate 的一列 |
| `thesis_fit` | 判据 3 + 判据 4（baseline 可对标 + 可量化对标） | 近似等价但拆成了两项 |

**关键错位**：`problem_truth` 和 `novelty` 这两列把 Step 4a/MVE 和 Step 3.5 的职责前移到了 Step 3，造成循环门控——例如 Q1 我判 problem_truth "⚠部分"理由是"A 的失效需证明退化（MVE 级）"，Q3 判 problem_truth "❌"理由"A 是待证假设需 oracle/MVE 证据"——这些都是**要求 Step 3 就拿到 Step 4a/MVE 的证据**，违反 FR-22。

### D. Step 3 / Step 3.5 / Step 4a 各自职责（owner 逐字核对）

| Step | owner 文件 | SHA256（本轮实测） | 职责（逐字/精确定位） |
| --- | --- | --- | --- |
| Step 3 精读 | `stages/gw-read.md` | `ebfa3f4cdc9a49f73449aa89579bee3d23ca23a0d1ef5a8cfacaebd76b1fc2d8` | L86 第 7 项"问题提取"：每篇按 glossary 拆 M/C/A + 过四判据（逐条标 ✅/❌+理由）+ A 的论文定位 + 方法产出形态。L198 质量门槛"研究问题清单非空[MUST]：至少含 1 条过四判据的 Q#，一条都没有 = Step 3 未产出可进 Step 4a 的问题候选，禁止离开 Step 3（处置见 glossary 候选全被筛掉时）" |
| Step 3.5 定向补充 | `stages/gw-supplement.md` | `849e9a112646b012979b930bcbce57989b71974c4863c3b58b9d537fdd4bd6bc` | 全文：用精读新认知做定向检索 + 引用链分析 + 新论文处理 + 更新综合分析。L57-64 检索充分性判据（关键词矩阵+源覆盖+引用链+收敛性+3 轮上限） |
| Step 4a 可行性 | `stages/gw-feasibility.md` | `11fca7377098b57e84d2a42b75463494baa6f93e4592f745622cf08bd8025ed4` | §A0 §0 前置门控（L37-46）：候选须对应某个四判据全过的 Q#。维度 A0（性能间隙/问题结构适配/跨域先例/MDP/负面证据/先验覆盖）、A'（竞争维度分解）、A（结构优势）、B（新颖性-可行性解耦+空白零假设）、D（MVE）|

**职责分离的逐字证据**：
- **Step 3 要求的是文献支持、具体、可证伪的失效假设 A**：gw-read.md L86 "问题提取…该论文解决的研究问题，按 glossary 拆 M/C/A 三要素"。判据 1 只要求"M/C/A 三要素都明确，是句子级、可解的陈述"——可解 = 可证伪（falsifiable），**不是"已证伪"**。
- **Step 3 不要求已经用 MVE 证明退化**：glossary L22 "任一不满足 = 不是问题"，判据 1 是"明确、可解的陈述"，不是"已被实验证明的退化"。Step 3 的产出是"问题候选"（候选 Q#），不是"已验证的失效"。
- **Step 3.5 负责定向补充检索、相邻工作和 novelty closure**：gw-supplement.md 全文。glossary"候选全被筛掉时"流程①=回扩检索（Step 3.5），novelty 在此闭合。
- **Step 4a 才负责性能间隙、方法适配性、核心假设验证**：gw-feasibility.md 维度 A0（性能间隙）/A（结构优势）/B（新颖性-可行性解耦+空白零假设检查）/D（MVE 实证）。FR-21 oracle 上界也只在 Step 4a 维度 D 收尾（TL-32/FR-25）。

### E. glossary"候选全被筛掉时"出口（L65-71，逐字）

> 四判据是过滤器，存在现实概率"精读完所有线索一条都不合格"。`gw-read.md` 的"问题清单非空"是单向门（堵），这里给出口（疏）。当问题清单为空（所有候选都过不了四判据）时，按顺序：
> 1. **先回 `gw-search.md` 扩关键词重检索**：当前线索库可能偏窄。换同义词、换子领域、查被引网络。补检索后再精读、再过四判据。
> 2. **扩检索后仍空 → 上报用户决策**：可能是 C 条件本身太窄…**禁止 agent 自己拍板放宽 C 条件**。

→ STEP3_NO_VALID_PROBLEM **不是终点**，它触发 Step 3.5（流程①）。本轮原 S004 把它当"诚实终止"停在 Step 3，**跳过了 glossary 明示的出口**（虽 H002 写了"Step 3.5 是下一轮合法动作"，但 Step 3 终态判定本身用了错误判据，需纠偏）。

## 结论

1. **协议唯一合法的四判据 owner = `stages/glossary.md` L22-31 + `templates.md` L301/L308/L311/L371**，SHA256 已固定（见上表）。`problem_truth/actionability/novelty/thesis_fit` 不是 owner 定义的四判据，不得继续作为 Step 3 terminal gate。
2. **Step 3 用自创四判据产生循环门控**：`problem_truth` 被要求"A 的失效已证明"（=Step 4a/MVE 证据）、`novelty` 被当 Step 3 terminal 一列（=Step 3.5/4a 职责），导致 Q1/Q3 因"待证"判未过——这是把下游证据前移。
3. **Step 3 的合法判据**：判据 1 只要求 M-C-A 明确、可证伪（不要求已证伪）；判据 2 方法产出形态；判据 3 近期 baseline；判据 4 可量化对标。新颖性 closure 在 Step 3.5，性能间隙/MVE 在 Step 4a。
4. **STEP3_NO_VALID_PROBLEM 是 Step 3.5 的触发器不是终点**（glossary 出口①）。

## 对决策的影响

- **新建 D005**：纠正 Step 3 终态为 `STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED`，保留 D004 的 Step 2 PASS + 5 CORE 身份 + Safi/L124 全文 blocker + 全文精读事实提取；只取代 STEP3_NO_VALID_PROBLEM 状态和用自创四判据得到的 Q1-Q5 terminal verdict。
- **V005 保留历史不删**：标明它验证的是本地自写合同（problem_truth 等四列）的一致性，**没有核对 canonical criteria owner**，因此科学语义层失效——这是回归候选（"verifier 必须核对 canonical criteria owner，不能只验证本地 prompt/contract 自洽"）。
- **Phase B 重建 Q#**：按 canonical 四判据重判。原 Q1/Q3/Q4/Q5 的现有 verdict（场景迁移/机械拼接/abstract-blocked/C-blocked）仍可保留，但**理由要映射到 canonical 判据**（场景迁移 → 判据 1 不成立因 A 是"换参数"非"失效"；abstract/C-blocked → 判据 1 的 A 无法从全文确认）。新建 Q-A（预测驱动风险失配）+ Q-B（动作时间尺度失配）。
