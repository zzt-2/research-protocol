# Topic Index: 星地相干 FSO 自适应编码调制 (AMC) Groundwork

> 状态: **dormant** | 创建: 2026-08-02 | 最后更新: 2026-08-03（**D009 科学冻结 — AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT**）：用户 campaign-level synthesis 裁决三条路线全部停止——Q-A=STOPPED_INCONCLUSIVE_TESTBED_ACTION_MISMATCH / Q-A′=HARVEST_ONLY_ENGINEERING_SEED（corrected_v2 工程种子保留，不晋级不进正文）/ Q-B=STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE（非 Kill family，基础设施缺位非假设证伪）；不补 3 篇 CORE、不搭 multi-day testbed、不重开 Safi/L124；**不得写成"领域无问题"**，只能写"当前目标条件和现有资产下没有得到可授权的第二项主方法"；恢复须显式 scope-change（新直接论文/现成合法 baseline/外部 testbed）+ 新开 GW 专题；保留全部历史 D/V/S/H + corrected_v2 工程产物 + unauthorized probe，不改写历史。campaign-level 论文综合判断在 `direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`（第二工程贡献 = NO_SECOND_CONTRIBUTION_YET）
>
> **上一轮（D008/V009/S008，保留历史）**：D008 纠正 D007 授权血缘 + Q-B bounded gate 完成——Phase A git 取证确认"同时跑两个动作契约"从未由用户发出（父 280b9a5 0 命中，1ed8347 首现 5 次），voice.md 移除伪造"用户即时原话"条目，D008 精确拆分 D007（科学/代码事实产物保留 / 授权·scope 层被取代），V008 check 1-11 科学事实有效 / check 12 terminal verdict 授权层失效；tune_C1 动作合同缺陷登记（probe_corrected.py:362 调谐未传 allow_no_transmit）；Q-A 终态=CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH，Q-A'=UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE（NONBINDING）；Phase B Q-B bounded gate → 终态 Q_B_BASELINE_UNAVAILABLE（primary）+ Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET（secondary），不 Kill family，不进 Step 4a MVE；V009 独立 verifier 12/12 PASS CONFIRM；未宣称 Groundwork 闭合（5 CORE < ≥8 整体门）

## 专题信息

- **slug**: `2026-08-02-fso-amc-groundwork`
- **title**: 星地相干 FSO 编码自适应与 AMC Groundwork
- **性质**: 独立系统层 Groundwork 专题。承接 system 专题 `2026-07-20-research-direction-lab-system` D020 授权的 `AMC_GROUNDWORK_TOPIC_CREATION`，从 GW Step 1 重新开始。
- **上游授权**: `.sessions/2026-07-20-research-direction-lab-system/topic-index.md` 的 `rdl_control` 块（`allowed_actions` 含 `AMC_GROUNDWORK_TOPIC_CREATION`，`authority_pointer` = D020）。
- **不属于**: 旧 receiver method-production campaign（`2026-07-23-research-direction-lab-longitudinal-test`，已 dormant）。

## 范围边界

### 原始目标（冻结，2026-08-02 用户执行提示词）

在"星地相干自由空间光通信 + Gamma-Gamma 大气湍流 + 真实编码链/信息不确定性"背景下，寻找一个有希望成为毕业论文第二项贡献的自适应编码调制或链路适配问题。本轮只做 Groundwork Step 1：两轮多来源问题驱动文献检索 + 逐条语义初筛 + 候选问题族地图 + Step 2 全文获取 shortlist，到 Step 1 验收即停止。

### 当前范围

- GW Step 1：检索（轴 A coded-goodput/MCS、轴 B CSI 不确定/反馈时延鲁棒 AMC、轴 C 跨层 coding/mod/power/interleaving 联合适配）+ 逐条语义初筛 + 候选问题族地图 + Step 2 shortlist。
- 中文检索轴：自由空间光通信/星地激光通信 + 自适应调制编码/链路自适应（走 `tools/blit --source cnki/wanfang`，cookie/IP 失败即记债）。

### 明确不含

