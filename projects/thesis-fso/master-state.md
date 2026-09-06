---
project: thesis-fso
direction: 星地激光通信（FSO）——子地带由地勘（S003 方法论 Step 0）全景表分类后选定，不预设
method_type: reference-method extension（非 ML；完整 deployable action chain，最终形态待 Step 3/4a）
domain: comms
created: 2026-06-21
updated: 2026-08-30
current_step: THESIS_METHOD_PRODUCTION_CP035_CH4_AUTHOR_MATERIAL_PACKAGE_READY
current_stage: GROUNDWORK
---

# Master Agent: thesis-fso

> 本文件 2026-06-21 由框架改造 3（缺陷 C 状态层修复，LOG-001）补建。
> 补建前 thesis-fso 无 master-state.md，跨 Step 无硬门控——agent 在 Step 2/3/3.5/4a 全 ⬜ 的真空里跑了 5 个方向（N1/③/A3/4b#1/(c)）全 Kill。本文件 + GW Progress 表把跨 Step 硬门控（FR-22）落到磁盘。

## §1 角色定义

你是研究项目 `thesis-fso` 的 Master 编排 agent。职责见
`templates/master-state-template.md` §1。禁止项同模板（不直接读论文
`content.md`、不直接 WebSearch、不由主控运行长脚本）。D004 与当前长期 Goal
取代旧的“用户中转/用户判断科学正确性”接口：主控自行作科学裁决，项目规则要求
执行与验收分离。D026 已停止长期 Goal 自动续跑并恢复普通 GLM 接力：Master
提供短启动提示词，技术细节写入文件，用户只中转任务路径与五项回执。

## §2 项目状态

### 论文方法收获旁路（不改变当前 Groundwork stage gate）

> **2026-08-07 D036/V020**：历史 T005 scheduling-only 证据已从失败的 Q(8,6) fixed-point 复合
> authority 中拆出，并按真实动作归属闭合为 `CCISP select-before-execute single-branch receiver
> architecture`，terminal=`THESIS_ENGINEERING_METHOD_READY`。该结论只授权 Ch5 方法写作与图表整合；
> 不创建新 GW 方向，不改变本文件 frontmatter 的 current_step/current_stage，不修改 CCISP 算法本体，
> 也不授权 fixed-point、硬件综合或新物理场景。

### 当前控制面桥接

> **2026-08-30 D073 / V048 / S028（当前最高 authority）**。Ch4 作者材料包已由 T096 独立终验；两项编辑级 P2
> 最小修复后 P0/P1/P2=`0/0/0`，terminal=`CH4_AUTHOR_MATERIAL_PACKAGE_PASS`。CP035 状态为
> `CH4_AUTHOR_MATERIALS_READY` 并停机等待用户；禁止自动执行 T093、总纲改写、Ch5、仿真、检索或新方法。

> **2026-08-30 D072 / S028（只读背景）**。用户明确暂停完整正文，要求先准备可由作者慢慢组织的材料。
> T093=`PAUSED_NOT_EXECUTED`；T094/V047 已以 814 行逐字段最大差 `0.0`、P0/P1/P2=`0/0/3` 独立验收图表。
> CP034 当前只开放 T095 formal fact/method/claim/citation cards、方法图、作者素材索引与跨章接口说明，随后独立审查并停机。
> 禁止 `chapter-draft.md`、总纲/Word改写、新增仿真、重归约或恢复 Ch5。

> **2026-08-30 D071 / V046 / S028（只读背景）**。T091 canonical publication exit=0；
> aggregate SHA=`916c4ba5...5602`、receipt SHA=`0fac1304...e697`。独立 reviewer 从 immutable raw 重算
> 570 pooled BER、76 paired cells、4 whole-curve comparisons 与 grade，757 个节点最大绝对差=`0.0`，
> grade=`A`、chapter gate=`true`、P0-P1-P2=`0-0-3`。CP033 只开放 Ch4 formal 图表/表格、完整章节草稿与
> 独立论文审查；禁止新增仿真、重归约、改科学 artifacts、恢复 Ch5 或开启新方法。

> **2026-08-30 D070 / V045 / S028（只读背景）**。T090 direct reducer在内存完成后、首次publication
> import处因空PYTHONPATH报`No module named projects`，exit1且无aggregate/receipt/tmp；raw与11项authority bytes
> 均exact。独立无写入probe确认显式`PYTHONPATH=repo;simulation;seam`可闭合import且environment不变。CP032
> 只开放T091同一entry一次corrected publication attempt与独立raw-only统计复算；禁止改bound code或重跑formal。

> **2026-08-30 D069 / V044 / S028（只读背景）**。T089唯一formal进程exit=0，canonical raw
> SHA=`642c7ae9...a72c5b`、size=`89,419,500` bytes、census=`128/384/15232/76160/ref128`；独立
> reviewer对namespace、hash、pairing、truth与delta0穷举复核为P0-P1-P2=`0-0-3`，且未读取BER/grade。
> CP031只开放T090 canonical reducer一次与独立raw-only统计复算；作图、正文与Ch5仍关闭。

> **2026-08-30 D068 / V043 / S028（只读背景）**。T088让focused suite在lock absent/present两态
> 均`19/19`，replacement lock唯一生成并独立终验为SHA=`095dc989...227987`、P0-P1-P2=`0-0-3`；
> manifest、runner/reducer/entry/tests、deps、HEAD与environment actual match。CP030只开放T089 exact `--formal`
> 一次生成128-latent canonical raw；成功后先独立raw-only复核，禁止提前reduction、grade、作图或正文。

> **2026-08-30 D067 / V042 / S028（只读背景）**。T087 runner/reducer/entry与唯一ID29999
> OS-temp smoke均通过，census=`1/3/119/595/ref1`；但首个tracked lock SHA=`3942883a...a45a492`
> 生成后的fresh suite仅`17/19`，两项pre-freeze测试永久要求canonical lock不存在，故该lock终态FAIL且formal
> IDs继续禁止。CP029只开放T088：删除exact invalid lock、把测试改为final-state safe、保持runner/reducer/entry
> 字节不变并生成/独立复核replacement lock；禁止重跑smoke、formal production、作图或正文。

> **2026-08-30 D066 / V041 / S028（只读背景）**。T086 canonical tuning经独立raw-only复算12个
> objective最大差0，ID20999/21999 structure smoke PASS；stale-test receipt以同一immutable raw修复。
> scientific manifest唯一冻结为SHA `417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`，
> 固定formal IDs、5:2:41网格、三scene/Np、mismatch、bootstrap、grade与tau lineage。CP028只开放T087
> formal runner/reducer/tests TDD、OS-temp ID29999全网格单latent smoke与唯一execution lock；禁止运行
> IDs `30000..30127`、作图或正文。

> **2026-08-30 D065 / V040 / S028（只读背景）**。T085 immutable raw 经独立 raw-only 复算为
> artifact P0-P1-P2=`0-0-0`，但预注册 C4-vs-B3 pooled Np2 CI 跨 0，科学 terminal 保持
> `CHEAP_COMPARATOR_NOT_CLEARED`；生成器字节复现绑定如实为 `PARTIAL`。按 D031/D032 的硕士级标准，
> 强邻居不再自动否决章节，也不得隐藏。Ch4 现收缩为统一的方向—尺度解耦短导频偏振解复用方法族：C4
> 为 channel-domain 无参数主变体，B3_PSC 为 receiver-domain pilot-calibrated 强变体/ablation。CP027 只开放
> T086 disjoint tuned-B2 development、非论文结构 smoke 与 scientific manifest/execution-lock 设计冻结；
> formal production、作图与正文仍禁止。

