# Mission Log — 星地相干 FSO AMC Groundwork

> 长程 mission 的紧凑 checkpoint 链。每行一个 CP###。只记裁决和轨迹，细节进 S/R/T。

## CP001: 2026-08-02 专题初始化 + GW Step 1 授权

- **mission**: AMC Groundwork Step 1（检索 + 逐条语义初筛 + 候选问题族地图 + Step 2 shortlist）。
- **authority**: system topic `2026-07-20-research-direction-lab-system` D020 / `AMC_GROUNDWORK_TOPIC_CREATION`。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `5de0dd4`。
- **allowed**: 检索（tools/search + blit）/ 逐条语义审查 / 候选族地图 / Step 2 shortlist 清单 / 独立验证 / 单次 commit 不 push。
- **forbidden**: 下载全文 / 精读 / Step 2-4a / MVE / Go-Kill / 仿真 / 设计方法 / METHOD_SIGNAL / 改 Skill / 改 4 个 p05_run*.log / push。
- **next_legal_action（本轮完成后）**: 主控验收 Step 1 → Groundwork Step 2 全文获取。
- **status**: STEP1_DONE（待 V001 独立验证 + 用户验收；209 candidates / 5 sources / F1-F4 / shortlist 12 / 直接竞品搜索级 0）。

## CP002: 2026-08-02 Step 1 限定完整性修复 + Step 2 acquisition 授权

- **mission**: 同对话内完成 Phase A（Step 1 科学完整性限定修复）+ Phase B（Step 2 全文获取）。
- **authority**: 用户执行提示词 §三 Phase A + §四 Phase B（paste-attachment 2026-08-02）。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `007a7c4`（CP001 之后无新 commit）。
- **allowed**: Phase A 确定性重算 / title-abstract identity 审计 / 候选族修订（4→3 A/B/C）/ ≤4 alias collision query / provenance receipt（force-add）/ D002+V002 / Step 2 acquisition（dry-run→3 轮下载止损）/ tools/convert / R002 覆盖面报告 / H001 / 单次 commit 不 push。
- **forbidden**: 进 Step 3 精读 / 设计方法 / 跑仿真 / 写 Go-NoGo/METHOD_SIGNAL / 改 Skill / 改 4 个 p05_run*.log / WebReader/WebSearch 抓全文 / push / 把 alias query 扩成新地勘重建 209 大表。
- **next_legal_action（Phase B 完成后）**: 主控/用户确认覆盖面 → Step 3 全文精读（独立新对话）。
- **status**: STEP1_ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR（D002/V002 PASS）+ STEP2_PASS（6 篇合格 content.md 覆盖 A/B/C 三族，待用户验收覆盖面进 Step 3）。

## CP003: 2026-08-02 Step 2 覆盖纠偏轮（D003 主控裁决）

- **mission**: 同对话内完成 (A) Step 2 覆盖纠偏与补充获取；(B) 若补齐 ≥5 篇真正 CORE 全文，立即进 GW Step 3 全文精读。
- **authority**: 用户执行提示词 §"必须先登记主控裁决"+ Phase A + Phase B（paste-attachment 2026-08-02-230536）。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `6ada2bc`（CP002 commit 之后）。
- **allowed**: D003 主控裁决登记 / 确定性补充获取（tools/download + 合法 OA URL + 子 agent API 身份确认）/ CORE 判定（子 agent 全文验证）/ 持久 acquisition receipt（force-add）/ 治理纠偏（topic-index/registry/master-state/R002·H001 supersession banner/V003 合并 verifications.md/S003/V004）/ 独立验证 / 单次 commit 不 push。
- **forbidden**: 进 Step 3.5/4a / 设计方法 / 跑仿真 / 写 Go-NoGo/METHOD_SIGNAL / 改 Skill / 改 4 个 p05_run*.log / WebReader/WebSearch 抓全文 / 绕过访问控制 / push / 把未达 ≥5 CORE 强行判 PASS / 伪造 Step 3 结果。
- **next_legal_action（本轮完成后）**: 用户决策二选一 — (1) 手动补全文到 ≥5 CORE → Step 2 重判 PASS → 进 Step 3；(2) 确认 4 CORE+Safi-abstract 可接受 → 授权仅推 A/B 两族 Step 3（C 族 BLOCKED）。
- **status**: STEP2_BLOCKED_BY_COVERAGE_GAP（D003/V004 PASS）— CORE 全文 4 篇（L023/L096/L146/Galijasevic）< 5 门槛；Safi CORE 无全文 PROVISIONAL；L075 DISPUTED；L165/L090 边界；L124 C 族 BLOCKED；Safi/Chang/Sun/L124 补充获取达 3 路径止损仅 Galijasevic 获全文；**未进 Step 3**（按 FR-22 + 执行提示词不伪造）。

