# CCISP 2026 论文整稿闭环

> 状态：active | 创建：2026-07-14 | 最近更新：2026-07-17

## 范围边界

### 原始目标

解决当前 CCISP 2026 论文“名义 PDF 页数够，但实质正文只有约三页半”的问题，在不灌水、不编造数据、不靠异常浮动图和参考文献凑页的前提下，补足达到 CCISP 官方最低篇幅所需的真实论文内容，并保证专业性、论证完整性和数据口径一致。

### 当前范围

- 第一轮仅完成 `INTAKE -> DIAGNOSE -> PROPOSE`。
- 用当前权威 LaTeX 源重新构建并逐页检查 PDF，量化名义页数与有效正文。
- 复用既有写作研究和至少 5 篇可比通信会议论文，建立 benchmark 内容矩阵。
- 建立专业性审计、事实矩阵、论证链、根因表和候选补强包。
- 形成具体 change contract，等待用户明确批准。
- 按 D001 将正文验收下限调整为至少 3,500 词，重算净增量和公式职责，形成修订版 `CCE-CC-002`。
- 按 D012 闭合 Fig.5 common-768 权威证据链，并分别完成图资产、四个门面/结果 section 的受限修订和整稿验证。
- 按 D016 仅允许 A1+ 候选参数复算与诊断性小切片，评估是否值得另立正式全量重跑合同；路线 B 为目标 receiver 架构。
- 按 D017 将诊断范围收窄为三档 Family 1 下行 old-vs-new 与路线 B/A 等价筛选；上行暂停。
- 按 D018 完成三档下行参数一手证据、正式 `params.py`、AWGN+三档 downlink fixed/A/B 全量、删除 CCISP uplink 评估、三张定量图、adaptive CPR 图文和 fresh independent verification；以 T018 为批准的执行合同。
- 按 D022 将投稿工程、内容/结果闭环和当前 Fig.1 布局返工统一收口到本专题；旧投稿骨架与字体专题只保留为历史证据，不再作为活动入口。
- 按 T019 只重构 Fig.1 的布局、视觉层级、字形和留白；冻结科研语义、节点/边端点与技术图元，并与其他整稿文件隔离执行。
- 2026-07-17 起新增反馈治理阶段：从 `ccisp_v1 批注.pdf` 提取导师关于篇幅、删句、格式、内容、图表和参考文献的完整意见；先由用户校正原意，再规划哪些意见升级为可复用 Skill 规则，哪些只做本篇局部修改。当前不执行 Skill 或论文修改。

### 明确不含

- D018 已批准正式参数、全量仿真和论文 WRITE，但必须按 evidence -> formal verifier -> WRITE 顺序；未过前门不得提前改结果叙事。
- 不修改 selector/CV/1.10 margin/13 dB/CPR/消歧/seed/window/metric；不根据正式结果调参或删点。
- 不以浮动图、参考文献、异常留白或纯排版手段冒充实质内容补足。
- 不编造数据、引用、物理归因、实现细节或比较结论。
- 不把本专题内容扩写塞回 `2026-07-13-ccisp-submission-prep`。
- 不顺手解决批准合同之外的历史债务。
- 不删除全局 uplink 参数字段、历史脚本/JSON；只从 CCISP 正式评估、图和论文叙事中移除 uplink。
- Fig.2 是用户独立维护资产；执行对话只集成和验收当前版本，不覆盖用户 diff。
- 不再为单张图、单次排版返工或同一论文的局部修订新开 CCISP 专题；除非任务具有独立长期生命周期且用户明确批准。

### 范围变更记录

- 2026-07-14，D001：正文目标由 `CCE-CC-001` 提议的 2,500–2,900 词改为至少 3,500 词；原因是用户确认低于该值无法满足页数需要。批准前仍禁止 WRITE。
- 2026-07-14，D007：范围增加双 Skill 实现真实性门禁改造；原因是用户明确批准修补本轮暴露的流程漏检。仍不包含论文、参考文献、仿真、数据或图资产修改。
- **2026-07-15** D012：将 Fig.5 common-768 证据闭环、重画和全文受限修订纳入当前范围。
  - 原因：R004 证明旧 mixed population 指标不公平；R005 给出 30-seed common-768 正证据，但 D011/半成品仍存在 estimand、CI、因果和 26/29 语义分叉。
  - 新范围：允许一次不改算法/判据/参数的 30-seed 权威结果重建；随后图、文分开执行，主控统一验证。
  - 影响的未决项：取代“等待旧 full-block 轴名修复”，转为等待权威 JSON、Fig.5 CI 图和全文指标闭环。
