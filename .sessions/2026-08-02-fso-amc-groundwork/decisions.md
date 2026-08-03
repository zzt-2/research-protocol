# Decisions — 星地相干 FSO AMC Groundwork

> 架构决策、方向选择、路线失败记录。每条有取代/被取代字段形成血缘链。旧决策标 `superseded` 不删。

## D001: 新系统层范围与旧轴边界

> 2026-08-02 | status: active | 取代: 无 | 被取代: 无

**决策**: 本专题范围 = 星地相干 FSO + Gamma-Gamma 湍流 + 真实编码链/信息不确定性背景下的**自适应编码调制 (adaptive modulation and coding, AMC) 或链路适配**问题，作为毕业论文潜在第二项贡献的独立 Groundwork。明确**不属于**旧 receiver method-production campaign（载波同步/均衡/双偏振）；旧 campaign 的 negatives 不是 AMC 证据，旧工程资产（P08-R2 LDPC/prefix-LS/bit-true/info-boundary）只作可复用工程资产，不引用为 AMC 科学结论。

**边界（继承历史 dead-end，逐条见 topic-index dead-end ledger）**:
1. 不复活 ISL AMC prediction（确定性信道输给简单方法，`domain-comms.md:243-247`）。
2. 不复活链路自适应反馈环（反馈延迟 > 相干时间 2-10ms，TL-03）。
3. 不重新包装 ③ MCS 排程窄切片（oracle 上界 0.09 dB）。
4. 不复活"AMC + CPR 联合设计"（ω_n 跨调制一致使前提崩塌，C4-12）。
5. 不把自适应交织/纯PS/N1/coded-chain repair 换名冒充 AMC。
6. 不把 P08-R2 工程资产当 AMC 科学证据。
7. 新 AMC 须不同系统层真实动作，不能是既有 DA/NDA 自适应 CPR 换名。
8. 检索须识别并排除 "automatic modulation classification" 假命中。
9. 须解耦 AMC↔Ch4 BER 循环依赖（前馈或独立量度）。

**依据**:
- 用户执行提示词 §四"必须继承的历史边界"（8 条）。
- FR-26 核验：8 条中 #1/#2/#3/#6/#7/#8/#9 + #4 经 grep/Read 在 cited 文件确认；#5 经 registry 专题边界确认（详见 topic-index dead-end ledger 证据指针列）。
- `method-production-campaign-thesis-map.md`（A/B/C 级资产分级）。
- master-state.md §2 当前控制面桥接（AMC 须另开专题）。

**触发原话**: 无（技术推导 + 用户执行提示词派发；用户本轮未给态度原话，voice.md 记执行提示词关键约束 verbatim）。

**影响**: 锁定本专题范围与旧轴隔离；R001 候选族须逐条对照本决策的 9 条边界打勾。

## D002: Step 1 科学完整性限定修复 — 候选族修订 + identity 审计 + provenance receipt

> 2026-08-02 | status: active | 取代: 无（修订 R001 候选族地图与 Step 1 计数口径，不取代 D001 范围） | 被取代: 无

**决策**: 对 GW Step 1 做**限定完整性修复**（不撤销 Step 1）。Step 1 状态从 `STEP1_DONE` 修订为 `STEP1_ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR`。具体修订：

1. **候选族地图从 4 族（F1-F4）合并为 3 族（A/B/C）**。原 F4（相干物理信息 AMC，锚 L124）不再算"机制不同的第 4 族"，因为 L124 官方身份（Optics Express 34(14):26128, 2026, DOI 10.1364/oe.595557）确认它**是一个真实的 coherent-FSO AMC 论文，AMC action 真实**（modulation selection driven by multi-dim CSI [SNR, scintillation index, phase variance]），即 L124 是 A 族（MCS/功率控制）的一个相干相位的实例，而非独立机制族。修订后：
   - **A_MCS_POWER_CONTROL** = instantaneous-CSI 分支（原 F3）+ delayed/statistical/uncertain-CSI 分支（原 F1）合并，因真实 action 相同（调制阶数/码率/功率切换）。
   - **B_HARQ_IR_RATE_ADAPTATION** = 原 F2，真实独立 action（IR-HARQ 重传+速率+功率），文献密集，当前更像 ENGINEERING_COMPONENT 候选。
   - **C_COHERENT_TX_ADAPTATION_UNVERIFIED** = 原 F4（L124 + L165），在 L124 全文身份/action/coding/CSI/channel/scenario 闭合前不算正式候选族（pre-fix 状态 `UNVERIFIED_BIBLIOGRAPHIC_HIT`）。