- 不进入 Step 2（全文获取）、Step 3（精读）、Step 3.5、Step 4a（Go/No-Go）。
- 不下载/精读全文，不设计方法，不跑仿真，不写 Go/No-Go，不产生 METHOD_SIGNAL。
- 不修改 Research Direction Lab Skill（V014 已冻结；本轮 patch=0）。
- 不修改四个 `projects/simulation/explore/cma-fade-divergence/p05_run*.log`（用户旧文件）。
- 不复活旧 dead-end（见下方 ledger），不把 P08/G1/P09/P11 或 negatives 升级成 AMC 证据。
- 不把"automatic modulation classification"当 AMC（adaptive modulation and coding）混入。

### 范围变更记录

- **2026-08-02 D002**：GW Step 1 从原授权的"Step 1 执行完成即停"修订为"Step 1 限定完整性修复后进入 Step 2 acquisition"。变更原因：用户 Phase A 执行提示词指示先做 Step 1 科学完整性限定修复（计数口径 / title-abstract identity / 候选族地图 / provenance receipt），修复 PASS 后**立即继续** Phase B Step 2 全文获取（同一对话内完成）。原始目标不变（找 AMC/链路适配问题作毕业第二贡献），仅把 Step 1→Step 2 的推进在同一对话内打通，并补做 Step 1 完整性修复。
- **2026-08-02 D003**：Step 2 覆盖纠偏——D002/R002/H001 宣称的"Step 2 PASS / 6 篇覆盖三族"不成立。主控重判：6 篇只过文件/转换质量门，未做 CORE 判定；逐篇 CORE 重判后保守核心集缩窄到 L023/L096/L146 3 篇，L075 改标 SEMANTICALLY_DISPUTED_PENDING_FULL_READ，L165（AO）/L090（fixed STTC）不计核心，L124（C 族）保持 C_L124_FULLTEXT_BLOCKED。本轮补充获取 Safi/Chang/Sun/Galijasevic/L124，仅 Galijasevic 获全文（NSF PAR），其余达 3 路径止损。**最终 CORE 全文 = 4 篇（L023/L096/L146/Galijasevic）< 5 门槛 → Step 2 终态 STEP2_BLOCKED_BY_COVERAGE_GAP，未进 Step 3**。范围不变（仍在 GW Step 2 acquisition 内），仅纠正 Step 2 PASS/BLOCKED 判定与 CORE 计数口径。
- **2026-08-03 D004**：Step 2 blocker 解除——用仓库主工作区已有历史全文 Nguyen2024（IEEE TAES 60(5):7498-7509, 2024，DOI 10.1109/TAES.2024.3403809，Crossref 独立验证身份 + SHA256 迁移一致，**非公开 OA** = 机构 IEEE Xplore 授权）规范迁入 worktree canonical DOI 路径 `papers/doi/10.1109_taes.2024.3403809/`；CORE 判定 = family-A（delayed-CSI + ESN 预测 + 联合 rate/power SAMP，IM/DD K-QAM γ∝h² + lognormal 弱湍流 + Beckmann pointing + sat-UAV）。**CORE 全文 4→5 ≥ 5 门槛**。Step 2 终态修订 **STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED**（D003 历史 BLOCKED 保留作 superseded_verdict；C 族 L124 仍 C_L124_FULLTEXT_BLOCKED；Safi 仍 PROVISIONAL_direct_competitor）。立即推进 GW Step 3 全文精读。范围不变（A/B 族 Step 3 + 边界/abstract 核查，不进 3.5/4a）。

## 已确认结论

### 不变量

