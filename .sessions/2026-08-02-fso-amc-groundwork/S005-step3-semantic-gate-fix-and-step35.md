# [S005] Step 3 语义门纠偏（D005）+ Step 3.5 定向补充检索

> 2026-08-03 | 阶段: GW Step 3 判据纠偏 + GW Step 3.5 定向补充检索 | 状态: 完成 — Step 3 终态 STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（D005）+ Step 3.5 终态 STEP3_5_SURVIVES（Q-A/Q-B 均 SURVIVES）

## 目标

一个对话内完成（用户执行提示词 2026-08-03-105947）：
1. 纠正 Step 3 语义门误用（用自创 problem_truth/actionability/novelty/thesis_fit 当 terminal gate）；
2. 按 protocol 唯一四判据（glossary/templates owner）重判 Q#；
3. 完成 GW Step 3.5 定向补充检索和竞争闭包；
4. 给出是否存在可进入 Step 4a 的问题；
5. 到 Step 3.5 终态停止，不进 Step 4a/MVE，不设计方法，不跑仿真。

## 记录

### Phase A — 确定性纠偏（D005 / R001）

**A1 semantic-gate owner receipt（R001）**: 逐字核对 canonical 四判据 owner：
- `stages/glossary.md` SHA256 `eafa43e3…073f610e74b`，四判据定义 L22-31（具体技术矛盾 / 方法产出形态 / 近期 baseline / 可量化对标）。
- `templates.md` SHA256 `bdc93d41…caa7b9e41`，Q# 表头 L301 + 填表规则 L308/L311 + 每篇提取 L371。
- Step 3（gw-read.md L86/L198）/ Step 3.5（gw-supplement.md 全文）/ Step 4a（gw-feasibility.md §A0）职责逐字核对。

**A2 自创标签错位**: `problem_truth` ≈ 判据1 但被要求"A 的失效已证明"（=Step 4a/MVE 证据前移，违反 FR-22）；`novelty` 不属四判据（=Step 3.5/4a 职责前移）。→ Q1/Q3 因"待证"判未过 = 把下游证据前移到 Step 3，循环门控。

**A3 D005**: Step 3 终态 STEP3_NO_VALID_PROBLEM → **STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED**。保留 D004 的 Step 2 PASS / 5 CORE 身份 / Safi·L124 blocker / 全文精读事实提取；只取代 STEP3_NO_VALID_PROBLEM 状态和自创四判据得到的 Q1-Q5 verdict。V005 保留历史，标"验证本地自写合同一致性，未核对 canonical owner，科学语义层失效"+ 回归候选。

### Phase B — 按 canonical 四判据重建 Q#（literature_notes_amc §6 重写）

- **Q-A（新建，预测驱动自适应编码的风险失配）**: M=Galijasevic 点预测选码 / C=延迟+估计误差+深衰尾+非线性 FER / A=点预测无后验，尾部误差经非线性门限放大致系统性违约。canonical 四判据 Step 3 层全 ✅（判据1 可证伪不要求已证伪；方法产出=risk/posterior-aware rule；baseline=Galijasevic；对标=FER 违约率/goodput）。**SURVIVES_STEP3 待 3.5 闭包**。
- **Q-B（新建，相干星地 AMC 动作位置-时间尺度失配）**: M=L023 单环 TX+RX CSI 反馈 / C=LEO RTT≈/>相干时间 RX 快 TX 慢 / A=同环绑定致 TX 动作收过期状态（L023 自陈 LEO 不可行）。canonical 四判据 Step 3 层 ✅（判据3 baseline ⚠ 因 L023 地面自陈卫星失效，待 3.5 确认合法星地 coherent AMC baseline）。**SURVIVES_STEP3 待 3.5 闭包**。
- **Q1**（场景迁移）维持 WEAK_SCENARIO_MIGRATION 不晋级（判据1 ❌：换参数重算≠失效）。
- **Q3**（三层错配）维持 TOO_BROAD_MECHANICAL_COMBINATION（判据1 ❌：宽集合非单一可证伪；可收窄子集已由 Q-A/Q-B 承接）。
- **Q2**（L096 future work）不单独晋级（切片被 Q-A 闭包覆盖；future-work 原料性保留，Step 3.5 一并查）。
- **Q4 Safi / Q5 L124** 继续 BLOCKED_BY_MISSING_FULLTEXT。
- **论文自列 future work ≠ novelty 自动失败**（D005）；**不得因尚无 MVE 否决 Q-A/Q-B**。