- **2026-07-15** D013：Fig.5 从 5/10/15 dB 九点扩为 5--25 dB、2 dB 间隔的 33 个场景点，并统一三张定量图的横轴为 data-symbol $E_s/N_0$ [dB]。
  - 原因：原网格未完整覆盖 16.9/18.0 dB 交叉区和论文定义的正常工作区；用户要求先对标同领域论文符号，禁止自行造符号。
  - 新范围：允许一次不改算法/判据/参数的 30-seed 网格扩展，以及随后的权威数据、Fig.5、定量图轴和有限正文同步。
- **2026-07-15** D016：增加路线 B receiver 与 A1+ 参数重标定的诊断性小切片。
  - 原因：V011 已证明 B 在旧参数下可真实先选后跑并保持 selected 端 bit-exact；R008b 证明五个旧参数均缺可靠来源，需在全量重跑前先验证强证据候选的方向性。
  - 新范围：允许 T016 复算候选参数，并在不修改正式 `params.py`、算法、阈值和论文的前提下运行 5 SNR × 3 seed diagnostic probe；若参数真相源纪律无法满足，则停在复算阶段。
  - 影响的未决项：D015 被 D016 取代；旧参数结果冻结为历史证据。T016 返回前不批准正式参数替换或全量重跑。
- **2026-07-15** D017：将五档 A1+ 诊断改为三档新下行先筛。
  - 原因：selector 的直接证据本来只在下行；两档 uplink 不是通行 GG 分档且不承担核心 selector 验证。先看三档能否独立支撑可避免继续扩大非核心上行模型范围。
  - 新范围：允许 T017 运行 3 scenes × 5 SNR × 3 seeds × 400 windows 的 old/new A evaluator 与 new B receiver diagnostic；仍不修改正式参数源、论文、图或旧权威数据。
  - 影响的未决项：D016/T016 被取代；若 R015 promising，下一轮才决定删除 uplink 并批准三档正式全量重跑。
- **2026-07-15** D018：R015 六门全 PASS 后批准三档下行 route-B adaptive CPR 正式全流程闭环。
  - 原因：Family-1 三档保留 DA/NDA 互补、selector 方向和 A/B exact；uplink 不承担核心 selector 证据且缺通行分档来源。
  - 新范围：先闭合 Al-Habash/Family-1 本地证据，再正式更新三档 `params.py`、运行 AWGN+三档 downlink fixed/A/B、重建图、删除 uplink/旧数字/26-of-29 并完成论文终验。
  - 影响的未决项：D008/D009 的旧代理/旧主结果及 D013 的旧参数数据失效；D014 方法身份继续有效。普通故障持续排查，科学硬门按 T018 §7 阻断有利叙事。
- **[2026-07-16] D022**：将 CCISP 投稿骨架、内容闭环和后续图文返工收口为一个活动专题。
  - 原因：用户指出同一论文被拆成多个散碎专题，活动入口和任务关系难以辨认。
  - 新范围：本专题成为 CCISP 论文唯一 active/canonical 入口；投稿骨架和字体专题关闭归档；刚建立但未执行的 Fig.1 专题迁为 S002/T019 后撤销。
  - 影响的未决项：Fig.1 A/B 布局选择与最终验证继续由 T019 管理；后续验证编号从 V020 开始。
- **2026-07-17** 用户明确扩大范围（待形成 D###）：将导师批注 PDF 的完整提取与 Skill 修改规划纳入当前专题。原因：批注覆盖篇幅、句子取舍、格式、内容、图表、引用和作者元数据，无法只作为本篇论文的零散修补处理。当前仅记录与分层，不执行 Skill 或论文修改。

## 进展线索

