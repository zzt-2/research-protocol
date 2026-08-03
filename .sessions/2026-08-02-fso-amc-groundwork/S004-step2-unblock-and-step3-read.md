# [S004] Step 2 blocker 解除（D004）+ GW Step 3 全文精读 — 终态 STEP3_NO_VALID_PROBLEM

> 2026-08-03 | 阶段: GW Step 2 解除 blocker + GW Step 3 全文精读 | 状态: 完成 — Step 3 终态 STEP3_NO_VALID_PROBLEM

## 目标

一个对话内完成：(1) 用仓库现有 Nguyen 2024 全文解除 Step 2 blocker；(2) 重判 Step 2；(3) 若五篇 CORE 门成立，立即完成 GW Step 3 全文精读；(4) 到 Step 3 终态停止，不进 Step 3.5/4a，不设计方法，不跑仿真。

## 记录

### Phase A — Step 2 blocker 解除（D004）

**A1 Nguyen 2024 身份独立验证 + 迁移**:
- 主工作区已有历史全文：`papers/downloads/2026-05-30/10535712.{pdf,md}`（546 行 MD，格式合格）。
- Crossref `/works/10.1109/TAES.2024.3403809` 独立验证：title/authors/venue(IEEE TAES)/vol(60)/issue(5)/pages(7498-7509)/year(2024-10)/publisher(IEEE) 逐字段匹配；content.md H1 Jaccard=1.0。
- **非公开 OA**：content.md 页脚 "Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30, 2026 at 07:31:59 UTC from IEEE Xplore. Restrictions apply." → metadata.json + receipt 完整保留此来源，**不声称 OA**。
- 迁移到 canonical DOI 路径 `papers/doi/10.1109_taes.2024.3403809/{source.pdf,content.md,metadata.json}`，SHA256 迁移前后完全一致（PDF b49f5abf…4c95c51 / MD 27f25473…87103f）。不重新转换。

**A2 Nguyen 2024 CORE 判定（全文证据）**:
- action = 运行时联合 rate（subcarrier K-QAM 星座 K∈{4,8,16,32,64,128}）+ power（EDFA 离散增益），per equal-duration channel state；AMP（理想连续）+ SAMP（离散，Alg.1-3）。
- condition = LEO-sat-to-UAV FSO + 弱湍流 **lognormal**（Rytov σ_R²，UAV<1km 论证，**非 GG**）+ Beckmann pointing + outdated 反馈 CSI（数 ms > 相干 <1ms）由 **ESN 多步预测**克服。
- deployable = 运行时 TX-side AMC controller；非 classification/AO/fixed/post-hoc → **CORE**。
- 关键缺口（vs 目标 coherent/GG/coded-chain）: **非 coherent**（IM/DD 风格 K-QAM，瞬时 BER γ∝h²）/ **非 GG**（弱 lognormal）/ **无 coded chain**（HARQ 仅 related work[8]）/ sat-to-UAV 非 sat-ground / info uncertainty 仅反馈时延。

**A3 Step 2 重判**: CORE 全文 4→5 ≥ 5 门槛。终态 **STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED**（D004）。C 族 L124 仍 BLOCKED；Safi 仍 PROVISIONAL abstract-only（不计门槛）；D003 历史 BLOCKED 保留作 superseded_verdict。

**A4 receipt 更新**: `_step2_acquisition_receipt.json` 加 last_updated_at + Nguyen 条目（含完整 provenance + Crossref 验证 + SHA256 + CORE 判定）+ coverage_summary 更新（core_with_fulltext=5, step2_verdict, superseded_verdict 保留）。json parse OK。

### Phase B — GW Step 3 全文精读（fresh-context 子 agent）

**B1 调度**: 3 个并行 fresh-context 子 agent 精读 5 CORE 全文（Agent1: L023+Galijasevic / Agent2: L096+L146 / Agent3: Nguyen2024）+ 2 个并行边界/bibliographic agent（L075 语义仲裁 / L165+L090+Safi+L124）。每个 ≤15 分钟，主线程只做结构化汇总和最终判断。

**B2 精读产出**: 每篇 read-note `papers/_read_notes/{paper_id}.md`（M-C-A + 7 结构化子表 + AMC 关键语义字段 + 与目标重合/缺失 + 四判据 + file:line 证据）。