### Phase C — Step 3.5 定向补充检索（2 子 agent 已完成）

**C1 调度**: 2 个并行子 agent（Q-A：6 query+引用链+Safi/L124 获取；Q-B：6 query+4 补充+引用链+合法星地 coherent baseline 确认）。每个 ≤15 分钟，主线程只接收结构化摘要 + 竞争闭包表。

**C2 检索规模 / 直接竞品 / 全文获取结果**:
- Q-A：6 专属 query ~120 命中 + Safi forward 49（筛后 48）+ Galijasevic citation **未闭合**（DOI 解析异常 + Exa 透支 + S2/OpenAlex 限速）。
- Q-B：6 专属 + 4 补充 query ~190 命中 + L023 forward 23（0 sat AMC）+ Nguyen2024 forward 5（0 coherent sat AMC）+ L023 backward 缺口（OpenAlex 未索引）。
- Safi/L124 全文获取：**均 3 路径失败仍 BLOCKED**（Safi：download all_failed + Unpaywall closed + 无作者稿；L124：download all_failed + Optica HTTP 202 Radware JS-challenge + arXiv 0）。未绕过访问控制，未用 WebReader/Scholar。

**C3 竞争闭包表（Q-A + Q-B）**: 见 `literature_notes_amc.md §十一` + `R003` 完整版。
- Q-A：唯一同 M+C 的 Nguyen2024 用点预测把 outdated CSI 当动机非纳入码率规则 → 印证 A 开放。**无 FSO posterior/risk-aware 码率规则直接竞品**。
- Q-B：FSO/sat 域无分层契约直接竞品；split-timescale 在 RF massive-MIMO（10.1049/cmu2.12389）有成熟先例证路径非空。**无合法 coherent 星地 AMC baseline**（L023/L124/TCOMM2026/LCOMM2026 全 terrestrial；L165 sat 但 AO）。

**C4 closure verdict + Step 4a 入口**:
- **Q-A = SURVIVES_STEP3_5**（带 Safi UNVERIFIED 尾巴）。
- **Q-B = SURVIVES_STEP3_5**（带 scenario-migration + baseline 缺位风险）。
- **两个 Q 均 SURVIVES → 存在 Step 4a 入口**。本轮不启动（brief 明示）。

## 决策引用

- D001（范围）/ D002（Step 1 修复）/ D003（Step 2 纠偏）/ D004（Step 2 解除 blocker）。
- **D005（新建）**：Step 3 语义门纠偏 — STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED，按 canonical 四判据重建 Q-A/Q-B。
- V001-V004（历史，有效）；**V005 保留历史标语义失效**；**V006（新建）**：D005 + Step 3.5 终审验证（10 项 checklist）。
- **R001 receipt（新建）**：semantic-gate owner receipt；**R002 已存在**（Step 2 覆盖报告，D003 supersede）；**R003（新建）**：Step 3.5 定向检索 + 竞争闭包记录。

## 范围确认

- 本轮是否在 scope boundary 内: **是**（Step 3 判据纠偏 + Step 3.5 定向检索 + 竞争闭包；不动 Skill/p05 log/dormant receiver；不进 4a/MVE/方法/仿真）。
- 到 Step 3.5 终态停止（brief 明示）。

## 后续

- **本轮终态 STEP3_5_SURVIVES**（Q-A/Q-B 均 SURVIVES），存在 Step 4a 入口但**本轮不启动**。
- **下一合法动作 = Step 4a**（需新对话 + 用户授权；gw-feasibility §A0 §0 前置门控会再查 Q# 四判据）。
- **Step 4a 启动前开放问题**（非本轮终止条件）：(1) Q-A Safi UNVERIFIED 尾巴——合法获取 Safi 全文关闭；(2) Q-B baseline 缺位——评估自建 coherent sat-ground GG 信道模型可行性（判据4 量化对标工程前提）；(3) Galijasevic DOI 异常 + L023 backward 缺口——用正确 DOI/标题重跑 citation。
- **若用户决定不进 Step 4a**：可调整 C 条件 / 换 AMC 子族 / 停止（跨阶段决策，禁 agent 自行放宽 C）。