> **2026-08-30 D064 / V039 / S028 thesis method production bridge（只读背景）**。T084 已冻结
> balanced pilots、七路 SeedSequence namespace、跨 SNR/Np latent pairing、三档 runtime authority、B3_PSC、
> mismatch 与 truth firewall。初审 consumer provenance `INVALID/P0-P1-P2=0-1-1` 由 17-case RED→GREEN 修复，
> fresh final=`PRODUCTION_CORE_CORRECTNESS_PASS/P0-P1-P2=0-0-1`；P2 仅限制 B3 mechanism metric 标签。
> CP026 唯一开放 T085 fixed A2 bridge：moderate `14/18 dB×Np2/4×64 shared latents`，C4 必须同时越过
> B2 与 B3_PSC；禁止 Task 5 tuning/full smoke、formal production 与正式正文。
>
> **D061 / V036 及之前 bridge（只读背景）**。T081 已完成
> Ch4 production-evidence preflight；第一轮独立审查的 5 个 P1 与第二轮的 3 个 P1 已逐项修复，fresh terminal=
> `CH4_PRODUCTION_PREFLIGHT_READY/P0-P1=0-0`。完整路线冻结为 A1 exact historical-observation demapper replay→
> A2 new production-seam bridge→smoke/B2 disjoint tuning→manifest freeze→128-window formal production→
> raw-only/whole-curve bootstrap→独立验证→章包。C5-5 继续暂停。CP023 唯一开放 T082：以 TDD 修正公共
> `m16apsk_demod` 为全 16 点欧氏最近邻并运行直接相关回归；禁止 historical replay、smoke、BER grid、
> production、算法身份变化与正式正文。旧 T071/Ch3 raw 保持 immutable，跨章兼容债务单列。
>
> **D060 / V035 及之前 bridge（只读背景）**。T080 已完成
> C5-5 两篇冻结全文的 Step 3：唯一 Q-C5-5 四判据 4/4，ordinary CRC/syndrome early stop 是 mandatory
> cheap comparator、非完整动作吸收；P0 2019 exact-collision/provenance debt 仍保留。按用户新的明确优先级，
> C5-5 暂停在 `STEP3_C5_5_Q_SURVIVES_READY_FOR_STEP3_5`，CP022 不开放 Step 3.5、实现或仿真。当前唯一
> foreground 是 Ch4 production-evidence preflight：把既有 `14/18 dB × Np=2/4` four-cell confirmation
> 与最终章级合同分开，统一 Ch3 的实用 pre-FEC BER/FEC 门限、SNR/湍流口径，审计现有 simulator seam，
> 冻结完整 BER–SNR、pilot 规律、required-SNR gain、NMSE/inverse-residual 机制、紧凑星地场景迁移、
> scaled-unitary mismatch boundary 与复杂度证据。preflight 独立接收前禁止 smoke/production；C4 action、
> B2 主对手、DP-(8,8)-16APSK 双偏振平台、truth firewall 和有限 claim 不变。
>
> **D059/V034 及之前 production history（只读背景）**。目标是在共同
> DP-(8,8)-16APSK+BICM/LDPC coherent FSO 平台上为 Ch4/Ch5 形成两个证据有效的方法章包。
> T039–T041 已完成新一轮 GW Step 1：共同平台默认 `single-tap 2×2 Jones`；多 tap FIR 只有在
> receiver filter/IQ timing-skew 等直接 authority 下才开放；Ch4 主候选为 C4-2 ring-aware
> semi-blind refinement 与 C4-1 scaled-unitary pilot-LS；Ch5 主候选为 C5-1 structured
> APSK covariance demapper，C5-2 syndrome rescue 因当前 adapter 只返回 hard information bits 而
> 先作接口后备。T042–T044 已完成：共同平台 6 篇全文、Ch5 6 篇全文均由主控按 D044
> 接受 bounded limitation；Ch4 已有 5 篇经典全文，但缺 APSK 直接均衡全文，仍停在 Step 2。
> T045 已用 Baldi 2012 direct APSK DFE/LMS 全文闭合 Ch4 Step 2；T046 已完成 Ch5 六篇精读，
> Q-C5-1=`4/4`、`NOT_EXACT_COLLISION / STRONG_PRIMITIVE_COLLISION`；T047 已冻结 6 个平台项并
> 将 filter/FIR 口径保留为 conditional UNKNOWN。T048 已完成 Ch4 七篇精读：Q-C4-2
> `SURVIVES / NOT_EXACT_COLLISION`，Q-C4-1 只作 bounded backup；T049 已完成 Ch5 Step 3.5，
> 63 个去重记录未确认完整 recipe 碰撞。T050 又以 15 个 archive、305 个去重记录闭合 Ch4
> Step 3.5，Q-C4-2=`SURVIVES`，最强邻居是摘要级 Di Rosa–Richter 2021；T051 判定 Ch5
> `PAPER_DIMENSIONS_PASS` 并冻结 candidate v1、B2/B3 强对手与 pre-MVE 停机条件。当前
> T052 已判定 Ch4 `PAPER_DIMENSIONS_PASS`。T053 的 canonical-radius 缺陷经 T058 修复并由 T056
> 独立复验 `PASS`（7 tests）；T054 也由 T057 独立复验 `PASS`（13 tests）。T055 进一步证明 circular
> control 不能冒充 Ch5 target residual，当前唯一合法前进路径是 `Ch4 demux → per-pol Ch3 DA CPR →
> known-pilot residual` 的 receiver-visible bridge。当前 checkpoint=`CP008`：允许 T059 运行预注册的
> Ch4 两轮有界开发，并允许 T060 只做 Ch5 bridge correctness；只有 Ch4 arm/参数冻结后才开放一格
> occurrence smoke。T059 随后按预注册门停止 C4-2：独立重算确认 candidate/cheap 均劣于 tuned plain，
> oracle headroom 约为零；该路线不再修复或重跑。C4-1 的 candidate-specific Step 3.5 已完成，未发现完整
> target-scene recipe 碰撞，但 balanced-pilot 等价将其身份收窄为经典 scaled-unitary 结构迁移。Ch5 的 T063/T065
> bridge 已接收，T066 唯一 occurrence cell 完成 `64/64`，主控从 raw 独立重算 terminal 为
> `DETECTABLE_OCCURRENCE`。T068 随后将 C4-1 裁为 `PAPER_DIMENSIONS_PASS_WITH_BOUNDARY`；T067 在
> 64-window held-out 开发中得到 `NO_METHOD_SIGNAL / D`，Round 2 未运行，C5-1 已关闭。T069 已通过 C0–C5，
> 并在 `14/18 dB × Np=2/4` 四格中相对最强廉价 B2 得到三格显著 BER 改善、一格不显著轻微退化；独立
> raw verifier 为 PASS，方法身份收窄为 scaled-unitary 公共增益—偏振矩阵联合估计；T071 已按 CP012 合法启动
> 固定配方 fresh-seed confirmation。T070 又以 6 篇 qualified fulltexts 闭合 C5-0 Step 2：A/B/C 三桶为
> `4/3/4`，B0 是同一 mismatched demapper 的 `s=1/alpha=1`，matched statistics 单列 `B_match/O1`。
> T071 已完成全新 seeds confirmation，另一上下文从 raw 重算四格与 pooled CI、19 项 fresh tests、256 seeds/hashes、
> truth firewall 和固定参数，结论 `PASS`。T073 又把该证据材料化为事实矩阵、章蓝图、算法框、claim ledger、
> raw-derived CSV/结果图和可编辑方法图，独立审查与主控视觉复核均 PASS，Ch4 terminal=`CH4_WRITE_PACKAGE_READY`，
> 不再开放任何科学或材料化任务。T072 完成 C5-0 六篇 Step 3，唯一 `Q-C5-0` 为 post-Ch4→Ch3 known-pilot
> residual 驱动的 per-frame global channel-LLR calibration，terminal=`STEP3_CLASSICAL_MIGRATION_READY_FOR_STEP3_5`。
> T074 已完成 bounded Step 3.5，未发现同一目标平台九字段完整 recipe；强邻居与 max-log B2=B3 只把
> claim 压到 target-scene classical migration。T075 随后以 `PAPER_DIMENSIONS_PASS_B2` 收口：只保留冻结/黑盒
> LDPC 外部的 current-frame global LLR calibration，内部 adaptive threshold reparameterization 限制 claim，
> B3 exact APP 是同信息预算强 comparator。T076 随后以 10 项 correctness 和 3 项既有 codec 回归闭合
> target DP-(8,8)-16APSK demapper→5G BG2 LDPC；mapper/label、LLR sign、`N0`/`N0/2`、live
> `out_int_inv`、16 filler、clip 顺序、one-frame-one-scalar 与 fresh lifecycle 均通过，修复后独立 reviewer
> 为 `PASS/P0-P1-P2=0-0-0`。T077 随后在固定 128-frame Gate 1 得到 `rho=0.9856654`、单侧下界
> `0.9758980`，但完整 512 frames 上 B0/O1 BER=`0.0492935/0.0533390`，`B0-O1` paired CI 全负；
> terminal=`SINGLE_CELL_NO_HEADROOM`，Gate 3 未开放，C5-0 关闭。T078 随后把 C5-5 收缩为
> per-codeword reliability-driven iteration-budget allocation；Q#/IAO 与最小 per-call `num_iter` seam 成立，
> 但 direct scheduling fulltext 和 ordinary early-stop/equal-update collision 尚未闭合，terminal=
> `STEP1_C5_5_EVIDENCE_GAP_BOUNDED`。T079 随后审计 3 个身份并冻结 Liu et al. 2025 reliability-list
> CBP 与 He et al. 2021 NR-LDPC 两篇 qualified fulltexts；DOI `10.1109/ACCESS.2019.2899106` 的下载
> 候选被核为错误的 2007 arXiv 身份，已安全拒绝，P0 exact collision 仍为 UNKNOWN。terminal=
> `STEP2_C5_5_READY_FOR_STEP3`。CP021 随 T080 完成而履行；该历史 checkpoint 不再授权新动作。

