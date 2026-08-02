# Topic Index: 星地相干 FSO 自适应编码调制 (AMC) Groundwork

> 状态: active | 创建: 2026-08-02 | 最后更新: 2026-08-02（GW Step 1 限定完整性修复完成 D002/V002：候选族 4→3 (A/B/C) / L124 身份闭合到 bibliographic 级 / 6 dup-abstract 组 18 条抓取污染确认 / provenance receipt 固化；进入 Phase B Step 2 acquisition）

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
| 2 acquire | ✅（PASS，6 篇合格 content.md，待用户验收覆盖面） | 2026-08-02 | （本轮统一 commit，SHA 见 H001） | papers/doi/{10.1038_s41377-023-01201-7, 10.1109_jlt.2023.3242215, 10.1109_tvt.2021.3127193, 10.1109_jiot.2025.3600439, 10.1109_access.2025.3650714}/ + papers/manual/L090-intechopen/ （6 篇 content.md 294–863 行）+ R002 覆盖面报告（A/B/C 三族覆盖）+ L124 bibliographic 级身份闭合 | 进 Step 3 前必 ✅（用户验收后） |
| 3 read | ⬜ | | | literature_notes（AMC 专属） | 进 Step 3.5/4a 前必 ✅ |
| 3.5 supplement | ⬜ | | | 补充检索 + 更新 notes | 进 Step 4a 前必 ✅ |
| 4a feasibility | ⬜ | | | feasibility_report.md | 进 Step 5 前必 ✅ |
| 5+ | ⬜ | | | — | — |

## 进展线索

- **S001**：专题初始化 + GW Step 1 执行完成。
- **S002**：Step 1 限定完整性修复（Phase A）+ Step 2 acquisition（Phase B）。
- **D001**：新系统层范围与旧轴边界。
- **D002**：Step 1 科学完整性限定修复 — 候选族 4→3（A/B/C）+ identity 审计 + provenance receipt（新建，修订 R001 口径不撤 Step 1）。
- **R001**：AMC Step 1 landscape（209 条逐条审查 + 原始 F1-F4 候选问题族 + Step 2 shortlist 12 篇 + 8 问诚实结论；**candidate-family 计数与 source 口径已被 D002 修订**）。
- **R002**：Step 2 acquisition 覆盖面报告（Phase B 产出）。
- **V001**：Step 1 原 12 项 checklist 独立验证（PASS 12/12；漏审 identity + source provenance，V002 已闭合）。
- **V002**：Step 1 限定完整性修复验证（Phase A 修订 PASS）。
- **H001**：Step 2 → Step 3 交接。

## 当前位置

Phase A（Step 1 限定修复）PASS（D002/V002）。Phase B（Step 2 acquisition）**PASS**：6 篇合格 content.md（L165/L023/L096/L146/L075/L090），覆盖 A/B/C 三族，引用质量 0% 预印本。L124 bibliographic 级身份闭合（Optics Express 34(14):26128, DOI 10.1364/oe.595557，coherent-FSO AMC），全文 coding/CSI 待用户手动获取。5 篇下载失败 + 2 篇中文 manual_required 进入用户 blocker，但不阻塞 Step 2 PASS（6 > 5 门槛，三族覆盖成立）。详见 R002/H001。

## 未决项

- L124 全文（coding/CSI/channel/scenario）——用户手动获取 DOI 10.1364/oe.595557。
- L075 标签修正（实为 classification 非 AMC）——Step 3 待办。
- 中文检索 cookie/IP（L050/L206）——校园网可用时重试。
- 候选族最终数（2-3）待 Step 3/4a 后定。

## 下一合法动作

Step 2 PASS 后唯一合法动作：**主控/用户确认覆盖面后进入 Step 3 全文精读**（独立新对话，先读 `stages/gw-read.md`）。L124 全文为 Step 3 第一优先（用户补全文后精读池 L023/L096/L146/L165/L090/L124）。禁止直接进入 Step 3.5/4a。