- S001：完成 INTAKE/DIAGNOSE/PROPOSE。当前源强制重建为 6 页，正文 2,219 词、有效正文约 3.0–3.2 双栏页；确认 G6 浮动体失衡、G4 指标/实现冲突和 G7 贡献错接。R001 提出 `CCE-CC-001`，等待用户批准。
- S003：完成导师批注 PDF 的 7 页/45 个可见批注提取，并接收用户对引言高亮范围、明确删除句、HD-FEC、Fig.3--5 图例适用范围、正好 5 页和作者信息的逐字纠正；下一步是用户确认清单后制定 Skill 修改合同。
- R001：五篇 benchmark、有效内容量测、专业性/事实/论证链、根因表、候选补强包和正式 change contract。
- D001：用户将正文验收下限调整为至少 3,500 词；公式只在三门通过且有明确论证职责时采用。
- R002：提出三种 3,500 词架构；推荐方案 A 以约 985 词删除/替换和 2,336 词毛新增达到约 3,570 词，并将公式限制为 8–9 个有职责的 displayed groups。形成 `CCE-CC-002`。
- V001：独立复核 `CCE-CC-002` 的算术、代码证据、公式总账、证据门和降级边界，最终 PASS；公式口径修正为 8–9 组。
- D002：冻结“内部完整审计、外部只呈现有利且可证实内容”的分层规则；内部风险标签、弱场景、失败路线和证据债务不得进入论文。
- R003：Batch A 初判 switching 公平性 FAIL，后经历史回查确认漏读 D005/D006；总体结论已由 D004/V003 取代。
- D003：曾因误用 full/net 口径冻结 WRITE，现已被 D004 取代。
- V002：原 Batch A 总体 FAIL 已被 V003 取代。
- D004/V003：恢复历史最终 data-BER 口径；A4 fixed JSON 确定性复算 26/29，WRITE 恢复且无需新仿真。
- D005/V004：五条短图题 PASS；标题层级总体规范，但三项实现真实性 G4 已由源码/历史闭合，投稿级交付暂停。
- D006/V005：参考文献排除；全部 LaTeX 真实性修复 PASS，Fig.5 图内纵轴旧 `BER reduction` 标签使整体保持 PARTIAL。
- D007/V006：paper-writing/sim-preflight 三联卡、调用链证据与三类阻断锚点实施完成；结构契约、标准 validator 和独立 RED/GREEN 行为压力均 PASS。
- V007：当前稿论证与专业性表面 PASS/PARTIAL，但实现真相终审 FAIL：26/29 为聚合 BER 接近度反推而非直接决策统计；1.3/1.2/1.9 dB 的 total-energy 坐标语义写反；Fig.5 error population 不对称且图内仍用旧 BER 轴名。
- D008：用户批准保留 `26/29` 为 Results 中一次 aggregate selected-output alignment 辅助证据；禁止写成 `26/26` 或称为选择准确率/正确恢复，且不在摘要、引言、结论反复放大。
- D009：用户批准双坐标呈现；1.3/1.2/1.9 dB 为 data-symbol-SNR 差值，2.5/2.4/3.1 dB 为加入 1.249 dB 导频项后的 total-energy-equivalent advantages，摘要 headline 使用最高 3.1 dB。
- T010：Fig.5 切换指标历史与语义专项审计任务已创建；要求新对话只读核查 D002/D005 冲突、metric signature、现有 JSON 可恢复性、pilot-overhead 记账和四条投稿路线，产出 R004 后再拍板。
- D010：用户批准 CCE-CC-003A；先实施 SNR 双坐标、calibration 来源/冻结边界和门面段降噪，Results 中 26/29/Fig.5 保持不动等待 R004。
- V008：CCE-CC-003A 局部 PASS；纯正文 3526 词、7 页、8 组公式，undefined/overfull 为 0，独立审查新增 Critical/Important/Minor 为 0。整稿因 D010 排除的 R004/Fig.5 与 26/29 语义仍为 PARTIAL。
- R004/R005/D011：旧 mixed 指标经审计被否决，30-seed common-768 九点验证支持保留 Fig.5；D011 因统计中心、CI、因果和影响范围未闭合被 D012 取代。
- D012/T011--T013：冻结 paired-seed mean+t-CI 口径；先闭合权威 JSON，再分别重画 Fig.5 和修订 Abstract/Introduction/Results/Conclusion，最后由主控整合验证。
- D013/V009：完成 5--25 dB、2 dB 间隔的 33 点 common-768 权威重建；三张定量图统一为 data-symbol $E_s/N_0$，正文与 Fig.5 的 $G_{\mathcal C}$ 闭合，数据/文字/定量图 PASS。整稿终验为 PARTIAL：仅余 Fig.2 dB 域符号和第 8 页稀疏版面两个 Important，无 Critical。
- R006：完成导师五条反馈逐字解码、全文带行号风险映射和三套 Skill 漏检诊断。确认贡献定位与 \((\alpha,\beta)\) 来源为两项 BLOCKED，Fig.2 最终尺寸局部碰撞为已证实缺陷；形成 `CCISP-SKILL-ADVISOR-001` DRAFT。本轮记录到的工具写操作仅指向 `.sessions`；因工作树进入本轮时已脏且无逐文件 hash 基线，非 session 既有改动归属保持 BLOCKED。
- R007：完成自适应 CPR 方法身份、本地命名实例、五组参数历史来源和全文精炼边界复核。推荐以 received-power-aware adaptive CPR scheme/method 为外层身份、two-stage selection 为内部机制；下行三组无可核验直接数值来源，上行两组为 assumption；高置信删减预算约 250--350 词，等待用户拍板，未进入论文 WRITE。
- D014：用户确认 R007 推荐定位；冻结论文身份为 received-power-aware adaptive CPR scheme/method，two-stage selection 为核心内部机制，禁止称新 adaptive phase estimator。本决策尚未授权论文 WRITE。
- T014：创建上行 Gamma--Gamma 参数证据专项，自包含要求新对话检验直接文献、物理映射、可复算设计场景和四条论文处理路线；产出预留 R008，禁止事后合理化和直接修改。
- R008：完成上行两组 (α,β) 证据专项（只读，外部检索与映射复算由独立子 Agent 执行，独立复核 PASS）。直接文献 FAIL（无可比场景命中，Sandalidis 2011/sat.1553 refs [7]-[11] 因付费墙 UNVERIFIED，Trinh2017 无支持）；物理映射 BLOCKED（sat.1553 的 σ_p² 是含 pointing 的 lognormal/combined scintillation index 而非 Rytov；标准映射给 0.15→(13.3,12.7)/0.25→(8.1,7.5)，目标 α<1.2 落入饱和无效区且非唯一）；params.py:158 把 σ_p² 误标 σ²_R 属符号/模型偷换；commit a46e03db 把 +2.48/+3.07 dB 列为选参理由属结果反向背书。四路线：1（exact+直接文献）BLOCKED；2（降级 representative stress-test regimes）PASS 受限且不重跑不删数据；3（物理标定重跑）本轮 BLOCKED 且 σ_p² 本就不可达；4（删除上行）PASS 受鲁但损失导师要求的上行场景。推荐路线 2，需用户批准措辞后进入 WRITE。
- R008b：用户追问"能否找到类似文献"后的五档全重标定调研（只读）。关键发现：①**下行三档同样无来源**（params.py source 是场景描述非引用，Trinh2017 无支持）——用户原假设不成立；②**五个现用值都不在标准 Al-Habash 映射可达范围**（β=0.8/0.9/0.7 < 渐近下限≈0.996）；③存在被广泛复用且公式反算验证的地面 GG 三档表 Family 1（σ²_R=0.2/1.6/3.5→(11.6,10.1)/(4.0,1.9)/(4.2,1.4)，引 Ghassemlooy CRC 2019 + Al-Habash 2001）；④上行无现成 GG 表但有 VERIFIED 的 σ²_R 锚点 Osborn 2021（*Opt.Express* 29(4):6113，1550nm HV5/7 plane-wave σ²_R=0.06天顶/0.21@30°/1.48@10°）。用户选**方向 A（五档全重标定 + 全部结果重跑）**。R008b 形成拟议合同 DRAFT，下行三档已锁（Family 1），上行 σ²_R 取法为关键开放项（A1 Osborn区间内 vs A2 下行强一档 vs A3 工程判断），并指出**上行叙事张力**：Osborn plane-wave 上限1.48 使上行 strong 难以超过下行 moderate(1.6)，与导师"上行远强于下行"冲突。待用户批方向A + 上行σ²_R取法后另批 scope 进入重跑。未修改任何文件。
- R009：`CCE-CC-004 v2` 经独立逐句审查，精炼预算收窄为 307--338 词并 PASS；定位 Batch 因 `method.tex:4` 统一 selected-output 与权威评估实现的真实性缺口保持 BLOCKED，合同当前不可批准。
- R010：形成 `CCE-FIG2-001` DRAFT，仅授权两个 effective-SNR dB 符号与控制带局部几何，冻结 17 条 edge、三 lane、算法和字号，并规定最终论文尺寸 QA；未批准、未改图。
- R011/V010/D015：调用链确认权威实现只做 common-768 error-count mux，未实现 Fig.2 所示 selected phase 或统一复数输出；V010=FAIL。否决 R009 机械换名与 R010 局部图修，D014 仅保留为目标定位，等待真实性路线拍板。
- R012：把不依赖参数/定位/Fig.2 的逐句精炼拆为 `CCE-CC-005` DRAFT，净减 307--338 词，保护信息访问、状态生命周期、公平性、指标和统计边界；可单独批准，当前未 WRITE。
- T015/R013：完成真实 selected complex-output mux 路线评估（只读，独立核验 4 项关键事实均有 exact file:line，确认 R011/V010/D015 结论与当前权威文件一致、行号漂移已修正）。三层严格分开：A=post-hoc complex-output mux（表达/接口闭环，默认 BER bit-exact 不变，不省计算不可部署，解锁 EVM/LLR 下游能力但可能仍不满足导师"估计算法"）；B=branch-routed receiver（先选后跑，最接近 D014 two-stage control 实质，可能省 ~50% branch compute，BER 等价前提与 A 一致，仍不可部署）；C=non-genie online algorithm（新算法 scope，触发 GW/Contract，超出投稿修复）。推荐档=A（最小真实性闭合零 BER 风险），但如实告知 A 局限；`CCE-SEL-001` DRAFT 已就绪待用户三档拍板。事实闭合 PASS，路线可决策性 PARTIAL（需用户/导师判断哪档满足"估计算法"），A 可实现性 PASS（条件性需 scope change 批准重跑网格），可部署性 A/B BLOCKED。
- V011/D016：用户完成路线 B 原型；独立报告在旧参数 33 点 × 30 seed 上给出 990/990 selector 端 bit-exact、selected_rx 20/20 抽查通过，以及一个 weak@5 dB 条件下 74.6% branch-compute 节省。D016 据此采用 B 为目标 receiver，参数采用 A1+，排除 A2/A3；旧数值不再预设为终稿结果。
- T016：创建 A1+ 新参数复算与小切片诊断任务。先以 5% 容差复现物理锚点，再跑 5 SNR × 3 seed old/new 对照并检查 B/A 45/45；产出预留 R014，禁止正式参数替换和全量重跑。
- R014：T016 在 P0 按门禁停止，未运行 BER；该结果暴露一手文献未落盘，不是参数或算法失败。随后 Osborn 与 Kaushal 已补为本地 `source.pdf + content.md`，Al-Habash/Ghassemlooy/Sandalidis 仍缺。
- D017/T017：用户决定先看三档新下行能否独立支撑论文。T017 跳过上行，只跑 5 SNR × 3 seed matched old/new 与 B/A 45-case 诊断，预留 R015；通过后才讨论删除 uplink 与正式全量合同。
- R014：P0 因四项指定本地全文未归档而 PARTIAL；下行 Family 1 三档已确定性复算，上行 Osborn/Kaushal 证据输入与 5% 锚点复现尚未闭合，故未运行 BER probe、未生成 probe JSON/verifier。该结论只阻断当前执行授权，不证伪 A1+；根因为 M1 管道断裂与 R008b 的 FR-26 证据状态标注过强。下一步是补一手文献落盘后只重做 P0。
- T017/R015：用户授权共享信道最小无副作用 `turb_params` 注入口后完成三档 Family 1 matched diagnostic。接口默认路径对修改前 bit-exact，专项 19/19；probe old/new 各 45 case-seed，独立 verifier 确认 A/B 45/45、六门全 PASS，判 `DOWNLINK_ONLY_PROMISING`。该 3-seed 结果仅为方向诊断，不是投稿数字；正式参数落库、30-seed、删除 uplink 和图文闭环仍待新合同。
- V012/D018/T018/H001：独立主控复核 R015 并由仿真管线、论文同步面、任务合同三路只读 critic 交叉审查。正式开跑获批；保留 common 无副作用注入口，正式真相源唯一为 `params.py`；旧 26/29/uplink/全部旧数字退出；新对话按三个宏阶段一次性执行。
- R016/V013：T018 宏阶段一的数学复算与 common 接口 PASS（相关回归 97/97），但 Al-Habash 原文和 Family-1 三个 sigma-R-squared 锚均未形成合法本地全文，按 §7.1 判 BLOCKED；未改 params、未跑 formal、未改图文。
- R017/D019/V014：参数证据门最终裁决并定死。用户手动取得 Al-Habash 2001 合法 PDF（UCF STARS）并归档 `papers/doi/10.1117_1.1386641/`（source.pdf+content.md），公式可核（Eq.13/14/18-19）；Family-1 三档经子 Agent 全文提取 Gu 2022（*Appl.Sci.* 12(7):3331，卫星下行）证实领域惯例为"著作级引 Ghassemlooy CRC 2019，不标表/页"，无需教材全文。D019 冻结三档 (11.6,10.1)/(4.0,1.9)/(4.2,1.4)（σ²_R=0.2/1.6/3.5）与唯一引用措辞，修订 D018 第3条过严的"式号/页码"硬门为"Al-Habash 已闭合 + Family-1 按惯例等效闭合"。证据门解除，T018 可进宏阶段二；用户要求这块定死不再动，禁止再开"找出处"对话。Al-Habash 原典证实 0.2/1.6/3.5 非经典"标准三档"，故引用只说"as given in [教材]"，禁止声称是文献标准值。
- S002/D022/T019：用户纠正专题拆分过细后完成治理收口。Fig.1 设计与执行合同迁入本专题；投稿骨架和字体专题保留为只读历史，不迁移其 S/D/V 编号。