| Thesis method production packet | Step 1 | Step 2 | 下游门控 |
|---|---|---|---|
| Shared coherent FSO platform | COMPLETE / T039 | COMPLETE / T042（6 qualified） | T047 parameter authority COMPLETE；默认 memoryless single-tap，finite FIR conditional |
| Ch4 APSK front-end (C4-2/C4-1) | COMPLETE / T040 | COMPLETE / T043+T045（6 qualified，含 direct APSK） | C4-2 scientific STOP；C4-1 preflight+demapper correctness+A1+core PASS；fixed A2 bridge active / D064+CP026 |
| Ch5 APSK receiver (C5-0/C5-1/C5-5) | C5-0/C5-1/C5-5 COMPLETE / T040–T041+T078 | C5-1 COMPLETE / T044；C5-0 COMPLETE / T070；C5-5 COMPLETE / T079（2 qualified，1 identity mismatch） | C5-1 closed；C5-0 `SINGLE_CELL_NO_HEADROOM` closed / T077；C5-5 Step 3 survivor paused / T080+D060 |

> **2026-08-12 K2 candidate-source / research-object scope change 与 GW Step 1（source D007/R004；new owner D001–D002/S001/R001–R003/V001/H001）**。Q001 保持 `PROBLEM_ABSENT_OR_TOO_SMALL` closed，不调参重跑、不计 Ch4 材料。唯一新对象为 Wang TSP 2022 suffix-pollution 的 bounded multi-hypothesis/fixed-lag task adaptation；预计后续公平比较 5–9 天可接受。Step 1 两轮 11 query：278 raw→242 title-dedup→138 semantic，98 formal=`71.01%`，12 must-read，S2/OA/SerpAPI Scholar 三贡献源。TCOM 2016 裁为 full-general mandatory comparator、非 confirmed exact action；D1/D2 仅是待审设计形态。V001 初审 PARTIAL 0/3/1 的 formal 归并、编号和预声明已修，final fresh verifier PASS 0/0/0；terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`，Step 2 未授权，无 Q#/Go/方法/METHOD_SIGNAL。

> **2026-08-12 K2 GW Step 2 acquisition（D003/S002）**。主控接受 Step 1 coverage，只开放 10 篇 P0/P1 pool 的 canonical reuse、合法获取、identity/hash/content quality 与三路线 coverage。Step 2=`AUTHORIZED / IN_PROGRESS`；动作级精读、collision/Q#/方法裁决及 Step 3 全部未授权。

> **2026-08-12 K2 GW Step 2 收口（R004/V002/H002）**。在授权的 8–12 篇范围内审计 12 篇：9 qualified、8 CORE，正式身份 12/12、2019+ 10/12、合格全文 preprint-source 2/9。A reference/unwrap、B full mixture/fixed-order、C recent coherent optical/FSO 三路线均有全文；P0 C01/C02 闭合。C06/C07/C13 保留全文 limitation。terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；Step 3 未授权。

> **2026-08-12 K2 GW Step 3 启动（D004/S003）**。主控接受 Step 2 coverage，只开放 9 篇 qualified 全文的结构化精读、exact action/complexity contract、comparator ladder 与 canonical Q001 四判据；Step 3.5/4a/实现/仿真保持未授权。

> **2026-08-12 K2 GW Step 3 收口（R005/D005）**。9/9 fulltext read；C02 在 primitive capability 上是 full-general superset、在 Q001 task contract 上是 strong neighbor，非 exact collision。D2 被 C09/C10/C11/C12 分块吸收并降为可选 component；唯一 D1-shaped Q001 四判据 4/4。terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`，只表示存在 Step 3.5 入口；无 Go/方法/METHOD_SIGNAL。

> **2026-08-12 K2 GW Step 3.5 启动（D006/S004）**。主控只开放 Q001 exact-action/claim closure：四类方法 query matrix、C01/C02/C09/C12 双向引用链、承重全文动作核验与最多三轮收敛。Step 4a/实现/仿真/算法参数冻结继续禁止。

> **2026-08-12 K2 GW Step 3.5 收口（R006–R007/D006/V004/H004）**。三轮 new MUST/SHOULD=`5/5→4/8→0/0`，实际筛查 60 条 citation records，新读 9 篇 primary fulltext。ICASSP 2023 已包含 single-tone integer-wrap Viterbi paths、likelihood score、fixed survivor cap 与 unwrapped-sequence output；D1 的 H=3/fixed-lag 只剩参数选择与 standard traceback truncation，未形成新 score/commit/fallback mechanism。60-row ledger/alias arithmetic 经 bounded repair 后 fresh verifier PASS 0/0/0。terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`（具体 cheap absorption）；Q001 closed，Step 4a 无入口。

| Bounded multi-hypothesis unwrap GW Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| 1 search | ✅ COMPLETE / VERIFIED | upstream D007/R004；new D001–D002/S001/R001–R003/V001/H001 + 11 JSON | terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION` |
| 2 acquire | ✅ COMPLETE / ACCEPTED | D003/S002/R004/V002/H002 + machine receipt | coverage 已由 D004 接受 |
| 3 read | ✅ COMPLETE / VERIFIED | D004–D005/S003/R005/V003/H003 + owner/read-log | terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`；Step 3.5 未授权 |
| 3.5 supplement | 🛑 COMPLETE / VERIFIED / CHEAP ABSORPTION | D006/S004/R006–R007/V004/H004/receipt | terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION` |
| 4a feasibility | ❌ FORBIDDEN | — | Q001 prior-art gate failed；禁止实现/仿真 |

> **2026-08-11 新算法专题 GW Step 3.5（D005/D006/S004/R005/V004/H004）**。Round 1=8 queries/45 unique，引用链=121 unique，Round 2=6 queries/4 unique 且 new MUST/SHOULD=0/0。Zhang 2023 全文为 estimator-changing neighbor；Sun/Xie/Qiu 等 direct-action primary evidence 仍不可得。fresh verifier 首验 PARTIAL 0/1/2，bounded repair 后 final PASS 0/0/0。terminal=`EVIDENCE_BLOCKED`，不是 collision/Kill；Step 4a 无入口。

> **2026-08-12 D007 feasibility-first Step 4a 例外（S005，pre-test freeze）**。不撤销上段 novelty debt，只允许 defect smoke。A0/A′/A/B 允许执行；历史 b3 因 truth-h/RNG/offset/FSTS/MRC 债务不复用端到端。独立 sandbox 经 fresh review 修闭 receiver firewall、单偏振 Park/FSTS proxy、equal-noise corrected MRC、paired RNG、递归 AST、strict raw/receipt/grid/schema 与 all-seed bootstrap。dev 仅运行一次：20×18=360 pairs、6480 rows；冻结 B1=`-8 dB`、B2=`K2→L2/K4→L4`、strongest cheap=`B2`，receipt=`test_started=false`。dev AUC delta=`0.0033864` 只作 NON-TEST 诊断。held-out=`NOT_STARTED`；本状态不是方法、Go 或 scientific terminal。

> **2026-08-12 D008/V005/R006/H005 Q001 scientific terminal**。Commit 1=`cbb8a2d` 后五批 held-out=100 seeds×18 cells=1800 pairs/12600 rows。G1 occurrence=`3.1111%`、CI=`[2.3333%,3.9444%]`，低于10%；G2 B0 regret=`0.1114%`、CI=`[-0.3785%,0.4947%]`，outage excess=0。G3/G4 诊断亦不支持：B2 regret=`0.1114%`；multi-vs-power AUC delta=`0.000464`、CI跨0。fresh raw verifier=`PASS 0/0/1`。唯一 terminal=`PROBLEM_ABSENT_OR_TOO_SMALL`，Q001 closed；formal science disposition 与 mission/thesis method disposition 分别为该 terminal、`NONE`、`NO_METHOD / NO_CH4_CONTRIBUTION`。