2. **F1 headroom 纠正**：F1（现 A 族的 delayed/statistical CSI 分支）**并非完全避开**旧 0.09 dB MCS 天花板（dead-end#3）。它与旧路线共享长时间尺度信息驱动的 MCS/码率切换，新增点只是"不确定信息约束"，headroom **未证**，须 Step 4a 维度 D 的 oracle 上界（FR-21）核算。
3. **"直接竞品 0 篇确认"改为 `CURRENT_SEARCH_DID_NOT_CONFIRM_A_DIRECT_COMPETITOR`**：4 个 alias collision query（coherent FSO ACM ModCod satellite / optical feeder variable-rate FEC / FSO rate-compatible LDPC puncturing / satellite optical DVB-S2X ACM）共 32 命中，0 直接竞品；但 Exa 402 透支 + OpenAlex 0 命中 + S2 限速，覆盖有 caveat，不把搜索未命中解释成真实空白（FR-23）。
4. **title-abstract identity 审计结论**：6 个 normalized-abstract 重复组覆盖 18 条 hit，根因是 Exa/SerpAPI abstract 抓取污染（少数通用 survey 摘要被反复注入到不同标题的条目）。受影响 shortlist/flagged 条目：**L124（abstract 是 6G-roadmap，真实 abstract 经 Crossref 确认为 coherent-FSO AMC）/ L020 / L038 / L090**。这些条目的 abstract 不可信，须用 title+DOI 定身份。
5. **L038 标签纠正**：原标 `chinese-FSO-AMC` 错误——L038 标题是英文，DOI 10.1080/24751839.2026.2637258（Taylor & Francis，非中文刊），应标 `IM/DD-FSO-AMC`（与 L020 同组）。其 abstract 同样是污染的 OWC-survey 文本。
6. **L070 标签一致性**：L070 文字声称属"mod-classification 排除 5 条"之一，但其 pri 是 `备选`（未排除）。修订：L070 维持 `备选`，文字改为"borderline demod/AI-mod survey，非纯 classification，pri=备选（保留观察）"，与 pri 一致。
7. **provenance receipt**：`search-archive/2026-08-02/_step1_receipt.json`（force-add）固化检索合同、raw 文件 SHA256、shortlist provenance、L124 官方身份、alias repair 结果、确定性重放命令。raw JSON 继续 gitignored，但 receipt 使 clean clone 至少能恢复检索合同与哈希。

**保留 V001**：V001（Step 1 原 12 项 checklist）仍 PASS 12/12，但明确它**漏审 title-abstract identity 和 source provenance 口径**（V001 Check 3 把 manifest published=153 当 cosmetic 误差，未追到 _alldigest 真值 115；V001 未做 normalized-abstract 分组审计）。新增 V002 记录本次修订血缘。

**依据**（证据链，FR-26）:
- 确定性重算脚本 `tools/amc_step1_recompute.py` + 输出 `tools/_amc_step1_recompute_out.json`（从 raw JSON 重算：32 文件=17 unique query / 16 非零；published 115/209=55.0%；6 dup-abstract 组覆盖 18 条；priority 分布 必读10/建议读17/待确认4/备选57/排除121）。
- L124 官方身份：Semantic Scholar Graph API（exact title match, with S2_API_KEY）+ Crossref `/works/10.1364/oe.595557`（title/authors/Optics Express 34(14):26128/abstract）双源交叉验证。OpenAlex HTTP 429 不可用，但不影响双源确认。
- 4 alias collision query：`search-archive/2026-08-02/{coherent-fso-acm-modcod-satellite,optical-feeder-link-variable-rate-fec,fso-rate-compatible-ldpc-puncturing,satellite-optical-dvbs2x-acm}.json`（SHA256 见 receipt）。
- `_step1_receipt.json`（23KB，json parse OK，raw hash 与磁盘一致）。

**触发原话**: 无（技术推导 + 用户执行提示词 §三 Phase A 限定修复指令；用户本轮 voice 见 voice.md "2026-08-02 Phase A 执行提示词" 段）。