## 已确认结论

### 不变量

- 状态机顺序固定：`INTAKE -> DIAGNOSE -> PROPOSE -> WRITE -> VERIFY -> DELIVER`。
- 第一轮止于 PROPOSE；无用户明确批准，不得修改论文正文。
- 每个拟补内容必须同时通过 benchmark gate、argument gate 和 evidence gate。
- 数据、代码、公式、图表或正文冲突时，相关论点先标 `BLOCKED`，不得用润色掩盖。
- G6 排版问题不得冒充 G1 实质内容补足。
- 新仿真和参数变更仅限 D018/T018 的三档下行正式矩阵；selector、判据、阈值、消歧、seed/window/metric 继续冻结。

### 其他结论

- D023：引用删减实行“论证职责 + 来源质量”双门；同等职责下优先保留 IEEE Transactions/JLT/PTL，禁止为压页机械删除高质量来源，低质量、弱相关或超出 downlink scope 的来源优先退出。
- 当前官方页数约束暂按用户提供的“full paper 5–10 页、双盲”作为待核验输入；若需重新访问官网，必须由子 Agent 获取并返回精简证据。
- `2026-07-13-ccisp-submission-prep` 已登记并于 D022 关闭归档；其投稿骨架事实由本专题继承，但历史 S/V 不搬迁、不重编号。
- 当前 6 页 PDF 仅约 3.0–3.2 个双栏页有效正文；第 5 页图独占，第 4/6 页存在完全空白右栏。
- 当前 2,219 正文词需净增至少约 1,281 词才能达到 D001；原 300–600 词预算已失效，必须用新的内容架构和公式职责重新论证。
- G4/G7 是扩写前置门：1.9 dB 属于 NDA-vs-DA，Fig.4 属于 BER ratio dB，现稿均错接到 switching headline。
- 外部论文不呈现内部问题诊断或自我否定措辞；事实冲突通过删除、收窄或正向重写解决，不通过“主动报忧”解释修改过程。
- 26/29 使用固定估计器各自标准 data-BER；Fig.5 的 2.3/2.0/1.3 dB 使用 switched path 的 1024-bit full-block 归一化，二者不是同一口径。
- NDA BER 评估逐 256 点使用真实 `tx_bits` 选择八重相位旋转；当前不存在“可实现且无需披露”的后续裁定。
- 湍流 selector 每 256 点重启相位 realization；当前正文不得声称其载波相位跨 DSP window 连续。
- 论文实现真实性检查必须分别记录信息访问、指标签名和状态生命周期，并追踪 `paper line -> caller -> callee -> metric/state`；缺项或声称强于实现即 BLOCKED。
- V003 对 data-BER 分母选择本身仍有效，但其“26/29 可确定性重算”不能等同于直接 selector recovery 证据；V007 将当前 recovery 声称重新标为 BLOCKED。
- D008 已被 D018 取代：route B 提供真实 selected output 后，旧 `26/29` 聚合接近度代理从论文删除，不用新参数复刻。
- D009 已被 D018 取代：旧 1.2/1.3/1.9/2.4/2.5/3.1 dB 及 uplink headline 全部失效；只允许回填 formal verifier 支持的新数字。
- CCE-CC-003A 已按 D010/V008 完成：门面段只保留 fixed-estimator 的 3.1 dB 主结果；calibration 参数来源、冻结范围和场景标签不进入选择器均已写明；纯正文达到 3526 词。