> **2026-08-11 K2/K3 reference-entry 自动轮换（Ch4 source owner D005–D006/R003/V004/H004，fresh verifier PASS 0/0/0）**。K2 的 suffix pollution 为 published defect，但 future action 未唯一化，order-2/3 Tikhonov mixture/sequence tracker 只构成 `UNRESOLVED_HIGH_RISK / STRONG_NEIGHBOR`，不声称 exact collision 或已完全吸收；完整比较预计 5–9 天。K3 缺 task-matched fixed-JP unequal-reliability published defect，且 Weighted/RW-BPS/unequal-SNR CPR 仅形成待全文闭合的 collision debt。terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_SHORTAGE`；未创建新 GW 专题、未执行 Step 1，`mission_method_delta=NONE`。K1/Q001 继续保持上段 `EVIDENCE_BLOCKED`，不是 scientific failure。

| DSP-outage-aware multi-aperture GW Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| 1 search | ✅ COMPLETE / VERIFIED | D001/R001/V001/H001 + q1–q6 JSON + receipt/matrix | 已授权并完成 Step 2 |
| 2 acquire | ✅ COMPLETE / ACCEPTED WITH LIMITATION | D003/R002/R003；qualified 5，optical CORE 3，P0 limitation | 允许 Step 3；若 Q# 存活，2019 债移交 Step 3.5 |
| 3 read | ✅ COMPLETE / VERIFIED | S003/T007–T010/R004/D004/V003/H003 | terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5` |
| 3.5 supplement | ⛔ EVIDENCE_BLOCKED / VERIFIED | D005/D006/S004/T011–T016/R005/V004/H004 | direct action debt 未闭合；不是 scientific Kill |
| 4a feasibility | ❌ COMPLETE / PROBLEM_ABSENT_OR_TOO_SMALL | D008/R006/V005/H005 + test raw/aggregate；verifier PASS 0/0/1 | Q001 closed；Contract/method/fair comparison forbidden |

> **2026-08-11 coded decoder-feedback C1 科学终态（D027/V021/CP016）**。S1 occurrence=`262/480` PASS；S2 exact 1620 rows 的 damage=`0.06944444444444449` 与 recoverability=`0.04008151917073723` 均未过冻结门。独立 verifier 对证据给出 `PASS 0/0/0`，science verdict=`FAIL`。按顺序 fail-stop，B2、decoder-information、S4、C1、FAIR_COMPARISON_RUN 全部 NOT_RUN；method signal/thesis contribution=`NONE`。

| Coded decoder-feedback GW Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| 0 recover / candidate converge | ✅ COMPLETE | S001/D001–D002/CP001–CP002；step-047–049；主控 source 核证 | C2/C1 两张机制不同预卡 |
| 1 search | ✅ PASS / C1 REFERENCE BASELINE ENTRY | D003–D005/V002；integrated v2.1=93→66；C1 core action exact 但由 D005 降为 baseline M | 允许固定 shortlist Step 2；不重做 broad search |
| 2 acquire | ✅ COMPLETE | D006/CP007；5 篇合格全文 + 2 unresolved；step2 coverage + step-058–065 | 允许 Step 3；全文债保留 claim ceiling |
| 3 read | ✅ COMPLETE / Q1 4/4 | D008/CP009；TVT read note + step-066 | 允许 mandatory Step 3.5；不等于 defect 已成立 |
| 3.5 supplement | ✅ COMPLETE / VERIFIED WITH LIMITS | D009/V003；step-067–083；supplement report | bounded-slice 非碰撞，不等于 defect/贡献成立 |
| 4a feasibility | 🛑 S2 SCIENCE TERMINAL / VERIFIED | D027/V021/CP016；step-203–206；S1/S2 raw artifacts | S1 PASS；S2 damage/headroom双FAIL；B2及后续NOT_RUN |

### 上一 formal 轨迹（RML-FSTS，dormant）

> **2026-08-09 既有状态：Groundwork Step 1–3.5 `✅ completed`；Step 4a=`INCONCLUSIVE / VERIFIED`，terminal=`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`（D011/V007/H006）**。Ch4 reference-method extension D004/T003
> 选择 Wang 2023 FSTS fixed-lag/`BL` condition-dependence 作为唯一独立 Groundwork research object。
> Step 1 已用满 7/7 query：121 unique、4 actual sources、正式发表 58.68%、12 篇 shortlist，质量门 PASS。
> Step 2 已获得 5 篇合格 CORE 并覆盖 C1–C4；T001 已完成5/5全文精读，canonical target Q1四判据4/4。D005/V003 已修正 A 的逻辑方向与近期 baseline 身份措辞。
> mandatory Step 3.5 已完成 8-query matrix、三类真实来源、Wang/Enhanced 双向引用链与三轮止损；qualified evidence 未确认 exact collision。主控接收发现 130981 共享全文漏查与 8 项 blanket blocker 过严，D008 撤回 D007 terminal。D009 授权的 Step 4a 在 performance 起飞前被 structural action-before causality、source-channel non-equivalence、dBm→discrete-noise non-identifiability 三类 hard blocker 阻断，B0 numeric calibration gate 不可执行。没有 scientific raw rows、paired delta/CI、performance grid 或 MVE；B0/B1/B2/O1/C1 数字均 `N/A (NOT_RUN)`。Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`；Contract/Execute/论文写作禁止，object/package计数仍为0/0。
> D012 受限重开只恢复两项输入：T020 三类公开 surface 未找到 exact executable source config，SC1 fields 1–7 exact-closed=`0/7`；T021 对 previous-frame/common-probe 的审计均缺 action-invariant measurement、time-series/feedback/freshness/cost caller path，AB1=`NOT_CLOSED`。D013/V008 verified recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`（V008 P0/P1/P2=`0/0/0`），故上述 scientific terminal与 NOT_RUN 数字均不变。

- **RML-FSTS fixed-lag condition-dependence Groundwork（独立专题，2026-08-08）—— STEP 3.5 COMPLETE / PROVISIONAL SURVIVOR**：
  source-domain defect 与 target FSO crossover 严格分离；future action 只作背景；最强廉价替代保持为
  dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。

  | RML-FSTS GW Step | 状态 | 证据 | 下游门控 |
  |---|---|---|---|
  | 1 search | ✅ PASS | R001 + step1 receipt + 7 query JSON | 允许 Step 2 |
  | 2 acquire | ✅ USER_CONFIRMED | 5 篇合格 CORE + R002 + coverage/receipt + D003 | 允许 Step 3 |
  | 3 read | ✅ completed | 5篇 read-notes/read-log + R003/D005/V003/H003 + receipt；Q1=4/4 | 用户确认后新对话方可执行 mandatory Step 3.5 |
  | 3.5 supplement | ✅ COMPLETE / PROVISIONAL SURVIVOR | R004/D008/V005/H005 + receipts + shared 130981 fulltext；三轮上限 | 保留全文限制，允许讨论 Step 4a |
  | 4a feasibility | 🛑 INCONCLUSIVE / VERIFIED; REOPEN INPUTS NOT CLOSED / VERIFIED | D009–D013/S004–S005/V006–V008/T015–T022/H006–H007 | terminal 5保持；SC1/AB1均未闭合；performance grid/MVE `NOT_RUN`，专题dormant，禁止下游 |

  **Step 4a 终态边界**：Wang Fig. 403/缺坐标是 recoverable gap，不是 hard blocker 的替代；SSRN 6293357 全文债与 strongest cheap comparator 不变量继续保留。本次 public recovery 未闭合 source config，纸面 previous-frame/probe 也未形成 executable protocol。未来只可在作者/source backend与 feedback/time-series testbed同时齐备后再 scope-change；否则维持 Inconclusive 边界。

- **低仰角强湍流 coded-burst reliability Groundwork（独立专题，2026-08-07）—— CLOSED / STEP 1 EVIDENCE INSUFFICIENT**：
  原始目标、六项 reopen gate、outage-vs-burst terminal 与禁止项已在新专题 S001/D001/topic-index 冻结。
  旧 4b#1 的 `Lburst=60–428`、B=27 容量约 810、0/15 超容和 0 dB 上界保持永久有效；只有一手证据
  支持的新物理切片可重开。P08-R2 只作工程资产和不可恢复 outage 反例，不继承方法 verdict。

  | Strong-turbulence coded-burst GW Step | 状态 | 证据 | 下游门控 |
  |---|---|---|---|
  | 1 search | 🛑 STOPPED | S001/R001–R004/D002 | `STEP1_EVIDENCE_INSUFFICIENT` |
  | 2 acquire | NOT_RUN | D002 | Step 1 未通过，禁止 |
  | 3 read | ⬜ FORBIDDEN | — | Step 2 用户确认前禁止 |
  | 3.5 supplement | ⬜ FORBIDDEN | — | Step 3 未完成前禁止 |
  | 4a feasibility | ⬜ FORBIDDEN | — | Step 3/3.5 未完成前禁止 |