## CP004: 2026-08-03 Step 2 blocker 解除（D004）+ GW Step 3 全文精读终态

- **mission**: 同对话内完成 (1) 用仓库现有 Nguyen2024 全文解除 Step 2 blocker；(2) 重判 Step 2；(3) 若五篇 CORE 门成立，立即完成 GW Step 3 全文精读；(4) 到 Step 3 终态停止。
- **authority**: 用户执行提示词（2026-08-03）Phase A + Phase B + 关键新事实独立验证要求。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `da180519`（CP003 之后无新 commit）。
- **allowed**: Nguyen2024 身份独立验证（Crossref API）/ 规范迁移到 canonical DOI 路径（保留 provenance 不声称 OA）/ CORE 重判 / `_step2_acquisition_receipt.json` 更新 / D004 / Step 3 全文精读（fresh-context 子 agent ≤3 并发 ≤15min）/ 直接竞品矩阵 + Q# 四判据 / literature_notes_amc 专属 owner / papers/_read_notes / 治理更新（topic-index/registry/master-state/V005/S004/H002）/ 独立验证 / 单次 commit 不 push。
- **forbidden**: 进 Step 3.5/4a / 设计方法 / 跑仿真 / 写 Go-NoGo/METHOD_SIGNAL / 改 Skill / 改 4 个 p05_run*.log / WebReader/WebSearch 抓全文 / 绕过访问控制 / 据 abstract 推 Safi/L124 失效机制 / push / 把 Nguyen 等已覆盖宽泛问题重命名为空白（FR-23）/ agent 自行放宽 C 条件。
- **next_legal_action（本轮完成后）**: **GW Step 3.5 定向补充检索**（glossary 空集处置流程①回扩检索；需新对话 + 用户授权扩检索范围 + 优先获取 Safi/L124 全文）；扩检索后仍无 Q# → 上报用户决策调整 C 或换子方向。
- **status**: STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED（D004）+ **STEP3_NO_VALID_PROBLEM（S004/V005）** — Nguyen2024（IEEE TAES 2024，Crossref 验证 + SHA256 迁移，非 OA 机构授权）补到 5 CORE 全文（L023/L096/L146/Galijasevic/Nguyen2024）；Step 3 精读 5 CORE+3 边界+2 abstract，直接竞品矩阵确认**无一篇 confirmed 覆盖 coherent+GG+coded+uncertainty 四要素**，5 候选 Q# 无一四判据全过（Q1 迁移/Q2 self-id future work/Q3 机械拼接/Q4 abstract-blocked/Q5 C-blocked）；C 族 L124 仍 BLOCKED；Safi PROVISIONAL；**未进 Step 3.5/4a**。

## CP005: 2026-08-03 Step 3 语义门纠偏（D005）+ Step 3.5 定向检索终态