**影响**: Step 1 修订为 ACCEPTED_AFTER_BOUNDED_INTEGRITY_REPAIR；候选族数从 4 降为 3（A/B/C）；L124 在 Step 2 必须得到确定身份结论（全文）；Step 2 shortlist 不变（12 篇），但 L038 标签与 L124 身份状态更新；进入 Phase B（Step 2 acquisition）。

## D003: Step 2 覆盖纠偏 — STEP2_BLOCKED_BY_COVERAGE_GAP，保守核心集缩窄，补充获取后再判 PASS

> 2026-08-02 | status: active | 取代: D002 关于"Step 2 PASS / 6 篇合格 / A/B/C 三族覆盖"的判定（不取代 D002 的 Step 1 限定修复与候选族修订） | 被取代: 无

**决策**: D002/R002/H001 将 GW Step 2 判为 PASS（6 篇合格 content.md 覆盖 A/B/C 三族）。主控复核后判定该 PASS 不成立——**Step 2 状态修订为 `STEP2_BLOCKED_BY_COVERAGE_GAP`**。具体纠偏：

1. **保守核心集缩窄到 3 篇**（不是 D002 宣称的"6 篇覆盖三族"）。6 篇只通过文件/转换质量门（content.md ≥50 行 + 身份闭合），但**未做 CORE 判定**。逐篇重判后保守 CORE 集：
   - **L023**（JLT 2023，CSI-driven mod+power+MIMO）—— CORE：运行时可部署 AMC action + 湍流场景 + 直接 comparator。
   - **L096**（IEEE TVT 2022，FSO sat IR-HARQ + rate adapt）—— CORE：运行时 HARQ-IR/rate action + FSO sat + 直接 comparator。
   - **L146**（IEEE IoT J 2025，robust MCS + imperfect CSI）—— CORE：运行时 MCS/功率 action + imperfect-CSI 条件 + 直接 comparator。
2. **L075 改标 `SEMANTICALLY_DISPUTED_PENDING_FULL_READ`**（不是"实为 classification 已定论"也不是"DL AMC 对照"）。其 abstract 明提"to classify real-time modulation schemes…accuracy 96.3%"（→ 倾向 classification，dead-end#8 族），但**不预判为纯 classification**，也不提前计入核心；留待 Step 3 全文语义仲裁。
3. **L165（AO/物理实验边界）、L090（STTC，是否真实运行时 adaptation 待全文核查）不计核心**——它们的 action 在 AO/物理层或边界，不构成 AMC 核心证据。L090 的 DOI/manual 路径问题（实为 IntechOpen DOI 10.5772/intechopen.84911，原短名单 manual slug 误导）须修。
4. **L124 是 coherent-FSO AMC 的关键直接竞品**（Optics Express 34(14):26128, DOI 10.1364/oe.595557，bibliographic 级确认）。**没有全文时，coherent-C 族不得通过问题/新颖性判断**——保留状态 `C_L124_FULLTEXT_BLOCKED`。
5. **允许在 ≥5 篇真正 CORE 全文齐备后推进 A/B 两族的 Step 3，不允许因 L124 付费墙让全部 Groundwork 无限停滞**；但 C 族（coherent）必须显式保留 BLOCKED，不得用 abstract/题目推导 coding/CSI/channel/方法空间。
6. 本决策**不改写历史 checkpoint**：D002 的 Step 1 限定修复（候选族 A/B/C、identity 审计、provenance receipt）保留；R002/H001 加 supersession banner，不删历史。