- **过采样相干 FSO 联合同步前端（独立专题，2026-08-06）—— STEP 4a KILL_OR_PIVOT / CLOSED**：
  Q1 为 sample-level frame/fractional-timing/CFO acquisition；Q2 为 GG fade 与 SCO 下 timing/carrier
  maintenance/reacquisition。7 篇 CORE 已通过子 agent 精读；D006 重判后 Q1 四判据 PASS，Q2 仅
  判据 3 FAIL。Step 3.5 两轮收敛且未确认 exact collision；JLT 2025 IQ-skew 全文已裁为非 exact
  collision，JOCN 2026 由用户确认不可得并保留 claim limitation。D009–D012/S002–S003 已完成 Step 4a
  discussion 与受限 Probe：B1/C exact-equivalent，joint C 无可用 headroom，terminal=
  `STEP4A_PREFLIGHT_KILL_OR_PIVOT`。V008 独立复验 PASS、blocker=0；H005 为当前恢复入口。完整 testbed
  11–14 日与 5.5–7.5 日 acquisition slice 仅作历史工程背景，不再有执行入口。权威证据见 formal D006–D012、
  `literature_notes_oversampled_sync.md`、`oversampled-sync-groundwork/step3-5-supplement-report.md` 与
  `oversampled-sync-groundwork/step4a-preflight-discussion.md`。

  | Oversampled Sync GW Step | 状态 | 证据 | 下游门控 |
  |---|---|---|---|
  | 1 search | ✅ | step1 search report/receipt | 两张预卡进入 Step 2 |
  | 2 acquire | ✅ | 7 CORE + V003 | 用户已确认 |
  | 3 read | ✅ / Q1 survivor | D006 + step3 report + 7 read notes | Q1 四判据 PASS；Q2 仅判据 3 FAIL |
  | 3.5 supplement | ✅ / COVERAGE HANDLED | D007–D008 + T005–T013 | Round 2 新增=0；Q1 保留 survivor |
  | 4a feasibility | **KILL_OR_PIVOT / CLOSED** | D009–D012/S002–S003/V007–V008/H005 + T015/T016 | 不建testbed/正式MVE；等待用户归档或新M-C-A pivot决定 |

- **P1 Shared M0-Power FOE–CPE Groundwork（独立专题，2026-08-05）—— CLOSED / 历史背景**：
  Step 1–2 已验收，Step 3 九篇精读由 V004 结构终审 PASS；最后一次 bounded closure 用尽 6/6 query，
  仍无 2019+ task-matched baseline。最终 terminal=`RECENT_BASELINE_UNAVAILABLE`，P1=`SUPPORTING_ONLY`，
  专题 closed。generic action 已碰撞，窄 delta 未形成合法 Q；禁止改名重开，不进 Step 3.5/4a/实现/仿真。
  权威证据见 P1 `topic-index.md`、D005、V005 与 H003。

- **C3 Adaptive Intra-Window Segmented CPE Groundwork（独立专题，2026-08-06）—— CLOSED**：
  4/4 query 得到 140 unique；近期 fixed-window baseline 存在，外部同信息同动作竞品未发现，但历史
  exact action 的 reopen condition 未满足。terminal=`PHYSICAL_PREMISE_UNSUPPORTED`，无 Q#，
  Step 2 未执行；禁止提高 linewidth、换 proxy、改名重开或进入 Step 3/4a/实现/仿真。

  | C3 GW Step | 状态 | 日期 | 证据 | 下游门控 |
  |---|---|---|---|---|
  | 1 search | STOPPED | 2026-08-06 | C3 R001/D002；4/4 query；140 unique | 无 Q#，Step 2 禁止 |
  | 2 acquire | NOT_RUN | — | gate stop，非下载失败 | Step 3 禁止 |
  | 3 read | FORBIDDEN | — | 用户范围 + D002 | Step 4a 禁止 |
  | 3.5 supplement | FORBIDDEN | — | 用户范围 + D002 | Step 4a 禁止 |
  | 4a feasibility | FORBIDDEN | — | 用户范围 + D002 | 实现/仿真禁止 |

- **Baseline-first method batch 001（RDL harvest，2026-08-06）—— CLOSED / 历史背景**：
  7 篇合法 baseline 覆盖 AGC+DPLL、STSB/FSTS、short-spectrum FOE、fixed-point VV、receiver-side
  MIMO detection 与 blind radius calibration；5 张完整方法卡分别在 problem evidence、active inventory、
  历史 dead end 或 strongest cheap alternative 门停止。terminal=`STRATEGIC_SHORTAGE_CONFIRMED`，不推荐候选进入 GW，
  不制造第六个弱候选。证据见 `direction-lab/harvest/baseline-first-method-batch-001.md`、system D027/V019。

### 历史背景：2026-08-02 dormant campaign（保留审计，不再称"唯一现行入口"）

> **2026-08-02 D058/V084/CP049 → epoch85 `SATURATED_NO_ACTIVE_CARRIER / DORMANT`**（历史背景）。
> 该 campaign 只保留历史审计与恢复条件；当前入口以本节顶部
> `OVERSAMPLED_SYNC_STEP3_5_COMPLETE_FULLTEXT_BLOCKED` 为准。