## 未决项

- Fig.2 原资产边界已由 D020 的用户授权解除；当前编辑源已修正为 branch command 前置、branch router 先选后跑，并以 0.88\textwidth 嵌入恢复 7 页版式。
- 旧第 8 页稀疏问题已通过等比例收窄三张定量图的最终嵌入宽度闭合；当前 fresh PDF 为 7 页，无空白页。
- 参考文献补充由用户所述其他流程处理，不在本专题当前修复范围。
- 导师所说“应该是估计算法”具体指哪个技术对象尚未确认；在 L6/G7 定位决策前禁止用改标题或换词代替方法定位。
- ~~五组 \((\alpha,\beta)\) 缺直接来源/物理映射~~ → **已由 D019/R017 闭环**：下行三档定死为 (11.6,10.1)/(4.0,1.9)/(4.2,1.4)（σ²_R=0.2/1.6/3.5），按 Gu 2022 惯例引 Ghassemlooy CRC 2019；上行两档已删（D018）。用户要求定死不再动。
- 方法定位已由 D014 拍板：整体称 received-power-aware adaptive CPR scheme/method，selection 作为核心内部控制机制；不得称新的 adaptive phase estimator，`two-stage` 必须限定为 control。
- 精炼已有保守候选边界：优先处理无职责否定、公式后独立复述和方法流程第三次复述，预计 250--350 词；不得删除真实性、公平性和指标定义。
- ~~下行三档正式 WRITE 的唯一前门是 Al-Habash 映射与 Family-1 σ²_R 本地可审计来源~~ → **已由 D019/V014 解除**：Al-Habash 已归档 `papers/doi/10.1117_1.1386641/`，Family-1 按 Gu 2022 著作级引用惯例等效闭合。证据门不再是阻塞项；T018 可进宏阶段二（改 params + 30-seed 重跑），仍守运行真实性门。
- adaptive CPR 定位新增实现真实性门：必须先闭合逻辑 branch routing、双分支评估和 selected metric/output 的关系；不得声称只执行所选分支或已有复数序列 mux。
- R009 的纯精炼逐句表仍可复用，但组合合同已被 D015 否决；不得借“精炼”顺手改方法身份或 Fig.2 语义。
- R012/`CCE-CC-005` 不得机械全量执行；删 uplink/26-of-29 后按正文不少于 3500 词的硬门，只做有职责的精炼。
- Fig.2 已新增三处最终尺寸碰撞事实（分支标签侵入节点/连线、菱形安全区不足）；下一轮图资产合同不得以结构 validator 或字号 PASS 代替局部视觉证据。
- `CCISP-SKILL-ADVISOR-001` 尚未获批；不得修改三套 Skill。
- D018 已拍板 route B + 三档下行正式闭环，A 仅作离线 evaluator；non-genie online ambiguity resolver 仍明确不含。
- Fig.2 用户资产、Al-Habash/Family-1 本地证据、formal 990/990 和最终独立终验是剩余硬门；其余按 T018 持续执行，不重复请求批准。
- Fig.1 布局重构待按 T019 生成 A/B 最终尺寸预览并由用户选择；选定前不得覆盖权威 Fig.1。