**B3 边界/语义仲裁结果**:
- L075 = **CLASSIFICATION**（CNN+BiLSTM+Attention softmax 分类器 on RX STFT，5 类调制标签，confusion-matrix + true-label 监督，无 CSI 反馈环 → dead-end#8，非 CORE）。
- L165 = **BOUNDARY_AO**（AO 波前校正 Shack-Hartmann+97-actuator DM 1.5kHz，调制固定 per measurement 比较 not switch）。
- L090 = **BOUNDARY_FIXED_SCHEME**（4-state STTC + coherent QPSK，"adaptive orthogonality controller"= ξ-parameterization design-time config，无 CSI 反馈/无 runtime AMC）。
- Safi2019 = **PROVISIONAL_DIRECT_COMPETITOR**（abstract-only：GG + estimation-error + adaptive coding/power，强竞品但全文缺失，不得推实现）。
- L124 = **C_FAMILY_BIBLIOGRAPHIC**（abstract-only：coherent + 多维 CSI physics-informed AMC，全文 BLOCKED，C 族不得过 novelty closure）。

**B4 直接竞品矩阵结论**: **无一篇 confirmed 同时覆盖 coherent + GG + coded-chain + info-uncertainty 四要素**。每篇缺 2-3 维度：Nguyen（非 coherent/非 GG/无 coded）、L096（非 coherent/非 GG/perfect CSI）、L146（非 coherent/非 GG/无 HARQ）、Galijasevic（非 coherent/非 GG/无 HARQ）、L023（非 GG/无 coded/地面非卫星）。rate/power（Nguyen）、HARQ-rate（L096）、coding-rate+prediction（Galijasevic）、robust-MCS（L146）等宽泛问题**已被覆盖**。

**B5 5 候选 Q# 四判据**（详见 literature_notes_amc.md §6）:
| Q# | M | 最强竞品 | 判定 | 原因 |
|---|---|---|---|---|
| Q1 | Nguyen SAMP | Nguyen2024 | 未过 | 场景迁移（coherent+GG 替换 IM/DD+lognormal）非失效证明 |
| Q2 | L096 IR-HARQ | L096 | 未过 | A = L096 self-identified future work（imperfect feedback）→ novelty ❌ |
| Q3 | Nguyen+Galijasevic 拼接 | Nguyen+Galijasevic | 未过 | 机械拼接待证假设，brief 明示 FAIL |
| Q4 | Safi2019 | Safi | 未过 | abstract-blocked，不得推失效 |
| Q5 | L124 | L124 | 未过 | C-family-blocked，不得过 novelty closure |

**无一四判据全过 → Step 3 终态 STEP3_NO_VALID_PROBLEM**（诚实终止，不包装空白、不设计方法）。

### B6 literature notes owner

新 owner `projects/thesis-fso/literature_notes_amc.md`（与 receiver `literature_notes.md` 同目录独立文件，**不覆盖** receiver 197KB 产物）。D004 §8 登记 adapter 路径。

## 决策引用

- D001（范围）/ D002（Step 1 修复）/ D003（Step 2 历史 BLOCKED，本决策 supersede 其 blocker 状态但保留纠偏）。
- **D004（新建）**：Step 2 blocker 解除 — STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED，立即推 Step 3。
- V001-V004（历史验证，继续有效）。
- **V005（新建）**：D004 + Step 3 终审验证（PASS）。

## 范围确认

- 本轮是否在 scope boundary 内: **是**（Step 2 解除 blocker + Step 3 全文精读到终态；不动 Skill/p05 log/dormant receiver；不进 3.5/4a/方法/仿真）。
- Step 3 终态按 brief 二选一诚实选 STEP3_NO_VALID_PROBLEM（无 Q# 全过）。

## 后续

- **Step 3.5（下一轮合法动作）**: glossary 流程①回扩检索；补 coherent+GG+AMC 直接竞品 + Safi/L124 全文 + 共同引用基础文献延伸。
- Safi（IEEE paywall）+ L124（Optica bot-block）全文获取是关键身份闭合（用户手动）。
- C 条件五要素锁死是否过窄 → 扩检索后仍无 Q# 则上报用户决策（禁 agent 自行放宽）。
- 候选族最终数（2-3）待 Step 3.5/4a 后定。