**补充获取目标**（确定性，先查仓库历史索引与旧专题，不直接从零搜索）：
- **Safi 2019**（已在 `all-papers.jsonl` 命中：DOI 10.1109/tvt.2019.2916843，IEEE TVT，cite 58；abstract 明证：adaptive channel coding + power control + Gamma-Gamma + **channel estimation error**）——关键 baseline，很可能已覆盖"GG + channel-estimation error + adaptive coding/power"，**不得再把这一宽泛问题包装成空白**。
- **Chang 2025**（Integrated FEC/Interleaving/ARQ/Adaptive Modulation for maritime FSO，DOI 10.1109/JPHOT.2025.3602148）——须核实正式题名/DOI/venue/年份。
- **Sun 2018**（Run-time reconfigurable adaptive LDPC for optical channels，DOI 10.1364/OE.26.029319）——须核实。
- **Galijasevic predictive adaptive LDPC**（已在 `all-papers.jsonl` 命中：DOI 10.1109/OJCOMS.2024.011100，IEEE OJCOMS 2024，UCLA/JPL，NSF PAR 预印本；abstract 明证：linear/quadratic prediction 动态选 LDPC code rate，feedback delay 0–4 ms）——很可能已覆盖"反馈时延/信道预测 + 动态码率"，**必须确定剩余切片**。
- **L124**（DOI 10.1364/oe.595557）——尝试 publisher/作者稿/机构仓储/Crossref-S2 OA 地址等合法路径，**最多三类路径，失败即止损，不绕过访问控制**。

**CORE 判据**（每篇候选同时满足才 CORE）：
- action 是运行时可部署的 modulation/coding/rate/power/HARQ/link adaptation；
- condition 是 FSO 信道、CSI 不确定性、反馈时延或湍流状态；
- 不是仅分类、固定方案比较、AO、固定编码或事后分析；
- 能进入 AMC 问题 M-C-A 或成为直接 comparator。

**达到 ≥5 篇 CORE 后 Step 2 才 PASS**；否则停在 Step 2 诚实汇报缺口，不用非核心论文凑数。建立可持久化 acquisition receipt（paper id / 正式身份 / 来源 URL-DOI / source+content 路径 / SHA256 / 获取时间 / CORE|ADJACENT|BOUNDARY|DISPUTED / 判定理由），PDF/content 若 gitignore 不提交则 receipt 必须 force-add 提交。

**Phase B（仅当 Phase A 得到 ≥5 篇 CORE）**：进 Step 3 全文精读，至少精读 L023/L096/L146 + Safi2019 + 新获取 Chang/Sun/Galijasevic 中最直接 ≥2 篇 + L075 语义仲裁 + L124（若获全文则最高优先级直接竞品精读）。每篇按 gw-read.md 完整模板提取，产出 AMC 专属 literature_notes（不覆盖旧 receiver 记录）、直接竞品矩阵、Q# 表（至少 1 个 Q# 四判据全过 Step 3 才完成；无则终态 STEP3_NO_VALID_PROBLEM，不包装空白、不设计方法）。

**依据**（证据链，FR-26）:
- 用户 Phase A+B 执行提示词（paste-attachment 2026-08-02-230536）§"必须先登记以下主控裁决"。
- `search-archive/_index/all-papers.jsonl` grep 命中：Safi（DOI 10.1109/tvt.2019.2916843，cite 58，abstract 明证 GG+coding+power+estimation error）/ Galijasevic（DOI 10.1109/OJCOMS.2024.011100，abstract 明证 prediction+LDPC rate+feedback delay 0–4ms）。
- D002/R002/H001（原 Step 2 PASS 判定的被取代对象）。
- FR-22（GW 流程强制）/ FR-23（增量改进非填补空白）/ FR-26（证据链强制）/ TL-32（Go/Kill 标准分离，oracle 上界不当 Go 判据）/ TL-33（证据链）。

**触发原话**: 无（用户执行提示词派发主控裁决；用户本轮 voice 见 voice.md "2026-08-02 Phase A+B 执行提示词（纠偏轮）" 段，登记后补）。

**影响**: Step 2 状态从 PASS 修订为 `STEP2_BLOCKED_BY_COVERAGE_GAP`；保守核心集 3 篇（L023/L096/L146）；L075 DISPUTED、L165/L090 边界、L124 C 族 BLOCKED；Phase A 补充获取 5 篇目标（Safi/Chang/Sun/Galijasevic/L124）后重判 Step 2 PASS/BLOCKED；R002/H001 加 supersession banner；V003 独立文件合并进 verifications.md 作 V003 条目。

## D004: Step 2 blocker 解除 — STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED，立即推进 A/B 族 Step 3

> 2026-08-03 | status: active | 取代: D003 的 Step 2 BLOCKED 状态（**不取代 D003 的历史纠偏与 CORE 判据**，D003 第 6 点所列"L124 保留 C_L124_FULLTEXT_BLOCKED / Safi PROVISIONAL / L075 DISPUTED / L165·L090 边界 / 不改写历史 checkpoint"全部继续有效） | 被取代: 无