## 当前位置

`T018 PASS / V015 PASS / V016 PASS`：D019 三档、fixed 870/870、消歧前 receiver-output A/B 990/990、formal-only 三图和正文均闭合。D020 已完成 Fig.2 route-B 语义修复；V016 又闭合导师所指重复段落、DA/NDA 专业命名和 SEL 符号。当前 fresh PDF 7 页，结构测试、逐页视觉、实现真相与 external-output C1--C10 全部 PASS。
- 2026-07-16 D021/V017：Fig.3 fixed 四场景统一 5--35 dB、2 dB 步长；正式 1920 cells 与独立 verifier PASS，A/B 5--25 dB 网格不变。
- 2026-07-16 D022：本目录现为 CCISP 唯一活动专题；下一项独立任务为 T019 Fig.1 布局重构。
- 2026-07-16 T019/V022：用户选择 A（balanced lanes）；权威 Fig.1 drawio/PDF/PNG 已更新。语义、validator、字体和测试门 PASS；独立视觉审查保留顶部标签贴边、Detected bits 贴角与灰度风险，任务结论 PARTIAL。
- 2026-07-16 V023：删除造成正文截断的强制分页；最新 PDF 中 Section I/II 在 p1 自然承接，Fig.1/Fig.2 分置 p2/p4，fresh build、40 项回归与独立视觉终验 PASS。
- 2026-07-16 V024：接收用户最新 Fig.1 drawio 微调，同源重导 PDF/PNG 并重建全文；修复一处语义边 source 脱绑及一处最终尺寸文字安全间距，validator、字体、回归与独立终验 PASS。
- 2026-07-16 V025：用户明确要求指定 drawio 原样重导；主控撤销 V024 中两处越权修补，恢复用户保存哈希 `CBD59FF2…` 并重导全文。忠实重导完成；原图一处未绑定 source 与 0.32 pt 水平安全间距按用户版本保留，当前资产结论 PARTIAL。
- 2026-07-17 S003：本专题当前阶段已明确为“导师批注证据归档与 Skill 修改规划”，不是立即改论文；完整原话、提取事实、用户纠正和主控分类已写入 S003，待用户复核。
- 2026-07-17 D024：用户批准继续执行；`paper-writing`/`external-output` 已完成导师反馈门禁升级与 RED/GREEN 压力测试，论文进入单一统一修订批次。当前以 21 项反馈账本实施全文同类扫描、图文/引用/作者/精确五页修改，完成后逐条核销并由独立 reviewer 终验。
- 2026-07-17 V026：本次工作定位为“导师批注驱动的 Skill 治理升级 + CCISP 全文同类问题修订”，不是局部改字。Skill RED/GREEN、正式 A/B 当前真相源重跑、三图重建、精确五页 fresh build、逐页视觉 QA 和 21 项独立终验全部 PASS；下一步由用户审阅最新版全文。
- 2026-07-17 续修：用户要求确认 Transactions、文字专业性并将 Fig.2 放回第 3 页。本次仅做已批准的版式/等义压缩修复：Fig.2 已在第 3 页顶部，fresh 5 页与确定性检查保持通过，等待独立 reviewer 对当前页位做 V027 最终核销。
- 2026-07-17 V028：按用户“标题 FSO 豁免、摘要与正文分别定义一次”完成缩写首现修复。引言中的全部正文缩写定义均早于 Fig.1/Fig.2，后文删除重复展开；fresh 5 页与独立 acronym 审查 PASS。