- accepted valid packages：**7**（P01–P06 + P07-R）；它们是局部负面/边界，不是七项贡献。
- method-production 结果：`METHOD_SIGNAL=0`，active carrier=0；固定 10 包不再是自动执行目标，`remaining_valid_packages` 退役。
- 无效/部分资产：P08/R/R2 partial chronology；P09 execution invalid；P10 evidence insufficient；P11 实际固定 20 dB partial baseline；G1 scale artifact。
- P11 纠偏证据：cell 标签的 gamma 没有传入 channel generator，generator 使用默认 `GAMMA_BAR=100`（20 dB）。
- 论文资产：A 级仅既有 DA/NDA 自适应 CPR；B/C 级映射见 `direction-lab/harvest/method-production-campaign-thesis-map.md`。
- 当前授权：只做 Research Direction Lab Skill 三类最小 patch 与历史回归；**不运行仿真，不建 P12，不启动 AMC**。
- 恢复条件：新物理自由度、新系统层级或用户明确 scope change。AMC 若获授权，另开 Groundwork 专题并从 Step 1 开始。
- 恢复入口：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/H003-skill-minimal-patch-and-regression.md`。
- **AMC Groundwork（独立专题，2026-08-02 起，2026-08-03 D009 冻结 dormant）**：专题已 `AMC_GROUNDWORK_SATURATED_NO_MAIN_METHOD / DORMANT`（D009）。三路线终态：Q-A=`STOPPED_INCONCLUSIVE_TESTBED_ACTION_MISMATCH`（Contract A 下不可评估，非 Kill）/ Q-A′=`HARVEST_ONLY_ENGINEERING_SEED`（corrected_v2 工程种子保留，不晋级不进正文）/ Q-B=`STOPPED_BASELINE_AND_TESTBED_UNAVAILABLE`（baseline+testbed 双缺位，非 Kill family）。**不补 3 篇 CORE、不搭 multi-day testbed、不重开 Safi/L124**（用户明令）。**不得写成"领域无问题"**，只能写"当前目标条件和现有资产下没有得到可授权的第二项主方法"。恢复须显式 scope-change（新直接论文/现成合法 baseline/外部 testbed）+ 新开 GW 专题。保留全部历史 D001-D009/V001-V009/S001-S008/H001-H006 + corrected_v2 + unauthorized probe，不改写历史。**对论文**：AMC 不产生第二项主方法（thesis-map 方案 B 生效）；唯一 T3 主贡献仍是既有 DA/NDA adaptive CPR；第二工程贡献 = `NO_SECOND_CONTRIBUTION_YET`（见 `direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md` §2.3）。详细 AMC GW Progress（Step 1-4a）见专题 topic-index（保留审计）。**禁在本 dormant 专题内续接 Q-A/Q-A′/Q-B；禁 agent 自行恢复 AMC**。

<details>
<summary>2026-07-29 旧 G1 / Scout 控制面（历史，不授权执行）</summary>

> **历史 D033/CP024 → epoch57 G1 FORMAL LINE CLOSED；T026 THESIS ARTIFACT TASK READY**：
> T009 的独立审查只接收 `BLOCKED_IDENTITY` 与 `mission_method_delta=NONE`；
> 随机 TX payload 被当 pilot、DA/NDA frequency stage 不对称、无来源且无 FEC
> crossing 的 working region，以及 raw/result 未进提交，共同否定“DA 在可靠条件
> 物理支配 NDA”的归因。A4 按预注册边界返回候选池且不再二修。R002 比较
> B10/C15/B1/B9 后，由 D006/D017 激活 B10 source-native adaptive pilot-RLS。
> T010 初次 Phase-B verdict 因 operational residual 反号与无来源 `.999` 被 V008
> 拒收；clean confirm 已由 V012 接收 source identity。D009/D020 分段授权
> Phase C；V021 已接收 C1 implementation contract，method delta 仍为 NONE。
> D010/D021 将下一动作切到 C2 起飞合同独立审查；V022 首轮三个 P1
> 已由 V023 确认关闭，V023 新增 B* exact-tie P1 已按预注册 arm index 补约，
> V024 第三轮 amendment PASS；control/task 递增 epoch 23，V025 最终 binding
> PASS。C2 随后在 28 cells / 840 canonical rows 暴露 deterministic pilot-unwrap
> identity failure；V026 接收 `BLOCKED_IDENTITY`、P0/P1/P2=`0/0/1` 与
> `mission_method_delta=NONE`。不补矩阵、不改 positive-slope gate、不运行 held-out。

- formal stage：`GROUNDWORK`；当前为
  `NO_ACTIVE_SCIENTIFIC_CARRIER / G1_THESIS_ARTIFACT_TASK_READY`。
  B9 与 B12 均已返回候选池。Direction Lab 的
  Scout/Sandbox 结果对正式研究的 promotion effect 仍为 `none`；Direction Lab
  campaign 已 dormant（D022 SCIENCE_FREEZE），无当前科学执行授权。
- **当前工作线**：T024 已追加 CP023。V060 推翻执行者的 Gate6 No-Go：
  正确 seed-cluster pooled bootstrap CI_lo≈`0.885`；但 Phase-A 检索/
  引用/read-note 未形成可提交闭包，D4 comparator 又是 post-CMA 恒等映射，
  因而 formal recommendation 同样拒收。D041 固定 binding disposition 为
  `G1_GROUNDWORK_EVIDENCE_INCOMPLETE / PHASE_B_NONBINDING_DIAGNOSTIC`。
  G1 不再 repair；T025 已接收为 bounded internal packaging source。T026 只把
  既有证据物化为模块化论文小节和正式图，不改变科学上限。
- **Pilot-Jones（退出 carrier）**：D066/V040 接收 fixed complex component rescue
  axis scoped Kill；4 篇 direct competitor 全文债继续保留，但不阻塞当前 carrier。
- P03（暂停，回候选池）：Headroom Atlas Stage A（2026-07-19，S077/D059/V033）runnable 子域 LOCAL_NEGATIVE；16QAM/receiver-CSI/coded-output 三轴 INFRASTRUCTURE_BLOCKED，历史反例落在被阻轴上 → DOMAIN/CANDIDATE/FAMILY 仍 UNRESOLVED/OPEN。**用户选项①已选定：暂停回候选池，不关闭 family**。
- Direction Lab sandbox history：last completed batch = `B003 / COMPLETED_SANDBOX_VERIFIED`；事实源为 `projects/thesis-fso/direction-lab/state/completion-events.jsonl`。`canonical-state.yaml` 仅为机器投影，不是正式研究授权源。
- formal promotion effect：`none`；B001–B003 数字不得进入论文或正式材料。
- 下一合法边界：用户将 T026 交给普通 GLM。任务只生成模块化论文小节、
  可编辑方法流程图、raw-derived 分层结果图和 worker log；不新增实验、检索
  或 formal closure，不修改 thesis framework，不声称 Step4a Go。不得 remap、
  重跑 T024、进入 Step 5 或修 Q15/G1。
  **T017 不得运行 Phase B、旧 C16 sandbox、seeds 71–80、Step 3/Q#/实现/
  seed/MVE，不得第二个 C16 source/formalization package；T016/C15 不得运行 Phase B、
  第二个 source package、seed/MVE、精读或写 Q#；
  不得复用/修 T006、T008/B1、
  T009/A4、T010/B10，不得做第三个 B9 包、T012/T016 amendment、旧 C15 sandbox
  或第二个 B12 repair；C15 无条件不进 Step 3，不复活
  Q14/T018 不得执行 final-binding、Phase A、Step 4a/实现/实验或第二个
  problem-evidence package；
  Scout/P03，不进入 Step 5/Contract/Execute。**

</details>

### 历史 Groundwork 轨迹（保留审计，不授权当前执行）

- 阶段：**方法层重开轨（GW）**。Q-CMA-FADE Contract 曾于 2026-07-15 完成 S0-S5 并冻结；D030 同日只解冻方法层，分析层/方法层旧状态尚待按 D040 分批修正。
- 步骤：**Batch 0.5 已闭合；Batch 1 fade/clip 低信息；Batch 2 已确认 fG 轴无事件、SOP rate=1e-5 有 2/3 seed BER tracking failure**。下一步做高速 SOP failure detector/recovery 最小侦察；不把该信号称为 lock-swap Go。D045 执行方式仍有效：正式 GW/Contract 门控留给批量结果中的少数晋级候选。
- Contract 状态：**曾冻结，方法层已解冻；当前不可授权 Execute**。D040 已推翻旧 Problem/H1 的关键前提——合法 standard-CMA 在注册新域 0/5 swap，fixed≈2e-4；fixed-weight ML 5/5 clean-swap。Contract 的旧 CMA lock-swap 叙事须后续增量修订。
- 方法类型：待新候选完成 Q# + GW Step 1/2/3/必要 3.5/Step 4a 后确定。

### 项目级参数（glossary 四判据 3/4 的当前值）

- 判据 3 baseline 年份范围：**2019 年至今顶刊**（导师"近 5-8 年"，2026-06-20 voice.md）
- 判据 4 对标数量：**每章 1-2 个对标对象**（导师原话，2026-06-20 voice.md）

> 这两个值是 glossary.md 判据 3/4 的项目级参数，记录在本项目档案里（不写进跨项目的 glossary）。

> **重定方向背景**（见 `.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/H002`）：导师反馈后，研究起点从"找空白/试方法"转为"按问题找"。方法形态必须从 GW Step 3 精读浮出，不从开题报告反推。下一轮第一步 = 路径 A（回 Step 3 精读，问题清单从精读浮出，过四判据筛）。

### GW Progress（跨 Step 硬门控，单一事实源）[MUST]

> **当前状态声明**：以下 GW Progress 与方法层重开轨仅保留历史审计和旧门控证据，不授权当前执行；当前正式状态、sandbox 指针、Scout 状态和下一动作只看本节上方“当前控制面桥接”。

| Step | 状态 | 完成日期 | commit | 关键产出 | 下游门控 |
| ---- | ---- | -------- | ------ | -------- | -------- |
| 1 search | ✅ | 2026-05-29 | — | search-archive + landscape.md 683 主表（S003-S010 五轮地勘） | — |
| 2 acquire | ✅ | 2026-06-26 | — | 块 A 7 篇 + 块 B 6 篇全文（OA + IEEE blit），papers/_read_notes/ 10 篇笔记 | 进 Step 3 前 Step 1 必 ✅（已满足）|
| 3 read | ✅ | 2026-06-26 | — | literature_notes.md 重写（10 篇 L## + 综合分析 + **Q# 清单 6 篇全过 4 篇部分不过**） | **进 Step 3.5/4a 前必 ✅，且 Q# 清单非空 ✅（已满足）** |
| 3.5 supplement | ✅ | 2026-06-27 | — | 块 D：盲区 A/B 定向补检索完成（search-archive/2026-06-27/ 7 JSON）+ **召回 Pech2025/Valjus2025/Paillier2019conf 入 Q# 清单（Q11/Q12/Q13，旧 B1 资产 H004 漏召纠正）** + **Paillier2020JLT 下载成功(arXiv LaTeX)+精读完成（条件性细化 Q12 gap）**。Viterbi1983 blit 元数据获（浅读够）。**债务**：Rustum2026(IET非OA)/Tang2024+Mosnier2025(SPIE无源)下不到（不阻塞，Q# 清单非空） | 进 Step 4a 前必 ✅（**已 ✅，Q# 清单 Q1-Q13 非空远超门槛**） |
| 4a feasibility | 🔄 进行中 | 2026-06-28 | — | **Q12=Kill（D006）**。**Q8 切入点 2=Kill（S017，MVE FAIL 散布 0.1-0.3dB）**。**Q8 切入点 4B=Kill（D008，2026-06-28）**：D007 重定义为"仰角驱动 σ² 慢包络自适应 PCS/Rs 调度"，三查坐实物理 gap（σ² 过顶变化 1-2 量级，Fernandes 当链路静态场景），**但 FR-21 数值显示 ABR 对 σ² 平缓，性能 gap 趋零**（vs 中档折中 +0.01dB，A2 指标敏感+A3 增量量级双重硬门槛失败）。**🔴 立「靠谱方向 checklist」v1（D009）**：A1 轻化（可验证处理贡献不锁"DSP 链路"）+ A2（指标敏感，4B 教训新提炼）+ A3（增量≥同门~2-4dB）+ B1/B2/B3 + C1/C2/C3。**Q1=Kill（D010，2026-06-28）**：D009 checklist 首次实战。**范围双重出界**（不变量6星地 + S007 ISL排除 + 真空无湍流）+ **A1 方法归属错位**（产出形态=论文自己的 TS-KF）+ **C3 堵死抢救**（搬星地撞 Q12/B1 换皮 D006）。A2 在 Q1 自身 ISL 场景反而过（Doppler 真硬动态）。论文 TS-KF **降级 baseline 参考**（未来星地 Doppler 对照）。**Q2=Kill（D011，2026-06-28）**：死因=Q1复刻（范围双重出界ISL+无湍流+A1归属错位+C3撞Q12/B1换皮）。论文降级**方法借鉴+同实验室前作**（二阶DPLL+前馈/ωn-N准则可复用）。**登记「16-QAM CPR扩展」为待回看种子**（Q2自承仅QPSK未扩展16-QAM，未被D006堵死，Step4a全评完后独立评估）。**Q3=Kill（D012，2026-06-28）**：范围双重出界（feeder系统级撞S007+无湍流建模，feeder辨析物理经大气但S007排系统级架构）+A1归属错位（产出形态=论文adaptive MMSE）。**C3未撞旧Kill**（Q3跟Q1/Q2唯一差别）但不构成salvage（A1+范围已双重硬门槛，"没撞旧Kill"≠可救）。论文降级**方法借鉴**（time-packing+MMSE检测框架+SINR-BER闭式可复用）。**🔴 候选池近清零**：四判据全过6候选已Kill 3（Q1/Q2/Q3），D010预测被Q2/Q3连续验证，实质在范围+未死候选仍然只剩Q10（高度同构N1）。**待评**：Q8 切入点 1（指向×Doppler 踩 S007 边界）+ Q7/Q10。feasibility_report.md 含 Q12+Q8+切入点2+切入点4B Kill 段 | **进 Step 5/Contract/MVE 前必 ✅（至少 1 个 Q# Go，暂 0 Go）** |
| 5 validate | ⬜ | | | Baseline 候选表 | 进 Step 4b 前必 ✅ |
| 4b sim-feasibility | ⬜ | | | feasibility_report.md (C/E) | 进 Step 6 前必 ✅ |
| 6 sim-design | ⬜ | | | 仿真器设计规格 | 进 Step 7 前必 ✅ |
| 7 implement | ⬜ | | | baseline_report.md | — |

### 方法层重开轨进度（2026-07-16，D042；优先于上方历史项目表授权新候选）

| Step | 状态 | 证据 | 下游门控 |
|---|---|---|---|
| 状态修复 / 候选重置 | ✅ | S036 + D042 + D043 | 只授权进入新候选 Step 1 |
| residual cascade Step 1 search | ✅ | R009 | 已完成；结论 DEFER，未发现直接 additive-residual 先例 |
| residual cascade Step 2 acquire | ✅ | S037 | 5 篇可读全文输入达到质量门 |
| residual cascade Step 3 read | ✅ | S038 | 5/5 精读；四判据 1/3/4 PASS、2 UNKNOWN |
| Q14 mandatory Step 3.5 supplement | ⏸ FROZEN_UNRESOLVED | R008 / V050–V051 / live D025 / formal D036 / T018 / D026 | T018 未执行且不是当前 workline |
| Q15 prefix-gated radius calibration Step 1-2 | 🟡 PARTIAL | T020 / T021 / live V054 | 检索与全文池可用；三源 PASS 撤回 |
| Q15 Step 3 | 🟡 CONTENT_COMPLETE_REFRAMED | T022 / live V056 / formal D039 | 六篇独立核心内容门过；判据 1/2 PARTIAL，3/4 PASS |
| Q15 nonlinear map | 🔴 NO-GO | live V058/D031 / formal D040 | T023 越过 A4/B0；map 无 gate+scale 外增量，不修复 |
| G1 gated normalization | 🟡 FORMAL CLOSED / T025 PACKAGING ACCEPTED / T026 ARTIFACT READY | live D033/CP024 / formal D041 | 内部有边界方法包已接收；只可生成论文资产，不二修、不晋级 |
| residual cascade Step 4a §0/A0 | **DEFER** | S039 / D044 | Q14 判据 2 UNKNOWN；不作为唯一主线 |
| 候选族地图（CMA-fade/SOP 基点） | ✅ | S041 / D045 | 6 类方法族、约 30 个变体，已按作用时段/接口/成本分组 |
| Batch 0 基线审计 | **PARTIAL** | S042 | paired 基线/口径可重算；CRITICAL=4，recovery-delay 缺口 |
| Batch 0.5 参数/指标闭合 | ✅ | S043–S045 / V006 | 端到端 smoke + 等价性 99 tests PASS；独立逐条审查 PASS |
| Batch 1 Fade 单轴族 | 🟨 | S041 / S046–S052 / V007–V012 | 5M性能批仍PARTIAL；1M fallback合同 PASS但inconclusive；freeze 当前低信息，clip 仅有机制触发 |
| Batch 2 fG lock/swap pilot | ✅ observation-only | S053 / V013 | fG=30/100/1000×3 seeds 全无事件，保留为无事件对照 |
| Batch 2 SOP rate event pilot | ✅ observation-only | S054 / V014 / D047 | 1e-5 在2/3 seed出现 BER failure，无 swap/div/fade；转 detector/recovery 侦察 |
| Batch 2 basic blind detector | 🔴 FAIL / stopped | S055 / V015 pending | cm_error/update_norm/power deviation 对 2 个 oracle failure 提前召回 0/2，控制组各有误报；不进入 recovery |
| Batch 2 evaluator provenance | ✅ | S056 / V016 | evaluator 已固化并纳入源码/SHA，2 TDD tests；真实 scout 尚待转换脚本接入后重算 |
| Batch 2 real blind recompute | 🟨 | S057 / V017 pending | N=100k、warmup=1，三种基础盲信号对2个 oracle failure recall=0/2；待审查后关闭支线 |
| Batch 2 geometry-feature scout | ✅ observation-only | S058 / V018 / D050 | Stokes-like recall=2/2、control FA=0/3；cov-eigen敏感性；cross降级 |
| Batch 2 Stokes-like short pilot | 🔴 PARTIAL / stopped | S059 / V019 / D051 | control 新 seed 有 oracle events，阈值前提失效；不晋级，转 E pilot-assisted |
| Batch 2 pilot-assisted E scout | ⬜ | D051 | dual canonical 稀疏 pilot 注入与 SOP/Jones 估计，先做短 pilot |
| E pilot seam / naive integration | 🟨 PARTIAL | S061 / V020 | seam角度估计可行且overhead 6.25%；naive injection无BER收益，集成脚本provenance待补 |
| E pilot Jones derotation | 🟨 feasible short integration | S062 / V021 / D052 | 公平性/泄漏审查PASS；failure seeds BER→0，准入新seed/rate/pilot-count扩展，非性能Go |
| E pilot Jones 72-cell expansion | 🟨 PARTIAL | S063–S064 / V022 / D053 | 正确≥50%计数：2p9/15、4p13/15、6p14/15；不改门槛，先做inverse稳定化 |
| E 6-pilot Jones EMA09 gate | ✅ family promotion | S065 / V023 / D054 | full24原门槛15/15、clean0/9；晋级正式GW Step1，非Go |
| Pilot Jones EMA09 formal GW Step1 | ✅ | S066 / D055 / V025 / V026b | 82候选/3源/正式比例68.3%；必读6；generic机制撞车、窄问题收敛 |
| Pilot Jones Step2 acquisition | 🟨 | S067 | LCOMM2026全文已有；4篇DOI all_failed并留metadata；Step1分类标注已补 |
| Pilot Jones Step2 gap follow-up | 🟨 | S070 | 4 DOI补检无可读稿件；转共享papers库邻近全文，失败条目不冒充已读 |
| Pilot Jones Step3 five-paper read | ✅ | S069 / S071 / V027b | 5篇结构化精读、read-log、Q1合法；Q2已按D055纠正，进入Step3.5 |
| Pilot Jones Step3.5 supplement | ⚠ WAIVED_TO_STEP4A_WITH_BLOCKING_DEBT | S072–S074 / D056 / D061 / D062 / V028–V029 / V035 | backward 与收敛门闭合；4 篇全文继续 BLOCKED_NO_FULLTEXT。D062 只豁免进入 4a，不把本步改写为 PASS。|
| Pilot Jones Step1 classification | ✅ | S068 / V026b | candidate_key/top-level stats；必读6、formal56、direct5/adjacent26/none51 |
| 候选族批量 MVE | ⬜ | — | 统一 baseline/seed/消融后执行 |
| 晋级候选正式 GW Step 1→4a | ⬜ | — | 仅对批量胜者补齐 |
| Pilot Jones Step4a unitary slice | 🔴 UNITARY_REAL_ROTATION_MCA_KILLED | D062 / T002 / S079 / V036 / V037 / D063 | 结构性 cond=1 结论成立；V037 修正 contract stale count 与无依据的 BER-ratio→dB 门。只 Kill 当前实例化，不 Kill family。 |
| Pilot Jones Step4a complex-model salvage | 🔴 SCOPED_AXIS_KILLED / RETURNED | D063–D066 / T003–T005 / S080–S082 / V038–V040 | T005 fixed/verified primary 8/8 cells max point/CI upper=0.0804/0.2372dB；scientific scoped Kill PASS，integrity PARTIAL；不再是当前 carrier。 |
| High-order CPR B10/B12 combination Step4a（历史 T006） | 🔴 SCIENCE_VERDICT_REJECTED / UNRESOLVED | step4a D012–D013 / S014–S015 / V001 / live T006 | 工程 PARTIAL；source/channel/statistics 多重失效，不 Kill family，不继续修组合实现。 |
| B10 source-native adaptive pilot-RLS Step4a | 🔴 BLOCKED_IDENTITY / RETURNED_TO_POOL | step4a D022 / live D011/V026/T010 | C2 在 840-row strict prefix 暴露 128-pilot unwrap 错误 branch；method delta NONE，不补矩阵、不改 gate、不开第二修复包。 |
| C15 blind-equalization cost family | 🟠 BLOCKED_FORMAL_READINESS / RETURNED / NO_SECOND_SOURCE_PACKAGE | formal D032 / live D021/V047 / T016 | 五个数量门局部 PASS，但三组同标题双非空 DOI 触发 identity hard block；A2/A3/Phase B 未运行，delta NONE。candidate view 仅 partial defensive evidence；禁止 Phase B、第二 source 包、Step 3 与 seed/MVE。 |
| C16-open full-complex FIR non-modulus family | 🟠 BLOCKED_FORMAL_READINESS / RETURNED / NO_SECOND_SOURCE_PACKAGE | formal D034 / live V049/D023 / T017 | 旧 C16 paradigm negative 仍撤回；T017 Phase A 得到 44 unique、R1/R2 direct=1/3，但 source=1<3、must-read=2<5，A6 停止。delta NONE，Phase B 未运行；不修 label/receipt，不给第二包。 |
| B9 virtual-carrier self-coherent + DRE | 🟠 RETURNED_TO_POOL / STEP1_SEARCH_COVERAGE_BLOCKED / NOT_ACTIVE_CARRIER | step4a D028 / live V037/D017 / T013–T014 | T014 A1 raw=0/0/1，实际 source union 仅 OpenAlex+IEEE 两源，三源门失败；唯一 repair 已消费，不得第三包。Step 2/3/MVE 禁止。 |
| B1 adaptive phase-window Step4a | 🔴 BLOCKED_IDENTITY / RETURNED_TO_POOL | step4a D014 / live D002 / V002 / T008 | T008 工程 17/17 PASS，但 no-crossing dB proxy、oracle candidate、eval population 与 artifact closure 失败；不接收 Kill，不再修当前实现。 |
| A4 deployable adaptive CPR Step4a | 🔴 BLOCKED_IDENTITY / RETURNED_TO_POOL | step4a D015–D016 / V003 / live D005–V006 / T009 | pilot/TX-truth、frequency-stage、working-region 与 evidence closure 失败；只接收停止裁决和 method delta NONE，不接收 DA 物理支配；不再同轴 repair。 |

> **FR-22 解释**：上方 2026-06-21 起的全项目历史表证明旧批次曾完成哪些步骤，**不能授权 2026-07-16 后出现的新候选直接进入 MVE**。新候选必须以本重开轨表为单一门控，从 Step 1 重新积累证据。

**硬门控规则（FR-22）**：进入任何下游步骤前先查本表——上游任一项 ⬜ = 禁止进入下游。Step 3 + Step 4a 是 Go/No-Go 硬门不可跳过。本表/literature_notes 进度表任一上游项 ⬜ 时，**禁止进 MVE/Contract/任意"试方法"动作**。跨对话恢复优先读本表。

> **历史教训锚点**（5 次殊途同归全 Kill）：N1(PCS) / ③(MCS排程) / A3(pilot CPE) / 4b#1(自适应交织) / (c)(GG-LLR译码) 全部发生在 Step 1 ✅ 之后、Step 3-4a 全 ⬜ 的真空地带。根因：C1(信道设定)+C2(目标=BER)+C3(单链路DSP) 三轴锁死。详见 `.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/S004`。

### 关键决策

- decision_log.md 尚未创建（待补）。关键历史决策散落在 `.sessions/`：
  - 4b#1 Kill（自适应交织）：`.sessions/2026-06-19-4b1-.../decisions.md` D001
  - (c) Kill（GG-LLR）：同上 D002
  - 重定方向 v2（问题驱动）：H002
  - 框架护栏 FR-22/23/24、TL-30/31：AGENTS.md + thesis-lessons.md

### 活跃文件

- literature_notes.md: projects/thesis-fso/literature_notes.md（**已重写 2026-06-26，块 D 召回更新 2026-06-27，Q1 Kill 标注更新 2026-06-28**：Step 1-3 ✅，Step 3.5 ✅，Step 4a 🔄；含 10 篇 L## + 综合分析 + **Q# 清单 Q1-Q13**，原 6 篇全过中 **Q1 已 Kill（D010 范围+A1归属+C3）降级 baseline 参考**，Q2/Q3/Q7/Q8/Q10 待评 + 4 篇部分不过作方法借鉴 + **3 篇块 D 召回（Q11/Q12/Q13，旧 B1 资产，Q12 已 Kill D006）**）
- thesis-framework.md / cnki-thesis-survey.md: projects/thesis-fso/
- decision_log.md: 待创建
- feasibility_report.md / baseline_report.md: 未创建

## §3 步骤调度表 / §4 FR 防坑清单

见 `templates/master-state-template.md` §3 / §4。本文件不再重复。

## §8 下一步（路径 A，H002 — S003 方法论迭代后）

> **S003 迭代（2026-06-21）**：方法论从"批评汇总作为第一步"升级为"**地勘前置，批评汇总降为地勘后第二步**"。范围从"物理层 DSP 锁死"放开为"**星地激光通信全谱**"（标题对得上即可，湍流可去、处理技术是宽义）。完整脉络见 `.sessions/2026-06-20-problem-driven-redirection/S003`。

**方法论链路（定盘）**：

```
地勘（大范围检索，产 landscape.md 全景表，全留拉表分类）
  → 看分类，选一块"🟢 有缝潜力"的地（判据 A 初筛）
    → 进这块地，批评汇总（框法乙，找问题候选 Q#）
      → 四判据筛 Q#
        → FR-21 oracle 上界量化缝宽（<0.5dB Kill）
          → Q# 进 Step 4a