- **mission**: 同对话内完成 (1) 纠正 Step 3 语义门误用（自创四判据标签当 terminal gate）；(2) 按 canonical 四判据 owner 重判 Q#；(3) 完成 Step 3.5 定向检索+竞争闭包；(4) 给出是否存在 Step 4a 入口；(5) 到 Step 3.5 终态停止。
- **authority**: 用户执行提示词（2026-08-03-105947）§"本轮主控裁决"+ Phase A/B/C。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `482d9ad`（CP004 之后无新 commit）。
- **allowed**: semantic-gate owner receipt（R001，SHA256+行号+原文逐字核对）/ D005 纠偏 STEP3_NO_VALID_PROBLEM → STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED / canonical 四判据重建 Q-A/Q-B / Step 3.5 定向检索（2 并行子 agent ≤15min，Q-A/Q-B 各 6 query+引用链）/ 竞争闭包表 / Safi·L124 ≤3 路径合法获取（失败止损）/ R003 / V006 独立验证 / 治理更新（topic-index/registry/master-state/S005/H003）/ 单次 commit 不 push。
- **forbidden**: 进 Step 4a / 设计方法 / 跑仿真 / 写 Go-NoGo/METHOD_SIGNAL / 改 Skill / 改 4 个 p05_run*.log / 据 abstract 推 Safi/L124 失效机制 / 绕过访问控制 / 用自创四判据标签当 terminal gate / 制造第三个弱 Q / agent 自行放宽 C 条件 / push。
- **next_legal_action（本轮完成后）**: **GW Step 4a**（需新对话+用户授权；§A0 §0 前置门控再查 Q# 四判据）。Step 4a 前建议关闭 3 个开放问题（Safi 全文 / Q-B 信道模型可行性 / Galijasevic citation 重跑）。或用户决策调整 C / 换 AMC 子族 / 停止。
- **status**: STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（D005/R001）+ **STEP3_5_SURVIVES（S005/R003/V006）** — 旧 STEP3_NO_VALID_PROBLEM 因用自创四判据（problem_truth 等）被取代；canonical 四判据 owner = glossary.md L22-31 + templates.md L301（SHA 固定）；重建 Q-A（预测驱动风险失配）+ Q-B（动作位置-时间尺度失配）；Step 3.5 ~190 命中+引用链闭包后 **Q-A（带 Safi UNVERIFIED 尾巴）+ Q-B（带 baseline 缺位风险）均 SURVIVES_STEP3_5** → 存在 Step 4a 入口但**本轮不启动**；Safi/L124 仍 BLOCKED（3 路径失败）；保留 Step 2 PASS+5 CORE+精读事实提取。

## CP006: 2026-08-03 Step 4a Q-A 科学完整性修复（D007 撤回 D006 科学 KILL）

- **mission**: 同对话内完成主控裁决执行提示词——撤回 D006 无效 Q-A KILL，Phase A RED 根因复现 + Phase B 物理身份闭合 + Phase C GREEN 修复 + Phase D feasibility-first 重测两动作契约 + 独立 verifier，输出修订 recommendation。
- **authority**: 用户主控裁决执行提示词（2026-08-03，本轮）§"执行 AMC Q-A Step 4a 科学完整性修复与正确重测"。
- **worktree**: `.worktrees/rdl-method-production-v2` @ `280b9a5`（CP005 之后无新 commit）。
- **allowed**: Phase A 10 RED 测试（red_receipt.json）/ Phase B Galijasevic PDF 视觉核对（fresh-context 子 agent，identity_receipt.md）/ Phase C corrected_v2 实现 + green_check（green_receipt.json）/ Phase D verdict_evaluator（两动作契约 27 cells×9 methods）/ V008 独立 verifier（12 项核验）/ D007 取代 D006 科学层 / V008 取代 V007 科学层 / S007 / feasibility_report_v2.md（不覆盖旧）/ probe_corrected_v2_raw.json / 治理更新（topic-index/voice/H004）/ 单次 commit 不 push。
- **forbidden**: 偷偷改 Q-A→Q-A'（Contract B 须显式标 reframe 候选交用户）/ 跑 fresh held-out MVE（须用户先决 Q-A'）/ 改 Skill / common/ params.py / 正式论文结论 / dormant receiver / 4 个 p05_run*.log / 删旧 probe_headroom.py/raw + feasibility_report.md（保留加 INVALIDATED_BY 指针）/ push / agent 自行最终 Go/No-Go。
- **next_legal_action（本轮完成后）**: 用户裁决 (i) Q-A' reframe→新 GW Step 1-3 / (ii) Contract A 下 Q-A 不可评估停止 / (iii) fresh held-out MVE 仅在决 Q-A' 后 / (iv) 补齐 3 篇 CORE。
- **status**: **STEP4A_QA_REPAIRED_KILL_WITHDRAWN（D007/V008/S007）** — Phase A 10/10 RED_OBSERVED 复现 8 承重缺陷（B1 未用 margin/scoring 对齐 k 非 k+td/FER 当 hard fail/per-turb dB-mean 重定心/outage floor 是 action-contract artifact）；Phase B Galijasevic PDF 视觉核对（OOK+APD/lognormal PSI=10/16率/FER 1e-6 Eq.23/per-rate margin/k+td/无outage规则）；Phase C corrected_v2 10/10 GREEN + verifier 手工复算 MATCH 1e-12；Phase D feasibility-first 重测（Contract A 27/27 action-contract 不可行 / Contract B O1 feasible 27/27, C1 feasible 9/27, 2 cells 胜 baseline +5-7%）；V008 12/12 PASS CONFIRM。held-out MVE 待用户决 Q-A' 后跑。**未宣称 Groundwork 闭合**（5 CORE < ≥8 整体门）。