**决策**: D003 判定 GW Step 2 = `STEP2_BLOCKED_BY_COVERAGE_GAP`（CORE 全文 4 < 5 门槛）。本轮（2026-08-03）用**仓库主工作区已有历史全文** Nguyen 2024 解除该 blocker。Nguyen 2024 身份独立验证 + 规范迁入当前 worktree 的 canonical DOI 路径 + CORE 判定后，**Step 2 终态修订为 `STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED`**，立即推进 A/B 族 GW Step 3 全文精读。具体：

1. **Nguyen 2024 身份独立验证（Crossref）**：
   - Crossref `/works/10.1109/TAES.2024.3403809` 返回：title="Adaptive Rate/Power Control With ML-Based Channel Prediction for Optical Satellite Systems"；authors=[Tinh V. Nguyen, Hoang D. Le, Anh T. Pham]；container=[IEEE Transactions on Aerospace and Electronic Systems]；volume=60, issue=5, page=7498-7509, published 2024-10, publisher=IEEE, type=journal-article, DOI=10.1109/taes.2024.3403809。
   - content.md H1 标题与 Crossref title 词重叠 Jaccard = **1.0**（完全匹配）；与执行提示词给的正式身份逐字段一致。
   - **不是公开 OA**：content.md 页脚明文 "Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY. Downloaded on May 30, 2026 at 07:31:59 UTC from IEEE Xplore. Restrictions apply." —— 机构 IEEE Xplore 授权下载，**禁止 redistribute as OA**。metadata.json + receipt 的 `provenance` 字段完整保留此来源，**不声称 OA**。
2. **迁移到 canonical DOI 路径**：
   - `papers/downloads/2026-05-30/10535712.pdf` → `papers/doi/10.1109_taes.2024.3403809/source.pdf`
   - `papers/downloads/2026-05-30/10535712.md` → `papers/doi/10.1109_taes.2024.3403809/content.md`（546 行，格式合格，**不重新转换**）
   - SHA256 迁移前后完全一致（PDF `b49f5abf…4c95c51`、MD `27f25473…87103f`），迁移动作零字节改动。
   - 新建 `metadata.json`（含 Crossref 身份、license_note="NOT public OA"、identity_verified_by、core_judgment=CORE）。
3. **Nguyen 2024 CORE 判定（全文证据，action/condition/deployability）**：
   - action = 运行时联合自适应 rate（subcarrier K-QAM 星座大小 K∈{4,8,16,32,64,128}）+ TX power（离散 EDFA 增益），per equal-duration channel state，由预测 CSI 驱动；AMP（理想连续功率）+ SAMP（离散功率，Algorithm 1-3）两 scheme。
   - condition = LEO-satellite-to-UAV FSO 链路 + **弱湍流 lognormal 闪烁（Rytov variance，UAV<1km 论证，**非 Gamma-Gamma**）** + Beckmann 指向误差（非零均值 misalignment，modified-Rayleigh 近似）+ **outdated 反馈 CSI（LEO 反馈时延数 ms > 相干时间 <1ms）**由 ESN 多步信道预测克服。
   - deployable = 运行时 TX-side AMC controller（QAM 调制器 + EDFA），非 classification/AO/fixed/post-hoc。
   - objective = min 平均 TX 功率 under requested-rate + targeted-outage + targeted-BER + Pmax 约束，max 能效；key = AM/AMP/SAMP 对照（AM-vs-SAMP ~0.85dB @1Gb/s，SAMP 接近理想 AMP），ESN 在反馈时延下胜 ARMA/LSTM/Ridge。
   - **关键覆盖缺口（AMC 目标 = 星地 coherent/GG/coded-chain/information uncertainty）**：Nguyen **非 coherent**（subcarrier K-QAM 瞬时 BER `0.2exp(-Pt²h²/(2σn²(K-1)))` = IM/DD-style SQNR-M² 约定，γ∝h²，**非 coherent 检测**）；**非 Gamma-Gamma**（弱 lognormal）；**无 coded chain**（action 是 rate+power，HARQ 仅作 related work [8] 引用，**不进 action**）。→ Nguyen 是 family-A（delayed-CSI/predictive rate+power）的直接竞品，**但与 coherent/GG/coded-chain 目标存在结构性差异**——这些差异是 Step 3 直接竞品矩阵区分它与目标的依据，**不是空白**。