- **AMC ≠ receiver method-production campaign**：本专题是独立系统层方向，旧 campaign（载波同步/均衡/双偏振）的 negatives 不是 AMC 证据，旧资产（P08-R2/LDPC/prefix-LS/bit-true/info-boundary）只是可复用工程资产（依据 `method-production-campaign-thesis-map.md` B 级行）。
- **既有 DA/NDA 自适应 CPR 是论文现有主贡献**（依据 `method-production-campaign-thesis-map.md` A 级行 + master-state §2）；新 AMC 必须形成**不同系统层的真实控制动作**，不能是 DA/NDA CPR 的换名。
- **GW 流程强制（FR-22/TL-30）**：到 Step 1 验收即停；Step 3 + Step 4a 是硬门控不可跳过；候选问题族只写"候选问题假设"，不伪称 Q# 过四判据。
- **Go/Kill 标准分离（TL-32/FR-25）**：Step 1 无 Go/Kill，只产 shortlist。Go 判据 = 赢传统未优化 baseline；oracle 上界（FR-21）只做后续 Step 4a 收尾 Kill 工具。
- **证据链强制（FR-26/TL-33）**：所有"已搜/已读/已确认"声称必须附证据指针（文件+行号/JSON 路径）。

### 其他结论

- **Step 1 搜索级核心发现（R001，经 D002 修订）**：coherent sat-ground FSO + Gamma-Gamma + AMC/MCS + 真实 coded chain + 信息不确定性**四要素齐全的直接竞品 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`**（round-1 71 + round-2 扩至 209 + 4 alias collision query 32 命中均未确认直接竞品；但 Exa 透支/OpenAlex 0/S2 限速的覆盖 caveat 存在，不把搜索未命中解释成真实空白，FR-23）。最接近的 L124 经 Crossref+S2 双源确认是**真实的 coherent-FSO AMC 论文**（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557，physics-informed AMC，modulation selection driven by [SNR, scintillation index, phase variance]），但 abstract 未提 Gamma-Gamma/satellite，pre-fix 状态 `UNVERIFIED_BIBLIOGRAPHIC_HIT`，须 Step 2 全文闭合 coding/CSI/channel/scenario。L165（Tbit/s feeder link）adaptive 动作在 AO 层非 AMC。
- **候选族从 4（F1-F4）修订为 3（A/B/C），均"候选假设，未过四判据"**（D002）：**A_MCS_POWER_CONTROL**（瞬时 CSI 分支 + delayed/statistical/uncertain CSI 分支合并，真实 action 相同）/ **B_HARQ_IR_RATE_ADAPTATION**（真实独立 action，文献密集，更像 ENGINEERING_COMPONENT）/ **C_COHERENT_TX_ADAPTATION_UNVERIFIED**（原 F4，L124 全文身份闭合前不算正式族）。原 F4 不再算机制不同的第 4 族——L124 是 A 族的一个相干相位实例。
- **F1 headroom 未证（D002 纠正）**：A 族 delayed/statistical CSI 分支**并非完全避开** dead-end#3 的 0.09 dB MCS 天花板；它与旧路线共享长时间尺度信息驱动 MCS/码率切换，新增点只是"不确定信息约束"，headroom 须 Step 4a 维度 D oracle 上界（FR-21）核算。
- **title-abstract identity 审计（D002）**：6 个 normalized-abstract 重复组覆盖 18 条 hit，根因是 Exa/SerpAPI abstract 抓取污染（少数通用 survey 摘要被反复注入不同标题条目）。受影响 shortlist/flagged：L124（6G-roadmap abstract，真实经 Crossref 确认）/ L020 / L038 / L090。这些条目 abstract 不可信，须 title+DOI 定身份。
- **诚实边界**：空白存在但非必然=问题（FR-23）——可能源于物理不成立（瞬时 CSI 撞相干时间 dead-end#2 被领域隐式放弃）。Step 2/3 必须区分"机会"vs"物理不可行"，不强造方向。
- **中文检索**：CNKI 40 条命中但 0 条抓到摘要（cookie/IP 受限），38 条进 digest 全部低 confidence；5 条标题强相关（L050/L206 概率整形 FSO 等）须 Step 2 抓全文。中文摘要抓取记为 Step 2 前置债务（仍 open，本轮 `tools/blit --source cnki` 未跑）。

## AMC 历史 dead-end ledger（继承边界，FR-26 证据指针）

> 这些是**局部**历史结果，不是"所有 AMC 都无效"。Step 1 任务是找机制不同、时间尺度成立、动作真实的新问题。新候选族须**逐条对照**本表打勾（防"换名重开"，TL-30/FR-22）。

| # | 历史 dead-end | 证据指针 | 继承约束 |
|---|---|---|---|
| 1 | ISL AMC prediction：轨道确定性信道，DL 输给简单方法 | `domain-comms.md:243-247` 反模式 3 isl-acm-pred D026；归档专题 `2026-05-16-isl-scheduling-drl`(closed) | 禁把"星间/确定性信道"当 AMC 机会；新方向须信道含真实不确定性 |
| 2 | 链路自适应撞"反馈延迟 > 相干时间 2-10ms"（TL-03） | `thesis-lessons.md:39` TL-03；`2026-06-10-.../R005-non-carrier-sync-rescan.md:100,106`；`H004-b1-gap-verified-direction-decision.md:34` | 任何反馈/预测类 AMC 须先核算动作时间尺度 vs 反馈+相干时间 |
| 3 | ③ MCS 排程 oracle 上界 0.09 dB（8/12 case=0） | `2026-06-10-.../decisions.md:539,578`；`S014-direction-3-mcs-scheduling-upperbound-fail.md:19,31` | 禁把同一窄切片 MCS/oracle 切换重新包装；新 MCS 须机制不同 |
| 4 | AMC+CPR 联合设计前提崩塌（ω_n 跨调制一致 C4-12） | `2026-05-31-.../R002-algorithm-direction-scout.md:52,294,361,550` | 禁"AMC+CPR 联合设计"换名；新 AMC 须独立于跨调制同步参数 |
| 5 | 自适应交织/纯PS/N1/coded-chain repair ≠ 新 AMC | registry 专题边界（4b#1/N1/(c)/P08-R2）；`2026-06-19-4b1-.../topic-index.md` 殊途同归死轴 | 禁把这些局部历史换名冒充 AMC 方法 |
| 6 | P08-R2 5G NR LDPC/prefix-LS/bit-true/info-boundary = 工程资产非证据 | `method-production-campaign-thesis-map.md` B 级行；`2026-07-23-.../R010-...md` §3 | 可复用工程资产，不得引用为 AMC 科学结论 |
| 7 | 既有 DA/NDA 自适应 CPR = 论文现有主贡献 | `method-production-campaign-thesis-map.md` A 级行；master-state §2 | 新 AMC 须不同系统层动作，不能是 CPR 换名 |
| 8 | "AMC"检索大量实为 automatic modulation classification | 论文参考文献 [24/41/43/45/46]（夏兆宇 thesis）；领域常识 | **运行时排除规则**：按 title/abstract 判，识别即排除 |
| 9 | AMC↔Ch4 BER 循环依赖（BER 决定切换门限但 BER 受 CPR 影响） | `2026-05-30-.../R003-direction-bc-deep-analysis.md:19,26` | 新 AMC 须解耦或前馈，避免与主贡献循环依赖 |

## GW Progress（FR-22 跨 Step 门控，本专题单一事实源）

> 本表只跟踪 AMC 独立专题的新一轮 GW，不复用 thesis-fso 历史表。

| Step | 状态 | 完成日期 | commit | 关键产出 | 下游门控 |
| ---- | ---- | -------- | ------ | -------- | -------- |
| 1 search | ✅（ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR, D002/V002） | 2026-08-02 | （本轮统一 commit，SHA 见 H001） | search-archive/2026-08-02/（**17 unique queries × 4 data channels = 209 unique**，非"16×5"；published 115/209=55.0%）+ R001 候选问题族地图（**修订后 3 族 A/B/C**，原 F1-F4 合并）+ Step 2 shortlist 12 篇 + `_step1_receipt.json`（force-add provenance）+ 4 alias collision query（0 直接竞品） | — |
| 2 acquire | ✅（**STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED, D004/V005**）— 用仓库历史全文 Nguyen2024（IEEE TAES 2024，Crossref 验证 + SHA256 迁移，**非 OA** 机构授权）补到 **5 CORE 全文** | 2026-08-03 | 本轮统一 commit | **5 CORE 全文 ≥ 5 门槛**：L023/L096/L146/Galijasevic（D003）+ Nguyen2024（D004 本轮迁入）= 5 CORE；C 族 L124 仍 BLOCKED；Safi2019 PROVISIONAL abstract-only（不计门槛）；L075 classification（D003）；L165 AO / L090 fixed-STTC 边界；+ `_step2_acquisition_receipt.json`（12 篇，step2_verdict 更新，superseded_verdict 保留 BLOCKED 历史） | 进 Step 3 前必 ✅（5 ≥ 5，A/B 族 PASS；C 族 BLOCKED） |
| 3 read | ✅ **STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED（S005/D005；旧 STEP3_NO_VALID_PROBLEM 因自创四判据标签被取代）** | 2026-08-03 | 本轮统一 commit | `projects/thesis-fso/literature_notes_amc.md`（canonical 四判据重建 Q#）+ 5 `papers/_read_notes/`（事实提取保留）；旧用 problem_truth/actionability/novelty/thesis_fit 当 terminal gate = Step 4a/MVE+3.5 证据前移循环门控；按 glossary/templates owner 重判 → **Q-A(预测驱动风险失配)+Q-B(动作时间尺度失配) Step 3 层 SURVIVES 待 3.5 闭包**；Q1 场景迁移/Q3 宽集合/Q2 切片重叠不晋级；Q4 Safi/Q5 L124 全文 BLOCKED | 进 Step 3.5 前必 ✅（完成；3.5 本轮执行）|
| 3.5 supplement | ✅（**STEP3_5_SURVIVES，S005/R003**；Q-A/Q-B 均 SURVIVES）| 2026-08-03 | 本轮统一 commit | R003 定向检索（Q-A/Q-B 各 6 query + 引用链 ~190 命中）+ 竞争闭包表（§11）；Safi/L124 仍 BLOCKED；存在 Step 4a 入口但本轮不启动 | 进 Step 4a 前必 ✅ |
| 4a feasibility | ✅(**STEP4A_QA_CONTRACT_A_INCONCLUSIVE + Q_B_BASELINE_UNAVAILABLE, D008/V009/S008**) — D007 授权血缘纠正（Contract B 未获授权）；Q-A Contract A 不可评估；Q-A' 降级 UNAUTHORIZED_DEV_ONLY；Q-B bounded gate = baseline + testbed 双门未过不进 MVE | 2026-08-03 | 本轮统一 commit | **Phase A 授权血缘修复**（git 取证父 0 命中子首现 5 次，voice.md 移除伪造用户原话，D008 精确拆分 D007 科学/代码事实产物保留 vs 授权·scope 层被取代）+ **tune_C1 动作合同缺陷登记**（probe_corrected.py:362 调谐未传 allow_no_transmit，不修复）+ **Q-A 终态=CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH / Q-A'=UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE（NONBINDING）**+ **Phase B Q-B bounded gate**（时间尺度审计 [LITERATURE] + baseline 梯子 B0-B4 + testbed 资产 caller→callee + 方法增量）→ **Q_B_BASELINE_UNAVAILABLE（primary）+ Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET（secondary）**+ **V009 12/12 PASS CONFIRM**。q-b-gate/feasibility-gate-audit.md。D007 科学/代码事实产物（RED→GREEN/Galijasevic 物理身份/corrected_v2）保留为工程事实；D007 授权·scope 层 + V008 check 12 被 D008/V009 取代。**未宣称 Groundwork 闭合**（5 CORE < ≥8 整体门）| 进 Step 5 前必 ✅（**Q-A=Contract A 不可评估待用户裁决；Q-A' 是否升新方向待用户授权；Q-B baseline+testbed 双缺位待用户；Step 5 入口未开**）|
| 5+ | ⬜ | | | — | — |

## 进展线索

- **S001**：专题初始化 + GW Step 1 执行完成。
- **S002**：Step 1 限定完整性修复（Phase A）+ Step 2 acquisition（Phase B）。
- **S003**：Step 2 覆盖纠偏轮（D003 主控裁决）— 补充获取 + CORE 重判 + 治理纠偏；终态 STEP2_BLOCKED_BY_COVERAGE_GAP（4 CORE 全文 < 5）。
- **S004**：Step 2 blocker 解除（D004）+ GW Step 3 全文精读 — Nguyen2024 迁移补到 5 CORE；Step 3 精读 5 CORE+3 边界+2 abstract；**旧终态 STEP3_NO_VALID_PROBLEM 已被 D005 取代**（用自创四判据标签 problem_truth 等）。
- **S005**：Step 3 语义门纠偏（D005/R001）+ Step 3.5 定向补充检索 — 纠正自创四判据 terminal gate，按 canonical 四判据重建 Q-A/Q-B（Step 3 层 SURVIVES 待 3.5 闭包）；执行 Step 3.5 定向检索+竞争闭包。
- **D001**：新系统层范围与旧轴边界。
- **D002**：Step 1 科学完整性限定修复 — 候选族 4→3（A/B/C）+ identity 审计 + provenance receipt（新建，修订 R001 landscape 口径不撤 Step 1）。
- **D003**：Step 2 覆盖纠偏 — 取代 D002/R002/H001 的"Step 2 PASS / 6 篇覆盖三族"判定，修订为 STEP2_BLOCKED_BY_COVERAGE_GAP；保守核心集 3→4（含本轮新获 Galijasevic）；L075 DISPUTED、L165/L090 边界、L124 C 族 BLOCKED。
- **D004**：Step 2 blocker 解除 — Nguyen2024（IEEE TAES 2024，Crossref 验证 + SHA256 迁移，非 OA 机构授权）补到 5 CORE 全文；Step 2 终态 STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED；立即推 Step 3（取代 D003 的 BLOCKED 状态，保留 D003 历史纠偏与 C/Safi/L075/L165/L090 边界）。
- **D005**：Step 3 语义门纠偏 — 取代 D004 末尾用自创四判据（problem_truth/actionability/novelty/thesis_fit）得到的 STEP3_NO_VALID_PROBLEM 终态+Q1-Q5 verdict，修订为 STEP3_READ_COMPLETE_SEMANTIC_GATE_MISAPPLIED；按 canonical 四判据 owner（glossary/templates）重建 Q-A/Q-B（保留 D004 的 Step 2 PASS + 5 CORE + Safi·L124 blocker + 精读事实提取）。
- **R001**（landscape）：AMC Step 1 landscape（209 条逐条审查 + 原始 F1-F4 候选问题族 + Step 2 shortlist 12 篇 + 8 问诚实结论；**candidate-family 计数与 source 口径已被 D002 修订；§4 F1-F4 headers banner 已闭合 V003 Issue 1**）。
- **R001**（receipt，本专题）：semantic-gate owner receipt（D005）— canonical 四判据 owner 路径+SHA256+行号+原文+Step 职责逐字核对。**注**：两个 R001 以路径区分（landscape 在 search-archive 旁；receipt 在 .sessions 专题目录）。
- **R002**：Step 2 acquisition 覆盖面报告（Phase B 产出，**已被 D003 supersede，顶部加 banner**）。
- **R003**：Step 3.5 定向检索 + 竞争闭包记录（**本轮待写，S005 子 agent 返回后**）。
- **V001**：Step 1 原 12 项 checklist 独立验证（PASS 12/12；漏审 identity + source provenance，V002 已闭合）。
- **V002**：Step 1 限定完整性修复验证（Phase A 修订 PASS）。
- **V003**：独立 fresh-context 终审（PASS 10/12 + 2 PARTIAL；2 PARTIAL = R001 body 未加 D002 banner + receipt 未 force-add；本轮合并入 verifications.md，独立 V003 文件删除）。
- **V005**：D004 + Step 3 终态独立验证（**保留历史不删**；**D005 标语义失效**：验证的是本地自写合同 problem_truth 等四列一致性，未核对 canonical criteria owner，因此科学语义层失效。回归候选：verifier 必须核对 canonical criteria owner）。
- **V006**：D005 + Step 3.5 终审验证（**本轮待写**，独立 verifier 核对 canonical owner + 竞争闭包 + 10 项 checklist）。
- **H001**：Step 2 → Step 3 交接（**已被 D003 supersede，顶部加 banner**；交接前提"Step 2 PASS"不成立）。
- **H002**：Step 3 终态 STEP3_NO_VALID_PROBLEM → Step 3.5 定向补充检索交接（**其前提"无 Q#"已被 D005 取代**；交接的"Step 3.5 是下一合法动作"方向正确，但理由从"无 Q#"改为"按 canonical 四判据 Q-A/Q-B SURVIVES 待 3.5 闭包"）。
- **H003**：Step 3.5 终态 → Step 4a/用户决策 交接（已被本轮 S006/D006 执行交接内容；Step 4a 已执行）。
- **S006**（本轮）：GW Step 4a Q-A — A0§0(Q-B 判据3致命暂存)/A0§1-6(PASS,§6条件性)/A′/A/B(条件性)/Phase C headroom probe + V5 独立重算 → **Q-A 实例化 KILL（recommendation）**，family 不 Kill，2 reframe 路径记录。**科学层 KILL 被 D007 撤回**（执行合规性保留）。
- **D006**：Step 4a Q-A 实例化 KILL（MVE 证据驱动）。**科学层被 D007 取代**（保留执行合规性 + 作 RED 根因历史材料）。
- **V007**：D006 + Step 4a bounded MVE 独立终审。**科学层被 V008 取代**（保留历史）。
- **S007**（新建）：GW Step 4a Q-A 科学完整性修复 — Phase A 10/10 RED_OBSERVED + Phase B PDF 身份 + Phase C 10/10 GREEN + Phase D feasibility-first 两契约重测 + V008 verifier 12/12 PASS → **D006 科学 KILL 撤回（D007）；Q-A Contract A 不可评估，Contract B 存活为 reliability-throughput tradeoff，Q-A' reframe 待用户裁决**。
- **D007**（新建）：STEP4A_EXECUTION_INVALID_PHYSICS_AND_ALGORITHM — 取代 D006 科学层 KILL；Q-A 在 Contract B 存活；保留旧 raw/code 加 INVALIDATED_BY 指针。**授权·scope 层 + 'Contract B 获授权/Q-A 在 Contract B 存活/Q-A' 晋级' 被 D008 取代**（科学/代码事实产物保留为工程事实）。
- **V008**（新建）：D007 独立终审 12/12 PASS CONFIRM（fresh-context verifier，PDF 视觉核对 + 手工复算 trajectory Δ<1e-12 + raw→aggregate 重算一致）。**check 12 terminal verdict + 结论段授权层被 V009 取代**（V008 没有核查授权 provenance；check 1-11 科学事实继续有效）。
- **S008**（新建）：D008 授权血缘修复 + Q-B bounded gate — git 取证确认"同时跑两个动作契约"伪造 provenance（父 0 命中子首现 5 次）；D008 精确拆分 D007；voice.md 移除伪造条目；tune_C1 动作合同缺陷登记；Q-A=CONTRACT_A_INCONCLUSIVE / Q-A'=UNAUTHORIZED_DEV_ONLY；Q-B bounded gate = BASELINE_UNAVAILABLE + TESTBED_UNAVAILABLE_WITHIN_BUDGET，不 Kill family，不进 MVE。
- **D008**（新建）：D007 授权血缘纠正 — Contract B 未获授权，Q-A' 降级 UNAUTHORIZED_DEV_ONLY_REFRAME_PROBE（NONBINDING）；Q-A 终态修订 CONTRACT_A_INCONCLUSIVE_TESTBED_ACTION_MISMATCH；tune_C1 缺陷登记（不修复）；不新开 Q-A' GW 周期。
- **V009**（新建）：D008 + Q-B gate 独立终审 12/12 PASS CONFIRM（provenance 修复 A1-A5 + Q-B gate B6-B10 + 治理 C11-C12）。
- **H005**（新建）：D008 纠正授权血缘 + Q-B bounded gate 完成，多裁决待用户（Q-A 停止 / Q-A' 升级 / Q-B 停止 / 补齐 CORE）。
- **D009**（新建）：AMC Groundwork 科学冻结 — `AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT`。用户 campaign-level synthesis 裁决三条路线全部停止（Q-A STOPPED_INCONCLUSIVE / Q-A′ HARVEST_ONLY_ENGINEERING_SEED / Q-B STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE）；不补 CORE、不搭 testbed、不重开 Safi/L124；保留全部历史不改写；恢复须显式 scope-change + 新开 GW 专题。
- **H006**（新建）：AMC dormant 最终交接 — 专题冻结，恢复条件 + campaign-level 论文综合指针。
- **campaign-level synthesis**（新建）：`projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md` — 全项目 contribution inventory（9 项分级）+ 唯一推荐 thesis spine（一个主方法 + 完整实现验证 + 边界分析）+ 第二工程贡献判断（NO_SECOND_CONTRIBUTION_YET）+ 可选 bounded package（fixed-point vs 浮点对比，不在本轮执行）。
- **Q-B gate audit**（新建）：`projects/thesis-fso/amc-groundwork/q-b-gate/feasibility-gate-audit.md`（B1 时间尺度 + B2 baseline 梯子 + B3 testbed 资产 + B4 方法增量 + B5 未执行 + C 终态）。
- **feasibility_report_v2.md**（新建，不覆盖旧）：`projects/thesis-fso/amc-groundwork/feasibility_report_v2.md`。旧 feasibility_report.md 加 INVALIDATED_BY_D007 banner 保留。**本轮补 §9 Q-B bounded gate 段**。
- **feasibility_report.md**（新建）：`projects/thesis-fso/amc-groundwork/feasibility_report.md`（Q-A Step 4a 完整 A0/A′/A/B/D + Kill 裁决 + 可回收产出）。

## 当前位置

**专题已 dormant — AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD（D009，2026-08-03）**:

用户 campaign-level synthesis 裁决三条路线全部停止，专题转 dormant:

- **Q-A = `STOPPED_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`**（Contract A 下不可评估，非 Kill）。
- **Q-A′ = `HARVEST_ONLY_ENGINEERING_SEED`**（corrected_v2 工程种子保留，不晋级、不进论文正文）。
- **Q-B = `STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE`**（baseline + testbed 双缺位，非 Kill family）。
- **不得写成"领域无问题"**——只能写"当前目标条件和现有资产下没有得到可授权的第二项主方法"。
- **保留全部历史**：D001-D009 / V001-V009 / S001-S008 / H001-H005 + corrected_v2 工程产物 + unauthorized probe，不改写历史。

**对论文的影响**（见 `direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`）:
- AMC **不产生**第二项主方法（thesis-map 方案 B 生效）。
- 唯一 T3 主贡献仍是既有 DA/NDA adaptive CPR。
- 第二工程贡献 = `NO_SECOND_CONTRIBUTION_YET`。
- Q-A′ corrected_v2 最多作 future-work 一句，不进正文。

## 未决项

**专题 dormant，无活跃未决项。** 历史未决项（Q-A/Q-A′/Q-B/CORE/Safi/L124）已被 D009 统一裁决为"停止"。恢复条件见下一合法动作。

## 下一合法动作

**专题 dormant。下一合法动作 = 显式 scope-change 恢复**（用户决定）。

恢复条件（出现以下之一才允许，且须新开 GW 专题从 Step 1 开始，FR-22）:
- 出现新的直接论文（coherent sat-ground AMC 同任务）；
- 现成合法 baseline（B2 同任务增强对手）可用；
- 外部 testbed 资产（不搭 multi-day）可用。

**禁止**（专题 dormant 期间）:
- 禁在本 dormant 专题内续接任何 Q-A/Q-A′/Q-B 工作。
- 禁补 3 篇 CORE 只为满足 ≥8 数量门。
- 禁搭 multi-day coherent sat-ground AMC testbed。
- 禁重开 Safi/L124 blocker。
- 禁把 AMC 写成"领域无问题"。
- 禁复活 INVALIDATED 资产 / 晋级 unauthorized Q-A′ dev signal / 把弱资产机械拼成方法。
- 禁修改 Skill / common/ params.py / 正式论文正文 / dormant receiver / 4 个 p05 log。
- 禁进 Contract/Execute。