```

**执行步骤**：

1. 读 `stages/glossary.md`（问题四判据）+ `.sessions/2026-06-20-problem-driven-redirection/H002`（地勘执行规范 + 偏航检查清单 A-E）+ topic-index 不变量段（8 条，S003 更新）
2. **地勘先于批评汇总先于精读**：派子 agent 用 `tools/search` 做大范围检索（检索词 = 星地激光通信大背景，**方法中性不锁模块**，年份 2019+），全留拉表到 `projects/thesis-fso/landscape.md`
3. 主线看全景表分类（🟢有缝 / 🟡不确定 / 🔴死地含 5 次失败轴 + 载波同步/自适应交织/GG-LLR/MCS/信道估计拥挤赛道），**先评估产出质量再选地**
4. **批评汇总（地勘选定地之后）**：在选定地内用框法乙找问题候选 Q#
5. **精读对象由批评汇总结果决定，不由开题线索反推**——Paillier 2020 等开题 4 线索（VV窗口/DPLL/SEP/编码辅助）已降级为事后验证对照（见 S001 第四步 + 不变量 3）
6. Step 3 精读（进 Step 3 前读 `stages/gw-read.md`，FR-22）：子 agent 读 content.md，按 gw-read.md 结构化提取 7 子表（含问题提取 M/C/A+四判据）
7. 精读 2-3 篇后：问题清单 Q# 从精读浮出 → 过四判据 → FR-21 验缝 → 选 1 个进 Step 4a
8. 同步更新本文件 GW Progress 表 + literature_notes 进度表

## §9 失败恢复

见 `templates/master-state-template.md` §9。恢复优先级：本文件 → `.sessions/` 最新 H### → stage file → decision_log。