4. **CORE 全文 5 篇门槛成立**：L023/L096/L146/Galijasevic（D003 已全文 CORE）+ Nguyen2024（本轮）= **5 ≥ 5**。Step 2 PASS（A/B 族）。
5. **C 族（coherent TX-side AMC）保持 BLOCKED**：L124（DOI 10.1364/oe.595557）全文仍未获（Optica gold-OA 但 Radware bot-block，无 author preprint）。**无 L124 全文时，coherent-C 族不得通过问题/新颖性判断**，C 族 Q# 不得过 novelty closure（沿用 D003 第 4/5 点）。本轮 Step 3 可建立 L124 的 bibliographic-only 条目（标题/DOI/venue/abstract 级），**但不得用 abstract/题目推导全文 coding/CSI/channel/方法空间**（FR-26）。
6. **Safi 2019 保持 PROVISIONAL_DIRECT_COMPETITOR**：abstract 级 CORE（adaptive coding + power + GG + channel-estimation error）但 IEEE paywall 无全文。**不计 5 篇门槛**，Step 3 只能使用可验证 abstract/bibliographic 信息，**不得据摘要推导实现细节**。
7. **不改写历史 checkpoint**：D003 的 CORE 判据、CORE 定义、L075 DISPUTED、L165 AO 边界、L090 fixed-STTC 边界、3 路径止损记录、持久 receipt 全部保留；本决策**只取代 D003 的 BLOCKED 终态**，不动 D003 的科学纠偏内容。`_step2_acquisition_receipt.json` 加 `last_updated_at` + Nguyen 条目 + coverage_summary 更新（保留 superseded_verdict 字段不删 BLOCKED 历史）。
8. **literature notes owner 路径**：旧 `projects/thesis-fso/literature_notes.md`（197KB receiver 产物）**不覆盖**。AMC Step 3 产出写入**专属 owner** `projects/thesis-fso/literature_notes_amc.md`（与 receiver notes 同目录但独立文件，避免覆盖/混淆）。每篇精读同步 `papers/_read_notes/{paper_id}.md`，并在 receiver 项目 `read-log.md`（或新建专题级 read-log）追加一条。

**依据**（证据链，FR-26）:
- 用户本轮执行提示词（2026-08-03，paste-attachment）§Phase A 第 1-4 步 + "关键新事实必须先独立验证"段（Nguyen 仓库历史全文路径 + 正式身份）。
- `papers/doi/10.1109_taes.2024.3403809/{source.pdf,content.md,metadata.json}`（本轮迁移创建；content.md 546 行格式合格；SHA256 与主工作区原始一致）。
- Crossref API `/works/10.1109/TAES.2024.3403809`（身份逐字段匹配，URLError 无）。
- `_step2_acquisition_receipt.json`（12 papers，coverage_summary.core_with_fulltext=5，step2_verdict=STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED，json parse OK）。
- D003（被取代的 BLOCKED 状态；CORE 判据与历史纠偏继续有效）。
- FR-22（GW 流程强制）/ FR-23（增量改进非填补空白）/ FR-26（证据链强制）/ TL-31（先读 decisions+thesis-lessons，本轮已读）/ TL-32（Go/Kill 标准分离，oracle 上界不当 Go 判据）/ TL-33（自欺式跳步防护，身份用 Crossref 独立验证不靠联想）。

**触发原话**: 无（用户执行提示词派发 Phase A 解除 blocker；用户本轮 voice 见 voice.md "2026-08-03 本轮执行提示词关键约束" 段，已 verbatim 登记）。

**影响**: Step 2 终态 `STEP2_PASS_WITH_COHERENT_C_FAMILY_BLOCKED`；A/B 族获权进 GW Step 3 全文精读（本轮 Phase B 立即执行）；C 族保持 BLOCKED；Safi 保持 PROVISIONAL；registry last_updated + master-state §2 AMC 指针 + topic-index GW Progress 表 Step 2 行更新；R002/H001 不再加新 banner（D003 banner 仍保留，D004 是 D003 blocker 的解除而非推翻）。
